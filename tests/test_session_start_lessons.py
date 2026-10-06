"""The session-start printout: the header, then the newest lessons, at most sixty lines.

The lessons files are planted by this file, and the expected printout is worked
out by hand from the planted shape: a four-line header leaves fifty-six lines,
one of which says how many older lessons were left out, so a hundred lessons
print as the header, that line, and lessons 46 to 100.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "tools" / "session_start_lessons.sh"
HEADER = ["# Lessons", "", "One line per mistake, newest last.", ""]


def lesson(n: int) -> str:
    return f"2026-09-{1 + n % 28:02d} lesson number {n}, written in the order it was learned."


def plant(tmp_path: Path, count: int) -> Path:
    path = tmp_path / "lessons.md"
    path.write_text("\n".join(HEADER + [lesson(n) for n in range(1, count + 1)]) + "\n",
                    encoding="utf-8")
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
