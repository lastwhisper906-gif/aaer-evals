<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# FELE — numbers reader — 10-Q 0000038725-26-000055 (quarter ended 2026-06-30)

## Before the items

**Input check.** My directory holds input_8k.md, input_numbers.json, input_prior_predictions.md and input_trends.json. None of them contains prices, abnormal returns, short interest, another company's files, a prior run's probability or an outcome window. input_prior_predictions.md says: "None on record."

**The quarter this filing reports has no trend cells.** quarters-back-0 (target end 2026-06-30) has no cells at all, so it gets no item. The reason the period gives: "no quarter ending within 20 days of 2026-06-30 is in the companyfacts record; the companyfacts record's newest row was filed 2026-04-29, before this run's cutoff 2026-07-29 — the record was fetched before the triggering report, so the periods that report is the first to state are not in it".
- As a result, my input holds none of the June-quarter trend ratios: gross margin, DSO, DSI, receivables over revenue, bad-debt reserve, warranty reserve, soft-asset share and accruals. I do not derive them.
- The 10-Q's own facts for that quarter are in input_numbers.json, and I report them below as facts.

**The fourth quarters have no cells either.** quarters-back-2 (2025-12-30) and quarters-back-6 (2024-12-31) give this reason: "no quarter ending within 20 days of 2025-12-30 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py".
- No fourth-quarter derivation is in my input. For quarters-back-1, therefore, quarter_over_quarter does not exist for any metric.

**What the input does not hold.**
- **Articulation checks:** none in my input, so I report no articulation gap.
- **Restatement traces:** none in my input. Facts carry a superseded_by field naming the later filing that re-reports the same context. I found no case where the input prints a different value for the same context and unit; the differences I saw are rounding only (decimals -3 against -5). I report no restated prior value.
- **Changes of tag:** no tag-change record exists, and no trend cell says a period rests on a different concept. I report none.

**The R&D-capitalized baseline has no paragraph_id, so it gets no item.** For years-back-0 it prints:
- book_value_with_rnd_capitalized 1380539000.0
- earnings_with_rnd_capitalized 148110000.0
- research_and_development_asset 57960000.0
- research_and_development_amortization 18980000.0
- capitalized_development_cost missing, because no us-gaap:CapitalizedComputerSoftwareAdditions row exists.

**Field conventions.**
- expected_direction gives the direction the quoted figure moved against the comparison the input prints next to it. It is "none" where no comparison exists or the item is insufficient.
- Values are copied as printed. I computed nothing.

## Seen in the statements

### Trend table — years-back-0 (fiscal 2025, 2025-01-01..2025-12-31), every metric

```json
{"id": "earnings_quality_accruals_over_total_assets_annual", "what_changed": "accruals_over_total_assets for fiscal 2025 is -0.047206700319124044; year_over_year change against years-back-1 is -0.002691851966432686; quarter_over_quarter does not apply to an annual period. Inputs as printed: NetIncomeLoss 147090000.0 and NetCashProvidedByUsedInOperatingActivities 238878000.0 (10-K 0000038725-26-000009), Assets 1944385000.0 (0000038725-26-000026). The value is negative. The 10-K facts I read also tag a 2025 pension settlement loss (DefinedBenefitPlanRecognizedNetGainLossDueToSettlementsAndCurtailments1 -41454000), which sits inside the net income input.", "account": "NetIncomeLoss; NetCashProvidedByUsedInOperatingActivities; Assets", "expected_direction": "down", "horizon": "fiscal 2025 against fiscal 2024", "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"", "paragraph_id": "0000038725-26-000055:trends:accruals_over_total_assets:2025-01-01..2025-12-31"}
```

```json
{"id": "estimates_and_discretion_bad_debt_reserve_ratio_annual", "what_changed": "bad_debt_reserve_ratio for fiscal 2025 is 0.015202998424394824; year_over_year change against years-back-1 is -0.00019377116231889674. Inputs: AllowanceForDoubtfulAccountsReceivableCurrent 3821000.0 and AccountsReceivableNetCurrent 247511000.0 at 2025-12-31. This is the lowest reserve of the five filled years.", "account": "AllowanceForDoubtfulAccountsReceivableCurrent; AccountsReceivableNetCurrent", "expected_direction": "down", "horizon": "fiscal 2025 against fiscal 2024", "quote": "\"position_in_history\": \"lowest of the 5 filled years\"", "paragraph_id": "0000038725-26-000055:trends:bad_debt_reserve_ratio:2025-01-01..2025-12-31"}
```

```json
{"id": "revenue_recognition_contract_liabilities_over_revenue_annual", "what_changed": "insufficient. contract_liabilities_over_revenue has no value for fiscal 2025. The cell says no contract-liability or deferred-revenue tag exists in any period of the record, so neither a level nor a trend can be stated.", "account": "ContractWithCustomerLiability / DeferredRevenue (untagged)", "expected_direction": "none", "horizon": "fiscal 2025", "quote": "\"missing\": \"no row for contract_liabilities: the companyfacts record tags none of us-gaap:ContractWithCustomerLiabilityCurrent, us-gaap:ContractWithCustomerLiability, us-gaap:DeferredRevenueCurrent, us-gaap:DeferredRevenue in any period.", "paragraph_id": "0000038725-26-000055:trends:contract_liabilities_over_revenue:2025-01-01..2025-12-31"}
```

