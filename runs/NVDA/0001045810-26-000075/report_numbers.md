<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# NVDA — numbers reader — current 10-Q 0001045810-26-000075 (filed 2026-08-26)

## Before the items

**What I read.** I read all four input files in full: `input_trends.json`, `input_numbers.json`, `input_8k.md` and `input_prior_predictions.md`. None of them holds prices, abnormal returns, short interest, another company's files, a prior run's probability or the outcome window.

**Prior flags.** `input_prior_predictions.md` reads: "None on record." There is nothing to carry forward.

**Inputs this run does not contain.** My directory has:
- no articulation checks,
- no restatement traces,
- no fourth-quarter derivation.

So there is no articulation gap or restatement trace I can report.

`input_trends.json` names `src/fourth_quarter.py` as the place a fourth quarter would be derived. No output from it is in my directory.

**Periods the record does not reach.** Two quarters have no cells at all:
- **quarters-back-2** (target end 2026-01-25). The table gives this reason: "no quarter ending within 20 days of 2026-01-25 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration".
- **quarters-back-6** (target end 2025-01-26). The reason is the same, with the date 2025-01-26.

Every quarter-over-quarter comparison against those two quarters is therefore missing. One example: the quarters-back-1 accruals cell prints "accruals_over_total_assets is not filled in quarters-back-2".

**Restated prior values.** I found none. Many earlier facts carry a `superseded_by` field. In each case I read, the later filing prints the same value for the same period. For example, `ProductWarrantyAccrual` at 2026-04-26 is 2948000000 in both 10-Qs.

Where an element appears twice in one filing at different `decimals`, that is a precision duplicate, not a restatement. For example, the prior 10-Q prints both "2900000000" and "2948000000" for that date.

**Changes of tag.** The only change of concept the input states is in five trend cells for years-back-3:
- revenue is `us-gaap:Revenues` in years-back-3,
- revenue is `us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax` in years-back-4.

Those five are items below. The matching years-back-4 cells print the position "the only filled year on the same concepts; 4 other filled years rest on a different concept and are not compared".

**Formula baseline with no paragraph_id.** The research-and-development capitalization baseline for years-back-0 prints values but no `paragraph_id`, and it does not sit inside a ratio cell. So I cannot quote it, and I write no item for it. Its printed values are:
- `book_value_with_rnd_capitalized` 195315400000.0
- `earnings_with_rnd_capitalized` 130940000000.0
- `research_and_development_amortization` 7624000000.0
- `research_and_development_asset` 38022400000.0
- `capitalized_development_cost` is missing: the record tags none of `us-gaap:CapitalizedComputerSoftwareAdditions`.

**History too short for a trend claim.** Some ratios do not have enough filled periods:
- `accruals_over_total_assets` is filled in only 2 quarters ("highest of the 2 filled quarters" is printed for quarters-back-1). That supports no quarterly trend claim.
- `bad_debt_reserve_ratio`, `inventory_reserve_ratio` and `non_gaap_gap` are filled in 0 of the periods the table holds.

**Note marker.** No fact in `input_numbers.json` carries a field saying whether its element sat inside a note. The fields I saw on every fact are: `id`, `paragraph_id`, `tag`, `prefix`, `namespace`, `context`, `context_ref`, `unit`, `decimals`, `value`, `number`, `nil`, `form`, `source_accession`, `filing_date`, and sometimes `superseded_by`. See "Seen in the notes" below.

**Direction and horizon.** `expected_direction` is my reading of which way each item points for the company's later reported results. It is "none" wherever the input does not support a direction.

---

## Seen in the statements

### Trend table — quarters-back-0 (2026-04-27..2026-07-26)

```json
{ "id": "revenue_recognition_receivables_over_revenue_latest_quarter_trend_table",
  "what_changed": "receivables_over_revenue is 0.6553558994398312 for 2026-04-27..2026-07-26. Quarter-over-quarter change is 0.15655053277929087 (against quarters-back-1). Year-over-year change is 0.06044329220452327 (against quarters-back-4). Cell inputs: AccountsReceivableNetCurrent 63059000000.0 at 2026-07-26 and Revenues 96221000000.0 for the quarter. The table places it highest of the 6 filled quarters.",
  "account": "Accounts receivable, net (AccountsReceivableNetCurrent) / Revenues",
  "expected_direction": "down",
  "horizon": "next two quarters",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001045810-26-000075:trends:receivables_over_revenue:2026-04-27..2026-07-26" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_latest_quarter_trend_table",
  "what_changed": "days_sales_outstanding is 59.63738684902464 for 2026-04-27..2026-07-26 (a 91-day period). Quarter-over-quarter change is 14.246098482915471 (against quarters-back-1). Year-over-year change is 5.500339590611617 (against quarters-back-4). The table places it highest of the 6 filled quarters.",
  "account": "Accounts receivable, net (AccountsReceivableNetCurrent) / Revenues x days",
  "expected_direction": "down",
  "horizon": "next two quarters",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001045810-26-000075:trends:days_sales_outstanding:2026-04-27..2026-07-26" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_latest_quarter_trend_table",
  "what_changed": "days_sales_of_inventory is 119.32908343369742 for 2026-04-27..2026-07-26. Quarter-over-quarter change is 4.58047653175197 (against quarters-back-1). Year-over-year change is 13.701309965892918 (against quarters-back-4). Cell inputs: InventoryNet 31575000000.0 at 2026-07-26 and CostOfRevenue 24079000000.0 for the quarter. The table places it highest of the 6 filled quarters.",
  "account": "Inventories (InventoryNet) / Cost of revenue x days",
  "expected_direction": "down",
  "horizon": "next two quarters",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001045810-26-000075:trends:days_sales_of_inventory:2026-04-27..2026-07-26" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_latest_quarter_insufficient",
  "what_changed": "insufficient. accruals_over_total_assets is not filled for 2026-04-27..2026-07-26 because the record has no operating cash flow row for this three-month period. Both comparisons print 'accruals_over_total_assets is not filled in quarters-back-0'. Only 2 quarters of this ratio are filled anywhere in the table, which supports no quarterly trend claim.",
  "account": "Net income less operating cash flow / total assets",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-04-27..2026-07-26: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0001045810-26-000075:trends:accruals_over_total_assets:2026-04-27..2026-07-26" }
```

```json
{ "id": "earnings_quality_gross_margin_latest_quarter_trend_table",
  "what_changed": "gross_margin is 0.7497531723844068 for 2026-04-27..2026-07-26. Quarter-over-quarter change is 0.0004178786271317181 (against quarters-back-1). Year-over-year change is 0.025516388266998757 (against quarters-back-4). The table places it highest of the 6 filled quarters.",
  "account": "Revenues less cost of revenue / Revenues",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001045810-26-000075:trends:gross_margin:2026-04-27..2026-07-26" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_latest_quarter_insufficient",
  "what_changed": "insufficient. bad_debt_reserve_ratio is not filled for 2026-04-27..2026-07-26: no allowance row exists at 2026-07-26. The ratio is filled in 0 periods of the table.",
  "account": "Allowance for credit losses / Accounts receivable",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"missing\": \"no row for bad_debt_allowance in 2026-07-26: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"",
  "paragraph_id": "0001045810-26-000075:trends:bad_debt_reserve_ratio:2026-04-27..2026-07-26" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_latest_quarter_insufficient",
  "what_changed": "insufficient. inventory_reserve_ratio is not filled for 2026-04-27..2026-07-26: the record tags no InventoryValuationReserves in any period. The ratio is filled in 0 periods of the table.",
  "account": "Inventory valuation reserves / Inventories",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001045810-26-000075:trends:inventory_reserve_ratio:2026-04-27..2026-07-26" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_latest_quarter_trend_table",
  "what_changed": "warranty_reserve_ratio is 0.030533875141601104 for 2026-04-27..2026-07-26. Quarter-over-quarter change is -0.0055869359838047646 (against quarters-back-1). Year-over-year change is -0.015333955335689615 (against quarters-back-4). Cell inputs: ProductWarrantyAccrual 2938000000.0 at 2026-07-26 and Revenues 96221000000.0. The table places it second lowest of the 6 filled quarters.",
  "account": "Product warranty accrual / Revenues",
  "expected_direction": "down",
  "horizon": "next two quarters",
  "quote": "\"position_in_history\": \"second lowest of the 6 filled quarters\"",
  "paragraph_id": "0001045810-26-000075:trends:warranty_reserve_ratio:2026-04-27..2026-07-26" }
```

