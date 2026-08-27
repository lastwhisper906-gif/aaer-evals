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
