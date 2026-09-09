"""What changed since last quarter, and what is word-for-word the same.

The rule from the input spec: match each paragraph against the previous report
of the same kind. A new or changed paragraph goes in verbatim. An unchanged one
is replaced by a single line naming the paragraph it repeats. The first report
a company has carries its full text, because there is nothing to compare it to.

**"Unchanged" is exact equality of the paragraph's own text, inside its own
note.** Nothing weaker is safe. A paragraph whose only difference is a number
is a *changed* paragraph and is carried verbatim: `docs/INPUT_SPEC.md` §2.3
says a new or changed paragraph goes in verbatim, and a number that moved is
the change a reader of these filings came for. Cycle 19 compared the *masked*
text against a **set** of every masked paragraph in the prior filing, so the
table cell `54,252` masked to `#` and matched any number anywhere. The mask
survives as `src/note_history.py`'s pairing key, where being approximate is the
point. Here it decides nothing.

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

# The placeholder names the paragraph it stands for. `n periods running` was a
# constant 2 on every one of Apple's 1,536 placeholders — nothing counted it —
# and `CLAUDE.md` says Python does the arithmetic. An id is not arithmetic: it
# is the thing a reader needs to check the claim, and it makes each placeholder
# a different line, so a quote of one resolves to one paragraph.
SAME_AS_PRIOR = "[same as prior period, unchanged from {prior_id}]"
_SAME_AS_PRIOR = re.compile(r"^\[same as prior period, unchanged from (\S+)\]$")

# Every number, at any scale or sign, becomes one placeholder.
_NUMBER = re.compile(r"\d[\d,.]*")

# docs/INPUT_SPEC.md §2 item 6. Matched on the note's tag name **and** on the
# paragraph's own words, because the topics are not only notes: Esterline's one
# contingencies paragraph in the whole input is in MD&A, and Apple's recent
# accounting pronouncements are in MD&A too. A rule that reads only tag names
# cannot see either.
#
# The name is read as words, not as a run of letters. `DebtSecuritiesAvailable
# ForSale…` contains "debt" and is an investments note; flattening the name to
# `usgaapdebtsecurities…` made that indistinguishable from a debt note, and
# pulled 410 of NVIDIA's 596 rescued paragraphs in with it.
ALWAYS_VERBATIM = {
    "contingencies_and_litigation": (
        r"\bcontingenc|\blitigation|\blegal matter|\bloss conting",
        r"\blitigation\b|\blegal proceeding|\bcontingenc|\bclaims?, charges"),
    "subsequent_events": (
        r"\bsubsequent event",
        r"\bsubsequent event"),
    "related_parties": (
        r"\brelated part",
        r"\brelated part(?:y|ies)\b"),
    "debt_and_covenants": (
        r"\bdebt\b(?! securities)|\bborrowing|\bcredit facilit|\bcredit agreement"
        r"|\bnotes payable|\bcovenant",
        r"\bcovenant|\bcredit facility\b|\bindenture\b|\bsenior notes due"),
    "accounting_changes_and_corrections": (
        r"\baccounting change|\berror correction|\bnew accounting pronouncement"
        r"|\brecently issued accounting|\bchange in accounting|\brestatement",
        # `ASU No. 2024-03` is how two of Apple's three pronouncement paragraphs
        # name the thing the third spells out, so the abbreviation is matched
        # where it carries a number and nowhere else.
        r"\baccounting standards update\b|\bASU (?:No\.|\d{4}-)"
        r"|\brecently issued accounting|\brecently adopted accounting"
        r"|\brestatement of\b"),
}
_ALWAYS_VERBATIM = {topic: (re.compile(name, re.IGNORECASE),
                            re.compile(body, re.IGNORECASE))
                    for topic, (name, body) in ALWAYS_VERBATIM.items()}

_CAMEL = re.compile(r"[A-Z]+(?![a-z])|[A-Z][a-z]*|[a-z]+|\d+")


def words_of(note_name: str) -> str:
    """`us-gaap:DebtDisclosureTextBlock` → `us gaap debt disclosure text block`."""
    return " ".join(_CAMEL.findall(note_name or "")).lower()


def always_verbatim(note_name: str, text: str = "") -> str | None:
    """Which always-verbatim topic this paragraph is, or None.

    The tag name decides first, because a note's own tag is what the input spec
    names. A paragraph in a section with no tag — MD&A — is read on its words.
    """
    name = words_of(note_name)
    for topic, (pattern, _) in _ALWAYS_VERBATIM.items():
        if pattern.search(name):
            return topic
    flat = html_text.normalized(text)
    for topic, (_, pattern) in _ALWAYS_VERBATIM.items():
        if pattern.search(flat):
            return topic
    return None


def mask(text: str) -> str:
    """The paragraph with its numbers taken out, for matching only."""
    return _NUMBER.sub("#", html_text.normalized(text))


def diff_stream(current: list[dict], prior: list[dict]) -> list[dict]:
    """One decision per current paragraph: carried verbatim, or collapsed.

    `current` and `prior` are lists of {id, text, note}. A paragraph collapses
    only when **its own text, unmasked, is a paragraph of the same note in the
    previous report** — one prior paragraph per current one, so a note that
    prints the same row twice this quarter and once last quarter collapses one
    and carries the other.

    Cycle 19 matched a *masked* paragraph against a **set** of every masked
    paragraph in the prior filing. A table cell `54,252` masks to `#`, and `#`
    was in that set the moment the prior filing contained any number at all:
    762 of Apple's collapsed note paragraphs held a digit and 541 of them
    occurred nowhere in the prior 10-Q. Apple's revenue note read `[same as
    prior period]` over a number that had moved. The mask is still here — it is
    what `src/note_history.py` pairs paragraphs with — but it decides nothing.
    """
    pool: dict[tuple[str, str], list[str]] = {}
    for entry in prior:
        pool.setdefault((entry["note"], entry["text"]), []).append(entry["id"])
    out = []
    for entry in current:
        topic = entry.get("verbatim_topic")
        counterparts = pool.get((entry["note"], entry["text"]))
        prior_id = counterparts.pop(0) if counterparts else None
        if prior_id is not None and topic is None:
            out.append({**entry, "kind": "collapsed", "prior_id": prior_id,
                        "line": SAME_AS_PRIOR.format(prior_id=prior_id)})
        else:
            out.append({**entry, "kind": "verbatim",
                        "reason": ("always verbatim: " + topic) if topic else
                                  ("unchanged but always verbatim" if prior_id else
                                   "new or changed")})
    return out


def notes(ticker: str, form: str, role: str, *, cutoff, fixtures_root) -> dict:
    """Every note once, as prose paragraphs and rendered tables.

    A filer tags a note, then each policy inside it, then each table inside
    that, and `extract_notes` takes all of them because a note that never
    reaches the file is a quote the predictor cannot make. The cost of taking
    all of them is that the same paragraph arrives three and four times over —
    71% to 77% of the raw stream. Two rules cut that without losing a
    paragraph:

    - a note whose whole text is already inside a note carried earlier is a
      copy of part of that note, and is skipped;
    - a paragraph or a table byte-identical to one already carried is skipped,
      and the id that does carry it is recorded.

    Neither rule can drop a text the file does not already hold. What each one
    dropped is in `repeats`, so the manifest can account for it.
    """
    payload = extract_notes.extract(ticker, form, role=role, cutoff=cutoff,
                                    fixtures_root=fixtures_root)
    out, repeats, dropped, carried, seen = [], [], [], [], {}
    for section in payload["sections"]:
        squeezed = re.sub(r"\s+", "", section["text"])
        if squeezed and any(squeezed in earlier for earlier in carried
                            if len(earlier) >= len(squeezed)):
            repeats.append({"source": section["name"], "kind": "note",
                            "already_carried": True})
            continue
        carried.append(squeezed)
        cleaned = clean_text.clean_stream(section["html"])
        for drop in cleaned["dropped"]:
            dropped.append({**drop, "source": section["name"]})
        for paragraph in cleaned["paragraphs"]:
            if paragraph in seen:
                repeats.append({"source": section["name"], "kind": "paragraph",
                                "text": paragraph, "already_at": seen[paragraph]})
                continue
            entry = {"id": f"{payload['accession']}:notes:{len(out) + 1}",
                     "text": paragraph, "note": section["name"],
                     "verbatim_topic": always_verbatim(section["name"], paragraph)}
            seen[paragraph] = entry["id"]
            out.append(entry)
    return {"paragraphs": out, "repeats": repeats, "dropped": dropped,
            "sections": len(payload["sections"]), "notes_carried": len(carried),
            "accession": payload["accession"]}


def _note_paragraphs(ticker: str, form: str, role: str, *, cutoff, fixtures_root) -> list[dict]:
    """The note stream's paragraphs alone, for callers that want only those."""
    return notes(ticker, form, role, cutoff=cutoff,
                 fixtures_root=fixtures_root)["paragraphs"]


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
    notes_before = (_note_paragraphs(ticker, "10-Q", "prior_period_xbrl_instance",
                                     cutoff=cutoff, fixtures_root=fixtures_root)
                    if has_prior else [])

    mdna_now = split_sections.extract(ticker, "10-Q", "mdna", cutoff=cutoff,
                                      fixtures_root=fixtures_root)
    mdna_kept = clean_text.clean_stream(blocks=mdna_now["blocks"])["paragraphs"]
    mdna_entries = [{"id": f"{current['accession']}:mdna:{index}", "text": text,
                     "note": "mdna", "verbatim_topic": always_verbatim("mdna", text)}
                    for index, text in enumerate(mdna_kept, start=1)]

    mdna_before = []
    if has_prior:
        prior_html = cutoff_guard.load_document(prior_rows[0]["full_path"], cutoff,
                                                fixtures_root=fixtures_root)
        prior_mdna = split_sections.split(prior_html, "10-Q", "mdna")
        mdna_before = [
            {"id": f"{prior_rows[0]['accession']}:mdna:{index}", "text": text,
             "note": "mdna"}
            for index, text in enumerate(
                clean_text.clean_stream(blocks=prior_mdna["blocks"])["paragraphs"],
                start=1)]

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
    """Exactly the placeholder, naming a paragraph id. Nothing else counts."""
    return _SAME_AS_PRIOR.match(line) is not None


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
