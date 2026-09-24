"""Fetch the fixture filings for the twelve companies from EDGAR. Read-only.

For each company, as of a fixed date, this pulls three filings:

    10-K   the latest annual report      XBRL instance + primary HTML
    10-Q   the latest quarterly report   XBRL instance + primary HTML
    10-Q   the one before it             the same two, as `prior_period`
    8-K    the latest one carrying item 2.02, with exhibit 99.1

and stores them under `tests/fixtures/{ticker}/{form}/`, with one
`manifest.json` per company recording, for every file, the accession number,
the URL it came from, the filing date and the sha256 of the bytes as EDGAR
served them.

Beside them it stores `tests/fixtures/{ticker}/submissions.json`: the rows of
the EDGAR submissions index, which is where an 8-K's item codes come from and
the only place they are stated. It is filtered to the cutoff and projected to
the fields used — see `submissions_record` for why both, and for the one place
in this file where "the bytes EDGAR served" is deliberately not the rule.

**Fixtures are records.** A file already on disk is never re-fetched and never
overwritten: if its bytes no longer match the manifest the script stops with
exit 4 rather than repairing anything. Adding a company or a form appends;
nothing is rewritten. That is the same rule the published record lives under,
applied to the inputs the parsers are judged against.

Files larger than 2 MB are stored gzipped with a `.gz` suffix. The recorded
sha256 is always of the raw document, so the record is of what EDGAR served and
not of how it is packed.

EDGAR requires a declared contact in the User-Agent header and refuses the
Archives without one. `EDGAR_USER_AGENT` overrides the default; the default
declares the repository owner, because a fetch this project's whole input layer
depends on should not announce a contact nobody reads.

    python3.12 src/fetch_fixtures.py [--as-of 2026-09-01] [--ticker AAPL ...]
    python3.12 src/fetch_fixtures.py --ticker CIEN --accession 0001628280-26-060361 --out STORE

**`--accession` fetches a store up to that filing.** The as-of date becomes the
filing date the submissions index gives the accession, so nothing filed after it
is in the store. An accession the index does not list for the company is refused
before anything is fetched: a store built to some other date would hand extract
a different filing. `--as-of` beside it is refused rather than replaced: a
cutoff that was given is never silently swapped for a later one. The store has
to be new -- a company directory that already exists keeps every document in
it, whatever date it was fetched to -- and once fetched, the store's filing of
that form has to be the one named: two filings of one form on one day are
picked by accession, and the named one may be the other. Either is exit 2,
never a store reported complete. The store also gets the companyfacts record
as of the same date (`src/fetch_companyfacts.py`), because the trend table is
built from it and a store without it is not one extract can build from.

Exit 0 all requested fixtures present, 2 a fetch or parse failed, 3 the wrong
interpreter, 4 a fixture on disk disagrees with its manifest.
"""

from __future__ import annotations

import argparse
import datetime as dt
import gzip
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

try:
    from src import interpreter_pin, universe
except ImportError:  # invoked as a plain script: python3.12 src/fetch_fixtures.py
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import interpreter_pin, universe

# The twelve were a literal here and three other modules imported it from this
# one, which made the universe a code change. It is `universe.json` at the
# repository root now. This name stays because the tests parametrise on it at
# import time, and it is a snapshot: `main` below asks `universe.tickers()`
# again when it runs, so a row appended to the file is a company this process
# will fetch without being restarted.
TICKERS = universe.tickers()

AS_OF = "2026-09-01"
FIXTURES = Path(__file__).resolve().parent.parent / "tests" / "fixtures"

DEFAULT_USER_AGENT = "aaer-evals research lastwhisper906@gmail.com"
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
ARCHIVE_URL = "https://www.sec.gov/Archives/edgar/data/{cik_int}/{accession}/{name}"

GZIP_OVER_BYTES = 2 * 1024 * 1024
# SEC asks for no more than ten requests a second. Six is polite and still
# finishes twelve companies in a couple of minutes.
MIN_SECONDS_BETWEEN_REQUESTS = 0.17

