"""Quarterly operating cash flow and the three accrual measures, judged against the filings.

docs/HEDGE_FUND_ANALYSIS.md §5.2 row 17. Every expected value is read through
`tests/companyfacts_source.py`, which imports nothing from `src/`, and is checked
against the figure the filing prints, read by eye from the committed fixture:

- **Cisco's year-to-date operating cash flow.** The 10-Q filed 2026-05-19
  (`tests/fixtures/CSCO/10-Q/csco-20260425.htm.gz`) prints net cash provided by
  operating activities of 8,791 for the nine months ended April 25, 2026 and
  9,959 a year earlier; the 10-Q filed 2026-02-17 (`csco-20260124.htm.gz`)
  prints 5,034 and 5,902 for the six months. Cisco states no quarter after its
  first, so each quarter is one year to date less the one before it, and the
  differences are worked by hand below.
- **NVIDIA's fiscal 2026 balance sheet and cash flow statement**
  (`tests/fixtures/NVDA/10-K/nvda-20260125.htm`): total current assets 125,605
  and 80,126; total current liabilities 32,163 and 18,047; short-term debt 999
  and none; taxes payable 2,669 and 881 (the accrued-liabilities note); and the
  rest named where each test uses it. The three measures are worked by hand
  from the definitions §2.2 and §2.11 copy from Sloan (1996), Hribar and
  Collins (2002) and the SEC's Accounting Quality Model.
"""

from __future__ import annotations

import gzip
import json
import re

import pytest

from src import analysis_check, calculator
from tests import companyfacts_source as source

MILLION = 1_000_000

CSCO = {"ticker": "CSCO", "cutoff": "2026-05-19", "period_end": "2026-04-25", "form": "10-Q"}
NVDA = {"ticker": "NVDA", "cutoff": "2026-02-25", "period_end": "2026-01-25", "form": "10-K"}
SECTION = "quarterly_cash_flow_and_accruals"


@pytest.fixture(scope="module")
def cisco():
    return calculator.calculate(**CSCO)


@pytest.fixture(scope="module")
def nvidia():
    return calculator.calculate(**NVDA)


def cfo(ticker: str, period: str, cutoff: str) -> float:
    return source.one_value(ticker, "NetCashProvidedByUsedInOperatingActivities", period, cutoff)


# --- quarterly operating cash flow, from the years to date ----------------------------------

def test_cisco_year_to_date_rows_are_the_printed_figures():
    """The independent reader's rows are the 10-Qs' printed columns, in millions."""
    cutoff = CSCO["cutoff"]
    assert cfo("CSCO", "2025-07-27..2026-04-25", cutoff) == 8_791 * MILLION
    assert cfo("CSCO", "2024-07-28..2025-04-26", cutoff) == 9_959 * MILLION
    assert cfo("CSCO", "2025-07-27..2026-01-24", cutoff) == 5_034 * MILLION
    assert cfo("CSCO", "2024-07-28..2025-01-25", cutoff) == 5_902 * MILLION


def test_cisco_quarters_are_the_years_to_date_differenced(cisco):
    """Worked by hand, in millions:

      quarter ended 2026-04-25   8,791 (nine months) - 5,034 (six months)  = 3,757
      quarter ended 2026-01-24   5,034 (six months)  - 3,212 (three months) = 1,822
      quarter ended 2025-10-25   3,212, stated as a quarter
      quarter ended 2025-07-26  14,193 (fiscal 2025) - 9,959 (nine months)  = 4,234
      quarter ended 2025-04-26   9,959 (nine months) - 5,902 (six months)  = 4,057
    """
    cutoff = CSCO["cutoff"]
    nine, six = cfo("CSCO", "2025-07-27..2026-04-25", cutoff), cfo("CSCO", "2025-07-27..2026-01-24", cutoff)
    three = cfo("CSCO", "2025-07-27..2025-10-25", cutoff)
    year = cfo("CSCO", "2024-07-28..2025-07-26", cutoff)
    nine_before = cfo("CSCO", "2024-07-28..2025-04-26", cutoff)
    six_before = cfo("CSCO", "2024-07-28..2025-01-25", cutoff)
    assert (nine - six, six - three, year - nine_before, nine_before - six_before) == (
        3_757 * MILLION, 1_822 * MILLION, 4_234 * MILLION, 4_057 * MILLION)

    quarterly = cisco[SECTION]["operating_cash_flow_quarterly"]
    history = quarterly["history"]
    assert [(row["end"], row["value"]) for row in history[:5]] == [
        ("2026-04-25", nine - six), ("2026-01-24", six - three), ("2025-10-25", three),
        ("2025-07-26", year - nine_before), ("2025-04-26", nine_before - six_before)]
    assert quarterly["value"] == 3_757 * MILLION and quarterly["unit"] == "USD"


def test_a_differenced_quarter_names_both_rows_with_accession_and_filing_date(cisco):
    newest = cisco[SECTION]["operating_cash_flow_quarterly"]
    assert newest["formula"] == "2025-07-27..2026-04-25 less 2025-07-27..2026-01-24"
    whole, part = newest["inputs"]["year_to_date"], newest["inputs"]["year_to_date_one_quarter_shorter"]
    assert (whole["tag"], whole["accession"], whole["filed"]) == (
        "NetCashProvidedByUsedInOperatingActivities", "0000858877-26-000078", "2026-05-19")
    assert (part["accession"], part["filed"]) == ("0000858877-26-000021", "2026-02-17")
    stated = newest["history"][2]
    assert stated["formula"] == "the quarter as stated"
    assert set(stated["inputs"]) == {"stated_quarter"}


def test_cisco_quarters_five_to_seven_are_the_years_to_date_differenced(cisco):
    """The three oldest of the eight, worked by hand, in millions:

      quarter ended 2025-01-25   5,902 (six months)  - 3,661 (three months) = 2,241
      quarter ended 2024-10-26   3,661, stated as a quarter
      quarter ended 2024-07-27  10,880 (fiscal 2024) - 7,150 (nine months)  = 3,730
    """
    cutoff = CSCO["cutoff"]
    six = cfo("CSCO", "2024-07-28..2025-01-25", cutoff)
    three = cfo("CSCO", "2024-07-28..2024-10-26", cutoff)
    year = cfo("CSCO", "2023-07-30..2024-07-27", cutoff)
    nine = cfo("CSCO", "2023-07-30..2024-04-27", cutoff)
    assert (six, three, year, nine) == (5_902 * MILLION, 3_661 * MILLION, 10_880 * MILLION,
                                        7_150 * MILLION)
    assert (six - three, year - nine) == (2_241 * MILLION, 3_730 * MILLION)
    history = cisco[SECTION]["operating_cash_flow_quarterly"]["history"]
    assert [row["quarters_back"] for row in history] == list(range(8))
    assert [(row["end"], row["value"]) for row in history[5:]] == [
        ("2025-01-25", six - three), ("2024-10-26", three), ("2024-07-27", year - nine)]
    assert history[6]["formula"] == "the quarter as stated"


def test_a_quarter_is_never_one_tag_less_another():
    """Johnson Controls' record, through the independent reader: fiscal 2024
    (2023-10-01..2024-09-30) only under the continuing-operations tag, 1,568
    million (the 10-K filed 2025-11-14); its nine months under both, 572 million
    total (the 10-Q filed 2024-07-31) and 216 million continuing (the 10-Q filed
    2025-08-06). The fourth quarter is 1,568 - 216 = 1,352 under one tag, never
    1,568 - 572 = 996 across two."""
    cut, continuing = "2026-07-29", "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations"
    year, nine = "2023-10-01..2024-09-30", "2023-10-01..2024-06-30"
    assert source.one_value("JCI", continuing, year, cut) == 1_568 * MILLION
    assert source.one_value("JCI", continuing, nine, cut) == 216 * MILLION
    assert cfo("JCI", nine, cut) == 572 * MILLION
    assert source.reported("JCI", "NetCashProvidedByUsedInOperatingActivities", year, cut) == []
    # companyfacts was fetched before the 10-Q; the run's committed bundle carries it
    bundle = source.FIXTURES.parent.parent / "runs" / "JCI" / "0000833444-26-000087"
    out = calculator.calculate(ticker="JCI", cutoff=cut, period_end="2026-06-30", form="10-Q",
                               bundle=bundle)
    oldest = out[SECTION]["operating_cash_flow_quarterly"]["history"][7]
    assert (oldest["end"], oldest["value"]) == ("2024-09-30", 1_352 * MILLION)
    assert oldest["inputs"]["year_to_date"]["tag"] == continuing
    assert oldest["inputs"]["year_to_date_one_quarter_shorter"]["tag"] == continuing
    assert oldest["inputs"]["year_to_date_one_quarter_shorter"]["filed"] == "2025-08-06"


def test_with_no_tag_carrying_both_spans_the_quarter_is_missing():
    """Planted: the year under one tag, the nine months under the other only."""
    def row(start, end, value):
        return {"start": start, "end": end, "val": value, "accn": "P-1", "form": "10-K",
                "filed": "2026-02-01"}
    record = calculator.Record({"ticker": "TEST", "facts": {"us-gaap": {
        "Revenues": {"units": {"USD": [row("2025-01-01", "2025-12-31", 1_000.0),
                                       row("2025-01-01", "2025-09-30", 700.0)]}},
        "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations": {
            "units": {"USD": [row("2025-01-01", "2025-12-31", 400.0)]}},
        "NetCashProvidedByUsedInOperatingActivities": {
            "units": {"USD": [row("2025-01-01", "2025-09-30", 250.0)]}}}}})
    spans = calculator.durations(record.usd)
    found = calculator.quarter(record, "operating_cash_flow", spans,
                               calculator.dt.date(2025, 12, 31))
    assert "value" not in found and "different scopes" in found["missing"]


# --- the three accrual measures, side by side -----------------------------------------------

def nvidia_inputs() -> dict:
    """NVIDIA's fiscal 2026 and 2025 rows, read through the independent reader."""
    cut, now, ago = NVDA["cutoff"], "2026-01-25", "2025-01-26"
    year = "2025-01-27..2026-01-25"
    read = lambda tag, period: source.one_value("NVDA", tag, period, cut)  # noqa: E731
    return {
        "current_assets": (read("AssetsCurrent", now), read("AssetsCurrent", ago)),
        "cash": (read("CashAndCashEquivalentsAtCarryingValue", now),
                 read("CashAndCashEquivalentsAtCarryingValue", ago)),
        "current_liabilities": (read("LiabilitiesCurrent", now), read("LiabilitiesCurrent", ago)),
        "debt_current": (read("DebtCurrent", now), read("DebtCurrent", ago)),
        "taxes_payable": (read("TaxesPayableCurrent", now), read("TaxesPayableCurrent", ago)),
        "assets": (read("Assets", now), read("Assets", ago)),
        "depreciation": read("DepreciationDepletionAndAmortization", year),
        "net_income": read("NetIncomeLoss", year),
        "operating_cash_flow": read("NetCashProvidedByUsedInOperatingActivities", year),
        "capital_expenditure": read("PaymentsToAcquireProductiveAssets", year),
    }


def test_nvidias_rows_are_the_printed_figures():
    """The 10-K's balance sheet, accrued-liabilities note and cash flow statement, in millions."""
    rows = nvidia_inputs()
    assert rows["current_assets"] == (125_605 * MILLION, 80_126 * MILLION)
    assert rows["cash"] == (10_605 * MILLION, 8_589 * MILLION)
    assert rows["current_liabilities"] == (32_163 * MILLION, 18_047 * MILLION)
    assert rows["debt_current"] == (999 * MILLION, 0)
    assert rows["taxes_payable"] == (2_669 * MILLION, 881 * MILLION)
    assert rows["assets"] == (206_803 * MILLION, 111_601 * MILLION)
    assert rows["depreciation"] == 2_843 * MILLION
    assert rows["net_income"] == 120_067 * MILLION
    assert rows["operating_cash_flow"] == 102_718 * MILLION
    assert rows["capital_expenditure"] == 6_042 * MILLION


def test_balance_sheet_accruals_are_sloans_formula_worked_by_hand(nvidia):
    """Sloan: [(change in current assets - change in cash) - (change in current
    liabilities - change in debt in current liabilities - change in taxes payable)
    - depreciation and amortization] / average total assets. In millions:

      change in current assets       125,605 - 80,126 = 45,479
      change in cash                  10,605 -  8,589 =  2,016
      change in current liabilities   32,163 - 18,047 = 14,116
      change in short-term debt          999 -      0 =    999
      change in taxes payable          2,669 -    881 =  1,788
      numerator   (45,479 - 2,016) - (14,116 - 999 - 1,788) - 2,843
                = 43,463 - 11,329 - 2,843 = 29,291
      average assets  (206,803 + 111,601) / 2 = 159,202
      accruals        29,291 / 159,202
    """
    rows = nvidia_inputs()
    change = {name: rows[name][0] - rows[name][1] for name in
              ("current_assets", "cash", "current_liabilities", "debt_current", "taxes_payable")}
    numerator = ((change["current_assets"] - change["cash"])
                 - (change["current_liabilities"] - change["debt_current"] - change["taxes_payable"])
                 - rows["depreciation"])
    assert numerator == 29_291 * MILLION
    average_assets = sum(rows["assets"]) / 2
    assert average_assets == 159_202 * MILLION
    cell = nvidia[SECTION]["balance_sheet_accruals"]
    assert cell["value"] == pytest.approx(29_291 / 159_202, rel=1e-12)
    assert cell["unit"] == "ratio"
    taxes = cell["inputs"]["change_in_income_taxes_payable"]["inputs"]["now"]
    assert (taxes["tag"], taxes["accession"], taxes["filed"]) == (
        "TaxesPayableCurrent", "0001045810-26-000021", "2026-02-25")


