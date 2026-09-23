"""Record where each row of `universe.json` got its CIK and SIC. Read-only on EDGAR.

A row's SIC is not in any filing this project stores: `submissions.json` beside
each company is the recent-filings rows of the EDGAR submissions index, and the
company's own header -- name, SIC, SIC description, tickers -- sits in the same
document above those rows and was projected away. So a SIC typed into
`universe.json` had nothing committed behind it. This stores that header.

For each company in `universe.json` it fetches
`data.sec.gov/submissions/CIK<cik>.json` through `fetch_fixtures.Fetcher` (the
declared User-Agent the SEC requires, and the same rate limit), and writes
`tests/fixtures/universe/<ticker>.json`: every top-level field of the document
EDGAR served *except* `filings`, with the url, the time it was fetched, and the
byte count and sha256 of the whole document as served.

`filings` is left out for the reason `fetch_fixtures.submissions_record` filters
its rows to the cutoff: fetched after the cutoff, the list names filings made
after it, and a fixture carrying them is look-ahead waiting to be read. The
header is a classification of the registrant, not a filing, and nothing here
hands it to a reader.

**A record is never rewritten.** A file already on disk is skipped. If EDGAR
reclassifies a company, that is a new fact with a new date, and the correction
is a new file, not an edit to this one.

    python3.12 -m src.fetch_universe_source [--ticker NVDA ...]

Exit 0 every requested header is on disk, 2 a fetch failed, 3 the wrong
interpreter.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

try:
    from src import fetch_fixtures, interpreter_pin, universe
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import fetch_fixtures, interpreter_pin, universe

OUT = fetch_fixtures.FIXTURES / "universe"


def header_record(ticker: str, cik: str, raw: bytes) -> dict:
    """The served document's header: every field but `filings`, plus provenance."""
    served = json.loads(raw)
    return {
        "ticker": ticker,
        "url": fetch_fixtures.SUBMISSIONS_URL.format(cik=cik),
        "fetched_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "served_bytes": len(raw),
        "served_sha256": fetch_fixtures.sha256(raw),
        "note": ("every top-level field of the EDGAR submissions document except "
                 "`filings`, which lists filings made after the cutoff"),
        "header": {key: value for key, value in served.items() if key != "filings"},
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticker", action="append", default=None,
                        help="one company (repeatable); default is every row")
    parser.add_argument("--out", default=str(OUT), help="where the headers go")
    args = parser.parse_args(argv)

    tickers = (tuple(t.upper() for t in args.ticker) if args.ticker
               else universe.tickers())
    out = Path(args.out)
    fetcher = fetch_fixtures.Fetcher(
        os.environ.get("EDGAR_USER_AGENT", fetch_fixtures.DEFAULT_USER_AGENT))

    problems = []
    for ticker in tickers:
        path = out / f"{ticker}.json"
        if path.exists():
            continue
        cik = universe.cik(ticker)
        try:
            raw = fetcher.get(fetch_fixtures.SUBMISSIONS_URL.format(cik=cik))
            record = header_record(ticker, cik, raw)
        except Exception as exc:  # noqa: BLE001 - the reason matters more than the type
            problems.append(f"{ticker}: {type(exc).__name__}: {exc}")
            continue
        out.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")
        print(f"{ticker} sic {record['header'].get('sic')} "
              f"{record['header'].get('sicDescription')}")

    if problems:
        print("fetch_universe_source: incomplete:", file=sys.stderr)
        for line in problems:
            print(f"  {line}", file=sys.stderr)
        return fetch_fixtures.FETCH_FAILED
    return 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
