"""The calculator: every number the three analysts cite is computed here.

The owner's decision of 2026-09-28 (`docs/structure_changes.md`): agents read
and judge, Python calculates. No agent does arithmetic. Every number in an
analysis comes from `calculator.json` or from companyfacts, and an agent that
wants a number this file does not print asks for it by name rather than working
it out. So this file prints a great deal.

What it reads
-------------

- **The companyfacts record**, through `src/trends.py`'s `read_record`, which is
  `cutoff_guard.load_catalogue`: every row filed after the cutoff is already gone
  when this sees the record. The rule that picks *the* row for a period is the
  trend table's own `term_source` -- the first tag in a term's list that the
  record carries for that period, the latest filing at or before the cutoff,
  and a refusal when that filing states two values -- so a term this file
  shares with the trend table is the same row in both.
- **The triggering filing's own facts**, `input_numbers.json` from the run
  bundle, through `cutoff_guard.load_bundle_file`, for the one family
  companyfacts cannot carry: a concentration percentage is stated against a
  customer axis, and companyfacts holds the entity-wide fact alone.
- **The triggering filing's own entity-wide facts, where companyfacts lags.**
  SEC's companyfacts can trail a filing by months; for an accession the record
  does not name at all, the bundle's instance facts with no dimension are added
  as rows of the record's own shape, and `read_from_the_filing_because_companyfacts_lagged`
  lists the accessions that were.
- **The cost of capital's two market-wide inputs**, committed under
  `src/cost_of_capital/` with the URL and hash they were fetched with.
- **Prices**, a directory of daily series in the shape `src/market.py`'s
  `read_prices` reads, for beta, the price at the cutoff and the market value
  of equity. With no directory, every figure that needs one is written as not
  computed, with the reason, and the rest is computed anyway.
- **The valuation analyst's assumptions** (`assumptions.json`) for the DCF,
  and **the accounting analyst's adjustments** (inside
  `analysis_accounting.json`) for the quality-adjusted free cash flow. Python
  never invents a driver and never computes an agent's number for it: an
  adjustment names the calculator field its amount is, and this file reads it.

What it refuses
---------------

A term with no row is written **missing**, with the trend table's own reason,
and never filled. A measure that needs a missing term is missing too, and says
which term. The run **fails loudly**: every missing core input is printed on
standard error, listed under `missing` at the top of the file, and turns the
exit status to `INCOMPLETE`. Nothing here is estimated, interpolated or
defaulted to zero -- with two rules stated in the open: the one below, and an
operating lease total that a quarterly report does not restate, which is read as
the newest balance filed at or before the period end, dated with `as_of`, and
flagged when a lease line the record holds at the period end is larger.

**A line the statement does not print is not a missing number.** A cash-flow
statement with no acquisitions line, or a balance sheet with no debt line, is a
company that reported none, and a family of such lines (debt, borrowing,
acquisitions) is summed over the lines the record carries for the period. The
output names each family's lines, so a reader sees `acquisitions: no line on
record for this period` rather than a silent zero; the core terms -- revenue,
operating cash flow, capital expenditure, operating income, diluted shares --
have no such rule and fail when absent.

Periods
-------

Every flow is on a **trailing-four-quarter** basis. A 10-Q states its quarter
and its year to date, and never the trailing year, so for a quarterly trigger:

    trailing four quarters = prior fiscal year + this year to date - prior year to date

and for an annual trigger it is the fiscal year itself. The fourth quarter is
never needed as a duration. Balances are read at the period end, and a year
earlier where a ratio divides a flow by an average balance.

Sign conventions are read from the tag
--------------------------------------

`DIRECTION` gives every cash-flow tag this file reads the sign its taxonomy
defines. `Payments...` is an amount of cash that left, stated positive;
`Proceeds...` is cash that came in; `NetCashProvidedByUsedIn...` and
`ProceedsFromRepayments...` are already signed. A cash-flow term whose tag has
no entry is refused, so a new tag cannot enter a free-cash-flow measure under an
assumed sign. A negative value under a `Payments...` tag is read as the taxonomy
defines it -- cash that came back -- and flagged, because it is unusual.

    python3.12 -m src.calculator --ticker NVDA --cutoff 2026-08-26 \\
        --period-end 2026-07-26 --form 10-Q --bundle <run directory> \\
        [--prices <directory>] [--assumptions assumptions.json] \\
        [--adjustments analysis_accounting.json] --out calculator.json
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import math
import re
import statistics
import sys
import zipfile
from pathlib import Path

try:
    from src import cutoff_guard, interpreter_pin, market, trends
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import cutoff_guard, interpreter_pin, market, trends

BAD_INPUT = 2
INCOMPLETE = 4

COST_OF_CAPITAL = Path(__file__).resolve().parent / "cost_of_capital"

# The statutory federal rate the effective rate is capped at. 21 per cent since
# the Tax Cuts and Jobs Act, section 13001, for tax years beginning after 2017.
STATUTORY_TAX_RATE = 0.21

DAYS_IN_YEAR = 365
TOLERANCE = trends.TOLERANCE_DAYS
YEAR_STEP = trends.YEAR_STEP
QUARTER_STEP = trends.QUARTER_STEP

# The forecast. Ten explicit years, then a terminal value.
FORECAST_YEARS = 10
SENSITIVITY_WACC_STEPS = (-0.01, 0.0, 0.01)
SENSITIVITY_GROWTH_STEPS = (-0.005, 0.0, 0.005)
REVERSE_BRACKET = (-0.50, 1.50)
REVERSE_TOLERANCE = 1e-10
REVERSE_ITERATIONS = 200


class CalculatorInputError(Exception):
    """An input is not there or not the shape this reads. Never a default."""


# --- the terms ----------------------------------------------------------------
#
# Which tags may stand for each term, best first, read by the trend table's
# rule. A term the trend table also reads is its own entry, so the two files
# divide the same row. `unit` is USD unless the entry says otherwise.

SHARED_WITH_THE_TREND_TABLE = (
    "revenue", "cost_of_revenue", "net_income", "operating_cash_flow",
    "receivables", "inventory", "assets", "cash", "contract_liabilities",
    "stockholders_equity", "inventory_reserve", "bad_debt_allowance",
    "warranty_accrual", "property_plant_and_equipment",
    "research_and_development_expense",
)

TERMS: dict[str, tuple[str, tuple[str, ...]]] = {
    **{term: trends.CONCEPTS[term] for term in SHARED_WITH_THE_TREND_TABLE},
    **trends.CALCULATOR_TERMS,
}

# Terms stated in shares. Read from the record under the unit `shares`.
SHARE_TERMS: dict[str, tuple[str, str, tuple[str, ...]]] = {
    "diluted_shares": ("us-gaap", "duration", ("WeightedAverageNumberOfDilutedSharesOutstanding",)),
    "shares_outstanding": ("dei", "instant", ("EntityCommonStockSharesOutstanding",)),
}

# Families: a figure a statement may print on several lines. Each family is a
# list of groups summed with their signs; inside a group the tags are
# alternatives for one line, and the first the record carries wins, so a line
# tagged under two names -- a total and its own component, as Generac tags its
# long-term borrowings both `LongTermDebtAndCapitalLeaseObligations` and
# `LongTermDebtNoncurrent` -- is read once. A `total`, where the record carries
# it, replaces every group: it is what they add up to. Every line on record that
# was not added is listed with its value, so the reader sees what was set aside.
#
# A group is a tuple of alternative tags, or a dict naming a subtotal and the
# lines it replaces, for the one family whose subtotal sits inside another:
# Apple's commercial paper, net, is the sum of three lines it also tags.
COMMERCIAL_PAPER = {"total": "ProceedsFromRepaymentsOfCommercialPaper",
                    "parts": ("ProceedsFromRepaymentsOfShortTermDebtMaturingInThreeMonthsOrLess",
                              "ProceedsFromShortTermDebtMaturingInMoreThanThreeMonths",
                              "RepaymentsOfShortTermDebtMaturingInMoreThanThreeMonths")}
FAMILIES: dict[str, dict] = {
    "debt_current": {"kind": "instant", "total": "DebtCurrent", "groups": (
        ("LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtCurrent"),
        ("ShortTermBorrowings", "CommercialPaper"))},
    # `LongTermDebt` is last: the taxonomy defines it as including current
    # maturities, but Qualcomm tags its balance sheet's noncurrent line with it
    # (12,781 million at 2026-06-28, beside short-term debt of 2,489). It is read
    # only where neither noncurrent tag is on record, and flagged when it is.
    "debt_noncurrent": {"kind": "instant", "total": None, "groups": (
        ("LongTermDebtAndCapitalLeaseObligations", "LongTermDebtNoncurrent", "LongTermDebt"),)},
    "acquisitions": {"kind": "duration", "total": None, "groups": (
        ("PaymentsToAcquireBusinessesNetOfCashAcquired",
         "PaymentsToAcquireBusinessesAndInterestInAffiliates"),)},
    "borrowing_issued": {"kind": "duration", "total": "ProceedsFromIssuanceOfDebt", "groups": (
        ("ProceedsFromIssuanceOfLongTermDebt", "ProceedsFromIssuanceOfSeniorLongTermDebt",
         "ProceedsFromDebtNetOfIssuanceCosts"),
        ("ProceedsFromConvertibleDebt",))},
    "borrowing_repaid": {"kind": "duration", "total": "RepaymentsOfDebt", "groups": (
        ("RepaymentsOfLongTermDebt", "RepaymentsOfLongTermDebtAndCapitalSecurities",
         "RepaymentsOfSeniorDebt", "RepaymentsOfUnsecuredDebt",
         "RepaymentsOfOtherLongTermDebt"),
        ("RepaymentsOfConvertibleDebt",),
        ("RepaymentsOfShortTermDebt",),
        ("RepaymentsOfOtherDebt", "RepaymentsOfAssumedDebt"))},
    "borrowing_short_term_net": {"kind": "duration",
                                 "total": "ProceedsFromRepaymentsOfShortTermDebt",
                                 "groups": (COMMERCIAL_PAPER,)},
}


def family_tags(name: str) -> tuple[str, ...]:
    """Every tag a family may read, total first."""
    spec = FAMILIES[name]
    tags = [spec["total"]] if spec["total"] else []
    for group in spec["groups"]:
        tags += [group["total"], *group["parts"]] if isinstance(group, dict) else list(group)
    return tuple(tags)


# Likewise the two lines of an operating lease, where the total is not tagged.
LEASE_LINES = ("OperatingLeaseLiabilityCurrent", "OperatingLeaseLiabilityNoncurrent")
# Depreciation and amortization stated on two lines, where the total is not.
DEPRECIATION_LINES = ("Depreciation", "AmortizationOfIntangibleAssets")

# The sign each cash-flow tag carries, as the taxonomy defines it.
#   "outflow"  -- a positive value is cash that left
#   "inflow"   -- a positive value is cash that came in
#   "signed"   -- the value already carries the sign of its cash effect
#   "increase_in_asset" / "increase_in_liability" -- a change in a balance
#   "noncash_addback" -- an expense added back because no cash left
DIRECTION: dict[str, str] = {
    "NetCashProvidedByUsedInOperatingActivities": "signed",
    "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations": "signed",
    "PaymentsToAcquirePropertyPlantAndEquipment": "outflow",
    "PaymentsToAcquireProductiveAssets": "outflow",
    "PaymentsForCapitalImprovements": "outflow",
    "PaymentsToAcquireBusinessesNetOfCashAcquired": "outflow",
    "PaymentsToAcquireBusinessesAndInterestInAffiliates": "outflow",
    "PaymentsOfDividends": "outflow",
    "PaymentsOfDividendsCommonStock": "outflow",
    "PaymentsForRepurchaseOfCommonStock": "outflow",
    "ProceedsFromIssuanceOfLongTermDebt": "inflow",
    "ProceedsFromIssuanceOfDebt": "inflow",
    "ProceedsFromIssuanceOfSeniorLongTermDebt": "inflow",
    "ProceedsFromDebtNetOfIssuanceCosts": "inflow",
    "ProceedsFromConvertibleDebt": "inflow",
    "RepaymentsOfLongTermDebt": "outflow",
    "RepaymentsOfDebt": "outflow",
    "RepaymentsOfSeniorDebt": "outflow",
    "RepaymentsOfConvertibleDebt": "outflow",
    "RepaymentsOfOtherLongTermDebt": "outflow",
    "RepaymentsOfLongTermDebtAndCapitalSecurities": "outflow",
    "RepaymentsOfUnsecuredDebt": "outflow",
    "RepaymentsOfOtherDebt": "outflow",
    "RepaymentsOfShortTermDebt": "outflow",
    "RepaymentsOfShortTermDebtMaturingInMoreThanThreeMonths": "outflow",
    "ProceedsFromShortTermDebtMaturingInMoreThanThreeMonths": "inflow",
    "RepaymentsOfAssumedDebt": "outflow",
    "ProceedsFromRepaymentsOfShortTermDebt": "signed",
    "ProceedsFromRepaymentsOfCommercialPaper": "signed",
    "ProceedsFromRepaymentsOfShortTermDebtMaturingInThreeMonthsOrLess": "signed",
    "ProceedsFromSaleAndCollectionOfReceivables": "inflow",
    "TransferOfFinancialAssetsAccountedForAsSalesCashProceedsReceivedForAssets"
    "DerecognizedAmount": "inflow",
    "ShareBasedCompensation": "noncash_addback",
    "AllocatedShareBasedCompensationExpense": "noncash_addback",
    "IncreaseDecreaseInAccountsReceivable": "increase_in_asset",
    "IncreaseDecreaseInReceivables": "increase_in_asset",
    "IncreaseDecreaseInAccountsAndOtherReceivables": "increase_in_asset",
    "IncreaseDecreaseInInventories": "increase_in_asset",
    "IncreaseDecreaseInAccountsPayable": "increase_in_liability",
    "IncreaseDecreaseInAccountsPayableTrade": "increase_in_liability",
}

# The cash-flow terms and families: every tag they read must carry a direction.
CASH_FLOW_TERMS = ("operating_cash_flow", "capital_expenditure", "share_based_compensation",
                   "dividends_paid", "share_repurchases", "proceeds_from_sale_of_receivables",
                   "change_in_receivables", "change_in_inventory", "change_in_payables")
CASH_FLOW_FAMILIES = ("acquisitions", "borrowing_issued", "borrowing_repaid",
                      "borrowing_short_term_net")

# What a flow of each direction does to cash, as a multiplier on the value.
CASH_EFFECT = {"inflow": 1.0, "outflow": -1.0, "signed": 1.0,
               "increase_in_asset": -1.0, "increase_in_liability": 1.0,
               "noncash_addback": 1.0}

# The terms whose absence stops the run: nothing the three analyses need can be
# computed without them.
CORE_TERMS = ("revenue", "operating_cash_flow", "capital_expenditure", "net_income",
              "assets", "diluted_shares")


def direction_of(tag: str) -> str:
    """The sign a cash-flow tag carries, or a refusal. Never assumed."""
    try:
        return DIRECTION[tag]
    except KeyError as exc:
        raise CalculatorInputError(
            f"us-gaap:{tag} is read as a cash flow but has no sign in DIRECTION -- "
            f"refused, because a free-cash-flow measure under an assumed sign is "
            f"wrong half the time and right by luck the other half") from exc


# --- the record ---------------------------------------------------------------

def index_units(document: dict, namespace: str, unit: str) -> dict:
    """tag -> (start, end) -> rows, for one namespace and one unit, statements only."""
    index: dict[str, dict[tuple, list[dict]]] = {}
    for tag, concept in (document.get("facts") or {}).get(namespace, {}).items():
        for row in concept.get("units", {}).get(unit, []):
            if not trends.from_a_statement(row):
                continue
            index.setdefault(tag, {}).setdefault((row.get("start"), row["end"]), []).append(row)
    return index


def _date(text: str) -> dt.date:
    return dt.date.fromisoformat(text)


def _days(start: str, end: str) -> int:
    return (_date(end) - _date(start)).days + 1


def _near(one: str, other: dt.date, tolerance: int = TOLERANCE) -> bool:
    return abs((_date(one) - other).days) <= tolerance


# --- periods --------------------------------------------------------------------

def durations(index: dict) -> list[tuple[str, str]]:
    """Every (start, end) a period-defining tag reports, the trend table's list."""
    found = set()
    for tag in trends.PERIOD_TAGS:
        for start, end in index.get(tag, {}):
            if start:
                found.add((start, end))
    return sorted(found)


