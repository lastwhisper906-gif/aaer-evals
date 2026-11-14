"""`src/calculator_drift.py`: which published calculator figures today's calculator prints
differently, in `calculator_filings_only.json` and in `calculator.json`, listed by run,
file and path, and each attributed.

A run under `runs/` stands as published; the list is for the owner to read
(`docs/needs_judgment.md`, Settled by default). Three lists, each a recomputation of
every committed run from its own bundle, market data and analysts' files:

- the baseline, with this change's two rules off: what the calculator already printed
  differently before it (two runs written before the cost of debt had a fallback);
- with the cost of debt's last-fiscal-year rung on: the runs whose published cost of
  debt was "the risk-free rate plus one point, because neither interest expense nor
  interest paid is on record" while interest paid was on record for the fiscal year;
- with the scope rule on as well: Johnson Controls' operating cash flow and Dell's
  interest expense.

Every expected value is worked below from rows read through
`tests/companyfacts_source.py`, or from the run's own bundle where the store's
companyfacts predates the triggering 10-Q; none is read from the tool's output.
"""

from __future__ import annotations

import json
import math

import pytest

from src import calculator, calculator_drift as drift
from tests import companyfacts_source as source

MILLION = 1_000_000
FILINGS_ONLY, FINAL = calculator.FILINGS_ONLY, "calculator.json"
JCI = "JCI/0000833444-26-000087"
DELL = "DELL/0001571996-26-000046"
CARR = "CARR/0001783180-26-000032"
CARR_RERUN = "CARR/0001783180-26-000032-rerun-2026-10-28"
AAPL = "AAPL/0000320193-26-000020"
CUTOFFS = {JCI: "2026-07-29", DELL: "2026-09-08", CARR: "2026-07-28", CARR_RERUN: "2026-07-28"}

NET_INCOME = "NetIncomeLoss"
CONTINUING = "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations"
TOTAL = "NetCashProvidedByUsedInOperatingActivities"


def keyed(rows: list[dict]) -> dict:
    return {(row["run"], row["file"], row["path"]): (row["old"], row["new"]) for row in rows}


@pytest.fixture(scope="module")
def listed() -> dict:
    rows = drift.report()
    assert (calculator.SCOPE_RULE, calculator.LAST_FISCAL_YEAR_RUNG) == (True, True)
    return keyed(rows)


@pytest.fixture(scope="module")
def without_the_scope_rule() -> dict:
    return keyed(drift.report(scope_rule=False))


@pytest.fixture(scope="module")
def baseline() -> dict:
    rows = drift.report(scope_rule=False, last_fiscal_year_rung=False)
    assert (calculator.SCOPE_RULE, calculator.LAST_FISCAL_YEAR_RUNG) == (True, True)
    return keyed(rows)


def source_row(run: str, tag: str, period: str) -> float:
    """One row of a run's company, in millions: companyfacts through the independent
    reader, or, where the store's companyfacts predates the triggering 10-Q, the run's
    own `input_numbers.json`, read here. `period` is a date or `start..end`."""
    ticker, cutoff = run.split("/")[0], CUTOFFS[run]
    standing = source.reported(ticker, tag, period, cutoff)
    if standing:
        values = {row["val"] for row in standing}
    else:
        start, _, end = period.rpartition("..")
        facts = json.loads((drift.RUNS / run / "input_numbers.json").read_text(encoding="utf-8"))

        def at(context: dict) -> bool:
            return (context.get("start") == start and context.get("end") == end) if start \
                else context.get("instant") == end
        values = {fact["number"] for fact in facts["facts"]
                  if fact["tag"] == tag and not fact.get("nil") and not fact.get("superseded_by")
                  and not (fact.get("context") or {}).get("segment")
                  and at(fact.get("context") or {}) and fact.get("filing_date", "9999") <= cutoff}
    assert len(values) == 1, (run, tag, period, values)
    return values.pop() / MILLION


def spread(values: list) -> float:
    """The population standard deviation, in plain arithmetic."""
    mean = sum(values) / len(values)
    return math.sqrt(sum((value - mean) ** 2 for value in values) / len(values))


