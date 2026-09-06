import fnmatch
import json
from pathlib import Path


def test_crossmodel_launch_paths_are_registered():
    registry_path = Path(__file__).resolve().parents[1] / "scoring" / "experiment_registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    experiment = next(exp for exp in registry["experiments"]
                      if exp["name"] == "crossmodel_gpt")

    assert "score_commit" in experiment
    assert "label_join_commit" in experiment
    assert any(fnmatch.fnmatch("runs/crossmodel_gpt/wave1_original/C01.json", pattern)
               for pattern in experiment["output_globs"])
    assert any(fnmatch.fnmatch(
        "runs/crossmodel_gpt/wave1_original/audit_original_C01.jsonl", pattern)
        for pattern in experiment["aux_globs"])
