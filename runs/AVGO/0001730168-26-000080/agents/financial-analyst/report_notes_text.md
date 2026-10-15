<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# report_notes_text: AVGO 10-Q 0001730168-26-000080 (quarter ended August 2, 2026)

## Input check

- I read all six files in full: input_8k.md, input_controls.md, input_mdna.md, input_notes.md, input_notes_history.md (all 773 lines) and input_prior_predictions.md.
- **Nothing forbidden was found.** There is no trend table, price, abnormal return, short-interest figure, other company's file, prior probability or outcome window. The 8-K exhibit 99.1 contains the company's own condensed statements. I read them as text only and did no arithmetic on them.
- **Prior predictions:** none on record. There are no flags to carry forward.
- **Missing from my directory:**
  - No Item 1A diff, Exhibit 21 diff or Exhibit 10.
  - No auditor's report. This is a 10-Q; input_controls.md carries only Item 4.
  - Only one 8-K body is included: item 2.02 / Ex. 99.1 of 0001730168-26-000076. The bodies of the other listed 8-Ks are not there. That includes the item 8.01 filings of 2026-06-11, 2026-06-18 and 2026-07-06, and the item 5.02 filings of 2026-03-02 and 2026-04-02.
  - The 8-K list shows no late-filing notification on or before 2026-09-10.
- **Limits on what I can compare:**
  - The prior-period MD&A wording is not in my input. For MD&A paragraphs carried as changed, I can say what the text now says, not which words are new.
  - The note change history covers only these note blocks: commitments and contingencies, basis of presentation, debt, revenue and subsequent events. For the other notes (supplemental financial information, intangibles, equity, income taxes, insider trading arrangements), the prior text is not visible.
- **No arithmetic.** Where a paragraph gives a current and a prior figure, I report both as stated and do not compare them.
- **Field conventions:**
  - `explanation` is true only where management explains the cause of a receivables, inventory or reserves number.
  - `insufficient` is true where the item depends on a clause whose newness I cannot confirm from my input.

## Items

