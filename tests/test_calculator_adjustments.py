"""Where an accounting adjustment's amount may come from, judged against the filings.

The rule (`calculator.adjustment_reading`, one function read by the analysis gate
and by the calculator): any dollar cell of the analysts' view
(`calculator_filings_only.json`) except under `free_cash_flow.`, `valuation.`,
`cost_of_capital.`, `market` and the sections the view removes; and, because
`applies_to` is `cash_flow` or `earnings`, both flows, a flow or a change between
two balances, never a balance at one date.

Three kinds of expected value, each written where it is used:

- **The adjustments the gate dropped in the published reruns.** Apple's note-tables
  rerun of 2026-10-29 cited `note_tables.tables.notes_38.changes.0`; Palo Alto's of
  2026-11-08 cited `notes_42.facts.8`, `notes_42.facts.14` and `notes_187.facts.17`
  (two cells of one table and one of another; the task row says three cells of
  notes_42, the run's `dropped_items` says the third is notes_187). Each cell's amount
  and period is read by eye in the filing's own note table, which the run commits as
  `input_notes.md` (paragraph ids given with each value), never from the cell.
- **Free cash flow before and after**, worked by hand from the numbers the run's view
  holds for simple free cash flow, share-based compensation and acquisitions.
- **Planted cells**, one for each class and each refused root, whose class is written
  into the test beside the cell.

The class table (`calculator.CELL_CLASSES`) is held over every USD cell of every
committed run: the published views, and the views today's calculator prints for the
same runs (four sections exist only in the latter).
"""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path

import pytest

from src import analysis_check, calculator, calculator_drift

REPO = Path(__file__).resolve().parent.parent
RUNS = REPO / "runs"
STORE = REPO / "tests" / "fixtures"
MILLION = 1_000_000

APPLE = RUNS / "AAPL" / "0000320193-26-000020-note-tables-2026-10-29"
PALO_ALTO = RUNS / "PANW" / "0001327567-26-000015-note-tables-2026-11-08"
NOT_A_FLOW = "a balance at one date is not a flow"


def view(run: Path) -> dict:
    return json.loads((run / "calculator_filings_only.json").read_text(encoding="utf-8"))


def analyst_file(run: Path) -> dict:
    return json.loads((run / "agents" / "accounting-analyst" / "analysis_accounting.json")
                      .read_text(encoding="utf-8"))


def final_with(run: Path, adjustments: list) -> dict:
    """calculator.json's free cash flow as the calculator prints it for this run's own
    inputs when the analyst's adjustments are the ones given."""
    return calculator.calculate(**calculator_drift.trigger(run), fixtures_root=STORE, bundle=run,
                                accounting={"adjustments": adjustments}
                                )["free_cash_flow"]["free_cash_flow_quality_adjusted"]


def adjustment(path: str, direction: str = "reduce", applies_to: str = "cash_flow") -> dict:
    return {"name": path, "direction": direction, "applies_to": applies_to,
            "calculator_field": path, "quote": "q"}


# --- the adjustments the gate dropped, read by eye ---------------------------------------------

def test_the_published_reruns_cited_these_cells_and_the_gate_dropped_them():
    """The analyst's own raw files and the gate's `dropped_items`, as published."""
    apple = analyst_file(APPLE)["adjustments"]
    assert [(a["calculator_field"], a["direction"], a["applies_to"]) for a in apple] == [
        ("note_tables.tables.notes_38.changes.0", "reduce", "cash_flow")]
    palo = analyst_file(PALO_ALTO)["adjustments"]
    assert [(a["calculator_field"], a["direction"], a["applies_to"]) for a in palo] == [
        ("note_tables.tables.notes_42.facts.8", "reduce", "earnings"),
        ("note_tables.tables.notes_42.facts.14", "reduce", "cash_flow"),
        ("note_tables.tables.notes_187.facts.17", "reduce", "earnings")]
    for run, count in ((APPLE, 1), (PALO_ALTO, 3)):
        published = json.loads((run / "analysis_accounting.json").read_text(encoding="utf-8"))
        assert published["dropped_count"] == count and published["adjustments"] == []
        assert all("is not a dollar amount under terms. or earnings_versus_cash." in item["reason"]
                   for item in published["dropped_items"])


