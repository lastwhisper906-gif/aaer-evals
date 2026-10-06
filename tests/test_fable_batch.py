"""The batch size, from hand-written records."""

import json

from src import fable_batch


def _manifest(path, agents):
    path.mkdir(parents=True)
    (path / "input_manifest.json").write_text(json.dumps({"agents": agents}))


FABLE = {"model_served": "claude-fable-5-1", "input_tokens": 10, "cache_creation_input_tokens": 20,
         "cache_read_input_tokens": 30, "output_tokens": 40}                # 100
OPUS = {"model_served": "claude-opus-5-5", "input_tokens": 1000, "output_tokens": 1000}


def test_fable_tokens_count_every_fable_agent_and_no_opus_one():
    manifest = {"agents": {"a": FABLE, "b": dict(FABLE, output_tokens=240), "r": OPUS}}
    assert fable_batch.fable_tokens(manifest) == 100 + 300


def test_the_batch_is_available_over_the_median_on_record(tmp_path):
    """Two filings cost 100 and 300: median 200. 1,000 available: five filings."""
    _manifest(tmp_path / "A" / "1", {"a": FABLE})
    _manifest(tmp_path / "B" / "1", {"a": dict(FABLE, output_tokens=240)})
    _manifest(tmp_path / "C" / "1", {"r": OPUS})          # no Fable agent: not on record
    record = fable_batch.on_record(tmp_path)
    assert record == {"A/1": 100, "B/1": 300}
    out = fable_batch.size(1000, record)
    assert out["batch"] == 5 and out["median_per_filing"] == 200
    assert "÷ median 200" in out["calculation"]


def test_with_nothing_on_record_the_batch_is_stated_not_guessed():
    out = fable_batch.size(1000, {})
    assert out["batch"] == 0 and "no filing on record" in out["calculation"]
