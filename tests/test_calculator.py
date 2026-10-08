"""The calculator, judged against numbers that did not come from it.

Three kinds of expected value, each named where it is used:

- **NVIDIA's own reconciliation.** The press release of 2026-08-26 (8-K
  exhibit 99.1, `tests/fixtures/NVDA/8-K/q2fy27pr.htm`) prints a free-cash-flow
  table: net cash provided by operating activities, purchases related to
  property and equipment and intangible assets, principal payments on property
  and equipment and intangible assets, and free cash flow, for the quarter and
  the six months of fiscal 2027 and 2026. The 10-K filed 2026-02-25
  (`tests/fixtures/NVDA/10-K/nvda-20260125.htm`) prints the fiscal 2026 year.
  Those printed figures, in millions, are the expected values.
- **The Gordon growth identity.** A firm whose free cash flow grows at one rate
  g for ever is worth its next year's cash flow over (WACC - g). A ten-year
  forecast at constant g with a terminal value grown at the same g must land
  on exactly that, whatever the ten years look like; the arithmetic is written
  out beside the test.
- **A year-by-year table worked by hand** for a forecast whose growth fades,
  each line written out as the multiplication it is.

The market-wide inputs are read against their publishers: the 10-year Treasury
yield of 2026-08-26 is FRED's DGS10 row for that day, and the implied equity
risk premium is the figure Damodaran's home page prints for the month.
"""

from __future__ import annotations

import copy
import datetime as dt
import gzip
import json
import math

import pytest

from src import calculator, cutoff_guard

MILLION = 1_000_000

NVDA_CUTOFF = "2026-08-26"
NVDA_PERIOD_END = "2026-07-26"


@pytest.fixture(scope="module")
def nvda():
    return calculator.calculate(ticker="NVDA", cutoff=NVDA_CUTOFF,
                                period_end=NVDA_PERIOD_END, form="10-Q",
                                accession="0001045810-26-000075")


@pytest.fixture(scope="module")
def nvda_record():
    from src import trends
    return calculator.Record(trends.read_record("NVDA", NVDA_CUTOFF))


# --- NVIDIA's printed free-cash-flow table ------------------------------------------

def test_six_months_to_date_match_the_press_release(nvda_record):
    """q2fy27pr.htm, six months ended July 26, 2026: operating cash flow 74,421 and
    purchases related to property and equipment and intangible assets (4,434)."""
    span = ("2026-01-26", "2026-07-26")
    assert nvda_record.term("operating_cash_flow", span)["value"] == 74_421 * MILLION
    capex = nvda_record.term("capital_expenditure", span)
    assert capex["value"] == 4_434 * MILLION
    assert capex["tag"] == "PaymentsToAcquireProductiveAssets"


def test_six_months_a_year_earlier_match_the_press_release(nvda_record):
    """q2fy27pr.htm, six months ended July 27, 2025: 42,779 and (3,122)."""
    span = ("2025-01-27", "2025-07-27")
    assert nvda_record.term("operating_cash_flow", span)["value"] == 42_779 * MILLION
    assert nvda_record.term("capital_expenditure", span)["value"] == 3_122 * MILLION


def test_trailing_four_quarters_are_worked_from_the_printed_figures(nvda):
    """Fiscal 2026 from the 10-K's cash flow statement: operating activities 102,718,
    purchases related to property and equipment and intangible assets (6,042).

    Trailing four quarters = fiscal 2026 + six months of 2027 - six months of 2026:
      operating cash flow  102,718 + 74,421 - 42,779 = 134,360
      capital expenditure    6,042 +  4,434 -  3,122 =   7,354
      free cash flow       134,360 -  7,354          = 127,006
    """
    ttm = nvda["terms"]["trailing_four_quarters"]
    assert ttm["operating_cash_flow"]["value"] == 134_360 * MILLION
    assert ttm["capital_expenditure"]["value"] == 7_354 * MILLION
    simple = nvda["free_cash_flow"]["free_cash_flow_simple"]
    assert simple["value"] == 127_006 * MILLION


def test_simple_free_cash_flow_reconciles_to_the_companys_own(nvda_record):
    """NVIDIA's free cash flow also subtracts principal payments on property and
    equipment and intangible assets, (92) for the six months. So the company's
    69,895 is this file's simple measure less 92:
      74,421 - 4,434 = 69,987;  69,987 - 92 = 69,895, the printed figure.
    The simple measure is CFO less capital expenditure and nothing else, as the
    owner defined it; the 92 is the whole of the difference.
    """
    span = ("2026-01-26", "2026-07-26")
    simple = (nvda_record.term("operating_cash_flow", span)["value"]
              - nvda_record.term("capital_expenditure", span)["value"])
    assert simple == 69_987 * MILLION
    assert simple - 92 * MILLION == 69_895 * MILLION


def test_every_trailing_input_names_its_rows(nvda):
    parts = nvda["terms"]["trailing_four_quarters"]["operating_cash_flow"]["parts"]
    assert set(parts) == {"prior_fiscal_year", "this_year_to_date", "prior_year_to_date"}
    assert parts["prior_fiscal_year"]["id"] == (
        "0001045810-26-000021:facts:NetCashProvidedByUsedInOperatingActivities:"
        "2025-01-27..2026-01-25")


# --- signs are read from the tag -------------------------------------------------------

def test_every_cash_flow_tag_carries_a_direction():
    for term in calculator.CASH_FLOW_TERMS:
        for tag in calculator.TERMS[term][1]:
            assert tag in calculator.DIRECTION, (term, tag)
    for family in calculator.CASH_FLOW_FAMILIES:
        for tag in calculator.family_tags(family):
            assert tag in calculator.DIRECTION, (family, tag)


def test_capital_expenditure_and_repurchases_are_outflows_by_their_tags():
    """us-gaap defines Payments... as cash paid, stated positive."""
    for tag in ("PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets",
                "PaymentsForRepurchaseOfCommonStock", "PaymentsOfDividends"):
        assert calculator.direction_of(tag) == "outflow"
        assert calculator.CASH_EFFECT["outflow"] == -1.0
    assert calculator.direction_of("ProceedsFromIssuanceOfLongTermDebt") == "inflow"
    assert calculator.direction_of("ProceedsFromRepaymentsOfCommercialPaper") == "signed"


def test_a_tag_with_no_direction_is_refused():
    with pytest.raises(calculator.CalculatorInputError):
        calculator.direction_of("PaymentsForSomethingNobodyListed")


def test_the_capital_expenditure_row_carries_its_tags_direction(nvda_record):
    capex = nvda_record.term("capital_expenditure", ("2026-01-26", "2026-07-26"))
    assert capex["direction"] == "outflow"
    assert calculator.cash_effect(capex) == -4_434 * MILLION


def test_a_negative_payment_is_read_as_cash_back_and_flagged():
    """Generac tags some acquisition periods negative under a Payments tag. The
    taxonomy's sign is kept: cash came back. It is flagged, not flipped."""
    document = {"ticker": "TEST", "facts": {"us-gaap": {
        "PaymentsToAcquireBusinessesNetOfCashAcquired": {"units": {"USD": [
            {"start": "2025-01-01", "end": "2025-12-31", "val": -5_000_000,
             "accn": "0000000000-26-000001", "fy": 2025, "fp": "FY", "form": "10-K",
             "filed": "2026-02-20"}]}}}}}
    record = calculator.Record(document)
    cell = record.family("acquisitions", ("2025-01-01", "2025-12-31"))
    assert cell["value"] == -5_000_000
    assert "flag" in cell["lines"][0]
    assert calculator.family_cash_effect(cell) == 5_000_000


# --- the market-wide inputs ---------------------------------------------------------------

def test_risk_free_rate_is_freds_row_for_the_day():
    """DGS10, 2026-08-26: 4.66 per cent (FRED's CSV row for that date)."""
    rate = calculator.risk_free_rate(dt.date(2026, 8, 26))
    assert rate["value"] == pytest.approx(0.0466)
    assert rate["date"] == "2026-08-26"


def test_a_weekend_cutoff_reads_the_last_observation_before_it():
    """2026-08-29 is a Saturday; the last row on or before it is Friday 2026-08-28, 4.73."""
    rate = calculator.risk_free_rate(dt.date(2026, 8, 29))
    assert rate["date"] == "2026-08-28"
    assert rate["value"] == pytest.approx(0.0473)


def test_equity_risk_premium_is_damodarans_figure_for_the_month():
    """Damodaran's home page, read 2026-09-28: 'Implied ERP on September 1, 2026 =
    4.14% (Trailing 12 month, with adjusted payout)', and for the previous month,
    'Implied ERP in previous month = 4.28% (Trailing 12 month, with adjusted payout)'."""
    august = calculator.equity_risk_premium(dt.date(2026, 8, 26))
    assert august["month_start"] == "2026-08-01"
    assert august["value"] == pytest.approx(0.0428)
    september = calculator.equity_risk_premium(dt.date(2026, 9, 3))
    assert september["month_start"] == "2026-09-01"
    assert september["value"] == pytest.approx(0.0414)


def test_a_cutoff_on_the_first_reads_the_month_before():
    """The rule is strictly before: on 2026-09-01 the September figure may not be posted."""
    premium = calculator.equity_risk_premium(dt.date(2026, 9, 1))
    assert premium["month_start"] == "2026-08-01"


def test_an_altered_input_file_is_refused(tmp_path, monkeypatch):
    folder = tmp_path / "inputs"
    folder.mkdir()
    for name in ("manifest.json", "dgs10_2024-01-01_2026-09-25.csv",
                 "damodaran_implied_erp_by_month.xlsx"):
        (folder / name).write_bytes((calculator.COST_OF_CAPITAL / name).read_bytes())
    path = folder / "dgs10_2024-01-01_2026-09-25.csv"
    path.write_text(path.read_text().replace("2026-08-26,4.66", "2026-08-26,1.00"))
    monkeypatch.setattr(calculator, "COST_OF_CAPITAL", folder)
    with pytest.raises(calculator.CalculatorInputError):
        calculator.risk_free_rate(dt.date(2026, 8, 26))


# --- the tax rate ---------------------------------------------------------------------------

def _tax(tax, pretax):
    cell = lambda v: {"value": v, "id": "x", "tag": "t", "period": "p"}
    return calculator.tax_rate({"trailing_four_quarters": {"income_tax_expense": cell(tax),
                                                           "pretax_income": cell(pretax)}})