```json
{"id": "earnings_quality_days_sales_of_inventory_annual", "what_changed": "days_sales_of_inventory for fiscal 2025 is 146.75663206878374; year_over_year change against years-back-1 is 10.951443507819192. Inputs: InventoryNet 552981000.0 at 2025-12-31 and CostOfGoodsAndServicesSold 1375325000.0 for 2025.", "account": "InventoryNet; CostOfGoodsAndServicesSold", "expected_direction": "up", "horizon": "fiscal 2025 against fiscal 2024", "quote": "\"position_in_history\": \"third highest of the 5 filled years\"", "paragraph_id": "0000038725-26-000055:trends:days_sales_of_inventory:2025-01-01..2025-12-31"}
```

```json
{"id": "revenue_recognition_days_sales_outstanding_annual", "what_changed": "days_sales_outstanding for fiscal 2025 is 42.38898064516129; year_over_year change against years-back-1 is 1.3180697993416075. Inputs: AccountsReceivableNetCurrent 247511000.0 at 2025-12-31 and RevenueFromContractWithCustomerExcludingAssessedTax 2131250000.0 for 2025.", "account": "AccountsReceivableNetCurrent; RevenueFromContractWithCustomerExcludingAssessedTax", "expected_direction": "up", "horizon": "fiscal 2025 against fiscal 2024", "quote": "\"position_in_history\": \"second highest of the 5 filled years\"", "paragraph_id": "0000038725-26-000055:trends:days_sales_outstanding:2025-01-01..2025-12-31"}
```

```json
{"id": "earnings_quality_gross_margin_annual", "what_changed": "gross_margin for fiscal 2025 is 0.35468621700879766; year_over_year change against years-back-1 is -0.0001673183422390978. Inputs: revenue 2131250000.0 and cost of goods sold 1375325000.0 for 2025.", "account": "RevenueFromContractWithCustomerExcludingAssessedTax; CostOfGoodsAndServicesSold", "expected_direction": "down", "horizon": "fiscal 2025 against fiscal 2024", "quote": "\"position_in_history\": \"second highest of the 5 filled years\"", "paragraph_id": "0000038725-26-000055:trends:gross_margin:2025-01-01..2025-12-31"}
```

```json
{"id": "estimates_and_discretion_inventory_reserve_ratio_annual", "what_changed": "insufficient. inventory_reserve_ratio has no value for fiscal 2025, because InventoryValuationReserves is untagged in every period. Inventory reserve movements cannot be seen in my input.", "account": "InventoryValuationReserves (untagged)", "expected_direction": "none", "horizon": "fiscal 2025", "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period.", "paragraph_id": "0000038725-26-000055:trends:inventory_reserve_ratio:2025-01-01..2025-12-31"}
```

```json
{"id": "results_against_expectations_non_gaap_gap_annual", "what_changed": "insufficient. non_gaap_gap has no value for fiscal 2025, because no us-gaap concept carries a non-GAAP measure. No gap between adjusted and GAAP earnings exists in the trend table for any period.", "account": "non-GAAP net income (not in companyfacts)", "expected_direction": "none", "horizon": "fiscal 2025", "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"", "paragraph_id": "0000038725-26-000055:trends:non_gaap_gap:2025-01-01..2025-12-31"}
```

```json
{"id": "revenue_recognition_receivables_over_revenue_annual", "what_changed": "receivables_over_revenue for fiscal 2025 is 0.1161341935483871; year_over_year change against years-back-1 is 0.003918590144508183. Inputs: receivables 247511000.0 at 2025-12-31 and revenue 2131250000.0 for 2025.", "account": "AccountsReceivableNetCurrent; RevenueFromContractWithCustomerExcludingAssessedTax", "expected_direction": "up", "horizon": "fiscal 2025 against fiscal 2024", "quote": "\"position_in_history\": \"second highest of the 5 filled years\"", "paragraph_id": "0000038725-26-000055:trends:receivables_over_revenue:2025-01-01..2025-12-31"}
```

```json
{"id": "earnings_quality_soft_asset_share_annual", "what_changed": "soft_asset_share for fiscal 2025 is 0.8190553825502666; year_over_year change against years-back-1 is 0.06298844659597436. Inputs: Assets 1944385000.0, PropertyPlantAndEquipmentNet 252164000.0 and CashAndCashEquivalentsAtCarryingValue 99662000.0 at 2025-12-31. Years-back-1 printed 0.7560669359542922, the lowest of the 5 filled years.", "account": "Assets; PropertyPlantAndEquipmentNet; CashAndCashEquivalentsAtCarryingValue", "expected_direction": "up", "horizon": "fiscal 2025 against fiscal 2024", "quote": "\"position_in_history\": \"third highest of the 5 filled years\"", "paragraph_id": "0000038725-26-000055:trends:soft_asset_share:2025-01-01..2025-12-31"}
```

```json
{"id": "estimates_and_discretion_warranty_reserve_ratio_annual", "what_changed": "warranty_reserve_ratio for fiscal 2025 is 0.004269794721407625; year_over_year change against years-back-1 is -0.00018269498715713442. Inputs: ProductWarrantyAccrual 9100000.0 at 2025-12-31 and revenue 2131250000.0. This is the lowest warranty reserve of the five filled years.", "account": "ProductWarrantyAccrual; RevenueFromContractWithCustomerExcludingAssessedTax", "expected_direction": "down", "horizon": "fiscal 2025 against fiscal 2024", "quote": "\"position_in_history\": \"lowest of the 5 filled years\"", "paragraph_id": "0000038725-26-000055:trends:warranty_reserve_ratio:2025-01-01..2025-12-31"}
```

