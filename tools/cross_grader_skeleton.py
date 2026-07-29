"""교차 패밀리 채점자 스팟체크 — 호출 봉쇄(call-disabled) 스켈레톤 (BN-09 / D121).

specs/cross_grader.md (SPEC ONLY, 동결 — 커밋 4ee5e0b) §2의 선정 입력과
동결 루브릭 앵커 프롬프트 구조를 결정론적으로 적재만 한다. 채점자 호출
지점은 설계상 봉쇄되어 있다: 이 스크립트는 어떤 모델도 호출하지 않고
항상 비영(non-zero) 종료한다. 실 호출·채점자 모델 선정·표본 20건
freeze-commit은 전부 소유자 게이트 Q-F07 (docs/OWNER_QUEUE.md) 서명 후의
소유자 발사 단계다 — docs/CROSS_GRADER_OWNER_PACKET.md 참조.

- 네트워크 모듈 없음, 자격 증명 요구 없음, 표준 라이브러리 외 의존성 없음.
- 루브릭 앵커는 scoring/grader_runner.py에서 ast로 추출한다 (import 없음 —
  호출 기계 자체를 적재하지 않는다).
- 결정론: 벽시계·난수 없음. 셀 내 선정은 spec §2의 seed 20260712 산술.
"""
from __future__ import annotations

import ast
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SPEC_PATH = "specs/cross_grader.md"
RUBRIC_SOURCE = "scoring/grader_runner.py"
SEED = 20260712  # spec §2 — 셀 내 결정론 선정 seed
N_SAMPLE = 20  # spec §2
MIN_PER_TIER = 4  # spec §2 — 각 tier 최소 보장

# spec §2 tier 층화 — scoring/grades* 하위 모든 디렉토리는 여기 매핑되어야
# 한다. 미매핑 디렉토리는 fail-closed (조용한 포함/배제 금지). 매핑 자체는
# 소유자 패킷 §2에서 확인 대상.
TIER_BY_DIR = {
    "grades/main": "wave-1",
    "grades/perturbed": "wave-1",
    "grades_v2/controls": "wave-1",
    "grades_wave2": "wave-2",
    "grades_holdout": "holdout+E1",
    "grades_holdout_controls": "holdout+E1",
}

# dim4 0..3 → spec §2의 하/중/상 밴드 (기계적 밴딩 제안 — 소유자 패킷 §2
# 확인 대상): {0,1}=low, {2}=mid, {3}=high.
DIM4_BAND = {0: "low", 1: "low", 2: "mid", 3: "high"}
# spec §2 dim2 수준 {0,1,2}; 대조군 레코드는 dim2=null — 별도 수준으로 취급.
DIM2_LEVELS = (None, 0, 1, 2)


def fail(msg: str) -> None:
    print(f"FAIL (fail-closed): {msg}", file=sys.stderr)
    raise SystemExit(3)


def load_rubric_anchor() -> dict:
    """동결 루브릭 앵커 프롬프트(SYSTEM)와 채점 스키마를 ast로 추출한다.

    grader_runner를 import하지 않는다 — 이 파일 안에는 모델 호출 경로가
    존재할 수 없다 (테스트가 import 허용목록으로 강제).
    """
    tree = ast.parse((REPO / RUBRIC_SOURCE).read_text(encoding="utf-8"))
    found = {}
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id in ("SYSTEM", "GRADE_SCHEMA")):
            found[node.targets[0].id] = ast.literal_eval(node.value)
    missing = {"SYSTEM", "GRADE_SCHEMA"} - set(found)
    if missing:
        fail(f"{RUBRIC_SOURCE}에서 루브릭 앵커 추출 실패 — {sorted(missing)} 미발견")
    return {
        "system_prompt": found["SYSTEM"],
        "grade_schema": found["GRADE_SCHEMA"],
        "sha256": hashlib.sha256(found["SYSTEM"].encode("utf-8")).hexdigest(),
    }


def load_population() -> list[dict]:
    """spec §2 모집단: scoring/grades*/ 전체의 human_finalized 레코드."""
    records = []
    scoring = REPO / "scoring"
    for grades_dir in sorted(p for p in scoring.glob("grades*") if p.is_dir()):
        for f in sorted(grades_dir.rglob("*.json")):
            rel_dir = f.parent.relative_to(scoring).as_posix()
            tier = TIER_BY_DIR.get(rel_dir)
            if tier is None:
                fail(f"미매핑 grades 디렉토리 {rel_dir!r} — TIER_BY_DIR 확장 후 "
                     "소유자 패킷 §2 매핑 표를 갱신할 것")
            data = json.loads(f.read_text(encoding="utf-8"))
            if not data.get("_meta", {}).get("human_finalized"):
                continue
            dim2 = data.get("dim2_mechanism")
            dim4 = data.get("dim4_evidence_quality")
            if dim2 not in DIM2_LEVELS or dim4 not in DIM4_BAND:
                fail(f"{rel_dir}/{f.name}: dim2={dim2!r} dim4={dim4!r} — "
                     "spec §2 층화 수준 밖 (spec 확인 필요)")
            records.append({"key": f"{rel_dir}/{f.stem}", "tier": tier,
                            "dim2": dim2, "dim4_band": DIM4_BAND[dim4]})
    if not records:
        fail("모집단 0건 — scoring/grades*/ 적재 실패")
    return records