def test_the_effective_rate_is_held_between_zero_and_statutory():
    assert _tax(15, 100)["value"] == pytest.approx(0.15)
    assert _tax(40, 100)["value"] == pytest.approx(0.21)
    assert _tax(-5, 100)["value"] == 0.0
    assert _tax(5, -100)["value"] == 0.0


# --- the DCF ------------------------------------------------------------------------------

GORDON = {"revenue_growth_year_one": 0.03, "terminal_growth": 0.03,
          "operating_margin_year_one": 0.20, "operating_margin_year_ten": 0.20,
          "reinvestment_rate_year_one": 0.40, "reinvestment_rate_year_ten": 0.40}


def test_a_constant_growth_forecast_is_the_gordon_value():
    """Revenue 1,000 growing 3% every year, margin 20%, tax 25%, reinvestment 40%,
    WACC 9%. Next year's free cash flow to the firm:
        1,000 x 1.03 x 0.20 x (1 - 0.25) x (1 - 0.40) = 92.7
    and a cash flow growing at 3% for ever, at 9%, is worth
        92.7 / (0.09 - 0.03) = 1,545.
    The ten explicit years and the terminal value must add up to exactly that.
    """
    run = calculator.forecast(1000.0, GORDON, 0.25, 0.09)
    assert run["years"][0]["free_cash_flow_to_firm"] == pytest.approx(92.7)
    assert run["enterprise_value"] == pytest.approx(1545.0)


def test_the_bridge_to_a_share():
    """(1,545 - net debt 100 - leases 45) / 10 shares = 140 a share."""
    out = calculator.bridge(1545.0, 100.0, 45.0, 10.0)
    assert out["equity_value"] == pytest.approx(1400.0)
    assert out["value_per_share"] == pytest.approx(140.0)


FADE = {"revenue_growth_year_one": 0.12, "terminal_growth": 0.03,
        "operating_margin_year_one": 0.20, "operating_margin_year_ten": 0.20,
        "reinvestment_rate_year_one": 0.40, "reinvestment_rate_year_ten": 0.40}

# Growth fades from 12% to 3% in nine equal steps of one point. Worked by hand,
# free cash flow = revenue x 0.20 x 0.75 x 0.60 = revenue x 0.09, discounted at 9%:
#   year  growth  revenue            free cash flow     present value
#    1    12%     1,120.0            100.8              100.8 / 1.09        =  92.4771
#    2    11%     1,243.2            111.888            111.888 / 1.09^2    =  94.1739
#    3    10%     1,367.52           123.0768                               =  95.0379
#    4     9%     1,490.5968         134.153712                             =  95.0379
#    5     8%     1,609.844544       144.88600896                           =  94.1660
#    6     7%     1,722.53366208     155.0280295872                         =  92.4381
#    7     6%     1,825.8856818048   164.329711362432                       =  89.8940
#    8     5%     1,917.1799658950   172.546196930554                       =  86.5951
#    9     4%     1,993.8671645308   179.448044807776                       =  82.6229
#   10     3%     2,053.6831794668   184.831486152009                       =  78.0748
# explicit years 900.5176; terminal cash flow 184.8315 x 1.03 = 190.3764;
# terminal value 190.3764 / 0.06 = 3,172.9405; discounted 3,172.9405 / 1.09^10 = 1,340.2844;
# enterprise value 2,240.8020; per share (2,240.8020 - 145) / 10 = 209.5802.
FADE_TABLE = [(1120.0, 100.8), (1243.2, 111.888), (1367.52, 123.0768),
              (1490.5968, 134.153712), (1609.844544, 144.88600896),
              (1722.53366208, 155.0280295872), (1825.8856818048, 164.329711362432),
              (1917.1799658950, 172.546196930554), (1993.8671645308, 179.448044807776),
              (2053.6831794668, 184.831486152009)]


def test_a_fading_forecast_matches_the_hand_table():
    run = calculator.forecast(1000.0, FADE, 0.25, 0.09)
    for row, (revenue, cash) in zip(run["years"], FADE_TABLE):
        assert row["revenue"] == pytest.approx(revenue, rel=1e-12)
        assert row["free_cash_flow_to_firm"] == pytest.approx(cash, rel=1e-12)
    assert run["explicit_present"] == pytest.approx(900.5176, abs=1e-4)
    assert run["terminal_value"] == pytest.approx(3172.9405, abs=1e-4)
    assert run["enterprise_value"] == pytest.approx(2240.8020, abs=1e-4)
    assert calculator.bridge(run["enterprise_value"], 100.0, 45.0, 10.0)[
        "value_per_share"] == pytest.approx(209.5802, abs=1e-4)


def test_terminal_growth_above_the_risk_free_rate_is_refused():
    with pytest.raises(calculator.CalculatorInputError):
        calculator._drivers(dict(GORDON, terminal_growth=0.05), rf=0.0466)


def test_a_missing_driver_is_refused_not_invented():
    scenario = dict(GORDON)
    del scenario["reinvestment_rate_year_ten"]
    with pytest.raises(calculator.CalculatorInputError):
        calculator._drivers(scenario, rf=0.0466)


def test_reverse_dcf_finds_the_growth_the_price_implies():
    """At 140 a share the Gordon case above is priced exactly: constant growth 3%."""
    out = calculator.reverse_dcf(1000.0, GORDON, 0.25, 0.09, 100.0, 45.0, 10.0, 140.0)
    assert out["value"] == pytest.approx(0.03, abs=1e-8)


def test_the_sensitivity_grid_moves_wacc_by_a_point():
    """WACC 10%, growth 3%: 92.7 / 0.07 = 1,324.2857; (1,324.2857 - 145) / 10 = 117.92857.
    WACC 8%, growth 3%: 92.7 / 0.05 = 1,854; (1,854 - 145) / 10 = 170.9."""
    grid = calculator.sensitivity(1000.0, GORDON, 0.25, 0.09, 0.0466, 100.0, 45.0, 10.0)["grid"]
    assert grid[1][1]["value_per_share"] == pytest.approx(140.0)
    assert grid[2][1]["value_per_share"] == pytest.approx(117.92857, abs=1e-5)
    assert grid[0][1]["value_per_share"] == pytest.approx(170.9)
    assert grid[1][2]["terminal_growth"] == pytest.approx(0.035)


# --- adjustments ---------------------------------------------------------------------------

def test_an_adjustment_takes_its_amount_from_the_field_it_names():
    """The analyst names a field by its path in calculator.json and a direction; the
    amount is the field's value. The field here is the trailing-four-quarter increase
    in receivables, from NVIDIA's cash-flow statements: fiscal 2026 (15,399) in the
    10-K, plus six months of 2027 (24,590), less six months of 2026 (4,743), in the
    10-Q -- 35,246 million."""
    accounting = {"adjustments": [
        {"name": "working capital pulled forward", "direction": "reduce",
         "applies_to": "cash_flow",
         "calculator_field": "terms.trailing_four_quarters.change_in_receivables",
         "quote": "q"},
        {"name": "a field that is not there", "direction": "reduce",
         "calculator_field": "nowhere.at_all", "quote": "q"},
        {"name": "days named as dollars", "direction": "reduce",
         "calculator_field": "ratios.efficiency.days_sales_outstanding", "quote": "q"}]}
    out = calculator.calculate(ticker="NVDA", cutoff=NVDA_CUTOFF, period_end=NVDA_PERIOD_END,
                               form="10-Q", accounting=accounting)
    quality = out["free_cash_flow"]["free_cash_flow_quality_adjusted"]
    assert quality["adjustments_applied"][0]["amount"] == 35_246 * MILLION
    assert [row["calculator_field"] for row in quality["adjustments_refused"]] == [
        "nowhere.at_all", "ratios.efficiency.days_sales_outstanding"]
    before = quality["adjustments_applied"][0]["before"]
    assert quality["value"] == before - 35_246 * MILLION


# --- the whole file on NVIDIA ------------------------------------------------------------------

def test_nvidia_computes_everything_but_what_needs_a_price(nvda):
    assert all(line.startswith(("wacc:", "valuation:")) for line in nvda["missing"]), nvda["missing"]
    for name in ("free_cash_flow_simple", "free_cash_flow_to_firm",
                 "free_cash_flow_to_equity", "free_cash_flow_quality_adjusted"):
        assert "value" in nvda["free_cash_flow"][name], name


def test_the_dupont_product_is_return_on_equity(nvda):
    profitability = nvda["ratios"]["profitability"]
    assert profitability["dupont"]["product"]["value"] == pytest.approx(
        profitability["return_on_equity"]["value"])


def test_the_run_names_what_it_could_not_compute(nvda):
    assert any("Tiingo" in line for line in nvda["missing"])


# --- a filing companyfacts has not caught up with ----------------------------------------------

def test_a_filing_the_record_lacks_is_read_from_its_own_instance(tmp_path):
    """SEC's companyfacts held nothing Carrier filed after 2026-04-30 on 2026-09-28,
    though Carrier filed a 10-Q on 2026-07-28. The bundle's instance facts fill
    that one accession, entity-wide facts only, and the output names it."""
    document = {"ticker": "TEST", "facts": {"us-gaap": {"Revenues": {"units": {"USD": [
        {"start": "2025-01-01", "end": "2025-12-31", "val": 100.0, "accn": "A-1",
         "form": "10-K", "filed": "2026-02-05"}]}}}}}
    numbers = {"facts": [
        {"id": "B-2:f-1", "tag": "Revenues", "prefix": "us-gaap", "unit": "iso4217:USD",
         "context": {"start": "2026-01-01", "end": "2026-06-30", "segment": []},
         "number": 60.0, "nil": False, "form": "10-Q", "source_accession": "B-2",
         "filing_date": "2026-07-28"},
        {"id": "B-2:f-2", "tag": "Revenues", "prefix": "us-gaap", "unit": "iso4217:USD",
         "context": {"start": "2026-01-01", "end": "2026-06-30",
                     "segment": [{"dimension": "srt:SegmentAxis", "member": "x:One"}]},
         "number": 20.0, "nil": False, "form": "10-Q", "source_accession": "B-2",
         "filing_date": "2026-07-28"},
        {"id": "A-1:f-9", "tag": "Revenues", "prefix": "us-gaap", "unit": "iso4217:USD",
         "context": {"start": "2025-01-01", "end": "2025-12-31", "segment": []},
         "number": 999.0, "nil": False, "form": "10-K", "source_accession": "A-1",
         "filing_date": "2026-02-05"}]}
    (tmp_path / "input_numbers.json").write_text(json.dumps(numbers))
    out, added = calculator.supplemented(document, tmp_path)
    assert added == ["B-2"]
    rows = out["facts"]["us-gaap"]["Revenues"]["units"]["USD"]
    assert [(row.get("start"), row["end"], row["val"]) for row in rows] == [
        ("2025-01-01", "2025-12-31", 100.0), ("2026-01-01", "2026-06-30", 60.0)]
    assert document["facts"]["us-gaap"]["Revenues"]["units"]["USD"][0]["val"] == 100.0
    assert len(document["facts"]["us-gaap"]["Revenues"]["units"]["USD"]) == 1