### Trend table — quarters-back-1 (2026-01-01..2026-03-31), the newest quarter with cells

```json
{"id": "earnings_quality_accruals_over_total_assets_quarterly", "what_changed": "accruals_over_total_assets for the quarter is 0.037667193404672526; year_over_year change against quarters-back-5 is 0.011522758752798401; quarter_over_quarter does not exist (quarters-back-2 not filled). Inputs: NetIncomeLoss 34330000.0, NetCashProvidedByUsedInOperatingActivities -40875000.0, Assets 1996565000.0. Only 2 quarters are filled, which is insufficient for a trend claim.", "account": "NetIncomeLoss; NetCashProvidedByUsedInOperatingActivities; Assets", "expected_direction": "up", "horizon": "quarter ended 2026-03-31 against quarter ended 2025-03-31", "quote": "\"position_in_history\": \"highest of the 2 filled quarters\"", "paragraph_id": "0000038725-26-000055:trends:accruals_over_total_assets:2026-01-01..2026-03-31"}
```

```json
{"id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly", "what_changed": "bad_debt_reserve_ratio for the quarter is 0.015605738628664722; year_over_year change against quarters-back-5 is 0.0017798167492976153; quarter_over_quarter does not exist. Inputs: allowance 4722000.0 and receivables 297859000.0 at 2026-03-31.", "account": "AllowanceForDoubtfulAccountsReceivableCurrent; AccountsReceivableNetCurrent", "expected_direction": "up", "horizon": "quarter ended 2026-03-31 against quarter ended 2025-03-31", "quote": "\"position_in_history\": \"highest of the 5 filled quarters\"", "paragraph_id": "0000038725-26-000055:trends:bad_debt_reserve_ratio:2026-01-01..2026-03-31"}
```

```json
{"id": "earnings_quality_days_sales_of_inventory_quarterly", "what_changed": "days_sales_of_inventory for the quarter is 161.27152285324516; year_over_year change against quarters-back-5 is -11.82426768989285; quarter_over_quarter does not exist. Inputs: InventoryNet 583208000.0 at 2026-03-31 and cost of goods sold 325468000.0.", "account": "InventoryNet; CostOfGoodsAndServicesSold", "expected_direction": "down", "horizon": "quarter ended 2026-03-31 against quarter ended 2025-03-31", "quote": "\"position_in_history\": \"second highest of the 5 filled quarters\"", "paragraph_id": "0000038725-26-000055:trends:days_sales_of_inventory:2026-01-01..2026-03-31"}
```

```json
{"id": "revenue_recognition_days_sales_outstanding_quarterly", "what_changed": "days_sales_outstanding for the quarter is 53.567801741278124; year_over_year change against quarters-back-5 is -0.14352419826678187; quarter_over_quarter does not exist. Inputs: receivables 297859000.0 at 2026-03-31 and revenue 500437000.0.", "account": "AccountsReceivableNetCurrent; RevenueFromContractWithCustomerExcludingAssessedTax", "expected_direction": "down", "horizon": "quarter ended 2026-03-31 against quarter ended 2025-03-31", "quote": "\"position_in_history\": \"second highest of the 5 filled quarters\"", "paragraph_id": "0000038725-26-000055:trends:days_sales_outstanding:2026-01-01..2026-03-31"}
```

```json
{"id": "earnings_quality_gross_margin_quarterly", "what_changed": "gross_margin for the quarter is 0.34963242126381544; year_over_year change against quarters-back-5 is -0.010398507001499857; quarter_over_quarter does not exist. Inputs: revenue 500437000.0 and cost of goods sold 325468000.0. The input holds no gross_margin for the quarter ended 2026-06-30.", "account": "RevenueFromContractWithCustomerExcludingAssessedTax; CostOfGoodsAndServicesSold", "expected_direction": "down", "horizon": "quarter ended 2026-03-31 against quarter ended 2025-03-31", "quote": "\"position_in_history\": \"lowest of the 5 filled quarters\"", "paragraph_id": "0000038725-26-000055:trends:gross_margin:2026-01-01..2026-03-31"}
```

```json
{"id": "revenue_recognition_receivables_over_revenue_quarterly", "what_changed": "receivables_over_revenue for the quarter is 0.5951977971253125 (quarterly revenue base); year_over_year change against quarters-back-5 is -0.0015947133140753467; quarter_over_quarter does not exist.", "account": "AccountsReceivableNetCurrent; RevenueFromContractWithCustomerExcludingAssessedTax", "expected_direction": "down", "horizon": "quarter ended 2026-03-31 against quarter ended 2025-03-31", "quote": "\"position_in_history\": \"second highest of the 5 filled quarters\"", "paragraph_id": "0000038725-26-000055:trends:receivables_over_revenue:2026-01-01..2026-03-31"}
```