def close(old, new) -> tuple:
    return (None if old is None else pytest.approx(old, rel=1e-9),
            None if new is None else pytest.approx(new, rel=1e-9))


def test_it_runs_on_every_committed_run_and_reruns_are_among_them():
    runs = drift.committed_runs()
    assert len(runs) == len(list(drift.RUNS.glob("*/*/input_manifest.json"))) >= 12
    assert any("rerun" in run.name for run in runs)
    named = drift.trigger(drift.RUNS / "JCI" / "0000833444-26-000087")
    assert named == {"ticker": "JCI", "cutoff": "2026-07-29", "period_end": "2026-06-30",
                     "form": "10-Q", "accession": "0000833444-26-000087"}


# --- the baseline: what the calculator already printed differently before this change --------

def test_the_baseline_is_two_runs_written_before_the_cost_of_debt_had_a_fallback(baseline):
    """With the scope rule and the last-fiscal-year rung both off, every published
    number of every run is reproduced, in both files. What is left are nine cells
    two early runs published as missing and the calculator has since found: Apple's
    cost of debt (its published cell is the missing interest expense, with no
    fallback) and what reads it, and the fallback beside Carrier's first run's
    cost of debt, which its valuation analyst chose. None is this change's; an
    unrelated drift would show here."""
    assert {run for run, _, _ in baseline} == {AAPL, CARR}
    assert all(file == FINAL and old is None for (_, file, _), (old, _) in baseline.items())
    assert {path for run, _, path in baseline if run == AAPL} == {
        "cost_of_capital.pre_tax_cost_of_debt.value", "cost_of_capital.value",
        "cost_of_capital.wacc.value", "valuation.base_revenue", "valuation.price_at_cutoff",
        "valuation.risk_free_rate_cap_on_terminal_growth", "valuation.tax_rate", "valuation.wacc"}
    assert {path for run, _, path in baseline if run == CARR} == {
        "cost_of_capital.pre_tax_cost_of_debt.computed.value"}
    published = json.loads((drift.RUNS / AAPL / FINAL).read_text(encoding="utf-8"))
    assert "fallback" not in published["cost_of_capital"]["pre_tax_cost_of_debt"]
    assert published["cost_of_capital"]["pre_tax_cost_of_debt"]["missing"].startswith(
        "interest_expense:")


# --- the last-fiscal-year rung of the cost of debt ---------------------------------------------

def average_debt(run: str, now: list, a_year_earlier: list) -> float:
    """The average of total debt now and a year earlier, each the sum of its lines."""
    return (sum(source_row(run, tag, date) for tag, date in now)
            + sum(source_row(run, tag, date) for tag, date in a_year_earlier)) / 2