def test_cash_flow_accruals_are_hribar_and_collins_worked_by_hand(nvidia):
    """Hribar and Collins: [income from continuing operations - (operating cash
    flow - operating cash flow of discontinued operations)] / average assets.
    NVIDIA tags no income from continuing operations and no discontinued
    operations, so the income is net income. In millions:

      (120,067 - (102,718 - 0)) / 159,202 = 17,349 / 159,202
    """
    rows = nvidia_inputs()
    assert rows["net_income"] - rows["operating_cash_flow"] == 17_349 * MILLION
    cell = nvidia[SECTION]["cash_flow_accruals"]
    assert cell["value"] == pytest.approx(17_349 / 159_202, rel=1e-12)
    income = cell["inputs"]["income_from_continuing_operations"]
    assert income["value"] == 120_067 * MILLION
    assert income["basis"].startswith("net income: the record tags neither")


def test_the_gap_between_the_first_two_measures_is_worked_by_python(nvidia):
    """The one comparison the accounting analyst is told to read, as a cell: Sloan's
    measure less Hribar and Collins's, both over NVIDIA's average assets of
    159,202 million: 29,291 / 159,202 - 17,349 / 159,202 = 11,942 / 159,202."""
    rows = nvidia_inputs()
    change = {name: rows[name][0] - rows[name][1] for name in
              ("current_assets", "cash", "current_liabilities", "debt_current", "taxes_payable")}
    sloan = ((change["current_assets"] - change["cash"])
             - (change["current_liabilities"] - change["debt_current"] - change["taxes_payable"])
             - rows["depreciation"])
    hribar = rows["net_income"] - rows["operating_cash_flow"]
    assert (sloan, hribar, sloan - hribar) == (29_291 * MILLION, 17_349 * MILLION, 11_942 * MILLION)
    cell = nvidia[SECTION]["balance_sheet_less_cash_flow_accruals"]
    assert cell["value"] == pytest.approx(11_942 / 159_202, rel=1e-12)
    assert cell["formula"] == "balance_sheet_accruals - cash_flow_accruals"
    assert set(cell["inputs"]) == {"balance_sheet_accruals", "cash_flow_accruals"}
    assert cell["inputs"]["balance_sheet_accruals"]["value"] == pytest.approx(29_291 / 159_202)
    assert cell["unit"] == "ratio"
    paragraph = " ".join((AGENTS / "accounting-analyst.md").read_text(encoding="utf-8").split())
    assert "`quarterly_cash_flow_and_accruals.balance_sheet_less_cash_flow_accruals`" in paragraph
    # the paragraph does not forbid a comparison and then ask for one: the analyst
    # compares nothing by hand, and the one gap that means something is Python's cell
    assert "never compared level for level" not in paragraph
    assert "do not compare one measure's level with another's yourself" in paragraph
    assert ("Python states the one gap that carries meaning, the first less the second, both "
            "over the same average assets, as "
            "`quarterly_cash_flow_and_accruals.balance_sheet_less_cash_flow_accruals`") in paragraph
    assert "it does not by itself say earnings were managed" in paragraph
    assert instructions_to_compute(paragraph_of(*PARAGRAPHS[0])) == []


def test_neither_paragraph_tells_an_analyst_to_do_arithmetic():
    """Python does every subtraction and division; the analysts read cells. Neither
    paragraph holds a verb of arithmetic outside a clause that tells the analyst
    not to, and the check is not a formality: a sentence planted in the accounting
    analyst's paragraph that hands over one subtraction is caught, in each of the
    verbs, while the same verb inside a prohibition is let through."""
    for name, opening in PARAGRAPHS:
        assert instructions_to_compute(paragraph_of(name, opening)) == [], name
    paragraph = paragraph_of(*PARAGRAPHS[0])
    planted = "Subtract the third from the first yourself."
    assert instructions_to_compute(f"{paragraph} {planted}") == [planted]
    middle = paragraph.replace("Operating cash flow by quarter runs from",
                               f"{planted} Operating cash flow by quarter runs from")
    assert middle != paragraph and instructions_to_compute(middle) == [planted]
    for order in ("Add up the eight quarters.", "Divide the first by average assets.",
                  "Multiply the share by revenue.", "Compute the gap for the year before.",
                  "Calculate the change in the share.", "Work out the difference in dollars.",
                  "The gap is read beside the third measure; subtract one from the other."):
        assert instructions_to_compute(f"{paragraph} {order}"), order
    for refusal in ("Do not subtract the third from the first yourself.",
                    "Never divide one measure by another.",
                    "The gap is Python's cell; never work out one of your own."):
        assert instructions_to_compute(f"{paragraph} {refusal}") == [], refusal


def test_free_cash_flow_accruals_are_the_sec_models_in_dollars(nvidia):
    """SEC Accounting Quality Model: income before extraordinary items less free
    cash flow. In millions: 120,067 - (102,718 - 6,042) = 120,067 - 96,676 = 23,391."""
    rows = nvidia_inputs()
    expected = rows["net_income"] - (rows["operating_cash_flow"] - rows["capital_expenditure"])
    assert expected == 23_391 * MILLION
    cell = nvidia[SECTION]["free_cash_flow_accruals"]
    assert cell["value"] == expected and cell["unit"] == "USD"
    capex = cell["inputs"]["capital_expenditure"]["parts"]["0"]
    assert (capex["tag"], capex["accession"], capex["filed"]) == (
        "PaymentsToAcquireProductiveAssets", "0001045810-26-000021", "2026-02-25")


def test_a_measure_whose_input_the_record_lacks_is_null_with_the_reason(cisco):
    """Cisco's 10-Q prints "Depreciation, amortization, and other", and the
    independent reader finds no us-gaap concept whose name begins with
    Depreciation carrying a row for fiscal 2026 to date (2025-07-27..2026-04-25),
    where fiscal 2025 has DepreciationDepletionAndAmortization. So Sloan's
    measure has nothing to subtract: null, never zero."""
    cut = CSCO["cutoff"]
    concepts = source.record("CSCO")["facts"]["us-gaap"]
    depreciation = [tag for tag in concepts if tag.startswith("Depreciation")]
    assert [tag for tag in depreciation
            if source.reported("CSCO", tag, "2025-07-27..2026-04-25", cut)] == []
    assert source.reported("CSCO", "DepreciationDepletionAndAmortization",
                           "2024-07-28..2025-07-26", cut)
    cell = cisco[SECTION]["balance_sheet_accruals"]
    assert cell["value"] is None
    assert cell["missing"].startswith("depreciation_and_amortization:")
    assert cisco[SECTION]["cash_flow_accruals"]["value"] is not None


def test_the_three_measures_reach_the_filings_only_view(nvidia):
    view = calculator.filings_only(nvidia)
    for name in ("balance_sheet_accruals", "cash_flow_accruals", "free_cash_flow_accruals",
                 "operating_cash_flow_quarterly"):
        assert view[SECTION][name]["value"] == nvidia[SECTION][name]["value"]


# --- income from continuing operations, planted -------------------------------------------------

def planted(extra: dict) -> calculator.Record:
    """One fiscal year of a company the test makes up, with revenue so the year exists."""
    def row(value):
        return [{"start": "2025-01-01", "end": "2025-12-31", "val": value, "accn": "P-1",
                 "form": "10-K", "filed": "2026-02-01"}]
    facts = {"Revenues": row(1_000.0), "NetIncomeLoss": row(100.0)}
    facts.update({tag: row(value) for tag, value in extra.items()})
    return calculator.Record({"ticker": "TEST", "facts": {"us-gaap": {
        tag: {"units": {"USD": rows}} for tag, rows in facts.items()}}})


def continuing(extra: dict) -> dict:
    record = planted(extra)
    periods = calculator.trigger_periods(record.usd, "2025-12-31", "10-K")
    return calculator.continuing_income(record, calculator.gather(record, periods), periods)


def test_net_income_stands_for_continuing_income_only_with_no_discontinued_line():
    assert continuing({})["value"] == 100.0
    refused = continuing({"IncomeLossFromDiscontinuedOperationsNetOfTax": -30.0})
    assert "value" not in refused
    assert refused["missing"].startswith("the record carries a discontinued-operations line")


def test_tagged_continuing_income_is_read_as_tagged():
    found = continuing({"IncomeLossFromContinuingOperations": 130.0,
                        "IncomeLossFromDiscontinuedOperationsNetOfTax": -30.0})
    assert found["value"] == 130.0
    assert found["basis"] == "income from continuing operations, as tagged"


# --- a line the record does not carry is never a zero ------------------------------------------

def test_taxes_payable_never_tagged_leaves_sloans_measure_null():
    """Generac tags neither income taxes payable nor taxes payable in any filing
    the independent reader holds, so the change in it is not a zero: Sloan's
    measure is null and says which line it lacked."""
    assert [tag for tag in ("AccruedIncomeTaxesCurrent", "TaxesPayableCurrent")
            if source.rows("GNRC", tag)] == []
    out = calculator.calculate(ticker="GNRC", cutoff="2026-08-04", period_end="2026-06-30",
                               form="10-Q")
    cell = out[SECTION]["balance_sheet_accruals"]
    assert cell["value"] is None
    assert cell["missing"].startswith("change_in_income_taxes_payable:")


def quarterly_planted(extra: dict) -> tuple:
    """A made-up quarterly filer: fiscal 2024, and six months of 2025 and of 2024."""
    spans = {"year": ("2024-01-01", "2024-12-31"), "to_date": ("2025-01-01", "2025-06-30"),
             "before": ("2024-01-01", "2024-06-30")}

    def rows(values: dict) -> list:
        return [{"start": spans[name][0], "end": spans[name][1], "val": value, "accn": "P-1",
                 "form": "10-Q", "filed": "2025-08-01"} for name, value in values.items()]
    facts = {"Revenues": rows({"year": 1_000.0, "to_date": 600.0, "before": 500.0}),
             "NetIncomeLoss": rows({"year": 100.0, "to_date": 60.0, "before": 50.0}),
             "NetCashProvidedByUsedInOperatingActivities":
                 rows({"year": 90.0, "to_date": 40.0, "before": 30.0})}
    facts["Assets"] = [{"end": end, "val": value, "accn": "P-1", "form": "10-Q",
                        "filed": "2025-08-01"}
                       for end, value in (("2025-06-30", 1_000.0), ("2024-06-30", 800.0))]
    facts.update({tag: rows(values) for tag, values in extra.items()})
    record = calculator.Record({"ticker": "TEST", "facts": {"us-gaap": {
        tag: {"units": {"USD": found}} for tag, found in facts.items()}}})
    periods = calculator.trigger_periods(record.usd, "2025-06-30", "10-Q")
    return record, calculator.gather(record, periods), periods


def test_discontinued_cash_flow_in_some_spans_only_is_missing_not_zero():
    """Planted: operating cash flow of discontinued operations in fiscal 2024 alone.
    The six months without it are not read as zero; the measure is null."""
    record, terms, periods = quarterly_planted(
        {"CashProvidedByUsedInOperatingActivitiesDiscontinuedOperations": {"year": 5.0}})
    carrying, lacking = calculator.spans_carrying(
        record, "operating_cash_flow_discontinued", periods)
    assert carrying == ["2024-01-01..2024-12-31"]
    assert lacking == ["2025-01-01..2025-06-30", "2024-01-01..2024-06-30"]
    cell = calculator.quarterly_cash_flow_and_accruals(record, terms, periods)["cash_flow_accruals"]
    assert cell["value"] is None and "not read as a zero" in cell["missing"]


def test_no_discontinued_line_anywhere_makes_continuing_cash_flow_the_total():
    """Planted, hand-worked: no discontinued line in any span, so operating cash
    flow of continuing operations is the total and the cell says why, rather than
    subtracting a zero. Trailing four quarters: income 100 + 60 - 50 = 110,
    operating cash flow 90 + 40 - 30 = 100, average assets (1,000 + 800) / 2 = 900,
    so cash-flow accruals are (110 - 100) / 900."""
    record, terms, periods = quarterly_planted({})
    cell = calculator.quarterly_cash_flow_and_accruals(record, terms, periods)["cash_flow_accruals"]
    assert cell["value"] == pytest.approx(10 / 900, rel=1e-12)
    cash = cell["inputs"]["operating_cash_flow_of_continuing_operations"]
    assert cash["value"] == 100.0 and cash["basis"].startswith("operating cash flow: the record")


# --- the analysts' paragraphs name paths that exist ---------------------------------------------