```json
{"id": "earnings_quality_soft_asset_share_quarterly", "what_changed": "soft_asset_share for the quarter is 0.8334769967419042; year_over_year change against quarters-back-5 is -0.0002489610578780832; quarter_over_quarter does not exist. Inputs: Assets 1996565000.0, PP&E 252074000.0 and cash 80400000.0 at 2026-03-31.", "account": "Assets; PropertyPlantAndEquipmentNet; CashAndCashEquivalentsAtCarryingValue", "expected_direction": "down", "horizon": "quarter ended 2026-03-31 against quarter ended 2025-03-31", "quote": "\"position_in_history\": \"second highest of the 5 filled quarters\"", "paragraph_id": "0000038725-26-000055:trends:soft_asset_share:2026-01-01..2026-03-31"}
```

```json
{"id": "estimates_and_discretion_warranty_reserve_ratio_quarterly", "what_changed": "warranty_reserve_ratio for the quarter is 0.01698515497455224 (quarterly revenue base); year_over_year change against quarters-back-5 is -0.0030039937732703713; quarter_over_quarter does not exist. Inputs: ProductWarrantyAccrual 8500000.0 at 2026-03-31 and revenue 500437000.0.", "account": "ProductWarrantyAccrual; RevenueFromContractWithCustomerExcludingAssessedTax", "expected_direction": "down", "horizon": "quarter ended 2026-03-31 against quarter ended 2025-03-31", "quote": "\"position_in_history\": \"third highest of the 5 filled quarters\"", "paragraph_id": "0000038725-26-000055:trends:warranty_reserve_ratio:2026-01-01..2026-03-31"}
```

```json
{"id": "revenue_recognition_contract_liabilities_over_revenue_quarterly", "what_changed": "insufficient. contract_liabilities_over_revenue has no value for the quarter, because no contract-liability or deferred-revenue tag exists in any period.", "account": "ContractWithCustomerLiability / DeferredRevenue (untagged)", "expected_direction": "none", "horizon": "quarter ended 2026-03-31", "quote": "\"missing\": \"no row for contract_liabilities: the companyfacts record tags none of us-gaap:ContractWithCustomerLiabilityCurrent, us-gaap:ContractWithCustomerLiability, us-gaap:DeferredRevenueCurrent, us-gaap:DeferredRevenue in any period.", "paragraph_id": "0000038725-26-000055:trends:contract_liabilities_over_revenue:2026-01-01..2026-03-31"}
```

```json
{"id": "estimates_and_discretion_inventory_reserve_ratio_quarterly", "what_changed": "insufficient. inventory_reserve_ratio has no value for the quarter, because InventoryValuationReserves is untagged in every period.", "account": "InventoryValuationReserves (untagged)", "expected_direction": "none", "horizon": "quarter ended 2026-03-31", "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period.", "paragraph_id": "0000038725-26-000055:trends:inventory_reserve_ratio:2026-01-01..2026-03-31"}
```

```json
{"id": "results_against_expectations_non_gaap_gap_quarterly", "what_changed": "insufficient. non_gaap_gap has no value for the quarter. Outside the trend table, the 8-K prints adjusted diluted EPS against GAAP diluted EPS for the June quarter only; no gap figure exists in the input.", "account": "non-GAAP net income (not in companyfacts)", "expected_direction": "none", "horizon": "quarter ended 2026-03-31", "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"", "paragraph_id": "0000038725-26-000055:trends:non_gaap_gap:2026-01-01..2026-03-31"}
```

### Numeric facts — 10-Q for the quarter ended 2026-06-30 (0000038725-26-000055) and the Q1 10-Q (0000038725-26-000026)

```json
{"id": "revenue_recognition_net_sales_reported", "what_changed": "Net sales for the quarter ended 2026-06-30 are 622880000, against 587434000 for the quarter ended 2025-06-30 in the same filing. The six months print 1123317000 against 1042681000. The 8-K prints 622,880 and calls it a 6% increase; its bridge attributes 15.0 to acquisitions, 6.1 to foreign currency and 14.4 to volume/price (in millions). No June-quarter receivables-to-revenue or DSO ratio exists in my input.", "account": "RevenueFromContractWithCustomerExcludingAssessedTax", "expected_direction": "up", "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30", "quote": "\"value\": \"622880000\"", "paragraph_id": "0000038725-26-000055:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30"}
```

```json
{"id": "earnings_quality_gross_profit_reported", "what_changed": "Gross profit for the quarter ended 2026-06-30 is 230605000, against 211826000 a year earlier; cost of goods sold is 392275000 against 375608000. My input has no gross_margin ratio for this quarter, and I do not derive one. The newest gross_margin cell (quarter ended 2026-03-31) is the lowest of the 5 filled quarters.", "account": "GrossProfit; CostOfGoodsAndServicesSold", "expected_direction": "up", "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30", "quote": "\"value\": \"230605000\"", "paragraph_id": "0000038725-26-000055:facts:GrossProfit:2026-04-01..2026-06-30"}
```

```json
{"id": "results_against_expectations_diluted_eps_reported", "what_changed": "GAAP diluted EPS for the quarter ended 2026-06-30 is 1.46, against 1.31 a year earlier. The six months print 2.23 against 1.97. Diluted weighted shares are 44700000 against 45900000.", "account": "EarningsPerShareDiluted", "expected_direction": "up", "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30", "quote": "\"value\": \"1.46\"", "paragraph_id": "0000038725-26-000055:facts:EarningsPerShareDiluted:2026-04-01..2026-06-30"}
```