def year_to_date(spans: list[tuple[str, str]], end: dt.date, *,
                 annual: bool = False) -> tuple[str, str] | None:
    """The longest duration of up to a year ending on `end` (the fiscal year to date).

    `annual` asks for a full year and nothing shorter.
    """
    low, high = trends.YEAR_DAYS if annual else (trends.QUARTER_DAYS[0], trends.YEAR_DAYS[1])
    ending = [(s, e) for s, e in spans if _date(e) == end and low <= _days(s, e) <= high]
    return max(ending, key=lambda span: _days(*span)) if ending else None


def like_span_a_year_earlier(spans, span: tuple[str, str]) -> tuple[str, str] | None:
    """The same stretch of the prior fiscal year: ends about 364 days earlier, same length."""
    target = _date(span[1]) - dt.timedelta(days=YEAR_STEP)
    length = _days(*span)
    fits = [(s, e) for s, e in spans
            if _near(e, target) and abs(_days(s, e) - length) <= TOLERANCE]
    return min(fits, key=lambda one: abs((_date(one[1]) - target).days)) if fits else None


def year_ending(spans, end: dt.date) -> tuple[str, str] | None:
    """The fiscal year that ends within the tolerance of `end`."""
    fits = [(s, e) for s, e in spans
            if trends.YEAR_DAYS[0] <= _days(s, e) <= trends.YEAR_DAYS[1] and _near(e, end)]
    return min(fits, key=lambda one: abs((_date(one[1]) - end).days)) if fits else None


def quarter_ending(spans, end: dt.date) -> tuple[str, str] | None:
    fits = [(s, e) for s, e in spans
            if trends.QUARTER_DAYS[0] <= _days(s, e) <= trends.QUARTER_DAYS[1] and _near(e, end)]
    return min(fits, key=lambda one: abs((_date(one[1]) - end).days)) if fits else None


def trigger_periods(index: dict, period_end: str, form: str) -> dict:
    """The spans every trailing-four-quarter figure is built from, or a refusal."""
    spans = durations(index)
    end = _date(period_end)
    annual_trigger = form.startswith("10-K")
    current = year_to_date(spans, end, annual=annual_trigger)
    if current is None:
        raise CalculatorInputError(
            f"no duration ending on the period of report {period_end} is in the "
            f"record under any tag the trend table reads -- the record predates the "
            f"triggering report, or the period of report is wrong")
    prior = like_span_a_year_earlier(spans, current)
    periods = {"current_to_date": current, "prior_to_date": prior,
               "annual_trigger": annual_trigger}
    if annual_trigger:
        periods["prior_year"] = prior
        periods["two_years_back_to_date"] = like_span_a_year_earlier(spans, prior) if prior else None
        periods["two_years_back"] = periods["two_years_back_to_date"]
    else:
        periods["prior_year"] = year_ending(spans, _date(current[0]) - dt.timedelta(days=1))
        periods["two_years_back_to_date"] = like_span_a_year_earlier(spans, prior) if prior else None
        periods["two_years_back"] = (year_ending(spans, _date(prior[0]) - dt.timedelta(days=1))
                                     if prior else None)
    periods["quarter"] = quarter_ending(spans, end)
    periods["prior_quarter_end"] = end - dt.timedelta(days=QUARTER_STEP)
    periods["year_ago_quarter"] = quarter_ending(spans, end - dt.timedelta(days=YEAR_STEP))
    periods["balance_now"] = period_end
    periods["balance_year_ago"] = prior[1] if prior else None
    periods["fiscal_years"] = fiscal_years(spans, end)
    return periods


def fiscal_years(spans, end: dt.date, count: int = 6) -> list[tuple[str, str]]:
    """The last `count` fiscal years ending at or before `end`, newest first."""
    years = sorted({(s, e) for s, e in spans
                    if trends.YEAR_DAYS[0] <= _days(s, e) <= trends.YEAR_DAYS[1]
                    and _date(e) <= end + dt.timedelta(days=TOLERANCE)},
                   key=lambda one: one[1], reverse=True)
    out, last_end = [], None
    for span in years:
        if last_end is not None and (_date(last_end) - _date(span[1])).days < 300:
            continue          # an overlapping annual-length span, not another year
        out.append(span)
        last_end = span[1]
        if len(out) == count:
            break
    return out


# --- one term -------------------------------------------------------------------

def _period(span: tuple[str, str] | None, *, instant: bool = False) -> dict | None:
    if span is None:
        return None
    if instant:
        return {"start": None, "end": span[1] if isinstance(span, tuple) else span}
    return {"start": span[0], "end": span[1]}


class Record:
    """One company's record at one cutoff, with every read named."""

    def __init__(self, document: dict):
        self.document = document
        self.usd = trends.observations(document)
        self.shares = {"us-gaap": index_units(document, "us-gaap", "shares"),
                       "dei": index_units(document, "dei", "shares")}

    # A term for one span, by the trend table's rule.
    def term(self, term: str, span) -> dict:
        if span is None:
            return {"missing": f"no {term}: the period it would be read for is not "
                               f"in the record"}
        if term in SHARE_TERMS:
            return self.share_term(term, span)
        kind = TERMS[term][0]
        period = {"start": None if kind == "instant" else span[0],
                  "end": span if isinstance(span, str) else span[1]}
        if kind == "instant" and isinstance(span, tuple):
            period = {"start": None, "end": span[1]}
        found = trends.term_source(self.document, self.usd, term, period, TERMS)
        if "missing" in found:
            fallback = self.two_line_fallback(term, period)
            if fallback is not None:
                return fallback
            return found
        if term in CASH_FLOW_TERMS:
            found["direction"] = direction_of(found["tag"])
        return found

    def two_line_fallback(self, term: str, period: dict) -> dict | None:
        """A total some companies state only as its two lines, summed."""
        lines = {"operating_lease_liability": LEASE_LINES,
                 "depreciation_and_amortization": DEPRECIATION_LINES}.get(term)
        if not lines:
            return None
        key = (period["start"], period["end"])
        parts = []
        for tag in lines:
            rows = self.usd.get(tag, {}).get(key)
            if not rows:
                return None
            settled = trends.as_filed(rows, f"us-gaap:{tag}")
            if "missing" in settled:
                return None
            parts.append(_fact(tag, key, settled))
        return {"value": sum(part["value"] for part in parts),
                "formula": " + ".join(lines), "parts": parts,
                "tag": " + ".join(lines), "unit": "USD"}

    def share_term(self, term: str, span) -> dict:
        namespace, kind, tags = SHARE_TERMS[term]
        index = self.shares[namespace]
        if kind == "instant":
            return self.cover_shares(tags)
        key = span if isinstance(span, tuple) else (None, span)
        for tag in tags:
            rows = index.get(tag, {}).get(key)
            if rows:
                settled = trends.as_filed(rows, f"{namespace}:{tag}")
                if "missing" in settled:
                    return settled
                return _fact(tag, key, settled, unit="shares", namespace=namespace)
        return {"missing": f"no row for {term} in {key[0]}..{key[1]} under "
                           f"{', '.join(namespace + ':' + t for t in tags)}"}

    def cover_shares(self, tags) -> dict:
        """The shares outstanding the newest filing at or before the cutoff printed on its cover."""
        rows = [row for tag in tags for spans in self.shares["dei"].get(tag, {}).values()
                for row in spans]
        if not rows:
            return {"missing": "no dei:EntityCommonStockSharesOutstanding row is in the record"}
        latest = max(row["filed"] for row in rows)
        newest = [row for row in rows if row["filed"] == latest]
        dates = {row["end"] for row in newest}
        if len(dates) != 1:
            return {"missing": f"the filing of {latest} states shares outstanding at "
                               f"{sorted(dates)} -- more than one class or date, which "
                               f"this does not add up for you"}
        total = sum(row["val"] for row in newest)
        classes = len(newest)
        accn = newest[0]["accn"]
        end = newest[0]["end"]
        return {"value": float(total), "tag": "EntityCommonStockSharesOutstanding",
                "namespace": "dei", "unit": "shares", "period": end,
                "accession": accn, "filed": latest, "classes_summed": classes,
                "id": f"{accn}:facts:EntityCommonStockSharesOutstanding:{end}"}

    # A family for one span: one line per group, summed with its sign.
    def family(self, name: str, span) -> dict:
        spec = FAMILIES[name]
        if span is None:
            return {"missing": f"no {name}: the period it would be read for is not in the record"}
        key = (None, span[1] if isinstance(span, tuple) else span) if spec["kind"] == "instant" \
            else span
        found: dict[str, dict] = {}
        for tag in family_tags(name):
            rows = self.usd.get(tag, {}).get(key)
            if not rows:
                continue
            settled = trends.as_filed(rows, f"us-gaap:{tag}")
            if "missing" in settled:
                return settled
            fact = _fact(tag, key, settled)
            if name in CASH_FLOW_FAMILIES:
                fact["direction"] = direction_of(tag)
                if fact["direction"] == "outflow" and fact["value"] < 0:
                    fact["flag"] = ("a negative value under a Payments tag: read as the "
                                    "taxonomy defines it, cash that came back")
            found[tag] = fact
        if spec["total"] and spec["total"] in found:
            lines = [found[spec["total"]]]
            rule = f"{spec['total']}, the total, which replaces its lines"
        else:
            lines, rule = [], "one line per group, the first tag on record in each"
            for group in spec["groups"]:
                if isinstance(group, dict):
                    if group["total"] in found:
                        lines.append(found[group["total"]])
                    else:
                        lines += [found[tag] for tag in group["parts"] if tag in found]
                    continue
                chosen = next((tag for tag in group if tag in found), None)
                if chosen:
                    lines.append(found[chosen])
        used = {line["tag"] for line in lines}
        value = sum(line["value"] for line in lines)
        out = {"value": value, "lines": lines, "rule": rule, "unit": "USD",
               "formula": " + ".join(line["tag"] for line in lines) or "no line on record",
               "lines_not_added": [{"tag": tag, "value": fact["value"], "id": fact["id"]}
                                   for tag, fact in found.items() if tag not in used]}
        if not lines:
            out["note"] = (f"{name}: no line on record for this period -- the statement "
                           f"prints none of {', '.join(family_tags(name))}")
        if "LongTermDebt" in used:
            out["check"] = ("the noncurrent line is read from us-gaap:LongTermDebt, which the "
                            "taxonomy defines as including current maturities; if this "
                            "company's figure includes them, they are counted again in "
                            "debt_current")
        return out

    def latest_balance(self, term: str, end: str) -> dict:
        """A balance at the period end, or the newest one filed before it, dated.

        For a line a quarterly report does not restate -- an operating lease
        total, which many companies print only in the annual report -- the
        newest balance at or before the period end is the as-filed figure, and
        it says which date it is. It is never read as zero.
        """
        at_end = self.term(term, end)
        if "missing" not in at_end:
            return at_end
        tags = TERMS[term][1]
        instants = sorted({date for tag in tags + LEASE_LINES
                           for (start, date) in self.usd.get(tag, {})
                           if start is None and date <= end}, reverse=True)
        partial = [{"tag": tag, "value": trends.as_filed(rows, tag).get("value")}
                   for tag in LEASE_LINES
                   for rows in [self.usd.get(tag, {}).get((None, end))] if rows]
        for date in instants:
            found = self.term(term, date)
            if "missing" not in found:
                out = dict(found, as_of=date,
                           note=f"the filing for {end} does not state {term}; this is the "
                                f"newest balance filed at or before it, at {date}")
                larger = [line for line in partial
                          if isinstance(line["value"], float) and line["value"] > found["value"]]
                if larger:
                    out["contradicted_at_period_end"] = (
                        f"the record holds {larger[0]['tag']} of {larger[0]['value']} at {end}, "
                        f"larger than this carried total -- the balance grew and the carried "
                        f"figure understates it")
                return out
        return at_end


