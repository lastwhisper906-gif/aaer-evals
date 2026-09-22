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
import shlex
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


def claude_stub(directory: Path, *, exit_code: int, result: str | None,
                model_usage: dict | None = None) -> None:
    """A `claude -p --output-format json` that prints one envelope."""
    if result is None:
        envelope = ""
    else:
        body = {"type": "result", "subtype": "success", "is_error": False, "result": result}
        if model_usage is not None:
            body["modelUsage"] = model_usage
        envelope = json.dumps(body)
    _write_stub(
        directory,
        "claude",
        'echo claude >> "$STUB_CALLS"\n'
        'pwd >> "$STUB_CWD"\n'
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
    environment["STUB_CWD"] = str(tmp_path / "cwd")
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
    environment["STUB_CWD"] = str(tmp_path / "cwd")
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
    """One copy of the mapping, and the script reads it rather than repeating it.

    `NO_LENS_RAN` is the one number the script has to know before any Python
    runs -- a usage error answers with it -- so it is written in both places and
    pinned equal here. The other three are printed by the module as the third
    field of its reading and are not in the script at all.
    """
    # Written out literally. Every scenario above compares against
    # `lens_verdict.NO_LENS_RAN`, so if both copies of it became 0 the whole
    # file would still pass while no-lens-ran had become an approval and the
    # table in SKILL.md had become false. This one line is what stops that.
    assert lens_verdict.NO_LENS_RAN == 3
    assert lens_verdict.NO_LENS_RAN not in lens_verdict.EXIT_FOR_VERDICT.values()
    script = SCRIPT.read_text(encoding="utf-8")
    assert "NO_LENS_RAN=3" in script
    assert lens_verdict.EXIT_FOR_VERDICT == {"pass": 0, "fail": 1, "needs_judgment": 2}
    for verdict, code in lens_verdict.EXIT_FOR_VERDICT.items():
        assert f"{verdict})" not in script or f"CODE={code}" not in script, (
            f"the script carries its own exit code for {verdict}"
        )


@pytest.mark.skipif(shutil.which("bash") is None, reason="no bash on this machine")
def test_the_script_is_executable() -> None:
    assert os.access(SCRIPT, os.X_OK)


# --- what a pass has to be before it is one --------------------------------
#
# These five are the second lens's own findings on this change, turned into
# judges. Each one was reachable before it was written: a pass that opened no
# files exited 0, a pass listing findings exited 0, the fallback reviewed
# whatever directory the caller happened to be in, and a ledger line that was
# never written took a pull request through to auto-merge with no row for the
# weekly routine to find.


def test_a_pass_that_opened_no_files_did_not_run(tmp_path: Path, stubs: Path) -> None:
    """`tools/lens_prompt.md` says so; until this, nothing but the model did."""
    codex_stub(stubs, exit_code=0, verdict={**PASS_VERDICT, "reads": 0})
    claude_stub(stubs, exit_code=1, result=None)

    result = run_lens(tmp_path)

    assert result.returncode == lens_verdict.NO_LENS_RAN, result.stderr
    assert [line["verdict"] for line in ledger_lines(tmp_path)] == ["no_lens_ran"]


def test_a_pass_carrying_findings_is_not_a_verdict(tmp_path: Path, stubs: Path) -> None:
    """Whichever half is true, the half that must not win is the one exiting 0."""
    contradiction = {**PASS_VERDICT, "findings": FAIL_VERDICT["findings"]}
    codex_stub(stubs, exit_code=0, verdict=contradiction)
    claude_stub(stubs, exit_code=1, result=None)

    result = run_lens(tmp_path)

    assert result.returncode == lens_verdict.NO_LENS_RAN, result.stderr


def test_a_fail_with_no_findings_still_blocks(tmp_path: Path, stubs: Path) -> None:
    """A poor verdict, and still not an approval -- so it is left as a fail."""
    codex_stub(stubs, exit_code=0, verdict={**FAIL_VERDICT, "findings": []})
    claude_stub(stubs, exit_code=1, result=None)

    result = run_lens(tmp_path)

    assert result.returncode == lens_verdict.FAIL, result.stderr


def test_needs_judgment_exits_two_and_is_not_a_merge(tmp_path: Path, stubs: Path) -> None:
    codex_stub(
        stubs,
        exit_code=0,
        verdict={
            "lens": "codex",
            "verdict": "needs_judgment",
            "findings": [
                {
                    "rule": 2,
                    "file": "src/market.py",
                    "line": 1,
                    "reason": "nothing judges the acceptance-time argument",
                }
            ],
            "reads": 4,
        },
    )
    claude_stub(stubs, exit_code=0, result=json.dumps(PASS_VERDICT))

    result = run_lens(tmp_path)

    assert result.returncode == lens_verdict.NEEDS_JUDGMENT, result.stderr
    (line,) = ledger_lines(tmp_path)
    assert line["verdict"] == "needs_judgment"
    assert calls(tmp_path) == ["codex"]


def test_the_fallback_is_started_in_the_tree_it_judges(tmp_path: Path, stubs: Path) -> None:
    """Codex gets -C; the fallback got whatever directory the caller was in.

    `docs/routines/weekly-relens.md` runs this script from the repository root
    against a detached worktree, so an unbound fallback reviews main and answers
    about a tree the item never produced.
    """
    codex_stub(stubs, exit_code=1, verdict=None)
    claude_stub(stubs, exit_code=0, result=json.dumps(PASS_VERDICT))

    run_lens(tmp_path)

    where = (tmp_path / "cwd").read_text(encoding="utf-8").split()
    assert where == [str((tmp_path / "worktree").resolve())]


def test_a_ledger_line_that_could_not_be_written_is_not_an_approval(
    tmp_path: Path, stubs: Path
) -> None:
    """The row the weekly routine greps for. No row, no re-lens, ever."""
    codex_stub(stubs, exit_code=0, verdict=PASS_VERDICT)
    claude_stub(stubs, exit_code=1, result=None)

    stubs_dir = tmp_path / "stubs"
    worktree = tmp_path / "worktree"
    worktree.mkdir(exist_ok=True)
    # A ledger whose parent is a regular file: the append cannot make the
    # directory and cannot write the line.
    blocked = tmp_path / "not-a-directory"
    blocked.write_text("", encoding="utf-8")
    environment = dict(os.environ)
    environment["PATH"] = f"{stubs_dir}:{environment['PATH']}"
    environment["STUB_CALLS"] = str(tmp_path / "calls")
    environment["STUB_CWD"] = str(tmp_path / "cwd")
    environment["LENS_LEDGER"] = str(blocked / "ledger.jsonl")
    environment["LENS_PYTHON"] = sys.executable
    result = subprocess.run(
        ["bash", str(SCRIPT), str(worktree), "an item"],
        capture_output=True,
        text=True,
        env=environment,
        cwd=tmp_path,
    )

    assert result.returncode == lens_verdict.NO_LENS_RAN, result.stdout + result.stderr
    assert "not an approval" in result.stdout


def test_the_reading_carries_the_exit_code_the_script_answers_with(
    tmp_path: Path,
) -> None:
    """Four fields: verdict, findings, exit code, model. The last two are fixes."""
    written = tmp_path / "codex.json"
    written.write_text(json.dumps(FAIL_VERDICT), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-m", "src.lens_verdict", "codex", str(written), "--lens", "codex"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env={**os.environ, "PYTHONPATH": str(REPO_ROOT)},
    )
    assert result.returncode == 0
    assert result.stdout.split() == [
        "fail",
        "1",
        str(lens_verdict.FAIL),
        lens_verdict.UNRECORDED_MODEL,
    ]


def test_a_pass_with_no_reads_is_refused_at_the_module_too(tmp_path: Path) -> None:
    written = tmp_path / "codex.json"
    written.write_text(json.dumps({**PASS_VERDICT, "reads": 0}), encoding="utf-8")
    with pytest.raises(lens_verdict.NotAVerdict, match="did not look"):
        lens_verdict.read_codex(written)


def test_a_pass_carrying_findings_is_refused_at_the_module_too(tmp_path: Path) -> None:
    written = tmp_path / "codex.json"
    written.write_text(
        json.dumps({**PASS_VERDICT, "findings": FAIL_VERDICT["findings"]}), encoding="utf-8"
    )
    with pytest.raises(lens_verdict.NotAVerdict, match="contradiction"):
        lens_verdict.read_codex(written)


def test_a_verdict_written_before_a_non_zero_exit_is_still_the_answer(
    tmp_path: Path, stubs: Path
) -> None:
    """A timeout killed after the file was flushed is not a lens that did not run.

    The cross-vendor lens writing a complete `fail` and then exiting non-zero,
    with the same-family fallback overwriting it with a `pass`, is the one path
    the design says cannot happen. It could, until the file was read whatever
    the exit status was.
    """
    codex_stub(stubs, exit_code=124, verdict=FAIL_VERDICT)  # 124: killed by timeout
    claude_stub(stubs, exit_code=0, result=json.dumps(PASS_VERDICT))

    result = run_lens(tmp_path)

    assert result.returncode == lens_verdict.FAIL, result.stderr
    (line,) = ledger_lines(tmp_path)
    assert line["lens"] == "codex"
    assert calls(tmp_path) == ["codex"], "the fallback overwrote a cross-vendor fail"


def test_the_ledger_records_the_model_and_not_only_the_lens_name(
    tmp_path: Path, stubs: Path
) -> None:
    """`LENS_FALLBACK_MODEL` can put another model behind the same lens name."""
    codex_stub(stubs, exit_code=1, verdict=None)
    stub = tmp_path / "stubs" / "claude"
    envelope = json.dumps(
        {
            "result": json.dumps(PASS_VERDICT),
            "is_error": False,
            "modelUsage": {"claude-fable-5-1": {"inputTokens": 2}},
        }
    )
    stub.write_text(
        "#!/bin/sh\n"
        'echo claude >> "$STUB_CALLS"\n'
        'pwd >> "$STUB_CWD"\n'
        f"printf %s {json.dumps(envelope)}\n"
        "exit 0\n",
        encoding="utf-8",
    )
    stub.chmod(0o755)

    result = run_lens(tmp_path)

    (line,) = ledger_lines(tmp_path)
    assert line["lens"] == "claude-fable-fallback"
    assert line["model"] == "claude-fable-5-1"
    assert "claude-fable-5-1" in result.stdout


def test_a_model_the_answer_does_not_name_is_recorded_as_unrecorded(
    tmp_path: Path, stubs: Path
) -> None:
    """Unrecorded is a fact about the record. It is never a guess at the model."""
    codex_stub(stubs, exit_code=1, verdict=None)
    claude_stub(stubs, exit_code=0, result=json.dumps(PASS_VERDICT))

    run_lens(tmp_path)

    (line,) = ledger_lines(tmp_path)
    assert line["model"] == lens_verdict.UNRECORDED_MODEL


def test_the_served_model_is_read_out_of_the_usage_record() -> None:
    assert lens_verdict.served_model(
        {"modelUsage": {"claude-fable-5-1": {"inputTokens": 2}}}
    ) == "claude-fable-5-1"
    assert lens_verdict.served_model({}) == lens_verdict.UNRECORDED_MODEL
    assert lens_verdict.served_model("not an object") == lens_verdict.UNRECORDED_MODEL


def test_no_lens_ran_records_no_model_rather_than_the_last_one_tried(
    tmp_path: Path, stubs: Path
) -> None:
    codex_stub(stubs, exit_code=1, verdict=None)
    claude_stub(stubs, exit_code=1, result=None)

    run_lens(tmp_path)

    (line,) = ledger_lines(tmp_path)
    assert (line["lens"], line["model"], line["verdict"]) == ("none", "none", "no_lens_ran")


# --- the model is the rest of the line, not the fourth word -----------------


def test_two_models_that_served_one_answer_are_both_recorded(
    tmp_path: Path, stubs: Path
) -> None:
    """A `claude -p` session routinely serves a small model beside the big one.

    The ledger row is what `docs/routines/weekly-relens.md` reads to decide what
    to look at again, and a row naming half the models that answered is a row
    that names the wrong thing. The reading used to split on whitespace and keep
    the fourth word, so this line came back as `claude-fable-5-1,` -- trailing
    comma, second model gone.
    """
    codex_stub(stubs, exit_code=127, verdict=None)
    claude_stub(
        stubs,
        exit_code=0,
        result=json.dumps({"lens": "fable", "verdict": "pass", "findings": [], "reads": 4}),
        model_usage={"claude-fable-5-1": {"inputTokens": 2},
                     "claude-haiku-4-5-20251001": {"inputTokens": 1}},
    )
    result = run_lens(tmp_path)

    assert result.returncode == 0
    recorded = ledger_lines(tmp_path)[-1]["model"]
    assert recorded == "claude-fable-5-1, claude-haiku-4-5-20251001"
    assert recorded in result.stdout


def test_a_model_name_with_a_space_survives_the_reading(
    tmp_path: Path, stubs: Path
) -> None:
    """Nothing forbids a provider a space in a name, and the split assumed none."""
    codex_stub(stubs, exit_code=127, verdict=None)
    claude_stub(
        stubs,
        exit_code=0,
        result=json.dumps({"lens": "fable", "verdict": "pass", "findings": [], "reads": 4}),
        model_usage={"a model with spaces": {"inputTokens": 2}},
    )
    result = run_lens(tmp_path)

    assert result.returncode == 0
    assert ledger_lines(tmp_path)[-1]["model"] == "a model with spaces"


def test_a_reading_with_no_model_at_all_is_not_a_crash(
    tmp_path: Path, stubs: Path
) -> None:
    """Three fields where four were expected killed the script under `set -u`.

    `$4: unbound variable` exits 1, which the build skill's table reads as
    *fail* -- a verdict -- with no ledger line and nothing printed. The reading
    has to degrade to `unrecorded`, which is what the ledger already says when
    nobody named a model.
    """
    codex_stub(stubs, exit_code=127, verdict=None)
    claude_stub(stubs, exit_code=0, result=json.dumps(
        {"lens": "fable", "verdict": "pass", "findings": [], "reads": 4}))

    # A stand-in for the module that prints the three fields it printed before
    # the model was added to the line, and otherwise defers to the real one.
    older = _write_stub(
        stubs,
        "older_lens_verdict",
        f'if [ "$3" = "ledger" ]; then exec {shlex.quote(sys.executable)} "$@"; fi\n'
        f'{shlex.quote(sys.executable)} "$@" | cut -d" " -f1-3\n',
    )
    environment = dict(os.environ)
    environment["PATH"] = f"{stubs}:{environment['PATH']}"
    environment["STUB_CALLS"] = str(tmp_path / "calls")
    environment["STUB_CWD"] = str(tmp_path / "cwd")
    environment["LENS_LEDGER"] = str(tmp_path / "ledger.jsonl")
    environment["LENS_PYTHON"] = str(older)
    environment["LENS_TIMEOUT"] = "60"
    worktree = tmp_path / "worktree"
    worktree.mkdir(exist_ok=True)
    result = subprocess.run(
        ["bash", str(SCRIPT), str(worktree), "a task-list item"],
        capture_output=True, text=True, env=environment, cwd=tmp_path)

    assert result.returncode == 0
    assert "unbound variable" not in result.stderr
    assert ledger_lines(tmp_path)[-1]["model"] == "unrecorded"


# --- an answer from an earlier run is not this run's -------------------------


def test_an_answer_left_from_an_earlier_run_is_not_read_as_this_one(
    tmp_path: Path, stubs: Path
) -> None:
    """The file's presence is the whole test of whether a lens answered.

    Since a verdict is read whatever the exit status was, a `codex.json` that
    could not be removed is indistinguishable from one this run wrote -- and
    `rm -f` says nothing when the directory refuses it. The first run passes,
    the second run's lens writes nothing, and without the check the second run
    reports the first run's pass.
    """
    codex_stub(stubs, exit_code=0, verdict={
        "lens": "codex", "verdict": "pass", "findings": [], "reads": 9})
    claude_stub(stubs, exit_code=127, result=None)
    first = run_lens(tmp_path)
    assert first.returncode == 0

    lens_dir = tmp_path / "worktree" / ".lens"
    codex_stub(stubs, exit_code=1, verdict=None)
    before = lens_dir.stat().st_mode
    lens_dir.chmod(0o500)
    try:
        second = run_lens(tmp_path)
    finally:
        lens_dir.chmod(before)

    assert second.returncode == 3, second.stdout
    assert ledger_lines(tmp_path)[-1]["lens"] == "none"


# --- a pass that opened no files --------------------------------------------


def test_a_pass_claiming_fewer_than_one_read_did_not_look(tmp_path: Path) -> None:
    """`reads` carries no lower bound in the schema, so the check needs one.

    Strict structured-output providers drop `minimum`, which is why the schema
    does not carry it; a check written as `== 0` then let `-1` through, and the
    rule the prompt states is "a lens that opened no files did not look".
    """
    for claimed in (0, -1, -100):
        with pytest.raises(lens_verdict.NotAVerdict, match="did not look"):
            lens_verdict.validate(
                {"lens": "codex", "verdict": "pass", "findings": [], "reads": claimed})


# --- the tree under review may not define its own judge ----------------------


def _repository_that(tmp_path: Path, *, edits: str | None) -> Path:
    """A worktree on `main` plus one commit, optionally touching a judge's file."""
    worktree = tmp_path / "worktree"
    worktree.mkdir(exist_ok=True)
    run = lambda *argv: subprocess.run(argv, cwd=worktree, check=True,
                                       capture_output=True, text=True)
    run("git", "init", "-q", "-b", "main")
    run("git", "config", "user.email", "lens@example.invalid")
    run("git", "config", "user.name", "lens")
    (worktree / ".claude" / "agents").mkdir(parents=True)
    (worktree / ".claude" / "agents" / "refute-check.md").write_text(
        "the five rules\n", encoding="utf-8")
    (worktree / "CLAUDE.md").write_text("the project rules\n", encoding="utf-8")
    (worktree / "a_file.py").write_text("x = 1\n", encoding="utf-8")
    run("git", "add", "-A")
    run("git", "commit", "-qm", "main")
    if edits is not None:
        # On a branch, the way an item is: the comparison is against `main`,
        # and a change committed onto `main` itself is not a change under review.
        run("git", "checkout", "-q", "-b", "item/under-review")
        (worktree / edits).write_text("moved\n", encoding="utf-8")
        run("git", "add", "-A")
        run("git", "commit", "-qm", "the change under review")
    return worktree


def test_a_change_that_edits_what_defines_its_judge_gets_no_lens(
    tmp_path: Path, stubs: Path
) -> None:
    """Both lenses read their own definition out of the tree they are judging.

    Codex takes `AGENTS.md`, the fallback takes `.claude/agents/refute-check.md`
    and the hooks in `.claude/settings.json`, and both take `CLAUDE.md`. A
    branch that moves one of those is graded by its own edit, which says nothing
    about the change -- so it lands where everything else that says nothing
    lands: exit 3, the `one-lens` label, and a person.
    """
    _repository_that(tmp_path, edits=".claude/agents/refute-check.md")
    codex_stub(stubs, exit_code=0, verdict={
        "lens": "codex", "verdict": "pass", "findings": [], "reads": 9})
    claude_stub(stubs, exit_code=0, result=json.dumps(
        {"lens": "fable", "verdict": "pass", "findings": [], "reads": 9}))
    result = run_lens(tmp_path)

    assert result.returncode == 3, result.stdout
    assert "changes what defines its judge" in result.stdout
    assert calls(tmp_path) == [], "a lens ran on a tree that had already disqualified it"
    assert ledger_lines(tmp_path)[-1]["lens"] == "none"


def test_a_change_that_leaves_its_judge_alone_is_judged_normally(
    tmp_path: Path, stubs: Path
) -> None:
    """The guard has to let ordinary work through, or it is just an off switch."""
    _repository_that(tmp_path, edits="a_file.py")
    codex_stub(stubs, exit_code=0, verdict={
        "lens": "codex", "verdict": "pass", "findings": [], "reads": 9})
    claude_stub(stubs, exit_code=127, result=None)
    result = run_lens(tmp_path)

    assert result.returncode == 0, result.stdout
    assert calls(tmp_path) == ["codex"]
