<!-- the quote gate removed 1 item(s) from this copy; input_manifest.json lists each with its reason -->
# FFIV — numbers report — 10-Q 0001048695-26-000067 (period ending 2026-06-30)

## Notes on this report (not items)

- **Inputs read in full:**
  - `input_trends.json`
  - `input_numbers.json`, which holds facts from the 10-K 0001048695-25-000157 and the 10-Qs 0001048695-26-000051 and 0001048695-26-000067
  - `input_8k.md`, the 8-K 0001048695-26-000063 filed 2026-07-27
  - `input_prior_predictions.md`
- **Nothing forbidden is in the directory.** It holds no prices, abnormal returns, short interest, other company's files, earlier run's probabilities or outcome window.
- **No prior flags.** `input_prior_predictions.md` says: "None on record. This company has no earlier run under the given run root, so there are no flags, no management explanations and no outcomes to carry forward."
- **Three expected inputs are missing from the directory:**
  - articulation checks
  - restatement traces
  - fourth-quarter derivation

  So I can report no articulation gap. None of these exists in my input, and I do not work one out.
- **No restated prior values.** No restatement-trace file was given. In `input_numbers.json` I found no fact where a later filing gives a different value for the same concept, period and dimensions. Every value I compared between an earlier filing and the filing that supersedes it is the same. So there are no restated-value items.
- **Changes of tag** are reported as items under `structure_and_disclosure_changes_*`. This covers:
  - every place where the trend table says a period rests on a different concept;
  - places in the facts where the same period and amount appear under a different concept in different filings.
- **Two quarters have no cells.** The record does not reach `quarters-back-3` (target 2025-09-30) or `quarters-back-7` (target 2024-10-01). The trend table gives the same reason for both: "no quarter ending within 20 days of [target] is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py". The fourth-quarter derivation is not in my directory.
- **The R&D baseline cannot be an item.** The formula-baseline block `research_and_development_capitalized` for `years-back-0` prints no `paragraph_id` and is not inside a ratio cell, so I cannot quote it. Values as printed:
  - `earnings_with_rnd_capitalized` 726650200.0
  - `research_and_development_amortization` 505544800.0
  - `research_and_development_asset` 1575954600.0
  - `life_years` 5
  - `book_value_with_rnd_capitalized` is missing: "no row for stockholders_equity: the companyfacts record tags none of us-gaap:StockholdersEquity in any period".
  - `capitalized_development_cost` and `capitalized_over_expense` are missing: "no row for capitalized_development_cost: the companyfacts record tags none of us-gaap:CapitalizedComputerSoftwareAdditions in any period".
- **History is short, so trend claims are `insufficient`.** Quarterly positions rest on 6 filled quarters and annual positions on 5 filled years. Quarterly accruals are filled in only 2 quarters (quarters-back-2 and quarters-back-6). Bad-debt same-concept comparisons cover 4 quarters. The only claim I make about where a value sits is the printed `position_in_history`.
- **`expected_direction` is "none"** unless the input itself states a direction. Only the company's raised full-year guidance does. I make no forecast of my own.
- **No in-note markers.** No fact in `input_numbers.json` carries a marker saying whether its element sat inside a note. So every fact item is under "Seen in the statements", and "Seen in the notes" holds none. I did not judge note membership myself. Some facts below may come from note tables, for example:
  - concentration percentages
  - geographic amounts
  - capitalized contract cost
  - effective tax rate
  - cyber incident costs

  This input cannot make that split.
- **Where the 8-K items sit.** The 8-K earnings-release figures are items under "Seen in the statements", because only two headings are allowed and the release is not a note.
- **No arithmetic.** Every number below is copied as printed. Where I give two numbers I show them side by side and compute no difference.

## Seen in the statements

