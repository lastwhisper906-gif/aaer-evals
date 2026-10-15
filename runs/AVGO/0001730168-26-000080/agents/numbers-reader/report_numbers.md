# AVGO — numbers reader — 10-Q 0001730168-26-000080 (quarter ended 2026-08-02)

## Before the items

**Input check.** My directory holds `input_8k.md`, `input_numbers.json`, `input_prior_predictions.md` and `input_trends.json`. None of them holds prices, abnormal returns, short interest, another company's files, a prior run's probability or an outcome window. `input_prior_predictions.md` says there are no earlier flags for this company.

**Inputs the brief names that are not in my directory.** I have no articulation checks, no restatement traces and no fourth-quarter derivation output. `input_numbers.json` holds only `ticker`, `cutoff`, `documents` (10-K 0001730168-25-000121, 10-Q 0001730168-26-000054, 10-Q 0001730168-26-000080) and `facts`. So there are no articulation-gap items and no restatement-trace items below: there is nothing to quote for them. A Python restatement trace does not exist in my input, so I report no restated prior value. The fact items below that carry `superseded_by` are re-reports whose later value my input prints as the same figure.

**Periods the record does not reach.** `quarters-back-3` (target end 2025-11-02) and `quarters-back-7` (target end 2024-11-03) have no cells. The reason `quarters-back-3` gives: "no quarter ending within 20 days of 2025-11-02 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py". `quarters-back-7` gives the same reason for 2024-11-03. The output of that derivation is not in my directory. Every quarter-over-quarter change that would compare against either of these quarters is printed as not filled.

**Formula baseline with no quotable id.** The years-back-0 research-and-development capitalisation baseline prints `earnings_with_rnd_capitalized` 28242200000.0, `research_and_development_asset` 24515200000.0 and `research_and_development_amortization` 5860800000.0, but it prints no `paragraph_id`. So it gets no item. Its `book_value_with_rnd_capitalized` is missing ("no row for stockholders_equity in 2025-11-02: us-gaap:StockholdersEquity is in the record, but not for this period"), and `capitalized_development_cost` and `capitalized_over_expense` are missing because the record tags no us-gaap:CapitalizedComputerSoftwareAdditions.

**8-K lists with no ids.** The 8-K file's item-code list and its late-filing list print no paragraph ids, so I quote nothing from them. The late-filing list reads "none on or before 2026-09-10".

**How `expected_direction` is used here.** It gives the sign of the change my input prints for the item. For trend cells that is the year-over-year change, and the quarter-over-quarter change is given in `what_changed`. For release figures it is the company's own stated change. Where no comparable change is printed it is `none`. It is a reading of the printed sign, not a forecast I worked out.

**Note marker.** No fact I read prints a field saying whether its element sat inside a note. Each fact prints `id`, `paragraph_id`, `tag`, `prefix`, `namespace`, `context`, `context_ref`, `unit`, `decimals`, `value`, `number`, `nil`, `form`, `source_accession`, `filing_date`, and on some facts `superseded_by`. The brief puts the numeric facts under "Seen in the statements", and nothing marks any fact as coming from a note. So every fact item sits under that heading, and each fact item says the marker is absent. The later notes split cannot rely on my placement for those items.

**Coverage of the numbers file.** `input_numbers.json` is 83,360 lines (about 1.2 million tokens), more than I could hold, so I did not read every fact. I read lines 1–300 (documents and the opening 10-K 0001730168-25-000121 facts), 40,000–40,200 (10-Q 0001730168-26-000054 cash-flow facts), 62,000–62,200 (10-Q 0001730168-26-000080 income-statement facts), 80,000–80,050 and 82,300–83,360 (the closing 10-Q 0001730168-26-000080 facts). A fact outside those lines is not reported. I make no claim that such facts carry no restated value, no note marker and nothing else worth an item. The trend table, the 8-K and the prior-predictions file were read in full.

## Seen in the statements

