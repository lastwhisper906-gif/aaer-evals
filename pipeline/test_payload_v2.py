"""test_payload_v2.py — payload-v2 진단 추출기 계약 테스트 (specs/payload_v2.md §5).

픽스처: pipeline/fixtures/data/ (TST = 정상 계약 전체, BAD = 파싱 불가 날짜).
"""
import datetime
from pathlib import Path

import pytest

from payload_v2_extract import (PayloadV2Error, extract_8k_items,
                                extract_share_facts, parse_items)

FIXTURES = Path(__file__).parent / "fixtures" / "data"
CUTOFF = datetime.date(2015, 6, 30)


# ── §5-1 item 파싱 ──────────────────────────────────────────────────────────

def test_parse_items_single():
    assert parse_items("4.01") == ["4.01"]


def test_parse_items_multi_with_space():
    assert parse_items("2.02, 9.01") == ["2.02", "9.01"]


def test_parse_items_empty_and_blank_tokens():
    assert parse_items("") == []
    assert parse_items(None) == []
    assert parse_items("4.02,,9.01,") == ["4.02", "9.01"]


# ── §5-2 컷오프 필터 (8-K 채널) ─────────────────────────────────────────────

def test_8k_cutoff_excludes_post_cutoff_and_includes_equal():
    rows, cov = extract_8k_items("TST", CUTOFF, data_dir=FIXTURES)
    dates = [r["filing_date"] for r in rows]
    assert all(datetime.date.fromisoformat(d) <= CUTOFF for d in dates)
    # 컷오프 후(2015-07-01, items 4.02) 부재 — 기계 검증
    assert not any("4.02" in r["items"] for r in rows)
    # == cutoff (2015-06-30) 포함
    assert "2015-06-30" in dates


def test_8k_channel_only_8k_forms_and_raw_preserved():
    rows, _ = extract_8k_items("TST", CUTOFF, data_dir=FIXTURES)
    assert {r["form"] for r in rows} <= {"8-K", "8-K/A"}
    r401 = [r for r in rows if r["items"] == ["4.01"]]
    assert len(r401) == 1 and r401[0]["items_raw"] == "4.01"
    multi = [r for r in rows if r["items_raw"] == "2.02, 9.01"]
    assert len(multi) == 1 and multi[0]["items"] == ["2.02", "9.01"]
    # 8-K/A 빈 items 도 행으로 보존
    assert any(r["form"] == "8-K/A" and r["items"] == [] for r in rows)


def test_8k_coverage_records_uncached_subfiles():
    _, cov = extract_8k_items("TST", CUTOFF, data_dir=FIXTURES)
    assert cov["paginated_subfiles_listed_not_cached"] == ["CIK0000000001-submissions-001.json"]


# ── §5-3 주식수·EPS 단위 추출 + 교차 오염 부재 ─────────────────────────────

def test_share_facts_units_and_no_usd_contamination():
    facts, cov = extract_share_facts("TST", CUTOFF, data_dir=FIXTURES)
    assert "dei:EntityCommonStockSharesOutstanding" in facts
    assert "us-gaap:EarningsPerShareBasic" in facts
    assert "us-gaap:WeightedAverageNumberOfDilutedSharesOutstanding" in facts
    # USD 단위 화이트리스트(동결 빌더 영역)와 교차 오염 없음
    assert not any("Revenues" in tag for tag in facts)
    units = {v["unit"] for vals in facts.values() for v in vals}
    assert units <= {"shares", "USD/shares"}


def test_share_facts_cutoff_and_period_banding():
    facts, _ = extract_share_facts("TST", CUTOFF, data_dir=FIXTURES)
    for vals in facts.values():
        for v in vals:
            assert datetime.date.fromisoformat(v["filed"]) <= CUTOFF
    eps = facts["us-gaap:EarningsPerShareBasic"]
    # 202일 span(val 9.9, filed<=cutoff)은 밴드 탈락 — 동결 빌더 동일 규칙
    assert not any(v["value"] == 9.9 for v in eps)
    ptypes = {v["period_type"] for v in eps}
    assert ptypes == {"annual", "quarterly"}


# ── §5-4 최신 filed 승리 ────────────────────────────────────────────────────

def test_latest_filed_wins_per_period():
    facts, _ = extract_share_facts("TST", CUTOFF, data_dir=FIXTURES)
    shares = facts["dei:EntityCommonStockSharesOutstanding"]
    jan31 = [v for v in shares if v["end"] == "2015-01-31"]
    assert len(jan31) == 1
    assert jan31[0]["value"] == 1000500 and jan31[0]["filed"] == "2015-05-01"
    # filed 2015-08-01 (> cutoff) 인 2015-04-30 instant 는 부재
    assert not any(v["end"] == "2015-04-30" for v in shares)


# ── §5-5 파일 부재 fail-closed ─────────────────────────────────────────────

def test_missing_submissions_fail_closed():
    with pytest.raises(PayloadV2Error):
        extract_8k_items("NOSUCH", CUTOFF, data_dir=FIXTURES)


def test_missing_companyfacts_fail_closed():
    with pytest.raises(PayloadV2Error):
        extract_share_facts("BAD", CUTOFF, data_dir=FIXTURES)  # BAD/xbrl 비어 있음


# ── §5-6 파싱 불가 날짜 fail-closed ────────────────────────────────────────

def test_unparseable_date_raises_not_skips():
    with pytest.raises(PayloadV2Error):
        extract_8k_items("BAD", CUTOFF, data_dir=FIXTURES)
