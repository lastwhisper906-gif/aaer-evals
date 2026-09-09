"""The trend table. Python does every division on this page.

The input is the companyfacts history — `tests/fixtures/{ticker}/companyfacts.json`,
stored gzipped, every standard-taxonomy fact the company has ever filed, each
row carrying the accession and the filing date that reported it — and, for what
companyfacts has not loaded, the XBRL instances of the filings this run reads.
One request per company covers 8 quarters and 5 years, which is what
`docs/INPUT_SPEC.md` §5 asks the table to span; a single instance carries three
years and two quarters and no more.

Each ratio carries its formula, and behind every term the fact id, the tag, the
value, the accession that filed it and which of the two records it came from,
so a reader can look the number up in the file it names. Nothing here is
rounded, smoothed, interpolated or carried forward.

**Periods are calendar frames.** `CY2025Q3` is the third calendar quarter of
2025, and a company's fiscal quarter is placed in the frame its own middle day
falls in — Apple's quarter ending 2026-06-27 is `CY2026Q2`, Cisco's ending
2026-04-25 is `CY2026Q1`. `docs/INPUT_SPEC.md` §1 requires it: fiscal years
differ, so any comparison across companies uses the calendar frame and never the
company's own quarter label. `Q-0` and `FY-0` stay as the row's position in the
window — the reader's "this quarter, one back, two back" — and the frame beside
it is what a comparer joins on.

A frame holds one period. When two fiscal periods claim one frame the newer
keeps it and the older takes the frame before it, and the row says so in
`frame_shifted_from`. That is not a tidy-up: Seagate's fiscal year ends within a
day or two of 1 July, so its middle day lands on either side of New Year
depending on whether the year ran 52 or 53 weeks, and two consecutive fiscal
years genuinely compute the same frame. Stepping the older one back is what
keeps the five annual rows five consecutive fiscal years, which is what
year-over-year then subtracts.

**What is left out is named, not dropped.** Every one of the 8 + 5 requested
frames is in `coverage` either filled or with the reason it is not, and the
reason carries the frame's own calendar dates and says where the frame sits
against the record. Two of the eight quarters requested are usually a company's
fourth fiscal quarter, which is reported only inside the annual figure — the
reason names the annual period that covers the frame, and deriving the quarter
from it is a separate piece of work, not this one.

The non-GAAP gap is missing for a different reason and says so: no `us-gaap`
concept carries a non-GAAP measure, so neither record can hold one. It comes off
the 8-K exhibit, which is a different file.

**The rules that decide which fact is the fact**, all of them mechanical:
consolidated only (a fact with a segment of either kind is a slice, not the
company — companyfacts holds entity-wide values only and satisfies this by
construction); a fact a later filing superseded is skipped; the latest filing at
or before the cutoff wins, and where two records hold the same filing's fact the
companyfacts row is the one named, because it is the record this table is built
from; a duration of 80–100 days is a quarter and one of 350–380 days is a year;
a balance-sheet instant belongs to the period whose end date it equals exactly;
and every term is a plain amount in dollars, because every ratio here divides
one money figure by another.

    python3.12 -m src.extract_numbers --ticker AAPL --out input_numbers.json
    python3.12 -m src.trends --numbers input_numbers.json --out input_trends.json
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

try:
    from src import (cutoff_guard, fetch_companyfacts, fetch_fixtures,
                     interpreter_pin)
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import (cutoff_guard, fetch_companyfacts, fetch_fixtures,
                     interpreter_pin)

BAD_INPUT = 2

QUARTERS_REQUESTED = 8
YEARS_REQUESTED = 5
QUARTER_DAYS = (80, 100)
YEAR_DAYS = (350, 380)

# Every term of every ratio is a money amount. A ratio reads a fact stated in
# dollars and nothing else -- a tag reported in shares, or per share, is a
# different measurement. The two records write the same unit differently, so
# `money` below reads both.
MONEY = "USD"

# Which record a fact came from. A companyfacts row is the history; an instance
# fact is the filing's own XBRL, which is what fills a period companyfacts has
# not loaded.
HISTORY = "companyfacts"
INSTANCE = "xbrl_instance"

FRAME = re.compile(r"^CY(?P<year>[0-9]{4})(?:Q(?P<quarter>[1-4]))?$")

# Which us-gaap tags may stand for each term, best first. A term is filled by
# the first tag in the list that the record actually carries; the output names
# which one it was, so a reader can see that Apple's revenue came from
# `RevenueFromContractWithCustomerExcludingAssessedTax` and Generac's did not.
CONCEPTS: dict[str, tuple[str, tuple[str, ...]]] = {
    "revenue": ("duration", (
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "RevenueFromContractWithCustomerIncludingAssessedTax",
        "Revenues", "SalesRevenueNet", "SalesRevenueGoodsNet")),
    "cost_of_revenue": ("duration", (
        "CostOfRevenue", "CostOfGoodsAndServicesSold", "CostOfGoodsSold",
        "CostOfServices", "CostOfSales")),
    "net_income": ("duration", ("NetIncomeLoss", "ProfitLoss")),
    "operating_cash_flow": ("duration", (
        "NetCashProvidedByUsedInOperatingActivities",
        "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations")),
    "receivables": ("instant", (
        "AccountsReceivableNetCurrent", "ReceivablesNetCurrent",
        "AccountsReceivableNet")),
    "bad_debt_allowance": ("instant", (
        "AccountsReceivableAllowanceForCreditLossCurrent",
        "AllowanceForDoubtfulAccountsReceivableCurrent",
        "AllowanceForDoubtfulAccountsReceivable")),
    "inventory": ("instant", ("InventoryNet",)),
    "inventory_reserve": ("instant", ("InventoryValuationReserves",)),
    "warranty_accrual": ("instant", (
        "StandardProductWarrantyAccrual", "ProductWarrantyAccrual",
        "StandardProductWarrantyAccrualCurrent")),
    "assets": ("instant", ("Assets",)),
    "property_plant_and_equipment": ("instant", (
        "PropertyPlantAndEquipmentNet",
        # Ciena's balance sheet line is property, plant and equipment together
        # with its finance-lease right-of-use assets, and that is the tag.
        "PropertyPlantAndEquipmentAndFinanceLeaseRightOfUseAssetAfter"
        "AccumulatedDepreciationAndAmortization")),
    "cash": ("instant", (
        "CashAndCashEquivalentsAtCarryingValue",
        "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents")),
    "contract_liabilities": ("instant", (
        "ContractWithCustomerLiabilityCurrent", "ContractWithCustomerLiability",
        "DeferredRevenueCurrent", "DeferredRevenue")),
    # Never present: no non-GAAP measure is a us-gaap concept. Kept in the
    # table so the gap is reported as missing rather than forgotten.
    "non_gaap_net_income": ("duration", ()),
}

# docs/INPUT_SPEC.md §5 item 1, in the order the spec lists them.
RATIOS: dict[str, dict] = {
    "receivables_over_revenue": {
        "terms": ("receivables", "revenue"),
        "formula": "receivables / revenue",
        "value": lambda v, days: v["receivables"] / v["revenue"],
    },
    "days_sales_outstanding": {
        "terms": ("receivables", "revenue"),
        "formula": "receivables / revenue * days_in_period",
        "value": lambda v, days: v["receivables"] / v["revenue"] * days,
    },
    "days_sales_of_inventory": {
        "terms": ("inventory", "cost_of_revenue"),
        "formula": "inventory / cost_of_revenue * days_in_period",
        "value": lambda v, days: v["inventory"] / v["cost_of_revenue"] * days,
    },
    "accruals_over_total_assets": {
        "terms": ("net_income", "operating_cash_flow", "assets"),
        "formula": "(net_income - operating_cash_flow) / assets",
        "value": lambda v, days: (v["net_income"] - v["operating_cash_flow"]) / v["assets"],
    },
    "gross_margin": {
        "terms": ("revenue", "cost_of_revenue"),
        "formula": "(revenue - cost_of_revenue) / revenue",
        "value": lambda v, days: (v["revenue"] - v["cost_of_revenue"]) / v["revenue"],
    },
    # Gross receivables are almost never tagged; net receivables and the
    # allowance almost always are, and gross is their sum by definition. That
    # is arithmetic on two facts, which is this file's job.
    "bad_debt_reserve_ratio": {
        "terms": ("bad_debt_allowance", "receivables"),
        "formula": "bad_debt_allowance / (receivables + bad_debt_allowance)",
        "value": lambda v, days: v["bad_debt_allowance"]
        / (v["receivables"] + v["bad_debt_allowance"]),
    },
    "inventory_reserve_ratio": {
        "terms": ("inventory_reserve", "inventory"),
        "formula": "inventory_reserve / inventory",
        "value": lambda v, days: v["inventory_reserve"] / v["inventory"],
    },
    "warranty_reserve_ratio": {
        "terms": ("warranty_accrual", "revenue"),
        "formula": "warranty_accrual / revenue",
        "value": lambda v, days: v["warranty_accrual"] / v["revenue"],
    },
    "soft_asset_share": {
        "terms": ("assets", "property_plant_and_equipment", "cash"),
        "formula": "(assets - property_plant_and_equipment - cash) / assets",
        "value": lambda v, days: (v["assets"] - v["property_plant_and_equipment"]
                                  - v["cash"]) / v["assets"],
    },
    "contract_liabilities_over_revenue": {
        "terms": ("contract_liabilities", "revenue"),
        "formula": "contract_liabilities / revenue",
        "value": lambda v, days: v["contract_liabilities"] / v["revenue"],
    },
    "non_gaap_gap": {
        "terms": ("non_gaap_net_income", "net_income"),
        "formula": "(non_gaap_net_income - net_income) / abs(net_income)",
        "value": lambda v, days: (v["non_gaap_net_income"] - v["net_income"])
        / abs(v["net_income"]),
    },
}

# What each ratio divides by, written out, for the one reason a fact can be
# present and still unusable.
DENOMINATORS: dict[str, tuple[str, object]] = {
    "receivables_over_revenue": ("revenue", lambda v: v["revenue"]),
    "days_sales_outstanding": ("revenue", lambda v: v["revenue"]),
    "days_sales_of_inventory": ("cost_of_revenue", lambda v: v["cost_of_revenue"]),
    "accruals_over_total_assets": ("assets", lambda v: v["assets"]),
    "gross_margin": ("revenue", lambda v: v["revenue"]),
    "bad_debt_reserve_ratio": ("receivables + bad_debt_allowance",
                               lambda v: v["receivables"] + v["bad_debt_allowance"]),
    "inventory_reserve_ratio": ("inventory", lambda v: v["inventory"]),
    "warranty_reserve_ratio": ("revenue", lambda v: v["revenue"]),
    "soft_asset_share": ("assets", lambda v: v["assets"]),
    "contract_liabilities_over_revenue": ("revenue", lambda v: v["revenue"]),
    "non_gaap_gap": ("net_income", lambda v: v["net_income"]),
}

NO_NON_GAAP = ("no us-gaap concept carries a non-GAAP measure, and neither "
               "companyfacts nor an XBRL instance holds anything but us-gaap "
               "and dei facts")


class TrendInputError(Exception):
    """The numbers file is not the shape this reads."""


def _date(value: str) -> dt.date:
    return dt.date.fromisoformat(value)


# --- calendar frames ---------------------------------------------------------

def frame_of(start: str, end: str, kind: str) -> str:
    """The calendar frame a fiscal period falls in, by its own middle day.

    A period runs from `start` to `end` inclusive; its middle day is the one
    halfway along, and where the period has an even number of days the later of
    the two middle days is taken. The frame is the calendar quarter or calendar
    year that day belongs to. Apple's 2026-03-29..2026-06-27 gives 2026-05-13
    and so `CY2026Q2`; its 2024-09-29..2025-09-27 gives 2025-03-30 and so
    `CY2025`.

    This is EDGAR's own answer wherever EDGAR gives one — companyfacts stamps a
    `frame` on the row it treats as canonical for a frame, and
    `test_the_frame_rule_agrees_with_the_frames_edgar_stamped` checks the rule
    against every stamp in the window. EDGAR stamps far from every period,
    though: Ciena's quarter ending 2025-08-02 carries no stamp at all, and a
    table that skipped it would be reporting six quarters and calling it eight.
    """
    span = (_date(end) - _date(start)).days
    middle = _date(start) + dt.timedelta(days=(span + 1) // 2)
    if kind == "quarter":
        return f"CY{middle.year}Q{(middle.month - 1) // 3 + 1}"
    return f"CY{middle.year}"


def frame_bounds(frame: str) -> tuple[dt.date, dt.date]:
    """The calendar dates a frame covers, first day and last day."""
    match = FRAME.match(frame)
    if match is None:
        raise TrendInputError(f"{frame!r} is not a calendar frame")
    year = int(match.group("year"))
    if match.group("quarter") is None:
        return dt.date(year, 1, 1), dt.date(year, 12, 31)
    quarter = int(match.group("quarter"))
    start = dt.date(year, quarter * 3 - 2, 1)
    end_month, end_year = quarter * 3 + 1, year
    if end_month > 12:
        end_month, end_year = 1, year + 1
    return start, dt.date(end_year, end_month, 1) - dt.timedelta(days=1)


def step_back(frame: str, count: int) -> str:
    """The frame `count` periods earlier. `CY2025Q1` back one is `CY2024Q4`."""
    match = FRAME.match(frame)
    if match is None:
        raise TrendInputError(f"{frame!r} is not a calendar frame")
    year = int(match.group("year"))
    if match.group("quarter") is None:
        return f"CY{year - count}"
    index = year * 4 + int(match.group("quarter")) - 1 - count
    return f"CY{index // 4}Q{index % 4 + 1}"


# --- the two records ---------------------------------------------------------

def usable(fact: dict) -> bool:
    """Consolidated, reported, still current, and a number.

    Consolidated means no dimension of either kind. A typed member is a
    dimension: NVIDIA's cash equivalents broken out by
    `StatementOfFinancialPositionLocationBalanceAxis`, and Ciena's amortized
    cost split between cash equivalents, short-term investments and non-current
    marketable securities, carry an empty `segment` and are not totals. Every
    companyfacts row passes this: the history holds the entity-wide value alone.
    """
    if fact.get("nil") or fact.get("number") is None:
        return False
    if fact.get("superseded_by"):
        return False
    context = fact.get("context") or {}
    return not context.get("segment") and not context.get("typed_segment")


def _history_fact(tag: str, unit: str, row: dict) -> dict:
    """One companyfacts row in the shape `src/extract_numbers.py` writes a fact.

    One shape means one lookup, one consolidated-only rule and one
    point-in-time rule serve both records. A companyfacts row states no
    `decimals`: it is EDGAR's own deduplication of a filing's cells and keeps
    the precisely stated one.
    """
    start, end = row.get("start"), row["end"]
    context = {"start": start, "end": end} if start else {"instant": end}
    context["segment"] = []
    period = f"{start}..{end}" if start else end
    return {
        "id": f"{row['accn']}:{HISTORY}:{tag}:{unit}:{period}",
        "tag": tag,
        "prefix": "us-gaap",
        "context": context,
        "unit": unit,
        "decimals": None,
        "value": str(row["val"]),
        "number": float(row["val"]),
        "nil": False,
        "form": row.get("form", ""),
        "source_accession": row["accn"],
        "filing_date": row["filed"],
        "record": HISTORY,
    }


def history_facts(record: dict, cutoff: dt.date | None) -> list[dict]:
    """Every companyfacts row filed at or before the cutoff, as a fact.

    Every unit, not only dollars. A ratio reads dollars alone, but a period is
    on record when the record holds any duration of that length: ESCO's July to
    September 2024 quarter is in companyfacts as one share-repurchase count and
    nothing else, and a table that dropped the period would be saying the
    record does not hold it.
    """
    return [_history_fact(tag, unit, row)
            for tag, concept in sorted((record.get("facts") or {})
                                       .get("us-gaap", {}).items())
            for unit, rows in sorted(concept.get("units", {}).items())
            for row in rows
            if cutoff is None or _date(row["filed"]) <= cutoff]


def read_history(ticker: str, fixtures_root) -> dict:
    """The companyfacts document on record for one company.

    Which file, and how it is stored, comes from the fixture manifest through
    `cutoff_guard.document_record`, so a file nobody recorded is refused here
    exactly as it is anywhere else. The bytes are then read with
    `fetch_fixtures.read_stored` -- the reader the fetcher itself verifies
    fixtures with -- and checked against the sha256 the manifest holds, so a
    document that is no longer the one that was fetched fails rather than being
    used.

    **The date gate is not the gate for this document, and it cannot be.**
    companyfacts is a catalogue of facts drawn from many filings and is not
    itself a filing: the fixture manifest says exactly that in the row's own
    `date_basis`, and the date it records is the newest filing the catalogue
    carries. `cutoff_guard.load_index` already makes this exception for the
    submissions index and states the rule that comes with it -- the look-ahead
    lives in the rows, and the caller drops them. That is `history_facts`, and
    `test_no_fact_filed_after_the_cutoff_reaches_a_cell` and
    `test_an_earlier_cutoff_takes_the_later_filings_back_out` are what hold it.

    One consequence is worth stating rather than leaving to be discovered: a
    read through `cutoff_guard.load_bytes` is what puts a document into a
    bundle's `documents_used` list, and this read is not one, so a bundle does
    not yet list the catalogue it read. Listing it needs the same exception by
    role that `assemble_bundle.INDEX_ROLE` already makes for the submissions
    index, in `assemble_bundle.documents_used` and in
    `extraction_checks.check_cutoff`, and `docs/INPUT_SPEC.md` §6 names the file
    it would carry, `input_companyfacts.json`. That is the bundle's piece of
    work and not this one.
    """
    rows = cutoff_guard.documents(ticker, form=fetch_companyfacts.FORM,
                                  role=fetch_companyfacts.ROLE,
                                  fixtures_root=fixtures_root)
    if len(rows) != 1:
        raise cutoff_guard.CutoffGuardError(
            f"{ticker}: {len(rows)} companyfacts documents on record, expected one")
    row = cutoff_guard.document_record(rows[0]["full_path"], fixtures_root=fixtures_root)
    raw = fetch_fixtures.read_stored(rows[0]["full_path"], row["stored"])
    if fetch_fixtures.sha256(raw) != row["sha256"]:
        raise cutoff_guard.CutoffGuardError(
            f"{ticker}: {row['path']} is no longer the bytes the manifest hashed")
    record = json.loads(raw.decode("utf-8"))
    record["path"] = row["path"]
    return record


def money(fact: dict) -> bool:
    """A plain amount in dollars — the only kind of fact a ratio here reads.

    An instance writes the unit `iso4217:USD`, companyfacts writes `USD`, and a
    per-share or product unit writes a divide or a product that is neither.
    """
    unit = str(fact.get("unit") or "")
    return "/" not in unit and "*" not in unit and unit.rsplit(":", 1)[-1] == MONEY


def _precision(fact: dict) -> float:
    """How precisely the filing stated this number.

    XBRL `decimals` is a power of ten: `-6` means the value is accurate to the
    million, `-8` to the hundred million, `INF` exactly. Larger is more precise.
    A fact with no `decimals` claims nothing and loses to one that does.
    """
    decimals = fact.get("decimals")
    if decimals is None:
        return float("-inf")
    text = str(decimals).strip()
    if text.upper() == "INF":
        return float("inf")
    try:
        return float(text)
    except ValueError:
        return float("-inf")


def pick_fact(facts: list[dict], term: str, period: dict) -> dict | None:
    """The one fact behind a term for one period, by the rules in the docstring."""
    period_type, tags = CONCEPTS[term]
    for tag in tags:
        matches = []
        for fact in facts:
            if fact["tag"] != tag or fact["prefix"] != "us-gaap" \
                    or not usable(fact) or not money(fact):
                continue
            context = fact["context"]
            if period_type == "duration":
                if context.get("start") == period["start"] and \
                        context.get("end") == period["end"]:
                    matches.append(fact)
            elif context.get("instant") == period["end"]:
                matches.append(fact)
        if matches:
            # The latest filing wins — the point-in-time rule. Where one filing
            # is in both records the companyfacts row is named, because that is
            # the record this table is built from and the instance is only what
            # fills what the history has not loaded.
            #
            # Within one filing and one record the more precisely stated cell
            # wins. Breaking that tie on the id string picked by accident:
            # Cisco's 10-Q holds `AccountsReceivableNetCurrent` twice, `f-36` at
            # 6,480,000,000 and decimals −6, the balance-sheet cell, and `f-525`
            # at 6,500,000,000 and decimals −8, the narrative sentence "Accounts
            # receivable, net was $6.5 billion". `"f-525" > "f-36"` as a string,
            # so the rounded sentence won and days-sales-outstanding was
            # published as 37.3398 where the balance sheet gives 37.2249.
            matches.sort(key=lambda f: (f["filing_date"], f["source_accession"],
                                        f.get("record") == HISTORY,
                                        _precision(f), f["id"]))
            return matches[-1]
    return None


def _in_period(fact: dict, period: dict) -> bool:
    context = fact.get("context") or {}
    return (context.get("start"), context.get("end")) == (period["start"], period["end"]) \
        or context.get("instant") == period["end"]


def why_missing(facts: list[dict], term: str, period: dict) -> str:
    """Which of the four ways this term is not here — the reader's next step
    differs for each: a tag nobody filed, a tag never filed as a total, a tag
    filed as a total elsewhere but only by segment here, or a tag filed for
    other periods only."""
    tags = CONCEPTS[term][1]
    if not tags:
        return f"no fact for {term}: {NO_NON_GAAP}"
    named = ", ".join(f"us-gaap:{tag}" for tag in tags)
    span = f"{period['start']}..{period['end']}"
    # Money only, the same rule `pick_fact` reads by, so every branch below is
    # a true sentence about the facts a ratio could have used.
    anywhere = [fact for fact in facts
                if fact["tag"] in tags and fact["prefix"] == "us-gaap" and money(fact)]
    if not anywhere:
        return (f"no fact for {term}: neither record tags any of {named} "
                f"as an amount in {MONEY}")
    if not any(usable(fact) for fact in anywhere):
        return (f"no fact for {term}: {named} is reported only by segment, or nil, "
                f"or superseded — never as a consolidated total")
    here = [fact for fact in anywhere if _in_period(fact, period)]
    if here:
        return (f"no fact for {term} in {span}: {named} is a consolidated total in "
                f"other periods, but in this one it is reported only by segment, "
                f"or nil, or superseded")
    return (f"no fact for {term} in {span}: "
            f"{named} is reported, but not for this period")


def ratio(facts: list[dict], name: str, period: dict) -> dict:
    """One ratio for one period: a value with its inputs, or a reason."""
    spec = RATIOS[name]
    inputs, values = {}, {}
    for term in spec["terms"]:
        fact = pick_fact(facts, term, period) if CONCEPTS[term][1] else None
        if fact is None:
            return {"missing": why_missing(facts, term, period)}
        inputs[term] = {"fact_id": fact["id"], "tag": fact["tag"],
                        "value": fact["number"], "unit": fact["unit"],
                        "decimals": fact.get("decimals"),
                        "accession": fact["source_accession"],
                        "filed": fact["filing_date"],
                        "record": fact.get("record", INSTANCE)}
        values[term] = fact["number"]
    written, of = DENOMINATORS[name]
    if of(values) == 0:
        return {"missing": f"{written} is zero in {period['start']}..{period['end']}"}
    return {"value": spec["value"](values, period["days"]),
            "formula": spec["formula"], "inputs": inputs}


# --- the periods the record holds, and the window over them ------------------

def periods(facts: list[dict], kind: str) -> list[dict]:
    """Every distinct period of the requested length, newest first.

    One period per end date. A filer that wrote one fiscal period with two start
    dates reported one period — TTM Technologies' 2025 year is `2024-12-31` on
    133 rows and `2024-12-30` on one — and the start the most rows carry is the
    one it reported.
    """
    low, high = QUARTER_DAYS if kind == "quarter" else YEAR_DAYS
    starts: dict[str, Counter] = defaultdict(Counter)
    for fact in facts:
        if not usable(fact):
            continue
        context = fact["context"]
        start, end = context.get("start"), context.get("end")
        if not start or not end:
            continue
        days = (_date(end) - _date(start)).days + 1
        if low <= days <= high:
            starts[end][start] += 1
    found = []
    for end in sorted(starts, reverse=True):
        start = min(starts[end].items(), key=lambda item: (-item[1], item[0]))[0]
        found.append({"start": start, "end": end,
                      "days": (_date(end) - _date(start)).days + 1})
    return found


def by_frame(available: list[dict], kind: str) -> dict[str, dict]:
    """Frame → the one period in it, newest period first.

    A frame a newer period already holds pushes the older period to the frame
    before it, and the period records the frame it was pushed off. See the
    module docstring for why that is Seagate and not tidying.
    """
    taken: dict[str, dict] = {}
    for period in available:
        frame = frame_of(period["start"], period["end"], kind)
        shifted = None
        while frame in taken:
            shifted = shifted or frame
            frame = step_back(frame, 1)
        taken[frame] = dict(period, frame=frame, frame_shifted_from=shifted)
    return taken


def requested(taken: dict[str, dict], count: int) -> list[str | None]:
    """The `count` consecutive frames ending at the newest one on record.

    `None` where there is no newest: a record holding no period of this length
    has no frame to count back from, and the rows are still named — thirteen
    requested periods come out of this file whatever went into it.
    """
    if not taken:
        return [None] * count
    newest = max(taken)
    return [step_back(newest, index) for index in range(count)]


def covering_year(years: dict[str, dict], frame: str) -> dict | None:
    """The annual period on record that contains a quarter frame's middle day.

    A company's fourth quarter is reported only inside the annual figure, so
    the frame it would have filled is empty and this is where the quarter went.
    Naming the annual period is as far as this file goes: deriving the quarter
    from it is a separate piece of work.
    """
    first, last = frame_bounds(frame)
    middle = first + dt.timedelta(days=((last - first).days + 1) // 2)
    for period in years.values():
        if _date(period["start"]) <= middle <= _date(period["end"]):
            return period
    return None


def _absent(frame: str, taken: dict[str, dict], kind: str,
            years: dict[str, dict]) -> str:
    """Why a requested frame holds no period. Always names the frame.

    The frame and nothing more: `frame_bounds` turns `CY2025Q3` into the two
    calendar dates whenever a reader wants them, and this text cannot carry
    them. A frame's calendar end can fall after the run's own cutoff — Apple's
    fiscal 2025 ended 2025-09-27 and its 10-K was filed on 2025-10-31, so the
    frame that year sits in, CY2025, ends two months after the cutoff — and
    `src/assemble_bundle.py` puts this file in front of the predictor, where
    `tests/test_assemble_bundle.py` refuses any date later than the cutoff. The
    dates that do appear here are a filed period's own start and end, which are
    inside the cutoff because the filing that stated them is.
    """
    said = f"neither record holds a {kind}-length period in {frame}"
    if not taken:
        return f"{said}, and no {kind} of any frame is on record"
    older = [one for one in taken if one < frame]
    newer = [one for one in taken if one > frame]
    if not newer:
        said = f"{said}; the newest on record is {max(taken)}"
    elif not older:
        said = f"{said}; the oldest on record is {min(taken)}"
    else:
        said = f"{said}; the record holds {min(newer)} and {max(older)} on either side"
    if kind == "quarter":
        covering = covering_year(years, frame)
        if covering is not None:
            said = (f"{said}. The annual period {covering['start']}..{covering['end']} "
                    f"({covering['frame']}) covers it")
    return said


def _series(facts: list[dict], taken: dict[str, dict], prefix: str, kind: str,
            count: int, years: dict[str, dict]) -> list[dict]:
    rows = []
    for index, frame in enumerate(requested(taken, count)):
        label = f"{prefix}-{index}"
        if frame is None:
            rows.append({"label": label, "frame": None, "filled": False,
                         "ratios": {},
                         "reason": f"no {kind}-length period is on record at all"})
            continue
        period = taken.get(frame)
        if period is None:
            rows.append({"label": label, "frame": frame, "filled": False,
                         "reason": _absent(frame, taken, kind, years), "ratios": {}})
            continue
        rows.append({"label": label, "frame": frame, "filled": True,
                     "start": period["start"], "end": period["end"],
                     "days": period["days"],
                     "frame_shifted_from": period["frame_shifted_from"],
                     "ratios": {name: ratio(facts, name, period) for name in RATIOS}})
    return rows


# --- changes -----------------------------------------------------------------

def _tags(cell: dict) -> dict:
    """Which us-gaap concept each term of a filled ratio was taken from."""
    return {term: entry["tag"] for term, entry in (cell.get("inputs") or {}).items()}


def _change(rows: list[dict], index: int, back: int, name: str, kind: str) -> dict:
    """This period's ratio minus the one `back` frames earlier.

    Only when both were built from the same concepts. `CONCEPTS` gives each
    term a list of acceptable tags and `pick_fact` takes the first one the
    record carries, so two periods of the same ratio can rest on different
    us-gaap concepts — 24 of 134 emitted changes did when the table read one
    instance. NVIDIA's contract liability change read +0.004437 where
    like-for-like gives +0.023102, and ESCO's **flipped sign**, −0.009963
    against +0.000324, feeding the `deferred_revenue_diverging` flag. A
    difference of two different things is not a change, so it is refused and
    the reason names both tags.
    """
    here = rows[index]["ratios"].get(name, {})
    if "value" not in here:
        return {"against": None, "reason": f"{name} is not filled in {rows[index]['label']}"}
    if index + back >= len(rows):
        return {"against": None,
                "reason": f"the {kind} {back} back is outside the requested window"}
    there = rows[index + back]
    if "value" not in there["ratios"].get(name, {}):
        return {"against": there["label"],
                "reason": f"{name} is not filled in {there['label']}"}

    mine, theirs = _tags(here), _tags(there["ratios"][name])
    differing = sorted(term for term in mine if mine[term] != theirs.get(term))
    if differing:
        named = "; ".join(f"{term}: us-gaap:{mine[term]} in {rows[index]['label']} "
                          f"and us-gaap:{theirs.get(term)} in {there['label']}"
                          for term in differing)
        return {"against": there["label"],
                "reason": f"{name} rests on a different concept in each period, so "
                          f"the difference would not be a change — {named}"}
    return {"against": there["label"],
            "change": here["value"] - there["ratios"][name]["value"]}


def add_changes(quarters: list[dict], years: list[dict]) -> None:
    """Year over year and quarter over quarter, in place.

    The rows are consecutive calendar frames, so four back is the same calendar
    quarter a year earlier and one back is the quarter before it. A year has no
    quarter-over-quarter change and says so rather than carrying a field a
    reader would have to guess the meaning of.
    """
    for index, row in enumerate(quarters):
        for name in list(row["ratios"]):
            row["ratios"][name]["year_over_year"] = _change(quarters, index, 4, name, "quarter")
            row["ratios"][name]["quarter_over_quarter"] = _change(quarters, index, 1, name, "quarter")
    for index, row in enumerate(years):
        for name in list(row["ratios"]):
            row["ratios"][name]["year_over_year"] = _change(years, index, 1, name, "year")
            row["ratios"][name]["quarter_over_quarter"] = {
                "against": None, "reason": "an annual period has no preceding quarter"}


# --- coverage ----------------------------------------------------------------

def coverage(quarters: list[dict], years: list[dict]) -> dict:
    """Every requested period, and every ratio, either filled or explained."""
    def period_rows(rows):
        out = []
        for row in rows:
            entry = {"label": row["label"], "frame": row["frame"],
                     "status": "filled" if row["filled"] else "missing"}
            if row["filled"]:
                entry["start"], entry["end"] = row["start"], row["end"]
                unfilled = sorted(name for name, cell in row["ratios"].items()
                                  if "value" not in cell)
                entry["ratios_filled"] = len(row["ratios"]) - len(unfilled)
                entry["ratios_missing"] = {name: row["ratios"][name]["missing"]
                                           for name in unfilled}
            else:
                entry["reason"] = row["reason"]
            out.append(entry)
        return out

    by_ratio = []
    for name in RATIOS:
        filled, missing = 0, []
        for row in quarters + years:
            if not row["filled"]:
                missing.append({"period": row["label"], "reason": row["reason"]})
            elif "value" in row["ratios"][name]:
                filled += 1
            else:
                missing.append({"period": row["label"],
                                "reason": row["ratios"][name]["missing"]})
        by_ratio.append({"ratio": name, "filled": filled, "missing": missing})

    # Two numbers, because they answer different questions and only one of them
    # is the substantive one. A period is "on record" when the record holds any
    # consolidated duration of that length — a frame can be held by a period two
    # share-repurchase facts put there and carry no ratio at all. Reporting
    # "10 of 13 filled" for that is a truthful sentence about the wrong thing.
    rows = quarters + years
    on_record = sum(1 for row in rows if row["filled"])
    with_a_ratio = sum(1 for row in rows if row["filled"]
                       and any("value" in cell for cell in row["ratios"].values()))
    return {
        "requested": {"quarters": QUARTERS_REQUESTED, "years": YEARS_REQUESTED},
        "periods_on_record": on_record,
        "periods_with_at_least_one_ratio": with_a_ratio,
        "quarters": period_rows(quarters),
        "years": period_rows(years),
        "ratios": by_ratio,
    }


# --- the table ---------------------------------------------------------------

def _cutoff_of(numbers: dict, fixtures_root) -> dt.date | None:
    if numbers.get("cutoff"):
        return cutoff_guard.parse_date(numbers["cutoff"], "cutoff")
    try:
        return cutoff_guard.default_cutoff(numbers["ticker"], fixtures_root=fixtures_root)
    except cutoff_guard.CutoffGuardError:
        return None


def _unloaded(facts: list[dict], ticker: str, cutoff: dt.date | None,
              fixtures_root) -> list[dict]:
    """Filings on record at the cutoff that no companyfacts row came from.

    EDGAR loads companyfacts filing by filing and runs behind: on the day this
    fixture set was fetched, Carrier's and Littelfuse's July 2026 quarterlies
    were in neither company's history. That is the source's own lag, and a
    period that resolves to one of them has nothing in the history to look up —
    so it is filled from the filing's own instance, and the cells say so. Named
    here rather than left to be inferred from the cells.
    """
    loaded = {fact["source_accession"] for fact in facts
              if fact.get("record") == HISTORY}
    out = []
    for form in ("10-K", "10-Q"):
        for row in cutoff_guard.documents(ticker, form=form, fixtures_root=fixtures_root):
            if not row.get("accession") or row["accession"] in loaded:
                continue
            if cutoff is not None and _date(row["filing_date"]) > cutoff:
                continue
            out.append({"accession": row["accession"], "form": row["form"],
                        "filing_date": row["filing_date"],
                        "report_date": row.get("report_date", "")})
    return sorted({(one["accession"], one["form"], one["filing_date"],
                    one["report_date"]) for one in out})


def trends(numbers: dict, *, fixtures_root=cutoff_guard.FIXTURES) -> dict:
    """The whole table: companyfacts first, the instances for what it lacks."""
    for key in ("ticker", "facts"):
        if key not in numbers:
            raise TrendInputError(f"input_numbers.json has no {key!r}")
    ticker = numbers["ticker"]
    cutoff = _cutoff_of(numbers, fixtures_root)

    # Both records are cut at the same date. The gate already refuses an
    # instance filed after the cutoff, so this drops nothing in a run assembled
    # under the same cutoff; it is here so that one sentence covers both
    # records -- no fact filed after the cutoff reaches a cell.
    instance = [dict(fact, record=INSTANCE) for fact in numbers["facts"]
                if cutoff is None or _date(fact["filing_date"]) <= cutoff]
    try:
        record = read_history(ticker, fixtures_root)
        history = history_facts(record, cutoff)
        # What the catalogue holds *for this run*, which is not what the
        # catalogue holds. Its own as-of date and the date of the newest filing
        # it carries are both later than every cutoff a run can have — that is
        # what makes it a catalogue — so neither belongs in a file the
        # predictor reads. `filed_through` is the newest filing among the rows
        # that survived the cutoff, and is inside it by construction.
        source = {"read": True, "path": record["path"], "rows": len(history),
                  "filed_through": max((fact["filing_date"] for fact in history),
                                       default=None)}
    except (cutoff_guard.CutoffGuardError, OSError, ValueError) as exc:
        history, source = [], {"read": False, "reason": str(exc)}
    facts = history + instance

    quarter_periods = by_frame(periods(facts, "quarter"), "quarter")
    year_periods = by_frame(periods(facts, "year"), "year")
    quarters = _series(facts, quarter_periods, "Q", "quarter",
                       QUARTERS_REQUESTED, year_periods)
    years = _series(facts, year_periods, "FY", "year", YEARS_REQUESTED, year_periods)
    add_changes(quarters, years)

    try:
        unloaded = _unloaded(facts, ticker, cutoff, fixtures_root)
    except cutoff_guard.CutoffGuardError:
        unloaded = []
    return {
        "ticker": ticker,
        "cutoff": numbers.get("cutoff") or (cutoff.isoformat() if cutoff else None),
        "source": {"companyfacts": source,
                   "documents": numbers.get("documents", []),
                   "facts": len(facts),
                   "facts_used": sum(1 for fact in facts if usable(fact)),
                   "accessions_with_no_companyfacts_row": [
                       {"accession": one[0], "form": one[1], "filing_date": one[2],
                        "report_date": one[3]} for one in unloaded]},
        "quarters": quarters,
        "years": years,
        "coverage": coverage(quarters, years),
    }


def render(payload: dict) -> str:
    """Deterministic by construction: sorted keys, no clock, no set iteration."""
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="the trend table, from companyfacts")
    parser.add_argument("--numbers", required=True, help="path to input_numbers.json")
    parser.add_argument("--fixtures", default=str(cutoff_guard.FIXTURES))
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)

    try:
        numbers = json.loads(Path(args.numbers).read_text(encoding="utf-8"))
        payload = trends(numbers, fixtures_root=Path(args.fixtures))
    except (OSError, ValueError, TrendInputError) as exc:
        print(f"trends: {exc}", file=sys.stderr)
        return BAD_INPUT
    Path(args.out).write_text(render(payload), encoding="utf-8")
    total = QUARTERS_REQUESTED + YEARS_REQUESTED
    print(f"trends: {payload['ticker']} "
          f"{payload['coverage']['periods_with_at_least_one_ratio']} of {total} "
          f"periods carry a ratio "
          f"({payload['coverage']['periods_on_record']} of {total} are on record "
          f"at all) → {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
