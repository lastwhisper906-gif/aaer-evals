"""The analysis gate and the memo, judged on analyses written here by hand.

Every expected value below is a rule stated in `docs/CHECKLIST.md` §7 or in the
three analyst prompts, applied by hand to an analysis written in this file:
a `{path}` that resolves stands, one that does not drops its item; a digit in an
analyst's own words drops its item; an evidence id that is not an item of a
report the analyst saw drops its item; a quote that is not in the file it names
drops its item; the owner's ruled-out words drop their item; and the memo puts
the calculator's number where the analyst put the path.
"""

from __future__ import annotations

import copy
import json

import pytest

from src import analysis_check, memo

FIELDS = {
    "ticker": "TEST", "form": "10-Q", "period_end": "2026-06-30", "cutoff": "2026-07-30",
    "missing": [],
    "trend_table": {"quarters-back-0": {"ratios": {"gross_margin": {"value": 0.7}}}},
    "ratios": {"liquidity": {"current_ratio": {"value": 2.5, "unit": "ratio"},
                             "cash_runway_months": {"value": None, "not_burning_cash": True,
                                                    "reason": "free cash flow is positive"}},
               "profitability": {"gross_margin": {"value": 0.4, "unit": "ratio"}},
               "efficiency": {"days_sales_outstanding": {"value": 61.25, "unit": "days"}}},
    "terms": {"trailing_four_quarters": {"revenue": {"value": 1.5e9, "unit": "USD"},
                                         "share_based_compensation": {"value": 3e7, "unit": "USD"}}},
    "earnings_versus_cash": {"history": {"years": [{"revenue_growth": 0.1}]}},
    "free_cash_flow": {"free_cash_flow_quality_adjusted": {"adjustments_applied": []}},
    "valuation": {"missing": "no price"},
}

NUMBERS = '''```json
{ "id": "revenue_recognition_receivables_rising", "what_changed": "x", "quote": "q", "paragraph_id": "p" }
```'''
NOTES = '''```json
{ "id": "revenue_recognition_payment_terms_extended", "what_changed": "y",
  "expected_direction": "up", "quote": "extended payment terms to certain customers",
  "paragraph_id": "p2" }
```
[p2] We extended payment terms to certain customers during the quarter.'''
SOURCES = {"report_numbers.md": NUMBERS, "report_notes_text.md": NOTES}

AREA = {"finding": "Days sales outstanding rose to {ratios.efficiency.days_sales_outstanding}.",
        "verdict": "weaker", "evidence": ["revenue_recognition_receivables_rising"],
        "fields": ["ratios.efficiency.days_sales_outstanding"]}


def accounting(**changes):
    payload = {
        "question": "do reported earnings and cash reflect economic reality?",
        "areas": {name: copy.deepcopy(AREA) for name in analysis_check.ACCOUNTING_AREAS},
        "reconciliation": [{"notes_item": "revenue_recognition_payment_terms_extended",
                            "numbers_items": ["revenue_recognition_receivables_rising"],
                            "outcome": "confirms", "why": "both rise"}],
        "anomalies": [{"id": "revenue_recognition_receivables_outrun_revenue",
                       "name": "receivables outrun revenue", "area": "revenue_recognition",
                       "what": "DSO at {ratios.efficiency.days_sales_outstanding}",
                       "numbers_vs_prose": "confirms",
                       "evidence": ["revenue_recognition_payment_terms_extended"],
                       "fields": []}],
        "adjustments": [{"name": "extended terms", "direction": "reduce",
                         "applies_to": "cash_flow",
                         "calculator_field": "terms.trailing_four_quarters.revenue",
                         "quote": "extended payment terms to certain customers",
                         "quote_from": "report_notes_text.md", "evidence": []}],
        "summary_ko": {"earnings_versus_cash": "매출채권 회전일수는 {ratios.efficiency.days_sales_outstanding}입니다."},
        "limits": analysis_check.LIMITS["accounting"],
    }
    payload.update(changes)
    return payload


