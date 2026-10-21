<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# ADTN 10-Q 0001193125-26-331632 (quarter ended June 30, 2026): notes-text reader

## Inputs read

- `input_notes.md` (notes:1–195), `input_mdna.md` (mdna:1–167), `input_controls.md` (item_4_controls:1–15), `input_8k.md` (8-K 0001193125-26-331458, item 2.02 body 8k_2_02:1–127, plus the item-code and late-filing lists), `input_notes_history.md` (note_history, 0001193125-26-205276 → 0001193125-26-331632), `input_prior_predictions.md`. I read all of them in full.
- Nothing forbidden is in the directory: no trend table, prices, abnormal returns, short interest, other-company files, prior probabilities or outcome window. The 8-K contains the company's own condensed statement tables. I did no arithmetic on them.
- Prior predictions: none on record.
- Not in my input: Item 1A diff, Exhibit 21 diff, any Exhibit 10 (none for the July 21, 2026 J.P. Morgan credit agreement), and an auditor's report. This is a 10-Q, so Item 4 is the only controls section. The only 8-K body present is the 2026-08-04 earnings release. The item-code list shows other 8-Ks whose bodies are absent:
  - 2026-07-23: items 1.01, 1.02, 2.03
  - 2026-07-22: items 2.02, 7.01, ahead of the full release
  - 2026-06-26: items 5.02, 8.01
  - 2026-05-18: items 5.03, 5.07
  - 2026-04-07: item 5.02

  I cannot report on any of those bodies.
- Item 4 is carried in full without the prior period's text, so for Item 4 I can say what the text says but not what changed.

## Items

