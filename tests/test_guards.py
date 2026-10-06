"""Every guard, two-sided: one case where it must fire and one where it must not.

A guard that has only ever been shown to pass is not known to work, and one that has
only ever been shown to fire is not known to let ordinary work through.
"""

from __future__ import annotations

import datetime as dt
import importlib.util
import json
import subprocess
from pathlib import Path

import pytest

from src import append_check, cutoff_guard, eval_guard, quote_gate

REPO = Path(__file__).resolve().parent.parent


# --- the PreToolUse hook on Bash ------------------------------------------------------------

def _hook():
    spec = importlib.util.spec_from_file_location(
        "guard_evals", REPO / ".claude" / "hooks" / "guard_evals.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("command", [
    "echo x > evals/thresholds.json",
    "printf '{}' >> evals/scoreboard.jsonl",
    "cat new.yaml | tee evals/golden/cases/a.yaml",
    "sed -i 's/0.6/0.1/' evals/thresholds.json",
    "mv draft.yaml evals/golden/cases/",
    "cp patched.py ./evals/regression/mechanical.py",
    "rm -rf evals/capability",
    "git checkout old -- evals/regression/coverage.py",
    "git restore evals/",
    "cd evals && echo x > thresholds.json",
])
def test_the_bash_hook_refuses_a_command_writing_under_evals(command):
    assert _hook().refused(command)


@pytest.mark.parametrize("command", [
    "make eval",
    "make eval-quick",
    ".venv/bin/python -m evals --runs runs/NVDA",
    "cat evals/README.md",
    "grep -rn dealbreaker evals/capability/rubric.md",
    "ls evals/golden/drafts",
    "echo x > notes_on_evals.txt",
    "git diff origin/main -- evals/",
])
def test_the_bash_hook_lets_reading_and_grading_through(command):
    assert _hook().refused(command) is None


def test_the_bash_hook_blocks_with_exit_two(tmp_path):
    payload = json.dumps({"tool_input": {"command": "rm evals/thresholds.json"}})
    done = subprocess.run(["python3", str(REPO / ".claude" / "hooks" / "guard_evals.py")],
                          input=payload, capture_output=True, text=True)
    assert done.returncode == 2 and "owner" in done.stderr
    allowed = subprocess.run(["python3", str(REPO / ".claude" / "hooks" / "guard_evals.py")],
                             input=json.dumps({"tool_input": {"command": "make eval"}}),
                             capture_output=True, text=True)
    assert allowed.returncode == 0


# --- the CI guard ---------------------------------------------------------------------------

def test_the_ci_guard_fails_an_unlabelled_change_to_a_grader():
    ok, why = eval_guard.decide([("M", "evals/regression/mechanical.py")], set(), True, "", "")
    assert not ok and "owner-approved-eval" in why


def test_the_ci_guard_fails_a_rewritten_scoreboard():
    ok, _ = eval_guard.decide([("M", eval_guard.SCOREBOARD)], set(), True,
                              '{"a": 1}\n', '{"a": 2}\n')
    assert not ok


def test_the_ci_guard_passes_the_owners_label():
    ok, _ = eval_guard.decide([("M", "evals/thresholds.json")], {"owner-approved-eval"},
                              True, "", "")
    assert ok


def test_the_ci_guard_passes_a_scoreboard_append_and_an_untouched_evals():
    ok, _ = eval_guard.decide([("M", eval_guard.SCOREBOARD)], set(), True,
                              '{"a": 1}\n', '{"a": 1}\n{"a": 2}\n')
    assert ok
    assert eval_guard.decide([], set(), True, None, None)[0]


def test_the_ci_guard_passes_the_pull_request_that_creates_evals():
    ok, why = eval_guard.decide([("A", "evals/README.md")], set(), False, None, None)
    assert ok and "creates" in why


# --- the append check on the scoreboard ------------------------------------------------------

def _repo(tmp_path, monkeypatch, first: str, second: str) -> list[str]:
    monkeypatch.chdir(tmp_path)
    run = lambda *a: subprocess.run(["git", *a], check=True, capture_output=True)  # noqa: E731
    run("init", "-q", "-b", "main")
    run("config", "user.email", "t@t")
    run("config", "user.name", "t")
    (tmp_path / "evals").mkdir()
    (tmp_path / "evals" / "scoreboard.jsonl").write_text(first)
    run("add", ".")
    run("commit", "-q", "-m", "one")
    run("branch", "base")
    (tmp_path / "evals" / "scoreboard.jsonl").write_text(second)
    run("commit", "-q", "-am", "two")
    return append_check.violations("base", "HEAD")


