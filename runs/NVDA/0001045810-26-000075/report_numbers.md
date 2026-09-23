# NVDA — 0001045810-26-000075 (10-Q, period ended 2026-07-26) — numbers report

## Run notes (read before the items)

- **No out-of-scope data found.** My directory holds only `input_8k.md`, `input_numbers.json`, `input_prior_predictions.md` and `input_trends.json`. None of them contains prices, returns, short interest, other companies' files, prior probabilities or an outcome window.
- **Three expected inputs are missing.** There are no articulation checks, no restatement traces and no fourth-quarter derivation in my directory. So there are no `articulation:` items. The fourth quarters (`quarters-back-2`, `quarters-back-6`) are unfilled in the trend table, and I do not derive them.
- **The facts have no in-note marker.** Each fact in `input_numbers.json` has these fields: id, tag, prefix, namespace, context, context_ref, unit, decimals, value, number, nil, form, source_accession and filing_date. None of them says whether the element sat inside a note. I was told not to judge this myself, so "Seen in the notes" is empty (see that section).
- **The fact ids use a different format.** Facts in `input_numbers.json` have ids like `0001045810-26-000075:f-1068`, not `{accession}:facts:{tag}:{period}`. For fact items I used the `{accession}:facts:{tag}:{period}` ids that the trend table prints for its formula inputs, and I quoted the value line as it appears there.
- **Trend ids.** I built trend ids as `{accession}:trends:{metric}:{period}`, with the quarter's start..end dates as the period. I quoted the ratio's `"value"` line exactly as it is printed in `input_trends.json`.
- **No prior flags.** `input_prior_predictions.md` says there is no earlier run for this company.

## Seen in the statements

```json
{ "id": "0001045810-26-000075:trends:days_sales_outstanding:2026-04-27..2026-07-26",
  "what_changed": "Days sales outstanding for the quarter ended 2026-07-26 is 59.63738684902464. The printed quarter-over-quarter change against quarters-back-1 is 14.246098482915471, and the printed year-over-year change against quarters-back-4 is 5.500339590611617. The receivables_over_revenue ratio for the same quarter moves the same way (value 0.6553558994398312, printed QoQ change 0.15655053277929087). Printed DSO values for the other filled quarters: 45.89427626703153 (quarters-back-7), 45.708592437928374 (quarters-back-5), 54.13704725841302 (quarters-back-4), 53.30282777251518 (quarters-back-3), 45.391288366109166 (quarters-back-1). The current value is the highest of the six filled quarters. The two fiscal fourth quarters are missing from the table.",
  "account": "Accounts receivable, net (AccountsReceivableNetCurrent) against Revenues",
  "expected_direction": "up",
  "horizon": "quarter-over-quarter and year-over-year, as of the quarter ended 2026-07-26; 6 of 8 quarterly points filled",
  "quote": "\"value\": 59.63738684902464",
  "paragraph_id": "0001045810-26-000075:trends:days_sales_outstanding:2026-04-27..2026-07-26" }
```

```json
{ "id": "0001045810-26-000075:facts:AccountsReceivableNetCurrent:2026-07-26",
  "what_changed": "Accounts receivable, net at 2026-07-26 is 63059000000.0 (USD). The trend table prints 40710000000.0 at 2026-04-26 (0001045810-26-000052). This is the numerator behind the DSO item above.",
  "account": "Accounts receivable, net",
  "expected_direction": "up",
  "horizon": "balance at 2026-07-26 against balance at 2026-04-26",
  "quote": "\"value\": 63059000000.0",
  "paragraph_id": "0001045810-26-000075:facts:AccountsReceivableNetCurrent:2026-07-26" }
```

```json
{ "id": "0001045810-26-000075:trends:days_sales_of_inventory:2026-04-27..2026-07-26",
  "what_changed": "Days sales of inventory for the quarter ended 2026-07-26 is 119.32908343369742. The printed QoQ change against quarters-back-1 is 4.58047653175197, and the printed YoY change against quarters-back-4 is 13.701309965892918. Printed values for the other filled quarters: 78.03204122787362 (quarters-back-7), 59.29073243647235 (quarters-back-5), 105.6277734678045 (quarters-back-4), 118.77970574651977 (quarters-back-3), 114.74860690194545 (quarters-back-1). The annual row for years-back-0 prints 124.70095238095239, with a YoY change of 12.285743581663198.",
  "account": "Inventories (InventoryNet) against Cost of revenue",
  "expected_direction": "up",
  "horizon": "quarter-over-quarter and year-over-year, as of the quarter ended 2026-07-26",
  "quote": "\"value\": 119.32908343369742",
  "paragraph_id": "0001045810-26-000075:trends:days_sales_of_inventory:2026-04-27..2026-07-26" }
```

```json
{ "id": "0001045810-26-000075:facts:InventoryNet:2026-07-26",
  "what_changed": "Inventories at 2026-07-26 are 31575000000.0 (USD). The trend table prints 25797000000.0 at 2026-04-26 and 21403000000.0 at 2026-01-25. No inventory reserve exists to compare against: the table says the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period, so inventory_reserve_ratio is unfilled in every period.",
  "account": "Inventories",
  "expected_direction": "up",
  "horizon": "balance at 2026-07-26 against 2026-04-26 and 2026-01-25",
  "quote": "\"value\": 31575000000.0",
  "paragraph_id": "0001045810-26-000075:facts:InventoryNet:2026-07-26" }
```

