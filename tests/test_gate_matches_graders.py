"""Every gate of the pipeline at least as strict as the owner's grader it answers to.

The first four Opus runs (2026-10-07) passed every pipeline gate and failed the
owner's regression graders, and each probe below is a shape a later run could
fail the same way: the gate kept what the grader refuses. Each test writes what
an analyst could write, runs the pipeline's own gate on it, and runs the owner's
grader (`evals/regression/`, imported here and never written) both on what the
analyst wrote, published as it stood, and on what the gate let through. The
grader refuses the first and passes the second, so the two rules cannot drift
apart again without a test saying so.

The run built here is small and written by hand: two reader directories holding
two paragraphs of ESE's earnings release 0001104659-26-092033 as its run
0001104659-26-093266 printed them, a reader report each, and an accounting
analyst handed the two reports and a calculator.
"""

from __future__ import annotations

import copy
import json
import math
from pathlib import Path

import pytest

from evals.common import PASS
from evals.regression import coverage, mechanical
from src import agent_inputs, analysis_check, calculator, extraction_checks, memo, run_analysis

ACCESSION = "0001104659-26-093266"
SALES_ID = "0001104659-26-092033:8k_2_02:36"
EPS_ID = "0001104659-26-092033:8k_2_02:37"
SALES = ("Raising the lower end of FY 2026 Sales guidance and now expect Sales to be in the "
         "range of $1.30 to $1.33 billion (19 to 21 percent growth over the prior year).")
EPS = ("Raising full year Adjusted EPS guidance to a range of $8.30 - $8.40 per share (38 to "
       "39 percent growth)")
# ESE's input_8k.md opens with the item codes of every 8-K on or before the cutoff,
# before its first [id] line (the valuation analyst could quote that list).
ITEM_CODES = "2026-06-03 0001104659-26-070116 — 1.01, 1.02, 2.03, 9.01"
EIGHT_K = ("# ESE 8-K — 0001104659-26-092033 filed 2026-08-06\n\n"
           "## item codes, every 8-K on or before 2026-08-10\n\n"
           f"- {ITEM_CODES}\n\n## item 2.02 — earnings release, exhibit 99.1\n\n"
           f"[{SALES_ID}]\n|  | · | {SALES} |\n\n"
           f"[{EPS_ID}]\n|  | · | {EPS}, which reflects a midpoint increase of $0.70 per "
           "share. |\n")
SALES_ITEM = "results_against_expectations_sales_guidance_lower_end_raised"
EPS_ITEM = "results_against_expectations_adjusted_eps_guidance_raised"
# NVDA's notes reader wrote prose outside its fences; this line is its own.
READER_PROSE = "No auditor's report. input_controls.md is titled"
NUMBERS_REPORT = ("# numbers\n```json\n"
                  + json.dumps({"id": SALES_ITEM, "what_changed": "the low end rose",
                                "quote": SALES, "paragraph_id": SALES_ID}) + "\n```\n")
NOTES_REPORT = (f"# notes\n\n{READER_PROSE} \"Controls and Procedures\".\n\n```json\n"
                + json.dumps({"id": EPS_ITEM, "what_changed": "adjusted EPS guidance rose",
                              "quote": EPS, "paragraph_id": EPS_ID}) + "\n```\n")
FIELDS = {
    "ticker": "ESE", "form": "10-Q", "period_end": "2026-06-30", "cutoff": "2026-08-10",
    "ratios": {"liquidity": {"current_ratio": {"value": 2.5, "unit": "ratio"}},
               "efficiency": {"days_sales_outstanding": {"value": 61.25, "unit": "days"}}},
    "terms": {"trailing_four_quarters": {"revenue": {"value": 1.5e9, "unit": "USD"}}},
    "free_cash_flow": {"free_cash_flow_quality_adjusted": {"adjustments_applied": []}},
    "valuation": {"missing": "no price"},
}
AREA = {"finding": "Days sales outstanding is {ratios.efficiency.days_sales_outstanding}.",
        "verdict": "steady", "evidence": [SALES_ITEM],
        "fields": ["ratios.efficiency.days_sales_outstanding"]}
ANOMALY_ID = "earnings_versus_cash_guidance_raised_while_cash_lags"


