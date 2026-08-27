"""스키마 검증 자동화 (CI + 로컬). COLLECTION_NOTES §4의 수동 검증을 기계화한다.

검증 내용:
  1. schemas/*.json 자체가 유효한 Draft-07 JSON Schema인지
  2. data/candidates/candidates.json의 모든 케이스가 case_input 스키마를 통과하는지
  3. data/evaluatee/cases.json(존재 시)이 evaluatee_input 스키마를 통과하는지

이력: v1 검증기는 기간 정밀도(YYYY/YYYY-MM) 편차 48건의 허용목록을 갖고 있었다.
2026-07-05 스키마 v1.1 서명(패턴 완화)으로 해당 편차가 스키마 적법이 되어
허용목록을 삭제 — 이제 어떤 편차도 예외 없이 실패다.
"""
import json
import re
import sys
from pathlib import Path

from jsonschema import Draft7Validator, FormatChecker

REPO = Path(__file__).resolve().parents[1]
SCHEMA_DIR = REPO / "schemas"
CANDIDATES = REPO / "data" / "candidates" / "candidates.json"
EVALUATEE = REPO / "data" / "evaluatee" / "cases.json"

# ── R3-11: 레거시 후보 파일 4종 — 기존 편차의 명시 특성화 ─────────────────
# 66/104 레코드가 동결 case_input 스키마에 실패한다 (AAER 필수 필드 부재,
# 패턴 밖 id, scheme_type null/문자열 드리프트, matched_treatment 개명 등).
# 데이터도 스키마도 동결 — 정리는 소유자 결정 (DECISIONS_PENDING D-P90).
# 이 게이트는 기존 편차를 blanket 면제하지 않고 열거해 잠근다: 시그니처
# 집합·invalid 케이스 집합·편차 총수 중 무엇이 변해도 실패 = 신규 드리프트.
LEGACY_CANDIDATE_FILES = {
    "candidates_wave2.json": {
        "invalid_ids": sorted(["W08", "W18", "W20", "W14", "T20", "W07", "T24",
                               "T02", "W23", "W12", "W13", "T23", "W05", "W10",
                               "W04", "W21", "W09", "W11", "T26", "W17", "W01",
                               "T19", "W03", "W22", "W16", "W06", "T22", "T29",
                               "W19", "W15", "W02", "T04"]),
        "allowed_signatures": {
            "not:<root>", "pattern:case_id", "required:aaer_date",
            "required:aaer_no", "required:aaer_url",
            "required:first_revelation_date", "required:matched_case_id",
            "required:revelation_source", "type:scheme_summary",
            "type:scheme_type"},
        "error_count": 275,
    },
    "candidates_holdout.json": {
        "invalid_ids": ["case_71", "case_72", "case_73"],
        "allowed_signatures": {
            "pattern:case_id", "required:aaer_date", "required:aaer_no",
            "required:aaer_url", "required:first_revelation_date",
            "required:revelation_source", "type:scheme_type"},
        "error_count": 21,
    },
    "candidates_holdout_controls.json": {
        "invalid_ids": sorted(["VIASP", "UTL", "GRDX", "RXO", "BCO", "XPO",
                               "GO", "SFM", "VLGEA"]),
        "allowed_signatures": {
            "not:<root>", "pattern:case_id", "required:aaer_date",
            "required:aaer_no", "required:aaer_url",
            "required:first_revelation_date", "required:matched_case_id",
            "required:revelation_source", "type:scheme_summary",
            "type:scheme_type"},
        "error_count": 90,
    },
    "candidates_v2_controls.json": {
        "invalid_ids": sorted([f"V{i:02d}" for i in range(1, 23)]),
        "allowed_signatures": {
            "not:<root>", "pattern:case_id", "required:aaer_date",
            "required:aaer_no", "required:aaer_url",
            "required:first_revelation_date", "required:matched_case_id",
            "required:revelation_source", "type:scheme_summary",
            "type:scheme_type"},
        "error_count": 220,
    },
}


