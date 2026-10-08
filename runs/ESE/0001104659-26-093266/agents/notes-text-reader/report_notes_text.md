# ESE — notes text reader — 10-Q 0001104659-26-093266 (quarter ended June 30, 2026)

## Inputs

All six input files read in full: input_notes.md, input_notes_history.md, input_mdna.md, input_controls.md, input_8k.md and input_prior_predictions.md.

- Missing from my directory: an auditor's report (this is a 10-Q, so there is none), an Item 1A diff, an Exhibit 21 diff and any Exhibit 10. None of those exist for me to read.
- Forbidden material: none. There is no trend table, price, return, short-interest figure or other company's file. The tables in the 8-K are part of the Item 2.02 exhibit body.
- Prior flags: none on record. There is nothing to carry forward.
- The 8-K index shows no late-filing notice on or before 2026-08-10. It lists two filings whose bodies are not in my input: 2026-06-03 (items 1.01, 1.02, 2.03, 9.01) and 2026-04-16 (items 1.01, 3.02, 9.01). Two items below refer to them.
- I did no arithmetic anywhere. Every amount, percentage and direction word below is the filing's own. Wherever two documents state the same balance, I leave the tie-out to the numbers reader.
- Three items start with `insufficient:`. They are `liquidity_and_capital_maritime_post_closing_payments`, `narrative_signs_of_operating_pressure_iran_lebanon_conflict_and_strait_of_hormuz` and `related_parties_contingencies_and_subsequent_events_contingencies_paragraph_unseen_change`.

## Items

