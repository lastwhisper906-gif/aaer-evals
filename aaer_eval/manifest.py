"""Hash-pinned result selection for published-number analyzers."""
from __future__ import annotations

import hashlib
import json
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# experiment_id: (result root, result pattern).  Manifests always live below
# runs/<experiment_id>; entries may point at the scoring-side result tree.
EXPERIMENT_SPECS = OrderedDict([
    ("main", ("runs/main", "case_*.json")),
    ("perturbed", ("runs/perturbed", "case_*.json")),
    ("rp09/scores", ("runs/rp09/scores", "case_*.json")),
    ("wave2/scores", ("runs/wave2/scores", "case_*.json")),
    ("wave2/perturbed", ("runs/wave2/perturbed", "case_*.json")),
    ("holdout/scores", ("runs/holdout/scores", "case_*.json")),
    ("holdout/controls/scores", ("runs/holdout/controls/scores", "hc_*.json")),
    ("main/grades_main", ("scoring/grades/main", "case_*.json")),
    ("main/grades_perturbed", ("scoring/grades/perturbed", "case_*.json")),
    ("main/rp05_perturbation_meta", ("logs", "run_*/runmeta_perturbed_*.json")),
    ("main/name_probe_v2", ("scoring/probe_results_v2/recognition", "case_*.json")),
    ("main/name_probe_v2ds_wave1", ("scoring/probe_results_v2ds_wave1/recognition", "case_*.json")),
    ("wave2/name_probe_v2ds_wave2", ("scoring/probe_results_v2ds_wave2/recognition", "case_*.json")),
    ("e2", ("runs/e2", "**/case_*.json")),
    ("e4", ("runs/e4", "**/*.json")),
    ("e2/usage", ("logs/run_e2_20260712T212907Z", "**/*.json")),
    ("crossmodel_gpt", ("runs/crossmodel_gpt", "**/*.json")),
])


class ManifestError(RuntimeError):
    """A run manifest or its pinned result set is invalid."""


@dataclass(frozen=True)
class ManifestEntry:
    path: Path
    sha256: str
    fingerprint_sha256: str | None


def _pairs_no_duplicates(pairs):
    out = OrderedDict()
    for key, value in pairs:
        if key in out:
            raise ManifestError(f"duplicate case id: {key}")
        out[key] = value
    return out


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_experiment(experiment_id: str, *, require_fingerprints: bool = False,
                    repo: Path = REPO) -> OrderedDict[str, ManifestEntry]:
    """Validate and return the manifest's entries in committed order."""
    if experiment_id not in EXPERIMENT_SPECS:
        raise ManifestError(f"unknown experiment: {experiment_id}")
    manifest_path = repo / "runs" / experiment_id / "MANIFEST.json"
    if not manifest_path.is_file():
        raise ManifestError(f"manifest missing: {manifest_path.relative_to(repo)}")
    try:
        doc = json.loads(manifest_path.read_text(encoding="utf-8"),
                         object_pairs_hook=_pairs_no_duplicates)
    except json.JSONDecodeError as exc:
        raise ManifestError(f"invalid manifest JSON: {exc}") from exc
    if doc.get("experiment_id") != experiment_id or not isinstance(doc.get("cases"), dict):
        raise ManifestError(f"invalid manifest structure: {experiment_id}")

    root_rel, pattern = EXPERIMENT_SPECS[experiment_id]
    registered = set()
    result = OrderedDict()
    for case_id, raw in doc["cases"].items():
        rel = raw.get("path") if isinstance(raw, dict) else None
        path = repo / rel if isinstance(rel, str) else repo / "__invalid_path__"
        if not path.is_file():
            raise ManifestError(f"registered case missing on disk: {case_id}: {rel}")
        registered.add(path.resolve())
        actual = _sha256(path)
        if actual != raw.get("sha256"):
            raise ManifestError(f"sha256 mismatch: {case_id}: {rel}")
        fingerprint = raw.get("fingerprint_sha256")
        if require_fingerprints and fingerprint is None:
            raise ManifestError(f"fingerprint required but null: {case_id}: {rel}")
        result[case_id] = ManifestEntry(path, actual, fingerprint)

    root = repo / root_rel
    present = ({p.resolve() for p in root.glob(pattern) if p.name != "MANIFEST.json"}
               if root.is_dir() else set())
    extra = sorted(present - registered)
    if extra:
        raise ManifestError(f"unregistered result file present: {extra[0].relative_to(repo)}")
    return result
