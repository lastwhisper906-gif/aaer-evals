<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# AAPL — numbers report, 10-Q 0000320193-26-000020 (quarter ended 2026-06-27)

## What my input holds, and what it does not

- **Files.** I read `input_trends.json`, `input_8k.md` and `input_prior_predictions.md` in full. `input_numbers.json` has 56,980 lines, and I read lines 1–4198, 8000–8119, 20000–20119, 24100–24999, 26600–26659, 32000–32119, 38200–50619, 51900–53199 and 56500–56980. The rest I did not read: most of the 10-K's note facts, most of the prior 10-Q's, and parts of this 10-Q's later notes. Anything those lines hold is not reflected here.
- **Nothing that should not be here.** None of what I read holds prices, returns, short interest, another company's files, a prior run's probability or an outcome window. One fact is the 10-K cover-page figure `dei:EntityPublicFloat`. It is a filed amount, not a price series, and I did not use it.
- **Prior flags:** `input_prior_predictions.md` says "None on record." There is nothing to carry forward.
- **Articulation checks, restatement traces and the fourth-quarter derivation are not in my directory.** `input_numbers.json` has four top-level keys and no others: `ticker`, `cutoff`, `documents` (the 10-K 0000320193-25-000079, the prior 10-Q 0000320193-26-000013 and this 10-Q 0000320193-26-000020) and `facts`. So no articulation gap and no change of tag is printed anywhere I can quote, and I derive none. Treat this as **insufficient**, not as clean.
- **Restated prior values.** No restatement trace exists in my input. Some earlier-filed facts carry a `superseded_by` field naming 0000320193-26-000020. It says a later filing reported the same element and context, not whether the value changed. I read the 10-K's and the prior 10-Q's primary balance-sheet facts at 2025-09-27 against this 10-Q's facts for the same element and date. One pair differs: `OtherAssetsNoncurrent` (`articulation_and_the_filed_history_other_non_current_assets_restated`). That pair was read off two printed values, not computed. I did not compare superseded facts in the lines I did not read, so other restated values may exist.
- **Periods the record does not reach.** Two of the 8 requested quarters have no cells: quarters-back-3 (target 2025-09-27) and quarters-back-7 (target 2024-09-28). The reason each gives: "no quarter ending within 20 days of 2025-09-27 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py". The quarters-back-7 reason is the same with 2024-09-28. The derived fourth quarters are not in my input. That is why every quarterly position below is out of 6 filled quarters, not 8. All 5 requested years are filled.
- **Formula baseline with R&D capitalized** (years-back-0, 5-year life) prints no `paragraph_id`, so I cannot itemize it. As printed: `earnings_with_rnd_capitalized` 120919600000.0 against `net_income` 112010000000.0; `book_value_with_rnd_capitalized` 166211200000.0 against `stockholders_equity` 73733000000.0; `research_and_development_asset` 92478200000.0; `research_and_development_amortization` 25640400000.0. `capitalized_development_cost` and `capitalized_over_expense` are missing: "no row for capitalized_development_cost in 2024-09-29..2025-09-27: us-gaap:CapitalizedComputerSoftwareAdditions is in the record, but not for this period".
- **Conventions in the items.** `expected_direction` is the direction of the change Python printed for the account over the stated `horizon`, read from the sign, or read off two printed values for a fact pair. When the quarter-over-quarter and year-over-year changes have opposite signs it is `none`, and it is `none` wherever the cell is insufficient or the item is a mismatch, not a movement. It is not a forecast. Every number in the items is copied as printed. I computed none of them.

## Seen in the statements

