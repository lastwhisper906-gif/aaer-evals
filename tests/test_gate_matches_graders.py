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
    """Only the top-level `dropped_items` is the gate's own record. The owner's
    forbidden_words and cited_numbers_exist leave only that one out, and
    no_combined_score leaves out none, the top one included, which the gate
    writes over with its own rows: one an analyst writes inside an item is read
    like any other key. The gate used to pass over it at every depth."""
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


@pytest.mark.parametrize("key, value", [
    ("dropped", "the antifraud review was skipped"),
    # a key named "" puts a nested `dropped` at the place string "dropped" too
    ("", {"dropped": "the antifraud review was skipped"})])
def test_a_dropped_key_at_the_top_is_the_analyst_s_words(tmp_path, key, value):
    """The gate writes its note on what it dropped inside an entry, never at the
    top, and the owner's forbidden_words leaves out only a `.dropped` below the
    top (and a quote): a `dropped` an analyst writes at the top is read for
    ruled-out words like any other key. The gate left out every string whose
    last key was `dropped`, and kept it (the critic's probe, 2026-10-08)."""
    run = _run(tmp_path)
    payload = accounting()
    payload[key] = value
    raw, gated, out = _both(run, payload, coverage.check_forbidden_words)
    assert raw.failures == ["analysis_accounting.json:dropped: fraud"]
    assert key not in out and gated.status == PASS


@pytest.mark.parametrize("place, value, grader", [
    ("top", "see {nothing.here}", mechanical.check_cited_numbers_exist),
    ("area", "the antifraud review was not read", coverage.check_forbidden_words)])
def test_a_dropped_key_the_owner_leaves_out_is_kept(tmp_path, place, value, grader):
    """The other side, standing before and after: cited_numbers_exist leaves out
    a `dropped` at the top as well as below it, and forbidden_words one below
    the top, so the gate holds neither there and keeps what carries it."""
    run = _run(tmp_path)
    payload = accounting()
    if place == "top":
        payload["dropped"] = value
    else:
        payload["areas"]["revenue_recognition"] = {"dropped": value}
    _publish(run, "analysis_accounting.json", payload)
    assert grader(run).status == PASS
    out = _gate(run, payload)
    if place == "top":
        assert out["dropped"] == value
    else:
        assert out["areas"]["revenue_recognition"] == {"dropped": value}
    _publish(run, "analysis_accounting.json", out)
    assert grader(run).status == PASS


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


def _null_under(payload: dict, place: str, value) -> None:
    """`value` written where an analyst could write it below the schema's items:
    under a point of an area, at the top of the analysis, under an anomaly's
    support -- the three places the critic's probe of 2026-10-08 put a null."""
    if place == "point":
        payload["areas"]["revenue_recognition"]["points"] = [value]
    elif place == "top":
        payload.update(value)
    else:
        payload["anomalies"][0]["support"] = value


@pytest.mark.parametrize("place, value, owner_says", [
    ("point", {"evidence": [None]}, "areas.revenue_recognition.points[0].evidence: None"),
    ("top", {"evidence": [None]}, "evidence: None"),
    ("support", {"evidence": [EPS_ITEM, None]}, "anomalies[0].support.evidence: None")])
def test_a_null_in_an_evidence_list_below_the_schema_s_items_is_dropped(tmp_path, place, value,
                                                                       owner_says):
    """The owner's cited_items_exist passes a null under every citation key but
    `evidence`, whose every entry it holds to the kept items. The gate passed a
    null under each, so one in an `evidence` list the schema's own checks do not
    reach was published and failed (the critic's probe of 2026-10-08)."""
    run = _run(tmp_path)
    payload = accounting()
    _null_under(payload, place, value)
    raw, gated, out = _both(run, payload, mechanical.check_cited_items_exist)
    assert raw.failures == [f"analysis_accounting.json:{owner_says}"]
    assert gated.status == PASS, gated.failures
    assert out["dropped_count"] == 1


@pytest.mark.parametrize("place, value", [
    ("point", {"numbers_items": [None], "notes_item": None}),
    ("top", {"line_items": [None]}),
    ("support", {"evidence": [EPS_ITEM], "notes_item": None})])
