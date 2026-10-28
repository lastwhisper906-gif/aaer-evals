<!-- the quote gate removed 1 item(s) from this copy; input_manifest.json lists each with its reason -->
# LFUS — numbers reader — filing 0001628280-26-050481 (10-Q for the quarter ended 2026-06-27, filed 2026-07-29)

## Before the items

- **Inputs read in full:** input_trends.json, input_numbers.json, input_8k.md and input_prior_predictions.md.
  - The prior-predictions file says no earlier run is on record for this company, so it has no flags to carry forward.
- **Out-of-scope data:** none in the directory. No prices, abnormal returns, short interest, other companies' files, prior-run probabilities or outcome windows. The run is not broken on that count.
- **quarters-back-0 (target 2026-06-27) has no cells.** The period's reason: "no quarter ending within 20 days of 2026-06-27 is in the companyfacts record; the companyfacts record's newest row was filed 2026-05-06, before this run's cutoff 2026-07-29". The newest quarter the trend table reaches is quarters-back-1 (2025-12-28..2026-03-28). Its metrics are reported below as the latest quarter on record.
- **quarters-back-2 (2025-12-27) and quarters-back-6 (2024-12-28) have no cells.** Reason: "the commonest cause is a fiscal fourth quarter, which no filing reports as a duration". No fourth-quarter derivation is in the input. So every quarters-back-1 quarter-over-quarter change is unavailable. Each cell says "<metric> is not filled in quarters-back-2".
- **No articulation checks, restatement-trace file or fourth-quarter derivation is in the input.** No articulation gap can be reported, because none is printed.
  - Restated prior values are reported from the numeric facts instead: the 10-K's ScenarioAdjustment rows, and the Basler purchase-price figures re-reported after the 10-K.
  - No trend cell or fact says that a period rests on a different concept, so there is no change of tag to report.
- **The research-and-development-capitalized block of years-back-0 prints no paragraph_id**, so nothing in it can be quoted.
  - Its capitalized_development_cost reason reads: "no row for capitalized_development_cost: the companyfacts record tags none of us-gaap:CapitalizedComputerSoftwareAdditions in any period". That makes the block insufficient.
- **No arithmetic was done.** Every number below is copied from the input.
- **expected_direction gives the direction of the printed change**, or of the later printed value against the earlier one in the same filing or the same history. It is "none" where the input prints nothing to compare. Horizon names the comparison window the item covers.
- **Two filled quarters do not support a trend claim.** Where a history is that short, the item says so.

## Seen in the statements

### Trend table — quarters-back-1 (2025-12-28..2026-03-28), the latest quarter on record

```json
{ "id": "earnings_quality_accruals_over_total_assets_trend_latest_quarter", "what_changed": "accruals_over_total_assets value -0.0013249338764412966. Year-over-year change against quarters-back-5 is 0.0043812541497453925. Quarter-over-quarter is unavailable (not filled in quarters-back-2). Only 2 filled quarters exist, which is insufficient for a trend claim. Inputs: net income 75147000, operating cash flow 80258000, assets 3857551000 (all from 0001628280-26-031041).", "account": "accruals (net income less operating cash flow) over total assets", "expected_direction": "up", "horizon": "quarter ended 2026-03-28 against quarter ended 2025-03-29", "quote": "\"position_in_history\": \"highest of the 2 filled quarters\"", "paragraph_id": "0001628280-26-050481:trends:accruals_over_total_assets:2025-12-28..2026-03-28" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_trend_latest_quarter", "what_changed": "bad_debt_reserve_ratio value 0.173363219553052. Year-over-year change -0.005528562854355407. Quarter-over-quarter unavailable. Inputs: allowance 79896000, receivables 380963000.", "account": "allowance for doubtful accounts over gross receivables", "expected_direction": "down", "horizon": "quarter ended 2026-03-28 against quarter ended 2025-03-29", "quote": "\"position_in_history\": \"third highest of the 5 filled quarters\"", "paragraph_id": "0001628280-26-050481:trends:bad_debt_reserve_ratio:2025-12-28..2026-03-28" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_trend_latest_quarter", "what_changed": "contract_liabilities_over_revenue value 0.010218138146548771, the highest of the 5 filled quarters. Year-over-year change 0.005572697984328197. Quarter-over-quarter unavailable. Inputs: deferred revenue 6713000, revenue 656969000.", "account": "contract liabilities (deferred revenue) over revenue", "expected_direction": "up", "horizon": "quarter ended 2026-03-28 against quarter ended 2025-03-29", "quote": "\"position_in_history\": \"highest of the 5 filled quarters\"", "paragraph_id": "0001628280-26-050481:trends:contract_liabilities_over_revenue:2025-12-28..2026-03-28" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_trend_latest_quarter", "what_changed": "days_sales_of_inventory value 94.63756020058587. Year-over-year change -14.730463519270884. Quarter-over-quarter unavailable. Inputs: inventory 418922000, cost of revenue 402820000.", "account": "inventory days", "expected_direction": "down", "horizon": "quarter ended 2026-03-28 against quarter ended 2025-03-29", "quote": "\"position_in_history\": \"second lowest of the 5 filled quarters\"", "paragraph_id": "0001628280-26-050481:trends:days_sales_of_inventory:2025-12-28..2026-03-28" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_trend_latest_quarter", "what_changed": "days_sales_outstanding value 52.769054552041275. Year-over-year change 0.5915644608102397. Quarter-over-quarter unavailable. Inputs: receivables 380963000, revenue 656969000.", "account": "receivable days", "expected_direction": "up", "horizon": "quarter ended 2026-03-28 against quarter ended 2025-03-29", "quote": "\"position_in_history\": \"second lowest of the 5 filled quarters\"", "paragraph_id": "0001628280-26-050481:trends:days_sales_outstanding:2025-12-28..2026-03-28" }
```

```json
{ "id": "earnings_quality_gross_margin_trend_latest_quarter", "what_changed": "gross_margin value 0.3868508255336249, the highest of the 5 filled quarters. Year-over-year change 0.012949720189474434. Quarter-over-quarter unavailable. Inputs: revenue 656969000, cost of revenue 402820000.", "account": "gross margin", "expected_direction": "up", "horizon": "quarter ended 2026-03-28 against quarter ended 2025-03-29", "quote": "\"position_in_history\": \"highest of the 5 filled quarters\"", "paragraph_id": "0001628280-26-050481:trends:gross_margin:2025-12-28..2026-03-28" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_trend_latest_quarter", "what_changed": "inventory_reserve_ratio value 0.19954311303774927. Year-over-year change 0.02631450229025825. Quarter-over-quarter unavailable. Inputs: inventory reserve 83593000, inventory 418922000.", "account": "inventory valuation reserve over inventory", "expected_direction": "up", "horizon": "quarter ended 2026-03-28 against quarter ended 2025-03-29", "quote": "\"position_in_history\": \"second highest of the 5 filled quarters\"", "paragraph_id": "0001628280-26-050481:trends:inventory_reserve_ratio:2025-12-28..2026-03-28" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_trend_latest_quarter", "what_changed": "receivables_over_revenue value 0.5798797203521019. Year-over-year change 0.006500708360552054. Quarter-over-quarter unavailable.", "account": "trade receivables over quarterly revenue", "expected_direction": "up", "horizon": "quarter ended 2026-03-28 against quarter ended 2025-03-29", "quote": "\"position_in_history\": \"second lowest of the 5 filled quarters\"", "paragraph_id": "0001628280-26-050481:trends:receivables_over_revenue:2025-12-28..2026-03-28" }
```

```json
{ "id": "earnings_quality_soft_asset_share_trend_latest_quarter", "what_changed": "soft_asset_share value 0.7368213667168626, the highest of the 5 filled quarters. Year-over-year change 0.02719039019409586. Quarter-over-quarter unavailable. Inputs: assets 3857551000, PP&E 533528000, cash 481697000.", "account": "assets other than PP&E and cash, over total assets", "expected_direction": "up", "horizon": "quarter ended 2026-03-28 against quarter ended 2025-03-29", "quote": "\"position_in_history\": \"highest of the 5 filled quarters\"", "paragraph_id": "0001628280-26-050481:trends:soft_asset_share:2025-12-28..2026-03-28" }
```

