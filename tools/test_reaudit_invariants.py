"""Track 4 재감사 회귀 락 — BLINDNESS·CUTOFF 불변의 코드 강제 지점 고정.

이 파일은 다른 트랙과 충돌하지 않는 NEW 파일이다(distinct name). 기존
pipeline/test_* 는 건드리지 않고, 재감사에서 발견한 '테스트 공백'만 메운다.

커버하는 공백 (재감사 finding):
  F1  피평가자 송출부(runner.call_model / probe_runner.call_model)가
      forbid_markers=EVALUATEE_FORBIDDEN_MARKERS 를 반드시 넘긴다는 소스 수준 락.
      (기존 test_cli_client 는 guard_payload 동작만 검증하고, '호출부가 실제로
       가드를 인자로 넘기는가'는 검증하지 않았다 — 인자를 빠뜨리는 회귀가
       어떤 테스트도 깨지 않고 통과할 수 있었다.)
  F2  guard_payload 가 user_payload 뿐 아니라 system_prompt 도 스캔한다는 락
      (cli_client.call_model 이 두 인자 모두에 가드를 건다 — 기존 mutation 테스트는
       payload 에만 마커를 주입해 system_prompt 경로가 미커버였다).
  F3  load_pit_series 컷오프 경계 의미론: filed == cutoff 는 포함(허용)된다는 락
      (기존 컷오프 테스트는 filed>cutoff 제외만 검증, 경계 동등은 미검증).
"""
import ast
import datetime as dt
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
PIPELINE = REPO / "pipeline"
sys.path.insert(0, str(PIPELINE))

import build_payload as bp   # noqa: E402
import cli_client            # noqa: E402


# ─────────────────────────────────────────────────────────────────────────
# F1 — 피평가자 송출부는 반드시 payload 가드를 인자로 넘긴다 (소스 AST 락)
# ─────────────────────────────────────────────────────────────────────────
def _call_model_sites(py_path: Path):
    """py_path 안의 모든 call_model(...) 호출 노드를 반환."""
    tree = ast.parse(py_path.read_text(encoding="utf-8"), filename=str(py_path))
    sites = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            name = (f.attr if isinstance(f, ast.Attribute)
                    else f.id if isinstance(f, ast.Name) else None)
            if name == "call_model":
                sites.append(node)
    return sites


def _first_pos_model_name(call: ast.Call):
    if not call.args:
        return None
    a = call.args[0]
    return a.id if isinstance(a, ast.Name) else None


def _forbid_markers_kw(call: ast.Call):
    for kw in call.keywords:
        if kw.arg == "forbid_markers":
            return kw
    return None


@pytest.mark.parametrize("relpath", ["pipeline/runner.py", "pipeline/probe_runner.py"])
def test_evaluatee_send_sites_pass_payload_guard(relpath):
    """EVALUATEE_MODEL 로 나가는 모든 call_model 은 forbid_markers 를 넘겨야 한다.

    forbid_markers 가 없거나 None 이면 cli_client.call_model 이 guard_payload 를
    건너뛴다(cli_client.py: `if forbid_markers:`) — 정답지/카나리가 피평가자에게
    새는 경로. 이 락은 그런 회귀를 소스 수준에서 차단한다."""
    path = REPO / relpath
    sites = _call_model_sites(path)
    assert sites, f"{relpath}: call_model 호출을 찾지 못함 (구조 변경?)"
    evaluatee_sites = [c for c in sites if _first_pos_model_name(c) == "EVALUATEE_MODEL"]
    assert evaluatee_sites, f"{relpath}: EVALUATEE_MODEL 송출부를 찾지 못함"
    for call in evaluatee_sites:
        kw = _forbid_markers_kw(call)
        assert kw is not None, (
            f"{relpath}:{call.lineno} EVALUATEE_MODEL call_model 이 forbid_markers 미전달 "
            "— 가드 우회 (BLINDNESS 위반)")
        # 상수 None 금지 (변수/리스트/속성참조는 허용 — 값은 아래 테스트가 검증)
        assert not (isinstance(kw.value, ast.Constant) and kw.value.value is None), (
            f"{relpath}:{call.lineno} forbid_markers=None — 가드 비활성")