### Trend table — quarters-back-0 (2026-05-04..2026-08-02)

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarterly_trend_cell",
  "what_changed": "receivables_over_revenue for 2026-05-04..2026-08-02 is 0.4632151667736812 (AccountsReceivableNetCurrent 13707000000.0 over revenue 29591000000.0). Change against quarters-back-1: -0.024908509252820843. Change against quarters-back-4: 0.056118877907081366. Position: second highest of the 6 filled quarters.",
  "account": "AccountsReceivableNetCurrent over RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"",
  "paragraph_id": "0001730168-26-000080:trends:receivables_over_revenue:2026-05-04..2026-08-02" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly_trend_cell",
  "what_changed": "days_sales_outstanding for 2026-05-04..2026-08-02 (91 days) is 42.15258017640499 (receivables 13707000000.0, revenue 29591000000.0). Change against quarters-back-1: -2.266674342006695. Change against quarters-back-4: 5.106817889544402. Position: second highest of the 6 filled quarters.",
  "account": "AccountsReceivableNetCurrent over RevenueFromContractWithCustomerExcludingAssessedTax, times days in period",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"",
  "paragraph_id": "0001730168-26-000080:trends:days_sales_outstanding:2026-05-04..2026-08-02" }
```

```json
{ "id": "estimates_and_discretion_days_sales_of_inventory_quarterly_trend_cell",
  "what_changed": "days_sales_of_inventory for 2026-05-04..2026-08-02 is 45.056704980842916 (InventoryNet 4523000000.0 over CostOfRevenue 9135000000.0). Change against quarters-back-1: -13.101593896888922. Change against quarters-back-4: 7.26283948265278. Position: second highest of the 6 filled quarters. The CostOfRevenue input is the same figure the release prints as 'Total cost of revenue' (9,135), a line that includes amortization of acquisition-related intangibles and restructuring.",
  "account": "InventoryNet over CostOfRevenue, times days in period",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"",
  "paragraph_id": "0001730168-26-000080:trends:days_sales_of_inventory:2026-05-04..2026-08-02" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly_trend_cell",
  "what_changed": "gross_margin for 2026-05-04..2026-08-02 is 0.6912912709945591 (revenue 29591000000.0, CostOfRevenue 9135000000.0). Change against quarters-back-1: -0.0034849493146309474. Change against quarters-back-4: 0.020340919941399638. Position: second highest of the 6 filled quarters.",
  "account": "RevenueFromContractWithCustomerExcludingAssessedTax and CostOfRevenue",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"",
  "paragraph_id": "0001730168-26-000080:trends:gross_margin:2026-05-04..2026-08-02" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly_trend_cell",
  "what_changed": "contract_liabilities_over_revenue for 2026-05-04..2026-08-02 is 0.3210773546010611 (ContractWithCustomerLiabilityCurrent 9501000000.0 over revenue 29591000000.0). Change against quarters-back-1: -0.1313497423476025. Change against quarters-back-4: -0.32492314690345236. Position: lowest of the 6 filled quarters. The input is the current contract liability only.",
  "account": "ContractWithCustomerLiabilityCurrent over RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001730168-26-000080:trends:contract_liabilities_over_revenue:2026-05-04..2026-08-02" }