### Trend table — quarters-back-0 (2026-04-01..2026-06-30)

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarterly",
  "what_changed": "receivables_over_revenue is 0.4955373914691987 in quarters-back-0. Change against quarters-back-1: -0.02884353744542495. Change against quarters-back-4: 0.0343984445593995. Position as printed: second lowest of the 6 filled quarters. Inputs: AccountsReceivableNetCurrent 428678000.0 at 2026-06-30; quarterly revenue 865077000.0. With 6 filled quarters, a trend claim is insufficient.",
  "account": "AccountsReceivableNetCurrent / RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "none",
  "horizon": "quarters-back-0 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"second lowest of the 6 filled quarters\"",
  "paragraph_id": "0001048695-26-000067:trends:receivables_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly",
  "what_changed": "days_sales_outstanding is 45.093902623697076 in quarters-back-0. Change against quarters-back-1: -2.10038097861905. Change against quarters-back-4: 3.130258454905352. The two changes have opposite signs. Position as printed: second lowest of the 6 filled quarters. Inputs: AccountsReceivableNetCurrent 428678000.0; quarterly revenue 865077000.0. With 6 filled quarters, a trend claim is insufficient.",
  "account": "AccountsReceivableNetCurrent / RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "none",
  "horizon": "quarters-back-0 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"second lowest of the 6 filled quarters\"",
  "paragraph_id": "0001048695-26-000067:trends:days_sales_outstanding:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly",
  "what_changed": "contract_liabilities_over_revenue is 1.4906962039217317 in quarters-back-0. Change against quarters-back-1: -0.07215953095568595. Change against quarters-back-4: -0.048386538879759966. Position as printed: lowest of the 6 filled quarters. Inputs: ContractWithCustomerLiabilityCurrent 1289567000.0 at 2026-06-30; quarterly revenue 865077000.0. The numerator is the current portion only. With 6 filled quarters, a trend claim is insufficient.",
  "account": "ContractWithCustomerLiabilityCurrent / RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "none",
  "horizon": "quarters-back-0 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001048695-26-000067:trends:contract_liabilities_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_quarterly",
  "what_changed": "days_sales_of_inventory is 75.19333958479852 in quarters-back-0. Change against quarters-back-1: 21.338270002293555. Change against quarters-back-4: 34.22044080394969. Position as printed: highest of the 6 filled quarters. Inputs: InventoryNet 126890000.0 at 2026-06-30; CostOfGoodsAndServicesSold 153564000.0 for the quarter. With 6 filled quarters, a trend claim is insufficient.",
  "account": "InventoryNet / CostOfGoodsAndServicesSold",
  "expected_direction": "none",
  "horizon": "quarters-back-0 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001048695-26-000067:trends:days_sales_of_inventory:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly",
  "what_changed": "gross_margin is 0.8224851660603623 in quarters-back-0. Change against quarters-back-1: 0.008391289012191772. Change against quarters-back-4: 0.012943538370932872. Position as printed: highest of the 6 filled quarters. Inputs: quarterly revenue 865077000.0; CostOfGoodsAndServicesSold 153564000.0. With 6 filled quarters, a trend claim is insufficient.",
  "account": "RevenueFromContractWithCustomerExcludingAssessedTax, CostOfGoodsAndServicesSold",
  "expected_direction": "none",
  "horizon": "quarters-back-0 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001048695-26-000067:trends:gross_margin:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_soft_asset_share_quarterly",
  "what_changed": "soft_asset_share is 0.7359721098350962 in quarters-back-0. Change against quarters-back-1: -0.014982261341878522. Change against quarters-back-4: -0.005680910800058836. Position as printed: lowest of the 6 filled quarters. Inputs: Assets 6829074000.0; CashAndCashEquivalentsAtCarryingValue 1605782000.0; PropertyPlantAndEquipmentNet 197284000.0, all at 2026-06-30. With 6 filled quarters, a trend claim is insufficient.",
  "account": "Assets, CashAndCashEquivalentsAtCarryingValue, PropertyPlantAndEquipmentNet",
  "expected_direction": "none",
  "horizon": "quarters-back-0 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001048695-26-000067:trends:soft_asset_share:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly",
  "what_changed": "insufficient. accruals_over_total_assets is not filled in quarters-back-0. The cell gives no operating cash flow for 2026-04-01..2026-06-30. Both its quarter_over_quarter and year_over_year read: accruals_over_total_assets is not filled in quarters-back-0. Across the table the quarterly measure is filled in only 2 quarters (quarters-back-2 and quarters-back-6).",
  "account": "NetIncomeLoss, NetCashProvidedByUsedInOperatingActivities, Assets",
  "expected_direction": "none",
  "horizon": "quarters-back-0",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-04-01..2026-06-30: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0001048695-26-000067:trends:accruals_over_total_assets:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly",
  "what_changed": "insufficient. non_gaap_gap is not filled in quarters-back-0, because companyfacts carries no non-GAAP measure. The table holds no gap number, and I compute none.",
  "account": "non-GAAP net income against NetIncomeLoss",
  "expected_direction": "none",
  "horizon": "quarters-back-0",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001048695-26-000067:trends:non_gaap_gap:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly",
  "what_changed": "bad_debt_reserve_ratio is 0.006461691071834166 in quarters-back-0. Change against quarters-back-1: -0.0009378047456900232. Change against quarters-back-4: -0.0025815783840000377. Position as printed: lowest of the 4 filled quarters on the same concepts; 2 other filled quarters rest on a different concept and are not compared. Inputs: AllowanceForDoubtfulAccountsReceivable 2788000.0 and AccountsReceivableNetCurrent 428678000.0 at 2026-06-30. With 4 same-concept quarters, a trend claim is insufficient.",
  "account": "AllowanceForDoubtfulAccountsReceivable / (AccountsReceivableNetCurrent + allowance)",
  "expected_direction": "none",
  "horizon": "quarters-back-0 against quarters-back-1 and quarters-back-4",
  "quote": "\"position_in_history\": \"lowest of the 4 filled quarters on the same concepts; 2 other filled quarters rest on a different concept and are not compared\"",
  "paragraph_id": "0001048695-26-000067:trends:bad_debt_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly",
  "what_changed": "insufficient. inventory_reserve_ratio is not filled in quarters-back-0. us-gaap:InventoryValuationReserves is tagged in no period of the record. The trend table fills this ratio in 0 periods.",
  "account": "InventoryValuationReserves",
  "expected_direction": "none",
  "horizon": "quarters-back-0",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001048695-26-000067:trends:inventory_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly",
  "what_changed": "insufficient. warranty_reserve_ratio is not filled in quarters-back-0. The warranty accrual concepts are in the record but not for 2026-06-30. The trend table fills this ratio in 0 periods.",
  "account": "StandardProductWarrantyAccrual, ProductWarrantyAccrual, StandardProductWarrantyAccrualCurrent",
  "expected_direction": "none",
  "horizon": "quarters-back-0",
  "quote": "\"missing\": \"no row for warranty_accrual in 2026-06-30: us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent is in the record, but not for this period\"",
  "paragraph_id": "0001048695-26-000067:trends:warranty_reserve_ratio:2026-04-01..2026-06-30" }
```

### Trend table — years-back-0 (2024-10-01..2025-09-30)

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual",
  "what_changed": "receivables_over_revenue is 0.13420444860093936 in years-back-0. Change against years-back-1: -0.003937391945628255. quarter_over_quarter reads: an annual period has no preceding quarter. Position as printed: second lowest of the 5 filled years. Inputs: AccountsReceivableNetCurrent 414433000.0 at 2025-09-30; annual revenue 3088072000.0. With 5 filled years, a trend claim is insufficient.",
  "account": "AccountsReceivableNetCurrent / RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "none",
  "horizon": "years-back-0 against years-back-1",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001048695-26-000067:trends:receivables_over_revenue:2024-10-01..2025-09-30" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual",
  "what_changed": "days_sales_outstanding is 48.984623739342865 in years-back-0. Change against years-back-1: -1.5752899007008807. Position as printed: second lowest of the 5 filled years. Inputs: AccountsReceivableNetCurrent 414433000.0; annual revenue 3088072000.0. With 5 filled years, a trend claim is insufficient.",
  "account": "AccountsReceivableNetCurrent / RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "none",
  "horizon": "years-back-0 against years-back-1",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001048695-26-000067:trends:days_sales_outstanding:2024-10-01..2025-09-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual",
  "what_changed": "contract_liabilities_over_revenue is 0.39287490706175243 in years-back-0. Change against years-back-1: -0.0054330485651384874. Position as printed: second lowest of the 5 filled years. Inputs: ContractWithCustomerLiabilityCurrent 1213226000.0 at 2025-09-30; annual revenue 3088072000.0. This value uses a year's revenue, while the quarterly cell uses a quarter's, so the two are not on one scale. With 5 filled years, a trend claim is insufficient.",
  "account": "ContractWithCustomerLiabilityCurrent / RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "none",
  "horizon": "years-back-0 against years-back-1",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0001048695-26-000067:trends:contract_liabilities_over_revenue:2024-10-01..2025-09-30" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_annual",
  "what_changed": "days_sales_of_inventory is 49.110915400938715 in years-back-0. Change against years-back-1: -1.0181949502332657. Position as printed: second highest of the 5 filled years. Inputs: InventoryNet 77229000.0 at 2025-09-30; CostOfGoodsAndServicesSold 573978000.0 for the year. With 5 filled years, a trend claim is insufficient.",
  "account": "InventoryNet / CostOfGoodsAndServicesSold",
  "expected_direction": "none",
  "horizon": "years-back-0 against years-back-1",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001048695-26-000067:trends:days_sales_of_inventory:2024-10-01..2025-09-30" }
```

