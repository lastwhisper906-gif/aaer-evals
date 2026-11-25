# FTNT — numbers report, 10-Q 0001262039-26-000021 (quarter ended 2026-06-30)

**Inputs read.**
- `input_trends.json`: the trend table. The formula inputs sit inside its cells.
- `input_numbers.json`: three XBRL instances — 10-K 0001262039-26-000007, 10-Q 0001262039-26-000013 and 10-Q 0001262039-26-000021. Its keys are `ticker`, `cutoff`, `documents` and `facts`, and nothing else. I read all 80,723 lines.
- `input_8k.md`: the earnings release, 0001262039-26-000018.
- `input_prior_predictions.md`: it says no prior run is on record.

**Not in my directory.** There are no articulation checks, no restatement traces and no fourth-quarter derivation. Neither `input_numbers.json` nor `input_trends.json` holds a section for any of them. I found no prices, abnormal returns, short interest, other company's files, prior probabilities or outcome window. The run is not broken on that count.

**Conventions.**
- `expected_direction` reads the sign of the year-over-year change Python printed in the quoted cell: positive is `up`, negative is `down`. For a release item, it reads the direction the release states. It is `none` where the item is insufficient, where no change is printed, or where only the concept changed. It reads a printed sign; it is not a forecast.
- `horizon` names the window of that printed change.
- Every number below is copied from my input. I computed none.

**Periods the record does not reach.** Two quarters have no cells at all, so they have no items:
- `quarters-back-2` (target 2025-12-30).
- `quarters-back-6` (target 2024-12-31).

The table gives this reason for both: no quarter ending within 20 days of the target date is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration; the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py. That derivation is not in my directory. As a result:
- `quarters-back-1` and `quarters-back-5` print no quarter-over-quarter change.
- Every quarterly position below is ranked among at most 6 filled quarters, all of them first, second or third fiscal quarters.

**Articulation gaps, restated values, changes of tag.**
- **Articulation.** No articulation check is in my input, so I have no articulation gap to report.
- **Restatement.** No restatement trace is in my input.
  - Facts from the 10-K and the first-quarter 10-Q carry `"superseded_by": "0001262039-26-000021"` where this 10-Q reports the same element and date again. The marker says a later filing reported the element. It does not say the value changed.
  - I compared the pairs by reading them. I did not run a check over every fact. In every pair I compared, the printed value is the same in the later filing:
    - the 2025-12-31 balance sheet: cash, short-term and long-term investments, receivables, inventory, prepaid expenses, current assets, PP&E, capitalized contract cost, deferred tax assets, goodwill, intangibles, other assets, total assets, payables, accrued and employee liabilities, current and noncurrent debt, current liabilities, other liabilities, total liabilities, and the equity lines;
    - the 2025-12-31 comparatives in this 10-Q's notes: the fair-value tables, inventory and its valuation reserve, PP&E, intangibles and debt.
  - So my input shows no restated prior value, and I wrote no restatement item.
- **Changes of tag.** Two balances changed concept between filings while keeping the same printed value: current and noncurrent deferred revenue.
  - The 10-K 0001262039-26-000007 files them as us-gaap:DeferredRevenueCurrent and us-gaap:DeferredRevenueNoncurrent.
  - Both 2026 10-Qs file the same 2025-12-31 balances as us-gaap:ContractWithCustomerLiabilityCurrent and us-gaap:ContractWithCustomerLiabilityNoncurrent, at the same printed values.
  - The trend table's 2024-12-31 contract-liability input reads ContractWithCustomerLiabilityCurrent from a filing dated 2025-11-07. The 10-K files that date under DeferredRevenueCurrent.
  - Neither 10-K deferred-revenue fact at 2025-12-31 carries a `superseded_by` marker. The 10-K's other 2025-12-31 liability facts that I read do carry one.
  - The items are under `structure_and_disclosure_changes_*` below. Within the trend table, every cell I checked for a given ratio reads the same concept.

**R&D-capitalisation block (`years-back-0`).** This block prints no `paragraph_id`, so I cannot write an item for it. Its printed values are:
- `book_value_with_rnd_capitalized` 3284520000.0
- `earnings_with_rnd_capitalized` 2147180000.0
- `research_and_development_asset` 2047020000.0
- `research_and_development_amortization` 521720000.0

`capitalized_development_cost` and `capitalized_over_expense` are missing. The record tags none of us-gaap:CapitalizedComputerSoftwareAdditions in any period.

## Seen in the statements