# The submission's own SGML header, as EDGAR republishes it. It is the only
# place the exhibit's *type* is stated: filers name the file anything they like
# -- q2fy27pr.htm, ex_994826.htm, a99-q22026earningsexhibit.htm are all EX-99.1
# -- so a filename heuristic picks the wrong document or none.
HEADER_URL = "https://www.sec.gov/Archives/edgar/data/{cik_int}/{accession}/{acc_dashed}-index-headers.html"
DOCUMENT_TYPE = re.compile(
    r"(?:<|&lt;)TYPE(?:>|&gt;)\s*(\S+).*?(?:<|&lt;)FILENAME(?:>|&gt;)\s*(\S+)",
    re.IGNORECASE | re.DOTALL)

FETCH_FAILED = 2
FIXTURE_CHANGED = 4


class Fetcher:
    """Every EDGAR request goes through here, so the rate limit is not optional."""

    def __init__(self, user_agent: str) -> None:
        self.user_agent = user_agent
        self._last = 0.0

    def get(self, url: str) -> bytes:
        for attempt in range(4):
            wait = self._last + MIN_SECONDS_BETWEEN_REQUESTS - time.monotonic()
            if wait > 0:
                time.sleep(wait)
            self._last = time.monotonic()
            request = urllib.request.Request(
                url, headers={"User-Agent": self.user_agent,
                              "Accept-Encoding": "identity"})
            try:
                with urllib.request.urlopen(request, timeout=60) as response:
                    return response.read()
            except urllib.error.HTTPError as exc:
                # EDGAR answers a client over its rate with 403 as well as 429,
                # so both are backed off before they are believed.
                if exc.code in (403, 429, 502, 503, 504) and attempt < 3:
                    time.sleep(2 ** attempt)
                    continue
                raise
            except urllib.error.URLError:
                if attempt < 3:
                    time.sleep(2 ** attempt)
                    continue
                raise
        raise RuntimeError(f"unreachable: {url}")

    def get_json(self, url: str):
        return json.loads(self.get(url))


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def recent_filings(fetcher: Fetcher, cik: str) -> list[dict]:
    """The submissions index as a list of rows, newest first."""
    data = fetcher.get_json(SUBMISSIONS_URL.format(cik=cik))
    recent = data["filings"]["recent"]
    fields = ("accessionNumber", "filingDate", "reportDate", "form", "items",
              "primaryDocument", "primaryDocDescription")
    return [{field: recent[field][i] for field in fields}
            for i in range(len(recent["form"]))]


OLDER_URL = "https://data.sec.gov/submissions/{name}"
ROW_FIELDS = ("accessionNumber", "filingDate", "reportDate", "form", "items",
              "primaryDocument", "primaryDocDescription", "isXBRL")


def every_filing(fetcher: Fetcher, cik: str) -> list[dict]:
    """The whole submissions index: the recent list and every older page.

    `filings.recent` stops at about a thousand rows; the rest are on the pages
    `filings.files` names, each holding the same parallel arrays at its top
    level. A company that files many ownership forms runs off the end of the
    recent list within a few years, so a history read from it alone would begin
    wherever that happened to be.
    """
    data = fetcher.get_json(SUBMISSIONS_URL.format(cik=cik))
    pages = [data["filings"]["recent"]]
    for older in data["filings"].get("files", []):
        pages.append(fetcher.get_json(OLDER_URL.format(name=older["name"])))
    rows, seen = [], set()
    for page in pages:
        for i in range(len(page["form"])):
            row = {field: (page[field][i] if field in page else None)
                   for field in ROW_FIELDS}
            if row["accessionNumber"] not in seen:
                seen.add(row["accessionNumber"])
                rows.append(row)
    return rows


