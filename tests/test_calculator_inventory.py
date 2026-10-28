"""Inventory composition and the growth gap, judged against the filings.

docs/HEDGE_FUND_ANALYSIS.md §5.2 row 20. Expected values, read by eye from the
committed filings and through `tests/companyfacts_source.py` (which imports
nothing from `src/`):

- **NVIDIA's inventory note.** The 10-K filed 2026-02-25
  (`tests/fixtures/NVDA/10-K/nvda-20260125.htm`), "Certain balance sheet
  components": raw materials 3,807 and 3,408; work in process 8,822 and 3,399;
  finished goods 8,774 and 3,273; total inventories 21,403 and 10,080, at
  January 25, 2026 and January 26, 2025 (millions). Revenue 215,938 and 130,497
  (the income statement).
- **Arista's inventory note.** The 10-K filed 2026-02-17
  (`tests/fixtures/ANET/10-K/anet-20251231.htm`): raw materials 611.2 and
  565.4; finished goods 1,635.9 and 1,269.2; total inventories 2,247.1 and
  1,834.6 (millions). No work-in-process line.
"""

from __future__ import annotations

import pytest

from src import calculator
from tests import companyfacts_source as source

MILLION = 1_000_000
SECTION = "inventory_composition_and_growth_gap"

NVDA = {"ticker": "NVDA", "cutoff": "2026-02-25", "period_end": "2026-01-25", "form": "10-K"}
ANET = {"ticker": "ANET", "cutoff": "2026-02-17", "period_end": "2025-12-31", "form": "10-K"}

NOW, AGO = "2026-01-25", "2025-01-26"
NVIDIA_LINES = {"raw_materials": ("InventoryRawMaterialsNetOfReserves", 3_807, 3_408),
                "work_in_process": ("InventoryWorkInProcessNetOfReserves", 8_822, 3_399),
                "finished_goods": ("InventoryFinishedGoodsNetOfReserves", 8_774, 3_273)}


@pytest.fixture(scope="module")
def nvidia():
    return calculator.calculate(**NVDA)


@pytest.fixture(scope="module")
def arista():
    return calculator.calculate(**ANET)


def test_nvidias_rows_are_the_inventory_notes_figures():
    cut = NVDA["cutoff"]
    for name, (tag, now, ago) in NVIDIA_LINES.items():
        assert source.one_value("NVDA", tag, NOW, cut) == now * MILLION, name
        assert source.one_value("NVDA", tag, AGO, cut) == ago * MILLION, name
    assert source.one_value("NVDA", "InventoryNet", NOW, cut) == 21_403 * MILLION
    assert source.one_value("NVDA", "InventoryNet", AGO, cut) == 10_080 * MILLION
    assert 3_807 + 8_822 + 8_774 == 21_403 and 3_408 + 3_399 + 3_273 == 10_080


def test_each_share_is_its_line_over_the_three_now_and_a_year_earlier(nvidia):
    """Raw 3,807 / 21,403 and 3,408 / 10,080; work in process 8,822 / 21,403 and
    3,399 / 10,080; finished goods 8,774 / 21,403 and 3,273 / 10,080."""
    for name, (tag, now, ago) in NVIDIA_LINES.items():
        cell = nvidia[SECTION][f"inventory_{name}_share"]
        assert cell["value"] == pytest.approx(now / 21_403, rel=1e-12), name
        assert cell["a_year_earlier"]["value"] == pytest.approx(ago / 10_080, rel=1e-12), name
        line = cell["inputs"][name]
        assert (line["tag"], line["accession"], line["filed"]) == (
            tag, "0001045810-26-000021", "2026-02-25"), name
        assert cell["unit"] == "ratio"


def test_finished_goods_growth_less_revenue_growth_is_worked_by_hand(nvidia):
    """(8,774 / 3,273 - 1) - (215,938 / 130,497 - 1) = 1.680721... - 0.654735..."""
    expected = (8_774 - 3_273) / 3_273 - (215_938 - 130_497) / 130_497
    cell = nvidia[SECTION]["finished_goods_growth_minus_revenue_growth"]
    assert cell["value"] == pytest.approx(expected, rel=1e-12)
    assert cell["value"] == pytest.approx(1.0259857, abs=1e-7)


def test_inventory_growth_less_revenue_growth_is_worked_by_hand(nvidia):
    """(21,403 / 10,080 - 1) - (215,938 / 130,497 - 1) = 1.123313... - 0.654735..."""
    expected = (21_403 - 10_080) / 10_080 - (215_938 - 130_497) / 130_497
    cell = nvidia[SECTION]["inventory_growth_minus_revenue_growth"]
    assert cell["value"] == pytest.approx(expected, rel=1e-12)
    revenue = cell["inputs"]["revenue_growth"]["inputs"]["now"]
    assert revenue["value"] == 215_938 * MILLION


def test_a_line_the_company_never_states_is_null_and_out_of_the_sum(arista):
    """Arista prints no work in process: its share is null with the reason, never
    zero, and the other two are each over raw materials plus finished goods,
    611.2 / 2,247.1 and 1,635.9 / 2,247.1, which add to one."""
    section = arista[SECTION]
    missing = section["inventory_work_in_process_share"]
    assert missing["value"] is None and "in any period" in missing["missing"]
    raw = section["inventory_raw_materials_share"]["value"]
    finished = section["inventory_finished_goods_share"]["value"]
    assert raw == pytest.approx(611.2 / 2_247.1, rel=1e-9)
    assert finished == pytest.approx(1_635.9 / 2_247.1, rel=1e-9)
    assert raw + finished == pytest.approx(1.0, rel=1e-12)
    assert section["inventory_raw_materials_share"]["a_year_earlier"]["value"] == pytest.approx(
        565.4 / 1_834.6, rel=1e-9)


def test_the_section_reaches_the_filings_only_view(nvidia):
    view = calculator.filings_only(nvidia)
    assert view[SECTION]["inventory_finished_goods_share"]["value"] \
        == nvidia[SECTION]["inventory_finished_goods_share"]["value"]