```json
{
  "id": "structure_and_disclosure_changes_ai_rack_backstop_moved_from_subsequent_events_into_guarantee_note",
  "what_changed": "Last period this arrangement appeared only as a subsequent event dated June 8, 2026, with an 'investor partner' (0001730168-26-000054:note_history:46, now removed). It is now disclosed in the Commitments and Contingencies note under a new 'Financial Guarantee' heading, as having occurred during the quarter, and the counterparty is now called a 'financial partner'. The text says the company arranged for this partner to take on agreements to purchase AI racks built on the company's custom AI accelerators, and the related compute-capacity leases with a customer.",
  "account": "guarantee obligations / contingent liabilities; semiconductor solutions revenue",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "During the fiscal quarter ended August 2, 2026, we arranged for a financial partner to take on certain agreements to purchase AI racks based on custom AI accelerators designed by us and the related lease agreements with a customer that enable access to compute capacity.",
  "paragraph_id": "0001730168-26-000080:notes:106",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "related_parties_contingencies_and_subsequent_events_backstop_eighty_five_percent_shortfall_formula",
  "what_changed": "New terms not in last period's subsequent-event text (0001730168-26-000054:note_history:46): in a customer lease default the company owes any difference between 85% of the amounts outstanding on the lease and the sale value of the AI racks. The total Backstop amount grows as racks are delivered and deployed and shrinks as the customer pays. Last period's text gave only a 'maximum exposure of $29 billion' and said the backstop 'will increase over time as the AI racks are deployed'. Direction: the prose says the Backstop amount increases as racks are delivered and deployed.",
  "account": "guarantee exposure under the Backstop; loss contingency",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "our Backstop liability will be equal to any difference between 85% of the outstanding amounts owed on the lease Backstop and the value of the AI racks received upon sale of the assets at that time",
  "paragraph_id": "0001730168-26-000080:notes:107",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "related_parties_contingencies_and_subsequent_events_rack_resale_to_seller_at_fixed_price",
  "what_changed": "Names a remedy not in last period's text: reselling the racks back to 'the seller' at a fixed price under certain conditions. Last period listed 'the assumption of the lease or effecting a sale of the AI racks'. The text implies a fixed-price resale right against the rack seller, but doesn't name the seller, give the price or state the conditions. Another listed remedy, assuming the applicable lease, would put the company in the lessee's position.",
  "account": "guarantee exposure; potential lease obligations",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "reselling the AI racks back to the seller at a fixed price under certain conditions",
  "paragraph_id": "0001730168-26-000080:notes:107",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "estimates_and_discretion_backstop_fair_value_judged_not_material",
  "what_changed": "New statements: the fair value of the Backstop 'was not material'; no amounts have been paid; and the maximum potential liability is about $29 billion 'upon the deployment of all AI racks, on an undiscounted basis'. Last period said only 'a maximum exposure of $29 billion'. The text doesn't give the valuation approach or inputs behind 'not material', or say where any recognized amount sits on the balance sheet.",
  "account": "guarantee liability (other current / other long-term liabilities)",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "The fair value of the Backstop was not material.",
  "paragraph_id": "0001730168-26-000080:notes:108",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "related_parties_contingencies_and_subsequent_events_customer_convertible_notes_issuable_to_company",
  "what_changed": "Entirely new disclosure, absent from last period's subsequent-event text. Under the compute-capacity lease agreements, the customer may, 'under certain circumstances and if needed', issue the company convertible promissory notes of up to $42 billion in principal. The notes are subject to conditions, and none had been issued as of August 2, 2026. The text doesn't say whether the company must accept or fund the notes, or give conversion terms or the circumstances. It is not one of the categories in the contractual commitments table (notes:101).",
  "account": "notes receivable / investments (other long-term assets); cash",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "our customer may, under certain circumstances and if needed, issue to us convertible promissory notes up to an aggregate principal amount of $42 billion",
  "paragraph_id": "0001730168-26-000080:notes:110",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "revenue_recognition_customer_lease_payments_may_be_funded_by_company_held_notes",
  "what_changed": "Read with notes:106 and notes:107, the text now describes a circle. A financial partner buys racks built on the company's accelerators and leases them to the customer. The company backstops the customer's lease payments. The customer may fund those lease payments with proceeds of notes it issues to the company, and the text says those proceeds may be used 'solely' for the lease obligations. The notes don't say how this bears on the transaction price or collectability of the related product sales.",
  "account": "semiconductor solutions revenue; trade accounts receivable",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "the requirement to use the notes or proceeds from the notes, if any, solely for the customer",
  "paragraph_id": "0001730168-26-000080:notes:110",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "narrative_signs_of_operating_pressure_customers_must_access_significant_capital",
  "what_changed": "New sentence in a new Recent Developments passage: having described 'unprecedented demand' from customers including the leading frontier AI labs, MD&A now says that meeting that demand 'requires our customers to access significant capital'.",
  "account": "semiconductor solutions revenue; trade accounts receivable",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "However, deploying AI infrastructure to meet this demand requires our customers to access significant capital.",
  "paragraph_id": "0001730168-26-000080:mdna:12",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "narrative_signs_of_operating_pressure_frontier_lab_cash_flows_short_of_investment_needs",
  "what_changed": "New: MD&A says the platform 'bridges the gap' between the frontier AI labs' current cash flows and the upfront investment they need. That is, customers' current cash flows don't cover their deployments of the company's products. In the same paragraph, the low probability of guarantee losses is said to rest on the labs' 'strong profitability trajectory'.",
  "account": "trade accounts receivable; guarantee exposure",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "The AI XPV platform bridges the gap between the current cash flows of the leading frontier AI labs and significant upfront investments required for their businesses.",
  "paragraph_id": "0001730168-26-000080:mdna:13",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "liquidity_and_capital_ai_xpv_platform_planned_twenty_gigawatts",
  "what_changed": "New: MD&A names an 'AI XPV platform', set up with 'certain sophisticated financial partners', to enable more than 20 gigawatts of compute using the company's XPUs and networking through 2028. Note 10 describes only one arrangement and uses neither the platform name nor the 20-gigawatt scope. Direction: the prose implies future deployments built on the company's accelerators.",
  "account": "semiconductor solutions revenue; guarantee exposure",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "We established the AI XPV platform with certain sophisticated financial partners to enable more than 20 gigawatts in compute capacity using our custom AI accelerators or XPUs and networking solutions customized for the leading frontier AI labs through 2028.",
  "paragraph_id": "0001730168-26-000080:mdna:13",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "related_parties_contingencies_and_subsequent_events_residual_value_guarantees_may_be_provided",
  "what_changed": "New: MD&A says the company 'may provide residual value guarantees' under the platform where necessary, and that management believes they 'would have a low probability of occurring'. The notes describe the existing arrangement as a Backstop of lease obligations, not a residual value guarantee, and say nothing about further guarantees. Direction: the prose anticipates more guarantees.",
  "account": "guarantee liabilities / contingent liabilities",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "Where necessary, we may provide residual value guarantees, which are contingent liabilities we believe would have a low probability of occurring",
  "paragraph_id": "0001730168-26-000080:mdna:13",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "liquidity_and_capital_ai_xpv_initial_tranche_led_by_financial_partner",
  "what_changed": "New: MD&A says the platform launched in June 2026 with an initial tranche of $35 billion, led by a financial partner, for more than 1 gigawatt of compute for 'our customer'. Note 10 gives neither the $35 billion tranche size nor the gigawatt figure.",
  "account": "semiconductor solutions revenue; guarantee exposure",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "In June 2026, we launched the AI XPV platform with an initial tranche of $35 billion led by a financial partner to facilitate the deployment of more than 1 gigawatt of compute infrastructure for our customer.",
  "paragraph_id": "0001730168-26-000080:mdna:14",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "liquidity_and_capital_backstop_raises_counterparty_credit_risk",
  "what_changed": "New sentence in the liquidity discussion: the company 'has provided a backstop' and 'may continue to enter into similar financing arrangements', which it says increases its exposure to counterparty credit risk. The same paragraph lists 'expansions of new business strategies and models' among possible uses of cash.",
  "account": "guarantee exposure; credit losses",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "In addition, we have provided a backstop and may continue to enter into similar financing arrangements, which increases our exposure to counterparty credit risk.",
  "paragraph_id": "0001730168-26-000080:mdna:71",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "liquidity_and_capital_potential_financing_arrangements_named_as_cash_requirement",
  "what_changed": "The list of liquidity requirements (carried as changed) ends with '(viii) potential financing arrangements' and cites $61,079 million of indebtedness with $2,252 million due within 12 months. The prior MD&A wording isn't in my input, so I can't confirm whether clause (viii) is new or only the amounts changed. Marked insufficient.",
  "account": "cash requirements; contingent funding",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "(viii) potential financing arrangements",
  "paragraph_id": "0001730168-26-000080:mdna:69",
  "explanation": false,
  "insufficient": true
}
```

