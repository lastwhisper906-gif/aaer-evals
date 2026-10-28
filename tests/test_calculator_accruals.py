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

import pytest

from src import calculator
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


def test_eight_quarters_are_carried(cisco):
    history = cisco[SECTION]["operating_cash_flow_quarterly"]["history"]
    assert [row["quarters_back"] for row in history] == list(range(8))


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
    """Cisco's record tags no depreciation and amortization for fiscal 2026 to date
    (the 10-Q prints "Depreciation, amortization, and other", which no tag in the
    chain carries), so Sloan's measure has nothing to subtract: null, never zero."""
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
