"""cutoff_guard.py — 유일한 데이터 로딩 게이트웨이 (PROJECT.md §5-1, CLAUDE.md 방법론 규율 1).

모든 파이프라인 데이터 로딩은 load_document()를 경유한다. 컷오프 위반은
예외로 즉시 중단시킨다 — 조용한 필터가 아니다. 필터는 "위반이 일어났다는
사실"을 지우지만, 예외는 위반 시도를 로그와 함께 증거로 남긴다.
doc_date == cutoff_date는 허용 (cutoff_date 자체가 폭로 '전일'로 정의됨).
"""
from __future__ import annotations

import datetime
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTRY = REPO_ROOT / "data" / "candidates" / "candidates.json"
DEFAULT_LOG = REPO_ROOT / "logs" / "access_log.jsonl"


class CutoffGuardError(Exception):
    """가드 자체의 실패(미등록 케이스, 파싱 불가 날짜, 미확정 컷오프). 항상 fail-closed."""


class CutoffViolationError(CutoffGuardError):
    """doc_date > cutoff_date. 파이프라인 실행을 무효화해야 하는 위반."""

    def __init__(self, case_id: str, doc_date: datetime.date, cutoff_date: datetime.date):
        self.case_id = case_id
        self.doc_date = doc_date
        self.cutoff_date = cutoff_date
        super().__init__(
            f"look-ahead 위반: case={case_id} doc_date={doc_date} > cutoff_date={cutoff_date}"
        )


def _parse_date(value, field: str) -> datetime.date:
    if isinstance(value, datetime.date):
        return value
    try:
        return datetime.date.fromisoformat(str(value))
    except ValueError as e:
        raise CutoffGuardError(f"{field}={value!r}: ISO 날짜가 아님 (UNRESOLVED 케이스는 로딩 불가)") from e


def load_registry(registry_path=DEFAULT_REGISTRY) -> dict:
    """candidates.json → {case_id: cutoff_date(date) | None(미확정)}."""
    raw = json.loads(Path(registry_path).read_text(encoding="utf-8"))
    cases = raw.get("candidates", raw) if isinstance(raw, dict) else raw
    registry = {}
    for case in cases:
        cutoff = case.get("cutoff_date")
        try:
            registry[case["case_id"]] = _parse_date(cutoff, "cutoff_date")
        except CutoffGuardError:
            registry[case["case_id"]] = None  # UNRESOLVED → 접근 시 fail-closed
    return registry


def _log(log_path, record: dict) -> None:
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(), **record}
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_document(case_id: str, path_or_url: str, doc_date, *,
                  registry_path=DEFAULT_REGISTRY, log_path=DEFAULT_LOG, loader=None):
    """게이트웨이. 허용/차단 모든 시도를 log_path에 기록하고, 위반은 예외로 중단."""
    def attempt(verdict: str, reason: str) -> None:
        _log(log_path, {"case_id": case_id, "doc": str(path_or_url),
                        "doc_date": str(doc_date), "verdict": verdict, "reason": reason})

    registry = load_registry(registry_path)
    if case_id not in registry:
        attempt("blocked", "unknown_case_id")
        raise CutoffGuardError(f"미등록 case_id={case_id!r}: 레지스트리에 없는 케이스는 로딩 불가")

    cutoff = registry[case_id]
    if cutoff is None:
        attempt("blocked", "cutoff_unresolved")
        raise CutoffGuardError(f"case={case_id}: cutoff_date 미확정(UNRESOLVED) — fail-closed")

    parsed = _parse_date(doc_date, "doc_date")
    if parsed > cutoff:
        attempt("blocked", "cutoff_violation")
        raise CutoffViolationError(case_id, parsed, cutoff)

    attempt("allowed", "doc_date <= cutoff_date")
    if loader is not None:
        return loader(path_or_url)
    p = Path(path_or_url)
    if not p.is_file():
        raise CutoffGuardError(f"{path_or_url!r}: 로컬 파일 아님 — URL은 loader= 콜백으로 주입 (v0)")
    return p.read_text(encoding="utf-8")
