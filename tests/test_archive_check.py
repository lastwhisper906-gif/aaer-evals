"""archive_check has to catch a rewrite of an archived file, and let a new one or an append through.

The baseline's archived file is `# the old method\n`, one line ending in a
newline. An append keeps those bytes and adds a line after them, the way
`archive/lessons_enforced.md` takes a lesson a script comes to enforce; a
rewrite changes the line; an append onto a baseline with no final newline
would finish that last line differently, so it is a rewrite too.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from src import archive_check

REPO_ROOT = Path(__file__).resolve().parent.parent


def git(repo, *args):
    subprocess.run(("git", *args), cwd=repo, check=True, capture_output=True)


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A repo whose baseline branch already holds one archived file and one live one."""
    git(tmp_path, "init", "-q", "-b", "baseline")
    git(tmp_path, "config", "user.email", "test@example.invalid")
    git(tmp_path, "config", "user.name", "test")

    (tmp_path / "archive" / "docs").mkdir(parents=True)
    (tmp_path / "archive" / "docs" / "method.md").write_text("# the old method\n")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "how.md").write_text("# how we work\n")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-qm", "baseline")

    git(tmp_path, "checkout", "-q", "-b", "work")
    monkeypatch.chdir(tmp_path)
    return tmp_path


def commit_all(repo, message="work"):
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", message)


def test_a_new_archived_file_and_a_live_edit_are_clean(repo):
    (repo / "archive" / "lessons_enforced.md").write_text("# moved here\n")
    (repo / "docs" / "how.md").write_text("# how we work, edited\n")
    commit_all(repo)

    assert archive_check.violations("baseline") == []
    assert archive_check.main(["--baseline", "baseline"]) == 0


def test_appending_to_an_archived_file_passes(repo):
    with (repo / "archive" / "docs" / "method.md").open("a") as f:
        f.write("2026-10-07 a lesson a script now enforces.\n  enforced by: src/x.py\n")
    commit_all(repo)

    assert archive_check.violations("baseline") == []
    assert archive_check.main(["--baseline", "baseline"]) == 0


ARCHIVED_LESSONS = (
    "# Lessons a script enforces\n"
    "\n"
    "2026-09-07 the first archived lesson.\n"
    "  (was line 19) obsolete: the artefact was retired.\n"
    "\n"
    "2026-09-08 the second archived lesson.\n"
    "  (was line 33) enforced by: `tests/test_x.py`.\n"
)
MOVED_BACK = (
    "\n"
    "## Moved back\n"
    "\n"
    "2026-10-07 (was line 19) \"the first archived lesson ...\" went back to lessons.md: "
    "the note retires the artefact, not the lesson.\n"
)


@pytest.fixture
def repo_with_archived_lessons(repo):
    """The baseline also holds archive/lessons_enforced.md, two lessons with their notes."""
    (repo / "archive" / "lessons_enforced.md").write_text(ARCHIVED_LESSONS)
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "the archive holds the lessons file")
    git(repo, "branch", "-f", "baseline")
    return repo


def test_a_move_back_recorded_by_appending_passes(repo_with_archived_lessons):
    repo = repo_with_archived_lessons
    (repo / "archive" / "lessons_enforced.md").write_text(ARCHIVED_LESSONS + MOVED_BACK)
    commit_all(repo)

    assert archive_check.violations("baseline") == []
    assert archive_check.main(["--baseline", "baseline"]) == 0


def test_a_move_back_recorded_under_its_row_fails(repo_with_archived_lessons):
    repo = repo_with_archived_lessons
    (repo / "archive" / "lessons_enforced.md").write_text(ARCHIVED_LESSONS.replace(
        "  (was line 19) obsolete: the artefact was retired.\n",
        "  (was line 19) obsolete: the artefact was retired.\n"
        "  moved back to lessons.md on 2026-10-07: the note retires the artefact.\n"))
    commit_all(repo)

    assert archive_check.violations("baseline") == ["modified: archive/lessons_enforced.md"]
    assert archive_check.main(["--baseline", "baseline"]) == archive_check.FOUND


def test_rewriting_a_line_and_appending_fails(repo):
    (repo / "archive" / "docs" / "method.md").write_text("# the old method, rewritten\nappended\n")
    commit_all(repo)

    assert archive_check.violations("baseline") == ["modified: archive/docs/method.md"]


def test_inserting_above_the_end_fails(repo):
    (repo / "archive" / "docs" / "method.md").write_text("inserted\n# the old method\n")
    commit_all(repo)

    assert archive_check.violations("baseline") == ["modified: archive/docs/method.md"]


def test_appending_onto_a_baseline_with_no_final_newline_fails(repo):
    path = repo / "archive" / "docs" / "method.md"
    path.write_text("# the old method")
    commit_all(repo, "no final newline")
    git(repo, "branch", "-f", "unterminated")
    path.write_text("# the old method\nappended\n")
    commit_all(repo)

    assert archive_check.violations("unterminated") == ["modified: archive/docs/method.md"]


def test_editing_an_archived_file_fails(repo):
    (repo / "archive" / "docs" / "method.md").write_text("# the old method, rewritten\n")
    commit_all(repo)

    assert archive_check.violations("baseline") == ["modified: archive/docs/method.md"]
    assert archive_check.main(["--baseline", "baseline"]) == archive_check.FOUND


def test_deleting_an_archived_file_fails(repo):
    (repo / "archive" / "docs" / "method.md").unlink()
    commit_all(repo)

    assert archive_check.violations("baseline") == ["deleted: archive/docs/method.md"]


def test_an_unresolvable_baseline_is_not_a_pass(repo):
    assert archive_check.main(["--baseline", "no-such-ref"]) == archive_check.CANNOT_RUN


def test_the_gate_runs_the_check():
    printed = subprocess.run(
        ("make", "-n", "check", f"PYTHON={sys.executable}", "BASELINE=origin/main"),
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    assert [line for line in printed.splitlines() if "src.archive_check" in line]
