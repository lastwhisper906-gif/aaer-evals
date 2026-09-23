"""The trend table. Python does every division on this page.

The input is the **companyfacts record** — `tests/fixtures/{ticker}/companyfacts.json.gz`,
read through `src/cutoff_guard.py`'s `load_catalogue` — and nothing else. Each
ratio carries its formula, and for every term the us-gaap tag, the accession and
the filing date of the row it was taken from, so a reader holding the same
record can find the row and redo the division. Nothing here is rounded,
smoothed, interpolated or carried forward.

**Why the record and not the filing.** `docs/INPUT_SPEC.md` §5 item 1 asks for
these eleven ratios "over 8 quarters and 5 years", and §1's "Why companyfacts"
says why that source: one request returns every period's value from every
filing, which fills the window without fetching nine years of filings. This
module read `input_numbers.json` instead until now — the facts of one 10-K and
one 10-Q — and between them those carry three fiscal years and two quarters, so
seven of the thirteen requested periods were reported missing for no reason but
the input. The window is the spec's; the record is what can fill it.

**The cutoff is applied to the rows, not to the file.** companyfacts is a
catalogue of facts drawn from many filings and is not itself a filing, so
`cutoff_guard.load_catalogue` is the route: it checks the path against the
fixture manifest exactly as the date gate does and then drops every row filed
after the cutoff, which is where the look-ahead in a catalogue lives. This
module re-counts that on the way in and refuses a record that still holds a late
row, because a table that is one row past its cutoff is not a smaller error than
a file that is.

**The window is anchored on the run's own period, not on the record's newest
one.** The caller passes the triggering report's period of report. The eight
quarters are walked back from there, so `quarters-back-0` is the quarter this
run is about whether or not the record reaches it, and `years-back-0` is the
newest fiscal year at or before that period — the trigger's own year on an annual report, and the last
year to end on a quarterly one. companyfacts can lag the filing that triggered
the run — two of these twelve records were fetched before their 10-Q — and
anchored on the record those tables labelled the quarter *before* the run's own
`quarters-back-0`, left the run's own period in no slot at all, and said twelve
of thirteen periods were on record. A slot the record cannot reach is reported empty with
that named as the reason.

**The rules that decide which row is the row**, all of them mechanical:

- us-gaap and USD only. companyfacts holds the entity-wide fact alone, so a
  consolidated total is what a row already is — and a line a company states only
  by segment, as Carrier states cost of sales, is not in the record at all.
- A duration of 80–100 days is a quarter and one of 350–380 days is a year (a
  52/53-week filer's quarters are 91 days and a year-to-date period is not a
  quarter). A balance-sheet instant belongs to the period whose end date it
  equals exactly.
- A period is a period when a tag this table actually reads reports it. Reading
  every annual-length duration as a fiscal year takes a slot in the window from
  a real year on the strength of a credit facility's commitment-fee period —
  `src/fourth_quarter.py` measured nine such spans across these twelve records.
- **When a period is reported more than once, the latest filing at or before the
  cutoff wins** (`docs/INPUT_SPEC.md` §1, "Cutoff"). If that filing states two
  different values for one period there is nothing to choose between, and the
  cell says so rather than choosing. That a later filing restated an earlier
  period is `src/restatement_trace.py`'s to report, not this file's to bury in
  a cell.

**What is still missing, and why it is named rather than filled.** A fiscal
fourth quarter is not reported as a duration by anyone: a 10-K states the year
and the three 10-Qs state Q1 to Q3, so the fourth quarter has to be derived —
`src/fourth_quarter.py` does that, and this table reports the slot as missing
with the derivation named instead of quietly skipping the period.

**Research and development, capitalized.** The spec's one further column —
book value and earnings with research and development capitalized — is on each
fiscal year and not on the quarters, because the life it amortizes over is
counted in years. Six years of `ResearchAndDevelopmentExpense` are read, the
year and five before it; the asset is what five-year straight-line amortization
leaves unamortized, earnings add back the year's expense and take off the
year's amortization, and book value adds the asset. No tax effect is applied.
Beside it is the development cost the company itself capitalized, read only
from `CapitalizedComputerSoftwareAdditions`: of the twelve, ESCO alone
capitalizes one in its latest 10-K, and it tags that line with its own
extension, which companyfacts does not carry, so the cell says missing. A
filing that says in words that nothing was capitalized, as Ciena's does, has
not tagged a zero, and this file does not read a zero into it.

The non-GAAP gap is missing for a different reason and says so: `Revenues` is a
us-gaap concept and "adjusted net income" is not, so no non-GAAP measure is in
companyfacts, which carries us-gaap and dei facts only. It comes off the 8-K
exhibit, which is a different file.

    python3.12 -m src.trends --ticker AAPL --cutoff 2026-07-31 --out input_trends.json
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import sys
from pathlib import Path

try:
    from src import cutoff_guard, fetch_companyfacts, interpreter_pin
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import cutoff_guard, fetch_companyfacts, interpreter_pin

BAD_INPUT = 2

NAMESPACE = "us-gaap"
UNIT = "USD"                # every term of every ratio is an amount of money

# The forms whose facts are an input here. `docs/INPUT_SPEC.md` §1 gives the
# numeric facts one row — "10-K, 10-Q, /A | all numeric facts" — lists DEF 14A
# under **Not fetched**, and gives an 8-K 8.01 or 9.01 "item codes only". A
# catalogue of every filing's facts carries all of them anyway, so the rule has
# to be applied here or the table quietly reads documents the spec excludes: a
# proxy statement's pay-versus-performance table states net income too, and
# Generac's says 161,400,000 for 2025 where its 10-K says 159,554,000. Filed
# later than the 10-K, that row wins "the latest filing wins" and the ratio it
# feeds is a proxy's rounded figure over a 10-K's cash flow, published with the
# proxy named as its source.
STATEMENT_FORMS = ("10-K", "10-Q")   # and their /A amendments, by prefix

QUARTERS_REQUESTED = 8
YEARS_REQUESTED = 5
QUARTER_DAYS = (80, 100)
YEAR_DAYS = (350, 380)
QUARTER_STEP = 91          # a 52/53-week quarter, in days
YEAR_STEP = 364            # thirteen of them
TOLERANCE_DAYS = 20        # how far a fiscal period end may sit from the step

# Which us-gaap tags may stand for each term, best first. A term is filled by
# the first tag in the list the record actually carries for that period, and the
# output names which one it was, so a reader can see that Apple's revenue came
# from `RevenueFromContractWithCustomerExcludingAssessedTax` and Generac's did
# not.
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
    # The research-and-development-capitalized column, and nothing else, reads
    # these three. One tag each, so six years of expense are six years of one
    # concept and never a sum across two.
    "research_and_development_expense": ("duration", ("ResearchAndDevelopmentExpense",)),
    # Development cost the company itself capitalized, as a statement line.
    # Only the additions: `CapitalizedComputerSoftwarePeriodIncreaseDecrease`
    # is a net change in the balance and may be net of amortization.
    "capitalized_development_cost": ("duration", ("CapitalizedComputerSoftwareAdditions",)),
    "stockholders_equity": ("instant", ("StockholdersEquity",)),
}

# Terms of the research-and-development column alone. They are not evidence
# that a fiscal period exists: that list was measured on the ratio terms, and a
# column added beside the table does not get to move the table's periods.
COLUMN_ONLY_TERMS = frozenset({"research_and_development_expense",
                               "capitalized_development_cost",
                               "stockholders_equity"})

# The tags whose durations are evidence that a fiscal period exists at all. An
# annual-length span under a tag no term names is not a fiscal year: TTM
# Technologies' record carries one `us-gaap:LossOnContracts` fact that starts
# its 2025 year a day early, and counting that as a second year ending the same
# day takes a slot from a real one.
PERIOD_TAGS = frozenset(tag for term, (kind, tags) in CONCEPTS.items()
                        if kind == "duration" and term not in COLUMN_ONLY_TERMS
                        for tag in tags)

# docs/INPUT_SPEC.md §5 item 1, in the order the spec lists them — §4 is the
# market table, which this file has nothing to do with.
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

# What each ratio divides by, written out, for the one reason a row can be
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

NO_NON_GAAP = ("no us-gaap concept carries a non-GAAP measure, and companyfacts "
               "holds us-gaap and dei facts only")

# What a quarter slot with no duration in the record is told. The commonest
# cause is not a gap in the record at all: a fiscal fourth quarter is reported
# by nobody, so the slot names where that number does come from.
DERIVED_FOURTH_QUARTER = ("the commonest cause is a fiscal fourth quarter, which "
                          "no filing reports as a duration — the 10-K states the "
                          "year and the three 10-Qs state the first three "
                          "quarters, so it is derived by src/fourth_quarter.py")


class TrendInputError(Exception):
    """The record is not there, or not the shape this reads. Never a default."""


def _date(value: str) -> dt.date:
    return dt.date.fromisoformat(value)


def _days(start: str, end: str) -> int:
    return (_date(end) - _date(start)).days + 1


def _spelled(start: str | None, end: str) -> str:
    """How a period is written inside a fact id: a span, or the instant's date.

    The spelling `docs/INPUT_SPEC.md` §2.2 gives and `src/articulation.py`
    already writes, so one fact has one name wherever it is cited.
    """
    return f"{start}..{end}" if start else end


# --- the record --------------------------------------------------------------

def observations(document: dict) -> dict[str, dict[tuple, list[dict]]]:
    """tag → (start, end) → the rows that reported it. `start` is None at an instant.

    us-gaap and USD only, which is every term of every ratio: each one is an
    amount of money, and a share count or a percentage under the same tag name
    is a different fact. companyfacts holds the entity-wide value alone, so
    there is no segment to filter out here — a line stated only by segment is
    simply not in the record, and `why_missing` says so.
    """
    facts = document.get("facts")
    if not isinstance(facts, dict):
        raise TrendInputError(
            "the companyfacts record carries no 'facts' object — refused, because "
            "a document with no rows is not the record this reads")
    index: dict[str, dict[tuple, list[dict]]] = {}
    for tag, concept in facts.get(NAMESPACE, {}).items():
        for row in concept.get("units", {}).get(UNIT, []):
            if not from_a_statement(row):
                continue
            index.setdefault(tag, {}).setdefault(
                (row.get("start"), row["end"]), []).append(row)
    return index


def from_a_statement(row: dict) -> bool:
    """Was this row reported by a periodic financial statement?

    `STATEMENT_FORMS` by prefix, so `10-K/A` and `10-Q/A` are in — the spec's
    own row is "10-K, 10-Q, /A" — and a proxy statement, an 8-K exhibit and a
    registration statement are out. A row with no form is out: a fact whose
    filing this cannot name is a fact whose source a reader cannot check.
    """
    return str(row.get("form") or "").startswith(STATEMENT_FORMS)


def units_of(document: dict, tag: str) -> list[str]:
    """Every unit a statement reported this tag in. For the reason, not the value."""
    concept = document.get("facts", {}).get(NAMESPACE, {}).get(tag)
    return sorted(unit for unit, rows in (concept or {}).get("units", {}).items()
                  if any(from_a_statement(row) for row in rows))


def other_forms(document: dict, tag: str) -> list[str]:
    """Which non-statement forms reported this tag. For the reason, not the value."""
    concept = document.get("facts", {}).get(NAMESPACE, {}).get(tag)
    return sorted({str(row.get("form") or "an unnamed form")
                   for rows in (concept or {}).get("units", {}).values()
                   for row in rows if not from_a_statement(row)})


def filed_after(document: dict, cutoff: dt.date) -> list[str]:
    """Rows the cutoff should have kept out. On a record read through the gate, none.

    `cutoff_guard.load_catalogue` drops them, so this answers for a record that
    reached here another way. A table one row past its cutoff is a look-ahead
    violation and not a smaller answer, so it is refused rather than trimmed.

    A row with no date of its own, or one that will not parse, is named here
    too: an absent date is not an early date, and it is not a late one either.
    That is also what lets `as_filed` below compare dates as the strings they
    are — every row still standing has been parsed once.
    """
    found = set()
    for namespace, concepts in (document.get("facts") or {}).items():
        for tag, concept in concepts.items():
            for unit, rows in (concept.get("units") or {}).items():
                for row in rows:
                    named = (f"{namespace}:{tag} [{unit}] {row.get('accn')} "
                             f"filed {row.get('filed')!r}")
                    try:
                        filed = cutoff_guard.parse_date(row.get("filed"), named)
                    except cutoff_guard.CutoffGuardError:
                        found.add(named)
                        continue
                    if filed > cutoff:
                        found.add(named)
    return sorted(found)


def as_filed(rows: list[dict], named: str) -> dict:
    """One period's value under one tag: the latest filing at or before the cutoff.

    `docs/INPUT_SPEC.md` §1, "Cutoff": "When a period is reported more than
    once, the latest filing before the cutoff wins." If that filing states two
    different values for the same period there is nothing to choose between
    them, and choosing anyway is how a wrong number gets published with a source
    note attached. `src/fourth_quarter.py` settles the same question the same way.

    That an earlier filing reported something else is not recorded here:
    `src/restatement_trace.py` is what reports a quiet restatement, and a
    difference buried in a ratio's inputs is a difference nobody reads.
    """
    latest = max(row["filed"] for row in rows)
    newest = [row for row in rows if row["filed"] == latest]
    values = sorted({row["val"] for row in newest})
    accessions = sorted({row["accn"] for row in newest})
    if len(values) != 1:
        return {"missing": f"{named} is reported as {values} by the filing of "
                           f"{latest} ({', '.join(accessions)}) — two values for "
                           f"one period is not a number to divide by"}
    return {"value": float(values[0]), "filed": latest, "accession": accessions[0]}


# --- the periods -------------------------------------------------------------

def periods(index: dict, kind: str) -> list[dict]:
    """Every distinct duration of the requested length, newest first."""
    low, high = QUARTER_DAYS if kind == "quarter" else YEAR_DAYS
    found: dict[tuple[str, str], dict] = {}
    for tag in PERIOD_TAGS:
        for start, end in index.get(tag, {}):
            if not start:
                continue
            days = _days(start, end)
            if low <= days <= high:
                found[(start, end)] = {"start": start, "end": end, "days": days}
    return sorted(found.values(), key=lambda p: (p["end"], p["start"]), reverse=True)


def requested(available: list[dict], count: int, step: int, kind: str,
              anchor: str | None = None, stale: str | None = None) -> list[dict]:
    """The `count` consecutive fiscal periods ending at the anchor.

    **The anchor is the run's own period, not the record's newest one.** The
    caller passes the triggering report's period of report — EDGAR's
    `report_date`, which the fixture manifest carries — and the window is walked
    back from there. Anchoring on whatever the record happens to hold instead
    looks identical until the record is older than the trigger, and then it
    quietly renames the periods: Carrier's record was fetched on 2026-04-30 and
    its 10-Q was filed 2026-07-28, so the quarter before the run's own was
    labelled `quarters-back-0`, the run's own quarter appeared nowhere, and the
    table said twelve of thirteen periods were on record. A reader comparing that against
    `input_numbers.json`, which does carry the June quarter, has two inputs
    disagreeing about which quarter this is.

    Without an anchor — the command line, with no triggering report — the newest
    period on record is used and `trends` records which of the two it was.

    Labelled by how far back they are, resolved to a real period when one ends
    within `TOLERANCE_DAYS` of where the step says it should. A period with no
    match is not dropped — it is returned with the date that was looked for and
    the reason nothing is there.
    """
    empty = (f"the companyfacts record carries no {kind}-length duration under "
             f"any concept this table reads")
    if anchor:
        end = _date(anchor)
    elif available:
        end = _date(available[0]["end"])
    else:
        return [{"index": index, "period": None, "reason": empty}
                for index in range(count)]
    reach = _date(available[0]["end"]) if available else None
    taken: set[tuple[str, str]] = set()
    out = []
    for index in range(count):
        target = end - dt.timedelta(days=step * index)
        best, best_gap = None, None
        for period in available:
            key = (period["start"], period["end"])
            if key in taken:
                continue
            gap = abs((_date(period["end"]) - target).days)
            if gap <= TOLERANCE_DAYS and (best_gap is None or gap < best_gap):
                best, best_gap = period, gap
        if best is None:
            reason = (f"no {kind} ending within {TOLERANCE_DAYS} days of "
                      f"{target.isoformat()} is in the companyfacts record")
            if stale and (reach is None or target > reach):
                reason = f"{reason}; {stale}"
            elif kind == "quarter":
                reason = f"{reason}; {DERIVED_FOURTH_QUARTER}"
            out.append({"index": index, "period": None,
                        "target_end": target.isoformat(), "reason": reason})
        else:
            taken.add((best["start"], best["end"]))
            out.append({"index": index, "period": best, "target_end": target.isoformat()})
    return out


def year_end_anchor(available: list[dict], period_end: str | None) -> str | None:
    """Where the five-year window ends: the newest fiscal year the run is about.

    Not the newest the record holds. For an annual trigger that is the trigger's
    own period; for a quarterly one it is the last fiscal year end at or before
    it. Both are the same sentence — *the newest fiscal year end at or before
    the run's period* — and the only question is how to place that date when the
    record does not carry the year. It is projected, by the same 364-day step
    `requested` already walks back on: a record fetched the day before a 10-K
    lands holds last year's annual figures and nothing else, and reading its
    newest year as `years-back-0` hands a reader the prior year under the label
    of the year the run is about. Projected instead, `years-back-0` is the year
    the run is about and the slot is empty with the reason.

    `None` when there is no anchor to place — no trigger period, or a record
    with no annual duration at all — and then the caller falls back to the
    newest year on record.
    """
    if not period_end or not available:
        return None
    end = _date(period_end)
    slack = dt.timedelta(days=TOLERANCE_DAYS)
    projected = _date(available[0]["end"])
    step = dt.timedelta(days=YEAR_STEP)
    while projected + step <= end + slack:
        projected += step
    # Within the slack of the run's own period, the trigger *is* the fiscal year
    # — an annual report — and the period it names is better than the projection.
    if abs((projected - end).days) <= TOLERANCE_DAYS:
        return period_end
    return projected.isoformat()


# --- one term, one period ----------------------------------------------------

def why_missing(document: dict, index: dict, term: str, period: dict,
                concepts: dict | None = None) -> str:
    """Which of the five ways this term is not here.

    The reader's next step differs for each: a concept nobody tags, a concept
    the record carries in another unit, a concept only a filing this table does
    not read reported, a concept reported for other periods, and the one concept
    that is in no filing's standard taxonomy at all.
    """
    concepts = CONCEPTS if concepts is None else concepts
    tags = concepts[term][1]
    if not tags:
        return f"no row for {term}: {NO_NON_GAAP}"
    named = ", ".join(f"us-gaap:{tag}" for tag in tags)
    elsewhere = sorted({unit for tag in tags for unit in units_of(document, tag)
                        if unit != UNIT})
    if not any(tag in index for tag in tags):
        if elsewhere:
            return (f"no row for {term}: {named} is in the record only in "
                    f"{', '.join(elsewhere)}, and every term of every ratio here "
                    f"is an amount in {UNIT}")
        unread = sorted({form for tag in tags for form in other_forms(document, tag)})
        if unread:
            return (f"no row for {term}: {named} is in the record only from "
                    f"{', '.join(unread)}, and this table reads the periodic "
                    f"financial statements — docs/INPUT_SPEC.md §1 gives the "
                    f"numeric facts to 10-K, 10-Q and their amendments")
        return (f"no row for {term}: the companyfacts record tags none of {named} "
                f"in any period. companyfacts holds the entity-wide fact alone, so "
                f"this is either a concept the company does not tag or one it "
                f"states only by segment — the filing says which, and this record "
                f"cannot")
    wanted = _spelled(period["start"], period["end"]) \
        if concepts[term][0] == "duration" else period["end"]
    return (f"no row for {term} in {wanted}: "
            f"{named} is in the record, but not for this period")


def term_source(document: dict, index: dict, term: str, period: dict,
                concepts: dict | None = None) -> dict:
    """The one row behind a term for one period, or the reason there is none.

    The first tag in `CONCEPTS[term]` the record carries for this period is the
    one used — and if that tag's rows cannot be settled, the cell says so rather
    than falling through to the next concept. Falling through would swap the
    concept under the reader without saying so, which is the mistake
    `_change` refuses across periods.

    `concepts` is another term map read by this same rule. `src/baselines.py`
    passes its own, because the formula baselines need terms this table does
    not read, and a term they share is picked out of the record the same way.
    """
    concepts = CONCEPTS if concepts is None else concepts
    kind, tags = concepts[term]
    for tag in tags:
        key = (period["start"], period["end"]) if kind == "duration" \
            else (None, period["end"])
        rows = index.get(tag, {}).get(key)
        if not rows:
            continue
        spelled = _spelled(*key)
        settled = as_filed(rows, f"us-gaap:{tag} for {spelled}")
        if "missing" in settled:
            return settled
        return {"tag": tag, "unit": UNIT, "period": spelled,
                "value": settled["value"], "accession": settled["accession"],
                "filed": settled["filed"],
                "id": f"{settled['accession']}:facts:{tag}:{spelled}"}
    return {"missing": why_missing(document, index, term, period, concepts)}


def ratio(document: dict, index: dict, name: str, period: dict) -> dict:
    """One ratio for one period: a value with its inputs, or a reason."""
    spec = RATIOS[name]
    inputs, values = {}, {}
    for term in spec["terms"]:
        found = term_source(document, index, term, period)
        if "missing" in found:
            return {"missing": found["missing"]}
        inputs[term] = found
        values[term] = found["value"]
    written, of = DENOMINATORS[name]
    if of(values) == 0:
        return {"missing": f"{written} is zero in "
                           f"{_spelled(period['start'], period['end'])}"}
    return {"value": spec["value"](values, period["days"]),
            "formula": spec["formula"], "inputs": inputs}


# --- the series --------------------------------------------------------------

def _label(prefix: str, index: int) -> str:
    """`quarters-back-0`, `years-back-3`: how far back, in words and a count.

    They were `Q-0` and `FY-3`, which is the letter-number shape `CLAUDE.md`
    forbids. A reader quotes these labels into a report, and the report is read
    by the plain-name check even though this table, as the text the agent saw,
    is not.
    """
    return f"{prefix}-{index}"


def _series(document: dict, index: dict, slots: list[dict], prefix: str) -> list[dict]:
    rows = []
    for slot in slots:
        label = _label(prefix, slot["index"])
        if slot["period"] is None:
            rows.append({"label": label, "filled": False,
                         "target_end": slot.get("target_end"),
                         "reason": slot["reason"], "ratios": {}})
            continue
        period = slot["period"]
        rows.append({"label": label, "filled": True, "start": period["start"],
                     "end": period["end"], "days": period["days"],
                     "target_end": slot.get("target_end"),
                     "ratios": {name: ratio(document, index, name, period)
                                for name in RATIOS}})
    return rows


def _tags(cell: dict) -> dict:
    """Which us-gaap concept each term of a filled ratio was taken from."""
    return {term: entry["tag"] for term, entry in (cell.get("inputs") or {}).items()}


def _change(rows: list[dict], index: int, back: int, name: str, kind: str) -> dict:
    """This period's ratio minus the one `back` periods earlier.

    Only when both were built from the same concepts. `CONCEPTS` gives each
    term a list of acceptable tags and the first one the record carries is
    taken, so two periods of the same ratio can rest on different us-gaap
    concepts — 24 of 134 emitted changes did on the instance route. NVIDIA's
    contract liability change read +0.004437 where like-for-like gives
    +0.023102, and ESCO's **flipped sign**, −0.009963 against +0.000324,
    feeding the `deferred_revenue_diverging` flag. A difference of two different
    things is not a change, so it is refused and the reason names both tags.

    The tag-continuity map `docs/INPUT_SPEC.md` names — `src/tag_continuity.py`
    and its versioned data file — is what would say that two of these concepts
    are one series under two names. Until this reads it, a pair it would join is
    a refusal here rather than a subtraction.
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

    A year has no quarter-over-quarter change and says so rather than carrying
    a field a reader would have to guess the meaning of.
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


