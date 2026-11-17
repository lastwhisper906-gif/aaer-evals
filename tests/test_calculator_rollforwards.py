"""One rollforward identity over every reserve family, judged against the filings.

docs/HEDGE_FUND_ANALYSIS.md section 5.3 (the reserve rows) and the task row "one
rollforward identity over every reserve family, with the release flag" of
docs/next_cycle_tasks.md. Python states, for each reserve family a filing tables as
a rollforward, the identity beginning + charged to expense + other - usage =
ending, whether it holds, and the measures read off it. Each expected value below
is from a source that is not the code it judges, and the arithmetic is written out.

- **Generac's warranty rollforward**, read by eye in its committed 10-K filed
  2026-02-18 (`tests/fixtures/GNRC/10-K/gnrc20251231_10k.htm.gz`), the note table
  as the filing prints it, in thousands of dollars:

      Year Ended December 31,             2025       2024       2023
      Balance at beginning of period   $ 110,987  $ 116,408  $ 138,011
      Payments                           (86,448)   (88,990)   (92,200)
      Provision for warranty issued       100,589     77,802     67,104
      Changes in estimates for
        pre-existing warranties             6,794      5,767      3,493
      Balance at end of period         $ 131,922  $ 110,987  $ 116,408

  The figures `docs/HEDGE_FUND_ANALYSIS.md` section 5.3 lists (110,987; (86,448);
  100,589; 6,794; 131,922). They foot by hand: 110,987 + 100,589 + 6,794 - 86,448 =
  131,922; for 2024, 116,408 + 77,802 + 5,767 - 88,990 = 110,987; for 2023,
  138,011 + 67,104 + 3,493 - 92,200 = 116,408. The facts' ids (instance contexts
  c140005329 to c140005341) are the ones the instance gives each printed cell.
  The same filing's Schedule II (note 195) is read by eye too: the allowance for
  credit losses 35,465 + 1,398 - 2,359 + 0 = 34,504 and the inventory valuation
  reserve 48,173 + 23,375 - 2,282 + 0 = 69,266.
- **Ciena's allowance**, read by eye in its committed 10-K filed 2025-12-12
  (`tests/fixtures/CIEN/10-K`), in thousands of dollars:

      Year Ended         Beginning Balance  Provisions  Net Deductions  Ending Balance
      October 28, 2023        10,958           5,718         5,022          11,654
      November 2, 2024        11,654           7,996         9,770           9,880
      November 1, 2025         9,880           4,226         2,894          11,212

  9,880 + 4,226 - 2,894 = 11,212; 11,654 + 7,996 - 9,770 = 9,880; 10,958 + 5,718 -
  5,022 = 11,654. Its inventory reserve table (beginning 107,173, provisions
  48,424, disposals 26,189, ending 129,408) foots only with the disposals row,
  which Ciena tags in its own namespace (`cien:InventoryValuationReservesDisposals`),
  so the rows Python may place give 107,173 + 48,424 = 155,597 against 129,408,
  a difference of -26,189 and a table the cell marks as not complete.
- **The ASU's own illustrative supplier-finance table**, planted: ASU 2022-04,
  https://viewpoint.pwc.com/dt/us/en/fasb_financial_accou/asus_fulltext/2022/asu2022-04/%41SU2022-04/liabilitiessuppfinprog.html
  "Confirmed obligations outstanding at the beginning of the year 733; invoices
  confirmed during the year 2,435; confirmed invoices paid during the year (2,315);
  confirmed obligations outstanding at the end of the year 853", and
  733 + 2,435 - 2,315 = 853.
- **A planted table that does not foot**: beginning 1,000, provision 400, translation
  (20), usage 300, stated ending 1,100. By hand 1,000 + 400 - 20 - 300 = 1,080, so
  the table is 20 above its rows.
- **A planted release** (a negative charge): beginning 500, provision (50), usage
  30, ending 420 (500 - 50 - 30 = 420). And **a planted fall while the base rose**:
  an inventory reserve 200 + 10 - 60 = 150 beside a gross inventory of 1,000 then
  1,200.
- **The printed sign of a translation row**, read by eye in four committed filings (the
  rendered table as `input_notes.md` prints it): Cisco's 10-K filed 2025-09-03, total
  column, "Foreign exchange and other" printed 3 and tagged -3 (`sign="-"`): 65 - 9 - 9 + 3
  = 50; Johnson Controls' 10-Q filed 2026-07-29, "Currency translation" printed (1) and
  tagged +1: 120 + 94 + 3 - 1 - 70 = 146; Logitech's 10-Q filed 2026-07-29, "Effects of
  foreign currency translation" printed 94 and tagged -94: 50,242 + 8,496 + 94 - 9,553 =
  49,279; Lennox's 10-K filed 2026-02-17, "Changes in foreign currency translation rates
  and other" printed (0.8) and tagged -0.8: 142.8 - 41.2 + 59.0 - 1.4 - 0.8 = 158.4.
- **Rows no role holds**, read by eye: Cisco's goodwill note (Splunk and other
  acquisitions on `BusinessAcquisitionAxis`; Americas 24,035 + 11,619 + 573 - 58 = 36,169,
  of which Python places 24,035 and (58)), Carrier's warranty note ("Reclassified to held
  for sale (7)", `carr:StandardAndExtendedProductDecreaseDueToDivestiture`), Dell's
  allowance note (fiscal 2024: 201 - 49 + 92 - 74 = 170, the (74) being `dell:...Other`),
  and TTM's supplier finance note (17,218 + 12,579 - 17,480 + 218 = 12,535 in thousands,
  the 218 the filer's exchange-rate effect).
"""

from __future__ import annotations

import datetime as dt
import gzip
import json
import re
import xml.etree.ElementTree as ET
from decimal import Decimal
from pathlib import Path

import pytest

from src import calculator, cutoff_guard, note_tables, rollforwards

FIXTURES = Path(__file__).resolve().parent / "fixtures"
ACCESSION = "0000000000-26-000001"
GNRC_ACCESSION = "0001437749-26-004568"
CIEN_ACCESSION = "0001628280-25-056698"


def tables_of(ticker: str, accession: str, cutoff: str) -> dict:
    """The note tables of one committed filing, as `note_tables.tables` reads them:
    every table paragraph of the inline document, numbered in document order (the
    committed fixtures hold no `input_notes.md` of these 10-Ks, so the paragraphs are
    the tables the filing itself prints)."""
    day = cutoff_guard.parse_date(cutoff, "cutoff")
    rows = {row["role"]: row for row in cutoff_guard.documents(ticker, fixtures_root=FIXTURES)
            if row.get("accession") == accession}
    html = cutoff_guard.load_bytes(rows["primary_html"]["full_path"], day, fixtures_root=FIXTURES)
    instance = cutoff_guard.load_bytes(rows["xbrl_instance"]["full_path"], day,
                                       fixtures_root=FIXTURES)
    paragraphs = [(f"{accession}:notes:{at}", text)
                  for at, text in enumerate(note_tables.inline_tables(html))
                  if text.startswith("|")]
    return note_tables.tables(paragraphs, html, instance, accession=accession, cutoff=cutoff)


@pytest.fixture(scope="module")
def generac():
    return rollforwards.build(tables_of("GNRC", GNRC_ACCESSION, "2026-02-18"))


@pytest.fixture(scope="module")
def ciena():
    return rollforwards.build(tables_of("CIEN", CIEN_ACCESSION, "2025-12-12"))


def series_of(result: dict, family: str, table: str) -> dict:
    return next(one for one in result[family]["series"] if one["table"] == table)


def period_of(series: dict, end: str) -> dict:
    return next(one for one in series["periods"] if one["period"]["end"] == end)


IX = "{http://www.xbrl.org/2013/inlineXBRL}"
XHTML = "{http://www.w3.org/1999/xhtml}"


def printed_ids(ticker: str, accession: str, row: str, printed: str) -> list[str]:
    """The ids the inline document itself gives the number printed as `printed` in the table
    row whose first cell begins `row`, read here with the standard library from the committed
    filing and with nothing of `src/`: every `ix:nonFraction` whose text is `printed`."""
    path = next(FIXTURES / ticker / entry["path"] for entry in json.loads(
        (FIXTURES / ticker / "manifest.json").read_text(encoding="utf-8"))["documents"]
                if entry["accession"] == accession and entry["role"] == "primary_html")
    raw = path.read_bytes() if path.exists() else gzip.open(f"{path}.gz").read()
    raw = gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw
    found = []
    for tr in ET.fromstring(raw).iter(f"{XHTML}tr"):
        text = " ".join("".join(tr.itertext()).replace("\u200b", " ").split())
        if not text.startswith(row):
            continue
        found += [f"{accession}:{one.get('id')}" for one in tr.iter(f"{IX}nonFraction")
                  if "".join(one.itertext()).strip() == printed]
    assert found, (row, printed)
    return found


def ids(accession: str, *numbers: str) -> list[str]:
    return [f"{accession}:{number}" for number in numbers]


# --- planted tables ----------------------------------------------------------------------

def fact(concept: str, value, *, at: str | None = None, start: str | None = None,
         end: str | None = None, axes: dict | None = None, number: str) -> dict:
    out = {"concept": concept if ":" in concept else f"us-gaap:{concept}", "value": float(value),
           "unit": "iso4217:USD"}
    if at:
        out["instant"] = at
    else:
        out["start"], out["end"] = start, end
    if axes:
        out["axes"] = axes
    out["fact"] = f"{ACCESSION}:{number}"
    return out


def planted(*tables: list[dict]) -> dict:
    """The shape `note_tables.tables` returns, with the facts planted."""
    return {"tables": {f"notes_{at}": {"paragraph": f"{ACCESSION}:notes:{at}", "facts": facts}
                       for at, facts in enumerate(tables, start=1)},
            "unmatched": [], "not_in_the_instance": [], "left_out_as_a_price": {},
            "left_out_ending_after_the_cutoff": {}}


YEAR = {"start": "2025-01-01", "end": "2025-12-31"}
OPENING, CLOSING = "2024-12-31", "2025-12-31"


def table_of(balance: str, charged: str | None, usage: str | None, *, opening, closing,
             charge=None, spent=None, other=None, other_concept=None) -> list[dict]:
    rows = [fact(balance, opening, at=OPENING, number="b1"),
            fact(balance, closing, at=CLOSING, number="b2")]
    if charged and charge is not None:
        rows.append(fact(charged, charge, **YEAR, number="c1"))
    if usage and spent is not None:
        rows.append(fact(usage, spent, **YEAR, number="u1"))
    if other_concept and other is not None:
        rows.append(fact(other_concept, other, **YEAR, number="o1"))
    return rows


# --- Generac's warranty rollforward ------------------------------------------------------

def test_generacs_warranty_figures_are_the_printed_ones(generac):
    series = series_of(generac, "product_warranty", "notes_169")
    year = period_of(series, "2025-12-31")
    assert year["beginning"]["value"] == 110_987_000
    assert year["usage"]["value"] == 86_448_000
    assert year["charged_to_expense"]["value"] == 100_589_000
    assert year["other"]["value"] == 6_794_000
    assert year["ending"]["value"] == 131_922_000


def test_generacs_warranty_foots_and_prints_its_fact_ids(generac):
    year = period_of(series_of(generac, "product_warranty", "notes_169"), "2025-12-31")
    # 110,987 + 100,589 + 6,794 - 86,448 = 131,922
    assert year["foots"] is True
    assert year["difference"]["value"] == 0
    assert year["expected_ending"]["value"] == 131_922_000
    # the ids are the ones the inline document gives the numbers as printed, read apart from src/
    row = "Balance at beginning of period"
    (beginning,) = year["beginning"]["facts"]
    assert beginning in printed_ids("GNRC", GNRC_ACCESSION, row, "110,987")
    (usage,) = year["usage"]["facts"]
    assert usage in printed_ids("GNRC", GNRC_ACCESSION, "Payments", "86,448")
    (charge,) = year["charged_to_expense"]["facts"]
    assert charge in printed_ids("GNRC", GNRC_ACCESSION, "Provision for warranty issued",
                                 "100,589")
    (revision,) = year["other"]["facts"]
    assert revision in printed_ids("GNRC", GNRC_ACCESSION,
                                   "Changes in estimates for pre-existing warranties", "6,794")
    (ending,) = year["ending"]["facts"]
    assert ending in printed_ids("GNRC", GNRC_ACCESSION, "Balance at end of period", "131,922")
    assert year["difference"]["facts"] == [beginning, charge, revision, usage, ending]
    assert year["complete"] is True and year["rows_not_placed"] == []


def test_generacs_earlier_years_foot_by_hand(generac):
    series = series_of(generac, "product_warranty", "notes_169")
    # 116,408 + 77,802 + 5,767 - 88,990 = 110,987
    last_year = period_of(series, "2024-12-31")
    assert last_year["beginning"]["value"] == 116_408_000
    assert last_year["ending"]["value"] == 110_987_000
    assert last_year["foots"] is True
    # 138,011 + 67,104 + 3,493 - 92,200 = 116,408
    assert period_of(series, "2023-12-31")["foots"] is True
    # the 2025 beginning is the 2024 ending: the one fact the filing states once
    assert (period_of(series, "2025-12-31")["beginning"]["facts"]
            == period_of(series, "2024-12-31")["ending"]["facts"])


def test_generacs_warranty_measures(generac):
    year = period_of(series_of(generac, "product_warranty", "notes_169"), "2025-12-31")
    assert year["provision_over_usage"]["value"] == pytest.approx(100_589 / 86_448)
    assert year["provision_over_usage"]["facts"] == ids(GNRC_ACCESSION, "c140005335",
                                                        "c140005332")
    # a year: 110,987 / 86,448
    assert year["coverage_years"]["value"] == pytest.approx(110_987 / 86_448)
    assert year["prior_period_revision_over_current_expense"]["value"] == pytest.approx(
        6_794 / 100_589)
    assert year["prior_period_revision_over_current_expense"]["facts"] == ids(
        GNRC_ACCESSION, "c140005338", "c140005335")
    assert year["release"] is False and year["release_because"] == []
    # Generac tags no gross base of a warranty reserve
    assert "missing" in year["ending_over_gross_base"]


def test_generacs_extended_warranty_table_is_not_the_standard_warranty_family(generac):
    """Its deferred revenue on extended warranties (note 170) is `ExtendedProductWarrantyAccrual`,
    which is no element of the table, so the family holds the one table."""
    assert [one["table"] for one in generac["product_warranty"]["series"]] == ["notes_169"]


