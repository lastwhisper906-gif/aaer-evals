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

Every submissions row and every filing's manifest row also carries
`acceptance_datetime`: EDGAR's acceptance instant, written as Eastern wall time
with its offset (`eastern_stamp` says what the index gives and what it is
turned into). A store fetched before this field existed carries none, and is
read as "no stamp on record"; it is never re-fetched to add one.

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
built from it and a store without it is not one extract can build from, and
the event filings made public since the company's previous periodic report --
event 8-K bodies, auditors' letters, late-filing notices and comment letters
(`fetch_event_filings`, under "event filings" below).

Exit 0 all requested fixtures present, 2 a fetch or parse failed, 3 the wrong
interpreter, 4 a fixture on disk disagrees with its manifest.
"""

from __future__ import annotations

import argparse
import datetime as dt
import gzip
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

try:
    from src import cutoff_guard, interpreter_pin, universe
except ImportError:  # invoked as a plain script: python3.12 src/fetch_fixtures.py
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import cutoff_guard, interpreter_pin, universe

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


# The clock the stamp is written on. `src/market.py` reads every acceptance
# stamp on this clock too (`EXCHANGE_TIMEZONE`), so what the record writes and
# what the market module reads are one zone named once each.
EASTERN = ZoneInfo("America/New_York")
# EDGAR's `acceptanceDateTime`, the only shape it writes: seconds, a fraction,
# and the universal-time letter.
ACCEPTANCE_RAW = re.compile(
    r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.\d{1,6})?Z")


def eastern_stamp(raw) -> str | None:
    """EDGAR's `acceptanceDateTime` as Eastern wall time with its offset, or None.

    The submissions index writes the stamp as `2026-08-26T20:36:00.000Z`, and
    the Z is real: the instant is universal time, not an Eastern wall clock
    with a decorative letter. The queue item that added this field, and
    `src/market.py`'s docstring, take the letter for decoration; the source
    `docs/needs_judgment.md` named for settling it says otherwise. That source
    is the filing's own SGML header, whose `<ACCEPTANCE-DATETIME>` is EDGAR's
    Eastern wall clock with no zone: each of the 43 headers committed under
    `tests/fixtures/` dates its filing the acceptance day when accepted before
    half past five and a later day when after, and five of them (ANET's two
    10-Ks, FTNT's 2026, TTMI's 2026 and WDC's 2025) would break that rule read
    as universal time. Set beside NVDA's index
    (`https://data.sec.gov/submissions/CIK0001045810.json`, read 2026-10-07;
    the rows are kept in
    `tests/fixtures/acceptance_stamp/nvda_submissions_rows.json`):

    * The 10-K 0001045810-26-000021: header `20260225164219`, index
      `2026-02-25T21:42:19.000Z`. The 10-K 0001045810-25-000023: header
      `20250226164833`, index `2025-02-26T21:48:33.000Z`. Each index stamp is
      its header's Eastern clock plus five hours, the offset of standard time
      in February: universal time, to the second. Read as an Eastern wall
      clock, 21:42 is past half past five and EDGAR would have dated the 10-K
      the 26th; the same index row dates it the 25th.
    * The index's other rows agree. Seven Form 4s stamped
      `2026-03-21T00:06:01Z` to `T00:14:03Z` are dated 2026-03-20: as
      universal time they are 20:06 to 20:14 Eastern on the 20th, inside
      EDGAR's hours (six in the morning to ten at night Eastern); as a wall
      clock they fall after midnight, outside them. NVDA's earnings 8-Ks are
      stamped 20:21 in summer and 21:21 in winter: one 16:21 Eastern release
      moving with daylight time, which a wall clock would not do.
    * The 10-Q 0001045810-26-000075, stamped `2026-08-26T20:36:00.000Z` and
      dated 2026-08-26, is 16:36 Eastern as universal time, before half past
      five, so the 26th; as a wall clock it would be after, and the 27th.

    So the stamp is converted: `2026-08-26T20:36:00.000Z` becomes
    `2026-08-26T16:36:00-04:00`, the form `src/market.py` and the cutoff
    grader read (an offset written out, never a Z, never a bare date). A
    missing value, or one in any other shape, is None: the record says "no
    stamp" rather than guess a zone. The fraction is dropped; every one of the
    thousand stamps in NVDA's index writes it `.000`.
    """
    if not isinstance(raw, str):
        return None
    match = ACCEPTANCE_RAW.fullmatch(raw)
    if match is None:
        return None
    try:
        instant = dt.datetime(*(int(part) for part in match.groups()),
                              tzinfo=dt.timezone.utc)
    except ValueError:  # a month 13, an hour 25: not a time
        return None
    return instant.astimezone(EASTERN).isoformat(timespec="seconds")


def recent_filings(fetcher: Fetcher, cik: str) -> list[dict]:
    """The submissions index as a list of rows, newest first.

    A field the page lacks is None on every row, so an index served without
    one (an older page, a stand-in) is still a list of rows and the stamp it
    lacks is "none on record" rather than a crash.
    """
    data = fetcher.get_json(SUBMISSIONS_URL.format(cik=cik))
    recent = data["filings"]["recent"]
    fields = ("accessionNumber", "filingDate", "reportDate", "form", "items",
              "primaryDocument", "primaryDocDescription", "acceptanceDateTime")
    return [{field: (recent[field][i] if field in recent else None) for field in fields}
            for i in range(len(recent["form"]))]


OLDER_URL = "https://data.sec.gov/submissions/{name}"
ROW_FIELDS = ("accessionNumber", "filingDate", "reportDate", "form", "items",
              "primaryDocument", "primaryDocDescription", "isXBRL", "acceptanceDateTime")


def every_filing(fetcher: Fetcher, cik: str) -> list[dict]:
    """The whole submissions index: the recent list and every older page.

    `filings.recent` stops at about a thousand rows; the rest are on the pages
    `filings.files` names, each holding the same parallel arrays at its top
    level. A company that files many ownership forms runs off the end of the
    recent list within a few years, so a history read from it alone would begin
    wherever that happened to be.
    """
    return registrant_and_filings(fetcher, cik)[1]


def registrant_of(data) -> dict:
    """The registrant's own tickers and SIC code, off the index's top level.

    A field the record does not carry, or carries in another shape, is None: a
    reader of this asks for them to price a run, and what it cannot read means
    no prices with that reason, not a failed run.
    """
    held = data if isinstance(data, dict) else {}
    tickers, sic = held.get("tickers"), held.get("sic")
    return {"tickers": ([str(t).strip().upper() for t in tickers]
                        if isinstance(tickers, list) else None),
            "sic": str(sic).strip() if isinstance(sic, (str, int)) and str(sic).strip() else None}


def registrant_and_filings(fetcher: Fetcher, cik: str) -> tuple[dict, list[dict]]:
    """`every_filing`'s rows and, from the same one read of the index, the registrant."""
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
    return registrant_of(data), rows


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
             "acceptance_datetime": eastern_stamp(filing.get("acceptanceDateTime")),
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
        "note": ("the rows of the EDGAR submissions index read for this store (the "
                 "recent list, and every older page for a store up to one filing), "
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


INDEX_PAGE_URL = "https://www.sec.gov/Archives/edgar/data/{cik_int}/{accession}/{acc_dashed}-index.htm"
# A row of a filing's index page: the document's link, then its type cell.
INDEX_ROW = re.compile(r'<a href="[^"]*/([^"/]+)">[^<]*</a></td>\s*<td[^>]*>([^<]*)</td>',
                       re.IGNORECASE)


def _not_found(exc: Exception) -> bool:
    return getattr(exc, "code", None) == 404 or str(exc).rstrip().endswith("HTTP 404")


def document_types(fetcher: Fetcher, cik: str, accession: str) -> list[tuple[str, str]]:
    """(type, filename) for every document in the submission, in sequence order.

    EDGAR serves the submission header as `-index-headers.html` for filings
    of about 2014 on; for an older one that page is not there (Axesstel's 10-K
    for fiscal 2012, 0001193125-13-084624, answers 404), and the filing's
    index page, `-index.htm`, carries the same types in its document tables."""
    folder = dict(cik_int=int(cik), accession=accession.replace("-", ""), acc_dashed=accession)
    try:
        header = fetcher.get(HEADER_URL.format(**folder)).decode("utf-8", "replace")
    except Exception as exc:        # a fetcher of its own kind says not-found its own way
        if not _not_found(exc):
            raise
        page = fetcher.get(INDEX_PAGE_URL.format(**folder)).decode("utf-8", "replace")
        return [(kind.strip().upper(), name) for name, kind in INDEX_ROW.findall(page)
                if kind.strip() and kind.strip() != "&nbsp;"]
    return [(t.upper(), name) for t, name in DOCUMENT_TYPE.findall(header)]


def inline_instance(filing: dict, names: list[str]) -> str:
    """The instance EDGAR extracts from an inline-XBRL primary document and
    publishes beside it as {stem}_htm.xml, or "" for a filing that has none."""
    instance = f"{filing['primaryDocument'].rsplit('.', 1)[0]}_htm.xml"
    if instance not in names:
        candidates = [n for n in names if n.endswith("_htm.xml")]
        instance = candidates[0] if candidates else ""
    return instance


def needs_types(form: str, filing: dict, names: list[str]) -> bool:
    """Whether the submission header must be read to find a document: an
    8-K's exhibit 99.1, and the instance of a report filed before inline XBRL,
    which only the header's EX-101.INS names."""
    return form == "8-K" or (form in ("10-K", "10-Q") and not inline_instance(filing, names))


def wanted_documents(form: str, filing: dict, names: list[str],
                     types: list[tuple[str, str]]) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """(role, filename) pairs to fetch, plus (role, reason) for anything not found."""
    primary = filing["primaryDocument"]
    wanted, missing = [("primary_html", primary)], []
    if form in ("10-K", "10-Q"):
        # A report filed before inline XBRL (large filers before mid-2019,
        # the rest by 2021) carries its instance as a document of its own,
        # typed EX-101.INS in the submission header.
        instance = inline_instance(filing, names) \
            or next((name for kind, name in types if kind == "EX-101.INS"), "")
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
        types = document_types(fetcher, cik, accession) \
            if needs_types(form, filing, names) else []
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
                "acceptance_datetime": eastern_stamp(filing.get("acceptanceDateTime")),
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
        types = document_types(fetcher, cik, accession) \
            if needs_types("10-Q", previous, names) else []
        wanted, unfound = wanted_documents("10-Q", previous, names, types)
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
                "acceptance_datetime": eastern_stamp(previous.get("acceptanceDateTime")),
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


ACCESSION = re.compile(r"(\d{10})-(\d{2})-(\d{6})$")
def accepted_at(stamp) -> dt.datetime | None:
    """An index row's acceptance as an instant, or None when it carries none.

    Read by `eastern_stamp`, the reading the store writes the stamp in and the
    owner's grader compares, so the rule that picks the store and the grader
    that checks it never read one stamp two ways; a stamp it cannot read, a
    date that does not exist among them, is no stamp.
    """
    eastern = eastern_stamp(stamp) if isinstance(stamp, str) else None
    return dt.datetime.fromisoformat(eastern) if eastern else None


def stood_before(row: dict, filing: dict) -> bool:
    """Whether a filing of the trigger's own day was accepted before it.

    The rule of the owner's grader (`evals/regression/mechanical.py`,
    `accepted_before_trigger`), so a store built here is never one it refuses:
    both acceptance stamps, compared as instants, the same instant counting as
    before; else the filer agent's accession sequence, a lower number under the
    same agent and year showing an earlier assembly; else no, since nothing
    shows it.
    """
    if row["accessionNumber"] == filing["accessionNumber"]:
        return True
    theirs = accepted_at(row.get("acceptanceDateTime"))
    mine = accepted_at(filing.get("acceptanceDateTime"))
    if theirs is not None and mine is not None:
        return theirs <= mine
    a, b = ACCESSION.match(row["accessionNumber"]), ACCESSION.match(filing["accessionNumber"])
    return bool(a and b and a.group(1, 2) == b.group(1, 2) and int(a.group(3)) < int(b.group(3)))


def known_at(rows: list[dict], filing: dict) -> list[dict]:
    """The filings that stood when `filing` was accepted.

    The cutoff is the filing's own date, and a filing made later that same day
    is not one its reader could have seen: the owner's grader refuses a
    document accepted after the triggering report on the cutoff day. A row of
    that day is kept when `stood_before` shows it was accepted first. A row
    dated earlier is kept unless both stamps show it was accepted after: a
    Form 4 accepted before ten at night is dated that day, after a report
    accepted after half past five that is dated the next.
    """
    day = filing["filingDate"]
    mine = accepted_at(filing.get("acceptanceDateTime"))

    def later(row: dict) -> bool:
        theirs = accepted_at(row.get("acceptanceDateTime"))
        return theirs is not None and mine is not None and theirs > mine

    return [row for row in rows
            if (row["filingDate"] < day and not later(row))
            or (row["filingDate"] == day and stood_before(row, filing))]


REGISTRANT_NAME = re.compile(
    rb"<dei:EntityRegistrantName\b[^>]*>\s*([^<]*?)\s*</dei:EntityRegistrantName>")


def name_as_filed(out: Path, ticker: str, filing: dict) -> str:
    """The registrant's name as the filing itself states it, or "" when its
    instance states none. EDGAR serves today's name, which a company renamed
    after the filing would show through. Read through the gate, at the filing's
    own date."""
    for row in cutoff_guard.documents(ticker, role="xbrl_instance", fixtures_root=out):
        if row.get("accession") == filing["accessionNumber"]:
            found = REGISTRANT_NAME.search(cutoff_guard.load_bytes(
                row["full_path"], filing["filingDate"], fixtures_root=out))
            return html.unescape(found.group(1).decode("utf-8", "replace")) if found else ""
    return ""


def held_to_the_trigger(out: Path, ticker: str, filing: dict,
                        known: frozenset[str]) -> list[str]:
    """What a store holds that the filing's reader could not have known: an index
    row of a filing that did not stand when it was accepted, a companyfacts row
    filed that day by such a filing, a name other than the one it states. The
    store is read through the gate, at the filing's own date, as the bundle
    reads it."""
    from src import fetch_companyfacts      # it imports this module
    problems = []
    try:
        rows = cutoff_guard.documents(ticker, fixtures_root=out)
        for row in rows:
            if row.get("role") in EVENT_ROLES:
                # an event filing is held only when it stood at the trigger, and
                # a letter only when it was public before the trigger's day
                if row.get("accession") not in known:
                    problems.append(f"{row['full_path']} is from {row.get('accession')}, "
                                    f"which did not stand when {filing['accessionNumber']} "
                                    "was accepted")
                elif row.get("form") in LETTER_FORMS and not row.get("released"):
                    problems.append(f"{row['full_path']} is a {row.get('form')} with no "
                                    "release on record, so nothing shows it was public "
                                    f"before {filing['accessionNumber']}'s day")
                elif str(row.get("released") or "") >= filing["filingDate"]:
                    problems.append(f"{row['full_path']} was made public "
                                    f"{row.get('released')}, not before "
                                    f"{filing['accessionNumber']}'s day")
                continue
            if row.get("form") not in ("submissions", fetch_companyfacts.FORM):
                continue
            path = row["full_path"]
            stored = json.loads(cutoff_guard.load_bytes(path, filing["filingDate"],
                                                        fixtures_root=out))
            if row.get("form") == "submissions":
                late = sorted({one["accession"] for one in stored.get("filings", [])} - known)
                if late:
                    problems.append(f"{path} lists {len(late)} filing(s) that did not stand "
                                    f"when {filing['accessionNumber']} was accepted: "
                                    f"{', '.join(late[:3])}")
                continue
            late = sorted({one.get("accn") for *_, one in fetch_companyfacts.rows(
                               stored.get("facts", {}))
                           if one.get("filed") == filing["filingDate"]
                           and one.get("accn") not in known}, key=str)
            if late:
                problems.append(f"{path} holds rows filed on {filing['filingDate']} by "
                                f"filing(s) accepted after the trigger: "
                                f"{', '.join(map(str, late[:3]))}")
            if stored.get("facts") != fetch_companyfacts.as_of_the_filing(
                    stored.get("facts", {})):
                problems.append(f"{path} keeps a frame or a taxonomy label EDGAR writes today")
            if stored.get("entity_name") != name_as_filed(out, ticker, filing):
                problems.append(f"{path} names the company {stored.get('entity_name')!r}, "
                                "not the name the filing states")
    except cutoff_guard.CutoffGuardError as exc:
        problems.append(f"the store cannot be read through the gate: {exc}")
    return problems


def store_up_to(fetcher, ticker: str, cik: str, filing: dict, out: Path,
                filings: list[dict]) -> list[str]:
    """A store up to one filing, as `--accession` builds one, for `src/on_demand.py`.

    `filing` is the filing's submissions row and `filings` the index rows that
    stood when it was accepted. A store that already holds it, the documents
    around it, the index and companyfacts, as of the filing's own date, is used
    as it is once its bytes are its manifest's and it holds nothing the filing's
    reader could not have known (`held_to_the_trigger`): a store built under an
    earlier rule is refused, not reused. Any other is fetched. The problems come
    back, an empty list when the store is whole.
    """
    ticker_dir = out / ticker
    known = frozenset(row["accessionNumber"] for row in filings)
    manifest = load_manifest(ticker_dir)
    roles = {(entry.get("form"), entry.get("role"), entry.get("accession"))
             for entry in manifest.get("documents", [])}
    whole = (manifest.get("as_of") == filing["filingDate"]
             and (filing["form"], "primary_html", filing["accessionNumber"]) in roles
             and any(form == "companyfacts" for form, _, _ in roles)
             and any(form == "submissions" for form, _, _ in roles)
             and (manifest.get(EVENT_RECORD) or {}).get("for") == filing["accessionNumber"])
    if whole:
        problems = [f"changed: {line}" if not line.startswith(("changed:", "missing:")) else line
                    for line in verify_existing(ticker_dir, manifest)]
        return problems or stale(out, ticker, filing, known)
    _, problems = fetch_company(fetcher, ticker, cik, filing["filingDate"], out,
                                filings=filings)
    if not problems:
        # Imported here: the companyfacts fetcher imports this module.
        from src import fetch_companyfacts
        try:
            name = name_as_filed(out, ticker, filing)
        except cutoff_guard.CutoffGuardError as exc:
            return [f"the filing's own name cannot be read through the gate: {exc}"]
        problems = fetch_companyfacts.fetch_company(
            fetcher, ticker, filing["filingDate"], out, known=known, entity_name=name)
    if not problems:
        held = {entry["accession"] for entry in load_manifest(ticker_dir).get("documents", [])
                if entry.get("form") == filing["form"] and entry.get("role") == "primary_html"}
        if held != {filing["accessionNumber"]}:
            problems = [f"the store's {filing['form']} is "
                        f"{', '.join(sorted(held)) or 'missing'}, not {filing['accessionNumber']}"]
    if not problems:
        problems = fetch_event_filings(fetcher, ticker, cik, filing, out, filings)
    # a store finished off here keeps the index, documents and companyfacts it
    # already held, so it is held to the rule as a whole one is
    return problems or stale(out, ticker, filing, known)


def stale(out: Path, ticker: str, filing: dict, known: frozenset[str]) -> list[str]:
    return [f"{line}; the store was built under another rule, so remove {out} and fetch again"
            for line in held_to_the_trigger(out, ticker, filing, known)]


# --- event filings -------------------------------------------------------------
#
# The filings forensic practice reads beside the periodic reports
# (`docs/HEDGE_FUND_ANALYSIS.md` §2.7 and §5.1 rows 6 and 7): the body of an 8-K
# reporting a terminated agreement (1.02), an accelerated obligation (2.04), exit
# costs (2.05), an impairment (2.06), a listing notice (3.01) or a change to
# holders' rights (3.03); the former auditor's letter (EX-16) of an 8-K reporting
# an auditor change (4.01), with that 8-K's body; the notifications of late
# filing (NT 10-K, NT 10-Q); and the SEC staff's comment letters (UPLOAD) and the
# company's responses (CORRESP).
#
# **Which ones: those made public since the last periodic report.** A store up to
# one filing fetches the event filings that became public after the company's
# previous 10-K or 10-Q stood and before the filing itself was accepted -- the
# filings `known_at` the trigger and not `known_at` the report before it. Each
# event filing so reaches exactly one run, the first periodic report after it was
# public; the earlier ones reached the earlier runs, whose flags come forward in
# `input_prior_predictions.md`, and `input_8k.md`'s item-code list still names
# every 8-K the index holds. The notes reader diffs a report against the prior
# period, and this is the same rule for the filings around it.
#
# **A comment letter is public when EDGAR releases it, not when it was filed.**
# EDGAR's `filingDate` of an UPLOAD or a CORRESP is the day the letter was sent
# in private; the conversation is made public weeks or months after the review
# closes, and the filing's own SGML header states the day
# (`<SEC-HEADER>{accession}.hdr.sgml : YYYYMMDD`, under `<PRIVATE-TO-PUBLIC>`).
# ADTRAN's staff letter printed September 25, 2024 has the EDGAR filing date
# 2024-09-26 and was made public 2024-12-04, after ADTRAN's 10-Q of 2024-11-12:
# a store read by filing date would have handed that 10-Q's reader a letter
# nobody outside the company and the SEC could see. So each letter's header is
# read and its release recorded (`RELEASES`), every letter row carries `released`,
# the gate refuses one made public after the cutoff
# (`cutoff_guard.RELEASED_LATER_FORMS`), and of a letter released on or after the
# trigger's day the store holds neither the document nor the release, since a
# release is a day with no time and the trigger's own day does not show it came
# first. Its row in the store's index is another matter: the index is EDGAR's
# list by filing date, so the row of a letter filed before the trigger and made
# public after it is there (ADTRAN's store for the 10-Q of 2024-11-12 holds the
# rows of three letters made public 2024-12-04). No input prints a letter's
# index row -- `input_8k.md` lists 8-Ks and late-filing notices from the index,
# and letters only from the documents the store holds -- and
# `docs/needs_judgment.md` carries the question of dropping such rows. The date
# printed on a letter decides nothing.
#
# The letters looked at are those filed in the two years before the window
# opens (`LETTER_LOOKBACK_YEARS`), since a letter's release can only be known
# from its header: NVIDIA's of July 2025 waited until January 2026, and a lag
# past two years is outside what this fetches.
#
# Each document is a row of the store's manifest with a role of its own, its
# EDGAR `filingDate`, its acceptance stamp, and for a letter `released`; the
# manifest's `event_filings` records which filing the window was drawn for and
# the report it opens after, so a bundle can say what the store does not hold.

EVENT_ITEMS = ("1.02", "2.04", "2.05", "2.06", "3.01", "3.03")
AUDITOR_CHANGE_ITEM = "4.01"
EVENT_8K_FORMS = ("8-K", "8-K/A")
LATE_NOTICE_FORMS = ("NT 10-K", "NT 10-Q", "NT 10-K/A", "NT 10-Q/A")
LETTER_FORMS = cutoff_guard.RELEASED_LATER_FORMS
PERIODIC_FORMS = ("10-K", "10-Q")
LETTER_LOOKBACK_YEARS = 2
# The roles an event filing's documents carry in a store's manifest.
EVENT_BODY, AUDITOR_LETTER, LATE_NOTICE = "event_body", "auditor_letter", "late_notice"
STAFF_LETTER, COMPANY_RESPONSE = "staff_letter", "company_response"
LETTER_ROLE = {"UPLOAD": STAFF_LETTER, "CORRESP": COMPANY_RESPONSE}
EVENT_ROLES = (EVENT_BODY, AUDITOR_LETTER, LATE_NOTICE, STAFF_LETTER, COMPANY_RESPONSE)
EVENT_RECORD = "event_filings"
# Under the record, the day EDGAR made each letter public, read off its header:
# a release is a fact about the filing's dissemination, not a document of the
# company's, so it is recorded with the header's address and hash and the
# header itself is not stored.
RELEASES = "releases"
EVENT_DIRECTORY = "events"
# EDGAR's dissemination stamp on a filing's SGML header: the accession, then the
# day the header was made public.
RELEASE_STAMP = re.compile(
    r"<SEC-HEADER>\s*(\d{10}-\d{2}-\d{6})\.hdr\.sgml\s*:\s*(\d{4})(\d{2})(\d{2})")


def codes_of(items) -> list[str]:
    """The index's `items` field as item codes."""
    return [part.strip() for part in str(items or "").split(",") if part.strip()]


def as_index_row(stored: dict) -> dict:
    """A row of a stored index (`submissions_record`), or a store's manifest row,
    in EDGAR's own shape, so `known_at` reads it as it reads the live index: the
    Eastern stamp the store writes turned back into the universal time EDGAR
    writes, or None when none is on record."""
    stamp, raw = stored.get("acceptance_datetime"), None
    if isinstance(stamp, str) and stamp:
        try:
            instant = dt.datetime.fromisoformat(stamp)
        except ValueError:
            instant = None
        if instant is not None and instant.tzinfo is not None:
            raw = instant.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    return {"accessionNumber": stored["accession"], "filingDate": stored["filing_date"],
            "reportDate": stored.get("report_date") or "", "form": stored.get("form"),
            "items": stored.get("items") or "",
            "primaryDocument": stored.get("primary_document"),
            "primaryDocDescription": stored.get("primary_doc_description") or "",
            "acceptanceDateTime": raw}


def previous_report(rows: list[dict], filing: dict) -> dict | None:
    """The company's last 10-K or 10-Q that stood when `filing` was accepted."""
    return max((row for row in known_at(rows, filing)
                if row["form"] in PERIODIC_FORMS
                and row["accessionNumber"] != filing["accessionNumber"]),
               key=lambda row: (row["filingDate"], row["accessionNumber"]), default=None)


def years_before(day: str, years: int) -> str:
    when = dt.date.fromisoformat(day)
    try:
        return when.replace(year=when.year - years).isoformat()
    except ValueError:                      # the 29th of February
        return when.replace(year=when.year - years, day=28).isoformat()


def event_window(rows: list[dict], filing: dict) -> dict:
    """The event filings of `filing`'s window, out of index rows in EDGAR's shape.

    `previous` is the report the window opens after (None for a company with no
    earlier 10-K or 10-Q on record); `eight_ks` and `notices` the 8-Ks carrying
    an event item or an auditor change, and the late-filing notices, that stood
    at `filing` and not at `previous`; `letters` every comment letter that stood
    at `filing` by its filing date and was filed after `letters_filed_after`,
    whose release decides whether it is in the window (`public_in_window`).
    """
    known = known_at(rows, filing)
    previous = previous_report(rows, filing)
    before = ({row["accessionNumber"] for row in known_at(rows, previous)}
              if previous is not None else set())
    fresh = [row for row in known if row["accessionNumber"] not in before
             and row["accessionNumber"] != filing["accessionNumber"]]
    wanted = set(EVENT_ITEMS) | {AUDITOR_CHANGE_ITEM}
    floor = years_before(previous["filingDate"] if previous is not None
                         else filing["filingDate"], LETTER_LOOKBACK_YEARS)
    order = lambda row: (row["filingDate"], row["accessionNumber"])  # noqa: E731
    return {
        "previous": previous,
        "eight_ks": sorted((row for row in fresh if row["form"] in EVENT_8K_FORMS
                            and wanted & set(codes_of(row.get("items")))), key=order),
        "notices": sorted((row for row in fresh if row["form"] in LATE_NOTICE_FORMS),
                          key=order),
        "letters": sorted((row for row in known if row["form"] in LETTER_FORMS
                           and row["filingDate"] > floor), key=order),
        "letters_filed_after": floor,
    }


def public_in_window(released: str, previous: dict | None, filing: dict) -> bool:
    """Whether a letter made public on `released` belongs to `filing`'s window:
    public before the trigger's day (a release has no time, so the trigger's own
    day is not shown to come first) and not before the previous report's day
    (whose run, by the same rule, could not show it)."""
    return (released < filing["filingDate"]
            and (previous is None or released >= previous["filingDate"]))


def released_on(header: bytes, accession: str, filing_date: str) -> str | None:
    """The day EDGAR made a filing public, from its SGML header, or None when the
    header does not state it for this accession. Never before the filing date."""
    found = RELEASE_STAMP.search(header.decode("utf-8", "replace"))
    if found is None or found.group(1) != accession:
        return None
    try:
        day = dt.date(*(int(part) for part in found.group(2, 3, 4))).isoformat()
    except ValueError:
        return None
    return max(day, filing_date)


def letter_document(form: str, types: list[tuple[str, str]], primary) -> str | None:
    """The letter's text: EDGAR's own text copy of it, else the document typed as
    the letter, else the primary document; None when every one is a PDF."""
    kinds = ("TEXT-EXTRACT", form, "LETTER")
    for kind in kinds:
        for typed, name in types:
            if typed == kind and not name.lower().endswith(".pdf"):
                return name
    if isinstance(primary, str) and primary and not primary.lower().endswith(".pdf"):
        return primary
    return None


def fetch_event_filings(fetcher, ticker: str, cik: str, filing: dict, out: Path,
                        filings: list[dict]) -> list[str]:
    """The event filings of `filing`'s window, fetched into the store at
    `out/ticker` beside what it holds. `filings` is the index rows that stood when
    `filing` was accepted (`known_at`). A document already on record is not
    fetched again. The problems come back, an empty list when every one is held.
    """
    ticker_dir = out / ticker
    manifest = load_manifest(ticker_dir)
    documents = list(manifest.get("documents", []))
    held = {(entry.get("accession"), entry.get("role"), entry.get("url"))
            for entry in documents}
    window = event_window(filings, filing)
    previous = window["previous"]
    problems: list[str] = []

    def url_of(row: dict, name: str) -> str:
        return ARCHIVE_URL.format(cik_int=int(cik),
                                  accession=row["accessionNumber"].replace("-", ""), name=name)

    def keep(row: dict, role: str, name: str, raw: bytes | None = None,
             released: str | None = None) -> None:
        url = url_of(row, name)
        if (row["accessionNumber"], role, url) in held:
            return
        raw = fetcher.get(url) if raw is None else raw
        path, encoding = store(ticker_dir / EVENT_DIRECTORY / row["accessionNumber"] / name,
                               raw)
        entry = {"form": row["form"], "role": role, "accession": row["accessionNumber"],
                 "filing_date": row["filingDate"],
                 "acceptance_datetime": eastern_stamp(row.get("acceptanceDateTime")),
                 "report_date": row.get("reportDate") or "",
                 "items": row.get("items") or "", "url": url,
                 "path": str(path.relative_to(ticker_dir)), "stored": encoding,
                 "bytes": len(raw), "sha256": sha256(raw)}
        if released is not None:
            entry["released"] = released
        documents.append(entry)
        held.add((row["accessionNumber"], role, url))
        print(f"  {ticker} {row['form']:8s} {role:16s} {len(raw):>9,d} B  "
              f"{row['accessionNumber']}/{name}")

    for row in window["eight_ks"]:
        primary = row.get("primaryDocument")
        if not primary:
            problems.append(f"{ticker}: {row['form']} {row['accessionNumber']} names no "
                            "primary document in the index")
            continue
        keep(row, EVENT_BODY, primary)
        if AUDITOR_CHANGE_ITEM in codes_of(row.get("items")):
            for typed, name in document_types(fetcher, cik, row["accessionNumber"]):
                if typed.startswith("EX-16"):
                    keep(row, AUDITOR_LETTER, name)
    for row in window["notices"]:
        primary = row.get("primaryDocument")
        if not primary:
            problems.append(f"{ticker}: {row['form']} {row['accessionNumber']} names no "
                            "primary document in the index")
            continue
        keep(row, LATE_NOTICE, primary)
    on_record = (manifest.get(EVENT_RECORD) or {}).get(RELEASES) or {}
    releases: dict[str, dict] = {}
    for row in window["letters"]:
        name = f"{row['accessionNumber']}.hdr.sgml"
        known_release = on_record.get(row["accessionNumber"])
        if isinstance(known_release, dict) and known_release.get("released"):
            release = known_release
        else:
            url = url_of(row, name)
            raw = fetcher.get(url)
            released = released_on(raw, row["accessionNumber"], row["filingDate"])
            if released is None:
                problems.append(f"{ticker}: the header of {row['form']} "
                                f"{row['accessionNumber']} states no day it was made public")
                continue
            release = {"form": row["form"], "filing_date": row["filingDate"],
                       "released": released, "header_url": url, "header_bytes": len(raw),
                       "header_sha256": sha256(raw)}
        released = release["released"]
        if released >= filing["filingDate"]:
            continue    # not public when the trigger was accepted: not in the store
        releases[row["accessionNumber"]] = release
        if not public_in_window(released, previous, filing):
            continue
        text = letter_document(row["form"], document_types(fetcher, cik, row["accessionNumber"]),
                               row.get("primaryDocument"))
        if text is not None:        # None: EDGAR holds the letter as a PDF only
            keep(row, LETTER_ROLE[row["form"]], text, released=released)

    record = {
        "for": filing["accessionNumber"],
        "after": previous["accessionNumber"] if previous is not None else None,
        "letters_filed_after": window["letters_filed_after"],
        "letter_lookback_years": LETTER_LOOKBACK_YEARS,
        RELEASES: dict(sorted(releases.items())),
        "note": ("the 8-K bodies of items " + ", ".join(EVENT_ITEMS) + " and "
                 + AUDITOR_CHANGE_ITEM + " with its EX-16 letter, the late-filing notices, "
                 "and the comment letters made public after the report named in `after` "
                 "stood and before the filing named in `for` was accepted; a letter's "
                 "release is its header's, a letter not public by then is not held, and "
                 "only letters filed within `letter_lookback_years` of the window's "
                 "opening were looked at"),
    }
    manifest = dict(manifest, documents=sorted(
        documents, key=lambda entry: (entry["form"], entry["role"], entry.get("accession") or "",
                                      entry["path"])))
    # The record says the window is whole, so a store that fell short of it
    # carries none, and is fetched again rather than used as it is.
    manifest.pop(EVENT_RECORD, None)
    if not problems:
        manifest[EVENT_RECORD] = record
    ticker_dir.mkdir(parents=True, exist_ok=True)
    (ticker_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return problems

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
            rows = every_filing(fetcher, universe.cik(tickers[0]))
            filing = filing_for(rows, args.accession)
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
            if args.accession is not None:
                # the filing, what stood when it was accepted, companyfacts and
                # the check that the store holds nothing later, in one
                found = store_up_to(fetcher, ticker, cik, filing, out,
                                    filings=known_at(rows, filing))
            else:
                _, found = fetch_company(fetcher, ticker, cik, args.as_of, out)
        except Exception as exc:  # noqa: BLE001
            problems.append(f"{ticker}: {type(exc).__name__}: {exc}")
            continue
        for line in found:
            (changed if line.startswith(("changed:", "missing:")) else problems).append(line)

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
