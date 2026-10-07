"""The batch size, from hand-written records."""

import json

from src import fable_batch, run_analysis


def _manifest(path, agents):
    """A finished run's manifest: `finish` wrote it, so it carries the one key
    only `finish` writes."""
    path.mkdir(parents=True)
    target = path / "input_manifest.json"
    target.write_text(json.dumps({"agents": agents,
                                  run_analysis.FINISH_MARKER: "2026-10-07T00:00:00Z"}))
    return target


FABLE = {"model_served": "claude-fable-5-1", "input_tokens": 10, "cache_creation_input_tokens": 20,
         "cache_read_input_tokens": 30, "output_tokens": 40}                # 100
OPUS = {"model_served": "claude-opus-5-5", "input_tokens": 1000, "output_tokens": 1000}


# A retried analyst: two failed attempts and the pass, 10+20+30+40 each on the
# first two and the pass's own 100, so 300 in all; the record's own fields are
# written stale here, at the pass's 100, to show the list is what is read.
RETRIED = {"model_served": "claude-fable-5-1", "input_tokens": 10,
           "cache_creation_input_tokens": 20, "cache_read_input_tokens": 30,
           "output_tokens": 40,
           "attempts": [dict(FABLE, attempt=1, outcome="failed"),
                        dict(FABLE, attempt=2, outcome="failed"),
                        dict(FABLE, attempt=3, outcome="written")]}


def test_a_retried_agent_costs_every_attempt_and_an_old_record_its_own_fields():
    assert fable_batch.agent_tokens(RETRIED) == 300
    assert fable_batch.agent_tokens(FABLE) == 100                  # no attempts list
    assert fable_batch.agent_tokens(dict(FABLE, attempts=[])) == 100
    assert fable_batch.fable_tokens({"agents": {"a": RETRIED, "b": FABLE, "c": OPUS}}) == 400


def test_the_batch_is_sized_from_the_summed_attempts(tmp_path):
    _manifest(tmp_path / "AAA" / "1", {"accounting-analyst": RETRIED})       # 300
    _manifest(tmp_path / "BBB" / "1", {"accounting-analyst": FABLE})         # 100
    record = fable_batch.on_record(tmp_path)
    assert record == {"AAA/1": 300, "BBB/1": 100}
    sized = fable_batch.size(1000, record)
    assert sized["median_per_filing"] == 200 and sized["batch"] == 5


def test_a_run_finish_did_not_write_is_not_on_record(tmp_path):
    path = _manifest(tmp_path / "AAA" / "1", {"accounting-analyst": FABLE})
    manifest = json.loads(path.read_text(encoding="utf-8"))
    del manifest[run_analysis.FINISH_MARKER]
    path.write_text(json.dumps(manifest), encoding="utf-8")
    assert fable_batch.on_record(tmp_path) == {}


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
        {"agents": {"a": dict(FABLE, output_tokens=240)}, "analysis_failure": None,
         run_analysis.FINISH_MARKER: "2026-10-07T00:00:00Z"}))
    (tmp_path / "C" / "1").mkdir(parents=True)
    (tmp_path / "C" / "1" / "input_manifest.json").write_text(json.dumps(
        {"agents": {"a": FABLE}, "analysis_failure": "the limit was reached at a: ...",
         "fable_limit_reached": ["a"]}))
    (tmp_path / "D" / "1").mkdir(parents=True)
    (tmp_path / "D" / "1" / "input_manifest.json").write_text(json.dumps(
        {"agents": {"a": FABLE}, "analysis_failure": "did not write: a"}))
    assert fable_batch.on_record(tmp_path) == {"A/1": 100, "B/1": 300}
    finished = {run_analysis.FINISH_MARKER: "2026-10-07T00:00:00Z"}
    assert fable_batch.published({"analysis_failure": None, **finished}) is True
    assert fable_batch.published({"fable_limit_reached": ["a"], **finished}) is False
    # a run finish did not write -- an error stopped it before the record was
    # finished -- is not a published filing either, whatever else it says
    assert fable_batch.published({"analysis_failure": None}) is False