def accounting() -> dict:
    return {
        "areas": {name: copy.deepcopy(AREA) for name in analysis_check.ACCOUNTING_AREAS},
        "reconciliation": [],
        "anomalies": [{"id": ANOMALY_ID, "name": "guidance raised while cash lags",
                       "name_ko": "가이던스 상향", "area": "earnings_versus_cash",
                       "what": "the release raised guidance", "numbers_vs_prose": "unresolved",
                       "evidence": [EPS_ITEM], "fields": [], "quote": EPS,
                       "quote_from": "report_notes_text.md"}],
        "adjustments": [],
        "summary_ko": {"earnings_versus_cash": "회전일수 {ratios.efficiency.days_sales_outstanding}"},
        "limits": analysis_check.LIMITS["accounting"],
    }


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _run(tmp_path: Path, *, notes: str = NOTES_REPORT, dropped=()) -> Path:
    """The run root, the two readers' directories and the accounting analyst's."""
    run = tmp_path / "run"
    _write(run / "input_manifest.json", json.dumps({
        "accession": ACCESSION, "dropped_items": [
            {"report": report, "item_id": item, "reason": "planted"}
            for report, item in dropped]}))
    _write(run / "input_8k.md", EIGHT_K)
    for reader in ("numbers-reader", "notes-text-reader"):
        _write(run / "agents" / reader / "input_8k.md", EIGHT_K)
    for name, text in (("report_numbers.md", NUMBERS_REPORT), ("report_notes_text.md", notes)):
        _write(run / name, text)
        _write(run / "agents" / "accounting-analyst" / name, text)
    for where in (run, run / "agents" / "accounting-analyst"):
        _write(where / "calculator_filings_only.json", json.dumps(FIELDS))
    return run


def _gate(run: Path, payload: dict) -> dict:
    """The accounting analysis through the pipeline's gate, as `check_analysis` runs it."""
    directory = run / "agents" / "accounting-analyst"
    sources = analysis_check.read_sources(directory, analysis_check.SOURCES["accounting"])
    return analysis_check.check("accounting", payload, fields=FIELDS, sources=sources,
                                excluded=run_analysis.excluded_by_report(run))


def _publish(run: Path, name: str, payload: dict) -> None:
    _write(run / name, json.dumps(payload, ensure_ascii=False))


def _both(run: Path, payload: dict, grader, name: str = "analysis_accounting.json"):
    """The grader on what the analyst wrote, published as it stood, and on what
    the gate let through."""
    _publish(run, name, payload)
    raw = grader(run)
    gated = _gate(run, payload)
    _publish(run, name, gated)
    return raw, grader(run), gated


def test_the_baseline_stands_at_the_gate_and_before_every_grader(tmp_path):
    run = _run(tmp_path)
    gated = _gate(run, accounting())
    assert gated["dropped_items"] == [], gated["dropped_items"]
    _publish(run, "analysis_accounting.json", gated)
    for grader in (mechanical.check_quotes_resolve, mechanical.check_cited_items_exist,
                   mechanical.check_cited_numbers_exist, coverage.check_forbidden_words,
                   coverage.check_no_combined_score, coverage.check_accounting_areas):
        result = grader(run)
        assert result.status == PASS, (result.grader, result.failures)


# --- quotes_resolve: an analyst's quote sits inside one unit of what it was handed ---------

def test_a_quote_of_the_reader_s_prose_outside_its_fences_is_dropped(tmp_path):
    """(a) NVDA's notes report carries 15.9k characters of prose outside its
    fenced items; a quote of it string-matches the file and is no item."""
    run = _run(tmp_path)
    payload = accounting()
    payload["anomalies"][0]["quote"] = READER_PROSE
    raw, gated, out = _both(run, payload, mechanical.check_quotes_resolve)
    assert raw.failures == ["analysis_accounting.json:anomalies[0]: in no one paragraph, value "
                            "or report item it was handed"]
    assert out["anomalies"] == [] and gated.status == PASS


def test_a_quote_of_an_item_the_gate_dropped_beside_a_kept_one_is_dropped(tmp_path):
    """(e) A dropped item still printed in a mixed block, quoted by the analyst."""
    mixed = ("# notes\n```json\n" + json.dumps([
        {"id": EPS_ITEM, "what_changed": "x", "quote": EPS, "paragraph_id": EPS_ID},
        {"id": "results_against_expectations_sales_restated", "what_changed": "y",
         "quote": "Raising the lower end", "paragraph_id": SALES_ID}]) + "\n```\n")
    run = _run(tmp_path, notes=mixed,
               dropped=[("report_notes_text.md", "results_against_expectations_sales_restated")])
    payload = accounting()
    payload["anomalies"][0]["quote"] = "Raising the lower end"
    _publish(run, "analysis_accounting.json", payload)
    assert any(line.startswith("analysis_accounting.json:anomalies[0]: in no one")
               for line in mechanical.check_quotes_resolve(run).failures)
    out = _gate(run, payload)
    assert out["anomalies"] == []
    assert "kept report item" in out["dropped_items"][0]["reason"]