```json
{ "id": "earnings_quality_gross_margin_against_quarterly_history",
  "what_changed": "Gross margin, (revenue - cost_of_revenue) / revenue, for the quarter 2026-03-29..2026-06-27 is printed as 0.500562069879452, on revenue 109417000000.0 and cost of revenue 54647000000.0 (both from 0000320193-26-000020). Printed change against quarters-back-1: 0.007856284874415254. Against quarters-back-4: 0.035655013007615644. Position: highest of the 6 filled quarters. A year earlier, quarters-back-4 (0.4649070568718363) sits at 'lowest of the 6 filled quarters'. The earnings release says the quarter's company gross margin includes a favorable impact of approximately 2 percentage points from tariff refunds (see earnings_quality_record_gross_margin_includes_tariff_refunds). My input prints no margin with the refunds removed.",
  "account": "gross margin: RevenueFromContractWithCustomerExcludingAssessedTax less CostOfGoodsAndServicesSold",
  "expected_direction": "up",
  "horizon": "quarter 2026-03-29..2026-06-27 against quarters-back-1 (2025-12-28..2026-03-28) and quarters-back-4 (2025-03-30..2025-06-28)",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0000320193-26-000020:trends:gross_margin:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_against_quarterly_history",
  "what_changed": "Days sales of inventory, inventory / cost_of_revenue * days_in_period (91 days), for the quarter 2026-03-29..2026-06-27 is printed as 18.47076692224642, on InventoryNet at 2026-06-27 of 11092000000.0 and cost of revenue 54647000000.0 (both from 0000320193-26-000020). Printed change against quarters-back-1 (10.885538003297697): 7.585228918948722. Against quarters-back-4 (10.715350371636392): 7.755416550610027. Position: highest of the 6 filled quarters. See earnings_quality_inventory_build_in_raw_materials_and_parts for the components.",
  "account": "inventory: InventoryNet against CostOfGoodsAndServicesSold",
  "expected_direction": "up",
  "horizon": "quarter 2026-03-29..2026-06-27 against quarters-back-1 (2025-12-28..2026-03-28) and quarters-back-4 (2025-03-30..2025-06-28)",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0000320193-26-000020:trends:days_sales_of_inventory:2026-03-29..2026-06-27" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_against_quarterly_history",
  "what_changed": "Days sales outstanding, receivables / revenue * days_in_period (91 days), for the quarter 2026-03-29..2026-06-27 is printed as 26.113108566310537, on AccountsReceivableNetCurrent at 2026-06-27 of 31398000000.0 and revenue 109417000000.0. Printed change against quarters-back-1: 1.2817569329819989. Against quarters-back-4: -0.5541996986092812. Position: second highest of the 6 filled quarters. The highest is quarters-back-4 (26.667308264919818). The two printed changes have opposite signs.",
  "account": "accounts receivable: AccountsReceivableNetCurrent against RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "none",
  "horizon": "quarter 2026-03-29..2026-06-27 against quarters-back-1 (2025-12-28..2026-03-28) and quarters-back-4 (2025-03-30..2025-06-28)",
  "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"",
  "paragraph_id": "0000320193-26-000020:trends:days_sales_outstanding:2026-03-29..2026-06-27" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_against_quarterly_history",
  "what_changed": "Receivables over revenue for the quarter 2026-03-29..2026-06-27 is printed as 0.2869572369924235, on receivables 31398000000.0 and revenue 109417000000.0. Printed change against quarters-back-1: 0.014085241021780215. Against quarters-back-4: -0.006090106578123977. Position: second highest of the 6 filled quarters. The highest is quarters-back-4 (0.29304734357054746). The two printed changes have opposite signs.",
  "account": "accounts receivable: AccountsReceivableNetCurrent against RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "none",
  "horizon": "quarter 2026-03-29..2026-06-27 against quarters-back-1 (2025-12-28..2026-03-28) and quarters-back-4 (2025-03-30..2025-06-28)",
  "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"",
  "paragraph_id": "0000320193-26-000020:trends:receivables_over_revenue:2026-03-29..2026-06-27" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_against_quarterly_history",
  "what_changed": "Contract liabilities over revenue for the quarter 2026-03-29..2026-06-27 is printed as 0.08717109772704425, on ContractWithCustomerLiabilityCurrent at 2026-06-27 of 9538000000.0 and revenue 109417000000.0. Printed change against quarters-back-1: 0.003247151835549064. Against quarters-back-4: -0.008313610257132023. Position: third highest of the 6 filled quarters. The highest is quarters-back-4 (0.09548470798417627). The two printed changes have opposite signs.",
  "account": "deferred revenue: ContractWithCustomerLiabilityCurrent against RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "none",
  "horizon": "quarter 2026-03-29..2026-06-27 against quarters-back-1 (2025-12-28..2026-03-28) and quarters-back-4 (2025-03-30..2025-06-28)",
  "quote": "\"position_in_history\": \"third highest of the 6 filled quarters\"",
  "paragraph_id": "0000320193-26-000020:trends:contract_liabilities_over_revenue:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_soft_asset_share_against_quarterly_history",
  "what_changed": "Soft asset share, (assets - property_plant_and_equipment - cash) / assets, at 2026-06-27 is printed as 0.7626322188767071, on Assets 383266000000.0, CashAndCashEquivalentsAtCarryingValue 39544000000.0 and PropertyPlantAndEquipmentNet 51431000000.0. Printed change against quarters-back-1: 0.020494362553845846. Against quarters-back-4: 0.018373632774352555. Position: third highest of the 6 filled quarters. Intangible assets rose over the same months (see estimates_and_discretion_intangible_assets_rise).",
  "account": "soft assets: Assets less PropertyPlantAndEquipmentNet and CashAndCashEquivalentsAtCarryingValue",
  "expected_direction": "up",
  "horizon": "balance at 2026-06-27 against quarters-back-1 (2026-03-28) and quarters-back-4 (2025-06-28)",
  "quote": "\"position_in_history\": \"third highest of the 6 filled quarters\"",
  "paragraph_id": "0000320193-26-000020:trends:soft_asset_share:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly_insufficient",
  "what_changed": "insufficient. Accruals over total assets, (net_income - operating_cash_flow) / assets, is not filled for the quarter 2026-03-29..2026-06-27: the record holds no operating cash flow for the three-month period. The metric is filled in only 2 of the 6 filled quarters, quarters-back-2 ('lowest of the 2 filled quarters', -0.031184006200945434) and quarters-back-6. Two quarters do not support a quarterly trend claim. The figure the formula needs does not exist in my input, and I do not derive it.",
  "account": "accruals: NetIncomeLoss less NetCashProvidedByUsedInOperatingActivities, over Assets",
  "expected_direction": "none",
  "horizon": "quarter 2026-03-29..2026-06-27",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-03-29..2026-06-27: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0000320193-26-000020:trends:accruals_over_total_assets:2026-03-29..2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly_insufficient",
  "what_changed": "insufficient. The bad debt reserve ratio is not filled for the quarter 2026-03-29..2026-06-27: no allowance for credit losses is in the record for 2026-06-27. The metric is filled in 0 of the periods in the table, quarterly or annual, so there is no history to place it in.",
  "account": "allowance for credit losses on accounts receivable",
  "expected_direction": "none",
  "horizon": "quarter 2026-03-29..2026-06-27",
  "quote": "\"missing\": \"no row for bad_debt_allowance in 2026-06-27: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"",
  "paragraph_id": "0000320193-26-000020:trends:bad_debt_reserve_ratio:2026-03-29..2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly_insufficient",
  "what_changed": "insufficient. The inventory reserve ratio is not filled for the quarter 2026-03-29..2026-06-27: the record tags no us-gaap:InventoryValuationReserves in any period. The metric is filled in 0 of the periods in the table. This is the same quarter in which days sales of inventory sits at 'highest of the 6 filled quarters'. The inventory components in my input are stated net of reserves, and no reserve figure is in my input to set against them.",
  "account": "inventory valuation reserve",
  "expected_direction": "none",
  "horizon": "quarter 2026-03-29..2026-06-27",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0000320193-26-000020:trends:inventory_reserve_ratio:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly_insufficient",
  "what_changed": "insufficient. The non-GAAP gap is not filled for the quarter 2026-03-29..2026-06-27: no us-gaap concept carries a non-GAAP measure. The metric is filled in 0 of the periods in the table. The earnings release figures in my input are GAAP statements and include no non-GAAP reconciliation.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "quarter 2026-03-29..2026-06-27",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0000320193-26-000020:trends:non_gaap_gap:2026-03-29..2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly_insufficient",
  "what_changed": "insufficient. The warranty reserve ratio is not filled for the quarter 2026-03-29..2026-06-27: the warranty accrual concepts are in the record, but not for 2026-06-27. The metric is not filled in any of the 6 filled quarters.",
  "account": "product warranty accrual",
  "expected_direction": "none",
  "horizon": "quarter 2026-03-29..2026-06-27",
  "quote": "\"missing\": \"no row for warranty_accrual in 2026-06-27: us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent is in the record, but not for this period\"",
  "paragraph_id": "0000320193-26-000020:trends:warranty_reserve_ratio:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_against_annual_history",
  "what_changed": "Accruals over total assets for the fiscal year 2024-09-29..2025-09-27 is printed as 0.0014697654220982572. Inputs: NetIncomeLoss 112010000000.0 and NetCashProvidedByUsedInOperatingActivities 111482000000.0 (both 0000320193-25-000079), and Assets at 2025-09-27 of 359241000000.0 (0000320193-26-000020). Printed change against years-back-1 (-0.06717628363197983, 'lowest of the 5 filled years'): 0.06864604905407809. Position: highest of the 5 filled years.",
  "account": "accruals: NetIncomeLoss less NetCashProvidedByUsedInOperatingActivities, over Assets",
  "expected_direction": "up",
  "horizon": "fiscal year 2024-09-29..2025-09-27 against years-back-1 (2023-10-01..2024-09-28)",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000320193-26-000020:trends:accruals_over_total_assets:2024-09-29..2025-09-27" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_against_annual_history",
  "what_changed": "Contract liabilities over revenue for the fiscal year 2024-09-29..2025-09-27 is printed as 0.02175840600152345, on ContractWithCustomerLiabilityCurrent at 2025-09-27 of 9055000000.0 (0000320193-26-000020) and revenue 416161000000.0 (0000320193-25-000079). Printed change against years-back-1: 0.0006631076266976656. Position: highest of the 5 filled years.",
  "account": "deferred revenue: ContractWithCustomerLiabilityCurrent against RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "up",
  "horizon": "fiscal year 2024-09-29..2025-09-27 against years-back-1 (2023-10-01..2024-09-28)",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000320193-26-000020:trends:contract_liabilities_over_revenue:2024-09-29..2025-09-27" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_against_annual_history",
  "what_changed": "Days sales of inventory for the fiscal year 2024-09-29..2025-09-27 (364 days) is printed as 9.419587255611875, on InventoryNet at 2025-09-27 of 5718000000.0 (0000320193-26-000020) and cost of revenue 220960000000.0 (0000320193-25-000079). Printed change against years-back-1 (12.607933368829391, 'highest of the 5 filled years'): -3.1883461132175164. Position: second lowest of the 5 filled years. The next fiscal year is not complete. In its third quarter the quarterly cell sits at 'highest of the 6 filled quarters'; see earnings_quality_days_sales_of_inventory_against_quarterly_history.",
  "account": "inventory: InventoryNet against CostOfGoodsAndServicesSold",
  "expected_direction": "down",
  "horizon": "fiscal year 2024-09-29..2025-09-27 against years-back-1 (2023-10-01..2024-09-28)",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0000320193-26-000020:trends:days_sales_of_inventory:2024-09-29..2025-09-27" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_against_annual_history",
  "what_changed": "Days sales outstanding for the fiscal year 2024-09-29..2025-09-27 (364 days) is printed as 34.79141005524304, on AccountsReceivableNetCurrent at 2025-09-27 of 39777000000.0 (0000320193-26-000020) and revenue 416161000000.0 (0000320193-25-000079). Printed change against years-back-1 (31.10013170176583): 3.6912783534772124. Position: highest of the 5 filled years. Annual and quarterly cells use different day counts, and I do not compare them.",
  "account": "accounts receivable: AccountsReceivableNetCurrent against RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "up",
  "horizon": "fiscal year 2024-09-29..2025-09-27 against years-back-1 (2023-10-01..2024-09-28)",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000320193-26-000020:trends:days_sales_outstanding:2024-09-29..2025-09-27" }
```

