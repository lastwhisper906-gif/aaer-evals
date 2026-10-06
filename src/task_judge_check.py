"""Fail when the work list holds an open item with no judge.

`CLAUDE.md`: "Work with no judge (test, schema, check) is not a task. Leave it as
'needs judgment'." The two lists that hold the work state the row shape in their
own headers, and this reads each row against it:

* `docs/next_cycle_tasks.md` -- `[ ] title · builds · judge · expected value from
  · PR`. Every `[ ] ` row under `## This cycle` or `## Next cycle` has at least
  three parts separated by ` · `, and its third part, the judge, is not empty.
  Rows under the other headings (landed, needs judgment, closed) are history and
  are not read.
* `queue.md`, when it exists -- `[ ] what · eval command that must pass · depends
  on`. Every `[ ] ` row under `## Open` has a second part carrying a command in
  backticks. Its own header says it: "An item with no eval command is not an
  item".

What it cannot see: whether the judge named is a good one. It says that a judge
is named, which is the line between a task and a wish.

    python3.12 -m src.task_judge_check [--tasks docs/next_cycle_tasks.md] [--queue queue.md]

Exit 0 and no output when clean, 1 when it found a row (one line each on stderr,
`path:line: reason`), 2 when neither list is there, 3 on the wrong interpreter.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    from src import interpreter_pin
except ImportError:  # invoked as a plain script: python3.12 src/task_judge_check.py
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import interpreter_pin

FOUND = 1
CANNOT_RUN = 2

OPEN_ROW = "[ ] "
FIELD = " · "
TASK_SECTIONS = frozenset({"## This cycle", "## Next cycle"})
QUEUE_SECTION = "## Open"
COMMAND = re.compile(r"`[^`]+`")


def _rows(path: Path, sections: frozenset[str]):
    section = ""
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("## "):
            section = line.strip()
        elif section in sections and line.startswith(OPEN_ROW):
            yield number, line.split(FIELD)


def task_findings(tasks: Path) -> list[str]:
    """One line per open task-list row whose judge is missing."""
    return [f"{tasks}:{number}: an open item names no judge"
            for number, parts in _rows(tasks, TASK_SECTIONS)
            if len(parts) < 3 or not parts[2].strip()]


def queue_findings(queue: Path) -> list[str]:
    """One line per open queue row with no eval command."""
    return [f"{queue}:{number}: an open item names no eval command"
            for number, parts in _rows(queue, frozenset({QUEUE_SECTION}))
            if len(parts) < 2 or COMMAND.search(parts[1]) is None]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fail on an open item with no judge.")
    parser.add_argument("--tasks", type=Path, default=Path("docs/next_cycle_tasks.md"))
    parser.add_argument("--queue", type=Path, default=Path("queue.md"))
    args = parser.parse_args(argv)

    if not args.tasks.is_file() and not args.queue.is_file():
        print(f"task_judge_check: neither {args.tasks} nor {args.queue} is there -- a "
              "list that cannot be read is not a clean list", file=sys.stderr)
        return CANNOT_RUN

    found = []
    if args.tasks.is_file():
        found += task_findings(args.tasks)
    if args.queue.is_file():
        found += queue_findings(args.queue)
    for line in found:
        print(line, file=sys.stderr)
    return FOUND if found else 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