```json
{ "id": "earnings_quality_gross_margin_annual",
  "what_changed": "gross_margin is 0.8141306290785966 in years-back-0. Change against years-back-1: 0.0121502447199755. Position as printed: highest of the 5 filled years. Inputs: annual revenue 3088072000.0; CostOfGoodsAndServicesSold 573978000.0. With 5 filled years, a trend claim is insufficient.",
  "account": "RevenueFromContractWithCustomerExcludingAssessedTax, CostOfGoodsAndServicesSold",
  "expected_direction": "none",
  "horizon": "years-back-0 against years-back-1",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001048695-26-000067:trends:gross_margin:2024-10-01..2025-09-30" }
```

```json
{ "id": "earnings_quality_soft_asset_share_annual",
  "what_changed": "soft_asset_share is 0.7624460953507023 in years-back-0. Change against years-back-1: -0.019213600598204872. Position as printed: lowest of the 5 filled years. Inputs: Assets 6319492000.0; cash 1344273000.0; PropertyPlantAndEquipmentNet 156947000.0, all at 2025-09-30. With 5 filled years, a trend claim is insufficient.",
  "account": "Assets, CashAndCashEquivalentsAtCarryingValue, PropertyPlantAndEquipmentNet",
  "expected_direction": "none",
  "horizon": "years-back-0 against years-back-1",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001048695-26-000067:trends:soft_asset_share:2024-10-01..2025-09-30" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_annual",
  "what_changed": "accruals_over_total_assets is -0.04071308263385728 in years-back-0. Change against years-back-1: -0.0005133963339722242. Position as printed: third highest of the 5 filled years. Inputs: NetIncomeLoss 692380000.0 and NetCashProvidedByUsedInOperatingActivities 949666000.0, both from the 10-K 0001048695-25-000157; Assets 6319492000.0. With 5 filled years, a trend claim is insufficient.",
  "account": "NetIncomeLoss, NetCashProvidedByUsedInOperatingActivities, Assets",
  "expected_direction": "none",
  "horizon": "years-back-0 against years-back-1",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001048695-26-000067:trends:accruals_over_total_assets:2024-10-01..2025-09-30" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual",
  "what_changed": "insufficient. non_gaap_gap is not filled in years-back-0. year_over_year reads: non_gaap_gap is not filled in years-back-0. The table holds no gap number.",
  "account": "non-GAAP net income against NetIncomeLoss",
  "expected_direction": "none",
  "horizon": "years-back-0",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001048695-26-000067:trends:non_gaap_gap:2024-10-01..2025-09-30" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual",
  "what_changed": "bad_debt_reserve_ratio is 0.006894155424025305 in years-back-0. Change against years-back-1: -0.004754460334252579. Position as printed: lowest of the 5 filled years. Inputs: AllowanceForDoubtfulAccountsReceivableCurrent 2877000.0, taken from 10-Q 0001048695-26-000023; AccountsReceivableNetCurrent 414433000.0. The allowance concept here differs from the one in the quarters-back-0 cell; see the structure items. With 5 filled years, a trend claim is insufficient.",
  "account": "AllowanceForDoubtfulAccountsReceivableCurrent / (AccountsReceivableNetCurrent + allowance)",
  "expected_direction": "none",
  "horizon": "years-back-0 against years-back-1",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001048695-26-000067:trends:bad_debt_reserve_ratio:2024-10-01..2025-09-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_annual",
  "what_changed": "insufficient. inventory_reserve_ratio is not filled in years-back-0. The record tags no InventoryValuationReserves in any period. year_over_year reads: inventory_reserve_ratio is not filled in years-back-0.",
  "account": "InventoryValuationReserves",
  "expected_direction": "none",
  "horizon": "years-back-0",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001048695-26-000067:trends:inventory_reserve_ratio:2024-10-01..2025-09-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_annual",
  "what_changed": "insufficient. warranty_reserve_ratio is not filled in years-back-0. The warranty accrual concepts are in the record but not for 2025-09-30.",
  "account": "StandardProductWarrantyAccrual, ProductWarrantyAccrual, StandardProductWarrantyAccrualCurrent",
  "expected_direction": "none",
  "horizon": "years-back-0",
  "quote": "\"missing\": \"no row for warranty_accrual in 2025-09-30: us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent is in the record, but not for this period\"",
  "paragraph_id": "0001048695-26-000067:trends:warranty_reserve_ratio:2024-10-01..2025-09-30" }
```

### Changes of tag

```json
{ "id": "structure_and_disclosure_changes_bad_debt_allowance_concept_latest_quarters",
  "what_changed": "The trend table says bad_debt_reserve_ratio rests on a different concept in quarters-back-1 than in quarters-back-2, so it prints no quarter-over-quarter change for quarters-back-1. quarters-back-1 uses AllowanceForDoubtfulAccountsReceivable; quarters-back-2 uses AllowanceForDoubtfulAccountsReceivableCurrent.",
  "account": "AllowanceForDoubtfulAccountsReceivable / AllowanceForDoubtfulAccountsReceivableCurrent",
  "expected_direction": "none",
  "horizon": "quarters-back-1 against quarters-back-2",
  "quote": "bad_debt_allowance: us-gaap:AllowanceForDoubtfulAccountsReceivable in quarters-back-1 and us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent in quarters-back-2",
  "paragraph_id": "0001048695-26-000067:trends:bad_debt_reserve_ratio:2026-01-01..2026-03-31" }
```

