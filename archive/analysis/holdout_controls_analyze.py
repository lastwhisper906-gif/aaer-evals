"""E1 홀드아웃 매칭 대조군 분석 (결정론) — HOLDOUT_CONTROLS_PLAN §4 사전 고정 그대로.

`python analysis/holdout_controls_analyze.py`
입력: runs/holdout/scores/case_NN.json (프라우드 3사, 동결)
      runs/holdout/controls/scores/hc_NN.json (E1 대조군)
      scoring/id_mapping_holdout_controls.json ({"mapping": {hc_NN: TICKER},
        "case_of": {hc_NN: case_71|72|73}} — 케이스 매칭 유지)
사전 고정 (§4 — 재해석 금지):
  1차 = per-case 병기 (프라우드 점수 vs 매칭 대조군 점수들). H2 강화용 병기, 유의성 아님.
  정확 소표본 검정 = CONTEXT ONLY (N=3 과소검정 — H1 미주장 사전 명시).
  FPR: fp=0 → rule-of-three 상한 3/n; fp>0 → 정확 Clopper-Pearson 95% (순수 파이썬).
  0% 헤드라인 금지. HUBG 우위여도 P1 단서(dim2=1 기제 빗나감) 유지.
출력: analysis/holdout_controls_results.json.
"""
import itertools
import json
import math
import statistics as st
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HOLDOUT = {"case_71": "HUBG", "case_72": "WMK", "case_73": "GNE"}


def load_p(path):
    p = REPO / path
    return json.load(open(p, encoding="utf-8"))["misstatement_probability"] if p.exists() else None


def binom_cdf(k, n, p):
    return sum(math.comb(n, i) * p**i * (1 - p) ** (n - i) for i in range(k + 1))


def clopper_pearson(fp, n, alpha=0.05):
    """정확 CP 95% 구간 (이분법, scipy 불요 — 결정론)."""
    if fp == 0:
        lo = 0.0
    else:
        f = lambda p: 1 - binom_cdf(fp - 1, n, p) - alpha / 2
        lo = _bisect(f, 0.0, 1.0)
    if fp == n:
        hi = 1.0
    else:
        g = lambda p: binom_cdf(fp, n, p) - alpha / 2
        hi = _bisect(g, 0.0, 1.0)
    return lo, hi


def _bisect(f, a, b, tol=1e-9):
    fa = f(a)
    for _ in range(200):
        m = (a + b) / 2
        fm = f(m)
        if abs(fm) < tol:
            return m
        if (fa < 0) == (fm < 0):
            a, fa = m, fm
        else:
            b = m
    return (a + b) / 2


def exact_perm_p(treat, ctrl):
    """정확 순열 p (mean-diff, one-sided treat>ctrl) — CONTEXT ONLY (§4)."""
    pool, nt = treat + ctrl, len(treat)
    obs = st.mean(treat) - st.mean(ctrl)
    total = ge = 0
    for comb in itertools.combinations(range(len(pool)), nt):
        t = [pool[i] for i in comb]
        c = [pool[i] for i in range(len(pool)) if i not in comb]
        total += 1
        if st.mean(t) - st.mean(c) >= obs - 1e-12:
            ge += 1
    return ge / total


def main():
    mapping = json.load(open(REPO / "scoring/id_mapping_holdout_controls.json",
                             encoding="utf-8"))
    ctrl_ticker = mapping["mapping"]          # hc_NN -> ticker
    case_of = mapping["case_of"]              # hc_NN -> case_71|72|73

    fraud_p = {t: load_p(f"runs/holdout/scores/{c}.json") for c, t in HOLDOUT.items()}
    ctrl_p = {hc: load_p(f"runs/holdout/controls/scores/{hc}.json") for hc in ctrl_ticker}
    missing = [hc for hc, v in ctrl_p.items() if v is None]

    per_case = {}
    for c, t in HOLDOUT.items():
        matched = {ctrl_ticker[hc]: ctrl_p[hc] for hc in ctrl_ticker
                   if case_of[hc] == c and ctrl_p[hc] is not None}
        per_case[t] = {
            "holdout_score": fraud_p[t],
            "matched_controls": matched,
            "holdout_above_all_matched": (bool(matched) and fraud_p[t] is not None
                                          and fraud_p[t] > max(matched.values())),
        }

    scored = [v for v in ctrl_p.values() if v is not None]
    n, fp = len(scored), sum(1 for v in scored if v >= 50)
    if n and fp == 0:
        fpr = {"fp": 0, "n": n, "language": "rule-of-three",
               "upper_bound": round(3 / n, 3),
               "statement": f"오탐 0/{n} — 상한 3/{n}={3/n:.1%} (0% 헤드라인 금지)"}
    elif n:
        lo, hi = clopper_pearson(fp, n)
        fpr = {"fp": fp, "n": n, "language": "Clopper-Pearson 95%",
               "point": round(fp / n, 3), "ci": [round(lo, 3), round(hi, 3)]}
    else:
        fpr = {"fp": None, "n": 0, "statement": "대조군 점수 없음 (E1 미실행)"}

    treat_vals = [v for v in fraud_p.values() if v is not None]
    context_p = (round(exact_perm_p(treat_vals, scored), 4)
                 if len(treat_vals) == 3 and scored else None)

    out = {
        "plan": "HOLDOUT_CONTROLS_PLAN.md §4 (사전 고정)",
        "per_case_side_by_side": per_case,
        "control_fpr": fpr,
        "exact_perm_p_CONTEXT_ONLY": {
            "value": context_p,
            "note": "N=3 과소검정 — H1 미주장 (참고 수치, 결론 근거 아님)"},
        "missing_scores": missing,
        "caveats": "HUBG 대조 우위여도 P1 단서 유지 (dim2=1 기제 빗나감 — forensic "
                   "정확성 입증 아님). G2 provisional — restatement/non-reliance 서술만.",
    }
    (REPO / "analysis/holdout_controls_results.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