```json
{ "id": "results_against_expectations_non_gaap_gap_trend_latest_quarter", "what_changed": "insufficient: the non_gaap_gap cell is not filled, so there is no value, no change and no position in history.", "account": "gap between non-GAAP and GAAP net income", "expected_direction": "none", "horizon": "quarter ended 2026-03-28", "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"", "paragraph_id": "0001628280-26-050481:trends:non_gaap_gap:2025-12-28..2026-03-28" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_trend_latest_quarter", "what_changed": "insufficient: the warranty_reserve_ratio cell is not filled, because no warranty accrual concept is tagged in any period of the record.", "account": "warranty reserve", "expected_direction": "none", "horizon": "quarter ended 2026-03-28", "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment", "paragraph_id": "0001628280-26-050481:trends:warranty_reserve_ratio:2025-12-28..2026-03-28" }
```

### Trend table — years-back-0 (2024-12-29..2025-12-27)

```json
{ "id": "earnings_quality_accruals_over_total_assets_trend_latest_year", "what_changed": "accruals_over_total_assets value -0.12774578219347169, the lowest of the 5 filled years. Year-over-year change against years-back-1 is -0.059028879203862045. Inputs: net income -71700000 and operating cash flow 433764000 (10-K 0001628280-26-009585), assets 3956796000 (0001628280-26-031041).", "account": "accruals over total assets", "expected_direction": "down", "horizon": "fiscal 2025 against fiscal 2024", "quote": "\"position_in_history\": \"lowest of the 5 filled years\"", "paragraph_id": "0001628280-26-050481:trends:accruals_over_total_assets:2024-12-29..2025-12-27" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_trend_latest_year", "what_changed": "bad_debt_reserve_ratio value 0.17505133003852025, the lowest of the 5 filled years. Year-over-year change -0.01703838318545267. Inputs: allowance 77073000, receivables 363215000.", "account": "allowance for doubtful accounts over gross receivables", "expected_direction": "down", "horizon": "fiscal 2025 against fiscal 2024", "quote": "\"position_in_history\": \"lowest of the 5 filled years\"", "paragraph_id": "0001628280-26-050481:trends:bad_debt_reserve_ratio:2024-12-29..2025-12-27" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_trend_latest_year", "what_changed": "contract_liabilities_over_revenue value 0.004699756190980659, the highest of the 5 filled years. Year-over-year change 0.003989046522042642. Inputs: deferred revenue 11215000, revenue 2386294000.", "account": "contract liabilities over revenue", "expected_direction": "up", "horizon": "fiscal 2025 against fiscal 2024", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0001628280-26-050481:trends:contract_liabilities_over_revenue:2024-12-29..2025-12-27" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_trend_latest_year", "what_changed": "days_sales_of_inventory value 102.41223143912755, the lowest of the 5 filled years. Year-over-year change -5.569926816206944. Inputs: inventory 416472000, cost of revenue 1480251000.", "account": "inventory days", "expected_direction": "down", "horizon": "fiscal 2025 against fiscal 2024", "quote": "\"position_in_history\": \"lowest of the 5 filled years\"", "paragraph_id": "0001628280-26-050481:trends:days_sales_of_inventory:2024-12-29..2025-12-27" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_trend_latest_year", "what_changed": "days_sales_outstanding value 55.404011408485296, the highest of the 5 filled years. Year-over-year change 6.493746149909313. Inputs: receivables 363215000, revenue 2386294000.", "account": "receivable days", "expected_direction": "up", "horizon": "fiscal 2025 against fiscal 2024", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0001628280-26-050481:trends:days_sales_outstanding:2024-12-29..2025-12-27" }
```

```json
{ "id": "earnings_quality_gross_margin_trend_latest_year", "what_changed": "gross_margin value 0.37968624151089514. Year-over-year change 0.020204087307437724. Inputs: revenue 2386294000, cost of revenue 1480251000.", "account": "gross margin", "expected_direction": "up", "horizon": "fiscal 2025 against fiscal 2024", "quote": "\"position_in_history\": \"third highest of the 5 filled years\"", "paragraph_id": "0001628280-26-050481:trends:gross_margin:2024-12-29..2025-12-27" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_trend_latest_year", "what_changed": "inventory_reserve_ratio value 0.19856076759061833, the highest of the 5 filled years. Year-over-year change 0.038749778167811666. Inputs: inventory reserve 82695000, inventory 416472000.", "account": "inventory valuation reserve over inventory", "expected_direction": "up", "horizon": "fiscal 2025 against fiscal 2024", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0001628280-26-050481:trends:inventory_reserve_ratio:2024-12-29..2025-12-27" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_trend_latest_year", "what_changed": "receivables_over_revenue value 0.15220882255078377, the highest of the 5 filled years. Year-over-year change 0.017839961950300298.", "account": "trade receivables over annual revenue", "expected_direction": "up", "horizon": "fiscal 2025 against fiscal 2024", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0001628280-26-050481:trends:receivables_over_revenue:2024-12-29..2025-12-27" }
```

```json
{ "id": "earnings_quality_soft_asset_share_trend_latest_year", "what_changed": "soft_asset_share value 0.7209785392019199. Year-over-year change 0.02983266478304869. Inputs: assets 3956796000, PP&E 540640000, cash 563391000.", "account": "soft assets over total assets", "expected_direction": "up", "horizon": "fiscal 2025 against fiscal 2024", "quote": "\"position_in_history\": \"third highest of the 5 filled years\"", "paragraph_id": "0001628280-26-050481:trends:soft_asset_share:2024-12-29..2025-12-27" }
```

```json
{ "id": "results_against_expectations_non_gaap_gap_trend_latest_year", "what_changed": "insufficient: the non_gaap_gap cell is not filled for the latest year.", "account": "gap between non-GAAP and GAAP net income", "expected_direction": "none", "horizon": "fiscal 2025", "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"", "paragraph_id": "0001628280-26-050481:trends:non_gaap_gap:2024-12-29..2025-12-27" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_trend_latest_year", "what_changed": "insufficient: the warranty_reserve_ratio cell is not filled for the latest year. No warranty accrual concept is tagged in any period.", "account": "warranty reserve", "expected_direction": "none", "horizon": "fiscal 2025", "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment", "paragraph_id": "0001628280-26-050481:trends:warranty_reserve_ratio:2024-12-29..2025-12-27" }
```


### Restated prior values (the filed history)

```json
{ "id": "articulation_and_the_filed_history_prior_year_cost_of_sales_adjustment", "what_changed": "The fiscal 2025 10-K carries a statement-scenario adjustment row for fiscal 2024 cost of goods sold of 12300000. Fiscal 2024 is therefore stated differently from what was originally reported.", "account": "cost of goods and services sold, fiscal 2024", "expected_direction": "up", "horizon": "fiscal 2024 as re-presented in the fiscal 2025 10-K", "quote": "\"value\": \"12300000\"", "paragraph_id": "0001628280-26-009585:facts:CostOfGoodsAndServicesSold:2023-12-31..2024-12-28:srt:StatementScenarioAxis=us-gaap:ScenarioAdjustmentMember" }
```

```json
{ "id": "articulation_and_the_filed_history_prior_year_inventory_adjustment", "what_changed": "The same 10-K carries a scenario adjustment to inventory at 2024-12-28 of -12300000. It pairs with the cost-of-sales adjustment above.", "account": "inventory, 2024-12-28", "expected_direction": "down", "horizon": "balance at 2024-12-28 as re-presented in the fiscal 2025 10-K", "quote": "\"value\": \"-12300000\"", "paragraph_id": "0001628280-26-009585:facts:InventoryNet:2024-12-28:srt:StatementScenarioAxis=us-gaap:ScenarioAdjustmentMember" }
```

```json
{ "id": "articulation_and_the_filed_history_basler_goodwill_restated", "what_changed": "Goodwill recognized for the Basler Electric acquisition at 2025-12-11 is reported as 160977000 in this 10-Q, as in the first-quarter 10-Q. The fiscal 2025 10-K reported 152343000 for the same acquisition-date item.", "account": "Basler acquisition goodwill", "expected_direction": "up", "horizon": "acquisition-date balance, 10-K against later 10-Qs", "quote": "\"value\": \"160977000\"", "paragraph_id": "0001628280-26-050481:facts:Goodwill:2025-12-11:us-gaap:BusinessAcquisitionAxis=lfus:BaslerElectricMember" }
```

