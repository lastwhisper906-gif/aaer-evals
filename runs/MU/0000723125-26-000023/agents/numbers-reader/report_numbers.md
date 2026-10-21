# MU — numbers reader — 10-K 0000723125-26-000023 (fiscal year ended 2026-09-03)

## Scope and what my input does not hold

- **quarters-back-0 is not reached.** The trend table holds no cells for it. Its reason, as printed: "no quarter ending within 20 days of 2026-09-03 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py". The same reason is given for quarters-back-4 (target 2025-09-04).
- **Inputs that do not exist in my directory.** There is no fourth-quarter derivation output, no articulation checks and no restatement traces. So no fourth-quarter ratio, no articulation gap and no restated prior value exists for me to report. I have not derived any of them.
- **Changes of tag.** The trend table says a period rests on a different concept only for contract liabilities. Both places are itemized below.
- **Formula baseline without a paragraph_id.** The R&D-capitalization baseline (life_years 5) prints values for each year: for years-back-0, earnings_with_rnd_capitalized 87394800000.0 and book_value_with_rnd_capitalized 150993200000.0. capitalized_development_cost is missing because no us-gaap:CapitalizedComputerSoftwareAdditions is tagged in any period. The block prints no paragraph_id, so it is not itemized.
- **Facts I read.** input_numbers.json has 80,043 lines of raw XBRL facts from three filings: 10-Q 0000723125-26-000006, 10-Q 0000723125-26-000015 and 10-K 0000723125-26-000023. That is more than fits in my context. I read its head and tail, and the 10-K's balance sheet and its receivables, inventory, PP&E, capitalized-interest, government-assistance, revenue, tax, segment-goodwill, concentration and geography facts. I did not read every 10-Q fact.
- **Not quotable.** The 8-K item-code index and the late-filing line ("none on or before 2026-10-09") print no id, so they are not itemized.
- **Prior flags.** input_prior_predictions.md says none are on record.
- **Material I must never see.** There are no prices, returns, short interest, other companies' files, prior probabilities or outcome windows in my directory.
- **How `expected_direction` is used.** It records the sign of the change Python printed for the metric over the stated horizon. For the one prose item, it records the direction the company itself states. It is `none` wherever no change is printed. It is not a price forecast.

## Seen in the statements

### Trend table, years-back-0 (2025-08-29..2026-09-03)

```json
{ "id": "earnings_quality_accruals_over_total_assets",
  "what_changed": "Accruals over total assets, formula (net_income - operating_cash_flow) / assets, is -0.024023932042799966. Change against years-back-1 is 0.0845052594835654 (years-back-1 value -0.10852919152636537). Position in the filed history: highest of the 5 filled years. Inputs as printed: net_income 84969000000.0, operating_cash_flow 89675000000.0, assets 195888000000.0. The value is negative, so net income is below operating cash flow under this formula.",
  "account": "accruals: net income less operating cash flow, over total assets",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2026-09-03 against fiscal year ended 2025-08-28",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000723125-26-000023:trends:accruals_over_total_assets:2025-08-29..2026-09-03" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio",
  "what_changed": "insufficient. The bad-debt reserve ratio could not be filled for the year. The allowance concepts are in the record, but not for 2026-09-03. The coverage block prints \"filled\": 0 for this ratio, so it is unfilled in every period: no value, no change, no history.",
  "account": "allowance for credit losses on receivables",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2026-09-03",
  "quote": "\"missing\": \"no row for bad_debt_allowance in 2026-09-03: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"",
  "paragraph_id": "0000723125-26-000023:trends:bad_debt_reserve_ratio:2025-08-29..2026-09-03" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue",
  "what_changed": "Contract liabilities over revenue, formula contract_liabilities / revenue, is 0.0976063909661531. No change is printed: years-back-1 rests on a different concept. Position: the only filled year on the same concepts; 2 other filled years rest on a different concept and are not compared. Inputs as printed: contract_liabilities (ContractWithCustomerLiability at 2026-09-03) 13000000000.0, revenue 133188000000.0. One year on this concept supports no trend: insufficient for a trend claim.",
  "account": "contract liabilities against revenue",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2026-09-03",
  "quote": "\"position_in_history\": \"the only filled year on the same concepts; 2 other filled years rest on a different concept and are not compared\"",
  "paragraph_id": "0000723125-26-000023:trends:contract_liabilities_over_revenue:2025-08-29..2026-09-03" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory",
  "what_changed": "Days sales of inventory, formula inventory / cost_of_revenue * days_in_period (371 days), is 149.82136738825727. Change against years-back-1 is 14.686064122316367 (years-back-1 value 135.1353032659409). Position: third highest of the 5 filled years. Inputs as printed: inventory (InventoryNet at 2026-09-03) 10372000000.0, cost_of_revenue 25684000000.0.",
  "account": "inventories against cost of goods sold",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2026-09-03 against fiscal year ended 2025-08-28",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0000723125-26-000023:trends:days_sales_of_inventory:2025-08-29..2026-09-03" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding",
  "what_changed": "Days sales outstanding, formula receivables / revenue * days_in_period (371 days), is 88.56055350331862. Change against years-back-1 is 18.804761326102067 (years-back-1 value 69.75579217721655). Position: highest of the 5 filled years. Inputs as printed: receivables (AccountsReceivableNetCurrent at 2026-09-03) 31793000000.0, revenue 133188000000.0. The formula sets a year-end balance against a full year's revenue. No fourth-quarter DSO exists in my input, because quarters-back-0 is not reached.",
  "account": "trade receivables against revenue",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2026-09-03 against fiscal year ended 2025-08-28",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000723125-26-000023:trends:days_sales_outstanding:2025-08-29..2026-09-03" }
```

