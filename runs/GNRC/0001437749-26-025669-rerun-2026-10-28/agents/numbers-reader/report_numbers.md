# GNRC — numbers reader — 10-Q 0001437749-26-025669 (period ending 2026-06-30, filed 2026-08-04)

## What this report is built from

I read all four input files in full:

- **input_trends.json**: the companyfacts record, cutoff 2026-08-04, 14 filings read.
- **input_numbers.json**: XBRL facts from three filings:
  - 10-K 0001437749-26-004568
  - Q1 10-Q 0001437749-26-014882
  - Q2 10-Q 0001437749-26-025669
- **input_8k.md**: 8-K 0001437749-26-024731, item 2.02 earnings release, filed 2026-07-29.
- **input_prior_predictions.md**

**Scope check.** My directory contains no prices, abnormal returns, short interest, other companies' files, prior-run probabilities or outcome window. The `window` block in input_trends.json describes the record window, anchored on the triggering report's period: quarters_end 2026-06-30, years_end 2025-12-31. It is not an outcome window.

**Prior flags.** input_prior_predictions.md says: "None on record."

**Periods the record does not reach.** These periods have no cells, so there is nothing to quote and they have no items:

- **quarters-back-2** (target_end 2025-12-30): "no quarter ending within 20 days of 2025-12-30 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py"
- **quarters-back-6** (target_end 2024-12-31): "no quarter ending within 20 days of 2024-12-31 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py"

The fourth-quarter derivation those reasons name is not in this directory, so this input has no fourth-quarter figure for either year.

**Sections that are not in the input:**

- **Articulation checks:** none in the input, so this report has no articulation-gap items from Python. The differences between filings that I found myself in the facts are the `articulation_and_the_filed_history_*` and intersegment items below.
- **Restatement traces:** none in the input.
- **Fourth-quarter derivation:** none in the input.

**Formula baseline without a paragraph_id.** years-back-0 carries an R&D-capitalisation block. It has values but no `paragraph_id`, so it cannot be quoted and has no item.
- Its `capitalized_development_cost` is missing for this reason: "no row for capitalized_development_cost: the companyfacts record tags none of us-gaap:CapitalizedComputerSoftwareAdditions in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment — the filing says which, and this record cannot".

**Tag changes.** No trend cell says that a period rests on a different concept. Every filled cell uses the same concepts in every period it covers, so there are no tag-change items. The only presentation change I found in the facts is a sign difference in the intersegment elimination between the two 10-Qs (two items below).

**Restated prior values.** I found these places where filings report the same period differently, or report two values for it:
- the 2024-12-31 contract liability (two values in the 10-K, and the trend used one of them);
- the Allmand acquisition payment (the 10-K and the Q1 10-Q differ).

Where a fact carries `superseded_by` and I could see the later filing's value, the value was the same.

**Insufficient metrics.**
- `inventory_reserve_ratio` and `non_gaap_gap` are filled in no period at all.
- `accruals_over_total_assets` is filled in only 2 quarters.

None of the three supports a quarterly trend claim.

## Seen in the statements

### Trend table — quarters-back-0 (2026-04-01..2026-06-30)

```json
{ "id": "earnings_quality_accruals_over_total_assets_trend_quarterly",
  "what_changed": "insufficient. accruals_over_total_assets has no value in quarters-back-0: the record has no discrete operating-cash-flow row for 2026-04-01..2026-06-30. Its quarter-over-quarter and year-over-year changes are not filled ('accruals_over_total_assets is not filled in quarters-back-0'). Only 2 quarters are filled in the whole table: quarters-back-1 (-0.008229900864665223, 'lowest of the 2 filled quarters') and quarters-back-5. Two points do not support a quarterly trend claim. The 8-K states a second-quarter operating cash flow (see across_documents_operating_cash_flow_quarter_in_release_only), but no ratio for this quarter exists in the input and none is derived here.",
  "account": "accruals (NetIncomeLoss - NetCashProvidedByUsedInOperatingActivities) / Assets",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-04-01..2026-06-30: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0001437749-26-025669:trends:accruals_over_total_assets:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_trend_quarterly",
  "what_changed": "Bad-debt reserve ratio is printed as 0.048034698444174795 (allowance 33767000.0 over receivables 669204000.0 plus allowance). Change against quarters-back-1: -0.002404253647686143. Change against quarters-back-4: -0.004855672436630619. It is the lowest of the 6 filled quarters: the allowance is at its thinnest relative to receivables in the filed quarterly history.",
  "account": "AllowanceForDoubtfulAccountsReceivableCurrent / AccountsReceivableNetCurrent",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001437749-26-025669:trends:bad_debt_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_trend_quarterly",
  "what_changed": "Contract liabilities over revenue is printed as 0.10048316588695452 (ContractWithCustomerLiability 117918000.0 over quarterly revenue 1173510000.0). Change against quarters-back-1: -0.02925304401237197. Change against quarters-back-4: 0.07807485957570721. It is the second highest of the 6 filled quarters. It fell from the first quarter, as the contract-liability balance did (see revenue_recognition_contract_liabilities_balance).",
  "account": "ContractWithCustomerLiability / RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"",
  "paragraph_id": "0001437749-26-025669:trends:contract_liabilities_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_trend_quarterly",
  "what_changed": "Days sales of inventory is printed as 172.98977135149818 (InventoryNet 1238871000.0, quarterly cost of goods sold 651699000.0, 91 days). Change against quarters-back-1: -0.567980651570565. Change against quarters-back-4: -4.1091749878457335. It is the third lowest of the 6 filled quarters.",
  "account": "InventoryNet / CostOfGoodsAndServicesSold",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
  "paragraph_id": "0001437749-26-025669:trends:days_sales_of_inventory:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_trend_quarterly",
  "what_changed": "Days sales outstanding is printed as 51.893519441674975 (AccountsReceivableNetCurrent 669204000.0, quarterly revenue 1173510000.0). Change against quarters-back-1: -1.3388980914698791. Change against quarters-back-4: -3.7385014711108226. It is the second lowest of the 6 filled quarters.",
  "account": "AccountsReceivableNetCurrent / RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"position_in_history\": \"second lowest of the 6 filled quarters\"",
  "paragraph_id": "0001437749-26-025669:trends:days_sales_outstanding:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_gross_margin_trend_quarterly",
  "what_changed": "Gross margin is printed as 0.444658332694225. Change against quarters-back-1: 0.0574112554356786. Change against quarters-back-4: 0.05193200917742419. It is the highest of the 6 filled quarters. The 8-K says tariff refunds contributed about 6% to gross margin in the quarter, and calls the refunds recorded during the current year quarter (see across_documents_tariff_refund_gross_margin_contribution). The top-of-history value therefore includes a refund that the company itself ties to this quarter.",
  "account": "gross margin (RevenueFromContractWithCustomerExcludingAssessedTax, CostOfGoodsAndServicesSold)",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001437749-26-025669:trends:gross_margin:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_trend_quarterly",
  "what_changed": "insufficient. inventory_reserve_ratio has no value in quarters-back-0, and none in any quarter or year of the table (0 filled). The cell says us-gaap:InventoryValuationReserves is in the record but not for this period. The 10-K's Schedule II does tag an inventory valuation reserve under a different element (see estimates_and_discretion_inventory_valuation_reserve_balance), but the ratio does not exist in this input and is not derived here.",
  "account": "InventoryValuationReserves / inventory",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"missing\": \"no row for inventory_reserve in 2026-06-30: us-gaap:InventoryValuationReserves is in the record, but not for this period\"",
  "paragraph_id": "0001437749-26-025669:trends:inventory_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_trend_quarterly",
  "what_changed": "insufficient. non_gaap_gap has no value in quarters-back-0, and none in any period of the table: companyfacts holds no non-GAAP measure. The 8-K prints adjusted net income attributable to the Company of $174 million against GAAP net income of $143 million (see earnings_quality_adjusted_net_income_in_release). The gap itself does not exist in this input and is not computed here.",
  "account": "non-GAAP net income against NetIncomeLoss",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001437749-26-025669:trends:non_gaap_gap:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_trend_quarterly",
  "what_changed": "Receivables over revenue is printed as 0.5702584554030217 (receivables 669204000.0 over quarterly revenue 1173510000.0). Change against quarters-back-1: -0.02121285052081001. Change against quarters-back-4: -0.04108243374847065. It is the second lowest of the 6 filled quarters.",
  "account": "AccountsReceivableNetCurrent / RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"position_in_history\": \"second lowest of the 6 filled quarters\"",
  "paragraph_id": "0001437749-26-025669:trends:receivables_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_soft_asset_share_trend_quarterly",
  "what_changed": "Soft-asset share is printed as 0.8046657130071615 (Assets 5772151000.0, PropertyPlantAndEquipmentNet 862578000.0, cash 264921000.0). Change against quarters-back-1: -0.0013233849487186422. Change against quarters-back-4: -0.011568733208239701. It is the lowest of the 6 filled quarters.",
  "account": "(Assets - PropertyPlantAndEquipmentNet - CashAndCashEquivalentsAtCarryingValue) / Assets",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001437749-26-025669:trends:soft_asset_share:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_trend_quarterly",
  "what_changed": "Warranty reserve ratio is printed as 0.11150309754497192 (StandardProductWarrantyAccrual 130850000.0 over quarterly revenue 1173510000.0). Change against quarters-back-1: -0.009658164154253551. Change against quarters-back-4: -0.001526966469336824. It is the second lowest of the 6 filled quarters. In the same quarter, warranties issued are printed at 20286000 against 25826000 a year earlier, while revenue rose (see estimates_and_discretion_warranty_issued_quarter).",
  "account": "StandardProductWarrantyAccrual / RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"position_in_history\": \"second lowest of the 6 filled quarters\"",
  "paragraph_id": "0001437749-26-025669:trends:warranty_reserve_ratio:2026-04-01..2026-06-30" }
```

