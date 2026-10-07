"""Fail when the owner's inbox holds a row that waits, or a sign-off file exists.

`CLAUDE.md`: "Never create a state that waits for the owner's signature. Proceed
with the default and leave one line." `docs/HOW_WE_WORK.md` §1 says the same as
two principles -- no sign-off queue, no pending-decisions file, and everything
has a default. Both were sentences. This is the check that makes them a gate.

The one place the owner is asked anything is `docs/needs_judgment.md`, and its
own header states the row shape:

    what is unsettled · the default in force today · what changes when the owner decides

So the check reads two things there, and one thing in the tree:

1. **Every open row names its default.** A line beginning `[ ] ` has at least
   three parts separated by ` · `, and its second part -- the default in force
   -- is not empty. An open row with no default is a signature queue under a new
   name (`lessons.md`, 2026-09-08 and 2026-09-13).
2. **Every settled row says `default:` and what it is.** Under the heading
   `## Settled by default`, a line beginning `- ` carries `default:` followed by
   text.
3. **No sign-off file.** No file outside `archive/` is named as a queue of
   decisions waiting on someone: its name, lowercased with everything but
   letters removed, does not contain `pendingdecision`, `decisionspending`,
   `ownerqueue`, `signoff` or `approvalqueue`. The archived project had
   `DECISIONS_PENDING.md` and `OWNER_QUEUE.md`; they stay where they are.

An inbox that is there but yields no row at all -- no `[ ] ` row under any
heading and no `- ` row under `## Settled by default` -- is refused, not passed:
a renamed section (`## Blocked`) would otherwise read as prose and the gate
would pass having examined nothing.

What it cannot see: whether a session actually stopped and waited. A file can
only show the states somebody wrote down, and that is what this reads.

    python3.12 -m src.owner_inbox_check [--inbox docs/needs_judgment.md] [--root .]

Exit 0 and no output when clean, 1 when it found a row or a file (one line each
on stderr, `path:line: reason`), 2 when the inbox is not there or yields no row,
3 on the wrong interpreter.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

try:
    from src import interpreter_pin
except ImportError:  # invoked as a plain script: python3.12 src/owner_inbox_check.py
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import interpreter_pin

FOUND = 1
CANNOT_RUN = 2

OPEN_ROW = "[ ] "
SETTLED_HEADING = "## Settled by default"
SETTLED_ROW = "- "
FIELD = " · "
DEFAULT_MARK = re.compile(r"default:\s*\S")

SIGN_OFF_NAMES = ("pendingdecision", "decisionspending", "ownerqueue", "signoff",
                  "approvalqueue")
SKIP_DIRECTORIES = frozenset({".git", ".venv", "__pycache__", ".pytest_cache",
                              "node_modules", "archive", "worktrees", "fixtures"})


def rows(inbox: Path) -> list[tuple[int, str, str]]:
    """Every row the check reads, as (line number, "open" or "settled", the line)."""
    found = []
    section = ""
    for number, line in enumerate(inbox.read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("## "):
            section = line.strip()
        elif line.startswith(OPEN_ROW):
            found.append((number, "open", line))
        elif section == SETTLED_HEADING and line.startswith(SETTLED_ROW):
            found.append((number, "settled", line))
    return found


def no_rows(inbox: Path) -> str:
    """The refusal for an inbox that yields nothing under the headings read."""
    return (f"{inbox}: no rows under any heading as `{OPEN_ROW.strip()} ` or under "
            f"{SETTLED_HEADING} as `{SETTLED_ROW.strip()} `; a renamed section is not an "
            "empty list")


def inbox_findings(inbox: Path) -> list[str]:
    """One line per inbox row that names no default."""
    found = []
    for number, kind, line in rows(inbox):
        if kind == "open":
            parts = line.split(FIELD)
            if len(parts) < 3 or not parts[1].strip():
                found.append(f"{inbox}:{number}: an open row names no default in force")
        elif DEFAULT_MARK.search(line) is None:
            found.append(f"{inbox}:{number}: a settled row does not say its default")
    return found


def sign_off_files(root: Path) -> list[str]:
    """One line per file outside archive/ named as a queue of decisions."""
    found = []
    for parent, directories, names in os.walk(root):
        directories[:] = sorted(d for d in directories if d not in SKIP_DIRECTORIES)
        for name in sorted(names):
            letters = re.sub(r"[^a-z]", "", name.lower())
            if any(word in letters for word in SIGN_OFF_NAMES):
                path = Path(parent) / name
                found.append(f"{path.relative_to(root)}:0: a file named as a sign-off queue")
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fail on an inbox row that waits.")
    parser.add_argument("--inbox", type=Path, default=Path("docs/needs_judgment.md"))
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args(argv)

    if not args.inbox.is_file():
        print(f"owner_inbox_check: {args.inbox} is not there -- an inbox that cannot be "
              "read is not a clean inbox", file=sys.stderr)
        return CANNOT_RUN

    if not rows(args.inbox):
        print(no_rows(args.inbox), file=sys.stderr)
        return CANNOT_RUN

    found = inbox_findings(args.inbox) + sign_off_files(args.root)
    for line in found:
        print(line, file=sys.stderr)
    return FOUND if found else 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
