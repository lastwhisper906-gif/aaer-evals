"""The bundle, and the manifest that has to account for every line of it.

The load-bearing test is the two-way set equality: every `[id]` in a bundle file
is in the manifest, and every id in the manifest is in a file. It runs over all
twelve companies. Everything else here is about what the bundle does with what
it does not have — a missing 8-K, a missing note history, no prior run — which
in this fixture set is most of the interesting cases.

Nothing writes to `runs/`. Every test names its own output directory, and one
test asserts the default root was not created as a side effect of importing or
running anything.
"""

from __future__ import annotations

import functools
import json
from pathlib import Path

import pytest

from src import assemble_bundle, cutoff_guard
from src.fetch_fixtures import TICKERS

REPO_ROOT = Path(__file__).resolve().parent.parent


@functools.lru_cache(maxsize=None)
def built(ticker: str, form: str = "10-Q") -> dict:
    return assemble_bundle.build(ticker, form)


def ids_in_files(texts: dict) -> set[str]:
    found: set[str] = set()
    for name in assemble_bundle.PARAGRAPH_FILES:
        found |= set(assemble_bundle.paragraph_ids(texts[name]))
    return found


# --- (b) the command writes the eight files ---------------------------------

def test_the_command_writes_all_eight_files(tmp_path):
    out = tmp_path / "bundle"
    assert assemble_bundle.main(
        ["--ticker", "aapl", "--form", "10-K", "--out", str(out)]) == 0
    assert sorted(path.name for path in out.iterdir()) == sorted(assemble_bundle.FILES)
    for name in assemble_bundle.FILES:
        assert (out / name).read_text(encoding="utf-8").strip()
    assert len(assemble_bundle.FILES) == 8


def test_the_command_refuses_a_form_that_does_not_trigger_a_run(tmp_path):
    assert assemble_bundle.main(
        ["--ticker", "AAPL", "--form", "10-K", "--cutoff", "2020-01-01",
         "--out", str(tmp_path / "b")]) == 2
    assert not (tmp_path / "b").exists()


def test_the_written_files_are_the_built_texts(tmp_path):
    out = tmp_path / "bundle"
    bundle = assemble_bundle.build("QCOM", "10-Q")
    assemble_bundle.write(bundle, out)
    for name, text in bundle["texts"].items():
        assert (out / name).read_text(encoding="utf-8") == text
    manifest = json.loads((out / "input_manifest.json").read_text(encoding="utf-8"))
    for name, record in manifest["files"].items():
        assert record["bytes"] == len(bundle["texts"][name].encode("utf-8"))


# --- (c) the manifest accounts for every paragraph --------------------------

@pytest.mark.parametrize("ticker", TICKERS)
def test_every_id_in_a_file_is_in_the_manifest_and_the_other_way(ticker):
    bundle = built(ticker)
    listed = {entry["id"] for entry in bundle["manifest"]["paragraphs"]}
    assert len(listed) == len(bundle["manifest"]["paragraphs"]), "an id is repeated"
    assert ids_in_files(bundle["texts"]) == listed


def test_the_same_holds_for_a_ten_k_bundle():
    bundle = built("AAPL", "10-K")
    listed = {entry["id"] for entry in bundle["manifest"]["paragraphs"]}
    assert ids_in_files(bundle["texts"]) == listed
    assert listed


@pytest.mark.parametrize("ticker", TICKERS)
def test_an_excluded_paragraph_is_not_in_any_file(ticker):
    bundle = built(ticker)
    excluded = {entry["id"] for entry in bundle["manifest"]["exclusions"]}
    assert not excluded & ids_in_files(bundle["texts"])
    assert len(excluded) == len(bundle["manifest"]["exclusions"])


# --- (d) every exclusion carries a reason -----------------------------------

@pytest.mark.parametrize("ticker", TICKERS)
def test_every_exclusion_carries_a_non_empty_reason(ticker):
    manifest = built(ticker)["manifest"]
    assert manifest["exclusions"], f"{ticker}: nothing was excluded at all"
    for entry in manifest["exclusions"]:
        assert entry["reason"].strip(), entry
        assert entry["source"].strip(), entry
        assert entry["id"]