def test_generacs_schedule_two_is_read_by_the_member_of_its_type_axis(generac):
    allowance = period_of(series_of(generac, "allowance_for_credit_losses", "notes_195"),
                          "2025-12-31")
    # 35,465 + 1,398 - 2,359 = 34,504 (the 2,359 is `ChargedToOtherAccounts`, signed)
    assert allowance["beginning"]["value"] == 35_465_000
    assert allowance["charged_to_expense"]["value"] == 1_398_000
    assert allowance["other"]["value"] == -2_359_000
    assert allowance["ending"]["value"] == 34_504_000
    assert allowance["foots"] is True
    inventory = period_of(series_of(generac, "inventory_reserve", "notes_195"), "2025-12-31")
    # 48,173 + 23,375 - 2,282 = 69,266
    assert (inventory["beginning"]["value"], inventory["ending"]["value"]) == (
        48_173_000, 69_266_000)
    assert inventory["foots"] is True
    # the valuation allowance of deferred tax assets is no reserve family of this section
    assert all("tax" not in json.dumps(one).lower() for one in
               generac["inventory_reserve"]["series"])


def test_a_net_change_row_is_no_role_and_a_table_with_one_is_not_complete(generac):
    """`ValuationAllowancesAndReservesPeriodIncreaseDecrease` is a net change, like its two
    excluded siblings, and lands in `rows_not_placed`: Generac's allowance reads, in dollars,

      2025: 35,465,000 + 1,398,000 - 2,359,000 = 34,504,000, the net change row 0
      2024: 33,925,000 + 4,524,000 - 3,509,000 = 34,940,000 against 35,465,000, row 525,000
      2023: 27,664,000 + 7,443,000 - 1,206,000 = 33,901,000 against 33,925,000, row 24,000

    so 2024 and 2023 do not foot and are marked not complete, the row named."""
    assert "ValuationAllowancesAndReservesPeriodIncreaseDecrease" not in rollforwards.CONFIRMED_IN
    series = series_of(generac, "allowance_for_credit_losses", "notes_195")
    for end, gap, row in (("2025-12-31", 0, 0), ("2024-12-31", 525_000, 525_000),
                          ("2023-12-31", 24_000, 24_000)):
        year = period_of(series, end)
        assert year["difference"]["value"] == gap
        assert year["foots"] is (gap == 0)
        assert year["complete"] is False
        # one row, that year's: a zero row counts, and another year's row does not
        assert [(one["concept"], one["value"]) for one in year["rows_not_placed"]] == [
            ("us-gaap:ValuationAllowancesAndReservesPeriodIncreaseDecrease", row)]


def test_generacs_goodwill_is_one_series_per_column_and_never_summed(generac):
    """Note 153, in thousands, the 2025 rows as the filing prints them:

        Balance as of December 31, 2024    1,041,147 (Domestic)  395,114 (International)  1,436,261 (Total)
        Purchase accounting adjustments       (6,182)                310                    (5,872)
        Foreign currency translation           112                36,593                    36,705
        Balance as of December 31, 2025    1,035,077             432,017                  1,467,094

    1,041,147 - 6,182 + 112 = 1,035,077; 395,114 + 310 + 36,593 = 432,017; and the filer's
    own Total column 1,436,261 - 5,872 + 36,705 = 1,467,094, a series of its own: Python
    sums no column into another."""
    series = {one["axes"].get("us-gaap:StatementBusinessSegmentsAxis"): one
              for one in generac["goodwill"]["series"] if one["table"] == "notes_153"}
    assert set(series) == {"gnrc:DomesticMember", "gnrc:InternationalMember", None}
    wanted = {"gnrc:DomesticMember": (1_041_147, -6_182 + 112, 1_035_077),
              "gnrc:InternationalMember": (395_114, 310 + 36_593, 432_017),
              None: (1_436_261, -5_872 + 36_705, 1_467_094)}
    for member, (opening, other, closing) in wanted.items():
        year = period_of(series[member], "2025-12-31")
        assert year["beginning"]["value"] == opening * 1000
        assert year["other"]["value"] == other * 1000
        assert year["ending"]["value"] == closing * 1000
        assert year["foots"] is True
        # a sibling's row on another member of the axis is no row of this one
        assert year["complete"] is True and year["rows_not_placed"] == []
    assert period_of(series[None], "2025-12-31")["ending"]["facts"][0] in printed_ids(
        "GNRC", GNRC_ACCESSION, "Balance as of December 31, 2025", "1,467,094")


# --- Ciena's allowance and inventory reserve --------------------------------------------

def test_cienas_allowance_foots_in_each_year(ciena):
    series = series_of(ciena, "allowance_for_credit_losses", "notes_40")
    # 9,880 + 4,226 - 2,894 = 11,212, the instance's f-1037, f-1039, f-1040 and f-1041
    year = period_of(series, "2025-11-01")
    assert year["beginning"]["value"] == 9_880_000
    assert year["charged_to_expense"]["value"] == 4_226_000
    assert year["usage"]["value"] == 2_894_000
    assert year["ending"]["value"] == 11_212_000
    assert year["foots"] is True
    # the ids the inline document gives the printed numbers, read apart from src/
    row = "November 1, 2025"
    # the 9,880 is printed twice (the 2024 ending, f-1037, and the 2025 beginning, f-1038), the
    # same fact of the same context tagged twice, and the section keeps the first
    assert year["beginning"]["facts"][0] in (
        printed_ids("CIEN", CIEN_ACCESSION, row, "9,880")
        + printed_ids("CIEN", CIEN_ACCESSION, "November 2, 2024", "9,880"))
    assert year["charged_to_expense"]["facts"][0] in printed_ids("CIEN", CIEN_ACCESSION, row,
                                                                 "4,226")
    assert year["usage"]["facts"][0] in printed_ids("CIEN", CIEN_ACCESSION, row, "2,894")
    assert year["ending"]["facts"][0] in printed_ids("CIEN", CIEN_ACCESSION, row, "11,212")
    # 11,654 + 7,996 - 9,770 = 9,880, and 10,958 + 5,718 - 5,022 = 11,654
    assert period_of(series, "2024-11-02")["foots"] is True
    assert period_of(series, "2023-10-28")["foots"] is True
    assert year["provision_over_usage"]["value"] == pytest.approx(4_226 / 2_894)
    assert year["coverage_years"]["value"] == pytest.approx(9_880 / 2_894)


def test_a_table_whose_own_row_is_in_the_filers_namespace_is_marked_not_complete(ciena):
    year = period_of(series_of(ciena, "inventory_reserve", "notes_42"), "2025-11-01")
    # 107,173 + 48,424 = 155,597 against 129,408
    assert year["expected_ending"]["value"] == 155_597_000
    assert year["difference"]["value"] == -26_189_000
    assert year["foots"] is False
    assert year["complete"] is False
    assert [row["concept"] for row in year["rows_not_placed"]] == [
        "cien:InventoryValuationReservesDisposals"]
    assert year["rows_not_placed"][0]["value"] == 26_189_000


# --- the ASU's supplier-finance table, planted -------------------------------------------

def test_the_asus_supplier_finance_table_foots():
    result = rollforwards.build(planted([
        fact("SupplierFinanceProgramObligation", 733, at=OPENING, number="s1"),
        fact("SupplierFinanceProgramObligationIncrease", 2_435, **YEAR, number="s2"),
        fact("SupplierFinanceProgramObligationDecreaseSettlement", 2_315, **YEAR, number="s3"),
        fact("SupplierFinanceProgramObligation", 853, at=CLOSING, number="s4"),
    ]))
    year = period_of(series_of(result, "supplier_finance_obligations", "notes_1"), CLOSING)
    # 733 + 2,435 - 2,315 = 853
    assert year["foots"] is True and year["difference"]["value"] == 0
    assert year["expected_ending"]["value"] == 853
    assert year["provision_over_usage"]["value"] == pytest.approx(2_435 / 2_315)
    assert year["coverage_years"]["value"] == pytest.approx(733 / 2_315)
    assert year["release"] is False
    assert year["ending"]["facts"] == [f"{ACCESSION}:s4"]


# --- a table that does not foot ----------------------------------------------------------

def test_a_table_that_does_not_foot_says_so_with_the_difference():
    result = rollforwards.build(planted(table_of(
        "ProductWarrantyAccrual", "ProductWarrantyAccrualWarrantiesIssued",
        "ProductWarrantyAccrualPayments", opening=1_000, closing=1_100, charge=400, spent=300,
        other=-20, other_concept="StandardProductWarrantyAccrualForeignCurrencyTranslationGainLoss")))
    year = period_of(series_of(result, "product_warranty", "notes_1"), CLOSING)
    # 1,000 + 400 - 20 - 300 = 1,080 against a stated 1,100
    assert year["expected_ending"]["value"] == 1_080
    assert year["foots"] is False
    assert year["difference"]["value"] == 20
    assert year["complete"] is True


def test_the_sign_of_usage_is_as_the_filer_tagged_it():
    """Usage is tagged positive and taken away: 1,000 + 400 - 300 = 1,100 foots, and the
    same table with usage tagged -300 does not (1,000 + 400 + 300 = 1,700)."""
    right = rollforwards.build(planted(table_of(
        "ProductWarrantyAccrual", "ProductWarrantyAccrualWarrantiesIssued",
        "ProductWarrantyAccrualPayments", opening=1_000, closing=1_100, charge=400, spent=300)))
    assert period_of(series_of(right, "product_warranty", "notes_1"), CLOSING)["foots"] is True
    flipped = rollforwards.build(planted(table_of(
        "ProductWarrantyAccrual", "ProductWarrantyAccrualWarrantiesIssued",
        "ProductWarrantyAccrualPayments", opening=1_000, closing=1_100, charge=400, spent=-300)))
    year = period_of(series_of(flipped, "product_warranty", "notes_1"), CLOSING)
    assert year["foots"] is False and year["difference"]["value"] == -600


def test_revenue_recognized_out_of_contract_liabilities_is_read_as_a_magnitude():
    """Filers tag it positive (19 of the committed facts) and negative (9): either way the
    revenue recognized leaves the balance, 900 - 400 + 500 = 1,000."""
    for sign in (400, -400):
        result = rollforwards.build(planted([
            fact("ContractWithCustomerLiability", 900, at=OPENING, number="l1"),
            fact("ContractWithCustomerLiabilityRevenueRecognized", sign, **YEAR, number="l2"),
            fact("ContractWithCustomerLiabilityIncreaseDecreaseForContractAcquiredInBusiness"
                 "Combination", 500, **YEAR, number="l3"),
            fact("ContractWithCustomerLiability", 1_000, at=CLOSING, number="l4")]))
        year = period_of(series_of(result, "contract_liabilities", "notes_1"), CLOSING)
        assert year["foots"] is True
        assert year["usage"]["value"] == 400


# --- the release flag --------------------------------------------------------------------

def test_a_negative_charge_is_a_release():
    result = rollforwards.build(planted(table_of(
        "AllowanceForDoubtfulAccountsReceivableCurrent", "ProvisionForDoubtfulAccounts",
        "AllowanceForDoubtfulAccountsReceivableWriteOffs", opening=500, closing=420,
        charge=-50, spent=30)))
    year = period_of(series_of(result, "allowance_for_credit_losses", "notes_1"), CLOSING)
    # 500 - 50 - 30 = 420
    assert year["foots"] is True
    assert year["release"] is True
    assert year["release_because"] == ["charged_to_expense_negative"]


def test_a_positive_charge_with_the_reserve_rising_is_no_release():
    result = rollforwards.build(planted(table_of(
        "AllowanceForDoubtfulAccountsReceivableCurrent", "ProvisionForDoubtfulAccounts",
        "AllowanceForDoubtfulAccountsReceivableWriteOffs", opening=500, closing=520,
        charge=50, spent=30)))
    year = period_of(series_of(result, "allowance_for_credit_losses", "notes_1"), CLOSING)
    assert year["release"] is False and year["release_because"] == []


INVENTORY_TYPE = {"us-gaap:ValuationAllowancesAndReservesTypeAxis":
                  "us-gaap:InventoryValuationReserveMember"}


def inventory_reserve(closing: int, base: tuple[int, int] | None) -> dict:
    """Schedule II's inventory valuation reserve, 200 + 10 - 60 = 150 when `closing` is 150,
    beside a gross inventory in another table of the filing when `base` is given."""
    schedule = [
        fact("ValuationAllowancesAndReservesBalance", 200, at=OPENING, axes=INVENTORY_TYPE,
             number="b1"),
        fact("ValuationAllowancesAndReservesChargedToCostAndExpense", 10, **YEAR,
             axes=INVENTORY_TYPE, number="c1"),
        fact("ValuationAllowancesAndReservesDeductions", 60, **YEAR, axes=INVENTORY_TYPE,
             number="u1"),
        fact("ValuationAllowancesAndReservesBalance", closing, at=CLOSING, axes=INVENTORY_TYPE,
             number="b2")]
    if base is None:
        return rollforwards.build(planted(schedule))
    return rollforwards.build(planted(schedule, [
        fact("InventoryGross", base[0], at=OPENING, number="g1"),
        fact("InventoryGross", base[1], at=CLOSING, number="g2")]))


def test_a_reserve_that_fell_while_its_gross_base_rose_is_a_release():
    year = period_of(series_of(inventory_reserve(150, (1_000, 1_200)), "inventory_reserve",
                               "notes_1"), CLOSING)
    assert year["foots"] is True                                 # 200 + 10 - 60 = 150
    assert year["release"] is True
    assert year["release_because"] == ["reserve_fell_while_gross_base_rose"]
    # 150 / 1,200, from two tables and neither summed with the other
    assert year["ending_over_gross_base"]["value"] == pytest.approx(150 / 1_200)
    assert year["ending_over_gross_base"]["facts"] == [f"{ACCESSION}:b2", f"{ACCESSION}:g2"]


def test_a_gross_base_on_other_axes_is_no_base_of_this_series():
    """A gross inventory the filing states for one segment is not the base of the reserve
    of the whole company: the base is read on the series' own axes."""
    segment = {"us-gaap:StatementBusinessSegmentsAxis": "x:NorthMember"}
    result = rollforwards.build(planted(
        [fact("ValuationAllowancesAndReservesBalance", 200, at=OPENING, axes=INVENTORY_TYPE,
              number="b1"),
         fact("ValuationAllowancesAndReservesChargedToCostAndExpense", 10, **YEAR,
              axes=INVENTORY_TYPE, number="c1"),
         fact("ValuationAllowancesAndReservesDeductions", 60, **YEAR, axes=INVENTORY_TYPE,
              number="u1"),
         fact("ValuationAllowancesAndReservesBalance", 150, at=CLOSING, axes=INVENTORY_TYPE,
              number="b2")],
        [fact("InventoryGross", 1_000, at=OPENING, axes=segment, number="g1"),
         fact("InventoryGross", 1_200, at=CLOSING, axes=segment, number="g2")]))
    year = period_of(series_of(result, "inventory_reserve", "notes_1"), CLOSING)
    assert "missing" in year["ending_over_gross_base"]
    assert year["release"] is False


