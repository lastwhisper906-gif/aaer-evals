FTNT — numbers reader — 10-Q 0001262039-26-000021 (quarter ended 2026-06-30, filed 2026-07-30)

**What my input holds.** I read all four files in full.
- `input_trends.json` is the trend table with its formula inputs.
- `input_numbers.json` has top-level keys `ticker`, `cutoff`, `documents` and `facts` only. It covers three XBRL instances: 10-K 0001262039-26-000007, 10-Q 0001262039-26-000013 and 10-Q 0001262039-26-000021.
- `input_8k.md` is 8-K 0001262039-26-000018, the Item 2.02 release.
- `input_prior_predictions.md` says "None on record".

There are no prices, returns, short interest, other companies' files, prior probabilities or outcome windows in my directory.

**What my input does not hold.** My directory has no articulation checks, no restatement traces and no fourth-quarter derivation. So no articulation gap can be reported: none exists in my input, and I built none myself. Restated prior values are covered below.

**Restated prior values.** No restatement trace is in my input. The facts mark `superseded_by` where a later filing reported the same element and period. That marker does not say the value changed.
- I read every 2025-12-31 balance-sheet fact in the 10-K and in both 10-Qs. Each later filing prints the same value string as the 10-K.
- I also read every other fact in all three instances. I found no element and period printed with a different value in a later filing.

So I report no restated value. Where the value stayed the same but the concept or the dimension member changed, there are items below.

**Periods the record does not reach.** `quarters-back-2` (target 2025-12-30) and `quarters-back-6` (target 2024-12-31) have no cells. The reason the table gives, for each: "no quarter ending within 20 days of 2025-12-30 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py". The text for 2024-12-31 is the same. The derivation it points to is not in my input, so neither fourth quarter exists here.

**Rows I could not itemize.**
- The `research_and_development_capitalized` block in each year prints no `paragraph_id`, so it is not itemized. In it, `capitalized_development_cost` is missing with this reason: "no row for capitalized_development_cost: the companyfacts record tags none of us-gaap:CapitalizedComputerSoftwareAdditions in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment — the filing says which, and this record cannot".
- The 8-K item-code list and the late-filing notice print no `[id]` lines, so they are not itemized. For the record:
  - the list shows 0001262039-24-000034 (2024-08-07, Items 2.02 and 9.01) as an amendment of 0001262039-24-000032;
  - it shows several Item 5.02 amendments whose subject the index does not give;
  - the notice reports no late-filing notifications on or before 2026-07-30.
- The income-statement interest line is tagged `InterestExpense` in the 10-K (annual periods) and `InterestExpenseNonoperating` in the 10-Qs (quarterly and year-to-date periods). No single period is printed under both concepts, so my input does not show one period resting on two concepts, and this is not itemized.

**Conventions.**
- `expected_direction` is read off the sign of the `year_over_year` change Python printed on the row: positive is `up`, negative is `down`. Where the row prints no change, it is `none`.
- For 8-K rows, it is `up` only where the release's own words say growth or an increase, and otherwise `none`.
- In every case it describes the direction the account is moving. It is not a forecast of price or of any outcome.
- `horizon` is the next filing that will recompute or restate the same figure.

## Seen in the statements