```json
{ "id": "articulation_and_the_filed_history_basler_intangibles_restated", "what_changed": "Identifiable intangibles recognized for Basler at 2025-12-11 are 145000000 in this 10-Q. The fiscal 2025 10-K reported 150000000.", "account": "Basler acquisition intangibles", "expected_direction": "down", "horizon": "acquisition-date balance, 10-K against later 10-Qs", "quote": "\"value\": \"145000000\"", "paragraph_id": "0001628280-26-050481:facts:BusinessCombinationRecognizedIdentifiableAssetsAcquiredAndLiabilitiesAssumedIntangibleAssetsOtherThanGoodwill:2025-12-11:us-gaap:BusinessAcquisitionAxis=lfus:BaslerElectricMember" }
```

```json
{ "id": "articulation_and_the_filed_history_basler_net_assets_restated", "what_changed": "Net assets acquired for Basler (goodwill plus identifiable net assets) are 353119000 in this 10-Q. The 10-K's consideration fact read 350300000 and is marked superseded by the first-quarter 10-Q, which reported 352809000.", "account": "Basler purchase price / net assets acquired", "expected_direction": "up", "horizon": "acquisition-date amounts across the 10-K and the two 2026 10-Qs", "quote": "\"value\": \"353119000\"", "paragraph_id": "0001628280-26-050481:facts:BusinessCombinationRecognizedIdentifiableAssetsAcquiredGoodwillAndLiabilitiesAssumedNet:2025-12-11:us-gaap:BusinessAcquisitionAxis=lfus:BaslerElectricMember" }
```

```json
{ "id": "estimates_and_discretion_basler_measurement_period_intangibles", "what_changed": "Measurement-period adjustment to Basler intangibles of -5000000.0 in the six months ended 2026-06-27. The first-quarter 10-Q carried the same -5000000.0 for its quarter.", "account": "Basler intangibles, provisional adjustment", "expected_direction": "down", "horizon": "six months ended 2026-06-27", "quote": "\"value\": \"-5000000.0\"", "paragraph_id": "0001628280-26-050481:facts:BusinessCombinationProvisionalInformationInitialAccountingIncompleteAdjustmentIntangibles:2025-12-28..2026-06-27:us-gaap:BusinessAcquisitionAxis=lfus:BaslerElectricMember" }
```

```json
{ "id": "estimates_and_discretion_basler_measurement_period_inventory", "what_changed": "Measurement-period adjustment to Basler inventory of -2600000 in the six months.", "account": "Basler inventory, provisional adjustment", "expected_direction": "down", "horizon": "six months ended 2026-06-27", "quote": "\"value\": \"-2600000\"", "paragraph_id": "0001628280-26-050481:facts:BusinessCombinationProvisionalInformationInitialAccountingIncompleteAdjustmentInventory:2025-12-28..2026-06-27:us-gaap:BusinessAcquisitionAxis=lfus:BaslerElectricMember" }
```

```json
{ "id": "estimates_and_discretion_basler_measurement_period_property", "what_changed": "Measurement-period adjustment to Basler property, plant and equipment of -1700000 in the six months.", "account": "Basler PP&E, provisional adjustment", "expected_direction": "down", "horizon": "six months ended 2026-06-27", "quote": "\"value\": \"-1700000\"", "paragraph_id": "0001628280-26-050481:facts:BusinessCombinationProvisionalInformationInitialAccountingIncompleteAdjustmentPropertyPlantAndEquipment:2025-12-28..2026-06-27:us-gaap:BusinessAcquisitionAxis=lfus:BaslerElectricMember" }
```

```json
{ "id": "estimates_and_discretion_basler_goodwill_purchase_accounting_adjustment", "what_changed": "Goodwill purchase-accounting adjustment for Basler of 8600000 in the six months. The segment goodwill roll-forward tags 8634000 as goodwill acquired during the period in Industrial (see the structure item below).", "account": "Basler goodwill adjustment", "expected_direction": "up", "horizon": "six months ended 2026-06-27", "quote": "\"value\": \"8600000\"", "paragraph_id": "0001628280-26-050481:facts:GoodwillTranslationAndPurchaseAccountingAdjustments:2025-12-28..2026-06-27:us-gaap:BusinessAcquisitionAxis=lfus:BaslerElectricMember" }
```

```json
{ "id": "estimates_and_discretion_basler_consideration_adjustment", "what_changed": "Additional Basler consideration transferred of 2800000 in the six months, of which the quarter ended 2026-06-27 carries 300000.", "account": "Basler consideration", "expected_direction": "up", "horizon": "six months ended 2026-06-27", "quote": "\"value\": \"2800000\"", "paragraph_id": "0001628280-26-050481:facts:BusinessCombinationConsiderationTransferred1:2025-12-28..2026-06-27:us-gaap:BusinessAcquisitionAxis=lfus:BaslerElectricMember" }
```

```json
{ "id": "estimates_and_discretion_basler_inventory_adjustment_prior_quarter", "what_changed": "This 10-Q tags a Basler inventory provisional-information adjustment of 6400000 for the quarter 2025-09-28..2025-12-27. The 8-K's trailing-twelve-month consolidated EBITDA lists a purchase accounting inventory step-up charge of 6.4.", "account": "Basler inventory step-up", "expected_direction": "up", "horizon": "fiscal fourth quarter 2025", "quote": "\"value\": \"6400000\"", "paragraph_id": "0001628280-26-050481:facts:BusinessCombinationProvisionalInformationInitialAccountingIncompleteAdjustmentInventory:2025-09-28..2025-12-27:us-gaap:BusinessAcquisitionAxis=lfus:BaslerElectricMember" }
```

### Numeric facts — income statement, quarter ended 2026-06-27

```json
{ "id": "results_against_expectations_net_sales_reported_quarter", "what_changed": "Net sales 738781000 against 613413000 in the quarter ended 2025-06-28.", "account": "revenue", "expected_direction": "up", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"738781000\"", "paragraph_id": "0001628280-26-050481:facts:RevenueFromContractWithCustomerIncludingAssessedTax:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_cost_of_sales_reported_quarter", "what_changed": "Cost of goods sold 432717000 against 381359000.", "account": "cost of sales", "expected_direction": "up", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"432717000\"", "paragraph_id": "0001628280-26-050481:facts:CostOfGoodsAndServicesSold:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_gross_profit_reported_quarter", "what_changed": "Gross profit 306064000 against 232054000.", "account": "gross profit", "expected_direction": "up", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"306064000\"", "paragraph_id": "0001628280-26-050481:facts:GrossProfit:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_selling_general_administrative_reported_quarter", "what_changed": "SG&A 120578000 against 95517000.", "account": "selling, general and administrative expense", "expected_direction": "up", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"120578000\"", "paragraph_id": "0001628280-26-050481:facts:SellingGeneralAndAdministrativeExpense:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_research_and_development_reported_quarter", "what_changed": "R&D expense 31037000 against 26401000.", "account": "research and development expense", "expected_direction": "up", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"31037000\"", "paragraph_id": "0001628280-26-050481:facts:ResearchAndDevelopmentExpense:2026-03-29..2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_intangible_amortization_reported_quarter", "what_changed": "Amortization of intangibles 14704000 against 14852000, while net intangibles include the Basler additions.", "account": "amortization of intangible assets", "expected_direction": "down", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"14704000\"", "paragraph_id": "0001628280-26-050481:facts:AmortizationOfIntangibleAssets:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_restructuring_impairment_other_charges_reported_quarter", "what_changed": "Restructuring, impairment and other charges 20021000 against 2506000. For the six months: 27443000 against 11525000.", "account": "restructuring, impairment and other charges", "expected_direction": "up", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"20021000\"", "paragraph_id": "0001628280-26-050481:facts:RestructuringSettlementAndImpairmentProvisions:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_operating_income_reported_quarter", "what_changed": "Operating income 119724000 against 92778000.", "account": "operating income", "expected_direction": "up", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"119724000\"", "paragraph_id": "0001628280-26-050481:facts:OperatingIncomeLoss:2026-03-29..2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_interest_expense_reported_quarter", "what_changed": "Interest expense 5739000 against 8568000.", "account": "interest expense", "expected_direction": "down", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"5739000\"", "paragraph_id": "0001628280-26-050481:facts:InterestExpenseNonoperating:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_foreign_exchange_reported_quarter", "what_changed": "Foreign currency transaction gain/loss 160000 against -10448000 a year earlier (sign as tagged). For the six months: 2573000 against -15291000.", "account": "foreign exchange gain or loss", "expected_direction": "up", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"160000\"", "paragraph_id": "0001628280-26-050481:facts:ForeignCurrencyTransactionGainLossBeforeTax:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_other_nonoperating_income_reported_quarter", "what_changed": "Other nonoperating income 2919000 against 4452000.", "account": "other income, net", "expected_direction": "down", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"2919000\"", "paragraph_id": "0001628280-26-050481:facts:OtherNonoperatingIncomeExpense:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_income_tax_expense_reported_quarter", "what_changed": "Income tax expense 27659000 against 20872000. Pretax income 117064000 against 78214000.", "account": "income tax expense", "expected_direction": "up", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"27659000\"", "paragraph_id": "0001628280-26-050481:facts:IncomeTaxExpenseBenefit:2026-03-29..2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_effective_tax_rate_reported_quarter", "what_changed": "Effective tax rate 0.236 against 0.267. For the six months: 0.230 against 0.270. The fiscal 2025 10-K tags 20.878 as the annual effective rate (see the 10-K item below).", "account": "effective income tax rate", "expected_direction": "down", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"0.236\"", "paragraph_id": "0001628280-26-050481:facts:EffectiveIncomeTaxRateContinuingOperations:2026-03-29..2026-06-27" }
```

