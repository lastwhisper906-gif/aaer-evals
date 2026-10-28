"""The SEC staff's comment letters and the company's responses reach the notes
reader by the day EDGAR made them public, never by a date printed on them.

The pair is ADTRAN's, a company of the universe. Read by eye from EDGAR on
2026-10-28 (the documents are committed under `tests/fixtures/event_filings/`
with their addresses and sha256 in `record.json`; the index rows are the
committed `tests/fixtures/ADTN/submissions.json`, EDGAR's submissions index for
CIK 0000926282):

* the staff's letter, UPLOAD 0000000000-24-010922: printed "September 25, 2024"
  (its text copy `filename2.txt`); EDGAR `filingDate` 2024-09-26 (the index
  row); made public 2024-12-04 (its header's first line,
  `<SEC-HEADER>0000000000-24-010922.hdr.sgml : 20241204`, under
  `<PRIVATE-TO-PUBLIC>`);
* the company's response, CORRESP 0000950170-24-109789: printed "September 27,
  2024", answering "the comment letter dated September 25, 2024"; `filingDate`
  2024-09-27; made public 2024-12-04;
* the staff's closing letter, UPLOAD 0000000000-24-012258, printed "November 4,
  2024", `filingDate` 2024-11-04, made public 2024-12-04; and a second
  conversation, on a registration statement, UPLOAD 0000000000-24-012928
  (`filingDate` 2024-11-21) and CORRESP 0001193125-24-264351 (2024-11-22), both
  made public 2024-12-27.

ADTRAN's 10-Q of 2024-11-12 (0000950170-24-125685) was filed after the first
three letters were and before any of them was public; its 10-K of 2025-03-03
(0000950170-25-031056) is the first periodic report after both releases.

The brief this was built to says the date that decides is EDGAR's `filingDate`,
"the release date". For these forms it is not: `filingDate` is the day a letter
was filed in private, and the header's dissemination day is the release. The
tests hold the cutoff to both -- never the printed date, never before the
`filingDate`, and never before the release.
"""

from __future__ import annotations

import json

import pytest

from src import cutoff_guard, fetch_fixtures, parse_8k
from tests import event_store
from tests.event_store import RecordedEdgar, fetched, manifest_rows, recorded, section

TICKER = "ADTN"
QUARTER = "0000950170-24-125685"       # 10-Q filed 2024-11-12
ANNUAL = "0000950170-25-031056"        # 10-K filed 2025-03-03
STAFF = "0000000000-24-010922"         # printed September 25, 2024; filed 2024-09-26
RESPONSE = "0000950170-24-109789"      # printed September 27, 2024; filed 2024-09-27
CLOSING = "0000000000-24-012258"       # filed 2024-11-04
SHELF = "0000000000-24-012928"         # filed 2024-11-21
SHELF_RESPONSE = "0001193125-24-264351"  # filed 2024-11-22
FIRST_CONVERSATION = (STAFF, CLOSING, RESPONSE)


def row(root, accession, role):
    return next(entry for entry in manifest_rows(root, TICKER)
                if entry["accession"] == accession and entry["role"] == role)


def folded(text: str) -> str:
    return " ".join(text.split())


def test_the_pair_was_printed_on_one_day_and_filed_on_another():
    """The source, read by eye: what the test below holds the cutoff against."""
    staff = recorded(STAFF, "filename2.txt").decode("utf-8")
    assert "September 25, 2024" in staff
    assert event_store.row_of(TICKER, STAFF)["filingDate"] == "2024-09-26"
    response = recorded(RESPONSE, "filename1.htm").decode("utf-8")
    assert "the comment letter dated September 25, 2024" in response
    assert recorded(STAFF, f"{STAFF}.hdr.sgml").startswith(
        f"<SEC-HEADER>{STAFF}.hdr.sgml : 20241204".encode())