# (run, path, the cell's value, its class, the period, where it was read by eye)
READ_BY_EYE = [
    # Apple, input_notes.md [0000320193-26-000020:notes:38]; the table's columns are
    # June 27, 2026 and September 27, 2025 (in millions).
    # "Gross intangible assets $ 38,220 | $ 24,950": 38,220 - 24,950 = 13,270.
    (APPLE, "note_tables.tables.notes_38.changes.0", 13_270 * MILLION, "change",
     "a change from {'instant': '2025-09-27'} to {'instant': '2026-06-27'}"),
    # "Non-current portion of intangible assets, net $ 20,342 | $ 11,093":
    # 20,342 - 11,093 = 9,249 (confirmed here; the earlier build's reading stands).
    (APPLE, "note_tables.tables.notes_38.changes.4", 9_249 * MILLION, "change",
     "a change from {'instant': '2025-09-27'} to {'instant': '2026-06-27'}"),
    # Palo Alto, input_notes.md [0001327567-26-000015:notes:42], the contingent consideration
    # table, columns three months and nine months ended April 30, 2026 and 2025 (millions).
    # "Change in fair value (110)", three months ended April 30, 2026: a duration.
    (PALO_ALTO, "note_tables.tables.notes_42.facts.8", -110 * MILLION, "flow",
     "a duration, 2026-02-01..2026-04-30"),
    # "Payments (154)", nine months ended April 30, 2026 (the cell holds it unsigned).
    (PALO_ALTO, "note_tables.tables.notes_42.facts.14", 154 * MILLION, "flow",
     "a duration, 2025-08-01..2026-04-30"),
    # [0001327567-26-000015:notes:187], other income, net: "Other, net 76", nine months
    # ended April 30, 2026.
    (PALO_ALTO, "note_tables.tables.notes_187.facts.17", 76 * MILLION, "flow",
     "a duration, 2025-08-01..2026-04-30"),
    # A change, in the notes:42 table: the liability at the end of the three months,
    # 240, less the liability at the beginning, 369: -129.
    (PALO_ALTO, "note_tables.tables.notes_42.changes.4", -129 * MILLION, "change",
     "a change from {'instant': '2026-01-31'} to {'instant': '2026-04-30'}"),
]


@pytest.mark.parametrize("run, path, amount, kind, period", READ_BY_EYE,
                         ids=[row[1].replace("note_tables.tables.", "") for row in READ_BY_EYE])
def test_a_flow_or_a_change_in_a_note_table_is_an_amount(run, path, amount, kind, period):
    held = view(run)
    cell = calculator._cell_at(held, path)
    assert cell["value"] == amount                      # the filing's number, as read by eye
    assert calculator.cell_period(cell) == (kind, period)
    assert calculator.adjustment_reading(held, path) == (amount, None)
    assert calculator.adjustment_amount(held, path) == amount
    assert analysis_check.adjustment_problem(held)(
        {"direction": "reduce", "applies_to": "cash_flow", "calculator_field": path,
         "quote": "q"}) is None


# (run, path, the cell's value, the date, where it was read by eye): balances, refused.
BALANCES_BY_EYE = [
    # Apple notes:38, "Non-current portion of intangible assets, net $ 20,342", June 27, 2026.
    (APPLE, "note_tables.tables.notes_38.facts.8", 20_342 * MILLION, "2026-06-27"),
    # Palo Alto notes:42, "Contingent consideration liability at the end of the period $ 240",
    # three months ended April 30, 2026, and "at the beginning of the period $ 369".
    (PALO_ALTO, "note_tables.tables.notes_42.facts.16", 240 * MILLION, "2026-04-30"),
    (PALO_ALTO, "note_tables.tables.notes_42.facts.0", 369 * MILLION, "2026-01-31"),
]


@pytest.mark.parametrize("run, path, value, day", BALANCES_BY_EYE,
                         ids=[row[1].replace("note_tables.tables.", "") for row in BALANCES_BY_EYE])
def test_a_balance_at_one_date_in_a_note_table_is_refused(run, path, value, day):
    held = view(run)
    assert calculator._cell_at(held, path)["value"] == value
    amount, reason = calculator.adjustment_reading(held, path)
    assert amount is None
    assert NOT_A_FLOW in reason and f"one date, {day}" in reason
    problem = analysis_check.adjustment_problem(held)(
        {"direction": "reduce", "applies_to": "earnings", "calculator_field": path, "quote": "q"})
    assert problem == f"calculator_field {path!r} cannot be an adjustment's amount: {reason}"


