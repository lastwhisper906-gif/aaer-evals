"""The improvement loop's two fixed tools (`docs/improve_loop.md`): `mine`, the
table of what a run shows, and `measure`, the reruns and the acceptance rule.

Every expected value is a count made by hand over an analysis, a manifest or a
grade written in this file, or the acceptance rule of `measure`'s docstring
applied by hand to metrics rows written here on both sides of its line.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.improve import measure, mine

# --- a run written by hand ------------------------------------------------------------------

ACCOUNTING = {
    "areas": {"earnings_versus_cash": {"finding": "stands", "evidence": []},
              "revenue_recognition": {"dropped": "finding: a number written in the analyst's own words: 'x 4.8'"},
              "cost_deferral": {"dropped": "finding: a number written in the analyst's own words: 'y 7'"}},
    "reconciliation": [{"outcome": "confirms"}, {"outcome": "confirms"}, {"outcome": "unresolved"}],
    "anomalies": [{"id": "a"}, {"id": "b"}, {"id": "c"}, {"id": "d"}],
    "adjustments": [],
    "dropped_items": [
        {"where": "areas.revenue_recognition", "reason": "finding: a number written in the analyst's own words: 'x 4.8'"},
        {"where": "areas.cost_deferral", "reason": "finding: a number written in the analyst's own words: 'y 7'"},
        {"where": "anomalies[9]", "reason": "evidence: 'notes:99' is not an item of a report this analyst saw"}],
    "dropped_count": 3}
FINANCIAL = {
    "sections": {"profitability": {"reading": "stands"}, "liquidity": {"reading": "stands"}},
    "dupont": {"reading": "stands"}, "path_to_distress": {"dropped": "reading: a number written in the analyst's own words: '53 weeks'"},
    "anomalies": [{"id": "a"}], "dropped_items": [
        {"where": "path_to_distress", "reason": "reading: a number written in the analyst's own words: '53 weeks'"}],
    "dropped_count": 1}
MANIFEST = {"ticker": "TEST", "form": "10-Q", "filing_date": "2026-08-01",
            "analysis_stages": {"quote_gate": {"dropped": 2}},
            "agents": {"accounting-analyst": {"result": "written", "model_served": "claude-opus-5-5",
                                              "attempts": [{"attempt": 1}, {"attempt": 2}],
                                              "output_tokens": 1000, "cost_usd": 4.0, "seconds": 60.0,
                                              "gate_feedback": [{"dropped_count": 3, "text": "..."}]},
                       "financial-analyst": {"result": "written", "model_served": "claude-opus-5-5",
                                             "attempt": 1, "output_tokens": 500, "cost_usd": 2.0,
                                             "seconds": 30.0}}}
GRADE = {"score": 0.9, "dealbreakers": [{"kind": "unsupported_claim"}, {"kind": "unsupported_claim"}],
         "grader": {"cost_usd": 6.0}}


def a_run(root: Path, ticker="TEST", accession="0000000000-26-000001", *, grade=True) -> Path:
    run = root / ticker / accession
    run.mkdir(parents=True)
    (run / "input_manifest.json").write_text(json.dumps(dict(MANIFEST, ticker=ticker)))
    (run / "analysis_accounting.json").write_text(json.dumps(ACCOUNTING))
    (run / "analysis_financial.json").write_text(json.dumps(FINANCIAL))
    if grade:
        (run / "grade.json").write_text(json.dumps(GRADE))
    return run


# --- mine ---------------------------------------------------------------------------------

def test_reason_classes_cut_the_particulars_and_keep_the_rule():
    own = "finding: a number written in the analyst's own words: 'x 4.8'"
    assert mine.reason_class(own) == "a number written in the analyst's own words"
    assert mine.reason_class("reading: a number written in the analyst's own words: '53'") == mine.reason_class(own)
    assert mine.reason_class("evidence: 'notes:99' is not an item of a report this analyst saw") == (
        "is not an item of a report this analyst saw")
    assert mine.reason_class("{valuation.price_position} is not a number in the calculator this analyst saw") == (
        "is not a number in the calculator this analyst saw")
    assert mine.reason_class("fields: 'x.y' is not a field of calculator.json") == "is not a field of calculator.json"
    assert mine.reason_class("revenue_growth_year_one: reason: a number written in the analyst's own words: '3'") == (
        "a number written in the analyst's own words")
    assert mine.reason_class(None) == "(no reason)"


def test_the_accounting_row_counts_by_hand(tmp_path):
    run = a_run(tmp_path)
    rows = {row["agent"]: row for row in mine.rows_of(run)}
    assert set(rows) == {"accounting-analyst", "financial-analyst"}
    acc = rows["accounting-analyst"]
    assert acc["ticker"] == "TEST" and acc["file"] == "analysis_accounting.json"
    assert acc["dropped_count"] == 3
    assert acc["drops_by_reason"] == {"a number written in the analyst's own words": 2,
                                      "is not an item of a report this analyst saw": 1}
    assert (acc["blocks"], acc["empty_blocks"]) == (3, 2)
    assert (acc["anomalies"], acc["adjustments"], acc["reconciliation"]) == (4, 0, 3)
    assert acc["reconciliation_outcomes"] == {"confirms": 2, "unresolved": 1}
    assert acc["quote_gate_dropped"] == 2
    assert acc["attempts"] == 2 and acc["gate_feedback_rounds"] == 1
    assert (acc["output_tokens"], acc["cost_usd"], acc["model_served"]) == (1000, 4.0, "claude-opus-5-5")
    assert acc["grade_score"] == 0.9 and acc["grade_dealbreakers"] == 2
    assert acc["grade_dealbreaker_kinds"] == {"unsupported_claim": 2}


def test_the_financial_row_counts_dupont_and_the_distress_path_as_blocks(tmp_path):
    fin = {row["agent"]: row for row in mine.rows_of(a_run(tmp_path))}["financial-analyst"]
    assert (fin["blocks"], fin["empty_blocks"]) == (4, 1)
    assert fin["anomalies"] == 1 and "adjustments" not in fin
    assert fin["attempts"] == 1 and fin["gate_feedback_rounds"] == 0


def test_a_run_without_a_grade_or_a_manifest(tmp_path):
    rows = mine.rows_of(a_run(tmp_path, grade=False))
    assert rows and all(row["grade_score"] is None and row["grade_dealbreakers"] is None for row in rows)
    (tmp_path / "empty").mkdir()
    assert mine.rows_of(tmp_path / "empty") == []


def test_runs_under_finds_each_run_once_and_the_table_prints_every_row(tmp_path):
    a_run(tmp_path, "A"); a_run(tmp_path, "B", "0000000000-26-000002")
    found = mine.runs_under(tmp_path)
    assert [p.parent.name for p in found] == ["A", "B"]
    assert mine.runs_under(found[0]) == [found[0]]
    rows = [row for run in found for row in mine.rows_of(run)]
    text = mine.table(rows)
    assert text.count("| A 0000000000-26-000001 |") == 2 and "| B 0000000000-26-000002 |" in text
    assert "| analysis_accounting.json | a number written in the analyst's own words | 4 |" in text


def test_the_command_prints_json_lines(tmp_path, capsys, monkeypatch):
    a_run(tmp_path)
    monkeypatch.setattr(mine.interpreter_pin, "enforce", lambda: 0)
    assert mine.main(["--runs", str(tmp_path)]) == 0
    lines = [json.loads(line) for line in capsys.readouterr().out.splitlines()]
    assert [row["agent"] for row in lines] == ["accounting-analyst", "financial-analyst"]


# --- measure: draw and plan -----------------------------------------------------------------

def test_the_draw_leaves_out_held_in_runs_and_repeats_under_its_seed(tmp_path):
    runs = [a_run(tmp_path, t, f"0000000000-26-00000{i}") for i, t in enumerate("ABCDE", 1)]
    drawn = measure.draw(tmp_path, [str(runs[0]), str(runs[1])], 2, seed=7)
    assert drawn["seed"] == 7 and drawn["pool"] == 3 and len(drawn["held_out"]) == 2
    assert not {str(runs[0].resolve()), str(runs[1].resolve())} & set(drawn["held_out"])
    assert measure.draw(tmp_path, [str(runs[0]), str(runs[1])], 2, seed=7) == drawn
    assert measure.draw(tmp_path, [], 9, seed=1)["held_out"] == sorted(str(r.resolve()) for r in runs)
    assert isinstance(measure.draw(tmp_path, [], 1)["seed"], int)


def test_the_plan_is_the_recorded_costs_times_the_repeats(tmp_path):
    run = a_run(tmp_path)
    estimate = measure.plan([run], ["accounting-analyst", "financial-analyst"], 2)
    assert estimate["estimate_usd"] == 12.0 and estimate["unknown"] == []    # (4 + 2) x 2
    with_grade = measure.plan([run], ["accounting-analyst"], 3, grade=True)
    assert with_grade["estimate_usd"] == 30.0                                 # 4 x 3 + 6 x 3
    assert measure.plan([run], ["valuation-analyst"], 1)["unknown"] == [f"{run}:valuation-analyst"]


def test_the_command_refuses_a_plan_over_budget_and_runs_nothing(tmp_path, capsys, monkeypatch):
    run = a_run(tmp_path)
    monkeypatch.setattr(measure.interpreter_pin, "enforce", lambda: 0)
    called = []
    monkeypatch.setattr(measure, "measure", lambda *a, **k: called.append(1) or [])
    assert measure.main(["run", "--runs", str(run), "--agents", "accounting-analyst", "--repeats", "2",
                         "--budget-usd", "7.99", "--work", str(tmp_path / "work")]) == measure.OVER_BUDGET
    assert "exceeds the budget" in capsys.readouterr().err and called == []
    assert measure.main(["plan", "--runs", str(run), "--agents", "accounting-analyst", "--repeats", "2",
                         "--budget-usd", "8"]) == 0


def test_a_version_string_is_never_a_model(tmp_path):
    with pytest.raises(measure.MeasureError, match="alias"):
        measure.alias_only("claude-opus-5-5")
    assert measure.alias_only("opus") == "opus"
    with pytest.raises(measure.MeasureError):
        measure.measure([], ["accounting-analyst"], 1, work=tmp_path, model="opus-5")


# --- measure: run over a stubbed rerun ------------------------------------------------------

def test_measure_reruns_on_copies_and_tags_each_row(tmp_path):
    run = a_run(tmp_path / "runs")
    seen = []

    def rerun(copy, agent, *, model, grade):
        seen.append((copy, agent, model, grade))
        payload = json.loads((copy / "analysis_accounting.json").read_text())
        payload["dropped_items"], payload["dropped_count"] = [], 0
        (copy / "analysis_accounting.json").write_text(json.dumps(payload))
        return copy
    rows = measure.measure([run], ["accounting-analyst"], 2, work=tmp_path / "work", model="opus",
                           grade=True, rerun=rerun)
    assert sorted(c.name for c, *_ in seen) == ["0000000000-26-000001-r1", "0000000000-26-000001-r2"]
    assert all(c.is_relative_to(tmp_path / "work") for c, *_ in seen)
    assert all(m == "opus" and g for _, _, m, g in seen)
    assert sorted((r["source"], r["repeat"], r["dropped_count"]) for r in rows) == [
        (str(run), 1, 0), (str(run), 2, 0)]
    # the published run is untouched
    assert json.loads((run / "analysis_accounting.json").read_text())["dropped_count"] == 3


# --- measure: the acceptance rule on rows written by hand -----------------------------------

def _row(source, agent, repeat, **metrics):
    base = {"dropped_count": 10, "empty_blocks": 5, "anomalies": 20, "grade_score": 0.9,
            "grade_dealbreakers": 1}
    return dict(base, source=source, agent=agent, repeat=repeat, **metrics)


IN, OUT, AGENT = "/r/held-in", "/r/held-out", "accounting-analyst"


def test_a_move_beyond_the_spread_with_no_regression_is_accepted():
    baseline = [_row(IN, AGENT, 1, dropped_count=10), _row(IN, AGENT, 2, dropped_count=12),
                _row(OUT, AGENT, 1), _row(OUT, AGENT, 2)]
    candidate = [_row(IN, AGENT, 1, dropped_count=8), _row(IN, AGENT, 2, dropped_count=8),
                 _row(OUT, AGENT, 1), _row(OUT, AGENT, 2)]
    # baseline mean 11, spread 2; candidate mean 8: better by 3 > 2 -> moved
    verdict = measure.compare(baseline, candidate, held_in=[IN], target="dropped_count")
    assert verdict["accepted"] and verdict["regressions"] == [] and not verdict["one_repeat"]
    cell = next(c for c in verdict["cells"] if c["metric"] == "dropped_count" and c["where"] == "held_in")
    assert (cell["baseline_mean"], cell["candidate_mean"], cell["spread"], cell["reading"]) == (11, 8, 2, "moved")


def test_a_move_inside_the_spread_is_not_a_move():
    baseline = [_row(IN, AGENT, 1, dropped_count=10), _row(IN, AGENT, 2, dropped_count=14)]
    candidate = [_row(IN, AGENT, 1, dropped_count=9), _row(IN, AGENT, 2, dropped_count=9)]
    # mean 12, spread 4; candidate 9: better by 3, not > 4 -> within spread
    verdict = measure.compare(baseline, candidate, held_in=[IN], target="dropped_count")
    assert not verdict["accepted"] and not verdict["target_moved_on_every_held_in_run"]
    assert verdict["cells"][0]["reading"] == "within spread"


def test_a_regression_on_a_held_out_run_refuses_the_edit():
    baseline = [_row(IN, AGENT, 1, dropped_count=10), _row(IN, AGENT, 2, dropped_count=10),
                _row(OUT, AGENT, 1, grade_score=0.9), _row(OUT, AGENT, 2, grade_score=0.9)]
    candidate = [_row(IN, AGENT, 1, dropped_count=0), _row(IN, AGENT, 2, dropped_count=0),
                 _row(OUT, AGENT, 1, grade_score=0.8), _row(OUT, AGENT, 2, grade_score=0.8)]
    verdict = measure.compare(baseline, candidate, held_in=[IN], target="dropped_count")
    assert verdict["target_moved_on_every_held_in_run"] and not verdict["accepted"]
    assert verdict["regressions"] == [f"{OUT} {AGENT} grade_score"]


def test_fewer_anomalies_beyond_the_spread_is_a_regression_on_the_held_in_run_too():
    baseline = [_row(IN, AGENT, 1, anomalies=20), _row(IN, AGENT, 2, anomalies=22)]
    candidate = [_row(IN, AGENT, 1, dropped_count=0, anomalies=10),
                 _row(IN, AGENT, 2, dropped_count=0, anomalies=10)]
    verdict = measure.compare(baseline, candidate, held_in=[IN], target="dropped_count")
    assert verdict["regressions"] == [f"{IN} {AGENT} anomalies"] and not verdict["accepted"]


def test_the_target_must_move_on_every_held_in_run():
    second = "/r/held-in-2"
    baseline = [_row(IN, AGENT, 1), _row(second, AGENT, 1)]
    candidate = [_row(IN, AGENT, 1, dropped_count=0), _row(second, AGENT, 1)]
    verdict = measure.compare(baseline, candidate, held_in=[IN, second], target="dropped_count")
    assert verdict["held_in_runs_measured"] == 1 and not verdict["accepted"]
    assert verdict["one_repeat"]


def test_a_missing_metric_is_unmeasured_and_an_unknown_target_is_refused():
    baseline = [_row(IN, AGENT, 1, grade_score=None)]
    candidate = [_row(IN, AGENT, 1, grade_score=None, dropped_count=0)]
    verdict = measure.compare(baseline, candidate, held_in=[IN], target="dropped_count")
    assert next(c["reading"] for c in verdict["cells"] if c["metric"] == "grade_score") == "unmeasured"
    with pytest.raises(measure.MeasureError, match="target"):
        measure.compare(baseline, candidate, held_in=[IN], target="cost_usd")


def test_the_compare_command_exits_zero_only_on_acceptance(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(measure.interpreter_pin, "enforce", lambda: 0)
    base, cand = tmp_path / "b.jsonl", tmp_path / "c.jsonl"
    base.write_text("\n".join(json.dumps(r) for r in [_row(IN, AGENT, 1), _row(IN, AGENT, 2)]))
    cand.write_text("\n".join(json.dumps(r) for r in [_row(IN, AGENT, 1, dropped_count=0),
                                                      _row(IN, AGENT, 2, dropped_count=0)]))
    assert measure.main(["compare", "--baseline", str(base), "--candidate", str(cand),
                         "--held-in", IN, "--target", "dropped_count"]) == 0
    assert json.loads(capsys.readouterr().out)["accepted"] is True
    assert measure.main(["compare", "--baseline", str(base), "--candidate", str(base),
                         "--held-in", IN, "--target", "dropped_count"]) == 1


# --- the fences guard ----------------------------------------------------------------------

import importlib.util
import subprocess

GUARD = Path(__file__).resolve().parent.parent / ".claude" / "hooks" / "guard_fences.py"


def _guard():
    spec = importlib.util.spec_from_file_location("guard_fences", GUARD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("command", [
    "echo x > runs/FN/0001408710-26-000028/memo_ko.md",
    "sed -i 's/a/b/' src/analysis_check.py",
    "cp x tests/fixtures/FN/expected.json",
    "rm -rf history/FN",
    "git checkout -- src/calculator.py",
    "echo '{}' >> docs/improve/ledger.jsonl",
    "touch .claude/settings.json",
    "mv a .github/workflows/ci.yml",
    "cd rules && rm x",
])
def test_the_fences_guard_refuses_a_shell_write_to_a_fence(command):
    assert "fenced path" in _guard().refused(command)


@pytest.mark.parametrize("command", [
    "cat src/analysis_check.py",
    "git diff origin/main -- runs/",
    ".venv/bin/python -m src.improve.measure run --runs runs/FN/x --agents financial-analyst --work /tmp/w --budget-usd 5",
    ".venv/bin/python -m src.improve.mine --runs runs --table",
    "make eval-quick PYTHON=.venv/bin/python",
    "echo x > docs/improve/weakness.md",
    "echo x > .claude/agents/accounting-analyst.md",
    "echo x > src/analysis_hook.py",
    ".venv/bin/python -m pytest tests/test_improve.py -q",
])
def test_the_fences_guard_lets_reading_measuring_and_editable_surfaces_through(command):
    assert _guard().refused(command) is None


def test_the_fences_guard_blocks_with_exit_two_and_prints_its_deny_rules():
    payload = json.dumps({"tool_input": {"command": "rm runs/x"}})
    done = subprocess.run(["python3", str(GUARD)], input=payload, capture_output=True, text=True)
    assert done.returncode == 2 and "fenced path" in done.stderr
    rules = json.loads(subprocess.run(["python3", str(GUARD), "--deny-rules"],
                                      capture_output=True, text=True).stdout)
    assert "Edit(runs/**)" in rules and "Write(src/analysis_check.py)" in rules
    assert "Edit(.claude/agents/analysis-grader.md)" in rules
    assert not any("accounting-analyst" in rule for rule in rules)
