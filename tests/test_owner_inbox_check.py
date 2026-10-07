"""owner_inbox_check has to name a row that waits, and stay silent on one that names its default.

Every inbox here is planted by this file as text, in the row shape
`docs/needs_judgment.md` states in its own header: `what is unsettled · the
default in force today · what changes when the owner decides`. The expected
lines are written out by hand from where each row was planted; nothing is read
back out of the check to decide what it should have said.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from src import owner_inbox_check

REPO_ROOT = Path(__file__).resolve().parent.parent

# Lines 1 to 4; the first row planted after it is line 5.
HEADER = "# Needs judgment\n\n## Open\n\n"
NAMED = ("[ ] **the word list** · not committed, so the indicator is written missing "
         "· the indicator is computed\n")
EMPTY_DEFAULT = "[ ] **the word list** ·  · the indicator is computed\n"
TWO_PARTS = "[ ] **the word list** · waiting for the owner\n"
NOTE = "- a bullet that explains the list is not a row\n"
# Lines 6 to 9 when it follows one row: blank, heading, blank, the row.
SETTLED = "\n## Settled by default\n\n- **the sector map** · default: one fund per division.\n"
SETTLED_BARE = "\n## Settled by default\n\n- **the sector map** · the owner will say.\n"


def plant(tmp_path: Path, text: str) -> Path:
    inbox = tmp_path / "docs" / "needs_judgment.md"
    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text(text, encoding="utf-8")
    return inbox


def run(tmp_path: Path, inbox: Path) -> int:
    return owner_inbox_check.main(["--inbox", str(inbox), "--root", str(tmp_path)])


def test_rows_that_name_their_default_are_clean(tmp_path, capsys):
    inbox = plant(tmp_path, HEADER + NOTE + NAMED + SETTLED)
    (tmp_path / "archive").mkdir()
    (tmp_path / "archive" / "OWNER_QUEUE.md").write_text("the archived queue\n")

    assert run(tmp_path, inbox) == 0
    assert capsys.readouterr().err == ""


def test_an_open_row_with_an_empty_default_is_named(tmp_path, capsys):
    inbox = plant(tmp_path, HEADER + NAMED + EMPTY_DEFAULT)

    assert run(tmp_path, inbox) == owner_inbox_check.FOUND
    assert capsys.readouterr().err.splitlines() == [
        f"{inbox}:6: an open row names no default in force"]


def test_an_open_row_with_no_default_part_is_named(tmp_path, capsys):
    inbox = plant(tmp_path, HEADER + TWO_PARTS)

    assert run(tmp_path, inbox) == owner_inbox_check.FOUND
    assert capsys.readouterr().err.splitlines() == [
        f"{inbox}:5: an open row names no default in force"]


def test_a_settled_row_that_does_not_say_its_default_is_named(tmp_path, capsys):
    inbox = plant(tmp_path, HEADER + NAMED + SETTLED_BARE)

    assert run(tmp_path, inbox) == owner_inbox_check.FOUND
    assert capsys.readouterr().err.splitlines() == [
        f"{inbox}:9: a settled row does not say its default"]


def test_a_sign_off_file_outside_the_archive_is_named(tmp_path, capsys):
    inbox = plant(tmp_path, HEADER + NAMED)
    (tmp_path / "DECISIONS_PENDING.md").write_text("waiting for the owner\n")

    assert run(tmp_path, inbox) == owner_inbox_check.FOUND
    assert capsys.readouterr().err.splitlines() == [
        "DECISIONS_PENDING.md:0: a file named as a sign-off queue"]


def test_an_inbox_whose_rows_sit_under_another_heading_is_refused(tmp_path, capsys):
    inbox = plant(tmp_path, "# Needs judgment\n\n## Blocked\n\n" + NOTE
                  + "\n## Settled elsewhere\n\n- **the sector map** · default: one fund.\n")

    assert run(tmp_path, inbox) == owner_inbox_check.CANNOT_RUN
    assert capsys.readouterr().err.splitlines() == [
        f"{inbox}: no rows under any heading as `[ ] ` or under ## Settled by default as "
        "`- `; a renamed section is not an empty list"]


def test_this_repository_s_inbox_yields_rows():
    kinds = [kind for _, kind, _ in owner_inbox_check.rows(REPO_ROOT / "docs" / "needs_judgment.md")]
    assert kinds.count("open") > 0
    assert kinds.count("settled") > 0


def test_an_inbox_that_is_not_there_is_not_a_clean_inbox(tmp_path, capsys):
    assert run(tmp_path, tmp_path / "docs" / "needs_judgment.md") == owner_inbox_check.CANNOT_RUN
    assert "is not there" in capsys.readouterr().err


def test_the_gate_runs_the_check():
    printed = subprocess.run(
        ("make", "-n", "check", f"PYTHON={sys.executable}", "BASELINE=origin/main"),
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    assert [line for line in printed.splitlines() if "src.owner_inbox_check" in line]
