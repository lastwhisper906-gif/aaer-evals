"""Where each trend cell sits in the company's own filed history, judged by hand.

The numbers reader does no arithmetic, so "the highest gross margin of the six
quarters on record" cannot be said by the reader unless Python has printed it.
Every filled ratio cell of `input_trends.json` carries `position_in_history`: a
plain-words sentence placing the cell's value among the filled periods of the
same ratio in the same window — quarters among the eight quarters, years among
the five years — which the reader quotes as it quotes any other part of the row.
It describes the value; it filters nothing.

The wording, chosen once and written here:

- `highest of the 6 filled quarters`, `second highest of the 6 filled
  quarters`, `third lowest of the 6 filled quarters`, `lowest of the 6 filled
  quarters` — counted from whichever end is nearer, from the top on a tie
  between the two, so the middle of five is `third highest of the 5 filled
  years`. "Filled" means this ratio has a value in that period.
- A period whose value rests on a different us-gaap concept for one of its terms
  is not compared, for the reason `src/trends.py` refuses the change between
  such periods, and the sentence says how many were left out:
  `second lowest of the 4 filled years on the same concepts; 1 other filled
  year rests on a different concept and is not compared`.

**Where the expected values come from.** For Apple's gross margin and Cisco's
days sales outstanding, the six filled quarters of each were read out of the
committed `tests/fixtures/{ticker}/companyfacts.json.gz` with
`tests/companyfacts_source.py`, which imports nothing from `src/`: every term
is typed in below with its period, the test re-reads each one out of the record
through that same reader, and the ratio is written out term by term. The six
values were then put in order by hand and the position of each written in.
Apple's annual gross margin, five years, is the odd count whose middle year is
equally near both ends. NVIDIA's annual gross margin and receivables over
revenue are the case where one year's revenue is tagged
`RevenueFromContractWithCustomerExcludingAssessedTax` and the other four years'
`Revenues` — the first term of one ratio and the second of the other — and
Carrier's annual accruals the case where the change is in net income, read the
same way. Nothing here came from running `src/trends.py`.

    .venv/bin/python -m pytest tests/test_trend_history_position.py -q
"""

from __future__ import annotations

import datetime as dt
import functools
import json

import pytest

from src import cutoff_guard, quote_gate, trends
from src.fetch_fixtures import TICKERS
from tests import companyfacts_source as source


@functools.lru_cache(maxsize=None)
def trigger(ticker: str) -> dict:
    """The manifest's row for the 10-Q the run is about, as `tests/test_trends.py` uses."""
    return cutoff_guard.one_document(ticker, "10-Q", "primary_html")


@functools.lru_cache(maxsize=None)
def table(ticker: str) -> dict:
    """The table as `src/assemble_bundle.py` builds it: cutoff and anchor both."""
    report = trigger(ticker)
    return trends.table(ticker, report["filing_date"], period_end=report["report_date"])


def quarter_tags_ending_near(ticker: str, end: str) -> set[str]:
    """Every us-gaap tag, in any unit, with a statement row inside the cutoff for
    a quarter-length span (80 to 100 days) ending within 20 days of `end`.

    Read out of the record by `tests/companyfacts_source.py`, over every tag and
    not only the ones the table reads, so the size of a history is checked
    against the record rather than against the table's own list of periods.
    """
    target = dt.date.fromisoformat(end)
    cutoff = trigger(ticker)["filing_date"]
    found = set()
    for tag, concept in source.record(ticker)["facts"][source.NAMESPACE].items():
        for rows in concept.get("units", {}).values():
            for row in source.inside([one for one in rows if source.a_statement(one)],
                                     cutoff):
                if not row.get("start"):
                    continue
                days = (dt.date.fromisoformat(row["end"])
                        - dt.date.fromisoformat(row["start"])).days + 1
                if 80 <= days <= 100 and \
                        abs((dt.date.fromisoformat(row["end"]) - target).days) <= 20:
                    found.add(tag)
    return found


