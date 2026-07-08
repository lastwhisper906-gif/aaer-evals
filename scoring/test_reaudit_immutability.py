"""Track 4 재감사 회귀 락 — IMMUTABILITY 불변 (runs/ 변조 매니페스트).

NEW 파일(distinct name). frozen 산출물을 수정하지 않고, runs/MANIFEST.sha256 이
네 개의 frozen 결과 세트를 실제로 커버하며 변조를 탐지할 민감도를 갖는지 락한다.

커버하는 공백 (재감사 finding):
  F4  verify_blindness.check_manifest 의 스코프(runs/ 전수)가 frozen 4세트
      (runs/main · runs/wave2/scores · runs/perturbed · runs/holdout/scores)를
      전부 포함하는지 — 세트가 매니페스트에서 조용히 빠지는 회귀를 차단.
  F5  매니페스트 해시가 현행 디스크와 일치(드리프트 0)하고, 1바이트 변조가
      기록 해시와 달라짐(탐지 민감도)을 락 — 매니페스트가 죽은 파일이 아니라
      실제 tamper 검출기임을 증명.
"""
import hashlib
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "runs" / "MANIFEST.sha256"

FROZEN_SETS = ["runs/main/", "runs/wave2/scores/",
               "runs/perturbed/", "runs/holdout/scores/"]


def _manifest_entries():
    """{relpath: sha256} — 'HASH  path' 라인 파싱."""
    entries = {}
    for ln in MANIFEST.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        h, path = ln.split("  ", 1)
        entries[path] = h
    return entries


def test_manifest_exists_and_nonempty():
    assert MANIFEST.is_file(), "runs/MANIFEST.sha256 부재 — IMMUTABILITY 기준선 없음"
    assert _manifest_entries(), "매니페스트 비어 있음"


@pytest.mark.parametrize("prefix", FROZEN_SETS)
def test_manifest_covers_each_frozen_set(prefix):
    """frozen 4세트 각각이 매니페스트에 최소 1개 파일로 기재돼 있어야 한다."""
    entries = _manifest_entries()
    covered = [p for p in entries if p.startswith(prefix)]
    assert covered, f"{prefix} 이 runs/MANIFEST.sha256 에서 미커버 — 변조 탐지 사각"


@pytest.mark.parametrize("prefix", FROZEN_SETS)
def test_frozen_files_match_manifest_hash(prefix):
    """각 frozen 세트의 기재 파일들이 현행 디스크 해시와 일치 (드리프트 0).

    이것이 실패하면 frozen 결과가 이미 변조됐다는 뜻 = 세션 오염 신호."""
    entries = _manifest_entries()
    checked = 0
    for relpath, recorded in entries.items():
        if not relpath.startswith(prefix):
            continue
        p = REPO / relpath
        assert p.is_file(), f"매니페스트 기재 파일 부재(변조 의심): {relpath}"
        actual = hashlib.sha256(p.read_bytes()).hexdigest()
        assert actual == recorded, f"HASH MISMATCH (frozen 변조): {relpath}"
        checked += 1
    assert checked, f"{prefix} 기재 파일 0개 — 커버리지 테스트와 모순"


def test_manifest_detects_single_byte_tamper():
    """탐지 민감도: frozen 파일 내용에 1바이트만 더해도 기록 해시와 달라진다.

    디스크는 건드리지 않는다 — 메모리에서 bytes 를 변형해 해시만 비교한다."""
    entries = _manifest_entries()
    sample = next(p for p in entries if p.startswith("runs/main/"))
    original = (REPO / sample).read_bytes()
    assert hashlib.sha256(original).hexdigest() == entries[sample]
    tampered = original + b" "
    assert hashlib.sha256(tampered).hexdigest() != entries[sample], (
        "1바이트 변조가 기록 해시와 동일 — 매니페스트가 tamper 를 못 잡음")


def test_no_frozen_file_missing_from_manifest():
    """디스크의 frozen 4세트 파일이 전부 매니페스트에 기재돼 있어야 한다
    (매니페스트 미기재 파일 = verify_blindness 의 EXTRA FAIL 대상)."""
    entries = set(_manifest_entries())
    for prefix in FROZEN_SETS:
        root = REPO / prefix
        if not root.is_dir():
            continue
        for p in sorted(root.rglob("*")):
            if not p.is_file() or p.name in ("MANIFEST.sha256", ".DS_Store"):
                continue
            rel = p.relative_to(REPO).as_posix()
            assert rel in entries, f"디스크 파일이 매니페스트에 미기재: {rel}"