```json
{ "id": "earnings_quality_gross_margin_against_annual_history",
  "what_changed": "Gross margin for the fiscal year 2024-09-29..2025-09-27 is printed as 0.4690516410716045, on revenue 416161000000.0 and cost of revenue 220960000000.0 (both 0000320193-25-000079). Printed change against years-back-1 (0.4620634981523393): 0.0069881429192651945. Position: highest of the 5 filled years. Each year from years-back-4 to years-back-0 prints a positive year-over-year change where one is printed.",
  "account": "gross margin: RevenueFromContractWithCustomerExcludingAssessedTax less CostOfGoodsAndServicesSold",
  "expected_direction": "up",
  "horizon": "fiscal year 2024-09-29..2025-09-27 against years-back-1 (2023-10-01..2024-09-28)",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000320193-26-000020:trends:gross_margin:2024-09-29..2025-09-27" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_against_annual_history",
  "what_changed": "Receivables over revenue for the fiscal year 2024-09-29..2025-09-27 is printed as 0.09558079685506331, on receivables at 2025-09-27 of 39777000000.0 and revenue 416161000000.0. Printed change against years-back-1 (0.08543992225759843): 0.010140874597464877. Position: highest of the 5 filled years. The printed change is also positive for years-back-1 against years-back-2 and for years-back-2 against years-back-3.",
  "account": "accounts receivable: AccountsReceivableNetCurrent against RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "up",
  "horizon": "fiscal year 2024-09-29..2025-09-27 against years-back-1 (2023-10-01..2024-09-28)",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000320193-26-000020:trends:receivables_over_revenue:2024-09-29..2025-09-27" }
```

