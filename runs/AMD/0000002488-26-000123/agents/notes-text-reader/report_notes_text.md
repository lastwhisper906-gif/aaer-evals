# Notes text reader: AMD 10-Q 0000002488-26-000123, quarter ended June 27, 2026

## Inputs and scope

- **Files read in full:** input_8k.md, input_controls.md, input_mdna.md, input_notes.md, input_notes_history.md and input_prior_predictions.md.
- **Nothing out of scope is in the directory.** There is no trend table, no prices, abnormal returns or short interest, no other company's files, no prior-run probability and no outcome window.
- **Not in my input:**
  - an auditor's report (the controls file holds only Item 4, as usual for a 10-Q);
  - an Item 1A diff;
  - an Exhibit 21 diff;
  - any Exhibit 10.
- **8-K bodies:** the only one I have is the 2026-08-04 Item 2.02 release (Exhibit 99.1). For every other 8-K I have the item codes only.
- **Prior predictions:** none on record.
- **Note change history:** it covers only four note sections (organization, significant accounting policies, debt, and commitments and contingencies). For every other paragraph carried as text, I have no prior wording.
- **How I sorted those paragraphs:**
  - An item where the text reports a new event, a new stated cause or a forward-looking statement.
  - "Amounts only" or "date rolled forward" where that is all the text shows.
  - "Insufficient" where something must have changed but I cannot tell what.
- **No arithmetic.** I did none. Where an item says a figure rose or fell, that is what the prose says.

## Items

