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
import re
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


# --- (b) the command writes every file --------------------------------------

def test_the_command_writes_every_file(tmp_path):
    out = tmp_path / "bundle"
    assert assemble_bundle.main(
        ["--ticker", "aapl", "--form", "10-K", "--out", str(out)]) == 0
    assert sorted(path.name for path in out.iterdir()) == sorted(assemble_bundle.FILES)
    for name in assemble_bundle.FILES:
        assert (out / name).read_text(encoding="utf-8").strip()
    # Nine, not the eight `docs/INPUT_SPEC.md` §5 lists: §1 requires the
    # auditor's report, Item 9A and Item 4, and §5 gives them no file. The
    # conflict is inside the spec and the spec is not ours to edit.
    assert len(assemble_bundle.FILES) == 9
    assert "input_controls.md" in assemble_bundle.FILES


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
    """The submissions index is the one row with no filing date — it is a
    catalogue of filings and not a filing, and the exemption is asserted
    separately rather than skipped here."""
    manifest = built(ticker)["manifest"]
    assert manifest["documents"]
    for row in manifest["documents"]:
        if row["role"] == assemble_bundle.INDEX_ROLE:
            assert row["filing_date"] is None, row
            continue
        assert row["filing_date"] <= manifest["cutoff"], row
    assert manifest["cutoff"] == manifest["filing_date"]
    for row in manifest["on_record_at_cutoff"]:
        assert row["filing_date"] <= manifest["cutoff"], row


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
    """Seagate's 8-K was filed after the 10-Q this bundle is for.

    The sentence says what is missing and stops there. It used to go on to name
    the held 8-K's own filing date — a date after the cutoff, written into the
    text the predictor reads, in 15 of the 24 bundles.
    """
    bundle = built("STX")
    cutoff = bundle["manifest"]["cutoff"]
    reasons = [entry["reason"] for entry in bundle["manifest"]["exclusions"]
               if entry["id"].endswith(":file:input_8k.md")]
    assert len(reasons) == 1
    assert f"no 8-K filed at or before {cutoff} is on record" in reasons[0]
    assert f"no 8-K filed at or before {cutoff} is on record" in \
        bundle["texts"]["input_8k.md"]
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


def test_the_submissions_index_is_listed_because_the_bundle_reads_it():
    """It used to be left out, on the grounds that a catalogue is not a filing
    and its recorded date would make every bundle look like a cutoff violation.
    Both halves of that are true and neither is a reason to omit it: it supplies
    the entire item-code section of `input_8k.md`, so leaving it out made "no
    document was filed after the cutoff" a statement about a list built to
    exclude the one entry that would fail it. It is listed, with no filing date,
    with the record's own reason, and with the cutoff its rows were read
    through — and `extraction_checks` checks all three."""
    manifest = built("AAPL")["manifest"]
    rows = [row for row in manifest["documents"] if row["form"] == "submissions"]
    assert len(rows) == 1
    assert rows[0]["contributed_to"] == ["input_8k.md"]
    assert rows[0]["filing_date"] is None
    assert rows[0]["rows_used_through"] == manifest["cutoff"]
    # And the fixture manifest's own later date is nowhere in the bundle.
    assert "2026-09-01" not in json.dumps(manifest)


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


# --- the untagged sections reach the bundle ----------------------------------
#
# `docs/INPUT_SPEC.md` §1 requires the auditor's report with its critical audit
# matters, Item 9A and the 10-Q's Item 4. Every caller in `src/` used to ask for
# `mdna` and nothing else, so across all 24 bundles there were zero occurrences
# of `critical audit matter`, `disclosure controls and procedures`, `material
# weakness` or `report of independent registered public accounting firm` — and
# `docs/CHECKLIST.md` asks the model four questions that can only be answered by
# quoting them.