def stratify(records: list[dict]) -> dict:
    """셀 = (tier, dim2 수준, dim4 밴드) → case key 정렬 목록."""
    cells: dict = {}
    for r in records:
        cells.setdefault((r["tier"], r["dim2"], r["dim4_band"]), []).append(r["key"])
    for members in cells.values():
        members.sort()
    return cells


def _largest_remainder(sizes: dict, total: int) -> dict:
    """결정론 비례 배분 (최대 잔여, 동률은 키 문자열 정렬)."""
    pop = sum(sizes.values())
    quotas = {k: sizes[k] * total / pop for k in sizes}
    alloc = {k: int(quotas[k]) for k in sizes}
    leftover = total - sum(alloc.values())
    by_remainder = sorted(sizes, key=lambda k: (-(quotas[k] - alloc[k]), str(k)))
    for k in by_remainder[:leftover]:
        alloc[k] += 1
    return alloc


def _enforce_tier_minimum(alloc: dict, tier_sizes: dict) -> dict:
    """spec §2 각 tier 최소 4건 — 최대 배분 tier에서 결정론적으로 이전."""
    alloc = dict(alloc)
    for tier in sorted(alloc):
        floor = min(MIN_PER_TIER, tier_sizes[tier])
        while alloc[tier] < floor:
            donors = [t for t in sorted(alloc)
                      if t != tier and alloc[t] > min(MIN_PER_TIER, tier_sizes[t])]
            if not donors:
                fail("tier 최소 보장 불가 — 배분 산술 확인 필요")
            donor = max(donors, key=lambda t: (alloc[t], t))
            alloc[donor] -= 1
            alloc[tier] += 1
    return alloc


def select_sample(cells: dict, n: int = N_SAMPLE, seed: int = SEED) -> list[str]:
    """spec §2 선정 규칙의 기계적 적용 (소유자 패킷 §2에 동일 산술 재서술).

    tier 수준 최대-잔여 비례 배분(+최소 4) → tier 내 셀 수준 최대-잔여 →
    셀 내 case key 정렬 후 offset = seed mod m, 인덱스 (offset + ⌊i·m/c⌋)
    mod m 균등 간격 추출.
    """
    tier_sizes: dict = {}
    for (tier, _, _), members in cells.items():
        tier_sizes[tier] = tier_sizes.get(tier, 0) + len(members)
    if n > sum(tier_sizes.values()):
        fail(f"n={n} > 모집단 {sum(tier_sizes.values())}건")
    tier_alloc = _enforce_tier_minimum(_largest_remainder(tier_sizes, n), tier_sizes)
    selected: list[str] = []
    for tier in sorted(tier_alloc):
        tier_cells = {k: v for k, v in cells.items() if k[0] == tier}
        cell_sizes = {k: len(tier_cells[k])
                      for k in sorted(tier_cells, key=str)}
        cell_alloc = _largest_remainder(cell_sizes, tier_alloc[tier])
        for key in cell_sizes:
            count = cell_alloc[key]
            if not count:
                continue
            members = tier_cells[key]
            m = len(members)
            offset = seed % m
            selected.extend(members[(offset + (i * m) // count) % m]
                            for i in range(count))
    return sorted(selected)


def grader_call_site() -> int:
    """호출 봉쇄 지점 — 이 파일에는 채점자 호출 경로가 존재하지 않는다."""
    print("CALLS DISABLED — cross_grader skeleton is fail-closed by design "
          "(BN-09/D121): no grader-model call path exists in this file. "
          "Launch = owner-signed gate Q-F07 (docs/OWNER_QUEUE.md) + owner "
          "steps in docs/CROSS_GRADER_OWNER_PACKET.md.", file=sys.stderr)
    return 2


def main() -> int:
    anchor = load_rubric_anchor()
    print(f"rubric anchor loaded: {RUBRIC_SOURCE} SYSTEM sha256={anchor['sha256']} "
          f"({len(anchor['system_prompt'])} chars), grade schema dims="
          f"{len(anchor['grade_schema']['required'])}")
    records = load_population()
    cells = stratify(records)
    tier_counts: dict = {}
    for r in records:
        tier_counts[r["tier"]] = tier_counts.get(r["tier"], 0) + 1
    print(f"stratification inputs loaded: population={len(records)} "
          f"human_finalized records, tiers={tier_counts}, cells={len(cells)}")
    sample = select_sample(cells)
    print(f"selection rule applied: n={len(sample)} (case list withheld — "
          "freeze-commit of the 20-case list is an owner launch step, "
          f"{SPEC_PATH} §5)")
    return grader_call_site()


if __name__ == "__main__":
    sys.exit(main())