def test_a_null_under_any_other_citation_key_is_passed_by_both(tmp_path, place, value):
    """The other side, standing before the fix and after it."""
    run = _run(tmp_path)
    payload = accounting()
    _null_under(payload, place, value)
    raw, gated, out = _both(run, payload, mechanical.check_cited_items_exist)
    assert raw.status == PASS and gated.status == PASS
    assert out["dropped_items"] == []


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


# The four cells QCOM's second pass cited for the reason each states, as the
# calculator.json of its run 0000804328-26-000086 (2026-10-07) printed them, and
# one cell with a number, written here.
NO_PRICE = ("no price series was given: the forward track's price source is Tiingo, and "
            "without its token no series is fetched")
NO_WACC = f"the cost of equity needs a beta and a price: {NO_PRICE}"
PRICELESS = {
    "valuation": {"missing": f"WACC is not computed: {NO_WACC}"},
    "market": {"missing": NO_PRICE},
    "cost_of_capital": {"value": None, "missing": NO_WACC},
    "implied_growth_beside_history": {"implied_ten_year_revenue_growth": {
        "missing": f"no reverse DCF: WACC is not computed: {NO_WACC}"}},
    "ratios": {"liquidity": {"current_ratio": {"value": 2.5, "unit": "ratio"}}},
}


@pytest.mark.parametrize("value_range, price_position, growth, stands", [
    (["valuation.missing", "cost_of_capital.missing"], ["market.missing"],
     ["implied_growth_beside_history.implied_ten_year_revenue_growth.missing"], True),
    (["valuation.reason"], ["ratios.liquidity.current_ratio.missing"],
     ["implied_growth_beside_history.implied_ten_year_revenue_growth.missing.text"], False)])
def test_the_reason_a_cell_states_for_having_no_value_is_a_field_an_analyst_cites(
        tmp_path, value_range, price_position, growth, stands):
    """QCOM's and NVDA's second passes, with no price on record, cited the reason
    calculator.json prints under `valuation.missing`, as the valuation analyst's
    prompt has them quote it. The owner's cited_numbers_exist resolves each path
    and passed both analyses as written; the gate took a cited field to be a
    number or a cell, and published value_range, price_position,
    market_implied_growth and (QCOM's) most_sensitive[1] as drop notes. The
    other side: a reason key the cell does not carry, or a path into the
    reason's words, names nothing in the calculator, and both refuse it."""
    run = tmp_path / "run"
    _write(run / "calculator.json", json.dumps(PRICELESS))
    payload = {"value_range": {"reading": "Not computed: there is no price.",
                               "fields": value_range},
               "price_position": {"reading": "Not computed.", "fields": price_position},
               "market_implied_growth": {"reading": "Not computed.", "fields": growth},
               "most_sensitive": [{"assumption": "the cost of capital",
                                   "reading": "Not measured.", "fields": value_range[-1:]}],
               "accounting_adjustments": {"reading": "None were applied.", "fields": []},
               "summary_ko": {}, "limits": analysis_check.LIMITS["valuation"]}
    _publish(run, "analysis_valuation.json", payload)
    raw = mechanical.check_cited_numbers_exist(run)
    out = analysis_check.check("valuation", copy.deepcopy(payload), fields=PRICELESS,
                               sources={})
    _publish(run, "analysis_valuation.json", out)
    assert mechanical.check_cited_numbers_exist(run).status == PASS
    read = ("value_range", "price_position", "market_implied_growth", "most_sensitive")
    if stands:
        assert raw.status == PASS, raw.failures
        assert out["dropped_items"] == [], out["dropped_items"]
        assert {key: out[key] for key in read} == {key: payload[key] for key in read}
    else:
        assert raw.failures == [
            f"analysis_valuation.json:{key}.fields[0]:{path}" for key, path in (
                ("value_range", value_range[0]), ("price_position", price_position[0]),
                ("market_implied_growth", growth[0]))]
        assert [row["where"] for row in out["dropped_items"]] == list(read[:3]) + [
            "most_sensitive[0]"]
        assert out["value_range"] == {
            "dropped": f"fields: {value_range[0]!r} is not a field of calculator.json"}
        assert out["most_sensitive"] == []