```json
{ "id": "earnings_quality_soft_asset_share_latest_quarter_trend_table",
  "what_changed": "soft_asset_share is 0.8853224758954888 at 2026-07-26. Quarter-over-quarter change is -0.015862228545033163 (against quarters-back-1). Year-over-year change is 0.03297062141204421 (against quarters-back-4). Cell inputs: Assets 320272000000.0, CashAndCashEquivalentsAtCarryingValue 22443000000.0 and PropertyPlantAndEquipmentNet 14285000000.0. The table places it second highest of the 6 filled quarters.",
  "account": "Total assets less PP&E and cash / Total assets",
  "expected_direction": "none",
  "horizon": "next two quarters",
  "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"",
  "paragraph_id": "0001045810-26-000075:trends:soft_asset_share:2026-04-27..2026-07-26" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_latest_quarter_trend_table",
  "what_changed": "contract_liabilities_over_revenue is 0.04797289572962243 for 2026-04-27..2026-07-26. Quarter-over-quarter change is 0.02697185425440342 (against quarters-back-1). Year-over-year change is 0.02700718963459216 (against quarters-back-4). Cell inputs: ContractWithCustomerLiabilityCurrent 4616000000.0 at 2026-07-26 and Revenues 96221000000.0. The table places it highest of the 6 filled quarters.",
  "account": "Contract liabilities, current / Revenues",
  "expected_direction": "up",
  "horizon": "next two quarters",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001045810-26-000075:trends:contract_liabilities_over_revenue:2026-04-27..2026-07-26" }
```

```json
{ "id": "results_against_expectations_non_gaap_gap_latest_quarter_insufficient",
  "what_changed": "insufficient. non_gaap_gap is not filled for 2026-04-27..2026-07-26 because the record holds no non-GAAP measure. The ratio is filled in 0 periods of the table. The release prints non-GAAP figures (see the release items below), but no gap is computed here.",
  "account": "GAAP net income against non-GAAP net income",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001045810-26-000075:trends:non_gaap_gap:2026-04-27..2026-07-26" }
```

### Trend table — years-back-0 (2025-01-27..2026-01-25)

For every cell in this period, the quarter-over-quarter comparison prints "an annual period has no preceding quarter".

```json
{ "id": "earnings_quality_accruals_over_total_assets_latest_year_trend_table",
  "what_changed": "accruals_over_total_assets is 0.08389143290958062 for 2025-01-27..2026-01-25. Year-over-year change is 0.0051197373154551196 (against years-back-1). Cell inputs: NetIncomeLoss 120067000000.0, NetCashProvidedByUsedInOperatingActivities 102718000000.0 and Assets 206803000000.0. The table places it highest of the 5 filled years.",
  "account": "Net income less operating cash flow / total assets",
  "expected_direction": "down",
  "horizon": "next four quarters",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001045810-26-000075:trends:accruals_over_total_assets:2025-01-27..2026-01-25" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_latest_year_insufficient",
  "what_changed": "insufficient. bad_debt_reserve_ratio is not filled for the year ended 2026-01-25: no allowance row exists at 2026-01-25. The ratio is filled in no year of the table.",
  "account": "Allowance for credit losses / Accounts receivable",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"missing\": \"no row for bad_debt_allowance in 2026-01-25: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"",
  "paragraph_id": "0001045810-26-000075:trends:bad_debt_reserve_ratio:2025-01-27..2026-01-25" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_latest_year_trend_table",
  "what_changed": "contract_liabilities_over_revenue is 0.0063860923042725224 for 2025-01-27..2026-01-25. Year-over-year change is -2.7848246084956688e-05 (against years-back-1). Cell inputs: ContractWithCustomerLiabilityCurrent 1379000000.0 at 2026-01-25 and Revenues 215938000000.0. The table places it lowest of the 4 filled years on the same concepts; 1 other filled year rests on a different concept.",
  "account": "Contract liabilities, current / Revenues",
  "expected_direction": "none",
  "horizon": "next four quarters",
  "quote": "\"position_in_history\": \"lowest of the 4 filled years on the same concepts; 1 other filled year rests on a different concept and is not compared\"",
  "paragraph_id": "0001045810-26-000075:trends:contract_liabilities_over_revenue:2025-01-27..2026-01-25" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_latest_year_trend_table",
  "what_changed": "days_sales_of_inventory is 124.70095238095239 for 2025-01-27..2026-01-25. Year-over-year change is 12.285743581663198 (against years-back-1). Cell inputs: InventoryNet 21403000000.0 at 2026-01-25 and CostOfRevenue 62475000000.0. The table places it second highest of the 5 filled years.",
  "account": "Inventories (InventoryNet) / Cost of revenue x days",
  "expected_direction": "down",
  "horizon": "next four quarters",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001045810-26-000075:trends:days_sales_of_inventory:2025-01-27..2026-01-25" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_latest_year_trend_table",
  "what_changed": "days_sales_outstanding is 64.84094508608953 for 2025-01-27..2026-01-25. Year-over-year change is 0.5049067097283881 (against years-back-1). Cell inputs: AccountsReceivableNetCurrent 38466000000.0 at 2026-01-25 and Revenues 215938000000.0. The table places it highest of the 4 filled years on the same concepts; 1 other filled year rests on a different concept.",
  "account": "Accounts receivable, net / Revenues x days",
  "expected_direction": "none",
  "horizon": "next four quarters",
  "quote": "\"position_in_history\": \"highest of the 4 filled years on the same concepts; 1 other filled year rests on a different concept and is not compared\"",
  "paragraph_id": "0001045810-26-000075:trends:days_sales_outstanding:2025-01-27..2026-01-25" }
```

```json
{ "id": "earnings_quality_gross_margin_latest_year_trend_table",
  "what_changed": "gross_margin is 0.7106808435754708 for 2025-01-27..2026-01-25. Year-over-year change is -0.039206127006228386 (against years-back-1). Cell inputs: Revenues 215938000000.0 and CostOfRevenue 62475000000.0. The table places it second lowest of the 4 filled years on the same concepts; 1 other filled year rests on a different concept.",
  "account": "Revenues less cost of revenue / Revenues",
  "expected_direction": "none",
  "horizon": "next four quarters",
  "quote": "\"position_in_history\": \"second lowest of the 4 filled years on the same concepts; 1 other filled year rests on a different concept and is not compared\"",
  "paragraph_id": "0001045810-26-000075:trends:gross_margin:2025-01-27..2026-01-25" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_latest_year_insufficient",
  "what_changed": "insufficient. inventory_reserve_ratio is not filled for the year ended 2026-01-25: the record tags no InventoryValuationReserves in any period. The ratio is filled in no year of the table.",
  "account": "Inventory valuation reserves / Inventories",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001045810-26-000075:trends:inventory_reserve_ratio:2025-01-27..2026-01-25" }
```

```json
{ "id": "results_against_expectations_non_gaap_gap_latest_year_insufficient",
  "what_changed": "insufficient. non_gaap_gap is not filled for the year ended 2026-01-25 because the record holds no non-GAAP measure. The ratio is filled in no year of the table.",
  "account": "GAAP net income against non-GAAP net income",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001045810-26-000075:trends:non_gaap_gap:2025-01-27..2026-01-25" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_latest_year_trend_table",
  "what_changed": "receivables_over_revenue is 0.17813446452222398 for 2025-01-27..2026-01-25. Year-over-year change is 0.001387106345407646 (against years-back-1). Cell inputs: AccountsReceivableNetCurrent 38466000000.0 and Revenues 215938000000.0. The table places it highest of the 4 filled years on the same concepts; 1 other filled year rests on a different concept.",
  "account": "Accounts receivable, net / Revenues",
  "expected_direction": "none",
  "horizon": "next four quarters",
  "quote": "\"position_in_history\": \"highest of the 4 filled years on the same concepts; 1 other filled year rests on a different concept and is not compared\"",
  "paragraph_id": "0001045810-26-000075:trends:receivables_over_revenue:2025-01-27..2026-01-25" }
```

```json
{ "id": "earnings_quality_soft_asset_share_latest_year_trend_table",
  "what_changed": "soft_asset_share is 0.8985121105593246 at 2026-01-25. Year-over-year change is 0.031772565214748805 (against years-back-1). Cell inputs: Assets 206803000000.0, CashAndCashEquivalentsAtCarryingValue 10605000000.0 and PropertyPlantAndEquipmentNet 10383000000.0. The table places it highest of the 5 filled years.",
  "account": "Total assets less PP&E and cash / Total assets",
  "expected_direction": "none",
  "horizon": "next four quarters",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001045810-26-000075:trends:soft_asset_share:2025-01-27..2026-01-25" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_latest_year_trend_table",
  "what_changed": "warranty_reserve_ratio is 0.012999101593976048 for 2025-01-27..2026-01-25. Year-over-year change is 0.0031138168747871005 (against years-back-1). Cell inputs: ProductWarrantyAccrual 2807000000.0 at 2026-01-25 and Revenues 215938000000.0. The table places it highest of the 4 filled years on the same concepts; 1 other filled year rests on a different concept.",
  "account": "Product warranty accrual / Revenues",
  "expected_direction": "none",
  "horizon": "next four quarters",
  "quote": "\"position_in_history\": \"highest of the 4 filled years on the same concepts; 1 other filled year rests on a different concept and is not compared\"",
  "paragraph_id": "0001045810-26-000075:trends:warranty_reserve_ratio:2025-01-27..2026-01-25" }
```