```json
{ "id": "results_against_expectations_net_income_reported_quarter", "what_changed": "Net income 89405000 against 57342000. For the six months: 164552000 against 100913000.", "account": "net income", "expected_direction": "up", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"89405000\"", "paragraph_id": "0001628280-26-050481:facts:NetIncomeLoss:2026-03-29..2026-06-27" }
```

```json
{ "id": "results_against_expectations_diluted_eps_reported_quarter", "what_changed": "Diluted EPS 3.49 against 2.30. For the six months: 6.44 against 4.05.", "account": "diluted earnings per share", "expected_direction": "up", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"3.49\"", "paragraph_id": "0001628280-26-050481:facts:EarningsPerShareDiluted:2026-03-29..2026-06-27" }
```

```json
{ "id": "structure_and_disclosure_changes_diluted_share_count_reported_quarter", "what_changed": "Weighted diluted shares 25620000 against 24905000. Shares issued 27511066 at 2026-06-27 against 27014490 at 2025-12-27.", "account": "diluted share count", "expected_direction": "up", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"25620000\"", "paragraph_id": "0001628280-26-050481:facts:WeightedAverageNumberOfDilutedSharesOutstanding:2026-03-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_comprehensive_income_reported_quarter", "what_changed": "Comprehensive income 83699000 against 155255000. Foreign currency translation was -6798000 against 91899000.", "account": "comprehensive income", "expected_direction": "down", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"83699000\"", "paragraph_id": "0001628280-26-050481:facts:ComprehensiveIncomeNetOfTax:2026-03-29..2026-06-27" }
```

```json
{ "id": "results_against_expectations_net_sales_reported_six_months", "what_changed": "Six-month net sales 1395750000 against 1167720000.", "account": "revenue, year to date", "expected_direction": "up", "horizon": "six months ended 2026-06-27 against six months ended 2025-06-28", "quote": "\"value\": \"1395750000\"", "paragraph_id": "0001628280-26-050481:facts:RevenueFromContractWithCustomerIncludingAssessedTax:2025-12-28..2026-06-27" }
```

### Numeric facts — cash flow, six months ended 2026-06-27

```json
{ "id": "earnings_quality_operating_cash_flow_reported_six_months", "what_changed": "Net cash from operating activities 226474000 against 148225000. The first-quarter 10-Q reported 80258000 for its quarter.", "account": "operating cash flow", "expected_direction": "up", "horizon": "six months ended 2026-06-27 against six months ended 2025-06-28", "quote": "\"value\": \"226474000\"", "paragraph_id": "0001628280-26-050481:facts:NetCashProvidedByUsedInOperatingActivities:2025-12-28..2026-06-27" }
```

```json
{ "id": "revenue_recognition_receivables_cash_flow_change_six_months", "what_changed": "Increase/decrease in accounts receivable tagged 65720000 against 52635000. The 8-K cash flow shows trade receivables as (65,720) and (52,635), i.e. cash absorbed.", "account": "change in trade receivables", "expected_direction": "up", "horizon": "six months ended 2026-06-27 against six months ended 2025-06-28", "quote": "\"value\": \"65720000\"", "paragraph_id": "0001628280-26-050481:facts:IncreaseDecreaseInAccountsReceivable:2025-12-28..2026-06-27" }
```

```json
{ "id": "earnings_quality_inventory_cash_flow_change_six_months", "what_changed": "Increase/decrease in inventories tagged 21254000 against -23316000.", "account": "change in inventories", "expected_direction": "up", "horizon": "six months ended 2026-06-27 against six months ended 2025-06-28", "quote": "\"value\": \"21254000\"", "paragraph_id": "0001628280-26-050481:facts:IncreaseDecreaseInInventories:2025-12-28..2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_accounts_payable_cash_flow_change_six_months", "what_changed": "Increase in accounts payable 39159000 against -7001000.", "account": "change in accounts payable", "expected_direction": "up", "horizon": "six months ended 2026-06-27 against six months ended 2025-06-28", "quote": "\"value\": \"39159000\"", "paragraph_id": "0001628280-26-050481:facts:IncreaseDecreaseInAccountsPayable:2025-12-28..2026-06-27" }
```

```json
{ "id": "revenue_recognition_contract_liability_cash_flow_change_six_months", "what_changed": "Change in contract liabilities -4308000 against 2844000.", "account": "change in contract liabilities", "expected_direction": "down", "horizon": "six months ended 2026-06-27 against six months ended 2025-06-28", "quote": "\"value\": \"-4308000\"", "paragraph_id": "0001628280-26-050481:facts:IncreaseDecreaseInContractWithCustomerLiability:2025-12-28..2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_capital_expenditure_six_months", "what_changed": "Purchases of PP&E 33021000 against 32999000.", "account": "capital expenditure", "expected_direction": "up", "horizon": "six months ended 2026-06-27 against six months ended 2025-06-28", "quote": "\"value\": \"33021000\"", "paragraph_id": "0001628280-26-050481:facts:PaymentsToAcquirePropertyPlantAndEquipment:2025-12-28..2026-06-27" }
```

```json
{ "id": "earnings_quality_asset_sale_proceeds_six_months", "what_changed": "Proceeds from sale of PP&E 9115000 against 712000.", "account": "proceeds from asset sales", "expected_direction": "up", "horizon": "six months ended 2026-06-27 against six months ended 2025-06-28", "quote": "\"value\": \"9115000\"", "paragraph_id": "0001628280-26-050481:facts:ProceedsFromSaleOfPropertyPlantAndEquipment:2025-12-28..2026-06-27" }
```

```json
{ "id": "earnings_quality_asset_impairment_addback_six_months", "what_changed": "Asset impairment charges added back 13146000 against 136000.", "account": "asset impairment charges", "expected_direction": "up", "horizon": "six months ended 2026-06-27 against six months ended 2025-06-28", "quote": "\"value\": \"13146000\"", "paragraph_id": "0001628280-26-050481:facts:AssetImpairmentCharges:2025-12-28..2026-06-27" }
```

```json
{ "id": "earnings_quality_deferred_tax_expense_six_months", "what_changed": "Deferred income tax expense 10026000 against -807000.", "account": "deferred income taxes", "expected_direction": "up", "horizon": "six months ended 2026-06-27 against six months ended 2025-06-28", "quote": "\"value\": \"10026000\"", "paragraph_id": "0001628280-26-050481:facts:DeferredIncomeTaxExpenseBenefit:2025-12-28..2026-06-27" }
```

