"""The nightly crew's night: detect, extract each new filing, check it, one summary line.

The owner's decision of 2026-09-24 (`docs/structure_changes.md`): the night work
is Python with no model. This is that night, run by `.github/workflows/nightly.yml`
on GitHub Actions, because the cloud session that writes the morning report may
not reach sec.gov and every EDGAR request happens here.

1. **Detect filing** -- `src/detect_filing.py`, one lookup per `universe.json`
   row. A filing is new when it was filed on or after `since` and has no run
   directory under `runs/` yet. `since` is the date of the last night whose
   lookups all succeeded, read out of the summary ledger, so a night that did
   not run is covered by the next one rather than skipped.
2. **Extract** each new 10-K and 10-Q: a store fetched up to it
   (`src/fetch_fixtures.py --accession`, `src/fetch_companyfacts.py --as-of` its
   filing date), then `src/assemble_bundle.py --accession`, which builds that
   filing or refuses. A new 8-K carrying item 2.02 is named and not extracted:
   extract builds bundles for the two triggering reports only.
3. **The four extraction checks** -- `src/extraction_checks.py` on the bundle,
   with the drift baseline read from the committed fixtures' `expected.json`.
   The assembler writes the bundle to `runs/{ticker}/{accession}/`, and a
   bundle that fails a check is removed again before anything is committed:
   `runs/` is append-only and a failed extraction is not a record of the
   filing. Its failure lines go in the summary, and the next night tries it
   again: every 10-K or 10-Q a summary line records as failed, and that still
   has no run directory, is extracted again whether or not it is new, until it
   passes.
4. **One summary line**, appended to `history/nightly.jsonl`: lookups, new
   filings, each extraction's result, and every failure with its reason. The
   morning report reads it, failures first.

Read, compare and decide are not run: the price source is unresolved, and the
target of this stage (`docs/HOW_WE_WORK.md` §7 step 5) is extraction.

    python3.12 -m src.nightly --work /tmp/nightly [--ticker CIEN --accession ...]

Exit 0 when nothing failed, 1 when the summary records a failure, 2 when the
summary could not be written, 3 the wrong interpreter.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

try:
    from src import detect_filing, fetch_fixtures, interpreter_pin, universe
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import detect_filing, fetch_fixtures, interpreter_pin, universe

REPO_ROOT = Path(__file__).resolve().parent.parent
SUMMARY = Path("history") / "nightly.jsonl"
FIXTURES = REPO_ROOT / "tests" / "fixtures"

FAILED = 1
NOT_WRITTEN = 2

# How much of a failing step's standard error the summary keeps: the last lines
# are where every entry point here prints its reason.
REASON_LINES = 6


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def since_from(summary: Path, today: dt.date) -> str:
    """The date of the last night whose lookups all succeeded, else yesterday."""
    last = None
    if summary.is_file():
        for line in summary.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            night = json.loads(line)
            if night.get("lookups", {}).get("passed"):
                last = night["date"]
    return last or (today - dt.timedelta(days=1)).isoformat()


def to_retry(summary: Path) -> list[dict]:
    """Every 10-K or 10-Q a past night failed to extract, oldest first, once each.

    `since` moves forward with every night whose lookups passed, so a filing
    whose extraction failed on its first night is not new on the next one; this
    is what brings it back. Whether it has a run by now is the caller's check.
    """
    found: dict[str, dict] = {}
    if summary.is_file():
        for text in summary.read_text(encoding="utf-8").splitlines():
            if not text.strip():
                continue
            for record in json.loads(text).get("extractions", []):
                if (record.get("result") == "failed"
                        and record.get("form") in detect_filing.TRIGGERING_FORMS
                        and record.get("filing_date")):
                    found.setdefault(record["accession"], {
                        "ticker": record["ticker"], "form": record["form"],
                        "accession": record["accession"],
                        "filing_date": record["filing_date"]})
    return sorted(found.values(), key=lambda entry: (entry["filing_date"], entry["accession"]))


def step(name: str, argv: list[str]) -> dict:
    """Run one entry point of this repository; its exit status and its reason."""
    done = subprocess.run([sys.executable, "-m", *argv], cwd=REPO_ROOT,
                          capture_output=True, text=True)
    tail = [line for line in (done.stderr or "").splitlines() if line.strip()]
    return {"step": name, "exit": done.returncode,
            "reason": " | ".join(tail[-REASON_LINES:]) if done.returncode else None,
            "stdout": done.stdout}


def remove(bundle: Path) -> None:
    """Take a failed bundle out of the run root, and its company folder if empty."""
    if bundle.exists():
        shutil.rmtree(bundle)
    if bundle.parent.is_dir() and not any(bundle.parent.iterdir()):
        bundle.parent.rmdir()


def extract(filing: dict, *, work: Path, runs_root: Path, fixtures: Path) -> dict:
    """One new filing through the store, the assembler and the four checks."""
    ticker, accession, form = filing["ticker"], filing["accession"], filing["form"]
    record = {"ticker": ticker, "form": form, "accession": accession,
              "filing_date": filing.get("filing_date"), "result": "failed",
              "stage": None, "reason": None, "checks": []}
    store = work / "store" / f"{ticker}-{accession}"
    bundle = runs_root / ticker / accession
    if bundle.exists():
        record.update(stage="extract", reason=f"{bundle} already exists, and runs/ "
                      "is append-only")
        return record
    steps = [
        ("fetch filings", ["src.fetch_fixtures", "--ticker", ticker,
                           "--accession", accession, "--out", str(store)]),
        ("fetch companyfacts", ["src.fetch_companyfacts", "--ticker", ticker,
                                "--as-of", str(filing.get("filing_date")),
                                "--out", str(store)]),
        ("extract", ["src.assemble_bundle", "--ticker", ticker, "--form", form,
                     "--accession", accession, "--fixtures", str(store),
                     "--prior-runs", str(runs_root), "--out", str(bundle)]),
    ]
    for name, argv in steps:
        ran = step(name, argv)
        if ran["exit"]:
            record.update(stage=name, reason=ran["reason"] or f"exit {ran['exit']}")
            # The assembler writes all of its files or none, but it creates
            # the directory first; a refusal leaves nothing to commit.
            remove(bundle)
            return record
    checked = subprocess.run(
        [sys.executable, "-m", "src.extraction_checks", str(bundle),
         "--fixtures", str(fixtures)],
        cwd=REPO_ROOT, capture_output=True, text=True)
    record["checks"] = [line for line in
                        (checked.stdout + checked.stderr).splitlines() if line.strip()]
    if checked.returncode:
        failing = [line for line in record["checks"] if ": FAIL" in line]
        record.update(stage="extraction checks",
                      reason=" | ".join(failing) or f"exit {checked.returncode}")
        remove(bundle)
        return record
    record.update(result="passed", stage=None, reason=None)
    return record


def forced(ticker: str, accession: str, fetcher, ciks: dict) -> dict:
    """A filing named by hand, looked up in the index like any other.

    `ciks` is the universe the night's detect read, by ticker.
    """
    try:
        if ticker.upper() not in ciks:
            raise universe.UniverseError(f"{ticker.upper()} is not in the universe")
        row = fetch_fixtures.filing_for(
            fetch_fixtures.recent_filings(fetcher, ciks[ticker.upper()]), accession)
    except (fetch_fixtures.NotInIndex, universe.UniverseError) as exc:
        return {"ticker": ticker.upper(), "accession": accession, "form": None,
                "filing_date": None, "error": str(exc)}
    except Exception as exc:  # noqa: BLE001
        return {"ticker": ticker.upper(), "accession": accession, "form": None,
                "filing_date": None, "error": f"{type(exc).__name__}: {exc}"}
    return {"ticker": ticker.upper(), "accession": accession, "form": row["form"],
            "filing_date": row["filingDate"], "error": None}


def label(kind: str) -> str:
    """A kind as a reader of the morning report names it."""
    return "8-K item 2.02" if kind == detect_filing.EARNINGS_RELEASE else kind


def night(*, fetcher, since: str, runs_root: Path, work: Path, fixtures: Path,
          companies=None, hand: tuple[str, str] | None = None,
          run_url: str | None = None, today: dt.date | None = None,
          retry: list[dict] | None = None) -> dict:
    today = today or dt.datetime.now(dt.timezone.utc).date()
    started = now()
    failures: list[str] = []
    found = detect_filing.detect(fetcher, since=since, companies=companies,
                                 runs_root=runs_root)
    for company in found["companies"]:
        if company["lookup"] == "failed":
            failures.append(f"detect filing: {company['ticker']} lookup failed: "
                            f"{company['reason']}")

    new = [dict(entry, ticker=company["ticker"])
           for company in found["companies"] for entry in company["new"]]
    to_extract = [entry for entry in new if entry["kind"] in detect_filing.TRIGGERING_FORMS]
    not_extracted = [entry for entry in new if entry["kind"] not in detect_filing.TRIGGERING_FORMS]

    extractions = []
    if hand is not None:
        named = forced(hand[0], hand[1], fetcher,
                       {company["ticker"]: company["cik"] for company in found["companies"]})
        if named["error"]:
            extractions.append({"ticker": named["ticker"], "form": None,
                                "accession": named["accession"], "filing_date": None,
                                "result": "failed", "stage": "detect filing",
                                "reason": named["error"], "checks": [],
                                "named_by_hand": True})
        elif named["form"] not in detect_filing.TRIGGERING_FORMS:
            extractions.append({"ticker": named["ticker"], "form": named["form"],
                                "accession": named["accession"],
                                "filing_date": named["filing_date"],
                                "result": "failed", "stage": "extract",
                                "reason": f"{named['form']} is not a triggering report; "
                                          "extract builds 10-K and 10-Q bundles only",
                                "checks": [], "named_by_hand": True})
        elif not any(entry["accession"] == named["accession"] for entry in to_extract):
            to_extract.append({"ticker": named["ticker"], "form": named["form"],
                               "accession": named["accession"],
                               "filing_date": named["filing_date"],
                               "named_by_hand": True})
    for entry in retry or []:
        if (not (runs_root / entry["ticker"] / entry["accession"]).exists()
                and not any(held["accession"] == entry["accession"] for held in to_extract)):
            to_extract.append(dict(entry, retried=True))
    for entry in to_extract:
        record = extract(entry, work=work, runs_root=runs_root, fixtures=fixtures)
        if entry.get("retried"):
            record["retried"] = True
        if entry.get("named_by_hand"):
            record["named_by_hand"] = True
        extractions.append(record)
    for record in extractions:
        if record["result"] != "passed":
            filing = " ".join(part for part in (record["ticker"], record["form"],
                                                record["accession"]) if part)
            failures.append(f"{record['stage']}: {filing}: {record['reason']}")

    return {
        "date": today.isoformat(),
        "started_utc": started,
        "finished_utc": now(),
        "run": run_url,
        "since": since,
        "lookups": {"succeeded": found["lookups"]["succeeded"],
                    "of": found["lookups"]["of"], "passed": found["passed"]},
        "new": [f"{entry['ticker']} {label(entry['kind'])} {entry['accession']} filed "
                f"{entry['filing_date']}" for entry in new],
        "not_extracted": [f"{entry['ticker']} {label(entry['kind'])} {entry['accession']}: "
                          "extract builds 10-K and 10-Q bundles only"
                          for entry in not_extracted],
        "extractions": extractions,
        "failures": failures,
    }


def crashed(today: dt.date, since: str, run_url: str | None, exc: Exception) -> dict:
    """The line a night that raised leaves: no lookups passed, and why."""
    return {"date": today.isoformat(), "finished_utc": now(), "run": run_url,
            "since": since, "lookups": {"succeeded": 0, "of": None, "passed": False},
            "new": [], "not_extracted": [], "extractions": [],
            "failures": [f"the night crashed: {type(exc).__name__}: {exc}"]}


def append(summary: Path, line: dict) -> None:
    summary.parent.mkdir(parents=True, exist_ok=True)
    with summary.open("a", encoding="utf-8") as out:
        out.write(json.dumps(line, sort_keys=True) + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="one night of the nightly crew")
    parser.add_argument("--summary", default=str(SUMMARY))
    parser.add_argument("--runs", default="runs")
    parser.add_argument("--work", required=True, help="scratch directory for stores")
    parser.add_argument("--fixtures", default=str(FIXTURES),
                        help="where expected.json, the drift baseline, lives")
    parser.add_argument("--since", default=None)
    parser.add_argument("--ticker", default=None, help="with --accession: extract "
                                                       "this filing whether or not it is new")
    parser.add_argument("--accession", default=None)
    parser.add_argument("--run-url", default=None)
    args = parser.parse_args(argv)

    summary = Path(args.summary)
    # A filing named by hand needs both halves. With one missing the night
    # still runs and says why nothing was named, rather than leaving no line.
    hand, refused = None, []
    if args.ticker and args.accession:
        hand = (args.ticker.strip().upper(), args.accession.strip())
    elif args.ticker or args.accession:
        refused.append("workflow input: a ticker and an accession go together, and "
                       f"only one was given (ticker {args.ticker!r}, accession "
                       f"{args.accession!r}); no filing was extracted by hand")
    today = dt.datetime.now(dt.timezone.utc).date()
    since = args.since
    fetcher = fetch_fixtures.Fetcher(
        os.environ.get("EDGAR_USER_AGENT", fetch_fixtures.DEFAULT_USER_AGENT))
    try:
        # Inside the try: an unreadable summary line is the night's failure
        # line, not a night that leaves none.
        since = since or since_from(summary, today)
        line = night(fetcher=fetcher, since=since, runs_root=Path(args.runs),
                     work=Path(args.work), fixtures=Path(args.fixtures), hand=hand,
                     run_url=args.run_url, today=today, retry=to_retry(summary))
    except Exception as exc:  # noqa: BLE001 - a night that crashed still leaves a line
        line = crashed(today, since, args.run_url, exc)
    line["failures"] = refused + line["failures"]
    try:
        append(summary, line)
    except OSError as exc:
        print(f"nightly: the summary could not be written: {exc}", file=sys.stderr)
        return NOT_WRITTEN
    print(json.dumps(line, indent=2))
    return FAILED if line["failures"] else 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
