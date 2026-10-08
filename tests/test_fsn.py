"""The notes data sets: the index, the disk floor, the loader, the ten values.

Every row planted here is copied from the SEC's `2011q2_notes.zip` (sha256
2b9873b0...a720): Celgene's 10-Q for the first quarter of 2011 and Extra Space
Storage's for the same quarter. The companyfacts rows are copied from
`data.sec.gov/api/xbrl/companyfacts/CIK0000816284.json` as served on
2026-09-28. The order two accessions are ranked in is their sha256, computed
here with `hashlib` -- that is the rule's definition, not the module's answer.
"""

from __future__ import annotations

import hashlib
import io
import json
import zipfile

import pytest

from src import fsn

CELGENE = "0000950123-11-044984"
EXTRA_SPACE = "0001104659-11-026800"

SUB_HEADER = ("adsh\tcik\tname\tsic\tcountryba\tstprba\tcityba\tzipba\tbas1\tbas2\tbaph\t"
              "countryma\tstprma\tcityma\tzipma\tmas1\tmas2\tcountryinc\tstprinc\tein\t"
              "former\tchanged\tafs\twksi\tfye\tform\tperiod\tfy\tfp\tfiled\taccepted\t"
              "prevrpt\tdetail\tinstance\tnciks\taciks\tpubfloatusd\tfloatdate\tfloataxis\t"
              "floatmems")
SUB_ROWS = [
    "0000950123-11-044984\t816284\tCELGENE CORP /DE/\t2834\tUS\tNJ\tSUMMIT\t07901\t"
    "86 MORRIS AVENUE\t\t(908)673-9000\tUS\tNJ\tSUMMIT\t07901\t86 MORRIS AVENUE\t\tUS\tDE\t"
    "222711928\t\t\t1-LAF\t1\t1231\t10-Q\t20110331\t2011\tQ1\t20110505\t"
    "2011-05-04 21:21:00.0\t0\t1\tcelg-20110331.xml\t1\t\t23349073920.00\t20100630\t\t",
    "0001104659-11-026800\t1289490\tEXTRA SPACE STORAGE INC.\t6798\tUS\tUT\tSALT LAKE CITY\t"
    "84121\t2795 COTTONWOOD PARKWAY, SUITE 400\t\t801-562-5556\tUS\tUT\tSALT LAKE CITY\t84121\t"
    "2795 COTTONWOOD PARKWAY, SUITE 400\t\tUS\tMD\t201076777\t\t\t1-LAF\t0\t1231\t10-Q\t"
    "20110331\t2011\tQ1\t20110506\t2011-05-06 14:47:00.0\t0\t0\texr-20110331.xml\t1\t\t\t\t\t",
]
NUM_HEADER = ("adsh\ttag\tversion\tddate\tqtrs\tuom\tdimh\tiprx\tvalue\tfootnote\tfootlen\t"
              "dimn\tcoreg\tdurp\tdatp\tdcml")
NUM_ROWS = [
    "0000950123-11-044984\tAccountsPayableCurrent\tus-gaap/2009\t20101231\t0\tUSD\t"
    "0x00000000\t0\t94465000.0000\t\t0\t0\t\t0.0\t0.0\t-3",
    "0000950123-11-044984\tRevenues\tus-gaap/2009\t20110331\t1\tUSD\t0x00000000\t0\t"
    "1125281000.0000\t\t0\t0\t\t0.024658024\t0.0\t-3",
    # A custom tag, carrying a dimension: companyfacts can hold neither.
    "0000950123-11-044984\tAdditionalContribution\t0000950123-11-044984\t20110331\t1\tUSD\t"
    "0xb66e4938233e3ed9f440c1878c0c1fe0\t0\t50000000.0000\t\t0\t1\t\t0.024658024\t0.0\t-5",
    "0001104659-11-026800\tStockholdersEquity\tus-gaap/2009\t20101231\t0\tUSD\t0x00000000\t0\t"
    "881401000.0000\t\t0\t0\t\t0.0\t0.0\t-3",
]
PRE = ("adsh\treport\tline\tstmt\tinpth\ttag\tversion\tprole\tplabel\tnegating\n"
       "0000950123-11-044984\t3\t19\tBS\t0\tAccountsPayableCurrent\tus-gaap/2009\tverboseLabel\t"
       "Accounts payable\t0\n")
