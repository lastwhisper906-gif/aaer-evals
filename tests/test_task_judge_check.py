"""task_judge_check has to name an open item with no judge, and pass one that has a judge.

Both lists are planted by this file as text, in the row shapes their own headers
state: `[ ] title · builds · judge · expected value from · PR` for
`docs/next_cycle_tasks.md` and `[ ] what · eval command that must pass · depends
on` for `queue.md`. The expected lines are written out by hand from where each
row was planted.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from src import task_judge_check

REPO_ROOT = Path(__file__).resolve().parent.parent

JUDGED = ("[ ] build the reader · `src/reader.py` · "
          "`.venv/bin/python -m pytest tests/test_reader.py -q` · the filing · PR: none\n")
NO_JUDGE = "[ ] build the reader · `src/reader.py` ·  · the filing · PR: none\n"
TITLE_ONLY = "[ ] build the reader\n"
# Lines 1 to 4: heading, blank, the judged row, blank.
TASKS_HEAD = "## This cycle\n\n" + JUDGED + "\n"
NEEDS_JUDGMENT = "## Needs judgment\n\n[ ] a wish with no judge\n"

QUEUED = "[ ] the reader · `.venv/bin/python -m pytest tests/test_reader.py -q` · none\n"
NO_COMMAND = "[ ] the reader · run it and see · none\n"
# Lines 1 to 2: heading, blank; the first row planted after it is line 3.
QUEUE_HEAD = "## Open\n\n"
DONE = "\n## Done\n\n[ ] an old line with no command · none\n"


def plant(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def run(tasks: Path, queue: Path) -> int:
    return task_judge_check.main(["--tasks", str(tasks), "--queue", str(queue)])


def test_open_items_with_judges_are_clean(tmp_path, capsys):
    tasks = plant(tmp_path / "docs" / "next_cycle_tasks.md", TASKS_HEAD + NEEDS_JUDGMENT)
    queue = plant(tmp_path / "queue.md", QUEUE_HEAD + QUEUED + DONE)

    assert run(tasks, queue) == 0
    assert capsys.readouterr().err == ""


def test_a_task_row_with_an_empty_judge_is_named(tmp_path, capsys):
    tasks = plant(tmp_path / "docs" / "next_cycle_tasks.md", TASKS_HEAD + NO_JUDGE)

    assert run(tasks, tmp_path / "queue.md") == task_judge_check.FOUND
    assert capsys.readouterr().err.splitlines() == [f"{tasks}:5: an open item names no judge"]


def test_a_task_row_that_is_only_a_title_is_named(tmp_path, capsys):
    tasks = plant(tmp_path / "docs" / "next_cycle_tasks.md",
                  TASKS_HEAD + "## Next cycle\n\n" + TITLE_ONLY)

    assert run(tasks, tmp_path / "queue.md") == task_judge_check.FOUND
    assert capsys.readouterr().err.splitlines() == [f"{tasks}:7: an open item names no judge"]


def test_a_queue_row_with_no_command_is_named(tmp_path, capsys):
    queue = plant(tmp_path / "queue.md", QUEUE_HEAD + QUEUED + NO_COMMAND)

    assert run(tmp_path / "docs" / "next_cycle_tasks.md", queue) == task_judge_check.FOUND
    assert capsys.readouterr().err.splitlines() == [
        f"{queue}:4: an open item names no eval command"]


def test_a_list_whose_open_rows_sit_under_another_heading_is_refused(tmp_path, capsys):
    tasks = plant(tmp_path / "docs" / "next_cycle_tasks.md", "## Blocked\n\n" + JUDGED)
    queue = plant(tmp_path / "queue.md", "## Blocked\n\n" + QUEUED)

    assert run(tasks, queue) == task_judge_check.CANNOT_RUN
    assert capsys.readouterr().err.splitlines() == [
        f"{tasks}: no rows under ## Next cycle or ## This cycle; a renamed section is not "
        "an empty list",
        f"{queue}: no rows under ## Open; a renamed section is not an empty list"]


def test_this_repository_s_lists_yield_rows():
    assert len(task_judge_check.rows(REPO_ROOT / "docs" / "next_cycle_tasks.md",
                                     task_judge_check.TASK_SECTIONS)) > 0
    assert len(task_judge_check.rows(REPO_ROOT / "queue.md",
                                     frozenset({task_judge_check.QUEUE_SECTION}))) > 0


def test_no_list_at_all_is_not_a_clean_list(tmp_path, capsys):
    assert (run(tmp_path / "docs" / "next_cycle_tasks.md", tmp_path / "queue.md")
            == task_judge_check.CANNOT_RUN)
    assert "neither" in capsys.readouterr().err


def test_the_gate_runs_the_check():
    printed = subprocess.run(
        ("make", "-n", "check", f"PYTHON={sys.executable}", "BASELINE=origin/main"),
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    assert [line for line in printed.splitlines() if "src.task_judge_check" in line]
