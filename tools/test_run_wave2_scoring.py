"""run_wave2_scoring._cutoff_name 회귀 테스트 (R1-3 / OV-002).

EDGAR 청크 파일(CIK…-submissions-001.json)은 사전순으로 본 파일보다 앞서고
formerNames를 싣지 않는다 — 첫 존재 파일만 보고 끊으면 컷오프 시점 사명
재구성이 통째로 건너뛰어져 후신 사명이 페이로드에 실린다 (§5-1 look-ahead).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_wave2_scoring import _cutoff_name


def _write(p: Path, obj: dict) -> Path:
    p.write_text(json.dumps(obj), encoding="utf-8")
    return p


def test_chunk_file_without_formernames_does_not_mask_main_file(tmp_path):
    chunk = _write(tmp_path / "CIK0000000001-submissions-001.json",
                   {"filings": {"files": []}})  # 청크: formerNames 없음
    main = _write(tmp_path / "CIK0000000001.json",
                  {"formerNames": [{"name": "OLD CORP",
                                    "from": "2000-01-01T00:00:00.000Z",
                                    "to": "2020-01-01T00:00:00.000Z"}]})
    paths = sorted([chunk, main])  # 사전순: 청크가 먼저 ('-' < '.')
    assert paths[0] == chunk
    assert _cutoff_name("1", "2015-06-30", "NEW CORP", paths) == "OLD CORP"


def test_no_span_anywhere_falls_through_to_regex_cleanup(tmp_path):
    chunk = _write(tmp_path / "CIK0000000002-submissions-001.json", {})
    main = _write(tmp_path / "CIK0000000002.json",
                  {"formerNames": [{"name": "ANCIENT CORP",
                                    "from": "1990-01-01T00:00:00.000Z",
                                    "to": "1995-01-01T00:00:00.000Z"}]})  # 컷오프 밖
    got = _cutoff_name("2", "2015-06-30", "CURRENT CO (n/k/a Future Co)",
                       sorted([chunk, main]))
    assert got == "CURRENT CO"


def test_earliest_covering_span_wins_across_files(tmp_path):
    main = _write(tmp_path / "CIK0000000003.json",
                  {"formerNames": [
                      {"name": "MID CORP", "from": "2010-01-01T00:00:00.000Z",
                       "to": "2018-01-01T00:00:00.000Z"},
                      {"name": "EARLY CORP", "from": "2000-01-01T00:00:00.000Z",
                       "to": "2016-01-01T00:00:00.000Z"}]})
    # 기존 규약 유지: 컷오프를 덮는 span 중 to가 가장 이른 것 (min)
    assert _cutoff_name("3", "2015-06-30", "NEW", [main]) == "EARLY CORP"
