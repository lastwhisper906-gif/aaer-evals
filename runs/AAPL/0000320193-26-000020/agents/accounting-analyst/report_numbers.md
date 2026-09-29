<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# AAPL 0000320193-26-000020: numbers reader

## What this reader had, and what it did not have

- **Inputs read in full:** `input_trends.json`, `input_numbers.json`, `input_8k.md` and `input_prior_predictions.md`. The prior-predictions file says: "None on record. This company has no earlier run under the given run root, so there are no flags, no management explanations and no outcomes to carry forward."
- **Nothing forbidden is in the directory.** There are no prices, abnormal returns, short interest, other companies' files, prior probabilities or outcome windows.
- **Missing quarters.** Two quarters the record does not reach have no cells at all: `quarters-back-3` (target end 2025-09-27) and `quarters-back-7` (target end 2024-09-28). The reason given for the first reads: "no quarter ending within 20 days of 2025-09-27 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py". The second gives the same reason with 2024-09-28.
  - No output of that fourth-quarter derivation is in the input, so no fiscal-fourth-quarter value exists for this reader.
  - Every "of the 6 filled quarters" position below is ranked without the two fiscal fourth quarters.
- **Absent sections.** The input holds no articulation-check section, no restatement-trace section and no tag-change record.
  - Every trend input in every period rests on the same concept for its role, so no change of tag appears anywhere in the trend table.
  - The only evidence of a re-reported period is the `superseded_by` field on facts. Nearly all superseded facts carry the same value in the later filing. One, `OtherAssetsNoncurrent` at 2025-09-27, carries a different value; it is reported below.
- **R&D capitalization block.** The `research_and_development_capitalized` block for `years-back-0` prints no `paragraph_id`, so no item can quote it. It holds:
  - `book_value_with_rnd_capitalized` 166211200000.0
  - `earnings_with_rnd_capitalized` 120919600000.0
  - `research_and_development_amortization` 25640400000.0
  - `research_and_development_asset` 92478200000.0
  - `capitalized_development_cost` and `capitalized_over_expense` both missing: "no row for capitalized_development_cost in 2024-09-29..2025-09-27: us-gaap:CapitalizedComputerSoftwareAdditions is in the record, but not for this period".
- **How `expected_direction` is used.** It is the direction the named account would be expected to move over the stated horizon if the reading holds. It is `none` wherever the input gives no basis for one.
- **Where the 8-K items sit.** Items quoting the 8-K earnings release (paragraph ids beginning `0000320193-26-000018:8k_2_02`) are placed under the first heading. This report has only two headings, and none of those items comes from a table inside a note.

## Seen in the statements

### Trend table, quarters-back-0 (quarter 2026-03-29..2026-06-27)

