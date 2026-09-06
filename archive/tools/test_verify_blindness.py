import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

import verify_blindness as vb


def write_json(root: Path, relative: str, value) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def registry(*, perturbed=None, aux=None, output=None) -> dict:
    return {"experiments": [{
        "name": "wave_test", "score_commit": "UNKNOWN",
        "label_join_commit": "UNKNOWN", "analysis_commit": "UNKNOWN",
        "output_globs": output or [], "perturbed_globs": perturbed or [],
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


# ── R13-4: 세 leg의 변별력 — 각각 자기 leg만 깨뜨린다 ──────────────────────
# 실측(2026-08-28, 008739e): 아래 세 곳을 각각 무력화해도 전 스위트가 green이었다.
#   check_manifest의 recorded−current 대조 루프 삭제 → 0 red
#   ANSWER_KEY_MARKERS 스캔의 `if marker in low` → `if False` → 0 red
#   check_not_shallow의 조건 → `if False` → 0 red
# leg (d)는 봉인 커밋 이후 runs/(봉인된 forward 사이클 포함) 사후 변조를
# 검출하는 유일한 기제이고, 마커 스캔은 채점 측 INV-09 검출기, not-shallow는
# 제3자 재현자가 가장 쉽게 빠지는 상태(shallow clone)에서 INV-07 이력 증명이
# 공진 통과하지 않게 하는 fail-closed다.

def _shallow_probe(monkeypatch, answer: str = "false", returncode: int = 0) -> None:
    """git 실행 없이 shallow 여부만 흉내낸다 (실트리·실 git 미사용)."""
    monkeypatch.setattr(vb, "subprocess", SimpleNamespace(
        run=lambda *a, **k: SimpleNamespace(returncode=returncode,
                                            stdout=answer, stderr="")))


def _three_leg_fixture(root: Path, text: str = "clean output") -> dict:
    """세 leg가 **모두 통과**하는 tmp 루트 — 각 테스트는 하나만 깨뜨린다."""
    write_json(root, "runs/wave_test/case_01.json", {"text": text})
    identity_files(root)
    vb.check_manifest(True, root)  # 정합 상태의 매니페스트로 시작
    return registry(output=["runs/wave_test/*.json"])


def _manifest_failures(root: Path) -> list[str]:
    vb.FAILS.clear()
    vb.WARNS.clear()
    vb.check_manifest(False, root)
    return list(vb.FAILS)


def test_manifest_leg_catches_post_hoc_mutation(tmp_path, monkeypatch):
    """leg (d): 양방향 — 기재된 파일의 소실/변조와 미기재 파일의 출현.

    두 루프를 각각 붙든다. 한 방향만 보면 `recorded − current` 루프를 통째로
    지워도 반대 루프가 대신 red를 내주어 변별력이 없다 (실측으로 확인).
    """
    reg = _three_leg_fixture(tmp_path)
    assert _manifest_failures(tmp_path) == []
    # 다른 두 leg는 이 픽스처에서 통과한다 (leg 격리)
    assert semantic_failures(tmp_path, reg) == []
    _shallow_probe(monkeypatch)
    vb.check_not_shallow(tmp_path)

    # (1) recorded − current: 기재된 파일이 사라졌다
    (tmp_path / "runs/wave_test/case_01.json").unlink()
    fails = _manifest_failures(tmp_path)
    assert [f for f in fails if "기재 파일 누락/변조" in f], fails
    assert not [f for f in fails if "미기재 파일 존재" in f], fails

    # (2) current − recorded: 기재되지 않은 파일이 나타났다
    write_json(tmp_path, "runs/wave_test/case_01.json", {"text": "clean output"})
    assert _manifest_failures(tmp_path) == []
    write_json(tmp_path, "runs/wave_test/case_02.json", {"text": "new"})
    fails = _manifest_failures(tmp_path)
    assert [f for f in fails if "미기재 파일 존재" in f], fails
    assert not [f for f in fails if "기재 파일 누락/변조" in f], fails

    # (3) 내용 변조는 양쪽에 동시에 걸린다
    (tmp_path / "runs/wave_test/case_02.json").unlink()
    write_json(tmp_path, "runs/wave_test/case_01.json", {"text": "tampered"})
    fails = _manifest_failures(tmp_path)
    assert [f for f in fails if "기재 파일 누락/변조" in f], fails
    assert [f for f in fails if "미기재 파일 존재" in f], fails


def test_answer_key_marker_leg_catches_a_registered_output(tmp_path, monkeypatch):
    """leg (b): 등록된 피평가자 출력에 정답지 마커."""
    reg = _three_leg_fixture(tmp_path, text="beneish 점수를 참고했다")
    # 다른 두 leg는 통과 — 마커가 심긴 뒤 매니페스트를 썼으므로 (d)는 정합
    assert _manifest_failures(tmp_path) == []
    _shallow_probe(monkeypatch)
    vb.check_not_shallow(tmp_path)

    fails = semantic_failures(tmp_path, reg)
    assert [f for f in fails if "정답지 마커" in f], fails


@pytest.mark.parametrize("answer,returncode", [("true", 0), ("false", 1)])
def test_not_shallow_leg_is_fail_closed(tmp_path, monkeypatch, answer, returncode):
    """check_not_shallow: shallow 응답과 명령 실패 양쪽 모두 fail-closed."""
    reg = _three_leg_fixture(tmp_path)
    # 다른 두 leg는 통과 (leg 격리)
    assert _manifest_failures(tmp_path) == []
    assert semantic_failures(tmp_path, reg) == []

    _shallow_probe(monkeypatch, "false")
    vb.check_not_shallow(tmp_path)  # 온전한 클론은 통과한다
    _shallow_probe(monkeypatch, answer, returncode)
    with pytest.raises(SystemExit):
        vb.check_not_shallow(tmp_path)


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


# ── R1-21: UNKNOWN 커밋의 공진(vacuous) 통과 차단 ─────────────────────────

def _unknown_exp(tmp_path, exempt=None):
    exp = {"name": "u", "score_commit": "UNKNOWN", "label_join_commit": "UNKNOWN",
           "output_globs": ["runs/u/case_*.json"], "perturbed_globs": []}
    if exempt:
        exp["history_proof_exempt"] = exempt
    return {"experiments": [exp]}


def test_unknown_with_existing_outputs_fails(tmp_path):
    write_json(tmp_path, "runs/u/case_01.json", {})
    assert any("공진 통과 금지" in f
               for f in history_failures(tmp_path, _unknown_exp(tmp_path)))


def test_unknown_with_no_outputs_passes(tmp_path):
    (tmp_path / "runs/u").mkdir(parents=True)
    assert history_failures(tmp_path, _unknown_exp(tmp_path)) == []


def test_unknown_manifest_only_passes(tmp_path):
    """MANIFEST.*는 모델 산출이 아니다 — crossmodel_gpt 현행 상태 판형."""
    write_json(tmp_path, "runs/u/MANIFEST.json", {})
    reg = {"experiments": [{"name": "u", "score_commit": "UNKNOWN",
                            "label_join_commit": "UNKNOWN",
                            "output_globs": ["runs/u/**/*.json"],
                            "perturbed_globs": []}]}
    assert history_failures(tmp_path, reg) == []


def test_unknown_with_documented_exemption_passes(tmp_path):
    write_json(tmp_path, "runs/u/case_01.json", {})
    reg = _unknown_exp(tmp_path, exempt="비실험 산출물 — 채점·라벨 결합 부재")
    assert history_failures(tmp_path, reg) == []


def test_real_registry_history_rule_passes():
    """현 트리: gil_memo는 문서화 면제, crossmodel은 MANIFEST뿐 — 규칙 무발화.
    (crossmodel arm의 첫 실산출은 커밋 확정 전까지 이 규칙이 잡는다.)"""
    vb.FAILS.clear()
    vb.WARNS.clear()
    vb.check_history(vb.REPO)
    assert vb.FAILS == []


def test_forward_runs_surface_preregistered(tmp_path):
    """R10-3: runs/forward/** 는 사전 등록된 표면 — 11월 봉인 push가
    'unregistered output surface'로 정본 CI를 붉히지 않는다. 발견 확장자
    전부가 카나리 전용 aux 클래스에 잡혀야 하고, output/perturbed 클래스에는
    잡히지 않아야 한다 (outcome 확정 전 라벨 결합·정답지가 없으므로
    ANSWER_KEY_MARKERS 어휘는 봉인 자유 서술에 적법 — 마커 스캔 부적합)."""
    registry = vb.load_registry(vb.REPO)
    for ext in ("json", "jsonl", "md", "txt"):
        p = tmp_path / f"runs/forward/cycle_001/fw001-r99.{ext}"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("{}", encoding="utf-8")
        assert p in vb._discovered_paths(tmp_path), ext
        registered = vb._registered_paths(tmp_path, registry)
        assert p in registered["aux"], ext
        assert p not in registered["output"], ext
        assert p not in registered["perturbed"], ext


def test_history_proof_exempt_set_is_pinned():
    """R6-1: 면제는 서명 근거가 있는 항목에만 — 집합을 실트리 테스트로 고정.
    crossmodel 첫 산출 시 CI가 붉어지면 최저마찰 green이 '면제 키 한 줄'인데,
    그 편집은 이 테스트의 가시적 개정 없이는 통과하지 못한다. 확장 절차:
    D-엔트리 근거(예: aux_nonexperiment의 D88/D93)를 확보한 뒤 여기 집합과
    레지스트리를 같은 커밋에서 함께 고친다."""
    registry = vb.load_registry(vb.REPO)
    exempted = {exp["name"] for exp in registry["experiments"]
                if exp.get("history_proof_exempt")}
    assert exempted == {"aux_nonexperiment"}, exempted
    crossmodel = next(exp for exp in registry["experiments"]
                      if exp["name"] == "crossmodel_gpt")
    assert "history_proof_exempt" not in crossmodel, \
        "crossmodel은 면제 불가 — 첫 산출 시 커밋 확정이 규칙 (R1-21 forcing)"


def test_canary_guid_sets_agree_across_planter_guard_and_scanner():
    """R7-10 (R6-4 패턴): 카나리 GUID가 세 모듈에 복제되어 있다 — 심는 쪽
    (runner.CANARY_MARKERS), 송출 전 가드(cli_client.EVALUATEE_FORBIDDEN_MARKERS),
    스캐너(verify_blindness.CANARIES). 한 곳에만 추가된 카나리는 스캔을
    조용히 빠져나간다 — 세 집합의 정합을 잠근다."""
    import sys
    from pathlib import Path as _P
    sys.path.insert(0, str(_P(__file__).resolve().parents[1] / "pipeline"))
    import cli_client
    import runner
    assert set(runner.CANARY_MARKERS) == set(vb.CANARIES)
    assert set(vb.CANARIES) <= set(cli_client.EVALUATEE_FORBIDDEN_MARKERS)
    # R7-18: cli_client의 명명 튜플(raw_tail redaction 소스)도 동일 집합
    assert set(cli_client.CANARY_MARKERS) == set(vb.CANARIES)


def test_every_canary_is_planted_in_a_committed_doc():
    """R8-4: 코드 세 벌의 정합(위 테스트)은 심긴 값과의 정합이 아니다 — 문서의
    GUID를 회전·삭제하면 스캐너가 아무 데도 없는 값을 사냥하며 셋 다 green.
    각 카나리 접두가 커밋된 식재 지점 중 하나 이상에 실재해야 한다."""
    plant_sites = [vb.REPO / "scoring/genre_tags.md",
                   vb.REPO / "docs/methodology_limitations.md"]
    planted = "\n".join(p.read_text(encoding="utf-8") for p in plant_sites).lower()
    missing = [c for c in vb.CANARIES if c.lower() not in planted]
    assert not missing, f"식재 지점에 없는 카나리 접두: {missing}"
