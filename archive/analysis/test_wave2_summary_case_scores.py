"""wave2_summary.md의 케이스별 산문 점수 ↔ runs/ 산출물 드리프트 잠금 (R12-7).

`tools/reproduce_analysis.py`는 게시 수치를 커밋된 JSON과 대조하지만(101/101),
**산문 안의 케이스별 점수**를 산출물에 묶는 게이트는 없었다. 그 사각에서
`analysis/wave2_summary.md:52`의 미탐 2건이 서로의 점수를 달고 동결됐다:
CSC와 BRX가 정확히 교환돼 있다 (산출물 참값 CSC 40 · BRX 20).

  case_52 → id map T02 → CSC → runs/wave2/scores/case_52.json = 40
  case_67 → id map T20 → BRX → runs/wave2/scores/case_67.json = 20

다른 표면은 모두 옳다 (atlas/INDEX.md:15,21 · atlas/PATTERNS.md:129,169 ·
analysis/error_analysis_wave2_holdout.md:98,114). 통계 영향 없음 — 미탐 2/9,
플래그 7/9, R3 3/9 모두 불변이며 어느 통계도 이 산문에서 점수를 읽지 않는다.

그 파일은 INV-06 동결(E-001 범위)이라 고칠 수 없다. 그래서 이 잠금은 양쪽을
모두 핀한다 — 산출물의 참값과, 동결 산문의 (틀린) 값. 어느 쪽이 움직여도,
또는 동결 파일이 조용히 '수정'되어도(INV-06 위반) 스위트가 붉어진다.

**미결(R12-7 BLOCKED)**: 이 전치의 ERRATA 등재는 아직 없다 — ERRATA.md가
하네스 봉인 매니페스트(1,634파일)에 들어 있어 append가 `seal_check`를
깨뜨리고, 재봉인은 소유자 전용이다. 소유자 판정 후 E-0NN을 추가하면 이
모듈 상단 기록을 그 항목 참조로 대체한다.
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SUMMARY = REPO / "analysis/wave2_summary.md"

# 모듈 독스트링에 기록된 상태 — 산출물의 참값과 동결 산문의 전치값
ARTIFACT_SCORES = {"CSC": 40, "BRX": 20}
FROZEN_PROSE_SCORES = {"CSC": 20, "BRX": 40}
TICKER_CASES = {"CSC": "case_52", "BRX": "case_67"}


def _prose_scores() -> dict[str, int]:
    """미탐 불릿에서 `**TICKER**(p=NN)` 쌍을 뽑는다."""
    text = SUMMARY.read_text(encoding="utf-8")
    line = next(ln for ln in text.splitlines() if "미탐 2" in ln)
    return {t: int(p) for t, p in re.findall(r"\*\*([A-Z]+)\*\*\(p=(\d+)\)", line)}


def _artifact_score(case_id: str) -> int:
    doc = json.loads((REPO / f"runs/wave2/scores/{case_id}.json").read_text(
        encoding="utf-8"))
    return doc["misstatement_probability"]


def test_id_map_resolves_the_two_miss_cases():
    """티커 ↔ case_id 결합은 id map + 후보 등록부를 경유해야 의미가 있다."""
    mapping = json.loads((REPO / "scoring/id_mapping_wave2.json").read_text(
        encoding="utf-8"))["mapping"]
    candidates = {c["case_id"]: c for c in json.loads(
        (REPO / "data/candidates/candidates_wave2.json").read_text(
            encoding="utf-8"))["candidates"]}
    for ticker, case_id in TICKER_CASES.items():
        assert candidates[mapping[case_id]]["ticker"] == ticker


def test_artifact_scores_are_pinned():
    for ticker, case_id in TICKER_CASES.items():
        assert _artifact_score(case_id) == ARTIFACT_SCORES[ticker], ticker


def test_frozen_prose_matches_its_recorded_state():
    """동결 산문은 E-004에 기록된 그대로여야 한다 — 변경도, 조용한 수정도 불가."""
    assert _prose_scores() == FROZEN_PROSE_SCORES


def test_prose_and_artifacts_are_exactly_transposed_as_recorded():
    """기록된 주장 자체: 두 값이 서로 교환돼 있다 (다른 형태의 오류가 아니라)."""
    prose = _prose_scores()
    assert prose["CSC"] == ARTIFACT_SCORES["BRX"]
    assert prose["BRX"] == ARTIFACT_SCORES["CSC"]
    assert prose != ARTIFACT_SCORES, "전치가 해소됐다면 이 모듈 기록을 갱신하라"