def cells(ticker: str, section: str, ratio: str) -> dict[str, tuple[dict, dict]]:
    """label → (the period row, its cell for one ratio). A slot with no period
    on record has no cells at all, and stands here as an empty one."""
    return {row["label"]: (row, row["ratios"].get(ratio, {}))
            for row in table(ticker)[section]}


# --- Apple, gross margin, the six filled quarters ------------------------------
#
# `RevenueFromContractWithCustomerExcludingAssessedTax` and
# `CostOfGoodsAndServicesSold`, the first tag of each term the record carries.
# The fiscal fourth quarters, `quarters-back-3` and `quarters-back-7`, are
# reported as a duration by no filing, so the history is six quarters long.
#
#   quarters-back-0   (109,417 - 54,647) / 109,417 = 0.50056
#   quarters-back-1   (111,184 - 56,403) / 111,184 = 0.49271
#   quarters-back-2   (143,756 - 74,525) / 143,756 = 0.48159
#   quarters-back-5   ( 95,359 - 50,492) /  95,359 = 0.47051
#   quarters-back-6   (124,300 - 66,025) / 124,300 = 0.46883
#   quarters-back-4   ( 94,036 - 50,318) /  94,036 = 0.46491
APPLE_GROSS_MARGIN = {
    "quarters-back-0": ("2026-03-29", "2026-06-27", 109_417_000_000.0, 54_647_000_000.0,
                        "highest of the 6 filled quarters"),
    "quarters-back-1": ("2025-12-28", "2026-03-28", 111_184_000_000.0, 56_403_000_000.0,
                        "second highest of the 6 filled quarters"),
    "quarters-back-2": ("2025-09-28", "2025-12-27", 143_756_000_000.0, 74_525_000_000.0,
                        "third highest of the 6 filled quarters"),
    "quarters-back-4": ("2025-03-30", "2025-06-28", 94_036_000_000.0, 50_318_000_000.0,
                        "lowest of the 6 filled quarters"),
    "quarters-back-5": ("2024-12-29", "2025-03-29", 95_359_000_000.0, 50_492_000_000.0,
                        "third lowest of the 6 filled quarters"),
    "quarters-back-6": ("2024-09-29", "2024-12-28", 124_300_000_000.0, 66_025_000_000.0,
                        "second lowest of the 6 filled quarters"),
}


def test_apples_gross_margin_is_placed_among_its_six_filled_quarters():
    cutoff = trigger("AAPL")["filing_date"]
    by_label = cells("AAPL", "quarters", "gross_margin")
    filled = {label for label, (_, cell) in by_label.items() if "value" in cell}
    assert filled == set(APPLE_GROSS_MARGIN)
    for label, (start, end, revenue, cost, position) in APPLE_GROSS_MARGIN.items():
        span = f"{start}..{end}"
        assert source.one_value(
            "AAPL", "RevenueFromContractWithCustomerExcludingAssessedTax", span, cutoff) == revenue
        assert source.one_value("AAPL", "CostOfGoodsAndServicesSold", span, cutoff) == cost
        row, cell = by_label[label]
        assert (row["start"], row["end"]) == (start, end)
        assert cell["value"] == pytest.approx((revenue - cost) / revenue, rel=0, abs=1e-12)
        assert cell["position_in_history"] == position, label
    for label in set(by_label) - filled:
        assert "position_in_history" not in by_label[label][1], label


def test_apples_two_empty_quarters_are_empty_in_the_record_under_every_tag():
    """Why the history is six long, asked of the record and not of the table.

    The window steps back 91 days from the 10-Q's period, 2026-06-27, so
    `quarters-back-3` looks for a quarter ending near 2025-09-27 and
    `quarters-back-7` near 2024-09-28: Apple's fiscal fourth quarters. No
    statement row under any us-gaap tag spans a quarter ending there.
    """
    by_label = cells("AAPL", "quarters", "gross_margin")
    for label, end in (("quarters-back-3", "2025-09-27"), ("quarters-back-7", "2024-09-28")):
        assert by_label[label][0]["target_end"] == end
        assert quarter_tags_ending_near("AAPL", end) == set(), label