```json
{ "id": "earnings_quality_gross_margin_trend_quarterly",
  "what_changed": "Gross margin for the quarter is 0.500562069879452. Change against quarters-back-1 is 0.007856284874415254; against quarters-back-4 it is 0.035655013007615644. It sits at 'highest of the 6 filled quarters'. The 8-K release says the quarter's margin includes a favorable impact of approximately 2 percentage points from tariff refunds. The trend value does not remove that effect, and a margin without the refund does not exist in the input.",
  "account": "Gross margin: revenue (us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax 109417000000.0) less cost of sales (us-gaap:CostOfGoodsAndServicesSold 54647000000.0)",
  "expected_direction": "down",
  "horizon": "next quarter, if the tariff-refund benefit named in the release does not recur",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0000320193-26-000020:trends:gross_margin:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_trend_quarterly",
  "what_changed": "Days sales of inventory is 18.47076692224642. Change against quarters-back-1 is 7.585228918948722; against quarters-back-4 it is 7.755416550610027. It sits at 'highest of the 6 filled quarters'. Its inputs are InventoryNet 11092000000.0 and CostOfGoodsAndServicesSold 54647000000.0. The facts show where the inventory sits: raw materials and purchased parts are 7645000000 at 2026-06-27 against 2124000000 at 2025-09-27, and finished goods are 3447000000 against 3594000000. The input gives no reason for the build.",
  "account": "Inventories (us-gaap:InventoryNet) against cost of sales",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0000320193-26-000020:trends:days_sales_of_inventory:2026-03-29..2026-06-27" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_trend_quarterly",
  "what_changed": "Days sales outstanding is 26.113108566310537. Change against quarters-back-1 is 1.2817569329819989; against quarters-back-4 it is -0.5541996986092812. It sits at 'second highest of the 6 filled quarters'. Its inputs are AccountsReceivableNetCurrent 31398000000.0 and quarterly revenue 109417000000.0.",
  "account": "Accounts receivable, net (us-gaap:AccountsReceivableNetCurrent) against revenue",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"",
  "paragraph_id": "0000320193-26-000020:trends:days_sales_outstanding:2026-03-29..2026-06-27" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_trend_quarterly",
  "what_changed": "Receivables over revenue is 0.2869572369924235. Change against quarters-back-1 is 0.014085241021780215; against quarters-back-4 it is -0.006090106578123977. It sits at 'second highest of the 6 filled quarters'. Its inputs are the same receivables and revenue facts as the DSO cell.",
  "account": "Accounts receivable, net (us-gaap:AccountsReceivableNetCurrent) against revenue",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"",
  "paragraph_id": "0000320193-26-000020:trends:receivables_over_revenue:2026-03-29..2026-06-27" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_trend_quarterly",
  "what_changed": "Contract liabilities over revenue is 0.08717109772704425. Change against quarters-back-1 is 0.003247151835549064; against quarters-back-4 it is -0.008313610257132023. It sits at 'third highest of the 6 filled quarters'. Its inputs are ContractWithCustomerLiabilityCurrent 9538000000.0 and revenue 109417000000.0.",
  "account": "Deferred revenue, current (us-gaap:ContractWithCustomerLiabilityCurrent) against revenue",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"position_in_history\": \"third highest of the 6 filled quarters\"",
  "paragraph_id": "0000320193-26-000020:trends:contract_liabilities_over_revenue:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_soft_asset_share_trend_quarterly",
  "what_changed": "Soft asset share is 0.7626322188767071. Change against quarters-back-1 is 0.020494362553845846; against quarters-back-4 it is 0.018373632774352555. It sits at 'third highest of the 6 filled quarters'. Its inputs are Assets 383266000000.0, CashAndCashEquivalentsAtCarryingValue 39544000000.0 and PropertyPlantAndEquipmentNet 51431000000.0.",
  "account": "Total assets less PP&E and cash, over total assets",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"position_in_history\": \"third highest of the 6 filled quarters\"",
  "paragraph_id": "0000320193-26-000020:trends:soft_asset_share:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_trend_quarterly",
  "what_changed": "insufficient. The cell is not filled for this quarter, and both its quarter-over-quarter and year-over-year changes say 'accruals_over_total_assets is not filled in quarters-back-0'. Across the whole quarterly window the ratio is filled in only 2 quarters (quarters-back-2 and quarters-back-6), which does not support a trend claim. The filing states operating cash flow only as a nine-month duration. A three-month figure does not exist in the input, and this reader does not derive one.",
  "account": "Accruals: net income less operating cash flow, over total assets",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-03-29..2026-06-27: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0000320193-26-000020:trends:accruals_over_total_assets:2026-03-29..2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_trend_quarterly",
  "what_changed": "insufficient. The ratio is filled in none of the 11 periods on record, so no value, change or position exists.",
  "account": "Allowance for credit losses on receivables against receivables",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"missing\": \"no row for bad_debt_allowance in 2026-06-27: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"",
  "paragraph_id": "0000320193-26-000020:trends:bad_debt_reserve_ratio:2026-03-29..2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_trend_quarterly",
  "what_changed": "insufficient. The companyfacts record tags no inventory valuation reserve in any period. The cell says the filing, not this record, would show whether the concept is untagged or stated only by segment.",
  "account": "Inventory valuation reserve (us-gaap:InventoryValuationReserves) against inventory",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0000320193-26-000020:trends:inventory_reserve_ratio:2026-03-29..2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_trend_quarterly",
  "what_changed": "insufficient. There is no warranty accrual for this quarter-end. Across the whole record the ratio is filled only in years-back-4 ('the only filled year'), which does not support a trend claim.",
  "account": "Product warranty accrual against revenue",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"missing\": \"no row for warranty_accrual in 2026-06-27: us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent is in the record, but not for this period\"",
  "paragraph_id": "0000320193-26-000020:trends:warranty_reserve_ratio:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_trend_quarterly",
  "what_changed": "insufficient. No non-GAAP net income exists in the record. The 8-K release in the input prints no non-GAAP reconciliation table either; it names tariff-refund effects on gross margin and diluted EPS, which are items below.",
  "account": "Non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0000320193-26-000020:trends:non_gaap_gap:2026-03-29..2026-06-27" }
```

### Trend table, years-back-0 (fiscal year 2024-09-29..2025-09-27)

Annual cells carry no quarter-over-quarter change ('an annual period has no preceding quarter'). The year-over-year change is against years-back-1.

