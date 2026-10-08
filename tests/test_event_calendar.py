"""The event calendar: which filings are which events, and that nothing is written twice.

The planted inputs are copied from what EDGAR serves: Apple's 8-K of
2009-02-27 (accession 0001181431-09-012161, items 4.01) as its submissions
record lists it; the first 10-K/A lines of `full-index/2009/QTR1/form.gz`;
Apple's `0001193125-09-209633.hdr.sgml`; six rows of the SEC's list of
accounting and auditing enforcement releases as served on 2026-09-28; and
sentences from the notes data sets `2011q2_notes.zip` and `2026_01_notes.zip`.
Which event each is, is read off the source by hand: the item number the filer
declared, the form the index prints, the release number the list prints.
"""

from __future__ import annotations

import datetime as dt
import gzip
import json
import zipfile

import pytest

from src import event_calendar as calendar
from src import plain_name_check

APPLE_AUDITOR_CHANGE = {"accessionNumber": "0001181431-09-012161", "filingDate": "2009-02-27",
                        "acceptanceDateTime": "2009-02-27T21:30:39.000Z", "form": "8-K",
                        "items": "4.01"}


def arrays(rows):
    keys = ("accessionNumber", "filingDate", "acceptanceDateTime", "form", "items")
    return {key: [row.get(key, "") for row in rows] for key in keys}


# -- which filing is which event -------------------------------------------------

@pytest.mark.parametrize("form, items, events", [
    ("8-K", "4.01", ["auditor_change"]),
    ("8-K", "2.02,4.02,9.01", ["non_reliance"]),
    ("8-K/A", "5.02", ["officer_director_change"]),
    ("8-K", "1.03,3.01,5.02", ["bankruptcy", "delisting_notice", "officer_director_change"]),
    ("8-K", "2.02,9.01", []),
    ("8-K", "", []),
    ("10-K/A", "", ["annual_report_amended"]),
    ("10-Q/A", "", ["quarterly_report_amended"]),
    ("UPLOAD", "", ["staff_comment_letter"]),
    ("CORRESP", "", ["filer_response_letter"]),
    ("10-K", "", []),
    ("8-K12B", "4.01", []),
])
def test_events_of_reads_the_form_and_the_declared_items(form, items, events):
    assert sorted(calendar.events_of(form, items)) == sorted(events)


def test_a_filing_of_two_items_is_two_events_and_names_its_items():
    lines = [calendar.line_for(event, cik=1, accession="a", form="8-K", filed="2020-01-02",
                               items="4.01,4.02", source="submissions")
             for event in calendar.events_of("8-K", "4.01,4.02")]
    assert {line["event"] for line in lines} == {"auditor_change", "non_reliance"}
    assert {line["items"] for line in lines} == {"4.01,4.02"}


# -- the submissions bulk file -------------------------------------------------

def bulk(tmp_path, members):
    path = tmp_path / "submissions.zip"
    with zipfile.ZipFile(path, "w") as archive:
        for name, document in members.items():
            archive.writestr(name, json.dumps(document))
    return zipfile.ZipFile(path)


def test_the_bulk_file_gives_events_from_the_main_file_and_its_older_pages(tmp_path):
    main = {"cik": "320193", "filings": {"recent": arrays([
        {"accessionNumber": "0000320193-20-000001", "filingDate": "2020-01-02", "form": "4"},
        {"accessionNumber": "0000320193-20-000002", "filingDate": "2020-01-03",
         "form": "CORRESP"}]), "files": [{"name": "CIK0000320193-submissions-001.json"}]}}
    older = arrays([APPLE_AUDITOR_CHANGE,
                    {"accessionNumber": "0001181431-08-000001", "filingDate": "2008-12-31",
                     "form": "8-K", "items": "4.02"}])
    found, seen = calendar.from_submissions(bulk(tmp_path, {
        "CIK0000320193.json": main, "CIK0000320193-submissions-001.json": older}))
    assert sorted((line["event"], line["accession"]) for line in found) == [
        ("auditor_change", "0001181431-09-012161"),
        ("filer_response_letter", "0000320193-20-000002")]
    change = next(line for line in found if line["event"] == "auditor_change")
    assert change == {"event": "auditor_change", "cik": 320193,
                      "accession": "0001181431-09-012161", "form": "8-K",
                      "filed": "2009-02-27", "accepted": "2009-02-27T21:30:39.000Z",
                      "source": "submissions", "items": "4.01"}
    # Watched means every filing of a watched form since 2009, event or not.
    assert seen == {int("000118143109012161"), int("000032019320000002")}