def test_apples_intangible_change_moves_free_cash_flow_by_the_amount():
    """Free cash flow before: the view's free_cash_flow_simple 136,683 less share-based
    compensation 13,706 less acquisitions 0 (the statement prints none) = 122,977
    (millions; each read in the view's `inputs`, the sum worked here by hand)."""
    held = view(APPLE)["free_cash_flow"]["free_cash_flow_quality_adjusted"]
    assert held["inputs"]["free_cash_flow_simple"] == 136_683 * MILLION
    assert held["inputs"]["share_based_compensation"]["value"] == 13_706 * MILLION
    assert held["inputs"]["acquisitions"]["cash_spent"] == 0
    before = (136_683 - 13_706 - 0) * MILLION
    assert before == 122_977 * MILLION and held["value"] == before and held["adjustments_applied"] == []

    cited = final_with(APPLE, [adjustment("note_tables.tables.notes_38.changes.0")])
    assert cited["adjustments_refused"] == []
    assert [(row["amount"], row["before"], row["after"]) for row in cited["adjustments_applied"]] == [
        (13_270 * MILLION, 122_977 * MILLION, (122_977 - 13_270) * MILLION)]
    assert cited["value"] == 109_707 * MILLION            # 122,977 - 13,270

    both = final_with(APPLE, [adjustment("note_tables.tables.notes_38.changes.0"),
                              adjustment("note_tables.tables.notes_38.changes.4", "increase")])
    assert [(row["before"], row["after"]) for row in both["adjustments_applied"]] == [
        (122_977 * MILLION, 109_707 * MILLION), (109_707 * MILLION, 118_956 * MILLION)]
    assert both["value"] == 118_956 * MILLION             # 109,707 + 9,249


def test_palo_altos_three_cells_move_free_cash_flow_and_its_balance_does_not():
    """Before: simple 3,793.8 less share-based compensation 1,668.1 less acquisitions
    5,118.4 = -2,992.7 (millions, from the view's `inputs`). The three cells are durations,
    each taken by its size and the analyst's direction (reduce): -2,992.7 - 110 = -3,102.7;
    - 154 = -3,256.7; - 76 = -3,332.7. The fourth is the liability at April 30, 2026."""
    held = view(PALO_ALTO)["free_cash_flow"]["free_cash_flow_quality_adjusted"]
    assert held["inputs"]["free_cash_flow_simple"] == 3_793_800_000
    assert held["inputs"]["share_based_compensation"]["value"] == 1_668_100_000
    assert held["inputs"]["acquisitions"]["cash_spent"] == 5_118_400_000
    assert 3_793_800_000 - 1_668_100_000 - 5_118_400_000 == -2_992_700_000 == held["value"]

    out = final_with(PALO_ALTO, [
        adjustment("note_tables.tables.notes_42.facts.8", applies_to="earnings"),
        adjustment("note_tables.tables.notes_42.facts.14"),
        adjustment("note_tables.tables.notes_187.facts.17", applies_to="earnings"),
        adjustment("note_tables.tables.notes_42.facts.16")])
    assert [(row["amount"], row["before"], row["after"]) for row in out["adjustments_applied"]] == [
        (110_000_000, -2_992_700_000, -3_102_700_000),
        (154_000_000, -3_102_700_000, -3_256_700_000),
        (76_000_000, -3_256_700_000, -3_332_700_000)]
    assert out["value"] == -3_332_700_000
    assert [(row["calculator_field"], NOT_A_FLOW in row["reason"])
            for row in out["adjustments_refused"]] == [
        ("note_tables.tables.notes_42.facts.16", True)]


# --- planted cells: each class, each refused root ----------------------------------------------

def usd(**more) -> dict:
    return {"value": 1_000_000.0, "unit": "USD", **more}


PLANTED = {
    # a calculator cell's own period: two dates joined by `..` is a duration, one date a balance
    "terms": {
        "trailing_four_quarters": {
            "revenue": usd(),                                            # no period: the table says a flow
            "operating_income": usd(parts={"this_year_to_date": usd(period="2026-01-01..2026-06-30")}),
        },
        "balances_now": {
            "receivables": usd(period="2026-06-30"),                     # one date
            "operating_lease_liability": usd(),                          # no period: the table says a balance
        },
        "debt_now": usd(lines=[usd(period="2026-06-30")]),
    },
    "note_tables": {"tables": {"notes_1": {
        "facts": [
            usd(unit="iso4217:USD", start="2025-08-01", end="2026-04-30"),   # 0 a duration
            usd(unit="iso4217:USD", instant="2026-04-30"),                   # 1 one date
            usd(unit="iso4217:USD", start="2025-08-01"),                     # 2 a start and no end: no period
        ],
        "changes": [
            {**usd(unit="iso4217:USD"), "from": {"instant": "2025-09-27"},
             "to": {"instant": "2026-06-27"}},                                # 0 a change
        ]}}},
    "earnings_versus_cash": {"working_capital": {"receivables": {"balance_sheet_change": usd()}}},
    "ratios": {"efficiency": {"days_sales_outstanding": {"value": 61.0, "unit": "days"}},
               "liquidity": {"current_ratio": {"value": 2.5, "unit": "ratio"}}},
    "ebit": usd(),
    "mystery": {"number": usd()},                                        # no period, not in the table
    # the roots refused, each carrying a flow-shaped dollar cell so only the root refuses it
    "free_cash_flow": {"free_cash_flow_simple": usd(period="2025-07-01..2026-06-30")},
    "valuation": {"base": usd(period="2025-07-01..2026-06-30")},
    "cost_of_capital": {"debt": usd(period="2025-07-01..2026-06-30")},
    "market": {"price_at_cutoff": usd(period="2025-07-01..2026-06-30")},
    "market_inputs": {"x": usd(period="2025-07-01..2026-06-30")},
    "free_cash_flow_yield": {"x": usd(period="2025-07-01..2026-06-30")},
    "wacc_components": {"x": usd(period="2025-07-01..2026-06-30")},
    "implied_growth_beside_history": {"x": usd(period="2025-07-01..2026-06-30")},
}