```json
[
  {
    "id": "liquidity_and_capital_new_secured_credit_facility_for_megger",
    "what_changed": "The debt note has a new paragraph that was not there last quarter. On May 29, 2026 the Company and certain subsidiaries signed a Credit Agreement (the New Credit Facility) with JPMorgan Chase Bank, N.A. as administrative agent to finance the Megger purchase. It takes effect only on, and substantially at the same time as, the closing of the Megger deal, and on that date it replaces the Existing Credit Facility. It provides a $500 million senior secured revolver, a $500 million senior secured term loan A and a $500 million senior secured term loan B. The Company can expand it up to the greater of $451 million or 100% of Consolidated EBITDA, plus further amounts subject to maximum leverage ratios. Certain foreign subsidiaries may borrow under it. The revolver and term loan A mature five years after the Effective Date and term loan B seven years after. The old facility is now called the Existing Credit Facility throughout the note. The 8-K index lists a 2026-06-03 filing with items 1.01, 1.02, 2.03 and 9.01. Its body is not in my input, and the note does not say which agreement, if any, was terminated under item 1.02. The 8-K cash flow statement carries a Debt issuance costs line for the current nine months.",
    "account": "long-term debt; interest expense",
    "expected_direction": "up",
    "horizon": "at Megger closing, which the filing expects in Q1 fiscal 2027 (within 12 months)",
    "quote": "The New Credit Facility provides for (i) a senior secured revolving credit facility in an initial aggregate commitment amount of $500 million, (ii) a senior secured term loan A facility in an initial aggregate principal amount of $500 million, and (iii) a senior secured term loan B facility in an initial aggregate principal amount of $500 million.",
    "paragraph_id": "0001104659-26-093266:notes:50",
    "explanation": false
  },
  {
    "id": "earnings_quality_megger_debt_financing_costs_in_interest_expense",
    "what_changed": "MD&A now says interest expense increased mainly because of approximately $7 million of debt financing costs incurred in Q3 2026 for the pending Megger acquisition. It says lower average borrowings and lower average interest rates partly offset this. These financing costs hit GAAP interest expense before any Megger debt is drawn. The 8-K removes them from Adjusted EPS (see earnings_quality_adjusted_eps_excludes_megger_financing_and_deal_costs).",
    "account": "interest expense",
    "expected_direction": "up",
    "horizon": "this quarter; the prose ties the cost to a pending deal, so more such costs can appear until closing",
    "quote": "was mainly due to approximately $7 million of debt financing costs incurred in the third quarter of 2026 related to the pending Megger acquisition",
    "paragraph_id": "0001104659-26-093266:mdna:36",
    "explanation": false
  },
  {
    "id": "earnings_quality_adjusted_eps_excludes_megger_financing_and_deal_costs",
    "what_changed": "The 8-K's Adjusted EPS reconciliation adds a new excluded item: debt financing related to the pending Megger acquisition, $0.20 per share in both Q3 and YTD. It sits alongside Megger acquisition costs at Corporate, $0.19 for Q3 and $0.23 YTD. None of the prior-year reconciliations shown lists a debt financing exclusion. The raised Adjusted EPS guidance is on this adjusted basis. Whether the per-share amounts tie to the MD&A's approximately $7 million is for the numbers reader.",
    "account": "Adjusted EPS reconciliation (excluded charges); interest expense; SG&A",
    "expected_direction": "up",
    "horizon": "next quarter, until Megger closes",
    "quote": "$0.20 of debt financing and $0.19 of acquisition costs at Corporate related to the pending Megger acquisition that was announced in April 2026",
    "paragraph_id": "0001104659-26-092033:8k_2_02:54",
    "explanation": false
  },
  {
    "id": "earnings_quality_megger_acquisition_costs_in_corporate_sga",
    "what_changed": "The MD&A's explanation of higher SG&A now names an increase at Corporate, mainly from acquisition costs for the pending Megger acquisition. The other causes it gives are Maritime-related SG&A in A&D, and higher sales and inflation in all three segments. The 8-K removes these Megger costs from Adjusted EPS.",
    "account": "SG&A (Corporate)",
    "expected_direction": "up",
    "horizon": "this quarter and until Megger closes",
    "quote": "an increase at Corporate mainly due to acquisition costs related to the pending Megger acquisition",
    "paragraph_id": "0001104659-26-093266:mdna:18",
    "explanation": false
  },
  {
    "id": "earnings_quality_share_based_compensation_increase_at_corporate",
    "what_changed": "The MD&A's explanation of Corporate costs now names an increase in share-based compensation costs. It names this alongside Megger acquisition costs and amortization from the Maritime acquisition. Note 3 gives the quarter's stock-unit and total share-based compensation expense, and $15.6 million of unrecognized cost to be recognized over a weighted-average 1.8 years. I have not compared those amounts.",
    "account": "SG&A - share-based compensation (Corporate)",
    "expected_direction": "up",
    "horizon": "this quarter; remaining cost over 1.8 years",
    "quote": "an increase in share-based compensation costs and acquisition related costs related to the pending Megger acquisition",
    "paragraph_id": "0001104659-26-093266:mdna:34",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_tax_return_to_provision_research_credit",
    "what_changed": "The tax note and MD&A (mdna:38 and mdna:39) now say Q3 and nine-month income tax expense benefited from return-to-provision adjustments. These were recognized when the 2025 federal income tax return was finalized, and they include an increase to the federal research credit. This corrects a prior-year estimate and comes from a single filing event; the prose does not say it will recur. The prose blames the prior-year rate on Maritime-related non-deductible transaction costs.",
    "account": "income tax expense; effective tax rate",
    "expected_direction": "down",
    "horizon": "this quarter; not stated to recur next quarter",
    "quote": "Income tax expense in the third quarter and first nine months of 2026 was favorably impacted by return-to-provision adjustments recognized upon finalization of the 2025 federal income tax return, including an increase to the federal research credit.",
    "paragraph_id": "0001104659-26-093266:notes:52",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_inventory_build_timing_of_existing_orders",
    "what_changed": "MD&A now explains, segment by segment, why inventories increased since September 30, 2025. A&D and USG increased, and the filing attributes both to higher work-in-process and raw materials inventories caused by the timing of manufacturing existing orders. A decrease in Test partly offset them. The cause given is order timing, which implies the build unwinds as those orders ship. Note 4's table has the finished goods, work in process and raw materials lines (for the numbers reader).",
    "account": "inventories",
    "expected_direction": "down",
    "horizon": "next quarter to 12 months",
    "quote": "Inventories increased $22.7 million during this period due to a $14.9 million increase within the A&D segment, and a $9.2 million increase within the USG segment; both increases due to higher work-in-process and raw materials inventories due to timing of manufacturing existing orders, partially offset by a $1.4 million decrease within the Test segment.",
    "paragraph_id": "0001104659-26-093266:mdna:41",
    "explanation": true
  },
  {
    "id": "liquidity_and_capital_contract_assets_maritime_timing",
    "what_changed": "MD&A now explains the increase in contract assets since September 30, 2025 as mainly in A&D (Maritime) and due to timing. Timing language implies billing catches up. Note 11 gives contract asset balances at both dates; tying them to the MD&A amount is for the numbers reader.",
    "account": "contract assets (unbilled receivables)",
    "expected_direction": "down",
    "horizon": "next quarter to 12 months",
    "quote": "Contract assets increased $36.9 million primarily within the A&D segment (Maritime) due to timing.",
    "paragraph_id": "0001104659-26-093266:mdna:41",
    "explanation": true
  },
  {
    "id": "liquidity_and_capital_contract_liabilities_customer_payment_timing",
    "what_changed": "MD&A now explains the increase in contract liabilities since September 30, 2025 as mainly in A&D (Globe and Maritime) and due to the timing of payments received from customers. Note 11 gives contract liability balances at both dates. It also says about $74 million of revenue in the nine months came from the opening balance. Tying the note, MD&A and 8-K balance sheet figures together is for the numbers reader. Because the filing calls these customer advances a timing effect, they should be worked off as revenue is recognized.",
    "account": "contract liabilities",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "Contract liabilities increased $71.5 million primarily within the A&D segment (Globe and Maritime) due to timing of payments received from customers.",
    "paragraph_id": "0001104659-26-093266:mdna:41",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_operating_cash_flow_lower_working_capital_requirements",
    "what_changed": "MD&A attributes the nine-month operating cash flow from continuing operations to lower working capital requirements and higher earnings. In mdna:41, the filing attributes the contract liability increase to the timing of customer payments, so part of the working-capital contribution depends on timing. The prior-quarter wording of this sentence is not in my input.",
    "account": "net cash provided by operating activities - continuing operations",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "was mainly driven by lower working capital requirements and higher earnings.",
    "paragraph_id": "0001104659-26-093266:mdna:42",
    "explanation": false
  },
  {
    "id": "revenue_recognition_remaining_performance_obligations_twelve_month_share",
    "what_changed": "The note on remaining performance obligations now gives $1,540.5 million at June 30, 2026, with about 59% expected to be recognized in the next twelve months. Last quarter's text, per the note change history, gave $1,470.0 million at March 31, 2026 with about 55%. The twelve-month share is a management estimate, and it has changed. The 8-K calls the backlog a record.",
    "account": "net sales; remaining performance obligations",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "At June 30, 2026, the Company had $1,540.5 million in remaining performance obligations of which the Company expects to recognize revenues of approximately 59% in the next twelve months.",
    "paragraph_id": "0001104659-26-093266:notes:79",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_nrg_renewables_tax_credit_expiration",
    "what_changed": "The 8-K attributes the decrease in NRG orders to the expiration of U.S. renewables tax credits, which is a policy cause. MD&A attributes the decrease in NRG sales to lower shipments of solar and wind products caused by weakness in the renewables market (mdna:11). The 8-K says USG Adjusted EBIT gains were mostly offset by lower EBIT at NRG on lower sales volumes (8k_2_02:26).",
    "account": "net sales - USG (NRG); USG segment EBIT",
    "expected_direction": "down",
    "horizon": "next quarter to 12 months",
    "quote": "NRG orders decreased $5.0 million (27 percent) to $13.5 million, related to the expiration of U.S. renewables tax credits.",
    "paragraph_id": "0001104659-26-092033:8k_2_02:27",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_test_asian_operations_decrease",
    "what_changed": "The MD&A's Q3 explanation for the Test segment names a $3.9 million decrease from the segment's Asian operations, offsetting gains in the U.S. and Europe. The nine-month explanation names a $1.9 million decrease in Asia. The 8-K's Test paragraph does not mention Asia. The prior-quarter wording is not in my input.",
    "account": "net sales - Test (international)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "partially offset by a $3.9 million decrease from the segment’s Asian operations",
    "paragraph_id": "0001104659-26-093266:mdna:13",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_aerospace_defense_inflation_and_unfavorable_mix",
    "what_changed": "MD&A and the 8-K (8k_2_02:22) say inflationary pressures and unfavorable mix partly offset the gains from volume leverage and price in A&D EBIT, for both the quarter and the nine months. The prior-quarter MD&A wording is not in my input. The prose does not put a number on the mix effect.",
    "account": "A&D segment EBIT; cost of sales",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "partially offset by inflationary pressures and unfavorable mix",
    "paragraph_id": "0001104659-26-093266:mdna:28",
    "explanation": false
  },
  {
    "id": "earnings_quality_continuing_restructuring_acoustics_exit_and_usg_severance",
    "what_changed": "Q3 other expenses now include $0.7 million of Test restructuring for exiting the acoustics product line, mostly asset write-offs. They also include $0.3 million of USG restructuring, mostly severance. MD&A describes Test's nine-month restructuring as asset write-offs, contract termination charges and severance (mdna:32). It says USG's nine-month EBIT bears restructuring charges and acquisition costs (mdna:30). The 8-K removes these charges from Adjusted EPS. The prose does not say whether more charges are planned.",
    "account": "other expenses, net; segment EBIT (Test, USG)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "$0.7 million of restructuring charges within the Test segment due to the exit of the acoustics product line (primarily asset write-offs)",
    "paragraph_id": "0001104659-26-093266:mdna:22",
    "explanation": false
  },
  {
    "id": "across_documents_aerospace_defense_restructuring_named_only_in_press_release",
    "what_changed": "The 8-K's year-to-date Adjusted EPS footnote names restructuring charges in Test, USG and A&D. The 10-Q MD&A names nine-month restructuring only in Test (mdna:22, mdna:32) and USG (mdna:22, mdna:30). Its A&D EBIT paragraph (mdna:28) names no 2026 restructuring charge. This item is about which words appear where; whether an A&D amount exists is for the numbers reader.",
    "account": "other expenses, net; A&D segment EBIT",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "$0.09 of restructuring charges within Test, USG & A&D segments",
    "paragraph_id": "0001104659-26-092033:8k_2_02:59",
    "explanation": false
  },
  {
    "id": "across_documents_mdna_liquidity_paragraph_silent_on_new_credit_facility",
    "what_changed": "The MD&A's credit facility paragraph updates availability, cash, borrowings and letters of credit. It repeats that operating cash flow and credit facility borrowings will meet capital and operating needs for the foreseeable future. It repeats that the $250 million increase option depends on the banks accepting it. It does not mention the May 29, 2026 New Credit Facility, which the debt note says will replace the existing facility when Megger closes. The MD&A paragraphs carried as unchanged (mdna:49 to mdna:51) are not visible to me. mdna:48 says committed financing is in place.",
    "account": "long-term debt; liquidity disclosure",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "Cash flow from operations and borrowings under the Company’s credit facility are expected to meet the Company’s capital requirements and operational needs for the foreseeable future.",
    "paragraph_id": "0001104659-26-093266:mdna:45",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_megger_moved_from_subsequent_event_to_acquisition_note",
    "what_changed": "Last quarter the Megger agreement was disclosed in Note 15, SUBSEQUENT EVENT. That note is gone, and the same text now appears as Note 15, ACQUISITION, and in the MD&A Acquisitions section (mdna:48). The terms are unchanged: about $2.35 billion in total, made up of $0.9 billion in cash and ESCO equity valued at about $1.4 billion. The cash is to be funded from cash on hand and incremental debt, completion is expected in Q1 fiscal 2027, and Megger will join USG. The equity component implies more shares outstanding at closing; the 8-K index lists a 2026-04-16 filing with item 3.02. The cash component implies more debt.",
    "account": "shares outstanding / diluted shares; long-term debt",
    "expected_direction": "up",
    "horizon": "Q1 fiscal 2027 at closing (within 12 months)",
    "quote": "Under the terms of the agreement, ESCO will acquire Megger for total consideration of approximately $2.35 billion, consisting of $0.9 billion in cash and ESCO equity valued at approximately $1.4 billion.",
    "paragraph_id": "0001104659-26-093266:notes:103",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_megger_regulatory_filings_underway",
    "what_changed": "The 8-K adds that all filings for regulatory approval are underway and that the Company still expects to close in Q1 of fiscal 2027. Closing is still conditional, and the New Credit Facility takes effect only when the deal closes.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "Q1 fiscal 2027",
    "quote": "All filings for regulatory approval are underway and we continue to anticipate",
    "paragraph_id": "0001104659-26-092033:8k_2_02:33",
    "explanation": false
  },
  {
    "id": "results_against_expectations_sales_guidance_lower_end_raised",
    "what_changed": "FY 2026 sales guidance has its lower end raised and is now $1.30 to $1.33 billion, which the release describes as 19 to 21 percent growth over the prior year. The release does not restate the previous sales range.",
    "account": "net sales",
    "expected_direction": "up",
    "horizon": "next quarter (Q4 fiscal 2026, closing the fiscal year)",
    "quote": "Raising the lower end of FY 2026 Sales guidance and now expect Sales to be in the range of $1.30 to $1.33 billion (19 to 21 percent growth over the prior year).",
    "paragraph_id": "0001104659-26-092033:8k_2_02:36",
    "explanation": false
  },
  {
    "id": "results_against_expectations_adjusted_eps_guidance_raised_again",
    "what_changed": "Full-year Adjusted EPS guidance is raised to $8.30 to $8.40. The release calls this a midpoint increase of $0.70 from the November guidance ($7.50 to $7.80) and of $0.22 from the May guidance ($8.00 to $8.25). The CEO says guidance is raised again (8k_2_02:18). The guidance is on the adjusted basis, which excludes Megger financing and deal costs and acquisition amortization.",
    "account": "Adjusted EPS; net earnings",
    "expected_direction": "up",
    "horizon": "next quarter (Q4 fiscal 2026)",
    "quote": "Raising full year Adjusted EPS guidance to a range of $8.30 - $8.40 per share (38 to 39 percent growth)",
    "paragraph_id": "0001104659-26-092033:8k_2_02:37",
    "explanation": false
  },
  {
    "id": "results_against_expectations_fourth_quarter_adjusted_eps_range",
    "what_changed": "The release gives a new, explicit Adjusted EPS range for Q4 fiscal 2026 of $2.55 to $2.65. It describes this as 10 to 14 percent growth over Q4 fiscal 2025 Adjusted EPS.",
    "account": "Adjusted EPS (Q4)",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "Q4’26 Adjusted EPS is expected to be in the range of $2.55 - $2.65 per share",
    "paragraph_id": "0001104659-26-092033:8k_2_02:38",
    "explanation": false
  },
  {
    "id": "results_against_expectations_test_orders_data_center_emi_filters",
    "what_changed": "The 8-K says Test orders were strong because of industrial shielding projects and electromagnetic interference (EMI) filters for U.S. data centers, and calls the Test backlog a record. It names data-center filters as a source of orders.",
    "account": "net sales - Test; backlog",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Orders strength in the quarter was driven by industrial shielding projects and electromagnetic interference (EMI) filters for U.S. data centers.",
    "paragraph_id": "0001104659-26-092033:8k_2_02:31",
    "explanation": false
  },
  {
    "id": "results_against_expectations_aerospace_defense_aerospace_orders_record_backlog",
    "what_changed": "The 8-K says A&D's book-to-bill for the quarter came from higher commercial and military aerospace OEM and aftermarket orders, giving a record A&D backlog. It says the year-ago orders included Maritime acquired backlog and Virginia Class and Columbia Class orders, which explains the lower year-on-year order comparison.",
    "account": "net sales - A&D; backlog",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Book-to-bill in the quarter was 1.16 driven by higher commercial and military aerospace OEM and aftermarket orders, resulting in record backlog of $1.1 billion.",
    "paragraph_id": "0001104659-26-092033:8k_2_02:23",
    "explanation": false
  },
  {
    "id": "results_against_expectations_doble_utility_demand_orders",
    "what_changed": "The 8-K says Doble orders increased because of broad-based increases in demand from utility customers, and describes that demand as continuing.",
    "account": "net sales - USG (Doble)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Doble orders increased $26.4 million (30 percent) to $113.3 million as the business continues to experience broad based increases in demand from utility customers.",
    "paragraph_id": "0001104659-26-092033:8k_2_02:27",
    "explanation": false
  },
  {
    "id": "results_against_expectations_maritime_contribution_laps",
    "what_changed": "The release splits Q3 sales growth into organic growth and growth contributed by Maritime; MD&A says the same in mdna:9. The release (8k_2_02:15) places the Maritime acquisition in Q3 2025. From Q4 fiscal 2026 the comparison period also contains Maritime, so the acquired contribution to growth that the prose identifies drops out.",
    "account": "net sales (acquired growth)",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "Q3 2026 organic sales increased $20 million (8 percent), and Maritime contributed $23 million of revenue growth in the quarter.",
    "paragraph_id": "0001104659-26-092033:8k_2_02:13",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_maritime_post_closing_payments",
    "what_changed": "insufficient: MD&A says that in the first nine months the Company paid a Maritime working capital settlement and a group tax relief payment, both tied to the Maritime acquisition. The goodwill rollforward has an A&D line called 'Acquisition activity and other'. The prior-quarter wording is not in my input, so I cannot say whether any part of this is new this quarter.",
    "account": "acquisition of business, net of cash acquired; goodwill (A&D)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "the Company paid $10.2 million consisting of a $5.1 million working capital settlement and a $5.1 million group tax relief payment, both related to the Maritime acquisition.",
    "paragraph_id": "0001104659-26-093266:mdna:47",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_iran_lebanon_conflict_and_strait_of_hormuz",
    "what_changed": "insufficient: the 10-Q forward-looking statements, and the 8-K's (8k_2_02:44), name wars including the conflicts involving Iran and Lebanon, and restrictions or closures of critical supply routes such as the Strait of Hormuz. The 10-Q paragraph is carried as changed, but the prior wording is not in my input, so I cannot confirm which words are new. No Item 1A diff is in my input either.",
    "account": "cost of sales (supply chain)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "restrictions or closures of critical supply routes such as the Strait of Hormuz",
    "paragraph_id": "0001104659-26-093266:mdna:59",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_contingencies_paragraph_unseen_change",
    "what_changed": "insufficient: the MD&A Contingencies heading (mdna:56) and paragraph are carried as changed. The text says claims and litigation arise in the normal course of business and the Company is at various stages of investigating and remediating environmental matters. It says Management believes the costs are adequately reserved, covered by insurance or not material. The prior wording is not in my input, and no amount is stated.",
    "account": "none (litigation and environmental reserves)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Additionally, the Company is currently involved in various stages of investigation and remediation relating to environmental matters.",
    "paragraph_id": "0001104659-26-093266:mdna:57",
    "explanation": false
  }
]
```

