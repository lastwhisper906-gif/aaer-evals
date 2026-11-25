# CARR — numbers reader — 10-Q 0001783180-26-000032 (period ending 2026-06-30, filed 2026-07-28)

## What I read, and what my input does not hold

- **input_8k.md** (8-K 0001783180-26-000030, item 2.02, filed 2026-07-28): read in full.
- **input_trends.json**: read in full.
- **input_prior_predictions.md**: read in full. It says: "None on record." No earlier flags exist for this company.
- **input_numbers.json**: 87,437 lines (2.9 MB). It is too large to hold in one context, so I read it in parts:
  - lines 1–6,499: the 10-K 0001783180-26-000008 primary statements and the start of its equity statement;
  - lines 60,150–70,998 and 72,000–74,959: the end of the Q1 10-Q 0001783180-26-000026 block, then the triggering 10-Q 0001783180-26-000032 from its first fact through its statements, inventory, goodwill, intangibles, borrowings, fair value, pension, share-based compensation and warranty facts;
  - lines 86,000–87,436: the 10-Q's geographic revenue, related-party and contingency facts;
  - short probes at lines 44,999–45,059, 75,500–75,619, 76,400–76,499, 77,400–77,499, 78,500–78,619, 81,500–81,619, 84,000–84,119 and 85,300–85,399.
  - I did not read the rest of the 10-K block (about lines 6,500–42,000), most of the Q1 10-Q block (about lines 42,000–60,149) or the remaining 10-Q segment-note lines. Nothing below claims anything about those lines.
- No prices, abnormal returns, short interest, other companies' files, prior-run probabilities or outcome windows are in my directory.
- **Articulation checks, restatement traces and the fourth-quarter derivation do not exist in my input.** input_numbers.json holds only `ticker`, `cutoff`, `documents` and `facts`. The trend table names `src/fourth_quarter.py` as the source of a fourth-quarter derivation, but that output is not in my directory. So there is no articulation gap to report.
- **Restated prior values.** Some facts carry a `superseded_by` field naming a later filing that re-reported the same period. I did not compute anything; I set the printed value strings side by side. In every pair I read, the later filing printed the same value:
  - 10-K vs 10-Q: every 2025-12-31 balance-sheet line, and the 2024-12-31 equity components;
  - Q1 10-Q vs 10-Q: the 2025-12-31 environmental, asbestos, related-party and held-for-sale facts;
  - the 2025-12-31 inventory valuation reserve (337000000) and warranty accrual (893000000) printed in the 10-Q equal the trend-table inputs taken from 0001783180-26-000026.
  - I found no restated value in the lines I read. This is not a statement about the lines I did not read.
- **quarters-back-0 (target end 2026-06-30) has no cells.** The reason the period gives: "no quarter ending within 20 days of 2026-06-30 is in the companyfacts record; the companyfacts record's newest row was filed 2026-04-30, before this run's cutoff 2026-07-28 — the record was fetched before the triggering report, so the periods that report is the first to state are not in it". No ratio exists for the triggering quarter. Below I report the triggering quarter's raw tagged facts instead, with no ratio computed.
- **quarters-back-2 (target end 2025-12-30) has no cells.** Reason: "no quarter ending within 20 days of 2025-12-30 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py". As a result, every quarters-back-1 cell has no quarter-over-quarter change.
- **R&D-capitalisation baseline (years-back-0).** Its rows print no `paragraph_id`, so they cannot be quoted and are not itemised. As printed:
  - `earnings_with_rnd_capitalized` 1605600000.0; `research_and_development_asset` 1736600000.0; `research_and_development_amortization` 503400000.0.
  - `book_value_with_rnd_capitalized` is missing: "no row for stockholders_equity in 2025-12-31: us-gaap:StockholdersEquity is in the record, but not for this period".
  - `capitalized_development_cost` is missing because the record tags no us-gaap:CapitalizedComputerSoftwareAdditions.
- **Conventions.**
  - `expected_direction` is the sign of the change as Python printed it. For raw facts it is the direction from the earlier printed value to the later one in the same filing. It is `none` where no change exists or the cell is insufficient.
  - Every number below is copied from my input; none is computed.

## Seen in the statements

