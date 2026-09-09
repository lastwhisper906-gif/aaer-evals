"""Exhibit 10 arrives because an 8-K asked for it, and never otherwise.

`docs/INPUT_SPEC.md` §1: *Exhibit 10 — credit-agreement amendments and waivers,
**on trigger only** — an 8-K 1.01, or the debt note naming one — exhibit type
from the SGML header.* Two claims live in that line and both are judged here.

**The trigger.** Seagate's 8-K `0001193125-23-106624` of 2023-04-19 carries item
1.01, *entry into a material definitive agreement*. That is stated in the EDGAR
submissions index, which `docs/INPUT_SPEC.md` §1 names as the only place an 8-K's
item codes are stated, and the index is committed at
`tests/fixtures/STX/submissions.json`. It is checked here against the item codes
the fixture manifest recorded for the same accession, so the record is tied to
EDGAR's own statement rather than to itself.

**The document.** That submission's own SGML header names fifteen documents, and
exactly one of them is of the `EX-10` family: `EX-10.1`, document 2, file
`d497922dex101.htm`. The header is committed beside the exhibit and is read here
a second way, by a regular expression written in this file that imports nothing
from `src/`, so the transcription below and a second reading of the document both
have to agree with the parser. What that exhibit *is* — Seagate's settlement with
the Bureau of Industry and Security, not an amendment to a credit facility — the
trigger cannot know and does not claim: item 1.01 covers any material definitive
agreement, and the reader is handed the text to judge.

**And no other.** The same submission files `EX-99.1` — an earnings release, in a
filing that carries item 2.02 as well — and three inline-XBRL taxonomy documents
whose types begin with the five characters of `EX-10`: `EX-101.SCH`,
`EX-101.LAB`, `EX-101.PRE`. A prefix rule takes four documents out of this
submission and three out of ESCO's, where there is no exhibit 10 at all.

**Nothing without a trigger.** The negative is planted rather than borrowed: the
same record, the same header, the same stored exhibit, with `1.01` struck out of
the recorded item codes — and nothing is pulled. Beside it, Seagate's own
earnings-release 8-K is on record, carries no 1.01, and is never asked.
"""

from __future__ import annotations

import functools
import hashlib
import json
import re
import shutil
from pathlib import Path

import pytest

from src import assemble_bundle, cutoff_guard, exhibits
from tests import independent_text

FIXTURES = Path(__file__).resolve().parent / "fixtures"

# --- what the sources say -----------------------------------------------------
#
# Transcribed, each from the document named beside it. Nothing here was produced
# by running `src/exhibits.py`.

# The trigger, read off the row for this accession in EDGAR's submissions index,
# committed at tests/fixtures/STX/submissions.json.
TRIGGER = {"ticker": "STX", "accession": "0001193125-23-106624",
           "filing_date": "2023-04-19", "items": "1.01,2.02,9.01",
           "codes": ["1.01", "2.02", "9.01"]}

# The document, read off the `<TYPE>` / `<SEQUENCE>` / `<FILENAME>` lines of that
# submission's own SGML header, committed at
# tests/fixtures/STX/8-K/0001193125-23-106624/0001193125-23-106624-index-headers.html
EXHIBIT = {"type": "EX-10.1", "sequence": "2", "filename": "d497922dex101.htm"}

# Every type that header declares, in the header's own order. Written out because
# "that document and no other" is a claim about what else was there to take.
DECLARED = ["8-K", "EX-10.1", "EX-99.1", "EX-101.SCH", "EX-101.LAB", "EX-101.PRE",
            "GRAPHIC", "XML", "XML", "EXCEL", "XML", "XML", "XML", "JSON", "ZIP"]

# The earnings release of the same submission — the document that must not be
# pulled, sitting one `<DOCUMENT>` block below the one that must.
RELEASE_IN_THE_SAME_SUBMISSION = "d497922dex991.htm"

# Seagate's other 8-K on record: the earnings release the fixture set was built
# around. Its item codes are the manifest's, which came from the same index.
NO_TRIGGER = {"ticker": "STX", "accession": "0001137789-26-000153",
              "filing_date": "2026-07-28", "items": "2.02,7.01,9.01"}