```json
{ "id": "earnings_quality_accruals_over_total_assets_trend_annual",
  "what_changed": "Accruals over total assets is 0.0014697654220982572. Change against years-back-1 is 0.06864604905407809. It sits at 'highest of the 5 filled years'. Its inputs are NetIncomeLoss 112010000000.0, NetCashProvidedByUsedInOperatingActivities 111482000000.0 and Assets 359241000000.0. It is the only positive value among the five filled years: the others print as -0.06717628363197983, -0.03842499496572438, -0.06335275190996584 and -0.02666081674748292.",
  "account": "Accruals: net income less operating cash flow, over total assets",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000320193-26-000020:trends:accruals_over_total_assets:2024-09-29..2025-09-27" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_trend_annual",
  "what_changed": "Contract liabilities over revenue is 0.02175840600152345. Change against years-back-1 is 0.0006631076266976656. It sits at 'highest of the 5 filled years'. Its inputs are ContractWithCustomerLiabilityCurrent 9055000000.0 and annual revenue 416161000000.0.",
  "account": "Deferred revenue, current (us-gaap:ContractWithCustomerLiabilityCurrent) against revenue",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000320193-26-000020:trends:contract_liabilities_over_revenue:2024-09-29..2025-09-27" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_trend_annual",
  "what_changed": "Days sales of inventory is 9.419587255611875. Change against years-back-1 is -3.1883461132175164. It sits at 'second lowest of the 5 filled years'. Its inputs are InventoryNet 5718000000.0 and annual cost of sales 220960000000.0. The latest quarter (item above) is at the top of its own quarterly history.",
  "account": "Inventories (us-gaap:InventoryNet) against cost of sales",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0000320193-26-000020:trends:days_sales_of_inventory:2024-09-29..2025-09-27" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_trend_annual",
  "what_changed": "Days sales outstanding is 34.79141005524304. Change against years-back-1 is 3.6912783534772124. It sits at 'highest of the 5 filled years'. Its inputs are AccountsReceivableNetCurrent 39777000000.0 and annual revenue 416161000000.0.",
  "account": "Accounts receivable, net (us-gaap:AccountsReceivableNetCurrent) against revenue",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000320193-26-000020:trends:days_sales_outstanding:2024-09-29..2025-09-27" }
```

```json
{ "id": "earnings_quality_gross_margin_trend_annual",
  "what_changed": "Gross margin is 0.4690516410716045. Change against years-back-1 is 0.0069881429192651945. It sits at 'highest of the 5 filled years'. Its inputs are annual revenue 416161000000.0 and cost of sales 220960000000.0.",
  "account": "Gross margin",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000320193-26-000020:trends:gross_margin:2024-09-29..2025-09-27" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_trend_annual",
  "what_changed": "Receivables over revenue is 0.09558079685506331. Change against years-back-1 is 0.010140874597464877. It sits at 'highest of the 5 filled years'.",
  "account": "Accounts receivable, net against revenue",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000320193-26-000020:trends:receivables_over_revenue:2024-09-29..2025-09-27" }
```

```json
{ "id": "earnings_quality_soft_asset_share_trend_annual",
  "what_changed": "Soft asset share is 0.7612521956012815. Change against years-back-1 is -0.03155014973270931. It sits at 'lowest of the 5 filled years'. Its inputs are Assets 359241000000.0, cash 35934000000.0 and PP&E 49834000000.0.",
  "account": "Total assets less PP&E and cash, over total assets",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0000320193-26-000020:trends:soft_asset_share:2024-09-29..2025-09-27" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_trend_annual",
  "what_changed": "insufficient. There is no allowance for the fiscal year-end, and the ratio is filled in none of the 5 years.",
  "account": "Allowance for credit losses on receivables against receivables",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"missing\": \"no row for bad_debt_allowance in 2025-09-27: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"",
  "paragraph_id": "0000320193-26-000020:trends:bad_debt_reserve_ratio:2024-09-29..2025-09-27" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_trend_annual",
  "what_changed": "insufficient. The companyfacts record tags no inventory valuation reserve in any year.",
  "account": "Inventory valuation reserve against inventory",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0000320193-26-000020:trends:inventory_reserve_ratio:2024-09-29..2025-09-27" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_trend_annual",
  "what_changed": "insufficient. No non-GAAP net income exists in the record for any year.",
  "account": "Non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0000320193-26-000020:trends:non_gaap_gap:2024-09-29..2025-09-27" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_trend_annual",
  "what_changed": "insufficient. There is no warranty accrual at the fiscal year-end. The only filled year is years-back-4, whose value is 0.009195854757980083 and whose position is 'the only filled year'. One point does not support a trend claim.",
  "account": "Product warranty accrual against revenue",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"missing\": \"no row for warranty_accrual in 2025-09-27: us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent is in the record, but not for this period\"",
  "paragraph_id": "0000320193-26-000020:trends:warranty_reserve_ratio:2024-09-29..2025-09-27" }
```