```json
{ "id": "structure_and_disclosure_changes_bad_debt_allowance_concept_earlier_quarters",
  "what_changed": "The same concept switch appears one fiscal year earlier. quarters-back-5 uses AllowanceForDoubtfulAccountsReceivable; quarters-back-6 uses AllowanceForDoubtfulAccountsReceivableCurrent. No quarter-over-quarter change is printed for quarters-back-5.",
  "account": "AllowanceForDoubtfulAccountsReceivable / AllowanceForDoubtfulAccountsReceivableCurrent",
  "expected_direction": "none",
  "horizon": "quarters-back-5 against quarters-back-6",
  "quote": "bad_debt_allowance: us-gaap:AllowanceForDoubtfulAccountsReceivable in quarters-back-5 and us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent in quarters-back-6",
  "paragraph_id": "0001048695-26-000067:trends:bad_debt_reserve_ratio:2025-01-01..2025-03-31" }
```

```json
{ "id": "structure_and_disclosure_changes_bad_debt_allowance_current_concept_cells",
  "what_changed": "The quarters-back-2 bad_debt_reserve_ratio cell, 0.00580452720897305, rests on AllowanceForDoubtfulAccountsReceivableCurrent 2882000.0 from 10-Q 0001048695-26-000023. It is compared only with the one other quarter on that concept. Its position reads as quoted. So the bad-debt quarterly history is split into two concept groups: 4 quarters and 2 quarters.",
  "account": "AllowanceForDoubtfulAccountsReceivableCurrent",
  "expected_direction": "none",
  "horizon": "quarters-back-2 against quarters-back-6",
  "quote": "\"position_in_history\": \"lowest of the 2 filled quarters on the same concepts; 4 other filled quarters rest on a different concept and are not compared\"",
  "paragraph_id": "0001048695-26-000067:trends:bad_debt_reserve_ratio:2025-10-01..2025-12-31" }
```


```json
{ "id": "structure_and_disclosure_changes_bad_debt_allowance_concept_retagged_fact",
  "what_changed": "The current 10-Q reports the 2025-09-30 allowance under AllowanceForDoubtfulAccountsReceivable at 2877000. That is the same amount the trend table takes from AllowanceForDoubtfulAccountsReceivableCurrent for 2025-09-30. Same period and same amount, but a different concept between filings. The 8-K balance sheet caption shows allowances of $2,788 and $2,877 (thousands). This is a change of tag, not of value.",
  "account": "AllowanceForDoubtfulAccountsReceivable",
  "expected_direction": "none",
  "horizon": "balance at 2025-09-30 as reported in successive filings",
  "quote": "\"value\": \"2877000\"",
  "paragraph_id": "0001048695-26-000067:facts:AllowanceForDoubtfulAccountsReceivable:2025-09-30" }
```

```json
{ "id": "structure_and_disclosure_changes_geographic_long_lived_assets_annual_filing_concept",
  "what_changed": "The 10-K tags long-lived assets by geography at 2025-09-30 as PropertyPlantAndEquipmentNet with srt:StatementGeographicalAxis. For the US member the value is 118414000. The other members also carry values that the 10-Qs report: OtherAmericas 1696000, Americas 120110000, EMEA 20985000, AsiaPacific 15852000. These 10-K geographic facts carry no superseded_by marker, though the 10-Qs report the same amounts under another concept.",
  "account": "PropertyPlantAndEquipmentNet (geographic)",
  "expected_direction": "none",
  "horizon": "balance at 2025-09-30 as reported in successive filings",
  "quote": "\"value\": \"118414000\"",
  "paragraph_id": "0001048695-25-000157:facts:PropertyPlantAndEquipmentNet:2025-09-30:srt:StatementGeographicalAxis=country:US" }
```

```json
{ "id": "structure_and_disclosure_changes_geographic_long_lived_assets_quarterly_filing_concept",
  "what_changed": "10-Q 0001048695-26-000051 reports the same 2025-09-30 geographic amounts under NoncurrentAssets instead of PropertyPlantAndEquipmentNet. US is 118414000; the total NoncurrentAssets at 2025-09-30 is 156947000, the same amount as PropertyPlantAndEquipmentNet on the balance sheet. The fact is marked superseded_by 0001048695-26-000067, which keeps NoncurrentAssets. Same period and same amount under a different concept between the 10-K and the 10-Qs. The input does not flag this change itself.",
  "account": "NoncurrentAssets (geographic)",
  "expected_direction": "none",
  "horizon": "balance at 2025-09-30 as reported in successive filings",
  "quote": "\"value\": \"118414000\"",
  "paragraph_id": "0001048695-26-000051:facts:NoncurrentAssets:2025-09-30:srt:StatementGeographicalAxis=country:US" }
```

```json
{ "id": "structure_and_disclosure_changes_customer_concentration_members_annual_filing",
  "what_changed": "The 10-K tags customer concentration with members CustomerA, CustomerB, CustomerC and CustomerD and type GeographicConcentrationRiskMember. CustomerB's share of fiscal 2025 revenue is 0.175. The 10-Qs tag WorldwideDistributor1 and WorldwideDistributor2 with type CustomerConcentrationRiskMember. The periods differ, and the input does not link the 10-K members to the 10-Q members, so the two cannot be compared. This is a change in how the disclosure is tagged.",
  "account": "ConcentrationRiskPercentage1",
  "expected_direction": "none",
  "horizon": "fiscal year to 2025-09-30 (10-K) against the 10-Q periods",
  "quote": "\"value\": \"0.175\"",
  "paragraph_id": "0001048695-25-000157:facts:ConcentrationRiskPercentage1:2024-10-01..2025-09-30:srt:MajorCustomersAxis=ffiv:CustomerBMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:SalesRevenueNetMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:GeographicConcentrationRiskMember" }
```

```json
{ "id": "structure_and_disclosure_changes_contract_cost_amortization_tagged_twice",
  "what_changed": "In 10-Q 0001048695-26-000067, two facts share this paragraph_id, both for nine-month CapitalizedContractCostAmortization: 32033000 at decimals -3 and 32000000.0 at decimals -5. The prior nine months likewise show 28261000 and 28300000. This is the same concept and period at two roundings within one filing, not a restatement.",
  "account": "CapitalizedContractCostAmortization",
  "expected_direction": "none",
  "horizon": "nine months to 2026-06-30",
  "quote": "\"value\": \"32000000.0\"",
  "paragraph_id": "0001048695-26-000067:facts:CapitalizedContractCostAmortization:2025-10-01..2026-06-30" }
```