@pytest.mark.parametrize("path, amount", [
    ("terms.trailing_four_quarters.revenue", 1_000_000.0),                          # no period, section: flow
    ("terms.trailing_four_quarters.operating_income.parts.this_year_to_date", 1_000_000.0),  # `..` duration
    ("note_tables.tables.notes_1.facts.0", 1_000_000.0),                            # start and end, the filing's unit
    ("note_tables.tables.notes_1.changes.0", 1_000_000.0),                          # a change
    ("earnings_versus_cash.working_capital.receivables.balance_sheet_change", 1_000_000.0),  # table: a change
    ("ebit", 1_000_000.0),                                                          # table: a flow
])
def test_a_flow_or_a_change_stands_and_the_amount_is_its_value(path, amount):
    assert calculator.adjustment_reading(PLANTED, path) == (amount, None)


@pytest.mark.parametrize("path, said", [
    ("terms.balances_now.receivables", "one date, 2026-06-30"),                     # a period of one date
    ("terms.balances_now.operating_lease_liability", "a line of the balance sheet"),  # table: a balance
    ("terms.debt_now.lines.0", "one date, 2026-06-30"),                             # a debt line is a balance
    ("note_tables.tables.notes_1.facts.1", "one date, 2026-04-30"),                 # an instant
])
def test_a_balance_at_one_date_is_refused_with_its_reason(path, said):
    amount, reason = calculator.adjustment_reading(PLANTED, path)
    assert amount is None
    assert reason.startswith(NOT_A_FLOW + ": ") and said in reason


@pytest.mark.parametrize("path, reason", [
    ("free_cash_flow.free_cash_flow_simple",
     "it is under free_cash_flow: an adjustment of free cash flow cannot be read from free cash flow"),
    ("valuation.base",
     "it is under valuation: the valuation reads a price, which the analysts' view removes"),
    ("cost_of_capital.debt",
     "it is under cost_of_capital: the cost of capital reads a price, which the analysts' view removes"),
    ("market.price_at_cutoff",
     "it is under market: the market table is a price, which the analysts' view removes"),
    ("market_inputs.x",
     "it is under market: the market table is a price, which the analysts' view removes"),
    ("free_cash_flow_yield.x", "it is under free_cash_flow_yield, a section the analysts' view "
                              "removes because it reads a price"),
    ("wacc_components.x", "it is under wacc_components, a section the analysts' view "
                          "removes because it reads a price"),
    ("implied_growth_beside_history.x", "it is under implied_growth_beside_history, a section the "
                                        "analysts' view removes because it reads a price"),
])
def test_a_refused_root_is_refused_by_name_whatever_the_cell(path, reason):
    """Each root carries a dollar cell with a duration, so nothing but the root refuses it;
    the first row's cell, free cash flow, is the one a free-cash-flow adjustment must never read."""
    assert calculator.adjustment_reading(PLANTED, path) == (None, reason)


def test_the_sections_the_view_removes_are_each_refused():
    """Every section `filings_only` removes is a root no amount is read from, with no list
    kept apart from `PRICED_SECTIONS`."""
    for section in calculator.PRICED_SECTIONS:
        fields = {section: {"x": usd(period="2025-07-01..2026-06-30")}}
        amount, reason = calculator.adjustment_reading(fields, f"{section}.x")
        assert amount is None and reason.startswith("it is under "), section


