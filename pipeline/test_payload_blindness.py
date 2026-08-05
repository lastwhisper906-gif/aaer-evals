"""Regression tests for the exact JSON exposed to the evaluatee."""
import json
import copy
from pathlib import Path
from types import SimpleNamespace

import pytest

import build_payload as bp
import date_shift
import probe_runner
import runner
import runner_api


FIXTURES = Path(__file__).resolve().parent / "fixtures"
CORPUS = FIXTURES / "synthetic_corpus"
CASE = json.loads(
    (FIXTURES / "synthetic_cases.json").read_text(encoding="utf-8"))["cases"][0]
EXPECTED_KEYS = {"case", "financial_series_point_in_time", "filing_chronology"}
FORBIDDEN = {"variant", "perturb", "dateshift", "anonym", "scoring_side"}


@pytest.fixture(autouse=True)
def synthetic_data_dir(monkeypatch):
    monkeypatch.setattr(bp, "DATA_DIR", CORPUS)


def _render(payload, keys):
    visible = {key: payload[key] for key in keys}
    return visible, json.dumps(visible, ensure_ascii=False)


@pytest.mark.parametrize("perturb", [False, True])
@pytest.mark.parametrize("send_path", [runner, runner_api, probe_runner])
def test_all_send_paths_expose_only_allowlisted_keys(send_path, perturb):
    payload = bp.build_payload(CASE, perturb=perturb)
    visible, sent = _render(payload, send_path.MODEL_VISIBLE_KEYS)

    assert set(visible) == EXPECTED_KEYS
    assert not [word for word in FORBIDDEN if word in sent.lower()]
    assert payload["_variant"] == ("perturbed" if perturb else "original")
    assert "_k_internal" in payload


@pytest.mark.parametrize("perturb", [False, True])
def test_probe_dateshift_shape_cannot_add_run_markers_to_sent_json(perturb):
    payload = date_shift.shift_payload(bp.build_payload(CASE, perturb=perturb))
    assert payload["variant"] == "perturbed_v2_dateshift"

    visible, sent = _render(payload, probe_runner.MODEL_VISIBLE_KEYS)
    assert set(visible) == EXPECTED_KEYS
    assert not [word for word in FORBIDDEN if word in sent.lower()]
    assert payload["_variant"] == ("perturbed" if perturb else "original")
    assert "_k_internal" in payload


def test_model_visible_top_level_keys_are_identical_across_arms():
    original, _ = _render(bp.build_payload(CASE, perturb=False),
                          runner.MODEL_VISIBLE_KEYS)
    perturbed, _ = _render(bp.build_payload(CASE, perturb=True),
                           runner.MODEL_VISIBLE_KEYS)
    assert set(original) == set(perturbed) == EXPECTED_KEYS


@pytest.mark.parametrize("perturb", [False, True])
def test_runner_send_site_drops_adversarial_nonunderscore_marker(
        monkeypatch, tmp_path, perturb):
    payload = bp.build_payload(CASE, perturb=perturb)
    payload["variant"] = "perturbed" if perturb else "original"
    captured = []

    def fake_call_model(model, system, user_payload, schema, **kwargs):
        captured.append(user_payload)
        return SimpleNamespace(ok=False, structured=None, fail_reason="test-stop",
                               served_models=[])

    monkeypatch.setattr(runner.bp, "build_payload",
                        lambda *args, **kwargs: copy.deepcopy(payload))
    monkeypatch.setattr(runner.cli_client, "call_model", fake_call_model)
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    result = runner.run_case(CASE, perturb, tmp_path / "out", log_dir)

    assert result["status"] == "FAIL (test-stop)"
    sent = json.loads(captured[0])
    assert set(sent) == EXPECTED_KEYS
    assert not [word for word in FORBIDDEN if word in captured[0].lower()]


def test_probe_send_site_drops_adversarial_nonunderscore_marker(monkeypatch, tmp_path):
    payload = bp.build_payload(CASE, perturb=True)
    payload["variant"] = "perturbed_v2_dateshift"
    captured = []

    def fake_call_model(model, system, user, schema, **kwargs):
        captured.append(user)
        return SimpleNamespace(ok=True,
                               structured={"company_guess": "unknown", "confidence": "low"},
                               fail_reason=None)

    monkeypatch.setattr(probe_runner.bp, "build_payload",
                        lambda *args, **kwargs: copy.deepcopy(payload))
    monkeypatch.setattr(probe_runner.cli_client, "call_model", fake_call_model)
    probe_runner.probe_case("recognition", CASE, tmp_path / "out", tmp_path / "logs")

    sent = json.loads(captured[0])
    assert set(sent) == EXPECTED_KEYS
    assert not [word for word in FORBIDDEN if word in captured[0].lower()]