def test_a_clean_analysis_stands_whole():
    out = analysis_check.check("accounting", accounting(), fields=FIELDS, sources=SOURCES)
    assert out["dropped_count"] == 0
    assert len(out["anomalies"]) == 1 and len(out["adjustments"]) == 1


def test_a_number_in_the_analysts_own_words_drops_the_item():
    payload = accounting()
    payload["anomalies"][0]["what"] = "DSO rose to 61 days"
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    assert out["anomalies"] == []
    assert out["dropped_count"] == 1


def test_a_form_name_and_a_year_are_not_numbers():
    payload = accounting()
    payload["anomalies"][0]["what"] = "the 10-Q for fiscal 2026 says so"
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    assert out["dropped_count"] == 0


def test_a_path_that_is_not_a_number_drops_the_item():
    payload = accounting()
    payload["anomalies"][0]["what"] = "{ratios.efficiency.nothing_here}"
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    assert out["anomalies"] == []


def test_an_evidence_id_no_report_carries_drops_the_item():
    payload = accounting()
    payload["anomalies"][0]["evidence"] = ["revenue_recognition_invented"]
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    assert out["anomalies"] == []


def test_a_quote_not_in_the_named_report_drops_the_adjustment():
    payload = accounting()
    payload["adjustments"][0]["quote"] = "payment terms were never changed"
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    assert out["adjustments"] == []


def test_a_quote_folds_whitespace_one_for_one_as_the_quote_gate_does():
    """The owner's fold of 2026-09-23: each whitespace character reads as one space,
    one for one, and a quote that stood only through it is counted. A run of two
    spaces against one is not the same text and is not folded into it."""
    payload = accounting()
    payload["adjustments"][0]["quote"] = "extended payment\nterms to certain customers"
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    assert len(out["adjustments"]) == 1
    assert out["normalized_quotes"] == 1
    payload["adjustments"][0]["quote"] = "extended  payment terms to certain customers"
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    assert out["adjustments"] == []


def test_an_anomaly_that_cites_nothing_is_dropped():
    payload = accounting()
    payload["anomalies"][0]["evidence"] = []
    payload["anomalies"][0]["fields"] = []
    payload["anomalies"][0]["what"] = "something is off"
    assert analysis_check.check("accounting", payload, fields=FIELDS,
                                sources=SOURCES)["anomalies"] == []


def test_a_bare_four_digit_number_is_a_number_and_a_named_year_is_not():
    payload = accounting()
    payload["anomalies"][0]["what"] = "inventory of 2048 million"
    assert analysis_check.check("accounting", payload, fields=FIELDS,
                                sources=SOURCES)["anomalies"] == []
    payload["anomalies"][0]["what"] = "since fiscal 2024, under ASC 606 and ASU 2022-04, in Note 12"
    assert analysis_check.check("accounting", payload, fields=FIELDS,
                                sources=SOURCES)["dropped_count"] == 0


def test_a_derivative_or_a_korean_ruled_out_word_is_caught():
    for text in ("fraudulent activity", "the figures were manipulated", "분식 의심"):
        payload = accounting()
        payload["anomalies"][0]["what"] = text
        assert analysis_check.check("accounting", payload, fields=FIELDS,
                                    sources=SOURCES)["anomalies"] == [], text


def test_the_korean_name_is_held_to_the_same_rule():
    payload = accounting()
    payload["anomalies"][0]["name_ko"] = "매출채권 61일"
    assert analysis_check.check("accounting", payload, fields=FIELDS,
                                sources=SOURCES)["anomalies"] == []


def test_a_brace_that_is_not_a_placeholder_drops_the_item():
    payload = accounting()
    payload["anomalies"][0]["what"] = "DSO { ratios.efficiency.days_sales_outstanding }"
    assert analysis_check.check("accounting", payload, fields=FIELDS,
                                sources=SOURCES)["anomalies"] == []