def submissions_record(ticker: str, cik: str, as_of: str,
                       filings: list[dict]) -> tuple[dict, bytes]:
    """The submissions index, as a fixture.

    Two departures from "store the bytes EDGAR served", both deliberate.

    It is **filtered to `filing_date <= as_of`**. The live index grows: fetched
    today it lists filings made after the cutoff this fixture set is pinned to,
    and a fixture carrying post-cutoff rows is the look-ahead the whole project
    exists to prevent — a gate downstream would be guarding a file that should
    never have contained them. The cutoff is applied where the document enters
    the record, not where it is read.

    It is **projected to the fields the index is used for**. `recent_filings`
    already reduces EDGAR's parallel arrays to rows; storing those rows is
    storing the index this program actually read. The url is recorded so the
    original is one request away.

    The manifest's `filing_date` for this record is the latest filing in it, so
    reading it under an earlier cutoff is refused rather than quietly allowed.
    """
    rows = [{"accession": filing["accessionNumber"],
             "filing_date": filing["filingDate"],
             "report_date": filing["reportDate"],
             "form": filing["form"],
             "items": filing["items"] or "",
             "primary_document": filing["primaryDocument"],
             "primary_doc_description": filing["primaryDocDescription"] or ""}
            for filing in filings if filing["filingDate"] <= as_of]
    rows.sort(key=lambda row: (row["filing_date"], row["accession"]), reverse=True)
    payload = {
        "ticker": ticker,
        "cik": cik,
        "as_of": as_of,
        "url": SUBMISSIONS_URL.format(cik=cik),
        "note": ("the recent-filings rows of the EDGAR submissions index, "
                 "projected to these fields and filtered to filing_date <= as_of"),
        "filings": rows,
    }
    return payload, (json.dumps(payload, indent=2) + "\n").encode("utf-8")


class NotInIndex(LookupError):
    """The submissions index does not list this accession for this company."""


def filing_for(filings: list[dict], accession: str) -> dict:
    """The submissions row for one accession, or NotInIndex."""
    for filing in filings:
        if filing["accessionNumber"] == accession:
            return filing
    raise NotInIndex(f"{accession} is not in the EDGAR submissions index for this "
                     f"company ({len(filings)} filings listed)")


def pick(filings: list[dict], as_of: str, form: str, item: str | None = None):
    """The latest filing of this form at or before the cutoff date."""
    matches = [f for f in filings
               if f["form"] == form and f["filingDate"] <= as_of
               and (item is None or item in (f["items"] or ""))]
    return max(matches, key=lambda f: (f["filingDate"], f["accessionNumber"]), default=None)


def pick_previous(filings: list[dict], as_of: str, form: str):
    """The filing of this form before the latest one, still at or before the cutoff.

    The prior-period diff needs a pair. One 10-Q per company is one period, and
    a differ with nothing to diff against silently carries the full text and
    looks like it works.
    """
    latest = pick(filings, as_of, form)
    if latest is None:
        return None
    key = (latest["filingDate"], latest["accessionNumber"])
    earlier = [f for f in filings
               if f["form"] == form and f["filingDate"] <= as_of
               and (f["filingDate"], f["accessionNumber"]) < key]
    return max(earlier, key=lambda f: (f["filingDate"], f["accessionNumber"]), default=None)


def directory(fetcher: Fetcher, cik: str, accession: str) -> list[str]:
    url = ARCHIVE_URL.format(cik_int=int(cik), accession=accession.replace("-", ""), name="index.json")
    return [item["name"] for item in fetcher.get_json(url)["directory"]["item"]]


def document_types(fetcher: Fetcher, cik: str, accession: str) -> list[tuple[str, str]]:
    """(type, filename) for every document in the submission, in sequence order."""
    url = HEADER_URL.format(cik_int=int(cik), accession=accession.replace("-", ""),
                            acc_dashed=accession)
    header = fetcher.get(url).decode("utf-8", "replace")
    return [(t.upper(), name) for t, name in DOCUMENT_TYPE.findall(header)]