## Paragraphs carried as text that are not an item

### Notes (0001104659-26-093266)

- `0001104659-26-093266:notes:3` — date rolled forward (three and nine months to June 30)
- `0001104659-26-093266:notes:6` — EPS share table, amounts only
- `0001104659-26-093266:notes:10` — amounts only (stock-unit expense, unvested units); the share-based compensation driver is item earnings_quality_share_based_compensation_increase_at_corporate
- `0001104659-26-093266:notes:12` — amounts only (director grant expense)
- `0001104659-26-093266:notes:13` — amounts only, date rolled forward (total share-based compensation, tax benefit, unrecognized cost)
- `0001104659-26-093266:notes:16` — inventory table, amounts only; the explanation is item liquidity_and_capital_inventory_build_timing_of_existing_orders
- `0001104659-26-093266:notes:18` — date rolled forward (table lead-in)
- `0001104659-26-093266:notes:19` — intangibles table, amounts only
- `0001104659-26-093266:notes:20` — date rolled forward (goodwill lead-in)
- `0001104659-26-093266:notes:21` — goodwill rollforward table, amounts only; the A&D acquisition line is part of item liquidity_and_capital_maritime_post_closing_payments
- `0001104659-26-093266:notes:23` — carried as text but no change recorded in the note history; same three reportable segments, no substance visible
- `0001104659-26-093266:notes:29` — carried as text but no change recorded in the note history; standard description of the chief operating decision maker, segment EBIT and segment assets, no substance visible
- `0001104659-26-093266:notes:30` — segment table Q3 2026, amounts only
- `0001104659-26-093266:notes:32` — capex reconciliation table, amounts only
- `0001104659-26-093266:notes:33` — segment table nine months 2026, amounts only
- `0001104659-26-093266:notes:34` — capex reconciliation table, amounts only
- `0001104659-26-093266:notes:35` — segment table Q3 2025, amounts only
- `0001104659-26-093266:notes:36` — table footnote, wording only
- `0001104659-26-093266:notes:37` — capex reconciliation table, amounts only
- `0001104659-26-093266:notes:38` — segment table nine months 2025, amounts only
- `0001104659-26-093266:notes:39` — capex reconciliation table, amounts only
- `0001104659-26-093266:notes:43` — heading
- `0001104659-26-093266:notes:44` — table lead-in, wording only
- `0001104659-26-093266:notes:45` — debt table, amounts only (term loan and revolver balances are for the numbers reader)
- `0001104659-26-093266:notes:46` — wording only: the facility is renamed "Existing Credit Facility"; the substance is item liquidity_and_capital_new_secured_credit_facility_for_megger
- `0001104659-26-093266:notes:47` — reordered and reworded (tense changed, the July 8, 2024 purchase agreement reference dropped); same Amendment No. 1 facts
- `0001104659-26-093266:notes:48` — amounts and date rolled forward (availability, cash, letters of credit), plus the defined-term rename
- `0001104659-26-093266:notes:49` — amounts and date rolled forward (weighted average rates); spread, fee and covenant-compliance wording unchanged apart from the rename
- `0001104659-26-093266:notes:54` — date rolled forward
- `0001104659-26-093266:notes:55` — equity rollforward table, amounts only
- `0001104659-26-093266:notes:62` — date rolled forward (fair value of financial instruments)
- `0001104659-26-093266:notes:66` — date rolled forward; still says no impairments were recorded
- `0001104659-26-093266:notes:69` — date rolled forward (disaggregation lead-in)
- `0001104659-26-093266:notes:70` — disaggregation table Q3 2026, amounts only
- `0001104659-26-093266:notes:71` — disaggregation table nine months 2026, amounts only
- `0001104659-26-093266:notes:72` — wording only ("from continuing operations" moved) and date rolled forward
- `0001104659-26-093266:notes:73` — disaggregation table Q3 2025, amounts only
- `0001104659-26-093266:notes:74` — disaggregation table nine months 2025, amounts only
- `0001104659-26-093266:notes:81` — amounts and date rolled forward (contract balances, revenue from opening contract liabilities); the substance is in the mdna:41 contract asset and contract liability items
- `0001104659-26-093266:notes:86` — carried as text, prior wording not in input; a generic list of lease types with no amount, commitment or policy
- `0001104659-26-093266:notes:88` — lease cost table, amounts only
- `0001104659-26-093266:notes:89` — lease cost table, amounts only
- `0001104659-26-093266:notes:91` — lease cash flow table, amounts only
- `0001104659-26-093266:notes:92` — lease cash flow table, amounts only
- `0001104659-26-093266:notes:93` — lease term and discount rate table, amounts only
- `0001104659-26-093266:notes:94` — date rolled forward (maturity table lead-in)
- `0001104659-26-093266:notes:95` — lease maturity table, amounts only
- `0001104659-26-093266:notes:97` — heading
- `0001104659-26-093266:notes:98` — carried as text, no change recorded in the note history; standard ASU 2024-03 disclosure, no expected effect beyond additional disclosure
- `0001104659-26-093266:notes:99` — carried as text, no change recorded in the note history; standard ASU 2023-09 disclosure, no expected effect beyond additional disclosure
- `0001104659-26-093266:notes:100` — heading
- `0001104659-26-093266:notes:101` — amounts and date rolled forward (sales to two Doble customers where Company directors are officers); same counterparties, terms and board conclusion per the note history
- `0001104659-26-093266:notes:102` — heading; the change from SUBSEQUENT EVENT is part of item structure_and_disclosure_changes_megger_moved_from_subsequent_event_to_acquisition_note

