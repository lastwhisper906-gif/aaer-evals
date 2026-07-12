"""engine_verdict.py — 엔진 판정 기계 계산 (specs/ENGINE_DECISION.md, D51).

스펙 사전 등록 커밋이 본 파일보다 선행한다. 판정은 §4의 순서 고정·전역 완전
규칙 그대로 — 이 스크립트 밖의 어떤 서사도 판정에 개입하지 못한다.

입력: analysis/e2_trajectories.json (스펙 §1 스키마 — E2 완료 후 어댑터가 조립)
출력: analysis/engine_verdict.json (판정 + 중간값 + 케이스별 lead 전수 표)

사용: .venv/bin/python analysis/engine_verdict.py [--in PATH] [--out PATH]
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "analysis"))
from stats import auc  # noqa: E402 (동결 tie-aware AUC 의미론 — 스펙 §3)

DEFAULT_IN = REPO / "analysis" / "e2_trajectories.json"
DEFAULT_OUT = REPO / "analysis" / "engine_verdict.json"
B3_SENSITIVITY = (1, 3)  # 스펙 §2 — 병기 전용, 판정 무가중


class VerdictError(Exception):
    """fail-closed: 스키마 위반·빈 그룹 — 조용한 기본값 금지."""


def case_lead(snapshots: list[dict], score_key: str, threshold: int) -> int:
    """스펙 §3: 임계 돌파 스냅샷 중 최대 quarters_to_revelation, 없으면 0."""
    crossed = [s["quarters_to_revelation"] for s in snapshots
               if s[score_key] is not None and s[score_key] >= threshold]
    return max(crossed, default=0)


def _case_lead_b4(snapshots: list[dict]) -> int:
    """§4b: B4 돌파 = b4_slope_aug > 0 (엄격 초과 — FUNNEL §1 임계 재사용)."""
    crossed = [s["quarters_to_revelation"] for s in snapshots
               if s.get("b4_slope_aug") is not None and s["b4_slope_aug"] > 0]
    return max(crossed, default=0)


def _b4_comparison(treat: list[dict], ctrl: list[dict], thr_llm: int) -> dict:
    """§4b 비교 블록 — 성립 조건·짝지은 부분집합 산식·전량 기록. 전역 완전."""
    covered_t = [c for c in treat
                 if any(s.get("b4_slope_aug") is not None for s in c["snapshots"])]
    coverage = len(covered_t) / len(treat)
    block = {"valid": False, "coverage": f"{len(covered_t)}/{len(treat)}",
             "coverage_ratio": round(coverage, 4), "dominates_llm": None}
    if coverage < 0.7:
        block["reason"] = "실험군 B4 커버리지 < 70% — 비교 불성립 (B4 스펙 §7 (i))"
        return block
    j0_t = [c for c in treat if _snapshot0_opt(c, "b4_slope_aug") is not None]
    j0_c = [c for c in ctrl if _snapshot0_opt(c, "b4_slope_aug") is not None]
    if not j0_t or not j0_c:
        block["reason"] = "j=0 B4 값 부재 (실험군/대조군 중 빈 쪽) — AUC 짝비교 불능"
        return block
    lead_b4 = statistics.median(_case_lead_b4(c["snapshots"]) for c in covered_t)
    lead_llm_paired = statistics.median(
        case_lead(c["snapshots"], "llm_p", thr_llm) for c in covered_t)
    auc_b4 = auc([_snapshot0_opt(c, "b4_slope_aug") for c in j0_t],
                 [_snapshot0_opt(c, "b4_slope_aug") for c in j0_c])
    auc_llm_paired = auc([_snapshot0_opt(c, "llm_p") for c in j0_t],
                         [_snapshot0_opt(c, "llm_p") for c in j0_c])
    dominated = lead_llm_paired <= lead_b4 and auc_llm_paired <= auc_b4
    block.update({
        "valid": True,
        "median_lead_b4": lead_b4, "median_lead_llm_paired": lead_llm_paired,
        "auc_b4_snapshot0_paired": round(auc_b4, 4),
        "auc_llm_snapshot0_paired": round(auc_llm_paired, 4),
        "paired_subset_note": "LLM 값은 B4 커버 부분집합에서 재계산 (§4b 정직 조항 — "
                              "전체군 값과의 차이는 상위 필드 대조)",
        "dominates_llm": dominated})
    return block


def _snapshot0_opt(case: dict, key: str):
    j0 = [s for s in case["snapshots"] if s["j"] == 0]
    return j0[0].get(key) if len(j0) == 1 else None


def _snapshot0(case: dict, score_key: str):
    j0 = [s for s in case["snapshots"] if s["j"] == 0]
    if len(j0) != 1:
        raise VerdictError(f"{case['case_id']}: 스냅샷 j=0이 정확히 1개여야 함 ({len(j0)}개)")
    return j0[0][score_key]


def compute(traj: dict) -> dict:
    thr_llm = traj["flag_threshold_llm"]
    thr_b3 = traj["flag_threshold_b3"]
    if (thr_llm, thr_b3) != (50, 2):
        raise VerdictError(f"임계 ({thr_llm},{thr_b3}) ≠ 사전 등록 (50,2) — 스펙 §2 위반")
    treat = [c for c in traj["cases"] if c["group"] == "treatment"]
    ctrl = [c for c in traj["cases"] if c["group"] == "control"]
    if not treat or not ctrl:
        raise VerdictError("실험군/대조군 중 빈 그룹 — 판정 불능 (fail-closed)")

    leads = [{"case_id": c["case_id"], "ticker": c["ticker"],
              "lead_llm": case_lead(c["snapshots"], "llm_p", thr_llm),
              "lead_b3": case_lead(c["snapshots"], "b3_score", thr_b3),
              **{f"lead_b3_ge{t}": case_lead(c["snapshots"], "b3_score", t)
                 for t in B3_SENSITIVITY}}
             for c in treat]
    med_llm = statistics.median(l["lead_llm"] for l in leads)
    med_b3 = statistics.median(l["lead_b3"] for l in leads)

    # §3 주석 (D71): j=0 값이 null인 케이스는 해당 지표 AUC에서 제외하고,
    # 어느 그룹이든 0이 되면 AUC = null + 플래그 (fail-closed — 프레임 혼합 금지:
    # RP-01 v1 대조군의 동결 점수는 원본 프레임뿐이라 perturbed j=0 llm_p가 없다).
    auc_flags = {}

    def _auc_j0(key: str):
        t = [v for c in treat if (v := _snapshot0(c, key)) is not None]
        k = [v for c in ctrl if (v := _snapshot0(c, key)) is not None]
        if not t or not k:
            auc_flags[key] = (f"j=0 {key} 가용 실험군 {len(t)}·대조군 {len(k)} — "
                              "빈 그룹으로 AUC 계산 불능 (fail-closed null, §3 주석 D71)")
            return None
        if len(t) < len(treat) or len(k) < len(ctrl):
            auc_flags[key] = (f"j=0 {key} 부분 커버 (실험군 {len(t)}/{len(treat)} · "
                              f"대조군 {len(k)}/{len(ctrl)}) — 커버 부분집합 AUC")
        return auc(t, k)

    auc_llm = _auc_j0("llm_p")
    auc_b3 = _auc_j0("b3_score")

    # 스펙 §4 — 순서 고정, 첫 일치가 판정
    if med_llm <= 1 and med_b3 <= 1:
        branch, reading = "c_terminated", ("어느 쪽도 폭로 직전 분기를 넘는 선행 신호 없음 — "
                                           "도구 경로 종료, screener 아카이브, stage-2 없음")
    elif med_llm >= med_b3 + 1:
        branch, reading = "a_llm_engine", "LLM lead ≥ B3+1분기 — stage-2 활성"
    else:
        branch, reading = "b_rules_engine", ("규칙 엔진 — stage-2 제거, LLM은 리포트 초안 "
                                             "보조로 강등")
    sub = None
    if branch == "b_rules_engine":
        if auc_llm is None or auc_b3 is None:
            sub = "b_auc_unavailable"  # §4 하위 라벨은 AUC 요구 — 판정 무영향 필드의 fail-closed
        else:
            sub = "b_strict" if (med_b3 >= med_llm and auc_b3 >= auc_llm) else "b_residual"

    # §4b (D58): B4 결합 — 기본 판정 후 적용, (a)만 강등 가능
    b4_cmp = _b4_comparison(treat, ctrl, thr_llm)
    if b4_cmp["valid"] and b4_cmp["dominates_llm"] and branch == "a_llm_engine":
        branch, sub = "b_rules_engine", "b4_dominated"
        reading = ("규칙 엔진 — §4b: 무료 B4 신호가 리드타임·AUC 모두에서 LLM과 "
                   "대등 이상 (E2 평결과 동일 가중치, B4 스펙 §7 완화 금지 조항 이행)")

    return {"spec": "specs/ENGINE_DECISION.md", "spec_decision": "D51 (+D58 §4b)",
            "thresholds": {"llm_p": thr_llm, "b3_score": thr_b3},
            "median_lead_llm_quarters": med_llm,
            "median_lead_b3_quarters": med_b3,
            "auc_snapshot0": {"llm": round(auc_llm, 4) if auc_llm is not None else None,
                              "b3": round(auc_b3, 4) if auc_b3 is not None else None},
            "auc_snapshot0_flags": auc_flags or None,
            "n_treatment": len(treat), "n_control": len(ctrl),
            "branch": branch, "b_subcase": sub, "reading": reading,
            "b4_comparison": b4_cmp,
            "per_case_leads": sorted(leads, key=lambda l: l["case_id"]),
            "note": "판정은 스펙 §4 기계 규칙 — 본 결과는 Claude 기반 단일 파이프라인에 한정 (§5-5)"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--in", dest="inp", default=str(DEFAULT_IN))
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args()
    verdict = compute(json.loads(Path(args.inp).read_text(encoding="utf-8")))
    Path(args.out).write_text(json.dumps(verdict, ensure_ascii=False, indent=1) + "\n",
                              encoding="utf-8")
    print(f"engine verdict: {verdict['branch']}"
          + (f" ({verdict['b_subcase']})" if verdict["b_subcase"] else "")
          + f" — lead LLM {verdict['median_lead_llm_quarters']}q vs "
            f"B3 {verdict['median_lead_b3_quarters']}q")
    return 0


if __name__ == "__main__":
    sys.exit(main())