```json
{"id": "related_parties_contingencies_and_subsequent_events_litigation_settlement_loss_tagged", "what_changed": "A new face-statement line: GainLossRelatedToLitigationSettlement is -4512000 for the quarter ended 2026-06-30, against 0 for the prior-year quarter; the six months also print -4512000. The segment table places 4500000 of it in Energy Systems.", "account": "GainLossRelatedToLitigationSettlement", "expected_direction": "down", "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30", "quote": "\"value\": \"-4512000\"", "paragraph_id": "0000038725-26-000055:facts:GainLossRelatedToLitigationSettlement:2026-04-01..2026-06-30"}
```

```json
{"id": "related_parties_contingencies_and_subsequent_events_esso_loss_contingency_recognized", "what_changed": "LossContingencyLossInPeriod of 4500000 is recognized in the quarter ended 2026-06-30 (and in the six months) for the EssoSAF case. The dimensions are LitigationStatusAxis = PendingLitigationMember and DamagesFromProductDefectsMember: the case is still tagged pending while a loss is booked.", "account": "LossContingencyLossInPeriod (EssoSAF, pending, product defects)", "expected_direction": "up", "horizon": "quarter ended 2026-06-30", "quote": "\"value\": \"4500000\"", "paragraph_id": "0000038725-26-000055:facts:LossContingencyLossInPeriod:2026-04-01..2026-06-30:srt:LitigationCaseAxis=fele:EssoSAFMember,us-gaap:LitigationStatusAxis=us-gaap:PendingLitigationMember,us-gaap:LossContingenciesByNatureOfContingencyAxis=us-gaap:DamagesFromProductDefectsMember"}
```

```json
{"id": "related_parties_contingencies_and_subsequent_events_esso_damages_sought", "what_changed": "The Q1 10-Q tags LossContingencyDamagesSoughtValue of 9500000 EUR for the same EssoSAF product-defect case, as pending litigation. The June-quarter loss recognized for that case is 4500000 USD. The input does not say whether the remaining claim stays open.", "account": "LossContingencyDamagesSoughtValue (EUR)", "expected_direction": "none", "horizon": "quarter ended 2026-03-31 disclosure, carried into the quarter ended 2026-06-30", "quote": "\"value\": \"9500000\"", "paragraph_id": "0000038725-26-000026:facts:LossContingencyDamagesSoughtValue:2026-01-01..2026-03-31:srt:LitigationCaseAxis=fele:EssoSAFMember,us-gaap:LitigationStatusAxis=us-gaap:PendingLitigationMember,us-gaap:LossContingenciesByNatureOfContingencyAxis=us-gaap:DamagesFromProductDefectsMember:unit=iso4217:EUR"}
```

```json
{"id": "earnings_quality_restructuring_charges", "what_changed": "Restructuring for the six months to 2026-06-30 is 4278000, against 323000 for the six months to 2025-06-30. The June quarter alone is 406000 against 164000. The segment table puts six-month restructuring of 4300000 in Water Systems. The 10-K facts I read tag RestructuringAndRelatedCostExpectedCost1 of 4000000 as a subsequent event. The 8-K excludes restructuring from adjusted EPS (0.01) and adjusted operating income (0.4).", "account": "RestructuringSettlementAndImpairmentProvisions", "expected_direction": "up", "horizon": "six months to 2026-06-30 against six months to 2025-06-30", "quote": "\"value\": \"4278000\"", "paragraph_id": "0000038725-26-000055:facts:RestructuringSettlementAndImpairmentProvisions:2026-01-01..2026-06-30"}
```

```json
{"id": "revenue_recognition_receivables_balance_build", "what_changed": "Net receivables are 352459000 at 2026-06-30, against 247511000 at 2025-12-31 in the same filing; the Q1 10-Q printed 297859000 at 2026-03-31. Acquired receivables include 2100000 from Wood Bros. The 10-Q facts give no 2025-06-30 receivables balance, so the comparison is against year-end. No DSO for the June quarter exists in my input.", "account": "AccountsReceivableNetCurrent", "expected_direction": "up", "horizon": "2026-06-30 against 2025-12-31", "quote": "\"value\": \"352459000\"", "paragraph_id": "0000038725-26-000055:facts:AccountsReceivableNetCurrent:2026-06-30"}
```

```json
{"id": "revenue_recognition_receivables_cash_absorption", "what_changed": "The cash-flow change in receivables (IncreaseDecreaseInAccountsReceivable) is 98781000 for the six months to 2026-06-30, against 61458000 for the six months to 2025-06-30. The 8-K prints these as (98,781) and (61,458).", "account": "IncreaseDecreaseInAccountsReceivable", "expected_direction": "up", "horizon": "six months to 2026-06-30 against six months to 2025-06-30", "quote": "\"value\": \"98781000\"", "paragraph_id": "0000038725-26-000055:facts:IncreaseDecreaseInAccountsReceivable:2026-01-01..2026-06-30"}
```

```json
{"id": "estimates_and_discretion_doubtful_accounts_allowance", "what_changed": "The allowance for doubtful accounts is 3260000 at 2026-06-30, against 3821000 at 2025-12-31 in the same filing; the Q1 10-Q input to the bad-debt cell was 4722000 at 2026-03-31. The allowance printed at June is below both earlier balances, while receivables printed at June are above both. No bad_debt_reserve_ratio for 2026-06-30 exists in my input.", "account": "AllowanceForDoubtfulAccountsReceivableCurrent", "expected_direction": "down", "horizon": "2026-06-30 against 2025-12-31 and 2026-03-31", "quote": "\"value\": \"3260000\"", "paragraph_id": "0000038725-26-000055:facts:AllowanceForDoubtfulAccountsReceivableCurrent:2026-06-30"}
```