CHECKLIST_WORDS = ("critical audit matter", "disclosure controls and procedures",
                   "report of independent registered public accounting firm")


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", ("10-K", "10-Q"))
def test_the_controls_file_carries_the_sections_the_spec_requires(ticker, form):
    bundle = built(ticker, form)
    text = bundle["texts"]["input_controls.md"]
    for section in assemble_bundle.CONTROL_SECTIONS[form]:
        assert f":{section}:" in text, f"{ticker} {form}: no {section} paragraph id"
    listed = {entry["id"] for entry in bundle["manifest"]["paragraphs"]
              if entry["file"] == "input_controls.md"}
    assert listed == set(assemble_bundle.paragraph_ids(text))
    assert listed, f"{ticker} {form}: the file is in the manifest with no paragraphs"


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_ten_k_bundle_can_answer_the_checklists_audit_questions(ticker):
    """A quote has to exist in the inputs before it can be checked against them."""
    joined = "\n".join(text for name, text in built(ticker, "10-K")["texts"].items()
                        if name.endswith(".md")).lower()
    for phrase in CHECKLIST_WORDS:
        assert phrase in joined, f"{ticker}: no bundle text says {phrase!r}"


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", ("10-K", "10-Q"))
def test_every_control_paragraph_is_the_filings_own_text(ticker, form):
    row = cutoff_guard.one_document(ticker, form, "primary_html")
    source = independent_text.Source(
        cutoff_guard.load_document(row["full_path"], row["filing_date"]))
    text = built(ticker, form)["texts"]["input_controls.md"]
    misses = []
    for _, body in assemble_bundle.paragraph_blocks(text):
        for piece in independent_text.quotable(body):
            if not source.contains(piece):
                misses.append(piece)
    assert not misses, f"{ticker} {form}: {misses[:2]}"


# --- the filing index reaches every bundle -----------------------------------

@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", ("10-K", "10-Q"))
def test_the_bundle_lists_exactly_the_filings_the_index_holds(ticker, form):
    """Counted straight out of `submissions.json` with `json` alone — the file
    the bundle's own list is built from, read again without going through
    `src/parse_8k.py`."""
    bundle = built(ticker, form)
    cutoff = bundle["manifest"]["cutoff"]
    rows = json.loads((REPO_ROOT / "tests" / "fixtures" / ticker /
                       "submissions.json").read_text())["filings"]
    want_8k = sum(1 for row in rows if row["form"] in ("8-K", "8-K/A")
                  and row["filing_date"] <= cutoff)
    want_late = sum(1 for row in rows if row["form"].startswith("NT 10-")
                    and row["filing_date"] <= cutoff)

    text = bundle["texts"]["input_8k.md"]
    codes = text.split("## item codes")[1].split("## late-filing")[0]
    listed_8k = [line for line in codes.split("\n") if line.startswith("- ")]
    tail = text.split("## late-filing")[1].split("\n## ")[0]
    listed_late = [line for line in tail.split("\n") if line.startswith("- ")]
    if listed_late == [f"- none on or before {cutoff}"]:
        listed_late = []
    assert len(listed_8k) == want_8k, f"{ticker} {form}: 8-K lines"
    assert len(listed_late) == want_late, f"{ticker} {form}: late-filing lines"


def test_a_bundle_with_no_earnings_exhibit_still_carries_the_filing_index():
    """TTMI's only stored 8-K was filed the day after its 10-Q, so that bundle
    has no earnings release. The item codes and the late-filing notices come
    from `submissions.json`, which is on record either way."""
    text = built("TTMI", "10-Q")["texts"]["input_8k.md"]
    assert "no 8-K filed at or before 2026-08-05 is on record" in text
    assert "## item codes, every 8-K on or before 2026-08-05" in text
    assert "## late-filing notifications on or before 2026-08-05" in text
    assert "0001193125-26-337923" not in text      # filed 2026-08-06
    assert "0001193125-26-336163" not in text


# --- the cutoff holds in the prose, not only in the document list ------------
#
# Gate 3 compares `documents[*].filing_date` to the cutoff, so a bundle can pass
# it while a post-cutoff date sits in the sentence the predictor actually reads.
# These two tests read the rendered bundle instead of the document list.

