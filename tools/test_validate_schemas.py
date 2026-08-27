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
