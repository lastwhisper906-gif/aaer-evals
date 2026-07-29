"""발행 수치 재계산 게이트 — 결정 표 · 홀드아웃 E1 · wave-2 rev2 (BN-13, F-01).

`tools/reproduce_analysis.py`의 recompute 게이트는 RP-05/wave-1에서 멈춘다 —
RESULTS 행 3/6/9/10/13이 인용하는 wave-2 분리 통계, 홀드아웃 대조군 수치,
결정 표(헤드라인 71.4% 셀 = L4 T≥50 오탐 5/7 포함)는 지금까지 커밋 산출물
그대로 신뢰됐다 (E-001급 사각). 본 테스트 3종은 그 산출물을 커밋된 runs/
점수·매핑·후보 명부만으로 재계산해 드리프트 시 verify-public을 실패시킨다.
API 호출 0 · 파일 쓰기 0 · 외부 데이터 0 (verify-public 계층).

결정론 주의: 수치는 전부 결정론이나, wave-2의 perm_p 4종(seed 20260707,
n_perm=100k)과 부트스트랩 auc_ci는 입력 나열 순서에 민감한 Monte-Carlo
추정치다 — 동결 산출물은 생성 시점의 파일시스템 glob 순서로 계산됐고
(R3 cases 순서가 그 증거) 본 테스트는 이식성(CI ext4 ↔ 로컬 APFS)을 위해
정렬 순서로 적재한다. 따라서 그 다섯 값만 MC 잡음 허용치(perm_p ±3e-3
≈ 10σ 초과, auc_ci ±0.02)로 대조하고, 나머지 — 평균차·중앙값·AUC·Cliff·
Fisher 2×2·CP 구간·표본 수·정렬 점수 리스트 — 는 정확 일치를 요구한다
(실 데이터 드리프트는 정확 대조 필드에서 먼저 걸린다). Beneish/Dechow
베이스라인 블록은 ~/aaer-data 필요(verify-full 전용)라 설계상 제외 —
conclusion_rule의 r2·fired도 같은 이유로 제외한다 (r1·r3는 대조).
"""
import json
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))  # 직접 실행 안전 (pytest는 conftest가 주입)
# wave2_analyze의 `from screens import run_case`가 CWD 무관하게 풀리도록 선삽입
sys.path.insert(0, str(REPO / "scoring" / "baselines"))

from analysis.decision_table import build  # noqa: E402
from analysis.holdout_controls_analyze import (  # noqa: E402
    HOLDOUT, clopper_pearson, exact_perm_p, load_p,
)
from analysis.wave2_analyze import compute_results  # noqa: E402

PERM_TOL = 3e-3   # perm_p MC 잡음 (n_perm=100k, 나열 순서 차이 — 헤더 주석)
CI_TOL = 2e-2     # 부트스트랩 auc_ci MC 잡음 (n_boot=10k)


def _load_json(rel):
    return json.loads((REPO / rel).read_text(encoding="utf-8"))


def test_decision_table_build_equals_committed_artifact():
    """(a) decision_table.build() 전체 dict == analysis/decision_table.json."""
    got = json.loads(json.dumps(build(), ensure_ascii=False))
    want = _load_json("analysis/decision_table.json")
    assert got == want


