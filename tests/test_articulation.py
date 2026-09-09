"""The articulation rows, against the statements they are supposed to reproduce.

The expected values here are not this module's output. They are the lines two
companies printed on two facing pages of four filings -- Apple's 10-K for the
year ended 27 September 2025 and its 10-Q for the nine months ended 27 June
2026, Littelfuse's 10-K for the year ended 27 December 2025 and its 10-Q for the
three months ended 28 March 2026 -- typed in from the committed documents and
differenced here, term by term, so a reader can follow the arithmetic without
running anything. Each of the twelve account-periods carries four numbers off
the statements: the two balance-sheet ends, the cash-flow line as the statement
prints it, and the same line as the us-gaap element states it.

**The sign is the thing a hand check exists to catch.** A cash-flow statement
prints the effect on cash, so for an asset the printed figure is the change in
the account negated -- Apple prints `Accounts receivable, net (6,682)` for a
year in which receivables rose by 6,682 -- while for a liability the printed
figure and the element agree. `AS_PRINTED` holds the figure as the page shows
it and the sign relation is asserted, so a module that read the element with the
wrong sign would pass no row here.

The other half is what the module refuses to compute, and every one of those is
asserted too: the two filings companyfacts has not loaded, the three companies
whose cash-flow statement states a wider line than the account, and Palo Alto's
missing inventory line. An absence has to arrive as an absence with a reason.
None of them may arrive as a zero, and `test_no_absence_arrives_as_a_zero` is
what makes that an assertion rather than a hope.

`test_littelfuse_receivables_gap_nets_out_the_acquisition_it_discloses` is a
strict expected failure. Littelfuse's 10-K discloses 16,798,000 of receivables
and 23,363,000 of inventory acquired with Basler Electric; both are in the
instance against `us-gaap:BusinessAcquisitionAxis`, neither is in companyfacts,
and this module reads companyfacts. So over half of each reported gap is an
acquisition the filing discloses, the row says the gap is before acquisitions,
and the mark turns the suite red on the day the amounts are read out of the
instance.
"""

from __future__ import annotations

import datetime as dt
import functools
import gzip
import json
from pathlib import Path

import pytest

from src import articulation, cutoff_guard
from src.fetch_fixtures import TICKERS

FIXTURES = Path(__file__).resolve().parent / "fixtures"

APPLE_ANNUAL = "0000320193-25-000079"        # 10-K filed 2025-10-31
APPLE_QUARTERLY = "0000320193-26-000020"     # 10-Q filed 2026-07-31
LITTELFUSE_ANNUAL = "0001628280-26-009585"   # 10-K filed 2026-02-19
LITTELFUSE_QUARTERLY = "0001628280-26-031041"  # 10-Q filed 2026-05-06

# The two filings in no companyfacts row at all, which
# `tests/test_fetch_companyfacts.py` records as EDGAR's own loading lag.
NOT_IN_COMPANYFACTS = (("CARR", "0001783180-26-000032"),
                       ("LFUS", "0001628280-26-050481"))


@functools.lru_cache(maxsize=None)
def payload(ticker: str) -> dict:
    return articulation.articulation(ticker)


def row(ticker: str, identifier: str) -> dict:
    found = [entry for entry in payload(ticker)["rows"] if entry["id"] == identifier]
    assert len(found) == 1, f"{identifier}: {len(found)} rows carry this id"
    return found[0]


def coverage(ticker: str, accession: str, account: str | None) -> dict:
    found = [entry for entry in payload(ticker)["coverage"]
             if entry["accession"] == accession and entry["account"] == account]
    assert len(found) == 1, f"{accession} {account}: {len(found)} coverage entries"
    return found[0]


