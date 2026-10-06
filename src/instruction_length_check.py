"""Fail when `CLAUDE.md` grows past its cap.

`docs/HOW_WE_WORK.md` §4 caps `CLAUDE.md` at 22 lines, because the file is read
in full at the start of every session and a rules file nobody finishes is a
rules file nobody follows. The owner's research note of 2026-10-06
(`docs/structure_changes.md`) says the same from the other side: prose rules are
followed inconsistently, so keep instructions to about a hundred lines. The cap
was a sentence; this makes it a gate, so a rule that cannot fit replaces a line
rather than appending one.

    python3.12 -m src.instruction_length_check [--file CLAUDE.md] [--cap 22]

Exit 0 and no output when within the cap, 1 when over it (one line on stderr), 2
when the file is not there, 3 on the wrong interpreter.
"""

from __future__ import annotations

import argparse
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


def line_count(path: Path) -> int:
    """Lines as `wc -l` would print them, plus a last line with no newline."""
    return len(path.read_text(encoding="utf-8").splitlines())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fail when CLAUDE.md passes its cap.")
    parser.add_argument("--file", type=Path, default=Path("CLAUDE.md"))
    parser.add_argument("--cap", type=int, default=CAP)
    args = parser.parse_args(argv)

    if not args.file.is_file():
        print(f"instruction_length_check: {args.file} is not there", file=sys.stderr)
        return CANNOT_RUN

    count = line_count(args.file)
    if count > args.cap:
        print(f"{args.file}:{count}: {count} lines, over the cap of {args.cap}; "
              "replace a line rather than append one", file=sys.stderr)
        return FOUND
    return 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
