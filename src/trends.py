"""The trend table. Python does every division on this page.

The input is `input_numbers.json` and nothing else — the file the reader also
has — so that a ratio in `input_trends.json` can be recomputed by hand from the
fact ids it names. Each ratio carries its formula, the fact id and tag behind
every term, and the period it was compared against. Nothing here is rounded,
smoothed, interpolated or carried forward.

**What is left out, and why it is named instead of filled.** The fixture set is
one 10-K and two 10-Qs per company, and `input_numbers.json` holds the 10-K and
the current 10-Q. Between them they carry three fiscal years and two quarters,
not five years and eight quarters. The missing periods are listed one by one in
`coverage` with the reason, because a trend table that quietly reports the six
periods it happens to have looks the same as one that had all thirteen.

The non-GAAP gap is missing for a different reason and says so: `Revenues` is a
us-gaap concept and "adjusted net income" is not, so a non-GAAP measure is never
in `input_numbers.json`, which carries us-gaap and dei facts only. It comes off
the 8-K exhibit, which is a different file.

**The rules that decide which fact is the fact**, all of them mechanical:
consolidated only (a fact with a segment is a slice, not the company); a fact a
later filing superseded is skipped; a duration of 80–100 days is a quarter and
one of 350–380 days is a year (a 52/53-week filer's quarters are 91 days and a
YTD period is not a quarter); a balance-sheet instant belongs to the period
whose end date it equals exactly.

    python3.12 -m src.extract_numbers --ticker AAPL --out input_numbers.json
    python3.12 -m src.trends --numbers input_numbers.json --out input_trends.json
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

try:
    from src import interpreter_pin
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import interpreter_pin

BAD_INPUT = 2

QUARTERS_REQUESTED = 8
YEARS_REQUESTED = 5
QUARTER_DAYS = (80, 100)
YEAR_DAYS = (350, 380)
QUARTER_STEP = 91          # a 52/53-week quarter, in days
YEAR_STEP = 364            # thirteen of them
TOLERANCE_DAYS = 20        # how far a fiscal period end may sit from the step

# Which us-gaap tags may stand for each term, best first. A term is filled by
# the first tag in the list that the filing actually reports; the output names
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

# docs/INPUT_SPEC.md §4 item 1, in the order the spec lists them.
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

NO_NON_GAAP = ("no us-gaap concept carries a non-GAAP measure, and "
               "input_numbers.json holds us-gaap and dei facts only")


class TrendInputError(Exception):
    """The numbers file is not the shape this reads."""


def _date(value: str) -> dt.date:
    return dt.date.fromisoformat(value)


def usable(fact: dict) -> bool:
    """Consolidated, reported, still current, and a number."""
    if fact.get("nil") or fact.get("number") is None:
        return False
    if fact.get("superseded_by"):
        return False
    context = fact.get("context") or {}
    return not context.get("segment")


def periods(facts: list[dict], kind: str) -> list[dict]:
    """Every distinct duration of the requested length, newest first."""
    low, high = QUARTER_DAYS if kind == "quarter" else YEAR_DAYS
    found: dict[tuple[str, str], dict] = {}
    for fact in facts:
        if not usable(fact):
            continue
        context = fact["context"]
        start, end = context.get("start"), context.get("end")
        if not start or not end:
            continue
        days = (_date(end) - _date(start)).days + 1
        if not low <= days <= high:
            continue
        found[(start, end)] = {"start": start, "end": end, "days": days}
    return sorted(found.values(), key=lambda p: (p["end"], p["start"]), reverse=True)


def pick_fact(facts: list[dict], term: str, period: dict) -> dict | None:
    """The one fact behind a term for one period, by the rules in the docstring."""
    period_type, tags = CONCEPTS[term]
    for tag in tags:
        matches = []
        for fact in facts:
            if fact["tag"] != tag or fact["prefix"] != "us-gaap" or not usable(fact):
                continue
            context = fact["context"]
            if period_type == "duration":
                if context.get("start") == period["start"] and \
                        context.get("end") == period["end"]:
                    matches.append(fact)
            elif context.get("instant") == period["end"]:
                matches.append(fact)
        if matches:
            # A filing may repeat a fact; the latest filing wins, then the id,
            # so the choice does not depend on the order of the file.
            matches.sort(key=lambda f: (f["filing_date"], f["source_accession"], f["id"]))
            return matches[-1]
    return None


def why_missing(facts: list[dict], term: str, period: dict) -> str:
    """Which of the three ways this term is not here — the reader's next step
    differs for each: a tag nobody filed, a tag filed only by segment, or a tag
    filed for other periods."""
    tags = CONCEPTS[term][1]
    if not tags:
        return f"no fact for {term}: {NO_NON_GAAP}"
    named = ", ".join(f"us-gaap:{tag}" for tag in tags)
    anywhere = [fact for fact in facts
                if fact["tag"] in tags and fact["prefix"] == "us-gaap"]
    if not anywhere:
        return f"no fact for {term}: the filings tag none of {named}"
    if not any(usable(fact) for fact in anywhere):
        return (f"no fact for {term}: {named} is reported only by segment, or nil, "
                f"or superseded — never as a consolidated total")
    return (f"no fact for {term} in {period['start']}..{period['end']}: "
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
                        "value": fact["number"], "unit": fact["unit"]}
        values[term] = fact["number"]
    written, of = DENOMINATORS[name]
    if of(values) == 0:
        return {"missing": f"{written} is zero in {period['start']}..{period['end']}"}
    return {"value": spec["value"](values, period["days"]),
            "formula": spec["formula"], "inputs": inputs}


def requested(available: list[dict], count: int, step: int) -> list[dict]:
    """The `count` consecutive fiscal periods ending at the newest one.

    Labelled by how far back they are, resolved to a real period when one ends
    within `TOLERANCE_DAYS` of where the step says it should. A period with no
    match is not dropped — it is returned with the date that was looked for.
    """
    if not available:
        return [{"index": index, "period": None,
                 "reason": "no period of this length is in input_numbers.json"}
                for index in range(count)]
    anchor = _date(available[0]["end"])
    taken: set[tuple[str, str]] = set()
    out = []
    for index in range(count):
        target = anchor - dt.timedelta(days=step * index)
        best, best_gap = None, None
        for period in available:
            key = (period["start"], period["end"])
            if key in taken:
                continue
            gap = abs((_date(period["end"]) - target).days)
            if gap <= TOLERANCE_DAYS and (best_gap is None or gap < best_gap):
                best, best_gap = period, gap
        if best is None:
            out.append({"index": index, "period": None, "target_end": target.isoformat(),
                        "reason": f"no period ending within {TOLERANCE_DAYS} days of "
                                  f"{target.isoformat()} is in input_numbers.json"})
        else:
            taken.add((best["start"], best["end"]))
            out.append({"index": index, "period": best, "target_end": target.isoformat()})
    return out


def _label(prefix: str, index: int) -> str:
    return f"{prefix}-{index}"


def _series(facts: list[dict], slots: list[dict], prefix: str) -> list[dict]:
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
                     "ratios": {name: ratio(facts, name, period) for name in RATIOS}})
    return rows


def _change(rows: list[dict], index: int, back: int, name: str, kind: str) -> dict:
    """This period's ratio minus the one `back` periods earlier."""
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

    return {
        "requested": {"quarters": QUARTERS_REQUESTED, "years": YEARS_REQUESTED},
        "quarters": period_rows(quarters),
        "years": period_rows(years),
        "ratios": by_ratio,
    }


