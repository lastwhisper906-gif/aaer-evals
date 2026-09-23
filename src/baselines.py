"""The formula baselines. Python does every division on this page.

`docs/CHECKLIST.md` §8 scores eight rows computed by Python beside the pipeline,
and this file writes the eight the task list names into `baselines.json`, one
object per scorecard row key:

    accounting   beneish_m_score, accruals_over_assets, net_operating_assets,
                 note_cosine_similarity, loughran_mcdonald_negative
    pressure     piotroski_f_score, ohlson_o_score, altman_z_score

`naive_forecast` and `short_interest_ratio` are scorecard rows too, and nothing
here writes them; `src/scorecard.py` already reads them as not on record.

Each row carries its value, the published formula it came from with the paper
and its coefficients named, every intermediate quantity, and for every term the
us-gaap tag, the accession and the filing date of the row it was taken from. A
row that cannot be computed carries `missing` and the reason, never a default:
a term the record does not carry is not a zero.

**Where the numbers come from.**

- *The financial statements*: the companyfacts record, read through
  `src/trends.py`'s `read_record` — `cutoff_guard.load_catalogue`, which drops
  every row filed after the cutoff — and re-counted here, so a record that still
  holds a late row is refused rather than trimmed. A term is picked out of the
  record by `trends.term_source`, the trend table's own rule: us-gaap, USD, the
  periodic statements only, the first tag in the term's list the record carries
  for that period, and the latest filing at or before the cutoff. The terms the
  trend table also reads are read under the trend table's own tag lists, so the
  two tables divide the same numbers.
- *The fiscal years*: the trend table's window rule. The current year is the
  newest fiscal year ending at or before the triggering report's period, the
  prior year the one before it, and the year two back supplies the balance
  sheet the prior year opened on. Every formula here is annual.
- *The notes*: `src/extract_notes.py` on the triggering report's XBRL instance
  and on the prior-period instance the fixture stores beside it, both through
  the date gate.
- *The price-level index* in the Ohlson O-score: the GNP implicit price
  deflator, committed under `src/price_level_index/` as ALFRED published it on
  two dates. A vintage is read only when it is dated at or before the cutoff —
  the same rule as a filing — and its bytes must still be the ones the manifest
  hashed.

**The cutoff** is the triggering report's own filing date, and the fiscal year
is anchored on its own period of report: both are read off the fixture manifest
row for that report, so there is no default to fall back to.

**What is not here, and why.**

- `loughran_mcdonald_negative` is `missing`. The Loughran and McDonald master
  dictionary is published as "free for use in academic research", with
  commercial licences on request and no grant to redistribute it, and this
  repository is public under Apache 2.0. The list is not committed, so there is
  no file to hash into the manifest and no share to compute from it.
  `docs/needs_judgment.md` carries the question.
- `altman_z_score` has no value until a caller hands it the market value of
  equity at the fiscal year end. Altman's fourth ratio is market value of equity
  over book value of total debt, no price is committed for these twelve, and the
  price backends answer unconfigured without a token. The four accounting ratios
  are computed and reported beside the reason.
- No row carries `market_direction.p_up`, which is what `src/scorecard.py`
  scores. None of these papers turns its score into a probability that the
  abnormal return is positive, and inventing that map would put a number on the
  page that no source gave. The scorecard reads the rows as not on record until
  a rule for that is decided.

    python3.12 -m src.baselines --ticker QCOM --form 10-Q --out baselines.json
"""

from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import hashlib
import json
import math
import re
import sys
from pathlib import Path

try:
    from src import cutoff_guard, extract_notes, interpreter_pin, trends
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import cutoff_guard, extract_notes, interpreter_pin, trends

BAD_INPUT = 2

CURRENT, PRIOR, TWO_BACK = "current_year", "prior_year", "two_years_back"
YEARS = (CURRENT, PRIOR, TWO_BACK)

# Which us-gaap tags may stand for each term, best first, read by the trend
# table's rule. The terms the trend table also reads are its own entries, so a
# ratio here and a ratio there divide the same row. `receivables` is the one
# term read differently, on purpose: the trend table's days-sales-outstanding
# reads trade receivables first, and Beneish's index is built on the
# receivables total the balance sheet states — Qualcomm's balance sheet line is
# `AccountsAndOtherReceivablesNetCurrent`, 4,315 million for fiscal 2025, where
# `AccountsReceivableNetCurrent` is a note's trade figure of 2,855.
SHARED = ("revenue", "cost_of_revenue", "net_income", "operating_cash_flow",
          "assets", "property_plant_and_equipment", "cash")
