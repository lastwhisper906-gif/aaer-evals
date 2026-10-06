"""The CI guard on evals/: a pull request that touches the owner's graders needs the
owner's label.

It passes when:
- the base branch has no `evals/` yet (the pull request that creates it);
- the pull request carries the label `owner-approved-eval`, which only the owner adds;
- the only change under `evals/` is lines appended to `evals/scoreboard.jsonl`, the
  one file `make eval` writes.

Anything else under `evals/` fails it: a file added, changed, renamed or deleted.

    python3.12 -m src.eval_guard --base origin/main --head HEAD --labels "a,b"
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LABEL = "owner-approved-eval"
SCOREBOARD = "evals/scoreboard.jsonl"


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout


def _show(ref: str, path: str) -> str | None:
    done = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=REPO_ROOT,
                          capture_output=True, text=True)
    return done.stdout if done.returncode == 0 else None


def decide(changes: list[tuple[str, str]], labels: set[str], base_has_evals: bool,
           scoreboard_before: str | None, scoreboard_after: str | None) -> tuple[bool, str]:
    """(passes, why). `changes` is (status, path) for every path under evals/."""
    if not changes:
        return True, "nothing under evals/ changed"
    if not base_has_evals:
        return True, "the base has no evals/: this is the pull request that creates it"
    if LABEL in labels:
        return True, f"labelled {LABEL} by the owner"
    others = [(status, path) for status, path in changes if path != SCOREBOARD]
    if not others:
        before, after = scoreboard_before or "", scoreboard_after or ""
        if after.startswith(before) and (not before or before.endswith("\n")):
            return True, "only lines appended to evals/scoreboard.jsonl"
        return False, "evals/scoreboard.jsonl was changed, not appended to"
    return False, (f"{len(others)} path(s) under evals/ changed without the label {LABEL}: "
                   + ", ".join(f"{s} {p}" for s, p in others[:10]))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="refuse unlabelled changes to evals/")
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--labels", default="", help="comma-separated pull request labels")
    args = parser.parse_args(argv)
    merge_base = _git("merge-base", args.base, args.head).strip()
    lines = _git("diff", "--name-status", "--no-renames", merge_base, args.head, "--",
                 "evals/").splitlines()
    changes = [(line.split("\t", 1)[0], line.split("\t", 1)[1]) for line in lines if "\t" in line]
    base_has_evals = bool(_git("ls-tree", "--name-only", merge_base, "evals/").strip())
    ok, why = decide(changes, {l.strip() for l in args.labels.split(",") if l.strip()},
                     base_has_evals, _show(merge_base, SCOREBOARD), _show(args.head, SCOREBOARD))
    print(f"eval_guard: {'pass' if ok else 'FAIL'}: {why}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
