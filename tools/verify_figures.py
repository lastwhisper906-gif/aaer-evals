#!/usr/bin/env python3
"""Verify hashes and semantic sidecars for all README figures."""
import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANIFEST = "analysis/figures.manifest.json"
FIGURES = (
    ("analysis/fig_dotplot.py", "analysis/fig_dotplot_30firms.sidecar.json",
     "analysis/fig_dotplot_30firms.png"),
    ("analysis/fig_tradeoff.py", "analysis/fig_tradeoff.sidecar.json",
     "analysis/fig_tradeoff.png"),
)


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _config_digest(sidecar: dict) -> str:
    config = {key: value for key, value in sidecar.items()
              if key not in {"figure", "data_sha256"}}
    encoded = json.dumps(config, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _load_generator(script: Path):
    name = f"_figure_generator_{script.stem}"
    spec = importlib.util.spec_from_file_location(name, script)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot import {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _differences(expected: object, actual: object, prefix: str = "") -> list[str]:
    if isinstance(expected, dict) and isinstance(actual, dict):
        fields = []
        for key in sorted(set(expected) | set(actual)):
            field = f"{prefix}.{key}" if prefix else key
            if key not in expected or key not in actual:
                fields.append(field)
            else:
                fields.extend(_differences(expected[key], actual[key], field))
        return fields
    return [] if expected == actual else [prefix]


def verify(sidecar_root: Path = REPO) -> list[str]:
    failures = []
    try:
        entries = json.loads((sidecar_root / MANIFEST).read_text(
            encoding="utf-8"))["figures"]
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        return [f"{MANIFEST}: {exc}"]
    if len(entries) != 5:
        failures.append(f"{MANIFEST}: expected 5 figures, found {len(entries)}")
    for entry in entries:
        path = REPO / entry.get("path", "")
        if not path.is_file():
            failures.append(f"{entry.get('path', '<missing path>')}: missing PNG")
        elif _digest(path) != entry.get("sha256"):
            failures.append(f"{entry['path']}: sha256 mismatch")
        if entry.get("mode") == "frozen":
            if entry.get("note") != "frozen wave-1 generator, pinned bytes":
                failures.append(f"{entry['path']}: missing frozen-generator note")
        elif entry.get("mode") != "current-generator":
            failures.append(f"{entry.get('path', '<missing path>')}: invalid mode")
    for script_rel, sidecar_rel, png_rel in FIGURES:
        if not (REPO / png_rel).is_file():
            failures.append(f"{png_rel}: missing README-referenced PNG")
            continue
        try:
            committed = json.loads((sidecar_root / sidecar_rel).read_text(
                encoding="utf-8"))
            computed = _load_generator(REPO / script_rel).compute_sidecar()
        except (OSError, ValueError, TypeError, ImportError,
                json.JSONDecodeError) as exc:
            failures.append(f"{sidecar_rel}: {exc}")
            continue
        for field in _differences(committed, computed):
            failures.append(f"{sidecar_rel}: drift in field {field}")
        entry = next((item for item in entries if item.get("path") == png_rel), None)
        if entry is None:
            failures.append(f"{png_rel}: missing manifest entry")
        else:
            if entry.get("source_data_sha256") != computed.get("data_sha256"):
                failures.append(f"{png_rel}: source-data hash mismatch")
            if entry.get("config_sha256") != _config_digest(computed):
                failures.append(f"{png_rel}: config hash mismatch")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sidecar-root", type=Path, default=REPO)
    args = parser.parse_args()
    failures = verify(args.sidecar_root)
    if failures:
        print("\n".join(f"FAIL: {failure}" for failure in failures), file=sys.stderr)
        return 1
    print("figure sidecars: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
