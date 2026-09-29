Numbers reader: CARR, 10-Q 0001783180-26-000032 (filed 2026-07-28). Earnings release: 8-K 0001783180-26-000030 (filed 2026-07-28).

**Run check.** My directory holds input_8k.md, input_numbers.json, input_prior_predictions.md and input_trends.json. None of them holds prices, abnormal returns, short interest, another company's files, a prior run's probability or an outcome window. input_prior_predictions.md says: "None on record."

**A period the record does not reach.** quarters-back-0 (target end 2026-06-30) has no cells. The trend table gives this reason: "no quarter ending within 20 days of 2026-06-30 is in the companyfacts record; the companyfacts record's newest row was filed 2026-04-30, before this run's cutoff 2026-07-28 — the record was fetched before the triggering report, so the periods that report is the first to state are not in it".

So none of the eleven trend metrics exists for the quarter ended 2026-06-30. That includes receivables over revenue, DSO, the inventory, warranty and bad-debt reserve ratios, contract liabilities over revenue, accruals, soft-asset share, gross margin, DSI and the non-GAAP gap. The 10-Q facts for that quarter appear below as facts. I did not turn them into ratios.

quarters-back-2 (target end 2025-12-30) also has no cells: "no quarter ending within 20 days of 2025-12-30 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py".

**What my input does not hold:**
- **No articulation checks.** So there is no articulation gap I can report.
- **No restatement traces.** Some facts from the 10-K and the Q1 10-Q carry `superseded_by`. In every pair I compared, the later filing reports the same value. My input therefore shows no restated prior value. Without a trace I cannot certify that for rows I did not pair.
- **No fourth-quarter derivation.** The output of src/fourth_quarter.py is not in my directory.
- **No in-note marker on any fact.** No fact in input_numbers.json says whether its element sat inside a note. Every fact item therefore goes under "Seen in the statements", and "Seen in the notes" is empty (see that heading).

**Which rows I itemised:**
- **Trend periods.** I itemised years-back-0 as required. I also itemised quarters-back-1 (2026-01-01..2026-03-31), because it is the newest quarter the record reaches. Earlier periods appear only through each cell's `position_in_history`.
- **R&D-capitalisation block for years-back-0.** It prints `earnings_with_rnd_capitalized` 1605600000. Its book value is missing: "no row for stockholders_equity in 2025-12-31: us-gaap:StockholdersEquity is in the record, but not for this period". The block has no paragraph_id, so it is not an item.
- **8-K item-code list.** It shows a 5.02 filing on 2026-07-24 (0000950142-26-002161). The list of late-filing notifications reads "none on or before 2026-07-28". Neither row has a paragraph_id, so neither is an item.
- **Sources for years-back-0.** The balance-sheet inputs for 2025-12-31 come from the Q1 10-Q (0001783180-26-000026), not the 10-K. This records where each input came from and is not a restatement.

**How to read the fields:**
- **`expected_direction`.** The direction the quoted figure moved against the comparison the input itself prints. That comparison is either the change Python computed or the prior-period value filed alongside the figure. It is `none` where the input prints no comparison or the metric is insufficient. It is not a forecast.
- **`horizon`.** The next filing that will print the same figure again.

## Seen in the statements

**Trend table, years-back-0 (2025-01-01..2025-12-31)**

```json
{ "id": "earnings_quality_accruals_over_total_assets_trend", "what_changed": "Value -0.02766872815272923. Year-over-year change -0.16244401355764326 against years-back-1. No quarter-over-quarter change: an annual period has no preceding quarter. Inputs: NetIncomeLoss 1484000000, NetCashProvidedByUsedInOperatingActivities 2513000000, Assets 37190000000. The value is ranked only against years on the same concepts, because years-back-4 rests on ProfitLoss.", "account": "accruals_over_total_assets = (net_income - operating_cash_flow) / assets", "expected_direction": "down", "horizon": "next 10-K (fiscal 2026 annual cell)", "quote": "\"position_in_history\": \"second lowest of the 4 filled years on the same concepts; 1 other filled year rests on a different concept and is not compared\"", "paragraph_id": "0001783180-26-000032:trends:accruals_over_total_assets:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_trend", "what_changed": "Value 0.02977941176470588. Year-over-year change -0.00551898707081086 against years-back-1. Inputs: AllowanceForDoubtfulAccountsReceivable 81000000 (10-K) and ReceivablesNetCurrent 2639000000. The years-back-1 allowance was 97000000. The allowance has no row for 2026-03-31, and the record does not reach 2026-06-30, so no interim ratio exists.", "account": "bad_debt_reserve_ratio = bad_debt_allowance / (receivables + bad_debt_allowance)", "expected_direction": "down", "horizon": "next 10-K (fiscal 2026 annual cell)", "quote": "\"position_in_history\": \"lowest of the 5 filled years\"", "paragraph_id": "0001783180-26-000032:trends:bad_debt_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_trend", "what_changed": "Value 0.03177449763185727. Year-over-year change 0.007181417493104265 against years-back-1. Inputs: ContractWithCustomerLiabilityCurrent 691000000 and revenue 21747000000.", "account": "contract_liabilities_over_revenue = ContractWithCustomerLiabilityCurrent / revenue", "expected_direction": "up", "horizon": "next 10-K (fiscal 2026 annual cell)", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0001783180-26-000032:trends:contract_liabilities_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_insufficient", "what_changed": "insufficient. The table could not fill days_sales_of_inventory for years-back-0: no cost-of-revenue concept has a row for 2025. There is no value, no change and no position. The 8-K prints cost of products sold and cost of services sold for the quarter and half-year only. I did not build the ratio from them.", "account": "days_sales_of_inventory = inventory / cost_of_revenue * days_in_period", "expected_direction": "none", "horizon": "next 10-K (fiscal 2026 annual cell)", "quote": "\"missing\": \"no row for cost_of_revenue in 2025-01-01..2025-12-31: us-gaap:CostOfRevenue, us-gaap:CostOfGoodsAndServicesSold, us-gaap:CostOfGoodsSold, us-gaap:CostOfServices, us-gaap:CostOfSales is in the record, but not for this period\"", "paragraph_id": "0001783180-26-000032:trends:days_sales_of_inventory:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_trend", "what_changed": "Value 44.29277601508254. Year-over-year change 1.1429939284508563 against years-back-1. Inputs: ReceivablesNetCurrent 2639000000, revenue 21747000000 and 365 days.", "account": "days_sales_outstanding = receivables / revenue * days_in_period", "expected_direction": "up", "horizon": "next 10-K (fiscal 2026 annual cell)", "quote": "\"position_in_history\": \"second highest of the 5 filled years\"", "paragraph_id": "0001783180-26-000032:trends:days_sales_outstanding:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_gross_margin_insufficient", "what_changed": "insufficient. The table could not fill gross_margin for years-back-0 because no cost-of-revenue row exists for 2025. There is no value, no change and no position. Gross margin exists in my input only for years-back-1 to years-back-3. No gross margin exists for any quarter in the trend table.", "account": "gross_margin = (revenue - cost_of_revenue) / revenue", "expected_direction": "none", "horizon": "next 10-K (fiscal 2026 annual cell)", "quote": "\"missing\": \"no row for cost_of_revenue in 2025-01-01..2025-12-31: us-gaap:CostOfRevenue, us-gaap:CostOfGoodsAndServicesSold, us-gaap:CostOfGoodsSold, us-gaap:CostOfServices, us-gaap:CostOfSales is in the record, but not for this period\"", "paragraph_id": "0001783180-26-000032:trends:gross_margin:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_trend", "what_changed": "Value 0.13572291582762788. Year-over-year change 0.042203994557510435 against years-back-1. Inputs: InventoryValuationReserves 337000000 and InventoryNet 2483000000. The years-back-1 inputs were 215000000 and 2299000000.", "account": "inventory_reserve_ratio = InventoryValuationReserves / InventoryNet", "expected_direction": "up", "horizon": "next 10-K (fiscal 2026 annual cell)", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0001783180-26-000032:trends:inventory_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_insufficient", "what_changed": "insufficient. The table has no non-GAAP row in any period, so non_gaap_gap is not filled for years-back-0 or for any other period. The 8-K prints adjusted figures, but the gap is not computed anywhere in my input.", "account": "non_gaap_gap (non-GAAP net income against GAAP net income)", "expected_direction": "none", "horizon": "none; companyfacts carries no non-GAAP concept", "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"", "paragraph_id": "0001783180-26-000032:trends:non_gaap_gap:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_trend", "what_changed": "Value 0.12135007127419874. Year-over-year change 0.003454491802527479 against years-back-1. Inputs: ReceivablesNetCurrent 2639000000 and revenue 21747000000.", "account": "receivables_over_revenue = ReceivablesNetCurrent / revenue", "expected_direction": "up", "horizon": "next 10-K (fiscal 2026 annual cell)", "quote": "\"position_in_history\": \"second highest of the 5 filled years\"", "paragraph_id": "0001783180-26-000032:trends:receivables_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_soft_asset_share_trend", "what_changed": "Value 0.8730841624092498. Year-over-year change 0.05937937937045612 against years-back-1. Inputs: Assets 37190000000, PropertyPlantAndEquipmentNet 3165000000 and cash 1555000000.", "account": "soft_asset_share = (assets - PP&E - cash) / assets", "expected_direction": "up", "horizon": "next 10-K (fiscal 2026 annual cell)", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0001783180-26-000032:trends:soft_asset_share:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_trend", "what_changed": "Value 0.041063135145077485. Year-over-year change 0.0061080519822206 against years-back-1. Inputs: ProductWarrantyAccrual 893000000 and revenue 21747000000.", "account": "warranty_reserve_ratio = ProductWarrantyAccrual / revenue", "expected_direction": "up", "horizon": "next 10-K (fiscal 2026 annual cell)", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0001783180-26-000032:trends:warranty_reserve_ratio:2025-01-01..2025-12-31" }
```

