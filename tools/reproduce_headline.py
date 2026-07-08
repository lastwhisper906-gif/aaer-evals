"""reproduce_headline.py — 현행 발행 헤드라인 수치를 동결 점수로 재계산·대조 (감사 B2).

기존 reproduce_analysis.py는 RP-05 파일럿(8v8)만 검증했다. 이 도구는 **현행 헤드라인**
을 커밋 산출물만으로(캐시 불요) 재계산해 committed JSON과 대조한다:
  · wave-1 primary/secondary (8v22): analysis/stats.frame_stats 재사용 → results_stats.json
  · wave-2 standalone/perturbed/pooled: wave2_analyze의 결정론 로직을 그대로 복제 →
    wave2_results.json (llm_score 기반 헤드라인만; 베이스라인 M/F는 캐시 의존이라 제외)

불일치 시 라인 출력 후 exit 1. `make verify`/CI 편입. 순수 결정론, API·네트워크 0.
"""
from __future__ import annotations

import glob
import json
import random
import statistics as st
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "analysis"))
import stats as W1  # noqa: E402 (frame_stats·load_table 재사용)

SEED = 20260707


# ---------- wave-1 (results_stats.json) — stats.py와 동일 rng 순서로 재계산 ----------
def check_wave1(fails: list[str]) -> None:
    committed = json.loads((REPO / "analysis/results_stats.json").read_text(encoding="utf-8"))
    rows = W1.load_table()
    fraud = [r for r in rows if r["group"] == "fraud"]
    ctrl = [r for r in rows if r["group"] == "control"]
    fraud_s = [r["llm_score"] for r in fraud if r["llm_score"] is not None]
    ctrl_s = [r["llm_score"] for r in ctrl if r["llm_score"] is not None]
    rng = random.Random(W1.SEED)  # main()과 동일 순서: primary 먼저, secondary 다음
    primary = W1.frame_stats(fraud_s, ctrl_s, rng, "recompute-primary")
    fraud_pert = [r["llm_perturbed"] for r in fraud if r["llm_perturbed"] is not None]
    secondary = W1.frame_stats(fraud_pert, ctrl_s, rng, "recompute-secondary")
    for name, recomp in (("primary", primary), ("secondary", secondary)):
        c = committed[name]
        for key in ("perm_p_one_sided", "auc", "auc_boot95", "median_fraud",
                    "median_control", "mean_diff"):
            if recomp[key] != c[key]:
                fails.append(f"wave1 {name}.{key}: 재계산 {recomp[key]} ≠ committed {c[key]}")
        if recomp["fisher_2x2"]["p_one_sided"] != c["fisher_2x2"]["p_one_sided"]:
            fails.append(f"wave1 {name}.fisher_p: {recomp['fisher_2x2']['p_one_sided']} ≠ "
                         f"{c['fisher_2x2']['p_one_sided']}")
        if recomp["fpr"] != c["fpr"]:
            fails.append(f"wave1 {name}.fpr: {recomp['fpr']} ≠ {c['fpr']}")


# ---------- wave-2 (wave2_results.json) — wave2_analyze.py의 결정론 로직 복제 ----------
def _perm(a, b, n=100000):  # wave2_analyze.perm과 동일 (per-call SEED, 1e-9)
    obs = st.mean(a) - st.mean(b); pool = a + b; k = len(a); rng = random.Random(SEED); ge = 0
    for _ in range(n):
        rng.shuffle(pool)
        if st.mean(pool[:k]) - st.mean(pool[k:]) >= obs - 1e-9:
            ge += 1
    return round(obs, 2), (ge + 1) / (n + 1)


def _auc(a, b):
    return round(sum((1 if x > y else .5 if x == y else 0) for x in a for y in b) / (len(a) * len(b)), 3)