```

```json
{ "id": "earnings_quality_soft_asset_share_quarterly_trend_cell",
  "what_changed": "soft_asset_share at 2026-08-02 is 0.855863469183834 (Assets 188148000000.0, PropertyPlantAndEquipmentNet 3144000000.0, CashAndCashEquivalentsAtCarryingValue 23975000000.0). Change against quarters-back-1: -0.019017920427570445. Change against quarters-back-4: -0.06462366710926892. Position: lowest of the 6 filled quarters.",
  "account": "Assets less PropertyPlantAndEquipmentNet less CashAndCashEquivalentsAtCarryingValue, over Assets",
  "expected_direction": "down",
  "horizon": "next quarterly filing",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001730168-26-000080:trends:soft_asset_share:2026-05-04..2026-08-02" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly_trend_cell_insufficient",
  "what_changed": "insufficient: the table could not fill accruals_over_total_assets for 2026-05-04..2026-08-02 because the record has no three-month operating cash flow row for the period. It prints no value and no change. This ratio has 2 filled quarters in the whole table (quarters-back-2 and quarters-back-6), which does not support a trend claim.",
  "account": "NetCashProvidedByUsedInOperatingActivities (three-month), ProfitLoss, Assets",
  "expected_direction": "none",
  "horizon": "none: insufficient",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-05-04..2026-08-02: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0001730168-26-000080:trends:accruals_over_total_assets:2026-05-04..2026-08-02" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly_trend_cell_insufficient",
  "what_changed": "insufficient: bad_debt_reserve_ratio is not filled for 2026-05-04..2026-08-02. The companyfacts record tags no allowance-for-credit-loss concept in any period, so no value and no change exist. The ratio is filled in 0 periods of the table.",
  "account": "allowance for credit losses on trade receivables",
  "expected_direction": "none",
  "horizon": "none: insufficient",
  "quote": "\"missing\": \"no row for bad_debt_allowance: the companyfacts record tags none of us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable in any period",
  "paragraph_id": "0001730168-26-000080:trends:bad_debt_reserve_ratio:2026-05-04..2026-08-02" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly_trend_cell_insufficient",
  "what_changed": "insufficient: inventory_reserve_ratio is not filled for 2026-05-04..2026-08-02. The record tags no us-gaap:InventoryValuationReserves in any period, so no value and no change exist. The ratio is filled in 0 periods of the table.",
  "account": "inventory valuation reserve",
  "expected_direction": "none",
  "horizon": "none: insufficient",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period",
  "paragraph_id": "0001730168-26-000080:trends:inventory_reserve_ratio:2026-05-04..2026-08-02" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly_trend_cell_insufficient",
  "what_changed": "insufficient: warranty_reserve_ratio is not filled for 2026-05-04..2026-08-02. The record tags none of the three product-warranty accrual concepts in any period, so no value and no change exist. The ratio is filled in 0 periods of the table.",
  "account": "product warranty accrual",
  "expected_direction": "none",
  "horizon": "none: insufficient",
  "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period",
  "paragraph_id": "0001730168-26-000080:trends:warranty_reserve_ratio:2026-05-04..2026-08-02" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly_trend_cell_insufficient",
  "what_changed": "insufficient: non_gaap_gap is not filled for 2026-05-04..2026-08-02 because no us-gaap concept carries a non-GAAP measure. The release prints GAAP and non-GAAP figures (see the release item on non-GAAP measures), but no gap computed by Python exists in my input. The ratio is filled in 0 periods of the table.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "none: insufficient",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001730168-26-000080:trends:non_gaap_gap:2026-05-04..2026-08-02" }
```

### Trend table — years-back-0 (2024-11-04..2025-11-02)

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual_trend_cell",
  "what_changed": "receivables_over_revenue for 2024-11-04..2025-11-02 is 0.11183808912611329 (AccountsReceivableNetCurrent 7145000000.0 at 2025-11-02 over revenue 63887000000.0). Change against years-back-1: 0.02621354962946769. Position: highest of the 5 filled years.",
  "account": "AccountsReceivableNetCurrent over RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "up",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001730168-26-000080:trends:receivables_over_revenue:2024-11-04..2025-11-02" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual_trend_cell",
  "what_changed": "days_sales_outstanding for 2024-11-04..2025-11-02 (364 days) is 40.709064441905234 (receivables 7145000000.0, revenue 63887000000.0). Change against years-back-1: 8.942360288649716. Position: highest of the 5 filled years.",
  "account": "AccountsReceivableNetCurrent over RevenueFromContractWithCustomerExcludingAssessedTax, times days in period",
  "expected_direction": "up",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001730168-26-000080:trends:days_sales_outstanding:2024-11-04..2025-11-02" }
```

```json
{ "id": "estimates_and_discretion_days_sales_of_inventory_annual_trend_cell",
  "what_changed": "days_sales_of_inventory for 2024-11-04..2025-11-02 is 40.12431408731122 (InventoryNet 2270000000.0 over CostOfRevenue 20593000000.0). Change against years-back-1: 5.875166434544369. Position: second lowest of the 5 filled years.",
  "account": "InventoryNet over CostOfRevenue, times days in period",
  "expected_direction": "up",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001730168-26-000080:trends:days_sales_of_inventory:2024-11-04..2025-11-02" }
```

```json
{ "id": "earnings_quality_gross_margin_annual_trend_cell",
  "what_changed": "gross_margin for 2024-11-04..2025-11-02 is 0.6776652527118193 (revenue 63887000000.0, CostOfRevenue 20593000000.0). Change against years-back-1: 0.047328261204470645. Position: second highest of the 5 filled years.",
  "account": "RevenueFromContractWithCustomerExcludingAssessedTax and CostOfRevenue",
  "expected_direction": "up",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001730168-26-000080:trends:gross_margin:2024-11-04..2025-11-02" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual_trend_cell",
  "what_changed": "contract_liabilities_over_revenue for 2024-11-04..2025-11-02 is 0.14821481678588758 (ContractWithCustomerLiabilityCurrent 9469000000.0 at 2025-11-02 over revenue 63887000000.0). Change against years-back-1: -0.03395061540862904. Position: second highest of the 5 filled years.",
  "account": "ContractWithCustomerLiabilityCurrent over RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "down",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001730168-26-000080:trends:contract_liabilities_over_revenue:2024-11-04..2025-11-02" }
```

