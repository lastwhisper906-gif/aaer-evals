<!-- the quote gate removed 2 item(s) from this copy; input_manifest.json lists each with its reason -->
# AMSC — numbers reader — 10-Q 0001437749-26-025922, quarter ended 2026-06-30

Inputs read: input_trends.json (in full), input_8k.md (in full), input_prior_predictions.md (in full: "None on record"), input_numbers.json (in part — see the last note below). Nothing in the directory holds prices, returns, short interest, another company's files, a prior probability or an outcome window.

Notes that are not items, because there is nothing to quote for them:

- **Periods the record does not reach.** quarters-back-1 (target end 2026-03-31) and quarters-back-5 (target end 2025-04-01) have no cells. The reason each gives: no quarter ending within 20 days of the target date is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py. As a result, no quarter-over-quarter change exists for quarters-back-0 on any metric.
- **Inputs that do not exist in my directory.** There are no articulation checks, no restatement traces and no fourth-quarter derivation (the src/fourth_quarter.py output). So I can report no articulation gap and no Python-traced restatement. input_numbers.json holds only `documents` and `facts`.
- **Tag changes.** Nothing in my input says a period rests on a different concept. Every trend input for every filled period uses the same tag per role: RevenueFromContractWithCustomerIncludingAssessedTax, CostOfRevenue, AccountsReceivableNetCurrent, InventoryNet, ContractWithCustomerLiabilityCurrent, ProductWarrantyAccrual, InventoryValuationReserves, Assets, CashAndCashEquivalentsAtCarryingValue, PropertyPlantAndEquipmentNet, NetIncomeLoss and NetCashProvidedByUsedInOperatingActivities.
- **Restated prior values.** None is traced, because there are no restatement traces. The fact rows I read put the same figure on both sides of each overlap. The 10-K (0001437749-26-018542) rows for 2026-03-31 for cash, receivables, inventory, prepaid, restricted cash, current assets, PP&E, intangibles, right-of-use assets, goodwill, noncurrent restricted cash, deferred tax assets, equity-method investments, other assets, total assets, payables, lease liabilities, contingent consideration (current), contract liabilities (current and noncurrent) and current liabilities match the 10-Q (0001437749-26-025922) rows for the same date. The prior 10-Q (0001437749-26-002978) rows for 2025-03-31 match the 10-K rows for the same date. These rows carry `superseded_by`, which marks a later filing reporting the same element; it is not a statement that the value changed. One near-overlap with different concepts is listed as an item (articulation_and_the_filed_history_comtrafo_goodwill_two_figures).
- **R&D capitalization baseline (years-back-0).** It prints book_value_with_rnd_capitalized 590806000.0 and research_and_development_asset 35359000.0. earnings_with_rnd_capitalized and research_and_development_amortization are missing: "5 year(s) back: no row for research_and_development_expense in 2020-04-01..2021-03-31". capitalized_development_cost and capitalized_over_expense are missing because the record tags no us-gaap:CapitalizedComputerSoftwareAdditions. None of these values prints a paragraph_id, so none is an item.
- **8-K index rows** carry no paragraph id, so they are not items. The index shows a 4.02 non-reliance item on 2011-07-11 (0000950123-11-064934), a 4.01 auditor-change item on 2013-08-21, and NT 10-K / NT 10-Q notices in 2011. Nothing comparable appears after 2013. On 2026-02-17 there is a 9.01-only amendment of the 2025-12-10 acquisition 8-K (0001193125-25-314153).
- **Coverage of input_numbers.json — the file was not read in full.** It is 68,330 lines, more than this run could hold. I read: lines 1–1,900 (start of the prior 10-Q block, including its balance sheet); lines 27,000–28,030 (the 10-K balance sheet); lines 46,880–47,005 (10-K income-tax rows); lines 52,200–56,940 (end of the 10-K block, then the current 10-Q balance sheet, income statement and equity statement); lines 58,800–60,200 (end of the current 10-Q cash flow statement and the Comtrafo acquisition note); and lines 67,000–68,330 (segment table and closing rows). I also took short samples elsewhere. Most of the prior 10-Q block, most of the 10-K block and lines 56,940–58,800 and 60,200–67,000 of the current 10-Q were not read. Rows there — including any restated value or tag change printed only there — are not reflected in this report.