def coverage(quarters: list[dict], years: list[dict]) -> dict:
    """Every requested period, and every ratio, either filled or explained."""
    def period_rows(rows):
        out = []
        for row in rows:
            entry = {"label": row["label"], "status": "filled" if row["filled"] else "missing",
                     "target_end": row.get("target_end")}
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
    # duration of that length under a concept this table reads; it carries a
    # ratio only when the terms of one are there too. Reporting the first for
    # the second is a truthful sentence about the wrong thing.
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


# --- research and development, capitalized --------------------------------

# `docs/INPUT_SPEC.md` §5 item 1's one further column: book value and earnings
# with research and development capitalized. The spec names the column and not
# the life, so the life is a default and `docs/needs_judgment.md` carries it:
# five years, straight line, a full year's weight on the year the money was
# spent, and no tax effect.
RND_LIFE_YEARS = 5

RND_FORMULAS = {
    "research_and_development_asset":
        "sum over k = 0..4 of research_and_development_expense[year - k] * (5 - k) / 5",
    "research_and_development_amortization":
        "sum over k = 1..5 of research_and_development_expense[year - k] / 5",
    "earnings_with_rnd_capitalized":
        "net_income + research_and_development_expense[year] "
        "- research_and_development_amortization",
    "book_value_with_rnd_capitalized":
        "stockholders_equity + research_and_development_asset",
    "capitalized_over_expense":
        "capitalized_development_cost / research_and_development_expense[year]",
}


