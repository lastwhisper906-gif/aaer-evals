<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
Numbers report for JCI, run 0000833444-26-000087 (10-Q for the quarter ended 2026-06-30, filed 2026-07-29), with the 8-K earnings release 0000833444-26-000083. The cutoff is 2026-07-29. Python computed every number below and I copied them as printed. I did no arithmetic. Where a number does not exist, the item says so.

Notes that sit outside the items:

- **The quarter that triggered this run (quarters-back-0) has no cells, so it has no value, change or position for any metric.** The reason the trend table gives for this period (target end 2026-06-30) is: "no quarter ending within 20 days of 2026-06-30 is in the companyfacts record; the companyfacts record's newest row was filed 2026-05-06, before this run's cutoff 2026-07-29 — the record was fetched before the triggering report, so the periods that report is the first to state are not in it". The raw line items for that quarter do appear in the numeric facts from the triggering 10-Q. They are reported below as facts, with no ratio, because no Python ratio exists for them.
- **quarters-back-3 (target end 2025-09-30) and quarters-back-7 (target end 2024-10-01) also have no cells.** The reason given for both is: "no quarter ending within 20 days of ... is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py". My directory holds no fourth-quarter derivation.
- **My input has no articulation-check section and no restatement-trace section.** Some facts carry a `superseded_by` field. Where I compared a superseded value with the value in the superseding filing, the two were equal (item `articulation_and_the_filed_history_superseded_september_balances_unchanged`).
- **No fact I read carries a field saying whether its element sat inside a note.** The fields present are id, paragraph_id, tag, prefix, namespace, context, context_ref, unit, decimals, value, number, nil, form, source_accession, filing_date and sometimes superseded_by. So no fact is placed under "Seen in the notes". That heading holds only items taken from the release's own numbered FOOTNOTES section (release paragraphs 83 to 165). Some facts I reported, such as the warranty roll-forward, may come from a note in the filing, but nothing in the input marks them.
- **The formula-baseline block for research and development capitalisation is not itemised.** It sits on each year of the trend table but prints no paragraph_id. Its `capitalized_development_cost` is missing in every year ("no row for capitalized_development_cost: the companyfacts record tags none of us-gaap:CapitalizedComputerSoftwareAdditions in any period").
- **The prior predictions file says "None on record."** There are no earlier flags to carry forward.
- **Some 8-K records print no paragraph id, so I cannot quote them as items.**
  - A late-filing notice: NT 10-K 0000833444-23-000040 filed 2023-11-29 for the period ended 2023-09-30.
  - An amended item 2.02 release: 0000833444-26-000054 filed 2026-05-07, amending 0000833444-26-000047.
  - Item 5.02 filings on 2026-05-04, 2026-05-13 and 2026-06-03 (the last also carries items 7.01 and 9.01).
- **I read input_numbers.json only in part.** The file has 95,337 lines (3.2 MB), which is more than I could hold. I read:
  - lines 1 to 5,199 (the start of the FY2025 10-K facts);
  - lines 72,525 to 76,624 (the start of the triggering 10-Q facts: income statement, comprehensive income and balance sheet);
  - lines 78,024 to 78,723 (cash-flow rows of the triggering 10-Q);
  - lines 85,000 to 85,399 and 94,000 to 95,337;
  - 25-line samples at 40,000, 60,000, 70,000, 72,500, 74,500 and 78,000.

  Facts in the unread ranges are not reported. Those ranges cover most of the 10-K note detail and most of 0000833444-26-000050.
- **Nothing in my directory is a price, return, short-interest figure, other company's file, prior probability or outcome window.**
- **How the item fields are filled:**
  - `expected_direction` is the direction the figure moved, as the input prints it. For trend cells, that is the sign of the year-over-year change, the only change an annual cell prints. Where the input prints no change, or the printed figures move both ways, it is "none".
  - Trend items carry the suffix "annual" for years-back-0 and "quarterly" for quarters-back-1. Because quarters-back-0 is empty, quarters-back-1 (ended 2026-03-31) is the latest filled quarter. I itemised it as well as the required years-back-0.

## Seen in the statements

```json
{ "id": "earnings_quality_accruals_over_total_assets_annual", "what_changed": "Accruals over total assets for the year ended 2025-09-30 is 0.019425920556683098. The change against years-back-1 is 0.016217113904850332; an annual cell prints no quarter-over-quarter change. Inputs as printed: NetIncomeLoss 3291000000, NetCashProvidedByUsedInOperatingActivitiesContinuingOperations 2554000000, Assets 37939000000. Only 4 of the 5 filled years rest on the same concepts; years-back-4 uses a different operating-cash-flow concept and is not compared (see structure_and_disclosure_changes_accruals_operating_cash_flow_concept_change).", "account": "accruals (net income less operating cash flow) over total assets", "expected_direction": "up", "horizon": "fiscal year ended 2025-09-30 (years-back-0)", "quote": "\"position_in_history\": \"highest of the 4 filled years on the same concepts; 1 other filled year rests on a different concept and is not compared\"", "paragraph_id": "0000833444-26-000087:trends:accruals_over_total_assets:2024-10-01..2025-09-30" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual", "what_changed": "Allowance over (receivables plus allowance) for the year ended 2025-09-30 is 0.03166512202656781. The change against years-back-1 is -0.0018758458699343478. Inputs as printed: AllowanceForDoubtfulAccountsReceivableCurrent 205000000 and AccountsReceivableNetCurrent 6269000000, both at 2025-09-30 from 0000833444-26-000050.", "account": "allowance for doubtful accounts", "expected_direction": "down", "horizon": "fiscal year ended 2025-09-30 (years-back-0)", "quote": "\"position_in_history\": \"second highest of the 5 filled years\"", "paragraph_id": "0000833444-26-000087:trends:bad_debt_reserve_ratio:2024-10-01..2025-09-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual", "what_changed": "Contract liabilities over revenue for the year ended 2025-09-30 is 0.10467875911171386. The change against years-back-1 is 0.010569313311783568. Inputs as printed: ContractWithCustomerLiabilityCurrent 2470000000 at 2025-09-30; RevenueFromContractWithCustomerExcludingAssessedTax 23596000000 for the year.", "account": "contract liabilities (deferred revenue)", "expected_direction": "up", "horizon": "fiscal year ended 2025-09-30 (years-back-0)", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0000833444-26-000087:trends:contract_liabilities_over_revenue:2024-10-01..2025-09-30" }
```