```json
[
  {
    "id": "results_against_expectations_net_revenue_growth_drivers",
    "what_changed": "MD&A states this quarter's net revenue as $11.5 billion, 'a 50% increase', and names three drivers: Data Center (EPYC processors and Instinct MI350 Series GPUs), Client and Gaming (Ryzen processors), and Embedded ('as demand strengthened across end markets'). The prose says revenue rose; whether the segment figures bear that out is the numbers reader's finding.",
    "account": "Net revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Net revenue for the three months ended June 27, 2026 was $11.5 billion, a 50% increase compared to the prior year period.",
    "paragraph_id": "0000002488-26-000123:mdna:12",
    "explanation": false
  },
  {
    "id": "earnings_quality_gross_margin_lapping_export_control_charge",
    "what_changed": "MD&A says gross margin was 54% against 40% and gives two causes: the absence of the prior-year inventory and related charges from the U.S. export control on Instinct MI308 products, and a favorable mix that includes higher Data Center revenue. One of the two stated causes is a prior-period charge that did not recur, not anything in this quarter's operations. The six-month paragraph (mdna:45) gives the same causes. The 10-Q calls the change 'a 14% increase' while the release (8k_2_02:17) says 'Up 14 ppts'; that difference is wording only.",
    "account": "Gross margin",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "a 14% increase primarily driven by the absence of inventory and related charges associated with the U.S. government export control on AMD Instinct MI308 Data Center GPU products that was recorded in the prior year period and a favorable product mix",
    "paragraph_id": "0000002488-26-000123:mdna:13",
    "explanation": false
  },
  {
    "id": "earnings_quality_net_income_attributed_to_operating_income",
    "what_changed": "MD&A credits the rise in net income 'primarily' to higher operating income. Two other paragraphs of the same MD&A bear on that. mdna:57 attributes the rise in other income primarily to unrealized gains on newly listed equity securities. mdna:61 says the prior-year period carried a discrete tax benefit from the release of uncertain tax positions. Whether 'primarily' still holds once those two are set apart is a question for the numbers reader.",
    "account": "Net income",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase in net income was primarily driven by higher operating income.",
    "paragraph_id": "0000002488-26-000123:mdna:14",
    "explanation": false
  },
  {
    "id": "results_against_expectations_data_center_revenue_epyc_and_instinct_demand",
    "what_changed": "MD&A says Data Center revenue rose 107% for the quarter and 81% for the six months, primarily on strong demand for EPYC processors and Instinct MI350 Series GPUs. This is the period's stated driver. The release adds an expectation of second-half acceleration, which is itemised separately.",
    "account": "Data Center segment net revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase in both periods was primarily driven by strong demand for our AMD EPYC processors and AMD Instinct MI350 Series GPUs.",
    "paragraph_id": "0000002488-26-000123:mdna:26",
    "explanation": false
  },
  {
    "id": "earnings_quality_data_center_operating_income_lapping_export_control_charge",
    "what_changed": "MD&A attributes Data Center's move from a prior-year operating loss to operating income primarily to two things: higher revenue, and the absence of the prior-year MI308 inventory and related charges. It says higher cost of sales and operating expenses partly offset them. As with gross margin, part of the stated improvement rests on a prior-period charge that did not recur.",
    "account": "Data Center segment operating income",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "primarily driven by higher revenue and the absence of inventory and related charges associated with the U.S. government export control on AMD Instinct MI308 Data Center GPU products that was recorded in the prior year period, partially offset by higher cost of sales and operating expenses",
    "paragraph_id": "0000002488-26-000123:mdna:27",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_client_selling_price_mix_shift",
    "what_changed": "MD&A says Client revenue rose 23% for the quarter on a 34% increase in client processor unit shipments, partly offset by a 6% decrease in average selling price. For the six months it says units rose 29% and average selling price fell 3%. It attributes the price decline to a shift in the mix of Ryzen sales, including lower Ryzen desktop processor sales. On the prose, growth comes from volume while price and mix work against it.",
    "account": "Client net revenue (average selling price)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "the decrease in average selling price in both periods was primarily due to a shift in mix of Ryzen processor sales, including lower AMD Ryzen desktop processors sales",
    "paragraph_id": "0000002488-26-000123:mdna:30",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_gaming_semi_custom_decline",
    "what_changed": "MD&A says Gaming revenue decreased 31% for the quarter, primarily because of lower semi-custom revenue. For the six months it says revenue decreased 15%, partly offset by higher Radeon GPU sales. The release (8k_2_02:24) gives the same cause.",
    "account": "Gaming net revenue",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Gaming net revenue of $779 million for the three months ended June 27, 2026 decreased by 31% compared to net revenue of $1.1 billion for the prior year period",
    "paragraph_id": "0000002488-26-000123:mdna:31",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_client_and_gaming_operating_income_decline",
    "what_changed": "MD&A says Client and Gaming operating income decreased in both periods, primarily because of higher operating expenses. The same MD&A says segment revenue increased 6% and 13% (mdna:29). The prose ties the lower segment profit to cost growth, not to revenue.",
    "account": "Client and Gaming segment operating income",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The decrease in operating income in both periods was primarily due to higher operating expenses.",
    "paragraph_id": "0000002488-26-000123:mdna:32",
    "explanation": false
  },
  {
    "id": "results_against_expectations_embedded_demand_strengthened",
    "what_changed": "MD&A says Embedded revenue increased 19% for the quarter and 12% for the six months 'as demand strengthened across end markets'. The release says 'across multiple end markets'.",
    "account": "Embedded segment net revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Net revenue increased in both periods as demand strengthened across end markets.",
    "paragraph_id": "0000002488-26-000123:mdna:34",
    "explanation": false
  },
  {
    "id": "results_against_expectations_embedded_operating_income_on_revenue",
    "what_changed": "MD&A says Embedded operating income increased in both periods, primarily on higher revenue, partly offset by higher cost of sales and operating expenses.",
    "account": "Embedded segment operating income",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase in operating income in both periods was primarily driven by higher revenue, partially offset by higher cost of sales and operating expenses.",
    "paragraph_id": "0000002488-26-000123:mdna:35",
    "explanation": false
  },
  {
    "id": "results_against_expectations_research_and_development_headcount_growth",
    "what_changed": "MD&A says R&D expense rose 33% for the quarter and 36% for the six months. It attributes both primarily to higher employee-related costs from more headcount in support of the AI strategy and long-term growth opportunities.",
    "account": "Research and development expense",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "an increase in headcount in support of our continued focus on our AI strategy",
    "paragraph_id": "0000002488-26-000123:mdna:48",
    "explanation": false
  },
  {
    "id": "results_against_expectations_marketing_general_and_administrative_go_to_market",
    "what_changed": "MD&A says MG&A expense rose 41% in both periods, primarily from more go-to-market activities to support revenue growth.",
    "account": "Marketing, general and administrative expense",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "market activities to support our revenue growth",
    "paragraph_id": "0000002488-26-000123:mdna:50",
    "explanation": false
  },
  {
    "id": "results_against_expectations_intangible_amortization_fully_amortized_assets",
    "what_changed": "MD&A says amortization of acquisition-related intangibles decreased 4% in both periods, primarily because certain intangibles were fully amortized in the prior fiscal year.",
    "account": "Amortization of acquisition-related intangibles",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "intangibles that were fully amortized in the prior fiscal year",
    "paragraph_id": "0000002488-26-000123:mdna:52",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_interest_expense_absent_commercial_paper",
    "what_changed": "MD&A says interest expense for the quarter decreased, primarily because there were no commercial paper borrowings. It says six-month interest expense increased because of the 4.212% and 4.319% Notes issued on March 24, 2025.",
    "account": "Interest expense",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The decrease for the three month period was primarily due to the absence of commercial paper borrowings.",
    "paragraph_id": "0000002488-26-000123:mdna:54",
    "explanation": false
  },
  {
    "id": "earnings_quality_other_income_unrealized_listing_gains",
    "what_changed": "This is a new stated cause. MD&A attributes the rise in other income in both periods primarily to unrealized gains when non-marketable equity securities listed on a public market during the second quarter of fiscal 2026. The gains are unrealized, marked to market and non-operating. The notes say part of the listed holdings carry sale restrictions that expire through October 2028 (notes:47). The release removes '(Gains) loss on long-term investments, net' from non-GAAP net income (8k_2_02:56). From now on, the quoted price of these holdings runs through other income every quarter, in either direction.",
    "account": "Other income (expense), net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "unrealized gains from the public market listing of non-marketable equity securities during the second quarter of fiscal year 2026",
    "paragraph_id": "0000002488-26-000123:mdna:57",
    "explanation": false
  },
  {
    "id": "across_documents_discontinued_operations_cause_tax_versus_measurement_period",
    "what_changed": "MD&A says the discontinued-operations result for the quarter and the six months 'included tax provision adjustments', and names nothing else. The release footnote (8k_2_02:58) says discontinued operations include the effect of measurement period adjustments in Q1 2026. notes:28 records a $243 million working-capital payment to the buyer that includes measurement-period effects. The 10-Q MD&A names only the tax adjustments.",
    "account": "Income (loss) from discontinued operations, net of tax",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "included tax provision adjustments",
    "paragraph_id": "0000002488-26-000123:mdna:63",
    "explanation": false
  },
  {
    "id": "controls_audit_and_filings_subsequent_commitments_and_current_reports",
    "what_changed": "MD&A (and notes:63 and notes:88) disclose two undertakings entered after June 27, 2026: investment commitments of up to $5.0 billion, and data center leases with $9.5 billion of future payments. In the item-code list, the filings dated after the quarter end are 2026-07-01 (Item 5.02) and 2026-08-04 (Items 2.02, 7.01 and 9.01); neither carries Item 1.01 or Item 2.03. My input names no counterparty to either undertaking. Whether either needed a current report is a judgment for the supervisors.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Subsequent to June 27, 2026, we entered into investment commitments of up to $5.0 billion, subject to certain conditions",
    "paragraph_id": "0000002488-26-000123:mdna:71",
    "explanation": false
  },
  {
    "id": "earnings_quality_receivables_increase_attributed_to_revenue",
    "what_changed": "MD&A explains the six-month rise in accounts receivable as 'driven primarily by higher revenue'. That is management's stated cause. Whether receivables moved in line with revenue is for the numbers reader. The same paragraph names no inventory driver among the primary drivers of working-capital change.",
    "account": "Accounts receivable, net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "a $966 million increase in accounts receivable driven primarily by higher revenue",
    "paragraph_id": "0000002488-26-000123:mdna:75",
    "explanation": true
  },
  {
    "id": "liquidity_and_capital_supply_agreement_prepayments",
    "what_changed": "MD&A says prepaid expenses and other assets rose primarily because of prepayments under supply agreements, meaning cash paid to suppliers before delivery. It does not name the suppliers or give the terms.",
    "account": "Prepaid expenses and other assets",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "a $1.0 billion increase in prepaid expenses and other assets primarily due to prepayments of supply agreements",
    "paragraph_id": "0000002488-26-000123:mdna:75",
    "explanation": false
  },
  {
    "id": "earnings_quality_payables_timing_supports_operating_cash_flow",
    "what_changed": "MD&A attributes the rise in accounts payable primarily to 'timing of payment obligations'. That rise supports this period's operating cash flow. A payables build the company itself calls timing implies a later unwind, with lower payables and operating cash flow.",
    "account": "Accounts payable (operating cash flow)",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "partially offset by a $2.2 billion increase in accounts payable primarily due to timing of payment obligations",
    "paragraph_id": "0000002488-26-000123:mdna:75",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_prior_period_reclassification",
    "what_changed": "A new sentence under significant accounting policies (confirmed by the note change history) says certain prior-period amounts were reclassified to match the current presentation. It does not say which line items or amounts. Prior-period comparatives in this filing may therefore not match the figures as first filed.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Prior Period Reclassification. Certain amounts in prior period were reclassified to conform to current period presentation.",
    "paragraph_id": "0000002488-26-000123:notes:5",
    "explanation": false
  },
  {
    "id": "across_documents_acquisition_related_costs_definition",
    "what_changed": "The 10-Q segment note defines acquisition-related and other costs as primarily certain compensation charges and transaction costs. The release footnote (8k_2_02:58) defines the same non-GAAP adjustment as primarily transaction costs, purchase price fair value adjustments for inventory, certain compensation charges and workforce rebalancing charges. The two documents describe the same line differently. The note change history does not cover this paragraph, so I cannot see whether the 10-Q wording itself changed.",
    "account": "Acquisition-related and other costs (All Other)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "and other costs primarily include certain compensation charges and transaction costs.",
    "paragraph_id": "0000002488-26-000123:notes:19",
    "explanation": false
  },
  {
    "id": "articulation_and_the_filed_history_zt_systems_measurement_period_working_capital_payment",
    "what_changed": "A new sentence says that during the quarter the Company paid $243 million to Sanmina for customary post-closing net working-capital adjustments on the sale of the ZT Manufacturing Business, including adjustments that came from measurement period adjustments on the ZT Systems acquisition. Two other places pick this up. The goodwill table (notes:34) carries a 'Measurement period adjustments related to prior acquisitions' row in Data Center. The release cash flow statement adds a 'Payment for working capital adjustment on divestiture' line under discontinued operations. Together they revise acquisition accounting already filed for a business acquired in March 2025 and sold in October 2025.",
    "account": "Net cash used in investing activities of discontinued operations",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "During the three months ended June 27, 2026, the Company made a payment of $243 million",
    "paragraph_id": "0000002488-26-000123:notes:28",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_immaterial_acquisition_mext",
    "what_changed": "The note says the Company completed acquisitions in the periods presented that were immaterial individually and in aggregate. The release lists 'Acquired MEXT' among its highlights (8k_2_02:37). The goodwill table (notes:34) carries a 'Current period acquisitions' row in Data Center, and the release cash flow statement shows acquisitions, net of cash acquired, for the quarter. The note names no acquiree and gives no purchase price allocation, and the history does not cover this paragraph's prior wording.",
    "account": "Goodwill (Data Center)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "For the periods presented, the Company also completed acquisitions that were immaterial both individually and in aggregate.",
    "paragraph_id": "0000002488-26-000123:notes:31",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_listed_equity_moved_to_quoted_prices",
    "what_changed": "A new sentence says long-term investments now consist mainly of previously non-marketable equity securities that became publicly traded in the second quarter of fiscal 2026. They were reclassified to Level 1 once quoted prices were available. The note puts net unrealized gains on marketable equity securities at $425 million at June 27, 2026 and calls them 'not material' at December 27, 2025. Measurement moves from observable events and impairments to quoted market prices, so each quarter's price movement now runs through other income. notes:47 says part of these holdings are under sale restrictions through October 2028.",
    "account": "Long-term investments (Other non-current assets)",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "equity securities that became publicly traded during the second quarter of fiscal year 2026 and were reclassified to Level 1 upon the availability of quoted market prices",
    "paragraph_id": "0000002488-26-000123:notes:46",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_non_marketable_equity_cumulative_upward_adjustments",
    "what_changed": "The paragraph gives cumulative gross unrealized gains of $118 million on non-marketable equity investments at June 27, 2026, and calls losses and impairments not material. Its comparative sentence calls 2025 gains, impairments and losses not material. These investments are carried 'based on observable events or adjustments from impairments' (notes:61). That makes the gains upward remeasurements that rest on management identifying observable transactions in private companies. I cannot see the Q1 wording, so I cannot say whether the $118 million disclosure is new this quarter.",
    "account": "Non-marketable equity investments (Other non-current assets)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "equity investments had cumulative gross unrealized gains of $118 million",
    "paragraph_id": "0000002488-26-000123:notes:62",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_investment_commitments_after_quarter_end",
    "what_changed": "A new subsequent-event sentence says that after June 27, 2026 the Company entered into investment commitments of up to $5.0 billion. They are subject to certain contingencies ('conditions' in MD&A mdna:71) and are expected to be made through fiscal 2028. The investee is not named. When funded, they should show as purchases of long-term investments.",
    "account": "Purchases of long-term investments",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Subsequent to June 27, 2026, the Company entered into investment commitments of up to $5.0 billion, subject to certain contingencies, which are expected to be made through fiscal year 2028.",
    "paragraph_id": "0000002488-26-000123:notes:63",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_partner_data_center_lease_guarantees",
    "what_changed": "A 'Lease Guarantees' paragraph in the derivatives note gives a maximum gross exposure of $4.1 billion on guarantees of commercial partners' data center lease obligations, with terms up to 15 years. The guarantees become payable if a partner defaults and may be issued in exchange for warrants. They are carried as a credit derivative within Other long-term liabilities, with fair-value changes in other income, and are called not material. MD&A mdna:71 repeats the $4.1 billion. The note change history does not cover this section, so I cannot tell whether the paragraph is new this quarter or only rolled forward. Either way, the text describes exposure to partners' credit that the balance sheet holds only at fair value.",
    "account": "Other long-term liabilities (guarantee credit derivative); off-balance-sheet guarantee exposure",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "As of June 27, 2026, the Company had a maximum gross exposure of $4.1 billion from guarantees issued in connection with certain commercial partner data center lease obligations with terms up to 15 years.",
    "paragraph_id": "0000002488-26-000123:notes:70",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_revolving_credit_facility_replaced",
    "what_changed": "A new paragraph (the history shows it added) says that in May 2026 the Company entered into a five-year $5.0 billion unsecured revolving facility, replacing the $3.0 billion facility from April 2022. Up to $250 million may be used for letters of credit. Borrowings bear a variable rate plus a margin based on credit ratings, and there is a commitment fee. The Company is in compliance and nothing is drawn. The removed prior paragraph said the old facility expired on April 29, 2027; MD&A (mdna:69) now says the facility expires in 2031. The 2026-05-15 8-K carries Items 1.01, 1.02 and 2.03, consistent with entering one facility and ending another. The prose does not itself say whether capacity rose, so I leave direction to the numbers reader.",
    "account": "Revolving credit facility (undrawn borrowing capacity)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "replacing its prior $3.0 billion revolving credit facility entered into in April 2022",
    "paragraph_id": "0000002488-26-000123:notes:82",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_commercial_paper_program_capacity_raised",
    "what_changed": "The commercial paper paragraph now says that in May 2026 the Company 'increased to $5.5 billion, from $3.0 billion' the most it may have outstanding under the program. The prior text described a $3.0 billion program. No paper is outstanding at either date, and MD&A (mdna:69) repeats the $5.5 billion. This is capacity, not borrowing.",
    "account": "Commercial paper program capacity (undrawn)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "In May 2026, the Company increased to $5.5 billion, from $3.0 billion, the maximum aggregate amount outstanding at any time of unsecured commercial paper notes",
    "paragraph_id": "0000002488-26-000123:notes:83",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_cloud_compute_capacity_commitments",
    "what_changed": "The commitments paragraph changed in two places. It now describes 'commitments for multi-year cloud compute capacity arrangements with cloud service providers (CSP)', where it said 'future payments related to multi-year cloud service provider (CSP), software, and technology license agreements'. It now says 'Cloud compute capacity may be reduced, terminated or sold to others by the CSPs', where it said 'Some cloud service capacity may be reduced...'. With 'Some' gone, the reduce/terminate/resell language reads as covering the cloud capacity commitments generally. The Company still expects to use the capacity or assign it to third parties. MD&A mdna:71 keeps the older 'future payments related to multi-year cloud service provider arrangements' wording.",
    "account": "Unconditional purchase commitments",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Cloud compute capacity may be reduced, terminated or sold to others by the CSPs",
    "paragraph_id": "0000002488-26-000123:notes:85",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_data_center_leases_signed_after_quarter_end",
    "what_changed": "A new subsequent-event sentence (confirmed by the history) says that after June 27, 2026 the Company entered into long-term data center leases. They carry $9.5 billion of aggregate future payments over terms of up to 16 years and are expected to commence in 2027 and 2028. MD&A mdna:71 repeats it. The leases stay off the balance sheet until commencement. When they commence, they should add operating lease liabilities and right-of-use assets, some of it beyond 12 months.",
    "account": "Operating lease liabilities and right-of-use assets",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "data center leases with aggregate future payments of $9.5 billion over lease terms of up to 16 years and these leases are expected to commence in 2027 and 2028",
    "paragraph_id": "0000002488-26-000123:notes:88",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_uncommenced_leases_commencement_wording_changed",
    "what_changed": "The sentence on leases not yet commenced changed. It now says $4.5 billion of future payments, terms of 6 to 11 years, 'expected to commence beginning in the second half of fiscal year 2026'. The prior filing said $4.4 billion, terms of 7 to 10 years, 'expected to commence beginning in the second quarter of fiscal year 2026'. So the wording on when commencement is expected changed. When the leases commence they come onto the balance sheet as operating lease liabilities and right-of-use assets. The old and new amounts are given only as the prose states them.",
    "account": "Operating lease liabilities and right-of-use assets",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "These leases are expected to commence beginning in the second half of fiscal year 2026.",
    "paragraph_id": "0000002488-26-000123:notes:88",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_treasury_share_retirement",
    "what_changed": "A new paragraph says that during the quarter the Company retired 66.9 million treasury shares, which returned to authorized but unissued status. The excess of purchase price over par was split between additional paid-in capital and retained earnings. The release balance sheet shows a dash for treasury stock at June 27, 2026. On the prose, retained earnings and APIC absorb a reclassification this quarter that is neither an earnings event nor a cash event. The quarter's movement in retained earnings therefore does not come from income and distributions alone.",
    "account": "Retained earnings and additional paid-in capital",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "During the three months ended June 27, 2026, the Company retired 66.9 million of treasury shares, which returned to the status of authorized but unissued shares.",
    "paragraph_id": "0000002488-26-000123:notes:98",
    "explanation": false
  },
  {
    "id": "across_documents_customer_warrant_vesting_and_helios_ramp",
    "what_changed": "The note restates, as of June 27, 2026, that no OpenAI or Meta warrant shares had vested or become exercisable and that the warrants had no effect on the statements. It says they 'will be classified as liabilities until certain conditions for equity classification are met'. Vesting is tied to Instinct GPU purchase milestones and stock price targets, plus stock-performance thresholds for OpenAI, and each vested tranche faces further technical and commercial conditions. MD&A mdna:16 says MI450 powers the first gigawatt of each deployment. The release (8k_2_02:13) says Helios begins to ramp in the second half. So the first purchase milestones are what to watch: on the text, a vested tranche brings a liability-classified instrument onto the books. I cannot see this paragraph's prior wording, so I cannot confirm whether the liability-classification sentence is new.",
    "account": "Warrant liabilities; Data Center net revenue",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "The warrants will be classified as liabilities until certain conditions for equity classification are met.",
    "paragraph_id": "0000002488-26-000123:notes:102",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_equity_incentive_plan_share_increase",
    "what_changed": "A new paragraph says that on May 13, 2026 the 2023 Equity Incentive Plan was amended and restated. The amendment increased the shares authorized under it by 65 million, to 153 million, and 107 million remain available. The item-code list shows a 2026-05-15 8-K carrying Items 5.02 and 5.07, which fits shareholder approval; its body is not in my input. More authorized shares means more room for future grants, which bears on stock-based compensation and dilution.",
    "account": "Shares available under the equity plan (stock-based compensation, dilution)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "On May 13, 2026, the Company amended and restated its 2023 Equity Incentive Plan (the Plan), increasing the authorized shares for issuance under the Plan by 65 million to a total of 153 million shares of common stock.",
    "paragraph_id": "0000002488-26-000123:notes:106",
    "explanation": false
  },
  {
    "id": "results_against_expectations_data_center_second_half_acceleration",
    "what_changed": "The CFO says the Company expects Data Center sales to accelerate in the second half of 2026, bringing stronger overall revenue growth and continued earnings expansion. The CEO (8k_2_02:13) says the Company enters the second half as EPYC demand accelerates, Instinct deployments scale and Helios begins to ramp. These are forward-looking statements made in this release.",
    "account": "Data Center segment net revenue",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "We expect Data Center sales to accelerate in the second half of 2026, driving stronger overall revenue growth and continued earnings expansion.",
    "paragraph_id": "0000002488-26-000121:8k_2_02:14",
    "explanation": false
  },
  {
    "id": "across_documents_anthropic_helios_deployment_partnership",
    "what_changed": "The release's highlights announce a strategic partnership with Anthropic to deploy up to 2 gigawatts of MI450 Series GPUs in Helios racks, and list Anthropic among Helios deployers (8k_2_02:28). The 10-Q prose carried as text in my input describes multi-year deployment agreements and customer warrants only for OpenAI and Meta (mdna:16, notes:102) and does not mention Anthropic. It also names no counterparty to the post-quarter investment commitments, the partner lease guarantees or the new data center leases. My input does not say whether any of these relate to the partnership.",
    "account": "Data Center segment net revenue",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Announced a strategic partnership with Anthropic to deploy up to 2 gigawatts of MI450 Series GPUs in AMD Helios racks",
    "paragraph_id": "0000002488-26-000121:8k_2_02:33",
    "explanation": false
  },
  {
    "id": "results_against_expectations_third_quarter_revenue_outlook",
    "what_changed": "The release gives a third-quarter 2026 outlook: revenue of approximately $13 billion, plus or minus $300 million. The company says the midpoint represents about 41% year-over-year growth and a sequential increase of about 13%. It guides non-GAAP gross margin to about 56%.",
    "account": "Net revenue",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "For the third quarter of 2026, AMD expects revenue to be approximately $13 billion, plus or minus $300 million.",
    "paragraph_id": "0000002488-26-000121:8k_2_02:51",
    "explanation": false
  },
  {
    "id": "across_documents_legal_loss_contingency_excluded_from_non_gaap",
    "what_changed": "The release's reconciliations carry a 'Loss contingency on legal matters' adjustment. It appears in the column for the three months ended June 27, 2026 in the gross-profit, operating-income, net-income and Adjusted EBITDA reconciliations, with dashes in the comparison columns. The Adjusted EBITDA definition (8k_2_02:89) now names it. The 10-Q contingencies note (notes:90) changes only its date and says there were no material legal proceedings in the quarter. Neither that note nor any other 10-Q paragraph in my input describes the matter or the accrual. Whether the two documents are consistent turns on materiality, which I leave to the supervisors.",
    "account": "Cost of sales and accrued liabilities (legal loss contingency)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "loss contingency on legal matters, and loss (income) from discontinued operations",
    "paragraph_id": "0000002488-26-000121:8k_2_02:89",
    "explanation": false
  },
  {
    "id": "controls_audit_and_filings_officer_director_change_without_body",
    "what_changed": "A Form 8-K carrying only Item 5.02 (departure, election or appointment of directors or officers, or compensatory arrangements) was filed on 2026-07-01, after the prior 10-Q. Its body is not in my input, so I cannot say who or what changed. This is insufficient beyond the fact that the filing exists.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "2026-07-01 0000002488-26-000115",
    "paragraph_id": "input_8k.md: item codes, every 8-K on or before 2026-08-05",
    "explanation": false
  }
]
```

