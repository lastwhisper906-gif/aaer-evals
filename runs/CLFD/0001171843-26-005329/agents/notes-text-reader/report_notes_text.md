# CLFD — notes/text reader report — 10-Q 0001171843-26-005329 (quarter ended June 30, 2026)

## Input check

- Files read in full: input_8k.md, input_controls.md, input_mdna.md, input_notes.md, input_notes_history.md, input_prior_predictions.md.
- Nothing forbidden is in the directory. There is no trend table, no prices, no abnormal returns, no short interest, no other company's files, no prior probability and no outcome window. The 8-K earnings release has condensed statements attached (8k_2_02:28–30). Those are part of the 8-K body, which I am allowed to see. I read them only as text and did no arithmetic on them.
- Some inputs are absent: there is no auditor's report (this is a 10-Q, and input_controls.md holds only Item 4), no Item 1A diff, no Exhibit 21 diff and no Exhibit 10. The only 8-K body included is Item 2.02 of 2026-08-05. The item-code list shows an Item 1.01 filed 2026-07-28 (0001171843-26-004903), but its body is not in my input.
- Prior flags: none on record, so nothing is carried forward.
- No late-filing notifications are listed, and between the prior 10-Q and this one the item-code list shows no 4.01, 4.02 or 5.02.

## Items