**Change of tag**

```json
{ "id": "articulation_and_the_filed_history_accruals_net_income_concept_change", "what_changed": "Change of tag in the net_income input to accruals_over_total_assets. It is us-gaap:ProfitLoss in years-back-4 (2021-01-01..2021-12-31) and us-gaap:NetIncomeLoss in years-back-0 through years-back-3. The table therefore ranks years-back-0 among 4 years, not 5. It also refuses the years-back-3 year-over-year change because each period rests on a different concept.", "account": "net_income input to accruals_over_total_assets (us-gaap:NetIncomeLoss against us-gaap:ProfitLoss)", "expected_direction": "none", "horizon": "the filed history this metric is ranked against", "quote": "\"position_in_history\": \"the only filled year on the same concepts; 4 other filled years rest on a different concept and are not compared\"", "paragraph_id": "0001783180-26-000032:trends:accruals_over_total_assets:2021-01-01..2021-12-31" }
```

**Trend table, quarters-back-1 (2026-01-01..2026-03-31), the newest quarter the record reaches**

```json
{ "id": "earnings_quality_accruals_over_total_assets_interim_trend", "what_changed": "Value 0.004275802721454311. Year-over-year change 0.006223836853207267 against quarters-back-5. No quarter-over-quarter change: the metric is not filled in quarters-back-2. Inputs: NetIncomeLoss 238000000, NetCashProvidedByUsedInOperatingActivities 79000000 and Assets 37186000000. Only 2 quarters are filled, which is insufficient for a trend claim.", "account": "accruals_over_total_assets (quarter)", "expected_direction": "up", "horizon": "next 10-Q cell the record reaches", "quote": "\"position_in_history\": \"highest of the 2 filled quarters\"", "paragraph_id": "0001783180-26-000032:trends:accruals_over_total_assets:2026-01-01..2026-03-31" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_interim_trend", "what_changed": "Value 0.13518067777569742. Year-over-year change 0.03130946275078367 against quarters-back-5. No quarter-over-quarter change: quarters-back-2 is not filled. Inputs: ContractWithCustomerLiabilityCurrent 722000000 and revenue 5341000000.", "account": "contract_liabilities_over_revenue (quarter)", "expected_direction": "up", "horizon": "next 10-Q cell the record reaches", "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"", "paragraph_id": "0001783180-26-000032:trends:contract_liabilities_over_revenue:2026-01-01..2026-03-31" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_interim_trend", "what_changed": "Value 52.7429320351994. Year-over-year change 1.3611765733366212 against quarters-back-5. No quarter-over-quarter change: quarters-back-2 is not filled. Inputs: ReceivablesNetCurrent 3130000000 and revenue 5341000000.", "account": "days_sales_outstanding (quarter)", "expected_direction": "up", "horizon": "next 10-Q cell the record reaches", "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"", "paragraph_id": "0001783180-26-000032:trends:days_sales_outstanding:2026-01-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_interim_trend", "what_changed": "Value 0.1336691204959318. Year-over-year change 0.04265703590378678 against quarters-back-5. No quarter-over-quarter change: quarters-back-2 is not filled. Inputs: InventoryValuationReserves 345000000 and InventoryNet 2581000000.", "account": "inventory_reserve_ratio (quarter)", "expected_direction": "up", "horizon": "next 10-Q cell the record reaches", "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"", "paragraph_id": "0001783180-26-000032:trends:inventory_reserve_ratio:2026-01-01..2026-03-31" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_interim_trend", "what_changed": "Value 0.5860325781688822. Year-over-year change 0.015124184148184616 against quarters-back-5. No quarter-over-quarter change: quarters-back-2 is not filled. Inputs: ReceivablesNetCurrent 3130000000 and revenue 5341000000.", "account": "receivables_over_revenue (quarter)", "expected_direction": "up", "horizon": "next 10-Q cell the record reaches", "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"", "paragraph_id": "0001783180-26-000032:trends:receivables_over_revenue:2026-01-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_soft_asset_share_interim_trend", "what_changed": "Value 0.8791749583176465. Year-over-year change 0.009171940236597287 against quarters-back-5. No quarter-over-quarter change: quarters-back-2 is not filled. Inputs: Assets 37186000000, PropertyPlantAndEquipmentNet 3122000000 and cash 1371000000.", "account": "soft_asset_share (quarter)", "expected_direction": "up", "horizon": "next 10-Q cell the record reaches", "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"", "paragraph_id": "0001783180-26-000032:trends:soft_asset_share:2026-01-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_interim_trend", "what_changed": "Value 0.17038007863695936. Year-over-year change 0.014381611791424664 against quarters-back-5. No quarter-over-quarter change: quarters-back-2 is not filled. Inputs: ProductWarrantyAccrual 910000000 and revenue 5341000000.", "account": "warranty_reserve_ratio (quarter)", "expected_direction": "up", "horizon": "next 10-Q cell the record reaches", "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"", "paragraph_id": "0001783180-26-000032:trends:warranty_reserve_ratio:2026-01-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_interim_insufficient", "what_changed": "insufficient. No allowance row exists for 2026-03-31, so bad_debt_reserve_ratio is not filled for quarters-back-1. There is no value, no change and no position.", "account": "bad_debt_reserve_ratio (quarter)", "expected_direction": "none", "horizon": "next 10-Q cell the record reaches", "quote": "\"missing\": \"no row for bad_debt_allowance in 2026-03-31: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"", "paragraph_id": "0001783180-26-000032:trends:bad_debt_reserve_ratio:2026-01-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_interim_insufficient", "what_changed": "insufficient. No cost-of-revenue row exists for 2026-01-01..2026-03-31, so days_sales_of_inventory is not filled for quarters-back-1.", "account": "days_sales_of_inventory (quarter)", "expected_direction": "none", "horizon": "next 10-Q cell the record reaches", "quote": "\"missing\": \"no row for cost_of_revenue in 2026-01-01..2026-03-31: us-gaap:CostOfRevenue, us-gaap:CostOfGoodsAndServicesSold, us-gaap:CostOfGoodsSold, us-gaap:CostOfServices, us-gaap:CostOfSales is in the record, but not for this period\"", "paragraph_id": "0001783180-26-000032:trends:days_sales_of_inventory:2026-01-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_gross_margin_interim_insufficient", "what_changed": "insufficient. No cost-of-revenue row exists for 2026-01-01..2026-03-31, so gross_margin is not filled for quarters-back-1.", "account": "gross_margin (quarter)", "expected_direction": "none", "horizon": "next 10-Q cell the record reaches", "quote": "\"missing\": \"no row for cost_of_revenue in 2026-01-01..2026-03-31: us-gaap:CostOfRevenue, us-gaap:CostOfGoodsAndServicesSold, us-gaap:CostOfGoodsSold, us-gaap:CostOfServices, us-gaap:CostOfSales is in the record, but not for this period\"", "paragraph_id": "0001783180-26-000032:trends:gross_margin:2026-01-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_interim_insufficient", "what_changed": "insufficient. The table has no non-GAAP row, so non_gaap_gap is not filled for quarters-back-1.", "account": "non_gaap_gap (quarter)", "expected_direction": "none", "horizon": "none; companyfacts carries no non-GAAP concept", "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"", "paragraph_id": "0001783180-26-000032:trends:non_gaap_gap:2026-01-01..2026-03-31" }
```

**Numeric facts: tax**

