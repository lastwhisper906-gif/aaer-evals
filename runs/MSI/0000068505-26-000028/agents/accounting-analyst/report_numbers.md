<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
**Reader notes: what this report rests on, and what it could not reach. These notes are not items.**

- **Company and filing.** Motorola Solutions, Inc. (MSI), 10-Q 0000068505-26-000028, quarter ended 2026-07-04, cutoff 2026-08-05. The earnings release is 8-K 0000068505-26-000027.
- **Files read.** `input_trends.json`, `input_8k.md` and `input_prior_predictions.md` were read in full. The prior-predictions file says "None on record", so there are no earlier flags to carry forward.
- **Coverage of `input_numbers.json`.** The file holds a document list and a fact list, 108,950 lines in total. It is too large to read in one pass, and I did not read every line. I read:
  - the current 10-Q's statement facts: income statement, comprehensive income, balance sheet, the start of the equity statement, cash flows and supplemental cash items (lines 76,590–84,100);
  - its closing facts (lines 107,500–108,950);
  - the 10-K's opening facts and its balance-sheet and equity facts (lines 1–400 and 2,380–4,800);
  - spot windows of the prior 10-Q.

  Every fact item below quotes a row I actually saw.
- **Inputs missing from my directory.** There are no articulation checks, no restatement traces and no fourth-quarter derivation (`src/fourth_quarter.py` output). That means I have no articulation gap and no restated prior value that I can quote.
  - Some 10-K facts carry a `superseded_by` field naming 0000068505-26-000028.
  - No field says that the later value differs.
  - In every superseded fact I read, the value matched the 10-Q fact for the same period, e.g. `Assets` 2025-12-31 is 19389000000 in both filings.
  - So I report no restated value.
- **Periods the record does not reach.** Two quarters have no cells at all: quarters-back-2 (target end 2026-01-03) and quarters-back-6 (target end 2025-01-04). The reason given for both is: "no quarter ending within 20 days of [target] is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py". That derivation is not in my input. As a result:
  - every quarterly position below is out of 6 filled quarters, not 8;
  - quarter-over-quarter comparisons against those two periods are unavailable.
- **Formula baseline with no `paragraph_id`.** The years-back-0 `research_and_development_capitalized` block prints the following values:
  - `book_value_with_rnd_capitalized` 5086800000.0
  - `earnings_with_rnd_capitalized` 2329200000.0
  - `research_and_development_asset` 2676800000.0
  - `research_and_development_amortization` 794800000.0
  - `capitalized_development_cost` and `capitalized_over_expense` are missing, with the reason "no row for capitalized_development_cost: the companyfacts record tags none of us-gaap:CapitalizedComputerSoftwareAdditions in any period…" (insufficient).

  The block prints no `paragraph_id`, so none of it can be an item. Years-back-1 to -4 hold the same kind of block.
- **No in-note marker on any fact.** None of the facts I read prints a field saying whether its element sat inside a note. The fields printed are:
  - `id`, `paragraph_id`, `tag`, `prefix`, `namespace`, `context`, `context_ref`, `unit`, `decimals`;
  - `value`, `number`, `nil`, `form`, `source_accession`, `filing_date`;
  - sometimes `superseded_by`.

  Because the marker is absent, every fact item sits under the first heading by default. I also left note-region facts (goodwill by segment, intangible-asset classes, acquisition prices) out of the items rather than judge where they came from.
- **Check for data I should not see.** I found no price series, abnormal returns, short interest, other companies' files, prior probabilities or outcome window. One company-reported figure comes close: 8-K paragraph 0000068505-26-000027:8k_2_02:26 states the average price paid per share for buybacks during the quarter. It is part of the earnings release I was given, not a market price series or an outcome. I did not use it, and I flag it here so the run owner can decide.
- **Sections I cannot quote.** The 8-K's item-code list and its late-filing section ("none on or before 2026-08-05") carry no `[id]` line, so they cannot be quoted.
- **How quotes are cut.**
  - Warranty-reason rows are quoted up to the em dash. The file stores that character as an escape sequence, and stopping there keeps the quote a plain substring.
  - Table rows from the 8-K are quoted with their spacing exactly as printed.
- **Meaning of `expected_direction`.** It is the direction the input itself states for the account over the horizon. Where the input states no forward expectation it is `none`. It is never inferred from where a value sits in its history.
- **No arithmetic.** Every number in `what_changed` is copied as printed. Where a comparison appears, both printed figures are given and nothing was computed.

## Seen in the statements

