# CIEN — numbers report — 10-Q 0001628280-26-040767 (quarter ended 2026-05-02), cutoff 2026-06-04

**Input check.** My directory holds input_8k.md, input_numbers.json, input_prior_predictions.md and input_trends.json. None of them holds prices, abnormal returns, short interest, another company's files, a prior run's probability or an outcome window. input_prior_predictions.md says: no earlier run on record, so there are no prior flags to carry forward.

**Inputs the instructions describe that are not in my directory.** There is no articulation-check file, no restatement-trace file and no fourth-quarter derivation file. So:
- I report no articulation gap; none is in my input.
- I report no fourth-quarter figure; none exists in my input.
- My restatement check is limited to comparing the prior-period values the 10-Qs print against the values the 10-K first printed (see below).

**Periods the record does not reach.** Two requested quarters have no cells in the trend table:
- quarters-back-2 (target end 2025-11-01). Reason given: "no quarter ending within 20 days of 2025-11-01 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py".
- quarters-back-6 (target end 2024-11-02). The table gives the same reason for 2024-11-02.

Because quarters-back-2 is missing, no quarter-over-quarter change is printed for quarters-back-1.

**Restated prior values.** I found none.
- These 2025-11-01 comparatives in the Q1 10-Q (0001628280-26-015152) and this 10-Q equal the values the 10-K (0001628280-25-056698) first printed:
  - accounts receivable
  - inventory, net
  - inventory valuation reserves
  - warranty accrual
  - contract liabilities
  - accrued liabilities
  - accrued salaries
  - assets
  - equity
- Every superseded_by link I read points to a later filing that prints the same value.
- The year-ago quarter (2025-02-02..2025-05-03) cannot be checked. The fiscal-2025 second-quarter 10-Q is not in my input, so no earlier-printed value exists to compare.
- Some paragraph_ids carry two facts that differ only in rounding. Examples: InventoryWriteDown in the 10-K (48424000 / 48400000), the Q1 10-Q (21832000 / 21800000) and this 10-Q (42481000 / 42500000). These are precision duplicates, not restatements.

**Changes of tag.** I report two, both below:
- the allowance concept that differs between quarterly and annual cells;
- the warranty accrual, which is tagged under a concept the trend table did not search.

**Other notes.**
- The R&D-capitalized baseline block in the trend table prints no paragraph_id. Its item quotes the fiscal-2025 R&D expense fact instead.
- The 8-K file lists no late-filing notification on or before 2026-06-04. That line has no paragraph id, so it is not an item.

**Direction convention.**
- Trend cells: expected_direction is the sign of the change Python printed. Where a cell prints changes of opposite sign, it is none.
- Facts: it is the direction the printed values moved from the earlier date to the later one, read off the printed values. No difference is computed.

## Seen in the statements

### Trend table — quarters-back-0 (2026-02-01..2026-05-02)

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly",
  "what_changed": "Bad-debt reserve ratio, bad_debt_allowance / (receivables + bad_debt_allowance), for quarters-back-0 is 0.010342535369120387. Printed change against quarters-back-1: -0.001102292386221896; against quarters-back-4: -8.744593141313782e-05. Position: third lowest of the 6 filled quarters, i.e. inside its history, not at an extreme. Inputs as printed: AllowanceForDoubtfulAccountsReceivable 11000000.0 and AccountsReceivableNetCurrent 1052569000.0, both from 0001628280-26-040767.",
  "account": "Allowance for doubtful accounts; accounts receivable, net",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-05-02, against the prior quarter and the year-ago quarter",
  "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
  "paragraph_id": "0001628280-26-040767:trends:bad_debt_reserve_ratio:2026-02-01..2026-05-02" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly",
  "what_changed": "Current contract liabilities over quarterly revenue for quarters-back-0 is 0.1517629599825305. Printed change against quarters-back-1: -0.05174751833555685; against quarters-back-4: -0.045269933457078415. Position: lowest of the 6 filled quarters. Inputs as printed: ContractWithCustomerLiabilityCurrent 238380000.0 and Revenues 1570739000.0, both from 0001628280-26-040767. The numerator is the current concept only. The release balance sheet prints a separate long-term deferred revenue line (102,107 thousands), which this ratio does not include.",
  "account": "Contract liabilities (current deferred revenue); revenue",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-05-02, against the prior quarter and the year-ago quarter",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001628280-26-040767:trends:contract_liabilities_over_revenue:2026-02-01..2026-05-02" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_quarterly",
  "what_changed": "Days sales of inventory, inventory / cost_of_revenue * days_in_period, for quarters-back-0 is 83.678266803915. Printed change against quarters-back-1: -12.351402999284417; against quarters-back-4: -34.53709335298505. Position: lowest of the 6 filled quarters. Inputs as printed: InventoryNet 808447000.0 and CostOfGoodsAndServicesSold 879185000.0, both from 0001628280-26-040767; the period is 91 days.",
  "account": "Inventories, net; cost of goods sold",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-05-02, against the prior quarter and the year-ago quarter",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001628280-26-040767:trends:days_sales_of_inventory:2026-02-01..2026-05-02" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly",
  "what_changed": "Days sales outstanding, receivables / revenue * days_in_period, for quarters-back-0 is 60.98007307388433. Printed change against quarters-back-1: -0.7098617703599146; against quarters-back-4: -14.171683155476217. Position: lowest of the 6 filled quarters. Inputs as printed: AccountsReceivableNetCurrent 1052569000.0 and Revenues 1570739000.0, both from 0001628280-26-040767.",
  "account": "Accounts receivable, net; revenue",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-05-02, against the prior quarter and the year-ago quarter",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001628280-26-040767:trends:days_sales_outstanding:2026-02-01..2026-05-02" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly",
  "what_changed": "Gross margin, (revenue - cost_of_revenue) / revenue, for quarters-back-0 is 0.44027301798707486. Printed change against quarters-back-1: 0.0019397383779253263; against quarters-back-4: 0.038064252916614305. Position: highest of the 6 filled quarters. Inputs as printed: Revenues 1570739000.0 and CostOfGoodsAndServicesSold 879185000.0, both from 0001628280-26-040767.",
  "account": "Revenue; cost of goods sold",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-05-02, against the prior quarter and the year-ago quarter",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001628280-26-040767:trends:gross_margin:2026-02-01..2026-05-02" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly",
  "what_changed": "Inventory reserve ratio, inventory_reserve / inventory, for quarters-back-0 is 0.19387170711252563. Printed change against quarters-back-1: 0.021326150890952078; against quarters-back-4: 0.05888658714583128. Position: highest of the 6 filled quarters. Inputs as printed: InventoryValuationReserves 156735000.0 and InventoryNet 808447000.0, both from 0001628280-26-040767. The provision behind the reserve is tagged only for six months (42481000 / 42500000, against 23431000 a year earlier) and for the first quarter (21832000); no three-month figure for the quarter ended 2026-05-02 exists in my input.",
  "account": "Inventory valuation reserves; inventories, net",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-05-02, against the prior quarter and the year-ago quarter",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001628280-26-040767:trends:inventory_reserve_ratio:2026-02-01..2026-05-02" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarterly",
  "what_changed": "Receivables over quarterly revenue for quarters-back-0 is 0.670110693119608. Printed change against quarters-back-1: -0.0078006787951638845; against quarters-back-4: -0.15573278192831008. Position: lowest of the 6 filled quarters. Inputs as printed: AccountsReceivableNetCurrent 1052569000.0 and Revenues 1570739000.0, both from 0001628280-26-040767.",
  "account": "Accounts receivable, net; revenue",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-05-02, against the prior quarter and the year-ago quarter",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001628280-26-040767:trends:receivables_over_revenue:2026-02-01..2026-05-02" }