```json
{ "id": "liquidity_and_capital_days_sales_of_inventory_annual", "what_changed": "Days sales of inventory for the year ended 2025-09-30 is 44.27486003732338. The change against years-back-1 is 0.6255154995082535. Inputs as printed: InventoryNet 1820000000 at 2025-09-30; CostOfGoodsAndServicesSold 15004000000; 365 days.", "account": "inventory", "expected_direction": "up", "horizon": "fiscal year ended 2025-09-30 (years-back-0)", "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"", "paragraph_id": "0000833444-26-000087:trends:days_sales_of_inventory:2024-10-01..2025-09-30" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual", "what_changed": "Days sales outstanding for the year ended 2025-09-30 is 96.9734276996101. The change against years-back-1 is 0.48222867555989524. Inputs as printed: AccountsReceivableNetCurrent 6269000000 at 2025-09-30; revenue 23596000000; 365 days.", "account": "accounts receivable", "expected_direction": "up", "horizon": "fiscal year ended 2025-09-30 (years-back-0)", "quote": "\"position_in_history\": \"second highest of the 5 filled years\"", "paragraph_id": "0000833444-26-000087:trends:days_sales_outstanding:2024-10-01..2025-09-30" }
```

```json
{ "id": "earnings_quality_gross_margin_annual", "what_changed": "Gross margin for the year ended 2025-09-30 is 0.3641295134768605. The change against years-back-1 is 0.012221183048139683. Inputs as printed: revenue 23596000000; CostOfGoodsAndServicesSold 15004000000.", "account": "gross margin", "expected_direction": "up", "horizon": "fiscal year ended 2025-09-30 (years-back-0)", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0000833444-26-000087:trends:gross_margin:2024-10-01..2025-09-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_annual", "what_changed": "insufficient. The table could not fill inventory_reserve_ratio for the year ended 2025-09-30, and it is unfilled in every year and quarter the table holds. No value, change or position exists.", "account": "inventory valuation reserve", "expected_direction": "none", "horizon": "fiscal year ended 2025-09-30 (years-back-0)", "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment", "paragraph_id": "0000833444-26-000087:trends:inventory_reserve_ratio:2024-10-01..2025-09-30" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual", "what_changed": "insufficient. The table could not fill non_gaap_gap for the year ended 2025-09-30, and it is unfilled in every period. No value, change or position exists. The release states GAAP and adjusted figures for the quarter ended 2026-06-30 (see earnings_quality_adjusted_net_income_against_gaap_in_release), but no Python-computed gap exists.", "account": "non-GAAP net income against GAAP net income", "expected_direction": "none", "horizon": "fiscal year ended 2025-09-30 (years-back-0)", "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"", "paragraph_id": "0000833444-26-000087:trends:non_gaap_gap:2024-10-01..2025-09-30" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual", "what_changed": "Receivables over revenue for the year ended 2025-09-30 is 0.2656806238345482. The change against years-back-1 is 0.002043468031132367. Inputs as printed: AccountsReceivableNetCurrent 6269000000; revenue 23596000000.", "account": "accounts receivable", "expected_direction": "up", "horizon": "fiscal year ended 2025-09-30 (years-back-0)", "quote": "\"position_in_history\": \"second highest of the 5 filled years\"", "paragraph_id": "0000833444-26-000087:trends:receivables_over_revenue:2024-10-01..2025-09-30" }
```

```json
{ "id": "earnings_quality_soft_asset_share_annual", "what_changed": "Soft-asset share for the year ended 2025-09-30 is 0.9322069638103271. The change against years-back-1 is 0.0026836004188292018. Inputs as printed: Assets 37939000000, PropertyPlantAndEquipmentNet 2193000000, CashAndCashEquivalentsAtCarryingValue 379000000.", "account": "soft assets (total assets less PP&E and cash) over total assets", "expected_direction": "up", "horizon": "fiscal year ended 2025-09-30 (years-back-0)", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0000833444-26-000087:trends:soft_asset_share:2024-10-01..2025-09-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_annual", "what_changed": "Warranty accrual over revenue for the year ended 2025-09-30 is 0.0050856077301237495. The change against years-back-1 is -0.00022983319005749799. Inputs as printed: StandardProductWarrantyAccrual 120000000 at 2025-09-30; revenue 23596000000.", "account": "product warranty accrual", "expected_direction": "down", "horizon": "fiscal year ended 2025-09-30 (years-back-0)", "quote": "\"position_in_history\": \"third highest of the 5 filled years\"", "paragraph_id": "0000833444-26-000087:trends:warranty_reserve_ratio:2024-10-01..2025-09-30" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly", "what_changed": "insufficient. accruals_over_total_assets is not filled for the quarter ended 2026-03-31, the latest filled quarter, because no discrete-quarter operating cash flow is in the record. It is also unfilled for quarters-back-4 and quarters-back-5, and quarters-back-0, -3 and -7 have no cells. Only quarters-back-2 and quarters-back-6 hold values. No value, change or position exists for this quarter.", "account": "accruals over total assets", "expected_direction": "none", "horizon": "quarter ended 2026-03-31 (quarters-back-1)", "quote": "\"missing\": \"no row for operating_cash_flow in 2026-01-01..2026-03-31: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"", "paragraph_id": "0000833444-26-000087:trends:accruals_over_total_assets:2026-01-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly", "what_changed": "Allowance over (receivables plus allowance) at 2026-03-31 is 0.025346301208370173. Change against quarters-back-2: -0.0024532904360463487. Change against quarters-back-5: -0.01290685919222086. Inputs as printed: AllowanceForDoubtfulAccountsReceivableCurrent 172000000; AccountsReceivableNetCurrent 6614000000.", "account": "allowance for doubtful accounts", "expected_direction": "down", "horizon": "quarter ended 2026-03-31 (quarters-back-1)", "quote": "\"position_in_history\": \"lowest of the 5 filled quarters\"", "paragraph_id": "0000833444-26-000087:trends:bad_debt_reserve_ratio:2026-01-01..2026-03-31" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly", "what_changed": "Contract liabilities over quarter revenue at 2026-03-31 is 0.4632041680234451. Change against quarters-back-2: 0.024701494226653686. Change against quarters-back-5: 0.04389479522570022. Inputs as printed: ContractWithCustomerLiabilityCurrent 2845000000; quarter revenue 6142000000.", "account": "contract liabilities (deferred revenue)", "expected_direction": "up", "horizon": "quarter ended 2026-03-31 (quarters-back-1)", "quote": "\"position_in_history\": \"highest of the 5 filled quarters\"", "paragraph_id": "0000833444-26-000087:trends:contract_liabilities_over_revenue:2026-01-01..2026-03-31" }
```

