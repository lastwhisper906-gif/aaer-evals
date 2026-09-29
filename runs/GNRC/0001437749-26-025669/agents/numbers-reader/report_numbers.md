# GNRC — numbers report — 10-Q 0001437749-26-025669 (period ended 2026-06-30, filed 2026-08-04)

## Before the items

- **What is in the directory.** There are four input files: input_8k.md, input_numbers.json, input_prior_predictions.md and input_trends.json. None of them holds prices, abnormal returns, short interest, another company's files, a prior run's probability or an outcome window, so the run is not broken on that count.
- **Prior flags.** There are none. input_prior_predictions.md says: "None on record. This company has no earlier run under the given run root, so there are no flags, no management explanations and no outcomes to carry forward."
- **Checks my instructions name that are not in the input.** There is no articulation-check file, no restatement-trace file and no fourth-quarter derivation (the src/fourth_quarter.py output). I computed no substitute for any of them.
  - This report therefore lists **no articulation gaps**. That is because no articulation check is in my input, not because the statements were shown to articulate.
  - The restated prior values listed below are ones I found directly in the numeric facts: the same concept and the same date carry different values in different filings. No Python restatement trace flagged them.
- **Periods the record does not reach (no cells, so there is nothing to quote).** These are quarters-back-2 (target end 2025-12-30) and quarters-back-6 (target end 2024-12-31). The trend table gives this reason for each: "no quarter ending within 20 days of 2025-12-30 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py". The reason for 2024-12-31 is the same text with that date. The derivation it points to is not in my input.
- **A formula baseline with no paragraph_id.** The years-back-0 block research_and_development_capitalized prints values but no paragraph_id, so I cannot quote it and it has no item.
  - Printed values: book_value_with_rnd_capitalized 3240408000.0, earnings_with_rnd_capitalized 255549800.0, research_and_development_amortization 147474200.0, research_and_development_asset 607986000.0.
  - capitalized_development_cost and capitalized_over_expense are missing. The reason given is that the record tags none of us-gaap:CapitalizedComputerSoftwareAdditions in any period.
- **Window.** The record is companyfacts: 20394 rows from 14 filings. Its newest filing is 2026-08-04 and the cutoff is 2026-08-04. record_predates_the_trigger is null.
- **The 8-K.** This is the earnings release 0001437749-26-024731, filed 2026-07-29. It lists no late-filing notifications on or before 2026-08-04. Its table rows carry invisible characters, so I quote only its prose paragraphs.
- **Arithmetic.** I did none. Every ratio, change and position below is Python's, copied as printed. Where a figure I would want does not exist in the input, I say so.

## Seen in the statements

### Trend table — quarters-back-0 (2026-04-01..2026-06-30)