```json
{ "id": "earnings_quality_gross_margin",
  "what_changed": "Gross margin, formula (revenue - cost_of_revenue) / revenue, is 0.8071598041865633. Change against years-back-1 is 0.40925194394792025 (years-back-1 value 0.39790786023864305). Position: highest of the 5 filled years. Inputs as printed: revenue 133188000000.0, cost_of_revenue 25684000000.0.",
  "account": "gross margin",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2026-09-03 against fiscal year ended 2025-08-28",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000723125-26-000023:trends:gross_margin:2025-08-29..2026-09-03" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio",
  "what_changed": "insufficient. The inventory reserve ratio could not be filled for the year: the record tags no us-gaap:InventoryValuationReserves in any period, and the coverage block prints \"filled\": 0 for this ratio. The record cannot say whether the concept is untagged or stated only by segment. See estimates_and_discretion_inventory_components_net_of_reserves.",
  "account": "inventory valuation reserve",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2026-09-03",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0000723125-26-000023:trends:inventory_reserve_ratio:2025-08-29..2026-09-03" }
```

```json
{ "id": "earnings_quality_non_gaap_gap",
  "what_changed": "insufficient. The non-GAAP gap could not be filled for the year: companyfacts holds only us-gaap and dei facts. The coverage block prints \"filled\": 0 for this ratio. The release prints non-GAAP net income (across_documents_non_gaap_net_income_in_release), but no computed gap exists in my input.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2026-09-03",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0000723125-26-000023:trends:non_gaap_gap:2025-08-29..2026-09-03" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue",
  "what_changed": "Receivables over revenue, formula receivables / revenue, is 0.23870769138360814. Change against years-back-1 is 0.0470708996879583 (years-back-1 value 0.19163679169564984). Position: highest of the 5 filled years. Inputs as printed: receivables (AccountsReceivableNetCurrent at 2026-09-03) 31793000000.0, revenue 133188000000.0.",
  "account": "trade receivables against revenue",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2026-09-03 against fiscal year ended 2025-08-28",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000723125-26-000023:trends:receivables_over_revenue:2025-08-29..2026-09-03" }
```

```json
{ "id": "earnings_quality_soft_asset_share",
  "what_changed": "Soft-asset share, formula (assets - property_plant_and_equipment - cash) / assets, is 0.4809585069019031. Change against years-back-1 is 0.1601053461975383 (years-back-1 value 0.3208531607043648). Position: highest of the 5 filled years. Inputs as printed: assets 195888000000.0, property_plant_and_equipment 63310000000.0, cash (CashAndCashEquivalentsAtCarryingValue) 38364000000.0. The formula removes only cash and PP&E. The 10-K tags AvailableForSaleSecuritiesDebtSecuritiesCurrent 5070000000 and AvailableForSaleSecuritiesDebtSecuritiesNoncurrent 30019000000 at 2026-09-03, and this formula counts them as soft assets.",
  "account": "assets other than cash and PP&E, over total assets",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2026-09-03 against fiscal year ended 2025-08-28",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000723125-26-000023:trends:soft_asset_share:2025-08-29..2026-09-03" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio",
  "what_changed": "insufficient. The warranty reserve ratio could not be filled for the year: the record tags none of the three warranty-accrual concepts in any period, and the coverage block prints \"filled\": 0 for this ratio. The record cannot say whether the concept is untagged or stated only by segment.",
  "account": "product warranty accrual",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2026-09-03",
  "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0000723125-26-000023:trends:warranty_reserve_ratio:2025-08-29..2026-09-03" }
```