```json
{ "id": "earnings_quality_accruals_over_total_assets_latest_year", "what_changed": "years-back-0 (2025-01-01..2025-12-31) accruals_over_total_assets value -0.02766872815272923; year-over-year change against years-back-1 -0.16244401355764326 (years-back-1 value 0.13477528540491404). Position: second lowest of the 4 filled years on the same concepts. years-back-4 rests on a different net_income concept and is not compared. Inputs: NetIncomeLoss 1484000000, NetCashProvidedByUsedInOperatingActivities 2513000000, Assets 37190000000. Other years: years-back-2 -0.03832795076473097, years-back-3 0.06865751744230622.", "account": "accruals: net income less operating cash flow over total assets (us-gaap:NetIncomeLoss, us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:Assets)", "expected_direction": "down", "horizon": "next annual report (fiscal 2026)", "quote": "\"position_in_history\": \"second lowest of the 4 filled years on the same concepts; 1 other filled year rests on a different concept and is not compared\"", "paragraph_id": "0001783180-26-000032:trends:accruals_over_total_assets:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_latest_year", "what_changed": "years-back-0 bad_debt_reserve_ratio value 0.02977941176470588; change against years-back-1 -0.00551898707081086. Position: lowest of the 5 filled years. Inputs: AllowanceForDoubtfulAccountsReceivable 81000000 (2025-12-31, from 0001783180-26-000008), ReceivablesNetCurrent 2639000000. Earlier years: 0.03529839883551674, 0.041916167664670656, 0.03966101694915254, 0.03532717784022481. Only one quarter (2024-12-31) is filled for this ratio, so there is no quarterly trend.", "account": "allowance for doubtful accounts receivable", "expected_direction": "down", "horizon": "next annual report (fiscal 2026)", "quote": "\"position_in_history\": \"lowest of the 5 filled years\"", "paragraph_id": "0001783180-26-000032:trends:bad_debt_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_latest_year", "what_changed": "years-back-0 contract_liabilities_over_revenue value 0.03177449763185727; change against years-back-1 0.007181417493104265. Position: highest of the 5 filled years. Inputs: ContractWithCustomerLiabilityCurrent 691000000 at 2025-12-31 (input printed from 0001783180-26-000026), revenue 21747000000. Earlier years: 0.024593080138753002, 0.022109651205741123, 0.0259717723276261, 0.020132925823509437.", "account": "current contract liabilities (us-gaap:ContractWithCustomerLiabilityCurrent)", "expected_direction": "up", "horizon": "next annual report (fiscal 2026)", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0001783180-26-000032:trends:contract_liabilities_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_latest_year_insufficient", "what_changed": "insufficient: the years-back-0 cell is not filled because no undimensioned cost-of-revenue row exists for 2025. Only years-back-1 (50.98055134807634), years-back-2 (48.255493509319024) and years-back-3 (74.17442845046571) are filled. Three annual points that stop at 2024 do not support a trend claim for 2025.", "account": "days sales of inventory (inventory over cost of revenue)", "expected_direction": "none", "horizon": "next annual report (fiscal 2026)", "quote": "\"missing\": \"no row for cost_of_revenue in 2025-01-01..2025-12-31: us-gaap:CostOfRevenue, us-gaap:CostOfGoodsAndServicesSold, us-gaap:CostOfGoodsSold, us-gaap:CostOfServices, us-gaap:CostOfSales is in the record, but not for this period\"", "paragraph_id": "0001783180-26-000032:trends:days_sales_of_inventory:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_latest_year", "what_changed": "years-back-0 days_sales_outstanding value 44.29277601508254; change against years-back-1 1.1429939284508563. Position: second highest of the 5 filled years. Inputs: ReceivablesNetCurrent 2639000000, revenue 21747000000. Earlier years: 43.14978208663168, 40.0612104902116 (lowest), 59.812875983341044 (highest), 42.55057487993014.", "account": "trade receivables (us-gaap:ReceivablesNetCurrent)", "expected_direction": "up", "horizon": "next annual report (fiscal 2026)", "quote": "\"position_in_history\": \"second highest of the 5 filled years\"", "paragraph_id": "0001783180-26-000032:trends:days_sales_outstanding:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_gross_margin_latest_year_insufficient", "what_changed": "insufficient: the years-back-0 gross_margin cell is not filled because no undimensioned cost-of-revenue row exists for 2025. Filled years are years-back-1 0.2659877256959886, years-back-2 0.2723866814416126 and years-back-3 0.2485539102267469. No 2025 gross margin exists in the trend table.", "account": "gross margin (revenue less cost of revenue over revenue)", "expected_direction": "none", "horizon": "next annual report (fiscal 2026)", "quote": "\"missing\": \"no row for cost_of_revenue in 2025-01-01..2025-12-31: us-gaap:CostOfRevenue, us-gaap:CostOfGoodsAndServicesSold, us-gaap:CostOfGoodsSold, us-gaap:CostOfServices, us-gaap:CostOfSales is in the record, but not for this period\"", "paragraph_id": "0001783180-26-000032:trends:gross_margin:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_latest_year", "what_changed": "years-back-0 inventory_reserve_ratio value 0.13572291582762788; change against years-back-1 0.042203994557510435. Position: highest of the 5 filled years. Inputs: InventoryValuationReserves 337000000, InventoryNet 2483000000 at 2025-12-31. Earlier years: 0.09351892127011745, 0.09489851892484914, 0.07196969696969698 (lowest), 0.07817258883248732.", "account": "inventory valuation reserves (us-gaap:InventoryValuationReserves)", "expected_direction": "up", "horizon": "next annual report (fiscal 2026)", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0001783180-26-000032:trends:inventory_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_latest_year_insufficient", "what_changed": "insufficient: non_gaap_gap is filled in no period, because companyfacts holds no non-GAAP measure. The 8-K prints adjusted figures, but no Python-computed gap between them and GAAP exists in my input.", "account": "gap between non-GAAP and GAAP net income", "expected_direction": "none", "horizon": "next annual report (fiscal 2026)", "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"", "paragraph_id": "0001783180-26-000032:trends:non_gaap_gap:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_latest_year", "what_changed": "years-back-0 receivables_over_revenue value 0.12135007127419874; change against years-back-1 0.003454491802527479. Position: second highest of the 5 filled years. Earlier years: 0.11789557947167126, 0.10975674106907288 (lowest), 0.16387089310504396 (highest), 0.11657691747926066.", "account": "trade receivables (us-gaap:ReceivablesNetCurrent)", "expected_direction": "up", "horizon": "next annual report (fiscal 2026)", "quote": "\"position_in_history\": \"second highest of the 5 filled years\"", "paragraph_id": "0001783180-26-000032:trends:receivables_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_soft_asset_share_latest_year", "what_changed": "years-back-0 soft_asset_share value 0.8730841624092498; change against years-back-1 0.05937937937045612. Position: highest of the 5 filled years. Inputs: Assets 37190000000, PropertyPlantAndEquipmentNet 3165000000, CashAndCashEquivalentsAtCarryingValue 1555000000. Earlier years: 0.8137047830387937, 0.6340259581987692 (lowest), 0.7876638810089703, 0.8161011768302002.", "account": "soft assets: total assets less PP&E and cash, over total assets", "expected_direction": "up", "horizon": "next annual report (fiscal 2026)", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0001783180-26-000032:trends:soft_asset_share:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_latest_year", "what_changed": "years-back-0 warranty_reserve_ratio value 0.041063135145077485; change against years-back-1 0.0061080519822206. Position: highest of the 5 filled years. Inputs: ProductWarrantyAccrual 893000000 at 2025-12-31 (printed from 0001783180-26-000026), revenue 21747000000. Earlier years: 0.034955083162856886, 0.029972033138092977, 0.03146691346598797, 0.02542085091932276 (lowest).", "account": "product warranty accrual (us-gaap:ProductWarrantyAccrual)", "expected_direction": "up", "horizon": "next annual report (fiscal 2026)", "quote": "\"position_in_history\": \"highest of the 5 filled years\"", "paragraph_id": "0001783180-26-000032:trends:warranty_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_latest_filled_quarter", "what_changed": "quarters-back-1 (2026-01-01..2026-03-31) accruals_over_total_assets value 0.004275802721454311; year-over-year change against quarters-back-5 0.006223836853207267 (quarters-back-5 value -0.0019480341317529564). There is no quarter-over-quarter change because quarters-back-2 is not filled. Position: highest of the 2 filled quarters. Two quarterly points do not support a trend claim. Inputs: NetIncomeLoss 238000000, NetCashProvidedByUsedInOperatingActivities 79000000, Assets 37186000000.", "account": "accruals: net income less operating cash flow over total assets", "expected_direction": "up", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"position_in_history\": \"highest of the 2 filled quarters\"", "paragraph_id": "0001783180-26-000032:trends:accruals_over_total_assets:2026-01-01..2026-03-31" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_latest_filled_quarter", "what_changed": "quarters-back-1 contract_liabilities_over_revenue value 0.13518067777569742; year-over-year change against quarters-back-5 0.03130946275078367. No quarter-over-quarter change exists (quarters-back-2 not filled). Position: highest of the 6 filled quarters. Inputs: ContractWithCustomerLiabilityCurrent 722000000 at 2026-03-31, revenue 5341000000.", "account": "current contract liabilities (us-gaap:ContractWithCustomerLiabilityCurrent)", "expected_direction": "up", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"", "paragraph_id": "0001783180-26-000032:trends:contract_liabilities_over_revenue:2026-01-01..2026-03-31" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_latest_filled_quarter", "what_changed": "quarters-back-1 days_sales_outstanding value 52.7429320351994; year-over-year change against quarters-back-5 1.3611765733366212. No quarter-over-quarter change exists. Position: highest of the 6 filled quarters. Inputs: ReceivablesNetCurrent 3130000000 at 2026-03-31, revenue 5341000000.", "account": "trade receivables (us-gaap:ReceivablesNetCurrent)", "expected_direction": "up", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"", "paragraph_id": "0001783180-26-000032:trends:days_sales_outstanding:2026-01-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_latest_filled_quarter", "what_changed": "quarters-back-1 inventory_reserve_ratio value 0.1336691204959318; year-over-year change against quarters-back-5 0.04265703590378678. No quarter-over-quarter change exists. Position: highest of the 6 filled quarters. Inputs: InventoryValuationReserves 345000000, InventoryNet 2581000000 at 2026-03-31.", "account": "inventory valuation reserves (us-gaap:InventoryValuationReserves)", "expected_direction": "up", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"", "paragraph_id": "0001783180-26-000032:trends:inventory_reserve_ratio:2026-01-01..2026-03-31" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_latest_filled_quarter", "what_changed": "quarters-back-1 receivables_over_revenue value 0.5860325781688822; year-over-year change against quarters-back-5 0.015124184148184616. No quarter-over-quarter change exists. Position: highest of the 6 filled quarters.", "account": "trade receivables (us-gaap:ReceivablesNetCurrent)", "expected_direction": "up", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"", "paragraph_id": "0001783180-26-000032:trends:receivables_over_revenue:2026-01-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_soft_asset_share_latest_filled_quarter", "what_changed": "quarters-back-1 soft_asset_share value 0.8791749583176465; year-over-year change against quarters-back-5 0.009171940236597287. No quarter-over-quarter change exists. Position: highest of the 6 filled quarters. Inputs: Assets 37186000000, PropertyPlantAndEquipmentNet 3122000000, cash 1371000000.", "account": "soft assets: total assets less PP&E and cash, over total assets", "expected_direction": "up", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"", "paragraph_id": "0001783180-26-000032:trends:soft_asset_share:2026-01-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_latest_filled_quarter", "what_changed": "quarters-back-1 warranty_reserve_ratio value 0.17038007863695936; year-over-year change against quarters-back-5 0.014381611791424664. No quarter-over-quarter change exists. Position: highest of the 6 filled quarters. Inputs: ProductWarrantyAccrual 910000000 at 2026-03-31, revenue 5341000000.", "account": "product warranty accrual (us-gaap:ProductWarrantyAccrual)", "expected_direction": "up", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"", "paragraph_id": "0001783180-26-000032:trends:warranty_reserve_ratio:2026-01-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_latest_filled_quarter_insufficient", "what_changed": "insufficient: no allowance row exists for 2026-03-31. bad_debt_reserve_ratio is filled in only one quarter of the window (2024-12-31, the only filled quarter).", "account": "allowance for doubtful accounts receivable", "expected_direction": "none", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"missing\": \"no row for bad_debt_allowance in 2026-03-31: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"", "paragraph_id": "0001783180-26-000032:trends:bad_debt_reserve_ratio:2026-01-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_latest_filled_quarter_insufficient", "what_changed": "insufficient: days_sales_of_inventory is filled in no quarter of the window, because no undimensioned cost-of-revenue row exists for any quarter.", "account": "days sales of inventory", "expected_direction": "none", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"missing\": \"no row for cost_of_revenue in 2026-01-01..2026-03-31: us-gaap:CostOfRevenue, us-gaap:CostOfGoodsAndServicesSold, us-gaap:CostOfGoodsSold, us-gaap:CostOfServices, us-gaap:CostOfSales is in the record, but not for this period\"", "paragraph_id": "0001783180-26-000032:trends:days_sales_of_inventory:2026-01-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_gross_margin_latest_filled_quarter_insufficient", "what_changed": "insufficient: gross_margin is filled in no quarter of the window, for the same missing cost-of-revenue row.", "account": "gross margin", "expected_direction": "none", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"missing\": \"no row for cost_of_revenue in 2026-01-01..2026-03-31: us-gaap:CostOfRevenue, us-gaap:CostOfGoodsAndServicesSold, us-gaap:CostOfGoodsSold, us-gaap:CostOfServices, us-gaap:CostOfSales is in the record, but not for this period\"", "paragraph_id": "0001783180-26-000032:trends:gross_margin:2026-01-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_latest_filled_quarter_insufficient", "what_changed": "insufficient: non_gaap_gap is not filled in quarters-back-1, nor in any other period.", "account": "gap between non-GAAP and GAAP net income", "expected_direction": "none", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"", "paragraph_id": "0001783180-26-000032:trends:non_gaap_gap:2026-01-01..2026-03-31" }
```