def test_the_rung_moves_the_runs_published_as_neither_on_record(without_the_scope_rule, baseline):
    """Johnson Controls and Carrier (its rerun, and the fallback beside its first run's
    chosen figure) were published at the risk-free rate plus one point, "because
    neither interest expense nor interest paid is on record", while each 10-K states
    interest paid for the fiscal year. In millions:

      Johnson Controls   321 paid in fiscal 2025; debt 311 + 865 + 8,299 = 9,475 at
                         2026-06-30 and 570 + 1,277 + 8,446 = 10,293 a year earlier;
                         321 / 9,884 = 0.032477, where 0.0567 was published
      Carrier            422 paid in 2025; debt 1,638 + 10,314 = 11,952 at 2026-06-30
                         and 107 + 11,336 = 11,443 a year earlier; 422 / 11,697.5 =
                         0.036076, where 0.0561 was published (its 10-Q's own words,
                         which the valuation analyst quoted: "an approximate
                         weighted-average interest rate of 3.65%")
    """
    jci_debt = average_debt(
        JCI, [("LongTermDebtAndCapitalLeaseObligationsCurrent", "2026-06-30"),
              ("ShortTermBorrowings", "2026-06-30"),
              ("LongTermDebtAndCapitalLeaseObligations", "2026-06-30")],
        [("LongTermDebtAndCapitalLeaseObligationsCurrent", "2025-06-30"),
         ("ShortTermBorrowings", "2025-06-30"),
         ("LongTermDebtAndCapitalLeaseObligations", "2025-06-30")])
    assert jci_debt == (9_475 + 10_293) / 2 == 9_884
    jci_paid = source_row(JCI, "InterestPaidNet", "2024-10-01..2025-09-30")
    assert jci_paid == 321
    carrier_debt = average_debt(
        CARR, [("DebtCurrent", "2026-06-30"), ("LongTermDebtAndCapitalLeaseObligations", "2026-06-30")],
        [("LongTermDebtCurrent", "2025-06-30"), ("LongTermDebtAndCapitalLeaseObligations", "2025-06-30")])
    assert carrier_debt == (11_952 + 11_443) / 2 == 11_697.5
    carrier_paid = source_row(CARR, "InterestPaidNet", "2025-01-01..2025-12-31")
    assert carrier_paid == 422
    assert jci_paid / jci_debt == pytest.approx(0.032477, abs=5e-7)
    assert carrier_paid / carrier_debt == pytest.approx(0.036076, abs=5e-7)

    moved = {key: value for key, value in without_the_scope_rule.items()
             if baseline.get(key) != value}
    cell = "cost_of_capital.pre_tax_cost_of_debt"

    def rung(run: str, published: float, worked: float) -> dict:
        return {(run, FINAL, f"{cell}.value"): close(published, worked),
                (run, FINAL, "wacc_components.rows.4.value"): close(published, worked),
                (run, FINAL, f"{cell}.parts.risk_free_rate.value"): close(published - 0.01, None),
                (run, FINAL, f"{cell}.parts.spread.value"): close(0.01, None)}
    assert moved == {
        **rung(JCI, 0.0567, jci_paid / jci_debt),
        **rung(CARR_RERUN, 0.0561, carrier_paid / carrier_debt),
        (CARR, FINAL, f"{cell}.computed.value"): close(None, carrier_paid / carrier_debt),
    }
    for run, rate in ((JCI, 0.0567), (CARR_RERUN, 0.0561)):
        published = json.loads((drift.RUNS / run / FINAL).read_text(encoding="utf-8"))
        assert published["cost_of_capital"]["pre_tax_cost_of_debt"]["value"] == pytest.approx(rate)
        assert "neither interest expense nor interest paid is on record" in \
            published["cost_of_capital"]["pre_tax_cost_of_debt"]["fallback"]


# --- the scope rule ------------------------------------------------------------------------------

def scope_rows(listed: dict, without_the_scope_rule: dict, run: str) -> dict:
    return {(file, path): value for (name, file, path), value in listed.items()
            if name == run and without_the_scope_rule.get((name, file, path)) != value}


def test_only_johnson_controls_and_dell_move_under_the_scope_rule(listed, without_the_scope_rule):
    """Arista's and Fortinet's capital expenditure, Fortinet's interest expense and
    Western Digital's depreciation and dividends each cross two tags of one
    same-concept group and stand as published."""
    moved = {run for (run, file, path), value in listed.items()
             if without_the_scope_rule.get((run, file, path)) != value}
    assert moved == {JCI, DELL}
    assert {run for run, _, _ in listed} == {AAPL, CARR, CARR_RERUN, DELL, JCI}