```json
{
  "id": "liquidity_and_capital_sufficiency_statement_now_points_to_backstops",
  "what_changed": "The 12-month liquidity sufficiency statement now points to backstops, alongside indebtedness and contractual commitments, as a cash requirement, and cites Note 10. The Backstop was entered after the prior period end, but the prior wording isn't in my input.",
  "account": "cash requirements; guarantee exposure",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "For additional information regarding our cash requirement from indebtedness, contractual commitments and backstops",
  "paragraph_id": "0001730168-26-000080:mdna:70",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "across_documents_earnings_release_silent_on_backstop_and_financing_platform",
  "what_changed": "The September 2, 2026 earnings release doesn't mention the AI XPV platform, the Backstop (about $29 billion maximum), the customer convertible notes (up to $42 billion), or counterparty credit risk, either in its body or in its forward-looking risk list. The closest it comes is this generic phrase. The 10-Q filed afterwards says the backstop increases counterparty credit risk (mdna:71). No prior release is in my input.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "expansion of our business strategy or adoption of new business models",
  "paragraph_id": "0001730168-26-000076:8k_2_02:47",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "estimates_and_discretion_critical_estimates_unchanged_despite_new_guarantee",
  "what_changed": "Only the period rolled forward. But the statement that critical accounting estimates did not change significantly now covers a quarter in which the notes add a financial guarantee whose fair value management judged not material (notes:108) and a newly footnoted global minimum tax payable (notes:45). Neither is named as a critical estimate in the text I have.",
  "account": "guarantee liability; income tax liabilities",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "There were no significant changes in our critical accounting estimates during the three fiscal quarters ended August 2, 2026",
  "paragraph_id": "0001730168-26-000080:mdna:19",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "revenue_recognition_upfront_license_revenue_amounts_in_products",
  "what_changed": "The note now states upfront license revenue of $3,465 million for the quarter and $7,184 million for the three quarters, included in products revenue. This is software license revenue on contracts without termination for convenience, recognized at transfer of control. It restates $1,916 million and $5,691 million for the prior-year periods. Related costs are still described as immaterial. The prior-period text gave $1,964 million and $3,719 million for the quarter and two quarters ended May 3, 2026. Not compared.",
  "account": "products revenue; cost of products sold",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "we included upfront license revenue of $3,465 million and $7,184 million, respectively, within products revenue",
  "paragraph_id": "0001730168-26-000080:notes:11",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "revenue_recognition_termination_for_convenience_removed_from_most_new_software_contracts",
  "what_changed": "MD&A now says most new software contracts no longer have termination for convenience provisions. It attributes software revenue and operating income growth partly to 'additional license revenue recognized on contracts where customers do not have the right to terminate'. Under the notes:11 policy, those licenses are recognized upfront rather than over the term. The same two sentences repeat at mdna:59.",
  "account": "products revenue (upfront license); contract assets; contract liabilities",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "As of the fiscal quarter ended August 2, 2026, we no longer have termination for convenience provisions for the majority of new software contracts.",
  "paragraph_id": "0001730168-26-000080:mdna:41",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "revenue_recognition_contract_asset_conditionality_criterion_removed",
  "what_changed": "This sentence is removed from the contract-balance policy; the current text is notes:25. It was the stated test separating a contract asset from a receivable. The remaining text says only that a contract asset arises when revenue recognized exceeds the amount invoiced and becomes a receivable when invoiced. MD&A:79 attributes part of the other current assets increase to higher software contract assets.",
  "account": "contract assets (other current assets, other long-term assets); trade accounts receivable",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "A contract asset is a right to consideration that is conditional on something other than the passage of time.",
  "paragraph_id": "0001730168-26-000054:note_history:38",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "revenue_recognition_contract_balance_changes_now_tied_to_billing",
  "what_changed": "The stated driver of changes in contract assets and contract liabilities is now the timing between performance and 'billing the customer'; it was 'the customer's payment' (0001730168-26-000054:note_history:39). Together with the removed conditionality sentence (revenue_recognition_contract_asset_conditionality_criterion_removed), the policy text now ties contract assets to invoicing rather than to conditions on the right to payment.",
  "account": "contract assets; contract liabilities; trade accounts receivable",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Changes in our contract assets and contract liabilities primarily result from the timing difference between our performance and billing the customer.",
  "paragraph_id": "0001730168-26-000080:notes:26",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "revenue_recognition_share_of_contract_liabilities_subject_to_termination",
  "what_changed": "Now says approximately 58% of contract liabilities relate to contracts subject to termination for convenience. The prior-period text, as of May 3, 2026, said approximately 64%. Revenue recognized out of the opening contract liability balance is now stated as $8,309 million for three quarters, with $8,021 million for the prior-year comparable; the prior-period text gave two-quarter figures. Direction: mdna:41 says most new software contracts no longer carry the provision, which implies this share should fall. Whether the two stated percentages show that is left to the numbers reader.",
  "account": "contract liabilities",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "As of August 2, 2026, approximately 58% of contract liabilities related to contracts subject to termination for convenience provisions.",
  "paragraph_id": "0001730168-26-000080:notes:27",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "revenue_recognition_remaining_performance_obligations_stated_amount",
  "what_changed": "Firmly committed remaining performance obligations are now stated at approximately $179.2 billion as of August 2, 2026. The prior-period text said approximately $164.6 billion as of May 3, 2026. Both texts say these include a long-term custom AI accelerator contract entered in the quarter ended May 3, 2026. Not compared.",
  "account": "net revenue (both segments); contract liabilities",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "the remaining performance obligations under these contracts as of August 2, 2026 were approximately $179.2 billion",
  "paragraph_id": "0001730168-26-000080:notes:29",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "estimates_and_discretion_near_term_portion_of_committed_backlog",
  "what_changed": "Management's estimate of the share of remaining performance obligations to be recognized as revenue over the next 12 months is now approximately 25%; the prior-period text said approximately 30%. This is a changed timing estimate. I haven't computed what either share implies in dollars.",
  "account": "net revenue",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "We expect approximately 25% of this amount to be recognized as revenue over the next 12 months.",
  "paragraph_id": "0001730168-26-000080:notes:29",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "revenue_recognition_software_revenue_varies_with_non_terminable_contract_volume",
  "what_changed": "Paragraph carried as changed. It now says software revenue each period varies with the timing and extent of renewals and the relative volume of non-terminable contracts. It also says AI and wireless order swings may be magnified by 'the timing of customer deployments, as well as product launches'. The prior wording isn't in my input, so I can't isolate the new words. The non-terminable-contract link matches the termination-for-convenience change in mdna:41.",
  "account": "infrastructure software revenue; products revenue",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "For infrastructure software, the timing and extent of renewals and relative volume of customer contracts without the right to terminate causes variations in revenue recognized in each period.",
  "paragraph_id": "0001730168-26-000080:mdna:35",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "revenue_recognition_single_distributor_share_of_net_revenue",
  "what_changed": "MD&A states that direct sales to one semiconductor distributor were 50% of net revenue for the quarter and 46% for the three quarters, and gives 32% and 30% for the prior-year periods. The prior 10-Q wording isn't in my input. Not compared. Revenue through one distributor bears on sell-in recognition and on receivable concentration.",
  "account": "semiconductor solutions revenue; trade accounts receivable",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Direct sales to one semiconductor solutions customer, which is a distributor, accounted for 50% and 46% of our net revenue",
  "paragraph_id": "0001730168-26-000080:mdna:33",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "narrative_signs_of_operating_pressure_dependence_on_top_five_end_customers",
  "what_changed": "MD&A estimates sales to the top five end customers, through all channels, at approximately 55% of net revenue for the quarter and 50% for the three quarters, and approximately 40% for each prior-year period. It expects significant concentration to continue and says losing any of these customers could have a material adverse effect. Not compared.",
  "account": "net revenue; trade accounts receivable",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "We believe aggregate sales to our top five end customers, through all channels, accounted for approximately 55% and 50% of our net revenue",
  "paragraph_id": "0001730168-26-000080:mdna:34",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "earnings_quality_receivables_increase_attributed_to_revenue_and_collection_timing",
  "what_changed": "Management explains the receivables increase since November 2, 2025 as 'higher semiconductor revenue and the timing of collections'. The prose says receivables increased; I haven't checked that. The same filing gives factoring volumes (notes:35) and single-distributor concentration (mdna:33), which bear on the same balance.",
  "account": "trade accounts receivable, net",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "primarily due to higher semiconductor revenue and the timing of collections",
  "paragraph_id": "0001730168-26-000080:mdna:76",
  "explanation": true,
  "insufficient": false
}
```

