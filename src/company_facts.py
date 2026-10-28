"""A company's XBRL facts, fetched from EDGAR when a run needs them and cut at
the run's cutoff row by row.

The third item of the build order in `docs/HEDGE_FUND_ANALYSIS.md` §5.1. The
companyfacts record at `data.sec.gov/api/xbrl/companyfacts/CIK##########.json`
holds every fact a company ever filed, each row carrying the accession and the
`filed` date it came from. Fetched through `src/edgar_client.py` and cut by
`cutoff_guard.cut_catalogue` before anything reads it, it is the record as it
stood on the cutoff; nothing about it needs to be committed to be exact.

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
amendments); a row from any other form is not read. When the filing a reading
settles on states the period twice with two values, both are returned under
`conflicting` and `value` is None: Python does not pick between a filer's own
numbers.
"""

from __future__ import annotations

from src import cutoff_guard, fourth_quarter, tag_continuity
from src.edgar_client import EdgarClient

COMPANYFACTS = "https://data.sec.gov/api/xbrl/companyfacts/"
NAMESPACE = "us-gaap"
UNIT = "USD"
STATEMENT_FORMS = ("10-K", "10-Q")
DATE_BASIS = ("fetched from EDGAR on demand and cut at the cutoff row by row: each "
              "row's own `filed` date, never the record's newest")


def facts_url(cik, base: str = COMPANYFACTS) -> str:
    return f"{base}CIK{int(cik):010d}.json"


def fetch(client: EdgarClient, cik, *, cutoff, base: str = COMPANYFACTS) -> dict:
    """The companyfacts record with every row filed after the cutoff taken out."""
    cutoff_guard.parse_date(cutoff, "cutoff")    # refused before any request
    url = facts_url(cik, base)
    return cutoff_guard.cut_catalogue(client.get_json(url), cutoff, source=url)


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


def _reading(rows: list[dict], period: str) -> dict | None:
    """What one filing's rows say about the period: a value, or the conflict."""
    if not rows:
        return None
    first = rows[0]
    values = sorted({row["val"] for row in rows})
    reading = {"period": period, "accession": first["accn"], "form": first["form"],
               "filed": first["filed"], "tags": sorted({row["tag"] for row in rows})}
    if len(values) == 1:
        return dict(reading, value=values[0], tag=first["tag"], conflicting=[])
    return dict(reading, value=None, tag=None, conflicting=values)


def first_xbrl_value(document: dict, tags, period: str, *, unit: str = UNIT) -> dict | None:
    """The value the earliest filing stated for the period, under any name in `tags`."""
    rows = statement_rows(document, tags, period, unit=unit)
    if not rows:
        return None
    earliest = min((row["filed"], row["accn"]) for row in rows)
    return _reading([row for row in rows if (row["filed"], row["accn"]) == earliest], period)


def as_of_cutoff_value(document: dict, tags, period: str, *, unit: str = UNIT) -> dict | None:
    """The value the latest filing in the cut record stated for the period."""
    rows = statement_rows(document, tags, period, unit=unit)
    if not rows:
        return None
    latest = max((row["filed"], row["accn"]) for row in rows)
    return _reading([row for row in rows if (row["filed"], row["accn"]) == latest], period)


def fourth_quarters(ticker: str, document: dict, cutoff, *, url: str | None = None,
                    years=fourth_quarter.YEARS_REQUESTED) -> dict:
    """`src/fourth_quarter.py` over a record fetched on demand."""
    return fourth_quarter.from_document(
        ticker, document, cutoff, years=years,
        source={"path": None, "url": url, "date_basis": DATE_BASIS})