# --- the statements, typed in ------------------------------------------------
#
# Apple, in millions, from `tests/fixtures/AAPL/10-K/aapl-20250927.htm` and
# `tests/fixtures/AAPL/10-Q/aapl-20260627.htm`; Littelfuse, in thousands, from
# `tests/fixtures/LFUS/10-K/lfus-20251227.htm.gz` and
# `tests/fixtures/LFUS/10-Q/lfus-20260328.htm`. Written in whole dollars, which
# is the unit the us-gaap elements carry.
#
# CONSOLIDATED BALANCE SHEETS, Apple, September 27, 2025 and September 28, 2024
#     Accounts receivable, net    39,777    33,410
#     Inventories                  5,718     7,286
#     Accounts payable            69,860    68,960
# CONSOLIDATED STATEMENTS OF CASH FLOWS, Apple, year ended September 27, 2025
#     Accounts receivable, net    (6,682)
#     Inventories                  1,400
#     Accounts payable               902
#
# CONDENSED CONSOLIDATED BALANCE SHEETS, Apple, June 27, 2026 and September 27, 2025
#     Accounts receivable, net    31,398    39,777
#     Inventories                 11,092     5,718
#     Accounts payable            64,525    69,860
# CONDENSED CONSOLIDATED STATEMENTS OF CASH FLOWS, Apple, nine months ended June 27, 2026
#     Accounts receivable, net     8,316
#     Inventories                 (5,461)
#     Accounts payable            (5,203)
#
# CONSOLIDATED BALANCE SHEETS, Littelfuse, December 27, 2025 and December 28, 2024
#     Trade receivables          363,215   294,371
#     Inventories                416,472   416,273
#     Accounts payable           211,079   188,359
# CONSOLIDATED STATEMENTS OF CASH FLOWS, Littelfuse, fiscal year ended December 27, 2025
#     Trade receivables         (36,401)
#     Inventories                40,181
#     Accounts payable           11,342
#
# CONDENSED CONSOLIDATED BALANCE SHEETS, Littelfuse, March 28, 2026 and December 27, 2025
#     Trade receivables          380,963   363,215
#     Inventories                418,922   416,472
#     Accounts payable           222,666   211,079
# CONDENSED CONSOLIDATED STATEMENTS OF CASH FLOWS, Littelfuse, three months ended March 28, 2026
#     Trade receivables         (21,783)
#     Inventories                (6,740)
#     Accounts payable            8,567

MILLION = 1_000_000
THOUSAND = 1_000

# ticker, accession, account, period, opening, closing, as printed on the
# cash-flow statement, the us-gaap element, and the gap differenced by hand.
BY_HAND = [
    ("AAPL", APPLE_ANNUAL, "receivables", "2024-09-29..2025-09-27",
     33_410 * MILLION, 39_777 * MILLION, -6_682 * MILLION, 6_682 * MILLION,
     -315 * MILLION),
    ("AAPL", APPLE_ANNUAL, "inventory", "2024-09-29..2025-09-27",
     7_286 * MILLION, 5_718 * MILLION, 1_400 * MILLION, -1_400 * MILLION,
     -168 * MILLION),
    ("AAPL", APPLE_ANNUAL, "payables", "2024-09-29..2025-09-27",
     68_960 * MILLION, 69_860 * MILLION, 902 * MILLION, 902 * MILLION,
     -2 * MILLION),

    ("AAPL", APPLE_QUARTERLY, "receivables", "2025-09-28..2026-06-27",
     39_777 * MILLION, 31_398 * MILLION, 8_316 * MILLION, -8_316 * MILLION,
     -63 * MILLION),
    ("AAPL", APPLE_QUARTERLY, "inventory", "2025-09-28..2026-06-27",
     5_718 * MILLION, 11_092 * MILLION, -5_461 * MILLION, 5_461 * MILLION,
     -87 * MILLION),
    ("AAPL", APPLE_QUARTERLY, "payables", "2025-09-28..2026-06-27",
     69_860 * MILLION, 64_525 * MILLION, -5_203 * MILLION, -5_203 * MILLION,
     -132 * MILLION),

    ("LFUS", LITTELFUSE_ANNUAL, "receivables", "2024-12-29..2025-12-27",
     294_371 * THOUSAND, 363_215 * THOUSAND, -36_401 * THOUSAND,
     36_401 * THOUSAND, 32_443 * THOUSAND),
    ("LFUS", LITTELFUSE_ANNUAL, "inventory", "2024-12-29..2025-12-27",
     416_273 * THOUSAND, 416_472 * THOUSAND, 40_181 * THOUSAND,
     -40_181 * THOUSAND, 40_380 * THOUSAND),
    ("LFUS", LITTELFUSE_ANNUAL, "payables", "2024-12-29..2025-12-27",
     188_359 * THOUSAND, 211_079 * THOUSAND, 11_342 * THOUSAND,
     11_342 * THOUSAND, 11_378 * THOUSAND),

    ("LFUS", LITTELFUSE_QUARTERLY, "receivables", "2025-12-28..2026-03-28",
     363_215 * THOUSAND, 380_963 * THOUSAND, -21_783 * THOUSAND,
     21_783 * THOUSAND, -4_035 * THOUSAND),
    ("LFUS", LITTELFUSE_QUARTERLY, "inventory", "2025-12-28..2026-03-28",
     416_472 * THOUSAND, 418_922 * THOUSAND, -6_740 * THOUSAND,
     6_740 * THOUSAND, -4_290 * THOUSAND),
    ("LFUS", LITTELFUSE_QUARTERLY, "payables", "2025-12-28..2026-03-28",
     211_079 * THOUSAND, 222_666 * THOUSAND, 8_567 * THOUSAND,
     8_567 * THOUSAND, 3_020 * THOUSAND),
]

