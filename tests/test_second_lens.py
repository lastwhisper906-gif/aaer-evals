"""The second lens says pass, fail, needs judgment, or that it did not run.

The fourth of those is the one this file exists for. A lens that could not run
tells you nothing about the change, and the failure mode the design has to
survive is that it looks like the third: Codex exits with some status nobody
wrote down when the quota is out, prints a sentence, and a script that reads
the sentence reads "no findings" as "no problems". So the script judges *did a
verdict come back* by whether a file validates against
`tools/lens_verdict.schema.json`, and every test here shadows the two binaries
rather than calling them.

The three scenarios, and where their expected values come from:

* Codex cannot run, the fallback answers. Expected: the fallback file exists and
  the ledger line names `claude-fable-fallback`. The expected values are the
  stub's own output and the lens names written in `tools/second_lens.sh`.
* Codex answers `fail`. Expected: exit 1, the ledger names `codex`, and the
  fallback binary is never invoked -- asserted by the stub recording its own
  calls, because "the fallback did not run" is not visible in the verdict.
* Neither lens runs. Expected: exit 3, and no line in the ledger that reads as
  an approval. Exit 3 is never an approval, so the assertion is on the ledger's
  contents and not only on the status.

The exit codes are read from `src/lens_verdict.py`, which is where the script
takes them from as well; a test that wrote `1` for fail by hand would keep
passing if the script changed its mind.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from src import lens_verdict

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "tools" / "second_lens.sh"

PASS_VERDICT = {"lens": "codex", "verdict": "pass", "findings": [], "reads": 9}
FAIL_VERDICT = {
    "lens": "codex",
    "verdict": "fail",
    "findings": [
        {
            "rule": 1,
            "file": "tests/test_trends.py",
            "line": 44,
            "reason": "the expected ratio came from a run of src/trends.py",
        }
    ],
    "reads": 12,
}


def _write_stub(directory: Path, name: str, body: str) -> Path:
    stub = directory / name
    stub.write_text(f"#!/bin/sh\n{body}\n", encoding="utf-8")
    stub.chmod(0o755)
    return stub


def codex_stub(directory: Path, *, exit_code: int, verdict: dict | str | None) -> None:
    """A `codex` that records its call and writes what it was told to write."""
    if verdict is None:
        payload = ""
    elif isinstance(verdict, str):
        payload = verdict
    else:
        payload = json.dumps(verdict)
    _write_stub(
        directory,
        "codex",
        'echo codex >> "$STUB_CALLS"\n'
        'out=""\n'
        'while [ $# -gt 0 ]; do\n'
        '  case "$1" in\n'
        '    -o) out="$2"; shift 2 ;;\n'
        '    *) shift ;;\n'
        '  esac\n'
        'done\n'
        'cat > /dev/null\n'
        f'if [ -n "$out" ] && [ -n {json.dumps(payload)} ]; then\n'
        f'  printf %s {json.dumps(payload)} > "$out"\n'
        'fi\n'
        f'exit {exit_code}\n',
    )


def claude_stub(directory: Path, *, exit_code: int, result: str | None) -> None:
    """A `claude -p --output-format json` that prints one envelope."""
    if result is None:
        envelope = ""
    else:
        envelope = json.dumps(
            {"type": "result", "subtype": "success", "is_error": False, "result": result}
        )
    _write_stub(
        directory,
        "claude",
        'echo claude >> "$STUB_CALLS"\n'
        f'printf %s {json.dumps(envelope)}\n'
        f'exit {exit_code}\n',
    )


def run_lens(tmp_path: Path, item: str = "a task-list item") -> subprocess.CompletedProcess:
    stubs = tmp_path / "stubs"
    worktree = tmp_path / "worktree"
    worktree.mkdir(exist_ok=True)
    ledger = tmp_path / "ledger.jsonl"
    environment = dict(os.environ)
    environment["PATH"] = f"{stubs}:{environment['PATH']}"
    environment["STUB_CALLS"] = str(tmp_path / "calls")
    environment["LENS_LEDGER"] = str(ledger)
    environment["LENS_PYTHON"] = sys.executable
    environment["LENS_TIMEOUT"] = "60"
    return subprocess.run(
        ["bash", str(SCRIPT), str(worktree), item],
        capture_output=True,
        text=True,
        env=environment,
        cwd=tmp_path,
    )


def ledger_lines(tmp_path: Path) -> list[dict]:
    ledger = tmp_path / "ledger.jsonl"
    if not ledger.exists():
        return []
    return [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines() if line]


def calls(tmp_path: Path) -> list[str]:
    record = tmp_path / "calls"
    if not record.exists():
        return []
    return record.read_text(encoding="utf-8").split()


@pytest.fixture
def stubs(tmp_path: Path) -> Path:
    directory = tmp_path / "stubs"
    directory.mkdir()
    return directory


def test_codex_cannot_run_so_fable_answers(tmp_path: Path, stubs: Path) -> None:
    codex_stub(stubs, exit_code=1, verdict=None)
    claude_stub(stubs, exit_code=0, result=json.dumps({**PASS_VERDICT, "lens": "whatever"}))

    result = run_lens(tmp_path)

    assert (tmp_path / "worktree" / ".lens" / "fable.json").exists()
    assert result.returncode == lens_verdict.PASS, result.stderr
    (line,) = ledger_lines(tmp_path)
    assert line["lens"] == "claude-fable-fallback"
    assert line["verdict"] == "pass"
    assert "claude-fable-fallback" in result.stdout


def test_the_fallback_verdict_is_filed_under_the_lens_that_ran(
    tmp_path: Path, stubs: Path
) -> None:
    """The model's own `lens` key is not trusted: the script knows what it ran."""
    codex_stub(stubs, exit_code=1, verdict=None)
    claude_stub(stubs, exit_code=0, result=json.dumps({**PASS_VERDICT, "lens": "codex"}))

    run_lens(tmp_path)

    written = json.loads((tmp_path / "worktree" / ".lens" / "verdict.json").read_text())
    assert written["lens"] == "claude-fable-fallback"
    assert written["lens_as_written"] == "codex"


