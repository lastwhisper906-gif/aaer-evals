"""A company's XBRL facts, fetched from EDGAR when a run needs them and cut at
the run's cutoff row by row.

The third item of the build order in `docs/HEDGE_FUND_ANALYSIS.md` §5.1. The
companyfacts record at `data.sec.gov/api/xbrl/companyfacts/CIK##########.json`
holds every fact a company ever filed, each row carrying the accession and the
`filed` date it came from. Fetched through `src/edgar_client.py` and cut by
`cutoff_guard.cut_catalogue` before anything reads it, it holds the rows filed
on or before the cutoff and nothing else; the one thing EDGAR assigns across
filings, a row's calendar `frame`, is taken off. The record is not committed;
it carries the URL and the hash of the bytes it was cut from (`read_from`), and
the run that reads it records them.

Three readings of one period, over the chain of names a company reported a
series under (`tag_continuity.tags_of`: Apple's top line is `SalesRevenueNet`,
then `Revenues`, then `RevenueFromContractWithCustomerExcludingAssessedTax`):

* **`first_xbrl_value`** — the value the earliest filing stated, under any name
  in the chain. CLAUDE.md's ground truth is the first-reported value; a later
  filing's comparative column restates the period under the name of its own
  day, and reading that instead would date the number by the wrong filing.
* **`as_of_cutoff_value`** — the value the latest filing at or before the cutoff
  stated, `docs/INPUT_SPEC.md` §1's rule for a period reported more than once.
  The two differ exactly when the company revised the number.
* **The fourth quarter**, which a company never tags on its own: the year less
  the nine months, by `src/fourth_quarter.py` over the same cut record.

Numeric facts come from the periodic statements (§1: 10-K, 10-Q and their
amendments); a row from any other form is not read. Both readings take the
cutoff and refuse a row filed after it, so an uncut record cannot be read
through them. When the filings a reading settles on (one filing, or one day's
filings when their acceptance order is not known) state the period at two
values, every one is returned under `conflicting` and `value` is None: Python
does not pick between a filer's own numbers.
"""

from __future__ import annotations

import datetime as dt
import json

from src import cutoff_guard, fourth_quarter, tag_continuity
from src.edgar_client import EdgarClient, EdgarError, sha256

COMPANYFACTS = "https://data.sec.gov/api/xbrl/companyfacts/"
NAMESPACE = "us-gaap"
UNIT = "USD"
STATEMENT_FORMS = ("10-K", "10-Q")
DATE_BASIS = ("fetched from EDGAR on demand and cut at the cutoff row by row: each "
              "row's own `filed` date, never the record's newest")


def facts_url(cik, base: str = COMPANYFACTS) -> str:
    return f"{base}CIK{int(cik):010d}.json"


def fetch(client: EdgarClient, cik, *, cutoff, base: str = COMPANYFACTS) -> dict:
    """The companyfacts record with every row filed after the cutoff taken out.

    The record carries `read_from`: the URL, and the sha256 and length of the
    bytes EDGAR served, for the run that read it to put in its manifest.
    """
    limit = cutoff_guard.parse_date(cutoff, "cutoff")    # refused before any request
    url = facts_url(cik, base)
    body = client.get(url)
    try:
        document = json.loads(body)
    except ValueError:
        raise EdgarError(f"{url}: the answer is not JSON") from None
    return dict(cutoff_guard.cut_catalogue(document, limit, source=url),
                read_from={"url": url, "sha256": sha256(body), "bytes": len(body),
                           "cutoff": limit.isoformat()})


def chain(ticker: str, series: str) -> tuple[str, ...]:
    """Every name the company reported one series under, oldest first."""
    return tag_continuity.tags_of(ticker, series)


def period_of(row: dict) -> str:
    """A row's period as a fact id spells it: `start..end`, or the instant alone."""
    return f"{row['start']}..{row['end']}" if row.get("start") else row["end"]