def _valuation_run(tmp_path: Path) -> tuple[Path, dict, dict]:
    """The valuation analyst's first pass: the 8-K copy, the gated accounting
    analysis, and the calculator before its drivers."""
    run = _run(tmp_path)
    accounting_gated = _gate(run, accounting())
    _publish(run, "analysis_accounting.json", accounting_gated)
    directory = run / "agents" / "valuation-analyst"
    _write(directory / "input_8k.md", EIGHT_K)
    directory.mkdir(parents=True, exist_ok=True)
    run_analysis.write_json(directory / "analysis_accounting.json", accounting_gated)
    _write(directory / "calculator_before_drivers.json", json.dumps(FIELDS))
    _write(run / "calculator_before_drivers.json", json.dumps(FIELDS))
    sources = analysis_check.read_sources(directory, analysis_check.SOURCES["assumptions"])
    filing = {"input_8k.md": EIGHT_K}
    return run, sources, filing


def _scenarios(reason: dict) -> dict:
    drivers = {"revenue_growth_year_one": 0.05, "terminal_growth": 0.02,
               "operating_margin_year_one": 0.2, "operating_margin_year_ten": 0.2,
               "reinvestment_rate_year_one": 0.3, "reinvestment_rate_year_ten": 0.3}
    good = {"reason": "the release raised guidance", "quote": SALES[:40],
            "quote_from": "input_8k.md"}
    return {"scenarios": {"bear": dict(drivers, reasons={d: reason for d in drivers}),
                          "base": dict(drivers, reasons={d: good for d in drivers}),
                          "bull": dict(drivers, reasons={d: good for d in drivers})}}


@pytest.mark.parametrize("probe, quote, quote_from, owner_says", [
    ("(b) the 8-K's item-code list before its first [id] line", ITEM_CODES, "input_8k.md",
     "in no one paragraph"),
    ("(c) a quote of the accounting analysis across a key",
     'steady",\n   "evidence"', "analysis_accounting.json", "in no one paragraph"),
    ("(d) a quote that is an anomaly id", ANOMALY_ID, "analysis_accounting.json",
     "carries only key names")])
def test_a_valuation_quote_outside_one_unit_is_dropped(tmp_path, probe, quote, quote_from,
                                                       owner_says):
    run, sources, filing = _valuation_run(tmp_path)
    reason = {"reason": "a reason", "quote": quote, "quote_from": quote_from}
    assert analysis_check.fold(quote) in analysis_check.fold(sources[quote_from]), probe
    written = _scenarios(reason)
    _publish(run, "assumptions.json", written)
    raw = mechanical.check_quotes_resolve(run)
    assert any(line.startswith("assumptions.json:scenarios.bear") and owner_says in line
               for line in raw.failures), raw.failures
    out = analysis_check.check_assumptions(written, fields=FIELDS, sources=sources,
                                           filing=filing)
    assert set(out["scenarios"]) == {"base", "bull"}, probe
    _publish(run, "assumptions.json", out)
    assert mechanical.check_quotes_resolve(run).status == PASS


# --- quotes_resolve: every quote in the tree --------------------------------------------

def test_a_quote_nested_under_an_item_or_under_a_key_the_schema_does_not_name_is_held(tmp_path):
    run = _run(tmp_path)
    payload = accounting()
    payload["anomalies"][0]["support"] = [{"quote": "words the reports never printed",
                                           "quote_from": "report_numbers.md"}]
    payload["extra_top"] = {"quote": "another invented sentence nobody wrote",
                            "quote_from": "report_numbers.md"}
    raw, gated, out = _both(run, payload, mechanical.check_quotes_resolve)
    assert sorted(raw.failures) == [
        "analysis_accounting.json:anomalies[0].support[0]: in no one paragraph, value or "
        "report item it was handed",
        "analysis_accounting.json:extra_top: in no one paragraph, value or report item it "
        "was handed"]
    assert out["anomalies"] == [] and "extra_top" not in out
    assert gated.status == PASS


def test_a_scenario_the_calculator_does_not_run_is_removed(tmp_path):
    run, sources, filing = _valuation_run(tmp_path)
    good = {"reason": "a reason", "quote": SALES[:40], "quote_from": "input_8k.md"}
    written = _scenarios(good)
    written["scenarios"]["stress"] = dict(written["scenarios"]["base"], reasons={
        "revenue_growth_year_one": {"reason": "r", "quote": "never printed",
                                    "quote_from": "input_8k.md"}})
    _publish(run, "assumptions.json", written)
    assert mechanical.check_quotes_resolve(run).status != PASS
    out = analysis_check.check_assumptions(written, fields=FIELDS, sources=sources,
                                           filing=filing)
    assert set(out["scenarios"]) == {"bear", "base", "bull"}
    assert {"where": "scenarios.stress", "reason": "not one of bear, base, bull"} \
        in out["dropped_items"]
    _publish(run, "assumptions.json", out)
    assert mechanical.check_quotes_resolve(run).status == PASS


