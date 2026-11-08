"""`src/calculator_drift.py`: which published calculator figures today's calculator prints
differently, listed by run and path, and shown to be the scope rule's alone.

A run under `runs/` stands as published; the list is for the owner to read
(`docs/needs_judgment.md`, Settled by default). Expected values: Johnson Controls'
operating cash flow over the four quarters to 2025-06-30 through
`tests/companyfacts_source.py` and the run's own bundle, worked by hand below
(1,568 + 1,586 - 216 = 2,938 million under the continuing-operations tag; the
published run summed 1,568 + 1,586 - 572 = 2,582 across two tags), its fourth
quarter of fiscal 2024 (1,568 - 216 = 1,352; published 1,568 - 572 = 996), the
quarter to June 2024 in the same scope (216 - (-437) = 653; published 572 - (-449) =
1,021 under the total), and the nine quarters its smoothness and growth read. Dell's
interest expense is the other moved term: two scopes, missing with the reason.
"""

from __future__ import annotations

import json
import math

import pytest

from src import calculator, calculator_drift as drift
from tests import companyfacts_source as source

MILLION = 1_000_000
JCI = "JCI/0000833444-26-000087"


@pytest.fixture(scope="module")
def listed() -> list[dict]:
    rows = drift.report()
    assert calculator.SCOPE_RULE is True
    return rows


@pytest.fixture(scope="module")
def control() -> list[dict]:
    rows = drift.report(scope_rule=False)
    assert calculator.SCOPE_RULE is True
    return rows


def test_it_runs_on_every_committed_run_and_reruns_are_among_them():
    runs = drift.committed_runs()
    assert len(runs) == len(list(drift.RUNS.glob("*/*/input_manifest.json"))) >= 12
    assert any("rerun" in run.name for run in runs)
    named = drift.trigger(drift.RUNS / "JCI" / "0000833444-26-000087")
    assert named == {"ticker": "JCI", "cutoff": "2026-07-29", "period_end": "2026-06-30",
                     "form": "10-Q", "accession": "0000833444-26-000087"}


def test_with_the_scope_rule_off_every_published_figure_is_reproduced(control):
    """The control: today's calculator with the scope rule for a trailing year and a
    quarter turned off prints every published number as published. So every change
    the list holds is that rule's, and an unrelated drift would show here."""
    assert control == []


def test_every_changed_path_is_under_a_term_held_to_one_scope(listed):
    """Each run's changed leaves sit under a trailing-four-quarters term whose own
    value the list shows moving, or under a cell that reads one, or a differenced
    quarter: nothing moves that `trailing` or `quarter` does not read."""
    assert listed
    by_run: dict[str, list[dict]] = {}
    for row in listed:
        by_run.setdefault(row["run"], []).append(row)
    for run, rows in by_run.items():
        moved_terms = {row["path"].split(".")[2] for row in rows
                       if row["path"].startswith("terms.trailing_four_quarters")
                       and row["path"].endswith(".value") and row["path"].count(".") == 3}
        assert moved_terms, run
        published = json.loads(
            (drift.RUNS / run / calculator.FILINGS_ONLY).read_text(encoding="utf-8"))
        for row in rows:
            path = row["path"]
            if path.startswith("terms."):
                assert path.split(".")[2] in moved_terms, (run, path)
            elif path.startswith("earnings_versus_cash.smoothness."):
                continue                       # quarters differenced by `quarter`
            else:
                # a measure whose inputs name a moved term, or whose own inputs do
                cell = drift._parent(published, path)
                while cell is not None and not (isinstance(cell, dict) and "inputs" in cell):
                    cell = drift._parent(published, path := path.rsplit(".", 1)[0]) \
                        if "." in path else None
                assert cell is not None, (run, row["path"])
                text = json.dumps(cell["inputs"])
                assert any(term in row["path"] or term in text for term in moved_terms), \
                    (run, row["path"])


CUTOFF = "2026-07-29"
NET_INCOME = "NetIncomeLoss"
CONTINUING = "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations"
TOTAL = "NetCashProvidedByUsedInOperatingActivities"


