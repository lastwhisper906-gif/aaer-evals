"""archive_check has to catch a rewrite of an archived file, and let a new one through."""

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
