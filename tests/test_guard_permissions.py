"""The permission rules on the Edit and Write tools, two-sided (see tests/test_guards.py).

Committed with the rules themselves, in the last commit of the pull request that
creates evals/: that session had to write evals/ before it could deny it.
"""

from __future__ import annotations

import fnmatch
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _deny() -> list[str]:
    settings = json.loads((REPO / ".claude" / "settings.json").read_text(encoding="utf-8"))
    return (settings.get("permissions") or {}).get("deny") or []


def _denied(tool: str, path: str) -> bool:
    """A tool rule `Tool(glob)` with `**` reading as any depth, as Claude Code reads it."""
    for rule in _deny():
        name, _, pattern = rule.partition("(")
        if name == tool and fnmatch.fnmatch(path, pattern.rstrip(")")):
            return True
    return False


def test_the_permission_rules_deny_editing_and_writing_under_evals():
    assert _denied("Edit", "evals/regression/mechanical.py")
    assert _denied("Write", "evals/golden/cases/new_case.yaml")


def test_the_permission_rules_leave_everything_else_alone():
    assert not _denied("Edit", "src/calculator.py")
    assert not _denied("Write", "queue.md")
    assert not _denied("Edit", "evalsish/notes.md")