BY_HAND_IDS = [f"{ticker}-{account}-{period}"
               for ticker, _, account, period, *_ in BY_HAND]

# Which way the statement's printed figure runs against the element. An asset
# rising is a use of cash and prints negated; a liability rising is a source of
# cash and prints as it stands.
PRINTS_NEGATED = {"receivables": True, "inventory": True, "payables": False}


# --- the hand difference -----------------------------------------------------

@pytest.mark.parametrize(
    "ticker,accession,account,period,opening,closing,as_printed,element,gap",
    BY_HAND, ids=BY_HAND_IDS)
def test_the_gap_is_the_hand_difference_of_the_two_statements(
        ticker, accession, account, period, opening, closing, as_printed, element, gap):
    """closing − opening − the cash-flow line, off the filing's own two pages."""
    assert closing - opening - element == gap, (
        "the three numbers typed in off the statements do not difference to the "
        "gap written beside them")
    found = row(ticker, f"{accession}:articulation:{account}:{period}")
    assert found["balance_sheet_change"] == closing - opening
    assert found["cash_flow_change"] == element
    assert found["gap"] == gap


@pytest.mark.parametrize(
    "ticker,accession,account,period,opening,closing,as_printed,element,gap",
    BY_HAND, ids=BY_HAND_IDS)
def test_the_cash_flow_line_is_read_with_the_statements_own_sign(
        ticker, accession, account, period, opening, closing, as_printed, element, gap):
    """An asset's line prints negated; a liability's does not."""
    expected = -element if PRINTS_NEGATED[account] else element
    assert as_printed == expected, (
        f"{account} prints {as_printed:,} on the statement and the us-gaap element "
        f"is {element:,}; one of the two was typed in wrong")
    found = row(ticker, f"{accession}:articulation:{account}:{period}")
    assert found["inputs"]["cash_flow"]["value"] == element


@pytest.mark.parametrize(
    "ticker,accession,account,period,opening,closing,as_printed,element,gap",
    BY_HAND, ids=BY_HAND_IDS)
def test_the_balance_sheet_ends_are_the_two_the_filing_prints(
        ticker, accession, account, period, opening, closing, as_printed, element, gap):
    found = row(ticker, f"{accession}:articulation:{account}:{period}")
    assert found["inputs"]["balance_sheet_opening"]["value"] == opening
    assert found["inputs"]["balance_sheet_closing"]["value"] == closing


# --- the whole fixture set, against companyfacts itself ----------------------

@functools.lru_cache(maxsize=None)
def companyfacts(ticker: str) -> dict:
    """`(tag, accession, start, end)` → value, read here rather than through src.

    A second reader of the same document, so a row's fact ids are checked
    against the record and not against the index the module built from it.
    """
    entry = [document for document in
             json.loads((FIXTURES / ticker / "manifest.json").read_text())["documents"]
             if document["form"] == "companyfacts"][0]
    raw = (FIXTURES / ticker / entry["path"]).read_bytes()
    record = json.loads(gzip.decompress(raw) if entry["stored"] == "gzip" else raw)
    held = {}
    for tag, concept in record["facts"]["us-gaap"].items():
        for fact in concept["units"].get("USD", []):
            held[(tag, fact["accn"], fact.get("start"), fact["end"])] = fact["val"]
    return held


@functools.lru_cache(maxsize=None)
def tags_in(ticker: str, accession: str) -> frozenset[str]:
    """Every us-gaap concept one filing reported, read straight from the record."""
    return frozenset(tag for tag, accn, _, _ in companyfacts(ticker) if accn == accession)