### Changes of tag stated by the trend table (years-back-3 against years-back-4)

```json
{ "id": "articulation_and_the_filed_history_revenue_tag_change_contract_liabilities_over_revenue",
  "what_changed": "Change of tag. In the cell for 2022-01-31..2023-01-29, the year-over-year comparison is withheld. The cell states that revenue is us-gaap:Revenues in years-back-3 and us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax in years-back-4, so the year-over-year difference is not treated as a change.",
  "account": "Revenue concept (Revenues / RevenueFromContractWithCustomerExcludingAssessedTax)",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"reason\": \"contract_liabilities_over_revenue rests on a different concept in each period, so the difference would not be a change",
  "paragraph_id": "0001045810-26-000075:trends:contract_liabilities_over_revenue:2022-01-31..2023-01-29" }
```

```json
{ "id": "articulation_and_the_filed_history_revenue_tag_change_days_sales_outstanding",
  "what_changed": "Change of tag. In the cell for 2022-01-31..2023-01-29, the year-over-year comparison is withheld. Revenue is us-gaap:Revenues in years-back-3 and us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax in years-back-4.",
  "account": "Revenue concept (Revenues / RevenueFromContractWithCustomerExcludingAssessedTax)",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"reason\": \"days_sales_outstanding rests on a different concept in each period, so the difference would not be a change",
  "paragraph_id": "0001045810-26-000075:trends:days_sales_outstanding:2022-01-31..2023-01-29" }
```

```json
{ "id": "articulation_and_the_filed_history_revenue_tag_change_gross_margin",
  "what_changed": "Change of tag. In the cell for 2022-01-31..2023-01-29, the year-over-year comparison is withheld. Revenue is us-gaap:Revenues in years-back-3 and us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax in years-back-4.",
  "account": "Revenue concept (Revenues / RevenueFromContractWithCustomerExcludingAssessedTax)",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"reason\": \"gross_margin rests on a different concept in each period, so the difference would not be a change",
  "paragraph_id": "0001045810-26-000075:trends:gross_margin:2022-01-31..2023-01-29" }
```

```json
{ "id": "articulation_and_the_filed_history_revenue_tag_change_receivables_over_revenue",
  "what_changed": "Change of tag. In the cell for 2022-01-31..2023-01-29, the year-over-year comparison is withheld. Revenue is us-gaap:Revenues in years-back-3 and us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax in years-back-4.",
  "account": "Revenue concept (Revenues / RevenueFromContractWithCustomerExcludingAssessedTax)",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"reason\": \"receivables_over_revenue rests on a different concept in each period, so the difference would not be a change",
  "paragraph_id": "0001045810-26-000075:trends:receivables_over_revenue:2022-01-31..2023-01-29" }
```

```json
{ "id": "articulation_and_the_filed_history_revenue_tag_change_warranty_reserve_ratio",
  "what_changed": "Change of tag. In the cell for 2022-01-31..2023-01-29, the year-over-year comparison is withheld. Revenue is us-gaap:Revenues in years-back-3 and us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax in years-back-4.",
  "account": "Revenue concept (Revenues / RevenueFromContractWithCustomerExcludingAssessedTax)",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"reason\": \"warranty_reserve_ratio rests on a different concept in each period, so the difference would not be a change",
  "paragraph_id": "0001045810-26-000075:trends:warranty_reserve_ratio:2022-01-31..2023-01-29" }
```

### Numeric facts

No fact carries an in-note marker, so every numeric-fact item sits under this heading.

```json
{ "id": "estimates_and_discretion_inventory_write_down_latest_quarter_filed_fact",
  "what_changed": "InventoryWriteDown is 784000000 for 2026-04-27..2026-07-26. The same filing prints 886000000 for 2025-04-28..2025-07-27, 1600000000 for 2026-01-26..2026-07-26 and 3200000000 for 2025-01-27..2025-07-27.",
  "account": "Inventory write-down (cost of revenue)",
  "expected_direction": "none",
  "horizon": "next two quarters",
  "quote": "\"value\": \"784000000\"",
  "paragraph_id": "0001045810-26-000075:facts:InventoryWriteDown:2026-04-27..2026-07-26" }
```

```json
{ "id": "estimates_and_discretion_inventory_write_down_latest_year_filed_fact",
  "what_changed": "The 10-K prints InventoryWriteDown of 4000000000.0 for fiscal year 2025-01-27..2026-01-25.",
  "account": "Inventory write-down (cost of revenue)",
  "expected_direction": "none",
  "horizon": "next four quarters",
  "quote": "\"value\": \"4000000000.0\"",
  "paragraph_id": "0001045810-26-000021:facts:InventoryWriteDown:2025-01-27..2026-01-25" }
```

```json
{ "id": "estimates_and_discretion_excess_purchase_obligation_charge_filed_fact",
  "what_changed": "CostOfRevenue tagged with the inventory-purchase-obligations-in-excess-of-projections member is 201000000 for 2026-04-27..2026-07-26. The same filing prints 137000000 for 2025-04-28..2025-07-27, 501000000 for 2026-01-26..2026-07-26 and 3100000000 for 2025-01-27..2025-07-27.",
  "account": "Cost of revenue: purchase obligations in excess of projections",
  "expected_direction": "none",
  "horizon": "next two quarters",
  "quote": "\"value\": \"201000000\"",
  "paragraph_id": "0001045810-26-000075:facts:CostOfRevenue:2026-04-27..2026-07-26:us-gaap:NatureOfExpenseAxis=nvda:InventoryPurchaseObligationsInExcessOfProjectionsMember" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_raw_materials_inventory_filed_fact",
  "what_changed": "InventoryRawMaterialsNetOfReserves is 11341000000 at 2026-07-26. The same filing prints 3807000000 at 2026-01-25.",
  "account": "Inventories: raw materials",
  "expected_direction": "none",
  "horizon": "next two quarters",
  "quote": "\"value\": \"11341000000\"",
  "paragraph_id": "0001045810-26-000075:facts:InventoryRawMaterialsNetOfReserves:2026-07-26" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_work_in_process_inventory_filed_fact",
  "what_changed": "InventoryWorkInProcessNetOfReserves is 13377000000 at 2026-07-26. The same filing prints 8822000000 at 2026-01-25.",
  "account": "Inventories: work in process",
  "expected_direction": "none",
  "horizon": "next two quarters",
  "quote": "\"value\": \"13377000000\"",
  "paragraph_id": "0001045810-26-000075:facts:InventoryWorkInProcessNetOfReserves:2026-07-26" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_finished_goods_inventory_filed_fact",
  "what_changed": "InventoryFinishedGoodsNetOfReserves is 6857000000 at 2026-07-26. The same filing prints 8774000000 at 2026-01-25.",
  "account": "Inventories: finished goods",
  "expected_direction": "none",
  "horizon": "next two quarters",
  "quote": "\"value\": \"6857000000\"",
  "paragraph_id": "0001045810-26-000075:facts:InventoryFinishedGoodsNetOfReserves:2026-07-26" }
```

```json
{ "id": "estimates_and_discretion_warranties_issued_latest_quarter_filed_fact",
  "what_changed": "ProductWarrantyAccrualWarrantiesIssued is 391000000 for 2026-04-27..2026-07-26. The same filing prints 220000000 for 2025-04-28..2025-07-27, 720000000 for 2026-01-26..2026-07-26 and 1090000000 for 2025-01-27..2025-07-27. The prior 10-Q printed 330000000 for 2026-01-26..2026-04-26 and 870000000 for 2025-01-27..2025-04-27.",
  "account": "Product warranty accrual: warranties issued",
  "expected_direction": "down",
  "horizon": "next two quarters",
  "quote": "\"value\": \"391000000\"",
  "paragraph_id": "0001045810-26-000075:facts:ProductWarrantyAccrualWarrantiesIssued:2026-04-27..2026-07-26" }
```