def rnd_capitalized(document: dict, index: dict, row: dict,
                    annual: list[dict]) -> dict:
    """One fiscal year of the research-and-development-capitalized column.

    Six years of expense are read — the year and the five before it — each
    found by walking back from this year's own end on the step the year window
    uses, and each one a row of the record with its accession. A year the record
    does not carry is not a zero: every quantity that needs it is missing, and
    the reason names the year. A company that states in words that it
    capitalized nothing has not tagged a zero, and a zero is not read into it.

    `capitalized_development_cost` is the development cost the company itself
    capitalized, beside the expense, for `rnd_capitalization_shift` in
    `docs/CHECKLIST.md`. It is not added to the asset: an amount already on the
    balance sheet was never in the expense line this capitalizes.
    """
    if not row["filled"]:
        return {"missing": f"no fiscal year in this slot: {row['reason']}"}
    period = {"start": row["start"], "end": row["end"], "days": row["days"]}
    chain = requested(annual, RND_LIFE_YEARS + 1, YEAR_STEP, "year", row["end"])
    expense: list[dict] = []
    for slot in chain:
        back = slot["index"]
        if slot["period"] is None:
            expense.append({"years_back": back,
                            "missing": f"{back} year(s) back: {slot['reason']}"})
            continue
        found = term_source(document, index, "research_and_development_expense",
                            slot["period"])
        expense.append({"years_back": back, **found} if "missing" not in found
                       else {"years_back": back,
                             "missing": f"{back} year(s) back: {found['missing']}"})

    def needs(backs, *cells) -> str | None:
        gaps = [expense[back]["missing"] for back in backs
                if "missing" in expense[back]]
        gaps += [cell["missing"] for cell in cells if "missing" in cell]
        return "; ".join(gaps) or None

    life = RND_LIFE_YEARS
    net_income = term_source(document, index, "net_income", period)
    equity = term_source(document, index, "stockholders_equity", period)
    capitalized = term_source(document, index, "capitalized_development_cost", period)
    out: dict = {"life_years": life, "formulas": RND_FORMULAS,
                 "research_and_development_expense": expense,
                 "net_income": net_income, "stockholders_equity": equity,
                 "capitalized_development_cost": capitalized}

    gap = needs(range(life))
    asset = None if gap else sum(expense[k]["value"] * (life - k) / life
                                 for k in range(life))
    out["research_and_development_asset"] = \
        {"missing": gap} if gap else {"value": asset}
    gap = needs(range(1, life + 1))
    amortization = None if gap else sum(expense[k]["value"] / life
                                        for k in range(1, life + 1))
    out["research_and_development_amortization"] = \
        {"missing": gap} if gap else {"value": amortization}

    gap = needs(range(life + 1), net_income)
    out["earnings_with_rnd_capitalized"] = {"missing": gap} if gap else {
        "value": net_income["value"] + expense[0]["value"] - amortization}
    gap = needs(range(life), equity)
    out["book_value_with_rnd_capitalized"] = {"missing": gap} if gap else {
        "value": equity["value"] + asset}

    gap = needs([0], capitalized)
    if gap:
        out["capitalized_over_expense"] = {"missing": gap}
    elif expense[0]["value"] == 0:
        out["capitalized_over_expense"] = {
            "missing": "research_and_development_expense is zero in "
                       f"{_spelled(period['start'], period['end'])}"}
    else:
        out["capitalized_over_expense"] = {
            "value": capitalized["value"] / expense[0]["value"]}
    return out


