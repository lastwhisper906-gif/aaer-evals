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
from tests.event_store import RECORD, RecordedEdgar, fetched, manifest_rows, recorded, section

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
    # filed, and still private: refused by the release through the release day
    # itself, since a release is a day with no time and cannot show the letter
    # was public before a report accepted that day
    for cutoff in ("2024-09-26", "2024-11-12", "2024-12-03", "2024-12-04"):
        with pytest.raises(cutoff_guard.NotYetPublicError) as private:
            cutoff_guard.load_bytes(path, cutoff, fixtures_root=root)
        assert private.value.doc_date.isoformat() == "2024-12-04"
    assert cutoff_guard.load_bytes(path, "2024-12-05", fixtures_root=root) == \
        recorded(STAFF, "filename2.txt")
    # the release is recorded off the header's first line, with the header's
    # address and hash; the header itself is not a document of the store
    release = fetch_fixtures.load_manifest(root / TICKER)["event_filings"]["releases"][STAFF]
    assert (release["form"], release["filing_date"], release["released"]) == \
        ("UPLOAD", "2024-09-26", "2024-12-04")
    assert release["header_sha256"] == RECORD["files"][f"{STAFF}/{STAFF}.hdr.sgml"]["sha256"]
    assert not [entry for entry in manifest_rows(root, TICKER) if entry["role"] == "release_header"]


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
    # an empty window prints nothing, so the file is the one a store fetched
    # without event filings gives; the manifest's record says which it was, and
    # says what was looked at
    assert text == ""
    record = parse_8k.window_record(events)
    assert record["state"] == "fetched" and record["carried"] == []
    assert ("no comment letter filed in the 2 years before the window opened was made "
            "public in this window") in record["note"]


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
    # a window that carries something says what was looked for
    assert ("### comment letters: those filed in the 2 years before the window opened were "
            "looked for, and are carried when made public inside it") in text
    assert "note" not in parse_8k.window_record(events)
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


# The window of the 10-Q of 2024-11-12 opens at the 10-Q of 2024-08-09
# (0000950170-24-094602, the committed index), so the lookback floor is 2022-08-09:
# a letter filed the day before it is never looked for, one filed the day after is.
PLANTED_OLD = {"accessionNumber": "0000000000-22-900001", "filingDate": "2022-08-08",
               "reportDate": "", "form": "UPLOAD", "items": "", "primaryDocument": "filename1.pdf",
               "primaryDocDescription": "", "acceptanceDateTime": "2022-08-08T14:00:00.000Z"}
PLANTED_INSIDE = dict(PLANTED_OLD, accessionNumber="0000000000-22-900002", filingDate="2022-08-10",
                      acceptanceDateTime="2022-08-10T14:00:00.000Z")


class ServesThePlantedHeader(RecordedEdgar):
    def get(self, url):
        if url.endswith(f"{PLANTED_INSIDE['accessionNumber']}.hdr.sgml"):
            self.asked.append(url)
            return (f"<SEC-HEADER>{PLANTED_INSIDE['accessionNumber']}.hdr.sgml : 20221001\n"
                    "<PRIVATE-TO-PUBLIC>\n").encode()
        return super().get(url)


def test_a_letter_filed_before_the_lookback_is_never_looked_for_and_the_line_says_so(tmp_path):
    root, problems, edgar = fetched(tmp_path, TICKER, QUARTER, edgar=ServesThePlantedHeader(),
                                    extra_rows=[PLANTED_OLD, PLANTED_INSIDE])
    assert problems == []
    asked = [url.rsplit("/", 1)[1] for url in edgar.asked]
    assert f"{PLANTED_OLD['accessionNumber']}.hdr.sgml" not in asked
    assert f"{PLANTED_INSIDE['accessionNumber']}.hdr.sgml" in asked
    record = fetch_fixtures.load_manifest(root / TICKER)["event_filings"]
    assert (record["letter_lookback_years"], record["letters_filed_after"]) == (2, "2022-08-09")
    assert PLANTED_OLD["accessionNumber"] not in record["releases"]
    # made public 2022-10-01, before the window opened: recorded, not carried
    assert record["releases"][PLANTED_INSIDE["accessionNumber"]]["released"] == "2022-10-01"
    events, text = section(root, TICKER, QUARTER)
    assert events["carried"] == []
    assert "no comment letter filed in the 2 years before the window opened" in \
        parse_8k.window_record(events)["note"]


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
    assert not [entry for entry in manifest_rows(root, TICKER) if entry["accession"] == CLOSING]
    releases = fetch_fixtures.load_manifest(root / TICKER)["event_filings"]["releases"]
    assert releases[CLOSING]["released"] == "2024-12-04"
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