```json
{ "id": "estimates_and_discretion_effective_tax_rate_rise", "what_changed": "Effective tax rate on continuing operations: 0.250 for the quarter ended 2026-06-30, against 0.200 for the quarter ended 2025-06-30. The 8-K names a higher effective tax rate as a driver of lower EPS.", "account": "EffectiveIncomeTaxRateContinuingOperations", "expected_direction": "up", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "\"value\": \"0.250\"", "paragraph_id": "0001783180-26-000032:facts:EffectiveIncomeTaxRateContinuingOperations:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_income_tax_expense", "what_changed": "Income tax expense was 180000000 for the quarter ended 2026-06-30; the 8-K prints (162) million for the same quarter a year earlier. For the six months the figures are 84000000 against 273000000.", "account": "IncomeTaxExpenseBenefit", "expected_direction": "up", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "\"value\": \"180000000\"", "paragraph_id": "0001783180-26-000032:facts:IncomeTaxExpenseBenefit:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_cumulative_effective_tax_rate", "what_changed": "Effective tax rate on continuing operations for the six months ended 2026-06-30: 0.094, against 0.201 a year earlier. The 10-K rate for fiscal 2025 was 0.134.", "account": "EffectiveIncomeTaxRateContinuingOperations (six months)", "expected_direction": "down", "horizon": "fiscal 2026 10-K", "quote": "\"value\": \"0.094\"", "paragraph_id": "0001783180-26-000032:facts:EffectiveIncomeTaxRateContinuingOperations:2026-01-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_negative_interim_tax_rate", "what_changed": "The Q1 10-Q reported an effective tax rate of -0.565 for 2026-01-01..2026-03-31, against 0.203 for the same period of 2025. In the same period the valuation-allowance reconciling item was -99000000.", "account": "EffectiveIncomeTaxRateContinuingOperations (Q1 10-Q)", "expected_direction": "down", "horizon": "fiscal 2026 10-K", "quote": "\"value\": \"-0.565\"", "paragraph_id": "0001783180-26-000026:facts:EffectiveIncomeTaxRateContinuingOperations:2026-01-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_valuation_allowance_release", "what_changed": "The tax reconciliation item for the change in the deferred-tax-asset valuation allowance is -99000000 for the six months ended 2026-06-30. The same -99000000 appears for Q1 in the Q1 10-Q. This is a judgment-driven reduction of tax expense.", "account": "IncomeTaxReconciliationChangeInDeferredTaxAssetsValuationAllowance", "expected_direction": "down", "horizon": "fiscal 2026 10-K", "quote": "\"value\": \"-99000000\"", "paragraph_id": "0001783180-26-000032:facts:IncomeTaxReconciliationChangeInDeferredTaxAssetsValuationAllowance:2026-01-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_nondeductible_impairment_tax_effect", "what_changed": "The tax reconciliation item for non-deductible impairment losses is 46000000 for the quarter ended 2026-06-30, and 46000000 for the six months. It sits alongside the 46000000 Riello impairment.", "account": "IncomeTaxReconciliationNondeductibleExpenseImpairmentLosses", "expected_direction": "up", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "\"value\": \"46000000\"", "paragraph_id": "0001783180-26-000032:facts:IncomeTaxReconciliationNondeductibleExpenseImpairmentLosses:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_unrecognized_tax_benefits_possible_decrease", "what_changed": "At 2026-06-30 the reasonably possible decrease in unrecognized tax benefits is a range: minimum 5000000, maximum 95000000.", "account": "DecreaseInUnrecognizedTaxBenefitsIsReasonablyPossible", "expected_direction": "down", "horizon": "twelve months after 2026-06-30", "quote": "\"value\": \"95000000\"", "paragraph_id": "0001783180-26-000032:facts:DecreaseInUnrecognizedTaxBenefitsIsReasonablyPossible:2026-06-30:srt:RangeAxis=srt:MaximumMember" }
```

```json
{ "id": "estimates_and_discretion_domestic_tax_settlement", "what_changed": "The tax reconciliation item for domestic tax settlements is -18000000 for the six months ended 2026-06-30.", "account": "IncomeTaxReconciliationTaxSettlementsDomestic", "expected_direction": "down", "horizon": "fiscal 2026 10-K", "quote": "\"value\": \"-18000000\"", "paragraph_id": "0001783180-26-000032:facts:IncomeTaxReconciliationTaxSettlementsDomestic:2026-01-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_deferred_tax_benefit", "what_changed": "The deferred income tax benefit is -242000000 for the six months ended 2026-06-30. The 8-K cash flow statement prints (242) against (158) a year earlier.", "account": "DeferredIncomeTaxExpenseBenefit", "expected_direction": "down", "horizon": "next 10-Q (nine months ending 2026-09-30)", "quote": "\"value\": \"-242000000\"", "paragraph_id": "0001783180-26-000032:facts:DeferredIncomeTaxExpenseBenefit:2026-01-01..2026-06-30" }
```

**Numeric facts: restructuring**

```json
{ "id": "earnings_quality_restructuring_charges_cumulative", "what_changed": "Restructuring charges are 116000000 for the six months ended 2026-06-30, against 55000000 a year earlier. The 10-K prints restructuring costs of 178000000 for fiscal 2025.", "account": "RestructuringCharges (six months)", "expected_direction": "up", "horizon": "fiscal 2026 10-K", "quote": "\"value\": \"116000000\"", "paragraph_id": "0001783180-26-000032:facts:RestructuringCharges:2026-01-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_restructuring_charges_recent_decline", "what_changed": "Restructuring charges are 8000000 for the quarter ended 2026-06-30, against 47000000 for the quarter ended 2025-06-30.", "account": "RestructuringCharges (quarter)", "expected_direction": "down", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "\"value\": \"8000000\"", "paragraph_id": "0001783180-26-000032:facts:RestructuringCharges:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_restructuring_charges_in_earlier_interim_filing", "what_changed": "The Q1 10-Q reported restructuring charges of 108000000 for 2026-01-01..2026-03-31. Operating income for that period was 259000000.", "account": "RestructuringCharges (Q1 10-Q)", "expected_direction": "up", "horizon": "fiscal 2026 10-K", "quote": "\"value\": \"108000000\"", "paragraph_id": "0001783180-26-000026:facts:RestructuringCharges:2026-01-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_restructuring_in_cost_of_sales", "what_changed": "Restructuring charged to cost of goods and services sold is 45000000 for the six months ended 2026-06-30, against 10000000 a year earlier. The SG&A portion is 71000000 against 45000000.", "account": "RestructuringCharges by income-statement line (cost of goods and services sold)", "expected_direction": "up", "horizon": "fiscal 2026 10-K", "quote": "\"value\": \"45000000\"", "paragraph_id": "0001783180-26-000032:facts:RestructuringCharges:2026-01-01..2026-06-30:us-gaap:StatementOfIncomeLocationBalanceAxis=us-gaap:CostOfGoodsAndServicesSold" }
```

```json
{ "id": "earnings_quality_restructuring_concentrated_in_europe", "what_changed": "Restructuring in the Climate Solutions Europe segment is 89000000 for the six months ended 2026-06-30, against 26000000 a year earlier. The other segments are 3000000 (CSA), 7000000 (CSAME) and 4000000 (CST); corporate is 13000000.", "account": "RestructuringCharges, Climate Solutions Europe segment", "expected_direction": "up", "horizon": "fiscal 2026 10-K", "quote": "\"value\": \"89000000\"", "paragraph_id": "0001783180-26-000032:facts:RestructuringCharges:2026-01-01..2026-06-30:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=carr:ClimateSolutionsEuropeSegmentMember" }
```

```json
{ "id": "estimates_and_discretion_restructuring_reserve_balance", "what_changed": "The restructuring reserve is 111000000 at 2026-06-30, against 102000000 at 2025-12-31 and 76000000 at 2025-06-30.", "account": "RestructuringReserve", "expected_direction": "up", "horizon": "next 10-Q (2026-09-30)", "quote": "\"value\": \"111000000\"", "paragraph_id": "0001783180-26-000032:facts:RestructuringReserve:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_restructuring_reserve_other_adjustment", "what_changed": "The translation-and-other adjustment in the restructuring reserve roll-forward is -96000000 for the six months ended 2026-06-30, against -37000000 a year earlier.", "account": "RestructuringReserveTranslationAndOtherAdjustment", "expected_direction": "down", "horizon": "fiscal 2026 10-K", "quote": "\"value\": \"-96000000\"", "paragraph_id": "0001783180-26-000032:facts:RestructuringReserveTranslationAndOtherAdjustment:2026-01-01..2026-06-30" }
```

**Numeric facts: earnings**

