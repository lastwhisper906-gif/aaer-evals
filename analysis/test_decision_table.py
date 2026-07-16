"""decision_table 픽스처 테스트 — 셀 산술·null fail-closed·비용 정의 불능 (무호출)."""
import decision_table as dt


def _traj_case(cid, group, points):
    # points: (llm_p, b3_score) — quarters 등은 셀 계산에 불사용
    return {"case_id": cid, "group": group,
            "snapshots": [{"j": j, "llm_p": p, "b3_score": b}
                          for j, (p, b) in enumerate(points)]}


def test_cell_counts_and_ci_bounds():
    c = dt.cell([80, 60, 40, 10], [30, 55], threshold=50, n_screens=6)
    assert c["detected"] == 2 and c["n_treatment"] == 4
    assert c["false_positives"] == 1 and c["n_control"] == 2
    lo, hi = c["detected_ci95"]
    assert 0.0 <= lo <= 0.5 <= hi <= 1.0  # 점추정 2/4를 구간이 감싼다
    assert c["cost_per_detection_usd"] == round(6 * dt.COST_PER_SCREEN_USD / 2, 2)


def test_cell_zero_detection_cost_undefined():
    c = dt.cell([10, 20], [5], threshold=70, n_screens=3)
    assert c["detected"] == 0
    assert c["cost_per_detection_usd"] is None  # 0으로 나누지 않는다 (§4)


def test_trajectory_any_snapshot_and_null_skip():
    cases = [
        _traj_case("t1", "treatment", [(None, 2), (60, 0), (10, 1)]),  # llm hit @60
        _traj_case("t2", "treatment", [(None, 2), (None, 2)]),          # 전부 null → 미플래그
        _traj_case("c1", "control", [(55, 0)]),                          # 오탐
    ]
    flagged, nulls = dt.trajectory_flags([c for c in cases if c["group"] == "treatment"], 50)
    assert flagged == ["t1"] and nulls == 3
    cell = dt.trajectory_cell(cases, 50, n_screens=3)
    assert cell["detected"] == 1 and cell["n_treatment"] == 2
    assert cell["false_positives"] == 1 and cell["n_control"] == 1


def test_trajectory_b3_gate_conjunction_same_snapshot():
    # llm 60은 b3=0 스냅샷, b3=2는 llm 10 스냅샷 — 동일 스냅샷 결합이면 미플래그
    cases = [_traj_case("t1", "treatment", [(60, 0), (10, 2)]),
             _traj_case("c1", "control", [(60, 2)])]
    cell = dt.trajectory_cell(cases, 50, n_screens=3, require_b3_gate=True)
    assert cell["detected"] == 0
    assert cell["false_positives"] == 1  # c1은 동일 스냅샷에서 양쪽 충족


def test_count_scored_snapshots():
    cases = [_traj_case("t1", "treatment", [(None, 2), (60, 0)]),
             _traj_case("c1", "control", [(55, 0)])]
    scored, nulls = dt.count_scored_snapshots(cases)
    assert scored == 2 and nulls == 1
