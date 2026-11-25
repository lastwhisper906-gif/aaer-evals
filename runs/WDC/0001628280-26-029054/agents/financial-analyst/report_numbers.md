<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
WDC — trigger 0001628280-26-029054 (10-Q for the quarter 2026-01-03..2026-04-03, filed 2026-05-01). Numbers reader.

Run check. The directory holds input_8k.md, input_numbers.json, input_prior_predictions.md and input_trends.json and nothing else. None of them carries prices, abnormal returns, short interest, another company's files, a prior run's probability or an outcome window. The run is not broken on that count.

Conventions used in every item. `expected_direction` records the sign of the change that Python printed for the item: the quarter-over-quarter change for a quarterly trend cell, the year-over-year change for an annual trend cell, and for a numeric fact the later printed value set against the comparator named in `horizon`. It is `none` where no change is printed or the cell is insufficient. It is not a forecast. `horizon` names the window that change spans. Every number below is copied from the input, and none is derived. Where a number I would want does not exist in the input, the item says so.

Facts outside the items (none of them can be quoted against a printed row id):
- Periods. Every one of the 13 requested periods (8 quarters, 5 years) is on record with status `filled`. No period lies beyond the record, so no unreached-period reason applies. The record does have holes. quarters-back-3 (2025-03-29..2025-06-27) and quarters-back-7 (2024-03-30..2024-06-28) are fiscal fourth quarters and have no cost_of_revenue row, and no fourth-quarter derivation exists in the input. That is why days_sales_of_inventory and gross_margin have 6 filled quarters, not 8. Operating cash flow exists only year-to-date, so accruals_over_total_assets is filled in 2 of 8 quarters.
- No articulation-check section, restatement-trace section or fourth-quarter derivation exists in the input. So there are no Python-computed articulation gaps to report, and the only articulation item below comes from duplicate fact rows.
- Restated prior values. Many facts from the prior 10-Q (0001628280-26-004207) carry `"superseded_by": "0001628280-26-029054"`. Every superseded row I compared shows the same value in the trigger 10-Q:
  - stockholders' equity at 2025-06-27 and 2026-01-02;
  - net income for 2025-10-04..2026-01-02 and 2024-09-28..2024-12-27;
  - cash, receivables, inventory and assets at 2025-06-27.

  I found no restated prior value. That comparison was not exhaustive.
- Tag change. The prior 10-Q tags depreciation as DepreciationAndAmortization and the trigger 10-Q tags DepreciationDepletionAndAmortization (two items below).
- In-note marker. No fact in input_numbers.json carries the marker saying whether its element sat inside a note. Every fact row has only id, paragraph_id, tag, prefix, namespace, context, context_ref, unit, decimals, value, number, nil, form, source_accession, filing_date, and sometimes superseded_by.
- 8-K. input_8k.md says "no 8-K filed at or before 2026-05-01 is on record, so this bundle has no earnings release and no verbatim item body". Yet its own item-code list prints "2026-04-30 0001628280-26-028878 — 2.02, 9.01", which is a results 8-K one day before the 10-Q. The two lines do not agree. Either way the release body is not in the bundle, so no guidance, release figure or consensus number exists to measure results against.
  - The same file lists a late-filing notice: "2024-02-08 0000106040-24-000011 — NT 10-Q, for the period ended 2023-12-29".
  - None of these lines prints a paragraph id, so none is an item.
- Prior flags. input_prior_predictions.md says "None on record."
- R&D capitalization (years-back-0). The trend file's research_and_development_capitalized block is unfilled in full. Its reasons are "no row for research_and_development_expense: the companyfacts record tags none of us-gaap:ResearchAndDevelopmentExpense in any period" and "no row for capitalized_development_cost: the companyfacts record tags none of us-gaap:CapitalizedComputerSoftwareAdditions in any period".
  - The block prints no paragraph_id, so it is not an item.
  - The related tag mismatch is an item below.

## Seen in the statements

**Trend table: quarters-back-0 (2026-01-03..2026-04-03, 91 days)**

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarterly",
  "what_changed": "receivables_over_revenue is 0.5675756667665568. Change against quarters-back-1 is 0.009073843763573675 and against quarters-back-4 is -0.07279050585768032. It sits third lowest of the 8 filled quarters. Inputs: AccountsReceivableNetCurrent 1894000000.0 at 2026-04-03 over quarterly revenue 3337000000.0. Eight quarters give a position, not a trend.",
  "account": "AccountsReceivableNetCurrent over RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "up",
  "horizon": "quarters-back-0 against quarters-back-1 (quarters-back-4 printed alongside)",
  "quote": "\"position_in_history\": \"third lowest of the 8 filled quarters\"",
  "paragraph_id": "0001628280-26-029054:trends:receivables_over_revenue:2026-01-03..2026-04-03" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly",
  "what_changed": "days_sales_outstanding is 51.64938567575667. Change against quarters-back-1 is 0.8257197824852014 and against quarters-back-4 is -6.623936033048906. It sits third lowest of the 8 filled quarters. Same inputs as receivables_over_revenue, over 91 days.",
  "account": "AccountsReceivableNetCurrent, RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "up",
  "horizon": "quarters-back-0 against quarters-back-1 (quarters-back-4 printed alongside)",
  "quote": "\"position_in_history\": \"third lowest of the 8 filled quarters\"",
  "paragraph_id": "0001628280-26-029054:trends:days_sales_outstanding:2026-01-03..2026-04-03" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_quarterly",
  "what_changed": "days_sales_of_inventory is 74.34497290788681. Change against quarters-back-1 is -0.6452531153263834 and against quarters-back-4 is -11.979918553762971. It sits lowest of the 6 filled quarters. Only 6 quarters are filled because quarters-back-3 and quarters-back-7 have no cost_of_revenue row. Inputs: InventoryNet 1357000000.0 at 2026-04-03, CostOfGoodsAndServicesSold 1661000000.0.",
  "account": "InventoryNet, CostOfGoodsAndServicesSold",
  "expected_direction": "down",
  "horizon": "quarters-back-0 against quarters-back-1 (quarters-back-4 printed alongside)",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001628280-26-029054:trends:days_sales_of_inventory:2026-01-03..2026-04-03" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly",
  "what_changed": "gross_margin is 0.5022475277195085. Change against quarters-back-1 is 0.04483950650638291 and against quarters-back-4 is 0.10468867854775615. It sits highest of the 6 filled quarters. The history is 6 quarters because the two fiscal fourth quarters lack cost_of_revenue. Inputs: revenue 3337000000.0, CostOfGoodsAndServicesSold 1661000000.0.",
  "account": "RevenueFromContractWithCustomerExcludingAssessedTax, CostOfGoodsAndServicesSold",
  "expected_direction": "up",
  "horizon": "quarters-back-0 against quarters-back-1 (quarters-back-4 printed alongside)",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001628280-26-029054:trends:gross_margin:2026-01-03..2026-04-03" }