```

```json
{ "id": "earnings_quality_soft_asset_share_quarterly",
  "what_changed": "Soft-asset share, (assets - property_plant_and_equipment - cash) / assets, for quarters-back-0 is 0.7532543117757928. Printed change against quarters-back-1: 0.018216273529990112; against quarters-back-4: -0.017193473364804146. The two printed changes have opposite signs, so no single direction is recorded. Position: third lowest of the 6 filled quarters, i.e. inside its history. Inputs as printed: Assets 6039449000.0, CashAndCashEquivalentsAtCarryingValue 1045126000.0 and PropertyPlantAndEquipmentAndFinanceLeaseRightOfUseAssetAfterAccumulatedDepreciationAndAmortization 445082000.0, all from 0001628280-26-040767.",
  "account": "Total assets less cash and PP&E",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-05-02, against the prior quarter and the year-ago quarter",
  "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
  "paragraph_id": "0001628280-26-040767:trends:soft_asset_share:2026-02-01..2026-05-02" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly_insufficient",
  "what_changed": "insufficient. Accruals over total assets cannot be filled for quarters-back-0: the record holds no operating cash flow for the three-month period, and the cell prints no value, no change and no position. Operating cash flow exists only for six months (release: 487,347 against 260,669, thousands). A three-month figure does not exist in my input, and I do not derive one. In the quarters the table holds, this ratio is filled only for quarters-back-1 and quarters-back-5 (7 filled periods in all, counting the 5 years).",
  "account": "Net income; net cash provided by operating activities; total assets",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-05-02",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-02-01..2026-05-02: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0001628280-26-040767:trends:accruals_over_total_assets:2026-02-01..2026-05-02" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly_history_too_short",
  "what_changed": "insufficient for a quarterly trend. The latest quarter that holds an accruals value is quarters-back-1 (2025-11-02..2026-01-31), at -0.013129206825313936, with a printed change of -0.002515167676590345 against quarters-back-5. No quarter-over-quarter change is printed because quarters-back-2 is not filled. Its position is lowest of only 2 filled quarters, and two points of history do not support a trend claim.",
  "account": "Net income; net cash provided by operating activities; total assets",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-01-31, against the year-ago quarter",
  "quote": "\"position_in_history\": \"lowest of the 2 filled quarters\"",
  "paragraph_id": "0001628280-26-040767:trends:accruals_over_total_assets:2025-11-02..2026-01-31" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly_insufficient",
  "what_changed": "insufficient. The non-GAAP gap cannot be filled for quarters-back-0 because companyfacts carries no non-GAAP measure. The cell prints no value, change or position, and the coverage block shows the ratio filled in 0 periods. The release (Appendix A) prints GAAP net income of 218,220 and adjusted (non-GAAP) net income of 240,199 (thousands) for the quarter. No gap figure exists in my input, and I do not compute one. The same appendix adds a holdback-arrangement adjustment of 2,411 that has no year-ago amount (printed as —). The release states the non-GAAP tax rate was 20% for this quarter against 22% for the year-ago quarter.",
  "account": "GAAP net income against adjusted (non-GAAP) net income",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-05-02",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001628280-26-040767:trends:non_gaap_gap:2026-02-01..2026-05-02" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly_insufficient",
  "what_changed": "insufficient. The warranty reserve ratio cannot be filled for quarters-back-0, and the cell prints no value, change or position; the coverage block shows it filled in 0 periods. The table searched only StandardProductWarrantyAccrual, ProductWarrantyAccrual and StandardProductWarrantyAccrualCurrent. The filings in my input do tag the accrual balance, under ProductWarrantyAccrualClassifiedCurrent: 60356000 at 2026-05-02 (see structure_and_disclosure_changes_warranty_accrual_tagged_outside_searched_concepts). So the input exists but the ratio does not, and I do not compute it.",
  "account": "Product warranty accrual",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-05-02",
  "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001628280-26-040767:trends:warranty_reserve_ratio:2026-02-01..2026-05-02" }