```json
{ "id": "earnings_quality_soft_asset_share_against_annual_history",
  "what_changed": "Soft asset share at 2025-09-27 is printed as 0.7612521956012815, on Assets 359241000000.0, cash 35934000000.0 and PropertyPlantAndEquipmentNet 49834000000.0 (all 0000320193-26-000020). Printed change against years-back-1 (0.7928023453339909): -0.03155014973270931. Position: lowest of the 5 filled years. These three inputs print the same at 2025-09-27 in the 10-K, so the restated other non-current assets line (articulation_and_the_filed_history_other_non_current_assets_restated) does not enter this ratio.",
  "account": "soft assets: Assets less PropertyPlantAndEquipmentNet and CashAndCashEquivalentsAtCarryingValue",
  "expected_direction": "down",
  "horizon": "balance at 2025-09-27 against years-back-1 (2024-09-28)",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0000320193-26-000020:trends:soft_asset_share:2024-09-29..2025-09-27" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual_insufficient",
  "what_changed": "insufficient. The bad debt reserve ratio is not filled for the fiscal year 2024-09-29..2025-09-27: no allowance for credit losses is in the record for 2025-09-27. It is not filled in any of the 5 years.",
  "account": "allowance for credit losses on accounts receivable",
  "expected_direction": "none",
  "horizon": "fiscal year 2024-09-29..2025-09-27",
  "quote": "\"missing\": \"no row for bad_debt_allowance in 2025-09-27: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"",
  "paragraph_id": "0000320193-26-000020:trends:bad_debt_reserve_ratio:2024-09-29..2025-09-27" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_annual_insufficient",
  "what_changed": "insufficient. The inventory reserve ratio is not filled for the fiscal year 2024-09-29..2025-09-27: the record tags no us-gaap:InventoryValuationReserves in any period. It is not filled in any of the 5 years.",
  "account": "inventory valuation reserve",
  "expected_direction": "none",
  "horizon": "fiscal year 2024-09-29..2025-09-27",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0000320193-26-000020:trends:inventory_reserve_ratio:2024-09-29..2025-09-27" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual_insufficient",
  "what_changed": "insufficient. The non-GAAP gap is not filled for the fiscal year 2024-09-29..2025-09-27: no us-gaap concept carries a non-GAAP measure. It is not filled in any of the 5 years.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "fiscal year 2024-09-29..2025-09-27",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0000320193-26-000020:trends:non_gaap_gap:2024-09-29..2025-09-27" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_annual_insufficient",
  "what_changed": "insufficient. The warranty reserve ratio is not filled for the fiscal year 2024-09-29..2025-09-27: the warranty accrual concepts are in the record, but not for 2025-09-27. The only filled period in the table is years-back-4, 'the only filled year', at 0.009195854757980083, on StandardProductWarrantyAccrual at 2021-09-25 of 3364000000.0 from 0000320193-22-000070. One year supports no trend. The input does not say that any later period rests on a different concept, so I report no tag change.",
  "account": "product warranty accrual",
  "expected_direction": "none",
  "horizon": "fiscal year 2024-09-29..2025-09-27",
  "quote": "\"missing\": \"no row for warranty_accrual in 2025-09-27: us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent is in the record, but not for this period\"",
  "paragraph_id": "0000320193-26-000020:trends:warranty_reserve_ratio:2024-09-29..2025-09-27" }
```

