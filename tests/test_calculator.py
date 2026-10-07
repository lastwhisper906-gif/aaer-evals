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
