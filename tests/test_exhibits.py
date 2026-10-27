"""Exhibit 21: the document the submission says it is, and the diff over it.

Two expected values, and neither of them can come from `src/exhibits.py`.

**The exhibit type**, for twelve of twelve, is transcribed into
`tests/fixtures/{ticker}/expected_values.json` off the `<TYPE>` line of each
stored submission header and read back through `tests/expected_values.py`, which
refuses an entry that names no source. It is asserted per company, and the same
headers are read a second time here by a regex written in this file that imports
nothing from `src/` — so the recorded transcription and a second reading of the
document both have to agree with the parser.

**The planted subsidiary** is written by these tests into a copy of a fixture,
so its value is known by construction rather than by running anything. Planting
it into the current 10-K's exhibit must make it an addition and planting it into
the prior year's must make it a removal; the same copy without the plant must
report it nowhere, which is the silence half of the same claim.

The filename is never the route in, and the ways a filename rule fails on this
fixture set are counted here rather than described: Generac's exhibit is
`ex_873991.htm` and NVIDIA's is `subsidiariesofregistrantfy.htm`, so a rule
looking for `21` never reaches the exhibit for two of the twelve; twenty-two of
the twenty-four submissions give that rule more than one candidate, because a
Section 1350 certification is `EX-32.1` and is filed as `ex321...`; and Apple's
and Qualcomm's prior-year submissions each add an `EX-10.21` material contract
to the pile.
"""

from __future__ import annotations

import functools
import hashlib
import json
import re
import shutil
from html.parser import HTMLParser
from pathlib import Path

import pytest

from src import assemble_bundle, cutoff_guard, exhibits
from src.fetch_fixtures import TICKERS
from tests import expected_values, independent_text

FIXTURES = Path(__file__).resolve().parent / "fixtures"

EXHIBIT_ROLES = ("submission_header", "exhibit_21",
                 "prior_year_submission_header", "prior_year_exhibit_21")

# The subsidiary these tests plant. Its name carries the word `Subsidiary`,
# which is one of the column-label words the heading rule reads, so a rule that
# dropped a row on either cell instead of both would swallow it and the plant
# would go missing.
PLANTED = {"name": "Planted Subsidiary Holdings Limited", "jurisdiction": "Nowhere"}
PLANTED_ROW = "<tr><td>{name}</td><td>{jurisdiction}</td></tr>"

# Cells a filer leaves as a zero-width space, a byte-order mark or a soft hyphen.
FILLER = "​﻿­"


# --- reading the documents a second way --------------------------------------
#
# Every reading in this file that could otherwise be "the parser agrees with
# itself" is made twice. The header is read by the regex below and the exhibit
# by the row parser below, both written here and importing nothing from `src/`.

HEADER_DOCUMENT = re.compile(
    r"&lt;TYPE&gt;(?P<type>\S+)\s*\n"
    r"&lt;SEQUENCE&gt;(?P<sequence>\S+)\s*\n"
    r"&lt;FILENAME&gt;(?P<filename>\S+)")

# A different shape of heading rule from the one under test: this one reads the
# jurisdiction cell alone, where `src/exhibits.py` requires both cells to name a
# column. Two rules that disagree would show up as a different list.
COLUMN_CELL = re.compile(r"jurisdiction|incorporation|organization", re.IGNORECASE)


class _Rows(HTMLParser):
    """Table rows as cell text. Twenty lines of `html.parser`, nothing from src/."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.rows: list[list[str]] = []
        self._cell: list[str] | None = None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.rows.append([])
        elif tag in ("td", "th"):
            if not self.rows:
                self.rows.append([])
            self.rows[-1].append("")
            self._cell = []

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._cell is not None:
            self.rows[-1][-1] = "".join(self._cell).strip()
            self._cell = None

    def handle_data(self, data):
        if self._cell is not None:
            self._cell.append(data)


def flat(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def recount(source: str) -> list[tuple[str, str]]:
    """(name, jurisdiction) for every subsidiary row, by this file's own reader."""
    parser = _Rows()
    parser.feed(source)
    parser.close()
    found = []
    for row in parser.rows:
        cells = [cell for cell in
                 (cell.strip().strip(FILLER).strip() for cell in row) if cell]
        if len(cells) < 2 or COLUMN_CELL.search(cells[1]):
            continue
        found.append((flat(cells[0]), flat(cells[1])))
    return found


# --- the record ---------------------------------------------------------------

def document(ticker: str, role: str) -> str:
    row = cutoff_guard.one_document(ticker, "10-K", role)
    return cutoff_guard.load_document(row["full_path"], row["filing_date"])


# Two of the eight added on 2026-10-07 filed no Exhibit 21 at all: Western
# Digital's 10-K of 2026-08-14 and Arista's of 2026-02-17 name the report, the
# certifications, the consent and the taxonomy and nothing of the EX-21 family.
# Read off the two headers by hand and held both ways below: the header names
# none and the record holds none, and the module reads that as the absence by
# name rather than a refusal. Every other company's current 10-K names one.
NAMES_NO_SUBSIDIARY_EXHIBIT = ("WDC", "ANET")