def test_a_quote_on_a_block_or_on_the_analysis_itself_is_held_and_the_block_stays(tmp_path):
    """The owner's `quoted` yields every object carrying a quote, the analysis
    itself and a block of areas too. A quote written on `areas` beside its
    entries goes and the eight areas stay answered (the gate used to remove the
    whole block); one written on the analysis object goes."""
    run = _run(tmp_path)
    payload = accounting()
    payload["areas"]["quote"] = "words the reports never printed"
    payload["areas"]["quote_from"] = "report_numbers.md"
    payload["quote"] = "another invented sentence nobody wrote"
    payload["quote_from"] = "report_numbers.md"
    raw, gated, out = _both(run, payload, mechanical.check_quotes_resolve)
    assert sorted(raw.failures) == [
        "analysis_accounting.json:: in no one paragraph, value or report item it was handed",
        "analysis_accounting.json:areas: in no one paragraph, value or report item it was "
        "handed"]
    assert gated.status == PASS
    assert "quote" not in out and "quote" not in out["areas"]
    assert coverage.check_accounting_areas(run).status == PASS
    assert all(coverage.answered(out["areas"][name]) == "answered"
               for name in coverage.ACCOUNTING_AREAS)


@pytest.mark.parametrize("nested, grader, owner_says", [
    ([{"reason": "the antifraud review"}], coverage.check_forbidden_words, "fraud"),
    ([{"reason": "rose to {ratios.liquidity.no_such_ratio}"}],
     mechanical.check_cited_numbers_exist, "ratios.liquidity.no_such_ratio"),
    ([{"overall_rank": "first"}], coverage.check_no_combined_score, "overall_rank")])
def test_a_dropped_items_key_below_the_top_is_the_analyst_s_words(tmp_path, nested, grader,
                                                                  owner_says):
    """Only the top-level `dropped_items` is the gate's own record, and the owner
    leaves only that one out of forbidden_words, cited_numbers_exist and
    no_combined_score: one an analyst writes inside an item is read like any
    other key. The gate used to pass over it at every depth."""
    run = _run(tmp_path)
    payload = accounting()
    payload["anomalies"][0]["dropped_items"] = nested
    raw, gated, out = _both(run, payload, grader)
    assert raw.status != PASS and any(owner_says in line for line in raw.failures)
    assert out["anomalies"] == [] and gated.status == PASS


def test_a_dropped_items_key_below_the_top_is_not_held_as_a_quote_or_a_citation(tmp_path):
    """The other side: the owner's `quoted` and cited_items_exist pass over a
    `dropped_items` at any depth, so a quote or an id written there is no
    departure, and the gate keeps the item that carries it."""
    run = _run(tmp_path)
    payload = accounting()
    payload["anomalies"][0]["dropped_items"] = [{"id": "no_such_item", "quote": "never printed",
                                                 "quote_from": "report_numbers.md"}]
    _publish(run, "analysis_accounting.json", payload)
    for grader in (mechanical.check_quotes_resolve, mechanical.check_cited_items_exist):
        assert grader(run).status == PASS, grader
    out = _gate(run, payload)
    assert [item["id"] for item in out["anomalies"]] == [ANOMALY_ID]


@pytest.mark.parametrize("key, value, owner_says", [
    ("line_items", ["no_such_item"], "analysis_accounting.json:line_items: no_such_item"),
    ("evidence", None, "analysis_accounting.json:evidence: evidence is not a list")])
def test_a_citation_key_at_the_top_of_the_analysis_is_held(tmp_path, key, value, owner_says):
    run = _run(tmp_path)
    payload = accounting()
    payload[key] = value
    raw, gated, out = _both(run, payload, mechanical.check_cited_items_exist)
    assert raw.failures == [owner_says]
    assert key not in out and gated.status == PASS


def test_what_the_assumptions_publish_as_written_is_held(tmp_path):
    """The assumptions gate overwrites only its drop list and count; a `limits`
    or `normalized_quotes` the valuation analyst writes is published as written
    and read by the owner (recommendation words, placeholders), so it is held."""
    run, sources, filing = _valuation_run(tmp_path)
    good = {"reason": "a reason", "quote": SALES[:40], "quote_from": "input_8k.md"}
    written = _scenarios(good)
    written["limits"] = "Investors should buy on weakness."
    written["normalized_quotes"] = ["see {nothing.here}"]
    _publish(run, "assumptions.json", written)
    assert coverage.check_forbidden_words(run).failures == ["assumptions.json:limits: buy"]
    assert mechanical.check_cited_numbers_exist(run).failures == [
        "assumptions.json:normalized_quotes[0]:nothing.here"]
    out = analysis_check.check_assumptions(written, fields=FIELDS, sources=sources,
                                           filing=filing)
    _publish(run, "assumptions.json", out)
    assert "limits" not in out and out["normalized_quotes"] == []
    assert set(out["scenarios"]) == {"bear", "base", "bull"}
    assert coverage.check_forbidden_words(run).status == PASS
    assert mechanical.check_cited_numbers_exist(run).status == PASS


# --- cited_items_exist ----------------------------------------------------------------