```json
{ "id": "earnings_quality_gross_margin_quarterly_cell",
  "what_changed": "gross_margin is 0.444658332694225, the highest of the 6 filled quarters. Change against quarters-back-1: 0.0574112554356786; against quarters-back-4: 0.05193200917742419. Inputs: revenue 1173510000.0, cost of revenue 651699000.0. The 8-K states 44.5% for the same quarter and says tariff refunds contributed approximately 6% to gross margin (0001437749-26-024731:8k_2_02:22). The full-year outlook treats the refund as a second-quarter item (0001437749-26-024731:8k_2_02:36). The top position therefore rests on an item the company ties to this one quarter. Six filled quarters is a short history.",
  "account": "gross margin (RevenueFromContractWithCustomerExcludingAssessedTax, CostOfGoodsAndServicesSold)",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
  "paragraph_id": "0001437749-26-025669:trends:gross_margin:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_quarterly_cell",
  "what_changed": "bad_debt_reserve_ratio is 0.048034698444174795, the lowest of the 6 filled quarters. Change against quarters-back-1: -0.002404253647686143; against quarters-back-4: -0.004855672436630619. Inputs: allowance 33767000.0, receivables 669204000.0. The allowance is at its smallest share of gross receivables in the six filled quarters. The input holds nothing on collections experience that would say whether the allowance is thin; that judgement is insufficient.",
  "account": "allowance for doubtful accounts receivable (AllowanceForDoubtfulAccountsReceivableCurrent)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001437749-26-025669:trends:bad_debt_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly_cell",
  "what_changed": "contract_liabilities_over_revenue is 0.10048316588695452, the second highest of the 6 filled quarters; quarters-back-1 is the highest. Change against quarters-back-1: -0.02925304401237197; against quarters-back-4: 0.07807485957570721. Inputs: contract liabilities 117918000.0, revenue 1173510000.0. The earliest filled quarter (quarters-back-7) is the lowest at 0.01694071813784177. The filed history of this concept carries different figures for one balance date under different contexts (see the contract-liability items below). Whether the rise reflects customer deposits or a change in what the tag covers is insufficient to judge from this input.",
  "account": "contract liabilities (ContractWithCustomerLiability)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"",
  "paragraph_id": "0001437749-26-025669:trends:contract_liabilities_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_quarterly_cell",
  "what_changed": "days_sales_of_inventory is 172.98977135149818, the third lowest of the 6 filled quarters. Change against quarters-back-1: -0.567980651570565; against quarters-back-4: -4.1091749878457335. Inputs: inventory 1238871000.0, cost of revenue 651699000.0. The 8-K says tariff refunds contributed to the quarter's gross margin, so the cost of revenue in the denominator is the refund-affected figure. The input does not isolate the refund inside cost of revenue.",
  "account": "inventory (InventoryNet) against cost of goods sold",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"position_in_history\": \"third lowest of the 6 filled quarters\"",
  "paragraph_id": "0001437749-26-025669:trends:days_sales_of_inventory:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly_cell",
  "what_changed": "days_sales_outstanding is 51.893519441674975, the second lowest of the 6 filled quarters. Change against quarters-back-1: -1.3388980914698791; against quarters-back-4: -3.7385014711108226. Inputs: receivables 669204000.0, revenue 1173510000.0.",
  "account": "accounts receivable (AccountsReceivableNetCurrent) against revenue",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"position_in_history\": \"second lowest of the 6 filled quarters\"",
  "paragraph_id": "0001437749-26-025669:trends:days_sales_outstanding:2026-04-01..2026-06-30" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarterly_cell",
  "what_changed": "receivables_over_revenue is 0.5702584554030217, the second lowest of the 6 filled quarters. Change against quarters-back-1: -0.02121285052081001; against quarters-back-4: -0.04108243374847065. Inputs: receivables 669204000.0, revenue 1173510000.0.",
  "account": "accounts receivable (AccountsReceivableNetCurrent) against revenue",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"position_in_history\": \"second lowest of the 6 filled quarters\"",
  "paragraph_id": "0001437749-26-025669:trends:receivables_over_revenue:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_soft_asset_share_quarterly_cell",
  "what_changed": "soft_asset_share is 0.8046657130071615, the lowest of the 6 filled quarters. Change against quarters-back-1: -0.0013233849487186422; against quarters-back-4: -0.011568733208239701. Inputs: assets 5772151000.0, cash 264921000.0, property, plant and equipment 862578000.0. The share sits at its low even though the 10-Q tags goodwill acquired of 208598000 in the six months (see the goodwill item).",
  "account": "total assets less cash and PP&E, over total assets",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
  "paragraph_id": "0001437749-26-025669:trends:soft_asset_share:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_quarterly_cell",
  "what_changed": "warranty_reserve_ratio is 0.11150309754497192, the second lowest of the 6 filled quarters. Change against quarters-back-1: -0.009658164154253551; against quarters-back-4: -0.001526966469336824. Inputs: standard warranty accrual 130850000.0, revenue 1173510000.0. The ratio holds only the standard warranty accrual. The extended warranty accrual (232924000 at 2026-06-30) is outside it.",
  "account": "standard product warranty accrual (StandardProductWarrantyAccrual)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"position_in_history\": \"second lowest of the 6 filled quarters\"",
  "paragraph_id": "0001437749-26-025669:trends:warranty_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly_cell",
  "what_changed": "insufficient. accruals_over_total_assets is not filled for the quarter because the record has no discrete-quarter operating cash flow. The two operating-cash-flow concepts named in the reason both exist in the record, but not for this period. The Q2 10-Q states a six-month operating cash flow of 240496000, and the 8-K states $121.2 million for the quarter. I do not derive the quarter from them. Across the quarters, only 2 are filled (quarters-back-1 prints 'lowest of the 2 filled quarters'), so no quarterly trend claim is possible.",
  "account": "net income less operating cash flow, over total assets",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-04-01..2026-06-30: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0001437749-26-025669:trends:accruals_over_total_assets:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_quarterly_cell",
  "what_changed": "insufficient. inventory_reserve_ratio is filled in no period of the window, quarter or year. The concept it looks for is not in the record for this date. The 10-K states the inventory reserve under a different concept and member (see the inventory-reserve concept item).",
  "account": "inventory valuation reserve",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"missing\": \"no row for inventory_reserve in 2026-06-30: us-gaap:InventoryValuationReserves is in the record, but not for this period\"",
  "paragraph_id": "0001437749-26-025669:trends:inventory_reserve_ratio:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly_cell",
  "what_changed": "insufficient. The companyfacts record carries no non-GAAP measure, so no gap is computed. The 8-K states adjusted net income of $174 million (0001437749-26-024731:8k_2_02:12) against net income of $143 million (0001437749-26-024731:8k_2_02:11). I do not compute the gap between them.",
  "account": "adjusted net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001437749-26-025669:trends:non_gaap_gap:2026-04-01..2026-06-30" }
```

### Trend table — years-back-0 (2025-01-01..2025-12-31)

Every annual cell prints the quarter-over-quarter reason "an annual period has no preceding quarter". The change given for each is year-over-year, against years-back-1.

