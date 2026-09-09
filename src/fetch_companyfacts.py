"""Fetch the twelve companies' standard-taxonomy filing history from EDGAR. Read-only.

One request per company to

    https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json

returns every numeric fact the company has ever reported under a standard
taxonomy -- `us-gaap` and `dei` -- for every period, each carrying the accession
number and the filing date that reported it. `docs/INPUT_SPEC.md` names it as
the source for the trend table, the fourth-quarter derivation, the
quiet-restatement trace and the formula-baseline terms, so all four read one
as-filed point-in-time record rather than the single instance a filing carries.

The record is stored as `tests/fixtures/{ticker}/companyfacts.json`, beside the
filings and gzipped past the same 2 MB threshold `src/fetch_fixtures.py` uses,
and its sha256 goes into that company's `manifest.json` as one more document
row. The manifest is where every fixture's hash already lives, and a second
place to look is a second thing to keep true.

**Filtered to the cutoff**, exactly as `fetch_fixtures.submissions_record` is
and for the same reason: companyfacts grows with every filing, so fetched today
it carries facts from filings made after the date this fixture set is pinned to.
A row is kept when its own `filed` date is at or before `--as-of`; a concept or
a unit left with no row is dropped rather than kept empty, because a concept
present only through a later filing is that filing showing through. The cutoff
is applied where the document enters the record, not where it is read.

Everything else is the document EDGAR served. The fact rows keep EDGAR's own
keys -- `accn`, `fy`, `fp`, `val`, `filed`, `frame` -- because those rows are the
record; the keys around them are this repository's, so `cik` is the ten-digit
form the manifests use and `entityName` is written `entity_name`.

**Fixtures are records.** A companyfacts document already on record is never
re-fetched and never overwritten: if its bytes no longer match the manifest the
script stops with exit 4 rather than repairing anything.

Access, probed on 2026-09-09 before this was written rather than assumed:
`data.sec.gov` answers 200 to a declared User-Agent, 403 to curl's default one
and 403 to a User-Agent containing github.com. `www.sec.gov`, which
`fetch_fixtures` reads, additionally refuses anything with no email-shaped
contact, so the default here is the same contact that one declares and
`EDGAR_USER_AGENT` overrides both.

    python3.12 src/fetch_companyfacts.py [--as-of 2026-09-01] [--ticker AAPL ...]

Exit 0 all requested companies on record, 2 a fetch failed or a company has no
fixture manifest to record it in, 3 the wrong interpreter, 4 a fixture on disk
disagrees with its manifest.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

try:
    from src import fetch_fixtures, interpreter_pin
except ImportError:  # invoked as a plain script: python3.12 src/fetch_companyfacts.py
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import fetch_fixtures, interpreter_pin

COMPANYFACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"

# One more row in the manifest's `documents`, in the shape the filings use.
FORM = "companyfacts"
ROLE = "standard_taxonomy_history"
FILENAME = "companyfacts.json"

DATE_BASIS = ("the latest filing whose facts this record contains; companyfacts "
              "is a catalogue of facts drawn from many filings and is not itself "
              "a filing")
NOTE = ("the EDGAR companyfacts document, filtered to fact rows with "
        "filed <= as_of; each row is as EDGAR wrote it")


def rows(facts: dict):
    """Every fact row in a companyfacts `facts` object, with what names it."""
    for namespace, concepts in facts.items():
        for tag, concept in concepts.items():
            for unit, unit_rows in concept.get("units", {}).items():
                for row in unit_rows:
                    yield namespace, tag, unit, row


def undated(facts: dict) -> list[str]:
    """Rows with no filing date of their own. The cutoff filter cannot read them."""
    return [f"{namespace}:{tag} {unit}" for namespace, tag, unit, row in rows(facts)
            if not row.get("filed")]


def within_cutoff(facts: dict, as_of: str) -> dict:
    """The `facts` object with every row filed after `as_of` removed.

    A unit with no row left is dropped and so is a concept with no unit left: a
    tag that exists in this record only because a later filing introduced it is
    that filing showing through, which is the look-ahead the cutoff exists to
    stop.
    """
    kept = {}
    for namespace, concepts in facts.items():
        namespace_kept = {}
        for tag, concept in concepts.items():
            units = {}
            for unit, unit_rows in concept.get("units", {}).items():
                inside = [row for row in unit_rows if row["filed"] <= as_of]
                if inside:
                    units[unit] = inside
            if units:
                namespace_kept[tag] = dict(concept, units=units)
        if namespace_kept:
            kept[namespace] = namespace_kept
    return kept


def latest_filed(facts: dict) -> str:
    """The filing date of the newest filing this record carries a fact from."""
    return max((row["filed"] for _, _, _, row in rows(facts)), default="")


def companyfacts_record(ticker: str, cik: str, as_of: str,
                        served: dict) -> tuple[dict, bytes]:
    payload = {
        "ticker": ticker,
        "cik": cik,
        "as_of": as_of,
        "url": COMPANYFACTS_URL.format(cik=cik),
        "note": NOTE,
        "entity_name": served.get("entityName", ""),
        "facts": within_cutoff(served.get("facts", {}), as_of),
    }
    return payload, (json.dumps(payload, indent=2) + "\n").encode("utf-8")


def on_record(manifest: dict) -> dict | None:
    for entry in manifest.get("documents", []):
        if (entry.get("form"), entry.get("role")) == (FORM, ROLE):
            return entry
    return None


def verify_existing(ticker_dir: Path, entry: dict) -> list[str]:
    """A fixture is a record: on disk it must still be the bytes that were hashed.

    A file that no longer reads back at all -- a truncated gzip -- disagrees
    with its manifest as surely as one whose bytes changed, and is reported the
    same way, so both leave by the documented exit and neither is repaired.
    """
    path = ticker_dir / entry["path"]
    if not path.exists():
        return [f"missing: {path}"]
    try:
        raw = fetch_fixtures.read_stored(path, entry["stored"])
    except Exception as exc:  # noqa: BLE001 - unreadable is one way of not matching
        return [f"changed: {path}: {type(exc).__name__}: {exc}"]
    return [] if fetch_fixtures.sha256(raw) == entry["sha256"] else [f"changed: {path}"]


def fetch_company(fetcher: fetch_fixtures.Fetcher, ticker: str, as_of: str,
                  out: Path) -> list[str]:
    ticker_dir = out / ticker
    manifest = fetch_fixtures.load_manifest(ticker_dir)
    if not manifest:
        return [f"{ticker}: no fixture manifest under {ticker_dir} — companyfacts "
                f"is recorded beside the filings, so fetch those first"]
    cik = manifest.get("cik")
    if not cik:
        return [f"{ticker}: the fixture manifest records no CIK"]

    held = on_record(manifest)
    if held is not None:
        problems = verify_existing(ticker_dir, held)
        if not problems:
            print(f"  {ticker} on record  {held['path']}  {held['bytes']:>10,d} B")
        return problems

    served = fetcher.get_json(COMPANYFACTS_URL.format(cik=cik))
    missing_dates = undated(served.get("facts", {}))
    if missing_dates:
        return [f"{ticker}: {len(missing_dates)} companyfacts rows carry no filing "
                f"date, so the cutoff cannot be applied to them: "
                f"{', '.join(sorted(set(missing_dates))[:5])}"]

    payload, raw = companyfacts_record(ticker, cik, as_of, served)
    if not payload["facts"]:
        return [f"{ticker}: companyfacts holds no fact filed on or before {as_of}"]

    path, encoding = fetch_fixtures.store(ticker_dir / FILENAME, raw)
    documents = list(manifest.get("documents", []))
    documents.append({
        "form": FORM,
        "role": ROLE,
        "accession": "",
        "filing_date": latest_filed(payload["facts"]),
        "report_date": "",
        "items": "",
        "date_basis": DATE_BASIS,
        "url": payload["url"],
        "path": str(path.relative_to(ticker_dir)),
        "stored": encoding,
        "bytes": len(raw),
        "sha256": fetch_fixtures.sha256(raw),
    })
    manifest = dict(manifest,
                    documents=sorted(documents, key=lambda d: (d["form"], d["role"])))
    (ticker_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"  {ticker} fetched    {path.name}  {len(raw):>10,d} B  "
          f"{sum(1 for _ in rows(payload['facts'])):,d} facts ≤ {as_of}")
    return []


def main(argv: list[str] | None = None) -> int:
    wrong_interpreter = interpreter_pin.enforce()
    if wrong_interpreter:
        return wrong_interpreter

    parser = argparse.ArgumentParser(description="the standard-taxonomy history, "
                                                 "one document per company")
    parser.add_argument("--as-of", default=fetch_fixtures.AS_OF,
                        help="cutoff date; no fact filed after it enters the record")
    parser.add_argument("--ticker", action="append", default=None,
                        help="fetch one company (repeatable); default is all twelve")
    parser.add_argument("--out", default=str(fetch_fixtures.FIXTURES),
                        help="fixture root")
    args = parser.parse_args(argv)

    tickers = tuple(t.upper() for t in args.ticker) if args.ticker \
        else fetch_fixtures.TICKERS
    out = Path(args.out)
    fetcher = fetch_fixtures.Fetcher(
        os.environ.get("EDGAR_USER_AGENT", fetch_fixtures.DEFAULT_USER_AGENT))

    problems, changed = [], []
    for ticker in tickers:
        try:
            found = fetch_company(fetcher, ticker, args.as_of, out)
        except Exception as exc:  # noqa: BLE001 - the reason matters more than the type
            found = [f"{ticker}: {type(exc).__name__}: {exc}"]
        for line in found:
            (changed if line.startswith(("changed:", "missing:")) else problems).append(line)

    if changed:
        print("fetch_companyfacts: fixtures on disk no longer match their manifest — "
              "fixtures are records and are not repaired here:", file=sys.stderr)
        for line in changed:
            print(f"  {line}", file=sys.stderr)
        return fetch_fixtures.FIXTURE_CHANGED
    if problems:
        print("fetch_companyfacts: incomplete:", file=sys.stderr)
        for line in problems:
            print(f"  {line}", file=sys.stderr)
        return fetch_fixtures.FETCH_FAILED
    print(f"fetch_companyfacts: {len(tickers)} companies on record as of {args.as_of}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