**Trend table, quarters-back-0 (2026-04-01..2026-06-30)**

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly_cell",
  "what_changed": "insufficient. accruals_over_total_assets has no value for 2026-04-01..2026-06-30: the cell says the operating cash flow concepts are in the record but not for this period. For this filing the facts hold operating cash flow only as the six-month figure NetCashProvidedByUsedInOperatingActivities 2026-01-01..2026-06-30 = 2120700000. No three-month figure exists in my input and none was derived. In the whole quarterly window only quarters-back-1 (lowest of the 2 filled quarters) and quarters-back-5 (highest of the 2 filled quarters) are filled. That does not support a quarterly trend claim.",
  "account": "accruals: NetIncomeLoss less NetCashProvidedByUsedInOperatingActivities, over Assets",
  "expected_direction": "none",
  "horizon": "next 10-Q (quarter ending 2026-09-30); the cell stays empty while operating cash flow is filed only year-to-date",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-04-01..2026-06-30: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0001262039-26-000021:trends:accruals_over_total_assets:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly_cell",
  "what_changed": "insufficient. bad_debt_reserve_ratio has no value at 2026-06-30: the allowance concepts are in the record but not for this period. In the quarterly window the ratio is filled only at 2024-09-30 (quarters-back-7); see structure_and_disclosure_changes_quarterly_allowance_tagged_once. No quarterly reserve trend can be claimed.",
  "account": "AllowanceForDoubtfulAccountsReceivable / (AccountsReceivableNetCurrent + allowance)",
  "expected_direction": "none",
  "horizon": "next 10-Q (quarter ending 2026-09-30)",
  "quote": "\"missing\": \"no row for bad_debt_allowance in 2026-06-30: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"",
  "paragraph_id": "0001262039-26-000021:trends:bad_debt_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly_cell",
  "what_changed": "contract_liabilities_over_revenue is 1.8759705063723815 for 2026-04-01..2026-06-30: ContractWithCustomerLiabilityCurrent 3841800000 at 2026-06-30 over quarterly revenue 2047900000. quarter_over_quarter change is -0.13868131023661512 against quarters-back-1; year_over_year change is -0.21758777583620725 against quarters-back-4. Position: lowest of the 6 filled quarters. The numerator is the current balance only. The non-current balance (ContractWithCustomerLiabilityNoncurrent 3833900000 at 2026-06-30) is outside the ratio.",
  "account": "ContractWithCustomerLiabilityCurrent / RevenueFromContractWithCustomerExcludingAssessedTax (quarter)",
  "expected_direction": "down",
  "horizon": "next 10-Q (quarter ending 2026-09-30)",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001262039-26-000021:trends:contract_liabilities_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_quarterly_cell",
  "what_changed": "days_sales_of_inventory is 95.85693106004447 for 2026-04-01..2026-06-30: InventoryNet 426300000 over CostOfGoodsAndServicesSold 404700000, times 91 days. quarter_over_quarter change is 4.597671800785221 against quarters-back-1; year_over_year change is -21.238019717980308 against quarters-back-4. Position: second lowest of the 6 filled quarters. The two printed changes point in opposite directions; expected_direction follows the year_over_year sign.",
  "account": "InventoryNet / CostOfGoodsAndServicesSold x days (quarter)",
  "expected_direction": "down",
  "horizon": "next 10-Q (quarter ending 2026-09-30)",
  "quote": "\"position_in_history\": \"second lowest of the 6 filled quarters\"",
  "paragraph_id": "0001262039-26-000021:trends:days_sales_of_inventory:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly_cell",
  "what_changed": "days_sales_outstanding is 64.68069729967284 for 2026-04-01..2026-06-30: AccountsReceivableNetCurrent 1455600000 over revenue 2047900000, times 91 days. quarter_over_quarter change is -7.636560485794277 against quarters-back-1; year_over_year change is -3.1896707984866595 against quarters-back-4. Position: third lowest of the 6 filled quarters.",
  "account": "AccountsReceivableNetCurrent / RevenueFromContractWithCustomerExcludingAssessedTax x days (quarter)",
  "expected_direction": "down",
  "horizon": "next 10-Q (quarter ending 2026-09-30)",
  "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
  "paragraph_id": "0001262039-26-000021:trends:days_sales_outstanding:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly_cell",
  "what_changed": "gross_margin is 0.8023829288539479 for 2026-04-01..2026-06-30: revenue 2047900000, CostOfGoodsAndServicesSold 404700000. quarter_over_quarter change is -0.0005474344678514376 against quarters-back-1; year_over_year change is -0.004426887096972365 against quarters-back-4. Position: lowest of the 6 filled quarters.",
  "account": "(revenue - CostOfGoodsAndServicesSold) / revenue (quarter)",
  "expected_direction": "down",
  "horizon": "next 10-Q (quarter ending 2026-09-30)",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001262039-26-000021:trends:gross_margin:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly_cell",
  "what_changed": "inventory_reserve_ratio is 0.2880600516068496 at 2026-06-30: InventoryValuationReserves 122800000 over InventoryNet 426300000. quarter_over_quarter change is -0.05095509990830188 against quarters-back-1; year_over_year change is -0.07324300861032712 against quarters-back-4. Position: lowest of the 6 filled quarters. As printed on the neighbouring cells, the reserve input is 125300000 at 2026-03-31 and 146400000 at 2025-06-30.",
  "account": "InventoryValuationReserves / InventoryNet",
  "expected_direction": "down",
  "horizon": "next 10-Q (quarter ending 2026-09-30)",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001262039-26-000021:trends:inventory_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly_cell",
  "what_changed": "insufficient. non_gaap_gap cannot be filled in any period of the window because companyfacts carries no non-GAAP concept. The 8-K release prints non-GAAP figures (see across_documents_non_gaap_net_income_only_in_release). The gap between them and GAAP is not computed anywhere in my input, so it does not exist here.",
  "account": "non-GAAP net income against GAAP NetIncomeLoss",
  "expected_direction": "none",
  "horizon": "next earnings release and 10-Q (quarter ending 2026-09-30)",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001262039-26-000021:trends:non_gaap_gap:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarterly_cell",
  "what_changed": "receivables_over_revenue is 0.7107768934029982 for 2026-04-01..2026-06-30: AccountsReceivableNetCurrent 1455600000 over revenue 2047900000. quarter_over_quarter change is -0.09274819310219207 against quarters-back-1; year_over_year change is -0.03505132745589745 against quarters-back-4. Position: third lowest of the 6 filled quarters.",
  "account": "AccountsReceivableNetCurrent / RevenueFromContractWithCustomerExcludingAssessedTax (quarter)",
  "expected_direction": "down",
  "horizon": "next 10-Q (quarter ending 2026-09-30)",
  "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
  "paragraph_id": "0001262039-26-000021:trends:receivables_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_soft_asset_share_quarterly_cell",
  "what_changed": "soft_asset_share is 0.5732282304405482 at 2026-06-30: Assets 10859200000, PropertyPlantAndEquipmentNet 1699500000, CashAndCashEquivalentsAtCarryingValue 2934900000. quarter_over_quarter change is -0.030626679257433342 against quarters-back-1; year_over_year change is 0.03494379418216109 against quarters-back-4. Position: third lowest of the 6 filled quarters. The two printed changes point in opposite directions; expected_direction follows the year_over_year sign.",
  "account": "(Assets - PropertyPlantAndEquipmentNet - CashAndCashEquivalentsAtCarryingValue) / Assets",
  "expected_direction": "up",
  "horizon": "next 10-Q (quarter ending 2026-09-30)",
  "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
  "paragraph_id": "0001262039-26-000021:trends:soft_asset_share:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly_cell",
  "what_changed": "insufficient. warranty_reserve_ratio is filled in no period of the window, quarterly or annual: the coverage block prints filled 0. The warranty accrual concepts are in the record but not for any requested period. No warranty reserve value or trend exists in my input.",
  "account": "StandardProductWarrantyAccrual / revenue",
  "expected_direction": "none",
  "horizon": "next 10-Q (quarter ending 2026-09-30)",
  "quote": "\"missing\": \"no row for warranty_accrual in 2026-06-30: us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent is in the record, but not for this period\"",
  "paragraph_id": "0001262039-26-000021:trends:warranty_reserve_ratio:2026-04-01..2026-06-30" }