```json
{ "id": "liquidity_and_capital_days_sales_of_inventory_quarterly", "what_changed": "Days sales of inventory at 2026-03-31 is 44.83762886597938. Change against quarters-back-2: -2.904514566736168. Change against quarters-back-5: 1.0228243192646644. Inputs as printed: InventoryNet 1933000000; CostOfGoodsAndServicesSold 3880000000; 90 days.", "account": "inventory", "expected_direction": "up", "horizon": "quarter ended 2026-03-31 (quarters-back-1)", "quote": "\"position_in_history\": \"third highest of the 5 filled quarters\"", "paragraph_id": "0000833444-26-000087:trends:days_sales_of_inventory:2026-01-01..2026-03-31" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly", "what_changed": "Days sales outstanding at 2026-03-31 is 96.9163139042657. Change against quarters-back-2: -1.3207052435693925. Change against quarters-back-5: 4.030478809128283. Inputs as printed: AccountsReceivableNetCurrent 6614000000; quarter revenue 6142000000; 90 days.", "account": "accounts receivable", "expected_direction": "up", "horizon": "quarter ended 2026-03-31 (quarters-back-1)", "quote": "\"position_in_history\": \"second highest of the 5 filled quarters\"", "paragraph_id": "0000833444-26-000087:trends:days_sales_outstanding:2026-01-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly", "what_changed": "Gross margin for the quarter ended 2026-03-31 is 0.3682839465971996. Change against quarters-back-2: 0.010512685600132132. Change against quarters-back-5: 0.003766680917143217. Inputs as printed: revenue 6142000000; CostOfGoodsAndServicesSold 3880000000.", "account": "gross margin", "expected_direction": "up", "horizon": "quarter ended 2026-03-31 (quarters-back-1)", "quote": "\"position_in_history\": \"second highest of the 5 filled quarters\"", "paragraph_id": "0000833444-26-000087:trends:gross_margin:2026-01-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly", "what_changed": "insufficient. inventory_reserve_ratio is not filled for the quarter ended 2026-03-31. No value, change or position exists.", "account": "inventory valuation reserve", "expected_direction": "none", "horizon": "quarter ended 2026-03-31 (quarters-back-1)", "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment", "paragraph_id": "0000833444-26-000087:trends:inventory_reserve_ratio:2026-01-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly", "what_changed": "insufficient. non_gaap_gap is not filled for the quarter ended 2026-03-31. No value, change or position exists.", "account": "non-GAAP net income against GAAP net income", "expected_direction": "none", "horizon": "quarter ended 2026-03-31 (quarters-back-1)", "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"", "paragraph_id": "0000833444-26-000087:trends:non_gaap_gap:2026-01-01..2026-03-31" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarterly", "what_changed": "Period-end receivables over one quarter's revenue at 2026-03-31 is 1.076847932269619. Change against quarters-back-2: 0.009054245880107059. Change against quarters-back-5: 0.044783097879203204. Inputs as printed: AccountsReceivableNetCurrent 6614000000; quarter revenue 6142000000.", "account": "accounts receivable", "expected_direction": "up", "horizon": "quarter ended 2026-03-31 (quarters-back-1)", "quote": "\"position_in_history\": \"highest of the 5 filled quarters\"", "paragraph_id": "0000833444-26-000087:trends:receivables_over_revenue:2026-01-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_soft_asset_share_quarterly", "what_changed": "Soft-asset share at 2026-03-31 is 0.9271523178807947. Change against quarters-back-2: -0.002237145826653353. Change against quarters-back-5: 0.0030840572062130756. Inputs as printed: Assets 38354000000, PropertyPlantAndEquipmentNet 2096000000, CashAndCashEquivalentsAtCarryingValue 698000000.", "account": "soft assets over total assets", "expected_direction": "up", "horizon": "quarter ended 2026-03-31 (quarters-back-1)", "quote": "\"position_in_history\": \"second highest of the 5 filled quarters\"", "paragraph_id": "0000833444-26-000087:trends:soft_asset_share:2026-01-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly", "what_changed": "Warranty accrual over quarter revenue at 2026-03-31 is 0.026538586779550635. Change against quarters-back-2: 0.003423182259971541. Change against quarters-back-5: 0.00557311813966339. Inputs as printed: ProductWarrantyAccrual 163000000; quarter revenue 6142000000.", "account": "product warranty accrual", "expected_direction": "up", "horizon": "quarter ended 2026-03-31 (quarters-back-1)", "quote": "\"position_in_history\": \"highest of the 5 filled quarters\"", "paragraph_id": "0000833444-26-000087:trends:warranty_reserve_ratio:2026-01-01..2026-03-31" }
```