# -- the filing indexes ------------------------------------------------------------

FORM_INDEX = """Description:           Master Index of EDGAR Dissemination Feed by Form Type
Last Data Received:    March 31, 2009
Comments:              webmaster@sec.gov
Anonymous FTP:         ftp://ftp.sec.gov/edgar/




Form Type   Company Name                                                  CIK         Date Filed  File Name
---------------------------------------------------------------------------------------------------------------------------------------------
1                C2 Options Exchange, Inc                                      1455287     2009-01-21  edgar/data/1455287/9999999997-09-002901.txt
10-K/A           250 WEST 57TH ST ASSOCIATES L.L.C.                            100412      2009-01-23  edgar/data/100412/0000100412-09-000004.txt
10-K/A           60 EAST 42ND STREET ASSOCIATES L.L.C.                         90794       2009-01-05  edgar/data/90794/0000090794-09-000002.txt
10-K405          SOME FILER                                                    1234        2009-01-05  edgar/data/1234/0000001234-09-000001.txt
8-K              APPLE INC                                                     320193      2009-10-19  edgar/data/320193/0001193125-09-209633.txt
"""


def test_index_rows_reads_the_watched_forms_and_nothing_else():
    assert list(calendar.index_rows(FORM_INDEX)) == [
        ("10-K/A", 100412, "2009-01-23", "0000100412-09-000004"),
        ("10-K/A", 90794, "2009-01-05", "0000090794-09-000002"),
        ("8-K", 320193, "2009-10-19", "0001193125-09-209633")]


APPLE_HEADER = b"""<SEC-HEADER>0001193125-09-209633.hdr.sgml : 20091019
<ACCEPTANCE-DATETIME>20091019162943
<ACCESSION-NUMBER>0001193125-09-209633
<TYPE>8-K
<PUBLIC-DOCUMENT-COUNT>3
<PERIOD>20091019
<ITEMS>2.02
<ITEMS>9.01
<FILING-DATE>20091019
"""


class Served:
    def __init__(self, documents):
        self.documents, self.asked = documents, []

    def get(self, url):
        self.asked.append(url)
        if url not in self.documents:
            raise OSError(f"not served: {url}")
        return self.documents[url]


def test_the_indexes_add_what_the_bulk_file_lacks_and_read_an_8k_items_from_its_header(tmp_path):
    index = FORM_INDEX + (
        "8-K              APPLE INC                                                     320193"
        "      2009-02-27  edgar/data/320193/0001181431-09-012161.txt          \n")
    header = APPLE_HEADER.replace(b"<ITEMS>2.02\n<ITEMS>9.01\n", b"<ITEMS>4.02\n")
    fetcher = Served({
        calendar.FORM_INDEX_URL.format(year=2009, quarter=1): gzip.compress(index.encode()),
        calendar.HEADER_URL.format(cik=320193, folder="000119312509209633",
                                   accession="0001193125-09-209633"): header})
    # The bulk file already holds the 60 East 42nd Street 10-K/A.
    seen = {int("0000090794-09-000002".replace("-", ""))}
    found = calendar.from_indexes(fetcher, seen, since="2009-01-01",
                                  today=dt.date(2009, 3, 1), root=tmp_path)
    assert sorted((line["event"], line["accession"], line["source"]) for line in found) == [
        ("annual_report_amended", "0000100412-09-000004", "full_index"),
        ("non_reliance", "0001193125-09-209633", "full_index")]
    source = calendar.sources(tmp_path)[0]
    assert (source["watched_filings_listed"], source["not_in_submissions"]) == (4, 3)
    # The index is named by its year and quarter: its address spells the quarter
    # as a capital tag on a digit, which the plain-name check reads as a code.
    assert (source["year"], source["quarter"], "url" in source) == (2009, 1, False)
    assert plain_name_check.codes_in((tmp_path / calendar.SOURCES).read_text()) == []
    # Apple's second 8-K header is not served: it is counted, not guessed at.
    assert len(source["headers_unread"]) == 1
    assert source["headers_unread"][0].startswith("0001181431-09-012161: OSError")