# --- Cisco, days sales outstanding, the six filled quarters --------------------
#
# `AccountsReceivableNetCurrent` at the quarter's end over
# `RevenueFromContractWithCustomerExcludingAssessedTax` for the quarter, times
# the quarter's 91 days. Every quarter here is 91 days, so the order is the
# order of receivables over revenue.
#
#   quarters-back-1   6,606 / 15,349 = 0.43039
#   quarters-back-0   6,480 / 15,841 = 0.40907
#   quarters-back-5   5,669 / 13,991 = 0.40519
#   quarters-back-4   5,277 / 14,149 = 0.37296
#   quarters-back-2   4,827 / 14,883 = 0.32433
#   quarters-back-6   4,457 / 13,841 = 0.32201
CISCO_DAYS_SALES_OUTSTANDING = {
    "quarters-back-0": ("2026-01-25", "2026-04-25", 6_480_000_000.0, 15_841_000_000.0,
                        "second highest of the 6 filled quarters"),
    "quarters-back-1": ("2025-10-26", "2026-01-24", 6_606_000_000.0, 15_349_000_000.0,
                        "highest of the 6 filled quarters"),
    "quarters-back-2": ("2025-07-27", "2025-10-25", 4_827_000_000.0, 14_883_000_000.0,
                        "second lowest of the 6 filled quarters"),
    "quarters-back-4": ("2025-01-26", "2025-04-26", 5_277_000_000.0, 14_149_000_000.0,
                        "third lowest of the 6 filled quarters"),
    "quarters-back-5": ("2024-10-27", "2025-01-25", 5_669_000_000.0, 13_991_000_000.0,
                        "third highest of the 6 filled quarters"),
    "quarters-back-6": ("2024-07-28", "2024-10-26", 4_457_000_000.0, 13_841_000_000.0,
                        "lowest of the 6 filled quarters"),
}


def test_ciscos_days_sales_outstanding_is_placed_among_its_six_filled_quarters():
    cutoff = trigger("CSCO")["filing_date"]
    by_label = cells("CSCO", "quarters", "days_sales_outstanding")
    filled = {label for label, (_, cell) in by_label.items() if "value" in cell}
    assert filled == set(CISCO_DAYS_SALES_OUTSTANDING)
    for label, (start, end, receivables, revenue, position) in \
            CISCO_DAYS_SALES_OUTSTANDING.items():
        assert source.one_value("CSCO", "AccountsReceivableNetCurrent", end, cutoff) \
            == receivables
        assert source.one_value(
            "CSCO", "RevenueFromContractWithCustomerExcludingAssessedTax",
            f"{start}..{end}", cutoff) == revenue
        row, cell = by_label[label]
        assert (row["start"], row["end"], row["days"]) == (start, end, 91)
        assert cell["value"] == pytest.approx(receivables / revenue * 91, rel=0, abs=1e-9)
        assert cell["position_in_history"] == position, label
    for label in set(by_label) - filled:
        assert "position_in_history" not in by_label[label][1], label


def test_ciscos_two_empty_quarters_hold_no_revenue_in_the_record():
    """Why Cisco's history is six long, asked of the record.

    Stepping back from 2026-04-25, `quarters-back-3` looks near 2025-07-26 and
    `quarters-back-7` near 2024-07-27: Cisco's fiscal fourth quarters. The only
    statement rows spanning a quarter ending there are the share repurchases, which
    are no term of days sales outstanding, so no revenue for the quarter exists
    to divide by.
    """
    repurchases = {"StockRepurchasedAndRetiredDuringPeriodShares",
                   "StockRepurchasedAndRetiredDuringPeriodValue"}
    by_label = cells("CSCO", "quarters", "days_sales_outstanding")
    for label, end in (("quarters-back-3", "2025-07-26"), ("quarters-back-7", "2024-07-27")):
        assert by_label[label][0]["target_end"] == end
        assert quarter_tags_ending_near("CSCO", end) == repurchases, label