```json
{ "id": "earnings_quality_soft_asset_share_annual_trend_cell",
  "what_changed": "soft_asset_share at 2025-11-02 is 0.890655319944825 (Assets 171092000000.0, PropertyPlantAndEquipmentNet 2530000000.0, cash 16178000000.0). Change against years-back-1: -0.037691445728753936. Position: second highest of the 5 filled years.",
  "account": "Assets less PropertyPlantAndEquipmentNet less CashAndCashEquivalentsAtCarryingValue, over Assets",
  "expected_direction": "down",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001730168-26-000080:trends:soft_asset_share:2024-11-04..2025-11-02" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_annual_trend_cell",
  "what_changed": "accruals_over_total_assets for 2024-11-04..2025-11-02 is -0.025781450915297034 (ProfitLoss 23126000000.0, operating cash flow 27537000000.0, Assets 171092000000.0). The table prints no change against years-back-1, because net income rests on us-gaap:ProfitLoss here and on us-gaap:NetIncomeLoss in years-back-1. Position: highest of the 2 filled years on the same concepts; 3 other filled years rest on a different concept and are not compared. With 2 comparable years, this is insufficient for a trend claim.",
  "account": "ProfitLoss less NetCashProvidedByUsedInOperatingActivities, over Assets",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "\"position_in_history\": \"highest of the 2 filled years on the same concepts; 3 other filled years rest on a different concept and are not compared\"",
  "paragraph_id": "0001730168-26-000080:trends:accruals_over_total_assets:2024-11-04..2025-11-02" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual_trend_cell_insufficient",
  "what_changed": "insufficient: bad_debt_reserve_ratio is not filled for 2024-11-04..2025-11-02. The record tags no allowance-for-credit-loss concept in any period, so no value and no change exist.",
  "account": "allowance for credit losses on trade receivables",
  "expected_direction": "none",
  "horizon": "none: insufficient",
  "quote": "\"missing\": \"no row for bad_debt_allowance: the companyfacts record tags none of us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable in any period",
  "paragraph_id": "0001730168-26-000080:trends:bad_debt_reserve_ratio:2024-11-04..2025-11-02" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_annual_trend_cell_insufficient",
  "what_changed": "insufficient: inventory_reserve_ratio is not filled for 2024-11-04..2025-11-02. The record tags no us-gaap:InventoryValuationReserves in any period, so no value and no change exist.",
  "account": "inventory valuation reserve",
  "expected_direction": "none",
  "horizon": "none: insufficient",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period",
  "paragraph_id": "0001730168-26-000080:trends:inventory_reserve_ratio:2024-11-04..2025-11-02" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_annual_trend_cell_insufficient",
  "what_changed": "insufficient: warranty_reserve_ratio is not filled for 2024-11-04..2025-11-02. The record tags none of the three product-warranty accrual concepts in any period, so no value and no change exist.",
  "account": "product warranty accrual",
  "expected_direction": "none",
  "horizon": "none: insufficient",
  "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period",
  "paragraph_id": "0001730168-26-000080:trends:warranty_reserve_ratio:2024-11-04..2025-11-02" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual_trend_cell_insufficient",
  "what_changed": "insufficient: non_gaap_gap is not filled for 2024-11-04..2025-11-02 because no us-gaap concept carries a non-GAAP measure. No value and no change exist.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "none: insufficient",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001730168-26-000080:trends:non_gaap_gap:2024-11-04..2025-11-02" }
```

### Changes of tag

```json
{ "id": "articulation_and_the_filed_history_net_income_tag_profit_loss_against_net_income_loss",
  "what_changed": "change of tag: in the accruals_over_total_assets cell for 2024-11-04..2025-11-02, net income rests on us-gaap:ProfitLoss in years-back-0 and on us-gaap:NetIncomeLoss in years-back-1, so the table prints no year-over-year change. Of the 5 filled years, 2 rest on the years-back-0 concepts and 3 on a different concept.",
  "account": "net income (ProfitLoss / NetIncomeLoss)",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "\"reason\": \"accruals_over_total_assets rests on a different concept in each period, so the difference would not be a change",
  "paragraph_id": "0001730168-26-000080:trends:accruals_over_total_assets:2024-11-04..2025-11-02" }
```

