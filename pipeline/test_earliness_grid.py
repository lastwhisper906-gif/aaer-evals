"""earliness_grid 순수 로직 전수 검증 (look-ahead-critical — 캐시 불요, CI에서 실행).

test_build_payload.py는 ~/aaer-data 부재 시 skip되지만, 이 테스트는 순수 함수라
어떤 환경에서도 돈다 — 스냅샷 컷오프 로직의 강제 지점이 CI에 상주하도록.
"""
import datetime as dt

import earliness_grid as eg

D = dt.date


def _grid(periodic, allf=None, rev=D(2016, 1, 1), **kw):
    return eg.compute_snapshot_grid(periodic, allf if allf is not None else periodic, rev, **kw)


def test_basic_grid_cutoffs_and_order():
    # 정기 제출 4건, 서로 한 달 이상 간격 → 스냅샷 4개, j=1이 최신(폭로 근접).
    filed = [D(2015, 1, 15), D(2015, 4, 20), D(2015, 7, 25), D(2015, 10, 30)]
    g = _grid(filed, rev=D(2015, 12, 31))
    assert [s.j for s in g.snapshots] == [1, 2, 3, 4]
    # j=1 = 최신(10/30) +1일; j=4 = 가장 오래된(1/15) +1일
    assert g.snapshots[0].cutoff == D(2015, 10, 31)
    assert g.snapshots[0].boundary_filed == D(2015, 10, 30)
    assert g.snapshots[3].cutoff == D(2015, 1, 16)
    assert g.max_depth == 4
    assert g.dropped == []


def test_max_snapshots_cap():
    filed = [D(2010, 1, 1) + dt.timedelta(days=90 * i) for i in range(20)]
    g = _grid(filed, rev=D(2030, 1, 1), max_snapshots=8)
    assert len(g.snapshots) == 8
    assert g.max_depth == 20  # 상한 적용 전 깊이는 기록


def test_G1_exceeds_revelation_is_dropped():
    # 최신 정기 제출이 폭로 '전일'(컷오프)과 같은 날 → +1일이면 폭로일 = 초과 → drop.
    rev = D(2016, 2, 28)
    filed = [D(2016, 2, 28), D(2015, 11, 30)]
    g = _grid(filed, rev=rev)
    reasons = {(d.j, d.reason) for d in g.dropped}
    assert (1, "exceeds_revelation") in reasons
    # j=2(11/30 +1 = 12/1)는 통과
    assert [s.j for s in g.snapshots] == [2]
    # 통과 스냅샷은 모두 폭로 컷오프 이하 (불변 속성)
    assert all(s.cutoff <= rev for s in g.snapshots)


def test_G2_adjacent_filing_leak_is_dropped():
    # 두 정기 제출이 연속일(3/14, 3/15) → j=2 컷오프(3/14+1=3/15)가 신규 제출(3/15)을
    # 끌어들임 → 깊이 무결성 위반 → drop. (폭로 이후는 아니지만 스냅샷 깊이가 어긋남.)
    rev = D(2016, 1, 1)
    filed = [D(2015, 3, 14), D(2015, 3, 15), D(2014, 6, 1)]
    g = _grid(filed, rev=rev)
    reasons = {(d.j, d.reason) for d in g.dropped}
    assert (2, "adjacent_filing_leak") in reasons
    # 통과 스냅샷 각각: filed<=cutoff 인 최신 제출이 정확히 그 경계여야 한다 (누출 0)
    allf = sorted(filed)
    for s in g.snapshots:
        included = [d for d in allf if d <= s.cutoff]
        assert max(included) == s.boundary_filed


def test_G2_uses_all_filings_not_just_periodic():
    # 8-K(비정기)가 정기 제출 하루 뒤에 있어도 스냅샷 컷오프가 그걸 끌어들이면 깊이 어긋남.
    rev = D(2016, 1, 1)
    periodic = [D(2015, 3, 14), D(2014, 6, 1)]
    allf = periodic + [D(2015, 3, 15)]  # 8-K 등
    g = eg.compute_snapshot_grid(periodic, allf, rev)
    reasons = {(d.j, d.reason) for d in g.dropped}
    assert (1, "adjacent_filing_leak") in reasons


def test_G3_duplicate_filed_dates_collapse():
    # 같은 날 두 건(10-K + 10-K/A) → 하나의 경계로 축약, 깊이 3이 아니라 2.
    filed = [D(2015, 5, 1), D(2015, 5, 1), D(2014, 5, 1)]
    g = _grid(filed, rev=D(2015, 12, 31))
    assert g.max_depth == 2
    assert [s.boundary_filed for s in g.snapshots] == [D(2015, 5, 1), D(2014, 5, 1)]


def test_no_snapshot_ever_exceeds_revelation_property():
    # 무작위스런 다양한 배치에서도 반환 스냅샷은 전부 폭로 컷오프 이하 (핵심 불변).
    rev = D(2016, 6, 30)
    for shift in range(0, 400, 7):
        filed = [rev - dt.timedelta(days=shift + 30 * i) for i in range(6)]
        g = _grid(filed, rev=rev)
        assert all(s.cutoff <= rev for s in g.snapshots)


def test_empty_and_single():
    assert _grid([]).snapshots == []
    g = _grid([D(2015, 5, 1)], rev=D(2015, 12, 31))
    assert [s.j for s in g.snapshots] == [1]


def test_is_periodic_filing():
    assert eg.is_periodic_filing("10-K")
    assert eg.is_periodic_filing("10-Q")
    assert eg.is_periodic_filing("10-K/A")
    assert eg.is_periodic_filing("10-Q/A")
    assert not eg.is_periodic_filing("8-K")
    assert not eg.is_periodic_filing("4")
    assert not eg.is_periodic_filing("S-1")


def test_day_offset_zero_includes_boundary_only():
    filed = [D(2015, 3, 14), D(2015, 3, 15), D(2014, 6, 1)]
    g = _grid(filed, rev=D(2016, 1, 1), day_offset=0)
    # offset 0이면 컷오프=경계일, 인접 신규 유입 없음 → 누출 drop 없음
    assert not any(d.reason == "adjacent_filing_leak" for d in g.dropped)
    for s in g.snapshots:
        assert s.cutoff == s.boundary_filed