**Trend table: quarters-back-0 (2026-04-05..2026-07-04)**

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly_trend",
  "what_changed": "bad_debt_reserve_ratio for 2026-04-05..2026-07-04 is 0.03700401248328132 (inputs: AllowanceForDoubtfulAccountsReceivableCurrent 83000000, AccountsReceivableNetCurrent 2160000000). quarter_over_quarter change -0.0024326072350285416 against quarters-back-1; year_over_year change -0.001916589488695844 against quarters-back-4. Position as printed: lowest of the 6 filled quarters. In the same quarter receivables_over_revenue prints third highest of the 6 filled quarters.",
  "account": "Allowance for doubtful accounts against accounts receivable",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0000068505-26-000028:trends:bad_debt_reserve_ratio:2026-04-05..2026-07-04" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly_trend",
  "what_changed": "contract_liabilities_over_revenue for 2026-04-05..2026-07-04 is 0.7472071496967763 (inputs: ContractWithCustomerLiabilityCurrent 2341000000, quarterly revenue 3133000000). quarter_over_quarter change -0.09877663807035708 against quarters-back-1; year_over_year change 0.01809322564614335 against quarters-back-4. Position as printed: third highest of the 6 filled quarters.",
  "account": "Contract liabilities (deferred revenue) against revenue",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "\"position_in_history\": \"third highest of the 6 filled quarters\"",
  "paragraph_id": "0000068505-26-000028:trends:contract_liabilities_over_revenue:2026-04-05..2026-07-04" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_quarterly_trend",
  "what_changed": "days_sales_of_inventory for 2026-04-05..2026-07-04 is 83.36975945017181 (inputs: InventoryNet 1333000000 at 2026-07-04, CostOfGoodsAndServicesSold 1455000000 for the quarter, 91 days). quarter_over_quarter change 1.2588127046096815 against quarters-back-1; year_over_year change 25.41783637324874 against quarters-back-4. Position as printed: highest of the 6 filled quarters. In the same quarter inventory_reserve_ratio prints lowest of the 6 filled quarters. The release says the company expects inventory to remain elevated; see the narrative item.",
  "account": "Inventories against cost of sales",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0000068505-26-000028:trends:days_sales_of_inventory:2026-04-05..2026-07-04" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly_trend",
  "what_changed": "days_sales_outstanding for 2026-04-05..2026-07-04 is 62.738589211618255 (inputs: AccountsReceivableNetCurrent 2160000000, quarterly revenue 3133000000, 91 days). quarter_over_quarter change -8.12508064836701 against quarters-back-1; year_over_year change 1.7866904774410415 against quarters-back-4. Position as printed: second highest of the 6 filled quarters.",
  "account": "Accounts receivable against revenue",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"",
  "paragraph_id": "0000068505-26-000028:trends:days_sales_outstanding:2026-04-05..2026-07-04" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly_trend",
  "what_changed": "gross_margin for 2026-04-05..2026-07-04 is 0.5355888924353654 (inputs: revenue 3133000000, CostOfGoodsAndServicesSold 1455000000). quarter_over_quarter change 0.03374659324597706 against quarters-back-1; year_over_year change 0.02455815102487724 against quarters-back-4. Position as printed: highest of the 6 filled quarters. The release says cost of sales for this quarter includes a $60 million favorable IEEPA tariff-refund adjustment; see the release items.",
  "account": "Gross margin (revenue less cost of sales)",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0000068505-26-000028:trends:gross_margin:2026-04-05..2026-07-04" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly_trend",
  "what_changed": "inventory_reserve_ratio for 2026-04-05..2026-07-04 is 0.09977494373593399 (inputs: InventoryValuationReserves 133000000, InventoryNet 1333000000). quarter_over_quarter change -0.004374082513007596 against quarters-back-1; year_over_year change -0.04540507949286973 against quarters-back-4. Position as printed: lowest of the 6 filled quarters, while days_sales_of_inventory prints highest of the 6 filled quarters in the same quarter.",
  "account": "Inventory valuation reserve against inventories",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0000068505-26-000028:trends:inventory_reserve_ratio:2026-04-05..2026-07-04" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarterly_trend",
  "what_changed": "receivables_over_revenue for 2026-04-05..2026-07-04 is 0.6894350462815193 (inputs: AccountsReceivableNetCurrent 2160000000, quarterly revenue 3133000000). quarter_over_quarter change -0.0644337820161962 against quarters-back-1; year_over_year change 0.019633961290560942 against quarters-back-4. Position as printed: third highest of the 6 filled quarters.",
  "account": "Accounts receivable against revenue",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "\"position_in_history\": \"third highest of the 6 filled quarters\"",
  "paragraph_id": "0000068505-26-000028:trends:receivables_over_revenue:2026-04-05..2026-07-04" }