```

**Trend table, years-back-0 (2025-01-01..2025-12-31)**

```json
{ "id": "earnings_quality_accruals_over_total_assets_annual_cell",
  "what_changed": "accruals_over_total_assets is -0.07095830285296269 for 2025: NetIncomeLoss 1853400000, NetCashProvidedByUsedInOperatingActivities 2590600000, Assets 10389200000 at 2025-12-31. year_over_year change is -0.01842375952143889 against years-back-1. Position: second highest of the 5 filled years.",
  "account": "accruals: NetIncomeLoss less NetCashProvidedByUsedInOperatingActivities, over Assets (year)",
  "expected_direction": "down",
  "horizon": "next 10-K (fiscal year ending 2026-12-31)",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001262039-26-000021:trends:accruals_over_total_assets:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual_cell",
  "what_changed": "bad_debt_reserve_ratio is 0.0043565289061580125 at 2025-12-31: AllowanceForDoubtfulAccountsReceivable 7400000 from the 10-K, AccountsReceivableNetCurrent 1691200000 from the 10-Q filed 2026-07-30. year_over_year change is 0.00034101131274618356 against years-back-1. Position: second highest of the 5 filled years.",
  "account": "AllowanceForDoubtfulAccountsReceivable / (AccountsReceivableNetCurrent + allowance)",
  "expected_direction": "up",
  "horizon": "next 10-K (fiscal year ending 2026-12-31)",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001262039-26-000021:trends:bad_debt_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual_cell",
  "what_changed": "contract_liabilities_over_revenue is 0.5347373374904406 for 2025: ContractWithCustomerLiabilityCurrent 3636000000 at 2025-12-31 over annual revenue 6799600000. year_over_year change is -0.015348293323220075 against years-back-1. Position: third highest of the 5 filled years. The 2025-12-31 input is the 10-Q's concept; the 10-K tagged the same balance as DeferredRevenueCurrent (see structure_and_disclosure_changes_current_deferred_revenue_concept_switch).",
  "account": "ContractWithCustomerLiabilityCurrent / RevenueFromContractWithCustomerExcludingAssessedTax (year)",
  "expected_direction": "down",
  "horizon": "next 10-K (fiscal year ending 2026-12-31)",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001262039-26-000021:trends:contract_liabilities_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_annual_cell",
  "what_changed": "days_sales_of_inventory is 109.72797050191888 for 2025: InventoryNet 399500000 at 2025-12-31 over CostOfGoodsAndServicesSold 1328900000, times 365 days. year_over_year change is 9.975897246908517 against years-back-1. Position: second highest of the 5 filled years.",
  "account": "InventoryNet / CostOfGoodsAndServicesSold x days (year)",
  "expected_direction": "up",
  "horizon": "next 10-K (fiscal year ending 2026-12-31)",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001262039-26-000021:trends:days_sales_of_inventory:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual_cell",
  "what_changed": "days_sales_outstanding is 90.78298723454321 for 2025: AccountsReceivableNetCurrent 1691200000 at 2025-12-31 over revenue 6799600000, times 365 days. year_over_year change is 0.8531037596112157 against years-back-1. Position: third highest of the 5 filled years.",
  "account": "AccountsReceivableNetCurrent / RevenueFromContractWithCustomerExcludingAssessedTax x days (year)",
  "expected_direction": "up",
  "horizon": "next 10-K (fiscal year ending 2026-12-31)",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001262039-26-000021:trends:days_sales_outstanding:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_gross_margin_annual_cell",
  "what_changed": "gross_margin is 0.8045620330607682 for 2025: revenue 6799600000, CostOfGoodsAndServicesSold 1328900000. year_over_year change is -0.0010728102852138877 against years-back-1. Position: second highest of the 5 filled years.",
  "account": "(revenue - CostOfGoodsAndServicesSold) / revenue (year)",
  "expected_direction": "down",
  "horizon": "next 10-K (fiscal year ending 2026-12-31)",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001262039-26-000021:trends:gross_margin:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_annual_cell",
  "what_changed": "inventory_reserve_ratio is 0.344180225281602 at 2025-12-31: InventoryValuationReserves 137500000 over InventoryNet 399500000. year_over_year change is -0.11477381592283536 against years-back-1. Position: second highest of the 4 filled years. years-back-4 is not filled; its cell says the reserve concept is in the record but not for 2021-12-31.",
  "account": "InventoryValuationReserves / InventoryNet (year-end)",
  "expected_direction": "down",
  "horizon": "next 10-K (fiscal year ending 2026-12-31)",
  "quote": "\"position_in_history\": \"second highest of the 4 filled years\"",
  "paragraph_id": "0001262039-26-000021:trends:inventory_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual_cell",
  "what_changed": "insufficient. non_gaap_gap has no value for 2025 or any other year because companyfacts carries no non-GAAP concept. No annual non-GAAP figure is in my input either: the 8-K release prints only the quarter's reconciliation.",
  "account": "non-GAAP net income against GAAP NetIncomeLoss (year)",
  "expected_direction": "none",
  "horizon": "next 10-K (fiscal year ending 2026-12-31)",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001262039-26-000021:trends:non_gaap_gap:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual_cell",
  "what_changed": "receivables_over_revenue is 0.24872051297135125 for 2025: AccountsReceivableNetCurrent 1691200000 over revenue 6799600000. year_over_year change is 0.003010448832192786 against years-back-1. Position: third highest of the 5 filled years.",
  "account": "AccountsReceivableNetCurrent / RevenueFromContractWithCustomerExcludingAssessedTax (year)",
  "expected_direction": "up",
  "horizon": "next 10-K (fiscal year ending 2026-12-31)",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001262039-26-000021:trends:receivables_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_soft_asset_share_annual_cell",
  "what_changed": "soft_asset_share is 0.6039829823278019 at 2025-12-31: Assets 10389200000, PropertyPlantAndEquipmentNet 1619000000, CashAndCashEquivalentsAtCarryingValue 2495300000. year_over_year change is 0.0367758452504392 against years-back-1. Position: third highest of the 5 filled years.",
  "account": "(Assets - PropertyPlantAndEquipmentNet - CashAndCashEquivalentsAtCarryingValue) / Assets (year-end)",
  "expected_direction": "up",
  "horizon": "next 10-K (fiscal year ending 2026-12-31)",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001262039-26-000021:trends:soft_asset_share:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_annual_cell",
  "what_changed": "insufficient. warranty_reserve_ratio has no value at 2025-12-31 or at any other year-end in the window: the warranty accrual concepts are in the record but not for these periods. No warranty reserve value exists in my input.",
  "account": "StandardProductWarrantyAccrual / revenue (year)",
  "expected_direction": "none",
  "horizon": "next 10-K (fiscal year ending 2026-12-31)",
  "quote": "\"missing\": \"no row for warranty_accrual in 2025-12-31: us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent is in the record, but not for this period\"",
  "paragraph_id": "0001262039-26-000021:trends:warranty_reserve_ratio:2025-01-01..2025-12-31" }