def test_the_empty_paragraphs_are_counted_rather_than_listed_one_by_one():
    """Esterline's 10-Q separates its blocks with thousands of zero-width
    spaces. They are still excluded and still explained; they are just not
    three quarters of a megabyte of manifest."""
    manifest = built("ESE")["manifest"]
    grouped = [entry for entry in manifest["exclusions"]
               if "empty_excluded" in entry["id"]]
    assert grouped
    assert all("with no text to record" in entry["reason"] for entry in grouped)
    assert not [entry for entry in manifest["exclusions"] if entry["reason"] == "empty"]
    assert len(manifest["exclusions"]) < 200


def test_grouping_keeps_every_drop_that_has_text():
    exclusions = [{"id": "a:1", "source": "notes", "reason": "empty", "text": ""},
                  {"id": "a:2", "source": "notes", "reason": "empty", "text": ""},
                  {"id": "a:3", "source": "notes", "reason": "page_number", "text": "42"}]
    grouped = assemble_bundle.group_empty(exclusions, "acc")
    assert [entry["id"] for entry in grouped] == ["a:3", "acc:empty_excluded:1"]
    assert "2 of them" in grouped[1]["reason"]


# --- (e) the two placeholders -----------------------------------------------

@pytest.mark.parametrize("ticker", TICKERS)
def test_the_rules_version_and_served_model_are_null_with_a_note(ticker):
    manifest = built(ticker)["manifest"]
    assert manifest["rules_version"] is None
    assert manifest["served_model"] is None
    assert "rules/v0.1" in manifest["rules_version_comment"]
    assert "pinned-model runner" in manifest["served_model_comment"]


# --- (f) nothing writes runs/ ------------------------------------------------

def test_the_default_root_is_named_but_never_created(tmp_path):
    """Trap 1. The default is `runs/`, the loop cannot write it, and building a
    bundle somewhere else must not bring it into being."""
    assert assemble_bundle.DEFAULT_ROOT == Path("runs")
    assemble_bundle.assemble("ESE", "10-Q", tmp_path / "somewhere")
    assert not (REPO_ROOT / "runs").exists()
    assert not (Path.cwd() / "runs").exists()
    assert assemble_bundle.default_out("ESE", "0001-2") == \
        Path("runs") / "ESE" / "0001-2"


# --- the cutoff --------------------------------------------------------------

@pytest.mark.parametrize("ticker", TICKERS)
def test_no_document_in_the_manifest_was_filed_after_the_cutoff(ticker):
    manifest = built(ticker)["manifest"]
    assert manifest["documents"]
    for row in manifest["documents"]:
        assert row["filing_date"] <= manifest["cutoff"], row
    assert manifest["cutoff"] == manifest["filing_date"]


def test_a_ten_k_bundle_leaves_out_the_ten_q_that_came_after_it():
    """Apple's 10-K was filed 2025-10-31 and its 10-Q 2026-07-31. The cutoff is
    the triggering report's own date, so the later quarter is not in the bundle
    — and the note change history, which needs two 10-Qs, is recorded as absent
    rather than quietly built out of documents the reader would not have."""
    manifest = built("AAPL", "10-K")["manifest"]
    assert manifest["cutoff"] == "2025-10-31"
    assert not [row for row in manifest["documents"] if row["form"] == "10-Q"]
    reasons = [entry["reason"] for entry in manifest["exclusions"]
               if entry["id"].endswith(":file:input_notes_history.md")]
    assert len(reasons) == 1 and "needs two 10-Qs" in reasons[0]


def test_a_bundle_without_an_eight_k_says_so_instead_of_shipping_an_empty_file():
    """Seagate's 8-K was filed after the 10-Q this bundle is for."""
    bundle = built("STX")
    reasons = [entry["reason"] for entry in bundle["manifest"]["exclusions"]
               if entry["id"].endswith(":file:input_8k.md")]
    assert len(reasons) == 1 and "after the 10-Q this bundle is for" in reasons[0]
    assert "no 8-K at or before" in bundle["texts"]["input_8k.md"]
    assert bundle["manifest"]["counts"]["eight_k"] == 0