def test_items_from_header_reads_every_items_line():
    fetcher = Served({calendar.HEADER_URL.format(cik=320193, folder="000119312509209633",
                                                 accession="0001193125-09-209633"):
                      APPLE_HEADER})
    assert calendar.items_from_header(fetcher, 320193, "0001193125-09-209633") == "2.02,9.01"


def test_quarters_run_from_the_first_to_the_one_today_is_in():
    assert calendar.quarters("2009-01-01", dt.date(2010, 2, 1)) == [
        (2009, 1), (2009, 2), (2009, 3), (2009, 4), (2010, 1)]


# -- going concern ---------------------------------------------------------------

@pytest.mark.parametrize("value, sentences", [
    # 2011q2, SignificantAccountingPoliciesTextBlock, 0001096906-11-000721.
    ("Accordingly, these factors raise substantial doubt as to the Company's ability to "
     "continue as a going concern.", 1),
    # 2026-01, SubstantialDoubtAboutGoingConcernTextBlock, 0001104659-26-003397: a policy.
    ("Note 3  Going Concern and Financial Condition Under ASC 205-40, Presentation of "
     "Financial StatementsGoing Concern , the Company has the responsibility to evaluate "
     "whether conditions and/or events raise substantial doubt about its ability to meet its "
     "future financial obligations as they become due within one year after the date that "
     "the financial statements are issued.", 1),
    # The two phrases in two sentences are not the language.
    ("The Company has incurred losses. There is substantial doubt. It is a going concern.", 0),
    ("AmendmentFlag false", 0),
])
def test_going_concern_counts_sentences_holding_both_phrases(value, sentences):
    assert calendar.going_concern(value) == sentences


def notes_zip(tmp_path, txt_rows):
    sub = ("adsh\tcik\tform\tfiled\taccepted\n"
           "0001096906-11-000721\t1284452\t10-K\t20110415\t2011-04-14 22:01:00.0\n")
    txt = "adsh\ttag\tversion\tvalue\n" + "".join(f"{row}\n" for row in txt_rows)
    path = tmp_path / "2011q2_notes.zip"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("sub.tsv", sub)
        archive.writestr("txt.tsv", txt)
    return path


def test_from_notes_is_one_line_per_filing_naming_the_first_tag(tmp_path):
    said = ("Accordingly, these factors raise substantial doubt as to the Company's ability "
            "to continue as a going concern.")
    path = notes_zip(tmp_path, [
        f"0001096906-11-000721\tSignificantAccountingPoliciesTextBlock\tus-gaap/2009\t{said}",
        f"0001096906-11-000721\tGoingConcernNote\t0001096906-11-000721\t\"{said} {said}\"",
        "0001096906-11-000721\tAmendmentFlag\tdei/2009\tfalse"])
    with zipfile.ZipFile(path) as archive:
        lines = calendar.from_notes(archive, "2011q2")
    # No form: the `sub` row holds it, and a registration statement's is a code.
    assert lines == [{"event": "going_concern_language", "cik": 1284452,
                      "accession": "0001096906-11-000721",
                      "filed": "2011-04-15", "accepted": "2011-04-14 22:01:00.0",
                      "source": "notes_data_set", "dataset": "2011q2",
                      "tag": "SignificantAccountingPoliciesTextBlock", "sentences": 3}]


def test_scan_notes_appends_once_and_records_the_data_set(tmp_path):
    said = ("Accordingly, these factors raise substantial doubt as to the Company's ability "
            "to continue as a going concern.")
    path = notes_zip(tmp_path, [f"0001096906-11-000721\tGoingConcernNote\tus-gaap/2009\t{said}"])
    line = {"period": "2011q2", "url": "https://x/2011q2_notes.zip", "sha256": "f" * 64,
            "bytes": path.stat().st_size}
    root = tmp_path / "calendar"
    assert calendar.scan_notes(path, line, root=root) == {"going_concern_filings": 1,
                                                          "added": 1}
    assert calendar.scan_notes(path, line, root=root) == {"going_concern_filings": 1,
                                                          "added": 0}
    assert len((root / "going_concern_language" / "2011.jsonl").read_text().splitlines()) == 1
    assert [source["dataset"] for source in calendar.sources(root)] == ["2011q2", "2011q2"]


# -- appending -------------------------------------------------------------------