### Restated prior value and presentation change (superseded facts)

```json
{ "id": "articulation_and_the_filed_history_other_non_current_assets_restated_prior_value",
  "what_changed": "The 10-K (0000320193-25-000079) reported other non-current assets at 2025-09-27 of 83727000000. That fact carries superseded_by 0000320193-26-000020, and the current 10-Q reports 72634000000 for the same tag and date. Several other lines are identical in both filings for that date: AssetsNoncurrent 211284000000, Assets 359241000000, PropertyPlantAndEquipmentNet 49834000000 and MarketableSecuritiesNoncurrent 77723000000. It is the only superseded 2025-09-27 balance-sheet fact in the input whose value differs in the later filing. The prior-quarter 10-Q (0000320193-26-000013) already carried 72634000000 for this date. The input holds no restatement trace explaining the change.",
  "account": "Other non-current assets (us-gaap:OtherAssetsNoncurrent)",
  "expected_direction": "none",
  "horizon": "next annual filing, where the comparative column will show which presentation is kept",
  "quote": "\"value\": \"83727000000\"",
  "paragraph_id": "0000320193-25-000079:facts:OtherAssetsNoncurrent:2025-09-27" }
```

```json
{ "id": "structure_and_disclosure_changes_intangible_assets_new_balance_sheet_line",
  "what_changed": "The current-period balance sheet in the 8-K release prints 'Intangible assets, net' as a separate non-current line: 20,342 at June 27, 2026 and 11,093 at September 27, 2025, in millions. In the 10-K facts in the input, the non-current asset lines run from PropertyPlantAndEquipmentNet (f-175 and f-176) straight to OtherAssetsNoncurrent (f-177 and f-178), with no intangible line. The same-date other non-current assets figure is the one re-reported in the item above. No fact in the current 10-Q's facts carries 20342000000 or 11093000000. Its balance-sheet facts skip from f-181 (PropertyPlantAndEquipmentNet) to f-184 (OtherAssetsNoncurrent).",
  "account": "Intangible assets, net (balance-sheet line)",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "| Intangible assets, net | 20,342 |  |  | 11,093 |  |",
  "paragraph_id": "0000320193-26-000018:8k_2_02:33" }
```

### Across documents: the release against the tagged 10-Q

Every other line of the 8-K's statements of operations, balance sheet and cash flows matches the corresponding 10-Q fact value, once the XBRL sign conventions for cash-flow change lines are taken into account. The one mismatch is intangible assets.

```json
{ "id": "across_documents_intangible_assets_tagged_net_value_quarter_end",
  "what_changed": "The 10-Q tags IntangibleAssetsNetExcludingGoodwill at 2026-06-27 as 25417000000. The 8-K balance-sheet line 'Intangible assets, net' for June 27, 2026 is 20,342 (millions). The two printed figures are not the same, and the input does not say whether they measure the same thing. The related tagged figures at 2026-06-27 are IntangibleAssetsGrossExcludingGoodwill 38220000000 and FiniteLivedIntangibleAssetsAccumulatedAmortization 12803000000. At 2025-09-27 they are 24950000000 and 11649000000.",
  "account": "Intangible assets, net excluding goodwill (us-gaap:IntangibleAssetsNetExcludingGoodwill)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"25417000000\"",
  "paragraph_id": "0000320193-26-000020:facts:IntangibleAssetsNetExcludingGoodwill:2026-06-27" }
```

```json
{ "id": "across_documents_intangible_assets_tagged_net_value_prior_year_end",
  "what_changed": "The 10-Q tags IntangibleAssetsNetExcludingGoodwill at 2025-09-27 as 13301000000; the prior-quarter 10-Q carried the same value. The 8-K balance-sheet line 'Intangible assets, net' for September 27, 2025 is 11,093 (millions). The two printed figures for the same date are not the same, and the input gives no reason.",
  "account": "Intangible assets, net excluding goodwill (us-gaap:IntangibleAssetsNetExcludingGoodwill)",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "\"value\": \"13301000000\"",
  "paragraph_id": "0000320193-26-000020:facts:IntangibleAssetsNetExcludingGoodwill:2025-09-27" }
```

### Earnings quality: what the release attributes to tariff refunds