### Numeric facts — 10-Q 0001048695-26-000067 and 0001048695-26-000051

```json
{ "id": "earnings_quality_inventory_balance",
  "what_changed": "InventoryNet is 126890000 at 2026-06-30, against 77229000 at 2025-09-30. These are the inputs behind days_sales_of_inventory sitting highest of 6 filled quarters. The facts also split the balance at the same two dates: raw materials 95875000 against 50296000, finished goods 31015000 against 26933000.",
  "account": "InventoryNet",
  "expected_direction": "none",
  "horizon": "2026-06-30 against 2025-09-30",
  "quote": "\"value\": \"126890000\"",
  "paragraph_id": "0001048695-26-000067:facts:InventoryNet:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_inventory_cash_outflow",
  "what_changed": "IncreaseDecreaseInInventories is 49661000 for the nine months to 2026-06-30, against -9458000 for the nine months to 2025-06-30. A positive value in this concept is an increase in inventory. The 8-K cash flow shows it as (49,661).",
  "account": "IncreaseDecreaseInInventories",
  "expected_direction": "none",
  "horizon": "nine months to 2026-06-30 against nine months to 2025-06-30",
  "quote": "\"value\": \"49661000\"",
  "paragraph_id": "0001048695-26-000067:facts:IncreaseDecreaseInInventories:2025-10-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_other_current_assets_balance",
  "what_changed": "OtherAssetsCurrent is 785623000 at 2026-06-30, against 682766000 at 2025-09-30.",
  "account": "OtherAssetsCurrent",
  "expected_direction": "none",
  "horizon": "2026-06-30 against 2025-09-30",
  "quote": "\"value\": \"785623000\"",
  "paragraph_id": "0001048695-26-000067:facts:OtherAssetsCurrent:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_other_current_assets_cash_outflow",
  "what_changed": "IncreaseDecreaseInOtherCurrentAssets is 101005000 for the nine months to 2026-06-30, against 54523000 for the nine months to 2025-06-30.",
  "account": "IncreaseDecreaseInOtherCurrentAssets",
  "expected_direction": "none",
  "horizon": "nine months to 2026-06-30 against nine months to 2025-06-30",
  "quote": "\"value\": \"101005000\"",
  "paragraph_id": "0001048695-26-000067:facts:IncreaseDecreaseInOtherCurrentAssets:2025-10-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_receivables_cash_flow_change",
  "what_changed": "IncreaseDecreaseInAccountsReceivable is 14262000 for the nine months to 2026-06-30, against -26834000 for the nine months to 2025-06-30. The balance is 428678000 at 2026-06-30 against 414433000 at 2025-09-30.",
  "account": "IncreaseDecreaseInAccountsReceivable",
  "expected_direction": "none",
  "horizon": "nine months to 2026-06-30 against nine months to 2025-06-30",
  "quote": "\"value\": \"14262000\"",
  "paragraph_id": "0001048695-26-000067:facts:IncreaseDecreaseInAccountsReceivable:2025-10-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_operating_cash_flow",
  "what_changed": "NetCashProvidedByUsedInOperatingActivities is 841373000 for the nine months to 2026-06-30, against 741598000 for the nine months to 2025-06-30. No quarterly operating cash flow is in the record, which is why the quarterly accruals cell is unfilled.",
  "account": "NetCashProvidedByUsedInOperatingActivities",
  "expected_direction": "none",
  "horizon": "nine months to 2026-06-30 against nine months to 2025-06-30",
  "quote": "\"value\": \"841373000\"",
  "paragraph_id": "0001048695-26-000067:facts:NetCashProvidedByUsedInOperatingActivities:2025-10-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_capital_expenditure",
  "what_changed": "PaymentsToAcquirePropertyPlantAndEquipment is 63705000 for the nine months to 2026-06-30, against 27119000 for the nine months to 2025-06-30. PropertyPlantAndEquipmentNet is 197284000 at 2026-06-30 against 156947000 at 2025-09-30.",
  "account": "PaymentsToAcquirePropertyPlantAndEquipment",
  "expected_direction": "none",
  "horizon": "nine months to 2026-06-30 against nine months to 2025-06-30",
  "quote": "\"value\": \"63705000\"",
  "paragraph_id": "0001048695-26-000067:facts:PaymentsToAcquirePropertyPlantAndEquipment:2025-10-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_acquisition_payments",
  "what_changed": "PaymentsToAcquireBusinessesNetOfCashAcquired is 47619000 for the nine months to 2026-06-30, against 24170000 for the nine months to 2025-06-30. Goodwill is 2482495000 at 2026-06-30 against 2443882000 at 2025-09-30.",
  "account": "PaymentsToAcquireBusinessesNetOfCashAcquired",
  "expected_direction": "none",
  "horizon": "nine months to 2026-06-30 against nine months to 2025-06-30",
  "quote": "\"value\": \"47619000\"",
  "paragraph_id": "0001048695-26-000067:facts:PaymentsToAcquireBusinessesNetOfCashAcquired:2025-10-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_share_repurchase_payments",
  "what_changed": "PaymentsForRepurchaseOfCommonStock is 501109000 for the nine months to 2026-06-30, against 377077000 for the nine months to 2025-06-30. Repurchased value is 100007000 for the quarter against 125010000 a year earlier. Average cost per share is 299.34 for the quarter against 256.23 a year earlier. Remaining authorization is 422400000 at 2026-06-30.",
  "account": "PaymentsForRepurchaseOfCommonStock",
  "expected_direction": "none",
  "horizon": "nine months to 2026-06-30 against nine months to 2025-06-30",
  "quote": "\"value\": \"501109000\"",
  "paragraph_id": "0001048695-26-000067:facts:PaymentsForRepurchaseOfCommonStock:2025-10-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_accounts_payable_balance",
  "what_changed": "AccountsPayableCurrent is 136157000 at 2026-06-30, against 83972000 at 2025-09-30.",
  "account": "AccountsPayableCurrent",
  "expected_direction": "none",
  "horizon": "2026-06-30 against 2025-09-30",
  "quote": "\"value\": \"136157000\"",
  "paragraph_id": "0001048695-26-000067:facts:AccountsPayableCurrent:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_payables_and_accruals_cash_change",
  "what_changed": "IncreaseDecreaseInAccountsPayableAndAccruedLiabilities is 50995000 for the nine months to 2026-06-30, against -19031000 for the nine months to 2025-06-30.",
  "account": "IncreaseDecreaseInAccountsPayableAndAccruedLiabilities",
  "expected_direction": "none",
  "horizon": "nine months to 2026-06-30 against nine months to 2025-06-30",
  "quote": "\"value\": \"50995000\"",
  "paragraph_id": "0001048695-26-000067:facts:IncreaseDecreaseInAccountsPayableAndAccruedLiabilities:2025-10-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_deferred_revenue_current_balance",
  "what_changed": "ContractWithCustomerLiabilityCurrent is 1289567000 at 2026-06-30, against 1213226000 at 2025-09-30. This is the numerator of contract_liabilities_over_revenue, which sits lowest of 6 filled quarters on a quarter's revenue.",
  "account": "ContractWithCustomerLiabilityCurrent",
  "expected_direction": "none",
  "horizon": "2026-06-30 against 2025-09-30",
  "quote": "\"value\": \"1289567000\"",
  "paragraph_id": "0001048695-26-000067:facts:ContractWithCustomerLiabilityCurrent:2026-06-30" }
```