AGENTS = source.FIXTURES.parent.parent / ".claude" / "agents"
RUNS = source.FIXTURES.parent.parent / "runs"
PARAGRAPHS = (("accounting-analyst.md", "**Revenue and working capital.**"),
              ("financial-analyst.md", "**Working capital and billings.**"))


def paragraph_of(name: str, opening: str) -> str:
    """One paragraph of an analyst's definition, on one line."""
    text = (AGENTS / name).read_text(encoding="utf-8")
    return " ".join(text[text.index(opening):].split("\n\n", 1)[0].split())


ARITHMETIC = re.compile(r"\b(subtract|add(s|ed|ing)? up|divid|multipl|comput|calculat|"
                        r"work(s|ed|ing)? out)", re.IGNORECASE)
TOLD_NOT_TO = re.compile(r"\b(do not|never)\b", re.IGNORECASE)


def instructions_to_compute(paragraph: str) -> list[str]:
    """Every sentence or clause of a paragraph (cut at a full stop, a semicolon or a
    colon) that holds a verb of arithmetic and does not tell the analyst not to.
    Python does the arithmetic; a paragraph that hands any of it to the analyst
    is refused, whatever else it says."""
    return [clause for clause in re.split(r"(?<=[.;:?!])\s+", paragraph)
            if ARITHMETIC.search(clause) and not TOLD_NOT_TO.search(clause)]


def named_paths(name: str, opening: str) -> list[str]:
    """Every backticked name in one paragraph of an analyst's definition."""
    text = (AGENTS / name).read_text(encoding="utf-8")
    paragraph = text[text.index(opening):].split("\n\n", 1)[0]
    return re.findall(r"`([^`]+)`", " ".join(paragraph.split()))


@pytest.fixture(scope="module")
def committed_calculators() -> dict:
    """The calculator of every committed run, reruns included (the analysts read
    those too), computed from its own bundle. A rerun's directory name is not its
    accession, so the trigger is the one its own manifest names."""
    whole = {}
    for manifest in sorted(RUNS.glob("*/*/input_manifest.json")):
        run = manifest.parent
        stated = json.loads(manifest.read_text(encoding="utf-8"))
        accession = stated["accession"]
        trigger, = {(d["form"], d["report_date"]) for d in stated["documents"]
                    if d.get("accession") == accession}
        whole[f"{run.parent.name}/{run.name}"] = (stated["cutoff"], calculator.calculate(
            ticker=run.parent.name, cutoff=stated["cutoff"], period_end=trigger[1],
            form=trigger[0], accession=accession, bundle=run))
    return whole


@pytest.fixture(scope="module")
def committed_views(committed_calculators) -> dict:
    """The filings-only view of every committed run, as the two analysts read it."""
    return {run: calculator.filings_only(payload)
            for run, (_, payload) in committed_calculators.items()}


def test_every_path_the_analysts_are_told_resolves_in_every_committed_run(committed_views):
    """Each name is a field the analyst may cite: the gate's own `resolve` finds it in
    every run's calculator_filings_only.json, it is a cell holding `value`, and
    where that value is a number `placeholder_value` prints that number. A null
    cell names its reason under `missing`."""
    assert len(committed_views) == len(list(RUNS.glob("*/*/input_manifest.json")))
    assert any("rerun" in run for run in committed_views)
    for name, opening in PARAGRAPHS:
        paths = named_paths(name, opening)
        assert len(paths) >= 10, name
        for path in paths:
            for run, view in committed_views.items():
                try:
                    node = analysis_check.resolve(view, path)
                except KeyError:
                    pytest.fail(f"{name} names {path}, which {run}'s view does not carry")
                assert isinstance(node, dict) and "value" in node, (name, path, run)
                if node["value"] is None:
                    assert node.get("missing"), (name, path, run)
                else:
                    assert analysis_check.placeholder_value(view, path) == node["value"], \
                        (name, path, run)


def test_the_past_due_share_carries_its_year_earlier_when_nothing_is_found(committed_views):
    """Most runs hold no past-due fact; the year-earlier cell is there anyway, null
    with its reason, so the path the accounting analyst is told never fails."""
    nulls = [view["receivables_extension"]["past_due_receivables_share"]
             for view in committed_views.values()
             if view["receivables_extension"]["past_due_receivables_share"]["value"] is None]
    assert nulls
    for cell in nulls:
        assert cell["as_of"] is None
        assert cell["a_year_earlier"]["value"] is None and cell["a_year_earlier"]["missing"]


# --- a trailing year is never a sum of two concepts ------------------------------------------------

def test_a_trailing_year_is_read_under_one_tag():
    """Johnson Controls' operating cash flow over the four quarters to 2025-06-30,
    through the independent reader: fiscal 2024 (2023-10-01..2024-09-30) 1,568
    million and the nine months to 2025-06-30 1,586 million, both under the
    continuing-operations tag; the nine months to 2024-06-30 under it as 216 and
    under the total tag as 572. Under one tag: 1,568 + 1,586 - 216 = 2,938, never
    1,568 + 1,586 - 572 = 2,582 across two."""
    cut, continuing = "2026-07-29", "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations"
    year, to_date = "2023-10-01..2024-09-30", "2024-10-01..2025-06-30"
    before = "2023-10-01..2024-06-30"
    assert source.one_value("JCI", continuing, year, cut) == 1_568 * MILLION
    assert source.one_value("JCI", continuing, to_date, cut) == 1_586 * MILLION
    assert source.one_value("JCI", continuing, before, cut) == 216 * MILLION
    assert cfo("JCI", before, cut) == 572 * MILLION
    bundle = source.FIXTURES.parent.parent / "runs" / "JCI" / "0000833444-26-000087"
    out = calculator.calculate(ticker="JCI", cutoff=cut, period_end="2026-06-30", form="10-Q",
                               bundle=bundle)
    ago = out["terms"]["trailing_four_quarters_a_year_earlier"]["operating_cash_flow"]
    assert ago["value"] == 2_938 * MILLION
    assert {part["tag"] for part in ago["parts"].values()} == {continuing}


def mixed_planted(cash_tags: dict, revenue_tags: dict) -> tuple:
    """A made-up quarterly filer whose spans may sit under different tags."""
    spans = {"year": ("2024-01-01", "2024-12-31"), "to_date": ("2025-01-01", "2025-06-30"),
             "before": ("2024-01-01", "2024-06-30")}
    values = {"year": 90.0, "to_date": 40.0, "before": 30.0}
    facts: dict = {}
    for tags, scale in ((cash_tags, 1.0), (revenue_tags, 10.0)):
        for name, tag in tags.items():
            facts.setdefault(tag, []).append(
                {"start": spans[name][0], "end": spans[name][1], "val": values[name] * scale,
                 "accn": "P-1", "form": "10-Q", "filed": "2025-08-01"})
    facts["NetIncomeLoss"] = [{"start": s, "end": e, "val": 10.0, "accn": "P-1", "form": "10-Q",
                               "filed": "2025-08-01"} for s, e in spans.values()]
    facts["AccountsReceivableNetCurrent"] = [
        {"end": end, "val": value, "accn": "P-1", "form": "10-Q", "filed": "2025-08-01"}
        for end, value in (("2025-06-30", 120.0), ("2024-06-30", 100.0))]
    record = calculator.Record({"ticker": "TEST", "facts": {"us-gaap": {
        tag: {"units": {"USD": rows}} for tag, rows in facts.items()}}})
    periods = calculator.trigger_periods(record.usd, "2025-06-30", "10-Q")
    return record, periods


def test_a_mixed_tag_trailing_sum_is_refused_not_labelled_continuing():
    """Planted: the fiscal year under the continuing-operations tag, both years to
    date under the total tag, no tag on all three. The trailing sum is missing,
    and the Hribar and Collins measure is not handed a continuing-operations
    figure built across the two."""
    continuing, total = ("NetCashProvidedByUsedInOperatingActivitiesContinuingOperations",
                         "NetCashProvidedByUsedInOperatingActivities")
    revenue = "Revenues"
    record, periods = mixed_planted({"year": continuing, "to_date": total, "before": total},
                                    {"year": revenue, "to_date": revenue, "before": revenue})
    terms = calculator.gather(record, periods)
    cash = terms["trailing_four_quarters"]["operating_cash_flow"]
    assert "value" not in cash and "different scopes" in cash["missing"]
    section = calculator.quarterly_cash_flow_and_accruals(record, terms, periods)
    assert section["cash_flow_accruals"]["value"] is None
    assert "different scopes" in section["cash_flow_accruals"]["missing"]


def test_a_growth_gap_never_divides_by_a_mixed_tag_revenue():
    """Planted: revenue a year earlier would mix two revenue tags (the fiscal year
    under one, the six months before it under another), so every growth gap is
    missing with that reason rather than measured against a sum of two concepts."""
    cash = "NetCashProvidedByUsedInOperatingActivities"
    record, periods = mixed_planted(
        {"year": cash, "to_date": cash, "before": cash},
        {"year": "Revenues", "to_date": "Revenues",
         "before": "RevenueFromContractWithCustomerExcludingAssessedTax"})
    terms = calculator.gather(record, periods)
    revenue = terms["trailing_four_quarters"]["revenue"]
    assert "value" not in revenue and "different scopes" in revenue["missing"]
    receivables = calculator.receivables_extension(record, terms, periods, [])
    gap = receivables["receivables_growth_minus_revenue_growth"]
    assert gap["value"] is None
    assert gap["missing"].startswith("revenue_growth:")
    assert "different scopes" in gap["missing"]
    index = receivables["days_sales_outstanding_index"]
    assert index["value"] is None and "different scopes" in index["missing"]


# --- a trailing year and a quarter are held to one scope of their term --------------------------

DEPRECIATION = "DepreciationDepletionAndAmortization"
TWO_LINES = "Depreciation + AmortizationOfIntangibleAssets"


def test_the_same_concept_table_names_tags_of_each_terms_chain_once():
    """One structure, read here: every tag in a group is in that term's chain (or is
    the two-line depreciation reading), no tag is in two groups, and the two
    operating-cash-flow tags are two scopes."""
    for term, groups in calculator.SAME_CONCEPT.items():
        chain = set(calculator.TERMS[term][1]) | {calculator.TWO_LINE_DEPRECIATION}
        seen: list[str] = []
        for group in groups:
            for tag in group:
                assert tag in chain, (term, tag)
                assert tag not in seen, (term, tag)
                seen.append(tag)
    assert calculator.scope_of("operating_cash_flow", "NetCashProvidedByUsedInOperatingActivities") \
        != calculator.scope_of("operating_cash_flow",
                               "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations")
    assert calculator.scope_of("capital_expenditure", "PaymentsToAcquireProductiveAssets") == \
        calculator.scope_of("capital_expenditure", "PaymentsToAcquirePropertyPlantAndEquipment")
    # a tag in no group is a scope of its own, so an undeclared chain is read strictly
    assert calculator.scope_of("revenue", "Revenues") == "Revenues"
    assert calculator.SCOPE_RULE is True


def depreciation_planted(by_span: dict) -> tuple:
    """A made-up quarterly filer whose depreciation sits, span by span, under the
    tags `by_span` names: fiscal 2024, six months of 2025 and six months of 2024,
    and fiscal 2024's nine months for the fourth quarter."""
    spans = {"year": ("2024-01-01", "2024-12-31"), "to_date": ("2025-01-01", "2025-06-30"),
             "before": ("2024-01-01", "2024-06-30"), "nine": ("2024-01-01", "2024-09-30")}
    facts: dict = {"Revenues": []}
    for name, span in spans.items():
        facts["Revenues"].append({"start": span[0], "end": span[1], "val": 1_000.0, "accn": "P-1",
                                  "form": "10-Q", "filed": "2025-08-01"})
        for tag, value in by_span.get(name, {}).items():
            facts.setdefault(tag, []).append(
                {"start": span[0], "end": span[1], "val": value, "accn": "P-1", "form": "10-Q",
                 "filed": "2025-08-01"})
    record = calculator.Record({"ticker": "TEST", "facts": {"us-gaap": {
        tag: {"units": {"USD": rows}} for tag, rows in facts.items()}}})
    return record, calculator.trigger_periods(record.usd, "2025-06-30", "10-Q")


def test_a_year_the_filer_tags_as_two_lines_in_every_span_is_summed():
    """Planted: no total tagged anywhere, Depreciation and AmortizationOfIntangibleAssets
    in every span. Hand-summed: (70 + 30) + (40 + 15) - (35 + 10) = 100 + 55 - 45 = 110."""
    lines = {"year": {"Depreciation": 70.0, "AmortizationOfIntangibleAssets": 30.0},
             "to_date": {"Depreciation": 40.0, "AmortizationOfIntangibleAssets": 15.0},
             "before": {"Depreciation": 35.0, "AmortizationOfIntangibleAssets": 10.0}}
    record, periods = depreciation_planted(lines)
    found = calculator.trailing(record, "depreciation_and_amortization", periods)
    assert found["value"] == 110.0
    assert {part["tag"] for part in found["parts"].values()} == {TWO_LINES}
    assert "tags_differ" not in found