# --- the rest of the free-cash-flow measures, from NVIDIA's filed figures ---------------------

def test_free_cash_flow_to_the_firm_is_worked_from_the_filed_figures(nvda):
    """Trailing four quarters, each from the 10-K (fiscal 2026) and the 10-Q
    (six months of 2027 and of 2026), in millions:
      operating income   130,387 + 117,270 - 50,078 = 197,579
      pretax income      141,450 + 141,410 - 53,117 = 229,743
      income tax          21,383 +  23,400 -  7,920 =  36,863
      tax rate           36,863 / 229,743 = 0.160453..., inside 0 and 0.21
      depreciation and amortization  2,843 + 2,124 - 1,280 = 3,687
      capital expenditure                                  = 7,354 (above)
    Trade working capital, receivables + inventory - payables:
      2026-07-26 (the 10-Q's balance sheet)   63,059 + 31,575 - 15,059 = 79,575
      2025-07-27 (companyfacts rows of 0001045810-25-000209)
                                              27,808 + 14,962 -  9,064 = 33,706
      change 45,869
    Free cash flow to the firm
      197,579 x (1 - 36,863/229,743) + 3,687 - 7,354 - 45,869 = 116,340.8168
    """
    to_firm = nvda["free_cash_flow"]["free_cash_flow_to_firm"]
    assert to_firm["value"] / MILLION == pytest.approx(116_340.8168, abs=1e-3)
    trade = to_firm["trade_working_capital"]
    assert trade["now"]["value"] == 79_575 * MILLION
    assert trade["a_year_earlier"]["value"] == 33_706 * MILLION
    assert nvda["tax_rate"]["value"] == pytest.approx(36_863 / 229_743)


def test_free_cash_flow_to_equity_adds_the_debt_nvidia_issued(nvda):
    """The 10-Q: 'Proceeds related to issuance of debt, net of costs 24,896' for the
    six months of 2027 and '—' for 2026; the 10-K's fiscal 2026 column prints no
    issuance and '—' under repayment of debt. Net borrowing 24,896;
    127,006 + 24,896 = 151,902."""
    to_equity = nvda["free_cash_flow"]["free_cash_flow_to_equity"]
    assert to_equity["net_borrowing"] == 24_896 * MILLION
    assert to_equity["value"] == 151_902 * MILLION


def test_cash_over_income_is_worked_from_the_filed_figures(nvda):
    """Net income, trailing: 120,067 (10-K) + 118,010 - 45,197 (10-Q six months) = 192,880;
    operating cash flow 134,360 (above); 134,360 / 192,880 = 0.696599..."""
    ratio = nvda["earnings_versus_cash"]["operating_cash_flow_over_net_income"]
    assert ratio["value"] == pytest.approx(134_360 / 192_880)


def test_the_current_ratio_is_the_balance_sheets():
    """NVIDIA's 10-Q balance sheet at 2026-07-26: total current assets 197,412, total
    current liabilities 43,019."""
    out = calculator.calculate(ticker="NVDA", cutoff=NVDA_CUTOFF, period_end=NVDA_PERIOD_END,
                               form="10-Q")
    assert out["ratios"]["liquidity"]["current_ratio"]["value"] == pytest.approx(197_412 / 43_019)


# --- a line stated twice is read once ---------------------------------------------------------

def test_generacs_debt_is_its_balance_sheets():
    """Generac's 10-Q for the quarter ended 2026-06-30 prints, in thousands:
    short-term borrowings 48,318; current portion of long-term borrowings and
    finance lease obligations 32,052; long-term borrowings and finance lease
    obligations 1,248,958. Total debt 1,329,328. The record also tags
    `LongTermDebtNoncurrent` and `LongTermDebtCurrent` for the same instant --
    components of the two lines above -- and they are not added again."""
    out = calculator.calculate(ticker="GNRC", cutoff="2026-08-04", period_end="2026-06-30",
                               form="10-Q")
    debt = out["terms"]["debt_now"]
    assert debt["value"] == 1_329_328_000
    set_aside = {line["tag"] for part in debt["parts"].values()
                 for line in part["lines_not_added"]}
    assert {"LongTermDebtNoncurrent", "LongTermDebtCurrent"} <= set_aside


def _rows(**tags):
    return {"ticker": "TEST", "facts": {"us-gaap": {
        tag: {"units": {"USD": [dict(row, accn="0000000000-26-000001", form="10-K",
                                     filed="2026-02-20") for row in rows]}}
        for tag, rows in tags.items()}}}


YEAR = {"start": "2025-01-01", "end": "2025-12-31"}


def test_a_subtotal_replaces_the_lines_it_adds_up():
    """Apple's fiscal 2025: commercial paper, net -2,032 = -5,820 + 5,836 - 2,048
    (the three lines it also tags). Read once, as the subtotal."""
    record = calculator.Record(_rows(
        ProceedsFromRepaymentsOfCommercialPaper=[dict(YEAR, val=-2032)],
        ProceedsFromRepaymentsOfShortTermDebtMaturingInThreeMonthsOrLess=[dict(YEAR, val=-5820)],
        ProceedsFromShortTermDebtMaturingInMoreThanThreeMonths=[dict(YEAR, val=5836)],
        RepaymentsOfShortTermDebtMaturingInMoreThanThreeMonths=[dict(YEAR, val=2048)]))
    cell = record.family("borrowing_short_term_net", ("2025-01-01", "2025-12-31"))
    assert calculator.family_cash_effect(cell) == -2032
    assert len(cell["lines_not_added"]) == 3


def test_separate_repayment_lines_are_both_added():
    """Cisco's fiscal 2024: repayments of convertible debt 3,140 and of other long-term
    debt 9,826 are two lines of the statement; repaid 12,966, an outflow."""
    record = calculator.Record(_rows(
        RepaymentsOfConvertibleDebt=[dict(YEAR, val=3140)],
        RepaymentsOfOtherLongTermDebt=[dict(YEAR, val=9826)]))
    cell = record.family("borrowing_repaid", ("2025-01-01", "2025-12-31"))
    assert cell["value"] == 12_966
    assert calculator.family_cash_effect(cell) == -12_966


def test_net_borrowing_carries_each_lines_sign():
    """Issued 50 (inflow), repaid 20 (outflow), short-term net -5 (signed): 50 - 20 - 5 = 25."""
    record = calculator.Record(_rows(
        ProceedsFromIssuanceOfLongTermDebt=[dict(YEAR, val=50)],
        RepaymentsOfLongTermDebt=[dict(YEAR, val=20)],
        ProceedsFromRepaymentsOfShortTermDebt=[dict(YEAR, val=-5)]))
    span = ("2025-01-01", "2025-12-31")
    total = sum(calculator.family_cash_effect(record.family(name, span))
                for name in ("borrowing_issued", "borrowing_repaid", "borrowing_short_term_net"))
    assert total == 25


# --- a lease the quarter does not restate -----------------------------------------------------

def test_a_lease_balance_the_quarter_omits_is_the_newest_filed_and_dated():
    record = calculator.Record(_rows(OperatingLeaseLiability=[
        {"end": "2025-12-31", "val": 400}]))
    cell = record.latest_balance("operating_lease_liability", "2026-06-30")
    assert cell["value"] == 400
    assert cell["as_of"] == "2025-12-31"


def test_a_lease_never_filed_is_missing_not_zero():
    record = calculator.Record(_rows(Revenues=[dict(YEAR, val=1)]))
    assert "missing" in record.latest_balance("operating_lease_liability", "2026-06-30")


# --- the fourth quarter -----------------------------------------------------------------------

def test_a_fourth_quarter_is_the_year_less_nine_months():
    """Revenue 400 for the year and 290 for the nine months on the same start: 110."""
    record = calculator.Record(_rows(Revenues=[
        dict(YEAR, val=400), {"start": "2025-01-01", "end": "2025-09-30", "val": 290}]))
    spans = calculator.durations(record.usd)
    cell = calculator.quarter(record, "revenue", spans, dt.date(2025, 12, 31))
    assert cell["value"] == 110


# --- the cost of capital ----------------------------------------------------------------------

def test_wacc_is_the_textbook_weighted_average():
    """Risk-free 4%, beta 1.2, premium 5%: cost of equity 0.04 + 1.2 x 0.05 = 0.10.
    Equity 900 (price 9 x 100 shares), debt 100, interest 5 on average debt 100:
    cost of debt 0.05; tax 21%. WACC = 0.9 x 0.10 + 0.1 x 0.05 x 0.79 = 0.09395."""
    cell = lambda v: {"value": v, "id": "x", "tag": "t", "period": "p"}
    terms = {"trailing_four_quarters": {"interest_expense": cell(5.0)},
             "debt_now": {"value": 100.0}, "debt_a_year_earlier": {"value": 100.0},
             "shares_outstanding": cell(100.0)}
    sections = {"tax_rate": {"value": 0.21}}
    market_data = {"beta": {"value": 1.2}, "price": {"value": 9.0}}
    original = calculator.risk_free_rate, calculator.equity_risk_premium
    try:
        calculator.risk_free_rate = lambda cutoff: {"value": 0.04}
        calculator.equity_risk_premium = lambda cutoff: {"value": 0.05}
        out = calculator.cost_of_capital(terms, sections, market_data, dt.date(2026, 1, 1), None)
    finally:
        calculator.risk_free_rate, calculator.equity_risk_premium = original
    assert out["cost_of_equity"]["value"] == pytest.approx(0.10)
    assert out["pre_tax_cost_of_debt"]["value"] == pytest.approx(0.05)
    assert out["wacc"]["value"] == pytest.approx(0.09395)