# --- the edges of each rule, one test per clause -----------------------------
#
# Each test below plants the one row or the one header that sits on a rule's
# boundary: a release on the cutoff's own day, a letter filed on the lookback
# floor's own day, a row with no release at all.

def set_release(root, accession, released):
    """Rewrite the store's rows of one letter: `released` set, or removed for None."""
    path = root / TICKER / "manifest.json"
    manifest = json.loads(path.read_text())
    for entry in manifest["documents"]:
        if entry["accession"] == accession and entry["role"] in ("staff_letter",
                                                                 "company_response"):
            if released is None:
                entry.pop("released", None)
            else:
                entry["released"] = released
    path.write_text(json.dumps(manifest, indent=2) + "\n")


def test_the_bundles_record_keeps_a_letter_from_the_day_after_its_release(tmp_path):
    """The staff letter was filed 2024-09-26 and made public 2024-12-04: a bundle
    whose cutoff is the release day does not list it, one a day later does."""
    from src import assemble_bundle
    root, _, _ = fetched(tmp_path, TICKER, ANNUAL)
    on_the_day = assemble_bundle.documents_on_record(TICKER, "2024-12-04", root)
    assert STAFF not in {entry["accession"] for entry in on_the_day}
    assert not [entry for entry in on_the_day
                if entry["role"] in ("staff_letter", "company_response")]
    after = assemble_bundle.documents_on_record(TICKER, "2024-12-05", root)
    assert {entry["accession"] for entry in after
            if entry["role"] in ("staff_letter", "company_response")} == set(FIRST_CONVERSATION)
    [letter] = [entry for entry in after if entry["accession"] == STAFF]
    assert (letter["filing_date"], letter["released"]) == ("2024-09-26", "2024-12-04")


def test_the_bundles_record_refuses_a_letter_with_no_release(tmp_path):
    """An absent release is not an early one: the row is refused, not listed."""
    from src import assemble_bundle
    root, _, _ = fetched(tmp_path, TICKER, ANNUAL)
    set_release(root, STAFF, None)
    with pytest.raises(cutoff_guard.CutoffGuardError, match="UPLOAD with no release on record"):
        assemble_bundle.documents_on_record(TICKER, "2025-03-03", root)


def held_problems(root, accession):
    """What the store's own check says of the 10-K's store, about one letter."""
    trigger = event_store.row_of(TICKER, ANNUAL)        # filed 2025-03-03
    known = frozenset(one["accessionNumber"] for one in fetch_fixtures.known_at(
        event_store.index_rows(TICKER), trigger))
    return [line for line in fetch_fixtures.held_to_the_trigger(root, TICKER, trigger, known)
            if accession in line]


def test_the_stores_check_refuses_a_letter_released_on_the_triggers_own_day(tmp_path):
    """The 10-K was filed 2025-03-03. As fetched the store passes; a letter row
    saying it was made public that day is named, the day before is not, and a
    row with no release is named for that."""
    root, _, _ = fetched(tmp_path, TICKER, ANNUAL)
    assert held_problems(root, STAFF) == []
    set_release(root, STAFF, "2025-03-03")
    [line] = held_problems(root, STAFF)
    assert "was made public 2025-03-03, not before" in line and ANNUAL in line
    set_release(root, STAFF, "2025-03-02")
    assert held_problems(root, STAFF) == []
    set_release(root, STAFF, None)
    [line] = held_problems(root, STAFF)
    assert "is a UPLOAD with no release on record" in line