def test_a_span_under_the_total_tag_beside_spans_under_two_lines_is_summed_and_marked():
    """Planted, the lens's case: fiscal 2024 tagged DepreciationDepletionAndAmortization
    (100), the six months of 2025 and of 2024 as two lines only (40 + 15, 35 + 10).
    The total tag and the two lines are one concept, so the year is
    100 + 55 - 45 = 110, with the tags it mixes named under `tags_differ`."""
    lines = {"year": {DEPRECIATION: 100.0},
             "to_date": {"Depreciation": 40.0, "AmortizationOfIntangibleAssets": 15.0},
             "before": {"Depreciation": 35.0, "AmortizationOfIntangibleAssets": 10.0}}
    record, periods = depreciation_planted(lines)
    found = calculator.trailing(record, "depreciation_and_amortization", periods)
    assert found["value"] == 110.0
    assert found["tags_differ"] == sorted([DEPRECIATION, TWO_LINES])
    assert found["parts"]["prior_fiscal_year"]["tag"] == DEPRECIATION
    assert found["parts"]["this_year_to_date"]["tag"] == TWO_LINES
    # and a rename of the total: 100 under DepreciationAndAmortization, the rest under
    # DepreciationDepletionAndAmortization -- one concept, 100 + 55 - 45 = 110, marked
    renamed = {"year": {"DepreciationAndAmortization": 100.0}, "to_date": {DEPRECIATION: 55.0},
               "before": {DEPRECIATION: 45.0}}
    record, periods = depreciation_planted(renamed)
    found = calculator.trailing(record, "depreciation_and_amortization", periods)
    assert found["value"] == 110.0
    assert found["tags_differ"] == sorted([DEPRECIATION, "DepreciationAndAmortization"])


def test_a_quarter_differenced_from_two_lines_in_both_spans_is_read_under_them():
    """Planted: fiscal 2024 and its nine months as two lines only. The fourth
    quarter is (70 + 30) - (50 + 20) = 30; and with the year under the total tag
    instead, one concept still, 100 - 70 = 30."""
    lines = {"year": {"Depreciation": 70.0, "AmortizationOfIntangibleAssets": 30.0},
             "nine": {"Depreciation": 50.0, "AmortizationOfIntangibleAssets": 20.0}}
    record, _ = depreciation_planted(lines)
    found = calculator.quarter(record, "depreciation_and_amortization",
                               calculator.durations(record.usd), calculator.dt.date(2024, 12, 31))
    assert found["value"] == 30.0
    assert [part["tag"] for part in found["parts"]] == [TWO_LINES, TWO_LINES]
    lines["year"] = {DEPRECIATION: 100.0}
    record, _ = depreciation_planted(lines)
    found = calculator.quarter(record, "depreciation_and_amortization",
                               calculator.durations(record.usd), calculator.dt.date(2024, 12, 31))
    assert found["value"] == 30.0
    assert [part["tag"] for part in found["parts"]] == [DEPRECIATION, TWO_LINES]


def test_two_scopes_with_one_on_record_in_every_span_are_read_under_that_scope():
    """Planted in Johnson Controls' shape: the fiscal year under the continuing-operations
    tag alone (90), the six months of 2025 under it alone (40), the six months of
    2024 under both (total 80, continuing 30). Continuing operations is the one
    scope on record in every span: 90 + 40 - 30 = 100, never 90 + 40 - 80 = 50."""
    continuing, total = ("NetCashProvidedByUsedInOperatingActivitiesContinuingOperations",
                         "NetCashProvidedByUsedInOperatingActivities")
    record, periods = mixed_planted({"year": continuing, "to_date": continuing, "before": total},
                                    {"year": "Revenues", "to_date": "Revenues", "before": "Revenues"})
    record.usd[continuing][("2024-01-01", "2024-06-30")] = [
        dict(record.usd[total][("2024-01-01", "2024-06-30")][0], val=30.0)]
    found = calculator.trailing(record, "operating_cash_flow", periods)
    assert found["value"] == 100.0
    assert {part["tag"] for part in found["parts"].values()} == {continuing}
    assert "tags_differ" not in found


def test_fortinets_capital_expenditure_is_summed_across_its_two_tags_as_the_statement_prints_it():
    """Fortinet, through the independent reader: its 10-Q for the six months to
    2026-06-30 tags purchases of property and equipment
    PaymentsToAcquirePropertyPlantAndEquipment, 148.6 million, and puts
    PaymentsToAcquireProductiveAssets on a sentence inside them -- "we purchased
    certain real estate property in the United States totaling $62.1 million". Its
    10-K tags the whole line for 2025 PaymentsToAcquireProductiveAssets, 364.8, and
    both tags carry the six months to 2025-06-30 at 234.3. The two tags are one
    concept, each span read under the first of them the record carries there:
    364.8 + 148.6 - 234.3 = 279.1 million, as the published run printed it, marked
    `tags_differ`. A year under the one tag that carries all three spans would be
    364.8 + 62.1 - 234.3 = 192.6: a statement line plus a sentence, which this
    does not print."""
    cut = "2026-07-30"
    line, sentence = ("PaymentsToAcquirePropertyPlantAndEquipment",
                      "PaymentsToAcquireProductiveAssets")
    assert source.one_value("FTNT", line, "2026-01-01..2026-06-30", cut) == 148.6 * MILLION
    assert source.one_value("FTNT", sentence, "2026-01-01..2026-06-30", cut) == 62.1 * MILLION
    assert source.one_value("FTNT", sentence, "2025-01-01..2025-12-31", cut) == 364.8 * MILLION
    assert source.one_value("FTNT", line, "2025-01-01..2025-06-30", cut) == 234.3 * MILLION
    assert source.one_value("FTNT", sentence, "2025-01-01..2025-06-30", cut) == 234.3 * MILLION
    assert source.reported("FTNT", line, "2025-01-01..2025-12-31", cut) == []
    assert round(364.8 + 148.6 - 234.3, 1) == 279.1 and round(364.8 + 62.1 - 234.3, 1) == 192.6
    bundle = source.FIXTURES.parent.parent / "runs" / "FTNT" / "0001262039-26-000021"
    out = calculator.calculate(ticker="FTNT", cutoff=cut, period_end="2026-06-30", form="10-Q",
                               bundle=bundle)
    cell = out["terms"]["trailing_four_quarters"]["capital_expenditure"]
    assert cell["value"] == pytest.approx(279.1 * MILLION)
    assert cell["parts"]["this_year_to_date"]["tag"] == line
    assert cell["parts"]["prior_fiscal_year"]["tag"] == sentence
    assert cell["tags_differ"] == sorted([line, sentence])
    assert out["free_cash_flow"]["free_cash_flow_simple"]["value"] == pytest.approx(
        out["terms"]["trailing_four_quarters"]["operating_cash_flow"]["value"] - 279.1 * MILLION)


def test_two_scopes_with_none_on_record_in_every_span_are_missing():
    """Planted: operating cash flow under the continuing-operations tag in the fiscal
    year and under the total in both six-month spans, no span under both. Neither
    scope reaches every span: missing with the reason, never 90 + 40 - 30 across
    the two."""
    continuing, total = ("NetCashProvidedByUsedInOperatingActivitiesContinuingOperations",
                         "NetCashProvidedByUsedInOperatingActivities")
    record, periods = mixed_planted({"year": continuing, "to_date": total, "before": total},
                                    {"year": "Revenues", "to_date": "Revenues", "before": "Revenues"})
    found = calculator.trailing(record, "operating_cash_flow", periods)
    assert "value" not in found
    assert "different scopes of operating_cash_flow" in found["missing"]
    assert f"prior fiscal year under us-gaap:{continuing}" in found["missing"]


# --- the cash side of Hribar and Collins beside a discontinued-operations income line --------

def test_a_total_operating_cash_flow_beside_discontinued_income_is_not_called_continuing():
    """Planted in Western Digital's shape: income from discontinued operations tagged
    for the fiscal year, operating cash flow as the total in every span, and no
    operating cash flow of discontinued operations anywhere. The total is not the
    continuing figure, so the cash side is missing with the reason, and so is the
    measure; it is not read as the total less a zero."""
    record, terms, periods = quarterly_planted(
        {"IncomeLossFromDiscontinuedOperationsNetOfTax": {"year": 5.0},
         "IncomeLossFromContinuingOperations": {"year": 95.0, "to_date": 60.0, "before": 50.0}})
    section = calculator.quarterly_cash_flow_and_accruals(record, terms, periods)
    cell = section["cash_flow_accruals"]
    assert cell["value"] is None
    assert "discontinued-operations income line for 2024-01-01..2024-12-31" in cell["missing"]
    assert "operating cash flow of continuing operations is not on record" in cell["missing"]
    # the SEC model's measure reads the same cash side, and is refused with it
    sec = section["free_cash_flow_accruals"]
    assert sec["value"] is None and sec["missing"] == cell["missing"]


def test_western_digitals_cash_side_is_refused_on_its_own_record():
    """Western Digital, through the independent reader, over the spans the trailing
    year reads (fiscal 2025, 2024-06-29..2025-06-27; the nine months to 2026-04-03
    and to 2025-03-28): income from continuing operations 1,643, 6,229 and 1,391;
    income from discontinued operations 246 and 216 (fiscal 2025 and the nine months
    to 2025-03-28; 468 for the six months to 2024-12-27); operating cash flow 1,691,
    2,540 and 945 under the total tag and nothing under the continuing-operations
    tag; purchases of property and equipment 412, 310 and 341. Both measures that
    pair income with operating cash flow are missing with the reason: the Hribar
    and Collins measure, and the SEC model's, which would otherwise have been
    (1,643 + 6,229 - 1,391) - ((1,691 + 2,540 - 945) - (412 + 310 - 341)) =
    6,481 - (3,286 - 381) = 3,576 across two scopes, and is not printed."""
    cut = "2026-05-01"
    year, to_date, before = "2024-06-29..2025-06-27", "2025-06-28..2026-04-03", "2024-06-29..2025-03-28"
    continuing_income = "IncomeLossFromContinuingOperations"
    discontinued = "IncomeLossFromDiscontinuedOperationsNetOfTaxAttributableToReportingEntity"
    assert [source.one_value("WDC", continuing_income, span, cut) for span in (year, to_date, before)] \
        == [1_643 * MILLION, 6_229 * MILLION, 1_391 * MILLION]
    assert source.one_value("WDC", discontinued, year, cut) == 246 * MILLION
    assert source.one_value("WDC", discontinued, before, cut) == 216 * MILLION
    assert source.one_value("WDC", discontinued, "2024-06-29..2024-12-27", cut) == 468 * MILLION
    assert source.one_value("WDC", "NetIncomeLoss", year, cut) == 1_889 * MILLION
    assert [cfo("WDC", span, cut) for span in (year, to_date, before)] \
        == [1_691 * MILLION, 2_540 * MILLION, 945 * MILLION]
    for span in (year, to_date, before):
        assert source.reported("WDC", "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations",
                               span, cut) == []
    assert [source.one_value("WDC", "PaymentsToAcquirePropertyPlantAndEquipment", span, cut)
            for span in (year, to_date, before)] == [412 * MILLION, 310 * MILLION, 341 * MILLION]
    assert (1_643 + 6_229 - 1_391) - ((1_691 + 2_540 - 945) - (412 + 310 - 341)) == 3_576
    bundle = source.FIXTURES.parent.parent / "runs" / "WDC" / "0001628280-26-029054"
    out = calculator.calculate(ticker="WDC", cutoff=cut, period_end="2026-04-03", form="10-Q",
                               bundle=bundle)
    assert out["terms"]["trailing_four_quarters"]["operating_cash_flow"]["value"] == 3_286 * MILLION
    cell = out[SECTION]["cash_flow_accruals"]
    assert cell["value"] is None
    assert "operating cash flow of continuing operations is not on record" in cell["missing"]
    sec = out[SECTION]["free_cash_flow_accruals"]
    assert sec["value"] is None and sec["missing"] == cell["missing"]
    assert "2024-06-29..2025-06-27" in sec["missing"]


# --- the pairing of continuing-operations cash flow with total net income is named -----------

def bundle_fact(run, tag: str, start: str, end: str, cutoff: str) -> float:
    """One entity-wide fact of a run's own bundle (`input_numbers.json`), where the
    fixture store's companyfacts predates the triggering filing: read here by the
    test, not through `src/`."""
    facts = json.loads((run / "input_numbers.json").read_text(encoding="utf-8"))["facts"]
    values = {fact["number"] for fact in facts
              if fact["tag"] == tag and not fact.get("nil") and not fact.get("superseded_by")
              and not (fact.get("context") or {}).get("segment")
              and (fact.get("context") or {}).get("start") == start
              and (fact.get("context") or {}).get("end") == end
              and fact.get("filing_date", "9999") <= cutoff}
    assert len(values) == 1, (tag, start, end, values)
    return values.pop()