```json
{ "id": "earnings_quality_operating_profit_decline", "what_changed": "Operating income is 825000000 for the quarter ended 2026-06-30, against 903000000 a year earlier. For the six months it is 1083000000 against 1532000000.", "account": "OperatingIncomeLoss", "expected_direction": "down", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "\"value\": \"825000000\"", "paragraph_id": "0001783180-26-000032:facts:OperatingIncomeLoss:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_pretax_earnings_decline", "what_changed": "Pre-tax income from continuing operations is 721000000 for the quarter ended 2026-06-30, against 812000000 a year earlier. For the six months it is 890000000 against 1360000000.", "account": "IncomeLossFromContinuingOperationsBeforeIncomeTaxes", "expected_direction": "down", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "\"value\": \"721000000\"", "paragraph_id": "0001783180-26-000032:facts:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_net_income_attributable_decline", "what_changed": "Net income attributable to common shareowners is 501000000 for the quarter ended 2026-06-30, against 591000000 a year earlier. For the six months it is 739000000 against 1003000000.", "account": "NetIncomeLoss", "expected_direction": "down", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "\"value\": \"501000000\"", "paragraph_id": "0001783180-26-000032:facts:NetIncomeLoss:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_riello_asset_impairment", "what_changed": "Asset impairment charges are 46000000 for the quarter ended 2026-06-30, against 0 a year earlier. The same 46000000 is tagged to the Riello held-for-sale disposal group.", "account": "AssetImpairmentCharges", "expected_direction": "up", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "\"value\": \"46000000\"", "paragraph_id": "0001783180-26-000032:facts:AssetImpairmentCharges:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_other_operating_income_swing", "what_changed": "Other operating income (expense), net is -3000000 for the quarter ended 2026-06-30, against 30000000 a year earlier. The segment-level figure is 37000000 against 42000000.", "account": "OtherOperatingIncomeExpenseNet", "expected_direction": "down", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "\"value\": \"-3000000\"", "paragraph_id": "0001783180-26-000032:facts:OtherOperatingIncomeExpenseNet:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_equity_method_income_decline", "what_changed": "Equity-method investment earnings are 58000000 for the quarter ended 2026-06-30, against 78000000 a year earlier. By segment: CSA 31000000 against 43000000, CSAME 25000000 against 30000000, CST 2000000 against 4000000, and CSE 0 against 1000000.", "account": "IncomeLossFromEquityMethodInvestments", "expected_direction": "down", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "\"value\": \"58000000\"", "paragraph_id": "0001783180-26-000032:facts:IncomeLossFromEquityMethodInvestments:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_equity_method_disposal_loss", "what_changed": "The realized gain (loss) on disposal of equity-method investments is -37000000 for the six months ended 2026-06-30.", "account": "EquityMethodInvestmentRealizedGainLossOnDisposal", "expected_direction": "down", "horizon": "fiscal 2026 10-K", "quote": "\"value\": \"-37000000\"", "paragraph_id": "0001783180-26-000032:facts:EquityMethodInvestmentRealizedGainLossOnDisposal:2026-01-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_prior_deconsolidation_gain_absent", "what_changed": "The deconsolidation gain is 0 for the quarter ended 2026-06-30. It was 7000000 for the quarter ended 2025-06-30; the 8-K labels that CCR gain.", "account": "DeconsolidationGainOrLossAmount", "expected_direction": "down", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "\"value\": \"0\"", "paragraph_id": "0001783180-26-000032:facts:DeconsolidationGainOrLossAmount:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_interest_expense_increase", "what_changed": "Non-operating interest income (expense), net is -105000000 for the quarter ended 2026-06-30, against -91000000 a year earlier. For the six months it is -195000000 against -173000000.", "account": "InterestIncomeExpenseNonoperatingNet", "expected_direction": "up", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "\"value\": \"-105000000\"", "paragraph_id": "0001783180-26-000032:facts:InterestIncomeExpenseNonoperatingNet:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_basic_share_count_decline", "what_changed": "Weighted-average basic shares are 828100000 for the quarter ended 2026-06-30, against 854900000 a year earlier. Diluted shares are 836500000 against 866300000.", "account": "WeightedAverageNumberOfSharesOutstandingBasic", "expected_direction": "down", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "\"value\": \"828100000\"", "paragraph_id": "0001783180-26-000032:facts:WeightedAverageNumberOfSharesOutstandingBasic:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_antidilutive_securities_increase", "what_changed": "Antidilutive securities excluded from diluted EPS are 3200000 for the quarter ended 2026-06-30, against 1900000 a year earlier.", "account": "AntidilutiveSecuritiesExcludedFromComputationOfEarningsPerShareAmount", "expected_direction": "up", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "\"value\": \"3200000\"", "paragraph_id": "0001783180-26-000032:facts:AntidilutiveSecuritiesExcludedFromComputationOfEarningsPerShareAmount:2026-04-01..2026-06-30" }
```

**Numeric facts: revenue, receivables, contract balances, inventory, warranty and goodwill**

```json
{ "id": "revenue_recognition_receivables_balance", "what_changed": "Receivables, net are 3246000000 at 2026-06-30. The trend-table inputs show 3130000000 at 2026-03-31 and 2639000000 at 2025-12-31. No receivables-over-revenue ratio or DSO exists for the quarter ended 2026-06-30, because the record does not reach that period.", "account": "ReceivablesNetCurrent", "expected_direction": "up", "horizon": "next 10-Q (2026-09-30)", "quote": "\"value\": \"3246000000\"", "paragraph_id": "0001783180-26-000032:facts:ReceivablesNetCurrent:2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_balance", "what_changed": "Current contract liabilities are 816000000 at 2026-06-30. The trend-table inputs show 722000000 at 2026-03-31 and 691000000 at 2025-12-31.", "account": "ContractWithCustomerLiabilityCurrent", "expected_direction": "up", "horizon": "next 10-Q (2026-09-30)", "quote": "\"value\": \"816000000\"", "paragraph_id": "0001783180-26-000032:facts:ContractWithCustomerLiabilityCurrent:2026-06-30" }
```

```json
{ "id": "revenue_recognition_total_contract_liabilities", "what_changed": "Total contract liabilities, current and noncurrent, are 1033000000 at 2026-06-30. This item quotes only this date.", "account": "ContractWithCustomerLiability", "expected_direction": "none", "horizon": "next 10-Q (2026-09-30)", "quote": "\"value\": \"1033000000\"", "paragraph_id": "0001783180-26-000032:facts:ContractWithCustomerLiability:2026-06-30" }
```

```json
{ "id": "revenue_recognition_united_states_revenue", "what_changed": "United States revenue is 3536000000 for the quarter ended 2026-06-30, against 3429000000 a year earlier. For the six months it is 6192000000 against 6168000000.", "account": "RevenueFromContractWithCustomerExcludingAssessedTax, United States", "expected_direction": "up", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "\"value\": \"3536000000\"", "paragraph_id": "0001783180-26-000032:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:StatementGeographicalAxis=country:US" }
```

```json
{ "id": "revenue_recognition_europe_revenue", "what_changed": "Europe revenue is 1581000000 for the quarter ended 2026-06-30, against 1520000000 a year earlier. For the six months it is 3130000000 against 2920000000.", "account": "RevenueFromContractWithCustomerExcludingAssessedTax, Europe", "expected_direction": "up", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "\"value\": \"1581000000\"", "paragraph_id": "0001783180-26-000032:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:StatementGeographicalAxis=srt:EuropeMember" }
```

```json
{ "id": "revenue_recognition_asia_pacific_revenue", "what_changed": "Asia Pacific revenue is 1029000000 for the quarter ended 2026-06-30, against 981000000 a year earlier. Other regions are 205000000 against 183000000.", "account": "RevenueFromContractWithCustomerExcludingAssessedTax, Asia Pacific", "expected_direction": "up", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "\"value\": \"1029000000\"", "paragraph_id": "0001783180-26-000032:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:StatementGeographicalAxis=srt:AsiaPacificMember" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_balance", "what_changed": "The inventory valuation reserve is 328000000 at 2026-06-30. The trend-table inputs show 345000000 at 2026-03-31 and 337000000 at 2025-12-31. Net inventory rose over the same dates. No inventory_reserve_ratio exists for 2026-06-30 in my input.", "account": "InventoryValuationReserves", "expected_direction": "down", "horizon": "next 10-Q (2026-09-30)", "quote": "\"value\": \"328000000\"", "paragraph_id": "0001783180-26-000032:facts:InventoryValuationReserves:2026-06-30" }
```

```json
{ "id": "earnings_quality_inventory_balance_build", "what_changed": "Net inventory is 2759000000 at 2026-06-30. The trend-table inputs show 2581000000 at 2026-03-31 and 2483000000 at 2025-12-31. The 8-K cash flow statement shows inventories using (197) million in the quarter against (111) a year earlier.", "account": "InventoryNet", "expected_direction": "up", "horizon": "next 10-Q (2026-09-30)", "quote": "\"value\": \"2759000000\"", "paragraph_id": "0001783180-26-000032:facts:InventoryNet:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_accrual_balance", "what_changed": "The product warranty accrual is 935000000 at 2026-06-30, against 862000000 at 2025-06-30. The trend-table inputs show 910000000 at 2026-03-31 and 893000000 at 2025-12-31.", "account": "ProductWarrantyAccrual", "expected_direction": "up", "horizon": "next 10-Q (2026-09-30)", "quote": "\"value\": \"935000000\"", "paragraph_id": "0001783180-26-000032:facts:ProductWarrantyAccrual:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_preexisting_adjustment", "what_changed": "The change in estimate for pre-existing warranties is -10000000 for the six months ended 2026-06-30, against 30000000 a year earlier: a reduction of prior estimates this year where last year added to them.", "account": "ProductWarrantyAccrualPreexistingIncreaseDecrease", "expected_direction": "down", "horizon": "fiscal 2026 10-K", "quote": "\"value\": \"-10000000\"", "paragraph_id": "0001783180-26-000032:facts:ProductWarrantyAccrualPreexistingIncreaseDecrease:2026-01-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_goodwill_currency_translation", "what_changed": "The foreign-currency translation effect on goodwill is -231000000 for the six months ended 2026-06-30. The 8-K balance sheet shows goodwill of 15,267 million against 15,501 million at 2025-12-31.", "account": "GoodwillForeignCurrencyTranslationGainLoss", "expected_direction": "down", "horizon": "next 10-Q (2026-09-30)", "quote": "\"value\": \"-231000000\"", "paragraph_id": "0001783180-26-000032:facts:GoodwillForeignCurrencyTranslationGainLoss:2026-01-01..2026-06-30" }
```