def _fact(tag: str, key: tuple, settled: dict, *, unit: str = "USD",
          namespace: str = "us-gaap") -> dict:
    spelled = trends._spelled(*key)
    return {"tag": tag, "namespace": namespace, "unit": unit, "period": spelled,
            "value": settled["value"], "accession": settled["accession"],
            "filed": settled["filed"],
            "id": f"{settled['accession']}:facts:{tag}:{spelled}"}


# --- trailing four quarters ----------------------------------------------------

def trailing(record: Record, term: str, periods: dict, *, back: int = 0,
             family: bool = False) -> dict:
    """A flow over the trailing four quarters, or one year earlier with `back=1`."""
    read = record.family if family else record.term
    if back == 0:
        to_date, prior_to_date, year = (periods["current_to_date"],
                                        periods["prior_to_date"], periods["prior_year"])
    else:
        to_date, prior_to_date, year = (periods["prior_to_date"],
                                        periods["two_years_back_to_date"],
                                        periods["two_years_back"])
    if periods["annual_trigger"]:
        part = read(term, to_date)
        if "missing" in part:
            return {"missing": part["missing"]}
        return {"value": part["value"], "formula": "the fiscal year", "parts": [part],
                "unit": part.get("unit", "USD")}
    parts = {"prior_fiscal_year": read(term, year),
             "this_year_to_date": read(term, to_date),
             "prior_year_to_date": read(term, prior_to_date)}
    for name, part in parts.items():
        if "missing" in part:
            return {"missing": f"{term} over the trailing four quarters needs the "
                               f"{name.replace('_', ' ')}: {part['missing']}"}
    value = (parts["prior_fiscal_year"]["value"] + parts["this_year_to_date"]["value"]
             - parts["prior_year_to_date"]["value"])
    out = {"value": value,
           "formula": "prior_fiscal_year + this_year_to_date - prior_year_to_date",
           "parts": parts, "unit": parts["this_year_to_date"].get("unit", "USD")}
    tags = {part.get("tag") or part.get("formula") for part in parts.values()}
    if len(tags) > 1:
        out["tags_differ"] = sorted(str(tag) for tag in tags)
    return out


def quarter(record: Record, term: str, spans: list, end: dt.date) -> dict:
    """One fiscal quarter's flow: stated, or this year to date minus the last.

    A fourth quarter is never stated as a duration -- the 10-K states the year
    -- so it is the year less the nine months, on the same start date, and the
    derivation is named.
    """
    direct = quarter_ending(spans, end)
    if direct is not None:
        found = record.term(term, direct)
        if "missing" not in found:
            return {"value": found["value"], "formula": "the quarter as stated",
                    "parts": [found], "end": direct[1]}
    to_date = year_to_date(spans, end)
    if to_date is None:
        near = [e for _, e in spans if _near(e, end)]
        if near:
            to_date = year_to_date(spans, _date(max(near)))
    if to_date is None:
        return {"missing": f"no {term} for the quarter ending near {end}: no duration "
                           f"ends there"}
    start = to_date[0]
    earlier = [(s, e) for s, e in spans if s == start and _date(e) < _date(to_date[1])
               and abs((_date(to_date[1]) - _date(e)).days - QUARTER_STEP) <= TOLERANCE]
    if not earlier:
        return {"missing": f"no {term} for the quarter ending {to_date[1]}: it is not "
                           f"stated and no shorter year-to-date on the same start is "
                           f"on record to take it from"}
    before = max(earlier, key=lambda span: span[1])
    whole, part = record.term(term, to_date), record.term(term, before)
    for found in (whole, part):
        if "missing" in found:
            return {"missing": found["missing"]}
    return {"value": whole["value"] - part["value"],
            "formula": f"{to_date[0]}..{to_date[1]} less {before[0]}..{before[1]}",
            "parts": [whole, part], "end": to_date[1]}


# --- arithmetic with its inputs named -------------------------------------------

def _v(cell: dict) -> float:
    return cell["value"]


def measure(formula: str, inputs: dict, compute, *, unit: str = "ratio",
            denominator: str | None = None) -> dict:
    """A number with its formula and every input, or the first missing input's reason."""
    for name, cell in inputs.items():
        if cell is None or "missing" in cell:
            reason = cell["missing"] if cell else "not computed"
            return {"missing": f"{name}: {reason}", "formula": formula}
    values = {name: _v(cell) for name, cell in inputs.items()}
    if denominator is not None and values.get(denominator) == 0:
        return {"missing": f"{denominator} is zero", "formula": formula}
    try:
        value = compute(values)
    except ZeroDivisionError:
        return {"missing": "a denominator is zero", "formula": formula}
    return {"value": value, "formula": formula, "unit": unit,
            "inputs": {name: _brief(cell) for name, cell in inputs.items()}}


def _brief(cell: dict) -> dict:
    """An input as the output cites it: its value and where it came from."""
    out = {"value": cell["value"]}
    for key in ("id", "tag", "period", "formula", "unit", "note"):
        if key in cell:
            out[key] = cell[key]
    if "parts" in cell:
        parts = cell["parts"]
        items = parts.items() if isinstance(parts, dict) else enumerate(parts)
        out["parts"] = {str(name): _brief(part) for name, part in items}
    if "lines" in cell:
        out["lines"] = [_brief(line) for line in cell["lines"]]
    return out


def average(one: dict, other: dict) -> dict:
    if "missing" in one:
        return one
    if "missing" in other:
        return other
    return {"value": (one["value"] + other["value"]) / 2,
            "formula": "(now + a year earlier) / 2",
            "parts": {"now": one, "a_year_earlier": other}}


def total_debt(record: Record, end) -> dict:
    current, noncurrent = record.family("debt_current", end), record.family("debt_noncurrent", end)
    for cell in (current, noncurrent):
        if "missing" in cell:
            return cell
    return {"value": current["value"] + noncurrent["value"],
            "formula": "debt_current + debt_noncurrent",
            "parts": {"debt_current": current, "debt_noncurrent": noncurrent},
            "lines": current["lines"] + noncurrent["lines"]}


def cash_and_short_term_investments(record: Record, end) -> dict:
    cash = record.term("cash", end)
    if "missing" in cash:
        return cash
    investments = record.term("short_term_investments", end)
    if "missing" in investments:
        return {"value": cash["value"], "formula": "cash",
                "parts": {"cash": cash},
                "note": "no short-term investments line on record for this date"}
    return {"value": cash["value"] + investments["value"],
            "formula": "cash + short_term_investments",
            "parts": {"cash": cash, "short_term_investments": investments}}


def cash_effect(cell: dict) -> float:
    """What a cash-flow cell did to cash, by the sign its tag carries."""
    if "lines" in cell:
        return sum(CASH_EFFECT[line["direction"]] * line["value"] for line in cell["lines"])
    parts = cell.get("parts")
    if isinstance(parts, dict) and parts and "this_year_to_date" in parts:
        direction = parts["this_year_to_date"].get("direction")
    elif isinstance(parts, list) and parts:
        direction = parts[0].get("direction")
    else:
        direction = cell.get("direction")
    if direction is None:
        raise CalculatorInputError(f"a cash-flow cell carries no direction: {cell.get('formula')}")
    return CASH_EFFECT[direction] * cell["value"]


def trailing_family(record: Record, name: str, periods: dict) -> dict:
    """A family over the trailing four quarters, keeping each line's sign."""
    if periods["annual_trigger"]:
        found = record.family(name, periods["current_to_date"])
        return found
    parts = {"prior_fiscal_year": record.family(name, periods["prior_year"]),
             "this_year_to_date": record.family(name, periods["current_to_date"]),
             "prior_year_to_date": record.family(name, periods["prior_to_date"])}
    for label, part in parts.items():
        if "missing" in part:
            return {"missing": f"{name} over the trailing four quarters needs the "
                               f"{label.replace('_', ' ')}: {part['missing']}"}
    effect = {label: (sum(CASH_EFFECT[line["direction"]] * line["value"]
                          for line in part["lines"]) if name in CASH_FLOW_FAMILIES
                      else part["value"]) for label, part in parts.items()}
    value = (parts["prior_fiscal_year"]["value"] + parts["this_year_to_date"]["value"]
             - parts["prior_year_to_date"]["value"])
    out = {"value": value,
           "formula": "prior_fiscal_year + this_year_to_date - prior_year_to_date",
           "parts": parts, "unit": "USD"}
    if name in CASH_FLOW_FAMILIES:
        out["cash_effect"] = (effect["prior_fiscal_year"] + effect["this_year_to_date"]
                              - effect["prior_year_to_date"])
    notes = [part["note"] for part in parts.values() if part.get("note")]
    if notes:
        out["note"] = "; ".join(sorted(set(notes)))
    return out


def family_cash_effect(cell: dict) -> float:
    if "cash_effect" in cell:
        return cell["cash_effect"]
    return sum(CASH_EFFECT[line["direction"]] * line["value"] for line in cell.get("lines", []))


# --- the sections ------------------------------------------------------------------