def test_johnson_controls_cross_scope_pairing_is_named_where_it_occurs():
    """Johnson Controls' record holds operating cash flow under the continuing-operations
    tag alone and net income as the total; `earnings_versus_cash` pairs them as it
    did, and now says so beside each ratio. For the four quarters to 2026-06-30:
    operating cash flow 2,554 + 2,572 - 1,586 = 3,540 (fiscal 2025 and the nine
    months of 2025 through the independent reader; the nine months of 2026 from the
    run's own bundle, the store's companyfacts predating the 10-Q) and net income
    3,291 + 1,886 - 1,598 = 3,579, so the ratio is 3,540 / 3,579."""
    cut, continuing = "2026-07-29", "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations"
    bundle = source.FIXTURES.parent.parent / "runs" / "JCI" / "0000833444-26-000087"
    assert source.one_value("JCI", continuing, "2024-10-01..2025-09-30", cut) == 2_554 * MILLION
    assert source.one_value("JCI", continuing, "2024-10-01..2025-06-30", cut) == 1_586 * MILLION
    assert bundle_fact(bundle, continuing, "2025-10-01", "2026-06-30", cut) == 2_572 * MILLION
    assert source.one_value("JCI", "NetIncomeLoss", "2024-10-01..2025-09-30", cut) == 3_291 * MILLION
    assert source.one_value("JCI", "NetIncomeLoss", "2024-10-01..2025-06-30", cut) == 1_598 * MILLION
    assert bundle_fact(bundle, "NetIncomeLoss", "2025-10-01", "2026-06-30", cut) == 1_886 * MILLION
    assert source.reported("JCI", "NetCashProvidedByUsedInOperatingActivities",
                           "2024-10-01..2025-09-30", cut) == []
    out = calculator.calculate(ticker="JCI", cutoff=cut, period_end="2026-06-30", form="10-Q",
                               bundle=bundle)
    ratio = out["earnings_versus_cash"]["operating_cash_flow_over_net_income"]
    assert ratio["value"] == pytest.approx(3_540 / 3_579, rel=1e-12)
    assert ratio["note"].startswith("operating cash flow is of continuing operations")
    assert out["earnings_versus_cash"]["accruals_over_average_assets"]["note"] == ratio["note"]
    history = out["earnings_versus_cash"]["history"]
    assert history["note"] == ratio["note"]
    assert history["years"][0]["operating_cash_flow"] == 2_554 * MILLION       # fiscal 2025, continuing
    assert history["years"][0]["net_income"] == 3_291 * MILLION                # the total: 0.776 across scopes
    # NVIDIA's record pairs the total with the total: no note
    nvidia = calculator.calculate(**NVDA)
    assert "note" not in nvidia["earnings_versus_cash"]["operating_cash_flow_over_net_income"]


# --- the cost of debt's fallback reason is written only when it is true -----------------------

def decimals_in_the_instance(ticker: str, form: str, name: str, tag: str) -> set:
    """The `decimals` every fact of one tag carries in a committed XBRL instance,
    read by this test's own regular expression."""
    raw = gzip.decompress((source.FIXTURES / ticker / form / name).read_bytes()).decode("utf-8")
    return set(re.findall(rf'<us-gaap:{tag} [^>]*decimals="(-?\d+)"', raw))


def test_dells_interest_expense_is_two_scopes_and_its_cost_of_debt_is_its_last_fiscal_years():
    """Dell, through the independent reader. Its 10-K tags InterestExpenseNonoperating
    1,560 for fiscal 2026 and the earlier 10-Q 753 for the six months to 2025-08-01;
    the triggering 10-Q tags only InterestExpenseDebt, 800 for both six-month spans,
    on the debt note's sentence about total interest expense related to its
    outstanding debt, "$0.8 billion for both the six months ended" (the whole
    sentence is read below). InterestExpenseDebt is interest on debt alone, a
    scope of its own; and in the instance every such fact carries decimals of -8
    ($0.1 billion) where the 10-K's interest expense carries -6 (the million), so
    the published 1,560 + 800 - 753 = 1,607 was not like for like on either count.
    Neither scope is on record in every span, so interest expense is missing with
    the reason.

    The cost of debt then steps down its ladder. Interest paid is on record for
    fiscal 2026 alone (1,354), so the trailing rung is missing and the
    last-fiscal-year rung is read, interest expense before interest paid: fiscal
    2026's own 1,560 over the average of debt at that year's end and start,
    (7,990 + 23,513 + 5,204 + 19,363) / 2 = 28,035, 0.055645 -- not over the
    trailing balances of 2026-07-31 and 2025-08-01 (31,577.5), a different year.
    The cell names both periods, and the label says the years to date state
    interest expense too, in two scopes, so that no trailing sum is taken --
    never that they do not state it, and never that neither figure is on record."""
    cut = "2026-09-08"
    nonoperating, debt = "InterestExpenseNonoperating", "InterestExpenseDebt"
    year, to_date, before = "2025-02-01..2026-01-30", "2026-01-31..2026-07-31", "2025-02-01..2025-08-01"
    assert source.one_value("DELL", nonoperating, year, cut) == 1_560 * MILLION
    assert source.one_value("DELL", nonoperating, before, cut) == 753 * MILLION
    assert source.one_value("DELL", debt, to_date, cut) == 800 * MILLION
    assert source.one_value("DELL", debt, before, cut) == 800 * MILLION
    assert source.reported("DELL", nonoperating, to_date, cut) == []
    assert source.reported("DELL", debt, year, cut) == []
    assert decimals_in_the_instance("DELL", "10-Q", "dell-20260731_htm.xml.gz", debt) == {"-8"}
    assert decimals_in_the_instance("DELL", "10-K", "dell-20260130_htm.xml.gz", nonoperating) == {"-6"}
    notes = (source.FIXTURES.parent.parent / "runs" / "DELL" / "0001571996-26-000046"
             / "input_notes.md").read_text(encoding="utf-8")
    assert ("Total interest expense related to the Company\u2019s outstanding debt was $0.4 billion "
            "for both the three months ended July\u00a031, 2026 and August\u00a01, 2025, and "
            "$0.8 billion for both the six months ended July\u00a031, 2026 and August\u00a01, 2025"
            ) in notes
    assert calculator.scope_of("interest_expense", debt) != calculator.scope_of("interest_expense",
                                                                                nonoperating)
    paid = source.one_value("DELL", "InterestPaidNet", year, cut)
    assert paid == 1_354 * MILLION
    assert source.reported("DELL", "InterestPaidNet", to_date, cut) == []
    assert source.reported("DELL", "InterestPaidNet", before, cut) == []
    debt_lines = [source.one_value("DELL", tag, date, cut) for tag, date in (
        ("DebtCurrent", "2026-01-30"), ("LongTermDebtNoncurrent", "2026-01-30"),
        ("DebtCurrent", "2025-01-31"), ("LongTermDebtNoncurrent", "2025-01-31"))]
    assert debt_lines == [7_990 * MILLION, 23_513 * MILLION, 5_204 * MILLION, 19_363 * MILLION]
    assert sum(debt_lines) / 2 == 28_035 * MILLION
    trailing_lines = [source.one_value("DELL", tag, date, cut) for tag, date in (
        ("DebtCurrent", "2026-07-31"), ("LongTermDebtNoncurrent", "2026-07-31"),
        ("DebtCurrent", "2025-08-01"), ("LongTermDebtNoncurrent", "2025-08-01"))]
    assert sum(trailing_lines) / 2 == 31_577.5 * MILLION

    dell = calculator.calculate(ticker="DELL", cutoff=cut, period_end="2026-07-31", form="10-Q",
                                bundle=source.FIXTURES.parent.parent / "runs" / "DELL"
                                / "0001571996-26-000046")
    interest = dell["terms"]["trailing_four_quarters"]["interest_expense"]
    assert "value" not in interest
    assert "different scopes of interest_expense" in interest["missing"]
    assert f"this year to date under us-gaap:{debt}" in interest["missing"]
    cost = dell["cost_of_capital"]["pre_tax_cost_of_debt"]
    assert cost["value"] == pytest.approx(1_560 / 28_035, rel=1e-12)
    assert cost["value"] != pytest.approx(1_560 / 31_577.5, rel=1e-6)
    assert cost["formula"] == "interest_expense_last_fiscal_year / average debt over that fiscal year"
    assert cost["inputs"]["interest_expense_last_fiscal_year"]["tag"] == nonoperating
    assert cost["periods"] == {"numerator": year, "denominator": ["2025-01-31", "2026-01-30"]}
    # the years to date do state interest expense -- 800 under the debt-only tag for
    # the six months to 2026-07-31, 753 under the whole-line tag for those to
    # 2025-08-01, each read above -- so the label says that, and never that they do not
    assert cost["fallback"].startswith(
        f"interest expense over the last fiscal year ({year}) over the average of debt at that "
        f"year's start and end (2025-01-31 and 2026-01-30), which the years to date state too "
        f"({to_date} under us-gaap:{debt}; {before} under us-gaap:{nonoperating}), the spans "
        f"falling in two scopes, so no trailing sum is taken, because interest expense is on "
        f"record but its spans fall in two scopes: ")
    assert "do not state" not in cost["fallback"]
    assert "neither interest expense nor interest paid" not in cost["fallback"]


def test_carriers_cost_of_debt_says_its_interest_expense_is_on_record_for_the_year():
    """Carrier, through the independent reader: its 10-K tags InterestExpenseDebt 458
    for 2025, the one interest tag it carries for the year, and its 10-Q states no
    interest expense for the six months to 2026-06-30 under any of the four tags.
    So the trailing sum is missing -- and the label says interest expense is on
    record for the last fiscal year and not for every span, where the published
    run said "neither interest expense nor interest paid is on record". The rung
    reads that year's 458 over the average of debt at its end and start,
    (468 + 11,365 + 1,336 + 11,026) / 2 = 12,097.5, 0.037859."""
    cut, year, to_date = "2026-07-28", "2025-01-01..2025-12-31", "2026-01-01..2026-06-30"
    assert source.one_value("CARR", "InterestExpenseDebt", year, cut) == 458 * MILLION
    for tag in ("InterestExpense", "InterestExpenseNonoperating"):
        assert source.reported("CARR", tag, year, cut) == []
    for tag in ("InterestExpense", "InterestExpenseNonoperating", "InterestExpenseDebt",
                "InterestAndDebtExpense"):
        assert source.reported("CARR", tag, to_date, cut) == []
    debt_lines = [source.one_value("CARR", tag, date, cut) for tag, date in (
        ("DebtCurrent", "2025-12-31"), ("LongTermDebtAndCapitalLeaseObligations", "2025-12-31"),
        ("DebtCurrent", "2024-12-31"), ("LongTermDebtAndCapitalLeaseObligations", "2024-12-31"))]
    assert debt_lines == [468 * MILLION, 11_365 * MILLION, 1_336 * MILLION, 11_026 * MILLION]
    assert sum(debt_lines) / 2 == 12_097.5 * MILLION
    run = source.FIXTURES.parent.parent / "runs" / "CARR" / "0001783180-26-000032-rerun-2026-10-28"
    out = calculator.calculate(ticker="CARR", cutoff=cut, period_end="2026-06-30", form="10-Q",
                               accession="0001783180-26-000032", bundle=run)
    cost = out["cost_of_capital"]["pre_tax_cost_of_debt"]
    assert cost["value"] == pytest.approx(458 / 12_097.5, rel=1e-12)
    assert cost["inputs"]["interest_expense_last_fiscal_year"]["tag"] == "InterestExpenseDebt"
    assert cost["periods"] == {"numerator": year, "denominator": ["2024-12-31", "2025-12-31"]}
    assert (f"because interest expense is on record for the last fiscal year ({year}) and not "
            f"for every span of the trailing four quarters: ") in cost["fallback"]
    assert "not on record" not in cost["fallback"].split("because", 1)[1].split(":", 1)[0]
    assert "neither interest expense nor interest paid" not in cost["fallback"]


def test_fortinets_interest_expense_is_one_scope_and_its_cost_of_debt_reads_it():
    """Fortinet, through the independent reader: InterestExpense 20.1 for 2025 (the
    10-K) and InterestExpenseNonoperating 7.4 and 9.5 for the six months to
    2026-06-30 and 2025-06-30 (the 10-Q, both halves under one tag), two names of
    one line: 20.1 + 7.4 - 9.5 = 18.0 million, marked `tags_differ`. Its cost of
    debt is interest expense over average debt and no fallback is written."""
    cut = "2026-07-30"
    assert source.one_value("FTNT", "InterestExpense", "2025-01-01..2025-12-31", cut) == 20.1 * MILLION
    assert source.one_value("FTNT", "InterestExpenseNonoperating", "2026-01-01..2026-06-30", cut) \
        == 7.4 * MILLION
    assert source.one_value("FTNT", "InterestExpenseNonoperating", "2025-01-01..2025-06-30", cut) \
        == 9.5 * MILLION
    assert round(20.1 + 7.4 - 9.5, 1) == 18.0
    fortinet = calculator.calculate(ticker="FTNT", cutoff=cut, period_end="2026-06-30", form="10-Q",
                                    bundle=source.FIXTURES.parent.parent / "runs" / "FTNT"
                                    / "0001262039-26-000021")
    interest = fortinet["terms"]["trailing_four_quarters"]["interest_expense"]
    assert interest["value"] == pytest.approx(18.0 * MILLION)
    assert interest["tags_differ"] == ["InterestExpense", "InterestExpenseNonoperating"]
    cost = fortinet["cost_of_capital"]["pre_tax_cost_of_debt"]
    assert cost["formula"] == "interest_expense / average debt" and "fallback" not in cost