```json
{ "id": "estimates_and_discretion_warranty_payments_latest_quarter_filed_fact",
  "what_changed": "ProductWarrantyAccrualPayments is 401000000 for 2026-04-27..2026-07-26. The same filing prints 156000000 for 2025-04-28..2025-07-27, 589000000 for 2026-01-26..2026-07-26 and 236000000 for 2025-01-27..2025-07-27. The warranty accrual is 2938000000 at 2026-07-26, 2948000000 at 2026-04-26 and 2144000000 at 2025-07-27.",
  "account": "Product warranty accrual: payments",
  "expected_direction": "down",
  "horizon": "next two quarters",
  "quote": "\"value\": \"401000000\"",
  "paragraph_id": "0001045810-26-000075:facts:ProductWarrantyAccrualPayments:2026-04-27..2026-07-26" }
```

```json
{ "id": "revenue_recognition_total_contract_liabilities_filed_fact",
  "what_changed": "ContractWithCustomerLiability is 6412000000 at 2026-07-26. The same filing prints 2572000000 at 2026-01-25, 2035000000 at 2025-07-27 and 1813000000 at 2025-01-26. Revenue recognized from opening contract liabilities is 758000000 for 2026-01-26..2026-07-26 and 479000000 for 2025-01-27..2025-07-27.",
  "account": "Contract liabilities (total)",
  "expected_direction": "up",
  "horizon": "next two quarters",
  "quote": "\"value\": \"6412000000\"",
  "paragraph_id": "0001045810-26-000075:facts:ContractWithCustomerLiability:2026-07-26" }
```

```json
{ "id": "revenue_recognition_customer_advances_and_deferrals_filed_fact",
  "what_changed": "ContractWithCustomerLiabilityCurrent tagged with the customer-advances-and-deferrals member is 2800000000 at 2026-07-26. The same filing prints 160000000 at 2026-01-25.",
  "account": "Contract liabilities, current: customer advances and deferrals",
  "expected_direction": "up",
  "horizon": "next two quarters",
  "quote": "\"value\": \"2800000000\"",
  "paragraph_id": "0001045810-26-000075:facts:ContractWithCustomerLiabilityCurrent:2026-07-26:us-gaap:NatureOfExpenseAxis=nvda:NatureOfExpenseCustomerAdvancesAndDeferralsMember" }
```

```json
{ "id": "revenue_recognition_noncurrent_contract_liabilities_filed_fact",
  "what_changed": "ContractWithCustomerLiabilityNoncurrent is 1796000000 at 2026-07-26. The same filing prints 1193000000 at 2026-01-25.",
  "account": "Contract liabilities, noncurrent",
  "expected_direction": "none",
  "horizon": "next four quarters",
  "quote": "\"value\": \"1796000000\"",
  "paragraph_id": "0001045810-26-000075:facts:ContractWithCustomerLiabilityNoncurrent:2026-07-26" }
```

```json
{ "id": "revenue_recognition_remaining_performance_obligation_filed_fact",
  "what_changed": "RevenueRemainingPerformanceObligation is 3200000000 at 2026-07-26. The filing tags a percentage of 0.39 against an expected-satisfaction start date of 2026-07-27.",
  "account": "Remaining performance obligations",
  "expected_direction": "none",
  "horizon": "next four quarters",
  "quote": "\"value\": \"3200000000\"",
  "paragraph_id": "0001045810-26-000075:facts:RevenueRemainingPerformanceObligation:2026-07-26" }
```

```json
{ "id": "revenue_recognition_unbilled_receivables_filed_fact",
  "what_changed": "UnbilledContractsReceivable is 244000000 at 2026-07-26. No earlier value for this tag appeared in the facts I read.",
  "account": "Unbilled contracts receivable",
  "expected_direction": "none",
  "horizon": "next two quarters",
  "quote": "\"value\": \"244000000\"",
  "paragraph_id": "0001045810-26-000075:facts:UnbilledContractsReceivable:2026-07-26" }
```

```json
{ "id": "revenue_recognition_receivables_customer_concentration_filed_fact",
  "what_changed": "Accounts-receivable concentration in the current 10-Q, context 2026-01-26..2026-07-26: customer A 0.22, B 0.14, C 0.13, D 0.11, E 0.10. The same filing prints, for 2025-01-27..2026-01-25: customer F 0.25, G 0.18, H 0.13. The prior 10-Q printed receivables concentrations of 0.30, 0.18 and 0.16.",
  "account": "Accounts receivable: customer concentration",
  "expected_direction": "down",
  "horizon": "next two quarters",
  "quote": "\"value\": \"0.22\"",
  "paragraph_id": "0001045810-26-000075:facts:ConcentrationRiskPercentage1:2026-01-26..2026-07-26:srt:MajorCustomersAxis=nvda:AccountsReceivableCustomerAMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:AccountsReceivableMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember" }
```

```json
{ "id": "revenue_recognition_revenue_customer_concentration_filed_fact",
  "what_changed": "Revenue concentration (Compute & Networking) is 0.16 for customer 1 for 2026-04-27..2026-07-26. For 2026-01-26..2026-07-26: customers 2, 3 and 4 are 0.16, 0.15 and 0.13. For 2025-04-28..2025-07-27: customers 5 and 6 are 0.23 and 0.16. For 2025-01-27..2025-07-27: customers 7 and 8 are 0.20 and 0.15.",
  "account": "Revenues: direct-customer concentration",
  "expected_direction": "none",
  "horizon": "next two quarters",
  "quote": "\"value\": \"0.16\"",
  "paragraph_id": "0001045810-26-000075:facts:ConcentrationRiskPercentage1:2026-04-27..2026-07-26:srt:MajorCustomersAxis=nvda:RevenueCustomer1Member,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:SalesRevenueNetMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember,us-gaap:StatementBusinessSegmentsAxis=nvda:ComputeAndNetworkingMember" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_non_us_revenue_share_filed_fact",
  "what_changed": "The non-US share of revenue is 0.38 for 2026-04-27..2026-07-26. The same filing prints 0.30 for 2025-04-28..2025-07-27, 0.30 for 2026-01-26..2026-07-26 and 0.35 for 2025-01-27..2025-07-27.",
  "account": "Revenues: non-US share",
  "expected_direction": "none",
  "horizon": "next two quarters",
  "quote": "\"value\": \"0.38\"",
  "paragraph_id": "0001045810-26-000075:facts:ConcentrationRiskPercentage1:2026-04-27..2026-07-26:srt:StatementGeographicalAxis=us-gaap:NonUsMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:SalesRevenueNetMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_taiwan_billed_revenue_filed_fact",
  "what_changed": "Revenues on the Taiwan geographic member are 26985000000 for 2026-04-27..2026-07-26. The same filing prints 8902000000 for 2025-04-28..2025-07-27. The United States member is 60074000000 against 32897000000 for the same two quarters.",
  "account": "Revenues by geography: Taiwan",
  "expected_direction": "none",
  "horizon": "next two quarters",
  "quote": "\"value\": \"26985000000\"",
  "paragraph_id": "0001045810-26-000075:facts:Revenues:2026-04-27..2026-07-26:srt:StatementGeographicalAxis=country:TW" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_china_revenue_filed_fact",
  "what_changed": "Revenues on the China-including-Hong-Kong member are 7880000000 for 2026-04-27..2026-07-26. The same filing prints 3985000000 for 2025-04-28..2025-07-27, 12430000000 for 2026-01-26..2026-07-26 and 13644000000 for 2025-01-27..2025-07-27. The release outlook (paragraph 15) assumes no Data Center compute revenue from China.",
  "account": "Revenues by geography: China including Hong Kong",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "\"value\": \"7880000000\"",
  "paragraph_id": "0001045810-26-000075:facts:Revenues:2026-04-27..2026-07-26:srt:StatementGeographicalAxis=nvda:ChinaIncludingHongKongMember" }
```

```json
{ "id": "revenue_recognition_data_center_platform_revenue_filed_fact",
  "what_changed": "Revenues on the Data Center product member are 89023000000 for 2026-04-27..2026-07-26. The same filing prints 41096000000 for 2025-04-28..2025-07-27. The release states 'Data Center revenue of $89.0 billion'.",
  "account": "Revenues: Data Center",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"89023000000\"",
  "paragraph_id": "0001045810-26-000075:facts:Revenues:2026-04-27..2026-07-26:srt:ProductOrServiceAxis=nvda:DataCenterMember" }
```

```json
{ "id": "revenue_recognition_hyperscale_platform_revenue_filed_fact",
  "what_changed": "Revenues on the Hyperscale member are 48710000000 for 2026-04-27..2026-07-26. The same filing prints 24168000000 for 2025-04-28..2025-07-27. The prior 10-Q printed 37869000000 for 2026-01-26..2026-04-26.",
  "account": "Revenues: Hyperscale",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"48710000000\"",
  "paragraph_id": "0001045810-26-000075:facts:Revenues:2026-04-27..2026-07-26:srt:ProductOrServiceAxis=nvda:HyperscaleMember" }
```