```json
{
  "id": "earnings_quality_inventory_build_for_expected_ai_shipments",
  "what_changed": "Management explains the inventory increase since November 2, 2025 as building 'to support higher expected shipments for AI-related semiconductor solutions'. The cause given is expected shipments, not orders on hand. The prose says inventory increased; I haven't checked that.",
  "account": "inventory",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "primarily to support higher expected shipments for AI-related semiconductor solutions",
  "paragraph_id": "0001730168-26-000080:mdna:80",
  "explanation": true,
  "insufficient": false
}
```

```json
{
  "id": "earnings_quality_other_current_assets_from_software_contract_assets_and_prepaids",
  "what_changed": "Management attributes the increase in other current assets (the sentence starts in mdna:77) mainly to 'higher software contract assets' and higher prepaid expenses. Software contract assets arise when license revenue recognized exceeds amounts invoiced and become receivables on invoicing (notes:25). I treat them as unbilled receivables, which is why explanation is set.",
  "account": "other current assets (current portion of contract assets; prepaid expenses)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "from higher software contract assets and an increase in prepaid expenses.",
  "paragraph_id": "0001730168-26-000080:mdna:79",
  "explanation": true,
  "insufficient": false
}
```

```json
{
  "id": "earnings_quality_receivables_sold_under_non_recourse_factoring",
  "what_changed": "States receivables sold under non-recourse factoring of $1,600 million for the quarter and $3,950 million for the three quarters, and $1,700 million and $5,651 million for the prior-year periods, with proceeds in operating cash flow. Carried as changed; this note block isn't in the note change history, so the prior-period figures aren't visible to me. Not compared.",
  "account": "trade accounts receivable; net cash provided by operating activities",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Total trade accounts receivable sold under the factoring arrangements were $1,600 million and $3,950 million during the fiscal quarter and three fiscal quarters ended August 2, 2026",
  "paragraph_id": "0001730168-26-000080:notes:35",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "liquidity_and_capital_payables_rise_on_inventory_purchase_timing",
  "what_changed": "Management attributes the accounts payable increase since November 2, 2025 to 'the timing of inventory purchases and payments'.",
  "account": "accounts payable",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "primarily due to the timing of inventory purchases and payments.",
  "paragraph_id": "0001730168-26-000080:mdna:82",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "earnings_quality_operating_cash_flow_increase_partly_offset_by_working_capital",
  "what_changed": "MD&A attributes the year-to-date increase in operating cash flow to higher net income and higher non-cash adjustments (mainly stock-based compensation), offset in part by changes in operating assets and liabilities. All three amounts are stated in the text; I haven't checked them.",
  "account": "net cash provided by operating activities; working capital",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "offset in part by $2,805 million from changes in operating assets and liabilities.",
  "paragraph_id": "0001730168-26-000080:mdna:91",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "structure_and_disclosure_changes_global_minimum_tax_payable_footnote_added",
  "what_changed": "New footnote: the 'Other' line of other long-term liabilities includes $2,186 million of global minimum tax payable as of August 2, 2026. No November 2, 2025 amount is given. This block isn't in the note change history. I infer the footnote is new from the paragraph alignment: last period, the paragraph after the other long-term liabilities table is the one that now follows this footnote (notes:46 = 0001730168-26-000054:notes:44).",
  "account": "other long-term liabilities; provision for income taxes",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "(a) Included $2,186 million global minimum tax payable as of August 2, 2026.",
  "paragraph_id": "0001730168-26-000080:notes:45",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "earnings_quality_tax_provision_increase_attributed_to_pretax_income",
  "what_changed": "The income tax note (carried as changed; prior wording not in my input) attributes the higher provision for the quarter and the three quarters 'primarily' to higher income before income taxes.",
  "account": "provision for income taxes",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "was primarily due to higher income before income taxes.",
  "paragraph_id": "0001730168-26-000080:notes:92",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "across_documents_tax_explanation_omits_global_minimum_tax",
  "what_changed": "MD&A repeats the tax note: the higher provision is due 'primarily' to higher pretax income. Neither text mentions the global minimum tax, yet notes:45 newly discloses a $2,186 million global minimum tax payable, and mdna:83 attributes the rise in other current liabilities to higher income tax payable.",
  "account": "provision for income taxes; tax liabilities",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "was primarily due to higher income before income taxes.",
  "paragraph_id": "0001730168-26-000080:mdna:65",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "earnings_quality_other_current_liabilities_rise_from_income_tax_payable",
  "what_changed": "Management attributes the increase in other current liabilities since November 2, 2025 to higher income tax payable.",
  "account": "other current liabilities (tax liabilities)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "primarily from higher income tax payable.",
  "paragraph_id": "0001730168-26-000080:mdna:83",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "earnings_quality_stock_compensation_decline_from_fully_vested_awards",
  "what_changed": "MD&A says stock-based compensation decreased in the quarter 'primarily' because of 'certain fully vested equity awards and headcount reduction', and increased year to date because of the full-period effect of the Two-Year Equity Awards. Carried as changed; prior wording not in my input.",
  "account": "stock-based compensation expense",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "The decrease was primarily due to the impact of certain fully vested equity awards and headcount reduction.",
  "paragraph_id": "0001730168-26-000080:mdna:53",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "estimates_and_discretion_two_year_equity_award_expense_period",
  "what_changed": "Paragraph carried as changed; it completes the sentence begun in mdna:51. It says the Two-Year Equity Awards vest like two annual grants, with start dates of March 15, 2025 and March 15, 2026 and four-year vesting, and that expense runs from grant date to vesting date over four to five years. The prior wording isn't in my input, so I can't tell what changed. Marked insufficient.",
  "account": "stock-based compensation expense",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "We recognize stock-based compensation expense related to these awards from the grant date through their respective vesting date, ranging from four to five years.",
  "paragraph_id": "0001730168-26-000080:mdna:52",
  "explanation": false,
  "insufficient": true
}
```