```json
[
  {
    "id": "liquidity_and_capital_revolving_credit_line_maturity_extended_again",
    "what_changed": "The debt note adds a new sentence. On July 24, 2026, after quarter end, the company amended the loan agreement again and moved the $40 million revolving line's maturity from July 24, 2026 to November 21, 2026. The same paragraph already recorded the April 25, 2026 amendment, which had extended the line from April 25, 2026 to July 24, 2026. The prose now shows successive interim extensions rather than a renewal. MD&A (mdna:34) now says the line matures November 21, 2026. mdna:35 still names the line of credit among the sources it calls sufficient 'beyond the next 12 months'. No borrowings are reported, and the company says it is in covenant compliance. The 8-K list shows an Item 1.01 on 2026-07-28 whose body I do not have.",
    "account": "line of credit / available liquidity",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "On July 24, 2026, the Company entered into an amendment to the loan agreement that extended the maturity of the line of credit from July 24, 2026, to November 21, 2026.",
    "paragraph_id": "0001171843-26-005329:notes:132",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_performance_stock_units_no_longer_probable",
    "what_changed": "New this quarter: as of June 30, 2026, management now judges the fiscal 2026 PSU performance goals no longer probable and estimates a 0% payout. It recorded a $221,000 benefit in the quarter that reverses previously recognized cumulative compensation cost. The note adds that any later change in probability will produce a cumulative adjustment. This is a change in estimate that lowers this quarter's stock-based compensation expense. It points the same way as the 8-K's reduced outlook (8k_2_02:17) and the MD&A's reduced performance-based compensation accruals (mdna:17).",
    "account": "stock-based compensation expense (selling, general and administrative)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "As of June 30, 2026, the Company determined that achievement of the fiscal year 2026 performance goals is no longer probable and estimated that 0% of the shares underlying the performance stock units will be awarded. As a result, during the three months ended June 30, 2026, the Company recorded a $221,000 benefit to stock-based compensation expense",
    "paragraph_id": "0001171843-26-005329:notes:67",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_performance_stock_units_excluded_from_diluted_shares",
    "what_changed": "The anti-dilution paragraph gains a sentence. It excludes the 69,117 fiscal 2026 performance stock units from diluted shares because their performance conditions were not deemed probable of achievement. In the same paragraph, the prior-year PSUs are excluded on anti-dilution grounds instead. This is the EPS side of the probability change in notes:67.",
    "account": "diluted weighted average shares",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Additionally, for the three and nine months ended June 30, 2026, 69,117 and 69,117 performance stock units, respectively, were not included in the computation of diluted net income (loss) per share, because the performance conditions were not deemed probable of achievement.",
    "paragraph_id": "0001171843-26-005329:notes:16",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_sales_concentration_large_regional_customer",
    "what_changed": "The quarter's concentration disclosure now names Customer A and Customer B as 10%-plus customers: one is a distributor and one is a large regional broadband service provider. The nine-month list names A, C and B. In the prior-year quarter (notes:89) both named customers were distributors. Customer C is in the nine-month list but not in the three-month list. The text now names a non-distributor customer as a 10% customer, which fits mdna:14 crediting the quarter's growth mainly to Large Regional Service Provider customers. The March-quarter wording is not in my input, so I cannot say whether Customer B was named there.",
    "account": "net sales (customer concentration)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "For the three months ended June 30, 2026, the Company had two customers, Customer A and Customer B, which accounted for approximately 13% and 10% of net sales, respectively. One of the customers is a distributor and one is a large regional broadband service provider.",
    "paragraph_id": "0001171843-26-005329:notes:88",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_receivables_concentration_large_regional_customer",
    "what_changed": "Receivables concentration at June 30, 2026 now names Customer B, the large regional broadband service provider, first at 21%, with Customer A at 12%. At September 30, 2025 the two named customers were Customer A and Customer C, both distributors. A single non-distributor customer now heads the receivables list. Elsewhere, MD&A says receivables rose on sales concentrated near period end and that DSO lengthened (mdna:37). The allowance for credit losses is still stated as $0 (notes:85).",
    "account": "accounts receivable",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "As of June 30, 2026, the Company had two customers, Customer B and Customer A, which accounted for approximately 21% and 12% of accounts receivable, respectively.",
    "paragraph_id": "0001171843-26-005329:notes:90",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_manufacturing_facility_lease_renewal",
    "what_changed": "The lease note describes the March 2026 exercise of the renewal option on the roughly 105,000 sq ft Brooklyn Park warehouse and manufacturing lease. The option extends the lease 61 months, to April 30, 2032, and increased the right-of-use asset and lease liability by $3,553,000. The 8-K cash-flow supplemental line shows the same figure as 'Right of use assets obtained through lease liabilities'. The paragraph differs from the prior-period version, but the prior text is not in my input, so I cannot say which sentence is new.",
    "account": "right-of-use lease assets / lease liabilities",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "In March 2026, the Company exercised the renewal option, which extended the term of the lease for an additional period of 61 months to end on April 30, 2032. The exercise of the renewal option resulted in an increase to the right-of-use asset and corresponding liability of $3,553,000 upon lease commencement.",
    "paragraph_id": "0001171843-26-005329:notes:123",
    "explanation": false
  },
  {
    "id": "across_documents_goodwill_no_triggering_events_despite_reduced_outlook",
    "what_changed": "The goodwill and intangibles notes (notes:96, notes:98) roll forward the statement that no triggering events occurred during the nine months. In the same period, the 8-K cuts fiscal 2026 guidance for 'industry demand constraints' (8k_2_02:17), and MD&A cites slower demand and an order no longer expected to be fulfilled (mdna:15). The note says the next annual goodwill test is as of September 30, 2026. This juxtaposition is for the supervisor; whether the amounts are material is not mine to judge.",
    "account": "goodwill / intangible assets",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "During the nine months ended June 30, 2026, there were no triggering events that indicate potential impairment exists.",
    "paragraph_id": "0001171843-26-005329:notes:96",
    "explanation": false
  },
  {
    "id": "results_against_expectations_quarter_sales_growth_drivers_by_customer_market",
    "what_changed": "New quarter explanation. MD&A credits the quarter's net sales increase mainly to Large Regional Service Provider customers (up 58%), Community Broadband (up 13%) and National Carrier (up 54%), attributing each to 'increased demand in the quarter'. It names offsets: MSO customers down 17%, Legacy down 100% (divested copper assemblies business) and International down 26%. All three numbers are as stated in the prose.",
    "account": "net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "was primarily driven by increased sales to Large Regional Service Provider customers of $4,025,000, up 58%",
    "paragraph_id": "0001171843-26-005329:mdna:14",
    "explanation": false
  },
  {
    "id": "across_documents_demand_described_as_both_increased_and_slower",
    "what_changed": "In the same quarter the prose describes demand two ways. mdna:14 says sales in three customer markets rose 'due to increased demand in the quarter'. mdna:15 says backlog fell partly 'due to slower demand during the quarter'. The 8-K reduces guidance for 'industry demand constraints' (8k_2_02:17). Both statements can hold if the quarter's shipments came out of existing orders while new orders slowed. The supervisor should reconcile the sales and backlog figures; I have not compared them.",
    "account": "net sales / order backlog",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "The decrease in backlog is due to slower demand during the quarter",
    "paragraph_id": "0001171843-26-005329:mdna:15",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_backlog_order_no_longer_expected_to_be_fulfilled",
    "what_changed": "New: MD&A says June 30, 2026 backlog excludes the remaining portion of a previously booked customer order of $4,624,000 that management no longer believes will be fulfilled. It describes backlog as decreased 34% from March 31, 2026 and 32% from June 30, 2025, as stated in the prose. The 8-K (8k_2_02:13) describes the same removal as 'a previously booked order of $4.6 million'. MD&A instead says 'remaining portion', which implies part of the order was already fulfilled. The customer is not named. The same order drives the inventory charge in mdna:16.",
    "account": "order backlog / net sales",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "as well as the exclusion of the remaining portion of a previously booked customer order in the amount of $4,624,000 which we no longer believe will be fulfilled.",
    "paragraph_id": "0001171843-26-005329:mdna:15",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_inventory_charge_for_order_no_longer_expected_to_be_fulfilled",
    "what_changed": "New: MD&A attributes the quarter's gross-margin decline to product mix and to higher excess-and-obsolete inventory charges. Specifically, it cites $2,560,000 for the remaining finished-goods portion of a customer order no longer expected to be fulfilled, which is the order removed from backlog in mdna:15. The 8-K (8k_2_02:14) calls it a $2.6 million inventory charge worth about 5.9 percentage points of gross margin. The nine-month paragraph (mdna:26) repeats the same charge. Here management explains a number in the inventory reserve.",
    "account": "inventory reserve / cost of sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "higher excess and obsolete inventory charges specifically driven by $2,560,000 in charges related to the remaining finished good portion of a customer order which we no longer believe will be fulfilled",
    "paragraph_id": "0001171843-26-005329:mdna:16",
    "explanation": true
  },
  {
    "id": "earnings_quality_recoveries_on_sales_of_previously_reserved_inventory",
    "what_changed": "MD&A says the inventory charge was partly offset by recoveries on sales of previously reserved inventory: $1,407,000 in the quarter and $2,781,000 for the nine months (mdna:26). The 8-K (8k_2_02:14) adds a detail not in the 10-Q text: $282,000 of inventory provision netted against the $1.4 million of recoveries. Management says the two together raised gross margin by $1.1 million, about 2.6 points. Selling reserved stock releases reserve into gross margin, so part of the quarter's margin comes from prior-period reserves. Here management explains a number in the inventory reserve.",
    "account": "inventory reserve / cost of sales",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "This was offset by recoveries on sales of previously reserved inventory of $1,407,000",
    "paragraph_id": "0001171843-26-005329:mdna:16",
    "explanation": true
  },
  {
    "id": "earnings_quality_tariff_refunds_not_expected_to_recur",
    "what_changed": "The release says the quarter's $655,000 of tariff recoveries added about 1.5 percentage points to gross margin. It says they are refunds of previously paid tariffs following a change in tariff regulations and are not expected to recur. The 10-Q MD&A reports the refunds ($655,000 for the quarter in mdna:16, $1,002,000 for nine months in mdna:26) but no 10-Q paragraph in my input says they will not recur. The prose implies gross margin loses this benefit in later periods.",
    "account": "cost of sales / gross margin",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "The Company does not expect tariff recoveries to recur in future periods, as they relate to previously paid tariffs that have been refunded following a change in tariff regulations.",
    "paragraph_id": "0001171843-26-005241:8k_2_02:14",
    "explanation": false
  },
  {
    "id": "earnings_quality_performance_compensation_accrual_reduction",
    "what_changed": "New: MD&A attributes the quarter's SG&A decrease to a $1,710,000 reduction of performance-based compensation accruals, reflecting lower projected incentive-plan expense, partly offset by $755,000 of higher wages and benefits. The 8-K (8k_2_02:15) gives the same cause, rounded to $1.7 million, for the decline from both the prior quarter and the prior-year quarter. The nine-month paragraph (mdna:27) lists lower performance-based compensation accruals of $1,204,000 among its offsets. mdna:18 credits part of the rise in quarterly income from operations to decreased SG&A. The accrual reduction is an estimate change made in the quarter.",
    "account": "selling, general and administrative / accrued compensation",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The decrease is due to a reduction of $1,710,000 of performance-based compensation accruals during the quarter",
    "paragraph_id": "0001171843-26-005329:mdna:17",
    "explanation": false
  },
  {
    "id": "earnings_quality_receivables_increase_attributed_to_period_end_sales_timing",
    "what_changed": "MD&A attributes the nine-month increase in accounts receivable ($4,064,000, as stated) to sales concentrated near the end of the period. The prior-year paragraph (mdna:38) uses the same explanation, in the same words, for that year's increase. In the same paragraph MD&A says DSO lengthened, and notes:90 now shows one large regional customer holding 21% of receivables. Here management explains a number in receivables.",
    "account": "accounts receivable",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase in accounts receivable is due to the timing of sales, which were concentrated near the end of the reporting period during the nine months ended June 30, 2026.",
    "paragraph_id": "0001171843-26-005329:mdna:37",
    "explanation": true
  },
  {
    "id": "earnings_quality_days_sales_outstanding_lengthened",
    "what_changed": "MD&A says DSO increased seven days, from 37 to 44, between June 30, 2025 and June 30, 2026. The prior-year comparison (mdna:38) says DSO decreased one day. The only cause offered is the timing-of-sales explanation for the receivables increase. The allowance for credit losses stays at $0 (notes:85).",
    "account": "accounts receivable",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Days sales outstanding, which measures how quickly receivables are collected, increased seven days from 37 to 44 from June 30, 2025 to June 30, 2026.",
    "paragraph_id": "0001171843-26-005329:mdna:37",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_inventory_drawdown_attributed_to_fulfilling_orders_from_stock",
    "what_changed": "MD&A attributes the nine-month decrease in inventories ($8,640,000, as stated) to using existing inventory on hand to fill customer orders. The cash-flow explanation does not mention the quarter's $2,560,000 excess-and-obsolete charge or the reserve recoveries described in mdna:16, although both bear on inventories, net. The prior-year explanation (mdna:38) also cited decreased purchases and lower stocking levels; this one does not. Here management explains a number in inventory.",
    "account": "inventories, net",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The decrease in inventory is due to the Company utilizing existing inventory on hand to fulfill customer orders to support sales demand.",
    "paragraph_id": "0001171843-26-005329:mdna:37",
    "explanation": true
  },
  {
    "id": "across_documents_other_assets_increase_attributed_to_income_tax_payments",
    "what_changed": "MD&A now attributes the nine-month increase in other assets to income tax payments and higher prepaid expenses. The prior-year paragraph (mdna:38) cited recognition of a deferred tax asset. The 8-K cash-flow supplement has a line labelled 'Cash (refunded) paid for income taxes, net' for the same nine months (8k_2_02:30). Whether that line supports an 'income tax payments' explanation is for the numbers reader to reconcile.",
    "account": "prepaid and other current assets / income taxes",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase in other assets is due to income tax payments and increase in prepaid expenses.",
    "paragraph_id": "0001171843-26-005329:mdna:37",
    "explanation": false
  },
  {
    "id": "across_documents_estimate_changes_described_as_not_significant",
    "what_changed": "The critical-estimates section rolls forward two statements: changes in estimates 'did not have a significant impact on earnings' for the three and nine months (mdna:52), and critical accounting estimates were not changed (mdna:51). The same filing describes several estimate-driven items in the quarter: an inventory charge for an order no longer expected to be fulfilled (mdna:16), recoveries of reserved inventory (mdna:16), a reduction of performance-compensation accruals (mdna:17), and a reversal of PSU expense after a probability reassessment (notes:67). Judging whether these are 'significant' is a magnitude comparison I am not permitted to make, so I leave it to the numbers reader and supervisor.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Changes in these estimates did not have a significant impact on earnings for the three and nine months ended June 30, 2026.",
    "paragraph_id": "0001171843-26-005329:mdna:52",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_hyperscale_data_center_order",
    "what_changed": "New in the release: after the quarter closed, the company received its 'first significant order', $22 million for a hyperscale data center project, with shipments expected to begin in early fiscal 2027. The CEO repeats this in 8k_2_02:10 and frames it as part of a push 'well beyond our traditional broadband markets'. The order came after June 30, 2026, so it is not in the stated June 30 backlog. No 10-Q paragraph in my input mentions it. The 10-Q says all of the quarter's sales were to Broadband Service Providers (mdna:13). The customer is not named.",
    "account": "order backlog / net sales",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Received first significant order for $22 million to support a hyperscale data center project after the close of the quarter; expect to begin shipments in early fiscal 2027",
    "paragraph_id": "0001171843-26-005241:8k_2_02:5",
    "explanation": false
  },
  {
    "id": "results_against_expectations_fiscal_year_outlook_reduced",
    "what_changed": "The release lowers the fiscal 2026 outlook, citing industry demand constraints discussed in the shareholder letter, which is not in my input. New ranges: fiscal 2026 net sales from continuing operations $151 million to $155 million and EPS $0.14 to $0.21; fourth-quarter net sales $38 million to $42 million and EPS $0.00 to $0.07. It again flags possible optical-fiber supply constraints and tariff uncertainty, both of which it says were raised in earlier letters. The prior guidance ranges are not in my input.",
    "account": "net sales / net income",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "As a result of industry demand constraints discussed in our Shareholder Letter, we are reducing our outlook for fiscal 2026.",
    "paragraph_id": "0001171843-26-005241:8k_2_02:17",
    "explanation": false
  },
  {
    "id": "across_documents_cash_generation_described_as_strong",
    "what_changed": "In the release, the CFO describes the company's cash generation as 'strong'. The nine-month operating cash flow for this year and the prior year is stated in mdna:37, mdna:38 and 8k_2_02:30. Whether those figures support the description is for the numbers reader; I have not compared them.",
    "account": "net cash provided by operating activities",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Our balance sheet and strong cash generation continue to provide the flexibility to invest in meaningful long-term growth opportunities",
    "paragraph_id": "0001171843-26-005241:8k_2_02:11",
    "explanation": false
  },
  {
    "id": "controls_audit_and_filings_earnings_release_mislabels_quarter",
    "what_changed": "Under the heading 'Financial Results for the Three Months Ended June 30, 2026', the release calls the quarter's net sales 'the second quarter of fiscal 2026'. Everywhere else in the release the period is the third quarter. This is a drafting error in the furnished release. It does not change any amount, but it is a filing-quality point. The 10-Q has a separate typographical slip in mdna:30.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Net sales from continuing operations for the second quarter of fiscal 2026 increased 13% to $43.9 million from $38.8 million in the same year-ago quarter.",
    "paragraph_id": "0001171843-26-005241:8k_2_02:12",
    "explanation": false
  }
]
```