### MD&A (0001104659-26-093266)

- `0001104659-26-093266:mdna:3` — date rolled forward
- `0001104659-26-093266:mdna:5` — amounts only (sales, net earnings, EPS)
- `0001104659-26-093266:mdna:7` — amounts only (segment sales contributions)
- `0001104659-26-093266:mdna:9` — amounts only (navy and aerospace drivers); the Maritime contribution is item results_against_expectations_maritime_contribution_laps
- `0001104659-26-093266:mdna:11` — amounts only; the NRG renewables cause is item narrative_signs_of_operating_pressure_nrg_renewables_tax_credit_expiration
- `0001104659-26-093266:mdna:15` — amounts only (Q3 orders, backlog, prior-year Maritime acquired backlog)
- `0001104659-26-093266:mdna:16` — amounts only (nine-month orders)
- `0001104659-26-093266:mdna:20` — amounts only; the Maritime amortization driver is unchanged
- `0001104659-26-093266:mdna:24` — amounts only (EBIT and margin)
- `0001104659-26-093266:mdna:25` — table lead-in, wording only
- `0001104659-26-093266:mdna:26` — EBIT reconciliation table, amounts only
- `0001104659-26-093266:mdna:30` — amounts only; NRG volumes and restructuring/acquisition costs are covered by the NRG and restructuring items
- `0001104659-26-093266:mdna:32` — amounts only; the restructuring description is covered by item earnings_quality_continuing_restructuring_acoustics_exit_and_usg_severance
- `0001104659-26-093266:mdna:38` — same content as notes:52, covered by item estimates_and_discretion_tax_return_to_provision_research_credit
- `0001104659-26-093266:mdna:39` — continuation of mdna:38 (sentence split), same content as notes:52
- `0001104659-26-093266:mdna:43` — amounts only (capex, capitalized software)
- `0001104659-26-093266:mdna:44` — heading
- `0001104659-26-093266:mdna:46` — heading
- `0001104659-26-093266:mdna:48` — same content as notes:103, covered by the structure item
- `0001104659-26-093266:mdna:52` — date rolled forward (the July 17, 2026 dividend added as a routine payment after quarter-end)
- `0001104659-26-093266:mdna:56` — heading (its paragraph is the mdna:57 insufficient item)