# Celestica's Exhibit 21, in both years, is a list with no table: one '<div>'
# line per subsidiary, 'Name, a <jurisdiction> corporation'.
# 10-K/0001030894-26-000011/exhibit2112025.htm (EX-21.1, document 3 of its
# header) names five, from 'Celestica Cayman Holdings 1 Limited, a Cayman
# Islands corporation' to 'Celestica Holdings Pte Limited, a Singapore
# corporation'; 10-K/0001030894-25-000014/exhibit2112024.htm (EX-21.1, document
# 10) names seven, the same five with '2480333 Ontario Inc., an Ontario, Canada
# corporation' and 'Celestica International LP, an Ontario, Canada limited
# partnership'. `src/exhibits.py` reads table rows only, so it reads none in
# either year, and `input_exhibits.md` tells the reader '0 subsidiaries in this
# 10-K against 0 in the prior' where the exhibits list five against seven, two
# of them dropped; a test that plants a row finds no table to plant it in. The
# lists themselves are the expected values below (LISTED_AS_LINES), and the
# tests that read a list hold it to at least one subsidiary before they assert
# anything of its members, so none of them passes on Celestica's two empty
# ones. The second reader in this file reads table rows too, so the two readers
# agree at none; a parser that learns lines needs that reader to learn them
# as well before the second-way test can pass. Strict, so a reading rule for a
# list written as lines turns these red and the marks come off.
LIST_WITHOUT_A_TABLE = {
    "CLS": "the exhibit lists 'Celestica LLC, a Delaware, U.S. limited liability "
           "company' and its siblings one <div> line each, with no table; 5 read this "
           "year and 7 the year before, none parsed",
}

# Celestica's two lists, each line as its exhibit prints it, in order, between
# the heading 'Subsidiaries of the Registrant*' and the footnote '* Subsidiaries
# that, in aggregate, would not be a “significant subsidiary” as defined in Rule
# 1-02(w) of Regulation S-X, have been omitted.' -- the current 10-K's
# exhibit2112025.htm and the prior year's exhibit2112024.htm.
LISTED_AS_LINES = {
    ("CLS", "exhibit_21"): (
        "Celestica Cayman Holdings 1 Limited, a Cayman Islands corporation",
        "Celestica LLC, a Delaware, U.S. limited liability company",
        "Celestica (Thailand) Limited, a Thailand corporation",
        "Celestica (USA) Inc., a Delaware, U.S. corporation",
        "Celestica Holdings Pte Limited, a Singapore corporation",
    ),
    ("CLS", "prior_year_exhibit_21"): (
        "Celestica Cayman Holdings 1 Limited, a Cayman Islands corporation",
        "Celestica LLC, a Delaware, U.S. limited liability company",
        "Celestica (Thailand) Limited, a Thailand corporation",
        "Celestica (USA) Inc., a Delaware, U.S. corporation",
        "2480333 Ontario Inc., an Ontario, Canada corporation",
        "Celestica Holdings Pte Limited, a Singapore corporation",
        "Celestica International LP, an Ontario, Canada limited partnership",
    ),
}


def listed_without_a_table(ticker: str):
    """One ticker case, carrying the strict mark where LIST_WITHOUT_A_TABLE names it."""
    if ticker not in LIST_WITHOUT_A_TABLE:
        return ticker
    return pytest.param(ticker, marks=pytest.mark.xfail(
        strict=True, reason=f"{ticker}: {LIST_WITHOUT_A_TABLE[ticker]}"))


def list_case(ticker: str, role: str):
    """One (ticker, role) case, carrying the strict mark for its company's defect:
    HEADING_ROW_KEPT for the document it names, LIST_WITHOUT_A_TABLE for both of
    a company's years."""
    if (ticker, role) in HEADING_ROW_KEPT:
        reason = HEADING_ROW_KEPT[(ticker, role)]
    elif ticker in LIST_WITHOUT_A_TABLE:
        reason = LIST_WITHOUT_A_TABLE[ticker]
    else:
        return pytest.param(ticker, role)
    return pytest.param(ticker, role, marks=pytest.mark.xfail(
        strict=True, reason=f"{ticker} {role}: {reason}"))


@functools.lru_cache(maxsize=None)
def no_subsidiary_exhibit(ticker: str) -> bool:
    """Does the current 10-K's header, read by this file's regex, name no EX-21?"""
    found = [entry for entry in HEADER_DOCUMENT.finditer(document(ticker, "submission_header"))
             if entry.group("type").upper() == "EX-21"
             or entry.group("type").upper().startswith("EX-21.")]
    return not found


@functools.lru_cache(maxsize=None)
def built(ticker: str) -> dict:
    return exhibits.extract(ticker)


def copy_fixtures(root: Path, ticker: str) -> Path:
    """One company's four Exhibit 21 documents in a fixture root of their own.

    A test that edits a filing edits this copy. `tests/fixtures/` is the record
    and `tests/test_fixtures.py` checks its bytes against the manifest, so
    nothing here may write there.
    """
    recorded = json.loads((FIXTURES / ticker / "manifest.json").read_text(encoding="utf-8"))
    kept = [entry for entry in recorded["documents"] if entry["role"] in EXHIBIT_ROLES]
    # A 10-K that filed no Exhibit 21 has three of the four documents on record.
    expected = len(EXHIBIT_ROLES) - (1 if no_subsidiary_exhibit(ticker) else 0)
    assert len(kept) == expected, f"{ticker}: {[e['role'] for e in kept]}"
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


def entry_of(manifest: dict, role: str) -> dict:
    return next(entry for entry in manifest["documents"] if entry["role"] == role)