# The words calculator.json prints where the second passes on record cited them, as
# each run printed them: CSCO's run 0000858877-26-000078 (the price's position, the
# price and what the reverse DCF holds) and CIEN's run 0001628280-26-040767 (the
# beta's window, and its one accounting adjustment's name and mechanism).
HELD = "base margins, base reinvestment, base terminal growth"
PRICED = {
    "valuation": {
        "price_at_cutoff": 115.38, "price_position": "above the range",
        "reverse_dcf": {"value": 0.14635827622259967, "held": HELD},
        "accounting_adjustments": {"each": [{
            "name": "accounts payable build from supplier payment timing",
            "mechanism": "one-time: value lowered by the amount over diluted shares",
            "moved_per_share": -1.28164085460038}]}},
    "cost_of_capital": {"value": 0.15472925611257576,
                        "beta": {"value": 2.6820943351306967, "window_first": "2025-06-05",
                                 "window_last": "2026-06-03"}},
}
# What each unit cited, in the analysts' own sentences, trimmed: CSCO's
# price_position, market_implied_growth and summary_ko.price_position; CIEN's
# most_sensitive[1] and accounting_adjustments.
WORDS_CITED = {"price_position": "valuation.price_position",
               "market_implied_growth": "valuation.reverse_dcf.held",
               "most_sensitive": "cost_of_capital.beta.window_first",
               "accounting_adjustments": "valuation.accounting_adjustments.each.0.name"}
# The same cells, at a key they do not carry or into the words they print.
NOTHING_CITED = {"price_position": "valuation.price_position.0",
                 "market_implied_growth": "valuation.reverse_dcf.holds",
                 "most_sensitive": "cost_of_capital.beta.window_middle",
                 "accounting_adjustments": "valuation.accounting_adjustments.each.1.name"}


def _cites(cited: dict) -> dict:
    return {
        "value_range": {"reading": "Python ran three scenarios.", "fields": []},
        "price_position": {
            "reading": "The price at the cutoff, {valuation.price_at_cutoff}, is "
                       f"{{{cited['price_position']}}}.",
            "fields": ["valuation.price_at_cutoff", cited["price_position"]]},
        "market_implied_growth": {
            "reading": f"Holding {{{cited['market_implied_growth']}}}, Python finds by "
                       "bisection that the base case is worth the price only if revenue "
                       "grows at a constant {valuation.reverse_dcf.value|pct} a year.",
            "fields": [cited["market_implied_growth"], "valuation.reverse_dcf.value"]},
        "most_sensitive": [{
            "assumption": "the discount rate (WACC), which is beta-driven",
            "reading": f"The beta is measured over the window {{{cited['most_sensitive']}}} "
                       "to {cost_of_capital.beta.window_last}.",
            "fields": [cited["most_sensitive"], "cost_of_capital.beta.window_last"]}],
        "accounting_adjustments": {
            "reading": f"One adjustment was applied: '{{{cited['accounting_adjustments']}}}', "
                       "carried from the accounting analysis as a one-time reduction to cash "
                       "flow ({valuation.accounting_adjustments.each.0.mechanism}).",
            "fields": [cited["accounting_adjustments"]]},
        "summary_ko": {"price_position": "기준일 주가 {valuation.price_at_cutoff}는 파이썬이 "
                                         f"'{{{cited['price_position']}}}'로 판정한 대로 산출 "
                                         "범위 위에 있습니다."},
        "limits": analysis_check.LIMITS["valuation"]}


