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


def test_the_task_list_has_judge_commands_to_read() -> None:
    """A check that found nothing to read would pass by reading nothing."""
    found = judge_commands.judge_commands(task_list())
    assert len(found) >= 39, f"only {len(found)} judge commands found"


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
