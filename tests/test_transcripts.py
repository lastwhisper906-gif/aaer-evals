"""Every agent session's whole transcript on disk (`docs/improve_loop.md`, the
first change the loop needs). Expected values are the CLI's documented
`stream-json` shape -- one JSON event per line, the last of type `result`
carrying what `--output-format json` printed whole -- and the rule stated in
`run_analysis.ask`: the transcript goes beside the stderr log, one file per
attempt, and a nested session is started without the two variables that mark a
process as already inside a session.
"""

from __future__ import annotations

import json
import os

from src import run_analysis

RESULT = {"type": "result", "is_error": False, "num_turns": 3, "total_cost_usd": 0.5,
          "usage": {"input_tokens": 7, "output_tokens": 2},
          "modelUsage": {"claude-opus-5-5": {"outputTokens": 2}}}
STREAM = "\n".join(json.dumps(e) for e in (
    {"type": "system", "subtype": "init"}, {"type": "assistant", "message": {}}, RESULT)) + "\n"


def test_the_result_is_the_last_result_event_of_the_stream():
    assert run_analysis.result_of(STREAM) == RESULT
    # two results: the last one is the session's
    two = STREAM + json.dumps(dict(RESULT, num_turns=4)) + "\n"
    assert run_analysis.result_of(two)["num_turns"] == 4


def test_one_json_object_is_still_read_whole_and_anything_else_is_an_error():
    assert run_analysis.result_of(json.dumps({"usage": {}, "is_error": False})) == {
        "usage": {}, "is_error": False}
    broken = run_analysis.result_of("Not logged in\n")
    assert broken["is_error"] is True and "Not logged in" in broken["result"]
    assert run_analysis.result_of("")["is_error"] is True


def test_the_transcript_is_written_beside_the_log_one_file_per_attempt(tmp_path, monkeypatch):
    seen = {}

    class Done:
        returncode, stdout, stderr = 0, STREAM, "stderr tail"

    def run(command, cwd, capture_output, text, timeout, env=None):
        seen["env"] = env
        (cwd / "out.json").write_text("{}")
        return Done()
    monkeypatch.setattr(run_analysis.subprocess, "run", run)
    monkeypatch.setenv("CLAUDECODE", "1")
    monkeypatch.setenv("CLAUDE_CODE_ENTRYPOINT", "cli")
    monkeypatch.setenv("HOME", str(tmp_path))
    log = tmp_path / "accounting-analyst.log"
    record = run_analysis.ask(tmp_path, agent="x", writes=("out.json",), message="m",
                              spec={"model": "opus", "description": "d", "prompt": "p",
                                    "tools": ["Read"]}, log=log)
    assert record["result"] == "written" and record["output_tokens"] == 2
    assert log.read_text() == "stderr tail"
    transcript = tmp_path / "accounting-analyst.1.transcript.jsonl"
    assert transcript.read_text() == STREAM
    assert run_analysis.transcript_path(log, 2).name == "accounting-analyst.2.transcript.jsonl"
    # the nested session is not told it is inside one
    assert "CLAUDECODE" not in seen["env"] and "CLAUDE_CODE_ENTRYPOINT" not in seen["env"]
    assert seen["env"]["HOME"] == str(tmp_path)
    assert os.environ["CLAUDECODE"] == "1"          # this process's own is untouched


def test_the_command_asks_for_the_stream(tmp_path, monkeypatch):
    calls = []

    class Done:
        returncode, stdout, stderr = 0, STREAM, ""

    def run(command, cwd, capture_output, text, timeout, env=None):
        calls.append(command)
        (cwd / "out.json").write_text("{}")
        return Done()
    monkeypatch.setattr(run_analysis.subprocess, "run", run)
    run_analysis.ask(tmp_path, agent="x", writes=("out.json",), message="m",
                     spec={"model": "opus", "description": "d", "prompt": "p", "tools": ["Read"]},
                     log=tmp_path / "x.log")
    [command] = calls
    assert command[command.index("--output-format") + 1] == "stream-json"
    assert "--verbose" in command and command[-1] == "m"