def trends(numbers: dict) -> dict:
    """The whole table, from the parsed `input_numbers.json`."""
    for key in ("ticker", "facts"):
        if key not in numbers:
            raise TrendInputError(f"input_numbers.json has no {key!r}")
    facts = numbers["facts"]
    quarters = _series(facts, requested(periods(facts, "quarter"),
                                        QUARTERS_REQUESTED, QUARTER_STEP), "Q")
    years = _series(facts, requested(periods(facts, "year"),
                                     YEARS_REQUESTED, YEAR_STEP), "FY")
    add_changes(quarters, years)
    return {
        "ticker": numbers["ticker"],
        "cutoff": numbers.get("cutoff"),
        "source": {"documents": numbers.get("documents", []),
                   "facts": len(facts),
                   "facts_used": sum(1 for fact in facts if usable(fact))},
        "quarters": quarters,
        "years": years,
        "coverage": coverage(quarters, years),
    }


def render(payload: dict) -> str:
    """Deterministic by construction: sorted keys, no clock, no set iteration."""
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="the trend table, from input_numbers.json")
    parser.add_argument("--numbers", required=True, help="path to input_numbers.json")
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)

    try:
        numbers = json.loads(Path(args.numbers).read_text(encoding="utf-8"))
        payload = trends(numbers)
    except (OSError, ValueError, TrendInputError) as exc:
        print(f"trends: {exc}", file=sys.stderr)
        return BAD_INPUT
    Path(args.out).write_text(render(payload), encoding="utf-8")
    filled = sum(1 for row in payload["quarters"] + payload["years"] if row["filled"])
    print(f"trends: {payload['ticker']} {filled} of "
          f"{QUARTERS_REQUESTED + YEARS_REQUESTED} periods filled → {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
