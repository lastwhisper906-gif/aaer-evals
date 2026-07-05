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
import sys
from pathlib import Path

from jsonschema import Draft7Validator, FormatChecker

REPO = Path(__file__).resolve().parents[1]
SCHEMA_DIR = REPO / "schemas"
CANDIDATES = REPO / "data" / "candidates" / "candidates.json"
EVALUATEE = REPO / "data" / "evaluatee" / "cases.json"


def validate_items(validator, items, label, failures) -> None:
    for item in items:
        for error in validator.iter_errors(item):
            loc = f"{item.get('case_id', '?')}.{'.'.join(str(p) for p in error.absolute_path)}"
            failures.append(f"[{label}] {loc}: {error.message}")
    print(f"{label}: {len(items)}건 검증")


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
