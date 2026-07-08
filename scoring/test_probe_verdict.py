"""probe_verdict 판정 규칙 테스트 (감사 B17 — 이 모듈은 테스트가 없었다).

D7 오염 판정·name-ID rate를 결정하는 name_match/within_2pct/normalize를 고정한다.
발견: 접두열(prefix) 규칙은 단일 공통 토큰을 과매칭할 수 있으나(예 "Apple"⊂"Apple
Hospitality"), 커밋된 실제 프로브 데이터의 매치 3건(Hertz·LivePerson·CSC)은 전부
정당한 인식이라 어떤 동결 판정도 이 이론적 과매칭의 영향을 받지 않는다. 따라서 규칙은
현행 유지(정확)하고, 여기서 현행 동작을 회귀 고정한다. 규칙을 조이면 정당한 매치(단일
토큰 'liveperson' 등)를 깨고 동결 name-ID를 바꾸므로 = owner-gate(Q-E02)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe_verdict import name_match, normalize, within_2pct


def test_normalize_strips_suffix_and_punct():
    assert normalize("Orthofix International N.V.") == ("orthofix", "n", "v")
    assert normalize("LIVEPERSON INC") == ("liveperson",)
    assert normalize("The Hertz Corporation") == ("hertz",)


def test_full_equality_and_suffix_insensitivity():
    assert name_match("Weis Markets, Inc.", "Weis Markets")
    assert name_match("Genie Energy Ltd.", "GENIE ENERGY")
    assert not name_match("unknown", "Hertz Global Holdings")


def test_real_committed_prefix_matches_are_true():
    # 커밋 데이터의 실제 접두열 매치 3건 — 전부 정당한 인식 (회귀 고정)
    assert name_match("Hertz Global Holdings, Inc. (Hertz Corporation)", "Hertz Global Holdings, Inc.")
    assert name_match("LivePerson, Inc. (ticker: LPSN)", "LIVEPERSON INC")
    assert name_match("Computer Sciences Corporation (CSC)", "Computer Sciences Corporation")
    assert name_match("Orthofix", "Orthofix International N.V.")  # docstring 예시(약칭)


def test_known_prefix_overmatch_is_documented_not_a_regression():
    # 이론적 과매칭: 단일 공통 토큰이 다른 회사의 접두를 이룸. 현행 규칙은 True를 준다.
    # 커밋 데이터엔 이런 케이스가 없어 동결 판정 무영향. 값이 바뀌면(누가 규칙을 조이면)
    # 이 테스트가 실패해 '동결 name-ID 변경 = owner-gate'임을 상기시킨다.
    assert name_match("Apple", "Apple Hospitality REIT") is True
    # 완전 무관한 이름은 매치 안 함
    assert name_match("Microsoft", "Hertz Global Holdings") is False
    assert name_match("Weis", "Genie Energy") is False


def test_within_2pct():
    assert within_2pct(100, 100)
    assert within_2pct(101.5, 100)         # 1.5% 이내
    assert not within_2pct(103, 100)       # 3% 초과
    assert not within_2pct(None, 100)
    assert not within_2pct(100, 0)         # 0 나눗셈 방지
    assert not within_2pct("x", 100)       # 파싱 실패
