import json
import subprocess
from pathlib import Path

import verify_blindness as vb


def write_json(root: Path, relative: str, value) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def registry(*, perturbed=None, aux=None) -> dict:
    return {"experiments": [{
        "name": "wave_test", "score_commit": "UNKNOWN",
        "label_join_commit": "UNKNOWN", "analysis_commit": "UNKNOWN",
        "output_globs": [], "perturbed_globs": perturbed or [],
        "aux_globs": aux or [],
        "perturbed_treatment_ids": "ids.json",
        "names_mapping": "mapping.json", "names_candidates": "candidates.json",
    }]}


def identity_files(root: Path, candidates=None, mapping=None) -> None:
    write_json(root, "ids.json", {"cases": [{"case_id": "case_01"}]})
    write_json(root, "mapping.json", {"mapping": mapping or {"case_01": "T01"}})
    if candidates is None:
        candidates = [{"case_id": "T01", "company_name": "Zebra Corp", "ticker": "ZBRA"}]
    write_json(root, "candidates.json", {"candidates": candidates})


def semantic_failures(root: Path, reg: dict) -> list[str]:
    vb.FAILS.clear()
    vb.WARNS.clear()
    vb.check_semantic_scans(root, reg)
    return list(vb.FAILS)


def commit(root: Path, message: str) -> str:
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "-c", "user.name=Test", "-c",
                    "user.email=test@example.invalid", "commit", "-m", message],
                   cwd=root, check=True, capture_output=True)
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True,
                          capture_output=True, text=True).stdout.strip()


def history_failures(root: Path, reg: dict) -> list[str]:
    vb.FAILS.clear()
    vb.WARNS.clear()
    vb.check_history(root, reg)
    return list(vb.FAILS)


def test_history_fails_when_criteria_commit_does_not_precede_results(tmp_path):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    write_json(tmp_path, "joined.json", {})
    joined = commit(tmp_path, "label join")
    write_json(tmp_path, "scores.json", {})
    score = commit(tmp_path, "criteria after results")
    reg = {"experiments": [{"name": "bad-order", "score_commit": score,
                             "label_join_commit": joined}]}

    assert any("조상이 아님" in failure for failure in history_failures(tmp_path, reg))


def test_history_unknown_skip_cannot_vacuously_pass_required_state(tmp_path):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    write_json(tmp_path, "initial.json", {})
    commit(tmp_path, "initial")
    reg = {"experiments": [{"name": "unknown-score", "score_commit": "UNKNOWN",
                             "label_join_commit": "UNKNOWN",
                             "blind_state_required": ["blind.json"]}]}

    assert any("트리를 읽지 못함" in failure
               for failure in history_failures(tmp_path, reg))


def test_synthetic_real_name_leak(tmp_path):
    reg = registry(perturbed=["runs/wave_test/**/*.json"])
    identity_files(tmp_path)
    write_json(tmp_path, "runs/wave_test/case_01.json", {"text": "Zebra Corp"})
    assert any("실명" in failure for failure in semantic_failures(tmp_path, reg))


def test_unregistered_surface_fails(tmp_path):
    write_json(tmp_path, "runs/rogue/case_01.json", {})
    assert any("unregistered output surface" in failure
               for failure in semantic_failures(tmp_path, {"experiments": []}))


def test_unregistered_nonjson_surface_fails(tmp_path):
    """R1-9: *.md/*.jsonl/*.txt 표면도 발견·등록 의무 — 카나리를 실은 미등록
    leak.md가 조용히 통과하면 안 된다."""
    leak = tmp_path / "runs/rogue/leak.md"
    leak.parent.mkdir(parents=True)
    leak.write_text("memo with canary 9fa11f98-dead-beef", encoding="utf-8")
    fails = semantic_failures(tmp_path, {"experiments": []})
    assert any("unregistered output surface" in f and "leak.md" in f for f in fails)


def test_registered_nonjson_surface_is_canary_scanned(tmp_path):
    reg = {"experiments": [{"name": "t", "score_commit": "UNKNOWN",
                            "label_join_commit": "UNKNOWN",
                            "output_globs": [], "perturbed_globs": [],
                            "aux_globs": ["runs/rogue/*.md"]}]}
    leak = tmp_path / "runs/rogue/leak.md"
    leak.parent.mkdir(parents=True)
    leak.write_text("memo with canary 9fa11f98-dead-beef", encoding="utf-8")
    assert any("카나리" in f for f in semantic_failures(tmp_path, reg))


