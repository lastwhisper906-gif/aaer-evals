# CIEN — numbers reader — 10-Q 0001628280-26-040767 (quarter ended 2026-05-02)

Inputs read in full: input_trends.json, input_numbers.json, input_8k.md (8-K 0001628280-26-040614, filed 2026-06-04), input_prior_predictions.md. None of them holds prices, abnormal returns, short interest, another company's files, a prior run's probability or an outcome window.

Notes that are not items:

- **Periods the record does not reach.** quarters-back-2 (target end 2025-11-01) and quarters-back-6 (target end 2024-11-02) have no cells. The reason each period gives is "no quarter ending within 20 days of 2025-11-01 [resp. 2024-11-02] is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py". My input holds no fourth-quarter derivation, so those two quarters do not exist for this report and I derive nothing. For the same reason, the quarters-back-1 cells print no quarter_over_quarter change (it would be against quarters-back-2), and the quarters-back-5 cells print none either (against quarters-back-6).
- **Articulation checks and restatement traces** are not in my input, so no articulation gap can be reported from them. In the numeric facts I found no concept and period that a later filing prints at a different value from an earlier filing, so no restated prior value is reported. The one change of tag my input shows (the bad-debt allowance) is reported below as two items.
- The years-back-0 `research_and_development_capitalized` block prints no paragraph_id. It cannot be quoted, so no item is written from it. Within the table itself, its capitalized_development_cost and capitalized_over_expense are missing, because no CapitalizedComputerSoftwareAdditions is tagged.
- **Prior flags:** none on record. input_prior_predictions.md states that this company has no earlier run.
- My input has no operating cash flow for the discrete fiscal second quarter: the 10-Q prints six months. I do not derive one.
- Which facts sat inside a note: see "Seen in the notes".

## Seen in the statements

### Trend table — quarters-back-0 (2026-02-01..2026-05-02)

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarterly_trend",
  "what_changed": "receivables_over_revenue in quarters-back-0 (2026-02-01..2026-05-02) is 0.670110693119608; quarter_over_quarter change against quarters-back-1 is -0.0078006787951638845; year_over_year change against quarters-back-4 is -0.15573278192831008. Inputs: receivables 1052569000.0 (AccountsReceivableNetCurrent, 2026-05-02), revenue 1570739000.0 (Revenues, 2026-02-01..2026-05-02). Position in the filed history: lowest of the 6 filled quarters.",
  "account": "accounts receivable, net, against quarterly revenue",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001628280-26-040767:trends:receivables_over_revenue:2026-02-01..2026-05-02" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly_trend",
  "what_changed": "days_sales_outstanding in quarters-back-0 is 60.98007307388433; quarter_over_quarter change against quarters-back-1 is -0.7098617703599146; year_over_year change against quarters-back-4 is -14.171683155476217. Inputs: receivables 1052569000.0, revenue 1570739000.0. Position: lowest of the 6 filled quarters.",
  "account": "accounts receivable, net (days sales outstanding)",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001628280-26-040767:trends:days_sales_outstanding:2026-02-01..2026-05-02" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_quarterly_trend",
  "what_changed": "days_sales_of_inventory in quarters-back-0 is 83.678266803915; quarter_over_quarter change against quarters-back-1 is -12.351402999284417; year_over_year change against quarters-back-4 is -34.53709335298505. Inputs: inventory 808447000.0 (InventoryNet, 2026-05-02), cost_of_revenue 879185000.0 (CostOfGoodsAndServicesSold). Position: lowest of the 6 filled quarters. Every quarter_over_quarter and year_over_year change the table prints for this ratio is negative (quarters-back-0, -1, -3, -4).",
  "account": "inventories, net (days sales of inventory)",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001628280-26-040767:trends:days_sales_of_inventory:2026-02-01..2026-05-02" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly_insufficient",
  "what_changed": "insufficient: accruals_over_total_assets cannot be filled in quarters-back-0 because the record holds no operating cash flow row for the discrete quarter 2026-02-01..2026-05-02 (the 10-Q prints operating cash flow for six months only); no quarter_over_quarter or year_over_year change is printed. Only 2 quarters of this ratio are filled in the whole table, which does not support a trend claim.",
  "account": "total accruals (net income less operating cash flow) over total assets",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-02-01..2026-05-02: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0001628280-26-040767:trends:accruals_over_total_assets:2026-02-01..2026-05-02" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly_trend",
  "what_changed": "gross_margin in quarters-back-0 is 0.44027301798707486; quarter_over_quarter change against quarters-back-1 is 0.0019397383779253263; year_over_year change against quarters-back-4 is 0.038064252916614305. Inputs: revenue 1570739000.0, cost_of_revenue 879185000.0 (CostOfGoodsAndServicesSold). Position: highest of the 6 filled quarters.",
  "account": "gross margin (Revenues, CostOfGoodsAndServicesSold)",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001628280-26-040767:trends:gross_margin:2026-02-01..2026-05-02" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly_trend",
  "what_changed": "bad_debt_reserve_ratio in quarters-back-0 is 0.010342535369120387; quarter_over_quarter change against quarters-back-1 is -0.001102292386221896; year_over_year change against quarters-back-4 is -8.744593141313782e-05. Inputs: bad_debt_allowance 11000000.0 (AllowanceForDoubtfulAccountsReceivable, 2026-05-02), receivables 1052569000.0. Position: third lowest of the 6 filled quarters.",
  "account": "allowance for doubtful accounts",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
  "paragraph_id": "0001628280-26-040767:trends:bad_debt_reserve_ratio:2026-02-01..2026-05-02" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly_trend",
  "what_changed": "inventory_reserve_ratio in quarters-back-0 is 0.19387170711252563; quarter_over_quarter change against quarters-back-1 is 0.021326150890952078; year_over_year change against quarters-back-4 is 0.05888658714583128. Inputs: inventory_reserve 156735000.0 (InventoryValuationReserves, 2026-05-02), inventory 808447000.0 (InventoryNet). Position: highest of the 6 filled quarters. Every quarter_over_quarter and year_over_year change the table prints for this ratio is positive (quarters-back-0, -1, -3, -4).",
  "account": "inventory valuation reserve (excess and obsolescence)",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001628280-26-040767:trends:inventory_reserve_ratio:2026-02-01..2026-05-02" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly_insufficient",
  "what_changed": "insufficient: warranty_reserve_ratio is not filled in quarters-back-0 (nor in any period of the table) because none of the three concepts its lookup searches is tagged in any period; no change is printed. The 10-Q does tag the warranty accrual, under ProductWarrantyAccrualClassifiedCurrent (see the numeric-fact item estimates_and_discretion_warranty_accrual_balance_classified_current_tag).",
  "account": "product warranty accrual",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001628280-26-040767:trends:warranty_reserve_ratio:2026-02-01..2026-05-02" }