### Trend table — years-back-0 (2025-01-01..2025-12-31)

For every annual cell the quarter-over-quarter change is not filled, with the printed reason "an annual period has no preceding quarter".

```json
{ "id": "earnings_quality_accruals_over_total_assets_trend_annual",
  "what_changed": "Accruals over total assets for fiscal 2025 is printed as -0.049953361146201636 (net income 159554000.0, operating cash flow 437978000.0, assets 5573679000.0). Change against years-back-1: 0.03322504322806967. It is the third highest of the 5 filled years.",
  "account": "(NetIncomeLoss - NetCashProvidedByUsedInOperatingActivities) / Assets",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001437749-26-025669:trends:accruals_over_total_assets:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_trend_annual",
  "what_changed": "Bad-debt reserve ratio at 2025-12-31 is printed as 0.05414574973754125 (allowance 34504000.0, receivables 602739000.0). Change against years-back-1: -0.0006203612122836349. It is the third highest of the 5 filled years. The 10-K's Schedule II prints a 2025 credit-loss charge of 1398000 against 4524000 in 2024.",
  "account": "AllowanceForDoubtfulAccountsReceivableCurrent / AccountsReceivableNetCurrent",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001437749-26-025669:trends:bad_debt_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_trend_annual",
  "what_changed": "Contract liabilities over revenue for fiscal 2025 is printed as 0.03593530945818713 (ContractWithCustomerLiability 151257000.0 over revenue 4209147000.0). Change against years-back-1: 0.02968320567577841. It is the highest of the 5 filled years. The years-back-1 comparison uses a 2024-12-31 contract liability of 26858000.0 from filing 0001437749-25-033048. The 10-K tags that same date at 97821000 without a scenario member and at 26858000 under PreviousYearMember (see the articulation_and_the_filed_history_contract_liability items). The printed change rests on the lower of the two.",
  "account": "ContractWithCustomerLiability / RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001437749-26-025669:trends:contract_liabilities_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_trend_annual",
  "what_changed": "Days sales of inventory for fiscal 2025 is printed as 175.4965350098752 (InventoryNet 1248867000.0 over cost of goods sold 2597410000.0, 365 days). Change against years-back-1: 31.940283184924482. It is the highest of the 5 filled years. In the same year the 10-K's inventory valuation reserve is printed at 69266000 against 48173000 a year earlier, with 23375000 charged to cost (see the estimates_and_discretion_inventory_valuation_reserve items).",
  "account": "InventoryNet / CostOfGoodsAndServicesSold",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001437749-26-025669:trends:days_sales_of_inventory:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_trend_annual",
  "what_changed": "Days sales outstanding for fiscal 2025 is printed as 52.267059097722175 (receivables 602739000.0 over revenue 4209147000.0). Change against years-back-1: 0.1162632336361753. It is the second highest of the 5 filled years.",
  "account": "AccountsReceivableNetCurrent / RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001437749-26-025669:trends:days_sales_outstanding:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_gross_margin_trend_annual",
  "what_changed": "Gross margin for fiscal 2025 is printed as 0.3829129750041992 (revenue 4209147000.0, cost of goods sold 2597410000.0). Change against years-back-1: -0.0048175564828182305. It is the second highest of the 5 filled years.",
  "account": "gross margin (RevenueFromContractWithCustomerExcludingAssessedTax, CostOfGoodsAndServicesSold)",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001437749-26-025669:trends:gross_margin:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_trend_annual",
  "what_changed": "insufficient. inventory_reserve_ratio has no value in years-back-0, and none in any of the 5 years. The cell says us-gaap:InventoryValuationReserves is in the record but not for 2025-12-31. The 10-K tags the reserve as ValuationAllowancesAndReservesBalance with InventoryValuationReserveMember, a concept this ratio does not read. The ratio does not exist here.",
  "account": "InventoryValuationReserves / inventory",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"missing\": \"no row for inventory_reserve in 2025-12-31: us-gaap:InventoryValuationReserves is in the record, but not for this period\"",
  "paragraph_id": "0001437749-26-025669:trends:inventory_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_trend_annual",
  "what_changed": "insufficient. non_gaap_gap has no value in years-back-0, and none in any year: companyfacts holds no non-GAAP measure. No annual non-GAAP figure is in this input.",
  "account": "non-GAAP net income against NetIncomeLoss",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001437749-26-025669:trends:non_gaap_gap:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_trend_annual",
  "what_changed": "Receivables over revenue for fiscal 2025 is printed as 0.1431974221855402. Change against years-back-1: 0.0007089088956877543. It is the second highest of the 5 filled years.",
  "account": "AccountsReceivableNetCurrent / RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001437749-26-025669:trends:receivables_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_soft_asset_share_trend_annual",
  "what_changed": "Soft-asset share at 2025-12-31 is printed as 0.7927727807790869 (Assets 5573679000.0, cash 341413000.0). Change against years-back-1: -0.017124053072546608. It is the lowest of the 5 filled years.",
  "account": "(Assets - PropertyPlantAndEquipmentNet - CashAndCashEquivalentsAtCarryingValue) / Assets",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001437749-26-025669:trends:soft_asset_share:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_trend_annual",
  "what_changed": "Warranty reserve ratio for fiscal 2025 is printed as 0.03134174216296081. Change against years-back-1: 0.005505781089977079. It is the highest of the 5 filled years. The 10-K prints the standard warranty accrual at 131922000 at 2025-12-31 against 110987000 a year earlier, with 2025 changes to pre-existing warranties of 6794000.",
  "account": "StandardProductWarrantyAccrual / RevenueFromContractWithCustomerExcludingAssessedTax",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001437749-26-025669:trends:warranty_reserve_ratio:2025-01-01..2025-12-31" }
```

### Restated prior values and differences across filings

```json
{ "id": "articulation_and_the_filed_history_contract_liability_opening_balance_as_tagged",
  "what_changed": "The 10-K tags the 2024-12-31 contract liability (excluding extended warranty, no scenario member) at 97821000. The same 10-K also tags 2024-12-31 at 26858000 under a PreviousYearMember scenario. The trend's years-back-1 input is 26858000.0, taken from filing 0001437749-25-033048. The 2025 ratio and its printed year-over-year change therefore rest on one of two values filed for the same date. Which value the company considers the 2024 closing balance is not stated in this input.",
  "account": "ContractWithCustomerLiability (ExcludingExtendedWarrantyMember)",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"value\": \"97821000\"",
  "paragraph_id": "0001437749-26-004568:facts:ContractWithCustomerLiability:2024-12-31:srt:ProductOrServiceAxis=gnrc:ExcludingExtendedWarrantyMember" }
```