```json
{ "id": "earnings_quality_share_based_compensation_six_months", "what_changed": "Share-based compensation 14953000 against 13447000.", "account": "share-based compensation", "expected_direction": "up", "horizon": "six months ended 2026-06-27 against six months ended 2025-06-28", "quote": "\"value\": \"14953000\"", "paragraph_id": "0001628280-26-050481:facts:ShareBasedCompensation:2025-12-28..2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_unsecured_term_loan_repayment_six_months", "what_changed": "Repayments of unsecured debt 66250000 against 7500000. The first-quarter 10-Q reported the same 66250000 for its quarter alone.", "account": "repayment of unsecured term loan", "expected_direction": "up", "horizon": "six months ended 2026-06-27 against six months ended 2025-06-28", "quote": "\"value\": \"66250000\"", "paragraph_id": "0001628280-26-050481:facts:RepaymentsOfUnsecuredDebt:2025-12-28..2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_revolver_repayment_six_months", "what_changed": "Repayments of long-term lines of credit 100000000 against 0. The debt note tags 100000000.0 of line-of-credit repayment in the first quarter.", "account": "revolving credit repayment", "expected_direction": "up", "horizon": "six months ended 2026-06-27 against six months ended 2025-06-28", "quote": "\"value\": \"100000000\"", "paragraph_id": "0001628280-26-050481:facts:RepaymentsOfLongTermLinesOfCredit:2025-12-28..2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_share_repurchases_six_months", "what_changed": "Share repurchases 0 against 27553000. Shares repurchased under the 2024 program: 0 in the six months, against 120689 a year earlier.", "account": "share repurchases", "expected_direction": "down", "horizon": "six months ended 2026-06-27 against six months ended 2025-06-28", "quote": "\"value\": \"0\"", "paragraph_id": "0001628280-26-050481:facts:PaymentsForRepurchaseOfCommonStock:2025-12-28..2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_dividends_paid_six_months", "what_changed": "Dividends paid 37872000 against 34677000. The per-share dividend paid was 0.75 in the quarter against 0.70 a year earlier.", "account": "cash dividends", "expected_direction": "up", "horizon": "six months ended 2026-06-27 against six months ended 2025-06-28", "quote": "\"value\": \"37872000\"", "paragraph_id": "0001628280-26-050481:facts:PaymentsOfDividends:2025-12-28..2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_debt_issuance_costs_six_months", "what_changed": "Debt issuance costs paid 2169000 against 0. Deferred finance costs on the balance sheet are 3322000 at 2026-06-27 against 1833000 at 2025-12-27.", "account": "debt issuance costs", "expected_direction": "up", "horizon": "six months ended 2026-06-27 against six months ended 2025-06-28", "quote": "\"value\": \"2169000\"", "paragraph_id": "0001628280-26-050481:facts:PaymentsOfDebtIssuanceCosts:2025-12-28..2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_stock_option_exercises_quarter", "what_changed": "Stock issued on option exercises 40938000 in the quarter, against 2483000 a year earlier. The first quarter of 2026 carried 45284000. APIC is 1199321000 at 2026-06-27 against 1098150000 at 2025-12-27.", "account": "equity issued on option exercise", "expected_direction": "up", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"40938000\"", "paragraph_id": "0001628280-26-050481:facts:StockIssuedDuringPeriodValueStockOptionsExercised:2026-03-29..2026-06-27" }
```

### Numeric facts — balance sheet at 2026-06-27 against 2025-12-27

```json
{ "id": "liquidity_and_capital_cash_balance", "what_changed": "Cash and equivalents 628224000 against 563391000.", "account": "cash and cash equivalents", "expected_direction": "up", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"628224000\"", "paragraph_id": "0001628280-26-050481:facts:CashAndCashEquivalentsAtCarryingValue:2026-06-27" }
```

```json
{ "id": "revenue_recognition_trade_receivables_balance", "what_changed": "Net trade receivables 423590000 against 363215000. The first-quarter 10-Q had 380963000 at 2026-03-28.", "account": "accounts receivable, net", "expected_direction": "up", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"423590000\"", "paragraph_id": "0001628280-26-050481:facts:AccountsReceivableNetCurrent:2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_doubtful_accounts_allowance_balance", "what_changed": "Allowance for doubtful accounts 86865000 against 77073000. It was 79896000 at 2026-03-28.", "account": "allowance for doubtful accounts", "expected_direction": "up", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"86865000\"", "paragraph_id": "0001628280-26-050481:facts:AllowanceForDoubtfulAccountsReceivableCurrent:2026-06-27" }
```

```json
{ "id": "earnings_quality_inventory_balance", "what_changed": "Net inventory 433755000 against 416472000. It was 418922000 at 2026-03-28.", "account": "inventory, net", "expected_direction": "up", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"433755000\"", "paragraph_id": "0001628280-26-050481:facts:InventoryNet:2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_inventory_valuation_reserve_balance", "what_changed": "Inventory valuation reserves 80530000 against 82695000, while net inventory rose. The reserve was 83593000 at 2026-03-28.", "account": "inventory valuation reserve", "expected_direction": "down", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"80530000\"", "paragraph_id": "0001628280-26-050481:facts:InventoryValuationReserves:2026-06-27" }
```

```json
{ "id": "revenue_recognition_deferred_revenue_balance", "what_changed": "Deferred revenue 4989000 against 11215000. It was 6713000 at 2026-03-28, the input that put contract_liabilities_over_revenue at the top of its quarterly history.", "account": "deferred revenue (contract liabilities)", "expected_direction": "down", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"4989000\"", "paragraph_id": "0001628280-26-050481:facts:DeferredRevenue:2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_property_plant_equipment_balance", "what_changed": "Net PP&E 513160000 against 540640000.", "account": "property, plant and equipment, net", "expected_direction": "down", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"513160000\"", "paragraph_id": "0001628280-26-050481:facts:PropertyPlantAndEquipmentNet:2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_intangible_assets_balance", "what_changed": "Net intangible assets 553511000 against 594907000.", "account": "intangible assets, net", "expected_direction": "down", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"553511000\"", "paragraph_id": "0001628280-26-050481:facts:IntangibleAssetsNetExcludingGoodwill:2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_goodwill_balance", "what_changed": "Goodwill 1203861000 against 1211411000. Six-month foreign currency translation on goodwill is -16184000.", "account": "goodwill", "expected_direction": "down", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"1203861000\"", "paragraph_id": "0001628280-26-050481:facts:Goodwill:2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_accumulated_goodwill_impairment_balance", "what_changed": "Accumulated goodwill impairment 388216000 at 2026-06-27 against 396982000 at 2025-12-27. Electronics is 296576000 against 303133000.", "account": "accumulated goodwill impairment", "expected_direction": "down", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"388216000\"", "paragraph_id": "0001628280-26-050481:facts:GoodwillImpairedAccumulatedImpairmentLoss:2026-06-27" }
```

```json
{ "id": "earnings_quality_long_term_investments_balance", "what_changed": "Long-term investments 11923000 against 20010000. A realized gain on the Polytronics holding is tagged for the quarter (next item).", "account": "investments", "expected_direction": "down", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"11923000\"", "paragraph_id": "0001628280-26-050481:facts:LongTermInvestments:2026-06-27" }
```

```json
{ "id": "earnings_quality_polytronics_realized_gain_quarter", "what_changed": "A realized gain on equity securities (Polytronics) of 7400000 is tagged for the quarter ended 2026-06-27.", "account": "gain on equity securities", "expected_direction": "up", "horizon": "quarter ended 2026-06-27", "quote": "\"value\": \"7400000\"", "paragraph_id": "0001628280-26-050481:facts:EquitySecuritiesFvNiRealizedGainLoss:2026-03-29..2026-06-27:srt:ScheduleOfEquityMethodInvestmentEquityMethodInvesteeNameAxis=lfus:PolytronicsMember" }
```