```json
[
  {
    "id": "related_parties_contingencies_and_subsequent_events_sec_inquiry_concluded_without_enforcement",
    "what_changed": "The legal-matters text now says the Company responded to the SEC. It says that on June 22, 2026 the SEC staff sent a letter saying it had concluded its investigation as to the Company and, based on the information to date, did not intend to move forward with an enforcement action. The prior text said the Company was cooperating and could not predict the timing or outcome of the inquiry that began with the August 4, 2025 letter. No amount is stated. The prose implies inquiry-related legal and professional work ends. The 8-K list shows an 8-K with items 5.02 and 8.01 filed 2026-06-26; its body is not in my input.",
    "account": "selling, general and administrative expenses (professional fees); contingent liabilities",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "the SEC staff did not intend to move forward with an enforcement action against the Company",
    "paragraph_id": "0001193125-26-331632:notes:165",
    "explanation": false
  },
  {
    "id": "earnings_quality_retirement_plan_correction_accrual_reversed",
    "what_changed": "The 401(k) voluntary correction program matter has been resolved. The prior text said the Company was still negotiating with the IRS and had accrued $1.4 million during 2025. The text now says the IRS issued a compliance statement in May 2026 approving a retroactive amendment, the Company executed it in June 2026, and the Company reversed $1.4 million of previously accrued amounts in June 2026. The earnings release's non-GAAP footnotes net this reversal against employee exit costs inside 'professional fees and other expenses', so the reversal lowers GAAP expense in the quarter and is excluded from non-GAAP results.",
    "account": "selling, general and administrative and research and development expenses; accrued expenses and other liabilities",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Based on this resolution, the Company reversed $1.4 million of amounts previously accrued related to the VCP in June 2026.",
    "paragraph_id": "0001193125-26-331632:notes:184",
    "explanation": true
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_dplta_appraisal_decision_timing",
    "what_changed": "The expected timing of a final decision in the DPLTA appraisal proceedings is reworded. The prior text said a ruling on the merits would take a minimum of 12 months, an appeal a further 12-24 months, and no final decision before 2027, most likely not until 2028 or beyond. The text now says the Regional Court Meiningen has not yet ruled, an appeal is likely, and the Company does not anticipate a final decision until late 2027 or 2028. The duration estimates are removed. The same paragraph restates the maximum aggregate Exit Compensation, including guaranteed interest, as approximately EUR 292.6 million / $334.2 million at June 30, 2026. The prior text said EUR 304.4 million / $351.7 million at March 31, 2026. The same wording appears in notes:7, mdna:17, mdna:90 and mdna:153-154.",
    "account": "redeemable non-controlling interest; DPLTA Exit Compensation obligation",
    "expected_direction": "none",
    "horizon": "beyond 12 months (company names late 2027 or 2028)",
    "quote": "the Company does not anticipate a final decision on the shareholders' claims until late 2027 or 2028",
    "paragraph_id": "0001193125-26-331632:notes:169",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_dplta_exit_compensation_tenders_paid",
    "what_changed": "New paragraph on Exit Compensation tenders. It says approximately 0.4 million Adtran Networks shares were tendered in the quarter and 0.6 million in the six months. It gives a single payment figure, approximately EUR 11.7 million or $13.8 million, against both the three- and six-month periods. The prior text said about 0.2 million shares were tendered in Q1 2026, with EUR 3.6 million (about $4.1 million) to be settled in cash in April 2026. MD&A names $13.8 million of payments for redemption of redeemable non-controlling interest in financing activities. It states holdings of 37,447,983 Adtran Networks shares, 71.9% of outstanding shares at June 30, 2026. Tenders redeem minority interest.",
    "account": "redeemable non-controlling interest; financing cash flows",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "approximately 0.4 million shares and 0.6 million shares, respectively, of Adtran Networks stock were tendered to the Company",
    "paragraph_id": "0001193125-26-331632:notes:171",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_dplta_annual_recurring_compensation_paid",
    "what_changed": "The Annual Recurring Compensation for fiscal 2025 has been paid. The prior text said the Adtran Networks general meeting was scheduled for Q2 2026 and payment would fall due three banking days later. The text now says the meeting occurred on June 15, 2026 and $8.9 million was paid. The continuing annual obligation is now stated as approximately EUR 7.6 million ($8.7 million) per year; the prior text said EUR 7.8 million ($9.0 million). Accruals are stated as $2.1 million for the quarter ($2.4 million in Q2 2025) and $4.3 million for six months ($4.8 million). The release's cash flow statement carries a new financing line, 'Payment of annual recurring compensation to non-controlling interest'.",
    "account": "cash; financing cash flows; retained deficit",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "the Annual Recurring Compensation was paid after the ordinary general shareholders' meeting in the amount of $8.9 million",
    "paragraph_id": "0001193125-26-331632:notes:8",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_exit_compensation_remote_probability_basis",
    "what_changed": "Management still judges it remote that more than a small minority of Adtran Networks shareholders will elect Exit Compensation in the next twelve months, but the stated basis changed from five factors to four. Factor (i) used to say 'we do not expect the final decision to be published within the next 12 months'. It now says no final decision is anticipated 'until late 2027 or 2028'. The former factor (iii) is removed: the decision date is uncertain, a ruling would take a minimum of 12 months, and an appeal a further 12-24 months. The remaining factors are the diverse shareholder base, the guaranteed recurring compensation and the trading value of Adtran Networks shares.",
    "account": "redeemable non-controlling interest; Exit Compensation obligations",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "the Company does not anticipate a final decision on shareholder's challenges to Exit Compensation until late 2027 or 2028",
    "paragraph_id": "0001193125-26-331632:notes:11",
    "explanation": false
  },
  {
    "id": "across_documents_exit_compensation_liquidity_sentence_only_in_mdna",
    "what_changed": "In the notes, the paragraph that opened 'As of March 31, 2026 ... the Company has sufficient liquidity to meet the majority of its payment obligations under the DPLTA pertaining to Exit Compensation' was removed. Its replacement (notes:11) carries no liquidity sentence, and notes:10 is unchanged and so cannot hold a re-dated version. MD&A keeps the sentence and now names the source as 'operating cash flow and the borrowings available under the Credit Facility'. At the filing date that facility is the new J.P. Morgan agreement. Both versions cover only 'a majority' of the obligation.",
    "account": "liquidity; redeemable non-controlling interest",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "the Company has sufficient liquidity through its operating cash flow and the borrowings available under the Credit Facility to meet a majority of its payment obligations under the DPLTA pertaining to Exit Compensation",
    "paragraph_id": "0001193125-26-331632:mdna:94",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_wells_fargo_facility_replaced_by_jp_morgan",
    "what_changed": "On July 21, 2026 the Wells Fargo agreement was terminated and all its principal repaid; the prior text said it matured in July 2027. It was replaced by a $350.0 million J.P. Morgan agreement maturing July 2031. The borrowers are ADTRAN, Inc. and Adtran Networks SE, with German borrowings limited to $50.0 million, and ADTRAN Holdings, Inc. is guarantor. Pricing is the Term Benchmark Rate plus 2.25%-3.25% or the Base Rate plus 1.25%-2.25%, set by the consolidated total net leverage ratio, with a 0.00% floor and a 0.25% fee on unused commitments. At June 30, 2026 the text states:\n- $25.0 million drawn under Wells Fargo\n- $6.8 million of letters of credit\n- $318.2 million available\n- a weighted average revolver rate of 8.89%\n\nThe prior text stated $5.8 million, $319.2 million and 8.92% at March 31, 2026. Note 18 (Subsequent Events) and the MD&A 'J.P. Morgan Credit Agreement' section are new. Neither the Exhibit 10 nor the 2026-07-23 8-K body (items 1.01, 1.02, 2.03) is in my input.",
    "account": "non-current revolving credit agreement; interest expense",
    "expected_direction": "insufficient",
    "horizon": "next quarter",
    "quote": "On July 21, 2026, the Company terminated the Former Credit Agreement with Wells Fargo, repaid all principal amounts under the Former Credit Agreement and entered into the New Credit Agreement, which is a five-year, $350.0 million credit agreement with J.P. Morgan Chase Bank, N.A.",
    "paragraph_id": "0001193125-26-331632:notes:105",
    "explanation": false
  },
  {
    "id": "results_against_expectations_refinancing_signed_after_stated_quarter",
    "what_changed": "The prior period's notes said the Company intended to refinance or replace the Wells Fargo agreement during the second quarter of 2026, with no assurance it would. The current filing reports the new agreement as a subsequent event (Note 18), signed July 21, 2026, after the June 30, 2026 balance-sheet date. The stated intention and the 'no assurances' sentence are removed.",
    "account": "non-current revolving credit agreement",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The Company intends to refinance or replace the existing Credit Agreement with a new credit facility during the second quarter of 2026.",
    "paragraph_id": "0001193125-26-205276:note_history:21",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_credit_covenant_levels_no_longer_stated",
    "what_changed": "The notes no longer state covenant levels. The removed text gave the Wells Fargo covenants:\n- Consolidated Total Net Leverage Ratio 5.00x\n- Consolidated Senior Secured Net Leverage Ratio 3.25x (4.0x to 3.5x during a Springing Covenant Period)\n- Consolidated Fixed Charge Coverage Ratio 1.25x\n- during a Springing Covenant Period, minimum cash of $50.0 million for the credit parties and $70.0 million for the Company and subsidiaries\n\nThe new agreement is described only as requiring 'certain' leverage ratios and fixed charge coverage ratios from the quarter ending December 31, 2026. No ratio levels or cash minimums are given, and no covenant test is described for the quarter ending September 30, 2026.",
    "account": "non-current revolving credit agreement (covenant compliance)",
    "expected_direction": "none",
    "horizon": "12 months (first stated test at the quarter ending December 31, 2026)",
    "quote": "Under the New Credit Agreement, the Company agreed to maintain certain leverage ratios and certain fixed charge coverage ratios commencing with the fiscal quarter ending December 31, 2026.",
    "paragraph_id": "0001193125-26-331632:notes:187",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_credit_collateral_and_guaranty_terminated",
    "what_changed": "New: on July 21, 2026 the Company terminated four agreements: the July 18, 2022 collateral agreement, the June 4, 2024 ADVA domestic collateral agreement, the July 18, 2022 guaranty agreement and the June 4, 2024 ADVA guaranty agreement. The Wells Fargo facility was described as a secured revolving credit facility. The J.P. Morgan agreement is described with ADTRAN Holdings, Inc. as guarantor, and the text does not say whether it is secured or by what collateral.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "the collateral agreement dated July 18, 2022, the ADVA domestic collateral agreement dated June 4, 2024",
    "paragraph_id": "0001193125-26-331632:notes:188",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_post_quarter_draw_on_jp_morgan_facility",
    "what_changed": "The contractual cash requirements table is now presented 'as of the date of this filing'. It replaces the credit line with a 'J.P. Morgan credit agreement' amount due after 2030. Its footnote says borrowings outstanding at the filing date include funds for closing and legal fees and other general corporate purposes. The prose therefore says that after quarter-end the Company drew on the new facility for more than repaying Wells Fargo. The size of the table amount against the June 30 revolver balance is for the numbers reader. mdna:161 does not name the refinancing among changes in cash requirements.",
    "account": "non-current revolving credit agreement",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "The borrowings outstanding as of the date of the filing include funds for",
    "paragraph_id": "0001193125-26-331632:mdna:135",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_ustr_tariffs_replace_expired_tariffs",
    "what_changed": "The prior text said only that the administration had announced its intention to invoke other laws and new tariffs on all countries. The text now says:\n- Section 122 was invoked to impose 10% tariffs on imports from all countries.\n- Section 232 tariffs on copper, steel and aluminum were amended, effective April 6, 2026, to rates based on metal content.\n- The Section 122 tariff expired on July 24, 2026.\n- On July 23, 2026 USTR announced Section 301 tariffs of 10% or 12.5% on most goods from about 60 trading partners.\n\nMD&A (mdna:26) adds that the lower rate applies to partners with a forced-labor import prohibition and that goods already under Section 232 are excluded. MD&A (mdna:27) says trade policy changes have the potential to materially alter input costs.",
    "account": "cost of revenue; inventory",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "announced a final action under Section 301 of the Trade Act of 1974 imposing additional ad valorem tariffs of 10% or 12.5% on most goods imported from approximately 60 foreign trading partners",
    "paragraph_id": "0001193125-26-331632:notes:178",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_ieepa_tariff_refund_not_recognized",
    "what_changed": "The Tariff Refund paragraphs (notes:179-181 and mdna:31) are carried as changed text but are not listed in the note change history, so the prior wording is not in my input. As filed, they say:\n- The refund is assessed under a loss recovery model (ASC 410-30).\n- The tariffs were capitalized to inventory and later expensed through cost of goods sold.\n- Recognition is limited to amounts previously recorded.\n- The CBP system became operational on April 20, 2026.\n- Given the lack of clarity on refund execution, recovery is judged not probable and no receivable is recognized.\n\nNo refund amount is stated. If recovery later becomes probable, the prose implies a credit against previously expensed cost.",
    "account": "other receivables; cost of revenue",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "the Company has concluded that recovery of the IEEPA tariffs is not probable as of the reporting date. Accordingly, no refund receivable has been recognized.",
    "paragraph_id": "0001193125-26-331632:notes:181",
    "explanation": true
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_tariff_passthrough_amounts_owed_to_customers",
    "what_changed": "The text says Adtran may owe money to customers, depending on final assessments of contractual or implicit tariff passthrough obligations. It says the Company will update its conclusions on both refund recoverability and customer refunds. The sentence is carried as changed text not listed in the note history, so whether it is new cannot be read from my input. No amount or accrual is stated.",
    "account": "revenue; accrued expenses and other liabilities",
    "expected_direction": "insufficient",
    "horizon": "12 months",
    "quote": "Additionally, Adtran may owe money to customers depending on final assessments of contractual or implicit passthrough obligations.",
    "paragraph_id": "0001193125-26-331632:notes:182",
    "explanation": false
  },
  {
    "id": "earnings_quality_factoring_proceeds_classified_in_operating_cash_flow",
    "what_changed": "New sentence: factoring proceeds are recorded as a component of accounts receivable in operating cash flows. Proceeds are stated as:\n- $43.0 million for Q2 2026 and $94.8 million for the six months\n- $38.5 million and $70.3 million for the same 2025 periods\n\nFactoring cost, included in interest expense, is $0.4 million and $0.9 million. Receivables factored at June 30, 2026 total $18.3 million, of which $3.7 million is held in the reserve account. notes:46 says the program 'accelerates receivable collection and helps to better manage cash flow'. The prose implies factoring lowers reported receivables and lifts operating cash flow.",
    "account": "accounts receivable, net; net cash provided by operating activities",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "which are recorded as a component of accounts receivable in operating cash flows on the Condensed Consolidated Statement of Cash Flows",
    "paragraph_id": "0001193125-26-331632:notes:47",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_factoring_reserve_account_in_other_assets",
    "what_changed": "New sentence: the reserve account the factor retains ($3.7 million at June 30, 2026) is included in other assets. The text does not say whether that is current or non-current. The release's cash flow statement also carries an investing line, 'Payments for beneficial interests in securitized accounts receivable', which no paragraph in my input describes.",
    "account": "other assets",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The balance in the reserve account is included in other assets.",
    "paragraph_id": "0001193125-26-331632:notes:46",
    "explanation": false
  },
  {
    "id": "across_documents_factoring_prior_year_proceeds_stated_two_ways",
    "what_changed": "MD&A states factoring proceeds of $73.8 million for the six months ended June 30, 2025. Note 2 (notes:47) states $70.3 million for the same period. The filing gives two different figures for the same quantity.",
    "account": "accounts receivable; operating cash flows",
    "expected_direction": "insufficient",
    "horizon": "this quarter",
    "quote": "the Company received $94.8 million and $73.8 million in cash proceeds from the Factoring Agreement",
    "paragraph_id": "0001193125-26-331632:mdna:149",
    "explanation": false
  },
  {
    "id": "revenue_recognition_receivable_days_commercial_terms_mix",
    "what_changed": "MD&A says quarterly DSO increased from 66 days at December 31, 2025 to 67 days at June 30, 2026. It gives the cause as customer and geographical mix of commercial terms. The explanation does not mention the factoring program, which the notes say brought in $94.8 million in the six months.",
    "account": "accounts receivable, net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Quarterly accounts receivable DSO increased from 66 days as of December 31, 2025, to 67 days as of June 30, 2026 and was primarily driven by customer and geographical mix of commercial terms.",
    "paragraph_id": "0001193125-26-331632:mdna:109",
    "explanation": true
  },
  {
    "id": "estimates_and_discretion_credit_loss_allowance_amount_now_stated",
    "what_changed": "The allowance for credit losses on accounts receivable is now stated as $1.6 million at June 30, 2026 ($1.3 million at December 31, 2025). The prior period's sentence stated $1.7 million at March 31, 2026. No cause is given. No allowance is recorded on contract assets (notes:49).",
    "account": "allowance for credit losses (accounts receivable)",
    "expected_direction": "insufficient",
    "horizon": "this quarter",
    "quote": "The allowance for credit losses was $1.6 million and $1.3 million as of June 30, 2026, and December 31, 2025, respectively, related to accounts receivable.",
    "paragraph_id": "0001193125-26-331632:notes:44",
    "explanation": false
  },
  {
    "id": "earnings_quality_inventory_decrease_attributed_to_buffer_stock_use",
    "what_changed": "MD&A says quarterly inventory turnover increased from 2.8 turns at December 31, 2025 to 3.4 turns at June 30, 2026. It attributes both that and the inventory decrease to sales volume and 'utilization of buffer stock', and expects inventory levels to fluctuate. The inventory-reserve note text is carried unchanged. The release's cash flow line 'Inventory reserves' is for the numbers reader.",
    "account": "inventory, net",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The decrease in inventory was primarily attributable to increased volume of sales activity due to continue strength of spending within our core markets and utilization of buffer stock.",
    "paragraph_id": "0001193125-26-331632:mdna:111",
    "explanation": true
  },
  {
    "id": "revenue_recognition_remaining_performance_obligations_amount_now_stated",
    "what_changed": "Remaining performance obligations are now stated as $214.2 million at June 30, 2026. The prior period's sentence stated $159.2 million at March 31, 2026. The timing language is unchanged: the majority within a year, the rest over one to three years.",
    "account": "remaining performance obligations; unearned revenue; future revenue",
    "expected_direction": "insufficient",
    "horizon": "12 months",
    "quote": "non-cancellable hardware contracts amounted to $214.2 million",
    "paragraph_id": "0001193125-26-331632:notes:39",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_tax_valuation_allowance_limits_benefit",
    "what_changed": "The effective tax rate is now stated as an expense of 10.0% of pre-tax loss for Q2 2026 (5.9% for Q2 2025) and 53.4% for the six months (2.3%). The stated driver is loss jurisdictions where tax benefits on losses are limited by a valuation allowance; the prose implies the allowance absorbs the period's loss benefits. notes:54 states net deferred tax assets of $114.2 million and a valuation allowance of $124.5 million 'against those deferred tax assets'. The numbers reader should check how those two stated figures fit together.",
    "account": "income tax expense; deferred tax asset valuation allowance",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "driven primarily by loss jurisdictions for which the recognition of tax benefits on pre-tax losses incurred during the three and six months ended June 30, 2026 were limited due to a valuation allowance",
    "paragraph_id": "0001193125-26-331632:notes:53",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_single_customer_project_delay",
    "what_changed": "New cause in MD&A: a project delay at a single customer drove the decrease in Access & Aggregation revenue, stated as $4.3 million for the quarter and $2.9 million for six months. The overview (mdna:23) names the same delay as offsetting international growth. The customer, project and expected timing are not given. The overview also says no customer exceeded 10.0% of revenue and the five largest made up 28.8%.",
    "account": "revenue (Access & Aggregation)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The decrease in Access & Aggregation revenue was primarily driven by a project delay from a single customer",
    "paragraph_id": "0001193125-26-331632:mdna:43",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_subscriber_solutions_products_decreased_in_quarter",
    "what_changed": "MD&A says that in the quarter, Network Solutions Subscriber Solutions products decreased $2.0 million and Access & Aggregation products decreased $5.2 million. It attributes the quarter's Network Solutions growth entirely to Optical Networking ($20.6 million). The six-month sentence still says Subscriber Solutions products increased ($16.5 million). No cause is given for the quarterly Subscriber Solutions product decrease; mdna:43 attributes Subscriber Solutions growth to fiber-to-the-home, Wi-Fi 7 and Carrier Ethernet.",
    "account": "revenue (Network Solutions, Subscriber Solutions)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "partially offset by a $5.2 million decrease in Access & Aggregation products and a $2.0 million decrease in Subscriber Solutions products",
    "paragraph_id": "0001193125-26-331632:mdna:45",
    "explanation": false
  },
  {
    "id": "across_documents_category_revenue_change_labels_conflict",
    "what_changed": "For the same quarter, two MD&A paragraphs describe 'products' differently:\n- mdna:43 says Subscriber Solutions 'products' increased $0.8 million and Optical Networking Solutions 'products' increased $19.6 million.\n- mdna:45 says Subscriber Solutions products decreased $2.0 million and Optical Networking products increased $20.6 million.\n\nmdna:47 gives the Services & Support category changes. mdna:43 appears to use 'products' for whole categories (products plus services). The supervisor should reconcile the labels against the disaggregation table (notes:37).",
    "account": "revenue by category",
    "expected_direction": "insufficient",
    "horizon": "this quarter",
    "quote": "a $0.8 million increase in Subscriber Solutions products",
    "paragraph_id": "0001193125-26-331632:mdna:43",
    "explanation": false
  },
  {
    "id": "across_documents_international_revenue_two_explanations",
    "what_changed": "MD&A gives two explanations for the quarter's international revenue. The overview (mdna:23) attributes the change to broad-based strength across Europe, partly offset by one customer's project delay. The international revenue section (mdna:51) calls it relatively flat, with minor fluctuations from customer and product mix. The geographic table (notes:161) splits out the United Kingdom, Germany and other international, so the numbers reader can test which explanation fits.",
    "account": "revenue (international)",
    "expected_direction": "insufficient",
    "horizon": "this quarter",
    "quote": "The change in international revenue for the three and six months ended June 30, 2026 compared to the three and six months June 30, 2025, remained relatively flat",
    "paragraph_id": "0001193125-26-331632:mdna:51",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_earnings_release_near_term_factors",
    "what_changed": "The CEO says second-quarter results were affected by a specific set of near-term factors and does not name them. The 8-K item list shows another 8-K with items 2.02 and 7.01 filed 2026-07-22, before this release; its body is not in my input. The release presents Q1 2026 columns alongside Q2 for sequential comparison.",
    "account": "revenue; gross profit; operating income",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "While our second quarter results were affected by a specific set of near-term factors, it does not change the underlying strength or trajectory of our business.",
    "paragraph_id": "0001193125-26-331458:8k_2_02:11",
    "explanation": false
  },
  {
    "id": "across_documents_mdna_margin_text_names_only_mix",
    "what_changed": "MD&A explains every cost-of-revenue and gross-profit line (mdna:54, 56, 57, 61, 62, 63) as 'relatively flat' with fluctuations from customer and product mix or customer buying habits. It does not mention the CEO's 'specific set of near-term factors' from the same-day release, or the $0.4 million of employee exit costs the release places in cost of revenue. mdna:62 also calls the Network Solutions six-month change a 'decrease' in the same paragraph that says the six-month percentage increased.",
    "account": "gross profit; cost of revenue",
    "expected_direction": "insufficient",
    "horizon": "this quarter",
    "quote": "The gross profit as a percentage of revenue for the three and six months ended June 30, 2026, remained relatively flat, with minor fluctuations driven by changes in customer and product mix.",
    "paragraph_id": "0001193125-26-331632:mdna:61",
    "explanation": false
  },
  {
    "id": "across_documents_employee_exit_costs_only_in_earnings_release",
    "what_changed": "The release's non-GAAP footnotes say Q2 2026 includes $2.0 million of 'related employee exit costs': $0.4 million in cost of revenue (8k:59) and $1.6 million in selling, general and administrative and research and development expenses (8k:69). These sit inside 'professional fees and other expenses', which non-GAAP results exclude. In my input, neither MD&A nor the notes mention employee exit costs, severance or restructuring for the quarter. MD&A's expense explanations name only employee-related costs, travel and government subsidies. The release's Q1 2026 column shows only one-time professional fees.",
    "account": "selling, general and administrative expenses; research and development expenses; cost of revenue",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "$2.0 million in related employee exit costs",
    "paragraph_id": "0001193125-26-331458:8k_2_02:91",
    "explanation": false
  },
  {
    "id": "across_documents_customer_class_growth_claim_not_in_filing",
    "what_changed": "The release says revenue from cloud providers/hyperscalers, enterprise and government customers grew 47% year over year. The 10-Q text in my input gives no revenue by that customer class. mdna:43 says only that Optical Networking was helped by increased sales to enterprise, government and internet content provider customers. The claim cannot be checked against the filing.",
    "account": "revenue",
    "expected_direction": "insufficient",
    "horizon": "this quarter",
    "quote": "with revenue from these customers growing 47% year-over-year",
    "paragraph_id": "0001193125-26-331458:8k_2_02:12",
    "explanation": false
  },
  {
    "id": "results_against_expectations_third_quarter_outlook_range",
    "what_changed": "New guidance for the quarter ending September 30, 2026: revenue of $275.0 million to $295.0 million and non-GAAP operating margin of 1.5% to 5.5%. No GAAP reconciliation is given. How the range relates to Q2 actuals is for the numbers reader.",
    "account": "revenue; non-GAAP operating margin",
    "expected_direction": "insufficient",
    "horizon": "next quarter",
    "quote": "For the third quarter of 2026, the Company expects revenue to be within a range of $275.0 million to $295.0 million.",
    "paragraph_id": "0001193125-26-331458:8k_2_02:14",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_operating_cash_flow_decrease_stated_without_cause",
    "what_changed": "MD&A states that six-month operating cash flow decreased by $36.7 million, from $75.3 million to $38.6 million. The paragraph gives no cause. The paragraph after it (mdna:107) is carried unchanged from the prior period, so any explanation there was written for that period. The release adds quarterly operating cash flow and free cash flow columns.",
    "account": "net cash provided by operating activities",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Net cash provided by operating activities of $38.6 million during the six months ended June 30, 2026, decreased by $36.7 million compared to net cash provided by operating activities of $75.3 million during the six months ended June 30, 2025.",
    "paragraph_id": "0001193125-26-331632:mdna:106",
    "explanation": false
  },
  {
    "id": "across_documents_capital_expenditure_increase_attributed_to_developed_technology",
    "what_changed": "MD&A attributes the increase in six-month capital expenditures ($33.2 million against $32.5 million) partly to higher spending on developed technology. The release's cash flow statement has separate lines for property, plant and equipment and for 'Intangibles - internally developed technology'. notes:93 states development costs of $16.7 million for the six months. The numbers reader should check whether the developed technology line moved the way the prose says.",
    "account": "capital expenditures; intangible assets (internally developed technology)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "was primarily attributable to increases in expenditures related to developed technology, equipment and building improvements",
    "paragraph_id": "0001193125-26-331632:mdna:115",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_undescribed_financing_agreement_payments",
    "what_changed": "Financing activities now include $1.4 million of 'payments on a financing agreement'. The release's cash flow statement has a matching 'Payments on financing agreement' line, with nothing in the 2025 column. No note or MD&A paragraph in my input describes the agreement's counterparty, purpose, remaining balance or balance-sheet classification. Notes 10 and 11 cover only the revolver and the 2030 Notes.",
    "account": "financing cash flows; other liabilities or debt",
    "expected_direction": "insufficient",
    "horizon": "this quarter",
    "quote": "of payments on a financing agreement partially offset by $6.6 million proceeds from stock option exercises",
    "paragraph_id": "0001193125-26-331632:mdna:119",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_chief_revenue_officer_trading_plan",
    "what_changed": "New Item 5 disclosure: James D. Wilson, Jr., Chief Revenue Officer, adopted a Rule 10b5-1 trading arrangement on May 19, 2026 to sell 56,068 shares of common stock. It terminates on the earlier of May 31, 2027 or the sale of all shares. No other director or officer adopted or terminated a plan in the quarter.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "trading arrangement covers the sale of 56,068 shares",
    "paragraph_id": "0001193125-26-331632:notes:194",
    "explanation": false
  },
  {
    "id": "controls_audit_and_filings_item_four_disclosure_controls_not_effective",
    "what_changed": "Item 4 is carried in full and the prior Item 4 is not in my input, so what changed cannot be read. As filed, disclosure controls are not effective at June 30, 2026 because of two material weaknesses:\n1. Controls not designed to respond to changes in the risks of material misstatement.\n2. Controls over financial statement preparation, presentation and disclosure, including non-controlling interest.\n\nThe weaknesses caused the restatements of 2022-2024 and material adjustments corrected before the March 31, 2025 quarterly statements were issued. The text says they could still result in material misstatements that are not prevented or detected. There is no auditor's report in my input.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "our disclosure controls and procedures were not effective as of June 30, 2026",
    "paragraph_id": "0001193125-26-331632:item_4_controls:4",
    "explanation": false
  },
  {
    "id": "controls_audit_and_filings_remediation_controls_said_operating_but_not_remediated",
    "what_changed": "The remediation text says additional financial statement review controls were fully implemented in Q4 2025 and that management believes the enhanced and additional controls operated effectively through the filing date. The weaknesses are not considered remediated until the controls have operated for a sufficient period and been tested. Item 4 also says internal control over financial reporting did not change during the quarter. The prior Item 4 is not in my input, so whether this wording is new cannot be read.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "We believe these enhanced and additional controls operated effectively through the date of this filing.",
    "paragraph_id": "0001193125-26-331632:item_4_controls:11",
    "explanation": false
  },
  {
    "id": "controls_audit_and_filings_earnings_release_investment_line_mislabelled",
    "what_changed": "The release's statement of loss labels the line 'Net investment loss' and shows positive amounts in all four columns. MD&A (mdna:78), the MD&A percentage table and the release's own other-income reconciliation call the same line a net investment gain ('Net investment gain (loss)'). This presentation slip falls in the area of the stated material weakness over presentation and disclosure.",
    "account": "net investment gain",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Net investment loss",
    "paragraph_id": "0001193125-26-331458:8k_2_02:45",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_financial_services_instability_dropped_from_assessed_conditions",
    "what_changed": "'Instability in the financial services industry' is no longer among the conditions management considered when assessing accounting matters that depend on forecasts. The list of accounting matters assessed is unchanged.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "the unknown future impacts of ongoing inflationary pressures, continued elevated interest rates, currency fluctuations and political tensions",
    "paragraph_id": "0001193125-26-331632:notes:20",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_convertible_note_terms_referred_to_annual_report",
    "what_changed": "The 10-Q no longer states several 2030 Notes terms and now refers to the 2025 Form 10-K for them. Removed:\n- holder conversion conditions before June 15, 2030: the 130%-of-conversion-price trigger on 20 of 30 trading days, the 98% trading-price trigger, corporate events and redemption calls\n- the settlement method\n- the Company's redemption right from September 20, 2028, with the $70.0 million minimum outstanding for partial redemption\n- holders' repurchase rights on a fundamental change\n\nStill stated: the conversion rate (86.8206 shares per $1,000, about $11.52 per share), the capped call terms and the estimated fair value of $307.0 million at June 30, 2026. The EPS note lists convertible senior notes among excluded shares.",
    "account": "non-current convertible senior notes",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "For additional information regarding the terms of the 2030 Notes, refer to the Consolidated Financial Statements and related footnotes in the Company's fiscal 2025 Annual Report on Form 10-K.",
    "paragraph_id": "0001193125-26-331632:notes:114",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_performance_bond_commitments_now_stated",
    "what_changed": "Bid, performance and customs bond commitments are now stated as $23.3 million at June 30, 2026, expiring at various dates through October 2029. The prior text stated $22.2 million at March 31, 2026, expiring through April 2029. The probability of default is still called remote.",
    "account": "guarantees (off-balance-sheet)",
    "expected_direction": "insufficient",
    "horizon": "12 months",
    "quote": "we had commitments related to these bonds totaling $23.3 million and $22.4 million, respectively, which expire at various dates through October 2029",
    "paragraph_id": "0001193125-26-331632:notes:174",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_purchase_obligations_now_stated",
    "what_changed": "Purchase obligations are now stated as $232.0 million at June 30, 2026; the prior text stated $223.7 million at March 31, 2026. They include multi-year supply and pricing commitments with contract manufacturers and suppliers. The MD&A cash requirements table schedules them across 2026-2029.",
    "account": "purchase obligations; inventory",
    "expected_direction": "insufficient",
    "horizon": "12 months",
    "quote": "As of June 30, 2026, purchase obligations totaled $232.0 million.",
    "paragraph_id": "0001193125-26-331632:notes:176",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_dplta_loss_absorption_extends_to_current_year",
    "what_changed": "This paragraph is carried as changed text but is not in the note change history, so the prior wording is not in my input. As filed, it says ADTRAN Holdings must absorb Adtran Networks' 2025 annual net loss and will absorb any 2026 net loss. No amount is stated for either year.",
    "account": "cash; redeemable non-controlling interest",
    "expected_direction": "insufficient",
    "horizon": "12 months",
    "quote": "applies to the net loss generated by Adtran Networks in 2025, and it will apply to any net loss generated by Adtran Networks in 2026",
    "paragraph_id": "0001193125-26-331632:notes:172",
    "explanation": false
  }
]
```

