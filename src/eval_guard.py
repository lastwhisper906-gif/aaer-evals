"""The CI guard on evals/: a pull request that touches the owner's graders, or the
guard itself, needs the owner's label.

Guarded: everything under `evals/`; the files that decide whether the graders run
(this file, `.claude/hooks/guard_evals.py`, `.claude/settings.json`); and the model
grader's instructions and what it is shown (`.claude/agents/analysis-grader.md`,
`src/grade_run.py`). CI runs this file and the
graders from main's copies, never the branch's (`.github/workflows/ci.yml`).

It passes when:
- the base branch itself (not the merge base) has no `evals/` yet: the pull request
  that creates it;
- the pull request carries the label `owner-approved-eval`, which only the owner adds;
- the only change under `evals/` is lines appended to `evals/scoreboard.jsonl`, the
  one file `make eval` writes.

Anything else under `evals/` fails it: a file added, changed, renamed or deleted.

    python3.12 -m src.eval_guard --base origin/main --head HEAD --labels "a,b" \\
        --action labeled --label-added owner-approved-eval
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

LABEL = "owner-approved-eval"
SCOREBOARD = "evals/scoreboard.jsonl"
GUARDED = ("evals/", "src/eval_guard.py", ".claude/hooks/guard_evals.py",
           ".claude/agents/analysis-grader.md", "src/grade_run.py", ".claude/settings.json")


def _git(*args: str) -> str:
    # The working directory, not this file's: CI runs main's copy from outside the tree.
    return subprocess.run(["git", *args], cwd=Path.cwd(), capture_output=True, text=True,
                          check=True).stdout


def _show(ref: str, path: str) -> str | None:
    done = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=Path.cwd(),
                          capture_output=True, text=True)
    return done.stdout if done.returncode == 0 else None


def decide(changes: list[tuple[str, str]], labels: set[str], base_has_evals: bool,
           scoreboard_before: str | None, scoreboard_after: str | None,
           action: str = "labeled", label_added: str | None = None,
           labeled_by: str | None = None, owner: str | None = None) -> tuple[bool, str]:
    """(passes, why). `changes` is (status, path) for every guarded path changed.

    The label counts on exactly one run: the `labeled` run that adding it starts
    (`label_added` is the label that event added, `labeled_by` who added it, and it
    counts only when that is `owner`, the repository's owner). It does not count on a
    `synchronize` run, the one a later push starts, nor on `opened`, `reopened` or
    the adding of any other label, so a commit pushed after the owner labelled is
    red until the owner labels again (remove and re-add), and no later event
    revives the approval. The approval covers the head it was given on.
    """
    if not changes:
        return True, "nothing guarded changed"
    if not base_has_evals:
        return True, "the base has no evals/: this is the pull request that creates it"
    if LABEL in labels and action == "labeled" and label_added == LABEL:
        # GitHub lets anyone with triage access add a label; only the repository's
        # owner adding it is the owner's approval
        if owner and labeled_by == owner:
            return True, f"labelled {LABEL} by the owner {owner}"
        return False, (f"labelled {LABEL} by {labeled_by or 'nobody named'}, who is not the "
                       f"repository's owner {owner or '(no owner given)'}; the owner labels to approve")
    if LABEL in labels:
        return False, (f"labelled {LABEL}, but this run was not started by adding it "
                       f"({action}{': ' + label_added if label_added else ''}); the owner "
                       "labels again to approve this head")
    others = [(status, path) for status, path in changes if path != SCOREBOARD]
    if not others:
        before, after = scoreboard_before or "", scoreboard_after or ""
        if after.startswith(before) and (not before or before.endswith("\n")):
            return True, "only lines appended to evals/scoreboard.jsonl"
        return False, "evals/scoreboard.jsonl was changed, not appended to"
    return False, (f"{len(others)} guarded path(s) changed without the label {LABEL}: "
                   + ", ".join(f"{s} {p}" for s, p in others[:10]))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="refuse unlabelled changes to evals/")
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--labels", default="", help="comma-separated pull request labels")
    parser.add_argument("--action", default="labeled",
                        help="the pull_request event's action (opened, synchronize, labeled)")
    parser.add_argument("--label-added", default=None,
                        help="on a labeled event, the label that was added")
    parser.add_argument("--labeled-by", default=None, help="the login that added it")
    parser.add_argument("--owner", default=None, help="the repository owner's login")
    args = parser.parse_args(argv)
    merge_base = _git("merge-base", args.base, args.head).strip()
    lines = _git("diff", "--name-status", "--no-renames", merge_base, args.head, "--",
                 *GUARDED).splitlines()
    changes = [(line.split("\t", 1)[0], line.split("\t", 1)[1]) for line in lines if "\t" in line]
    # The base branch as it stands, never the merge base: a branch forked before
    # evals/ existed must not take the creating pull request's exemption.
    base_has_evals = bool(_git("ls-tree", "--name-only", args.base, "evals/").strip())
    ok, why = decide(changes, {l.strip() for l in args.labels.split(",") if l.strip()},
                     base_has_evals, _show(merge_base, SCOREBOARD), _show(args.head, SCOREBOARD),
                     action=args.action, label_added=args.label_added,
                     labeled_by=args.labeled_by, owner=args.owner)
    print(f"eval_guard: {'pass' if ok else 'FAIL'}: {why}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
