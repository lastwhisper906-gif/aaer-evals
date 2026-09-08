"""What moved in the key notes between one period and the next.

The input spec asks for the added, removed and changed paragraphs of six notes
— revenue recognition policy, critical accounting estimates, contingencies,
debt, related parties, subsequent events — in date order, and **never several
periods of full text**. So this file is a change log and nothing else: an
unchanged paragraph does not appear here at all. The spec also says
contingencies, related parties and subsequent events *may* be carried whole
because they are short; they already are, by the always-verbatim list in
`src/diff_periods.py`, which is where carrying whole belongs. Doing it twice
would put several periods of full text in the file the spec says must not have
any.

**Matching notes across periods.** Companies renumber and retitle their notes,
so the tag name is tried first and a title similarity is the recorded fallback.
Every entry says which rule matched it and, for the fallback, the score — a
derived file whose match rule is not recorded cannot be reproduced by a reader
holding the same two filings, and reproducibility from the published inputs is
the claim this file has to support.

    python3.12 -m src.note_history --ticker AAPL --out input_notes_history.md
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path

try:
    from src import clean_text, cutoff_guard, diff_periods, extract_notes, html_text, interpreter_pin
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import clean_text, cutoff_guard, diff_periods, extract_notes, html_text, interpreter_pin

BAD_INPUT = 2

# docs/INPUT_SPEC.md §4 item 2, matched on the note's tag name.
KEY_NOTES = {
    "revenue_recognition_policy":
        r"revenuefromcontractwithcustomer|revenuerecognition|disaggregationofrevenue",
    "critical_accounting_estimates":
        r"useofestimates|significantaccountingpolicies|basisofpresentation"
        r"|businessdescriptionandaccountingpolicies|organizationconsolidation",
    "contingencies":
        r"contingenc|commitmentsandcontingencies|litigation|legalmatter",
    "debt": r"debtdisclosure|debt|borrowing|creditfacilit|notespayable|convertible",
    "related_parties": r"relatedparty|relatedpartie",
    "subsequent_events": r"subsequentevent",
}
_KEY_NOTES = {topic: re.compile(pattern, re.IGNORECASE)
              for topic, pattern in KEY_NOTES.items()}

TITLE_SIMILARITY_FLOOR = 0.70
CHANGED_SIMILARITY_FLOOR = 0.60

# The two labels for a note that has no counterpart at all. Calling either of
# them `tag_name` or `title_similarity` would put a match in the record where
# there was none; dropping them would lose the two changes a reader most wants
# to see — a note that appeared, and a note that went away. So they are entries
# and they say why they are unmatched: every paragraph of a new note is
# `added`, every paragraph of a vanished note is `removed`.
NO_PRIOR_NOTE = "no_prior_note"
NO_CURRENT_NOTE = "no_current_note"
MATCH_RULES = ("tag_name", "title_similarity", NO_PRIOR_NOTE, NO_CURRENT_NOTE)


def key_note(name: str) -> str | None:
    """Which of the six key notes this tag is, or None."""
    flat = re.sub(r"[^a-z]", "", (name or "").lower())
    for topic, pattern in _KEY_NOTES.items():
        if pattern.search(flat):
            return topic
    return None


def title_of(section: dict) -> str:
    """A note's own first line, which is the heading the filer wrote."""
    for start, end in html_text.lines(section.get("text", "")):
        return html_text.normalized(section["text"][start:end])
    return ""


def similarity(left: str, right: str) -> float:
    return round(difflib.SequenceMatcher(None, left, right).ratio(), 4)


def match_notes(current: list[dict], prior: list[dict]) -> list[dict]:
    """Pair this period's notes with last period's. Tag name first, title after."""
    remaining = list(prior)
    pairs = []
    by_name: dict[str, list[dict]] = {}
    for section in remaining:
        by_name.setdefault(section["name"], []).append(section)

    for section in current:
        candidates = by_name.get(section["name"], [])
        if candidates:
            match = candidates.pop(0)
            remaining.remove(match)
            pairs.append({"current": section, "prior": match,
                          "matched_by": "tag_name", "score": 1.0})
            continue
        title = title_of(section)
        best, best_score = None, 0.0
        for candidate in remaining:
            score = similarity(title, title_of(candidate)) if title else 0.0
            if score > best_score:
                best, best_score = candidate, score
        if best is not None and best_score >= TITLE_SIMILARITY_FLOOR:
            remaining.remove(best)
            pairs.append({"current": section, "prior": best,
                          "matched_by": "title_similarity", "score": best_score})
        else:
            pairs.append({"current": section, "prior": None,
                          "matched_by": NO_PRIOR_NOTE, "score": 0.0})

    for section in remaining:  # last period had it, this one does not
        pairs.append({"current": None, "prior": section,
                      "matched_by": NO_CURRENT_NOTE, "score": 0.0})
    return pairs


def _paragraphs(section: dict) -> list[str]:
    """The note as the bundle carries it — prose paragraphs and whole tables."""
    return clean_text.clean_stream(section["html"])["paragraphs"]


