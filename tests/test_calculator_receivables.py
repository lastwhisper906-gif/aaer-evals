"""The receivables extension, judged against the filings.

docs/HEDGE_FUND_ANALYSIS.md §5.2 row 18. Expected values, each read by eye from
a committed filing and, where companyfacts carries it, through
`tests/companyfacts_source.py` (which imports nothing from `src/`):

- **Littelfuse's past-due receivables.** The 10-K filed 2026-02-19
  (`tests/fixtures/LFUS/10-K/lfus-20251227.htm.gz`), note 1: "the Company had
  $ 9.3 million and $ 3.8 million of trade receivables greater than 90 days past
  due as of December 27, 2025 and December 28, 2024". Its balance sheet: trade
  receivables, less allowances, 363,215 and 294,371 (thousands). The two
  past-due amounts are dimensional facts -- the past-due axis, member "equal to
  or greater than 90 days" -- that companyfacts cannot carry, so this test reads
  them out of the committed XBRL instance with its own regular expressions and
  hands them to the calculator as the run bundle's `input_numbers.json`.
- **NVIDIA's receivables against revenue.** The 10-K filed 2026-02-25: accounts
  receivable, net 38,466 and 23,065; revenue 215,938 and 130,497 (millions).
- **Carrier's contract assets.** The 10-K filed 2026-02-05, contract balances:
  current 499, non-current 83, total 582 (millions).
- **Ciena's long-term receivables and contract assets.** The 10-K filed
  2025-12-12, contract balances: long-term accounts receivable 28,610 and
  contract assets for unbilled accounts receivable 157,868 (thousands).
"""

from __future__ import annotations

import gzip
import json
import re

import pytest

from src import calculator
from tests import companyfacts_source as source

MILLION = 1_000_000
THOUSAND = 1_000
SECTION = "receivables_extension"

LFUS = {"ticker": "LFUS", "cutoff": "2026-02-19", "period_end": "2025-12-27", "form": "10-K"}
LFUS_ACCESSION = "0001628280-26-009585"
PAST_DUE_AXIS = "us-gaap:FinancingReceivablesPeriodPastDueAxis"
OVER_NINETY = "us-gaap:FinancingReceivablesEqualToGreaterThan90DaysPastDueMember"


# --- a second reader of the instance, for the past-due facts ---------------------------------

CONTEXT = re.compile(r'<(?:\w+:)?context id="([^"]+)">(.*?)</(?:\w+:)?context>', re.S)
MEMBER = re.compile(r'<xbrldi:explicitMember dimension="([^"]+)">([^<]+)</xbrldi:explicitMember>')
INSTANT = re.compile(r"<(?:\w+:)?instant>([^<]+)</(?:\w+:)?instant>")
FACT = re.compile(r'<(us-gaap):(\w+) contextRef="([^"]+)"[^>]*id="([^"]+)"[^>]*unitRef="usd"[^>]*>'
                  r'([^<]+)</us-gaap:\w+>')


def past_due_facts_in_the_instance() -> list[dict]:
    """Every USD fact of the committed 10-K instance on the past-due axis alone,
    in the shape `input_numbers.json` carries."""
    raw = gzip.decompress((source.FIXTURES / "LFUS" / "10-K" / "lfus-20251227_htm.xml.gz")
                          .read_bytes()).decode("utf-8")
    contexts = {}
    for name, body in CONTEXT.findall(raw):
        members = MEMBER.findall(body)
        instant = INSTANT.findall(body)
        if members == [(PAST_DUE_AXIS, OVER_NINETY)] and instant:
            contexts[name] = instant[0]
    out = []
    for prefix, tag, context, fact_id, number in FACT.findall(raw):
        if context in contexts:
            out.append({"id": f"{LFUS_ACCESSION}:{fact_id}", "tag": tag, "prefix": prefix,
                        "unit": "iso4217:USD",
                        "context": {"instant": contexts[context],
                                    "segment": [{"dimension": PAST_DUE_AXIS, "member": OVER_NINETY}]},
                        "number": float(number), "nil": False, "form": "10-K",
                        "source_accession": LFUS_ACCESSION, "filing_date": LFUS["cutoff"]})
    return out


def bundle_with(tmp_path, facts: list[dict]):
    (tmp_path / "input_numbers.json").write_text(json.dumps({"facts": facts}), encoding="utf-8")
    return tmp_path