ISO_DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")

# The two ways a filing states a period that has not happened yet, in the words
# the taxonomy uses for it: a forecast, a subsequent event, or a remaining
# performance obligation bucketed by the year it is expected to be recognised
# in. All three are disclosures *made by* a document filed inside the cutoff.
FORWARD_MEMBERS = {"srt:ScenarioForecastMember", "us-gaap:SubsequentEventMember"}
FORWARD_TAGS = ("RevenueRemainingPerformanceObligation",)

PROSE_FILES = tuple(name for name in assemble_bundle.FILES
                    if name != "input_numbers.json")


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", ("10-K", "10-Q"))
def test_no_prose_in_a_bundle_carries_a_date_later_than_its_own_cutoff(ticker, form):
    """Every ISO date in the eight non-numeric files, against the bundle's own
    cutoff. The manifest is one of the eight, so its exclusion reasons are read
    here too — that is where the absence sentence was copied to."""
    bundle = built(ticker, form)
    cutoff = bundle["manifest"]["cutoff"]
    late = []
    for name in PROSE_FILES:
        for line in bundle["texts"][name].split("\n"):
            for date in ISO_DATE.findall(line):
                if date > cutoff:
                    late.append(f"{name}: {date} in {line.strip()[:120]}")
    assert late == [], f"{ticker} {form} cutoff {cutoff}"


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", ("10-K", "10-Q"))
def test_a_later_date_in_the_numbers_is_the_filings_own_forward_disclosure(ticker, form):
    """`input_numbers.json` is the one file where a date after the cutoff is
    legitimate, because XBRL period dates are content, not provenance: GNRC's
    10-K buckets extended-warranty revenue out to 2031, QCOM forecasts a tax
    rate for fiscal 2027, NVDA's 10-Q reports a guarantee as a subsequent event
    at 2026-08-31. Deleting those would delete disclosure the filing made.

    So the assertion is not "no late date" but "every late date belongs to a
    forward-looking fact that a document filed inside the cutoff disclosed". A
    number lifted out of a document filed after the cutoff fails this.
    """
    bundle = built(ticker, form)
    cutoff = bundle["manifest"]["cutoff"]
    numbers = json.loads(bundle["texts"]["input_numbers.json"])
    filed = {row["accession"]: row["filing_date"] for row in numbers["documents"]}
    for fact in numbers["facts"]:
        blob = json.dumps(fact)
        if not [date for date in ISO_DATE.findall(blob) if date > cutoff]:
            continue
        source = fact["id"].split(":")[0]
        assert source in filed, f"{ticker} {form}: {fact['id']} names no document"
        assert filed[source] <= cutoff, (
            f"{ticker} {form}: {fact['tag']} comes from {source}, filed "
            f"{filed[source]}, after the cutoff {cutoff}")
        members = {part.get("member")
                   for part in (fact["context"].get("segment") or [])}
        assert (members & FORWARD_MEMBERS) or fact["tag"].startswith(FORWARD_TAGS), (
            f"{ticker} {form}: {fact['tag']} is dated after the cutoff {cutoff} "
            f"and is not a forecast, a subsequent event or a remaining "
            f"performance obligation — context {fact['context']}")


# --- a run of a later quarter is not a prior run -----------------------------

def written_run(root: Path, ticker: str, accession: str, flag: str,
                filing_date: str | None) -> Path:
    """One past run on disk: its own manifest, and one prediction."""
    run = root / ticker / accession
    run.mkdir(parents=True)
    if filing_date is not None:
        (run / "input_manifest.json").write_text(
            json.dumps({"ticker": ticker, "accession": accession,
                        "cutoff": filing_date, "filing_date": filing_date}),
            encoding="utf-8")
    (run / "prediction_accounting.json").write_text(
        json.dumps({"flags": [{"flag": flag, "outcome": "did not materialize"}]}),
        encoding="utf-8")
    return run


