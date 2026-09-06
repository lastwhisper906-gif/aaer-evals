"""smoke_rev3 무호출 테스트 — 매니페스트 산술·결정론·래치 (FREEZE_REV3 §3·§6-3)."""
import importlib.util
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("smoke_rev3", REPO / "tools" / "smoke_rev3.py")
smoke = importlib.util.module_from_spec(spec)
spec.loader.exec_module(smoke)


def test_manifest_arithmetic_matches_spec():
    m = smoke.build_manifest()
    # §3-5: 2케이스 × 5draw × (하네스 + raw 미핀 + raw temp0) = 30
    assert m["n_calls_total"] == 30
    assert m["n_calls_by_arm"] == {"harness": 10, "api_unpinned": 10, "api_temp0": 10}
    assert m["sample_list"] == ["case_90", "case_91"]  # 스펙 샘플 리스트 = pilot 2건
    assert m["model_pin"] == "claude-sonnet-5"
    assert "게이트 아님" in m["purpose"]
    assert "6.4pp" in m["reading_rule"]  # 2×σ(3.2pp) 사전 고정 판독


def test_manifest_temperature_pins():
    m = smoke.build_manifest()
    temps = {c["arm"]: set() for c in m["calls"]}
    for c in m["calls"]:
        temps[c["arm"]].add(c["temperature"])
    assert temps == {"harness": {None}, "api_unpinned": {None}, "api_temp0": {0.0}}
    # 미핀도 '명시적' 미핀 — arm 메타에 사유 문장이 있어야 함
    notes = {a["arm"]: a["temperature_note"] for a in m["arms"]}
    assert "미핀" in notes["api_unpinned"] and "0.0" in notes["api_temp0"]


def test_manifest_deterministic_and_seq_ordered():
    m1, m2 = smoke.build_manifest(), smoke.build_manifest()
    assert m1 == m2
    assert [c["seq"] for c in m1["calls"]] == list(range(1, 31))
    assert all(c["payload_variant"].startswith("original") for c in m1["calls"])


def test_live_blocked_without_latch(monkeypatch):
    monkeypatch.delenv("AAER_RAW_API_APPROVED", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="raw API 경로 미승인"):
        smoke.cmd_live()


def test_committed_dryrun_manifest_in_sync():
    """커밋된 DRYRUN_MANIFEST.json이 재생성본과 일치해야 함 (§6-3 순서 보증)."""
    import json
    committed = json.loads((REPO / "runs/smoke_rev3/DRYRUN_MANIFEST.json")
                           .read_text(encoding="utf-8"))
    assert committed["calls"] == smoke.build_manifest()["calls"]