CONCEPTS: dict[str, tuple[str, tuple[str, ...]]] = {
    **{term: trends.CONCEPTS[term] for term in SHARED},
    "receivables": ("instant", (
        "ReceivablesNetCurrent", "AccountsAndOtherReceivablesNetCurrent",
        "AccountsReceivableNetCurrent")),
    "current_assets": ("instant", ("AssetsCurrent",)),
    "current_liabilities": ("instant", ("LiabilitiesCurrent",)),
    "total_liabilities": ("instant", ("Liabilities",)),
    "short_term_investments": ("instant", (
        "ShortTermInvestments", "MarketableSecuritiesCurrent",
        "AvailableForSaleSecuritiesDebtSecuritiesCurrent")),
    # Debt in current liabilities: short-term borrowings and the current
    # portion of long-term debt together, which is what us-gaap's DebtCurrent
    # is. Sloan subtracts it, and so do Hirshleifer and others.
    "debt_in_current_liabilities": ("instant", (
        "DebtCurrent", "LongTermDebtCurrent",
        "LongTermDebtAndCapitalLeaseObligationsCurrent")),
    # The current maturities of long-term debt alone, which is Beneish's term.
    "current_maturities_of_long_term_debt": ("instant", (
        "LongTermDebtCurrent", "LongTermDebtAndCapitalLeaseObligationsCurrent")),
    "income_taxes_payable": ("instant", (
        "AccruedIncomeTaxesCurrent", "TaxesPayableCurrent")),
    "long_term_debt": ("instant", (
        "LongTermDebtNoncurrent", "LongTermDebtAndCapitalLeaseObligations")),
    "retained_earnings": ("instant", ("RetainedEarningsAccumulatedDeficit",)),
    # Common equity, preferred stock and minority interest together, which is
    # what us-gaap's stockholders' equity including the noncontrolling interest
    # is: preferred stock sits inside stockholders' equity there.
    "total_equity": ("instant", (
        "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest",
        "StockholdersEquity")),
    "depreciation_and_amortization": ("duration", (
        "DepreciationDepletionAndAmortization", "DepreciationAndAmortization",
        "DepreciationAmortizationAndAccretionNet")),
    "selling_general_and_administrative": ("duration", (
        "SellingGeneralAndAdministrativeExpense",)),
    "pretax_income": ("duration", (
        "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItems"
        "NoncontrollingInterest",
        "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAnd"
        "IncomeLossFromEquityMethodInvestments")),
    "interest_expense": ("duration", ("InterestExpense", "InterestExpenseNonoperating")),
    "common_stock_issued": ("duration", (
        "ProceedsFromIssuanceOfCommonStock", "ProceedsFromStockPlans",
        "ProceedsFromIssuanceOfSharesUnderIncentiveAndShareBasedCompensation"
        "PlansIncludingStockOptions",
        "ProceedsFromStockOptionsExercised")),
}


class BaselineInputError(Exception):
    """An input is not there, not the shape this reads, or not allowed. Never a default."""


# --- the papers ---------------------------------------------------------------

BENEISH = {
    "source": ("Beneish, M. D. (1999). The Detection of Earnings Manipulation. "
               "Financial Analysts Journal 55(5): 24-36. The eight-variable "
               "unweighted probit model and the variable definitions of its "
               "appendix."),
    "coefficients": {
        "constant": -4.84,
        "days_sales_in_receivables_index": 0.920,
        "gross_margin_index": 0.528,
        "asset_quality_index": 0.404,
        "sales_growth_index": 0.892,
        "depreciation_index": 0.115,
        "sales_general_and_administrative_expenses_index": -0.172,
        "total_accruals_to_total_assets": 4.679,
        "leverage_index": -0.327,
    },
    "components": {
        "days_sales_in_receivables_index":
            "(receivables[t] / revenue[t]) / (receivables[t-1] / revenue[t-1])",
        "gross_margin_index":
            "((revenue[t-1] - cost_of_revenue[t-1]) / revenue[t-1]) "
            "/ ((revenue[t] - cost_of_revenue[t]) / revenue[t])",
        "asset_quality_index":
            "(1 - (current_assets[t] + property_plant_and_equipment[t]) / assets[t]) "
            "/ (1 - (current_assets[t-1] + property_plant_and_equipment[t-1]) / assets[t-1])",
        "sales_growth_index": "revenue[t] / revenue[t-1]",
        "depreciation_index":
            "(depreciation_and_amortization[t-1] / (depreciation_and_amortization[t-1] "
            "+ property_plant_and_equipment[t-1])) / (depreciation_and_amortization[t] "
            "/ (depreciation_and_amortization[t] + property_plant_and_equipment[t]))",
        "sales_general_and_administrative_expenses_index":
            "(selling_general_and_administrative[t] / revenue[t]) "
            "/ (selling_general_and_administrative[t-1] / revenue[t-1])",
        "total_accruals_to_total_assets":
            "((change in current_assets - change in cash) - (change in "
            "current_liabilities - change in current_maturities_of_long_term_debt "
            "- change in income_taxes_payable) - depreciation_and_amortization[t]) "
            "/ assets[t]",
        "leverage_index":
            "((current_liabilities[t] + long_term_debt[t]) / assets[t]) "
            "/ ((current_liabilities[t-1] + long_term_debt[t-1]) / assets[t-1])",
    },
    "formula": "constant + the sum over the eight components of coefficient * component",
}

SLOAN = {
    "source": ("Sloan, R. G. (1996). Do Stock Prices Fully Reflect Information in "
               "Accruals and Cash Flows about Future Earnings? The Accounting "
               "Review 71(3): 289-315. Accruals from the balance sheet, scaled "
               "by average total assets."),
    "formula": ("((change in current_assets - change in cash) - (change in "
                "current_liabilities - change in debt_in_current_liabilities - "
                "change in income_taxes_payable) - depreciation_and_amortization[t]) "
                "/ ((assets[t] + assets[t-1]) / 2)"),
}

HIRSHLEIFER = {
    "source": ("Hirshleifer, D., Hou, K., Teoh, S. H. and Zhang, Y. (2004). Do "
               "investors overvalue firms with bloated balance sheets? Journal of "
               "Accounting and Economics 38: 297-331. Net operating assets over "
               "lagged total assets."),
    "components": {
        "operating_assets": "assets[t] - (cash[t] + short_term_investments[t])",
        "operating_liabilities":
            "assets[t] - debt_in_current_liabilities[t] - long_term_debt[t] "
            "- total_equity[t]",
    },
    "formula": "(operating_assets - operating_liabilities) / assets[t-1]",
}

