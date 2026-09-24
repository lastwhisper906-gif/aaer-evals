"""Detect filing: what the twelve have filed, read off the EDGAR submissions index.

`docs/HOW_WE_WORK.md` §3 gives the stage one line -- "daily: new filings for the
twelve, from the EDGAR submissions index" -- and one pass condition: "12 of 12
lookups succeed". Until this file the stage was run by hand through
`src/fetch_fixtures.py`'s `recent_filings`, which is what the second pipeline
check did on 2026-09-23. This is that, as a module.

**The companies come from `universe.json`**, through `src/universe.py`, read
when the stage runs. One lookup per row: the row's own CIK, one request to
`data.sec.gov/submissions/CIK##########.json`. The count of lookups is the count
of rows, so a thirteenth row is a thirteenth lookup and the pass condition reads
"13 of 13".

For every company that answered, the stage names the latest filing of each form
the pipeline triggers on or reads -- the 10-K, the 10-Q and the 8-K carrying item
2.02 -- as EDGAR's own row says it. A company that did not answer is a failed
lookup with its reason, never a company with no filings.

**New** means a filing of one of those three forms, filed on or after `since`,
for which no run directory exists under the run root yet. `since` is the day
the caller last looked, and it is required: nothing here remembers it, because
a state file says what some earlier run believed and the caller has the record
of what happened. A default such as "yesterday" would lose, without a line
saying so, every filing of a night that did not run.

Nothing is fetched beyond the index. Carrying a new filing through extract is
the caller's job.

    python3.12 -m src.detect_filing --since 2026-09-23 [--out detect.json]

Exit 0 when every lookup succeeded, 2 when any failed, 3 the wrong interpreter.
The JSON goes to `--out` when given and to standard output otherwise; one
summary line goes to standard error either way.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

try:
    from src import cutoff_guard, fetch_fixtures, interpreter_pin, universe
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import cutoff_guard, fetch_fixtures, interpreter_pin, universe

LOOKUP_FAILED = 2

# What the pipeline triggers on, then what it reads beside them. The 8-K is only
# the one that carries the earnings release.
TRIGGERING_FORMS = ("10-K", "10-Q")
EARNINGS_FORM, EARNINGS_ITEM = "8-K", "2.02"
# The kind's machine key: an 8-K carrying item 2.02 is the earnings release.
EARNINGS_RELEASE = "earnings_release"
KINDS = (*TRIGGERING_FORMS, EARNINGS_RELEASE)


def kind(filing: dict) -> str | None:
    """Which of the three a submissions row is, or None for anything else.

    An amendment is not the form it amends: `10-K/A` is its own form in the
    index and extract has no route for it, so it is not named here.
    """
    if filing["form"] in TRIGGERING_FORMS:
        return filing["form"]
    if filing["form"] == EARNINGS_FORM and EARNINGS_ITEM in (filing.get("items") or "").split(","):
        return EARNINGS_RELEASE
    return None


def row(filing: dict) -> dict:
    """The submissions row, in the names the fixture manifests use."""
    return {"accession": filing["accessionNumber"],
            "form": filing["form"],
            "filing_date": filing["filingDate"],
            "report_date": filing["reportDate"],
            "items": filing.get("items") or "",
            "primary_document": filing["primaryDocument"]}


def latest(filings: list[dict]) -> dict:
    """The latest filing of each kind, by filing date and then accession."""
    out: dict = {name: None for name in KINDS}
    for filing in filings:
        name = kind(filing)
        if name is None:
            continue
        key = (filing["filingDate"], filing["accessionNumber"])
        held = out[name]
        if held is None or key > (held["filing_date"], held["accession"]):
            out[name] = row(filing)
    return out


def new_filings(filings: list[dict], since: str, runs_on_record: set[str]) -> list[dict]:
    """Every filing of the three kinds filed on or after `since` with no run yet."""
    found = [dict(row(filing), kind=kind(filing)) for filing in filings
             if kind(filing) is not None and filing["filingDate"] >= since
             and filing["accessionNumber"] not in runs_on_record]
    found.sort(key=lambda entry: (entry["filing_date"], entry["accession"]))
    return found


def runs_on_record(runs_root: Path, ticker: str) -> set[str]:
    """The accessions that already have a run directory under the run root."""
    return {run.name for run in cutoff_guard.prior_runs(runs_root, ticker)}


def detect(fetcher, *, since: str, companies=None,
           runs_root: Path = Path("runs")) -> dict:
    """One lookup per universe row, and what each lookup found.

    `companies` is `universe.rows()` unless a caller read another universe
    file itself; this function reads no file of its own.
    """
    if companies is None:
        companies = universe.rows()
    results = []
    for company in companies:
        ticker, cik = company["ticker"], company["cik"]
        try:
            filings = fetch_fixtures.recent_filings(fetcher, cik)
        except Exception as exc:  # noqa: BLE001 - a failed lookup is recorded, whatever failed
            results.append({"ticker": ticker, "cik": cik, "lookup": "failed",
                            "reason": f"{type(exc).__name__}: {exc}",
                            "latest": None, "new": []})
            continue
        results.append({"ticker": ticker, "cik": cik, "lookup": "succeeded",
                        "reason": None, "latest": latest(filings),
                        "new": new_filings(filings, since,
                                           runs_on_record(runs_root, ticker))})
    succeeded = sum(1 for result in results if result["lookup"] == "succeeded")
    return {"since": since,
            "lookups": {"succeeded": succeeded, "of": len(companies)},
            "passed": succeeded == len(companies),
            "companies": results}


def summary_line(found: dict) -> str:
    lookups = found["lookups"]
    new = [f"{result['ticker']} {entry['kind']} {entry['accession']}"
           for result in found["companies"] for entry in result["new"]]
    failed = [f"{result['ticker']}: {result['reason']}"
              for result in found["companies"] if result["lookup"] == "failed"]
    line = (f"detect filing: {lookups['succeeded']} of {lookups['of']} lookups "
            f"succeeded, {len(new)} new since {found['since']}")
    if new:
        line += " (" + "; ".join(new) + ")"
    if failed:
        line += "; failed: " + "; ".join(failed)
    return line


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="new filings for the universe, "
                                                 "from the EDGAR submissions index")
    parser.add_argument("--since", required=True,
                        help="ISO date; a filing on or after it is new")
    parser.add_argument("--universe", default=None, help="the universe file")
    parser.add_argument("--runs", default="runs",
                        help="the run root; a filing with a run here is not new")
    parser.add_argument("--out", default=None, help="write the JSON here")
    args = parser.parse_args(argv)

    since = args.since
    try:
        dt.date.fromisoformat(since)
    except ValueError:
        print(f"detect_filing: --since {since!r} is not a YYYY-MM-DD date", file=sys.stderr)
        return LOOKUP_FAILED
    fetcher = fetch_fixtures.Fetcher(
        os.environ.get("EDGAR_USER_AGENT", fetch_fixtures.DEFAULT_USER_AGENT))
    try:
        companies = universe.rows(Path(args.universe) if args.universe else None)
        found = detect(fetcher, since=since, companies=companies,
                       runs_root=Path(args.runs))
    except universe.UniverseError as exc:
        print(f"detect_filing: {exc}", file=sys.stderr)
        return LOOKUP_FAILED
    text = json.dumps(found, indent=2) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    print(summary_line(found), file=sys.stderr)
    return 0 if found["passed"] else LOOKUP_FAILED


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