REN = ("adsh\treport\trfile\tmenucat\tshortname\tlongname\troleuri\tparentroleuri\t"
       "parentreport\tultparentrpt\n"
       "0000950123-11-044984\t3\tX\tO\tConsolidated Balance Sheets (Unaudited)\t"
       "0120 - Statement - Consolidated Balance Sheets (Unaudited)\t"
       "http://celgene.com/role/BalanceSheets\t\t\t\n")
TXT = ("adsh\ttag\tversion\tddate\tqtrs\tiprx\tlang\tdcml\tdurp\tdatp\tdimh\tdimn\tcoreg\t"
       "escaped\tsrclen\ttxtlen\tfootnote\tfootlen\tcontext\tvalue\n"
       "0000950123-11-044984\tAmendmentFlag\tdei/2009\t20110331\t1\t0\ten-US\t32767\t"
       "0.024658024\t0.0\t0x00000000\t0\t\t0\t5\t5\t\t0\tThreeMonthsEnded_31Mar2011\tfalse\n")
TAG = ("tag\tversion\tcustom\tabstract\tdatatype\tiord\tcrdr\ttlabel\tdoc\n"
       "LiabilitiesAndStockholdersEquity\tus-gaap/2009\t0\t0\tmonetary\tI\tC\t"
       "Liabilities and Equity\tAmount of liabilities and equity items, including the portion "
       "of equity attributable to noncontrolling interests, if any.\n")
DIM = ("dimhash\tsegments\tsegt\n"
       "0xf1697743cea5ebe83a2df8f6ac5c4ef8\t"
       "RealEstateAndAccumulatedDepreciationDescriptionOfProperty=StAndrewsAtWinstonPark;\t0\n")


def members(num_rows=None, sub_rows=None):
    return {
        "sub.tsv": "\n".join([SUB_HEADER] + (SUB_ROWS if sub_rows is None else sub_rows)) + "\n",
        "num.tsv": "\n".join([NUM_HEADER] + (NUM_ROWS if num_rows is None else num_rows)) + "\n",
        "pre.tsv": PRE, "ren.tsv": REN, "txt.tsv": TXT, "tag.tsv": TAG, "dim.tsv": DIM,
    }


def planted_zip(path, **kwargs):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, text in members(**kwargs).items():
            archive.writestr(name, text)
    return path


def rank(text):
    return hashlib.sha256(text.encode()).hexdigest()


# -- names and the listing -------------------------------------------------------

@pytest.mark.parametrize("name, period", [
    ("2009q2_notes.zip", "2009q2"),
    ("2010q3_notes_0.zip", "2010q3"),
    ("2010q1_notes_1.zip", "2010q1"),
    ("2025_07_notes.zip", "2025-07"),
])
def test_period_of_reads_both_shapes_of_name(name, period):
    assert fsn.period_of(name) == period


def test_period_of_refuses_a_name_that_is_neither():
    with pytest.raises(ValueError):
        fsn.period_of("2009q2.zip")


def test_listed_reads_the_links_oldest_first_and_once_each():
    # The shape of the SEC's page: each zip linked from its table row, some twice.
    page = ('<a href="/files/dera/data/financial-statement-notes-data-sets/2026_08_notes.zip">'
            '2026 August</a> <a href="/files/dera/data/financial-statement-notes-data-sets/'
            '2009q2_notes.zip">2009 Q2</a> <a href="/files/dera/data/financial-statement-notes-'
            'data-sets/2026_08_notes.zip">again</a> <a href="/files/aqfsn_1.pdf">readme</a>')
    assert fsn.listed(page) == [
        {"period": "2009q2", "name": "2009q2_notes.zip",
         "url": "https://www.sec.gov/files/dera/data/financial-statement-notes-data-sets/"
                "2009q2_notes.zip"},
        {"period": "2026-08", "name": "2026_08_notes.zip",
         "url": "https://www.sec.gov/files/dera/data/financial-statement-notes-data-sets/"
                "2026_08_notes.zip"},
    ]