def test_the_instance_states_the_two_amounts_the_note_prints():
    """9.3 and 3.8 million, as note 1 prints them; tagged by the filer with an
    allowance element, which is why the axis member and not the tag says what
    the amount is."""
    facts = past_due_facts_in_the_instance()
    assert sorted((fact["context"]["instant"], fact["number"]) for fact in facts) == [
        ("2024-12-28", 3_800_000.0), ("2025-12-27", 9_300_000.0)]
    assert {fact["tag"] for fact in facts} == {"AllowanceForDoubtfulAccountsReceivableNoncurrent"}


def test_littelfuses_past_due_share_is_the_note_over_the_balance_sheet(tmp_path):
    """Worked by hand: 9,300 / 363,215 now, and 3,800 / 294,371 a year earlier (thousands)."""
    cutoff = LFUS["cutoff"]
    receivables_now = source.one_value("LFUS", "AccountsReceivableNetCurrent", "2025-12-27", cutoff)
    receivables_ago = source.one_value("LFUS", "AccountsReceivableNetCurrent", "2024-12-28", cutoff)
    assert (receivables_now, receivables_ago) == (363_215 * THOUSAND, 294_371 * THOUSAND)

    out = calculator.calculate(**LFUS, bundle=bundle_with(tmp_path, past_due_facts_in_the_instance()))
    cell = out[SECTION]["past_due_receivables_share"]
    assert cell["value"] == pytest.approx(9_300 / 363_215, rel=1e-12)
    assert cell["as_of"] == "2025-12-27"
    assert cell["a_year_earlier"]["value"] == pytest.approx(3_800 / 294_371, rel=1e-12)
    over = cell["inputs"]["past_due_over_ninety_days"]
    assert (over["tag"], over["accession"], over["filed"], over["period"]) == (
        "AllowanceForDoubtfulAccountsReceivableNoncurrent", LFUS_ACCESSION, "2026-02-19",
        "2025-12-27")
    assert over["axis"] == f"{PAST_DUE_AXIS} = {OVER_NINETY}"
    assert calculator.filings_only(out)[SECTION]["past_due_receivables_share"]["value"] \
        == cell["value"]


def test_a_financing_book_on_the_past_due_axis_is_set_aside_and_named(tmp_path):
    """Cisco's shape, planted: loan receivables aged on the same axis are not trade
    receivables, so a planted 50 million there leaves the share where it was."""
    planted = dict(past_due_facts_in_the_instance()[0], id="P:f-1", tag="NotesReceivableGross",
                   number=50_000_000.0)
    facts = past_due_facts_in_the_instance() + [planted]
    out = calculator.calculate(**LFUS, bundle=bundle_with(tmp_path, facts))
    cell = out[SECTION]["past_due_receivables_share"]
    assert cell["value"] == pytest.approx(9_300 / 363_215, rel=1e-12)
    assert "NotesReceivableGross" in cell["set_aside"]


def test_a_past_due_fact_filed_after_the_cutoff_is_not_read(tmp_path):
    late = [dict(fact, filing_date="2026-02-20") for fact in past_due_facts_in_the_instance()]
    out = calculator.calculate(**LFUS, bundle=bundle_with(tmp_path, late))
    cell = out[SECTION]["past_due_receivables_share"]
    assert cell["value"] is None and "states no fact" in cell["missing"]


def test_with_no_bundle_the_share_is_null_and_says_why():
    out = calculator.calculate(**LFUS)
    cell = out[SECTION]["past_due_receivables_share"]
    assert cell["value"] is None and "no run bundle was given" in cell["missing"]


# --- receivables against revenue -------------------------------------------------------------

@pytest.fixture(scope="module")
def nvidia():
    return calculator.calculate(ticker="NVDA", cutoff="2026-02-25", period_end="2026-01-25",
                                form="10-K")


def nvidia_rows() -> dict:
    cut = "2026-02-25"
    return {"receivables": (source.one_value("NVDA", "AccountsReceivableNetCurrent", "2026-01-25", cut),
                            source.one_value("NVDA", "AccountsReceivableNetCurrent", "2025-01-26", cut)),
            "revenue": (source.one_value("NVDA", "Revenues", "2025-01-27..2026-01-25", cut),
                        source.one_value("NVDA", "Revenues", "2024-01-29..2025-01-26", cut))}


def test_nvidias_rows_are_the_printed_figures():
    rows = nvidia_rows()
    assert rows["receivables"] == (38_466 * MILLION, 23_065 * MILLION)
    assert rows["revenue"] == (215_938 * MILLION, 130_497 * MILLION)


