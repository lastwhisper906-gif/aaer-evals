"""engine_verdict.py 픽스처 테스트 — 세 브랜치 전부 + fail-closed (D51, 무호출)."""
import pytest

import engine_verdict as ev


def _case(cid, group, points):
    """points: [(j, t, llm_p, b3)] — j=0이 최신 스냅샷."""
    return {"case_id": cid, "ticker": cid.upper(),
            "group": group,
            "snapshots": [{"j": j, "cutoff": f"2026-0{j+1}-01",
                           "quarters_to_revelation": t, "llm_p": p, "b3_score": b}
                          for j, t, p, b in points]}


def _traj(cases):
    return {"flag_threshold_llm": 50, "flag_threshold_b3": 2, "cases": cases}


CONTROLS = [_case(f"ctl{i}", "control", [(0, 0, 20 + i, 0)]) for i in range(3)]


def test_branch_a_llm_engine():
    # LLM이 3분기 전 돌파, B3는 j=0에서만 (lead 1) → med 3 >= 1+1
    treat = [_case(f"t{i}", "treatment",
                   [(0, 1, 80, 2), (1, 2, 70, 1), (2, 3, 60, 0), (3, 4, 30, 0)])
             for i in range(3)]
    v = ev.compute(_traj(treat + CONTROLS))
    assert v["branch"] == "a_llm_engine" and v["b_subcase"] is None
    assert v["median_lead_llm_quarters"] == 3 and v["median_lead_b3_quarters"] == 1
    assert v["per_case_leads"][0]["lead_b3_ge1"] == 2  # 민감도 열 병기 (판정 무가중)


def test_branch_b_strict_rules_engine():
    # B3가 리드타임·AUC 모두 우위 → (b) + b_strict
    treat = [_case(f"t{i}", "treatment",
                   [(0, 1, 55, 3), (1, 2, 40, 3), (2, 3, 30, 2)]) for i in range(3)]
    v = ev.compute(_traj(treat + CONTROLS))
    assert v["branch"] == "b_rules_engine" and v["b_subcase"] == "b_strict"
    assert v["median_lead_b3_quarters"] == 3 and v["median_lead_llm_quarters"] == 1


def test_branch_b_residual_sub_quarter_edge():
    # LLM 우위(중위 2.5 vs 2)지만 +1분기 미만 → 잔여 지대는 규칙 엔진 (보수 기본값)
    deep = [_case(f"td{i}", "treatment",
                  [(0, 1, 80, 1), (1, 2, 60, 2), (2, 3, 55, 1)]) for i in range(2)]
    shallow = [_case(f"ts{i}", "treatment",
                     [(0, 1, 80, 1), (1, 2, 60, 2), (2, 3, 30, 1)]) for i in range(2)]
    v = ev.compute(_traj(deep + shallow + CONTROLS))
    assert v["median_lead_llm_quarters"] == 2.5 and v["median_lead_b3_quarters"] == 2
    assert v["branch"] == "b_rules_engine" and v["b_subcase"] == "b_residual"


def test_branch_c_terminated():
    # 양쪽 다 j=0(t=1)에서만 켜짐 → 선행 신호 없음
    treat = [_case(f"t{i}", "treatment", [(0, 1, 70, 2), (1, 2, 30, 1)])
             for i in range(3)]
    v = ev.compute(_traj(treat + CONTROLS))
    assert v["branch"] == "c_terminated"
    assert v["median_lead_llm_quarters"] == 1 and v["median_lead_b3_quarters"] == 1


def test_never_crossing_lead_is_zero():
    treat = [_case("t0", "treatment", [(0, 1, 30, 0), (1, 2, 20, 0)])]
    v = ev.compute(_traj(treat + CONTROLS))
    lead = v["per_case_leads"][0]
    assert lead["lead_llm"] == 0 and lead["lead_b3"] == 0
    assert v["branch"] == "c_terminated"


def test_fail_closed():
    with pytest.raises(ev.VerdictError):  # 사전 등록 임계 위반
        ev.compute({"flag_threshold_llm": 60, "flag_threshold_b3": 2, "cases": []})
    with pytest.raises(ev.VerdictError):  # 빈 대조군
        ev.compute(_traj([_case("t0", "treatment", [(0, 1, 70, 2)])]))
    dup = _case("t0", "treatment", [(0, 1, 70, 2), (0, 1, 71, 2)])  # j=0 중복
    with pytest.raises(ev.VerdictError):
        ev.compute(_traj([dup] + CONTROLS))