```json
{ "id": "0001045810-26-000075:trends:contract_liabilities_over_revenue:2026-04-27..2026-07-26",
  "what_changed": "Current contract liabilities over quarterly revenue is 0.04797289572962243. The printed QoQ change is 0.02697185425440342 and the printed YoY change is 0.02700718963459216. The other filled quarters print 0.021435493985519638 (quarters-back-7), 0.024374744677953794 (quarters-back-5), 0.020965706095030272 (quarters-back-4), 0.021892432375539415 (quarters-back-3) and 0.021001041475219015 (quarters-back-1). The current quarter is outside that earlier range.",
  "account": "Contract liabilities, current (ContractWithCustomerLiabilityCurrent) against Revenues",
  "expected_direction": "up",
  "horizon": "quarter-over-quarter and year-over-year, as of the quarter ended 2026-07-26",
  "quote": "\"value\": 0.04797289572962243",
  "paragraph_id": "0001045810-26-000075:trends:contract_liabilities_over_revenue:2026-04-27..2026-07-26" }
```

```json
{ "id": "0001045810-26-000075:facts:ContractWithCustomerLiabilityCurrent:2026-07-26",
  "what_changed": "Current contract liabilities at 2026-07-26 are 4616000000.0 (USD). The trend table prints 1714000000.0 at 2026-04-26 (0001045810-26-000052) and 1379000000.0 at 2026-01-25.",
  "account": "Contract liabilities, current",
  "expected_direction": "up",
  "horizon": "balance at 2026-07-26 against 2026-04-26 and 2026-01-25",
  "quote": "\"value\": 4616000000.0",
  "paragraph_id": "0001045810-26-000075:facts:ContractWithCustomerLiabilityCurrent:2026-07-26" }
```

```json
{ "id": "0001045810-26-000075:trends:warranty_reserve_ratio:2026-04-27..2026-07-26",
  "what_changed": "The warranty accrual over quarterly revenue is 0.030533875141601104. The printed QoQ change is -0.0055869359838047646 and the printed YoY change is -0.015333955335689615. The input warranty accrual is 2938000000.0 at 2026-07-26, against 2948000000.0 at 2026-04-26 (both from 0001045810-26-000075), while quarterly revenue printed as the other input is 96221000000.0 against 81615000000.0. The ratio falls because the accrual stays roughly flat while revenue grows.",
  "account": "Product warranty accrual (ProductWarrantyAccrual) against Revenues",
  "expected_direction": "down",
  "horizon": "quarter-over-quarter and year-over-year, as of the quarter ended 2026-07-26",
  "quote": "\"value\": 0.030533875141601104",
  "paragraph_id": "0001045810-26-000075:trends:warranty_reserve_ratio:2026-04-27..2026-07-26" }
```

```json
{ "id": "0001045810-26-000075:trends:accruals_over_total_assets:2026-04-27..2026-07-26",
  "what_changed": "Insufficient. accruals_over_total_assets does not exist for the quarter ended 2026-07-26, because the record has no operating-cash-flow row for this discrete quarter. Only 2 of the 8 quarterly points are filled: quarters-back-1 (0.030742964613024813) and quarters-back-5 (-0.06897184920242068). Those two do not support a trend claim. I have not derived the missing quarter.",
  "account": "Total accruals (net income less operating cash flow) over total assets",
  "expected_direction": "none",
  "horizon": "insufficient — 2 quarterly points",
  "quote": "no row for operating_cash_flow in 2026-04-27..2026-07-26",
  "paragraph_id": "0001045810-26-000075:trends:accruals_over_total_assets:2026-04-27..2026-07-26" }
```

### Insufficient or not computed (no items written)

- **bad_debt_reserve_ratio:** 0 of 13 periods are filled. The allowance tags are in the record, but not for any requested period.
- **inventory_reserve_ratio:** 0 of 13 periods are filled. InventoryValuationReserves is never tagged.
- **non_gaap_gap:** 0 of 13 periods are filled, because companyfacts carries no non-GAAP measure. The 8-K prints GAAP and non-GAAP net income, but no computed gap row exists, so I do not compute one.
- **gross_margin:** 0.7497531723844068, with a printed QoQ change of 0.0004178786271317181. There is no meaningful quarter-over-quarter movement, so I wrote no item.
- **soft_asset_share:** 0.8853224758954888, with a printed QoQ change of -0.015862228545033163 and YoY change of 0.03297062141204421. The quarterly and yearly changes point in opposite directions, so I make no directional claim.
- **Fourth quarters (quarters-back-2 and quarters-back-6):** unfilled, and the fourth-quarter derivation is not in my inputs.

## Seen in the notes

No items. None of the facts in `input_numbers.json` carries an in-note marker, so no fact can be assigned to this section without me judging where it came from, which I was told not to do. Some inputs above, such as ProductWarrantyAccrual, may well come from a note table. The input cannot confirm this, so those items stay above as they are and are not duplicated here.
