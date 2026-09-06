"""D1 (2026-07-06) 검증기 코드 수준 강제의 단위 테스트 — scheme_type × group 규칙."""
from validate_schemas import check_scheme_type_by_group


def run(cases):
    failures = []
    check_scheme_type_by_group(cases, failures)
    return failures


def test_treatment_requires_scheme_type():
    assert run([{"case_id": "T01", "group": "treatment"}])
    assert run([{"case_id": "T01", "group": "treatment", "scheme_type": []}])
    assert run([{"case_id": "T01", "group": "treatment", "scheme_type": None}])
    assert not run([{"case_id": "T01", "group": "treatment", "scheme_type": ["revenue_recognition"]}])


def test_control_forbids_scheme_type_value():
    assert run([{"case_id": "C01", "group": "control", "scheme_type": ["revenue_recognition"]}])
    assert not run([{"case_id": "C01", "group": "control", "scheme_type": None}])
    assert not run([{"case_id": "C01", "group": "control"}])


# ── R3-11: 레거시 후보 4파일 편차 특성화 게이트 ───────────────────────────

import json
import shutil
from pathlib import Path

from jsonschema import Draft7Validator

import validate_schemas as vs

REPO = Path(__file__).resolve().parents[1]
CASE_INPUT = json.loads((REPO / "schemas/case_input.json").read_text(encoding="utf-8"))


def _legacy_failures(base=None):
    failures = []
    vs.check_legacy_candidates(CASE_INPUT, failures, base=base)
    return failures


def test_current_tree_deviations_fully_characterized():
    """현 트리: 66건 기존 편차가 전부 열거 특성화 안 — 게이트 무발화."""
    assert _legacy_failures() == []


def _copied_base(tmp_path):
    base = tmp_path / "candidates"
    base.mkdir()
    for name in vs.LEGACY_CANDIDATE_FILES:
        shutil.copy(REPO / "data/candidates" / name, base / name)
    return base


def test_planted_new_deviation_kind_fails(tmp_path):
    base = _copied_base(tmp_path)
    doc = json.loads((base / "candidates_holdout.json").read_text(encoding="utf-8"))
    doc["candidates"][0]["cutoff_date"] = "not-a-date"  # 신규 편차 클래스
    (base / "candidates_holdout.json").write_text(json.dumps(doc), encoding="utf-8")
    failures = _legacy_failures(base)
    assert any("특성화 밖 신규 편차" in f for f in failures), failures[:5]


def test_new_invalid_case_fails(tmp_path):
    base = _copied_base(tmp_path)
    doc = json.loads((base / "candidates_wave2.json").read_text(encoding="utf-8"))
    extra = dict(doc["candidates"][0])
    extra["case_id"] = "W99"
    doc["candidates"].append(extra)
    (base / "candidates_wave2.json").write_text(json.dumps(doc), encoding="utf-8")
    failures = _legacy_failures(base)
    assert any("invalid 케이스 집합 변화" in f for f in failures)


def test_silent_improvement_also_fails(tmp_path):
    """편차 감소도 특성화 갱신 없이 통과 금지 — 침묵 드리프트 대칭 차단."""
    base = _copied_base(tmp_path)
    doc = json.loads((base / "candidates_holdout.json").read_text(encoding="utf-8"))
    doc["candidates"][0]["aaer_no"] = "AAER-9999"  # required 편차 1건 해소
    (base / "candidates_holdout.json").write_text(json.dumps(doc), encoding="utf-8")
    failures = _legacy_failures(base)
    assert any("편차 총수" in f for f in failures)


def test_compensating_swap_on_invalid_cases_fails(tmp_path):
    """R4-8: 허용 시그니처 집합 안의 보상 스왑 — W-케이스에서 required 편차
    1건 해소(-1), T-케이스에 다른 허용 클래스 편차 1건 추가(+1). invalid id
    집합·시그니처 집합·총수 전부 불변 → 집계 잠금은 눈멀고, 케이스별
    특성화 sha256만이 잡는다."""
    base = _copied_base(tmp_path)
    name = "candidates_wave2.json"
    doc = json.loads((base / name).read_text(encoding="utf-8"))
    by_id = {c["case_id"]: c for c in doc["candidates"]}
    w01, t04 = by_id["W01"], by_id["T04"]
    assert "aaer_no" not in w01 and "scheme_summary" in t04
    w01["aaer_no"] = "AAER-1111"    # -1: required:aaer_no (W01은 여전히 invalid)
    t04["scheme_summary"] = 123     # +1: type:scheme_summary (허용 클래스)
    (base / name).write_text(json.dumps(doc), encoding="utf-8")
    failures = _legacy_failures(base)
    assert any("케이스별 편차 특성화 sha256 불일치" in f for f in failures), failures
    # 스왑 특성상 집계 잠금은 정말로 침묵해야 테스트가 의미를 가진다
    assert not any("편차 총수" in f or "invalid 케이스 집합" in f
                   or "특성화 밖 신규 편차" in f for f in failures), failures


def test_emit_characterization_output_is_pasteable(tmp_path, capsys):
    """R5-4: 서명 정리 집행 시뮬레이션 — 도구 출력 복사만으로 상수 갱신 가능."""
    import subprocess
    import sys as _sys
    base = _copied_base(tmp_path)
    doc = json.loads((base / "candidates_holdout.json").read_text(encoding="utf-8"))
    doc["candidates"][0]["aaer_no"] = "AAER-9999"  # 서명된 정리라고 가정
    (base / "candidates_holdout.json").write_text(json.dumps(doc), encoding="utf-8")
    # 갱신 경로: emit이 내놓는 해시가 곧 새 상수 — 재계산 일치 확인
    vs.emit_characterization(CASE_INPUT, base=base)
    out = capsys.readouterr().out
    import re as _re
    hashes = _re.findall(r'"characterization_sha256": "([0-9a-f]{64})",', out)
    assert len(hashes) == len(vs.LEGACY_CANDIDATE_FILES)
    validator = Draft7Validator(CASE_INPUT)
    _, _, per_case, _, _ = vs.characterize_file(
        validator, base / "candidates_holdout.json")
    assert vs.characterization_sha256(per_case) in hashes


def test_mismatch_error_carries_full_hash(tmp_path):
    base = _copied_base(tmp_path)
    doc = json.loads((base / "candidates_holdout.json").read_text(encoding="utf-8"))
    doc["candidates"][0]["aaer_no"] = "AAER-9999"
    (base / "candidates_holdout.json").write_text(json.dumps(doc), encoding="utf-8")
    failures = _legacy_failures(base)
    sha_failures = [f for f in failures if "sha256 불일치" in f]
    assert sha_failures
    import re as _re
    assert _re.search(r"실측 [0-9a-f]{64} ≠ 기록 [0-9a-f]{64}", sha_failures[0])