```

```json
{ "id": "earnings_quality_soft_asset_share_quarterly_trend",
  "what_changed": "soft_asset_share for 2026-04-05..2026-07-04 is 0.9024529674669993 (inputs: Assets 19242000000, PP&E 1167000000 tagged PropertyPlantAndEquipmentAndFinanceLeaseRightOfUseAssetAfterAccumulatedDepreciationAndAmortization, cash 710000000). quarter_over_quarter change 0.009738082770982537 against quarters-back-1; year_over_year change 0.16299403497857623 against quarters-back-4. Position as printed: highest of the 6 filled quarters.",
  "account": "Non-cash, non-PP&E assets against total assets",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0000068505-26-000028:trends:soft_asset_share:2026-04-05..2026-07-04" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly_insufficient",
  "what_changed": "insufficient: accruals_over_total_assets has no value for 2026-04-05..2026-07-04. The cell gives the quoted reason, and its quarter_over_quarter and year_over_year rows both print 'accruals_over_total_assets is not filled in quarters-back-0'. The 10-Q facts hold operating cash flow only for 2026-01-01..2026-07-04 (920000000). The three-month figure exists only in the earnings release; see the across-documents item.",
  "account": "Accruals (net income less operating cash flow) against total assets",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-04-05..2026-07-04: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0000068505-26-000028:trends:accruals_over_total_assets:2026-04-05..2026-07-04" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly_insufficient",
  "what_changed": "insufficient: non_gaap_gap has no value for 2026-04-05..2026-07-04, and both comparison rows print 'non_gaap_gap is not filled in quarters-back-0'. The gap cannot be filled from companyfacts in any period. The release prints its own non-GAAP figures; see the across-documents item.",
  "account": "Non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0000068505-26-000028:trends:non_gaap_gap:2026-04-05..2026-07-04" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly_insufficient",
  "what_changed": "insufficient: warranty_reserve_ratio has no value for 2026-04-05..2026-07-04, and it is filled in 0 of the periods the table holds. The record tags no entity-wide warranty accrual. The 10-Q text is not in my input, so I cannot say whether the company states the accrual only by segment or does not tag it at all.",
  "account": "Product warranty accrual",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0000068505-26-000028:trends:warranty_reserve_ratio:2026-04-05..2026-07-04" }
```

**Trend table: years-back-0 (2025-01-01..2025-12-31)**

```json
{ "id": "earnings_quality_accruals_over_total_assets_annual_trend",
  "what_changed": "accruals_over_total_assets for 2025-01-01..2025-12-31 is -0.035226159162411674 (inputs: NetIncomeLoss 2154000000, NetCashProvidedByUsedInOperatingActivities 2837000000, Assets 19389000000). year_over_year change 0.020546365674861365 against years-back-1; quarter_over_quarter prints 'an annual period has no preceding quarter'. Position as printed: second highest of the 5 filled years. Operating cash flow exceeds net income, so the value is negative.",
  "account": "Accruals (net income less operating cash flow) against total assets",
  "expected_direction": "none",
  "horizon": "next 10-K",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0000068505-26-000028:trends:accruals_over_total_assets:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual_trend",
  "what_changed": "bad_debt_reserve_ratio at 2025-12-31 is 0.036355672360928605 (inputs: AllowanceForDoubtfulAccountsReceivableCurrent 83000000, AccountsReceivableNetCurrent 2200000000). year_over_year change -0.004430568425312184 against years-back-1. Position as printed: lowest of the 5 filled years. In the same year receivables_over_revenue and days_sales_outstanding both print highest of the 5 filled years.",
  "account": "Allowance for doubtful accounts against accounts receivable",
  "expected_direction": "none",
  "horizon": "next 10-K",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0000068505-26-000028:trends:bad_debt_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual_trend",
  "what_changed": "contract_liabilities_over_revenue for 2025 is 0.19388803287108372 (inputs: ContractWithCustomerLiabilityCurrent 2265000000, annual revenue 11682000000). year_over_year change 0.002337695439263432 against years-back-1. Position as printed: second lowest of the 5 filled years.",
  "account": "Contract liabilities (deferred revenue) against revenue",
  "expected_direction": "none",
  "horizon": "next 10-K",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0000068505-26-000028:trends:contract_liabilities_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_annual_trend",
  "what_changed": "days_sales_of_inventory for 2025 is 63.53727642996281 (inputs: InventoryNet 983000000 at 2025-12-31, CostOfGoodsAndServicesSold 5647000000, 365 days). year_over_year change 10.689774073695133 against years-back-1. Position as printed: third highest of the 5 filled years.",
  "account": "Inventories against cost of sales",
  "expected_direction": "none",
  "horizon": "next 10-K",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0000068505-26-000028:trends:days_sales_of_inventory:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual_trend",
  "what_changed": "days_sales_outstanding for 2025 is 68.7382297551789 (inputs: AccountsReceivableNetCurrent 2200000000, annual revenue 11682000000, 365 days). year_over_year change 2.6910817474133495 against years-back-1. Position as printed: highest of the 5 filled years.",
  "account": "Accounts receivable against revenue",
  "expected_direction": "none",
  "horizon": "next 10-K",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000068505-26-000028:trends:days_sales_outstanding:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_gross_margin_annual_trend",
  "what_changed": "gross_margin for 2025 is 0.5166067454203047 (inputs: revenue 11682000000, CostOfGoodsAndServicesSold 5647000000). year_over_year change 0.007038473256118727 against years-back-1. Position as printed: highest of the 5 filled years.",
  "account": "Gross margin (revenue less cost of sales)",
  "expected_direction": "none",
  "horizon": "next 10-K",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000068505-26-000028:trends:gross_margin:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_annual_trend",
  "what_changed": "inventory_reserve_ratio at 2025-12-31 is 0.11800610376398779 (inputs: InventoryValuationReserves 116000000, InventoryNet 983000000). year_over_year change -0.04909572391225242 against years-back-1. Position as printed: lowest of the 5 filled years.",
  "account": "Inventory valuation reserve against inventories",
  "expected_direction": "none",
  "horizon": "next 10-K",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0000068505-26-000028:trends:inventory_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual_trend",
  "what_changed": "receivables_over_revenue for 2025 is 0.18832391713747645 (inputs: AccountsReceivableNetCurrent 2200000000, annual revenue 11682000000). year_over_year change 0.00786722859166894 against years-back-1. Position as printed: highest of the 5 filled years.",
  "account": "Accounts receivable against revenue",
  "expected_direction": "none",
  "horizon": "next 10-K",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000068505-26-000028:trends:receivables_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_soft_asset_share_annual_trend",
  "what_changed": "soft_asset_share at 2025-12-31 is 0.8798287688895766 (inputs: Assets 19389000000, cash 1165000000, PP&E 1165000000 tagged PropertyPlantAndEquipmentNet). year_over_year change 0.09387467502181368 against years-back-1. Position as printed: highest of the 5 filled years.",
  "account": "Non-cash, non-PP&E assets against total assets",
  "expected_direction": "none",
  "horizon": "next 10-K",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000068505-26-000028:trends:soft_asset_share:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual_insufficient",
  "what_changed": "insufficient: non_gaap_gap has no value for 2025-01-01..2025-12-31, and the year_over_year row prints 'non_gaap_gap is not filled in years-back-0'. It is filled in none of the 5 years.",
  "account": "Non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "next 10-K",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0000068505-26-000028:trends:non_gaap_gap:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_annual_insufficient",
  "what_changed": "insufficient: warranty_reserve_ratio has no value for 2025-01-01..2025-12-31, and the year_over_year row prints 'warranty_reserve_ratio is not filled in years-back-0'. It is filled in none of the 5 years.",
  "account": "Product warranty accrual",
  "expected_direction": "none",
  "horizon": "next 10-K",
  "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0000068505-26-000028:trends:warranty_reserve_ratio:2025-01-01..2025-12-31" }
```

**Depth of history**

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly_history_depth",
  "what_changed": "insufficient: quarterly accruals_over_total_assets is filled in only 2 quarters: quarters-back-1 (2026-01-01..2026-04-04, value -0.004454926624737945, year_over_year change 0.0010879265589383525 against quarters-back-5) and quarters-back-5. It is missing in quarters-back-0, -3, -4 and -7 because the 10-Qs state operating cash flow only year-to-date, and missing in -2 and -6 because those fourth quarters were not derived. Two periods do not support a trend claim.",
  "account": "Accruals (net income less operating cash flow) against total assets",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "\"position_in_history\": \"highest of the 2 filled quarters\"",
  "paragraph_id": "0000068505-26-000028:trends:accruals_over_total_assets:2026-01-01..2026-04-04" }
```

**Changes of tag: the quarterly and annual cells rest on different concepts**

```json
{ "id": "structure_and_disclosure_changes_property_plant_equipment_concept_quarterly_cells",
  "what_changed": "Every quarterly soft_asset_share cell (quarters-back-0, -1, -3, -4, -5, -7) takes property_plant_and_equipment from PropertyPlantAndEquipmentAndFinanceLeaseRightOfUseAssetAfterAccumulatedDepreciationAndAmortization (1167000000 at 2026-07-04). Every annual cell (years-back-0 to -4) takes it from PropertyPlantAndEquipmentNet. The quarterly and annual soft_asset_share series therefore rest on different concepts, and the quarterly concept includes finance-lease right-of-use assets by its name.",
  "account": "Property, plant and equipment (soft_asset_share input)",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "\"tag\": \"PropertyPlantAndEquipmentAndFinanceLeaseRightOfUseAssetAfterAccumulatedDepreciationAndAmortization\"",
  "paragraph_id": "0000068505-26-000028:trends:soft_asset_share:2026-04-05..2026-07-04" }
```

```json
{ "id": "structure_and_disclosure_changes_property_plant_equipment_concept_annual_cells",
  "what_changed": "The years-back-0 soft_asset_share cell takes property_plant_and_equipment from PropertyPlantAndEquipmentNet (1165000000 at 2025-12-31, accession 0000068505-26-000010, filed 2026-02-12). Its assets and cash inputs come from the current 10-Q, 0000068505-26-000028. The annual series rests on a different PP&E concept from the quarterly series.",
  "account": "Property, plant and equipment (soft_asset_share input)",
  "expected_direction": "none",
  "horizon": "next 10-K",
  "quote": "\"tag\": \"PropertyPlantAndEquipmentNet\"",
  "paragraph_id": "0000068505-26-000028:trends:soft_asset_share:2025-01-01..2025-12-31" }
```

```json
{ "id": "structure_and_disclosure_changes_property_plant_equipment_concept_annual_report_face",
  "what_changed": "The 10-K (0000068505-26-000010) tags its 2025-12-31 balance-sheet PP&E under PropertyPlantAndEquipmentAndFinanceLeaseRightOfUseAssetAfterAccumulatedDepreciationAndAmortization at 1165000000, and this fact carries superseded_by 0000068505-26-000028. The annual trend cell instead uses PropertyPlantAndEquipmentNet from the same 10-K, which also prints 1165000000. The concept differs; the printed value for 2025-12-31 is the same.",
  "account": "Property, plant and equipment",
  "expected_direction": "none",
  "horizon": "next 10-K",
  "quote": "\"tag\": \"PropertyPlantAndEquipmentAndFinanceLeaseRightOfUseAssetAfterAccumulatedDepreciationAndAmortization\"",
  "paragraph_id": "0000068505-26-000010:facts:PropertyPlantAndEquipmentAndFinanceLeaseRightOfUseAssetAfterAccumulatedDepreciationAndAmortization:2025-12-31" }
```

**Numeric facts (10-Q 0000068505-26-000028 unless stated)**

```json
{ "id": "liquidity_and_capital_inventory_balance_fact",
  "what_changed": "InventoryNet is 1333000000 at 2026-07-04. The same filing prints 983000000 at 2025-12-31, and the prior 10-Q input in the trend table prints 1181000000 at 2026-04-04.",
  "account": "Inventories, net",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "\"value\": \"1333000000\"",
  "paragraph_id": "0000068505-26-000028:facts:InventoryNet:2026-07-04" }
```

```json
{ "id": "liquidity_and_capital_inventory_increase_cash_flow_fact",
  "what_changed": "IncreaseDecreaseInInventories is 355000000 for 2026-01-01..2026-07-04. The comparative fact prints 84000000 for 2025-01-01..2025-06-28. This is the inventory build as it shows in operating cash flow.",
  "account": "Change in inventories (operating cash flow)",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "\"value\": \"355000000\"",
  "paragraph_id": "0000068505-26-000028:facts:IncreaseDecreaseInInventories:2026-01-01..2026-07-04" }
```

```json
{ "id": "estimates_and_discretion_contingent_consideration_remeasurement_fact",
  "what_changed": "BusinessCombinationContingentConsiderationArrangementsChangeInAmountOfContingentConsiderationLiability1 is 91000000 for 2026-01-01..2026-07-04, against 0 for 2025-01-01..2025-06-28. The release reconciliation lists a 'Contingent earnout adjustment' under Other charges (income), 16 for the quarter and 91 for six months, and removes it from non-GAAP results. It is a fair-value remeasurement of an earnout liability that runs through GAAP operating earnings.",
  "account": "Contingent consideration (earnout) liability remeasurement, Other charges",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "\"value\": \"91000000\"",
  "paragraph_id": "0000068505-26-000028:facts:BusinessCombinationContingentConsiderationArrangementsChangeInAmountOfContingentConsiderationLiability1:2026-01-01..2026-07-04" }
```

```json
{ "id": "liquidity_and_capital_operating_cash_flow_fact",
  "what_changed": "NetCashProvidedByUsedInOperatingActivities is 920000000 for 2026-01-01..2026-07-04, against 783000000 for 2025-01-01..2025-06-28. The 10-Q facts give this year-to-date figure only; there is no three-month operating cash flow fact.",
  "account": "Net cash provided by operating activities",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "\"value\": \"920000000\"",
  "paragraph_id": "0000068505-26-000028:facts:NetCashProvidedByUsedInOperatingActivities:2026-01-01..2026-07-04" }
```

```json
{ "id": "liquidity_and_capital_interest_expense_fact",
  "what_changed": "InterestExpenseNonoperating is 103000000 for 2026-04-05..2026-07-04, against 55000000 for 2025-03-30..2025-06-28. The six-month facts print 208000000 against 106000000.",
  "account": "Interest expense, net",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "\"value\": \"103000000\"",
  "paragraph_id": "0000068505-26-000028:facts:InterestExpenseNonoperating:2026-04-05..2026-07-04" }
```

```json
{ "id": "liquidity_and_capital_interest_paid_fact",
  "what_changed": "InterestPaidNet is 229000000 for 2026-01-01..2026-07-04, against 135000000 for 2025-01-01..2025-06-28.",
  "account": "Interest paid",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "\"value\": \"229000000\"",
  "paragraph_id": "0000068505-26-000028:facts:InterestPaidNet:2026-01-01..2026-07-04" }
```

```json
{ "id": "liquidity_and_capital_income_taxes_paid_fact",
  "what_changed": "IncomeTaxesPaidNet is 276000000 for 2026-01-01..2026-07-04, against 315000000 for 2025-01-01..2025-06-28. The release gives lower tax payments as one reason operating cash flow rose.",
  "account": "Income taxes paid",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "\"value\": \"276000000\"",
  "paragraph_id": "0000068505-26-000028:facts:IncomeTaxesPaidNet:2026-01-01..2026-07-04" }
```

```json
{ "id": "liquidity_and_capital_cash_balance_fact",
  "what_changed": "CashAndCashEquivalentsAtCarryingValue is 710000000 at 2026-07-04, against 1165000000 at 2025-12-31 in the same filing. The six-month change in cash is printed as -455000000.",
  "account": "Cash and cash equivalents",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "\"value\": \"710000000\"",
  "paragraph_id": "0000068505-26-000028:facts:CashAndCashEquivalentsAtCarryingValue:2026-07-04" }
```

```json
{ "id": "liquidity_and_capital_accounts_payable_fact",
  "what_changed": "AccountsPayableCurrent is 957000000 at 2026-07-04, against 1134000000 at 2025-12-31 in the same filing.",
  "account": "Accounts payable",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "\"value\": \"957000000\"",
  "paragraph_id": "0000068505-26-000028:facts:AccountsPayableCurrent:2026-07-04" }
```

```json
{ "id": "liquidity_and_capital_accrued_liabilities_fact",
  "what_changed": "AccruedLiabilitiesCurrent is 1666000000 at 2026-07-04, against 1930000000 at 2025-12-31 in the same filing.",
  "account": "Accrued liabilities",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "\"value\": \"1666000000\"",
  "paragraph_id": "0000068505-26-000028:facts:AccruedLiabilitiesCurrent:2026-07-04" }
```

```json
{ "id": "revenue_recognition_contract_assets_fact",
  "what_changed": "ContractWithCustomerAssetNetCurrent is 1455000000 at 2026-07-04, against 1574000000 at 2025-12-31 in the same filing. No trend cell covers contract assets, so this balance has two printed points here and no trend claim is possible.",
  "account": "Contract assets (unbilled revenue)",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "\"value\": \"1455000000\"",
  "paragraph_id": "0000068505-26-000028:facts:ContractWithCustomerAssetNetCurrent:2026-07-04" }
```

```json
{ "id": "earnings_quality_share_based_compensation_fact",
  "what_changed": "ShareBasedCompensation is 204000000 for 2026-01-01..2026-07-04, against 140000000 for 2025-01-01..2025-06-28. The release prints 104 for the quarter against 74 a year earlier and excludes the expense from non-GAAP results.",
  "account": "Share-based compensation expense",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "\"value\": \"204000000\"",
  "paragraph_id": "0000068505-26-000028:facts:ShareBasedCompensation:2026-01-01..2026-07-04" }
```

```json
{ "id": "liquidity_and_capital_share_repurchase_payments_fact",
  "what_changed": "PaymentsForRepurchaseOfCommonStock is 449000000 for 2026-01-01..2026-07-04, against 543000000 for 2025-01-01..2025-06-28. The equity statement prints StockRepurchasedAndRetiredDuringPeriodValue of 326000000 for 2026-04-05..2026-07-04.",
  "account": "Repurchases of common stock",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "\"value\": \"449000000\"",
  "paragraph_id": "0000068505-26-000028:facts:PaymentsForRepurchaseOfCommonStock:2026-01-01..2026-07-04" }
```

```json
{ "id": "structure_and_disclosure_changes_other_operating_expense_line_fact",
  "what_changed": "OtherOperatingIncomeExpenseNet is -113000000 for 2026-04-05..2026-07-04, against -40000000 for 2025-03-30..2025-06-28. The six-month facts print -259000000 against -89000000. The release income statement prints 'Other charges' (18 against 1) and 'Intangibles amortization' (95 against 39) as separate lines, and no release line prints 113. This single XBRL value does not map to one line of the release statement.",
  "account": "Other operating income/expense (XBRL line)",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "\"value\": \"-113000000\"",
  "paragraph_id": "0000068505-26-000028:facts:OtherOperatingIncomeExpenseNet:2026-04-05..2026-07-04" }
```

```json
{ "id": "earnings_quality_goodwill_balance_fact",
  "what_changed": "Goodwill is 6883000000 at 2026-07-04, against 6800000000 at 2025-12-31 in the same filing. The 10-K fact 0000068505-26-000010:facts:Goodwill:2024-12-31 prints 3526000000. Over the same span soft_asset_share prints highest in both its quarterly and annual histories.",
  "account": "Goodwill",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "\"value\": \"6883000000\"",
  "paragraph_id": "0000068505-26-000028:facts:Goodwill:2026-07-04" }
```

**Figures in the 8-K earnings release (not from a note; grouped under this heading because only two headings are allowed)**

```json
{ "id": "estimates_and_discretion_tariff_refund_cost_of_sales_release_figure",
  "what_changed": "Cost of sales for the quarter includes a $60 million favorable adjustment for IEEPA tariff refunds. The company booked it because, after U.S. Customs and Border Protection launched a refund-claim system, it judged recovery of a portion of the refunds 'now probable'. This is a probability judgment by management, and it sits inside the 1455000000 cost-of-revenue input of the quarterly gross_margin cell.",
  "account": "Cost of sales (IEEPA tariff refund receivable)",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "Accordingly, during the quarter ended July 4, 2026, the company recognized a favorable adjustment of $60 million recorded within Cost of sales in its Condensed Consolidated Statements of Operations.",
  "paragraph_id": "0000068505-26-000027:8k_2_02:51" }
```

```json
{ "id": "earnings_quality_tariff_refund_kept_in_non_gaap_release_figure",
  "what_changed": "Footnote 2 says the GAAP and non-GAAP operating earnings, margins and EPS in the summary table include the $60M IEEPA refund benefit ($0.25 per share). The non-GAAP reconciliation (0000068505-26-000027:8k_2_02:132) lists no IEEPA line, while it does remove the Gain on Hytera litigation. This one-time benefit therefore stays inside non-GAAP results.",
  "account": "Non-GAAP operating earnings and EPS",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "Inclusive of a $60M (pre-tax) benefit, or $0.25 per share",
  "paragraph_id": "0000068505-26-000027:8k_2_02:19" }
```

```json
{ "id": "earnings_quality_tariff_refund_margin_basis_points_release_figure",
  "what_changed": "The release puts the IEEPA refund at 190 bps of operating margin. GAAP operating margin is printed as 25.8% against 25.0%, and non-GAAP as 32.9% against 29.6%.",
  "account": "Operating margin",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "inclusive of higher direct material costs and a $60 million benefit, or 190 bps, from IEEPA refunds recorded during the quarter.",
  "paragraph_id": "0000068505-26-000027:8k_2_02:23" }
```

```json
{ "id": "revenue_recognition_acquired_revenue_release_figure",
  "what_changed": "Of the quarter's sales of $3,133 million, the release attributes $243 million to acquisitions and $35 million to foreign-currency tailwinds. Reported growth is printed as 13%.",
  "account": "Net sales (acquired and currency contributions)",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "Revenue from acquisitions was $243 million and foreign currency tailwinds were $35 million in the quarter.",
  "paragraph_id": "0000068505-26-000027:8k_2_02:22" }
```

```json
{ "id": "revenue_recognition_organic_revenue_release_figure",
  "what_changed": "Organic revenue is printed as $2,890 million against $2,765 million, a 5% change, while reported sales are up 13%. For six months the release prints organic revenue of 5,382 against 5,290, a 2% change, against reported growth of 10%.",
  "account": "Organic revenue (non-GAAP)",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "| Organic revenue |  | $ | 2,890 |  |  | $ | 2,765 |  |  | 5 | % |",
  "paragraph_id": "0000068505-26-000027:8k_2_02:157" }
```

```json
{ "id": "across_documents_quarterly_operating_cash_flow_release_figure",
  "what_changed": "The release prints a three-month operating cash flow of $469 million against $272 million. The XBRL record holds operating cash flow only year-to-date, which is why the quarterly accruals_over_total_assets cell is unfilled. This quarterly figure exists only in the release.",
  "account": "Net cash provided by operating activities (three months)",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "Operating cash flow was $469 million, compared to $272 million in the year-ago quarter",
  "paragraph_id": "0000068505-26-000027:8k_2_02:25" }
```

```json
{ "id": "across_documents_quarterly_inventory_cash_use_release_figure",
  "what_changed": "The release's three-month cash-flow statement prints a change in inventories of (156) against (22) a year earlier. The XBRL record gives only the six-month figure, 355000000.",
  "account": "Change in inventories (three months, operating cash flow)",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "| Inventories | (156) |  |  | (22) |  |",
  "paragraph_id": "0000068505-26-000027:8k_2_02:114" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_inventory_expected_elevated_release_figure",
  "what_changed": "Management says it expects inventory to stay elevated while it manages supply-chain volatility. This is consistent with days_sales_of_inventory printing highest of the 6 filled quarters, and with inventory_reserve_ratio printing lowest of the 6 filled quarters. 'Remain elevated' is not a statement of further increase, so the direction is none.",
  "account": "Inventories",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "The company expects inventory levels to remain elevated as it mitigates this dynamic supply chain environment.",
  "paragraph_id": "0000068505-26-000027:8k_2_02:53" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_memory_costs_release_figure",
  "what_changed": "Management reports higher memory-component costs driven by AI demand, together with tariff and import/export uncertainty. It says the environment 'has led to increased costs on materials and components'. Those costs sit inside the same cost of sales that carries the $60 million IEEPA benefit.",
  "account": "Cost of sales (component costs)",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "the company is experiencing higher costs for memory in its products which is a result of substantial demand in the market driven by AI.",
  "paragraph_id": "0000068505-26-000027:8k_2_02:53" }
```

```json
{ "id": "across_documents_non_gaap_gap_release_figure",
  "what_changed": "The trend table cannot fill non_gaap_gap. The release prints the gap itself as about $1.08 per diluted share after tax. Its reconciliation (0000068505-26-000027:8k_2_02:132) prints non-GAAP net earnings of $737 million against GAAP $557 million for the quarter, and $1,303 million against $923 million for six months.",
  "account": "Non-GAAP adjustments",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "Non-GAAP financial information excludes the after-tax impact of approximately $1.08 per diluted share related to highlighted items, share-based compensation expense and intangible assets amortization expense.",
  "paragraph_id": "0000068505-26-000027:8k_2_02:18" }
```

```json
{ "id": "earnings_quality_hytera_gains_excluded_from_non_gaap_release_figure",
  "what_changed": "Hytera litigation gains are recognized in GAAP Other charges and excluded from non-GAAP results. The release lists $61 million (2024), $157 million (2025) and $60 million in the first half of 2026. The reconciliation prints Gain on Hytera litigation of (20) for the quarter against (10) a year earlier.",
  "account": "Other charges (Hytera litigation gains)",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "$61 million realized in 2024, $157 million realized in 2025, and $60 million realized in the first half of 2026.",
  "paragraph_id": "0000068505-26-000027:8k_2_02:71" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_hytera_payments_gain_release_figure",
  "what_changed": "Cumulative Hytera payments against the award are $232 million, of which $60 million came in the first half of 2026. Each payment is recorded as a gain in Other charges when received. The rest of the award, including the copyright damages the District Court must recalculate, remains contingent.",
  "account": "Other charges (Hytera award, gain contingency)",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "Hytera had paid $232 million against this award, $60 million of which was paid in the first half of 2026. These payments were recorded as a gain within Other charges within the Consolidated Statement of Operations.",
  "paragraph_id": "0000068505-26-000027:8k_2_02:67" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_hytera_royalties_uncollected_release_figure",
  "what_changed": "Hytera has reported about $116 million of H-Series royalties subject to the court order. These are under appeal and the company is still seeking to collect them. They are an unrecognized gain contingency.",
  "account": "Royalty receivable (unrecognized gain contingency)",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "While several aspects of the court proceedings related to the H-Series are subject to appeal, the company continues to seek collection of the amounts owed by Hytera through the ongoing legal process.",
  "paragraph_id": "0000068505-26-000027:8k_2_02:70" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_dfend_agreement_release_figure",
  "what_changed": "The company has signed a definitive agreement to acquire D-Fend Solutions for $1.5 billion. Over the same period the release reports cash of $710 million and short-term borrowings of $615 million at July 4, 2026.",
  "account": "Acquisitions (pending), cash and borrowings",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "The company also entered into a definitive agreement to acquire D-Fend Solutions",
  "paragraph_id": "0000068505-26-000027:8k_2_02:26" }
```

```json
{ "id": "results_against_expectations_full_year_revenue_guidance_release_figure",
  "what_changed": "Full-year revenue guidance is raised to about $12.975 billion from $12.8 billion. Non-GAAP EPS guidance is raised to $17.62–$17.72 from $16.87–$16.99. For the third quarter the company guides revenue growth of about 8% and non-GAAP EPS of $4.39–$4.44.",
  "account": "Revenue (company guidance)",
  "expected_direction": "up",
  "horizon": "fiscal year 2026, as guided",
  "quote": "The company now expects revenue of approximately $12.975 billion, up from its prior guidance of $12.8 billion",
  "paragraph_id": "0000068505-26-000027:8k_2_02:46" }
```

```json
{ "id": "results_against_expectations_backlog_release_figure",
  "what_changed": "Ending backlog is $15.6 billion, printed as up 11% or $1.5 billion year over year. Products and Systems Integration backlog is up $329 million and Software and Services backlog is up $1.2 billion. Backlog is not a GAAP balance and appears nowhere in the trend table.",
  "account": "Backlog (non-GAAP disclosure)",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "The company ended the quarter with record Q2 backlog of $15.6 billion, up 11% or $1.5 billion from the year-ago quarter driven by record Q2 orders.",
  "paragraph_id": "0000068505-26-000027:8k_2_02:27" }
```

```json
{ "id": "earnings_quality_effective_tax_rate_release_figure",
  "what_changed": "The GAAP effective tax rate is printed as 24.8% against 24.3%, and the non-GAAP rate as 22.6% against 23.5%. The release attributes the non-GAAP decrease to a higher export-sales deduction. XBRL income tax expense is 184000000 against 165000000 for the quarter.",
  "account": "Income tax expense",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "The GAAP effective tax rate during the quarter was 24.8%, versus 24.3% in the year-ago quarter",
  "paragraph_id": "0000068505-26-000027:8k_2_02:24" }
```

```json
{ "id": "earnings_quality_intangibles_amortization_release_figure",
  "what_changed": "Intangibles amortization on the release income statement is 95 for the quarter against 39 a year earlier, and 185 against 76 for six months. It is excluded from non-GAAP results. The balance sheet prints intangible assets, net, of 2,951 at July 4, 2026 against 3,104 at December 31, 2025.",
  "account": "Intangibles amortization",
  "expected_direction": "none",
  "horizon": "next 10-Q",
  "quote": "| Intangibles amortization | 95 |  |  | 39 |  |",
  "paragraph_id": "0000068505-26-000027:8k_2_02:96" }
```

## Seen in the notes

Nothing is placed under this heading. The split depends on each fact being marked with whether its element sat inside a note. No fact I read in `input_numbers.json` carries that marker, including the note-type facts at the end of the file (goodwill by segment, intangible-asset classes, acquisition fair values). Placing anything here would mean judging, without the marker, which findings came from a note, and the instructions bar that.

For the same reason, every fact item above sits under "Seen in the statements" by default, and I did not itemize the facts in the file's note region. The reader that takes over this split needs the marker restored to `input_numbers.json` before it can re-sort these items.