## Paragraphs carried as text that are not items

One line per paragraph: its paragraph id and why it is not an item. Lines marked `insufficient` are paragraphs shown as changed where my input does not let me tell what changed.

### Notes

- `0001171843-26-005329:notes:4` — date rolled forward; note_history:1 confirms the only change is the period label.
- `0001171843-26-005329:notes:10` — insufficient: the prior text is not in my input. The ASU 2024-03 paragraph and its October 1, 2027 adoption year read as recurring, and I cannot see what changed.
- `0001171843-26-005329:notes:11` — insufficient: the prior text is not in my input. The ASU 2025-06 paragraph and its October 1, 2028 adoption year read as recurring, and I cannot see what changed.
- `0001171843-26-005329:notes:12` — heading only.
- `0001171843-26-005329:notes:13` — insufficient: EPS definition that reads as boilerplate; I cannot see what changed.
- `0001171843-26-005329:notes:14` — date rolled forward.
- `0001171843-26-005329:notes:15` — amounts only (EPS table).
- `0001171843-26-005329:notes:19` — amounts only (cash table).
- `0001171843-26-005329:notes:23` — date rolled forward.
- `0001171843-26-005329:notes:24` — amounts only (available-for-sale table).
- `0001171843-26-005329:notes:27` — date rolled forward.
- `0001171843-26-005329:notes:28` — amounts only (unrealized-loss table; note_history:5 shows a table change only).
- `0001171843-26-005329:notes:31` — insufficient: date rolled forward. It states a count of six securities for both dates, and the prior count is not in my input.
- `0001171843-26-005329:notes:38` — date rolled forward.
- `0001171843-26-005329:notes:39` — amounts only (fair-value table).
- `0001171843-26-005329:notes:42` — date rolled forward.
- `0001171843-26-005329:notes:43` — date rolled forward.
- `0001171843-26-005329:notes:45` — date rolled forward.
- `0001171843-26-005329:notes:46` — amounts only (OCI roll-forward with a June-quarter row added).
- `0001171843-26-005329:notes:47` — date rolled forward.
- `0001171843-26-005329:notes:48` — amounts only (prior-year OCI roll-forward).
- `0001171843-26-005329:notes:50` — amounts only (stock compensation expense and unrecognized cost).
- `0001171843-26-005329:notes:51` — amounts only (prior-year comparative).
- `0001171843-26-005329:notes:53` — date rolled forward (no options granted).
- `0001171843-26-005329:notes:54` — date rolled forward.
- `0001171843-26-005329:notes:55` — amounts only (option activity table).
- `0001171843-26-005329:notes:56` — amounts only (intrinsic value and term).
- `0001171843-26-005329:notes:58` — date rolled forward (restricted stock grants).
- `0001171843-26-005329:notes:59` — date rolled forward (fiscal 2025 PSU certification).
- `0001171843-26-005329:notes:60` — insufficient: date rolled forward. I cannot tell whether the director grants are new this quarter.
- `0001171843-26-005329:notes:61` — date rolled forward (annual director grant).
- `0001171843-26-005329:notes:62` — date rolled forward (prior-year director grant).
- `0001171843-26-005329:notes:63` — date rolled forward.
- `0001171843-26-005329:notes:64` — amounts only (restricted stock table).
- `0001171843-26-005329:notes:66` — date rolled forward (fiscal 2026 PSU grant terms).
- `0001171843-26-005329:notes:68` — date rolled forward (fiscal 2025 PSU payout).
- `0001171843-26-005329:notes:69` — date rolled forward.
- `0001171843-26-005329:notes:70` — amounts only (PSU table).
- `0001171843-26-005329:notes:72` — amounts only (new ESPP phase purchase in the recurring sentence).
- `0001171843-26-005329:notes:73` — amounts only (ESPP shares available).
- `0001171843-26-005329:notes:79` — wording only; note_history:8 shows 'six' changed to 'nine'.
- `0001171843-26-005329:notes:80` — amounts only (geographic table).
- `0001171843-26-005329:notes:82` — wording only; note_history:10 shows 'six' changed to 'nine'.
- `0001171843-26-005329:notes:83` — amounts only (market-mix table).
- `0001171843-26-005329:notes:85` — date rolled forward; note_history:12 confirms the allowance is still $0 and the date is the only change.
- `0001171843-26-005329:notes:89` — amounts only (prior-year concentration comparative).
- `0001171843-26-005329:notes:93` — amounts only (inventory table).
- `0001171843-26-005329:notes:97` — amounts only (patent count).
- `0001171843-26-005329:notes:98` — date rolled forward (no intangible triggering events; covered with notes:96 in across_documents_goodwill_no_triggering_events_despite_reduced_outlook).
- `0001171843-26-005329:notes:99` — date rolled forward.
- `0001171843-26-005329:notes:100` — amounts only (intangibles table).
- `0001171843-26-005329:notes:103` — amounts only (amortization).
- `0001171843-26-005329:notes:104` — amounts only (amortization schedule).
- `0001171843-26-005329:notes:110` — date rolled forward (no additional Nestor impairment).
- `0001171843-26-005329:notes:111` — date rolled forward.
- `0001171843-26-005329:notes:112` — amounts only (discontinued-operations table).
- `0001171843-26-005329:notes:114` — amounts only (held-for-sale table).
- `0001171843-26-005329:notes:116` — date rolled forward and amounts only; same effective-rate drivers as in the MD&A.
- `0001171843-26-005329:notes:117` — date rolled forward; prior-year comparative tax explanation.
- `0001171843-26-005329:notes:118` — date rolled forward (no valuation allowance).
- `0001171843-26-005329:notes:119` — date rolled forward (no unrecognized tax benefits).
- `0001171843-26-005329:notes:121` — insufficient: describes the April 2024 Winnetka renewal, which is already in effect. No new event is visible, and the prior text is not in my input.
- `0001171843-26-005329:notes:124` — insufficient: lease recognition policy that reads as boilerplate; I cannot see what changed.
- `0001171843-26-005329:notes:125` — date rolled forward.
- `0001171843-26-005329:notes:126` — amounts only (lease expense table).
- `0001171843-26-005329:notes:127` — date rolled forward.
- `0001171843-26-005329:notes:128` — amounts only (lease maturities).
- `0001171843-26-005329:notes:129` — amounts only (weighted term, discount rate, lease cash outflows).
- `0001171843-26-005329:notes:130` — heading only.
- `0001171843-26-005329:notes:131` — amounts only; note_history:2 shows only the interest rate and its date changed.
- `0001171843-26-005329:notes:133` — date rolled forward and amounts only; note_history:4 shows the date and the collateral amount changed.
- `0001171843-26-005329:notes:135` — date rolled forward (no 10b5-1 plan adoptions or terminations).