def test_two_different_gross_bases_at_one_date_are_no_base():
    result = rollforwards.build(planted(
        [fact("ValuationAllowancesAndReservesBalance", 200, at=OPENING, axes=INVENTORY_TYPE,
              number="b1"),
         fact("ValuationAllowancesAndReservesChargedToCostAndExpense", 10, **YEAR,
              axes=INVENTORY_TYPE, number="c1"),
         fact("ValuationAllowancesAndReservesBalance", 210, at=CLOSING, axes=INVENTORY_TYPE,
              number="b2")],
        [fact("InventoryGross", 1_000, at=CLOSING, number="g1")],
        [fact("InventoryGross", 1_100, at=CLOSING, number="g2")]))
    year = period_of(series_of(result, "inventory_reserve", "notes_1"), CLOSING)
    assert "more than one gross base" in year["ending_over_gross_base"]["missing"]


def test_a_reserve_that_fell_with_its_base_is_no_release():
    year = period_of(series_of(inventory_reserve(150, (1_000, 900)), "inventory_reserve",
                               "notes_1"), CLOSING)
    assert year["release"] is False


def test_a_reserve_that_rose_with_its_base_is_no_release():
    # 200 + 10 - 60 + 110 of translation is not tagged, so the reserve is 150 or more here
    year = period_of(series_of(inventory_reserve(260, (1_000, 1_200)),
                               "inventory_reserve", "notes_1"), CLOSING)
    assert year["release"] is False


def test_a_fall_with_no_base_tagged_is_not_called_a_release():
    year = period_of(series_of(inventory_reserve(150, None), "inventory_reserve", "notes_1"),
                     CLOSING)
    assert year["release"] is False
    assert "missing" in year["ending_over_gross_base"]


# --- one table, never two ----------------------------------------------------------------

def test_nothing_is_summed_across_two_tables():
    """The beginning balance is in one table and the flows and the ending in another: 1,000
    + 400 - 300 = 1,100 would foot if the two were joined, and neither table holds a whole
    rollforward, so neither makes a period."""
    result = rollforwards.build(planted(
        [fact("ProductWarrantyAccrual", 1_000, at=OPENING, number="a1")],
        [fact("ProductWarrantyAccrualWarrantiesIssued", 400, **YEAR, number="a2"),
         fact("ProductWarrantyAccrualPayments", 300, **YEAR, number="a3"),
         fact("ProductWarrantyAccrual", 1_100, at=CLOSING, number="a4")]))
    for one in result["product_warranty"].get("series", []):
        for year in one["periods"]:
            assert "foots" not in year
            assert "missing" in year


def test_a_series_on_one_axis_member_is_never_joined_to_another_member():
    """Two segments' goodwill in one table: each foots on its own, 100 + 20 - 5 = 115 and 50
    + 10 - 0 = 60, and a mix of the two (100 + 10 - 5) is no period."""
    north, south = {"us-gaap:StatementBusinessSegmentsAxis": "x:NorthMember"}, {
        "us-gaap:StatementBusinessSegmentsAxis": "x:SouthMember"}
    result = rollforwards.build(planted([
        fact("Goodwill", 100, at=OPENING, axes=north, number="n1"),
        fact("GoodwillAcquiredDuringPeriod", 20, **YEAR, axes=north, number="n2"),
        fact("GoodwillImpairmentLoss", 5, **YEAR, axes=north, number="n3"),
        fact("Goodwill", 115, at=CLOSING, axes=north, number="n4"),
        fact("Goodwill", 50, at=OPENING, axes=south, number="s1"),
        fact("GoodwillAcquiredDuringPeriod", 10, **YEAR, axes=south, number="s2"),
        fact("Goodwill", 60, at=CLOSING, axes=south, number="s4")]))
    series = result["goodwill"]["series"]
    assert len(series) == 2
    assert all(one["periods"][0]["foots"] for one in series)
    assert {one["axes"]["us-gaap:StatementBusinessSegmentsAxis"] for one in series} == {
        "x:NorthMember", "x:SouthMember"}


# --- what is missing ---------------------------------------------------------------------

def test_a_family_the_filing_does_not_table_is_missing_with_the_reason():
    result = rollforwards.build(planted(table_of(
        "ProductWarrantyAccrual", "ProductWarrantyAccrualWarrantiesIssued",
        "ProductWarrantyAccrualPayments", opening=1_000, closing=1_100, charge=400, spent=300)))
    for family in rollforwards.FAMILIES:
        if family != "product_warranty":
            assert "series" not in result[family]
            assert "no table of the filing's notes" in result[family]["missing"]
            assert family.replace("_", " ") in result[family]["missing"]


def test_note_tables_that_were_not_read_make_every_family_missing_with_that_reason():
    result = rollforwards.build({"missing": "no run bundle or accession was given"})
    for family in rollforwards.FAMILIES:
        assert result[family] == {"missing": "no run bundle or accession was given"}


def test_a_balance_sheet_line_with_no_flows_is_no_rollforward():
    result = rollforwards.build(planted([
        fact("ProductWarrantyAccrual", 1_000, at=OPENING, number="a1"),
        fact("ProductWarrantyAccrual", 1_100, at=CLOSING, number="a2")]))
    assert "missing" in result["product_warranty"]


def test_a_period_with_no_beginning_balance_is_missing_not_guessed():
    result = rollforwards.build(planted([
        fact("ProductWarrantyAccrualWarrantiesIssued", 400, **YEAR, number="a2"),
        fact("ProductWarrantyAccrualPayments", 300, **YEAR, number="a3"),
        fact("ProductWarrantyAccrual", 1_100, at=CLOSING, number="a4")]))
    year = period_of(series_of(result, "product_warranty", "notes_1"), CLOSING)
    assert "beginning" in year["missing"] and "foots" not in year


def test_a_coverage_year_is_read_only_off_a_period_of_a_year():
    quarter = {"start": "2025-10-01", "end": "2025-12-31"}
    result = rollforwards.build(planted([
        fact("ProductWarrantyAccrual", 1_000, at="2025-09-30", number="a1"),
        fact("ProductWarrantyAccrualWarrantiesIssued", 400, **quarter, number="a2"),
        fact("ProductWarrantyAccrualPayments", 300, **quarter, number="a3"),
        fact("ProductWarrantyAccrual", 1_100, at=CLOSING, number="a4")]))
    period = period_of(series_of(result, "product_warranty", "notes_1"), CLOSING)
    assert period["foots"] is True
    assert "missing" in period["coverage_years"]
    assert period["provision_over_usage"]["value"] == pytest.approx(400 / 300)


def test_a_zero_usage_has_no_ratio():
    result = rollforwards.build(planted(table_of(
        "ProductWarrantyAccrual", "ProductWarrantyAccrualWarrantiesIssued",
        "ProductWarrantyAccrualPayments", opening=1_000, closing=1_400, charge=400, spent=0)))
    year = period_of(series_of(result, "product_warranty", "notes_1"), CLOSING)
    assert "missing" in year["provision_over_usage"] and "missing" in year["coverage_years"]


# --- arithmetic in Decimal ---------------------------------------------------------------

def test_the_identity_is_worked_in_decimal_so_a_cent_is_not_lost_to_a_float():
    """0.1 + 0.2 - 0.3 is 5.55e-17 in floats and zero in Decimal."""
    result = rollforwards.build(planted([
        fact("ProductWarrantyAccrual", 0.1, at=OPENING, number="d1"),
        fact("ProductWarrantyAccrualWarrantiesIssued", 0.2, **YEAR, number="d2"),
        fact("ProductWarrantyAccrualPayments", 0.0, **YEAR, number="d3"),
        fact("ProductWarrantyAccrual", 0.3, at=CLOSING, number="d4")]))
    year = period_of(series_of(result, "product_warranty", "notes_1"), CLOSING)
    assert year["foots"] is True and year["difference"]["value"] == 0
    assert Decimal("0.1") + Decimal("0.2") - Decimal("0.3") == 0


# --- the element table -------------------------------------------------------------------

def instance_text(ticker: str) -> bytes:
    import gzip
    blob = b""
    for path in sorted((FIXTURES / ticker).rglob("*")):
        name = path.name
        if not path.is_file() or not re.search(r"\.(htm|xml)(\.gz)?$", name):
            continue
        blob += gzip.open(path).read() if name.endswith(".gz") else path.read_bytes()
    return blob


def test_every_element_of_the_table_is_confirmed_in_a_committed_instance():
    """Each element is named with the ticker whose committed instances use it, and the
    instances of that ticker do: `name="us-gaap:Element"` of an inline fact or the
    `<us-gaap:Element` of an instance. An element nobody confirmed is left out."""
    named = {name for family in rollforwards.ELEMENTS.values() for names in family.values()
             for name in names}
    named |= {name for names in rollforwards.SCHEDULE_TWO.values() for name in names}
    assert named == set(rollforwards.CONFIRMED_IN), named ^ set(rollforwards.CONFIRMED_IN)
    blobs: dict[str, bytes] = {}
    for element, ticker in sorted(rollforwards.CONFIRMED_IN.items()):
        blobs.setdefault(ticker, instance_text(ticker))
        blob = blobs[ticker]
        assert (f'name="us-gaap:{element}"'.encode() in blob
                or f"<us-gaap:{element} ".encode() in blob
                or f"<us-gaap:{element}>".encode() in blob), (element, ticker)


def test_an_element_in_no_role_twice():
    seen: dict[str, str] = {}
    for family, roles in rollforwards.ELEMENTS.items():
        for role, names in roles.items():
            for name in names:
                if role == "base":
                    continue
                assert (name not in seen), (name, family, seen.get(name))
                seen[name] = family
    for role, names in rollforwards.SCHEDULE_TWO.items():
        for name in names:
            assert name not in seen, name
            seen[name] = "schedule_two"


def test_the_families_are_the_seven_the_task_names_and_schedule_twos_other_accounts():
    assert set(rollforwards.FAMILIES) == {
        "allowance_for_credit_losses", "product_warranty", "inventory_reserve",
        "restructuring_reserve", "contract_liabilities", "supplier_finance_obligations",
        "goodwill", "schedule_two_other"}


# --- the calculator carries it -----------------------------------------------------------

def test_the_calculator_carries_the_section_and_it_reaches_the_filings_only_view():
    payload = calculator.calculate(ticker="GNRC", cutoff="2026-02-18", period_end="2025-12-31",
                                   form="10-K")
    assert set(payload["rollforwards"]) >= set(rollforwards.FAMILIES)
    # no run bundle was given, so no table was read, and each family says so
    assert "missing" in payload["rollforwards"]["product_warranty"]
    assert "rollforwards" in calculator.filings_only(payload)


GNRC_TEN_Q = Path(__file__).resolve().parent.parent / "runs" / "GNRC" / "0001437749-26-025669"


def test_the_calculator_reads_a_runs_note_tables_into_the_section():
    """Generac's 10-Q filed 2026-08-04 (a committed run's bundle), note 108 read by eye, in
    thousands, three months to June 30, 2026: beginning 128,354, payments (20,454), provision
    20,286, changes in estimates 2,582, reserve assumed in acquisition 82, ending 130,850.
    128,354 + 20,286 + 2,582 + 82 - 20,454 = 130,850."""
    payload = calculator.calculate(
        ticker="GNRC", cutoff="2026-08-04", period_end="2026-06-30", form="10-Q",
        accession="0001437749-26-025669", bundle=GNRC_TEN_Q)
    series = series_of(payload["rollforwards"], "product_warranty", "notes_108")
    quarter = period_of(series, "2026-06-30")
    assert (quarter["beginning"]["value"], quarter["ending"]["value"]) == (128_354_000,
                                                                          130_850_000)
    assert quarter["other"]["value"] == (2_582 + 82) * 1000
    assert quarter["foots"] is True
    # a quarter, so no coverage in years
    assert "missing" in quarter["coverage_years"]
    view = calculator.filings_only(payload)
    assert view["rollforwards"]["product_warranty"] == payload["rollforwards"]["product_warranty"]


# --- a translation row contributes the sign the filing prints ----------------------------

def one_period(ticker: str, accession: str, cutoff: str, family: str, table: str,
               end: str, *, axes: dict | None = None) -> dict:
    result = rollforwards.build(tables_of(ticker, accession, cutoff))
    series = next(one for one in result[family]["series"]
                  if one["table"] == table and one["axes"] == (axes or {}))
    return period_of(series, end)


def translation_row(year: dict) -> dict:
    (row,) = [one for one in year["other"]["rows"] if "Translation" in one["concept"]]
    return row


def test_ciscos_printed_3_tagged_minus_3_adds_3():
    """Cisco's 10-K filed 2025-09-03, total column, in millions: Foreign exchange and other
    printed 3 (the instance tags -3, `sign="-"`), 65 - 9 (provisions) - 9 (recoveries
    (write-offs), net) + 3 = 50."""
    year = one_period("CSCO", "0000858877-25-000111", "2025-09-03",
                      "allowance_for_credit_losses", "notes_97", "2025-07-26")
    row = translation_row(year)
    assert (row["value"], row["contribution"]) == (-3_000_000, 3_000_000)
    assert row["sign_source"] == "printed" and row["sign_disagrees"] is True
    assert year["other"]["sign_source"] == "printed"
    assert year["other"]["value"] == 3_000_000
    assert (year["beginning"]["value"], year["ending"]["value"]) == (65_000_000, 50_000_000)
    assert year["foots"] is True and year["difference"]["value"] == 0


def test_johnson_controls_printed_1_in_parentheses_tagged_plus_1_takes_1_away():
    """Johnson Controls' 10-Q filed 2026-07-29: Currency translation printed (1), tagged +1;
    120 + 94 + 3 - 1 - 70 = 146."""
    year = one_period("JCI", "0000833444-26-000087", "2026-07-29", "product_warranty",
                      "notes_35", "2026-06-30")
    row = translation_row(year)
    assert (row["value"], row["contribution"]) == (1_000_000, -1_000_000)
    assert row["sign_source"] == "printed" and row["sign_disagrees"] is True
    assert year["other"]["value"] == (3 - 1) * 1_000_000
    assert (year["beginning"]["value"], year["ending"]["value"]) == (120_000_000, 146_000_000)
    assert year["foots"] is True