def test_the_ruled_out_words_drop_their_item():
    payload = accounting()
    payload["anomalies"][0]["what"] = "this looks like fraud"
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    assert out["anomalies"] == []


def test_a_failing_area_keeps_its_name_and_says_it_was_dropped():
    payload = accounting()
    payload["areas"]["cost_deferral"]["finding"] = "capitalized cost rose 12 percent"
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    assert "dropped" in out["areas"]["cost_deferral"]
    assert set(out["areas"]) == set(analysis_check.ACCOUNTING_AREAS)


def test_an_area_left_out_is_named_as_missing():
    payload = accounting()
    del payload["areas"]["industry_lens"]
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    assert out["areas"]["industry_lens"] == {"dropped": "the analyst wrote nothing for it"}


def test_a_contradiction_is_an_outcome_and_a_made_up_one_is_not():
    payload = accounting()
    payload["reconciliation"][0]["outcome"] = "contradicts"
    assert analysis_check.check("accounting", payload, fields=FIELDS,
                                sources=SOURCES)["reconciliation"]
    payload["reconciliation"][0]["outcome"] = "mostly fine"
    assert not analysis_check.check("accounting", payload, fields=FIELDS,
                                    sources=SOURCES)["reconciliation"]


def test_an_anomaly_id_starts_with_its_area():
    payload = accounting()
    payload["anomalies"][0]["id"] = "receivables_outrun_revenue"
    assert analysis_check.check("accounting", payload, fields=FIELDS,
                                sources=SOURCES)["anomalies"] == []


def test_the_limits_sentence_is_the_rules_version_own():
    payload = accounting(limits="we looked hard")
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    assert out["limits"] == analysis_check.LIMITS["accounting"]
    assert any(row["where"] == "limits" for row in out["dropped_items"])


def test_the_valuation_analysis_may_not_say_buy():
    payload = {"value_range": {"reading": "a buy at this range", "fields": []},
               "price_position": {"reading": "not computed", "fields": []},
               "market_implied_growth": {"reading": "not computed", "fields": []},
               "accounting_adjustments": {"reading": "none", "fields": []},
               "most_sensitive": [], "summary_ko": {}, "limits": ""}
    out = analysis_check.check("valuation", payload, fields=FIELDS, sources={})
    assert "dropped" in out["value_range"]


def test_an_assumption_scenario_without_a_reason_is_dropped_whole():
    driver = {"reason": "the base case", "fields": ["ratios.profitability.gross_margin"]}
    scenario = {name: 0.02 for name in ("revenue_growth_year_one", "terminal_growth",
                                         "operating_margin_year_one",
                                         "operating_margin_year_ten",
                                         "reinvestment_rate_year_one",
                                         "reinvestment_rate_year_ten")}
    good = dict(scenario, reasons={name: driver for name in scenario})
    bad = dict(scenario, reasons={})
    out = analysis_check.check_assumptions({"scenarios": {"bear": bad, "base": good,
                                                          "bull": good}},
                                           fields=FIELDS, sources={})
    assert set(out["scenarios"]) == {"base", "bull"}
    assert out["dropped_count"] == 1


# --- the memo ---------------------------------------------------------------------------

def test_the_memo_puts_the_calculators_number_where_the_path_was():
    """61.25 days is written '61.2일' or '61.3일'; Python's own format rounds half to even
    on the binary value, so the test reads it as one decimal of 61.25."""
    text = memo.fill("회전일수 {ratios.efficiency.days_sales_outstanding}", FIELDS)
    assert text == f"회전일수 {61.25:,.1f}일"
    assert memo.fill("{ratios.profitability.gross_margin|pct}", FIELDS) == "40.0%"
    assert memo.fill("{terms.trailing_four_quarters.revenue}", FIELDS) == "15.0억 달러"