```json
{ "id": "revenue_recognition_ai_clouds_industrial_enterprise_revenue_filed_fact",
  "what_changed": "Revenues on the AI Clouds, Industrial and Enterprise member are 40313000000 for 2026-04-27..2026-07-26. The same filing prints 16928000000 for 2025-04-28..2025-07-27. The prior 10-Q printed 37377000000 for 2026-01-26..2026-04-26.",
  "account": "Revenues: AI Clouds, Industrial and Enterprise",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"40313000000\"",
  "paragraph_id": "0001045810-26-000075:facts:Revenues:2026-04-27..2026-07-26:srt:ProductOrServiceAxis=nvda:AICloudsIndustrialEnterpriseMember" }
```

```json
{ "id": "revenue_recognition_edge_computing_revenue_filed_fact",
  "what_changed": "Revenues on the Edge Computing member are 7198000000 for 2026-04-27..2026-07-26. The same filing prints 5647000000 for 2025-04-28..2025-07-27. The prior 10-Q printed 6369000000 for 2026-01-26..2026-04-26.",
  "account": "Revenues: Edge Computing",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"7198000000\"",
  "paragraph_id": "0001045810-26-000075:facts:Revenues:2026-04-27..2026-07-26:srt:ProductOrServiceAxis=nvda:EdgeComputingMember" }
```

```json
{ "id": "earnings_quality_non_marketable_equity_securities_filed_fact",
  "what_changed": "EquitySecuritiesWithoutReadilyDeterminableFairValueAmount is 47898000000 at 2026-07-26. The same filing prints 42336000000 at 2026-04-26, 22251000000 at 2026-01-25 and 3799000000 at 2025-07-27. EquityMethodInvestments is 3300000000 at 2026-07-26. The release balance sheet line 'Non-marketable securities' is 51,157 at July 26, 2026.",
  "account": "Non-marketable equity securities (measurement alternative)",
  "expected_direction": "none",
  "horizon": "next two quarters",
  "quote": "\"value\": \"47898000000\"",
  "paragraph_id": "0001045810-26-000075:facts:EquitySecuritiesWithoutReadilyDeterminableFairValueAmount:2026-07-26" }
```

```json
{ "id": "earnings_quality_upward_price_adjustments_non_marketable_filed_fact",
  "what_changed": "Upward price adjustments on non-marketable equity securities are 4900000000 for 2026-04-27..2026-07-26. The same filing prints 267000000 for 2025-04-28..2025-07-27, 7504000000 for 2026-01-26..2026-07-26 and 330000000 for 2025-01-27..2025-07-27. The cumulative upward adjustment is 9100000000 at 2026-07-26 and 661000000 at 2025-07-27.",
  "account": "Non-marketable equity securities: upward price adjustments (other income)",
  "expected_direction": "down",
  "horizon": "next two quarters",
  "quote": "\"value\": \"4900000000\"",
  "paragraph_id": "0001045810-26-000075:facts:EquitySecuritiesWithoutReadilyDeterminableFairValueUpwardPriceAdjustmentAnnualAmount:2026-04-27..2026-07-26" }
```

```json
{ "id": "earnings_quality_gains_on_investments_latest_quarter_filed_fact",
  "what_changed": "GainLossOnInvestments is 7771000000 for 2026-04-27..2026-07-26. The same filing prints 2247000000 for 2025-04-28..2025-07-27, 23707000000 for 2026-01-26..2026-07-26 and 2073000000 for 2025-01-27..2025-07-27. Unrealized gains on publicly held equity securities are 1500000000 for the quarter and 12500000000 for the six months. Income before tax is 71507000000 for the quarter.",
  "account": "Other income: gains on investments",
  "expected_direction": "down",
  "horizon": "next two quarters",
  "quote": "\"value\": \"7771000000\"",
  "paragraph_id": "0001045810-26-000075:facts:GainLossOnInvestments:2026-04-27..2026-07-26" }
```

```json
{ "id": "liquidity_and_capital_restricted_public_equity_investments_filed_fact",
  "what_changed": "RestrictedInvestmentsCurrent on the publicly-held-equity member is 36900000000 at 2026-07-26. The same filing prints 10500000000 at 2026-01-25. RestrictedInvestmentsNoncurrent is 5000000000.0 at 2026-07-26 and 4800000000 at 2026-01-25. The release shows marketable equity securities of 42,783 at July 26, 2026.",
  "account": "Restricted investments (publicly held equity securities)",
  "expected_direction": "none",
  "horizon": "next two quarters",
  "quote": "\"value\": \"36900000000\"",
  "paragraph_id": "0001045810-26-000075:facts:RestrictedInvestmentsCurrent:2026-07-26:us-gaap:FinancialInstrumentAxis=nvda:PubliclyHeldEquitySecuritiesMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_public_company_warrants_filed_fact",
  "what_changed": "DerivativeNotionalAmount on the public-company-warrants member is 4800000000 at 2026-07-26. The same filing prints 0 at 2026-01-25. Their net fair value is 824000000 at 2026-07-26.",
  "account": "Derivatives: public company warrants (non-designated)",
  "expected_direction": "none",
  "horizon": "next two quarters",
  "quote": "\"value\": \"4800000000\"",
  "paragraph_id": "0001045810-26-000075:facts:DerivativeNotionalAmount:2026-07-26:us-gaap:DerivativeInstrumentRiskAxis=nvda:PublicCompanyWarrantsMember,us-gaap:HedgingDesignationAxis=us-gaap:NondesignatedMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_equity_forward_contract_filed_fact",
  "what_changed": "DerivativeNotionalAmount on the equity-forward-contract member is 1000000000 at 2026-07-26. The same filing prints 0 at 2026-01-25.",
  "account": "Derivatives: equity forward contract (non-designated)",
  "expected_direction": "none",
  "horizon": "next two quarters",
  "quote": "\"value\": \"1000000000\"",
  "paragraph_id": "0001045810-26-000075:facts:DerivativeNotionalAmount:2026-07-26:us-gaap:DerivativeInstrumentRiskAxis=nvda:EquityForwardContractMember,us-gaap:HedgingDesignationAxis=us-gaap:NondesignatedMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_variable_interest_exposure_filed_fact",
  "what_changed": "VariableInterestEntityEntityMaximumLossExposureAmount (carrying values and future committed amounts) is 4700000000 at 2026-07-26.",
  "account": "Variable interest entities: maximum loss exposure",
  "expected_direction": "none",
  "horizon": "next four quarters",
  "quote": "\"value\": \"4700000000\"",
  "paragraph_id": "0001045810-26-000075:facts:VariableInterestEntityEntityMaximumLossExposureAmount:2026-07-26:us-gaap:InvestmentTypeAxis=nvda:CarryingValuesAndFutureCommittedAmountsMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_guarantee_maximum_exposure_filed_fact",
  "what_changed": "GuaranteeObligationsMaximumExposure is 108500000000 at 2026-07-26. Of the tagged parts, the financial-guarantee member is 105000000000.0 and the land, power and shell guarantees for AI clouds member is 3500000000. The latter's notional is 3529000000 at 2026-07-26 and 3530000000 at 2026-01-25. The 10-K printed a guarantee maximum exposure of 3500000000.",
  "account": "Guarantees: maximum exposure",
  "expected_direction": "down",
  "horizon": "next four quarters",
  "quote": "\"value\": \"108500000000\"",
  "paragraph_id": "0001045810-26-000075:facts:GuaranteeObligationsMaximumExposure:2026-07-26" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_sb_energy_guarantee_subsequent_event_filed_fact",
  "what_changed": "A financial guarantee with SB Energy Corp. is tagged as a subsequent event at 2026-08-31, with maximum exposure 105000000000. The release (paragraph 30) describes a partnership with SB Energy for land, power and shell capacity in Ohio.",
  "account": "Guarantees: SB Energy (subsequent event)",
  "expected_direction": "down",
  "horizon": "next four quarters",
  "quote": "\"value\": \"105000000000\"",
  "paragraph_id": "0001045810-26-000075:facts:GuaranteeObligationsMaximumExposure:2026-08-31:srt:CounterpartyNameAxis=nvda:SBEnergyCorp.Member,us-gaap:GuaranteeObligationsByNatureAxis=us-gaap:FinancialGuaranteeMember,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

```json
{ "id": "liquidity_and_capital_supply_and_capacity_commitments_filed_fact",
  "what_changed": "OtherCommitment on the supply-and-capacity member is 279000000000 at 2026-07-26. The same filing prints 119000000000 at 2026-04-26. Timing at 2026-07-26: remainder of fiscal year 92000000000, next twelve months 87000000000, second year 88000000000, third year 6000000000, fourth year 5000000000. The 10-K printed 95200000000 on its manufacturing and supply commitment member.",
  "account": "Commitments: supply and capacity",
  "expected_direction": "down",
  "horizon": "next four quarters",
  "quote": "\"value\": \"279000000000\"",
  "paragraph_id": "0001045810-26-000075:facts:OtherCommitment:2026-07-26:us-gaap:OtherCommitmentsAxis=nvda:SupplyAndCapacityCommitmentsMember" }