### Changes of tag

```json
{ "id": "structure_and_disclosure_changes_contract_liability_concept_switch",
  "what_changed": "Change of tag in the annual series. The contract-liability input is us-gaap:ContractWithCustomerLiability in years-back-0 and us-gaap:ContractWithCustomerLiabilityCurrent in years-back-1, so no year-over-year change is printed. The older cells say the same from their side: years-back-1 (value 0.0006955963400931029, ContractWithCustomerLiabilityCurrent 26000000.0 at 2025-08-28) and years-back-2 (value 0.03050455975468918, 766000000.0 at 2024-08-29) each say 1 other filled year rests on a different concept. Years-back-3 and years-back-4 have no contract-liability row.",
  "account": "contract liabilities",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2026-09-03 against fiscal year ended 2025-08-28",
  "quote": "\"reason\": \"contract_liabilities_over_revenue rests on a different concept in each period, so the difference would not be a change",
  "paragraph_id": "0000723125-26-000023:trends:contract_liabilities_over_revenue:2025-08-29..2026-09-03" }
```

```json
{ "id": "structure_and_disclosure_changes_contract_liability_concept_switch_quarterly",
  "what_changed": "The same change of tag in the quarterly series. The input is us-gaap:ContractWithCustomerLiability in quarters-back-1 (422000000.0 at 2026-05-28; ratio 0.010179467387109224) and us-gaap:ContractWithCustomerLiabilityCurrent in quarters-back-5, so no year-over-year change is printed. Quarters-back-1 is the only filled quarter on its concept; 3 other filled quarters rest on a different concept. Quarters-back-5 (3000000.0), quarters-back-6 (413000000.0) and quarters-back-7 (473000000.0) each say 1 other filled quarter rests on a different concept. Quarters-back-2 and quarters-back-3 have no contract-liability row.",
  "account": "contract liabilities",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-05-28 against quarter ended 2025-05-29",
  "quote": "\"reason\": \"contract_liabilities_over_revenue rests on a different concept in each period, so the difference would not be a change",
  "paragraph_id": "0000723125-26-000023:trends:contract_liabilities_over_revenue:2026-02-27..2026-05-28" }
```

### Numeric facts (10-K 0000723125-26-000023)

```json
{ "id": "structure_and_disclosure_changes_noncurrent_contract_liability_outside_ratio_concepts",
  "what_changed": "The 10-K balance sheet tags ContractWithCustomerLiabilityNoncurrent: 12895000000 at 2026-09-03 and 142000000 at 2025-08-28. The trend table searches only four contract-liability concepts (ContractWithCustomerLiabilityCurrent, ContractWithCustomerLiability, DeferredRevenueCurrent, DeferredRevenue), and this is not one of them. So the years-back-1 input is ContractWithCustomerLiabilityCurrent 26000000.0 alone, while years-back-0 uses ContractWithCustomerLiability 13000000000 (decimals -9). This is the change of tag above, seen from the balance sheet.",
  "account": "noncurrent contract liabilities",
  "expected_direction": "none",
  "horizon": "balance at 2026-09-03 against 2025-08-28",
  "quote": "\"value\": \"142000000\"",
  "paragraph_id": "0000723125-26-000023:facts:ContractWithCustomerLiabilityNoncurrent:2025-08-28" }
```

```json
{ "id": "revenue_recognition_receivables_tagged_components",
  "what_changed": "The 10-K tags the balance-sheet receivables line as ReceivablesNetCurrent: 36197000000 at 2026-09-03 and 9265000000 at 2025-08-28. Its tagged components, as printed (2026-09-03 / 2025-08-28): AccountsReceivableNetCurrent 31793000000 / 7163000000; GovernmentAssistanceAmountCumulativeCurrent 3319000000 / 1572000000; IncomeTaxesReceivable 635000000 / 436000000; OtherReceivablesNetCurrent 450000000 / 94000000. The trend table's DSO and receivables-over-revenue use AccountsReceivableNetCurrent only. No allowance amount is tagged for 2026-09-03 (see estimates_and_discretion_bad_debt_reserve_ratio).",
  "account": "receivables",
  "expected_direction": "none",
  "horizon": "balance at 2026-09-03 against 2025-08-28",
  "quote": "\"value\": \"36197000000\"",
  "paragraph_id": "0000723125-26-000023:facts:ReceivablesNetCurrent:2026-09-03" }
```