PIOTROSKI = {
    "source": ("Piotroski, J. D. (2000). Value Investing: The Use of Historical "
               "Financial Statement Information to Separate Winners from Losers. "
               "Journal of Accounting Research 38 (Supplement): 1-41. Nine binary "
               "signals, each one when the condition holds and zero otherwise."),
    "signals": {
        "return_on_assets_positive": "net_income[t] / assets[t-1] > 0",
        "operating_cash_flow_positive": "operating_cash_flow[t] / assets[t-1] > 0",
        "return_on_assets_rose":
            "net_income[t] / assets[t-1] - net_income[t-1] / assets[t-2] > 0",
        "cash_flow_exceeds_return_on_assets":
            "operating_cash_flow[t] / assets[t-1] > net_income[t] / assets[t-1]",
        "leverage_fell":
            "long_term_debt[t] / ((assets[t] + assets[t-1]) / 2) "
            "- long_term_debt[t-1] / ((assets[t-1] + assets[t-2]) / 2) < 0",
        "current_ratio_rose":
            "current_assets[t] / current_liabilities[t] "
            "- current_assets[t-1] / current_liabilities[t-1] > 0",
        "no_common_equity_issued": "common_stock_issued[t] == 0",
        "gross_margin_rose":
            "(revenue[t] - cost_of_revenue[t]) / revenue[t] "
            "- (revenue[t-1] - cost_of_revenue[t-1]) / revenue[t-1] > 0",
        "asset_turnover_rose":
            "revenue[t] / assets[t-1] - revenue[t-1] / assets[t-2] > 0",
    },
    "formula": "the sum of the nine signals",
}

OHLSON = {
    "source": ("Ohlson, J. A. (1980). Financial Ratios and the Probabilistic "
               "Prediction of Bankruptcy. Journal of Accounting Research 18(1): "
               "109-131. Model 1, the one-year model. Size is the log of total "
               "assets over the GNP price-level index, the index at 100 for 1968, "
               "total assets as reported in dollars, and the index year the year "
               "before the year of the balance sheet date."),
    "coefficients": {
        "constant": -1.32,
        "size": -0.407,
        "total_liabilities_over_total_assets": 6.03,
        "working_capital_over_total_assets": -1.43,
        "current_liabilities_over_current_assets": 0.0757,
        "liabilities_exceed_assets": -1.72,
        "net_income_over_total_assets": -2.37,
        "funds_from_operations_over_total_liabilities": -1.83,
        "net_loss_in_both_years": 0.285,
        "change_in_net_income": -0.521,
    },
    "components": {
        "size": "ln(assets[t] / price_level_index), the index at 100 for 1968",
        "total_liabilities_over_total_assets": "total_liabilities[t] / assets[t]",
        "working_capital_over_total_assets":
            "(current_assets[t] - current_liabilities[t]) / assets[t]",
        "current_liabilities_over_current_assets":
            "current_liabilities[t] / current_assets[t]",
        "liabilities_exceed_assets": "1 if total_liabilities[t] > assets[t], else 0",
        "net_income_over_total_assets": "net_income[t] / assets[t]",
        "funds_from_operations_over_total_liabilities":
            "operating_cash_flow[t] / total_liabilities[t]",
        "net_loss_in_both_years": "1 if net_income[t] < 0 and net_income[t-1] < 0, else 0",
        "change_in_net_income":
            "(net_income[t] - net_income[t-1]) / (|net_income[t]| + |net_income[t-1]|)",
    },
    "formula": "constant + the sum over the nine components of coefficient * component",
    # Funds provided by operations was the working-capital statement's line;
    # the cash flow statement replaced that statement in 1988, and its
    # operating total is what is read.
    "reading": ("funds from operations is read as net cash provided by operating "
                "activities; the log is the natural log"),
}

ALTMAN = {
    "source": ("Altman, E. I. (1968). Financial Ratios, Discriminant Analysis and "
               "the Prediction of Corporate Bankruptcy. Journal of Finance 23(4): "
               "589-609. The discriminant function as the paper prints it, "
               "Z = .012X1 + .014X2 + .033X3 + .006X4 + .999X5, with the first "
               "four ratios written as percentages."),
    "coefficients": {
        "working_capital_over_total_assets": 0.012,
        "retained_earnings_over_total_assets": 0.014,
        "earnings_before_interest_and_taxes_over_total_assets": 0.033,
        "market_value_of_equity_over_total_liabilities": 0.006,
        "sales_over_total_assets": 0.999,
    },
    "components": {
        "working_capital_over_total_assets":
            "(current_assets[t] - current_liabilities[t]) / assets[t]",
        "retained_earnings_over_total_assets": "retained_earnings[t] / assets[t]",
        "earnings_before_interest_and_taxes_over_total_assets":
            "(pretax_income[t] + interest_expense[t]) / assets[t]",
        "market_value_of_equity_over_total_liabilities":
            "market_value_of_equity / total_liabilities[t]",
        "sales_over_total_assets": "revenue[t] / assets[t]",
    },
    "formula": ("the first four ratios times 100, each times its coefficient, plus "
                ".999 times the fifth"),
}
PERCENT_RATIOS = ("working_capital_over_total_assets",
                  "retained_earnings_over_total_assets",
                  "earnings_before_interest_and_taxes_over_total_assets",
                  "market_value_of_equity_over_total_liabilities")