```

```json
{ "id": "earnings_quality_soft_asset_share_quarterly",
  "what_changed": "soft_asset_share is 0.7027583914921901. Change against quarters-back-1 is -0.020065258498201288 and against quarters-back-4 is 0.05857461827615884. The two printed changes have opposite signs. It sits fourth lowest of the 8 filled quarters. Inputs: Assets 15045000000.0, CashAndCashEquivalentsAtCarryingValue 2050000000.0, PropertyPlantAndEquipmentNet 2422000000.0, all at 2026-04-03.",
  "account": "Assets, PropertyPlantAndEquipmentNet, CashAndCashEquivalentsAtCarryingValue",
  "expected_direction": "down",
  "horizon": "quarters-back-0 against quarters-back-1 (quarters-back-4 printed alongside)",
  "quote": "\"position_in_history\": \"fourth lowest of the 8 filled quarters\"",
  "paragraph_id": "0001628280-26-029054:trends:soft_asset_share:2026-01-03..2026-04-03" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly",
  "what_changed": "warranty_reserve_ratio is 0.05693736889421636. Change against quarters-back-1 is -0.0017301816526845287 and against quarters-back-4 is 0.0063706731662303145. It sits fourth highest of the 8 filled quarters. Inputs: StandardProductWarrantyAccrual 190000000.0 at 2026-04-03 over one quarter's revenue 3337000000.0. The annual cell divides by a full year's revenue, so its value is on a different scale from this one.",
  "account": "StandardProductWarrantyAccrual over RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "down",
  "horizon": "quarters-back-0 against quarters-back-1 (quarters-back-4 printed alongside)",
  "quote": "\"position_in_history\": \"fourth highest of the 8 filled quarters\"",
  "paragraph_id": "0001628280-26-029054:trends:warranty_reserve_ratio:2026-01-03..2026-04-03" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly",
  "what_changed": "insufficient. The cell is unfilled because no operating cash flow row exists for the three months alone. Only the year-to-date figure exists (see liquidity_and_capital_operating_cash_flow_year_to_date). No quarterly accrual ratio exists, and none is derived here.",
  "account": "NetIncomeLoss, NetCashProvidedByUsedInOperatingActivities, Assets",
  "expected_direction": "none",
  "horizon": "quarters-back-0",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-01-03..2026-04-03: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0001628280-26-029054:trends:accruals_over_total_assets:2026-01-03..2026-04-03" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly",
  "what_changed": "insufficient. The record tags no allowance for doubtful accounts in any period, so no bad-debt reserve ratio exists for any of the 13 periods.",
  "account": "allowance for credit losses on receivables (untagged)",
  "expected_direction": "none",
  "horizon": "quarters-back-0",
  "quote": "\"missing\": \"no row for bad_debt_allowance: the companyfacts record tags none of us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable in any period.",
  "paragraph_id": "0001628280-26-029054:trends:bad_debt_reserve_ratio:2026-01-03..2026-04-03" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly",
  "what_changed": "insufficient. The contract-liability and deferred-revenue concepts exist in the record but not at 2026-04-03, so no ratio exists for this quarter.",
  "account": "ContractWithCustomerLiability / DeferredRevenue (absent at this date)",
  "expected_direction": "none",
  "horizon": "quarters-back-0",
  "quote": "\"missing\": \"no row for contract_liabilities in 2026-04-03: us-gaap:ContractWithCustomerLiabilityCurrent, us-gaap:ContractWithCustomerLiability, us-gaap:DeferredRevenueCurrent, us-gaap:DeferredRevenue is in the record, but not for this period\"",
  "paragraph_id": "0001628280-26-029054:trends:contract_liabilities_over_revenue:2026-01-03..2026-04-03" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly",
  "what_changed": "insufficient. The record tags no inventory valuation reserve in any period, so no inventory reserve ratio exists.",
  "account": "InventoryValuationReserves (untagged)",
  "expected_direction": "none",
  "horizon": "quarters-back-0",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period.",
  "paragraph_id": "0001628280-26-029054:trends:inventory_reserve_ratio:2026-01-03..2026-04-03" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly",
  "what_changed": "insufficient. No non-GAAP net income exists in the record, and the 8-K release that would carry one is not in the bundle.",
  "account": "non-GAAP net income against NetIncomeLoss",
  "expected_direction": "none",
  "horizon": "quarters-back-0",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001628280-26-029054:trends:non_gaap_gap:2026-01-03..2026-04-03" }
```

**Trend table: years-back-0 (2024-06-29..2025-06-27, 364 days)**

```json
{ "id": "earnings_quality_accruals_over_total_assets_annual",
  "what_changed": "accruals_over_total_assets is 0.014140837023282388. Change against years-back-1 is 0.03497761559116729. It sits highest of the 5 filled years. Inputs: NetIncomeLoss 1889000000.0 and NetCashProvidedByUsedInOperatingActivities 1691000000.0, both from 0000106040-25-000038 filed 2025-08-14, and Assets 14002000000.0 at 2025-06-27 from the trigger 10-Q. The ratio mixes two filings. The input does not say whether the net income and cash flow include the discontinued operations.",
  "account": "NetIncomeLoss, NetCashProvidedByUsedInOperatingActivities, Assets",
  "expected_direction": "up",
  "horizon": "years-back-0 against years-back-1",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-029054:trends:accruals_over_total_assets:2024-06-29..2025-06-27" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_annual",
  "what_changed": "days_sales_of_inventory is 80.63212079615649. Change against years-back-1 is -30.474393288350555. It sits lowest of the 5 filled years. Inputs: InventoryNet 1291000000.0 at 2025-06-27, CostOfGoodsAndServicesSold 5828000000.0 from the 10-K filed 2025-08-14.",
  "account": "InventoryNet, CostOfGoodsAndServicesSold",
  "expected_direction": "down",
  "horizon": "years-back-0 against years-back-1",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-029054:trends:days_sales_of_inventory:2024-06-29..2025-06-27" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual",
  "what_changed": "days_sales_outstanding is 56.81764705882353. Change against years-back-1 is -14.115390775591543. It sits third highest of the 5 filled years. Inputs: AccountsReceivableNetCurrent 1486000000.0 at 2025-06-27, revenue 9520000000.0.",
  "account": "AccountsReceivableNetCurrent, RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "down",
  "horizon": "years-back-0 against years-back-1",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-029054:trends:days_sales_outstanding:2024-06-29..2025-06-27" }
```

```json
{ "id": "earnings_quality_gross_margin_annual",
  "what_changed": "gross_margin is 0.3878151260504202. Change against years-back-1 is 0.10714392136465162. It sits highest of the 5 filled years. Inputs: revenue 9520000000.0, CostOfGoodsAndServicesSold 5828000000.0.",
  "account": "RevenueFromContractWithCustomerExcludingAssessedTax, CostOfGoodsAndServicesSold",
  "expected_direction": "up",
  "horizon": "years-back-0 against years-back-1",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-029054:trends:gross_margin:2024-06-29..2025-06-27" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual",
  "what_changed": "receivables_over_revenue is 0.15609243697478992. Change against years-back-1 is -0.03877854608678996. It sits third highest of the 5 filled years.",
  "account": "AccountsReceivableNetCurrent over RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "down",
  "horizon": "years-back-0 against years-back-1",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-029054:trends:receivables_over_revenue:2024-06-29..2025-06-27" }
```

```json
{ "id": "earnings_quality_soft_asset_share_annual",
  "what_changed": "soft_asset_share is 0.6816883302385374. Change against years-back-1 is -0.15666126460187935. It sits lowest of the 5 filled years. Inputs: Assets 14002000000.0, cash 2114000000.0, PropertyPlantAndEquipmentNet 2343000000.0, all at 2025-06-27.",
  "account": "Assets, PropertyPlantAndEquipmentNet, CashAndCashEquivalentsAtCarryingValue",
  "expected_direction": "down",
  "horizon": "years-back-0 against years-back-1",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-029054:trends:soft_asset_share:2024-06-29..2025-06-27" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_annual",
  "what_changed": "warranty_reserve_ratio is 0.015966386554621848. Change against years-back-1 is -0.006512638298947885. It sits second lowest of the 5 filled years. Inputs: StandardProductWarrantyAccrual 152000000.0 at 2025-06-27 over revenue 9520000000.0.",
  "account": "StandardProductWarrantyAccrual over RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "down",
  "horizon": "years-back-0 against years-back-1",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-029054:trends:warranty_reserve_ratio:2024-06-29..2025-06-27" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual",
  "what_changed": "insufficient. No allowance for doubtful accounts is tagged in any period, so no annual ratio exists.",
  "account": "allowance for credit losses on receivables (untagged)",
  "expected_direction": "none",
  "horizon": "years-back-0",
  "quote": "\"missing\": \"no row for bad_debt_allowance: the companyfacts record tags none of us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable in any period.",
  "paragraph_id": "0001628280-26-029054:trends:bad_debt_reserve_ratio:2024-06-29..2025-06-27" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual",
  "what_changed": "insufficient. Contract-liability concepts exist in the record but not at 2025-06-27.",
  "account": "ContractWithCustomerLiability / DeferredRevenue (absent at this date)",
  "expected_direction": "none",
  "horizon": "years-back-0",
  "quote": "\"missing\": \"no row for contract_liabilities in 2025-06-27: us-gaap:ContractWithCustomerLiabilityCurrent, us-gaap:ContractWithCustomerLiability, us-gaap:DeferredRevenueCurrent, us-gaap:DeferredRevenue is in the record, but not for this period\"",
  "paragraph_id": "0001628280-26-029054:trends:contract_liabilities_over_revenue:2024-06-29..2025-06-27" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_annual",
  "what_changed": "insufficient. No inventory valuation reserve is tagged in any period.",
  "account": "InventoryValuationReserves (untagged)",
  "expected_direction": "none",
  "horizon": "years-back-0",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period.",
  "paragraph_id": "0001628280-26-029054:trends:inventory_reserve_ratio:2024-06-29..2025-06-27" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual",
  "what_changed": "insufficient. No non-GAAP measure exists in the record for the fiscal year.",
  "account": "non-GAAP net income against NetIncomeLoss",
  "expected_direction": "none",
  "horizon": "years-back-0",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001628280-26-029054:trends:non_gaap_gap:2024-06-29..2025-06-27" }
```

**Articulation and the filed history**

```json
{ "id": "articulation_and_the_filed_history_receivables_printed_at_two_precisions",
  "what_changed": "The trigger 10-Q prints AccountsReceivableNetCurrent at 2026-04-03 twice under one paragraph_id. One row is 1894000000, the figure the trend table uses. The other (f-523, decimals -7, printed beside the customer-concentration facts) is 1890000000. The same pairing appears at 2025-06-27: 1486000000 in the trend inputs against 1490000000 at decimals -7 (f-524). The two rows differ only in printed precision and neither is marked as a restatement. No articulation-check section exists to say more.",
  "account": "AccountsReceivableNetCurrent",
  "expected_direction": "none",
  "horizon": "balance at 2026-04-03 (and 2025-06-27)",
  "quote": "\"value\": \"1890000000\"",
  "paragraph_id": "0001628280-26-029054:facts:AccountsReceivableNetCurrent:2026-04-03" }
```

```json
{ "id": "articulation_and_the_filed_history_preferred_liquidation_preference_after_conversion",
  "what_changed": "TemporaryEquityLiquidationPreference is still printed at 265000000 at 2026-04-03, the same figure as at 2025-06-27. Yet the temporary-equity carrying amount at 2026-04-03 is 0 (see structure_and_disclosure_changes_temporary_equity_eliminated), and the equity statement shows a conversion of 229000000 in the quarter. A liquidation preference printed for a class whose carrying amount is 0 is a row the input does not reconcile. A separate fact dated 2026-02-17 prints PreferredStockLiquidationPreferenceValue 267000000.",
  "account": "TemporaryEquityLiquidationPreference",
  "expected_direction": "none",
  "horizon": "2026-04-03 against 2025-06-27",
  "quote": "\"value\": \"265000000\"",
  "paragraph_id": "0001628280-26-029054:facts:TemporaryEquityLiquidationPreference:2026-04-03" }
```

**Changes of tag and concept**

```json
{ "id": "structure_and_disclosure_changes_depreciation_tag_trigger_filing",
  "what_changed": "The trigger 10-Q tags depreciation and amortization on the cash-flow statement as DepreciationDepletionAndAmortization: 276000000 for 2025-06-28..2026-04-03. The prior 10-Q used a different concept (next item). A reader chaining the two filings by tag finds no common row. The two periods differ (nine months against six), so no quarterly figure exists in the input, and none is derived.",
  "account": "DepreciationDepletionAndAmortization",
  "expected_direction": "none",
  "horizon": "2025-06-28..2026-04-03",
  "quote": "\"value\": \"276000000\"",
  "paragraph_id": "0001628280-26-029054:facts:DepreciationDepletionAndAmortization:2025-06-28..2026-04-03" }
```

```json
{ "id": "structure_and_disclosure_changes_depreciation_tag_prior_filing",
  "what_changed": "The prior 10-Q (0001628280-26-004207) tagged the same cash-flow line as DepreciationAndAmortization: 180000000 for 2025-06-28..2026-01-02. The concept changed between consecutive 10-Qs.",
  "account": "DepreciationAndAmortization",
  "expected_direction": "none",
  "horizon": "2025-06-28..2026-01-02",
  "quote": "\"value\": \"180000000\"",
  "paragraph_id": "0001628280-26-004207:facts:DepreciationAndAmortization:2025-06-28..2026-01-02" }
```

```json
{ "id": "structure_and_disclosure_changes_research_and_development_concept",
  "what_changed": "R&D is tagged as ResearchAndDevelopmentExpenseExcludingAcquiredInProcessCost: 294000000 for the quarter. The trend table looks only for us-gaap:ResearchAndDevelopmentExpense and finds it in no period. So the whole R&D-capitalization block (book value and earnings with R&D capitalized, capitalized over expense) is unfilled for this company. That is a concept mismatch, not missing spending.",
  "account": "ResearchAndDevelopmentExpenseExcludingAcquiredInProcessCost",
  "expected_direction": "none",
  "horizon": "2026-01-03..2026-04-03",
  "quote": "\"value\": \"294000000\"",
  "paragraph_id": "0001628280-26-029054:facts:ResearchAndDevelopmentExpenseExcludingAcquiredInProcessCost:2026-01-03..2026-04-03" }
```

```json
{ "id": "structure_and_disclosure_changes_discontinued_operations_in_prior_year",
  "what_changed": "The prior-year quarter 2024-12-28..2025-03-28 carries net income from discontinued operations to common of -248000000. The current quarter prints 0. Income from continuing operations for the prior-year quarter is 772000000. Prior-year totals mix continuing and discontinued results, and year-over-year comparisons of bottom-line figures cross that change.",
  "account": "NetIncomeLossFromDiscontinuedOperationsAvailableToCommonShareholdersBasic",
  "expected_direction": "none",
  "horizon": "2026-01-03..2026-04-03 against 2024-12-28..2025-03-28",
  "quote": "\"value\": \"-248000000\"",
  "paragraph_id": "0001628280-26-029054:facts:NetIncomeLossFromDiscontinuedOperationsAvailableToCommonShareholdersBasic:2024-12-28..2025-03-28" }
```

```json
{ "id": "structure_and_disclosure_changes_single_reportable_segment",
  "what_changed": "The 10-Q reports one reportable segment for 2025-06-28..2026-04-03. Its HDD segment revenue for the quarter is printed at 3337000000, the same as total revenue. No segment split exists against which to test revenue mix.",
  "account": "NumberOfReportableSegments",
  "expected_direction": "none",
  "horizon": "2025-06-28..2026-04-03",
  "quote": "\"value\": \"1\"",
  "paragraph_id": "0001628280-26-029054:facts:NumberOfReportableSegments:2025-06-28..2026-04-03" }
```

```json
{ "id": "structure_and_disclosure_changes_temporary_equity_eliminated",
  "what_changed": "The temporary-equity carrying amount (convertible preferred) is 0 at 2026-04-03, against 229000000 earlier. The equity statement prints a conversion of convertible securities of 229000000 in the quarter. A paid-in-kind preferred dividend of 32000000 is printed for 2026-02-17..2026-03-17.",
  "account": "TemporaryEquityCarryingAmountAttributableToParent",
  "expected_direction": "down",
  "horizon": "2026-04-03 against 2025-06-27",
  "quote": "\"value\": \"0\"",
  "paragraph_id": "0001628280-26-029054:facts:TemporaryEquityCarryingAmountAttributableToParent:2026-04-03" }
```

```json
{ "id": "structure_and_disclosure_changes_convertible_conversion_price",
  "what_changed": "The conversion price of the 3.00% convertible notes due 2028 is printed at 37.72 at 2026-04-03, in two rows that share this paragraph_id. My read of the prior 10-Q (0001628280-26-004207) printed 37.74 for this term. That row is not quoted here, and the input does not mark the change as a restatement. The capped-call cap price is printed at 50.41.",
  "account": "DebtInstrumentConvertibleConversionPrice1",
  "expected_direction": "down",
  "horizon": "2026-04-03 against 2026-01-02",
  "quote": "\"value\": \"37.72\"",
  "paragraph_id": "0001628280-26-029054:facts:DebtInstrumentConvertibleConversionPrice1:2026-04-03:us-gaap:DebtInstrumentAxis=wdc:ThreePointZeroZeroPercentConvertibleNotesDueTwoThousandTwentyEightMember,us-gaap:LongtermDebtTypeAxis=us-gaap:ConvertibleDebtMember" }
```

**Results, earnings quality and estimates (numeric facts)**

```json
{ "id": "results_against_expectations_revenue_without_a_benchmark",
  "what_changed": "Revenue is 3337000000 for 2026-01-03..2026-04-03, against 2294000000 for 2024-12-28..2025-03-28 in the same filing, and nine-month revenue is 9172000000. The input holds no guidance, no release figure and no consensus number, so whether this beat or missed expectations is insufficient. No benchmark exists in the bundle.",
  "account": "RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "up",
  "horizon": "2026-01-03..2026-04-03 against 2024-12-28..2025-03-28",
  "quote": "\"value\": \"3337000000\"",
  "paragraph_id": "0001628280-26-029054:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-01-03..2026-04-03" }
```

```json
{ "id": "earnings_quality_operating_income",
  "what_changed": "Operating income is 1190000000 for the quarter, against 760000000 in the prior-year quarter. The prior-year quarter carried a litigation settlement gain of 201000000 (see related_parties_contingencies_and_subsequent_events_ip_litigation_settlement_gain). The current quarter prints 0 for that line.",
  "account": "OperatingIncomeLoss",
  "expected_direction": "up",
  "horizon": "2026-01-03..2026-04-03 against 2024-12-28..2025-03-28",
  "quote": "\"value\": \"1190000000\"",
  "paragraph_id": "0001628280-26-029054:facts:OperatingIncomeLoss:2026-01-03..2026-04-03" }
```

```json
{ "id": "earnings_quality_unrealized_gain_on_equity_securities",
  "what_changed": "An unrealized gain on equity securities of 2734000000 is booked in the quarter, against -606000000 in the prior-year quarter, with 4448000000 for nine months. The quarter's gain is larger than the quarter's operating income of 1190000000. Pretax income is 3359000000 and income from continuing operations is 3205000000. Much of reported earnings is a mark-to-market on a held stake rather than operations.",
  "account": "EquitySecuritiesFvNiUnrealizedGainLoss",
  "expected_direction": "up",
  "horizon": "2026-01-03..2026-04-03 against 2024-12-28..2025-03-28",
  "quote": "\"value\": \"2734000000\"",
  "paragraph_id": "0001628280-26-029054:facts:EquitySecuritiesFvNiUnrealizedGainLoss:2026-01-03..2026-04-03:us-gaap:StatementBusinessSegmentsAxis=wdc:HDDMember" }
```

```json
{ "id": "earnings_quality_income_from_continuing_operations",
  "what_changed": "Income from continuing operations is 3205000000 for the quarter, against 772000000 in the prior-year quarter. Nine months print 6229000000 against 1391000000. Basic EPS from continuing operations is 9.26 against 2.17. The prior-year quarter's figure was lifted by an income tax benefit of -698000000 on pretax income of 74000000. The current quarter's figure is lifted by the equity-securities gain.",
  "account": "IncomeLossFromContinuingOperations",
  "expected_direction": "up",
  "horizon": "2026-01-03..2026-04-03 against 2024-12-28..2025-03-28",
  "quote": "\"value\": \"3205000000\"",
  "paragraph_id": "0001628280-26-029054:facts:IncomeLossFromContinuingOperations:2026-01-03..2026-04-03" }
```

```json
{ "id": "earnings_quality_debt_extinguishment_loss",
  "what_changed": "The quarter carries a loss on extinguishment of debt of -545000000, against 0 in the prior-year quarter. The printed components are -539000000 on Term Loan A-3 and -6000000 on senior notes, both dated 2026-02-01..2026-02-28.",
  "account": "GainsLossesOnExtinguishmentOfDebt",
  "expected_direction": "down",
  "horizon": "2026-01-03..2026-04-03 against 2024-12-28..2025-03-28",
  "quote": "\"value\": \"-545000000\"",
  "paragraph_id": "0001628280-26-029054:facts:GainsLossesOnExtinguishmentOfDebt:2026-01-03..2026-04-03:us-gaap:StatementBusinessSegmentsAxis=wdc:HDDMember" }
```

```json
{ "id": "earnings_quality_term_loan_extinguishment_component",
  "what_changed": "The Term Loan A-3 extinguishment in 2026-02-01..2026-02-28 prints a loss of -539000000. The loan's carrying amount was 1649000000 at 2025-06-27 and is 0 at 2026-04-03, and a 9-month term loan repayment of 63000000 is printed. The input does not say what was given to settle the loan, so the source of a loss this size is not shown.",
  "account": "GainsLossesOnExtinguishmentOfDebt (Term Loan A-3)",
  "expected_direction": "down",
  "horizon": "2026-02-01..2026-02-28",
  "quote": "\"value\": \"-539000000\"",
  "paragraph_id": "0001628280-26-029054:facts:GainsLossesOnExtinguishmentOfDebt:2026-02-01..2026-02-28:us-gaap:DebtInstrumentAxis=wdc:TermLoanA3Member" }
```

```json
{ "id": "estimates_and_discretion_effective_tax_rate",
  "what_changed": "The effective tax rate is printed at 0.05 for the quarter, against -9.43 for the prior-year quarter. Nine months print 0.06 against -0.78. Income tax expense is 154000000, against a benefit of -698000000 a year earlier. The low current rate applies to pretax income that is mostly an unrealized securities gain, and the input does not show the rate's drivers.",
  "account": "EffectiveIncomeTaxRateContinuingOperations",
  "expected_direction": "up",
  "horizon": "2026-01-03..2026-04-03 against 2024-12-28..2025-03-28",
  "quote": "\"value\": \"0.05\"",
  "paragraph_id": "0001628280-26-029054:facts:EffectiveIncomeTaxRateContinuingOperations:2026-01-03..2026-04-03" }
```

```json
{ "id": "estimates_and_discretion_unrecognized_tax_benefits",
  "what_changed": "Unrecognized tax benefits are 603000000 at 2026-04-03, against 569000000 at 2025-06-27. Increases of 8000000 for current-period positions and 30000000 for prior-period positions are printed for nine months. Accrued interest and penalties are 123000000. The noncurrent liability for uncertain tax positions is 228000000, against 163000000.",
  "account": "UnrecognizedTaxBenefits",
  "expected_direction": "up",
  "horizon": "2026-04-03 against 2025-06-27",
  "quote": "\"value\": \"603000000\"",
  "paragraph_id": "0001628280-26-029054:facts:UnrecognizedTaxBenefits:2026-04-03" }
```

```json
{ "id": "estimates_and_discretion_warranty_provisions",
  "what_changed": "Warranties issued in the quarter are 40000000, against 24000000 in the prior-year quarter. Payments are 21000000 against 18000000. The warranty accrual is 190000000 at 2026-04-03, against 152000000 at 2025-06-27. The noncurrent part is 151000000 against 95000000, and the current part is 39000000 against 57000000.",
  "account": "StandardProductWarrantyAccrualWarrantiesIssued",
  "expected_direction": "up",
  "horizon": "2026-01-03..2026-04-03 against 2024-12-28..2025-03-28",
  "quote": "\"value\": \"40000000\"",
  "paragraph_id": "0001628280-26-029054:facts:StandardProductWarrantyAccrualWarrantiesIssued:2026-01-03..2026-04-03" }
```

```json
{ "id": "estimates_and_discretion_warranty_estimate_changes",
  "what_changed": "Changes in estimate for pre-existing warranties are 0 for nine months, against -38000000 for the prior-year nine months. The quarter prints -6000000 against -11000000. Smaller releases of prior estimates are being booked.",
  "account": "StandardProductWarrantyAccrualPreexistingIncreaseDecrease",
  "expected_direction": "up",
  "horizon": "2025-06-28..2026-04-03 against 2024-06-29..2025-03-28",
  "quote": "\"value\": \"0\"",
  "paragraph_id": "0001628280-26-029054:facts:StandardProductWarrantyAccrualPreexistingIncreaseDecrease:2025-06-28..2026-04-03" }
```

```json
{ "id": "earnings_quality_share_based_compensation",
  "what_changed": "Share-based compensation expense is 53000000 for the quarter, against 35000000 in the prior-year quarter. Nine months print 159000000 against 122000000. Unrecognized compensation cost is 331000000 at 2026-04-03. RSU and PSU grants for nine months are 2600000 units at a weighted grant-date fair value of 83.26.",
  "account": "AllocatedShareBasedCompensationExpense",
  "expected_direction": "up",
  "horizon": "2026-01-03..2026-04-03 against 2024-12-28..2025-03-28",
  "quote": "\"value\": \"53000000\"",
  "paragraph_id": "0001628280-26-029054:facts:AllocatedShareBasedCompensationExpense:2026-01-03..2026-04-03" }
```

```json
{ "id": "earnings_quality_diluted_share_count",
  "what_changed": "Incremental dilutive shares are 45000000 for the quarter, against 10000000 in the prior-year quarter. Diluted weighted shares are 387000000 against basic 342000000. Diluted EPS is printed at 8.20 and basic at 9.26. The concept used is IncrementalCommonSharesAttributableToShareBasedPaymentArrangements. The input does not split how much of the count comes from the in-the-money convertible notes.",
  "account": "IncrementalCommonSharesAttributableToShareBasedPaymentArrangements",
  "expected_direction": "up",
  "horizon": "2026-01-03..2026-04-03 against 2024-12-28..2025-03-28",
  "quote": "\"value\": \"45000000\"",
  "paragraph_id": "0001628280-26-029054:facts:IncrementalCommonSharesAttributableToShareBasedPaymentArrangements:2026-01-03..2026-04-03" }
```

```json
{ "id": "revenue_recognition_customer_receivable_concentration",
  "what_changed": "Customer one holds 0.28 of accounts receivable in the context ending 2026-04-03, against 0.20 in the context ending 2025-06-27. Customer two holds 0.12 against 0.19. Concentration of receivables in the largest customer is higher.",
  "account": "ConcentrationRiskPercentage1 (customer one, accounts receivable)",
  "expected_direction": "up",
  "horizon": "context 2025-06-28..2026-04-03 against 2024-06-29..2025-06-27",
  "quote": "\"value\": \"0.28\"",
  "paragraph_id": "0001628280-26-029054:facts:ConcentrationRiskPercentage1:2025-06-28..2026-04-03:srt:MajorCustomersAxis=wdc:CustomerOneMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:AccountsReceivableMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember" }
```

```json
{ "id": "estimates_and_discretion_pension_funded_status",
  "what_changed": "The defined-benefit funded status is -75000000 at 2026-04-03, against -68000000 at 2025-06-27. Plan assets are 176000000 against 204000000, and the benefit obligation is 251000000 against 272000000. The expected long-term return assumption is printed at 0.025.",
  "account": "DefinedBenefitPlanFundedStatusOfPlan",
  "expected_direction": "down",
  "horizon": "2026-04-03 against 2025-06-27",
  "quote": "\"value\": \"-75000000\"",
  "paragraph_id": "0001628280-26-029054:facts:DefinedBenefitPlanFundedStatusOfPlan:2026-04-03" }
```

**Liquidity and capital (numeric facts)**

```json
{ "id": "liquidity_and_capital_operating_cash_flow_year_to_date",
  "what_changed": "Operating cash flow is 2540000000 for nine months 2025-06-28..2026-04-03, against 945000000 for 2024-06-29..2025-03-28. No three-month operating cash flow exists in the input. That is why quarterly accruals are insufficient, and no quarterly figure is derived here.",
  "account": "NetCashProvidedByUsedInOperatingActivities",
  "expected_direction": "up",
  "horizon": "2025-06-28..2026-04-03 against 2024-06-29..2025-03-28",
  "quote": "\"value\": \"2540000000\"",
  "paragraph_id": "0001628280-26-029054:facts:NetCashProvidedByUsedInOperatingActivities:2025-06-28..2026-04-03" }
```

```json
{ "id": "liquidity_and_capital_long_term_debt_noncurrent",
  "what_changed": "Noncurrent long-term debt is 0 at 2026-04-03, against 2485000000 at 2025-06-27. The 4.75% notes due 2026, the 2.85% notes due 2029, the 3.10% notes due 2032 and Term Loan A-3 all print a carrying amount of 0 at 2026-04-03. Total debt principal (DebtInstrumentCarryingAmount) is 1600000000, against 4749000000.",
  "account": "LongTermDebtNoncurrent",
  "expected_direction": "down",
  "horizon": "2026-04-03 against 2025-06-27",
  "quote": "\"value\": \"0\"",
  "paragraph_id": "0001628280-26-029054:facts:LongTermDebtNoncurrent:2026-04-03" }
```

```json
{ "id": "liquidity_and_capital_long_term_debt_current",
  "what_changed": "Current long-term debt is 1581000000 at 2026-04-03, against 2226000000 at 2025-06-27. Total LongTermDebt is also 1581000000, so all remaining debt is classified current. The only instrument with a carrying amount is the 3.00% convertible notes due 2028, with face value 1600000000. The input does not state why notes due 2028 sit in current liabilities.",
  "account": "LongTermDebtCurrent",
  "expected_direction": "down",
  "horizon": "2026-04-03 against 2025-06-27",
  "quote": "\"value\": \"1581000000\"",
  "paragraph_id": "0001628280-26-029054:facts:LongTermDebtCurrent:2026-04-03" }
```

```json
{ "id": "liquidity_and_capital_convertible_notes_fair_value",
  "what_changed": "The Level 2 fair-value estimate of the 3.00% convertible notes due 2028 is 12507000000 at 2026-04-03, against a carrying amount of 1581000000. At 2025-06-27 the estimate was 2849000000 against carrying 1575000000. Total debt fair value is 12507000000 against 5908000000. The conversion price is 37.72.",
  "account": "LongTermDebtFairValue (convertible notes due 2028)",
  "expected_direction": "up",
  "horizon": "2026-04-03 against 2025-06-27",
  "quote": "\"value\": \"12507000000\"",
  "paragraph_id": "0001628280-26-029054:facts:LongTermDebtFairValue:2026-04-03:us-gaap:DebtInstrumentAxis=wdc:ThreePointZeroZeroPercentConvertibleNotesDueTwoThousandTwentyEightMember,us-gaap:FairValueByFairValueHierarchyLevelAxis=us-gaap:FairValueInputsLevel2Member,us-gaap:FairValueByMeasurementBasisAxis=us-gaap:EstimateOfFairValueFairValueDisclosureMember" }
```

```json
{ "id": "liquidity_and_capital_bridge_loan",
  "what_changed": "A bridge loan with face amount 1500000000 is printed at 2026-02-28 (decimals -7), in the same month as the Term Loan A-3 and senior-note extinguishments. Its carrying amount at 2026-04-03 does not appear among the instruments printed at that date.",
  "account": "DebtInstrumentFaceAmount (bridge loan)",
  "expected_direction": "none",
  "horizon": "2026-02-28",
  "quote": "\"value\": \"1500000000\"",
  "paragraph_id": "0001628280-26-029054:facts:DebtInstrumentFaceAmount:2026-02-28:us-gaap:DebtInstrumentAxis=us-gaap:BridgeLoanMember" }
```

```json
{ "id": "liquidity_and_capital_cash",
  "what_changed": "Cash and cash equivalents are 2050000000 at 2026-04-03, against 2114000000 at 2025-06-27.",
  "account": "CashAndCashEquivalentsAtCarryingValue",
  "expected_direction": "down",
  "horizon": "2026-04-03 against 2025-06-27",
  "quote": "\"value\": \"2050000000\"",
  "paragraph_id": "0001628280-26-029054:facts:CashAndCashEquivalentsAtCarryingValue:2026-04-03" }
```

```json
{ "id": "liquidity_and_capital_equity_securities_stake",
  "what_changed": "Equity securities at fair value (Level 1) are 1187000000 at 2026-04-03, against 354000000 at 2025-06-27. The prior 10-Q printed 2068000000 at 2026-01-02. The holding is lower at quarter end despite the quarter's 2734000000 unrealized gain. The input holds no row that shows how the shares left the balance sheet.",
  "account": "EquitySecuritiesFvNi",
  "expected_direction": "up",
  "horizon": "2026-04-03 against 2025-06-27",
  "quote": "\"value\": \"1187000000\"",
  "paragraph_id": "0001628280-26-029054:facts:EquitySecuritiesFvNi:2026-04-03:us-gaap:FairValueByAssetClassAxis=us-gaap:EquitySecuritiesMember" }
```

```json
{ "id": "liquidity_and_capital_share_repurchases",
  "what_changed": "Treasury stock bought in the quarter is 752000000 for 2900000 shares. For nine months it is 1920000000 for 13100000 shares. Remaining repurchase authorization is 3930000000 at 2026-04-03. Excise tax on repurchases is 5000000 for the quarter.",
  "account": "TreasuryStockValueAcquiredCostMethod",
  "expected_direction": "none",
  "horizon": "2026-01-03..2026-04-03",
  "quote": "\"value\": \"752000000\"",
  "paragraph_id": "0001628280-26-029054:facts:TreasuryStockValueAcquiredCostMethod:2026-01-03..2026-04-03" }
```

```json
{ "id": "liquidity_and_capital_stockholders_equity",
  "what_changed": "Stockholders' equity is 9680000000 at 2026-04-03, against 5311000000 at 2025-06-27.",
  "account": "StockholdersEquity",
  "expected_direction": "up",
  "horizon": "2026-04-03 against 2025-06-27",
  "quote": "\"value\": \"9680000000\"",
  "paragraph_id": "0001628280-26-029054:facts:StockholdersEquity:2026-04-03" }
```

```json
{ "id": "liquidity_and_capital_accrued_income_taxes_paid_down",
  "what_changed": "The change in accrued income taxes payable is -598000000 for nine months in the cash-flow statement. Current accrued income taxes are printed at 202000000 at 2026-04-03.",
  "account": "IncreaseDecreaseInAccruedIncomeTaxesPayable",
  "expected_direction": "down",
  "horizon": "2025-06-28..2026-04-03",
  "quote": "\"value\": \"-598000000\"",
  "paragraph_id": "0001628280-26-029054:facts:IncreaseDecreaseInAccruedIncomeTaxesPayable:2025-06-28..2026-04-03" }
```

```json
{ "id": "liquidity_and_capital_construction_in_progress",
  "what_changed": "Construction in progress (gross PP&E) is 464000000 at 2026-04-03, against 532000000 at 2025-06-27. Gross PP&E is 9350000000 against 9085000000, and net PP&E is 2422000000 against 2343000000. Capital expenditure for nine months is printed at 310000000.",
  "account": "PropertyPlantAndEquipmentGross (construction in progress)",
  "expected_direction": "down",
  "horizon": "2026-04-03 against 2025-06-27",
  "quote": "\"value\": \"464000000\"",
  "paragraph_id": "0001628280-26-029054:facts:PropertyPlantAndEquipmentGross:2026-04-03:us-gaap:PropertyPlantAndEquipmentByTypeAxis=us-gaap:ConstructionInProgressMember" }
```

**Operating pressure, contingencies and subsequent events (numeric facts)**

```json
{ "id": "narrative_signs_of_operating_pressure_restructuring_charges",
  "what_changed": "Business-realignment restructuring charges are 95000000 for nine months, all one-time termination benefits (contract termination prints 0). Payments are 76000000. The reserve is 29000000 at 2026-04-03, against 10000000 at 2025-06-27. Accelerated share-based compensation in realignment is 5000000 for the quarter.",
  "account": "RestructuringCharges (business realignment)",
  "expected_direction": "up",
  "horizon": "2025-06-28..2026-04-03",
  "quote": "\"value\": \"95000000\"",
  "paragraph_id": "0001628280-26-029054:facts:RestructuringCharges:2025-06-28..2026-04-03:us-gaap:RestructuringPlanAxis=wdc:BusinessRealignmentActivitiesMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_dividend_increase",
  "what_changed": "A dividend per share of 0.15 is declared on 2026-04-29, tagged as a subsequent event. The quarter's declared dividend was 0.125.",
  "account": "CommonStockDividendsPerShareDeclared",
  "expected_direction": "up",
  "horizon": "2026-04-29 against 2026-01-03..2026-04-03",
  "quote": "\"value\": \"0.15\"",
  "paragraph_id": "0001628280-26-029054:facts:CommonStockDividendsPerShareDeclared:2026-04-29..2026-04-29:us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_spex_litigation",
  "what_changed": "In the SPEX Technologies case, damages awarded of 316000000 are printed for 2024-10-18 and settlement interest of 237000000 for 2025-01-08. Later damages-awarded rows for 2025-06-16 and 2025-06-27 print 1 at decimals 0. The case is tagged settled. No current-period accrual for it appears in the input.",
  "account": "LossContingencyDamagesAwardedValue (SPEX)",
  "expected_direction": "down",
  "horizon": "2024-10-18 against 2025-06-27",
  "quote": "\"value\": \"316000000\"",
  "paragraph_id": "0001628280-26-029054:facts:LossContingencyDamagesAwardedValue:2024-10-18..2024-10-18:srt:LitigationCaseAxis=wdc:SPEXTechnologiesInc.LawsuitMember,us-gaap:LitigationStatusAxis=us-gaap:SettledLitigationMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_ip_litigation_settlement_gain",
  "what_changed": "A gain related to an intellectual-property litigation settlement of 201000000 sits in the prior-year quarter 2024-12-28..2025-03-28, and 198000000 in the prior-year nine months. A settlement payment of 130000000 is printed for 2025-04-01..2025-04-30. The current quarter has no such gain, so year-over-year operating comparisons cross a one-off item.",
  "account": "GainLossRelatedToLitigationSettlement",
  "expected_direction": "down",
  "horizon": "2024-12-28..2025-03-28 against 2026-01-03..2026-04-03",
  "quote": "\"value\": \"201000000\"",
  "paragraph_id": "0001628280-26-029054:facts:GainLossRelatedToLitigationSettlement:2024-12-28..2025-03-28:srt:LitigationCaseAxis=wdc:IntellectualPropertyLitigationMember,us-gaap:LitigationStatusAxis=us-gaap:SettledLitigationMember" }
```

## Seen in the notes

No items. Each fact was supposed to carry a marker saying whether its element sat inside a note when it was extracted. No fact in input_numbers.json carries that marker. With no marker, the input does not say which facts came from a table inside a note, and I have not placed any here on my own reading.

Several items above use tags that 10-Qs usually disclose in notes. They stay under "Seen in the statements" only because the input does not mark them; a later split should treat their placement as unverified. They are:
- the warranty roll-forward;
- debt fair value and conversion terms;
- customer concentration;
- the effective tax rate and unrecognized tax benefits;
- restructuring;
- litigation;
- share-based compensation;
- pension;
- PP&E by type;
- the receivables row at decimals -7.