# --- Apple, gross margin, the five fiscal years ---------------------------------
#
# The same two tags in every year. Five is odd, so the middle year sits two
# places from each end, and the rule counts it from the top.
#
#   years-back-0   (416,161 - 220,960) / 416,161 = 0.46905
#   years-back-1   (391,035 - 210,352) / 391,035 = 0.46206
#   years-back-2   (383,285 - 214,137) / 383,285 = 0.44131
#   years-back-3   (394,328 - 223,546) / 394,328 = 0.43310
#   years-back-4   (365,817 - 212,981) / 365,817 = 0.41779
APPLE_ANNUAL_GROSS_MARGIN = {
    "years-back-0": ("2024-09-29", "2025-09-27", 416_161_000_000.0, 220_960_000_000.0,
                     "highest of the 5 filled years"),
    "years-back-1": ("2023-10-01", "2024-09-28", 391_035_000_000.0, 210_352_000_000.0,
                     "second highest of the 5 filled years"),
    "years-back-2": ("2022-09-25", "2023-09-30", 383_285_000_000.0, 214_137_000_000.0,
                     "third highest of the 5 filled years"),
    "years-back-3": ("2021-09-26", "2022-09-24", 394_328_000_000.0, 223_546_000_000.0,
                     "second lowest of the 5 filled years"),
    "years-back-4": ("2020-09-27", "2021-09-25", 365_817_000_000.0, 212_981_000_000.0,
                     "lowest of the 5 filled years"),
}


def test_apples_middle_year_is_counted_from_the_top():
    cutoff = trigger("AAPL")["filing_date"]
    by_label = cells("AAPL", "years", "gross_margin")
    assert {label for label, (_, cell) in by_label.items() if "value" in cell} \
        == set(APPLE_ANNUAL_GROSS_MARGIN)
    for label, (start, end, revenue, cost, position) in APPLE_ANNUAL_GROSS_MARGIN.items():
        span = f"{start}..{end}"
        assert source.one_value(
            "AAPL", "RevenueFromContractWithCustomerExcludingAssessedTax", span, cutoff) == revenue
        assert source.one_value("AAPL", "CostOfGoodsAndServicesSold", span, cutoff) == cost
        row, cell = by_label[label]
        assert (row["start"], row["end"]) == (start, end)
        assert cell["value"] == pytest.approx((revenue - cost) / revenue, rel=0, abs=1e-12)
        assert cell["position_in_history"] == position, label


# --- NVIDIA, gross margin, five years on two revenue concepts -------------------
#
# `CostOfRevenue` in all five years. Revenue is `Revenues` in fiscal 2023 to
# 2026, and `RevenueFromContractWithCustomerExcludingAssessedTax` in fiscal 2022,
# because that tag comes first in the table's list and the record carries it for
# that year alone. The four years on one concept are compared with each other;
# fiscal 2022 is compared with nothing.
#
#   years-back-1   (130,497 - 32,639) / 130,497 = 0.74989
#   years-back-2   ( 60,922 - 16,621) /  60,922 = 0.72718
#   years-back-0   (215,938 - 62,475) / 215,938 = 0.71068
#   years-back-3   ( 26,974 - 11,618) /  26,974 = 0.56929
#   years-back-4   ( 26,914 -  9,439) /  26,914 = 0.64929, on the other concept
AGAINST_FOUR = "of the 4 filled years on the same concepts; 1 other filled year " \
               "rests on a different concept and is not compared"
NVIDIA_GROSS_MARGIN = {
    "years-back-0": ("2025-01-27", "2026-01-25", "Revenues",
                     215_938_000_000.0, 62_475_000_000.0, f"second lowest {AGAINST_FOUR}"),
    "years-back-1": ("2024-01-29", "2025-01-26", "Revenues",
                     130_497_000_000.0, 32_639_000_000.0, f"highest {AGAINST_FOUR}"),
    "years-back-2": ("2023-01-30", "2024-01-28", "Revenues",
                     60_922_000_000.0, 16_621_000_000.0, f"second highest {AGAINST_FOUR}"),
    "years-back-3": ("2022-01-31", "2023-01-29", "Revenues",
                     26_974_000_000.0, 11_618_000_000.0, f"lowest {AGAINST_FOUR}"),
    "years-back-4": ("2021-02-01", "2022-01-30",
                     "RevenueFromContractWithCustomerExcludingAssessedTax",
                     26_914_000_000.0, 9_439_000_000.0,
                     "the only filled year on the same concepts; 4 other filled years "
                     "rest on a different concept and are not compared"),
}


