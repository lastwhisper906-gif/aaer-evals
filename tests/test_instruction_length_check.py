"""instruction_length_check has to pass 22 lines and name the 23rd.

The cap is `docs/HOW_WE_WORK.md`'s: "`CLAUDE.md` is capped at 22 lines". The
files below are planted by this file with a line count written out by hand.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from src import instruction_length_check

REPO_ROOT = Path(__file__).resolve().parent.parent


def plant(tmp_path: Path, lines: int) -> Path:
    path = tmp_path / "CLAUDE.md"
    path.write_text("".join(f"- rule {n}\n" for n in range(1, lines + 1)), encoding="utf-8")
    return path


def test_twenty_two_lines_are_within_the_cap(tmp_path, capsys):
    assert instruction_length_check.main(["--file", str(plant(tmp_path, 22))]) == 0
    assert capsys.readouterr().err == ""


def test_twenty_three_lines_are_named(tmp_path, capsys):
    path = plant(tmp_path, 23)

    assert instruction_length_check.main(["--file", str(path)]) == instruction_length_check.FOUND
    assert capsys.readouterr().err.splitlines() == [
        f"{path}:23: 23 lines, over the cap of 22; replace a line rather than append one"]


def test_a_last_line_with_no_newline_still_counts(tmp_path):
    path = plant(tmp_path, 22)
    path.write_text(path.read_text(encoding="utf-8") + "- one more", encoding="utf-8")

    assert instruction_length_check.main(["--file", str(path)]) == instruction_length_check.FOUND


def test_a_file_that_is_not_there_cannot_be_judged(tmp_path):
    assert (instruction_length_check.main(["--file", str(tmp_path / "CLAUDE.md")])
            == instruction_length_check.CANNOT_RUN)


def test_the_gate_runs_the_check():
    printed = subprocess.run(
        ("make", "-n", "check", f"PYTHON={sys.executable}", "BASELINE=origin/main"),
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    assert [line for line in printed.splitlines() if "src.instruction_length_check" in line]
