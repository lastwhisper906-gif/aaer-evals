"""What changed since last quarter, and what is word-for-word the same.

The rule from the input spec: match each paragraph against the previous report
of the same kind with every number replaced by a placeholder. A new or changed
paragraph goes in verbatim. An unchanged one is replaced by the single line
`[same as prior period, n periods running]`. The first report a company has
carries its full text, because there is nothing to compare it to.

**"Compare similarity" is implemented as exact equality of the masked text**,
which is the strictest reading available and the only one that cannot collapse
a real change. A fuzzy ratio would score a paragraph that gained the word
"not" at 0.99 and delete it; a paragraph whose only difference is its numbers
masks to the same string and collapses; a paragraph whose difference is a word
does not.

**Never diffed away**, whatever it says and however often it repeats:
contingencies and litigation, subsequent events, related parties, debt and
covenants, accounting changes and corrections. That is `docs/INPUT_SPEC.md` §2
item 6 and it is a list, not a heuristic — these are the notes where an
unchanged paragraph is itself the finding.

    python3.12 -m src.diff_periods --ticker AAPL --out-notes input_notes.md \\
        --out-mdna input_mdna.md
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    from src import (clean_text, cutoff_guard, extract_notes, html_text,
                     interpreter_pin, split_sections)
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import (clean_text, cutoff_guard, extract_notes, html_text,
                     interpreter_pin, split_sections)

BAD_INPUT = 2

SAME_AS_PRIOR = "[same as prior period, {periods} periods running]"
_SAME_AS_PRIOR = re.compile(r"^\[same as prior period, (\d+) periods running\]$")

# Every number, at any scale or sign, becomes one placeholder.
_NUMBER = re.compile(r"\d[\d,.]*")

# docs/INPUT_SPEC.md §2 item 6, matched on the note's tag name. Written as a
# mapping so the output can record *which* rule kept a note whole.
ALWAYS_VERBATIM = {
    "contingencies_and_litigation":
        r"contingenc|litigation|legalmatter|lossconting|commitmentsandcontingencies",
    "subsequent_events": r"subsequentevent",
    "related_parties": r"relatedparty|relatedpartie",
    "debt_and_covenants": r"debt|borrowing|creditfacilit|creditagreement|notespayable|covenant",
    "accounting_changes_and_corrections":
        r"accountingchange|errorcorrection|newaccountingpronouncement"
        r"|recentlyissuedaccounting|changeinaccounting|restatement",
}
_ALWAYS_VERBATIM = {topic: re.compile(pattern, re.IGNORECASE)
                    for topic, pattern in ALWAYS_VERBATIM.items()}


def always_verbatim(note_name: str) -> str | None:
    """Which always-verbatim topic this note is, or None."""
    flat = re.sub(r"[^a-z]", "", (note_name or "").lower())
    for topic, pattern in _ALWAYS_VERBATIM.items():
        if pattern.search(flat):
            return topic
    return None


def mask(text: str) -> str:
    """The paragraph with its numbers taken out, for matching only."""
    return _NUMBER.sub("#", html_text.normalized(text))


def diff_stream(current: list[dict], prior: list[str], *, periods: int = 2) -> list[dict]:
    """One decision per current paragraph: carried verbatim, or collapsed.

    `current` is a list of {id, text, note, verbatim_topic}. `prior` is the
    previous period's paragraphs, as plain strings.
    """
    seen = {mask(paragraph) for paragraph in prior}
    out = []
    for entry in current:
        topic = entry.get("verbatim_topic")
        unchanged = mask(entry["text"]) in seen
        if unchanged and topic is None:
            out.append({**entry, "kind": "collapsed",
                        "line": SAME_AS_PRIOR.format(periods=periods)})
        else:
            out.append({**entry, "kind": "verbatim",
                        "reason": ("always verbatim: " + topic) if topic else
                                  ("unchanged but always verbatim" if unchanged else
                                   "new or changed")})
    return out


def _note_paragraphs(ticker: str, form: str, role: str, *, cutoff, fixtures_root) -> list[dict]:
    """Cleaned paragraphs of every note, each carrying the note it came from."""
    payload = extract_notes.extract(ticker, form, role=role, cutoff=cutoff,
                                    fixtures_root=fixtures_root)
    out = []
    for section in payload["sections"]:
        topic = always_verbatim(section["name"])
        kept = clean_text.clean_section(
            [section["text"][a:b] for a, b in html_text.spans(section["text"])])
        for paragraph in kept["paragraphs"]:
            out.append({"id": f"{payload['accession']}:notes:{len(out) + 1}",
                        "text": paragraph, "note": section["name"],
                        "verbatim_topic": topic})
    return out


def extract(ticker: str, *, cutoff=None, fixtures_root=cutoff_guard.FIXTURES) -> dict:
    """Diff this company's 10-Q against the 10-Q before it."""
    cutoff = cutoff or cutoff_guard.default_cutoff(ticker, fixtures_root=fixtures_root)
    current = cutoff_guard.one_document(ticker, "10-Q", "primary_html",
                                        fixtures_root=fixtures_root)
    prior_rows = cutoff_guard.documents(ticker, form="10-Q", role="prior_period",
                                        fixtures_root=fixtures_root)
    has_prior = bool(prior_rows)

    notes_now = _note_paragraphs(ticker, "10-Q", "xbrl_instance",
                                 cutoff=cutoff, fixtures_root=fixtures_root)
    notes_before = ([entry["text"] for entry in
                     _note_paragraphs(ticker, "10-Q", "prior_period_xbrl_instance",
                                      cutoff=cutoff, fixtures_root=fixtures_root)]
                    if has_prior else [])

    mdna_now = split_sections.extract(ticker, "10-Q", "mdna", cutoff=cutoff,
                                      fixtures_root=fixtures_root)
    mdna_kept = clean_text.clean_section(mdna_now["paragraphs"])["paragraphs"]
    mdna_entries = [{"id": f"{current['accession']}:mdna:{index}", "text": text,
                     "note": "mdna", "verbatim_topic": None}
                    for index, text in enumerate(mdna_kept, start=1)]

    mdna_before = []
    if has_prior:
        prior_html = cutoff_guard.load_document(prior_rows[0]["full_path"], cutoff,
                                                fixtures_root=fixtures_root)
        prior_mdna = split_sections.split(prior_html, "10-Q", "mdna")
        mdna_before = clean_text.clean_section(prior_mdna["paragraphs"])["paragraphs"]

    notes = diff_stream(notes_now, notes_before)
    mdna = diff_stream(mdna_entries, mdna_before)
    entries = notes + mdna
    return {
        "ticker": ticker,
        "cutoff": str(cutoff),
        "accession": current["accession"],
        "filing_date": current["filing_date"],
        "prior_accession": prior_rows[0]["accession"] if has_prior else None,
        "has_prior_period": has_prior,
        "notes": notes,
        "mdna": mdna,
        "collapsed": sum(1 for entry in entries if entry["kind"] == "collapsed"),
        "carried": sum(1 for entry in entries if entry["kind"] == "verbatim"),
    }