```json
{ "id": "structure_and_disclosure_changes_accruals_operating_cash_flow_concept_change", "what_changed": "Change of tag. The years-back-3 accruals cell prints no change against years-back-4 because the operating_cash_flow input rests on a different concept in each year: us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations in years-back-3 (fiscal year ended 2022-09-30), and us-gaap:NetCashProvidedByUsedInOperatingActivities in years-back-4 (fiscal year ended 2021-09-30, fact 0000833444-21-000046, value 2551000000). The years-back-4 cell's position reads 'the only filled year on the same concepts; 4 other filled years rest on a different concept and are not compared'.", "account": "operating cash flow input to accruals over total assets", "expected_direction": "none", "horizon": "fiscal years ended 2021-09-30 and 2022-09-30 (years-back-4 and years-back-3)", "quote": "\"reason\": \"accruals_over_total_assets rests on a different concept in each period, so the difference would not be a change", "paragraph_id": "0000833444-26-000087:trends:accruals_over_total_assets:2021-10-01..2022-09-30" }
```

```json
{ "id": "structure_and_disclosure_changes_warranty_accrual_concept_change", "what_changed": "Change of tag between filings for the same date. The years-back-0 warranty input for 2025-09-30 is tagged StandardProductWarrantyAccrual (id 0000833444-25-000097:facts:StandardProductWarrantyAccrual:2025-09-30, value 120000000). The triggering 10-Q states the 2025-09-30 warranty balance under ProductWarrantyAccrual (fact 0000833444-26-000087:facts:ProductWarrantyAccrual:2025-09-30, value 120000000), and every quarterly warranty cell rests on ProductWarrantyAccrual. The printed values for that date are equal. The trend table prints no concept-change note for warranty, because its annual and quarterly cells sit in separate series.", "account": "product warranty accrual", "expected_direction": "none", "horizon": "balance at 2025-09-30", "quote": "\"tag\": \"StandardProductWarrantyAccrual\"", "paragraph_id": "0000833444-26-000087:trends:warranty_reserve_ratio:2024-10-01..2025-09-30" }
```

```json
{ "id": "earnings_quality_accruals_net_income_includes_discontinued_operations", "what_changed": "The years-back-0 accruals numerator is NetIncomeLoss 3291000000, total net income attributable to the company. For the same year the 10-K prints IncomeLossFromContinuingOperations 1721000000 and IncomeLossFromDiscontinuedOperationsNetOfTaxAttributableToReportingEntity 1570000000. The operating-cash-flow input (2554000000) is the continuing-operations concept. So the highest-of-four-years accruals reading pairs a total net income with a continuing-operations cash flow. Release paragraph 85 records the July 2025 sale of the Residential and Light Commercial HVAC business as a discontinued operation. No re-scoped ratio exists and none is computed here.", "account": "net income from discontinued operations", "expected_direction": "none", "horizon": "fiscal year ended 2025-09-30", "quote": "\"value\": \"1570000000\"", "paragraph_id": "0000833444-25-000097:facts:IncomeLossFromDiscontinuedOperationsNetOfTaxAttributableToReportingEntity:2024-10-01..2025-09-30" }
```

```json
{ "id": "articulation_and_the_filed_history_superseded_september_balances_unchanged", "what_changed": "No restated prior value found in the rows compared. The 10-K fact for receivables at 2025-09-30 (6269000000) carries superseded_by 0000833444-26-000087, and that 10-Q prints the same value for the same date (0000833444-26-000087:facts:AccountsReceivableNetCurrent:2025-09-30). The other 2025-09-30 balance-sheet rows compared between the two filings are also equal: cash 379000000, allowance 205000000, inventory 1820000000, PP&E 2193000000, assets 37939000000, contract liabilities 2470000000, accounts payable 3614000000, short-term borrowings 723000000. The input holds no restatement-trace section and no articulation checks.", "account": "balance sheet at 2025-09-30", "expected_direction": "none", "horizon": "balance at 2025-09-30", "quote": "\"superseded_by\": \"0000833444-26-000087\"", "paragraph_id": "0000833444-25-000097:facts:AccountsReceivableNetCurrent:2025-09-30" }
```

```json
{ "id": "revenue_recognition_receivables_balance_at_period_end", "what_changed": "AccountsReceivableNetCurrent at 2026-06-30 is 6970000000 in the triggering 10-Q. The same filing prints 6269000000 at 2025-09-30, and the quarters-back-1 trend input is 6614000000 at 2026-03-31. Quarter revenue for the three months to 2026-06-30 is 6614000000. With no quarters-back-0 cell, no receivables_over_revenue or days_sales_outstanding value, change or position exists for this quarter, and none is computed here.", "account": "accounts receivable", "expected_direction": "up", "horizon": "balance at 2026-06-30", "quote": "\"value\": \"6970000000\"", "paragraph_id": "0000833444-26-000087:facts:AccountsReceivableNetCurrent:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_allowance_for_doubtful_accounts_balance", "what_changed": "AllowanceForDoubtfulAccountsReceivableCurrent at 2026-06-30 is 165000000. The same filing prints 205000000 at 2025-09-30, and the quarters-back-1 input is 172000000 at 2026-03-31. Receivables rose over the same dates (6269000000, then 6614000000, then 6970000000). No bad_debt_reserve_ratio exists for this quarter.", "account": "allowance for doubtful accounts", "expected_direction": "down", "horizon": "balance at 2026-06-30", "quote": "\"value\": \"165000000\"", "paragraph_id": "0000833444-26-000087:facts:AllowanceForDoubtfulAccountsReceivableCurrent:2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_balance_at_period_end", "what_changed": "ContractWithCustomerLiabilityCurrent at 2026-06-30 is 2943000000. The same filing prints 2470000000 at 2025-09-30, and the quarters-back-1 input is 2845000000 at 2026-03-31. The release balance sheet labels this line 'Deferred revenue' (2,943 against 2,470). No contract_liabilities_over_revenue exists for this quarter.", "account": "contract liabilities (deferred revenue)", "expected_direction": "up", "horizon": "balance at 2026-06-30", "quote": "\"value\": \"2943000000\"", "paragraph_id": "0000833444-26-000087:facts:ContractWithCustomerLiabilityCurrent:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_inventory_balance_at_period_end", "what_changed": "InventoryNet at 2026-06-30 is 1955000000. The same filing prints 1820000000 at 2025-09-30, and the quarters-back-1 input is 1933000000 at 2026-03-31. Quarter CostOfGoodsAndServicesSold is 4140000000. No days_sales_of_inventory exists for this quarter.", "account": "inventory", "expected_direction": "up", "horizon": "balance at 2026-06-30", "quote": "\"value\": \"1955000000\"", "paragraph_id": "0000833444-26-000087:facts:InventoryNet:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_accrual_balance_at_period_end", "what_changed": "ProductWarrantyAccrual at 2026-06-30 is 146000000. The quarters-back-1 input is 163000000 at 2026-03-31, and the same 10-Q prints 120000000 at 2025-09-30. Nine-month roll-forward facts in the same filing: ProductWarrantyAccrualWarrantiesIssued 94000000, ProductWarrantyAccrualPayments 70000000, ProductWarrantyAccrualPreexistingIncreaseDecrease 3000000, foreign-currency translation 1000000. These facts carry no note marker. No warranty_reserve_ratio exists for this quarter.", "account": "product warranty accrual", "expected_direction": "down", "horizon": "balance at 2026-06-30 against 2026-03-31", "quote": "\"value\": \"146000000\"", "paragraph_id": "0000833444-26-000087:facts:ProductWarrantyAccrual:2026-06-30" }
```