def test_the_cutoff_reads_edgars_filing_date_and_the_release_never_the_printed_date(tmp_path):
    root, problems, _ = fetched(tmp_path, TICKER, ANNUAL)
    assert problems == []
    letter = row(root, STAFF, fetch_fixtures.STAFF_LETTER)
    assert (letter["form"], letter["filing_date"], letter["released"]) == \
        ("UPLOAD", "2024-09-26", "2024-12-04")
    assert letter["acceptance_datetime"] == "2024-09-26T07:36:09-04:00"
    path = root / TICKER / letter["path"]
    # the printed date: refused by EDGAR's filing date, the day after it
    with pytest.raises(cutoff_guard.CutoffViolationError) as printed:
        cutoff_guard.load_bytes(path, "2024-09-25", fixtures_root=root)
    assert not isinstance(printed.value, cutoff_guard.NotYetPublicError)
    assert printed.value.doc_date.isoformat() == "2024-09-26"
    # filed, and still private: refused by the release until its day, which the
    # date rule allows as it allows a filing date; which letters of the trigger's
    # own day stood is decided where they are picked (the test after the next)
    for cutoff in ("2024-09-26", "2024-11-12", "2024-12-03"):
        with pytest.raises(cutoff_guard.NotYetPublicError) as private:
            cutoff_guard.load_bytes(path, cutoff, fixtures_root=root)
        assert private.value.doc_date.isoformat() == "2024-12-04"
    assert cutoff_guard.load_bytes(path, "2024-12-04", fixtures_root=root) == \
        recorded(STAFF, "filename2.txt")
    # the header, EDGAR's record of the release, is dated by its own first line
    header = row(root, STAFF, fetch_fixtures.RELEASE_HEADER)
    assert (header["filing_date"], header["released"], header["edgar_filing_date"]) == \
        ("2024-12-04", "2024-12-04", "2024-09-26")


def test_letters_filed_before_a_report_and_made_public_after_it_never_reach_it(tmp_path):
    """The 10-Q of 2024-11-12: three letters were filed and none was public."""
    root, problems, edgar = fetched(tmp_path, TICKER, QUARTER)
    assert problems == []
    held = {entry["accession"] for entry in manifest_rows(root, TICKER)}
    assert not held & set(FIRST_CONVERSATION)
    # each letter's header was read to learn its release, and nothing more
    assert sorted(edgar.asked) == sorted(
        f"https://www.sec.gov/Archives/edgar/data/926282/{accession.replace('-', '')}/"
        f"{accession}.hdr.sgml" for accession in FIRST_CONVERSATION)
    events, text = section(root, TICKER, QUARTER)
    assert events["state"] == "fetched"
    assert events["carried"] == []
    for accession in FIRST_CONVERSATION:
        assert accession not in text
    assert parse_8k.NOTHING_IN_THE_WINDOW in text


def test_the_first_report_after_the_release_carries_the_whole_conversation(tmp_path):
    root, problems, _ = fetched(tmp_path, TICKER, ANNUAL)
    assert problems == []
    events, text = section(root, TICKER, ANNUAL)
    assert events["previous"]["accession"] == QUARTER
    carried = [(entry["accession"], entry["role"], entry["filing_date"], entry["released"])
               for entry in events["carried"]]
    assert carried == [
        (STAFF, "staff_letter", "2024-09-26", "2024-12-04"),
        (CLOSING, "staff_letter", "2024-11-04", "2024-12-04"),
        (RESPONSE, "company_response", "2024-09-27", "2024-12-04"),
        (SHELF, "staff_letter", "2024-11-21", "2024-12-27"),
        (SHELF_RESPONSE, "company_response", "2024-11-22", "2024-12-27"),
    ]
    assert (f"### UPLOAD {STAFF}, a letter from the SEC staff, filed 2024-09-26 and made "
            "public 2024-12-04, verbatim") in text
    assert (f"### CORRESP {RESPONSE}, the company's letter to the SEC staff, filed "
            "2024-09-27 and made public 2024-12-04, verbatim") in text
    staff = next(entry for entry in events["carried"] if entry["accession"] == STAFF)
    # the comment, read by eye in filename2.txt, line breaks as the text copy has them
    assert any(paragraph.startswith(
        "1.     From the disclosure incorporated by reference from page 45 of the\n"
        "Definitive Proxy\n       Statement filed on March 27, 2024, it appears that you "
        "have not provided") for paragraph in staff["paragraphs"])
    assert staff["paragraph_ids"] == [f"{STAFF}:staff_letter:{number}"
                                      for number in range(1, len(staff["paragraphs"]) + 1)]
    for paragraph in staff["paragraphs"]:
        assert paragraph in recorded(STAFF, "filename2.txt").decode("utf-8")
    response = next(entry for entry in events["carried"] if entry["accession"] == RESPONSE)
    assert ("Response: The Company respectfully acknowledges the Staff’s comment. The "
            "Company has noted for future filings that disclosure about the Company’s "
            "recovery analysis should also be included in an Interactive Data File in "
            "accordance with Rule 405 of Regulation S-T and the EDGAR Filer Manual."
            in [folded(paragraph) for paragraph in response["paragraphs"]])
    for identifier in staff["paragraph_ids"] + response["paragraph_ids"]:
        assert f"[{identifier}]" in text