```json
{ "id": "earnings_quality_tariff_refund_in_gross_margin",
  "what_changed": "The release states that the quarter's 50.1 percent gross margin includes about 2 percentage points from tariff refunds. The trend table's gross margin for the quarter is 0.500562069879452, at 'highest of the 6 filled quarters'. No tagged fact in the input isolates the refund amount.",
  "account": "Cost of sales / gross margin (tariff refunds)",
  "expected_direction": "down",
  "horizon": "next quarter, if the refund does not recur",
  "quote": "Company gross margin was 50.1 percent, including a favorable impact of approximately 2 percentage points from tariff refunds.",
  "paragraph_id": "0000320193-26-000018:8k_2_02:7" }
```

```json
{ "id": "earnings_quality_tariff_refund_in_diluted_eps",
  "what_changed": "The release states that quarterly diluted EPS of $2.02 includes $0.11 from tariff refunds. The tagged EarningsPerShareDiluted is 2.02 for the quarter against 1.57 a year earlier. An EPS figure excluding the refund does not exist in the input.",
  "account": "Diluted earnings per share",
  "expected_direction": "down",
  "horizon": "next quarter, if the refund does not recur",
  "quote": "Diluted earnings per share was $2.02, up 29 percent year over year, and included a favorable impact of $0.11 from tariff refunds.",
  "paragraph_id": "0000320193-26-000018:8k_2_02:7" }
```

### Numeric facts, current 10-Q (0000320193-26-000020)

#### Working capital and cash flow

```json
{ "id": "earnings_quality_raw_materials_inventory_build",
  "what_changed": "Raw materials and purchased parts, net of reserves, are 7645000000 at 2026-06-27 against 2124000000 at 2025-09-27. Finished goods, net of reserves, are 3447000000 against 3594000000. InventoryNet is 11092000000 against 5718000000. The rise sits in components, not finished goods. The input says nothing about why.",
  "account": "Inventory: raw materials and purchased parts (us-gaap:InventoryRawMaterialsAndPurchasedPartsNetOfReserves)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"7645000000\"",
  "paragraph_id": "0000320193-26-000020:facts:InventoryRawMaterialsAndPurchasedPartsNetOfReserves:2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_inventory_cash_outflow",
  "what_changed": "IncreaseDecreaseInInventories for 2025-09-28..2026-06-27 is 5461000000, an increase that the 8-K cash-flow statement shows as (5,461). For 2024-09-29..2025-06-28 it was -1223000000, shown there as 1,223.",
  "account": "Change in inventories (us-gaap:IncreaseDecreaseInInventories)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"5461000000\"",
  "paragraph_id": "0000320193-26-000020:facts:IncreaseDecreaseInInventories:2025-09-28..2026-06-27" }
```

```json
{ "id": "earnings_quality_other_operating_assets_build",
  "what_changed": "IncreaseDecreaseInOtherOperatingAssets for 2025-09-28..2026-06-27 is 16266000000, against 6116000000 for 2024-09-29..2025-06-28. In the 8-K this is 'Other current and non-current assets' at (16,266) against (6,116). Other current assets on the balance sheet are 17420000000 at 2026-06-27 against 14585000000; other non-current assets are 77557000000 against 72634000000.",
  "account": "Other current and non-current operating assets (us-gaap:IncreaseDecreaseInOtherOperatingAssets)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"16266000000\"",
  "paragraph_id": "0000320193-26-000020:facts:IncreaseDecreaseInOtherOperatingAssets:2025-09-28..2026-06-27" }
```

```json
{ "id": "earnings_quality_other_operating_liabilities_swing",
  "what_changed": "IncreaseDecreaseInOtherOperatingLiabilities for 2025-09-28..2026-06-27 is 10016000000, against -15161000000 for 2024-09-29..2025-06-28. The sign runs the other way from the prior-year period. The input does not name what drove it.",
  "account": "Other current and non-current operating liabilities (us-gaap:IncreaseDecreaseInOtherOperatingLiabilities)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"10016000000\"",
  "paragraph_id": "0000320193-26-000020:facts:IncreaseDecreaseInOtherOperatingLiabilities:2025-09-28..2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_other_non_current_liabilities_rise",
  "what_changed": "OtherLiabilitiesNoncurrent is 55080000000 at 2026-06-27 against 41549000000 at 2025-09-27; the 2025-09-27 value is identical in the 10-K. OtherLiabilitiesCurrent is 62259000000 against 66387000000. The input does not break the non-current line down.",
  "account": "Other non-current liabilities (us-gaap:OtherLiabilitiesNoncurrent)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"55080000000\"",
  "paragraph_id": "0000320193-26-000020:facts:OtherLiabilitiesNoncurrent:2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_operating_cash_flow_cumulative",
  "what_changed": "Operating cash flow for 2025-09-28..2026-06-27 is 116996000000, against 81754000000 for 2024-09-29..2025-06-28. Net income for the same durations is 101464000000 against 84544000000. The filing states operating cash flow only for the nine-month durations. That is why the quarterly accruals cell is empty; a three-month operating cash flow does not exist in the input.",
  "account": "Net cash provided by operating activities (us-gaap:NetCashProvidedByUsedInOperatingActivities)",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "\"value\": \"116996000000\"",
  "paragraph_id": "0000320193-26-000020:facts:NetCashProvidedByUsedInOperatingActivities:2025-09-28..2026-06-27" }
```