```

### Trend table — years-back-0 (fiscal year 2024-11-03..2025-11-01)

```json
{ "id": "earnings_quality_accruals_over_total_assets_annual",
  "what_changed": "Accruals over total assets, (net_income - operating_cash_flow) / assets, for years-back-0 is -0.11641837464940465. Printed change against years-back-1: -0.04009320563361991. Position: lowest of the 5 filled years. Inputs as printed: NetIncomeLoss 123338000.0 and NetCashProvidedByUsedInOperatingActivities 806093000.0 from 0001628280-25-056698, and Assets 5864667000.0 from 0001628280-26-040767.",
  "account": "Net income; net cash provided by operating activities; total assets",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2025-11-01, against the prior fiscal year",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-040767:trends:accruals_over_total_assets:2024-11-03..2025-11-01" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual",
  "what_changed": "Bad-debt reserve ratio for years-back-0 is 0.011358893206952308. Printed change against years-back-1: 0.0006019553631086399. Position: second lowest of the 5 filled years. Inputs as printed: AllowanceForDoubtfulAccountsReceivableCurrent 11212000.0 from 0001628280-25-056698 and AccountsReceivableNetCurrent 975856000.0 from 0001628280-26-040767. The 10-K tags a fiscal-2025 provision for doubtful accounts of 4226000 (7996000 for fiscal 2024) and write-offs of 2894000 (9770000 for fiscal 2024).",
  "account": "Allowance for doubtful accounts; accounts receivable, net",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2025-11-01, against the prior fiscal year",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-040767:trends:bad_debt_reserve_ratio:2024-11-03..2025-11-01" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual",
  "what_changed": "Current contract liabilities over annual revenue for years-back-0 is 0.043806624038920584. Printed change against years-back-1: 0.004857495094760564. Position: highest of the 5 filled years. Inputs as printed: ContractWithCustomerLiabilityCurrent 208936000.0 from 0001628280-26-040767 and Revenues 4769507000.0 from 0001628280-25-056698. The annual denominator is a full year of revenue, so this value is not on the same scale as the quarterly cells.",
  "account": "Contract liabilities (current deferred revenue); revenue",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2025-11-01, against the prior fiscal year",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-040767:trends:contract_liabilities_over_revenue:2024-11-03..2025-11-01" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_annual",
  "what_changed": "Days sales of inventory for years-back-0 is 108.78630827717673. Printed change against years-back-1: -23.81984804218861. Position: second lowest of the 5 filled years. Inputs as printed: InventoryNet 826235000.0 from 0001628280-26-040767 and CostOfGoodsAndServicesSold 2764590000.0 from 0001628280-25-056698; the period is 364 days.",
  "account": "Inventories, net; cost of goods sold",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2025-11-01, against the prior fiscal year",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-040767:trends:days_sales_of_inventory:2024-11-03..2025-11-01" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual",
  "what_changed": "Days sales outstanding for years-back-0 is 74.4755346831444. Printed change against years-back-1: -9.482937329617883. Position: lowest of the 5 filled years. Inputs as printed: AccountsReceivableNetCurrent 975856000.0 from 0001628280-26-040767 and Revenues 4769507000.0 from 0001628280-25-056698.",
  "account": "Accounts receivable, net; revenue",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2025-11-01, against the prior fiscal year",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-040767:trends:days_sales_outstanding:2024-11-03..2025-11-01" }
```

```json
{ "id": "earnings_quality_gross_margin_annual",
  "what_changed": "Gross margin for years-back-0 is 0.42036147551518427. Printed change against years-back-1: -0.007934732038823167. Position: lowest of the 5 filled years. Inputs as printed: Revenues 4769507000.0 and CostOfGoodsAndServicesSold 2764590000.0, both from 0001628280-25-056698.",
  "account": "Revenue; cost of goods sold",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2025-11-01, against the prior fiscal year",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-040767:trends:gross_margin:2024-11-03..2025-11-01" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_annual",
  "what_changed": "Inventory reserve ratio for years-back-0 is 0.1566237208542364. Printed change against years-back-1: 0.025993441610425216. Position: highest of the 5 filled years. Inputs as printed: InventoryValuationReserves 129408000.0 and InventoryNet 826235000.0, both from 0001628280-26-040767.",
  "account": "Inventory valuation reserves; inventories, net",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2025-11-01, against the prior fiscal year",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-040767:trends:inventory_reserve_ratio:2024-11-03..2025-11-01" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual",
  "what_changed": "Receivables over annual revenue for years-back-0 is 0.20460311726138572. Printed change against years-back-1: -0.021700041802663578. Position: lowest of the 5 filled years. Inputs as printed: AccountsReceivableNetCurrent 975856000.0 from 0001628280-26-040767 and Revenues 4769507000.0 from 0001628280-25-056698.",
  "account": "Accounts receivable, net; revenue",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2025-11-01, against the prior fiscal year",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-040767:trends:receivables_over_revenue:2024-11-03..2025-11-01" }
```

```json
{ "id": "earnings_quality_soft_asset_share_annual",
  "what_changed": "Soft-asset share for years-back-0 is 0.7478576362477187. Printed change against years-back-1: -0.026560201225915625. Position: second lowest of the 5 filled years. Inputs as printed: Assets 5864667000.0, CashAndCashEquivalentsAtCarryingValue 1091952000.0 and PropertyPlantAndEquipmentAndFinanceLeaseRightOfUseAssetAfterAccumulatedDepreciationAndAmortization 386779000.0, all from 0001628280-26-040767.",
  "account": "Total assets less cash and PP&E",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2025-11-01, against the prior fiscal year",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-040767:trends:soft_asset_share:2024-11-03..2025-11-01" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual_insufficient",
  "what_changed": "insufficient. The non-GAAP gap cannot be filled for years-back-0 because companyfacts carries no non-GAAP measure. The cell prints no value, change or position, and no year of the table holds it.",
  "account": "GAAP net income against adjusted (non-GAAP) net income",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2025-11-01",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001628280-26-040767:trends:non_gaap_gap:2024-11-03..2025-11-01" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_annual_insufficient",
  "what_changed": "insufficient. The warranty reserve ratio cannot be filled for years-back-0. The cell prints no value, change or position, and no year of the table holds it, because the table searched only three warranty-accrual concepts. The 10-K tags the year-end accrual under ProductWarrantyAccrualClassifiedCurrent, at 55533000 at 2025-11-01 and 55267000 at 2024-11-02. The input exists but the ratio does not, and I do not compute it.",
  "account": "Product warranty accrual",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2025-11-01",
  "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001628280-26-040767:trends:warranty_reserve_ratio:2024-11-03..2025-11-01" }