def test_holdout_controls_recompute_equals_committed_artifact():
    """(b) 홀드아웃 E1 결과를 동결 함수로 재구성 == holdout_controls_results.json.

    holdout_controls_analyze.main()과 동일 로직 — 파일 쓰기만 없음.
    """
    mapping = _load_json("scoring/id_mapping_holdout_controls.json")
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

    got = {
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
    want = _load_json("analysis/holdout_controls_results.json")
    assert json.loads(json.dumps(got, ensure_ascii=False)) == want


def test_wave2_rev2_recompute_baseline_independent_blocks():
    """(c) wave-2 rev2 재계산 (베이스라인 무관 블록) == 커밋 산출물 + 동결 원본 대조.

    m_pairs/f_pairs 빈 입력 (Beneish/Dechow는 ~/aaer-data 필요 — verify-public
    제외 설계) — baselines·conclusion_rule r2/fired만 대조 제외.
    """
    mapping = _load_json("scoring/id_mapping_wave2.json")["mapping"]
    cands = {c["case_id"]: c
             for c in _load_json("data/candidates/candidates_wave2.json")["candidates"]}

    def load_dir(rel):
        out = {}
        for p in sorted((REPO / rel).glob("case_*.json")):
            rec = json.loads(p.read_text(encoding="utf-8"))
            out[mapping[rec["case_id"]]] = rec.get("misstatement_probability")
        return out

    scores = load_dir("runs/wave2/scores")
    perturbed = load_dir("runs/wave2/perturbed")
    fraud = {k: v for k, v in scores.items() if cands[k]["group"] == "treatment"}
    control = {k: v for k, v in scores.items() if cands[k]["group"] == "control"}

    # wave-1 풀링 입력 — load_wave1_scores와 동일 정의, 정렬·REPO 기준 적재
    w1_map = _load_json("scoring/id_mapping.json")["mapping"]
    w1_fraud_ids = {"T07", "T11", "T12", "T13", "T16", "T17", "T21", "T28"}
    wave1_fraud = [json.loads(p.read_text(encoding="utf-8"))["misstatement_probability"]
                   for p in sorted((REPO / "runs/main").glob("case_*.json"))
                   if w1_map[p.stem] in w1_fraud_ids]
    wave1_control = [json.loads(p.read_text(encoding="utf-8"))["misstatement_probability"]
                     for p in sorted((REPO / "runs/rp09/scores").glob("case_*.json"))]

    got = compute_results(fraud, control, perturbed, [], [],
                          wave1_fraud=wave1_fraud, wave1_control=wave1_control)
    rev2 = _load_json("analysis/out/wave2_rev2/wave2_results_rev2.json")

    # original — MC 2필드(perm_p·auc_ci)만 허용치, 나머지 정확
    g, w = got["original"], rev2["original"]
    for key in ("mean_diff", "cliff", "auc", "fraud_median", "control_median"):
        assert g[key] == w[key], key
    assert abs(g["perm_p"] - w["perm_p"]) < PERM_TOL
    assert all(abs(a - b) < CI_TOL for a, b in zip(g["auc_ci"], w["auc_ci"]))

    # perturbed_frame
    g, w = got["perturbed_frame"], rev2["perturbed_frame"]
    for key in ("n_perturbed", "available", "mean_diff", "auc"):
        assert g[key] == w[key], key
    assert abs(g["perm_p"] - w["perm_p"]) < PERM_TOL

    # fisher_2x2 · fpr — 전 필드 정확
    assert got["fisher_2x2"] == rev2["fisher_2x2"]
    assert got["fpr"] == rev2["fpr"]

    # worst_case_substitution
    g, w = got["worst_case_substitution"], rev2["worst_case_substitution"]
    assert g["n_incomplete"] == w["n_incomplete"]
    assert g["mean_diff"] == w["mean_diff"]
    assert abs(g["perm_p"] - w["perm_p"]) < PERM_TOL

    # R3_memorization — cases는 case_id 키로 (나열 순서는 glob 이력일 뿐)
    g, w = got["R3_memorization"], rev2["R3_memorization"]
    assert ({c["case_id"]: (c["delta_mean"], c["counts"]) for c in g["cases"]}
            == {c["case_id"]: (c["delta_mean"], c["counts"]) for c in w["cases"]})
    for key in ("n_counting", "n_treatment", "fires"):
        assert g[key] == w[key], key

    # conclusion_rule — r1·r3만 (r2·fired는 베이스라인 의존 — 헤더 주석)
    for key in ("r1", "r3"):
        assert (got["conclusion_rule_standalone"][key]
                == rev2["conclusion_rule_standalone"][key]), key

    # pooled_secondary
    g, w = got["pooled_secondary"], rev2["pooled_secondary"]
    for key in ("n_fraud", "n_control", "mean_diff", "auc"):
        assert g[key] == w[key], key
    assert abs(g["perm_p"] - w["perm_p"]) < PERM_TOL

    # 동결 wave-1 게시 소스 analysis/wave2_results.json "original" 공유 필드 대조
    frozen = _load_json("analysis/wave2_results.json")["original"]
    fraud_scores = sorted(v for v in fraud.values() if v is not None)
    control_scores = sorted(v for v in control.values() if v is not None)
    assert fraud_scores == frozen["fraud_scores"]
    assert control_scores == frozen["control_scores"]
    g = got["original"]
    assert round(g["mean_diff"], 2) == frozen["mean_diff"]
    assert round(g["cliff"], 3) == frozen["cliff"]
    assert round(g["auc"], 3) == frozen["auc"]
    assert g["fraud_median"] == frozen["fraud_median"]
    assert g["control_median"] == frozen["control_median"]
    assert round(statistics.mean(fraud_scores), 1) == frozen["fraud_mean"]
    assert round(statistics.mean(control_scores), 1) == frozen["control_mean"]
    assert abs(g["perm_p"] - frozen["perm_p"]) < PERM_TOL
    assert all(abs(a - b) < CI_TOL for a, b in zip(g["auc_ci"], frozen["auc_ci"]))
