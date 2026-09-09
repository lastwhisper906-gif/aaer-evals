"""A period that comes back at a different number than the filing that first reported it.

`docs/CHECKLIST.md` calls it `quiet_restatement`: a period reported in an earlier
filing comes back with a different value in a later one, with no amendment and no
correction note. `docs/INPUT_SPEC.md` says where the finding goes — into the
numbers reader's input beside the trend table, and into `events/ledger.jsonl`.

The source is the company's companyfacts document, which is the only record that
holds every filing's version of a period side by side, each row carrying the
accession and the filing date that reported it. Nothing here is fetched: the
document is the committed fixture, read through `src/cutoff_guard.py` like every
other document this project reads.

**Ground truth is the first-reported value.** `CLAUDE.md` says so, and the whole
finding rests on it: the earliest filing to report a period is what the period
was, and every later filing that disagrees is the trace. The comparison is
therefore always against that first value and never against the previous one, so
a figure that goes 100 → 90 → 100 reports one disagreement and not two — the
return to 100 agrees with what was first reported.

**One trace per distinct later value**, recorded at the filing that first carried
it. Four consecutive filings repeating a restated number are one restatement, and
the filing that introduced it is the one that restated.

**Nothing is filtered by size.** A one-dollar disagreement is reported exactly
like a billion-dollar one. There is no threshold here and adding one would be
inventing an answer this project has not decided.

**The difference is subtracted in decimal, not in binary.** companyfacts prints
a dividend per share as `0.38` and then as `0.37`; float subtraction of those
two reports `-0.010000000000000009`, and that is the number the numbers reader
would be handed as the finding. The digits the document printed are the ones
subtracted here, so the answer is `-0.01`. Two integers subtract to an integer
and stay one.

**An amendment is marked, not dropped.** A restatement announced in a 10-K/A is a
loud one, and calling it quiet would be a false statement; a trace whose later
filing is an amendment carries `amendment: true` and is counted separately. The
other half of the checklist's definition — no correction note — is prose, which
`CLAUDE.md` leaves to a reader and not to Python, so this module does not
pretend to decide it.

**A filing that reports one period at two values is not a restatement.** It is
the same fact at two roundings inside one document; companyfacts keeps the
precise one, and no such row survives in the twelve records committed here. If
one ever does, that filing is named under `ambiguous_within_one_filing` and left
out of the comparison rather than having one of its two values picked to
disagree with — but only that filing. The period's other filings are still
compared, because dropping the whole period would trade a real disagreement for
silence. The exception is a period whose *first* filing is the ambiguous one:
there is then no first-reported value to compare anything against, so the
period is named and nothing else is said about it.

**A filing companyfacts has not loaded is reported absent.** Two of the committed
accessions — Carrier's and Littelfuse's quarterlies filed in late July 2026 — are
in no companyfacts row, which is EDGAR's own loading lag. A period reported only
there cannot be looked up here, so the accessions are named in
`absent_from_companyfacts` and the numbers reader reads them out of the XBRL
instance instead. An absence is never a value, and never a zero. That list is
cut off like everything else: a filing later than the cutoff is not missing from
the run, it is outside it, and naming it would put a document the run may not
see into the run's own output.

**The cutoff.** companyfacts is a catalogue drawn from many filings, and its
manifest row is dated with the newest filing it carries a fact from. The gate
therefore refuses the whole document to a run whose cutoff is earlier than that
— the run is refused rather than quietly reading a record it cannot vouch for —
and the rows are filtered to `filed <= cutoff` on top of it.

The adverse half of that, said plainly: with the fixture set as it stands, two
of the twelve records are dated later than the company's own last committed
report — CSCO's 2026-08-20 against a 10-Q filed 2026-08-12, QCOM's 2026-07-31
against 2026-07-29 — so a run at the triggering report's own filing date is
refused for those two and the trace does not run for them at all. That is the
gate working, and it is a smaller answer than twelve.

    python3.12 -m src.restatement_trace --ticker CARR --out restatement_trace.json

The payload belongs with the trend table in `input_trends.json`, which is the
file `docs/INPUT_SPEC.md` names for what is derived from companyfacts; `--out` is
where this module leaves it and the assembler decides the rest.

Exit 0, 2 the gate refused the document or the company has no companyfacts row,
3 the wrong interpreter.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

try:
    from src import cutoff_guard, extract_numbers, interpreter_pin
except ImportError:  # invoked as a plain script: python3.12 src/restatement_trace.py
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import cutoff_guard, extract_numbers, interpreter_pin

EVENT = "quiet_restatement"
LEDGER = cutoff_guard.REPO_ROOT / "events" / "ledger.jsonl"

# The companyfacts document, as `src/fetch_companyfacts.py` records it in the
# manifest. The roles beside it are the documents that carry XBRL facts, taken
# from the module that reads them rather than listed again here: a third role
# would otherwise have to be remembered in two places.
COMPANYFACTS_FORM = "companyfacts"
COMPANYFACTS_ROLE = "standard_taxonomy_history"
INSTANCE_ROLES = extract_numbers.INSTANCE_ROLES

BAD_INPUT = 2


def is_amendment(form: str) -> bool:
    """`10-K/A`, `10-Q/A`. An amendment says out loud what a quiet one does not."""
    return str(form).endswith("/A")


def difference(restated, first_reported):
    """The later value minus the first-reported one, subtracted in decimal.

    `0.37 - 0.38` in binary floating point is `-0.010000000000000009`, and that
    is what the finding would carry. The values are subtracted as the digits the
    document printed them in instead. Two integers stay an integer.
    """
    if isinstance(restated, int) and isinstance(first_reported, int):
        return restated - first_reported
    return float(Decimal(str(restated)) - Decimal(str(first_reported)))


def by_period(facts: dict, cutoff: str) -> dict[tuple, list[dict]]:
    """Every fact row filed at or before the cutoff, gathered by the period it is about.

    The key is what makes two rows the same fact: namespace, tag, unit and the
    period itself. `filed` is read straight off the row: `fetch_companyfacts`
    refuses to record a document holding a row without one, so every row that
    reaches here has a filing date of its own.
    """
    grouped: dict[tuple, list[dict]] = defaultdict(list)
    for namespace, concepts in facts.items():
        for tag, concept in concepts.items():
            for unit, rows in concept.get("units", {}).items():
                for row in rows:
                    if row["filed"] <= cutoff:
                        grouped[(namespace, tag, unit,
                                 row.get("start"), row["end"])].append(row)
    return dict(grouped)


def _filings(rows: list[dict]) -> tuple[dict, dict]:
    """One period's rows, folded to what each filing said about it.

    Two maps keyed by accession: the distinct values that filing reported, and
    the filing itself — its date and its form.
    """
    values: dict[str, set] = defaultdict(set)
    filings: dict[str, dict] = {}
    for row in rows:
        values[row["accn"]].add(row["val"])
        filings.setdefault(row["accn"], {"filing_date": row["filed"],
                                         "form": row.get("form", "")})
    return values, filings


def traces(grouped: dict[tuple, list[dict]]) -> tuple[list[dict], list[dict]]:
    """The disagreements with the first-reported value, and the periods left out.

    Returns `(traces, ambiguous)`. Both are sorted, so two runs over one record
    write the same file.
    """
    found, ambiguous = [], []
    for key, rows in grouped.items():
        namespace, tag, unit, start, end = key
        values, filings = _filings(rows)

        at_two_values = {accession for accession in values
                         if len(values[accession]) > 1}
        if at_two_values:
            named = sorted(at_two_values)
            ambiguous.append({
                "namespace": namespace, "tag": tag, "unit": unit,
                "period": {"start": start, "end": end},
                "accessions": named,
                "values": {accession: sorted(values[accession])
                           for accession in named},
            })

        order = sorted(values, key=lambda accession: (filings[accession]["filing_date"],
                                                      accession))
        first = order[0]
        if first in at_two_values:
            # The filing that reported the period first reported it at two
            # numbers, so there is no first-reported value to compare against.
            continue
        first_value = next(iter(values[first]))
        frame = next((row["frame"] for row in rows if row.get("frame")), None)

        reported = {first_value}
        for accession in order[1:]:
            if accession in at_two_values:
                continue
            value = next(iter(values[accession]))
            if value in reported:
                continue
            reported.add(value)
            found.append({
                "namespace": namespace,
                "tag": tag,
                "unit": unit,
                "period": {"start": start, "end": end},
                "frame": frame,
                "first_reported": {"value": first_value, "accession": first,
                                   **filings[first]},
                "restated": {"value": value, "accession": accession,
                             **filings[accession]},
                "difference": difference(value, first_value),
                "amendment": is_amendment(filings[accession]["form"]),
            })

    found.sort(key=lambda trace: (trace["restated"]["filing_date"], trace["namespace"],
                                  trace["tag"], trace["unit"],
                                  trace["period"]["start"] or "", trace["period"]["end"]))
    ambiguous.sort(key=lambda row: (row["namespace"], row["tag"], row["unit"],
                                    row["period"]["start"] or "", row["period"]["end"]))
    return found, ambiguous


def absent_from_companyfacts(ticker: str, reported: set, cutoff: dt.date, *,
                             fixtures_root) -> list[dict]:
    """Filings at or before the cutoff that are in no companyfacts row at all.

    EDGAR loads companyfacts from filings on its own schedule, and two of the
    accessions committed here were filed too recently to be in it. A period whose
    only source is one of those cannot be looked up in this record, so it is
    named rather than counted as agreeing — and never as a zero.

    A filing later than the cutoff is not absent from the run; it is outside it,
    and naming it would put a document the run may not see into the run's own
    output. A filing with no recorded date cannot be shown to be inside the
    cutoff, so it is refused rather than assumed early.
    """
    missing = []
    for role in INSTANCE_ROLES:
        for row in cutoff_guard.documents(ticker, role=role, fixtures_root=fixtures_root):
            if not row["accession"] or row["accession"] in reported:
                continue
            filed = cutoff_guard.parse_date(
                row.get("filing_date"), f"{ticker} {row.get('path')} filing_date")
            if filed <= cutoff:
                missing.append({"form": row["form"], "role": role,
                                "accession": row["accession"],
                                "filing_date": row["filing_date"]})
    missing.sort(key=lambda row: (row["filing_date"], row["accession"], row["role"]))
    return missing


def scan(ticker: str, *, cutoff=None, fixtures_root=cutoff_guard.FIXTURES) -> dict:
    """One company's companyfacts, read through the gate, scanned for traces."""
    fixtures_root = Path(fixtures_root)
    cutoff = cutoff_guard.parse_date(
        cutoff or cutoff_guard.default_cutoff(ticker, fixtures_root=fixtures_root),
        "cutoff")
    record = cutoff_guard.one_document(ticker, COMPANYFACTS_FORM, COMPANYFACTS_ROLE,
                                       fixtures_root=fixtures_root)
    document = json.loads(cutoff_guard.load_bytes(record["full_path"], cutoff,
                                                  fixtures_root=fixtures_root))

    grouped = by_period(document["facts"], str(cutoff))
    found, ambiguous = traces(grouped)
    reported_by = {row["accn"] for rows in grouped.values() for row in rows}
    return {
        "ticker": ticker,
        "cutoff": str(cutoff),
        "record": {"path": record["path"], "filing_date": record["filing_date"],
                   "sha256": record["sha256"], "url": record["url"]},
        "counts": {
            "periods": len(grouped),
            "periods_reported_more_than_once":
                sum(1 for rows in grouped.values()
                    if len({row["accn"] for row in rows}) > 1),
            "traces": len(found),
            "amendments": sum(1 for trace in found if trace["amendment"]),
        },
        "traces": found,
        "absent_from_companyfacts": absent_from_companyfacts(
            ticker, reported_by, cutoff, fixtures_root=fixtures_root),
        "ambiguous_within_one_filing": ambiguous,
    }