## Paragraphs carried as text with no item

Insufficient answers: 9 in total. Eight are paragraphs marked "insufficient" below, and one is the item `controls_audit_and_filings_officer_director_change_without_body`.

Paragraphs marked `[same as prior period ...]` are not listed. The note-history entries are accounted for through the notes paragraphs they map to. The removed prior paragraphs map as follows:
- 0000002488-26-000076:note_history:6 was replaced by notes:1.
- :17 was merged into notes:76.
- :18 was replaced by notes:79.
- :19 (the old revolver) is covered in the revolver item.

### Item 4 controls
- 0000002488-26-000123:item_4_controls:1 — heading
- 0000002488-26-000123:item_4_controls:2 — standard disclosure-controls design language; no change discernible
- 0000002488-26-000123:item_4_controls:3 — effectiveness conclusion; date rolled forward, still effective
- 0000002488-26-000123:item_4_controls:4 — no changes in internal control; date rolled forward
- 0000002488-26-000123:item_4_controls:5 — page number

### MD&A
- 0000002488-26-000123:mdna:11 — introduction; period rolled forward
- 0000002488-26-000123:mdna:15 — amounts and period rolled forward; repurchase figure repeats notes:100
- 0000002488-26-000123:mdna:16 — warrant status restated as of new date; itemised at notes:102
- 0000002488-26-000123:mdna:20 — no change to critical accounting estimates; date rolled forward
- 0000002488-26-000123:mdna:24 — segment table; amounts only
- 0000002488-26-000123:mdna:29 — Client and Gaming revenue amounts; no cause stated (causes itemised at mdna:30, mdna:31)
- 0000002488-26-000123:mdna:37 — All Other quarterly composition; amounts only
- 0000002488-26-000123:mdna:38 — All Other six-month composition; amounts only
- 0000002488-26-000123:mdna:40 — international sales share; amounts only
- 0000002488-26-000123:mdna:43 — results table; amounts only
- 0000002488-26-000123:mdna:45 — six-month restatement of the gross-margin causes itemised at mdna:13
- 0000002488-26-000123:mdna:47 — heading
- 0000002488-26-000123:mdna:49 — heading
- 0000002488-26-000123:mdna:56 — insufficient: definition of other income; prior wording not in input, cannot tell what changed
- 0000002488-26-000123:mdna:60 — tax provision and rate; amounts and period rolled, no direction claim (same as notes:109)
- 0000002488-26-000123:mdna:61 — prior-year comparative tax prose rolled to six months
- 0000002488-26-000123:mdna:66 — cash and short-term investments; amounts only, repeats mdna:15
- 0000002488-26-000123:mdna:67 — lead-in sentence; period rolled forward
- 0000002488-26-000123:mdna:68 — cash flow table; amounts only
- 0000002488-26-000123:mdna:69 — restates the revolver and commercial paper changes itemised at notes:82 and notes:83
- 0000002488-26-000123:mdna:70 — debt principal; amounts only
- 0000002488-26-000123:mdna:72 — insufficient: liquidity-sufficiency statement; prior wording not in input and nothing in it reads as new
- 0000002488-26-000123:mdna:76 — prior-year comparative operating cash flow prose rolled to six months
- 0000002488-26-000123:mdna:78 — investing cash flows; amounts only; the $243 million payment is itemised at notes:28
- 0000002488-26-000123:mdna:79 — prior-year comparative investing prose
- 0000002488-26-000123:mdna:81 — financing cash flows; amounts only
- 0000002488-26-000123:mdna:82 — prior-year comparative financing prose