```json
{ "id": "earnings_quality_accruals_over_total_assets_annual_cell",
  "what_changed": "accruals_over_total_assets is -0.049953361146201636, the third highest of the 5 filled years. Change against years-back-1: 0.03322504322806967. Inputs: net income 159554000.0, operating cash flow 437978000.0, assets 5573679000.0. The negative sign means operating cash flow exceeded net income in 2025. The 10-K's 2025 cash flow includes an increase in other accrued liabilities of 198722000, and the Zawaski accrual of 206500000 sat in other accrued liabilities at year-end; that accrual was paid in 2026 (see the Zawaski items).",
  "account": "net income less operating cash flow, over total assets",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001437749-26-025669:trends:accruals_over_total_assets:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_annual_cell",
  "what_changed": "bad_debt_reserve_ratio is 0.05414574973754125, the third highest of the 5 filled years. Change against years-back-1: -0.0006203612122836349. Inputs: allowance 34504000.0, receivables 602739000.0.",
  "account": "allowance for doubtful accounts receivable (AllowanceForDoubtfulAccountsReceivableCurrent)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001437749-26-025669:trends:bad_debt_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual_cell",
  "what_changed": "contract_liabilities_over_revenue is 0.03593530945818713, the highest of the 5 filled years. Change against years-back-1: 0.02968320567577841. Inputs: contract liabilities 151257000.0 (taken from the Q2 10-Q 0001437749-26-025669), revenue 4209147000.0. The years-back-1 cell's contract-liability input comes from a different filing (0001437749-25-033048), and the 10-K prints another figure for that same balance date. The annual change may therefore compare figures of different scope. A trend claim is insufficient.",
  "account": "contract liabilities (ContractWithCustomerLiability)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001437749-26-025669:trends:contract_liabilities_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_annual_cell",
  "what_changed": "days_sales_of_inventory is 175.4965350098752, the highest of the 5 filled years. Change against years-back-1: 31.940283184924482. Inputs: inventory 1248867000.0, cost of revenue 2597410000.0. The 10-K shows the build behind it: an increase in inventories of 163117000 in the 2025 cash flow, an inventory valuation reserve of 69266000 at 2025-12-31 against 48173000 a year earlier, and 23375000 charged to the reserve in 2025.",
  "account": "inventory (InventoryNet) against cost of goods sold",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001437749-26-025669:trends:days_sales_of_inventory:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual_cell",
  "what_changed": "days_sales_outstanding is 52.267059097722175, the second highest of the 5 filled years. Change against years-back-1: 0.1162632336361753. Inputs: receivables 602739000.0, revenue 4209147000.0.",
  "account": "accounts receivable (AccountsReceivableNetCurrent) against revenue",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001437749-26-025669:trends:days_sales_outstanding:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_gross_margin_annual_cell",
  "what_changed": "gross_margin is 0.3829129750041992, the second highest of the 5 filled years. Change against years-back-1: -0.0048175564828182305. Inputs: revenue 4209147000.0, cost of revenue 2597410000.0.",
  "account": "gross margin (RevenueFromContractWithCustomerExcludingAssessedTax, CostOfGoodsAndServicesSold)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001437749-26-025669:trends:gross_margin:2025-01-01..2025-12-31" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual_cell",
  "what_changed": "receivables_over_revenue is 0.1431974221855402, the second highest of the 5 filled years. Change against years-back-1: 0.0007089088956877543. Inputs: receivables 602739000.0, revenue 4209147000.0.",
  "account": "accounts receivable (AccountsReceivableNetCurrent) against revenue",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0001437749-26-025669:trends:receivables_over_revenue:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_soft_asset_share_annual_cell",
  "what_changed": "soft_asset_share is 0.7927727807790869, the lowest of the 5 filled years. Change against years-back-1: -0.017124053072546608. Inputs: assets 5573679000.0, cash 341413000.0, property, plant and equipment 813605000.0.",
  "account": "total assets less cash and PP&E, over total assets",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001437749-26-025669:trends:soft_asset_share:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_annual_cell",
  "what_changed": "warranty_reserve_ratio is 0.03134174216296081, the highest of the 5 filled years. Change against years-back-1: 0.005505781089977079. Inputs: standard warranty accrual 131922000.0, revenue 4209147000.0. The 10-K tags a 6794000 increase in estimates for pre-existing standard warranties in 2025.",
  "account": "standard product warranty accrual (StandardProductWarrantyAccrual)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0001437749-26-025669:trends:warranty_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_annual_cell",
  "what_changed": "insufficient. inventory_reserve_ratio is not filled for the year, nor in any other period of the window. The 10-K does state an inventory reserve for 2025-12-31 (69266000), but under ValuationAllowancesAndReservesBalance with InventoryValuationReserveMember, which is not the concept the ratio reads.",
  "account": "inventory valuation reserve",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"missing\": \"no row for inventory_reserve in 2025-12-31: us-gaap:InventoryValuationReserves is in the record, but not for this period\"",
  "paragraph_id": "0001437749-26-025669:trends:inventory_reserve_ratio:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual_cell",
  "what_changed": "insufficient. The companyfacts record carries no non-GAAP measure, so no annual gap is computed.",
  "account": "adjusted net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001437749-26-025669:trends:non_gaap_gap:2025-01-01..2025-12-31" }
```

### Restated prior values: one period, reported differently by an earlier filing

```json
{ "id": "articulation_and_the_filed_history_short_term_debt_rate_refiled",
  "what_changed": "The same concept and date carry two values. The first-quarter 10-Q states the weighted average interest rate on short-term borrowings at 2025-12-31 as 0.13. The 10-K had stated 0.0567 for that date (0001437749-26-004568:facts:ShortTermDebtWeightedAverageInterestRate:2025-12-31). The Q2 10-Q states 0.0615 at 2026-06-30. The input gives no explanation, so whether 0.13 is a restatement or a tagging error does not exist in this record.",
  "account": "short-term borrowings weighted average interest rate (ShortTermDebtWeightedAverageInterestRate)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"0.13\"",
  "paragraph_id": "0001437749-26-014882:facts:ShortTermDebtWeightedAverageInterestRate:2025-12-31" }
```

```json
{ "id": "articulation_and_the_filed_history_allmand_payment_refiled",
  "what_changed": "The 10-K reported the cash paid for Allmand on 2026-01-05 as a subsequent event of 123201000 (0001437749-26-004568:facts:PaymentsToAcquireBusinessesGross:2026-01-05..2026-01-05:us-gaap:BusinessAcquisitionAxis=gnrc:AllmandMember,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember). The first-quarter 10-Q reports 122828000 for the same date, without the subsequent-event member. Same concept and date, different value, slightly different context. Whether this is a purchase-price update or a correction is not stated in the input.",
  "account": "payments to acquire businesses, Allmand (PaymentsToAcquireBusinessesGross)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"122828000\"",
  "paragraph_id": "0001437749-26-014882:facts:PaymentsToAcquireBusinessesGross:2026-01-05..2026-01-05:us-gaap:BusinessAcquisitionAxis=gnrc:AllmandMember" }
```

```json
{ "id": "articulation_and_the_filed_history_contract_liability_prior_year_end_trend_input",
  "what_changed": "The years-back-1 contract_liabilities_over_revenue cell takes contract liabilities at 2024-12-31 as 26858000.0, from filing 0001437749-25-033048. The 10-K 0001437749-26-004568 prints 97821000 for contract liabilities excluding extended warranty at the same date. That cell's value is 0.006252103782408725, the second lowest of the 5 filled years. The years-back-0 cell takes 151257000.0 from the Q2 10-Q. Different filings and contexts feed the two ends of the annual change, so it is insufficient to tell whether they measure the same thing.",
  "account": "contract liabilities (ContractWithCustomerLiability)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": 26858000.0",
  "paragraph_id": "0001437749-26-025669:trends:contract_liabilities_over_revenue:2024-01-01..2024-12-31" }
```

