# report_numbers.md

**Run check.** My input directory holds exactly four files: `input_numbers.json`, `input_trends.json`, `input_8k.md`, `input_prior_predictions.md`. No prices, abnormal returns, short interest, other companies' files or outcome-window material are present — the run is clean on that count. Three inputs named in my task are *not* in the directory and I therefore read none of them: the articulation checks, the restatement traces, and the fourth-quarter derivation. Everything below comes from the trend table, the formula baselines' inputs inside it, the numeric facts, and the 8-K earnings release. Prior flags: `None on record. This company has no earlier run under the given run root, so there are no flags, no management explanations and no outcomes to carry forward.`

Triggering filing: 10-Q, accession 0001045810-26-000075, filed 2026-08-26, quarter ended 2026-07-26 (Q-0). Cutoff 2026-08-26.

## Seen in the statements

```json
{ "id": "days-sales-outstanding-jumped-in-the-filing-quarter",
  "what_changed": "Days sales outstanding for the quarter ended 2026-07-26 is 59.64 days, a quarter-over-quarter change of +14.25 days against Q-1. The ratio rests on receivables of 63,059,000,000 (us-gaap:AccountsReceivableNetCurrent, fact 0001045810-26-000075:f-116) over revenue of 96,221,000,000. Receivables grew faster than the revenue they sit against.",
  "account": "accounts receivable, net (current)",
  "expected_direction": "up",
  "horizon": "next quarterly report, Q3 fiscal 2027",
  "quote": "\"change\": 14.246098482915471",
  "paragraph_id": "0001045810-26-000075:trends:days_sales_outstanding:Q-0" }
```

```json
{ "id": "receivables-consumed-cash-in-the-quarter",
  "what_changed": "The condensed consolidated statement of cash flows in the earnings release shows the change in accounts receivable as (22,346) for the three months ended July 26, 2026 against (5,675) for the three months ended July 27, 2025. The company's own first-reported statement corroborates the receivables build seen in the trend table.",
  "account": "accounts receivable (operating cash flow line)",
  "expected_direction": "up",
  "horizon": "next quarterly report, Q3 fiscal 2027",
  "quote": "| Accounts receivable | (22,346) |  |  | (5,675) |  |  | (24,590) |  |  | (4,743) |  |",
  "paragraph_id": "0001045810-26-000073:8k_2_02:71" }
```

```json
{ "id": "operating-cash-flow-below-net-income-for-the-quarter",
  "what_changed": "For the three months ended July 26, 2026 the release prints net cash provided by operating activities of 24,077 and, in the same statement, net income of 59,688; a year earlier the same two lines read 15,365 and 26,422. Operating cash is the smaller of the two figures in the current quarter by a wider margin than in the comparative quarter. The trend table could not compute accruals over total assets for this period, so this printed pair is the only accrual-quality evidence in my input.",
  "account": "net cash provided by operating activities",
  "expected_direction": "down",
  "horizon": "next quarterly report, Q3 fiscal 2027",
  "quote": "| Net cash provided by operating activities | 24,077 |  |  | 15,365 |  |  | 74,421 |  |  | 42,779 |  |",
  "paragraph_id": "0001045810-26-000073:8k_2_02:71" }
```

```json
{ "id": "inventory-days-rose-quarter-over-quarter",
  "what_changed": "Days sales of inventory for the quarter ended 2026-07-26 is 119.33 days, a quarter-over-quarter change of +4.58 days against Q-1. The ratio rests on inventory of 31,575,000,000 (us-gaap:InventoryNet, fact 0001045810-26-000075:f-635) over cost of revenue of 24,079,000,000.",
  "account": "inventories, net",
  "expected_direction": "up",
  "horizon": "next quarterly report, Q3 fiscal 2027",
  "quote": "\"change\": 4.58047653175197",
  "paragraph_id": "0001045810-26-000075:trends:days_sales_of_inventory:Q-0" }
```

```json
{ "id": "contract-liabilities-grew-faster-than-revenue",
  "what_changed": "Contract liabilities over revenue for the quarter ended 2026-07-26 is 0.0480, a quarter-over-quarter change of +0.0270 against Q-1. The ratio rests on contract liabilities of 4,616,000,000 (us-gaap:ContractWithCustomerLiabilityCurrent, fact 0001045810-26-000075:f-648) over revenue of 96,221,000,000. More revenue is being deferred relative to revenue recognized than in the prior quarter.",
  "account": "contract with customer liability, current",
  "expected_direction": "up",
  "horizon": "next quarterly report, Q3 fiscal 2027",
  "quote": "\"change\": 0.02697185425440342",
  "paragraph_id": "0001045810-26-000075:trends:contract_liabilities_over_revenue:Q-0" }
```

```json
{ "id": "contract-liabilities-tagged-under-two-different-elements",
  "what_changed": "The same economic line is carried by us-gaap:ContractWithCustomerLiabilityCurrent in Q-0 and Q-1 but by us-gaap:ContractWithCustomerLiability in Q-4 and Q-5, so the trend table refuses the year-over-year comparison for contract liabilities over revenue in every quarter where it would be available. The same element switch blocks the FY-1 against FY-2 comparison. This is a tagging inconsistency across periods, not a movement in the account.",
  "account": "contract with customer liability (element consistency)",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"tag\": \"ContractWithCustomerLiability\"",
  "paragraph_id": "0001045810-26-000075:trends:contract_liabilities_over_revenue:Q-4" }
```