# ESCO's 8-K of 2024-08-07 carries item 1.01 and files no exhibit for the
# agreement: its submission header names no `EX-10` document at all. Read off
# tests/fixtures/ESE/8-K/0001104659-24-086768/0001104659-24-086768-index-headers.html
NAMES_NO_EXHIBIT = {"ticker": "ESE", "accession": "0001104659-24-086768",
                    "filing_date": "2024-08-07", "items": "1.01,2.02,5.02,7.01,9.01"}
NAMES_NO_EXHIBIT_DECLARED = ["8-K", "EX-99.1", "EX-101.SCH", "EX-101.LAB",
                             "EX-101.PRE", "GRAPHIC", "XML", "EXCEL", "XML", "XML",
                             "XML", "JSON", "ZIP", "XML"]


# --- reading the header a second way ------------------------------------------
#
# A regular expression written here, importing nothing from `src/`, so the
# assertions below are not `src/exhibits.py` agreeing with itself.

HEADER_DOCUMENT = re.compile(
    r"&lt;TYPE&gt;(?P<type>\S+)\s*\n"
    r"&lt;SEQUENCE&gt;(?P<sequence>\S+)\s*\n"
    r"&lt;FILENAME&gt;(?P<filename>\S+)")


def document(ticker: str, role: str, accession: str) -> str:
    """One recorded 8-K document of a named submission, through the gate."""
    rows = [row for row in cutoff_guard.documents(ticker, form="8-K", role=role)
            if row["accession"] == accession]
    assert len(rows) == 1, f"{ticker} {role} {accession}: {len(rows)} on record"
    return cutoff_guard.load_document(rows[0]["full_path"], rows[0]["filing_date"])


def declared(ticker: str, accession: str) -> list[tuple[str, str, str]]:
    """(type, sequence, filename) for every document the header declares."""
    header = document(ticker, exhibits.TRIGGER_HEADER_ROLE, accession)
    return [(found.group("type"), found.group("sequence"), found.group("filename"))
            for found in HEADER_DOCUMENT.finditer(header)]


def index_row(ticker: str, accession: str) -> dict:
    """One filing's row in the committed EDGAR submissions index."""
    record = cutoff_guard.one_document(ticker, "submissions", "submissions_index")
    index = json.loads(cutoff_guard.load_index(record["full_path"]))
    rows = [row for row in index["filings"] if row["accession"] == accession]
    assert len(rows) == 1, f"{ticker}: {len(rows)} index rows for {accession}"
    return rows[0]


@functools.lru_cache(maxsize=None)
def built(ticker: str) -> dict:
    return exhibits.extract_on_trigger(ticker)


def only_trigger(ticker: str) -> dict:
    payload = built(ticker)
    assert len(payload["triggers"]) == 1, [t["accession"] for t in payload["triggers"]]
    return payload["triggers"][0]


# --- a copy of the record, for the plants --------------------------------------

