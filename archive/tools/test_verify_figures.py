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
        "analysis/figures.manifest.json",
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


def test_checker_covers_all_five_readme_figures():
    manifest = json.loads((REPO / "analysis/figures.manifest.json").read_text(
        encoding="utf-8"))
    assert {entry["path"] for entry in manifest["figures"]} == {
        "analysis/fig_dotplot_30firms.png",
        "analysis/fig_tradeoff.png",
        "analysis/fig_reliability.png",
        "analysis/fig_memorization_doseresponse.png",
        "analysis/fig_memorization_decomposition.png",
    }
    current = [entry for entry in manifest["figures"]
               if entry["mode"] == "current-generator"]
    assert all({"source_data_sha256", "config_sha256"} <= set(entry)
               for entry in current)


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


# ── R1-22: README 그림 참조 ↔ 매니페스트 링키지 ───────────────────────────

def test_readme_refs_extracted_and_all_manifested(tmp_path):
    import json as _json
    import verify_figures as vf
    refs = vf.readme_figure_refs()
    assert refs, "README에서 그림 참조를 하나도 찾지 못함 — 추출 회귀"
    manifest = _json.loads((vf.REPO / vf.MANIFEST).read_text(encoding="utf-8"))
    manifest_paths = {e["path"] for e in manifest["figures"]}
    assert refs <= manifest_paths, refs - manifest_paths


def test_unmanifested_readme_figure_fails(tmp_path, monkeypatch):
    import verify_figures as vf
    rogue_readme = tmp_path / "README.md"
    rogue_readme.write_text(
        (vf.REPO / "README.md").read_text(encoding="utf-8")
        + "\n![new figure](analysis/fig_brand_new.png)\n", encoding="utf-8")
    monkeypatch.setattr(vf, "README_PATH", rogue_readme)
    failures = vf.verify()
    assert any("fig_brand_new.png" in f and "no manifest entry" in f
               for f in failures), failures[:5]


def test_unmanifested_ko_readme_figure_fails(tmp_path, monkeypatch):
    """R7-12: README.ko.md는 1급 발행 표면 — 거기에만 추가된 그림도 매니페스트
    등재 의무 (en/ko 한쪽 구멍 차단)."""
    import verify_figures as vf
    rogue = tmp_path / "README.ko.md"
    rogue.write_text(
        vf.KO_README_PATH.read_text(encoding="utf-8")
        + "\n![새 그림](analysis/fig_ko_only.png)\n", encoding="utf-8")
    monkeypatch.setattr(vf, "KO_README_PATH", rogue)
    failures = vf.verify()
    assert any("fig_ko_only.png" in f and "no manifest entry" in f
               for f in failures), failures[:5]