def rnd_sources(row: dict) -> list[dict]:
    """Every record row the column read for one fiscal year."""
    column = row.get("research_and_development_capitalized") or {}
    cells = list(column.get("research_and_development_expense") or [])
    cells += [column.get(term) or {} for term in
              ("net_income", "stockholders_equity", "capitalized_development_cost")]
    return [cell for cell in cells if "accession" in cell]


# --- the table ---------------------------------------------------------------

def read_record(ticker: str, cutoff, *, fixtures_root=cutoff_guard.FIXTURES) -> dict:
    """One company's companyfacts record, through the gate's catalogue route.

    `cutoff_guard.load_catalogue` and nothing else: the record is a committed
    fixture, gzipped, and reading it any other way is a read the bypass scan in
    `tests/test_cutoff_guard.py` cannot see. What comes back is the record with
    every row filed after the cutoff already gone.
    """
    entry = cutoff_guard.one_document(ticker, fetch_companyfacts.FORM,
                                      fetch_companyfacts.ROLE,
                                      fixtures_root=fixtures_root)
    return cutoff_guard.load_catalogue(entry["full_path"], cutoff,
                                       fixtures_root=fixtures_root)


def newest_filing(index: dict) -> str | None:
    """The filing date of the newest row in the record. None on an empty one."""
    filed = [row["filed"] for spans in index.values() for rows in spans.values()
             for row in rows if row.get("filed")]
    return max(filed) if filed else None