```json
{ "id": "revenue_recognition_net_sales_continuing_operations", "what_changed": "RevenueFromContractWithCustomerExcludingAssessedTax for the three months to 2026-06-30 is 6614000000, against 6052000000 for the three months to 2025-06-30 in the same filing. Products and systems: 4596000000 against 4122000000. Services: 2018000000 against 1930000000. The release reports sales up 9% and organic sales up 10%.", "account": "net sales", "expected_direction": "up", "horizon": "quarter ended 2026-06-30", "quote": "\"value\": \"6614000000\"", "paragraph_id": "0000833444-26-000087:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_gross_profit_continuing_operations", "what_changed": "GrossProfit for the three months to 2026-06-30 is 2474000000, against 2246000000 a year earlier. CostOfGoodsAndServicesSold is 4140000000 against 3806000000. Services cost of sales is 1128000000 against 1150000000, while services revenue rose. With no quarters-back-0 cell, no gross_margin value, change or position exists, and none is computed here.", "account": "gross profit", "expected_direction": "up", "horizon": "quarter ended 2026-06-30", "quote": "\"value\": \"2474000000\"", "paragraph_id": "0000833444-26-000087:facts:GrossProfit:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_operating_cash_flow_tagged_only_cumulatively", "what_changed": "insufficient for the quarter. The triggering 10-Q tags NetCashProvidedByUsedInOperatingActivitiesContinuingOperations for 2025-10-01..2026-06-30 (2572000000, against 1586000000 for the prior nine months). It tags no three-month figure in the rows I read, so accruals over total assets cannot be formed for the quarter from the facts. NetIncomeLoss for the three months to 2026-06-30 is 749000000. The three-month operating cash flow (1,289) exists only in the release.", "account": "operating cash flow, continuing operations", "expected_direction": "none", "horizon": "nine months ended 2026-06-30", "quote": "\"value\": \"2572000000\"", "paragraph_id": "0000833444-26-000087:facts:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations:2025-10-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_soft_asset_inputs_total_assets", "what_changed": "Assets at 2026-06-30 is 38759000000, against 37939000000 at 2025-09-30 in the same filing. CashAndCashEquivalentsAtCarryingValue is 641000000 and PropertyPlantAndEquipmentNet is 1977000000 at 2026-06-30. The inputs to soft_asset_share for the quarter are present in the numeric facts, but no Python ratio exists and none is computed here.", "account": "total assets", "expected_direction": "up", "horizon": "balance at 2026-06-30", "quote": "\"value\": \"38759000000\"", "paragraph_id": "0000833444-26-000087:facts:Assets:2026-06-30" }
```

```json
{ "id": "earnings_quality_income_tax_provision", "what_changed": "IncomeTaxExpenseBenefit for the three months to 2026-06-30 is 165000000, against 87000000 a year earlier. Pre-tax income from continuing operations is 917000000 against 705000000. Nine months: 443000000 against 160000000.", "account": "income tax provision", "expected_direction": "up", "horizon": "quarter ended 2026-06-30", "quote": "\"value\": \"165000000\"", "paragraph_id": "0000833444-26-000087:facts:IncomeTaxExpenseBenefit:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_restructuring_and_impairment_charge", "what_changed": "RestructuringCostsAndAssetImpairmentCharges for the three months to 2026-06-30 is 80000000, against 51000000 a year earlier. Nine months: 224000000 against 146000000.", "account": "restructuring and impairment costs", "expected_direction": "up", "horizon": "quarter ended 2026-06-30", "quote": "\"value\": \"80000000\"", "paragraph_id": "0000833444-26-000087:facts:RestructuringCostsAndAssetImpairmentCharges:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_selling_general_and_administrative_expense", "what_changed": "SellingGeneralAndAdministrativeExpense for the three months to 2026-06-30 is 1407000000, against 1417000000 a year earlier. Nine months: 4029000000 against 4243000000.", "account": "selling, general and administrative expense", "expected_direction": "down", "horizon": "quarter ended 2026-06-30", "quote": "\"value\": \"1407000000\"", "paragraph_id": "0000833444-26-000087:facts:SellingGeneralAndAdministrativeExpense:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_adjusted_net_income_against_gaap_in_release", "what_changed": "The release states GAAP net income from continuing operations attributable to JCI of $749 million and adjusted net income from continuing operations of $868 million for the quarter. Paragraph 8 gives GAAP EPS of $1.23 and adjusted EPS of $1.42. The trend table's non_gaap_gap is insufficient in every period, and no Python-computed gap exists.", "account": "adjusted net income against GAAP net income", "expected_direction": "none", "horizon": "quarter ended 2026-06-30", "quote": "For the quarter, GAAP net income from continuing operations attributable to JCI was $749 million and adjusted net income from continuing operations was $868 million.", "paragraph_id": "0000833444-26-000083:8k_2_02:15" }
```

