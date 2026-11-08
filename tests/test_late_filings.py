"""Notifications of late filing reach the notes reader, with the report they
gave notice of.

Two real notices, read by eye from EDGAR on 2026-10-28 (the documents are
committed under `tests/fixtures/event_filings/` with their addresses and sha256
in `record.json`; the index rows are the committed
`tests/fixtures/{LFUS,ADTN}/submissions.json`, EDGAR's submissions index):

* Littelfuse's NT 10-K, 0001140361-25-006294, `filingDate` 2025-02-27, report
  date 2024-12-28. Part III: the company "has determined that it is unable to
  file, without unreasonable effort or expense, its Annual Report on Form 10-K
  for the fiscal year ended December 28, 2024", and "expects to file on or
  before March 13, 2025". The late report is the 10-K 0000889331-25-000039,
  `filingDate` 2025-03-13; the report before the notice is the 10-Q
  0000889331-24-000191 of 2024-10-30.
* ADTRAN's NT 10-Q, 0000950170-25-070493, `filingDate` 2025-05-13 (the index
  gives its report date as 2025-05-13; the form's own "For Period Ended" is
  March 31, 2025). Part III: the company "is unable, without unreasonable effort
  or expense, to file its Quarterly Report on Form 10-Q for the quarter ended
  March 31, 2025". The late report is the 10-Q 0000950170-25-075374,
  `filingDate` 2025-05-20; the report before the notice is the 10-K
  0000950170-25-031056 of 2025-03-03.
"""

from __future__ import annotations

import pytest

from src import cutoff_guard, fetch_fixtures
from tests.event_store import fetched, manifest_rows, recorded, section, RECORD

NOTICE = "0001140361-25-006294"
LATE_TEN_K = "0000889331-25-000039"
QUARTER_BEFORE = "0000889331-24-000191"
ADTRAN_NOTICE = "0000950170-25-070493"
ADTRAN_LATE_TEN_Q = "0000950170-25-075374"
ADTRAN_TEN_K = "0000950170-25-031056"


def folded(text: str) -> str:
    return " ".join(text.split())


def test_littelfuses_notice_reaches_the_annual_report_it_gave_notice_of(tmp_path):
    root, problems, _ = fetched(tmp_path, "LFUS", LATE_TEN_K)
    assert problems == []
    rows = [entry for entry in manifest_rows(root, "LFUS") if entry["role"] == "late_notice"]
    assert [(entry["form"], entry["accession"], entry["filing_date"], entry["report_date"])
            for entry in rows] == [("NT 10-K", NOTICE, "2025-02-27", "2024-12-28")]
    assert rows[0]["sha256"] == RECORD["files"][f"{NOTICE}/ef20044546_nt10k.htm"]["sha256"]
    events, text = section(root, "LFUS", LATE_TEN_K)
    assert events["previous"]["accession"] == QUARTER_BEFORE
    [notice] = events["carried"]
    assert notice["late_report"] == {"form": "10-K", "accession": LATE_TEN_K,
                                     "filing_date": "2025-03-13", "items": []}
    assert (f"### NT 10-K {NOTICE} filed 2025-02-27, report date 2024-12-28 in the index, "
            "a notification of late filing; the report it gives notice of: the 10-K "
            f"{LATE_TEN_K} filed 2025-03-13; verbatim") in text
    paragraphs = [folded(paragraph) for paragraph in notice["paragraphs"]]
    assert any(paragraph.startswith(
        "Littelfuse, Inc. (the “Company”) has determined that it is unable to file, without "
        "unreasonable effort or expense, its Annual Report on Form 10-K for the fiscal year "
        "ended December 28, 2024 (the “Form 10-K”) by the prescribed filing due date")
        for paragraph in paragraphs)
    assert ("The Company is currently finalizing these items and will detail its "
            "conclusions in the Form 10-K, which it expects to file on or before March 13, "
            "2025.") in paragraphs
    assert notice["paragraph_ids"] == [f"{NOTICE}:late_notice:{number}"
                                       for number in range(1, len(paragraphs) + 1)]
    # each paragraph is the notice's own characters, out of the one tag stripper
    from src import html_text
    stripped = html_text.strip_tags(recorded(NOTICE, "ef20044546_nt10k.htm").decode("utf-8"))
    assert all(paragraph in stripped for paragraph in notice["paragraphs"])


def test_the_notice_is_not_in_the_window_of_the_quarter_before_it(tmp_path):
    """The 10-Q of 2024-10-30 stood before the notice was filed."""
    root, problems, _ = fetched(tmp_path, "LFUS", QUARTER_BEFORE)
    assert problems == []
    assert NOTICE not in {entry["accession"] for entry in manifest_rows(root, "LFUS")}
    _, text = section(root, "LFUS", QUARTER_BEFORE)
    assert NOTICE not in text