```json
{ "id": "revenue_recognition_remaining_performance_obligation_tagged",
  "what_changed": "The 10-K tags RevenueRemainingPerformanceObligation of 134000000000 at 2026-09-03 (decimals -9). Fiscal 2026 revenue is tagged 133188000000. No earlier-period remaining-performance-obligation fact sits beside it in the facts I read: one period, insufficient for a trend.",
  "account": "remaining performance obligations",
  "expected_direction": "none",
  "horizon": "balance at 2026-09-03",
  "quote": "\"value\": \"134000000000\"",
  "paragraph_id": "0000723125-26-000023:facts:RevenueRemainingPerformanceObligation:2026-09-03" }
```

```json
{ "id": "revenue_recognition_refund_liability_tagged",
  "what_changed": "The 10-K tags ContractWithCustomerRefundLiabilityCurrent of 4320000000 at 2026-09-03, against 1190000000 at 2025-08-28 (paragraph 0000723125-26-000023:facts:ContractWithCustomerRefundLiabilityCurrent:2025-08-28), both at decimals -7. Two periods only: insufficient for a trend. No ratio of this liability to revenue exists in my input.",
  "account": "refund liabilities to customers",
  "expected_direction": "none",
  "horizon": "balance at 2026-09-03 against 2025-08-28",
  "quote": "\"value\": \"4320000000\"",
  "paragraph_id": "0000723125-26-000023:facts:ContractWithCustomerRefundLiabilityCurrent:2026-09-03" }
```

```json
{ "id": "revenue_recognition_customer_concentration_tagged",
  "what_changed": "The 10-K tags ConcentrationRiskPercentage1 for an undisclosed customer's share of revenue: 0.17 for fiscal 2025 and 0.10 for fiscal 2024. No fiscal 2026 value for this customer sits beside these facts in my input. Fiscal 2026: insufficient.",
  "account": "customer concentration of revenue",
  "expected_direction": "none",
  "horizon": "fiscal years ended 2025-08-28 and 2024-08-29",
  "quote": "\"value\": \"0.17\"",
  "paragraph_id": "0000723125-26-000023:facts:ConcentrationRiskPercentage1:2024-08-30..2025-08-28:srt:MajorCustomersAxis=mu:UndisclosedCustomerMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:RevenueFromContractWithCustomerMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember" }
```

```json
{ "id": "estimates_and_discretion_inventory_components_net_of_reserves",
  "what_changed": "The 10-K tags inventory components net of reserves (2026-09-03 / 2025-08-28): InventoryWorkInProcessNetOfReserves 8252000000 / 6401000000; InventoryFinishedGoodsNetOfReserves 958000000 / 1094000000; InventoryRawMaterialsAndSuppliesNetOfReserves 1162000000 / 860000000; InventoryNet 10372000000 / 8355000000. No reserve amount is tagged, consistent with inventory_reserve_ratio being unfilled. Two periods: insufficient for a trend.",
  "account": "inventories by stage",
  "expected_direction": "none",
  "horizon": "balance at 2026-09-03 against 2025-08-28",
  "quote": "\"value\": \"8252000000\"",
  "paragraph_id": "0000723125-26-000023:facts:InventoryWorkInProcessNetOfReserves:2026-09-03" }
```

```json
{ "id": "estimates_and_discretion_equipment_not_placed_in_service",
  "what_changed": "Gross PP&E in the 10-K includes equipment not placed into service of 6120000000 at 2026-09-03, against 4050000000.00 at 2025-08-28 (decimals -7). Construction in progress is 11424000000 against 5518000000. Depreciation is tagged 9420000000 for fiscal 2026, 8280000000 for fiscal 2025 and 7700000000 for fiscal 2024. My input does not say when the equipment enters service.",
  "account": "property, plant and equipment not yet in service",
  "expected_direction": "none",
  "horizon": "balance at 2026-09-03 against 2025-08-28",
  "quote": "\"value\": \"6120000000\"",
  "paragraph_id": "0000723125-26-000023:facts:PropertyPlantAndEquipmentAndFinanceLeaseRightOfUseAssetBeforeAccumulatedDepreciationAndAmortization:2026-09-03:us-gaap:PropertyPlantAndEquipmentByTypeAxis=mu:EquipmentnotplacedintoserviceMember" }
```