# Two planted staff letters filed 2025-02-03, inside the 10-K's lookback, one
# made public on the 10-K's own day (2025-03-03) and one the day before. EDGAR
# is planted to hold each as a PDF only, so no text is asked for.
ON_THE_DAY = dict(PLANTED_OLD, accessionNumber="0000000000-25-900001", filingDate="2025-02-03",
                  acceptanceDateTime="2025-02-03T14:00:00.000Z")
THE_DAY_BEFORE = dict(ON_THE_DAY, accessionNumber="0000000000-25-900002")
# and one filed on the lookback floor's own day for the 10-Q of 2024-11-12
ON_THE_FLOOR = dict(PLANTED_OLD, accessionNumber="0000000000-22-900003", filingDate="2022-08-09",
                    acceptanceDateTime="2022-08-09T14:00:00.000Z")


class PlantedLetters(RecordedEdgar):
    """The record, and for each planted accession a header stamped with its day
    and a listing that names a PDF alone."""

    def __init__(self, stamps: dict[str, str]) -> None:
        super().__init__()
        self.stamps = stamps

    def get(self, url):
        for accession, stamp in self.stamps.items():
            if url.endswith(f"{accession}.hdr.sgml"):
                self.asked.append(url)
                return f"<SEC-HEADER>{accession}.hdr.sgml : {stamp}\n<PRIVATE-TO-PUBLIC>\n".encode()
            if url.endswith(f"{accession}-index-headers.html"):
                self.asked.append(url)
                return b"<TYPE>LETTER\n<SEQUENCE>1\n<FILENAME>filename1.pdf\n"
        return super().get(url)


def test_the_fetch_keeps_no_release_of_a_letter_made_public_on_the_triggers_own_day(tmp_path):
    edgar = PlantedLetters({ON_THE_DAY["accessionNumber"]: "20250303",
                            THE_DAY_BEFORE["accessionNumber"]: "20250302"})
    root, problems, _ = fetched(tmp_path, TICKER, ANNUAL, edgar=edgar,
                                extra_rows=[ON_THE_DAY, THE_DAY_BEFORE])
    assert problems == []
    releases = fetch_fixtures.load_manifest(root / TICKER)["event_filings"]["releases"]
    assert ON_THE_DAY["accessionNumber"] not in releases
    assert releases[THE_DAY_BEFORE["accessionNumber"]]["released"] == "2025-03-02"
    # the header of each was read; only the one public in time had its listing read
    asked = [url.rsplit("/", 1)[1] for url in edgar.asked]
    assert f"{ON_THE_DAY['accessionNumber']}.hdr.sgml" in asked
    assert f"{ON_THE_DAY['accessionNumber']}-index-headers.html" not in asked
    assert f"{THE_DAY_BEFORE['accessionNumber']}-index-headers.html" in asked
    events, text = section(root, TICKER, ANNUAL)
    assert ON_THE_DAY["accessionNumber"] not in text
    assert (f"### not carried: UPLOAD {THE_DAY_BEFORE['accessionNumber']} filed 2025-02-03 "
            "and made public 2025-03-02") in text


def test_a_letter_filed_on_the_lookback_floors_own_day_is_never_looked_for(tmp_path):
    """The floor for the 10-Q of 2024-11-12 is 2022-08-09 (`letters_filed_after`):
    a letter filed that day is outside, the one filed 2022-08-10 inside."""
    edgar = ServesThePlantedHeader()
    root, problems, _ = fetched(tmp_path, TICKER, QUARTER, edgar=edgar,
                                extra_rows=[ON_THE_FLOOR, PLANTED_INSIDE])
    assert problems == []
    asked = [url.rsplit("/", 1)[1] for url in edgar.asked]
    assert not [name for name in asked if ON_THE_FLOOR["accessionNumber"] in name]
    assert f"{PLANTED_INSIDE['accessionNumber']}.hdr.sgml" in asked
    record = fetch_fixtures.load_manifest(root / TICKER)["event_filings"]
    assert record["letters_filed_after"] == "2022-08-09"
    assert ON_THE_FLOOR["accessionNumber"] not in record["releases"]
    window = fetch_fixtures.event_window(
        event_store.index_rows(TICKER) + [ON_THE_FLOOR, PLANTED_INSIDE],
        event_store.row_of(TICKER, QUARTER))
    planted = [one["accessionNumber"] for one in window["letters"]
               if one["accessionNumber"].startswith("0000000000-22-9")]
    assert planted == [PLANTED_INSIDE["accessionNumber"]]