```json
{ "id": "liquidity_and_capital_total_assets_balance", "what_changed": "Total assets 4012479000 against 3956796000.", "account": "total assets", "expected_direction": "up", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"4012479000\"", "paragraph_id": "0001628280-26-050481:facts:Assets:2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_current_assets_balance", "what_changed": "Current assets 1583609000 against 1435334000.", "account": "total current assets", "expected_direction": "up", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"1583609000\"", "paragraph_id": "0001628280-26-050481:facts:AssetsCurrent:2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_current_liabilities_balance", "what_changed": "Current liabilities 573512000 against 532769000.", "account": "total current liabilities", "expected_direction": "up", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"573512000\"", "paragraph_id": "0001628280-26-050481:facts:LiabilitiesCurrent:2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_accounts_payable_balance", "what_changed": "Accounts payable 248972000 against 211079000.", "account": "accounts payable", "expected_direction": "up", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"248972000\"", "paragraph_id": "0001628280-26-050481:facts:AccountsPayableCurrent:2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_accrued_liabilities_balance", "what_changed": "Accrued liabilities 191873000 against 199271000.", "account": "accrued liabilities", "expected_direction": "down", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"191873000\"", "paragraph_id": "0001628280-26-050481:facts:AccruedLiabilitiesCurrent:2026-06-27" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_employee_related_liabilities_balance", "what_changed": "Employee-related current liabilities 107717000 against 114662000.", "account": "accrued payroll and employee liabilities", "expected_direction": "down", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"107717000\"", "paragraph_id": "0001628280-26-050481:facts:EmployeeRelatedLiabilitiesCurrent:2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_other_accrued_liabilities_balance", "what_changed": "Other accrued current liabilities 37587000 against 29733000.", "account": "other accrued liabilities", "expected_direction": "up", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"37587000\"", "paragraph_id": "0001628280-26-050481:facts:OtherAccruedLiabilitiesCurrent:2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_restructuring_reserve_balance", "what_changed": "Current restructuring reserve 5258000 against 6014000. The noncurrent reserve is 200000 against 300000.", "account": "restructuring reserve", "expected_direction": "down", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"5258000\"", "paragraph_id": "0001628280-26-050481:facts:RestructuringReserveCurrent:2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_accrued_income_taxes_balance", "what_changed": "Accrued income taxes 32667000 against 26186000.", "account": "accrued income taxes", "expected_direction": "up", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"32667000\"", "paragraph_id": "0001628280-26-050481:facts:AccruedIncomeTaxesCurrent:2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_deferred_tax_liabilities_balance", "what_changed": "Net deferred tax liabilities 110081000 against 102335000.", "account": "deferred income tax liabilities", "expected_direction": "up", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"110081000\"", "paragraph_id": "0001628280-26-050481:facts:DeferredIncomeTaxLiabilitiesNet:2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_current_debt_balance", "what_changed": "Current portion of long-term debt 100000000 against 96233000.", "account": "current portion of long-term debt", "expected_direction": "up", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"100000000\"", "paragraph_id": "0001628280-26-050481:facts:LongTermDebtCurrent:2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_noncurrent_debt_balance", "what_changed": "Long-term debt, less current portion, 529660000 against 706394000.", "account": "long-term debt, noncurrent", "expected_direction": "down", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"529660000\"", "paragraph_id": "0001628280-26-050481:facts:LongTermDebtNoncurrent:2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_total_debt_balance", "what_changed": "Total long-term debt 629660000 against 802627000. The first-quarter 10-Q had 631532000 at 2026-03-28.", "account": "long-term debt, total", "expected_direction": "down", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"629660000\"", "paragraph_id": "0001628280-26-050481:facts:LongTermDebt:2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_total_liabilities_balance", "what_changed": "Total liabilities 1394119000 against 1530762000.", "account": "total liabilities", "expected_direction": "down", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"1394119000\"", "paragraph_id": "0001628280-26-050481:facts:Liabilities:2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_stockholders_equity_balance", "what_changed": "Stockholders' equity 2618360000 against 2426034000. Retained earnings are 1798379000 against 1671699000.", "account": "stockholders' equity", "expected_direction": "up", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"2618360000\"", "paragraph_id": "0001628280-26-050481:facts:StockholdersEquity:2026-06-27" }
```

```json
{ "id": "earnings_quality_accumulated_other_comprehensive_loss_balance", "what_changed": "Accumulated other comprehensive loss -30263000 against -5383000. The translation component is -24072000 at 2026-06-27 against -828000.", "account": "accumulated other comprehensive income (loss)", "expected_direction": "down", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"-30263000\"", "paragraph_id": "0001628280-26-050481:facts:AccumulatedOtherComprehensiveIncomeLossNetOfTax:2026-06-27" }
```

### Numeric facts — debt and credit facility

```json
{ "id": "liquidity_and_capital_line_of_credit_balance", "what_changed": "Line-of-credit carrying amount 200000000 at 2026-06-27 against 100000000 at 2025-12-27. The same 200000000 is tagged at the 2026-03-12 amendment date.", "account": "revolving line of credit drawn", "expected_direction": "up", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"200000000\"", "paragraph_id": "0001628280-26-050481:facts:DebtInstrumentCarryingAmount:2026-06-27:us-gaap:LongtermDebtTypeAxis=us-gaap:LineOfCreditMember" }
```

```json
{ "id": "liquidity_and_capital_unsecured_term_loan_balance", "what_changed": "The unsecured term loan carried 266250000 at 2025-12-27 and 0 at 2026-06-27.", "account": "unsecured term loan", "expected_direction": "down", "horizon": "2026-06-27 against 2025-12-27", "quote": "\"value\": \"266250000\"", "paragraph_id": "0001628280-26-050481:facts:DebtInstrumentCarryingAmount:2025-12-27:us-gaap:LongtermDebtTypeAxis=us-gaap:UnsecuredDebtMember" }
```

```json
{ "id": "liquidity_and_capital_revolver_borrowing_capacity", "what_changed": "Revolving facility maximum borrowing capacity 800000000 at the 2026-03-12 amendment, against 700000000 tagged at 2022-06-30. A 300000000 unsecured capacity fact is also tagged at 2026-03-12.", "account": "revolving credit capacity", "expected_direction": "up", "horizon": "amendment of 2026-03-12 against the 2022 facility", "quote": "\"value\": \"800000000\"", "paragraph_id": "0001628280-26-050481:facts:LineOfCreditFacilityMaximumBorrowingCapacity:2026-03-12:us-gaap:CreditFacilityAxis=us-gaap:RevolvingCreditFacilityMember,us-gaap:LongtermDebtTypeAxis=us-gaap:UnsecuredDebtMember" }
```

```json
{ "id": "liquidity_and_capital_revolver_remaining_capacity", "what_changed": "Remaining line-of-credit borrowing capacity 599900000 at 2026-06-27. No earlier remaining-capacity fact in this filing to compare.", "account": "undrawn revolving capacity", "expected_direction": "none", "horizon": "2026-06-27", "quote": "\"value\": \"599900000\"", "paragraph_id": "0001628280-26-050481:facts:LineOfCreditFacilityRemainingBorrowingCapacity:2026-06-27:us-gaap:LongtermDebtTypeAxis=us-gaap:LineOfCreditMember" }
```

### Numeric facts — segments, products and geography, quarter ended 2026-06-27

```json
{ "id": "narrative_signs_of_operating_pressure_transportation_segment_operating_income", "what_changed": "Transportation segment operating income 25691000 against 28074000, while Transportation sales were 182411000 against 179400000.", "account": "Transportation segment operating income", "expected_direction": "down", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"25691000\"", "paragraph_id": "0001628280-26-050481:facts:OperatingIncomeLoss:2026-03-29..2026-06-27:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=lfus:TransportationSegmentMember" }
```

```json
{ "id": "results_against_expectations_electronics_segment_operating_income", "what_changed": "Electronics segment operating income 86916000 against 49861000.", "account": "Electronics segment operating income", "expected_direction": "up", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"86916000\"", "paragraph_id": "0001628280-26-050481:facts:OperatingIncomeLoss:2026-03-29..2026-06-27:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=lfus:ElectronicsSegmentMember" }
```

