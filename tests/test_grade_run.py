"""The analysis-grader's runner: what it hands the grader, and where its answer lands."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from src import grade_run, run_analysis

CLEAN = Path(__file__).resolve().parent.parent / "runs" / "CSCO" / "0000858877-26-000078"


@pytest.fixture
def run(tmp_path):
    target = tmp_path / "CSCO" / CLEAN.name
    shutil.copytree(CLEAN, target, ignore=shutil.ignore_patterns("agents", "control-*"))
    return target


def test_the_grader_runs_on_opus_never_the_analysts_model():
    assert run_analysis.definition("analysis-grader")["model"] == "opus"
    assert run_analysis.definition("accounting-analyst")["model"] != "opus"


def test_the_grader_sees_outputs_and_the_rubric_and_writes_grade_json_into_the_run(run):
    seen = {}

    def ask(directory, *, agent, writes, message, spec, log):
        seen["files"] = sorted(p.name for p in directory.iterdir())
        (directory / "grade.json").write_text(json.dumps({"score": 0.5, "items": []}))
        return {"result": "written", "model_requested": spec["model"]}

    record = grade_run.grade(run, ask=ask)
    assert record["result"] == "written"
    assert "rubric.md" in seen["files"] and "analysis_accounting.json" in seen["files"]
    assert not any(name.startswith(("agents", "control")) for name in seen["files"])
    assert json.loads((run / "grade.json").read_text())["score"] == 0.5


def test_a_run_is_graded_once(run):
    (run / "grade.json").write_text("{}")
    with pytest.raises(grade_run.GradeError):
        grade_run.grade(run, ask=lambda *a, **k: {"result": "written"})
