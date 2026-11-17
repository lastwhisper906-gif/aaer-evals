"""The memo and the page show the accounting analyst's earnings adjustments beside the cash-flow ones.

An earnings adjustment moves no summed value (`docs/ANALYSIS_PIPELINE.md` section 5): it is printed with its own
per-share effect and the plain words that it is shown alone and not summed. Only a cash-flow row is described as
moving the value, and a run whose standing adjustments are all earnings never prints "없음"."""

from __future__ import annotations

import pytest

from src import analysis_page, memo

ALONE = "합산하지 않음"


def planted(*, cash_flow: bool = True, earnings: bool = True) -> dict:
    rows_cash = [{"position": 0, "name": "채권 증가", "calculator_field": "terms.trailing_four_quarters.change_in_receivables",
                  "direction": "reduce", "applies_to": "cash_flow", "amount": 4.0e9}] if cash_flow else []
    rows_earn = [{"position": 1, "name": "충당금 변동", "calculator_field": "note_tables.tables.notes_1.changes.0",
                  "direction": "reduce", "applies_to": "earnings", "amount": 9.7e7}] if earnings else []
    return {"free_cash_flow": {"free_cash_flow_quality_adjusted": {
                "value": 1.0e9, "unit": "USD", "adjustments_applied": rows_cash,
                "adjustments_to_earnings": rows_earn}},
            "valuation": {"accounting_adjustments": {"each": [
                {"name": "채권 증가", "applies_to": "cash_flow", "moved_per_share": -1.5},
                {"name": "충당금 변동", "applies_to": "earnings", "alone_per_share": -0.42,
                 "summed": "shown alone; not summed until the special-items table exists"}],
                "all_together": {"moved_per_share": -1.5}}}}


def memo_lines(fields: dict) -> list[str]:
    analysis = {"summary_ko": {}, "anomalies": [], "areas": {}}
    return memo.accounting_section(analysis, fields, adjusted=fields)


def adjustment_lines(lines: list[str]) -> list[str]:
    start = next(i for i, line in enumerate(lines) if line.startswith("**회계 조정**"))
    return [line for line in lines[start + 1:] if line.startswith("- ")]


def test_the_memo_shows_both_rows_and_only_the_cash_flow_row_moves_the_value():
    rows = adjustment_lines(memo_lines(planted()))
    assert len(rows) == 2
    cash, earn = rows
    assert "채권 증가" in cash and ALONE not in cash and "단독" not in cash
    assert "충당금 변동" in earn and ALONE in earn and "단독으로만 표시" in earn
    assert "주당 -0.42달러" in earn                            # its own effect, read from the valuation's row


def test_a_run_whose_adjustments_are_all_earnings_does_not_print_none():
    rows = adjustment_lines(memo_lines(planted(cash_flow=False)))
    assert len(rows) == 1 and "충당금 변동" in rows[0] and rows[0] != "- 없음"
    assert adjustment_lines(memo_lines(planted(cash_flow=False, earnings=False))) == ["- 없음"]


def test_an_earnings_row_without_a_computed_effect_says_so():
    fields = planted(cash_flow=False)
    fields["valuation"] = {"missing": "no assumptions"}
    row, = adjustment_lines(memo_lines(fields))
    assert "주당 효과 계산 안 됨" in row and ALONE in row


def test_the_page_shows_both_rows_and_only_the_cash_flow_row_moves_the_value():
    fields = planted()
    page = analysis_page.accounting({"summary_ko": {}, "anomalies": [], "areas": {}}, fields, fields)
    cash, earn = page["adjustments"]
    assert cash["name"] == "채권 증가" and ALONE not in cash["text"] and "applies_to" not in cash
    assert earn["name"] == "충당금 변동" and ALONE in earn["text"] and earn["applies_to"] == "earnings"
    assert "주당 -0.42달러" in earn["text"]


def test_the_page_shows_an_all_earnings_run_with_its_row():
    fields = planted(cash_flow=False)
    page = analysis_page.accounting({"summary_ko": {}, "anomalies": [], "areas": {}}, fields, fields)
    assert [row["name"] for row in page["adjustments"]] == ["충당금 변동"]


def test_the_valuation_part_of_the_memo_puts_the_cash_flow_figure_under_its_heading_and_shows_earnings_alone():
    fields = planted()
    lines = memo.accounting_adjustment_lines(fields)
    heading = [line for line in lines if line.startswith(f"- {memo.VALUATION_KO['accounting_adjustments']}")]
    assert heading == ["- 회계 조정이 바꾼 가치 (잉여현금흐름 조정만 합산): 주당 -1.50달러"]
    earn, = [line for line in lines if "이익 조정" in line]
    assert "충당금 변동" in earn and "단독으로만 표시" in earn and "더하지 않음" in earn and "-0.42" in earn
    assert "-1.50" not in earn
    assert memo.accounting_adjustment_lines({"valuation": {"missing": "no assumptions"}}) == []


def test_an_earnings_row_has_no_moved_per_share_for_a_reader_to_add():
    fields = planted()
    each = fields["valuation"]["accounting_adjustments"]["each"]
    assert "moved_per_share" in each[0] and "moved_per_share" not in each[1] and "alone_per_share" in each[1]


def test_the_memos_valuation_section_prints_the_adjustment_lines():
    fields = planted()
    fields["valuation"].update({"value_range_per_share": {"low": 10.0, "high": 20.0}, "price_at_cutoff": 15.0,
                                "price_position": "범위 안", "reverse_dcf": {"value": 0.05}})
    text = "\n".join(memo.valuation_section(None, fields))
    assert "회계 조정이 바꾼 가치 (잉여현금흐름 조정만 합산): 주당 -1.50달러" in text
    assert "이익 조정 충당금 변동: 단독으로만 표시" in text