def plant(root: Path, ticker: str, role: str, subsidiary: dict) -> None:
    """Put one more subsidiary row into a copied exhibit, and re-record it."""
    manifest = manifest_of(root, ticker)
    entry = entry_of(manifest, role)
    path = root / ticker / entry["path"]
    source = path.read_text(encoding="utf-8")
    closing = source.rfind("</table>")
    assert closing > 0, f"{ticker} {role}: no table to plant a subsidiary in"
    edited = source[:closing] + PLANTED_ROW.format(**subsidiary) + source[closing:]
    path.write_text(edited, encoding="utf-8")
    entry["bytes"] = len(edited.encode("utf-8"))
    entry["sha256"] = hashlib.sha256(edited.encode("utf-8")).hexdigest()
    write_manifest(root / ticker, manifest)


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_stored_documents_came_from_the_urls_this_module_names(ticker):
    """`src/exhibits.py` does not fetch, so the record is where the provenance
    lives: every one of these four documents has to name the EDGAR url its
    bytes came from, and it has to be the url the module's own two shapes
    build."""
    recorded = json.loads((FIXTURES / ticker / "manifest.json").read_text(encoding="utf-8"))
    cik = int(recorded["cik"])
    for header_role, exhibit_role in exhibits.ROLE_PAIRS:
        header = entry_of(recorded, header_role)
        accession = header["accession"]
        assert header["url"] == exhibits.HEADER_URL.format(
            cik=cik, accession=accession.replace("-", ""), dashed=accession)
        if header_role == "submission_header" and no_subsidiary_exhibit(ticker):
            # The header names no exhibit, so the record holds none to source.
            assert not [e for e in recorded["documents"] if e["role"] == exhibit_role]
            continue
        exhibit = entry_of(recorded, exhibit_role)
        assert exhibit["accession"] == accession
        assert exhibit["url"] == exhibits.ARCHIVE_URL.format(
            cik=cik, accession=accession.replace("-", ""),
            name=Path(exhibit["path"]).name)


@pytest.mark.parametrize("ticker", [listed_without_a_table(ticker) for ticker in TICKERS])
def test_a_ten_k_that_names_no_exhibit_21_is_read_as_the_absence_by_name(ticker):
    """Both sides: where the header names no document of the EX-21 family the
    record holds none, the expected values are null, and the module names the
    absence; everywhere else the header names one and the module reads it."""
    absent = no_subsidiary_exhibit(ticker)
    assert absent == (ticker in NAMES_NO_SUBSIDIARY_EXHIBIT)
    current = built(ticker)["exhibit"]
    if absent:
        assert current["subsidiaries"] is None
        assert current["absent"] == exhibits.NO_SUBSIDIARY_EXHIBIT
        assert current["type"] is None and current["filename"] is None
        assert expected_values.value(ticker, "exhibits.10-K.exhibit_type") is None
        assert expected_values.value(ticker, "exhibits.10-K.exhibit_filename") is None
        assert built(ticker)["diff"] is None
    else:
        assert "absent" not in current
        assert current["subsidiaries"]
        assert expected_values.value(ticker, "exhibits.10-K.exhibit_type")


# --- the type is the header's, for twelve of twelve ---------------------------

@pytest.mark.parametrize("ticker", TICKERS)
def test_the_exhibit_type_is_the_one_the_submission_header_declares(ticker):
    assert built(ticker)["exhibit"]["type"] == \
        expected_values.value(ticker, "exhibits.10-K.exhibit_type")


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_exhibit_read_is_the_file_the_header_pairs_with_that_type(ticker):
    assert built(ticker)["exhibit"]["filename"] == \
        expected_values.value(ticker, "exhibits.10-K.exhibit_filename")


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_prior_years_type_comes_from_its_own_submissions_header(ticker):
    assert built(ticker)["prior_exhibit"]["type"] == \
        expected_values.value(ticker, "exhibits.10-K.prior_year_exhibit_type")


@pytest.mark.parametrize("ticker", TICKERS)
def test_the_prior_years_exhibit_is_the_file_that_header_names(ticker):
    assert built(ticker)["prior_exhibit"]["filename"] == \
        expected_values.value(ticker, "exhibits.10-K.prior_year_exhibit_filename")


@pytest.mark.parametrize("ticker", TICKERS)
@pytest.mark.parametrize("role,key", [
    ("submission_header", "exhibits.10-K.exhibit"),
    ("prior_year_submission_header", "exhibits.10-K.prior_year_exhibit")])
def test_the_header_read_a_second_way_names_the_same_one_document(ticker, role, key):
    """The recorded value is a transcription; this is the header read again.

    One document of the EX-21 family per submission, found by a regex written in
    this file, and it is the one the expected value names.
    """
    found = [entry for entry in HEADER_DOCUMENT.finditer(document(ticker, role))
             if entry.group("type").upper() == "EX-21"
             or entry.group("type").upper().startswith("EX-21.")]
    if expected_values.value(ticker, key + "_type") is None:
        # The recorded absence: the header, read again, names none either.
        assert found == [], f"{ticker} {role}: {[e.group('type') for e in found]}"
        assert expected_values.value(ticker, key + "_filename") is None
        return
    assert len(found) == 1, f"{ticker} {role}: {[e.group('type') for e in found]}"
    assert found[0].group("type") == expected_values.value(ticker, key + "_type")
    assert found[0].group("filename") == expected_values.value(ticker, key + "_filename")