```json
{ "id": "earnings_quality_interest_costs_capitalized_tagged",
  "what_changed": "The 10-K tags InterestCostsCapitalized of 383000000 for fiscal 2026, 321000000 for fiscal 2025 and 225000000 for fiscal 2024. The release income statement prints interest expense as — for the third and fourth quarters of fiscal 2026 and (106) for the year. No quarterly split of capitalized interest exists in my input.",
  "account": "capitalized interest",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2026-09-03 against the two prior fiscal years",
  "quote": "\"value\": \"383000000\"",
  "paragraph_id": "0000723125-26-000023:facts:InterestCostsCapitalized:2025-08-29..2026-09-03" }
```

```json
{ "id": "estimates_and_discretion_government_incentive_receivable",
  "what_changed": "Within current receivables, the 10-K tags GovernmentAssistanceAmountCumulativeCurrent of 3319000000 at 2026-09-03, against 1572000000 at 2025-08-28. GovernmentAssistanceAmountCumulativeNoncurrent is tagged 914000000 at 2025-08-28. GovernmentAssistanceLiabilityNoncurrent is 786000000 against 1018000000. CHIPS direct-funding award amounts tagged at 2026-09-03 are 6100000000 (Boise ID and Clay NY), 275000000 (Manassas VA) and 6400000000 (CHIPS direct funding). Two periods: insufficient for a trend.",
  "account": "government incentives receivable",
  "expected_direction": "none",
  "horizon": "balance at 2026-09-03 against 2025-08-28",
  "quote": "\"value\": \"3319000000\"",
  "paragraph_id": "0000723125-26-000023:facts:GovernmentAssistanceAmountCumulativeCurrent:2026-09-03" }
```

```json
{ "id": "estimates_and_discretion_equity_securities_without_readily_determinable_fair_value",
  "what_changed": "The 10-K tags EquitySecuritiesWithoutReadilyDeterminableFairValueAmount of 1300000000 at 2026-09-03, against 194000000 at 2025-08-28. The release cash flow statement prints Purchases of non-marketable equity securities of (1,046) for fiscal 2026 and (34) for fiscal 2025, in millions. Two periods: insufficient for a trend.",
  "account": "non-marketable equity securities",
  "expected_direction": "none",
  "horizon": "balance at 2026-09-03 against 2025-08-28",
  "quote": "\"value\": \"1300000000\"",
  "paragraph_id": "0000723125-26-000023:facts:EquitySecuritiesWithoutReadilyDeterminableFairValueAmount:2026-09-03" }
```

### Figures in the 8-K earnings release (0000723125-26-000018, filed 2026-09-30)

```json
{ "id": "across_documents_receivables_line_against_trade_receivables_tag",
  "what_changed": "The release balance sheet prints Receivables of 36,197 at September 3, 2026, 31,025 at May 28, 2026 and 9,265 at August 28, 2025 (millions). The 2026-09-03 and 2025-08-28 figures match the 10-K's ReceivablesNetCurrent (36197000000; 9265000000). The trend table's receivables input is a narrower concept: AccountsReceivableNetCurrent, 31793000000 at 2026-09-03 and 26894000000 at 2026-05-28. The release line and the ratio input are different concepts, not a discrepancy.",
  "account": "receivables",
  "expected_direction": "none",
  "horizon": "balance at 2026-09-03",
  "quote": "| Receivables | 36,197 |  | 31,025 |  | 9,265 |  |",
  "paragraph_id": "0000723125-26-000018:8k_2_02:60" }
```

```json
{ "id": "revenue_recognition_noncurrent_customer_contract_liabilities",
  "what_changed": "The release balance sheet prints Noncurrent customer contract liabilities of 12,895 at September 3, 2026, 568 at May 28, 2026 and 142 at August 28, 2025 (millions). The 10-K tags the 2026-09-03 and 2025-08-28 figures as ContractWithCustomerLiabilityNoncurrent (12895000000; 142000000). The trend table's input is ContractWithCustomerLiability: 13000000000 at 2026-09-03 and 422000000 at 2026-05-28. The CEO's statement in the release refers to Strategic Customer Agreements (paragraph 0000723125-26-000018:8k_2_02:20).",
  "account": "noncurrent customer contract liabilities",
  "expected_direction": "none",
  "horizon": "balance at 2026-09-03 against 2026-05-28 and 2025-08-28",
  "quote": "| Noncurrent customer contract liabilities | 12,895 |  | 568 |  | 142 |  |",
  "paragraph_id": "0000723125-26-000018:8k_2_02:60" }
```