# --- what the accounting adjustments move -----------------------------------------------------

def test_a_one_time_adjustment_moves_value_once():
    """A receivables build of 35 on 10 diluted shares, not marked recurring: 140 - 3.5."""
    moved = {"applied": [{"name": "receivables build", "direction": "reduce",
                          "applies_to": "cash_flow", "amount": 35.0}], "nopat": 100.0}
    out = calculator.adjusted_value(1000.0, GORDON, 0.25, 0.09, 100.0, 45.0, 10.0, 140.0,
                                    moved, {"revenue": {"value": 1000.0}})
    assert out["each"][0]["moved_per_share"] == pytest.approx(-3.5)
    assert out["all_together"]["value_per_share"] == pytest.approx(136.5)


def test_an_earnings_adjustment_lowers_the_margin_in_every_year():
    """The Gordon case, with an earnings adjustment of 10 against revenue of 1,000:
    margin 0.20 - 0.01 = 0.19; next year's cash flow 1,030 x 0.19 x 0.75 x 0.6 = 88.065;
    value 88.065 / 0.06 = 1,467.75; per share (1,467.75 - 145) / 10 = 132.275, which is
    7.725 below the unadjusted 140."""
    ttm = {"revenue": {"value": 1000.0}}
    moved = {"applied": [{"name": "a reserve release", "direction": "reduce",
                          "applies_to": "earnings", "amount": 10.0, "recurs": True}],
             "nopat": None}
    out = calculator.adjusted_value(1000.0, GORDON, 0.25, 0.09, 100.0, 45.0, 10.0, 140.0,
                                    moved, ttm)
    assert out["each"][0]["value_per_share"] == pytest.approx(132.275)
    assert out["each"][0]["moved_per_share"] == pytest.approx(-7.725)


def test_a_filing_fact_filed_after_the_cutoff_is_not_added(tmp_path):
    document = {"ticker": "TEST", "facts": {"us-gaap": {}}}
    numbers = {"facts": [
        {"id": "C-3:f-1", "tag": "Revenues", "prefix": "us-gaap", "unit": "iso4217:USD",
         "context": {"start": "2026-07-01", "end": "2026-09-30", "segment": []},
         "number": 70.0, "nil": False, "form": "10-Q", "source_accession": "C-3",
         "filing_date": "2026-10-28"}]}
    (tmp_path / "input_numbers.json").write_text(json.dumps(numbers))
    out, added = calculator.supplemented(document, tmp_path, dt.date(2026, 7, 28))
    assert added == []
    assert out["facts"]["us-gaap"] == {}


def test_a_carried_lease_says_when_the_period_end_holds_more():
    """The shape the refute-check found at Palo Alto Networks on 2026-04-30: a total
    of 417.4 million filed at the prior year end, and a noncurrent line alone of
    719.0 million at the period end."""
    record = calculator.Record(_rows(
        OperatingLeaseLiability=[{"end": "2025-07-31", "val": 417_400_000}],
        OperatingLeaseLiabilityNoncurrent=[{"end": "2026-04-30", "val": 719_000_000}]))
    cell = record.latest_balance("operating_lease_liability", "2026-04-30")
    assert cell["value"] == 417_400_000
    assert "contradicted_at_period_end" in cell


def test_a_field_path_may_index_a_list():
    assert calculator.field_value({"a": {"b": [{"c": 1.5}]}}, "a.b.0.c") == 1.5
    assert calculator.field_value({"a": {"b": [{"c": 1.5}]}}, "a.b.3.c") is None


@pytest.mark.parametrize("part, value", [
    ("0", 1.5), ("3", 4.5), ("4", None), ("²", None), ("①", None), ("٣", None)],
    ids=["zero", "three", "past_the_end", "superscript_two", "circled_one", "arabic_indic_three"])
def test_a_field_path_indexes_a_list_by_ascii_digits_alone(part, value):
    """'²' and '①' are digits to `str.isdigit` and not to `int`, which raised
    ValueError; '٣' is a digit to both and read the fourth element. Each now
    names nothing. The other side, before and after: ASCII digits name their
    element, and an index past the end names nothing."""
    tree = {"a": {"b": [{"c": 1.5}, {"c": 2.5}, {"c": 3.5}, {"c": 4.5}]}}
    assert calculator.field_value(tree, f"a.b.{part}.c") == value


def test_the_filings_only_view_carries_no_price(nvda):
    """The accounting and financial analysts never see a price (CLAUDE.md)."""
    priced = dict(nvda, market={"price": {"value": 170.0}, "beta": {"value": 1.9}})
    view = calculator.filings_only(priced)
    assert "market" not in view and "cost_of_capital" not in view and "valuation" not in view
    assert "price" not in json.dumps(view).replace("proceeds_from_sale", "")
    assert view["free_cash_flow"] == nvda["free_cash_flow"]


def test_a_price_left_in_another_section_is_refused(nvda):
    leaked = dict(nvda, ratios=dict(nvda["ratios"], stray={"price_at_cutoff": 1.0}))
    with pytest.raises(calculator.CalculatorInputError):
        calculator.filings_only(leaked)


def test_qualcomms_debt_is_its_balance_sheets():
    """Qualcomm's 10-Q for the quarter ended 2026-06-28 prints short-term debt 2,489
    and long-term debt 12,781 (millions): total 15,270. The long-term line is tagged
    `LongTermDebt`, and no noncurrent tag is on record at that date."""
    out = calculator.calculate(ticker="QCOM", cutoff="2026-07-29", period_end="2026-06-28",
                               form="10-Q")
    debt = out["terms"]["debt_now"]
    assert debt["value"] == 15_270 * MILLION
    assert "check" in debt["parts"]["debt_noncurrent"]


def test_a_recurring_cash_flow_adjustment_raises_reinvestment_in_every_year():
    """The Gordon case with a recurring cash-flow adjustment of 15 against after-tax
    operating income of 100: reinvestment 0.40 + 0.15 = 0.55; next year's cash flow
    1,030 x 0.20 x 0.75 x 0.45 = 69.525; value 69.525 / 0.06 = 1,158.75; per share
    (1,158.75 - 145) / 10 = 101.375, which is 38.625 below 140."""
    moved = {"applied": [{"name": "factoring that will continue", "direction": "reduce",
                          "applies_to": "cash_flow", "amount": 15.0, "recurs": True}],
             "nopat": 100.0}
    out = calculator.adjusted_value(1000.0, GORDON, 0.25, 0.09, 100.0, 45.0, 10.0, 140.0,
                                    moved, {"revenue": {"value": 1000.0}})
    assert out["each"][0]["value_per_share"] == pytest.approx(101.375)
    assert out["each"][0]["moved_per_share"] == pytest.approx(-38.625)


def test_the_valuation_analyst_may_state_a_missing_cost_of_debt_with_a_quote():
    """Interest expense is not on record; the analyst quotes the notes' rate, 5%.
    With the textbook case above the WACC is 0.9 x 0.10 + 0.1 x 0.05 x 0.79 = 0.09395."""
    cell = lambda v: {"value": v, "id": "x", "tag": "t", "period": "p"}
    terms = {"trailing_four_quarters": {"interest_expense": {"missing": "no row"}},
             "debt_now": {"value": 100.0}, "debt_a_year_earlier": {"value": 100.0},
             "shares_outstanding": cell(100.0)}
    original = calculator.risk_free_rate, calculator.equity_risk_premium
    try:
        calculator.risk_free_rate = lambda cutoff: {"value": 0.04}
        calculator.equity_risk_premium = lambda cutoff: {"value": 0.05}
        without = calculator.cost_of_capital(terms, {"tax_rate": {"value": 0.21}},
                                             {"beta": {"value": 1.2}, "price": {"value": 9.0}},
                                             dt.date(2026, 1, 1), None)
        chosen = calculator.cost_of_capital(
            terms, {"tax_rate": {"value": 0.21}},
            {"beta": {"value": 1.2}, "price": {"value": 9.0}}, dt.date(2026, 1, 1),
            {"pre_tax_cost_of_debt": {"value": 0.05, "reason": "the notes' coupon",
                                      "quote": "bear interest at 5.00%"}})
    finally:
        calculator.risk_free_rate, calculator.equity_risk_premium = original
    # Until 2026-10-06 a missing interest expense left the WACC uncomputed here. The
    # owner's default of that day (docs/needs_judgment.md) fills it with the
    # risk-free rate plus one point, labelled: 0.04 + 0.01 = 0.05, the same 0.09395.
    assert "fallback" in without["pre_tax_cost_of_debt"]
    assert without["wacc"]["value"] == pytest.approx(0.09395)
    assert chosen["pre_tax_cost_of_debt"]["chosen_by"] == "the valuation analyst"
    assert chosen["wacc"]["value"] == pytest.approx(0.09395)


def _wacc_with(ttm: dict, rf: float = 0.04, debt_ago: dict | None = None) -> dict:
    cell = lambda v: {"value": v, "id": "x", "tag": "t", "period": "p"}
    terms = {"trailing_four_quarters": ttm, "debt_now": {"value": 100.0},
             "debt_a_year_earlier": debt_ago or {"value": 100.0},
             "shares_outstanding": cell(100.0)}
    original = calculator.risk_free_rate, calculator.equity_risk_premium
    try:
        calculator.risk_free_rate = lambda cutoff: {"value": rf}
        calculator.equity_risk_premium = lambda cutoff: {"value": 0.05}
        return calculator.cost_of_capital(terms, {"tax_rate": {"value": 0.21}},
                                          {"beta": {"value": 1.2}, "price": {"value": 9.0}},
                                          dt.date(2026, 1, 1), None)
    finally:
        calculator.risk_free_rate, calculator.equity_risk_premium = original


def test_interest_paid_stands_in_when_no_interest_expense_is_tagged():
    """No interest expense; interest paid 4 on average debt 100: cost of debt 0.04.
    WACC = 0.9 x 0.10 + 0.1 x 0.04 x 0.79 = 0.09 + 0.00316 = 0.09316."""
    cell = {"value": 4.0, "id": "x", "tag": "InterestPaidNet", "period": "p"}
    out = _wacc_with({"interest_expense": {"missing": "no row"}, "interest_paid": cell})
    assert out["pre_tax_cost_of_debt"]["value"] == pytest.approx(0.04)
    assert "interest paid" in out["pre_tax_cost_of_debt"]["fallback"]
    assert out["wacc"]["value"] == pytest.approx(0.09316)


