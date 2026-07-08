"""earliness_analyze 순수 지표 검증 (합성 궤적, 캐시/점수 불요, CI 상주)."""
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "analysis"))
import earliness_analyze as ea  # noqa: E402


def test_quarters_before():
    assert ea.quarters_before(dt.date(2016, 1, 1), dt.date(2016, 1, 1)) == 0.0
    # 약 4분기 전
    q = ea.quarters_before(dt.date(2016, 1, 1), dt.date(2015, 1, 2))
    assert 3.9 <= q <= 4.1


def test_lead_time_rising_trajectory():
    # 폭로 접근 시 상승, 8분기 전부터 p>=50 → 선행시간 = 가장 이른 켜짐 t
    traj = [(0, 78), (2, 65), (4, 55), (6, 52), (8, 40), (10, 30)]
    assert ea.detection_lead_time(traj) == 6      # t=6에서 처음 >=50 (t=8은 40)
    assert ea.detection_lead_time([(0, 40), (2, 30)]) is None  # 안 켜짐


def test_crossings_nonmonotone():
    # 켜졌다(t=8) 꺼졌다(t=6) 다시 켜짐(t=2) → 두 번의 상향 교차
    traj = [(8, 55), (6, 40), (4, 45), (2, 60), (0, 70)]
    assert ea.crossings(traj) == [8, 2]


def test_ols_slope_sign():
    # 폭로 접근(t 감소) 시 상승 → t와 p는 음의 상관 → 음의 기울기
    traj = [(0, 80), (4, 60), (8, 40)]
    s = ea.ols_slope(traj)
    assert s is not None and s < 0
    assert ea.ols_slope([(0, 50)]) is None


def test_flat_control_slope_near_zero():
    traj = [(0, 30), (2, 32), (4, 29), (6, 31)]
    assert abs(ea.ols_slope(traj)) < 2


def test_noise_band():
    traj = [(0, 50), (2, 52), (4, 40)]  # 50->52 (밴드 내), 52->40 (밴드 밖)
    # t 오름차순: (0,50)->(2,52) diff 2 <=6.3 True ; (2,52)->(4,40) diff 12 >6.3 False
    assert ea.neighbor_moves_within_band(traj) == [True, False]


def test_snapshot0_frame_consistency(tmp_path, monkeypatch):
    import json
    pert = tmp_path / "perturbed"; ident = tmp_path / "main"
    pert.mkdir(); ident.mkdir()
    (pert / "case_39.json").write_text(json.dumps({"misstatement_probability": 58}))
    (ident / "case_39.json").write_text(json.dumps({"misstatement_probability": 90}))
    monkeypatch.setattr(ea, "SNAPSHOT0_SOURCES",
                        {"perturbed": (pert,), "original": (ident,)})
    # 교란 궤적의 t=0은 교란 본실행(58)이어야 한다 — 정체(90) 아님 (프레임 일관 버그 회귀)
    assert ea._snapshot0_p("case_39", "perturbed") == 58
    assert ea._snapshot0_p("case_39", "original") == 90
    assert ea._snapshot0_p("case_04", "perturbed") is None  # 교란 본실행 부재(대조군)


def test_assemble_trajectory_omits_missing_snapshot0(tmp_path, monkeypatch):
    import json
    import datetime as dt
    snapdir = tmp_path / "snaps"; snapdir.mkdir()
    (snapdir / "case_04_s1.json").write_text(json.dumps({"misstatement_probability": 30}))
    monkeypatch.setattr(ea, "SNAPSHOT0_SOURCES", {"perturbed": (tmp_path / "none",)})
    traj = ea.assemble_trajectory(
        "case_04", dt.date(2019, 2, 20), snapdir,
        [{"case_id": "case_04_s1", "cutoff_date": "2018-11-01"}], frame="perturbed")
    assert len(traj) == 1 and traj[0][1] == 30.0 and traj[0][0] > 0  # t=0 생략, j=1만