# ── §4b B4 결합 (D58) ────────────────────────────────────────────────────────

def _case_b4(cid, group, points):
    """points: [(j, t, llm_p, b3, b4)] — b4 = b4_slope_aug|None."""
    return {"case_id": cid, "ticker": cid.upper(), "group": group,
            "snapshots": [{"j": j, "cutoff": f"2026-0{j+1}-01",
                           "quarters_to_revelation": t, "llm_p": p,
                           "b3_score": b, "b4_slope_aug": b4}
                          for j, t, p, b, b4 in points]}


def _a_branch_treat_b4(b4_j0, b4_deep):
    # LLM lead 3 vs B3 lead 1 → 기본 판정 (a); B4는 파라미터로 지배 여부 제어
    return [_case_b4(f"t{i}", "treatment",
                     [(0, 1, 80, 2, b4_j0), (1, 2, 70, 1, b4_deep),
                      (2, 3, 60, 0, b4_deep), (3, 4, 30, 0, b4_deep)])
            for i in range(3)]


CONTROLS_B4 = [_case_b4(f"ctl{i}", "control", [(0, 0, 20 + i, 0, 0.001 * i)])
               for i in range(3)]


def test_b4_dominating_demotes_a_to_b():
    # B4가 4분기 전부터 양(+) → lead 4 ≥ LLM 3; j=0 B4 AUC 완전 분리 ≥ LLM AUC
    treat = _a_branch_treat_b4(b4_j0=0.05, b4_deep=0.04)
    v = ev.compute(_traj(treat + CONTROLS_B4))
    assert v["b4_comparison"]["valid"] and v["b4_comparison"]["dominates_llm"]
    assert v["branch"] == "b_rules_engine" and v["b_subcase"] == "b4_dominated"
    assert v["b4_comparison"]["median_lead_b4"] == 4


def test_b4_valid_but_not_dominating_keeps_a():
    # B4는 j=0에서만 양 (lead 1 < LLM 3) → 성립하나 지배 아님 → (a) 유지
    treat = _a_branch_treat_b4(b4_j0=0.05, b4_deep=-0.01)
    v = ev.compute(_traj(treat + CONTROLS_B4))
    assert v["b4_comparison"]["valid"] and not v["b4_comparison"]["dominates_llm"]
    assert v["branch"] == "a_llm_engine"


def test_b4_coverage_below_70pct_invalid():
    # 실험군 3 중 1만 B4 커버 (1/3 < 70%) → 불성립, 기본 판정 그대로
    treat = (_a_branch_treat_b4(0.05, 0.04)[:1]
             + [_case_b4(f"tn{i}", "treatment",
                         [(0, 1, 80, 2, None), (1, 2, 70, 1, None),
                          (2, 3, 60, 0, None), (3, 4, 30, 0, None)])
                for i in range(2)])
    v = ev.compute(_traj(treat + CONTROLS_B4))
    assert not v["b4_comparison"]["valid"]
    assert "커버리지" in v["b4_comparison"]["reason"]
    assert v["branch"] == "a_llm_engine"


def test_b4_absent_key_backward_compatible():
    # b4 키가 아예 없는 구식 trajectories → 불성립·기본 판정 (기존 픽스처 호환)
    treat = [_case(f"t{i}", "treatment",
                   [(0, 1, 80, 2), (1, 2, 70, 1), (2, 3, 60, 0), (3, 4, 30, 0)])
             for i in range(3)]
    v = ev.compute(_traj(treat + CONTROLS))
    assert not v["b4_comparison"]["valid"]
    assert v["branch"] == "a_llm_engine"


def test_b4_never_rescues_b_or_c():
    # B4가 LLM에 지배당해도(유리해도) (c)는 (c) — §4b는 (a)만 건드린다
    treat = [_case_b4(f"t{i}", "treatment", [(0, 1, 70, 2, 0.05), (1, 2, 30, 1, 0.04)])
             for i in range(3)]
    v = ev.compute(_traj(treat + CONTROLS_B4))
    assert v["branch"] == "c_terminated"