def test_append_writes_each_event_once_oldest_first_and_never_rewrites(tmp_path):
    def line(accession, filed, cik=1):
        return calendar.line_for("non_reliance", cik=cik, accession=accession, form="8-K",
                                 filed=filed, items="4.02", source="submissions")
    first = calendar.append(tmp_path, [line("b", "2020-03-01"), line("a", "2020-01-01")])
    path = tmp_path / "non_reliance" / "2020.jsonl"
    before = path.read_bytes()
    second = calendar.append(tmp_path, [line("a", "2020-01-01"), line("a", "2020-01-01", cik=2),
                                        line("c", "2021-06-01")])
    assert (first["non_reliance"], second["non_reliance"]) == (2, 2)
    assert path.read_bytes().startswith(before)
    assert [json.loads(text)["accession"] for text in path.read_text().splitlines()] == [
        "a", "b", "a"]
    assert (tmp_path / "non_reliance" / "2021.jsonl").is_file()


def test_counts_over_every_filer_and_over_the_named_ones(tmp_path):
    calendar.append(tmp_path, [
        calendar.line_for("auditor_change", cik=320193, accession="a", form="8-K",
                          filed="2009-02-27", items="4.01", source="submissions"),
        calendar.line_for("auditor_change", cik=1, accession="b", form="8-K",
                          filed="2010-02-27", items="4.01", source="submissions")])
    assert calendar.counts(tmp_path)["auditor_change"] == 2
    assert calendar.counts(tmp_path, {320193})["auditor_change"] == 1
    assert calendar.counts(tmp_path, {320193})["non_reliance"] == 0


# -- enforcement releases ----------------------------------------------------------

LIST_PAGE = """<table><thead><tr><th>Date</th><th>Respondents</th></tr></thead><tbody>
<tr> <td headers="view-field-publish-date-table-column" class="views-field views-field-field-publish-date is-active"> <time datetime="2026-09-23T19:27:20Z" class="datetime">Sept. 23, 2026</time> </td> <td headers="view-nothing-1-table-column" class="views-field views-field-field-release-file-number views-field-nothing-1"><div class='release-view__respondents'><a href='https://www.sec.gov/files/litigation/opinions/2026/33-11440.pdf'>L&amp;L Energy, Inc. and Dickson Lee, CPA (Order Granting Extension of Time to File a Reply)</a></div> <div class="view-table_subfield view-table_subfield_release_number"> <span class="view-table_subfield_label">Release No.</span> <span class="view-table_subfield_value">33-11440, 34-106474, AAER-4602</span> </div> </td> </tr>
<tr> <td headers="view-field-publish-date-table-column" class="views-field views-field-field-publish-date is-active"> <time datetime="2026-09-22T18:03:59Z" class="datetime">Sept. 22, 2026</time> </td> <td headers="view-nothing-1-table-column" class="views-field views-field-field-release-file-number views-field-nothing-1"><div class='release-view__respondents'><a href='https://www.sec.gov/files/litigation/admin/2026/34-106459.pdf'>Nihat Cardak</a></div> <div class="view-table_subfield view-table_subfield_release_number"> <span class="view-table_subfield_label">Release No.</span> <span class="view-table_subfield_value">34-106459, AAER-4601</span> </div> </td> </tr>
<tr> <td headers="view-field-publish-date-table-column" class="views-field views-field-field-publish-date is-active"> <time datetime="2026-09-12T02:28:56Z" class="datetime">Sept. 11, 2026</time> </td> <td headers="view-nothing-1-table-column" class="views-field views-field-field-release-file-number views-field-nothing-1"><div class='release-view__respondents'><a href='https://www.sec.gov/files/litigation/admin/2026/34-106344.pdf'>Dada Nexus Limited</a></div> <div class="view-table_subfield view-table_subfield_release_number"> <span class="view-table_subfield_label">Release No.</span> <span class="view-table_subfield_value">34-106344, AAER-4600</span> </div> </td> </tr>
</tbody></table>"""