@pytest.mark.parametrize("path, said", [
    ("ratios.efficiency.days_sales_outstanding", "not a dollar cell"),              # days
    ("ratios.liquidity.current_ratio", "not a dollar cell"),                        # a ratio
    ("terms.trailing_four_quarters", "not a dollar cell"),                          # a dict with no unit
    ("terms", "not a dollar cell"),
    ("terms.nowhere", "names no cell"),
    ("terms.balances_now.receivables.value", "not a dollar cell"),                  # a bare number
    ("", "names no path"),
    ("mystery.number", "does not place it"),                                        # the table's fallback
    ("note_tables.tables.notes_1.facts.2", "does not place it"),                    # a start and no end
    ("terms.debt_now.lines.²", "names no cell"),                                    # not an ASCII digit
    ("terms.debt_now.lines.①", "names no cell"),
    ("terms.debt_now.lines.9", "names no cell"),
])
def test_what_is_not_a_cell_to_take_an_amount_from_is_named(path, said):
    amount, reason = calculator.adjustment_reading(PLANTED, path)
    assert amount is None and said in reason


def test_a_path_that_is_not_a_string_names_nothing():
    for path in (None, 3, ["terms"], {"terms": 1}):
        assert calculator.adjustment_reading(PLANTED, path)[0] is None


def test_a_cell_with_periods_of_two_kinds_is_refused_not_guessed():
    fields = {"terms": {"x": usd(period="2026-06-30", start="2025-07-01", end="2026-06-30")}}
    amount, reason = calculator.adjustment_reading(fields, "terms.x")
    assert amount is None and "more than one kind" in reason


def test_a_dollar_cell_whose_value_is_not_a_number_is_refused():
    fields = {"terms": {"x": {"value": None, "unit": "USD", "period": "2025-07-01..2026-06-30"},
                        "y": {"value": True, "unit": "USD", "period": "2025-07-01..2026-06-30"},
                        "z": {"value": float("inf"), "unit": "USD", "period": "2025-07-01..2026-06-30"}}}
    for name in "xyz":
        assert calculator.adjustment_reading(fields, f"terms.{name}") == (None, "its value is not a number")


def test_a_unit_that_is_not_a_dollar_is_not_one_even_in_the_filings_spelling():
    for unit in ("iso4217:EUR", "shares", "xbrli:shares", "usd", "USD/shares"):
        fields = {"terms": {"x": {"value": 5.0, "unit": unit, "period": "2025-07-01..2026-06-30"}}}
        assert calculator.adjustment_reading(fields, "terms.x")[0] is None, unit


def test_a_list_is_indexed_by_ascii_digits_alone_and_nothing_raises():
    """The reading the old gate's test held for a debt line, held here for a flow: '²' and
    '①' are digits to `str.isdigit` and not to `int`, and such a part names nothing."""
    fields = {"terms": {"lines": [usd(period="2025-07-01..2026-06-30")]}}
    assert calculator.adjustment_reading(fields, "terms.lines.0") == (1_000_000.0, None)
    for part in ("²", "①", "٣", "-1", "00x"):
        assert calculator.adjustment_reading(fields, f"terms.lines.{part}")[0] is None, part


def test_a_period_decides_before_the_table_does():
    """A cell under a name the table calls a balance, with a duration of its own, is a flow:
    the cell says what it is."""
    fields = {"terms": {"balances_now": {"x": usd(period="2025-07-01..2026-06-30")}}}
    assert calculator.adjustment_reading(fields, "terms.balances_now.x")[0] == 1_000_000.0


def test_the_unit_may_be_the_calculators_or_the_filings():
    for unit in ("USD", "iso4217:USD"):
        fields = {"terms": {"x": usd(unit=unit, period="2025-07-01..2026-06-30")}}
        assert calculator.adjustment_reading(fields, "terms.x") == (1_000_000.0, None)


# --- the gate and the calculator read one rule --------------------------------------------------

@pytest.mark.parametrize("path", [
    "terms.balances_now.receivables", "free_cash_flow.free_cash_flow_simple", "valuation.base",
    "ratios.liquidity.current_ratio", "terms.nowhere", "mystery.number",
    "terms.trailing_four_quarters.revenue"])
def test_the_gate_and_the_calculator_say_the_same_thing(path):
    amount, reason = calculator.adjustment_reading(PLANTED, path)
    gate = analysis_check.adjustment_problem(PLANTED)(
        {"direction": "reduce", "applies_to": "cash_flow", "calculator_field": path, "quote": "q"})
    if amount is not None:
        assert gate is None
    else:
        assert gate == f"calculator_field {path!r} cannot be an adjustment's amount: {reason}"