Item count: 44. Items marked `insufficient`: 14. Items with `explanation: true`: 4.

## Paragraphs carried as text that are not an item

### Item 4 (input_controls.md)

- `0001193125-26-331632:item_4_controls:1` — heading
- `0001193125-26-331632:item_4_controls:2` — heading
- `0001193125-26-331632:item_4_controls:3` — definition of disclosure controls; boilerplate; prior Item 4 not in input
- `0001193125-26-331632:item_4_controls:5` — heading
- `0001193125-26-331632:item_4_controls:6` — material weakness definition and determination; carried in item controls_audit_and_filings_item_four_disclosure_controls_not_effective
- `0001193125-26-331632:item_4_controls:7` — first material weakness; carried in item controls_audit_and_filings_item_four_disclosure_controls_not_effective
- `0001193125-26-331632:item_4_controls:8` — second material weakness; carried in item controls_audit_and_filings_item_four_disclosure_controls_not_effective
- `0001193125-26-331632:item_4_controls:9` — restatement history; carried in item controls_audit_and_filings_item_four_disclosure_controls_not_effective
- `0001193125-26-331632:item_4_controls:10` — heading
- `0001193125-26-331632:item_4_controls:12` — not-yet-remediated condition; carried in item controls_audit_and_filings_remediation_controls_said_operating_but_not_remediated
- `0001193125-26-331632:item_4_controls:13` — heading
- `0001193125-26-331632:item_4_controls:14` — no change in internal control during quarter; carried in item controls_audit_and_filings_remediation_controls_said_operating_but_not_remediated
- `0001193125-26-331632:item_4_controls:15` — page number