```json
{ "id": "articulation_and_the_filed_history_net_income_tag_net_income_loss_against_profit_loss",
  "what_changed": "change of tag: in the accruals_over_total_assets cell for 2021-11-01..2022-10-30, net income rests on us-gaap:NetIncomeLoss in years-back-3 and on us-gaap:ProfitLoss in years-back-4, so the table prints no change between them. Read with the item above, the filed annual history moves from ProfitLoss (years-back-4) to NetIncomeLoss (years-back-3 to years-back-1) and back to ProfitLoss (years-back-0).",
  "account": "net income (ProfitLoss / NetIncomeLoss)",
  "expected_direction": "none",
  "horizon": "next annual filing",
  "quote": "\"reason\": \"accruals_over_total_assets rests on a different concept in each period, so the difference would not be a change",
  "paragraph_id": "0001730168-26-000080:trends:accruals_over_total_assets:2021-11-01..2022-10-30" }
```

### Numeric facts

```json
{ "id": "articulation_and_the_filed_history_cash_superseded_unchanged_tagged_fact",
  "what_changed": "The 10-K fact for cash at 2025-11-02 (16178000000) is marked superseded by 10-Q 0001730168-26-000080. The trend table's years-back-0 cash input, taken from 0001730168-26-000080, prints 16178000000.0, the same figure. This is a re-report, not a restatement. The fact prints no in-note marker.",
  "account": "CashAndCashEquivalentsAtCarryingValue",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"superseded_by\": \"0001730168-26-000080\"",
  "paragraph_id": "0001730168-25-000121:facts:CashAndCashEquivalentsAtCarryingValue:2025-11-02" }
```

```json
{ "id": "articulation_and_the_filed_history_receivables_superseded_unchanged_tagged_fact",
  "what_changed": "The 10-K fact for trade receivables at 2025-11-02 (7145000000) is marked superseded by 10-Q 0001730168-26-000080. The trend table's years-back-0 receivables input from 0001730168-26-000080 prints 7145000000.0, the same figure. This is a re-report, not a restatement. The fact prints no in-note marker.",
  "account": "AccountsReceivableNetCurrent",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"superseded_by\": \"0001730168-26-000080\"",
  "paragraph_id": "0001730168-25-000121:facts:AccountsReceivableNetCurrent:2025-11-02" }
```

```json
{ "id": "articulation_and_the_filed_history_inventory_superseded_unchanged_tagged_fact",
  "what_changed": "The 10-K fact for inventory at 2025-11-02 (2270000000) is marked superseded by 10-Q 0001730168-26-000080. The trend table's years-back-0 inventory input from 0001730168-26-000080 prints 2270000000.0, the same figure. This is a re-report, not a restatement. The fact prints no in-note marker.",
  "account": "InventoryNet",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"superseded_by\": \"0001730168-26-000080\"",
  "paragraph_id": "0001730168-25-000121:facts:InventoryNet:2025-11-02" }
```

```json
{ "id": "articulation_and_the_filed_history_other_current_assets_superseded_unchanged_tagged_fact",
  "what_changed": "The 10-K fact for other current assets at 2025-11-02 (5980000000) is marked superseded by 10-Q 0001730168-26-000080. The release balance sheet prints other current assets at November 2, 2025 of 5,980 (in millions), the same figure. No restatement is shown. The fact prints no in-note marker.",
  "account": "OtherAssetsCurrent",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"superseded_by\": \"0001730168-26-000080\"",
  "paragraph_id": "0001730168-25-000121:facts:OtherAssetsCurrent:2025-11-02" }
```

```json
{ "id": "articulation_and_the_filed_history_current_assets_superseded_unchanged_tagged_fact",
  "what_changed": "The 10-K fact for total current assets at 2025-11-02 (31573000000) is marked superseded by 10-Q 0001730168-26-000080. The release balance sheet prints total current assets at November 2, 2025 of 31,573 (in millions), the same figure. No restatement is shown. The fact prints no in-note marker.",
  "account": "AssetsCurrent",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"superseded_by\": \"0001730168-26-000080\"",
  "paragraph_id": "0001730168-25-000121:facts:AssetsCurrent:2025-11-02" }
```