### Notes
- 0000002488-26-000123:notes:1 — product list reordered; 'data center and professional GPUs' dropped while GPUs stay listed; wording only
- 0000002488-26-000123:notes:2 — period rolled forward
- 0000002488-26-000123:notes:3 — period rolled forward (13 and 26 weeks)
- 0000002488-26-000123:notes:4 — note history shows no change; standard use-of-estimates language
- 0000002488-26-000123:notes:7 — inventory table; amounts only
- 0000002488-26-000123:notes:8 — property and equipment table; amounts only
- 0000002488-26-000123:notes:9 — accrued liabilities table; amounts only
- 0000002488-26-000123:notes:11 — remaining performance obligations; amounts and date only
- 0000002488-26-000123:notes:12 — share of revenue recognized over time; amounts only
- 0000002488-26-000123:notes:21 — segment table; amounts only
- 0000002488-26-000123:notes:22 — All Other footnote; amounts only
- 0000002488-26-000123:notes:24 — insufficient: ZT acquisition and its October 2025 settlement were already past at the prior filing; prior wording not in input
- 0000002488-26-000123:notes:25 — insufficient: description of the retained business and the divestiture; prior wording not in input
- 0000002488-26-000123:notes:29 — insufficient: earn-out terms and receivable restated as of new date; prior wording and amount not in input; no change of method stated
- 0000002488-26-000123:notes:30 — pro forma omission; no change in substance
- 0000002488-26-000123:notes:34 — goodwill table; its rows are cited in the items from notes:28 and notes:31
- 0000002488-26-000123:notes:37 — intangibles table; amounts only
- 0000002488-26-000123:notes:38 — amortization expense; amounts only
- 0000002488-26-000123:notes:39 — lead-in; date rolled forward
- 0000002488-26-000123:notes:40 — future amortization table; amounts only
- 0000002488-26-000123:notes:41 — equity-method carrying value; amounts only
- 0000002488-26-000123:notes:42 — related-party purchases, payables and term loan; amounts and dates only
- 0000002488-26-000123:notes:43 — equity income not material; period rolled forward
- 0000002488-26-000123:notes:45 — fair value table; amounts only (the Level 1 reclassification is itemised at notes:46)
- 0000002488-26-000123:notes:47 — sale-restricted marketable equity; amounts only (context for the notes:46 item)
- 0000002488-26-000123:notes:50 — available-for-sale table; amounts only
- 0000002488-26-000123:notes:51 — continuous-loss statement; date rolled forward
- 0000002488-26-000123:notes:53 — maturities table; amounts only
- 0000002488-26-000123:notes:56 — debt fair value table; amounts only
- 0000002488-26-000123:notes:60 — insufficient: description of non-marketable investments; prior wording not in input
- 0000002488-26-000123:notes:61 — non-marketable carrying value; amounts only
- 0000002488-26-000123:notes:66 — cash flow hedge notional; amounts only
- 0000002488-26-000123:notes:68 — non-designated hedge notional; amounts only
- 0000002488-26-000123:notes:71 — heading
- 0000002488-26-000123:notes:72 — date rolled forward (history)
- 0000002488-26-000123:notes:73 — debt table; amounts only (history)
- 0000002488-26-000123:notes:74 — heading
- 0000002488-26-000123:notes:75 — March 2025 issuance terms; no change shown
- 0000002488-26-000123:notes:76 — reordered: the holders' change-of-control sentence was merged in from its own paragraph (history); terms unchanged
- 0000002488-26-000123:notes:77 — heading reorganised to group the three older note series
- 0000002488-26-000123:notes:78 — interest terms restated under the reorganised heading; no change in terms stated
- 0000002488-26-000123:notes:79 — insufficient: the reorganised paragraph now includes the 2.375% Notes (history 'added'); my input does not show whether their terms appeared elsewhere before; no change in terms stated
- 0000002488-26-000123:notes:80 — date rolled forward (history)
- 0000002488-26-000123:notes:81 — heading
- 0000002488-26-000123:notes:84 — heading
- 0000002488-26-000123:notes:86 — date rolled forward (history)
- 0000002488-26-000123:notes:87 — commitments table; amounts only
- 0000002488-26-000123:notes:89 — heading
- 0000002488-26-000123:notes:90 — date rolled forward (history); set against the release's legal loss contingency in the item from 8k_2_02:89
- 0000002488-26-000123:notes:92 — EPS table; amounts only
- 0000002488-26-000123:notes:96 — share activity table; amounts only
- 0000002488-26-000123:notes:97 — heading
- 0000002488-26-000123:notes:100 — repurchase program; amounts and period rolled forward
- 0000002488-26-000123:notes:105 — stock-based compensation table; amounts only
- 0000002488-26-000123:notes:109 — tax provision and rate; amounts and period rolled forward, no direction claim
- 0000002488-26-000123:notes:110 — prior-year comparative tax prose
- 0000002488-26-000123:notes:111 — liability for unrecognized tax benefits; amounts only, no cause stated