```json
{ "id": "results_against_expectations_organic_orders_growth", "what_changed": "The release reports quarterly orders up 27% organically. Paragraph 18 says orders before Q1 2026 exclude a category now counted (see structure_and_disclosure_changes_orders_and_backlog_definition_restated).", "account": "orders (Solutions and Services)", "expected_direction": "up", "horizon": "quarter ended 2026-06-30", "quote": "Q3 orders +27% organically year-over-year", "paragraph_id": "0000833444-26-000083:8k_2_02:9" }
```

```json
{ "id": "results_against_expectations_backlog_growth", "what_changed": "The release reports backlog of $21.0 billion, up 32% organically. Paragraph 18 says backlog has been restated to include a new category.", "account": "backlog", "expected_direction": "up", "horizon": "at 2026-06-30", "quote": "Backlog of $21.0 billion increased 32% organically year-over-year", "paragraph_id": "0000833444-26-000083:8k_2_02:10" }
```

```json
{ "id": "structure_and_disclosure_changes_orders_and_backlog_definition_restated", "what_changed": "Definition change. Orders before Q1 2026 exclude certain equipment-only sales for longer-cycle projects, and backlog was restated to include this new category. The input gives no figure for the size of the category.", "account": "orders and backlog", "expected_direction": "none", "horizon": "orders and backlog comparisons in the release", "quote": "Orders prior to Q1 2026 exclude certain equipment-only sales for longer cycle projects. Backlog has been restated to include this new category.", "paragraph_id": "0000833444-26-000083:8k_2_02:18" }
```

```json
{ "id": "results_against_expectations_americas_orders_and_backlog", "what_changed": "Americas orders rose 37% and backlog of $15.9 billion rose 40%, on the release's organic basis. The release attributes this to data centers and other mission-critical environments. Americas sales were $4,504 against $4,042 (paragraph 22).", "account": "Americas orders and backlog", "expected_direction": "up", "horizon": "quarter ended 2026-06-30", "quote": "orders increased 37% year-over-year and backlog of $15.9 billion increased 40% year-over-year", "paragraph_id": "0000833444-26-000083:8k_2_02:24" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_emea_middle_east", "what_changed": "EMEA sales were $1,264 against $1,273, down 1% (paragraph 28). Organic sales rose 1%, which the release says was constrained by the Middle East conflicts. Organic orders rose 6% (paragraph 30).", "account": "EMEA segment sales", "expected_direction": "down", "horizon": "quarter ended 2026-06-30", "quote": "Organic sales increased 1% versus the prior year quarter; constrained by continued pressure in the region due to the conflicts in the Middle East.", "paragraph_id": "0000833444-26-000083:8k_2_02:29" }
```

```json
{ "id": "estimates_and_discretion_corporate_incentive_compensation_accruals", "what_changed": "GAAP corporate expense was $167 against $141, and adjusted corporate expense was $100 against $93 (paragraph 39). The release attributes the increase to higher incentive-compensation accruals and to timing of corporate expenses.", "account": "corporate expense; incentive compensation accruals", "expected_direction": "up", "horizon": "quarter ended 2026-06-30", "quote": "The increase year-over-year is primarily due to increased corporate accruals related to incentive compensation and the timing of certain corporate expenses.", "paragraph_id": "0000833444-26-000083:8k_2_02:40" }
```

```json
{ "id": "liquidity_and_capital_operating_cash_flow_continuing_operations", "what_changed": "Three-month operating cash flow from continuing operations is $1,289 million; the release cash-flow statement prints 1,289 against 787 (paragraph 81). Free cash flow is $1,194 million and adjusted free cash flow is $1,179 million. The numeric facts carry this figure only cumulatively for nine months (2572000000).", "account": "cash provided by operating activities", "expected_direction": "up", "horizon": "quarter ended 2026-06-30", "quote": "Cash provided by operating activities was $1,289 million.", "paragraph_id": "0000833444-26-000083:8k_2_02:42" }
```

```json
{ "id": "results_against_expectations_initiated_adjusted_eps_guidance", "what_changed": "The company initiated guidance for the next quarter: adjusted EPS of about $1.55, organic sales growth of 9% to 10%, and operating leverage of 45% to 50% (paragraphs 46 to 48). No prior guidance for that quarter is in the input.", "account": "adjusted EPS guidance", "expected_direction": "none", "horizon": "fiscal 2026 fourth quarter guidance", "quote": "Adjusted EPS of ~$1.55", "paragraph_id": "0000833444-26-000083:8k_2_02:49" }
```

```json
{ "id": "results_against_expectations_organic_sales_guidance_raised", "what_changed": "Full-year organic sales growth guidance was raised to about 8%, from about 6%.", "account": "organic sales growth guidance", "expected_direction": "up", "horizon": "fiscal 2026 full-year guidance", "quote": "Organic sales growth of ~8% (previously up ~6%)", "paragraph_id": "0000833444-26-000083:8k_2_02:51" }
```

```json
{ "id": "results_against_expectations_operating_leverage_guidance_range", "what_changed": "Full-year operating-leverage guidance moved from about 50% to a range of 45% to 50%. The top of the new range equals the previous point.", "account": "operating leverage guidance", "expected_direction": "down", "horizon": "fiscal 2026 full-year guidance", "quote": "Operating leverage of 45% to 50% (previously ~50%)", "paragraph_id": "0000833444-26-000083:8k_2_02:52" }
```

```json
{ "id": "results_against_expectations_adjusted_eps_guidance_raised", "what_changed": "Full-year adjusted EPS guidance was raised to about $5.05, from about $4.85.", "account": "adjusted EPS guidance", "expected_direction": "up", "horizon": "fiscal 2026 full-year guidance", "quote": "Adjusted EPS of ~$5.05 (previously ~$4.85)", "paragraph_id": "0000833444-26-000083:8k_2_02:53" }
```

```json
{ "id": "results_against_expectations_free_cash_flow_conversion_guidance_unchanged", "what_changed": "Full-year adjusted free-cash-flow conversion guidance is unchanged at about 100%. Nine-month adjusted free-cash-flow conversion is 98% against 108% a year earlier (release footnote table, paragraph 133).", "account": "adjusted free cash flow conversion guidance", "expected_direction": "none", "horizon": "fiscal 2026 full-year guidance", "quote": "Adjusted free cash flow conversion of ~100% (unchanged)", "paragraph_id": "0000833444-26-000083:8k_2_02:54" }
```

