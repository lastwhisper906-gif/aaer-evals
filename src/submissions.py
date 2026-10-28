"""A company's filing list, read from EDGAR when a run needs it and cut at the
run's cutoff by `filingDate`.

The second item of the build order in `docs/HEDGE_FUND_ANALYSIS.md` §5.1. The
submissions index at `data.sec.gov/submissions/CIK##########.json` lists every
filing a company made: the newest thousand or so under `filings.recent`, and the
rest on the overflow pages `filings.files` names, each holding the same parallel
arrays at its top level. A history read from the recent list alone begins
wherever that list happened to stop, so every overflow page is read too.

**The cutoff key is `filingDate`, as EDGAR gives it** (CLAUDE.md: a document's
filing date at or before the filing date of the triggering report). Each row's
date is parsed (`cutoff_guard.parse_date`), never compared as a string: a blank
date would sort before every cutoff. The rule is a date, so a filing made later
on the trigger's own day is inside it (Apple's Form 4 accepted at 21:30 Eastern
on 2020-04-30, five hours after that day's earnings release, is dated the 30th);
a reader that times events within the day cuts on the acceptance stamp. It is never
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

import datetime as dt
import re

from src import cutoff_guard
from src.edgar_client import EdgarClient, EdgarError
from src.fetch_fixtures import eastern_stamp

SUBMISSIONS = "https://data.sec.gov/submissions/"
DATE = re.compile(r"\d{4}-\d{2}-\d{2}", re.ASCII)
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
    """One page's parallel arrays as rows.

    Refused: a page with no accession or filing-date array (an error answer, an
    empty object), arrays whose lengths disagree, and a row whose filing date is
    absent or not a date, which is neither early nor late and so is not let
    past a cutoff.
    """
    if not isinstance(page, dict) or not isinstance(page.get("accessionNumber"), list) \
            or not isinstance(page.get("filingDate"), list):
        raise EdgarError(f"{where}: no accessionNumber and filingDate arrays")
    count = len(page["accessionNumber"])
    for field, _ in FIELDS:
        if field in page and len(page[field]) != count:
            raise EdgarError(f"{where}: {field} lists {len(page[field])} values "
                             f"for {count} filings")
    rows = []
    for i in range(count):
        row = {name: (page[field][i] if field in page else None) for field, name in FIELDS}
        row["filing_date"] = cutoff_guard.parse_date(
            row["filing_date"], f"{where} {row['accession']} filingDate").isoformat()
        row["items"] = row["items"] or ""
        row["acceptance_datetime"] = eastern_stamp(row["acceptance_datetime"])
        rows.append(row)
    return rows


def filings(client: EdgarClient, cik, *, cutoff, base: str = SUBMISSIONS) -> list[dict]:
    """Every filing the company made with `filing_date <= cutoff`, newest first."""
    if not DATE.fullmatch(str(cutoff)):
        raise EdgarError(f"a cutoff is a date, YYYY-MM-DD, not {cutoff!r}")
    try:
        limit = cutoff_guard.parse_date(cutoff, "cutoff")
    except cutoff_guard.CutoffGuardError:
        raise EdgarError(f"a cutoff is a date, YYYY-MM-DD, not {cutoff!r}") from None
    url = index_url(cik, base)
    index = client.get_json(url)
    pages = [(url, index["filings"]["recent"], None)]
    page_name = re.compile(rf"CIK{int(cik):010d}-submissions-\d{{3}}\.json", re.ASCII)
    for older in index["filings"].get("files", []):
        if not page_name.fullmatch(str(older.get("name", ""))):
            raise EdgarError(f"{url}: an overflow page named {older.get('name')!r}, "
                             "not one of this company's")
        pages.append((base + older["name"], client.get_json(base + older["name"]),
                      older.get("filingCount")))
    seen, kept = set(), []
    for where, page, promised in pages:
        rows = rows_of(page, where)
        if promised is not None and len(rows) != promised:
            raise EdgarError(f"{where}: {len(rows)} filings where the index promises "
                             f"{promised}")
        for row in rows:
            if row["accession"] in seen:
                continue
            seen.add(row["accession"])
            if dt.date.fromisoformat(row["filing_date"]) <= limit:
                kept.append(row)
    kept.sort(key=lambda row: (row["filing_date"], row["accession"]), reverse=True)
    return kept