NO_MARKET_VALUE = ("Altman's fourth ratio is the market value of equity over the "
                   "book value of total debt, and no market value of equity was "
                   "handed to this computation: no price is committed for these "
                   "companies and the price backends answer unconfigured without a "
                   "token. The book-equity model of Altman (1983) is a different "
                   "model with different coefficients, not this one with a "
                   "substitute input")

LAZY_PRICES = {
    "source": ("Cohen, L., Malloy, C. and Nguyen, Q. (2020). Lazy Prices. Journal "
               "of Finance 75(3): 1371-1415. Cosine similarity of term-frequency "
               "vectors of two filings' text."),
    "formula": "sum over words of count_now * count_before / (|now| * |before|)",
    "words": ("the text lower-cased, and every maximal run of the letters a to z "
              "is one word; digits, punctuation and every other character "
              "separate words"),
    "pairing": ("the triggering report's notes against the notes of the "
                "prior-period report the fixture stores beside it — consecutive "
                "note text, as docs/CHECKLIST.md names the row"),
}

LOUGHRAN_MCDONALD = {
    "source": ("Loughran, T. and McDonald, B. (2011). When Is a Liability Not a "
               "Liability? Textual Analysis, Dictionaries, and 10-Ks. Journal of "
               "Finance 66(1): 35-65. The negative word list of the master "
               "dictionary."),
    "missing": ("the Loughran and McDonald master dictionary is published as free "
                "for use in academic research, with commercial licences on "
                "request and no grant to redistribute it, and this repository is "
                "public under Apache 2.0 — so the word list is not committed, "
                "there is no file whose sha256 the manifest could record, and no "
                "share is computed. docs/needs_judgment.md carries the question"),
}


# --- the record ---------------------------------------------------------------

def fiscal_years(index: dict, period_end: str | None) -> dict[str, dict]:
    """The current year, the prior year and the year two back, by the trend table's rule."""
    annual = trends.periods(index, "year")
    slots = trends.requested(annual, len(YEARS), trends.YEAR_STEP, "year",
                             trends.year_end_anchor(annual, period_end))
    return dict(zip(YEARS, slots))


def _named(year: str) -> str:
    return year.replace("_", " ")


class Terms:
    """Every term read, for every year, once. What was read is what is reported."""

    def __init__(self, document: dict, index: dict, years: dict[str, dict]):
        self.document, self.index, self.years = document, index, years
        self.cells: dict[tuple[str, str], dict] = {}

    def __call__(self, term: str, year: str) -> dict:
        key = (term, year)
        if key not in self.cells:
            slot = self.years[year]
            if slot["period"] is None:
                cell = {"missing": f"{term} in the {_named(year)}: {slot['reason']}"}
            else:
                found = trends.term_source(self.document, self.index, term,
                                           slot["period"], CONCEPTS)
                cell = found if "missing" not in found else \
                    {"missing": f"{_named(year)}: {found['missing']}"}
            self.cells[key] = cell
        return self.cells[key]

    def gather(self, needs: list[tuple[str, str]]) -> tuple[dict, dict, list[str]]:
        """The values, the inputs as reported, and every reason one is not there.

        A term read in more than one year must rest on the same concept in each,
        for the reason `trends._change` gives: an index of two different things
        is not a change in one.
        """
        values, inputs, gaps = {}, {}, []
        for term, year in needs:
            cell = self(term, year)
            inputs.setdefault(term, {})[year] = cell
            if "missing" in cell:
                gaps.append(cell["missing"])
            else:
                values[(term, year)] = cell["value"]
        for term, by_year in inputs.items():
            tags = {year: cell["tag"] for year, cell in by_year.items() if "tag" in cell}
            if len(set(tags.values())) > 1:
                named = "; ".join(f"us-gaap:{tag} in the {_named(year)}"
                                  for year, tag in tags.items())
                gaps.append(f"{term} rests on a different concept in each year, so "
                            f"the years are not one series — {named}")
        return values, inputs, gaps


def _both(term: str) -> list[tuple[str, str]]:
    return [(term, CURRENT), (term, PRIOR)]


def _result(spec: dict, inputs: dict, gaps: list[str], compute) -> dict:
    """The paper, the inputs, and either the computed row or the reason it is not."""
    out = {key: spec[key] for key in ("source", "formula", "coefficients",
                                      "components", "signals", "reading")
           if key in spec}
    out["inputs"] = inputs
    if gaps:
        out["missing"] = "; ".join(gaps)
        return out
    try:
        out.update(compute())
    except ZeroDivisionError:
        out["missing"] = ("a denominator in the formula is zero for these inputs, "
                          "and a quotient over zero is not a number")
    return out