```json
{"id": "earnings_quality_inventory_balance_build", "what_changed": "Net inventory is 597736000 at 2026-06-30, against 552981000 at 2025-12-31 and 583208000 at 2026-03-31 (Q1 10-Q). Components at 2026-06-30 against 2025-12-31:\n- raw materials 206446000 against 189380000\n- work in process 33536000 against 27750000\n- finished goods 357754000 against 335851000\nWood Bros added 6000000.0 of inventory. The six-month cash-flow inventory change is 30750000 against 49215000. No DSI for the June quarter exists in my input.", "account": "InventoryNet; InventoryRawMaterials; InventoryWorkInProcess; InventoryFinishedGoods", "expected_direction": "up", "horizon": "2026-06-30 against 2025-12-31", "quote": "\"value\": \"597736000\"", "paragraph_id": "0000038725-26-000055:facts:InventoryNet:2026-06-30"}
```

```json
{"id": "liquidity_and_capital_current_debt", "what_changed": "Current maturities of debt and short-term borrowings are 108491000 at 2026-06-30, against 31827000 at 2025-12-31. Long-term debt is 134317000 against 135184000. Total current liabilities are 455797000 against 344046000; total current assets are 1096868000 against 958626000.", "account": "DebtCurrent", "expected_direction": "up", "horizon": "2026-06-30 against 2025-12-31", "quote": "\"value\": \"108491000\"", "paragraph_id": "0000038725-26-000055:facts:DebtCurrent:2026-06-30"}
```

```json
{"id": "liquidity_and_capital_revolver_borrowing", "what_changed": "Revolving credit facility carrying amount is 107000000.0 at 2026-06-30, against 30000000.0 at 2025-12-31; the Q1 10-Q printed 87000000.0 at 2026-03-31. Six-month ProceedsFromIssuanceOfDebt is 251606000 and RepaymentsOfDebtAndCapitalLeaseObligations is 175667000. The revolver interest rate during the period is 0.046 against 0.029 for 2025.", "account": "DebtInstrumentCarryingAmount (revolving credit facility)", "expected_direction": "up", "horizon": "2026-06-30 against 2025-12-31", "quote": "\"value\": \"107000000.0\"", "paragraph_id": "0000038725-26-000055:facts:DebtInstrumentCarryingAmount:2026-06-30:us-gaap:CreditFacilityAxis=us-gaap:RevolvingCreditFacilityMember"}
```

```json
{"id": "liquidity_and_capital_revolver_remaining_capacity", "what_changed": "Remaining borrowing capacity on the revolving facility is 236600000 at 2026-06-30, against 313600000 at 2025-12-31 and 256600000 at 2026-03-31. Letters of credit stay at 6400000. Cash is 97283000 against 99662000.", "account": "LineOfCreditFacilityRemainingBorrowingCapacity (revolving credit facility)", "expected_direction": "down", "horizon": "2026-06-30 against 2025-12-31", "quote": "\"value\": \"236600000\"", "paragraph_id": "0000038725-26-000055:facts:LineOfCreditFacilityRemainingBorrowingCapacity:2026-06-30:us-gaap:CreditFacilityAxis=us-gaap:RevolvingCreditFacilityMember"}
```

```json
{"id": "liquidity_and_capital_operating_cash_flow", "what_changed": "Net cash from operating activities is 58705000 for the six months to 2026-06-30, against 31997000 for the six months to 2025-06-30. The Q1 10-Q printed -40875000 for the three months to 2026-03-31. No quarterly operating-cash-flow figure for the June quarter exists in my input, and I do not derive one.", "account": "NetCashProvidedByUsedInOperatingActivities", "expected_direction": "up", "horizon": "six months to 2026-06-30 against six months to 2025-06-30", "quote": "\"value\": \"58705000\"", "paragraph_id": "0000038725-26-000055:facts:NetCashProvidedByUsedInOperatingActivities:2026-01-01..2026-06-30"}
```

```json
{"id": "liquidity_and_capital_share_repurchases", "what_changed": "Payments for repurchase of common stock are 18326000 for the six months to 2026-06-30, against 129321000 a year earlier. Dividends paid are 24862000 against 25321000; the dividend per share is 0.280 in the June quarter against 0.265.", "account": "PaymentsForRepurchaseOfCommonStock", "expected_direction": "down", "horizon": "six months to 2026-06-30 against six months to 2025-06-30", "quote": "\"value\": \"18326000\"", "paragraph_id": "0000038725-26-000055:facts:PaymentsForRepurchaseOfCommonStock:2026-01-01..2026-06-30"}
```

```json
{"id": "liquidity_and_capital_accounts_payable_balance", "what_changed": "Accounts payable are 206192000 at 2026-06-30, against 174954000 at 2025-12-31. The six-month cash-flow change in payables and accrued liabilities is 37945000, against 11514000 a year earlier. Wood Bros added 2100000 of payables.", "account": "AccountsPayableCurrent; IncreaseDecreaseInAccountsPayableAndAccruedLiabilities", "expected_direction": "up", "horizon": "2026-06-30 against 2025-12-31", "quote": "\"value\": \"206192000\"", "paragraph_id": "0000038725-26-000055:facts:AccountsPayableCurrent:2026-06-30"}
```

