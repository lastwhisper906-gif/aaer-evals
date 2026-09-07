"""Fetch the fixture filings for the twelve companies from EDGAR. Read-only.

For each company, as of a fixed date, this pulls three filings:

    10-K   the latest annual report      XBRL instance + primary HTML
    10-Q   the latest quarterly report   XBRL instance + primary HTML
    8-K    the latest one carrying item 2.02, with exhibit 99.1

and stores them under `tests/fixtures/{ticker}/{form}/`, with one
`manifest.json` per company recording, for every file, the accession number,
the URL it came from, the filing date and the sha256 of the bytes as EDGAR
served them.

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
    from src import interpreter_pin
except ImportError:  # invoked as a plain script: python3.12 src/fetch_fixtures.py
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import interpreter_pin

TICKERS = ("AAPL", "STX", "CSCO", "PANW", "CARR", "LFUS",
           "GNRC", "CIEN", "QCOM", "ESE", "TTMI", "NVDA")

AS_OF = "2026-09-01"
FIXTURES = Path(__file__).resolve().parent.parent / "tests" / "fixtures"

DEFAULT_USER_AGENT = "aaer-evals research lastwhisper906@gmail.com"
TICKER_MAP_URL = "https://www.sec.gov/files/company_tickers.json"
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
                if exc.code in (429, 502, 503, 504) and attempt < 3:
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


def cik_map(fetcher: Fetcher) -> dict[str, str]:
    raw = fetcher.get_json(TICKER_MAP_URL)
    return {row["ticker"].upper(): f"{int(row['cik_str']):010d}"
            for row in raw.values()}


def recent_filings(fetcher: Fetcher, cik: str) -> list[dict]:
    """The submissions index as a list of rows, newest first."""
    data = fetcher.get_json(SUBMISSIONS_URL.format(cik=cik))
    recent = data["filings"]["recent"]
    fields = ("accessionNumber", "filingDate", "reportDate", "form", "items",
              "primaryDocument", "primaryDocDescription")
    return [{field: recent[field][i] for field in fields}
            for i in range(len(recent["form"]))]


def pick(filings: list[dict], as_of: str, form: str, item: str | None = None):
    """The latest filing of this form at or before the cutoff date."""
    matches = [f for f in filings
               if f["form"] == form and f["filingDate"] <= as_of
               and (item is None or item in (f["items"] or ""))]
    return max(matches, key=lambda f: (f["filingDate"], f["accessionNumber"]), default=None)


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
                  out: Path) -> tuple[dict, list[str]]:
    ticker_dir = out / ticker
    manifest = load_manifest(ticker_dir)
    problems = verify_existing(ticker_dir, manifest)
    if problems:
        return manifest, problems

    have = {(e["form"], e["role"]) for e in manifest.get("documents", [])}
    documents = list(manifest.get("documents", []))
    filings = recent_filings(fetcher, cik)

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
    parser.add_argument("--as-of", default=AS_OF,
                        help="cutoff date; nothing filed after it is fetched")
    parser.add_argument("--ticker", action="append", default=None,
                        help="fetch one company (repeatable); default is all twelve")
    parser.add_argument("--out", default=str(FIXTURES), help="fixture root")
    args = parser.parse_args(argv)

    tickers = tuple(t.upper() for t in args.ticker) if args.ticker else TICKERS
    out = Path(args.out)
    fetcher = Fetcher(os.environ.get("EDGAR_USER_AGENT", DEFAULT_USER_AGENT))

    try:
        ciks = cik_map(fetcher)
    except Exception as exc:  # noqa: BLE001 - the reason matters more than the type
        print(f"fetch_fixtures: could not read the EDGAR ticker map: {exc}", file=sys.stderr)
        return FETCH_FAILED

    problems, changed = [], []
    for ticker in tickers:
        cik = ciks.get(ticker)
        if cik is None:
            problems.append(f"{ticker}: not in the EDGAR ticker map")
            continue
        print(f"{ticker} (CIK {cik})")
        try:
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
