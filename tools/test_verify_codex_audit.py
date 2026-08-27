"""R2-12: codex audit 스트림 게이트 — 픽스처 양방향 + 실트리 상시 스캔."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_codex_audit as vca


def _line(obj):
    return json.dumps(obj) + "\n"


TOOL_FREE = (
    _line({"type": "thread.started", "model": "gpt-test"})
    + _line({"type": "item.completed",
             "item": {"type": "reasoning", "text": "thinking"}})
    + _line({"type": "item.completed",
             "item": {"type": "agent_message", "text": "{\"answer\": 1}"}})
    + _line({"type": "token_count", "input": 10, "output": 5})
    + _line({"type": "turn.completed"})
)


def test_tool_free_transcript_passes():
    assert vca.audit_violations(TOOL_FREE) == []


def test_command_execution_item_fails():
    text = TOOL_FREE + _line({"type": "item.completed",
                              "item": {"type": "command_execution",
                                       "command": "cat scoring/id_mapping.json"}})
    violations = vca.audit_violations(text)
    assert violations and "command_execution" in violations[0]


def test_file_and_tool_items_fail():
    for item_type in ("file_change", "mcp_tool_call", "web_search"):
        text = TOOL_FREE + _line({"type": "item.completed",
                                  "item": {"type": item_type}})
        assert vca.audit_violations(text), item_type


def test_unknown_event_type_fails_closed():
    assert vca.audit_violations(_line({"type": "surprise.event"}))


def test_non_json_line_fails():
    assert vca.audit_violations("not json\n")


def test_tree_scan(tmp_path):
    d = tmp_path / "runs/crossmodel_gpt"
    d.mkdir(parents=True)
    (d / "audit_original_C01.jsonl").write_text(TOOL_FREE, encoding="utf-8")
    assert vca.scan_tree(d) == []
    (d / "audit_original_C02.jsonl").write_text(
        TOOL_FREE + _line({"type": "item.completed",
                           "item": {"type": "command_execution"}}),
        encoding="utf-8")
    assert vca.scan_tree(d)


def test_real_tree_gate():
    """상시 게이트 — 현재 vacuous(runs/crossmodel_gpt는 MANIFEST뿐)지만
    arm의 첫 라이브 발사(소유자 게이트)를 이 게이트가 선행한다."""
    assert vca.scan_tree() == []


# ── R5-5: 스트림 접합·강건성 ──────────────────────────────────────────────

def test_retry_streams_joined_with_newline_pass(tmp_path):
    """R5-5(a): 시도 1이 행 중간에서 절단돼도, "\\n" 접합이면 절단 잔여와
    시도 2의 첫 이벤트가 별개 행 — 절단 행만 위반, 융합 오탐 없음. 실제
    crossmodel_gpt의 접합("\\n".join)을 그대로 재현해 게이트를 통과·실패
    양방향으로 검증한다."""
    attempt1_truncated = TOOL_FREE[: len(TOOL_FREE) // 2].rstrip("\n")
    attempt2 = TOOL_FREE
    fused = "".join([attempt1_truncated, attempt2])        # 종전 판형 (버그)
    joined = "\n".join([attempt1_truncated, attempt2])     # 수정 판형
    fused_violations = vca.audit_violations(fused)
    joined_violations = vca.audit_violations(joined)
    # 수정 판형: 절단 행 1건만 (그 자체는 정직한 무결성 신호), 융합 없음
    assert len(joined_violations) == 1 and "비JSON" in joined_violations[0]
    # 버그 판형은 시도 2의 첫 정상 이벤트까지 융합 — 수정본과 동일해선 안 된다
    assert fused != joined


def test_clean_retry_with_complete_attempts_passes():
    """양 시도 모두 완결 스트림이면 "\\n" 접합 후 위반 0."""
    assert vca.audit_violations("\n".join([TOOL_FREE.rstrip("\n"),
                                           TOOL_FREE.rstrip("\n")])) == []


def test_non_string_event_type_is_clean_violation_not_crash():
    violations = vca.audit_violations(_line({"type": 42}) + _line({"type": None}))
    assert len(violations) == 2
    assert all("비문자열" in v for v in violations)
