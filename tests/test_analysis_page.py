"""The one-page view of every run's accounting and financial analysis.

Every expected value is a rule applied by hand: the page prints each Korean
sentence exactly as the run's memo prints it (one reading, `src/memo.py`), from
the file the analysts were handed and not from the final calculator; a dropped
sentence as dropped and nothing of its English; the free cash flow after the
accounting adjustments where the page says so; no valuation and no price; the
companies by ticker and, within one, the newest filing first with a rerun before
the run it repeats; and no text in the data can end the element that holds it.
The memo's units are worked by hand: a dollar amount whose path ends in a
quarter, an index, a part or an input's side prints in dollars, a cell read as
`.value` prints in the cell's own unit, and share-based pay in dollars.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from src import analysis_page, memo

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "runs"
PUBLISHED = sorted(p.parent for p in RUNS.glob("*/*/analysis_accounting.json")
                   if (p.parent / "analysis_financial.json").is_file())


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _memo_lines(run: Path, *, view: str = "calculator_filings_only.json") -> list[str]:
    fields = _load(run / "calculator.json")
    return memo.memo(ticker=fields["ticker"], form=fields["form"],
                     period_end=fields["period_end"], cutoff=fields["cutoff"], fields=fields,
                     accounting=_load(run / "analysis_accounting.json"),
                     financial=_load(run / "analysis_financial.json"),
                     valuation=None, baselines=None,
                     filings_only=_load(run / view)).splitlines()


@pytest.mark.parametrize("run", PUBLISHED, ids=lambda p: f"{p.parent.name}/{p.name}")
def test_each_sentence_is_the_line_the_memo_prints_for_it(run):
    entry = analysis_page.run_entry(run)
    lines = _memo_lines(run)
    for area in entry["accounting"]["areas"]:
        assert f"- **{area['name']}**: {area['text']}" in lines
    for section in entry["financial"]["sections"]:
        assert f"- **{section['name']}**: {section['text']}" in lines
    assert len(entry["accounting"]["areas"]) == len(memo.ACCOUNTING_KO)
    assert len(entry["financial"]["sections"]) == len(memo.FINANCIAL_KO)


def test_the_sentences_come_from_the_view_the_analysts_were_handed():
    # where the final calculator reads a path differently, the page must follow
    # the analysts' view; at least one published run has such a sentence, so a
    # page filled from calculator.json fails the test above
    differs = 0
    for run in PUBLISHED:
        if (run / "calculator_filings_only.json").is_file():
            differs += _memo_lines(run) != _memo_lines(run, view="calculator.json")
    assert differs


def test_every_anomaly_the_analysts_listed_is_on_the_page():
    run = RUNS / "DELL" / "0001571996-26-000046"
    entry = analysis_page.run_entry(run)
    for frame in ("accounting", "financial"):
        listed = _load(run / f"analysis_{frame}.json")["anomalies"]
        assert [a["id"] for a in entry[frame]["anomalies"]] == [a["id"] for a in listed]
    outcomes = {a["outcome"] for a in entry["accounting"]["anomalies"]}
    assert outcomes <= {"contradicts", "unresolved", "confirms", None}


def test_a_key_figure_is_the_number_the_memo_prints_for_its_path():
    seen = {"ratios": {"profitability": {"gross_margin": {"value": 0.4, "unit": "ratio"}},
                       "efficiency": {"days_sales_outstanding": {"value": 61.25, "unit": "days"}}}}
    shown = analysis_page.figures(seen, (("매출총이익률", "ratios.profitability.gross_margin|pct"),
                                         ("매출채권회수일수", "ratios.efficiency.days_sales_outstanding"),
                                         ("유동비율", "ratios.liquidity.current_ratio")))
    assert [f["text"] for f in shown] == ["40.0%", "61.2일", "계산되지 않음"]
    assert [f["missing"] for f in shown] == [False, False, True]
    assert shown[0]["path"] == "ratios.profitability.gross_margin"


def test_the_adjusted_free_cash_flow_is_read_after_the_adjustments():
    path = "free_cash_flow.free_cash_flow_quality_adjusted"
    seen = {"free_cash_flow": {"free_cash_flow_quality_adjusted": {
        "value": 7.75e9, "unit": "USD", "adjustments_applied": []}}}
    final = {"free_cash_flow": {"free_cash_flow_quality_adjusted": {
        "value": 4.65e9, "unit": "USD", "adjustments_applied": [{"amount": 3.1e9}]}}}
    shown = analysis_page.figures(seen, (("잉여현금흐름", path),
                                         ("매출총이익률", "ratios.profitability.gross_margin|pct")),
                                  final)
    assert shown[0]["text"] == "46.5억 달러"
    assert shown[1]["missing"]          # every other figure is the analysts' view


def test_a_dropped_sentence_shows_as_dropped_and_nothing_of_its_english():
    # the gate drops the whole area ...
    analysis = {"areas": {"revenue_recognition": {"dropped": "a digit in the analyst's words"}},
                "summary_ko": {"revenue_recognition": None}, "anomalies": []}
    out = analysis_page.accounting(analysis, {}, {})
    area = next(a for a in out["areas"] if a["key"] == "revenue_recognition")
    assert area["text"] == memo.DROPPED_KO
    assert "original" not in area and "verdict" not in area
    # ... or the Korean sentence only, the English reading standing
    analysis = {"sections": {"liquidity": {"reading": "Liquidity is ample."}},
                "summary_ko": {"liquidity": None, "solvency": "부채는 적습니다."},
                "anomalies": []}
    out = analysis_page.financial(analysis, {})
    liquidity = next(s for s in out["sections"] if s["key"] == "liquidity")
    assert liquidity["text"] == memo.DROPPED_KO
    assert "original" not in liquidity


def _plant(root: Path, ticker: str, name: str, filed: str, *, price: float | None = None):
    run = root / ticker / name
    run.mkdir(parents=True)
    calculator = {"ticker": ticker, "form": "10-Q", "period_end": filed, "cutoff": filed,
                  "accession": name.split("-rerun")[0]}
    if price is not None:
        calculator["valuation"] = {"price_at_cutoff": {"value": price, "unit": "USD per share"}}
    (run / "calculator.json").write_text(json.dumps(calculator))
    (run / "analysis_accounting.json").write_text(json.dumps({"anomalies": []}))
    (run / "analysis_financial.json").write_text(json.dumps({"anomalies": []}))


def test_companies_by_ticker_newest_filing_first_and_a_rerun_before_its_run(tmp_path):
    _plant(tmp_path, "ZZZ", "0000000001-26-000001", "2026-01-30")
    _plant(tmp_path, "ZZZ", "0000000001-26-000009", "2026-07-30")
    _plant(tmp_path, "ZZZ", "0000000001-26-000009-rerun-2026-10-28", "2026-07-30")
    _plant(tmp_path, "AAA", "0000000002-26-000004", "2026-05-01")
    _plant(tmp_path, "BBB", "0000000003-26-000004", "2026-05-01")
    (tmp_path / "BBB" / "0000000003-26-000004" / "analysis_financial.json").unlink()
    got = [e["run"] for e in analysis_page.collect(tmp_path)]
    assert got == ["AAA/0000000002-26-000004",
                   "ZZZ/0000000001-26-000009-rerun-2026-10-28",
                   "ZZZ/0000000001-26-000009",
                   "ZZZ/0000000001-26-000001"]


def test_every_published_run_with_both_analyses_is_on_the_page():
    assert {e["run"] for e in analysis_page.collect(RUNS)} == {
        f"{p.parent.name}/{p.name}" for p in PUBLISHED}


def test_the_page_holds_no_valuation_and_no_price(tmp_path):
    _plant(tmp_path, "ZZZ", "0000000001-26-000001", "2026-01-30", price=271.35)
    page = analysis_page.page(analysis_page.collect(tmp_path))
    assert "271.35" not in page and "271" not in page
    entry = analysis_page.collect(tmp_path)[0]
    assert "valuation" not in entry


@pytest.mark.parametrize("text", ["</script><b>", "<!--<script>", "a < b > c & d"])
def test_text_in_the_data_cannot_end_or_swallow_its_element(text):
    html = analysis_page.page([{"ticker": "X", "note": text}])
    data = re.search(r'<script id="runs-data" type="application/json">(.*?)</script>', html, re.S)
    assert "<" not in data.group(1)
    assert json.loads(data.group(1))[0]["note"] == text


def test_an_amount_named_by_its_metric_prints_in_dollars():
    fields = {"ratios": {"growth": {"operating_cash_flow": {
        "this_quarter": 2_231_000_000.0,
        "year_over_year": {"value": 0.1, "inputs": {"before": 2_031_000_000.0}}}}},
        "earnings_versus_cash": {"smoothness": {"net_income": [125_213_000.0, -242_135_000.0]},
                                 "history": {"years": [{"share_based_compensation": 3.641e9}]}},
        "terms": {"debt_now": {"parts": {"debt_current": {"lines_not_added": [
            {"value": 916_000_000.0}]}}}}}
    assert memo.fill("{ratios.growth.operating_cash_flow.this_quarter}", fields) == "22.3억 달러"
    assert memo.fill("{ratios.growth.operating_cash_flow.year_over_year.inputs.before}",
                     fields) == "20.3억 달러"
    assert memo.fill("{earnings_versus_cash.smoothness.net_income.1}", fields) == "-2.4억 달러"
    assert memo.fill("{earnings_versus_cash.history.years.0.share_based_compensation}",
                     fields) == "36.4억 달러"
    assert memo.fill("{terms.debt_now.parts.debt_current.lines_not_added.0.value}",
                     fields) == "9.2억 달러"
    assert memo.fill("{ratios.growth.operating_cash_flow.year_over_year|pct}", fields) == "10.0%"
    assert memo.unit_of("concentration.facts.3", 0.16) == "ratio"
    assert memo.unit_of("ratios.efficiency.share_based_compensation_over_revenue", 0.05) == "ratio"


def test_a_cell_read_as_value_prints_in_the_cells_unit():
    fields = {"ratios": {"efficiency": {"days_sales_outstanding": {"value": 23.04, "unit": "days"}},
                         "liquidity": {"current_ratio": {"value": 1.003, "unit": "ratio"}}},
              "terms": {"shares_outstanding": {"value": 344_700_000.0, "unit": "shares"},
                        "trailing_four_quarters": {"revenue": {"value": 1.5e9, "unit": "USD"}}}}
    assert memo.fill("{ratios.efficiency.days_sales_outstanding.value}", fields) == "23.0일"
    assert memo.fill("{ratios.liquidity.current_ratio.value}", fields) == "1.003"
    assert memo.fill("{terms.shares_outstanding.value}", fields) == "344.7백만 주"
    assert memo.fill("{terms.trailing_four_quarters.revenue.value}", fields) == "15.0억 달러"
