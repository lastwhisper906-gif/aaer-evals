"""Historical collection: the twelve's past filings, a few a night, each checked.

The owner's decision of 2026-09-24 (`docs/structure_changes.md`): past filings
are collected a little every night. This is data collection under the first
decision of 2026-09-23, "collect all the data first"; it records what EDGAR
served and what the four extraction checks said, and nothing about signal.

**Scope.** Every 10-K, 10-Q and 8-K carrying item 2.02 each company in
`universe.json` has filed since its first XBRL filing, read off the EDGAR
submissions index -- the recent list and every older page it points to, because
the recent list stops at about a thousand rows and a company that files many
ownership forms runs off its end within a few years. "Since XBRL began" is the
filing date of the company's earliest row that EDGAR marks `isXBRL`.

**Order.** Oldest first across all companies, by filing date, then ticker, then
accession, so the collection grows forward in time and every night's batch is
the next one in line. A filing is collected once: its accession is on a line of
`history/{ticker}/manifest.jsonl` or it is still to come.

**For each filing.** The primary document is fetched and its sha256 recorded,
with the URL, so the filing can be fetched again from EDGAR, which is the
archive, and checked against this record. A 10-K or 10-Q is then carried
through extract exactly as a new filing is: a store fetched as of its filing
date, holding it and nothing later; the companyfacts record as of that date;
the bundle built for that accession or refused; and the four extraction checks
(`src/extraction_checks.py`), with the drift baseline read from the committed
fixtures. Their four results go on the filing's line. An 8-K carrying item 2.02
is recorded with no checks, because extract builds bundles for the two
triggering reports only.

**What is committed.** One line per filing, appended to
`history/{ticker}/manifest.jsonl`, and, when the bundle was built, its files
gzipped under `history/{ticker}/{accession}/` -- whether the checks passed or
not, because a failed check is the thing a reader will want to open. Raw
filings are not committed. The largest bundle the committed fixtures build is
205,560 bytes gzipped (CSCO's 10-Q), and a company files four triggering
reports a year, so seventeen years of them is about 14 MB, under the 50 MB a
company may take; `docs/structure_changes.md` records the measurement.
`history/` is append-only, like `runs/`.

    python3.12 -m src.collect_history --batch 30 --work /tmp/history

Exit 0 when every filing collected tonight was collected and passed or was not
checkable, 1 when any failed, 3 the wrong interpreter. The JSON summary goes to
standard output.
"""

from __future__ import annotations

import argparse
import datetime as dt
import gzip
import json
import os
import shutil
import sys
from pathlib import Path

try:
    from src import (assemble_bundle, cutoff_guard, extraction_checks, fetch_companyfacts,
                     fetch_fixtures, interpreter_pin, universe)
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import (assemble_bundle, cutoff_guard, extraction_checks, fetch_companyfacts,
                     fetch_fixtures, interpreter_pin, universe)

HISTORY = Path("history")
BATCH = 30
FAILED = 1

TRIGGERING_FORMS = ("10-K", "10-Q")
EARNINGS_FORM, EARNINGS_ITEM = "8-K", "2.02"

# The four gates, as `src/extraction_checks.py` names them on its lines, and the
# slug each result is recorded under.
GATES = {"schema": "schema", "paragraph counts": "paragraph_counts",
         "cutoff": "cutoff", "notes": "text_blocks"}


class CachingFetcher(fetch_fixtures.Fetcher):
    """The fetcher, remembering what `data.sec.gov` answered for one night.

    The submissions pages and the companyfacts record are asked for once per
    filing collected, and a night collects several filings of one company: the
    record is the same document each time, so it is fetched once. Filing
    documents are not kept -- each is read once and they are large.
    """

    def __init__(self, user_agent: str) -> None:
        super().__init__(user_agent)
        self._kept: dict[str, bytes] = {}

    def get(self, url: str) -> bytes:
        if not url.startswith("https://data.sec.gov/"):
            return super().get(url)
        if url not in self._kept:
            self._kept[url] = super().get(url)
        return self._kept[url]