def statement_rows(document: dict, tags, period: str, *, unit: str = UNIT,
                   namespace: str = NAMESPACE) -> list[dict]:
    """Every periodic-statement row for one period under any name in `tags`.

    A name may carry its namespace (`us-gaap:Revenues`, as the tag map writes
    it) or not, in which case it is read in `namespace`.
    """
    found = []
    facts = document.get("facts") or {}
    for tag in tags:
        prefix, _, name = tag.rpartition(":")
        concept = facts.get(prefix or namespace, {}).get(name) or {}
        for row in concept.get("units", {}).get(unit, []):
            if str(row.get("form") or "").startswith(STATEMENT_FORMS) \
                    and period_of(row) == period:
                found.append(dict(row, tag=tag))
    return found


def _moment(stamp: str):
    return dt.datetime.fromisoformat(stamp)


def _settle(rows: list[dict], period: str, which, cutoff: dt.date,
            accepted: dict | None) -> dict | None:
    """What the first (`which=min`) or last (`which=max`) filing day says.

    The cutoff is a date, so every filing made on one day is equally inside it,
    and the accession number is not the order filings were made in. Within the
    day the filings are ordered by their acceptance stamps when `accepted`
    (accession to the Eastern stamp `src/submissions.py` gives) holds one for
    each; otherwise the day stands whole. Either way, filings that disagree are
    a conflict: `value` is None and every filing's number is listed.
    """
    late = sorted({row["accn"] for row in rows
                   if cutoff_guard.parse_date(row.get("filed"), "filed") > cutoff})
    if late:
        raise cutoff_guard.CutoffGuardError(
            f"{period}: {', '.join(late)} filed after the cutoff {cutoff.isoformat()} "
            "reached the reader; a record is read only once cut at the cutoff")
    if not rows:
        return None
    day = which(row["filed"] for row in rows)
    rows = [row for row in rows if row["filed"] == day]
    stamps = {row["accn"]: (accepted or {}).get(row["accn"]) for row in rows}
    if accepted is not None and all(stamps.values()):
        moment = which(_moment(stamp) for stamp in stamps.values())
        rows = [row for row in rows if _moment(stamps[row["accn"]]) == moment]
    accessions = sorted({row["accn"] for row in rows})
    forms = sorted({row["form"] for row in rows})
    tags = sorted({row["tag"] for row in rows})
    values = sorted({row["val"] for row in rows})
    reading = {"period": period, "filed": day, "accessions": accessions,
               "accession": accessions[0] if len(accessions) == 1 else None,
               "form": forms[0] if len(forms) == 1 else None,
               "tags": tags, "tag": tags[0] if len(tags) == 1 else None}
    if len(values) == 1:
        return dict(reading, value=values[0], conflicting=[])
    return dict(reading, value=None, conflicting=sorted(
        ({"accession": row["accn"], "form": row["form"], "tag": row["tag"],
          "value": row["val"]} for row in rows),
        key=lambda found: (found["accession"], found["tag"], found["value"])))


def first_xbrl_value(document: dict, tags, period: str, *, cutoff, unit: str = UNIT,
                     accepted: dict | None = None) -> dict | None:
    """The value the earliest filing stated for the period, under any name in `tags`."""
    return _settle(statement_rows(document, tags, period, unit=unit), period, min,
                   cutoff_guard.parse_date(cutoff, "cutoff"), accepted)


def as_of_cutoff_value(document: dict, tags, period: str, *, cutoff, unit: str = UNIT,
                       accepted: dict | None = None) -> dict | None:
    """The value the latest filing at or before the cutoff stated for the period."""
    return _settle(statement_rows(document, tags, period, unit=unit), period, max,
                   cutoff_guard.parse_date(cutoff, "cutoff"), accepted)


def fourth_quarters(ticker: str, document: dict, cutoff, *, url: str | None = None,
                    years=fourth_quarter.YEARS_REQUESTED) -> dict:
    """`src/fourth_quarter.py` over a record fetched on demand."""
    return fourth_quarter.from_document(
        ticker, document, cutoff, years=years,
        source={"path": None, "url": url, "date_basis": DATE_BASIS})