```json
{ "id": "earnings_quality_depreciation_and_amortization_lower", "what_changed": "Cash-flow statement depreciation and amortization: 162 for three months against 190, and 495 for nine months against 585.", "account": "depreciation and amortization", "expected_direction": "down", "horizon": "quarter ended 2026-06-30", "quote": "| Depreciation and amortization | 162 |", "paragraph_id": "0000833444-26-000083:8k_2_02:81" }
```

```json
{ "id": "earnings_quality_noncash_restructuring_and_impairment", "what_changed": "Noncash restructuring and impairment charges: 56 for three months against 23, and 160 for nine months against 56.", "account": "noncash restructuring and impairment charges", "expected_direction": "up", "horizon": "quarter ended 2026-06-30", "quote": "| Noncash restructuring and impairment charges | 56 |", "paragraph_id": "0000833444-26-000083:8k_2_02:81" }
```

```json
{ "id": "estimates_and_discretion_equity_based_compensation", "what_changed": "Equity-based compensation: 29 for three months against 48, and 95 for nine months against 107.", "account": "equity-based compensation", "expected_direction": "down", "horizon": "quarter ended 2026-06-30", "quote": "| Equity-based compensation | 29 |", "paragraph_id": "0000833444-26-000083:8k_2_02:81" }
```

```json
{ "id": "earnings_quality_divestiture_gain_in_operating_cash_flow", "what_changed": "(Gain) loss on business divestiture in the cash-flow statement: (13) for three months against nothing, and (86) for nine months against 6. The release's non-GAAP reconciliation prints a gain on divestiture of 70 for the nine months (paragraph 153). The input holds no check that reconciles the two figures.", "account": "gain on business divestiture", "expected_direction": "up", "horizon": "quarter and nine months ended 2026-06-30", "quote": "| (Gain) loss on business divestiture | (13) |", "paragraph_id": "0000833444-26-000083:8k_2_02:81" }
```

```json
{ "id": "revenue_recognition_receivables_cash_flow_use", "what_changed": "The change in accounts receivable absorbed (368) of cash for three months against (172), and (757) for nine months against (79). The release balance sheet shows receivables of 6,970 against 6,269 (paragraph 77).", "account": "accounts receivable", "expected_direction": "up", "horizon": "quarter ended 2026-06-30", "quote": "| Accounts receivable | (368) |", "paragraph_id": "0000833444-26-000083:8k_2_02:81" }
```

```json
{ "id": "earnings_quality_payables_and_accrued_liabilities_cash_inflow", "what_changed": "The change in accounts payable and accrued liabilities provided 701 for three months against 258, and 764 for nine months against 31. Over the same three months operating cash flow was 1,289 against 787.", "account": "accounts payable and accrued liabilities", "expected_direction": "up", "horizon": "quarter ended 2026-06-30", "quote": "| Accounts payable and accrued liabilities | 701 |", "paragraph_id": "0000833444-26-000083:8k_2_02:81" }
```

```json
{ "id": "earnings_quality_accrued_income_taxes_cash_inflow", "what_changed": "The change in accrued income taxes provided 125 for three months against 23, and 205 for nine months against (12).", "account": "accrued income taxes", "expected_direction": "up", "horizon": "quarter ended 2026-06-30", "quote": "| Accrued income taxes | 125 |", "paragraph_id": "0000833444-26-000083:8k_2_02:81" }
```

```json
{ "id": "structure_and_disclosure_changes_business_acquisitions_cash", "what_changed": "Acquisitions of businesses, net of cash acquired: (291) for three months against (1), and (291) for nine months against (9). Divestitures provided 122 for three months and 331 for nine months.", "account": "acquisitions of businesses", "expected_direction": "up", "horizon": "quarter ended 2026-06-30", "quote": "| Acquisitions of businesses, net of cash acquired | (291) |", "paragraph_id": "0000833444-26-000083:8k_2_02:81" }
```

```json
{ "id": "liquidity_and_capital_share_repurchases", "what_changed": "Stock repurchases and retirements: (635) for three months against (310), and (850) for nine months against (970). Dividends were (245) against (243).", "account": "stock repurchases", "expected_direction": "up", "horizon": "quarter ended 2026-06-30", "quote": "| Stock repurchases and retirements | (635) |", "paragraph_id": "0000833444-26-000083:8k_2_02:81" }
```

## Seen in the notes

All items in this section come from the release's numbered FOOTNOTES section (release paragraphs 83 to 165). No numeric fact in my input carries a note marker, so no fact item appears here.

```json
{ "id": "earnings_quality_transformation_costs_excluded_from_adjusted", "what_changed": "Transformation costs excluded from adjusted net income: 80 for three months against 45 (0.13 against 0.07 per diluted share), and 197 for nine months against 124 (paragraph 153). Paragraph 106 describes these as incremental expenses for strategic growth initiatives and cost-saving opportunities.", "account": "transformation costs", "expected_direction": "up", "horizon": "quarter ended 2026-06-30", "quote": "| Transformation costs | 80 |", "paragraph_id": "0000833444-26-000083:8k_2_02:150" }
```

```json
{ "id": "earnings_quality_afff_insurance_recoveries_excluded_from_adjusted", "what_changed": "Water systems AFFF insurance recoveries removed from adjusted net income: (148) for nine months against (13), and (17) for three months against (1) (paragraph 150). Per diluted share, (0.24) against (0.02) for nine months. GAAP results include these recoveries.", "account": "AFFF insurance recoveries", "expected_direction": "up", "horizon": "nine months ended 2026-06-30", "quote": "| Water systems AFFF insurance recoveries | (148) |", "paragraph_id": "0000833444-26-000083:8k_2_02:153" }
```

```json
{ "id": "earnings_quality_gain_on_divestiture_excluded_from_adjusted", "what_changed": "Gain on divestiture removed from adjusted net income: (70) for nine months, with none a year earlier ((0.11) per diluted share). Paragraph 108 ties the item to the sale of the ADT Mexico Security and ADTi businesses. The cash-flow statement prints (86) for (gain) loss on business divestiture over the same nine months (paragraph 81).", "account": "gain on divestiture", "expected_direction": "up", "horizon": "nine months ended 2026-06-30", "quote": "| Gain on divestiture | (70) |", "paragraph_id": "0000833444-26-000083:8k_2_02:153" }
```