```json
{ "id": "articulation_and_the_filed_history_contract_liability_excluding_extended_warranty",
  "what_changed": "The 10-K tags contract liabilities excluding extended warranty at 2024-12-31 as 97821000. For the same balance date the trend table uses 26858000.0, drawn from 0001437749-25-033048 without a product axis. The record carries two figures for one date, and the input does not say which is like-for-like with the 151257000 used for 2025-12-31.",
  "account": "contract liabilities excluding extended warranty (ContractWithCustomerLiability, ExcludingExtendedWarrantyMember)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"97821000\"",
  "paragraph_id": "0001437749-26-004568:facts:ContractWithCustomerLiability:2024-12-31:srt:ProductOrServiceAxis=gnrc:ExcludingExtendedWarrantyMember" }
```

### Changes of tag, member and scale

```json
{ "id": "structure_and_disclosure_changes_inventory_reserve_concept",
  "what_changed": "The trend table reads us-gaap:InventoryValuationReserves and finds it in no period of the window. The 10-K states the inventory reserve at 2025-12-31 as 69266000 under a different concept and member: ValuationAllowancesAndReservesBalance with InventoryValuationReserveMember. The same schedule gives 48173000 at 2024-12-31 and 23375000 charged in 2025. The trend table does not itself say this period rests on a different concept; this is what the facts show.",
  "account": "inventory valuation reserve",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"69266000\"",
  "paragraph_id": "0001437749-26-004568:facts:ValuationAllowancesAndReservesBalance:2025-12-31:us-gaap:ValuationAllowancesAndReservesTypeAxis=us-gaap:InventoryValuationReserveMember" }
```

```json
{ "id": "structure_and_disclosure_changes_remaining_obligations_member_name",
  "what_changed": "At 2026-06-30 the Q2 10-Q states remaining performance obligations excluding extended warranties as 143000000 (decimals -6), under member gnrc:ExcludingExtendedWarrantiesMember. The 10-K stated 378782000 at 2025-12-31 under gnrc:ExcludingExtendedWarrantyMember, with an expected-timing start date of 2026-01-01. The member name changed between filings, and the 2026-06-30 value is lower than the 2025-12-31 value. The Q2 10-Q also tags 0.80 as a remaining-obligation percentage under the timing start date 2027-07-01.",
  "account": "remaining performance obligations excluding extended warranties (RevenueRemainingPerformanceObligation)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"143000000\"",
  "paragraph_id": "0001437749-26-025669:facts:RevenueRemainingPerformanceObligation:2026-06-30:srt:ProductOrServiceAxis=gnrc:ExcludingExtendedWarrantiesMember" }
```

```json
{ "id": "structure_and_disclosure_changes_extended_warranty_obligation_bucket_scale",
  "what_changed": "The extended-warranty remaining-obligation schedule at 2026-06-30 looks inconsistently scaled. Two timing buckets carry decimals INF and values in the tens of thousands: start 2026-07-01 at 21376, and start 2030-07-01 at 28940. The other buckets are in the tens of millions (43980000, 42922000, 36437000, 59269000), as is the total (232924000). The two small buckets look like thousands tagged as dollars. I do not add the buckets, so whether the schedule foots as tagged does not exist in my input.",
  "account": "remaining performance obligations, extended warranties (RevenueRemainingPerformanceObligation, ExtendedWarrantiesMember)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"21376\"",
  "paragraph_id": "0001437749-26-025669:facts:RevenueRemainingPerformanceObligation:2026-06-30:srt:ProductOrServiceAxis=gnrc:ExtendedWarrantiesMember,us-gaap:RevenueRemainingPerformanceObligationExpectedTimingOfSatisfactionStartDateAxis=2026-07-01" }
```

```json
{ "id": "structure_and_disclosure_changes_antidilutive_share_scale",
  "what_changed": "The Q2 10-Q tags antidilutive securities excluded from diluted EPS (all with decimals -6) as: 124000000 shares for the quarter, 123000000 for the six months, 779000000 for the prior-year quarter and 428000000 for the prior-year six months. The same filing prints weighted basic shares of 58822634 for the quarter. Earlier filings used another scale: the 10-K tagged 300000 for 2025, and the Q1 10-Q tagged 178000 (decimals INF) for its quarter. The Q2 values look scaled differently from earlier filings. Diluted EPS itself (2.4) agrees with the 8-K's $2.40.",
  "account": "antidilutive securities excluded from EPS (AntidilutiveSecuritiesExcludedFromComputationOfEarningsPerShareAmount)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"124000000\"",
  "paragraph_id": "0001437749-26-025669:facts:AntidilutiveSecuritiesExcludedFromComputationOfEarningsPerShareAmount:2026-04-01..2026-06-30" }
```

```json
{ "id": "structure_and_disclosure_changes_program_repurchase_share_scale",
  "what_changed": "The Q2 10-Q tags shares repurchased under the program in the prior-year quarter as 392521000 (decimals -3), and 1109206000 for the prior-year six months. The same filing's treasury-share fact for that quarter without the program axis prints 392521 (0001437749-26-025669:facts:TreasuryStockSharesAcquired:2025-04-01..2025-06-30:us-gaap:StatementEquityComponentsAxis=us-gaap:TreasuryStockCommonMember). Weighted basic shares for that quarter were 58496998. The program-axis share counts look mis-scaled. The cost is tagged at 50463000 for that quarter.",
  "account": "treasury shares acquired under the repurchase program (TreasuryStockSharesAcquired)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"392521000\"",
  "paragraph_id": "0001437749-26-025669:facts:TreasuryStockSharesAcquired:2025-04-01..2025-06-30:srt:ShareRepurchaseProgramAxis=gnrc:StockRepurchaseProgramMember,us-gaap:StatementEquityComponentsAxis=us-gaap:TreasuryStockCommonMember" }
```

```json
{ "id": "structure_and_disclosure_changes_repurchase_authorization_date",
  "what_changed": "The Q2 10-Q dates a remaining repurchase authorization of 199340000 at 2026-02-09. The Q1 10-Q printed the same amount dated 2024-02-12 (0001437749-26-014882:facts:StockRepurchaseProgramRemainingAuthorizedRepurchaseAmount1:2024-02-12). Same amount, different context date. The input does not say whether a new program replaced the old one or the date was corrected.",
  "account": "stock repurchase program remaining authorization (StockRepurchaseProgramRemainingAuthorizedRepurchaseAmount1)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"199340000\"",
  "paragraph_id": "0001437749-26-025669:facts:StockRepurchaseProgramRemainingAuthorizedRepurchaseAmount1:2026-02-09" }
```