**Numeric facts: segments**

```json
{ "id": "narrative_signs_of_operating_pressure_americas_segment_profit", "what_changed": "Climate Solutions Americas segment operating profit is 823000000 for the quarter ended 2026-06-30, against 879000000 a year earlier. Segment revenue is 3372000000 against 3252000000.", "account": "OperatingIncomeLoss, Climate Solutions Americas segment", "expected_direction": "down", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "\"value\": \"823000000\"", "paragraph_id": "0001783180-26-000032:facts:OperatingIncomeLoss:2026-04-01..2026-06-30:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=carr:ClimateSolutionsAmericasSegmentMember" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_americas_cumulative_segment_profit", "what_changed": "Climate Solutions Americas segment operating profit is 1196000000 for the six months ended 2026-06-30, against 1449000000 a year earlier. Segment revenue is 5873000000 against 5824000000.", "account": "OperatingIncomeLoss, Climate Solutions Americas segment (six months)", "expected_direction": "down", "horizon": "fiscal 2026 10-K", "quote": "\"value\": \"1196000000\"", "paragraph_id": "0001783180-26-000032:facts:OperatingIncomeLoss:2026-01-01..2026-06-30:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=carr:ClimateSolutionsAmericasSegmentMember" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_americas_segment_cost_of_sales", "what_changed": "Climate Solutions Americas segment cost of goods and services sold is 2227000000 for the quarter ended 2026-06-30, against 2061000000 a year earlier. Segment revenue is 3372000000 against 3252000000. I did not compute a segment gross margin; the 8-K prints segment operating margin of 24.4% against 27.0%.", "account": "CostOfGoodsAndServicesSold, Climate Solutions Americas segment", "expected_direction": "up", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "\"value\": \"2227000000\"", "paragraph_id": "0001783180-26-000032:facts:CostOfGoodsAndServicesSold:2026-04-01..2026-06-30:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=carr:ClimateSolutionsAmericasSegmentMember" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_asia_middle_east_africa_segment_profit", "what_changed": "CSAME segment operating profit is 108000000 for the quarter ended 2026-06-30, against 135000000 a year earlier. For the six months it is 189000000 against 256000000.", "account": "OperatingIncomeLoss, Climate Solutions Asia Pacific, Middle East & Africa segment", "expected_direction": "down", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "\"value\": \"108000000\"", "paragraph_id": "0001783180-26-000032:facts:OperatingIncomeLoss:2026-04-01..2026-06-30:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=carr:ClimateSolutionsCSAMESegmentMember" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_segment_equity_method_income_asia", "what_changed": "Equity-method earnings in the CSAME segment are 25000000 for the quarter ended 2026-06-30, against 30000000 a year earlier. For the six months they are 42000000 against 48000000.", "account": "IncomeLossFromEquityMethodInvestments, CSAME segment", "expected_direction": "down", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "\"value\": \"25000000\"", "paragraph_id": "0001783180-26-000032:facts:IncomeLossFromEquityMethodInvestments:2026-04-01..2026-06-30:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=carr:ClimateSolutionsCSAMESegmentMember" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_europe_segment_profit", "what_changed": "Climate Solutions Europe segment operating profit is 95000000 for the quarter ended 2026-06-30, against 99000000 a year earlier. For the six months it is 184000000 against 204000000.", "account": "OperatingIncomeLoss, Climate Solutions Europe segment", "expected_direction": "down", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "\"value\": \"95000000\"", "paragraph_id": "0001783180-26-000032:facts:OperatingIncomeLoss:2026-04-01..2026-06-30:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=carr:ClimateSolutionsEuropeSegmentMember" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_transportation_segment_profit", "what_changed": "Climate Solutions Transportation segment operating profit is 118000000 for the quarter ended 2026-06-30, against 128000000 a year earlier. For the six months it is 219000000 against 225000000.", "account": "OperatingIncomeLoss, Climate Solutions Transportation segment", "expected_direction": "down", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "\"value\": \"118000000\"", "paragraph_id": "0001783180-26-000032:facts:OperatingIncomeLoss:2026-04-01..2026-06-30:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=carr:ClimateSolutionsTransportationSegmentMember" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_total_segment_profit", "what_changed": "Total segment operating profit is 1144000000 for the quarter ended 2026-06-30, against 1241000000 a year earlier. For the six months it is 1788000000 against 2134000000. All four segments are lower in the quarter.", "account": "OperatingIncomeLoss, all operating segments", "expected_direction": "down", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "\"value\": \"1144000000\"", "paragraph_id": "0001783180-26-000032:facts:OperatingIncomeLoss:2026-04-01..2026-06-30:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_segment_selling_general_administrative", "what_changed": "Segment-level SG&A is 762000000 for the quarter ended 2026-06-30, against 735000000 a year earlier. For the six months it is 1514000000 against 1423000000.", "account": "SellingGeneralAndAdministrativeExpense, all operating segments", "expected_direction": "up", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "\"value\": \"762000000\"", "paragraph_id": "0001783180-26-000032:facts:SellingGeneralAndAdministrativeExpense:2026-04-01..2026-06-30:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember" }
```

```json
{ "id": "structure_and_disclosure_changes_corporate_and_other_cost", "what_changed": "The other segment-reporting item, which the 8-K labels corporate and other, is 49000000 for the quarter ended 2026-06-30, against 75000000 a year earlier. For the six months it is 99000000 against 120000000.", "account": "SegmentReportingOtherItemAmount", "expected_direction": "down", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "\"value\": \"49000000\"", "paragraph_id": "0001783180-26-000032:facts:SegmentReportingOtherItemAmount:2026-04-01..2026-06-30" }
```

```json
{ "id": "structure_and_disclosure_changes_reportable_segment_count", "what_changed": "The number of reportable segments is 4 for the six months ended 2026-06-30. The number of operating segments is also 4. No prior count is quoted here.", "account": "NumberOfReportableSegments", "expected_direction": "none", "horizon": "next 10-Q", "quote": "\"value\": \"4\"", "paragraph_id": "0001783180-26-000032:facts:NumberOfReportableSegments:2026-01-01..2026-06-30" }
```

**Numeric facts: disposals and held-for-sale**

```json
{ "id": "structure_and_disclosure_changes_assets_held_for_sale", "what_changed": "Assets of the held-for-sale disposal group are 815000000 at 2026-06-30, against 592000000 at 2025-12-31.", "account": "AssetsOfDisposalGroupIncludingDiscontinuedOperation (held for sale, not discontinued)", "expected_direction": "up", "horizon": "next 10-Q (2026-09-30), after the Riello close on July 1", "quote": "\"value\": \"815000000\"", "paragraph_id": "0001783180-26-000032:facts:AssetsOfDisposalGroupIncludingDiscontinuedOperation:2026-06-30:us-gaap:DisposalGroupClassificationAxis=us-gaap:DisposalGroupHeldforsaleNotDiscontinuedOperationsMember" }
```

```json
{ "id": "structure_and_disclosure_changes_liabilities_held_for_sale", "what_changed": "Current liabilities of the held-for-sale disposal group are 414000000 at 2026-06-30, against 170000000 at 2025-12-31. Within them, accounts payable is 148000000 against 91000000 and accrued liabilities 88000000 against 48000000.", "account": "LiabilitiesOfDisposalGroupIncludingDiscontinuedOperationCurrent", "expected_direction": "up", "horizon": "next 10-Q (2026-09-30)", "quote": "\"value\": \"414000000\"", "paragraph_id": "0001783180-26-000032:facts:LiabilitiesOfDisposalGroupIncludingDiscontinuedOperationCurrent:2026-06-30:us-gaap:DisposalGroupClassificationAxis=us-gaap:DisposalGroupHeldforsaleNotDiscontinuedOperationsMember" }
```

```json
{ "id": "structure_and_disclosure_changes_riello_sale_consideration", "what_changed": "The consideration for the Riello disposal group is 430000000, tagged at 2025-12-16. The Riello group also carries a 46000000 impairment for the quarter ended 2026-06-30.", "account": "DisposalGroupIncludingDiscontinuedOperationConsideration, Riello", "expected_direction": "none", "horizon": "next 10-Q (2026-09-30)", "quote": "\"value\": \"430000000\"", "paragraph_id": "0001783180-26-000032:facts:DisposalGroupIncludingDiscontinuedOperationConsideration:2025-12-16:us-gaap:DisposalGroupClassificationAxis=us-gaap:DisposalGroupHeldforsaleNotDiscontinuedOperationsMember,us-gaap:IncomeStatementBalanceSheetAndAdditionalDisclosuresByDisposalGroupsIncludingDiscontinuedOperationsAxis=carr:RielloBusinessMember" }
```

```json
{ "id": "structure_and_disclosure_changes_goodwill_in_disposal_group", "what_changed": "Goodwill in the held-for-sale disposal group is 188000000 at 2026-06-30, against 175000000 at 2025-12-31.", "account": "DisposalGroupIncludingDiscontinuedOperationGoodwillCurrent", "expected_direction": "up", "horizon": "next 10-Q (2026-09-30)", "quote": "\"value\": \"188000000\"", "paragraph_id": "0001783180-26-000032:facts:DisposalGroupIncludingDiscontinuedOperationGoodwillCurrent:2026-06-30:us-gaap:DisposalGroupClassificationAxis=us-gaap:DisposalGroupHeldforsaleNotDiscontinuedOperationsMember" }
```