@pytest.mark.parametrize("cited, stands", [(WORDS_CITED, True), (NOTHING_CITED, False)])
def test_words_the_calculator_prints_are_a_field_and_a_placeholder_an_analyst_cites(
        tmp_path, cited, stands):
    """Every priced second pass on record cited words calculator.json prints --
    the price's position ("above the range"), what the reverse DCF holds, the
    beta's window, the accounting adjustment's name -- in `fields` and as
    `{path}`. The owner's cited_numbers_exist resolves each path and passes them
    as written; the gate took a field to be a number or a reason and a
    placeholder to be a number, and CARR, CIEN, CSCO, PANW and STX published
    thirteen units as drop notes, the memo printing its dropped sentence in
    their place. Now each stands, and the memo prints the words verbatim, the
    analyst's own words after them as written. The other side, before and
    after: a key the cell does not carry, an index past the list, or a path
    into the words names nothing, and both refuse it."""
    run = tmp_path / "run"
    _write(run / "calculator.json", json.dumps(PRICED))
    payload = _cites(cited)
    _publish(run, "analysis_valuation.json", payload)
    raw = mechanical.check_cited_numbers_exist(run)
    out = analysis_check.check("valuation", copy.deepcopy(payload), fields=PRICED, sources={})
    _publish(run, "analysis_valuation.json", out)
    assert mechanical.check_cited_numbers_exist(run).status == PASS
    units = ("price_position", "market_implied_growth", "most_sensitive",
             "accounting_adjustments", "summary_ko")
    if stands:
        assert raw.status == PASS, raw.failures
        assert out["dropped_items"] == [], out["dropped_items"]
        assert {key: out[key] for key in units} == {key: payload[key] for key in units}
        assert memo.fill(out["summary_ko"]["price_position"], PRICED) == (
            "기준일 주가 주당 115.38달러는 파이썬이 'above the range'로 판정한 대로 산출 범위 "
            "위에 있습니다.")
        assert memo.fill("{valuation.accounting_adjustments.each.0.mechanism}, over "
                         "{cost_of_capital.beta.window_first}..{cost_of_capital.beta.window_last}",
                         PRICED) == ("one-time: value lowered by the amount over diluted shares, "
                                     "over 2025-06-05..2026-06-03")
    else:
        # the owner holds a `fields` entry under a list item as no path (its
        # FOLLOWS_PATHS reads the place before the first index), and every
        # `{path}` wherever it sits
        place = "analysis_valuation.json"
        assert raw.failures == [
            f"{place}:price_position.reading:{cited['price_position']}",
            f"{place}:price_position.fields[1]:{cited['price_position']}",
            f"{place}:market_implied_growth.reading:{cited['market_implied_growth']}",
            f"{place}:market_implied_growth.fields[0]:{cited['market_implied_growth']}",
            f"{place}:most_sensitive[0].reading:{cited['most_sensitive']}",
            f"{place}:accounting_adjustments.reading:{cited['accounting_adjustments']}",
            f"{place}:accounting_adjustments.fields[0]:{cited['accounting_adjustments']}",
            f"{place}:summary_ko.price_position:{cited['price_position']}"]
        assert sorted(row["where"] for row in out["dropped_items"]) == [
            "accounting_adjustments", "market_implied_growth", "most_sensitive[0]",
            "price_position", "summary_ko.price_position"]
        assert out["most_sensitive"] == [] and out["summary_ko"]["price_position"] is None
        for key in ("price_position", "market_implied_growth", "accounting_adjustments"):
            assert cited[key] in out[key]["dropped"]


@pytest.mark.parametrize("path, value", [
    # QCOM's cost_of_capital, as its run 0000804328-26-000086 printed it: a cell whose
    # value is null; and the cell itself
    ("cost_of_capital.value", None), ("cost_of_capital", {"value": None, "missing": NO_WACC}),
    # words carrying a ruled-out word: none of the calculator files on record holds one
    ("valuation.price_position", "buy below the range")])
