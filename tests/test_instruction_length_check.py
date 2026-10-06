"""instruction_length_check has to pass 22 lines and name the 23rd, and name an undated lesson.

The cap is `docs/HOW_WE_WORK.md`'s: "`CLAUDE.md` is capped at 22 lines". The
files below are planted by this file with a line count written out by hand.

The date rule is `lessons.md`'s header's: every lesson starts with its date,
YYYY-MM-DD and a space. The planted lessons file has a two-line header, three
dated lessons, one indented line under the second (the shape of
`archive/lessons_enforced.md`, whose note sits under each lesson), and the
undated line is planted at a line number written out by hand.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from src import instruction_length_check

REPO_ROOT = Path(__file__).resolve().parent.parent
DATED_LESSONS = [
    "# Lessons",
    "",
    "2026-09-06 the first lesson.",
    "2026-09-07 the second lesson.",
    "  (was line 8) enforced by: `src/append_check.py`, run by `make check`.",
    "2026-09-08 the third lesson.",
]


def plant(tmp_path: Path, lines: int) -> Path:
    path = tmp_path / "CLAUDE.md"
    path.write_text("".join(f"- rule {n}\n" for n in range(1, lines + 1)), encoding="utf-8")
    return path


def plant_lessons(tmp_path: Path, lines: list[str]) -> Path:
    path = tmp_path / "lessons.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
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


def test_dated_lessons_with_an_indented_note_pass(tmp_path, capsys):
    lessons = plant_lessons(tmp_path, DATED_LESSONS)

    assert instruction_length_check.main(
        ["--file", str(plant(tmp_path, 22)), "--lessons", str(lessons)]) == 0
    assert capsys.readouterr().err == ""


def test_an_undated_lesson_is_named_with_its_line(tmp_path, capsys):
    lessons = plant_lessons(tmp_path, DATED_LESSONS + ["a lesson written without its date."])

    assert instruction_length_check.main(
        ["--file", str(plant(tmp_path, 22)), "--lessons", str(lessons)]
    ) == instruction_length_check.FOUND
    assert capsys.readouterr().err.splitlines() == [
        f"{lessons}:7: a lesson starts with its date, YYYY-MM-DD and a space; "
        "this line does not: a lesson written without its date."]


def test_the_header_above_the_first_lesson_is_not_a_lesson(tmp_path, capsys):
    lessons = plant_lessons(tmp_path, ["# Lessons", "", "One line per mistake.", ""] + DATED_LESSONS[2:])

    assert instruction_length_check.main(
        ["--file", str(plant(tmp_path, 22)), "--lessons", str(lessons)]) == 0
    assert capsys.readouterr().err == ""


def test_a_lessons_file_that_is_not_there_cannot_be_judged(tmp_path):
    assert instruction_length_check.main(
        ["--file", str(plant(tmp_path, 22)), "--lessons", str(tmp_path / "lessons.md")]
    ) == instruction_length_check.CANNOT_RUN


def test_this_repository_s_lessons_files_are_dated():
    for path in instruction_length_check.LESSONS:
        assert instruction_length_check.undated_lessons(path) == []


def test_the_gate_runs_the_check():
    printed = subprocess.run(
        ("make", "-n", "check", f"PYTHON={sys.executable}", "BASELINE=origin/main"),
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    assert [line for line in printed.splitlines() if "src.instruction_length_check" in line]