def all_rows() -> list[tuple[str, dict]]:
    return [(ticker, entry) for ticker in TICKERS for entry in payload(ticker)["rows"]]


def test_every_company_produces_rows():
    """A silent empty result would pass every assertion below it."""
    for ticker in TICKERS:
        assert payload(ticker)["rows"], f"{ticker}: no articulation row at all"


def test_every_fact_a_row_names_is_in_companyfacts_at_that_value():
    """The three numbers behind every gap, looked up where they came from."""
    wrong = []
    for ticker, entry in all_rows():
        held = companyfacts(ticker)
        cash_flow = entry["inputs"]["cash_flow"]
        start, end = entry["start"], entry["end"]
        looked_up = {
            (cash_flow["tag"], entry["accession"], start, end): cash_flow["value"]}
        for side in ("balance_sheet_opening", "balance_sheet_closing"):
            fact = entry["inputs"][side]
            looked_up[(fact["tag"], entry["accession"], None, fact["period"])] = \
                fact["value"]
        for key, value in looked_up.items():
            if held.get(key) != value:
                wrong.append(f"{ticker} {entry['id']}: {key} is {held.get(key)} in "
                             f"companyfacts and {value} in the row")
    assert wrong == [], "\n".join(wrong)


def test_every_gap_is_the_two_changes_and_the_adjustments_and_nothing_else():
    wrong = []
    for ticker, entry in all_rows():
        opening = entry["inputs"]["balance_sheet_opening"]["value"]
        closing = entry["inputs"]["balance_sheet_closing"]["value"]
        netted = sum(fact["value"] for fact in entry["netted"])
        gap = (closing - opening) - netted - entry["cash_flow_change"]
        if entry["balance_sheet_change"] != closing - opening or entry["gap"] != gap:
            wrong.append(f"{ticker} {entry['id']}: {entry['gap']} against {gap}")
    assert wrong == [], "\n".join(wrong)


def test_a_period_is_paired_with_the_balance_sheet_day_before_it_opens():
    wrong = []
    for ticker, entry in all_rows():
        opening = entry["inputs"]["balance_sheet_opening"]["period"]
        closing = entry["inputs"]["balance_sheet_closing"]["period"]
        day_before = (dt.date.fromisoformat(entry["start"]) - dt.timedelta(days=1))
        if opening != day_before.isoformat() or closing != entry["end"]:
            wrong.append(f"{ticker} {entry['id']}: {opening}..{closing} against "
                         f"{entry['start']}..{entry['end']}")
    assert wrong == [], "\n".join(wrong)


def test_a_rows_three_facts_all_come_from_the_one_filing():
    wrong = []
    for ticker, entry in all_rows():
        for name, fact in entry["inputs"].items():
            if not fact["id"].startswith(f"{entry['accession']}:facts:"):
                wrong.append(f"{ticker} {entry['id']}: {name} is {fact['id']}")
    assert wrong == [], "\n".join(wrong)


def test_the_two_balance_sheet_ends_come_from_one_concept():
    """A change from one concept to another is not a change in the account."""
    wrong = []
    for ticker, entry in all_rows():
        opening = entry["inputs"]["balance_sheet_opening"]["tag"]
        closing = entry["inputs"]["balance_sheet_closing"]["tag"]
        if opening != closing:
            wrong.append(f"{ticker} {entry['id']}: {opening} against {closing}")
    assert wrong == [], "\n".join(wrong)


def test_coverage_names_every_account_of_every_filing_once():
    """No account of no filing goes unaccounted for, filled or not."""
    for ticker in TICKERS:
        held = payload(ticker)
        absent = {entry["accession"] for entry in held["coverage"]
                  if entry["status"] == "absent_from_companyfacts"}
        wanted = {(accession, account)
                  for accession in held["source"]["filings"] if accession not in absent
                  for account in articulation.ACCOUNTS}
        wanted |= {(accession, None) for accession in absent}
        named = [(entry["accession"], entry["account"]) for entry in held["coverage"]]
        assert len(named) == len(set(named)), f"{ticker}: a repeated coverage entry"
        assert set(named) == wanted, f"{ticker}: coverage and the filings disagree"