```json
{ "id": "articulation_and_the_filed_history_net_income_concept_switch_in_accruals_history", "what_changed": "Change of tag: the net_income input of accruals_over_total_assets is us-gaap:NetIncomeLoss in years-back-0 through years-back-3 and us-gaap:ProfitLoss in years-back-4 (2021: 1701000000 from 0001783180-24-000009). The table therefore prints no years-back-3 against years-back-4 change, and it ranks years-back-0 to years-back-3 only among themselves; each of those cells reports that 1 other filled year rests on a different concept.", "account": "net income concept feeding the accruals ratio (us-gaap:NetIncomeLoss vs us-gaap:ProfitLoss)", "expected_direction": "none", "horizon": "every annual accruals comparison that reaches fiscal 2021", "quote": "net_income: us-gaap:NetIncomeLoss in years-back-3 and us-gaap:ProfitLoss in years-back-4", "paragraph_id": "0001783180-26-000032:trends:accruals_over_total_assets:2022-01-01..2022-12-31" }
```

```json
{ "id": "articulation_and_the_filed_history_profit_loss_year_left_uncompared", "what_changed": "years-back-4 (2021-01-01..2021-12-31) accruals_over_total_assets value -0.020479902185541802 rests on us-gaap:ProfitLoss, and is set apart from the four NetIncomeLoss years. Its year-over-year change does not exist (the year before is outside the requested window).", "account": "accruals ratio, fiscal 2021", "expected_direction": "none", "horizon": "every annual accruals comparison that reaches fiscal 2021", "quote": "\"position_in_history\": \"the only filled year on the same concepts; 4 other filled years rest on a different concept and are not compared\"", "paragraph_id": "0001783180-26-000032:trends:accruals_over_total_assets:2021-01-01..2021-12-31" }
```