```

```json
{ "id": "liquidity_and_capital_future_purchase_and_other_commitments_filed_fact",
  "what_changed": "OtherCommitment on the future-purchase-and-other-commitments member is 366000000000 at 2026-07-26. Timing: remainder of fiscal year 120000000000, next twelve months 100000000000, second year 98000000000, third year 16000000000, fourth year 10000000000.",
  "account": "Commitments: future purchase and other commitments (total)",
  "expected_direction": "down",
  "horizon": "next four quarters",
  "quote": "\"value\": \"366000000000\"",
  "paragraph_id": "0001045810-26-000075:facts:OtherCommitment:2026-07-26:us-gaap:OtherCommitmentsAxis=nvda:FuturePurchaseAndOtherCommitmentsMember" }
```

```json
{ "id": "liquidity_and_capital_ai_cloud_partnership_commitments_filed_fact",
  "what_changed": "OtherCommitment on the AI-cloud-partnership member is 36000000000 at 2026-07-26. Timing: remainder of fiscal year 0, next twelve months 6000000000, second year 8000000000, third year 7000000000, fourth year 6000000000. No earlier value for this member appeared in the facts I read.",
  "account": "Commitments: AI cloud partnerships",
  "expected_direction": "down",
  "horizon": "next four quarters",
  "quote": "\"value\": \"36000000000\"",
  "paragraph_id": "0001045810-26-000075:facts:OtherCommitment:2026-07-26:us-gaap:OtherCommitmentsAxis=nvda:AICloudPartnershipCommitmentsMember" }
```

```json
{ "id": "liquidity_and_capital_future_additional_commitments_filed_fact",
  "what_changed": "OtherCommitment on the future-additional-commitments member is 56000000000 at 2026-07-26. Timing: next twelve months 6000000000, second year 9000000000, third year 8000000000, fourth year 7000000000.",
  "account": "Commitments: future additional commitments",
  "expected_direction": "down",
  "horizon": "next four quarters",
  "quote": "\"value\": \"56000000000\"",
  "paragraph_id": "0001045810-26-000075:facts:OtherCommitment:2026-07-26:us-gaap:OtherCommitmentsAxis=nvda:FutureAdditionalCommitmentsMember" }
```

```json
{ "id": "liquidity_and_capital_data_center_lease_not_yet_commenced_filed_fact",
  "what_changed": "OtherCommitment on the data-center-lease-not-yet-commenced member is 25000000000 at 2026-07-26.",
  "account": "Commitments: data center leases not yet commenced",
  "expected_direction": "none",
  "horizon": "next four quarters",
  "quote": "\"value\": \"25000000000\"",
  "paragraph_id": "0001045810-26-000075:facts:OtherCommitment:2026-07-26:us-gaap:OtherCommitmentsAxis=nvda:DataCenterLeaseNotYetCommencedMember" }
```

```json
{ "id": "liquidity_and_capital_third_party_data_center_lease_not_yet_commenced_filed_fact",
  "what_changed": "OtherCommitment on the data-center-for-third-party-lease-not-yet-commenced member is 20000000000 at 2026-07-26.",
  "account": "Commitments: data center leases for third parties not yet commenced",
  "expected_direction": "none",
  "horizon": "next four quarters",
  "quote": "\"value\": \"20000000000\"",
  "paragraph_id": "0001045810-26-000075:facts:OtherCommitment:2026-07-26:us-gaap:OtherCommitmentsAxis=nvda:DataCenterForThirdPartyLeaseNotYetCommencedMember" }
```

```json
{ "id": "liquidity_and_capital_equity_investment_commitments_filed_fact",
  "what_changed": "OtherCommitment on the equity-investment-commitments member is 25000000000 at 2026-07-26. Timing: remainder of fiscal year 18000000000, next twelve months 3000000000, second year 2000000000, third year 2000000000. The prior 10-Q printed an investment commitment of 27000000000; the 10-K printed 11400000000.",
  "account": "Commitments: equity investments",
  "expected_direction": "none",
  "horizon": "next two quarters",
  "quote": "\"value\": \"25000000000\"",
  "paragraph_id": "0001045810-26-000075:facts:OtherCommitment:2026-07-26:us-gaap:OtherCommitmentsAxis=nvda:EquityInvestmentCommitmentsMember" }
```

```json
{ "id": "liquidity_and_capital_cloud_service_agreement_commitments_filed_fact",
  "what_changed": "OtherCommitment on the cloud-service-agreement member is 29000000000 at 2026-07-26. The prior 10-Q tagged 30000000000 at 2026-04-26 on a differently named member (MultiYearCloudServiceAgreementCommitmentsMember).",
  "account": "Commitments: cloud service agreements",
  "expected_direction": "none",
  "horizon": "next four quarters",
  "quote": "\"value\": \"29000000000\"",
  "paragraph_id": "0001045810-26-000075:facts:OtherCommitment:2026-07-26:us-gaap:OtherCommitmentsAxis=nvda:CloudServiceAgreementCommitmentsMember" }
```

```json
{ "id": "liquidity_and_capital_capital_expenditure_obligations_filed_fact",
  "what_changed": "OtherCommitment on the capital-expenditure-obligations member is 8000000000 at 2026-07-26 (remainder of fiscal year 7000000000, next twelve months 1000000000).",
  "account": "Commitments: capital expenditure obligations",
  "expected_direction": "none",
  "horizon": "next two quarters",
  "quote": "\"value\": \"8000000000\"",
  "paragraph_id": "0001045810-26-000075:facts:OtherCommitment:2026-07-26:us-gaap:OtherCommitmentsAxis=nvda:CapitalExpenditureObligationsMember" }
```

```json
{ "id": "structure_and_disclosure_changes_commitment_member_relabel_filed_fact",
  "what_changed": "The 2026-04-26 commitment is tagged on different members in the two 10-Qs, both at the value 119000000000. The current 10-Q uses nvda:SupplyAndCapacityCommitmentsMember. The prior 10-Q used nvda:ManufacturingProductionAndLongTermSupplyAndCapacityAgreementCommitmentsMember. The input itself does not call this a change of tag; I report the member name difference only.",
  "account": "Commitments: supply and capacity (member name)",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"value\": \"119000000000\"",
  "paragraph_id": "0001045810-26-000075:facts:OtherCommitment:2026-04-26:us-gaap:OtherCommitmentsAxis=nvda:SupplyAndCapacityCommitmentsMember" }
```

```json
{ "id": "liquidity_and_capital_long_term_debt_filed_fact",
  "what_changed": "LongTermDebt is 33366000000 at 2026-07-26. The same filing prints 8468000000 at 2026-01-25; the prior 10-Q printed 8470000000 at 2026-04-26. LongTermDebtNoncurrent is 32366000000, and LongTermDebtFairValue is 31400000000 at 2026-07-26. Notes carried at 0 at 2026-01-25 and non-zero at 2026-07-26 include the 2028 (one), 2029, 2031 (one), 2033, 2036, 2046 and 2056 notes.",
  "account": "Long-term debt",
  "expected_direction": "none",
  "horizon": "next four quarters",
  "quote": "\"value\": \"33366000000\"",
  "paragraph_id": "0001045810-26-000075:facts:LongTermDebt:2026-07-26" }
```

```json
{ "id": "liquidity_and_capital_notes_issued_face_amount_filed_fact",
  "what_changed": "DebtInstrumentFaceAmount on notes payable is 25000000000.0 at 2026-06-30. ProceedsFromDebtNetOfIssuanceCosts is 24896000000 for 2026-01-26..2026-07-26 and 0 for 2025-01-27..2025-07-27.",
  "account": "Notes issued in the quarter",
  "expected_direction": "none",
  "horizon": "next four quarters",
  "quote": "\"value\": \"25000000000.0\"",
  "paragraph_id": "0001045810-26-000075:facts:DebtInstrumentFaceAmount:2026-06-30:us-gaap:LongtermDebtTypeAxis=us-gaap:NotesPayableOtherPayablesMember" }
```

```json
{ "id": "liquidity_and_capital_interest_expense_latest_quarter_filed_fact",
  "what_changed": "InterestExpenseNonoperating is 227000000 for 2026-04-27..2026-07-26. The same filing prints 62000000 for 2025-04-28..2025-07-27, 329000000 for 2026-01-26..2026-07-26 and 124000000 for 2025-01-27..2025-07-27.",
  "account": "Interest expense",
  "expected_direction": "none",
  "horizon": "next two quarters",
  "quote": "\"value\": \"227000000\"",
  "paragraph_id": "0001045810-26-000075:facts:InterestExpenseNonoperating:2026-04-27..2026-07-26" }
