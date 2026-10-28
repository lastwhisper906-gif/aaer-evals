# WDC — numbers reader — 10-Q 0001628280-26-029054 (period ended 2026-04-03, filed 2026-05-01)

## What the input holds and lacks (outside the items)

- **Files read in full:**
  - `input_trends.json`
  - `input_numbers.json`, which holds two filings: the prior 10-Q 0001628280-26-004207 (filed 2026-01-30) and the current 10-Q 0001628280-26-029054 (filed 2026-05-01)
  - `input_8k.md`
  - `input_prior_predictions.md`
- **Forbidden-data check.** Nothing in the directory is a price, abnormal return, short-interest figure, another company's file, a prior-run probability or an outcome window. The per-share amounts in the facts all come from the filings themselves:
  - contract terms of the 2028 convertible notes (conversion price 37.72, cap price 50.41, a 1.30 stock-price trigger);
  - EPS;
  - dividends per share;
  - grant-date fair values.
  None of these is market data.
- **No articulation checks, restatement traces or fourth-quarter derivation are in the input.** No articulation gap from such checks can be reported. Values printed twice at different precision under one paragraph id are reported as items below.
- **Restated prior values: none.** Every prior-10-Q fact that the input marks as superseded by the current 10-Q has the same value in both filings. This holds for:
  - the 2025-06-27 balance sheet;
  - net income for each quarter;
  - the equity rollforwards;
  - the warranty accrual.

  No period was reported differently by an earlier filing, so there is no restated value to quote.
- **Tag changes: none.** No trend cell says that its period rests on a concept different from the other periods' concept.
- **Periods reached: all.** The trend table requested 8 quarters and 5 years, and all 13 periods are present with status filled. No period lacks cells.
- **Formula baseline `research_and_development_capitalized`: insufficient.** Its years-back-0 cell is missing and prints no paragraph_id, so it cannot be quoted. The reason the input gives is that the record tags none of us-gaap:ResearchAndDevelopmentExpense in any period. The item `articulation_and_the_filed_history_tagged_research_and_development_concept_not_matched` below quotes the concept the company actually files.
- **8-K bundle, which has no paragraph ids and so yields no items.**
  - `input_8k.md` states that no 8-K filed at or before 2026-05-01 is on record and that the bundle has no earnings release. Its own item-code list nevertheless shows an 8-K dated 2026-04-30 (0001628280-26-028878) with items 2.02 and 9.01. The two statements disagree.
  - Either way, this input holds no earnings-release figures, no guidance and no non-GAAP numbers.
  - The same file lists an NT 10-Q filed 2024-02-08 for the period ended 2023-12-29.
- **Expectations: none.** No consensus, guidance or release figure is in the input, so `results_against_expectations` has no items.
- **Prior predictions:** none on record.
- **Conventions.**
  - `expected_direction` is `none` throughout. The input gives a value, a change and a position, not a direction, and this reader does not forecast.
  - `horizon` is `next 10-Q` for a quarterly figure, `next 10-K` for an annual one and `none` for a structural observation.
  - Ids that start with an area and then `trend` come from `input_trends.json`. Ids with `tagged` come from `input_numbers.json`.

## Seen in the statements