def test_the_gate_still_checks_what_it_checked_before():
    problem = analysis_check.adjustment_problem(PLANTED)
    base = {"direction": "reduce", "applies_to": "cash_flow",
            "calculator_field": "terms.trailing_four_quarters.revenue", "quote": "q"}
    assert problem(base) is None
    assert "direction" in problem({**base, "direction": "hold"})
    assert "applies_to" in problem({**base, "applies_to": "debt"})
    assert problem({**base, "quote": ""}) == "an adjustment carries no quote"


def test_the_calculator_lists_a_refused_adjustment_with_the_same_reason():
    from src.calculator import quality_adjusted
    simple = {"value": 100.0}
    out = quality_adjusted(simple, {"value": 10.0}, {"value": 0.0, "formula": "x"},
                           [adjustment("terms.balances_now.receivables"),
                            adjustment("terms.trailing_four_quarters.revenue", "increase"),
                            adjustment("free_cash_flow.free_cash_flow_simple"),
                            {**adjustment("terms.trailing_four_quarters.revenue"), "direction": "sideways"}],
                           PLANTED)
    assert out["value"] == 100.0 - 10.0 + 1_000_000.0
    assert [(r["after"]) for r in out["adjustments_applied"]] == [1_000_090.0]
    reasons = {row["calculator_field"]: row["reason"] for row in out["adjustments_refused"]}
    assert reasons["terms.balances_now.receivables"] == (
        "'terms.balances_now.receivables' cannot be an adjustment's amount: "
        + calculator.adjustment_reading(PLANTED, "terms.balances_now.receivables")[1])
    assert "cannot be read from free cash flow" in reasons["free_cash_flow.free_cash_flow_simple"]
    assert "direction is not 'reduce' or 'increase'" in list(reasons.values())


def test_the_module_says_nothing_about_debt_is_adjusted_here():
    text = (REPO / "src" / "calculator.py").read_text(encoding="utf-8")
    assert "Nothing about debt" in text and "adjusted debt in the next wave" in text
    assert "Nothing about debt is decided here" in calculator.adjustment_reading.__doc__
    assert "Nothing about debt is applied here" in calculator.quality_adjusted.__doc__


# --- the class table, held over every committed run's analysts' view -----------------------------

def usd_cells(node, path=""):
    """Every dict with a dollar unit, by its dotted path."""
    if isinstance(node, dict):
        if node.get("unit") in calculator.USD_UNITS:
            yield path, node
        for key, value in node.items():
            yield from usd_cells(value, f"{path}.{key}" if path else key)
    elif isinstance(node, list):
        for position, value in enumerate(node):
            yield from usd_cells(value, f"{path}.{position}" if path else str(position))


def refused_root(path: str) -> bool:
    root = path.split(".")[0]
    return root in {name for name, _ in calculator.ADJUSTMENT_REFUSED_ROOTS} | set(
        calculator.PRICED_SECTIONS) or root.startswith("market")


def committed_views() -> list[tuple[str, dict]]:
    return [(str(path.parent.relative_to(RUNS)), json.loads(path.read_text(encoding="utf-8")))
            for path in sorted(RUNS.glob("*/*/calculator_filings_only.json"))]


@pytest.fixture(scope="module")
def published_views():
    views = committed_views()
    assert len(views) >= 32
    return views


@pytest.fixture(scope="module")
def todays_views(published_views):
    """The same runs' views as today's calculator prints them: four sections exist only here."""
    return [(name, calculator_drift.recompute(RUNS / name, STORE)) for name, _ in published_views]


def classes_of(path: str, cell: dict) -> set[str]:
    """Every class a cell is put in: by its own period, and by each entry of the table."""
    own = calculator.cell_period(cell)
    found = {kind for kind, pattern, _ in calculator.CELL_CLASSES if re.fullmatch(pattern, path)}
    if own is not None:
        found.add(own[0])
    return found


def check_every_cell_is_in_exactly_one_class(views):
    counted = {"flow": 0, "change": 0, "balance": 0, "root": 0}
    for name, held in views:
        for path, cell in usd_cells(held):
            if refused_root(path):
                counted["root"] += 1
                assert calculator.adjustment_reading(held, path)[0] is None, (name, path)
                continue
            found = classes_of(path, cell)
            assert len(found) == 1, (name, path, found)
            kind, why = calculator.cell_class(path, cell)
            assert {kind} == found and why, (name, path)
            counted[kind] += 1
    return counted


def test_every_dollar_cell_of_every_published_view_is_in_exactly_one_class(published_views):
    counted = check_every_cell_is_in_exactly_one_class(published_views)
    assert all(counted.values()), counted            # a class nothing falls in would be a dead class


