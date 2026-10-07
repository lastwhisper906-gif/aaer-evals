"""Fail when `CLAUDE.md` grows past its cap, or a lesson in `lessons.md` has no date.

`docs/HOW_WE_WORK.md` §4 caps `CLAUDE.md` at 22 lines, because the file is read
in full at the start of every session and a rules file nobody finishes is a
rules file nobody follows. The owner's research note of 2026-10-06
(`docs/structure_changes.md`) says the same from the other side: prose rules are
followed inconsistently, so keep instructions to about a hundred lines. The cap
was a sentence; this makes it a gate, so a rule that cannot fit replaces a line
rather than appending one.

The second rule is the lessons files' shape. `tools/session_start_lessons.sh`
tells a lesson from the header by its date, YYYY-MM-DD and a space, and prints
the newest ones; a lesson appended without a date would be a continuation of the
lesson before it there, printed but counted as part of another lesson, and
nothing would say so. This refuses it instead: after the header (everything
above the first dated line), every line that is not blank and does not start
with whitespace must start with a date. A line that starts with whitespace
belongs to the lesson above it: `archive/lessons_enforced.md` puts under each
lesson one indented line naming what enforces it, and a wrapped line is written
the same way.

The third rule is that `CLAUDE.md`'s parentheses name real files. Its header
says every rule names what enforces it, and a path that resolves to nothing is
a rule naming nothing, back in the file the header is about. So every
path-shaped token in `CLAUDE.md` -- a token containing `/` that ends in `.py`,
`.sh`, `.md` or `.json`, or a directory written with its trailing slash like
`evals/` -- must exist in the tree, relative to the directory `CLAUDE.md` is
in. A rule whose judge is still on another branch fails here until that branch
merges, which is the point: the file says what is true at the commit it is in.

    python3.12 -m src.instruction_length_check [--file CLAUDE.md] [--cap 22]
        [--lessons lessons.md archive/lessons_enforced.md] [--paths | --no-paths]

Exit 0 and no output when within the cap, every lesson is dated and every path
named exists, 1 when not (one line on stderr per finding), 2 when a file is not
there, 3 on the wrong interpreter. The lessons paths default to the
repository's own two files, so the gate reads them from wherever it is run.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    from src import interpreter_pin
except ImportError:  # invoked as a plain script: python3.12 src/instruction_length_check.py
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import interpreter_pin

FOUND = 1
CANNOT_RUN = 2
CAP = 22
REPO_ROOT = Path(__file__).resolve().parent.parent
LESSONS = (REPO_ROOT / "lessons.md", REPO_ROOT / "archive" / "lessons_enforced.md")
DATED = re.compile(r"^\d{4}-\d{2}-\d{2} ")
PATH_SUFFIXES = (".py", ".sh", ".md", ".json")
DIRECTORY = re.compile(r"^[\w.\-]+(/[\w.\-]+)*/$")
TOKEN_EDGE = "()[]{},;:`'\"<>"


def named_paths(path: Path) -> list[tuple[int, str]]:
    """Every (line number, token) in the file that is shaped like a path."""
    found = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        for raw in line.split():
            token = raw.strip(TOKEN_EDGE)
            if "/" not in token or "://" in token:
                continue
            if token.endswith(PATH_SUFFIXES) or DIRECTORY.match(token):
                found.append((number, token))
    return found


def missing_paths(path: Path) -> list[tuple[int, str]]:
    """Every path the file names that does not exist, relative to the file's directory."""
    root = path.resolve().parent
    return [(number, token) for number, token in named_paths(path)
            if not (root / token).exists()]


def line_count(path: Path) -> int:
    """Lines as `wc -l` would print them, plus a last line with no newline."""
    return len(path.read_text(encoding="utf-8").splitlines())


def undated_lessons(path: Path) -> list[tuple[int, str]]:
    """Every (line number, line) after the header that starts a lesson without a date."""
    found = []
    started = False
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if DATED.match(line):
            started = True
        elif started and line.strip() and not line[0].isspace():
            found.append((number, line))
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fail when CLAUDE.md passes its cap or a lesson has no date.")
    parser.add_argument("--file", type=Path, default=Path("CLAUDE.md"))
    parser.add_argument("--cap", type=int, default=CAP)
    parser.add_argument("--lessons", type=Path, nargs="*", default=list(LESSONS))
    parser.add_argument("--paths", action=argparse.BooleanOptionalAction, default=True,
                        help="refuse a path CLAUDE.md names that is not in the tree (on by default)")
    args = parser.parse_args(argv)

    for path in [args.file, *args.lessons]:
        if not path.is_file():
            print(f"instruction_length_check: {path} is not there", file=sys.stderr)
            return CANNOT_RUN

    status = 0
    count = line_count(args.file)
    if count > args.cap:
        print(f"{args.file}:{count}: {count} lines, over the cap of {args.cap}; "
              "replace a line rather than append one", file=sys.stderr)
        status = FOUND
    for path in args.lessons:
        for number, line in undated_lessons(path):
            print(f"{path}:{number}: a lesson starts with its date, YYYY-MM-DD and a space; "
                  f"this line does not: {line}", file=sys.stderr)
            status = FOUND
    if args.paths:
        for number, token in missing_paths(args.file):
            print(f"{args.file}:{number}: names {token}, which is not in the tree; a rule "
                  "naming a file that is not there names nothing", file=sys.stderr)
            status = FOUND
    return status


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