```json
{
  "id": "narrative_signs_of_operating_pressure_research_headcount_decrease",
  "what_changed": "MD&A attributes the quarterly R&D decrease to lower compensation, including stock-based compensation, from a decrease in headcount, partly offset by higher engineering project costs. So the company names a headcount reduction in the same period MD&A reports revenue increases.",
  "account": "research and development expense",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "due to lower compensation, including stock-based compensation, resulting from a decrease in headcount, offset by higher engineering project costs",
  "paragraph_id": "0001730168-26-000080:mdna:46",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "earnings_quality_research_expense_increase_driven_by_two_year_grant",
  "what_changed": "MD&A attributes the year-to-date R&D increase 'primarily' to higher stock-based compensation from the full impact of the two-year equity grant, plus higher engineering project costs, offset by the headcount decrease.",
  "account": "research and development expense",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "reflecting the full impact of a two-year equity grant in the second quarter of fiscal year 2025",
  "paragraph_id": "0001730168-26-000080:mdna:47",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "narrative_signs_of_operating_pressure_selling_and_administrative_headcount_decrease",
  "what_changed": "MD&A attributes SG&A decreases for the quarter and three quarters 'primarily' to lower compensation from a decrease in headcount.",
  "account": "selling, general and administrative expense",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "primarily due to lower compensation resulting from a decrease in headcount.",
  "paragraph_id": "0001730168-26-000080:mdna:49",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "results_against_expectations_semiconductor_growth_attributed_to_custom_accelerators",
  "what_changed": "MD&A attributes the semiconductor segment's revenue increase to demand for 'networking solutions, primarily custom AI accelerators and AI networking products'; mdna:58 repeats this for segment operating income. The 10-Q text in my input doesn't quantify AI revenue; the release does (0001730168-26-000076:8k_2_02:13).",
  "account": "semiconductor solutions revenue",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "due to strong demand for our networking solutions, primarily custom AI accelerators and AI networking products.",
  "paragraph_id": "0001730168-26-000080:mdna:40",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "results_against_expectations_gross_margin_dollars_attributed_to_ai_demand",
  "what_changed": "MD&A attributes the gross margin dollar increases for the quarter and three quarters 'primarily' to strong product demand for AI-related semiconductor solutions.",
  "account": "gross margin",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The increases were primarily due to strong product demand for our AI-related semiconductor solutions.",
  "paragraph_id": "0001730168-26-000080:mdna:43",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "results_against_expectations_gross_margin_rate_offset_by_semiconductor_mix",
  "what_changed": "MD&A says the gross margin percentage increases came from the benefit of revenue growth, 'partially offset' by a higher mix of semiconductor revenue, which carries a lower gross margin than software. The direction given is that of this named mix effect as semiconductor share grows, which mdna:80 and the release expect. It is not a forecast of the total margin.",
  "account": "gross margin percentage",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "partially offset by a higher mix of semiconductor solutions net revenue, which has a lower gross margin than infrastructure software.",
  "paragraph_id": "0001730168-26-000080:mdna:44",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "earnings_quality_excise_tax_reversal_gain_in_other_income",
  "what_changed": "MD&A says year-to-date other income includes a $315 million gain from reversing excise tax charges on the VMware acquisition, because the final Inflation Reduction Act regulations exempt stock purchases in acquisitions. It also says the prior-year quarter had a gain on sale of a business. The release's non-GAAP reconciliation lists an excise tax benefit adjustment in the year-to-date column (0001730168-26-000076:8k_2_02:66). Both are one-time items within other income.",
  "account": "other income, net",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "we had a $315 million gain from the reversal of excise tax charges on our acquisition of VMware",
  "paragraph_id": "0001730168-26-000080:mdna:64",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "liquidity_and_capital_senior_notes_repurchased_by_tender_and_redemption",
  "what_changed": "New paragraph, replacing last period's 0001730168-26-000054:note_history:20, which covered first-quarter issuance and repayments and a second-quarter redemption. In the quarter the company repurchased $5,641 million of senior notes 'through cash tender offers and redemptions', a method not described before. Year to date it issued $4,500 million and repaid and repurchased $10,541 million. MD&A lists the repurchase as a quarterly highlight (mdna:10). The release shows a loss on debt extinguishment line.",
  "account": "long-term debt; loss on debt extinguishment (within interest expense)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "During the fiscal quarter ended August 2, 2026, we repurchased a total of $5,641 million of our senior notes through cash tender offers and redemptions.",
  "paragraph_id": "0001730168-26-000080:notes:67",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "liquidity_and_capital_interest_expense_lower_from_debt_reduction",
  "what_changed": "MD&A attributes the lower interest expense for the quarter and three quarters 'primarily' to lower outstanding debt balances and debt refinancing.",
  "account": "interest expense",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "The decreases were primarily due to a reduction in outstanding debt balances and debt refinancing activities.",
  "paragraph_id": "0001730168-26-000080:mdna:62",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "liquidity_and_capital_withholding_taxes_settled_by_selling_vested_shares",
  "what_changed": "MD&A says that in the current year, withholding taxes on vesting were settled using proceeds from selling part of the vested shares. In the prior-year period, the company paid $3,860 million in withholding taxes and withheld 17 million shares under net share settlement. Under this change the company no longer pays the withholding cash, and the shares that were withheld before now stay outstanding. Carried as changed; prior wording not in my input.",
  "account": "financing cash flows (shares repurchased for tax withholdings); shares outstanding",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "In the current year fiscal period, we settled withholding taxes upon the vesting of employee equity awards using proceeds from the sale of a portion of the vested shares.",
  "paragraph_id": "0001730168-26-000080:mdna:87",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "liquidity_and_capital_investing_outflows_from_capex_and_short_term_investments",
  "what_changed": "MD&A attributes the increase in investing cash outflows to higher capital expenditures and higher net purchases of short-term investments. It notes the prior-year period included proceeds from a business sale.",
  "account": "capital expenditures; short-term investments",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "was due to higher capital expenditures and an increase in net purchases of short-term investments.",
  "paragraph_id": "0001730168-26-000080:mdna:93",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "narrative_signs_of_operating_pressure_macro_language_names_supply_constraints",
  "what_changed": "Carried as changed, with the sentence continuing in mdna:23. The macro-risk paragraph names supply constraints, and higher trade tensions and tariffs with U.S. trading partners, as risks that may cause revenue to fluctuate and disrupt supply chains. The prior wording isn't in my input, so I can't tell whether these words are new or only the page split moved. Marked insufficient.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "geopolitical events, supply constraints, efforts of governments to stimulate or stabilize the economy",
  "paragraph_id": "0001730168-26-000080:mdna:21",
  "explanation": false,
  "insufficient": true
}
```

