"""verify_manifest 오프라인 테스트 (R10-2) — 네트워크 0·원본 디스크 불요."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_manifest as vm


def test_regenerated_manifest_with_forward_fetch_log_passes_own_schema(tmp_path, monkeypatch):
    """R10-2(b): forward 수집(fetch_xbrl_facts --universe)이 루트에 남기는
    fetch_log.jsonl은 derived_from으로 귀속되어야 한다 — 종전에는 source_url도
    derived_from도 없어 --write 재생성 매니페스트가 자신의 check_schema에서
    실패했다 (재생성 경로 자체가 막히는 상태)."""
    data = tmp_path / "aaer-data"
    (data / "TK99" / "xbrl").mkdir(parents=True)
    (data / "TK99" / "edgar").mkdir(parents=True)
    (data / "TK99" / "xbrl" / "CIK0000001099.json").write_text("{}", encoding="utf-8")
    (data / "TK99" / "edgar" / "CIK0000001099.json").write_text("{}", encoding="utf-8")
    (data / "fetch_log.jsonl").write_text('{"record_id": "fw001-r99"}\n',
                                          encoding="utf-8")
    monkeypatch.setattr(vm, "DATA_DIR", data)
    m = vm.build_manifest()
    assert vm.check_schema(m) == []
    log_entry = next(f for f in m["files"] if f["path"] == "fetch_log.jsonl")
    assert log_entry.get("derived_from")
    assert log_entry["source_url"] is None