def test_the_append_check_refuses_a_rewritten_scoreboard(tmp_path, monkeypatch):
    assert _repo(tmp_path, monkeypatch, '{"a": 1}\n', '{"a": 9}\n') == \
        ["modified: evals/scoreboard.jsonl"]


def test_the_append_check_lets_the_scoreboard_grow(tmp_path, monkeypatch):
    assert _repo(tmp_path, monkeypatch, '{"a": 1}\n', '{"a": 1}\n{"a": 2}\n') == []


# --- the quote gate ---------------------------------------------------------------------------

INDEX = {"0000000000-26-000001:notes:1": "Revenue rose 10 percent in the quarter."}


def test_the_quote_gate_drops_a_quote_that_is_not_in_the_input():
    item = {"id": "revenue_recognition_rise", "paragraph_id": "0000000000-26-000001:notes:1",
            "quote": "Revenue rose 12 percent"}
    assert "does not string-match" in quote_gate.quote_drop_reason(item, INDEX)


def test_the_quote_gate_keeps_a_quote_that_is_there_whitespace_folded():
    item = {"id": "revenue_recognition_rise", "paragraph_id": "0000000000-26-000001:notes:1",
            "quote": "Revenue rose 10 percent"}
    assert quote_gate.quote_drop_reason(item, INDEX) is None


# --- the cutoff guard -------------------------------------------------------------------------

AAPL_10K = cutoff_guard.FIXTURES / "AAPL" / "10-K" / "aapl-20250927.htm"
AAPL_10K_FILED = dt.date(2025, 10, 31)      # the filing's date, stated, not read back


def test_the_cutoff_guard_refuses_a_document_filed_after_the_cutoff():
    with pytest.raises(cutoff_guard.CutoffViolationError):
        cutoff_guard.check(AAPL_10K, AAPL_10K_FILED - dt.timedelta(days=1))


def test_the_cutoff_guard_admits_a_document_filed_on_the_cutoff():
    assert cutoff_guard.check(AAPL_10K, AAPL_10K_FILED)["filing_date"] == "2025-10-31"


# --- the CI guard's git plumbing ---------------------------------------------------------------

def _git_repo(tmp_path, monkeypatch, *, main_has_evals: bool, branch_forked_before: bool):
    """main, and a branch that changes evals/thresholds.json; the branch is forked
    either before or after evals/ reached main."""
    monkeypatch.chdir(tmp_path)
    run = lambda *a: subprocess.run(["git", *a], check=True, capture_output=True)  # noqa: E731
    run("init", "-q", "-b", "main")
    run("config", "user.email", "t@t")
    run("config", "user.name", "t")
    (tmp_path / "README").write_text("x\n")
    run("add", ".")
    run("commit", "-q", "-m", "start")
    if branch_forked_before:
        run("branch", "work")
    if main_has_evals:
        (tmp_path / "evals").mkdir()
        (tmp_path / "evals" / "thresholds.json").write_text("{}\n")
        run("add", ".")
        run("commit", "-q", "-m", "evals")
    if not branch_forked_before:
        run("branch", "work")
    run("checkout", "-q", "work")
    (tmp_path / "evals").mkdir(exist_ok=True)
    (tmp_path / "evals" / "thresholds.json").write_text('{"capability": {"golden": 0.0}}\n')
    run("add", ".")
    run("commit", "-q", "-m", "lower the floor")


def test_the_ci_guard_refuses_a_branch_forked_before_evals_reached_main(tmp_path, monkeypatch):
    _git_repo(tmp_path, monkeypatch, main_has_evals=True, branch_forked_before=True)
    assert eval_guard.main(["--base", "main", "--head", "work", "--labels", ""]) == 1


def test_the_ci_guard_lets_the_creating_branch_through_when_main_has_no_evals(tmp_path, monkeypatch):
    _git_repo(tmp_path, monkeypatch, main_has_evals=False, branch_forked_before=False)
    assert eval_guard.main(["--base", "main", "--head", "work", "--labels", ""]) == 0


def test_the_ci_guard_guards_itself(tmp_path, monkeypatch):
    ok, _ = eval_guard.decide([("M", "src/eval_guard.py")], set(), True, None, None)
    assert not ok