def test_johnson_controls_moves_as_worked_by_hand(listed, without_the_scope_rule):
    """The eight leaves of Johnson Controls' run the scope rule moves, the same in both
    files, each worked from the source rows, in millions.

    Operating cash flow a year earlier: 1,568 (fiscal 2024) + 1,586 (nine months to
    2025-06-30) - 216 (nine months to 2024-06-30), all continuing operations, 2,938;
    the published run subtracted the total 572 instead, 2,582. This year: 2,554
    (fiscal 2025) + 2,572 (nine months to 2026-06-30) - 1,586 = 3,540, so growth is
    (3,540 - 2,938) / 2,938 where it was (3,540 - 2,582) / 2,582.

    Smoothness reads nine quarters, newest first. Net income: 749, 613, 524, 3,291 -
    1,598 = 1,693, 701, 478, 419, 1,705 - 1,072 = 633, 975. Operating cash flow:
    2,572 - 1,283 = 1,289, 1,283 - 611 = 672, 611, 2,554 - 1,586 = 968, 1,586 - 799 =
    787, 799 - 249 = 550, 249, then the fourth quarter of fiscal 2024 -- 1,568 - 216 =
    1,352 within continuing operations, where the published run took 1,568 - 572 =
    996 across the total -- and the quarter to June 2024 in the same scope, 216 -
    (-437) = 653, where the published run took 572 - (-449) = 1,021 under the total.
    The value is the population standard deviation of the eight quarter-to-quarter
    changes in net income over the same for operating cash flow: 1.44369 as
    published, 1.05002 with the series in one scope.
    """
    def row(tag: str, period: str) -> float:
        return source_row(JCI, tag, period)
    year_earlier = (row(CONTINUING, "2023-10-01..2024-09-30") + row(CONTINUING, "2024-10-01..2025-06-30")
                    - row(CONTINUING, "2023-10-01..2024-06-30"))
    published_year_earlier = (row(CONTINUING, "2023-10-01..2024-09-30")
                              + row(CONTINUING, "2024-10-01..2025-06-30")
                              - row(TOTAL, "2023-10-01..2024-06-30"))
    this_year = (row(CONTINUING, "2024-10-01..2025-09-30") + row(CONTINUING, "2025-10-01..2026-06-30")
                 - row(CONTINUING, "2024-10-01..2025-06-30"))
    assert (year_earlier, published_year_earlier, this_year) == (2_938, 2_582, 3_540)
    assert row(CONTINUING, "2023-10-01..2024-06-30") == 216
    assert row(TOTAL, "2023-10-01..2024-06-30") == 572

    net_income = [
        row(NET_INCOME, "2026-04-01..2026-06-30"),
        row(NET_INCOME, "2026-01-01..2026-03-31"),
        row(NET_INCOME, "2025-10-01..2025-12-31"),
        row(NET_INCOME, "2024-10-01..2025-09-30") - row(NET_INCOME, "2024-10-01..2025-06-30"),
        row(NET_INCOME, "2025-04-01..2025-06-30"),
        row(NET_INCOME, "2025-01-01..2025-03-31"),
        row(NET_INCOME, "2024-10-01..2024-12-31"),
        row(NET_INCOME, "2023-10-01..2024-09-30") - row(NET_INCOME, "2023-10-01..2024-06-30"),
        row(NET_INCOME, "2024-04-01..2024-06-30"),
    ]
    assert net_income == [749, 613, 524, 1_693, 701, 478, 419, 633, 975]
    cash_to_fiscal_2025 = [
        row(CONTINUING, "2025-10-01..2026-06-30") - row(CONTINUING, "2025-10-01..2026-03-31"),
        row(CONTINUING, "2025-10-01..2026-03-31") - row(CONTINUING, "2025-10-01..2025-12-31"),
        row(CONTINUING, "2025-10-01..2025-12-31"),
        row(CONTINUING, "2024-10-01..2025-09-30") - row(CONTINUING, "2024-10-01..2025-06-30"),
        row(CONTINUING, "2024-10-01..2025-06-30") - row(CONTINUING, "2024-10-01..2025-03-31"),
        row(CONTINUING, "2024-10-01..2025-03-31") - row(CONTINUING, "2024-10-01..2024-12-31"),
        row(CONTINUING, "2024-10-01..2024-12-31"),
    ]
    assert cash_to_fiscal_2025 == [1_289, 672, 611, 968, 787, 550, 249]
    fourth_quarter = row(CONTINUING, "2023-10-01..2024-09-30") - row(CONTINUING, "2023-10-01..2024-06-30")
    published_fourth = row(CONTINUING, "2023-10-01..2024-09-30") - row(TOTAL, "2023-10-01..2024-06-30")
    oldest = row(CONTINUING, "2023-10-01..2024-06-30") - row(CONTINUING, "2023-10-01..2024-03-31")
    published_oldest = row(TOTAL, "2023-10-01..2024-06-30") - row(TOTAL, "2023-10-01..2024-03-31")
    assert (fourth_quarter, published_fourth, oldest, published_oldest) == (1_352, 996, 653, 1_021)

    def smoothness(cash: list) -> float:
        changes_in_income = [a - b for a, b in zip(net_income, net_income[1:])]
        changes_in_cash = [a - b for a, b in zip(cash, cash[1:])]
        return spread(changes_in_income) / spread(changes_in_cash)
    old_smoothness = smoothness(cash_to_fiscal_2025 + [published_fourth, published_oldest])
    new_smoothness = smoothness(cash_to_fiscal_2025 + [fourth_quarter, oldest])
    assert old_smoothness == pytest.approx(1.44369, abs=5e-6)
    assert new_smoothness == pytest.approx(1.05002, abs=5e-6)
    assert (3_540 - 2_938) / 2_938 == pytest.approx(0.204901, abs=5e-7)
    assert (3_540 - 2_582) / 2_582 == pytest.approx(0.371030, abs=5e-7)

    one_file = {
        "earnings_versus_cash.smoothness.operating_cash_flow.7":
            (published_fourth * MILLION, fourth_quarter * MILLION),
        "earnings_versus_cash.smoothness.operating_cash_flow.8":
            (published_oldest * MILLION, oldest * MILLION),
        "earnings_versus_cash.smoothness.value": close(old_smoothness, new_smoothness),
        "ratios.growth.operating_cash_flow.trailing_four_quarters.inputs.before.parts"
        ".prior_year_to_date.value": (572 * MILLION, 216 * MILLION),
        "ratios.growth.operating_cash_flow.trailing_four_quarters.inputs.before.value":
            (published_year_earlier * MILLION, year_earlier * MILLION),
        "ratios.growth.operating_cash_flow.trailing_four_quarters.value": close(
            (this_year - published_year_earlier) / published_year_earlier,
            (this_year - year_earlier) / year_earlier),
        "terms.trailing_four_quarters_a_year_earlier.operating_cash_flow.parts"
        ".prior_year_to_date.value": (572 * MILLION, 216 * MILLION),
        "terms.trailing_four_quarters_a_year_earlier.operating_cash_flow.value":
            (published_year_earlier * MILLION, year_earlier * MILLION),
    }
    assert scope_rows(listed, without_the_scope_rule, JCI) == {
        (file, path): value for file in (FILINGS_ONLY, FINAL) for path, value in one_file.items()}