def wanted_documents(form: str, filing: dict, names: list[str],
                     types: list[tuple[str, str]]) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """(role, filename) pairs to fetch, plus (role, reason) for anything not found."""
    primary = filing["primaryDocument"]
    wanted, missing = [("primary_html", primary)], []
    if form in ("10-K", "10-Q"):
        # EDGAR extracts the instance from an inline-XBRL primary document and
        # publishes it beside it as {stem}_htm.xml.
        stem = primary.rsplit(".", 1)[0]
        instance = f"{stem}_htm.xml"
        if instance not in names:
            candidates = [n for n in names if n.endswith("_htm.xml")]
            instance = candidates[0] if candidates else ""
        if instance:
            wanted.append(("xbrl_instance", instance))
        else:
            missing.append(("xbrl_instance",
                            f"{form} {filing['accessionNumber']}: no XBRL instance in the filing"))
        return wanted, missing
    # 8-K: the body carries the item text, exhibit 99.1 the earnings release.
    exhibit = next((n for t, n in types if t == "EX-99.1"), None) \
        or next((n for t, n in types if t.startswith("EX-99")), None)
    if exhibit:
        wanted.append(("exhibit_99_1", exhibit))
    else:
        missing.append(("exhibit_99_1",
                        f"8-K {filing['accessionNumber']}: no EX-99.1 in the submission header"))
    return wanted, missing


