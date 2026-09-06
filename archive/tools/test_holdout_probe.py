"""holdout_probe transcript overwrite guards (model-free)."""
import json

import holdout_probe as hp


def test_existing_valid_transcript_skips_model_and_is_not_overwritten(tmp_path, monkeypatch):
    monkeypatch.setattr(hp, "REPO", tmp_path)
    record = {
        "ticker": "TEST", "company": "Test Co", "kind": "holdout-control",
        "context": "context", "knows_event": False, "event_description": "none",
        "approx_date": None, "confidence": "none", "served_models": [hp.PIN_MODEL],
        "pin_ok": True, "session_id": "session", "cost_ref_usd": 0,
    }
    out = tmp_path / "TEST.json"
    original = json.dumps(record) + "\n"
    out.write_text(original, encoding="utf-8")
    monkeypatch.setattr(hp, "call_model", lambda **kwargs: (_ for _ in ()).throw(
        AssertionError("model must not be called")))

    result = hp.probe("TEST", "Test Co", "holdout-control", "context", tmp_path)

    assert result == record
    assert out.read_text(encoding="utf-8") == original
