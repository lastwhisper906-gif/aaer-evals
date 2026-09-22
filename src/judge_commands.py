"""Every judge command in the task list has to name an interpreter that runs it.

On 2026-09-13 six of six reproduce-lens runs exited 1 with `No module named
pytest` before collecting a single test. Every judge line in
`docs/next_cycle_tasks.md` was written `python3.12 -m pytest ...`, and bare
`python3.12` on this machine is `/opt/homebrew/opt/python@3.12/bin/python3.12`,
which has no site-packages for this project. Each of those six runs was rescued
by the lens substituting the project's own interpreter, and it was that
substitution -- not the command in the ledger -- that produced every number the
lens reported. A judge nobody can run is not a judge, and six results that
looked like judgements were the substitution's.

`Makefile` carried the same default, `PYTHON ?= python3.12`, which is why the
stop-time hook overrides it on every call and why nobody had noticed.

So the accepted interpreter is the project's own, `.venv/bin/python`, named in
both places. This module reads the command lines back out of the file and says
which ones name something else.

What counts as a judge command
------------------------------

Any backticked span in the file that runs pytest: the span has to contain
`-m pytest`. That is deliberately wider than the judge field, because the same
mistake in a note or a state line is the same mistake. A backticked
`python3.12` that is not running pytest is prose about the interpreter -- the
paragraph above quotes it twice -- and is left alone.

Two questions, and they are different
-------------------------------------

* **Does the command name the accepted interpreter?** A question about the
  text, answerable anywhere, including in continuous integration where no
  virtual environment exists. This is what `problems` answers.
* **Does that interpreter import pytest here?** A question about this machine,
  answerable only where the interpreter is installed. This is what
  `imports_pytest` answers, and it returns `None` where there is nothing to ask.

Keeping them apart is the point. Continuous integration runs `make check
PYTHON=python` against an interpreter it installed itself and has no `.venv` at
all; a check that conflated the two would either fail there for the wrong reason
or be switched off, and a check switched off is how the original hole stayed
open for a week.

    python3.12 -m src.judge_commands docs/next_cycle_tasks.md

Exit 0 and no output when every command names the accepted interpreter, 1 when
one does not, 3 on the wrong interpreter.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

try:
    from src import interpreter_pin
except ImportError:  # invoked as a plain script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import interpreter_pin

FOUND = 1

# The project's own interpreter, relative to the repository root. A worktree
# symlinks `.venv` to the main checkout's, so the same spelling runs in both.
ACCEPTED = ".venv/bin/python"

# A backticked span. The file writes every command inside one.
BACKTICKED = re.compile(r"`([^`]+)`")

RUNS_PYTEST = "-m pytest"


def judge_commands(text: str) -> list[tuple[int, str]]:
    """Every backticked command in the file that runs pytest, with its line."""
    found = []
    for number, line in enumerate(text.splitlines(), start=1):
        for span in BACKTICKED.finditer(line):
            command = span.group(1).strip()
            if RUNS_PYTEST in command:
                found.append((number, command))
    return found


def interpreter_of(command: str) -> str:
    """The interpreter a `<something> -m pytest ...` command names."""
    head = command.split(RUNS_PYTEST)[0].split()
    if not head:
        raise ValueError(f"{command!r} runs pytest with no interpreter in front of it")
    return head[-1]


def problems(text: str, *, path: str = "docs/next_cycle_tasks.md") -> list[str]:
    """One line per judge command naming an interpreter that is not the accepted one."""
    found = []
    for number, command in judge_commands(text):
        named = interpreter_of(command)
        if named != ACCEPTED:
            found.append(
                f"{path}:{number}: the judge names {named!r}, which is not {ACCEPTED!r}"
            )
    return found


def imports_pytest(interpreter: str, *, root: Path | None = None) -> bool | None:
    """True, False, or None when that interpreter is not on this machine."""
    here = Path.cwd() if root is None else root
    path = Path(interpreter)
    resolved = path if path.is_absolute() else here / path
    if not resolved.exists():
        return None
    result = subprocess.run(
        [str(resolved), "-c", "import pytest"], capture_output=True, text=True
    )
    return result.returncode == 0


def main(argv: list[str] | None = None) -> int:
    wrong_interpreter = interpreter_pin.enforce()
    if wrong_interpreter:
        return wrong_interpreter
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("path", type=Path)
    args = parser.parse_args(argv)
    found = problems(args.path.read_text(encoding="utf-8"), path=str(args.path))
    for line in found:
        print(line, file=sys.stderr)
    return FOUND if found else 0


if __name__ == "__main__":
    raise SystemExit(main())