```json
{"id": "structure_and_disclosure_changes_wood_bros_acquisition", "what_changed": "In the June quarter the company paid 49900000 for 100 percent of Wood Bros. The purchase allocation at 2026-06-30 prints:\n- goodwill 23000000.0\n- intangibles 27900000 (customer relationships 19100000, trade names 8800000)\n- inventory 6000000.0\n- receivables 2100000\n- deferred tax liabilities 7100000\n- net assets 50300000\nAcquisition-related costs are 300000 in the quarter. Six-month payments for acquisitions net of cash are 71926000, against 109687000 a year earlier.", "account": "PaymentsToAcquireBusinessesGross (Wood Bros)", "expected_direction": "up", "horizon": "quarter ended 2026-06-30", "quote": "\"value\": \"49900000\"", "paragraph_id": "0000038725-26-000055:facts:PaymentsToAcquireBusinessesGross:2026-04-01..2026-06-30:us-gaap:BusinessAcquisitionAxis=fele:WoodBros.Member"}
```

```json
{"id": "structure_and_disclosure_changes_benson_pump_acquisition", "what_changed": "The company paid 21700000 in the June quarter for 100 percent of Benson Pump. The Q1 10-Q facts I read carried Benson Pump as a subsequent event with an expected price of 21300000. This is a second acquisition closed in the quarter, alongside Wood Bros.", "account": "PaymentsToAcquireBusinessesGross (Benson Pump)", "expected_direction": "up", "horizon": "quarter ended 2026-06-30", "quote": "\"value\": \"21700000\"", "paragraph_id": "0000038725-26-000055:facts:PaymentsToAcquireBusinessesGross:2026-04-01..2026-06-30:us-gaap:BusinessAcquisitionAxis=fele:BensonPumpMember"}
```

```json
{"id": "structure_and_disclosure_changes_goodwill_balance", "what_changed": "Goodwill is 432092000 at 2026-06-30, against 398127000 at 2025-12-31. The rollforward for the six months prints:\n- acquired 28500000 (Water 23000000, Distribution 5500000)\n- foreign-currency translation 5300000\n- purchase-accounting adjustments 200000\nIntangibles net of goodwill are 280986000 against 251692000.", "account": "Goodwill; IntangibleAssetsNetExcludingGoodwill", "expected_direction": "up", "horizon": "2026-06-30 against 2025-12-31", "quote": "\"value\": \"432092000\"", "paragraph_id": "0000038725-26-000055:facts:Goodwill:2026-06-30"}
```

```json
{"id": "estimates_and_discretion_purchase_accounting_goodwill_adjustment", "what_changed": "GoodwillPurchaseAccountingAdjustments is 200000 for the six months to 2026-06-30, all in Water Systems. Barnes de Colombia goodwill prints 43400000 at 2026-03-31 in both 10-Qs; the 10-K facts I read printed 44500000 for Barnes de Colombia at 2025-12-31. These are different dates, so this is a measurement-period movement and not a restatement trace.", "account": "GoodwillPurchaseAccountingAdjustments", "expected_direction": "up", "horizon": "six months to 2026-06-30", "quote": "\"value\": \"200000\"", "paragraph_id": "0000038725-26-000055:facts:GoodwillPurchaseAccountingAdjustments:2026-01-01..2026-06-30"}
```

```json
{"id": "estimates_and_discretion_warranty_accrual_balance", "what_changed": "The product warranty accrual is 8800000 at 2026-06-30, against 9100000 at 2025-12-31 and 8500000 at 2026-03-31. Six-month warranties issued are 6700000 and payments are 7000000.0. No warranty_reserve_ratio for the June quarter exists in my input.", "account": "ProductWarrantyAccrual", "expected_direction": "down", "horizon": "2026-06-30 against 2025-12-31", "quote": "\"value\": \"8800000\"", "paragraph_id": "0000038725-26-000055:facts:ProductWarrantyAccrual:2026-06-30"}
```

```json
{"id": "earnings_quality_equity_swap_gain_in_selling_expense", "what_changed": "A non-designated equity swap (150000 shares notional) produced a gain of 2100000 recorded in SG&A in the June quarter, against a loss of 1600000 in the June 2025 quarter. The six months print a gain of 1400000 against a loss of 2800000; the Q1 10-Q printed a loss of 700000 for Q1 2026. SG&A for the June quarter is 132088000 against 123521000.", "account": "GainOnDerivativeInstrumentsPretax (equity swap, in SellingGeneralAndAdministrativeExpense)", "expected_direction": "up", "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30", "quote": "\"value\": \"2100000\"", "paragraph_id": "0000038725-26-000055:facts:GainOnDerivativeInstrumentsPretax:2026-04-01..2026-06-30:us-gaap:DerivativeInstrumentRiskAxis=us-gaap:EquitySwapMember,us-gaap:HedgingDesignationAxis=us-gaap:NondesignatedMember,us-gaap:StatementOfIncomeLocationBalanceAxis=us-gaap:SellingGeneralAndAdministrativeExpense"}
```

```json
{"id": "earnings_quality_effective_tax_rate", "what_changed": "The effective income tax rate is 0.257 for the quarter ended 2026-06-30, against 0.249 a year earlier. The six months print 0.252 against 0.249; Q1 2026 printed 0.242. Income tax expense for the quarter is 22822000 against 20061000.", "account": "EffectiveIncomeTaxRateContinuingOperations", "expected_direction": "up", "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30", "quote": "\"value\": \"0.257\"", "paragraph_id": "0000038725-26-000055:facts:EffectiveIncomeTaxRateContinuingOperations:2026-04-01..2026-06-30"}
```

