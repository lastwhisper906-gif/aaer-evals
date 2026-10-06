"""The owner's graders, two-sided: each fires on a planted fault and passes the clean run.

The clean run is a copy of CSCO's published run (#103). Each test plants one fault in
a fresh copy and expects exactly the grader that owns it to fail; the untouched copy
passes every grader. The DCF case is the hand-worked one in tests/test_calculator.py.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from evals.capability import golden
from evals.common import FAIL, PASS
from evals.golden_format import GoldenFormatError, loads
from evals.regression import coverage, mechanical

REPO = Path(__file__).resolve().parent.parent
CLEAN = REPO / "runs" / "CSCO" / "0000858877-26-000078"
# Read off the published run by hand: the accounting anomaly
# earnings_versus_cash_operating_cash_flow_falls_while_net_income_rises cites the
# reader item liquidity_and_capital_operating_cash_flow_nine_months, whose
# paragraph_id in report_numbers.md is the nine-month operating cash flow fact.
NINE_MONTH_CASH_FLOW = ("0000858877-26-000078:facts:NetCashProvidedByUsedInOperatingActivities:"
                        "2025-07-27..2026-04-25")


@pytest.fixture
def run(tmp_path):
    target = tmp_path / "CSCO" / CLEAN.name
    shutil.copytree(CLEAN, target, ignore=shutil.ignore_patterns("control-single-agent-analyses"))
    return target


def _edit(path: Path, change):
    data = json.loads(path.read_text(encoding="utf-8"))
    change(data)
    path.write_text(json.dumps(data), encoding="utf-8")


def _status(results, grader):
    return next(r.status for r in results if r.grader == grader)


def test_the_clean_run_passes_every_grader(run):
    results = mechanical.grade(run) + coverage.grade(run)
    assert [r.grader for r in results if r.status != PASS] == []


def test_the_hand_worked_cases_reproduce():
    assert all(r.status == PASS for r in mechanical.check_hand_worked_cases())
    gordon = mechanical.forecast(1000.0, mechanical.GORDON, 0.25, 0.09)
    assert gordon["enterprise_value"] == pytest.approx(1545.0)       # 92.7 / 0.06
    fade = mechanical.forecast(1000.0, mechanical.FADE, 0.25, 0.09)
    assert fade["enterprise_value"] == pytest.approx(2240.8020, abs=1e-4)


def test_an_altered_quote_fails_quotes_resolve(run):
    _edit(run / "analysis_valuation.json",
          lambda d: d["most_sensitive"][0].update(quote="a sentence no filing printed"))
    assert _status(mechanical.grade(run), "mechanical.quotes_resolve") == FAIL


def test_a_reader_quote_attached_to_the_wrong_paragraph_fails_quotes_resolve(run):
    """The quote still exists in the input, under another id; the check holds it
    to the paragraph the item names."""
    report = run / "report_numbers.md"
    text = report.read_text(encoding="utf-8")
    assert NINE_MONTH_CASH_FLOW in text
    report.write_text(text.replace(NINE_MONTH_CASH_FLOW,
                                   "0000858877-26-000078:facts:EntityPublicFloat:2025-01-24", 1),
                      encoding="utf-8")
    result = _status(mechanical.grade(run), "mechanical.quotes_resolve")
    assert result == FAIL


def test_a_run_with_no_record_of_what_an_agent_saw_fails_quotes_resolve(run):
    shutil.rmtree(run / "agents" / "numbers-reader")
    assert _status(mechanical.grade(run), "mechanical.quotes_resolve") == FAIL


def test_a_source_read_past_the_cutoff_fails_nothing_after_cutoff(run):
    def late(d):
        for doc in d["documents"]:
            if doc.get("rows_used_through"):
                doc["rows_used_through"] = "2099-01-01"
    _edit(run / "input_manifest.json", late)
    assert _status(mechanical.grade(run), "mechanical.nothing_after_cutoff") == FAIL


def test_a_price_dated_after_the_cutoff_fails_nothing_after_cutoff(run):
    _edit(run / "calculator.json", lambda d: d["market"]["price"].update(date="2099-01-01"))
    assert _status(mechanical.grade(run), "mechanical.nothing_after_cutoff") == FAIL


def test_a_kept_reader_item_without_a_quote_fails_quotes_resolve(run):
    report = run / "report_numbers.md"
    text = report.read_text(encoding="utf-8")
    report.write_text(text.replace('"quote": "', '"quote": "", "was": "', 1), encoding="utf-8")
    assert _status(mechanical.grade(run), "mechanical.quotes_resolve") == FAIL


def test_a_late_fact_in_a_calculator_stage_file_fails_nothing_after_cutoff(run):
    path = run / "calculator_filings_only.json"
    text = path.read_text(encoding="utf-8")
    data = json.loads(text)
    data["terms"]["balances_now"]["assets"]["filed"] = "2099-01-01"
    path.write_text(json.dumps(data), encoding="utf-8")
    assert _status(mechanical.grade(run), "mechanical.nothing_after_cutoff") == FAIL


def test_an_evidence_id_no_reader_kept_fails_cited_items_exist(run):
    _edit(run / "analysis_accounting.json",
          lambda d: d["anomalies"][0].update(evidence=["an_item_no_reader_wrote"]))
    assert _status(mechanical.grade(run), "mechanical.cited_items_exist") == FAIL


def test_evidence_that_is_not_a_list_fails_cited_items_exist(run):
    _edit(run / "analysis_accounting.json",
          lambda d: d["anomalies"][0].update(evidence=NINE_MONTH_CASH_FLOW))
    assert _status(mechanical.grade(run), "mechanical.cited_items_exist") == FAIL


def test_a_quote_from_a_file_the_analyst_was_not_handed_fails_quotes_resolve(run):
    _edit(run / "analysis_accounting.json", lambda d: d["anomalies"][0].update(
        quote="Revenue", quote_from="input_mdna.md"))        # the accounting analyst sees no filing
    assert _status(mechanical.grade(run), "mechanical.quotes_resolve") == FAIL


def test_a_quote_of_a_key_name_or_the_id_is_not_a_quote_of_the_row(run):
    """The nine-month cash flow row prints the tag and the key "value"; a quote of
    either carries nothing the filing said."""
    report = run / "report_numbers.md"
    text = report.read_text(encoding="utf-8")
    escaped = '\\"value\\": \\"8791000000\\"'       # as the fenced JSON prints the quote
    assert escaped in text
    report.write_text(text.replace(escaped, '\\"value\\"', 1), encoding="utf-8")
    assert _status(mechanical.grade(run), "mechanical.quotes_resolve") == FAIL
    assert mechanical.says_something('"value": "8791000000"', {"value", "tag"}, "x")
    assert mechanical.says_something('"missing": "no row for inventory_reserve: the', {"missing"}, "x")
    assert not mechanical.says_something('"value"', {"value"}, "x")
    assert not mechanical.says_something('"x", "tag":', {"value", "tag"}, "x")


def test_a_quote_spanning_two_files_fails_quotes_resolve(run):
    directory = run / "agents" / "accounting-analyst"
    end = (directory / "report_notes_text.md").read_text(encoding="utf-8")[-30:]
    start = (directory / "report_numbers.md").read_text(encoding="utf-8")[:30]
    _edit(run / "analysis_accounting.json",
          lambda d: d["anomalies"][0].update(quote=end + "\n" + start))
    assert _status(mechanical.grade(run), "mechanical.quotes_resolve") == FAIL


def test_a_path_the_calculator_lacks_fails_cited_numbers_exist(run):
    _edit(run / "analysis_accounting.json", lambda d: d["areas"]["cost_deferral"].update(
        finding="Capitalized software is {terms.balances_now.no_such_balance}."))
    assert _status(mechanical.grade(run), "mechanical.cited_numbers_exist") == FAIL


def test_a_price_path_in_the_filings_only_view_fails_cited_numbers_exist(run):
    _edit(run / "analysis_financial.json", lambda d: d["sections"]["growth"].update(
        reading="The price is {cost_of_capital.price_at_cutoff}."))
    assert _status(mechanical.grade(run), "mechanical.cited_numbers_exist") == FAIL


def test_a_document_after_the_cutoff_fails_nothing_after_cutoff(run):
    _edit(run / "input_manifest.json",
          lambda d: d["documents"][0].update(filing_date="2099-01-01"))
    assert _status(mechanical.grade(run), "mechanical.nothing_after_cutoff") == FAIL


def test_a_non_finite_value_fails_calculator_finite(run):
    text = (run / "calculator.json").read_text(encoding="utf-8")
    data = json.loads(text)
    data["ratios"]["liquidity"]["current_ratio"]["value"] = float("nan")
    (run / "calculator.json").write_text(json.dumps(data), encoding="utf-8")
    assert _status(mechanical.grade(run), "mechanical.calculator_finite") == FAIL


def test_a_tampered_enterprise_value_fails_dcf_recomputes(run):
    _edit(run / "calculator.json",
          lambda d: d["valuation"]["scenarios"]["base"].update(enterprise_value=1.0))
    assert _status(mechanical.grade(run), "mechanical.dcf_recomputes") == FAIL


def test_a_failed_agent_fails_agents_written(run):
    _edit(run / "input_manifest.json",
          lambda d: d["agents"]["financial-analyst"].update(result="failed"))
    assert _status(mechanical.grade(run), "mechanical.agents_written") == FAIL


def test_a_missing_file_fails_files_present(run):
    (run / "memo_ko.md").unlink()
    assert _status(mechanical.grade(run), "mechanical.files_present") == FAIL


def test_an_absent_area_fails_and_a_dropped_one_does_not(run):
    _edit(run / "analysis_accounting.json",
          lambda d: d["areas"]["industry_lens"].update(dropped="finding: the gate's reason"))
    assert _status(coverage.grade(run), "coverage.accounting_areas") == PASS
    _edit(run / "analysis_accounting.json", lambda d: d["areas"].pop("industry_lens"))
    assert _status(coverage.grade(run), "coverage.accounting_areas") == FAIL


def test_an_absent_dupont_fails_financial_sections(run):
    _edit(run / "analysis_financial.json", lambda d: d.pop("dupont"))
    assert _status(coverage.grade(run), "coverage.financial_sections") == FAIL


def test_no_range_and_no_reason_fails_valuation_answer(run):
    _edit(run / "calculator.json", lambda d: d["valuation"].update(
        value_range_per_share=None, scenarios={}))
    assert _status(coverage.grade(run), "coverage.valuation_answer") == FAIL


def test_a_memo_without_the_finance_frame_fails_memo_frames(run):
    memo = run / "memo_ko.md"
    memo.write_text("\n".join(line for line in memo.read_text(encoding="utf-8").splitlines()
                              if not (line.startswith("#") and "재무" in line)), encoding="utf-8")
    assert _status(coverage.grade(run), "coverage.memo_frames") == FAIL


def test_a_recommendation_in_the_valuation_fails_forbidden_words(run):
    _edit(run / "analysis_valuation.json", lambda d: d["value_range"].update(
        reading=d["value_range"]["reading"] + " Investors should buy."))
    assert _status(coverage.grade(run), "coverage.forbidden_words") == FAIL


def test_an_accusation_anywhere_fails_forbidden_words(run):
    _edit(run / "analysis_accounting.json", lambda d: d["areas"]["cost_deferral"].update(
        finding="This looks like fraud."))
    assert _status(coverage.grade(run), "coverage.forbidden_words") == FAIL


def test_a_company_selling_product_is_not_a_recommendation(run):
    _edit(run / "analysis_accounting.json", lambda d: d["areas"]["cost_deferral"].update(
        finding="Credit extended to sell product and an agreement to buy a supplier."))
    assert _status(coverage.grade(run), "coverage.forbidden_words") == PASS


def test_a_score_field_fails_no_combined_score(run):
    _edit(run / "analysis_financial.json", lambda d: d.update(overall_score=0.7))
    assert _status(coverage.grade(run), "coverage.no_combined_score") == FAIL


# --- golden cases ----------------------------------------------------------------------------

CASE = {"filing": {"accession": "0000858877-26-000078"}, "frame": "accounting",
        "must_find": [{"area": "earnings_versus_cash", "what": "income up, cash down",
                       "keywords": ["operating cash flow falls"]},
                      {"what": "a finding nobody made", "keywords": ["zeppelin"]}],
        "must_not_claim": [{"what": "a claim nobody made", "keywords": ["zeppelin"]}],
        "approved_by_owner": True}


def test_golden_scores_found_and_missed_with_partial_credit():
    row = golden.score_run(CASE, CLEAN)
    assert row["found"] == ["income up, cash down"]
    assert row["missed"] == ["a finding nobody made"]
    assert row["score"] == pytest.approx(0.5)


def test_golden_takes_credit_away_for_a_claim_it_must_not_make():
    case = dict(CASE, must_not_claim=[{"what": "x", "keywords": ["operating cash flow falls"]}])
    assert golden.score_run(case, CLEAN)["score"] == pytest.approx(0.0)


def test_golden_counts_only_approved_cases_in_cases():
    assert all(case.get("approved_by_owner") is True for _, case in golden.approved_cases())


def test_the_case_format_reads_the_template_and_refuses_what_it_cannot_read():
    template = loads((REPO / "evals" / "golden" / "TEMPLATE.yaml").read_text(encoding="utf-8"))
    assert template["approved_by_owner"] is False
    assert template["must_find"][0]["paragraph_ids"] == ["0000000000-00-000000:notes:0"]
    for bad in ("a:\n\tb: 1\n", 'a: "open\n', "a: 1\na: 2\n", "a: {b: 1}\n"):
        with pytest.raises(GoldenFormatError):
            loads(bad)


def test_golden_credits_a_filing_paragraph_reached_through_a_reader_item():
    case = dict(CASE, must_find=[{"what": "by paragraph", "paragraph_ids": [NINE_MONTH_CASH_FLOW]}],
                must_not_claim=[])
    assert golden.score_run(case, CLEAN)["score"] == pytest.approx(1.0)
    # a paragraph no reader item cites reaches nothing
    case = dict(case, must_find=[{"what": "x", "paragraph_ids": ["0000858877-26-000078:notes:1"]}])
    assert golden.score_run(case, CLEAN)["score"] == pytest.approx(0.0)


def test_golden_keywords_are_whole_words():
    anomaly = {"id": "a", "name": "an improbable shortfall to resell", "what": ""}
    for word in ("probable", "falls", "sell"):
        assert not golden.matches(anomaly, {"keywords": [word]}), word
    assert golden.matches(anomaly, {"keywords": ["improbable resell"]})


def test_golden_credits_nothing_to_evidence_that_resolves_to_no_reader_item():
    anomaly = {"id": "a", "area": "x", "evidence": ["0000858877-26-000078:notes:1"],
               "paragraphs": set()}
    assert not golden.matches(anomaly, {"paragraph_ids": ["0000858877-26-000078:notes:1"]})


# --- the capability graders that read more than one run -----------------------------------

from evals.capability import consistency, grader_agreement, memorization, outcomes, rubric_score  # noqa: E402


def test_consistency_is_one_for_identical_runs_and_less_when_they_differ(tmp_path, monkeypatch):
    first = tmp_path / "CSCO" / "a"
    second = tmp_path / "CSCO" / "b"
    for target in (first, second):
        shutil.copytree(CLEAN, target, ignore=shutil.ignore_patterns("agents", "control-*"))
    monkeypatch.setattr(golden, "approved_cases", lambda: [(Path("case.yaml"), CASE)])
    same = consistency.grade([first, second])
    assert same["cases"][0]["anomaly_overlap"] == pytest.approx(1.0)
    assert same["cases"][0]["value_spread"] == pytest.approx(0.0)
    _edit(second / "analysis_accounting.json", lambda d: d.update(anomalies=d["anomalies"][:1]))
    differ = consistency.grade([first, second])
    assert differ["cases"][0]["anomaly_overlap"] < 1.0


# Read off the published run by hand: the one accounting anomaly whose name holds
# the words "operating cash flow falls" is this one.
CASH_FALLS = "earnings_versus_cash_operating_cash_flow_falls_while_net_income_rises"


def test_grader_agreement_counts_where_the_grader_matches_the_owner(tmp_path, monkeypatch):
    run = tmp_path / "CSCO" / CLEAN.name
    shutil.copytree(CLEAN, run, ignore=shutil.ignore_patterns("agents", "control-*"))
    (run / "grade.json").write_text(json.dumps({"items": [
        {"id": CASH_FALLS, "verdict": "supported", "severity": "high"}]}))
    monkeypatch.setattr(golden, "approved_cases", lambda: [(Path("case.yaml"), CASE)])
    assert grader_agreement.grade([run])["score"] == pytest.approx(1.0)
    (run / "grade.json").write_text(json.dumps({"items": [
        {"id": CASH_FALLS, "verdict": "unsupported", "severity": "high"}]}))
    assert grader_agreement.grade([run])["score"] == pytest.approx(0.0)


def test_outcomes_wait_sixty_trading_days_counted_from_the_day_after_the_filing():
    """CSCO's cutoff is 2026-05-19, a Tuesday. The filing day is not counted, so
    the first counted day is Wednesday the 20th and the sixtieth is 2026-08-11."""
    import datetime as dt
    assert outcomes.weekdays_between(dt.date(2026, 5, 19), dt.date(2026, 5, 19)) == 0
    assert outcomes.weekdays_between(dt.date(2026, 5, 19), dt.date(2026, 5, 20)) == 1
    early = outcomes.grade([CLEAN], today=dt.date(2026, 8, 10))["runs"][0]
    late = outcomes.grade([CLEAN], today=dt.date(2026, 8, 11))["runs"][0]
    assert early["status"] == "pending" and early["trading_days_since"] == 59
    assert late["status"] == "aged" and late["trading_days_since"] == 60


def test_outcomes_count_company_events_and_never_the_ledgers_process_rows(tmp_path):
    import datetime as dt
    ledger = tmp_path / "ledger.jsonl"
    ledger.write_text("\n".join([
        json.dumps({"ticker": "CSCO", "date": "2026-06-01", "event": "restatement"}),
        json.dumps({"ticker": "CSCO", "date": "2026-05-01", "event": "earlier"}),
        json.dumps({"ticker": "CSCO", "at": "2026-06-01T00:00:00+00:00", "accession": "x",
                    "layers_that_ran": ["detect filing"]}),
        json.dumps({"at": "2026-06-02T00:00:00+00:00", "lens": "codex", "verdict": "pass"}),
    ]) + "\n")
    out = outcomes.grade([CLEAN], today=dt.date(2026, 9, 1), ledger=ledger)
    assert out["runs"][0]["events"] == 1
    assert "no company event row" not in out["status"]
    assert "no company event row" in outcomes.grade([CLEAN], today=dt.date(2026, 9, 1),
                                                    ledger=tmp_path / "none")["status"]


def test_memorization_never_calls_a_run_clean_without_a_cutoff_on_record(monkeypatch):
    assert memorization.classify(CLEAN)["status"] == "unknown"
    monkeypatch.setattr(memorization, "TRAINING_CUTOFF",
                        {"claude-fable-5-1": ("2026-01", "s"), "claude-opus-5-5": ("2026-01", "s")})
    assert memorization.classify(CLEAN)["status"] == "forward"       # filed 2026-05
    monkeypatch.setattr(memorization, "TRAINING_CUTOFF",
                        {"claude-fable-5-1": ("2026-06", "s"), "claude-opus-5-5": ("2026-01", "s")})
    assert memorization.classify(CLEAN)["status"] == "historical"


def test_memorization_calls_a_run_with_no_served_model_unknown(tmp_path):
    run = tmp_path / "CSCO" / CLEAN.name
    shutil.copytree(CLEAN, run, ignore=shutil.ignore_patterns("agents", "control-*"))
    _edit(run / "input_manifest.json", lambda d: d.update(agents={}))
    assert memorization.classify(run)["status"] == "unknown"


def test_the_grader_score_is_recomputed_from_its_items():
    """High supported (3 x 1) + medium unclear (2 x 0.5) + low unsupported (1 x 0),
    over weight 6: 4 / 6. A dealbreaker on the first item takes its 3 away: 1 / 6."""
    grade = {"items": [{"id": "a", "verdict": "supported", "severity": "high"},
                       {"id": "b", "verdict": "unclear", "severity": "medium"},
                       {"id": "c", "verdict": "unsupported", "severity": "low"}],
             "score": 0.9}
    out = rubric_score.check(grade)
    assert out["score"] == pytest.approx(4 / 6) and out["agrees"] is False
    grade["dealbreakers"] = [{"kind": "number_not_from_calculator", "id": "a",
                              "where": "anomalies[0].what", "why": "a bare figure"}]
    assert rubric_score.recompute(grade) == pytest.approx(1 / 6)
    # a whole-run dealbreaker with no id strikes no item
    grade["dealbreakers"] = [{"kind": "post_cutoff_fact", "id": None, "where": "memo", "why": "x"}]
    assert rubric_score.recompute(grade) == pytest.approx(4 / 6)


# --- the eval runner: exit status, floors, the scoreboard and --quick ----------------------

from evals import __main__ as runner  # noqa: E402


def _isolated(monkeypatch, tmp_path, runs):
    monkeypatch.setattr(runner, "SCOREBOARD", tmp_path / "scoreboard.jsonl")
    monkeypatch.setattr(runner, "THRESHOLDS", tmp_path / "thresholds.json")
    monkeypatch.setattr(runner, "find_runs", lambda paths=None: runs)
    monkeypatch.setattr(runner, "changed_runs", lambda base="origin/main": runs)


def test_make_eval_exits_zero_on_the_clean_run_and_appends_one_scoreboard_line(run, monkeypatch, tmp_path):
    _isolated(monkeypatch, tmp_path, [run])
    assert runner.main([]) == 0
    assert runner.main([]) == 0
    lines = (tmp_path / "scoreboard.jsonl").read_text().splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["regression"]["fail"] == 0


def test_make_eval_exits_one_on_a_regression_failure(run, monkeypatch, tmp_path):
    _isolated(monkeypatch, tmp_path, [run])
    (run / "memo_ko.md").unlink()
    assert runner.main(["--no-scoreboard"]) == 1


def test_make_eval_exits_one_below_a_floor_the_owner_set(run, monkeypatch, tmp_path):
    _isolated(monkeypatch, tmp_path, [run])
    (tmp_path / "thresholds.json").write_text(json.dumps(
        {"capability": {"coverage.accounting_areas_answered": 1.01}}))
    assert runner.main(["--no-scoreboard"]) == 1
    (tmp_path / "thresholds.json").write_text("{}")
    assert runner.main(["--no-scoreboard"]) == 0


def test_eval_quick_grades_only_the_changed_runs_and_writes_no_scoreboard(run, monkeypatch, tmp_path):
    _isolated(monkeypatch, tmp_path, [run])
    assert runner.main(["--quick"]) == 0
    assert not (tmp_path / "scoreboard.jsonl").exists()
    monkeypatch.setattr(runner, "changed_runs", lambda base="origin/main": [])
    assert runner.main(["--quick"]) == 0