def _deviation_signature(error) -> str:
    path = ".".join(str(p) for p in error.absolute_path)
    if error.validator == "required":
        m = re.search(r"'([^']+)' is a required property", error.message)
        return f"required:{m.group(1) if m else path}"
    return f"{error.validator}:{path or '<root>'}"


def check_legacy_candidates(case_input_schema, failures,
                            base: Path | None = None) -> None:
    validator = Draft7Validator(case_input_schema, format_checker=FormatChecker())
    base = base or (REPO / "data" / "candidates")
    for name, expected in LEGACY_CANDIDATE_FILES.items():
        cases = json.loads((base / name).read_text(encoding="utf-8"))["candidates"]
        invalid_ids, n_err = [], 0
        for c in cases:
            errors = list(validator.iter_errors(c))
            if errors:
                invalid_ids.append(c.get("case_id", "?"))
            for e in errors:
                n_err += 1
                sig = _deviation_signature(e)
                if sig not in expected["allowed_signatures"]:
                    failures.append(f"[{name}] {c.get('case_id', '?')}: "
                                    f"특성화 밖 신규 편차 {sig}")
        if sorted(invalid_ids) != expected["invalid_ids"]:
            failures.append(f"[{name}] invalid 케이스 집합 변화: "
                            f"{sorted(invalid_ids)} ≠ 기록 {expected['invalid_ids']}")
        if n_err != expected["error_count"]:
            failures.append(f"[{name}] 편차 총수 {n_err} ≠ 기록 "
                            f"{expected['error_count']} — 침묵 드리프트 금지 "
                            "(개선이어도 특성화를 갱신·서명하라)")
        print(f"{name}: {len(cases)}건 — 기존 편차 {n_err}건 열거 대조")


def validate_items(validator, items, label, failures) -> None:
    for item in items:
        for error in validator.iter_errors(item):
            loc = f"{item.get('case_id', '?')}.{'.'.join(str(p) for p in error.absolute_path)}"
            failures.append(f"[{label}] {loc}: {error.message}")
    print(f"{label}: {len(items)}건 검증")


def check_scheme_type_by_group(cases, failures) -> None:
    """D1 (2026-07-06): scheme_type 규칙의 코드 수준 강제 — description 산문에 의존하지 않는다.

    treatment: scheme_type 필수, 비어 있지 않은 배열 (정답 키의 일부).
    control:   scheme_type 부재 또는 null만 허용 (정답 오염 방지 — 값 보유 금지).
    스키마 allOf(if/then)와 중복 강제이나, 규칙의 소재를 코드에 명시적으로 둔다.
    """
    for c in cases:
        cid, group, st = c.get("case_id", "?"), c.get("group"), c.get("scheme_type")
        if group == "treatment":
            if not st:
                failures.append(f"[D1] {cid}: treatment인데 scheme_type 부재/빈 값")
        elif group == "control":
            if st is not None:
                failures.append(f"[D1] {cid}: control인데 scheme_type 값 보유 (null/부재만 허용)")


def main() -> int:
    failures = []

    schemas = {}
    for path in sorted(SCHEMA_DIR.glob("*.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        try:
            Draft7Validator.check_schema(schema)
        except Exception as e:  # noqa: BLE001
            failures.append(f"{path.name}: 스키마 자체가 무효 — {e}")
            continue
        schemas[path.stem] = schema
        print(f"schema OK: {path.name}")

    if "case_input" in schemas:
        cases = json.loads(CANDIDATES.read_text(encoding="utf-8"))["candidates"]
        validate_items(Draft7Validator(schemas["case_input"], format_checker=FormatChecker()),
                       cases, "candidates.json", failures)
        check_scheme_type_by_group(cases, failures)
        check_legacy_candidates(schemas["case_input"], failures)

    if "evaluatee_input" in schemas and EVALUATEE.is_file():
        cases = json.loads(EVALUATEE.read_text(encoding="utf-8"))["cases"]
        validate_items(Draft7Validator(schemas["evaluatee_input"], format_checker=FormatChecker()),
                       cases, "evaluatee/cases.json", failures)

    if failures:
        print(f"\nFAIL — {len(failures)}건:", file=sys.stderr)
        for f in failures:
            print(f"  {f}", file=sys.stderr)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