```json
{ "id": "liquidity_and_capital_customer_contract_liability_deposits_in_financing",
  "what_changed": "The release cash flow statement prints Proceeds from customer contract liability deposits of 12,747 (millions) for fiscal 2026, under financing activities. Nothing is on that line for fiscal 2025. These deposits sit outside the operating cash flow of 89,675 that feeds the accruals ratio.",
  "account": "customer contract liability deposits (financing cash flow)",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2026-09-03 against fiscal year ended 2025-08-28",
  "quote": "| Proceeds from customer contract liability deposits | 12,747 |",
  "paragraph_id": "0000723125-26-000018:8k_2_02:66" }
```

```json
{ "id": "earnings_quality_operating_cash_flow_from_other_noncurrent_liabilities",
  "what_changed": "In the release's reconciliation of net income to operating cash flow, the change in Other noncurrent liabilities is 9,633 (millions) for fiscal 2026, against 381 for fiscal 2025. The balance sheet prints Other noncurrent liabilities of 11,659 at September 3, 2026, 7,172 at May 28, 2026 and 2,002 at August 28, 2025; the 10-K tags OtherLiabilitiesNoncurrent 11659000000 and 2002000000. My input does not say what the line holds.",
  "account": "other noncurrent liabilities",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2026-09-03 against fiscal year ended 2025-08-28",
  "quote": "| Other noncurrent liabilities | 9,633 |  | 381 |  |",
  "paragraph_id": "0000723125-26-000018:8k_2_02:66" }
```

```json
{ "id": "earnings_quality_operating_cash_flow_receivables_build",
  "what_changed": "In the release's reconciliation of net income to operating cash flow, the change in Receivables is (25,206) for fiscal 2026, against (1,776) for fiscal 2025 (millions). Other working-capital lines, fiscal 2026 then fiscal 2025: Accounts payable and accrued expenses 8,707 and 862; Other current liabilities 3,141 and (272); Inventories (2,017) and 520.",
  "account": "receivables (cash flow change)",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2026-09-03 against fiscal year ended 2025-08-28",
  "quote": "| Receivables | (25,206) |  | (1,776) |  |",
  "paragraph_id": "0000723125-26-000018:8k_2_02:66" }
```

```json
{ "id": "earnings_quality_patent_license_charges_reconciliation",
  "what_changed": "The release's non-GAAP reconciliation removes Patent license charges of 500 in the fourth quarter of fiscal 2026 and 500 for the year (millions). The third quarter of fiscal 2026 and the fourth quarter of fiscal 2025 print —; fiscal 2025 prints 57. On the income statement, Other operating (income) expense, net is 524 in the fourth quarter, 15 in the third quarter and 39 in the year-earlier quarter. The 10-K tags OtherOperatingIncomeExpenseNet -567000000 for fiscal 2026 and -100000000 for fiscal 2025.",
  "account": "patent license charges / other operating expense",
  "expected_direction": "none",
  "horizon": "fourth quarter of fiscal 2026 and fiscal year ended 2026-09-03",
  "quote": "| Patent license charges | 500 |",
  "paragraph_id": "0000723125-26-000018:8k_2_02:70" }
```

```json
{ "id": "earnings_quality_loss_on_debt_prepayments_reconciliation",
  "what_changed": "The release's non-GAAP reconciliation adds back Loss on debt prepayments, in millions: 9 (fourth quarter of fiscal 2026), 325 (third quarter), 9 (fourth quarter of fiscal 2025), 511 (fiscal 2026) and 59 (fiscal 2025).",
  "account": "loss on debt prepayments",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2026-09-03 against fiscal year ended 2025-08-28",
  "quote": "| Loss on debt prepayments | 9 |  | 325 |  | 9 |  | 511 |  | 59 |  |",
  "paragraph_id": "0000723125-26-000018:8k_2_02:70" }
```

```json
{ "id": "across_documents_non_gaap_net_income_in_release",
  "what_changed": "The release prints Non-GAAP net income, in millions: 38,398 (fourth quarter of fiscal 2026), 28,857 (third quarter), 3,469 (fourth quarter of fiscal 2025), 86,758 (fiscal 2026) and 9,470 (fiscal 2025). GAAP net income for the same columns: 37,701, 28,243, 3,201, 84,969 and 8,539. The trend table cannot fill non_gaap_gap from companyfacts, and no computed gap exists in my input.",
  "account": "non-GAAP net income",
  "expected_direction": "none",
  "horizon": "fourth quarter of fiscal 2026 and fiscal year ended 2026-09-03",
  "quote": "| Non-GAAP net income | $ | 38,398 |  | $ | 28,857 |  | $ | 3,469 |  | $ | 86,758 |  | $ | 9,470 |  |",
  "paragraph_id": "0000723125-26-000018:8k_2_02:70" }
```