```

**Concept and member changes, and disclosure cadence (trend table and numeric facts)**

```json
{ "id": "structure_and_disclosure_changes_quarterly_allowance_tagged_once",
  "what_changed": "In the quarterly window the allowance concept fills bad_debt_reserve_ratio only at 2024-09-30: AllowanceForDoubtfulAccountsReceivable 4700000 from 0001262039-24-000043, ratio value 0.004481311975591152. Every later quarter-end cell in the window (2025-03-31, 2025-06-30, 2025-09-30, 2026-03-31, 2026-06-30) prints that the allowance concepts are in the record but not for that period. Apart from that cell, my input holds the allowance only at year-ends, in the 10-K: 7400000 at 2025-12-31 and 5900000 at 2024-12-31. A quarterly allowance trend is insufficient.",
  "account": "AllowanceForDoubtfulAccountsReceivable (quarter-end tagging)",
  "expected_direction": "none",
  "horizon": "next 10-Q (quarter ending 2026-09-30)",
  "quote": "\"position_in_history\": \"the only filled quarter\"",
  "paragraph_id": "0001262039-26-000021:trends:bad_debt_reserve_ratio:2024-07-01..2024-09-30" }
```

```json
{ "id": "structure_and_disclosure_changes_current_deferred_revenue_concept_switch",
  "what_changed": "The 10-K 0001262039-26-000007 (filed 2026-02-25) tags the 2025-12-31 current deferred revenue balance as DeferredRevenueCurrent, value 3636000000. That fact carries no superseded_by. The 10-Qs 0001262039-26-000013 and 0001262039-26-000021 tag the same date as ContractWithCustomerLiabilityCurrent, value 3636000000. The trend's years-back-0 contract_liabilities input rests on the 10-Q concept (id 0001262039-26-000021:facts:ContractWithCustomerLiabilityCurrent:2025-12-31). The printed value is the same string in all three filings: the concept changed, the number did not, so this is not a restated value.",
  "account": "current deferred revenue / contract liabilities (DeferredRevenueCurrent vs ContractWithCustomerLiabilityCurrent)",
  "expected_direction": "none",
  "horizon": "next 10-K (fiscal year ending 2026-12-31)",
  "quote": "\"value\": \"3636000000\"",
  "paragraph_id": "0001262039-26-000007:facts:DeferredRevenueCurrent:2025-12-31" }