def test_the_payload_is_the_same_twice():
    """Deterministic by construction: two runs, byte for byte."""
    once = articulation.render(articulation.articulation("AAPL"))
    twice = articulation.render(articulation.articulation("AAPL"))
    assert once == twice
    assert json.loads(once)["rows"][0]["id"].startswith(f"{APPLE_ANNUAL}:articulation:")


def test_no_two_rows_carry_the_same_id():
    """`docs/INPUT_SPEC.md` §2.2 gives a row an id its reader can quote."""
    for ticker in TICKERS:
        ids = [entry["id"] for entry in payload(ticker)["rows"]]
        assert len(ids) == len(set(ids)), f"{ticker}: a repeated articulation id"


def test_the_reads_line_carries_the_gap_and_what_it_is_before():
    """The quotable sentence cannot be quoted without its qualifier."""
    for ticker, entry in all_rows():
        assert f"{entry['gap']:,}" in entry["reads"]
        for absent in entry["not_netted"]:
            assert absent["kind"].replace("_", " ") in entry["reads"]


# --- the absences ------------------------------------------------------------

@pytest.mark.parametrize("ticker,accession", NOT_IN_COMPANYFACTS)
def test_a_filing_companyfacts_has_not_loaded_is_reported_absent(ticker, accession):
    assert tags_in(ticker, accession) == frozenset(), (
        "the premise of this test is that companyfacts holds nothing under this "
        "accession; it holds something, so the absence is not the source's")
    entry = coverage(ticker, accession, None)
    assert entry["status"] == "absent_from_companyfacts"
    assert accession in entry["reason"]
    assert not [found for found in payload(ticker)["rows"]
                if found["accession"] == accession]


def test_no_absence_arrives_as_a_zero():
    """Nothing missing is filled in: an unfilled coverage entry carries no number."""
    for ticker in TICKERS:
        for entry in payload(ticker)["coverage"]:
            if entry["status"] == "filled":
                continue
            assert entry.get("reason"), f"{ticker} {entry['accession']}: no reason"
            assert "periods" not in entry, (
                f"{ticker} {entry['accession']} {entry['account']}: an unfilled "
                f"coverage entry carries periods")


@pytest.mark.parametrize("ticker,accession", [
    ("CARR", "0001783180-26-000008"), ("CARR", "0001783180-26-000026"),
    ("CIEN", "0001628280-25-056698"), ("CIEN", "0001628280-26-015152"),
    ("CIEN", "0001628280-26-040767")])
def test_payables_and_accrued_liabilities_together_is_refused(ticker, accession):
    """A wider cash-flow line is not this account's line, and is not differenced."""
    stated = tags_in(ticker, accession)
    assert "IncreaseDecreaseInAccountsPayableAndAccruedLiabilities" in stated
    assert not stated & {"IncreaseDecreaseInAccountsPayable",
                         "IncreaseDecreaseInAccountsPayableTrade"}
    entry = coverage(ticker, accession, "payables")
    assert entry["status"] == "stated_wider"
    assert "IncreaseDecreaseInAccountsPayableAndAccruedLiabilities" in entry["reason"]
    assert not [found for found in payload(ticker)["rows"]
                if found["accession"] == accession and found["account"] == "payables"]


@pytest.mark.parametrize("accession", ["0001104659-26-058482", "0001104659-26-093266"])
@pytest.mark.parametrize("account", ["receivables", "inventory", "payables"])
def test_one_working_capital_line_for_everything_is_refused(accession, account):
    """ESCO's quarterlies state `IncreaseDecreaseInOperatingCapital` and nothing else."""
    stated = tags_in("ESE", accession)
    assert "IncreaseDecreaseInOperatingCapital" in stated
    assert not stated & {"IncreaseDecreaseInAccountsReceivable",
                         "IncreaseDecreaseInReceivables",
                         "IncreaseDecreaseInInventories",
                         "IncreaseDecreaseInAccountsPayable"}
    entry = coverage("ESE", accession, account)
    assert entry["status"] == "stated_wider"
    assert "IncreaseDecreaseInOperatingCapital" in entry["reason"]


@pytest.mark.parametrize("accession,on_the_balance_sheet", [
    ("0001327567-25-000027", True),    # the 10-K carries an inventory balance
    ("0001327567-26-000005", False),   # the quarterlies carry no inventory at all
    ("0001327567-26-000015", False)])
