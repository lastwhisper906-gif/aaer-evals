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
from tests import companyfacts_source as source

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


def test_apples_free_cash_flow_before_is_worked_by_hand_from_companyfacts():
    """Apple's trailing four quarters to 2026-06-27, each term read in companyfacts through
    `tests/companyfacts_source.py` (rows filed at or before the cutoff 2026-07-31, the latest
    filing per period): the fiscal year 2024-09-29..2025-09-27 of the 10-K, plus the nine
    months 2025-09-28..2026-06-27, less the nine months 2024-09-29..2025-06-28.
    Operating cash flow 111,482 + 116,996 - 81,754 = 146,724; payments for property and
    equipment 12,715 + 6,799 - 9,473 = 10,041; share-based compensation 12,863 + 10,523 -
    9,680 = 13,706; acquisitions none (companyfacts holds no row, the statement prints none).
    Free cash flow 146,724 - 10,041 = 136,683, less 13,706 = 122,977 (millions)."""
    cutoff = view(APPLE)["cutoff"]
    assert cutoff == "2026-07-31"
    year, ytd, before = "2024-09-29..2025-09-27", "2025-09-28..2026-06-27", "2024-09-29..2025-06-28"

    def trailing(tag):
        return (source.one_value("AAPL", tag, year, cutoff) + source.one_value("AAPL", tag, ytd, cutoff)
                - source.one_value("AAPL", tag, before, cutoff))
    assert source.reported("AAPL", "PaymentsToAcquireBusinessesNetOfCashAcquired", ytd, cutoff) == []
    cash = trailing("NetCashProvidedByUsedInOperatingActivities")
    capex = trailing("PaymentsToAcquirePropertyPlantAndEquipment")
    pay = trailing("ShareBasedCompensation")
    assert (cash, capex, pay) == (146_724 * MILLION, 10_041 * MILLION, 13_706 * MILLION)
    by_hand = cash - capex - pay - 0
    assert by_hand == 122_977 * MILLION
    held = view(APPLE)["free_cash_flow"]["free_cash_flow_quality_adjusted"]
    assert held["value"] == by_hand and held["adjustments_applied"] == []
    assert final_with(APPLE, [])["value"] == by_hand


def test_apples_intangible_change_moves_free_cash_flow_by_the_amount():
    before = (146_724 - 10_041 - 13_706 - 0) * MILLION           # the hand-worked base above
    cited = final_with(APPLE, [adjustment("note_tables.tables.notes_38.changes.0")])
    assert cited["adjustments_refused"] == [] and cited["adjustments_to_earnings"] == []
    row, = cited["adjustments_applied"]
    assert (row["amount"], row["before"], row["after"]) == (
        13_270 * MILLION, before, (122_977 - 13_270) * MILLION)
    assert cited["value"] == 109_707 * MILLION            # 122,977 - 13,270
    # the row carries the cell's signed value, its class and its dates beside the amount
    assert (row["signed_value"], row["class"], row["direction"], row["applies_to"]) == (
        13_270 * MILLION, "change", "reduce", "cash_flow")
    assert row["period"] == {"from": {"instant": "2025-09-27"}, "to": {"instant": "2026-06-27"}}
    assert row["free_cash_flow_covers"] == "the four quarters ending 2026-06-27"

    both = final_with(APPLE, [adjustment("note_tables.tables.notes_38.changes.0"),
                              adjustment("note_tables.tables.notes_38.changes.4", "increase")])
    assert [(row["before"], row["after"]) for row in both["adjustments_applied"]] == [
        (122_977 * MILLION, 109_707 * MILLION), (109_707 * MILLION, 118_956 * MILLION)]
    assert both["value"] == 118_956 * MILLION             # 109,707 + 9,249