# Three more rows as served on 2026-09-28, from pages 7, 10 and 15 of the list: a
# respondent named with a capital and a digit, a row naming two releases, and
# a row carrying another act's release number in the shape of a code.
CODED_ROWS = """<table><tbody>
<tr> <td headers="view-field-publish-date-table-column" class="views-field views-field-field-publish-date is-active"> <time datetime="2017-01-11T13:24:43Z" class="datetime">Jan. 11, 2017</time> </td> <td headers="view-nothing-1-table-column" class="views-field views-field-field-release-file-number views-field-nothing-1"><div class='release-view__respondents'><a href='https://www.sec.gov/files/litigation/admin/2017/34-79772.pdf'>L3 Technologies, Inc.</a></div> <div class="view-table_subfield view-table_subfield_release_number"> <span class="view-table_subfield_label">Release No.</span> <span class="view-table_subfield_value">34-79772, AAER-3844</span> </div> </td> </tr>
<tr> <td headers="view-field-publish-date-table-column" class="views-field views-field-field-publish-date is-active"> <time datetime="2014-07-25T14:25:26Z" class="datetime">July 25, 2014</time> </td> <td headers="view-nothing-1-table-column" class="views-field views-field-field-release-file-number views-field-nothing-1"><div class='release-view__respondents'><a href='/enforcement-litigation/litigation-releases/lr-23051'>Volt Information Sciences, Inc. and Debra L. Hobbs; Jack J. Egan, Jr.</a></div> <div class="view-table_subfield view-table_subfield_release_number"> <span class="view-table_subfield_label">Release No.</span> <span class="view-table_subfield_value">LR-23051, AAER-3569 and AAER-3570, AAER-3569</span> </div> </td> </tr>
<tr> <td headers="view-field-publish-date-table-column" class="views-field views-field-field-publish-date is-active"> <time datetime="2009-10-28T13:17:12Z" class="datetime">Oct. 28, 2009</time> </td> <td headers="view-nothing-1-table-column" class="views-field views-field-field-release-file-number views-field-nothing-1"><div class='release-view__respondents'><a href='https://www.sec.gov/files/litigation/admin/2009/34-60898.pdf'>Tab Keplinger, CPA</a></div> <div class="view-table_subfield view-table_subfield_release_number"> <span class="view-table_subfield_label">Release No.</span> <span class="view-table_subfield_value">34-60898, IA-2942, AAER-3061</span> </div> </td> </tr>
</tbody></table>"""


def test_releases_on_reads_each_row_of_the_list():
    releases = calendar.releases_on(LIST_PAGE)
    assert [line["release"] for line in releases] == [4602, 4601, 4600]
    assert releases[0] == {
        "event": "enforcement_release", "release": 4602, "filed": "2026-09-23",
        "document": "https://www.sec.gov/files/litigation/opinions/2026/33-11440.pdf",
        "cik": None, "source": "enforcement_list"}


def test_a_row_naming_two_releases_is_a_line_for_each_and_no_line_holds_a_code():
    releases = calendar.releases_on(CODED_ROWS)
    assert [(line["release"], line["filed"]) for line in releases] == [
        (3844, "2017-01-11"), (3569, "2014-07-25"), (3570, "2014-07-25"),
        (3061, "2009-10-28")]
    # The list's own link to a litigation release is relative.
    assert releases[1]["document"] == ("https://www.sec.gov/enforcement-litigation/"
                                       "litigation-releases/lr-23051")
    # What the list prints that the check reads as a code: a respondent's name,
    # every release number of the list's own kind, and another act's. The line
    # keeps the numbers as numbers; the rest stays in the document.
    assert plain_name_check.codes_in(CODED_ROWS) == [
        "L3", "AAER-3844", "AAER-3569", "AAER-3570", "AAER-3569", "IA-2942", "AAER-3061"]
    assert plain_name_check.codes_in(json.dumps(releases)) == []


def test_a_release_is_dated_on_new_york_s_clock():
    # 02:28 universal time on the twelfth is the evening of the eleventh in New York;
    # the third row's time is moved past midnight for this reason.
    assert calendar.releases_on(LIST_PAGE)[2]["filed"] == "2026-09-11"


def test_the_list_is_read_until_a_page_reaches_before_the_start(tmp_path):
    fetcher = Served({calendar.ENFORCEMENT_URL.format(page=0): LIST_PAGE.encode(),
                      calendar.ENFORCEMENT_URL.format(page=1): LIST_PAGE.encode()})
    found = calendar.from_enforcement_list(fetcher, since="2026-09-12")
    assert [line["release"] for line in found] == [4602, 4601]
    assert len(fetcher.asked) == 1
    added = calendar.append(tmp_path, found)
    assert added["enforcement_release"] == 2
    assert calendar.append(tmp_path, found)["enforcement_release"] == 0