def test_the_risk_free_fallback_is_one_point_over_the_rate_and_says_so():
    """Neither interest expense nor interest paid (AAPL tagged InterestPaidNet last for
    fiscal 2023): risk-free 4.66% + 1 point = 5.66%."""
    out = _wacc_with({"interest_expense": {"missing": "no row"},
                      "interest_paid": {"missing": "no row"}}, rf=0.0466)
    debt = out["pre_tax_cost_of_debt"]
    assert debt["value"] == pytest.approx(0.0566)
    assert "risk-free rate plus one point" in debt["fallback"]
    assert "neither interest expense nor interest paid is on record" in debt["fallback"]
    assert debt["needs_judgment"] == ("docs/needs_judgment.md: the pre-tax cost of debt "
                                      "when the record carries no interest expense")


def test_the_fallback_label_says_which_input_was_missing():
    """Two-sided, after the second lens's finding of 2026-10-06. Interest paid 4 is
    on record and the year-earlier debt is not, so average debt is missing: the
    cost of debt is still the risk-free rate plus one point, 0.04 + 0.01 = 0.05,
    and the label says interest paid is on record and the debt is not. With
    neither interest expense nor interest paid on record the label says that, and
    not the other. Both reach WACC = 0.9 x 0.10 + 0.1 x 0.05 x 0.79 = 0.09395."""
    paid = {"value": 4.0, "id": "x", "tag": "InterestPaidNet", "period": "p"}
    only_debt_missing = _wacc_with({"interest_expense": {"missing": "no row"},
                                    "interest_paid": paid},
                                   debt_ago={"missing": "no debt a year earlier"})
    debt = only_debt_missing["pre_tax_cost_of_debt"]
    assert debt["value"] == pytest.approx(0.05)
    assert ("interest paid is on record but average debt is missing/zero, so the cost "
            "of debt is the risk-free rate plus one point") in debt["fallback"]
    assert "no debt a year earlier" in debt["fallback"]
    assert "neither interest expense nor interest paid" not in debt["fallback"]
    assert only_debt_missing["wacc"]["value"] == pytest.approx(0.09395)

    neither = _wacc_with({"interest_expense": {"missing": "no row"},
                          "interest_paid": {"missing": "no row"}})
    debt = neither["pre_tax_cost_of_debt"]
    assert debt["value"] == pytest.approx(0.05)
    assert "neither interest expense nor interest paid is on record" in debt["fallback"]
    assert "interest paid is on record but" not in debt["fallback"]
    assert neither["wacc"]["value"] == pytest.approx(0.09395)


def test_a_zero_average_debt_is_labelled_like_a_missing_one():
    """The fallback called as cost_of_capital calls it, with debt on record at zero
    both now and a year earlier: average debt is zero, interest paid 4 is on
    record, and the label says so."""
    paid = {"value": 4.0, "id": "x", "tag": "InterestPaidNet", "period": "p"}
    out = calculator.cost_of_debt_fallback(
        {"interest_expense": {"missing": "no row"}, "interest_paid": paid},
        {"value": 0.0}, {"value": 0.0}, {"value": 0.04}, "interest_expense: no row")
    assert out["value"] == pytest.approx(0.05)
    assert "interest paid is on record but average debt is missing/zero" in out["fallback"]
    assert "average_debt is zero" in out["fallback"]


def test_the_ladder_runs_under_a_tagged_interest_expense_with_no_average_debt():
    """Two-sided, after the second lens's third reading. Interest expense 5 is on
    record and the year-earlier debt is not, so the primary is missing on its
    denominator: interest paid over the same average debt is impossible too, so the
    rate is the risk-free rate plus one point, 0.04 + 0.01 = 0.05, and the label
    says interest expense is on record and the debt is not. With everything on
    record there is no fallback at all: 5 / 100 = 0.05 by the primary formula."""
    cell = lambda v: {"value": v, "id": "x", "tag": "t", "period": "p"}
    out = _wacc_with({"interest_expense": cell(5.0), "interest_paid": cell(4.0)},
                     debt_ago={"missing": "no debt a year earlier"})
    debt = out["pre_tax_cost_of_debt"]
    assert debt["value"] == pytest.approx(0.05)
    assert debt["formula"] == "risk_free_rate + 0.01"
    assert debt["fallback"].endswith("interest expense is on record but average debt is "
                                     "missing/zero: average_debt: no debt a year earlier")
    assert "interest paid" not in debt["fallback"]
    assert out["wacc"]["value"] == pytest.approx(0.09395)

    whole = _wacc_with({"interest_expense": cell(5.0), "interest_paid": cell(4.0)})
    assert whole["pre_tax_cost_of_debt"]["formula"] == "interest_expense / average debt"
    assert "fallback" not in whole["pre_tax_cost_of_debt"]


def test_a_refused_interest_paid_is_labelled_on_record_not_absent():
    """A hand-built trailing term refused the way trends.as_filed refuses one filing's
    two values for one period: the label says interest paid is on record but refused,
    with the trends module's reason, and not that nothing is on record."""
    from src import trends
    reason = ("us-gaap:InterestPaidNet for 2025-12-28..2026-06-27 is reported as "
              "[13091000.0, 13100000.0] by the filing of 2026-07-29 "
              f"(0001628280-26-050481) — {trends.TWO_VALUES}")
    out = calculator.cost_of_debt_fallback(
        {"interest_expense": {"missing": "no row"}, "interest_paid": {"missing": reason}},
        {"value": 100.0}, {"value": 100.0}, {"value": 0.04}, "interest_expense: no row")
    assert out["value"] == pytest.approx(0.05)
    assert "interest paid is on record but refused: " + reason in out["fallback"]
    assert "neither interest expense nor interest paid" not in out["fallback"]
    absent = calculator.cost_of_debt_fallback(
        {"interest_expense": {"missing": "no row"}, "interest_paid": {"missing": "no row"}},
        {"value": 100.0}, {"value": 100.0}, {"value": 0.04}, "interest_expense: no row")
    assert "neither interest expense nor interest paid is on record" in absent["fallback"]
    assert "refused" not in absent["fallback"]


def test_a_refused_interest_expense_is_labelled_on_record_before_the_ladder_steps_down():
    """Two-sided. Interest expense refused the way trends.as_filed refuses one filing's
    two values for one period: with interest paid 4 on average debt 100 the ladder
    steps down to 0.04 and the label says interest expense is on record but refused,
    with the trends module's reason, not "not on record"; with interest paid absent
    too, the label says the expense is refused and the paid is absent, and the
    "neither" words appear only when both are absent."""
    from src import trends
    reason = ("us-gaap:InterestExpense for 2025-01-01..2025-12-31 is reported as "
              "[5000000.0, 5100000.0] by the filing of 2026-02-19 "
              f"(0001628280-26-000001) — {trends.TWO_VALUES}")
    paid = {"value": 4.0, "id": "x", "tag": "InterestPaidNet", "period": "p"}
    stepped = calculator.cost_of_debt_fallback(
        {"interest_expense": {"missing": reason}, "interest_paid": paid},
        {"value": 100.0}, {"value": 100.0}, {"value": 0.04}, f"interest_expense: {reason}")
    assert stepped["value"] == pytest.approx(0.04)
    assert "interest expense is on record but refused: " + reason in stepped["fallback"]
    assert "not on record" not in stepped["fallback"]

    alone = calculator.cost_of_debt_fallback(
        {"interest_expense": {"missing": reason}, "interest_paid": {"missing": "no row"}},
        {"value": 100.0}, {"value": 100.0}, {"value": 0.04}, f"interest_expense: {reason}")
    assert alone["value"] == pytest.approx(0.05)
    assert "interest expense is on record but refused: " + reason in alone["fallback"]
    assert "interest paid is not on record: no row" in alone["fallback"]
    assert "neither" not in alone["fallback"]

    neither = calculator.cost_of_debt_fallback(
        {"interest_expense": {"missing": "no row"}, "interest_paid": {"missing": "no row"}},
        {"value": 100.0}, {"value": 100.0}, {"value": 0.04}, "interest_expense: no row")
    assert "neither interest expense nor interest paid is on record" in neither["fallback"]
    assert "refused" not in neither["fallback"]


def test_tagged_interest_expense_is_never_replaced_by_a_fallback():
    cell = lambda v: {"value": v, "id": "x", "tag": "t", "period": "p"}
    out = _wacc_with({"interest_expense": cell(5.0), "interest_paid": cell(4.0)})
    assert out["pre_tax_cost_of_debt"]["value"] == pytest.approx(0.05)
    assert "fallback" not in out["pre_tax_cost_of_debt"]


def test_cash_runway_is_months_of_cash_at_the_trailing_burn():
    """Cash 120, free cash flow -24 a year: a burn of 2 a month, 60 months. With free
    cash flow positive there is no burn and no runway, and it says so."""
    out = calculator.runway_months({"value": 120.0}, {"value": -24.0})
    assert out["value"] == pytest.approx(60.0)
    assert calculator.runway_months({"value": 120.0}, {"value": 5.0})["not_burning_cash"]