```

```json
{ "id": "earnings_quality_soft_asset_share_quarterly_trend",
  "what_changed": "soft_asset_share in quarters-back-0 is 0.7532543117757928; quarter_over_quarter change against quarters-back-1 is 0.018216273529990112; year_over_year change against quarters-back-4 is -0.017193473364804146. Inputs: assets 6039449000.0, cash 1045126000.0, property_plant_and_equipment 445082000.0. Position: third lowest of the 6 filled quarters.",
  "account": "soft assets (total assets less PP&E and cash) over total assets",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
  "paragraph_id": "0001628280-26-040767:trends:soft_asset_share:2026-02-01..2026-05-02" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly_trend",
  "what_changed": "contract_liabilities_over_revenue in quarters-back-0 is 0.1517629599825305; quarter_over_quarter change against quarters-back-1 is -0.05174751833555685; year_over_year change against quarters-back-4 is -0.045269933457078415. Inputs: contract_liabilities 238380000.0 (ContractWithCustomerLiabilityCurrent, 2026-05-02), revenue 1570739000.0. Position: lowest of the 6 filled quarters. The ratio uses the current portion only; the long-term portion is outside it (see revenue_recognition_total_contract_liabilities_including_long_term).",
  "account": "current contract liabilities (deferred revenue)",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001628280-26-040767:trends:contract_liabilities_over_revenue:2026-02-01..2026-05-02" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly_insufficient",
  "what_changed": "insufficient: non_gaap_gap is not filled in quarters-back-0 (nor in any period of the table) because no us-gaap concept carries a non-GAAP measure; no change is printed. The release's own GAAP and non-GAAP figures are reported separately in earnings_quality_non_gaap_gap_in_release.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001628280-26-040767:trends:non_gaap_gap:2026-02-01..2026-05-02" }
