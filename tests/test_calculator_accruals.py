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
    assert "value" not in found and "no tag carries both" in found["missing"]


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


def named_paths(name: str, opening: str) -> list[str]:
    """Every backticked name in one paragraph of an analyst's definition."""
    text = (AGENTS / name).read_text(encoding="utf-8")
    paragraph = text[text.index(opening):].split("\n\n", 1)[0]
    return re.findall(r"`([^`]+)`", " ".join(paragraph.split()))


@pytest.fixture(scope="module")
def committed_views() -> dict:
    """The filings-only view of every committed run, reruns included (the analysts
    read those too), computed from its own bundle. A rerun's directory name is not
    its accession, so the trigger is the one its own manifest names."""
    views = {}
    for manifest in sorted(RUNS.glob("*/*/input_manifest.json")):
        run = manifest.parent
        stated = json.loads(manifest.read_text(encoding="utf-8"))
        accession = stated["accession"]
        trigger, = {(d["form"], d["report_date"]) for d in stated["documents"]
                    if d.get("accession") == accession}
        views[f"{run.parent.name}/{run.name}"] = calculator.filings_only(calculator.calculate(
            ticker=run.parent.name, cutoff=stated["cutoff"], period_end=trigger[1],
            form=trigger[0], accession=accession, bundle=run))
    return views


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
    assert "value" not in cash and "no tag carries all three" in cash["missing"]
    section = calculator.quarterly_cash_flow_and_accruals(record, terms, periods)
    assert section["cash_flow_accruals"]["value"] is None
    assert "no tag carries all three" in section["cash_flow_accruals"]["missing"]


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
    assert "value" not in revenue and "no tag carries all three" in revenue["missing"]
    receivables = calculator.receivables_extension(record, terms, periods, [])
    gap = receivables["receivables_growth_minus_revenue_growth"]
    assert gap["value"] is None
    assert gap["missing"].startswith("revenue_growth:")
    assert "no tag carries all three" in gap["missing"]
    index = receivables["days_sales_outstanding_index"]
    assert index["value"] is None and "no tag carries all three" in index["missing"]