def test_the_memo_prints_a_unit_once_and_a_particle_that_agrees_with_it():
    """The CSCO memo of 2026-09-28 printed "37.2일일" and "65.2억 달러과". Expected
    Korean worked by hand: 달러 ends in a vowel, so 과 becomes 와 and 이 becomes 가;
    % is read 퍼센트, so 을 becomes 를; 5 is read 오 and 0 is read 영, so 1.5 takes
    로 and 2.50 takes 으로; 일 ends in ㄹ, which takes 로, never 으로."""
    fill = memo.fill
    assert fill("회전일수 {ratios.efficiency.days_sales_outstanding}일로 높다", FIELDS) \
        == f"회전일수 {61.25:,.1f}일로 높다"
    assert fill("매출 {terms.trailing_four_quarters.revenue}과 이익", FIELDS) == "매출 15.0억 달러와 이익"
    assert fill("매출 {terms.trailing_four_quarters.revenue}이 늘고", FIELDS) == "매출 15.0억 달러가 늘고"
    assert fill("{ratios.profitability.gross_margin|pct}%을 넘어", FIELDS) == "40.0%를 넘어"
    assert fill("{ratios.liquidity.current_ratio}으로", FIELDS) == "2.500으로"
    assert fill("{ratios.efficiency.days_sales_outstanding}으로", FIELDS) == f"{61.25:,.1f}일로"
    # a syllable that is not a particle stays as the analyst wrote it
    assert fill("{ratios.liquidity.current_ratio}이상", FIELDS) == "2.500이상"


def test_the_memo_keeps_the_three_analyses_apart_and_adds_nothing_up():
    checked = analysis_check.check("accounting", accounting(), fields=FIELDS, sources=SOURCES)
    text = memo.memo(ticker="TEST", form="10-Q", period_end="2026-06-30", cutoff="2026-07-30",
                     fields=FIELDS, accounting=checked, financial=None, valuation=None,
                     baselines=None)
    # Two top-level sections, 회계 and 재무, by the owner's decision of 2026-10-06;
    # the financial analysis and the valuation are the two subsections of 재무.
    assert (text.index("\n## 1. 회계\n") < text.index("\n### 1.1 회계 분석")
            < text.index("\n## 2. 재무\n") < text.index("\n### 2.1 재무 분석")
            < text.index("\n### 2.2 가치평가"))
    analyses = text[:text.index("\n## 참고")]
    assert [line for line in analyses.splitlines() if line.startswith("## ")] == [
        "## 1. 회계", "## 2. 재무"]
    assert "no price" in text
    for word in ("종합 점수", "순위", "매수", "매도"):
        assert word not in text.replace("회사 간 순위는 없습니다", "")


def test_a_trend_table_label_with_hyphens_is_a_path():
    payload = accounting()
    payload["anomalies"][0]["what"] = "gross margin {trend_table.quarters-back-0.ratios.gross_margin|pct}"
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    assert out["dropped_count"] == 0


def test_a_cited_field_that_states_why_it_has_no_value_stands_but_not_in_a_sentence():
    payload = accounting()
    payload["anomalies"][0]["fields"] = ["ratios.liquidity.cash_runway_months"]
    assert analysis_check.check("accounting", payload, fields=FIELDS,
                                sources=SOURCES)["dropped_count"] == 0
    payload["anomalies"][0]["what"] = "runway {ratios.liquidity.cash_runway_months}"
    assert analysis_check.check("accounting", payload, fields=FIELDS,
                                sources=SOURCES)["anomalies"] == []


def test_a_filing_date_an_item_number_and_a_form_before_a_korean_particle_are_not_numbers():
    payload = accounting()
    payload["anomalies"][0]["what"] = "an 8-K filed 2026-07-02 under Item 5.02"
    payload["summary_ko"]["earnings_versus_cash"] = "임원 변동 8-K의 본문은 없습니다."
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    assert out["dropped_count"] == 0