```json
[
  {
    "id": "earnings_quality_trend_accruals_over_total_assets_quarterly",
    "what_changed": "insufficient: the table could not fill accruals_over_total_assets for 2026-04-01..2026-06-30 because the record has no operating cash flow row for that three-month period (the 10-Q states cash flows year to date). The cell prints no value and no quarter-over-quarter or year-over-year change.",
    "account": "accruals: net income (NetIncomeLoss) less operating cash flow (NetCashProvidedByUsedInOperatingActivities), over total assets (Assets)",
    "expected_direction": "none",
    "horizon": "none: the cell prints no change",
    "quote": "\"missing\": \"no row for operating_cash_flow in 2026-04-01..2026-06-30: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
    "paragraph_id": "0001262039-26-000021:trends:accruals_over_total_assets:2026-04-01..2026-06-30"
  },
  {
    "id": "estimates_and_discretion_trend_bad_debt_reserve_ratio_quarterly",
    "what_changed": "insufficient: the table could not fill bad_debt_reserve_ratio for the quarter ended 2026-06-30 because the record has no allowance-for-doubtful-accounts row at 2026-06-30. The cell prints no value and no change.",
    "account": "allowance for doubtful accounts (AllowanceForDoubtfulAccountsReceivable) over gross receivables",
    "expected_direction": "none",
    "horizon": "none: the cell prints no change",
    "quote": "\"missing\": \"no row for bad_debt_allowance in 2026-06-30: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"",
    "paragraph_id": "0001262039-26-000021:trends:bad_debt_reserve_ratio:2026-04-01..2026-06-30"
  },
  {
    "id": "revenue_recognition_trend_contract_liabilities_over_revenue_quarterly",
    "what_changed": "contract_liabilities_over_revenue for 2026-04-01..2026-06-30 is 1.8759705063723815. Quarter-over-quarter change -0.13868131023661512 against quarters-back-1; year-over-year change -0.21758777583620725 against quarters-back-4. It is the lowest of the 6 filled quarters. Inputs printed, both from 0001262039-26-000021: ContractWithCustomerLiabilityCurrent 3841800000.0 at 2026-06-30, and RevenueFromContractWithCustomerExcludingAssessedTax 2047900000.0 for the quarter. The year-ago cell prints 3412500000.0 and 1630000000.0 for the same two inputs.",
    "account": "current contract liabilities (ContractWithCustomerLiabilityCurrent) over quarterly revenue (RevenueFromContractWithCustomerExcludingAssessedTax)",
    "expected_direction": "down",
    "horizon": "year over year, against quarters-back-4 (2025-04-01..2025-06-30)",
    "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
    "paragraph_id": "0001262039-26-000021:trends:contract_liabilities_over_revenue:2026-04-01..2026-06-30"
  },
  {
    "id": "liquidity_and_capital_trend_days_sales_of_inventory_quarterly",
    "what_changed": "days_sales_of_inventory for 2026-04-01..2026-06-30 is 95.85693106004447. Quarter-over-quarter change 4.597671800785221 against quarters-back-1; year-over-year change -21.238019717980308 against quarters-back-4. The two changes point opposite ways. It is the second lowest of the 6 filled quarters. Inputs printed: InventoryNet 426300000.0 at 2026-06-30, CostOfGoodsAndServicesSold 404700000.0 for the quarter, 91 days.",
    "account": "inventory (InventoryNet) over cost of revenue (CostOfGoodsAndServicesSold), in days",
    "expected_direction": "down",
    "horizon": "year over year, against quarters-back-4 (2025-04-01..2025-06-30)",
    "quote": "\"position_in_history\": \"second lowest of the 6 filled quarters\"",
    "paragraph_id": "0001262039-26-000021:trends:days_sales_of_inventory:2026-04-01..2026-06-30"
  },
  {
    "id": "revenue_recognition_trend_days_sales_outstanding_quarterly",
    "what_changed": "days_sales_outstanding for 2026-04-01..2026-06-30 is 64.68069729967284. Quarter-over-quarter change -7.636560485794277 against quarters-back-1; year-over-year change -3.1896707984866595 against quarters-back-4. It is the third lowest of the 6 filled quarters. Inputs printed: AccountsReceivableNetCurrent 1455600000.0 at 2026-06-30, revenue 2047900000.0 for the quarter, 91 days.",
    "account": "net accounts receivable (AccountsReceivableNetCurrent) over quarterly revenue, in days",
    "expected_direction": "down",
    "horizon": "year over year, against quarters-back-4 (2025-04-01..2025-06-30)",
    "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
    "paragraph_id": "0001262039-26-000021:trends:days_sales_outstanding:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_trend_gross_margin_quarterly",
    "what_changed": "gross_margin for 2026-04-01..2026-06-30 is 0.8023829288539479. Quarter-over-quarter change -0.0005474344678514376 against quarters-back-1; year-over-year change -0.004426887096972365 against quarters-back-4. It is the lowest of the 6 filled quarters. Inputs printed: revenue 2047900000.0 and CostOfGoodsAndServicesSold 404700000.0 for the quarter.",
    "account": "gross margin: revenue less cost of revenue, over revenue",
    "expected_direction": "down",
    "horizon": "year over year, against quarters-back-4 (2025-04-01..2025-06-30)",
    "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
    "paragraph_id": "0001262039-26-000021:trends:gross_margin:2026-04-01..2026-06-30"
  },
  {
    "id": "estimates_and_discretion_trend_inventory_reserve_ratio_quarterly",
    "what_changed": "inventory_reserve_ratio at 2026-06-30 is 0.2880600516068496. Quarter-over-quarter change -0.05095509990830188 against quarters-back-1; year-over-year change -0.07324300861032712 against quarters-back-4. It is the lowest of the 6 filled quarters. Inputs printed: InventoryValuationReserves 122800000.0 and InventoryNet 426300000.0 at 2026-06-30. The year-ago cell prints 146400000.0 and 405200000.0, so the reserve balance printed is smaller than a year earlier while the inventory printed is larger. The prior-quarter cell prints a reserve of 125300000.0.",
    "account": "inventory valuation reserve (InventoryValuationReserves) over net inventory (InventoryNet)",
    "expected_direction": "down",
    "horizon": "year over year, against quarters-back-4 (2025-06-30)",
    "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
    "paragraph_id": "0001262039-26-000021:trends:inventory_reserve_ratio:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_trend_non_gaap_gap_quarterly",
    "what_changed": "insufficient: the table cannot fill non_gaap_gap for 2026-04-01..2026-06-30, or for any period, because companyfacts carries no non-GAAP measure. The coverage block prints filled 0 for this ratio. The release's reconciliation (paragraph 0001262039-26-000018:8k_2_02:76) prints GAAP net income 606.3 and non-GAAP net income 665.0 for the quarter, in millions. No gap figure exists anywhere in my input, and I did not compute one.",
    "account": "gap between non-GAAP and GAAP net income",
    "expected_direction": "none",
    "horizon": "none: the cell prints no change",
    "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
    "paragraph_id": "0001262039-26-000021:trends:non_gaap_gap:2026-04-01..2026-06-30"
  },
  {
    "id": "revenue_recognition_trend_receivables_over_revenue_quarterly",
    "what_changed": "receivables_over_revenue for 2026-04-01..2026-06-30 is 0.7107768934029982. Quarter-over-quarter change -0.09274819310219207 against quarters-back-1; year-over-year change -0.03505132745589745 against quarters-back-4. It is the third lowest of the 6 filled quarters. Inputs printed: AccountsReceivableNetCurrent 1455600000.0 at 2026-06-30, revenue 2047900000.0 for the quarter. The year-ago cell prints 1215700000.0 and 1630000000.0.",
    "account": "net accounts receivable (AccountsReceivableNetCurrent) over quarterly revenue",
    "expected_direction": "down",
    "horizon": "year over year, against quarters-back-4 (2025-04-01..2025-06-30)",
    "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
    "paragraph_id": "0001262039-26-000021:trends:receivables_over_revenue:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_trend_soft_asset_share_quarterly",
    "what_changed": "soft_asset_share at 2026-06-30 is 0.5732282304405482. Quarter-over-quarter change -0.030626679257433342 against quarters-back-1; year-over-year change 0.03494379418216109 against quarters-back-4. The two changes point opposite ways. It is the third lowest of the 6 filled quarters. Inputs printed: Assets 10859200000.0, CashAndCashEquivalentsAtCarryingValue 2934900000.0 and PropertyPlantAndEquipmentNet 1699500000.0 at 2026-06-30.",
    "account": "soft assets: total assets less PP&E and cash, over total assets",
    "expected_direction": "up",
    "horizon": "year over year, against quarters-back-4 (2025-06-30)",
    "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
    "paragraph_id": "0001262039-26-000021:trends:soft_asset_share:2026-04-01..2026-06-30"
  },
  {
    "id": "estimates_and_discretion_trend_warranty_reserve_ratio_quarterly",
    "what_changed": "insufficient: the table could not fill warranty_reserve_ratio at 2026-06-30 because the record has no warranty-accrual row for that date. The coverage block prints filled 0 for this ratio: it is filled in no quarter and no year of the window.",
    "account": "product warranty accrual over product revenue",
    "expected_direction": "none",
    "horizon": "none: the cell prints no change",
    "quote": "\"missing\": \"no row for warranty_accrual in 2026-06-30: us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent is in the record, but not for this period\"",
    "paragraph_id": "0001262039-26-000021:trends:warranty_reserve_ratio:2026-04-01..2026-06-30"
  },
  {
    "id": "earnings_quality_trend_accruals_over_total_assets_annual",
    "what_changed": "accruals_over_total_assets for 2025-01-01..2025-12-31 is -0.07095830285296269. Year-over-year change -0.01842375952143889 against years-back-1. It is the second highest of the 5 filled years. Inputs printed: NetIncomeLoss 1853400000.0 and NetCashProvidedByUsedInOperatingActivities 2590600000.0 for 2025 (0001262039-26-000007), and Assets 10389200000.0 at 2025-12-31 (0001262039-26-000021).",
    "account": "accruals: net income less operating cash flow, over total assets",
    "expected_direction": "down",
    "horizon": "year over year, against years-back-1 (2024-01-01..2024-12-31)",
    "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
    "paragraph_id": "0001262039-26-000021:trends:accruals_over_total_assets:2025-01-01..2025-12-31"
  },
  {
    "id": "estimates_and_discretion_trend_bad_debt_reserve_ratio_annual",
    "what_changed": "bad_debt_reserve_ratio at 2025-12-31 is 0.0043565289061580125. Year-over-year change 0.00034101131274618356 against years-back-1. It is the second highest of the 5 filled years. Inputs printed: AllowanceForDoubtfulAccountsReceivable 7400000.0 (0001262039-26-000007) and AccountsReceivableNetCurrent 1691200000.0 (0001262039-26-000021) at 2025-12-31.",
    "account": "allowance for doubtful accounts (AllowanceForDoubtfulAccountsReceivable) over gross receivables",
    "expected_direction": "up",
    "horizon": "year over year, against years-back-1 (2024-12-31)",
    "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
    "paragraph_id": "0001262039-26-000021:trends:bad_debt_reserve_ratio:2025-01-01..2025-12-31"
  },
  {
    "id": "revenue_recognition_trend_contract_liabilities_over_revenue_annual",
    "what_changed": "contract_liabilities_over_revenue for 2025-01-01..2025-12-31 is 0.5347373374904406. Year-over-year change -0.015348293323220075 against years-back-1. It is the third highest of the 5 filled years. Inputs printed: ContractWithCustomerLiabilityCurrent 3636000000.0 at 2025-12-31 (0001262039-26-000021), and RevenueFromContractWithCustomerExcludingAssessedTax 6799600000.0 for 2025 (0001262039-26-000007). The 10-K files the same 2025-12-31 balance under DeferredRevenueCurrent, at the same printed value, and the cell does not read that fact. See the structure_and_disclosure_changes items.",
    "account": "current contract liabilities (ContractWithCustomerLiabilityCurrent) over annual revenue",
    "expected_direction": "down",
    "horizon": "year over year, against years-back-1 (2024-01-01..2024-12-31)",
    "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
    "paragraph_id": "0001262039-26-000021:trends:contract_liabilities_over_revenue:2025-01-01..2025-12-31"
  },
  {
    "id": "liquidity_and_capital_trend_days_sales_of_inventory_annual",
    "what_changed": "days_sales_of_inventory for 2025-01-01..2025-12-31 is 109.72797050191888. Year-over-year change 9.975897246908517 against years-back-1. It is the second highest of the 5 filled years. Inputs printed: InventoryNet 399500000.0 at 2025-12-31, CostOfGoodsAndServicesSold 1328900000.0 for 2025, 365 days.",
    "account": "inventory (InventoryNet) over cost of revenue, in days",
    "expected_direction": "up",
    "horizon": "year over year, against years-back-1 (2024-01-01..2024-12-31)",
    "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
    "paragraph_id": "0001262039-26-000021:trends:days_sales_of_inventory:2025-01-01..2025-12-31"
  },
  {
    "id": "revenue_recognition_trend_days_sales_outstanding_annual",
    "what_changed": "days_sales_outstanding for 2025-01-01..2025-12-31 is 90.78298723454321. Year-over-year change 0.8531037596112157 against years-back-1. It is the third highest of the 5 filled years. Inputs printed: AccountsReceivableNetCurrent 1691200000.0 at 2025-12-31, revenue 6799600000.0 for 2025, 365 days.",
    "account": "net accounts receivable over annual revenue, in days",
    "expected_direction": "up",
    "horizon": "year over year, against years-back-1 (2024-01-01..2024-12-31)",
    "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
    "paragraph_id": "0001262039-26-000021:trends:days_sales_outstanding:2025-01-01..2025-12-31"
  },
  {
    "id": "earnings_quality_trend_gross_margin_annual",
    "what_changed": "gross_margin for 2025-01-01..2025-12-31 is 0.8045620330607682. Year-over-year change -0.0010728102852138877 against years-back-1. It is the second highest of the 5 filled years. Inputs printed: revenue 6799600000.0 and CostOfGoodsAndServicesSold 1328900000.0 for 2025.",
    "account": "gross margin: revenue less cost of revenue, over revenue",
    "expected_direction": "down",
    "horizon": "year over year, against years-back-1 (2024-01-01..2024-12-31)",
    "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
    "paragraph_id": "0001262039-26-000021:trends:gross_margin:2025-01-01..2025-12-31"
  },
  {
    "id": "estimates_and_discretion_trend_inventory_reserve_ratio_annual",
    "what_changed": "inventory_reserve_ratio at 2025-12-31 is 0.344180225281602. Year-over-year change -0.11477381592283536 against years-back-1. It is the second highest of the 4 filled years: years-back-4 is not filled, see the history-gap item. Inputs printed: InventoryValuationReserves 137500000.0 and InventoryNet 399500000.0 at 2025-12-31. The years-back-1 cell prints 144800000.0 and 315500000.0.",
    "account": "inventory valuation reserve (InventoryValuationReserves) over net inventory (InventoryNet)",
    "expected_direction": "down",
    "horizon": "year over year, against years-back-1 (2024-12-31)",
    "quote": "\"position_in_history\": \"second highest of the 4 filled years\"",
    "paragraph_id": "0001262039-26-000021:trends:inventory_reserve_ratio:2025-01-01..2025-12-31"
  },
  {
    "id": "earnings_quality_trend_non_gaap_gap_annual",
    "what_changed": "insufficient: the table cannot fill non_gaap_gap for 2025-01-01..2025-12-31 because companyfacts carries no non-GAAP measure. No year of the window is filled.",
    "account": "gap between non-GAAP and GAAP net income",
    "expected_direction": "none",
    "horizon": "none: the cell prints no change",
    "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
    "paragraph_id": "0001262039-26-000021:trends:non_gaap_gap:2025-01-01..2025-12-31"
  },
  {
    "id": "revenue_recognition_trend_receivables_over_revenue_annual",
    "what_changed": "receivables_over_revenue for 2025-01-01..2025-12-31 is 0.24872051297135125. Year-over-year change 0.003010448832192786 against years-back-1. It is the third highest of the 5 filled years. Inputs printed: AccountsReceivableNetCurrent 1691200000.0 at 2025-12-31, revenue 6799600000.0 for 2025.",
    "account": "net accounts receivable over annual revenue",
    "expected_direction": "up",
    "horizon": "year over year, against years-back-1 (2024-01-01..2024-12-31)",
    "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
    "paragraph_id": "0001262039-26-000021:trends:receivables_over_revenue:2025-01-01..2025-12-31"
  },
  {
    "id": "earnings_quality_trend_soft_asset_share_annual",
    "what_changed": "soft_asset_share at 2025-12-31 is 0.6039829823278019. Year-over-year change 0.0367758452504392 against years-back-1. It is the third highest of the 5 filled years. Inputs printed: Assets 10389200000.0, CashAndCashEquivalentsAtCarryingValue 2495300000.0 and PropertyPlantAndEquipmentNet 1619000000.0 at 2025-12-31.",
    "account": "soft assets: total assets less PP&E and cash, over total assets",
    "expected_direction": "up",
    "horizon": "year over year, against years-back-1 (2024-12-31)",
    "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
    "paragraph_id": "0001262039-26-000021:trends:soft_asset_share:2025-01-01..2025-12-31"
  },
  {
    "id": "estimates_and_discretion_trend_warranty_reserve_ratio_annual",
    "what_changed": "insufficient: the table could not fill warranty_reserve_ratio at 2025-12-31 because the record has no warranty-accrual row for that date. No year of the window is filled.",
    "account": "product warranty accrual over product revenue",
    "expected_direction": "none",
    "horizon": "none: the cell prints no change",
    "quote": "\"missing\": \"no row for warranty_accrual in 2025-12-31: us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent is in the record, but not for this period\"",
    "paragraph_id": "0001262039-26-000021:trends:warranty_reserve_ratio:2025-01-01..2025-12-31"
  },
  {
    "id": "earnings_quality_trend_accruals_over_total_assets_quarterly_history_depth",
    "what_changed": "insufficient for a trend claim: the quarterly accruals ratio is filled in only two quarters, quarters-back-1 and quarters-back-5. Those are the first fiscal quarters, the only ones whose year-to-date cash flow is a three-month figure. The quarters-back-1 cell (2026-01-01..2026-03-31) prints -0.054899580108261244, with a year-over-year change of -0.013590845602640025 against quarters-back-5. It prints no quarter-over-quarter change because quarters-back-2 is not filled. Two points do not make a trend.",
    "account": "accruals: net income less operating cash flow, over total assets",
    "expected_direction": "none",
    "horizon": "none: two filled quarters do not support a trend",
    "quote": "\"position_in_history\": \"lowest of the 2 filled quarters\"",
    "paragraph_id": "0001262039-26-000021:trends:accruals_over_total_assets:2026-01-01..2026-03-31"
  },
  {
    "id": "estimates_and_discretion_trend_bad_debt_reserve_ratio_quarterly_history_depth",
    "what_changed": "insufficient for a trend claim: the quarterly bad-debt reserve ratio is filled in a single quarter, quarters-back-7 (2024-07-01..2024-09-30), where it prints 0.004481311975591152. Every later quarter in the window lacks an allowance row in the record. The ratio can be followed only at fiscal year ends.",
    "account": "allowance for doubtful accounts over gross receivables",
    "expected_direction": "none",
    "horizon": "none: one filled quarter does not support a trend",
    "quote": "\"position_in_history\": \"the only filled quarter\"",
    "paragraph_id": "0001262039-26-000021:trends:bad_debt_reserve_ratio:2024-07-01..2024-09-30"
  },
  {
    "id": "estimates_and_discretion_trend_inventory_reserve_ratio_annual_history_gap",
    "what_changed": "insufficient: the table could not fill inventory_reserve_ratio for 2021-01-01..2021-12-31 because the record has no inventory-reserve row at 2021-12-31. The annual history of this ratio is therefore 4 filled years, not 5. The years-back-0 position (second highest of the 4 filled years) and the years-back-3 cell, which prints no year-over-year change, both rest on that shorter history.",
    "account": "inventory valuation reserve (InventoryValuationReserves) over net inventory",
    "expected_direction": "none",
    "horizon": "none: the cell prints no change",
    "quote": "\"missing\": \"no row for inventory_reserve in 2021-12-31: us-gaap:InventoryValuationReserves is in the record, but not for this period\"",
    "paragraph_id": "0001262039-26-000021:trends:inventory_reserve_ratio:2021-01-01..2021-12-31"
  },
  {
    "id": "structure_and_disclosure_changes_current_deferred_revenue_concept_quarterly_report",
    "what_changed": "Change of tag, not of value. This 10-Q (0001262039-26-000021, filed 2026-07-30) files the 2025-12-31 current deferred-revenue balance under us-gaap:ContractWithCustomerLiabilityCurrent at 3636000000. The 10-K 0001262039-26-000007 (filed 2026-02-25) filed the same date under us-gaap:DeferredRevenueCurrent at 3636000000, the same printed value. That 10-K fact carries no superseded_by marker. The 10-K's other 2025-12-31 liability facts that I read carry one, pointing to this 10-Q. The annual contract_liabilities_over_revenue cell for 2025 reads this 10-Q fact.",
    "account": "current deferred revenue / current contract liabilities",
    "expected_direction": "none",
    "horizon": "the 2025-12-31 balance as filed in the 10-K (2026-02-25) and in this 10-Q (2026-07-30)",
    "quote": "\"value\": \"3636000000\"",
    "paragraph_id": "0001262039-26-000021:facts:ContractWithCustomerLiabilityCurrent:2025-12-31"
  },
  {
    "id": "structure_and_disclosure_changes_current_deferred_revenue_concept_annual_report",
    "what_changed": "Change of tag, not of value, seen from the 10-K's side. The 10-K 0001262039-26-000007 files current deferred revenue at 2025-12-31 under us-gaap:DeferredRevenueCurrent at 3636000000. Both later 10-Qs in my input (0001262039-26-000013 and 0001262039-26-000021) file the same date under us-gaap:ContractWithCustomerLiabilityCurrent at 3636000000. No fact in my input reports DeferredRevenueCurrent at 2025-12-31 a second time, and this fact carries no superseded_by marker.",
    "account": "current deferred revenue / current contract liabilities",
    "expected_direction": "none",
    "horizon": "the 2025-12-31 balance as filed in the 10-K (2026-02-25)",
    "quote": "\"value\": \"3636000000\"",
    "paragraph_id": "0001262039-26-000007:facts:DeferredRevenueCurrent:2025-12-31"
  },
  {
    "id": "structure_and_disclosure_changes_current_deferred_revenue_concept_first_quarter_report",
    "what_changed": "Change of tag, not of value, already present in the first-quarter 10-Q. The 10-Q 0001262039-26-000013 (filed 2026-05-08) files current deferred revenue at 2025-12-31 under us-gaap:ContractWithCustomerLiabilityCurrent at 3636000000. The 10-K filed it as us-gaap:DeferredRevenueCurrent at 3636000000. This fact carries superseded_by 0001262039-26-000021, and this 10-Q prints the same value for the same element and date.",
    "account": "current deferred revenue / current contract liabilities",
    "expected_direction": "none",
    "horizon": "the 2025-12-31 balance as filed in the first-quarter 10-Q (2026-05-08)",
    "quote": "\"value\": \"3636000000\"",
    "paragraph_id": "0001262039-26-000013:facts:ContractWithCustomerLiabilityCurrent:2025-12-31"
  },
  {
    "id": "structure_and_disclosure_changes_noncurrent_deferred_revenue_concept_quarterly_report",
    "what_changed": "Change of tag, not of value. This 10-Q files the 2025-12-31 noncurrent deferred-revenue balance under us-gaap:ContractWithCustomerLiabilityNoncurrent at 3479800000. The 10-K 0001262039-26-000007 filed the same date under us-gaap:DeferredRevenueNoncurrent at 3479800000, the same printed value. That 10-K fact carries no superseded_by marker. No trend ratio reads the noncurrent balance. This 10-Q prints 3833900000 at 2026-06-30 under ContractWithCustomerLiabilityNoncurrent.",
    "account": "noncurrent deferred revenue / noncurrent contract liabilities",
    "expected_direction": "none",
    "horizon": "the 2025-12-31 balance as filed in the 10-K (2026-02-25) and in this 10-Q (2026-07-30)",
    "quote": "\"value\": \"3479800000\"",
    "paragraph_id": "0001262039-26-000021:facts:ContractWithCustomerLiabilityNoncurrent:2025-12-31"
  },
  {
    "id": "structure_and_disclosure_changes_noncurrent_deferred_revenue_concept_annual_report",
    "what_changed": "Change of tag, not of value, seen from the 10-K's side. The 10-K files noncurrent deferred revenue at 2025-12-31 under us-gaap:DeferredRevenueNoncurrent at 3479800000. Both later 10-Qs file the same date under us-gaap:ContractWithCustomerLiabilityNoncurrent at 3479800000. This fact carries no superseded_by marker. The 10-K also prints DeferredRevenueNoncurrent 3084700000 at 2024-12-31. No other filing in my input reports a noncurrent contract-liability balance at 2024-12-31, so that date has nothing to compare against.",
    "account": "noncurrent deferred revenue / noncurrent contract liabilities",
    "expected_direction": "none",
    "horizon": "the 2025-12-31 balance as filed in the 10-K (2026-02-25)",
    "quote": "\"value\": \"3479800000\"",
    "paragraph_id": "0001262039-26-000007:facts:DeferredRevenueNoncurrent:2025-12-31"
  },
  {
    "id": "structure_and_disclosure_changes_noncurrent_deferred_revenue_concept_first_quarter_report",
    "what_changed": "Change of tag, not of value, already present in the first-quarter 10-Q. The 10-Q 0001262039-26-000013 files noncurrent deferred revenue at 2025-12-31 under us-gaap:ContractWithCustomerLiabilityNoncurrent at 3479800000. The 10-K filed it as us-gaap:DeferredRevenueNoncurrent at 3479800000. This fact carries superseded_by 0001262039-26-000021, and this 10-Q prints the same value.",
    "account": "noncurrent deferred revenue / noncurrent contract liabilities",
    "expected_direction": "none",
    "horizon": "the 2025-12-31 balance as filed in the first-quarter 10-Q (2026-05-08)",
    "quote": "\"value\": \"3479800000\"",
    "paragraph_id": "0001262039-26-000013:facts:ContractWithCustomerLiabilityNoncurrent:2025-12-31"
  },
  {
    "id": "structure_and_disclosure_changes_current_deferred_revenue_concept_prior_year_end_annual_report",
    "what_changed": "Change of tag, not of value, at the prior year end. The 10-K 0001262039-26-000007 files current deferred revenue at 2024-12-31 under us-gaap:DeferredRevenueCurrent at 3276200000. The trend table's years-back-1 contract-liability input reads us-gaap:ContractWithCustomerLiabilityCurrent at 2024-12-31 from 0001262039-25-000039 (filed 2025-11-07), and that cell prints the value 3276200000.0. Same date, same printed value, different concept. The 10-K's fact is not the one the table reads.",
    "account": "current deferred revenue / current contract liabilities",
    "expected_direction": "none",
    "horizon": "the 2024-12-31 balance as filed in the 10-K (2026-02-25)",
    "quote": "\"value\": \"3276200000\"",
    "paragraph_id": "0001262039-26-000007:facts:DeferredRevenueCurrent:2024-12-31"
  },
  {
    "id": "structure_and_disclosure_changes_current_deferred_revenue_concept_prior_year_end_trend_input",
    "what_changed": "The years-back-1 contract_liabilities_over_revenue cell (2024-01-01..2024-12-31) takes its contract-liability input from 0001262039-25-000039, filed 2025-11-07: ContractWithCustomerLiabilityCurrent 3276200000.0 at 2024-12-31. For revenue it uses the 10-K 0001262039-26-000007. That 10-K files the 2024-12-31 balance as DeferredRevenueCurrent, so the cell draws its numerator and denominator from filings that use different concepts for the balance. The years-back-0 cell likewise reads ContractWithCustomerLiabilityCurrent, from this 10-Q, not from the 10-K. Within the table the concept does not change. The 10-K is the filing that departs from it.",
    "account": "current contract liabilities as read by the trend table",
    "expected_direction": "none",
    "horizon": "years-back-1 (2024-12-31) as read by the trend table",
    "quote": "\"id\": \"0001262039-25-000039:facts:ContractWithCustomerLiabilityCurrent:2024-12-31\"",
    "paragraph_id": "0001262039-26-000021:trends:contract_liabilities_over_revenue:2024-01-01..2024-12-31"
  },
  {
    "id": "across_documents_release_operating_cash_flow_absent_from_quarterly_record",
    "what_changed": "The release states a three-month operating cash flow that the trend record lacks. Its free-cash-flow reconciliation (paragraph 0001262039-26-000018:8k_2_02:79) prints net cash provided by operating activities of 1,043.6 for the three months ended June 30, 2026 and 451.9 a year earlier, in millions. The trend table has no operating cash flow row for 2026-04-01..2026-06-30, so the quarterly accruals cell stays insufficient. I did not compute accruals from the release figure.",
    "account": "net cash provided by operating activities, three months",
    "expected_direction": "none",
    "horizon": "three months ended June 30, 2026",
    "quote": "•Operating cash flow of $1.04 billion",
    "paragraph_id": "0001262039-26-000018:8k_2_02:15"
  },
  {
    "id": "across_documents_release_revenue_growth_beside_revenue_scaled_ratios",
    "what_changed": "The release states revenue grew 26% year over year. Revenue is the denominator of three quarterly ratios that fell year over year: contract_liabilities_over_revenue, receivables_over_revenue and days_sales_outstanding. The numerators the trend cells print did not fall. ContractWithCustomerLiabilityCurrent is 3841800000.0 at 2026-06-30 against 3412500000.0 at 2025-06-30. AccountsReceivableNetCurrent is 1455600000.0 against 1215700000.0. The three falls come with larger balances, not smaller ones.",
    "account": "total revenue, as the denominator of the receivable and contract-liability ratios",
    "expected_direction": "up",
    "horizon": "year over year, as the release states",
    "quote": "•Revenue grew 26% year over year to $2.05 billion",
    "paragraph_id": "0001262039-26-000018:8k_2_02:8"
  },
  {
    "id": "across_documents_release_product_revenue_growth_beside_gross_margin",
    "what_changed": "The release states product revenue grew 52% year over year, and the quarterly gross_margin cell sits at the lowest of the 6 filled quarters. The release's income statement (paragraph 0001262039-26-000018:8k_2_02:68) prints, in millions:\n- product: revenue 773.0, cost of revenue 233.8;\n- service: revenue 1,274.9, cost of revenue 170.9.\nIts non-GAAP reconciliation prints GAAP gross margin of 80.2% against 80.7% a year earlier. A larger product share is one possible reading of the lower margin. No product-mix figure exists in my input, and I did not compute one.",
    "account": "product revenue and gross margin",
    "expected_direction": "up",
    "horizon": "year over year, as the release states",
    "quote": "•Product revenue grew 52% year over year to $773 million",
    "paragraph_id": "0001262039-26-000018:8k_2_02:9"
  },
  {
    "id": "across_documents_release_billings_growth_beside_contract_liabilities_ratio",
    "what_changed": "The release states billings grew 33% year over year. Billings is non-GAAP: revenue plus the change in deferred revenue. The release's billings reconciliation (paragraph 0001262039-26-000018:8k_2_02:81) prints a change in deferred revenue of 324.2 for the quarter against 149.2 a year earlier, in millions. Its balance sheet prints current deferred revenue of 3,841.8 and noncurrent deferred revenue of 3,833.9 at June 30, 2026. The quarterly contract_liabilities_over_revenue cell uses the current balance only and sits at the lowest of the 6 filled quarters. On the release's own figures, that low position is not a fall in deferred revenue.",
    "account": "billings and deferred revenue (contract liabilities)",
    "expected_direction": "up",
    "horizon": "year over year, as the release states",
    "quote": "•Billings grew 33% year over year to $2.37 billion1",
    "paragraph_id": "0001262039-26-000018:8k_2_02:10"
  }
]
```

## Seen in the notes

```json
[]
```

This section is empty because none of my input says which facts sat inside a note. Every fact in `input_numbers.json` prints the same fields: `id`, `paragraph_id`, `tag`, `prefix`, `namespace`, `context`, `context_ref`, `unit`, `decimals`, `value`, `number`, `nil`, `form`, `source_accession`, `filing_date`, and on some `superseded_by`. None of these says whether the element sat inside a note when it was extracted. That includes facts such as:
- the inventory reserve and the inventory write-downs;
- the allowance and the refund liability;
- the revenue disaggregation and geographic revenue;
- the fair-value tables;
- PP&E, intangibles and debt;
- stock compensation, the effective tax rate and the segment table;
- customer concentration.

The instructions bar me from judging which facts came from notes, so I placed no item here. The split this heading anticipates cannot be made from this run's input.