```

```json
{ "id": "structure_and_disclosure_changes_current_deferred_revenue_concept_switch_comparative",
  "what_changed": "The same 10-K tags the 2024-12-31 current deferred revenue balance as DeferredRevenueCurrent, value 3276200000. The trend's years-back-1 contract_liabilities input for that date is ContractWithCustomerLiabilityCurrent from accession 0001262039-25-000039 (filed 2025-11-07), value 3276200000, not from the 10-K. The earlier annual cells likewise take their contract_liabilities input from accessions filed in November: 0001262039-24-000043, 0001262039-23-000038 and 0001262039-22-000038. That year's revenue input comes from the 10-K, so each annual contract_liabilities ratio mixes inputs from two filings that tag the balance under different concepts. The value strings are the same; no restated value.",
  "account": "current deferred revenue / contract liabilities, comparative year-end",
  "expected_direction": "none",
  "horizon": "next 10-K (fiscal year ending 2026-12-31)",
  "quote": "\"value\": \"3276200000\"",
  "paragraph_id": "0001262039-26-000007:facts:DeferredRevenueCurrent:2024-12-31" }
```

```json
{ "id": "structure_and_disclosure_changes_noncurrent_deferred_revenue_concept_switch",
  "what_changed": "The 10-K tags the 2025-12-31 non-current deferred revenue balance as DeferredRevenueNoncurrent, value 3479800000, with no superseded_by. Both 10-Qs tag the same date as ContractWithCustomerLiabilityNoncurrent, value 3479800000. The value is the same; the concept differs. No trend ratio uses the non-current balance.",
  "account": "non-current deferred revenue (DeferredRevenueNoncurrent vs ContractWithCustomerLiabilityNoncurrent)",
  "expected_direction": "none",
  "horizon": "next 10-K (fiscal year ending 2026-12-31)",
  "quote": "\"value\": \"3479800000\"",
  "paragraph_id": "0001262039-26-000007:facts:DeferredRevenueNoncurrent:2025-12-31" }
