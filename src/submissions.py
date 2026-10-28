"""A company's filing list, read from EDGAR when a run needs it and cut at the
run's cutoff by `filingDate`.

The second item of the build order in `docs/HEDGE_FUND_ANALYSIS.md` §5.1. The
submissions index at `data.sec.gov/submissions/CIK##########.json` lists every
filing a company made: the newest thousand or so under `filings.recent`, and the
rest on the overflow pages `filings.files` names, each holding the same parallel
arrays at its top level. A history read from the recent list alone begins
wherever that list happened to stop, so every overflow page is read too.

**The cutoff key is `filingDate`, as EDGAR gives it** (CLAUDE.md: a document's
filing date at or before the filing date of the triggering report). It is never
worked out from `acceptanceDateTime`: EDGAR dates a filing accepted after half
past five Eastern the next business day, except Forms 3, 4 and 5, which it
accepts until ten at night and dates the same day, so a date derived from the
stamp would be wrong for exactly the filings an insider reading needs. The
stamp is kept beside the date, on the Eastern clock (`fetch_fixtures.
eastern_stamp`), for the readers that time a release.

Every request goes through `edgar_client.EdgarClient`, so the rate limit and
the declared contact hold here too. The index changes as the company files, so
it is fetched fresh, not cached; the rows a run read are what its manifest
records.
"""

from __future__ import annotations

import re

from src.edgar_client import EdgarClient, EdgarError
from src.fetch_fixtures import eastern_stamp

SUBMISSIONS = "https://data.sec.gov/submissions/"
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
# an overflow page's name as the index gives it; anything else is not fetched
PAGE = re.compile(r"CIK\d{10}-submissions-\d{3}\.json")
# EDGAR's field, then the name a row carries it under
FIELDS = (("accessionNumber", "accession"),
          ("filingDate", "filing_date"),
          ("reportDate", "report_date"),
          ("form", "form"),
          ("items", "items"),
          ("primaryDocument", "primary_document"),
          ("primaryDocDescription", "primary_doc_description"),
          ("isXBRL", "is_xbrl"),
          ("isInlineXBRL", "is_inline_xbrl"),
          ("acceptanceDateTime", "acceptance_datetime"))


def index_url(cik, base: str = SUBMISSIONS) -> str:
    return f"{base}CIK{int(cik):010d}.json"


def rows_of(page: dict, where: str) -> list[dict]:
    """One page's parallel arrays as rows; a page whose arrays disagree is refused."""
    count = len(page.get("accessionNumber", []))
    for field, _ in FIELDS:
        if field in page and len(page[field]) != count:
            raise EdgarError(f"{where}: {field} lists {len(page[field])} values "
                             f"for {count} filings")
    rows = []
    for i in range(count):
        row = {name: (page[field][i] if field in page else None) for field, name in FIELDS}
        row["items"] = row["items"] or ""
        row["acceptance_datetime"] = eastern_stamp(row["acceptance_datetime"])
        rows.append(row)
    return rows


def filings(client: EdgarClient, cik, *, cutoff: str, base: str = SUBMISSIONS) -> list[dict]:
    """Every filing the company made with `filing_date <= cutoff`, newest first."""
    if not DATE.fullmatch(cutoff):
        raise EdgarError(f"a cutoff is a date, YYYY-MM-DD, not {cutoff!r}")
    url = index_url(cik, base)
    index = client.get_json(url)
    pages = [(url, index["filings"]["recent"])]
    for older in index["filings"].get("files", []):
        if not PAGE.fullmatch(older.get("name", "")):
            raise EdgarError(f"{url}: an overflow page named {older.get('name')!r}")
        pages.append((base + older["name"], client.get_json(base + older["name"])))
    seen, kept = set(), []
    for where, page in pages:
        for row in rows_of(page, where):
            if row["accession"] in seen:
                continue
            seen.add(row["accession"])
            if row["filing_date"] <= cutoff:
                kept.append(row)
    kept.sort(key=lambda row: (row["filing_date"], row["accession"]), reverse=True)
    return kept