```

### Change of tag

```json
{ "id": "structure_and_disclosure_changes_allowance_concept_differs_between_quarterly_and_annual_cells",
  "what_changed": "The bad-debt reserve ratio rests on two different concepts, depending on the period type. Every filled annual cell takes bad_debt_allowance from us-gaap AllowanceForDoubtfulAccountsReceivableCurrent (years-back-0: 11212000.0). Every filled quarterly cell takes it from AllowanceForDoubtfulAccountsReceivable (quarters-back-0: 11000000.0). Neither series changes concept within itself, and no printed change compares across the two. Python prints no explicit tag-change flag here; this is the printed tag of each input as it stands.",
  "account": "Allowance for doubtful accounts",
  "expected_direction": "none",
  "horizon": "all filled quarters and years of the trend table",
  "quote": "\"id\": \"0001628280-25-056698:facts:AllowanceForDoubtfulAccountsReceivableCurrent:2025-11-01\"",
  "paragraph_id": "0001628280-26-040767:trends:bad_debt_reserve_ratio:2024-11-03..2025-11-01" }
```

```json
{ "id": "structure_and_disclosure_changes_warranty_accrual_tagged_outside_searched_concepts",
  "what_changed": "The warranty accrual balance is tagged under us-gaap ProductWarrantyAccrualClassifiedCurrent. That is not one of the three concepts the trend table searched, so every warranty reserve ratio cell is empty even though the balance exists. Printed balances: 60356000 at 2026-05-02 (this 10-Q); 58084000 at 2026-01-31 (Q1 10-Q); 55533000 at 2025-11-01 (10-K and both 10-Qs agree); 52313000 at 2025-05-03; 55267000 at 2024-11-02. The 10-K also tags 57089000 and 45503000 at earlier balance dates. The balance has risen at each of the last three printed dates. The ratio itself does not exist in my input, and I do not compute it.",
  "account": "Product warranty accrual",
  "expected_direction": "up",
  "horizon": "balances at 2025-11-01, 2026-01-31 and 2026-05-02",
  "quote": "\"value\": \"60356000\"",
  "paragraph_id": "0001628280-26-040767:facts:ProductWarrantyAccrualClassifiedCurrent:2026-05-02" }
```

### Numeric facts

```json
{ "id": "earnings_quality_research_and_development_capitalized_baseline",
  "what_changed": "The trend table's R&D-capitalized baseline (5-year life) for years-back-0 prints:\n- earnings_with_rnd_capitalized 329813800.0, against reported net income 123338000.0;\n- a research_and_development_asset of 2269857600.0;\n- research_and_development_amortization of 641853200.0;\n- book_value_with_rnd_capitalized 4999180600.0, against stockholders_equity 2729323000.0.\nFor years-back-1 it prints earnings_with_rnd_capitalized 253471400.0. The baseline block prints no paragraph_id of its own, so this item quotes the fiscal-2025 R&D expense fact it is built on. capitalized_development_cost and capitalized_over_expense do not exist: companyfacts tags no CapitalizedComputerSoftwareAdditions in any period. The share of development cost the company capitalises is therefore insufficient.",
  "account": "Research and development expense",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2025-11-01, with the four years before it",
  "quote": "\"value\": \"848329000\"",
  "paragraph_id": "0001628280-25-056698:facts:ResearchAndDevelopmentExpense:2024-11-03..2025-11-01" }
```

```json
{ "id": "estimates_and_discretion_warranty_expense_tagged_annual",
  "what_changed": "The 10-K tags warranty expense (ProductWarrantyExpense) of 24442000 for fiscal 2025, 25643000 for fiscal 2024 and 31742000 for fiscal 2023. Warranty settlements (ProductWarrantyAccrualPayments) are 24176000, 27465000 and 20156000 for the same years. Fiscal 2025 expense is lower than fiscal 2024, which is lower than fiscal 2023.",
  "account": "Product warranty expense",
  "expected_direction": "down",
  "horizon": "fiscal years ended 2023-10-28 through 2025-11-01",
  "quote": "\"value\": \"24442000\"",
  "paragraph_id": "0001628280-25-056698:facts:ProductWarrantyExpense:2024-11-03..2025-11-01" }
```

```json
{ "id": "estimates_and_discretion_warranty_provision_year_to_date",
  "what_changed": "This 10-Q tags six-month warranty expense of 16685000, against 10714000 for the year-ago six months. The Q1 10-Q tagged 8185000 for the first quarter, against 5697000 a year earlier. Six-month warranty settlements are 11862000, against 13668000 a year earlier. Provisions are above settlements this year and below them a year earlier, and the accrual balance rose. The release prints the same provision for warranty of 16,685 against 10,714 (thousands). No three-month provision for the quarter ended 2026-05-02 exists in my input.",
  "account": "Product warranty expense and settlements",
  "expected_direction": "up",
  "horizon": "six months ended 2026-05-02, against the six months ended 2025-05-03",
  "quote": "\"value\": \"16685000\"",
  "paragraph_id": "0001628280-26-040767:facts:ProductWarrantyExpense:2025-11-02..2026-05-02" }
```

```json
{ "id": "estimates_and_discretion_finite_lived_intangible_impairment",
  "what_changed": "The 10-K tags an impairment of finite-lived intangible assets of 89100000 for fiscal 2025, against 0 for fiscal 2024 and 0 for fiscal 2023. The same filing tags in-process research and development within finite-lived intangibles at a gross 89100000 at 2024-11-02 and 86000000 at 2025-11-01. The 86000000 matches the in-process technology the filing tags as acquired with Nubis Communications on 2025-10-07. RestructuringCostsAndAssetImpairmentCharges is tagged at 112113000 for fiscal 2025, against 24592000 for fiscal 2024 and 23834000 for fiscal 2023. This 10-Q prints other intangible assets, net of 202190000 at 2026-05-02 against 224210000 at 2025-11-01.",
  "account": "Finite-lived intangible assets (in-process R&D); restructuring costs and asset impairment charges",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2025-11-01, against the two prior fiscal years",
  "quote": "\"value\": \"89100000\"",
  "paragraph_id": "0001628280-25-056698:facts:ImpairmentOfIntangibleAssetsFinitelived:2024-11-03..2025-11-01" }
```

```json
{ "id": "estimates_and_discretion_inventory_write_down_annual",
  "what_changed": "The 10-K tags inventory write-downs (InventoryWriteDown) of 48424000 for fiscal 2025, against 77341000 for fiscal 2024 and 29464000 for fiscal 2023. The same paragraph_id also carries a rounded fact of 48400000 (decimals -5) in the same filing. In the same fiscal year, the trend table puts the inventory reserve ratio at the highest of its 5 filled years.",
  "account": "Inventory write-down / provision for excess and obsolescence",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2025-11-01, against the prior fiscal year",
  "quote": "\"value\": \"48424000\"",
  "paragraph_id": "0001628280-25-056698:facts:InventoryWriteDown:2024-11-03..2025-11-01" }
