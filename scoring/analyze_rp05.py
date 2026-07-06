"""RP-05 사전 등록 분석 — 결정론 Python (§5-4: 수치 계산은 코드).

실패 기준 (eval_spec §5, freeze 고정):
  (a) 스키마 불통과 또는 인용 날조(차원4=0) ≥ 4/16
  (b) one-sided Mann-Whitney rank-sum p ≥ 0.20 ∨ 중위값 분리 < 10pp ∨ 퇴화 분포(σ<5pp)
  (c) memorization_suspect 제외 집계에서 (a)(b) 발생
D7 CONTAMINATED 분기: 본 분석 = 교란 실행 (실험군) vs 원본 (대조군 — 교란 부재는
D5/D8 freeze 결정의 귀결, 비대칭은 한계로 명기). 원본 실험군 = 부록 상한.

Mann-Whitney: 정확 검정 — C(16,8)=12,870 전수 열거, 동순위 midrank.
"""
from __future__ import annotations

import itertools
import json
import statistics
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

mapping = json.loads((REPO / "scoring/id_mapping.json").read_text(encoding="utf-8"))["mapping"]
cands = {c["case_id"]: c for c in json.loads(
    (REPO / "data/candidates/candidates.json").read_text(encoding="utf-8"))["candidates"]}


def load_dir(d):
    out = {}
    for p in sorted((REPO / d).glob("case_*.json")):
        out[p.stem] = json.loads(p.read_text(encoding="utf-8"))
    return out


runs_main = load_dir("runs/main")
runs_pert = load_dir("runs/perturbed")
grades_main = load_dir("scoring/grades/main")
grades_pert = load_dir("scoring/grades/perturbed")

treat = sorted(n for n, o in mapping.items() if o.startswith("T"))
ctrl = sorted(n for n, o in mapping.items() if o.startswith("C"))
assert len(treat) == 8 and len(ctrl) == 8