### Note change history

- `0001171843-26-005329:note_history:1` — change record for notes:4 (date rolled forward).
- `0001171843-26-005329:note_history:2` — change record for notes:131 (interest rate and date only).
- `0001171843-26-005329:note_history:3` — change record for notes:132 (itemized there).
- `0001171843-26-005329:note_history:4` — change record for notes:133 (date and collateral amount).
- `0001171843-26-005329:note_history:5` — change record for notes:28 (table amounts).
- `0001171843-26-005329:note_history:6` — change record for notes:80 (table amounts).
- `0001171843-26-005329:note_history:7` — change record for notes:83 (table amounts).
- `0001171843-26-005329:note_history:8` — change record for notes:79 (period word).
- `0001171843-26-005329:note_history:9` — change record for notes:80 (repeat of the same table).
- `0001171843-26-005329:note_history:10` — change record for notes:82 (period word).
- `0001171843-26-005329:note_history:11` — change record for notes:83 (repeat of the same table).
- `0001171843-26-005329:note_history:12` — change record for notes:85 (date rolled forward).

### MD&A

- `0001171843-26-005329:mdna:2` — date rolled forward.
- `0001171843-26-005329:mdna:12` — heading, date rolled forward.
- `0001171843-26-005329:mdna:13` — amounts only (quarter net sales, international and Legacy sales).
- `0001171843-26-005329:mdna:18` — amounts only; the cause restates mdna:16 and mdna:17.
- `0001171843-26-005329:mdna:19` — amounts only; the lower-interest-rate reason reads as recurring.
- `0001171843-26-005329:mdna:20` — amounts only (quarter tax rate and its drivers).
- `0001171843-26-005329:mdna:21` — amounts only.
- `0001171843-26-005329:mdna:22` — amounts only; the Nestor sale was in the first quarter.
- `0001171843-26-005329:mdna:23` — heading, date rolled forward.
- `0001171843-26-005329:mdna:24` — amounts only (nine-month net sales).
- `0001171843-26-005329:mdna:25` — amounts only; nine-month version of the mdna:14 drivers.
- `0001171843-26-005329:mdna:26` — amounts only; nine-month version of the mdna:16 causes. Its nine-month recoveries and tariff figures are cited inside the mdna:16 and 8k_2_02:14 items.
- `0001171843-26-005329:mdna:27` — amounts only; the nine-month SG&A drivers. The performance-accrual figure is cited inside the mdna:17 item.
- `0001171843-26-005329:mdna:28` — amounts only; the causes restate mdna:26 and mdna:27.
- `0001171843-26-005329:mdna:29` — amounts only.
- `0001171843-26-005329:mdna:30` — amounts only. Contains a typographical slip ('$1,562, 000'), mentioned in the mislabel item.
- `0001171843-26-005329:mdna:31` — amounts only.
- `0001171843-26-005329:mdna:32` — amounts only.
- `0001171843-26-005329:mdna:34` — date rolled forward and amounts only. The new maturity date is itemized at notes:132.
- `0001171843-26-005329:mdna:35` — insufficient: a liquidity-sufficiency and uses-of-cash statement that reads as recurring. The prior text is not in my input, so I cannot tell whether 'potential future strategic transactions' is new. Its reliance on the line of credit is noted in the notes:132 item.
- `0001171843-26-005329:mdna:38` — amounts only (prior-year operating cash flow comparative; cited inside the mdna:37 items).
- `0001171843-26-005329:mdna:39` — amounts only (discontinued-operations operating cash).
- `0001171843-26-005329:mdna:40` — amounts only (prior-year discontinued operations).
- `0001171843-26-005329:mdna:42` — amounts only (investing flows; the Nestor transaction costs relate to the first-quarter sale).
- `0001171843-26-005329:mdna:43` — amounts only (prior-year investing).
- `0001171843-26-005329:mdna:44` — amounts only.
- `0001171843-26-005329:mdna:46` — amounts only (repurchases, ESPP, withholding).
- `0001171843-26-005329:mdna:47` — amounts only (prior-year financing).
- `0001171843-26-005329:mdna:48` — amounts only (Nestor factoring flows).
- `0001171843-26-005329:mdna:51` — date rolled forward (no change to critical accounting estimates; cited inside the mdna:52 item).
- `0001171843-26-005329:mdna:54` — page number.