def compare(current: list[str], prior: list[str]) -> list[dict]:
    """Added, removed and changed. An unchanged paragraph is not an entry."""
    prior_masks = [diff_periods.mask(paragraph) for paragraph in prior]
    # One prior paragraph per current paragraph. A note's table has a hundred
    # cells that all mask to "#", and matching every one of them against the
    # *first* such cell would leave ninety-nine looking removed.
    available: dict[str, list[int]] = {}
    for index, masked in enumerate(prior_masks):
        available.setdefault(masked, []).append(index)

    unchanged_prior, entries, unmatched = set(), [], []
    for paragraph in current:
        masked = diff_periods.mask(paragraph)
        pool = available.get(masked)
        if pool:
            unchanged_prior.add(pool.pop(0))
            continue
        unmatched.append((paragraph, masked))

    spare = [index for index in range(len(prior)) if index not in unchanged_prior]
    for paragraph, masked in unmatched:
        best, best_score = None, 0.0
        for index in spare:
            score = similarity(masked, prior_masks[index])
            if score > best_score:
                best, best_score = index, score
        if best is not None and best_score >= CHANGED_SIMILARITY_FLOOR:
            spare.remove(best)
            entries.append({"kind": "changed", "text": paragraph,
                            "previous_text": prior[best], "score": best_score})
        else:
            entries.append({"kind": "added", "text": paragraph, "score": best_score})
    for index in spare:
        entries.append({"kind": "removed", "text": prior[index], "score": 0.0})
    return entries


def history(ticker: str, *, cutoff=None, fixtures_root=cutoff_guard.FIXTURES) -> dict:
    cutoff = cutoff or cutoff_guard.default_cutoff(ticker, fixtures_root=fixtures_root)
    now = extract_notes.extract(ticker, "10-Q", cutoff=cutoff, fixtures_root=fixtures_root)
    before = extract_notes.extract(ticker, "10-Q", role="prior_period_xbrl_instance",
                                   cutoff=cutoff, fixtures_root=fixtures_root)

    current_keys = [section for section in now["sections"] if key_note(section["name"])]
    prior_keys = [section for section in before["sections"] if key_note(section["name"])]

    entries = []
    pairs = match_notes(current_keys, prior_keys)
    for pair in pairs:
        section = pair["current"] or pair["prior"]
        current_paragraphs = _paragraphs(pair["current"]) if pair["current"] else []
        prior_paragraphs = _paragraphs(pair["prior"]) if pair["prior"] else []
        for entry in compare(current_paragraphs, prior_paragraphs):
            entries.append({
                "note": section["name"],
                "key_note": key_note(section["name"]),
                "matched_by": pair["matched_by"],
                "match_score": pair["score"],
                "period": now["filing_date"],
                "prior_period": before["filing_date"],
                "accession": now["accession"],
                "prior_accession": before["accession"],
                **entry,
            })
    entries.sort(key=lambda entry: (entry["period"], entry["key_note"], entry["note"]))
    # An id per entry, minted after the sort so it is the file's own order. The
    # bundle manifest lists these, and an entry with no id cannot be listed.
    #
    # **The id names the filing the text came from.** A `removed` entry's text
    # is the prior filing's, and a `changed` entry prints two paragraphs from
    # two filings, so it carries two ids. Minting all of them from the current
    # accession published prior-period text under a current-period id — AAPL 7
    # removed and 8 changed, CSCO 24 and 76, NVDA 123 and 22 — and a quote
    # checked against the filing that id names would not be found.
    for number, entry in enumerate(entries, start=1):
        source = before["accession"] if entry["kind"] == "removed" else now["accession"]
        entry["id"] = f"{source}:note_history:{number}"
        if entry["kind"] == "changed":
            entry["previous_id"] = f"{before['accession']}:note_history:{number}"
    counts = {kind: sum(1 for entry in entries if entry["kind"] == kind)
              for kind in ("added", "removed", "changed")}
    match_rules = {rule: sum(1 for pair in pairs if pair["matched_by"] == rule)
                   for rule in MATCH_RULES}
    return {
        "ticker": ticker,
        "cutoff": str(cutoff),
        "accession": now["accession"],
        "prior_accession": before["accession"],
        "key_notes": len(pairs),
        "entries": entries,
        "counts": counts,
        "match_rules": match_rules,
    }


def render(payload: dict) -> str:
    out = [f"# {payload['ticker']} note change history — "
           f"{payload['prior_accession']} → {payload['accession']}", ""]
    note = None
    for entry in payload["entries"]:
        if entry["note"] != note:
            note = entry["note"]
            out.extend(["", f"## {note} ({entry['key_note']}) — "
                            f"matched_by: {entry['matched_by']}, "
                            f"score: {entry['match_score']}", ""])
        out.append(f"- {entry['kind']} ({entry['period']}):")
        out.append(f"[{entry['id']}]")
        out.append(entry["text"])
        if entry["kind"] == "changed":
            out.append(f"  (was, {entry['prior_period']}, similarity {entry['score']}):")
            out.append(f"[{entry['previous_id']}]")
            out.append(entry["previous_text"])
        out.append("")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="added, removed and changed note paragraphs")
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--cutoff", default=None)
    parser.add_argument("--fixtures", default=str(cutoff_guard.FIXTURES))
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)

    try:
        payload = history(args.ticker.upper(), cutoff=args.cutoff,
                          fixtures_root=Path(args.fixtures))
    except cutoff_guard.CutoffGuardError as exc:
        print(f"note_history: {exc}", file=sys.stderr)
        return BAD_INPUT
    Path(args.out).write_text(render(payload), encoding="utf-8")
    print(f"note_history: {args.ticker.upper()} {payload['counts']} → {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