# --- the three sanity checks beside the DCF, on Ciena's record ---------------------------------
#
# Ciena's 10-Q for the quarter ended 2026-05-02 (0001628280-26-040767, filed
# 2026-06-04) is the trigger. Every fact below is a row of
# tests/fixtures/CIEN/companyfacts.json.gz, quoted by concept, period and value,
# in thousands of dollars (the record states dollars), the row read being the
# latest filing at or before the cutoff that states the period. The market-wide
# inputs are planted by the tests and labelled so: risk-free rate 4%, equity risk
# premium 5%, beta 1.2, so the cost of equity is 0.04 + 1.2 x 0.05 = 0.10; the
# price is named in each test.
#
# Trailing four quarters = fiscal 2025 (2024-11-03..2025-11-01, the 10-K filed
# 2025-12-12) + six months of fiscal 2026 (2025-11-02..2026-05-02) - six months
# of fiscal 2025 (2024-11-03..2025-05-03), the last two from the 10-Q:
#   Revenues                                   4,769,507 + 2,997,781 - 2,198,138 = 5,569,150
#   OperatingIncomeLoss                          197,531 +   427,283 -   113,505 =   511,309
#   IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest
#                                                156,287 +   412,175 -    87,610 =   480,852
#   IncomeTaxExpenseBenefit                       32,949 +    43,672 -    34,069 =    42,552
#   InterestExpenseNonoperating                   89,403 +    42,176 -    44,615 =    86,964
#   NetCashProvidedByUsedInOperatingActivities   806,093 +   487,347 -   260,669 = 1,032,771
#   PaymentsToAcquirePropertyPlantAndEquipment   140,801 +   114,933 -    55,622 =   200,112
#   RepaymentsOfLongTermDebt                      11,580 +     5,790 -     5,790 =    11,580
#   Depreciation + AmortizationOfIntangibleAssets, the two lines the record carries
#   where no total is tagged:
#                        (104,133 + 25,758) + (67,021 + 8,449) - (49,771 + 13,090) =   142,500
# Balances at 2026-05-02 (the 10-Q) and at 2025-05-03 (the 10-Q filed 2025-06-05):
#   AccountsReceivableNetCurrent        1,052,569      929,799
#   InventoryNet                          808,447      874,326
#   AccountsPayableCurrent                606,599      419,077
#   LongTermDebtCurrent                    11,580       11,580
#   LongTermDebtNoncurrent              1,519,539    1,528,776
#   CashAndCashEquivalentsAtCarryingValue 1,045,126 at 2026-05-02
#   ShortTermInvestments                  157,708   at 2026-05-02
#   OperatingLeaseLiabilityCurrent 12,396 and OperatingLeaseLiabilityNoncurrent 31,996 at 2026-05-02
# Shares: dei:EntityCommonStockSharesOutstanding at 2026-05-29, the 10-Q's cover,
# 141,552,922; WeightedAverageNumberOfDilutedSharesOutstanding for the quarter
# 2026-02-01..2026-05-02, 146,314,000.
#
# Worked from those:
#   tax rate                    42,552 / 480,852 = 0.0884929, inside 0 and 0.21
#   after-tax operating income  511,309 x (1 - 0.0884929) = 466,061.771
#   trade working capital       2026-05-02: 1,052,569 + 808,447 - 606,599 = 1,254,417
#                               2025-05-03:   929,799 + 874,326 - 419,077 = 1,385,048
#                               change -130,631
#   free cash flow to the firm  466,061.771 + 142,500 - 200,112 + 130,631 = 539,080.771
#   free cash flow to equity    1,032,771 - 200,112 - 11,580 = 821,079
#   total debt                  2026-05-02: 11,580 + 1,519,539 = 1,531,119
#                               2025-05-03: 11,580 + 1,528,776 = 1,540,356; average 1,535,737.5
#   net debt                    1,531,119 - (1,045,126 + 157,708) = 328,285
#   operating lease liability   12,396 + 31,996 = 44,392
#   pre-tax cost of debt        86,964 / 1,535,737.5 = 0.0566269
#   after tax                   0.0566269 x (1 - 0.0884929) = 0.0516158

CIEN_CUTOFF, CIEN_PERIOD_END = "2026-06-04", "2026-05-02"
CIEN_SHARES_OUTSTANDING = 141_552_922
CIEN_DILUTED_SHARES = 146_314_000
CIEN_TAX_RATE = 42_552 / 480_852
CIEN_FREE_CASH_FLOW_TO_FIRM = (511_309 * (1 - CIEN_TAX_RATE) + 142_500 - 200_112 + 130_631) * 1000
CIEN_FREE_CASH_FLOW_TO_EQUITY = 821_079 * 1000
CIEN_TOTAL_DEBT = 1_531_119 * 1000
CIEN_COST_OF_DEBT_AFTER_TAX = 86_964 / 1_535_737.5 * (1 - CIEN_TAX_RATE)

PLANTED_RISK_FREE = {"value": 0.04, "date": "2026-06-04", "series": "DGS10",
                     "source": "planted by the test"}
PLANTED_PREMIUM = {"value": 0.05, "month_start": "2026-06-01", "source": "planted by the test"}


def _cien(price: float, assumptions: dict | None = None) -> dict:
    original = calculator.risk_free_rate, calculator.equity_risk_premium
    try:
        calculator.risk_free_rate = lambda cutoff: dict(PLANTED_RISK_FREE)
        calculator.equity_risk_premium = lambda cutoff: dict(PLANTED_PREMIUM)
        return calculator.calculate(
            ticker="CIEN", cutoff=CIEN_CUTOFF, period_end=CIEN_PERIOD_END, form="10-Q",
            accession="0001628280-26-040767",
            market_data={"beta": {"value": 1.2},
                         "price": {"value": price, "unit": "USD per share",
                                   "source": "planted by the test"}},
            assumptions=assumptions)
    finally:
        calculator.risk_free_rate, calculator.equity_risk_premium = original


@pytest.fixture(scope="module")
def cien_at_100():
    return _cien(100.0)


def test_cienas_record_reads_as_the_hand_table_above_for_the_free_cash_flow_yield(cien_at_100):
    """The inputs the three checks share, each against the hand table."""
    ttm = cien_at_100["terms"]["trailing_four_quarters"]
    assert ttm["revenue"]["value"] == 5_569_150 * 1000
    assert ttm["depreciation_and_amortization"]["value"] == 142_500 * 1000
    assert cien_at_100["tax_rate"]["value"] == pytest.approx(CIEN_TAX_RATE)
    free = cien_at_100["free_cash_flow"]
    assert free["free_cash_flow_to_firm"]["value"] == pytest.approx(CIEN_FREE_CASH_FLOW_TO_FIRM)
    assert free["free_cash_flow_to_equity"]["value"] == CIEN_FREE_CASH_FLOW_TO_EQUITY
    assert cien_at_100["terms"]["debt_now"]["value"] == CIEN_TOTAL_DEBT
    assert cien_at_100["ratios"]["solvency"]["net_debt"]["value"] == 328_285 * 1000
    assert cien_at_100["ratios"]["solvency"]["operating_lease_liability"]["value"] == 44_392 * 1000
    assert cien_at_100["terms"]["shares_outstanding"]["value"] == CIEN_SHARES_OUTSTANDING
    assert cien_at_100["terms"]["diluted_shares"]["value"] == CIEN_DILUTED_SHARES


def test_cienas_free_cash_flow_yield_is_worked_from_the_filed_figures(cien_at_100):
    """At a planted price of 100 a share:
      market value of equity  100 x 141,552,922 = 14,155,292,200
      enterprise value        14,155,292,200 + 328,285,000 + 44,392,000 = 14,527,969,200
      free cash flow to the firm over enterprise value
                              539,080,771 / 14,527,969,200 = 0.0371064
      free cash flow to equity over market value of equity
                              821,079,000 / 14,155,292,200 = 0.0580051
    """
    out = cien_at_100["free_cash_flow_yield"]
    assert out["price_at_cutoff"]["value"] == 100.0
    assert out["enterprise_value"]["value"] == pytest.approx(14_527_969_200)
    assert out["enterprise_value"]["formula"] == (
        "market_value_of_equity + net_debt + operating_lease_liability")
    to_firm = out["free_cash_flow_to_firm_over_enterprise_value"]
    to_equity = out["free_cash_flow_to_equity_over_market_value_of_equity"]
    assert to_firm["value"] == pytest.approx(539_080_771 / 14_527_969_200, abs=1e-9)
    assert to_firm["value"] == pytest.approx(0.0371064, abs=5e-8)
    assert to_equity["value"] == pytest.approx(821_079_000 / 14_155_292_200)
    assert to_equity["value"] == pytest.approx(0.0580051, abs=5e-8)


def test_cienas_wacc_components_table_names_each_input_and_its_source(cien_at_100):
    """At a planted price of 100 a share:
      E = 14,155,292,200;  D = 1,531,119,000;  D + E = 15,686,411,200
      E/(D+E) = 0.9023920;  D/(D+E) = 0.0976080
      WACC = 0.9023920 x 0.10 + 0.0976080 x 0.0516158 = 0.0902392 + 0.0050381 = 0.0952773
    Each row names its value and its source: the planted series and date for the
    two market-wide inputs, the record ids for the shares and the debt, the
    formula for the cost of debt (no fallback: interest expense is on record).
    """
    table = cien_at_100["wacc_components"]
    rows = {row["input"]: row for row in table["rows"]}
    assert list(rows) == ["risk_free_rate", "equity_risk_premium", "beta", "cost_of_equity",
                          "pre_tax_cost_of_debt", "tax_rate", "market_value_of_equity",
                          "total_debt", "weight_of_equity", "weight_of_debt", "wacc"]
    assert rows["risk_free_rate"]["value"] == 0.04
    assert rows["risk_free_rate"]["source"] == "DGS10 on 2026-06-04; planted by the test"
    assert rows["equity_risk_premium"]["value"] == 0.05
    assert rows["equity_risk_premium"]["source"] == (
        "the month starting 2026-06-01; planted by the test")
    assert rows["beta"]["value"] == 1.2
    assert rows["cost_of_equity"]["value"] == pytest.approx(0.10)
    assert rows["pre_tax_cost_of_debt"]["value"] == pytest.approx(86_964 / 1_535_737.5)
    assert rows["pre_tax_cost_of_debt"]["source"].startswith("interest_expense / average debt")
    assert "fallback" not in rows["pre_tax_cost_of_debt"]["source"]
    assert rows["tax_rate"]["value"] == pytest.approx(CIEN_TAX_RATE)
    assert rows["tax_rate"]["source"].startswith("the effective rate, inside the bounds")
    assert rows["market_value_of_equity"]["value"] == pytest.approx(14_155_292_200)
    assert rows["market_value_of_equity"]["source"].endswith(
        "shares_outstanding 0001628280-26-040767:facts:EntityCommonStockSharesOutstanding:2026-05-29")
    assert rows["total_debt"]["value"] == CIEN_TOTAL_DEBT
    assert rows["total_debt"]["source"] == (
        "debt_current + debt_noncurrent; "
        "0001628280-26-040767:facts:LongTermDebtCurrent:2026-05-02, "
        "0001628280-26-040767:facts:LongTermDebtNoncurrent:2026-05-02")
    assert rows["weight_of_equity"]["value"] == pytest.approx(0.9023920, abs=5e-8)
    assert rows["weight_of_debt"]["value"] == pytest.approx(0.0976080, abs=5e-8)
    assert rows["wacc"]["value"] == pytest.approx(0.0952773, abs=5e-8)
    assert rows["wacc"]["value"] == pytest.approx(
        14_155_292_200 / 15_686_411_200 * 0.10
        + 1_531_119_000 / 15_686_411_200 * CIEN_COST_OF_DEBT_AFTER_TAX)
    assert table["formula"] == cien_at_100["cost_of_capital"]["wacc"]["formula"]
    assert all("source" in row and "missing" not in row for row in table["rows"])


