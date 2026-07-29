"""발행 수치 재계산 게이트 — 결정 표 · 홀드아웃 E1 · wave-2 rev2 · 보정 ·
재추첨 밴드 · name-ID (BN-13, F-01 ×2).

`tools/reproduce_analysis.py`의 recompute 게이트는 RP-05/wave-1에서 멈춘다 —
RESULTS 행 3/6/9/10/13이 인용하는 wave-2 분리 통계, 홀드아웃 대조군 수치,
결정 표(헤드라인 71.4% 셀 = L4 T≥50 오탐 5/7 포함)는 지금까지 커밋 산출물
그대로 신뢰됐다 (E-001급 사각). 테스트 (a)–(c)는 그 산출물을 커밋된 runs/
점수·매핑·후보 명부만으로 재계산해 드리프트 시 verify-public을 실패시킨다.
테스트 (d)–(f)는 같은 경계를 RESULTS 행 4/7/11의 corpus-free 산출물로 확장한다:
(d) calibration_wave2.json(ECE 0.179)을 wave2_results.json에서 동결 10-bin
정의로, (e) holdout_redraw_results.json 밴드를 runs/holdout/scores +
mainscore_redraw/draw_2..5에서 §7 규칙으로, (f) name-ID 헤드라인(15/30 ·
7/32)을 프로브 행 기록·동결 name_match 재적용으로 재계산해 대조한다.
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
sys.path.append(str(REPO / "scoring"))  # probe_verdict (동결 name_match)

from analysis.decision_table import build  # noqa: E402
from analysis.holdout_controls_analyze import (  # noqa: E402
    HOLDOUT, clopper_pearson, exact_perm_p, load_p,
)
from analysis.holdout_redraw_analyze import (  # noqa: E402
    CASES as REDRAW_CASES, DRAWS as REDRAW_DRAWS, load_p as redraw_load_p,
)
from analysis.wave2_analyze import compute_results  # noqa: E402
from probe_verdict import name_match  # noqa: E402

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


def test_calibration_wave2_recompute_equals_committed_artifact():
    """(d) RESULTS 행 11 — wave-2 보정 재계산 == analysis/calibration_wave2.json.

    calibration_wave2.py의 동결 정의(10-bin ECE, 확신 |p−50|/50, 임계 p>=50)를
    analysis/wave2_results.json에서 인메모리로 재적용 — 파일 쓰기 없음. 전부
    결정론이라 정확 일치를 요구한다.
    """
    r = _load_json("analysis/wave2_results.json")["original"]
    pts = [(s / 100, 1) for s in r["fraud_scores"]] + [(s / 100, 0) for s in r["control_scores"]]
    n = len(pts)

    bins = [[] for _ in range(10)]
    for p, y in pts:
        bins[min(int(p * 10), 9)].append((p, y))
    ece = 0.0
    diagram = []
    for b in bins:
        if not b:
            diagram.append(None)
            continue
        mp = sum(p for p, _ in b) / len(b)
        my = sum(y for _, y in b) / len(b)
        ece += (len(b) / n) * abs(mp - my)
        diagram.append({"n": len(b), "mean_pred": round(mp, 3), "frac_pos": round(my, 3)})

    conf = [abs(p * 100 - 50) / 50 for p, _ in pts]
    corr = [1 if ((p * 100 >= 50) == bool(y)) else 0 for p, y in pts]
    pos = [conf[i] for i in range(n) if corr[i]]
    neg = [conf[i] for i in range(n) if not corr[i]]
    auroc = (sum((a > b) + 0.5 * (a == b) for a in pos for b in neg)
             / (len(pos) * len(neg))) if pos and neg else None

    want = _load_json("analysis/calibration_wave2.json")
    assert n == want["n"]
    assert len(r["fraud_scores"]) == want["n_fraud"]
    assert len(r["control_scores"]) == want["n_control"]
    assert round(ece, 3) == want["ece_10bin"]
    assert round(ece - want["wave1_ece_10bin_reference"], 3) == want["delta_vs_wave1"]
    assert round(auroc, 3) == want["confidence_correctness_auroc"]
    assert f"{sum(corr)}/{n}" == want["threshold_accuracy"]
    assert diagram == want["reliability_diagram_10bin"]


def test_holdout_redraw_recompute_equals_committed_artifact():
    """(e) RESULTS 행 7 — 재추첨 밴드 재계산 == analysis/holdout_redraw_results.json.

    holdout_redraw_analyze.main()과 동일 로직(§7-3 판정 규칙 그대로) — 파일
    쓰기만 없음. 입력은 커밋된 runs/holdout/scores(draw-1) +
    runs/holdout/mainscore_redraw/draw_2..5.
    """
    scores = {c: {} for c in REDRAW_CASES}
    for c in REDRAW_CASES:
        scores[c][1] = redraw_load_p(f"runs/holdout/scores/{c}.json")
        for d in (2, 3, 4, 5):
            scores[c][d] = redraw_load_p(f"runs/holdout/mainscore_redraw/draw_{d}/{c}.json")

    assert all(scores[c][1] is not None for c in REDRAW_CASES), "draw-1 (동결 published) 부재"
    done = [d for d in REDRAW_DRAWS if all(scores[c][d] is not None for c in REDRAW_CASES)]
    k = len(done)

    per_case = {}
    for c, t in REDRAW_CASES.items():
        vals = [scores[c][d] for d in done]
        per_case[t] = {
            "published_draw1": scores[c][1],
            "by_draw": {f"draw_{d}": scores[c][d] for d in REDRAW_DRAWS},
            "median": statistics.median(vals),
            "band_min": min(vals),
            "band_max": max(vals),
            "n_ge50": sum(1 for v in vals if v >= 50),
            "k": k,
        }

    hubg_ge50 = per_case["HUBG"]["n_ge50"]
    if k == 5:
        primary = ("H2 탐지는 draw 잡음에 강건(robust) — HUBG p>=50 {}/5 (>=4 충족)"
                   .format(hubg_ge50) if hubg_ge50 >= 4 else
                   "draw-민감으로 보고 (HUBG p>=50 {}/5 <=3) — 표현 완화 없음".format(hubg_ge50))
    else:
        primary = f"PARTIAL k={k}/5 — 판정 유보 (HUBG p>=50 잠정 {hubg_ge50}/{k})"

    instability = {t: per_case[t]["n_ge50"] for t in ("WMK", "GNE")}
    flags = [t for t, n in instability.items() if n >= 2]

    got = {
        "plan": "W2_MAINSCORE_REDRAW_PLAN.md §7 (로그된 개정 #1)",
        "k_completed": k, "draws_done": done,
        "per_case": per_case,
        "primary_rule_HUBG": {"n_ge50": hubg_ge50, "threshold": "4/5", "verdict": primary},
        "secondary_instability": {"counts": instability,
                                  "flagged": flags,
                                  "note": "'불안정' 보고 전용 — 신규 탐지 승격 금지 (§7-3)"},
        "invariants": "H1 미주장(N=3) · 발행 per-case = draw-1 유지 (§3 승계)",
    }
    want = _load_json("analysis/holdout_redraw_results.json")
    assert json.loads(json.dumps(got, ensure_ascii=False)) == want


def test_name_probe_counts_match_headers_and_synthesis():
    """(f) RESULTS 행 4 — name-ID 헤드라인(15/30 · 7/32)을 행 기록에서 재집계.

    wave-1 15/30은 name_probe_results.json 행 기록 재집계, wave-2 7/32는 커밋
    프로브 원문(scoring/probe_results_wave2/recognition)에 동결 name_match를
    재적용해 재계산 — 각 산출물의 헤더 합계와 synthesis.json의 게시 필드
    (name_id_pct · wave2_name_id_reconcile)에 대조한다.
    """
    # wave-1 v1 프레임 — 행 재집계 == 헤더 합계 (RESULTS 행 4 첫 값 15/30)
    v1 = _load_json("analysis/name_probe_results.json")
    assert len(v1["rows"]) == v1["n_probes"] == 30
    assert sum(r["recognized"] for r in v1["rows"]) == v1["recognized_total"] == 15
    assert v1["rate_pct"] == round(100 * v1["recognized_total"] / v1["n_probes"], 1)
    for grp, blk in v1["by_group"].items():
        rows = [r for r in v1["rows"] if r["group"] == grp]
        assert len(rows) == blk["n"], grp
        assert sum(r["recognized"] for r in rows) == blk["recognized"], grp

    # v2ds 산출물 — 각 프레임 행 재집계 == 자체 헤더, 동결 v1 기준선 문자열 대조
    v2 = _load_json("analysis/name_probe_results_v2ds.json")
    for tier, n_exp in (("wave1", 30), ("wave2", 32)):
        f = v2[tier]
        assert len(f["rows"]) == f["n"] == n_exp, tier
        assert sum(r["recognized"] for r in f["rows"]) == f["recognized"], tier
        assert f["rate_pct"] == round(100 * f["recognized"] / f["n"], 1), tier
        assert f["delta_vs_v1_pp"] == round(f["rate_pct"] - f["v1_frozen"]["rate_pct"], 1), tier
    assert v2["wave1"]["v1_frozen"] == {
        "count": f"{v1['recognized_total']}/{v1['n_probes']}", "rate_pct": v1["rate_pct"]}

    # wave-2 v1 프레임 7/32 — 동결 name_match를 커밋 프로브 행 기록에 재적용
    mapping = _load_json("scoring/id_mapping_wave2.json")["mapping"]
    cands = {c["case_id"]: c
             for c in _load_json("data/candidates/candidates_wave2.json")["candidates"]}
    frauds = set(_load_json("runs/wave2/fraud_case_ids.json"))
    counts = {"fraud": [0, 0], "control": [0, 0]}  # [n, recognized]
    for p in sorted((REPO / "scoring/probe_results_wave2/recognition").glob("case_*.json")):
        guess = json.loads(p.read_text(encoding="utf-8"))["company_guess"]
        truth = cands[mapping[p.stem]]["company_name"]
        grp = counts["fraud" if p.stem in frauds else "control"]
        grp[0] += 1
        grp[1] += bool(name_match(guess, truth))
    n = counts["fraud"][0] + counts["control"][0]
    rec = counts["fraud"][1] + counts["control"][1]
    assert (n, rec) == (32, 7)

    # 게시 필드 대조 — v2ds 동결 기준선 + synthesis.json (RESULTS 행 4 소스)
    frozen_pct = round(100 * rec / n, 1)
    assert v2["wave2"]["v1_frozen"] == {"count": f"{rec}/{n}", "rate_pct": frozen_pct}
    syn = _load_json("analysis/synthesis.json")
    reconcile = syn["wave2_name_id_reconcile"]
    assert reconcile["frozen_rule_pct"] == frozen_pct
    assert reconcile["frozen_rule_count"] == (
        f"{rec}/{n} (fraud {counts['fraud'][1]}/{counts['fraud'][0]}, "
        f"control {counts['control'][1]}/{counts['control'][0]})")
    dose = {d["tier"]: d["name_id_pct"] for d in syn["memorization_dose_response"]}
    assert dose["wave1 (famous)"] == v1["rate_pct"]
    assert dose["wave2 (less-famous)"] == frozen_pct
