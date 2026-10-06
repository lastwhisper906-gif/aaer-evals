"""PreToolUse hook on Bash: refuse a command that writes under evals/.

evals/ is the owner's (CLAUDE.md). The permission rules deny the Edit and Write
tools there; this closes the shell. It reads the hook's JSON on stdin and exits 2,
which blocks the call and hands the reason back, when the command:
- redirects into evals/ (`>` or `>>`), or tees into it;
- edits a file there in place (`sed -i`, `perl -i`);
- moves, copies, links, removes, truncates or touches anything there;
- checks out, restores, removes or moves evals/ with git;
- runs inside evals/ (`cd evals`) and then writes.

`make eval` is allowed: it appends to evals/scoreboard.jsonl, the one write the owner
gave it. Reading is always allowed. A shell can always be talked around (a script
written elsewhere, then run); the CI guard (src/eval_guard.py) is the backstop that
no command line reaches. Standard library only: it runs before anything is installed.
"""

from __future__ import annotations

import json
import re
import sys

TARGET = r"(?:\./)?(?:[\w./-]*/)?evals(?:/|\b)"
WRITES = [
    re.compile(r">{1,2}\s*['\"]?" + TARGET),                          # > evals/x, >> evals/x
    re.compile(r"\btee\b[^|;&]*\s['\"]?" + TARGET),                    # tee [-a] evals/x
    re.compile(r"\b(?:sed|perl)\b[^|;&]*\s-i\b[^|;&]*" + TARGET),      # sed -i ... evals/x
    re.compile(r"\b(?:mv|cp|rm|rmdir|ln|install|truncate|touch|chmod|chown|mkdir|rsync|dd)"
               r"\b[^|;&]*\s['\"]?" + TARGET),
    re.compile(r"\bgit\s+(?:checkout|restore|rm|mv|apply|am|stash\s+pop)\b[^|;&]*" + TARGET),
    re.compile(r"\bcd\s+['\"]?" + TARGET + r"[^;&|]*[;&|]+[^;&|]*(?:>|\btee\b|\brm\b|\bmv\b"
               r"|\bcp\b|\bsed\s+-i)"),
]
ALLOWED = re.compile(r"^\s*make\s+eval(?:-quick)?\b[^;&|>]*$")


def refused(command: str) -> str | None:
    """The reason this command is refused, or None."""
    if ALLOWED.match(command):
        return None
    for pattern in WRITES:
        match = pattern.search(command)
        if match:
            return (f"evals/ is the owner's and this command writes under it "
                    f"({match.group().strip()!r}). Propose the change as a row in "
                    "docs/needs_judgment.md instead.")
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return 0
    command = ((payload.get("tool_input") or {}).get("command") or "")
    reason = refused(command)
    if reason:
        print(reason, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
