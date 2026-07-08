"""Track 1 (하드닝 2026-07-08): 플래그 임계 민감도 스윕 — 순수 재계산.

동결 점수(runs/main·wave2·holdout)만 읽어, 임계 t를 스윕하며 코호트별 혼동행렬·
FPR(Clopper-Pearson/rule-of-three)·민감도·Fisher p·플래그 순열 p를 재계산한다.
추정기는 analysis/stats.py의 기존 함수를 재사용(재발명 금지).

미터링 0 · 네트워크 0 · frozen 무침해. runner/grader/probe 미실행.
결정론: seed 고정, 네트워크 없음.
사용: python analysis/threshold_sweep.py

산출: analysis/threshold_sensitivity.csv + (md/fig는 각 스크립트 참조)

본 결과는 Claude 기반 단일 파이프라인에 한정.
"""
import csv
import json
import random
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import stats  # noqa: E402  (기존 추정기 재사용: perm_test_mean/fisher_one_sided/fpr_bound/auc)

# 스윕 대상 임계 (동결 스펙 §Track 1). 발행 임계 = 50.
THRESHOLDS = [40, 42, 44, 45, 46, 48, 50, 52, 54, 55, 56, 58, 60]
PUBLISHED_T = 50
SEED = stats.SEED  # 20260707


# --------------------------------------------------------------------------- #
# 동결 점수 로더 (읽기 전용)
# --------------------------------------------------------------------------- #
def load_wave1():
    """wave-1 8v22: baseline_table.csv 의 llm_score, group∈{fraud,control}."""
    rows = list(csv.DictReader(
        open(REPO / "analysis/baseline_table.csv", encoding="utf-8")))
    fraud, control = [], []
    for r in rows:
        v = r["llm_score"]
        if v in ("", "None", None):
            continue
        (fraud if r["group"] == "fraud" else control).append(float(v))
    return {"cohort": "wave-1 (8v22)", "fraud": fraud, "control": control,
            "score_field": "llm_score"}


def load_wave2():
    """wave-2 9v23: runs/wave2/scores/*.json misstatement_probability.
    fraud = runs/wave2/fraud_case_ids.json; 나머지는 control."""
    fraud_ids = set(json.loads(
        (REPO / "runs/wave2/fraud_case_ids.json").read_text()))
    fraud, control = [], []
    for f in sorted((REPO / "runs/wave2/scores").glob("*.json")):
        j = json.loads(f.read_text())
        v = float(j["misstatement_probability"])
        (fraud if j["case_id"] in fraud_ids else control).append(v)
    return {"cohort": "wave-2 (9v23)", "fraud": fraud, "control": control,
            "score_field": "misstatement_probability"}


def load_holdout():
    """holdout: runs/holdout/scores/*.json — 3건 전부 fraud, control 없음."""
    fraud = []
    for f in sorted((REPO / "runs/holdout/scores").glob("*.json")):
        j = json.loads(f.read_text())
        fraud.append(float(j["misstatement_probability"]))
    return {"cohort": "holdout (3v0)", "fraud": fraud, "control": [],
            "score_field": "misstatement_probability"}


# --------------------------------------------------------------------------- #
# 임계별 재계산
# --------------------------------------------------------------------------- #
def confusion(fraud, control, t):
    """임계 t 에서의 혼동행렬. 플래그: score >= t → 1.
    control 이 비면 fp/tn 은 None (holdout). 순열 없이 저비용 — 테스트가 재사용."""
    tp = sum(1 for s in fraud if s >= t)
    fn = len(fraud) - tp
    if not control:
        return tp, None, fn, None
    fp = sum(1 for s in control if s >= t)
    tn = len(control) - fp
    return tp, fp, fn, tn