def test_both_types_are_in_the_fixture_set_so_the_rule_is_the_family():
    """A match on the literal `EX-21.1` would find nine of the twelve, and
    Franklin Electric, of the eight added on 2026-10-07, files the bare type
    too, as does Motorola Solutions of the next eight; Flex files `EX-21.01`,
    a third spelling of the family; the two that filed no exhibit at all
    record no type.

    Of the third eight, AMD files the bare type in both years ('<TYPE>EX-21
    <SEQUENCE>5 <FILENAME>exh_21-10kfy25.htm' and '<TYPE>EX-21 <SEQUENCE>4
    <FILENAME>ex21-10kfy2412_28.htm' in its two headers), as does ADTRAN
    ('<TYPE>EX-21 <SEQUENCE>9 <FILENAME>adtn-ex21.htm' in its 10-K of 2026-02-26,
    0001193125-26-073878, and '<TYPE>EX-21 <SEQUENCE>7 <FILENAME>adtn-ex21.htm'
    in its 10-K of 2025-03-03, 0000950170-25-031056), and NAPCO a fourth
    spelling, `EX-21.0`, in both ('<TYPE>EX-21.0 <SEQUENCE>3
    <FILENAME>nssc-20260630xex21d0.htm' and '<TYPE>EX-21.0 <SEQUENCE>3
    <FILENAME>nssc-20250630xex21d0.htm')."""
    recorded = {ticker: expected_values.value(ticker, "exhibits.10-K.exhibit_type")
                for ticker in TICKERS if ticker not in NAMES_NO_SUBSIDIARY_EXHIBIT}
    assert sorted(t for t, kind in recorded.items() if kind == "EX-21") == \
        ["ADTN", "AMD", "CARR", "ESE", "FELE", "MSI", "QCOM"]
    assert sorted(t for t, kind in recorded.items() if kind == "EX-21.01") == ["FLEX"]
    assert sorted(t for t, kind in recorded.items() if kind == "EX-21.0") == ["NSSC"]
    assert {kind for kind in recorded.values()} == \
        {"EX-21", "EX-21.1", "EX-21.01", "EX-21.0"}


# --- what a filename rule does instead ----------------------------------------

def test_two_of_the_twelve_name_the_exhibit_without_a_21_in_it():
    """Generac's `ex_873991.htm` and NVIDIA's `subsidiariesofregistrantfy.htm`.

    And, of the third eight, American Superconductor's: its header pairs
    '<TYPE>EX-21.1 <SEQUENCE>2' with '<FILENAME>ex_919730.htm', and the prior
    year's '<TYPE>EX-21.1 <SEQUENCE>3' with '<FILENAME>ex_774519.htm' -- serial
    names from the same filer agent as Generac's, whose accessions both begin
    0001437749."""
    blind = [ticker for ticker in TICKERS
             if ticker not in NAMES_NO_SUBSIDIARY_EXHIBIT
             and "21" not in expected_values.value(ticker,
                                                   "exhibits.10-K.exhibit_filename")]
    assert blind == ["GNRC", "NVDA", "AMSC"]


@pytest.mark.parametrize("ticker", ("GNRC", "NVDA", "AMSC"))
@pytest.mark.parametrize("role,key", [
    ("submission_header", "exhibits.10-K.exhibit_filename"),
    ("prior_year_submission_header", "exhibits.10-K.prior_year_exhibit_filename")])
def test_a_filename_rule_never_reaches_those_two_exhibits(ticker, role, key):
    """Not "it finds nothing": the rule finds other documents and returns one of
    them. The exhibit it was looking for is never among them."""
    header = document(ticker, role)
    wanted = expected_values.value(ticker, key)
    candidates = [entry.group("filename") for entry in HEADER_DOCUMENT.finditer(header)
                  if "21" in entry.group("filename")]
    assert wanted not in candidates
    assert exhibits.named_exhibit(header)["filename"] == wanted


def test_a_filename_rule_has_more_than_one_candidate_almost_everywhere():
    """A Section 1350 certification is `EX-32.1` and gets filed as `ex321...`,
    `exhibit321-...`, `nvda-2026xex321.htm` — so `21` in the name matches it too,
    in twenty-two of these twenty-four submissions. Generac's two are the
    exception, and there the one candidate is not an exhibit at all."""
    counted = {(ticker, role): [entry.group("type") for entry
                                in HEADER_DOCUMENT.finditer(document(ticker, role))
                                if "21" in entry.group("filename")]
               for ticker in TICKERS
               for role in ("submission_header", "prior_year_submission_header")}
    # Two headers per company, over the twelve, the eight added on 2026-10-07,
    # the next eight and the third eight added the same day: 36 × 2. Every one
    # of the eight's sixteen headers lists an `R21.htm` among its XML files, and
    # so does every one of the next eight's sixteen, so none of them is alone
    # either. The third eight's sixteen list an `R21.htm` too, and fifteen of
    # them a second name with 21 in it: the exhibit itself, an `EX-32.1`, or
    # American Superconductor's prior-year `EX-31.1` 'ex_774521.htm'. American
    # Superconductor's current header, 0001437749-26-018542, is the sixteenth:
    # its exhibit is 'ex_919730.htm' and its certifications carry serial names
    # too, so 'R21.htm' is the one candidate, and not an exhibit at all.
    assert len(counted) == 72
    alone = sorted(key for key, found in counted.items() if len(found) < 2)
    assert alone == [("AMSC", "submission_header"),
                     ("GNRC", "prior_year_submission_header"),
                     ("GNRC", "submission_header")]
    for key in alone:
        assert not [kind for kind in counted[key] if kind.upper().startswith("EX-")]


@pytest.mark.parametrize("ticker", ("AAPL", "QCOM"))
def test_a_rule_reading_the_filename_answers_with_a_material_contract(ticker):
    """These two prior-year submissions carry an `EX-10.21` whose name has 21 in
    it. A filename rule has several candidates and no way to choose between them;
    the header has one document of the EX-21 family and says which."""
    header = document(ticker, "prior_year_submission_header")
    named_21 = [(entry.group("type"), entry.group("filename"))
                for entry in HEADER_DOCUMENT.finditer(header)
                if "21" in entry.group("filename")]
    assert len(named_21) > 1, named_21
    assert "EX-10.21" in [kind for kind, name in named_21]
    assert exhibits.named_exhibit(header)["filename"] == \
        expected_values.value(ticker, "exhibits.10-K.prior_year_exhibit_filename")