```json
{ "id": "articulation_and_the_filed_history_contract_liability_previous_year_scenario",
  "what_changed": "The second 10-K value for the 2024-12-31 contract liability, tagged under StatementScenarioAxis=PreviousYearMember, is 26858000. The trend uses the same figure. The 10-K tags the 2023-12-31 balance under the same scenario at 19173000.",
  "account": "ContractWithCustomerLiability (ExcludingExtendedWarrantyMember, PreviousYearMember)",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"value\": \"26858000\"",
  "paragraph_id": "0001437749-26-004568:facts:ContractWithCustomerLiability:2024-12-31:srt:ProductOrServiceAxis=gnrc:ExcludingExtendedWarrantyMember,srt:StatementScenarioAxis=gnrc:PreviousYearMember" }
```

```json
{ "id": "articulation_and_the_filed_history_contract_liability_value_the_trend_used",
  "what_changed": "The years-back-1 contract_liabilities_over_revenue cell takes its contract-liability input from 0001437749-25-033048 at 26858000.0, not the 97821000 the 10-K tags without a scenario member. The years-back-1 ratio is printed as 0.006252103782408725, 'second lowest of the 5 filled years'.",
  "account": "ContractWithCustomerLiability",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"value\": 26858000.0",
  "paragraph_id": "0001437749-26-025669:trends:contract_liabilities_over_revenue:2024-01-01..2024-12-31" }
```

```json
{ "id": "articulation_and_the_filed_history_allmand_payment_as_first_filed",
  "what_changed": "The 10-K reports the Allmand acquisition, closed 2026-01-05 and disclosed as a subsequent event, with a gross payment of 123201000.",
  "account": "PaymentsToAcquireBusinessesGross (Allmand)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"123201000\"",
  "paragraph_id": "0001437749-26-004568:facts:PaymentsToAcquireBusinessesGross:2026-01-05..2026-01-05:us-gaap:BusinessAcquisitionAxis=gnrc:AllmandMember,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

```json
{ "id": "articulation_and_the_filed_history_allmand_payment_as_refiled",
  "what_changed": "The Q1 10-Q reports the same Allmand payment, for the same 2026-01-05 event date, at 122828000 rather than the 10-K's 123201000. A later filing reports the same event at a different value. The Q1 10-Q prints Allmand goodwill at 34439000 and intangibles at 44300000.",
  "account": "PaymentsToAcquireBusinessesGross (Allmand)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"122828000\"",
  "paragraph_id": "0001437749-26-014882:facts:PaymentsToAcquireBusinessesGross:2026-01-05..2026-01-05:us-gaap:BusinessAcquisitionAxis=gnrc:AllmandMember" }
```

```json
{ "id": "structure_and_disclosure_changes_intersegment_elimination_sign_in_first_quarter_filing",
  "what_changed": "In the Q1 10-Q, the intersegment-elimination revenue member carries positive values: 2916000 for 2026-01-01..2026-03-31 and 5548000 for 2025-01-01..2025-03-31. The Q2 10-Q tags the same member with negative values (next item). The sign convention for this member differs between the two filings.",
  "account": "RevenueFromContractWithCustomerExcludingAssessedTax (IntersegmentEliminationMember)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"2916000\"",
  "paragraph_id": "0001437749-26-014882:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-01-01..2026-03-31:srt:ConsolidationItemsAxis=us-gaap:IntersegmentEliminationMember" }
```

```json
{ "id": "structure_and_disclosure_changes_intersegment_elimination_sign_in_second_quarter_filing",
  "what_changed": "In the Q2 10-Q, the intersegment-elimination revenue member is tagged negative: -4243000 for 2026-04-01..2026-06-30 and -7159000 for 2026-01-01..2026-06-30. The Q1 10-Q tagged the member positive. Anything that sums segment rows across the two filings would treat the eliminations with opposite signs.",
  "account": "RevenueFromContractWithCustomerExcludingAssessedTax (IntersegmentEliminationMember)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"-4243000\"",
  "paragraph_id": "0001437749-26-025669:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:ConsolidationItemsAxis=us-gaap:IntersegmentEliminationMember" }
```

### Earnings release (8-K 0001437749-26-024731) against the filed numbers

```json
{ "id": "across_documents_tariff_refund_gross_margin_contribution",
  "what_changed": "The release attributes about 6% of second-quarter gross margin to tariff refunds. The 10-Q gross profit is printed at 521811000 against 416749000 a year earlier, and the trend gross margin is at the top of its 6-quarter history. The release ties the refund to this quarter.",
  "account": "gross margin / tariff refunds",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "The increase was primarily driven by tariff refunds which contributed approximately 6% to gross margin during the quarter.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:22" }
```

```json
{ "id": "across_documents_tariff_refund_pretax_impact",
  "what_changed": "The release says GAAP net income, adjusted net income and adjusted EBITDA all include about $71 million of pre-tax tariff refunds, recorded during the quarter. The 10-Q facts I read contain no separately tagged tariff-refund element, so the refund amount exists only in the release.",
  "account": "net income / tariff refunds",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "Net income, adjusted net income, and adjusted EBITDA all include a pre-tax impact of approximately $71 million related to tariff refunds that were recorded during the current year quarter.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:14" }
```

```json
{ "id": "across_documents_tariff_refund_residential_margin",
  "what_changed": "In the Residential segment, the release attributes about 9% of adjusted-EBITDA margin to tariff refunds. Segment adjusted EBITDA is stated as $215.4 million (34.7%) against $146.4 million (23.1%).",
  "account": "Residential segment adjusted EBITDA",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "This increase was primarily driven by tariff refunds which impacted margins by approximately 9%, as well as favorable sales mix and operational efficiencies resulting in lower operating expenses.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:32" }
```

```json
{ "id": "across_documents_tariff_refund_commercial_industrial_margin",
  "what_changed": "In C&I, the release attributes about 2% of adjusted-EBITDA margin to tariff refunds, offset by unfavorable mix and investment spending. C&I adjusted EBITDA is stated as $81.5 million (14.6%) against $53.3 million (12.4%).",
  "account": "C&I segment adjusted EBITDA",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "This margin increase was primarily driven by an impact from tariff refunds of approximately 2%, as well as the favorable impact of acquisitions/divestitures and improved operating leverage, offset by an unfavorable sales mix shift and strategic operating expense investments to support future growth.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:29" }
```

```json
{ "id": "across_documents_free_cash_flow_tariff_receipts",
  "what_changed": "The release attributes the quarter's free-cash-flow increase partly to cash receipts from tariff refunds. The cash-flow benefit, like the margin benefit, rests on the refund.",
  "account": "free cash flow / operating cash flow",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "This strong increase in free cash flow during the quarter was primarily driven by higher operating earnings, including cash receipts from tariff refunds.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:25" }
```

```json
{ "id": "across_documents_operating_cash_flow_quarter_in_release_only",
  "what_changed": "The release states a second-quarter operating cash flow of $121.2 million. The XBRL record holds only the six-month figure (240496000) and the Q1 10-Q's first-quarter figure (119285000). This is why the trend's quarterly accruals cell is missing. The quarterly figure exists in the release text only; no quarterly accrual ratio exists in this input.",
  "account": "NetCashProvidedByUsedInOperatingActivities",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "Cash flow from operations was $121.2 million during the second quarter, as compared to $72.2 million in the prior year.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:25" }
