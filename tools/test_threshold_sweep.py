"""analysis/threshold_sweep.py 위생 검증 (캐시 불요, CI 커버).

미터링 0·네트워크 0: 동결 점수만 읽는 순수 재계산의 계약을 고정한다.
- t=50 혼동행렬이 동결 산출물(results_stats.json fisher_2x2 · wave2_results.json flags)과 일치
- t=50 Fisher p 가 results_stats.json 과 일치 (추정기 재사용 증명)
- TP 는 t 증가에 따라 비증가(단조) — 각 코호트
- FPR 0카운트 → rule-of-three, sensitivity = tp/n_fraud
비싼 순열은 통합 지점(코호트당 t=50 1회)만 호출해 러너 미실행·저비용 유지.
"""
import json
import random
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "analysis"))

import threshold_sweep as sweep  # noqa: E402


def _wave1():
    c = sweep.load_wave1()
    return c["fraud"], c["control"]


def _wave2():
    c = sweep.load_wave2()
    return c["fraud"], c["control"]


# ---------- 코호트 크기 (동결 스펙) ----------

def test_cohort_sizes():
    f1, c1 = _wave1()
    f2, c2 = _wave2()
    h = sweep.load_holdout()
    assert (len(f1), len(c1)) == (8, 22)
    assert (len(f2), len(c2)) == (9, 23)
    assert (len(h["fraud"]), len(h["control"])) == (3, 0)


# ---------- t=50 혼동행렬 = 동결 산출물 ----------

def test_wave1_t50_matches_results_stats():
    f, c = _wave1()
    tp, fp, fn, tn = sweep.confusion(f, c, 50)
    frozen = json.loads(
        (REPO / "analysis/results_stats.json").read_text())["primary"]["fisher_2x2"]
    assert frozen["threshold"] == 50
    assert (tp, fn, fp, tn) == (frozen["tp"], frozen["fn"],
                                frozen["fp"], frozen["tn"])
    assert (tp, fn, fp, tn) == (6, 2, 3, 19)


def test_wave2_t50_matches_wave2_results():
    f, c = _wave2()
    tp, fp, fn, tn = sweep.confusion(f, c, 50)
    flags = json.loads(
        (REPO / "analysis/wave2_results.json").read_text())["flags"]
    assert f"{tp}/{len(f)}" == flags["fraud"]        # "7/9"
    assert f"{fp}/{len(c)}" == flags["control_fp"]   # "5/23"
    assert (tp, fp) == (7, 5)


# ---------- t=50 Fisher p = 동결 (추정기 재사용) ----------

def test_wave1_t50_fisher_p_matches_frozen():
    f, c = _wave1()
    rng = random.Random(sweep.SEED)
    row = sweep.sweep_row("wave-1", f, c, 50, rng)
    frozen_p = json.loads(
        (REPO / "analysis/results_stats.json").read_text()
    )["primary"]["fisher_2x2"]["p_one_sided"]
    assert row["fisher_p"] == frozen_p            # 0.003145
    # 플래그 순열 p 는 Fisher 와 근접해야 (같은 2x2 의 두 검정)
    assert abs(row["flag_perm_p"] - frozen_p) < 0.01


# ---------- 단조성: TP 는 t 증가에 비증가 ----------

def test_tp_monotone_nonincreasing_in_t():
    for fraud, control in (_wave1(), _wave2(),
                           (sweep.load_holdout()["fraud"], [])):
        tps = [sweep.confusion(fraud, control, t)[0] for t in sweep.THRESHOLDS]
        assert all(a >= b for a, b in zip(tps, tps[1:])), tps
        # FP 도 비증가
        if control:
            fps = [sweep.confusion(fraud, control, t)[1]
                   for t in sweep.THRESHOLDS]
            assert all(a >= b for a, b in zip(fps, fps[1:])), fps


# ---------- FPR 규칙 + 민감도 정의 ----------

def test_fpr_rule_of_three_and_sensitivity():
    f, c = _wave2()
    rng = random.Random(sweep.SEED)
    # wave-2 t=60: FP=0 → rule-of-three (3/n)
    tp, fp, fn, tn = sweep.confusion(f, c, 60)
    assert fp == 0
    row = sweep.sweep_row("wave-2", f, c, 60, rng)
    assert row["fpr_rule"] == "rule-of-three"
    assert row["fpr_upper95_pct"] == round(300 / len(c), 1)
    assert row["sensitivity"] == round(tp / len(f), 4)


# ---------- holdout: control 없음 → FP/FPR/p = n/a, 민감도만 ----------

def test_holdout_has_no_control_metrics():
    h = sweep.load_holdout()
    rng = random.Random(sweep.SEED)
    row = sweep.sweep_row(h["cohort"], h["fraud"], h["control"], 50, rng)
    assert row["fp"] is None and row["tn"] is None
    assert row["fpr_point_pct"] is None and row["fisher_p"] is None
    assert row["flag_perm_p"] is None
    assert row["sensitivity"] is not None
