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


def test_with_nothing_on_record_the_batch_is_one_and_the_text_says_so():
    out = fable_batch.size(1000, {})
    assert out["batch"] == 1 and out["filings_on_record"] == 0
    assert "the batch is one filing" in out["calculation"]
    assert fable_batch.size(1000, {"A/1": 400})["batch"] == 2


def test_only_a_published_filing_is_on_record(tmp_path):
    """A run the limit stopped, or an analyst failed, is not a published filing:
    its tokens are a part of a filing's and would pull the median down."""
    _manifest(tmp_path / "A" / "1", {"a": FABLE})                            # no failure key
    (tmp_path / "B" / "1").mkdir(parents=True)
    (tmp_path / "B" / "1" / "input_manifest.json").write_text(json.dumps(
        {"agents": {"a": dict(FABLE, output_tokens=240)}, "analysis_failure": None}))
    (tmp_path / "C" / "1").mkdir(parents=True)
    (tmp_path / "C" / "1" / "input_manifest.json").write_text(json.dumps(
        {"agents": {"a": FABLE}, "analysis_failure": "the limit was reached at a: ...",
         "fable_limit_reached": ["a"]}))
    (tmp_path / "D" / "1").mkdir(parents=True)
    (tmp_path / "D" / "1" / "input_manifest.json").write_text(json.dumps(
        {"agents": {"a": FABLE}, "analysis_failure": "did not write: a"}))
    assert fable_batch.on_record(tmp_path) == {"A/1": 100, "B/1": 300}
    assert fable_batch.published({"analysis_failure": None}) is True
    assert fable_batch.published({"fable_limit_reached": ["a"]}) is False
