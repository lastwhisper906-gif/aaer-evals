"""tools/ 테스트 공통 픽스처.

R15-1: 수집 로그의 정본 위치가 `REPO/data/provenance/fetch_log.jsonl`(git
관리)로 옮겨졌으므로, 그 경로를 따로 격리하지 않는 테스트는 픽스처 행을
**실제 저장소 파일에 append한다** — R14-5 탐침이 정확히 그렇게 해서 64.5 KB의
tmp 경로 행을 만들었다. 아래 autouse 픽스처가 테스트마다 임시 루트를 꽂아
writer·가드·source_manifest를 **함께** 옮긴다 (한쪽만 옮길 수 없는 것이 R15-1
설계의 요점이므로 seam도 단일 지점이다).

정본 해석 자체를 검사하는 테스트는 `FETCH_LOG_ROOT`를 None으로 되돌려
`fetch_log_path() == REPO / FETCH_LOG_REL`을 직접 확인한다 — seam이 프로덕션
경로를 가리는 일이 없도록 그 테스트가 고정한다
(test_forward_tools.py::test_canonical_fetch_log_lives_in_git_outside_the_corpus).
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))


@pytest.fixture(autouse=True)
def isolate_fetch_log(tmp_path_factory, monkeypatch):
    import fetch_xbrl_facts as fxf
    monkeypatch.setattr(
        fxf, "FETCH_LOG_ROOT", tmp_path_factory.mktemp("fetch-log-root"))