def gather(record: Record, periods: dict) -> dict:
    """Every term the sections read, over the trailing four quarters and at the balances."""
    now, year_ago = periods["balance_now"], periods["balance_year_ago"]
    flows = ("revenue", "cost_of_revenue", "net_income", "operating_cash_flow",
             "operating_income", "pretax_income", "income_tax_expense", "interest_expense",
             "depreciation_and_amortization", "share_based_compensation",
             "capital_expenditure", "dividends_paid", "share_repurchases",
             "proceeds_from_sale_of_receivables", "inventory_write_down",
             "change_in_receivables", "change_in_inventory", "change_in_payables",
             "research_and_development_expense")
    stocks = ("receivables", "inventory", "assets", "cash", "contract_liabilities",
              "stockholders_equity", "current_assets", "current_liabilities",
              "accounts_payable", "short_term_investments", "total_liabilities",
              "operating_lease_liability", "supplier_finance_obligation",
              "unconditional_purchase_obligations", "guarantee_maximum_exposure",
              "inventory_reserve",
              "bad_debt_allowance", "warranty_accrual", "property_plant_and_equipment")
    ttm = {term: trailing(record, term, periods) for term in flows}
    ttm_prior = {term: trailing(record, term, periods, back=1)
                 for term in ("revenue", "operating_income", "net_income",
                              "operating_cash_flow", "capital_expenditure")}
    at_now = {term: record.term(term, now) for term in stocks}
    at_year_ago = {term: record.term(term, year_ago) if year_ago else
                   {"missing": "no period a year earlier is on record"} for term in stocks}
    families = {name: trailing_family(record, name, periods) for name in CASH_FLOW_FAMILIES}
    diluted_span = periods["quarter"] or periods["current_to_date"]
    return {
        "trailing_four_quarters": ttm,
        "trailing_four_quarters_a_year_earlier": ttm_prior,
        "balances_now": at_now,
        "balances_a_year_earlier": at_year_ago,
        "debt_now": total_debt(record, now),
        "debt_a_year_earlier": total_debt(record, year_ago) if year_ago else
        {"missing": "no period a year earlier is on record"},
        "cash_and_short_term_investments_now": cash_and_short_term_investments(record, now),
        "cash_flow_families": families,
        "diluted_shares": record.term("diluted_shares", diluted_span),
        "shares_outstanding": record.term("shares_outstanding", now),
    }


def ebit(terms: dict) -> dict:
    """Operating income, or pretax income plus interest where no operating line is filed."""
    ttm = terms["trailing_four_quarters"]
    if "missing" not in ttm["operating_income"]:
        return dict(ttm["operating_income"], basis="operating_income")
    if "missing" in ttm["pretax_income"] or "missing" in ttm["interest_expense"]:
        return {"missing": f"operating income: {ttm['operating_income']['missing']}; and "
                           f"pretax income plus interest expense cannot stand in for it"}
    return {"value": ttm["pretax_income"]["value"] + ttm["interest_expense"]["value"],
            "formula": "pretax_income + interest_expense",
            "basis": "pretax income plus interest expense, because the record carries no "
                     "operating income line for this period",
            "parts": {"pretax_income": ttm["pretax_income"],
                      "interest_expense": ttm["interest_expense"]}}


def tax_rate(terms: dict) -> dict:
    """The effective rate over the trailing four quarters, held between 0 and statutory."""
    ttm = terms["trailing_four_quarters"]
    tax, pretax = ttm["income_tax_expense"], ttm["pretax_income"]
    for cell in (tax, pretax):
        if "missing" in cell:
            return {"missing": cell["missing"]}
    raw = None if pretax["value"] <= 0 else tax["value"] / pretax["value"]
    if raw is None:
        rate, why = 0.0, "pretax income is not positive, so no rate is defined; held at 0"
    elif raw < 0:
        rate, why = 0.0, "the effective rate is negative; held at 0"
    elif raw > STATUTORY_TAX_RATE:
        rate, why = STATUTORY_TAX_RATE, "the effective rate is above statutory; held at 21%"
    else:
        rate, why = raw, "the effective rate, inside the bounds"
    return {"value": rate, "effective_rate": raw, "rule": why,
            "formula": "income_tax_expense / pretax_income, held between 0 and 0.21",
            "inputs": {"income_tax_expense": _brief(tax), "pretax_income": _brief(pretax)}}


def net_working_capital(balances: dict, debt_current: dict, cash: dict) -> dict:
    """Operating working capital: current assets less cash, less current liabilities less current debt."""
    return measure(
        "(current_assets - cash_and_short_term_investments) - "
        "(current_liabilities - debt_current)",
        {"current_assets": balances["current_assets"],
         "cash_and_short_term_investments": cash,
         "current_liabilities": balances["current_liabilities"],
         "debt_current": debt_current},
        lambda v: (v["current_assets"] - v["cash_and_short_term_investments"])
        - (v["current_liabilities"] - v["debt_current"]), unit="USD")


def ratios(record: Record, terms: dict, periods: dict) -> dict:
    ttm = terms["trailing_four_quarters"]
    now, ago = terms["balances_now"], terms["balances_a_year_earlier"]
    avg = {name: average(now[name], ago[name]) for name in now}
    op = ebit(terms)
    tax = tax_rate(terms)
    cash_now = terms["cash_and_short_term_investments_now"]
    debt = terms["debt_now"]
    ebitda = measure("ebit + depreciation_and_amortization",
                     {"ebit": op, "depreciation_and_amortization": ttm["depreciation_and_amortization"]},
                     lambda v: v["ebit"] + v["depreciation_and_amortization"], unit="USD")

    profitability = {
        "gross_margin": measure("(revenue - cost_of_revenue) / revenue",
                                {"revenue": ttm["revenue"], "cost_of_revenue": ttm["cost_of_revenue"]},
                                lambda v: (v["revenue"] - v["cost_of_revenue"]) / v["revenue"],
                                denominator="revenue"),
        "operating_margin": measure("ebit / revenue", {"ebit": op, "revenue": ttm["revenue"]},
                                    lambda v: v["ebit"] / v["revenue"], denominator="revenue"),
        "net_margin": measure("net_income / revenue",
                              {"net_income": ttm["net_income"], "revenue": ttm["revenue"]},
                              lambda v: v["net_income"] / v["revenue"], denominator="revenue"),
        "return_on_assets": measure("net_income / average assets",
                                    {"net_income": ttm["net_income"], "average_assets": avg["assets"]},
                                    lambda v: v["net_income"] / v["average_assets"]),
        "return_on_equity": measure("net_income / average stockholders_equity",
                                    {"net_income": ttm["net_income"],
                                     "average_equity": avg["stockholders_equity"]},
                                    lambda v: v["net_income"] / v["average_equity"]),
    }
    profitability["dupont"] = {
        "net_margin": profitability["net_margin"],
        "asset_turnover": measure("revenue / average assets",
                                  {"revenue": ttm["revenue"], "average_assets": avg["assets"]},
                                  lambda v: v["revenue"] / v["average_assets"]),
        "equity_multiplier": measure("average assets / average stockholders_equity",
                                     {"average_assets": avg["assets"],
                                      "average_equity": avg["stockholders_equity"]},
                                     lambda v: v["average_assets"] / v["average_equity"]),
    }
    dupont = profitability["dupont"]
    if all("value" in dupont[k] for k in ("net_margin", "asset_turnover", "equity_multiplier")):
        dupont["product"] = {"value": dupont["net_margin"]["value"] * dupont["asset_turnover"]["value"]
                             * dupont["equity_multiplier"]["value"],
                             "formula": "net_margin * asset_turnover * equity_multiplier, "
                                        "which is return_on_equity by construction"}
    invested_now = measure(
        "debt + stockholders_equity + operating_lease_liability - cash_and_short_term_investments",
        {"debt": debt, "stockholders_equity": now["stockholders_equity"],
         "operating_lease_liability": record.latest_balance("operating_lease_liability",
                                                            periods["balance_now"]),
         "cash_and_short_term_investments": cash_now},
        lambda v: v["debt"] + v["stockholders_equity"] + v["operating_lease_liability"]
        - v["cash_and_short_term_investments"], unit="USD")
    profitability["return_on_invested_capital"] = measure(
        "ebit * (1 - tax_rate) / invested_capital",
        {"ebit": op, "tax_rate": tax, "invested_capital": invested_now},
        lambda v: v["ebit"] * (1 - v["tax_rate"]) / v["invested_capital"],
        denominator="invested_capital")
    profitability["return_on_invested_capital"]["invested_capital"] = invested_now

    days = DAYS_IN_YEAR
    dso = measure("average receivables / revenue * 365",
                  {"average_receivables": avg["receivables"], "revenue": ttm["revenue"]},
                  lambda v: v["average_receivables"] / v["revenue"] * days, unit="days",
                  denominator="revenue")
    dsi = measure("average inventory / cost_of_revenue * 365",
                  {"average_inventory": avg["inventory"], "cost_of_revenue": ttm["cost_of_revenue"]},
                  lambda v: v["average_inventory"] / v["cost_of_revenue"] * days, unit="days",
                  denominator="cost_of_revenue")
    dpo = measure("average accounts_payable / cost_of_revenue * 365",
                  {"average_payables": avg["accounts_payable"], "cost_of_revenue": ttm["cost_of_revenue"]},
                  lambda v: v["average_payables"] / v["cost_of_revenue"] * days, unit="days",
                  denominator="cost_of_revenue")
    efficiency = {
        "days_sales_outstanding": dso, "days_sales_of_inventory": dsi,
        "days_payables_outstanding": dpo,
        "cash_conversion_cycle": measure(
            "days_sales_outstanding + days_sales_of_inventory - days_payables_outstanding",
            {"days_sales_outstanding": dso, "days_sales_of_inventory": dsi,
             "days_payables_outstanding": dpo},
            lambda v: v["days_sales_outstanding"] + v["days_sales_of_inventory"]
            - v["days_payables_outstanding"], unit="days"),
        "asset_turnover": dupont["asset_turnover"],
    }

    free_simple = measure("operating_cash_flow - capital_expenditure",
                          {"operating_cash_flow": ttm["operating_cash_flow"],
                           "capital_expenditure": ttm["capital_expenditure"]},
                          lambda v: v["operating_cash_flow"] - v["capital_expenditure"], unit="USD")
    runway = runway_months(cash_now, free_simple)
    liquidity = {
        "current_ratio": measure("current_assets / current_liabilities",
                                 {"current_assets": now["current_assets"],
                                  "current_liabilities": now["current_liabilities"]},
                                 lambda v: v["current_assets"] / v["current_liabilities"],
                                 denominator="current_liabilities"),
        "quick_ratio": measure("(cash_and_short_term_investments + receivables) / current_liabilities",
                               {"cash_and_short_term_investments": cash_now,
                                "receivables": now["receivables"],
                                "current_liabilities": now["current_liabilities"]},
                               lambda v: (v["cash_and_short_term_investments"] + v["receivables"])
                               / v["current_liabilities"], denominator="current_liabilities"),
        "cash_runway_months": runway,
    }
    solvency = {
        "total_debt": debt,
        "net_debt": measure("total_debt - cash_and_short_term_investments",
                            {"total_debt": debt, "cash_and_short_term_investments": cash_now},
                            lambda v: v["total_debt"] - v["cash_and_short_term_investments"],
                            unit="USD"),
        "ebitda": ebitda,
        "debt_over_ebitda": measure("total_debt / ebitda", {"total_debt": debt, "ebitda": ebitda},
                                    lambda v: v["total_debt"] / v["ebitda"], denominator="ebitda"),
        "interest_coverage": measure("ebit / interest_expense",
                                     {"ebit": op, "interest_expense": ttm["interest_expense"]},
                                     lambda v: v["ebit"] / v["interest_expense"],
                                     denominator="interest_expense"),
        "liabilities_over_assets": measure("total_liabilities / assets",
                                           {"total_liabilities": now["total_liabilities"],
                                            "assets": now["assets"]},
                                           lambda v: v["total_liabilities"] / v["assets"]),
        "operating_lease_liability": record.latest_balance("operating_lease_liability",
                                                           periods["balance_now"]),
    }
    return {"profitability": profitability, "efficiency": efficiency, "liquidity": liquidity,
            "solvency": solvency, "growth": growth(record, terms, periods),
            "ebit": op, "tax_rate": tax, "free_cash_flow_simple": free_simple}


# The trend table's reason for a term the record tags in no period at all.
NEVER_TAGGED = "in any period"


def _or_absent(cell: dict) -> dict:
    """A line the company never states at all -- a software company's inventory --
    reads as none, and says so. A line it states in other periods but not in
    this one stays missing: that is a gap, not an absence."""
    if "missing" in cell and NEVER_TAGGED in cell["missing"]:
        return {"value": 0.0, "note": f"no line in any filing on record: {cell['missing']}"}
    return cell


def runway_months(cash: dict, free_cash_flow: dict) -> dict:
    """Months of cash at the trailing burn, when there is a burn."""
    if "missing" in cash or "missing" in free_cash_flow:
        return {"missing": (cash.get("missing") or free_cash_flow.get("missing"))}
    if free_cash_flow["value"] >= 0:
        return {"value": None, "not_burning_cash": True,
                "formula": "cash_and_short_term_investments / (-free_cash_flow_simple / 12)",
                "reason": "free cash flow over the trailing four quarters is not negative, "
                          "so there is no burn to divide by"}
    burn = -free_cash_flow["value"] / 12
    return {"value": cash["value"] / burn, "unit": "months",
            "formula": "cash_and_short_term_investments / (-free_cash_flow_simple / 12)",
            "inputs": {"cash_and_short_term_investments": _brief(cash),
                       "free_cash_flow_simple": _brief(free_cash_flow)}}