def test_dell_moves_as_worked_by_hand(listed, without_the_scope_rule):
    """Dell's published interest expense summed 1,560 (InterestExpenseNonoperating,
    fiscal 2026) + 800 (InterestExpenseDebt, six months to 2026-07-31) - 753
    (InterestExpenseNonoperating, six months to 2025-08-01) = 1,607 across two
    scopes; it is missing now, in both files, with what read it:

      interest coverage   EBIT 8,149 + 9,041 - 2,938 = 14,252 over 1,607 = 8.8687,
                          now missing
      cost of debt        1,607 over average debt (8,481 + 25,985 + 7,154 + 21,535)
                          / 2 = 31,577.5, 0.050891; now interest paid in fiscal
                          2026, 1,354 / 31,577.5 = 0.042879, the ladder's next rung
    """
    def row(tag: str, period: str) -> float:
        return source_row(DELL, tag, period)
    year, to_date, before = "2025-02-01..2026-01-30", "2026-01-31..2026-07-31", "2025-02-01..2025-08-01"
    interest = (row("InterestExpenseNonoperating", year), row("InterestExpenseDebt", to_date),
                row("InterestExpenseNonoperating", before))
    assert interest == (1_560, 800, 753)
    published_interest = interest[0] + interest[1] - interest[2]
    ebit = (row("OperatingIncomeLoss", year), row("OperatingIncomeLoss", to_date),
            row("OperatingIncomeLoss", before))
    assert ebit == (8_149, 9_041, 2_938)
    published_ebit = ebit[0] + ebit[1] - ebit[2]
    assert (published_interest, published_ebit) == (1_607, 14_252)
    debt = (row("DebtCurrent", "2026-07-31") + row("LongTermDebtNoncurrent", "2026-07-31")
            + row("DebtCurrent", "2025-08-01") + row("LongTermDebtNoncurrent", "2025-08-01")) / 2
    assert debt == (8_481 + 25_985 + 7_154 + 21_535) / 2 == 31_577.5
    paid = row("InterestPaidNet", year)
    assert paid == 1_354
    assert published_interest / debt == pytest.approx(0.050891, abs=5e-7)
    assert paid / debt == pytest.approx(0.042879, abs=5e-7)

    def trailing_cell(prefix: str, parts: tuple, total: float) -> dict:
        names = ("prior_fiscal_year", "this_year_to_date", "prior_year_to_date")
        return {f"{prefix}.value": (total * MILLION, None),
                **{f"{prefix}.parts.{name}.value": (part * MILLION, None)
                   for name, part in zip(names, parts)}}
    both_files = {
        **trailing_cell("terms.trailing_four_quarters.interest_expense", interest, published_interest),
        **trailing_cell("ratios.solvency.interest_coverage.inputs.interest_expense", interest,
                        published_interest),
        **trailing_cell("ratios.solvency.interest_coverage.inputs.ebit", ebit, published_ebit),
        "ratios.solvency.interest_coverage.value": close(published_ebit / published_interest, None),
    }
    cost_of_debt = {
        **trailing_cell("cost_of_capital.pre_tax_cost_of_debt.inputs.interest_expense", interest,
                        published_interest),
        "cost_of_capital.pre_tax_cost_of_debt.value": close(published_interest / debt, paid / debt),
        "wacc_components.rows.4.value": close(published_interest / debt, paid / debt),
    }
    assert scope_rows(listed, without_the_scope_rule, DELL) == {
        **{(file, path): value for file in (FILINGS_ONLY, FINAL) for path, value in both_files.items()},
        **{(FINAL, path): value for path, value in cost_of_debt.items()}}
    assert len(scope_rows(listed, without_the_scope_rule, DELL)) == 13 + 13 + 6