```

```json
{ "id": "estimates_and_discretion_inventory_write_down_year_to_date",
  "what_changed": "This 10-Q tags six-month inventory write-downs of 42500000 (decimals -5). The same paragraph_id also carries 42481000, the cash-flow figure; the two differ only in rounding. The year-ago six months show 23431000. The Q1 10-Q tagged 21832000 (rounded 21800000) for the first quarter, against 10918000 a year earlier. The release prints the provision for inventory excess and obsolescence at 42,481 against 23,431 (thousands). Both the year-to-date provision and the first-quarter provision are above their year-ago amounts. No three-month figure for the quarter ended 2026-05-02 exists in my input.",
  "account": "Inventory write-down / provision for excess and obsolescence",
  "expected_direction": "up",
  "horizon": "six months ended 2026-05-02, against the six months ended 2025-05-03",
  "quote": "\"value\": \"42500000\"",
  "paragraph_id": "0001628280-26-040767:facts:InventoryWriteDown:2025-11-02..2026-05-02" }
```

```json
{ "id": "estimates_and_discretion_inventory_valuation_reserve_balance",
  "what_changed": "Inventory valuation reserves are 156735000 at 2026-05-02, 145943000 at 2026-01-31 (Q1 10-Q) and 129408000 at 2025-11-01. The reserve rose at each date. Over the same span:\n- gross inventory: 965182000 against 955643000;\n- net inventory: 808447000 against 826235000.\nComponents at 2026-05-02 against 2025-11-01:\n- raw materials: 546457000 against 593783000;\n- work in process: 40187000 against 35051000;\n- finished goods: 334488000 against 286050000;\n- other capitalized inventory costs: 44050000 against 40759000.",
  "account": "Inventory valuation reserves; inventory components",
  "expected_direction": "up",
  "horizon": "balances at 2025-11-01, 2026-01-31 and 2026-05-02",
  "quote": "\"value\": \"156735000\"",
  "paragraph_id": "0001628280-26-040767:facts:InventoryValuationReserves:2026-05-02" }
```

```json
{ "id": "revenue_recognition_receivables_factoring_disclosed",
  "what_changed": "The 10-K tags a fair-value disclosure for factoring receivables (cien FactoringReceivablesMember) of:\n- 1000000 at 2025-11-01;\n- 18100000 at 2024-11-02;\n- 60300000 at 2023-10-28.\nIt tags interest expense attributable to factoring of 3800000 for fiscal 2025, 900000 for fiscal 2024 and 1200000 for fiscal 2023. The trend table's receivables ratios and DSO use AccountsReceivableNetCurrent alone and print no adjustment for receivables factored. I found no factoring fact for 2026-01-31 or 2026-05-02 in the two 10-Qs in my input.",
  "account": "Accounts receivable sold under factoring arrangements",
  "expected_direction": "down",
  "horizon": "fiscal years ended 2023-10-28 through 2025-11-01",
  "quote": "\"value\": \"1000000\"",
  "paragraph_id": "0001628280-25-056698:facts:ReceivablesFairValueDisclosure:2025-11-01:us-gaap:AccountsNotesLoansAndFinancingReceivableByReceivableTypeAxis=cien:FactoringReceivablesMember" }
```

```json
{ "id": "earnings_quality_nubis_holdback_contingent_compensation",
  "what_changed": "The 10-K tags a contingent-compensation amount of 28900000 for the Nubis Communications acquisition (2025-10-07), alongside consideration transferred of 270500000 and cash paid of 232600000. For this quarter, the release excludes a holdback arrangement of 2,411 (thousands) from adjusted operating expense and adjusted EBITDA. It describes this as a one-time holdback of Nubis merger consideration, treated as contingent compensation for GAAP; the year-ago column prints —. My input does not print how much of the 28900000 remains to be expensed.",
  "account": "Contingent compensation (acquisition holdback); adjusted operating expense",
  "expected_direction": "none",
  "horizon": "quarters following the 2025-10-07 acquisition",
  "quote": "\"value\": \"28900000\"",
  "paragraph_id": "0001628280-25-056698:facts:BusinessCombinationContingentConsiderationLiability:2025-10-07:us-gaap:BusinessAcquisitionAxis=cien:NubisCommunicationsMember,us-gaap:ContingentConsiderationByTypeAxis=cien:ContingentCompensationMember" }
```

```json
{ "id": "revenue_recognition_remaining_performance_obligations_balance",
  "what_changed": "Remaining performance obligations (RevenueRemainingPerformanceObligation) are:\n- 2500000000 at 2026-05-02 (this 10-Q);\n- 2300000000 at 2026-01-31 (Q1 10-Q, with 0.85 expected within twelve months);\n- 2100000000 at 2025-11-01 (10-K, with 0.83 expected within twelve months).\nThe balance rose at each date. My input holds no twelve-month share for 2026-05-02. These facts are rounded to hundreds of millions (decimals -8).",
  "account": "Remaining performance obligations",
  "expected_direction": "up",
  "horizon": "balances at 2025-11-01, 2026-01-31 and 2026-05-02",
  "quote": "\"value\": \"2500000000\"",
  "paragraph_id": "0001628280-26-040767:facts:RevenueRemainingPerformanceObligation:2026-05-02" }
```

```json
{ "id": "revenue_recognition_contract_liability_balance_current_and_noncurrent",
  "what_changed": "Total contract liabilities (ContractWithCustomerLiability) are 340487000 at 2026-05-02. That is above the 303786000 at 2025-11-01 and below the 390873000 at 2026-01-31 (Q1 10-Q).\n- Current: 238380000 at 2026-05-02, against 208936000 at year-end and 290418000 at 2026-01-31.\n- Noncurrent: 102107000, against 94850000 at year-end.\n- Revenue recognized from the opening balance: 149600000 for the six months, against 111300000 a year earlier; the Q1 10-Q tagged 88200000 for the first quarter.\nThe balance is up against year-end and down against the prior quarter, so no single direction is recorded.",
  "account": "Contract liabilities (deferred revenue)",
  "expected_direction": "none",
  "horizon": "balances at 2025-11-01, 2026-01-31 and 2026-05-02; six months ended 2026-05-02",
  "quote": "\"value\": \"340487000\"",
  "paragraph_id": "0001628280-26-040767:facts:ContractWithCustomerLiability:2026-05-02" }