def test_probe_runner_marker_source_is_evaluatee_list():
    """probe_runner 의 두 분기(recognition/verbatim)가 모두 마커 소스를
    cli_client.EVALUATEE_FORBIDDEN_MARKERS 로 고정하는지 락."""
    src = (REPO / "pipeline/probe_runner.py").read_text(encoding="utf-8")
    assert src.count("cli_client.EVALUATEE_FORBIDDEN_MARKERS") >= 2, (
        "probe_runner 의 두 분기 중 하나가 EVALUATEE_FORBIDDEN_MARKERS 를 쓰지 않음")
    assert "forbid_markers=markers" in src


def test_runner_uses_evaluatee_forbidden_markers_symbol():
    src = (REPO / "pipeline/runner.py").read_text(encoding="utf-8")
    assert "forbid_markers=EVALUATEE_FORBIDDEN_MARKERS" in src


# ─────────────────────────────────────────────────────────────────────────
# F2 — guard_payload 는 system_prompt 도 스캔한다 (호출 미발생)
# ─────────────────────────────────────────────────────────────────────────
def test_guard_scans_system_prompt_no_subprocess(tmp_path, monkeypatch):
    """system_prompt 에 금지 마커가 있으면 subprocess 도달 전에 예외."""
    def _boom(*a, **k):
        raise AssertionError("guard 위반인데 subprocess.run 이 호출됨")
    monkeypatch.setattr(cli_client.subprocess, "run", _boom)

    with pytest.raises(cli_client.PayloadGuardError):
        cli_client.call_model(
            "claude-sonnet-5",
            system_prompt="analyze this beneish m_score",   # 마커: beneish, m_score
            user_payload='{"clean": true}',                 # payload 는 깨끗
            schema={"type": "object"},
            log_dir=tmp_path / "logs", log_name="t",
            forbid_markers=cli_client.EVALUATEE_FORBIDDEN_MARKERS)


def test_guard_payload_symmetric_on_both_args():
    """guard_payload 함수 자체: 마커 존재 시 예외, 부재 시 통과 (양방향)."""
    with pytest.raises(cli_client.PayloadGuardError):
        cli_client.guard_payload("...aaer-1272 matched_case...",
                                 cli_client.EVALUATEE_FORBIDDEN_MARKERS)
    # 깨끗한 문자열은 통과
    cli_client.guard_payload('{"revenue": 100, "ticker": "ZZ"}',
                             cli_client.EVALUATEE_FORBIDDEN_MARKERS)


# ─────────────────────────────────────────────────────────────────────────
# F3 — 컷오프 경계 동등(filed == cutoff)은 포함된다
# ─────────────────────────────────────────────────────────────────────────
def _corpus_equal_boundary(tmp_path, ticker="TSTEQ"):
    xb = tmp_path / ticker / "xbrl"
    xb.mkdir(parents=True)
    facts = {"facts": {"us-gaap": {"Revenues": {"units": {"USD": [
        # filed == cutoff → 포함돼야 함 (cutoff_date 는 폭로 '전일'로 정의)
        {"val": 500, "filed": "2019-12-31", "start": "2018-01-01", "end": "2018-12-31",
         "accn": "0000000000-00-000009", "form": "10-K"},
        # filed == cutoff+1 → 제외
        {"val": 999, "filed": "2020-01-01", "start": "2019-01-01", "end": "2019-12-31",
         "accn": "0000000000-00-000010", "form": "10-K"},
    ]}}}}}
    (xb / "CIK0000000009.json").write_text(json.dumps(facts), encoding="utf-8")
    return tmp_path


def test_load_pit_series_includes_filed_equal_cutoff(tmp_path, monkeypatch):
    monkeypatch.setattr(bp, "DATA_DIR", _corpus_equal_boundary(tmp_path))
    cutoff = dt.date(2019, 12, 31)
    series = bp.load_pit_series("TSTEQ", cutoff)
    vals = [v for vs in series.values() for v in vs]
    filed_dates = {v["filed"] for v in vals}
    assert "2019-12-31" in filed_dates, "filed == cutoff 항목이 잘못 제외됨 (경계 오프바이원)"
    assert "2020-01-01" not in filed_dates, "filed > cutoff 항목이 누출됨"
    assert all(dt.date.fromisoformat(v["filed"]) <= cutoff for v in vals)