def test_a_filing_with_no_inventory_line_says_so(accession, on_the_balance_sheet):
    """Palo Alto states no change in inventory in any of the three filings."""
    stated = tags_in("PANW", accession)
    assert ("InventoryNet" in stated) is on_the_balance_sheet
    assert "IncreaseDecreaseInInventories" not in stated
    entry = coverage("PANW", accession, "inventory")
    assert entry["status"] == "no_cash_flow_line"
    assert "IncreaseDecreaseInInventories" in entry["reason"]


def test_an_earlier_cash_flow_column_is_counted_and_not_differenced():
    """A 10-K prints three cash-flow years and two balance sheets.

    The two earlier columns have no opening balance in that filing, so they
    carry no row -- and are named in `not_paired` rather than dropped.
    """
    entry = coverage("AAPL", APPLE_ANNUAL, "receivables")
    assert entry["periods"] == ["2024-09-29..2025-09-27"]
    assert [absent["period"] for absent in entry["not_paired"]] == [
        "2022-09-25..2023-09-30", "2023-10-01..2024-09-28"]


def test_a_cash_flow_line_with_no_balance_sheet_behind_it_is_named_and_not_zeroed():
    """No filing in this fixture set is that shape, so the branch is built one.

    A filing that states the change and carries one end of the period is a
    filing this check cannot make, and the coverage line has to say so rather
    than report a gap against a missing opening balance.
    """
    held = {
        "IncreaseDecreaseInInventories": {
            "durations": {("2025-01-01", "2025-12-31"): 400}, "instants": {}},
        "InventoryNet": {"durations": {}, "instants": {"2025-12-31": 1_500}},
    }
    filing = {"accession": "0000000000-00-000000", "form": "10-K",
              "filing_date": "2026-02-01", "report_date": "2025-12-31"}
    rows, entry = articulation.account_rows(held, filing, "inventory")
    assert rows == []
    assert entry["status"] == "no_paired_period"
    assert "IncreaseDecreaseInInventories" in entry["reason"]
    assert [absent["period"] for absent in entry["not_paired"]] == [
        "2025-01-01..2025-12-31"]


def test_a_company_with_no_companyfacts_fixture_is_an_error_and_not_an_empty_result(
        tmp_path):
    (tmp_path / "AAPL").mkdir()
    with pytest.raises(cutoff_guard.CutoffGuardError):
        articulation.articulation("AAPL", tmp_path)


# --- the gate ----------------------------------------------------------------

def test_the_record_is_read_through_the_gate_and_not_around_it():
    """`cutoff_guard.recording()` sees the read, which a borrowed helper would not.

    `tests/test_fetch_companyfacts.py` fails any module but the fetcher that
    reaches a fixture through `src/fetch_fixtures.py`'s helpers, because the
    bypass scan reads the call and cannot see one made through them.
    """
    with cutoff_guard.recording() as opened:
        articulation.articulation("AAPL")
    assert [path.name for path in opened] == ["companyfacts.json.gz"]


def test_a_cutoff_earlier_than_the_record_refuses_it_rather_than_filtering_it():
    """companyfacts is a catalogue, and the gate has no catalogue route for it."""
    with pytest.raises(cutoff_guard.CutoffViolationError):
        articulation.articulation("AAPL", cutoff="2026-01-01")


def test_a_filing_made_after_the_cutoff_is_not_read_at_all():
    """Carrier's July quarterly is past a 30 April cutoff, so it is not a filing here.

    Under the fixture set's own as-of date it is a filing companyfacts has not
    loaded; under this one it is not an input, which is a different answer and
    the record says which.
    """
    payload = articulation.articulation("CARR", cutoff="2026-04-30")
    assert payload["source"]["filings"] == ["0001783180-26-000008",
                                            "0001783180-26-000026"]
    assert not [entry for entry in payload["coverage"]
                if entry["status"] == "absent_from_companyfacts"]


# --- netting -----------------------------------------------------------------

def test_every_row_names_the_adjustments_it_could_not_net_out():
    """Across these twelve filings that is both of them, every time.

    A purchase-price allocation is reported against the acquisition axis and
    companyfacts holds the entity-wide fact alone, and the taxonomy has no
    concept for the foreign-exchange effect on a working-capital account. So
    every gap here is a gap before both, and every row says so.
    """
    for ticker, entry in all_rows():
        assert entry["netted"] == []
        assert [absent["kind"] for absent in entry["not_netted"]] == [
            "acquisitions", "foreign_exchange"]