def test_every_dollar_cell_of_every_view_as_printed_today_is_in_exactly_one_class(todays_views):
    counted = check_every_cell_is_in_exactly_one_class(todays_views)
    assert all(counted.values()), counted
    sections = {section for _, held in todays_views for section in held}
    assert {"quarterly_cash_flow_and_accruals", "receivables_extension",
            "contract_liabilities_and_billings", "inventory_composition_and_growth_gap",
            "note_tables"} <= sections


def test_a_cell_that_names_no_period_is_placed_by_the_table_and_every_entry_is_used(todays_views):
    used = [0] * len(calculator.CELL_CLASSES)
    for _, held in todays_views:
        for path, cell in usd_cells(held):
            if refused_root(path) or calculator.cell_period(cell) is not None:
                continue
            for position, (_, pattern, _) in enumerate(calculator.CELL_CLASSES):
                if re.fullmatch(pattern, path):
                    used[position] += 1
    assert all(used), used                           # an entry no cell uses is not a fact of the cells


def test_every_table_entry_has_a_class_a_pattern_and_one_line_of_why():
    for kind, pattern, why in calculator.CELL_CLASSES:
        assert kind in (calculator.FLOW, calculator.CHANGE, calculator.BALANCE)
        assert re.compile(pattern) and why.strip() and "\n" not in why


# One planted path for each table entry, in the table's order, with the class it must get.
ONE_PATH_PER_ENTRY = [
    ("terms.balances_now.operating_lease_liability", "balance"),
    ("quarterly_cash_flow_and_accruals.balance_sheet_accruals.inputs.change_in_debt_in_current_liabilities."
     "inputs.now", "balance"),
    ("earnings_versus_cash.working_capital.receivables.balance_sheet_change", "change"),
    ("earnings_versus_cash.working_capital.inventory.share_of_net_income.inputs.change", "change"),
    ("terms.trailing_four_quarters.change_in_receivables", "flow"),
    ("ratios.profitability.net_margin.inputs.revenue", "flow"),
    ("ratios.solvency.ebitda.inputs.depreciation_and_amortization.parts.this_year_to_date", "flow"),
    ("earnings_versus_cash.working_capital.inventory.cash_flow_statement_change", "flow"),
    ("ratios.growth.revenue.trailing_four_quarters.inputs.now", "flow"),
    ("quarterly_cash_flow_and_accruals.operating_cash_flow_quarterly", "flow"),
]


def test_the_table_has_a_planted_path_for_each_entry():
    assert len(ONE_PATH_PER_ENTRY) == len(calculator.CELL_CLASSES)
    for position, ((path, kind), entry) in enumerate(zip(ONE_PATH_PER_ENTRY, calculator.CELL_CLASSES)):
        assert re.fullmatch(entry[1], path), (position, path)
        assert entry[0] == kind, (position, path)
        assert classes_of(path, usd()) == {kind}, (position, path)
        # the cell is put at its path by walking the parts
        parts = path.split(".")
        built: dict = {}
        cursor = built
        for part in parts[:-1]:
            cursor = cursor.setdefault(part, {})
        cursor[parts[-1]] = usd()
        amount, reason = calculator.adjustment_reading(built, path)
        if kind == "balance":
            assert amount is None and reason.startswith(NOT_A_FLOW + ": " + entry[2]), position
        else:
            assert amount == 1_000_000.0, (position, reason)


# The names the table classes, written out here so that a name dropped from the table fails.
FLOW_NAMES = {"revenue", "revenue_a_year_earlier", "net_income", "cost_of_revenue", "ebit", "ebitda",
              "pretax_income", "income_tax_expense", "interest_expense", "operating_cash_flow",
              "operating_cash_flow_discontinued", "operating_cash_flow_of_continuing_operations",
              "income_from_continuing_operations", "capital_expenditure",
              "depreciation_and_amortization", "free_cash_flow_simple", "free_cash_flow_accruals",
              "billings", "billings_a_year_earlier"}
BALANCE_NAMES = {"balances_now", "balances_a_year_earlier", "debt_now", "debt_a_year_earlier",
                 "cash_and_short_term_investments_now", "debt_at_the_start", "debt_at_the_end",
                 "operating_lease_liability", "total_debt", "net_debt", "invested_capital"}
CHANGE_NAMES = {"balance_sheet_change", "articulation_gap", "change_in_cash",
                "change_in_current_assets", "change_in_current_liabilities",
                "change_in_debt_in_current_liabilities", "change_in_income_taxes_payable",
                "change_in_contract_liabilities"}