```json
{ "id": "structure_and_disclosure_changes_goodwill_acquired",
  "what_changed": "Goodwill acquired in the six months is tagged 208598000. The deals behind it: the 10-K and Q1 10-Q record the Allmand payment in January 2026, and the Q1 10-Q records the Enercon acquisition on 2026-04-01 as a subsequent event (consideration 122322000). The 8-K says Enercon closed during the quarter (0001437749-26-024731:8k_2_02:18). Purchase accounting in its first period is a place where estimates are set; the input does not show the allocation.",
  "account": "goodwill acquired (GoodwillAcquiredDuringPeriod)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"208598000\"",
  "paragraph_id": "0001437749-26-025669:facts:GoodwillAcquiredDuringPeriod:2026-01-01..2026-06-30" }
```

### Numeric facts

```json
{ "id": "related_parties_contingencies_and_subsequent_events_zawaski_accrual_paid",
  "what_changed": "Payments against the Zawaski accrual in the six months are tagged 206500000. That equals the accrual the 10-K carried at 2025-12-31 in other accrued liabilities. The Q2 10-Q still shows the accrual at 206500000 at 2026-03-31 (0001437749-26-025669:facts:LossContingencyAccrualAtCarryingValue:2026-03-31:srt:LitigationCaseAxis=gnrc:ZawaskiEtAlVGeneralPowerSystemsIncEtAlMember), which places the payment after that date.",
  "account": "loss contingency accrual payments, Zawaski et al. (LossContingencyAccrualPayments)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"206500000\"",
  "paragraph_id": "0001437749-26-025669:facts:LossContingencyAccrualPayments:2026-01-01..2026-06-30:srt:LitigationCaseAxis=gnrc:ZawaskiEtAlVGeneralPowerSystemsIncEtAlMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_zawaski_accrual_year_end",
  "what_changed": "The 10-K carried the Zawaski accrual at 2025-12-31 as 206500000 within other accrued liabilities, with an insurance receivable of 102000000 in prepaid expenses and other current assets (0001437749-26-004568:facts:InsuranceSettlementsReceivable:2025-12-31:srt:LitigationCaseAxis=gnrc:ZawaskiEtAlVGeneralPowerSystemsIncEtAlMember,us-gaap:BalanceSheetLocationAxis=us-gaap:PrepaidExpensesAndOtherCurrentAssetsMember).",
  "account": "loss contingency accrual, Zawaski et al. (LossContingencyAccrualAtCarryingValue)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"206500000\"",
  "paragraph_id": "0001437749-26-004568:facts:LossContingencyAccrualAtCarryingValue:2025-12-31:srt:LitigationCaseAxis=gnrc:ZawaskiEtAlVGeneralPowerSystemsIncEtAlMember,us-gaap:BalanceSheetLocationAxis=gnrc:OtherAccruedLiabilitiesMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_zawaski_insurance_receivable",
  "what_changed": "The insurance receivable against the Zawaski matter is 102000000 at 2026-03-31, the same figure as at 2025-12-31 in the 10-K. I found no 2026-06-30 value for it in the facts I read. Whether it was collected in the quarter therefore does not exist in my input.",
  "account": "insurance settlements receivable, Zawaski et al. (InsuranceSettlementsReceivable)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"102000000\"",
  "paragraph_id": "0001437749-26-025669:facts:InsuranceSettlementsReceivable:2026-03-31:srt:LitigationCaseAxis=gnrc:ZawaskiEtAlVGeneralPowerSystemsIncEtAlMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_portable_generator_legal_fees",
  "what_changed": "The 10-K tags legal fees of 104500000 for the portable-generator product-liability case in the fourth quarter of 2025. The 8-K says the quarter's operating expenses rose by $6.4 million, partly offset by lower legal expenses in the current year (0001437749-26-024731:8k_2_02:23). The input has no current-quarter legal-fee fact for this case.",
  "account": "legal fees, portable generator product liability (LegalFees)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"104500000\"",
  "paragraph_id": "0001437749-26-004568:facts:LegalFees:2025-10-01..2025-12-31:srt:LitigationCaseAxis=gnrc:PortableGeneratorProductLiabilityCaseMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_enercon_consideration",
  "what_changed": "As a subsequent event, the Q1 10-Q tags consideration transferred for Enercon on 2026-04-01 as 122322000. It also tags the high end of the contingent-consideration range as 112043000 (0001437749-26-014882:facts:BusinessCombinationContingentConsiderationArrangementsRangeOfOutcomesValueHigh:2026-04-01:us-gaap:BusinessAcquisitionAxis=gnrc:EnerconEngineeringIncMember,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember).",
  "account": "business combination consideration, Enercon (BusinessCombinationConsiderationTransferred1)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"122322000\"",
  "paragraph_id": "0001437749-26-014882:facts:BusinessCombinationConsiderationTransferred1:2026-04-01..2026-04-01:us-gaap:BusinessAcquisitionAxis=gnrc:EnerconEngineeringIncMember,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember" }
```