```json
{ "id": "earnings_quality_gross_margin_as_percent_of_revenue",
  "what_changed": "The release prints GAAP gross margin as a percent of revenue: 86.8% for the fourth quarter of fiscal 2026, 84.6% for the third quarter and 44.7% for the fourth quarter of fiscal 2025 (non-GAAP 87.0%, 84.9%, 45.7%). The trend table holds no fourth-quarter gross margin (quarters-back-0 is not reached), so this company-printed figure is the only fourth-quarter gross margin in my input. The table's quarters-back-1 gross margin is 0.8456194519490544, the highest of the 6 filled quarters.",
  "account": "gross margin",
  "expected_direction": "none",
  "horizon": "fourth quarter of fiscal 2026",
  "quote": "| Percent of revenue | 86.8 | % | 84.6 | % | 44.7 | % |  | 87.0 | % | 84.9 | % | 45.7 | % |",
  "paragraph_id": "0000723125-26-000018:8k_2_02:21" }
```

```json
{ "id": "earnings_quality_interest_expense_not_printed",
  "what_changed": "The release income statement prints Interest expense as — for the fourth and third quarters of fiscal 2026. It prints (124) for the fourth quarter of fiscal 2025, (106) for fiscal 2026 and (477) for fiscal 2025, in millions. The balance sheet still carries Current debt of 491 and Long-term debt of 4,688 at September 3, 2026. The 10-K tags capitalized interest of 383000000 for the year (earnings_quality_interest_costs_capitalized_tagged); no quarterly split exists in my input.",
  "account": "interest expense",
  "expected_direction": "none",
  "horizon": "fourth and third quarters of fiscal 2026",
  "quote": "| Interest expense | — |  | — |  | (124) |  | (106) |  | (477) |  |",
  "paragraph_id": "0000723125-26-000018:8k_2_02:55" }
```

```json
{ "id": "liquidity_and_capital_debt_repayment_figures",
  "what_changed": "The release balance sheet prints Long-term debt of 4,688 at September 3, 2026, 5,140 at May 28, 2026 and 14,017 at August 28, 2025 (millions); the 10-K tags LongTermDebtAndCapitalLeaseObligations 4688000000 and 14017000000. The cash flow statement prints Repayments of debt of (10,043) for fiscal 2026 and (4,619) for fiscal 2025. Fiscal 2026 has no proceeds from issuance of debt; fiscal 2025 has 4,430.",
  "account": "long-term debt",
  "expected_direction": "none",
  "horizon": "balance at 2026-09-03 against 2025-08-28",
  "quote": "| Long-term debt | 4,688 |  | 5,140 |  | 14,017 |  |",
  "paragraph_id": "0000723125-26-000018:8k_2_02:60" }
```

```json
{ "id": "liquidity_and_capital_marketable_investment_purchases",
  "what_changed": "The release cash flow statement prints Purchases of available-for-sale securities of (34,871) for fiscal 2026 and (1,890) for fiscal 2025 (millions). The balance sheet prints Long-term marketable investments of 30,019, 4,106 and 1,629, and Short-term investments of 5,070, 1,027 and 665, at September 3, 2026, May 28, 2026 and August 28, 2025. Paragraph 0000723125-26-000018:8k_2_02:23 states cash, marketable investments and restricted cash of $73.48 billion at year end.",
  "account": "marketable investments",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2026-09-03 against fiscal year ended 2025-08-28",
  "quote": "| Purchases of available-for-sale securities | (34,871) |  | (1,890) |  |",
  "paragraph_id": "0000723125-26-000018:8k_2_02:66" }
```

```json
{ "id": "liquidity_and_capital_share_repurchases_figures",
  "what_changed": "The release cash flow statement prints, fiscal 2026 then fiscal 2025 (millions): Repurchases of common stock - repurchase program (650), with nothing in fiscal 2025; withholdings on employee equity awards (1,127) and (340); Payments of dividends (610) and (522). The balance sheet prints Treasury stock of (8,502) at September 3 and May 28, 2026, and (7,852) at August 28, 2025.",
  "account": "share repurchases and dividends",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2026-09-03 against fiscal year ended 2025-08-28",
  "quote": "| Repurchases of common stock - repurchase program | (650) |",
  "paragraph_id": "0000723125-26-000018:8k_2_02:66" }
```