```json
{ "id": "structure_and_disclosure_changes_cost_of_sales_tagged_only_by_product_and_service", "what_changed": "In the fiscal 2025 10-K facts, CostOfGoodsAndServicesSold for 2025-01-01..2025-12-31 is tagged with srt:ProductOrServiceAxis members: product 14232000000, service 1891000000. The trend table finds no undimensioned cost row for 2025 or for any quarter of the window. Years-back-1 to years-back-3 instead use an undimensioned CostOfGoodsAndServicesSold from 0001783180-25-000008. The triggering 10-Q likewise tags product 4081000000 and service 542000000 for 2026-04-01..2026-06-30. This tagging is why gross margin and days sales of inventory are insufficient for 2025 and for every quarter.", "account": "cost of products and services sold (us-gaap:CostOfGoodsAndServicesSold)", "expected_direction": "none", "horizon": "every gross-margin comparison from fiscal 2025 on", "quote": "\"value\": \"14232000000\"", "paragraph_id": "0001783180-26-000008:facts:CostOfGoodsAndServicesSold:2025-01-01..2025-12-31:srt:ProductOrServiceAxis=us-gaap:ProductMember" }
```

```json
{ "id": "results_against_expectations_quarter_revenue_in_the_filed_facts", "what_changed": "Triggering 10-Q: RevenueFromContractWithCustomerExcludingAssessedTax for 2026-04-01..2026-06-30 is 6351000000. The same filing prints 6113000000 for 2025-04-01..2025-06-30, and the Q1 10-Q printed 5341000000 for 2026-01-01..2026-03-31. Six months: 11692000000 vs 11331000000. Product 5634000000 vs 5477000000; service 717000000 vs 636000000. This paragraph_id prints twice in the 10-Q (statement and segment note), both 6351000000.", "account": "revenue (us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax)", "expected_direction": "up", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"6351000000\"", "paragraph_id": "0001783180-26-000032:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30" }
```