## Seen in the statements

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly", "what_changed": "Accruals over total assets for the quarter ended 2026-06-30 is -0.008557930353167143 (net income 9490000.0 and operating cash flow 16013000.0 over assets 762217000.0, all from 0001437749-26-025922). Year-over-year change against quarters-back-4 is -0.014297188290744157 (that cell is 0.005739257937577013). There is no quarter-over-quarter change: the cell says accruals_over_total_assets is not filled in quarters-back-1. Position: lowest of the 2 filled quarters. Two filled quarters are insufficient for a trend claim.", "account": "accruals (net income less operating cash flow) over total assets", "expected_direction": "none", "horizon": "none; insufficient history", "quote": "\"position_in_history\": \"lowest of the 2 filled quarters\",", "paragraph_id": "0001437749-26-025922:trends:accruals_over_total_assets:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly", "what_changed": "insufficient. The cell for the quarter ended 2026-06-30 is not filled; the record holds no allowance row for 2026-06-30. Coverage prints this ratio as filled 0, so there is no value, change or position in any quarter or year.", "account": "allowance for credit losses over receivables", "expected_direction": "none", "horizon": "none; insufficient", "quote": "\"missing\": \"no row for bad_debt_allowance in 2026-06-30: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\",", "paragraph_id": "0001437749-26-025922:trends:bad_debt_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly", "what_changed": "Current contract liabilities over quarterly revenue is 0.9024480988168763 (ContractWithCustomerLiabilityCurrent 84896000.0 over revenue 94073000.0). Year-over-year change against quarters-back-4 is -0.010443357552840982 (that cell is 0.9128914563697172). There is no quarter-over-quarter change: the cell says contract_liabilities_over_revenue is not filled in quarters-back-1. Position: second lowest of the 6 filled quarters.", "account": "deferred revenue, current portion, over revenue", "expected_direction": "none", "horizon": "next quarter", "quote": "\"position_in_history\": \"second lowest of the 6 filled quarters\",", "paragraph_id": "0001437749-26-025922:trends:contract_liabilities_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_days_sales_of_inventory_quarterly", "what_changed": "Days sales of inventory is 128.6219591330555 (InventoryNet 98017000.0 over CostOfRevenue 69347000.0 for a 91-day quarter). Year-over-year change against quarters-back-4 is -7.494985027048131 (that cell is 136.11694416010363). There is no quarter-over-quarter change: the cell says days_sales_of_inventory is not filled in quarters-back-1. Position: lowest of the 6 filled quarters.", "account": "inventory, net, against cost of revenue", "expected_direction": "none", "horizon": "next quarter", "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\",", "paragraph_id": "0001437749-26-025922:trends:days_sales_of_inventory:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly", "what_changed": "Days sales outstanding is 78.0986680556589 (AccountsReceivableNetCurrent 80736000.0 over revenue 94073000.0 for a 91-day quarter). Year-over-year change against quarters-back-4 is 9.326120445166637 (that cell is 68.77254761049227). There is no quarter-over-quarter change: the cell says days_sales_outstanding is not filled in quarters-back-1. Position: second highest of the 6 filled quarters; the highest is quarters-back-3 at 87.41690200722724.", "account": "accounts receivable, net, against revenue", "expected_direction": "down", "horizon": "next two quarters", "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\",", "paragraph_id": "0001437749-26-025922:trends:days_sales_outstanding:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly", "what_changed": "Gross margin is 0.26283843398212026 (revenue 94073000.0, cost of revenue 69347000.0). Year-over-year change against quarters-back-4 is -0.07560375623872612; that cell is 0.3384421902208464, the highest of the 6 filled quarters. There is no quarter-over-quarter change: the cell says gross_margin is not filled in quarters-back-1. Position: lowest of the 6 filled quarters.", "account": "gross margin", "expected_direction": "down", "horizon": "next quarter", "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\",", "paragraph_id": "0001437749-26-025922:trends:gross_margin:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly", "what_changed": "insufficient. The quarterly cell is not filled: InventoryValuationReserves is in the record, but not for 2026-06-30. Coverage prints this ratio as filled 5, all of them fiscal years; no quarter is filled, so no quarterly value, change or position exists.", "account": "inventory valuation reserve over inventory", "expected_direction": "none", "horizon": "none; insufficient", "quote": "\"missing\": \"no row for inventory_reserve in 2026-06-30: us-gaap:InventoryValuationReserves is in the record, but not for this period\",", "paragraph_id": "0001437749-26-025922:trends:inventory_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly", "what_changed": "insufficient. The cell is empty because companyfacts carries no non-GAAP measure; coverage prints this ratio as filled 0 in every period. The 8-K release does print a non-GAAP figure; see earnings_quality_non_gaap_net_income_below_gaap.", "account": "non-GAAP net income against GAAP net income", "expected_direction": "none", "horizon": "none; insufficient", "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\",", "paragraph_id": "0001437749-26-025922:trends:non_gaap_gap:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarterly", "what_changed": "Receivables over quarterly revenue is 0.8582271214907572 (80736000.0 over 94073000.0). Year-over-year change against quarters-back-4 is 0.10248484005677616 (that cell is 0.755742281433981). There is no quarter-over-quarter change: the cell says receivables_over_revenue is not filled in quarters-back-1. Position: second highest of the 6 filled quarters; the highest is quarters-back-3 at 0.9501837174698612.", "account": "accounts receivable, net, over revenue", "expected_direction": "down", "horizon": "next two quarters", "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\",", "paragraph_id": "0001437749-26-025922:trends:receivables_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "structure_and_disclosure_changes_soft_asset_share_quarterly", "what_changed": "Soft-asset share is 0.6818989867714838 (assets 762217000.0, PP&E 98755000.0, cash 143707000.0). Year-over-year change against quarters-back-4 is 0.22603761226447694 (that cell is 0.4558613745070068). There is no quarter-over-quarter change: the cell says soft_asset_share is not filled in quarters-back-1. Position: second highest of the 6 filled quarters; the highest is quarters-back-2 at 0.6824013875647293.", "account": "assets other than PP&E and cash, over total assets", "expected_direction": "none", "horizon": "next fiscal year", "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\",", "paragraph_id": "0001437749-26-025922:trends:soft_asset_share:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly", "what_changed": "Warranty accrual over quarterly revenue is 0.051034834649686944 (ProductWarrantyAccrual 4801000.0 over 94073000.0). Year-over-year change against quarters-back-4 is 0.006257477619365487; that cell is 0.04477735703032146, the lowest of the 6 filled quarters. There is no quarter-over-quarter change: the cell says warranty_reserve_ratio is not filled in quarters-back-1. Position: third highest of the 6 filled quarters.", "account": "product warranty accrual over revenue", "expected_direction": "none", "horizon": "next quarter", "quote": "\"position_in_history\": \"third highest of the 6 filled quarters\",", "paragraph_id": "0001437749-26-025922:trends:warranty_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_annual", "what_changed": "Accruals over total assets for the fiscal year ended 2026-03-31 is 0.14964684691019783 (net income 133809000.0 and operating cash flow 23148000.0 from 0001437749-26-018542; assets 739481000.0 from 0001437749-26-025922). Year-over-year change against years-back-1 is 0.22130705668667028; that cell is -0.07166020977647244, the lowest of the 5 filled years. Position: highest of the 5 filled years. The tax rows behind the net income are in earnings_quality_annual_tax_benefit_against_operating_income.", "account": "accruals (net income less operating cash flow) over total assets", "expected_direction": "down", "horizon": "next fiscal year", "quote": "\"position_in_history\": \"highest of the 5 filled years\",", "paragraph_id": "0001437749-26-025922:trends:accruals_over_total_assets:2025-04-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual", "what_changed": "insufficient. The annual cell for the fiscal year ended 2026-03-31 is not filled; the record holds no allowance row for 2026-03-31, and none for any of the five year-ends.", "account": "allowance for credit losses over receivables", "expected_direction": "none", "horizon": "none; insufficient", "quote": "\"missing\": \"no row for bad_debt_allowance in 2026-03-31: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\",", "paragraph_id": "0001437749-26-025922:trends:bad_debt_reserve_ratio:2025-04-01..2026-03-31" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual", "what_changed": "Current contract liabilities over fiscal-year revenue is 0.26052046597917466 (77936000.0 at 2026-03-31 over 299155000.0). Year-over-year change against years-back-1 is -0.03926231638131683 (that cell is 0.2997827823604915). Position: second lowest of the 5 filled years.", "account": "deferred revenue, current portion, over revenue", "expected_direction": "none", "horizon": "next fiscal year", "quote": "\"position_in_history\": \"second lowest of the 5 filled years\",", "paragraph_id": "0001437749-26-025922:trends:contract_liabilities_over_revenue:2025-04-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_days_sales_of_inventory_annual", "what_changed": "Days sales of inventory for the fiscal year is 182.25406206684121 (InventoryNet 103748000.0 at 2026-03-31 over CostOfRevenue 207776000.0 for a 365-day year). Year-over-year change against years-back-1 is 20.87210709554327 (that cell is 161.38195497129794). Position: highest of the 5 filled years.", "account": "inventory, net, against cost of revenue", "expected_direction": "down", "horizon": "next fiscal year", "quote": "\"position_in_history\": \"highest of the 5 filled years\",", "paragraph_id": "0001437749-26-025922:trends:days_sales_of_inventory:2025-04-01..2026-03-31" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual", "what_changed": "Days sales outstanding for the fiscal year is 84.6519864284401 (receivables 69381000.0 at 2026-03-31 over revenue 299155000.0). Year-over-year change against years-back-1 is 8.994319633118351 (that cell is 75.65766679532175). Position: second highest of the 5 filled years; the highest is years-back-3 at 105.60768606582126.", "account": "accounts receivable, net, against revenue", "expected_direction": "down", "horizon": "next fiscal year", "quote": "\"position_in_history\": \"second highest of the 5 filled years\",", "paragraph_id": "0001437749-26-025922:trends:days_sales_outstanding:2025-04-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_gross_margin_annual", "what_changed": "Gross margin for the fiscal year is 0.3054570373217897 (revenue 299155000.0, cost of revenue 207776000.0). Year-over-year change against years-back-1 is 0.027858279591265245 (that cell is 0.27759875773052445). Position: highest of the 5 filled years. The latest quarter sits at the bottom of its own quarterly history (see earnings_quality_gross_margin_quarterly).", "account": "gross margin", "expected_direction": "none", "horizon": "next fiscal year", "quote": "\"position_in_history\": \"highest of the 5 filled years\",", "paragraph_id": "0001437749-26-025922:trends:gross_margin:2025-04-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_annual", "what_changed": "Inventory reserve over inventory is 0.033735590083664266 (InventoryValuationReserves 3500000.0 from 0001437749-26-018542 over InventoryNet 103748000.0). Year-over-year change against years-back-1 is 0.012658997747113241; that cell is 0.021076592336551025, the lowest of the 5 filled years. Position: second lowest of the 5 filled years; the highest is years-back-4 at 0.08028395166061016.", "account": "inventory valuation reserve over inventory", "expected_direction": "none", "horizon": "next fiscal year", "quote": "\"position_in_history\": \"second lowest of the 5 filled years\",", "paragraph_id": "0001437749-26-025922:trends:inventory_reserve_ratio:2025-04-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual", "what_changed": "insufficient. The annual cell for the fiscal year ended 2026-03-31 is empty because companyfacts carries no non-GAAP measure; no year is filled.", "account": "non-GAAP net income against GAAP net income", "expected_direction": "none", "horizon": "none; insufficient", "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\",", "paragraph_id": "0001437749-26-025922:trends:non_gaap_gap:2025-04-01..2026-03-31" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual", "what_changed": "Receivables over fiscal-year revenue is 0.231923250488877 (69381000.0 over 299155000.0). Year-over-year change against years-back-1 is 0.02464197159758455 (that cell is 0.20728127889129244). Position: second highest of the 5 filled years; the highest is years-back-3 at 0.28933612620772947.", "account": "accounts receivable, net, over revenue", "expected_direction": "down", "horizon": "next fiscal year", "quote": "\"position_in_history\": \"second highest of the 5 filled years\",", "paragraph_id": "0001437749-26-025922:trends:receivables_over_revenue:2025-04-01..2026-03-31" }
```

```json
{ "id": "structure_and_disclosure_changes_soft_asset_share_annual", "what_changed": "Soft-asset share at 2026-03-31 is 0.6883381723127436 (assets 739481000.0, PP&E 89775000.0, cash 140693000.0). Year-over-year change against years-back-1 is 0.06855722352023041 (that cell is 0.6197809487925132). Position: second highest of the 5 filled years; the highest is years-back-3 at 0.7968284527884895.", "account": "assets other than PP&E and cash, over total assets", "expected_direction": "none", "horizon": "next fiscal year", "quote": "\"position_in_history\": \"second highest of the 5 filled years\",", "paragraph_id": "0001437749-26-025922:trends:soft_asset_share:2025-04-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_annual", "what_changed": "Warranty accrual over fiscal-year revenue is 0.01565743510889004 (ProductWarrantyAccrual 4684000.0 at 2026-03-31 over 299155000.0). Year-over-year change against years-back-1 is 0.002045428897542662; that cell is 0.013612006211347378, the lowest of the 5 filled years. Position: second lowest of the 5 filled years.", "account": "product warranty accrual over revenue", "expected_direction": "none", "horizon": "next fiscal year", "quote": "\"position_in_history\": \"second lowest of the 5 filled years\",", "paragraph_id": "0001437749-26-025922:trends:warranty_reserve_ratio:2025-04-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_accruals_discrete_quarter_cash_flow_absent", "what_changed": "insufficient. The accruals cell for the quarter ended 2025-12-31 is not filled because the record holds no operating cash flow for that discrete quarter. The cells for the quarters ended 2025-09-30, 2024-12-31 and 2024-09-30 give the same reason for their own periods. Accruals therefore fills only quarters-back-0 and quarters-back-4, and no quarterly accruals trend exists.", "account": "operating cash flow for second and third fiscal quarters", "expected_direction": "none", "horizon": "none; insufficient", "quote": "\"missing\": \"no row for operating_cash_flow in 2025-10-01..2025-12-31: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\",", "paragraph_id": "0001437749-26-025922:trends:accruals_over_total_assets:2025-10-01..2025-12-31" }
```


```json
{ "id": "earnings_quality_annual_tax_benefit_against_operating_income", "what_changed": "The 10-K prints income tax expense (benefit) of -117061000 for the fiscal year ended 2026-03-31, against -3667000 the year before. Deferred income tax expense (benefit) prints -118683000 against -4304000. Operating income for the year prints 11445000 against -1077000, while net income (the accruals input) is 133809000.0 and operating cash flow 23148000.0. DeferredIncomeTaxAssetsNet prints 1178000 at 2025-03-31, 117342000 at 2025-12-31 (0001437749-26-002978), 119474000 at 2026-03-31 and 119754000 at 2026-06-30. The latest quarter prints tax expense of 1262000 against 199000 a year earlier.", "account": "income tax expense (benefit); deferred tax assets", "expected_direction": "down", "horizon": "next fiscal year", "quote": "\"value\": \"-117061000\",", "paragraph_id": "0001437749-26-018542:facts:IncomeTaxExpenseBenefit:2025-04-01..2026-03-31" }
```


```json
{ "id": "earnings_quality_segment_reconciling_item_contingent_consideration", "what_changed": "The reconciling item between segment and consolidated operating income prints 8115000 for the quarter ended 2026-06-30 and 0 for the quarter ended 2025-06-30. The segment-expense reconciling row prints -8115000. The statement of operations tags the same amount as a fair-value liability gain included in earnings of 8115000 (prior-year quarter -0), and a corporate change in contingent consideration liability prints 8100000.", "account": "change in fair value of contingent consideration", "expected_direction": "down", "horizon": "next quarter", "quote": "\"value\": \"8115000\",", "paragraph_id": "0001437749-26-025922:facts:OperatingIncomeLoss:2026-04-01..2026-06-30:srt:ConsolidationItemsAxis=us-gaap:MaterialReconcilingItemsMember" }
```

```json
{ "id": "estimates_and_discretion_contingent_consideration_earnout_range", "what_changed": "The 10-Q tags the high end of the Comtrafo contingent-consideration range at BRL 382500000 at the 2025-12-05 acquisition date. Consideration transferred prints 202900000 (USD): 88300000 cash, 79800000 equity (2417142 shares at a share price of 33.01) and 34800000 of liabilities incurred. Recorded contingent consideration prints 3959000 current and 27930000 long-term at 2026-06-30, after the quarter's 8115000 fair-value gain. The release says its next-quarter net income guidance assumes no further change in this fair value.", "account": "contingent consideration (Comtrafo earnout)", "expected_direction": "down", "horizon": "next fiscal year", "quote": "\"value\": \"382500000\",", "paragraph_id": "0001437749-26-025922:facts:BusinessCombinationContingentConsiderationArrangementsRangeOfOutcomesValueHigh:2025-12-05:us-gaap:BusinessAcquisitionAxis=amsc:ComtrafoIndustriaDeTransformadoresEletricosSAMember:unit=iso4217:BRL" }
```

```json
{ "id": "structure_and_disclosure_changes_comtrafo_quarter_contribution", "what_changed": "The 10-Q tags Comtrafo's contribution for the quarter ended 2026-06-30 as revenue 19400000 and net income 9000000 (decimals -6), against consolidated net income of 9490000. Comtrafo-tagged cost of revenue prints 700000 and amortization of intangible assets 700000. Grid revenue from South America prints 21980000 against 248000 a year earlier; from North America 43162000 against 37772000. Pro forma net income for the quarter ended 2025-06-30 prints 9291000 (pro forma basic EPS 0.23). The input does not say whether the 8115000 contingent-consideration gain sits inside the Comtrafo net income.", "account": "acquired-business revenue and net income (Comtrafo)", "expected_direction": "none", "horizon": "next fiscal year", "quote": "\"value\": \"9000000\",", "paragraph_id": "0001437749-26-025922:facts:NetIncomeLoss:2026-04-01..2026-06-30:us-gaap:BusinessAcquisitionAxis=amsc:ComtrafoIndustriaDeTransformadoresEletricosSAMember" }
```

```json
{ "id": "estimates_and_discretion_comtrafo_acquired_receivables_uncollectible", "what_changed": "At the 2025-12-05 acquisition date the 10-Q tags Comtrafo receivables at a gross contractual amount of 10500000, a fair value of 6900000 and an estimated uncollectible amount of 3600000. The trend table holds no bad-debt allowance in any period (bad_debt_reserve_ratio filled 0), so no allowance trend exists to set this against.", "account": "acquired receivables, estimated uncollectible", "expected_direction": "none", "horizon": "next fiscal year", "quote": "\"value\": \"3600000\",", "paragraph_id": "0001437749-26-025922:facts:BusinessCombinationAcquiredReceivablesEstimatedUncollectible:2025-12-05:us-gaap:BusinessAcquisitionAxis=amsc:ComtrafoIndustriaDeTransformadoresEletricosSAMember" }
```

```json
{ "id": "articulation_and_the_filed_history_comtrafo_goodwill_two_figures", "what_changed": "The 10-Q filed 2026-08-05 tags Comtrafo goodwill at 2025-12-31 of 122700000. The 10-Q filed 2026-02-04 tagged goodwill acquired during the nine months ended 2025-12-31 of 122200000. The two rows are different concepts and periods and no restatement trace exists in my input, so I cannot say whether the allocation moved. The later 10-Q also tags a provisional measurement-period adjustment to inventory of 1500000 (dated 2025-12-05). Its allocation rows at 2025-12-31 print intangibles 10500000 (backlog 2600000, customer relationships 7900000), inventory 28600000, PP&E 49900000, receivables 6500000 and deferred revenue 23300000.", "account": "goodwill and purchase-price allocation (Comtrafo)", "expected_direction": "none", "horizon": "none", "quote": "\"value\": \"122700000\",", "paragraph_id": "0001437749-26-025922:facts:Goodwill:2025-12-31:us-gaap:BusinessAcquisitionAxis=amsc:ComtrafoIndustriaDeTransformadoresEletricosSAMember" }
```

```json
{ "id": "structure_and_disclosure_changes_goodwill_acquired_comtrafo", "what_changed": "The 10-Q filed 2026-02-04 prints goodwill acquired during the nine months ended 2025-12-31 of 122200000. Goodwill prints 48164000 at 2025-03-31, 166373000 at 2025-12-31, 175376000 at 2026-03-31 and 176678000 at 2026-06-30. The Comtrafo acquisition is tagged with 2417142 shares issued on 2025-12-05. The 10-K prints PP&E in South America of 51494000 at 2026-03-31 against 0 at 2025-03-31. Goodwill impairment prints 0 for the latest quarter.", "account": "goodwill; acquisition of Comtrafo", "expected_direction": "none", "horizon": "next fiscal year", "quote": "\"value\": \"122200000\",", "paragraph_id": "0001437749-26-002978:facts:GoodwillAcquiredDuringPeriod:2025-04-01..2025-12-31" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_property_payment_brazil", "what_changed": "The 10-K tags a payment to acquire property, plant and equipment of BRL 37200000 dated 2026-05-15 as a subsequent event. The 10-Q filed 2026-08-05 tags a BRL 37200000 payment on the same date without the subsequent-event axis. The quarter's cash flow statement prints purchases of PP&E of (10,438) thousand against (814).", "account": "payments to acquire property, plant and equipment (Brazilian reais)", "expected_direction": "none", "horizon": "next fiscal year", "quote": "\"value\": \"37200000\",", "paragraph_id": "0001437749-26-018542:facts:PaymentsToAcquirePropertyPlantAndEquipment:2026-05-15..2026-05-15:us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember:unit=iso4217:BRL" }
```

```json
{ "id": "revenue_recognition_customer_concentration_grid", "what_changed": "For the quarter ended 2026-06-30 the 10-Q tags Fuji Bridex at a maximum of 0.10 of Grid revenue (RangeAxis MaximumMember). The 10-Q filed 2026-02-04 tagged Innomotics at 0.10 of Grid revenue for the quarter and nine months ended 2025-12-31, and Fuji Bridex at a maximum of 0.10.", "account": "customer concentration, Grid revenue", "expected_direction": "none", "horizon": "none", "quote": "\"value\": \"0.10\",", "paragraph_id": "0001437749-26-025922:facts:ConcentrationRiskPercentage1:2026-04-01..2026-06-30:srt:MajorCustomersAxis=amsc:FujiBridexPteLtdMember,srt:RangeAxis=srt:MaximumMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:SalesRevenueNetMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember,us-gaap:StatementBusinessSegmentsAxis=amsc:GridMember" }
```

```json
{ "id": "earnings_quality_contingent_consideration_gain_within_operating_expenses", "what_changed": "The release's statement of operations prints a change in fair value of contingent consideration of (8,115) thousand inside operating expenses for the quarter ended 2026-06-30, against none a year earlier. Total operating expenses print 14,894 against 18,845 and operating income 9,832 against 5,644. The cash flow statement adds the same (8,115) as a non-cash item. The release says second-quarter net income guidance assumes no changes in fair value of contingent consideration.", "account": "change in fair value of contingent consideration (operating expenses)", "expected_direction": "down", "horizon": "next quarter", "quote": "| Change in fair value of contingent consideration |  |  | (8,115 | ) |  |  | — |  |", "paragraph_id": "0001437749-26-025921:8k_2_02:25" }
```

```json
{ "id": "earnings_quality_non_gaap_net_income_below_gaap", "what_changed": "The release prints non-GAAP net income of 7,615 thousand for the quarter ended 2026-06-30 against GAAP net income of 9,490. A year earlier it was 11,587 against 6,724. The reconciliation deducts the (8,115) contingent-consideration change and adds back stock-based compensation of 5,264 and acquisition amortization of 976. Non-GAAP net income per share (basic) prints 0.17 against 0.30.", "account": "non-GAAP net income", "expected_direction": "down", "horizon": "next quarter", "quote": "| Non-GAAP net income |  | $ | 7,615 |  |  | $ | 11,587 |  |", "paragraph_id": "0001437749-26-025921:8k_2_02:37" }
```

```json
{ "id": "across_documents_acquisition_amortization_two_figures", "what_changed": "In the same release, the statement of operations prints amortization of acquisition-related intangibles of 466 thousand for the quarter ended 2026-06-30, and the non-GAAP reconciliation adds back 976 under the same label; both print 337 for the year-earlier quarter. The 10-Q tags AmortizationOfAcquisitionCosts at 466000 for the quarter, and Comtrafo-tagged amortization of intangible assets at 700000 and Comtrafo-tagged cost of revenue at 700000. Neither the release nor the rows I read say why the two release rows differ.", "account": "amortization of acquisition-related intangibles", "expected_direction": "none", "horizon": "none", "quote": "| Amortization of acquisition-related intangibles |  |  | 976 |  |  |  | 337 |  |", "paragraph_id": "0001437749-26-025921:8k_2_02:37" }
```

```json
{ "id": "across_documents_non_gaap_tax_effect_not_shown", "what_changed": "The release's non-GAAP definition includes the tax effect of adjustments. The reconciliation table prints no tax-effect row: it runs from net income through stock-based compensation, acquisition amortization and the contingent-consideration change to non-GAAP net income.", "account": "non-GAAP reconciliation", "expected_direction": "none", "horizon": "none", "quote": "and the tax effect of adjustments calculated at the relevant rate for our non-GAAP metric", "paragraph_id": "0001437749-26-025921:8k_2_02:42" }
```

```json
{ "id": "results_against_expectations_revenue_guidance_below_reported", "what_changed": "Guidance for the quarter ending 2026-09-30 is revenue above $85.0 million, after reported revenue of $94.1 million for the quarter ended 2026-06-30. My input holds no consensus and no earlier guidance for this quarter, so results against outside expectations cannot be judged.", "account": "revenue guidance", "expected_direction": "down", "horizon": "quarter ending 2026-09-30", "quote": "For the second quarter ending September 30, 2026, AMSC expects that its revenues will exceed $85.0 million.", "paragraph_id": "0001437749-26-025921:8k_2_02:14" }
```

```json
{ "id": "results_against_expectations_net_income_guidance", "what_changed": "Guidance for the quarter ending 2026-09-30 is GAAP net income above $1.0 million ($0.02 per share) and non-GAAP net income above $8.0 million ($0.17 per share). The quarter ended 2026-06-30 reported $9.5 million ($0.21 per share), which includes the (8,115) thousand contingent-consideration change, and non-GAAP $7.6 million. The forecast reconciliation prints stock-based compensation of 6.3 and acquisition amortization of 0.7 (millions) and 46.5 million shares.", "account": "net income guidance", "expected_direction": "down", "horizon": "quarter ending 2026-09-30", "quote": "net income for the second quarter of fiscal 2026 is expected to exceed $1.0 million, or $0.02 per share.", "paragraph_id": "0001437749-26-025921:8k_2_02:14" }
```

```json
{ "id": "across_documents_gross_margin_improvement_claim", "what_changed": "Management says it is positioned for gross margin improvement in the second half of the fiscal year. The trend table puts the quarter's gross margin at 0.26283843398212026, the lowest of the 6 filled quarters. The release prints gross margin of 24,726 thousand on revenue of 94,073, against 24,489 on 72,358 a year earlier.", "account": "gross margin", "expected_direction": "none", "horizon": "second half of fiscal 2026", "quote": "believe we are well positioned for gross margin improvement in the second half of the fiscal year", "paragraph_id": "0001437749-26-025921:8k_2_02:11" }
```

```json
{ "id": "liquidity_and_capital_capital_expenditure_increase", "what_changed": "Purchases of property, plant and equipment print (10,438) thousand for the quarter ended 2026-06-30 against (814). PP&E, net prints 98,755 at 2026-06-30 against 89,775 at 2026-03-31. Net cash used in investing prints (10,489) against (735), and there is no financing inflow this quarter against a 124,577 equity offering a year earlier.", "account": "capital expenditure", "expected_direction": "none", "horizon": "next fiscal year", "quote": "| Purchases of property, plant and equipment |  |  | (10,438 | ) |  |  | (814 | ) |", "paragraph_id": "0001437749-26-025921:8k_2_02:33" }
```

```json
{ "id": "liquidity_and_capital_operating_cash_flow_deferred_revenue", "what_changed": "Net cash provided by operating activities prints 16,013 thousand against 4,125. Within it, the deferred revenue change prints 9,255 against (777), the inventory change 4,947 against (1,046) and the receivables change (11,119) against (8,512). The release headline reads 'Nearly Quadrupled Operating Cash Flow to $16 million'. Deferred revenue prints 84,896 current and 17,722 long-term at 2026-06-30, against 77,936 and 15,395 at 2026-03-31.", "account": "operating cash flow; deferred revenue", "expected_direction": "none", "horizon": "next two quarters", "quote": "| Deferred revenue |  |  | 9,255 |  |  |  | (777 | ) |", "paragraph_id": "0001437749-26-025921:8k_2_02:33" }
```

```json
{ "id": "liquidity_and_capital_contingent_consideration_liability", "what_changed": "Contingent consideration prints 3,959 thousand current and 27,930 long-term at 2026-06-30, against 12,808 and 26,721 at 2026-03-31. At 2025-03-31 the 10-K prints the current portion at 0.", "account": "contingent consideration liability", "expected_direction": "none", "horizon": "next fiscal year", "quote": "| Contingent consideration, current portion |  |  | 3,959 |  |  |  | 12,808 |  |", "paragraph_id": "0001437749-26-025921:8k_2_02:29" }
```

```json
{ "id": "structure_and_disclosure_changes_comtrafo_in_revenue_growth", "what_changed": "Revenue prints $94.1 million against $72.4 million. The release attributes the increase to organic growth and the Comtrafo acquisition and does not split the two in its text. Grid revenue prints 76,323 thousand against 60,087, and Wind 17,750 against 12,271. The 10-Q's Comtrafo-tagged revenue for the quarter is in structure_and_disclosure_changes_comtrafo_quarter_contribution.", "account": "revenue", "expected_direction": "none", "horizon": "next fiscal year", "quote": "The year-over-year increase was driven by organic growth and the acquisition of Comtrafo.", "paragraph_id": "0001437749-26-025921:8k_2_02:8" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_selling_general_administrative_increase", "what_changed": "Selling, general and administrative expense prints 18,618 thousand for the quarter ended 2026-06-30 against 14,204. Research and development prints 3,925 against 4,304.", "account": "selling, general and administrative expense", "expected_direction": "none", "horizon": "next quarter", "quote": "| Selling, general and administrative |  |  | 18,618 |  |  |  | 14,204 |  |", "paragraph_id": "0001437749-26-025921:8k_2_02:25" }
```

```json
{ "id": "estimates_and_discretion_excess_obsolete_inventory_provision", "what_changed": "The provision for excess and obsolete inventory prints 1,073 thousand for the quarter ended 2026-06-30 against 711. The quarterly inventory-reserve ratio is insufficient (no reserve row for 2026-06-30). The 10-K reserve at 2026-03-31 is 3500000.0.", "account": "provision for excess and obsolete inventory", "expected_direction": "none", "horizon": "next quarter", "quote": "| Provision for excess and obsolete inventory |  |  | 1,073 |  |  |  | 711 |  |", "paragraph_id": "0001437749-26-025921:8k_2_02:33" }
```

```json
{ "id": "earnings_quality_quarterly_income_tax_expense", "what_changed": "Income tax expense prints 1,262 thousand for the quarter ended 2026-06-30 against 199, on income before tax of 10,752 against 6,923. The 10-Q prints income taxes paid of 43000 against 38000. This is the first quarter after the fiscal year that carried the deferred tax benefit described in earnings_quality_annual_tax_benefit_against_operating_income.", "account": "income tax expense", "expected_direction": "none", "horizon": "next quarter", "quote": "| Income tax expense |  |  | 1,262 |  |  |  | 199 |  |", "paragraph_id": "0001437749-26-025921:8k_2_02:25" }
```

```json
{ "id": "earnings_quality_other_nonoperating_swing", "what_changed": "Other (expense)/income, net prints (617) thousand for the quarter ended 2026-06-30 against 347. Interest income, net prints 1,537 against 932.", "account": "other non-operating income (expense)", "expected_direction": "none", "horizon": "next quarter", "quote": "| Other (expense)/income, net |  |  | (617 | ) |  |  | 347 |  |", "paragraph_id": "0001437749-26-025921:8k_2_02:25" }
```

## Seen in the notes

No item. In the rows I read, no fact carries a marker saying whether its element sat inside a note. Each fact prints id, paragraph_id, tag, prefix, namespace, context (sometimes with a typed_segment), context_ref, unit, decimals, value, number, nil, form, source_accession, filing_date and, sometimes, superseded_by — nothing else. Because the marker is absent, I cannot sort facts into this section without judging their origin myself, which the instructions rule out. All fact-based items therefore sit above.

Several of those facts are of kinds that usually come from note tables, but that is my judgment, not a marker:

- segment operating income and reconciling items (narrative_signs_of_operating_pressure_grid_segment_operating_loss, earnings_quality_segment_reconciling_item_contingent_consideration)
- the Comtrafo acquisition rows (estimates_and_discretion_contingent_consideration_earnout_range, structure_and_disclosure_changes_comtrafo_quarter_contribution, estimates_and_discretion_comtrafo_acquired_receivables_uncollectible, articulation_and_the_filed_history_comtrafo_goodwill_two_figures, structure_and_disclosure_changes_goodwill_acquired_comtrafo)
- the subsequent-event payment (related_parties_contingencies_and_subsequent_events_property_payment_brazil)
- customer concentration (revenue_recognition_customer_concentration_grid)
- the 10-K tax rows (earnings_quality_annual_tax_benefit_against_operating_income)

The later split into its own reader needs the extraction marker to be present in input_numbers.json.
