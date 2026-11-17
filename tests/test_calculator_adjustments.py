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
import datetime as dt
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
EARNINGS_LABEL = ("not to free cash flow; the valuation applies it "
                  "(once, or as a margin cut where it recurs)")


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


# The trailing year free cash flow covers, as a view prints it: the prior year to date ended
# 2025-06-30, so the year runs 2025-07-01..2026-06-30 (a planted view that names none is given it).
YEAR_CELL = {"operating_cash_flow": {"parts": {"prior_year_to_date": {"period": "2025-01-01..2025-06-30"}}}}


def with_year(held: dict) -> dict:
    out = dict(held)
    terms = dict(out.get("terms") or {})
    trailing = dict(terms.get("trailing_four_quarters") or {})
    trailing.setdefault("operating_cash_flow", YEAR_CELL["operating_cash_flow"])
    terms["trailing_four_quarters"] = trailing
    out["terms"] = terms
    return out


def reading(held: dict, path, recurs: bool = False, applies_to: str = "cash_flow"):
    """`calculator.adjustment_reading`, a planted view first given the trailing year."""
    return calculator.adjustment_reading(with_year(held), path, recurs, applies_to)


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
]


@pytest.mark.parametrize("run, path, amount, kind, period", READ_BY_EYE,
                         ids=[row[1].replace("note_tables.tables.", "") for row in READ_BY_EYE])
def test_a_flow_or_a_change_in_a_note_table_is_an_amount(run, path, amount, kind, period):
    held = view(run)
    cell = calculator._cell_at(held, path)
    assert cell["value"] == amount                      # the filing's number, as read by eye
    assert calculator.cell_period(cell) == (kind, period)
    assert reading(held, path) == (amount, None)
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
    amount, reason = reading(held, path)
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


def test_apples_working_capital_changes_move_free_cash_flow_by_their_amounts():
    """Apple's receivables rose from 27,557 (2025-06-28) to 31,398 (2026-06-27) million, and its
    accounts payable from 50,374 to 64,525 (companyfacts through the second reader, cutoff
    2026-07-31): 3,841 and 14,151. Reducing free cash flow by the first, 122,977 - 3,841 = 119,136;
    increasing it by the second, 119,136 + 14,151 = 133,287."""
    cutoff = "2026-07-31"
    rise = lambda tag: (source.one_value("AAPL", tag, "2026-06-27", cutoff)
                        - source.one_value("AAPL", tag, "2025-06-28", cutoff))
    assert (rise("AccountsReceivableNetCurrent"), rise("AccountsPayableCurrent")) == (
        3_841 * MILLION, 14_151 * MILLION)
    receivables = "earnings_versus_cash.working_capital.receivables.balance_sheet_change"
    payables = "earnings_versus_cash.working_capital.accounts_payable.balance_sheet_change"
    one = final_with(APPLE, [adjustment(receivables)])
    assert one["adjustments_refused"] == [] and one["adjustments_to_earnings"] == []
    row, = one["adjustments_applied"]
    assert (row["amount"], row["before"], row["after"]) == (
        3_841 * MILLION, 122_977 * MILLION, 119_136 * MILLION)
    assert one["value"] == 119_136 * MILLION
    # the row carries the cell's signed value, its class and its span beside the amount: the two
    # balance dates its inputs carry, a year apart
    assert (row["signed_value"], row["class"], row["direction"], row["applies_to"]) == (
        3_841 * MILLION, "change", "reduce", "cash_flow")
    assert row["period"] is None
    assert row["its_own_span"].startswith(
        "no dates of its own; its balances, 2025-06-28 and 2026-06-27, are the year's")
    # Apple's trailing year starts the day after the prior year to date ends (2025-06-28)
    assert row["free_cash_flow_covers"] == "the four quarters 2025-06-29..2026-06-27"
    assert row["recurs"] is False
    both = final_with(APPLE, [adjustment(receivables), adjustment(payables, "increase")])
    assert [(r["before"], r["after"]) for r in both["adjustments_applied"]] == [
        (122_977 * MILLION, 119_136 * MILLION), (119_136 * MILLION, 133_287 * MILLION)]
    assert both["value"] == 133_287 * MILLION


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
    assert row["free_cash_flow_covers"] == "the four quarters 2025-05-01..2026-04-30"
    assert row["its_own_span"] == ("2025-08-01..2026-04-30 within the four quarters ending 2026-04-30")
    assert [(r["calculator_field"], r["amount"], r["signed_value"], r["class"], r["period"],
             r["applied_to"] == EARNINGS_LABEL) for r in out["adjustments_to_earnings"]] == [
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
    assert reading(PLANTED, path) == (amount, None)


@pytest.mark.parametrize("path, said", [
    ("terms.balances_now.receivables", "one date, 2026-06-30"),                     # a period of one date
    ("terms.balances_now.operating_lease_liability", "a line of the balance sheet"),  # table: a balance
    ("terms.debt_now.lines.0", "one date, 2026-06-30"),                             # a debt line is a balance
    ("note_tables.tables.notes_1.facts.1", "one date, 2026-04-30"),                 # an instant
])
def test_a_balance_at_one_date_is_refused_with_its_reason(path, said):
    amount, reason = reading(PLANTED, path)
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
    assert reading(PLANTED, path) == (None, reason)


def test_the_sections_the_view_removes_are_each_refused():
    """Every section `filings_only` removes is a root no amount is read from, with no list
    kept apart from `PRICED_SECTIONS`."""
    for section in calculator.PRICED_SECTIONS:
        fields = {section: {"x": usd(period="2025-07-01..2026-06-30")}}
        amount, reason = reading(fields, f"{section}.x")
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
    amount, reason = reading(PLANTED, path)
    assert amount is None and said in reason


def test_a_path_that_is_not_a_string_names_nothing():
    for path in (None, 3, ["terms"], {"terms": 1}):
        assert reading(PLANTED, path)[0] is None


def test_a_cell_with_periods_of_two_kinds_is_refused_not_guessed():
    fields = {"terms": {"x": usd(period="2026-06-30", start="2025-07-01", end="2026-06-30")}}
    amount, reason = reading(fields, "terms.x")
    assert amount is None and "more than one kind" in reason


def test_a_dollar_cell_whose_value_is_not_a_number_is_refused():
    fields = {"period_end": "2026-06-30",
              "terms": {"x": {"value": None, "unit": "USD", "period": "2025-07-01..2026-06-30"},
                        "y": {"value": True, "unit": "USD", "period": "2025-07-01..2026-06-30"},
                        "z": {"value": float("inf"), "unit": "USD", "period": "2025-07-01..2026-06-30"}}}
    for name in "xyz":
        assert reading(fields, f"terms.{name}") == (None, "its value is not a number")


def test_a_unit_that_is_not_a_dollar_is_not_one_even_in_the_filings_spelling():
    for unit in ("iso4217:EUR", "shares", "xbrli:shares", "usd", "USD/shares"):
        fields = {"terms": {"x": {"value": 5.0, "unit": unit, "period": "2025-07-01..2026-06-30"}}}
        assert reading(fields, "terms.x")[0] is None, unit


def test_a_list_is_indexed_by_ascii_digits_alone_and_nothing_raises():
    """The reading the old gate's test held for a debt line, held here for a flow: '²' and
    '①' are digits to `str.isdigit` and not to `int`, and such a part names nothing."""
    fields = {"period_end": "2026-06-30", "terms": {"lines": [usd(period="2025-07-01..2026-06-30")]}}
    assert reading(fields, "terms.lines.0") == (1_000_000.0, None)
    for part in ("²", "①", "٣", "-1", "00x"):
        assert reading(fields, f"terms.lines.{part}")[0] is None, part


def test_a_period_decides_before_the_table_does():
    """A cell under a name the table calls a balance, with a duration of its own, is a flow:
    the cell says what it is."""
    fields = {"period_end": "2026-06-30",
              "terms": {"balances_now": {"x": usd(period="2025-07-01..2026-06-30")}}}
    assert reading(fields, "terms.balances_now.x")[0] == 1_000_000.0


def test_the_unit_may_be_the_calculators_or_the_filings():
    for unit in ("USD", "iso4217:USD"):
        fields = {"period_end": "2026-06-30", "terms": {"x": usd(unit=unit, period="2025-07-01..2026-06-30")}}
        assert reading(fields, "terms.x") == (1_000_000.0, None)


# --- the gate and the calculator read one rule --------------------------------------------------

@pytest.mark.parametrize("path", [
    "terms.balances_now.receivables", "free_cash_flow.free_cash_flow_simple", "valuation.base",
    "ratios.liquidity.current_ratio", "terms.nowhere", "mystery.number",
    "terms.trailing_four_quarters.revenue"])
def test_the_gate_and_the_calculator_say_the_same_thing(path):
    amount, reason = reading(PLANTED, path)
    gate = analysis_check.adjustment_problem(with_year(PLANTED))(
        {"direction": "reduce", "applies_to": "cash_flow", "calculator_field": path, "quote": "q"})
    if amount is not None:
        assert gate is None
    else:
        assert gate == f"calculator_field {path!r} cannot be an adjustment's amount: {reason}"


def test_the_gate_still_checks_what_it_checked_before():
    problem = analysis_check.adjustment_problem(with_year(PLANTED))
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
                           with_year(PLANTED))
    assert out["value"] == 100.0 - 10.0 + 1_000_000.0
    assert [(r["after"]) for r in out["adjustments_applied"]] == [1_000_090.0]
    reasons = {row["calculator_field"]: row["reason"] for row in out["adjustments_refused"]}
    assert reasons["terms.balances_now.receivables"] == (
        "'terms.balances_now.receivables' cannot be an adjustment's amount: "
        + reading(PLANTED, "terms.balances_now.receivables")[1])
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
                assert reading(held, path)[0] is None, (name, path)
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
        amount, reason = reading(built, path)
        if kind == "balance":
            assert amount is None and reason.startswith(NOT_A_FLOW + ": " + entry[2]), position
        else:
            assert amount == 1_000_000.0, (position, reason)


def test_a_balance_names_the_table_line_that_says_so():
    """The reason is built from the table: it carries the entry's own line of why."""
    built = {"terms": {"balances_now": {"operating_lease_liability": usd()}}}
    amount, reason = reading(built, "terms.balances_now.operating_lease_liability")
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