def in_scope(filings: list[dict]) -> list[dict]:
    """Every 10-K, 10-Q and 8-K carrying 2.02 filed since the first XBRL filing."""
    xbrl = [filing["filingDate"] for filing in filings if filing.get("isXBRL")]
    if not xbrl:
        return []
    began = min(xbrl)
    return [filing for filing in filings
            if filing["filingDate"] >= began
            and (filing["form"] in TRIGGERING_FORMS
                 or (filing["form"] == EARNINGS_FORM
                     and EARNINGS_ITEM in (filing.get("items") or "").split(",")))]


def collected(history_root: Path, ticker: str) -> list[dict]:
    """The lines already on record for one company."""
    path = history_root / ticker / "manifest.jsonl"
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()]


def checks_from(lines: list[str]) -> dict:
    """Each gate's result, read off the lines `extraction_checks.run` printed."""
    out = {slug: None for slug in GATES.values()}
    for line in lines:
        gate, _, rest = line.partition(": ")
        # A gate prints one pass line or one FAIL line per failure, never both.
        if gate in GATES:
            out[GATES[gate]] = "fail" if rest.startswith("FAIL") else "pass"
    return out


def write_gzipped(texts: dict, folder: Path) -> int:
    """The bundle's files, each gzipped with no timestamp. Total bytes written."""
    folder.mkdir(parents=True, exist_ok=True)
    total = 0
    for name, text in sorted(texts.items()):
        packed = gzip.compress(text.encode("utf-8"), mtime=0)
        (folder / f"{name}.gz").write_bytes(packed)
        total += len(packed)
    return total


def extract(fetcher, company: dict, filing: dict, filings: list[dict], *,
            work: Path, history_root: Path) -> dict:
    """One past 10-K or 10-Q through the store, the assembler and the four checks."""
    ticker, cik = company["ticker"], company["cik"]
    accession, form, as_of = (filing["accessionNumber"], filing["form"],
                              filing["filingDate"])
    out = {"result": "failed", "stage": None, "reason": None,
           "checks": None, "bundle": None, "bundle_gzip_bytes": None}
    store = work / "store" / f"{ticker}-{accession}"
    bundle_dir = work / "bundle" / ticker / accession
    try:
        _, problems = fetch_fixtures.fetch_company(fetcher, ticker, cik, as_of, store,
                                                   filings=filings)
        if problems:
            out.update(stage="fetch filings", reason="; ".join(problems))
            return out
        problems = fetch_companyfacts.fetch_company(fetcher, ticker, as_of, store)
        if problems:
            out.update(stage="fetch companyfacts", reason="; ".join(problems))
            return out
        try:
            bundle = assemble_bundle.build(ticker, form, fixtures_root=store,
                                           prior_runs=work / "no-prior-runs",
                                           accession=accession)
        except (assemble_bundle.BundleError, cutoff_guard.CutoffGuardError) as exc:
            out.update(stage="extract", reason=str(exc))
            return out
        assemble_bundle.write(bundle, bundle_dir)
        code, lines = extraction_checks.run(bundle_dir)
        folder = history_root / ticker / accession
        out.update(checks=checks_from(lines), bundle=str(folder),
                   bundle_gzip_bytes=write_gzipped(bundle["texts"], folder))
        if code:
            out.update(stage="extraction checks",
                       reason=" | ".join(line for line in lines if ": FAIL" in line))
            return out
        out.update(result="passed")
        return out
    except Exception as exc:  # noqa: BLE001 - one filing's failure is its own line
        out.update(stage=out["stage"] or "collect", reason=f"{type(exc).__name__}: {exc}")
        return out
    finally:
        shutil.rmtree(store, ignore_errors=True)
        shutil.rmtree(bundle_dir, ignore_errors=True)