```json
{ "id": "estimates_and_discretion_contingent_consideration_liability",
  "what_changed": "The contingent consideration liability at 2026-06-30 is tagged 121866000, a figure above the Enercon high-end outcome of 112043000 that the Q1 10-Q disclosed. The liability fact is not split by acquisition, so how much of it belongs to Enercon does not exist in my input. Remeasurement of this liability runs through earnings.",
  "account": "business combination contingent consideration liability (BusinessCombinationContingentConsiderationLiability)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"121866000\"",
  "paragraph_id": "0001437749-26-025669:facts:BusinessCombinationContingentConsiderationLiability:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_other_accrued_liabilities_balance",
  "what_changed": "Other accrued liabilities are 447770000 at 2026-06-30. The 10-K stated 591387000 at 2025-12-31 (0001437749-26-004568:facts:OtherAccruedLiabilitiesCurrent:2025-12-31). The year-end balance held the Zawaski accrual of 206500000, which was paid in the six months.",
  "account": "other accrued liabilities (OtherAccruedLiabilitiesCurrent)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"447770000\"",
  "paragraph_id": "0001437749-26-025669:facts:OtherAccruedLiabilitiesCurrent:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_other_accrued_liabilities_cash_flow_change",
  "what_changed": "The six-month cash-flow change in other accrued liabilities is -110996000. The 10-K's 2025 figure was an increase of 198722000.",
  "account": "increase/decrease in other accrued liabilities (IncreaseDecreaseInOtherAccruedLiabilities)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"-110996000\"",
  "paragraph_id": "0001437749-26-025669:facts:IncreaseDecreaseInOtherAccruedLiabilities:2026-01-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_operating_cash_flow_cumulative",
  "what_changed": "Operating cash flow for the six months is 240496000. The record holds no discrete-quarter figure (see the quarterly accruals item). The 8-K states $121.2 million for the quarter and attributes part of the cash to tariff-refund receipts (0001437749-26-024731:8k_2_02:25). I do not derive the quarter from the six-month and first-quarter figures.",
  "account": "net cash provided by operating activities (NetCashProvidedByUsedInOperatingActivities)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"240496000\"",
  "paragraph_id": "0001437749-26-025669:facts:NetCashProvidedByUsedInOperatingActivities:2026-01-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_other_operating_assets_change",
  "what_changed": "The six-month cash-flow change in other operating assets is tagged 105336000. The input does not say what the assets are; in particular, no tariff-refund receivable is separately tagged in what I read.",
  "account": "increase/decrease in other operating assets (IncreaseDecreaseInOtherOperatingAssets)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"105336000\"",
  "paragraph_id": "0001437749-26-025669:facts:IncreaseDecreaseInOtherOperatingAssets:2026-01-01..2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_short_term_debt_rate_current",
  "what_changed": "The weighted average rate on short-term borrowings is 0.0615 at 2026-06-30. The 2025-12-31 comparative is 0.0567 in the 10-K and 0.13 in the Q1 10-Q (see the restated item). Short-term borrowings are 48318000 at 2026-06-30 against 50618000 at 2025-12-31.",
  "account": "short-term borrowings weighted average interest rate (ShortTermDebtWeightedAverageInterestRate)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"0.0615\"",
  "paragraph_id": "0001437749-26-025669:facts:ShortTermDebtWeightedAverageInterestRate:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_revolver_remaining_capacity",
  "what_changed": "Remaining revolver capacity is 999250000 at 2026-06-30, the same figure the 10-K stated at 2025-12-31. The revolver line of credit is 0 at 2026-06-30. Term loan A carries 700000000 at both dates; term loan B carries 491250000 against 493750000.",
  "account": "revolving credit facility remaining borrowing capacity (LineOfCreditFacilityRemainingBorrowingCapacity)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"999250000\"",
  "paragraph_id": "0001437749-26-025669:facts:LineOfCreditFacilityRemainingBorrowingCapacity:2026-06-30:us-gaap:CreditFacilityAxis=us-gaap:RevolvingCreditFacilityMember" }
```

```json
{ "id": "liquidity_and_capital_current_portion_long_term_debt",
  "what_changed": "The current portion of long-term debt is 21277000 at 2026-06-30, against 12729000 at 2025-12-31 (0001437749-26-025669:facts:LongTermDebtCurrent:2025-12-31). Total debt and finance lease obligations are 1281010000 against 1282448000.",
  "account": "long-term debt, current (LongTermDebtCurrent)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"21277000\"",
  "paragraph_id": "0001437749-26-025669:facts:LongTermDebtCurrent:2026-06-30" }
```

```json
{ "id": "liquidity_and_capital_no_program_repurchases",
  "what_changed": "No shares were repurchased under the program in the quarter: the fact is 0. The prior-year quarter's program cost is tagged 50463000 (its share count is mis-scaled; see the structure item).",
  "account": "treasury shares acquired under the repurchase program (TreasuryStockSharesAcquired)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"0\"",
  "paragraph_id": "0001437749-26-025669:facts:TreasuryStockSharesAcquired:2026-04-01..2026-06-30:srt:ShareRepurchaseProgramAxis=gnrc:StockRepurchaseProgramMember,us-gaap:StatementEquityComponentsAxis=us-gaap:TreasuryStockCommonMember" }
```

```json
{ "id": "earnings_quality_net_income_reported",
  "what_changed": "Net income for the quarter is 143244000, against 74016000 in the prior-year quarter. Six-month net income is 216497000, against 117856000. Diluted EPS is 2.4 against 1.25. The 8-K states that net income includes a pre-tax impact of approximately $71 million from tariff refunds recorded in the quarter (0001437749-26-024731:8k_2_02:14). No filed fact in my input isolates that refund, so the quarter's net income without it does not exist in the input.",
  "account": "net income (NetIncomeLoss)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"143244000\"",
  "paragraph_id": "0001437749-26-025669:facts:NetIncomeLoss:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_effective_tax_rate_cumulative",
  "what_changed": "The Q2 10-Q tags an effective tax rate of 0.246 to the six-month period, with a prior-year six-month comparative of 0.20. The 10-K's 2025 rate is 0.189. The 8-K gives 24.6% for the quarter and 17.2% for the prior-year quarter (0001437749-26-024731:8k_2_02:24). Whether the six-month tag and the release's quarterly 24.6% are the same figure under different contexts cannot be told from this input: insufficient.",
  "account": "effective income tax rate (EffectiveIncomeTaxRateContinuingOperations)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"0.246\"",
  "paragraph_id": "0001437749-26-025669:facts:EffectiveIncomeTaxRateContinuingOperations:2026-01-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_loss_on_sale_of_businesses",
  "what_changed": "The loss on sale of businesses in the quarter is tagged -13456000. The 8-K footnote says the current-year loss relates primarily to four immaterial business dispositions, two closing in the first quarter and two in the second (0001437749-26-024731:8k_2_02:129). Goodwill written off on these sales in the six months is 15943000.",
  "account": "gain/loss on sale of business (GainLossOnSaleOfBusiness)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"-13456000\"",
  "paragraph_id": "0001437749-26-025669:facts:GainLossOnSaleOfBusiness:2026-04-01..2026-06-30" }
```

