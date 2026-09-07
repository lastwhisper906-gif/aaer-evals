"""Fail if this branch modifies or deletes a published file.

Published means: anything under runs/, rules/ or events/ that already exists on
the baseline ref (origin/main by default). Those three directories are
append-only: existing content is never changed or deleted. A correction is a new
file plus one ledger line.

Appending to the end of a ledger file is allowed, and a .jsonl ledger is the one
published file that legitimately grows: it passes as long as its new bytes begin
with its old bytes. Rewriting or truncating a line that was already published
fails like any other change to existing content.

Everything under those three prefixes is a record. Documentation about them
lives in docs/, because a file inside an append-only directory can never be
corrected.

Run it before pytest. A violation is not a test failure to be triaged later --
it means the prediction record is damaged, and the cycle stops.

    python -m src.append_check [--baseline origin/main]

Exit 0 clean, 1 violation, 2 the baseline ref could not be resolved, 3 the wrong
interpreter.

One-time exemption: a published path that is absent from the head tree but
present at archive/<same path> passes. That is the 2026-09-06 relocation of the
old experiment into archive/. The exemption is on the path and not on the
content, because origin/main sits 171 commits behind the archived tip and the
old project legitimately changed its own files in between; what pins that
content is tag archive-v1, not this check. Once the relocation has merged, no
protected path exists on main outside archive/, so this branch stops matching
anything.
"""

from __future__ import annotations

import argparse
import subprocess
import sys

from src import interpreter_pin

PROTECTED = ("runs/", "rules/", "events/")


def _git(*args: str) -> str:
    return subprocess.run(
        ("git", *args), capture_output=True, text=True, check=True
    ).stdout


def _blob(sha: str) -> bytes:
    return subprocess.run(
        ("git", "cat-file", "blob", sha), capture_output=True, check=True
    ).stdout


def _is_pure_append(old_sha: str, new_sha: str) -> bool:
    """A ledger may grow at the end and nowhere else."""
    return _blob(new_sha).startswith(_blob(old_sha))


def _tree(ref: str) -> dict[str, str]:
    """Map path -> blob hash for every protected file in ref."""
    out = _git("ls-tree", "-r", "--format=%(objectname) %(path)", ref)
    files = {}
    for line in out.splitlines():
        blob, _, path = line.partition(" ")
        if path.startswith(PROTECTED):
            files[path] = blob
    return files


def violations(baseline: str, head: str = "HEAD") -> list[str]:
    base_files = _tree(baseline)
    head_files = _tree(head)
    # The exemption needs the whole head tree, not just its protected part.
    relocated = {
        line.partition(" ")[2]
        for line in _git("ls-tree", "-r", "--format=%(objectname) %(path)", head).splitlines()
    }
    found = []
    for path, blob in sorted(base_files.items()):
        if head_files.get(path) == blob:
            continue
        if path in head_files:
            if path.endswith(".jsonl") and _is_pure_append(blob, head_files[path]):
                continue
            found.append(f"modified: {path}")
        elif f"archive/{path}" in relocated:
            continue  # the one-time archive relocation
        else:
            found.append(f"deleted: {path}")
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", default="origin/main")
    parser.add_argument("--head", default="HEAD")
    args = parser.parse_args(argv)

    try:
        _git("rev-parse", "--verify", f"{args.baseline}^{{commit}}")
    except subprocess.CalledProcessError:
        print(
            f"append_check: baseline ref {args.baseline!r} does not resolve. "
            "Fetch it before running -- an unresolvable baseline is not a pass.",
            file=sys.stderr,
        )
        return 2

    found = violations(args.baseline, args.head)
    if found:
        print(
            f"append_check: the prediction record is damaged "
            f"({len(found)} published file(s) changed against {args.baseline}):",
            file=sys.stderr,
        )
        for line in found:
            print(f"  {line}", file=sys.stderr)
        print(
            "runs/, rules/ and events/ are append-only. "
            "A correction is a new file plus one ledger line.",
            file=sys.stderr,
        )
        return 1

    print(f"append_check: clean against {args.baseline}")
    return 0


if __name__ == "__main__":
    # The pin comes first, before argument parsing and before any git call: a
    # result from an unpinned interpreter is not worth producing. It sits here
    # rather than inside main() so main() stays importable and testable on
    # whatever interpreter is running the tests.
    raise SystemExit(interpreter_pin.enforce() or main())