@pytest.mark.parametrize("shape, path, run, kind", [
    ("note_tables.tables.notes_<n>.facts.<k>", "note_tables.tables.notes_42.facts.14",
     "PANW/0001327567-26-000015-note-tables-2026-11-08", "flow"),
    ("note_tables.tables.notes_<n>.changes.<k>", "note_tables.tables.notes_91.changes.1", "STX/0001137789-26-000159", "change"),
    ("earnings_versus_cash.working_capital.receivables.balance_sheet_change",
     "earnings_versus_cash.working_capital.receivables.balance_sheet_change",
     "DELL/0001571996-26-000046", "change"),
])
def test_each_example_in_the_definition_has_an_instance_in_a_run_as_printed_today_that_is_accepted(shape, path, run, kind):
    assert f"`{shape}`" in adjustments_section()
    assert shaped(shape).fullmatch(path)
    held = printed(run)
    cell = calculator._cell_at(held, path)
    assert isinstance(cell, dict) and "value" in cell
    assert calculator.cell_class(path, cell)[0] == kind
    assert reading(held, path)[0] == cell["value"]


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
    amount, reason = reading(held, path)
    assert amount is None and said in reason, (path, amount, reason)


INSIDE = "already inside free cash flow"
OUTSIDE = "not the period free cash flow covers"
BALANCES_NOT = "its balances are not the period's"
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


def test_apples_share_based_pay_table_refuses_the_expense_and_not_the_tax_benefit():
    """notes_52 holds the allocated expense (an exact concept of the table) and its tax benefit
    (another quantity: no source says it is inside free cash flow). The expense facts are
    refused as inside free cash flow; the tax benefit is not refused for that reason, and the
    ones of the period free cash flow covers (three months and nine months to 2026-06-27)
    stand."""
    held = printed(AAPL_RUN)
    table = held["note_tables"]["tables"]["notes_52"]
    seen = {"expense": 0, "benefit": 0}
    for position, fact in enumerate(table["facts"]):
        path = f"note_tables.tables.notes_52.facts.{position}"
        amount, reason = reading(held, path)
        if fact["concept"] == "us-gaap:AllocatedShareBasedCompensationExpense":
            seen["expense"] += 1
            assert amount is None and INSIDE in reason, (path, reason)
        else:
            assert fact["concept"].endswith("TaxBenefitFromCompensationExpense"), fact["concept"]
            seen["benefit"] += 1
            assert INSIDE not in (reason or ""), (path, reason)
    assert seen == {"expense": 4, "benefit": 4}
    # the benefit of the nine months to the period end stands; last year's is a prior-year column
    assert reading(held, "note_tables.tables.notes_52.facts.6")[0] == fact_value(table, 6) == 3_217e6
    refused_with(held, "note_tables.tables.notes_52.facts.7", OUTSIDE)


def fact_value(table: dict, position: int) -> float:
    return table["facts"][position]["value"]


@pytest.mark.parametrize("run, table, position, concept", [
    # the lens's and refuter's cells: lines that name share-based compensation and are other things
    ("FTNT/0001262039-26-000021", "notes_103", 4, "us-gaap:AdjustmentsRelatedToTaxWithholdingForShareBasedCompensation"),
    (CARR_RUN, "notes_61", 4, "us-gaap:EmployeeServiceShareBasedCompensationCashFlowEffectCashUsedToSettleAwards"),
    (STX_RUN, "notes_144", 4, "us-gaap:IncomeTaxReconciliationNondeductibleExpenseShareBasedCompensationCost"),
    ("CIEN/0001628280-26-040767", "notes_132", 28,
     "us-gaap:EmployeeServiceShareBasedCompensationAllocationOfRecognizedPeriodCostsCapitalizedAmount"),
    (AAPL_RUN, "notes_52", 4, "us-gaap:EmployeeServiceShareBasedCompensationTaxBenefitFromCompensationExpense"),
])
def test_a_line_that_names_share_based_pay_but_is_another_quantity_is_not_refused_as_inside(run, table, position, concept):
    held = printed(run)
    path = f"note_tables.tables.{table}.facts.{position}"
    assert calculator._cell_at(held, path)["concept"] == concept
    assert INSIDE not in (reading(held, path)[1] or "")


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
    assert reading(held, path) == (1_000_000.0, None)


def a_fact(concept: str) -> dict:
    return {"period_end": "2026-06-30", "note_tables": {"tables": {"notes_1": {"facts": [
        usd(unit="iso4217:USD", concept=concept, start="2025-07-01", end="2026-06-30")]}}}}


@pytest.mark.parametrize("concept", [
    "us-gaap:NetCashProvidedByUsedInOperatingActivities",
    "us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations",
    "us-gaap:PaymentsToAcquirePropertyPlantAndEquipment",
    "us-gaap:PaymentsToAcquireProductiveAssets", "us-gaap:PaymentsForCapitalImprovements",
    "us-gaap:ShareBasedCompensation", "us-gaap:AllocatedShareBasedCompensationExpense",
    "us-gaap:PaymentsToAcquireBusinessesNetOfCashAcquired", "us-gaap:PaymentsToAcquireBusinessesGross",
    # goodwill acquired in the period carries acquisitions (changes in the carrying amounts of
    # property and of goodwill are held by the asset tests below)
    "us-gaap:GoodwillAcquiredDuringPeriod"])
def test_the_concepts_inside_free_cash_flow_are_each_refused(concept):
    refused_with(a_fact(concept), "note_tables.tables.notes_1.facts.0", INSIDE)


@pytest.mark.parametrize("concept", [
    # lines inside operating cash flow stay adjustable: a legitimate analytic choice
    "us-gaap:NetIncomeLoss", "us-gaap:DepreciationDepletionAndAmortization",
    "us-gaap:IncreaseDecreaseInAccountsReceivable",
    # lines that name share-based compensation and are other quantities
    "us-gaap:EmployeeServiceShareBasedCompensationTaxBenefitFromCompensationExpense",
    "us-gaap:AdjustmentsRelatedToTaxWithholdingForShareBasedCompensation",
    "us-gaap:AllocatedShareBasedCompensationExpenseNetOfTax", "aapl:ShareBasedCompensationOther",
    "us-gaap:GoodwillGross", "us-gaap:Goodwill"])
def test_a_line_inside_operating_cash_flow_or_another_quantity_is_not_refused_as_inside(concept):
    assert reading(a_fact(concept), "note_tables.tables.notes_1.facts.0") == (1_000_000.0, None)


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
    refused_with(held, two_years, BALANCES_NOT)
    refused_with(held, two_flows, "a change between two spans")
    assert reading(held, one_year) == (380e6, None)


# notes_42's eighteen facts, each pinned: the contingent consideration table's four columns (three
# and nine months ended April 30, 2026 and 2025) for four rows, and the balances at their dates.
PALO_NOTES_42 = {
    **{i: "balance" for i in (0, 1, 2, 3, 16, 17)},     # liability at 2026-01-31, 2025-01-31, 2025-07-31, 2024-07-31, 2026-04-30, 2025-04-30
    **{i: "stands" for i in (4, 6, 8, 10, 12, 14)},     # purchases, gain or loss, payments: 2026-02-01..04-30 and 2025-08-01..2026-04-30
    **{i: "prior year" for i in (5, 7, 9, 11, 13, 15)}, # the same rows for 2025-02-01..04-30 and 2024-08-01..2025-04-30
}


def test_palo_altos_prior_year_columns_are_refused_one_by_one_and_the_latest_stand():
    held = printed(PALO_RUN)
    assert held["period_end"] == "2026-04-30"
    facts = held["note_tables"]["tables"]["notes_42"]["facts"]
    assert len(facts) == len(PALO_NOTES_42) == 18
    for position, how in PALO_NOTES_42.items():
        path = f"note_tables.tables.notes_42.facts.{position}"
        amount, reason = reading(held, path)
        fact = facts[position]
        if how == "balance":
            assert "instant" in fact and amount is None and NOT_A_FLOW in reason, (path, reason)
        elif how == "stands":
            assert fact["end"] == "2026-04-30" and fact["start"] in ("2026-02-01", "2025-08-01"), path
            assert amount == fact["value"], (path, reason)
        else:
            assert fact["end"] == "2025-04-30" and fact["start"] in ("2025-02-01", "2024-08-01"), path
            assert amount is None and OUTSIDE in reason and "ends 2025-04-30" in reason, (path, reason)
    assert reading(held, "note_tables.tables.notes_42.facts.8")[0] == -110e6


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
    assert reading({**held, "x": {"revenue": usd()}}, "x.revenue")[0] == 1_000_000.0


@pytest.mark.parametrize("cell, said", [
    ({"from": {"instant": "2025-06-30"}}, "half of a change"),                       # from and no to
    ({"to": {"instant": "2026-06-30"}}, "half of a change"),                         # to and no from
    ({"from": "2025-06-30", "to": "2026-06-30"}, "half of a change"),                # not periods
    ({"from": {"start": "2024-07-01", "end": "2025-06-30"},
      "to": {"start": "2025-07-01", "end": "2026-06-30"}}, "a change between two spans"),
    ({"from": {"instant": "2024-06-30"}, "to": {"instant": "2026-06-30"}}, BALANCES_NOT),     # two years
    ({"from": {"instant": "2025-06-30"}, "to": {"instant": "2026-03-31"}}, BALANCES_NOT),     # not to the period end
    ({"from": {"instant": "2026-06-30"}, "to": {"instant": "2026-06-30"}}, "not in order"),
    ({"from": {"instant": "not a date"}, "to": {"instant": "2026-06-30"}}, "not dates"),
    ({"start": "2025-06-30", "end": "2026-07-01"}, OUTSIDE),                          # ends after
    ({"start": "2024-07-01", "end": "2026-06-30"}, "before 2025-07-01"),              # two years
    ({"start": "2026-06-30", "end": "2026-06-30"}, None),                             # a day at the period end
    ({"start": "2025-06-30", "end": "2026-06-30"}, "before 2025-07-01"),              # a day before the year
    ({"start": "2025-07-01", "end": "2026-06-30"}, None),                             # the year itself
    ({"from": {"instant": "2025-06-30"}, "to": {"instant": "2026-06-30"}}, None),      # the day before the year
    ({"from": {"instant": "2025-06-29"}, "to": {"instant": "2026-06-30"}}, "before 2025-06-30"),
    ({"start": "bad", "end": "2026-06-30"}, "not two dates"),
    ({"period": "2025-07-01..2026-03-31"}, OUTSIDE),
])
def test_the_span_rule_on_planted_cells(cell, said):
    held = {"period_end": "2026-06-30", "x": {"cell": {**usd(), **cell}}}
    amount, reason = reading(held, "x.cell")
    if said is None:
        assert amount == 1_000_000.0
    else:
        assert amount is None and said in reason, reason


def view_with_year(period_end: str, prior_year_to_date: str, **sections) -> dict:
    return {"period_end": period_end, "terms": {"trailing_four_quarters": {"operating_cash_flow": {
        "parts": {"prior_year_to_date": {"period": prior_year_to_date}}}}}, **sections}


