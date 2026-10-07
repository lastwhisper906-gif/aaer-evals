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
2. **Extract** each new 10-K and 10-Q, **newest filing first**: a store fetched
   up to it (`src/fetch_fixtures.py --accession`, `src/fetch_companyfacts.py
   --as-of` its filing date), then `src/assemble_bundle.py --accession`, which
   builds that filing or refuses. A new 8-K carrying item 2.02 is named and not
   extracted: extract builds bundles for the two triggering reports only. The
   order is the filing dates', latest first and the later accession first on
   one date, whatever order the index lists them in; a filing retried from an
   earlier night takes its place by its own date.
3. **The four extraction checks** -- `src/extraction_checks.py` on the bundle,
   with the drift baseline read from the committed fixtures' `expected.json`.
   The assembler writes the bundle to `runs/{ticker}/{accession}/`, and a
   bundle that fails a check is removed again before anything is committed:
   `runs/` is append-only and a failed extraction is not a record of the
   filing. Its failure lines go in the summary, and the next night tries it
   again: every 10-K or 10-Q a summary line records as failed, and that still
   has no run directory, is extracted again whether or not it is new, until it
   passes.
4. **The price folder**, for each bundle that passed: `src/market.fetch_prices`
   writes, from Tiingo, the three daily series `market.market_table` measures
   the company against -- its own, the broad market's and its sector's, the
   last two read off the rules' SIC map -- for the 400 days before the filing
   date through the filing date, which is as far as a night can see (reaction
   days one and two have not traded yet), into
   `runs/{ticker}/{accession}/prices/`, and its record of the fetch into
   `price_fetch.json` beside it -- which backend, when, how many rows. Both sit
   outside the run's `agents/`, where a raw series would be a document past
   reaction day two in front of a reader. The credential is the `TIINGO_TOKEN`
   the workflow hands this process; it is read out of the environment, never
   written, and a night without it records `no price series: TIINGO_TOKEN
   unset` for the run and goes on. A fetch that fails is recorded by its reason
   and does not undo the extraction.
5. **Historical collection**, `src/collect_history.py`: the next batch of the
   twelve's past filings, oldest first, each hashed and, for a 10-K or 10-Q,
   carried through the same extract and the same four checks. Its failures are
   the checks' results on old filings and are counted in the summary's
   `history`, not listed as the night's failures; a company whose index could
   not be listed is a failure of the night.
6. **One summary line**, appended to `history/nightly.jsonl`: lookups, new
   filings, each extraction's result and its price folder, historical progress,
   and every failure with its reason. The morning report reads it, failures
   first.
