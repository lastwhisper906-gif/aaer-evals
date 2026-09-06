"""One pinned interpreter: Python 3.12.

Every entry point a person or a scheduled task can run calls enforce() before it
does anything else. CI pins 3.12 too, but CI is not where this bit: a gate was
once run on 3.12 in CI and 3.14 on the machine, one test failed on 3.14 alone,
and the failure was nearly reported as real.

The guard belongs in main(), not at import time, so the module stays importable
and testable on whatever interpreter happens to be running the tests.
"""

from __future__ import annotations

import sys

REQUIRED = (3, 12)
WRONG_INTERPRETER = 3


def mismatch(version_info: tuple[int, ...] | None = None) -> str | None:
    """One plain line if this is not the pinned interpreter, otherwise None."""
    found = tuple(version_info or sys.version_info)[:2]
    if found == REQUIRED:
        return None
    return (
        f"This runs on Python {REQUIRED[0]}.{REQUIRED[1]} only, and this is "
        f"Python {found[0]}.{found[1]}. A result from another interpreter "
        f"cannot be trusted. Re-run with python{REQUIRED[0]}.{REQUIRED[1]}."
    )


def enforce(version_info: tuple[int, ...] | None = None) -> int:
    """0 when the interpreter is the pinned one, otherwise the exit code."""
    message = mismatch(version_info)
    if message is None:
        return 0
    print(message, file=sys.stderr)
    return WRONG_INTERPRETER