def test_a_read_of_the_notice_before_its_filing_date_is_refused(tmp_path):
    root, _, _ = fetched(tmp_path, "LFUS", LATE_TEN_K)
    [entry] = [one for one in manifest_rows(root, "LFUS") if one["role"] == "late_notice"]
    with pytest.raises(cutoff_guard.CutoffViolationError):
        cutoff_guard.load_bytes(root / "LFUS" / entry["path"], "2025-02-26", fixtures_root=root)
    assert cutoff_guard.load_bytes(root / "LFUS" / entry["path"], "2025-02-27",
                                   fixtures_root=root) == \
        recorded(NOTICE, "ef20044546_nt10k.htm")


def test_adtrans_notice_names_the_quarter_it_filed_a_week_later(tmp_path):
    root, problems, _ = fetched(tmp_path, "ADTN", ADTRAN_LATE_TEN_Q)
    assert problems == []
    events, text = section(root, "ADTN", ADTRAN_LATE_TEN_Q)
    assert events["previous"]["accession"] == ADTRAN_TEN_K
    notices = [entry for entry in events["carried"] if entry["role"] == "late_notice"]
    assert [(entry["form"], entry["accession"], entry["filing_date"]) for entry in notices] \
        == [("NT 10-Q", ADTRAN_NOTICE, "2025-05-13")]
    assert notices[0]["late_report"]["accession"] == ADTRAN_LATE_TEN_Q
    assert notices[0]["late_report"]["filing_date"] == "2025-05-20"
    assert ("ADTRAN Holdings, Inc. (the “Company”) is unable, without unreasonable effort "
            "or expense, to file its Quarterly Report on Form 10-Q for the quarter ended "
            "March 31, 2025 (the “Q1 Form 10-Q”) with the Securities and Exchange Commission "
            "(the “SEC”) within the prescribed time period for the reasons set forth below."
            in [folded(paragraph) for paragraph in notices[0]["paragraphs"]])
    # the comment letters filed in 2024 were public in December 2024, before the
    # window opened at the 10-K of 2025-03-03: read for their release, not carried
    assert not [entry for entry in events["carried"] if entry["role"] != "late_notice"]
    assert not [entry for entry in manifest_rows(root, "ADTN")
                if entry["form"] in ("UPLOAD", "CORRESP")]
    releases = fetch_fixtures.load_manifest(root / "ADTN")["event_filings"]["releases"]
    assert {accession: release["released"] for accession, release in releases.items()} == {
        "0000000000-24-010922": "2024-12-04", "0000950170-24-109789": "2024-12-04",
        "0000000000-24-012258": "2024-12-04", "0000000000-24-012928": "2024-12-27",
        "0001193125-24-264351": "2024-12-27"}


def test_the_late_report_is_the_first_of_the_noticed_form_after_the_notice():
    """Planted rows: a notice, a 10-Q of another period filed before it, and the
    10-K that answers it two weeks on, then a later 10-K."""
    notice = {"accessionNumber": "a", "filingDate": "2025-02-27", "form": "NT 10-K/A"}
    known = [{"accessionNumber": "b", "filingDate": "2025-02-01", "form": "10-K"},
             {"accessionNumber": "c", "filingDate": "2025-03-13", "form": "10-Q"},
             {"accessionNumber": "d", "filingDate": "2025-03-13", "form": "10-K"},
             {"accessionNumber": "e", "filingDate": "2026-03-01", "form": "10-K"}]
    from src import parse_8k
    assert parse_8k._late_report(notice, known)["accessionNumber"] == "d"
    assert parse_8k._late_report(notice, known[:2]) is None


def test_a_notice_is_fetched_by_its_index_row_whatever_its_header_calls_it():
    """EDGAR's header types the notice's document `NT` (the form name holds a
    space), so the document is the index row's primary document."""
    assert fetch_fixtures.LATE_NOTICE_FORMS == ("NT 10-K", "NT 10-Q", "NT 10-K/A", "NT 10-Q/A")
    window = fetch_fixtures.event_window(
        [{"accessionNumber": "0001140361-25-006294", "filingDate": "2025-02-27",
          "form": "NT 10-K", "items": "", "acceptanceDateTime": None},
         {"accessionNumber": "0000889331-24-000191", "filingDate": "2024-10-30",
          "form": "10-Q", "items": "", "acceptanceDateTime": None}],
        {"accessionNumber": LATE_TEN_K, "filingDate": "2025-03-13", "form": "10-K",
         "acceptanceDateTime": None})
    assert [row["accessionNumber"] for row in window["notices"]] == [NOTICE]
    assert window["previous"]["accessionNumber"] == QUARTER_BEFORE
