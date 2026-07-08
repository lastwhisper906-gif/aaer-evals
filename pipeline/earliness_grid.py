"""earliness_grid.py — E2 조기성 스냅샷 그리드 계산 (사전등록: analysis/EARLINESS_PLAN.md).

이 모듈은 **look-ahead-critical** 하다. 스냅샷 j의 컷오프를 잘못 계산하면 그 시점에
공개되지 않았던 제출이 조용히 페이로드에 들어가 백테스트가 오염된다(§5-1). 따라서
핵심 로직(compute_snapshot_grid)은 순수 함수로 분리해 오프라인·합성 픽스처로 전수
검증한다 (test_earliness_grid.py). I/O 래퍼(build_case_grid)는 기존
build_payload.load_filing_chronology(filed<=cutoff 단일 필터)만 재사용한다.

사전등록 규약 (EARLINESS_PLAN §2, 불변 — freeze-then-run):
  - 스냅샷 j의 컷오프 = 폭로 컷오프 이전 j번째 최신 10-K/10-Q 제출 filed일 + 1일.
  - 스냅샷 0 = 기존 본실행(폭로 컷오프) 점수 재사용 — 이 모듈은 j>=1만 생성.
  - 케이스당 스냅샷 상한 8. 얕은 것(폭로 근접, j=1)부터.

가드 (이 모듈이 추가하는 look-ahead 방어 — 사전등록 +1일 규칙을 바꾸지 않고 위반만 차단):
  G1 폭로 상한: 어떤 스냅샷 컷오프도 폭로 컷오프를 초과할 수 없다(초과 시 그 스냅샷
     drop, reason=exceeds_revelation). 폭로일 이후 데이터 접근 원천 차단.
  G2 깊이 무결성: +1일 오프셋이 인접일 신규 제출을 끌어들이면(스냅샷 j에 f_{j-1}이
     포함되면) 그 스냅샷의 정보집합이 의도(=j번째까지)와 달라진다 → drop,
     reason=adjacent_filing_leak. "이웃 점 차 = 제출 1건 제거" 해석성(§2)도 보존.
  G3 중복 컷오프: 같은 filed일이 여러 건이어도 스냅샷 컷오프는 distinct filed일 기준.
"""
from __future__ import annotations

import dataclasses
import datetime

FORM_PREFIXES = ("10-K", "10-Q")  # XBRL 연차/분기 제출 (수정본 10-K/A·10-Q/A 포함 — 아래 참조)
DEFAULT_MAX_SNAPSHOTS = 8
DEFAULT_DAY_OFFSET = 1  # EARLINESS_PLAN §2: "+1일" (불변)


@dataclasses.dataclass(frozen=True)
class Snapshot:
    j: int                          # 스냅샷 인덱스 (1 = 최신 제출, 폭로 근접)
    cutoff: datetime.date           # 이 스냅샷의 as-of 컷오프 (filed(f_j) + offset)
    boundary_filed: datetime.date   # 의도한 j번째 최신 제출의 filed일 (f_j)


@dataclasses.dataclass(frozen=True)
class DroppedSnapshot:
    j: int
    boundary_filed: datetime.date
    reason: str                     # exceeds_revelation | adjacent_filing_leak


@dataclasses.dataclass(frozen=True)
class Grid:
    snapshots: list[Snapshot]       # 채점 대상 (얕은 것부터, j 오름차순)
    dropped: list[DroppedSnapshot]  # 가드에 걸려 제외된 스냅샷 (감사 기록)
    max_depth: int                  # 폭로 전 distinct 제출 filed일 수 (상한 적용 전)


def is_periodic_filing(form: str) -> bool:
    """10-K/10-Q(및 수정본 /A)인가. 수정본 포함 이유: XBRL을 실은 정기 제출이며
    각각 distinct filed 사건이라 스냅샷 깊이의 한 점이 된다. (형식 판정은 감사 대상 —
    수정본 배제가 필요하면 owner 규약으로 전환; runbook에 명시.)"""
    f = form.upper().strip()
    return any(f == p or f.startswith(p + "/") or f == p + "T" for p in FORM_PREFIXES)


def compute_snapshot_grid(periodic_filed_dates: list[datetime.date],
                          all_filed_dates: list[datetime.date],
                          revelation_cutoff: datetime.date,
                          *,
                          max_snapshots: int = DEFAULT_MAX_SNAPSHOTS,
                          day_offset: int = DEFAULT_DAY_OFFSET) -> Grid:
    """순수 함수 — look-ahead-critical 핵심. 모든 입력 날짜는 filed<=revelation_cutoff 전제.

    periodic_filed_dates: 10-K/10-Q(정기) 제출들의 filed일 (스냅샷 경계 후보).
    all_filed_dates:      모든 제출(정기+8-K 등)의 filed일 — G2 깊이 무결성 검사용
                          (스냅샷 컷오프가 인접 신규 '정기' 제출을 끌어들이는지 판정).
    반환: Grid (통과 스냅샷 + drop 사유 + 최대깊이). j=1이 최신(폭로 근접).
    """
    if day_offset < 0:
        raise ValueError("day_offset는 음수 불가")
    # distinct filed일, 최신순(내림차순). 중복 filed일(G3)은 하나의 경계로 축약.
    periodic_desc = sorted({d for d in periodic_filed_dates if d <= revelation_cutoff},
                           reverse=True)
    all_sorted = sorted(d for d in all_filed_dates if d <= revelation_cutoff)
    max_depth = len(periodic_desc)
    offset = datetime.timedelta(days=day_offset)

    snapshots: list[Snapshot] = []
    dropped: list[DroppedSnapshot] = []
    for j in range(1, min(max_depth, max_snapshots) + 1):
        boundary = periodic_desc[j - 1]      # j번째 최신 정기 제출 filed일 (f_j)
        cutoff = boundary + offset
        # G1 폭로 상한 — 폭로 컷오프 초과 절대 불가 (강한 look-ahead 차단).
        if cutoff > revelation_cutoff:
            dropped.append(DroppedSnapshot(j, boundary, "exceeds_revelation"))
            continue
        # G2 깊이 무결성 — filed<=cutoff 인 최신 제출이 f_j를 넘어서면(인접일 신규 제출
        #    유입) 정보집합이 의도와 다름 → drop. (all_filed 기준: 정기·비정기 무관하게
        #    '그 시점에 이미 공개된 최신 제출'이 f_j여야 스냅샷 깊이가 정의대로다.)
        included = [d for d in all_sorted if d <= cutoff]
        if included and max(included) > boundary:
            dropped.append(DroppedSnapshot(j, boundary, "adjacent_filing_leak"))
            continue
        snapshots.append(Snapshot(j=j, cutoff=cutoff, boundary_filed=boundary))
    # 얕은 것(j=1, 폭로 근접)부터 — EARLINESS_PLAN §5 채점 순서.
    snapshots.sort(key=lambda s: s.j)
    return Grid(snapshots=snapshots, dropped=dropped, max_depth=max_depth)
