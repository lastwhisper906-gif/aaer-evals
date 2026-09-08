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

from src import (assemble_bundle, clean_text, cutoff_guard, diff_periods,
                 extract_notes, split_sections)
from src.fetch_fixtures import TICKERS
from tests import independent_text

REPO_ROOT = Path(__file__).resolve().parent.parent
BAR = chr(124)


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


# --- the notes arrive as a reader can quote them -----------------------------
#
# `docs/INPUT_SPEC.md` asks for tables as pipe-delimited rows and the notes file
# had none: `td`, `th` and `tr` are block tags, so every cell arrived as its own
# paragraph and NVIDIA's contingencies note read `Remainder of 2027`, `Total`,
# `(In billions)`, `88`, `6`, `$`. No figure in it could be quoted with the row
# and the column it belongs to.

def notes_paragraphs(ticker: str, form: str) -> list[str]:
    """The `[id]` blocks of `input_notes.md`, as the file itself defines them."""
    text = built(ticker, form)["texts"]["input_notes.md"]
    return [body for _, body in assemble_bundle.paragraph_blocks(text) if body]


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", ("10-K", "10-Q"))
def test_the_notes_file_holds_tables_as_rows(ticker, form):
    text = built(ticker, form)["texts"]["input_notes.md"]
    rows = [line for line in text.split("\n") if line.startswith(BAR + " ")]
    assert rows, f"{ticker} {form}: input_notes.md has no rendered table row"


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", ("10-K", "10-Q"))
def test_most_of_a_note_paragraph_is_more_than_three_words(ticker, form):
    """79% to 88% of note paragraphs used to be three words or fewer, because
    they were single table cells. A quarter is the line the dispatch drew."""
    paragraphs = notes_paragraphs(ticker, form)
    short = sum(1 for text in paragraphs if len(text.split()) <= 3)
    share = short / max(1, len(paragraphs))
    assert share < 0.25, f"{ticker} {form}: {share:.0%} of {len(paragraphs)}"


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", ("10-K", "10-Q"))
def test_no_note_is_carried_into_the_file_twice(ticker, form):
    """Apple emitted the paragraph `$` 290 times and Cisco 1,231, because a
    filer tags a note, then each policy in it, then each table in that. A quote
    that resolves to a hundred ids is not a quote anyone can check."""
    paragraphs = notes_paragraphs(ticker, form)
    repeated = {text for text in paragraphs if paragraphs.count(text) > 1}
    assert not repeated, f"{ticker} {form}: {sorted(repeated)[:1]}"


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", ("10-K", "10-Q"))
def test_every_rendered_cell_is_the_filings_own_text(ticker, form):
    """A row is a rendering; a cell is the filing. The guarantee is at the cell,
    and it is asserted there against the independent stripper."""
    sections = extract_notes.extract(ticker, form)["sections"]
    sources = [independent_text.Source(section["html"]) for section in sections]
    misses = []
    for text in notes_paragraphs(ticker, form):
        if diff_periods.is_collapsed_line(text):
            continue            # the diff layer's placeholder, not the filing
        for piece in independent_text.quotable(text):
            if not any(source.contains(piece) for source in sources):
                misses.append(piece)
    assert not misses, f"{ticker} {form}: {misses[:3]}"


def test_a_note_inside_another_note_is_carried_once():
    """Apple's 10-Q tags 26 notes; twelve of them are wholly inside another."""
    stream = diff_periods.notes("AAPL", "10-Q", "xbrl_instance",
                                cutoff=None, fixtures_root=cutoff_guard.FIXTURES)
    assert stream["sections"] == 26
    assert stream["notes_carried"] < stream["sections"]
    assert any(repeat["kind"] == "note" for repeat in stream["repeats"])
    for repeat in stream["repeats"]:
        assert repeat["kind"] in ("note", "paragraph")
        if repeat["kind"] == "paragraph":
            assert repeat["already_at"].startswith("0000320193")


def test_a_table_is_one_paragraph_holding_all_of_its_rows():
    """Not one paragraph per row: 2,321 rows in the fixture set are identical to
    a row of another table, and one id per row makes those ids ambiguous."""
    html = ("<p>Before</p><table><tr><td>Year</td><td>Amount</td></tr>"
            "<tr><td>2026</td><td>1,000</td></tr></table><p>After</p>")
    stream = clean_text.clean_stream(html)["paragraphs"]
    assert stream[0] == "Before"
    assert stream[2] == "After"
    assert stream[1].split("\n") == [BAR + " Year " + BAR + " Amount " + BAR,
                                     BAR + " 2026 " + BAR + " 1,000 " + BAR]


# --- one id per paragraph, minted once ---------------------------------------

@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", ("10-K", "10-Q"))
def test_no_id_in_the_bundle_names_two_different_paragraphs(ticker, form):
    """Across the eight files of one bundle, an id resolves to one text."""
    texts = built(ticker, form)["texts"]
    seen = {}
    for name, text in texts.items():
        if not name.endswith(".md"):
            continue
        for identifier, body in assemble_bundle.paragraph_blocks(text):
            if identifier in seen:
                assert seen[identifier] == body, f"{ticker} {form}: {identifier}"
            seen[identifier] = body


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", ("10-K", "10-Q"))
def test_the_section_cli_mints_the_ids_the_bundle_publishes(ticker, form):
    """`split_sections` and the bundle name the same paragraph by the same id.
    They were two producers over two lists: 333 of AAPL's 365 `…:mdna:n` ids
    named one paragraph in the CLI's file and a different one in the bundle."""
    found = split_sections.extract(ticker, form, "mdna")
    if form == "10-Q":
        entries = diff_periods.extract(ticker)["mdna"]
    else:
        _, entries, _ = assemble_bundle.note_stream(
            ticker, form, cutoff=None, fixtures_root=cutoff_guard.FIXTURES)
    assert list(zip(found["paragraph_ids"], found["carried"])) == \
        [(entry["id"], entry["text"]) for entry in entries]


def test_the_section_cli_refuses_to_write_a_bundle_filename(tmp_path, capsys):
    """It mints the bundle's ids over text the diff layer has not seen, so a
    file of that name from here would hold different text under the same ids."""
    out = tmp_path / "input_mdna.md"
    assert split_sections.main(["--ticker", "AAPL", "--form", "10-Q",
                                "--out", str(out)]) != 0
    assert not out.exists()
    assert "bundle filename" in capsys.readouterr().err
    other = tmp_path / "aapl-mdna.md"
    assert split_sections.main(["--ticker", "AAPL", "--form", "10-Q",
                                "--out", str(other)]) == 0
    assert other.exists()


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", ("10-K", "10-Q"))
def test_the_note_history_count_is_its_entries_plus_its_changed_ones(ticker, form):
    """The recorded count is not free-floating: a changed entry puts two
    paragraphs in the file, so the count is entries + changed, and both halves
    are recorded separately in the same expected.json."""
    manifest = built(ticker, form)["manifest"]
    listed = manifest["counts"]["note_history"]
    record = json.loads((REPO_ROOT / "tests" / "fixtures" / ticker /
                         "expected.json").read_text())
    if "note_history" not in record or form not in record["note_history"]:
        assert listed == 0 or form == "10-K"
        return
    block = record["note_history"][form]
    assert listed == sum(block[kind] for kind in ("added", "removed", "changed")) \
        + block["changed"]