def test_logitechs_printed_94_tagged_minus_94_adds_94():
    """Logitech's 10-Q filed 2026-07-29, in thousands: Effects of foreign currency
    translation printed 94 (tagged -94); 50,242 + 8,496 + 94 - 9,553 = 49,279."""
    year = one_period("LOGI", "0001032975-26-000050", "2026-07-29", "product_warranty",
                      "notes_17", "2026-06-30")
    row = translation_row(year)
    assert (row["value"], row["contribution"]) == (-94_000, 94_000)
    assert row["sign_source"] == "printed" and row["sign_disagrees"] is True
    assert (year["beginning"]["value"], year["ending"]["value"]) == (50_242_000, 49_279_000)
    assert year["foots"] is True


def test_lennoxs_printed_and_tagged_signs_agree():
    """Lennox's 10-K filed 2026-02-17, in millions: Changes in foreign currency translation
    rates and other printed (0.8) and tagged -0.8; 142.8 - 41.2 + 59.0 - 1.4 - 0.8 = 158.4."""
    year = one_period("LII", "0001069202-26-000028", "2026-02-17", "product_warranty",
                      "notes_50", "2024-12-31")
    row = translation_row(year)
    assert row["value"] == pytest.approx(-0.8e6) and row["contribution"] == pytest.approx(-0.8e6)
    assert row["sign_source"] == "printed" and row["sign_disagrees"] is False
    assert year["beginning"]["value"] == pytest.approx(142.8e6)
    assert year["ending"]["value"] == pytest.approx(158.4e6)
    assert year["foots"] is True


def with_signs(tables: dict, signs: dict) -> dict:
    tables["printed_signs"] = {f"{ACCESSION}:{key}": value for key, value in signs.items()}
    return tables


TRANSLATION = "StandardProductWarrantyAccrualForeignCurrencyTranslationGainLoss"


def test_a_translation_row_with_no_printed_sign_keeps_its_tagged_value_and_says_so():
    """The refuter's planted table: 1,000 + 400 - 300 + 20 = 1,120 against a stated 1,080, the
    20 a translation row tagged +20 with nothing printed to read. The table is not made to
    foot by reversing the row: stated ending less the rows is 1,080 - 1,120 = -40."""
    result = rollforwards.build(planted(table_of(
        "ProductWarrantyAccrual", "ProductWarrantyAccrualWarrantiesIssued",
        "ProductWarrantyAccrualPayments", opening=1_000, closing=1_080, charge=400, spent=300,
        other=20, other_concept=TRANSLATION)))
    year = period_of(series_of(result, "product_warranty", "notes_1"), CLOSING)
    assert year["foots"] is False and year["difference"]["value"] == -40
    assert year["other"]["sign_source"] == "tagged"
    assert year["other"]["rows"][0]["sign_source"] == "tagged"
    assert "sign_disagrees" not in year["other"]["rows"][0]


def test_a_printed_sign_decides_the_contribution_whatever_the_tag_and_the_footing():
    """Tagged +20 and printed (20): 1,000 + 400 - 20 - 300 = 1,080 foots. Tagged +20 and
    printed 20 against a stated 1,080 reads 1,120 and does not foot, though reversing the
    row would have made it."""
    rows = table_of("ProductWarrantyAccrual", "ProductWarrantyAccrualWarrantiesIssued",
                    "ProductWarrantyAccrualPayments", opening=1_000, closing=1_080,
                    charge=400, spent=300, other=20, other_concept=TRANSLATION)
    negative = with_signs(planted(rows), {"o1": "negative"})
    year = period_of(series_of(rollforwards.build(negative), "product_warranty", "notes_1"),
                     CLOSING)
    assert year["foots"] is True and year["other"]["value"] == -20
    assert year["other"]["sign_source"] == "printed" and year["other"]["sign_disagrees"]
    positive = with_signs(planted(rows), {"o1": "positive"})
    year = period_of(series_of(rollforwards.build(positive), "product_warranty", "notes_1"),
                     CLOSING)
    assert year["foots"] is False and year["difference"]["value"] == -40
    assert year["other"]["sign_source"] == "printed" and not year["other"]["sign_disagrees"]


def test_the_printed_sign_is_read_from_the_inline_document():
    """`note_tables.printed_signs` on a planted row: (1,647 | ) is negative, 1,647 positive, a
    dollar sign before the parenthesis changes nothing."""
    cells = ('<tr><td>A</td><td>(</td><td><ix:nonFraction id="a" name="x:Y" contextRef="c" '
             'unitRef="usd">1,647</ix:nonFraction></td><td>)</td></tr>'
             '<tr><td>B</td><td><ix:nonFraction id="b" name="x:Y" contextRef="c" unitRef="usd" '
             'sign="-">1</ix:nonFraction></td></tr>'
             '<tr><td>C</td><td>$ (<ix:nonFraction id="c" name="x:Y" contextRef="c" '
             'unitRef="usd">2</ix:nonFraction></td><td>)</td></tr>')
    html = ('<html xmlns="http://www.w3.org/1999/xhtml" '
            'xmlns:ix="http://www.xbrl.org/2013/inlineXBRL"><body><table>' + cells
            + "</table></body></html>").encode()
    assert note_tables.printed_signs(html) == {"a": "negative", "b": "positive", "c": "negative"}


# --- a row no role holds makes a table not complete --------------------------------------

def test_ciscos_acquisition_rows_make_its_goodwill_note_not_complete():
    """Cisco's 10-K filed 2025-09-03, note 71, in millions, Americas: 24,035 + 11,619 (Splunk)
    + 573 (other acquisitions) - 58 = 36,169. The Splunk and other-acquisition rows are on
    `BusinessAcquisitionAxis`, a member beside the segment, and are not summed into the
    segment's role: 24,035 - 58 = 23,977 against 36,169 is 12,192 short."""
    year = one_period("CSCO", "0000858877-25-000111", "2025-09-03", "goodwill", "notes_71",
                      "2024-07-27", axes={"us-gaap:StatementBusinessSegmentsAxis":
                                          "csco:AmericasSegmentMember"})
    assert year["foots"] is False and year["difference"]["value"] == 12_192_000_000
    assert year["complete"] is False
    assert sorted(row["value"] for row in year["rows_not_placed"]) == [573e6, 11_619e6]


def test_carriers_held_for_sale_row_makes_its_warranty_note_not_complete():
    """Carrier's 10-K filed 2026-02-05, note 56, 2025, in millions: 786 + 364 + 32 - 282 - 7
    (reclassified to held for sale) = 893; the 7 is `carr:StandardAndExtendedProduct
    DecreaseDueToDivestiture`, so the rows Python places make 900 and the table reads 7 under."""
    year = one_period("CARR", "0001783180-26-000008", "2026-02-05", "product_warranty",
                      "notes_56", "2025-12-31")
    assert year["foots"] is False and year["difference"]["value"] == -7_000_000
    assert year["complete"] is False
    assert [row["concept"] for row in year["rows_not_placed"]] == [
        "carr:StandardAndExtendedProductDecreaseDueToDivestiture"]


def test_dells_other_row_makes_its_allowance_note_not_complete():
    """Dell's 10-K filed 2026-03-16, note 40, fiscal 2024 (year to February 2, 2024), in
    millions: 201 - 49 (charge-offs, net of recoveries) + 92 + (74) = 170; the (74) is
    `dell:FinancingReceivableOtherExpenseReversal`."""
    year = one_period("DELL", "0001571996-26-000008", "2026-03-16", "allowance_for_credit_losses",
                      "notes_40", "2024-02-02", axes={
                          "us-gaap:AccountsNotesLoansAndFinancingReceivableByReceivableTypeAxis":
                          "us-gaap:LoansAndFinanceReceivablesMember"})
    assert year["foots"] is False and year["difference"]["value"] == -74_000_000
    assert year["complete"] is False
    assert [(row["concept"], row["value"]) for row in year["rows_not_placed"]] == [
        ("dell:FinancingReceivableOtherExpenseReversal", -74_000_000)]


def test_ttms_exchange_rate_row_makes_its_supplier_finance_note_not_complete():
    """TTM's 10-K filed 2026-02-17, note 56, 2025, in thousands: 17,218 + 12,579 - 17,480 +
    218 = 12,535; the 218 is `ttmi:EffectOfForeignCurrencyExchangeRates`."""
    year = one_period("TTMI", "0001193125-26-051976", "2026-02-17",
                      "supplier_finance_obligations", "notes_56", "2025-12-29")
    assert year["foots"] is False and year["difference"]["value"] == 218_000
    assert year["complete"] is False
    assert [row["concept"] for row in year["rows_not_placed"]] == [
        "ttmi:EffectOfForeignCurrencyExchangeRates"]


def all_filings():
    """Every committed filing with an inline document and an instance (72), as a pair of its
    ticker and accession and the cutoff of its own filing date."""
    for manifest in sorted(FIXTURES.glob("*/manifest.json")):
        documents = json.loads(manifest.read_text(encoding="utf-8"))["documents"]
        roles: dict[str, dict] = {}
        for entry in documents:
            roles.setdefault(entry["accession"], {})[entry["role"]] = entry
        for accession, found in sorted(roles.items()):
            if {"primary_html", "xbrl_instance"} <= set(found):
                yield manifest.parent.name, accession, found["primary_html"]["filing_date"]


def recomputed_difference(year: dict) -> Decimal | None:
    """The stated ending less the sum of the placed rows, from the period's own rows and
    nothing else: the beginning, the charge, each row of `other` at its contribution (its
    tagged value where it has none), each usage row taken away as tagged (revenue recognized out
    of contract liabilities, the one element read as a magnitude, by its size). Charge rows of
    different elements are one charge: their values are equal and printed in one cell, so the
    charge is counted once. None where the period carries overlapping charge elements, which the
    section does not resolve and does not add up."""
    def total(cell: dict, *, usage: bool = False) -> Decimal:
        out = Decimal(0)
        for row in cell.get("rows", []):
            value = Decimal(str(row.get("contribution", row["value"])))
            if usage and row["concept"].endswith(":ContractWithCustomerLiabilityRevenueRecognized"):
                value = abs(value)
            out += value
        return out

    def charge(cell: dict) -> Decimal:
        by_concept: dict[str, list[dict]] = {}
        for row in cell.get("rows", []):
            by_concept.setdefault(row["concept"], []).append(row)
        counted = {sum((Decimal(str(row["value"])) for row in rows), Decimal(0))
                   for rows in by_concept.values()}
        assert len(counted) <= 1, "charge rows of different values are counted once"
        return counted.pop() if counted else Decimal(0)
    if "overlapping" in year["charged_to_expense"].get("missing", ""):
        return None
    return (Decimal(str(year["ending"]["value"]))
            - (Decimal(str(year["beginning"]["value"])) + charge(year["charged_to_expense"])
               + total(year["other"]) - total(year["usage"], usage=True)))


def check_period(year: dict, where) -> int:
    """The structural invariants of one period; 1 where it reads foots false and complete."""
    assert year["foots"] is (year["difference"]["value"] == 0), where
    assert year["complete"] is (not year["rows_not_placed"]), where
    recomputed = recomputed_difference(year)
    if recomputed is None:
        # overlapping charge elements: not complete, and no difference to recompute
        assert year["complete"] is False, where
        assert year["rows_not_placed"], where
    else:
        assert Decimal(str(year["difference"]["value"])) == recomputed, where
    return int(year["foots"] is False and year["complete"] is True)


def planted_periods():
    """Periods built here so the overlap and same-cell paths of the sweep run today: two charge
    elements with different values, two printed rows with equal values, one figure in one cell,
    and an overlap of negative charges."""
    for charges, same_cell in ((((("RestructuringCharges", 50),
                                   ("RestructuringCostsAndAssetImpairmentCharges", 70))), False),
                               ((("RestructuringCharges", 20),
                                 ("RestructuringSettlementAndImpairmentProvisions", 20)), False),
                               ((("RestructuringCosts", 70), ("RestructuringCharges", 70)), True),
                               ((("RestructuringCharges", -30), ("RestructuringCosts", -20)),
                                False)):
        tables = restructuring_tables(*charges, closing=140, same_cell=same_cell)
        yield (series_of(rollforwards.build(tables), "restructuring_reserve", "notes_1")
               ["periods"][0])


def test_over_all_committed_filings_each_period_is_what_its_own_rows_say(capsys):
    """Structural invariants over every period of the 72 committed filings and of the periods
    planted above, each worked out from the period's own cells and no counts held: `foots` is
    true exactly when `difference` is zero; `complete` is false exactly when `rows_not_placed` is
    not empty; and `difference` is the stated ending less the sum of the placed rows, recomputed
    here (a period with overlapping charge elements is not complete and has no difference to
    recompute). The independent evidence that the identity is right is in the hand-worked
    tables, not in this sweep."""
    filings = periods = false_and_complete = overlapping = 0
    for ticker, accession, cutoff in all_filings():
        filings += 1
        result = rollforwards.build(tables_of(ticker, accession, cutoff))
        for family in rollforwards.FAMILIES:
            for series in result[family].get("series", []):
                for year in series["periods"]:
                    if "foots" not in year:
                        continue
                    periods += 1
                    overlapping += recomputed_difference(year) is None
                    false_and_complete += check_period(
                        year, (ticker, accession, family, series["table"],
                               year["period"]["end"]))
    assert filings == 72
    assert periods > 0
    planted_count = 0
    for year in planted_periods():
        planted_count += 1
        check_period(year, "planted")
    assert planted_count == 4
    with capsys.disabled():
        print(f"\nrollforward sweep: {filings} filings, {periods} periods, "
              f"{false_and_complete} read foots false with complete true, "
              f"{overlapping} with overlapping charge elements; {planted_count} planted periods")


# --- the same figure twice, a row with no dated span -------------------------------------

def test_one_figure_tagged_twice_in_two_contexts_is_counted_once():
    """The same 400 provision for the same dates tagged twice: 1,000 + 400 - 300 = 1,100, not
    1,500."""
    rows = table_of("ProductWarrantyAccrual", "ProductWarrantyAccrualWarrantiesIssued",
                    "ProductWarrantyAccrualPayments", opening=1_000, closing=1_100, charge=400,
                    spent=300)
    rows.append(fact("ProductWarrantyAccrualWarrantiesIssued", 400, **YEAR, number="c2"))
    year = period_of(series_of(rollforwards.build(planted(rows)), "product_warranty",
                               "notes_1"), CLOSING)
    assert year["charged_to_expense"]["value"] == 400
    assert year["charged_to_expense"]["facts"] == [f"{ACCESSION}:c1"]
    assert year["foots"] is True and year["complete"] is True