def test_codex_answering_fail_is_the_answer(tmp_path: Path, stubs: Path) -> None:
    codex_stub(stubs, exit_code=0, verdict=FAIL_VERDICT)
    claude_stub(stubs, exit_code=0, result=json.dumps(PASS_VERDICT))

    result = run_lens(tmp_path)

    assert result.returncode == lens_verdict.FAIL, result.stderr
    (line,) = ledger_lines(tmp_path)
    assert line["lens"] == "codex"
    assert line["verdict"] == "fail"
    assert line["findings_count"] == 1
    assert calls(tmp_path) == ["codex"], "the fallback ran behind a lens that answered"


def test_neither_lens_runs_and_that_is_never_an_approval(
    tmp_path: Path, stubs: Path
) -> None:
    codex_stub(stubs, exit_code=1, verdict=None)
    claude_stub(stubs, exit_code=1, result=None)

    result = run_lens(tmp_path)

    assert result.returncode == lens_verdict.NO_LENS_RAN, result.stderr
    lines = ledger_lines(tmp_path)
    assert [line["verdict"] for line in lines] == ["no_lens_ran"]
    assert not [line for line in lines if line["verdict"] == "pass"]
    assert lines[0]["lens"] == "none"


def test_a_lens_that_answers_something_that_is_not_a_verdict_did_not_run(
    tmp_path: Path, stubs: Path
) -> None:
    """Exit zero and a sentence is the quota failure this design is built for."""
    codex_stub(stubs, exit_code=0, verdict="You have reached your usage limit.")
    claude_stub(stubs, exit_code=0, result="I was unable to complete the review.")

    result = run_lens(tmp_path)

    assert result.returncode == lens_verdict.NO_LENS_RAN, result.stderr
    assert [line["verdict"] for line in ledger_lines(tmp_path)] == ["no_lens_ran"]