def beneish_m_score(terms: Terms) -> dict:
    needs = [pair for term in ("receivables", "revenue", "cost_of_revenue",
                               "current_assets", "property_plant_and_equipment",
                               "assets", "depreciation_and_amortization",
                               "selling_general_and_administrative",
                               "current_liabilities", "long_term_debt", "cash",
                               "current_maturities_of_long_term_debt",
                               "income_taxes_payable")
             for pair in _both(term)]
    values, inputs, gaps = terms.gather(needs)

    def compute():
        def v(term, year):
            return values[(term, year)]

        def change(term):
            return v(term, CURRENT) - v(term, PRIOR)

        def rate_of_depreciation(year):
            return v("depreciation_and_amortization", year) / (
                v("depreciation_and_amortization", year)
                + v("property_plant_and_equipment", year))

        def gross_margin(year):
            return (v("revenue", year) - v("cost_of_revenue", year)) / v("revenue", year)

        def hard_asset_share(year):
            return (v("current_assets", year)
                    + v("property_plant_and_equipment", year)) / v("assets", year)

        def leverage(year):
            return (v("current_liabilities", year) + v("long_term_debt", year)) \
                / v("assets", year)

        accruals = ((change("current_assets") - change("cash"))
                    - (change("current_liabilities")
                       - change("current_maturities_of_long_term_debt")
                       - change("income_taxes_payable"))
                    - v("depreciation_and_amortization", CURRENT))
        components = {
            "days_sales_in_receivables_index":
                (v("receivables", CURRENT) / v("revenue", CURRENT))
                / (v("receivables", PRIOR) / v("revenue", PRIOR)),
            "gross_margin_index": gross_margin(PRIOR) / gross_margin(CURRENT),
            "asset_quality_index":
                (1 - hard_asset_share(CURRENT)) / (1 - hard_asset_share(PRIOR)),
            "sales_growth_index": v("revenue", CURRENT) / v("revenue", PRIOR),
            "depreciation_index":
                rate_of_depreciation(PRIOR) / rate_of_depreciation(CURRENT),
            "sales_general_and_administrative_expenses_index":
                (v("selling_general_and_administrative", CURRENT) / v("revenue", CURRENT))
                / (v("selling_general_and_administrative", PRIOR) / v("revenue", PRIOR)),
            "total_accruals_to_total_assets": accruals / v("assets", CURRENT),
            "leverage_index": leverage(CURRENT) / leverage(PRIOR),
        }
        weights = BENEISH["coefficients"]
        value = weights["constant"] + sum(weights[name] * components[name]
                                          for name in components)
        return {"value": value, "component_values": components,
                "total_accruals": accruals}

    return _result(BENEISH, inputs, gaps, compute)


def accruals_over_assets(terms: Terms) -> dict:
    needs = [pair for term in ("current_assets", "cash", "current_liabilities",
                               "debt_in_current_liabilities", "income_taxes_payable",
                               "assets")
             for pair in _both(term)] + [("depreciation_and_amortization", CURRENT)]
    values, inputs, gaps = terms.gather(needs)

    def compute():
        def change(term):
            return values[(term, CURRENT)] - values[(term, PRIOR)]

        accruals = ((change("current_assets") - change("cash"))
                    - (change("current_liabilities")
                       - change("debt_in_current_liabilities")
                       - change("income_taxes_payable"))
                    - values[("depreciation_and_amortization", CURRENT)])
        average = (values[("assets", CURRENT)] + values[("assets", PRIOR)]) / 2
        return {"value": accruals / average, "accruals": accruals,
                "average_total_assets": average}

    return _result(SLOAN, inputs, gaps, compute)


def net_operating_assets(terms: Terms) -> dict:
    needs = [(term, CURRENT) for term in ("assets", "cash", "short_term_investments",
                                          "debt_in_current_liabilities",
                                          "long_term_debt", "total_equity")]
    needs.append(("assets", PRIOR))
    values, inputs, gaps = terms.gather(needs)

    def compute():
        def v(term):
            return values[(term, CURRENT)]

        operating_assets = v("assets") - (v("cash") + v("short_term_investments"))
        operating_liabilities = (v("assets") - v("debt_in_current_liabilities")
                                 - v("long_term_debt") - v("total_equity"))
        return {"value": (operating_assets - operating_liabilities)
                / values[("assets", PRIOR)],
                "component_values": {"operating_assets": operating_assets,
                                     "operating_liabilities": operating_liabilities}}

    return _result(HIRSHLEIFER, inputs, gaps, compute)


def piotroski_f_score(terms: Terms) -> dict:
    needs = (_both("net_income") + [("operating_cash_flow", CURRENT)]
             + [("assets", year) for year in YEARS]
             + _both("long_term_debt") + _both("current_assets")
             + _both("current_liabilities") + [("common_stock_issued", CURRENT)]
             + _both("revenue") + _both("cost_of_revenue"))
    values, inputs, gaps = terms.gather(needs)

    def compute():
        def v(term, year):
            return values[(term, year)]

        def average_assets(year, before):
            return (v("assets", year) + v("assets", before)) / 2

        def gross_margin(year):
            return (v("revenue", year) - v("cost_of_revenue", year)) / v("revenue", year)

        measures = {
            "return_on_assets": {CURRENT: v("net_income", CURRENT) / v("assets", PRIOR),
                                 PRIOR: v("net_income", PRIOR) / v("assets", TWO_BACK)},
            "operating_cash_flow_over_assets":
                {CURRENT: v("operating_cash_flow", CURRENT) / v("assets", PRIOR)},
            "leverage": {
                CURRENT: v("long_term_debt", CURRENT) / average_assets(CURRENT, PRIOR),
                PRIOR: v("long_term_debt", PRIOR) / average_assets(PRIOR, TWO_BACK)},
            "current_ratio": {
                year: v("current_assets", year) / v("current_liabilities", year)
                for year in (CURRENT, PRIOR)},
            "gross_margin": {year: gross_margin(year) for year in (CURRENT, PRIOR)},
            "asset_turnover": {CURRENT: v("revenue", CURRENT) / v("assets", PRIOR),
                               PRIOR: v("revenue", PRIOR) / v("assets", TWO_BACK)},
            "common_stock_issued": {CURRENT: v("common_stock_issued", CURRENT)},
        }
        roa, cfo = measures["return_on_assets"], measures["operating_cash_flow_over_assets"]
        signals = {
            "return_on_assets_positive": roa[CURRENT] > 0,
            "operating_cash_flow_positive": cfo[CURRENT] > 0,
            "return_on_assets_rose": roa[CURRENT] - roa[PRIOR] > 0,
            "cash_flow_exceeds_return_on_assets": cfo[CURRENT] > roa[CURRENT],
            "leverage_fell": measures["leverage"][CURRENT] - measures["leverage"][PRIOR] < 0,
            "current_ratio_rose":
                measures["current_ratio"][CURRENT] - measures["current_ratio"][PRIOR] > 0,
            "no_common_equity_issued": v("common_stock_issued", CURRENT) == 0,
            "gross_margin_rose":
                measures["gross_margin"][CURRENT] - measures["gross_margin"][PRIOR] > 0,
            "asset_turnover_rose":
                measures["asset_turnover"][CURRENT] - measures["asset_turnover"][PRIOR] > 0,
        }
        signals = {name: int(held) for name, held in signals.items()}
        return {"value": sum(signals.values()), "signal_values": signals,
                "measures": measures}

    return _result(PIOTROSKI, inputs, gaps, compute)