@pytest.mark.parametrize("key, value, owner_says", [
    ("evidence", None, "evidence is not a list"),
    ("evidence", "", "evidence is not a list"),
    ("line_items", ["no_such_item"], "no_such_item")])
def test_an_evidence_that_is_not_a_list_or_a_citation_key_naming_no_kept_item_drops_its_area(
        tmp_path, key, value, owner_says):
    run = _run(tmp_path)
    payload = accounting()
    payload["areas"]["estimates_and_reserves"][key] = value
    raw, gated, out = _both(run, payload, mechanical.check_cited_items_exist)
    assert raw.failures == [f"analysis_accounting.json:areas.estimates_and_reserves.{key}: "
                            f"{owner_says}"]
    assert "dropped" in out["areas"]["estimates_and_reserves"]
    assert gated.status == PASS


# --- cited_numbers_exist ----------------------------------------------------------------

def test_a_placeholder_under_a_key_that_is_not_prose_is_resolved(tmp_path):
    run = _run(tmp_path)
    payload = accounting()
    payload["anomalies"][0]["detail"] = "rose to {ratios.liquidity.no_such_ratio}"
    payload["anomalies"][0]["basis"] = {"note": "see {nothing.here}"}
    raw, gated, out = _both(run, payload, mechanical.check_cited_numbers_exist)
    assert raw.failures == [
        "analysis_accounting.json:anomalies[0].detail:ratios.liquidity.no_such_ratio",
        "analysis_accounting.json:anomalies[0].basis.note:nothing.here"]
    assert out["anomalies"] == [] and gated.status == PASS


# --- forbidden_words and no_combined_score ------------------------------------------------

def test_the_gate_holds_the_owner_s_patterns():
    assert analysis_check.ACCUSATION.pattern == coverage.ACCUSATION.pattern
    assert analysis_check.ACCUSATION.flags == coverage.ACCUSATION.flags
    assert analysis_check.RECOMMENDATION.pattern == coverage.RECOMMENDATION.pattern
    assert analysis_check.RECOMMENDATION.flags == coverage.RECOMMENDATION.flags
    assert analysis_check.SCORE_KEY.pattern == coverage.SCORE_KEY.pattern
    assert analysis_check.CITATION_KEY.pattern == mechanical.CITATION_KEY.pattern
    assert analysis_check.LABEL_KEYS == mechanical.LABEL_KEYS
    assert run_analysis.ISO_DATE.pattern == mechanical.ISO_DATE.pattern
    assert agent_inputs.MARKET_FIGURE.pattern == mechanical.MARKET_FIGURE.pattern
    assert agent_inputs.MARKET_FIGURE.flags == mechanical.MARKET_FIGURE.flags
    assert extraction_checks.STAMP.pattern == mechanical.STAMP.pattern
    assert extraction_checks.ACCESSION.pattern == mechanical.ACCESSION.pattern
    assert extraction_checks.ROW_DATE_KEYS == mechanical.ROW_DATE_KEYS
    assert extraction_checks.ANY_DATE.pattern == mechanical.ANY_DATE.pattern
    assert extraction_checks.ACCESSION_ANYWHERE.pattern == mechanical.ACCESSION_ANYWHERE.pattern
    # the one reading of an [id] line the trim, the boundary check and the quote
    # gate share, and the owner's
    assert agent_inputs.ID_LINE.pattern == mechanical.ID_LINE.pattern
    assert agent_inputs.ID_LINE.flags == mechanical.ID_LINE.flags


@pytest.mark.parametrize("words", ["The antifraud program is described unchanged.",
                                   "Management called the claims nonfraudulent."])
def test_a_ruled_out_word_inside_another_word_is_dropped(tmp_path, words):
    run = _run(tmp_path)
    payload = accounting()
    area = payload["areas"]["controls_audit_and_filing_signals"]
    area["finding"] += " " + words
    raw, gated, out = _both(run, payload, coverage.check_forbidden_words)
    assert raw.failures and raw.failures[0].startswith(
        "analysis_accounting.json:areas.controls_audit_and_filing_signals.finding: ")
    assert "dropped" in out["areas"]["controls_audit_and_filing_signals"]
    assert gated.status == PASS


def test_a_key_that_scores_or_ranks_is_removed(tmp_path):
    run = _run(tmp_path)
    payload = accounting()
    payload["overall_reading"] = "few anomalies"
    payload["areas"]["revenue_recognition"]["risk_score"] = "elevated"
    payload["summary_ko"]["overall"] = "종합하면 특이점이 적다."
    raw, gated, out = _both(run, payload, coverage.check_no_combined_score)
    assert sorted(raw.failures) == sorted([
        "analysis_accounting.json.overall_reading",
        "analysis_accounting.json.areas.revenue_recognition.risk_score",
        "analysis_accounting.json.summary_ko.overall"])
    assert "overall_reading" not in out and "overall" not in out["summary_ko"]
    assert "dropped" in out["areas"]["revenue_recognition"]
    assert gated.status == PASS