```json
{ "id": "articulation_and_the_filed_history_other_non_current_assets_restated",
  "what_changed": "Other non-current assets at 2025-09-27 were filed with two different values. The 10-K 0000320193-25-000079 prints OtherAssetsNoncurrent at 2025-09-27 as 83727000000, and that fact carries superseded_by 0000320193-26-000020. The prior 10-Q 0000320193-26-000013 (0000320193-26-000013:facts:OtherAssetsNoncurrent:2025-09-27) and this 10-Q (0000320193-26-000020:facts:OtherAssetsNoncurrent:2025-09-27) both print the same element at the same date as 72634000000. AssetsNoncurrent (211284000000) and Assets (359241000000) at 2025-09-27 print the same in all three filings. The release balance sheet has a line 'Intangible assets, net' of 11,093 at September 27, 2025 that has no counterpart among the 10-K's balance-sheet facts, which run from PropertyPlantAndEquipmentNet (f-175, f-176) straight to OtherAssetsNoncurrent (f-177, f-178). In both 10-Qs the balance-sheet fact ids skip f-182 and f-183 between those two lines, and no fact for that balance-sheet line is in my input. No restatement trace exists. I read this pair off two printed values, and I do not compute what moved between the lines.",
  "account": "other non-current assets (OtherAssetsNoncurrent); intangible assets, net",
  "expected_direction": "down",
  "horizon": "balance at 2025-09-27 as filed in the 10-K (2025-10-31) against as filed in the 10-Qs (2026-05-01 and 2026-07-31)",
  "quote": "\"value\": \"83727000000\"",
  "paragraph_id": "0000320193-25-000079:facts:OtherAssetsNoncurrent:2025-09-27" }
```

