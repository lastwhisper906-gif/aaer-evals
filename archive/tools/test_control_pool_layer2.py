"""R3-3: 대조군 풀 layer-2 해시 게이트 — 4개 풀 전부, 경로 이식성.

동결 MANIFEST.sha256들은 stale 클론 절대 경로로 키가 박혀 layer-2가 죽어
있었다. 병행 MANIFEST.relpaths.sha256(키 재작성, 재해시 아님)을 우선 사용해
현재 체크아웃 어디서든 검증이 살아난다. in-repo 항목은 항상 검증,
BIG_DIR(~/aaer-data/_rp08) 항목은 코퍼스 부재 시 skip.
"""
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_control_input as vci

REPO = Path(__file__).resolve().parents[1]
POOLS = ["runs/rp08/control_pool_raw", "runs/wave2/control_pool_raw",
         "runs/rp09/control_pool_raw", "runs/holdout/controls/pool_raw"]
DATA_ROOT = Path.home() / "aaer-data"


def _layer2(pool_dir: Path, repo: Path | None = None) -> list:
    problems: list = []
    # big_dir=None: 공유 코퍼스의 미등재-파일 스윕 제외 (등재분 검증은 전건)
    vci.layer2_hashes(problems, manifest_path=pool_dir / "MANIFEST.sha256",
                      raw_dir=pool_dir, repo=repo, big_dir=None)
    return problems


@pytest.mark.parametrize("pool", POOLS)
def test_layer2_clean_from_this_checkout(pool):
    problems = _layer2(REPO / pool)
    if not (DATA_ROOT / "_rp08").exists():
        problems = [p for p in problems
                    if not p["item"].startswith(str(DATA_ROOT))
                    or "파일 부재" not in p["reason"]]
    assert problems == [], problems[:5]


def test_resolver_never_consults_stale_clone_paths():
    stale = "/Users/chaeryeollee/Documents/aaer-evals/runs/rp08/control_pool_raw/x.atom"
    resolved = vci.resolve_manifest_key(stale)
    assert resolved == vci.REPO / "runs/rp08/control_pool_raw/x.atom"
    assert not str(resolved).startswith("/Users/chaeryeollee/Documents"), \
        "stale 클론 절대 경로가 그대로 참조됨"
    data = vci.resolve_manifest_key("/Users/chaeryeollee/aaer-data/_rp08/f/CIK1.json")
    assert data == Path.home() / "aaer-data/_rp08/f/CIK1.json"
    assert vci.resolve_manifest_key("~/aaer-data/_rp08/y.json") == \
        Path.home() / "aaer-data/_rp08/y.json"
    assert vci.resolve_manifest_key("runs/rp09/control_pool_raw/z.atom") == \
        vci.REPO / "runs/rp09/control_pool_raw/z.atom"


def _copy_pool(tmp_path: Path, pool: str) -> Path:
    dst = tmp_path / pool
    shutil.copytree(REPO / pool, dst)
    return dst


def test_one_byte_mutation_in_repo_pool_file_fails(tmp_path):
    dst = _copy_pool(tmp_path, "runs/rp09/control_pool_raw")
    victim = dst / "pool_extract.json"
    data = bytearray(victim.read_bytes())
    data[0] ^= 0xFF
    victim.write_bytes(bytes(data))
    problems = _layer2(dst, repo=tmp_path)
    assert any("sha256 불일치" in p["reason"] for p in problems), problems[:5]


def test_legacy_manifest_generation_still_resolves(tmp_path):
    """정규화 매니페스트 부재 시 구세대(절대 경로 키)도 마커 재정박으로 해석."""
    dst = _copy_pool(tmp_path, "runs/rp09/control_pool_raw")
    (dst / "MANIFEST.relpaths.sha256").unlink()
    problems = _layer2(dst, repo=tmp_path)
    assert problems == [], problems[:5]