# --- the implied growth, anchored to prices worked from the quoted facts -----------------------
#
# The reverse DCF holds the base scenario's margins, reinvestment and terminal
# growth and finds the constant growth g for years one to ten at which the base
# case a share equals the price. The base scenario here is the Gordon case of the
# DCF tests above (margin 20%, reinvestment 40%, terminal growth 3%), so year t's
# free cash flow to the firm is R x (1+g)^t x 0.20 x (1 - tax) x 0.60, and with
#     F1 = R x (1+g) x 0.20 x (1 - tax) x 0.60      (next year's cash flow)
#     q  = (1+g) / (1+W)                              (one year's growth over one year's discount)
# the ten explicit years, end-of-year discounted, are the geometric series
#     F1/(1+W) + F1 (1+g)/(1+W)^2 + ... + F1 (1+g)^9/(1+W)^10 = F1/(1+W) x (1 - q^10)/(1 - q)
# and the terminal value, year ten's cash flow grown once at 3% over (W - 0.03),
# discounted ten years, is
#     F1 (1+g)^9 x 1.03 / (W - 0.03) / (1+W)^10.
# When g is the terminal rate the two collapse to F1 / (W - g) exactly: 1 - q is
# (W - g)/(1+W), so the series is F1 (1 - q^10)/(W - g), and (1+g)^10/(1+W)^10 is
# q^10, so the terminal is F1 q^10/(W - g); together F1/(W - g), the Gordon value.
# A share: (enterprise value - N) / S, with N = net debt + leases = 328,285,000 +
# 44,392,000 = 372,677,000 and S = 146,314,000 diluted shares.
#
# The helpers below are that arithmetic in plain Python on the quoted facts, and
# import nothing from src/: a reader reruns them by hand and gets the constants
# the assertions use, at the precision the assertions use.
CIEN_REVENUE = 5_569_150 * 1000
CIEN_NET_DEBT_AND_LEASES = (328_285 + 44_392) * 1000
GORDON_TERMINAL_GROWTH = GORDON["terminal_growth"]


def _hand_wacc(price: float) -> float:
    """E/(D+E) x 0.10 + D/(D+E) x the after-tax cost of debt, E = price x shares outstanding."""
    equity = price * CIEN_SHARES_OUTSTANDING
    return (equity / (equity + CIEN_TOTAL_DEBT) * 0.10
            + CIEN_TOTAL_DEBT / (equity + CIEN_TOTAL_DEBT) * CIEN_COST_OF_DEBT_AFTER_TAX)


def _hand_enterprise_value(growth: float, wacc: float) -> float:
    """The geometric series and the terminal value written above."""
    next_year = CIEN_REVENUE * (1 + growth) * 0.20 * (1 - CIEN_TAX_RATE) * 0.60
    q = (1 + growth) / (1 + wacc)
    explicit = next_year / (1 + wacc) * (1 - q ** 10) / (1 - q)
    terminal = (next_year * (1 + growth) ** 9 * (1 + GORDON_TERMINAL_GROWTH)
                / (wacc - GORDON_TERMINAL_GROWTH) / (1 + wacc) ** 10)
    return explicit + terminal


def _hand_price(growth: float, wacc: float) -> float:
    return (_hand_enterprise_value(growth, wacc) - CIEN_NET_DEBT_AND_LEASES) / CIEN_DILUTED_SHARES


# Through the whole file the WACC moves with the price, because E is the price
# times the shares outstanding, so the price at which the base case is worth the
# price itself -- where the growth the price implies is the base case's 3% -- is
# a fixed point. At g = 0.03 the value is the Gordon form, so with
#     A = F1 at g = 0.03,  a = n x (0.10 - 0.03),  b = D x (after-tax cost of debt - 0.03)
# (n = shares outstanding, D = total debt) the condition (A / (W(P) - 0.03) - N) / S = P
# multiplies out to
#     (a P + b) (S P + N) = A (D + n P),  that is  a S P^2 + (a N + b S - A n) P + (b N - A D) = 0,
# a quadratic in P whose positive root is the price. The coefficients are written
# as the expressions, not as rounded figures; rounded, a = 9,908,704.54,
# b = 33,096,343.75, a S = 1.44978 x 10^15, a N + b S - A n = -8.02798 x 10^16,
# b N - A D = -9.48341 x 10^17, and the root is 65.3788514.
CIEN_GORDON_NEXT_YEAR_CASH = (CIEN_REVENUE * (1 + GORDON_TERMINAL_GROWTH) * 0.20
                              * (1 - CIEN_TAX_RATE) * 0.60)
_a = CIEN_SHARES_OUTSTANDING * (0.10 - GORDON_TERMINAL_GROWTH)
_b = CIEN_TOTAL_DEBT * (CIEN_COST_OF_DEBT_AFTER_TAX - GORDON_TERMINAL_GROWTH)
_quadratic = (_a * CIEN_DILUTED_SHARES,
              _a * CIEN_NET_DEBT_AND_LEASES + _b * CIEN_DILUTED_SHARES
              - CIEN_GORDON_NEXT_YEAR_CASH * CIEN_SHARES_OUTSTANDING,
              _b * CIEN_NET_DEBT_AND_LEASES - CIEN_GORDON_NEXT_YEAR_CASH * CIEN_TOTAL_DEBT)
CIEN_PRICE_AT_ITS_GORDON_VALUE = (
    (-_quadratic[1] + math.sqrt(_quadratic[1] ** 2 - 4 * _quadratic[0] * _quadratic[2]))
    / (2 * _quadratic[0]))


def test_the_hand_price_for_the_growth_beside_history_is_the_fixed_point_it_claims_to_be():
    """The lines above, rerun: the root is 65.3788514, and at that price the hand
    WACC is 0.0931315 and the hand Gordon value a share is the price again --
    the written arithmetic produces the constant to the precision asserted below."""
    price = CIEN_PRICE_AT_ITS_GORDON_VALUE
    assert price == pytest.approx(65.3788514, abs=5e-8)
    assert _hand_wacc(price) == pytest.approx(0.0931315, abs=5e-8)
    assert (CIEN_GORDON_NEXT_YEAR_CASH / (_hand_wacc(price) - GORDON_TERMINAL_GROWTH)
            - CIEN_NET_DEBT_AND_LEASES) / CIEN_DILUTED_SHARES == pytest.approx(price, abs=1e-9)
    assert _hand_price(GORDON_TERMINAL_GROWTH, _hand_wacc(price)) == pytest.approx(price, abs=1e-9)


@pytest.fixture(scope="module")
def cien_at_its_gordon_value():
    return _cien(CIEN_PRICE_AT_ITS_GORDON_VALUE, {"scenarios": {"base": dict(GORDON)}})


def test_cienas_growth_beside_history_is_the_three_and_five_year_compound_and_the_implied_rate(
        cien_at_its_gordon_value):
    """Revenues, the fiscal years on record:
      2024-11-03..2025-11-01  4,769,507  (the 10-K filed 2025-12-12)
      2021-10-31..2022-10-29  3,632,661  (the same value in the 10-Ks filed 2022-12-16,
                                          2023-12-15 and 2024-12-20)
      2019-11-03..2020-10-31  3,532,157  (the same value in the 10-Ks filed 2020-12-18,
                                          2021-12-17 and 2022-12-16)
      three-year compound  (4,769,507 / 3,632,661) ** (1/3) - 1 = 1.3129513 ** (1/3) - 1 = 0.0950053
      five-year compound   (4,769,507 / 3,532,157) ** (1/5) - 1 = 1.3503100 ** (1/5) - 1 = 0.0619075
    and beside them the implied ten-year growth at the fixed-point price worked
    above, 0.03, found by a bisection that stops at 1e-10.
    """
    out = cien_at_its_gordon_value["implied_growth_beside_history"]
    three = out["revenue_growth_three_year_compound"]
    five = out["revenue_growth_five_year_compound"]
    assert three["value"] == pytest.approx((4_769_507 / 3_632_661) ** (1 / 3) - 1)
    assert three["value"] == pytest.approx(0.0950053, abs=5e-8)
    assert three["fiscal_years"] == "2021-10-31..2022-10-29 to 2024-11-03..2025-11-01"
    assert three["inputs"]["revenue_3_years_earlier"]["value"] == 3_632_661 * 1000
    assert five["value"] == pytest.approx((4_769_507 / 3_532_157) ** (1 / 5) - 1)
    assert five["value"] == pytest.approx(0.0619075, abs=5e-8)
    assert five["fiscal_years"] == "2019-11-03..2020-10-31 to 2024-11-03..2025-11-01"
    assert five["inputs"]["revenue_5_years_earlier"]["value"] == 3_532_157 * 1000
    implied = out["implied_ten_year_revenue_growth"]
    assert implied["value"] == pytest.approx(GORDON_TERMINAL_GROWTH, abs=1e-8)
    assert implied["price"] == CIEN_PRICE_AT_ITS_GORDON_VALUE
    base = cien_at_its_gordon_value["valuation"]["scenarios"]["base"]
    assert base["value_per_share"] == pytest.approx(CIEN_PRICE_AT_ITS_GORDON_VALUE, abs=1e-6)
    assert cien_at_its_gordon_value["cost_of_capital"]["value"] == pytest.approx(
        _hand_wacc(CIEN_PRICE_AT_ITS_GORDON_VALUE), abs=1e-12)
    # The flat keys the owner's coverage grader reads carry the same two rates.
    history = cien_at_its_gordon_value["earnings_versus_cash"]["history"]
    assert history["revenue_growth_three_year_compound"] == three["value"]
    assert history["revenue_growth_five_year_compound"] == five["value"]


