"""PreToolUse hook on Bash for the improvement loop's session: refuse a command
that writes to a fenced path (`docs/improve_loop.md`, the first table).

The fences are what judges the loop and what records it: the gates, the
measurement, the graders, the expected values, the records, the hooks and
settings, the workflows. The session's settings deny the Edit and Write tools
there (`--deny-rules` prints those rules, so the list lives here once); this
closes the shell the same way `guard_evals.py` closes it for evals/, and with
the same shapes of command, so one reading covers both. Standard library only.
"""

from __future__ import annotations

import json
import re
import sys

# A path ending in / is a directory and everything under it; any other is a file.
FENCED = (
    "evals/", "runs/", "rules/", "events/", "history/",
    "tests/fixtures/", "tests/expected_values.py",
    "src/analysis_check.py", "src/quote_gate.py", "src/plain_name_check.py",
    "src/cutoff_guard.py", "src/extraction_checks.py", "src/calculator.py",
    "src/append_check.py", "src/eval_guard.py", "src/grade_run.py",
    "src/improve/measure.py", "src/improve/mine.py",
    ".claude/agents/analysis-grader.md", ".claude/hooks/", ".claude/settings.json",
    ".github/", "docs/improve/ledger.jsonl",
)


def _target() -> str:
    parts = []
    for path in FENCED:
        if path.endswith("/"):
            parts.append(re.escape(path.rstrip("/")) + r"(?:/|\b)")
        else:
            parts.append(re.escape(path) + r"\b")
    return r"(?:\./)?(?:" + "|".join(parts) + ")"


TARGET = _target()
WRITES = [
    re.compile(r">{1,2}\s*['\"]?" + TARGET),
    re.compile(r"\btee\b[^|;&]*\s['\"]?" + TARGET),
    re.compile(r"\b(?:sed|perl)\b[^|;&]*\s-i\b[^|;&]*" + TARGET),
    re.compile(r"\b(?:mv|cp|rm|rmdir|ln|install|truncate|touch|chmod|chown|mkdir|rsync|dd)"
               r"\b[^|;&]*\s['\"]?" + TARGET),
    re.compile(r"\bgit\s+(?:checkout|restore|rm|mv|apply|am|stash\s+pop)\b[^|;&]*" + TARGET),
    re.compile(r"\bcd\s+['\"]?" + TARGET + r"[^;&|]*[;&|]+[^;&|]*(?:>|\btee\b|\brm\b|\bmv\b"
               r"|\bcp\b|\bsed\s+-i)"),
]
# `src.improve.measure run` copies runs outside the tree and the graders append
# to evals/scoreboard.jsonl: both read the fenced paths and write elsewhere.
ALLOWED = re.compile(r"^\s*(?:make\s+eval(?:-quick)?(?:\s+PYTHON=[A-Za-z0-9_./-]*python3?(?:\.\d+)?)?"
                     r"|[A-Za-z0-9_./-]*python3?(?:\.\d+)?\s+-m\s+src\.improve\.(?:measure|mine)\b[^;&|>]*)\s*$")


def refused(command: str) -> str | None:
    """The reason this command is refused, or None."""
    if ALLOWED.match(command):
        return None
    for pattern in WRITES:
        match = pattern.search(command)
        if match:
            return (f"a fenced path: the improvement loop reads it and never writes it "
                    f"({match.group().strip()!r}). A change there is the owner's: a row in "
                    "docs/needs_judgment.md with the patch in the report (docs/improve_loop.md).")
    return None


def deny_rules() -> list[str]:
    """The permission rules that deny the Edit and Write tools on every fence."""
    rules = []
    for path in FENCED:
        pattern = path + "**" if path.endswith("/") else path
        rules += [f"Edit({pattern})", f"Write({pattern})"]
    return rules


def main(argv: list[str]) -> int:
    if argv[1:] == ["--deny-rules"]:
        print(json.dumps(deny_rules()))
        return 0
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
    sys.exit(main(sys.argv))
