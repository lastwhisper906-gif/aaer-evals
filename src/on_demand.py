"""A run on demand: one company, one filing, fetched from EDGAR when asked.

The owner's decision of 2026-10-28 is that the repository does not hold every
company's filings. This is the command that makes that work for any company,
not only the thirty-six of `universe.json`: give it a ticker and a form (or an
accession) and it builds the filing's store in the local cache, through
`src/edgar_client.py`, the way `src/fetch_fixtures.py` builds a fixture store,
then the bundle, then, when asked, the run.

1. **Ticker to CIK.** A company of the universe keeps the CIK its row records
   (`src/fetch_fixtures.py` says why the file, not EDGAR's ticker map, answers
   which registrant a fixture is). Any other ticker is looked up in EDGAR's own
   map, `company_tickers.json`, and must name exactly one registrant; the
   answer and where it came from are printed and returned.
2. **The filing.** The accession given, or the company's latest filing of the
   form, read off the submissions index with every overflow page. Only the
   filings that stood when it was accepted are picked from: a filing made later
   on its own day is not (`known_at`).
3. **The store**, under `$AAER_CACHE/stores/<ticker>-<accession>/`: the
   filing, the documents the bundle reads around it (the latest 10-K, the
   10-Q before, the latest earnings 8-K), the submissions index and the
   companyfacts record, each as of the filing's own date, so nothing filed after
   it is in the store. A store already there is checked against its manifest
   and used as it is; one whose bytes changed is refused.
4. **The bundle**, by `src/assemble_bundle.py` over that store, into
   `runs/<ticker>/<accession>/` unless another directory is named.
5. **The run**, by `src/run_analysis.py`, when `--run` is given.

    python -m src.on_demand --ticker MSFT --form 10-Q
    python -m src.on_demand --ticker MSFT --accession 0001193125-26-191507 --run
    python -m src.on_demand --ticker SOMEONE --cik 1234567 --accession <accession> --run

A run directory that already exists is refused, and the one named is claimed
by creating it before anything is built: `runs/` is append-only, so a published
run, or another invocation's, is never written into. "Any company" still
needs what the bundle is built from: a 10-K, two 10-Qs and an earnings 8-K on
or before the filing; a company without them is refused with what is missing.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from src import assemble_bundle, edgar_client, fetch_fixtures, interpreter_pin, universe
    # the rule of what stood when a filing was accepted is the store's, shared
    # with `fetch_fixtures --accession`
    from src.fetch_fixtures import known_at, stood_before  # noqa: F401
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import assemble_bundle, edgar_client, fetch_fixtures, interpreter_pin, universe
    from src.fetch_fixtures import known_at, stood_before  # noqa: F401

TICKER_MAP = "https://www.sec.gov/files/company_tickers.json"
FORMS = ("10-Q", "10-K")
BAD_INPUT = 2


class OnDemandError(Exception):
    """The company, the filing or the store cannot be had as asked."""


def cik_of(client, ticker: str, *, ticker_map: str = TICKER_MAP) -> tuple[str, str]:
    """The ten-digit CIK for a ticker, and where the answer came from.

    A universe file that cannot be read is an error, not a ticker outside it.
    """
    try:
        if ticker.strip().upper() in universe.tickers():
            return universe.cik(ticker), "universe.json"
    except universe.UniverseError as exc:
        raise OnDemandError(f"universe.json cannot be read: {exc}") from None
    rows = client.get_json(ticker_map)
    found = sorted({int(row["cik_str"]) for row in (rows or {}).values()
                    if isinstance(row, dict) and str(row.get("ticker", "")).upper()
                    == ticker.upper()})
    if len(found) != 1:
        raise OnDemandError(f"{ticker}: EDGAR's ticker map names "
                            f"{len(found)} registrants for it, not one")
    return f"{found[0]:010d}", ticker_map


def the_filing(rows: list[dict], form: str, accession: str | None) -> dict:
    """The submissions row asked for: the accession, or the latest of the form."""
    if accession is not None:
        named = [row for row in rows if row["accessionNumber"] == accession]
        if not named:
            raise OnDemandError(f"{accession} is not in the company's submissions index")
        if named[0]["form"] not in FORMS:
            raise OnDemandError(f"{accession} is a {named[0]['form']}; a run is for a "
                                f"{' or '.join(FORMS)}")
        return named[0]
    latest = max((row for row in rows if row["form"] == form),
                 key=lambda row: (row["filingDate"], row["accessionNumber"]), default=None)
    if latest is None:
        raise OnDemandError(f"the company has filed no {form}")
    return latest


def fetch_store(client, ticker: str, *, form: str = "10-Q", accession: str | None = None,
                root: Path | None = None, ticker_map: str = TICKER_MAP,
                cik: str | None = None) -> dict:
    """The filing's store in the cache, fetched or found, and what it holds.

    `cik`, when given, names the registrant and `ticker` is only the name the
    store and the run go under: a company whose shares no longer trade is in
    no ticker map, and a ticker once its own may name another registrant now."""
    ticker = ticker.upper()
    if cik is not None:
        if not str(cik).strip().isdigit():
            raise OnDemandError(f"--cik {cik!r} is not a number")
        cik, cik_from = f"{int(cik):010d}", "--cik"
    else:
        cik, cik_from = cik_of(client, ticker, ticker_map=ticker_map)
    rows = fetch_fixtures.every_filing(client, cik)
    filing = the_filing(rows, form, accession)
    accession, as_of = filing["accessionNumber"], filing["filingDate"]
    store = (root or client.root / "stores") / f"{ticker}-{accession}"
    problems = fetch_fixtures.store_up_to(client, ticker, cik, filing, store,
                                          filings=known_at(rows, filing))
    if problems:
        raise OnDemandError(f"{ticker} {accession}: " + "; ".join(problems))
    return {"ticker": ticker, "cik": cik, "cik_from": cik_from, "form": filing["form"],
            "accession": accession, "filing_date": as_of,
            "period_end": filing["reportDate"], "store": store}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--form", default="10-Q", choices=FORMS)
    parser.add_argument("--accession", default=None)
    parser.add_argument("--cik", default=None,
                        help="the registrant, when the ticker is not in EDGAR's ticker map "
                             "or names another company now; --ticker is then only the name "
                             "the run goes under")
    parser.add_argument("--out", default=None,
                        help="the run directory; default runs/<ticker>/<accession>/")
    parser.add_argument("--run", action="store_true",
                        help="also run the analysis over the bundle")
    args = parser.parse_args(argv)
    try:
        client = edgar_client.EdgarClient()
        held = fetch_store(client, args.ticker, form=args.form, accession=args.accession,
                           cik=args.cik)
    except (OnDemandError, edgar_client.EdgarError) as exc:
        print(f"on_demand: {exc}", file=sys.stderr)
        return BAD_INPUT
    print(f"{held['ticker']} CIK {held['cik']} (from {held['cik_from']}): {held['form']} "
          f"{held['accession']} filed {held['filing_date']}, store {held['store']}")
    run = args.out or str(assemble_bundle.default_out(held["ticker"], held["accession"]))
    try:
        # Claimed by creating it, which only one process can do: `runs/` is
        # append-only (CLAUDE.md), so a directory that is already there -- a
        # published run, another invocation's -- is never written into, and a
        # new run of the same filing goes in a directory of its own.
        Path(run).parent.mkdir(parents=True, exist_ok=True)
        Path(run).mkdir()
    except OSError as exc:
        print(f"on_demand: {run} cannot be claimed for a new run ({type(exc).__name__}); "
              "name a new directory with --out", file=sys.stderr)
        return BAD_INPUT
    status = None
    try:
        status = assemble_bundle.main(["--ticker", held["ticker"], "--form", held["form"],
                                       "--accession", held["accession"],
                                       "--fixtures", str(held["store"]), "--out", run])
    finally:
        # a bundle that failed, by its status or by an exception, gives the
        # claim back when nothing was written in it; what it did write stays,
        # named, for whoever reads the failure
        if status != 0:
            if not any(Path(run).iterdir()):
                Path(run).rmdir()
            else:
                print(f"on_demand: the bundle failed part-way; what it wrote is left in "
                      f"{run}", file=sys.stderr)
    if status or not args.run:
        return status
    from src import run_analysis      # imported here: the fetch needs none of it
    return run_analysis.main(["--run", run, "--ticker", held["ticker"], "--form", held["form"],
                              "--cutoff", held["filing_date"],
                              "--period-end", held["period_end"],
                              "--store", str(held["store"])])


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