7. **Publish**, with `--publish`: the night's run directories and the ledger
   line are committed on a branch `nightly-<date>` (`nightly-<date>-2` for a
   second run on a date whose branch is still on the remote), pushed, and a
   pull request into `main` is opened with auto-merge on (`gh pr create`, then
   `gh pr merge --auto --merge`, the repository's merge method). Nothing is
   ever pushed to `main` from here; `main` takes the line when CI is green. A
   night with nothing to commit opens no pull request and says so.

Read, compare and decide are not run: the target of this stage
(`docs/HOW_WE_WORK.md` §7 step 5) is extraction.

    python3.12 -m src.nightly --work /tmp/nightly [--ticker CIEN --accession ...] [--publish]

Exit 0 when nothing failed, 1 when the summary records a failure or the
publish step did not open its pull request, 2 when the summary could not be
written, 3 the wrong interpreter.
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
    from src import (collect_history, detect_filing, fetch_fixtures, interpreter_pin,
                     market, universe)
    from src.prices import tiingo
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import (collect_history, detect_filing, fetch_fixtures, interpreter_pin,
                     market, universe)
    from src.prices import tiingo

REPO_ROOT = Path(__file__).resolve().parent.parent
SUMMARY = Path("history") / "nightly.jsonl"
FIXTURES = REPO_ROOT / "tests" / "fixtures"

FAILED = 1
NOT_WRITTEN = 2

# How much of a failing step's standard error the summary keeps: the last lines
# are where every entry point here prints its reason.
REASON_LINES = 6

# The price folder: the window before the filing date, the folder and the record
# inside the run, and the source and the variable its credential is read from.
# The symbols are not here: they are the ones `market.market_table` measures
# against, read off the rules' map. The window is 400 calendar days because the
# beta is estimated over the 250 trading days before the filing date
# (`market.BETA_TRADING_DAYS`), a little under a calendar year, and each of
# those days' returns needs the close before it. The reason a night without the
# credential records is a fixed string, so the morning report and the tests can
# look for it by name.
PRICE_DAYS_BEFORE_FILING = 400
PRICE_FOLDER = "prices"
PRICE_RECORD = market.FETCH_RECORD
PRICE_SOURCE = tiingo.NAME
TOKEN_VARIABLE = tiingo.TOKEN_VARIABLE
NO_PRICES_UNSET = f"no price series: {TOKEN_VARIABLE} unset"
TOKEN_STAND_IN = f"<{TOKEN_VARIABLE}>"

# What the publish step commits: the two trees the night writes under.
PUBLISHED = ("history", "runs")


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


def newest_first(filings: list[dict]) -> list[dict]:
    """The filings to extract, the latest filing date first, then the later accession.

    Two filings of one day are ordered by accession, the later one first, so the
    order is a function of the rows and not of the index's own order.
    """
    return sorted(filings, key=lambda entry: (entry["filing_date"] or "", entry["accession"]),
                  reverse=True)


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


def without_token(text: str, token: str) -> str:
    """The text with the credential, wherever it appears, replaced by its name.

    A source's refusal can echo the request that carried the token; what is
    written into the ledger is the refusal with the token's name in its place.
    """
    return text.replace(token, TOKEN_STAND_IN) if token else text


def price_window(filing_date: str) -> tuple[dt.date, dt.date]:
    """The 400 days before the filing date, through the filing date."""
    end = dt.date.fromisoformat(filing_date)
    return end - dt.timedelta(days=PRICE_DAYS_BEFORE_FILING), end


def price_series(ticker: str, sic) -> dict:
    """The series `market.market_table` measures one company against, or why none.

    The company's own, the broad market's and its sector's, the last two read
    off the rules' map (`src/sic_to_sector_etf_map_<version>.json`) and not
    named here: the map moves with the rules. A sector series that is the broad
    market's (the map's nonclassifiable division) is asked for once. A SIC code
    the map cannot place is the reason, recorded on the run, not raised through
    the night.
    """
    try:
        symbols = [ticker, market.broad_market_symbol(), market.sector_symbol(sic)]
    except Exception as exc:  # noqa: BLE001 - the extraction stands; the prices say why not
        return {"symbols": None, "reason": f"{type(exc).__name__}: {exc}"}
    return {"symbols": list(dict.fromkeys(symbols)), "reason": None}


def prices_for(filing: dict, *, series: dict, bundle: Path, environ, fetch=None) -> dict:
    """The run's price folder and the record of its fetch, or the reason there is none.

    `series` is `price_series` for the filing's company. `environ` is the
    mapping the credential is read from, and the only one: the night hands in
    `os.environ`, a test hands in a mapping of its own. The token itself is
    never part of what this returns or writes. `fetch` is `market.fetch_prices`
    unless a test stands one in, and the source is the one whose token this
    reads, whatever `PRICE_BACKEND` the mapping names.
    """
    fetch = fetch if fetch is not None else market.fetch_prices
    out = {"folder": None, "record": None, "reason": None}
    record_path = bundle / PRICE_RECORD
    token = (environ.get(TOKEN_VARIABLE) or "").strip()
    if not token:
        out["reason"] = NO_PRICES_UNSET
        market.write_fetch_record({"fetched": False, "reason": NO_PRICES_UNSET}, record_path)
        return out
    if series["reason"]:
        out["reason"] = without_token(series["reason"], token)
        market.write_fetch_record({"fetched": False, "reason": out["reason"]}, record_path)
        return out
    folder = bundle / PRICE_FOLDER
    try:
        start, end = price_window(filing["filing_date"])
        record = fetch(symbols=series["symbols"], start=start, end=end,
                       into=folder, environ=environ, backend=PRICE_SOURCE)
    except Exception as exc:  # noqa: BLE001 - the extraction stands; the prices say why not
        out["reason"] = without_token(f"{type(exc).__name__}: {exc}", token)
        market.write_fetch_record({"fetched": False, "reason": out["reason"]}, record_path)
        return out
    market.write_fetch_record(record, record_path)
    out.update(folder=str(folder), record=str(record_path))
    return out


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
          retry: list[dict] | None = None, environ=None, fetch_prices=None) -> dict:
    """One night's detect, extract, check and price folder, as the summary line.

    `environ` is the mapping the price credential is read from; a caller that
    hands none in hands in an empty one, which is a night with no token, never
    the process's own environment by default.
    """
    today = today or dt.datetime.now(dt.timezone.utc).date()
    environ = environ if environ is not None else {}
    companies = companies if companies is not None else universe.rows()
    # Each company's SIC code names the sector series its price folder holds.
    sics = {company["ticker"]: company.get("sic") for company in companies}
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
    for entry in newest_first(to_extract):
        record = extract(entry, work=work, runs_root=runs_root, fixtures=fixtures)
        if entry.get("retried"):
            record["retried"] = True
        if entry.get("named_by_hand"):
            record["named_by_hand"] = True
        if record["result"] == "passed":
            record["prices"] = prices_for(
                entry, series=price_series(entry["ticker"], sics.get(entry["ticker"])),
                bundle=runs_root / entry["ticker"] / entry["accession"],
                environ=environ, fetch=fetch_prices)
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
        "history": None,
        "failures": failures,
    }