# --- the memo ---------------------------------------------------------------------------

def test_what_the_memo_prints_is_held_to_the_recommendation_words(tmp_path):
    """The memo prints each summary sentence, each anomaly's Korean or English
    name and each adjustment's name, and the owner reads every memo line for buy,
    sell and their Korean phrases, whatever analysis it came from."""
    run = _run(tmp_path)
    payload = accounting()
    payload["summary_ko"]["earnings_versus_cash"] = "회사는 매수 권리를 부여했다"
    payload["anomalies"][0]["name_ko"] = "임원의 주식 매수 권리 행사 증가"
    second = dict(payload["anomalies"][0], id=ANOMALY_ID + "_again", name="Share buy back")
    del second["name_ko"]
    payload["anomalies"].append(second)

    def memo_of(analysis) -> str:
        return memo.memo(ticker="ESE", form="10-Q", period_end="2026-06-30",
                         cutoff="2026-08-10", fields=FIELDS, filings_only=FIELDS,
                         accounting=analysis, financial=None, valuation=None,
                         baselines=None, missing={})

    (run / "memo_ko.md").write_text(memo_of(payload), encoding="utf-8")
    raw = coverage.check_forbidden_words(run)
    assert sorted(hit.split(": ", 1)[1] for hit in raw.failures) == ["buy", "매수 권", "매수 권"]
    with pytest.raises(analysis_check.AnalysisInputError, match="ruled-out word"):
        run_analysis.memo_words_hold(run / "memo_ko.md")
    out = _gate(run, payload)
    assert out["anomalies"] == [] and out["summary_ko"]["earnings_versus_cash"] is None
    (run / "memo_ko.md").write_text(memo_of(out), encoding="utf-8")
    _publish(run, "analysis_accounting.json", out)
    assert coverage.check_forbidden_words(run).status == PASS
    run_analysis.memo_words_hold(run / "memo_ko.md")


# --- the reading: an entry with no finding or reading answers nothing ----------------------

def test_an_area_with_no_finding_is_dropped_and_accounted_for(tmp_path):
    run = _run(tmp_path)
    payload = accounting()
    payload["areas"]["earnings_versus_cash"] = {"verdict": "clean", "evidence": []}
    payload["areas"]["revenue_recognition"] = {"finding": "", "verdict": "clean",
                                               "evidence": []}
    raw, gated, out = _both(run, payload, coverage.check_accounting_areas)
    assert raw.failures == ["earnings_versus_cash", "revenue_recognition"]
    assert gated.status == PASS
    for name in ("earnings_versus_cash", "revenue_recognition"):
        assert coverage.answered(out["areas"][name]) == "dropped"


def test_every_section_dupont_and_the_value_range_is_answered_or_dropped():
    financial = {"sections": {name: {"verdict": "fine", "evidence": [], "fields": []}
                              for name in analysis_check.FINANCIAL_SECTIONS},
                 "dupont": {"verdict": "x"}, "path_to_distress": {"reading": "none"},
                 "anomalies": [], "summary_ko": {}, "limits": ""}
    out = analysis_check.check("financial", financial, fields=FIELDS, sources={})
    for name in coverage.FINANCIAL_SECTIONS:
        assert coverage.answered(out["sections"][name]) != "absent", name
    assert coverage.answered(out["dupont"]) != "absent"
    valuation = {"value_range": {"verdict": "x"}, "price_position": {"reading": "r"},
                 "market_implied_growth": {"reading": "r"},
                 "accounting_adjustments": {"reading": "r"}, "most_sensitive": [],
                 "summary_ko": {}, "limits": ""}
    out = analysis_check.check("valuation", valuation, fields=FIELDS, sources={})
    assert coverage.answered(out["value_range"]) == "dropped"


def test_a_block_that_is_not_there_is_dropped_whole_and_accounted_for():
    """What the owner reads as absent when a block is missing or is not an
    object -- every area or section of it -- is answered with the gate's note."""
    dropped: list = []
    financial = {"sections": "liquid", "anomalies": []}
    analysis_check.unanswered(financial, "financial", dropped)
    for name in coverage.FINANCIAL_SECTIONS:
        assert coverage.answered(financial["sections"][name]) == "dropped", name
    assert coverage.answered(financial["dupont"]) == "dropped"
    accounting_only = {}
    analysis_check.unanswered(accounting_only, "accounting", dropped)
    assert all(coverage.answered(accounting_only["areas"][name]) == "dropped"
               for name in coverage.ACCOUNTING_AREAS)
    assert {row["reason"] for row in dropped} == {"nothing stood for it"}


# --- what an agent left in its directory --------------------------------------------------