```

```json
{ "id": "structure_and_disclosure_changes_equity_statement_total_concept_switch",
  "what_changed": "Both 10-Qs, 0001262039-26-000013 and 0001262039-26-000021, tag the totals in their statements of stockholders' equity as StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest. In the 10-Q filed 2026-07-30 that covers 2024-12-31 (value 1493800000), 2025-03-31, 2025-06-30, 2025-12-31, 2026-03-31 and 2026-06-30. The 10-Q filed 2026-05-08 prints the same concept for 2024-12-31 (1493800000), 2025-03-31, 2025-12-31 and 2026-03-31. The 10-K tags total equity at 2024-12-31 as StockholdersEquity, value 1493800000. The 10-Q filed 2026-07-30 keeps StockholdersEquity on its balance sheet for 2025-12-31 (1237500000) and 2026-06-30 (1551100000). The 2024-12-31 period therefore rests on two concepts across filings, with the same value string. The trend table's R&D-capitalisation block reads StockholdersEquity.",
  "account": "total stockholders' equity (StockholdersEquity vs StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest)",
  "expected_direction": "none",
  "horizon": "next 10-Q (quarter ending 2026-09-30)",
  "quote": "\"value\": \"1493800000\"",
  "paragraph_id": "0001262039-26-000021:facts:StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest:2024-12-31" }
```

```json
{ "id": "structure_and_disclosure_changes_geographic_member_switch_emea",
  "what_changed": "The 10-K 0001262039-26-000007 files EMEA property and equipment, net, at 2025-12-31 under the geographic member ftnt:EuropeMiddleEastAndAfricaMember, value 211300000, and that fact carries no superseded_by. The 10-Q 0001262039-26-000013 files 2025-12-31 under us-gaap:EMEAMember, value 211300000, marked superseded_by 0001262039-26-000021. The 10-K's US, Canada, Latin America and Americas property facts for the same date do carry superseded_by. Revenue by geography follows the same pattern. The 10-K files 2025 EMEA revenue under ftnt:EuropeMiddleEastAndAfricaMember (2834300000). Both 10-Qs file regional revenue under us-gaap:EMEAMember: 784800000 for 2026-01-01..2026-03-31 in the 10-Q filed 2026-05-08, and the 2026-04-01..2026-06-30 row in the 10-Q filed 2026-07-30. The 2025-12-31 value string is the same under both members: the element changed, the number did not. My input does not say whether the two members define the same region.",
  "account": "geographic disaggregation, EMEA (property and equipment, net; revenue)",
  "expected_direction": "none",
  "horizon": "next 10-K (fiscal year ending 2026-12-31)",
  "quote": "\"value\": \"211300000\"",
  "paragraph_id": "0001262039-26-000007:facts:PropertyPlantAndEquipmentNet:2025-12-31:srt:StatementGeographicalAxis=ftnt:EuropeMiddleEastAndAfricaMember" }
```

```json
{ "id": "structure_and_disclosure_changes_geographic_member_switch_asia_pacific",
  "what_changed": "The 10-K files Asia-Pacific property and equipment, net, at 2025-12-31 under ftnt:AsiaPacificAndJapanMember, value 72800000, with no superseded_by. The 10-Q 0001262039-26-000013 files 2025-12-31 under srt:AsiaPacificMember, value 72800000, marked superseded_by 0001262039-26-000021. Revenue by geography follows the same pattern: the 10-K files 2025 revenue under ftnt:AsiaPacificAndJapanMember (1264900000), and the 10-Q filed 2026-05-08 files regional revenue under srt:AsiaPacificMember (325000000 for 2026-01-01..2026-03-31). The 2025-12-31 value string is the same under both members. My input does not say whether the two members define the same region.",
  "account": "geographic disaggregation, Asia-Pacific (property and equipment, net; revenue)",
  "expected_direction": "none",
  "horizon": "next 10-K (fiscal year ending 2026-12-31)",
  "quote": "\"value\": \"72800000\"",
  "paragraph_id": "0001262039-26-000007:facts:PropertyPlantAndEquipmentNet:2025-12-31:srt:StatementGeographicalAxis=ftnt:AsiaPacificAndJapanMember" }