def test_the_index_is_sharded_by_year_and_the_newest_line_of_a_period_wins(tmp_path):
    fsn.append_index({"period": "2010q3", "sha256": "first"}, tmp_path)
    fsn.append_index({"period": "2025-07", "sha256": "only"}, tmp_path)
    fsn.append_index({"period": "2010q3", "sha256": "reissued"}, tmp_path)
    assert sorted(path.name for path in tmp_path.iterdir()) == ["2010.jsonl", "2025.jsonl"]
    assert len((tmp_path / "2010.jsonl").read_text().splitlines()) == 2
    assert {period: line["sha256"] for period, line in
            fsn.latest(fsn.read_index(tmp_path)).items()} == {"2010q3": "reissued",
                                                               "2025-07": "only"}


# -- the floor -----------------------------------------------------------------

def test_the_floor_lets_a_write_through_that_leaves_exactly_the_floor(tmp_path):
    fsn.room_for(tmp_path, 10 * 10**9, fsn.FLOOR_BYTES, free=lambda _: 60 * 10**9)


def test_the_floor_stops_a_write_that_would_leave_less(tmp_path):
    with pytest.raises(fsn.FloorReached, match="under the 50 GB floor"):
        fsn.room_for(tmp_path, 10 * 10**9 + 1, fsn.FLOOR_BYTES, free=lambda _: 60 * 10**9)


def test_the_floor_measures_the_disk_of_a_directory_not_made_yet(tmp_path):
    assert fsn.free_bytes(tmp_path / "not" / "yet") == fsn.free_bytes(tmp_path)


def test_fetch_stops_at_the_floor_before_it_downloads(tmp_path, monkeypatch):
    fsn.append_index({"period": "2011q2", "name": "2011q2_notes.zip", "url": "https://x/",
                      "bytes": 59_459_810, "sha256": "0" * 64}, tmp_path / "index")
    monkeypatch.setattr(fsn, "download", lambda *a, **k: pytest.fail("downloaded anyway"))
    with pytest.raises(fsn.FloorReached):
        fsn.fetch(zips=tmp_path / "zips", user_agent="ua", index_dir=tmp_path / "index",
                  free=lambda _: 23 * 10**9)


def test_main_exits_four_at_the_floor(tmp_path, monkeypatch):
    fsn.append_index({"period": "2011q2", "name": "2011q2_notes.zip", "url": "https://x/",
                      "bytes": 59_459_810, "sha256": "0" * 64}, tmp_path / "index")
    monkeypatch.setattr(fsn, "free_bytes", lambda _: 23 * 10**9)
    assert fsn.main(["fetch", "--root", str(tmp_path / "data"),
                     "--index-dir", str(tmp_path / "index")]) == fsn.FLOOR


def test_fetch_refuses_bytes_that_are_not_the_indexed_ones(tmp_path, monkeypatch):
    fsn.append_index({"period": "2011q2", "name": "2011q2_notes.zip", "url": "https://x/",
                      "bytes": 5, "sha256": rank("indexed")}, tmp_path / "index")

    def served(url, dest, user_agent):
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(b"other")
        return hashlib.sha256(b"other").hexdigest(), 5
    monkeypatch.setattr(fsn, "download", served)
    problems = fsn.fetch(zips=tmp_path / "zips", user_agent="ua",
                         index_dir=tmp_path / "index", free=lambda _: 10**12)
    assert len(problems) == 1 and "2011q2: the SEC now serves" in problems[0]
    assert not (tmp_path / "zips" / "2011q2_notes.zip").exists()


def test_a_load_the_floor_stops_has_written_nothing(tmp_path):
    # The zip is fetched and verified, and the disk is the Mac's of 2026-09-28:
    # the store and its work directory are not made before the floor is asked.
    root = tmp_path / "data"
    zips = root / "fsn" / "zips"
    zips.mkdir(parents=True)
    path = planted_zip(zips / "2011q2_notes.zip")
    with zipfile.ZipFile(path) as archive:
        counts = fsn.count_rows(archive)
    fsn.append_index({"period": "2011q2", "name": path.name, "sha256": fsn.file_sha256(path),
                      "rows": counts}, tmp_path / "index")
    with pytest.raises(fsn.FloorReached, match="nothing was written"):
        fsn.load(db=root / "fsn.duckdb", zips=zips, index_dir=tmp_path / "index",
                 free=lambda _: 23 * 10**9)
    assert sorted(child.name for child in root.iterdir()) == ["fsn"]


# -- reading a zip ---------------------------------------------------------------

