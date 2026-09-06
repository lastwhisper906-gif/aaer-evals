"""append_check has to catch an edit to a published file, and let a new one through."""

from __future__ import annotations

import subprocess

import pytest

from src import append_check

PUBLISHED_LINE = '{"event": "late_filing", "ticker": "STX"}\n'


def git(repo, *args):
    subprocess.run(("git", *args), cwd=repo, check=True, capture_output=True)


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A repo whose baseline branch already holds one published prediction."""
    git(tmp_path, "init", "-q", "-b", "baseline")
    git(tmp_path, "config", "user.email", "test@example.invalid")
    git(tmp_path, "config", "user.name", "test")

    run = tmp_path / "runs" / "AAPL" / "0000320193-26-000001"
    run.mkdir(parents=True)
    (run / "prediction_pressure.json").write_text('{"tier": "clear"}\n')
    (tmp_path / "runs" / "README.md").write_text("# runs/\n\nappend-only\n")
    (tmp_path / "events").mkdir()
    (tmp_path / "events" / "ledger.jsonl").write_text(PUBLISHED_LINE)
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-qm", "baseline")

    git(tmp_path, "checkout", "-q", "-b", "work")
    monkeypatch.chdir(tmp_path)
    return tmp_path


def commit_all(repo, message="work"):
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", message)


def test_a_new_prediction_is_clean(repo):
    new = repo / "runs" / "AAPL" / "0000320193-26-000002"
    new.mkdir(parents=True)
    (new / "prediction_pressure.json").write_text('{"tier": "watch"}\n')
    commit_all(repo)

    assert append_check.violations("baseline") == []
    assert append_check.main(["--baseline", "baseline"]) == 0


def test_appending_to_the_ledger_is_clean(repo):
    ledger = repo / "events" / "ledger.jsonl"
    ledger.write_text(PUBLISHED_LINE + '{"event": "guidance_cut", "ticker": "CIEN"}\n')
    commit_all(repo)

    assert append_check.violations("baseline") == []


def test_rewriting_a_published_ledger_line_fails(repo):
    ledger = repo / "events" / "ledger.jsonl"
    ledger.write_text('{"event": "late_filing", "ticker": "AAPL"}\n')
    commit_all(repo)

    assert append_check.violations("baseline") == ["modified: events/ledger.jsonl"]


def test_truncating_the_ledger_fails(repo):
    (repo / "events" / "ledger.jsonl").write_text("")
    commit_all(repo)

    assert append_check.violations("baseline") == ["modified: events/ledger.jsonl"]


def test_editing_a_published_prediction_fails(repo):
    published = repo / "runs" / "AAPL" / "0000320193-26-000001" / "prediction_pressure.json"
    published.write_text('{"tier": "elevated"}\n')
    commit_all(repo)

    assert append_check.violations("baseline") == [
        "modified: runs/AAPL/0000320193-26-000001/prediction_pressure.json"
    ]
    assert append_check.main(["--baseline", "baseline"]) == 1


def test_deleting_a_published_prediction_fails(repo):
    published = repo / "runs" / "AAPL" / "0000320193-26-000001" / "prediction_pressure.json"
    published.unlink()
    commit_all(repo)

    assert append_check.violations("baseline") == [
        "deleted: runs/AAPL/0000320193-26-000001/prediction_pressure.json"
    ]


def test_the_directory_readme_stays_editable(repo):
    """It explains the directory; freezing it the day it is written is a bug."""
    (repo / "runs" / "README.md").write_text("# runs/\n\nrewritten\n")
    commit_all(repo)

    assert append_check.violations("baseline") == []


def test_a_readme_inside_a_prediction_is_still_protected(repo):
    inside = repo / "runs" / "AAPL" / "0000320193-26-000001" / "README.md"
    inside.write_text("first\n")
    commit_all(repo, "publish a readme inside the bundle")
    git(repo, "branch", "-f", "baseline", "HEAD")

    inside.write_text("second\n")
    commit_all(repo, "quietly change it")

    assert append_check.violations("baseline") == [
        "modified: runs/AAPL/0000320193-26-000001/README.md"
    ]


def test_unprotected_paths_are_ignored(repo):
    (repo / "README.md").write_text("rewritten\n")
    (repo / "src").mkdir()
    (repo / "src" / "extract.py").write_text("# new\n")
    commit_all(repo)

    assert append_check.violations("baseline") == []


def test_the_one_time_archive_relocation_passes(repo):
    git(repo, "mv", "runs", "archive_runs_tmp")
    (repo / "archive").mkdir()
    git(repo, "mv", "archive_runs_tmp", "archive/runs")
    git(repo, "mv", "events", "archive_events_tmp")
    git(repo, "mv", "archive_events_tmp", "archive/events")
    commit_all(repo)

    assert append_check.violations("baseline") == []


def test_relocating_anywhere_but_archive_fails(repo):
    git(repo, "mv", "runs", "old_runs")
    commit_all(repo)

    assert append_check.violations("baseline") == [
        "deleted: runs/AAPL/0000320193-26-000001/prediction_pressure.json"
    ]


def test_an_unresolvable_baseline_is_not_a_pass(repo):
    assert append_check.main(["--baseline", "no-such-ref"]) == 2
