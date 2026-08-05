import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_checker_passes_committed_tree():
    result = subprocess.run(
        [sys.executable, "tools/verify_figures.py"], cwd=REPO,
        text=True, capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stderr


def test_checker_names_tampered_field(tmp_path):
    for relative in (
        "analysis/fig_dotplot_30firms.sidecar.json",
        "analysis/fig_tradeoff.sidecar.json",
    ):
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REPO / relative, target)
    target = tmp_path / "analysis/fig_dotplot_30firms.sidecar.json"
    sidecar = json.loads(target.read_text(encoding="utf-8"))
    sidecar["xlabel"] = "tampered"
    target.write_text(json.dumps(sidecar), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "tools/verify_figures.py", "--sidecar-root", str(tmp_path)],
        cwd=REPO, text=True, capture_output=True, check=False,
    )
    assert result.returncode != 0
    assert "field xlabel" in result.stderr


def test_dotplot_sidecar_pins_bn12_labels():
    module = _load(REPO / "analysis/fig_dotplot.py", "fig_dotplot_test")
    sidecar = module.compute_sidecar()
    assert sidecar["xlabel"] == "Evaluatee risk score (0-100, ordinal; original frame)"
    assert "flag threshold T=50\n(pre-frozen rubric)" in sidecar["annotations"]


def test_checker_import_needs_no_matplotlib():
    source = (REPO / "tools/verify_figures.py").read_text(encoding="utf-8")
    assert "matplotlib" not in source
    assert "pyplot" not in source


@pytest.mark.parametrize("script", ["fig_dotplot.py", "fig_tradeoff.py"])
def test_figure_renders_to_requested_output(tmp_path, script):
    output = tmp_path / f"{Path(script).stem}.png"
    env = os.environ.copy()
    env.pop("DISPLAY", None)
    result = subprocess.run(
        [sys.executable, str(REPO / "analysis" / script), "--out", str(output)],
        cwd=REPO, env=env, text=True, capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stderr
    assert output.stat().st_size > 0