#### Income statement

```json
{ "id": "earnings_quality_cash_taxes_paid_against_provision",
  "what_changed": "IncomeTaxesPaidNet for 2025-09-28..2026-06-27 is 26555000000, against 37332000000 for 2024-09-29..2025-06-28. IncomeTaxExpenseBenefit for the same durations is 21638000000 against 15381000000. For the quarter, the provision is 6478000000 against 4597000000, on pre-tax income of 36267000000 against 28031000000. No effective-rate figure is printed in the input, and this reader does not derive one.",
  "account": "Income taxes paid (us-gaap:IncomeTaxesPaidNet) and provision (us-gaap:IncomeTaxExpenseBenefit)",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "\"value\": \"26555000000\"",
  "paragraph_id": "0000320193-26-000020:facts:IncomeTaxesPaidNet:2025-09-28..2026-06-27" }
```

```json
{ "id": "earnings_quality_other_income_swing",
  "what_changed": "Non-operating income for the quarter is 572000000, against -171000000 in the prior-year quarter. For the nine-month durations it is 670000000 against -698000000. The input does not break the line down.",
  "account": "Other income/(expense), net (us-gaap:NonoperatingIncomeExpense)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"572000000\"",
  "paragraph_id": "0000320193-26-000020:facts:NonoperatingIncomeExpense:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_research_and_development_step_up",
  "what_changed": "R&D expense for the quarter is 11729000000, against 8866000000 in the prior-year quarter. For the nine-month durations it is 34035000000 against 25684000000. SG&A for the quarter is 7346000000 against 6650000000.",
  "account": "Research and development expense (us-gaap:ResearchAndDevelopmentExpense)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"11729000000\"",
  "paragraph_id": "0000320193-26-000020:facts:ResearchAndDevelopmentExpense:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_corporate_unallocated_operating_loss",
  "what_changed": "The corporate non-segment operating loss for the quarter is -14041000000, against -10747000000 in the prior-year quarter. For the nine-month durations it is -40718000000 against -31636000000.",
  "account": "Operating income, corporate non-segment (us-gaap:OperatingIncomeLoss, CorporateNonSegmentMember)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"-14041000000\"",
  "paragraph_id": "0000320193-26-000020:facts:OperatingIncomeLoss:2026-03-29..2026-06-27:srt:ConsolidationItemsAxis=us-gaap:CorporateNonSegmentMember" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_ipad_revenue_decline",
  "what_changed": "iPad revenue for the quarter is 6191000000, against 6581000000 in the prior-year quarter; it is the only product category whose quarterly revenue is lower. The other categories: iPhone 54252000000 against 44582000000, Mac 10352000000 against 8046000000, Wearables, Home and Accessories 7883000000 against 7404000000, and Services 30739000000 against 27423000000. Every geographic segment's quarterly revenue is higher than a year earlier.",
  "account": "Net sales, iPad (us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax, IPadMember)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"6191000000\"",
  "paragraph_id": "0000320193-26-000020:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-03-29..2026-06-27:srt:ProductOrServiceAxis=aapl:IPadMember" }
```

#### Revenue recognition detail

```json
{ "id": "revenue_recognition_total_contract_liabilities",
  "what_changed": "Total contract liabilities are 14900000000 at 2026-06-27 against 13700000000 at 2025-09-27 (decimals -8). Revenue recognized in the quarter that was in contract liabilities at the start is 4086000000, against 4015000000 in the prior-year quarter. For the nine-month durations it is 7260000000 against 6958000000.",
  "account": "Contract liabilities, total (us-gaap:ContractWithCustomerLiability)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"14900000000\"",
  "paragraph_id": "0000320193-26-000020:facts:ContractWithCustomerLiability:2026-06-27" }
```

```json
{ "id": "revenue_recognition_remaining_performance_obligation_timing",
  "what_changed": "Of remaining performance obligations at 2026-06-27, the share expected from 2026-06-28 is 0.64, from 2027-06-27 is 0.23, from 2028-07-02 is 0.11 and from 2029-07-01 is 0.02. The input holds only one date for this schedule, so no change can be stated: insufficient for a trend.",
  "account": "Remaining performance obligation, expected timing (us-gaap:RevenueRemainingPerformanceObligationPercentage)",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"value\": \"0.64\"",
  "paragraph_id": "0000320193-26-000020:facts:RevenueRemainingPerformanceObligationPercentage:2026-06-27:us-gaap:RevenueRemainingPerformanceObligationExpectedTimingOfSatisfactionStartDateAxis=2026-06-28" }
```