def sweep_row(cohort, fraud, control, t, rng):
    """임계 t 에서의 혼동행렬 + FPR + 민감도 + Fisher/순열 p.

    플래그: score >= t → 1. 순열 p 는 t 에서의 이진 플래그 라벨을 순열
    (stats.perm_test_mean, (b+1)/(m+1)). control 이 없으면 FP/FPR/p 는 n/a.
    """
    tp, _fp, fn, _tn = confusion(fraud, control, t)
    sensitivity = tp / len(fraud) if fraud else None

    row = {
        "cohort": cohort, "t": t,
        "n_fraud": len(fraud), "n_control": len(control),
        "tp": tp, "fn": fn, "fp": None, "tn": None,
        "sensitivity": round(sensitivity, 4) if sensitivity is not None else None,
        "fpr_point_pct": None, "fpr_lo_pct": None,
        "fpr_upper95_pct": None, "fpr_rule": None,
        "fisher_p": None, "flag_perm_p": None,
    }
    if not control:
        return row  # holdout: control 없음 → FP/FPR/Fisher/순열 = n/a

    fp = _fp
    tn = _tn
    fraud_flag = [1 if s >= t else 0 for s in fraud]
    control_flag = [1 if s >= t else 0 for s in control]
    fpr = stats.fpr_bound(fp, len(control))
    fisher_p = stats.fisher_one_sided(tp, fn, fp, tn)
    perm_p, _ = stats.perm_test_mean(fraud_flag, control_flag, rng)

    row.update({
        "fp": fp, "tn": tn,
        "fpr_point_pct": round(100 * fp / len(control), 1),
        "fpr_lo_pct": fpr.get("lo_pct", 0.0),
        "fpr_upper95_pct": fpr["upper95_pct"],
        "fpr_rule": fpr["rule"],
        "fisher_p": round(fisher_p, 6),
        "flag_perm_p": round(perm_p, 6),
    })
    return row


def run_sweep():
    """모든 코호트 × 임계 스윕. 결정론(seed 고정)."""
    cohorts = [load_wave1(), load_wave2(), load_holdout()]
    rng = random.Random(SEED)
    rows = []
    for c in cohorts:
        for t in THRESHOLDS:
            rows.append(sweep_row(c["cohort"], c["fraud"], c["control"], t, rng))
    # 임계 무관 교차검증용 AUC
    aucs = {}
    for c in cohorts:
        aucs[c["cohort"]] = (round(stats.auc(c["fraud"], c["control"]), 4)
                             if c["control"] else None)
    return cohorts, rows, aucs


CSV_FIELDS = [
    "cohort", "t", "n_fraud", "n_control", "tp", "fp", "fn", "tn",
    "sensitivity", "fpr_point_pct", "fpr_lo_pct", "fpr_upper95_pct",
    "fpr_rule", "fisher_p", "flag_perm_p",
]


def write_csv(rows, path):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CSV_FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k))
                        for k in CSV_FIELDS})


def main() -> int:
    cohorts, rows, aucs = run_sweep()
    out_csv = REPO / "analysis/threshold_sensitivity.csv"
    write_csv(rows, out_csv)

    print("# 플래그 임계 민감도 스윕 (재계산, grader-free)")
    print(f"seed={SEED} · 임계 {THRESHOLDS} · 발행 임계 t={PUBLISHED_T}")
    for c in cohorts:
        name = c["cohort"]
        print(f"\n## {name}  (AUC={aucs[name]}, 임계 무관)")
        hdr = ("  t   TP  FP  FN  TN   sens   FPR%   FPR95%   Fisher_p  perm_p")
        print(hdr)
        for r in rows:
            if r["cohort"] != name:
                continue
            def g(k, w, nd=None):
                v = r[k]
                if v is None:
                    return "n/a".rjust(w)
                if nd is not None:
                    return f"{v:.{nd}f}".rjust(w)
                return str(v).rjust(w)
            print(f"{r['t']:>3}  {g('tp',3)} {g('fp',3)} {g('fn',3)} {g('tn',3)}"
                  f"  {g('sensitivity',5,3)}  {g('fpr_point_pct',5,1)}"
                  f"  {g('fpr_upper95_pct',6,1)}  {g('fisher_p',8,4)}"
                  f"  {g('flag_perm_p',6,4)}")
    print(f"\nwrote {out_csv.relative_to(REPO)}")
    print("본 결과는 Claude 기반 단일 파이프라인에 한정.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
