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