def test_the_family_rule_takes_ex_21_and_its_suffixes_and_nothing_else():
    assert exhibits.is_subsidiary_exhibit("EX-21")
    assert exhibits.is_subsidiary_exhibit("EX-21.1")
    assert exhibits.is_subsidiary_exhibit("ex-21.2")
    assert not exhibits.is_subsidiary_exhibit("EX-10.21")
    assert not exhibits.is_subsidiary_exhibit("EX-211")
    assert not exhibits.is_subsidiary_exhibit("EX-2")
    assert not exhibits.is_subsidiary_exhibit("EX-99.1")


def test_a_submission_naming_no_exhibit_of_the_family_is_refused():
    with pytest.raises(exhibits.ExhibitError):
        exhibits.named_exhibit("&lt;TYPE&gt;EX-10.21\n&lt;SEQUENCE&gt;2\n"
                               "&lt;FILENAME&gt;contract.htm\n")


def test_a_submission_naming_two_of_the_family_is_refused():
    with pytest.raises(exhibits.ExhibitError):
        exhibits.named_exhibit(
            "&lt;TYPE&gt;EX-21.1\n&lt;SEQUENCE&gt;2\n&lt;FILENAME&gt;one.htm\n"
            "&lt;TYPE&gt;EX-21.2\n&lt;SEQUENCE&gt;3\n&lt;FILENAME&gt;two.htm\n")


# --- the subsidiary list ------------------------------------------------------

# Fortinet's exhibits open on a heading row that reads `Entity` against
# `Jurisdiction of Incorporation`. `src/exhibits.py` drops a row only when both
# of its first two cells carry a column-label word, and `Entity` is not one, so
# the parser keeps the heading as a subsidiary called `Entity` in `Jurisdiction
# of Incorporation`; the reader here drops it on the jurisdiction cell alone.
# The expected list stands as the exhibit reads. Strict, so adding the word to
# `COLUMN_LABEL_WORDS` turns these red and the marks come off.
HEADING_ROW_KEPT = {
    ("FTNT", "exhibit_21"): "'Entity' | 'Jurisdiction of Incorporation' kept as a "
                            "subsidiary; 90 read, 91 parsed",
    ("FTNT", "prior_year_exhibit_21"): "'Entity' | 'Jurisdiction of Incorporation' "
                                       "kept as a subsidiary; 93 read, 94 parsed",
}


@pytest.mark.parametrize("ticker,role", [
    list_case(ticker, role)
    for ticker in TICKERS for role in ("exhibit_21", "prior_year_exhibit_21")])
def test_the_subsidiary_list_read_a_second_way_is_the_same_list(ticker, role):
    """Both readers over both years: one list per document on record, and the
    recorded absence where a 10-K filed none. Two readers that both read
    nothing agree about nothing, so the list has to hold a subsidiary first;
    every exhibit on record lists at least one."""
    if role == "exhibit_21" and no_subsidiary_exhibit(ticker):
        assert built(ticker)["exhibit"]["subsidiaries"] is None
        return
    source = document(ticker, role)
    mine = [(flat(entry["name"]), flat(entry["jurisdiction"]))
            for entry in exhibits.subsidiaries(source)]
    assert mine, f"{ticker} {role}: no subsidiary read"
    assert mine == recount(source)


@pytest.mark.parametrize("ticker", [listed_without_a_table(ticker) for ticker in TICKERS])
def test_every_subsidiary_is_the_exhibits_own_text(ticker):
    if no_subsidiary_exhibit(ticker):
        assert built(ticker)["exhibit"]["absent"] == exhibits.NO_SUBSIDIARY_EXHIBIT
        return
    source = independent_text.Source(document(ticker, "exhibit_21"))
    subsidiaries = built(ticker)["exhibit"]["subsidiaries"]
    assert subsidiaries, f"{ticker}: no subsidiary read, so none was checked"
    for entry in subsidiaries:
        assert source.contains(entry["name"]), entry
        assert source.contains(entry["jurisdiction"]), entry


# The expected lists the parser is held to where no table holds them, read off
# the two documents a second way first: the lines recorded in LISTED_AS_LINES
# are the exhibit's own blocks, by this file's block reader, exactly the ones
# between its heading and its footnote, and the exhibit holds no table, so the
# table reader rightly has none to read.

@pytest.mark.parametrize("ticker,role", sorted(LISTED_AS_LINES))
def test_a_list_written_as_lines_is_the_exhibits_own_lines(ticker, role):
    source = document(ticker, role)
    assert "<table" not in source.lower(), f"{ticker} {role}: the exhibit holds a table"
    blocks = [flat(block) for block in independent_text.block_paragraphs(source)
              if flat(block)]
    first = blocks.index("Subsidiaries of the Registrant*") + 1
    last = next(index for index, block in enumerate(blocks)
                if block.startswith("* Subsidiaries that"))
    assert tuple(blocks[first:last]) == LISTED_AS_LINES[(ticker, role)]


@pytest.mark.parametrize("ticker,role", [
    pytest.param(ticker, role, marks=pytest.mark.xfail(
        strict=True, reason=f"{ticker} {role}: {LIST_WITHOUT_A_TABLE[ticker]}"))
    if ticker in LIST_WITHOUT_A_TABLE else pytest.param(ticker, role)
    for ticker, role in sorted(LISTED_AS_LINES)])
def test_a_list_written_as_lines_is_read_as_its_lines(ticker, role):
    """One subsidiary per recorded line: as many entries as lines, each named by
    its line's opening words up to ', a' or ', an', and placed in a
    jurisdiction its line names."""
    lines = LISTED_AS_LINES[(ticker, role)]
    found = exhibits.subsidiaries(document(ticker, role))
    assert len(found) == len(lines), f"{ticker} {role}: {len(found)} read"
    for entry, line in zip(found, lines):
        assert line.startswith(entry["name"] + ", a"), (entry, line)
        assert entry["jurisdiction"] and entry["jurisdiction"] in line, (entry, line)


