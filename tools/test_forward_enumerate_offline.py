"""forward_enumerate --offline 결정론 재계산의 오프라인 pytest (BN-15 part i).

OWNER_LAUNCH_GATE §4 step (1)의 개막 명령("python tools/forward_enumerate.py
--offline — 동결본 재계산 일치 확인")을 봉인 창(2026-11-15) 밖에서 미리
실측한다 — 창 안 첫 실행에서의 실패는 INV-22 abort로 전환되므로.

주의: T₀ 스냅샷 2816파일 중 submissions_CIK*.json은 .gitignore로 git 밖이다
(data/candidates/universe/.gitignore). 전체 재계산 테스트는
SNAPSHOT_MANIFEST.sha256 대비 스냅샷 완전성을 검사해 불완전하면 명시적
skip한다 (CI·워크트리에서는 skip, 전체 스냅샷 보유 머신에서 실측).
게이트 핀 sha256 대조는 커밋 산출물만으로 어디서나 실행된다.
"""
import hashlib
import sys
import urllib.request
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import forward_common
import forward_enumerate

REPO = forward_common.REPO
FROZEN = REPO / "forward/cycle_001/universe.json"
GATE = REPO / "forward/cycle_001/OWNER_LAUNCH_GATE.md"
SNAP = REPO / "data/candidates/universe"
MANIFEST = SNAP / "SNAPSHOT_MANIFEST.sha256"

# OWNER_LAUNCH_GATE §1 핀 (동결 2026-07-20) — 여기 하드코딩해 게이트 문서와
# 커밋 파일 양쪽을 상호 대조한다.
GATE_PIN = "95eea6ec31f056e45f7b084ead51ace8764060ab12d269a306cd7c25c7b4aaee"


class NetworkAttempt(BaseException):
    """BaseException 파생 — fetch()의 except Exception에 삼켜지지 않고
    (`.missing` 마커 기록 없이) 테스트를 즉시 실패시킨다."""


def _refuse_network(*args, **kwargs):
    raise NetworkAttempt(f"offline 재계산 중 네트워크 시도: {args[:1]}")


def _missing_snapshot_files():
    names = [line.split("  ", 1)[1].strip().lstrip("./")
             for line in MANIFEST.read_text(encoding="utf-8").splitlines() if line]
    return [n for n in names if not (SNAP / n).exists()], len(names)


def _forward_tree_state():
    return {str(p.relative_to(REPO)): forward_common.sha256_file(p)
            for p in sorted((REPO / "forward").rglob("*")) if p.is_file()}


def test_committed_universe_matches_gate_pinned_sha256():
    digest = hashlib.sha256(FROZEN.read_bytes()).hexdigest()
    assert digest == GATE_PIN, (
        f"forward/cycle_001/universe.json sha256 {digest} ≠ 게이트 핀 {GATE_PIN} "
        "— 동결 산출물 무결성 위반 (INV-06)")
    assert GATE_PIN in GATE.read_text(encoding="utf-8"), (
        "OWNER_LAUNCH_GATE.md에서 핀 sha256을 찾지 못함 — 핀 표류")


def test_offline_recompute_reproduces_frozen_universe(tmp_path, monkeypatch):
    missing, total = _missing_snapshot_files()
    if missing:
        pytest.skip(
            f"T₀ 스냅샷 불완전: {len(missing)}/{total} 파일 부재 "
            "(submissions_CIK*.json은 git 밖 — 전체 스냅샷 보유 머신에서 실측)")

    for var in forward_common.METERED_CREDENTIAL_VARS:
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setattr(urllib.request, "urlopen", _refuse_network)
    monkeypatch.setattr(forward_enumerate, "_provenance", [])

    before = _forward_tree_state()
    out = tmp_path / "universe_recomputed.json"
    monkeypatch.setattr(sys, "argv",
                        ["forward_enumerate.py", "--offline", "--out", str(out)])
    assert forward_enumerate.main() == 0

    assert out.read_bytes() == FROZEN.read_bytes(), (
        "--offline 재계산이 동결 universe.json과 바이트 불일치 — 봉인 창 "
        "개막 명령이 창 안에서 실패한다 (OWNER_LAUNCH_GATE §4 (1))")
    assert _forward_tree_state() == before, "재계산이 forward/ 하위를 수정했다"
