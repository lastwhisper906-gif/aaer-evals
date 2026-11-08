"""`src/calculator_drift.py`: which published calculator figures today's calculator prints
differently, listed by run and path, and shown to be the scope rule's alone.

A run under `runs/` stands as published; the list is for the owner to read
(`docs/needs_judgment.md`, Settled by default). Expected values: Johnson Controls'
operating cash flow over the four quarters to 2025-06-30 through
`tests/companyfacts_source.py`, worked by hand in `tests/test_calculator_accruals.py`
(1,568 + 1,586 - 216 = 2,938 million under the continuing-operations tag; the
published run summed 1,568 + 1,586 - 572 = 2,582 across two tags), and its fourth
quarter of fiscal 2024 (1,568 - 216 = 1,352; published 1,568 - 572 = 996).
"""

from __future__ import annotations

import json

import pytest

from src import calculator, calculator_drift as drift

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


def test_johnson_controls_moves_as_worked_by_hand(listed):
    """The seven leaves of the one run whose figure moves rather than goes missing."""
    rows = {row["path"]: (row["old"], row["new"]) for row in listed if row["run"] == JCI}
    assert rows == {
        "earnings_versus_cash.smoothness.operating_cash_flow.7": (996 * MILLION, 1_352 * MILLION),
        "earnings_versus_cash.smoothness.value": rows["earnings_versus_cash.smoothness.value"],
        "ratios.growth.operating_cash_flow.trailing_four_quarters.inputs.before.parts"
        ".prior_year_to_date.value": (572 * MILLION, 216 * MILLION),
        "ratios.growth.operating_cash_flow.trailing_four_quarters.inputs.before.value":
            (2_582 * MILLION, 2_938 * MILLION),
        "ratios.growth.operating_cash_flow.trailing_four_quarters.value":
            rows["ratios.growth.operating_cash_flow.trailing_four_quarters.value"],
        "terms.trailing_four_quarters_a_year_earlier.operating_cash_flow.parts"
        ".prior_year_to_date.value": (572 * MILLION, 216 * MILLION),
        "terms.trailing_four_quarters_a_year_earlier.operating_cash_flow.value":
            (2_582 * MILLION, 2_938 * MILLION),
    }
    old_growth, new_growth = rows["ratios.growth.operating_cash_flow.trailing_four_quarters.value"]
    # the growth rate over the year earlier, with 3,540 of operating cash flow this year
    # (fiscal 2025's 2,554 + 2,572 to date - 1,586, each under the continuing tag)
    assert new_growth == pytest.approx(old_growth * 2_582 / 2_938 + (2_582 / 2_938 - 1), rel=1e-9)


def test_no_other_published_run_changes(listed):
    """Only Johnson Controls mixed two scopes. Arista's and Fortinet's capital
    expenditure, Dell's and Fortinet's interest expense and Western Digital's
    depreciation and dividends each cross two tags of one same-concept group, and
    stand as published."""
    assert {row["run"] for row in listed} == {JCI}
    assert len(listed) == 7


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