def test_count_rows_counts_every_table_and_a_last_row_with_no_newline(tmp_path):
    path = tmp_path / "planted.zip"
    with zipfile.ZipFile(path, "w") as archive:
        for name, text in members().items():
            archive.writestr(name, text.rstrip("\n") if name == "num.tsv" else text)
    with zipfile.ZipFile(path) as archive:
        assert fsn.count_rows(archive) == {"sub": 2, "num": 4, "pre": 1, "tag": 1,
                                           "txt": 1, "dim": 1, "ren": 1}


def test_candidates_rank_filings_by_the_sha256_of_the_accession(tmp_path):
    assert rank(EXTRA_SPACE) < rank(CELGENE)
    with zipfile.ZipFile(planted_zip(tmp_path / "p.zip")) as archive:
        drawn = fsn.candidates(archive, count=1)
    assert [value["accession"] for value in drawn] == [EXTRA_SPACE]
    assert drawn[0]["value"] == "881401000.0000" and drawn[0]["cik"] == 1289490
    # The accession names the filing; a form would put EDGAR's registration
    # statement names, codes to the plain-name check, into the index.
    assert "form" not in drawn[0]


def test_a_filing_value_is_its_lowest_ranked_eligible_row(tmp_path):
    with zipfile.ZipFile(planted_zip(tmp_path / "p.zip")) as archive:
        drawn = {value["accession"]: value for value in fsn.candidates(archive, count=2)}
    keys = {tag: rank("|".join((CELGENE, tag, "us-gaap/2009", ddate, qtrs, "USD")))
            for tag, ddate, qtrs in (("AccountsPayableCurrent", "20101231", "0"),
                                     ("Revenues", "20110331", "1"))}
    assert drawn[CELGENE]["tag"] == min(keys, key=keys.get)
    # The custom, dimensioned row is never drawn, whatever its rank.
    assert drawn[CELGENE]["tag"] != "AdditionalContribution"


# -- the loader ------------------------------------------------------------------

@pytest.fixture
def loaded(tmp_path):
    pytest.importorskip("duckdb")
    path = planted_zip(tmp_path / "2011q2_notes.zip")
    with zipfile.ZipFile(path) as archive:
        counts = fsn.count_rows(archive)
    line = {"period": "2011q2", "name": path.name, "sha256": fsn.file_sha256(path),
            "rows": counts}
    connection = fsn._connect(tmp_path / "fsn.duckdb")
    fsn.load_one(connection, path, line, work=tmp_path)
    yield connection
    connection.close()


def test_every_table_is_loaded_with_its_dataset(loaded):
    for table, rows in {"sub": 2, "num": 4, "pre": 1, "tag": 1, "txt": 1, "dim": 1,
                        "ren": 1}.items():
        assert loaded.execute(f"SELECT count(*), count(dataset) FROM {table} "
                              "WHERE dataset = '2011q2'").fetchone() == (rows, rows)


def test_every_row_that_has_an_accession_carries_its_filed_date(loaded):
    import datetime as dt
    for table in fsn.BY_ACCESSION:
        dates = dict(loaded.execute(f"SELECT DISTINCT adsh, filed_date FROM {table}").fetchall())
        assert dates[CELGENE] == dt.date(2011, 5, 5)
    assert dict(loaded.execute("SELECT adsh, filed_date FROM sub").fetchall()) == {
        CELGENE: dt.date(2011, 5, 5), EXTRA_SPACE: dt.date(2011, 5, 6)}


def test_a_dictionary_row_carries_the_last_filed_date_of_its_data_set(loaded):
    import datetime as dt
    for table in fsn.BY_DATASET:
        assert loaded.execute(f"SELECT DISTINCT filed_through FROM {table}").fetchall() == [
            (dt.date(2011, 5, 6),)]


def test_a_value_is_loaded_as_filed(loaded):
    assert loaded.execute("SELECT value FROM num WHERE adsh = ? AND tag = 'Revenues'",
                          [CELGENE]).fetchall() == [("1125281000.0000",)]


def test_the_loaded_ledger_names_the_zip(loaded):
    dataset, name, _, rows, _ = loaded.execute("SELECT * FROM loaded").fetchone()
    assert (dataset, name) == ("2011q2", "2011q2_notes.zip")
    assert json.loads(rows)["num"] == 4