def ohlson_o_score(terms: Terms, price_level: dict) -> dict:
    needs = ([(term, CURRENT) for term in ("assets", "total_liabilities",
                                           "current_assets", "current_liabilities",
                                           "operating_cash_flow")]
             + _both("net_income"))
    values, inputs, gaps = terms.gather(needs)
    if "missing" in price_level:
        gaps.append(f"price-level index: {price_level['missing']}")

    def compute():
        def v(term, year=CURRENT):
            return values[(term, year)]

        now, before = v("net_income"), v("net_income", PRIOR)
        deflated = v("assets") / price_level["value"]
        if deflated <= 0:
            return {"missing": "total assets over the price-level index is not "
                               "positive, and it has no log"}
        components = {
            "size": math.log(deflated),
            "total_liabilities_over_total_assets": v("total_liabilities") / v("assets"),
            "working_capital_over_total_assets":
                (v("current_assets") - v("current_liabilities")) / v("assets"),
            "current_liabilities_over_current_assets":
                v("current_liabilities") / v("current_assets"),
            "liabilities_exceed_assets": int(v("total_liabilities") > v("assets")),
            "net_income_over_total_assets": now / v("assets"),
            "funds_from_operations_over_total_liabilities":
                v("operating_cash_flow") / v("total_liabilities"),
            "net_loss_in_both_years": int(now < 0 and before < 0),
            "change_in_net_income": (now - before) / (abs(now) + abs(before)),
        }
        weights = OHLSON["coefficients"]
        value = weights["constant"] + sum(weights[name] * components[name]
                                          for name in components)
        return {"value": value, "component_values": components}

    out = _result(OHLSON, inputs, gaps, compute)
    out["price_level_index"] = price_level
    return out


def altman_z_score(terms: Terms, market_value_of_equity: dict | None) -> dict:
    needs = [(term, CURRENT) for term in ("current_assets", "current_liabilities",
                                          "retained_earnings", "pretax_income",
                                          "interest_expense", "total_liabilities",
                                          "revenue", "assets")]
    values, inputs, gaps = terms.gather(needs)
    out = _result(ALTMAN, inputs, gaps, lambda: {})
    if gaps:
        return out

    def v(term):
        return values[(term, CURRENT)]

    try:
        ratios = {
            "working_capital_over_total_assets":
                (v("current_assets") - v("current_liabilities")) / v("assets"),
            "retained_earnings_over_total_assets": v("retained_earnings") / v("assets"),
            "earnings_before_interest_and_taxes_over_total_assets":
                (v("pretax_income") + v("interest_expense")) / v("assets"),
            "sales_over_total_assets": v("revenue") / v("assets"),
        }
    except ZeroDivisionError:
        out["missing"] = "total assets are zero, and a quotient over zero is not a number"
        return out
    out["market_value_of_equity"] = market_value_of_equity
    if market_value_of_equity is None:
        out["component_values"] = ratios
        out["missing"] = NO_MARKET_VALUE
        return out
    if v("total_liabilities") == 0:
        out["component_values"] = ratios
        out["missing"] = "total liabilities are zero, and a quotient over zero is not a number"
        return out
    ratios["market_value_of_equity_over_total_liabilities"] = \
        market_value_of_equity["value"] / v("total_liabilities")
    weights = ALTMAN["coefficients"]
    out["component_values"] = ratios
    out["value"] = sum(weights[name] * (ratios[name] * 100 if name in PERCENT_RATIOS
                                        else ratios[name])
                       for name in weights)
    return out


# --- the price-level index ----------------------------------------------------

INDEX_DIRECTORY = Path(__file__).resolve().parent / "price_level_index"
BASE_YEAR = 1968
QUARTER_STARTS = ("01-01", "04-01", "07-01", "10-01")