### Item 4 controls

- `0001171843-26-005329:item_4_controls:1` — heading.
- `0001171843-26-005329:item_4_controls:2` — heading.
- `0001171843-26-005329:item_4_controls:3` — date rolled forward; disclosure controls are still concluded effective.
- `0001171843-26-005329:item_4_controls:4` — heading.
- `0001171843-26-005329:item_4_controls:5` — date rolled forward; no changes in internal control over financial reporting reported.

### 8-K Item 2.02 (0001171843-26-005241)

- `0001171843-26-005241:8k_2_02:1` — exhibit header.
- `0001171843-26-005241:8k_2_02:2` — exhibit header.
- `0001171843-26-005241:8k_2_02:3` — title.
- `0001171843-26-005241:8k_2_02:4` — amounts only (headline results).
- `0001171843-26-005241:8k_2_02:6` — amounts only (buyback and remaining authorization).
- `0001171843-26-005241:8k_2_02:7` — wording only (release dateline; refers to a shareholder letter not in my input).
- `0001171843-26-005241:8k_2_02:8` — amounts only (quarter summary table).
- `0001171843-26-005241:8k_2_02:9` — amounts only (year-to-date summary table).
- `0001171843-26-005241:8k_2_02:10` — the CEO repeats the order in 8k_2_02:5 and adds strategy commentary; covered by that item.
- `0001171843-26-005241:8k_2_02:13` — same disclosure as mdna:15 (backlog and the removed order). The differing description of the order is noted in that item.
- `0001171843-26-005241:8k_2_02:15` — same cause as mdna:17 (the performance-compensation accrual reduction), with a sequential comparison added; covered by that item.
- `0001171843-26-005241:8k_2_02:16` — amounts only (net income and repurchases).
- `0001171843-26-005241:8k_2_02:18` — conference call logistics.
- `0001171843-26-005241:8k_2_02:19` — conference call logistics.
- `0001171843-26-005241:8k_2_02:20` — conference call logistics.
- `0001171843-26-005241:8k_2_02:21` — conference call logistics.
- `0001171843-26-005241:8k_2_02:22` — conference call logistics.
- `0001171843-26-005241:8k_2_02:23` — conference call logistics.
- `0001171843-26-005241:8k_2_02:24` — heading.
- `0001171843-26-005241:8k_2_02:25` — boilerplate company description.
- `0001171843-26-005241:8k_2_02:26` — heading (cautionary statement title only).
- `0001171843-26-005241:8k_2_02:27` — investor relations contact.
- `0001171843-26-005241:8k_2_02:28` — amounts only (condensed balance sheet).
- `0001171843-26-005241:8k_2_02:29` — amounts only (condensed statement of earnings).
- `0001171843-26-005241:8k_2_02:30` — amounts only (condensed cash flows; cited inside the mdna:37 other-assets item and the cash-generation item).

Insufficient count: 8 (notes:10, notes:11, notes:13, notes:31, notes:60, notes:121, notes:124, mdna:35).