def test_the_memo_never_prints_what_the_gate_dropped():
    payload = accounting()
    payload["areas"]["cost_deferral"]["finding"] = "capitalized cost rose 12 percent, fraud risk"
    checked = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
    text = memo.memo(ticker="TEST", form="10-Q", period_end="2026-06-30", cutoff="2026-07-30",
                     fields=FIELDS, accounting=checked, financial=None, valuation=None,
                     baselines=None)
    assert "12 percent" not in text and "fraud" not in text
    assert "제외된 문장" in text


def test_the_memo_names_a_cost_of_debt_fallback_where_the_calculator_labels_one():
    """The decision of docs/needs_judgment.md: the fallback is labelled in
    calculator.json and in the memo. With `cost_of_capital.pre_tax_cost_of_debt.fallback`
    the valuation section carries one line with the label verbatim; without it, no
    such line, and the memo prints no number of its own either way."""
    label = ("the risk-free rate plus one point, because neither interest expense nor "
             "interest paid is on record: interest_expense: no row")
    with_fallback = copy.deepcopy(FIELDS)
    with_fallback["cost_of_capital"] = {"pre_tax_cost_of_debt": {"value": 0.0566,
                                                                   "fallback": label}}
    text = memo.memo(ticker="TEST", form="10-Q", period_end="2026-06-30", cutoff="2026-07-30",
                     fields=with_fallback, accounting=None, financial=None, valuation=None,
                     baselines=None)
    valuation = text[text.index("## 3. 가치평가"):text.index("## 참고")]
    assert memo.FALLBACK_KO in valuation
    assert label in valuation
    assert "0.0566" not in text and "5.66" not in text

    without = copy.deepcopy(FIELDS)
    without["cost_of_capital"] = {"pre_tax_cost_of_debt": {"value": 0.05}}
    text = memo.memo(ticker="TEST", form="10-Q", period_end="2026-06-30", cutoff="2026-07-30",
                     fields=without, accounting=None, financial=None, valuation=None,
                     baselines=None)
    assert memo.FALLBACK_KO not in text and "risk-free" not in text
    assert memo.cost_of_debt_fallback_line(FIELDS) == []


def test_the_control_cites_the_paragraphs_of_its_own_input():
    sources = {"input_notes.md": "[acc:notes:1] We extended payment terms to certain customers.\n"}
    payload = accounting()
    payload["anomalies"][0]["evidence"] = ["acc:notes:1"]
    payload["reconciliation"] = []
    payload["adjustments"][0]["quote_from"] = "input_notes.md"
    for area in payload["areas"].values():
        area["evidence"] = ["acc:notes:1"]
    out = analysis_check.check("accounting", payload, fields=FIELDS, sources=sources,
                               paragraph_ids=True)
    assert out["dropped_count"] == 0


def test_a_bare_year_in_a_reason_is_a_year_not_a_number():
    """GNRC's and LFUS's scenarios of 2026-09-29 were dropped for these words
    (their assumptions.json dropped_items)."""
    for text in ("the second half of 2026", "through 2027, then flat", "laps in December 2026",
                 "the June 2026 quarter", "year-end 2025",
                 # the second lens's cases of 2026-10-06: a year-context word before or
                 # after, a range dash, a fiscal prefix, a Korean year suffix
                 "in 2026", "fiscal 2027 guidance", "through 2030", "2026년",
                 "December 2026", "FY2026", "the second half of 2026", "2026 outlook",
                 "mid-2026", "as of 2026", "2026 하반기",
                 # phrasings the eight published analyses of 2026-09-29 use
                 "the first six months of 2026", "a first-quarter 2026 amendment",
                 "notes due 2030", "far above 2022's",
                 "회계연도 2025 수준", "the fiscal-2025 figure",
                 # a date or a range after a context word is read whole (AAPL's valuation
                 # analyst quoted "no row for interest_expense in 2024-09-29..2025-09-27")
                 "no row in 2024-09-29..2025-09-27", "in 2024-2026", "in 2024–2026",
                 # the third reading's cases: a year-terminator after the context word's
                 # year, and a list that borrows its context from a member
                 "by 2030.", "by 2030,", "in 2030 and 2031", "in 2026 the company",
                 "2021 and 2022 guidance", "the first six months of 2026 ran at"):
        payload = accounting()
        payload["anomalies"][0]["what"] = text
        assert analysis_check.check("accounting", payload, fields=FIELDS,
                                    sources=SOURCES)["dropped_count"] == 0, text