def test_seagates_year_is_read_from_the_view_and_a_day_earlier_is_refused():
    """Seagate's 10-K for the year ended 2026-07-03 prints one fiscal year, 2025-06-28..2026-07-03
    (53 weeks, the first day the day after the 2025-06-27 year end): the filing's own year, read by
    eye in its cash flow statement's column heading. A flow of that year stands; one starting a
    day earlier does not; a change from the 2025-06-27 balance sheet date stands, from the day
    before that does not."""
    held = printed(STX_RUN)
    assert calculator.trailing_year_start(held) == dt.date(2025, 6, 28)
    pe = "2026-07-03"
    year = view_with_year(pe, "2025-01-01..2025-06-27", x={
        "year": usd(period="2025-06-28..2026-07-03"), "early": usd(period="2025-06-27..2026-07-03"),
        "change": {**usd(), "from": {"instant": "2025-06-27"}, "to": {"instant": pe}},
        "change_early": {**usd(), "from": {"instant": "2025-06-26"}, "to": {"instant": pe}}})
    assert calculator.trailing_year_start(year) == dt.date(2025, 6, 28)
    assert reading(year, "x.year") == (1_000_000.0, None)
    refused_with(year, "x.early", OUTSIDE)
    assert reading(year, "x.change") == (1_000_000.0, None)
    refused_with(year, "x.change_early", BALANCES_NOT)


def test_apples_year_is_364_days_and_a_flow_starting_eight_days_before_is_refused():
    """Apple's 10-Q for the quarter ended 2026-06-27: the prior year to date ended 2025-06-28 (the
    nine months of 2025 in the 10-Q's own column), so the trailing year is 2025-06-29..2026-06-27,
    364 days. A flow of 2025-06-21..2026-06-27 (eight days earlier, 371 days, which a limit of
    a 53-week year would have let in) is refused."""
    held = printed(AAPL_RUN)
    assert calculator.trailing_year_start(held) == dt.date(2025, 6, 29)
    year = view_with_year("2026-06-27", "2024-09-29..2025-06-28", x={
        "year": usd(period="2025-06-29..2026-06-27"), "eight_early": usd(period="2025-06-21..2026-06-27"),
        "nine_months": usd(period="2025-09-28..2026-06-27")})
    assert reading(year, "x.year") == (1_000_000.0, None)
    assert reading(year, "x.nine_months") == (1_000_000.0, None)
    refused_with(year, "x.eight_early", "before 2025-06-29")
    assert (dt.date(2026, 6, 27) - dt.date(2025, 6, 21)).days == 371


def test_a_view_that_prints_no_trailing_year_holds_nothing_to_a_span():
    held = {"period_end": "2026-06-30", "x": {"c": usd(period="2025-07-01..2026-06-30")}}
    assert calculator.adjustment_reading(held, "x.c")[0] is None
    assert "no period end and trailing year" in calculator.adjustment_reading(held, "x.c")[1]


def test_a_view_with_no_period_end_holds_nothing_to_a_span():
    held = {"x": {"c": usd(period="2025-07-01..2026-06-30")}}
    refused_with(held, "x.c", "no period end and trailing year")


# earnings never moves free cash flow

def test_the_calculator_lists_an_earnings_adjustment_and_does_not_apply_it_to_free_cash_flow():
    out = calculator.quality_adjusted(
        {"value": 100.0}, {"value": 10.0}, {"value": 0.0, "formula": "x"},
        [adjustment("terms.trailing_four_quarters.revenue", "reduce", "earnings"),
         adjustment("terms.trailing_four_quarters.net_income", "increase", "cash_flow")],
        with_year({**PLANTED, "terms": {"trailing_four_quarters": {"revenue": usd(), "net_income": usd()}}}))
    assert out["value"] == 100.0 - 10.0 + 1_000_000.0
    assert [r["calculator_field"] for r in out["adjustments_applied"]] == ["terms.trailing_four_quarters.net_income"]
    earnings, = out["adjustments_to_earnings"]
    assert earnings["calculator_field"] == "terms.trailing_four_quarters.revenue"
    assert earnings["amount"] == 1_000_000.0
    assert earnings["applied_to"] == EARNINGS_LABEL
    assert "before" not in earnings and "after" not in earnings


def test_an_adjustment_of_neither_target_is_refused_by_the_calculator():
    out = calculator.quality_adjusted(
        {"value": 100.0}, {"value": 10.0}, {"value": 0.0, "formula": "x"},
        [adjustment("terms.trailing_four_quarters.revenue", "reduce", "debt")], with_year(PLANTED))
    assert out["value"] == 90.0 and out["adjustments_applied"] == []
    assert out["adjustments_refused"][0]["reason"] == "applies_to is not 'cash_flow' or 'earnings'"


# the four newer sections reach the calculator's fields