def with_history(line: dict, fetcher, *, history_root: Path, work: Path, batch: int,
                 companies=None) -> dict:
    """The night's line, with tonight's batch of past filings collected into it.

    A past filing failing its checks is data and is counted under `history`; a
    company whose index could not be listed is a failure of the night, and so is
    the collection raising, which leaves the rest of the night's line as it was.
    """
    if not batch:
        return line
    try:
        history = collect_history.collect(
            fetcher, companies=companies if companies is not None else universe.rows(),
            history_root=history_root, work=work, batch=batch)
    except Exception as exc:  # noqa: BLE001 - the night's own results stand
        return dict(line, failures=line["failures"] + [
            f"historical collection crashed: {type(exc).__name__}: {exc}"],
            finished_utc=now())
    failures = line["failures"] + [f"historical collection: {entry}"
                                   for entry in history["listing_failures"]]
    return dict(line, history=history, failures=failures, finished_utc=now())


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


def run_command(argv: list[str]) -> subprocess.CompletedProcess:
    """One git or gh command at the repository root; the publish step's runner."""
    return subprocess.run(argv, cwd=REPO_ROOT, capture_output=True, text=True)


def publish(*, date: str, run_url: str | None, root: Path = REPO_ROOT,
            runner=None) -> dict:
    """Commit the night's lines on `nightly-<date>`, open the pull request, auto-merge on.

    Every command goes through `runner`, which is `run_command` unless a test
    stands one in. None of them pushes to `main`: the branch is pushed, the pull
    request is opened against `main` with `gh pr create`, and `gh pr merge
    --auto --merge` (the repository's merge method) lands it when CI is green.
    The record says which step stopped it, or that there was nothing to commit.

    A second run on one date -- a filing named by hand after the scheduled
    night -- finds `nightly-<date>` taken when the first night's branch is
    still on the remote, and a push onto it would be refused and the run's
    directories lost with the runner; it takes `nightly-<date>-2`, then `-3`.
    """
    run = runner if runner is not None else run_command
    title = f"the nightly crew's night of {date}"
    out = {"branch": None, "pull_request": None, "auto_merge": False, "reason": None}

    def failed(name: str, done: subprocess.CompletedProcess) -> dict:
        tail = [line for line in (done.stderr or "").splitlines() if line.strip()]
        out["reason"] = f"{name}: exit {done.returncode}: " + " | ".join(tail[-REASON_LINES:])
        return out

    listed = run(["git", "ls-remote", "--heads", "origin"])
    if listed.returncode:
        return failed("git ls-remote", listed)
    taken = {line.split("refs/heads/", 1)[1].strip()
             for line in (listed.stdout or "").splitlines() if "refs/heads/" in line}
    branch, again = f"nightly-{date}", 2
    while branch in taken:
        branch, again = f"nightly-{date}-{again}", again + 1
    out["branch"] = branch

    done = run(["git", "checkout", "-b", branch])
    if done.returncode:
        return failed("git checkout", done)
    # `git add` refuses every path when one does not exist, and a night that
    # found nothing new has no runs/ to add.
    written = [name for name in PUBLISHED if (root / name).exists()]
    if written:
        done = run(["git", "add", "--", *written])
        if done.returncode:
            return failed("git add", done)
    staged = run(["git", "diff", "--cached", "--quiet"])
    if staged.returncode == 0:
        out["reason"] = "nothing to publish: the night committed no line and no run"
        return out
    if staged.returncode != 1:
        return failed("git diff --cached", staged)
    message = f"{title}: detect, extract, check, price, collect"
    if run_url:
        message += f"\n\nRun: {run_url}"
    for name, argv in (
            ("git commit", ["git", "commit", "-q", "-m", message]),
            ("git push", ["git", "push", "-u", "origin", branch]),
    ):
        done = run(argv)
        if done.returncode:
            return failed(name, done)
    body = f"Run: {run_url}" if run_url else "the night's run directories and its ledger line"
    done = run(["gh", "pr", "create", "--base", "main", "--head", branch,
                "--title", title, "--body", body])
    if done.returncode:
        return failed("gh pr create", done)
    # `gh pr create` prints the pull request's address last.
    printed = [line for line in (done.stdout or "").splitlines() if line.strip()]
    out["pull_request"] = printed[-1] if printed else None
    done = run(["gh", "pr", "merge", "--auto", "--merge", branch])
    if done.returncode:
        return failed("gh pr merge --auto", done)
    out["auto_merge"] = True
    return out


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
    parser.add_argument("--history-batch", type=int, default=0,
                        help="past filings to collect tonight; 0 collects none")
    parser.add_argument("--history", default=str(collect_history.HISTORY))
    parser.add_argument("--publish", action="store_true",
                        help="commit the night on nightly-<date> and open its "
                             "auto-merging pull request")
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
    fetcher = collect_history.CachingFetcher(
        os.environ.get("EDGAR_USER_AGENT", fetch_fixtures.DEFAULT_USER_AGENT))
    try:
        # Inside the try: an unreadable summary line is the night's failure
        # line, not a night that leaves none.
        since = since or since_from(summary, today)
        line = night(fetcher=fetcher, since=since, runs_root=Path(args.runs),
                     work=Path(args.work), fixtures=Path(args.fixtures), hand=hand,
                     run_url=args.run_url, today=today, retry=to_retry(summary),
                     environ=os.environ)
    except Exception as exc:  # noqa: BLE001 - a night that crashed still leaves a line
        line = crashed(today, since, args.run_url, exc)
    line["failures"] = refused + line["failures"]
    line = with_history(line, fetcher, history_root=Path(args.history),
                        work=Path(args.work) / "history", batch=args.history_batch)
    try:
        append(summary, line)
    except OSError as exc:
        print(f"nightly: the summary could not be written: {exc}", file=sys.stderr)
        return NOT_WRITTEN
    print(json.dumps(line, indent=2))
    code = FAILED if line["failures"] else 0
    if args.publish:
        published = publish(date=line["date"], run_url=args.run_url)
        print(json.dumps({"publish": published}, indent=2))
        # A night with nothing to commit is not a failure; a step that stopped
        # short of auto-merge is, because the line is then waiting for a click.
        if published["reason"] and not published["reason"].startswith("nothing to publish"):
            print(f"nightly: the night was not published: {published['reason']}",
                  file=sys.stderr)
            code = FAILED
    return code


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