```json
{ "id": "results_against_expectations_quarter_operating_income_in_the_filed_facts", "what_changed": "OperatingIncomeLoss for 2026-04-01..2026-06-30 is 825000000 against 903000000 for 2025-04-01..2025-06-30. Six months: 1083000000 vs 1532000000. OtherOperatingIncomeExpenseNet for the quarter is -3000000 vs 30000000.", "account": "operating income (us-gaap:OperatingIncomeLoss)", "expected_direction": "down", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"825000000\"", "paragraph_id": "0001783180-26-000032:facts:OperatingIncomeLoss:2026-04-01..2026-06-30" }
```

```json
{ "id": "results_against_expectations_quarter_net_income_in_the_filed_facts", "what_changed": "NetIncomeLoss for 2026-04-01..2026-06-30 is 501000000 against 591000000; six months 739000000 vs 1003000000. Pre-tax income from continuing operations: 721000000 vs 812000000.", "account": "net income attributable to common shareowners (us-gaap:NetIncomeLoss)", "expected_direction": "down", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"501000000\"", "paragraph_id": "0001783180-26-000032:facts:NetIncomeLoss:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_quarter_income_tax_expense_in_the_filed_facts", "what_changed": "IncomeTaxExpenseBenefit for 2026-04-01..2026-06-30 is 180000000 against 162000000, on pre-tax income of 721000000 vs 812000000. Six months: 84000000 vs 273000000. The 8-K prints effective tax rates of 25.0% vs 20.0% for the quarter and 9.4% vs 20.1% for six months; I computed no rate.", "account": "income tax expense (us-gaap:IncomeTaxExpenseBenefit)", "expected_direction": "up", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"180000000\"", "paragraph_id": "0001783180-26-000032:facts:IncomeTaxExpenseBenefit:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_quarter_equity_method_income_in_the_filed_facts", "what_changed": "IncomeLossFromEquityMethodInvestments for 2026-04-01..2026-06-30 is 58000000 against 78000000; six months 89000000 vs 122000000. Six-month distributions from equity method investments: 51000000 vs 81000000.", "account": "equity method investment earnings (us-gaap:IncomeLossFromEquityMethodInvestments)", "expected_direction": "down", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"58000000\"", "paragraph_id": "0001783180-26-000032:facts:IncomeLossFromEquityMethodInvestments:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_receivables_at_quarter_end_in_the_filed_facts", "what_changed": "ReceivablesNetCurrent at 2026-06-30 is 3246000000. The same filing prints 2639000000 at 2025-12-31; the trend input at 2026-03-31 is 3130000000. Six-month IncreaseDecreaseInReceivables: 651000000 vs 702000000. The related-party portion is 396000000 (see notes). A receivables-to-revenue or days-sales-outstanding figure for this quarter does not exist in my input.", "account": "trade receivables (us-gaap:ReceivablesNetCurrent)", "expected_direction": "up", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"3246000000\"", "paragraph_id": "0001783180-26-000032:facts:ReceivablesNetCurrent:2026-06-30" }
```

```json
{ "id": "earnings_quality_inventory_at_quarter_end_in_the_filed_facts", "what_changed": "InventoryNet at 2026-06-30 is 2759000000. The same filing prints 2483000000 at 2025-12-31; the trend input at 2026-03-31 is 2581000000. Six-month IncreaseDecreaseInInventories: 335000000 vs 412000000. No days-sales-of-inventory or reserve ratio exists for this quarter in my input.", "account": "inventory (us-gaap:InventoryNet)", "expected_direction": "up", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"2759000000\"", "paragraph_id": "0001783180-26-000032:facts:InventoryNet:2026-06-30" }
```