def test_a_duration_with_no_dated_span_is_a_row_not_placed_and_never_a_crash():
    rows = table_of("ProductWarrantyAccrual", "ProductWarrantyAccrualWarrantiesIssued",
                    "ProductWarrantyAccrualPayments", opening=1_000, closing=1_100, charge=400,
                    spent=300)
    rows.append(fact("ProductWarrantyAccrualPayments", 55, start=None, end=None, number="f1"))
    year = period_of(series_of(rollforwards.build(planted(rows)), "product_warranty",
                               "notes_1"), CLOSING)
    assert year["foots"] is True and year["usage"]["value"] == 300
    assert year["complete"] is False
    assert [row["fact"] for row in year["rows_not_placed"]] == [f"{ACCESSION}:f1"]


def test_a_conflicting_figure_for_one_span_is_no_period():
    rows = table_of("ProductWarrantyAccrual", "ProductWarrantyAccrualWarrantiesIssued",
                    "ProductWarrantyAccrualPayments", opening=1_000, closing=1_100, charge=400,
                    spent=300)
    rows.append(fact("ProductWarrantyAccrualWarrantiesIssued", 450, **YEAR, number="c2"))
    year = period_of(series_of(rollforwards.build(planted(rows)), "product_warranty",
                               "notes_1"), CLOSING)
    assert "twice" in year["missing"] and "foots" not in year


# --- goodwill has no release -------------------------------------------------------------

def test_a_negative_acquisition_adjustment_is_no_release_of_goodwill():
    """100 - 30 (impairment, usage) - 6 (a purchase accounting adjustment) = 64."""
    result = rollforwards.build(planted([
        fact("Goodwill", 100, at=OPENING, number="g1"),
        fact("GoodwillImpairmentLoss", 30, **YEAR, number="g2"),
        fact("GoodwillPurchaseAccountingAdjustments", -6, **YEAR, number="g3"),
        fact("Goodwill", 64, at=CLOSING, number="g4")]))
    year = period_of(series_of(result, "goodwill", "notes_1"), CLOSING)
    assert year["foots"] is True and year["usage"]["value"] == 30
    assert year["release"] is None and year["release_because"] == []
    assert "not a reserve" in year["release_note"]


# --- the bounds of each rule -------------------------------------------------------------

def span_table(start: str, end: str, *, opening_at: str, charge=400, spent=300,
               closing=1_100, other=None, other_concept=None) -> dict:
    rows = [fact("ProductWarrantyAccrual", 1_000, at=opening_at, number="b1"),
            fact("ProductWarrantyAccrualWarrantiesIssued", charge, start=start, end=end,
                 number="c1"),
            fact("ProductWarrantyAccrualPayments", spent, start=start, end=end, number="u1"),
            fact("ProductWarrantyAccrual", closing, at=end, number="b2")]
    if other_concept:
        rows.append(fact(other_concept, other, start=start, end=end, number="o1"))
    return planted(rows)


@pytest.mark.parametrize("start,end,days,year", [
    ("2025-01-17", "2025-12-31", 348, False), ("2025-01-16", "2025-12-31", 349, False),
    ("2025-01-15", "2025-12-31", 350, True), ("2025-01-01", "2025-12-31", 364, True),
    ("2024-12-27", "2025-12-31", 369, True),
    ("2024-12-12", "2025-12-31", 384, False), ("2024-12-17", "2025-12-31", 379, True),
    ("2024-12-16", "2025-12-31", 380, True), ("2024-12-15", "2025-12-31", 381, False)])
def test_coverage_is_read_over_spans_of_350_to_380_days_only(start, end, days, year):
    opening = (dt.date.fromisoformat(start) - dt.timedelta(days=1)).isoformat()
    result = rollforwards.build(span_table(start, end, opening_at=opening))
    period = period_of(series_of(result, "product_warranty", "notes_1"), end)
    assert period["period"]["days"] == days
    assert ("value" in period["coverage_years"]) is year


def test_a_balance_two_days_off_is_the_balance_and_five_days_off_is_none():
    near = rollforwards.build(span_table(YEAR["start"], YEAR["end"], opening_at="2024-12-29"))
    assert period_of(series_of(near, "product_warranty", "notes_1"), CLOSING)["foots"] is True
    for far in ("2024-12-27", "2024-12-20", "2025-01-10"):
        result = rollforwards.build(span_table(YEAR["start"], YEAR["end"], opening_at=far))
        period = period_of(series_of(result, "product_warranty", "notes_1"), CLOSING)
        assert "beginning" in period["missing"], far


def test_a_series_on_two_axes_is_not_grouped_by_the_first_alone():
    """Goodwill by segment and product: North with product A and with product B are two series,
    each 100 + 20 = 120 and 200 + 5 = 205."""
    def axes(product):
        return {"us-gaap:StatementBusinessSegmentsAxis": "x:NorthMember",
                "us-gaap:ProductOrServiceAxis": product}
    a, b = axes("x:AMember"), axes("x:BMember")
    result = rollforwards.build(planted([
        fact("Goodwill", 100, at=OPENING, axes=a, number="a1"),
        fact("GoodwillAcquiredDuringPeriod", 20, **YEAR, axes=a, number="a2"),
        fact("Goodwill", 120, at=CLOSING, axes=a, number="a3"),
        fact("Goodwill", 200, at=OPENING, axes=b, number="b1"),
        fact("GoodwillAcquiredDuringPeriod", 5, **YEAR, axes=b, number="b2"),
        fact("Goodwill", 205, at=CLOSING, axes=b, number="b3")]))
    series = result["goodwill"]["series"]
    assert [one["axes"]["us-gaap:ProductOrServiceAxis"] for one in series] == [
        "x:AMember", "x:BMember"]
    assert all(one["periods"][0]["foots"] and one["periods"][0]["complete"] for one in series)


def test_a_gross_base_on_a_superset_or_a_subset_of_the_axes_is_no_base():
    segment = {"us-gaap:StatementBusinessSegmentsAxis": "x:NorthMember"}
    both = {**segment, "us-gaap:ProductOrServiceAxis": "x:AMember"}
    schedule = [fact("ValuationAllowancesAndReservesBalance", 200, at=OPENING,
                     axes={**INVENTORY_TYPE, **segment}, number="b1"),
                fact("ValuationAllowancesAndReservesChargedToCostAndExpense", 10, **YEAR,
                     axes={**INVENTORY_TYPE, **segment}, number="c1"),
                fact("ValuationAllowancesAndReservesBalance", 210, at=CLOSING,
                     axes={**INVENTORY_TYPE, **segment}, number="b2")]
    for base_axes in (both, None):
        result = rollforwards.build(planted(schedule, [
            fact("InventoryGross", 1_000, at=OPENING, axes=base_axes, number="g1"),
            fact("InventoryGross", 1_200, at=CLOSING, axes=base_axes, number="g2")]))
        year = period_of(series_of(result, "inventory_reserve", "notes_1"), CLOSING)
        assert "missing" in year["ending_over_gross_base"]
    result = rollforwards.build(planted(schedule, [
        fact("InventoryGross", 1_000, at=OPENING, axes=segment, number="g1"),
        fact("InventoryGross", 1_200, at=CLOSING, axes=segment, number="g2")]))
    year = period_of(series_of(result, "inventory_reserve", "notes_1"), CLOSING)
    assert year["ending_over_gross_base"]["value"] == pytest.approx(210 / 1_200)


def test_a_row_of_another_member_is_no_row_of_this_series_but_a_row_on_more_axes_is():
    """North's own rollforward, a South row beside it (a series of its own, with balances), and
    an acquisition row on North and a deal: only the last is a row North's table does not place."""
    north = {"us-gaap:StatementBusinessSegmentsAxis": "x:NorthMember"}
    south = {"us-gaap:StatementBusinessSegmentsAxis": "x:SouthMember"}
    deal = {**north, "us-gaap:BusinessAcquisitionAxis": "x:DealMember"}
    rows = [fact("Goodwill", 100, at=OPENING, axes=north, number="n1"),
            fact("GoodwillAcquiredDuringPeriod", 20, **YEAR, axes=north, number="n2"),
            fact("Goodwill", 120, at=CLOSING, axes=north, number="n3"),
            fact("Goodwill", 50, at=OPENING, axes=south, number="s1"),
            fact("GoodwillAcquiredDuringPeriod", 10, **YEAR, axes=south, number="s2"),
            fact("Goodwill", 60, at=CLOSING, axes=south, number="s3")]
    clean = rollforwards.build(planted(rows))
    for one in clean["goodwill"]["series"]:
        assert one["periods"][0]["complete"] is True
    dealt = rollforwards.build(planted(rows + [
        fact("GoodwillAcquiredDuringPeriod", 7, **YEAR, axes=deal, number="d1")]))
    by = {one["axes"]["us-gaap:StatementBusinessSegmentsAxis"]: one["periods"][0]
          for one in dealt["goodwill"]["series"]}
    assert by["x:NorthMember"]["complete"] is False
    assert [row["fact"] for row in by["x:NorthMember"]["rows_not_placed"]] == [f"{ACCESSION}:d1"]
    assert by["x:SouthMember"]["complete"] is True


def test_a_row_with_no_stem_of_the_family_is_still_a_row_not_placed():
    rows = table_of("ProductWarrantyAccrual", "ProductWarrantyAccrualWarrantiesIssued",
                    "ProductWarrantyAccrualPayments", opening=1_000, closing=1_100, charge=400,
                    spent=300)
    rows.append(fact("zzz:SomethingTheFilerAddedThatNamesNothing", 5, **YEAR, number="z1"))
    year = period_of(series_of(rollforwards.build(planted(rows)), "product_warranty",
                               "notes_1"), CLOSING)
    assert year["complete"] is False and year["rows_not_placed"][0]["fact"] == f"{ACCESSION}:z1"


def test_the_release_flag_needs_a_charge_below_zero_and_a_fall_with_a_base_that_rose():
    zero = rollforwards.build(planted(table_of(
        "AllowanceForDoubtfulAccountsReceivableCurrent", "ProvisionForDoubtfulAccounts",
        "AllowanceForDoubtfulAccountsReceivableWriteOffs", opening=500, closing=470, charge=0,
        spent=30)))
    year = period_of(series_of(zero, "allowance_for_credit_losses", "notes_1"), CLOSING)
    assert year["foots"] is True and year["release"] is False
    # the base level: 200 + 10 - 60 = 150 fell, and a base of 1,000 then 1,000 did not rise
    level = period_of(series_of(inventory_reserve(150, (1_000, 1_000)), "inventory_reserve",
                                "notes_1"), CLOSING)
    assert level["release"] is False
    # the reserve level: 200 + 10 - 10 = 200 did not fall while the base rose
    flat = rollforwards.build(planted(
        [fact("ValuationAllowancesAndReservesBalance", 200, at=OPENING, axes=INVENTORY_TYPE,
              number="b1"),
         fact("ValuationAllowancesAndReservesChargedToCostAndExpense", 10, **YEAR,
              axes=INVENTORY_TYPE, number="c1"),
         fact("ValuationAllowancesAndReservesDeductions", 10, **YEAR, axes=INVENTORY_TYPE,
              number="u1"),
         fact("ValuationAllowancesAndReservesBalance", 200, at=CLOSING, axes=INVENTORY_TYPE,
              number="b2")],
        [fact("InventoryGross", 1_000, at=OPENING, number="g1"),
         fact("InventoryGross", 1_200, at=CLOSING, number="g2")]))
    assert period_of(series_of(flat, "inventory_reserve", "notes_1"), CLOSING)["release"] is False


def test_a_negative_revision_has_its_sign_in_the_ratio_over_the_charge():
    """100 - 6 of change in estimate: -6 / 100."""
    result = rollforwards.build(planted(table_of(
        "ProductWarrantyAccrual", "ProductWarrantyAccrualWarrantiesIssued",
        "ProductWarrantyAccrualPayments", opening=1_000, closing=1_094, charge=100,
        spent=0 + 0, other=-6,
        other_concept="ProductWarrantyAccrualPreexistingIncreaseDecrease")))
    year = period_of(series_of(result, "product_warranty", "notes_1"), CLOSING)
    assert year["prior_period_revision_over_current_expense"]["value"] == pytest.approx(-0.06)


def test_a_row_of_a_note_table_element_on_schedule_twos_type_axis_is_no_note_row():
    result = rollforwards.build(planted([
        fact("InventoryValuationReserves", 200, at=OPENING, axes=INVENTORY_TYPE, number="b1"),
        fact("InventoryWriteDown", 10, **YEAR, axes=INVENTORY_TYPE, number="c1"),
        fact("InventoryValuationReserves", 210, at=CLOSING, axes=INVENTORY_TYPE, number="b2")]))
    assert "missing" in result["inventory_reserve"]


def test_a_balance_split_at_a_date_is_no_row_of_the_span():
    """The current and noncurrent parts of the ending balance are instants, not flows."""
    rows = table_of("ProductWarrantyAccrual", "ProductWarrantyAccrualWarrantiesIssued",
                    "ProductWarrantyAccrualPayments", opening=1_000, closing=1_100, charge=400,
                    spent=300)
    rows += [fact("ProductWarrantyAccrualClassifiedCurrent", 600, at=CLOSING, number="k1"),
             fact("ProductWarrantyAccrualNoncurrent", 500, at=CLOSING, number="k2")]
    year = period_of(series_of(rollforwards.build(planted(rows)), "product_warranty",
                               "notes_1"), CLOSING)
    assert year["foots"] is True and year["complete"] is True and year["rows_not_placed"] == []


def test_nssc_prints_a_deduction_in_parentheses_and_tags_it_as_recoveries():
    """NSSC's 10-K filed 2026-08-24, Schedule II note 82, in thousands, the allowance for credit
    losses: beginning 32, charged 0 (printed "-"), deductions/(recoveries) printed (7), end 25;
    and beginning 131, charged 0, (99), end 32. The instance tags the 7 and the 99 as
    `ValuationAllowancesAndReservesRecoveries` with +7 and +99. 32 - 7 = 25 and 131 - 99 = 32."""
    for end, opening, row, closing in (("2025-06-30", 32, 7, 25), ("2024-06-30", 131, 99, 32)):
        year = one_period("NSSC", "0001104659-26-100081", "2026-08-24",
                          "allowance_for_credit_losses", "notes_82", end)
        (recovery,) = year["other"]["rows"]
        assert recovery["concept"] == "us-gaap:ValuationAllowancesAndReservesRecoveries"
        assert (recovery["value"], recovery["contribution"]) == (row * 1000, -row * 1000)
        assert recovery["sign_source"] == "printed" and recovery["sign_disagrees"] is True
        assert (year["beginning"]["value"], year["ending"]["value"]) == (
            opening * 1000, closing * 1000)
        assert year["foots"] is True and year["difference"]["value"] == 0
        assert year["complete"] is True