def test_a_data_set_whose_loaded_rows_differ_from_its_count_loads_nothing(tmp_path):
    pytest.importorskip("duckdb")
    # A num row whose accession has no sub row cannot be given a filed date.
    orphan = NUM_ROWS[0].replace(CELGENE, "0000000000-11-000000")
    path = planted_zip(tmp_path / "2011q2_notes.zip", num_rows=NUM_ROWS + [orphan])
    with zipfile.ZipFile(path) as archive:
        line = {"period": "2011q2", "name": path.name, "sha256": fsn.file_sha256(path),
                "rows": fsn.count_rows(archive)}
    connection = fsn._connect(tmp_path / "fsn.duckdb")
    with pytest.raises(ValueError, match="rows loaded differ"):
        fsn.load_one(connection, path, line, work=tmp_path)
    tables = {row[0] for row in connection.execute(
        "SELECT table_name FROM information_schema.tables").fetchall()}
    for table in tables - {"loaded"}:
        assert connection.execute(f"SELECT count(*) FROM {table}").fetchone()[0] == 0
    assert connection.execute("SELECT count(*) FROM loaded").fetchone()[0] == 0
    connection.close()


def test_load_skips_a_data_set_already_loaded_and_refuses_an_unverified_zip(tmp_path):
    pytest.importorskip("duckdb")
    zips = tmp_path / "zips"
    zips.mkdir()
    path = planted_zip(zips / "2011q2_notes.zip")
    with zipfile.ZipFile(path) as archive:
        counts = fsn.count_rows(archive)
    index = tmp_path / "index"
    fsn.append_index({"period": "2011q2", "name": path.name, "sha256": fsn.file_sha256(path),
                      "rows": counts}, index)
    fsn.append_index({"period": "2011q3", "name": "2011q3_notes.zip", "sha256": "0" * 64,
                      "rows": {}}, index)
    db = tmp_path / "fsn.duckdb"
    unlimited = lambda _: 10**13  # noqa: E731
    first = fsn.load(db=db, zips=zips, index_dir=index, free=unlimited)
    second = fsn.load(db=db, zips=zips, index_dir=index, free=unlimited)
    assert first == second == ["2011q3: " + str(zips / "2011q3_notes.zip")
                               + " is not the indexed zip; run fetch first"]
    import duckdb
    connection = duckdb.connect(str(db))
    assert connection.execute("SELECT count(*) FROM num").fetchone()[0] == 4
    connection.close()


# -- the ten values --------------------------------------------------------------

# Copied from Celgene's companyfacts document, keys and all.
COMPANYFACTS = {"cik": 816284, "entityName": "CELGENE CORP /DE/", "facts": {"us-gaap": {
    "AccountsPayableCurrent": {"units": {"USD": [
        {"end": "2010-12-31", "val": 94465000, "accn": CELGENE, "fy": 2011, "fp": "Q1",
         "form": "10-Q", "filed": "2011-05-05"}]}},
    "Revenues": {"units": {"USD": [
        {"start": "2010-01-01", "end": "2010-03-31", "val": 791254000, "accn": CELGENE,
         "fy": 2011, "fp": "Q1", "form": "10-Q", "filed": "2011-05-05"},
        {"start": "2011-01-01", "end": "2011-03-31", "val": 1125281000, "accn": CELGENE,
         "fy": 2011, "fp": "Q1", "form": "10-Q", "filed": "2011-05-05"}]}}}}}


def value(tag, ddate, qtrs, amount, accession=CELGENE):
    return {"accession": accession, "cik": 816284, "tag": tag, "version": "us-gaap/2009",
            "ddate": ddate, "qtrs": qtrs, "uom": "USD", "value": amount}


def test_an_instant_value_matches_its_companyfacts_row():
    found = fsn.lookup(COMPANYFACTS, value("AccountsPayableCurrent", "20101231", 0,
                                           "94465000.0000"))
    assert found["result"] == "match" and found["companyfacts"]["val"] == 94465000


def test_a_duration_matches_the_row_whose_start_is_a_quarter_back():
    found = fsn.lookup(COMPANYFACTS, value("Revenues", "20110331", 1, "1125281000.0000"))
    assert found["result"] == "match"
    assert found["companyfacts"]["start"] == "2011-01-01"


