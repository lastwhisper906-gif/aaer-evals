"""decision_table — 임계·결정 표 계산 (DECISION_TABLE_PLAN.md 사전 등록 그대로).

동결 산출물 재집계 전용: 신규 API 호출 0, runs/ 읽기 전용, 신규 통계 코드 0
(CP는 동결 holdout_controls_analyze.clopper_pearson 재사용). 출력은
analysis/decision_table.json 하나.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "analysis"))
from holdout_controls_analyze import clopper_pearson  # noqa: E402 (동결 CP 재사용)

PLAN = "analysis/DECISION_TABLE_PLAN.md"
THRESHOLDS = [40, 50, 60, 70]
# BUYER_METRICS.md §3 실측 인용 — 재측정·재계산 금지 (사전 등록 §4)
COST_PER_SCREEN_USD = 0.5304

# scoring/id_mapping.json T*/C* 접두 그대로 (사전 등록 §2)
W1_TREATMENT = ["case_01", "case_02", "case_03", "case_06",
                "case_08", "case_09", "case_12", "case_13"]
W1_CONTROL = ["case_04", "case_05", "case_07", "case_10",
              "case_11", "case_14", "case_15", "case_16"]
HOLDOUT = ["case_71", "case_72", "case_73"]
E1_CONTROLS = [f"hc_{i:02d}" for i in range(1, 10)]


def load_score(path: Path) -> int:
    with open(path) as f:
        return json.load(f)["misstatement_probability"]


def cell(t_scores: list[int], c_scores: list[int], threshold: int,
         n_screens: int) -> dict:
    """단일 스냅샷 레이어 셀: 탐지·오탐 + CP95 + 탐지당 비용 (사전 등록 §3–4)."""
    x = sum(1 for s in t_scores if s >= threshold)
    y = sum(1 for s in c_scores if s >= threshold)
    det_lo, det_hi = clopper_pearson(x, len(t_scores))
    fpr_lo, fpr_hi = clopper_pearson(y, len(c_scores))
    cost = round(n_screens * COST_PER_SCREEN_USD / x, 2) if x else None
    return {"threshold": threshold,
            "detected": x, "n_treatment": len(t_scores),
            "detected_ci95": [round(det_lo, 4), round(det_hi, 4)],
            "false_positives": y, "n_control": len(c_scores),
            "fpr_ci95": [round(fpr_lo, 4), round(fpr_hi, 4)],
            "cost_per_detection_usd": cost}


def trajectory_flags(cases: list[dict], threshold: int,
                     require_b3_gate: bool = False) -> tuple[list[str], int]:
    """궤적 플래그: 어느 스냅샷이든 llm_p≥T (null 스냅샷 fail-closed 제외).

    require_b3_gate=True면 동일 스냅샷 b3_score≥2 AND llm_p≥T (EXPLORATORY §5).
    반환: (플래그된 case_id 목록, 제외된 null 스냅샷 수).
    """
    flagged, nulls = [], 0
    for c in cases:
        hit = False
        for s in c["snapshots"]:
            if s["llm_p"] is None:
                nulls += 1
                continue
            if s["llm_p"] >= threshold and (not require_b3_gate or s["b3_score"] >= 2):
                hit = True
        if hit:
            flagged.append(c["case_id"])
    return flagged, nulls


def trajectory_cell(cases: list[dict], threshold: int, n_screens: int,
                    require_b3_gate: bool = False) -> dict:
    t_cases = [c for c in cases if c["group"] == "treatment"]
    c_cases = [c for c in cases if c["group"] == "control"]
    t_flagged, _ = trajectory_flags(t_cases, threshold, require_b3_gate)
    c_flagged, _ = trajectory_flags(c_cases, threshold, require_b3_gate)
    x, y = len(t_flagged), len(c_flagged)
    det_lo, det_hi = clopper_pearson(x, len(t_cases))
    fpr_lo, fpr_hi = clopper_pearson(y, len(c_cases))
    cost = round(n_screens * COST_PER_SCREEN_USD / x, 2) if x else None
    return {"threshold": threshold,
            "detected": x, "n_treatment": len(t_cases),
            "detected_ci95": [round(det_lo, 4), round(det_hi, 4)],
            "false_positives": y, "n_control": len(c_cases),
            "fpr_ci95": [round(fpr_lo, 4), round(fpr_hi, 4)],
            "cost_per_detection_usd": cost,
            "flagged_treatment": t_flagged, "flagged_control": c_flagged}


def count_scored_snapshots(cases: list[dict]) -> tuple[int, int]:
    """(llm_p 비-null 스냅샷 수, null 제외 수) — 비용 분모·정직 기록용."""
    scored = sum(1 for c in cases for s in c["snapshots"] if s["llm_p"] is not None)
    nulls = sum(1 for c in cases for s in c["snapshots"] if s["llm_p"] is None)
    return scored, nulls


def build(repo: Path = REPO) -> dict:
    w2_fraud = set(json.load(open(repo / "runs/wave2/fraud_case_ids.json")))
    w2_all = sorted(p.stem for p in (repo / "runs/wave2/scores").glob("case_*.json"))

    layers = {
        "L1_wave1_perturbed": {
            "t_scores": [load_score(repo / f"runs/perturbed/{c}.json") for c in W1_TREATMENT],
            "c_scores": [load_score(repo / f"runs/main/{c}.json") for c in W1_CONTROL],
            "note": ("프레임 비대칭: 실험군=perturbed, 대조군=original "
                     "(대조군 perturbed 미채점 — 사전 등록 §2①, 신규 채점 금지)"),
        },
        "L2_wave2": {
            "t_scores": [load_score(repo / f"runs/wave2/scores/{c}.json")
                         for c in w2_all if c in w2_fraud],
            "c_scores": [load_score(repo / f"runs/wave2/scores/{c}.json")
                         for c in w2_all if c not in w2_fraud],
            "note": None,
        },
        "L3_holdout_e1": {
            "t_scores": [load_score(repo / f"runs/holdout/scores/{c}.json") for c in HOLDOUT],
            "c_scores": [load_score(repo / f"runs/holdout/controls/scores/{c}.json")
                         for c in E1_CONTROLS],
            "note": ("라벨 G2 provisional (restatement/non-reliance, NOT fraud) — "
                     "'탐지'가 아니라 잠정 라벨 이벤트 플래깅 (사전 등록 §2②)"),
        },
    }

    result: dict = {
        "plan": PLAN,
        "generated_by": "analysis/decision_table.py",
        "cost_per_screen_usd": COST_PER_SCREEN_USD,
        "cost_source": "analysis/BUYER_METRICS.md §3 (실측 인용 — 재계산 없음)",
        "thresholds": THRESHOLDS,
        "layers": {},
    }

    for name, layer in layers.items():
        n_screens = len(layer["t_scores"]) + len(layer["c_scores"])
        result["layers"][name] = {
            "n_treatment": len(layer["t_scores"]),
            "n_control": len(layer["c_scores"]),
            "n_screens": n_screens,
            "note": layer["note"],
            "cells": [cell(layer["t_scores"], layer["c_scores"], t, n_screens)
                      for t in THRESHOLDS],
        }

    traj = json.load(open(repo / "analysis/e2_trajectories.json"))
    cases = traj["cases"]
    n_screens, n_nulls = count_scored_snapshots(cases)
    result["layers"]["L4_e2_trajectory"] = {
        "n_treatment": sum(1 for c in cases if c["group"] == "treatment"),
        "n_control": sum(1 for c in cases if c["group"] == "control"),
        "n_screens": n_screens,
        "excluded_null_snapshots": n_nulls,
        "note": ("플래그 = 어느 스냅샷이든 llm_p≥T; null 스냅샷 fail-closed 제외 "
                 "(대조군 j=0 null — D71 규약)"),
        "cells": [trajectory_cell(cases, t, n_screens) for t in THRESHOLDS],
    }

    result["exploratory_combo"] = {
        "label": "EXPLORATORY",
        "rule": "동일 스냅샷에서 b3_score>=2 AND llm_p>=T (L4 궤적 전용)",
        "status": ("사후(post-hoc) 규칙 — 소급 성능 주장 금지. "
                   "Cycle-2 사전 등록 후보 전용 (사전 등록 §5)"),
        "cells": [trajectory_cell(cases, t, n_screens, require_b3_gate=True)
                  for t in THRESHOLDS],
    }
    return result


def main() -> None:
    out = REPO / "analysis/decision_table.json"
    result = build()
    with open(out, "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