def test_a_charge_and_a_usage_row_keep_their_roles_direction_whatever_is_printed():
    """A usage row printed in parentheses is still taken away once, never added: 1,000 + 400 -
    300 = 1,100 with the 300 tagged +300 and printed (300)."""
    rows = table_of("ProductWarrantyAccrual", "ProductWarrantyAccrualWarrantiesIssued",
                    "ProductWarrantyAccrualPayments", opening=1_000, closing=1_100, charge=400,
                    spent=300)
    result = rollforwards.build(with_signs(planted(rows), {"u1": "negative", "c1": "negative"}))
    year = period_of(series_of(result, "product_warranty", "notes_1"), CLOSING)
    assert year["foots"] is True and "sign_source" not in year["usage"]
    assert "sign_source" not in year["charged_to_expense"]


def test_any_row_of_other_takes_its_printed_sign_and_the_difference_is_ending_less_rows():
    """A recoveries row tagged +7 and printed (7) against 32 - 7 = 25; printed 7 it would read 39
    and the stated 25 less 39 is -14."""
    rows = table_of("AllowanceForDoubtfulAccountsReceivableCurrent",
                    "ProvisionForDoubtfulAccounts", None, opening=32, closing=25, charge=0,
                    other=7, other_concept="ValuationAllowancesAndReservesRecoveries")
    # the schedule's own element needs its type axis: use a note table row of the other role
    rows = [one for one in rows if "Recoveries" not in one["concept"]] + [
        fact("FinancingReceivableAllowanceForCreditLossForeignCurrencyTranslation", 7, **YEAR,
             number="o1")]
    year = period_of(series_of(rollforwards.build(with_signs(planted(rows), {"o1": "negative"})),
                               "allowance_for_credit_losses", "notes_1"), CLOSING)
    assert year["foots"] is True
    year = period_of(series_of(rollforwards.build(with_signs(planted(rows), {"o1": "positive"})),
                               "allowance_for_credit_losses", "notes_1"), CLOSING)
    assert year["foots"] is False and year["difference"]["value"] == -14


def inline_page(*rows: str) -> bytes:
    return ('<html xmlns="http://www.w3.org/1999/xhtml" '
            'xmlns:ix="http://www.xbrl.org/2013/inlineXBRL"><body><table>'
            + "".join(f"<tr>{row}</tr>" for row in rows) + "</table></body></html>").encode()


def number_cell(fact_id: str, shown: str, sign: str = "") -> str:
    attribute = f' sign="{sign}"' if sign else ""
    return (f'<ix:nonFraction id="{fact_id}" name="x:Y" contextRef="c" unitRef="usd"'
            f'{attribute}>{shown}</ix:nonFraction>')


def test_a_negative_printed_with_a_hyphen_a_minus_sign_or_an_en_dash_is_a_printed_negative():
    page = inline_page(
        f"<td>hyphen</td><td>-{number_cell('h', '5')}</td>",
        f"<td>minus</td><td>\u2212{number_cell('m', '5')}</td>",
        f"<td>en dash</td><td>$ \u2013{number_cell('e', '5')}</td>",
        f"<td>split</td><td>(</td><td>{number_cell('p', '5')}</td><td>)</td>",
        f"<td>plain</td><td>{number_cell('q', '5')}</td>")
    assert note_tables.printed_signs(page) == {
        "h": "negative", "m": "negative", "e": "negative", "p": "negative", "q": "positive"}


def test_the_dash_of_an_empty_cell_beside_a_number_is_no_sign():
    """Generac's "Acquisitions of businesses, net | 22,641 | - | 22,641": the "-" is a cell of
    its own that says nothing was acquired, and the number after it is positive."""
    page = inline_page(f"<td>Acquisitions</td><td>{number_cell('a', '22,641')}</td><td>-</td>"
                       f"<td>{number_cell('b', '22,641')}</td>")
    assert note_tables.printed_signs(page) == {"a": "positive", "b": "positive"}


def test_the_tagged_sign_is_the_elements_own_and_is_kept_apart_from_the_printed_one():
    """Cisco's shape: printed 3, tagged `sign="-"`; Johnson Controls': printed (1), tagged +."""
    page = inline_page(f"<td>cisco</td><td>{number_cell('c', '3', '-')}</td>",
                       f"<td>jci</td><td>(</td><td>{number_cell('j', '1')}</td><td>)</td>")
    assert note_tables.tagged_signs(page) == {"c": "negative", "j": "positive"}
    assert note_tables.printed_signs(page) == {"c": "positive", "j": "negative"}


def test_a_row_printed_with_a_minus_sign_takes_it():
    """The other row tagged +20 and printed -20: 1,000 + 400 - 300 - 20 = 1,080 foots."""
    rows = table_of("ProductWarrantyAccrual", "ProductWarrantyAccrualWarrantiesIssued",
                    "ProductWarrantyAccrualPayments", opening=1_000, closing=1_080, charge=400,
                    spent=300, other=20, other_concept=TRANSLATION)
    page = inline_page(f"<td>x</td><td>\u2212{number_cell('o1', '20')}</td>")
    carried = with_signs(planted(rows), {key: value for key, value in
                                         note_tables.printed_signs(page).items()})
    year = period_of(series_of(rollforwards.build(carried), "product_warranty", "notes_1"),
                     CLOSING)
    assert year["foots"] is True and year["other"]["rows"][0]["sign_source"] == "printed"


def test_a_zero_row_of_other_carries_a_sign_source_too():
    rows = table_of("ProductWarrantyAccrual", "ProductWarrantyAccrualWarrantiesIssued",
                    "ProductWarrantyAccrualPayments", opening=1_000, closing=1_100, charge=400,
                    spent=300, other=0, other_concept=TRANSLATION)
    year = period_of(series_of(rollforwards.build(planted(rows)), "product_warranty",
                               "notes_1"), CLOSING)
    assert year["foots"] is True
    assert [row["sign_source"] for row in year["other"]["rows"]] == ["tagged"]
    assert year["other"]["sign_source"] == "tagged"


# Five tables whose printed rows do not add to the printed ending, worked by hand; each must
# read `foots` false with the difference shown, whatever the sign rules do to a row.
DOES_NOT_FOOT = [
    # 1,000 + 400 - 300 = 1,100, the filer printing 1,150: 50 over
    ("plain", dict(opening=1_000, closing=1_150, charge=400, spent=300), {}, 50),
    # 1,000 + 400 - 300 + 20 = 1,120 (a change in estimate, printed positive), printed 1,100: -20
    ("estimate", dict(opening=1_000, closing=1_100, charge=400, spent=300, other=20,
                      other_concept="ProductWarrantyAccrualPreexistingIncreaseDecrease"),
     {"o1": "positive"}, -20),
    # translation tagged +20 and printed (20): 1,000 + 400 - 20 - 300 = 1,080, printed 1,120: 40 over
    ("printed negative", dict(opening=1_000, closing=1_120, charge=400, spent=300, other=20,
                              other_concept=TRANSLATION), {"o1": "negative"}, 40),
    # translation tagged -20 and printed 20: 1,000 + 400 + 20 - 300 = 1,120, printed 1,080: -40
    ("printed positive", dict(opening=1_000, closing=1_080, charge=400, spent=300, other=-20,
                              other_concept=TRANSLATION), {"o1": "positive"}, -40),
    # a usage row printed in parentheses is still taken away once: 1,000 + 400 - 300 = 1,100,
    # printed 1,700 (what adding it back would give): 600 over
    ("usage in parentheses", dict(opening=1_000, closing=1_700, charge=400, spent=300), {
        "u1": "negative"}, 600),
]


@pytest.mark.parametrize("name,table,signs,gap", DOES_NOT_FOOT, ids=[one[0] for one in
                                                                   DOES_NOT_FOOT])
def test_a_table_that_does_not_foot_as_printed_reads_foots_false(name, table, signs, gap):
    rows = table_of("ProductWarrantyAccrual", "ProductWarrantyAccrualWarrantiesIssued",
                    "ProductWarrantyAccrualPayments", **table)
    year = period_of(series_of(rollforwards.build(with_signs(planted(rows), signs)),
                               "product_warranty", "notes_1"), CLOSING)
    assert year["foots"] is False and year["difference"]["value"] == gap


# --- Omnicell's Schedule II, in its own members ------------------------------------------

OMNICELL = ("OMCL", "0000926326-26-000006", "2026-02-26")


def omnicell_series(member: str) -> dict:
    result = rollforwards.build(tables_of(*OMNICELL))
    return next(one for one in result["schedule_two_other"]["series"] if one["member"] == member)


def test_a_filers_own_schedule_two_member_is_a_series_of_schedule_two_other_keyed_by_it():
    """Omnicell's 10-K filed 2026-02-26, Schedule II, in thousands, accounts receivable and
    unbilled receivables, 2023: beginning 5,153, charged 2,726, other 126, deductions 2,441,
    ending 5,564. 5,153 + 2,726 - 2,441 + 126 = 5,564, the instance's f-1376 (beginning), f-1377,
    f-1379, f-1378 and f-1380 (ending)."""
    series = omnicell_series("omcl:AccountsReceivableAndUnbilledReceivablesMember")
    assert series["table"] == "notes_65" and series["kind"] == "schedule_two"
    year = period_of(series, "2023-12-31")
    assert year["beginning"]["value"] == 5_153_000 and year["ending"]["value"] == 5_564_000
    assert year["charged_to_expense"]["value"] == 2_726_000
    assert year["usage"]["value"] == 2_441_000 and year["other"]["value"] == 126_000
    assert year["foots"] is True and year["complete"] is True
    assert year["difference"]["facts"] == ids("0000926326-26-000006", "f-1376", "f-1377",
                                              "f-1379", "f-1378", "f-1380")
    assert year["release"] is False
    # the three accounts of the table are three series, and none is the sum of the others
    members = {one["member"] for one in rollforwards.build(tables_of(*OMNICELL))[
        "schedule_two_other"]["series"]}
    assert members == {"omcl:AccountsReceivableAndUnbilledReceivablesMember",
                       "omcl:ContractWithCustomerAssetUnbilledReceivablesNoncurrentMember",
                       "omcl:NetInvestmentInSalesTypeLeasesMember"}


def test_omnicells_negative_charges_are_releases():
    """Unbilled receivables, 2023: 35 + (4) - 0 = 31 in thousands, the charge f-1382 = -4,000;
    net investment in sales-type leases, 2023: 308 + (51) = 257, the charge f-1387 = -51,000."""
    unbilled = period_of(omnicell_series(
        "omcl:ContractWithCustomerAssetUnbilledReceivablesNoncurrentMember"), "2023-12-31")
    assert unbilled["charged_to_expense"]["facts"] == ids("0000926326-26-000006", "f-1382")
    assert unbilled["charged_to_expense"]["value"] == -4_000
    assert (unbilled["beginning"]["value"], unbilled["ending"]["value"]) == (35_000, 31_000)
    assert unbilled["foots"] is True
    assert unbilled["release"] is True and unbilled["release_because"] == [
        "charged_to_expense_negative"]
    leases = period_of(omnicell_series("omcl:NetInvestmentInSalesTypeLeasesMember"), "2023-12-31")
    assert leases["charged_to_expense"]["facts"] == ids("0000926326-26-000006", "f-1387")
    assert leases["charged_to_expense"]["value"] == -51_000
    assert (leases["beginning"]["value"], leases["ending"]["value"]) == (308_000, 257_000)
    assert leases["release"] is True


def test_the_deferred_tax_valuation_allowance_is_no_account_of_schedule_two_other():
    result = rollforwards.build(tables_of("GNRC", GNRC_ACCESSION, "2026-02-18"))
    assert "missing" in result["schedule_two_other"]


# --- the printed sign, in the forms a filing really uses ---------------------------------

def one_cell(cell: str) -> dict:
    return note_tables.printed_signs(inline_page(f"<td>label</td>{cell}"))


def test_every_kind_of_space_inside_the_parentheses_is_a_space():
    thin, figure, narrow = " ", " ", " "
    assert one_cell(f"<td>({thin}{number_cell('t', '5')}{thin})</td>") == {"t": "negative"}
    assert one_cell(f"<td>({figure}{number_cell('f', '5')}{figure})</td>") == {"f": "negative"}
    assert one_cell(f"<td>{narrow}({number_cell('n', '5')}){narrow}</td>") == {"n": "negative"}
    assert one_cell(f"<td>(​{number_cell('z', '5')}​)</td>") == {"z": "negative"}


def test_a_minus_after_thin_and_narrow_spaces_is_a_minus():
    assert one_cell(f"<td>− {number_cell('n', '5')}</td>") == {"n": "negative"}
    assert one_cell(f"<td> - {number_cell('t', '5')}</td>") == {"t": "negative"}


def test_a_footnote_mark_before_a_minus_or_inside_the_parentheses_is_no_text():
    assert one_cell(f"<td><sup>(a)</sup> −{number_cell('a', '5')}</td>") == {"a": "negative"}
    assert one_cell(f"<td>(a) −{number_cell('b', '5')}</td>") == {"b": "negative"}
    assert one_cell(f"<td>({number_cell('p', '5')}<sup>(1)</sup>)</td>") == {"p": "negative"}
    assert one_cell(f"<td>({number_cell('q', '5')} (1))</td>") == {"q": "negative"}
    assert one_cell(f"<td>(1) {number_cell('c', '5')}</td>") == {"c": "positive"}
    assert one_cell(f"<td><sup>1</sup>\u2212{number_cell('s', '5')}</td>") == {"s": "negative"}
    assert one_cell(f"<td>({number_cell('u', '5')}<sup>*</sup>)</td>") == {"u": "negative"}


def test_a_percent_inside_the_parentheses_is_part_of_the_number():
    assert one_cell(f"<td>({number_cell('p', '5')}%)</td>") == {"p": "negative"}


def test_a_nested_fact_has_the_sign_of_the_cell_it_is_printed_in():
    nested = ('<ix:nonFraction id="o" name="x:Y" contextRef="c" unitRef="usd">'
              + number_cell("i", "5") + "</ix:nonFraction>")
    assert one_cell(f"<td>({nested})</td>") == {"o": "negative", "i": "negative"}
    assert one_cell(f"<td>{nested}</td>") == {"o": "positive", "i": "positive"}