def test_the_ladder_says_how_each_input_stood_and_neither_only_when_true():
    """Planted, each called as `cost_of_capital` calls the ladder: trailing debt of 100
    at both dates, the last fiscal year's own debt 40 at its start and 60 at its end
    (average 50), and a risk-free rate of 4%.

    - interest expense in two scopes over the trailing year, 3 for the last fiscal
      year, interest paid 2 for it: the rung reads interest expense first,
      3 / 50 = 0.06 -- not 3 / 100 over the trailing debt, and not interest paid;
    - no interest expense for that year, interest paid 2: 2 / 50 = 0.04;
    - interest expense for the year alone and its year's debt not on record:
      0.04 + 0.01 = 0.05, labelled as on record for the last fiscal year;
    - interest expense in two scopes and no interest paid anywhere: 0.05, and the
      label says interest expense is on record in two scopes and interest paid is
      not, never "neither";
    - neither on record: 0.05, and the label says "neither"."""
    scopes = {"missing": "interest_expense over the trailing four quarters: prior fiscal year "
                         "under us-gaap:A; this year to date under us-gaap:B; these are "
                         "different scopes of interest_expense, and none is on record in every "
                         "span, so the sum would be of two concepts"}
    partial = {"missing": "interest_expense over the trailing four quarters needs the this year "
                          "to date: no row"}
    absent = {"missing": "no row for interest_paid in any period"}
    trailing_debt, rate = {"value": 100.0}, {"value": 0.04}
    period = "2025-01-01..2025-12-31"

    def last_year(expense: dict, paid: dict, start: dict | None = None,
                  to_date: dict | None = None) -> dict:
        silent = {"2026-01-01..2026-06-30": {"missing": "no row"},
                  "2025-01-01..2025-06-30": {"missing": "no row"}}
        return {"period": period, "debt_dates": ["2024-12-31", "2025-12-31"],
                "years_to_date": {"interest_expense": to_date or silent, "interest_paid": silent},
                "interest_expense": expense, "interest_paid": paid,
                "debt_at_the_end": {"value": 60.0}, "debt_at_the_start": start or {"value": 40.0}}

    def ladder(expense: dict, paid: dict, year: dict | None) -> dict:
        return calculator.cost_of_debt_fallback(
            {"interest_expense": expense, "interest_paid": paid}, trailing_debt, trailing_debt,
            rate, f"interest_expense: {expense['missing']}", year)

    no_trailing_paid = {"missing": "interest_paid over the trailing four quarters needs the this "
                                   "year to date: no row"}
    both = ladder(scopes, no_trailing_paid, last_year({"value": 3.0, "tag": "A"},
                                                      {"value": 2.0, "tag": "InterestPaidNet"}))
    assert both["value"] == 3.0 / 50.0
    assert both["formula"] == "interest_expense_last_fiscal_year / average debt over that fiscal year"
    assert both["periods"] == {"numerator": period, "denominator": ["2024-12-31", "2025-12-31"]}
    assert both["fallback"].startswith(f"interest expense over the last fiscal year ({period})")
    assert "interest expense is on record but its spans fall in two scopes" in both["fallback"]

    paid_only = ladder(scopes, no_trailing_paid, last_year({"missing": "no row"},
                                                           {"value": 2.0, "tag": "InterestPaidNet"}))
    assert paid_only["value"] == 2.0 / 50.0
    assert paid_only["formula"] == "interest_paid_last_fiscal_year / average debt over that fiscal year"
    assert paid_only["fallback"].startswith(
        f"interest paid in cash over the last fiscal year ({period})")

    no_debt = ladder(partial, absent, last_year({"value": 3.0, "tag": "A"}, {"missing": "no row"},
                                                start={"missing": "no debt at the start"}))
    assert no_debt["value"] == pytest.approx(0.05)
    assert (f"interest expense is on record for the last fiscal year ({period}) and not for "
            f"every span of the trailing four quarters") in no_debt["fallback"]
    assert "that year's average debt is missing/zero" in no_debt["fallback"]
    assert "no debt at the start" in no_debt["fallback"]
    assert "neither interest expense nor interest paid" not in no_debt["fallback"]

    no_paid = ladder(scopes, absent, None)
    assert no_paid["value"] == pytest.approx(0.05)
    assert "interest expense is on record but its spans fall in two scopes" in no_paid["fallback"]
    assert "interest paid is not on record: no row for interest_paid in any period" \
        in no_paid["fallback"]
    assert "neither interest expense nor interest paid" not in no_paid["fallback"]

    neither = ladder({"missing": "no row for interest_expense in any period"}, absent, None)
    assert neither["value"] == pytest.approx(0.05)
    assert "neither interest expense nor interest paid is on record" in neither["fallback"]

    # no row in any span of the trailing four quarters, the last fiscal year read
    # and empty too: still "neither", and the only case that is
    empty_year = ladder(partial, absent, last_year({"missing": "no row"}, {"missing": "no row"}))
    assert empty_year["value"] == pytest.approx(0.05)
    assert "neither interest expense nor interest paid is on record" in empty_year["fallback"]


def test_the_last_fiscal_year_is_tried_before_the_risk_free_rate_whenever_it_is_on_record():
    """Planted: interest paid 4 over the trailing four quarters is on record, and the
    trailing debt a year earlier is not, so that rung has no average debt. The last
    fiscal year has its own interest expense, 3, and its own debt, 40 at its start
    and 60 at its end: 3 / 50 = 0.06 is read before the risk-free rate plus one
    point (0.04 + 0.01 = 0.05), and the label says why each rung above it stood
    aside. With that year's opening debt missing too, the rate plus one point is
    read, and the label still says interest expense is on record for the year."""
    period = "2025-01-01..2025-12-31"
    partial = {"missing": "interest_expense over the trailing four quarters needs the this year "
                          "to date: no row"}
    paid = {"value": 4.0, "tag": "InterestPaidNet", "period": "trailing"}

    def year(start: dict) -> dict:
        silent = {"2026-01-01..2026-06-30": {"missing": "no row"}}
        return {"period": period, "debt_dates": ["2024-12-31", "2025-12-31"],
                "years_to_date": {"interest_expense": silent, "interest_paid": silent},
                "interest_expense": {"value": 3.0, "tag": "InterestExpense"},
                "interest_paid": {"missing": "no row"},
                "debt_at_the_end": {"value": 60.0}, "debt_at_the_start": start}

    def ladder(last_year: dict) -> dict:
        return calculator.cost_of_debt_fallback(
            {"interest_expense": partial, "interest_paid": paid}, {"value": 100.0},
            {"missing": "no debt a year earlier"}, {"value": 0.04},
            f"interest_expense: {partial['missing']}", last_year)

    stepped = ladder(year({"value": 40.0}))
    assert stepped["value"] == 3.0 / 50.0
    assert stepped["periods"] == {"numerator": period, "denominator": ["2024-12-31", "2025-12-31"]}
    # the one year to date planted above states no interest expense, and the label,
    # built from the walk of those spans, says so of the figure this rung reads
    assert stepped["fallback"].startswith(
        f"interest expense over the last fiscal year ({period}) over the average of debt at "
        f"that year's start and end (2024-12-31 and 2025-12-31), which the years to date do "
        f"not state, because interest expense is on record for the last fiscal year ({period}) "
        f"and not for every span of the trailing four quarters: ")
    assert "interest paid is on record but average debt is missing/zero: " in stepped["fallback"]
    assert "no debt a year earlier" in stepped["fallback"]
    assert "risk-free rate" not in stepped["fallback"]

    no_rung = ladder(year({"missing": "no debt at the start"}))
    assert no_rung["value"] == pytest.approx(0.05)
    assert (f"interest expense is on record for the last fiscal year ({period}) and not for "
            f"every span of the trailing four quarters") in no_rung["fallback"]
    assert "interest paid is on record but average debt is missing/zero" in no_rung["fallback"]
    assert "that year's average debt is missing/zero" in no_rung["fallback"]
    assert "no debt at the start" in no_rung["fallback"]


def test_an_interest_expense_stated_for_the_years_to_date_alone_is_never_called_not_on_record():
    """Planted in Johnson Controls' shape, with no interest paid anywhere: interest
    expense for both years to date and none for the last fiscal year. Nothing can
    be divided, so the risk-free rate plus one point is read, 0.04 + 0.01 = 0.05;
    the label names the spans that state interest expense and the one that does
    not, and neither "not on record" nor "neither" is said of it."""
    period = "2025-01-01..2025-12-31"
    partial = {"missing": "interest_expense over the trailing four quarters needs the prior "
                          "fiscal year: no row"}
    year = {"period": period, "debt_dates": ["2024-12-31", "2025-12-31"],
            "years_to_date": {
                "interest_expense": {
                    "2026-01-01..2026-06-30": {"value": 2.0, "tag": "InterestExpense"},
                    "2025-01-01..2025-06-30": {"value": 1.0, "tag": "InterestExpense"}},
                "interest_paid": {"2026-01-01..2026-06-30": {"missing": "no row"},
                                  "2025-01-01..2025-06-30": {"missing": "no row"}}},
            "interest_expense": {"missing": "no row"}, "interest_paid": {"missing": "no row"},
            "debt_at_the_end": {"value": 60.0}, "debt_at_the_start": {"value": 40.0}}
    out = calculator.cost_of_debt_fallback(
        {"interest_expense": partial, "interest_paid": {"missing": "no row for interest_paid"}},
        {"value": 100.0}, {"value": 100.0}, {"value": 0.04},
        f"interest_expense: {partial['missing']}", year)
    assert out["value"] == pytest.approx(0.05)
    assert (f"interest expense is on record for the years to date (2026-01-01..2026-06-30 and "
            f"2025-01-01..2025-06-30) and not for the last fiscal year ({period}): ") \
        in out["fallback"]
    assert "interest paid is not on record: no row for interest_paid" in out["fallback"]
    assert "which is not on record" not in out["fallback"]
    assert "neither interest expense nor interest paid" not in out["fallback"]


def test_the_rung_is_tried_when_trailing_interest_expense_has_no_average_debt():
    """Planted, the other half of the rung's precondition: interest expense 4 over the
    trailing four quarters is on record and the trailing debt a year earlier is
    not. The last fiscal year's own interest expense, 3, over its own debt, 40 and
    60, is read: 3 / 50 = 0.06, never the risk-free rate plus one point (0.05).
    The trailing sum is on record, so the label says nothing of the years to date."""
    period = "2025-01-01..2025-12-31"
    stated = {"2026-01-01..2026-06-30": {"value": 2.0, "tag": "InterestExpense"},
              "2025-01-01..2025-06-30": {"value": 1.0, "tag": "InterestExpense"}}
    silent = {period: {"missing": "no row"} for period in stated}
    year = {"period": period, "debt_dates": ["2024-12-31", "2025-12-31"],
            "years_to_date": {"interest_expense": stated, "interest_paid": silent},
            "interest_expense": {"value": 3.0, "tag": "InterestExpense"},
            "interest_paid": {"missing": "no row"},
            "debt_at_the_end": {"value": 60.0}, "debt_at_the_start": {"value": 40.0}}
    out = calculator.cost_of_debt_fallback(
        {"interest_expense": {"value": 4.0, "tag": "InterestExpense"},
         "interest_paid": {"missing": "no row"}},
        {"value": 100.0}, {"missing": "no debt a year earlier"}, {"value": 0.04},
        "average_debt: no debt a year earlier", year)
    assert out["value"] == 3.0 / 50.0
    assert out["fallback"] == (
        f"interest expense over the last fiscal year ({period}) over the average of debt at "
        f"that year's start and end (2024-12-31 and 2025-12-31), because interest expense is on "
        f"record but average debt is missing/zero: average_debt: no debt a year earlier")
    assert out["standing"]["interest_expense"]["trailing"] == "on_record"


