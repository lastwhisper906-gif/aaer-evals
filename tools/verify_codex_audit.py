"""Codex 교차모델 arm의 audit 이벤트 스트림 파서-게이트 (R2-12).

D-P44b/D-P45가 공개한 약점의 기계적 상계: codex exec --sandbox read-only는
쓰기만 막는다 — read-only 샌드박스도 실행 중 scoring/ 정답 파일을 *읽고*
마커를 에코하지 않은 채 활용할 수 있다. 격리 임시 cwd가 1차 방어지만,
이 게이트는 보존된 `--json` audit 스트림(runs/crossmodel_gpt/**/
audit_*.jsonl)을 전건 파싱해 프롬프트/모델 메시지/토큰 스트림 외의 어떤
이벤트(command_execution·파일 읽기·도구 호출류)라도 나타나면 FAIL한다 —
fail-closed: 미지 이벤트 유형·비JSON 행도 FAIL.

usage: python tools/verify_codex_audit.py   (위반 시 exit 1)
pytest sweep에는 tools/test_verify_codex_audit.py가 상시 배선 — arm의 첫
라이브 발사(소유자 게이트) 이전부터 게이트가 선행한다 (현재 vacuous).
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# 프롬프트 송출·모델 텍스트·토큰 계량·스레드 수명주기 — 도구성 활동 없음
ALLOWED_EVENT_TYPES = {
    "thread.started", "turn.started", "turn.completed", "turn.failed",
    "token_count", "error",
}
ALLOWED_ITEM_TYPES = {"agent_message", "reasoning"}


def audit_violations(text: str, label: str = "<audit>") -> list[str]:
    """audit jsonl 본문의 위반 목록 — 빈 목록 = 도구-무활동 스트림."""
    violations = []
    for n, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            violations.append(f"{label}:{n}: 비JSON 행 (스트림 무결성)")
            continue
        etype = event.get("type")
        if etype in ALLOWED_EVENT_TYPES:
            continue
        if isinstance(etype, str) and etype.startswith("item."):
            item_type = (event.get("item") or {}).get("type")
            if item_type in ALLOWED_ITEM_TYPES:
                continue
            violations.append(
                f"{label}:{n}: 도구성 item 이벤트 {item_type!r} — read-only "
                "샌드박스의 파일 읽기/명령 실행 흔적 (교차모델 no-leak 상계 위반)")
            continue
        violations.append(f"{label}:{n}: 미지 이벤트 유형 {etype!r} (fail-closed)")
    return violations


def scan_tree(root: Path | None = None) -> list[str]:
    root = root or (REPO / "runs" / "crossmodel_gpt")
    violations = []
    if not root.is_dir():
        return violations
    for path in sorted(root.rglob("audit_*.jsonl")):
        violations.extend(audit_violations(path.read_text(encoding="utf-8"),
                                           str(path.relative_to(root))))
    return violations


def main() -> int:
    violations = scan_tree()
    for v in violations:
        print(f"FAIL {v}")
    print(f"{'PASS' if not violations else 'FAIL'} — codex audit 스트림 게이트")
    return 0 if not violations else 1


if __name__ == "__main__":
    sys.exit(main())
