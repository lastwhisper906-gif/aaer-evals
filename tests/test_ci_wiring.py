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
    eval_job = _job("eval")
    # main's evals/ is unpacked outside the tree and run with -I, so nothing the
    # branch puts at its root or installs can stand in for a module the graders import
    assert "git archive origin/main evals | tar -x -C \"$RUNNER_TEMP/graders\"" in eval_job
    assert "python -I -S -c" in eval_job and "runpy.run_module('evals'" in eval_job
    # no site module: nothing the branch's requirements installed is on the path,
    # and no .pth of theirs runs at start; the graders come after the standard library
    assert "sys.path += ['$RUNNER_TEMP/graders', '$GITHUB_WORKSPACE']" in eval_job
    assert "site-packages" not in eval_job
    # and the job installs nothing: no build script of the branch's requirements runs
    assert "pip install" not in eval_job and "requirements.txt" not in eval_job
    assert 'AAER_REPO="$GITHUB_WORKSPACE"' in eval_job
    assert "python -m evals" not in eval_job and "make eval" not in eval_job
    assert "git checkout origin/main -- evals" not in eval_job
    assert "origin/main:src/eval_guard.py" in _job("guard")
    guard = _job("guard")
    # the event's strings reach the guard through the environment only: no
    # ${{ }} of the event sits on the command line, where a crafted label could
    # end the step before the guard ran
    assert '--action "$ACTION" --label-added "$LABEL_ADDED" --labeled-by "$LABELED_BY" --owner "$OWNER"' in guard
    run_lines = [l for l in guard.splitlines() if "eval_guard.py" in l and "python" in l]
    assert run_lines and all("${{" not in l for l in run_lines)
    for key, expr in (("ACTION", "github.event.action"), ("LABEL_ADDED", "github.event.label.name"),
                      ("LABELED_BY", "github.event.sender.login"), ("OWNER", "github.repository_owner")):
        assert f"{key}: ${{{{ {expr} }}}}" in guard


def test_the_required_job_waits_on_the_guard_and_the_graders_and_fails_with_either():
    check = _job("check")
    assert "needs: [guard, eval]" in check and "if: always()" in check
    assert 'test "${{ needs.eval.result }}" = "success"' in check
    assert "guard_ok=" in check and "exit 1" in check


def test_the_guard_runs_again_when_a_label_changes():
    assert "labeled" in CI and "unlabeled" in CI