```json
{ "id": "earnings_quality_goodwill_written_off_on_disposals",
  "what_changed": "Goodwill written off on the sale of business units in the six months is 15943000. It relates to the dispositions the 8-K calls immaterial.",
  "account": "goodwill written off on sale of business units (GoodwillWrittenOffRelatedToSaleOfBusinessUnit)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"15943000\"",
  "paragraph_id": "0001437749-26-025669:facts:GoodwillWrittenOffRelatedToSaleOfBusinessUnit:2026-01-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_goodwill_impairment_residential",
  "what_changed": "Goodwill impairment for the six months is 1523000. The Q1 10-Q tags the same amount to the Residential segment for the first quarter (0001437749-26-014882:facts:GoodwillImpairmentLoss:2026-01-01..2026-03-31:us-gaap:StatementBusinessSegmentsAxis=gnrc:ResidentialSegmentMember). The 10-K states accumulated goodwill impairment of 507804000 at 2025-12-31.",
  "account": "goodwill impairment (GoodwillImpairmentLoss)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"1523000\"",
  "paragraph_id": "0001437749-26-025669:facts:GoodwillImpairmentLoss:2026-01-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_charge",
  "what_changed": "The 10-K tags 23375000 charged to the inventory valuation reserve in 2025. The reserve stood at 69266000 at 2025-12-31 against 48173000 a year earlier. No reserve figure for 2026 exists in my input.",
  "account": "inventory valuation reserve charged to cost and expense (ValuationAllowancesAndReservesChargedToCostAndExpense)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"23375000\"",
  "paragraph_id": "0001437749-26-004568:facts:ValuationAllowancesAndReservesChargedToCostAndExpense:2025-01-01..2025-12-31:us-gaap:ValuationAllowancesAndReservesTypeAxis=us-gaap:InventoryValuationReserveMember" }
```

```json
{ "id": "earnings_quality_inventory_build_cash_flow",
  "what_changed": "The 10-K's 2025 cash flow tags an increase in inventories of 163117000. That is the build behind the annual days_sales_of_inventory being the highest of the 5 filled years.",
  "account": "increase/decrease in inventories (IncreaseDecreaseInInventories)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"163117000\"",
  "paragraph_id": "0001437749-26-004568:facts:IncreaseDecreaseInInventories:2025-01-01..2025-12-31" }
```

```json
{ "id": "earnings_quality_other_accrued_liabilities_build_cash_flow",
  "what_changed": "The 10-K's 2025 cash flow tags an increase in other accrued liabilities of 198722000. The year-end balance of other accrued liabilities held the Zawaski accrual of 206500000, which was paid in the first six months of 2026. Operating cash flow in 2025 carried the accrual; operating cash flow in 2026 carries the payment.",
  "account": "increase/decrease in other accrued liabilities (IncreaseDecreaseInOtherAccruedLiabilities)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"198722000\"",
  "paragraph_id": "0001437749-26-004568:facts:IncreaseDecreaseInOtherAccruedLiabilities:2025-01-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_standard_warranty_prior_estimate_change",
  "what_changed": "Changes in estimates for pre-existing standard warranties in the quarter are tagged 2582000; the 10-K tagged 6794000 for all of 2025. A positive value means earlier estimates were raised. The standard warranty accrual is 130850000 at 2026-06-30 against 131922000 at 2025-12-31.",
  "account": "standard product warranty, pre-existing estimate changes (StandardProductWarrantyAccrualPreexistingIncreaseDecrease)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"2582000\"",
  "paragraph_id": "0001437749-26-025669:facts:StandardProductWarrantyAccrualPreexistingIncreaseDecrease:2026-04-01..2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_extended_warranty_accrual",
  "what_changed": "The extended warranty accrual is 232924000 at 2026-06-30, against 219404000 at 2025-12-31 and 202650000 at 2025-06-30. Extended warranties issued in the quarter are 16253000, against 16915000 in the prior-year quarter. No trend ratio includes this accrual. With three balance dates, a trend claim is insufficient.",
  "account": "extended product warranty accrual (ExtendedProductWarrantyAccrual)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"232924000\"",
  "paragraph_id": "0001437749-26-025669:facts:ExtendedProductWarrantyAccrual:2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_assets_balance",
  "what_changed": "Contract assets are 78730000 at 2026-06-30, against 8867000 at 2025-12-31 (0001437749-26-025669:facts:ContractWithCustomerAssetNet:2025-12-31). A higher contract-asset balance means more revenue recognized ahead of billing. The input does not tie these assets to any contract. With two balance dates, a trend claim is insufficient.",
  "account": "contract assets (ContractWithCustomerAssetNet)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"78730000\"",
  "paragraph_id": "0001437749-26-025669:facts:ContractWithCustomerAssetNet:2026-06-30" }
```

```json
{ "id": "revenue_recognition_contract_liability_revenue_recognized",
  "what_changed": "Revenue recognized in the six months from contract liabilities is tagged 90360000; the 10-K tagged 61299000 for all of 2025. The contract-liability balance is 117918000 at 2026-06-30 against 151257000 at 2025-12-31.",
  "account": "revenue recognized from contract liabilities (ContractWithCustomerLiabilityRevenueRecognized)",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "\"value\": \"90360000\"",
  "paragraph_id": "0001437749-26-025669:facts:ContractWithCustomerLiabilityRevenueRecognized:2026-01-01..2026-06-30" }
```

### Earnings-release figures against the filed numbers