```json
{ "id": "structure_and_disclosure_changes_disposal_group_other_noncurrent_assets", "what_changed": "Other noncurrent assets in the held-for-sale disposal group are 155000000 at 2026-06-30, against 87000000 at 2025-12-31. In the same group, inventory is 114000000 against 98000000 and receivables 105000000 against 103000000.", "account": "DisposalGroupIncludingDiscontinuedOperationOtherNoncurrentAssets", "expected_direction": "up", "horizon": "next 10-Q (2026-09-30)", "quote": "\"value\": \"155000000\"", "paragraph_id": "0001783180-26-000032:facts:DisposalGroupIncludingDiscontinuedOperationOtherNoncurrentAssets:2026-06-30:us-gaap:DisposalGroupClassificationAxis=us-gaap:DisposalGroupHeldforsaleNotDiscontinuedOperationsMember" }
```

```json
{ "id": "structure_and_disclosure_changes_acquisition_and_divestiture_costs", "what_changed": "Acquisition- and divestiture-related costs are 18000000 for the six months ended 2026-06-30, against 11000000 a year earlier. For the quarter they are 8000000 against 6000000.", "account": "BusinessCombinationAcquisitionRelatedCosts", "expected_direction": "up", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "\"value\": \"18000000\"", "paragraph_id": "0001783180-26-000032:facts:BusinessCombinationAcquisitionRelatedCosts:2026-01-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_cash_classified_held_for_sale", "what_changed": "Cash inside the held-for-sale disposal group is 95000000 at 2026-06-30, against 25000000 at 2025-12-31. The 8-K cash flow statement prints a line for the change in cash balances classified as assets held for sale.", "account": "DisposalGroupIncludingDiscontinuedOperationCashAndCashEquivalents", "expected_direction": "up", "horizon": "next 10-Q (2026-09-30)", "quote": "\"value\": \"95000000\"", "paragraph_id": "0001783180-26-000032:facts:DisposalGroupIncludingDiscontinuedOperationCashAndCashEquivalents:2026-06-30:us-gaap:DisposalGroupClassificationAxis=us-gaap:DisposalGroupHeldforsaleNotDiscontinuedOperationsMember" }
```

**Numeric facts: liquidity, capital and cash flow**

```json
{ "id": "liquidity_and_capital_current_debt", "what_changed": "Current debt is 1638000000 at 2026-06-30. The 8-K balance sheet prints 468 million for short-term borrowings and current portion of long-term debt at 2025-12-31.", "account": "DebtCurrent", "expected_direction": "up", "horizon": "next 10-Q (2026-09-30)", "quote": "\"value\": \"1638000000\"", "paragraph_id": "0001783180-26-000032:facts:DebtCurrent:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_commercial_paper", "what_changed": "Commercial paper outstanding is 685000000 at 2026-06-30. This item quotes only this date.", "account": "CommercialPaper", "expected_direction": "none", "horizon": "next 10-Q (2026-09-30)", "quote": "\"value\": \"685000000\"", "paragraph_id": "0001783180-26-000032:facts:CommercialPaper:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_short_term_borrowings_increase", "what_changed": "The net change in short-term borrowings is 361000000 for the six months ended 2026-06-30. The 8-K prints (57) million for the same six months of 2025.", "account": "ProceedsFromRepaymentsOfShortTermDebt", "expected_direction": "up", "horizon": "next 10-Q (nine months ending 2026-09-30)", "quote": "\"value\": \"361000000\"", "paragraph_id": "0001783180-26-000032:facts:ProceedsFromRepaymentsOfShortTermDebt:2026-01-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_long_term_debt", "what_changed": "Noncurrent long-term debt is 10314000000 at 2026-06-30. The 8-K prints 11,365 million at 2025-12-31.", "account": "LongTermDebtNoncurrent", "expected_direction": "down", "horizon": "next 10-Q (2026-09-30)", "quote": "\"value\": \"10314000000\"", "paragraph_id": "0001783180-26-000032:facts:LongTermDebtNoncurrent:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_share_repurchases", "what_changed": "Share repurchases are 745000000 for the six months ended 2026-06-30. The 8-K prints (1,628) million a year earlier, and (439) against (340) for the quarter.", "account": "PaymentsForRepurchaseOfCommonStock", "expected_direction": "down", "horizon": "next 10-Q (nine months ending 2026-09-30)", "quote": "\"value\": \"745000000\"", "paragraph_id": "0001783180-26-000032:facts:PaymentsForRepurchaseOfCommonStock:2026-01-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_remaining_repurchase_authorization", "what_changed": "The remaining authorized repurchase amount is 4600000000 at 2026-06-30. This item quotes only this date.", "account": "StockRepurchaseProgramRemainingAuthorizedRepurchaseAmount1", "expected_direction": "none", "horizon": "next 10-Q (2026-09-30)", "quote": "\"value\": \"4600000000\"", "paragraph_id": "0001783180-26-000032:facts:StockRepurchaseProgramRemainingAuthorizedRepurchaseAmount1:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_noncontrolling_interest_dividends", "what_changed": "Dividends paid to non-controlling interests are 65000000 for the six months ended 2026-06-30, against 9000000 a year earlier. The 8-K prints (64) against (9) for the quarter.", "account": "PaymentsOfDividendsMinorityInterest", "expected_direction": "up", "horizon": "next 10-Q (nine months ending 2026-09-30)", "quote": "\"value\": \"65000000\"", "paragraph_id": "0001783180-26-000032:facts:PaymentsOfDividendsMinorityInterest:2026-01-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_continuing_operating_cash_flow", "what_changed": "Operating cash flow from continuing operations is 953000000 for the six months ended 2026-06-30. The 8-K prints 752 million a year earlier, and 888 against 264 for the quarter.", "account": "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations", "expected_direction": "up", "horizon": "next 10-Q (nine months ending 2026-09-30)", "quote": "\"value\": \"953000000\"", "paragraph_id": "0001783180-26-000032:facts:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations:2026-01-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_total_operating_cash_flow", "what_changed": "Total operating cash flow is 1006000000 for the six months ended 2026-06-30, against 1132000000 a year earlier. The 8-K shows discontinued operating cash of 53 million against 380 million over the same periods.", "account": "NetCashProvidedByUsedInOperatingActivities", "expected_direction": "down", "horizon": "next 10-Q (nine months ending 2026-09-30)", "quote": "\"value\": \"1006000000\"", "paragraph_id": "0001783180-26-000032:facts:NetCashProvidedByUsedInOperatingActivities:2026-01-01..2026-06-30" }
```

**Numeric facts: related parties and contingencies**