### MD&A (input_mdna.md)

- `0001193125-26-331632:mdna:1` — heading
- `0001193125-26-331632:mdna:8` — business overview; no new amount, date, commitment or risk visible; prior wording not in input
- `0001193125-26-331632:mdna:16` — DPLTA terms and ARC payment; same changes as items liquidity_and_capital_dplta_annual_recurring_compensation_paid and related_parties_contingencies_and_subsequent_events_dplta_appraisal_decision_timing
- `0001193125-26-331632:mdna:17` — appraisal timeline; same change as item related_parties_contingencies_and_subsequent_events_dplta_appraisal_decision_timing
- `0001193125-26-331632:mdna:18` — Exit Compensation tenders; same change as item liquidity_and_capital_dplta_exit_compensation_tenders_paid
- `0001193125-26-331632:mdna:19` — liquidity adequacy summary; conclusion unchanged; still cites the Wells Fargo amendments (wording)
- `0001193125-26-331632:mdna:20` — Adtran Networks shares held and percentage; amounts only (cited in tenders item)
- `0001193125-26-331632:mdna:23` — quarter overview; project delay in item narrative_signs_of_operating_pressure_single_customer_project_delay; international explanation in item across_documents_international_revenue_two_explanations; concentration figures amounts only
- `0001193125-26-331632:mdna:26` — tariff actions; same change as item narrative_signs_of_operating_pressure_ustr_tariffs_replace_expired_tariffs
- `0001193125-26-331632:mdna:27` — general tariff-risk and supply-chain mitigation language; no new amount, date or commitment visible
- `0001193125-26-331632:mdna:31` — IEEPA refund not probable; same change as item estimates_and_discretion_ieepa_tariff_refund_not_recognized
- `0001193125-26-331632:mdna:37` — page number
- `0001193125-26-331632:mdna:38` — heading; dates rolled forward
- `0001193125-26-331632:mdna:40` — percentage-of-revenue table; amounts only
- `0001193125-26-331632:mdna:42` — total revenue growth; amounts rolled, drivers as before
- `0001193125-26-331632:mdna:44` — heading
- `0001193125-26-331632:mdna:46` — heading
- `0001193125-26-331632:mdna:47` — Services & Support category changes; amounts only (referenced in item across_documents_category_revenue_change_labels_conflict)
- `0001193125-26-331632:mdna:48` — heading
- `0001193125-26-331632:mdna:49` — U.S. revenue; amounts only
- `0001193125-26-331632:mdna:50` — heading
- `0001193125-26-331632:mdna:52` — description of international revenue drivers; no visible change in substance
- `0001193125-26-331632:mdna:54` — cost of revenue percentage; amounts only, mix boilerplate (referenced in item across_documents_mdna_margin_text_names_only_mix)
- `0001193125-26-331632:mdna:55` — currency effect on cost of revenue; amounts only
- `0001193125-26-331632:mdna:56` — Network Solutions cost percentage; amounts only
- `0001193125-26-331632:mdna:57` — Services & Support cost percentage; amounts only
- `0001193125-26-331632:mdna:58` — Services & Support description; no visible change (paragraph split at page break)
- `0001193125-26-331632:mdna:59` — continuation of mdna:58; no visible change
- `0001193125-26-331632:mdna:62` — Network Solutions gross profit; amounts only; wording slip noted in item across_documents_mdna_margin_text_names_only_mix
- `0001193125-26-331632:mdna:63` — Services & Support gross profit; amounts only
- `0001193125-26-331632:mdna:65` — SG&A percentage; amounts only
- `0001193125-26-331632:mdna:66` — SG&A; amounts rolled; six-month drivers employee-related costs and travel (gap noted in item across_documents_employee_exit_costs_only_in_earnings_release)
- `0001193125-26-331632:mdna:68` — R&D percentage; amounts only
- `0001193125-26-331632:mdna:69` — R&D; amounts rolled; drivers employee costs and subsidies
- `0001193125-26-331632:mdna:70` — government grants; amounts only
- `0001193125-26-331632:mdna:71` — R&D boilerplate; split at page break
- `0001193125-26-331632:mdna:72` — continuation of mdna:71; boilerplate
- `0001193125-26-331632:mdna:74` — interest and dividend income; amounts only
- `0001193125-26-331632:mdna:76` — interest expense; amounts; drivers as previously disclosed (2030 Notes, Wells Fargo paydown)
- `0001193125-26-331632:mdna:77` — heading
- `0001193125-26-331632:mdna:78` — net investment gain; amounts only (label conflict in item controls_audit_and_filings_earnings_release_investment_line_mislabelled)
- `0001193125-26-331632:mdna:79` — heading
- `0001193125-26-331632:mdna:80` — other income (expense); amounts only
- `0001193125-26-331632:mdna:81` — heading
- `0001193125-26-331632:mdna:82` — effective tax rate; same change as item estimates_and_discretion_tax_valuation_allowance_limits_benefit
- `0001193125-26-331632:mdna:84` — net loss attributable; amounts only
- `0001193125-26-331632:mdna:87` — operating cash flow amount; amounts only
- `0001193125-26-331632:mdna:88` — cash, foreign-held cash, facility availability; amounts only
- `0001193125-26-331632:mdna:90` — DPLTA terms; same change as item related_parties_contingencies_and_subsequent_events_dplta_appraisal_decision_timing
- `0001193125-26-331632:mdna:91` — ARC; same change as item liquidity_and_capital_dplta_annual_recurring_compensation_paid
- `0001193125-26-331632:mdna:92` — Former Credit Agreement availability; same change as item liquidity_and_capital_wells_fargo_facility_replaced_by_jp_morgan
- `0001193125-26-331632:mdna:93` — new credit agreement; same change as item liquidity_and_capital_wells_fargo_facility_replaced_by_jp_morgan
- `0001193125-26-331632:mdna:95` — page number
- `0001193125-26-331632:mdna:96` — continuation of remote-probability factors; same change as item estimates_and_discretion_exit_compensation_remote_probability_basis
- `0001193125-26-331632:mdna:97` — liquidity adequacy summary; references updated to Former/New Credit Agreement; conclusion unchanged
- `0001193125-26-331632:mdna:100` — 2030 Notes issuance; previously disclosed; no visible change
- `0001193125-26-331632:mdna:101` — 2030 Notes interest expense and issuance costs; amounts only
- `0001193125-26-331632:mdna:102` — new heading; same change as item liquidity_and_capital_wells_fargo_facility_replaced_by_jp_morgan
- `0001193125-26-331632:mdna:103` — new agreement terms; same changes as items liquidity_and_capital_wells_fargo_facility_replaced_by_jp_morgan and structure_and_disclosure_changes_credit_covenant_levels_no_longer_stated
- `0001193125-26-331632:mdna:104` — termination of collateral and guaranty agreements; same change as item related_parties_contingencies_and_subsequent_events_credit_collateral_and_guaranty_terminated
- `0001193125-26-331632:mdna:108` — operating cash flow table; amounts only
- `0001193125-26-331632:mdna:116` — deferred compensation and marketable securities; amounts only
- `0001193125-26-331632:mdna:118` — financing activities; amounts (RNCI and ARC in their items; financing agreement in item structure_and_disclosure_changes_undescribed_financing_agreement_payments)
- `0001193125-26-331632:mdna:121` — no stock repurchases; dates rolled forward
- `0001193125-26-331632:mdna:123` — option exercises; amounts only
- `0001193125-26-331632:mdna:128` — deferred compensation program assets and liabilities; amounts only
- `0001193125-26-331632:mdna:130` — off-balance-sheet statement; date rolled forward
- `0001193125-26-331632:mdna:132` — cash requirements table intro now dated to the filing; same change as item liquidity_and_capital_post_quarter_draw_on_jp_morgan_facility
- `0001193125-26-331632:mdna:133` — cash requirements table; amounts; J.P. Morgan line in item liquidity_and_capital_post_quarter_draw_on_jp_morgan_facility
- `0001193125-26-331632:mdna:134` — table footnote (1); same change as item liquidity_and_capital_post_quarter_draw_on_jp_morgan_facility
- `0001193125-26-331632:mdna:136` — continuation of footnote (1); same change as item liquidity_and_capital_post_quarter_draw_on_jp_morgan_facility
- `0001193125-26-331632:mdna:137` — continuation of footnote (1); cross-reference only
- `0001193125-26-331632:mdna:138` — continuation of footnote (1); cross-reference only
- `0001193125-26-331632:mdna:139` — footnote (2) cross-reference
- `0001193125-26-331632:mdna:140` — purchase obligations footnote; wording
- `0001193125-26-331632:mdna:141` — settlement years 2026 through 2029; date rolled forward
- `0001193125-26-331632:mdna:142` — cross-reference
- `0001193125-26-331632:mdna:143` — fragment ('information.')
- `0001193125-26-331632:mdna:144` — lease description; no change visible
- `0001193125-26-331632:mdna:145` — remaining lease terms; amounts only
- `0001193125-26-331632:mdna:151` — DPLTA execution and effective dates; previously disclosed facts
- `0001193125-26-331632:mdna:153` — DPLTA terms (part one); same change as item related_parties_contingencies_and_subsequent_events_dplta_appraisal_decision_timing
- `0001193125-26-331632:mdna:154` — DPLTA terms (part two); same change as item related_parties_contingencies_and_subsequent_events_dplta_appraisal_decision_timing
- `0001193125-26-331632:mdna:155` — ARC; same change as item liquidity_and_capital_dplta_annual_recurring_compensation_paid
- `0001193125-26-331632:mdna:156` — 2022 board authorization to buy Adtran Networks shares; previously disclosed; no change visible
- `0001193125-26-331632:mdna:157` — tenders; same change as item liquidity_and_capital_dplta_exit_compensation_tenders_paid
- `0001193125-26-331632:mdna:158` — Adtran Networks shares held; amounts only
- `0001193125-26-331632:mdna:159` — DPLTA exhibit reference to 2025 Form 10-K; wording
- `0001193125-26-331632:mdna:161` — cash-requirements change statement naming DPLTA payments and receivables purchase arrangements; omission of the refinancing noted in item liquidity_and_capital_post_quarter_draw_on_jp_morgan_facility; otherwise wording
- `0001193125-26-331632:mdna:163` — performance bonds; same change as item related_parties_contingencies_and_subsequent_events_performance_bond_commitments_now_stated
- `0001193125-26-331632:mdna:166` — critical accounting policies statement; period rolled forward to six months
- `0001193125-26-331632:mdna:167` — page number