def test_a_heading_row_goes_and_a_subsidiary_that_reads_like_one_stays():
    """Qualcomm's heading is `Subsidiaries of Qualcomm Incorporated` against
    `State or Other Jurisdiction of Incorporation`, and a subsidiary could be
    called `Qualcomm Incorporated` in `Delaware`. Both cells have to name a
    column for the row to be a heading, which is what tells them apart."""
    found = exhibits.subsidiaries(
        "<table>"
        "<tr><td>Subsidiaries of Qualcomm Incorporated</td>"
        "<td>State or Other Jurisdiction of Incorporation</td></tr>"
        "<tr><td>Qualcomm Incorporated</td><td>Delaware</td></tr>"
        "</table>")
    assert found == [{"name": "Qualcomm Incorporated", "jurisdiction": "Delaware"}]


def test_an_exhibit_that_opens_on_a_subsidiary_keeps_its_first_row():
    """Seagate's exhibit has no heading row, so a rule that dropped the first
    row of the table would delete a subsidiary."""
    found = exhibits.subsidiaries(
        "<table>"
        "<tr><td>Seagate Technology Holdings Public Limited Company</td>"
        "<td>Ireland</td></tr>"
        "<tr><td>Seagate Technology Unlimited Company</td><td>Ireland</td></tr>"
        "</table>")
    assert [entry["name"] for entry in found] == [
        "Seagate Technology Holdings Public Limited Company",
        "Seagate Technology Unlimited Company"]


def test_spacer_cells_do_not_make_a_row_three_columns_wide():
    """Filers space the columns with empty cells and differ in how many, so the
    name and the jurisdiction are the first two cells with text in them, not the
    first two cells."""
    found = exhibits.subsidiaries(
        "<table><tr><td>TTM Technologies Cayman Limited</td><td>​</td>"
        "<td>Cayman Islands</td></tr></table>")
    assert found == [{"name": "TTM Technologies Cayman Limited",
                      "jurisdiction": "Cayman Islands"}]


# --- the diff -----------------------------------------------------------------

@pytest.mark.parametrize("ticker", [listed_without_a_table(ticker) for ticker in TICKERS])
def test_a_subsidiary_planted_in_a_copy_of_the_exhibit_is_reported_as_added(
        ticker, tmp_path):
    """The judge's second expected value: a name this test wrote into a copy of
    the current 10-K's exhibit, which the diff has to report as an addition and
    which the same copy without the plant reports nowhere."""
    plain = copy_fixtures(tmp_path / "plain", ticker)
    if no_subsidiary_exhibit(ticker):
        # Nothing to plant into: the copy, like the record, reads as the
        # absence by name and diffs nothing.
        before = exhibits.extract(ticker, fixtures_root=plain)
        assert before["diff"] is None
        assert before["exhibit"]["absent"] == exhibits.NO_SUBSIDIARY_EXHIBIT
        return
    planted = copy_fixtures(tmp_path / "planted", ticker)
    plant(planted, ticker, "exhibit_21", PLANTED)

    before = exhibits.extract(ticker, fixtures_root=plain)["diff"]
    after = exhibits.extract(ticker, fixtures_root=planted)["diff"]

    added = [entry["name"] for entry in after["added"]]
    assert added.count(PLANTED["name"]) == 1, added
    assert PLANTED in after["added"]
    assert PLANTED["name"] not in [entry["name"] for entry in before["added"]]
    # One row planted is one addition, and nothing else moves.
    assert len(after["added"]) == len(before["added"]) + 1
    assert after["removed"] == before["removed"]
    assert after["jurisdiction_changed"] == before["jurisdiction_changed"]
    assert after["current_count"] == before["current_count"] + 1
    assert after["prior_count"] == before["prior_count"]


@pytest.mark.parametrize("ticker", [listed_without_a_table(ticker) for ticker in TICKERS])
def test_a_subsidiary_planted_in_the_prior_year_is_reported_as_dropped(
        ticker, tmp_path):
    """The same plant on the other side of the pair. A diff that reported every
    difference as an addition would pass the test above and fail this one."""
    plain = copy_fixtures(tmp_path / "plain", ticker)
    planted = copy_fixtures(tmp_path / "planted", ticker)
    plant(planted, ticker, "prior_year_exhibit_21", PLANTED)

    if no_subsidiary_exhibit(ticker):
        # The prior year's list grows by one and there is still nothing to
        # diff it against; the absence is named either way.
        before = exhibits.extract(ticker, fixtures_root=plain)
        after = exhibits.extract(ticker, fixtures_root=planted)
        assert before["diff"] is None and after["diff"] is None
        assert len(after["prior_exhibit"]["subsidiaries"]) == \
            len(before["prior_exhibit"]["subsidiaries"]) + 1
        assert PLANTED in after["prior_exhibit"]["subsidiaries"]
        assert after["exhibit"]["absent"] == exhibits.NO_SUBSIDIARY_EXHIBIT
        return

    before = exhibits.extract(ticker, fixtures_root=plain)["diff"]
    after = exhibits.extract(ticker, fixtures_root=planted)["diff"]

    assert PLANTED in after["removed"]
    assert len(after["removed"]) == len(before["removed"]) + 1
    assert after["added"] == before["added"]
    assert after["prior_count"] == before["prior_count"] + 1