def test_a_different_number_is_reported_as_one():
    found = fsn.lookup(COMPANYFACTS, value("Revenues", "20110331", 1, "1125281001.0000"))
    assert found["result"] == "different_value"


def test_a_fact_companyfacts_does_not_hold_is_absent():
    assert fsn.lookup(COMPANYFACTS, value("Revenues", "20110331", 4, "1125281000.0000"))[
        "result"] == "absent"
    assert fsn.lookup(COMPANYFACTS, value("Revenues", "20110331", 1, "1125281000.0000",
                                          accession=EXTRA_SPACE))["result"] == "absent"


class Served:
    def __init__(self, documents):
        self.documents, self.asked = documents, []

    def get_json(self, url):
        self.asked.append(url)
        return self.documents[url]


def test_reconcile_checks_the_lowest_ranked_across_data_sets_and_appends_a_record(tmp_path):
    celgene = value("AccountsPayableCurrent", "20101231", 0, "94465000.0000")
    fsn.append_index({"period": "2011q2", "candidates": [
        dict(celgene, rank="b"), dict(celgene, rank="d", value="1.0000")]}, tmp_path)
    fsn.append_index({"period": "2012q1", "candidates": [
        dict(value("Revenues", "20110331", 1, "1125281000.0000"), rank="a")]}, tmp_path)
    fetcher = Served({"https://data.sec.gov/api/xbrl/companyfacts/CIK0000816284.json":
                      COMPANYFACTS})
    record = fsn.reconcile(fetcher, index_dir=tmp_path, size=2)
    assert [entry["fsn"]["rank"] for entry in record["checked"]] == ["a", "b"]
    assert [entry["result"] for entry in record["checked"]] == ["match", "match"]
    assert record["matched"] == 2 and record["pool"] == 3
    assert len(fetcher.asked) == 1
    written = (tmp_path / fsn.RECONCILIATION).read_text().splitlines()
    assert len(written) == 1 and json.loads(written[0])["matched"] == 2


def test_rows_splits_on_tabs_and_keeps_empty_fields(tmp_path):
    path = planted_zip(tmp_path / "p.zip")
    with zipfile.ZipFile(path) as archive:
        header, body = fsn.rows(archive, "num")
        first = next(body)
    assert len(header) == len(first) == 16
    assert dict(zip(header, first))["coreg"] == ""


def test_member_finds_a_table_by_its_stem(tmp_path):
    path = tmp_path / "p.zip"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("num.txt", NUM_HEADER + "\n")
    with zipfile.ZipFile(path) as archive:
        assert fsn.member(archive, "num") == "num.txt"
        with pytest.raises(KeyError):
            fsn.member(archive, "txt")


# -- the download ----------------------------------------------------------------

class Response:
    """What `urlopen` hands back: a promised length and the bytes that came."""

    def __init__(self, body: bytes, promised: int | None):
        self.body, self.headers = io.BytesIO(body), {}
        if promised is not None:
            self.headers["Content-Length"] = str(promised)

    def read(self, size=-1):
        return self.body.read(size)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def test_a_download_that_stops_short_of_its_promised_length_is_refused(tmp_path, monkeypatch):
    # 2012q3 on 2026-09-28: the connection closed early and nothing said so.
    monkeypatch.setattr(fsn.urllib.request, "urlopen",
                        lambda request, timeout: Response(b"PK\x03\x04 half", 461_466_618))
    monkeypatch.setattr(fsn.time, "sleep", lambda seconds: None)
    with pytest.raises(OSError, match="9 of the 461,466,618 bytes promised arrived"):
        fsn.download("https://x/2012q3_notes.zip", tmp_path / "z.zip", "ua")
    assert list(tmp_path.iterdir()) == []


def test_a_download_is_hashed_as_it_arrives(tmp_path, monkeypatch):
    served = iter([Response(b"short", 7), Response(b"payload", 7)])
    monkeypatch.setattr(fsn.urllib.request, "urlopen", lambda request, timeout: next(served))
    monkeypatch.setattr(fsn.time, "sleep", lambda seconds: None)
    assert fsn.download("https://x/z.zip", tmp_path / "z.zip", "ua") == (
        hashlib.sha256(b"payload").hexdigest(), 7)
    assert (tmp_path / "z.zip").read_bytes() == b"payload"