### Item 4 controls (0001104659-26-093266)

- `0001104659-26-093266:item_4_controls:1` — heading
- `0001104659-26-093266:item_4_controls:2` — no change in substance: disclosure controls effective, no material change in internal control over financial reporting
- `0001104659-26-093266:item_4_controls:3` — page number

### 8-K 0001104659-26-092033, Item 2.02, Exhibit 99.1

- `0001104659-26-092033:8k_2_02:1` — exhibit label
- `0001104659-26-092033:8k_2_02:2` — exhibit title
- `0001104659-26-092033:8k_2_02:3` — letterhead
- `0001104659-26-092033:8k_2_02:4` — contact heading
- `0001104659-26-092033:8k_2_02:5` — contact name
- `0001104659-26-092033:8k_2_02:6` — contact details
- `0001104659-26-092033:8k_2_02:7` — release title
- `0001104659-26-092033:8k_2_02:8` — headline, amounts only (sales)
- `0001104659-26-092033:8k_2_02:9` — headline, amounts only (GAAP EPS)
- `0001104659-26-092033:8k_2_02:10` — headline, amounts only (Adjusted EPS)
- `0001104659-26-092033:8k_2_02:11` — dateline and period
- `0001104659-26-092033:8k_2_02:12` — heading
- `0001104659-26-092033:8k_2_02:14` — amounts only (EPS)
- `0001104659-26-092033:8k_2_02:15` — amounts only (orders, book-to-bill, backlog); backlog is covered by the remaining-obligations and segment order items
- `0001104659-26-092033:8k_2_02:16` — amounts only (YTD operating cash); covered by item liquidity_and_capital_operating_cash_flow_lower_working_capital_requirements
- `0001104659-26-092033:8k_2_02:17` — CEO quote, amounts and margin description, no new driver
- `0001104659-26-092033:8k_2_02:18` — CEO quote; the guidance raise is covered by the guidance items, and the organic growth and backlog statements are amounts only
- `0001104659-26-092033:8k_2_02:19` — heading
- `0001104659-26-092033:8k_2_02:20` — heading
- `0001104659-26-092033:8k_2_02:21` — amounts only (A&D sales, organic/Maritime split; commercial aerospace and Navy drivers as in MD&A)
- `0001104659-26-092033:8k_2_02:22` — same content as mdna:28, covered by item narrative_signs_of_operating_pressure_aerospace_defense_inflation_and_unfavorable_mix
- `0001104659-26-092033:8k_2_02:24` — heading
- `0001104659-26-092033:8k_2_02:25` — amounts only; the NRG cause is covered by the NRG item
- `0001104659-26-092033:8k_2_02:26` — covered by the NRG item (lower NRG EBIT on lower volumes)
- `0001104659-26-092033:8k_2_02:28` — heading
- `0001104659-26-092033:8k_2_02:29` — amounts only (Test sales; EMC and shielding drivers)
- `0001104659-26-092033:8k_2_02:30` — amounts only (Test EBIT)
- `0001104659-26-092033:8k_2_02:32` — heading
- `0001104659-26-092033:8k_2_02:34` — heading
- `0001104659-26-092033:8k_2_02:35` — heading
- `0001104659-26-092033:8k_2_02:39` — heading
- `0001104659-26-092033:8k_2_02:40` — date rolled forward (next dividend)
- `0001104659-26-092033:8k_2_02:41` — heading
- `0001104659-26-092033:8k_2_02:42` — conference call details
- `0001104659-26-092033:8k_2_02:43` — heading
- `0001104659-26-092033:8k_2_02:44` — same risk list as mdna:59, covered by the Iran/Lebanon and Strait of Hormuz item
- `0001104659-26-092033:8k_2_02:45` — heading
- `0001104659-26-092033:8k_2_02:46` — non-GAAP definitions, boilerplate
- `0001104659-26-092033:8k_2_02:47` — non-GAAP rationale, boilerplate
- `0001104659-26-092033:8k_2_02:48` — heading
- `0001104659-26-092033:8k_2_02:49` — company description, boilerplate
- `0001104659-26-092033:8k_2_02:50` — heading
- `0001104659-26-092033:8k_2_02:51` — heading
- `0001104659-26-092033:8k_2_02:52` — units caption
- `0001104659-26-092033:8k_2_02:53` — income statement table Q3, amounts only
- `0001104659-26-092033:8k_2_02:55` — heading
- `0001104659-26-092033:8k_2_02:56` — heading
- `0001104659-26-092033:8k_2_02:57` — units caption
- `0001104659-26-092033:8k_2_02:58` — income statement table YTD, amounts only
- `0001104659-26-092033:8k_2_02:60` — heading
- `0001104659-26-092033:8k_2_02:61` — heading
- `0001104659-26-092033:8k_2_02:62` — units caption
- `0001104659-26-092033:8k_2_02:63` — segment table Q3, amounts only
- `0001104659-26-092033:8k_2_02:64` — same content as 8k_2_02:54 (Q3 adjustments)
- `0001104659-26-092033:8k_2_02:65` — prior-year Q3 adjustments, amounts only
- `0001104659-26-092033:8k_2_02:66` — heading
- `0001104659-26-092033:8k_2_02:67` — EBITDA reconciliation table Q3, amounts only
- `0001104659-26-092033:8k_2_02:68` — heading
- `0001104659-26-092033:8k_2_02:69` — heading
- `0001104659-26-092033:8k_2_02:70` — units caption
- `0001104659-26-092033:8k_2_02:71` — segment table YTD, amounts only
- `0001104659-26-092033:8k_2_02:72` — same content as 8k_2_02:59 (YTD adjustments)
- `0001104659-26-092033:8k_2_02:73` — prior-year YTD adjustments, amounts only
- `0001104659-26-092033:8k_2_02:74` — heading
- `0001104659-26-092033:8k_2_02:75` — EBITDA reconciliation table YTD, amounts only
- `0001104659-26-092033:8k_2_02:76` — heading
- `0001104659-26-092033:8k_2_02:77` — heading
- `0001104659-26-092033:8k_2_02:78` — units caption
- `0001104659-26-092033:8k_2_02:79` — balance sheet table, amounts only
- `0001104659-26-092033:8k_2_02:80` — heading
- `0001104659-26-092033:8k_2_02:81` — heading
- `0001104659-26-092033:8k_2_02:82` — units caption
- `0001104659-26-092033:8k_2_02:83` — cash flow table, amounts only (the Debt issuance costs line is noted in the New Credit Facility item)
- `0001104659-26-092033:8k_2_02:84` — heading
- `0001104659-26-092033:8k_2_02:85` — heading
- `0001104659-26-092033:8k_2_02:86` — units caption
- `0001104659-26-092033:8k_2_02:87` — backlog table Q3, amounts only
- `0001104659-26-092033:8k_2_02:88` — backlog table YTD, amounts only
- `0001104659-26-092033:8k_2_02:89` — heading
- `0001104659-26-092033:8k_2_02:90` — heading
- `0001104659-26-092033:8k_2_02:91` — EPS reconciliation table Q3 2026, amounts only
- `0001104659-26-092033:8k_2_02:92` — same content as 8k_2_02:54 (Q3 adjustments)
- `0001104659-26-092033:8k_2_02:93` — EPS reconciliation table Q3 2025, amounts only
- `0001104659-26-092033:8k_2_02:94` — prior-year Q3 adjustments, amounts only
- `0001104659-26-092033:8k_2_02:95` — EPS reconciliation table YTD 2026, amounts only
- `0001104659-26-092033:8k_2_02:96` — same content as 8k_2_02:59 (YTD adjustments)
- `0001104659-26-092033:8k_2_02:97` — EPS reconciliation table YTD 2025, amounts only
- `0001104659-26-092033:8k_2_02:98` — prior-year YTD adjustments, amounts only