```

```json
{ "id": "revenue_recognition_product_deferred_revenue_drawn_down",
  "what_changed": "Within contract liabilities, the product portion is 31649000 at 2026-05-02, against 65382000 at 2025-11-01. The service portion is 308838000, against 238404000. Product deferred revenue fell while service deferred revenue rose. The product figure here is a balance; no product revenue recognized out of it is tagged separately in my input.",
  "account": "Contract liabilities — product",
  "expected_direction": "down",
  "horizon": "balance at 2026-05-02, against 2025-11-01",
  "quote": "\"value\": \"31649000\"",
  "paragraph_id": "0001628280-26-040767:facts:ContractWithCustomerLiability:2026-05-02:srt:ProductOrServiceAxis=us-gaap:ProductMember" }
```

```json
{ "id": "revenue_recognition_contract_assets_balance",
  "what_changed": "Contract assets (ContractWithCustomerAssetNet) are 163614000 at 2026-05-02, against 157868000 at 2025-11-01.",
  "account": "Contract assets (unbilled receivables)",
  "expected_direction": "up",
  "horizon": "balance at 2026-05-02, against 2025-11-01",
  "quote": "\"value\": \"163614000\"",
  "paragraph_id": "0001628280-26-040767:facts:ContractWithCustomerAssetNet:2026-05-02" }
```

```json
{ "id": "revenue_recognition_capitalized_contract_costs_balance",
  "what_changed": "Capitalized contract costs (CapitalizedContractCostNet) are 35500000 at 2026-05-02, against 37400000 at 2025-11-01. Their amortization is 19700000 for the six months, against 16700000 a year earlier.",
  "account": "Capitalized costs to obtain contracts",
  "expected_direction": "down",
  "horizon": "balance at 2026-05-02, against 2025-11-01; six months ended 2026-05-02",
  "quote": "\"value\": \"35500000\"",
  "paragraph_id": "0001628280-26-040767:facts:CapitalizedContractCostNet:2026-05-02" }
```

```json
{ "id": "revenue_recognition_cloud_provider_a_revenue_concentration",
  "what_changed": "Revenue from Cloud Provider A is tagged at:\n- 321224000 for the quarter, against 151345000 for the year-ago quarter;\n- 652206000 for the six months, against 320242000;\n- 330981000 for the first quarter (Q1 10-Q), against 168896000.\nTotal revenue for the quarter is 1570739000. Revenue from this customer in the quarter was slightly below its first-quarter level and above the year-ago quarter.",
  "account": "Revenue — largest customer",
  "expected_direction": "up",
  "horizon": "quarter and six months ended 2026-05-02, against the year-ago periods",
  "quote": "\"value\": \"321224000\"",
  "paragraph_id": "0001628280-26-040767:facts:Revenues:2026-02-01..2026-05-02:srt:MajorCustomersAxis=cien:CloudProviderAMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:SalesRevenueNetMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember" }
```

```json
{ "id": "structure_and_disclosure_changes_ten_percent_customer_set_changed",
  "what_changed": "The set of named 10%-plus customers differs between the current and year-ago columns of this 10-Q.\n- Cloud Provider B is tagged for current periods only: 212288000 for the quarter and 372493000 for the six months. My input has no year-ago Cloud Provider B fact.\n- Service Provider A is tagged for year-ago periods only: 117355000 for the quarter and 228379000 for the six months. There is no current-period Service Provider A fact.\n- Concentration totals: 533512000 for the quarter against 268700000; 1024699000 for the six months against 548621000.\nThe release says two customers represented 10%-plus of revenue, for a total of 34.0% of revenue.",
  "account": "Revenue — customers above 10% of revenue",
  "expected_direction": "up",
  "horizon": "quarter and six months ended 2026-05-02, against the year-ago periods",
  "quote": "\"value\": \"212288000\"",
  "paragraph_id": "0001628280-26-040767:facts:Revenues:2026-02-01..2026-05-02:srt:MajorCustomersAxis=cien:CloudProviderBMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:SalesRevenueNetMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_blue_planet_segment_loss",
  "what_changed": "The Blue Planet Automation Software and Services segment profit (tagged NetIncomeLoss on the operating-segment axis) is -2842000 for the quarter, against 6477000 for the year-ago quarter. For the six months it is -6657000, against 12976000.\n- Segment revenue: 23361000 against 27951000 for the quarter; 43781000 against 53982000 for the six months.\n- Segment gross profit: 7386000 against 15393000 for the quarter; 12962000 against 30182000 for the six months.\n- Segment R&D: 10228000 against 8916000 for the quarter.\nGoodwill allocated to the segment is 89049000 at both 2026-05-02 and 2025-11-01. It is the only segment of four whose revenue and profit fell.",
  "account": "Segment profit, revenue and gross profit — Blue Planet; goodwill allocated to the segment",
  "expected_direction": "down",
  "horizon": "quarter and six months ended 2026-05-02, against the year-ago periods",
  "quote": "\"value\": \"-2842000\"",
  "paragraph_id": "0001628280-26-040767:facts:NetIncomeLoss:2026-02-01..2026-05-02:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=cien:BluePlanetAutomationSoftwareandServicesSegmentMember" }
```

```json
{ "id": "earnings_quality_networking_platforms_segment_profit",
  "what_changed": "Networking Platforms segment profit is 361551000 for the quarter, against 151422000 for the year-ago quarter, and 678182000 for the six months, against 333584000. Segment revenue is 1274078000 against 866315000, and segment gross profit 551054000 against 321098000, for the quarter. Other segments for the quarter:\n- Platform Software and Services: profit 62444000 against 52995000; revenue 93878000 against 85441000.\n- Global Services: profit 64383000 against 52342000; revenue 179422000 against 146171000.\nTotal segment profit is 485536000 against 263236000 for the quarter.",
  "account": "Segment profit and revenue",
  "expected_direction": "up",
  "horizon": "quarter and six months ended 2026-05-02, against the year-ago periods",
  "quote": "\"value\": \"361551000\"",
  "paragraph_id": "0001628280-26-040767:facts:NetIncomeLoss:2026-02-01..2026-05-02:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=cien:NetworkingPlatformsSegmentMember" }