```json
{ "id": "earnings_quality_six_month_operating_cash_flow_in_the_filed_facts", "what_changed": "NetCashProvidedByUsedInOperatingActivities for 2026-01-01..2026-06-30 is 1006000000 against 1132000000 for 2025-01-01..2025-06-30. Operating cash from discontinued operations: 53000000 vs 380000000. Capital expenditures (PaymentsToAcquireProductiveAssets): 211000000 vs 144000000.", "account": "operating cash flow (us-gaap:NetCashProvidedByUsedInOperatingActivities)", "expected_direction": "down", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"1006000000\"", "paragraph_id": "0001783180-26-000032:facts:NetCashProvidedByUsedInOperatingActivities:2026-01-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_six_month_continuing_operating_cash_flow_in_the_filed_facts", "what_changed": "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations for 2026-01-01..2026-06-30 is 953000000 against 752000000. Six-month IncreaseDecreaseInAccountsPayableAndAccruedLiabilities: 631000000 vs 378000000.", "account": "operating cash flow from continuing operations (us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations)", "expected_direction": "up", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"953000000\"", "paragraph_id": "0001783180-26-000032:facts:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations:2026-01-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_current_debt_at_quarter_end_in_the_filed_facts", "what_changed": "DebtCurrent at 2026-06-30 is 1638000000 against 468000000 at 2025-12-31 in the same filing. Six-month ProceedsFromRepaymentsOfShortTermDebt: 361000000 vs -57000000. The current portion of long-term debt is 916000000 vs 108000000 (see notes).", "account": "short-term borrowings and current portion of long-term debt (us-gaap:DebtCurrent)", "expected_direction": "up", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"1638000000\"", "paragraph_id": "0001783180-26-000032:facts:DebtCurrent:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_long_term_debt_at_quarter_end_in_the_filed_facts", "what_changed": "LongTermDebtNoncurrent at 2026-06-30 is 10314000000 against 11365000000 at 2025-12-31.", "account": "long-term debt, noncurrent (us-gaap:LongTermDebtNoncurrent)", "expected_direction": "down", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"10314000000\"", "paragraph_id": "0001783180-26-000032:facts:LongTermDebtNoncurrent:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_cash_at_quarter_end_in_the_filed_facts", "what_changed": "CashAndCashEquivalentsAtCarryingValue at 2026-06-30 is 1344000000 against 1555000000 at 2025-12-31 (1797000000 at 2025-06-30). Cash, cash equivalents and restricted cash: 1347000000.", "account": "cash and cash equivalents (us-gaap:CashAndCashEquivalentsAtCarryingValue)", "expected_direction": "down", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"1344000000\"", "paragraph_id": "0001783180-26-000032:facts:CashAndCashEquivalentsAtCarryingValue:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_six_month_share_repurchase_payments_in_the_filed_facts", "what_changed": "PaymentsForRepurchaseOfCommonStock for 2026-01-01..2026-06-30 is 745000000 against 1628000000. Treasury stock acquired in the quarter (equity statement): 446000000 vs 334000000. Six-month common dividends paid: 400000000 vs 390000000; dividends declared per share in the quarter: 0.48 vs 0.45.", "account": "share repurchases (us-gaap:PaymentsForRepurchaseOfCommonStock)", "expected_direction": "down", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"745000000\"", "paragraph_id": "0001783180-26-000032:facts:PaymentsForRepurchaseOfCommonStock:2026-01-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_total_equity_at_quarter_end_in_the_filed_facts", "what_changed": "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest at 2026-06-30 is 13472000000 against 14128000000 at 2025-12-31 (13801000000 at 2026-03-31). Treasury stock: 7550000000 vs 6795000000. AOCI: -537000000 vs -269000000.", "account": "total equity", "expected_direction": "down", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"13472000000\"", "paragraph_id": "0001783180-26-000032:facts:StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest:2026-06-30" }
```

```json
{ "id": "structure_and_disclosure_changes_assets_held_for_sale_at_quarter_end_in_the_filed_facts", "what_changed": "AssetsOfDisposalGroupIncludingDiscontinuedOperationCurrent at 2026-06-30 is 815000000 against 592000000 at 2025-12-31 (0 at 2024-12-31 in the 10-K).", "account": "assets held for sale (us-gaap:AssetsOfDisposalGroupIncludingDiscontinuedOperationCurrent)", "expected_direction": "up", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"815000000\"", "paragraph_id": "0001783180-26-000032:facts:AssetsOfDisposalGroupIncludingDiscontinuedOperationCurrent:2026-06-30" }
```

```json
{ "id": "structure_and_disclosure_changes_liabilities_held_for_sale_at_quarter_end_in_the_filed_facts", "what_changed": "LiabilitiesOfDisposalGroupIncludingDiscontinuedOperationCurrent at 2026-06-30 is 414000000 against 170000000 at 2025-12-31.", "account": "liabilities held for sale (us-gaap:LiabilitiesOfDisposalGroupIncludingDiscontinuedOperationCurrent)", "expected_direction": "up", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"414000000\"", "paragraph_id": "0001783180-26-000032:facts:LiabilitiesOfDisposalGroupIncludingDiscontinuedOperationCurrent:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_goodwill_at_quarter_end_in_the_filed_facts", "what_changed": "Goodwill at 2026-06-30 is 15267000000 against 15501000000 at 2025-12-31. Six-month roll-forward facts: acquired 10000000, transfers -13000000, foreign currency translation -231000000.", "account": "goodwill (us-gaap:Goodwill)", "expected_direction": "down", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"15267000000\"", "paragraph_id": "0001783180-26-000032:facts:Goodwill:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_intangible_assets_at_quarter_end_in_the_filed_facts", "what_changed": "IntangibleAssetsNetExcludingGoodwill at 2026-06-30 is 5756000000 against 6326000000 at 2025-12-31. Customer relationships, net: 4140000000 vs 4570000000.", "account": "intangible assets, net (us-gaap:IntangibleAssetsNetExcludingGoodwill)", "expected_direction": "down", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"5756000000\"", "paragraph_id": "0001783180-26-000032:facts:IntangibleAssetsNetExcludingGoodwill:2026-06-30" }
```

