#!/usr/bin/env python3
"""Verify semantic sidecars for current-generation README figures."""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
# The reliability diagram tests the probability hypothesis, while the
# dose-response/decomposition memorization figures are label-clean. Their real
# generators (calibration.py, synthesis.py, fig_memorization.py) are frozen
# wave-1 outputs, so only the two current-generation figures are registered.
FIGURES = (
    ("analysis/fig_dotplot.py", "analysis/fig_dotplot_30firms.sidecar.json",
     "analysis/fig_dotplot_30firms.png"),
    ("analysis/fig_tradeoff.py", "analysis/fig_tradeoff.sidecar.json",
     "analysis/fig_tradeoff.png"),
)


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
