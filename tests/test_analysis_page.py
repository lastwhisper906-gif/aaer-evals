"""The one-page view of every run's accounting and financial analysis.

Every expected value is a rule applied by hand: the page prints each Korean
sentence exactly as the run's memo prints it (one reading, `src/memo.py`), a
dropped sentence as dropped, each key figure as the memo prints that `{path}`,
no valuation and no price, the companies by ticker and, within one, the newest
filing first with a rerun before the run it repeats; and a dollar amount whose
path ends in a quarter, an index or an input's side prints in dollars, as the
metric it belongs to is named, and share-based pay in dollars.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from src import analysis_page, memo

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "runs"
DELL = RUNS / "DELL" / "0001571996-26-000046"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_each_sentence_is_the_line_the_memo_prints_for_it():
    entry = analysis_page.run_entry(DELL)
    fields = _load(DELL / "calculator.json")
    seen = _load(DELL / "calculator_filings_only.json")
    lines = memo.memo(ticker="DELL", form="10-Q", period_end=fields["period_end"],
                      cutoff=fields["cutoff"], fields=fields,
                      accounting=_load(DELL / "analysis_accounting.json"),
                      financial=_load(DELL / "analysis_financial.json"),
                      valuation=None, baselines=None, filings_only=seen).splitlines()
    for area in entry["accounting"]["areas"]:
        assert f"- **{area['name']}**: {area['text']}" in lines
    for section in entry["financial"]["sections"]:
        assert f"- **{section['name']}**: {section['text']}" in lines
    assert len(entry["accounting"]["areas"]) == len(memo.ACCOUNTING_KO)
    assert len(entry["financial"]["sections"]) == len(memo.FINANCIAL_KO)


def test_every_anomaly_the_analysts_listed_is_on_the_page():
    entry = analysis_page.run_entry(DELL)
    for frame in ("accounting", "financial"):
        listed = _load(DELL / f"analysis_{frame}.json")["anomalies"]
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


def test_a_dropped_area_shows_as_dropped_and_its_original_is_not_quoted():
    analysis = {"areas": {"revenue_recognition": {"dropped": "a digit in the analyst's words"}},
                "summary_ko": {"revenue_recognition": None}, "anomalies": []}
    seen = {"free_cash_flow": {}}
    out = analysis_page.accounting(analysis, seen, seen)
    area = next(a for a in out["areas"] if a["key"] == "revenue_recognition")
    assert area["text"] == memo.DROPPED_KO
    assert "original" not in area and "verdict" not in area


def test_the_page_holds_no_valuation_and_no_price():
    entry = analysis_page.run_entry(DELL)
    assert "valuation" not in entry
    text = json.dumps(entry, ensure_ascii=False)
    assert "price_at_cutoff" not in text and "주당" not in text


def test_companies_by_ticker_newest_filing_first_and_a_rerun_before_its_run():
    entries = analysis_page.collect(RUNS)
    tickers = [e["ticker"] for e in entries]
    assert tickers == sorted(tickers)
    for ticker in set(tickers):
        mine = [e for e in entries if e["ticker"] == ticker]
        dates = [e["filing_date"] for e in mine]
        assert dates == sorted(dates, reverse=True)
        for a, b in zip(mine, mine[1:]):
            if a["filing_date"] == b["filing_date"]:
                assert a["rerun"] or not b["rerun"]
    published = {p.parent.parent.name + "/" + p.parent.name
                 for p in RUNS.glob("*/*/analysis_accounting.json")
                 if (p.parent / "analysis_financial.json").is_file()}
    assert {e["run"] for e in entries} == published


def test_text_cannot_close_the_data_script():
    html = analysis_page.page([{"ticker": "X", "note": "</script><b>"}])
    data = re.search(r'<script id="runs-data" type="application/json">(.*?)</script>', html, re.S)
    assert json.loads(data.group(1))[0]["note"] == "</script><b>"


def test_an_amount_named_by_its_metric_prints_in_dollars():
    fields = {"ratios": {"growth": {"operating_cash_flow": {
        "this_quarter": 2_231_000_000.0,
        "year_over_year": {"value": 0.1, "inputs": {"before": 2_031_000_000.0}}}}},
        "earnings_versus_cash": {"smoothness": {"net_income": [125_213_000.0, -242_135_000.0]},
                                 "history": {"years": [{"share_based_compensation": 3.641e9}]}}}
    assert memo.fill("{ratios.growth.operating_cash_flow.this_quarter}", fields) == "22.3억 달러"
    assert memo.fill("{ratios.growth.operating_cash_flow.year_over_year.inputs.before}",
                     fields) == "20.3억 달러"
    assert memo.fill("{earnings_versus_cash.smoothness.net_income.1}", fields) == "-2.4억 달러"
    assert memo.fill("{ratios.growth.operating_cash_flow.year_over_year|pct}", fields) == "10.0%"
    assert memo.fill("{earnings_versus_cash.history.years.0.share_based_compensation}",
                     fields) == "36.4억 달러"
    assert memo.unit_of("concentration.facts.3", 0.16) == "ratio"