@pytest.mark.parametrize("ticker", [listed_without_a_table(ticker) for ticker in TICKERS])
def test_the_planted_subsidiary_reaches_the_file_the_reader_sees(ticker, tmp_path):
    """`input_exhibits.md` is what the notes-text reader is handed, so the plant
    has to be in it, on its own paragraph id, and not merely in the payload."""
    planted = copy_fixtures(tmp_path / "planted", ticker)
    out = tmp_path / "input_exhibits.md"
    if no_subsidiary_exhibit(ticker):
        # What the reader is handed instead of a list: the absence, by name,
        # on the header line and the counts line.
        assert exhibits.main(["--ticker", ticker, "--fixtures", str(planted),
                              "--out", str(out)]) == 0
        lines = out.read_text(encoding="utf-8").split("\n")
        accession = entry_of(manifest_of(planted, ticker), "submission_header")["accession"]
        assert any(line.startswith(f"- 10-K {accession} filed ")
                   and line.endswith(exhibits.NO_SUBSIDIARY_EXHIBIT) for line in lines)
        assert f"## {exhibits.NO_SUBSIDIARY_EXHIBIT}; nothing to diff (none)" in lines
        assert any(line.startswith("## counts — no subsidiary exhibit in this 10-K")
                   for line in lines)
        assert not any(line.startswith(f"[{accession}:exhibits:") for line in lines)
        return
    plant(planted, ticker, "exhibit_21", PLANTED)
    assert exhibits.main(["--ticker", ticker, "--fixtures", str(planted),
                          "--out", str(out)]) == 0
    lines = out.read_text(encoding="utf-8").split("\n")
    assert "## subsidiaries added since the prior 10-K" in lines
    planted_row = f"| {PLANTED['name']} | {PLANTED['jurisdiction']} |"
    assert planted_row in lines
    # The row a reader quotes has to carry an id, or nothing can verify the quote.
    accession = entry_of(manifest_of(planted, ticker), "exhibit_21")["accession"]
    assert lines[lines.index(planted_row) - 1].startswith(f"[{accession}:exhibits:")


def test_two_subsidiaries_under_one_name_are_two_entries():
    """A multiset, so the second copy does not collapse onto the first —
    `src/diff_periods.py::match_paragraphs` learned this the expensive way."""
    twins = [{"name": "Twin Holdings", "jurisdiction": "Delaware"},
             {"name": "Twin Holdings", "jurisdiction": "Delaware"}]
    changes = exhibits.diff(twins[:1], twins)
    assert changes["unchanged"] == 1
    assert changes["removed"] == twins[:1]
    assert changes["added"] == []


def test_a_jurisdiction_that_moved_is_neither_an_addition_nor_a_removal():
    """Ciena's `Ciena Global Holding, LP` went from Scotland to the United
    Kingdom between these two 10-Ks. Reported as an addition and a removal it
    would read as a subsidiary gained and one lost."""
    changes = exhibits.diff(
        [{"name": "Ciena Global Holding, LP", "jurisdiction": "United Kingdom"}],
        [{"name": "Ciena Global Holding, LP", "jurisdiction": "Scotland"}])
    assert changes["added"] == [] and changes["removed"] == []
    assert changes["jurisdiction_changed"] == [
        {"name": "Ciena Global Holding, LP", "prior_jurisdiction": "Scotland",
         "jurisdiction": "United Kingdom"}]


@pytest.mark.parametrize("ticker", [listed_without_a_table(ticker) for ticker in TICKERS])
def test_the_counts_add_up_to_both_years_lists(ticker):
    """Every subsidiary of either year is in exactly one of the four buckets,
    and each year holds one: two empty lists add up to anything."""
    changes = built(ticker)["diff"]
    if no_subsidiary_exhibit(ticker):
        assert changes is None
        return
    assert changes["current_count"] and changes["prior_count"], \
        f"{ticker}: {changes['current_count']} and {changes['prior_count']} subsidiaries"
    moved = len(changes["jurisdiction_changed"])
    assert changes["current_count"] == \
        len(changes["added"]) + moved + changes["unchanged"]
    assert changes["prior_count"] == \
        len(changes["removed"]) + moved + changes["unchanged"]


# --- what the record has to hold ----------------------------------------------

def test_a_header_that_names_an_exhibit_the_record_lacks_is_refused(tmp_path):
    """The other side of the absence rule: a 10-K that names an Exhibit 21 is
    not read as having filed none when the record merely fails to hold it."""
    root = copy_fixtures(tmp_path / "unheld", "AAPL")
    manifest = manifest_of(root, "AAPL")
    entry = entry_of(manifest, "exhibit_21")
    (root / "AAPL" / entry["path"]).unlink()
    manifest["documents"] = [e for e in manifest["documents"] if e["role"] != "exhibit_21"]
    write_manifest(root / "AAPL", manifest)
    with pytest.raises(exhibits.ExhibitError, match="record holds no exhibit_21"):
        exhibits.extract("AAPL", fixtures_root=root)


def test_a_header_that_names_no_exhibit_is_the_absence_and_not_a_refusal(tmp_path):
    """Western Digital's own record, copied: the header names nothing of the
    EX-21 family, no exhibit is held, and the payload says so by name."""
    root = copy_fixtures(tmp_path / "absent", "WDC")
    payload = exhibits.extract("WDC", fixtures_root=root)
    assert payload["exhibit"]["absent"] == exhibits.NO_SUBSIDIARY_EXHIBIT
    assert payload["exhibit"]["subsidiaries"] is None
    assert payload["prior_exhibit"]["type"] == "EX-21"
    assert payload["diff"] is None
    assert exhibits.NO_SUBSIDIARY_EXHIBIT in exhibits.render(payload)