def price_level_index(year: int, cutoff: dt.date, *,
                      directory: Path = INDEX_DIRECTORY) -> dict:
    """The GNP price-level index for one calendar year, with 1968 at 100.

    The annual level is the mean of the year's four quarters, in the newest
    committed vintage dated at or before the cutoff — a vintage is the series as
    it was published on that date, and a later one is a document filed after the
    trigger. A year whose four quarters that vintage does not all carry is
    missing, not estimated.
    """
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    usable = [row for row in manifest["vintages"]
              if cutoff_guard.parse_date(row["vintage_date"], "vintage_date") <= cutoff]
    if not usable:
        earliest = min(row["vintage_date"] for row in manifest["vintages"])
        return {"missing": f"no committed vintage of {manifest['series']} is dated at "
                           f"or before the cutoff {cutoff.isoformat()}; the earliest "
                           f"is {earliest}"}
    vintage = max(usable, key=lambda row: row["vintage_date"])
    raw = (directory / vintage["path"]).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != vintage["sha256"]:
        raise BaselineInputError(
            f"{vintage['path']} hashes to {digest}, not the {vintage['sha256']} its "
            f"manifest recorded — refused, because the file is no longer the "
            f"vintage that was published")
    levels: dict[str, float] = {}
    for row in list(csv.reader(raw.decode("utf-8").splitlines()))[1:]:
        if len(row) == 2 and row[1].strip() not in ("", "."):
            levels[row[0]] = float(row[1])

    def annual(of: int) -> tuple[float | None, list[float]]:
        found = [levels[f"{of}-{start}"] for start in QUARTER_STARTS
                 if f"{of}-{start}" in levels]
        return (sum(found) / 4 if len(found) == 4 else None), found

    described = {"series": manifest["series"], "vintage_date": vintage["vintage_date"],
                 "path": f"src/price_level_index/{vintage['path']}",
                 "sha256": vintage["sha256"], "year": year, "base_year": BASE_YEAR}
    level, quarters = annual(year)
    base, base_quarters = annual(BASE_YEAR)
    if level is None or base is None:
        short = year if level is None else BASE_YEAR
        count = len(quarters) if level is None else len(base_quarters)
        return {**described,
                "missing": f"the vintage of {vintage['vintage_date']} carries {count} "
                           f"of the four quarters of {short}, and an annual level is "
                           f"not estimated from part of a year"}
    return {**described, "value": level / base * 100, "annual_mean": level,
            "base_year_mean": base, "quarters": quarters, "base_quarters": base_quarters}


# --- the notes ----------------------------------------------------------------

WORD = re.compile(r"[a-z]+")


def words(text: str) -> collections.Counter:
    """Term frequencies, by the rule `LAZY_PRICES["words"]` states."""
    return collections.Counter(WORD.findall(text.lower()))


def cosine(now: collections.Counter, before: collections.Counter) -> float | None:
    """The cosine of two term-frequency vectors. None when either has no word."""
    size_now = math.sqrt(sum(count * count for count in now.values()))
    size_before = math.sqrt(sum(count * count for count in before.values()))
    if size_now == 0 or size_before == 0:
        return None
    return sum(count * before[word] for word, count in now.items()) \
        / (size_now * size_before)


def _notes(payload: dict) -> dict[str, str]:
    """Section name → its text, in document order, one entry per name.

    A section tagged inside another is left out: its text is already inside the
    one that contains it, and counting it twice would weigh a table by how many
    levels the filer tagged it at. Two sections under one name are joined.
    """
    found: dict[str, list[str]] = {}
    for section in payload["sections"]:
        if section["contained_in"] is None:
            found.setdefault(section["name"], []).append(section["text"])
    return {name: "\n".join(texts) for name, texts in found.items()}


def note_cosine_similarity(now: dict, before: dict) -> dict:
    """The whole of the notes, and each note both filings carry, compared."""
    out = {key: LAZY_PRICES[key] for key in LAZY_PRICES}
    out["current"] = {"accession": now["accession"], "filing_date": now["filing_date"]}
    out["prior"] = {"accession": before["accession"],
                    "filing_date": before["filing_date"]}
    notes_now, notes_before = _notes(now), _notes(before)
    whole_now = sum((words(text) for text in notes_now.values()), collections.Counter())
    whole_before = sum((words(text) for text in notes_before.values()),
                       collections.Counter())
    out["current"]["words"] = sum(whole_now.values())
    out["prior"]["words"] = sum(whole_before.values())
    out["sections"] = {}
    for name in notes_now:
        if name in notes_before:
            similarity = cosine(words(notes_now[name]), words(notes_before[name]))
            out["sections"][name] = similarity if similarity is not None else {
                "missing": "one of the two holds no word"}
    out["added"] = [name for name in notes_now if name not in notes_before]
    out["removed"] = [name for name in notes_before if name not in notes_now]
    similarity = cosine(whole_now, whole_before)
    if similarity is None:
        out["missing"] = "the notes of one of the two filings hold no word"
    else:
        out["value"] = similarity
    return out


def read_notes(ticker: str, form: str, cutoff: dt.date, *,
               fixtures_root=cutoff_guard.FIXTURES) -> dict:
    """Both filings' notes through the date gate, or the reason there is no pair."""
    try:
        now = extract_notes.extract(ticker, form, role="xbrl_instance", cutoff=cutoff,
                                    fixtures_root=fixtures_root)
        before = extract_notes.extract(ticker, form, role="prior_period_xbrl_instance",
                                       cutoff=cutoff, fixtures_root=fixtures_root)
    except cutoff_guard.CutoffGuardError as exc:
        out = {key: LAZY_PRICES[key] for key in LAZY_PRICES}
        out["missing"] = f"no pair of consecutive notes to compare: {exc}"
        return out
    return note_cosine_similarity(now, before)


# --- the whole file -----------------------------------------------------------