def test_a_store_fetched_for_another_window_opening_is_refused(tmp_path):
    """The 10-K's window opens after the 10-Q of 2024-11-12, by the index. A
    record that says the event filings were fetched for a window opening after
    some other report does not describe this window, and nothing is read."""
    root, _, _ = fetched(tmp_path, TICKER, ANNUAL)
    path = root / TICKER / "manifest.json"
    manifest = json.loads(path.read_text())
    assert manifest["event_filings"]["after"] == QUARTER
    earlier = "0000950170-24-094602"            # ADTRAN's 10-Q of 2024-08-09
    manifest["event_filings"]["after"] = earlier
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    with pytest.raises(cutoff_guard.CutoffGuardError) as refusal:
        section(root, TICKER, ANNUAL)
    assert (f"fetched for the window after {earlier}, and the index at 2025-03-03 opens it "
            f"after {QUARTER}") in str(refusal.value)
    assert not isinstance(refusal.value, cutoff_guard.CutoffViolationError)


def test_the_index_keeps_the_rows_of_letters_not_yet_public_and_no_input_prints_them(tmp_path):
    """The store for the 10-Q of 2024-11-12 holds no document and no release of
    the three letters made public 2024-12-04, and its index, EDGAR's list by
    filing date, holds their rows. The file the reader gets names none of them."""
    root, _, _ = fetched(tmp_path, TICKER, QUARTER)
    index = json.loads((root / TICKER / "submissions.json").read_text())
    listed = {entry["accession"]: (entry["form"], entry["filing_date"])
              for entry in index["filings"]}
    assert {accession: listed[accession] for accession in FIRST_CONVERSATION} == {
        STAFF: ("UPLOAD", "2024-09-26"), RESPONSE: ("CORRESP", "2024-09-27"),
        CLOSING: ("UPLOAD", "2024-11-04")}
    manifest = fetch_fixtures.load_manifest(root / TICKER)
    assert not set(FIRST_CONVERSATION) & set(manifest["event_filings"]["releases"])
    assert not set(FIRST_CONVERSATION) & {entry["accession"] for entry in manifest["documents"]}
    text = parse_8k.render_index(TICKER, cutoff="2024-11-12", fixtures_root=root,
                                 trigger=event_store.as_trigger(TICKER, QUARTER))
    assert "## item codes, every 8-K on or before 2024-11-12" in text    # the index is printed
    for accession in FIRST_CONVERSATION:
        assert accession not in text
    assert "UPLOAD" not in text and "CORRESP" not in text


def test_a_header_that_names_another_filing_states_no_release_for_this_one():
    # the header's first line names the accession it belongs to: the closing
    # letter's own header gives its release, 2024-12-04, and says nothing about
    # the staff's first letter, whatever date it carries
    header = f"<SEC-HEADER>{CLOSING}.hdr.sgml : 20241204\n<PRIVATE-TO-PUBLIC>\n".encode()
    assert fetch_fixtures.released_on(header, CLOSING, "2024-11-04") == "2024-12-04"
    assert fetch_fixtures.released_on(header, STAFF, "2024-09-26") is None


def test_a_release_is_never_recorded_before_the_filing_date_nor_from_a_day_that_is_none():
    # a letter filed 2024-09-26 cannot have been public on 2024-09-01: the day
    # recorded is the filing date, so the letter is never placed in an earlier window
    early = f"<SEC-HEADER>{STAFF}.hdr.sgml : 20240901\n".encode()
    assert fetch_fixtures.released_on(early, STAFF, "2024-09-26") == "2024-09-26"
    # the thirteenth month is no day, and states no release
    no_day = f"<SEC-HEADER>{STAFF}.hdr.sgml : 20241304\n".encode()
    assert fetch_fixtures.released_on(no_day, STAFF, "2024-09-26") is None