```

```json
{ "id": "earnings_quality_share_based_compensation_expense_rising",
  "what_changed": "Share-based compensation (ShareBasedCompensation) is 55473000 for the quarter, against 47960000 for the year-ago quarter, and 105300000 for the six months, against 88767000. Unrecognized RSU compensation cost is 394800000 at 2026-05-02. For the year-ago quarter, release Appendix B adds back 48,024 (thousands), while this 10-Q tags 47960000 for the same quarter. The 10-Q also tags a capitalized share-based compensation amount of -64000 for that quarter. The two prior-year figures in my input differ, and I do not reconcile them.",
  "account": "Share-based compensation expense",
  "expected_direction": "up",
  "horizon": "quarter and six months ended 2026-05-02, against the year-ago periods",
  "quote": "\"value\": \"55473000\"",
  "paragraph_id": "0001628280-26-040767:facts:ShareBasedCompensation:2026-02-01..2026-05-02" }
```

```json
{ "id": "estimates_and_discretion_restructuring_reserve_run_off",
  "what_changed": "The restructuring reserve is 755000 at 2026-05-02, against 8436000 at 2025-11-01. Six-month restructuring charges are 2303000 (3492000 a year earlier), and payments are 9984000 (4743000 a year earlier). A year earlier the reserve went from 1927000 at 2024-11-02 to 676000 at 2025-05-03. The release prints significant asset impairments and restructuring costs of 805 against 1,948 (thousands) for the quarter.",
  "account": "Restructuring reserve; restructuring charges",
  "expected_direction": "down",
  "horizon": "balance at 2026-05-02, against 2025-11-01; six months ended 2026-05-02",
  "quote": "\"value\": \"755000\"",
  "paragraph_id": "0001628280-26-040767:facts:RestructuringReserve:2026-05-02" }
```

```json
{ "id": "estimates_and_discretion_accrued_compensation_balance",
  "what_changed": "Accrued salaries (AccruedSalariesCurrent) are 172568000 at 2026-05-02, against 281542000 at 2025-11-01 and 152223000 at 2026-01-31 (Q1 10-Q). Total accrued liabilities are 439626000, against 531081000 at year-end and 395881000 at 2026-01-31. Other accrued liabilities are 152279000, against 132413000. Accrued income taxes are 659000, against 10729000. The balances are down against year-end and up against the prior quarter, so no single direction is recorded.",
  "account": "Accrued compensation; accrued liabilities",
  "expected_direction": "none",
  "horizon": "balances at 2025-11-01, 2026-01-31 and 2026-05-02",
  "quote": "\"value\": \"172568000\"",
  "paragraph_id": "0001628280-26-040767:facts:AccruedSalariesCurrent:2026-05-02" }
```

```json
{ "id": "estimates_and_discretion_effective_tax_rate_annual",
  "what_changed": "The 10-K tags an effective tax rate of 0.2108 for fiscal 2025, against 0.2995 for fiscal 2024 and 0.2127 for fiscal 2023.\n- Valuation allowance: 214456000 at 2025-11-01, against 192447000 at 2024-11-02.\n- Change in valuation allowance, as a rate-reconciliation item: 0.1408 for fiscal 2025, against 0.0215 for fiscal 2024.\n- Domestic pre-tax income: -22804000 for fiscal 2025.\nFor this quarter, the release prints a GAAP provision for income taxes of 12,840 against 10,047 (thousands), and a non-GAAP rate of 20% against 22%. I do not compute a GAAP quarterly rate.",
  "account": "Income tax expense; deferred tax valuation allowance",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2025-11-01, against the prior fiscal year",
  "quote": "\"value\": \"0.2108\"",
  "paragraph_id": "0001628280-25-056698:facts:EffectiveIncomeTaxRateContinuingOperations:2024-11-03..2025-11-01" }
```

```json
{ "id": "estimates_and_discretion_unrecognized_tax_benefit_statute_lapse",
  "what_changed": "The 10-K tags a reduction in unrecognized tax benefits from statute-of-limitations lapses of 21596000 for fiscal 2025, against 116000 for fiscal 2024. Unrecognized tax benefits are 95685000 at 2025-11-01, against 105281000 at 2024-11-02.",
  "account": "Unrecognized tax benefits",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2025-11-01, against the prior fiscal year",
  "quote": "\"value\": \"21596000\"",
  "paragraph_id": "0001628280-25-056698:facts:UnrecognizedTaxBenefitsReductionsResultingFromLapseOfApplicableStatuteOfLimitations:2024-11-03..2025-11-01" }
```

```json
{ "id": "liquidity_and_capital_purchase_obligations_balance",
  "what_changed": "Purchase obligations (PurchaseObligation) are:\n- 2800000000 at 2026-05-02 (this 10-Q);\n- 1900000000 at 2026-01-31 (Q1 10-Q);\n- 2100000000 at 2025-11-01 (10-K).\nThe latest balance is the highest of the three printed. All three facts are rounded to hundreds of millions.",
  "account": "Purchase obligations (off-balance-sheet commitments)",
  "expected_direction": "up",
  "horizon": "balances at 2025-11-01, 2026-01-31 and 2026-05-02",
  "quote": "\"value\": \"2800000000\"",
  "paragraph_id": "0001628280-26-040767:facts:PurchaseObligation:2026-05-02" }
```

```json
{ "id": "liquidity_and_capital_operating_cash_flow_year_to_date",
  "what_changed": "The release cash-flow statement prints:\n- net cash provided by operating activities: 487,347 for the six months, against 260,669 a year earlier;\n- payments for equipment, furniture and fixtures: 114,933 against 55,622;\n- change in accounts receivable: (71,555) against (20,857);\n- change in deferred revenue: 35,442 against 66,493 (all thousands).\nNo three-month cash-flow figure exists in my input.",
  "account": "Operating cash flow; capital expenditure",
  "expected_direction": "up",
  "horizon": "six months ended 2026-05-02, against the six months ended 2025-05-03",
  "quote": "Net cash provided by operating activities | 487,347",
  "paragraph_id": "0001628280-26-040614:8k_2_02:67" }
