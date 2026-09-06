"""lint_doc_counts pytest collection failure handling tests."""
from types import SimpleNamespace

import pytest

import lint_doc_counts as ldc


def test_collect_error_transcript_fails_instead_of_returning_shrunken_count(monkeypatch):
    transcript = "12 tests collected, 1 error in 0.10s\n"
    monkeypatch.setattr(
        ldc.subprocess, "run",
        lambda *a, **k: SimpleNamespace(
            returncode=2, stdout=transcript, stderr="collection error"),
    )

    with pytest.raises(SystemExit, match="pytest --collect-only 실패"):
        ldc.pytest_collected()