def source_row(tag: str, period: str) -> float:
    """One of Johnson Controls' rows, in millions: companyfacts through the independent
    reader, or, for the two facts the 10-Q filed 2026-07-29 first stated (the store's
    companyfacts predates it), the run's own `input_numbers.json`, read here."""
    standing = source.reported("JCI", tag, period, CUTOFF)
    if standing:
        values = {row["val"] for row in standing}
    else:
        start, end = period.split("..")
        facts = json.loads((drift.RUNS / JCI / "input_numbers.json").read_text(encoding="utf-8"))
        values = {fact["number"] for fact in facts["facts"]
                  if fact["tag"] == tag and not fact.get("nil") and not fact.get("superseded_by")
                  and not (fact.get("context") or {}).get("segment")
                  and (fact.get("context") or {}).get("start") == start
                  and (fact.get("context") or {}).get("end") == end
                  and fact.get("filing_date", "9999") <= CUTOFF}
    assert len(values) == 1, (tag, period, values)
    return values.pop() / MILLION


def spread(values: list) -> float:
    """The population standard deviation, in plain arithmetic."""
    mean = sum(values) / len(values)
    return math.sqrt(sum((value - mean) ** 2 for value in values) / len(values))


def test_johnson_controls_moves_as_worked_by_hand(listed):
    """The seven leaves of the one run whose figure moves rather than goes missing,
    each worked from the source rows, in millions.

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
    year_earlier = (source_row(CONTINUING, "2023-10-01..2024-09-30")
                    + source_row(CONTINUING, "2024-10-01..2025-06-30")
                    - source_row(CONTINUING, "2023-10-01..2024-06-30"))
    published_year_earlier = (source_row(CONTINUING, "2023-10-01..2024-09-30")
                              + source_row(CONTINUING, "2024-10-01..2025-06-30")
                              - source_row(TOTAL, "2023-10-01..2024-06-30"))
    this_year = (source_row(CONTINUING, "2024-10-01..2025-09-30")
                 + source_row(CONTINUING, "2025-10-01..2026-06-30")
                 - source_row(CONTINUING, "2024-10-01..2025-06-30"))
    assert (year_earlier, published_year_earlier, this_year) == (2_938, 2_582, 3_540)
    assert source_row(CONTINUING, "2023-10-01..2024-06-30") == 216
    assert source_row(TOTAL, "2023-10-01..2024-06-30") == 572

    net_income = [
        source_row(NET_INCOME, "2026-04-01..2026-06-30"),
        source_row(NET_INCOME, "2026-01-01..2026-03-31"),
        source_row(NET_INCOME, "2025-10-01..2025-12-31"),
        source_row(NET_INCOME, "2024-10-01..2025-09-30") - source_row(NET_INCOME, "2024-10-01..2025-06-30"),
        source_row(NET_INCOME, "2025-04-01..2025-06-30"),
        source_row(NET_INCOME, "2025-01-01..2025-03-31"),
        source_row(NET_INCOME, "2024-10-01..2024-12-31"),
        source_row(NET_INCOME, "2023-10-01..2024-09-30") - source_row(NET_INCOME, "2023-10-01..2024-06-30"),
        source_row(NET_INCOME, "2024-04-01..2024-06-30"),
    ]
    assert net_income == [749, 613, 524, 1_693, 701, 478, 419, 633, 975]
    cash_to_fiscal_2025 = [
        source_row(CONTINUING, "2025-10-01..2026-06-30") - source_row(CONTINUING, "2025-10-01..2026-03-31"),
        source_row(CONTINUING, "2025-10-01..2026-03-31") - source_row(CONTINUING, "2025-10-01..2025-12-31"),
        source_row(CONTINUING, "2025-10-01..2025-12-31"),
        source_row(CONTINUING, "2024-10-01..2025-09-30") - source_row(CONTINUING, "2024-10-01..2025-06-30"),
        source_row(CONTINUING, "2024-10-01..2025-06-30") - source_row(CONTINUING, "2024-10-01..2025-03-31"),
        source_row(CONTINUING, "2024-10-01..2025-03-31") - source_row(CONTINUING, "2024-10-01..2024-12-31"),
        source_row(CONTINUING, "2024-10-01..2024-12-31"),
    ]
    assert cash_to_fiscal_2025 == [1_289, 672, 611, 968, 787, 550, 249]
    fourth_quarter = source_row(CONTINUING, "2023-10-01..2024-09-30") - source_row(CONTINUING, "2023-10-01..2024-06-30")
    published_fourth = source_row(CONTINUING, "2023-10-01..2024-09-30") - source_row(TOTAL, "2023-10-01..2024-06-30")
    oldest = source_row(CONTINUING, "2023-10-01..2024-06-30") - source_row(CONTINUING, "2023-10-01..2024-03-31")
    published_oldest = source_row(TOTAL, "2023-10-01..2024-06-30") - source_row(TOTAL, "2023-10-01..2024-03-31")
    assert (fourth_quarter, published_fourth, oldest, published_oldest) == (1_352, 996, 653, 1_021)

    def smoothness(cash: list) -> float:
        changes_in_income = [a - b for a, b in zip(net_income, net_income[1:])]
        changes_in_cash = [a - b for a, b in zip(cash, cash[1:])]
        return spread(changes_in_income) / spread(changes_in_cash)
    old_smoothness = smoothness(cash_to_fiscal_2025 + [published_fourth, published_oldest])
    new_smoothness = smoothness(cash_to_fiscal_2025 + [fourth_quarter, oldest])
    assert old_smoothness == pytest.approx(1.44369, abs=5e-6)
    assert new_smoothness == pytest.approx(1.05002, abs=5e-6)

    rows = {row["path"]: (row["old"], row["new"]) for row in listed if row["run"] == JCI}
    approx = lambda a, b: (pytest.approx(a, rel=1e-9), pytest.approx(b, rel=1e-9))  # noqa: E731
    assert rows == {
        "earnings_versus_cash.smoothness.operating_cash_flow.7":
            (published_fourth * MILLION, fourth_quarter * MILLION),
        "earnings_versus_cash.smoothness.operating_cash_flow.8":
            (published_oldest * MILLION, oldest * MILLION),
        "earnings_versus_cash.smoothness.value": approx(old_smoothness, new_smoothness),
        "ratios.growth.operating_cash_flow.trailing_four_quarters.inputs.before.parts"
        ".prior_year_to_date.value": (572 * MILLION, 216 * MILLION),
        "ratios.growth.operating_cash_flow.trailing_four_quarters.inputs.before.value":
            (published_year_earlier * MILLION, year_earlier * MILLION),
        "ratios.growth.operating_cash_flow.trailing_four_quarters.value": approx(
            (this_year - published_year_earlier) / published_year_earlier,
            (this_year - year_earlier) / year_earlier),
        "terms.trailing_four_quarters_a_year_earlier.operating_cash_flow.parts"
        ".prior_year_to_date.value": (572 * MILLION, 216 * MILLION),
        "terms.trailing_four_quarters_a_year_earlier.operating_cash_flow.value":
            (published_year_earlier * MILLION, year_earlier * MILLION),
    }
    assert (3_540 - 2_938) / 2_938 == pytest.approx(0.204901, abs=5e-7)
    assert (3_540 - 2_582) / 2_582 == pytest.approx(0.371030, abs=5e-7)


def test_dells_interest_expense_is_the_only_other_moved_term(listed):
    """Dell's published interest expense summed 1,560 (InterestExpenseNonoperating,
    fiscal 2026) + 800 (InterestExpenseDebt, six months to 2026-07-31) - 753
    (InterestExpenseNonoperating, six months to 2025-08-01); the two tags are two
    scopes (tests/test_calculator_accruals.py reads the rows), so the term and the
    interest coverage that reads it are missing, thirteen leaves. Arista's and
    Fortinet's capital expenditure, Fortinet's interest expense and Western Digital's
    depreciation and dividends each cross two tags of one same-concept group and
    stand as published."""
    dell = [row for row in listed if row["run"] == "DELL/0001571996-26-000046"]
    assert {row["run"] for row in listed} == {JCI, "DELL/0001571996-26-000046"}
    assert len(listed) == 8 + 13 and len(dell) == 13
    assert all(row["new"] is None for row in dell)
    assert {row["path"].split(".")[0] for row in dell} == {"terms", "ratios"}
    assert {row["path"].split(".")[2] for row in dell if row["path"].startswith("terms.")} \
        == {"interest_expense"}
    assert {row["path"] for row in dell if row["path"].count(".") == 3} == {
        "terms.trailing_four_quarters.interest_expense.value",
        "ratios.solvency.interest_coverage.value"}
    moved = {row["path"]: row["old"] for row in dell}
    assert moved["terms.trailing_four_quarters.interest_expense.value"] == (1_560 + 800 - 753) * MILLION


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


def test_the_printed_list_counts_per_run_and_names_old_and_new():
    rows = [{"run": "X/1", "path": "terms.t.value", "old": 2_582_000_000.0, "new": 2_938_000_000.0},
            {"run": "X/1", "path": "ratios.r.value", "old": 0.371, "new": None}]
    text = drift.printed(rows)
    assert text.splitlines() == ["X/1: 2 changed",
                                 "  terms.t.value: 2,582,000,000 -> 2,938,000,000",
                                 "  ratios.r.value: 0.371 -> missing"]
    assert drift.printed([]) == "no published figure changes"