def test_the_table_names_are_the_ones_written_out_here():
    assert set(calculator._FLOW_NAMES.split("|")) == FLOW_NAMES
    assert set(calculator._BALANCE_NAMES.split("|")) == BALANCE_NAMES
    assert set(calculator._CHANGE_NAMES.split("|")) == CHANGE_NAMES


@pytest.mark.parametrize("kind, names", [("flow", FLOW_NAMES), ("balance", BALANCE_NAMES),
                                          ("change", CHANGE_NAMES)])
def test_a_cell_with_no_period_under_a_name_of_the_table_is_of_its_class(kind, names):
    for name in sorted(names):
        path = f"ratios.profitability.some_ratio.inputs.{name}"
        assert calculator.cell_class(path, usd())[0] == kind, name
        assert {k for k, pattern, _ in calculator.CELL_CLASSES if re.fullmatch(pattern, path)} == {kind}


@pytest.mark.parametrize("section, kind", [
    ("terms.balances_now", "balance"), ("terms.balances_a_year_earlier", "balance"),
    ("terms.debt_now", "balance"), ("terms.debt_a_year_earlier", "balance"),
    ("terms.cash_and_short_term_investments_now", "balance"),
    ("terms.trailing_four_quarters", "flow"), ("terms.trailing_four_quarters_a_year_earlier", "flow"),
    ("terms.cash_flow_families", "flow")])
def test_a_cell_with_no_period_in_a_section_of_the_terms_is_of_its_class(section, kind):
    path = f"{section}.some_line"
    assert calculator.cell_class(path, usd())[0] == kind
    assert calculator.cell_class(f"{path}.parts.some_part", usd())[0] == kind


def test_a_balance_names_the_table_line_that_says_so():
    """The reason is built from the table: it carries the entry's own line of why."""
    built = {"terms": {"balances_now": {"x": usd()}}}
    amount, reason = calculator.adjustment_reading(built, "terms.balances_now.x")
    assert amount is None
    assert calculator.CELL_CLASSES[0][2] in reason and calculator.PLACED_BY_THE_TABLE in reason


def test_a_cell_on_a_published_view_is_never_left_to_the_fallback(published_views):
    for name, held in published_views:
        for path, cell in usd_cells(held):
            if not refused_root(path):
                assert calculator.cell_class(path, cell)[0] is not None, (name, path)


# --- the accounting analyst's definition ---------------------------------------------------------

def adjustments_section() -> str:
    text = (REPO / ".claude" / "agents" / "accounting-analyst.md").read_text(encoding="utf-8")
    start = text.index("## Adjustments")
    return " ".join(text[start:text.index("## Citations")].split())


def test_the_definition_says_what_the_rule_says():
    section = adjustments_section()
    for sentence in (
            "The amount may be any dollar cell of `calculator_filings_only.json` except free cash "
            "flow itself",
            "an adjustment of free cash flow cannot be read from free cash flow",
            "`cash_flow` and `earnings` are both flows",
            "the cell must be a flow (a number over a span of dates) or a change between two balances",
            "a note table's `changes` cell is a change, later minus earlier",
            "A balance at one date is not a flow",
            "Python drops an adjustment that names one"):
        assert sentence in section, sentence
    text = (REPO / ".claude" / "agents" / "accounting-analyst.md").read_text(encoding="utf-8")
    assert re.search(r"`applies_to` is `cash_flow` or\s+`earnings`, and either needs "
                     r"`calculator_field` to be a flow or a change, never\s+a balance at one date", text)
    # what still held stays
    for kept in ("You never compute the amount", "you never take a portion of a field",
                 "Share-based compensation and acquisitions are already subtracted there",
                 "`earnings_versus_cash.working_capital.receivables.balance_sheet_change`"):
        assert kept in section, kept


@pytest.mark.parametrize("path, run, kind", [
    ("note_tables.tables.notes_42.facts.14", PALO_ALTO, "flow"),
    ("note_tables.tables.notes_38.changes.0", APPLE, "change"),
    ("earnings_versus_cash.working_capital.receivables.balance_sheet_change",
     RUNS / "DELL" / "0001571996-26-000046", "change"),
])
def test_each_example_path_in_the_definition_resolves_in_a_published_run_and_is_accepted(path, run, kind):
    assert f"`{path}`" in adjustments_section()
    held = view(run)
    cell = calculator._cell_at(held, path)
    assert isinstance(cell, dict) and "value" in cell
    assert calculator.cell_class(path, cell)[0] == kind
    assert calculator.adjustment_reading(held, path)[0] == cell["value"]