def test_a_number_that_looks_like_a_year_is_still_a_number():
    for text in ("revenue of $2026 thousand", "a ratio of 2026.5", "2030 employees",
                 "2026 million of backlog", "1,995 units", "a 2049 percent rise"):
        payload = accounting()
        payload["anomalies"][0]["what"] = text
        assert analysis_check.check("accounting", payload, fields=FIELDS,
                                    sources=SOURCES)["anomalies"] == [], text


def test_a_quantity_with_no_unit_word_is_still_a_number():
    """The second lens's finding of 2026-10-06: none of these carries a unit word on
    any list, and none has a year-context word around it, so each is a number the
    analyst wrote. "inventory of 2048" is the case the comment in
    `src/analysis_check.py` has always named."""
    for text in ("inventory of 2048", "backlog rose to 2030 orders", "2026 stores", "€2026",
                 "USD 2026", "2026 Million", "2026 bn", "-2026", "margin 2026",
                 "from 2026 onward", "leases to 2040", "2021 and 2022 units", "(2025)",
                 "due 2030 shares",
                 # the second lens's third reading: a bare noun after the year, "by" with
                 # an amount, and a range or list with no context word of its own
                 "cut headcount by 2030", "grew by 2026", "a rise in 2030 orders",
                 "backlog grew by 2030 orders", "up by 1999", "in 2030 and 2031 orders",
                 "inventory of 2021 and 2022", "2024–2026",
                 # GNRC's valuation analyst of 2026-09-29 wrote these with "of" alone
                 "the margins of 2021, 2022 and 2023", "the growth of 2021 and 2022"):
        payload = accounting()
        payload["anomalies"][0]["what"] = text
        out = analysis_check.check("accounting", payload, fields=FIELDS, sources=SOURCES)
        assert out["anomalies"] == [], text
        assert "a number written in the analyst's own words" in json.dumps(
            out["dropped_items"], ensure_ascii=False), text


def test_a_quantity_after_a_year_word_or_a_notes_word_is_still_a_number():
    for text in ("grew by 1950 basis points", "sold in 2048 units", "senior notes 25 million",
                 "non-recurring items 12 percent"):
        payload = accounting()
        payload["anomalies"][0]["what"] = text
        assert analysis_check.check("accounting", payload, fields=FIELDS,
                                    sources=SOURCES)["anomalies"] == [], text


def test_innocent_korean_words_are_not_the_ruled_out_ones():
    payload = accounting()
    payload["anomalies"][0]["what"] = "사기업 고객과 검사기 재고, 자사주 매수, 매도가능증권"
    assert analysis_check.check("accounting", payload, fields=FIELDS,
                                sources=SOURCES)["dropped_count"] == 0


def test_an_adjustment_amount_is_a_dollar_cell_and_nothing_else():
    payload = accounting()
    payload["adjustments"][0]["calculator_field"] = "ratios.efficiency.days_sales_outstanding"
    assert analysis_check.check("accounting", payload, fields=FIELDS,
                                sources=SOURCES)["adjustments"] == []


def test_a_quarter_of_a_year_stands_and_a_labelled_quantity_does_not():
    payload = accounting()
    payload["anomalies"][0]["what"] = "Q4 2026 guidance, Q2 of fiscal 2027"
    assert analysis_check.check("accounting", payload, fields=FIELDS,
                                sources=SOURCES)["dropped_count"] == 0
    for text in ("Note 12 million", "Item 12 million", "ASC 606 million"):
        payload["anomalies"][0]["what"] = text
        assert analysis_check.check("accounting", payload, fields=FIELDS,
                                    sources=SOURCES)["anomalies"] == [], text