def test_a_placeholder_the_memo_cannot_print_is_the_gate_s_own_refusal(tmp_path, path, value):
    """The pipeline's own rule, standing before and after: a `{path}` stands only
    for a number or for words the memo can print. A null, or a cell with no
    number, the owner's cited_numbers_exist resolves and passes, and the memo has
    nothing to print for it. Words carrying a ruled-out word the owner passes
    there too, and its forbidden_words passes the analysis, where the word is
    not; the memo would print them verbatim, on a line forbidden_words reads.
    The gate drops the sentence; the owner passes what it publishes."""
    fields = copy.deepcopy(PRICELESS)
    *heads, last = path.split(".")
    node = fields
    for part in heads:
        node = node.setdefault(part, {})
    node[last] = value
    run = tmp_path / "run"
    _write(run / "calculator.json", json.dumps(fields))
    payload = {key: {"reading": "Not computed.", "fields": ["valuation.missing"]}
               for key in analysis_check.VALUATION_KEYS}
    payload.update(most_sensitive=[], limits=analysis_check.LIMITS["valuation"],
                   summary_ko={"price_position": f"주가의 위치는 {{{path}}}입니다."})
    _publish(run, "analysis_valuation.json", payload)
    assert mechanical.check_cited_numbers_exist(run).status == PASS
    assert coverage.check_forbidden_words(run).status == PASS
    out = analysis_check.check("valuation", copy.deepcopy(payload), fields=fields, sources={})
    assert [row["where"] for row in out["dropped_items"]] == ["summary_ko.price_position"]
    assert out["summary_ko"]["price_position"] is None
    _publish(run, "analysis_valuation.json", out)
    assert mechanical.check_cited_numbers_exist(run).status == PASS


# CARR's pre-tax cost of debt as the calculator.json of its run 0001783180-26-000032
# printed it: the first-pass valuation analyst chose the notes' rate, and Python
# copied the analyst's reason into the cell, two `{path}`s of the analyst's own in it.
CARR_RUN = Path(__file__).resolve().parents[1] / "runs" / "CARR" / "0001783180-26-000032"
CARR_REASON = (
    "The calculator prints pre_tax_cost_of_debt as missing because interest expense is not "
    "tagged for the year-to-date period. The MD&A states the weighted-average interest rate "
    "on the long-term notes, which make up most of total debt of {terms.debt_now.value}; "
    "commercial paper within current debt of {terms.debt_now.parts.debt_current.value} "
    "carries a rate not stated in these inputs, and the quarter's interest expense rose "
    "because of it, so the true blended rate may sit a little above the notes' rate. The "
    "notes' stated rate is the only figure in the inputs and is used as the pre-tax cost of "
    "debt.")


@pytest.mark.parametrize("sentence, printed", [
    ("세전 타인자본비용은 장기 사채의 이자율이며, 그 근거는 "
     "{cost_of_capital.pre_tax_cost_of_debt.reason}", None),
    # CARR's terms.debt_now.value, 11,952,000,000, in hundreds of millions to one
    # decimal, as the memo prints dollars: 119.5억 달러
    ("세전 타인자본비용은 총차입금 {terms.debt_now.value} 가운데 "
     "대부분을 차지하는 장기 사채의 이자율입니다.",
     "세전 타인자본비용은 총차입금 119.5억 달러 가운데 "
     "대부분을 차지하는 장기 사채의 이자율입니다.")], ids=["the_reason", "the_debt"])
def test_words_holding_a_placeholder_of_their_own_are_the_gate_s_own_refusal(
        tmp_path, sentence, printed):
    """The memo prints the words a `{path}` names as written, so a sentence citing
    CARR's reason would print `{terms.debt_now.value}` and
    `{terms.debt_now.parts.debt_current.value}` in the memo, unexpanded: the
    owner's cited_numbers_exist resolves the path and passes it, and so did the
    gate. The gate drops the sentence, and the memo says it was dropped. The
    other side, before and after: the reason cited in `fields` stands in every
    unit, and a sentence citing the analyst's own path is printed with the
    number."""
    fields = json.loads((CARR_RUN / "calculator.json").read_text(encoding="utf-8"))
    assert fields["cost_of_capital"]["pre_tax_cost_of_debt"]["reason"] == CARR_REASON
    run = tmp_path / "run"
    _write(run / "calculator.json", json.dumps(fields))
    reason = ["cost_of_capital.pre_tax_cost_of_debt.reason"]
    payload = {key: {"reading": "Read.", "fields": reason}
               for key in analysis_check.VALUATION_KEYS}
    payload.update(most_sensitive=[], limits=analysis_check.LIMITS["valuation"],
                   summary_ko={"most_sensitive": sentence})
    _publish(run, "analysis_valuation.json", payload)
    assert mechanical.check_cited_numbers_exist(run).status == PASS
    out = analysis_check.check("valuation", copy.deepcopy(payload), fields=fields, sources={})
    _publish(run, "analysis_valuation.json", out)
    assert mechanical.check_cited_numbers_exist(run).status == PASS
    units = analysis_check.VALUATION_KEYS
    assert {key: out[key] for key in units} == {key: payload[key] for key in units}
    lines = memo.valuation_section(out, fields)
    assert not analysis_check.PLACEHOLDER.search("\n".join(lines))
    if printed:
        assert out["dropped_items"] == []
        assert f"- **가장 민감한 가정**: {printed}" in lines
    else:
        assert [row["where"] for row in out["dropped_items"]] == ["summary_ko.most_sensitive"]
        assert "'{terms.debt_now.value}'" in out["dropped_items"][0]["reason"]
        assert out["summary_ko"]["most_sensitive"] is None
        assert f"- **가장 민감한 가정**: {memo.DROPPED_KO}" in lines