```json
{ "id": "estimates_and_discretion_income_tax_holiday_amount_tagged_fact",
  "what_changed": "The 10-K tags an income tax holiday aggregate amount of 2709000000 for 2024-11-04..2025-11-02, on the IncomeTaxAuthorityAxis member DomesticCountryMember. No other period of this fact is in what I read, so it is insufficient for a trend claim. The fact prints no in-note marker.",
  "account": "IncomeTaxHolidayAggregateDollarAmount",
  "expected_direction": "none",
  "horizon": "none: insufficient",
  "quote": "\"value\": \"2709000000\"",
  "paragraph_id": "0001730168-25-000121:facts:IncomeTaxHolidayAggregateDollarAmount:2024-11-04..2025-11-02:us-gaap:IncomeTaxAuthorityAxis=us-gaap:DomesticCountryMember" }
```

```json
{ "id": "earnings_quality_stock_based_compensation_expense_tagged_fact",
  "what_changed": "Share-based compensation for 2026-05-04..2026-08-02 is 2019000000. The same-quarter prior-year fact (2025-05-05..2025-08-03) prints 2322000000. The year-to-date facts print 6287000000 (2025-11-03..2026-08-02) and 5373000000 (2024-11-04..2025-08-03). My input computes no change for these. The fact prints no in-note marker.",
  "account": "AllocatedShareBasedCompensationExpense",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"2019000000\"",
  "paragraph_id": "0001730168-26-000080:facts:AllocatedShareBasedCompensationExpense:2026-05-04..2026-08-02" }
```

```json
{ "id": "earnings_quality_restructuring_and_impairment_charges_tagged_fact",
  "what_changed": "Restructuring costs and asset impairment charges for 2026-05-04..2026-08-02 are 115000000. The same-quarter prior-year fact prints 213000000. The year-to-date facts print 312000000 and 513000000. My input computes no change. The fact prints no in-note marker.",
  "account": "RestructuringCostsAndAssetImpairmentCharges",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"115000000\"",
  "paragraph_id": "0001730168-26-000080:facts:RestructuringCostsAndAssetImpairmentCharges:2026-05-04..2026-08-02" }
```

```json
{ "id": "earnings_quality_acquisition_related_costs_tagged_fact",
  "what_changed": "Business-combination acquisition-related costs for 2026-05-04..2026-08-02 are 0. The same-quarter prior-year fact prints 7000000. The year-to-date facts print 2000000 (2025-11-03..2026-08-02) and 204000000 (2024-11-04..2025-08-03). My input computes no change. The fact prints no in-note marker.",
  "account": "BusinessCombinationAcquisitionRelatedCosts",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"0\"",
  "paragraph_id": "0001730168-26-000080:facts:BusinessCombinationAcquisitionRelatedCosts:2026-05-04..2026-08-02" }
```

```json
{ "id": "earnings_quality_amortization_of_intangible_assets_tagged_fact",
  "what_changed": "Amortization of intangible assets for 2026-05-04..2026-08-02 is 2006000000. The same-quarter prior-year fact prints 2026000000. The year-to-date facts print 5942000000 and 6010000000. My input computes no change. The fact prints no in-note marker.",
  "account": "AmortizationOfIntangibleAssets",
  "expected_direction": "none",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"2006000000\"",
  "paragraph_id": "0001730168-26-000080:facts:AmortizationOfIntangibleAssets:2026-05-04..2026-08-02" }
```

```json
{ "id": "results_against_expectations_operating_income_tagged_fact",
  "what_changed": "Operating income for 2026-05-04..2026-08-02 is 15955000000. The same-quarter prior-year fact prints 5887000000. The year-to-date facts print 35306000000 and 17976000000. The release prints the quarterly change as +171%. The fact prints no in-note marker.",
  "account": "OperatingIncomeLoss",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "\"value\": \"15955000000\"",
  "paragraph_id": "0001730168-26-000080:facts:OperatingIncomeLoss:2026-05-04..2026-08-02" }
```

```json
{ "id": "across_documents_segment_research_expense_matches_release_non_gaap_line_tagged_fact",
  "what_changed": "The 10-Q tags research and development of 1551000000 for 2026-05-04..2026-08-02 on the StatementBusinessSegmentsAxis member SemiconductorSolutionsAndInfrastructureSoftwareMember. The release prints 'Research and development on non-GAAP basis' of 1,551 (in millions) for the same quarter, while GAAP research and development is 2,895. The segment-axis SG&A fact likewise prints 545000000, against the release's non-GAAP SG&A of 545. So the segment-tagged expense figures carry the release's non-GAAP amounts, not the GAAP lines. The fact prints no in-note marker.",
  "account": "ResearchAndDevelopmentExpense (segment axis)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"1551000000\"",
  "paragraph_id": "0001730168-26-000080:facts:ResearchAndDevelopmentExpense:2026-05-04..2026-08-02:us-gaap:StatementBusinessSegmentsAxis=avgo:SemiconductorSolutionsAndInfrastructureSoftwareMember" }
```

