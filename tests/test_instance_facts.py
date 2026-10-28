"""One filing's instance on demand: dimensional, extension and non-numeric facts.

The instances served here are the committed fixtures, each held to the sha256
its manifest row records, served from a planted local server at the path the
EDGAR Archives use. Every expected value was read by eye off the instance and is
quoted beside it; none was read off the reader under test.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src import cutoff_guard, instance_facts
from src.edgar_client import CacheMismatch, EdgarClient, EdgarError
from tests.planted_edgar import DIRECT, SAMPLE_CONTACT, serve

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def manifest_row(ticker: str, name: str) -> dict:
    manifest = json.loads((FIXTURES / ticker / "manifest.json").read_text(encoding="utf-8"))
    [row] = [d for d in manifest["documents"] if d["path"].endswith("/" + name)]
    return row


FILINGS = {
    "NVDA": ("1045810", manifest_row("NVDA", "nvda-20260125_htm.xml")),
    "AAPL": ("320193", manifest_row("AAPL", "aapl-20250927_htm.xml")),
    "ANET": ("1596532", manifest_row("ANET", "anet-20251231_htm.xml")),
}


@pytest.fixture
def server():
    for planted in serve(default=None):
        for ticker, (cik, row) in FILINGS.items():
            name = row["path"].rsplit("/", 1)[1]
            path = "/" + instance_facts.archive_url(cik, row["accession"], name, base="")
            planted.bodies[path] = ((FIXTURES / ticker / row["path"]).read_bytes(), "")
        yield planted


def client(tmp_path):
    return EdgarClient(environ={"EDGAR_USER_AGENT": SAMPLE_CONTACT, "AAER_CACHE": str(tmp_path)},
                       opener=DIRECT, sleep=lambda seconds: None)


def read(tmp_path, server, ticker, *, cutoff=None, expected=True, fetcher=None):
    cik, row = FILINGS[ticker]
    filing = {"accession": row["accession"], "filing_date": row["filing_date"]}
    return instance_facts.fetch(
        fetcher or client(tmp_path), cik, filing, row["path"].rsplit("/", 1)[1],
        cutoff=cutoff or row["filing_date"],
        expected_sha256=row["sha256"] if expected else None, base=server.url + "/")


def test_the_archive_address_is_edgars():
    _, row = FILINGS["NVDA"]
    assert instance_facts.archive_url("0001045810", row["accession"], "nvda-20260125_htm.xml") \
        == row["url"]
    assert instance_facts.instance_name("aapl-20250927.htm") == "aapl-20250927_htm.xml"
    with pytest.raises(EdgarError):
        instance_facts.instance_name("form4.xml")


def test_nvidias_customer_concentration_is_read_against_its_axes(tmp_path, server):
    """The 10-K for fiscal 2026 (0001045810-26-000021), read by eye: two
    `us-gaap:ConcentrationRiskPercentage1` facts for 2025-01-27..2026-01-25,
    0.22 and 0.14, against `srt:MajorCustomersAxis` `nvda:CustomerOneMember`
    and `nvda:CustomerTwoMember`, `us-gaap:ConcentrationRiskByBenchmarkAxis`
    `us-gaap:SalesRevenueNetMember`, `us-gaap:ConcentrationRiskByTypeAxis`
    `us-gaap:CustomerConcentrationRiskMember` and
    `us-gaap:StatementBusinessSegmentsAxis` `nvda:ComputeAndNetworkingSegmentMember`;
    `decimals="2"`, `unitRef="number"`, whose `<unit id="number">` holds the
    measure `pure`.
    """
    found = read(tmp_path, server, "NVDA")
    revenue_share = {
        members["srt:MajorCustomersAxis"]: fact["value"]
        for fact in instance_facts.named(found, "us-gaap:ConcentrationRiskPercentage1")
        for members in [instance_facts.members(fact)]
        if members.get("us-gaap:ConcentrationRiskByBenchmarkAxis") == "us-gaap:SalesRevenueNetMember"
        and fact["context"].get("start") == "2025-01-27" and fact["context"].get("end") == "2026-01-25"
        and "srt:MajorCustomersAxis" in members
        and members.get("us-gaap:StatementBusinessSegmentsAxis")
        == "nvda:ComputeAndNetworkingSegmentMember"}
    assert revenue_share == {"nvda:CustomerOneMember": 0.22, "nvda:CustomerTwoMember": 0.14}
    one = [f for f in instance_facts.named(found, "us-gaap:ConcentrationRiskPercentage1")
           if f["value"] == 0.22][0]
    assert one["kind"] == "numeric" and one["unit"] == "pure" and one["decimals"] == "2"
    assert one["extension"] is False


def test_apples_auditor_is_read_as_text(tmp_path, server):
    """The 10-K `aapl-20250927.htm` (0000320193-25-000079), read by eye:
    `dei:AuditorName` "Ernst &amp; Young LLP", `dei:AuditorFirmId` "42",
    `dei:AuditorLocation` "San Jose, California" and
    `dei:IcfrAuditorAttestationFlag` "true", each in context `c-1`.
    """
    found = read(tmp_path, server, "AAPL")
    auditor = {name: [f["value"] for f in instance_facts.named(found, name)]
               for name in ("dei:AuditorName", "dei:AuditorFirmId", "dei:AuditorLocation",
                            "dei:IcfrAuditorAttestationFlag")}
    assert auditor == {"dei:AuditorName": ["Ernst & Young LLP"],
                       "dei:AuditorFirmId": ["42"],
                       "dei:AuditorLocation": ["San Jose, California"],
                       "dei:IcfrAuditorAttestationFlag": ["true"]}
    [name] = instance_facts.named(found, "dei:AuditorName")
    assert (name["kind"], name["unit"], name["context_ref"]) == ("text", None, "c-1")


def test_aristas_remaining_performance_obligation_is_its_own_extension(tmp_path, server):
    """The 10-K `anet-20251231.htm` (0001596532-26-000013), read by eye: one
    `anet:RevenueRemainingPerformanceObligationIncludingContractLiabilitiesDeferredRevenueAndOtherPerformanceObligationsAmount`
    in context `c-4`, `decimals="-8"`, `unitRef="usd"` (the measure
    `iso4217:USD`): 6100000000.
    """
    found = read(tmp_path, server, "ANET")
    [rpo] = instance_facts.named(
        found, "anet:RevenueRemainingPerformanceObligationIncludingContractLiabilities"
               "DeferredRevenueAndOtherPerformanceObligationsAmount")
    assert (rpo["value"], rpo["decimals"], rpo["context_ref"], rpo["unit"]) == \
        (6100000000.0, "-8", "c-4", "iso4217:USD")
    assert rpo["extension"] is True and rpo["kind"] == "numeric"
    assert not any(f["extension"] for f in found if f["name"].startswith(("us-gaap:", "dei:")))


def test_every_element_with_a_context_is_a_fact(tmp_path, server):
    """Counted independently: every `contextRef=` in the instance's bytes."""
    _, row = FILINGS["AAPL"]
    raw = (FIXTURES / "AAPL" / row["path"]).read_bytes()
    assert len(read(tmp_path, server, "AAPL")) == raw.count(b" contextRef=")


def test_the_instance_is_fetched_once(tmp_path, server):
    fetcher = client(tmp_path)
    first = read(tmp_path, server, "AAPL", fetcher=fetcher)
    second = read(tmp_path, server, "AAPL", fetcher=fetcher)
    assert first == second
    assert sum(server.hits.values()) == 1


def test_served_bytes_unlike_the_manifests_hash_are_refused(tmp_path, server):
    cik, row = FILINGS["AAPL"]
    name = row["path"].rsplit("/", 1)[1]
    path = "/" + instance_facts.archive_url(cik, row["accession"], name, base="")
    server.bodies[path] = (server.bodies[path][0].replace(b"San Jose", b"San Juan"), "")
    with pytest.raises(CacheMismatch):
        read(tmp_path, server, "AAPL")


def test_a_filing_after_the_cutoff_is_refused_before_any_request(tmp_path, server):
    with pytest.raises(cutoff_guard.CutoffGuardError, match="after the cutoff"):
        read(tmp_path, server, "NVDA", cutoff="2026-02-24")
    assert server.seen == []