```

**8-K earnings release (Item 2.02, exhibit 99.1), condensed statements and figures**

```json
{ "id": "results_against_expectations_release_exceeds_quarter_guidance",
  "what_changed": "The release says the quarter's revenue and profitability exceeded the high end of the company's own second-quarter guidance. The guidance figures it was measured against are not in my input.",
  "account": "revenue and profitability against company guidance",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 (reported)",
  "quote": "Exceeds high end of second quarter guidance on revenue and profitability",
  "paragraph_id": "0001262039-26-000018:8k_2_02:5" }
```

```json
{ "id": "results_against_expectations_full_year_revenue_guidance_raised",
  "what_changed": "The release raises fiscal 2026 revenue guidance and prints a full-year revenue range of $8.020 billion to $8.180 billion (paragraph 0001262039-26-000018:8k_2_02:34). The guidance it replaces is not in my input.",
  "account": "fiscal 2026 revenue guidance",
  "expected_direction": "up",
  "horizon": "fiscal year ending 2026-12-31 (next 10-K)",
  "quote": "Raises 2026 revenue guidance to 19% year over year growth",
  "paragraph_id": "0001262039-26-000018:8k_2_02:6" }
```

```json
{ "id": "results_against_expectations_next_quarter_revenue_guidance_range",
  "what_changed": "Third-quarter 2026 guidance: revenue of $2.010 billion to $2.100 billion and billings of $2.250 billion to $2.350 billion (paragraph 0001262039-26-000018:8k_2_02:29). No comparison of these ranges with the reported quarter is computed in my input.",
  "account": "third-quarter 2026 revenue guidance",
  "expected_direction": "none",
  "horizon": "next 10-Q (quarter ending 2026-09-30)",
  "quote": "•Revenue in the range of $2.010 billion to $2.100 billion",
  "paragraph_id": "0001262039-26-000018:8k_2_02:28" }
```

```json
{ "id": "across_documents_non_gaap_net_income_only_in_release",
  "what_changed": "The trend table's non_gaap_gap is insufficient in every period because companyfacts holds no non-GAAP concept. The release's reconciliation prints, for the three months ended June 30, 2026 against the year-earlier quarter: non-GAAP net income 665.0 (491.1); GAAP net income 606.3 (440.1); add-backs of stock-based compensation 80.8, amortization of acquired intangible assets 9.9 and gain on intellectual property matters (1.3); a tax adjustment of (30.7) to an 18% non-GAAP rate. The gap between non-GAAP and GAAP is not computed in my input, so it does not exist here.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "next earnings release (quarter ending 2026-09-30)",
  "quote": "Non-GAAP net income | $ | 665.0",
  "paragraph_id": "0001262039-26-000018:8k_2_02:76" }
```

```json
{ "id": "across_documents_three_month_operating_cash_flow_only_in_release",
  "what_changed": "The trend table's accruals cell for the quarter is insufficient because companyfacts holds operating cash flow only year-to-date: the 10-Q facts print NetCashProvidedByUsedInOperatingActivities 2120700000 for 2026-01-01..2026-06-30. The release prints three-month operating cash flow of 1,043.6 (451.9 a year earlier), free cash flow of 965.6 (284.1) and free cash flow margin of 47.2% (17.4%). No quarterly accrual ratio is computed in my input.",
  "account": "operating cash flow, three months ended June 30, 2026",
  "expected_direction": "none",
  "horizon": "next 10-Q (quarter ending 2026-09-30)",
  "quote": "Net cash provided by operating activities | $ | 1,043.6",
  "paragraph_id": "0001262039-26-000018:8k_2_02:79" }