def collect_one(fetcher, company: dict, filing: dict, filings: list[dict], *,
                work: Path, history_root: Path) -> dict:
    """One filing's line: where EDGAR serves it, its hash, and the checks."""
    ticker, cik = company["ticker"], company["cik"]
    accession = filing["accessionNumber"]
    url = fetch_fixtures.ARCHIVE_URL.format(
        cik_int=int(cik), accession=accession.replace("-", ""),
        name=filing["primaryDocument"])
    line = {"accession": accession, "form": filing["form"],
            "filing_date": filing["filingDate"], "report_date": filing["reportDate"],
            "items": filing.get("items") or "", "url": url, "sha256": None,
            "bytes": None, "collected_utc": None}
    try:
        raw = fetcher.get(url)
        line.update(sha256=fetch_fixtures.sha256(raw), bytes=len(raw))
    except Exception as exc:  # noqa: BLE001
        line.update(result="failed", stage="fetch primary document",
                    reason=f"{type(exc).__name__}: {exc}", checks=None, bundle=None,
                    bundle_gzip_bytes=None)
    else:
        if filing["form"] in TRIGGERING_FORMS:
            line.update(extract(fetcher, company, filing, filings, work=work,
                                history_root=history_root))
        else:
            line.update(result="not_applicable", stage=None,
                        reason="extract builds 10-K and 10-Q bundles only",
                        checks=None, bundle=None, bundle_gzip_bytes=None)
    line["collected_utc"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return line


def collect(fetcher, *, companies, history_root: Path, work: Path,
            batch: int = BATCH) -> dict:
    """Plan across every company, collect the oldest `batch`, summarise."""
    listing_failures, plan, per_company = [], [], {}
    for company in companies:
        ticker = company["ticker"]
        try:
            filings = fetch_fixtures.every_filing(fetcher, company["cik"])
        except Exception as exc:  # noqa: BLE001
            listing_failures.append(f"{ticker}: the submissions index could not be "
                                    f"listed: {type(exc).__name__}: {exc}")
            continue
        scope = in_scope(filings)
        done = {line["accession"] for line in collected(history_root, ticker)}
        per_company[ticker] = {"filings": filings, "in_scope": len(scope)}
        plan.extend((filing["filingDate"], ticker, filing["accessionNumber"], company, filing)
                    for filing in scope if filing["accessionNumber"] not in done)
    plan.sort(key=lambda entry: entry[:3])

    tonight = []
    for _, ticker, _, company, filing in plan[:batch]:
        line = collect_one(fetcher, company, filing, per_company[ticker]["filings"],
                           work=work, history_root=history_root)
        path = history_root / ticker / "manifest.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as ledger:
            ledger.write(json.dumps(line, sort_keys=True) + "\n")
        tonight.append((ticker, line))

    on_record = [line for company in companies
                 for line in collected(history_root, company["ticker"])]
    return {
        "batch": batch,
        "collected_tonight": len(tonight),
        "passed_tonight": sum(1 for _, line in tonight if line["result"] == "passed"),
        "failed_tonight": [f"{ticker} {line['form']} {line['accession']} filed "
                           f"{line['filing_date']}: {line['stage']}: {line['reason']}"
                           for ticker, line in tonight if line["result"] == "failed"],
        "not_checkable_tonight": sum(1 for _, line in tonight
                                     if line["result"] == "not_applicable"),
        "in_scope": sum(entry["in_scope"] for entry in per_company.values()),
        "collected": len(on_record),
        "passed": sum(1 for line in on_record if line.get("result") == "passed"),
        "remaining": len(plan) - len(tonight),
        "listing_failures": listing_failures,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="a night's batch of past filings")
    parser.add_argument("--batch", type=int, default=BATCH)
    parser.add_argument("--history", default=str(HISTORY))
    parser.add_argument("--work", required=True, help="scratch directory for stores")
    args = parser.parse_args(argv)
    fetcher = CachingFetcher(
        os.environ.get("EDGAR_USER_AGENT", fetch_fixtures.DEFAULT_USER_AGENT))
    summary = collect(fetcher, companies=universe.rows(), history_root=Path(args.history),
                      work=Path(args.work), batch=args.batch)
    print(json.dumps(summary, indent=2))
    return FAILED if summary["failed_tonight"] or summary["listing_failures"] else 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