def test_receivables_growth_less_revenue_growth_is_worked_by_hand(nvidia):
    """(38,466 / 23,065 - 1) - (215,938 / 130,497 - 1) = 0.667722... - 0.654735... """
    expected = (38_466 - 23_065) / 23_065 - (215_938 - 130_497) / 130_497
    cell = nvidia[SECTION]["receivables_growth_minus_revenue_growth"]
    assert cell["value"] == pytest.approx(expected, rel=1e-12)
    assert cell["value"] == pytest.approx(0.0129863, abs=1e-7)


def test_the_days_sales_outstanding_index_is_beneishs_by_hand(nvidia):
    """Beneish's index: (receivables / sales) now over the same a year earlier,
    (38,466 / 215,938) / (23,065 / 130,497)."""
    cell = nvidia[SECTION]["days_sales_outstanding_index"]
    assert cell["value"] == pytest.approx((38_466 / 215_938) / (23_065 / 130_497), rel=1e-12)
    receivables = cell["inputs"]["receivables"]
    assert (receivables["tag"], receivables["accession"], receivables["filed"]) == (
        "AccountsReceivableNetCurrent", "0001045810-26-000021", "2026-02-25")


def test_contract_assets_are_current_plus_noncurrent_over_revenue():
    """Carrier, millions: (499 + 83) / revenue, and 582 is the note's own total."""
    cut = "2026-02-05"
    current = source.one_value("CARR", "ContractWithCustomerAssetNetCurrent", "2025-12-31", cut)
    noncurrent = source.one_value("CARR", "ContractWithCustomerAssetNetNoncurrent", "2025-12-31", cut)
    revenue = source.one_value("CARR", "RevenueFromContractWithCustomerExcludingAssessedTax",
                               "2025-01-01..2025-12-31", cut)
    assert (current, noncurrent) == (499 * MILLION, 83 * MILLION)
    out = calculator.calculate(ticker="CARR", cutoff=cut, period_end="2025-12-31", form="10-K")
    cell = out[SECTION]["contract_assets_over_revenue"]
    assert cell["value"] == pytest.approx(582 * MILLION / revenue, rel=1e-12)
    assert cell["inputs"]["contract_assets"]["formula"] == "current + noncurrent"


def test_a_total_tag_stands_in_where_no_split_is_tagged_and_long_term_receivables_are_read():
    """Ciena, thousands: contract assets 157,868 (tagged as a total only) and long-term
    accounts receivable 28,610, each over fiscal 2025 revenue."""
    cut = "2025-12-12"
    revenue = source.one_value("CIEN", "Revenues", "2024-11-03..2025-11-01", cut)
    assert source.one_value("CIEN", "AccountsReceivableNetNoncurrent", "2025-11-01", cut) \
        == 28_610 * THOUSAND
    assert source.one_value("CIEN", "ContractWithCustomerAssetNet", "2025-11-01", cut) \
        == 157_868 * THOUSAND
    out = calculator.calculate(ticker="CIEN", cutoff=cut, period_end="2025-11-01", form="10-K")
    section = out[SECTION]
    assert section["long_term_receivables_over_revenue"]["value"] == pytest.approx(
        28_610 * THOUSAND / revenue, rel=1e-12)
    assert section["contract_assets_over_revenue"]["value"] == pytest.approx(
        157_868 * THOUSAND / revenue, rel=1e-12)
    assert "its total line is read" in \
        section["contract_assets_over_revenue"]["inputs"]["contract_assets"]["note"]


def test_a_ratio_whose_numerator_the_record_never_tags_is_null_not_zero(nvidia):
    """The independent reader finds no us-gaap concept named for contract assets in
    NVIDIA's record, and no noncurrent accounts receivable under any name (its one
    noncurrent receivable concept is income taxes receivable), so both ratios are
    null with the reason, never zero."""
    concepts = source.record("NVDA")["facts"]["us-gaap"]
    assert [tag for tag in concepts if tag.startswith("ContractWithCustomerAsset")] == []
    assert [tag for tag in concepts if "AccountsReceivable" in tag and "Noncurrent" in tag
            and source.rows("NVDA", tag)] == []
    for name in ("contract_assets_over_revenue", "long_term_receivables_over_revenue"):
        cell = nvidia[SECTION][name]
        assert cell["value"] is None, name
        assert "in any period" in cell["missing"], name