def test_a_prior_run_of_a_later_quarter_is_not_carried(tmp_path):
    """`cutoff_guard.load_bundle_file` does not date-gate, on purpose, so
    nothing stopped a run of a later quarter — its flags and its outcomes —
    from entering `input_prior_predictions.md`. The date is the one the past run
    recorded for itself."""
    written_run(tmp_path, "AAPL", "0000320193-25-000079",
                "earlier quarter flag", "2025-08-01")
    written_run(tmp_path, "AAPL", "0000320193-26-000050",
                "later quarter flag", "2026-07-31")

    text, entries = assemble_bundle.prior_predictions("AAPL", tmp_path, "2025-10-31")
    assert "earlier quarter flag" in text
    assert "later quarter flag" not in text
    assert len(entries) == 1
    assert "0000320193-26-000050" not in text


def test_a_prior_run_that_records_no_date_is_not_carried_either(tmp_path):
    """An undated run cannot be shown to be earlier, so it is not carried."""
    written_run(tmp_path, "AAPL", "0000320193-25-000079", "undated flag", None)
    text, entries = assemble_bundle.prior_predictions("AAPL", tmp_path, "2025-10-31")
    assert entries == [] and "undated flag" not in text
    assert "None on record" in text


def test_a_build_leaves_the_later_quarters_prediction_out_of_the_bundle(tmp_path):
    """The same thing through `build`, which is how it reaches a reader: the
    10-K's cutoff is 2025-10-31 and the run of the 2026 quarter is not in the
    file, by its text and by the manifest's count."""
    written_run(tmp_path, "AAPL", "0000320193-26-000050",
                "later quarter flag", "2026-07-31")
    bundle = assemble_bundle.build("AAPL", "10-K", prior_runs=tmp_path)
    assert bundle["manifest"]["cutoff"] == "2025-10-31"
    assert "later quarter flag" not in bundle["texts"]["input_prior_predictions.md"]
    assert "2026-07-31" not in bundle["texts"]["input_prior_predictions.md"]

    written_run(tmp_path, "AAPL", "0000320193-25-000079",
                "earlier quarter flag", "2025-08-01")
    again = assemble_bundle.build("AAPL", "10-K", prior_runs=tmp_path)
    assert "earlier quarter flag" in again["texts"]["input_prior_predictions.md"]


# --- the cutoff is bounded above by the report that triggered the run --------

def test_a_cutoff_after_the_triggering_report_is_refused():
    """`--cutoff 2026-08-01` on Apple's 10-K, filed 2025-10-31, used to build a
    bundle out of six documents filed after the report the bundle is for."""
    with pytest.raises(assemble_bundle.BundleError) as raised:
        assemble_bundle.build("AAPL", "10-K", cutoff="2026-08-01")
    assert "2026-08-01" in str(raised.value) and "2025-10-31" in str(raised.value)


def test_the_command_exits_non_zero_on_a_cutoff_after_the_report(tmp_path, capsys):
    out = tmp_path / "bundle"
    code = assemble_bundle.main(["--ticker", "aapl", "--form", "10-K",
                                 "--cutoff", "2026-08-01", "--out", str(out)])
    assert code != 0
    printed = capsys.readouterr().err
    assert "2026-08-01" in printed and "2025-10-31" in printed
    assert not out.exists()


# --- the manifest describes the bundle it is the index of --------------------

