"""Regression tests for the exact JSON exposed to the evaluatee."""
import json
from pathlib import Path

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