def trends(document: dict, cutoff, *, period_end=None) -> dict:
    """The whole table, from one companyfacts record read at `cutoff`.

    `period_end` is the triggering report's own period of report, and it anchors
    the quarter window — see `requested`. The years are anchored on the newest
    fiscal year on record whatever the trigger is, because a quarterly trigger's
    period is not a fiscal year end and looking for one there would report every
    year as missing.
    """
    try:
        stated = cutoff_guard.parse_date(cutoff, "cutoff")
    except cutoff_guard.CutoffGuardError as exc:
        raise TrendInputError(str(exc)) from exc
    if period_end is not None:
        try:
            period_end = cutoff_guard.parse_date(period_end, "period_end").isoformat()
        except cutoff_guard.CutoffGuardError as exc:
            raise TrendInputError(str(exc)) from exc
    if not document.get("ticker"):
        raise TrendInputError("the companyfacts record names no ticker")
    late = filed_after(document, stated)
    if late:
        raise TrendInputError(
            f"{len(late)} row(s) in the record are filed after the cutoff "
            f"{stated}, or carry no date this can read: {', '.join(late[:3])} — "
            f"refused, because a table one row past its cutoff is a look-ahead "
            f"violation and not a smaller answer")

    index = observations(document)
    # The triggering report was filed on the cutoff, so a record holding nothing
    # filed that day was fetched before it and cannot carry the periods that
    # report introduced. Said once here, and again in the slot it empties.
    newest = newest_filing(index)
    stale = None
    if newest and newest < stated.isoformat():
        stale = (f"the companyfacts record's newest row was filed {newest}, "
                 f"before this run's cutoff {stated.isoformat()} — the record "
                 f"was fetched before the triggering report, so the periods that "
                 f"report is the first to state are not in it")
    quarters = _series(document, index,
                       requested(periods(index, "quarter"), QUARTERS_REQUESTED,
                                 QUARTER_STEP, "quarter", period_end, stale),
                       "quarters-back")
    annual = periods(index, "year")
    years = _series(document, index,
                    requested(annual, YEARS_REQUESTED, YEAR_STEP, "year",
                              year_end_anchor(annual, period_end), stale),
                    "years-back")
    add_changes(quarters, years)
    for row in years:
        row["research_and_development_capitalized"] = rnd_capitalized(
            document, index, row, annual)
    used = sorted({entry["accession"]
                   for row in quarters + years
                   for cell in row["ratios"].values()
                   for entry in (cell.get("inputs") or {}).values()}
                  | {entry["accession"] for row in years
                     for entry in rnd_sources(row)})
    return {
        "ticker": document["ticker"],
        "cutoff": stated.isoformat(),
        "window": {
            "quarters_end": quarters[0].get("target_end") if quarters else None,
            "years_end": years[0].get("target_end") if years else None,
            "anchored_on": ("the triggering report's period of report"
                            if period_end else
                            "the newest quarter in the record, because no "
                            "triggering report was named"),
            "triggering_period_end": period_end,
            "record_newest_filing": newest,
            "record_predates_the_trigger": stale,
        },
        "source": {"record": "companyfacts",
                   "cik": document.get("cik"),
                   "entity_name": document.get("entity_name"),
                   "rows": sum(len(rows) for spans in index.values()
                               for rows in spans.values()),
                   "filings_read": used},
        "quarters": quarters,
        "years": years,
        "coverage": coverage(quarters, years),
    }


