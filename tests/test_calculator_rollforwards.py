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
"""

from __future__ import annotations

import json
import re
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
    assert year["beginning"]["facts"] == ids(GNRC_ACCESSION, "c140005329")
    assert year["usage"]["facts"] == ids(GNRC_ACCESSION, "c140005332")
    assert year["charged_to_expense"]["facts"] == ids(GNRC_ACCESSION, "c140005335")
    assert year["other"]["facts"] == ids(GNRC_ACCESSION, "c140005338")
    assert year["ending"]["facts"] == ids(GNRC_ACCESSION, "c140005341")
    assert year["difference"]["facts"] == ids(GNRC_ACCESSION, "c140005329", "c140005335",
                                              "c140005338", "c140005332", "c140005341")
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
    # 35,465 + 1,398 - 2,359 + 0 = 34,504 (the 2,359 is `ChargedToOtherAccounts`, signed)
    assert allowance["beginning"]["value"] == 35_465_000
    assert allowance["charged_to_expense"]["value"] == 1_398_000
    assert allowance["other"]["value"] == -2_359_000 + 0
    assert allowance["ending"]["value"] == 34_504_000
    assert allowance["foots"] is True
    inventory = period_of(series_of(generac, "inventory_reserve", "notes_195"), "2025-12-31")
    # 48,173 + 23,375 - 2,282 + 0 = 69,266
    assert (inventory["beginning"]["value"], inventory["ending"]["value"]) == (
        48_173_000, 69_266_000)
    assert inventory["foots"] is True
    # the valuation allowance of deferred tax assets is no reserve family of this section
    assert all("tax" not in json.dumps(one).lower() for one in
               generac["inventory_reserve"]["series"])


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
    assert period_of(series[None], "2025-12-31")["ending"]["facts"] == ids(
        GNRC_ACCESSION, "c140005123")


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
    assert year["beginning"]["facts"] == ids(CIEN_ACCESSION, "f-1037")
    assert year["charged_to_expense"]["facts"] == ids(CIEN_ACCESSION, "f-1039")
    assert year["usage"]["facts"] == ids(CIEN_ACCESSION, "f-1040")
    assert year["ending"]["facts"] == ids(CIEN_ACCESSION, "f-1041")
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


def test_a_translation_row_is_read_with_the_sign_that_makes_the_table_foot():
    """Filers differ over the sign of a reserve's translation row (Cisco and Johnson Controls
    tag a printed increase as negative): 1,000 + 400 - 300 - 20 = 1,080 with the row tagged
    +20 reads only if the row is reversed; tagged -20 it foots as it stands."""
    for tagged, sign in ((20, "reversed"), (-20, "as_tagged")):
        result = rollforwards.build(planted(table_of(
            "ProductWarrantyAccrual", "ProductWarrantyAccrualWarrantiesIssued",
            "ProductWarrantyAccrualPayments", opening=1_000, closing=1_080, charge=400,
            spent=300, other=tagged,
            other_concept="StandardProductWarrantyAccrualForeignCurrencyTranslationGainLoss")))
        year = period_of(series_of(result, "product_warranty", "notes_1"), CLOSING)
        assert year["foots"] is True and year["translation_sign"] == sign
        assert year["other"]["value"] == -20


def test_a_row_that_is_no_translation_is_never_reversed_to_make_a_table_foot():
    """The same 1,000 + 400 - 300 + 20 = 1,120 against a stated 1,080 with the 20 tagged as a
    change in estimate (an element whose sign is not in doubt) does not foot."""
    result = rollforwards.build(planted(table_of(
        "ProductWarrantyAccrual", "ProductWarrantyAccrualWarrantiesIssued",
        "ProductWarrantyAccrualPayments", opening=1_000, closing=1_080, charge=400, spent=300,
        other=20, other_concept="ProductWarrantyAccrualPreexistingIncreaseDecrease")))
    year = period_of(series_of(result, "product_warranty", "notes_1"), CLOSING)
    assert year["foots"] is False and year["translation_sign"] == "as_tagged"
    assert year["difference"]["value"] == -40


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


def test_the_seven_families_are_the_ones_the_task_names():
    assert set(rollforwards.FAMILIES) == {
        "allowance_for_credit_losses", "product_warranty", "inventory_reserve",
        "restructuring_reserve", "contract_liabilities", "supplier_finance_obligations",
        "goodwill"}


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