def test_a_letter_made_public_on_the_triggers_own_day_is_not_shown_to_stand():
    """A release is a day with no time: on the trigger's day it is not shown to
    come first, and the day after it is."""
    previous = {"accessionNumber": QUARTER, "filingDate": "2024-11-12"}
    on_the_day = {"accessionNumber": "0000950170-24-999999", "filingDate": "2024-12-04"}
    after = dict(on_the_day, filingDate="2024-12-05")
    assert not fetch_fixtures.public_in_window("2024-12-04", previous, on_the_day)
    assert fetch_fixtures.public_in_window("2024-12-04", previous, after)
    # and a release on the previous report's own day belongs to the later window
    assert fetch_fixtures.public_in_window("2024-11-12", previous, after)


def test_a_letter_with_no_release_on_record_is_refused_by_the_gate(tmp_path):
    root, _, _ = fetched(tmp_path, TICKER, ANNUAL)
    path = root / TICKER / "manifest.json"
    manifest = json.loads(path.read_text())
    for entry in manifest["documents"]:
        if entry["accession"] == STAFF and entry["role"] == "staff_letter":
            del entry["released"]
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    letter = row(root, STAFF, fetch_fixtures.STAFF_LETTER)
    with pytest.raises(cutoff_guard.CutoffGuardError, match="no release date on record"):
        cutoff_guard.load_bytes(root / TICKER / letter["path"], "2025-03-03",
                                fixtures_root=root)
    with pytest.raises(cutoff_guard.CutoffGuardError, match="no release date on record"):
        section(root, TICKER, ANNUAL)


class PdfOnly(RecordedEdgar):
    """The record, except that the closing letter's header names its PDF alone:
    a planted listing, as EDGAR serves for letters before it kept text copies."""

    def get(self, url):
        if url.endswith(f"{CLOSING}-index-headers.html"):
            self.asked.append(url)
            return b"<TYPE>LETTER\n<SEQUENCE>1\n<FILENAME>filename1.pdf\n"
        return super().get(url)


def test_a_letter_held_as_a_pdf_only_is_named_and_not_carried(tmp_path):
    root, problems, _ = fetched(tmp_path, TICKER, ANNUAL, edgar=PdfOnly())
    assert problems == []
    roles = {entry["role"] for entry in manifest_rows(root, TICKER)
             if entry["accession"] == CLOSING}
    assert roles == {"release_header"}
    events, text = section(root, TICKER, ANNUAL)
    assert CLOSING not in {entry["accession"] for entry in events["carried"]}
    assert (f"### not carried: UPLOAD {CLOSING} filed 2024-11-04 and made public "
            "2024-12-04: EDGAR holds the letter as a PDF with no text copy") in text


def test_every_letter_reaches_the_reader_through_the_gate(tmp_path, monkeypatch):
    root, _, _ = fetched(tmp_path, TICKER, ANNUAL)
    with cutoff_guard.recording() as seen:
        events, _ = section(root, TICKER, ANNUAL)
    texts = {(root / TICKER / entry["path"]).resolve()
             for entry in manifest_rows(root, TICKER)
             if entry["role"] in ("staff_letter", "company_response")}
    assert len(texts) == 5
    assert set(seen) == texts | {(root / TICKER / "submissions.json").resolve()}

    def refused(path, cutoff, **_):
        raise cutoff_guard.CutoffGuardError(f"the gate refused {path}")

    monkeypatch.setattr(cutoff_guard, "load_bytes", refused)
    with pytest.raises(cutoff_guard.CutoffGuardError, match="the gate refused"):
        section(root, TICKER, ANNUAL)


def test_a_store_holding_a_letter_not_yet_public_at_the_trigger_is_refused(tmp_path):
    """A store built under the filing-date rule would hold the first conversation
    for the 10-Q of 2024-11-12; the store's own check names it."""
    root, _, _ = fetched(tmp_path, TICKER, ANNUAL)
    trigger = event_store.row_of(TICKER, QUARTER)
    known = frozenset(one["accessionNumber"] for one in fetch_fixtures.known_at(
        event_store.index_rows(TICKER), trigger))
    found = fetch_fixtures.held_to_the_trigger(root, TICKER, trigger, known)
    assert any(STAFF in line and "made public 2024-12-04" in line for line in found)
    assert any(SHELF in line and "did not stand" in line for line in found)