```json
{ "id": "across_documents_quarter_operating_cash_flow_printed_only_in_the_release", "what_changed": "The 8-K prints second-quarter operating cash flow of 927 against 649 (millions), and continuing operating cash flow of 888 against 264. Every operating-cash-flow fact I read in the 10-Q covers a six-month period (1006000000 for 2026-01-01..2026-06-30). The trend table has no quarters-back-0 cell, so no second-quarter accruals figure exists in my input; the three-month cash figure appears only in the release.", "account": "net cash flows provided by operating activities, three months ended 2026-06-30", "expected_direction": "up", "horizon": "next quarter (period ending 2026-09-30)", "quote": "Net cash flows generated from operating activities were $927 million and capital expenditures were $117 million, resulting in free cash flow of $810 million.", "paragraph_id": "0001783180-26-000030:8k_2_02:45" }
```

## Seen in the notes

No fact in input_numbers.json is marked with whether its element sat inside a note. The fields each fact prints are:

- `id`, `paragraph_id`, `tag`, `prefix`, `namespace`, `context`, `context_ref`, `unit`, `decimals`, `value`, `number`, `nil`, `form`, `source_accession`, `filing_date`;
- and, on some facts only, `superseded_by`.

The marker the split depends on therefore does not exist in my input. I placed the items below here by my own reading, not by a marker: each quotes a 10-Q fact that comes after the primary-statement block in the filing's fact order (from `0001783180-26-000032:f-451` onward) and is a disclosure-table element. A reader splitting by the marker should treat this placement as unmarked.

```json
{ "id": "estimates_and_discretion_inventory_valuation_reserve_at_quarter_end_in_the_notes", "what_changed": "InventoryValuationReserves at 2026-06-30 is 328000000. The same filing prints 337000000 at 2025-12-31; the trend input at 2026-03-31 is 345000000 (printed from 0001783180-26-000026). Inventory net is 2759000000. The reserve-to-inventory ratio for this quarter does not exist in my input.", "account": "inventory valuation reserves (us-gaap:InventoryValuationReserves)", "expected_direction": "down", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"328000000\"", "paragraph_id": "0001783180-26-000032:facts:InventoryValuationReserves:2026-06-30" }
```

```json
{ "id": "earnings_quality_finished_goods_inventory_at_quarter_end_in_the_notes", "what_changed": "InventoryFinishedGoodsNetOfReserves at 2026-06-30 is 1793000000 against 1572000000 at 2025-12-31. Raw materials: 690000000 vs 666000000; work in process: 276000000 vs 245000000.", "account": "finished goods inventory (us-gaap:InventoryFinishedGoodsNetOfReserves)", "expected_direction": "up", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"1793000000\"", "paragraph_id": "0001783180-26-000032:facts:InventoryFinishedGoodsNetOfReserves:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_accrual_at_quarter_end_in_the_notes", "what_changed": "ProductWarrantyAccrual at 2026-06-30 is 935000000. The same filing prints 893000000 at 2025-12-31, 862000000 at 2025-06-30 and 786000000 at 2024-12-31; the trend input at 2026-03-31 is 910000000. Six-month warranties issued: 184000000 vs 174000000; settlements: 132000000 vs 129000000. The warranty-to-revenue ratio for this quarter does not exist in my input.", "account": "product warranty accrual (us-gaap:ProductWarrantyAccrual)", "expected_direction": "up", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"935000000\"", "paragraph_id": "0001783180-26-000032:facts:ProductWarrantyAccrual:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_preexisting_estimate_change_in_the_notes", "what_changed": "ProductWarrantyAccrualPreexistingIncreaseDecrease for 2026-01-01..2026-06-30 is -10000000, against 30000000 for 2025-01-01..2025-06-30. The change in estimates for warranties issued before the period is negative this year and was positive last year.", "account": "change in pre-existing warranty estimates (us-gaap:ProductWarrantyAccrualPreexistingIncreaseDecrease)", "expected_direction": "down", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"-10000000\"", "paragraph_id": "0001783180-26-000032:facts:ProductWarrantyAccrualPreexistingIncreaseDecrease:2026-01-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_current_portion_of_long_term_debt_in_the_notes", "what_changed": "LongTermDebtCurrent at 2026-06-30 is 916000000 against 108000000 at 2025-12-31. Total debt (DebtAndCapitalLeaseObligations): 11230000000 vs 11473000000. Revolving credit facility: capacity 2500000000, with 0 drawn at 2026-06-30. Long-term debt fair value at 2026-06-30: 10003000000 against a 10747000000 carrying amount of unsecured debt.", "account": "current portion of long-term debt (us-gaap:LongTermDebtCurrent)", "expected_direction": "up", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"916000000\"", "paragraph_id": "0001783180-26-000032:facts:LongTermDebtCurrent:2026-06-30" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_related_party_receivables_in_the_notes", "what_changed": "ReceivablesNetCurrent with RelatedPartyMember at 2026-06-30 is 396000000 against 220000000 at 2025-12-31; the Q1 10-Q printed 290000000 at 2026-03-31. Related-party payables: 31000000 vs 40000000.", "account": "related-party receivables", "expected_direction": "up", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"396000000\"", "paragraph_id": "0001783180-26-000032:facts:ReceivablesNetCurrent:2026-06-30:us-gaap:RelatedPartyTransactionsByRelatedPartyAxis=us-gaap:RelatedPartyMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_related_party_product_revenue_in_the_notes", "what_changed": "Product revenue with RelatedPartyMember for 2026-04-01..2026-06-30 is 951000000 against 845000000; six months 1637000000 vs 1625000000. The related-party cost of goods for the quarter is 59000000 vs 57000000.", "account": "related-party product revenue", "expected_direction": "up", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"951000000\"", "paragraph_id": "0001783180-26-000032:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:ProductOrServiceAxis=us-gaap:ProductMember,us-gaap:RelatedPartyTransactionsByRelatedPartyAxis=us-gaap:RelatedPartyMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_asbestos_accrual_in_the_notes", "what_changed": "LossContingencyAccrualAtCarryingValue for asbestos matters at 2026-06-30 is 209000000 against 218000000 at 2025-12-31 (212000000 at 2026-03-31 in the Q1 10-Q). Current portion 17000000 in both periods; noncurrent 192000000 vs 201000000.", "account": "asbestos loss accrual", "expected_direction": "down", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"209000000\"", "paragraph_id": "0001783180-26-000032:facts:LossContingencyAccrualAtCarryingValue:2026-06-30:us-gaap:LossContingenciesByNatureOfContingencyAxis=carr:AsbestosMattersMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_asbestos_insurance_receivable_in_the_notes", "what_changed": "LossContingencyReceivable for asbestos matters at 2026-06-30 is 89000000 against 92000000 at 2025-12-31 (91000000 at 2026-03-31). Current 6000000 in both periods; noncurrent 83000000 vs 86000000.", "account": "asbestos insurance receivable", "expected_direction": "down", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"89000000\"", "paragraph_id": "0001783180-26-000032:facts:LossContingencyReceivable:2026-06-30:us-gaap:LossContingenciesByNatureOfContingencyAxis=carr:AsbestosMattersMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_environmental_accrual_in_the_notes", "what_changed": "AccrualForEnvironmentalLossContingencies at 2026-06-30 is 200000000, the same as at 2025-12-31 (198000000 at 2026-03-31 in the Q1 10-Q). Current 20000000 vs 18000000; noncurrent 180000000 vs 182000000.", "account": "environmental loss accrual", "expected_direction": "none", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"200000000\"", "paragraph_id": "0001783180-26-000032:facts:AccrualForEnvironmentalLossContingencies:2026-06-30" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_foam_litigation_insurance_recoveries_in_the_notes", "what_changed": "EstimatedInsuranceRecoveries for pending aqueous film forming foam litigation is 2400000000 at 2026-06-30, the same value the Q1 10-Q printed at 2026-03-31. The 10-Q also re-prints this litigation's accrual facts at earlier dates: 565000000 at 2024-12-31 and 50000000 at 2023-05-14.", "account": "insurance recoveries for aqueous film forming foam litigation", "expected_direction": "none", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"2400000000\"", "paragraph_id": "0001783180-26-000032:facts:EstimatedInsuranceRecoveries:2026-06-30:srt:LitigationCaseAxis=carr:AqueousFilmFormingFoamMember,us-gaap:LitigationStatusAxis=us-gaap:PendingLitigationMember" }
```