def formula_baselines(document: dict, cutoff, *, period_end=None,
                      market_value_of_equity: dict | None = None,
                      index_directory: Path = INDEX_DIRECTORY) -> dict:
    """The six baselines that read the financial statements, from one record."""
    try:
        stated = cutoff_guard.parse_date(cutoff, "cutoff")
        if period_end is not None:
            period_end = cutoff_guard.parse_date(period_end, "period_end").isoformat()
    except cutoff_guard.CutoffGuardError as exc:
        raise BaselineInputError(str(exc)) from exc
    late = trends.filed_after(document, stated)
    if late:
        raise BaselineInputError(
            f"{len(late)} row(s) in the record are filed after the cutoff {stated}, "
            f"or carry no date this can read: {', '.join(late[:3])} — refused, "
            f"because a baseline one row past its cutoff is a look-ahead violation "
            f"and not a smaller answer")
    try:
        index = trends.observations(document)
    except trends.TrendInputError as exc:
        raise BaselineInputError(str(exc)) from exc
    years = fiscal_years(index, period_end)
    terms = Terms(document, index, years)

    current = years[CURRENT]["period"]
    if current is None:
        price_level = {"missing": f"no current fiscal year: {years[CURRENT]['reason']}"}
    else:
        balance_sheet_year = cutoff_guard.parse_date(current["end"], "year end").year
        price_level = price_level_index(balance_sheet_year - 1, stated,
                                        directory=index_directory)

    rows = {
        "beneish_m_score": beneish_m_score(terms),
        "accruals_over_assets": accruals_over_assets(terms),
        "net_operating_assets": net_operating_assets(terms),
        "piotroski_f_score": piotroski_f_score(terms),
        "ohlson_o_score": ohlson_o_score(terms, price_level),
        "altman_z_score": altman_z_score(terms, market_value_of_equity),
    }
    read = sorted({cell["accession"] for cell in terms.cells.values()
                   if "accession" in cell})
    return {
        "fiscal_years": {year: ({"start": slot["period"]["start"],
                                 "end": slot["period"]["end"]}
                                if slot["period"] else {"missing": slot["reason"]})
                         for year, slot in years.items()},
        "record": {"cik": document.get("cik"), "entity_name": document.get("entity_name"),
                   "filings_read": read},
        "price_level_index": price_level,
        "rows": rows,
    }


def baselines(ticker: str, form: str = "10-Q", *,
              market_value_of_equity: dict | None = None,
              fixtures_root=cutoff_guard.FIXTURES,
              index_directory: Path = INDEX_DIRECTORY) -> dict:
    """Every row of `baselines.json` for the run this report triggers.

    The cutoff is the report's own filing date and the fiscal years are anchored
    on its own period of report, both off its manifest row.
    """
    trigger = cutoff_guard.one_document(ticker, form, "primary_html",
                                        fixtures_root=fixtures_root)
    cutoff = cutoff_guard.parse_date(trigger["filing_date"], "the trigger's filing date")
    document = trends.read_record(ticker, cutoff, fixtures_root=fixtures_root)
    statements = formula_baselines(document, cutoff, period_end=trigger["report_date"],
                                   market_value_of_equity=market_value_of_equity,
                                   index_directory=index_directory)
    notes = read_notes(ticker, form, cutoff, fixtures_root=fixtures_root)
    rows = statements["rows"]
    return {
        "ticker": ticker,
        "trigger": {"form": form, "accession": trigger["accession"],
                    "filing_date": trigger["filing_date"],
                    "report_date": trigger["report_date"]},
        "cutoff": cutoff.isoformat(),
        "fiscal_years": statements["fiscal_years"],
        "beneish_m_score": rows["beneish_m_score"],
        "accruals_over_assets": rows["accruals_over_assets"],
        "net_operating_assets": rows["net_operating_assets"],
        "note_cosine_similarity": notes,
        "loughran_mcdonald_negative": dict(LOUGHRAN_MCDONALD),
        "piotroski_f_score": rows["piotroski_f_score"],
        "ohlson_o_score": rows["ohlson_o_score"],
        "altman_z_score": rows["altman_z_score"],
        "manifest": {
            "record": statements["record"],
            "price_level_index": {key: value for key, value in
                                  statements["price_level_index"].items()
                                  if key in ("series", "vintage_date", "path",
                                             "sha256", "missing")},
            "notes": {key: notes[key] for key in ("current", "prior") if key in notes},
            "word_list": {"missing": LOUGHRAN_MCDONALD["missing"]},
        },
    }


def render(payload: dict) -> str:
    """Deterministic by construction: sorted keys, no clock, no set iteration."""
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="the formula baselines")
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--form", default="10-Q",
                        help="the triggering report's form; its filing date is the "
                             "cutoff and its period of report anchors the years")
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    try:
        payload = baselines(args.ticker.upper(), args.form)
    except (OSError, ValueError, BaselineInputError, trends.TrendInputError,
            cutoff_guard.CutoffGuardError) as exc:
        print(f"baselines: {exc}", file=sys.stderr)
        return BAD_INPUT
    Path(args.out).write_text(render(payload), encoding="utf-8")
    rows = ("beneish_m_score", "accruals_over_assets", "net_operating_assets",
            "note_cosine_similarity", "loughran_mcdonald_negative",
            "piotroski_f_score", "ohlson_o_score", "altman_z_score")
    computed = [row for row in rows if "value" in payload[row]]
    print(f"baselines: {payload['ticker']} {len(computed)} of {len(rows)} rows "
          f"computed at the cutoff {payload['cutoff']} → {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