```json
{
  "id": "related_parties_contingencies_and_subsequent_events_chief_financial_officer_trading_plan",
  "what_changed": "New: the CFO adopted a Rule 10b5-1 trading plan on July 2, 2026, during the quarter. It provides for selling 50% of the net shares from vesting of up to 150,000 shares and any future awards granted during the plan term, and expires September 28, 2027.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "On July 2, 2026, Amie Thuener, our Chief Financial Officer, adopted a trading plan intended to satisfy Rule 10b5-1(c) under the Exchange Act",
  "paragraph_id": "0001730168-26-000080:notes:120",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "results_against_expectations_revenue_guidance_stated_growth_rate",
  "what_changed": "The release, filed September 2, 2026 (no prior release in my input), guides fourth-quarter revenue to approximately $34.8 billion and describes this as a 93% increase from the prior-year period.",
  "account": "net revenue",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "Fourth quarter fiscal year 2026 revenue guidance of approximately $34.8 billion, an increase of 93 percent from the prior year period",
  "paragraph_id": "0001730168-26-000076:8k_2_02:10",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "results_against_expectations_non_gaap_operating_margin_guidance",
  "what_changed": "The release guides fourth-quarter non-GAAP operating income to about 66% of projected revenue. It says it can't reconcile this to GAAP 'without unreasonable effort'.",
  "account": "operating income (non-GAAP)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "Fourth quarter fiscal year 2026 Non-GAAP operating income guidance of approximately 66 percent of projected revenue",
  "paragraph_id": "0001730168-26-000076:8k_2_02:11",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "results_against_expectations_ai_semiconductor_revenue_outlook",
  "what_changed": "CEO quote in the release: third-quarter AI semiconductor revenue of $16.7 billion, which the quote says grew 221% year over year and 54% quarter over quarter, and an expected $21.7 billion in the fourth quarter. The 10-Q text in my input doesn't separately quantify AI revenue.",
  "account": "semiconductor solutions revenue",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "we expect AI semiconductor revenue to accelerate to $21.7 billion, up 236% year-over-year.",
  "paragraph_id": "0001730168-26-000076:8k_2_02:13",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "results_against_expectations_cfo_claims_flat_non_gaap_margin",
  "what_changed": "CFO quote in the release: record revenue, operating profit and free cash flow; non-GAAP operating income growth of 92%; and an expectation that fourth-quarter non-GAAP operating margin stays at 66%, 'flat from a year ago'. These are the release's own claims; I haven't checked them.",
  "account": "operating income (non-GAAP)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "we expect to maintain our non-GAAP operating margin at 66%, flat from a year ago.",
  "paragraph_id": "0001730168-26-000076:8k_2_02:14",
  "explanation": false,
  "insufficient": false
}
```

## Paragraphs carried as text that are not items

### Notes
- 0001730168-26-000080:notes:5: date rolled forward (quarter end in the basis-of-presentation sentence)
- 0001730168-26-000080:notes:12: amounts and period rolled; history shows it as added, but it replaces the removed 0001730168-26-000054:note_history:42 of the same form
- 0001730168-26-000080:notes:13: amounts and period rolled; replaces the removed 0001730168-26-000054:note_history:43 of the same form
- 0001730168-26-000080:notes:17: amounts only (revenue disaggregation table)
- 0001730168-26-000080:notes:18: amounts only (revenue disaggregation table)
- 0001730168-26-000080:notes:19: amounts only (revenue disaggregation table)
- 0001730168-26-000080:notes:20: amounts only (revenue disaggregation table)
- 0001730168-26-000080:notes:24: amounts only (contract assets and liabilities table)
- 0001730168-26-000080:notes:25: covered by revenue_recognition_contract_asset_conditionality_criterion_removed (quote taken from the removed prior sentence)
- 0001730168-26-000080:notes:32: amounts only as far as visible (time deposits, money-market funds); block not in note change history
- 0001730168-26-000080:notes:33: amounts only as far as visible (Treasury bills, level split); block not in note change history
- 0001730168-26-000080:notes:37: amounts only (inventory components table)
- 0001730168-26-000080:notes:39: amounts only (other current assets table)
- 0001730168-26-000080:notes:41: amounts only (other current liabilities table)
- 0001730168-26-000080:notes:43: amounts only (other long-term liabilities table); its new (a) marker is itemised via notes:45
- 0001730168-26-000080:notes:44: footnote separator line
- 0001730168-26-000080:notes:47: amounts only (cash paid for interest and taxes table)
- 0001730168-26-000080:notes:49: amounts only (intangibles table); the August 2, 2026 block has no in-process R&D row, and whether that is new this quarter is not visible to me
- 0001730168-26-000080:notes:50: date rolled forward
- 0001730168-26-000080:notes:51: amounts only (expected amortization table)
- 0001730168-26-000080:notes:53: date header rolled (weighted-average useful lives table); prior figures not in my input
- 0001730168-26-000080:notes:58: amounts only (EPS table)
- 0001730168-26-000080:notes:59: amounts only (EPS table)
- 0001730168-26-000080:notes:60: heading
- 0001730168-26-000080:notes:61: amounts only (debt table; note history confirms); retirements are covered by liquidity_and_capital_senior_notes_repurchased_by_tender_and_redemption
- 0001730168-26-000080:notes:62: amounts only (debt table; note history confirms)
- 0001730168-26-000080:notes:63: amounts only (debt totals table; note history confirms)
- 0001730168-26-000080:notes:64: not shown as changed in note change history; no change visible
- 0001730168-26-000080:notes:65: heading
- 0001730168-26-000080:notes:66: not shown as changed in note change history; no change visible
- 0001730168-26-000080:notes:68: heading
- 0001730168-26-000080:notes:69: not shown as changed in note change history; no change visible
- 0001730168-26-000080:notes:70: heading
- 0001730168-26-000080:notes:71: date rolled forward (no revolver borrowings at the new date)
- 0001730168-26-000080:notes:72: heading
- 0001730168-26-000080:notes:73: date rolled forward (no commercial paper at the new date)
- 0001730168-26-000080:notes:74: heading
- 0001730168-26-000080:notes:75: amount and date only (fair value of debt)
- 0001730168-26-000080:notes:76: heading
- 0001730168-26-000080:notes:77: date rolled forward
- 0001730168-26-000080:notes:78: amounts only (principal payment schedule)
- 0001730168-26-000080:notes:79: date rolled forward (covenant compliance)
- 0001730168-26-000080:notes:81: amounts only (dividends table)
- 0001730168-26-000080:notes:83: period and amounts rolled; both authorizations described are dated before the prior period end; identical to mdna:86
- 0001730168-26-000080:notes:85: amounts only (stock-based compensation table)
- 0001730168-26-000080:notes:87: amounts only (unrecognized compensation cost and period)
- 0001730168-26-000080:notes:90: amounts only (RSU activity table)
- 0001730168-26-000080:notes:91: amount only (fair value of vested RSUs)
- 0001730168-26-000080:notes:98: amounts only (segment table)
- 0001730168-26-000080:notes:99: heading; not shown as changed
- 0001730168-26-000080:notes:100: date rolled forward
- 0001730168-26-000080:notes:101: amounts only (contractual commitments table)
- 0001730168-26-000080:notes:102: not shown as changed in note change history; definition unchanged
- 0001730168-26-000080:notes:103: not shown as changed in note change history; definition unchanged
- 0001730168-26-000080:notes:104: amount and date only (unrecognized tax benefits excluded)
- 0001730168-26-000080:notes:105: new heading; covered by structure_and_disclosure_changes_ai_rack_backstop_moved_from_subsequent_events_into_guarantee_note
- 0001730168-26-000080:notes:109: new heading; covered by related_parties_contingencies_and_subsequent_events_customer_convertible_notes_issuable_to_company
- 0001730168-26-000080:notes:111: heading
- 0001730168-26-000080:notes:112: not shown as changed in note change history; litigation boilerplate unchanged
- 0001730168-26-000080:notes:113: heading
- 0001730168-26-000080:notes:114: not shown as changed in note change history; no change visible
- 0001730168-26-000080:notes:115: not shown as changed in note change history; no change visible
- 0001730168-26-000080:notes:116: heading
- 0001730168-26-000080:notes:117: not shown as changed in note change history; no change visible
- 0001730168-26-000080:notes:118: heading rearranged because the backstop subsequent event was removed; covered by structure_and_disclosure_changes_ai_rack_backstop_moved_from_subsequent_events_into_guarantee_note
- 0001730168-26-000080:notes:119: dates rolled forward; per-share amount text unchanged

