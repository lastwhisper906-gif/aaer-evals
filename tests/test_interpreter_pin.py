"""The pin has to refuse an unpinned interpreter, and the entry point has to use it."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from src import interpreter_pin

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_the_pinned_interpreter_passes():
    assert interpreter_pin.mismatch((3, 12, 12)) is None
    assert interpreter_pin.enforce((3, 12, 12)) == 0


@pytest.mark.parametrize("version", [(3, 11, 9), (3, 13, 0), (3, 14, 7), (4, 0, 0)])
def test_any_other_interpreter_is_refused(version, capsys):
    message = interpreter_pin.mismatch(version)
    assert message is not None
    assert f"{version[0]}.{version[1]}" in message
    assert "3.12" in message

    assert interpreter_pin.enforce(version) == interpreter_pin.WRONG_INTERPRETER
    assert interpreter_pin.WRONG_INTERPRETER != 0
    assert message in capsys.readouterr().err


def test_the_default_reads_the_live_interpreter(monkeypatch):
    monkeypatch.setattr(sys, "version_info", (3, 14, 7, "final", 0))
    assert interpreter_pin.enforce() == interpreter_pin.WRONG_INTERPRETER

    monkeypatch.setattr(sys, "version_info", (3, 12, 12, "final", 0))
    assert interpreter_pin.enforce() == 0


def _an_unpinned_interpreter() -> str | None:
    for name in ("python3.14", "python3.13", "python3.11", "python3.10"):
        found = shutil.which(name)
        if found:
            return found
    return None


def test_the_append_check_entry_point_refuses_before_it_does_anything():
    """Proof that the guard is wired in, not just written.

    Skipped where the machine has only the pinned interpreter -- which is the
    case in CI, and is exactly the situation this test is not needed for.
    """
    other = _an_unpinned_interpreter()
    if other is None:
        pytest.skip("no unpinned interpreter on this machine")

    result = subprocess.run(
        (other, "-m", "src.append_check", "--baseline", "no-such-ref"),
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == interpreter_pin.WRONG_INTERPRETER
    assert "3.12" in result.stderr
    # It stopped before touching the baseline, so it never reported on that ref.
    assert "no-such-ref" not in result.stderr