```json
{ "id": "warranty-reserve-ratio-fell-in-both-available-comparisons",
  "what_changed": "Warranty accrual over revenue for the quarter ended 2026-07-26 is 0.03053, a year-over-year change of -0.01533 against Q-4 and a quarter-over-quarter change of -0.00559 against Q-1. The accrual balance itself rose in dollars over the same span (2,144,000,000 in Q-4, 2,948,000,000 in Q-1, 2,938,000,000 in Q-0), so the ratio fell because revenue rose faster than the accrual, not because the accrual was released. The annual rows use annual revenue against a point-in-time accrual and are not comparable to the quarterly rows; I read only the quarterly series here.",
  "account": "product warranty accrual relative to revenue",
  "expected_direction": "down",
  "horizon": "next quarterly report, Q3 fiscal 2027",
  "quote": "\"change\": -0.015333955335689615",
  "paragraph_id": "0001045810-26-000075:trends:warranty_reserve_ratio:Q-0" }
```

```json
{ "id": "gross-margin-flat-quarter-over-quarter",
  "what_changed": "Gross margin for the quarter ended 2026-07-26 is 0.74975, a quarter-over-quarter change of +0.00042 against Q-1 and a year-over-year change of +0.02552 against Q-4. The earnings release prints the same movement independently as 0.1 pts quarter over quarter and 2.6 pts year over year, so the computed row and the first-reported figure agree in sign. Margin is not where the movement is this quarter.",
  "account": "gross margin",
  "expected_direction": "none",
  "horizon": "next quarterly report, Q3 fiscal 2027",
  "quote": "| Gross margin | 75.0 | % | 74.9 | % | 72.4 | % | 0.1 pts | 2.6 pts |",
  "paragraph_id": "0001045810-26-000073:8k_2_02:11" }
```

```json
{ "id": "accrual-ratio-not-computable-for-the-filing-quarter",
  "what_changed": "Insufficient. Accruals over total assets is not filled for the quarter ended 2026-07-26 because no operating cash flow fact exists for the three months 2026-04-27 to 2026-07-26 in the instance; the tag is reported, but only for the six-month period. The same ratio is also missing in Q-4 and Q-5, leaving it filled in only three of the thirteen periods requested. No accrual-ratio trend claim is supported by this input.",
  "account": "accruals over total assets",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"missing\": \"no fact for operating_cash_flow in 2026-04-27..2026-07-26: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is reported, but not for this period\"",
  "paragraph_id": "0001045810-26-000075:trends:accruals_over_total_assets:Q-0" }
```

```json
{ "id": "no-receivables-allowance-tagged-in-any-period",
  "what_changed": "Insufficient. The bad debt reserve ratio is filled in zero of the thirteen periods requested: none of the three filings tags an allowance for credit losses on receivables under any of the three concepts searched. Receivables of 63,059,000,000 sit on the balance sheet at 2026-07-26 with no tagged allowance anywhere in my input, so I can say nothing about reserve adequacy on receivables in either direction.",
  "account": "allowance for credit losses on accounts receivable",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"missing\": \"no fact for bad_debt_allowance: the filings tag none of us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable\"",
  "paragraph_id": "0001045810-26-000075:trends:bad_debt_reserve_ratio:Q-0" }
```

```json
{ "id": "no-inventory-valuation-reserve-tagged-in-any-period",
  "what_changed": "Insufficient. The inventory reserve ratio is filled in zero of the thirteen periods requested: us-gaap:InventoryValuationReserves is tagged in none of the three filings. Inventory days are rising, but no reserve figure exists in my input to set against the inventory balance, so no claim about inventory reserve adequacy is supported.",
  "account": "inventory valuation reserves",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"missing\": \"no fact for inventory_reserve: the filings tag none of us-gaap:InventoryValuationReserves\"",
  "paragraph_id": "0001045810-26-000075:trends:inventory_reserve_ratio:Q-0" }
```

```json
{ "id": "quarterly-history-has-four-of-eight-quarters",
  "what_changed": "Insufficient, and it qualifies every quarterly item above. Of the eight quarters requested, Q-2, Q-3, Q-6 and Q-7 are absent because no period ends within twenty days of their target dates in the numeric facts; of the five years requested, FY-3 and FY-4 are absent for the same reason. Receivables over revenue, days sales outstanding, days sales of inventory and soft asset share are each filled in only four of thirteen periods, and only two of those four are quarters. Every quarter-over-quarter change I report is therefore a two-point comparison between Q-0 and Q-1, not a trend.",
  "account": "period coverage",
  "expected_direction": "none",
  "horizon": "not applicable",
  "quote": "\"reason\": \"no period ending within 20 days of 2026-01-25 is in input_numbers.json\"",
  "paragraph_id": "0001045810-26-000075:trends:coverage:Q-2" }
```

## Seen in the notes

Insufficient — no items, and this is a result rather than an omission.

My task says each numeric fact is marked with whether its element sat inside a note when it was extracted, and that I do not have to judge which those are. That marker does not exist in `input_numbers.json` as delivered. Every fact object in the file carries exactly these keys and no others: `id`, `tag`, `prefix`, `namespace`, `context`, `context_ref`, `unit`, `decimals`, `value`, `number`, `nil`, `form`, `source_accession`, `filing_date`. I sampled facts from all three accessions and across the file, including the warranty-accrual and fair-value blocks that would sit inside notes in the filed document, and found no note flag on any of them.

Several of the accounts I report above — the product warranty accrual, the contract with customer liability, the concentration percentages — are the kind of element that is normally presented in a note rather than on the face of a statement. I am not assigning them to this heading on that basis, because doing so would be me judging which findings came from where, which is exactly what the marker exists to prevent and exactly what the later split must not have to re-derive. If the marker is restored upstream, these items should be re-sorted then, not guessed at now.
