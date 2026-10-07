"""Fail if this branch rewrites or deletes a file already under archive/.

`docs/HOW_WE_WORK.md` §1 and §8: the old repository is archived, not rewritten
-- "Rewrite or refactor the archived repo. It is an archive." That was a
sentence. This is the gate.

The archive is append-only, not frozen. A file under `archive/` that exists on
the baseline ref (origin/main by default) must be in the head commit with its
baseline bytes intact: either the same bytes, or the baseline's bytes followed
by more, the way the ledgers grow under `src/append_check.py`. The append is
allowed only when the baseline ends in a newline, so the new content starts on
a line of its own and no line already in the archive is finished differently.
`archive/lessons_enforced.md` is the file that grows this way: `lessons.md`'s
header and `docs/HOW_WE_WORK.md` §1 principle 12 say a lesson a script comes to
enforce moves there, and a gate that froze every archived byte would forbid the
procedure the rule it holds describes (the 2026-09-06 append-check lesson, in
that same file). Any other byte change -- a line rewritten, removed or inserted
above the end -- is refused, and so is a deletion. A new file under `archive/`
passes: moving a retired piece into the archive, or recording what left a live
file there, adds to the archive without rewriting it. It is the same shape as
`src/append_check.py` for `runs/`, `rules/`, `events/` and `history/`, kept
apart because those four are the prediction record and the archive is not.

    python3.12 -m src.archive_check [--baseline origin/main]

Exit 0 clean, 1 a rewritten or deleted file (one line each on stderr), 2 the
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


def _blob(sha: str) -> bytes:
    return subprocess.run(
        ("git", "cat-file", "blob", sha), capture_output=True, check=True
    ).stdout


def is_pure_append(old_sha: str, new_sha: str) -> bool:
    """The new bytes are the old bytes, ending in a newline, with more after them."""
    old = _blob(old_sha)
    return old.endswith(b"\n") and _blob(new_sha).startswith(old)


def violations(baseline: str, head: str = "HEAD") -> list[str]:
    base_files = _archive_tree(baseline)
    head_files = _archive_tree(head)
    found = []
    for path, blob in sorted(base_files.items()):
        if path not in head_files:
            found.append(f"deleted: {path}")
        elif head_files[path] != blob and not is_pure_append(blob, head_files[path]):
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
        print(f"archive_check: {len(found)} archived file(s) rewritten or deleted against "
              f"{args.baseline}; the archive is appended to, never rewritten:", file=sys.stderr)
        for line in found:
            print(f"  {line}", file=sys.stderr)
        return FOUND
    print(f"archive_check: clean against {args.baseline}")
    return 0


if __name__ == "__main__":
    raise SystemExit(interpreter_pin.enforce() or main())