```json
{ "id": "results_against_expectations_industrial_segment_operating_income", "what_changed": "Industrial segment operating income 27474000 against 18863000.", "account": "Industrial segment operating income", "expected_direction": "up", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"27474000\"", "paragraph_id": "0001628280-26-050481:facts:OperatingIncomeLoss:2026-03-29..2026-06-27:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=lfus:IndustrialSegmentMember" }
```

```json
{ "id": "earnings_quality_corporate_unallocated_operating_loss_quarter", "what_changed": "Corporate, non-segment operating loss -20357000 against -4020000. For the six months: -34335000 against -12627000.", "account": "corporate and other operating loss", "expected_direction": "down", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"-20357000\"", "paragraph_id": "0001628280-26-050481:facts:OperatingIncomeLoss:2026-03-29..2026-06-27:srt:ConsolidationItemsAxis=us-gaap:CorporateNonSegmentMember" }
```

```json
{ "id": "results_against_expectations_electronics_segment_sales", "what_changed": "Electronics segment sales 406420000 against 335666000.", "account": "Electronics segment revenue", "expected_direction": "up", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"406420000\"", "paragraph_id": "0001628280-26-050481:facts:RevenueFromContractWithCustomerIncludingAssessedTax:2026-03-29..2026-06-27:us-gaap:StatementBusinessSegmentsAxis=lfus:ElectronicsSegmentMember" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_transportation_segment_sales", "what_changed": "Transportation segment sales 182411000 against 179400000.", "account": "Transportation segment revenue", "expected_direction": "up", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"182411000\"", "paragraph_id": "0001628280-26-050481:facts:RevenueFromContractWithCustomerIncludingAssessedTax:2026-03-29..2026-06-27:us-gaap:StatementBusinessSegmentsAxis=lfus:TransportationSegmentMember" }
```

```json
{ "id": "structure_and_disclosure_changes_industrial_segment_sales_with_acquisition", "what_changed": "Industrial segment sales 149950000 against 98347000. The segment includes the Basler acquisition closed 2025-12-11.", "account": "Industrial segment revenue", "expected_direction": "up", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"149950000\"", "paragraph_id": "0001628280-26-050481:facts:RevenueFromContractWithCustomerIncludingAssessedTax:2026-03-29..2026-06-27:us-gaap:StatementBusinessSegmentsAxis=lfus:IndustrialSegmentMember" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_auto_sensor_sales", "what_changed": "Automotive sensor product sales 15294000 against 16989000. For the six months: 30554000 against 32047000.", "account": "automotive sensor revenue", "expected_direction": "down", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"15294000\"", "paragraph_id": "0001628280-26-050481:facts:RevenueFromContractWithCustomerIncludingAssessedTax:2026-03-29..2026-06-27:srt:ProductOrServiceAxis=lfus:AutomotiveSensorsMember" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_passenger_car_sales", "what_changed": "Passenger car product sales 76500000 against 76151000.", "account": "passenger car product revenue", "expected_direction": "up", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"76500000\"", "paragraph_id": "0001628280-26-050481:facts:RevenueFromContractWithCustomerIncludingAssessedTax:2026-03-29..2026-06-27:srt:ProductOrServiceAxis=lfus:PassengerCarProductsMember" }
```

```json
{ "id": "results_against_expectations_commercial_vehicle_sales", "what_changed": "Commercial vehicle product sales 90617000 against 86260000.", "account": "commercial vehicle product revenue", "expected_direction": "up", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"90617000\"", "paragraph_id": "0001628280-26-050481:facts:RevenueFromContractWithCustomerIncludingAssessedTax:2026-03-29..2026-06-27:srt:ProductOrServiceAxis=lfus:CommercialVehicleProductsMember" }
```

```json
{ "id": "results_against_expectations_china_sales", "what_changed": "China sales 184067000 against 146343000. US sales 267404000 against 219480000. Other countries 287310000 against 247590000.", "account": "revenue by geography", "expected_direction": "up", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"184067000\"", "paragraph_id": "0001628280-26-050481:facts:RevenueFromContractWithCustomerIncludingAssessedTax:2026-03-29..2026-06-27:srt:StatementGeographicalAxis=country:CN" }
```

### Numeric facts — restructuring and impairment detail

```json
{ "id": "earnings_quality_restructuring_charges_quarter", "what_changed": "Restructuring charges 6875000 against 2506000. Severance is 5207000 of the quarter. For the six months: 14297000.", "account": "restructuring charges", "expected_direction": "up", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"6875000\"", "paragraph_id": "0001628280-26-050481:facts:RestructuringCharges:2026-03-29..2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_long_lived_asset_impairment_quarter", "what_changed": "Impairment of long-lived assets held for use 13100000 in the quarter. A year earlier the other-asset impairment for the quarter was 0.", "account": "long-lived asset impairment", "expected_direction": "up", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "\"value\": \"13100000\"", "paragraph_id": "0001628280-26-050481:facts:ImpairmentOfLongLivedAssetsHeldForUse:2026-03-29..2026-06-27:us-gaap:DisposalGroupClassificationAxis=us-gaap:DisposalGroupNotDiscontinuedOperationsMember" }
```

```json
{ "id": "estimates_and_discretion_electronics_asset_impairment_quarter", "what_changed": "Other asset impairment in Electronics 12898000 of the 13146000 total for the quarter. Transportation 248000, Industrial 0.", "account": "Electronics asset impairment", "expected_direction": "up", "horizon": "quarter ended 2026-06-27", "quote": "\"value\": \"12898000\"", "paragraph_id": "0001628280-26-050481:facts:OtherAssetImpairmentCharges:2026-03-29..2026-06-27:us-gaap:StatementBusinessSegmentsAxis=lfus:ElectronicsSegmentMember" }
```

```json
{ "id": "structure_and_disclosure_changes_goodwill_acquired_tag_for_measurement_adjustment", "what_changed": "The goodwill roll-forward tags 8634000 as goodwill acquired during the six months in Industrial. No acquisition closed in the period. The Basler note tags 8600000 as a purchase-accounting adjustment.", "account": "goodwill acquired during period", "expected_direction": "up", "horizon": "six months ended 2026-06-27", "quote": "\"value\": \"8634000\"", "paragraph_id": "0001628280-26-050481:facts:GoodwillAcquiredDuringPeriod:2025-12-28..2026-06-27:us-gaap:StatementBusinessSegmentsAxis=lfus:IndustrialSegmentMember" }
```

### Numeric facts — related parties, contingencies and subsequent events