```json
{ "id": "earnings_quality_discrete_tax_items_excluded_from_adjusted", "what_changed": "Discrete tax items in the nine-month adjusted reconciliation: 11 against (36) a year earlier (0.02 against (0.05) per diluted share).", "account": "discrete tax items", "expected_direction": "up", "horizon": "nine months ended 2026-06-30", "quote": "| Discrete tax items | 11 |", "paragraph_id": "0000833444-26-000083:8k_2_02:153" }
```

```json
{ "id": "earnings_quality_adjusted_effective_tax_rate", "what_changed": "After adjusting for non-recurring items, the effective tax rate is about 17% for the three and nine months to 2026-06-30, against about 12% a year earlier. The GAAP provision is 165 against 87 for three months (statement paragraph 72).", "account": "effective tax rate", "expected_direction": "up", "horizon": "three and nine months ended 2026-06-30", "quote": "effective tax rate for continuing operations was approximately 17% for the three and nine months ending June 30, 2026 and approximately 12% for the three and nine months ending June 30, 2025", "paragraph_id": "0000833444-26-000083:8k_2_02:164" }
```

```json
{ "id": "earnings_quality_jc_capital_net_loss", "what_changed": "JC Capital net (income) loss: 26 for three months against (8), and 22 for nine months against (4). JC Capital cash provided (used) by operating activities: (8) against 34 for three months, and (33) against 111 for nine months. Both are adjustments in the adjusted free-cash-flow table.", "account": "JC Capital financing activity", "expected_direction": "up", "horizon": "quarter ended 2026-06-30", "quote": "| JC Capital net (income) loss | 26 |", "paragraph_id": "0000833444-26-000083:8k_2_02:133" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_afff_settlement_cash_flows", "what_changed": "Water systems AFFF settlement cash payments and insurance recoveries, as an adjustment to free cash flow: (7) for three months against (3), and (165) for nine months against 383.", "account": "AFFF settlement cash payments and insurance recoveries", "expected_direction": "none", "horizon": "quarter and nine months ended 2026-06-30", "quote": "| Water systems AFFF settlement cash payments and insurance recoveries | (7) |", "paragraph_id": "0000833444-26-000083:8k_2_02:133" }
```

```json
{ "id": "liquidity_and_capital_adjusted_free_cash_flow_conversion", "what_changed": "Adjusted free-cash-flow conversion: 132% for three months against 106%, and 98% for nine months against 108%. The two horizons move in opposite directions. Full-year guidance is about 100% (paragraph 54).", "account": "adjusted free cash flow conversion", "expected_direction": "none", "horizon": "three and nine months ended 2026-06-30", "quote": "| Adjusted free cash flow conversion (non-GAAP) | 132 | % |", "paragraph_id": "0000833444-26-000083:8k_2_02:133" }
```

```json
{ "id": "results_against_expectations_adjusted_ebit_margin", "what_changed": "Adjusted EBIT margin: 16.9% for three months against 14.3%, and 15.0% for nine months against 12.4%. GAAP EBIT margin: 14.9% against 12.9% for three months.", "account": "adjusted EBIT margin", "expected_direction": "up", "horizon": "quarter ended 2026-06-30", "quote": "| Adjusted EBIT margin (non-GAAP) | 16.9 | % |", "paragraph_id": "0000833444-26-000083:8k_2_02:137" }
```

```json
{ "id": "liquidity_and_capital_diluted_share_count", "what_changed": "Diluted weighted-average shares (millions): 610 for three months against 657, and 612 for nine months against 661. Basic shares: 608 against 655.", "account": "diluted weighted average shares outstanding", "expected_direction": "down", "horizon": "quarter ended 2026-06-30", "quote": "| Diluted weighted average shares outstanding | 610 |", "paragraph_id": "0000833444-26-000083:8k_2_02:156" }
```

```json
{ "id": "liquidity_and_capital_net_debt_to_adjusted_ebitda", "what_changed": "Net debt to adjusted EBITDA: 1.9x at 2026-06-30, 2.0x at 2026-03-31 and 2.5x at 2025-06-30. Net debt: 8,834, then 8,825, then 9,562. Net debt to income before income taxes: 3.3x, then 3.5x, then 4.2x.", "account": "net debt to adjusted EBITDA", "expected_direction": "down", "horizon": "at 2026-06-30", "quote": "| Net debt to adjusted EBITDA (non-GAAP) | 1.9x |", "paragraph_id": "0000833444-26-000083:8k_2_02:160" }
```

```json
{ "id": "estimates_and_discretion_erp_asset_accelerated_depreciation", "what_changed": "The ERP asset accelerated-depreciation adjustment is 102 in the twelve months to 2026-06-30 and 102 in the twelve months to 2026-03-31, with none in the twelve months to 2025-06-30. Paragraph 107 says a change in ERP strategy in EMEA led to assets being abandoned and useful lives reduced.", "account": "accelerated depreciation of ERP assets (useful-life estimate)", "expected_direction": "up", "horizon": "twelve months ended 2026-06-30", "quote": "| ERP asset - accelerated depreciation | 102 |", "paragraph_id": "0000833444-26-000083:8k_2_02:162" }
```

```json
{ "id": "earnings_quality_restructuring_and_impairment_in_ebitda_reconciliation", "what_changed": "Restructuring and impairment costs added back in the adjusted EBITDA reconciliation: 624 for the twelve months to 2026-06-30, 595 for the twelve months to 2026-03-31, and 279 for the twelve months to 2025-06-30. Transformation costs in the same table: 253, then 218, then 124.", "account": "restructuring and impairment costs", "expected_direction": "up", "horizon": "twelve months ended 2026-06-30", "quote": "| Restructuring and impairment costs | 624 |", "paragraph_id": "0000833444-26-000083:8k_2_02:162" }
```