```

```json
{ "id": "earnings_quality_adjusted_net_income_in_release",
  "what_changed": "The release gives adjusted net income attributable to the Company of $174 million ($2.91 per share), against GAAP net income of $143 million ($2.40 diluted). The release says both include the tariff refund. The trend's non_gaap_gap is not filled, and no gap is computed here.",
  "account": "adjusted net income (non-GAAP)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "Adjusted net income attributable to the Company, as defined in the accompanying reconciliation schedules, was $174 million, or $2.91 per share, as compared to $97 million, or $1.65 per share, in the second quarter of 2025.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:12" }
```

```json
{ "id": "earnings_quality_adjusted_ebitda_in_release",
  "what_changed": "Adjusted EBITDA is stated as $291 million (24.8% of net sales) against $188 million (17.7%). The release says the figure includes the roughly $71 million tariff refund.",
  "account": "adjusted EBITDA (non-GAAP)",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "Adjusted EBITDA before deducting for noncontrolling interests, as defined in the accompanying reconciliation schedules, was $291 million, or 24.8% of net sales, as compared to $188 million, or 17.7% of net sales, in the prior year.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:13" }
```

```json
{ "id": "results_against_expectations_adjusted_ebitda_margin_guidance",
  "what_changed": "Full-year 2026 adjusted EBITDA margin guidance is raised to about 20.0 to 21.0% from 18.5 to 19.5%. The release says the new range reflects about 1.5% from tariff refunds. Net sales growth guidance is held at the mid-to-high teens.",
  "account": "adjusted EBITDA margin guidance",
  "expected_direction": "none",
  "horizon": "fiscal 2026",
  "quote": "Adjusted EBITDA margin, before deducting for non-controlling interests, is now expected to be approximately 20.0 to 21.0%, reflecting an approximate 1.5% impact from tariff refunds for the full year 2026.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:19" }
```

```json
{ "id": "results_against_expectations_guidance_raise_rests_on_tariff_refund",
  "what_changed": "The release says the raised outlook is primarily due to the second-quarter tariff refund. The guidance increase rests mainly on that refund, not on a change in the operating outlook.",
  "account": "full-year 2026 outlook",
  "expected_direction": "none",
  "horizon": "fiscal 2026",
  "quote": "This increased outlook is primarily due to the tariff refund included in the second quarter, which is expected to have an approximate 1.5% impact for the full year 2026.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:36" }
```

```json
{ "id": "results_against_expectations_net_income_margin_guidance",
  "what_changed": "Full-year 2026 net income margin guidance is raised to about 9.0 to 10.0% from 8.0 to 9.0%.",
  "account": "net income margin guidance",
  "expected_direction": "none",
  "horizon": "fiscal 2026",
  "quote": "Additionally, the Company now expects net income margin, before deducting for non-controlling interests, to be approximately 9.0 to 10.0% for the full-year 2026, as compared to the previous guidance of 8.0 to 9.0%.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:36" }
```

```json
{ "id": "results_against_expectations_segment_sales_outlook",
  "what_changed": "The segment outlook changes: C&I is now expected to grow in the low 30% range, and Residential is now projected to grow in the high single digits. Total growth guidance is unchanged. Second-quarter Residential total sales were 621263000 against 634718000 a year earlier, so the full-year Residential projection depends on the second half.",
  "account": "segment sales outlook",
  "expected_direction": "none",
  "horizon": "fiscal 2026",
  "quote": "C&I segment sales are now expected to grow in the low 30% range during the year as a result of continued significant momentum in the data center market, and Residential segment sales are now projected to increase in the high-single digit range from the prior year.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:35" }
```

```json
{ "id": "earnings_quality_effective_tax_rate_prior_year_discrete_item",
  "what_changed": "The release gives a quarterly effective tax rate of 24.6% against 17.2%. It attributes the difference to a favorable discrete item in the prior-year quarter that did not repeat.",
  "account": "IncomeTaxExpenseBenefit / effective tax rate",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "The increase in the effective tax rate was primarily related to a non-recurring favorable discrete item in the prior year period that did not repeat in the current year.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:24" }
```

```json
{ "id": "across_documents_data_center_backlog_outside_remaining_obligations",
  "what_changed": "The release says data-center backlog has risen to about $1.6 billion. The 10-Q's remaining performance obligations excluding extended warranties are printed at 143000000 at 2026-06-30, against 272000000 at 2026-03-31 in the Q1 10-Q. The backlog the release cites is not reflected in the tagged RPO. The release's risk factors list cancellation rights in data-center contracts (see narrative_signs_of_operating_pressure_data_center_contract_terms).",
  "account": "RevenueRemainingPerformanceObligation / backlog",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "In total, our backlog for products serving the data center market has now increased to approximately $1.6 billion as of today, which does not include any committed volumes from the second hyperscale customer.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:20" }
```

```json
{ "id": "across_documents_hyperscale_committed_volume",
  "what_changed": "The release says product-specific terms under the first hyperscale agreement committed nearly $700 million of volume for 2027. No XBRL fact in this input carries that commitment.",
  "account": "data center supply agreement",
  "expected_direction": "none",
  "horizon": "fiscal 2027",
  "quote": "In addition, product specific terms related to this agreement were recently finalized, which committed nearly $700 million of volume for 2027.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:16" }
```

```json
{ "id": "across_documents_second_hyperscale_terms_pending",
  "what_changed": "The release says the second hyperscale agreement's product-specific terms for 2027 and 2028 are still being negotiated.",
  "account": "data center supply agreement",
  "expected_direction": "none",
  "horizon": "fiscal 2027",
  "quote": "On June 24th, the Company secured a global supply agreement with a second hyperscale customer and is currently negotiating final product specific terms for 2027 and 2028 volumes.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:17" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_data_center_contract_terms",
  "what_changed": "The release's forward-looking factors name contract risk with data-center customers: cancellation rights, delivery requirements, and liability tied to performance obligations.",
  "account": "data center contracts",
  "expected_direction": "none",
  "horizon": "fiscal 2027",
  "quote": "increase in contract risk related to terms with certain data center customers, including cancellation rights, delivery requirements, and potential liability exposure tied to our performance obligations or other claimed damages;",
  "paragraph_id": "0001437749-26-024731:8k_2_02:59" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_residential_sales_decline",
  "what_changed": "Residential total sales fell, which the release attributes to lower energy-storage and portable-generator shipments. Residential operating-segment revenue is printed at 621263000 against 634718000.",
  "account": "Residential segment revenue",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "This modest sales decrease was primarily driven by lower energy storage system and portable generator shipments compared to the prior year, mostly offset by growth in home standby generator sales.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:31" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_industrial_distributor_channel",
  "what_changed": "Within C&I, the release says shipments to the domestic industrial distributor channel fell by more than rental and telecom gains.",
  "account": "C&I segment revenue",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "In addition, increased shipments to rental and telecom channel customers were more than offset by a decrease in shipments to the domestic industrial distributor channel.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:28" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_mix_and_input_costs",
  "what_changed": "Outside the tariff refund, the release says unfavorable mix and higher input costs were only partly offset by price.",
  "account": "gross margin",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "Additionally, unfavorable sales mix and higher input costs were partially offset by favorable price realization.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:22" }
```

```json
{ "id": "earnings_quality_lower_legal_expenses",
  "what_changed": "Operating expenses rose $6.4 million, which the release says was partly offset by lower legal expenses. The release's legal reconciliation shows a net credit for the quarter (see related_parties_contingencies_and_subsequent_events_patent_lawsuit_credit). General and administrative expense is printed at 73155000 against 79430000.",
  "account": "operating expenses / legal expense",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "partially offset by lower legal expenses in the current year",
  "paragraph_id": "0001437749-26-024731:8k_2_02:23" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_patent_lawsuit_credit",
  "what_changed": "In the release's reconciliation of legal and regulatory items, the patent-lawsuit line is printed as (3,485) for the quarter against 1,696 a year earlier, a credit. The quarter's total provision for legal, regulatory and other matters is printed as (951) against 4,911.",
  "account": "provision for legal, regulatory and other costs",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "Legal expenses, judgements and settlements related to certain patent lawsuits",
  "paragraph_id": "0001437749-26-024731:8k_2_02:126" }
```

```json
{ "id": "estimates_and_discretion_clean_energy_warranty_release",
  "what_changed": "The release's legal-and-other reconciliation shows a release of a warranty provision recorded in 2022 for clean-energy warranty matters: (1,129) for the six months of 2026 and nothing in the second quarter. A prior-period estimate was reversed this year. The 10-Q's quarterly warranty rollforward prints changes to pre-existing warranties of 2582000 and 1250000 for the first quarter (separate items).",
  "account": "warranty provision (clean energy)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "Release of warranty provision recorded in 2022 to address clean energy warranty-related matters",
  "paragraph_id": "0001437749-26-024731:8k_2_02:126" }
```

```json
{ "id": "structure_and_disclosure_changes_acquisitions_divestitures_sales_contribution",
  "what_changed": "The release says acquisitions, divestitures and currency added a net 2% to second-quarter sales growth. For C&I it says about 6%.",
  "account": "net sales",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "Acquisitions, divestitures and foreign currency had a net favorable impact of 2% to sales growth during the quarter.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:8" }
```

```json
{ "id": "structure_and_disclosure_changes_enercon_and_facility_in_release",
  "what_changed": "The release says the Enercon acquisition closed during the quarter and an additional facility was acquired.",
  "account": "business combinations",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "During the quarter, the Company completed the previously disclosed acquisition of Enercon, headquartered in East Peoria, Illinois, and acquired an additional facility in Belvidere, Illinois, significantly expanding capacity for large megawatt generator packaging.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:18" }
```

```json
{ "id": "structure_and_disclosure_changes_business_dispositions_in_release",
  "what_changed": "The release attributes the year's disposition loss to four immaterial business dispositions, two in each quarter of 2026. The 10-Q disposition loss is printed at -13456000 for the quarter and -18238000 for the six months.",
  "account": "GainLossOnSaleOfBusiness",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "The current year loss relates primarily to four immaterial business dispositions with two closing in the first quarter and two closing in the second quarter of 2026.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:129" }
```

### Numeric facts — income statement, tax and cash flow

```json
{ "id": "earnings_quality_gross_profit_quarter",
  "what_changed": "Second-quarter 2026 gross profit is printed as 521811000, against 416749000 for the second quarter of 2025. Revenue is printed as 1173510000 against 1061169000.",
  "account": "GrossProfit",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "\"value\": \"521811000\"",
  "paragraph_id": "0001437749-26-025669:facts:GrossProfit:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_operating_income_quarter",
  "what_changed": "Second-quarter 2026 operating income is printed as 210433000, against 111789000 a year earlier. The release attributes most of the margin change to tariff refunds.",
  "account": "OperatingIncomeLoss",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "\"value\": \"210433000\"",
  "paragraph_id": "0001437749-26-025669:facts:OperatingIncomeLoss:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_net_income_quarter",
  "what_changed": "Second-quarter 2026 net income attributable to Generac is printed as 143244000, against 74016000 a year earlier. Six-month net income is printed as 216497000.",
  "account": "NetIncomeLoss",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "\"value\": \"143244000\"",
  "paragraph_id": "0001437749-26-025669:facts:NetIncomeLoss:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_diluted_earnings_per_share_quarter",
  "what_changed": "Second-quarter 2026 diluted EPS is printed as 2.4, against 1.25 a year earlier.",
  "account": "EarningsPerShareDiluted",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "\"value\": \"2.4\"",
  "paragraph_id": "0001437749-26-025669:facts:EarningsPerShareDiluted:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_income_tax_expense_quarter",
  "what_changed": "Second-quarter 2026 income tax expense is printed as 46696000, against 15422000 a year earlier. Pretax income is printed as 189706000 against 89852000.",
  "account": "IncomeTaxExpenseBenefit",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"46696000\"",
  "paragraph_id": "0001437749-26-025669:facts:IncomeTaxExpenseBenefit:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_effective_tax_rate_year_to_date",
  "what_changed": "The six-month 2026 effective tax rate is printed as 0.246, against 0.20 for the six months of 2025. The Q1 10-Q printed 0.244 for the first quarter. The 10-K prints 0.189 for 2025, 0.226 for 2024 and 0.252 for 2023.",
  "account": "EffectiveIncomeTaxRateContinuingOperations",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"0.246\"",
  "paragraph_id": "0001437749-26-025669:facts:EffectiveIncomeTaxRateContinuingOperations:2026-01-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_operating_cash_flow_year_to_date",
  "what_changed": "Six-month 2026 operating cash flow is printed as 240496000, against 130341000 for the six months of 2025. The record has no discrete second-quarter figure, which is why quarterly accruals are insufficient.",
  "account": "NetCashProvidedByUsedInOperatingActivities",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"240496000\"",
  "paragraph_id": "0001437749-26-025669:facts:NetCashProvidedByUsedInOperatingActivities:2026-01-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_operating_cash_flow_first_quarter",
  "what_changed": "First-quarter 2026 operating cash flow, from the Q1 10-Q, is printed as 119285000. It is the input to the only filled recent accruals cell (quarters-back-1).",
  "account": "NetCashProvidedByUsedInOperatingActivities",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"119285000\"",
  "paragraph_id": "0001437749-26-014882:facts:NetCashProvidedByUsedInOperatingActivities:2026-01-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_other_accrued_liabilities_cash_flow_change",
  "what_changed": "The six-month 2026 change in other accrued liabilities is printed as -110996000, against -18798000 in the release for the six months of 2025. Over the same six months, payments on the Zawaski litigation accrual are printed at 206500000 (see related_parties_contingencies_and_subsequent_events_zawaski_accrual_paid).",
  "account": "IncreaseDecreaseInOtherAccruedLiabilities",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"-110996000\"",
  "paragraph_id": "0001437749-26-025669:facts:IncreaseDecreaseInOtherAccruedLiabilities:2026-01-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_other_operating_assets_cash_flow_change",
  "what_changed": "The six-month 2026 change in other operating assets is printed as 105336000, shown in the release's cash-flow statement as a (105,336) use of cash against 7,990 a year earlier.",
  "account": "IncreaseDecreaseInOtherOperatingAssets",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"105336000\"",
  "paragraph_id": "0001437749-26-025669:facts:IncreaseDecreaseInOtherOperatingAssets:2026-01-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_deferred_tax_asset_balance",
  "what_changed": "The net deferred income tax asset is printed as 8107000 at 2026-06-30, against 41949000 at 2025-12-31. The release's cash-flow statement shows deferred income tax expense of 26,447 for the six months, against a benefit of (18,668) a year earlier.",
  "account": "DeferredIncomeTaxAssetsNet",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"8107000\"",
  "paragraph_id": "0001437749-26-025669:facts:DeferredIncomeTaxAssetsNet:2026-06-30" }
```

```json
{ "id": "earnings_quality_investment_fair_value_gain",
  "what_changed": "The six-month 2026 unrealized gain on investments is printed as 4542000, against -11471000 for the six months of 2025. The release identifies it as fair-value changes on the Wallbox N.V. warrants and equity and excludes it from adjusted figures.",
  "account": "UnrealizedGainLossOnInvestments",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"4542000\"",
  "paragraph_id": "0001437749-26-025669:facts:UnrealizedGainLossOnInvestments:2026-01-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_depreciation_and_amortization_year_to_date",
  "what_changed": "Six-month 2026 depreciation and amortization is printed as 114384000, against 94462000 for the six months of 2025.",
  "account": "DepreciationDepletionAndAmortization",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"114384000\"",
  "paragraph_id": "0001437749-26-025669:facts:DepreciationDepletionAndAmortization:2026-01-01..2026-06-30" }
```

### Numeric facts — contingencies

```json
{ "id": "related_parties_contingencies_and_subsequent_events_zawaski_accrual_year_end",
  "what_changed": "The 10-K carries a loss-contingency accrual of 206500000 for Zawaski et al. v. Generac Power Systems at 2025-12-31, within other accrued liabilities.",
  "account": "LossContingencyAccrualAtCarryingValue (Zawaski)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"206500000\"",
  "paragraph_id": "0001437749-26-004568:facts:LossContingencyAccrualAtCarryingValue:2025-12-31:srt:LitigationCaseAxis=gnrc:ZawaskiEtAlVGeneralPowerSystemsIncEtAlMember,us-gaap:BalanceSheetLocationAxis=gnrc:OtherAccruedLiabilitiesMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_zawaski_insurance_receivable_year_end",
  "what_changed": "The 10-K carries an insurance settlement receivable of 102000000 for the Zawaski case at 2025-12-31, within prepaid expenses and other current assets.",
  "account": "InsuranceSettlementsReceivable (Zawaski)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"102000000\"",
  "paragraph_id": "0001437749-26-004568:facts:InsuranceSettlementsReceivable:2025-12-31:srt:LitigationCaseAxis=gnrc:ZawaskiEtAlVGeneralPowerSystemsIncEtAlMember,us-gaap:BalanceSheetLocationAxis=us-gaap:PrepaidExpensesAndOtherCurrentAssetsMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_zawaski_accrual_first_quarter_end",
  "what_changed": "The Q2 10-Q still prints the Zawaski accrual at 206500000 at 2026-03-31. No 2026-06-30 accrual balance for this case appears in the facts.",
  "account": "LossContingencyAccrualAtCarryingValue (Zawaski)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"206500000\"",
  "paragraph_id": "0001437749-26-025669:facts:LossContingencyAccrualAtCarryingValue:2026-03-31:srt:LitigationCaseAxis=gnrc:ZawaskiEtAlVGeneralPowerSystemsIncEtAlMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_zawaski_insurance_receivable_first_quarter_end",
  "what_changed": "The Q2 10-Q prints the Zawaski insurance receivable at 102000000 at 2026-03-31. No 2026-06-30 receivable balance for this case appears in the facts, so whether it was collected does not exist in this input.",
  "account": "InsuranceSettlementsReceivable (Zawaski)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"102000000\"",
  "paragraph_id": "0001437749-26-025669:facts:InsuranceSettlementsReceivable:2026-03-31:srt:LitigationCaseAxis=gnrc:ZawaskiEtAlVGeneralPowerSystemsIncEtAlMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_zawaski_accrual_paid",
  "what_changed": "Payments against the Zawaski accrual are printed at 206500000 for 2026-01-01..2026-06-30. That equals the full accrual, which was still printed at 2026-03-31. Other accrued liabilities are printed at 447770000 at 2026-06-30 against 591387000 at 2025-12-31.",
  "account": "LossContingencyAccrualPayments (Zawaski)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"206500000\"",
  "paragraph_id": "0001437749-26-025669:facts:LossContingencyAccrualPayments:2026-01-01..2026-06-30:srt:LitigationCaseAxis=gnrc:ZawaskiEtAlVGeneralPowerSystemsIncEtAlMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_portable_generator_legal_charge",
  "what_changed": "The 10-K tags a fourth-quarter 2025 legal charge of 104500000 for the portable-generator product-liability case.",
  "account": "LegalFees (portable generator product liability)",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"value\": \"104500000\"",
  "paragraph_id": "0001437749-26-004568:facts:LegalFees:2025-10-01..2025-12-31:srt:LitigationCaseAxis=gnrc:PortableGeneratorProductLiabilityCaseMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_powerhome_solar_damages_sought",
  "what_changed": "The Q2 10-Q still carries the PowerHome Solar claim against Generac Power Systems, with minimum damages sought of 25000000.",
  "account": "LossContingencyDamagesSoughtValue (PowerHome Solar)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"25000000\"",
  "paragraph_id": "0001437749-26-025669:facts:LossContingencyDamagesSoughtValue:2022-08-01..2022-08-01:srt:LitigationCaseAxis=gnrc:PowerHomeSolarLlcAgainstGeneracPowerSystemsIncMember,srt:RangeAxis=srt:MinimumMember" }
```

### Numeric facts — warranty, inventory and reserves

```json
{ "id": "estimates_and_discretion_warranty_issued_quarter",
  "what_changed": "Standard warranties issued in the second quarter of 2026 are printed as 20286000, against 25826000 a year earlier, while quarterly revenue is printed at 1173510000 against 1061169000. Six-month issued warranties are printed at 39315000 against 43944000. New accruals are lower while sales are higher.",
  "account": "StandardProductWarrantyAccrualWarrantiesIssued",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"20286000\"",
  "paragraph_id": "0001437749-26-025669:facts:StandardProductWarrantyAccrualWarrantiesIssued:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_payments_quarter",
  "what_changed": "Standard warranty payments in the second quarter of 2026 are printed as 20454000, against 18868000 a year earlier. Six-month payments are printed at 44430000 against 39755000.",
  "account": "StandardProductWarrantyAccrualPayments",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"20454000\"",
  "paragraph_id": "0001437749-26-025669:facts:StandardProductWarrantyAccrualPayments:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_preexisting_adjustment_quarter",
  "what_changed": "Changes in estimate for pre-existing standard warranties in the second quarter of 2026 are printed as 2582000, against 2269000 a year earlier. Six-month figures: 3832000 against 4768000. Additions from acquisitions: 82000 for the quarter, 211000 for the six months.",
  "account": "StandardProductWarrantyAccrualPreexistingIncreaseDecrease",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"2582000\"",
  "paragraph_id": "0001437749-26-025669:facts:StandardProductWarrantyAccrualPreexistingIncreaseDecrease:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_preexisting_adjustment_first_quarter",
  "what_changed": "The Q1 10-Q prints first-quarter 2026 changes in estimate for pre-existing warranties as 1250000. The 10-K printed 6794000 for 2025.",
  "account": "StandardProductWarrantyAccrualPreexistingIncreaseDecrease",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"1250000\"",
  "paragraph_id": "0001437749-26-014882:facts:StandardProductWarrantyAccrualPreexistingIncreaseDecrease:2026-01-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_standard_warranty_accrual_balance",
  "what_changed": "The standard warranty accrual is printed as 130850000 at 2026-06-30. Earlier balances: 128354000 at 2026-03-31, 131922000 at 2025-12-31 and 119944000 at 2025-06-30. Current portion: 43473000 against 44716000 at 2025-12-31.",
  "account": "StandardProductWarrantyAccrual",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"130850000\"",
  "paragraph_id": "0001437749-26-025669:facts:StandardProductWarrantyAccrual:2026-06-30" }
```

```json
{ "id": "revenue_recognition_extended_warranty_deferred_balance",
  "what_changed": "The extended warranty balance is printed as 232924000 at 2026-06-30. Earlier balances: 226631000 at 2026-03-31, 219404000 at 2025-12-31 and 202650000 at 2025-06-30. Extended warranties issued in the second quarter: 16253000, against 16915000 a year earlier.",
  "account": "ExtendedProductWarrantyAccrual",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"232924000\"",
  "paragraph_id": "0001437749-26-025669:facts:ExtendedProductWarrantyAccrual:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_valuation_reserve_balance",
  "what_changed": "The 10-K's Schedule II prints the inventory valuation reserve at 69266000 at 2025-12-31. Prior balances: 48173000 at 2024-12-31, 39027000 at 2023-12-31 and 39714000 at 2022-12-31. The trend's inventory_reserve_ratio does not read this element and is unfilled. No 2026 quarter-end reserve balance appears in the facts.",
  "account": "ValuationAllowancesAndReservesBalance (InventoryValuationReserveMember)",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"value\": \"69266000\"",
  "paragraph_id": "0001437749-26-004568:facts:ValuationAllowancesAndReservesBalance:2025-12-31:us-gaap:ValuationAllowancesAndReservesTypeAxis=us-gaap:InventoryValuationReserveMember" }
```

```json
{ "id": "estimates_and_discretion_inventory_valuation_reserve_prior_balance",
  "what_changed": "The 10-K's Schedule II prints the inventory valuation reserve at 48173000 at 2024-12-31, the opening balance for the 69266000 at 2025-12-31.",
  "account": "ValuationAllowancesAndReservesBalance (InventoryValuationReserveMember)",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"value\": \"48173000\"",
  "paragraph_id": "0001437749-26-004568:facts:ValuationAllowancesAndReservesBalance:2024-12-31:us-gaap:ValuationAllowancesAndReservesTypeAxis=us-gaap:InventoryValuationReserveMember" }
```

```json
{ "id": "estimates_and_discretion_inventory_valuation_reserve_charges",
  "what_changed": "The 10-K's Schedule II prints 2025 inventory reserve charges to cost of 23375000, against 10738000 in 2024 and 4621000 in 2023. Fiscal 2025 days sales of inventory is the highest of 5 filled years.",
  "account": "ValuationAllowancesAndReservesChargedToCostAndExpense (InventoryValuationReserveMember)",
  "expected_direction": "none",
  "horizon": "next annual report",
  "quote": "\"value\": \"23375000\"",
  "paragraph_id": "0001437749-26-004568:facts:ValuationAllowancesAndReservesChargedToCostAndExpense:2025-01-01..2025-12-31:us-gaap:ValuationAllowancesAndReservesTypeAxis=us-gaap:InventoryValuationReserveMember" }
```

```json
{ "id": "earnings_quality_finished_goods_inventory",
  "what_changed": "Finished goods inventory, net of reserves, is printed as 562786000 at 2026-06-30, against 530665000 at 2025-12-31. Total InventoryNet is printed at 1238871000 against 1248867000.",
  "account": "InventoryFinishedGoodsNetOfReserves",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"562786000\"",
  "paragraph_id": "0001437749-26-025669:facts:InventoryFinishedGoodsNetOfReserves:2026-06-30" }
```

```json
{ "id": "earnings_quality_raw_materials_inventory",
  "what_changed": "Raw materials inventory, net of reserves, is printed as 663614000 at 2026-06-30, against 705610000 at 2025-12-31. Work in process: 12471000 against 12592000.",
  "account": "InventoryRawMaterialsNetOfReserves",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"663614000\"",
  "paragraph_id": "0001437749-26-025669:facts:InventoryRawMaterialsNetOfReserves:2026-06-30" }
```

### Numeric facts — revenue recognition

```json
{ "id": "revenue_recognition_contract_assets_balance",
  "what_changed": "The net contract asset is printed as 78730000 at 2026-06-30, against 8867000 at 2025-12-31. Over the same six months, contract liabilities are printed lower and RPO excluding extended warranties is printed lower. More revenue is now recognized ahead of billing.",
  "account": "ContractWithCustomerAssetNet",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"78730000\"",
  "paragraph_id": "0001437749-26-025669:facts:ContractWithCustomerAssetNet:2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_balance",
  "what_changed": "The contract liability is printed as 117918000 at 2026-06-30, against 151257000 at 2025-12-31 in the same filing. The Q1 10-Q printed 137438000 at 2026-03-31.",
  "account": "ContractWithCustomerLiability",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"117918000\"",
  "paragraph_id": "0001437749-26-025669:facts:ContractWithCustomerLiability:2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_first_quarter_balance",
  "what_changed": "The Q1 10-Q prints the contract liability at 137438000 at 2026-03-31. It is the quarters-back-1 input behind the printed quarter-over-quarter change of -0.02925304401237197.",
  "account": "ContractWithCustomerLiability",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"137438000\"",
  "paragraph_id": "0001437749-26-014882:facts:ContractWithCustomerLiability:2026-03-31" }
```

```json
{ "id": "revenue_recognition_contract_liability_revenue_recognized_year_to_date",
  "what_changed": "Revenue recognized from the opening contract liability is printed as 90360000 for the six months of 2026. The 10-K printed 61299000 for all of 2025 and 19173000 for 2024.",
  "account": "ContractWithCustomerLiabilityRevenueRecognized",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"90360000\"",
  "paragraph_id": "0001437749-26-025669:facts:ContractWithCustomerLiabilityRevenueRecognized:2026-01-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liability_revenue_recognized_first_quarter",
  "what_changed": "The Q1 10-Q prints revenue recognized from the opening contract liability as 46832000 for the first quarter of 2026.",
  "account": "ContractWithCustomerLiabilityRevenueRecognized",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"46832000\"",
  "paragraph_id": "0001437749-26-014882:facts:ContractWithCustomerLiabilityRevenueRecognized:2026-01-01..2026-03-31" }
```

```json
{ "id": "revenue_recognition_remaining_performance_obligations_balance",
  "what_changed": "Remaining performance obligations excluding extended warranties are printed as 143000000 at 2026-06-30 (decimals -6). The tagged share expected within twelve months is 0.80. The Q1 10-Q printed 272000000 at 2026-03-31, and the 10-K printed 378782000 at 2025-12-31. The release, meanwhile, cites a rising data-center backlog.",
  "account": "RevenueRemainingPerformanceObligation (ExcludingExtendedWarrantiesMember)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"143000000\"",
  "paragraph_id": "0001437749-26-025669:facts:RevenueRemainingPerformanceObligation:2026-06-30:srt:ProductOrServiceAxis=gnrc:ExcludingExtendedWarrantiesMember" }
```

```json
{ "id": "revenue_recognition_remaining_performance_obligations_first_quarter_balance",
  "what_changed": "The Q1 10-Q prints remaining performance obligations excluding extended warranties at 272000000 at 2026-03-31.",
  "account": "RevenueRemainingPerformanceObligation (ExcludingExtendedWarrantiesMember)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"272000000\"",
  "paragraph_id": "0001437749-26-014882:facts:RevenueRemainingPerformanceObligation:2026-03-31:srt:ProductOrServiceAxis=gnrc:ExcludingExtendedWarrantiesMember" }
```

### Numeric facts — segments, acquisitions and dispositions

```json
{ "id": "structure_and_disclosure_changes_residential_segment_sales",
  "what_changed": "Residential operating-segment revenue for the second quarter of 2026 is printed as 621263000, against 634718000 a year earlier.",
  "account": "RevenueFromContractWithCustomerExcludingAssessedTax (ResidentialSegmentMember)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"621263000\"",
  "paragraph_id": "0001437749-26-025669:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=gnrc:ResidentialSegmentMember" }
```

```json
{ "id": "structure_and_disclosure_changes_commercial_industrial_segment_sales",
  "what_changed": "C&I operating-segment revenue for the second quarter of 2026 is printed as 556490000, against 430575000 a year earlier. The release says acquisitions, divestitures and currency contributed about 6% of C&I growth.",
  "account": "RevenueFromContractWithCustomerExcludingAssessedTax (CommercialAndIndustrialSegmentMember)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"556490000\"",
  "paragraph_id": "0001437749-26-025669:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-04-01..2026-06-30:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=gnrc:CommercialAndIndustrialSegmentMember" }
```

```json
{ "id": "structure_and_disclosure_changes_residential_segment_assets",
  "what_changed": "Residential segment assets are printed as 2905028000 at 2026-06-30, against 3144332000 at 2025-12-31.",
  "account": "Assets (ResidentialSegmentMember)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"2905028000\"",
  "paragraph_id": "0001437749-26-025669:facts:Assets:2026-06-30:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=gnrc:ResidentialSegmentMember" }
```

```json
{ "id": "structure_and_disclosure_changes_commercial_industrial_segment_assets",
  "what_changed": "C&I segment assets are printed as 2808887000 at 2026-06-30, against 2367764000 at 2025-12-31.",
  "account": "Assets (CommercialAndIndustrialSegmentMember)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"2808887000\"",
  "paragraph_id": "0001437749-26-025669:facts:Assets:2026-06-30:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=gnrc:CommercialAndIndustrialSegmentMember" }
```

```json
{ "id": "structure_and_disclosure_changes_united_states_revenue_share",
  "what_changed": "The United States share of revenue in the second quarter of 2026 is printed as 0.76, against 0.80 a year earlier. Six-month figures: 0.77 against 0.79.",
  "account": "ConcentrationRiskPercentage1 (US, revenue)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"0.76\"",
  "paragraph_id": "0001437749-26-025669:facts:ConcentrationRiskPercentage1:2026-04-01..2026-06-30:srt:StatementGeographicalAxis=country:US,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:SalesRevenueNetMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:GeographicConcentrationRiskMember" }
```

```json
{ "id": "structure_and_disclosure_changes_acquisitions_consideration",
  "what_changed": "Consideration transferred for the fiscal 2026 acquisitions is printed as 348482000. Cash paid for acquisitions in the six-month cash-flow statement is printed as 211820000.",
  "account": "BusinessCombinationConsiderationTransferred1 (Fiscal2026AcquisitionsMember)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"348482000\"",
  "paragraph_id": "0001437749-26-025669:facts:BusinessCombinationConsiderationTransferred1:2026-06-01..2026-06-30:us-gaap:BusinessAcquisitionAxis=gnrc:Fiscal2026AcquisitionsMember" }
```

```json
{ "id": "structure_and_disclosure_changes_acquired_goodwill_year_to_date",
  "what_changed": "Goodwill acquired in the six months of 2026 is printed as 208598000, all in C&I (Residential: 0). Acquired intangibles for the 2026 acquisitions are printed at 88900000. The Q1 10-Q had printed first-quarter goodwill acquired of 28263000.",
  "account": "GoodwillAcquiredDuringPeriod",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"208598000\"",
  "paragraph_id": "0001437749-26-025669:facts:GoodwillAcquiredDuringPeriod:2026-01-01..2026-06-30" }
```

```json
{ "id": "structure_and_disclosure_changes_goodwill_balance",
  "what_changed": "Goodwill is printed as 1651751000 at 2026-06-30, against 1467094000 at 2025-12-31. By segment: Residential 853566000 against 855118000; C&I 798185000 against 611976000. Six-month currency translation on goodwill: -6475000.",
  "account": "Goodwill",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"1651751000\"",
  "paragraph_id": "0001437749-26-025669:facts:Goodwill:2026-06-30" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_enercon_consideration",
  "what_changed": "The Q1 10-Q reported the Enercon Engineering acquisition, closed 2026-04-01, as a subsequent event with consideration transferred of 122322000. It also tagged an equity component of 44785000; the Q2 10-Q prints treasury stock reissued in the quarter at 44785000.",
  "account": "BusinessCombinationConsiderationTransferred1 (Enercon)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"122322000\"",
  "paragraph_id": "0001437749-26-014882:facts:BusinessCombinationConsiderationTransferred1:2026-04-01..2026-04-01:us-gaap:BusinessAcquisitionAxis=gnrc:EnerconEngineeringIncMember,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_enercon_contingent_consideration_high",
  "what_changed": "The Q1 10-Q tagged the high end of Enercon contingent consideration at 112043000. Its later fair value is an estimate that runs through earnings.",
  "account": "BusinessCombinationContingentConsiderationArrangementsRangeOfOutcomesValueHigh (Enercon)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"112043000\"",
  "paragraph_id": "0001437749-26-014882:facts:BusinessCombinationContingentConsiderationArrangementsRangeOfOutcomesValueHigh:2026-04-01:us-gaap:BusinessAcquisitionAxis=gnrc:EnerconEngineeringIncMember,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

```json
{ "id": "liquidity_and_capital_contingent_consideration_liability",
  "what_changed": "The contingent consideration liability is printed as 121866000 at 2026-06-30, against 32872000 at 2025-12-31.",
  "account": "BusinessCombinationContingentConsiderationLiability",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"121866000\"",
  "paragraph_id": "0001437749-26-025669:facts:BusinessCombinationContingentConsiderationLiability:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_contingent_consideration_current",
  "what_changed": "The current portion of contingent consideration is printed as 105858000 at 2026-06-30, against 11175000 at 2025-12-31. Most of the liability is classified as due within a year.",
  "account": "BusinessCombinationContingentConsiderationLiabilityCurrent",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"105858000\"",
  "paragraph_id": "0001437749-26-025669:facts:BusinessCombinationContingentConsiderationLiabilityCurrent:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_goodwill_impairment_residential",
  "what_changed": "A Residential goodwill impairment of 1523000 is printed for the six months of 2026. It is the same amount the Q1 10-Q printed for the first quarter. The 10-K printed a 2025 goodwill and intangible impairment of 0.",
  "account": "GoodwillImpairmentLoss (ResidentialSegmentMember)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"1523000\"",
  "paragraph_id": "0001437749-26-025669:facts:GoodwillImpairmentLoss:2026-01-01..2026-06-30:us-gaap:StatementBusinessSegmentsAxis=gnrc:ResidentialSegmentMember" }
```

```json
{ "id": "structure_and_disclosure_changes_goodwill_written_off_on_sale",
  "what_changed": "Goodwill written off on business sales is printed as 15943000 for the six months of 2026, all in C&I.",
  "account": "GoodwillWrittenOffRelatedToSaleOfBusinessUnit",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"15943000\"",
  "paragraph_id": "0001437749-26-025669:facts:GoodwillWrittenOffRelatedToSaleOfBusinessUnit:2026-01-01..2026-06-30" }
```

```json
{ "id": "structure_and_disclosure_changes_business_disposition_loss_quarter",
  "what_changed": "The loss on business dispositions is printed as -13456000 for the second quarter of 2026, against -3905000 a year earlier. Six-month 2026: -18238000. The Q1 10-Q printed -4782000. Six-month proceeds from divestitures: 23654000. The release adds the loss back in adjusted net income and adjusted EBITDA.",
  "account": "GainLossOnSaleOfBusiness",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"-13456000\"",
  "paragraph_id": "0001437749-26-025669:facts:GainLossOnSaleOfBusiness:2026-04-01..2026-06-30" }
```

```json
{ "id": "structure_and_disclosure_changes_immaterial_dispositions_loss",
  "what_changed": "The loss on the immaterial business dispositions closed 2026-06-01 is printed as -13392000.",
  "account": "GainLossOnSaleOfBusiness (ImmaterialBusinessDispositionsMember)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"-13392000\"",
  "paragraph_id": "0001437749-26-025669:facts:GainLossOnSaleOfBusiness:2026-06-01..2026-06-01:us-gaap:DisposalGroupClassificationAxis=gnrc:ImmaterialBusinessDispositionsMember" }
```

### Numeric facts — liquidity and capital

```json
{ "id": "liquidity_and_capital_other_accrued_liabilities_balance",
  "what_changed": "Other accrued liabilities are printed as 447770000 at 2026-06-30, against 591387000 at 2025-12-31. The Zawaski accrual of 206500000 sat in this line at year end and is printed as paid during the six months.",
  "account": "OtherAccruedLiabilitiesCurrent",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"447770000\"",
  "paragraph_id": "0001437749-26-025669:facts:OtherAccruedLiabilitiesCurrent:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_accounts_payable_balance",
  "what_changed": "Accounts payable is printed as 556088000 at 2026-06-30, against 436583000 at 2025-12-31. The six-month cash-flow change in accounts payable is printed at 116387000.",
  "account": "AccountsPayableCurrent",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"556088000\"",
  "paragraph_id": "0001437749-26-025669:facts:AccountsPayableCurrent:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_repurchase_authorization_remaining",
  "what_changed": "Remaining repurchase authorization is printed as 199340000 as of 2026-02-09. No shares were repurchased in the six months of 2026; the release's cash-flow statement shows stock repurchases of (147,917) for the six months of 2025.",
  "account": "StockRepurchaseProgramRemainingAuthorizedRepurchaseAmount1",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"199340000\"",
  "paragraph_id": "0001437749-26-025669:facts:StockRepurchaseProgramRemainingAuthorizedRepurchaseAmount1:2026-02-09" }
```

```json
{ "id": "liquidity_and_capital_total_debt",
  "what_changed": "Debt and finance-lease obligations are printed as 1281010000 at 2026-06-30, against 1282448000 at 2025-12-31. Tranche A term loan: 700000000. Tranche B: 491250000 against 493750000. Cash is printed at 264921000 against 341413000.",
  "account": "DebtAndCapitalLeaseObligations",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"1281010000\"",
  "paragraph_id": "0001437749-26-025669:facts:DebtAndCapitalLeaseObligations:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_revolver_drawn",
  "what_changed": "The long-term line of credit (revolver) is printed as 0 at 2026-06-30, as it was at 2025-12-31.",
  "account": "LongTermLineOfCredit",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"0\"",
  "paragraph_id": "0001437749-26-025669:facts:LongTermLineOfCredit:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_short_term_borrowing_rate",
  "what_changed": "The weighted average short-term borrowing rate is printed as 0.0615 at 2026-06-30. Short-term borrowings: 48318000 against 50618000. The Q1 10-Q printed 0.0619 at 2026-03-31 (next item for its prior-year-end figure).",
  "account": "ShortTermDebtWeightedAverageInterestRate",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"0.0615\"",
  "paragraph_id": "0001437749-26-025669:facts:ShortTermDebtWeightedAverageInterestRate:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_short_term_borrowing_rate_prior_year_end",
  "what_changed": "The Q1 10-Q prints the weighted average short-term borrowing rate at 2025-12-31 as 0.13, against 0.0619 at 2026-03-31 and 0.0615 at 2026-06-30. The 2025-12-31 value stands apart from the two that follow it. This input does not show whether it is a different rate or a tagging difference.",
  "account": "ShortTermDebtWeightedAverageInterestRate",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"0.13\"",
  "paragraph_id": "0001437749-26-014882:facts:ShortTermDebtWeightedAverageInterestRate:2025-12-31" }
```

```json
{ "id": "liquidity_and_capital_capital_expenditure_quarter",
  "what_changed": "Second-quarter 2026 capital expenditure is printed as 58290000, against 57716000 a year earlier. Six-month figures: 87687000 against 88653000. By segment for the quarter: C&I 46412000 against 28992000; Residential 10438000 against 27404000.",
  "account": "SegmentExpenditureAdditionToLongLivedAssets",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"58290000\"",
  "paragraph_id": "0001437749-26-025669:facts:SegmentExpenditureAdditionToLongLivedAssets:2026-04-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_interest_expense_year_to_date",
  "what_changed": "Six-month 2026 interest expense is printed as 32163000, against 35352000 for the six months of 2025.",
  "account": "InterestExpense",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "\"value\": \"32163000\"",
  "paragraph_id": "0001437749-26-025669:facts:InterestExpense:2026-01-01..2026-06-30" }
```

## Seen in the notes

No items.

Each fact in input_numbers.json carries these fields: `id`, `paragraph_id`, `tag`, `prefix`, `namespace`, `context`, `context_ref`, `unit`, `decimals`, `value`, `number`, `nil`, `form`, `source_accession`, `filing_date`, and sometimes `superseded_by`. None of them says whether the element sat inside a note when it was extracted. I was told not to decide that myself, so no fact can be placed under this heading on the input's own marking.

All fact-based items above therefore sit under "Seen in the statements". That includes the warranty rollforward, the contingency, the segment, the RPO, the acquisition and the Schedule II items, which may have come from note tables.

The marker is missing from this input. The later split into a notes reader cannot be applied to this run's items until the facts carry it.