```json
{ "id": "liquidity_and_capital_unrecorded_purchase_obligations_tagged_fact",
  "what_changed": "Unrecorded unconditional purchase obligations at 2026-08-02 total 126821000000. By year: remainder of fiscal year 1110000000, first anniversary 52674000000, second 72952000000, third 85000000, fourth 0. No earlier period of this fact is in what I read, and my input computes no change, so it is insufficient for a trend claim. The fact prints no in-note marker.",
  "account": "UnrecordedUnconditionalPurchaseObligationBalanceSheetAmount",
  "expected_direction": "none",
  "horizon": "none: insufficient",
  "quote": "\"value\": \"126821000000\"",
  "paragraph_id": "0001730168-26-000080:facts:UnrecordedUnconditionalPurchaseObligationBalanceSheetAmount:2026-08-02" }
```

```json
{ "id": "liquidity_and_capital_other_commitments_tagged_fact",
  "what_changed": "Other commitments at 2026-08-02 total 3941000000. By year: remainder of fiscal year 313000000, next twelve months 758000000, second year 778000000, third year 904000000, fourth year 303000000. No earlier period is in what I read, so it is insufficient for a trend claim. The fact prints no in-note marker.",
  "account": "OtherCommitment",
  "expected_direction": "none",
  "horizon": "none: insufficient",
  "quote": "\"value\": \"3941000000\"",
  "paragraph_id": "0001730168-26-000080:facts:OtherCommitment:2026-08-02" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_guarantee_maximum_exposure_tagged_fact",
  "what_changed": "Guarantee obligations' maximum exposure at 2026-08-02 is 29000000000 (decimals -8). No earlier period is in what I read, so it is insufficient for a trend claim. The fact prints no in-note marker.",
  "account": "GuaranteeObligationsMaximumExposure",
  "expected_direction": "none",
  "horizon": "none: insufficient",
  "quote": "\"value\": \"29000000000\"",
  "paragraph_id": "0001730168-26-000080:facts:GuaranteeObligationsMaximumExposure:2026-08-02" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_dividend_declared_tagged_fact",
  "what_changed": "A dividend of 0.65 per share is tagged as declared for 2026-09-01, on the SubsequentEventMember. The release says the dividend is payable on September 30, 2026 to holders of record on September 21, 2026. The fact prints no in-note marker.",
  "account": "CommonStockDividendsPerShareDeclared (SubsequentEventMember)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"0.65\"",
  "paragraph_id": "0001730168-26-000080:facts:CommonStockDividendsPerShareDeclared:2026-09-01..2026-09-01:us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

### Earnings release figures (8-K 0001730168-26-000076)

```json
{ "id": "results_against_expectations_reported_revenue_growth_release_figure",
  "what_changed": "The release prints third-quarter revenue of $29.6 billion, up 86 percent from the prior-year period. Its statement of operations prints net revenue of 29,591 against 15,952 (in millions).",
  "account": "net revenue",
  "expected_direction": "up",
  "horizon": "next quarterly filing",
  "quote": "Revenue of $29.6 billion for the third quarter, up 86 percent from the prior year period",
  "paragraph_id": "0001730168-26-000076:8k_2_02:5" }
```

```json
{ "id": "results_against_expectations_revenue_guidance_release_figure",
  "what_changed": "The company guides revenue for the quarter ending November 1, 2026 to approximately $34.8 billion. The release states this as an increase of 93 percent from the prior-year period. That quarter is a fiscal fourth quarter, which the trend table can reach only through the fourth-quarter derivation that is not in my directory.",
  "account": "net revenue",
  "expected_direction": "up",
  "horizon": "quarter ending November 1, 2026",
  "quote": "Fourth quarter revenue guidance of approximately $34.8 billion",
  "paragraph_id": "0001730168-26-000076:8k_2_02:28" }
```

```json
{ "id": "results_against_expectations_non_gaap_operating_margin_guidance_release_figure",
  "what_changed": "The company guides non-GAAP operating income for the quarter ending November 1, 2026 to approximately 66 percent of projected revenue. The CFO calls this flat from a year ago. The release says it cannot reconcile projected non-GAAP measures to GAAP without unreasonable effort.",
  "account": "non-GAAP operating income",
  "expected_direction": "none",
  "horizon": "quarter ending November 1, 2026",
  "quote": "Fourth quarter non-GAAP operating income guidance of approximately 66 percent of projected revenue",
  "paragraph_id": "0001730168-26-000076:8k_2_02:29" }