def test_a_range_hyphen_is_no_minus():
    """FELE's 10-K (accession 0000038725-26-000009) prints the rate of compensation increase as
    "2.00 - 9.00%": f-1137, f-1139 and f-1141 are the upper bounds, read by eye in the inline
    document, and positive."""
    page = inline_page(f"<td>{number_cell('r1', '2.00')} - {number_cell('r2', '9.00')}%</td>")
    assert note_tables.printed_signs(page) == {"r1": "positive", "r2": "positive"}
    path = next(FIXTURES / "FELE" / entry["path"] for entry in json.loads(
        (FIXTURES / "FELE" / "manifest.json").read_text(encoding="utf-8"))["documents"]
                if entry["accession"] == "0000038725-26-000009"
                and entry["role"] == "primary_html")
    raw = path.read_bytes() if path.exists() else gzip.open(f"{path}.gz").read()
    raw = gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw
    signs = note_tables.printed_signs(raw)
    assert [signs[one] for one in ("f-1137", "f-1139", "f-1141")] == ["positive"] * 3


def test_a_dash_is_a_minus_only_when_nothing_else_stands_before_the_number_in_its_cell():
    """Text before the dash: "Total - 5" is not a minus; a currency sign or an opening
    parenthesis before it is no text; a missing closing parenthesis is no negative."""
    assert one_cell(f"<td>Total - {number_cell('t', '5')}</td>") == {"t": "positive"}
    assert one_cell(f"<td>x-{number_cell('x', '5')}</td>") == {"x": "positive"}
    assert one_cell(f"<td>$ -{number_cell('d', '5')}</td>") == {"d": "negative"}
    assert one_cell(f"<td>({number_cell('o', '5')}</td>") == {"o": "positive"}
    assert one_cell(f"<td>({number_cell('p', '5')}</td><td>x</td>") == {"p": "positive"}


def nested_warranty():
    """The refuter's planted table: every cell a fact nested in a fact, the outer in the
    company-wide context and the inner in a segment member's, translation tagged +20 and
    printed (20): 1,000 + 400 - (300) - (20) = 1,080."""
    def fact_of(number, name, context, shown):
        return (f'<ix:nonFraction id="{number}" name="us-gaap:{name}" contextRef="{context}" '
                f'unitRef="usd" decimals="0" scale="0">{shown}</ix:nonFraction>')

    def nested(outer, inner, name, outer_context, inner_context, shown):
        return (f'<ix:nonFraction id="{outer}" name="us-gaap:{name}" contextRef="{outer_context}" '
                f'unitRef="usd" decimals="0" scale="0">'
                + fact_of(inner, name, inner_context, shown) + "</ix:nonFraction>")
    balance, issued = "ProductWarrantyAccrual", "ProductWarrantyAccrualWarrantiesIssued"
    paid, move = ("ProductWarrantyAccrualPayments",
                  "StandardProductWarrantyAccrualForeignCurrencyTranslationGainLoss")
    rows = [("Balance at beginning", nested("b1", "b1m", balance, "i0", "i0m", "1,000"), ""),
            ("Provision", nested("c1", "c1m", issued, "d", "dm", "400"), ""),
            ("Payments", "(" + nested("u1", "u1m", paid, "d", "dm", "300"), ")"),
            ("Currency translation", "(" + nested("o1", "o1m", move, "d", "dm", "20"), ")"),
            ("Balance at end", nested("b2", "b2m", balance, "i1", "i1m", "1,080"), "")]
    html = ('<html xmlns="http://www.w3.org/1999/xhtml" '
            'xmlns:ix="http://www.xbrl.org/2013/inlineXBRL"><body><table>'
            + "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in rows)
            + "</table></body></html>").encode()

    def context(name, *, start=None, end=None, at=None, member=False):
        segment = ('<xbrli:segment><xbrldi:explicitMember dimension="us-gaap:'
                   'StatementBusinessSegmentsAxis">x:OnlyMember</xbrldi:explicitMember>'
                   "</xbrli:segment>" if member else "")
        period = (f"<xbrli:instant>{at}</xbrli:instant>" if at else
                  f"<xbrli:startDate>{start}</xbrli:startDate><xbrli:endDate>{end}</xbrli:endDate>")
        return (f'<xbrli:context id="{name}"><xbrli:entity><xbrli:identifier scheme="http://www.'
                f'sec.gov/CIK">1</xbrli:identifier>{segment}</xbrli:entity><xbrli:period>'
                f"{period}</xbrli:period></xbrli:context>")
    contexts = "".join([
        context("i0", at="2024-12-31"), context("i1", at="2025-12-31"),
        context("d", start="2025-01-01", end="2025-12-31"),
        context("i0m", at="2024-12-31", member=True), context("i1m", at="2025-12-31", member=True),
        context("dm", start="2025-01-01", end="2025-12-31", member=True)])
    values = {"b1": (balance, "i0", 1000), "b2": (balance, "i1", 1080), "c1": (issued, "d", 400),
              "u1": (paid, "d", 300), "o1": (move, "d", 20)}
    facts = "".join(
        f'<us-gaap:{name} id="{key}{suffix}" contextRef="{ref}{suffix}" unitRef="usd" '
        f'decimals="0">{value}</us-gaap:{name}>'
        for key, (name, ref, value) in values.items() for suffix in ("", "m")).replace(
        'contextRef="d"', 'contextRef="d"')
    instance = ('<xbrli:xbrl xmlns:xbrli="http://www.xbrl.org/2003/instance" '
                'xmlns:xbrldi="http://xbrl.org/2006/xbrldi" '
                'xmlns:us-gaap="http://fasb.org/us-gaap/2025" '
                'xmlns:iso4217="http://www.xbrl.org/2003/iso4217">' + contexts
                + '<xbrli:unit id="usd"><xbrli:measure>iso4217:USD</xbrli:measure></xbrli:unit>'
                + facts + "</xbrli:xbrl>").encode()
    paragraphs = [(f"{ACCESSION}:notes:{at}", text)
                  for at, text in enumerate(note_tables.inline_tables(html)) if text.startswith("|")]
    return note_tables.tables(paragraphs, html, instance, accession=ACCESSION,
                              cutoff="2026-02-01")


def test_a_table_of_nested_facts_foots_in_the_outer_and_the_inner_series():
    tables = nested_warranty()
    assert tables["printed_signs"][f"{ACCESSION}:o1m"] == "negative"
    # a fact nested in another is in the cell of its outer fact: the figure is one
    assert tables["same_cell_facts"][f"{ACCESSION}:c1"] == [f"{ACCESSION}:c1m"]
    assert tables["same_cell_facts"][f"{ACCESSION}:c1m"] == [f"{ACCESSION}:c1"]
    # only flows carry a printed sign: the balances (instants) are not listed
    assert not {f"{ACCESSION}:b1", f"{ACCESSION}:b2m"} & set(tables["printed_signs"])
    result = rollforwards.build(tables)
    series = {tuple(one["axes"].values()): one for one in result["product_warranty"]["series"]}
    assert set(series) == {(), ("x:OnlyMember",)}
    for one in series.values():
        year = one["periods"][0]
        # 1,000 + 400 - 300 - 20 = 1,080 with the (20) printed on a +20 tag
        assert year["foots"] is True and year["difference"]["value"] == 0
        assert year["other"]["rows"][0]["contribution"] == -20
        assert year["other"]["rows"][0]["sign_source"] == "printed"


# --- Restructuring costs are the provision -----------------------------------------------

def test_dells_severance_liability_foots_in_each_year():
    """Dell's 10-K filed 2026-03-16, note 92, in millions, severance liability: fiscal 2026
    238 + 569 - 671 = 136; fiscal 2025 352 + 693 - 807 = 238; fiscal 2024 408 + 648 - 704 = 352
    (`RestructuringCosts` is the charge, "Cash paid and other" `PaymentsForRestructuring`)."""
    series = series_of(rollforwards.build(tables_of("DELL", "0001571996-26-000008",
                                                    "2026-03-16")),
                       "restructuring_reserve", "notes_92")
    for end, opening, charge, paid, closing in (
            ("2026-01-30", 238, 569, 671, 136), ("2025-01-31", 352, 693, 807, 238),
            ("2024-02-02", 408, 648, 704, 352)):
        year = period_of(series, end)
        assert (year["beginning"]["value"], year["charged_to_expense"]["value"],
                year["usage"]["value"], year["ending"]["value"]) == (
            opening * 1e6, charge * 1e6, paid * 1e6, closing * 1e6)
        assert year["foots"] is True and year["complete"] is True


def test_dells_quarterly_severance_liability_foots_in_each_span():
    """Dell's 10-Q filed 2026-09-08, note 51, in millions: three months to July 31, 2026
    242 + 261 - 164 = 339; six months 136 + 488 - 285 = 339; three months to August 1, 2025
    151 + 204 - 144 = 211; six months 238 + 334 - 361 = 211."""
    series = series_of(rollforwards.build(tables_of("DELL", "0001571996-26-000046",
                                                    "2026-09-08")),
                       "restructuring_reserve", "notes_51")
    spans = {(year["period"]["start"], year["period"]["end"]): year for year in series["periods"]}
    for span, (opening, charge, paid, closing) in {
            ("2026-05-02", "2026-07-31"): (242, 261, 164, 339),
            ("2026-01-31", "2026-07-31"): (136, 488, 285, 339),
            ("2025-05-03", "2025-08-01"): (151, 204, 144, 211),
            ("2025-02-01", "2025-08-01"): (238, 334, 361, 211)}.items():
        year = spans[span]
        assert (year["beginning"]["value"], year["charged_to_expense"]["value"],
                year["usage"]["value"], year["ending"]["value"]) == (
            opening * 1e6, charge * 1e6, paid * 1e6, closing * 1e6)
        assert year["foots"] is True and year["complete"] is True


def test_johnson_controls_impairment_column_foots_with_the_costs_and_impairment_charges():
    """Johnson Controls' 10-Q filed 2026-07-29, note 30, in millions, the long-lived asset
    impairments column: balance 0 (printed "-"), restructuring and related costs 53, utilized
    noncash (53): 0 + 53 - 53 = 0. The "Other" row is the filer's `jci:RestructuringCostsOther`,
    so the table is not complete."""
    result = rollforwards.build(tables_of("JCI", "0000833444-26-000087", "2026-07-29"))
    series = next(one for one in result["restructuring_reserve"]["series"]
                  if one["table"] == "notes_30" and one["axes"].get(
                      "us-gaap:RestructuringCostAndReserveAxis") == "jci:FixedAssetImpairmentMember")
    year = series["periods"][0]
    assert (year["beginning"]["value"], year["charged_to_expense"]["value"],
            year["usage"]["value"], year["ending"]["value"]) == (0, 53e6, 53e6, 0)
    assert year["foots"] is True and year["complete"] is False
    assert {row["concept"] for row in year["rows_not_placed"]} == {"jci:RestructuringCostsOther"}


# --- rules held by a test of their own ---------------------------------------------------

def test_a_change_in_estimate_takes_its_printed_sign_and_so_does_its_ratio():
    """Tagged +6 and printed (6) over a charge of 100: 1,000 + 100 - 6 = 1,094 foots, and the
    revision over the charge is -6 / 100."""
    rows = table_of("ProductWarrantyAccrual", "ProductWarrantyAccrualWarrantiesIssued",
                    "ProductWarrantyAccrualPayments", opening=1_000, closing=1_094, charge=100,
                    spent=0, other=6,
                    other_concept="ProductWarrantyAccrualPreexistingIncreaseDecrease")
    year = period_of(series_of(rollforwards.build(with_signs(planted(rows), {"o1": "negative"})),
                               "product_warranty", "notes_1"), CLOSING)
    assert year["foots"] is True and year["other"]["rows"][0]["contribution"] == -6
    assert year["prior_period_revision_over_current_expense"]["value"] == pytest.approx(-0.06)


def other_rows(*rows: tuple[int, str | None]):
    """A warranty table whose `other` role holds the given (tagged value, printed sign) rows,
    ending where the tagged values put it."""
    concepts = ["StandardProductWarrantyAccrualForeignCurrencyTranslationGainLoss",
                "ProductWarrantyAccrualPreexistingIncreaseDecrease",
                "ProductWarrantyAccrualAdditionsFromBusinessAcquisition"]
    facts = [fact("ProductWarrantyAccrual", 1_000, at=OPENING, number="b1"),
             fact("ProductWarrantyAccrual", 1_000 + sum(value for value, _ in rows), at=CLOSING,
                  number="b2")]
    signs = {}
    for at, (value, printed) in enumerate(rows):
        facts.append(fact(concepts[at], value, **YEAR, number=f"o{at}"))
        if printed:
            signs[f"o{at}"] = printed
    result = rollforwards.build(with_signs(planted(facts), signs))
    return period_of(series_of(result, "product_warranty", "notes_1"), CLOSING)


def test_the_cell_level_sign_source_of_other():
    # only zero rows: nothing to read, tagged, no disagreement
    zero = other_rows((0, None))
    assert zero["other"]["sign_source"] == "tagged" and zero["other"]["sign_disagrees"] is False
    assert zero["other"]["rows"][0]["sign_source"] == "tagged"
    assert zero["other"]["rows"][0]["contribution"] == 0
    # a zero row beside a printed one does not turn the cell to tagged
    printed = other_rows((0, None), (5, "positive"))
    assert printed["other"]["sign_source"] == "printed"
    # printed and tagged rows together: the cell says tagged, a disagreement elsewhere says so
    mixed = other_rows((5, "positive"), (7, None))
    assert [row["sign_source"] for row in mixed["other"]["rows"]] == ["printed", "tagged"]
    assert mixed["other"]["sign_source"] == "tagged"
    # all printed, one against its tag
    both = other_rows((5, "positive"), (7, "negative"))
    assert both["other"]["sign_source"] == "printed" and both["other"]["sign_disagrees"] is True
    agree = other_rows((5, "positive"), (7, "positive"))
    assert agree["other"]["sign_source"] == "printed" and agree["other"]["sign_disagrees"] is False


def test_a_row_of_a_standard_schedule_two_account_is_no_row_of_a_filers_own_account():
    """A table of Schedule II holding a filer's own account whole (100 + 20 - 5 = 115) beside a
    charge row of the allowance for credit losses and of the deferred tax valuation allowance,
    each with no balances in this table: neither is a row of the filer's own account."""
    own = {SCHEDULE_AXIS: "x:ReturnsMember"}
    result = rollforwards.build(planted([
        fact("ValuationAllowancesAndReservesBalance", 100, at=OPENING, axes=own, number="r1"),
        fact("ValuationAllowancesAndReservesChargedToCostAndExpense", 20, **YEAR, axes=own,
             number="r2"),
        fact("ValuationAllowancesAndReservesDeductions", 5, **YEAR, axes=own, number="r3"),
        fact("ValuationAllowancesAndReservesBalance", 115, at=CLOSING, axes=own, number="r4"),
        fact("ValuationAllowancesAndReservesChargedToCostAndExpense", 9, **YEAR,
             axes={SCHEDULE_AXIS: "us-gaap:AllowanceForCreditLossMember"}, number="s1"),
        fact("ValuationAllowancesAndReservesChargedToCostAndExpense", 8, **YEAR,
             axes={SCHEDULE_AXIS: "us-gaap:ValuationAllowanceOfDeferredTaxAssetsMember"},
             number="s2")]))
    (series,) = result["schedule_two_other"]["series"]
    assert series["member"] == "x:ReturnsMember"
    year = series["periods"][0]
    assert year["foots"] is True and year["complete"] is True and year["rows_not_placed"] == []


