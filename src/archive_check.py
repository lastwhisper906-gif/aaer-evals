"""Fail if this branch changes or deletes a file already under archive/.

`docs/HOW_WE_WORK.md` §1 and §8: the old repository is archived, not rewritten
-- "Rewrite or refactor the archived repo. It is an archive." That was a
sentence. This is the gate.

A file under `archive/` that exists on the baseline ref (origin/main by
default) must be in the head commit with the same bytes. A new file under
`archive/` passes: moving a retired piece into the archive, or recording what
left a live file there, adds to the archive without rewriting it. It is the
same shape as `src/append_check.py` for `runs/`, `rules/`, `events/` and
`history/`, kept apart because those four are the prediction record and the
archive is not.

    python3.12 -m src.archive_check [--baseline origin/main]

Exit 0 clean, 1 a changed or deleted file (one line each on stderr), 2 the
baseline ref could not be resolved, 3 the wrong interpreter.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

try:
    from src import interpreter_pin
except ImportError:  # invoked as a plain script: python3.12 src/archive_check.py
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src import interpreter_pin

ARCHIVE = "archive/"
FOUND = 1
CANNOT_RUN = 2


def _archive_tree(ref: str) -> dict[str, str]:
    """Map path -> blob hash for every file under archive/ in ref."""
    out = subprocess.run(
        ("git", "ls-tree", "-r", "--format=%(objectname) %(path)", ref, "--", ARCHIVE),
        capture_output=True, text=True, check=True,
    ).stdout
    files = {}
    for line in out.splitlines():
        blob, _, path = line.partition(" ")
        files[path] = blob
    return files


def violations(baseline: str, head: str = "HEAD") -> list[str]:
    base_files = _archive_tree(baseline)
    head_files = _archive_tree(head)
    found = []
    for path, blob in sorted(base_files.items()):
        if path not in head_files:
            found.append(f"deleted: {path}")
        elif head_files[path] != blob:
            found.append(f"modified: {path}")
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fail on a rewrite of archive/.")
    parser.add_argument("--baseline", default="origin/main")
    parser.add_argument("--head", default="HEAD")
    args = parser.parse_args(argv)

    try:
        subprocess.run(("git", "rev-parse", "--verify", f"{args.baseline}^{{commit}}"),
                       capture_output=True, check=True)
    except subprocess.CalledProcessError:
        print(f"archive_check: baseline ref {args.baseline!r} does not resolve. Fetch it "
              "before running -- an unresolvable baseline is not a pass.", file=sys.stderr)
        return CANNOT_RUN

    found = violations(args.baseline, args.head)
    if found:
        print(f"archive_check: {len(found)} archived file(s) changed against "
              f"{args.baseline}; the archive is added to, never rewritten:", file=sys.stderr)
        for line in found:
            print(f"  {line}", file=sys.stderr)
        return FOUND
    print(f"archive_check: clean against {args.baseline}")
    return 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
