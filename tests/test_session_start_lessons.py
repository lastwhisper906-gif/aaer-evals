"""The session-start printout: the header, then the newest lessons, at most sixty lines.

The lessons files are planted by this file, and the expected printout is worked
out by hand from the planted shape: a four-line header leaves fifty-six lines,
one of which says how many older lessons were left out, so a hundred lessons
print as the header, that line, and lessons 46 to 100.

A lesson is a dated line plus its continuation lines: a line after the first
lesson that does not start with a date belongs to the lesson before it. With
lesson 80 wrapped onto a second line, the fifty-five lines after the note hold
lessons 100 down to 81 (twenty lines), lesson 80 (two) and lessons 79 down to
47 (thirty-three), so the note says 46 older lessons, not 45. With every lesson
two lines long, fifty-five lines hold twenty-seven whole lessons (fifty-four
lines) and a lesson is never split, so the printout is fifty-nine lines.

The header is capped by the script too: a seventy-line header with five
lessons leaves no room for the note, so the first fifty-nine header lines
print and the sixtieth says eleven header lines and five lessons were left
out; a fifty-five-line header with three lessons prints whole, fifty-eight
lines, and a sixty-line header with no lessons prints whole, sixty lines.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "tools" / "session_start_lessons.sh"
HEADER = ["# Lessons", "", "One line per mistake, newest last.", ""]


def lesson(n: int) -> str:
    return f"2026-09-{1 + n % 28:02d} lesson number {n}, written in the order it was learned."


def wrapped(n: int) -> str:
    return f"  and this is the rest of lesson number {n}, wrapped onto a second line."


def plant(tmp_path: Path, count: int, wrap: set[int] = frozenset()) -> Path:
    path = tmp_path / "lessons.md"
    lines = list(HEADER)
    for n in range(1, count + 1):
        lines.append(lesson(n))
        if n in wrap:
            lines.append(wrapped(n))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def printed(path: Path) -> subprocess.CompletedProcess:
    return subprocess.run(("sh", str(SCRIPT), str(path)), capture_output=True, text=True)


def test_a_long_file_prints_the_header_and_the_newest_lessons_newest_last(tmp_path):
    result = printed(plant(tmp_path, 100))

    assert result.returncode == 0
    lines = result.stdout.splitlines()
    assert len(lines) == 60
    assert lines[:4] == HEADER
    assert lines[4] == f"(45 older lessons are in {tmp_path / 'lessons.md'} and not printed here.)"
    assert lines[5:] == [lesson(n) for n in range(46, 101)]


def test_a_short_file_prints_whole_with_no_note(tmp_path):
    result = printed(plant(tmp_path, 10))

    assert result.returncode == 0
    assert result.stdout.splitlines() == HEADER + [lesson(n) for n in range(1, 11)]


def test_a_wrapped_lesson_prints_both_of_its_lines_and_the_count_says_so(tmp_path):
    result = printed(plant(tmp_path, 100, wrap={80}))

    assert result.returncode == 0
    lines = result.stdout.splitlines()
    assert len(lines) == 60
    assert lines[4] == f"(46 older lessons are in {tmp_path / 'lessons.md'} and not printed here.)"
    assert lines[5:] == ([lesson(n) for n in range(47, 80)]
                         + [lesson(80), wrapped(80)]
                         + [lesson(n) for n in range(81, 101)])


def test_a_wrapped_lesson_in_a_short_file_is_printed_whole(tmp_path):
    result = printed(plant(tmp_path, 10, wrap={3, 10}))

    assert result.returncode == 0
    assert result.stdout.splitlines() == (
        HEADER + [lesson(1), lesson(2), lesson(3), wrapped(3)]
        + [lesson(n) for n in range(4, 10)] + [lesson(10), wrapped(10)])


def test_the_cap_holds_with_wrapped_lessons_and_no_lesson_is_split(tmp_path):
    result = printed(plant(tmp_path, 100, wrap=set(range(1, 101))))

    assert result.returncode == 0
    lines = result.stdout.splitlines()
    assert len(lines) <= 60
    assert len(lines) == 59
    assert lines[4] == f"(73 older lessons are in {tmp_path / 'lessons.md'} and not printed here.)"
    assert lines[5] == lesson(74)
    assert lines[5:] == [line for n in range(74, 101) for line in (lesson(n), wrapped(n))]


def plant_with_header(tmp_path: Path, header_lines: int, count: int) -> Path:
    path = tmp_path / "lessons.md"
    lines = ["# Lessons"] + [f"header line {n}" for n in range(2, header_lines + 1)]
    lines += [lesson(n) for n in range(1, count + 1)]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def test_a_header_longer_than_the_cap_is_cut_and_the_sixtieth_line_says_so(tmp_path):
    path = plant_with_header(tmp_path, 70, 5)
    result = printed(path)

    assert result.returncode == 0
    lines = result.stdout.splitlines()
    assert len(lines) == 60
    assert lines[:59] == ["# Lessons"] + [f"header line {n}" for n in range(2, 60)]
    assert lines[59] == f"(11 header lines and 5 lessons are in {path} and not printed here.)"


def test_a_header_within_the_cap_prints_whole_with_its_lessons(tmp_path):
    result = printed(plant_with_header(tmp_path, 55, 3))

    assert result.returncode == 0
    lines = result.stdout.splitlines()
    assert len(lines) == 58
    assert lines[:55] == ["# Lessons"] + [f"header line {n}" for n in range(2, 56)]
    assert lines[55:] == [lesson(1), lesson(2), lesson(3)]


def test_a_sixty_line_header_with_no_lessons_prints_whole(tmp_path):
    result = printed(plant_with_header(tmp_path, 60, 0))

    assert result.returncode == 0
    lines = result.stdout.splitlines()
    assert len(lines) == 60
    assert lines == ["# Lessons"] + [f"header line {n}" for n in range(2, 61)]


def test_a_sixty_line_header_with_a_lesson_still_holds_the_cap(tmp_path):
    """Sixty header lines and one lesson: fifty-nine print, so 60 - 59 = 1 header line is left out."""
    path = plant_with_header(tmp_path, 60, 1)
    result = printed(path)

    assert result.returncode == 0
    lines = result.stdout.splitlines()
    assert len(lines) == 60
    assert lines[59] == f"(1 header lines and 1 lessons are in {path} and not printed here.)"


def test_a_file_that_cannot_be_read_is_not_an_empty_one(tmp_path):
    result = printed(tmp_path / "lessons.md")

    assert result.returncode == 2
    assert result.stdout == ""
    assert "cannot be read" in result.stderr


def test_this_repository_prints_at_most_sixty_lines_ending_on_its_newest_lesson():
    result = printed(REPO_ROOT / "lessons.md")
    newest = (REPO_ROOT / "lessons.md").read_text(encoding="utf-8").splitlines()[-1]

    assert result.returncode == 0
    assert len(result.stdout.splitlines()) <= 60
    assert result.stdout.splitlines()[-1] == newest