```json
{ "id": "revenue_recognition_deferred_revenue_noncurrent_balance",
  "what_changed": "ContractWithCustomerLiabilityNoncurrent is 903131000 at 2026-06-30, against 786011000 at 2025-09-30. The trend ratio leaves out the non-current portion.",
  "account": "ContractWithCustomerLiabilityNoncurrent",
  "expected_direction": "none",
  "horizon": "2026-06-30 against 2025-09-30",
  "quote": "\"value\": \"903131000\"",
  "paragraph_id": "0001048695-26-000067:facts:ContractWithCustomerLiabilityNoncurrent:2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liability_cash_change",
  "what_changed": "IncreaseDecreaseInContractWithCustomerLiability is 192266000 for the nine months to 2026-06-30, against 159003000 for the nine months to 2025-06-30. Revenue recognized from the opening contract liability is -1025461000 against -964083000. Contract liability acquired in a business combination is 1195000 against 0.",
  "account": "IncreaseDecreaseInContractWithCustomerLiability",
  "expected_direction": "none",
  "horizon": "nine months to 2026-06-30 against nine months to 2025-06-30",
  "quote": "\"value\": \"192266000\"",
  "paragraph_id": "0001048695-26-000067:facts:IncreaseDecreaseInContractWithCustomerLiability:2025-10-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_capitalized_contract_cost_balance",
  "what_changed": "CapitalizedContractCostNet is 87035000 at 2026-06-30. It is 76552000 at 2025-09-30 and 72292000 at 2025-06-30. Amortization is 32033000 for the nine months to 2026-06-30, against 28261000 a year earlier. Impairment is 0 in both nine-month periods.",
  "account": "CapitalizedContractCostNet",
  "expected_direction": "none",
  "horizon": "2026-06-30 against 2025-09-30 and 2025-06-30",
  "quote": "\"value\": \"87035000\"",
  "paragraph_id": "0001048695-26-000067:facts:CapitalizedContractCostNet:2026-06-30" }
```

```json
{ "id": "earnings_quality_effective_tax_rate",
  "what_changed": "EffectiveIncomeTaxRateContinuingOperations is 0.080 for the quarter to 2026-06-30, against 0.108 for the quarter to 2025-06-30. For the nine months it is 0.160, against 0.154.",
  "account": "EffectiveIncomeTaxRateContinuingOperations",
  "expected_direction": "none",
  "horizon": "quarter to 2026-06-30 against quarter to 2025-06-30",
  "quote": "\"value\": \"0.080\"",
  "paragraph_id": "0001048695-26-000067:facts:EffectiveIncomeTaxRateContinuingOperations:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_cyber_incident_costs",
  "what_changed": "OtherNonrecurringExpense on the CyberIncidentMember is 3000000.0 for the quarter to 2026-06-30 and 26500000 for the nine months. The 8-K non-GAAP reconciliation excludes cyber incident costs.",
  "account": "OtherNonrecurringExpense (CyberIncidentMember)",
  "expected_direction": "none",
  "horizon": "quarter and nine months to 2026-06-30",
  "quote": "\"value\": \"3000000.0\"",
  "paragraph_id": "0001048695-26-000067:facts:OtherNonrecurringExpense:2026-04-01..2026-06-30:us-gaap:OtherCommitmentsAxis=ffiv:CyberIncidentMember" }
```

```json
{ "id": "earnings_quality_cyber_insurance_recoveries",
  "what_changed": "InsuranceRecoveries is 5300000 for the quarter to 2026-06-30 and also 5300000 for the nine months; the two print the same. The 8-K excludes insurance recoveries from non-GAAP measures.",
  "account": "InsuranceRecoveries",
  "expected_direction": "none",
  "horizon": "quarter and nine months to 2026-06-30",
  "quote": "\"value\": \"5300000\"",
  "paragraph_id": "0001048695-26-000067:facts:InsuranceRecoveries:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_second_distributor_concentration_quarterly",
  "what_changed": "ConcentrationRiskPercentage1 for WorldwideDistributor2 (share of revenue) is 0.184 for the quarter to 2026-06-30. It is also 0.184 for the quarter to 2025-06-30.",
  "account": "ConcentrationRiskPercentage1 (WorldwideDistributor2, revenue)",
  "expected_direction": "none",
  "horizon": "quarter to 2026-06-30 against quarter to 2025-06-30",
  "quote": "\"value\": \"0.184\"",
  "paragraph_id": "0001048695-26-000067:facts:ConcentrationRiskPercentage1:2026-04-01..2026-06-30:srt:MajorCustomersAxis=ffiv:WorldwideDistributor2Member,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:SalesRevenueNetMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember" }
```

```json
{ "id": "revenue_recognition_second_distributor_concentration_cumulative",
  "what_changed": "ConcentrationRiskPercentage1 for WorldwideDistributor2 (share of revenue) is 0.231 for the nine months to 2026-06-30, against 0.176 for the nine months to 2025-06-30.",
  "account": "ConcentrationRiskPercentage1 (WorldwideDistributor2, revenue)",
  "expected_direction": "none",
  "horizon": "nine months to 2026-06-30 against nine months to 2025-06-30",
  "quote": "\"value\": \"0.231\"",
  "paragraph_id": "0001048695-26-000067:facts:ConcentrationRiskPercentage1:2025-10-01..2026-06-30:srt:MajorCustomersAxis=ffiv:WorldwideDistributor2Member,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:SalesRevenueNetMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember" }
```