```json
{ "id": "structure_and_disclosure_changes_riello_disposal_consideration_in_the_notes", "what_changed": "DisposalGroupIncludingDiscontinuedOperationConsideration for the Riello business (held for sale, not a discontinued operation) is 430000000 at 2025-12-16. The 8-K says the Riello divestiture completed on July 1, 2026.", "account": "Riello disposal consideration", "expected_direction": "none", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"430000000\"", "paragraph_id": "0001783180-26-000032:facts:DisposalGroupIncludingDiscontinuedOperationConsideration:2025-12-16:us-gaap:DisposalGroupClassificationAxis=us-gaap:DisposalGroupHeldforsaleNotDiscontinuedOperationsMember,us-gaap:IncomeStatementBalanceSheetAndAdditionalDisclosuresByDisposalGroupsIncludingDiscontinuedOperationsAxis=carr:RielloBusinessMember" }
```

```json
{ "id": "estimates_and_discretion_europe_goodwill_translation_in_the_notes", "what_changed": "GoodwillForeignCurrencyTranslationGainLoss for Climate Solutions Europe for 2026-01-01..2026-06-30 is -219000000 (all segments -231000000). Climate Solutions Europe goodwill is 7586000000 at 2026-06-30 against 7808000000 at 2025-12-31.", "account": "goodwill foreign currency translation, Climate Solutions Europe", "expected_direction": "down", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"-219000000\"", "paragraph_id": "0001783180-26-000032:facts:GoodwillForeignCurrencyTranslationGainLoss:2026-01-01..2026-06-30:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=carr:ClimateSolutionsEuropeSegmentMember" }
```

```json
{ "id": "revenue_recognition_united_states_quarter_revenue_in_the_notes", "what_changed": "Revenue with country:US for 2026-04-01..2026-06-30 is 3536000000 against 3429000000. Europe: 1581000000 vs 1520000000. Asia Pacific: 1029000000 vs 981000000. Other: 205000000 vs 183000000.", "account": "revenue by geography, United States", "expected_direction": "up", "horizon": "next quarter (period ending 2026-09-30)", "quote": "\"value\": \"3536000000\"", "paragraph_id": "0001783180-26-000032:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:StatementGeographicalAxis=country:US" }
```

The trend table uses ContractWithCustomerLiabilityCurrent at 2026-03-31 (722000000). I found no contract-liability fact for 2026-06-30 in the lines of input_numbers.json I read. That is a statement about my reading, not about whether such a fact exists in the lines I did not read.