```json
{ "id": "revenue_recognition_single_customer_receivable_concentration",
  "what_changed": "The single customer tagged CustomerOneMember holds 0.18 of trade receivables for 2025-09-28..2026-06-27, against 0.12 for 2024-09-29..2025-09-27. Cellular network carriers as a group hold 0.27, against 0.34.",
  "account": "Trade accounts receivable concentration (us-gaap:ConcentrationRiskPercentage1)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"0.18\"",
  "paragraph_id": "0000320193-26-000020:facts:ConcentrationRiskPercentage1:2025-09-28..2026-06-27:srt:MajorCustomersAxis=aapl:CustomerOneMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:TradeAccountsReceivableMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CreditConcentrationRiskMember" }
```

```json
{ "id": "liquidity_and_capital_vendor_non_trade_receivable_concentration",
  "what_changed": "The vendor tagged VendorOneMember holds 0.47 of vendor non-trade receivables for 2025-09-28..2026-06-27, against 0.46 for the fiscal year to 2025-09-27. VendorTwoMember holds 0.22 against 0.23. Vendor non-trade receivables are 27509000000 at 2026-06-27 against 33180000000 at 2025-09-27.",
  "account": "Vendor non-trade receivables concentration (us-gaap:ConcentrationRiskPercentage1, NonTradeReceivableMember)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"0.47\"",
  "paragraph_id": "0000320193-26-000020:facts:ConcentrationRiskPercentage1:2025-09-28..2026-06-27:srt:MajorCustomersAxis=aapl:VendorOneMember,us-gaap:ConcentrationRiskByBenchmarkAxis=aapl:NonTradeReceivableMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CreditConcentrationRiskMember" }
```

#### Debt, capital returns and investments

```json
{ "id": "liquidity_and_capital_commercial_paper_and_term_debt_paydown",
  "what_changed": "Commercial paper is 1997000000 at 2026-06-27, against 7979000000 at 2025-09-27. Total term debt (LongTermDebt, decimals -8) is 82300000000 against 90700000000. The 10-K fact for 2025-09-27, as read, prints 90678000000 at decimals -6; that is a difference of rounding precision, and no trace flags it as a restatement. No term debt was issued in 2025-09-28..2026-06-27 (ProceedsFromIssuanceOfLongTermDebt 0). Repayments of term debt were 8146000000, and commercial paper net was -5911000000.",
  "account": "Commercial paper (us-gaap:CommercialPaper) and term debt (us-gaap:LongTermDebt)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"1997000000\"",
  "paragraph_id": "0000320193-26-000020:facts:CommercialPaper:2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_share_repurchases",
  "what_changed": "Repurchases of common stock for 2025-09-28..2026-06-27 are 62094000000, against 70579000000 for 2024-09-29..2025-06-28. Shares repurchased and retired in the period are 215000000. Common shares outstanding are 14608963000 at 2026-06-27 against 14773260000 at 2025-09-27.",
  "account": "Payments for repurchase of common stock (us-gaap:PaymentsForRepurchaseOfCommonStock)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"62094000000\"",
  "paragraph_id": "0000320193-26-000020:facts:PaymentsForRepurchaseOfCommonStock:2025-09-28..2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_marketable_securities_purchases",
  "what_changed": "Purchases of available-for-sale debt securities for 2025-09-28..2026-06-27 are 48752000000, against 17591000000 for 2024-09-29..2025-06-28. Proceeds from maturities are 26504000000 against 35036000000; proceeds from sales are 12016000000 against 10785000000. Non-current marketable securities are 84118000000 at 2026-06-27 against 77723000000.",
  "account": "Purchases of marketable securities (us-gaap:PaymentsToAcquireAvailableForSaleSecuritiesDebt)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"48752000000\"",
  "paragraph_id": "0000320193-26-000020:facts:PaymentsToAcquireAvailableForSaleSecuritiesDebt:2025-09-28..2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_unrealized_losses_on_debt_securities",
  "what_changed": "Gross unrealized losses on Level 2 available-for-sale debt securities are 2603000000 at 2026-06-27, against 3025000000 at 2025-09-27. Gross unrealized gains are 268000000 against 559000000.",
  "account": "Available-for-sale debt securities, gross unrealized loss (us-gaap:AvailableForSaleDebtSecuritiesAccumulatedGrossUnrealizedLossBeforeTax)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"2603000000\"",
  "paragraph_id": "0000320193-26-000020:facts:AvailableForSaleDebtSecuritiesAccumulatedGrossUnrealizedLossBeforeTax:2026-06-27:us-gaap:FairValueByFairValueHierarchyLevelAxis=us-gaap:FairValueInputsLevel2Member" }
```