@pytest.mark.parametrize("path", [
    "valuation.price_position", "valuation.reverse_dcf", "valuation.reverse_dcf.held",
    "cost_of_capital.value", "valuation.accounting_adjustments.each.0.name",
    "valuation.accounting_adjustments.each.-1.name", "valuation.accounting_adjustments.each.+0",
    "valuation.accounting_adjustments.each. 0", "valuation.accounting_adjustments.each.0_0",
    "valuation.accounting_adjustments.each.²", "valuation.accounting_adjustments.each.1",
    "valuation.price_position.0", "valuation.price_at_cutoff.value", "valuation..held", "",
    "valuation.reverse_dcf.value.real", "missing", "valuation.missing"])
def test_the_gate_reads_a_path_as_the_owner_s_grader_reads_it(path):
    """One reading of a calculator path, the owner's (`evals.common.resolve`),
    written out in the gate as the grader writes it: a `fields` entry stands
    exactly when the owner resolves it, and a `{path}` is refused whenever it
    names nothing to the owner -- in CSCO's and CIEN's priced cells and in
    QCOM's priceless ones, where `cost_of_capital.value` is a null and
    `valuation.missing` the reason."""
    from evals import common
    for tree in (PRICED, PRICELESS):
        try:
            owner = ("names", common.resolve(tree, path))
        except KeyError:
            owner = ("nothing", None)
        assert analysis_check.field_cited(tree, path) is (owner[0] == "names")
        try:
            gate = ("names", analysis_check.resolve(tree, path))
        except KeyError:
            gate = ("nothing", None)
        assert gate == owner
        if owner[0] == "nothing":
            assert analysis_check.placeholder_problem(tree, path) is not None


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

def test_a_stray_file_in_an_agent_s_directory_is_named_at_the_boundary(tmp_path):
    """The check the runner calls after each agent returns; the runner's own stop
    is held in tests/test_run_analysis.py, by running it."""
    run = _run(tmp_path)
    _write(run / "agents" / "financial-analyst" / "draft.json", '{"items": []}')
    layers = mechanical.check_layers_hold(run)
    assert "agents/financial-analyst/draft.json: not a file the financial-analyst layer sees" \
        in layers.failures
    with pytest.raises(agent_inputs.AgentInputError, match="draft.json"):
        run_analysis.boundary_holds(run, "in the test")


def test_a_routed_name_the_run_does_not_hold_is_named(tmp_path):
    """A file an agent writes under the name of one of its own inputs, which the
    run does not hold: the owner's layers_hold passes the name, and its
    inputs_on_record finds no such input on record. The boundary check held a
    routed name only to bytes the run has, and named nothing."""
    run = _run(tmp_path)
    _write(run / "agents" / "numbers-reader" / "input_numbers.json", '{"facts": []}\n')
    assert mechanical.check_layers_hold(run).status == PASS
    assert "agents/numbers-reader/input_numbers.json: no such input on record" \
        in mechanical.check_inputs_on_record(run).failures
    with pytest.raises(agent_inputs.AgentInputError,
                       match="input_numbers.json, which the run does not hold"):
        run_analysis.boundary_holds(run, "in the test")