```json
[
  {
    "id": "earnings_quality_trend_accruals_ratio_quarterly_insufficient",
    "what_changed": "insufficient. Accruals over total assets is not filled for the quarter 2026-01-03..2026-04-03 because the record has no operating cash flow row for that quarter. There is no value, no quarter-over-quarter change and no year-over-year change. Only 2 of the 8 requested quarters (quarters-back-2 and quarters-back-6) are filled, and two points do not support a trend claim.",
    "account": "accruals (net income less operating cash flow) over total assets",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"missing\": \"no row for operating_cash_flow in 2026-01-03..2026-04-03: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
    "paragraph_id": "0001628280-26-029054:trends:accruals_over_total_assets:2026-01-03..2026-04-03"
  },
  {
    "id": "estimates_and_discretion_trend_bad_debt_reserve_ratio_quarterly_insufficient",
    "what_changed": "insufficient. The bad debt reserve ratio is not filled for the quarter 2026-01-03..2026-04-03 because the record tags no allowance-for-doubtful-accounts concept in any period. It is filled in none of the 13 periods on record, so there is no value, no change and no position.",
    "account": "allowance for doubtful accounts receivable",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"missing\": \"no row for bad_debt_allowance: the companyfacts record tags none of us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
    "paragraph_id": "0001628280-26-029054:trends:bad_debt_reserve_ratio:2026-01-03..2026-04-03"
  },
  {
    "id": "revenue_recognition_trend_contract_liabilities_ratio_quarterly_insufficient",
    "what_changed": "insufficient. Contract liabilities over revenue is not filled for the quarter 2026-01-03..2026-04-03. The listed contract-liability and deferred-revenue concepts are in the record, but not at 2026-04-03. The ratio is filled in none of the 13 periods on record, so there is no value, no change and no position.",
    "account": "contract liabilities / deferred revenue",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"missing\": \"no row for contract_liabilities in 2026-04-03: us-gaap:ContractWithCustomerLiabilityCurrent, us-gaap:ContractWithCustomerLiability, us-gaap:DeferredRevenueCurrent, us-gaap:DeferredRevenue is in the record, but not for this period\"",
    "paragraph_id": "0001628280-26-029054:trends:contract_liabilities_over_revenue:2026-01-03..2026-04-03"
  },
  {
    "id": "earnings_quality_trend_days_sales_of_inventory_quarterly",
    "what_changed": "Days sales of inventory for the quarter 2026-01-03..2026-04-03 is 74.34497290788681. Inputs: InventoryNet 1357000000.0 at 2026-04-03; CostOfGoodsAndServicesSold 1661000000.0; 91 days. The change is -0.6452531153263834 against quarters-back-1 and -11.979918553762971 against quarters-back-4. It is the lowest of the 6 filled quarters; quarters-back-3 and quarters-back-7 have no cost-of-revenue row.",
    "account": "inventory",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
    "paragraph_id": "0001628280-26-029054:trends:days_sales_of_inventory:2026-01-03..2026-04-03"
  },
  {
    "id": "revenue_recognition_trend_days_sales_outstanding_quarterly",
    "what_changed": "Days sales outstanding for the quarter 2026-01-03..2026-04-03 is 51.64938567575667. Inputs: AccountsReceivableNetCurrent 1894000000.0 at 2026-04-03; RevenueFromContractWithCustomerExcludingAssessedTax 3337000000.0; 91 days. The change is 0.8257197824852014 against quarters-back-1 and -6.623936033048906 against quarters-back-4. It is the third lowest of the 8 filled quarters.",
    "account": "accounts receivable",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"position_in_history\": \"third lowest of the 8 filled quarters\"",
    "paragraph_id": "0001628280-26-029054:trends:days_sales_outstanding:2026-01-03..2026-04-03"
  },
  {
    "id": "earnings_quality_trend_gross_margin_quarterly",
    "what_changed": "Gross margin for the quarter 2026-01-03..2026-04-03 is 0.5022475277195085. Inputs: revenue 3337000000.0; CostOfGoodsAndServicesSold 1661000000.0. The change is 0.04483950650638291 against quarters-back-1 and 0.10468867854775615 against quarters-back-4. It is the highest of the 6 filled quarters; quarters-back-3 and quarters-back-7 have no cost-of-revenue row.",
    "account": "gross margin (revenue and cost of goods and services sold)",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
    "paragraph_id": "0001628280-26-029054:trends:gross_margin:2026-01-03..2026-04-03"
  },
  {
    "id": "estimates_and_discretion_trend_inventory_reserve_ratio_quarterly_insufficient",
    "what_changed": "insufficient. The inventory reserve ratio is not filled for the quarter 2026-01-03..2026-04-03 because the record tags us-gaap:InventoryValuationReserves in no period. It is filled in none of the 13 periods on record, so there is no value, no change and no position.",
    "account": "inventory valuation reserve",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
    "paragraph_id": "0001628280-26-029054:trends:inventory_reserve_ratio:2026-01-03..2026-04-03"
  },
  {
    "id": "earnings_quality_trend_non_gaap_gap_quarterly_insufficient",
    "what_changed": "insufficient. The non-GAAP gap is not filled for the quarter 2026-01-03..2026-04-03 because no us-gaap concept carries a non-GAAP measure. The 8-K input holds no earnings release either, so no non-GAAP figure exists anywhere in this input. The gap is filled in none of the 13 periods.",
    "account": "non-GAAP net income",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
    "paragraph_id": "0001628280-26-029054:trends:non_gaap_gap:2026-01-03..2026-04-03"
  },
  {
    "id": "revenue_recognition_trend_receivables_over_revenue_quarterly",
    "what_changed": "Receivables over revenue for the quarter 2026-01-03..2026-04-03 is 0.5675756667665568. Inputs: AccountsReceivableNetCurrent 1894000000.0; revenue 3337000000.0. The change is 0.009073843763573675 against quarters-back-1 and -0.07279050585768032 against quarters-back-4. It is the third lowest of the 8 filled quarters.",
    "account": "accounts receivable",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"position_in_history\": \"third lowest of the 8 filled quarters\"",
    "paragraph_id": "0001628280-26-029054:trends:receivables_over_revenue:2026-01-03..2026-04-03"
  },
  {
    "id": "earnings_quality_trend_soft_asset_share_quarterly",
    "what_changed": "Soft asset share at 2026-04-03 is 0.7027583914921901. Inputs: Assets 15045000000.0; PropertyPlantAndEquipmentNet 2422000000.0; CashAndCashEquivalentsAtCarryingValue 2050000000.0. The change is -0.020065258498201288 against quarters-back-1 and 0.05857461827615884 against quarters-back-4. It is the fourth lowest of the 8 filled quarters.",
    "account": "soft assets (total assets less PP&E and cash)",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"position_in_history\": \"fourth lowest of the 8 filled quarters\"",
    "paragraph_id": "0001628280-26-029054:trends:soft_asset_share:2026-01-03..2026-04-03"
  },
  {
    "id": "estimates_and_discretion_trend_warranty_reserve_ratio_quarterly",
    "what_changed": "Warranty reserve ratio for the quarter 2026-01-03..2026-04-03 is 0.05693736889421636. Inputs: StandardProductWarrantyAccrual 190000000.0 at 2026-04-03; quarterly revenue 3337000000.0. The change is -0.0017301816526845287 against quarters-back-1 and 0.0063706731662303145 against quarters-back-4. It is the fourth highest of the 8 filled quarters.",
    "account": "standard product warranty accrual",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"position_in_history\": \"fourth highest of the 8 filled quarters\"",
    "paragraph_id": "0001628280-26-029054:trends:warranty_reserve_ratio:2026-01-03..2026-04-03"
  },
  {
    "id": "earnings_quality_trend_accruals_ratio_annual",
    "what_changed": "Accruals over total assets for the fiscal year 2024-06-29..2025-06-27 is 0.014140837023282388. Inputs: NetIncomeLoss 1889000000.0; NetCashProvidedByUsedInOperatingActivities 1691000000.0; Assets 14002000000.0 at 2025-06-27. The change against years-back-1 is 0.03497761559116729; an annual period has no preceding-quarter change. It is the highest of the 5 filled years.",
    "account": "accruals (net income less operating cash flow) over total assets",
    "expected_direction": "none",
    "horizon": "next 10-K",
    "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
    "paragraph_id": "0001628280-26-029054:trends:accruals_over_total_assets:2024-06-29..2025-06-27"
  },
  {
    "id": "estimates_and_discretion_trend_bad_debt_reserve_ratio_annual_insufficient",
    "what_changed": "insufficient. The bad debt reserve ratio is not filled for the fiscal year 2024-06-29..2025-06-27 because no allowance-for-doubtful-accounts concept is tagged in any period. There is no value, no change and no position.",
    "account": "allowance for doubtful accounts receivable",
    "expected_direction": "none",
    "horizon": "next 10-K",
    "quote": "\"missing\": \"no row for bad_debt_allowance: the companyfacts record tags none of us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
    "paragraph_id": "0001628280-26-029054:trends:bad_debt_reserve_ratio:2024-06-29..2025-06-27"
  },
  {
    "id": "revenue_recognition_trend_contract_liabilities_ratio_annual_insufficient",
    "what_changed": "insufficient. Contract liabilities over revenue is not filled for the fiscal year 2024-06-29..2025-06-27. The listed concepts are in the record, but not at 2025-06-27. There is no value, no change and no position.",
    "account": "contract liabilities / deferred revenue",
    "expected_direction": "none",
    "horizon": "next 10-K",
    "quote": "\"missing\": \"no row for contract_liabilities in 2025-06-27: us-gaap:ContractWithCustomerLiabilityCurrent, us-gaap:ContractWithCustomerLiability, us-gaap:DeferredRevenueCurrent, us-gaap:DeferredRevenue is in the record, but not for this period\"",
    "paragraph_id": "0001628280-26-029054:trends:contract_liabilities_over_revenue:2024-06-29..2025-06-27"
  },
  {
    "id": "earnings_quality_trend_days_sales_of_inventory_annual",
    "what_changed": "Days sales of inventory for the fiscal year 2024-06-29..2025-06-27 is 80.63212079615649. Inputs: InventoryNet 1291000000.0 at 2025-06-27; CostOfGoodsAndServicesSold 5828000000.0; 364 days. The change against years-back-1 is -30.474393288350555. It is the lowest of the 5 filled years.",
    "account": "inventory",
    "expected_direction": "none",
    "horizon": "next 10-K",
    "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
    "paragraph_id": "0001628280-26-029054:trends:days_sales_of_inventory:2024-06-29..2025-06-27"
  },
  {
    "id": "revenue_recognition_trend_days_sales_outstanding_annual",
    "what_changed": "Days sales outstanding for the fiscal year 2024-06-29..2025-06-27 is 56.81764705882353. Inputs: AccountsReceivableNetCurrent 1486000000.0 at 2025-06-27; revenue 9520000000.0; 364 days. The change against years-back-1 is -14.115390775591543. It is the third highest of the 5 filled years.",
    "account": "accounts receivable",
    "expected_direction": "none",
    "horizon": "next 10-K",
    "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
    "paragraph_id": "0001628280-26-029054:trends:days_sales_outstanding:2024-06-29..2025-06-27"
  },
  {
    "id": "earnings_quality_trend_gross_margin_annual",
    "what_changed": "Gross margin for the fiscal year 2024-06-29..2025-06-27 is 0.3878151260504202. Inputs: revenue 9520000000.0; CostOfGoodsAndServicesSold 5828000000.0. The change against years-back-1 is 0.10714392136465162. It is the highest of the 5 filled years.",
    "account": "gross margin (revenue and cost of goods and services sold)",
    "expected_direction": "none",
    "horizon": "next 10-K",
    "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
    "paragraph_id": "0001628280-26-029054:trends:gross_margin:2024-06-29..2025-06-27"
  },
  {
    "id": "estimates_and_discretion_trend_inventory_reserve_ratio_annual_insufficient",
    "what_changed": "insufficient. The inventory reserve ratio is not filled for the fiscal year 2024-06-29..2025-06-27 because us-gaap:InventoryValuationReserves is untagged in every period. There is no value, no change and no position.",
    "account": "inventory valuation reserve",
    "expected_direction": "none",
    "horizon": "next 10-K",
    "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
    "paragraph_id": "0001628280-26-029054:trends:inventory_reserve_ratio:2024-06-29..2025-06-27"
  },
  {
    "id": "earnings_quality_trend_non_gaap_gap_annual_insufficient",
    "what_changed": "insufficient. The non-GAAP gap is not filled for the fiscal year 2024-06-29..2025-06-27 because no us-gaap concept carries a non-GAAP measure. There is no value, no change and no position.",
    "account": "non-GAAP net income",
    "expected_direction": "none",
    "horizon": "next 10-K",
    "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
    "paragraph_id": "0001628280-26-029054:trends:non_gaap_gap:2024-06-29..2025-06-27"
  },
  {
    "id": "revenue_recognition_trend_receivables_over_revenue_annual",
    "what_changed": "Receivables over revenue for the fiscal year 2024-06-29..2025-06-27 is 0.15609243697478992. Inputs: AccountsReceivableNetCurrent 1486000000.0; revenue 9520000000.0. The change against years-back-1 is -0.03877854608678996. It is the third highest of the 5 filled years.",
    "account": "accounts receivable",
    "expected_direction": "none",
    "horizon": "next 10-K",
    "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
    "paragraph_id": "0001628280-26-029054:trends:receivables_over_revenue:2024-06-29..2025-06-27"
  },
  {
    "id": "earnings_quality_trend_soft_asset_share_annual",
    "what_changed": "Soft asset share at 2025-06-27 is 0.6816883302385374. Inputs: Assets 14002000000.0; PropertyPlantAndEquipmentNet 2343000000.0; CashAndCashEquivalentsAtCarryingValue 2114000000.0. The change against years-back-1 is -0.15666126460187935. It is the lowest of the 5 filled years.",
    "account": "soft assets (total assets less PP&E and cash)",
    "expected_direction": "none",
    "horizon": "next 10-K",
    "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
    "paragraph_id": "0001628280-26-029054:trends:soft_asset_share:2024-06-29..2025-06-27"
  },
  {
    "id": "estimates_and_discretion_trend_warranty_reserve_ratio_annual",
    "what_changed": "Warranty reserve ratio for the fiscal year 2024-06-29..2025-06-27 is 0.015966386554621848. Inputs: StandardProductWarrantyAccrual 152000000.0 at 2025-06-27; annual revenue 9520000000.0. The change against years-back-1 is -0.006512638298947885. It is the second lowest of the 5 filled years.",
    "account": "standard product warranty accrual",
    "expected_direction": "none",
    "horizon": "next 10-K",
    "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
    "paragraph_id": "0001628280-26-029054:trends:warranty_reserve_ratio:2024-06-29..2025-06-27"
  },
  {
    "id": "articulation_and_the_filed_history_trend_cost_of_revenue_row_absent",
    "what_changed": "insufficient. The record has no cost-of-revenue row for the quarter 2025-03-29..2025-06-27, the quarter that ends the fiscal year, so gross margin and days sales of inventory are not filled there. The same holds for 2024-03-30..2024-06-28. Both metrics therefore have 6 filled quarters, not 8, and quarters-back-2 has no quarter-over-quarter change for either. The input contains no fourth-quarter derivation.",
    "account": "cost of goods and services sold",
    "expected_direction": "none",
    "horizon": "next 10-K",
    "quote": "\"missing\": \"no row for cost_of_revenue in 2025-03-29..2025-06-27: us-gaap:CostOfRevenue, us-gaap:CostOfGoodsAndServicesSold, us-gaap:CostOfGoodsSold, us-gaap:CostOfServices, us-gaap:CostOfSales is in the record, but not for this period\"",
    "paragraph_id": "0001628280-26-029054:trends:gross_margin:2025-03-29..2025-06-27"
  },
  {
    "id": "structure_and_disclosure_changes_trend_comparison_inputs_from_different_filings",
    "what_changed": "The year-over-year comparison cell for the latest quarter (quarters-back-4, 2024-12-28..2025-03-28) mixes filings. Its receivables, inventory, assets, cash and PP&E inputs come from accession 0000106040-25-000026, filed 2025-05-02. Its revenue and cost-of-goods inputs come from 0001628280-26-029054, filed 2026-05-01. Quarters-back-5 and quarters-back-6 also take balance-sheet inputs from older accessions (0000106040-25-000008 and 0000106040-24-000040) and revenue from filings dated 2026-01-30 and 2025-10-31. The numeric facts show a Sandisk discontinued operation in 2024-12-28..2025-03-28. The input does not say whether the balance-sheet and revenue inputs of these cells are on the same basis.",
    "account": "accounts receivable, inventory, total assets against revenue",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"id\": \"0000106040-25-000026:facts:AccountsReceivableNetCurrent:2025-03-28\"",
    "paragraph_id": "0001628280-26-029054:trends:receivables_over_revenue:2024-12-28..2025-03-28"
  },
  {
    "id": "articulation_and_the_filed_history_tagged_research_and_development_concept_not_matched",
    "what_changed": "insufficient. The formula baseline research_and_development_capitalized has no years-back-0 cell because the record tags no us-gaap:ResearchAndDevelopmentExpense in any period. The company files R&D under us-gaap:ResearchAndDevelopmentExpenseExcludingAcquiredInProcessCost: 294000000 for 2026-01-03..2026-04-03, against 289000000 for 2025-10-04..2026-01-02 in the prior 10-Q. The baseline looks for a concept the company does not use, so no R&D capitalization figure exists in this input.",
    "account": "research and development expense",
    "expected_direction": "none",
    "horizon": "next 10-K",
    "quote": "\"value\": \"294000000\"",
    "paragraph_id": "0001628280-26-029054:facts:ResearchAndDevelopmentExpenseExcludingAcquiredInProcessCost:2026-01-03..2026-04-03"
  },
  {
    "id": "earnings_quality_tagged_unrealized_gain_on_equity_securities",
    "what_changed": "The unrealized gain on equity securities held at fair value through net income is 2734000000 for 2026-01-03..2026-04-03. It was 1103000000 for 2025-10-04..2026-01-02 (prior 10-Q) and -606000000 for 2024-12-28..2025-03-28, and it is 4448000000 year to date. For the same quarter, operating income is 1190000000, non-operating income 2169000000, pre-tax income 3359000000 and net income 3205000000. The quarter's unrealized gain is larger than its operating income. The holdings are Level 1 equity securities: 1187000000 at 2026-04-03, 2068000000 at 2026-01-02 and 354000000 at 2025-06-27.",
    "account": "equity securities at fair value through net income (non-operating income)",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"value\": \"2734000000\"",
    "paragraph_id": "0001628280-26-029054:facts:EquitySecuritiesFvNiUnrealizedGainLoss:2026-01-03..2026-04-03"
  },
  {
    "id": "liquidity_and_capital_tagged_debt_extinguishment_loss",
    "what_changed": "The loss on extinguishment of debt is -545000000 for 2026-01-03..2026-04-03, against 0 for 2024-12-28..2025-03-28, and -545000000 year to date. The facts split it into -539000000 tagged to Term Loan A-3 and -6000000 tagged to senior notes, both for 2026-02-01..2026-02-28. It sits in non-operating income alongside the unrealized gain on equity securities.",
    "account": "gain (loss) on extinguishment of debt",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"value\": \"-545000000\"",
    "paragraph_id": "0001628280-26-029054:facts:GainsLossesOnExtinguishmentOfDebt:2026-01-03..2026-04-03"
  },
  {
    "id": "liquidity_and_capital_tagged_term_loan_extinguishment",
    "what_changed": "Term Loan A-3 accounts for -539000000 of the quarter's extinguishment loss, dated 2026-02-01..2026-02-28. Its carrying amount is 0 at 2026-04-03, against 1649000000 at 2025-06-27, and the year-to-date repayments tagged to it are 63000000. A separate fact tags an 800000000 Term Loan A-3 extinguishment for 2025-06-01..2025-06-30 to the Sandisk member. The input does not say how the remaining balance was settled or what the loss consists of.",
    "account": "Term Loan A-3",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"value\": \"-539000000\"",
    "paragraph_id": "0001628280-26-029054:facts:GainsLossesOnExtinguishmentOfDebt:2026-02-01..2026-02-28:us-gaap:DebtInstrumentAxis=wdc:TermLoanA3Member"
  },
  {
    "id": "liquidity_and_capital_tagged_long_term_debt_all_current",
    "what_changed": "Noncurrent long-term debt is 0 at 2026-04-03, against 2485000000 at 2025-06-27. Current long-term debt is 1581000000 (2226000000 at 2025-06-27) and total long-term debt is 1581000000 (4711000000). Of the instruments listed, only the 3.00% convertible notes due 2028 keep a carrying amount, with 1600000000 principal. The 4.75% notes due 2026, the 2.85% notes due 2029, the 3.10% notes due 2032 and Term Loan A-3 all carry 0. All remaining debt is classified current. The facts print the notes' conversion trigger terms but do not say whether a trigger was met or why the notes are current.",
    "account": "long-term debt (current and noncurrent)",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"value\": \"0\"",
    "paragraph_id": "0001628280-26-029054:facts:LongTermDebtNoncurrent:2026-04-03"
  },
  {
    "id": "liquidity_and_capital_tagged_convertible_notes_fair_value_against_carrying",
    "what_changed": "The estimated Level 2 fair value of the 3.00% convertible notes due 2028 is 12507000000 at 2026-04-03, against a carrying amount of 1581000000. At 2025-06-27 the fair value was 2849000000 against 1575000000 carrying. The prior 10-Q printed 7993000000 against 1579000000 at 2026-01-02. The conversion price is 37.72 and the capped-call cap price is 50.41. 32000000 of the notes converted in the quarter.",
    "account": "3.00% convertible notes due 2028",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"value\": \"12507000000\"",
    "paragraph_id": "0001628280-26-029054:facts:LongTermDebtFairValue:2026-04-03:us-gaap:DebtInstrumentAxis=wdc:ThreePointZeroZeroPercentConvertibleNotesDueTwoThousandTwentyEightMember,us-gaap:FairValueByFairValueHierarchyLevelAxis=us-gaap:FairValueInputsLevel2Member,us-gaap:FairValueByMeasurementBasisAxis=us-gaap:EstimateOfFairValueFairValueDisclosureMember"
  },
  {
    "id": "liquidity_and_capital_tagged_incremental_dilutive_shares",
    "what_changed": "Incremental dilutive shares are 45000000 for 2026-01-03..2026-04-03, against 10000000 for 2024-12-28..2025-03-28, and 38000000 year to date. Diluted weighted shares are 387000000 against 342000000 basic. The tag names share-based payment arrangements, and the input does not break the 45000000 down by instrument.",
    "account": "weighted average diluted shares",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"value\": \"45000000\"",
    "paragraph_id": "0001628280-26-029054:facts:IncrementalCommonSharesAttributableToShareBasedPaymentArrangements:2026-01-03..2026-04-03"
  },
  {
    "id": "earnings_quality_tagged_diluted_earnings_per_share",
    "what_changed": "Diluted EPS is 8.20 for 2026-01-03..2026-04-03 (basic 9.26), against 1.42 for 2024-12-28..2025-03-28. Year to date it is 16.05, against 4.38. The comparison quarter's diluted EPS includes -0.69 from discontinued operations; the current quarter has none. The input holds no consensus, guidance or earnings release, so there is nothing to set this result against.",
    "account": "earnings per share",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"value\": \"8.20\"",
    "paragraph_id": "0001628280-26-029054:facts:EarningsPerShareDiluted:2026-01-03..2026-04-03"
  },
  {
    "id": "revenue_recognition_tagged_quarterly_revenue_and_regions",
    "what_changed": "Revenue is 3337000000 for 2026-01-03..2026-04-03, against 2294000000 for 2024-12-28..2025-03-28. Year to date it is 9172000000, against 6915000000. By end market the facts print 2972000000 for Cloud, 179000000 for Client and 186000000 for Consumer. By region (comparison quarter in brackets): Americas 1499000000 (1182000000), Asia 1320000000 (753000000), Europe, Middle East and Africa 518000000 (359000000). The single reportable segment, HDD, carries the whole amount.",
    "account": "revenue",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"value\": \"3337000000\"",
    "paragraph_id": "0001628280-26-029054:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-01-03..2026-04-03"
  },
  {
    "id": "revenue_recognition_tagged_customer_concentration_top_ten",
    "what_changed": "The top ten customers are 0.71 of revenue for 2026-01-03..2026-04-03, against 0.73 for 2024-12-28..2025-03-28. Year to date the share is 0.74, against 0.68. The prior 10-Q printed 0.76. By customer this quarter (comparison quarter in brackets): Customer One 0.17 (0.18), Customer Two 0.15 (0.16), Customer Three 0.11 (0.13).",
    "account": "revenue concentration",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"value\": \"0.71\"",
    "paragraph_id": "0001628280-26-029054:facts:ConcentrationRiskPercentage1:2026-01-03..2026-04-03:srt:MajorCustomersAxis=wdc:TopTenCustomersMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:RevenueFromContractWithCustomerMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember"
  },
  {
    "id": "revenue_recognition_tagged_customer_concentration_receivables",
    "what_changed": "Customer One is 0.28 of accounts receivable (tagged over 2025-06-28..2026-04-03), against 0.20 for 2024-06-29..2025-06-27; the prior 10-Q printed 0.24. Customer Two is 0.12 (0.19). Customer Three has 0.12 for 2024-06-29..2025-06-27 and no current figure. Customer One's share of receivables is above its 0.17 share of the quarter's revenue.",
    "account": "accounts receivable concentration",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"value\": \"0.28\"",
    "paragraph_id": "0001628280-26-029054:facts:ConcentrationRiskPercentage1:2025-06-28..2026-04-03:srt:MajorCustomersAxis=wdc:CustomerOneMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:AccountsReceivableMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember"
  },
  {
    "id": "articulation_and_the_filed_history_tagged_receivables_printed_twice_at_different_precision",
    "what_changed": "The prior 10-Q prints receivables at 2026-01-02 twice under one paragraph id: 1685000000 at decimals -6 and 1690000000 at decimals -7. It does the same at 2025-06-27, with 1486000000 and 1490000000. This is the same amount at two roundings, not a restatement, but a reader matching on paragraph id alone gets two values.",
    "account": "accounts receivable",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"value\": \"1690000000\"",
    "paragraph_id": "0001628280-26-004207:facts:AccountsReceivableNetCurrent:2026-01-02"
  },
  {
    "id": "articulation_and_the_filed_history_tagged_receivables_rounded_beside_concentration_facts",
    "what_changed": "The current 10-Q prints receivables at 2026-04-03 as 1890000000 at decimals -7, next to the customer-concentration facts. The trend cells use 1894000000.0 for the same concept and date. The 10-Q also prints 1490000000 at decimals -7 for 2025-06-27. These are rounding duplicates under one paragraph id, not restatements.",
    "account": "accounts receivable",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"value\": \"1890000000\"",
    "paragraph_id": "0001628280-26-029054:facts:AccountsReceivableNetCurrent:2026-04-03"
  },
  {
    "id": "articulation_and_the_filed_history_tagged_goodwill_printed_at_two_precisions",
    "what_changed": "In the current 10-Q, goodwill prints 4320000000 at decimals -7 at both 2026-04-03 and 2025-06-27. For 2025-06-27 the prior 10-Q printed both 4319000000 at decimals -6 and 4320000000 at decimals -7. At this precision goodwill shows no change between 2025-06-27 and 2026-04-03.",
    "account": "goodwill",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"value\": \"4320000000\"",
    "paragraph_id": "0001628280-26-029054:facts:Goodwill:2026-04-03"
  },
  {
    "id": "estimates_and_discretion_tagged_warranty_provisions_issued",
    "what_changed": "Warranty provisions for 2026-01-03..2026-04-03 are 40000000, against 24000000 for 2024-12-28..2025-03-28. Payments are 21000000 (18000000). The accrual is 190000000 at 2026-04-03, 177000000 at 2026-01-02 and 116000000 at 2025-03-28. At 2026-04-03 the current portion is 39000000 and the noncurrent portion 151000000; at 2025-06-27 they were 57000000 and 95000000.",
    "account": "standard product warranty accrual",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"value\": \"40000000\"",
    "paragraph_id": "0001628280-26-029054:facts:StandardProductWarrantyAccrualWarrantiesIssued:2026-01-03..2026-04-03"
  },
  {
    "id": "estimates_and_discretion_tagged_warranty_preexisting_estimate_change",
    "what_changed": "The change in estimate for pre-existing warranties is -6000000 for 2026-01-03..2026-04-03, against -11000000 for 2024-12-28..2025-03-28. Year to date it is 0, against -38000000 for 2024-06-29..2025-03-28.",
    "account": "standard product warranty accrual (pre-existing warranties)",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"value\": \"-6000000\"",
    "paragraph_id": "0001628280-26-029054:facts:StandardProductWarrantyAccrualPreexistingIncreaseDecrease:2026-01-03..2026-04-03"
  },
  {
    "id": "estimates_and_discretion_tagged_unrecognized_tax_benefits",
    "what_changed": "Unrecognized tax benefits are 603000000 at 2026-04-03, against 569000000 at 2025-06-27. Year-to-date increases are 8000000 from current-period positions and 30000000 from prior-period positions. Decreases are 3000000 from settlements and 1000000 from lapses of the statute of limitations. Accrued interest and penalties are 123000000. The noncurrent liability for uncertain tax positions is 228000000, against 163000000 at 2025-06-27.",
    "account": "unrecognized tax benefits",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"value\": \"603000000\"",
    "paragraph_id": "0001628280-26-029054:facts:UnrecognizedTaxBenefits:2026-04-03"
  },
  {
    "id": "earnings_quality_tagged_effective_tax_rate",
    "what_changed": "The effective tax rate on continuing operations is 0.05 for 2026-01-03..2026-04-03, against -9.43 for 2024-12-28..2025-03-28. Year to date it is 0.06, against -0.78 for 2024-06-29..2025-03-28. Tax expense is 154000000 on pre-tax income of 3359000000; the comparison quarter had a -698000000 benefit on pre-tax income of 74000000. The input does not say what drives the rate.",
    "account": "income tax expense",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"value\": \"0.05\"",
    "paragraph_id": "0001628280-26-029054:facts:EffectiveIncomeTaxRateContinuingOperations:2026-01-03..2026-04-03"
  },
  {
    "id": "estimates_and_discretion_tagged_restructuring_reserve",
    "what_changed": "The business realignment reserve is 29000000 at 2026-04-03, against 10000000 at 2025-06-27. One-time termination benefits are 23000000 of it and contract termination 6000000. Year-to-date charges are 95000000, all one-time termination benefits, and payments are 76000000. Accelerated share-based compensation under the plan is 5000000 for the quarter and 8000000 year to date.",
    "account": "restructuring reserve (business realignment)",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"value\": \"29000000\"",
    "paragraph_id": "0001628280-26-029054:facts:RestructuringReserve:2026-04-03:us-gaap:RestructuringPlanAxis=wdc:BusinessRealignmentActivitiesMember"
  },
  {
    "id": "liquidity_and_capital_tagged_share_repurchases",
    "what_changed": "Repurchases are 752000000 for 2900000 shares in 2026-01-03..2026-04-03, and 1920000000 for 13100000 shares year to date. The remaining authorization is 3930000000 at 2026-04-03. Shares outstanding are 345000000 at 2026-04-03, against 347000000 at 2025-06-27. Dividends paid are 43000000 in the quarter and 120000000 year to date.",
    "account": "treasury stock / share repurchases",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"value\": \"752000000\"",
    "paragraph_id": "0001628280-26-029054:facts:TreasuryStockValueAcquiredCostMethod:2026-01-03..2026-04-03"
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_tagged_dividend_declaration",
    "what_changed": "On 2026-04-29, after the balance sheet date and tagged as a subsequent event, a dividend of 0.15 per share was declared. The dividend declared in 2026-01-03..2026-04-03 was 0.125 per share, and 0.35 year to date.",
    "account": "common stock dividends per share",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"value\": \"0.15\"",
    "paragraph_id": "0001628280-26-029054:facts:CommonStockDividendsPerShareDeclared:2026-04-29..2026-04-29:us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember"
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_tagged_retained_sandisk_shares",
    "what_changed": "The company holds 1700000 Sandisk shares at 2026-04-03, tagged under the equity-method investee axis with the Sandisk member. Level 1 equity securities are 1187000000 at the same date, and the quarter's unrealized gain on equity securities is 2734000000. The input does not tie the 1187000000 to these shares one-to-one.",
    "account": "investment in former subsidiary (Sandisk shares)",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"value\": \"1700000\"",
    "paragraph_id": "0001628280-26-029054:facts:InvestmentOwnedBalanceShares:2026-04-03:srt:ScheduleOfEquityMethodInvestmentEquityMethodInvesteeNameAxis=wdc:SandiskCorporationFlashMember"
  },
  {
    "id": "structure_and_disclosure_changes_tagged_sandisk_spin_off_discontinued_operations",
    "what_changed": "The comparison quarter 2024-12-28..2025-03-28 carries Sandisk as a spun-off discontinued operation. Its revenue is 602000000, operating loss -209000000 and net loss -252000000; per share, -0.71 basic and -0.69 diluted. For 2024-06-29..2025-03-28 the discontinued revenue is 4361000000 and net income 216000000. The current quarter and year to date carry 0 from discontinued operations. Continuing income in the comparison quarter is 772000000.",
    "account": "discontinued operations (Sandisk spin-off)",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"value\": \"602000000\"",
    "paragraph_id": "0001628280-26-029054:facts:DisposalGroupIncludingDiscontinuedOperationRevenue:2024-12-28..2025-03-28:us-gaap:DisposalGroupClassificationAxis=us-gaap:DiscontinuedOperationsDisposedOfByMeansOtherThanSaleSpinoffMember,us-gaap:IncomeStatementBalanceSheetAndAdditionalDisclosuresByDisposalGroupsIncludingDiscontinuedOperationsAxis=wdc:SandiskSemiconductorCo.Ltd.Member"
  },
  {
    "id": "structure_and_disclosure_changes_tagged_single_reportable_segment",
    "what_changed": "There is one reportable segment, HDD. Its revenue (3337000000 for the quarter) and its income from continuing operations (3205000000) equal the consolidated figures, so the segment facts add no breakdown.",
    "account": "segment reporting",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"value\": \"1\"",
    "paragraph_id": "0001628280-26-029054:facts:NumberOfReportableSegments:2025-06-28..2026-04-03"
  },
  {
    "id": "liquidity_and_capital_tagged_bridge_loan",
    "what_changed": "A bridge loan with a face amount of 1500000000 is tagged at 2026-02-28. Year-to-date debt proceeds are 1496000000 and repayments 1564000000. The debt carrying amounts at 2026-04-03 list only the 2028 convertible notes (1600000000 principal), so no bridge loan balance is printed at quarter end. The revolving credit facility due 2027 shows current borrowing capacity of 1250000000.",
    "account": "bridge loan / borrowings",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"value\": \"1500000000\"",
    "paragraph_id": "0001628280-26-029054:facts:DebtInstrumentFaceAmount:2026-02-28:us-gaap:DebtInstrumentAxis=us-gaap:BridgeLoanMember"
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_tagged_litigation_settlement_gain_in_comparison_base",
    "what_changed": "The comparison quarter 2024-12-28..2025-03-28 includes a 201000000 gain related to settled IP litigation; the figure for 2024-06-29..2025-03-28 is 198000000. The facts also print an IP litigation accrual of 384000000 at 2024-06-28 and legal settlement payments of 130000000 for 2025-04-01..2025-04-30. Year-over-year comparisons of the quarter therefore carry this gain in their base.",
    "account": "litigation settlement gain",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"value\": \"201000000\"",
    "paragraph_id": "0001628280-26-029054:facts:GainLossRelatedToLitigationSettlement:2024-12-28..2025-03-28:srt:LitigationCaseAxis=wdc:IntellectualPropertyLitigationMember,us-gaap:LitigationStatusAxis=us-gaap:SettledLitigationMember"
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_tagged_spex_damages_printed_as_one",
    "what_changed": "For the SPEX Technologies lawsuit, tagged as settled, damages awarded print 316000000 for 2024-10-18 and settlement interest 237000000 for 2025-01-08. The same damages concept then prints 1, in USD at decimals 0, for both 2025-06-16 and 2025-06-27. The input does not say whether 1 is a nominal award or a scaling choice.",
    "account": "loss contingency (SPEX litigation)",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"value\": \"1\"",
    "paragraph_id": "0001628280-26-029054:facts:LossContingencyDamagesAwardedValue:2025-06-27..2025-06-27:srt:LitigationCaseAxis=wdc:SPEXTechnologiesInc.LawsuitMember,us-gaap:LitigationStatusAxis=us-gaap:SettledLitigationMember"
  },
  {
    "id": "structure_and_disclosure_changes_tagged_convertible_preferred_conversion",
    "what_changed": "The convertible preferred's liquidation preference prints 265000000 at 2026-04-03, the same as at 2025-06-27. The equity facts show temporary equity of 0 at 2026-04-03 after a 229000000 conversion of convertible securities. The facts also print, at 2026-02-17, a liquidation preference of 267000000 and 7000000 under PreferredStockSharesOutstanding, against 235000 temporary-equity shares at 2025-06-27. There is a 32000000 paid-in-kind preferred dividend for 2026-02-17..2026-03-17. The input does not explain a nonzero liquidation preference at a date when the carrying amount is 0, and it does not reconcile the two share counts.",
    "account": "Series A convertible preferred stock (temporary equity)",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"value\": \"265000000\"",
    "paragraph_id": "0001628280-26-029054:facts:TemporaryEquityLiquidationPreference:2026-04-03"
  },
  {
    "id": "liquidity_and_capital_tagged_pension_funded_status",
    "what_changed": "The defined benefit plan's funded status is -75000000 at 2026-04-03, against -68000000 at 2025-06-27. The benefit obligation is 251000000 (272000000) and plan assets are 176000000 (204000000).",
    "account": "defined benefit pension plan",
    "expected_direction": "none",
    "horizon": "next 10-Q",
    "quote": "\"value\": \"-75000000\"",
    "paragraph_id": "0001628280-26-029054:facts:DefinedBenefitPlanFundedStatusOfPlan:2026-04-03"
  }
]
```

## Seen in the notes

No fact in `input_numbers.json` carries a marker saying whether its element sat inside a note. Each fact has only these fields: id, paragraph_id, tag, prefix, namespace, context, context_ref, unit, decimals, value, number, nil, form, source_accession, filing_date, and on some prior-10-Q facts superseded_by.

Without that marker, this reader cannot place any finding here, and it does not guess. Several items above come from tables that usually sit in notes:

- customer concentration
- warranty rollforward
- debt fair values
- tax reserves
- restructuring
- litigation
- preferred stock
- pension

They stay under the statements heading because the input does not mark them.

```json
[]
```