```json
{ "id": "liquidity_and_capital_undesignated_currency_hedge_notional",
  "what_changed": "The notional amount of foreign-exchange contracts not designated as hedges is 64053000000 at 2026-06-27, against 109079000000 at 2025-09-27. Designated foreign-exchange notional is 61313000000 against 62647000000; designated interest-rate notional is 10625000000 against 12875000000.",
  "account": "Derivative notional amount, foreign exchange, not designated (us-gaap:DerivativeNotionalAmount)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"64053000000\"",
  "paragraph_id": "0000320193-26-000020:facts:DerivativeNotionalAmount:2026-06-27:us-gaap:DerivativeInstrumentRiskAxis=us-gaap:ForeignExchangeContractMember,us-gaap:HedgingDesignationAxis=us-gaap:NondesignatedMember" }
```

```json
{ "id": "liquidity_and_capital_dividend_per_share",
  "what_changed": "The dividend declared per share for the quarter is 0.27, against 0.26 in the prior-year quarter. For the nine-month durations it is 0.79 against 0.76. The release declares a further $0.27.",
  "account": "Dividends declared per share (us-gaap:CommonStockDividendsPerShareDeclared)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"0.27\"",
  "paragraph_id": "0000320193-26-000020:facts:CommonStockDividendsPerShareDeclared:2026-03-29..2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_retained_earnings_turned_positive",
  "what_changed": "Retained earnings are 11326000000 at 2026-06-27, against -14264000000 at 2025-09-27. Total shareholders' equity is 107520000000 against 73733000000.",
  "account": "Retained earnings/(accumulated deficit) (us-gaap:RetainedEarningsAccumulatedDeficit)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"11326000000\"",
  "paragraph_id": "0000320193-26-000020:facts:RetainedEarningsAccumulatedDeficit:2026-06-27" }
```

#### Commitments and share-based compensation

```json
{ "id": "related_parties_contingencies_and_subsequent_events_unconditional_purchase_obligations",
  "what_changed": "Unrecorded unconditional purchase obligations are 27628000000 at 2026-06-27. The schedule is 2053000000 for the remainder of the fiscal year, then 7652000000, 6406000000, 5421000000 and 5481000000 in the following four years. The input holds this schedule for one date only: insufficient for a trend.",
  "account": "Unrecorded unconditional purchase obligations (us-gaap:UnrecordedUnconditionalPurchaseObligationBalanceSheetAmount)",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"value\": \"27628000000\"",
  "paragraph_id": "0000320193-26-000020:facts:UnrecordedUnconditionalPurchaseObligationBalanceSheetAmount:2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_unrecognized_share_based_compensation",
  "what_changed": "Unrecognized RSU compensation cost is 26700000000 at 2026-06-27; the input holds this for one date only. Nonvested RSUs are 143962000 at a weighted grant-date fair value of 225.06, against 151574000 at 189.75 at 2025-09-27. Grants in the period are 72400000 at 258.16. Share-based compensation expense for the quarter is 3401000000, against 3168000000 in the prior-year quarter.",
  "account": "Unrecognized share-based compensation cost (us-gaap:EmployeeServiceShareBasedCompensationNonvestedAwardsTotalCompensationCostNotYetRecognized)",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"value\": \"26700000000\"",
  "paragraph_id": "0000320193-26-000020:facts:EmployeeServiceShareBasedCompensationNonvestedAwardsTotalCompensationCostNotYetRecognized:2026-06-27:us-gaap:AwardTypeAxis=us-gaap:RestrictedStockUnitsRSUMember" }
```

## Seen in the notes

No items. The instructions say each fact is marked with whether its element sat inside a note, but no fact in `input_numbers.json` carries such a marker. The only fields present on any fact are `id`, `paragraph_id`, `tag`, `prefix`, `namespace`, `context`, `context_ref`, `unit`, `decimals`, `value`, `number`, `nil`, `form`, `source_accession`, `filing_date` and, on some facts, `superseded_by`.

This reader does not judge on its own which tables sat inside a note, so nothing is placed under this heading. Some fact items under the first heading (inventory components, intangible assets, remaining performance obligations, concentrations, debt, purchase obligations, share-based compensation, fair-value and derivative figures) may come from note tables. The input cannot say which, and that split has to be made where the marker exists.