def table(ticker: str, cutoff, *, period_end=None,
          fixtures_root=cutoff_guard.FIXTURES) -> dict:
    """The record and the table in one call, for a caller that wants both done."""
    return trends(read_record(ticker, cutoff, fixtures_root=fixtures_root), cutoff,
                  period_end=period_end)


def name_cells(payload: dict, accession: str) -> dict:
    """The table with every cell of a filled period printing the id it is cited by.

    `docs/INPUT_SPEC.md` §2 gives a trend cell `{accession}:trends:{metric}:{period}`.
    The period is the row's own `start..end`, spelled as a fact id spells it,
    and a cell recording why a ratio is missing is named like one that holds a
    value, since the absence is what a reader may need to quote. The accession
    is the run's, because the table is the companyfacts record's and names no
    filing of its own; so the table is named where the run is assembled, and
    the table given is left as it was.
    """
    named = copy.deepcopy(payload)
    for row in (named.get("quarters") or []) + (named.get("years") or []):
        if not row.get("filled"):
            continue
        period = _spelled(row["start"], row["end"])
        for metric, cell in row["ratios"].items():
            cell["paragraph_id"] = f"{accession}:trends:{metric}:{period}"
    return named


def render(payload: dict) -> str:
    """Deterministic by construction: sorted keys, no clock, no set iteration."""
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="the trend table, from the companyfacts record")
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--cutoff", help="the triggering report's filing date; "
                                         "the fixture set's own as-of date by default")
    parser.add_argument("--period-end", help="the triggering report's period of "
                                             "report, which anchors the quarter "
                                             "window; the newest quarter on record "
                                             "by default")
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)

    try:
        # Absent means the default; empty means wrong, and the two are not the
        # same thing. `args.cutoff or default` turns `--cutoff ""` into a date
        # months after the trigger without saying so, which is the look-ahead
        # this module refuses everywhere else. An empty string reaches
        # `parse_date` and is refused there, by name.
        # Through the shared rule, not around it. This line was written the
        # long way and then reverted to `default_cutoff` by the merge that
        # brought the companyfacts trend table in, and the AST walk in
        # `tests/test_empty_cutoff.py` is what said so -- the invariant
        # `resolve_cutoff` claims in its own docstring was false on the tree
        # that claimed it.
        cutoff = cutoff_guard.resolve_cutoff(args.cutoff, args.ticker)
        payload = table(args.ticker, cutoff, period_end=args.period_end)
    except (OSError, ValueError, TrendInputError,
            cutoff_guard.CutoffGuardError) as exc:
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