def copy_eight_k(root: Path, ticker: str) -> Path:
    """One company's 8-K documents in a fixture root of their own.

    A test that edits the record edits this copy: `tests/fixtures/` is the record
    and `tests/test_fixtures.py` checks its bytes against the manifest.
    """
    recorded = json.loads((FIXTURES / ticker / "manifest.json").read_text(encoding="utf-8"))
    kept = [entry for entry in recorded["documents"] if entry["form"] == "8-K"]
    assert kept, ticker
    folder = root / ticker
    for entry in kept:
        target = folder / entry["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(FIXTURES / ticker / entry["path"], target)
    write_manifest(folder, {**recorded, "documents": kept})
    return root


def write_manifest(folder: Path, manifest: dict) -> None:
    (folder / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n",
                                          encoding="utf-8")


def manifest_of(root: Path, ticker: str) -> dict:
    return json.loads((root / ticker / "manifest.json").read_text(encoding="utf-8"))


def rows_of(manifest: dict, accession: str) -> list[dict]:
    return [entry for entry in manifest["documents"] if entry["accession"] == accession]


# --- the trigger is the item code, and the index is where it is stated ---------

@pytest.mark.parametrize("case", [TRIGGER, NO_TRIGGER, NAMES_NO_EXHIBIT],
                         ids=lambda case: case["accession"])
def test_the_recorded_item_codes_are_the_ones_the_submissions_index_states(case):
    """The record's `items` field is EDGAR's, copied when the fixture was made.

    Tying the two together is what makes the trigger a statement about the
    filing: without it, `items` would be a field this project could write
    anything into and the test would be reading its own note back.
    """
    row = index_row(case["ticker"], case["accession"])
    assert row["items"] == case["items"]
    assert row["filing_date"] == case["filing_date"]
    recorded = {entry["items"] for entry
                in cutoff_guard.documents(case["ticker"], form="8-K")
                if entry["accession"] == case["accession"]}
    assert recorded == {case["items"]}


def test_the_trigger_item_is_the_one_the_input_spec_names():
    assert exhibits.TRIGGER_ITEM == "1.01"
    assert TRIGGER["items"].split(",") == TRIGGER["codes"]
    assert exhibits.TRIGGER_ITEM in TRIGGER["codes"]
    assert exhibits.TRIGGER_ITEM not in NO_TRIGGER["items"].split(",")


def test_the_index_names_far_more_triggers_than_the_record_holds_a_document_for():
    """Twenty-five, which is the number `src/exhibits.py` says out loud.

    It is the reason the pull is bounded by the record and not by the index: a
    bundle carrying every exhibit of every 8-K Seagate ever filed under item 1.01
    is the *every exhibit ever filed* this item exists to avoid. What the reader
    loses by that bound is nothing, because `src/parse_8k.py::index_lines` prints
    the item codes and the date of all twenty-five into `input_8k.md`.
    """
    record = cutoff_guard.one_document("STX", "submissions", "submissions_index")
    index = json.loads(cutoff_guard.load_index(record["full_path"]))
    carrying = [row["accession"] for row in index["filings"]
                if row["form"] in ("8-K", "8-K/A")
                and exhibits.TRIGGER_ITEM in row["items"].split(",")]
    assert len(carrying) == 25
    assert TRIGGER["accession"] in carrying
    held = {entry["accession"] for entry
            in exhibits.eight_k_submissions("STX", cutoff="2026-09-01")}
    assert held & set(carrying) == {TRIGGER["accession"]}


def test_seagate_holds_two_8ks_and_one_of_them_carries_the_trigger():
    """Both submissions are on record, so the negative is a filing that was
    looked at and not taken, rather than a filing that was never there."""
    submissions = exhibits.eight_k_submissions("STX", cutoff="2026-09-01")
    assert [entry["accession"] for entry in submissions] == \
        [NO_TRIGGER["accession"], TRIGGER["accession"]]
    carrying = [entry["accession"] for entry in submissions
                if exhibits.TRIGGER_ITEM in entry["items"]]
    assert carrying == [TRIGGER["accession"]]


# --- the document is the one the submission header names -----------------------

def test_the_header_read_a_second_way_names_the_documents_transcribed_above():
    """The recorded list is a transcription; this is the header read again."""
    found = declared(TRIGGER["ticker"], TRIGGER["accession"])
    assert [kind for kind, _, _ in found] == DECLARED
    assert (EXHIBIT["type"], EXHIBIT["sequence"], EXHIBIT["filename"]) in found
    assert RELEASE_IN_THE_SAME_SUBMISSION in [name for _, _, name in found]


def test_the_exhibit_pulled_is_the_one_the_header_names_and_no_other():
    """The judge's claim. One `EX-10` document in a submission of fifteen."""
    pulled = only_trigger(TRIGGER["ticker"])["exhibits"]
    assert [(entry["type"], entry["sequence"], entry["filename"]) for entry in pulled] \
        == [(EXHIBIT["type"], EXHIBIT["sequence"], EXHIBIT["filename"])]
    names = [entry["filename"] for entry in pulled]
    assert RELEASE_IN_THE_SAME_SUBMISSION not in names
    assert not [name for name in names if name.endswith((".xsd", ".xml"))]


def test_the_stored_exhibit_declares_itself_the_document_the_header_named():
    """EDGAR serves an exhibit with its own `<DOCUMENT>` block on the front, so
    the bytes on record state what they are independently of the header that
    named them and of the filename they were fetched under."""
    html = document(TRIGGER["ticker"], exhibits.CONTRACT_EXHIBIT_ROLE,
                    TRIGGER["accession"])
    assert (f"<TYPE>{EXHIBIT['type']}\n<SEQUENCE>{EXHIBIT['sequence']}\n"
            f"<FILENAME>{EXHIBIT['filename']}\n") in html


def test_a_prefix_rule_takes_the_xbrl_taxonomy_documents_and_the_family_rule_does_not():
    """`EX-101.SCH`, `EX-101.LAB` and `EX-101.PRE` begin with the five characters
    of `EX-10` and are not exhibits. Every submission in this fixture set files
    all three, so the near-miss is the common case rather than a curiosity."""
    for case, expected in ((TRIGGER, [EXHIBIT["type"]]), (NAMES_NO_EXHIBIT, [])):
        kinds = [kind for kind, _, _ in declared(case["ticker"], case["accession"])]
        naive = [kind for kind in kinds if kind.upper().startswith("EX-10")]
        assert naive[-3:] == ["EX-101.SCH", "EX-101.LAB", "EX-101.PRE"]
        assert [kind for kind in kinds
                if exhibits.is_material_contract_exhibit(kind)] == expected


def test_the_family_rule_takes_ex_10_and_its_suffixes_and_nothing_else():
    assert exhibits.is_material_contract_exhibit("EX-10")
    assert exhibits.is_material_contract_exhibit("EX-10.1")
    assert exhibits.is_material_contract_exhibit("ex-10.27")
    assert not exhibits.is_material_contract_exhibit("EX-101.SCH")
    assert not exhibits.is_material_contract_exhibit("EX-100")
    assert not exhibits.is_material_contract_exhibit("EX-1")
    assert not exhibits.is_material_contract_exhibit("EX-21.1")
    assert not exhibits.is_material_contract_exhibit("8-K")


# --- and nothing without a trigger ---------------------------------------------

def test_an_8k_with_no_triggering_item_pulls_nothing(tmp_path):
    """The same record with `1.01` struck out of the item codes it recorded.

    The header still names `EX-10.1` and the exhibit is still on disk; the only
    thing that changed is the item codes EDGAR stated. Nothing is pulled, and the
    unedited copy beside it pulls the one exhibit — the positive control that
    keeps this from passing because the copy was broken.
    """
    intact = copy_eight_k(tmp_path / "intact", "STX")
    struck = copy_eight_k(tmp_path / "struck", "STX")
    manifest = manifest_of(struck, "STX")
    rows = rows_of(manifest, TRIGGER["accession"])
    assert len(rows) == 2, [row["role"] for row in rows]
    for row in rows:
        row["items"] = "2.02,9.01"
    write_manifest(struck / "STX", manifest)

    before = exhibits.extract_on_trigger("STX", fixtures_root=intact)
    after = exhibits.extract_on_trigger("STX", fixtures_root=struck)
    assert [entry["filename"] for trigger in before["triggers"]
            for entry in trigger["exhibits"]] == [EXHIBIT["filename"]]
    assert after["triggers"] == []
    assert after["eight_k_count"] == before["eight_k_count"]
    assert "exhibits named: 0" in exhibits.trigger_counts(after)


def test_the_earnings_release_8k_is_on_record_and_is_never_asked():
    """Seagate's other 8-K is a filing this module read the item codes of and
    passed over. Its exhibit 99.1 is on record too, and is not an exhibit 10."""
    payload = built("STX")
    assert payload["eight_k_count"] == 2
    assert [trigger["accession"] for trigger in payload["triggers"]] == \
        [TRIGGER["accession"]]
    held = cutoff_guard.one_document("STX", "8-K", "exhibit_99_1")
    assert held["accession"] == NO_TRIGGER["accession"]


def test_a_cutoff_before_the_triggering_8k_pulls_nothing():
    """`CLAUDE.md`: nothing filed after the triggering report enters the input.
    The day itself is allowed and the day before is not."""
    assert [trigger["accession"] for trigger
            in exhibits.extract_on_trigger("STX", cutoff=TRIGGER["filing_date"])
            ["triggers"]] == [TRIGGER["accession"]]
    earlier = exhibits.extract_on_trigger("STX", cutoff="2023-04-18")
    assert earlier["triggers"] == []
    assert earlier["eight_k_count"] == 0


def test_a_company_whose_8ks_carry_no_trigger_pulls_nothing():
    payload = built("AAPL")
    assert payload["eight_k_count"] == 1
    assert payload["triggers"] == []


# --- a trigger whose submission filed no exhibit --------------------------------

def test_a_trigger_whose_submission_names_no_exhibit_is_reported_not_refused():
    """ESCO's 8-K of 2024-08-07 carries item 1.01 and files no `EX-10`.

    Refusing it would take a real filing out of the bundle; reporting it is what
    tells the reader the agreement exists and was not filed as an exhibit.
    """
    kinds = [kind for kind, _, _ in declared(NAMES_NO_EXHIBIT["ticker"],
                                             NAMES_NO_EXHIBIT["accession"])]
    assert kinds == NAMES_NO_EXHIBIT_DECLARED       # the header was read, not empty
    trigger = only_trigger(NAMES_NO_EXHIBIT["ticker"])
    assert trigger["accession"] == NAMES_NO_EXHIBIT["accession"]
    assert trigger["exhibits"] == []
    text = exhibits.render_on_trigger(built(NAMES_NO_EXHIBIT["ticker"]))
    assert "names no EX-10 document" in text


# --- what the record has to hold ------------------------------------------------

def test_an_exhibit_on_record_that_the_header_does_not_name_is_refused(tmp_path):
    root = copy_eight_k(tmp_path / "renamed", "STX")
    manifest = manifest_of(root, "STX")
    entry = next(row for row in manifest["documents"]
                 if row["role"] == exhibits.CONTRACT_EXHIBIT_ROLE)
    stored = root / "STX" / entry["path"]
    moved = stored.with_name("some-other-name.htm")
    stored.rename(moved)
    entry["path"] = str(moved.relative_to(root / "STX"))
    write_manifest(root / "STX", manifest)
    with pytest.raises(exhibits.ExhibitError):
        exhibits.extract_on_trigger("STX", fixtures_root=root)


def test_a_trigger_with_no_submission_header_on_record_is_refused(tmp_path):
    """The header is what names the exhibit. Without it the trigger fires and
    there is nothing to name, which is a refusal and not an empty list."""
    root = copy_eight_k(tmp_path / "headerless", "STX")
    manifest = manifest_of(root, "STX")
    manifest["documents"] = [row for row in manifest["documents"]
                             if row["role"] != exhibits.TRIGGER_HEADER_ROLE]
    write_manifest(root / "STX", manifest)
    with pytest.raises(exhibits.ExhibitError):
        exhibits.extract_on_trigger("STX", fixtures_root=root)


def test_the_stored_documents_came_from_the_urls_this_module_names():
    """`src/exhibits.py` does not fetch, so the record is where the provenance
    lives: both documents name the EDGAR url their bytes came from, and it is
    the url the module's own two shapes build."""
    wanted = {TRIGGER["accession"]: [exhibits.TRIGGER_HEADER_ROLE,
                                     exhibits.CONTRACT_EXHIBIT_ROLE],
              NAMES_NO_EXHIBIT["accession"]: [exhibits.TRIGGER_HEADER_ROLE]}
    for case in (TRIGGER, NAMES_NO_EXHIBIT):
        recorded = json.loads((FIXTURES / case["ticker"] / "manifest.json")
                              .read_text(encoding="utf-8"))
        cik, accession = int(recorded["cik"]), case["accession"]
        rows = [entry for entry in recorded["documents"]
                if entry["accession"] == accession]
        # A loop over no rows asserts nothing; this is what says how many there are.
        assert sorted(entry["role"] for entry in rows) == sorted(wanted[accession])
        for entry in rows:
            name = Path(entry["path"]).name
            shape = (exhibits.HEADER_URL.format(cik=cik, dashed=accession,
                                                accession=accession.replace("-", ""))
                     if entry["role"] == exhibits.TRIGGER_HEADER_ROLE else
                     exhibits.ARCHIVE_URL.format(
                         cik=cik, accession=accession.replace("-", ""), name=name))
            assert entry["url"] == shape
            assert hashlib.sha256(
                (FIXTURES / case["ticker"] / entry["path"]).read_bytes()
            ).hexdigest() == entry["sha256"]


# --- the file the notes-text reader is handed ------------------------------------

def test_every_pulled_paragraph_is_the_exhibits_own_text():
    """Verbatim, checked against a second tag stripper that imports nothing from
    `src/`. A table's rows are checked cell by cell, because rendering a row
    inserts the `|` the source never had."""
    html = document(TRIGGER["ticker"], exhibits.CONTRACT_EXHIBIT_ROLE,
                    TRIGGER["accession"])
    source = independent_text.Source(html)
    paragraphs = only_trigger(TRIGGER["ticker"])["exhibits"][0]["paragraphs"]
    assert paragraphs
    prose = [text for text in paragraphs if not text.startswith("|")]
    cells = [cell.strip() for text in paragraphs if text.startswith("|")
             for row in text.split("\n") for cell in row.split("|") if cell.strip()]
    assert cells
    assert not source.missing(prose)
    assert not source.missing(cells)


def test_every_paragraph_id_names_the_triggering_8k_and_counts_from_one():
    payload = built(TRIGGER["ticker"])
    text = exhibits.render_on_trigger(payload)
    found = [line.strip()[1:-1] for line in text.split("\n")
             if line.startswith("[") and line.rstrip().endswith("]")]
    count = sum(len(entry["paragraphs"] or []) for trigger in payload["triggers"]
                for entry in trigger["exhibits"])
    assert found == [f"{TRIGGER['accession']}:exhibit_10:{number}"
                     for number in range(1, count + 1)]


def test_the_command_writes_both_exhibits_into_the_one_file(tmp_path):
    """`docs/INPUT_SPEC.md`: `input_exhibits.md` is the Exhibit 21 diff *and* any
    Exhibit 10 pulled on trigger."""
    out = tmp_path / "input_exhibits.md"
    assert exhibits.main(["--ticker", "stx", "--out", str(out)]) == 0
    text = out.read_text(encoding="utf-8")
    assert text.startswith("# STX Exhibit 21")
    assert f"## exhibit 10 — a material definitive agreement, pulled where an 8-K " \
           f"on record carries item {exhibits.TRIGGER_ITEM}" in text
    assert EXHIBIT["type"] in text and EXHIBIT["filename"] in text
    assert TRIGGER["accession"] in text


def test_the_file_says_so_when_nothing_triggered(tmp_path):
    """Silence would read as *no amendment*. Apple has filed no 8-K carrying
    item 1.01 at all, and the file it is handed says that in a sentence."""
    out = tmp_path / "input_exhibits.md"
    assert exhibits.main(["--ticker", "AAPL", "--out", str(out)]) == 0
    text = out.read_text(encoding="utf-8")
    assert f"carries item {exhibits.TRIGGER_ITEM}, so no exhibit 10 was pulled" in text
    assert "exhibits named: 0, read: 0, paragraphs: 0" in text


def test_every_quotable_block_is_a_subsidiary_row_or_a_paragraph_of_the_exhibit(
        tmp_path):
    """`assemble_bundle.paragraph_blocks` skips `#` headings and folds every other
    line into the block of the id above it, and a quote gate matches a reader's
    quote against that block. The Exhibit 10 half is appended below the last
    subsidiary row, so every line of it that is not the exhibit's own text has to
    be a heading — otherwise the arithmetic in it lands inside that subsidiary's
    block and a reader quoting it would pass the gate.
    """
    out = tmp_path / "input_exhibits.md"
    assert exhibits.main(["--ticker", "STX", "--out", str(out)]) == 0
    payload = exhibits.extract("STX")
    changes = payload["diff"]
    expected = (
        [exhibits.row(entry) for entry in changes["added"] + changes["removed"]]
        + [exhibits.moved_row(entry) for entry in changes["jurisdiction_changed"]]
        + [text for trigger in built("STX")["triggers"]
           for entry in trigger["exhibits"] for text in entry["paragraphs"] or []])
    blocks = assemble_bundle.paragraph_blocks(out.read_text(encoding="utf-8"))
    assert [text for _, text in blocks] == expected