def midranks(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = r
        i = j + 1
    return ranks


def mann_whitney_exact(t_vals, c_vals):
    """one-sided (H1: treatment > control) 정확 p — 전수 열거."""
    pooled = list(t_vals) + list(c_vals)
    ranks = midranks(pooled)
    n_t = len(t_vals)
    obs = sum(ranks[:n_t])
    count = total = 0
    for combo in itertools.combinations(range(len(pooled)), n_t):
        total += 1
        if sum(ranks[i] for i in combo) >= obs - 1e-9:
            count += 1
    u = obs - n_t * (n_t + 1) / 2
    auc = u / (n_t * len(c_vals))
    return {"rank_sum": obs, "U": u, "auc": round(auc, 4),
            "p_one_sided_exact": round(count / total, 4)}


def failure_test(label, t_vals, c_vals):
    all16 = list(t_vals) + list(c_vals)
    med_t, med_c = statistics.median(t_vals), statistics.median(c_vals)
    sep = med_t - med_c
    sd = statistics.pstdev(all16)
    mw = mann_whitney_exact(t_vals, c_vals)
    degenerate = sd < 5
    brier = (sum((p / 100 - 1) ** 2 for p in t_vals) +
             sum((p / 100 - 0) ** 2 for p in c_vals)) / 16
    trig = {"p>=0.20": mw["p_one_sided_exact"] >= 0.20,
            "separation<10pp": sep < 10, "degenerate(sd<5pp)": degenerate}
    return {"label": label, "treatment_p": t_vals, "control_p": c_vals,
            "median_t": med_t, "median_c": med_c, "separation_pp": sep,
            "sd_all16": round(sd, 2), **mw, "brier": round(brier, 4),
            "brier_baseline_p50": 0.25,
            "failure_b_triggers": trig, "failure_b": any(trig.values())}


p_orig = {n: runs_main[n]["misstatement_probability"] for n in mapping}
p_pert = {n: runs_pert[n]["misstatement_probability"] for n in treat}

primary = failure_test("PRIMARY (D7 branch: perturbed T vs original C)",
                       [p_pert[n] for n in treat], [p_orig[n] for n in ctrl])
appendix = failure_test("APPENDIX upper bound (original T vs original C)",
                        [p_orig[n] for n in treat], [p_orig[n] for n in ctrl])

# 실패 기준 (a): 스키마 불통과(실행 로그상 0) + dim4=0 건수 — 본 분석 채점 기준
dim4_zero_primary = [n for n in treat if grades_pert[n]["dim4_evidence_quality"] == 0] + \
                    [n for n in ctrl if grades_main[n]["dim4_evidence_quality"] == 0]
dim4_zero_appendix = [n for n in mapping if grades_main[n]["dim4_evidence_quality"] == 0]
mem2 = [n for n in mapping if grades_main[n]["memorization_suspect_condition2"]] + \
       [f"{n}(pert)" for n in treat if grades_pert[n]["memorization_suspect_condition2"]]

# 교란 일관성 (원본−교란 delta, 실험군 8)
k_factors = {}
for p in (REPO / "logs").glob("run_*/runmeta_perturbed_*.json"):
    d = json.loads(p.read_text(encoding="utf-8"))
    if d.get("perturb_factor"):
        k_factors[d["case_id"]] = round(d["perturb_factor"], 3)
deltas = {n: p_orig[n] - p_pert[n] for n in treat}

result = {
    "primary": primary, "appendix": appendix,
    "failure_a_dim4zero_primary": dim4_zero_primary,
    "failure_a_primary": len(dim4_zero_primary) >= 4,
    "failure_a_dim4zero_appendix": dim4_zero_appendix,
    "memorization_suspect_flags": mem2,
    "perturbation": {"k": k_factors, "delta_orig_minus_pert": deltas,
                     "delta_mean": round(statistics.mean(deltas.values()), 1),
                     "delta_median": statistics.median(deltas.values()),
                     "delta_range": [min(deltas.values()), max(deltas.values())]},
    "per_case": {n: {
        "original_id": mapping[n], "ticker": cands[mapping[n]]["ticker"],
        "group": cands[mapping[n]]["group"],
        "p_original": p_orig[n], "p_perturbed": p_pert.get(n),
        "grade_main": {k: grades_main[n][k] for k in
                       ("dim1_probability_band", "dim2_mechanism", "dim4_evidence_quality",
                        "memorization_suspect_condition2")},
        "grade_main_d3": grades_main[n]["dim3_genre_mapping"],
        "grade_pert": ({k: grades_pert[n][k] for k in
                        ("dim1_probability_band", "dim2_mechanism", "dim4_evidence_quality")}
                       | {"d3": grades_pert[n]["dim3_genre_mapping"]}) if n in grades_pert else None,
    } for n in sorted(mapping)},
}

# ---- 분석 ③: 정량 스크린 vs 피평가자 (ROC/AUC, 데이터 허용 범위 — §"as data permits") ----

def screen_values():
    tvals, cvals = {}, {}
    for n in treat:
        oid = mapping[n]
        d = json.loads((REPO / f"scoring/baselines/results/{oid}.json").read_text(encoding="utf-8"))
        tvals[n] = {"M": d["beneish"]["m_score"], "F": d["dechow_f"]["f_score"],
                    "C": d["montier_c"]["c_score"], "Sloan": d["sloan_accruals"]["value"],
                    "Piotroski": None}
    import re as _re

    def first_word(s):
        toks = [t for t in _re.sub(r"[^a-z0-9 ]", " ", s.lower()).split() if t != "the"]
        return toks[0] if toks else ""

    by_cand = {}
    for p in (REPO / "scoring/baselines/results/controls").glob("*.json"):
        d = json.loads(p.read_text(encoding="utf-8"))
        by_cand[first_word(d["candidate"])] = d
    for n in ctrl:
        d = by_cand.get(first_word(cands[mapping[n]]["company_name"]))
        cvals[n] = ({"M": d["beneish_m"], "F": d["dechow_f"], "C": d["montier_c"],
                     "Sloan": d["sloan"], "Piotroski": d["piotroski_f9"]} if d else
                    {"M": None, "F": None, "C": None, "Sloan": None, "Piotroski": None})
    return tvals, cvals


def auc_defined(tv, cv, transform=lambda x: x):
    t = [transform(v) for v in tv if v is not None]
    c = [transform(v) for v in cv if v is not None]
    if not t or not c:
        return None, 0, 0
    wins = sum((1.0 if a > b else 0.5 if a == b else 0.0) for a in t for b in c)
    return round(wins / (len(t) * len(c)), 3), len(t), len(c)


tv, cv = screen_values()
baselines = {}
for key, tf in (("M", lambda x: x), ("F", lambda x: x), ("C", lambda x: x),
                ("Sloan_abs", lambda x: abs(x))):
    k0 = key.split("_")[0]
    auc, nt, nc = auc_defined([tv[n][k0] for n in treat], [cv[n][k0] for n in ctrl], tf)
    baselines[key] = {"auc": auc, "n_treat": nt, "n_ctrl": nc}
baselines["Piotroski"] = {"auc": None, "note": "실험군 미계산 — 대조군 전용 값만 존재 (AUC 불능)"}
baselines["evaluatee_primary"] = {"auc": primary["auc"], "n_treat": 8, "n_ctrl": 8}
baselines["evaluatee_appendix"] = {"auc": appendix["auc"], "n_treat": 8, "n_ctrl": 8}
result["baselines_auc"] = baselines
result["screen_values"] = {"treatment": {mapping[n]: tv[n] for n in treat},
                           "control": {mapping[n]: cv[n] for n in ctrl}}

out = REPO / "scoring/rp05_stats.json"
out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