```json
{ "id": "revenue_recognition_first_distributor_concentration_quarterly",
  "what_changed": "ConcentrationRiskPercentage1 for WorldwideDistributor1 (share of revenue) is 0.164 for the quarter to 2026-06-30, against 0.170 for the quarter to 2025-06-30. For the nine months it is 0.172, against 0.167.",
  "account": "ConcentrationRiskPercentage1 (WorldwideDistributor1, revenue)",
  "expected_direction": "none",
  "horizon": "quarter to 2026-06-30 against quarter to 2025-06-30",
  "quote": "\"value\": \"0.164\"",
  "paragraph_id": "0001048695-26-000067:facts:ConcentrationRiskPercentage1:2026-04-01..2026-06-30:srt:MajorCustomersAxis=ffiv:WorldwideDistributor1Member,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:SalesRevenueNetMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember" }
```

```json
{ "id": "revenue_recognition_systems_revenue",
  "what_changed": "Systems product revenue is 239519000 for the quarter to 2026-06-30, against 180855000 for the quarter to 2025-06-30. For the nine months it is 684264000, against 519968000.",
  "account": "RevenueFromContractWithCustomerExcludingAssessedTax (SystemsMember, ProductMember)",
  "expected_direction": "none",
  "horizon": "quarter to 2026-06-30 against quarter to 2025-06-30",
  "quote": "\"value\": \"239519000\"",
  "paragraph_id": "0001048695-26-000067:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:ffiv:SystemsAndSoftwareAxis=ffiv:SystemsMember,srt:ProductOrServiceAxis=us-gaap:ProductMember" }
```

```json
{ "id": "revenue_recognition_software_revenue",
  "what_changed": "Software product revenue is 223310000 for the quarter to 2026-06-30, against 207983000 for the quarter to 2025-06-30. For the nine months it is 599363000, against 574563000. Services revenue is 402248000, against 391532000.",
  "account": "RevenueFromContractWithCustomerExcludingAssessedTax (SoftwareMember, ProductMember)",
  "expected_direction": "none",
  "horizon": "quarter to 2026-06-30 against quarter to 2025-06-30",
  "quote": "\"value\": \"223310000\"",
  "paragraph_id": "0001048695-26-000067:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:ffiv:SystemsAndSoftwareAxis=ffiv:SoftwareMember,srt:ProductOrServiceAxis=us-gaap:ProductMember" }
```

```json
{ "id": "revenue_recognition_asia_pacific_revenue",
  "what_changed": "Asia Pacific revenue is 130484000 for the quarter to 2026-06-30, against 147326000 for the quarter to 2025-06-30. It is the one geographic member whose quarterly value is lower than a year earlier. For the nine months it is 403420000, against 398481000.",
  "account": "RevenueFromContractWithCustomerExcludingAssessedTax (AsiaPacificMember)",
  "expected_direction": "none",
  "horizon": "quarter to 2026-06-30 against quarter to 2025-06-30",
  "quote": "\"value\": \"130484000\"",
  "paragraph_id": "0001048695-26-000067:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:StatementGeographicalAxis=srt:AsiaPacificMember" }
```

```json
{ "id": "revenue_recognition_emea_revenue",
  "what_changed": "EMEA revenue is 256030000 for the quarter to 2026-06-30, against 202073000 for the quarter to 2025-06-30. For the nine months it is 770600000, against 620431000. Americas is 478563000 against 430971000; US is 453985000 against 411093000.",
  "account": "RevenueFromContractWithCustomerExcludingAssessedTax (EMEAMember)",
  "expected_direction": "none",
  "horizon": "quarter to 2026-06-30 against quarter to 2025-06-30",
  "quote": "\"value\": \"256030000\"",
  "paragraph_id": "0001048695-26-000067:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:StatementGeographicalAxis=us-gaap:EMEAMember" }
```

```json
{ "id": "estimates_and_discretion_deferred_tax_assets",
  "what_changed": "DeferredIncomeTaxAssetsNet is 487177000 at 2026-06-30, against 446388000 at 2025-09-30.",
  "account": "DeferredIncomeTaxAssetsNet",
  "expected_direction": "none",
  "horizon": "2026-06-30 against 2025-09-30",
  "quote": "\"value\": \"487177000\"",
  "paragraph_id": "0001048695-26-000067:facts:DeferredIncomeTaxAssetsNet:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_goodwill_balance",
  "what_changed": "Goodwill is 2482495000 at 2026-06-30, against 2443882000 at 2025-09-30. Business acquisition payments in the nine months are 47619000, net of cash acquired.",
  "account": "Goodwill",
  "expected_direction": "none",
  "horizon": "2026-06-30 against 2025-09-30",
  "quote": "\"value\": \"2482495000\"",
  "paragraph_id": "0001048695-26-000067:facts:Goodwill:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_unrecognized_tax_benefits",
  "what_changed": "UnrecognizedTaxBenefits is 72700000 at 2026-06-30. This item makes no comparison. AccruedIncomeTaxesNoncurrent, in the facts, is 66829000 at 2026-06-30 against 85278000 at 2025-09-30.",
  "account": "UnrecognizedTaxBenefits",
  "expected_direction": "none",
  "horizon": "2026-06-30",
  "quote": "\"value\": \"72700000\"",
  "paragraph_id": "0001048695-26-000067:facts:UnrecognizedTaxBenefits:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_restructuring_reserve_reversal",
  "what_changed": "In the prior 10-Q, RestructuringReservePeriodIncreaseDecrease is -358000 for the six months to 2026-03-31, against 11321000 for the six months to 2025-03-31. The restructuring reserve is 41000 at 2026-03-31 and 8846000 at 2025-09-30. The 8-K income statement shows restructuring charges of (30) for the quarter and (388) for the nine months to 2026-06-30, against 11,321 a year earlier (thousands).",
  "account": "RestructuringReservePeriodIncreaseDecrease",
  "expected_direction": "none",
  "horizon": "six months to 2026-03-31 against six months to 2025-03-31",
  "quote": "\"value\": \"-358000\"",
  "paragraph_id": "0001048695-26-000051:facts:RestructuringReservePeriodIncreaseDecrease:2025-10-01..2026-03-31" }
```