def test_the_reverse_dcf_finds_the_growth_beside_history_at_two_hand_prices():
    """The reverse DCF on Ciena's quoted figures, at the hand WACC for a price of 100
    (0.0952773, worked in the WACC test above) so that nothing couples the price
    to the discount rate, against two prices worked by the formulas above:
      g = 0.03:  F1 = 5,569,150,000 x 1.03 x 0.20 x (1 - 0.0884929) x 0.60 = 627,433,105.82
                 F1 / (0.0952773 - 0.03) = 9,611,809,406; less N = 9,239,132,406;
                 over S = 63.1459218 a share
      g = 0.02:  F1 = 5,569,150,000 x 1.02 x 0.20 x (1 - 0.0884929) x 0.60 = 621,341,522.27
                 q = 1.02 / 1.0952773 = 0.9312710
                 series   F1 / 1.0952773 x (1 - q^10) / (1 - q)                = 4,204,294,961
                 terminal F1 x 1.02^9 x 1.03 / (0.0952773 - 0.03) / 1.0952773^10 = 4,715,914,709
                 together 8,920,209,671; less N = 8,547,532,671; over S = 58.4191032 a share
    At each price the growth found is the one the price was worked at, within the
    bisection's own stop of 1e-10; neither expected growth is read off a run.
    """
    wacc = _hand_wacc(100.0)
    assert wacc == pytest.approx(0.0952773, abs=5e-8)
    for growth, written in ((0.03, 63.1459218), (0.02, 58.4191032)):
        price = _hand_price(growth, wacc)
        assert price == pytest.approx(written, abs=5e-8)
        out = calculator.reverse_dcf(CIEN_REVENUE, GORDON, CIEN_TAX_RATE, wacc,
                                     328_285 * 1000, 44_392 * 1000, CIEN_DILUTED_SHARES, price)
        assert out["value"] == pytest.approx(growth, abs=1e-8), growth
    # The Gordon form and the series agree where the growth is the terminal rate.
    assert _hand_enterprise_value(0.03, wacc) == pytest.approx(
        CIEN_GORDON_NEXT_YEAR_CASH / (wacc - 0.03), rel=1e-12)


def _history(ends: list[str], revenues: list[float]) -> list[dict]:
    """History rows, newest first, one per fiscal-year end, each a year long."""
    return [{"fiscal_year": f"{(dt.date.fromisoformat(end) - dt.timedelta(days=364)).isoformat()}..{end}",
             "revenue": revenue, "revenue_id": None}
            for end, revenue in zip(ends, revenues)]


def test_growth_beside_history_with_fewer_fiscal_years_is_absent_with_the_count():
    """Four consecutive years ending each 31 October, 400, 300, 200, 100 newest first:
    three-year compound (400/100)**(1/3) - 1; five-year needs six years and says it
    has four; a revenue that is not a number is named."""
    rows = _history(["2025-10-31", "2024-10-31", "2023-10-31", "2022-10-31"],
                    [400.0, 300.0, 200.0, 100.0])
    assert calculator.compound_revenue_growth(rows, 3)["value"] == pytest.approx(4 ** (1 / 3) - 1)
    five = calculator.compound_revenue_growth(rows, 5)
    assert five["missing"] == "4 fiscal years on record, and 5-year compound growth needs 6"
    rows[3]["revenue"] = None
    assert "not a positive number" in calculator.compound_revenue_growth(rows, 3)["missing"]


def test_growth_beside_history_over_a_gap_in_the_fiscal_years_is_absent_with_the_gap_named():
    """Two-sided, after the second lens's second reading. Six fiscal years ending
    each 31 October with 2021 absent -- 2025, 2024, 2023, 2022, 2020, 2019 -- and
    revenue 320, 300, 280, 260, 220, 200 newest first:
      the four newest are consecutive (365, 366, 365 days apart), so the three-year
      rate is (320 / 260) ** (1/3) - 1 = 1.230769 ** (1/3) - 1 = 0.0717;
      the six span 2025-10-31 less 2019-10-31 = 2,192 days (six years, two of them
      leap years), not five fiscal years, because 2022-10-31 less 2020-10-31 is
      730 days (no leap day between them), so the five-year rate is
      absent and the sentence names that step -- (320 / 200) ** (1/5) - 1 under the
      exponent 1/5 would have been a six-year rate called a five-year one.
    With 2021 on record (revenue 240) the five-year rate is (320 / 200) ** (1/5) - 1 = 0.0986."""
    with_gap = _history(["2025-10-31", "2024-10-31", "2023-10-31", "2022-10-31", "2020-10-31",
                         "2019-10-31"], [320.0, 300.0, 280.0, 260.0, 220.0, 200.0])
    three = calculator.compound_revenue_growth(with_gap, 3)
    assert three["value"] == pytest.approx((320 / 260) ** (1 / 3) - 1)
    assert three["value"] == pytest.approx(0.0717, abs=5e-5)
    five = calculator.compound_revenue_growth(with_gap, 5)
    assert "value" not in five
    assert five["missing"] == (
        "the 6 newest fiscal years on record span 2192 days, not 5 fiscal years of 350 to "
        "380 days each: 730 days from the fiscal year ending 2020-10-31 to the one ending "
        "2022-10-31, so a fiscal year between them is absent from the record")
    assert calculator.fiscal_year_gap(with_gap[:4]) is None
    consecutive = _history(["2025-10-31", "2024-10-31", "2023-10-31", "2022-10-31", "2021-10-31",
                            "2020-10-31"], [320.0, 300.0, 280.0, 260.0, 240.0, 200.0])
    assert calculator.compound_revenue_growth(consecutive, 5)["value"] == pytest.approx(
        (320 / 200) ** (1 / 5) - 1)
    assert calculator.compound_revenue_growth(consecutive, 5)["value"] == pytest.approx(
        0.0986, abs=5e-5)
    # The same gap under the three-year key, whose rows[3] read predates this item;
    # 2022-10-31 to 2024-10-31 is 731 days, with 2024's leap day between them.
    gap_in_three = _history(["2025-10-31", "2024-10-31", "2022-10-31", "2021-10-31"],
                            [320.0, 300.0, 260.0, 240.0])
    assert "731 days from the fiscal year ending 2022-10-31 to the one ending 2024-10-31" in \
        calculator.compound_revenue_growth(gap_in_three, 3)["missing"]


def test_the_history_the_grader_reads_carries_no_rate_across_a_growth_beside_history_gap():
    """Through annual_history, on a planted record of 10-K revenues for the fiscal
    years ending each 31 October 2019 to 2025 with 2021 absent: the flat three-year
    key is (320 / 260) ** (1/3) - 1 and the flat five-year key is not written at all,
    rather than a six-year rate under its name."""
    ends = ["2019-10-31", "2020-10-31", "2022-10-31", "2023-10-31", "2024-10-31", "2025-10-31"]
    revenues = [200.0, 220.0, 260.0, 280.0, 300.0, 320.0]
    record = calculator.Record(_rows(Revenues=[
        {"start": (dt.date.fromisoformat(end) - dt.timedelta(days=364)).isoformat(),
         "end": end, "val": revenue} for end, revenue in zip(ends, revenues)]))
    spans = calculator.durations(record.usd)
    periods = {"fiscal_years": calculator.fiscal_years(spans, dt.date(2025, 10, 31))}
    assert [span[1] for span in periods["fiscal_years"]] == list(reversed(ends))
    history = calculator.annual_history(record, periods)
    assert history["revenue_growth_three_year_compound"] == pytest.approx((320 / 260) ** (1 / 3) - 1)
    assert "revenue_growth_five_year_compound" not in history
    beside = calculator.implied_growth_beside_history({"missing": "no assumptions"}, history)
    assert ("730 days from the fiscal year ending 2020-10-31 to the one ending 2022-10-31"
            in beside["revenue_growth_five_year_compound"]["missing"])


def test_free_cash_flow_yield_and_wacc_components_without_a_price_are_absent_with_the_reason(nvda):
    """NVIDIA's run has no price series: the yields, the enterprise value and every
    WACC row that needs a price say so, and the rows that do not (the two
    market-wide inputs, the cost of debt, the tax rate, the debt) carry their value."""
    yields = nvda["free_cash_flow_yield"]
    for name in ("price_at_cutoff", "enterprise_value",
                 "free_cash_flow_to_firm_over_enterprise_value",
                 "free_cash_flow_to_equity_over_market_value_of_equity"):
        assert "value" not in yields[name] and "Tiingo" in yields[name]["missing"], name
    rows = {row["input"]: row for row in nvda["wacc_components"]["rows"]}
    for name in ("beta", "cost_of_equity", "market_value_of_equity", "weight_of_equity",
                 "weight_of_debt", "wacc"):
        assert rows[name]["value"] is None and "Tiingo" in rows[name]["missing"], name
    for name in ("risk_free_rate", "equity_risk_premium", "pre_tax_cost_of_debt",
                 "tax_rate", "total_debt"):
        assert rows[name]["value"] is not None and "missing" not in rows[name], name
    assert rows["risk_free_rate"]["source"].startswith("DGS10 on 2026-08-26; ")
    implied = nvda["implied_growth_beside_history"]["implied_ten_year_revenue_growth"]
    assert "value" not in implied and implied["missing"].startswith("no reverse DCF: ")


def test_wacc_components_carry_the_cost_of_debt_fallback_label():
    """With neither interest expense nor interest paid on record the cost-of-debt
    row's source is the ladder's own label, verbatim, and not a formula; the WACC
    is the textbook case's 0.09395."""
    capital = _wacc_with({"interest_expense": {"missing": "no row"},
                          "interest_paid": {"missing": "no row"}})
    rows = {row["input"]: row for row in
            calculator.wacc_components(capital, {"debt_now": {"value": 100.0}})["rows"]}
    assert rows["pre_tax_cost_of_debt"]["value"] == pytest.approx(0.05)
    assert rows["pre_tax_cost_of_debt"]["source"] == (
        "fallback: " + capital["pre_tax_cost_of_debt"]["fallback"])
    assert rows["wacc"]["value"] == pytest.approx(0.09395)


def test_the_free_cash_flow_yield_and_wacc_components_never_reach_the_filings_only_view(cien_at_100):
    """All three blocks read the price, so the accounting and financial analysts never see them."""
    view = calculator.filings_only(cien_at_100)
    for name in ("free_cash_flow_yield", "wacc_components", "implied_growth_beside_history"):
        assert name not in view
        assert name in view["sections_removed_for_this_view"]
        assert name in calculator.PRICED_SECTIONS