def test_a_stray_file_in_an_agent_s_directory_stops_the_run(tmp_path):
    run = _run(tmp_path)
    _write(run / "agents" / "financial-analyst" / "draft.json", '{"items": []}')
    layers = mechanical.check_layers_hold(run)
    assert "agents/financial-analyst/draft.json: not a file the financial-analyst layer sees" \
        in layers.failures
    with pytest.raises(agent_inputs.AgentInputError, match="draft.json"):
        run_analysis.boundary_holds(run, "in the test")


def test_the_router_hands_each_layer_what_the_owner_s_table_names(tmp_path):
    """The owner's layer table, written out in the grader, against the router's:
    every file a live agent is handed, and every file the control is handed, is
    one the owner's table names for it, and the other way round. The three files
    no builder writes yet are withheld until the owner's table names them."""
    for name, spec in agent_inputs.AGENTS.items():
        routed = set(spec.sees) - set(agent_inputs.NOT_BUILT_YET)
        assert routed == mechanical.LAYER_SEES[name], name
    run = tmp_path / "run"
    run.mkdir()
    for name in agent_inputs.BUNDLE_CATALOGUE:
        (run / name).write_text("x\n", encoding="utf-8")
    assert set(run_analysis.control_sees(run)) == mechanical.LAYER_SEES[mechanical.CONTROL_DIR]


def test_a_file_no_builder_writes_yet_is_not_routed_and_named_if_placed(tmp_path):
    run = _run(tmp_path)
    for name in agent_inputs.AGENTS["notes-text-reader"].sees:
        if not (run / name).exists():
            (run / name).write_text(f"this is {name}\n", encoding="utf-8")
    built = agent_inputs.build(run, "notes-text-reader")
    assert sorted(built["withheld"]) == ["input_exhibits.md", "input_risk_factors.md"]
    assert agent_inputs.isolation_violations(run) == []
    (run / "agents" / "notes-text-reader" / "input_risk_factors.md").write_text(
        "this is input_risk_factors.md\n", encoding="utf-8")
    assert "agents/notes-text-reader/input_risk_factors.md: not a file the notes-text-reader " \
           "layer sees" in mechanical.check_layers_hold(run).failures
    assert any("input_risk_factors.md" in line for line in agent_inputs.isolation_violations(run))


# --- the cutoff day ------------------------------------------------------------------------

def _manifest(eight_k: dict) -> dict:
    """CIEN's 10-Q 0001628280-26-040767 and its earnings 8-K, both filed on the
    cutoff day 2026-06-04, as the bundle manifest records them."""
    return {"cutoff": "2026-06-04", "filing_date": "2026-06-04", "form": "10-Q",
            "accession": "0001628280-26-040767", "accepted": "2026-06-04T16:05:00-04:00",
            "documents": [
                {"form": "10-Q", "role": "primary_html", "accession": "0001628280-26-040767",
                 "filing_date": "2026-06-04", "accepted": "2026-06-04T16:05:00-04:00"},
                dict({"form": "8-K", "role": "exhibit_99_1", "filing_date": "2026-06-04"},
                     **eight_k)]}


@pytest.mark.parametrize("eight_k, stands", [
    ({"accession": "0001628280-26-040614", "accepted": "2026-06-04T16:10:00-04:00"}, False),
    ({"accession": "0001193125-26-040614"}, False),
    ({"accession": "0001628280-26-040614", "accepted": "2026-06-04T16:00:00-04:00"}, True),
    ({"accession": "0001628280-26-040614"}, True)])
def test_a_same_day_filing_is_held_to_the_owner_s_order(tmp_path, eight_k, stands):
    """Stamped after the 10-Q, or under another filer agent's prefix with no
    stamp: the owner's nothing_after_cutoff fails it, and so does the bundle's
    cutoff check now. Stamped before, or lower in the same agent's sequence:
    both pass."""
    manifest = _manifest(eight_k)
    run = tmp_path / "run"
    _write(run / "input_manifest.json", json.dumps(manifest))
    owner = mechanical.check_nothing_after_cutoff(run)
    assert (owner.status == PASS) is stands, owner.failures
    assert extraction_checks.check_cutoff(manifest).passed is stands


FOREIGN = "0001193125-26-040699"      # another filer agent's prefix, no stamp