### 8-K earnings release 0001048695-26-000063

```json
{ "id": "results_against_expectations_full_year_revenue_guidance_raise",
  "what_changed": "The release raises full-year revenue growth guidance to approximately 9% to 10%, from 7% to 8%. This is the company's own stated expectation, not mine.",
  "account": "RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "up",
  "horizon": "fiscal year ending 2026-09-30",
  "quote": "F5 raised its outlook for its fiscal year 2026, guiding for revenue growth of approximately 9% to 10%, up from 7% to 8% previously.",
  "paragraph_id": "0001048695-26-000063:8k_2_02:21" }
```

```json
{ "id": "results_against_expectations_full_year_earnings_guidance_raise",
  "what_changed": "The release raises non-GAAP EPS guidance to $17.21 to $17.33, from $16.25 to $16.55. The record holds no non-GAAP measure (non_gaap_gap is insufficient in every period), so this guidance cannot be tied to a filed figure.",
  "account": "non-GAAP earnings per share",
  "expected_direction": "up",
  "horizon": "fiscal year ending 2026-09-30",
  "quote": "F5 expects non-GAAP earnings per share in a range of $17.21 to $17.33, up from $16.25 to $16.55 previously.",
  "paragraph_id": "0001048695-26-000063:8k_2_02:21" }
```

```json
{ "id": "results_against_expectations_next_quarter_guidance",
  "what_changed": "The release guides next-quarter revenue to $870 million to $890 million and non-GAAP EPS to $4.14 to $4.26. The record holds no quarterly duration for the fiscal fourth quarter (quarters-back-3 is not reached), so there is no filed prior-year comparison in my input.",
  "account": "RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "none",
  "horizon": "quarter ending 2026-09-30",
  "quote": "For the fourth quarter of fiscal year 2026, F5 is guiding to revenue in the range of $870 million to $890 million, with non-GAAP earnings in the range of $4.14 to $4.26 per diluted share.",
  "paragraph_id": "0001048695-26-000063:8k_2_02:22" }
```

```json
{ "id": "across_documents_release_revenue_against_filing",
  "what_changed": "The release states quarterly revenue of $865 million against $780 million. The 10-Q facts are 865077000 and 780370000. I compare them only at the release's stated rounding and compute nothing.",
  "account": "RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "none",
  "horizon": "quarter to 2026-06-30 against quarter to 2025-06-30",
  "quote": "Third quarter fiscal year 2026 revenue totaled $865 million, representing 11% growth compared with $780 million in the third quarter of fiscal year 2025.",
  "paragraph_id": "0001048695-26-000063:8k_2_02:11" }
```

```json
{ "id": "across_documents_release_product_mix_against_filing",
  "what_changed": "The release states systems revenue of $240 million (grew 32%) and software revenue of $223 million (grew 7%). The 10-Q facts are 239519000 against 180855000 for systems and 223310000 against 207983000 for software.",
  "account": "RevenueFromContractWithCustomerExcludingAssessedTax (SystemsMember, SoftwareMember)",
  "expected_direction": "none",
  "horizon": "quarter to 2026-06-30 against quarter to 2025-06-30",
  "quote": "Systems revenue of $240 million grew 32% from the year-ago period while software revenue of $223 million grew 7%.",
  "paragraph_id": "0001048695-26-000063:8k_2_02:11" }
```

```json
{ "id": "across_documents_release_gross_margin_against_trend",
  "what_changed": "The release states a GAAP gross margin of 82.2%, against 81.0% a year earlier. The trend table's gross_margin for quarters-back-0 is 0.8224851660603623, highest of the 6 filled quarters. The release's non-GAAP gross margin is 84.2% against 83.1%.",
  "account": "GrossProfit",
  "expected_direction": "none",
  "horizon": "quarter to 2026-06-30 against quarter to 2025-06-30",
  "quote": "GAAP gross profit for the third quarter of fiscal year 2026 was $712 million, representing GAAP gross margin of 82.2%.",
  "paragraph_id": "0001048695-26-000063:8k_2_02:12" }
```

```json
{ "id": "across_documents_release_operating_margin",
  "what_changed": "The release states a GAAP operating margin of 24.7% against 25.2% a year earlier, while GAAP gross margin is 82.2% against 81.0%. The 8-K income statement shows R&D of 164,661 against 136,345 and G&A of 95,589 against 78,652 for the quarter (thousands). The trend table has no operating-margin ratio.",
  "account": "OperatingIncomeLoss",
  "expected_direction": "none",
  "horizon": "quarter to 2026-06-30 against quarter to 2025-06-30",
  "quote": "GAAP income from operations for the third quarter of fiscal year 2026 was $213 million, representing GAAP operating margin of 24.7%.",
  "paragraph_id": "0001048695-26-000063:8k_2_02:13" }
```

```json
{ "id": "across_documents_release_non_gaap_net_income",
  "what_changed": "The release states non-GAAP net income of $272 million ($4.73 per diluted share) against $243 million ($4.16). GAAP net income is $208 million ($3.62) against $190 million ($3.25). The trend table cannot fill non_gaap_gap, so no gap figure exists in my input and I compute none.",
  "account": "non-GAAP net income against NetIncomeLoss",
  "expected_direction": "none",
  "horizon": "quarter to 2026-06-30 against quarter to 2025-06-30",
  "quote": "Non-GAAP net income for the third quarter of fiscal year 2026 was $272 million, or $4.73 per diluted share, compared to $243 million, or $4.16 per diluted share, in the third quarter of fiscal year 2025.",
  "paragraph_id": "0001048695-26-000063:8k_2_02:16" }
```

## Seen in the notes

No items. No fact in `input_numbers.json` carries a marker of whether its element sat inside a note when it was extracted. The fields on every fact are:

- `id`, `paragraph_id`, `tag`, `prefix`, `namespace`
- `context`, `context_ref`, `unit`, `decimals`
- `value`, `number`, `nil`
- `form`, `source_accession`, `filing_date`
- `superseded_by` (on some facts)

None of these marks note membership. I do not judge it myself, so nothing is separated here. Some items above may have come from note tables, as listed in the notes at the top. A later split cannot take that from this input; the extraction has to supply the marker.