def store(path: Path, raw: bytes) -> tuple[Path, str]:
    """Write the document, gzipped past the size threshold. Returns (path, encoding)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if len(raw) > GZIP_OVER_BYTES:
        packed = path.with_name(path.name + ".gz")
        # mtime=0 so the same document always produces the same file.
        with gzip.GzipFile(filename="", mode="wb", fileobj=packed.open("wb"), mtime=0) as out:
            out.write(raw)
        return packed, "gzip"
    path.write_bytes(raw)
    return path, "identity"


def read_stored(path: Path, encoding: str) -> bytes:
    return gzip.decompress(path.read_bytes()) if encoding == "gzip" else path.read_bytes()


def load_manifest(ticker_dir: Path) -> dict:
    manifest = ticker_dir / "manifest.json"
    return json.loads(manifest.read_text()) if manifest.exists() else {}


def verify_existing(ticker_dir: Path, manifest: dict) -> list[str]:
    """A fixture is a record: on disk it must still be the bytes EDGAR served."""
    problems = []
    for entry in manifest.get("documents", []):
        path = ticker_dir / entry["path"]
        if not path.exists():
            problems.append(f"missing: {path}")
            continue
        if sha256(read_stored(path, entry["stored"])) != entry["sha256"]:
            problems.append(f"changed: {path}")
    return problems


def fetch_company(fetcher: Fetcher, ticker: str, cik: str, as_of: str,
                  out: Path, filings: list[dict] | None = None) -> tuple[dict, list[str]]:
    """Fetch one company's store as of a date.

    `filings` is the submissions index to pick from; `recent_filings` when not
    given. A store for a date years back needs `every_filing`, because the
    filings it picks may be older than the recent list reaches.
    """
    ticker_dir = out / ticker
    manifest = load_manifest(ticker_dir)
    problems = verify_existing(ticker_dir, manifest)
    if problems:
        return manifest, problems

    have = {(e["form"], e["role"]) for e in manifest.get("documents", [])}
    documents = list(manifest.get("documents", []))
    if filings is None:
        filings = recent_filings(fetcher, cik)

    if ("submissions", "submissions_index") not in have:
        record, raw = submissions_record(ticker, cik, as_of, filings)
        if not record["filings"]:
            problems.append(f"{ticker}: the submissions index has no filing on or before {as_of}")
        else:
            path, encoding = store(ticker_dir / "submissions.json", raw)
            documents.append({
                "form": "submissions",
                "role": "submissions_index",
                "accession": "",
                "filing_date": record["filings"][0]["filing_date"],
                "report_date": "",
                "items": "",
                "date_basis": ("the latest filing this index contains; the index "
                               "is not itself a filing and has no filing date"),
                "url": record["url"],
                "path": str(path.relative_to(ticker_dir)),
                "stored": encoding,
                "bytes": len(raw),
                "sha256": sha256(raw),
            })
            print(f"  {ticker} {'index':5s} {'submissions':14s} {len(raw):>9,d} B  "
                  f"{len(record['filings'])} filings ≤ {as_of}")

    for form, item in (("10-K", None), ("10-Q", None), ("8-K", "2.02")):
        filing = pick(filings, as_of, form, item)
        if filing is None:
            problems.append(f"{ticker}: no {form}"
                            f"{'' if item is None else ' with item ' + item}"
                            f" filed on or before {as_of}")
            continue
        accession = filing["accessionNumber"]
        names = directory(fetcher, cik, accession)
        types = document_types(fetcher, cik, accession) if form == "8-K" else []
        wanted, unfound = wanted_documents(form, filing, names, types)
        # A document already on record is never reported missing: the fixture is
        # the record, and a hiccup in one directory listing does not unmake it.
        problems.extend(f"{ticker}: {line}" for role, line in unfound
                        if (form, role) not in have)
        for role, name in wanted:
            if (form, role) in have:
                continue
            url = ARCHIVE_URL.format(cik_int=int(cik),
                                     accession=accession.replace("-", ""), name=name)
            raw = fetcher.get(url)
            path, encoding = store(ticker_dir / form / name, raw)
            documents.append({
                "form": form,
                "role": role,
                "accession": accession,
                "filing_date": filing["filingDate"],
                "report_date": filing["reportDate"],
                "items": filing["items"] or "",
                "url": url,
                "path": str(path.relative_to(ticker_dir)),
                "stored": encoding,
                "bytes": len(raw),
                "sha256": sha256(raw),
            })
            print(f"  {ticker} {form:5s} {role:14s} {len(raw):>9,d} B  {name}")

    # The 10-Q before the one already held, so the prior-period diff has a real
    # pair to work on. Both its documents: the differ reads the HTML, the note
    # change history reads the instance.
    previous = pick_previous(filings, as_of, "10-Q")
    if previous is None:
        if ("10-Q", "prior_period") not in have:
            problems.append(f"{ticker}: only one 10-Q filed on or before {as_of}")
    else:
        accession = previous["accessionNumber"]
        names = directory(fetcher, cik, accession)
        wanted, unfound = wanted_documents("10-Q", previous, names, [])
        prior_roles = {"primary_html": "prior_period",
                       "xbrl_instance": "prior_period_xbrl_instance"}
        problems.extend(f"{ticker}: prior period {line}" for role, line in unfound
                        if ("10-Q", prior_roles[role]) not in have)
        for role, name in wanted:
            prior_role = prior_roles[role]
            if ("10-Q", prior_role) in have:
                continue
            url = ARCHIVE_URL.format(cik_int=int(cik),
                                     accession=accession.replace("-", ""), name=name)
            raw = fetcher.get(url)
            path, encoding = store(ticker_dir / "10-Q" / name, raw)
            documents.append({
                "form": "10-Q",
                "role": prior_role,
                "accession": accession,
                "filing_date": previous["filingDate"],
                "report_date": previous["reportDate"],
                "items": previous["items"] or "",
                "url": url,
                "path": str(path.relative_to(ticker_dir)),
                "stored": encoding,
                "bytes": len(raw),
                "sha256": sha256(raw),
            })
            print(f"  {ticker} {'10-Q':5s} {prior_role:26s} {len(raw):>9,d} B  {name}")

    manifest = {
        "ticker": ticker,
        "cik": cik,
        "as_of": as_of,
        "fetched_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "EDGAR",
        "documents": sorted(documents, key=lambda d: (d["form"], d["role"])),
    }
    ticker_dir.mkdir(parents=True, exist_ok=True)
    (ticker_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest, problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--as-of", default=None,
                        help=f"cutoff date; nothing filed after it is fetched. "
                             f"Default {AS_OF}")
    parser.add_argument("--ticker", action="append", default=None,
                        help="fetch one company (repeatable); default is all twelve")
    parser.add_argument("--out", default=str(FIXTURES), help="fixture root")
    parser.add_argument("--accession", default=None,
                        help="fetch a store up to this filing: the as-of date "
                             "becomes its filing date; needs exactly one --ticker")
    args = parser.parse_args(argv)

    # Read from the file here rather than trusting the import-time snapshot: a
    # thirteenth row is a thirteenth company to plan for, not a restart.
    tickers = (tuple(t.upper() for t in args.ticker) if args.ticker
               else universe.tickers())
    out = Path(args.out)
    if args.accession is not None and len(tickers) != 1:
        print("fetch_fixtures: --accession names one filing of one company; "
              "give exactly one --ticker", file=sys.stderr)
        return FETCH_FAILED
    if args.accession is not None and args.as_of is not None:
        print("fetch_fixtures: --accession sets the as-of date to the filing's own; "
              "give one or the other, not both", file=sys.stderr)
        return FETCH_FAILED
    if args.as_of is None:
        args.as_of = AS_OF
    fetcher = Fetcher(os.environ.get("EDGAR_USER_AGENT", DEFAULT_USER_AGENT))

    if args.accession is not None:
        try:
            filing = filing_for(recent_filings(fetcher, universe.cik(tickers[0])),
                                args.accession)
        except (NotInIndex, universe.UniverseError) as exc:
            print(f"fetch_fixtures: {tickers[0]}: {exc}", file=sys.stderr)
            return FETCH_FAILED
        except Exception as exc:  # noqa: BLE001
            print(f"fetch_fixtures: {tickers[0]}: {type(exc).__name__}: {exc}",
                  file=sys.stderr)
            return FETCH_FAILED
        args.as_of = filing["filingDate"]
        if (out / tickers[0]).exists():
            print(f"fetch_fixtures: {out / tickers[0]} already holds a store; a "
                  f"store up to {args.accession} is fetched into a new directory",
                  file=sys.stderr)
            return FETCH_FAILED
        print(f"{tickers[0]} {filing['form']} {args.accession} filed "
              f"{args.as_of}: the store is fetched as of that date")

    # The CIK is the file's, not EDGAR's ticker map's. The map was a second
    # answer to "which registrant is this?" that `universe.json` never got a
    # say in: a row whose ticker the map lacked failed whatever CIK it carried,
    # and a ticker the map had re-pointed would be fetched as someone else.
    problems, changed = [], []
    for ticker in tickers:
        try:
            cik = universe.cik(ticker)
        except universe.UniverseError as exc:
            problems.append(f"{ticker}: {exc}")
            continue
        print(f"{ticker} (CIK {cik})")
        try:
            _, found = fetch_company(fetcher, ticker, cik, args.as_of, out)
        except Exception as exc:  # noqa: BLE001
            problems.append(f"{ticker}: {type(exc).__name__}: {exc}")
            continue
        for line in found:
            (changed if line.startswith(("changed:", "missing:")) else problems).append(line)

    if args.accession is not None and not problems:
        # Imported here: the companyfacts fetcher imports this module.
        from src import fetch_companyfacts
        try:
            problems.extend(fetch_companyfacts.fetch_company(
                fetcher, tickers[0], args.as_of, out))
        except Exception as exc:  # noqa: BLE001
            problems.append(f"{tickers[0]}: companyfacts: {type(exc).__name__}: {exc}")
    if args.accession is not None and not problems:
        held = {entry["accession"] for entry in
                load_manifest(out / tickers[0]).get("documents", [])
                if entry.get("form") == filing["form"] and entry.get("role") == "primary_html"}
        if held != {args.accession}:
            problems.append(f"{tickers[0]}: the store's {filing['form']} is "
                            f"{', '.join(sorted(held)) or 'missing'}, not {args.accession}")

    if changed:
        print("fetch_fixtures: fixtures on disk no longer match their manifest — "
              "fixtures are records and are not repaired here:", file=sys.stderr)
        for line in changed:
            print(f"  {line}", file=sys.stderr)
        return FIXTURE_CHANGED
    if problems:
        print("fetch_fixtures: incomplete:", file=sys.stderr)
        for line in problems:
            print(f"  {line}", file=sys.stderr)
        return FETCH_FAILED
    print(f"fetch_fixtures: {len(tickers)} companies complete as of {args.as_of}")
    return 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
