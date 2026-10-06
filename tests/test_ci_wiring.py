"""The CI workflow's wiring, read off the file: which copies the jobs run, and what
the required job waits on. GitHub runs the file; this is the only judge it has here.
"""

from pathlib import Path

CI = (Path(__file__).resolve().parent.parent / ".github" / "workflows" / "ci.yml").read_text()


def _job(name: str) -> str:
    start = CI.index(f"\n  {name}:\n")
    rest = CI[start + 1:]
    nxt = [i for i in (rest.find(f"\n  {j}:\n") for j in ("guard", "eval", "check")) if i > 0]
    return rest[: min(nxt)] if nxt else rest


def test_the_graders_and_the_guard_that_run_are_mains_copies():
    assert "git checkout origin/main -- evals/" in _job("eval")
    assert "python -m evals" in _job("eval") and "make eval" not in _job("eval")
    assert "origin/main:src/eval_guard.py" in _job("guard")
    assert '--action "${{ github.event.action }}"' in _job("guard")


def test_the_required_job_waits_on_the_guard_and_the_graders_and_fails_with_either():
    check = _job("check")
    assert "needs: [guard, eval]" in check and "if: always()" in check
    assert 'test "${{ needs.eval.result }}" = "success"' in check
    assert "guard_ok=" in check and "exit 1" in check


def test_the_guard_runs_again_when_a_label_changes():
    assert "labeled" in CI and "unlabeled" in CI