def _control_run(tmp_path: Path) -> Path:
    """A run whose single-agent control was handed what `control_sees` routes and
    wrote its three files, as `run_control` builds the directory."""
    run = _run(tmp_path)
    _write(run / run_analysis.BEFORE_ANALYSTS, json.dumps(FIELDS))
    directory = run / run_analysis.CONTROL_DIRNAME
    for name in run_analysis.control_sees(run):
        _write(directory / name, (run / name).read_text(encoding="utf-8"))
    for name in run_analysis.CONTROL_WRITES:
        _write(directory / name, "{}")
    return run


@pytest.mark.parametrize("damage, owner_says", [
    (lambda directory: _write(directory / "draft.json", '{"items": []}'),
     "control-single-agent-analyses/draft.json: not a file the control-single-agent-analyses "
     "layer sees"),
    (lambda directory: _write(directory / run_analysis.BEFORE_ANALYSTS, json.dumps(
        dict(FIELDS, cutoff="2026-08-11"))),
     "control-single-agent-analyses/calculator_before_analysts.json: not the run's "
     "calculator_before_analysts.json")])
def test_the_control_s_directory_is_held_at_the_boundary(tmp_path, damage, owner_says):
    """The owner's layers_hold and inputs_on_record walk the control's directory
    beside the agents', and the router's boundary check does not: a stray file
    the control left, or a copy that is not the run's, stopped no run. The
    boundary the runner checks after the control returns now holds it (the
    runner's stop: tests/test_run_analysis.py, by running it)."""
    assert run_analysis.CONTROL_DIRNAME == mechanical.CONTROL_DIR
    run = _control_run(tmp_path)
    for grader in (mechanical.check_layers_hold, mechanical.check_inputs_on_record):
        assert not any(line.startswith(mechanical.CONTROL_DIR) for line in grader(run).failures)
    run_analysis.boundary_holds(run, "in the test")
    damage(run / run_analysis.CONTROL_DIRNAME)
    failures = (mechanical.check_layers_hold(run).failures
                + mechanical.check_inputs_on_record(run).failures)
    assert owner_says in failures
    with pytest.raises(agent_inputs.AgentInputError, match=owner_says.split(":")[0]):
        run_analysis.boundary_holds(run, "in the test")


# GNRC's notes reader left an eleven-byte "placeholder" beside its report
# (runs/GNRC/0001437749-26-025669/agents/notes-text-reader/scratch_check.txt). Each
# stray here is (name, bytes, the run's own file of that name or None), and whether
# the owner passes it: one word of letters, under a name no record carries, that no
# run file of the same name contradicts.
STRAYS = [
    ("scratch_check.txt", b"placeholder", None, True),
    ("note.txt", b"placeholder\n", None, True),
    ("memo_ko.md", b"placeholder", None, True),
    ("memo_ko.md", b"placeholder", b"placeholder", True),
    ("memo_ko.md", b"placeholder", "# ESE memo\n".encode(), False),
    ("draft.json", b'{"items": []}', None, False),
    ("note.txt", b"shares fell sharply after the report", None, False),
    ("note.txt", b"shares-fell-after-the-report", None, False),
    ("note.txt", b"x" * 65, None, False),
    ("note.txt", b"", None, False),
    ("note.txt", "naïve".encode(), None, False),
    ("report_draft.md", b"placeholder", None, False),
    ("calculator_notes.txt", b"placeholder", None, False),
]


@pytest.mark.parametrize("place", ["agents/notes-text-reader", run_analysis.CONTROL_DIRNAME])
@pytest.mark.parametrize("name, data, run_file, owner_passes", STRAYS)
def test_the_boundary_passes_a_stray_word_as_the_owner_does_and_nothing_else(
        tmp_path, place, name, data, run_file, owner_passes):
    """The runner's boundary check named every file nobody routed, so it stopped a
    run on GNRC's "placeholder", which the owner's layers_hold and
    inputs_on_record pass and note; and a run stopped there could not be resumed,
    because the router refused to rebuild the reader's directory over it. Both
    sides now read a stray file one way: what the owner refuses, the boundary
    names, and what the owner passes, it passes."""
    run = _control_run(tmp_path)
    if run_file is not None:
        (run / name).write_bytes(run_file)
    assert run_analysis.control_violations(run) == []
    assert agent_inputs.isolation_violations(run) == []
    (run / place / name).write_bytes(data)
    where = f"{place.split('/')[-1]}/{name}"
    owner = [line for line in mechanical.check_layers_hold(run).failures
             + mechanical.check_inputs_on_record(run).failures if where in line]
    boundary = [line for line in agent_inputs.isolation_violations(run)
                + run_analysis.control_violations(run) if name in line]
    assert (owner == []) is owner_passes, owner
    assert (boundary == []) is owner_passes, boundary