```

```json
{ "id": "results_against_expectations_ai_semiconductor_revenue_outlook_release_figure",
  "what_changed": "The CEO prints third-quarter AI semiconductor revenue of $16.7 billion (221% year-over-year, 54% quarter-over-quarter) and expects $21.7 billion next quarter, up 236% year-over-year. No tagged fact in what I read carries AI semiconductor revenue, so no Python figure checks it.",
  "account": "AI semiconductor revenue (release only)",
  "expected_direction": "up",
  "horizon": "quarter ending November 1, 2026",
  "quote": "we expect AI semiconductor revenue to accelerate to $21.7 billion, up 236% year-over-year",
  "paragraph_id": "0001730168-26-000076:8k_2_02:13" }
```

```json
{ "id": "earnings_quality_non_gaap_measures_release_figure",
  "what_changed": "The release prints GAAP diluted EPS of $2.68 and non-GAAP diluted EPS of $3.32 for the quarter. Its reconciliation prints GAAP net income of 13,088 and non-GAAP net income of 16,372 (in millions). The adjustments are amortization of intangibles, stock-based compensation, restructuring, acquisition costs, loss on debt extinguishment and non-GAAP tax reconciling adjustments of (931). The trend table's non_gaap_gap is insufficient (no us-gaap concept), and no gap computed by Python exists in my input.",
  "account": "non-GAAP net income and EPS",
  "expected_direction": "none",
  "horizon": "none: insufficient",
  "quote": "GAAP diluted EPS of $2.68 for the third quarter; Non-GAAP diluted EPS of $3.32 for the third quarter",
  "paragraph_id": "0001730168-26-000076:8k_2_02:7" }
```

```json
{ "id": "across_documents_quarterly_operating_cash_flow_only_release_figure",
  "what_changed": "The release prints a three-month operating cash flow ($14.2 billion; 14,197 in millions in its reconciliation) and free cash flow of $13.7 billion. The trend table has no operating_cash_flow row for 2026-05-04..2026-08-02, which is why quarterly accruals_over_total_assets is insufficient. Python did not use the release figure, and I do not substitute it.",
  "account": "NetCashProvidedByUsedInOperatingActivities (three-month)",
  "expected_direction": "none",
  "horizon": "none: insufficient",
  "quote": "Cash from operations of $14.2 billion for the third quarter, less capital expenditures of $0.5 billion, resulted in $13.7 billion of free cash flow, or 46 percent of revenue",
  "paragraph_id": "0001730168-26-000076:8k_2_02:8" }
```

```json
{ "id": "liquidity_and_capital_cash_balance_release_figure",
  "what_changed": "The release prints cash and cash equivalents of $24.0 billion at quarter end against $19.6 billion at the prior quarter end. The trend table's soft_asset_share inputs print cash of 23975000000.0 at 2026-08-02 and 19628000000.0 at 2026-05-03. The release prints no change figure.",
  "account": "CashAndCashEquivalentsAtCarryingValue",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "cash and cash equivalents at the end of the fiscal quarter were $24.0 billion, compared to $19.6 billion at the end of the prior fiscal quarter",
  "paragraph_id": "0001730168-26-000076:8k_2_02:22" }
```

```json
{ "id": "liquidity_and_capital_dividend_paid_release_figure",
  "what_changed": "The release says the company paid a cash dividend of $0.65 per share, totaling $3.1 billion, on June 30, 2026. Its cash flow statement prints dividend payments of (3,103) for the quarter (in millions).",
  "account": "dividends paid",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "On June 30, 2026, the Company paid a cash dividend of $0.65 per share, totaling $3.1 billion",
  "paragraph_id": "0001730168-26-000076:8k_2_02:24" }
```

## Seen in the notes

No items. No fact in what I read prints a marker saying its element sat inside a note, and I do not guess which facts did. So no finding can be placed here on the input's own word. The fact items above that a reader might take for note disclosures (purchase obligations, other commitments, guarantees, the segment-axis expense, the tax holiday, the subsequent-event dividend) are under "Seen in the statements", each marked "no in-note marker". The later notes split will have to place them from the source filing, not from this report.