def test_a_disclosed_acquisition_is_netted_out_of_the_balance_sheet_change():
    """By construction, on a record with an acquired inventory amount planted in.

    100 of inventory acquired inside the period is 100 of the balance-sheet
    change that never passed through the cash-flow statement, so the gap is the
    difference less that amount and not more.
    """
    accession, acquired = "0000000000-00-000000", (
        "BusinessCombinationRecognizedIdentifiableAssetsAcquired"
        "AndLiabilitiesAssumedInventory")
    held = {
        "IncreaseDecreaseInInventories": {
            "durations": {("2025-01-01", "2025-12-31"): 400}, "instants": {}},
        "InventoryNet": {
            "durations": {}, "instants": {"2024-12-31": 1_000, "2025-12-31": 1_500}},
        acquired: {"durations": {}, "instants": {"2025-06-30": 100}},
    }
    filing = {"accession": accession, "form": "10-K",
              "filing_date": "2026-02-01", "report_date": "2025-12-31"}
    rows, entry = articulation.account_rows(held, filing, "inventory")

    assert entry["status"] == "filled"
    assert len(rows) == 1
    assert rows[0]["balance_sheet_change"] == 1_500 - 1_000
    assert rows[0]["gap"] == (1_500 - 1_000) - 100 - 400
    assert [(fact["kind"], fact["value"]) for fact in rows[0]["netted"]] == [
        ("acquisitions", 100)]
    assert [absent["kind"] for absent in rows[0]["not_netted"]] == ["foreign_exchange"]


def test_an_acquisition_outside_the_period_is_not_netted_out():
    """The measurement-period table of an earlier year is not this year's cause."""
    acquired = ("BusinessCombinationRecognizedIdentifiableAssetsAcquired"
                "AndLiabilitiesAssumedInventory")
    held = {
        "IncreaseDecreaseInInventories": {
            "durations": {("2025-01-01", "2025-12-31"): 400}, "instants": {}},
        "InventoryNet": {
            "durations": {}, "instants": {"2024-12-31": 1_000, "2025-12-31": 1_500}},
        acquired: {"durations": {}, "instants": {"2023-06-30": 100}},
    }
    filing = {"accession": "0000000000-00-000000", "form": "10-K",
              "filing_date": "2026-02-01", "report_date": "2025-12-31"}
    rows, _ = articulation.account_rows(held, filing, "inventory")
    assert rows[0]["netted"] == []
    assert rows[0]["gap"] == (1_500 - 1_000) - 400


def test_littelfuse_receivables_gap_is_reported_before_the_acquisition_it_discloses():
    """The adverse result, stated: most of the gap is an acquisition, and unreachable.

    Littelfuse acquired Basler Electric on 10 December 2025, inside this fiscal
    year, and its 10-K's purchase-price allocation states 16,798,000 of
    receivables acquired. companyfacts carries no entity-wide row for it, so the
    32,443,000 reported here is the gap before acquisitions and says so.
    """
    found = row("LFUS", f"{LITTELFUSE_ANNUAL}:articulation:receivables:"
                        f"2024-12-29..2025-12-27")
    assert found["gap"] == 32_443 * THOUSAND
    assert "acquisitions" in [absent["kind"] for absent in found["not_netted"]]
    assert "before acquisitions" in found["reads"]


@pytest.mark.xfail(strict=True, reason=(
    "the 16,798,000 of receivables acquired with Basler Electric is in the 10-K "
    "instance against us-gaap:BusinessAcquisitionAxis and companyfacts holds the "
    "entity-wide fact alone, so src/articulation.py cannot reach it from the "
    "record it reads; this mark comes off when the amount is read out of the "
    "instance"))
def test_littelfuse_receivables_gap_nets_out_the_acquisition_it_discloses():
    """Gap 32,443,000 less 16,798,000 acquired leaves 15,645,000."""
    found = row("LFUS", f"{LITTELFUSE_ANNUAL}:articulation:receivables:"
                        f"2024-12-29..2025-12-27")
    assert found["gap"] == 32_443 * THOUSAND - 16_798 * THOUSAND