def test_unregistered_grades_sibling_tree_fails(tmp_path):
    """R2-1: scoring/grades_wave2 등 grades 형제 트리는 채점자 모델 산출 —
    미등록 파일이 발견을 피해 조용히 통과하면 안 된다."""
    write_json(tmp_path, "scoring/grades_wave2/case_99.json", {})
    fails = semantic_failures(tmp_path, {"experiments": []})
    assert any("unregistered output surface" in f and "grades_wave2" in f
               for f in fails)


def test_logs_call_log_is_discovered_and_canary_scanned(tmp_path):
    """R2-1: logs/run_*/ 호출 로그(raw_tail 실패 텍스트 채널 포함)는 발견
    대상이며, aux 등록 시 카나리 스캔을 받는다."""
    write_json(tmp_path, "logs/run_x/evaluatee_test.json",
               {"raw_tail": "canary 9fa11f98-dead-beef"})
    unreg = semantic_failures(tmp_path, {"experiments": []})
    assert any("unregistered output surface" in f and "evaluatee_test" in f
               for f in unreg)
    reg = {"experiments": [{"name": "t", "score_commit": "UNKNOWN",
                            "label_join_commit": "UNKNOWN",
                            "output_globs": [], "perturbed_globs": [],
                            "aux_globs": ["logs/run_*/**/*.json"]}]}
    assert any("카나리" in f for f in semantic_failures(tmp_path, reg))


def test_real_tree_discovery_fully_registered():
    """R2-1: 현재 트리의 모든 발견 표면이 레지스트리에 등록되어 있다
    (내용 스캔 없이 글롭 대조만 — 전체 스캔은 verify_blindness 게이트)."""
    registry = vb.load_registry(vb.REPO)
    registered = vb._registered_paths(vb.REPO, registry)
    all_registered = set().union(*registered.values())
    unregistered = vb._discovered_paths(vb.REPO) - all_registered
    assert unregistered == set(), sorted(
        str(p.relative_to(vb.REPO)) for p in unregistered)


def test_derivation_missing_mapping_fails_closed(tmp_path):
    reg = registry(perturbed=["runs/wave_test/**/*.json"])
    identity_files(tmp_path, mapping={"different": "T01"})
    write_json(tmp_path, "runs/wave_test/case_01.json", {})
    assert any("이름 파생 실패" in failure for failure in semantic_failures(tmp_path, reg))


def test_derivation_empty_candidates_fails_closed(tmp_path):
    reg = registry(perturbed=["runs/wave_test/**/*.json"])
    identity_files(tmp_path, candidates=[])
    write_json(tmp_path, "runs/wave_test/case_01.json", {})
    assert any("이름 파생 실패" in failure for failure in semantic_failures(tmp_path, reg))


def test_wave1_distinctive_name_variants():
    real_registry = vb.load_registry(vb.REPO)
    wave1 = next(exp for exp in real_registry["experiments"] if exp["name"] == "wave1")
    patterns = vb.derive_treatment_patterns(vb.REPO, wave1)
    assert patterns is not None
    for name in ("comscore", "orthofix", "logitech", "monsanto", "hertz",
                 "iconix", "kraft heinz", "marvell"):
        assert patterns[0].search(name), name


def test_registered_clean_perturbed_passes_semantic_scan(tmp_path):
    reg = registry(perturbed=["runs/wave_test/**/*.json"])
    identity_files(tmp_path)
    write_json(tmp_path, "runs/wave_test/case_01.json", {"text": "clean output"})
    assert semantic_failures(tmp_path, reg) == []


def test_perturbed_precedes_aux(tmp_path):
    reg = registry(perturbed=["runs/wave_test/**/*.json"],
                   aux=["runs/**/*.json"])
    identity_files(tmp_path)
    write_json(tmp_path, "runs/wave_test/case_01.json", {"text": "Zebra"})
    assert any("실명" in failure for failure in semantic_failures(tmp_path, reg))