### Notes (input_notes.md)

- `0001193125-26-331632:notes:4` — section heading
- `0001193125-26-331632:notes:7` — DPLTA terms and timeline; same change as item related_parties_contingencies_and_subsequent_events_dplta_appraisal_decision_timing
- `0001193125-26-331632:notes:9` — Former Credit Agreement and refinancing; same change as item liquidity_and_capital_wells_fargo_facility_replaced_by_jp_morgan
- `0001193125-26-331632:notes:12` — 2030 Notes issuance; previously disclosed; not in the change history
- `0001193125-26-331632:notes:13` — liquidity adequacy statement; facility reference updated for refinancing; conclusion unchanged
- `0001193125-26-331632:notes:19` — list of significant estimates; not in the change history; no visible change
- `0001193125-26-331632:notes:21` — no other changes to critical policies; period rolled forward
- `0001193125-26-331632:notes:23` — ASU 2025-06 description; no visible change
- `0001193125-26-331632:notes:24` — ASU 2024-03 description; no visible change
- `0001193125-26-331632:notes:25` — heading
- `0001193125-26-331632:notes:26` — no recently adopted pronouncements; no change
- `0001193125-26-331632:notes:37` — three-month disaggregation table; amounts only, rows reordered
- `0001193125-26-331632:notes:38` — six-month disaggregation table; amounts only
- `0001193125-26-331632:notes:41` — contract balances table; amounts only
- `0001193125-26-331632:notes:45` — heading; singular 'Agreement' (wording)
- `0001193125-26-331632:notes:49` — no allowance on contract assets; period rolled forward
- `0001193125-26-331632:notes:51` — unearned revenue recognized; amounts only
- `0001193125-26-331632:notes:54` — deferred tax assets and valuation allowance amounts; same change as item estimates_and_discretion_tax_valuation_allowance_limits_benefit
- `0001193125-26-331632:notes:58` — shares available for awards; amounts only
- `0001193125-26-331632:notes:59` — stock-based compensation expense; amounts only
- `0001193125-26-331632:notes:61` — table intro; dates rolled forward
- `0001193125-26-331632:notes:62` — PSU/RSU table; amounts only
- `0001193125-26-331632:notes:64` — unrecognized compensation; amounts only
- `0001193125-26-331632:notes:65` — heading
- `0001193125-26-331632:notes:66` — table intro
- `0001193125-26-331632:notes:67` — fair value table at June 30, 2026; amounts only
- `0001193125-26-331632:notes:68` — fair value table at December 31, 2025; amounts only
- `0001193125-26-331632:notes:69` — money market footnote; date rolled forward
- `0001193125-26-331632:notes:70` — pricing method; no visible change (hierarchy definitions removed per history are boilerplate)
- `0001193125-26-331632:notes:72` — inventory intro; date rolled forward
- `0001193125-26-331632:notes:73` — inventory table; amounts only
- `0001193125-26-331632:notes:77` — PP&E table; amounts only
- `0001193125-26-331632:notes:79` — depreciation expense; amounts only
- `0001193125-26-331632:notes:82` — assets held for sale; date rolled forward
- `0001193125-26-331632:notes:84` — goodwill intro; dates rolled forward
- `0001193125-26-331632:notes:85` — goodwill table; amounts only
- `0001193125-26-331632:notes:86` — goodwill impairment policy; no visible change
- `0001193125-26-331632:notes:87` — no goodwill impairment; dates rolled forward
- `0001193125-26-331632:notes:89` — intangibles intro; date rolled forward
- `0001193125-26-331632:notes:90` — intangibles table; amounts only
- `0001193125-26-331632:notes:91` — no intangible impairment; dates rolled forward
- `0001193125-26-331632:notes:92` — amortization expense; amounts only
- `0001193125-26-331632:notes:93` — capitalized development costs; amounts only
- `0001193125-26-331632:notes:95` — amortization schedule; amounts only
- `0001193125-26-331632:notes:96` — heading
- `0001193125-26-331632:notes:97` — table intro
- `0001193125-26-331632:notes:98` — revolver table; amounts only
- `0001193125-26-331632:notes:99` — revolver fair value and rate; amounts only (rate cited in item liquidity_and_capital_wells_fargo_facility_replaced_by_jp_morgan)
- `0001193125-26-331632:notes:100` — heading
- `0001193125-26-331632:notes:101` — amendment history; defined term renamed 'Former Credit Agreement' (wording)
- `0001193125-26-331632:notes:102` — facility size; tense changed (wording)
- `0001193125-26-331632:notes:103` — borrowings, letters of credit and availability; same change as item liquidity_and_capital_wells_fargo_facility_replaced_by_jp_morgan
- `0001193125-26-331632:notes:104` — German sublimit; tense changed (wording)
- `0001193125-26-331632:notes:106` — heading
- `0001193125-26-331632:notes:107` — table intro
- `0001193125-26-331632:notes:108` — convertible notes table; amounts only
- `0001193125-26-331632:notes:109` — convertible notes fair value; amounts only
- `0001193125-26-331632:notes:110` — effective interest rate; no visible change
- `0001193125-26-331632:notes:111` — interest expense table; amounts only
- `0001193125-26-331632:notes:112` — 2030 Notes terms; paragraph split (wording)
- `0001193125-26-331632:notes:113` — continuation of conversion terms; paragraph split (wording)
- `0001193125-26-331632:notes:115` — heading
- `0001193125-26-331632:notes:116` — capped call terms; no visible change
- `0001193125-26-331632:notes:117` — capped call purpose; no visible change
- `0001193125-26-331632:notes:118` — capped call accounting; no visible change
- `0001193125-26-331632:notes:121` — pension intro; dates rolled forward
- `0001193125-26-331632:notes:122` — pension balance table; amounts only
- `0001193125-26-331632:notes:125` — net periodic pension cost table; amounts only
- `0001193125-26-331632:notes:126` — pension contributions and expected remainder; amounts only
- `0001193125-26-331632:notes:130` — AOCI table Q2 2026; amounts only
- `0001193125-26-331632:notes:131` — AOCI table Q2 2025; amounts only
- `0001193125-26-331632:notes:132` — AOCI table six months 2026; amounts only
- `0001193125-26-331632:notes:133` — AOCI table six months 2025; amounts only
- `0001193125-26-331632:notes:134` — table intro
- `0001193125-26-331632:notes:135` — reclassification table Q2 2026; amounts only
- `0001193125-26-331632:notes:136` — reclassification table Q2 2025; amounts only
- `0001193125-26-331632:notes:138` — reclassification table six months 2026; amounts only
- `0001193125-26-331632:notes:139` — reclassification table six months 2025; amounts only
- `0001193125-26-331632:notes:140` — table intro
- `0001193125-26-331632:notes:141` — OCI tax effects, three months; amounts only
- `0001193125-26-331632:notes:142` — OCI tax effects, six months; amounts only
- `0001193125-26-331632:notes:143` — RNCI table intro; dates rolled forward
- `0001193125-26-331632:notes:144` — RNCI roll-forward table; amounts only
- `0001193125-26-331632:notes:146` — EPS intro; dates rolled forward
- `0001193125-26-331632:notes:147` — EPS table; amounts only
- `0001193125-26-331632:notes:149` — antidilutive shares table; amounts only
- `0001193125-26-331632:notes:151` — CODM and two reportable segments; no change visible
- `0001193125-26-331632:notes:152` — Network Solutions segment description; no change visible
- `0001193125-26-331632:notes:154` — segment performance basis; no change visible
- `0001193125-26-331632:notes:156` — segment table, three months; amounts only
- `0001193125-26-331632:notes:157` — segment table, six months; amounts only
- `0001193125-26-331632:notes:158` — segment depreciation; amounts only
- `0001193125-26-331632:notes:161` — revenue by geography table; amounts only (used in item across_documents_international_revenue_two_explanations)
- `0001193125-26-331632:notes:162` — heading
- `0001193125-26-331632:notes:163` — heading
- `0001193125-26-331632:notes:164` — general legal-matters language; no visible change
- `0001193125-26-331632:notes:166` — heading
- `0001193125-26-331632:notes:167` — DPLTA appraisal proceedings; no new amount, date or estimate visible; prior wording not in input
- `0001193125-26-331632:notes:168` — heading
- `0001193125-26-331632:notes:170` — ARC; same change as item liquidity_and_capital_dplta_annual_recurring_compensation_paid
- `0001193125-26-331632:notes:173` — heading
- `0001193125-26-331632:notes:175` — heading
- `0001193125-26-331632:notes:177` — heading
- `0001193125-26-331632:notes:179` — loss recovery model and inventory/COGS treatment; same item as estimates_and_discretion_ieepa_tariff_refund_not_recognized
- `0001193125-26-331632:notes:180` — probability threshold and CBP system date; same item as estimates_and_discretion_ieepa_tariff_refund_not_recognized
- `0001193125-26-331632:notes:183` — heading
- `0001193125-26-331632:notes:185` — heading
- `0001193125-26-331632:notes:186` — heading
- `0001193125-26-331632:notes:189` — continuation of terminated agreements; same change as item related_parties_contingencies_and_subsequent_events_credit_collateral_and_guaranty_terminated
- `0001193125-26-331632:notes:190` — heading
- `0001193125-26-331632:notes:191` — 'Not applicable'
- `0001193125-26-331632:notes:192` — 'Not applicable'
- `0001193125-26-331632:notes:193` — heading
- `0001193125-26-331632:notes:195` — no other trading plans; boilerplate, carried in item related_parties_contingencies_and_subsequent_events_chief_revenue_officer_trading_plan