```

```json
{ "id": "liquidity_and_capital_share_repurchase_authorization_remaining",
  "what_changed": "The remaining repurchase authorization is:\n- 506700000 at 2026-05-02;\n- 589800000 at 2026-01-31 (Q1 10-Q);\n- 638600000 at 2025-12-05 (10-K subsequent event).\nSix-month repurchases are 600000 shares for 163700000. Treasury stock at 2026-05-02 is 4500000 shares at 493300000, with an average cost per share of 108.43. The release says approximately 0.2 million shares were repurchased in the quarter, for $83.1 million.",
  "account": "Share repurchase program",
  "expected_direction": "down",
  "horizon": "balances at 2025-12-05, 2026-01-31 and 2026-05-02",
  "quote": "\"value\": \"506700000\"",
  "paragraph_id": "0001628280-26-040767:facts:StockRepurchaseProgramRemainingAuthorizedRepurchaseAmount1:2026-05-02" }
```

```json
{ "id": "liquidity_and_capital_tax_withholding_on_vested_awards",
  "what_changed": "Payments related to tax withholding for share-based compensation are 179400000 for the six months. The release cash-flow statement prints 179,420 against 42,266 (thousands) for the year-ago six months. In the release, these payments are larger than repurchases under the program for the same six months (164,920).",
  "account": "Cash paid for tax withholding on vested stock awards",
  "expected_direction": "up",
  "horizon": "six months ended 2026-05-02, against the six months ended 2025-05-03",
  "quote": "\"value\": \"179400000\"",
  "paragraph_id": "0001628280-26-040767:facts:PaymentsRelatedToTaxWithholdingForShareBasedCompensation:2025-11-02..2026-05-02" }
```

```json
{ "id": "liquidity_and_capital_long_term_investments_maturing_within_five_years",
  "what_changed": "Available-for-sale debt securities maturing after one year through five years have a fair value of 200106000 at 2026-05-02; the noncurrent marketable securities line was 57142000 at 2025-11-01. Total available-for-sale debt securities are 468377000, against 342828000. Securities maturing within one year are 268271000 at fair value. Cash and cash equivalents are 1045126000 at 2026-05-02, against 1091952000 at 2025-11-01.",
  "account": "Investments; cash and cash equivalents",
  "expected_direction": "up",
  "horizon": "balances at 2026-05-02, against 2025-11-01",
  "quote": "\"value\": \"200106000\"",
  "paragraph_id": "0001628280-26-040767:facts:AvailableForSaleSecuritiesDebtMaturitiesAfterOneThroughFiveYearsFairValue:2026-05-02" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_repurchases_after_quarter_end",
  "what_changed": "After the quarter ended, this 10-Q tags repurchases of 44628 shares for 25100000 between 2026-05-03 and 2026-05-29, leaving a remaining authorization of 481600000 at 2026-05-29. The Q1 10-Q tagged a remaining authorization of 564700000 at 2026-02-27 as a subsequent event. The 10-K tagged 162347 shares for 31700000 and a remaining 638600000 at 2025-12-05.",
  "account": "Share repurchase program — subsequent events",
  "expected_direction": "down",
  "horizon": "2026-05-03 through 2026-05-29",
  "quote": "\"value\": \"481600000\"",
  "paragraph_id": "0001628280-26-040767:facts:StockRepurchaseProgramRemainingAuthorizedRepurchaseAmount1:2026-05-29:us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

### Earnings release figures set against the table

```json
{ "id": "across_documents_release_dso_against_trend_table_dso",
  "what_changed": "The release states average DSO of 71 for the quarter. The trend table prints quarterly DSO of 60.98007307388433 for the same quarter (period-end receivables / quarterly revenue * 91), and annual DSO of 74.4755346831444 for fiscal 2025. The release calls its figure an average and does not print its formula. The two quarterly figures are built differently, and my input holds nothing that reconciles them. I do not reconcile them.",
  "account": "Days sales outstanding",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-05-02",
  "quote": "•Average days' sales outstanding (DSOs) were 71.",
  "paragraph_id": "0001628280-26-040614:8k_2_02:34" }
```

```json
{ "id": "across_documents_release_inventory_turns_against_trend_table_dsi",
  "what_changed": "The release states inventory turns of 3.6 for the quarter. The trend table prints days sales of inventory of 83.678266803915 for the same quarter, the lowest of its 6 filled quarters. The release does not print how turns are computed, and no turns figure exists in the table. I do not convert one into the other.",
  "account": "Inventory turns; days sales of inventory",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-05-02",
  "quote": "•Inventory turns were 3.6.",
  "paragraph_id": "0001628280-26-040614:8k_2_02:35" }
```

```json
{ "id": "results_against_expectations_full_year_revenue_guidance_raised",
  "what_changed": "The release raises fiscal 2026 revenue guidance to $6.3 billion plus or minus $100 million. It guides fiscal third-quarter revenue to $1.625 billion plus or minus $50 million, and full-year adjusted gross margin to between 44.5% and 45%. Six-month revenue is tagged at 2997781000. The guidance level before this raise does not exist in my input, so the size of the raise is the company's statement and not a figure I can check. My input holds no outside expectation figure.",
  "account": "Revenue guidance",
  "expected_direction": "up",
  "horizon": "fiscal year 2026, as the release labels it",
  "quote": "•Raising revenue guidance for fiscal year 2026 to $6.3 billion plus or minus $100 million, a 32% increase YoY at the midpoint",
  "paragraph_id": "0001628280-26-040614:8k_2_02:9" }
```

## Seen in the notes

No item is placed here. The instructions say each fact carries a marker for whether its element sat inside a note when it was extracted. No fact in input_numbers.json carries that marker. Every fact prints only these fields: id, paragraph_id, tag, prefix, namespace, context, context_ref, unit, decimals, value, number, nil, form, source_accession, filing_date and, on some facts, superseded_by.

Without the marker, I cannot route a fact here unless I judge where it sat myself, and the instructions say routing is not mine to judge. Every fact item above is therefore listed under the statements heading as received. That includes the ones that read like note-table figures:
- warranty accrual
- inventory reserves and components
- RPO
- contract liabilities by product and service
- customer concentration
- segment results
- restructuring reserve
- tax rate reconciliation
- purchase obligations
- repurchases

The missing marker looks like an extraction defect in this run's input, not a property of the filing.
