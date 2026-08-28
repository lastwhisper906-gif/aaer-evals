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


# ── R14-3(a): verify()·check_schema()의 판별 leg 고정 ─────────────────────
#
# INV-05의 `make verify-public`은 "manifest PASS (N files)"를 2026-07-05 데이터
# 소실 사고 이후 커밋된 corpus와 디스크가 바이트 동일하다는 증거로 인쇄한다.
# 그런데 verify()는 스위트 어디서도 호출되지 않았고 (`verify_manifest.verify(`
# grep 0건), 해시 대조 `elif sha256_of(p) != f["sha256"]:` → `elif False:` 도,
# check_schema의 64-hex 길이 검사 → `if False:` 도 0 red였다. 유일한 기존
# 테스트는 **정상** 매니페스트에 대해 check_schema(m) == []만 보므로 어떤
# leg도 변별하지 못한다. 이 루프가 그 두 파일의 가장 유력한 편집자다.

def _entry(path: str, blob: bytes, **extra) -> dict:
    import hashlib
    return {"path": path, "size": len(blob),
            "sha256": hashlib.sha256(blob).hexdigest(),
            "fetched_at": "2026-07-05T00:00:00+00:00",
            "source_url": f"https://example.invalid/{path}", **extra}


def _manifest_of(entries: list[dict]) -> dict:
    return {"manifest_version": 1, "file_count": len(entries),
            "total_bytes": sum(e["size"] for e in entries), "files": entries}


def _two_file_corpus(tmp_path, monkeypatch):
    """디스크 2파일 + 그것과 정합한 매니페스트 — 무오류 기준선."""
    data = tmp_path / "aaer-data"
    (data / "TK01" / "xbrl").mkdir(parents=True)
    a, b = data / "TK01/xbrl/a.json", data / "TK01/xbrl/b.json"
    a.write_bytes(b'{"a": 1}')
    b.write_bytes(b'{"b": 2}')
    monkeypatch.setattr(vm, "DATA_DIR", data)
    m = _manifest_of([_entry("TK01/xbrl/a.json", a.read_bytes()),
                      _entry("TK01/xbrl/b.json", b.read_bytes())])
    assert vm.verify(m) == [], "기준선이 무오류여야 각 leg를 격리 측정할 수 있다"
    return data, a, b, m


def test_verify_reports_exactly_one_error_per_disk_divergence(tmp_path, monkeypatch):
    """R14-3(a): 네 가지 이탈 각각이 정확히 하나의 오류로 보고된다.

    같은 크기의 바이트 변경은 크기 leg를 지나 해시 leg에서만 잡히므로,
    HASH MISMATCH 케이스가 해시 대조의 유일한 고정점이다."""
    data, a, b, m = _two_file_corpus(tmp_path, monkeypatch)

    a.write_bytes(b'{"a": 9}')  # 같은 크기, 다른 바이트
    errs = vm.verify(m)
    assert errs == ["HASH MISMATCH: TK01/xbrl/a.json"], errs

    a.write_bytes(b'{"a": 1, "more": 1}')  # 크기까지 변경
    errs = vm.verify(m)
    assert len(errs) == 1 and errs[0].startswith("SIZE MISMATCH: TK01/xbrl/a.json"), errs

    a.unlink()
    errs = vm.verify(m)
    assert len(errs) == 1 and errs[0].startswith("MISSING: TK01/xbrl/a.json"), errs

    a.write_bytes(b'{"a": 1}')
    (data / "TK01/xbrl/c.json").write_bytes(b"{}")
    errs = vm.verify(m)
    assert len(errs) == 1 and errs[0].startswith("EXTRA: TK01/xbrl/c.json"), errs


def test_check_schema_catches_malformed_entries(tmp_path):
    """R14-3(a): 자체 정합성 leg — 각 결함이 정확히 하나의 오류."""
    good = _entry("TK01/xbrl/a.json", b"{}")

    short = dict(good, sha256=good["sha256"][:63])
    errs = vm.check_schema(_manifest_of([short]))
    assert len(errs) == 1 and "sha256 형식 오류" in errs[0], errs

    dup = _manifest_of([good, dict(good)])
    errs = vm.check_schema(dup)
    assert len(errs) == 1 and errs[0].startswith("중복 path:"), errs

    orphan = dict(good, source_url=None)
    errs = vm.check_schema(_manifest_of([orphan]))
    assert len(errs) == 1 and "source_url도 derived_from도 없음" in errs[0], errs
    # derived_from이 있으면 같은 항목이 적법하다 (귀속 경로가 둘이다)
    assert vm.check_schema(_manifest_of([dict(orphan, derived_from="x")])) == []