def growth(record: Record, terms: dict, periods: dict) -> dict:
    spans = durations(record.usd)
    end = _date(periods["balance_now"])
    out = {}
    for term in ("revenue", "operating_income", "net_income", "operating_cash_flow"):
        this = quarter(record, term, spans, end)
        last = quarter(record, term, spans, end - dt.timedelta(days=QUARTER_STEP))
        year_ago = quarter(record, term, spans, end - dt.timedelta(days=YEAR_STEP))
        now_ttm = terms["trailing_four_quarters"][term]
        prior_ttm = terms["trailing_four_quarters_a_year_earlier"][term]
        out[term] = {
            "quarter_over_quarter": _growth(this, last),
            "year_over_year": _growth(this, year_ago),
            "trailing_four_quarters": _growth(now_ttm, prior_ttm),
            "this_quarter": this,
        }
    return out


def _growth(now: dict, before: dict) -> dict:
    return measure("(now - before) / abs(before)",
                   {"now": now, "before": before},
                   lambda v: (v["now"] - v["before"]) / abs(v["before"]), denominator="before")


# --- earnings against cash ----------------------------------------------------------

def earnings_versus_cash(record: Record, terms: dict, periods: dict) -> dict:
    """Area 1's numbers: cash over income, accruals, working capital, smoothness, history."""
    ttm = terms["trailing_four_quarters"]
    now, ago = terms["balances_now"], terms["balances_a_year_earlier"]
    out = {
        "operating_cash_flow_over_net_income": measure(
            "operating_cash_flow / net_income",
            {"operating_cash_flow": ttm["operating_cash_flow"], "net_income": ttm["net_income"]},
            lambda v: v["operating_cash_flow"] / v["net_income"], denominator="net_income"),
        "accruals_over_average_assets": measure(
            "(net_income - operating_cash_flow) / average assets",
            {"net_income": ttm["net_income"], "operating_cash_flow": ttm["operating_cash_flow"],
             "average_assets": average(now["assets"], ago["assets"])},
            lambda v: (v["net_income"] - v["operating_cash_flow"]) / v["average_assets"]),
    }
    absorbed = {}
    for balance, flow, sign in (("receivables", "change_in_receivables", "asset"),
                                ("inventory", "change_in_inventory", "asset"),
                                ("accounts_payable", "change_in_payables", "liability")):
        change = measure(f"{balance} now - {balance} a year earlier",
                         {"now": now[balance], "a_year_earlier": ago[balance]},
                         lambda v: v["now"] - v["a_year_earlier"], unit="USD")
        stated = ttm[flow]
        gap = measure(f"balance-sheet change in {balance} - cash-flow statement's change",
                      {"balance_sheet_change": change, "cash_flow_statement_change": stated},
                      lambda v: v["balance_sheet_change"] - v["cash_flow_statement_change"],
                      unit="USD")
        absorbed[balance] = {
            "balance_sheet_change": change,
            "cash_flow_statement_change": stated,
            "articulation_gap": gap,
            "share_of_net_income": measure(
                f"balance-sheet change in {balance} / net_income",
                {"change": change, "net_income": ttm["net_income"]},
                lambda v: v["change"] / v["net_income"], denominator="net_income"),
            "note": ("an increase in an asset absorbs cash and an increase in a liability "
                     "supplies it; the statement's own line is the increase in the balance "
                     "as the taxonomy defines it"),
        }
    out["working_capital"] = absorbed
    out["smoothness"] = smoothness(record, periods)
    out["history"] = annual_history(record, periods)
    return out


def smoothness(record: Record, periods: dict) -> dict:
    """Is income smoother than cash? Standard deviation of quarterly changes, eight quarters."""
    spans = durations(record.usd)
    end = _date(periods["balance_now"])
    income, cash, used = [], [], []
    for back in range(9):
        when = end - dt.timedelta(days=QUARTER_STEP * back)
        one = quarter(record, "net_income", spans, when)
        two = quarter(record, "operating_cash_flow", spans, when)
        if "missing" in one or "missing" in two:
            break
        income.append(one["value"])
        cash.append(two["value"])
        used.append(one.get("end"))
    if len(income) < 5:
        return {"missing": f"{len(income)} consecutive quarters of net income and operating "
                           f"cash flow are on record, and the comparison needs five"}
    d_income = [a - b for a, b in zip(income, income[1:])]
    d_cash = [a - b for a, b in zip(cash, cash[1:])]
    spread_cash = statistics.pstdev(d_cash)
    if spread_cash == 0:
        return {"missing": "operating cash flow did not change across the quarters"}
    return {"value": statistics.pstdev(d_income) / spread_cash,
            "formula": "population standard deviation of quarter-to-quarter changes in net "
                       "income / the same for operating cash flow; below 1 means income "
                       "moves less than cash",
            "quarters_read": used, "net_income": income, "operating_cash_flow": cash}


def annual_history(record: Record, periods: dict) -> dict:
    """Each of the last fiscal years on record: the figures the analysts compare against."""
    rows = []
    for span in periods["fiscal_years"]:
        get = {term: record.term(term, span) for term in
               ("revenue", "operating_income", "net_income", "operating_cash_flow",
                "capital_expenditure", "share_based_compensation")}
        row = {"fiscal_year": f"{span[0]}..{span[1]}"}
        for term, cell in get.items():
            row[term] = cell.get("value") if "missing" not in cell else None
            if "id" in cell:
                row[f"{term}_id"] = cell["id"]
        if row["revenue"] and row["operating_income"] is not None:
            row["operating_margin"] = row["operating_income"] / row["revenue"]
        if row["net_income"] and row["operating_cash_flow"] is not None:
            row["operating_cash_flow_over_net_income"] = row["operating_cash_flow"] / row["net_income"]
        if row["operating_cash_flow"] is not None and row["capital_expenditure"] is not None:
            row["free_cash_flow_simple"] = row["operating_cash_flow"] - row["capital_expenditure"]
        rows.append(row)
    for newer, older in zip(rows, rows[1:]):
        if newer["revenue"] is not None and older["revenue"]:
            newer["revenue_growth"] = newer["revenue"] / older["revenue"] - 1
    out = {"years": rows}
    if len(rows) >= 4 and rows[0]["revenue"] and rows[3]["revenue"] and rows[3]["revenue"] > 0:
        out["revenue_growth_three_year_compound"] = (rows[0]["revenue"] / rows[3]["revenue"]) ** (1 / 3) - 1
        out["revenue_growth_three_year_compound_formula"] = (
            "(revenue of the newest fiscal year / revenue three fiscal years earlier) ** (1/3) - 1")
    margins = [row["operating_margin"] for row in rows[:3] if "operating_margin" in row]
    if len(margins) == 3:
        out["operating_margin_three_year_average"] = sum(margins) / 3
    return out


# --- the four free-cash-flow measures -------------------------------------------------

def free_cash_flows(terms: dict, sections: dict, adjustments: list | None,
                    fields: dict) -> dict:
    ttm = terms["trailing_four_quarters"]
    now, ago = terms["balances_now"], terms["balances_a_year_earlier"]
    families = terms["cash_flow_families"]
    simple = sections["free_cash_flow_simple"]
    op, tax = sections["ebit"], sections["tax_rate"]

    # The change in working capital is the trade working capital's: receivables
    # plus inventory less payables. The broad measure -- current assets less
    # cash and short-term investments, less current liabilities other than debt
    # -- is printed beside it and not used, because it counts every financial
    # asset a company files under current assets as operating capital: NVIDIA's
    # 10-Q for the quarter ended 2026-07-26 carries 42,783 million of
    # marketable equity securities there, and no tag says which securities are
    # current in general, so the broad change would move by what the company
    # invested rather than what its operations absorbed.
    trade_now = trade_working_capital(now)
    trade_ago = trade_working_capital(ago)
    delta_nwc = measure("trade_working_capital now - trade_working_capital a year earlier",
                        {"now": trade_now, "a_year_earlier": trade_ago},
                        lambda v: v["now"] - v["a_year_earlier"], unit="USD")
    to_firm = measure(
        "ebit * (1 - tax_rate) + depreciation_and_amortization - capital_expenditure "
        "- change_in_trade_working_capital",
        {"ebit": op, "tax_rate": tax,
         "depreciation_and_amortization": ttm["depreciation_and_amortization"],
         "capital_expenditure": ttm["capital_expenditure"],
         "change_in_trade_working_capital": delta_nwc},
        lambda v: v["ebit"] * (1 - v["tax_rate"]) + v["depreciation_and_amortization"]
        - v["capital_expenditure"] - v["change_in_trade_working_capital"], unit="USD")
    to_firm["trade_working_capital"] = {"now": trade_now, "a_year_earlier": trade_ago}
    nwc_now = net_working_capital(now, terms["debt_now"].get("parts", {}).get("debt_current")
                                  or {"missing": terms["debt_now"].get("missing", "no debt")},
                                  terms["cash_and_short_term_investments_now"])
    nwc_ago = net_working_capital(ago, terms["debt_a_year_earlier"].get("parts", {}).get("debt_current")
                                  or {"missing": terms["debt_a_year_earlier"].get("missing", "no debt")},
                                  cash_and_short_term_investments_from(ago))
    to_firm["net_working_capital_broad_not_used"] = {
        "now": nwc_now, "a_year_earlier": nwc_ago,
        "why_not_used": "counts any financial asset filed under current assets -- marketable "
                        "equity securities, for one -- as operating capital"}

    borrowing = {name: families[name] for name in
                 ("borrowing_issued", "borrowing_repaid", "borrowing_short_term_net")}
    missing = [f"{name}: {cell['missing']}" for name, cell in borrowing.items() if "missing" in cell]
    if missing or "missing" in simple:
        to_equity = {"missing": "; ".join(missing) or simple.get("missing"),
                     "formula": "operating_cash_flow - capital_expenditure + net_borrowing"}
    else:
        net_borrowing = sum(family_cash_effect(cell) for cell in borrowing.values())
        to_equity = {"value": simple["value"] + net_borrowing,
                     "formula": "operating_cash_flow - capital_expenditure + net_borrowing",
                     "unit": "USD", "net_borrowing": net_borrowing,
                     "inputs": {"free_cash_flow_simple": simple["value"],
                                **{name: {"cash_effect": family_cash_effect(cell),
                                          "formula": cell.get("formula"),
                                          "note": cell.get("note")}
                                   for name, cell in borrowing.items()}}}

    quality = quality_adjusted(simple, ttm["share_based_compensation"], families["acquisitions"],
                               adjustments, fields)
    return {"free_cash_flow_simple": simple, "free_cash_flow_to_firm": to_firm,
            "free_cash_flow_to_equity": to_equity, "free_cash_flow_quality_adjusted": quality}


def trade_working_capital(balances: dict) -> dict:
    """Receivables plus inventory less accounts payable, at one balance date.

    A company that states no inventory line -- a software company -- has none,
    and the line is read as absent and named; receivables and payables are
    required.
    """
    return measure("receivables + inventory - accounts_payable",
                   {"receivables": balances["receivables"],
                    "inventory": _or_absent(balances["inventory"]),
                    "accounts_payable": balances["accounts_payable"]},
                   lambda v: v["receivables"] + v["inventory"] - v["accounts_payable"],
                   unit="USD")


def cash_and_short_term_investments_from(balances: dict) -> dict:
    cash = balances["cash"]
    if "missing" in cash:
        return cash
    investments = balances["short_term_investments"]
    if "missing" in investments:
        return {"value": cash["value"], "formula": "cash", "parts": {"cash": cash}}
    return {"value": cash["value"] + investments["value"],
            "formula": "cash + short_term_investments",
            "parts": {"cash": cash, "short_term_investments": investments}}


