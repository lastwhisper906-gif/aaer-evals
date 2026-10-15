"""The analysis gate, read to an analyst at write time (`src/analysis_hook.py`).

Every expected value below is a rule stated in the hook's docstring or in the
three analyst prompts, applied to a file written in this test: a digit in an
analyst's own words is a drop the session is told about, with where it is and
why; a file the gate does not read, or an agent it does not read, is passed in
silence; the hook goes quiet after `MAX_FEEDBACK` messages; and the command
`run_analysis` builds hands a restricted session this hook through `--settings`.
"""

from __future__ import annotations

import json
from pathlib import Path

from src import analysis_hook, run_analysis


def _event(path: Path) -> dict:
    return {"tool_name": "Write", "tool_input": {"file_path": str(path)}}


def _gate(monkeypatch, answer):
    """The gate stubbed: `answer` is what it returns, or the exception it raises."""
    asked = []

    def check_analysis(run, name, kind):
        asked.append((name, kind))
        if isinstance(answer, Exception):
            raise answer
        return answer
    monkeypatch.setattr(run_analysis, "check_analysis", check_analysis)
    return asked


DROPPED = {"dropped_count": 1, "dropped_items": [
    {"where": "areas.revenue_recognition",
     "reason": "finding: a number written in the analyst's own words: 'recognized $4.8 million'"}]}


def test_a_drop_is_handed_back_with_where_and_why(tmp_path, monkeypatch):
    asked = _gate(monkeypatch, DROPPED)
    feedback = tmp_path / "fb.jsonl"
    code, text = analysis_hook.respond(
        _event(tmp_path / "analysis_accounting.json"), run=tmp_path,
        agent="accounting-analyst", feedback=feedback)
    assert code == analysis_hook.HAND_BACK == 2
    assert asked == [("accounting-analyst", "accounting")]
    assert text.startswith(analysis_hook.HEADER)
    assert "- areas.revenue_recognition: finding: a number written" in text
    rows = [json.loads(line) for line in feedback.read_text().splitlines()]
    assert rows == [{"dropped_count": 1, "text": text}]


def test_each_gated_agent_is_read_as_its_own_kind(tmp_path, monkeypatch):
    asked = _gate(monkeypatch, DROPPED)
    for agent, written in (("financial-analyst", "analysis_financial.json"),
                           ("valuation-analyst", "assumptions.json"),
                           ("valuation-analyst-second-pass", "analysis_valuation.json")):
        analysis_hook.respond(_event(tmp_path / written), run=tmp_path, agent=agent,
                              feedback=tmp_path / f"{agent}.jsonl")
    assert asked == [("financial-analyst", "financial"),
                     ("valuation-analyst", "assumptions"),
                     ("valuation-analyst-second-pass", "valuation")]


def test_a_file_that_stands_is_passed_in_silence(tmp_path, monkeypatch):
    _gate(monkeypatch, {"dropped_count": 0, "dropped_items": []})
    feedback = tmp_path / "fb.jsonl"
    assert analysis_hook.respond(_event(tmp_path / "analysis_financial.json"), run=tmp_path,
                                 agent="financial-analyst", feedback=feedback) == (0, "")
    assert not feedback.exists()


def test_another_file_and_another_agent_are_not_read(tmp_path, monkeypatch):
    asked = _gate(monkeypatch, DROPPED)
    feedback = tmp_path / "fb.jsonl"
    assert analysis_hook.respond(_event(tmp_path / "notes.md"), run=tmp_path,
                                 agent="accounting-analyst", feedback=feedback) == (0, "")
    assert analysis_hook.respond(_event(tmp_path / "report_numbers.md"), run=tmp_path,
                                 agent="numbers-reader", feedback=feedback) == (0, "")
    assert asked == [] and not feedback.exists()


def test_a_file_the_gate_cannot_read_is_handed_back(tmp_path, monkeypatch):
    _gate(monkeypatch, ValueError("Expecting value: line 1 column 1 (char 0)"))
    code, text = analysis_hook.respond(
        _event(tmp_path / "analysis_accounting.json"), run=tmp_path,
        agent="accounting-analyst", feedback=tmp_path / "fb.jsonl")
    assert code == 2 and "Expecting value" in text


def test_the_hook_goes_quiet_after_its_last_message(tmp_path, monkeypatch):
    _gate(monkeypatch, DROPPED)
    feedback = tmp_path / "fb.jsonl"
    codes = [analysis_hook.respond(_event(tmp_path / "analysis_accounting.json"),
                                   run=tmp_path, agent="accounting-analyst",
                                   feedback=feedback)[0]
             for _ in range(analysis_hook.MAX_FEEDBACK + 2)]
    assert codes == [2] * analysis_hook.MAX_FEEDBACK + [0, 0]
    assert len(feedback.read_text().splitlines()) == analysis_hook.MAX_FEEDBACK


def test_the_gate_runs_on_a_real_file_with_a_quoted_figure(tmp_path):
    """The real gate, not a stub: an accounting analyst's file whose finding
    quotes a figure inline is handed back at that finding."""
    run = tmp_path / "run"
    directory = run / "agents" / "accounting-analyst"
    directory.mkdir(parents=True)
    (run / "input_manifest.json").write_text("{}")
    (directory / "calculator_filings_only.json").write_text("{}")
    (directory / "report_numbers.md").write_text("no items\n")
    (directory / "report_notes_text.md").write_text("no items\n")
    written = directory / "analysis_accounting.json"
    written.write_text(json.dumps({"areas": {"revenue_recognition": {
        "finding": 'the note says "the Company recognized $4.8 million"'}}}))
    code, text = analysis_hook.respond(_event(written), run=run, agent="accounting-analyst",
                                       feedback=tmp_path / "fb.jsonl")
    assert code == 2
    assert ("- areas.revenue_recognition: finding: a number written in the analyst's "
            "own words") in text


def test_the_command_hands_an_analyst_the_hook_and_a_reader_nothing(tmp_path):
    feedback = tmp_path / "accounting-analyst.gate_feedback.jsonl"
    settings = json.loads(run_analysis.gate_hook(tmp_path, "accounting-analyst", feedback))
    [entry] = settings["hooks"]["PostToolUse"]
    assert entry["matcher"] == "Write|Edit"
    command = entry["hooks"][0]["command"]
    assert "-m src.analysis_hook" in command and "--agent accounting-analyst" in command
    assert str(feedback.resolve()) in command
    assert run_analysis.gate_hook(tmp_path, "numbers-reader", feedback) is None


class _Done:
    returncode, stdout, stderr = 0, json.dumps({"usage": {}}), ""


def test_ask_passes_the_settings_before_the_message_and_none_without(tmp_path, monkeypatch):
    calls = []

    def run(command, cwd, capture_output, text, timeout):
        calls.append(command)
        (cwd / "out.json").write_text("{}")
        return _Done()
    monkeypatch.setattr(run_analysis.subprocess, "run", run)
    spec = {"model": "opus", "description": "d", "prompt": "p", "tools": ["Read"]}
    run_analysis.ask(tmp_path, agent="x", writes=("out.json",), message="m", spec=spec,
                     log=tmp_path / "x.log", settings='{"hooks": {}}')
    run_analysis.ask(tmp_path, agent="x", writes=("out.json",), message="m", spec=spec,
                     log=tmp_path / "x.log")
    assert calls[0][-3:] == ["--settings", '{"hooks": {}}', "m"]
    assert "--settings" not in calls[1] and calls[1][-1] == "m"