```json
{ "id": "related_parties_contingencies_and_subsequent_events_atec_purchases_six_months", "what_changed": "Purchases from related party ATEC 5000000.0 in the six months. The first-quarter 10-Q tagged 4200000 for its quarter. The fiscal 2025 10-K tagged 9000000.0 for the year.", "account": "related-party purchases (ATEC)", "expected_direction": "none", "horizon": "six months ended 2026-06-27", "quote": "\"value\": \"5000000.0\"", "paragraph_id": "0001628280-26-050481:facts:RelatedPartyTransactionPurchasesFromRelatedParty:2025-12-28..2026-06-27:srt:CounterpartyNameAxis=lfus:ATECMember,us-gaap:RelatedPartyTransactionsByRelatedPartyAxis=us-gaap:RelatedPartyMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_pension_expense_forecast", "what_changed": "A forecast subsequent-event pension expense of 6000000 (minimum) to 8000000 (maximum) is tagged for 2026-12-27..2027-03-31.", "account": "pension expense", "expected_direction": "up", "horizon": "quarter beginning 2026-12-27", "quote": "\"value\": \"6000000\"", "paragraph_id": "0001628280-26-050481:facts:PensionExpense:2026-12-27..2027-03-31:srt:RangeAxis=srt:MinimumMember,srt:StatementScenarioAxis=srt:ScenarioForecastMember,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

### Numeric facts — fiscal 2025 10-K (0001628280-26-009585)

```json
{ "id": "estimates_and_discretion_annual_effective_tax_rate", "what_changed": "The 10-K tags an effective income tax rate of 20.878 for fiscal 2025, a year with net loss -71700000.", "account": "annual effective tax rate", "expected_direction": "none", "horizon": "fiscal 2025", "quote": "\"value\": \"20.878\"", "paragraph_id": "0001628280-26-009585:facts:EffectiveIncomeTaxRateContinuingOperations:2024-12-29..2025-12-27" }
```

```json
{ "id": "estimates_and_discretion_germany_valuation_allowance_change", "what_changed": "The tax rate reconciliation tags a change in the deferred-tax-asset valuation allowance for Germany of 26839000 in fiscal 2025.", "account": "valuation allowance, Germany", "expected_direction": "up", "horizon": "fiscal 2025", "quote": "\"value\": \"26839000\"", "paragraph_id": "0001628280-26-009585:facts:IncomeTaxReconciliationChangeInDeferredTaxAssetsValuationAllowance:2024-12-29..2025-12-27:us-gaap:IncomeTaxAuthorityAxis=country:DE" }
```

```json
{ "id": "estimates_and_discretion_deferred_tax_valuation_allowance_year_end", "what_changed": "Deferred tax asset valuation allowance 97557000 at 2025-12-27, against 55468000 at 2024-12-28 in the same 10-K.", "account": "deferred tax asset valuation allowance", "expected_direction": "up", "horizon": "2025-12-27 against 2024-12-28", "quote": "\"value\": \"97557000\"", "paragraph_id": "0001628280-26-009585:facts:DeferredTaxAssetsValuationAllowance:2025-12-27" }
```

```json
{ "id": "earnings_quality_corporate_unallocated_operating_loss_year", "what_changed": "Corporate, non-segment operating loss -326341000 in fiscal 2025, against -112022000 in fiscal 2024 and -28153000 in fiscal 2023.", "account": "corporate and other operating loss", "expected_direction": "down", "horizon": "fiscal 2025 against fiscal 2024", "quote": "\"value\": \"-326341000\"", "paragraph_id": "0001628280-26-009585:facts:OperatingIncomeLoss:2024-12-29..2025-12-27:srt:ConsolidationItemsAxis=us-gaap:CorporateNonSegmentMember" }
```

```json
{ "id": "estimates_and_discretion_asset_impairment_charges_year", "what_changed": "Asset impairment charges tagged 302100000 for fiscal 2025. The 10-K also carries goodwill impairment of 301185000. The 8-K's trailing-twelve-month EBITDA adds back impairment charges of 315.1 (millions).", "account": "asset impairment charges", "expected_direction": "up", "horizon": "fiscal 2025", "quote": "\"value\": \"302100000\"", "paragraph_id": "0001628280-26-009585:facts:AssetImpairmentCharges:2024-12-29..2025-12-27" }
```

```json
{ "id": "revenue_recognition_sales_discounts_and_allowances_reserve", "what_changed": "The Schedule II reserve for sales discounts and allowances is 74553000 at 2025-12-27, against 68401000 a year earlier. Charges to the reserve were 168821000 against 138735000.", "account": "sales discounts and allowances reserve", "expected_direction": "up", "horizon": "2025-12-27 against 2024-12-28", "quote": "\"value\": \"74553000\"", "paragraph_id": "0001628280-26-009585:facts:ValuationAllowancesAndReservesBalance:2025-12-27:us-gaap:ValuationAllowancesAndReservesTypeAxis=lfus:SECSchedule1209ReserveSalesDiscountsandAllowancesMember" }
```

### Earnings release figures checked against the filed facts (8-K 0001628280-26-050382)

```json
{ "id": "across_documents_release_net_sales_matches_filed_revenue", "what_changed": "The release's $739 million net sales matches the 10-Q fact 738781000. The release's statement of operations prints 738,781. No difference is printed between the two documents.", "account": "revenue", "expected_direction": "up", "horizon": "quarter ended 2026-06-27", "quote": "Net sales of $739 million, +20%; organic growth contributed +14%", "paragraph_id": "0001628280-26-050382:8k_2_02:8" }
```

```json
{ "id": "liquidity_and_capital_credit_agreement_amended_add_backs", "what_changed": "The release states the credit agreement was amended in the first quarter of 2026 to allow restructuring and business-optimization add-backs in covenant EBITDA. This coincides with the revolver capacity rising to 800000000 at 2026-03-12.", "account": "covenant definition of consolidated EBITDA", "expected_direction": "none", "horizon": "from the first quarter of 2026", "quote": "The Credit Agreement was amended in Q1 2026 and now allows to add restructuring charges and business optimization expenses in addition to the prior credit agreement.", "paragraph_id": "0001628280-26-050382:8k_2_02:84" }
```

```json
{ "id": "liquidity_and_capital_net_leverage_covenant_ratio", "what_changed": "Consolidated net leverage ratio 0.8x for the twelve months ended 2026-06-27, against a covenant trigger above 3.50:1.00 (paragraph 83). The twelve-month consolidated EBITDA is 623.9.", "account": "consolidated net leverage ratio", "expected_direction": "none", "horizon": "twelve months ended 2026-06-27", "quote": "Consolidated Net Leverage Ratio (as defined in the Credit Agreement) * |  | 0.8x", "paragraph_id": "0001628280-26-050382:8k_2_02:82" }
```

```json
{ "id": "earnings_quality_trailing_impairment_addback", "what_changed": "The release's trailing-twelve-month consolidated EBITDA starts from a net loss of (8.2) and adds back impairment charges of 315.1 (millions).", "account": "impairment charges in covenant EBITDA", "expected_direction": "none", "horizon": "twelve months ended 2026-06-27", "quote": "Impairment charges |  | 315.1", "paragraph_id": "0001628280-26-050382:8k_2_02:82" }
```

```json
{ "id": "earnings_quality_indemnification_receivable_reversal", "what_changed": "A $2.7 million indemnification receivable was reversed in the first quarter of 2026 in other income. It is offset by $2.7 million of tax benefits from statute-of-limitation lapses (paragraph 91). Both are excluded from adjusted results.", "account": "other income and income tax", "expected_direction": "none", "horizon": "first quarter of 2026", "quote": "2026 included the reversal of an indemnification receivable of $2.7 million related to lapses in the statute of limitations for previously unrecognized tax benefits recognized in the first quarter of 2026.", "paragraph_id": "0001628280-26-050382:8k_2_02:90" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_transportation_margin_decline", "what_changed": "The release reports Transportation adjusted EBITDA margin down to 18.6% (-190 bps). This matches the filed segment operating income 25691000 against 28074000.", "account": "Transportation segment margin", "expected_direction": "down", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "Adjusted EBITDA margin for the second quarter 2026 decreased to 18.6% (-190 bps) driven by lower commercial vehicle profitability which more than offset passenger vehicle margin expansion.", "paragraph_id": "0001628280-26-050382:8k_2_02:28" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_passenger_vehicle_and_auto_sensor_decline", "what_changed": "The release attributes the weaker passenger vehicle sales to lower global builds and auto sensor declines. This matches the filed automotive sensor sales of 15294000 against 16989000.", "account": "passenger vehicle and auto sensor revenue", "expected_direction": "down", "horizon": "quarter ended 2026-06-27 against quarter ended 2025-06-28", "quote": "Passenger vehicle sales were impacted by lower global passenger car builds and auto sensor product declines.", "paragraph_id": "0001628280-26-050382:8k_2_02:27" }
```

```json
{ "id": "results_against_expectations_third_quarter_sales_guidance", "what_changed": "Third-quarter 2026 net sales guidance of $780 - $800 million, with adjusted diluted EPS of $4.85 – $5.05, against second-quarter filed net sales of 738781000.", "account": "revenue guidance", "expected_direction": "up", "horizon": "quarter ending in September 2026", "quote": "Net sales in the range of $780 - $800 million", "paragraph_id": "0001628280-26-050382:8k_2_02:19" }
```

## Seen in the notes

No items. The instructions say every fact is marked with whether its element sat inside a note when it was extracted, but no fact row in input_numbers.json carries such a marker. Every row prints only id, paragraph_id, tag, prefix, namespace, context, context_ref, unit, decimals, value, number, nil, form, source_accession, filing_date and, on some rows, superseded_by.

With no marker, this reader has not judged which facts came from note tables. All fact items, including the segment, product, geography, restructuring, Basler, debt, related-party, pension and tax-note facts, are listed under "Seen in the statements" above. A later notes reader will need the marker added to the input before this split can be made without re-deriving it.