### 8-K item 2.02 (input_8k.md)

- `0001193125-26-331458:8k_2_02:1` — exhibit header
- `0001193125-26-331458:8k_2_02:2` — exhibit header
- `0001193125-26-331458:8k_2_02:3` — release title
- `0001193125-26-331458:8k_2_02:4` — dateline
- `0001193125-26-331458:8k_2_02:5` — revenue highlight; amounts only
- `0001193125-26-331458:8k_2_02:6` — gross margin highlight; amounts only
- `0001193125-26-331458:8k_2_02:7` — operating margin highlight; amounts only
- `0001193125-26-331458:8k_2_02:8` — operating cash flow highlight; amounts only
- `0001193125-26-331458:8k_2_02:9` — EPS highlight; amounts only
- `0001193125-26-331458:8k_2_02:10` — cash highlight; amounts only
- `0001193125-26-331458:8k_2_02:13` — heading
- `0001193125-26-331458:8k_2_02:15` — non-GAAP guidance footnote; boilerplate
- `0001193125-26-331458:8k_2_02:16` — heading
- `0001193125-26-331458:8k_2_02:17` — conference call logistics
- `0001193125-26-331458:8k_2_02:18` — replay logistics
- `0001193125-26-331458:8k_2_02:19` — heading
- `0001193125-26-331458:8k_2_02:20` — investor conference date
- `0001193125-26-331458:8k_2_02:21` — investor conference date
- `0001193125-26-331458:8k_2_02:22` — heading
- `0001193125-26-331458:8k_2_02:23` — company description
- `0001193125-26-331458:8k_2_02:24` — company description
- `0001193125-26-331458:8k_2_02:25` — heading with no body in input
- `0001193125-26-331458:8k_2_02:26` — heading
- `0001193125-26-331458:8k_2_02:27` — non-GAAP definitions; boilerplate
- `0001193125-26-331458:8k_2_02:28` — contact block
- `0001193125-26-331458:8k_2_02:29` — contact block
- `0001193125-26-331458:8k_2_02:30` — contact block
- `0001193125-26-331458:8k_2_02:31` — contact block
- `0001193125-26-331458:8k_2_02:32` — contact block
- `0001193125-26-331458:8k_2_02:33` — contact block
- `0001193125-26-331458:8k_2_02:34` — contact block
- `0001193125-26-331458:8k_2_02:35` — contact block
- `0001193125-26-331458:8k_2_02:36` — contact block
- `0001193125-26-331458:8k_2_02:37` — contact block
- `0001193125-26-331458:8k_2_02:38` — heading
- `0001193125-26-331458:8k_2_02:39` — heading
- `0001193125-26-331458:8k_2_02:40` — heading
- `0001193125-26-331458:8k_2_02:41` — balance sheet; amounts only
- `0001193125-26-331458:8k_2_02:42` — heading
- `0001193125-26-331458:8k_2_02:43` — heading
- `0001193125-26-331458:8k_2_02:44` — heading
- `0001193125-26-331458:8k_2_02:46` — NCI accrual footnote; amounts only (same as ARC item)
- `0001193125-26-331458:8k_2_02:47` — RNCI effect on EPS; amounts only
- `0001193125-26-331458:8k_2_02:48` — heading
- `0001193125-26-331458:8k_2_02:49` — heading
- `0001193125-26-331458:8k_2_02:50` — heading
- `0001193125-26-331458:8k_2_02:51` — cash flow statement; amounts only (lines cited in ARC, capex and financing-agreement items)
- `0001193125-26-331458:8k_2_02:52` — heading
- `0001193125-26-331458:8k_2_02:53` — heading
- `0001193125-26-331458:8k_2_02:54` — heading
- `0001193125-26-331458:8k_2_02:55` — heading
- `0001193125-26-331458:8k_2_02:56` — heading
- `0001193125-26-331458:8k_2_02:57` — gross margin reconciliation table; amounts only
- `0001193125-26-331458:8k_2_02:58` — amortization rationale; boilerplate
- `0001193125-26-331458:8k_2_02:59` — exit costs in cost of revenue; same change as item across_documents_employee_exit_costs_only_in_earnings_release
- `0001193125-26-331458:8k_2_02:60` — heading
- `0001193125-26-331458:8k_2_02:61` — heading
- `0001193125-26-331458:8k_2_02:62` — heading
- `0001193125-26-331458:8k_2_02:63` — heading
- `0001193125-26-331458:8k_2_02:64` — operating expense reconciliation table; amounts only
- `0001193125-26-331458:8k_2_02:65` — amortization rationale; boilerplate
- `0001193125-26-331458:8k_2_02:66` — amortization split; amounts only
- `0001193125-26-331458:8k_2_02:67` — stock compensation split; amounts only
- `0001193125-26-331458:8k_2_02:68` — deferred compensation description; boilerplate
- `0001193125-26-331458:8k_2_02:69` — exit costs and 401(k) reversal in opex; same changes as items across_documents_employee_exit_costs_only_in_earnings_release and earnings_quality_retirement_plan_correction_accrual_reversed
- `0001193125-26-331458:8k_2_02:70` — Q1 2026 amortization split; amounts only
- `0001193125-26-331458:8k_2_02:71` — Q1 2026 stock compensation split; amounts only
- `0001193125-26-331458:8k_2_02:72` — Q1 2026 one-time professional fees; prior-quarter column
- `0001193125-26-331458:8k_2_02:73` — Q2 2025 amortization split; prior-year column
- `0001193125-26-331458:8k_2_02:74` — Q2 2025 stock compensation split; prior-year column
- `0001193125-26-331458:8k_2_02:75` — 2025 Business Efficiency Program true-up and headquarters sale aim; prior-year column
- `0001193125-26-331458:8k_2_02:76` — 2025 internal investigation fees; prior-year column
- `0001193125-26-331458:8k_2_02:77` — six-month amortization split; amounts only
- `0001193125-26-331458:8k_2_02:78` — six-month stock compensation split; amounts only
- `0001193125-26-331458:8k_2_02:79` — six-month exit costs and 401(k) reversal; same changes as items across_documents_employee_exit_costs_only_in_earnings_release and earnings_quality_retirement_plan_correction_accrual_reversed
- `0001193125-26-331458:8k_2_02:80` — 2025 six-month amortization split; prior-year column
- `0001193125-26-331458:8k_2_02:81` — 2025 six-month stock compensation split; prior-year column
- `0001193125-26-331458:8k_2_02:82` — 2025 internal investigation fees; prior-year column
- `0001193125-26-331458:8k_2_02:83` — heading
- `0001193125-26-331458:8k_2_02:84` — heading
- `0001193125-26-331458:8k_2_02:85` — heading
- `0001193125-26-331458:8k_2_02:86` — heading
- `0001193125-26-331458:8k_2_02:87` — heading
- `0001193125-26-331458:8k_2_02:88` — operating income reconciliation table; amounts only
- `0001193125-26-331458:8k_2_02:89` — amortization rationale; boilerplate
- `0001193125-26-331458:8k_2_02:90` — deferred compensation description; boilerplate
- `0001193125-26-331458:8k_2_02:92` — Q1 2026 one-time fees; prior-quarter column
- `0001193125-26-331458:8k_2_02:93` — 2025 internal investigation fees; prior-year column
- `0001193125-26-331458:8k_2_02:94` — heading
- `0001193125-26-331458:8k_2_02:95` — heading
- `0001193125-26-331458:8k_2_02:96` — heading
- `0001193125-26-331458:8k_2_02:97` — heading
- `0001193125-26-331458:8k_2_02:98` — other income reconciliation table; amounts only
- `0001193125-26-331458:8k_2_02:99` — deferred compensation description; boilerplate
- `0001193125-26-331458:8k_2_02:100` — pension amortization description; boilerplate
- `0001193125-26-331458:8k_2_02:101` — heading
- `0001193125-26-331458:8k_2_02:102` — heading
- `0001193125-26-331458:8k_2_02:103` — heading
- `0001193125-26-331458:8k_2_02:104` — heading
- `0001193125-26-331458:8k_2_02:105` — heading
- `0001193125-26-331458:8k_2_02:106` — heading
- `0001193125-26-331458:8k_2_02:107` — heading
- `0001193125-26-331458:8k_2_02:108` — heading
- `0001193125-26-331458:8k_2_02:109` — heading
- `0001193125-26-331458:8k_2_02:110` — heading
- `0001193125-26-331458:8k_2_02:111` — heading
- `0001193125-26-331458:8k_2_02:112` — net income and EPS reconciliation table; amounts only
- `0001193125-26-331458:8k_2_02:113` — RNCI effect on EPS; amounts only
- `0001193125-26-331458:8k_2_02:114` — NCI description; boilerplate
- `0001193125-26-331458:8k_2_02:115` — amortization rationale; boilerplate
- `0001193125-26-331458:8k_2_02:116` — deferred compensation description; boilerplate
- `0001193125-26-331458:8k_2_02:117` — pension amortization description; boilerplate
- `0001193125-26-331458:8k_2_02:118` — 2025 restructuring reversal; prior-year column
- `0001193125-26-331458:8k_2_02:119` — exit costs and 401(k) reversal; same changes as items across_documents_employee_exit_costs_only_in_earnings_release and earnings_quality_retirement_plan_correction_accrual_reversed
- `0001193125-26-331458:8k_2_02:120` — Q1 2026 one-time fees; prior-quarter column
- `0001193125-26-331458:8k_2_02:121` — 2025 internal investigation fees; prior-year column
- `0001193125-26-331458:8k_2_02:122` — heading
- `0001193125-26-331458:8k_2_02:123` — heading
- `0001193125-26-331458:8k_2_02:124` — heading
- `0001193125-26-331458:8k_2_02:125` — heading
- `0001193125-26-331458:8k_2_02:126` — free cash flow table; amounts only
- `0001193125-26-331458:8k_2_02:127` — free cash flow footnote; boilerplate