# --- the tool's own parts -------------------------------------------------------------------------

def test_changed_leaves_are_numbers_that_moved_or_went_missing_or_were_found():
    old = {"a": {"value": 1.0, "unit": "USD"}, "b": {"missing": "no b"}, "c": {"value": 3.0},
           "list": [1, 2], "section": {"x": {"value": 5.0}}}
    new = {"a": {"value": 2.0, "unit": "USD"}, "b": {"value": 7.0}, "c": {"missing": "gone"},
           "list": [1, 3], "section": {"x": {"value": 5.0}, "added": {"value": 9.0}},
           "new_section": {"y": {"value": 1.0}}}
    assert drift.changed_leaves(old, new) == [
        {"path": "a.value", "old": 1.0, "new": 2.0},
        {"path": "b.value", "old": None, "new": 7.0},
        {"path": "c.value", "old": 3.0, "new": None},
        {"path": "list.1", "old": 2, "new": 3},
    ]
    assert drift.numeric_leaves({"t": True, "n": 1}) == {"n": 1}


def test_the_printed_list_counts_per_run_and_names_file_old_and_new():
    rows = [{"run": "X/1", "file": FINAL, "path": "terms.t.value", "old": 2_582_000_000.0,
             "new": 2_938_000_000.0},
            {"run": "X/1", "file": FILINGS_ONLY, "path": "ratios.r.value", "old": 0.371, "new": None}]
    text = drift.printed(rows)
    assert text.splitlines() == [
        "X/1: 2 changed",
        "  calculator.json terms.t.value: 2,582,000,000 -> 2,938,000,000",
        "  calculator_filings_only.json ratios.r.value: 0.371 -> missing"]
    assert drift.printed([]) == "no published figure changes"