def test_a_verdict_outside_the_schema_did_not_run(tmp_path: Path, stubs: Path) -> None:
    codex_stub(stubs, exit_code=0, verdict={"lens": "codex", "verdict": "looks fine"})
    claude_stub(stubs, exit_code=1, result=None)

    result = run_lens(tmp_path)

    assert result.returncode == lens_verdict.NO_LENS_RAN, result.stderr


def test_missing_binaries_are_no_lens_rather_than_a_crash(tmp_path: Path, stubs: Path) -> None:
    """Neither binary on PATH at all -- the plainest way for no lens to run.

    The system directories stay on PATH because the script needs `sed`, `cat`
    and `mkdir`; what is taken off it is wherever `codex` and `claude` are
    installed, which on this machine is under the user's own bin directory.
    """
    ledger = tmp_path / "ledger.jsonl"
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    environment = dict(os.environ)
    environment["PATH"] = f"{stubs}:/usr/bin:/bin:/usr/sbin:/sbin"
    assert shutil.which("codex", path=environment["PATH"]) is None
    assert shutil.which("claude", path=environment["PATH"]) is None
    environment["STUB_CALLS"] = str(tmp_path / "calls")
    environment["LENS_LEDGER"] = str(ledger)
    environment["LENS_PYTHON"] = sys.executable
    result = subprocess.run(
        [shutil.which("bash"), str(SCRIPT), str(worktree), "an item"],
        capture_output=True,
        text=True,
        env=environment,
        cwd=tmp_path,
    )
    assert result.returncode == lens_verdict.NO_LENS_RAN, result.stderr


def test_both_lenses_are_handed_the_same_prompt(tmp_path: Path, stubs: Path) -> None:
    """The lens's own name is the only difference the composed prompts may carry."""
    codex_stub(stubs, exit_code=1, verdict=None)
    claude_stub(stubs, exit_code=0, result=json.dumps(PASS_VERDICT))

    run_lens(tmp_path)

    lens_dir = tmp_path / "worktree" / ".lens"
    codex_prompt = (lens_dir / "prompt.codex.md").read_text(encoding="utf-8")
    fable_prompt = (lens_dir / "prompt.claude-fable-fallback.md").read_text(encoding="utf-8")
    assert codex_prompt != fable_prompt
    assert codex_prompt.replace("`codex`", "X") == fable_prompt.replace(
        "`claude-fable-fallback`", "X"
    )
    rules = (REPO_ROOT / "tools" / "lens_prompt.md").read_text(encoding="utf-8")
    assert rules in codex_prompt
    assert rules in fable_prompt


def test_the_usage_line_is_not_an_approval(tmp_path: Path) -> None:
    result = subprocess.run(
        ["bash", str(SCRIPT)], capture_output=True, text=True, cwd=REPO_ROOT
    )
    assert result.returncode == lens_verdict.NO_LENS_RAN
    assert "usage" in result.stderr