def test_palo_altos_payments_move_free_cash_flow_and_its_earnings_cells_move_nothing():
    """Before: simple 3,793.8 less share-based compensation 1,668.1 less acquisitions
    5,118.4 = -2,992.7 (millions). The analyst's three cells are durations ending at the
    period end 2026-04-30, as the analyst typed them: facts.8 and notes_187.facts.17 for
    `earnings`, facts.14 for `cash_flow`. Only the cash-flow one moves free cash flow:
    -2,992.7 - 154 = -3,146.7. The two earnings ones are listed, 110 and 76, applied to
    nothing. The fourth cell, the liability at April 30, 2026, is a balance."""
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
    row, = out["adjustments_applied"]
    assert (row["amount"], row["before"], row["after"]) == (
        154_000_000, -2_992_700_000, -3_146_700_000)
    assert out["value"] == -3_146_700_000
    assert (row["signed_value"], row["class"], row["period"]) == (
        154_000_000, "flow", "2025-08-01..2026-04-30")
    assert row["free_cash_flow_covers"] == "the four quarters ending 2026-04-30"
    assert [(r["calculator_field"], r["amount"], r["signed_value"], r["class"], r["period"],
             r["applied_to"].startswith("nothing")) for r in out["adjustments_to_earnings"]] == [
        ("note_tables.tables.notes_42.facts.8", 110_000_000, -110_000_000, "flow",
         "2026-02-01..2026-04-30", True),
        ("note_tables.tables.notes_187.facts.17", 76_000_000, 76_000_000, "flow",
         "2025-08-01..2026-04-30", True)]
    assert [(r["calculator_field"], NOT_A_FLOW in r["reason"]) for r in out["adjustments_refused"]] == [
        ("note_tables.tables.notes_42.facts.16", True)]


def test_an_earnings_adjustment_moves_free_cash_flow_by_nothing():
    """Two adjustments of one cell, one for each target: free cash flow moves by the first."""
    path = "note_tables.tables.notes_42.facts.14"
    only_cash = final_with(PALO_ALTO, [adjustment(path)])["value"]
    both = final_with(PALO_ALTO, [adjustment(path), adjustment(path, applies_to="earnings")])
    assert both["value"] == only_cash == -3_146_700_000
    assert len(both["adjustments_applied"]) == 1 and len(both["adjustments_to_earnings"]) == 1


# --- planted cells: each class, each refused root ----------------------------------------------

def usd(**more) -> dict:
    return {"value": 1_000_000.0, "unit": "USD", **more}