FILE_OF_SOURCE = {"8-K exhibit 99.1": "input_8k.md"}


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", ("10-K", "10-Q"))
def test_no_excluded_paragraph_is_still_in_the_file_it_was_excluded_from(ticker, form):
    """The one that mattered: 43 paragraphs across the fixture set were recorded
    as excluded and published as `verbatim` at the same time, because the 8-K
    was rendered from the uncleaned text while the exclusions came from a second
    cleaning of the same document.

    `test_an_excluded_paragraph_is_not_in_any_file` could not catch it — it
    compares **id sets**, and an exclusion id lives in its own namespace
    (`…:8k_excluded:1` against `…:8k_2_02:13`), so the two sets are disjoint
    whatever the text says. This compares text.
    """
    bundle = built(ticker, form)
    blocks = {}
    for name in assemble_bundle.PARAGRAPH_FILES:
        blocks[name] = {text.strip() for _, text
                        in assemble_bundle.paragraph_blocks(bundle["texts"][name])}
    still_there = []
    for entry in bundle["manifest"]["exclusions"]:
        text = (entry.get("text") or "").strip()
        source = entry["source"]
        if not text:
            continue
        if source.startswith(f"{form} notes"):
            name = "input_notes.md"
        elif source == f"{form} MD&A":
            name = "input_mdna.md"
        else:
            name = FILE_OF_SOURCE.get(source)
        if name and text in blocks[name]:
            still_there.append((entry["id"], name, text[:80]))
    assert still_there == [], f"{ticker} {form}"


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", ("10-K", "10-Q"))
def test_the_manifest_lists_the_documents_the_build_opened(ticker, form, monkeypatch):
    """Instrument the gateway itself and compare. `manifest.documents` used to
    be every fixture filed at or before the cutoff — AAPL's 10-Q listed the 10-K
    primary HTML, which nothing opens, and left out `submissions.json`, which
    supplies the whole item-code section of `input_8k.md`."""
    seen: list[Path] = []
    for name in ("load_bytes", "load_index"):
        original = getattr(cutoff_guard, name)

        def watched(path, *args, _original=original, **kwargs):
            result = _original(path, *args, **kwargs)
            seen.append(Path(path).resolve())
            return result
        monkeypatch.setattr(cutoff_guard, name, watched)

    manifest = assemble_bundle.build(ticker, form)["manifest"]
    listed = {(REPO_ROOT / "tests" / "fixtures" / ticker / row["path"]).resolve()
              for row in manifest["documents"]}
    assert listed == set(seen), f"{ticker} {form}"
    for row in manifest["documents"]:
        assert row["contributed_to"], row


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", ("10-K", "10-Q"))
def test_every_listed_document_points_a_reader_at_edgar(ticker, form):
    """A path into a fixture store the reader does not have is not a pointer.

    The submissions index is the one row with no accession and no report date:
    it is EDGAR's catalogue for a company, one JSON file per CIK, not a filing.
    Its URL is asserted against that shape instead.
    """
    for row in built(ticker, form)["manifest"]["documents"]:
        assert row["url"], row
        if row["role"] == assemble_bundle.INDEX_ROLE:
            assert row["url"].startswith("https://data.sec.gov/submissions/")
            assert row["accession"] == "" and row["report_date"] == ""
            continue
        assert row["accession"].replace("-", "") in row["url"], row
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", row["report_date"]), row


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("form", ("10-K", "10-Q"))
def test_the_submissions_index_carries_no_filing_date_and_says_why(ticker, form):
    """The fixture manifest records `filing_date` for the index as *the latest
    filing this index contains*, which is the newest date in the whole set —
    later than every cutoff. Copying it into a bundle as a filing date would put
    look-ahead in every manifest, and would state something the record itself
    says is false: the index is not a filing and has no filing date."""
    manifest = built(ticker, form)["manifest"]
    rows = [row for row in manifest["documents"]
            if row["role"] == assemble_bundle.INDEX_ROLE]
    assert len(rows) == 1
    assert rows[0]["filing_date"] is None
    assert "not itself a filing" in rows[0]["date_basis"]
    assert rows[0]["rows_used_through"] == manifest["cutoff"]


def test_a_cutoff_equal_to_the_triggering_reports_own_date_is_the_default():
    """The boundary itself is allowed — it is the default — so the check above
    is an upper bound and not an off-by-one that forbids the normal case."""
    named = assemble_bundle.build("AAPL", "10-K", cutoff="2025-10-31")["texts"]
    assert named == built("AAPL", "10-K")["texts"]