def render(entries: list[dict], title: str) -> str:
    out = [f"# {title}", ""]
    current_note = None
    for entry in entries:
        if entry.get("note") != current_note:
            current_note = entry.get("note")
            out.extend(["", f"## {current_note}", ""])
        out.append(f"[{entry['id']}]")
        out.append(entry["line"] if entry["kind"] == "collapsed" else entry["text"])
        out.append("")
    return "\n".join(out)


def is_collapsed_line(line: str) -> bool:
    """Exactly the placeholder, with an integer in it. Nothing else counts."""
    match = _SAME_AS_PRIOR.match(line)
    return match is not None and match.group(1).isdigit()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="diff a 10-Q against the one before it")
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--cutoff", default=None)
    parser.add_argument("--fixtures", default=str(cutoff_guard.FIXTURES))
    parser.add_argument("--out-notes", required=True)
    parser.add_argument("--out-mdna", required=True)
    args = parser.parse_args(argv)

    ticker = args.ticker.upper()
    try:
        payload = extract(ticker, cutoff=args.cutoff, fixtures_root=Path(args.fixtures))
    except cutoff_guard.CutoffGuardError as exc:
        print(f"diff_periods: {exc}", file=sys.stderr)
        return BAD_INPUT
    Path(args.out_notes).write_text(
        render(payload["notes"], f"{ticker} 10-Q notes — {payload['accession']}, "
                                 f"diffed against {payload['prior_accession']}"),
        encoding="utf-8")
    Path(args.out_mdna).write_text(
        render(payload["mdna"], f"{ticker} 10-Q MD&A — {payload['accession']}, "
                                f"diffed against {payload['prior_accession']}"),
        encoding="utf-8")
    print(f"diff_periods: {ticker} {payload['collapsed']} collapsed, "
          f"{payload['carried']} carried verbatim")
    return 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