def quality_adjusted(simple: dict, compensation: dict, acquisitions: dict,
                     adjustments: list | None, fields: dict) -> dict:
    """Simple FCF less share-based pay less acquisitions, then the analyst's adjustments.

    The analyst names each adjustment's direction and the calculator field whose
    value is its amount; this function reads the amount and applies it, and
    records what each one moved. An adjustment naming a field that is not a
    number in `calculator.json` is refused and listed, never guessed at.
    """
    formula = ("free_cash_flow_simple - share_based_compensation - acquisitions "
               "- (each reducing adjustment) + (each increasing adjustment)")
    if "missing" in simple:
        return {"missing": f"free cash flow: {simple['missing']}", "formula": formula}
    if "missing" in compensation:
        return {"missing": f"share_based_compensation: {compensation['missing']}", "formula": formula}
    if "missing" in acquisitions:
        return {"missing": f"acquisitions: {acquisitions['missing']}", "formula": formula}
    acquired = -family_cash_effect(acquisitions)          # cash spent on acquisitions
    value = simple["value"] - compensation["value"] - acquired
    applied, refused = [], []
    for position, item in enumerate(adjustments or []):
        field = item.get("calculator_field")
        direction = item.get("direction")
        amount = adjustment_amount(fields, field)
        if direction not in ("reduce", "increase") or amount is None:
            refused.append({"position": position, "name": item.get("name"),
                            "calculator_field": field, "direction": direction,
                            "reason": ("direction is not 'reduce' or 'increase'"
                                       if direction not in ("reduce", "increase") else
                                       f"{field!r} is not a dollar amount under "
                                       f"{' or '.join(ADJUSTMENT_ROOTS)}")})
            continue
        before = value
        value = value - abs(amount) if direction == "reduce" else value + abs(amount)
        applied.append({"name": item.get("name"), "calculator_field": field,
                        "direction": direction, "amount": abs(amount),
                        "before": before, "after": value, "quote": item.get("quote")})
    return {"value": value, "formula": formula, "unit": "USD",
            "inputs": {"free_cash_flow_simple": simple["value"],
                       "share_based_compensation": _brief(compensation),
                       "acquisitions": {"cash_spent": acquired,
                                        "formula": acquisitions.get("formula"),
                                        "note": acquisitions.get("note")}},
            "adjustments_applied": applied, "adjustments_refused": refused,
            "rule": "an adjustment's amount is the absolute value of the field it names; "
                    "its direction is the analyst's"}


# Where an adjustment's amount may come from: a dollar cell of the terms or of the
# earnings-versus-cash section. A ratio or a count of days named as an amount
# would be subtracted from free cash flow as though it were dollars.
ADJUSTMENT_ROOTS = ("terms.", "earnings_versus_cash.")


def adjustment_amount(fields: dict, path) -> float | None:
    """The dollar amount at a path an adjustment names, or None. One rule, read by
    the analysis gate and by the calculator alike."""
    if not isinstance(path, str) or not path.startswith(ADJUSTMENT_ROOTS):
        return None
    node = fields
    for part in path.split("."):
        if isinstance(node, dict) and part in node:
            node = node[part]
        elif isinstance(node, list) and part.isdigit() and int(part) < len(node):
            node = node[int(part)]
        else:
            return None
    if not isinstance(node, dict) or node.get("unit") != "USD":
        return None
    return field_value(fields, path)


def field_value(fields: dict, path: str | None) -> float | None:
    """The number at a dotted path of calculator.json, or None."""
    if not path or not isinstance(path, str):
        return None
    node = fields
    for part in path.split("."):
        if isinstance(node, dict) and part in node:
            node = node[part]
        elif isinstance(node, list) and part.isdigit() and int(part) < len(node):
            node = node[int(part)]
        else:
            return None
    if isinstance(node, dict):
        node = node.get("value")
    if isinstance(node, bool) or not isinstance(node, (int, float)):
        return None
    return float(node) if math.isfinite(node) else None


# --- the cost of capital ----------------------------------------------------------------

def _verified(entry: dict, directory: Path) -> bytes:
    raw = (directory / entry["path"]).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != entry["sha256"]:
        raise CalculatorInputError(
            f"{entry['path']} hashes to {digest}, not the {entry['sha256']} its manifest "
            f"recorded -- refused, because the file is no longer what was published")
    return raw


def risk_free_rate(cutoff: dt.date) -> dict:
    directory = COST_OF_CAPITAL          # the committed inputs, and no path a caller hands in
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    entry = manifest["risk_free_rate"]
    raw = _verified(entry, directory)
    best = None
    for row in list(csv.reader(raw.decode("utf-8").splitlines()))[1:]:
        if len(row) != 2 or row[1].strip() in ("", "."):
            continue
        day = _date(row[0])
        if day <= cutoff and (best is None or day > best[0]):
            best = (day, float(row[1]) / 100)
    if best is None:
        return {"missing": f"no DGS10 observation on or before {cutoff} is committed"}
    # The file's own name and URL carry the date it was fetched to, which is later
    # than most cutoffs, so the citation names the manifest entry and the hash.
    return {"value": best[1], "date": best[0].isoformat(), "series": entry["series"],
            "source": "src/cost_of_capital/manifest.json, risk_free_rate",
            "sha256": entry["sha256"]}


def _xlsx_rows(raw: bytes) -> tuple[list[list], bool]:
    """The first worksheet's cells as rows of values, and whether dates count from 1904."""
    with zipfile.ZipFile(__import__("io").BytesIO(raw)) as book:
        shared = [re.sub(r"<[^>]+>", "", item) for item in
                  re.findall(r"<si>(.*?)</si>", book.read("xl/sharedStrings.xml").decode(), re.S)]
        from_1904 = 'date1904="1"' in book.read("xl/workbook.xml").decode()
        sheet = book.read("xl/worksheets/sheet1.xml").decode()
    rows = []
    for body in re.findall(r"<row [^>]*>(.*?)</row>", sheet, re.S):
        cells = {}
        for ref, attrs, inner in re.findall(r'<c r="([A-Z]+)\d+"([^>]*)>(.*?)</c>', body, re.S):
            value = re.search(r"<v>([^<]*)</v>", inner)
            if value is None:
                continue
            text = value.group(1)
            cells[ref] = shared[int(text)] if 't="s"' in attrs else text
        rows.append(cells)
    return rows, from_1904


# The header of the premium column, by the words that end it: the workbook
# spells it with the trailing-twelve-month abbreviation, and no other column's
# header ends this way.
PREMIUM_HEADER_ENDS = "with sustainable payout)"


def equity_risk_premium(cutoff: dt.date) -> dict:
    directory = COST_OF_CAPITAL          # the committed inputs, and no path a caller hands in
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    entry = manifest["equity_risk_premium"]
    raw = _verified(entry, directory)
    rows, from_1904 = _xlsx_rows(raw)
    header = rows[0]
    column = next((ref for ref, text in header.items()
                   if re.sub(r"\s+", " ", text).strip().endswith(PREMIUM_HEADER_ENDS)), None)
    date_column = next((ref for ref, text in header.items() if text.strip() == "Start of month"), None)
    if column is None or date_column is None:
        raise CalculatorInputError("the workbook has no premium column ending "
                                   f"{PREMIUM_HEADER_ENDS!r} or no 'Start of month' "
                                   "column -- its layout changed")
    epoch = dt.date(1904, 1, 1) if from_1904 else dt.date(1899, 12, 30)
    best = None
    for row in rows[1:]:
        if date_column not in row or column not in row:
            continue
        try:
            day = epoch + dt.timedelta(days=int(float(row[date_column])))
            premium = float(row[column])
        except ValueError:
            continue
        if day < cutoff and (best is None or day > best[0]):
            best = (day, premium)
    if best is None:
        return {"missing": f"no implied premium dated before {cutoff} is in the workbook"}
    return {"value": best[1], "month_start": best[0].isoformat(), "column": entry["column"],
            "source": "src/cost_of_capital/manifest.json, equity_risk_premium",
            "sha256": entry["sha256"], "rule": entry["rule"]}


NO_PRICES = ("no price series was given: the forward track's price source is Tiingo, "
             "and without its token no series is fetched")


def market_inputs(ticker: str, cutoff: dt.date, prices: Path | None) -> dict:
    """Price at the cutoff, and beta over the 250 trading days before it."""
    if prices is None:
        return {"missing": NO_PRICES}
    try:
        series = market.read_prices(prices)
    except market.MarketError as exc:
        return {"missing": f"the price series could not be read: {exc}"}
    broad = market.broad_market_symbol()
    if ticker not in series or broad not in series:
        return {"missing": f"the price directory needs {ticker}.csv and {broad}.csv; it holds "
                           f"{sorted(series)}"}
    calendar = market.trading_calendar(series, broad)
    try:
        window = market.estimation_window(calendar, cutoff)
        slope = market.beta(market.daily_returns(series[ticker]),
                            market.daily_returns(series[broad]), window)
    except market.MarketError as exc:
        return {"missing": f"beta: {exc}"}
    close = raw_close(prices / f"{ticker}.csv", cutoff)
    if "missing" in close:
        return close
    return {"beta": {"value": slope, "window_first": window[0].isoformat(),
                     "window_last": window[-1].isoformat(), "trading_days": len(window),
                     "against": broad,
                     "formula": "covariance of daily adjusted-close returns / variance of the "
                                "market's, over the 250 trading days before the cutoff"},
            "price": close}


def raw_close(path: Path, cutoff: dt.date) -> dict:
    """The unadjusted close on the last trading day on or before the cutoff."""
    reader = csv.DictReader(path.read_text(encoding="utf-8").splitlines())
    if "close" not in (reader.fieldnames or ()):
        return {"missing": f"{path.name} has no unadjusted close column"}
    best = None
    for row in reader:
        day = _date(row["date"])
        if day <= cutoff and (best is None or day > best[0]):
            best = (day, float(row["close"]))
    if best is None:
        return {"missing": f"no close on or before {cutoff} in {path.name}"}
    return {"value": best[1], "date": best[0].isoformat(), "unit": "USD per share",
            "source": path.name}


def cost_of_capital(terms: dict, sections: dict, market_data: dict, cutoff: dt.date,
                    overrides: dict | None) -> dict:
    ttm = terms["trailing_four_quarters"]
    rf, erp = risk_free_rate(cutoff), equity_risk_premium(cutoff)
    tax = sections["tax_rate"]
    debt_now, debt_ago = terms["debt_now"], terms["debt_a_year_earlier"]
    shares = terms["shares_outstanding"]
    out = {"risk_free_rate": rf, "equity_risk_premium": erp, "tax_rate": tax}
    overrides = overrides or {}

    if "missing" in debt_now:
        cost_of_debt = {"missing": debt_now["missing"]}
    elif debt_now["value"] == 0 and ("missing" in debt_ago or debt_ago["value"] == 0):
        cost_of_debt = {"value": 0.0, "note": "no debt on the balance sheet, so it carries no weight"}
    else:
        cost_of_debt = measure("interest_expense / average debt",
                               {"interest_expense": ttm["interest_expense"],
                                "average_debt": average(debt_now, debt_ago)},
                               lambda v: v["interest_expense"] / v["average_debt"],
                               denominator="average_debt")
    if "pre_tax_cost_of_debt" in overrides:
        chosen = overrides["pre_tax_cost_of_debt"]
        if isinstance(chosen.get("value"), (int, float)) and chosen.get("quote"):
            cost_of_debt = {"value": float(chosen["value"]),
                            "chosen_by": "the valuation analyst",
                            "reason": chosen.get("reason"), "quote": chosen.get("quote"),
                            "computed": cost_of_debt}
    out["pre_tax_cost_of_debt"] = cost_of_debt

    if "missing" in market_data:
        out["beta"] = {"missing": market_data["missing"]}
        out["market_value_of_equity"] = {"missing": market_data["missing"]}
        out["cost_of_equity"] = {"missing": market_data["missing"]}
        out["value"] = None
        out["missing"] = f"the cost of equity needs a beta and a price: {market_data['missing']}"
        return out
    beta = market_data["beta"]
    price = market_data["price"]
    out["beta"] = beta
    out["price_at_cutoff"] = price
    equity_value = measure("price_at_cutoff * shares_outstanding",
                           {"price_at_cutoff": price, "shares_outstanding": shares},
                           lambda v: v["price_at_cutoff"] * v["shares_outstanding"], unit="USD")
    out["market_value_of_equity"] = equity_value
    cost_of_equity = measure("risk_free_rate + beta * equity_risk_premium",
                             {"risk_free_rate": rf, "beta": beta, "equity_risk_premium": erp},
                             lambda v: v["risk_free_rate"] + v["beta"] * v["equity_risk_premium"])
    out["cost_of_equity"] = cost_of_equity
    wacc = measure(
        "E/(D+E) * cost_of_equity + D/(D+E) * pre_tax_cost_of_debt * (1 - tax_rate)",
        {"E": equity_value, "D": debt_now, "cost_of_equity": cost_of_equity,
         "pre_tax_cost_of_debt": cost_of_debt, "tax_rate": tax},
        lambda v: (v["E"] / (v["D"] + v["E"]) * v["cost_of_equity"]
                   + v["D"] / (v["D"] + v["E"]) * v["pre_tax_cost_of_debt"] * (1 - v["tax_rate"])))
    out["weights"] = ({"equity": equity_value["value"] / (equity_value["value"] + debt_now["value"]),
                       "debt": debt_now["value"] / (equity_value["value"] + debt_now["value"])}
                      if "value" in equity_value and "value" in debt_now else None)
    out["wacc"] = wacc
    out["value"] = wacc.get("value")
    if "missing" in wacc:
        out["missing"] = wacc["missing"]
    return out