```json
{ "id": "across_documents_intangible_assets_release_against_filed_fact",
  "what_changed": "This 10-Q prints IntangibleAssetsNetExcludingGoodwill as 25417000000 at 2026-06-27 and as 13301000000 at 2025-09-27 (0000320193-26-000020:facts:IntangibleAssetsNetExcludingGoodwill:2025-09-27). The earnings release balance sheet prints 'Intangible assets, net' as 20,342 at June 27, 2026 and 11,093 at September 27, 2025 (millions). For neither date do the two print the same value. My input does not say what separates them, and I do not compute it. At the same two dates the 10-Q prints IntangibleAssetsGrossExcludingGoodwill as 38220000000 against 24950000000, and FiniteLivedIntangibleAssetsAccumulatedAmortization as 12803000000 against 11649000000. No fact carrying the release's balance-sheet line is in my input: the 10-Q's balance-sheet fact ids skip f-182 and f-183 between PropertyPlantAndEquipmentNet and OtherAssetsNoncurrent.",
  "account": "intangible assets, net: IntangibleAssetsNetExcludingGoodwill against the release balance-sheet line",
  "expected_direction": "none",
  "horizon": "balances at 2026-06-27 and 2025-09-27, release 0000320193-26-000018 (2026-07-30) against 10-Q 0000320193-26-000020 (2026-07-31)",
  "quote": "\"value\": \"25417000000\"",
  "paragraph_id": "0000320193-26-000020:facts:IntangibleAssetsNetExcludingGoodwill:2026-06-27" }
```