```

```json
{ "id": "estimates_and_discretion_effective_tax_rate_latest_quarter_filed_fact",
  "what_changed": "EffectiveIncomeTaxRateContinuingOperations is 0.165 for 2026-04-27..2026-07-26. The same filing prints 0.153 for 2025-04-28..2025-07-27, 0.165 for 2026-01-26..2026-07-26 and 0.149 for 2025-01-27..2025-07-27. The prior 10-Q printed 0.166 for 2026-01-26..2026-04-26. The release (paragraph 18) expects a full-year rate between 16.0% and 18.0%.",
  "account": "Income tax expense: effective rate",
  "expected_direction": "none",
  "horizon": "next two quarters",
  "quote": "\"value\": \"0.165\"",
  "paragraph_id": "0001045810-26-000075:facts:EffectiveIncomeTaxRateContinuingOperations:2026-04-27..2026-07-26" }
```

```json
{ "id": "liquidity_and_capital_taxes_payable_current_filed_fact",
  "what_changed": "TaxesPayableCurrent is 5206000000 at 2026-07-26. The same filing prints 2669000000 at 2026-01-25. The prior 10-Q printed 10638000000 at 2026-04-26.",
  "account": "Income taxes payable, current",
  "expected_direction": "none",
  "horizon": "next two quarters",
  "quote": "\"value\": \"5206000000\"",
  "paragraph_id": "0001045810-26-000075:facts:TaxesPayableCurrent:2026-07-26" }
```

```json
{ "id": "estimates_and_discretion_accrued_income_taxes_noncurrent_filed_fact",
  "what_changed": "AccruedIncomeTaxesNoncurrent is 5602000000 at 2026-07-26. The same filing prints 3958000000 at 2026-01-25. The 10-K printed unrecognized tax benefits of 4420000000 at 2026-01-25 and 2861000000 at 2025-01-26.",
  "account": "Income taxes payable, noncurrent",
  "expected_direction": "none",
  "horizon": "next four quarters",
  "quote": "\"value\": \"5602000000\"",
  "paragraph_id": "0001045810-26-000075:facts:AccruedIncomeTaxesNoncurrent:2026-07-26" }
```

```json
{ "id": "liquidity_and_capital_repurchase_authorization_remaining_filed_fact",
  "what_changed": "StockRepurchaseProgramRemainingAuthorizedRepurchaseAmount1 is 99300000000 at 2026-07-26. The prior 10-Q printed 38500000000 at 2026-04-26; the 10-K printed 58500000000. Shares repurchased: 94000000 for 2026-04-27..2026-07-26 and 203000000 for 2026-01-26..2026-07-26.",
  "account": "Share repurchase authorization remaining",
  "expected_direction": "none",
  "horizon": "next four quarters",
  "quote": "\"value\": \"99300000000\"",
  "paragraph_id": "0001045810-26-000075:facts:StockRepurchaseProgramRemainingAuthorizedRepurchaseAmount1:2026-07-26" }
```

```json
{ "id": "liquidity_and_capital_dividend_per_share_declared_filed_fact",
  "what_changed": "CommonStockDividendsPerShareDeclared is 0.25 for 2026-04-27..2026-07-26 and 0.01 for 2025-04-28..2025-07-27. DividendsCommonStockCash is 6047000000 against 244000000 for the same two quarters. The prior 10-Q tagged a 0.25 dividend as a subsequent event on 2026-05-18.",
  "account": "Dividends declared per share",
  "expected_direction": "none",
  "horizon": "next four quarters",
  "quote": "\"value\": \"0.25\"",
  "paragraph_id": "0001045810-26-000075:facts:CommonStockDividendsPerShareDeclared:2026-04-27..2026-07-26" }
```

```json
{ "id": "earnings_quality_operating_cash_flow_six_months_filed_fact",
  "what_changed": "NetCashProvidedByUsedInOperatingActivities is 74421000000 for 2026-01-26..2026-07-26 and 42779000000 for 2025-01-27..2025-07-27. NetIncomeLoss for the same six months is 118010000000 and 45197000000. The record holds no three-month operating cash flow row for 2026-04-27..2026-07-26, which is why the quarterly accruals cell is unfilled. The prior 10-Q printed 50344000000 for 2026-01-26..2026-04-26.",
  "account": "Net cash provided by operating activities",
  "expected_direction": "down",
  "horizon": "next two quarters",
  "quote": "\"value\": \"74421000000\"",
  "paragraph_id": "0001045810-26-000075:facts:NetCashProvidedByUsedInOperatingActivities:2026-01-26..2026-07-26" }
```

```json
{ "id": "earnings_quality_receivables_cash_flow_change_six_months_filed_fact",
  "what_changed": "IncreaseDecreaseInAccountsReceivable is 24590000000 for 2026-01-26..2026-07-26 and 4743000000 for 2025-01-27..2025-07-27. The release cash flow shows (22,346) for the three months ended July 26, 2026.",
  "account": "Change in accounts receivable (cash flow)",
  "expected_direction": "down",
  "horizon": "next two quarters",
  "quote": "\"value\": \"24590000000\"",
  "paragraph_id": "0001045810-26-000075:facts:IncreaseDecreaseInAccountsReceivable:2026-01-26..2026-07-26" }
```

```json
{ "id": "earnings_quality_inventories_cash_flow_change_six_months_filed_fact",
  "what_changed": "IncreaseDecreaseInInventories is 10204000000 for 2026-01-26..2026-07-26 and 4880000000 for 2025-01-27..2025-07-27.",
  "account": "Change in inventories (cash flow)",
  "expected_direction": "down",
  "horizon": "next two quarters",
  "quote": "\"value\": \"10204000000\"",
  "paragraph_id": "0001045810-26-000075:facts:IncreaseDecreaseInInventories:2026-01-26..2026-07-26" }
```

```json
{ "id": "earnings_quality_prepaid_and_other_assets_cash_flow_change_six_months_filed_fact",
  "what_changed": "IncreaseDecreaseInPrepaidDeferredExpenseAndOtherAssets is 6480000000 for 2026-01-26..2026-07-26 and -946000000 for 2025-01-27..2025-07-27. OtherAssetsNoncurrent is 15746000000 at 2026-07-26 and 8301000000 at 2026-01-25.",
  "account": "Change in prepaid expenses and other assets (cash flow)",
  "expected_direction": "none",
  "horizon": "next two quarters",
  "quote": "\"value\": \"6480000000\"",
  "paragraph_id": "0001045810-26-000075:facts:IncreaseDecreaseInPrepaidDeferredExpenseAndOtherAssets:2026-01-26..2026-07-26" }
```

```json
{ "id": "liquidity_and_capital_operating_lease_liability_filed_fact",
  "what_changed": "OperatingLeaseLiability is 5494000000 at 2026-07-26; the prior 10-Q printed 4344000000 at 2026-04-26. Right-of-use assets obtained are 2792000000 for 2026-01-26..2026-07-26 against 458000000 a year earlier. The weighted-average discount rate is 0.0469 at 2026-07-26 and 0.0438 at 2026-01-25. Operating lease cost is 208000000 for the quarter and 109000000 a year earlier.",
  "account": "Operating lease liabilities",
  "expected_direction": "none",
  "horizon": "next four quarters",
  "quote": "\"value\": \"5494000000\"",
  "paragraph_id": "0001045810-26-000075:facts:OperatingLeaseLiability:2026-07-26" }
```

```json
{ "id": "liquidity_and_capital_leases_not_yet_commenced_prior_quarter_filed_fact",
  "what_changed": "The prior 10-Q tags an unrecorded obligation for operating leases not yet commenced of 32400000000 at 2026-04-26.",
  "account": "Operating leases not yet commenced",
  "expected_direction": "none",
  "horizon": "next four quarters",
  "quote": "\"value\": \"32400000000\"",
  "paragraph_id": "0001045810-26-000052:facts:UnrecordedUnconditionalPurchaseObligationBalanceSheetAmount:2026-04-26:us-gaap:UnrecordedUnconditionalPurchaseObligationByCategoryOfItemPurchasedAxis=us-gaap:OperatingLeaseLeaseNotYetCommencedMember" }
```

```json
{ "id": "estimates_and_discretion_unrecognized_stock_compensation_filed_fact",
  "what_changed": "Unrecognized share-based compensation cost is 19400000000 at 2026-07-26. The prior 10-Q printed 20800000000 at 2026-04-26.",
  "account": "Unrecognized stock-based compensation",
  "expected_direction": "none",
  "horizon": "next four quarters",
  "quote": "\"value\": \"19400000000\"",
  "paragraph_id": "0001045810-26-000075:facts:EmployeeServiceShareBasedCompensationNonvestedAwardsTotalCompensationCostNotYetRecognized:2026-07-26" }
