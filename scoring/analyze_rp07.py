"""RP-09 Stage 1 (= RP-07 D-2 종결): 원본 재추첨 k=5 — delta 분해 완결.

프레이밍: RP-05 §1 사전 등록 판정 불변 — 본 분석은 L-3(표본 잡음) 정량화의
완결이다 (RP-06 §D-2 정의 승계, analyze_hardening.py와 동일 불변 프레이밍).

입력: runs/main (원본 draw1) + runs/rp07/draws/draw_{2..5} (원본 draws 2-5, 실험군 8)
      + scoring/rp06_hardening_stats.json (교란 k=5 — 동결 산출물, 읽기 전용)
출력: scoring/rp07_stats.json (결정론 — 재실행 = 동일 결과)

분해 모델 (케이스별):
  delta(draw d) = p_orig(d) − p_pert(d)
  inside-noise  = 같은 페이로드 재호출 표본 산포 (sd_orig, sd_pert — pstdev, k=5)
  outside(교란 효과) = mean_orig − mean_pert; 유의 판정 = |Δmean| > 2·SE,
      SE = sqrt(sd_orig²/k + sd_pert²/k)  (독립 표본 근사)
  draw1 delta의 잡음 설명 가능성 = |delta_draw1| ≤ 2·sqrt(sd_orig² + sd_pert²)
"""
import json
import math
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scoring"))
from analyze_hardening import stats_block  # noqa: E402 (동결 통계 함수 재사용 — 수치 비교 가능성)
TREAT = ["case_01", "case_02", "case_03", "case_06",
         "case_08", "case_09", "case_12", "case_13"]
CTRL = ["case_04", "case_05", "case_07", "case_10",
        "case_11", "case_14", "case_15", "case_16"]


def load_p(rel: str) -> dict:
    out = {}
    for p in sorted((REPO / rel).glob("case_*.json")):
        j = json.loads(p.read_text(encoding="utf-8"))
        out[j["case_id"]] = j["misstatement_probability"]
    return out


def main() -> int:
    rp06 = json.loads((REPO / "scoring/rp06_hardening_stats.json").read_text())
    a3 = rp06["a3_sampling"]

    # 원본 실험군 draws: draw1 = runs/main, draws 2-5 = runs/rp07
    p_main = load_p("runs/main")
    orig_draws = {1: {n: p_main[n] for n in TREAT}}
    for d in (2, 3, 4, 5):
        dp = load_p(f"runs/rp07/draws/draw_{d}")
        missing = [n for n in TREAT if n not in dp]
        if missing:
            raise SystemExit(f"draw_{d} 불완전: {missing}")
        orig_draws[d] = dp
    k = len(orig_draws)

    # 대조군 draws (원본 — RP-06 A3에서 기수집): draw1 = runs/main, 2-5 = hardening
    ctrl_draws = {1: {n: p_main[n] for n in CTRL}}
    for i, dname in enumerate(sorted(
            d.name for d in (REPO / "runs/hardening/draws").iterdir() if d.is_dir()), start=2):
        dp = load_p(f"runs/hardening/draws/{dname}")
        ctrl_draws[i] = {n: dp[n] for n in CTRL}

    per_case, decomposition = {}, []
    for n in TREAT:
        ovals = [orig_draws[d][n] for d in sorted(orig_draws)]
        pc6 = a3["per_case"][n]
        pvals = pc6["draws"]
        sd_o = statistics.pstdev(ovals)
        sd_p = pc6["sd"]
        mean_o, mean_p = statistics.mean(ovals), statistics.mean(pvals)
        delta1 = ovals[0] - pvals[0]
        noise_sd_delta = math.sqrt(sd_o ** 2 + sd_p ** 2)
        se_dmean = math.sqrt(sd_o ** 2 / k + sd_p ** 2 / len(pvals))
        per_case[n] = {"ticker": pc6["ticker"], "company": pc6["company"],
                       "orig_draws": ovals, "orig_mean": round(mean_o, 1),
                       "orig_sd": round(sd_o, 2), "orig_range_pp": max(ovals) - min(ovals),
                       "pert_draws": pvals, "pert_mean": round(mean_p, 1),
                       "pert_sd": sd_p}
        decomposition.append({
            "case_id": n, "ticker": pc6["ticker"],
            "delta_draw1": delta1,
            "delta_mean_orig_minus_pert": round(mean_o - mean_p, 1),
            "inside_noise_sd_orig": round(sd_o, 2),
            "inside_noise_sd_pert": sd_p,
            "noise_sd_delta_single_draw": round(noise_sd_delta, 2),
            "delta_draw1_within_2sd_noise": abs(delta1) <= 2 * noise_sd_delta,
            "se_delta_mean": round(se_dmean, 2),
            "outside_signal_delta_mean_beyond_2se": abs(mean_o - mean_p) > 2 * se_dmean,
        })

    # 원본-원본 k=5 패밀리 (실험군 원본 draws vs 대조군 원본 draws — 같은 draw 번호 쌍)
    orig_family = []
    for d in sorted(orig_draws):
        blk = stats_block([orig_draws[d][n] for n in TREAT],
                          [ctrl_draws[d][n] for n in CTRL])
        blk["draw"] = d
        blk["separation<10pp"] = blk["separation_pp"] < 10
        orig_family.append(blk)

    seps_pert_family = [b["separation_pp"] for b in a3["per_draw_stats"]]
    seps_orig_family = [b["separation_pp"] for b in orig_family]

    out = {
        "framing": "post-hoc robustness completion (RP-07 D-2) — RP-05 §1 "
                   "pre-registered verdict stands unchanged regardless of outcome",
        "k": k,
        "per_case": per_case,
        "delta_decomposition_completed": decomposition,
        "n_outside_signal": sum(1 for d in decomposition
                                if d["outside_signal_delta_mean_beyond_2se"]),
        "n_delta_draw1_explained_by_noise": sum(
            1 for d in decomposition if d["delta_draw1_within_2sd_noise"]),
        "original_vs_control_per_draw": orig_family,
        "separation_families": {
            "perturbed_treat_vs_original_ctrl_k5": seps_pert_family,
            "original_treat_vs_original_ctrl_k5": seps_orig_family,
            "note": "전자 = RP-06 A3 (draw3=9.0pp 사건의 프레임), 후자 = 본 완결",
        },
        "draw3_event": {
            "observed": 9.0,
            "pert_family_mean": round(statistics.mean(seps_pert_family), 1),
            "pert_family_sd": round(statistics.stdev(seps_pert_family), 2),
            "z_of_draw3": round((9.0 - statistics.mean(seps_pert_family))
                                / statistics.stdev(seps_pert_family), 2),
            "orig_family_min": min(seps_orig_family),
            "any_orig_family_below_10": any(s < 10 for s in seps_orig_family),
        },
    }
    dest = REPO / "scoring/rp07_stats.json"
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out["draw3_event"], indent=2))
    print("decomposition:", json.dumps(decomposition, indent=1)[:2000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