def test_nvidias_annual_gross_margin_is_compared_only_on_the_same_concepts():
    cutoff = trigger("NVDA")["filing_date"]
    by_label = cells("NVDA", "years", "gross_margin")
    assert {label for label, (_, cell) in by_label.items() if "value" in cell} \
        == set(NVIDIA_GROSS_MARGIN)
    for label, (start, end, revenue_tag, revenue, cost, position) in \
            NVIDIA_GROSS_MARGIN.items():
        span = f"{start}..{end}"
        assert source.one_value("NVDA", revenue_tag, span, cutoff) == revenue
        assert source.one_value("NVDA", "CostOfRevenue", span, cutoff) == cost
        row, cell = by_label[label]
        assert (row["start"], row["end"]) == (start, end)
        assert cell["inputs"]["revenue"]["tag"] == revenue_tag
        assert cell["value"] == pytest.approx((revenue - cost) / revenue, rel=0, abs=1e-12)
        assert cell["position_in_history"] == position, label


# --- NVIDIA, receivables over revenue, the concept change in the second term ----
#
# `AccountsReceivableNetCurrent` at every fiscal year end, over the same revenue
# as above. Here revenue is the ratio's second term, so a rule that compared the
# first term's concept alone would rank fiscal 2022 with the other four.
#
#   years-back-0   38,466 / 215,938 = 0.17813
#   years-back-1   23,065 / 130,497 = 0.17675
#   years-back-2    9,999 /  60,922 = 0.16413
#   years-back-3    3,827 /  26,974 = 0.14188
#   years-back-4    4,650 /  26,914 = 0.17277, on the other concept
NVIDIA_RECEIVABLES_OVER_REVENUE = {
    "years-back-0": ("2025-01-27", "2026-01-25", "Revenues",
                     38_466_000_000.0, 215_938_000_000.0, f"highest {AGAINST_FOUR}"),
    "years-back-1": ("2024-01-29", "2025-01-26", "Revenues",
                     23_065_000_000.0, 130_497_000_000.0, f"second highest {AGAINST_FOUR}"),
    "years-back-2": ("2023-01-30", "2024-01-28", "Revenues",
                     9_999_000_000.0, 60_922_000_000.0, f"second lowest {AGAINST_FOUR}"),
    "years-back-3": ("2022-01-31", "2023-01-29", "Revenues",
                     3_827_000_000.0, 26_974_000_000.0, f"lowest {AGAINST_FOUR}"),
    "years-back-4": ("2021-02-01", "2022-01-30",
                     "RevenueFromContractWithCustomerExcludingAssessedTax",
                     4_650_000_000.0, 26_914_000_000.0,
                     "the only filled year on the same concepts; 4 other filled years "
                     "rest on a different concept and are not compared"),
}


def test_a_concept_change_in_the_second_term_also_keeps_a_year_out():
    cutoff = trigger("NVDA")["filing_date"]
    by_label = cells("NVDA", "years", "receivables_over_revenue")
    assert {label for label, (_, cell) in by_label.items() if "value" in cell} \
        == set(NVIDIA_RECEIVABLES_OVER_REVENUE)
    for label, (start, end, revenue_tag, receivables, revenue, position) in \
            NVIDIA_RECEIVABLES_OVER_REVENUE.items():
        assert source.one_value("NVDA", "AccountsReceivableNetCurrent", end, cutoff) \
            == receivables
        assert source.one_value("NVDA", revenue_tag, f"{start}..{end}", cutoff) == revenue
        row, cell = by_label[label]
        assert (row["start"], row["end"]) == (start, end)
        assert cell["inputs"]["receivables"]["tag"] == "AccountsReceivableNetCurrent"
        assert cell["inputs"]["revenue"]["tag"] == revenue_tag
        assert cell["value"] == pytest.approx(receivables / revenue, rel=0, abs=1e-12)
        assert cell["position_in_history"] == position, label