```json
{ "id": "earnings_quality_inventory_build_in_raw_materials_and_parts",
  "what_changed": "This 10-Q prints InventoryRawMaterialsAndPurchasedPartsNetOfReserves as 7645000000 at 2026-06-27 against 2124000000 at 2025-09-27 (0000320193-26-000020:facts:InventoryRawMaterialsAndPurchasedPartsNetOfReserves:2025-09-27). InventoryFinishedGoodsNetOfReserves prints 3447000000 against 3594000000, and InventoryNet 11092000000 against 5718000000. Of the two components, raw materials and purchased parts print higher at 2026-06-27 and finished goods print lower. This is the quarter in which days sales of inventory sits at 'highest of the 6 filled quarters'. Both components are stated net of reserves, and no reserve figure is in my input.",
  "account": "inventory: raw materials and purchased parts; finished goods",
  "expected_direction": "up",
  "horizon": "balance at 2026-06-27 against 2025-09-27",
  "quote": "\"value\": \"7645000000\"",
  "paragraph_id": "0000320193-26-000020:facts:InventoryRawMaterialsAndPurchasedPartsNetOfReserves:2026-06-27" }
```

```json
{ "id": "revenue_recognition_trade_receivables_customer_concentration",
  "what_changed": "This 10-Q prints ConcentrationRiskPercentage1 for aapl:CustomerOneMember against trade accounts receivable as 0.18 for 2025-09-28..2026-06-27, against 0.12 for 2024-09-29..2025-09-27. For aapl:CellularNetworkCarriersMember it prints 0.27 against 0.34. These sit beside the receivables cells: quarterly receivables over revenue is 'second highest of the 6 filled quarters', and annual receivables over revenue is 'highest of the 5 filled years'. My input does not name the customer.",
  "account": "trade accounts receivable: credit concentration",
  "expected_direction": "up",
  "horizon": "2025-09-28..2026-06-27 against 2024-09-29..2025-09-27",
  "quote": "\"value\": \"0.18\"",
  "paragraph_id": "0000320193-26-000020:facts:ConcentrationRiskPercentage1:2025-09-28..2026-06-27:srt:MajorCustomersAxis=aapl:CustomerOneMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:TradeAccountsReceivableMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CreditConcentrationRiskMember" }
```

```json
{ "id": "earnings_quality_record_gross_margin_includes_tariff_refunds",
  "what_changed": "The earnings release for the quarter ended June 27, 2026 says the company gross margin of 50.1 percent includes a favorable impact of approximately 2 percentage points from tariff refunds. The trend table puts the quarter's gross margin at 'highest of the 6 filled quarters'. By the release's own figures, part of that level comes from tariff refunds. My input has no gross margin with the refunds removed and says nothing on whether they recur, and I do not derive either.",
  "account": "gross margin: cost of sales benefit from tariff refunds",
  "expected_direction": "up",
  "horizon": "quarter ended June 27, 2026",
  "quote": "Company gross margin was 50.1 percent, including a favorable impact of approximately 2 percentage points from tariff refunds.",
  "paragraph_id": "0000320193-26-000018:8k_2_02:7" }
```