# --- the DCF --------------------------------------------------------------------------

SCENARIOS = ("bear", "base", "bull")
DRIVERS = ("revenue_growth_year_one", "terminal_growth", "operating_margin_year_one",
           "operating_margin_year_ten", "reinvestment_rate_year_one",
           "reinvestment_rate_year_ten")


def linear(first: float, last: float, years: int = FORECAST_YEARS) -> list[float]:
    """`years` values from `first` to `last` in equal steps, both ends included."""
    return [first + (last - first) * t / (years - 1) for t in range(years)]


def forecast(base_revenue: float, drivers: dict, tax: float, wacc: float, *,
             growth_path: list[float] | None = None) -> dict:
    """Ten years of free cash flow to the firm, a terminal value, and their present value."""
    growth_path = growth_path or linear(drivers["revenue_growth_year_one"],
                                        drivers["terminal_growth"])
    margins = linear(drivers["operating_margin_year_one"], drivers["operating_margin_year_ten"])
    reinvest = linear(drivers["reinvestment_rate_year_one"], drivers["reinvestment_rate_year_ten"])
    terminal = drivers["terminal_growth"]
    if wacc <= terminal:
        raise CalculatorInputError(f"WACC {wacc} is not above terminal growth {terminal}, so the "
                                   f"terminal value is not defined")
    years, revenue, present = [], base_revenue, 0.0
    for t in range(FORECAST_YEARS):
        revenue = revenue * (1 + growth_path[t])
        nopat = revenue * margins[t] * (1 - tax)
        cash = nopat * (1 - reinvest[t])
        factor = (1 + wacc) ** (t + 1)
        present += cash / factor
        years.append({"year": t + 1, "revenue_growth": growth_path[t], "revenue": revenue,
                      "operating_margin": margins[t], "nopat": nopat,
                      "reinvestment_rate": reinvest[t], "free_cash_flow_to_firm": cash,
                      "discount_factor": 1 / factor, "present_value": cash / factor})
    terminal_cash = years[-1]["free_cash_flow_to_firm"] * (1 + terminal)
    terminal_value = terminal_cash / (wacc - terminal)
    terminal_present = terminal_value / (1 + wacc) ** FORECAST_YEARS
    return {"years": years, "terminal_free_cash_flow": terminal_cash,
            "terminal_value": terminal_value, "terminal_value_present": terminal_present,
            "explicit_present": present, "enterprise_value": present + terminal_present}


def bridge(enterprise_value: float, net_debt: float, leases: float, shares: float) -> dict:
    equity = enterprise_value - net_debt - leases
    return {"enterprise_value": enterprise_value, "net_debt": net_debt,
            "operating_lease_liability": leases, "equity_value": equity,
            "diluted_shares": shares, "value_per_share": equity / shares,
            "formula": "(enterprise_value - net_debt - operating_lease_liability) / diluted_shares"}


def _drivers(scenario: dict, rf: float) -> dict:
    missing = [name for name in DRIVERS if not isinstance(scenario.get(name), (int, float))]
    if missing:
        raise CalculatorInputError(f"the scenario names no {', '.join(missing)}; Python never "
                                   f"invents a driver")
    drivers = {name: float(scenario[name]) for name in DRIVERS}
    if drivers["terminal_growth"] > rf:
        raise CalculatorInputError(
            f"terminal growth {drivers['terminal_growth']} is above the risk-free rate {rf}, "
            f"which the owner's rule does not allow")
    return drivers


def valuation(terms: dict, sections: dict, capital: dict, assumptions: dict | None,
              adjustments_moved: dict | None = None) -> dict:
    if assumptions is None:
        return {"missing": "no assumptions.json: the valuation analyst has not written drivers "
                           "yet, and Python never invents one"}
    if capital.get("value") is None:
        return {"missing": f"WACC is not computed: {capital.get('missing')}"}
    ttm = terms["trailing_four_quarters"]
    solvency = sections["solvency"]
    needed = {"revenue": ttm["revenue"], "net_debt": solvency["net_debt"],
              "diluted_shares": terms["diluted_shares"], "tax_rate": sections["tax_rate"]}
    for name, cell in needed.items():
        if "missing" in cell:
            return {"missing": f"{name}: {cell['missing']}"}
    leases = solvency["operating_lease_liability"]
    if "missing" in leases:
        return {"missing": f"operating_lease_liability: {leases['missing']}"}
    wacc, rf = capital["value"], capital["risk_free_rate"]["value"]
    tax = sections["tax_rate"]["value"]
    base_revenue = ttm["revenue"]["value"]
    out = {"base_revenue": base_revenue, "wacc": wacc, "tax_rate": tax,
           "risk_free_rate_cap_on_terminal_growth": rf, "scenarios": {},
           "conventions": "end-of-year discounting; growth fades linearly from year one to "
                          "the terminal rate at year ten; margin and reinvestment move "
                          "linearly from year one to year ten; terminal value is year ten's "
                          "free cash flow grown once at the terminal rate, over WACC less "
                          "that rate"}
    price = capital.get("price_at_cutoff", {}).get("value")
    scenarios = assumptions.get("scenarios") or {}
    for name in SCENARIOS:
        if name not in scenarios:
            out["scenarios"][name] = {"missing": f"assumptions.json has no {name} scenario"}
            continue
        try:
            drivers = _drivers(scenarios[name], rf)
            run = forecast(base_revenue, drivers, tax, wacc)
        except CalculatorInputError as exc:
            out["scenarios"][name] = {"missing": str(exc)}
            continue
        run["drivers"] = drivers
        run.update(bridge(run["enterprise_value"], solvency["net_debt"]["value"],
                          leases["value"], terms["diluted_shares"]["value"]))
        out["scenarios"][name] = run
    values = [out["scenarios"][n]["value_per_share"] for n in SCENARIOS
              if "value_per_share" in out["scenarios"][n]]
    if values:
        out["value_range_per_share"] = {"low": min(values), "high": max(values)}
    if price is not None:
        out["price_at_cutoff"] = price
        if values:
            low, high = min(values), max(values)
            out["price_position"] = ("below the range" if price < low else
                                     "above the range" if price > high else "inside the range")
    base = out["scenarios"].get("base", {})
    if "drivers" in base:
        out["reverse_dcf"] = reverse_dcf(base_revenue, base["drivers"], tax, wacc,
                                         solvency["net_debt"]["value"], leases["value"],
                                         terms["diluted_shares"]["value"], price)
        out["sensitivity"] = sensitivity(base_revenue, base["drivers"], tax, wacc, rf,
                                         solvency["net_debt"]["value"], leases["value"],
                                         terms["diluted_shares"]["value"])
        if adjustments_moved:
            out["accounting_adjustments"] = adjusted_value(
                base_revenue, base["drivers"], tax, wacc, solvency["net_debt"]["value"],
                leases["value"], terms["diluted_shares"]["value"], base["value_per_share"],
                adjustments_moved, ttm)
    else:
        out["reverse_dcf"] = {"missing": "no base scenario"}
        out["sensitivity"] = {"missing": "no base scenario"}
    return out


def per_share(base_revenue, drivers, tax, wacc, net_debt, leases, shares, *, growth_path=None):
    run = forecast(base_revenue, drivers, tax, wacc, growth_path=growth_path)
    return bridge(run["enterprise_value"], net_debt, leases, shares)["value_per_share"]


def reverse_dcf(base_revenue, drivers, tax, wacc, net_debt, leases, shares, price) -> dict:
    """The constant ten-year revenue growth at which the base case is worth the price."""
    if price is None:
        return {"missing": "no price at the cutoff"}

    def gap(growth: float) -> float:
        return per_share(base_revenue, drivers, tax, wacc, net_debt, leases, shares,
                         growth_path=[growth] * FORECAST_YEARS) - price

    low, high = REVERSE_BRACKET
    at_low, at_high = gap(low), gap(high)
    if at_low > 0 or at_high < 0:
        return {"missing": f"no constant growth between {low} and {high} gives the price: "
                           f"value less price is {at_low} at {low} and {at_high} at {high}",
                "held": "base margins, base reinvestment, base terminal growth"}
    for _ in range(REVERSE_ITERATIONS):
        middle = (low + high) / 2
        if gap(middle) > 0:
            high = middle
        else:
            low = middle
        if high - low < REVERSE_TOLERANCE:
            break
    return {"value": (low + high) / 2, "price": price,
            "held": "base margins, base reinvestment, base terminal growth",
            "formula": "the constant revenue growth g for years one to ten at which the base "
                       "case per-share value equals the price, found by bisection"}


def sensitivity(base_revenue, drivers, tax, wacc, rf, net_debt, leases, shares) -> dict:
    grid = []
    for step_w in SENSITIVITY_WACC_STEPS:
        row = []
        for step_g in SENSITIVITY_GROWTH_STEPS:
            w, g = wacc + step_w, drivers["terminal_growth"] + step_g
            cell = {"wacc": w, "terminal_growth": g}
            if w <= g:
                cell["missing"] = "WACC is not above terminal growth"
            else:
                moved = dict(drivers, terminal_growth=g)
                cell["value_per_share"] = per_share(base_revenue, moved, tax, w, net_debt,
                                                    leases, shares)
                if g > rf:
                    cell["above_risk_free"] = True
            row.append(cell)
        grid.append(row)
    return {"rows": "WACC -1 point, as is, +1 point", "columns":
            "terminal growth -0.5 point, as is, +0.5 point", "grid": grid}


def adjusted_value(base_revenue, drivers, tax, wacc, net_debt, leases, shares, base_value,
                   moved: dict, ttm: dict) -> dict:
    """How much the accounting analyst's adjustments move the base value.

    An adjustment is one-time unless the analyst marks it `recurs`: a
    receivables build or a reserve release happened once, and it moves value
    once -- by its amount, over diluted shares, with no discounting because it
    is already in the past. Only an adjustment the analyst marks as recurring,
    with a quote saying why, is carried into every forecast year, by one of two
    stated mechanisms: an earnings adjustment lowers the operating margin by its
    amount over trailing revenue; a cash-flow adjustment raises the reinvestment
    rate by its amount over trailing after-tax operating income. Each is applied
    alone and then all together, and the per-share change is printed for each.
    """
    revenue = ttm["revenue"]["value"]
    rows, margin_cut, reinvest_add, once = [], 0.0, 0.0, 0.0
    nopat = moved.get("nopat")
    for item in moved.get("applied", []):
        amount = item["amount"] if item["direction"] == "reduce" else -item["amount"]
        target = item.get("applies_to", "cash_flow")
        if not item.get("recurs"):
            once += amount
            rows.append({"name": item["name"], "applies_to": target, "recurs": False,
                         "mechanism": "one-time: value lowered by the amount over diluted shares",
                         "value_per_share": base_value - amount / shares,
                         "moved_per_share": -amount / shares})
            continue
        one = dict(drivers)
        if target == "earnings":
            cut = amount / revenue
            one["operating_margin_year_one"] -= cut
            one["operating_margin_year_ten"] -= cut
            margin_cut += cut
            how = f"recurring: operating margin lowered by {cut} in every year"
        else:
            if not nopat:
                rows.append({"name": item["name"], "missing": "after-tax operating income is "
                             "not computed, so a recurring cash-flow adjustment cannot be "
                             "expressed as reinvestment"})
                continue
            add = amount / nopat
            one["reinvestment_rate_year_one"] += add
            one["reinvestment_rate_year_ten"] += add
            reinvest_add += add
            how = f"recurring: reinvestment rate raised by {add} in every year"
        value = per_share(base_revenue, one, tax, wacc, net_debt, leases, shares)
        rows.append({"name": item["name"], "applies_to": target, "recurs": True,
                     "mechanism": how, "value_per_share": value,
                     "moved_per_share": value - base_value})
    together = dict(drivers)
    together["operating_margin_year_one"] -= margin_cut
    together["operating_margin_year_ten"] -= margin_cut
    together["reinvestment_rate_year_one"] += reinvest_add
    together["reinvestment_rate_year_ten"] += reinvest_add
    value = per_share(base_revenue, together, tax, wacc, net_debt, leases, shares) - once / shares
    return {"each": rows, "all_together": {"value_per_share": value,
                                           "moved_per_share": value - base_value},
            "base_value_per_share": base_value}