```

```json
{ "id": "earnings_quality_stock_compensation_expense_latest_quarter_filed_fact",
  "what_changed": "AllocatedShareBasedCompensationExpense is 2027000000 for 2026-04-27..2026-07-26. The same filing prints 1624000000 for 2025-04-28..2025-07-27, 3954000000 for 2026-01-26..2026-07-26 and 3099000000 for 2025-01-27..2025-07-27. The release states that non-GAAP measures no longer exclude this expense.",
  "account": "Stock-based compensation expense",
  "expected_direction": "none",
  "horizon": "next two quarters",
  "quote": "\"value\": \"2027000000\"",
  "paragraph_id": "0001045810-26-000075:facts:AllocatedShareBasedCompensationExpense:2026-04-27..2026-07-26" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_commitments_and_contingencies_nil_filed_fact",
  "what_changed": "CommitmentsAndContingencies is tagged nil at 2026-07-26. It is also nil at 2026-01-25, and the prior 10-Q tagged it nil.",
  "account": "Commitments and contingencies (balance sheet caption)",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"nil\": true",
  "paragraph_id": "0001045810-26-000075:facts:CommitmentsAndContingencies:2026-07-26" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_loss_contingency_accrual_filed_fact",
  "what_changed": "LossContingencyAccrualAtCarryingValue is 0 at 2026-07-26. The prior 10-Q also printed 0 at 2026-04-26.",
  "account": "Loss contingency accrual",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"value\": \"0\"",
  "paragraph_id": "0001045810-26-000075:facts:LossContingencyAccrualAtCarryingValue:2026-07-26" }
```

```json
{ "id": "structure_and_disclosure_changes_goodwill_increase_filed_fact",
  "what_changed": "GoodwillPeriodIncreaseDecrease is 293000000 for 2026-01-26..2026-07-26. Goodwill is 21125000000 at 2026-07-26 and 20832000000 at 2026-01-25.",
  "account": "Goodwill",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"value\": \"293000000\"",
  "paragraph_id": "0001045810-26-000075:facts:GoodwillPeriodIncreaseDecrease:2026-01-26..2026-07-26" }
```

```json
{ "id": "earnings_quality_other_nonoperating_expense_latest_quarter_filed_fact",
  "what_changed": "OtherNonoperatingIncomeExpense is -267000000 for 2026-04-27..2026-07-26. The same filing prints -11000000 for 2025-04-28..2025-07-27, -275000000 for 2026-01-26..2026-07-26 and -18000000 for 2025-01-27..2025-07-27.",
  "account": "Other non-operating income (expense)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"-267000000\"",
  "paragraph_id": "0001045810-26-000075:facts:OtherNonoperatingIncomeExpense:2026-04-27..2026-07-26" }
```

```json
{ "id": "liquidity_and_capital_capital_expenditures_incurred_not_paid_filed_fact",
  "what_changed": "CapitalExpendituresIncurredButNotYetPaid is 1200000000 for 2026-01-26..2026-07-26 and 1100000000 for 2025-01-27..2025-07-27. PaymentsToAcquireProductiveAssets is 4434000000 against 3122000000 for the same periods.",
  "account": "Capital expenditures incurred but not yet paid",
  "expected_direction": "none",
  "horizon": "next two quarters",
  "quote": "\"value\": \"1200000000\"",
  "paragraph_id": "0001045810-26-000075:facts:CapitalExpendituresIncurredButNotYetPaid:2026-01-26..2026-07-26" }
```

### From the 8-K earnings release (0001045810-26-000073, filed 2026-08-26)

```json
{ "id": "structure_and_disclosure_changes_non_gaap_measures_now_include_stock_compensation",
  "what_changed": "The release states a change in the non-GAAP definition: from the first quarter of fiscal 2027, non-GAAP measures no longer exclude stock-based compensation, and history has been updated to match. The trend table's non_gaap_gap is unfilled in every period, so the record cannot show the effect.",
  "account": "Non-GAAP measures definition",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "non-GAAP financial measures no longer exclude stock-based compensation expense. The historical non-GAAP financial information presented has been updated to include stock-based compensation expense.",
  "paragraph_id": "0001045810-26-000073:8k_2_02:57" }
```

```json
{ "id": "across_documents_quarterly_operating_cash_flow_printed_in_release_only",
  "what_changed": "The release cash flow statement prints net cash provided by operating activities of 24,077 for the three months ended July 26, 2026 (15,365 a year earlier). The trend table found no three-month operating cash flow row in the record for 2026-04-27..2026-07-26; the 10-Q facts carry six-month operating cash flow only (74421000000).",
  "account": "Net cash provided by operating activities",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "Net cash provided by operating activities | 24,077",
  "paragraph_id": "0001045810-26-000073:8k_2_02:71" }
```

```json
{ "id": "earnings_quality_export_charges_and_releases_footnote_in_release",
  "what_changed": "The release footnotes H20 charges and releases inside the reported periods. For fiscal 2026 they were $4.5 billion in the first quarter and ($180 million) in the second quarter; for fiscal 2027 they were none in the first quarter and insignificant in the second. The year-ago comparison bases for gross margin include these items.",
  "account": "Cost of revenue: H20 charges and releases",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "Includes H20 charges/(releases), net, which were $4.5 billion and none for the first quarter, and ($180 million) and insignificant for the second quarter, of fiscal years 2026 and 2027, respectively.",
  "paragraph_id": "0001045810-26-000073:8k_2_02:74" }
```

```json
{ "id": "across_documents_repurchase_authorization_release_versus_filing",
  "what_changed": "The release states approximately $99.0 billion remaining under the repurchase authorization at the end of the second quarter. The 10-Q fact StockRepurchaseProgramRemainingAuthorizedRepurchaseAmount1 at 2026-07-26 is 99300000000. Both figures are as printed; I compute no difference.",
  "account": "Share repurchase authorization remaining",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "As of the end of the second quarter, the company had approximately $99.0 billion remaining under its share repurchase authorization.",
  "paragraph_id": "0001045810-26-000073:8k_2_02:8" }
```

```json
{ "id": "liquidity_and_capital_groq_payment_in_financing_activities",
  "what_changed": "The release cash flow statement shows a financing outflow on a line named 'Groq, Inc.' of (2,944) for the three and six months ended July 26, 2026, and none a year earlier. The 10-K facts tied Groq to goodwill of 14400000000, acquisition payments of 13000000000.0 and liabilities incurred of 4000000000.",
  "account": "Financing activities: Groq, Inc.",
  "expected_direction": "none",
  "horizon": "next four quarters",
  "quote": "Groq, Inc. | (2,944)",
  "paragraph_id": "0001045810-26-000073:8k_2_02:72" }
```

```json
{ "id": "results_against_expectations_third_quarter_revenue_outlook_release",
  "what_changed": "The release outlook for the third quarter of fiscal 2027 is revenue of $108.0 billion, plus or minus 2%, with no Data Center compute revenue from China assumed. My input holds no consensus or expectation figure, so whether results or outlook beat expectations is insufficient.",
  "account": "Revenue outlook",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "Revenue is expected to be $108.0 billion, plus or minus 2%. NVIDIA is not assuming any Data Center compute revenue from China in its outlook.",
  "paragraph_id": "0001045810-26-000073:8k_2_02:15" }
```

```json
{ "id": "results_against_expectations_non_gaap_net_income_printed_in_release",
  "what_changed": "The release prints non-GAAP net income of $53,954 (Q2 FY27), $45,548 (Q1 FY27) and $24,763 (Q2 FY26). GAAP net income in the GAAP summary is $59,688, $58,321 and $26,422. Diluted EPS is $2.46 GAAP and $2.22 non-GAAP. No gap is computed here; the trend table's non_gaap_gap cell is unfilled.",
  "account": "Non-GAAP net income",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "Net income | $53,954 | $45,548 | $24,763",
  "paragraph_id": "0001045810-26-000073:8k_2_02:12" }
```

---

## Seen in the notes

No fact in `input_numbers.json` carries a marker saying whether its element sat inside a note when it was extracted. I checked every field on every fact I read. So I can place no item under this heading without judging note membership myself, which I am told not to do.

Several numeric-fact items above may come from tables that sit inside notes in the filings: inventory write-downs, the warranty roll-forward, contract liabilities, customer concentration, commitments, guarantees, debt instruments, leases and tax. They appear under "Seen in the statements" only because the input gives no marker. The later split should not read that placement as a finding about where they sat.