def test_the_rungs_label_says_which_years_to_date_state_its_figure_and_which_do_not():
    """Planted: the last fiscal year's interest expense is 3 over that year's debt, 40
    and 60, so the rung reads 3 / 50 = 0.06 each time; what its label says of the
    years to date follows the rows planted for them. With the earlier year to
    date stating 1 and the later one silent, it names each. With both stating
    it and the trailing sum still not taken, it says they state it too, and
    never that interest expense is on record for the year alone."""
    period = "2025-01-01..2025-12-31"
    later, earlier = "2026-01-01..2026-06-30", "2025-01-01..2025-06-30"
    silent = {"missing": "no row"}

    def ladder(this_year: dict, missing: str) -> dict:
        year = {"period": period, "debt_dates": ["2024-12-31", "2025-12-31"],
                "years_to_date": {
                    "interest_expense": {later: this_year,
                                         earlier: {"value": 1.0, "tag": "InterestExpense"}},
                    "interest_paid": {later: silent, earlier: silent}},
                "interest_expense": {"value": 3.0, "tag": "InterestExpense"},
                "interest_paid": silent,
                "debt_at_the_end": {"value": 60.0}, "debt_at_the_start": {"value": 40.0}}
        return calculator.cost_of_debt_fallback(
            {"interest_expense": {"missing": missing}, "interest_paid": silent},
            {"value": 100.0}, {"value": 100.0}, {"value": 0.04},
            f"interest_expense: {missing}", year)

    opening = (f"interest expense over the last fiscal year ({period}) over the average of "
               f"debt at that year's start and end (2024-12-31 and 2025-12-31), which the "
               f"years to date state ")
    needs = "interest_expense over the trailing four quarters needs the this year to date: no row"
    mixed = ladder(silent, needs)
    assert mixed["value"] == 3.0 / 50.0
    assert mixed["fallback"] == (
        f"{opening}for {earlier} and not for {later}, because interest expense is on record "
        f"for the last fiscal year ({period}) and not for every span of the trailing four "
        f"quarters: interest_expense: {needs}")
    assert mixed["standing"]["interest_expense"]["trailing"] == "fiscal_year_only"

    unsummed = "the trailing four quarters are not summed for a reason of their own"
    every = ladder({"value": 2.0, "tag": "InterestExpense"}, unsummed)
    assert every["value"] == 3.0 / 50.0
    assert every["fallback"] == (
        f"{opening}too, because interest expense is on record for every span of the trailing "
        f"four quarters but no trailing sum is taken: interest_expense: {unsummed}")
    assert "do not state" not in every["fallback"] and "not for every span" not in every["fallback"]
    assert every["standing"]["interest_expense"]["trailing"] == "no_sum"


def test_a_filing_with_no_last_fiscal_year_to_walk_is_labelled_without_one():
    """Planted in an annual report's shape: the trailing four quarters are the fiscal
    year itself, so there is no last fiscal year and no year to date to walk. A
    missing interest expense and interest paid are then absent, the rate is
    0.04 + 0.01 = 0.05, and the label says "neither"; with interest paid refused
    it says that instead."""
    annual = {"missing": "the trailing four quarters are the fiscal year itself"}
    none = {"missing": "no row for interest_expense in 2025-01-01..2025-12-31"}

    def ladder(paid: dict) -> dict:
        return calculator.cost_of_debt_fallback(
            {"interest_expense": none, "interest_paid": paid}, {"value": 100.0}, {"value": 100.0},
            {"value": 0.04}, f"interest_expense: {none['missing']}", annual)

    out = ladder({"missing": "no row for interest_paid in 2025-01-01..2025-12-31"})
    assert out["value"] == pytest.approx(0.05)
    assert "neither interest expense nor interest paid is on record" in out["fallback"]
    assert out["standing"] == {"interest_expense": {"trailing": "absent", "spans": []},
                               "interest_paid": {"trailing": "absent", "spans": []}}
    refused = ladder({"missing": f"InterestPaidNet is reported as [1.0, 2.0] -- "
                                 f"{calculator.trends.TWO_VALUES}"})
    assert "interest paid is on record but refused" in refused["fallback"]
    assert "neither interest expense nor interest paid" not in refused["fallback"]


def test_a_year_to_date_row_is_never_called_not_on_record_where_no_fiscal_year_stands_before():
    """Planted: a quarterly report whose record holds no fiscal year before its year
    to date. Interest expense 2 is stated for that year to date. There is no
    trailing sum and no last fiscal year, so the rate is 0.04 + 0.01 = 0.05; the
    label names the span that states interest expense, and says "neither" only
    once that row is taken away."""
    span = "2026-01-01..2026-06-30"
    partial = {"missing": "interest_expense over the trailing four quarters needs the prior "
                          "fiscal year: no row"}
    nothing = {"missing": "no row for interest_paid in any period"}

    def ladder(to_date: dict) -> dict:
        year = {"missing": "no complete fiscal year before the year to date is on record",
                "years_to_date": {"interest_expense": {span: to_date},
                                  "interest_paid": {span: {"missing": "no row"}}}}
        return calculator.cost_of_debt_fallback(
            {"interest_expense": partial, "interest_paid": nothing}, {"value": 100.0},
            {"value": 100.0}, {"value": 0.04}, f"interest_expense: {partial['missing']}", year)

    out = ladder({"value": 2.0, "tag": "InterestExpense"})
    assert out["value"] == pytest.approx(0.05)
    assert (f"interest expense is on record for the years to date ({span}) and no complete "
            f"fiscal year before them is on record: ") in out["fallback"]
    assert "neither interest expense nor interest paid" not in out["fallback"]
    assert "which is not on record" not in out["fallback"]
    assert out["standing"]["interest_expense"] == {
        "trailing": "years_to_date_only",
        "spans": [{"span": "year_to_date", "period": span, "on_record": True,
                   "tag": "InterestExpense", "scope": "InterestExpense"}]}
    empty = ladder({"missing": "no row"})
    assert empty["value"] == pytest.approx(0.05)
    assert "neither interest expense nor interest paid is on record" in empty["fallback"]


def test_interest_paid_stated_for_the_years_to_date_alone_is_not_called_neither():
    """Planted: no interest expense in any span; interest paid for both years to date
    and not for the last fiscal year. No trailing sum and no rung can be read, so
    the rate is 0.04 + 0.01 = 0.05, and the label says where interest paid is on
    record -- not that neither figure is."""
    period = "2025-01-01..2025-12-31"
    spans = ("2026-01-01..2026-06-30", "2025-01-01..2025-06-30")
    year = {"period": period, "debt_dates": ["2024-12-31", "2025-12-31"],
            "years_to_date": {
                "interest_expense": {span: {"missing": "no row"} for span in spans},
                "interest_paid": {span: {"value": 2.0, "tag": "InterestPaidNet"} for span in spans}},
            "interest_expense": {"missing": "no row"}, "interest_paid": {"missing": "no row"},
            "debt_at_the_end": {"value": 60.0}, "debt_at_the_start": {"value": 40.0}}
    none = {"missing": "no row for interest_expense in any period"}
    partial = {"missing": "interest_paid over the trailing four quarters needs the prior fiscal "
                          "year: no row"}
    out = calculator.cost_of_debt_fallback(
        {"interest_expense": none, "interest_paid": partial}, {"value": 100.0}, {"value": 100.0},
        {"value": 0.04}, f"interest_expense: {none['missing']}", year)
    assert out["value"] == pytest.approx(0.05)
    assert (f"interest paid is on record for the years to date ({spans[0]} and {spans[1]}) and "
            f"not for the last fiscal year ({period}): ") in out["fallback"]
    assert "neither interest expense nor interest paid" not in out["fallback"]
    assert out["standing"]["interest_paid"]["trailing"] == "years_to_date_only"
    assert out["standing"]["interest_expense"]["trailing"] == "absent"


INTEREST_TAGS = ("InterestExpense", "InterestExpenseNonoperating", "InterestExpenseDebt",
                 "InterestAndDebtExpense")
PAID_TAGS = ("InterestPaidNet", "InterestPaid")


def rows_on_record(run: str, cutoff: str, tags: tuple, periods: list) -> list:
    """Every (tag, period) the record holds for the tags and spans named, in the
    order of the tags: companyfacts through the independent reader, and the run's
    own bundle, read here."""
    ticker = run.split("/")[0]
    facts = json.loads((RUNS / run / "input_numbers.json").read_text(encoding="utf-8"))["facts"]
    in_bundle = {(fact["tag"], f"{context['start']}..{context['end']}") for fact in facts
                 for context in [fact.get("context") or {}]
                 if fact["tag"] in tags and context.get("start")
                 and not context.get("segment") and not fact.get("nil")
                 and fact.get("filing_date", "9999") <= cutoff}
    return [(tag, period) for tag in tags for period in periods
            if (tag, period) in in_bundle or source.reported(ticker, tag, period, cutoff)]


def interest_rows_on_record(run: str, cutoff: str, periods: list) -> list:
    return rows_on_record(run, cutoff, INTEREST_TAGS, periods)


def test_johnson_controls_label_names_the_spans_that_state_interest_expense():
    """Johnson Controls' 10-Q filed 2026-07-29 tags InterestExpense 160 for the nine
    months to 2026-06-30 and 178 for the nine months to 2025-06-30 (the run's own
    bundle; the store's companyfacts predates the filing), and no interest tag
    carries fiscal 2025. So the cost of debt reads fiscal 2025's interest paid, and
    its label says interest expense is on record for the years to date and not
    for the last fiscal year -- not that it "is not on record"."""
    cut, run = "2026-07-29", "JCI/0000833444-26-000087"
    year, to_date, before = "2024-10-01..2025-09-30", "2025-10-01..2026-06-30", "2024-10-01..2025-06-30"
    bundle = RUNS / run
    assert bundle_fact(bundle, "InterestExpense", "2025-10-01", "2026-06-30", cut) == 160 * MILLION
    assert bundle_fact(bundle, "InterestExpense", "2024-10-01", "2025-06-30", cut) == 178 * MILLION
    assert interest_rows_on_record(run, cut, [year]) == []
    assert interest_rows_on_record(run, cut, [to_date, before]) == [
        ("InterestExpense", to_date), ("InterestExpense", before)]
    out = calculator.calculate(ticker="JCI", cutoff=cut, period_end="2026-06-30", form="10-Q",
                               bundle=bundle)
    cost = out["cost_of_capital"]["pre_tax_cost_of_debt"]
    assert cost["value"] == pytest.approx(321 / 9_686.5, rel=1e-12)
    assert cost["fallback"].startswith(
        f"interest paid in cash over the last fiscal year ({year}) over the average of debt at "
        f"that year's start and end (2024-09-30 and 2025-09-30), which the years to date do not "
        f"state, because interest expense is on record for the years to date ({to_date} and "
        f"{before}) and not for the last fiscal year ({year}): ")
    assert "which is not on record" not in cost["fallback"]


def test_esco_label_keeps_what_is_said_of_interest_expense_apart_from_interest_paid(
        committed_calculators):
    """ESCO's 10-Q for the nine months to 2026-06-30 states no interest expense for
    them; its 10-K states the year to 2025-09-30, and interest paid is on record
    for every span, read here. The cost of debt is interest paid over average debt,
    as published, and its label says how interest expense stands as a sentence of
    its own -- not "in place of interest expense is on record ...", which reads as
    said of interest paid."""
    run = "ESE/0001104659-26-093266"
    cutoff, payload = committed_calculators[run]
    year, to_date, before = ("2024-10-01..2025-09-30", "2025-10-01..2026-06-30",
                             "2024-10-01..2025-06-30")
    assert rows_on_record(run, cutoff, INTEREST_TAGS, [year]) == [("InterestExpense", year)]
    assert rows_on_record(run, cutoff, INTEREST_TAGS, [to_date]) == []
    assert {period for _, period in rows_on_record(run, cutoff, PAID_TAGS, [year, to_date, before])} \
        == {year, to_date, before}
    cell = payload["cost_of_capital"]["pre_tax_cost_of_debt"]
    assert cell["formula"] == "interest_paid / average debt"
    assert cell["fallback"].startswith(
        f"interest paid in cash in place of interest expense: interest expense is on record for "
        f"the last fiscal year ({year}) and not for every span of the trailing four quarters: ")
    published = json.loads((RUNS / run / "calculator.json").read_text(encoding="utf-8"))
    assert cell["value"] == published["cost_of_capital"]["pre_tax_cost_of_debt"]["value"]