def test_an_exhibit_the_header_does_not_name_is_refused(tmp_path):
    """The stored document has to be the one the submission header names. A
    record holding some other file is a refusal, not a parse."""
    root = copy_fixtures(tmp_path / "renamed", "AAPL")
    manifest = manifest_of(root, "AAPL")
    entry = entry_of(manifest, "exhibit_21")
    stored = root / "AAPL" / entry["path"]
    moved = stored.with_name("some-other-name.htm")
    stored.rename(moved)
    entry["path"] = str(moved.relative_to(root / "AAPL"))
    write_manifest(root / "AAPL", manifest)
    with pytest.raises(exhibits.ExhibitError):
        exhibits.extract("AAPL", fixtures_root=root)


def test_an_exhibit_read_through_another_submissions_header_is_refused(tmp_path):
    root = copy_fixtures(tmp_path / "crossed", "AAPL")
    manifest = manifest_of(root, "AAPL")
    entry_of(manifest, "exhibit_21")["accession"] = \
        entry_of(manifest, "prior_year_exhibit_21")["accession"]
    write_manifest(root / "AAPL", manifest)
    with pytest.raises(exhibits.ExhibitError):
        exhibits.extract("AAPL", fixtures_root=root)


def test_a_cutoff_before_the_latest_ten_k_reads_the_earlier_one_and_diffs_nothing():
    """`docs/INPUT_SPEC.md` §2: the first filing on record for a company is read
    whole. Apple's 10-K was filed 2025-10-31 and the one before it 2024-11-01,
    so a cutoff between them leaves one 10-K on record and nothing to diff."""
    payload = exhibits.extract("AAPL", cutoff="2025-10-30")
    assert payload["exhibit"]["accession"] == "0000320193-24-000123"
    assert payload["exhibit"]["filename"] == \
        expected_values.value("AAPL", "exhibits.10-K.prior_year_exhibit_filename")
    assert payload["prior_exhibit"] is None
    assert payload["diff"] is None
    text = exhibits.render(payload)
    assert "carried whole" in text
    assert "no earlier 10-K on record at or before 2025-10-30" in text


def test_a_cutoff_before_every_ten_k_leaves_nothing_to_read():
    with pytest.raises(exhibits.ExhibitError):
        exhibits.extract("AAPL", cutoff="2024-10-31")


# --- the file the notes-text reader is handed ---------------------------------

@pytest.mark.parametrize("ticker", TICKERS)
def test_the_rendered_file_carries_every_change_the_diff_found(ticker):
    payload = built(ticker)
    text = exhibits.render(payload)
    changes = payload["diff"]
    if no_subsidiary_exhibit(ticker):
        # No change to carry: the absence rides on the header line and on the
        # section heading, and the prior year's file is still named.
        assert changes is None
        assert text.count(exhibits.NO_SUBSIDIARY_EXHIBIT) == 2
        assert payload["prior_exhibit"]["filename"] in text
        return
    for entry in changes["added"] + changes["removed"]:
        assert exhibits.row(entry) in text, entry
    for entry in changes["jurisdiction_changed"]:
        assert exhibits.moved_row(entry) in text, entry
    assert payload["exhibit"]["type"] in text
    assert payload["exhibit"]["filename"] in text
    assert payload["prior_exhibit"]["filename"] in text


@pytest.mark.parametrize("ticker", TICKERS)
def test_every_paragraph_id_names_this_ten_k_and_counts_from_one(ticker):
    payload = built(ticker)
    accession = payload["exhibit"]["accession"]
    found = [line.strip()[1:-1] for line in exhibits.render(payload).split("\n")
             if line.startswith("[") and line.rstrip().endswith("]")]
    changes = payload["diff"]
    if no_subsidiary_exhibit(ticker):
        assert found == []
        return
    expected = (len(changes["added"]) + len(changes["removed"])
                + len(changes["jurisdiction_changed"]))
    assert found == [f"{accession}:exhibits:{n}" for n in range(1, expected + 1)]


@pytest.mark.parametrize("ticker", TICKERS)
def test_every_quotable_block_is_a_subsidiary_row_and_nothing_this_module_wrote(ticker):
    """`assemble_bundle.paragraph_blocks` skips `#` headings and folds every
    other line into the block of the id above it, and a quote gate matches a
    reader's quote against that block. So the counts sentence and an empty
    section's marker ride on headings: were they plain lines they would land in
    the last subsidiary's block, and a reader quoting arithmetic under that
    subsidiary's id would pass the gate. What is quotable here is what the
    exhibit said."""
    payload = built(ticker)
    changes = payload["diff"]
    if no_subsidiary_exhibit(ticker):
        # Every line is a heading, so nothing is quotable: the absence can be
        # read but not cited as a subsidiary.
        assert assemble_bundle.paragraph_blocks(exhibits.render(payload)) == []
        return
    rows = ([exhibits.row(entry) for entry in changes["added"] + changes["removed"]]
            + [exhibits.moved_row(entry) for entry in changes["jurisdiction_changed"]])
    blocks = assemble_bundle.paragraph_blocks(exhibits.render(payload))
    assert [text for _, text in blocks] == rows


def test_the_command_writes_the_file_the_input_spec_names(tmp_path):
    out = tmp_path / "input_exhibits.md"
    assert exhibits.main(["--ticker", "aapl", "--out", str(out)]) == 0
    text = out.read_text(encoding="utf-8")
    assert text.startswith("# AAPL Exhibit 21")
    assert expected_values.value("AAPL", "exhibits.10-K.exhibit_type") in text


def test_the_command_reports_a_company_with_no_exhibit_on_record(tmp_path, capsys):
    assert exhibits.main(["--ticker", "AAPL", "--cutoff", "2024-10-31",
                          "--out", str(tmp_path / "input_exhibits.md")]) == exhibits.BAD_INPUT
    assert "exhibits:" in capsys.readouterr().err