### MD&A
- 0001730168-26-000080:mdna:7: date rolled forward (highlights lead-in)
- 0001730168-26-000080:mdna:8: amount only (cash from operations)
- 0001730168-26-000080:mdna:9: amount only (dividends paid)
- 0001730168-26-000080:mdna:10: covered by liquidity_and_capital_senior_notes_repurchased_by_tender_and_redemption (same amount)
- 0001730168-26-000080:mdna:11: heading for the section carrying the new platform paragraphs (itemised from mdna:12 to mdna:14); whether the heading itself is new isn't visible
- 0001730168-26-000080:mdna:15: verbatim repeat of notes:107; covered by the two notes:107 items
- 0001730168-26-000080:mdna:16: verbatim repeat of notes:108 plus a cross-reference to Note 10; covered by estimates_and_discretion_backstop_fair_value_judged_not_material
- 0001730168-26-000080:mdna:23: continuation of the mdna:21 sentence; covered by narrative_signs_of_operating_pressure_macro_language_names_supply_constraints
- 0001730168-26-000080:mdna:26: heading, period rolled forward
- 0001730168-26-000080:mdna:28: amounts only (results table)
- 0001730168-26-000080:mdna:30: amounts only (results table)
- 0001730168-26-000080:mdna:31: near-verbatim repeat of notes:11; covered by revenue_recognition_upfront_license_revenue_amounts_in_products
- 0001730168-26-000080:mdna:36: page number
- 0001730168-26-000080:mdna:38: amounts only (segment revenue table)
- 0001730168-26-000080:mdna:39: amounts only (segment mix table)
- 0001730168-26-000080:mdna:51: first half of the sentence completed in mdna:52; covered by estimates_and_discretion_two_year_equity_award_expense_period
- 0001730168-26-000080:mdna:54: amounts only (unrecognized compensation cost and period)
- 0001730168-26-000080:mdna:55: amounts only (unrecognized compensation schedule)
- 0001730168-26-000080:mdna:57: amounts only (segment operating income table)
- 0001730168-26-000080:mdna:58: repeats the mdna:40 cause for segment operating income; covered by results_against_expectations_semiconductor_growth_attributed_to_custom_accelerators
- 0001730168-26-000080:mdna:59: repeats mdna:41 including the termination-for-convenience sentence; covered by revenue_recognition_termination_for_convenience_removed_from_most_new_software_contracts
- 0001730168-26-000080:mdna:60: amounts; cause given (stock-based compensation) is covered by earnings_quality_stock_compensation_decline_from_fully_vested_awards
- 0001730168-26-000080:mdna:68: amounts only (cash balance, revolver size)
- 0001730168-26-000080:mdna:72: debt-management text; prior wording not in my input; the tender-offer activity it mentions is itemised from notes:67
- 0001730168-26-000080:mdna:74: amounts only (working capital)
- 0001730168-26-000080:mdna:75: amounts only (cash change drivers are cash-flow-statement lines)
- 0001730168-26-000080:mdna:77: first half of the sentence completed in mdna:79; covered by earnings_quality_other_current_assets_from_software_contract_assets_and_prepaids
- 0001730168-26-000080:mdna:78: page number
- 0001730168-26-000080:mdna:85: amounts only (dividends table)
- 0001730168-26-000080:mdna:86: identical to notes:83; period and amounts rolled
- 0001730168-26-000080:mdna:89: amounts only (cash flow summary table)
- 0001730168-26-000080:mdna:94: page number
- 0001730168-26-000080:mdna:96: amounts; drivers covered by liquidity_and_capital_senior_notes_repurchased_by_tender_and_redemption and liquidity_and_capital_withholding_taxes_settled_by_selling_vested_shares