# --- the triggering filing's own facts, where companyfacts has not caught up ---------------

FILING_UNITS = {"iso4217:USD": "USD", "shares": "shares"}


def supplemented(document: dict, bundle: Path | None,
                 cutoff: dt.date | None = None) -> tuple[dict, list[str]]:
    """The record, plus the filing's own entity-wide facts for any filing it lacks.

    SEC's companyfacts can lag a filing by months: on 2026-09-28 it still held
    nothing Carrier or Littelfuse filed after the spring, though both had filed
    a 10-Q in July. The bundle carries each filing's XBRL instance as
    `input_numbers.json`, read through the gate, so for an accession the record
    does not name at all, its facts with no dimension are added as rows of the
    same shape -- same concept, period, value, accession and filing date --
    and the accessions added are listed in the output. A filing the record
    already carries is never touched: its rows are the record's.
    """
    if bundle is None:
        return document, []
    try:
        numbers = json.loads(cutoff_guard.load_bundle_file(bundle, "input_numbers.json"))
    except cutoff_guard.CutoffGuardError:
        return document, []
    known = {row.get("accn") for concepts in (document.get("facts") or {}).values()
             for concept in concepts.values() for rows in concept.get("units", {}).values()
             for row in rows}
    facts = copy_facts(document.get("facts") or {})
    added = set()
    for fact in numbers.get("facts", []):
        context = fact.get("context") or {}
        unit = FILING_UNITS.get(fact.get("unit"))
        accession = fact.get("source_accession")
        if (context.get("segment") or context.get("typed_segment") or unit is None
                or fact.get("prefix") not in ("us-gaap", "dei") or accession in known
                or fact.get("nil") or not isinstance(fact.get("number"), (int, float))):
            continue
        # The bundle's reader is ungated by design, so the cutoff is applied here,
        # to the row, as the catalogue route applies it to companyfacts.
        if cutoff is not None and (not fact.get("filing_date") or cutoff_guard.parse_date(
                fact["filing_date"], "filing_date") > cutoff):
            continue
        row = {"start": context.get("start"), "end": context.get("end") or context.get("instant"),
               "val": fact["number"], "accn": accession, "form": fact.get("form"),
               "filed": fact.get("filing_date"), "from_the_filing": fact.get("id")}
        if row["start"] is None:
            del row["start"]
        facts.setdefault(fact["prefix"], {}).setdefault(fact["tag"], {"units": {}}) \
            .setdefault("units", {}).setdefault(unit, []).append(row)
        added.add(accession)
    return dict(document, facts=facts), sorted(added)


def copy_facts(facts: dict) -> dict:
    return {namespace: {tag: {**concept, "units": {unit: list(rows) for unit, rows
                                                   in concept.get("units", {}).items()}}
                        for tag, concept in concepts.items()}
            for namespace, concepts in facts.items()}


# --- concentration, from the triggering filing -------------------------------------------

def concentration(bundle: Path | None) -> dict:
    """Every ConcentrationRiskPercentage1 fact the filing states, with its axes."""
    if bundle is None:
        return {"missing": "no run bundle was given, so the filing's own facts were not read"}
    try:
        numbers = json.loads(cutoff_guard.load_bundle_file(bundle, "input_numbers.json"))
    except cutoff_guard.CutoffGuardError as exc:
        return {"missing": str(exc)}
    rows = []
    for fact in numbers.get("facts", []):
        if fact.get("tag") != "ConcentrationRiskPercentage1" or fact.get("superseded_by"):
            continue
        axes = {item["dimension"]: item["member"] for item in
                (fact.get("context") or {}).get("segment") or []}
        rows.append({"id": fact["id"], "value": fact.get("number"),
                     "start": fact["context"].get("start"), "end": fact["context"].get("end"),
                     "axes": axes})
    return {"facts": sorted(rows, key=lambda row: (row["end"] or "", row["id"])),
            "note": "percentages as the filing states them, 0.25 meaning a quarter; "
                    "facts a later filing in the bundle superseded are left out"}


# --- the trend table, carried -------------------------------------------------------------

def trend_values(document: dict, cutoff: dt.date, period_end: str) -> dict:
    """Every ratio the trend table computes, value and place in history only."""
    table = trends.trends(document, cutoff, period_end=period_end)
    out = {}
    for row in table["quarters"] + table["years"]:
        cells = {}
        for name, cell in row["ratios"].items():
            if "value" in cell:
                cells[name] = {"value": cell["value"], "formula": cell["formula"],
                               "position_in_history": cell.get("position_in_history")}
            else:
                cells[name] = {"missing": cell.get("missing")}
        out[row["label"]] = {"start": row.get("start"), "end": row.get("end"), "ratios": cells}
    return out


# --- the whole file ---------------------------------------------------------------------

def calculate(*, ticker: str, cutoff, period_end: str, form: str, accession: str | None = None,
              fixtures_root=cutoff_guard.FIXTURES, bundle: Path | None = None,
              market_data: dict | None = None, assumptions: dict | None = None,
              accounting: dict | None = None) -> dict:
    """The whole file. `market_data` is what `market_inputs` read from a price
    directory; the caller reads it, so this function opens no path it is handed
    other than through the gate."""
    cutoff = cutoff_guard.parse_date(cutoff, "cutoff")
    document, from_the_filing = supplemented(
        trends.read_record(ticker, cutoff, fixtures_root=fixtures_root), bundle, cutoff)
    record = Record(document)
    periods = trigger_periods(record.usd, period_end, form)
    terms = gather(record, periods)
    sections = ratios(record, terms, periods)
    # The paths an adjustment names are paths into calculator.json as it is written
    # -- `terms.trailing_four_quarters....`, `earnings_versus_cash....` -- so the
    # fields it is read from have that shape, and a path the gate admitted against
    # the analyst's file is the path this reads.
    earnings = earnings_versus_cash(record, terms, periods)
    fields = {"terms": terms, "earnings_versus_cash": earnings,
              "ratios": {key: sections[key] for key in ("profitability", "efficiency",
                                                        "liquidity", "solvency", "growth")},
              "ebit": sections["ebit"], "tax_rate": sections["tax_rate"]}
    adjustments = (accounting or {}).get("adjustments")
    free = free_cash_flows(terms, sections, adjustments, fields)
    if market_data is None:
        market_data = {"missing": NO_PRICES}
    capital = cost_of_capital(terms, sections, market_data, cutoff,
                              (assumptions or {}).get("wacc_overrides"))
    moved = None
    quality = free["free_cash_flow_quality_adjusted"]
    if quality.get("adjustments_applied"):
        by_name = {item.get("name"): item for item in adjustments or []}
        op, tax = sections["ebit"], sections["tax_rate"]
        nopat = (op["value"] * (1 - tax["value"])
                 if "value" in op and "value" in tax else None)
        moved = {"applied": [dict(item, applies_to=by_name.get(item["name"], {})
                                  .get("applies_to", "cash_flow"),
                                  recurs=by_name.get(item["name"], {}).get("recurs") is True)
                             for item in quality["adjustments_applied"]],
                 "nopat": nopat}
    value = valuation(terms, sections, capital, assumptions, moved)

    missing = [f"{term}: {terms['trailing_four_quarters'][term]['missing']}"
               for term in CORE_TERMS if term in terms["trailing_four_quarters"]
               and "missing" in terms["trailing_four_quarters"][term]]
    for term in CORE_TERMS:
        if term in terms["balances_now"] and "missing" in terms["balances_now"][term]:
            missing.append(f"{term}: {terms['balances_now'][term]['missing']}")
    if "missing" in terms["diluted_shares"]:
        missing.append(f"diluted_shares: {terms['diluted_shares']['missing']}")
    for name in ("free_cash_flow_simple", "free_cash_flow_to_firm",
                 "free_cash_flow_to_equity", "free_cash_flow_quality_adjusted"):
        if "missing" in free[name]:
            missing.append(f"{name}: {free[name]['missing']}")
    if capital.get("value") is None:
        missing.append(f"wacc: {capital.get('missing')}")
    if "missing" in value:
        missing.append(f"valuation: {value['missing']}")

    return {
        "ticker": ticker, "accession": accession, "form": form,
        "cutoff": cutoff.isoformat(), "period_end": period_end,
        "missing": missing,
        "read_from_the_filing_because_companyfacts_lagged": from_the_filing,
        "what_this_is": ("every number the three analysts may cite, computed in Python from "
                         "the as-filed companyfacts rows at the cutoff; each value names its "
                         "formula and each input names its row id"),
        "periods": {key: (list(value) if isinstance(value, tuple) else
                          value.isoformat() if isinstance(value, dt.date) else value)
                    for key, value in periods.items() if key != "fiscal_years"}
        | {"fiscal_years": [list(span) for span in periods["fiscal_years"]]},
        "terms": terms,
        "ratios": {key: sections[key] for key in ("profitability", "efficiency", "liquidity",
                                                  "solvency", "growth")},
        "ebit": sections["ebit"], "tax_rate": sections["tax_rate"],
        "earnings_versus_cash": earnings,
        "free_cash_flow": free,
        "concentration": concentration(bundle),
        "trend_table": trend_values(document, cutoff, period_end),
        "trend_table_note": ("computed on the same record as every figure above, which for "
                             "an accession listed under "
                             "read_from_the_filing_because_companyfacts_lagged includes that "
                             "filing's own facts; the run's input_trends.json is computed on "
                             "companyfacts alone and can hold fewer periods"),
        "market": market_data,
        "cost_of_capital": capital,
        "valuation": value,
    }


# What the accounting and financial analysts may not see: every figure read off a
# price. `CLAUDE.md` -- they "see reports and calculator.json, never prices; the
# valuation analyst adds ... the price at the cutoff". So they are handed this
# view, and the valuation analyst the whole file.
PRICED_SECTIONS = ("market", "cost_of_capital", "valuation")
FILINGS_ONLY = "calculator_filings_only.json"


def filings_only(payload: dict) -> dict:
    """calculator.json with every section that reads a price removed, and checked.

    Refuses rather than trims if a price is still anywhere in what is left, so a
    new section that carries one cannot reach an analyst who may not see it.
    """
    out = {key: value for key, value in payload.items() if key not in PRICED_SECTIONS}
    out["sections_removed_for_this_view"] = list(PRICED_SECTIONS)
    out["missing"] = [line for line in payload.get("missing", [])
                      if not line.startswith(("wacc:", "valuation:"))]
    text = json.dumps(out)
    for word in ("price_at_cutoff", '"price"', "market_value_of_equity", '"beta"'):
        if word in text:
            raise CalculatorInputError(f"the filings-only view still carries {word}")
    return out


def read_json(path: str | None) -> dict | None:
    """An agent's written file, which is not a filing and not a bundle input."""
    return json.loads(Path(path).read_text(encoding="utf-8")) if path else None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="calculator.json for one filing")
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--cutoff", required=True)
    parser.add_argument("--period-end", required=True)
    parser.add_argument("--form", required=True, choices=["10-K", "10-Q"])
    parser.add_argument("--accession", default=None)
    parser.add_argument("--fixtures", default=str(cutoff_guard.FIXTURES))
    parser.add_argument("--bundle", default=None)
    parser.add_argument("--prices", default=None)
    parser.add_argument("--assumptions", default=None)
    parser.add_argument("--adjustments", default=None,
                        help="analysis_accounting.json, whose `adjustments` are applied")
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    code = interpreter_pin.enforce()
    if code:
        return code
    assumptions = read_json(args.assumptions)
    accounting = read_json(args.adjustments)
    try:
        prices = market_inputs(args.ticker, cutoff_guard.parse_date(args.cutoff, "cutoff"),
                               Path(args.prices) if args.prices else None)
        payload = calculate(
            ticker=args.ticker, cutoff=args.cutoff, period_end=args.period_end,
            form=args.form, accession=args.accession, fixtures_root=Path(args.fixtures),
            bundle=Path(args.bundle) if args.bundle else None,
            market_data=prices, assumptions=assumptions, accounting=accounting)
    except (CalculatorInputError, cutoff_guard.CutoffGuardError,
            trends.TrendInputError) as exc:
        print(f"calculator: {exc}", file=sys.stderr)
        return BAD_INPUT
    Path(args.out).write_text(json.dumps(payload, indent=1, sort_keys=False) + "\n",
                              encoding="utf-8")
    Path(args.out).with_name(FILINGS_ONLY).write_text(
        json.dumps(filings_only(payload), indent=1) + "\n", encoding="utf-8")
    for line in payload["missing"]:
        print(f"calculator: NOT COMPUTED -- {line}", file=sys.stderr)
    return INCOMPLETE if payload["missing"] else 0


if __name__ == "__main__":
    sys.exit(main())