# --- Carrier, accruals over total assets, a concept change with no revenue in it -
#
# `(net_income - operating_cash_flow) / assets`. Net income is `NetIncomeLoss`
# in 2022 to 2025 and `ProfitLoss` in 2021, the one year the record carries only
# the second tag, so the change sits in the ratio's first term and no term is
# revenue. Operating cash flow is
# `NetCashProvidedByUsedInOperatingActivities` and assets `Assets` at the year
# end, in all five years.
#
#   years-back-1   (5,604 -   563) / 37,403 =  0.13478
#   years-back-3   (3,534 - 1,743) / 26,086 =  0.06866
#   years-back-0   (1,484 - 2,513) / 37,190 = -0.02767
#   years-back-2   (1,349 - 2,607) / 32,822 = -0.03833
#   years-back-4   (1,701 - 2,237) / 26,172 = -0.02048, on the other concept
CARRIER_ACCRUALS = {
    "years-back-0": ("2025-01-01", "2025-12-31", "NetIncomeLoss", 1_484_000_000.0,
                     2_513_000_000.0, 37_190_000_000.0, f"second lowest {AGAINST_FOUR}"),
    "years-back-1": ("2024-01-01", "2024-12-31", "NetIncomeLoss", 5_604_000_000.0,
                     563_000_000.0, 37_403_000_000.0, f"highest {AGAINST_FOUR}"),
    "years-back-2": ("2023-01-01", "2023-12-31", "NetIncomeLoss", 1_349_000_000.0,
                     2_607_000_000.0, 32_822_000_000.0, f"lowest {AGAINST_FOUR}"),
    "years-back-3": ("2022-01-01", "2022-12-31", "NetIncomeLoss", 3_534_000_000.0,
                     1_743_000_000.0, 26_086_000_000.0, f"second highest {AGAINST_FOUR}"),
    "years-back-4": ("2021-01-01", "2021-12-31", "ProfitLoss", 1_701_000_000.0,
                     2_237_000_000.0, 26_172_000_000.0,
                     "the only filled year on the same concepts; 4 other filled years "
                     "rest on a different concept and are not compared"),
}


def test_a_concept_change_outside_revenue_also_keeps_a_year_out():
    cutoff = trigger("CARR")["filing_date"]
    by_label = cells("CARR", "years", "accruals_over_total_assets")
    assert {label for label, (_, cell) in by_label.items() if "value" in cell} \
        == set(CARRIER_ACCRUALS)
    for label, (start, end, income_tag, income, cash_flow, assets, position) in \
            CARRIER_ACCRUALS.items():
        span = f"{start}..{end}"
        assert source.one_value("CARR", income_tag, span, cutoff) == income
        assert source.one_value(
            "CARR", "NetCashProvidedByUsedInOperatingActivities", span, cutoff) == cash_flow
        assert source.one_value("CARR", "Assets", end, cutoff) == assets
        row, cell = by_label[label]
        assert (row["start"], row["end"]) == (start, end)
        assert cell["inputs"]["net_income"]["tag"] == income_tag
        assert cell["value"] == pytest.approx((income - cash_flow) / assets, rel=0, abs=1e-12)
        assert cell["position_in_history"] == position, label


# --- ties and a flat history, planted -----------------------------------------
#
# Neither happens in the twelve records at these cutoffs, so the rows are
# planted: four quarters of one ratio, two of them equal, and one slot with no
# value at all, which is not part of the history.

def planted(values: list[float | None]) -> list[dict]:
    one_concept = {"revenue": {"tag": "Revenues"}}
    return [{"label": f"quarters-back-{back}",
             "ratios": {} if value is None else
             {"gross_margin": {"value": value, "inputs": one_concept}}}
            for back, value in enumerate(values)]