```json
{ "id": "related_parties_contingencies_and_subsequent_events_related_party_revenue", "what_changed": "Product revenue from related parties is 951000000 for the quarter ended 2026-06-30, against 845000000 a year earlier. For the six months it is 1637000000 against 1625000000. The related-party cost of goods sold is 59000000 against 57000000 for the quarter.", "account": "RevenueFromContractWithCustomerExcludingAssessedTax, related parties (product)", "expected_direction": "up", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "\"value\": \"951000000\"", "paragraph_id": "0001783180-26-000032:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:ProductOrServiceAxis=us-gaap:ProductMember,us-gaap:RelatedPartyTransactionsByRelatedPartyAxis=us-gaap:RelatedPartyMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_related_party_receivables", "what_changed": "Receivables from related parties are 396000000 at 2026-06-30, against 220000000 at 2025-12-31.", "account": "ReceivablesNetCurrent, related parties", "expected_direction": "up", "horizon": "next 10-Q (2026-09-30)", "quote": "\"value\": \"396000000\"", "paragraph_id": "0001783180-26-000032:facts:ReceivablesNetCurrent:2026-06-30:us-gaap:RelatedPartyTransactionsByRelatedPartyAxis=us-gaap:RelatedPartyMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_related_party_payables", "what_changed": "Payables to related parties are 31000000 at 2026-06-30, against 40000000 at 2025-12-31.", "account": "AccountsPayableCurrent, related parties", "expected_direction": "down", "horizon": "next 10-Q (2026-09-30)", "quote": "\"value\": \"31000000\"", "paragraph_id": "0001783180-26-000032:facts:AccountsPayableCurrent:2026-06-30:us-gaap:RelatedPartyTransactionsByRelatedPartyAxis=us-gaap:RelatedPartyMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_asbestos_accrual", "what_changed": "The asbestos loss-contingency accrual is 209000000 at 2026-06-30, against 218000000 at 2025-12-31: 17000000 current (unchanged) and 192000000 noncurrent (against 201000000).", "account": "LossContingencyAccrualAtCarryingValue, asbestos matters", "expected_direction": "down", "horizon": "next 10-Q (2026-09-30)", "quote": "\"value\": \"209000000\"", "paragraph_id": "0001783180-26-000032:facts:LossContingencyAccrualAtCarryingValue:2026-06-30:us-gaap:LossContingenciesByNatureOfContingencyAxis=carr:AsbestosMattersMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_asbestos_insurance_receivable", "what_changed": "The asbestos-related insurance receivable is 89000000 at 2026-06-30, against 92000000 at 2025-12-31.", "account": "LossContingencyReceivable, asbestos matters", "expected_direction": "down", "horizon": "next 10-Q (2026-09-30)", "quote": "\"value\": \"89000000\"", "paragraph_id": "0001783180-26-000032:facts:LossContingencyReceivable:2026-06-30:us-gaap:LossContingenciesByNatureOfContingencyAxis=carr:AsbestosMattersMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_environmental_accrual", "what_changed": "The environmental loss-contingency accrual is 200000000 at 2026-06-30 and 200000000 at 2025-12-31. The current part is 20000000 against 18000000; the noncurrent part is 180000000 against 182000000.", "account": "AccrualForEnvironmentalLossContingencies", "expected_direction": "none", "horizon": "next 10-Q (2026-09-30)", "quote": "\"value\": \"200000000\"", "paragraph_id": "0001783180-26-000032:facts:AccrualForEnvironmentalLossContingencies:2026-06-30" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_aqueous_film_forming_foam_insurance_recoveries", "what_changed": "Estimated insurance recoveries for the pending aqueous film-forming foam litigation are 2400000000 at 2026-06-30. The value is tagged at hundred-million precision (decimals -8).", "account": "EstimatedInsuranceRecoveries, AFFF pending litigation", "expected_direction": "none", "horizon": "open-ended; next filing that updates the AFFF matter", "quote": "\"value\": \"2400000000\"", "paragraph_id": "0001783180-26-000032:facts:EstimatedInsuranceRecoveries:2026-06-30:srt:LitigationCaseAxis=carr:AqueousFilmFormingFoamMember,us-gaap:LitigationStatusAxis=us-gaap:PendingLitigationMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_aqueous_film_forming_foam_accrual_history", "what_changed": "The 10-Q repeats earlier AFFF accrual figures: 565000000 at 2024-12-31 and 50000000 at 2023-05-14. No AFFF accrual at 2026-06-30 is among the facts I can quote.", "account": "LossContingencyAccrualAtCarryingValue, AFFF pending litigation", "expected_direction": "none", "horizon": "open-ended; next filing that updates the AFFF matter", "quote": "\"value\": \"565000000\"", "paragraph_id": "0001783180-26-000032:facts:LossContingencyAccrualAtCarryingValue:2024-12-31:srt:LitigationCaseAxis=carr:AqueousFilmFormingFoamMember,us-gaap:LitigationStatusAxis=us-gaap:PendingLitigationMember" }
```

**Earnings release (8-K 0001783180-26-000030): figures and statements against the 10-Q**

```json
{ "id": "across_documents_release_and_quarterly_filing_agree", "what_changed": "The 8-K and the 10-Q facts print the same headline figures for the quarter ended 2026-06-30. Net sales: 6,351 million against 6351000000. Operating profit: 825 against 825000000. Net income attributable: 501 against 501000000. Effective tax rate: 25.0% against 0.250. The balance sheet also agrees: receivables 3,246 against 3246000000, inventories 2,759 against 2759000000. No disagreement was found in the rows compared.", "account": "RevenueFromContractWithCustomerExcludingAssessedTax (release against filing)", "expected_direction": "none", "horizon": "next 8-K and 10-Q pair", "quote": "\"value\": \"6351000000\"", "paragraph_id": "0001783180-26-000032:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30" }
```

```json
{ "id": "across_documents_free_cash_flow_definition_versus_reconciliation", "what_changed": "The release defines free cash flow as starting from cash flows of continuing operating activities. Its reconciliation tables (paragraphs 44 and 119) start instead from the total operating-activities line: 927 for the quarter and 1,006 for the six months. The cash flow statement (paragraph 93) prints continuing operating cash of 888 for the quarter and 953 for the six months, and discontinued operating cash of 39 and 53 (385 and 380 a year earlier). The reported free cash flow therefore rests on a larger line than the stated definition. I did not compute the figure on the stated definition.", "account": "Free cash flow (non-GAAP)", "expected_direction": "down", "horizon": "next earnings release", "quote": "Free cash flow is a non-GAAP financial measure that represents net cash flows provided by continuing operating activities (a GAAP measure) less capital expenditures.", "paragraph_id": "0001783180-26-000030:8k_2_02:78" }
```

```json
{ "id": "results_against_expectations_management_claims_beat", "what_changed": "insufficient. Management calls the quarter better than expected. My input holds no consensus or other expectation figure, so the claim cannot be checked against a number.", "account": "Reported results against expectations", "expected_direction": "none", "horizon": "none; no expectation data in input", "quote": "today reported better than expected financial results for the second quarter of 2026.", "paragraph_id": "0001783180-26-000030:8k_2_02:13" }
```

```json
{ "id": "results_against_expectations_full_year_outlook_raised", "what_changed": "Full-year guidance is raised to ~$23B sales, ~$3.5B adjusted operating profit and ~$2.90 adjusted EPS. The prior guidance printed in paragraph 48 was ~$22 billion, ~$3.4 billion and ~$2.80. Free-cash-flow guidance is unchanged at ~$2 billion.", "account": "Full-year 2026 guidance (sales, adjusted operating profit, adjusted EPS)", "expected_direction": "up", "horizon": "fiscal 2026", "quote": "Raises full year outlook to ~$23B sales, ~$3.5B adj. op. profit and ~$2.90 adj. EPS", "paragraph_id": "0001783180-26-000030:8k_2_02:11" }
```

```json
{ "id": "results_against_expectations_outlook_absorbs_exit_and_factory_costs", "what_changed": "The raised outlook includes a stated negative adjusted-EPS effect from the NORESCO exit and new U.S. factory costs. Guidance also carries year-over-year revenue headwinds from the Riello and NORESCO exits (paragraph 48).", "account": "Adjusted EPS guidance", "expected_direction": "down", "horizon": "fiscal 2026", "quote": "Includes ~($0.05) adj. EPS impact from NORESCO exit and new U.S. factory costs", "paragraph_id": "0001783180-26-000030:8k_2_02:12" }
```

```json
{ "id": "results_against_expectations_orders_growth", "what_changed": "The release reports order growth. Orders are a non-GAAP operating measure with no XBRL fact in my input, so the figure cannot be checked against filed numbers.", "account": "Orders (non-GAAP)", "expected_direction": "up", "horizon": "next two quarters of revenue", "quote": "Total company orders1 up ~40%; Commercial HVAC1 up ~65%; data centers up >300%", "paragraph_id": "0001783180-26-000030:8k_2_02:6" }
```

```json
{ "id": "results_against_expectations_eps_decline", "what_changed": "GAAP EPS from continuing operations fell to $0.60 and adjusted EPS to $0.86, against $0.70 and $0.92 a year earlier (paragraph 19).", "account": "Diluted EPS, continuing operations (GAAP and adjusted)", "expected_direction": "down", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "GAAP EPS from continuing operations was $0.60 and adjusted EPS was $0.86, down 14% and 7% year-over-year, respectively.", "paragraph_id": "0001783180-26-000030:8k_2_02:22" }
```

```json
{ "id": "revenue_recognition_net_sales_growth", "what_changed": "Net sales rose, with the organic and currency components as the release states them. The 10-Q fact prints 6351000000 against 6113000000.", "account": "Net sales", "expected_direction": "up", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "second-quarter sales of $6.4 billion increased 4% compared to the prior year. Organic sales increased 3% and foreign currency translation was a tailwind of 1%.", "paragraph_id": "0001783180-26-000030:8k_2_02:20" }
```