# -- the daily indexes -------------------------------------------------------------

DAILY_INDEX = """Description:           Daily Index of EDGAR Dissemination Feed by Form Type
Last Data Received:    Sep 25, 2026
Comments:              webmaster@sec.gov
Anonymous FTP:         ftp://ftp.sec.gov/edgar/
 
 
 
 
Form Type   Company Name                                                  CIK
      Date Filed  File Name
---------------------------------------------------------------------------------------------------------------------------------------------
1-A POS          Modern Mining Technology Corp.                                1898722     20260925    edgar/data/1898722/0001213900-26-103507.txt    
8-K              ACNB CORP                                                     715579      20260925    edgar/data/715579/0001628280-26-063501.txt                                                
"""


def test_index_rows_reads_the_daily_index_s_undashed_date():
    assert list(calendar.index_rows(DAILY_INDEX)) == [
        ("8-K", 715579, "2026-09-25", "0001628280-26-063501")]


def test_read_through_takes_the_latest_day_a_source_line_names(tmp_path):
    assert calendar.read_through(tmp_path) is None
    calendar.record_source(tmp_path, {"source": "full_index", "through": "2026-09-24"})
    calendar.record_source(tmp_path, {"source": "notes_data_set", "through": "2026-09-27"})
    assert calendar.read_through(tmp_path) == dt.date(2026, 9, 24)


def test_a_quarterly_line_that_names_no_day_stands_for_the_week_before_it_was_read(tmp_path):
    (tmp_path / calendar.SOURCES).write_text(json.dumps(
        {"source": "full_index", "at": "2026-09-28T21:00:00Z"}) + "\n")
    assert calendar.read_through(tmp_path) == dt.date(2026, 9, 21)


def test_daily_reads_each_business_day_after_the_last_one_read(tmp_path):
    calendar.record_source(tmp_path, {"source": "full_index", "through": "2026-09-24"})
    # A planted header: ACNB's 8-K declaring item 5.02.
    fetcher = Served({
        calendar.DAILY_INDEX_URL.format(year=2026, quarter=3, day="20260925"):
            DAILY_INDEX.encode(),
        calendar.HEADER_URL.format(cik=715579, folder="000162828026063501",
                                   accession="0001628280-26-063501"):
            b"<ITEMS>5.02\n<ITEMS>9.01\n"})
    done = calendar.daily(fetcher, root=tmp_path, today=dt.date(2026, 9, 29))
    assert done == {"from": "2026-09-25", "through": "2026-09-28", "days": 4,
                    "added": {"officer_director_change": 1}}
    # Friday and Monday are asked for; the weekend is not; Monday is not served.
    assert [url for url in fetcher.asked if "daily-index" in url] == [
        calendar.DAILY_INDEX_URL.format(year=2026, quarter=3, day="20260925"),
        calendar.DAILY_INDEX_URL.format(year=2026, quarter=3, day="20260928")]
    line = json.loads((tmp_path / "officer_director_change" / "2026.jsonl").read_text())
    assert (line["source"], line["items"], line["accepted"]) == ("daily_index", "5.02,9.01",
                                                                  None)
    assert calendar.read_through(tmp_path) == dt.date(2026, 9, 25)
    assert [source.get("unread", "")[:7] for source in calendar.sources(tmp_path)][-1] == \
        "OSError"
    assert plain_name_check.codes_in((tmp_path / calendar.SOURCES).read_text()) == []


def test_daily_before_any_index_was_read_says_so(tmp_path):
    assert calendar.daily(Served({}), root=tmp_path, today=dt.date(2026, 9, 29))["days"] == 0


# -- the disk floor ----------------------------------------------------------------

def test_a_submissions_read_the_floor_stops_has_written_nothing(tmp_path, monkeypatch):
    from src import fsn
    # 2 GB held for the bulk file on a disk with 9 GB free leaves 7, under the 10 GB floor.
    monkeypatch.setattr(fsn, "free_bytes", lambda _: 9 * 10**9)
    monkeypatch.setattr(fsn, "download", lambda *a, **k: pytest.fail("downloaded anyway"))
    assert calendar.main(["submissions", "--root", str(tmp_path / "calendar"),
                          "--work", str(tmp_path / "data" / "tmp" / "calendar")]) == \
        calendar.FAILED
    assert list(tmp_path.iterdir()) == []