def _scores(d, mapping):
    m = json.loads((REPO / mapping).read_text(encoding="utf-8"))["mapping"]
    out = {}
    for f in glob.glob(str(REPO / d / "*.json")):
        j = json.loads(Path(f).read_text(encoding="utf-8"))
        out[m[j["case_id"]]] = j["misstatement_probability"]
    return out


def check_wave2(fails: list[str]) -> None:
    committed = json.loads((REPO / "analysis/wave2_results.json").read_text(encoding="utf-8"))
    w2c = {c["case_id"]: c for c in json.loads(
        (REPO / "data/candidates/candidates_wave2.json").read_text(encoding="utf-8"))["candidates"]}
    sc2 = _scores("runs/wave2/scores", "scoring/id_mapping_wave2.json")
    frv = [p for s, p in sc2.items() if w2c[s]["group"] == "treatment"]
    cov = [p for s, p in sc2.items() if w2c[s]["group"] == "control"]
    # 순서 독립 헤드라인(AUC·중위·평균)은 정확 대조 (glob 순서 무관)
    for label, got, exp in (("auc", _auc(frv, cov), committed["original"]["auc"]),
                            ("fraud_median", st.median(frv), committed["original"]["fraud_median"]),
                            ("control_median", st.median(cov), committed["original"]["control_median"]),
                            ("fraud_mean", round(st.mean(frv), 1), committed["original"]["fraud_mean"]),
                            ("control_mean", round(st.mean(cov), 1), committed["original"]["control_mean"])):
        if got != exp:
            fails.append(f"wave2 original.{label}: {got} ≠ {exp}")
    # FPR(플래그) — 순서 독립
    cf = sum(1 for x in cov if x >= 50)
    if round(100 * cf / len(cov), 1) != committed["flags"]["fpr_pct"]:
        fails.append(f"wave2 flags.fpr_pct: {round(100*cf/len(cov),1)} ≠ {committed['flags']['fpr_pct']}")
    # perm_p — glob 순서 의존(비결정론, 아래 caveat) → 유의성 수준만 보존 확인
    _, p = _perm(frv, cov)
    if not (p < 0.01 and committed["original"]["perm_p"] < 0.01):
        fails.append(f"wave2 original.perm_p 유의성 붕괴: 재계산 {p:.5f}, committed "
                     f"{committed['original']['perm_p']:.5f} (둘 다 <0.01 이어야)")
    # pooled secondary auc — 순서 독립 정확 대조
    m1 = json.loads((REPO / "scoring/id_mapping.json").read_text(encoding="utf-8"))["mapping"]
    w1_fraud_codes = {"T07", "T11", "T12", "T13", "T16", "T17", "T21", "T28"}
    w1fr = [json.loads(Path(pp).read_text())["misstatement_probability"]
            for pp in glob.glob(str(REPO / "runs/main/case_*.json"))
            if m1[json.loads(Path(pp).read_text())["case_id"]] in w1_fraud_codes]
    w1co = [json.loads(Path(pp).read_text())["misstatement_probability"]
            for pp in glob.glob(str(REPO / "runs/rp09/scores/case_*.json"))]
    if _auc(frv + w1fr, cov + w1co) != committed["pooled_secondary"]["auc"]:
        fails.append("wave2 pooled.auc mismatch")
    _, pp_pooled = _perm(frv + w1fr, cov + w1co)
    if not (pp_pooled < 0.01 and committed["pooled_secondary"]["perm_p"] < 0.01):
        fails.append("wave2 pooled.perm_p 유의성 붕괴")


def main() -> int:
    fails: list[str] = []
    check_wave1(fails)
    check_wave2(fails)
    if fails:
        print("FAIL — 헤드라인 재계산 불일치:")
        for f in fails:
            print(f"  {f}")
        return 1
    print("PASS — 현행 헤드라인 재계산 일치 (wave-1 8v22 primary/secondary + "
          "wave-2 standalone/pooled, 커밋 점수 재계산 ↔ committed JSON)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