def test_a_bundle_with_an_eight_k_carries_its_paragraphs():
    bundle = built("AAPL")
    assert bundle["manifest"]["counts"]["eight_k"] > 0
    assert not [entry for entry in bundle["manifest"]["exclusions"]
                if entry["id"].endswith(":file:input_8k.md")]


# --- prior predictions -------------------------------------------------------

def test_no_prior_run_is_a_sentence_not_an_empty_file(tmp_path):
    text, entries = assemble_bundle.prior_predictions("AAPL", tmp_path)
    assert entries == []
    assert "None on record" in text
    assert text.startswith("# AAPL prior predictions")


def test_a_prior_runs_flags_come_through_without_their_probabilities(tmp_path):
    run = tmp_path / "AAPL" / "0000320193-25-000079"
    run.mkdir(parents=True)
    (run / "prediction_accounting.json").write_text(json.dumps({"flags": [
        {"flag": "receivables grew faster than revenue", "probability": 0.62,
         "outcome": "did not materialize"},
        {"flag": "auditor changed", "score": 3, "outcome": "materialized"}]}),
        encoding="utf-8")
    text, entries = assemble_bundle.prior_predictions("AAPL", tmp_path)
    assert len(entries) == 2
    assert "receivables grew faster than revenue" in text
    assert "did not materialize" in text
    assert "0.62" not in text and "probability" not in text
    assert '"score"' not in text
    for entry in entries:
        assert entry["id"] in assemble_bundle.paragraph_ids(text)


def test_a_prior_run_that_is_not_json_is_refused(tmp_path):
    run = tmp_path / "AAPL" / "acc"
    run.mkdir(parents=True)
    (run / "prediction_accounting.json").write_text("not json", encoding="utf-8")
    with pytest.raises(assemble_bundle.BundleError):
        assemble_bundle.prior_predictions("AAPL", tmp_path)


# --- determinism and shape ---------------------------------------------------

def test_two_builds_of_the_same_bundle_are_identical():
    first = assemble_bundle.build("TTMI", "10-Q")["texts"]
    second = assemble_bundle.build("TTMI", "10-Q")["texts"]
    assert first == second


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_counts_are_the_manifests_own_arithmetic(ticker):
    manifest = built(ticker)["manifest"]
    counts = manifest["counts"]
    assert counts["paragraphs"] == len(manifest["paragraphs"])
    assert counts["exclusions"] == len(manifest["exclusions"])
    for key, name in (("notes", "input_notes.md"), ("mdna", "input_mdna.md"),
                      ("note_history", "input_notes_history.md"),
                      ("eight_k", "input_8k.md")):
        assert counts[key] == sum(1 for entry in manifest["paragraphs"]
                                  if entry["file"] == name)


def test_a_paragraph_id_line_is_only_an_id_line():
    assert assemble_bundle.paragraph_ids("[a:notes:1]\ntext\n[b:mdna:2]\n") == \
        ["a:notes:1", "b:mdna:2"]
    assert assemble_bundle.paragraph_ids("[see note 3]\n[1]\ntext") == []


def test_the_submissions_index_is_not_one_of_the_bundles_documents():
    """It is EDGAR's catalogue of filings, not a filing, and it carries the
    fixture set's as-of date. Letting it into the manifest would make every
    bundle look like a cutoff violation."""
    manifest = built("AAPL")["manifest"]
    assert not [row for row in manifest["documents"] if row["form"] == "submissions"]


def test_the_index_loader_refuses_anything_that_is_not_the_index():
    row = cutoff_guard.one_document("AAPL", "10-K", "primary_html")
    with pytest.raises(cutoff_guard.CutoffGuardError):
        cutoff_guard.load_index(row["full_path"])
    index = cutoff_guard.one_document("AAPL", "submissions", "submissions_index")
    assert json.loads(cutoff_guard.load_index(index["full_path"]))["filings"]