### 8-K item 2.02 (Exhibit 99.1)
- 0000002488-26-000121:8k_2_02:1 — exhibit header
- 0000002488-26-000121:8k_2_02:2 — document label
- 0000002488-26-000121:8k_2_02:3 — heading
- 0000002488-26-000121:8k_2_02:4 — contact heading
- 0000002488-26-000121:8k_2_02:5 — contact name
- 0000002488-26-000121:8k_2_02:6 — contact affiliation
- 0000002488-26-000121:8k_2_02:7 — contact email
- 0000002488-26-000121:8k_2_02:8 — contact name
- 0000002488-26-000121:8k_2_02:9 — contact affiliation
- 0000002488-26-000121:8k_2_02:10 — contact email
- 0000002488-26-000121:8k_2_02:11 — headline
- 0000002488-26-000121:8k_2_02:12 — headline results; amounts only (results prose itemised from the 10-Q MD&A)
- 0000002488-26-000121:8k_2_02:13 — CEO outlook; covered by the item from 8k_2_02:14
- 0000002488-26-000121:8k_2_02:15 — page number
- 0000002488-26-000121:8k_2_02:16 — table heading
- 0000002488-26-000121:8k_2_02:17 — GAAP results table; amounts only
- 0000002488-26-000121:8k_2_02:18 — prior-year MI308 charge footnote; comparative, cause itemised at mdna:13
- 0000002488-26-000121:8k_2_02:19 — table heading
- 0000002488-26-000121:8k_2_02:20 — non-GAAP results table; amounts only
- 0000002488-26-000121:8k_2_02:21 — same prior-year footnote as 8k_2_02:18
- 0000002488-26-000121:8k_2_02:22 — heading
- 0000002488-26-000121:8k_2_02:23 — Data Center summary; same driver as mdna:26
- 0000002488-26-000121:8k_2_02:24 — Client and Gaming summary; same drivers as mdna:30 and mdna:31
- 0000002488-26-000121:8k_2_02:25 — Embedded summary; same driver as mdna:34
- 0000002488-26-000121:8k_2_02:26 — heading
- 0000002488-26-000121:8k_2_02:27 — highlight lead-in
- 0000002488-26-000121:8k_2_02:28 — Helios launch and deployer list; marketing, with Anthropic and OpenAI/Meta covered in the items from 8k_2_02:33 and notes:102
- 0000002488-26-000121:8k_2_02:29 — product launch (MI400 family)
- 0000002488-26-000121:8k_2_02:30 — continuation of 8k_2_02:29
- 0000002488-26-000121:8k_2_02:31 — product launch (EPYC)
- 0000002488-26-000121:8k_2_02:32 — software release
- 0000002488-26-000121:8k_2_02:34 — Microsoft collaboration; no terms stated
- 0000002488-26-000121:8k_2_02:35 — Cerebras collaboration; no terms stated
- 0000002488-26-000121:8k_2_02:36 — product launch (MI350P)
- 0000002488-26-000121:8k_2_02:37 — MEXT acquisition; covered by the item from notes:31
- 0000002488-26-000121:8k_2_02:38 — highlight lead-in
- 0000002488-26-000121:8k_2_02:39 — product release (Ryzen AI Halo)
- 0000002488-26-000121:8k_2_02:40 — product line extension (Ryzen PRO)
- 0000002488-26-000121:8k_2_02:41 — product launch and platform support
- 0000002488-26-000121:8k_2_02:42 — Cisco collaboration; no terms stated
- 0000002488-26-000121:8k_2_02:43 — product availability (Radeon)
- 0000002488-26-000121:8k_2_02:44 — highlight lead-in
- 0000002488-26-000121:8k_2_02:45 — product launch (embedded)
- 0000002488-26-000121:8k_2_02:46 — product announcement (Kria)
- 0000002488-26-000121:8k_2_02:47 — product launch (Versal)
- 0000002488-26-000121:8k_2_02:48 — page number
- 0000002488-26-000121:8k_2_02:49 — heading
- 0000002488-26-000121:8k_2_02:50 — forward-looking caution; boilerplate
- 0000002488-26-000121:8k_2_02:52 — heading
- 0000002488-26-000121:8k_2_02:53 — call logistics
- 0000002488-26-000121:8k_2_02:54 — page number
- 0000002488-26-000121:8k_2_02:55 — reconciliation table; amounts, with the new legal line covered by the item from 8k_2_02:89
- 0000002488-26-000121:8k_2_02:56 — net income reconciliation; amounts, with the new legal line covered by the item from 8k_2_02:89
- 0000002488-26-000121:8k_2_02:57 — page number
- 0000002488-26-000121:8k_2_02:58 — footnotes: (1) used in the item from notes:19, (2) prior-year tax release, (3) used in the item from mdna:63
- 0000002488-26-000121:8k_2_02:59 — heading
- 0000002488-26-000121:8k_2_02:60 — company description
- 0000002488-26-000121:8k_2_02:61 — heading; the body of the cautionary statement is not in my input
- 0000002488-26-000121:8k_2_02:62 — page number
- 0000002488-26-000121:8k_2_02:63 — insufficient: non-GAAP definitions and the fiscal-2026 non-GAAP tax rate; prior release not in input
- 0000002488-26-000121:8k_2_02:64 — end mark
- 0000002488-26-000121:8k_2_02:65 — trademarks
- 0000002488-26-000121:8k_2_02:66 — page number
- 0000002488-26-000121:8k_2_02:67 — heading
- 0000002488-26-000121:8k_2_02:68 — heading
- 0000002488-26-000121:8k_2_02:69 — heading
- 0000002488-26-000121:8k_2_02:70 — statement of operations; amounts only
- 0000002488-26-000121:8k_2_02:71 — page number
- 0000002488-26-000121:8k_2_02:72 — heading
- 0000002488-26-000121:8k_2_02:73 — heading
- 0000002488-26-000121:8k_2_02:74 — heading
- 0000002488-26-000121:8k_2_02:75 — balance sheet; amounts only (treasury line is context for notes:98)
- 0000002488-26-000121:8k_2_02:76 — heading
- 0000002488-26-000121:8k_2_02:77 — heading
- 0000002488-26-000121:8k_2_02:78 — heading
- 0000002488-26-000121:8k_2_02:79 — cash flow statement; amounts only (working-capital payment line is context for notes:28)
- 0000002488-26-000121:8k_2_02:80 — page number
- 0000002488-26-000121:8k_2_02:81 — heading
- 0000002488-26-000121:8k_2_02:82 — heading
- 0000002488-26-000121:8k_2_02:83 — heading
- 0000002488-26-000121:8k_2_02:84 — selected corporate data; amounts only
- 0000002488-26-000121:8k_2_02:85 — segment description; matches the 10-Q, no change discernible
- 0000002488-26-000121:8k_2_02:86 — page number
- 0000002488-26-000121:8k_2_02:87 — table heading
- 0000002488-26-000121:8k_2_02:88 — Adjusted EBITDA reconciliation; amounts, with the legal line covered by the item from 8k_2_02:89
- 0000002488-26-000121:8k_2_02:90 — table heading
- 0000002488-26-000121:8k_2_02:91 — free cash flow reconciliation; amounts only
- 0000002488-26-000121:8k_2_02:92 — free cash flow definition; standard
- 0000002488-26-000121:8k_2_02:93 — page number

### 8-K item codes and late filings
- 8-K item-code list: only the filings dated after the prior 10-Q are new. 2026-05-15 is cited in the revolver and equity-plan items, 2026-07-01 is its own item, and 2026-08-04 is the release read above.
- Late-filing notifications: none listed; no item.
