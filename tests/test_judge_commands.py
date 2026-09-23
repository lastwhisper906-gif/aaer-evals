"""The judge commands in the task list are read back and run.

The expected values are two things this project already wrote down, and neither
of them came from running the module under test:

* **The command strings**, read out of `docs/next_cycle_tasks.md` by the test
  itself. The file is the ledger of what each item's judge is; if a line there
  names an interpreter, that is the claim being checked.
* **The import failure**, reproduced here rather than quoted. On 2026-09-13 six
  of six reproduce-lens runs exited 1 with `No module named pytest` before
  collecting a test, because every judge said `python3.12 -m pytest` and bare
  `python3.12` on this machine has no site-packages for this project. The test
  below puts that same question to whatever `python3.12` resolves to and records
  the answer instead of asserting a machine fact that could change under it.

Two questions are kept apart on purpose, because they have different answers in
different places. *Does the command name the accepted interpreter* is a question
about the text and is asked everywhere, continuous integration included. *Does
that interpreter import pytest* is a question about this machine and is asked
only where the interpreter exists -- continuous integration runs `make check
PYTHON=python` against an interpreter it installed itself and has no `.venv` at
all. A test that conflated them would go red there for the wrong reason, and a
test that goes red for the wrong reason gets switched off.

Every test that asserts silence also plants a bad command into the same input,
so a pattern that matches nothing cannot pass by finding nothing.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from src import judge_commands

REPO_ROOT = Path(__file__).resolve().parent.parent
TASK_LIST = REPO_ROOT / "docs" / "next_cycle_tasks.md"

# The command that was in the file until this item, and the one that replaced it.
THE_COMMAND_THAT_COULD_NOT_RUN = "python3.12 -m pytest tests/test_market.py -q"
THE_COMMAND_THAT_RUNS = ".venv/bin/python -m pytest tests/test_market.py -q"


def task_list() -> str:
    return TASK_LIST.read_text(encoding="utf-8")


# --- the file ---------------------------------------------------------------


# How many judge commands the ledger held before this item rewrote them:
#     git show resume/lens-and-prices:docs/next_cycle_tasks.md
#         | grep -c '`python3.12 -m pytest'
# gave 39. The floor is that count, not a number chosen to pass.
#
# The rows that already named the interpreter this item moves the rest onto
# are counted by the same command with `.venv/bin/python` in place of
# `python3.12`. No number is written here: nothing asserts one, and the last
# number written here was wrong.
JUDGE_COMMANDS_BEFORE = 39

# An independent reading of the same file: any one-line backtick span that runs
# pytest. It is deliberately not the module's own extractor -- a bound checked
# with the code under test would move whenever that code dropped something.
A_JUDGE_COMMAND = re.compile(r"`([^`\n]*-m pytest[^`\n]*)`")


def test_the_task_list_has_judge_commands_to_read() -> None:
    """A check that found nothing to read would pass by reading nothing.

    Two readings of the same file have to agree. `>= 39` alone is loose by the
    rows that already named the project interpreter (the command in the comment
    above counts them), so an extractor that silently dropped that many
    commands would still pass it -- and
    `problems() == []` below would then be silent about every one it dropped.
    """
    found = judge_commands.judge_commands(task_list())
    assert len(found) >= JUDGE_COMMANDS_BEFORE, f"only {len(found)} judge commands found"

    independently = A_JUDGE_COMMAND.findall(task_list())
    assert len(found) == len(independently), (
        f"the extractor read {len(found)} judge commands where a plain scan of the "
        f"same file found {len(independently)}")


def test_every_judge_command_names_the_project_interpreter() -> None:
    assert judge_commands.problems(task_list()) == []


def test_the_interpreter_every_judge_names_imports_pytest() -> None:
    """The question the six failed reproduce runs were really asking."""
    named = {judge_commands.interpreter_of(command)
             for _, command in judge_commands.judge_commands(task_list())}
    assert named, "no interpreter was named by any judge command"
    asked = 0
    for interpreter in sorted(named):
        answer = judge_commands.imports_pytest(interpreter, root=REPO_ROOT)
        if answer is None:
            continue  # not installed here; continuous integration has no .venv
        asked += 1
        assert answer, f"{interpreter} cannot import pytest, so its judge cannot run"
    if shutil.which(judge_commands.ACCEPTED) or (REPO_ROOT / judge_commands.ACCEPTED).exists():
        assert asked, "the project interpreter is here and was not asked"


def _planted_interpreter(directory: Path, name: str, exit_code: int) -> str:
    """An executable that answers `-c "import pytest"` the way we tell it to."""
    planted = directory / name
    planted.write_text(f"#!/bin/sh\nexit {exit_code}\n", encoding="utf-8")
    planted.chmod(0o755)
    return str(planted)


def test_an_interpreter_without_pytest_is_answered_false(tmp_path: Path) -> None:
    """The branch the six failed runs actually took, asserted rather than skipped.

    `test_the_interpreter_the_old_judges_named_still_cannot_run_them` above can
    only *record* this machine's answer -- it skips when the bare interpreter
    happens to have pytest, which is right, because that is a fact about
    somebody's machine. But then nothing asserted the False branch at all, and
    `return result.returncode == 0` could have been `return True` with the suite
    still green. So the interpreter is planted here instead of found: one that
    cannot import pytest, one that can, and one that is not there.
    """
    without = _planted_interpreter(tmp_path, "no-pytest", 1)
    assert judge_commands.imports_pytest(without) is False

    with_it = _planted_interpreter(tmp_path, "has-pytest", 0)
    assert judge_commands.imports_pytest(with_it) is True

    assert judge_commands.imports_pytest(str(tmp_path / "not-here")) is None


def test_a_relative_interpreter_is_read_from_the_root_it_was_given(tmp_path: Path) -> None:
    """`.venv/bin/python` is relative; which tree it means is the whole question."""
    (tmp_path / "here").mkdir()
    _planted_interpreter(tmp_path / "here", "python", 1)
    assert judge_commands.imports_pytest("here/python", root=tmp_path) is False
    assert judge_commands.imports_pytest("here/python", root=tmp_path / "elsewhere") is None


def test_the_makefile_default_is_the_same_interpreter() -> None:
    """The Makefile carried the same hole, which is why the Stop hook overrode it."""
    makefile = (REPO_ROOT / "Makefile").read_text(encoding="utf-8")
    default = [line for line in makefile.splitlines() if line.startswith("PYTHON ?=")]
    assert default == [f"PYTHON ?= {judge_commands.ACCEPTED}"]


def test_continuous_integration_still_names_its_own_interpreter() -> None:
    """The default is for this machine; CI installs the requirements elsewhere."""
    workflow = (REPO_ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "make check PYTHON=python" in workflow


# --- the check itself -------------------------------------------------------


def test_the_command_that_could_not_run_is_reported() -> None:
    planted = f"[ ] an item · a module · `{THE_COMMAND_THAT_COULD_NOT_RUN}` · a source · PR:"
    found = judge_commands.problems(planted, path="planted.md")
    assert len(found) == 1
    assert "python3.12" in found[0]
    assert "planted.md:1:" in found[0]


def test_the_command_that_runs_is_not_reported() -> None:
    planted = (
        f"[ ] one item · a module · `{THE_COMMAND_THAT_RUNS}` · a source · PR:\n"
        f"[ ] another · a module · `{THE_COMMAND_THAT_COULD_NOT_RUN}` · a source · PR:"
    )
    found = judge_commands.problems(planted, path="planted.md")
    assert [line.split(":")[1] for line in found] == ["2"]


def test_prose_about_the_interpreter_is_left_alone() -> None:
    """The file quotes `python3.12` twice while explaining the failure."""
    planted = (
        "bare `python3.12` on this machine is `/opt/homebrew/bin/python3.12`\n"
        f"[ ] an item · a module · `{THE_COMMAND_THAT_COULD_NOT_RUN}` · a source · PR:"
    )
    found = judge_commands.problems(planted, path="planted.md")
    assert [line.split(":")[1] for line in found] == ["2"]


def test_a_command_outside_backticks_is_not_a_command() -> None:
    assert judge_commands.judge_commands("run python3.12 -m pytest tests -q somewhere") == []


def test_the_interpreter_is_the_word_before_the_module_flag() -> None:
    assert judge_commands.interpreter_of(THE_COMMAND_THAT_RUNS) == ".venv/bin/python"
    assert judge_commands.interpreter_of(THE_COMMAND_THAT_COULD_NOT_RUN) == "python3.12"
    assert judge_commands.interpreter_of("/usr/bin/env python3 -m pytest -q") == "python3"


def test_an_interpreter_that_is_not_here_is_not_a_pass(tmp_path: Path) -> None:
    """None means unasked. A check that read it as True would pass on absence."""
    assert judge_commands.imports_pytest(str(tmp_path / "nothing"), root=REPO_ROOT) is None


def test_this_interpreter_imports_pytest() -> None:
    assert judge_commands.imports_pytest(sys.executable, root=REPO_ROOT) is True


def test_the_command_line_reports_what_it_found(tmp_path: Path) -> None:
    planted = tmp_path / "list.md"
    planted.write_text(
        f"[ ] an item · a module · `{THE_COMMAND_THAT_COULD_NOT_RUN}` · a source · PR:\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, "-m", "src.judge_commands", str(planted)],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        env={"PATH": "/usr/bin:/bin", "PYTHONPATH": str(REPO_ROOT)},
    )
    assert result.returncode == judge_commands.FOUND
    assert "python3.12" in result.stderr


# --- the failure this item exists for --------------------------------------


def test_the_interpreter_the_old_judges_named_still_cannot_run_them() -> None:
    """Recorded, not asserted: the machine could change and the item would not.

    The point of the item is that the ledger named an interpreter nobody had
    checked. Asserting that a particular homebrew interpreter has no pytest
    would be asserting a fact about somebody's machine; what is asserted is that
    if it cannot run the judge, the judge that named it was not a judge.
    """
    found = shutil.which("python3.12")
    # Compared unresolved on purpose. A virtual environment's `python` is a
    # symlink to the very interpreter `python3.12` names, so resolving both
    # makes them equal while their site-packages remain different -- which is
    # the whole difference the six failed runs were about.
    if found is None or Path(found) == Path(sys.executable):
        pytest.skip("no separate bare python3.12 on this machine")
    answer = judge_commands.imports_pytest(found, root=REPO_ROOT)
    if answer:
        pytest.skip(f"{found} imports pytest here, so the old judges would have run")
    assert judge_commands.problems(
        f"`{THE_COMMAND_THAT_COULD_NOT_RUN}`", path="planted.md"
    ), "the check has to report the command that this very interpreter cannot run"


def test_every_place_that_runs_a_judge_in_a_fresh_tree_provides_the_interpreter() -> None:
    """A relative interpreter is only an interpreter where `.venv` exists.

    The judges say `.venv/bin/python`, which is relative to the tree the command
    runs in. Three procedures run a judge in a tree that is not the main
    checkout, and each one has to put the interpreter there first or the command
    exits 127 before collecting a test -- loud rather than silent, but still a
    run that says nothing about the item. `reproduce-check` is the one that was
    missing it: it creates a detached worktree "outside the working tree", where
    the `../../../.venv` recipe does not reach.
    """
    procedures = {
        ".claude/agents/reproduce-check.md": REPO_ROOT / ".claude/agents/reproduce-check.md",
        ".claude/skills/build-item/SKILL.md": REPO_ROOT / ".claude/skills/build-item/SKILL.md",
        "docs/routines/weekly-relens.md": REPO_ROOT / "docs/routines/weekly-relens.md",
    }
    silent = []
    for name, path in procedures.items():
        if not path.is_file():
            silent.append(f"{name}: not there")
            continue
        text = path.read_text(encoding="utf-8")
        if ".venv" not in text:
            silent.append(f"{name}: runs a judge in a fresh tree and never names .venv")
    assert silent == [], silent