def test_a_worktree_that_is_not_there_is_not_an_approval(tmp_path: Path) -> None:
    result = subprocess.run(
        ["bash", str(SCRIPT), str(tmp_path / "nowhere"), "an item"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    assert result.returncode == lens_verdict.NO_LENS_RAN


# --- the one prompt both lenses read ---------------------------------------


def test_the_five_rules_are_the_refute_agent_s_five_rules_verbatim() -> None:
    """One file, read by both lenses, so the three copies cannot drift.

    The expected value is `.claude/agents/refute-check.md` itself, which is the
    first lens's own prompt. If the rules are edited there and not here, the two
    lenses are running different reviews and calling the agreement a
    cross-vendor confirmation.
    """
    agent = (REPO_ROOT / ".claude" / "agents" / "refute-check.md").read_text(encoding="utf-8")
    prompt = (REPO_ROOT / "tools" / "lens_prompt.md").read_text(encoding="utf-8")
    start = "**1. Where does every expected value come from?**"
    end = "A supervisor directory holding a filing or the market table is `fail`."
    assert start in agent and end in agent
    rules = agent[agent.index(start) : agent.index(end) + len(end)]
    assert rules in prompt, "tools/lens_prompt.md has drifted from refute-check.md"
    for number in range(1, 6):
        assert f"**{number}." in rules


def test_the_schema_is_the_shape_the_prompt_asks_for() -> None:
    prompt = (REPO_ROOT / "tools" / "lens_prompt.md").read_text(encoding="utf-8")
    properties = lens_verdict.schema()["properties"]
    assert set(properties) == {"lens", "verdict", "findings", "reads"}
    for key in properties:
        assert f"`{key}`" in prompt
    assert set(properties["verdict"]["enum"]) == set(lens_verdict.EXIT_FOR_VERDICT)


# --- reading one lens's answer ---------------------------------------------


def test_a_fenced_answer_is_read_on_the_claude_side(tmp_path: Path) -> None:
    envelope = tmp_path / "fable.json"
    envelope.write_text(
        json.dumps(
            {
                "result": "```json\n" + json.dumps(PASS_VERDICT) + "\n```",
                "is_error": False,
            }
        ),
        encoding="utf-8",
    )
    assert lens_verdict.read_claude(envelope)["verdict"] == "pass"


def test_a_fence_is_not_read_on_the_codex_side(tmp_path: Path) -> None:
    written = tmp_path / "codex.json"
    written.write_text("```json\n" + json.dumps(PASS_VERDICT) + "\n```", encoding="utf-8")
    with pytest.raises(lens_verdict.NotAVerdict):
        lens_verdict.read_codex(written)


def test_an_errored_envelope_is_not_a_verdict(tmp_path: Path) -> None:
    envelope = tmp_path / "fable.json"
    envelope.write_text(
        json.dumps({"result": "quota exceeded", "is_error": True}), encoding="utf-8"
    )
    with pytest.raises(lens_verdict.NotAVerdict):
        lens_verdict.read_claude(envelope)


def test_an_empty_file_is_not_a_verdict(tmp_path: Path) -> None:
    empty = tmp_path / "codex.json"
    empty.write_text("", encoding="utf-8")
    with pytest.raises(lens_verdict.NotAVerdict):
        lens_verdict.read_codex(empty)


def test_a_file_that_was_never_written_is_not_a_verdict(tmp_path: Path) -> None:
    with pytest.raises(lens_verdict.NotAVerdict):
        lens_verdict.read_codex(tmp_path / "nothing.json")


def test_the_ledger_grows_by_one_line_and_moves_nothing(tmp_path: Path) -> None:
    ledger = tmp_path / "ledger.jsonl"
    ledger.write_text('{"already": "here"}\n', encoding="utf-8")
    before = ledger.read_text(encoding="utf-8")
    lens_verdict.append_ledger(ledger, lens_verdict.ledger_line("an item", "codex", "pass", 0, "now"))
    after = ledger.read_text(encoding="utf-8")
    assert after.startswith(before)
    assert len(after.splitlines()) == 2


def test_a_ledger_with_no_trailing_newline_still_gets_its_own_line(tmp_path: Path) -> None:
    ledger = tmp_path / "ledger.jsonl"
    ledger.write_text('{"already": "here"}', encoding="utf-8")
    lens_verdict.append_ledger(ledger, lens_verdict.ledger_line("an item", "codex", "pass", 0, "now"))
    lines = ledger.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0]) == {"already": "here"}


def test_the_exit_codes_are_the_ones_the_script_uses() -> None:
    """The script writes them once; nothing here may write a second copy."""
    script = SCRIPT.read_text(encoding="utf-8")
    assert f"NO_LENS_RAN={lens_verdict.NO_LENS_RAN}" in script
    assert lens_verdict.EXIT_FOR_VERDICT == {"pass": 0, "fail": 1, "needs_judgment": 2}


@pytest.mark.skipif(shutil.which("bash") is None, reason="no bash on this machine")
def test_the_script_is_executable() -> None:
    assert os.access(SCRIPT, os.X_OK)