```

```json
{ "id": "revenue_recognition_noncurrent_deferred_revenue_outside_ratio",
  "what_changed": "The release balance sheet prints non-current deferred revenue of 3,833.9 at June 30, 2026 (3,479.8 at December 31, 2025), beside current deferred revenue of 3,841.8 (3,636.0). The trend's contract_liabilities_over_revenue uses the current balance only; a ratio on total deferred revenue does not exist in my input. The release's billings reconciliation prints the quarter's change in deferred revenue as 324.2 (149.2 a year earlier). The six-month cash flow statement prints a deferred revenue change of 559.9 (204.8).",
  "account": "deferred revenue, current and non-current",
  "expected_direction": "up",
  "horizon": "next 10-Q (quarter ending 2026-09-30)",
  "quote": "DEFERRED REVENUE | 3,833.9",
  "paragraph_id": "0001262039-26-000018:8k_2_02:64" }
```

```json
{ "id": "revenue_recognition_billings_growth_in_release",
  "what_changed": "The release reports billings, a non-GAAP measure defined as revenue plus the change in deferred revenue less acquired deferred revenue, of 2,372.1 against 1,778.4 a year earlier (paragraph 0001262039-26-000018:8k_2_02:81). Billings has no companyfacts concept and is not in the trend table.",
  "account": "billings (non-GAAP)",
  "expected_direction": "up",
  "horizon": "next earnings release (quarter ending 2026-09-30)",
  "quote": "•Billings grew 33% year over year to $2.37 billion1",
  "paragraph_id": "0001262039-26-000018:8k_2_02:10" }
```

```json
{ "id": "revenue_recognition_product_revenue_growth_in_release",
  "what_changed": "The release income statement prints product revenue of 773.0 for the quarter against 508.9 a year earlier, and service revenue of 1,274.9 against 1,121.1 (paragraph 0001262039-26-000018:8k_2_02:68). The same quarter's inventory cells sit beside this: days_sales_of_inventory year_over_year change -21.238019717980308, and inventory_reserve_ratio lowest of the 6 filled quarters.",
  "account": "product revenue",
  "expected_direction": "up",
  "horizon": "next 10-Q (quarter ending 2026-09-30)",
  "quote": "•Product revenue grew 52% year over year to $773 million",
  "paragraph_id": "0001262039-26-000018:8k_2_02:9" }
```

```json
{ "id": "liquidity_and_capital_senior_notes_repaid",
  "what_changed": "The six-month cash flow statement prints repayment of senior notes of (500.0), with none a year earlier. The 10-Q facts print RepaymentsOfSeniorDebt 500000000 for 2026-01-01..2026-06-30 and LongTermDebtCurrent 0 at 2026-06-30, against 499700000 at 2025-12-31. Non-current long-term debt is 496900000 at 2026-06-30.",
  "account": "senior notes / long-term debt",
  "expected_direction": "down",
  "horizon": "next 10-Q (quarter ending 2026-09-30)",
  "quote": "Repayment of senior notes | (500.0)",
  "paragraph_id": "0001262039-26-000018:8k_2_02:72" }
```

```json
{ "id": "liquidity_and_capital_share_repurchases_six_months",
  "what_changed": "The six-month cash flow statement prints repurchase and retirement of common stock of (972.8), against (401.1) a year earlier. The 10-Q facts print StockRepurchasedAndRetiredDuringPeriodShares 12500000 for 2026-01-01..2026-06-30, and CommonStockSharesOutstanding of 733600000 at 2026-06-30 against 743000000 at 2025-12-31. The release prints quarterly interest income of 33.2 against 45.0 a year earlier.",
  "account": "share repurchases (cash) and shares outstanding",
  "expected_direction": "none",
  "horizon": "next 10-Q (quarter ending 2026-09-30)",
  "quote": "Repurchase and retirement of common stock | (972.8)",
  "paragraph_id": "0001262039-26-000018:8k_2_02:72" }
```

## Seen in the notes

No items. My instructions say each fact is marked with whether its element sat inside a note. I read every fact in `input_numbers.json`, and none carries such a marker. Every fact prints only `id`, `paragraph_id`, `tag`, `prefix`, `namespace`, `context` (sometimes with `typed_segment`), `context_ref`, `unit`, `decimals`, `value`, `number`, `nil`, `form`, `source_accession`, `filing_date` and, on some facts, `superseded_by`. I was told not to judge where a fact sat, so I placed nothing here and itemized no fact whose location I would have had to guess.

The facts that look like disclosure-table rows are left unplaced for this reason. Examples are fair-value hierarchy levels, available-for-sale security detail, customer concentration percentages, remaining performance obligations, refund liabilities, the tax-rate reconciliation, and subsequent-event repurchases. The geographic member items above are placed under the statements heading for the same reason: no marker places them anywhere else. The emptiness of this heading reflects the missing marker. It does not mean the filing has no notes.