```json
{ "id": "estimates_and_discretion_government_incentives_cash_flow",
  "what_changed": "The release cash flow statement prints Proceeds from government incentives of 3,316 for fiscal 2026 and 2,005 for fiscal 2025 (millions). The non-GAAP capex reconciliation prints 327 in the fourth quarter of fiscal 2026, 733 in the third quarter and 711 in the fourth quarter of fiscal 2025. The balance sheet prints Noncurrent unearned government incentives of 786, 1,020 and 1,018 at September 3, 2026, May 28, 2026 and August 28, 2025.",
  "account": "government incentives",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2026-09-03 against fiscal year ended 2025-08-28",
  "quote": "| Proceeds from government incentives | 3,316 |  | 2,005 |  |",
  "paragraph_id": "0000723125-26-000018:8k_2_02:66" }
```

```json
{ "id": "earnings_quality_other_noncurrent_assets",
  "what_changed": "The release balance sheet prints Other noncurrent assets of 10,339 at September 3, 2026, 5,693 at May 28, 2026 and 4,588 at August 28, 2025 (millions); the 10-K tags OtherAssetsNoncurrent 10339000000 and 4588000000. The 10-K also tags equity securities without readily determinable fair value of 1300000000 at 2026-09-03 (see estimates_and_discretion_equity_securities_without_readily_determinable_fair_value). No further breakdown is in the facts I read.",
  "account": "other noncurrent assets",
  "expected_direction": "none",
  "horizon": "balance at 2026-09-03 against 2026-05-28 and 2025-08-28",
  "quote": "| Other noncurrent assets | 10,339 |  | 5,693 |  | 4,588 |  |",
  "paragraph_id": "0000723125-26-000018:8k_2_02:60" }
```

```json
{ "id": "results_against_expectations_revenue_outlook_figures",
  "what_changed": "The release guides the first quarter of fiscal 2027: revenue $61.5 billion ± $1.5 billion (GAAP and non-GAAP), GAAP gross margin approximately 85.95%, GAAP operating expenses approximately $2.31 billion, and GAAP diluted EPS $37.84 ± $1.00 on approximately 1.15 billion diluted shares. Fourth-quarter fiscal 2026 actuals as printed: revenue 54,229 (millions) and GAAP gross margin 86.8%. No consensus or other outside expectation exists in my input.",
  "account": "revenue and margin outlook",
  "expected_direction": "none",
  "horizon": "first quarter of fiscal 2027",
  "quote": "| Revenue | $61.5 billion",
  "paragraph_id": "0000723125-26-000018:8k_2_02:28" }
```

```json
{ "id": "results_against_expectations_company_statement_of_direction",
  "what_changed": "The CEO's statement in the release gives the company's own expected direction for the coming fiscal year. It is a statement of expectation, not a figure; `up` here is the company's stated direction, not mine.",
  "account": "revenue and earnings",
  "expected_direction": "up",
  "horizon": "fiscal 2027",
  "quote": "we expect an even stronger fiscal 2027",
  "paragraph_id": "0000723125-26-000018:8k_2_02:20" }
```

## Seen in the notes

No item. The instructions say each fact carries a mark of whether its element sat inside a note. No fact in input_numbers.json carries one. Every fact prints only these fields: id, paragraph_id, tag, prefix, namespace, context, context_ref, unit, decimals, value, number, nil, form, source_accession, filing_date. The trend table carries no such mark either. Without the mark I do not judge, so every fact-based item sits under "Seen in the statements".

For a later split, these items rest on 10-K facts whose note status my input does not record:

- structure_and_disclosure_changes_noncurrent_contract_liability_outside_ratio_concepts
- revenue_recognition_receivables_tagged_components
- revenue_recognition_remaining_performance_obligation_tagged
- revenue_recognition_refund_liability_tagged
- revenue_recognition_customer_concentration_tagged
- estimates_and_discretion_inventory_components_net_of_reserves
- estimates_and_discretion_equipment_not_placed_in_service
- earnings_quality_interest_costs_capitalized_tagged
- estimates_and_discretion_government_incentive_receivable
- estimates_and_discretion_equity_securities_without_readily_determinable_fair_value
