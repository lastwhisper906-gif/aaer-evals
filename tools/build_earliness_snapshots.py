"""build_earliness_snapshots.py — E2 조기성 스냅샷 케이스 생성기 (사전등록 EARLINESS_PLAN).

이 도구는 **채점을 발사하지 않는다** — 스냅샷 케이스 파일 + 스냅샷 레지스트리 + 감사용
그리드 덤프만 만든다. 실제 채점은 pipeline/runner.py로 별도 실행하며 owner 게이트
(overrides.md 토큰)를 통과해야 한다(권한 최종). 미터링 0.

파이프라인 (모두 결정론·오프라인, 네트워크 0):
  1. select_eligible()  — 적격 케이스 선정. 커밋 산출물만 읽음(캐시 불요):
       · fraud = fraud 케이스 중 본채점 p>=50(detected). MON(case_06) 명시 제외.
       · control = RP-01 wave-1 대조군 8 (동일 그리드 baseline, EARLINESS_PLAN §4).
  2. build_case_grid()  — 케이스별 스냅샷 그리드. bp.load_filing_chronology(filed<=폭로
       컷오프)로 정기 제출 filed일을 얻어 earliness_grid.compute_snapshot_grid에 투입.
       (~/aaer-data 캐시 필요 — 부재 시 이 단계는 건너뛰고 명시 보고.)
  3. guard_snapshot()   — 스냅샷별 cutoff_guard.load_document(스냅샷 레지스트리 경유)로
       그 시점 최신 제출의 filed일을 EDGAR filingDate와 대조 → "allowed" 기록 + 폭로/
       인접 위반 fail-closed. candidates.json(정답지) 불변 — 스냅샷 전용 레지스트리 사용.

모드:
  --plan   : 적격 세트 + (캐시 있으면) 그리드를 출력만. 파일 미기록. (기본)
  --emit   : 스냅샷 케이스 파일 + 레지스트리 기록 (캐시 필수 — 부재 시 거부).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "pipeline"))

import build_payload as bp          # noqa: E402  (load_filing_chronology 재사용)
import cutoff_guard                 # noqa: E402
import earliness_grid as eg         # noqa: E402

WAVE1_CASES = REPO / "data" / "evaluatee" / "cases.json"
WAVE2_CASES = REPO / "data" / "evaluatee" / "cases_wave2.json"
ID_MAPPING = REPO / "scoring" / "id_mapping.json"          # 채점측 — T#/C# (fraud/control)
WAVE2_FRAUD = REPO / "runs" / "wave2" / "fraud_case_ids.json"
MAIN_RUN = REPO / "runs" / "main"
WAVE2_SCORES = REPO / "runs" / "wave2" / "scores"
OUT_DIR = REPO / "runs" / "earliness"                      # NEW 경로 — runs/main 불침해
MON_EXCLUDED = "case_06"                                   # EARLINESS_DESIGN §2: 1점 궤적
DETECT_THRESHOLD = 50
MIN_RESIDUAL_FILINGS = 6                                   # §1 스냅샷 최소 요건 (본실행 바닥)


def _load_cases(path: Path) -> dict[str, dict]:
    return {c["case_id"]: c for c in json.loads(path.read_text(encoding="utf-8"))["cases"]}


def _score_p(scores_dir: Path, case_id: str) -> int | None:
    f = scores_dir / f"{case_id}.json"
    if not f.is_file():
        return None
    return json.loads(f.read_text(encoding="utf-8"))["misstatement_probability"]


def select_eligible() -> list[dict]:
    """적격 케이스(캐시 불요, 커밋 산출물만). fraud=detected p>=50 (MON 제외) + control=RP-01 8."""
    w1 = _load_cases(WAVE1_CASES)
    w2 = _load_cases(WAVE2_CASES)
    mapping = json.loads(ID_MAPPING.read_text(encoding="utf-8"))["mapping"]
    w1_fraud = {cid for cid, nid in mapping.items() if nid.startswith("T")}
    w1_control = {cid for cid, nid in mapping.items() if nid.startswith("C")}
    w2_fraud = set(json.loads(WAVE2_FRAUD.read_text(encoding="utf-8")))

    out: list[dict] = []
    # wave-1 fraud detected (MON 제외)
    for cid in sorted(w1_fraud):
        if cid == MON_EXCLUDED:
            continue
        p = _score_p(MAIN_RUN, cid)
        if p is None or p < DETECT_THRESHOLD:
            continue
        out.append({**_meta(w1[cid]), "group": "fraud", "wave": 1, "main_p": p})
    # wave-2 fraud detected
    for cid in sorted(w2_fraud):
        p = _score_p(WAVE2_SCORES, cid)
        if p is None or p < DETECT_THRESHOLD:
            continue
        out.append({**_meta(w2[cid]), "group": "fraud", "wave": 2, "main_p": p})
    # RP-01 wave-1 대조군 8 (baseline — detected 요건 없음)
    for cid in sorted(w1_control):
        out.append({**_meta(w1[cid]), "group": "control", "wave": 1, "main_p": _score_p(MAIN_RUN, cid)})
    return out


def _meta(case: dict) -> dict:
    return {"case_id": case["case_id"], "ticker": case["ticker"], "cik": case.get("cik"),
            "company_name": case["company_name"], "revelation_cutoff": case["cutoff_date"]}


def _residual_at(chrono: list[dict], cutoff) -> tuple[int, int]:
    """스냅샷 컷오프 시점의 잔존 제출 수 · 10-K 수 (§1 최소 요건 판정용)."""
    import datetime as dt
    res = [r for r in chrono if dt.date.fromisoformat(r["filing_date"]) <= cutoff]
    tenk = sum(1 for r in res if r["form"].upper().startswith("10-K"))
    return len(res), tenk


def filter_min_data(grid: eg.Grid, chrono: list[dict], *, min_filings: int) -> eg.Grid:
    """§1 스냅샷 최소 요건 — 잔존 제출 ≥min_filings 및 10-K ≥1 아니면 drop(insufficient_data).
    MON 본실행 수준 바닥. 깊은(이른) 스냅샷일수록 잔존이 적어 자연히 이 필터에 걸린다."""
    kept, dropped = [], list(grid.dropped)
    for s in grid.snapshots:
        n, tenk = _residual_at(chrono, s.cutoff)
        if n < min_filings or tenk < 1:
            dropped.append(eg.DroppedSnapshot(s.j, s.boundary_filed, "insufficient_data"))
        else:
            kept.append(s)
    return eg.Grid(snapshots=kept, dropped=dropped, max_depth=grid.max_depth)


def build_case_grid(elig: dict, *, max_snapshots: int, day_offset: int,
                    min_filings: int = MIN_RESIDUAL_FILINGS) -> eg.Grid:
    """케이스의 스냅샷 그리드 (캐시 필요). load_filing_chronology = filed<=폭로컷오프.
    §1 최소 요건(잔존 ≥6, 10-K ≥1) 미달 스냅샷은 insufficient_data로 drop."""
    import datetime as dt
    rev = dt.date.fromisoformat(elig["revelation_cutoff"])
    chrono = bp.load_filing_chronology(elig["ticker"], rev)  # [{form, filing_date}]
    periodic = [dt.date.fromisoformat(r["filing_date"]) for r in chrono
                if eg.is_periodic_filing(r["form"])]
    allf = [dt.date.fromisoformat(r["filing_date"]) for r in chrono]
    grid = eg.compute_snapshot_grid(periodic, allf, rev,
                                    max_snapshots=max_snapshots, day_offset=day_offset)
    return filter_min_data(grid, chrono, min_filings=min_filings)


def snapshot_case(elig: dict, snap: eg.Snapshot) -> dict:
    """스냅샷 1건의 러너 입력 케이스. base_id로 스냅샷 간 동일 교란 k·정체 보장."""
    return {"case_id": f"{elig['case_id']}_s{snap.j}", "base_id": elig["case_id"],
            "ticker": elig["ticker"], "cik": elig["cik"],
            "company_name": elig["company_name"], "cutoff_date": snap.cutoff.isoformat()}


def revelation_registry(elig: list[dict]) -> list[dict]:
    """base case_id → 폭로 컷오프 레지스트리 (스냅샷 가드 전용, candidates.json 불침해)."""
    seen: dict[str, str] = {}
    for e in elig:
        seen[e["case_id"]] = e["revelation_cutoff"]
    return [{"case_id": cid, "cutoff_date": co} for cid, co in seen.items()]


def guard_snapshot(rev_reg_path: Path, base_case_id: str, snap_case: dict, log_path: Path) -> str:
    """스냅샷 컷오프가 그 케이스의 폭로 컷오프를 넘지 않는지 cutoff_guard로 독립 검증.

    이것이 non-vacuous한 look-ahead 경계 검사다: load_pit_series/그리드는 이미 filed<=
    스냅샷컷오프로 자기정합적이므로, 정작 막아야 할 위반은 '스냅샷 컷오프 자체가 폭로
    경계를 넘는 것'(§5-1). 감사 게이트웨이(cutoff_guard)로 그 날짜만 대조 → access log에
    allowed 기록 + 위반 시 CutoffViolationError fail-closed. 순수 날짜 검사라 캐시 불요."""
    cutoff_guard.load_document(
        base_case_id, f"earliness_snapshot:{snap_case['case_id']}",
        snap_case["cutoff_date"], registry_path=str(rev_reg_path),
        log_path=str(log_path), loader=lambda _p: "verified")
    return "allowed"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit", action="store_true", help="스냅샷 케이스+레지스트리 기록 (캐시 필수)")
    ap.add_argument("--max-snapshots", type=int, default=eg.DEFAULT_MAX_SNAPSHOTS)
    ap.add_argument("--day-offset", type=int, default=eg.DEFAULT_DAY_OFFSET)
    args = ap.parse_args()

    elig = select_eligible()
    n_fraud = sum(1 for e in elig if e["group"] == "fraud")
    n_ctrl = sum(1 for e in elig if e["group"] == "control")
    print(f"적격: fraud(detected) {n_fraud} + control {n_ctrl} = {len(elig)} 케이스")
    for e in elig:
        print(f"  [{e['group'][:1].upper()}] {e['case_id']:9s} {e['ticker']:6s} "
              f"rev={e['revelation_cutoff']} main_p={e['main_p']}")

    cache = bp.DATA_DIR.exists()
    if not cache:
        print(f"\n~/aaer-data 캐시 부재 → 그리드/emit 단계 보류 (감독 세션에서 실행).")
        print("선정 로직은 위와 같이 커밋 산출물만으로 검증됨. 미터링 0.")
        return 0

    total = 0
    all_snap_cases: list[dict] = []
    for e in elig:
        grid = build_case_grid(e, max_snapshots=args.max_snapshots, day_offset=args.day_offset)
        snaps = grid.snapshots
        cases = [snapshot_case(e, s) for s in snaps]
        all_snap_cases += cases
        total += len(snaps)
        drops = ",".join(f"{d.j}:{d.reason}" for d in grid.dropped) or "-"
        note = "" if grid.max_depth >= MIN_RESIDUAL_FILINGS else " ⚑빈약(<6)"
        print(f"  {e['case_id']} depth={grid.max_depth} snaps={len(snaps)} drop=[{drops}]{note}")
    print(f"\n총 스냅샷(=미터링 예상, 스냅샷0 재사용 제외): {total}")

    if args.emit:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        rev_reg_path = OUT_DIR / "revelation_registry.json"
        rev_reg_path.write_text(
            json.dumps({"candidates": revelation_registry(elig)}, ensure_ascii=False, indent=2),
            encoding="utf-8")
        (OUT_DIR / "cases_earliness.json").write_text(
            json.dumps({"cases": all_snap_cases}, ensure_ascii=False, indent=2), encoding="utf-8")
        log_path = OUT_DIR / "access_log.jsonl"
        base_of = {sc["case_id"]: sc["base_id"] for sc in all_snap_cases}
        verdicts = {guard_snapshot(rev_reg_path, base_of[c["case_id"]], c, log_path)
                    for c in all_snap_cases}
        print(f"emit 완료: {len(all_snap_cases)} 스냅샷 케이스 · guard verdicts={verdicts}")
        print("채점은 owner 게이트 후 runner.py로 별도 발사(권한 최종).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