@pytest.mark.parametrize("name, text, stands", [
    ("input_numbers.json", {"facts": [{"source_accession": FOREIGN, "filing_date": "2026-06-04",
                                       "value": "1"}]}, False),
    ("input_numbers.json", {"facts": [{"source_accession": "0001628280-26-040500",
                                       "filing_date": "2026-06-04", "value": "1"}]}, True),
    ("input_trends.json", {"years": [{"filed": "2026-06-05", "value": 1}]}, False),
    ("input_trends.json", {"years": [{"filed": "2026-06-03", "value": 1}]}, True),
    ("input_8k.md", f"# CIEN 8-K\n\n- 2026-06-04 {FOREIGN} — 2.02, 9.01\n", False),
    ("input_8k.md", "# CIEN 8-K\n\n- 2026-06-05 0001628280-26-040900 — 8.01\n", False),
    ("input_8k.md", f"# CIEN 8-K\n\nsee {FOREIGN}\n", False),
    ("input_8k.md", "# CIEN 8-K\n\n- 2026-06-03 0001628280-26-040500 — 8.01\n", True),
    ("input_prior_predictions.md", "# prior predictions\n\n- the shares fell 5% after\n", False),
    ("input_prior_predictions.md", "# prior predictions\n\nNone on record.\n", True)])
def test_the_inputs_rows_and_id_less_lines_are_held_at_the_bundle(tmp_path, name, text, stands):
    """The owner's nothing_after_cutoff reads the inputs as well as the documents:
    a JSON row dated after the cutoff, or the cutoff day from a filing not shown
    accepted first; an id-less prose line (the 8-K index when the release has no
    paragraph) naming such a filing, a later date, or an accession no document
    carries; a price or return in the prior predictions. The bundle's cutoff
    gate held the documents alone; it now holds these too, the same way."""
    manifest = _manifest({"accession": "0001628280-26-040614"})
    run = tmp_path / "run"
    _write(run / "input_manifest.json", json.dumps(manifest))
    _write(run / name, text if isinstance(text, str) else json.dumps(text))
    owner = mechanical.check_nothing_after_cutoff(run)
    assert (owner.status == PASS) is stands, owner.failures
    texts = {name: (run / name).read_text(encoding="utf-8")}
    assert extraction_checks.check_cutoff(manifest, texts).passed is stands


# --- the calculator ---------------------------------------------------------------------------

def test_a_date_after_the_cutoff_in_a_calculator_stage_stops_the_run():
    """AAPL's accounting analyst could name an adjustment '2027-06-30': the
    calculator copies the name into the quality-adjusted free cash flow, and the
    owner's nothing_after_cutoff reads every string of every calculator file."""
    payload = {"free_cash_flow": {"free_cash_flow_quality_adjusted": {
        "adjustments_applied": [{"name": "2027-06-30", "amount": 1.0}]}},
        "period": "2026-04-01..2026-06-27"}
    assert run_analysis.calculator_problems(payload, "2026-07-31") == [
        "free_cash_flow.free_cash_flow_quality_adjusted.adjustments_applied[0].name = "
        "2027-06-30 is after the cutoff 2026-07-31"]
    assert run_analysis.calculator_problems({"period": "2026-04-01..2026-06-27"},
                                            "2026-07-31") == []


def test_a_number_that_is_not_finite_stops_the_run(tmp_path):
    payload = {"valuation": {"scenarios": {"bull": {"value_per_share": math.nan,
                                                    "enterprise_value": {"value": math.inf}}}},
               "flag": {"value": True}}
    problems = run_analysis.calculator_problems(payload, "2026-07-31")
    assert len(problems) == 3
    run = tmp_path / "run"
    _write(run / "calculator.json", json.dumps(payload))
    # the owner names a `value` that is a float twice, once per rule
    assert set(mechanical.check_calculator_finite(run).failures) == {
        "valuation.scenarios.bull.value_per_share",
        "valuation.scenarios.bull.enterprise_value.value", "flag.value"}


def test_a_driver_or_override_that_is_not_finite_drops_its_scenario():
    reason = {"reason": "r", "fields": ["ratios.liquidity.current_ratio"]}
    written = _scenarios(reason)
    written["scenarios"]["bull"]["revenue_growth_year_one"] = math.inf
    written["wacc_overrides"] = {"pre_tax_cost_of_debt": {"value": math.nan, "quote": "q",
                                                          "quote_from": "input_8k.md"}}
    out = analysis_check.check_assumptions(written, fields=FIELDS,
                                           sources={"input_8k.md": EIGHT_K})
    assert set(out["scenarios"]) == {"bear", "base"}
    assert out["wacc_overrides"] == {}
    assert calculator.SCENARIOS == ("bear", "base", "bull")


def test_a_price_figure_in_the_prior_predictions_file_is_refused(tmp_path):
    run = _run(tmp_path)
    (run / "input_prior_predictions.md").write_text(
        "# prior predictions\n\n- the stock fell $5 after the release\n", encoding="utf-8")
    assert mechanical.prior_predictions_problems(
        (run / "input_prior_predictions.md").read_text(encoding="utf-8"))
    for name in agent_inputs.AGENTS["numbers-reader"].sees:
        if not (run / name).exists():
            (run / name).write_text("x\n", encoding="utf-8")
    with pytest.raises(agent_inputs.AgentInputError, match="price or return figure"):
        agent_inputs.build(run, "numbers-reader")