def test_a_tie_is_named_and_a_flat_history_says_so():
    rows = planted([0.5, None, 0.3, 0.5, 0.1])
    said = {row["label"]: trends.position_in_history(rows, back, "gross_margin", "quarter")
            for back, row in enumerate(rows) if row["ratios"]}
    assert said == {
        "quarters-back-0": "tied for highest of the 4 filled quarters",
        "quarters-back-2": "second lowest of the 4 filled quarters",
        "quarters-back-3": "tied for highest of the 4 filled quarters",
        "quarters-back-4": "lowest of the 4 filled quarters",
    }
    flat = planted([0.2, 0.2])
    assert trends.position_in_history(flat, 1, "gross_margin", "year") == \
        "the same value in both filled years"
    flat = planted([0.2, 0.2, 0.2])
    assert trends.position_in_history(flat, 0, "gross_margin", "quarter") == \
        "the same value in all 3 filled quarters"
    alone = planted([None, 0.2])
    assert trends.position_in_history(alone, 1, "gross_margin", "quarter") == \
        "the only filled quarter"
    middle = planted([0.1, 0.2, 0.3, 0.4, 0.5])
    assert trends.position_in_history(middle, 2, "gross_margin", "quarter") == \
        "third highest of the 5 filled quarters"


def test_every_term_of_the_ratio_is_compared_for_its_concept():
    """Planted: the same receivables tag throughout, revenue's tag changing in one
    quarter, so only the second term tells the three periods apart."""
    def row(back, value, revenue_tag):
        return {"label": f"quarters-back-{back}",
                "ratios": {"receivables_over_revenue": {
                    "value": value,
                    "inputs": {"receivables": {"tag": "AccountsReceivableNetCurrent"},
                               "revenue": {"tag": revenue_tag}}}}}
    rows = [row(0, 0.3, "Revenues"), row(1, 0.2, "Revenues"),
            row(2, 0.9, "SalesRevenueNet")]
    said = [trends.position_in_history(rows, back, "receivables_over_revenue", "quarter")
            for back in range(3)]
    assert said == [
        "highest of the 2 filled quarters on the same concepts; 1 other filled "
        "quarter rests on a different concept and is not compared",
        "lowest of the 2 filled quarters on the same concepts; 1 other filled "
        "quarter rests on a different concept and is not compared",
        "the only filled quarter on the same concepts; 2 other filled quarters "
        "rest on a different concept and are not compared",
    ]


# --- every cell, every company -------------------------------------------------

@pytest.mark.parametrize("ticker", TICKERS)
def test_every_filled_cell_says_where_it_sits_and_no_empty_cell_does(ticker):
    """Every metric, every period: a value carries its place, a gap carries none."""
    payload = table(ticker)
    placed = 0
    for row in payload["quarters"] + payload["years"]:
        for name, cell in row["ratios"].items():
            if "value" in cell:
                assert isinstance(cell.get("position_in_history"), str) \
                    and cell["position_in_history"], f"{row['label']} {name}"
                placed += 1
            else:
                assert "position_in_history" not in cell, f"{row['label']} {name}"
    assert placed, f"{ticker}: no filled cell, so nothing was tested"


def test_the_position_is_quoted_under_the_cells_own_id(tmp_path):
    """The field is part of the row the reader already quotes, not a new row.

    The id stays `{accession}:trends:{metric}:{period}` and the quote is a slice
    of the committed file, so a reader item quoting the sentence stands at the
    gate, and the same item with the sentence reworded is dropped.
    """
    accession = "0000320193-26-000020"
    (tmp_path / "input_trends.json").write_text(trends.render(table("AAPL")),
                                                encoding="utf-8")
    index = quote_gate.quotable(tmp_path, accession)
    identifier = f"{accession}:trends:gross_margin:quarters-back-0"
    quote = '"position_in_history": "highest of the 6 filled quarters"'
    assert quote in index[identifier]
    item = {"id": "gross_margin_highest", "paragraph_id": identifier, "quote": quote}
    assert quote_gate.quote_drop_reason(item, index) is None
    reworded = dict(item, quote=quote.replace("highest of", "the highest of"))
    assert quote_gate.quote_drop_reason(reworded, index) is not None
    # The row still parses back into the same table, so nothing else moved.
    assert json.loads(index[identifier])["position_in_history"] == \
        "highest of the 6 filled quarters"