```json
{ "id": "earnings_quality_diluted_eps_includes_tariff_refunds",
  "what_changed": "The release says diluted earnings per share for the quarter ended June 27, 2026 was $2.02, up 29 percent year over year, and included a favorable impact of $0.11 from tariff refunds. The release statement of operations prints diluted EPS of 2.02 against 1.57 for the quarter ended June 28, 2025, as do the 10-Q facts. My input has no EPS with the refunds removed, and I do not derive one.",
  "account": "diluted earnings per share",
  "expected_direction": "up",
  "horizon": "quarter ended June 27, 2026 against quarter ended June 28, 2025",
  "quote": "Diluted earnings per share was $2.02, up 29 percent year over year, and included a favorable impact of $0.11 from tariff refunds.",
  "paragraph_id": "0000320193-26-000018:8k_2_02:7" }
```

```json
{ "id": "estimates_and_discretion_intangible_assets_rise",
  "what_changed": "The release's condensed balance sheet prints intangible assets, net, of 20,342 at June 27, 2026 against 11,093 at September 27, 2025 (millions). The 10-Q's IntangibleAssetsNetExcludingGoodwill also prints higher at 2026-06-27 than at 2025-09-27, though at different values (see across_documents_intangible_assets_release_against_filed_fact). The balance-sheet line is new against the 10-K's filed balance sheet (see articulation_and_the_filed_history_other_non_current_assets_restated). The trend table has no metric for intangible assets alone. They sit inside soft assets, where the quarterly soft asset share is 'third highest of the 6 filled quarters'. My input does not say what was added.",
  "account": "intangible assets, net",
  "expected_direction": "up",
  "horizon": "balance at June 27, 2026 against September 27, 2025",
  "quote": "| Intangible assets, net | 20,342 |  |  | 11,093 |  |",
  "paragraph_id": "0000320193-26-000018:8k_2_02:33" }
```

```json
{ "id": "earnings_quality_inventory_build_cash_use",
  "what_changed": "The release's cash flow statement prints the change in inventories as (5,461) for the nine months ended June 27, 2026 against 1,223 for the nine months ended June 28, 2025 (millions). The 10-Q fact IncreaseDecreaseInInventories prints 5461000000 against -1223000000. The release balance sheet prints inventories of 11,092 at June 27, 2026 against 5,718 at September 27, 2025. This matches the quarterly days sales of inventory at 'highest of the 6 filled quarters'. My input has no inventory reserve figure (see estimates_and_discretion_inventory_reserve_ratio_quarterly_insufficient).",
  "account": "inventory",
  "expected_direction": "up",
  "horizon": "nine months ended June 27, 2026 against nine months ended June 28, 2025",
  "quote": "| Inventories | (5,461) |  |  | 1,223 |  |",
  "paragraph_id": "0000320193-26-000018:8k_2_02:37" }
```

## Seen in the notes

Nothing is placed under this heading. No fact I read carries a mark saying whether its element sat inside a note. Each fact prints `id`, `paragraph_id`, `tag`, `prefix`, `namespace`, `context` (some contexts also carry `typed_segment`), `context_ref`, `unit`, `decimals`, `value`, `number`, `nil`, `form`, `source_accession` and `filing_date`; some earlier-filed facts also print `superseded_by`. Three items above rest on facts whose tables are not the primary statements as the release prints them: `across_documents_intangible_assets_release_against_filed_fact`, `earnings_quality_inventory_build_in_raw_materials_and_parts` and `revenue_recognition_trade_receivables_customer_concentration`. My input does not say whether they sat in a note, so they stay under the statements heading, named here so a later reader that has the mark can move them. The split should rest on the mark, not on my reading.