### Item 4
- 0001730168-26-000080:item_4_controls:1: heading
- 0001730168-26-000080:item_4_controls:2: date rolled forward; disclosure controls still concluded effective
- 0001730168-26-000080:item_4_controls:3: boilerplate on reasonable assurance; no change
- 0001730168-26-000080:item_4_controls:4: standard statement that internal control over financial reporting did not change, now made for the quarter in which the Backstop was entered; no change in wording visible

### 8-K 0001730168-26-000076, item 2.02 / Ex. 99.1
- 0001730168-26-000076:8k_2_02:1: exhibit cover metadata
- 0001730168-26-000076:8k_2_02:2: document label
- 0001730168-26-000076:8k_2_02:3: exhibit label
- 0001730168-26-000076:8k_2_02:4: headline
- 0001730168-26-000076:8k_2_02:5: amounts only (revenue and growth headline)
- 0001730168-26-000076:8k_2_02:6: amounts only (operating income)
- 0001730168-26-000076:8k_2_02:7: amounts only (EPS)
- 0001730168-26-000076:8k_2_02:8: amounts only (cash from operations, free cash flow)
- 0001730168-26-000076:8k_2_02:9: amount only (dividend)
- 0001730168-26-000076:8k_2_02:12: introductory sentence, dates
- 0001730168-26-000076:8k_2_02:15: separator line
- 0001730168-26-000076:8k_2_02:16: reconciliation footnote boilerplate
- 0001730168-26-000076:8k_2_02:17: page number
- 0001730168-26-000076:8k_2_02:18: heading
- 0001730168-26-000076:8k_2_02:19: amounts only (highlights table)
- 0001730168-26-000076:8k_2_02:20: amounts only (cash flow highlights table)
- 0001730168-26-000076:8k_2_02:21: amounts only (segment revenue table)
- 0001730168-26-000076:8k_2_02:22: amounts only (cash balances)
- 0001730168-26-000076:8k_2_02:23: amounts only (cash from operations, capex)
- 0001730168-26-000076:8k_2_02:24: amounts and date only (dividend paid)
- 0001730168-26-000076:8k_2_02:25: boilerplate cross-reference to reconciliations
- 0001730168-26-000076:8k_2_02:26: heading
- 0001730168-26-000076:8k_2_02:27: guidance lead-in, period end date
- 0001730168-26-000076:8k_2_02:28: repeat of 8k_2_02:10; covered by results_against_expectations_revenue_guidance_stated_growth_rate
- 0001730168-26-000076:8k_2_02:29: repeat of 8k_2_02:11; covered by results_against_expectations_non_gaap_operating_margin_guidance
- 0001730168-26-000076:8k_2_02:30: guidance disclaimer boilerplate
- 0001730168-26-000076:8k_2_02:31: page number
- 0001730168-26-000076:8k_2_02:32: heading
- 0001730168-26-000076:8k_2_02:33: dividend declaration, dates and amount; consistent with notes:119
- 0001730168-26-000076:8k_2_02:34: heading
- 0001730168-26-000076:8k_2_02:35: call logistics
- 0001730168-26-000076:8k_2_02:36: call logistics
- 0001730168-26-000076:8k_2_02:37: call logistics
- 0001730168-26-000076:8k_2_02:38: heading
- 0001730168-26-000076:8k_2_02:39: non-GAAP boilerplate
- 0001730168-26-000076:8k_2_02:40: non-GAAP boilerplate
- 0001730168-26-000076:8k_2_02:41: free cash flow boilerplate
- 0001730168-26-000076:8k_2_02:42: page number
- 0001730168-26-000076:8k_2_02:43: continuation of free cash flow boilerplate
- 0001730168-26-000076:8k_2_02:44: heading
- 0001730168-26-000076:8k_2_02:45: company description boilerplate
- 0001730168-26-000076:8k_2_02:46: heading
- 0001730168-26-000076:8k_2_02:48: page number
- 0001730168-26-000076:8k_2_02:49: continuation of the 8k_2_02:47 risk list; covered by across_documents_earnings_release_silent_on_backstop_and_financing_platform
- 0001730168-26-000076:8k_2_02:50: forward-looking boilerplate
- 0001730168-26-000076:8k_2_02:51: contact block
- 0001730168-26-000076:8k_2_02:52: contact block
- 0001730168-26-000076:8k_2_02:53: contact block
- 0001730168-26-000076:8k_2_02:54: contact block
- 0001730168-26-000076:8k_2_02:55: contact block
- 0001730168-26-000076:8k_2_02:56: contact block
- 0001730168-26-000076:8k_2_02:57: release code
- 0001730168-26-000076:8k_2_02:58: page number
- 0001730168-26-000076:8k_2_02:59: heading
- 0001730168-26-000076:8k_2_02:60: heading
- 0001730168-26-000076:8k_2_02:61: heading
- 0001730168-26-000076:8k_2_02:62: amounts only (statement of operations)
- 0001730168-26-000076:8k_2_02:63: heading
- 0001730168-26-000076:8k_2_02:64: heading
- 0001730168-26-000076:8k_2_02:65: heading
- 0001730168-26-000076:8k_2_02:66: amounts only (GAAP to non-GAAP reconciliation); excise tax line referenced in earnings_quality_excise_tax_reversal_gain_in_other_income
- 0001730168-26-000076:8k_2_02:67: amounts only (reconciliation continued)
- 0001730168-26-000076:8k_2_02:68: non-GAAP share-count footnote boilerplate
- 0001730168-26-000076:8k_2_02:69: heading
- 0001730168-26-000076:8k_2_02:70: heading
- 0001730168-26-000076:8k_2_02:71: heading
- 0001730168-26-000076:8k_2_02:72: amounts only (balance sheet)
- 0001730168-26-000076:8k_2_02:73: amounts only (cash flow statement)

## Counts

- **Items:** 55
  - `explanation` true: 3 (receivables at mdna:76, inventory at mdna:80, software contract assets at mdna:79)
  - `insufficient` true: 3 (mdna:69, mdna:52, mdna:21)
- **Paragraphs carried as text and not made items:** 171
  - notes: 66
  - MD&A: 33
  - Item 4: 4
  - 8-K Ex. 99.1: 68
- **Paragraphs that carry items:** 49 distinct (13 notes, 31 MD&A, 5 Ex. 99.1). One more item takes its quote from the prior-text paragraph 0001730168-26-000054:note_history:38.
- Together these account for every paragraph carried as text: 79 notes, 64 MD&A, 4 Item 4 and 73 Ex. 99.1.