```

### Trend table — years-back-0 (2024-11-03..2025-11-01)

```json
{ "id": "earnings_quality_accruals_over_total_assets_annual_trend",
  "what_changed": "accruals_over_total_assets in years-back-0 (2024-11-03..2025-11-01) is -0.11641837464940465; year_over_year change against years-back-1 is -0.04009320563361991; an annual period has no quarter_over_quarter change. Inputs: net_income 123338000.0, operating_cash_flow 806093000.0, assets 5864667000.0. Position: lowest of the 5 filled years.",
  "account": "total accruals (net income less operating cash flow) over total assets",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-040767:trends:accruals_over_total_assets:2024-11-03..2025-11-01" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual_trend",
  "what_changed": "bad_debt_reserve_ratio in years-back-0 is 0.011358893206952308; year_over_year change against years-back-1 is 0.0006019553631086399. Inputs: bad_debt_allowance 11212000.0 (AllowanceForDoubtfulAccountsReceivableCurrent, 2025-11-01, from the 10-K 0001628280-25-056698), receivables 975856000.0 (from 0001628280-26-040767). Position: second lowest of the 5 filled years.",
  "account": "allowance for doubtful accounts",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-040767:trends:bad_debt_reserve_ratio:2024-11-03..2025-11-01" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual_trend",
  "what_changed": "contract_liabilities_over_revenue in years-back-0 is 0.043806624038920584; year_over_year change against years-back-1 is 0.004857495094760564. Inputs: contract_liabilities 208936000.0, revenue 4769507000.0. Position: highest of the 5 filled years.",
  "account": "current contract liabilities (deferred revenue)",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-040767:trends:contract_liabilities_over_revenue:2024-11-03..2025-11-01" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_annual_trend",
  "what_changed": "days_sales_of_inventory in years-back-0 is 108.78630827717673; year_over_year change against years-back-1 is -23.81984804218861. Inputs: inventory 826235000.0, cost_of_revenue 2764590000.0. Position: second lowest of the 5 filled years.",
  "account": "inventories, net (days sales of inventory)",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-040767:trends:days_sales_of_inventory:2024-11-03..2025-11-01" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual_trend",
  "what_changed": "days_sales_outstanding in years-back-0 is 74.4755346831444; year_over_year change against years-back-1 is -9.482937329617883. Inputs: receivables 975856000.0, revenue 4769507000.0. Position: lowest of the 5 filled years.",
  "account": "accounts receivable, net (days sales outstanding)",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-040767:trends:days_sales_outstanding:2024-11-03..2025-11-01" }
```

```json
{ "id": "earnings_quality_gross_margin_annual_trend",
  "what_changed": "gross_margin in years-back-0 is 0.42036147551518427; year_over_year change against years-back-1 is -0.007934732038823167. Inputs: revenue 4769507000.0, cost_of_revenue 2764590000.0. Position: lowest of the 5 filled years.",
  "account": "gross margin (Revenues, CostOfGoodsAndServicesSold)",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-040767:trends:gross_margin:2024-11-03..2025-11-01" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_annual_trend",
  "what_changed": "inventory_reserve_ratio in years-back-0 is 0.1566237208542364; year_over_year change against years-back-1 is 0.025993441610425216. Inputs: inventory_reserve 129408000.0 (InventoryValuationReserves, 2025-11-01), inventory 826235000.0. Position: highest of the 5 filled years.",
  "account": "inventory valuation reserve (excess and obsolescence)",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-040767:trends:inventory_reserve_ratio:2024-11-03..2025-11-01" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual_insufficient",
  "what_changed": "insufficient: non_gaap_gap is not filled in years-back-0 because no us-gaap concept carries a non-GAAP measure; no change is printed.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001628280-26-040767:trends:non_gaap_gap:2024-11-03..2025-11-01" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual_trend",
  "what_changed": "receivables_over_revenue in years-back-0 is 0.20460311726138572; year_over_year change against years-back-1 is -0.021700041802663578. Inputs: receivables 975856000.0, revenue 4769507000.0. Position: lowest of the 5 filled years.",
  "account": "accounts receivable, net, against annual revenue",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-040767:trends:receivables_over_revenue:2024-11-03..2025-11-01" }
```

```json
{ "id": "earnings_quality_soft_asset_share_annual_trend",
  "what_changed": "soft_asset_share in years-back-0 is 0.7478576362477187; year_over_year change against years-back-1 is -0.026560201225915625. Inputs: assets 5864667000.0, cash 1091952000.0, property_plant_and_equipment 386779000.0. Position: second lowest of the 5 filled years.",
  "account": "soft assets (total assets less PP&E and cash) over total assets",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-040767:trends:soft_asset_share:2024-11-03..2025-11-01" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_annual_insufficient",
  "what_changed": "insufficient: warranty_reserve_ratio is not filled in years-back-0 because none of the three concepts its lookup searches is tagged in any period; no change is printed. The 10-Q prints the 2025-11-01 warranty accrual under ProductWarrantyAccrualClassifiedCurrent as 55533000.",
  "account": "product warranty accrual",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001628280-26-040767:trends:warranty_reserve_ratio:2024-11-03..2025-11-01" }
```

### Change of tag

```json
{ "id": "articulation_and_the_filed_history_bad_debt_allowance_tag_change_annual_cells",
  "what_changed": "Change of tag inside one metric: every annual bad_debt_reserve_ratio cell (years-back-0 to years-back-4) rests on AllowanceForDoubtfulAccountsReceivableCurrent, while every filled quarterly cell rests on AllowanceForDoubtfulAccountsReceivable. The annual and quarterly series of this ratio therefore rest on different concepts.",
  "account": "allowance for doubtful accounts",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"tag\": \"AllowanceForDoubtfulAccountsReceivableCurrent\"",
  "paragraph_id": "0001628280-26-040767:trends:bad_debt_reserve_ratio:2024-11-03..2025-11-01" }
```

```json
{ "id": "articulation_and_the_filed_history_bad_debt_allowance_tag_change_quarterly_cells",
  "what_changed": "Change of tag inside one metric, quarterly side: the quarters-back-0 bad_debt_reserve_ratio cell rests on AllowanceForDoubtfulAccountsReceivable (value 11000000.0), not on the AllowanceForDoubtfulAccountsReceivableCurrent concept the annual cells use.",
  "account": "allowance for doubtful accounts",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"tag\": \"AllowanceForDoubtfulAccountsReceivable\"",
  "paragraph_id": "0001628280-26-040767:trends:bad_debt_reserve_ratio:2026-02-01..2026-05-02" }
```

### Numeric facts

```json
{ "id": "estimates_and_discretion_warranty_accrual_balance_classified_current_tag",
  "what_changed": "The 10-Q tags the warranty accrual as ProductWarrantyAccrualClassifiedCurrent, a concept the trend lookup does not search; that is why warranty_reserve_ratio is insufficient in every period. The balance is 60356000 at 2026-05-02. The same filing prints 55533000 at 2025-11-01, 52313000 at 2025-05-03 and 55267000 at 2024-11-02; the Q1 10-Q (0001628280-26-015152) printed 58084000 at 2026-01-31. No ratio of this balance to revenue or to cost exists in my input and none is derived; a handful of balance points is insufficient for a trend claim.",
  "account": "product warranty accrual (current)",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"60356000\"",
  "paragraph_id": "0001628280-26-040767:facts:ProductWarrantyAccrualClassifiedCurrent:2026-05-02" }
```

```json
{ "id": "estimates_and_discretion_warranty_provision_six_months",
  "what_changed": "The warranty provision (ProductWarrantyExpense) for the six months ended 2026-05-02 is 16685000. The same filing prints 10714000 for the six months ended 2025-05-03 (row 0001628280-26-040767:facts:ProductWarrantyExpense:2024-11-03..2025-05-03), and the 8-K cash flow statement prints the same pair (16,685 and 10,714, thousands). The 10-K printed 24442000 for fiscal 2025. No discrete-quarter provision is printed and none is derived.",
  "account": "product warranty provision",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"16685000\"",
  "paragraph_id": "0001628280-26-040767:facts:ProductWarrantyExpense:2025-11-02..2026-05-02" }
```

```json
{ "id": "estimates_and_discretion_warranty_settlements_six_months",
  "what_changed": "Warranty settlements (ProductWarrantyAccrualPayments) for the six months ended 2026-05-02 are 11862000. The same filing prints 13668000 for the six months ended 2025-05-03 (row 0001628280-26-040767:facts:ProductWarrantyAccrualPayments:2024-11-03..2025-05-03). Provision and settlements are printed side by side in the rollforward; I compute no net.",
  "account": "product warranty settlements",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"11862000\"",
  "paragraph_id": "0001628280-26-040767:facts:ProductWarrantyAccrualPayments:2025-11-02..2026-05-02" }
```

```json
{ "id": "estimates_and_discretion_inventory_valuation_reserve_balance",
  "what_changed": "The inventory valuation reserve is 156735000 at 2026-05-02. The same filing prints 129408000 at 2025-11-01; the Q1 10-Q printed 145943000 at 2026-01-31 (the quarters-back-1 trend input). In the same filing, gross inventory (InventoryGross) is 965182000 against 955643000 and net inventory (InventoryNet) is 808447000 against 826235000. The trend ratio built on this reserve is the item estimates_and_discretion_inventory_reserve_ratio_quarterly_trend.",
  "account": "inventory valuation reserve (excess and obsolescence)",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"156735000\"",
  "paragraph_id": "0001628280-26-040767:facts:InventoryValuationReserves:2026-05-02" }
```

```json
{ "id": "estimates_and_discretion_inventory_write_down_six_months",
  "what_changed": "The provision for inventory excess and obsolescence (InventoryWriteDown) for the six months ended 2026-05-02 is 42481000. The 8-K cash flow statement prints 42,481 against 23,431 (thousands) for the six months ended May 3, 2025 (0001628280-26-040614:8k_2_02:67). The 10-K printed 48424000 for fiscal 2025. No discrete-quarter figure is printed and none is derived.",
  "account": "inventory write-down (excess and obsolescence provision)",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"42481000\"",
  "paragraph_id": "0001628280-26-040767:facts:InventoryWriteDown:2025-11-02..2026-05-02" }
```

```json
{ "id": "articulation_and_the_filed_history_inventory_write_down_two_precisions_one_filing",
  "what_changed": "Within 0001628280-26-040767, InventoryWriteDown for 2025-11-02..2026-05-02 is printed twice under the same paragraph_id: once as 42481000 and once as 42500000, the second row carrying \"decimals\": \"-5\". Both values are in one filing, so this is not a restatement by a later filing. I report both values and compute no gap between them.",
  "account": "inventory write-down (excess and obsolescence provision)",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"42500000\"",
  "paragraph_id": "0001628280-26-040767:facts:InventoryWriteDown:2025-11-02..2026-05-02" }
```

```json
{ "id": "earnings_quality_operating_cash_flow_six_months_only",
  "what_changed": "insufficient for the discrete quarter: the 10-Q prints operating cash flow only for the six months ended 2026-05-02, as 487347000; the 8-K prints 487,347 against 260,669 (thousands) for the prior-year six months. The Q1 10-Q printed 227645000 for 2025-11-02..2026-01-31 (the quarters-back-1 trend input). Operating cash flow for the discrete quarter 2026-02-01..2026-05-02 does not exist in my input and I do not derive it; this is why accruals_over_total_assets is not filled in quarters-back-0. Six-month net income is 368503000.",
  "account": "net cash provided by operating activities",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"487347000\"",
  "paragraph_id": "0001628280-26-040767:facts:NetCashProvidedByUsedInOperatingActivities:2025-11-02..2026-05-02" }
```

```json
{ "id": "revenue_recognition_remaining_performance_obligations",
  "what_changed": "Remaining performance obligations are 2500000000 at 2026-05-02. The Q1 10-Q printed 2300000000 at 2026-01-31 and the 10-K printed 2100000000 at 2025-11-01, all at rounded precision. Three points are insufficient for a trend claim; no growth rate is computed.",
  "account": "remaining performance obligations (backlog under contract)",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"2500000000\"",
  "paragraph_id": "0001628280-26-040767:facts:RevenueRemainingPerformanceObligation:2026-05-02" }
```

```json
{ "id": "liquidity_and_capital_purchase_obligations",
  "what_changed": "Purchase obligations are 2800000000 at 2026-05-02 (decimals -8). The Q1 10-Q printed 1900000000 at 2026-01-31 and the 10-K printed 2100000000 at 2025-11-01. On the same date, inventory, net is 808447000. No ratio is computed.",
  "account": "purchase obligations (supplier commitments)",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"2800000000\"",
  "paragraph_id": "0001628280-26-040767:facts:PurchaseObligation:2026-05-02" }
```

```json
{ "id": "revenue_recognition_total_contract_liabilities_including_long_term",
  "what_changed": "Total contract liabilities (ContractWithCustomerLiability) are 340487000 at 2026-05-02. The trend ratio contract_liabilities_over_revenue uses only the current portion, ContractWithCustomerLiabilityCurrent 238380000. The 8-K balance sheet prints deferred revenue of 238,380 and long-term deferred revenue of 102,107, against 208,936 and 94,850 at November 1, 2025 (thousands; 0001628280-26-040614:8k_2_02:61). The long-term portion sits outside the trend ratio.",
  "account": "contract liabilities (current and long-term deferred revenue)",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"340487000\"",
  "paragraph_id": "0001628280-26-040767:facts:ContractWithCustomerLiability:2026-05-02" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_share_repurchases_after_quarter_end",
  "what_changed": "Subsequent event: 44628 shares were repurchased between 2026-05-03 and 2026-05-29 for 25100000 (row 0001628280-26-040767:facts:StockRepurchasedDuringPeriodValue:2026-05-03..2026-05-29:us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember). Remaining authorization is 481600000 at 2026-05-29, against 506700000 at 2026-05-02 (row 0001628280-26-040767:facts:StockRepurchaseProgramRemainingAuthorizedRepurchaseAmount1:2026-05-02).",
  "account": "share repurchase program (subsequent event)",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"44628\"",
  "paragraph_id": "0001628280-26-040767:facts:StockRepurchasedDuringPeriodShares:2026-05-03..2026-05-29:us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

```json
{ "id": "liquidity_and_capital_share_repurchases_six_months",
  "what_changed": "Repurchases for the six months ended 2026-05-02 are 163700000, for 600000 shares (decimals -5). For the quarter, the release states approximately 0.2 million shares for $83.1 million (0001628280-26-040614:8k_2_02:36). The 8-K cash flow prints repurchase-program cash of (164,920) against (168,197) (thousands). Remaining authorization at 2026-05-02 is 506700000. Weighted basic shares are 141949000 in the quarter against 142503000 a year earlier.",
  "account": "share repurchases",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"163700000\"",
  "paragraph_id": "0001628280-26-040767:facts:StockRepurchasedDuringPeriodValue:2025-11-02..2026-05-02" }
```

```json
{ "id": "liquidity_and_capital_tax_withholding_on_vested_stock_units",
  "what_changed": "Payments for tax withholding on vested share-based awards for the six months ended 2026-05-02 are 179400000 (decimals -5). The 8-K cash flow statement prints (179,420) against (42,266) (thousands) for the prior-year six months, next to (164,920) of repurchase-program cash (0001628280-26-040614:8k_2_02:67).",
  "account": "shares repurchased for tax withholdings on vesting of stock unit awards",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"179400000\"",
  "paragraph_id": "0001628280-26-040767:facts:PaymentsRelatedToTaxWithholdingForShareBasedCompensation:2025-11-02..2026-05-02" }
```

```json
{ "id": "earnings_quality_share_based_compensation_quarter",
  "what_changed": "Share-based compensation for the quarter ended 2026-05-02 is 55473000, against 47960000 for the quarter ended 2025-05-03 as printed in this filing. It is 105300000 for six months, against 88767000. Unrecognized RSU compensation cost is 394800000 at 2026-05-02. The release adds share-based compensation back in every non-GAAP measure.",
  "account": "share-based compensation expense",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"55473000\"",
  "paragraph_id": "0001628280-26-040767:facts:ShareBasedCompensation:2026-02-01..2026-05-02" }
```

```json
{ "id": "across_documents_share_based_compensation_prior_year_quarter",
  "what_changed": "For the quarter ended 2025-05-03, the 10-Q's ShareBasedCompensation fact is 47960000, while the 8-K's Appendix B adds back share-based compensation expense of 48,024 (thousands) for the same quarter (0001628280-26-040614:8k_2_02:71). The 10-Q also prints a capitalized share-based compensation amount of -64000 for that quarter (row 0001628280-26-040767:facts:EmployeeServiceShareBasedCompensationAllocationOfRecognizedPeriodCostsCapitalizedAmount:2025-02-02..2025-05-03). For the current quarter both documents print 55,473 / 55473000, and the capitalized amount is 0. The two documents print different prior-year figures; I compute no gap.",
  "account": "share-based compensation expense",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"47960000\"",
  "paragraph_id": "0001628280-26-040767:facts:ShareBasedCompensation:2025-02-02..2025-05-03" }
```

```json
{ "id": "earnings_quality_diluted_share_count",
  "what_changed": "Weighted diluted shares for the quarter are 146314000, against 144972000 a year earlier. The dilutive adjustment is 4365000 against 2469000, basic shares are 141949000 against 142503000, and antidilutive securities excluded are 1000 against 1630000. Diluted EPS is 1.49 against 0.06.",
  "account": "weighted average diluted shares",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"146314000\"",
  "paragraph_id": "0001628280-26-040767:facts:WeightedAverageNumberOfDilutedSharesOutstanding:2026-02-01..2026-05-02" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_blue_planet_segment_revenue",
  "what_changed": "Blue Planet Automation Software and Services segment revenue is 23361000 for the quarter, against 27951000 a year earlier; for six months it is 43781000 against 53982000. Segment gross profit is 7386000 against 15393000 for the quarter. The release prints 23.4 against 28.0 ($ millions), or 1.5% against 2.5% of revenue (0001628280-26-040614:8k_2_02:38). Other segments as printed for the quarter: Networking Platforms 1274078000 against 866315000, Platform Software and Services 93878000 against 85441000, Global Services 179422000 against 146171000.",
  "account": "Blue Planet segment revenue",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"23361000\"",
  "paragraph_id": "0001628280-26-040767:facts:Revenues:2026-02-01..2026-05-02:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=cien:BluePlanetAutomationSoftwareandServicesSegmentMember" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_blue_planet_segment_measure",
  "what_changed": "The Blue Planet segment profit measure (tagged NetIncomeLoss in the segment disclosure) is -2842000 for the quarter, against 6477000 a year earlier; for six months it is -6657000 against 12976000. Segment research and development is 10228000 against 8916000 for the quarter. Goodwill allocated to the segment is printed as 89049000 at both 2026-05-02 and 2025-11-01.",
  "account": "Blue Planet segment profit",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"-2842000\"",
  "paragraph_id": "0001628280-26-040767:facts:NetIncomeLoss:2026-02-01..2026-05-02:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=cien:BluePlanetAutomationSoftwareandServicesSegmentMember" }
```

```json
{ "id": "structure_and_disclosure_changes_segment_measure_tagged_net_income_loss",
  "what_changed": "The segment disclosure tags its segment profit measure with NetIncomeLoss. The operating-segments total is 485536000 for the quarter (918824000 for six months), while consolidated NetIncomeLoss for the quarter is 218220000 (row 0001628280-26-040767:facts:NetIncomeLoss:2026-02-01..2026-05-02). A reader keyed on the NetIncomeLoss tag has to filter on ConsolidationItemsAxis. My input does not show whether earlier filings tagged the segment measure the same way.",
  "account": "segment profit measure (tagging)",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"485536000\"",
  "paragraph_id": "0001628280-26-040767:facts:NetIncomeLoss:2026-02-01..2026-05-02:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember" }
```

```json
{ "id": "estimates_and_discretion_accrued_compensation_balance",
  "what_changed": "Accrued salaries (AccruedSalariesCurrent) are 172568000 at 2026-05-02, against 281542000 at 2025-11-01 in the same filing. Other rows of the accrued-liabilities table in the same filing: accrued income taxes 659000 against 10729000, other accrued liabilities 152279000 against 132413000, and total accrued liabilities 439626000 against 531081000. My input says nothing on the cause; I infer none.",
  "account": "accrued compensation",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"172568000\"",
  "paragraph_id": "0001628280-26-040767:facts:AccruedSalariesCurrent:2026-05-02" }
```

### Figures in the 8-K earnings release

```json
{ "id": "across_documents_days_sales_outstanding_release_against_trend",
  "what_changed": "The release states average DSO of 71 for the quarter. The trend table's days_sales_outstanding for quarters-back-0 (receivables / revenue * days_in_period, on period-end receivables) is 60.98007307388433, the lowest of the 6 filled quarters. The release calls its figure an average, and its method is not in my input; I reconcile nothing.",
  "account": "accounts receivable (days sales outstanding)",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "Average days' sales outstanding (DSOs) were 71.",
  "paragraph_id": "0001628280-26-040614:8k_2_02:34" }
```

```json
{ "id": "across_documents_inventory_turns_release_against_trend",
  "what_changed": "The release states inventory turns of 3.6 for the quarter. The trend table's days_sales_of_inventory for quarters-back-0 is 83.678266803915, the lowest of the 6 filled quarters. The release's turns method is not in my input; I convert nothing.",
  "account": "inventories (turns)",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "Inventory turns were 3.6.",
  "paragraph_id": "0001628280-26-040614:8k_2_02:35" }
```

```json
{ "id": "results_against_expectations_third_quarter_revenue_guidance",
  "what_changed": "New guidance for fiscal Q3 2026 revenue: $1.625 billion plus or minus $50 million. Q2 revenue as printed is 1570739000 (10-Q) and $1.57 billion (release). Insufficient to judge Q2 against expectations: the guidance given for Q2 (in the 8-K of 2026-03-05) is not in my input, and no consensus figure is either.",
  "account": "revenue",
  "expected_direction": "none",
  "horizon": "fiscal third quarter 2026 (next quarterly filing)",
  "quote": "Providing revenue guidance for fiscal third quarter 2026 of $1.625 billion plus or minus $50 million",
  "paragraph_id": "0001628280-26-040614:8k_2_02:8" }
```

```json
{ "id": "results_against_expectations_full_year_revenue_guidance_raised",
  "what_changed": "The company raises fiscal 2026 revenue guidance to $6.3 billion plus or minus $100 million and itself prints a 32% year-over-year increase at the midpoint. The guidance figure this replaces is not in my input. Fiscal 2025 revenue in the trend inputs is 4769507000.",
  "account": "revenue",
  "expected_direction": "up",
  "horizon": "fiscal year 2026 (next annual report)",
  "quote": "Raising revenue guidance for fiscal year 2026 to $6.3 billion plus or minus $100 million, a 32% increase YoY at the midpoint",
  "paragraph_id": "0001628280-26-040614:8k_2_02:9" }
```

```json
{ "id": "results_against_expectations_third_quarter_adjusted_gross_margin_guidance",
  "what_changed": "Fiscal Q3 2026 adjusted gross margin guidance is 45% plus or minus 50 bps. Q2 adjusted gross margin is printed as 44.9% and GAAP gross margin as 44.0% (0001628280-26-040614:8k_2_02:19). Fiscal 2026 adjusted gross margin guidance is between 44.5% and 45% (:29). The trend gross_margin for quarters-back-0 is 0.44027301798707486, the highest of the 6 filled quarters. The margin guidance is non-GAAP only; the release says it cannot reconcile it to GAAP.",
  "account": "gross margin (adjusted, non-GAAP)",
  "expected_direction": "none",
  "horizon": "fiscal third quarter 2026 (next quarterly filing)",
  "quote": "Adjusted (non-GAAP) gross margin in the range of 45% plus or minus 50 bps",
  "paragraph_id": "0001628280-26-040614:8k_2_02:24" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_in_release",
  "what_changed": "The trend table cannot fill non_gaap_gap, but the release prints both sides. Diluted EPS is $1.49 GAAP and $1.64 adjusted for Q2 2026, against $0.06 and $0.42 a year earlier. Appendix A prints GAAP net income of 218,220 and adjusted net income of 240,199 (thousands), against 8,969 and 60,657 (0001628280-26-040614:8k_2_02:68). The adjustments are share-based compensation, amortization of intangibles, restructuring, the holdback arrangement and a non-GAAP tax provision. I compute no gap ratio.",
  "account": "non-GAAP net income and EPS against GAAP",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "$1.49 GAAP and $1.64 adjusted (non-GAAP) for the fiscal second quarter 2026, compared to $0.06 and $0.42 for fiscal second quarter 2025, respectively",
  "paragraph_id": "0001628280-26-040614:8k_2_02:17" }
```

```json
{ "id": "estimates_and_discretion_non_gaap_tax_rate_lowered",
  "what_changed": "The statutory rate applied in the non-GAAP tax provision is 20% for Q2 fiscal 2026, against 22% for Q2 fiscal 2025. Appendix A prints a non-GAAP tax provision of 60,050 on adjusted income before income taxes of 300,249 (thousands), against 17,108 on 77,765 (0001628280-26-040614:8k_2_02:68). The release says the rate may change.",
  "account": "non-GAAP tax provision rate",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "utilizes a current, blended U.S. and foreign statutory annual tax rate of 20% for the second quarter of fiscal 2026 and 22% for the second quarter of fiscal 2025",
  "paragraph_id": "0001628280-26-040614:8k_2_02:78" }
```

```json
{ "id": "earnings_quality_gaap_tax_provision_quarter",
  "what_changed": "The GAAP provision for income taxes is 12,840 on income before income taxes of 231,060 for Q2 2026, against 10,047 on 19,016 a year earlier. For six months it is 43,672 on 412,175, against 34,069 on 87,610 (thousands). Cash paid for income taxes over six months is 48,830 against 55,466 (:67). Accrued income taxes in the 10-Q are 659000 at 2026-05-02 against 10729000 at 2025-11-01. The non-GAAP provision for the same quarter is 60,050. My input prints no GAAP effective rate, and I compute none.",
  "account": "provision for income taxes (GAAP)",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "| Provision for income taxes | 12,840 |",
  "paragraph_id": "0001628280-26-040614:8k_2_02:55" }
```

```json
{ "id": "structure_and_disclosure_changes_holdback_arrangement_adjustment",
  "what_changed": "A new non-GAAP adjustment, \"Holdback arrangement\", of 2,411 (thousands) appears in the Q2 2026 operating expense and Adjusted EBITDA reconciliations, with a dash in the prior-year column (:68, :71). It concerns merger consideration for Nubis Communications that GAAP treats as contingent compensation. The six-month GAAP income statement also prints acquisition and integration costs of 306 (:55).",
  "account": "non-GAAP adjustments (acquisition-related compensation)",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "Holdback arrangement - reflects a one-time holdback of a portion of the merger consideration otherwise payable at closing to certain key employee shareholders of Nubis Communications, Inc. who became employees of Ciena, which is treated as contingent compensation for GAAP reporting purposes.",
  "paragraph_id": "0001628280-26-040614:8k_2_02:77" }
```

```json
{ "id": "liquidity_and_capital_capital_expenditures_six_months",
  "what_changed": "Payments for equipment, furniture and fixtures are (114,933) for the six months ended May 2, 2026, against (55,622) a year earlier (thousands). The balance sheet prints equipment, net of 445,082 against 386,779, cash and cash equivalents of 1,045,126 against 1,091,952, and long-term investments of 200,106 against 57,142 (0001628280-26-040614:8k_2_02:61).",
  "account": "capital expenditures",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "| Payments for equipment, furniture, and fixtures | (114,933) |",
  "paragraph_id": "0001628280-26-040614:8k_2_02:67" }
```

```json
{ "id": "revenue_recognition_customer_concentration_two_customers",
  "what_changed": "Two customers are each 10%-plus of Q2 revenue, together 34.0%. The 10-Q facts carry two customer-level revenue amounts for the quarter tagged to cloud-provider members, 321224000 and 212288000. The concentration share for earlier quarters is not in my input, so a trend in concentration is insufficient.",
  "account": "revenue concentration (major customers)",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "Two customers represented 10%-plus of revenue for a total of 34.0% of revenue.",
  "paragraph_id": "0001628280-26-040614:8k_2_02:33" }
```

## Seen in the notes

No item is placed here. The split this heading needs is not in my input: no row in input_numbers.json records whether its element sat inside a note. Each fact prints only id, paragraph_id, tag, prefix, namespace, context, context_ref, unit, decimals, value, number, nil, form, source_accession, filing_date and, on some rows, superseded_by. So every numeric-fact item stays under "Seen in the statements", and this empty section does not mean that none of those facts came from a note table.
