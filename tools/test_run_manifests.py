"""Run-manifest validation and analyzer selection coverage."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from aaer_eval import manifest as rm
from analysis import buyer_metrics_build as bm


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _fixture(tmp_path: Path, monkeypatch, *, fingerprint=None):
    repo = tmp_path
    result_dir = repo / "results"
    result_dir.mkdir()
    record = {"case_id": "case_01"}
    if fingerprint is not ...:
        record["fingerprint"] = fingerprint
    result = result_dir / "case_01.json"
    result.write_text(json.dumps(record), encoding="utf-8")
    manifest_dir = repo / "runs" / "test"
    manifest_dir.mkdir(parents=True)
    doc = {"experiment_id": "test", "generated_from_commit": "abc",
           "cases": {"case_01": {"path": "results/case_01.json",
                                    "sha256": _sha(result),
                                    "fingerprint_sha256": None}}}
    (manifest_dir / "MANIFEST.json").write_text(json.dumps(doc), encoding="utf-8")
    monkeypatch.setitem(rm.EXPERIMENT_SPECS, "test", ("results", "case_*.json"))
    return repo, result, manifest_dir / "MANIFEST.json"


def test_duplicate_case_id_fails(tmp_path, monkeypatch):
    repo, result, manifest = _fixture(tmp_path, monkeypatch, fingerprint=...)
    entry = json.dumps({"path": "results/case_01.json", "sha256": _sha(result),
                        "fingerprint_sha256": None})
    manifest.write_text('{"experiment_id":"test","generated_from_commit":"abc",'
                        '"cases":{"case_01":' + entry + ',"case_01":' + entry + '}}')
    with pytest.raises(rm.ManifestError, match="duplicate case id: case_01"):
        rm.load_experiment("test", repo=repo)


def test_registered_case_missing_fails(tmp_path, monkeypatch):
    repo, result, _ = _fixture(tmp_path, monkeypatch, fingerprint=...)
    result.unlink()
    with pytest.raises(rm.ManifestError, match="registered case missing on disk"):
        rm.load_experiment("test", repo=repo)


def test_unregistered_result_file_fails(tmp_path, monkeypatch):
    repo, _, _ = _fixture(tmp_path, monkeypatch, fingerprint=...)
    (repo / "results/case_02.json").write_text("{}", encoding="utf-8")
    with pytest.raises(rm.ManifestError, match="unregistered result file present"):
        rm.load_experiment("test", repo=repo)


def test_sha256_mismatch_fails(tmp_path, monkeypatch):
    repo, result, _ = _fixture(tmp_path, monkeypatch, fingerprint=...)
    result.write_text('{"changed":true}', encoding="utf-8")
    with pytest.raises(rm.ManifestError, match="sha256 mismatch"):
        rm.load_experiment("test", repo=repo)


def test_required_fingerprint_rejects_legacy_null(tmp_path, monkeypatch):
    repo, _, _ = _fixture(tmp_path, monkeypatch, fingerprint=...)
    with pytest.raises(rm.ManifestError, match="fingerprint required but null"):
        rm.load_experiment("test", repo=repo, require_fingerprints=True)


@pytest.mark.parametrize("experiment_id", [
    "main", "perturbed", "rp09/scores", "wave2/scores", "holdout/scores",
    "holdout/controls/scores", "main/grades_main", "main/grades_perturbed",
    "main/rp05_perturbation_meta", "main/name_probe_v2",
    "main/name_probe_v2ds_wave1", "wave2/name_probe_v2ds_wave2", "e2", "e4",
    ("e2/usage", "crossmodel_gpt"), "wave2/perturbed",
])
def test_committed_selection_matches_manifest(experiment_id):
    experiment_ids = ((experiment_id,) if isinstance(experiment_id, str)
                      else experiment_id)
    for current_id in experiment_ids:
        manifest_path = rm.REPO / "runs" / current_id / "MANIFEST.json"
        raw = json.loads(manifest_path.read_text(encoding="utf-8"))
        expected = [rm.REPO / item["path"] for item in raw["cases"].values()]
        selected = [entry.path for entry in rm.load_experiment(current_id).values()]
        assert selected == expected


def test_buyer_metrics_rejects_wrong_in_repo_logs_dir():
    wrong = rm.REPO / "logs" / "run_e2_20260712T200708Z"
    with pytest.raises(bm.BuyerMetricsError, match="manifest root mismatch"):
        bm.compute({"flag_threshold_llm": 50, "flag_threshold_b3": 2,
                    "cases": [{"case_id": "t", "group": "treatment",
                               "snapshots": [{"llm_p": 50, "b3_score": 2,
                                              "quarters_to_revelation": 1}]},
                              {"case_id": "c", "group": "control",
                               "snapshots": [{"llm_p": 0, "b3_score": 0,
                                              "quarters_to_revelation": 1}]}]},
                   wrong, None, None)