SCHEDULE_AXIS = "us-gaap:ValuationAllowancesAndReservesTypeAxis"


# --- Broadcom's Schedule II: a filer's own addition row ----------------------------------

BROADCOM = ("AVGO", "0001730168-25-000121", "2025-12-18")
AVGO_ADDITION = "avgo:SECSchedule1209ValuationAllowancesAndReservesAddition"


def test_broadcoms_schedule_two_accounts_are_not_complete_and_name_the_addition_row():
    """Broadcom's 10-K filed 2025-12-18, Schedule II note 75, in millions. The additions of both
    accounts are `avgo:SECSchedule1209ValuationAllowancesAndReservesAddition`, the filer's own
    element, so the identity has no charge row and each of the six periods is short by it:
    allowance for distributor credit 418, 351 and 502 (fiscal 2025, 2024, 2023: 94 + 418 - 439 =
    73, 133 + 351 - 390 = 94, 125 + 502 - 494 = 133), allowance for doubtful accounts and sales
    returns 11, 17 and 5 (11 + 11 - 19 = 3, 4 + 17 - 10 = 11, 1 + 5 - 2 = 4)."""
    result = rollforwards.build(tables_of(*BROADCOM))
    series = {one["member"]: one for one in result["schedule_two_other"]["series"]}
    assert set(series) == {"avgo:AllowanceForDistributorCreditMember",
                           "avgo:AllowanceForDoubtfulAccountsAndSalesReturnsMember"}
    wanted = {"avgo:AllowanceForDistributorCreditMember": (418e6, 351e6, 502e6),
              "avgo:AllowanceForDoubtfulAccountsAndSalesReturnsMember": (11e6, 17e6, 5e6)}
    for member, added in wanted.items():
        years = series[member]["periods"]
        assert [year["period"]["end"] for year in years] == ["2025-11-02", "2024-11-03",
                                                              "2023-10-29"]
        for year, value in zip(years, added):
            assert year["foots"] is False and year["difference"]["value"] == value
            assert year["complete"] is False
            assert [(row["concept"], row["value"]) for row in year["rows_not_placed"]] == [
                (AVGO_ADDITION, value)]
            # no charge row was placed, so a release was never looked for
            assert year["release"] is None and "not read" in year["release_note"]


def test_a_filers_own_addition_row_is_not_a_charge_and_a_release_is_not_read():
    """Planted: a filer-own addition of -200 beside a deduction, the table not reading a charge:
    1,000 - 200 - 100 = 700 against a stated 900 leaves the -200 unplaced, `release` null."""
    own = {SCHEDULE_AXIS: "x:ReturnsMember"}
    result = rollforwards.build(planted([
        fact("ValuationAllowancesAndReservesBalance", 1_000, at=OPENING, axes=own, number="r1"),
        fact("x:SECSchedule1209Addition", -200, **YEAR, axes=own, number="r2"),
        fact("ValuationAllowancesAndReservesDeductions", 100, **YEAR, axes=own, number="r3"),
        fact("ValuationAllowancesAndReservesBalance", 700, at=CLOSING, axes=own, number="r4")]))
    year = result["schedule_two_other"]["series"][0]["periods"][0]
    assert year["foots"] is False and year["complete"] is False
    assert [row["value"] for row in year["rows_not_placed"]] == [-200]
    assert year["release"] is None


def test_a_period_whose_charge_was_read_has_a_release_that_is_true_or_false():
    result = rollforwards.build(planted(table_of(
        "AllowanceForDoubtfulAccountsReceivableCurrent", "ProvisionForDoubtfulAccounts",
        "AllowanceForDoubtfulAccountsReceivableWriteOffs", opening=500, closing=520, charge=50,
        spent=30)))
    year = period_of(series_of(result, "allowance_for_credit_losses", "notes_1"), CLOSING)
    assert year["release"] is False


# --- the deferred tax valuation allowance is told by its name ---------------------------

def one_member(member: str) -> dict:
    axes = {SCHEDULE_AXIS: member}
    return rollforwards.build(planted([
        fact("ValuationAllowancesAndReservesBalance", 1_000, at=OPENING, axes=axes, number="t1"),
        fact("ValuationAllowancesAndReservesChargedToCostAndExpense", -200, **YEAR, axes=axes,
             number="t2"),
        fact("ValuationAllowancesAndReservesBalance", 800, at=CLOSING, axes=axes, number="t3")]))


def assert_left_out(member: str, word: str) -> None:
    result = one_member(member)
    assert all("series" not in result[family] for family in rollforwards.FAMILIES), member
    assert [(one["member"], one["table"]) for one in result["left_out"]] == [(member, "notes_1")]
    assert word in result["left_out"][0]["reason"]


def test_a_member_with_valuation_allowance_and_tax_is_left_out_and_listed():
    assert_left_out("x:TaxValuationAllowanceMember", "tax")


def test_a_member_with_valuation_allowance_and_deferred_is_left_out_and_listed():
    assert_left_out("x:DeferredValuationAllowanceMember", "deferred")


def test_a_member_with_valuation_allowance_and_an_operating_loss_is_left_out_and_listed():
    assert_left_out("x:ValuationAllowanceOnNetOperatingLossesMember", "operatingloss")


def test_the_bare_valuation_allowance_member_is_left_out_and_listed():
    assert_left_out("x:ValuationAllowanceMember", "bare valuation allowance")


@pytest.mark.parametrize("member", [
    "abc:IncomeTaxValuationAllowanceMember", "abc:DeferredIncomeTaxValuationAllowanceMember",
    "abc:TaxValuationAllowanceMember", "abc:ValuationAllowanceOnDeferredIncomeTaxesMember",
    "abc:SECSchedule1209ValuationAllowanceIncomeTaxesMember", "abc:ValuationAllowanceMember",
    "abc:ValuationAllowanceOnNetOperatingLossesMember",
    "abc:DeferredTaxAssetValuationAllowanceMember",
    "us-gaap:ValuationAllowanceOfDeferredTaxAssetsMember"])
def test_the_tax_valuation_allowance_members_of_any_namespace_make_no_series(member):
    result = one_member(member)
    assert all("series" not in result[family] for family in rollforwards.FAMILIES)
    assert [one["member"] for one in result["left_out"]] == [member]


def test_a_filing_with_no_left_out_account_lists_none():
    assert rollforwards.build(planted(table_of(
        "ProductWarrantyAccrual", "ProductWarrantyAccrualWarrantiesIssued",
        "ProductWarrantyAccrualPayments", opening=1_000, closing=1_100, charge=400,
        spent=300)))["left_out"] == []


@pytest.mark.parametrize("member", ["x:ValuationAllowanceForReturnsMember",
                                    "x:SalesTaxReserveMember", "x:DeferredRevenueAllowanceMember",
                                    "x:OperatingLossReserveMember"])
def test_a_member_with_only_half_of_the_tax_valuation_name_is_an_account(member):
    result = one_member(member)
    (series,) = result["schedule_two_other"]["series"]
    assert series["member"] == member and series["periods"][0]["foots"] is True
    assert series["periods"][0]["release"] is True and result["left_out"] == []


@pytest.mark.parametrize("ticker,accession,cutoff", [
    BROADCOM, ("LFUS", "0001628280-26-009585", "2026-02-19"),
    ("LOGI", "0001032975-26-000021", "2026-05-21"),
    ("NVDA", "0001045810-26-000021", "2026-02-25"), OMNICELL])
def test_the_real_reserve_members_of_a_schedule_two_are_still_series(ticker, accession, cutoff):
    """Broadcom's distributor credit, Littelfuse's sales discounts and allowances, Logitech's
    customer incentive programs and others, NVIDIA's sales returns, Omnicell's receivables: no
    name says valuation allowance beside a deferred tax or a tax asset."""
    result = rollforwards.build(tables_of(ticker, accession, cutoff))
    members = {one["member"] for one in result["schedule_two_other"].get("series", [])}
    assert members
    assert not any("valuationallowance" in one.lower() and "tax" in one.lower()
                   for one in members)


# --- several charge elements in one period -----------------------------------------------

def restructuring_tables(*charges: tuple[str, int], closing: int, same_cell: bool = False,
                         opening: int = 100) -> dict:
    rows = [fact("RestructuringReserve", opening, at=OPENING, number="b1"),
            fact("PaymentsForRestructuring", 30, **YEAR, number="u1"),
            fact("RestructuringReserve", closing, at=CLOSING, number="b2")]
    rows += [fact(name, value, **YEAR, number=f"c{at}") for at, (name, value) in
             enumerate(charges)]
    tables = planted(rows)
    if same_cell:
        names = [f"{ACCESSION}:c{at}" for at in range(len(charges))]
        tables["same_cell_facts"] = {one: [other for other in names if other != one]
                                     for one in names}
    return tables


def restructuring(*charges: tuple[str, int], closing: int, same_cell: bool = False) -> dict:
    tables = restructuring_tables(*charges, closing=closing, same_cell=same_cell)
    return period_of(series_of(rollforwards.build(tables), "restructuring_reserve", "notes_1"),
                     CLOSING)


def test_the_same_figure_tagged_twice_in_one_cell_is_counted_once():
    """100 + 70 - 30 = 140, 70 tagged as both `RestructuringCosts` and `RestructuringCharges` in
    one cell (a fact nested in another, or two tags on one figure)."""
    year = restructuring(("RestructuringCosts", 70), ("RestructuringCharges", 70), closing=140,
                         same_cell=True)
    assert year["charged_to_expense"]["value"] == 70
    assert len(year["charged_to_expense"]["facts"]) == 2
    assert year["foots"] is True and year["complete"] is True and year["release"] is False
    assert year["provision_over_usage"]["value"] == pytest.approx(70 / 30)


def test_two_printed_rows_with_equal_values_are_overlapping_and_not_resolved():
    """100 + 20 (RestructuringCharges) + 20 (RestructuringSettlementAndImpairmentProvisions) - 30
    = 110: two rows that print the same number are two rows, and which is the charge is not
    known."""
    year = restructuring(("RestructuringCharges", 20),
                         ("RestructuringSettlementAndImpairmentProvisions", 20), closing=110)
    assert "overlapping charge elements" in year["charged_to_expense"]["missing"]
    assert year["complete"] is False and year["foots"] is False
    assert year["expected_ending"]["value"] == 70
    assert sorted(row["value"] for row in year["rows_not_placed"]) == [20, 20]


def test_the_allowances_two_provision_elements_with_equal_values_are_overlapping():
    result = rollforwards.build(planted([
        fact("AllowanceForDoubtfulAccountsReceivable", 100, at=OPENING, number="b1"),
        fact("AllowanceForDoubtfulAccountsReceivable", 110, at=CLOSING, number="b2"),
        fact("ProvisionForDoubtfulAccounts", 10, **YEAR, number="c1"),
        fact("ProvisionForLoanLossesExpensed", 10, **YEAR, number="c2"),
        fact("AllowanceForDoubtfulAccountsReceivableWriteOffs", 10, **YEAR, number="u1")]))
    year = period_of(series_of(result, "allowance_for_credit_losses", "notes_1"), CLOSING)
    assert "overlapping" in year["charged_to_expense"]["missing"]
    assert year["complete"] is False and year["release"] is None


def test_charge_elements_with_different_values_are_not_summed():
    """`RestructuringCharges` 50 beside `RestructuringCostsAndAssetImpairmentCharges` 70: which is
    the charge is not known, so neither is summed to 120 and the period is not complete."""
    year = restructuring(("RestructuringCharges", 50),
                         ("RestructuringCostsAndAssetImpairmentCharges", 70), closing=140)
    assert "overlapping charge elements" in year["charged_to_expense"]["missing"]
    assert year["expected_ending"]["value"] == 70           # 100 - 30, no charge
    assert year["complete"] is False
    assert sorted(row["value"] for row in year["rows_not_placed"]) == [50, 70]
    assert all(row["why"] == "overlapping charge elements not resolved"
               for row in year["rows_not_placed"])
    assert "missing" in year["provision_over_usage"] and year["release"] is None


def test_an_overlapping_period_lists_none_of_the_uncounted_charge_facts_in_its_identity():
    year = restructuring(("RestructuringCharges", 50),
                         ("RestructuringCostsAndAssetImpairmentCharges", 70), closing=140)
    charges = {f"{ACCESSION}:c0", f"{ACCESSION}:c1"}
    assert not charges & set(year["expected_ending"]["facts"])
    assert not charges & set(year["difference"]["facts"])
    assert {row["fact"] for row in year["rows_not_placed"]} == charges


def test_an_overlap_whose_charges_are_all_negative_is_a_release_and_a_mixed_one_is_not_read():
    negative = restructuring(("RestructuringCharges", -30), ("RestructuringCosts", -20),
                             closing=40)
    assert negative["release"] is True
    assert negative["release_because"] == ["charged_to_expense_negative"]
    assert negative["complete"] is False
    mixed = restructuring(("RestructuringCharges", -30), ("RestructuringCosts", 20), closing=90)
    assert mixed["release"] is None and mixed["release_because"] == []
    zero = restructuring(("RestructuringCharges", -30), ("RestructuringCosts", 0), closing=70)
    assert zero["release"] is None


def test_the_same_cell_facts_of_an_inline_table_are_read_from_its_cells():
    page = inline_page(
        f"<td>nested</td><td>"
        f'<ix:nonFraction id="o" name="x:Y" contextRef="c" unitRef="usd">'
        f"{number_cell('i', '5')}</ix:nonFraction></td>",
        f"<td>two tags</td><td>{number_cell('a', '5')}{number_cell('b', '5')}</td>",
        f"<td>two rows</td><td>{number_cell('c', '5')}</td><td>{number_cell('d', '5')}</td>")
    assert note_tables.same_cell_facts(page) == {"o": ["i"], "i": ["o"], "a": ["b"], "b": ["a"]}


# --- the dash rule's parenthesis ---------------------------------------------------------

def test_an_opening_parenthesis_before_a_dash_is_no_text_of_the_cell():
    assert one_cell(f"<td>(-{number_cell('a', '5')}</td>") == {"a": "negative"}
    assert one_cell(f"<td>( − {number_cell('b', '5')}</td>") == {"b": "negative"}