```json
{ "id": "across_documents_net_income_release_agreement",
  "what_changed": "The release's net income of $143 million and $2.40 per diluted share agree with the 10-Q facts: NetIncomeLoss 143244000 and EarningsPerShareDiluted 2.4. The prior-year $74 million and $1.25 agree with 74016000 and 1.25. The input shows no gap between the release and the filing on these lines.",
  "account": "net income and diluted EPS",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "Net income attributable to the Company during the second quarter was $143 million, or $2.40 per share, as compared to $74 million, or $1.25 per share, for the same period of 2025.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:11" }
```

```json
{ "id": "across_documents_tariff_refund_in_net_income",
  "what_changed": "The release says the quarter's net income, adjusted net income and adjusted EBITDA each include a pre-tax tariff-refund impact of approximately $71 million, recorded in the quarter. No fact in the filed record I read isolates the refund. The release ties it to this quarter, so the earnings lines it lifts are expected to lose it next quarter unless another refund is recorded.",
  "account": "tariff refunds within cost of goods sold and net income",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "Net income, adjusted net income, and adjusted EBITDA all include a pre-tax impact of approximately $71 million related to tariff refunds that were recorded during the current year quarter.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:14" }
```

```json
{ "id": "across_documents_gross_margin_tariff_contribution",
  "what_changed": "The release gives 44.5% gross margin for the quarter against 39.3%. It says tariff refunds contributed approximately 6% of it, with unfavorable mix and higher input costs partly offset by price. The trend cell prints 0.444658332694225 for the same quarter, the highest of the 6 filled quarters.",
  "account": "gross margin",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "The increase was primarily driven by tariff refunds which contributed approximately 6% to gross margin during the quarter.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:22" }
```

```json
{ "id": "across_documents_residential_margin_tariff_contribution",
  "what_changed": "The release gives Residential adjusted EBITDA of $215.4 million, or 34.7% of segment sales, against 23.1%. It says tariff refunds account for approximately 9% of the margin. The input has no filed segment-margin fact to set against it.",
  "account": "Residential segment adjusted EBITDA margin",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "This increase was primarily driven by tariff refunds which impacted margins by approximately 9%, as well as favorable sales mix and operational efficiencies resulting in lower operating expenses.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:32" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_residential_sales_decline",
  "what_changed": "Per the release, Residential segment sales fell by about 2%, to $621.3 million from $634.7 million, on lower energy storage and portable generator shipments. Home standby growth mostly offset the decline. The release still projects Residential sales up in the high-single digits for the year (0001437749-26-024731:8k_2_02:35). The input has no filed segment-sales fact.",
  "account": "Residential segment sales",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "Residential segment total sales decreased approximately 2% to $621.3 million as compared to $634.7 million in the prior year quarter.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:31" }
```

```json
{ "id": "results_against_expectations_guidance_raise_rests_on_tariff_refund",
  "what_changed": "The release raises full-year 2026 net income margin guidance to 9.0 to 10.0% (from 8.0 to 9.0%) and adjusted EBITDA margin guidance to 20.0 to 21.0% (from 18.5 to 19.5%). It keeps sales growth guidance at mid-to-high teens (0001437749-26-024731:8k_2_02:19). It attributes the raise primarily to the second-quarter tariff refund, an approximate 1.5% full-year impact. The input holds no consensus or prior-expectation figure.",
  "account": "full-year margin guidance",
  "expected_direction": "none",
  "horizon": "full year 2026",
  "quote": "This increased outlook is primarily due to the tariff refund included in the second quarter, which is expected to have an approximate 1.5% impact for the full year 2026.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:36" }
```

```json
{ "id": "across_documents_effective_tax_rate_release",
  "what_changed": "The release gives a quarterly tax provision of $46.7 million at 24.6%, against $15.4 million at 17.2%, and attributes the rise to a non-recurring favorable discrete item in the prior-year period. The filed fact 0.246 is tagged to the six-month period, with a six-month prior-year comparative of 0.20. It is insufficient to say whether the two sources describe the same period.",
  "account": "effective income tax rate",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "Provision for income taxes for the current year quarter was $46.7 million, or an effective tax rate of 24.6%, as compared to $15.4 million, or a 17.2% effective tax rate, for the prior year.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:24" }
```

```json
{ "id": "across_documents_operating_cash_flow_release",
  "what_changed": "The release gives quarterly operating cash flow of $121.2 million against $72.2 million, and free cash flow of $62.9 million against $14.5 million. It attributes the rise partly to cash receipts from tariff refunds. The companyfacts record has no discrete-quarter operating cash flow, only the six-month 240496000, so the release's quarterly figure has no filed fact to match. The Zawaski payment of 206500000 falls after 2026-03-31, and the input does not reconcile it with the quarter's cash flow.",
  "account": "operating cash flow and free cash flow",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "This strong increase in free cash flow during the quarter was primarily driven by higher operating earnings, including cash receipts from tariff refunds.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:25" }
```

```json
{ "id": "across_documents_data_center_backlog_against_obligations",
  "what_changed": "The release puts data-center backlog at approximately $1.6 billion as of its date. It separately says nearly $700 million of 2027 volume was committed under the first hyperscale agreement (0001437749-26-024731:8k_2_02:16). The 10-Q tags remaining performance obligations excluding extended warranties as 143000000 at 2026-06-30, lower than the 10-K's 378782000 at 2025-12-31. Backlog and remaining performance obligations are different measures, and the input does not reconcile them.",
  "account": "backlog against remaining performance obligations",
  "expected_direction": "none",
  "horizon": "none",
  "quote": "In total, our backlog for products serving the data center market has now increased to approximately $1.6 billion as of today, which does not include any committed volumes from the second hyperscale customer.",
  "paragraph_id": "0001437749-26-024731:8k_2_02:20" }
```

## Seen in the notes

No fact in input_numbers.json carries a marker saying whether its element sat inside a note when it was extracted. Each fact prints only id, paragraph_id, tag, prefix, namespace, context, context_ref, unit, decimals, value, number, nil, form, source_accession and filing_date. So no finding can be sorted here from the input's own marking. I have not made that judgement myself, and this section holds no items.