```json
{ "id": "revenue_recognition_americas_commercial_delivery_timing", "what_changed": "CSA commercial sales fell, attributed to the timing of customer deliveries. Over the same period, current contract liabilities rose from 691000000 (2025-12-31) to 816000000 (2026-06-30) and receivables rose. The link between the two is management's explanation, not a figure in my input.", "account": "CSA Commercial revenue", "expected_direction": "down", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "partially offset by Commercial1, down 8% due to the timing of customer deliveries.", "paragraph_id": "0001783180-26-000030:8k_2_02:26" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_adjusted_margin_input_costs_and_mix", "what_changed": "Adjusted operating margin fell to 17.2% from 19.1%. GAAP operating margin fell to 13.0% from 14.8% (paragraph 19). The release attributes the fall to input costs and business mix.", "account": "Adjusted operating margin (non-GAAP)", "expected_direction": "down", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "Adjusted operating margin of 17.2% was down 190 basis points from last year, predominantly due to favorable volume and productivity more than offset by the impact of increased input costs and unfavorable business mix.", "paragraph_id": "0001783180-26-000030:8k_2_02:21" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_americas_price_offset_by_mix", "what_changed": "CSA segment margin fell to 24.4% from 27.0%. The release says the revenue growth came mainly from price and was more than offset by mix and input costs.", "account": "CSA segment operating margin", "expected_direction": "down", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "Segment operating margin decreased 260 basis points as revenue growth mainly related to price which was more than offset by unfavorable mix and input costs.", "paragraph_id": "0001783180-26-000030:8k_2_02:27" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_europe_mix_and_selling_investments", "what_changed": "CSE segment margin fell to 7.2% from 7.9%, attributed to mix and selling investments.", "account": "CSE segment operating margin", "expected_direction": "down", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "Segment operating margin decreased 70 basis points driven by volume growth and favorable price / cost more than offset by unfavorable mix and selling investments.", "paragraph_id": "0001783180-26-000030:8k_2_02:31" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_china_residential_pressure", "what_changed": "The release names continued pressure in residential and light commercial in China within CSAME.", "account": "CSAME segment sales", "expected_direction": "down", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "partially offset by continued pressure in RLC in China.", "paragraph_id": "0001783180-26-000030:8k_2_02:36" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_middle_east_joint_venture_income", "what_changed": "CSAME margin fell to 11.8% from 15.3%. The release attributes part of the fall to lower JV income tied to the Middle East conflict. The CSAME equity-method earnings fact is 25000000 against 30000000.", "account": "CSAME segment operating margin and equity-method income", "expected_direction": "down", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "lower JV income due to the impacts from the Middle East conflict.", "paragraph_id": "0001783180-26-000030:8k_2_02:37" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_truck_and_trailer_declines", "what_changed": "CST organic sales were flat. Container growth offset low-teens declines in Global Truck and Trailer, and CST margin fell to 16.0% from 17.6%.", "account": "CST segment sales", "expected_direction": "down", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "Organic sales were flat as strong Container growth of ~40% was offset by low-teens declines in Global Truck and Trailer.", "paragraph_id": "0001783180-26-000030:8k_2_02:40" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_riello_sale_completed_after_period_end", "what_changed": "The Riello sale closed on July 1, after the 2026-06-30 balance-sheet date, so the disposal group is still on the balance sheet as held for sale (815000000 assets, 414000000 liabilities). The NORESCO divestiture is announced.", "account": "Disposal groups (Riello, NORESCO)", "expected_direction": "none", "horizon": "next 10-Q (2026-09-30)", "quote": "Riello divestiture completed on July 1st. NORESCO divestiture announced.", "paragraph_id": "0001783180-26-000030:8k_2_02:49" }
```

```json
{ "id": "earnings_quality_adjusted_versus_reported_earnings", "what_changed": "Adjusted and GAAP earnings from continuing operations differ for the quarter. For the six months the figures are 1,203 adjusted against 739 GAAP (paragraph 111); a year earlier they were 796 against 608 for the quarter (paragraph 116). The trend table's non_gaap_gap is not filled, and I did not compute the gap.", "account": "Adjusted net earnings against GAAP net earnings (continuing operations)", "expected_direction": "none", "horizon": "next earnings release", "quote": "Net earnings from continuing operations were $501 million and adjusted net earnings from continuing operations were $721 million.", "paragraph_id": "0001783180-26-000030:8k_2_02:22" }
```

```json
{ "id": "estimates_and_discretion_reported_and_adjusted_tax_rates", "what_changed": "Reported effective tax rate is 25.0% for the quarter against an adjusted 23.2%. For the six months it is 9.4% reported against 15.1% adjusted. A year earlier (paragraph 116) the quarter was 20.0% reported against 22.1% adjusted.", "account": "Effective tax rate, reported and adjusted", "expected_direction": "up", "horizon": "next earnings release", "quote": "| Effective tax rate | 25.0 | % |  |  |  | 23.2 | % |  | 9.4 | % |  |  |  | 15.1 | % |", "paragraph_id": "0001783180-26-000030:8k_2_02:111" }
```

```json
{ "id": "earnings_quality_payables_and_accruals_cash_contribution", "what_changed": "Accounts payable and accrued liabilities contributed 280 to operating cash in the quarter, against (103) a year earlier; for the six months, 631 against 378. The balance sheet shows accounts payable of 3,216 against 2,702 at 2025-12-31.", "account": "Change in accounts payable and accrued liabilities (cash flow)", "expected_direction": "up", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "| Accounts payable and accrued liabilities |  | 280 |  |  | (103) |  |  | 631 |  |  | 378 |  |", "paragraph_id": "0001783180-26-000030:8k_2_02:93" }
```

```json
{ "id": "earnings_quality_other_operating_activities_cash", "what_changed": "Other operating activities, net contributed 122 to operating cash in the quarter, against 5 a year earlier; for the six months, 83 against (47).", "account": "Other operating activities, net (cash flow)", "expected_direction": "up", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "| Other operating activities, net |  | 122 |  |  | 5 |  |  | 83 |  |  | (47) |  |", "paragraph_id": "0001783180-26-000030:8k_2_02:93" }
```

```json
{ "id": "earnings_quality_equity_method_distributions", "what_changed": "Distributions from equity-method investments are 39 in the quarter against 4 a year earlier, while equity-method earnings are 58 against 78. For the six months, distributions are 51 against 81.", "account": "Distributions from equity method investments (cash flow)", "expected_direction": "up", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "| Distributions from equity method investments |  | 39 |  |  | 4 |  |  | 51 |  |  | 81 |  |", "paragraph_id": "0001783180-26-000030:8k_2_02:93" }
```

```json
{ "id": "earnings_quality_discontinued_operating_cash", "what_changed": "Discontinued operating cash flow is 39 in the quarter against 385 a year earlier; for the six months, 53 against 380. It is part of the total operating-cash line that the free cash flow reconciliation starts from.", "account": "Net cash flows from discontinued operating activities", "expected_direction": "down", "horizon": "next 10-Q (quarter ending 2026-09-30)", "quote": "| Net cash flows provided by (used in) discontinued operating activities |  | 39 |  |  | 385 |  |  | 53 |  |  | 380 |  |", "paragraph_id": "0001783180-26-000030:8k_2_02:93" }
```

```json
{ "id": "earnings_quality_free_cash_flow_comparison", "what_changed": "The release's free cash flow is 810 for the quarter against 568 a year earlier, and 795 for the six months against 988. Capital expenditures are (117) against (81) for the quarter and (211) against (144) for the six months.", "account": "Free cash flow (non-GAAP, as reconciled in the release)", "expected_direction": "up", "horizon": "next earnings release", "quote": "| Free cash flow |  | $ | 810 |  |  | $ | 568 |  |  | $ | 795 |  |  | $ | 988 |  |", "paragraph_id": "0001783180-26-000030:8k_2_02:44" }
```

```json
{ "id": "liquidity_and_capital_net_debt", "what_changed": "The release's net debt is 10,608 at 2026-06-30 against 10,278 at 2025-12-31. Cash is 1,344 against 1,555; current debt 1,638 against 468; long-term debt 10,314 against 11,365.", "account": "Net debt (non-GAAP)", "expected_direction": "up", "horizon": "next 10-Q (2026-09-30)", "quote": "| Net debt |  | $ | 10,608 |  |  | $ | 10,278 |  |", "paragraph_id": "0001783180-26-000030:8k_2_02:121" }
```

```json
{ "id": "liquidity_and_capital_total_equity_decline", "what_changed": "Total equity is 13,472 at 2026-06-30 against 14,128 at 2025-12-31. Treasury stock is (7,550) against (6,795), and accumulated other comprehensive loss (537) against (269).", "account": "Total Equity", "expected_direction": "down", "horizon": "next 10-Q (2026-09-30)", "quote": "| Total Equity |  | 13,472 |  |  | 14,128 |  |", "paragraph_id": "0001783180-26-000030:8k_2_02:88" }
```

```json
{ "id": "liquidity_and_capital_accounts_payable_balance", "what_changed": "Accounts payable is 3,216 at 2026-06-30 against 2,702 at 2025-12-31, and accrued liabilities 3,963 against 3,774. Total current liabilities are 9,231 against 7,114.", "account": "Accounts payable", "expected_direction": "up", "horizon": "next 10-Q (2026-09-30)", "quote": "| Accounts payable |  | $ | 3,216 |  |  | $ | 2,702 |  |", "paragraph_id": "0001783180-26-000030:8k_2_02:88" }
```

```json
{ "id": "estimates_and_discretion_intangible_assets_decline", "what_changed": "Intangible assets, net are 5,756 at 2026-06-30 against 6,326 at 2025-12-31. Amortization of acquired intangibles is 426 for the six months (paragraph 105).", "account": "Intangible assets, net", "expected_direction": "down", "horizon": "next 10-Q (2026-09-30)", "quote": "| Intangible assets, net |  | 5,756 |  |  | 6,326 |  |", "paragraph_id": "0001783180-26-000030:8k_2_02:88" }
```

## Seen in the notes

No items. No fact in input_numbers.json carries a marker saying whether its element sat inside a note: each fact prints only id, paragraph_id, tag, prefix, namespace, context, context_ref, unit, decimals, value, number, nil, form, source_accession, filing_date and, on some rows, superseded_by. With nothing to sort by, every fact item stays under "Seen in the statements". That includes the segment, disposal-group, tax-reconciliation, restructuring and contingency tables. When the marker exists, those are the items to re-sort.