```json
{"id": "liquidity_and_capital_interest_expense", "what_changed": "Interest expense is 3524000 for the quarter ended 2026-06-30, against 2805000 a year earlier. The six months print 5835000 against 4604000.", "account": "InterestExpense", "expected_direction": "up", "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30", "quote": "\"value\": \"3524000\"", "paragraph_id": "0000038725-26-000055:facts:InterestExpense:2026-04-01..2026-06-30"}
```

```json
{"id": "earnings_quality_foreign_exchange_loss", "what_changed": "The foreign-currency transaction loss is -2497000 for the quarter ended 2026-06-30, against -4548000 a year earlier. Non-designated FX forwards gained 1700000 in the quarter against 6800000; their notional is 0 at 2026-06-30. Other nonoperating income is 1345000 against -164000.", "account": "ForeignCurrencyTransactionGainLossBeforeTax", "expected_direction": "up", "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30", "quote": "\"value\": \"-2497000\"", "paragraph_id": "0000038725-26-000055:facts:ForeignCurrencyTransactionGainLossBeforeTax:2026-04-01..2026-06-30"}
```

### 8-K earnings release (0000038725-26-000051) against the filed figures

```json
{"id": "across_documents_adjusted_eps_printed_two_ways", "what_changed": "The release's highlight bullet prints adjusted diluted EPS as $1.551. The body text (paragraph 12) and the reconciliation table (paragraph 49) print $1.55, all with an 18 percent increase. GAAP diluted EPS is 1.46 in both the release and the 10-Q fact. The two adjusted figures are printed differently in the same document; the input does not say which is intended.", "account": "Adjusted diluted EPS (non-GAAP)", "expected_direction": "none", "horizon": "quarter ended 2026-06-30", "quote": "Adjusted diluted EPS was $1.551, an increase of 18 percent", "paragraph_id": "0000038725-26-000051:8k_2_02:10"}
```

```json
{"id": "across_documents_legal_settlement_against_pending_litigation_tag", "what_changed": "The release calls the Energy Systems charge a legal settlement expense and removes it from adjusted operating income (4.5) and adjusted EPS (0.08). The 10-Q tags the same 4500000 as LossContingencyLossInPeriod for the EssoSAF case, with PendingLitigationMember. The release describes the matter as settled; the tags describe it as pending.", "account": "GainLossRelatedToLitigationSettlement; LossContingencyLossInPeriod", "expected_direction": "none", "horizon": "quarter ended 2026-06-30", "quote": "included a $4.5 million legal settlement expense compared to $0.0 million in the second quarter of 2025", "paragraph_id": "0000038725-26-000051:8k_2_02:19"}
```

```json
{"id": "results_against_expectations_full_year_guidance_range_raised", "what_changed": "The company raised its full-year 2026 guidance: net sales of 2.21 to 2.29 billion and adjusted diluted EPS of 4.50 to 4.70. The prior guidance range is not in my input, so the size of the raise cannot be stated.", "account": "Guidance: net sales and adjusted diluted EPS", "expected_direction": "up", "horizon": "full year 2026", "quote": "The Company is raising its guidance for full year 2026 net sales to be in the range of $2.21 billion to $2.29 billion and full year 2026 Adjusted Diluted EPS to be in the range of $4.50 to $4.70.", "paragraph_id": "0000038725-26-000051:8k_2_02:22"}
```

```json
{"id": "narrative_signs_of_operating_pressure_sourced_materials_logistics_inflation", "what_changed": "The CEO says the company continues to manage inflationary price pressures in sourced materials and logistics lanes. The newest gross_margin cell in the trend table (quarter ended 2026-03-31) is the lowest of the 5 filled quarters; no gross_margin for the June quarter exists in my input.", "account": "Cost of sales (sourced materials, logistics)", "expected_direction": "down", "horizon": "rest of 2026", "quote": "we continue to manage closely the inflationary price pressures", "paragraph_id": "0000038725-26-000051:8k_2_02:15"}
```

```json
{"id": "narrative_signs_of_operating_pressure_energy_segment_operating_income_lower", "what_changed": "Energy Systems operating income is 27.9 million against 29.1 million, while its net sales are 80.2 against 77.5. The release's margin table prints 34.8% against 37.5%, and adjusted operating income excluding the legal charge prints 32.4 against 29.1. The 10-Q segment facts print 27900000 against 29100000.", "account": "OperatingIncomeLoss (Energy Systems segment)", "expected_direction": "down", "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30", "quote": "Energy Systems operating income in the second quarter of 2026 was $27.9 million compared to the second quarter 2025 operating income of $29.1 million", "paragraph_id": "0000038725-26-000051:8k_2_02:19"}
```

## Seen in the notes

No fact in my input carries a marker saying its element sat inside a note when it was extracted. Each fact prints only these fields:
- id, paragraph_id, tag, prefix, namespace
- context, context_ref, unit, decimals
- value, number, nil
- form, source_accession, filing_date
- and on some, superseded_by

The trend cells and the 8-K paragraphs carry no in-note field either. Because note membership is not marked, I place no item here, and I do not decide it myself from decimals, dimensions or tag names.