def ledger_line(payload: dict, *, recorded_utc: str | None = None) -> dict:
    """The one event line a run appends, whether or not it found anything.

    A scan that found nothing is a thing the record should be able to say, so
    that the event-gap routine can tell "no restatement" from "never looked".
    """
    counts = payload["counts"]
    return {
        "event": EVENT,
        "ticker": payload["ticker"],
        "cutoff": payload["cutoff"],
        "source": "companyfacts",
        "record_sha256": payload["record"]["sha256"],
        "periods_reported_more_than_once": counts["periods_reported_more_than_once"],
        "traces": counts["traces"],
        "amendments": counts["amendments"],
        "absent_from_companyfacts": len(payload["absent_from_companyfacts"]),
        "recorded_utc": recorded_utc or dt.datetime.now(dt.timezone.utc)
                                          .strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def append_line(line: dict, path) -> Path:
    """Append one line to a ledger. The only write this module makes to `events/`."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as ledger:
        ledger.write(json.dumps(line) + "\n")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="periods that came back at a different value than first reported")
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--cutoff", default=None,
                        help="ISO date; default is the fixture set's as-of date")
    parser.add_argument("--fixtures", default=str(cutoff_guard.FIXTURES))
    parser.add_argument("--out", required=True,
                        help="where the trace goes; it belongs in input_trends.json")
    parser.add_argument("--ledger", default=str(LEDGER),
                        help="the event ledger this run appends its one line to")
    args = parser.parse_args(argv)

    try:
        payload = scan(args.ticker.upper(), cutoff=args.cutoff,
                       fixtures_root=Path(args.fixtures))
    except cutoff_guard.CutoffGuardError as exc:
        print(f"restatement_trace: {exc}", file=sys.stderr)
        return BAD_INPUT

    Path(args.out).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    written = append_line(ledger_line(payload), args.ledger)
    counts = payload["counts"]
    print(f"restatement_trace: {payload['ticker']} {counts['traces']} traces "
          f"({counts['amendments']} in an amendment) over "
          f"{counts['periods_reported_more_than_once']} periods reported more than "
          f"once → {args.out}, one line → {written}")
    return 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