PLANTED = {
    "period_end": "2026-06-30",
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
            usd(unit="iso4217:USD", start="2025-07-01", end="2026-06-30"),   # 0 a duration
            usd(unit="iso4217:USD", instant="2026-04-30"),                   # 1 one date
            usd(unit="iso4217:USD", start="2025-08-01"),                     # 2 a start and no end: no period
        ],
        "changes": [
            {**usd(unit="iso4217:USD"), "from": {"instant": "2025-06-30"},
             "to": {"instant": "2026-06-30"}},                                # 0 a change
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
    fields = {"period_end": "2026-06-30",
              "terms": {"x": {"value": None, "unit": "USD", "period": "2025-07-01..2026-06-30"},
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
    fields = {"period_end": "2026-06-30", "terms": {"lines": [usd(period="2025-07-01..2026-06-30")]}}
    assert calculator.adjustment_reading(fields, "terms.lines.0") == (1_000_000.0, None)
    for part in ("²", "①", "٣", "-1", "00x"):
        assert calculator.adjustment_reading(fields, f"terms.lines.{part}")[0] is None, part


def test_a_period_decides_before_the_table_does():
    """A cell under a name the table calls a balance, with a duration of its own, is a flow:
    the cell says what it is."""
    fields = {"period_end": "2026-06-30",
              "terms": {"balances_now": {"x": usd(period="2025-07-01..2026-06-30")}}}
    assert calculator.adjustment_reading(fields, "terms.balances_now.x")[0] == 1_000_000.0


def test_the_unit_may_be_the_calculators_or_the_filings():
    for unit in ("USD", "iso4217:USD"):
        fields = {"period_end": "2026-06-30", "terms": {"x": usd(unit=unit, period="2025-07-01..2026-06-30")}}
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
    assert "Nothing about debt is" in " ".join(calculator.quality_adjusted.__doc__.split()) \
        and "applied here" in calculator.quality_adjusted.__doc__
    assert "wave" in calculator.quality_adjusted.__doc__ and "earnings" in calculator.quality_adjusted.__doc__


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


def refused_root(path: str, cell: dict | None = None) -> bool:
    """Refused before its class is asked: under a root no amount is read from, or already
    inside free cash flow. Such a cell is not placed by the table."""
    root = path.split(".")[0]
    return (root in {name for name, _ in calculator.ADJUSTMENT_REFUSED_ROOTS} | set(
        calculator.PRICED_SECTIONS) or root.startswith("market")
        or (cell is not None and calculator.inside_free_cash_flow(path, cell) is not None))


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
            if refused_root(path, cell):
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
            if refused_root(path, cell) or calculator.cell_period(cell) is not None:
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
]


def test_the_table_has_a_planted_path_for_each_entry():
    assert len(ONE_PATH_PER_ENTRY) == len(calculator.CELL_CLASSES)
    for position, ((path, kind), entry) in enumerate(zip(ONE_PATH_PER_ENTRY, calculator.CELL_CLASSES)):
        assert re.fullmatch(entry[1], path), (position, path)
        assert entry[0] == kind, (position, path)
        assert classes_of(path, usd()) == {kind}, (position, path)
        # the cell is put at its path by walking the parts
        parts = path.split(".")
        built: dict = {"period_end": "2026-06-30"}
        cursor = built
        for part in parts[:-1]:
            cursor = cursor.setdefault(part, {})
        cursor[parts[-1]] = usd()
        amount, reason = calculator.adjustment_reading(built, path)
        if kind == "balance":
            assert amount is None and reason.startswith(NOT_A_FLOW + ": " + entry[2]), position
        else:
            assert amount == 1_000_000.0, (position, reason)


def test_a_balance_names_the_table_line_that_says_so():
    """The reason is built from the table: it carries the entry's own line of why."""
    built = {"terms": {"balances_now": {"operating_lease_liability": usd()}}}
    amount, reason = calculator.adjustment_reading(built, "terms.balances_now.operating_lease_liability")
    assert amount is None
    assert calculator.CELL_CLASSES[0][2] in reason and calculator.PLACED_BY_THE_TABLE in reason


def test_a_cell_on_a_published_view_is_never_left_to_the_fallback(published_views):
    for name, held in published_views:
        for path, cell in usd_cells(held):
            if not refused_root(path, cell):
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
                     r"`calculator_field` to be a flow or a change of the\s+period free cash flow "
                     r"covers, never a balance at one date; only `cash_flow` moves free cash flow", text)
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


def test_every_example_path_in_the_adjustments_paragraph_resolves_in_a_committed_view(published_views):
    """A definition's example must be a path some committed run's view holds, with a number."""
    paths = re.findall(r"`((?:terms|earnings_versus_cash|note_tables|ratios)\.[a-z0-9_.]+)`",
                       adjustments_section())
    assert len(paths) >= 5
    for path in paths:
        found = [name for name, held in published_views
                 if isinstance(calculator._cell_at(held, path), dict)
                 and isinstance(calculator._cell_at(held, path).get("value"), (int, float))]
        assert found, path


def test_the_refused_example_is_refused_in_the_run_it_was_published_in():
    """Supplier finance as a balance: DELL and STX each had it applied before this rule; now
    it is refused, and the definition says why and what to do instead."""
    path = "terms.balances_now.supplier_finance_obligation"
    section = adjustments_section()
    assert f"`{path}`" in section and "debt-like" in section and "adjusted debt" in section
    for run in (RUNS / "DELL" / "0001571996-26-000046", RUNS / "STX" / "0001137789-26-000159"):
        amount, reason = calculator.adjustment_reading(view(run), path)
        assert amount is None and NOT_A_FLOW in reason


def contains(published, recomputed, where=""):
    """Every leaf the published file holds is in the recomputed one, equal; the recomputed
    file may hold more (sections and cells added since the run was published)."""
    if isinstance(published, dict):
        assert isinstance(recomputed, dict), where
        for key, value in published.items():
            assert key in recomputed, f"{where}.{key}"
            contains(value, recomputed[key], f"{where}.{key}")
    elif isinstance(published, list):
        assert isinstance(recomputed, list) and len(published) == len(recomputed), where
        for position, (a, b) in enumerate(zip(published, recomputed)):
            contains(a, b, f"{where}.{position}")
    else:
        assert published == recomputed, where


@pytest.mark.parametrize("run", [APPLE, PALO_ALTO], ids=["apple", "palo_alto"])
def test_reading_the_whole_view_changed_no_section_outside_free_cash_flow(run):
    """The calculator now builds one `fields` from every section before free cash flow; each
    published section other than free_cash_flow is still what a recompute prints (the run
    published before four sections were added, so the recompute may hold more, never less).
    With no adjustment, free cash flow's own value is the published one."""
    held = view(run)
    again = calculator_drift.recompute(run, STORE)
    for section in held:
        if section != "free_cash_flow":
            contains(held[section], again[section], section)
    assert (again["free_cash_flow"]["free_cash_flow_quality_adjusted"]["value"]
            == held["free_cash_flow"]["free_cash_flow_quality_adjusted"]["value"])


# --- what the refuter found: free cash flow's own parts, the span, earnings, the plumbing ---------

import functools


@functools.lru_cache(maxsize=None)
def printed(name: str) -> dict:
    """The view of a committed run as today's calculator prints it, note tables included."""
    return calculator_drift.recompute(RUNS / name, STORE)


def refused_with(held: dict, path: str, said: str) -> None:
    amount, reason = calculator.adjustment_reading(held, path)
    assert amount is None and said in reason, (path, amount, reason)


INSIDE = "already inside free cash flow"
OUTSIDE = "not the period free cash flow covers"
CARR_RUN = "CARR/0001783180-26-000032"
AAPL_RUN = "AAPL/0000320193-26-000020-note-tables-2026-10-29"
PALO_RUN = "PANW/0001327567-26-000015-note-tables-2026-11-08"
LFUS_RUN = "LFUS/0001628280-26-050481-note-tables-2026-11-08"
WDC_RUN = "WDC/0001628280-26-029054"
STX_RUN = "STX/0001137789-26-000159"
TTMI_RUN = "TTMI/0001193125-26-335107"


@pytest.mark.parametrize("run, path, concept", [
    # the cells the refuter named, each with the concept the note table tags it with
    (CARR_RUN, "note_tables.tables.notes_61.facts.2", "us-gaap:ShareBasedCompensation"),
    (PALO_RUN, "note_tables.tables.notes_75.facts.0", "us-gaap:PaymentsToAcquireBusinessesGross"),
    (LFUS_RUN, "note_tables.tables.notes_37.facts.0", "us-gaap:PaymentsToAcquireBusinessesNetOfCashAcquired"),
    (WDC_RUN, "note_tables.tables.notes_31.facts.0", "us-gaap:PaymentsToAcquirePropertyPlantAndEquipment"),
    (AAPL_RUN, "note_tables.tables.notes_52.facts.0", "us-gaap:AllocatedShareBasedCompensationExpense"),
    (AAPL_RUN, "note_tables.tables.notes_52.facts.2", "us-gaap:AllocatedShareBasedCompensationExpense"),
])
def test_a_note_table_fact_of_a_part_of_free_cash_flow_is_already_inside_it(run, path, concept):
    held = printed(run)
    assert calculator._cell_at(held, path)["concept"] == concept
    refused_with(held, path, INSIDE)


def test_every_fact_of_apples_share_based_pay_table_is_refused():
    """notes_52 holds the allocated expense and its tax benefit, three months and nine months,
    this year and last: each is refused, by its concept or by its dates."""
    table = printed(AAPL_RUN)["note_tables"]["tables"]["notes_52"]
    assert len(table["facts"]) >= 8
    for position, fact in enumerate(table["facts"]):
        path = f"note_tables.tables.notes_52.facts.{position}"
        assert calculator.adjustment_reading(printed(AAPL_RUN), path)[0] is None, (path, fact["concept"])
    for position in range(len(table["changes"])):
        path = f"note_tables.tables.notes_52.changes.{position}"
        assert calculator.adjustment_reading(printed(AAPL_RUN), path)[0] is None, path


def test_the_quarterly_operating_cash_flow_and_its_history_are_already_inside_free_cash_flow():
    held = printed(AAPL_RUN)
    base = "quarterly_cash_flow_and_accruals.operating_cash_flow_quarterly"
    refused_with(held, base, INSIDE)
    history = calculator._cell_at(held, base)["history"]
    assert len(history) == 8
    for position in range(len(history)):
        refused_with(held, f"{base}.history.{position}", INSIDE)


def test_free_cash_flow_simple_inside_the_cash_runway_is_already_inside_free_cash_flow():
    path = "ratios.liquidity.cash_runway_months.inputs.free_cash_flow_simple"
    held = printed(TTMI_RUN)
    assert calculator._cell_at(held, path)["unit"] == "USD"
    refused_with(held, path, INSIDE)


@pytest.mark.parametrize("path", [
    "terms.trailing_four_quarters.operating_cash_flow", "terms.trailing_four_quarters.capital_expenditure",
    "terms.trailing_four_quarters.share_based_compensation",
    "terms.trailing_four_quarters.operating_cash_flow.parts.this_year_to_date",
    "terms.cash_flow_families.acquisitions", "terms.cash_flow_families.acquisitions.parts.this_year_to_date",
    "quarterly_cash_flow_and_accruals.free_cash_flow_accruals",
    "quarterly_cash_flow_and_accruals.cash_flow_accruals.inputs.operating_cash_flow_discontinued",
    "quarterly_cash_flow_and_accruals.cash_flow_accruals.inputs.operating_cash_flow_of_continuing_operations",
])
def test_each_name_of_a_part_of_free_cash_flow_is_refused_wherever_it_stands(path):
    held = {"period_end": "2026-06-30"}
    node = held
    parts = path.split(".")
    for part in parts[:-1]:
        node = node.setdefault(part, {})
    node[parts[-1]] = usd(period="2025-07-01..2026-06-30")
    refused_with(held, path, INSIDE)


def test_a_ratio_of_cash_flow_to_income_is_not_cash_flow_and_its_net_income_input_stands():
    path = "earnings_versus_cash.operating_cash_flow_over_net_income.inputs.net_income"
    held = {"period_end": "2026-06-30", "earnings_versus_cash": {"operating_cash_flow_over_net_income": {
        "inputs": {"net_income": usd()}}}}
    assert calculator.adjustment_reading(held, path) == (1_000_000.0, None)


def test_the_concepts_inside_free_cash_flow_are_each_refused():
    for concept in ("us-gaap:NetCashProvidedByUsedInOperatingActivities",
                    "us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations",
                    "us-gaap:PaymentsToAcquirePropertyPlantAndEquipment",
                    "us-gaap:PaymentsToAcquireProductiveAssets", "us-gaap:PaymentsForCapitalImprovements",
                    "us-gaap:ShareBasedCompensation", "us-gaap:AllocatedShareBasedCompensationExpense",
                    "us-gaap:PaymentsToAcquireBusinessesNetOfCashAcquired",
                    "us-gaap:PaymentsToAcquireBusinessesGross", "aapl:ShareBasedCompensationOther"):
        held = {"period_end": "2026-06-30", "note_tables": {"tables": {"notes_1": {"facts": [
            usd(unit="iso4217:USD", concept=concept, start="2025-07-01", end="2026-06-30")]}}}}
        refused_with(held, "note_tables.tables.notes_1.facts.0", INSIDE)
    held = {"period_end": "2026-06-30", "note_tables": {"tables": {"notes_1": {"facts": [
        usd(unit="iso4217:USD", concept="us-gaap:PaymentsToAcquireIntangibleAssets",
            start="2025-07-01", end="2026-06-30")]}}}}
    assert calculator.adjustment_reading(held, "note_tables.tables.notes_1.facts.0")[0] == 1_000_000.0


# the span: a year ending at the period's end, or two dates ending at it

def test_stx_changes_a_year_stands_two_years_and_two_flows_do_not():
    """Seagate's note on its supplier finance obligation, the 10-K for the year ended
    2026-07-03 (a 53-week year): the obligation was 400 million at 2026-07-03, 20 at
    2025-06-27 and 50 at 2024-06-28 (companyfacts, through tests/companyfacts_source.py),
    and the increase 1,817 over the year to 2026-07-03 and 1,344 over the year before."""
    cutoff = "2026-08-04"
    at = lambda day: source.one_value("STX", "SupplierFinanceProgramObligation", day, cutoff)
    assert (at("2026-07-03"), at("2025-06-27"), at("2024-06-28")) == (400e6, 20e6, 50e6)
    increase = lambda span: source.one_value("STX", "SupplierFinanceProgramObligationIncrease", span, cutoff)
    assert (increase("2025-06-28..2026-07-03"), increase("2024-06-29..2025-06-27")) == (1_817e6, 1_344e6)
    held = printed(STX_RUN)
    assert held["period_end"] == "2026-07-03"
    two_years = "note_tables.tables.notes_91.changes.0"
    one_year = "note_tables.tables.notes_91.changes.1"
    two_flows = "note_tables.tables.notes_91.changes.2"
    assert calculator._cell_at(held, two_years)["value"] == at("2026-07-03") - at("2024-06-28") == 350e6
    assert calculator._cell_at(held, one_year)["value"] == at("2026-07-03") - at("2025-06-27") == 380e6
    assert calculator._cell_at(held, two_flows)["value"] == (
        increase("2025-06-28..2026-07-03") - increase("2024-06-29..2025-06-27")) == 473e6
    refused_with(held, two_years, OUTSIDE)
    refused_with(held, two_flows, "a change between two spans")
    assert calculator.adjustment_reading(held, one_year) == (380e6, None)


def test_palo_altos_prior_year_columns_are_refused_and_the_latest_ones_stand():
    """notes_42 (contingent consideration) states four columns: three and nine months ended
    April 30, 2026 and 2025. The 2025 ones start 2025-02-01 and 2024-08-01 and end 2025-04-30;
    the nine months of 2026 start 2025-08-01 and the three months 2026-02-01, both ending at
    the period's end 2026-04-30."""
    held = printed(PALO_RUN)
    assert held["period_end"] == "2026-04-30"
    for position, fact in enumerate(held["note_tables"]["tables"]["notes_42"]["facts"]):
        path = f"note_tables.tables.notes_42.facts.{position}"
        amount, reason = calculator.adjustment_reading(held, path)
        if fact.get("start") == "2024-08-01" or fact.get("end") == "2025-04-30" or \
                fact.get("instant", "").startswith(("2025", "2024")):
            assert amount is None and OUTSIDE in reason or "balance" in reason, (path, reason)
        if fact.get("end") == "2026-04-30" and fact.get("start") in ("2026-02-01", "2025-08-01") \
                and not fact["concept"].endswith("Purchases"):
            assert amount == fact["value"], (path, reason)
    assert calculator.adjustment_reading(held, "note_tables.tables.notes_42.facts.8")[0] == -110e6
    refused_with(held, "note_tables.tables.notes_42.facts.11", OUTSIDE)      # 2024-08-01..2025-04-30
    refused_with(held, "note_tables.tables.notes_42.facts.9", OUTSIDE)       # 2025-02-01..2025-04-30


@pytest.mark.parametrize("path", [
    "terms.trailing_four_quarters_a_year_earlier.revenue",
    "terms.trailing_four_quarters.revenue.parts.prior_fiscal_year",
    "terms.trailing_four_quarters.revenue.parts.prior_year_to_date",
    "ratios.growth.revenue.trailing_four_quarters.inputs.before",
    "contract_liabilities_and_billings.billings_a_year_earlier",
    "receivables_extension.days_sales_outstanding_index.inputs.revenue_a_year_earlier",
])
def test_a_prior_year_comparative_of_the_calculator_is_refused_as_not_the_period(path):
    held = printed("NVDA/0001045810-26-000075")
    assert calculator._cell_at(held, path)["unit"] == "USD"
    refused_with(held, path, OUTSIDE)


def test_a_history_entry_is_refused_as_not_the_period():
    held = {"period_end": "2026-06-30", "x": {"history": {"revenue": usd(), "0": {"revenue": usd()}}}}
    refused_with(held, "x.history.revenue", OUTSIDE)
    refused_with(held, "x.history.0.revenue", OUTSIDE)
    assert calculator.adjustment_reading({**held, "x": {"revenue": usd()}}, "x.revenue")[0] == 1_000_000.0


@pytest.mark.parametrize("cell, said", [
    ({"from": {"instant": "2025-06-30"}}, "half of a change"),                       # from and no to
    ({"to": {"instant": "2026-06-30"}}, "half of a change"),                         # to and no from
    ({"from": "2025-06-30", "to": "2026-06-30"}, "half of a change"),                # not periods
    ({"from": {"start": "2024-07-01", "end": "2025-06-30"},
      "to": {"start": "2025-07-01", "end": "2026-06-30"}}, "a change between two spans"),
    ({"from": {"instant": "2024-06-30"}, "to": {"instant": "2026-06-30"}}, OUTSIDE),     # two years
    ({"from": {"instant": "2025-06-30"}, "to": {"instant": "2026-03-31"}}, OUTSIDE),     # not to the period end
    ({"from": {"instant": "2026-06-30"}, "to": {"instant": "2026-06-30"}}, "same day"),
    ({"from": {"instant": "not a date"}, "to": {"instant": "2026-06-30"}}, "not dates"),
    ({"start": "2025-06-30", "end": "2026-07-01"}, OUTSIDE),                          # ends after
    ({"start": "2024-07-01", "end": "2026-06-30"}, "more than 371"),                  # two years
    ({"start": "2026-06-30", "end": "2026-06-30"}, None),                             # a day at the period end
    ({"start": "bad", "end": "2026-06-30"}, "not two dates"),
    ({"period": "2025-07-01..2026-03-31"}, OUTSIDE),
])
def test_the_span_rule_on_planted_cells(cell, said):
    held = {"period_end": "2026-06-30", "x": {"cell": {**usd(), **cell}}}
    amount, reason = calculator.adjustment_reading(held, "x.cell")
    if said is None:
        assert amount == 1_000_000.0
    else:
        assert amount is None and said in reason, reason


def test_a_year_of_371_days_stands_and_one_of_372_does_not():
    ok = {"period_end": "2026-07-03", "x": {"c": usd(period="2025-06-27..2026-07-03")}}     # 371 days
    long = {"period_end": "2026-07-03", "x": {"c": usd(period="2025-06-26..2026-07-03")}}   # 372
    assert calculator.adjustment_reading(ok, "x.c")[0] == 1_000_000.0
    refused_with(long, "x.c", OUTSIDE)


def test_a_view_with_no_period_end_holds_nothing_to_a_span():
    held = {"x": {"c": usd(period="2025-07-01..2026-06-30")}}
    refused_with(held, "x.c", "names no period end")


# earnings never moves free cash flow

def test_the_calculator_lists_an_earnings_adjustment_and_applies_it_to_nothing():
    out = calculator.quality_adjusted(
        {"value": 100.0}, {"value": 10.0}, {"value": 0.0, "formula": "x"},
        [adjustment("terms.trailing_four_quarters.revenue", "reduce", "earnings"),
         adjustment("terms.trailing_four_quarters.net_income", "increase", "cash_flow")],
        {**PLANTED, "terms": {"trailing_four_quarters": {"revenue": usd(), "net_income": usd()}}})
    assert out["value"] == 100.0 - 10.0 + 1_000_000.0
    assert [r["calculator_field"] for r in out["adjustments_applied"]] == ["terms.trailing_four_quarters.net_income"]
    earnings, = out["adjustments_to_earnings"]
    assert earnings["calculator_field"] == "terms.trailing_four_quarters.revenue"
    assert earnings["amount"] == 1_000_000.0
    assert earnings["applied_to"].startswith("nothing until normalised operating income")
    assert "before" not in earnings and "after" not in earnings


def test_an_adjustment_of_neither_target_is_refused_by_the_calculator():
    out = calculator.quality_adjusted(
        {"value": 100.0}, {"value": 10.0}, {"value": 0.0, "formula": "x"},
        [adjustment("terms.trailing_four_quarters.revenue", "reduce", "debt")], PLANTED)
    assert out["value"] == 90.0 and out["adjustments_applied"] == []
    assert out["adjustments_refused"][0]["reason"] == "applies_to is not 'cash_flow' or 'earnings'"


# the four newer sections reach the calculator's fields

@pytest.mark.parametrize("path", [
    "quarterly_cash_flow_and_accruals.balance_sheet_accruals.inputs.change_in_cash",
    "receivables_extension.days_sales_outstanding_index.inputs.revenue",
    "contract_liabilities_and_billings.billings",
    "inventory_composition_and_growth_gap.inventory_growth_minus_revenue_growth.inputs.revenue_growth.inputs.now",
    "concentration.facts.0.value",
])
def test_every_section_of_the_view_reaches_the_calculators_adjustments(path):
    """NVIDIA's run, each of the four sections added since most runs were published: the
    adjustment naming a cell of it is applied by `calculate`, to the cell's value."""
    run = RUNS / "NVDA" / "0001045810-26-000075"
    out = calculator.calculate(**calculator_drift.trigger(run), fixtures_root=STORE, bundle=run,
                               accounting={"adjustments": [adjustment(path)]})
    quality = out["free_cash_flow"]["free_cash_flow_quality_adjusted"]
    cell = calculator._cell_at(out, path)
    if path.startswith("concentration"):                  # a percentage, not a dollar cell
        assert quality["adjustments_applied"] == [] and "not a dollar cell" in quality["adjustments_refused"][0]["reason"]
        return
    row, = quality["adjustments_applied"]
    assert quality["adjustments_refused"] == [] and row["signed_value"] == cell["value"] != 0


def test_the_calculators_fields_carry_every_section_before_free_cash_flow():
    """The sections the view holds, as `calculate` builds its fields: a path in each is read."""
    run = RUNS / "NVDA" / "0001045810-26-000075"
    out = calculator.calculate(**calculator_drift.trigger(run), fixtures_root=STORE, bundle=run)
    for section in ("terms", "ratios", "ebit", "tax_rate", "earnings_versus_cash",
                    "quarterly_cash_flow_and_accruals", "receivables_extension",
                    "contract_liabilities_and_billings", "inventory_composition_and_growth_gap",
                    "concentration", "note_tables", "trend_table"):
        assert section in out, section


# the class table against the filing's own period types (companyfacts, through the second reader)

def period_type(ticker: str, tag: str) -> str:
    """`duration` if companyfacts rows for the tag carry a start, `instant` if an end alone;
    a tag whose rows are of both kinds fails."""
    kinds = {"duration" if row.get("start") else "instant"
             for row in source.rows(ticker, tag, every_form=True)}
    assert len(kinds) == 1, (ticker, tag, kinds)
    return kinds.pop()


# One committed cell with no period of its own for each entry of `CELL_CLASSES`, in order, the
# ticker whose companyfacts holds its source, and the tags it came from (read in the cell's
# formula and ids, or, for a change worked out from a balance, in its sibling's), and the class
# the table must give it: a duration is a flow, an instant a balance, a change of instants a change.
FROM_THE_FILING = [
    (AAPL_RUN, "AAPL", "terms.debt_now.parts.debt_current", ("LongTermDebtCurrent", "CommercialPaper"), "balance"),
    ("NVDA/0001045810-26-000075", "NVDA", "quarterly_cash_flow_and_accruals.balance_sheet_accruals.inputs."
     "change_in_debt_in_current_liabilities.inputs.now", ("DebtCurrent",), "balance"),
    (AAPL_RUN, "AAPL", "earnings_versus_cash.working_capital.receivables.balance_sheet_change",
     ("AccountsReceivableNetCurrent",), "change"),
    (AAPL_RUN, "AAPL", "earnings_versus_cash.working_capital.receivables.share_of_net_income.inputs.change",
     ("AccountsReceivableNetCurrent",), "change"),           # its formula: receivables now - a year earlier
    (AAPL_RUN, "AAPL", "terms.trailing_four_quarters.operating_income", ("OperatingIncomeLoss",), "flow"),
    (AAPL_RUN, "AAPL", "ratios.profitability.gross_margin.inputs.revenue",
     ("RevenueFromContractWithCustomerExcludingAssessedTax",), "flow"),
    ("CIEN/0001628280-26-040767-note-tables-2026-11-14", "CIEN",
     "ratios.solvency.ebitda.inputs.depreciation_and_amortization.parts.prior_fiscal_year",
     ("Depreciation", "AmortizationOfIntangibleAssets"), "flow"),
    (AAPL_RUN, "AAPL", "earnings_versus_cash.working_capital.receivables.cash_flow_statement_change",
     ("IncreaseDecreaseInAccountsReceivable",), "flow"),
    (AAPL_RUN, "AAPL", "ratios.growth.revenue.trailing_four_quarters.inputs.now",
     ("RevenueFromContractWithCustomerExcludingAssessedTax",), "flow"),
]


@pytest.mark.parametrize("position", range(9))
def test_each_table_entry_gives_a_cell_the_class_of_its_tag_in_the_filing(position):
    run, ticker, path, tags, kind = FROM_THE_FILING[position]
    entry_kind, pattern, _ = calculator.CELL_CLASSES[position]
    held = printed(run)
    cell = calculator._cell_at(held, path)
    assert calculator.cell_period(cell) is None              # no period of its own: the table decides
    assert re.fullmatch(pattern, path)
    placing = [i for i, (_, other, _) in enumerate(calculator.CELL_CLASSES) if re.fullmatch(other, path)]
    assert position in placing and {calculator.CELL_CLASSES[i][0] for i in placing} == {entry_kind}
    types = {period_type(ticker, tag) for tag in tags}
    assert len(types) == 1
    expected = {"duration": "flow", "instant": "balance"}[types.pop()]
    if kind == "change":                                      # a change between two balances
        assert expected == "balance"
        expected = "change"
    assert kind == expected
    assert calculator.cell_class(path, cell)[0] == expected == entry_kind
    for tag in tags:
        assert tag in json.dumps(held)                        # the tag is one the view cites


def test_the_definition_says_the_cash_flow_rule_the_span_rule_and_whose_view_an_example_is():
    section = adjustments_section()
    for sentence in (
            "Nor may it be one of free cash flow's own parts, which are already inside it: operating "
            "cash flow, capital expenditure (payments for property and equipment), share-based "
            "compensation and acquisitions",
            "ends at the filing's period end and lasts no more than a year (a 53-week year is allowed)",
            "A prior-year column, a history entry, a change between two spans and a change over two "
            "years are dropped as not the period free cash flow covers",
            "Only a `cash_flow` adjustment moves free cash flow",
            "listed with its amount, and it is applied to nothing until normalised operating income "
            "exists in the next wave",
            "`note_tables.tables.notes_38.changes.0` in Apple's view",
            "`note_tables.tables.notes_42.facts.14` in Palo Alto's view"):
        assert sentence in section, sentence
    # the example that names a view resolves in that view, to the cell the sentence describes
    apple = calculator._cell_at(view(APPLE), "note_tables.tables.notes_38.changes.0")
    assert apple["concept"] == "us-gaap:IntangibleAssetsGrossExcludingGoodwill"
    palo = calculator._cell_at(view(PALO_ALTO), "note_tables.tables.notes_42.facts.14")
    assert palo["concept"].endswith("LiabilityPayment")
