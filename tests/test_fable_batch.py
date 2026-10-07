"""The batch size, from hand-written records."""

import json

from src import fable_batch, run_analysis


def _manifest(path, agents, fallback=None):
    """A finished run's manifest: `finish` wrote it, so it carries the one key
    only `finish` writes; `fallback` plants the `model_fallback` row of a run
    that fell back to Opus at the limit."""
    path.mkdir(parents=True)
    target = path / "input_manifest.json"
    manifest = {"agents": agents, run_analysis.FINISH_MARKER: "2026-10-07T00:00:00Z"}
    if fallback:
        manifest["model_fallback"] = {"from": "fable", "to": "opus",
                                      "at": "2026-10-07T01:00:00Z", "first_agent": "a"}
    target.write_text(json.dumps(manifest))
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


# --- a run that fell back to Opus at the limit (the owner's decision of 2026-10-07) ---------

# The financial analyst's record after the limit: a Fable attempt that answered
# the limit (100 tokens, as FABLE above) and the Opus attempt that wrote (2,000,
# as OPUS above), the record's own fields the sum, 2,100, and the fallback named.
FALLEN_BACK = {"model_requested": "fable", "model_served": "claude-opus-5-5",
               "fallback_from": "fable", "fallback_reason": "fable_limit_reached",
               "input_tokens": 1010, "cache_creation_input_tokens": 20,
               "cache_read_input_tokens": 30, "output_tokens": 1040,
               "attempts": [dict(FABLE, attempt=1, model_requested="fable", outcome="limit"),
                            dict(OPUS, attempt=2, model_requested="opus", outcome="written")]}


def test_a_fallback_agent_counts_its_fable_served_attempts_only():
    """The Opus attempt's 2,000 tokens are on record and are not Fable tokens:
    the agent costs the limit attempt's 100. An attempt with no served model on
    record is read by what it asked for, and one saying neither by the record's
    own request."""
    assert fable_batch.agent_tokens(FALLEN_BACK) == 100
    assert fable_batch.fable_tokens({"agents": {"a": FALLEN_BACK, "b": OPUS, "c": FABLE}}) == 200
    unserved = {"model_requested": "fable",
                "attempts": [{"attempt": 1, "model_requested": "fable", "input_tokens": 7,
                              "outcome": "limit"},
                             {"attempt": 2, "model_requested": "opus", "input_tokens": 9,
                              "outcome": "failed"},
                             {"attempt": 3, "input_tokens": 11, "outcome": "failed"}]}
    assert fable_batch.agent_tokens(unserved) == 7 + 11
    assert fable_batch.fable_served({"model_served": "claude-fable-5-1"}, {}) is True
    assert fable_batch.fable_served({"model_served": "claude-opus-5-5"},
                                    {"model_requested": "fable"}) is False
    assert fable_batch.fable_served({}, {"model_requested": "opus"}) is False


def test_a_filing_that_fell_back_is_left_out_of_the_median_and_named(tmp_path):
    """The default in force (docs/needs_judgment.md): the median is of the
    filings Fable served whole. Three published filings: A/1 on Fable throughout,
    the retried analyst's 300; B/1, which fell back, 100 (its limit attempt; the
    Opus attempt's 2,000 is not Fable); C/1, served by Opus alone with the row --
    a run that carried the batch's fallback from its first call -- no Fable token,
    so not on record. B/1 and C/1 are left out and named: the median is A/1's
    300, and 1,000 available is 1,000 // 300 = 3 filings. Counted in, B/1 would
    have made the median (300 + 100) / 2 = 200 and the batch 1,000 // 200 = 5,
    which is the bias this rule refuses."""
    _manifest(tmp_path / "A" / "1", {"a": RETRIED})
    _manifest(tmp_path / "B" / "1", {"a": FALLEN_BACK}, fallback=True)
    _manifest(tmp_path / "C" / "1", {"r": OPUS}, fallback=True)
    record = fable_batch.on_record(tmp_path)
    assert record == {"A/1": 300, "B/1": 100}
    assert fable_batch.fell_back(tmp_path) == ["B/1", "C/1"]
    sized = fable_batch.size(1000, record, fable_batch.fell_back(tmp_path))
    assert sized["median_per_filing"] == 300 and sized["batch"] == 3
    assert sized["filings_on_record"] == 1
    assert sized["fell_back"] == 2 and sized["fell_back_filings"] == ["B/1", "C/1"]
    assert sized["calculation"] == (
        "1,000 Fable tokens available ÷ median 300 per filing over 1 filing(s) on record "
        "= 3 filing(s); 2 filing(s) fell back to opus and are left out of the median "
        "(B/1, C/1)")
    # the other side: nothing named as fallen back, both filings count, and the
    # words end at the count
    plain = fable_batch.size(1000, record)
    assert plain["median_per_filing"] == 200 and plain["batch"] == 5
    assert plain["fell_back"] == 0 and plain["fell_back_filings"] == []
    assert plain["calculation"].endswith("= 5 filing(s)")
    # every filing on record fell back: one filing, as with an empty record,
    # and the words name what was left out
    every = fable_batch.size(1000, {"B/1": 100}, ["B/1", "C/1"])
    assert every["batch"] == 1 and every["median_per_filing"] is None
    assert every["filings_on_record"] == 0
    assert every["fell_back"] == 2 and every["fell_back_filings"] == ["B/1", "C/1"]
    assert "the batch is one filing" in every["calculation"]
    assert every["calculation"].endswith(
        "; 2 filing(s) fell back to opus and are left out of the median (B/1, C/1)")
    empty = fable_batch.size(1000, {})
    assert empty["fell_back"] == 0 and empty["fell_back_filings"] == []
    assert empty["calculation"].endswith("sizes the next night")
    # a stopped run with the row is not published, so it is not a fallback on record
    (tmp_path / "D" / "1").mkdir(parents=True)
    (tmp_path / "D" / "1" / "input_manifest.json").write_text(json.dumps(
        {"agents": {"a": FALLEN_BACK}, "model_fallback": {"to": "opus"}, "stopped_on": "x"}))
    assert fable_batch.fell_back(tmp_path) == ["B/1", "C/1"]