@pytest.mark.parametrize("path", [
    "quarterly_cash_flow_and_accruals.balance_sheet_accruals.inputs.change_in_current_liabilities",
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


def test_the_definition_says_the_cash_flow_rule_the_span_rule_and_the_earnings_rule():
    section = adjustments_section()
    for sentence in (
            "Nor may it be one of free cash flow's own parts, which are already inside it: operating "
            "cash flow, capital expenditure (payments for property and equipment), share-based "
            "compensation and acquisitions",
            "begins no earlier than the first day of the trailing year the view prints "
            "(`terms.trailing_four_quarters`) and ends at the filing's period end",
            "A prior-year column, a history entry, a change between two spans and a change over two "
            "years are dropped as not the period free cash flow covers",
            "An adjustment you mark `\"recurs\": true` must cover the whole trailing year",
            "a shorter span (a quarter, the year to date), a change whose earlier balance is inside the "
            "year, and a cell with no dates in its own inputs can stand only as one-time",
            "A change whose later balance is not the period's end, or whose earlier balance is before the "
            "day before the trailing year, is dropped as \"its balances are not the period's\"",
            "A change in cash, or in a total that includes cash (current assets, total assets), "
            "contains free cash flow and is refused",
            "A note table's `changes` cell may be the amount of a `cash_flow` adjustment only if it is the "
            "change in a working-capital or financing balance that free cash flow carries in operating "
            "cash flow or leaves out",
            "is not on that list: name a calculator cell instead",
            "A note table's cash totals and its investing-activity flows are refused as `cash_flow` amounts",
            "A non-cash charge (an impairment, a write-down, a write-off) is never a `cash_flow` "
            "amount: it is an `earnings` adjustment",
            "Two `cash_flow` adjustments never cite the same field, nor two cells of one note table",
            "Only a `cash_flow` adjustment moves free cash flow",
            "it does not move free cash flow, and the valuation applies it (once, or as a margin cut "
            "where it recurs)"):
        assert sentence in section, sentence
    assert "applied to nothing" not in section


def test_the_accounting_analysts_definition_names_no_company_and_no_ticker():
    """Every run reads this definition, a run of the same company at an earlier cutoff among them:
    it names no company of the universe and no fact of one. `universe.json` holds tickers; the
    names of its companies are written here, one for each ticker."""
    universe = json.loads((REPO / "universe.json").read_text(encoding="utf-8"))["companies"]
    tickers = {row["ticker"] for row in universe}
    assert len(tickers) >= 18
    names = ("Apple", "Seagate", "Cisco", "Palo Alto", "Carrier", "Littelfuse", "Generac", "Ciena",
             "Qualcomm", "Escent", "ESCO", "TTM Technologies", "NVIDIA", "Nvidia", "Dell",
             "Western Digital", "Arista", "Fortinet", "Johnson Controls", "Fabrinet", "Powell",
             "Franklin Electric", "Motorola", "Lumentum", "Flex", "Broadcom", "Super Micro",
             "Sandisk", "SanDisk", "F5", "Logitech", "Lennox", "American Superconductor",
             "Ubiquiti", "Napco", "Celestica", "Advanced Micro", "Omnicell", "Adtran", "ADTRAN")
    for definition in sorted((REPO / ".claude" / "agents").glob("accounting-analyst.md")):
        text = definition.read_text(encoding="utf-8")
        found = re.findall(r"\b(?:" + "|".join(sorted(tickers | set(names), key=len, reverse=True)) + r")\b", text)
        assert found == [], (definition.name, found)


def shaped(path: str) -> re.Pattern:
    """The shape of an example path: `<n>` and `<k>` stand for digits."""
    return re.compile(re.escape(path).replace(re.escape("<n>"), r"\d+").replace(re.escape("<k>"), r"\d+"))


def test_every_example_path_in_the_adjustments_paragraph_resolves_in_a_committed_view(published_views):
    """A definition's example is a path, or the shape of one, that some committed run's view
    holds with a number: `<n>` and `<k>` are digits, so the shape is looked for in every view's
    cells."""
    text = (REPO / ".claude" / "agents" / "accounting-analyst.md").read_text(encoding="utf-8")
    examples = text[text.index("Examples of the shape:"):text.index("## Citations")]
    paths = re.findall(r"`((?:terms|earnings_versus_cash|note_tables|ratios)\.[a-z0-9_.<>]+)`", examples)
    assert len(paths) >= 5
    for path in paths:
        pattern = shaped(path)
        found = [name for name, held in published_views if any(
            pattern.fullmatch(where) and isinstance(cell.get("value"), (int, float))
            for where, cell in usd_cells(held))]
        if not found:                         # the views as printed today hold the note tables
            found = [name for name, held in [(n, printed(n)) for n, _ in published_views[:6]] if any(
                pattern.fullmatch(where) and isinstance(cell.get("value"), (int, float))
                for where, cell in usd_cells(held))]
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


# --- Palo Alto's base from companyfacts, and the valuation's reading of an earnings adjustment ------

PALO_FIRST = RUNS / "PANW" / "0001327567-26-000015"


def test_palo_altos_free_cash_flow_before_is_worked_by_hand_from_companyfacts():
    """The trailing four quarters to 2026-04-30, each term through `tests/companyfacts_source.py`
    (cutoff 2026-06-03): the fiscal year 2024-08-01..2025-07-31, plus the nine months
    2025-08-01..2026-04-30, less the nine months 2024-08-01..2025-04-30. Operating cash flow
    3,716.0 + 3,196.0 - 2,695.0 = 4,217.0; payments for productive assets 246.2 + 337.0 - 160.0 =
    423.2; free cash flow 4,217.0 - 423.2 = 3,793.8; share-based compensation 1,295.1 + 1,314.0 -
    941.0 = 1,668.1; payments to acquire businesses 1,054.4 + 4,563.0 - 499.0 = 5,118.4 (millions).
    3,793.8 - 1,668.1 - 5,118.4 = -2,992.7."""
    cutoff = view(PALO_ALTO)["cutoff"]
    assert cutoff == "2026-06-03"
    spans = ("2024-08-01..2025-07-31", "2025-08-01..2026-04-30", "2024-08-01..2025-04-30")

    def trailing(tag):
        year, ytd, before = (source.one_value("PANW", tag, span, cutoff) for span in spans)
        return year + ytd - before
    cash = trailing("NetCashProvidedByUsedInOperatingActivities")
    capex = trailing("PaymentsToAcquireProductiveAssets")
    pay = trailing("ShareBasedCompensation")
    bought = trailing("PaymentsToAcquireBusinessesNetOfCashAcquired")
    assert (cash, capex, pay, bought) == (4_217.0e6, 423.2e6, 1_668.1e6, 5_118.4e6)
    assert round(cash - capex - pay - bought) == -2_992_700_000
    held = view(PALO_ALTO)["free_cash_flow"]["free_cash_flow_quality_adjusted"]
    assert held["value"] == pytest.approx(cash - capex - pay - bought)
    assert final_with(PALO_ALTO, [])["value"] == pytest.approx(-2_992_700_000)


GORDON = {"revenue_growth_year_one": 0.03, "terminal_growth": 0.03,
          "operating_margin_year_one": 0.20, "operating_margin_year_ten": 0.20,
          "reinvestment_rate_year_one": 0.40, "reinvestment_rate_year_ten": 0.40}


def earnings_row(position, name, amount, direction="reduce", applies_to="earnings", recurs=False):
    return {"position": position, "name": name, "amount": amount, "direction": direction,
            "applies_to": applies_to, "recurs": recurs}


def valued(rows, nopat=None):
    """Palo Alto's trailing revenue (10,606.5 million: fiscal 2025's 9,221.5 plus 8,070.0 for the
    nine months less 6,685.0, companyfacts) on a firm that grows at 3% for ever, 20% margin, 25% tax,
    reinvestment 40%, cost of capital 9%, no debt, 801 million diluted shares (the 10-Q's own fact
    f-200). Its value is revenue x 1.03 x 0.2 x 0.75 x 0.6 / (0.09 - 0.03) = revenue x 1.545."""
    revenue = 10_606.5e6
    shares = 801e6
    base = revenue * 1.545 / shares
    out = calculator.adjusted_value(revenue, GORDON, 0.25, 0.09, 0.0, 0.0, shares, base,
                                    {"applied": rows, "nopat": nopat}, {"revenue": {"value": revenue}})
    return revenue, shares, base, out


def test_palo_altos_diluted_shares_are_the_filings_own_801_million():
    facts = json.loads((PALO_FIRST / "input_numbers.json").read_text(encoding="utf-8"))["facts"]
    shares, = [f for f in facts if f["id"] == "0001327567-26-000015:f-200"]
    assert (shares["tag"], shares["number"], shares["context"]["start"], shares["context"]["end"]) == (
        "WeightedAverageNumberOfDilutedSharesOutstanding", 801e6, "2026-02-01", "2026-04-30")


def test_a_one_time_earnings_adjustment_lowers_value_by_its_amount_over_diluted_shares():
    """110 million (Palo Alto's change in fair value, facts.8) over 801 million shares: 0.13733..."""
    revenue, shares, base, out = valued([earnings_row(0, "gain", 110e6)])
    row, = out["each"]
    assert row["applies_to"] == "earnings" and row["recurs"] is False and "one-time" in row["mechanism"]
    assert row["moved_per_share"] == pytest.approx(-110e6 / 801e6, rel=1e-12)
    assert row["value_per_share"] == pytest.approx(base - 110e6 / 801e6, rel=1e-12)
    assert out["all_together"]["moved_per_share"] == pytest.approx(-110e6 / 801e6, rel=1e-12)


def test_a_recurring_earnings_adjustment_cuts_the_margin_by_its_amount_over_revenue():
    """76 million over revenue 10,606.5 million lowers the margin by c = 0.00716...; the value,
    revenue x 1.03 x (0.2 - c) x 0.75 x 0.6 / 0.06, falls by 76e6 x 1.03 x 0.75 x 0.6 / 0.06
    = 76e6 x 7.725 = 587.1 million, 0.7329... a share."""
    revenue, shares, base, out = valued([earnings_row(0, "other", 76e6, recurs=True)])
    row, = out["each"]
    assert row["recurs"] is True and f"operating margin lowered by {76e6 / revenue}" in row["mechanism"]
    assert row["moved_per_share"] == pytest.approx(-76e6 * 7.725 / 801e6, rel=1e-9)
    assert out["all_together"]["moved_per_share"] == pytest.approx(-76e6 * 7.725 / 801e6, rel=1e-9)


def test_an_increasing_earnings_adjustment_raises_value_and_a_recurring_cash_flow_one_raises_reinvestment():
    revenue, shares, base, out = valued([earnings_row(0, "up", 110e6, "increase"),
                                          earnings_row(1, "flow", 54e6, applies_to="cash_flow", recurs=True)],
                                         nopat=1.5e9)
    up, flow = out["each"]
    assert up["moved_per_share"] == pytest.approx(110e6 / 801e6, rel=1e-12)
    # reinvestment rises by 54e6 / 1.5e9 = 0.036: value falls by revenue x 1.03 x 0.2 x 0.75 x 0.036 / 0.06
    assert "reinvestment rate raised by 0.036" in flow["mechanism"]
    assert flow["moved_per_share"] == pytest.approx(
        -revenue * 1.03 * 0.2 * 0.75 * 0.036 / 0.06 / shares, rel=1e-9)


def test_the_valuation_keeps_every_row_in_the_analysts_order_and_each_rows_own_flags():
    rows = [earnings_row(0, "a", 10e6, applies_to="cash_flow", recurs=True),
            earnings_row(1, "b", 20e6), earnings_row(2, "c", 30e6, recurs=True)]
    out = valued(rows, nopat=1.5e9)[3]
    assert [(r["name"], r["applies_to"], r["recurs"]) for r in out["each"]] == [
        ("a", "cash_flow", True), ("b", "earnings", False), ("c", "earnings", True)]


def test_two_adjustments_keep_their_own_target_and_recurrence_through_the_valuation():
    """The refuter's case with its two names made distinct, as the gate now requires: one an
    earnings adjustment applied once, one a cash-flow adjustment that recurs. The valuation reads
    each row's own flags, not a lookup by name. Palo Alto's first run holds the price the
    valuation needs."""
    published = json.loads((PALO_FIRST / "calculator.json").read_text(encoding="utf-8"))
    assumptions = json.loads((PALO_FIRST / "assumptions.json").read_text(encoding="utf-8"))
    adjustments = [
        {"name": "x", "direction": "reduce", "applies_to": "earnings", "recurs": False, "quote": "q",
         "calculator_field": "note_tables.tables.notes_42.facts.8"},
        {"name": "y", "direction": "reduce", "applies_to": "cash_flow", "recurs": True, "quote": "q",
         "calculator_field": "terms.trailing_four_quarters.net_income"}]
    out = calculator.calculate(**calculator_drift.trigger(PALO_FIRST), fixtures_root=STORE, bundle=PALO_FIRST,
                               market_data=published["market"], assumptions=assumptions,
                               accounting={"adjustments": adjustments})
    quality = out["free_cash_flow"]["free_cash_flow_quality_adjusted"]
    assert quality["adjustments_refused"] == []
    assert [(r["applies_to"], r["recurs"]) for r in quality["adjustments_applied"]] == [("cash_flow", True)]
    assert [(r["applies_to"], r["recurs"]) for r in quality["adjustments_to_earnings"]] == [("earnings", False)]
    each = out["valuation"]["accounting_adjustments"]["each"]
    assert [(r["name"], r["applies_to"], r["recurs"]) for r in each] == [
        ("x", "earnings", False), ("y", "cash_flow", True)]
    assert "one-time" in each[0]["mechanism"] and "reinvestment rate raised" in each[1]["mechanism"]
    assert each[0]["moved_per_share"] == pytest.approx(-110e6 / 801e6, rel=1e-9)   # 110 over 801 million shares


# --- a recurring amount must cover the year --------------------------------------------------------

@pytest.mark.parametrize("cell, covers", [
    (usd(period="2025-07-01..2026-06-30"), True),                           # the year itself
    (usd(period="2025-07-02..2026-06-30"), False),                          # a day short
    (usd(period="2026-04-01..2026-06-30"), False),                          # a quarter
    (usd(period="2025-10-01..2026-06-30"), False),                          # the year to date
    ({**usd(), "from": {"instant": "2025-06-30"}, "to": {"instant": "2026-06-30"}}, True),
    ({**usd(), "from": {"instant": "2025-07-01"}, "to": {"instant": "2026-06-30"}}, False),
    ({**usd(), "from": {"instant": "2026-03-31"}, "to": {"instant": "2026-06-30"}}, False),
])
def test_a_recurring_amount_must_cover_the_year_and_a_one_time_one_need_not(cell, covers):
    held = view_with_year("2026-06-30", "2025-01-01..2025-06-30", x={"c": cell})
    assert calculator.adjustment_reading(held, "x.c", False)[0] == 1_000_000.0
    amount, reason = calculator.adjustment_reading(held, "x.c", True)
    assert (amount == 1_000_000.0) is covers
    if not covers:
        assert amount is None and "a recurring amount must cover the year" in reason


def test_the_quarter_over_annual_revenue_case_is_refused_when_it_recurs():
    """The refuter's case: a three-month amount, taken as a margin cut over a year of revenue,
    would be four times too small. Palo Alto's `facts.8` (three months to 2026-04-30) stands once and
    is refused as recurring; its nine months (`facts.14`) is not the year either."""
    held = printed(PALO_RUN)
    for path in ("note_tables.tables.notes_42.facts.8", "note_tables.tables.notes_42.facts.14"):
        assert reading(held, path, False)[0] is not None
        refused_with_recurs(held, path)
    # the analysis gate reads the same
    problem = analysis_check.adjustment_problem(held)(
        {"direction": "reduce", "applies_to": "earnings", "recurs": True, "quote": "q",
         "calculator_field": "note_tables.tables.notes_42.facts.8"})
    assert "a recurring amount must cover the year" in problem
    # and the calculator lists it refused
    out = final_with(PALO_ALTO, [{**adjustment("note_tables.tables.notes_42.facts.8", applies_to="earnings"),
                                  "recurs": True}])
    assert out["adjustments_to_earnings"] == [] and "must cover the year" in out["adjustments_refused"][0]["reason"]


def refused_with_recurs(held, path):
    amount, reason = reading(held, path, True)
    assert amount is None and "a recurring amount must cover the year" in reason, (path, reason)


def test_a_table_placed_cells_span_is_read_from_its_own_formula_and_inputs_not_its_section():
    """The span of a cell with no dates comes from what it says of itself. NVIDIA's change in current
    liabilities (`quarterly_cash_flow_and_accruals`) is `current_liabilities now - current_liabilities
    a year earlier`, its inputs the balances of 2026-07-26 (the period's end) and 2025-07-27, 364 days
    apart: a year, so it may recur. Apple's borrowing repaid is `prior_fiscal_year + this_year_to_date -
    prior_year_to_date`, the trailing year, so it may recur; its `parts.this_year_to_date` names the
    year to date and may not."""
    held = printed(AAPL_RUN)
    nvidia = printed("NVDA/0001045810-26-000075")
    change = "quarterly_cash_flow_and_accruals.balance_sheet_accruals.inputs.change_in_current_liabilities"
    cell = calculator._cell_at(nvidia, change)
    assert cell["formula"] == "current_liabilities now - current_liabilities a year earlier"
    assert (cell["inputs"]["now"]["period"], cell["inputs"]["a_year_earlier"]["period"]) == (
        "2026-07-26", "2025-07-27")
    assert nvidia["period_end"] == "2026-07-26"
    year = calculator.trailing_year_start(nvidia)
    assert year == dt.date(2025, 7, 28)
    assert calculator.derived_span(cell, dt.date(2026, 7, 26), year) == (
        "year", "its balances, 2025-07-27 and 2026-07-26, are the year's: the later the period's end, "
                "the earlier the day before the trailing year")
    assert reading(nvidia, change, True)[0] == cell["value"]
    borrowing = calculator._cell_at(held, "terms.cash_flow_families.borrowing_repaid")
    assert borrowing["formula"] == "prior_fiscal_year + this_year_to_date - prior_year_to_date"
    assert calculator.derived_span(borrowing, dt.date(2026, 6, 27), calculator.trailing_year_start(held))[0] == "year"
    assert reading(held, "terms.cash_flow_families.borrowing_repaid", True)[0] is not None
    assert reading(held, "terms.trailing_four_quarters.net_income", True)[0] is not None
    assert reading(held, "earnings_versus_cash.working_capital.receivables.balance_sheet_change", True)[0] is not None
    refused_with_recurs(held, "terms.cash_flow_families.borrowing_repaid.parts.this_year_to_date")


def test_a_cell_whose_two_balances_are_a_quarter_apart_may_not_recur():
    quarter = {**usd(), "formula": "x now - x a year earlier", "inputs": {
        "now": {"period": "2026-06-30"}, "a_year_earlier": {"period": "2026-03-31"}}}
    year = dt.date(2025, 7, 1)
    assert calculator.derived_span(quarter, dt.date(2026, 6, 30), year) == (
        "shorter", "its balances, 2026-03-31 and 2026-06-30, are a part of the year: the earlier is inside the trailing year")
    held = {"period_end": "2026-06-30", "x": {"change_in_current_liabilities": quarter}}
    assert reading(held, "x.change_in_current_liabilities", False)[0] == 1_000_000.0       # once, it stands
    refused_with_recurs(held, "x.change_in_current_liabilities")


def two_balances(now: str, earlier: str, **more) -> dict:
    return {**usd(), "formula": "x now - x a year earlier",
            "inputs": {"now": {"period": now, "unit": "USD"}, "a_year_earlier": {"period": earlier, "unit": "USD"}}, **more}


@pytest.mark.parametrize("now, earlier", [
    ("2026-03-31", "2025-03-31"),     # a year apart, but the later is not the period's end
    ("2024-06-30", "2023-06-30"),     # a year apart, two years back
    ("2026-06-30", "2025-03-31"),     # the period's end, but the earlier is before the trailing year
])
def test_two_balances_that_sit_elsewhere_are_not_the_periods_once_or_recurring(now, earlier):
    """The refuter's plants, period end 2026-06-30 (trailing year 2025-07-01..2026-06-30): the dates
    are held to the period for a one-time change as for a recurring one, so 371 days and 364 days are
    judged one way."""
    cell = two_balances(now, earlier)
    held = {"period_end": "2026-06-30", "x": {"balance_sheet_change": cell}}
    for recurs in (False, True):
        amount, reason = reading(held, "x.balance_sheet_change", recurs)
        assert amount is None and BALANCES_NOT in reason, (recurs, reason)
    kind, why = calculator.derived_span(cell, dt.date(2026, 6, 30), dt.date(2025, 7, 1))
    assert kind == "outside" and BALANCES_NOT in why


@pytest.mark.parametrize("earlier, once, recurring", [
    ("2025-06-30", True, True),       # the day before the trailing year: a year
    ("2025-12-31", True, False),      # inside the trailing year: once only
    ("2025-06-29", False, False),     # before the day before the trailing year
])
def test_a_change_of_the_period_stands_once_inside_the_year_and_recurs_only_over_all_of_it(earlier, once, recurring):
    held = {"period_end": "2026-06-30", "x": {"balance_sheet_change": two_balances("2026-06-30", earlier)}}
    assert (reading(held, "x.balance_sheet_change", False)[0] is not None) is once
    assert (reading(held, "x.balance_sheet_change", True)[0] is not None) is recurring


def test_a_formula_with_no_dated_inputs_is_refused_for_recurrence_whatever_it_is_called():
    """Its wording never decides: a formula that says 'now less a year earlier', or a sum of a fiscal
    year and a year to date, with no dates in its inputs or parts, is refused as a recurring amount."""
    for formula in ("x now - x a year earlier", "prior_fiscal_year + this_year_to_date - prior_year_to_date",
                    "the fiscal year"):
        held = {"period_end": "2026-06-30", "x": {"balance_sheet_change": {**usd(), "formula": formula}}}
        assert calculator.derived_span(held["x"]["balance_sheet_change"], dt.date(2026, 6, 30), dt.date(2025, 7, 1)) is None
        amount, reason = reading(held, "x.balance_sheet_change", True)
        assert amount is None and "its span is not read" in reason, formula
        assert reading(held, "x.balance_sheet_change", False)[0] == 1_000_000.0


def test_a_cell_that_says_nothing_of_its_span_is_refused_for_recurrence_not_defaulted_to_a_year():
    held = {"period_end": "2026-06-30", "x": {"balance_sheet_change": usd()}}
    assert calculator.derived_span(usd(), dt.date(2026, 6, 30), dt.date(2025, 7, 1)) is None
    amount, reason = reading(held, "x.balance_sheet_change", True)
    assert amount is None and "its span is not read" in reason
    assert reading(held, "x.balance_sheet_change", False)[0] == 1_000_000.0


# the cells that really are a year, each deriving its span from its own formula, inputs, lines or
# parts: the fiscal year (a 10-K), billings, ebitda, an articulation gap, a cash-flow family
YEAR_CELLS = [
    (STX_RUN, "terms.trailing_four_quarters.net_income", "formula 'the fiscal year' with its one part"),
    (STX_RUN, "ebit", "formula 'the fiscal year'"),
    (STX_RUN, "ratios.solvency.ebitda", "its inputs, each the fiscal year"),
    (STX_RUN, "terms.cash_flow_families.borrowing_repaid", "its one dated line, the fiscal year"),
    (AAPL_RUN, "terms.trailing_four_quarters.net_income", "the trailing sum"),
    (AAPL_RUN, "ratios.solvency.ebitda", "ebit and depreciation, trailing sums"),
    (AAPL_RUN, "contract_liabilities_and_billings.billings", "revenue and the change in contract liabilities"),
    (AAPL_RUN, "earnings_versus_cash.working_capital.receivables.cash_flow_statement_change", "the trailing sum"),
    (AAPL_RUN, "terms.cash_flow_families.borrowing_repaid", "the trailing sum"),
]


@pytest.mark.parametrize("run, path, how", YEAR_CELLS, ids=[f"{row[0][:4]}-{row[1][-34:]}" for row in YEAR_CELLS])
def test_a_cell_that_really_is_a_year_derives_it_from_itself_and_may_recur(run, path, how):
    held = printed(run)
    cell = calculator._cell_at(held, path)
    assert "value" in cell and cell.get("unit") == "USD", how
    period_end = dt.date.fromisoformat(held["period_end"])
    kind, why = calculator.derived_span(cell, period_end, calculator.trailing_year_start(held))
    assert kind == "year", (path, why)
    assert reading(held, path, True)[0] == cell["value"], reading(held, path, True)


def test_no_section_name_decides_a_span():
    assert not any("quarterly" in pattern or "families" in pattern
                   for pattern, _ in calculator.SHORTER_THAN_A_YEAR_SEGMENTS)


# --- the sections an adjustment reads -----------------------------------------------------------

def test_the_sections_the_adjustment_rule_reads_hold_every_section_with_a_dollar_cell(todays_views):
    """Every top-level section of every view as printed today that holds a dollar cell the rule
    could accept is one of `ADJUSTMENT_SECTIONS`, the names the calculator builds its fields from."""
    holding = set()
    for _, held in todays_views:
        for path, cell in usd_cells(held):
            if not refused_root(path, cell):
                holding.add(path.split(".")[0])
    assert holding <= set(calculator.ADJUSTMENT_SECTIONS), holding - set(calculator.ADJUSTMENT_SECTIONS)
    assert {"ebit", "tax_rate", "terms", "ratios", "note_tables"} <= holding
    assert set(calculator.ADJUSTMENT_SECTIONS) - holding <= {"concentration", "trend_table"}


@pytest.mark.parametrize("path", ["ebit", "tax_rate.inputs.income_tax_expense",
                                  "ratios.profitability.net_margin.inputs.net_income"])
def test_a_cell_of_ebit_tax_rate_or_ratios_is_read_by_the_calculator_as_the_gate_reads_it(path):
    run = RUNS / "NVDA" / "0001045810-26-000075"
    out = calculator.calculate(**calculator_drift.trigger(run), fixtures_root=STORE, bundle=run,
                               accounting={"adjustments": [adjustment(path)]})
    quality = out["free_cash_flow"]["free_cash_flow_quality_adjusted"]
    row, = quality["adjustments_applied"]
    assert quality["adjustments_refused"] == [] and row["signed_value"] == calculator._cell_at(out, path)["value"]
    assert analysis_check.adjustment_problem(printed("NVDA/0001045810-26-000075"))(
        {"direction": "reduce", "applies_to": "cash_flow", "calculator_field": path, "quote": "q"}) is None


def test_the_row_names_free_cash_flows_span_and_its_own_beside_it():
    """A nine-month amount is never labelled as twelve months."""
    out = final_with(PALO_ALTO, [adjustment("note_tables.tables.notes_42.facts.14"),
                                 adjustment("terms.trailing_four_quarters.net_income")])
    nine, year = out["adjustments_applied"]
    assert nine["free_cash_flow_covers"] == year["free_cash_flow_covers"] == "the four quarters 2025-05-01..2026-04-30"
    assert nine["its_own_span"] == "2025-08-01..2026-04-30 within the four quarters ending 2026-04-30"
    assert year["its_own_span"].startswith("no dates of its own")


# --- a note-table change is an allow-list for a cash-flow amount ------------------------------------------

CIEN_RUN = "CIEN/0001628280-26-040767-note-tables-2026-11-14"
NOT_ON_THE_LIST = ("not a balance whose change free cash flow carries in operating cash flow or leaves "
                   "out; name a calculator cell instead")
NON_CASH = "a non-cash charge; it is an earnings adjustment"
CONTAINS = "contains free cash flow"
CONTAINS_OR_INSIDE = "contains or is already inside free cash flow"
NVDA_RUN = "NVDA/0001045810-26-000075"


def a_change(concept: str, applies_to: str = "cash_flow") -> tuple:
    held = {"period_end": "2026-06-30", "note_tables": {"tables": {"notes_1": {"changes": [
        {**usd(unit="iso4217:USD"), "concept": concept,
         "from": {"instant": "2025-06-30"}, "to": {"instant": "2026-06-30"}}]}}}}
    return held, "note_tables.tables.notes_1.changes.0"


# the refuter's cells, each a concept the earlier lists let through: (run, path, the local name, the value
# the note prints, by eye)
REFUTER_CHANGES = [
    ("TTMI/0001193125-26-335107", "note_tables.tables.notes_45.changes.6", "MachineryAndEquipmentGross", 122_495_000.0),
    ("TTMI/0001193125-26-335107", "note_tables.tables.notes_45.changes.8", "ConstructionInProgressGross", 81_359_000.0),
    ("FN/0001408710-26-000016", "note_tables.tables.notes_167.changes.5", "NoncurrentAssets", 142_999_000.0),
    ("CSCO/0000858877-26-000078", "note_tables.tables.notes_76.changes.1", "RestrictedCashAndCashEquivalentsAtCarryingValue", -564e6),
    (STX_RUN, "note_tables.tables.notes_177.changes.0", "CashandCashEquivalentsandShorttermInvestmentsFairValueDisclosure", 248e6),
    (STX_RUN, "note_tables.tables.notes_177.changes.3", "CashandCashEquivalentsandShorttermInvestmentsFairValueDisclosure", 248e6),
    ("LFUS/0001628280-26-050481-note-tables-2026-11-08", "note_tables.tables.notes_67.changes.3", "GoodwillGross", -16_316_000.0),
    (PALO_RUN, "note_tables.tables.notes_102.changes.0", "Goodwill", 17_335e6),
    (PALO_RUN, "note_tables.tables.notes_105.changes.18", "IntangibleAssetsGrossExcludingGoodwill", 6_857e6),
    (CIEN_RUN, "note_tables.tables.notes_145.changes.3",
     "PropertyPlantAndEquipmentFinanceLeaseRightOfUseAssetAfterAccumulatedDepreciationAndAmortizationAndOperatingLeaseRightOfUseAsset",
     58_149_000.0),                                        # notes:145 reads 483,541 against 425,392 (thousands)
    (AAPL_RUN, "note_tables.tables.notes_38.changes.0", "IntangibleAssetsGrossExcludingGoodwill", 13_270e6),
    (AAPL_RUN, "note_tables.tables.notes_38.changes.4", "IntangibleAssetsNetExcludingGoodwillNoncurrent", 9_249e6),
]


@pytest.mark.parametrize("run, path, local, value", REFUTER_CHANGES, ids=[f"{r[0][:4]}-{r[1][-20:]}" for r in REFUTER_CHANGES])
def test_a_note_table_change_not_on_the_allow_list_is_not_a_cash_flow_amount(run, path, local, value):
    held = printed(run)
    cell = calculator._cell_at(held, path)
    assert cell["concept"].rpartition(":")[2].lower() == local.lower() and cell["value"] == value
    assert reading(held, path) == (None, NOT_ON_THE_LIST)
    # an earnings adjustment is not held to the list
    assert reading(held, path, False, "earnings")[0] == value or reading(held, path, False, "earnings")[1]


@pytest.mark.parametrize("concept", [
    "us-gaap:AssetsFairValueDisclosure", "us-gaap:Assets", "us-gaap:AssetsCurrent", "us-gaap:Cash",
    "us-gaap:CashAndCashEquivalentsAtCarryingValue", "us-gaap:RestrictedCash", "us-gaap:MarketableSecuritiesCurrent",
    "us-gaap:AvailableForSaleSecurities", "us-gaap:LongTermInvestments", "us-gaap:PropertyPlantAndEquipmentGross",
    "us-gaap:LandAndLandImprovements", "us-gaap:BuildingsAndImprovementsGross", "us-gaap:FurnitureAndFixturesGross",
    "us-gaap:MachineryAndEquipmentGross", "us-gaap:ConstructionInProgressGross", "us-gaap:Goodwill",
    "us-gaap:GoodwillGross", "us-gaap:IntangibleAssetsNetExcludingGoodwill", "us-gaap:CapitalizedComputerSoftwareNet",
    "us-gaap:OperatingLeaseRightOfUseAsset", "us-gaap:NoncurrentAssets", "us-gaap:OtherAssetsNoncurrent",
    "us-gaap:DeferredTaxAssetsNet", "us-gaap:AccumulatedDepreciationDepletionAndAmortizationPropertyPlantAndEquipment",
    "us-gaap:LongTermDebt", "us-gaap:StockholdersEquity", "co:SomethingNotListed",
    # a receivable or a payable that is also one of the excluded words
    "co:ReceivablesNoncurrent", "co:AccountsPayableLongTermNoncurrent", "co:RestrictedCashReceivable",
    "co:InventoryEquipment", "co:PrepaidSoftware"])
def test_a_concept_off_the_allow_list_or_with_an_excluded_word_is_refused_as_a_cash_flow_amount(concept):
    held, path = a_change(concept)
    assert reading(held, path) == (None, NOT_ON_THE_LIST)


@pytest.mark.parametrize("concept", [
    "us-gaap:AccountsReceivableNetCurrent", "us-gaap:ReceivablesNetCurrent", "co:UnbilledReceivablesCurrent",
    "us-gaap:OtherReceivablesNetCurrent", "us-gaap:ContractWithCustomerAssetNetCurrent",
    "us-gaap:ContractWithCustomerLiabilityCurrent", "us-gaap:DeferredRevenueCurrent", "us-gaap:InventoryNet",
    "us-gaap:InventoryFinishedGoodsNetOfReserves", "us-gaap:InventoryRawMaterials", "us-gaap:PrepaidExpenseCurrent",
    "us-gaap:PrepaidExpenseAndOtherAssetsCurrent", "us-gaap:OtherAssetsCurrent", "us-gaap:AccountsPayableCurrent",
    "us-gaap:AccruedLiabilitiesCurrent", "us-gaap:AccruedSalariesCurrent", "us-gaap:OtherAccruedLiabilitiesCurrent",
    "us-gaap:SupplierFinanceProgramObligation", "co:ReceivablesSold", "us-gaap:TransferOfFinancialAssetsAccountedForAsSalesAmountDerecognized",
    "nvda:BusinessCombinationConsiderationPayable", "us-gaap:BusinessCombinationContingentConsiderationLiabilityCurrent",
    "co:DeferredConsiderationPayable", "co:ACCOUNTSPAYABLECURRENT"])        # case-insensitive
def test_a_working_capital_or_financing_balance_is_on_the_allow_list(concept):
    held, path = a_change(concept)
    assert reading(held, path) == (1_000_000.0, None)


def test_the_allow_list_binds_a_cash_flow_amount_and_not_an_earnings_one():
    held, path = a_change("us-gaap:Goodwill")
    assert reading(held, path, False, "cash_flow") == (None, NOT_ON_THE_LIST)
    assert reading(held, path, False, "earnings") == (1_000_000.0, None)


def test_a_calculator_cell_is_not_held_to_the_allow_list():
    """The list is for a note-table change (a cell with a concept); a calculator change has no concept."""
    held = printed(AAPL_RUN)
    assert reading(held, "earnings_versus_cash.working_capital.receivables.balance_sheet_change")[0] == 3_841e6


@pytest.mark.parametrize("run, path, value", [
    (STX_RUN, "note_tables.tables.notes_91.changes.1", 380e6),            # supplier finance obligation, a year
    (NVDA_RUN, "note_tables.tables.notes_60.changes.6", -2_935e6),        # accrued purchase consideration
])
def test_the_working_capital_and_financing_cells_the_analyst_may_cite_are_accepted(run, path, value):
    """STX's obligation (400 million at 2026-07-03 less 20 at 2025-06-27, companyfacts) and NVIDIA's
    accrued consideration payable for an acquisition, paid later and outside investing: free cash flow
    leaves it out, and an analyst may adjust for it (docs/needs_judgment.md)."""
    held = printed(run)
    cell = calculator._cell_at(held, path)
    assert cell["value"] == value
    assert reading(held, path) == (value, None)


def test_apples_working_capital_changes_stand_and_its_intangible_changes_do_not():
    """Apple's published applied adjustment (the first run's accounts payable change, a calculator
    cell) stands under the list; its intangible changes (notes_38, which its note-tables rerun cited
    and the gate dropped) are not on it."""
    held = printed(AAPL_RUN)
    payables = "earnings_versus_cash.working_capital.accounts_payable.balance_sheet_change"
    assert reading(held, payables) == (14_151e6, None)
    assert reading(held, "earnings_versus_cash.working_capital.receivables.balance_sheet_change") == (3_841e6, None)
    for position in (0, 4):
        assert reading(held, f"note_tables.tables.notes_38.changes.{position}") == (None, NOT_ON_THE_LIST)


# --- note-table flows: cash totals and investing activities ------------------------------------------------

@pytest.mark.parametrize("concept", [
    "us-gaap:NetCashProvidedByUsedInOperatingActivities", "us-gaap:NetCashProvidedByUsedInInvestingActivities",
    "us-gaap:NetCashProvidedByUsedInFinancingActivities", "us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations",
    "us-gaap:CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsPeriodIncreaseDecreaseIncludingExchangeRateEffect",
    "us-gaap:CashAndCashEquivalentsPeriodIncreaseDecrease", "us-gaap:PaymentsToAcquireInvestments",
    "us-gaap:PaymentsToAcquireIntangibleAssets", "us-gaap:PaymentsToAcquireMarketableSecurities",
    "us-gaap:PaymentsForProceedsFromOtherInvestingActivities", "us-gaap:PaymentsForProceedsFromEquityMethodInvestments",
    "us-gaap:ProceedsFromSaleOfPropertyPlantAndEquipment", "us-gaap:ProceedsFromSaleOfBusinessesNetOfCashDivested",
    "us-gaap:ProceedsFromSaleOfIntangibleAssets", "us-gaap:NETCASHPROVIDEDBYUSEDININVESTINGACTIVITIES",
    "co:paymentstoacquirethings"])
def test_a_cash_total_or_an_investing_flow_contains_or_is_already_inside_free_cash_flow(concept):
    held = {"period_end": "2026-06-30", "note_tables": {"tables": {"notes_1": {"facts": [
        usd(unit="iso4217:USD", concept=concept, start="2025-07-01", end="2026-06-30")]}}}}
    path = "note_tables.tables.notes_1.facts.0"
    amount, reason = reading(held, path, False, "cash_flow")
    assert amount is None and (reason == CONTAINS_OR_INSIDE or reason.startswith(INSIDE)), reason


@pytest.mark.parametrize("concept", ["us-gaap:ProceedsFromSaleOfAvailableForSaleSecurities", "us-gaap:RepaymentsOfDebt",
                                     "us-gaap:ProceedsFromIssuanceOfDebt", "us-gaap:IncreaseDecreaseInAccountsReceivable"])
def test_other_flows_are_not_refused_as_cash_totals_or_investing(concept):
    held = {"period_end": "2026-06-30", "note_tables": {"tables": {"notes_1": {"facts": [
        usd(unit="iso4217:USD", concept=concept, start="2025-07-01", end="2026-06-30")]}}}}
    assert reading(held, "note_tables.tables.notes_1.facts.0") == (1_000_000.0, None)


def test_an_investing_flow_may_still_be_an_earnings_adjustment():
    held = {"period_end": "2026-06-30", "note_tables": {"tables": {"notes_1": {"facts": [
        usd(unit="iso4217:USD", concept="us-gaap:PaymentsToAcquireInvestments", start="2025-07-01", end="2026-06-30")]}}}}
    assert reading(held, "note_tables.tables.notes_1.facts.0", False, "earnings") == (1_000_000.0, None)


# --- calculator cells that contain free cash flow ---------------------------------------------------------------

@pytest.mark.parametrize("path", [
    "quarterly_cash_flow_and_accruals.balance_sheet_accruals.inputs.change_in_cash",
    "quarterly_cash_flow_and_accruals.balance_sheet_accruals.inputs.change_in_current_assets",
    "quarterly_cash_flow_and_accruals.balance_sheet_less_cash_flow_accruals.inputs.balance_sheet_accruals.inputs.change_in_cash",
    "quarterly_cash_flow_and_accruals.balance_sheet_less_cash_flow_accruals.inputs.balance_sheet_accruals.inputs.change_in_current_assets",
])
def test_a_calculator_change_in_cash_or_in_a_total_that_includes_cash_contains_free_cash_flow(path):
    held = printed(NVDA_RUN)
    assert calculator._cell_at(held, path)["unit"] == "USD"
    refused_with(held, path, CONTAINS)


def test_a_change_in_receivables_or_current_liabilities_does_not_contain_free_cash_flow():
    held = printed(NVDA_RUN)
    for path in ("quarterly_cash_flow_and_accruals.balance_sheet_accruals.inputs.change_in_current_liabilities",
                 "earnings_versus_cash.working_capital.receivables.balance_sheet_change"):
        assert reading(held, path)[0] is not None, path


# --- a non-cash charge is an earnings adjustment -----------------------------------------------------------------

def test_gnrcs_goodwill_impairment_is_refused_as_cash_flow_and_accepted_as_earnings():
    """Generac's `notes_105.facts.9`, the goodwill impairment loss of the six months to 2026-06-30
    (1.523 million): a non-cash charge, so never the amount of a cash-flow adjustment."""
    held = printed("GNRC/0001437749-26-025669")
    path = "note_tables.tables.notes_105.facts.9"
    cell = calculator._cell_at(held, path)
    assert cell["concept"] == "us-gaap:GoodwillImpairmentLoss" and cell["value"] == 1_523_000.0
    assert reading(held, path, False, "cash_flow") == (None, NON_CASH)
    assert reading(held, path, False, "earnings") == (1_523_000.0, None)
    assert analysis_check.adjustment_problem(held)(
        {"direction": "reduce", "applies_to": "cash_flow", "calculator_field": path, "quote": "q"}).endswith(NON_CASH)
    assert analysis_check.adjustment_problem(held)(
        {"direction": "reduce", "applies_to": "earnings", "calculator_field": path, "quote": "q"}) is None
    run = RUNS / "GNRC" / "0001437749-26-025669"
    out = calculator.calculate(**calculator_drift.trigger(run), fixtures_root=STORE, bundle=run, accounting={
        "adjustments": [adjustment(path), adjustment(path, applies_to="earnings")]})
    quality = out["free_cash_flow"]["free_cash_flow_quality_adjusted"]
    assert [r["reason"].endswith(NON_CASH) for r in quality["adjustments_refused"]] == [True]
    assert len(quality["adjustments_to_earnings"]) == 1 and quality["adjustments_applied"] == []


@pytest.mark.parametrize("path", ["terms.trailing_four_quarters.inventory_write_down", "x.asset_impairment_charges",
                                  "x.receivables_write_off"])
def test_a_calculator_cell_named_for_a_non_cash_charge_is_refused_as_cash_flow(path):
    held = {"period_end": "2026-06-30"}
    node = held
    parts = path.split(".")
    for part in parts[:-1]:
        node = node.setdefault(part, {})
    node[parts[-1]] = usd(period="2025-07-01..2026-06-30")
    assert reading(held, path, False, "cash_flow") == (None, NON_CASH)
    assert reading(held, path, False, "earnings")[0] == 1_000_000.0


@pytest.mark.parametrize("concept", [
    "us-gaap:GoodwillImpairmentLoss", "us-gaap:AssetImpairmentCharges", "us-gaap:IMPAIRMENTOFINTANGIBLEASSETS",
    "csco:AccountsReceivableWriteoffAfterRecovery", "co:InventoryWriteDown", "co:InventoryWritedown",
    "co:WriteOffOfReceivables", "co:WriteoffOfDeferredCosts"])
def test_a_charge_with_impairment_write_down_or_write_off_in_its_name_is_refused_in_any_case(concept):
    held = {"period_end": "2026-06-30", "note_tables": {"tables": {"notes_1": {"facts": [
        usd(unit="iso4217:USD", concept=concept, start="2025-07-01", end="2026-06-30")]}}}}
    assert reading(held, "note_tables.tables.notes_1.facts.0") == (None, NON_CASH)


def test_csco_write_off_after_recovery_is_refused_and_qcoms_excluding_impairments_is_not():
    """Cisco's `...WriteoffAfterRecovery` (a charge) is refused as a cash-flow amount; Qualcomm's
    `MarketableSecuritiesRealizedGainLossExcludingOtherThanTemporaryImpairments` is a gain or loss
    excluding impairments, not a charge: the words after "Excluding" do not count."""
    csco = printed("CSCO/0000858877-26-000078")
    found = [(t, i) for t, v in csco["note_tables"]["tables"].items() for i, f in enumerate(v["facts"])
             if f["concept"].lower().endswith("writeoffafterrecovery")]
    assert found
    table, position = found[0]
    path = f"note_tables.tables.{table}.facts.{position}"
    assert calculator.non_cash_charge(path, calculator._cell_at(csco, path)) == NON_CASH
    assert reading(csco, path, False, "earnings")[1] != NON_CASH
    name = "MarketableSecuritiesRealizedGainLossExcludingOtherThanTemporaryImpairments"
    held = {"period_end": "2026-06-30", "note_tables": {"tables": {"notes_1": {"facts": [
        usd(unit="iso4217:USD", concept=f"us-gaap:{name}", start="2025-07-01", end="2026-06-30")]}}}}
    assert calculator.non_cash_charge("note_tables.tables.notes_1.facts.0", held["note_tables"]["tables"]["notes_1"]["facts"][0]) is None
    assert reading(held, "note_tables.tables.notes_1.facts.0") == (1_000_000.0, None)
    qcom = printed("QCOM/0000804328-26-000086")
    hits = [(t, i) for t, v in qcom["note_tables"]["tables"].items() for k in ("facts", "changes")
            for i, f in enumerate(v.get(k, [])) if f["concept"].endswith(name)]
    assert hits
    for table, position in hits[:3]:
        body = qcom["note_tables"]["tables"][table]
        key = "facts" if body.get("facts") and body["facts"][position]["concept"].endswith(name) else "changes"
        assert calculator.non_cash_charge("x", body[key][position]) is None


def test_a_flow_fact_of_goodwill_is_not_a_change_and_stands_once():
    """CARR's currency translation loss on goodwill over the year to date (a flow fact of
    2026-01-01..2026-06-30, -231 million) is accepted once, and is not a recurring year."""
    held = printed(CARR_RUN)
    path = "note_tables.tables.notes_17.facts.19"
    assert calculator._cell_at(held, path)["concept"] == "us-gaap:GoodwillForeignCurrencyTranslationGainLoss"
    assert reading(held, path, False) == (-231e6, None)
    refused_with_recurs(held, path)


# --- one amount counted once ----------------------------------------------------------------------------------------

def test_a_second_cash_flow_adjustment_citing_the_same_field_is_refused_by_the_calculator_and_the_gate():
    path = "earnings_versus_cash.working_capital.receivables.balance_sheet_change"
    out = final_with(APPLE, [adjustment(path), {**adjustment(path), "name": "again"}])
    applied, = out["adjustments_applied"]
    assert applied["name"] == path and out["value"] == 119_136 * MILLION
    refused, = out["adjustments_refused"]
    assert refused["name"] == "again" and "counts one amount twice" in refused["reason"] and "cites" in refused["reason"]


def test_a_second_cash_flow_adjustment_from_the_same_note_table_is_refused():
    """A table's cells contain each other: STX's supplier-finance obligation change and its increase,
    both of notes_91, are one amount counted twice. One adjustment for each table."""
    held = printed(STX_RUN)
    first, second = "note_tables.tables.notes_91.changes.1", "note_tables.tables.notes_91.facts.0"
    assert reading(held, first)[0] is not None
    assert calculator.counted_twice(second, [first]) is not None
    assert "same note table, notes_91" in calculator.counted_twice(second, [first])
    assert calculator.counted_twice("note_tables.tables.notes_92.changes.0", [first]) is None
    assert calculator.counted_twice(first, []) is None
    assert calculator.counted_twice("terms.trailing_four_quarters.net_income", [first]) is None


def test_two_allowed_cells_of_one_note_table_are_counted_once_through_calculate():
    """Two cells of NVIDIA's `notes_60` (its accrued consideration and another allowed line of the same
    table): the first applies, the second is refused as one amount counted twice."""
    run = RUNS / "NVDA" / "0001045810-26-000075"
    held = printed(NVDA_RUN)
    table = held["note_tables"]["tables"]["notes_60"]
    allowed = [i for i, c in enumerate(table["changes"])
               if reading(held, f"note_tables.tables.notes_60.changes.{i}")[0] is not None]
    assert len(allowed) >= 2, allowed
    paths = [f"note_tables.tables.notes_60.changes.{i}" for i in allowed[:2]]
    out = calculator.calculate(**calculator_drift.trigger(run), fixtures_root=STORE, bundle=run, accounting={
        "adjustments": [adjustment(paths[0]), {**adjustment(paths[1]), "name": "second"}]})
    quality = out["free_cash_flow"]["free_cash_flow_quality_adjusted"]
    assert [r["calculator_field"] for r in quality["adjustments_applied"]] == [paths[0]]
    assert "same note table, notes_60" in quality["adjustments_refused"][0]["reason"]


def gate_overlap(items):
    from tests import test_analysis_check as gate
    payload = gate.accounting()
    payload["adjustments"] = items
    return analysis_check.check("accounting", payload, fields=gate.FIELDS, sources=gate.SOURCES)


def test_the_gate_drops_a_second_cash_flow_adjustment_on_one_field_but_not_an_earnings_one():
    base = {"direction": "reduce", "recurs": False, "quote": "extended payment terms to certain customers",
            "quote_from": "report_notes_text.md", "evidence": [],
            "calculator_field": "terms.trailing_four_quarters.revenue"}
    one = {**base, "name": "a", "applies_to": "cash_flow"}
    two = {**base, "name": "b", "applies_to": "cash_flow"}
    three = {**base, "name": "c", "applies_to": "earnings"}
    out = gate_overlap([one, two, three])
    assert [item["name"] for item in out["adjustments"]] == ["a", "c"]
    dropped, = [d for d in out["dropped_items"] if "counts one amount twice" in d["reason"]]
    assert dropped["where"] == "adjustments[1]" and "cites" in dropped["reason"]


def test_the_gate_drops_a_second_cash_flow_adjustment_from_one_note_table():
    held = copy.deepcopy(printed(STX_RUN))
    # two allowed cells of one table, the gate reading the same rule the calculator does
    problem = analysis_check.adjustment_overlap
    kept = [{"applies_to": "cash_flow", "calculator_field": "note_tables.tables.notes_91.changes.1"}]
    again = {"applies_to": "cash_flow", "calculator_field": "note_tables.tables.notes_91.changes.2"}
    assert "same note table, notes_91" in problem(again, kept)
    assert problem({**again, "applies_to": "earnings"}, kept) is None
    assert problem(again, [{**kept[0], "applies_to": "earnings"}]) is None
    assert problem({**again, "calculator_field": "note_tables.tables.notes_92.changes.0"}, kept) is None


# --- a name is used once, enforced at the gate --------------------------------------------------

def gate_adjustments(items):
    """The gate on the analysis test file's own accounting payload, its adjustments replaced."""
    from tests import test_analysis_check as gate
    payload = gate.accounting()
    payload["adjustments"] = items
    return analysis_check.check("accounting", payload, fields=gate.FIELDS, sources=gate.SOURCES)


ONE = {"name": "x", "direction": "reduce", "applies_to": "earnings", "recurs": False,
       "calculator_field": "terms.trailing_four_quarters.revenue",
       "quote": "extended payment terms to certain customers",
       "quote_from": "report_notes_text.md", "evidence": []}


def test_the_gate_drops_an_adjustment_whose_name_repeats_an_earlier_one():
    first = ONE
    second = {**ONE, "applies_to": "cash_flow"}
    third = {**ONE, "name": "y"}
    out = gate_adjustments([first, second, third])
    assert [(item["name"], item["applies_to"]) for item in out["adjustments"]] == [
        ("x", "earnings"), ("y", "earnings")]                    # the first of the name stands
    repeats = [d for d in out["dropped_items"] if "repeats" in d["reason"]]
    assert [d["where"] for d in repeats] == ["adjustments[1]"]
    assert "name 'x' repeats an earlier adjustments item's name" in repeats[0]["reason"]
    assert out["dropped_count"] >= 1


def test_a_dropped_first_adjustment_does_not_take_its_name_from_a_later_one():
    bad = {**ONE, "direction": "sideways"}
    out = gate_adjustments([bad, ONE])
    assert [item["name"] for item in out["adjustments"]] == ["x"]
    assert not [d for d in out["dropped_items"] if "repeats" in d["reason"]]


# --- the definitions name no company, no ticker and no concrete table ------------------------------

def test_no_definition_gives_a_concrete_note_table_locator():
    """A path such as `notes_38.facts.3` is one company's table: the accounting and the financial
    analysts' definitions write `notes_<n>`, `facts.<i>` and `changes.<i>` instead."""
    for definition in sorted((REPO / ".claude" / "agents").glob("*.md")):
        text = definition.read_text(encoding="utf-8")
        assert re.findall(r"notes[_:]\d+", text) == [], definition.name
    for name in ("accounting-analyst", "financial-analyst"):
        text = (REPO / ".claude" / "agents" / f"{name}.md").read_text(encoding="utf-8")
        assert "{note_tables.tables.notes_<n>.facts.<i>}" in text and "{note_tables.tables.notes_<n>.changes.<i>}" in text


def test_the_view_and_the_definition_call_billings_one_formula_for_every_company():
    text = (REPO / ".claude" / "agents" / "accounting-analyst.md").read_text(encoding="utf-8")
    flat = " ".join(text.split())
    assert ("one formula for every company, revenue plus the change in deferred revenue, a definition some "
            "companies publish and not the company's own unless its filing says so") in flat
    held = printed(AAPL_RUN)
    definition = held["contract_liabilities_and_billings"]["billings"]["definition"]
    assert "one formula for every company" in definition and "not the company's own unless its filing says so" in definition
    assert "Fortinet" not in json.dumps(held["contract_liabilities_and_billings"])


def test_a_placeholder_form_in_a_definition_is_not_a_citation_the_gate_would_resolve():
    """The definitions' `{note_tables.tables.notes_<n>.facts.<i>}` is a shape, not a path: the
    gate's placeholder reader leaves it alone, and the same shape with digits is read."""
    assert analysis_check.PLACEHOLDER.fullmatch("{note_tables.tables.notes_<n>.facts.<i>}") is None
    assert analysis_check.PLACEHOLDER.fullmatch("{note_tables.tables.notes_7.facts.3}") is not None


@pytest.mark.parametrize("run", [STX_RUN, AAPL_RUN], ids=["seagate", "apple"])
def test_an_articulation_gap_whose_balance_change_carries_no_dates_is_not_read_as_a_year(run):
    """The gap's input `balance_sheet_change` is printed without its two balances, so the span of the
    gap is not read from dates and the gap cannot recur; it stands once."""
    held = printed(run)
    path = "earnings_versus_cash.working_capital.receivables.articulation_gap"
    assert "inputs" not in calculator._cell_at(held, path + ".inputs.balance_sheet_change")
    assert calculator.derived_span(calculator._cell_at(held, path), dt.date.fromisoformat(held["period_end"]),
                                   calculator.trailing_year_start(held)) is None
    refused_with_recurs(held, path)
    assert reading(held, path, False)[0] == calculator._cell_at(held, path)["value"]


# --- the exclusions bind a name that also holds an allowed word; and dated parts are held to the year --------

@pytest.mark.parametrize("word", ["Cash", "Restricted", "Investments", "Securities", "FairValueDisclosure", "Noncurrent",
                                  "PropertyPlant", "Machinery", "Building", "Land", "ConstructionInProgress", "Furniture",
                                  "Equipment", "Goodwill", "Intangible", "Software", "RightOfUse"])
def test_each_excluded_word_refuses_a_name_that_also_holds_an_allowed_word(word):
    held, path = a_change(f"co:Receivable{word}Other")
    assert reading(held, path) == (None, NOT_ON_THE_LIST)
    held, path = a_change(f"co:{word.upper()}PAYABLE")
    assert reading(held, path) == (None, NOT_ON_THE_LIST)


def test_a_total_of_assets_is_refused_even_where_a_working_capital_word_follows():
    for concept in ("co:AssetsPrepaid", "us-gaap:AssetsCurrentReceivable"):
        held, path = a_change(concept)
        assert reading(held, path) == (None, NOT_ON_THE_LIST)
    held, path = a_change("us-gaap:PrepaidExpenseAndOtherAssetsCurrent")
    assert reading(held, path) == (1_000_000.0, None)


def test_a_path_segment_named_for_a_charge_is_read_in_any_case():
    held = {"period_end": "2026-06-30", "x": {"AssetImpairmentCharges": usd(period="2025-07-01..2026-06-30")}}
    assert reading(held, "x.AssetImpairmentCharges", False, "cash_flow") == (None, NON_CASH)
    assert reading(held, "x.AssetImpairmentCharges", False, "earnings")[0] == 1_000_000.0


def parted(this_year: str, prior_year: str, fiscal: str = "2024-07-01..2025-06-30") -> dict:
    return {**usd(), "formula": "prior_fiscal_year + this_year_to_date - prior_year_to_date", "parts": {
        "prior_fiscal_year": {"period": fiscal}, "this_year_to_date": {"period": this_year},
        "prior_year_to_date": {"period": prior_year}}}


def test_the_parts_of_a_trailing_sum_must_run_from_the_trailing_years_first_day_to_the_period_end():
    """The trailing year is 2025-07-01..2026-06-30 (the prior year to date ended 2025-06-30)."""
    year, end = dt.date(2025, 7, 1), dt.date(2026, 6, 30)
    good = parted("2025-07-01..2026-06-30", "2024-07-01..2025-06-30")
    assert calculator.derived_span(good, end, year)[0] == "year"
    for wrong in (parted("2025-07-01..2026-03-31", "2024-07-01..2025-03-31"),       # a quarter early
                  parted("2025-07-01..2026-06-30", "2024-07-01..2025-03-31")):      # the prior year to date ends early
        assert calculator.derived_span(wrong, end, year)[0] == "outside"
        held = {"period_end": "2026-06-30", "x": {"balance_sheet_change": wrong}}
        amount, reason = reading(held, "x.balance_sheet_change", True)
        assert amount is None and "a recurring amount must cover the year" in reason and "not the trailing year" in reason


def test_dated_lines_are_held_to_the_trailing_year_one_by_one():
    year, end = dt.date(2025, 7, 1), dt.date(2026, 6, 30)

    def lined(period):
        return {**usd(), "lines": [{"period": period, "unit": "USD", "value": 1.0}]}
    assert calculator.derived_span(lined("2025-07-01..2026-06-30"), end, year)[0] == "year"
    assert calculator.derived_span(lined("2025-10-01..2026-06-30"), end, year)[0] == "shorter"
    for outside in ("2025-07-01..2026-03-31", "2025-06-30..2026-06-30", "2024-07-01..2025-06-30"):
        kind, why = calculator.derived_span(lined(outside), end, year)
        assert kind == "outside" and "not the period's" in why, outside
    held = {"period_end": "2026-06-30", "x": {"balance_sheet_change": lined("2025-07-01..2026-03-31")}}
    amount, reason = reading(held, "x.balance_sheet_change", True)
    assert amount is None and "a recurring amount must cover the year" in reason
