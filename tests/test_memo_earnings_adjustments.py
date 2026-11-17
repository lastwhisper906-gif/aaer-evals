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
    heading = [line for line in lines if line.startswith(f"- {memo.ADJUSTED_VALUE_LINE_KO}")]
    assert heading == ["- 회계 조정으로 달라진 주당 가치 (잉여현금흐름 조정만 합산): 주당 -1.50달러"]
    earn, = [line for line in lines if "이익 조정" in line]
    assert "충당금 변동" in earn and "단독으로만 표시" in earn and earn.endswith("가치에 합산하지 않음") and "-0.42" in earn
    assert "-1.50" not in earn
    assert memo.accounting_adjustment_lines({"valuation": {"missing": "no assumptions"}}) == []


def test_an_earnings_row_has_no_moved_per_share_for_a_reader_to_add():
    """Read what `calculator.adjusted_value` emits, not a dict planted here."""
    from src import calculator
    gordon = {"revenue_growth_year_one": 0.03, "terminal_growth": 0.03, "operating_margin_year_one": 0.20,
              "operating_margin_year_ten": 0.20, "reinvestment_rate_year_one": 0.40,
              "reinvestment_rate_year_ten": 0.40}
    moved = {"applied": [{"name": "a reserve release", "direction": "reduce", "applies_to": "earnings",
                          "amount": 10.0, "recurs": True},
                         {"name": "a one-time gain", "direction": "reduce", "applies_to": "earnings",
                          "amount": 5.0}], "nopat": None}
    out = calculator.adjusted_value(1000.0, gordon, 0.25, 0.09, 100.0, 45.0, 10.0, 140.0, moved,
                                    {"revenue": {"value": 1000.0}})
    assert len(out["each"]) == 2
    for row in out["each"]:
        assert "moved_per_share" not in row and isinstance(row["alone_per_share"], float), row
    assert out["all_together"]["moved_per_share"] == pytest.approx(0.0, abs=1e-9)


def test_the_memos_valuation_section_prints_the_adjustment_lines():
    fields = planted()
    fields["valuation"].update({"value_range_per_share": {"low": 10.0, "high": 20.0}, "price_at_cutoff": 15.0,
                                "price_position": "범위 안", "reverse_dcf": {"value": 0.05}})
    text = "\n".join(memo.valuation_section(None, fields))
    assert "회계 조정으로 달라진 주당 가치 (잉여현금흐름 조정만 합산): 주당 -1.50달러" in text
    assert "이익 조정 충당금 변동: 단독으로만 표시" in text


NODE_HARNESS = r"""
const fs = require("fs");
const html = fs.readFileSync(process.argv[2], "utf8");
const script = html.match(/<script>\s*(\(function[\s\S]*?)<\/script>/)[1];
const data = html.match(/<script id="runs-data" type="application\/json">([\s\S]*?)<\/script>/)[1];
const out = {};
const element = (id) => new Proxy({ id }, {
  get(target, key) { return key in target ? target[key] : () => element(id); },
  set(target, key, value) { target[key] = value; if (key === "innerHTML") out[id] = value; return true; } });
global.document = { getElementById: (id) => id === "runs-data" ? { textContent: data } : element(id),
  addEventListener() {}, querySelector: () => element("q"), querySelectorAll: () => [] };
global.window = { addEventListener() {}, scrollTo() {} };
global.location = { hash: "" };
new Function(script)();
process.stdout.write(out.main || "");
"""


def rendered_page(tmp_path, accounting: dict) -> str:
    """The page's own script run under node against a stub document; returns the main element's markup."""
    import json
    import shutil
    import subprocess
    node = shutil.which("node")
    if node is None:
        pytest.skip("node is not installed")
    entry = {"ticker": "ZZZ", "form": "10-Q", "period_end": "2026-06-30", "filing_date": "2026-07-30",
             "accession": "0000000001-26-000001", "run": "ZZZ/0000000001-26-000001", "models": [],
             "accounting": accounting, "financial": None}
    page = analysis_page.page([entry])
    (tmp_path / "page.html").write_text(page, encoding="utf-8")
    (tmp_path / "harness.js").write_text(NODE_HARNESS, encoding="utf-8")
    done = subprocess.run([node, str(tmp_path / "harness.js"), str(tmp_path / "page.html")],
                          capture_output=True, text=True, timeout=60)
    assert done.returncode == 0, done.stderr[-600:]
    return done.stdout


def test_the_page_puts_each_adjustment_row_under_its_own_heading(tmp_path):
    fields = planted()
    page = analysis_page.accounting({"summary_ko": {}, "anomalies": [], "areas": {}}, fields, fields)
    markup = rendered_page(tmp_path, page)
    cash_heading = "잉여현금흐름에 적용한 회계 조정"
    earn_heading = "가치에 합산하지 않은 이익 조정"
    assert markup.count(cash_heading) == 1 and markup.count(earn_heading) == 1
    cash_at, earn_at = markup.index(cash_heading), markup.index(earn_heading)
    assert cash_at < earn_at
    cash_part, earn_part = markup[cash_at:earn_at], markup[earn_at:]
    assert "채권 증가" in cash_part and "충당금 변동" not in cash_part
    assert "충당금 변동" in earn_part and "채권 증가" not in earn_part and "각각 단독 효과" in markup


def test_a_page_with_no_earnings_row_has_no_earnings_list(tmp_path):
    fields = planted(earnings=False)
    page = analysis_page.accounting({"summary_ko": {}, "anomalies": [], "areas": {}}, fields, fields)
    markup = rendered_page(tmp_path, page)
    assert "채권 증가" in markup and "가치에 합산하지 않은 이익 조정" not in markup