@pytest.mark.parametrize("place", ["agents/notes-text-reader", run_analysis.CONTROL_DIRNAME])
def test_a_directory_left_in_an_agent_s_directory_is_refused_by_both(tmp_path, place):
    run = _control_run(tmp_path)
    (run / place / "scratch").mkdir()
    assert any("scratch" in line for line in mechanical.check_layers_hold(run).failures)
    assert any("scratch" in line for line in agent_inputs.isolation_violations(run)
               + run_analysis.control_violations(run))


def test_the_boundary_reads_a_stray_word_with_the_owner_s_own_rule():
    assert agent_inputs.RECORD_NAMES == mechanical.RECORD_NAMES
    assert agent_inputs.ONE_WORD.pattern == mechanical.ONE_WORD.pattern
    assert agent_inputs.ONE_WORD.flags == mechanical.ONE_WORD.flags
    for _, data, _, _ in STRAYS:
        assert agent_inputs.is_placeholder(data) == mechanical.is_placeholder(data), data


@pytest.mark.parametrize("retired, holds", [
    ("numbers-vs-market", None),
    ("numbers-vs-market", "report_numbers.md"),
    ("supervisor-accounting", "report_notes_text.md")])
def test_a_retired_agent_s_directory_on_a_live_run_is_refused_by_both(tmp_path, retired, holds):
    """The boundary check judged a directory named for a retired agent by the
    layer the agent had on the pilot runs, and counted it among the agents'
    directories, so the boundary the runner checks passed one holding nothing or
    a copy of what the comparer or supervisor saw; the owner's layers_hold
    refuses any directory under `agents/` its table does not name. A run on
    record keeps the old reading (a pilot run's directory is the record of what
    the agent saw); a run the live pipeline is building does not."""
    run = _run(tmp_path)
    directory = run / "agents" / retired
    directory.mkdir()
    if holds:
        (directory / holds).write_bytes((run / holds).read_bytes())
    assert f"agents/{retired}: no layer the grader knows" \
        in mechanical.check_layers_hold(run).failures
    assert agent_inputs.isolation_violations(run) == []
    with pytest.raises(agent_inputs.AgentInputError, match=retired):
        run_analysis.boundary_holds(run, "in the test")
    assert any(line.startswith(f"{retired}: a retired agent's directory")
               for line in agent_inputs.isolation_violations(run, live_run=True))


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


@pytest.mark.parametrize("where, filed, stands", [
    ("row", "2026-06-03", False),
    ("row", "20260604", False),
    ("top", "20260604", False),
    ("row", "2026-06-04", True)])
def test_each_document_of_the_triggering_report_is_held_to_the_cutoff(tmp_path, where, filed,
                                                                      stands):
    """The owner's nothing_after_cutoff holds each document row of the triggering
    report, and the manifest's own filing date, to the cutoff as written. The
    bundle's cutoff gate held only the top-level date, and as a date, so CIEN's
    10-Q row dated 2026-06-03 under a cutoff of 2026-06-04 passed it (the
    critic's probe of 2026-10-08), and so did a date written 20260604, which
    Python reads as the same day and the owner, comparing text, does not."""
    manifest = _manifest({"accession": "0001628280-26-040614"})
    if where == "row":
        manifest["documents"][0]["filing_date"] = filed
    else:
        manifest["filing_date"] = filed
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

def test_a_date_after_the_cutoff_in_a_calculator_stage_is_named():
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


def test_a_number_that_is_not_finite_is_named(tmp_path):
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