def test_every_clause_of_every_committed_runs_label_is_true_of_the_record(committed_calculators):
    """Every committed run, recomputed. The cost of debt's label is built from one
    walk of the record, carried in the cell as `standing`; here each fact of that
    walk, and then each clause of the label, is checked against companyfacts and
    the run's bundle, read by this test and never by the calculator:

    - a span is on record for a figure exactly where a row of one of its tags is,
      and is read under the first such tag in the chain's order;
    - how each figure stands follows from those rows alone: absent where no span
      carries one, the last fiscal year only, the years to date only, or every span;
    - "the years to date do not state" the rung's figure only where no year to date
      carries a row of it; they "state it too", in two scopes, only where every one
      does and the debt-only tag and a whole-line tag are both among the spans;
    - interest expense "is not on record", and "neither" figure is, only where no
      span carries a row; "on record for the last fiscal year and not for every
      span" and "on record for the years to date and not for the last fiscal year"
      each exactly where the rows say so;
    - where the cell is interest expense over average debt and carries no label,
      interest expense has a row in every span."""
    assert len(committed_calculators) == len(list(RUNS.glob("*/*/input_manifest.json"))) >= 32
    tags = {"interest_expense": INTEREST_TAGS, "interest_paid": PAID_TAGS}
    said = {}
    for run, (cutoff, payload) in committed_calculators.items():
        cell = payload["cost_of_capital"]["pre_tax_cost_of_debt"]
        parts = payload["terms"]["trailing_four_quarters"]["revenue"]["parts"]
        if not isinstance(parts, dict):
            # an annual report: the trailing four quarters are the year itself, and
            # no committed annual run's cost of debt stands on a fallback
            assert "fallback" not in cell and "standing" not in cell, run
            continue
        year = parts["prior_fiscal_year"]["period"]
        to_date = [parts["this_year_to_date"]["period"], parts["prior_year_to_date"]["period"]]

        def stated(figure: str, periods: list) -> list:
            return rows_on_record(run, cutoff, tags[figure], periods)

        def stands(figure: str) -> str:
            in_year = bool(stated(figure, [year]))
            in_to_date = {period for _, period in stated(figure, to_date)}
            return ("every span" if in_year and in_to_date == set(to_date) else
                    "fiscal_year_only" if in_year else
                    "years_to_date_only" if in_to_date else "absent")

        label = cell.get("fallback")
        if not label:
            assert "standing" not in cell, run
            if cell.get("formula") == "interest_expense / average debt":
                assert stands("interest_expense") == "every span", run
                said.setdefault("no label", set()).add(run.split("/")[0])
            continue
        for figure, fact in cell["standing"].items():
            assert [row["period"] for row in fact["spans"]] == [year] + to_date, run
            for row in fact["spans"]:
                found = stated(figure, [row["period"]])
                assert row["on_record"] is bool(found), (run, figure, row)
                assert row["tag"] == (found[0][0] if found else None), (run, figure, row)
            if stands(figure) == "every span":
                assert fact["trailing"] in ("on_record", "refused", "two_scopes", "no_sum"), \
                    (run, figure)
            else:
                assert fact["trailing"] == stands(figure), (run, figure)

        expense, paid = stands("interest_expense"), stands("interest_paid")
        rung = ("interest_expense" if label.startswith("interest expense over the last fiscal year")
                else "interest_paid" if label.startswith("interest paid in cash over the last "
                                                         "fiscal year") else None)
        clauses = {
            "do not state": "which the years to date do not state" in label,
            "two scopes": "which the years to date state too" in label,
            "not on record": "interest expense, which is not on record" in label
                             or "neither interest expense" in label,
            "neither": "neither interest expense nor interest paid is on record" in label,
            "fiscal year only": "interest expense is on record for the last fiscal year" in label,
            "years to date only": "interest expense is on record for the years to date" in label}
        for clause, present in clauses.items():
            if present:
                said.setdefault(clause, set()).add(run.split("/")[0])
        if rung:
            # the rung reads the year's figure, so the year carries a row of it; what
            # the label says of the years to date is what their rows say
            assert stated(rung, [year]), run
            assert clauses["do not state"] is (stated(rung, to_date) == []), (run, label[:200])
        else:
            assert not clauses["do not state"], (run, label[:200])
        if clauses["two scopes"]:
            assert stands(rung) == "every span", run
            first = {period: stated(rung, [period])[0][0] for period in [year] + to_date}
            assert {"InterestExpenseDebt"} < set(first.values()), (run, first)
            for period in to_date:
                assert f"{period} under us-gaap:{first[period]}" in label, (run, period)
        assert clauses["not on record"] is (expense == "absent"), (run, label[:200])
        assert clauses["neither"] is (expense == "absent" and paid == "absent"), (run, label[:200])
        assert clauses["fiscal year only"] is (expense == "fiscal_year_only"), (run, label[:200])
        assert clauses["years to date only"] is (expense == "years_to_date_only"), (run, label[:200])
        if clauses["years to date only"]:
            named = label.split("is on record for the years to date (")[1].split(")")[0]
            for period in to_date:
                assert (period in named) is bool(stated("interest_expense", [period])), (run, period)
    # every clause is exercised by a committed run: the three labels worked by hand
    # in the tests above, and Apple's, whose record states neither figure
    assert "DELL" in said["two scopes"] and {"CARR", "JCI"} <= said["do not state"]
    assert "CARR" in said["fiscal year only"] and "JCI" in said["years to date only"]
    assert "AAPL" in said["not on record"] and "AAPL" in said["neither"]
    assert said["no label"]


# --- the two years to date are read like for like within a scope ------------------------------

def test_the_two_years_to_date_are_read_under_one_tag_within_a_scope():
    """Planted: fiscal 2024 under DepreciationDepletionAndAmortization (100); the six
    months of 2025 under it (60) and under DepreciationAndAmortization (55); the six
    months of 2024 under DepreciationAndAmortization alone (40). One scope, but the
    two years to date would be differenced across a rename: both are read under the
    tag that carries both, so the year is 100 + 55 - 40 = 115, not 100 + 60 - 40 = 120,
    and the tags still differ across the sum."""
    renamed = "DepreciationAndAmortization"
    lines = {"year": {DEPRECIATION: 100.0}, "to_date": {DEPRECIATION: 60.0, renamed: 55.0},
             "before": {renamed: 40.0}}
    record, periods = depreciation_planted(lines)
    found = calculator.trailing(record, "depreciation_and_amortization", periods)
    assert found["value"] == 115.0
    assert found["parts"]["this_year_to_date"]["tag"] == renamed
    assert found["parts"]["prior_year_to_date"]["tag"] == renamed
    assert found["tags_differ"] == sorted([DEPRECIATION, renamed])


def test_like_for_like_holds_when_the_spans_first_fell_in_two_scopes():
    """Planted: interest expense 100 under InterestExpense for fiscal 2024; the six
    months of 2025 under InterestExpenseNonoperating (60) and InterestAndDebtExpense
    (55); the six months of 2024 under InterestExpenseDebt (8), a scope of its own
    and the first tag found there, and InterestAndDebtExpense (40). The spans first
    fall in two scopes; the interest-expense group is on record in every span and
    is read, and within it the two years to date are read under the one tag that
    carries both: 100 + 55 - 40 = 115, not 100 + 60 - 40 = 120 across a rename."""
    lines = {"year": {"InterestExpense": 100.0},
             "to_date": {"InterestExpenseNonoperating": 60.0, "InterestAndDebtExpense": 55.0},
             "before": {"InterestExpenseDebt": 8.0, "InterestAndDebtExpense": 40.0}}
    record, periods = depreciation_planted(lines)
    assert record.term("interest_expense", periods["prior_to_date"])["tag"] == "InterestExpenseDebt"
    found = calculator.trailing(record, "interest_expense", periods)
    assert found["value"] == 115.0
    assert found["parts"]["this_year_to_date"]["tag"] == "InterestAndDebtExpense"
    assert found["parts"]["prior_year_to_date"]["tag"] == "InterestAndDebtExpense"
    assert found["tags_differ"] == ["InterestAndDebtExpense", "InterestExpense"]


def test_the_scope_read_is_the_first_in_chain_order_that_every_span_carries():
    """Planted: interest on debt alone (InterestExpenseDebt, a scope of its own) in
    every span, 8, 5 and 4; the interest-expense group in every span too, under
    InterestAndDebtExpense for fiscal 2024 (100) and the six months of 2024 (40) and
    under InterestExpense for the six months of 2025 (60). Both scopes are on record
    in every span; the group comes first in the chain and is the one read:
    100 + 60 - 40 = 120, never the debt-only 8 + 5 - 4 = 9."""
    lines = {"year": {"InterestExpenseDebt": 8.0, "InterestAndDebtExpense": 100.0},
             "to_date": {"InterestExpense": 60.0, "InterestExpenseDebt": 5.0},
             "before": {"InterestExpenseDebt": 4.0, "InterestAndDebtExpense": 40.0}}
    record, periods = depreciation_planted(lines)
    assert record.term("interest_expense", periods["prior_year"])["tag"] == "InterestExpenseDebt"
    assert record.term("interest_expense", periods["current_to_date"])["tag"] == "InterestExpense"
    found = calculator.trailing(record, "interest_expense", periods)
    assert found["value"] == 120.0
    assert {name: part["tag"] for name, part in found["parts"].items()} == {
        "prior_fiscal_year": "InterestAndDebtExpense", "this_year_to_date": "InterestExpense",
        "prior_year_to_date": "InterestAndDebtExpense"}


def test_a_scope_one_filing_states_twice_is_refused_not_called_two_scopes():
    """Planted: interest expense 100 and 60 under InterestExpense for fiscal 2024 and
    the six months of 2025; for the six months of 2024, InterestExpenseDebt 4 (a
    scope of its own, the first tag found there) and InterestAndDebtExpense stated
    twice by one filing, 40 and 41. The spans first fall in two scopes, and the
    interest-expense group is on record in every span; its refusal is what the cell
    says -- two values for one period -- not that the spans are in different
    scopes, and no sum is read from the debt-only tag."""
    lines = {"year": {"InterestExpense": 100.0}, "to_date": {"InterestExpense": 60.0},
             "before": {"InterestExpenseDebt": 4.0, "InterestAndDebtExpense": 40.0}}
    record, periods = depreciation_planted(lines)
    span = periods["prior_to_date"]
    stated = record.usd["InterestAndDebtExpense"][span]
    stated.append(dict(stated[0], val=41.0))
    found = calculator.trailing(record, "interest_expense", periods)
    assert "value" not in found
    assert calculator.trends.TWO_VALUES in found["missing"]
    assert "different scopes" not in found["missing"]
    assert found["missing"].startswith(
        "interest_expense over the trailing four quarters needs the prior year to date")


# --- a series of quarters is held to one scope -----------------------------------------------------

def test_a_series_of_quarters_is_read_in_the_one_scope_some_of_it_is_on_record_in():
    """Planted in Johnson Controls' shape, quarterly: the fiscal year and the six months
    of 2025 under the continuing-operations tag alone, the six months of 2024 under
    both (total 80, continuing 30) with its first quarter under both (total 50,
    continuing 10). The newest quarters are readable in continuing operations only,
    so the series is: the quarter to June 2024 is 30 - 10 = 20 of continuing
    operations, not 80 - 50 = 30 of the total, and says so."""
    continuing, total = ("NetCashProvidedByUsedInOperatingActivitiesContinuingOperations",
                         "NetCashProvidedByUsedInOperatingActivities")
    record, periods = mixed_planted({"year": continuing, "to_date": continuing, "before": total},
                                    {"year": "Revenues", "to_date": "Revenues", "before": "Revenues"})
    row = dict(record.usd[total][("2024-01-01", "2024-06-30")][0])
    record.usd[total][("2024-01-01", "2024-06-30")] = [dict(row, val=80.0)]
    record.usd[continuing][("2024-01-01", "2024-06-30")] = [dict(row, val=30.0)]
    record.usd[total][("2024-01-01", "2024-03-31")] = [dict(row, end="2024-03-31", val=50.0)]
    record.usd[continuing][("2024-01-01", "2024-03-31")] = [dict(row, end="2024-03-31", val=10.0)]
    # the three months of 2025 under continuing operations alone, so the quarter to
    # June 2025 is 40 - 15 = 25 and readable in that scope only
    record.usd[continuing][("2025-01-01", "2025-03-31")] = [
        dict(row, start="2025-01-01", end="2025-03-31", val=15.0)]
    spans = calculator.durations(record.usd)
    alone = calculator.quarter(record, "operating_cash_flow", spans, calculator.dt.date(2024, 6, 30))
    assert alone["value"] == 30.0 and alone["parts"][0]["tag"] == total
    ends = [calculator.dt.date(2025, 6, 30), calculator.dt.date(2024, 6, 30)]
    series = calculator.quarters_in_one_scope(record, "operating_cash_flow", spans, ends)
    assert [found["value"] for found in series] == [25.0, 20.0]
    assert {found["scope"] for found in series} == {continuing}
    assert [part["tag"] for part in series[1]["parts"]] == [continuing, continuing]
    # a quarter the forced scope does not reach is missing with the reason, never read in the other
    del record.usd[continuing][("2024-01-01", "2024-03-31")]
    series = calculator.quarters_in_one_scope(record, "operating_cash_flow", spans, ends)
    assert "value" not in series[1]
    assert f"in the scope the series is read in, us-gaap:{continuing}" in series[1]["missing"]


def test_johnson_controls_oldest_smoothness_quarter_is_continuing_operations():
    """Through the independent reader: the six months to 2024-06-30 are 216 under the
    continuing-operations tag and 572 under the total; the three months to
    2024-03-31 are -437 and -449. The eight newer quarters of the series are on
    record under continuing operations alone, so the quarter to June 2024 is
    216 - (-437) = 653, not 572 - (-449) = 1,021, and the cell says which scope."""
    cut, continuing, total = ("2026-07-29",
                              "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations",
                              "NetCashProvidedByUsedInOperatingActivities")
    assert source.one_value("JCI", continuing, "2023-10-01..2024-06-30", cut) == 216 * MILLION
    assert source.one_value("JCI", continuing, "2023-10-01..2024-03-31", cut) == -437 * MILLION
    assert cfo("JCI", "2023-10-01..2024-06-30", cut) == 572 * MILLION
    assert cfo("JCI", "2023-10-01..2024-03-31", cut) == -449 * MILLION
    assert source.reported("JCI", total, "2024-10-01..2025-09-30", cut) == []
    bundle = source.FIXTURES.parent.parent / "runs" / "JCI" / "0000833444-26-000087"
    out = calculator.calculate(ticker="JCI", cutoff=cut, period_end="2026-06-30", form="10-Q",
                               bundle=bundle)
    smooth = out["earnings_versus_cash"]["smoothness"]
    assert smooth["quarters_read"][8] == "2024-06-30"
    assert smooth["operating_cash_flow"][8] == 653 * MILLION
    assert smooth["operating_cash_flow"][7] == 1_352 * MILLION
    assert smooth["operating_cash_flow_scope"].startswith(f"every quarter read under us-gaap:{continuing}")
