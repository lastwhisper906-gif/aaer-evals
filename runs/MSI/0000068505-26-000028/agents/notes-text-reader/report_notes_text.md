# report_notes_text: MSI 10-Q 0000068505-26-000028 (quarter ended July 4, 2026)

## Scope

Inputs read in full: input_notes.md (notes:1 to notes:199), input_notes_history.md (note_history:1 to 28, used only to see what is new), input_mdna.md (mdna:1 to mdna:209), input_controls.md (item_4_controls:1 to 4), input_8k.md (item-code list, late-filing list, and the Item 2.02 release 0000068505-26-000027:8k_2_02:1 to 157), and input_prior_predictions.md (none on record).

Not in the input, so nothing is reported from them: an Item 1A diff, an Exhibit 21 diff, any Exhibit 10, and an auditor's report (this is a 10-Q and none is carried). The only 8-K body carried is the 2026-08-05 Item 2.02 release. Of the other 8-Ks, only the item codes are given.

Out-of-scope check: there is no trend table, price series, abnormal return, short interest, other company's file, prior-run probability or outcome window in the directory. The release and MD&A do give the average price the company paid in its own share buybacks. That is the company's own disclosure, not market data.

No arithmetic was done. Where an item puts two figures side by side, both figures come from the prose. Checking or reconciling them is left to the numbers reader.

## Items

```json
[
  {
    "id": "structure_and_disclosure_changes_dfend_acquisition_agreement",
    "what_changed": "New paragraph, marked 'added' in the change history. The Company says that on May 31, 2026 it entered a definitive agreement to acquire D-Fend, a counter-drone technology company, for $1.5 billion, subject to customary adjustments. Completion is expected in the second half of 2026. The paragraph does not say how the deal will be funded. The derivatives note separately adds Treasury rate locks on forecasted debt transactions (notes:125). The release lists the agreement in its highlights (8k_2_02:13, :26).",
    "account": "Goodwill and Intangible assets, net",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "On May 31, 2026, the Company entered into a definitive agreement to acquire D-Fend for $1.5 billion, subject to customary adjustments.",
    "paragraph_id": "0000068505-26-000028:notes:11",
    "explanation": false
  },
  {
    "id": "across_documents_dfend_agreement_without_material_agreement_filing",
    "what_changed": "The notes date the D-Fend definitive agreement May 31, 2026. The 8-K item-code list shows no Item 1.01 filing on or after that date. The only later 8-K is the 2026-08-05 Item 2.02/9.01 release, which mentions the agreement. The Bell Mobility agreement of March 26, 2026 (notes:12) also has no Item 1.01 entry in the list. Earlier periods do show Item 1.01 filings, for example 2025-05-27 and 2025-07-21. Whether Item 1.01 was required is a materiality judgment outside this reader, so this is flagged for the supervisors.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "D-Fend provides advanced counter-drone technology.",
    "paragraph_id": "0000068505-26-000028:notes:11",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_bell_mobility_segment_sentence_removed",
    "what_changed": "A sentence was removed. The prior text said: 'Subject to the closing of the transaction, this business will be part of both the Products and Systems Integration segment and the Software and Services segment.' The paragraph no longer assigns the Bell Mobility LMR services business to any segment. The price (675 million Canadian dollars) and the expected completion in the fourth quarter of 2026 are unchanged. A sentence with the same two-segment wording now appears in the Silvus paragraph (notes:184).",
    "account": "Segment net sales (allocation of acquired business)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "The acquisition is expected to be completed in the fourth quarter of 2026.",
    "paragraph_id": "0000068505-26-000028:notes:12",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_credit_loss_practical_expedient_elected",
    "what_changed": "Under 'Recently Adopted Accounting Pronouncements', the paragraph says the Company has elected the ASU 2025-05 practical expedient. For current receivables and contract assets, it assumes that conditions at the balance sheet date do not change for the rest of the asset's life. The Company says this had no material impact on expected credit losses. The input does not carry the prior wording, so I cannot confirm whether the election is new this quarter. The policy affects how the allowance for credit losses is estimated.",
    "account": "Allowance for credit losses (Accounts receivable, net; Contract assets)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The Company has elected the practical expedient to assume that current conditions as of the balance sheet date do not change for the remaining life of the asset, which did not have a material impact to the Company's current expected credit losses.",
    "paragraph_id": "0000068505-26-000028:notes:24",
    "explanation": false
  },
  {
    "id": "across_documents_remaining_performance_obligations_against_record_backlog",
    "what_changed": "Per the change history, only the as-of date changed. The prior text gave $9.5 billion of remaining performance obligations, $4.1 billion within twelve months, as of April 4, 2026. The current text gives $9.5 billion and $4.1 billion as of July 4, 2026. The same-day release reports record Q2 backlog of $15.6 billion, with Software and Services backlog 'up $1.2 billion' (8k_2_02:12, :27). The note says remaining performance obligations equal backlog except where Software and Services contracts can be terminated for convenience. Reconciling the two is for the numbers reader.",
    "account": "Remaining performance obligations / backlog",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The transaction value associated with remaining performance obligations which were not yet satisfied as of July 4, 2026 was $9.5 billion, of which $4.1 billion is expected to be recognized in the next twelve months.",
    "paragraph_id": "0000068505-26-000028:notes:31",
    "explanation": false
  },
  {
    "id": "revenue_recognition_cumulative_catch_up_reversal_system_contracts",
    "what_changed": "This recurring sentence now says $1 million of revenue was reversed in the quarter for performance obligations satisfied in earlier periods, 'primarily driven by changes in the estimates of progress on system contracts'. The prior quarter's text said $2 million was recognized for the three months ended April 4, 2026. The six-month text says $1 million was recognized. The paragraph also adds three-month and six-month figures for revenue recognized from contract liabilities ($796 million and $1.2 billion).",
    "account": "Net sales (cumulative catch-up on system contracts)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Revenue of $1 million was reversed during the three months ended July 4, 2026 related to performance obligations satisfied, or partially satisfied, in previous periods",
    "paragraph_id": "0000068505-26-000028:notes:35",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_contract_cost_amortization_range_changed",
    "what_changed": "The amortization range for incremental costs to obtain a contract (sales-incentive portfolio approach) now reads 'one to seven years'. The prior text read 'one to eight years'. No reason is given. Read as a change in the amortization-period estimate, the top of the range is now seven years where it was eight, which points to faster amortization. Amortization of contract cost assets is now given as $13 million for the quarter and $27 million for six months. The prior text gave $14 million for the three months ended April 4, 2026.",
    "account": "Contract cost assets / amortization of contract cost assets",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "with amortization ranging from one to seven years to approximate the recognition of revenues over time",
    "paragraph_id": "0000068505-26-000028:notes:39",
    "explanation": false
  },
  {
    "id": "earnings_quality_silvus_earnout_charge_excluded_from_non_gaap",
    "what_changed": "The paragraph gives a $91 million six-month charge to raise the fair value of the Silvus contingent earnout. The input marks it as changed but does not carry the prior wording. The release lists 'Contingent earnout adjustment' among its non-GAAP adjustments (8k_2_02:132, :145) and names 'adjustments to contingent earnout' among the highlighted items excluded from non-GAAP (8k_2_02:65). This non-cash charge therefore sits in GAAP Other charges but is left out of non-GAAP operating earnings and EPS.",
    "account": "Other charges",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "During the six months ended July 4, 2026, the Company recorded a charge of $91 million to increase the fair value of the contingent earnout consideration related to the Silvus acquisition.",
    "paragraph_id": "0000068505-26-000028:notes:55",
    "explanation": false
  },
  {
    "id": "results_against_expectations_silvus_earnout_targets_and_share_settlement",
    "what_changed": "The EPS note restates the Silvus earnout. Up to $600 million is payable in shares: up to $150 million for July 5, 2026 to July 3, 2027, and up to $450 million for July 4, 2027 to July 1, 2028, with a catch-up. The fair value is now given as $127 million as of July 4, 2026. The first measurement year begins the day after this quarter ends. notes:146 says the fair value was raised because of 'updated expectations regarding the achievement' of the financial targets, so the prose signals that management now expects Silvus to meet its targets to a greater degree. The settlement shares would enter diluted EPS only when targets are achieved.",
    "account": "Diluted weighted average common shares",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "The shares required to settle the contingent earnout consideration will only be reflected within diluted earnings per share when and if the earnout financial targets have been achieved, in each of the two respective periods.",
    "paragraph_id": "0000068505-26-000028:notes:65",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_brinc_strategic_investment",
    "what_changed": "The paragraph says that on July 1, 2026, a date inside this quarter, the Company paid $100 million for a strategic equity investment in BRINC Drones, Inc., a public safety drone company. It says such investments are carried at cost. Adjustments from observable price changes in orderly transactions are recorded in Other, net, which gives a non-operating gain or loss route. The investments table shows a Strategic investments balance at July 4, 2026, which is for the numbers reader. No relationship other than investor is described.",
    "account": "Investments",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "On July 1, 2026, the Company paid $100 million for a strategic investment in equity securities of BRINC Drones, Inc.",
    "paragraph_id": "0000068505-26-000028:notes:83",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_term_loan_partial_maturity_extension",
    "what_changed": "A sentence was added. On June 26, 2026 the Company used its option under the 364-Day Term Loan Credit Agreement to extend the maturity of $250 million of the outstanding principal by one year. Other changes are wording only ('facility' instead of 'term loan'), the covenant-compliance date, and the quarter's weighted average rates: 4.73% and 4.85%, where the prior text gave 4.77% and 4.99%. The paragraph does not give the new maturity date or say what happens to the principal that was not extended. MD&A repeats the paragraph (mdna:194). The debt table still shows the '364 day term loan' as one line. How the extended portion is split between current and long-term is for the numbers reader.",
    "account": "Current portion of long-term debt (Short-term borrowings)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "On June 26, 2026, the Company exercised its option under the 364-Day Term Loan Credit Agreement to extend the maturity of $250 million of the outstanding principal amount by one year.",
    "paragraph_id": "0000068505-26-000028:notes:105",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_commercial_paper_outstanding",
    "what_changed": "The commercial paper sentence now says $65 million was outstanding at July 4, 2026, at a 4.03% weighted-average rate for the quarter. The prior text said there was no outstanding debt under the program at April 4, 2026. The debt table adds a 'Commercial papers' line. MD&A's financing discussion (mdna:184) cites short-term borrowings 'including commercial paper'.",
    "account": "Short-term borrowings",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "As of July 4, 2026, the Company had $65 million outstanding debt under the commercial paper program, which had a weighted-average interest rate of 4.03% during the three months ended July 4, 2026.",
    "paragraph_id": "0000068505-26-000028:notes:106",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_treasury_rate_lock_forecasted_debt",
    "what_changed": "The input carries a 'Treasury Rate Lock' heading (notes:124) and paragraph as changed. The prose says that during the period the Company entered Treasury rate locks to hedge interest rates on forecasted debt transactions. They are designated as cash flow hedges, with a $150 million notional and a de minimis fair value. They settle when the related debt is issued, and gains or losses go to interest expense over the life of the debt. The prose does not name the forecasted debt. Other new items next to it are the D-Fend agreement (notes:11), the commercial paper (notes:106) and the term-loan extension (notes:105).",
    "account": "Long-term debt",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "In order to manage interest rate exposure, during the period ended July 4, 2026, the Company entered into Treasury rate lock agreements to protect against unfavorable interest rate changes relating to forecasted debt transactions.",
    "paragraph_id": "0000068505-26-000028:notes:125",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_unrecognized_tax_benefits_increase",
    "what_changed": "The rate comparison says the quarter's 25% effective tax rate was higher than the prior-year quarter's 24% 'primarily due to a net increase in unrecognized tax benefits'. It says the six-month rate of 22% was lower than 23% because of higher excess tax benefits on share-based compensation and a larger deduction for foreign-derived deduction-eligible income. A net increase in unrecognized tax benefits is a change in a tax reserve estimate. The prose gives no amount and no jurisdiction. MD&A repeats this (mdna:98, :163).",
    "account": "Unrecognized tax benefits (Other liabilities) / Income tax expense",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The effective tax rate for the three months ended July 4, 2026 of 25% was higher than the effective tax rate for the three months ended June 28, 2025 of 24%, primarily due to a net increase in unrecognized tax benefits.",
    "paragraph_id": "0000068505-26-000028:notes:131",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_retirement_plan_match_paid_in_stock",
    "what_changed": "The paragraph says that from January 1, 2026 the 401(k) Plan company match is made in Company common stock. It says 0.03 million and 0.06 million shares (grant-date fair value $13 million and $27 million) were issued for the three and six months. The input does not carry the prior wording, so I cannot confirm whether the stock-settled match was described last quarter. A match paid in shares instead of cash is a non-cash compensation cost and adds to shares outstanding.",
    "account": "Net cash provided by operating activities",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Beginning January 1, 2026, the Company's matching contribution under the 401(k) Plan was made in Company common stock.",
    "paragraph_id": "0000068505-26-000028:notes:140",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_silvus_earnout_fair_value_remeasurement",
    "what_changed": "The fair-value paragraph now puts the Silvus contingent earnout liability at $127 million as of July 4, 2026. It is measured with a Monte Carlo model using Level 3 inputs: projected net sales, gross margin and cash flows. The paragraph gives charges of $16 million for the quarter and $91 million for six months, recorded in Other charges. It says the non-cash charge is due to 'updated expectations regarding the achievement of the previously noted financial targets'. The acquisition-date value is restated as approximately $38 million. This is management's own Level 3 estimate, and it moved this period.",
    "account": "Other liabilities: contingent earnout consideration",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "This non-cash charge is attributable to the Company's updated expectations regarding the achievement of the previously noted financial targets.",
    "paragraph_id": "0000068505-26-000028:notes:146",
    "explanation": false
  },
  {
    "id": "earnings_quality_accounts_receivable_sales_proceeds",
    "what_changed": "The receivable-sales table has an 'Accounts receivable sales proceeds' row, with amounts in the 2026 columns and dashes in the 2025 columns. The servicing sentence (notes:151) refers to 'sales of accounts receivables and long-term receivables'. The table's lead-in (notes:149) and MD&A's lead-in (mdna:188) still describe the table as sales of long-term receivables only. The input does not show whether this row was in the prior quarter's table. Selling current trade receivables reduces Accounts receivable and adds operating cash without a customer collection.",
    "account": "Accounts receivable, net",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Accounts receivable sales proceeds",
    "paragraph_id": "0000068505-26-000028:notes:150",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_customer_financing_commitments",
    "what_changed": "The sentence now gives outstanding commitments to provide long-term financing to third parties of $293 million at July 4, 2026, against $179 million at December 31, 2025. It gives retained servicing obligations of $861 million (December 31, 2025: $814 million). These customer-financing commitments become long-term receivables when funded. MD&A repeats the commitment figure (mdna:206).",
    "account": "Long-term receivables (Other assets)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "The Company had outstanding commitments to provide long-term financing to third parties totaling $293 million at July 4, 2026, compared to $179 million at December 31, 2025.",
    "paragraph_id": "0000068505-26-000028:notes:151",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_hytera_payments_withholding_sentence_removed",
    "what_changed": "Payments against the civil award are now given as '$232 million', '$60 million of which was paid in the first half of 2026'. The prior text said 'over $212 million', with '$40 million' paid in the first quarter. This sentence was removed: 'Net of withholding taxes, the Company had received over $192 million as of April 4, 2026, $36 million of which was received in the first quarter of 2026.' The note therefore no longer separates the amount Hytera paid from the cash received after withholding. Payments are still said to be recorded as a gain within Other charges, and notes:56 gives six-month Hytera gains of $60 million. The release carries the same text (8k_2_02:67).",
    "account": "Gain on Hytera litigation (within Other charges)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Hytera had paid $232 million against this award, $60 million of which was paid in the first half of 2026.",
    "paragraph_id": "0000068505-26-000028:notes:155",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_hytera_royalty_appeal_scope",
    "what_changed": "The closing sentence now says the parts of the proceedings 'related to the H-Series are subject to appeal'. The prior text said 'related to both the I-Series and H-Series'. The H-Series royalties Hytera has reported are now 'approximately $116 million' reported 'to the Company'. The prior text said approximately $110 million. Neither amount is described as recognized, and any gain depends on collection. The release carries the same text (8k_2_02:68, :70).",
    "account": "Gain on Hytera litigation (within Other charges)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "While several aspects of the court proceedings related to the H-Series are subject to appeal, the Company continues to seek collection of the amounts owed by Hytera through the ongoing legal process.",
    "paragraph_id": "0000068505-26-000028:notes:156",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_hytera_court_ordered_annual_payment",
    "what_changed": "The criminal-matter paragraph says that at the March 5, 2026 sentencing, as a condition of probation, the District Court ordered Hytera to pay the Company $100 million in 2026 toward the civil judgment, and $100 million in each later year until the judgment is paid in full. It also fined Hytera $50 million, payable after the civil judgment. The Company has appealed the sentencing order. The input does not carry the prior wording, so it does not show which sentence changed. Payments are recognized as gains when received (notes:155). The prose implies further Hytera gains during 2026 if Hytera complies.",
    "account": "Gain on Hytera litigation (within Other charges)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "the District Court ordered Hytera to pay the Company $100 million in 2026 towards the civil judgment and $100 million for each succeeding year until the civil judgment is paid in full.",
    "paragraph_id": "0000068505-26-000028:notes:158",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_restructuring_accrual_reversals_and_headcount",
    "what_changed": "The accrual roll-forward text now gives: 2026 additional charges of $33 million for severance of approximately 500 employees; a $3 million adjustment for 'reversals for accruals no longer needed'; $24 million used; and a remaining $30 million accrual in Accrued liabilities, expected to be paid mostly within one year to approximately 655 employees. The quarter's text (notes:167) also shows a $3 million reversal inside the quarter's net charge. Management explains the reserve in terms of headcount and reversals.",
    "account": "Accrued liabilities (reorganization of business accrual)",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "The 2026 additional charges of $33 million represent severance costs for approximately 500 employees. The adjustment of $3 million reflects reversals for accruals no longer needed.",
    "paragraph_id": "0000068505-26-000028:notes:174",
    "explanation": true
  },
  {
    "id": "across_documents_contingent_earnout_classification_wording",
    "what_changed": "The Silvus paragraph says changes in the earnout's fair value 'will be recorded as a component of operating income within Other income, net'. The fair-value note (notes:146) says the charges were 'recorded within Other Charges'. The Other charges table (notes:54) lists 'Contingent earnout adjustment', and the release's reconciliation puts it under 'Other charges (income)'. The input does not show whether the 'Other income, net' wording is new. The two descriptions name different line items.",
    "account": "Other charges",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Changes to the fair value of the contingent earnout consideration will be recorded as a component of operating income within Other income, net in the Company's Consolidated Statement of Operations.",
    "paragraph_id": "0000068505-26-000028:notes:181",
    "explanation": false
  },
  {
    "id": "articulation_and_the_filed_history_silvus_goodwill_measurement_period_adjustment",
    "what_changed": "The paragraph says the Silvus business 'is part of both the Products and Systems Integration segment and the Software and Services segment'. It says that between the acquisition date and July 4, 2026 the Company recorded 'a net reduction of $12 million in goodwill and an increase primarily to intangible assets' from measurement-period adjustments, and that purchase accounting is not complete. notes:182 still says the goodwill was 'allocated primarily to the Products and Systems Integration segment'. The prior wording is not in the input. The goodwill roll-forward (notes:199) has a 'Purchase accounting adjustments' row by segment for January 1 to July 4, 2026. Matching the prose's 'net reduction' against that row, for both direction and period, is for the numbers reader.",
    "account": "Goodwill",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Between the acquisition date and July 4, 2026, the Company recorded a net reduction of $12 million in goodwill and an increase primarily to intangible assets related to purchase accounting adjustments during the measurement period.",
    "paragraph_id": "0000068505-26-000028:notes:184",
    "explanation": false
  },
  {
    "id": "earnings_quality_ieepa_tariff_refund_in_cost_of_sales",
    "what_changed": "The input carries this paragraph as changed. It now says that after the February 20, 2026 Supreme Court ruling that struck down IEEPA tariffs, and the April 20, 2026 launch of the CBP refund-claim system, the Company recognized a favorable $60 million adjustment within Cost of sales in the quarter ended July 4, 2026. The release puts the benefit at 190 basis points of operating margin (8k_2_02:23) and $0.25 per share (8k_2_02:19). This is a one-time recovery of tariffs already paid, recorded in an operating cost line.",
    "account": "Cost of sales",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Accordingly, during the quarter ended July 4, 2026, we recognized a favorable adjustment of $60 million recorded within Cost of sales in our Condensed Consolidated Statements of Operations.",
    "paragraph_id": "0000068505-26-000028:mdna:20",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_ieepa_refund_recognized_as_probable",
    "what_changed": "The same paragraph gives the basis for recognition: management 'determined that the recovery of a portion of these refunds is now probable'. Only a portion is recognized. The paragraph does not give the total claimed, the part not recognized, or the balance-sheet line that holds the refund receivable. The judgment that recovery is probable is what triggered the $60 million, and management attributes the recognition to the CBP system going live.",
    "account": "Other current assets (IEEPA refund receivable; line not stated)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Following the implementation of this system, we have determined that the recovery of a portion of these refunds is now probable.",
    "paragraph_id": "0000068505-26-000028:mdna:20",
    "explanation": true
  },
  {
    "id": "narrative_signs_of_operating_pressure_memory_cost_inflation",
    "what_changed": "The paragraph says the Company is 'experiencing higher costs for memory in our products' because of AI-driven market demand, and that 'the current environment has led to increased costs on materials and components'. MD&A's gross margin text now cites 'higher direct material costs' as an offset in Products and Systems Integration (mdna:60, :127). The input marks this paragraph as changed but does not carry its prior wording. The release carries it word for word (8k_2_02:53).",
    "account": "Costs of products sales",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "In addition, we are experiencing higher costs for memory in our products which is a result of substantial demand in the market driven by AI.",
    "paragraph_id": "0000068505-26-000028:mdna:21",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_inventory_held_elevated",
    "what_changed": "The paragraph says the Company is actively managing inventory against volatility in memory costs, tariffs and import/export rules, 'to ensure supply continues at levels necessary to meet our current customer demand'. It adds: 'We expect inventory levels to remain elevated'. This is management's stated cause for the inventory level. MD&A's cash flow text (mdna:178) and the release (8k_2_02:25) both cite higher investment in inventory as a drag on operating cash flow.",
    "account": "Inventories, net",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "We expect inventory levels to remain elevated as we mitigate this dynamic supply chain environment.",
    "paragraph_id": "0000068505-26-000028:mdna:21",
    "explanation": true
  },
  {
    "id": "earnings_quality_products_gross_margin_includes_tariff_refund",
    "what_changed": "The quarter's driver sentence for Products and Systems Integration gross margin now names 'IEEPA tariff refunds' as a driver of the 3.0% increase, alongside higher sales and favorable mix, 'partially offset by higher direct material costs'. Management thus attributes part of the segment's margin increase to a one-time refund.",
    "account": "Gross margin: Products and Systems Integration",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "primarily driven by higher sales, including favorable mix, and IEEPA tariff refunds partially offset by higher direct material costs",
    "paragraph_id": "0000068505-26-000028:mdna:60",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_north_america_products_flat_half_year",
    "what_changed": "New six-month discussion. Products and Systems Integration net sales growth for the first half is described as 'driven by an increase of 35% in the International region, while the North America region remained flat'. The segment's six-month increase is stated as including $392 million of revenue from acquisitions (mdna:106).",
    "account": "Net sales: Products and Systems Integration, North America",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The $269 million, or 8%, increase in net sales within the Products and Systems Integration segment was driven by an increase of 35% in the International region, while the North America region remained flat.",
    "paragraph_id": "0000068505-26-000028:mdna:104",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_north_america_mission_critical_products_offset",
    "what_changed": "Six-month MCN growth in Products and Systems Integration, including revenue from acquisitions, is described as 'driven by the International region partially offset by the North America region'. In other words, the prose says North America MCN product sales moved against the half's growth.",
    "account": "Net sales: MCN, Products and Systems Integration, North America",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "driven by the International region partially offset by the North America region",
    "paragraph_id": "0000068505-26-000028:mdna:113",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_products_margin_flat_despite_refund",
    "what_changed": "Six-month text: Products and Systems Integration gross margin as a percentage of sales 'remained flat', with higher sales and IEEPA tariff refunds 'offset by higher direct material costs'. Read with mdna:21, which says material and component cost increases are continuing, the prose implies pressure on segment margin once the refund does not repeat.",
    "account": "Gross margin percentage: Products and Systems Integration",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "gross margin as a percentage of net sales in the Products and Systems Integration segment remained flat, inclusive of acquisitions, primarily driven by higher sales and IEEPA tariff refunds, offset by higher direct material costs.",
    "paragraph_id": "0000068505-26-000028:mdna:127",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_products_segment_half_year_earnings_decrease",
    "what_changed": "Six-month text: Products and Systems Integration operating earnings fell by $49 million. The prose gives the drivers as higher intangible amortization, the Silvus contingent earnout charge, expenses of acquired businesses and higher direct material costs. These are partly offset by higher sales, IEEPA refunds, operating leverage, the Hytera gain and lower legal expenses.",
    "account": "Operating earnings: Products and Systems Integration",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "a $49 million decrease in the Products and Systems Integration segment, primarily driven by an increase in intangible amortization expense, a contingent earnout charge related to the Silvus acquisition, higher expenses associated with acquired businesses, and higher direct material costs",
    "paragraph_id": "0000068505-26-000028:mdna:151",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_operating_cash_flow_inventory_and_interest_offsets",
    "what_changed": "The six-month operating cash flow increase is attributed to higher earnings net of non-cash charges, 'partially offset by increased investments in inventory and higher interest payments'. Higher interest payments are named as an offset, alongside the term loans and notes that funded Silvus (notes:104, :105). The quarter's release explanation differs: it names lower tax payments and does not mention interest (8k_2_02:25).",
    "account": "Interest paid (operating cash flow)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "partially offset by increased investments in inventory and higher interest payments in the first half of 2026 compared to the first half of 2025.",
    "paragraph_id": "0000068505-26-000028:mdna:178",
    "explanation": false
  },
  {
    "id": "across_documents_non_gaap_measures_keep_ieepa_refund",
    "what_changed": "Release footnote 2 says GAAP and non-GAAP operating earnings and EPS both include the IEEPA refund benefit. The refund is not among the non-GAAP adjustments in the reconciliation (8k_2_02:132). Hytera gains (8k_2_02:71) and the contingent earnout adjustment are excluded as highlighted items. Non-GAAP EPS of $4.41, and the raised outlook (8k_2_02:46), therefore include a one-time refund. The release does not say whether the outlook assumes further refunds.",
    "account": "Non-GAAP operating earnings and EPS",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Inclusive of a $60M (pre-tax) benefit, or $0.25 per share",
    "paragraph_id": "0000068505-26-000027:8k_2_02:19",
    "explanation": false
  },
  {
    "id": "results_against_expectations_acquired_revenue_in_reported_growth",
    "what_changed": "The release says the quarter's revenue included $243 million from acquisitions and a $35 million foreign currency tailwind. The organic revenue reconciliation (8k_2_02:157) gives organic growth of 5% for the quarter and 2% for six months, beside reported growth of 13% and 10%. The 10-Q MD&A splits acquisition revenue into $210 million in Products and Systems Integration and $33 million in Software and Services (mdna:39, :40).",
    "account": "Net sales",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Revenue from acquisitions was $243 million and foreign currency tailwinds were $35 million in the quarter.",
    "paragraph_id": "0000068505-26-000027:8k_2_02:22",
    "explanation": false
  },
  {
    "id": "across_documents_tax_rate_explanations_gaap_and_non_gaap",
    "what_changed": "The release explains the lower non-GAAP effective tax rate (22.6% versus 23.5%) by 'a higher deduction for income generated from export sales'. The 10-Q explains the higher GAAP quarterly rate (25% versus 24%) by 'a net increase in unrecognized tax benefits' (notes:131). The non-GAAP reconciliation includes an 'Assessments of uncertain tax positions' line, and the highlighted-items definition excludes 'income tax effects of significant tax matters'. The release does not say whether the increase in unrecognized tax benefits is treated as a highlighted item.",
    "account": "Income tax expense",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The decrease in the non-GAAP effective tax rate was primarily driven by a higher deduction for income generated from export sales recognized in the current quarter.",
    "paragraph_id": "0000068505-26-000027:8k_2_02:24",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_quarterly_cash_flow_lower_tax_payments",
    "what_changed": "The release attributes the quarter's higher operating and free cash flow to higher earnings net of non-cash charges 'and lower tax payments', partly offset by higher inventory investment. The 10-Q's six-month cash flow explanation (mdna:178) does not mention tax payments. The prose does not say whether the lower tax payments are a timing effect.",
    "account": "Net cash provided by operating activities",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Both the operating cash flow and free cash flow for the quarter increased primarily due to higher earnings, net of non-cash charges and lower tax payments, partially offset by higher investments in inventory.",
    "paragraph_id": "0000068505-26-000027:8k_2_02:25",
    "explanation": false
  },
  {
    "id": "results_against_expectations_third_quarter_outlook",
    "what_changed": "The release gives third-quarter 2026 guidance: revenue growth of approximately 8% versus the third quarter of 2025, and non-GAAP EPS of $4.39 to $4.44. It assumes about 168 million diluted shares and a non-GAAP tax rate of about 23%.",
    "account": "Net sales",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "The company expects revenue growth of approximately 8% compared to the third quarter of 2025 and non-GAAP EPS between $4.39 and $4.44 per share.",
    "paragraph_id": "0000068505-26-000027:8k_2_02:45",
    "explanation": false
  },
  {
    "id": "results_against_expectations_full_year_outlook_raised",
    "what_changed": "The release raises full-year 2026 guidance. Revenue is now approximately $12.975 billion (prior guidance $12.8 billion). Non-GAAP EPS is now $17.62 to $17.72 (prior $16.87 to $16.99). It assumes a non-GAAP tax rate of 22% to 22.5% and about 168 million diluted shares. The quarter includes the $60 million IEEPA refund (8k_2_02:19), and the release does not separate its effect on the raised EPS range.",
    "account": "Net sales",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "The company now expects revenue of approximately $12.975 billion, up from its prior guidance of $12.8 billion and non-GAAP EPS between $17.62 and $17.72 per share, up from the prior guidance of between $16.87 and $16.99 per share.",
    "paragraph_id": "0000068505-26-000027:8k_2_02:46",
    "explanation": false
  },
  {
    "id": "across_documents_intangibles_amortization_presentation",
    "what_changed": "The release's statements of operations show 'Other charges' and 'Intangibles amortization' as separate lines (8k_2_02:96, :102). The 10-Q MD&A results table (mdna:25), the segment tables (notes:160, :161) and the Other charges note (notes:54) put intangibles amortization inside 'Other charges'. So the label 'Other charges' covers different content in the two documents for the same quarter. Reconciling the line items is for the numbers reader.",
    "account": "Other charges / Intangibles amortization",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Intangibles amortization",
    "paragraph_id": "0000068505-26-000027:8k_2_02:96",
    "explanation": false
  }
]
```

## Paragraphs carried as text but not made an item

`insufficient` below means the paragraph is marked as changed but the input does not carry its prior wording, and nothing in its content shows a change in substance.

### Notes
- `0000068505-26-000028:notes:1`: date rolled forward (period description).
- `0000068505-26-000028:notes:3`: date rolled forward.
- `0000068505-26-000028:notes:22`: insufficient. Pending ASU 2024-03 is still being evaluated; no estimate or commitment.
- `0000068505-26-000028:notes:23`: heading.
- `0000068505-26-000028:notes:25`: wording only ('Part 1' changed to 'Part I').
- `0000068505-26-000028:notes:27`: date rolled forward (table lead-in).
- `0000068505-26-000028:notes:28`: amounts only (three-month disaggregation table).
- `0000068505-26-000028:notes:29`: amounts only (six-month disaggregation table, present because this is a second-quarter filing).
- `0000068505-26-000028:notes:33`: amounts only (contract balances table).
- `0000068505-26-000028:notes:34`: wording only ('are less than' changed to 'is less than').
- `0000068505-26-000028:notes:36`: date rolled forward.
- `0000068505-26-000028:notes:38`: amounts only (contract cost asset table).
- `0000068505-26-000028:notes:41`: amounts only (lease cost table).
- `0000068505-26-000028:notes:43`: amounts only (lease balance table).
- `0000068505-26-000028:notes:45`: amounts only (lease cash flow table).
- `0000068505-26-000028:notes:46`: date rolled forward (six months).
- `0000068505-26-000028:notes:47`: amounts only (lease term and discount rate).
- `0000068505-26-000028:notes:49`: amounts only (lease maturity table).
- `0000068505-26-000028:notes:54`: amounts only (Other charges table; earnout and Hytera rows itemized elsewhere).
- `0000068505-26-000028:notes:56`: amounts and dates rolled forward (Hytera gains; substance itemized at notes:155).
- `0000068505-26-000028:notes:59`: amounts only (interest and Other, net table).
- `0000068505-26-000028:notes:62`: amounts only (EPS table).
- `0000068505-26-000028:notes:63`: wording only.
- `0000068505-26-000028:notes:64`: amounts only (antidilutive awards).
- `0000068505-26-000028:notes:69`: amounts only (receivables and allowance table).
- `0000068505-26-000028:notes:72`: amounts only (inventory and reserves table; cause itemized at mdna:21).
- `0000068505-26-000028:notes:75`: amounts only (other current assets table).
- `0000068505-26-000028:notes:78`: amounts only (property table).
- `0000068505-26-000028:notes:79`: amounts only (depreciation).
- `0000068505-26-000028:notes:82`: amounts only (investments table; BRINC itemized at notes:83).
- `0000068505-26-000028:notes:86`: amounts only (other assets table).
- `0000068505-26-000028:notes:89`: amounts only (supplier finance program outstanding).
- `0000068505-26-000028:notes:92`: amounts only (accrued liabilities table).
- `0000068505-26-000028:notes:95`: amounts only (other liabilities table; earnout and tax rows itemized elsewhere).
- `0000068505-26-000028:notes:97`: amounts only (repurchases).
- `0000068505-26-000028:notes:98`: amounts and date rolled forward (dividends, including the recurring post-quarter payment).
- `0000068505-26-000028:notes:100`: date rolled forward.
- `0000068505-26-000028:notes:101`: amounts only (AOCI table).
- `0000068505-26-000028:notes:102`: heading.
- `0000068505-26-000028:notes:103`: amounts only (debt table; new Commercial papers row itemized at notes:106).
- `0000068505-26-000028:notes:104`: insufficient. Restates the June 2025 note issuance; no new amount.
- `0000068505-26-000028:notes:108`: amounts only (FX notional).
- `0000068505-26-000028:notes:109`: date rolled forward.
- `0000068505-26-000028:notes:110`: amounts only (FX positions table).
- `0000068505-26-000028:notes:112`: amounts and date rolled forward (counterparty exposure).
- `0000068505-26-000028:notes:114`: date rolled forward.
- `0000068505-26-000028:notes:115`: amounts only (derivative fair values).
- `0000068505-26-000028:notes:117`: date rolled forward.
- `0000068505-26-000028:notes:118`: amounts only (derivative effects table).
- `0000068505-26-000028:notes:120`: amounts and date rolled forward (net investment hedges).
- `0000068505-26-000028:notes:123`: amounts and date rolled forward (equity swap notional).
- `0000068505-26-000028:notes:124`: heading (content itemized at notes:125).
- `0000068505-26-000028:notes:128`: amounts only (effective tax rate table).
- `0000068505-26-000028:notes:129`: insufficient. Recurring statutory-rate reconciliation; no new cause named.
- `0000068505-26-000028:notes:130`: prior-year comparative period rolled forward.
- `0000068505-26-000028:notes:132`: date rolled forward (OBBBA impact still not material).
- `0000068505-26-000028:notes:135`: amounts only (pension three-month table).
- `0000068505-26-000028:notes:136`: amounts only (pension six-month table).
- `0000068505-26-000028:notes:138`: amounts only (share-based compensation table).
- `0000068505-26-000028:notes:139`: amounts and dates rolled forward (six-month grants).
- `0000068505-26-000028:notes:141`: heading and date rolled forward.
- `0000068505-26-000028:notes:142`: amounts only (fair value hierarchy table).
- `0000068505-26-000028:notes:144`: amounts only (money market funds).
- `0000068505-26-000028:notes:145`: amounts only (debt fair value).
- `0000068505-26-000028:notes:149`: date rolled forward (table lead-in; lead-in wording noted in the notes:150 item).
- `0000068505-26-000028:notes:152`: heading.
- `0000068505-26-000028:notes:153`: heading.
- `0000068505-26-000028:notes:154`: wording only ('for Northern District' changed to 'for the Northern District').
- `0000068505-26-000028:notes:157`: heading.
- `0000068505-26-000028:notes:160`: amounts only (segment three-month table).
- `0000068505-26-000028:notes:161`: amounts only (segment six-month table).
- `0000068505-26-000028:notes:163`: amounts only (capital expenditure by segment).
- `0000068505-26-000028:notes:165`: amounts only (depreciation by segment).
- `0000068505-26-000028:notes:167`: amounts only (quarter reorganization charges; reversal itemized at notes:174).
- `0000068505-26-000028:notes:168`: amounts only (six-month reorganization charges).
- `0000068505-26-000028:notes:170`: amounts only (reorganization by segment).
- `0000068505-26-000028:notes:172`: amounts only (accrual roll-forward table).
- `0000068505-26-000028:notes:176`: prior-year comparative period rolled forward.
- `0000068505-26-000028:notes:177`: prior-year comparative period rolled forward.
- `0000068505-26-000028:notes:178`: amounts only (prior-year reorganization by segment).
- `0000068505-26-000028:notes:182`: insufficient. Silvus allocation amounts; measurement-period change itemized at notes:184.
- `0000068505-26-000028:notes:183`: insufficient. Silvus intangible amounts and lives; no change stated.
- `0000068505-26-000028:notes:186`: insufficient. Description of the Hyper acquisition (March 2026); purchase accounting still open.
- `0000068505-26-000028:notes:187`: insufficient. Description of the Exacom acquisition (March 2026); purchase accounting still open.
- `0000068505-26-000028:notes:189`: insufficient. Theatro purchase accounting is said to be complete as of the first quarter of 2026, a period the prior filing covered; no amount change visible.
- `0000068505-26-000028:notes:190`: insufficient. RapidDeploy purchase accounting is said to be complete as of the first quarter of 2026; no amount change visible.
- `0000068505-26-000028:notes:193`: amounts only (intangibles table).
- `0000068505-26-000028:notes:194`: amounts only (amortization expense and the recurring forward schedule; Silvus explanation is recurring).
- `0000068505-26-000028:notes:196`: amounts only (intangibles by segment).
- `0000068505-26-000028:notes:198`: date rolled forward.
- `0000068505-26-000028:notes:199`: amounts only (goodwill roll-forward; referenced in the notes:184 item).

### MD&A
- `0000068505-26-000028:mdna:2`: date rolled forward.
- `0000068505-26-000028:mdna:11`: heading.
- `0000068505-26-000028:mdna:12`: amounts only.
- `0000068505-26-000028:mdna:13`: amounts only.
- `0000068505-26-000028:mdna:14`: amounts only.
- `0000068505-26-000028:mdna:15`: amounts only.
- `0000068505-26-000028:mdna:16`: amounts only.
- `0000068505-26-000028:mdna:19`: insufficient. General trade-environment sentence with no amount or commitment; the release carries it word for word (8k_2_02:50).
- `0000068505-26-000028:mdna:25`: amounts only (results table; presentation difference itemized at 8k_2_02:96).
- `0000068505-26-000028:mdna:27`: page number.
- `0000068505-26-000028:mdna:28`: heading, date rolled forward.
- `0000068505-26-000028:mdna:29`: date rolled forward (seasonality statement).
- `0000068505-26-000028:mdna:35`: amounts only (segment table).
- `0000068505-26-000028:mdna:37`: amounts only (segment mix).
- `0000068505-26-000028:mdna:38`: amounts only (quarter growth by region).
- `0000068505-26-000028:mdna:39`: amounts only (acquisition revenue; cited in the 8k_2_02:22 item).
- `0000068505-26-000028:mdna:40`: amounts only (acquisition revenue; cited in the 8k_2_02:22 item).
- `0000068505-26-000028:mdna:41`: amounts only (currency).
- `0000068505-26-000028:mdna:43`: amounts only (international region).
- `0000068505-26-000028:mdna:44`: amounts only (North America region).
- `0000068505-26-000028:mdna:45`: page number.
- `0000068505-26-000028:mdna:47`: amounts only.
- `0000068505-26-000028:mdna:48`: amounts only.
- `0000068505-26-000028:mdna:49`: amounts only.
- `0000068505-26-000028:mdna:50`: amounts only.
- `0000068505-26-000028:mdna:52`: amounts only.
- `0000068505-26-000028:mdna:53`: amounts only.
- `0000068505-26-000028:mdna:54`: amounts only.
- `0000068505-26-000028:mdna:55`: amounts only.
- `0000068505-26-000028:mdna:56`: amounts only.
- `0000068505-26-000028:mdna:58`: amounts only (gross margin table).
- `0000068505-26-000028:mdna:59`: amounts only.
- `0000068505-26-000028:mdna:61`: recurring driver (higher sales, favorable mix), amounts updated.
- `0000068505-26-000028:mdna:63`: amounts only (SG&A table).
- `0000068505-26-000028:mdna:64`: amounts only.
- `0000068505-26-000028:mdna:65`: recurring drivers (acquired businesses, incentive costs, lower Hytera legal costs), amounts updated.
- `0000068505-26-000028:mdna:66`: recurring drivers, amounts updated.
- `0000068505-26-000028:mdna:67`: amounts only.
- `0000068505-26-000028:mdna:70`: amounts only (R&D table).
- `0000068505-26-000028:mdna:71`: amounts only.
- `0000068505-26-000028:mdna:72`: recurring drivers, amounts updated.
- `0000068505-26-000028:mdna:73`: recurring drivers, amounts updated.
- `0000068505-26-000028:mdna:74`: amounts only.
- `0000068505-26-000028:mdna:76`: amounts only (Other charges table).
- `0000068505-26-000028:mdna:77`: amounts only.
- `0000068505-26-000028:mdna:78`: amounts only (intangible amortization).
- `0000068505-26-000028:mdna:79`: amounts only (earnout charge itemized at notes:55 and notes:146).
- `0000068505-26-000028:mdna:80`: amounts only (Hytera gain itemized at notes:155).
- `0000068505-26-000028:mdna:82`: amounts only (operating earnings table).
- `0000068505-26-000028:mdna:83`: amounts only.
- `0000068505-26-000028:mdna:84`: drivers repeat items itemized elsewhere (IEEPA, Hytera, earnout, direct material costs).
- `0000068505-26-000028:mdna:85`: recurring drivers, amounts updated.
- `0000068505-26-000028:mdna:87`: amounts only (interest table).
- `0000068505-26-000028:mdna:88`: recurring driver (higher outstanding debt), amounts updated.
- `0000068505-26-000028:mdna:90`: amounts only (Other, net table).
- `0000068505-26-000028:mdna:91`: amounts only.
- `0000068505-26-000028:mdna:92`: amounts only (derivatives).
- `0000068505-26-000028:mdna:93`: amounts only (equity investment fair value).
- `0000068505-26-000028:mdna:94`: amounts only (pension benefit).
- `0000068505-26-000028:mdna:95`: amounts only (foreign currency).
- `0000068505-26-000028:mdna:97`: amounts only (tax table).
- `0000068505-26-000028:mdna:98`: duplicate of notes:131 (itemized).
- `0000068505-26-000028:mdna:99`: date rolled forward (OBBBA).
- `0000068505-26-000028:mdna:100`: heading.
- `0000068505-26-000028:mdna:101`: amounts only (six-month segment table).
- `0000068505-26-000028:mdna:102`: heading.
- `0000068505-26-000028:mdna:103`: amounts only (six-month segment mix).
- `0000068505-26-000028:mdna:105`: amounts only.
- `0000068505-26-000028:mdna:106`: amounts only (acquisition revenue; cited in the mdna:104 item).
- `0000068505-26-000028:mdna:107`: amounts only (currency).
- `0000068505-26-000028:mdna:108`: heading.
- `0000068505-26-000028:mdna:109`: amounts only.
- `0000068505-26-000028:mdna:110`: amounts only.
- `0000068505-26-000028:mdna:111`: heading.
- `0000068505-26-000028:mdna:112`: amounts only.
- `0000068505-26-000028:mdna:114`: amounts only (Video).
- `0000068505-26-000028:mdna:115`: amounts only (currency).
- `0000068505-26-000028:mdna:116`: page number.
- `0000068505-26-000028:mdna:117`: heading.
- `0000068505-26-000028:mdna:118`: amounts only.
- `0000068505-26-000028:mdna:119`: amounts only.
- `0000068505-26-000028:mdna:120`: amounts only.
- `0000068505-26-000028:mdna:121`: amounts only.
- `0000068505-26-000028:mdna:122`: amounts only.
- `0000068505-26-000028:mdna:123`: heading.
- `0000068505-26-000028:mdna:124`: amounts only (six-month gross margin table).
- `0000068505-26-000028:mdna:125`: amounts only.
- `0000068505-26-000028:mdna:126`: recurring driver (higher sales, favorable mix).
- `0000068505-26-000028:mdna:128`: heading.
- `0000068505-26-000028:mdna:129`: amounts only (six-month SG&A table).
- `0000068505-26-000028:mdna:130`: amounts only.
- `0000068505-26-000028:mdna:131`: recurring drivers.
- `0000068505-26-000028:mdna:132`: recurring drivers.
- `0000068505-26-000028:mdna:133`: amounts only.
- `0000068505-26-000028:mdna:134`: heading.
- `0000068505-26-000028:mdna:135`: amounts only (six-month R&D table).
- `0000068505-26-000028:mdna:136`: amounts only.
- `0000068505-26-000028:mdna:137`: recurring drivers.
- `0000068505-26-000028:mdna:138`: recurring drivers.
- `0000068505-26-000028:mdna:139`: amounts only.
- `0000068505-26-000028:mdna:140`: page number.
- `0000068505-26-000028:mdna:141`: heading.
- `0000068505-26-000028:mdna:142`: amounts only (six-month Other charges table).
- `0000068505-26-000028:mdna:143`: amounts only.
- `0000068505-26-000028:mdna:144`: amounts only (amortization).
- `0000068505-26-000028:mdna:145`: amounts only (earnout itemized at notes:55 and notes:146).
- `0000068505-26-000028:mdna:146`: amounts only (Hytera itemized at notes:155).
- `0000068505-26-000028:mdna:147`: heading.
- `0000068505-26-000028:mdna:148`: amounts only.
- `0000068505-26-000028:mdna:149`: amounts only.
- `0000068505-26-000028:mdna:150`: recurring drivers.
- `0000068505-26-000028:mdna:152`: heading.
- `0000068505-26-000028:mdna:153`: amounts only.
- `0000068505-26-000028:mdna:154`: recurring driver (higher outstanding debt).
- `0000068505-26-000028:mdna:155`: heading.
- `0000068505-26-000028:mdna:156`: amounts only.
- `0000068505-26-000028:mdna:157`: amounts only.
- `0000068505-26-000028:mdna:158`: amounts only.
- `0000068505-26-000028:mdna:159`: amounts only.
- `0000068505-26-000028:mdna:160`: amounts only.
- `0000068505-26-000028:mdna:161`: heading.
- `0000068505-26-000028:mdna:162`: amounts only.
- `0000068505-26-000028:mdna:163`: duplicate of notes:131 (itemized).
- `0000068505-26-000028:mdna:164`: date rolled forward (OBBBA).
- `0000068505-26-000028:mdna:166`: duplicate of notes:167 (amounts).
- `0000068505-26-000028:mdna:167`: duplicate of notes:168 (amounts).
- `0000068505-26-000028:mdna:168`: prior-year comparative period rolled forward.
- `0000068505-26-000028:mdna:169`: prior-year comparative period rolled forward.
- `0000068505-26-000028:mdna:171`: amounts only.
- `0000068505-26-000028:mdna:172`: amounts only (repeats notes:174, itemized).
- `0000068505-26-000028:mdna:174`: amounts only (cash flow table).
- `0000068505-26-000028:mdna:176`: amounts only (cash by geography).
- `0000068505-26-000028:mdna:180`: amounts only (investing).
- `0000068505-26-000028:mdna:182`: lead-in sentence.
- `0000068505-26-000028:mdna:183`: amounts only (the 2025 issuance did not recur).
- `0000068505-26-000028:mdna:184`: duplicate of notes:106 (commercial paper, itemized).
- `0000068505-26-000028:mdna:185`: amounts only (repurchases).
- `0000068505-26-000028:mdna:186`: amounts only (short-term debt repayments).
- `0000068505-26-000028:mdna:188`: date rolled forward; lead-in wording noted in the notes:150 item.
- `0000068505-26-000028:mdna:189`: duplicate of notes:150 (itemized).
- `0000068505-26-000028:mdna:191`: amounts only (total and current debt).
- `0000068505-26-000028:mdna:192`: page number.
- `0000068505-26-000028:mdna:193`: insufficient. Restates the June 2025 note issuance.
- `0000068505-26-000028:mdna:194`: duplicate of notes:105 (itemized).
- `0000068505-26-000028:mdna:195`: duplicate of notes:106 (itemized).
- `0000068505-26-000028:mdna:196`: date rolled forward (revolving facility).
- `0000068505-26-000028:mdna:199`: amounts only (repurchases and remaining authority).
- `0000068505-26-000028:mdna:201`: amounts and date rolled forward (dividends).
- `0000068505-26-000028:mdna:206`: duplicate of notes:151 (itemized).
- `0000068505-26-000028:mdna:208`: wording only (cross-reference now names 'Recently Adopted Accounting Pronouncements').
- `0000068505-26-000028:mdna:209`: page number.

### Item 4
- `0000068505-26-000028:item_4_controls:1`: heading.
- `0000068505-26-000028:item_4_controls:2`: insufficient. Standard conclusion that disclosure controls are effective; no change in conclusion visible.
- `0000068505-26-000028:item_4_controls:3`: date rolled forward; no change in internal control reported.
- `0000068505-26-000028:item_4_controls:4`: page number.

### 8-K Item 2.02 release (0000068505-26-000027)
- `0000068505-26-000027:8k_2_02:1`: exhibit file header.
- `0000068505-26-000027:8k_2_02:2`: file header.
- `0000068505-26-000027:8k_2_02:3`: exhibit label.
- `0000068505-26-000027:8k_2_02:4`: headline.
- `0000068505-26-000027:8k_2_02:5`: sub-headline; guidance itemized at 8k_2_02:46.
- `0000068505-26-000027:8k_2_02:6`: amounts only.
- `0000068505-26-000027:8k_2_02:7`: amounts only.
- `0000068505-26-000027:8k_2_02:8`: amounts only.
- `0000068505-26-000027:8k_2_02:9`: amounts only.
- `0000068505-26-000027:8k_2_02:10`: amounts only.
- `0000068505-26-000027:8k_2_02:11`: amounts only.
- `0000068505-26-000027:8k_2_02:12`: amounts only (backlog; cited in the notes:31 item).
- `0000068505-26-000027:8k_2_02:13`: duplicate of notes:11 (itemized).
- `0000068505-26-000027:8k_2_02:14`: dateline.
- `0000068505-26-000027:8k_2_02:15`: executive quote; no amount, estimate or commitment.
- `0000068505-26-000027:8k_2_02:16`: heading.
- `0000068505-26-000027:8k_2_02:17`: amounts only (key results table).
- `0000068505-26-000027:8k_2_02:18`: amounts only (non-GAAP per-share adjustment).
- `0000068505-26-000027:8k_2_02:20`: page number.
- `0000068505-26-000027:8k_2_02:21`: heading.
- `0000068505-26-000027:8k_2_02:23`: the same IEEPA benefit is itemized at 8k_2_02:19 and mdna:20; margin amounts.
- `0000068505-26-000027:8k_2_02:26`: amounts only; D-Fend repeats notes:11.
- `0000068505-26-000027:8k_2_02:27`: amounts only (backlog by segment; cited in the notes:31 item).
- `0000068505-26-000027:8k_2_02:28`: page number.
- `0000068505-26-000027:8k_2_02:29`: heading.
- `0000068505-26-000027:8k_2_02:30`: heading.
- `0000068505-26-000027:8k_2_02:31`: order announcement; no accounting substance.
- `0000068505-26-000027:8k_2_02:32`: order announcement; no accounting substance.
- `0000068505-26-000027:8k_2_02:33`: order announcement; no accounting substance.
- `0000068505-26-000027:8k_2_02:34`: order announcement; no accounting substance.
- `0000068505-26-000027:8k_2_02:35`: order announcement; no accounting substance.
- `0000068505-26-000027:8k_2_02:36`: order announcement; no accounting substance.
- `0000068505-26-000027:8k_2_02:37`: heading.
- `0000068505-26-000027:8k_2_02:38`: order announcement; no accounting substance.
- `0000068505-26-000027:8k_2_02:39`: order announcement; no accounting substance.
- `0000068505-26-000027:8k_2_02:40`: order announcement; no accounting substance.
- `0000068505-26-000027:8k_2_02:41`: order announcement; no accounting substance.
- `0000068505-26-000027:8k_2_02:42`: order announcement; no accounting substance.
- `0000068505-26-000027:8k_2_02:43`: order announcement; no accounting substance.
- `0000068505-26-000027:8k_2_02:44`: heading.
- `0000068505-26-000027:8k_2_02:47`: boilerplate (guidance not reconciled to GAAP).
- `0000068505-26-000027:8k_2_02:48`: heading.
- `0000068505-26-000027:8k_2_02:49`: heading.
- `0000068505-26-000027:8k_2_02:50`: duplicate of mdna:19.
- `0000068505-26-000027:8k_2_02:51`: duplicate of mdna:20 (itemized).
- `0000068505-26-000027:8k_2_02:52`: page number.
- `0000068505-26-000027:8k_2_02:53`: duplicate of mdna:21 (itemized).
- `0000068505-26-000027:8k_2_02:54`: conference call notice.
- `0000068505-26-000027:8k_2_02:55`: heading.
- `0000068505-26-000027:8k_2_02:56`: lead-in.
- `0000068505-26-000027:8k_2_02:57`: amounts only.
- `0000068505-26-000027:8k_2_02:58`: heading.
- `0000068505-26-000027:8k_2_02:59`: boilerplate rationale for non-GAAP measures.
- `0000068505-26-000027:8k_2_02:60`: boilerplate pointer.
- `0000068505-26-000027:8k_2_02:61`: page number.
- `0000068505-26-000027:8k_2_02:62`: boilerplate definition (free cash flow).
- `0000068505-26-000027:8k_2_02:63`: boilerplate definition (organic revenue).
- `0000068505-26-000027:8k_2_02:64`: boilerplate lead-in.
- `0000068505-26-000027:8k_2_02:65`: boilerplate highlighted-items definition (earnout exclusion cited in the notes:55 item).
- `0000068505-26-000027:8k_2_02:66`: duplicate of notes:154.
- `0000068505-26-000027:8k_2_02:67`: duplicate of notes:155 (itemized).
- `0000068505-26-000027:8k_2_02:68`: duplicate of notes:156 (itemized).
- `0000068505-26-000027:8k_2_02:69`: page number.
- `0000068505-26-000027:8k_2_02:70`: duplicate of notes:156 (continuation).
- `0000068505-26-000027:8k_2_02:71`: recurring Hytera non-GAAP policy with amounts updated; it says 'excluded such expenses from its GAAP operating Income' where non-GAAP is plainly meant (wording only).
- `0000068505-26-000027:8k_2_02:72`: boilerplate (share-based compensation exclusion).
- `0000068505-26-000027:8k_2_02:73`: boilerplate (amortization exclusion).
- `0000068505-26-000027:8k_2_02:74`: heading.
- `0000068505-26-000027:8k_2_02:75`: page number.
- `0000068505-26-000027:8k_2_02:76`: boilerplate forward-looking risk list (fragment; no Item 1A diff in input to compare).
- `0000068505-26-000027:8k_2_02:77`: boilerplate (Regulation FD website).
- `0000068505-26-000027:8k_2_02:78`: boilerplate.
- `0000068505-26-000027:8k_2_02:79`: boilerplate.
- `0000068505-26-000027:8k_2_02:80`: contact block.
- `0000068505-26-000027:8k_2_02:81`: contact block.
- `0000068505-26-000027:8k_2_02:82`: contact block.
- `0000068505-26-000027:8k_2_02:83`: contact block.
- `0000068505-26-000027:8k_2_02:84`: contact block.
- `0000068505-26-000027:8k_2_02:85`: contact block.
- `0000068505-26-000027:8k_2_02:86`: contact block.
- `0000068505-26-000027:8k_2_02:87`: contact block.
- `0000068505-26-000027:8k_2_02:88`: contact block.
- `0000068505-26-000027:8k_2_02:89`: contact block.
- `0000068505-26-000027:8k_2_02:90`: trademark notice.
- `0000068505-26-000027:8k_2_02:91`: page number.
- `0000068505-26-000027:8k_2_02:92`: table label.
- `0000068505-26-000027:8k_2_02:93`: heading.
- `0000068505-26-000027:8k_2_02:94`: heading.
- `0000068505-26-000027:8k_2_02:95`: heading.
- `0000068505-26-000027:8k_2_02:97`: page number.
- `0000068505-26-000027:8k_2_02:98`: table label.
- `0000068505-26-000027:8k_2_02:99`: heading.
- `0000068505-26-000027:8k_2_02:100`: heading.
- `0000068505-26-000027:8k_2_02:101`: heading.
- `0000068505-26-000027:8k_2_02:102`: amounts only (six-month statement of operations; presentation noted in the 8k_2_02:96 item).
- `0000068505-26-000027:8k_2_02:103`: page number.
- `0000068505-26-000027:8k_2_02:104`: table label.
- `0000068505-26-000027:8k_2_02:105`: heading.
- `0000068505-26-000027:8k_2_02:106`: heading.
- `0000068505-26-000027:8k_2_02:107`: heading.
- `0000068505-26-000027:8k_2_02:108`: amounts only (balance sheet).
- `0000068505-26-000027:8k_2_02:109`: page number.
- `0000068505-26-000027:8k_2_02:110`: table label.
- `0000068505-26-000027:8k_2_02:111`: heading.
- `0000068505-26-000027:8k_2_02:112`: heading.
- `0000068505-26-000027:8k_2_02:113`: heading.
- `0000068505-26-000027:8k_2_02:114`: amounts only (three-month cash flow).
- `0000068505-26-000027:8k_2_02:115`: page number.
- `0000068505-26-000027:8k_2_02:116`: table label.
- `0000068505-26-000027:8k_2_02:117`: heading.
- `0000068505-26-000027:8k_2_02:118`: heading.
- `0000068505-26-000027:8k_2_02:119`: heading.
- `0000068505-26-000027:8k_2_02:120`: amounts only (six-month cash flow).
- `0000068505-26-000027:8k_2_02:121`: page number.
- `0000068505-26-000027:8k_2_02:122`: table label.
- `0000068505-26-000027:8k_2_02:123`: heading.
- `0000068505-26-000027:8k_2_02:124`: heading.
- `0000068505-26-000027:8k_2_02:125`: heading.
- `0000068505-26-000027:8k_2_02:126`: amounts only (free cash flow).
- `0000068505-26-000027:8k_2_02:127`: page number.
- `0000068505-26-000027:8k_2_02:128`: table label.
- `0000068505-26-000027:8k_2_02:129`: heading.
- `0000068505-26-000027:8k_2_02:130`: heading.
- `0000068505-26-000027:8k_2_02:131`: heading.
- `0000068505-26-000027:8k_2_02:132`: amounts only (non-GAAP net earnings reconciliation; cited in the notes:55 and 8k_2_02:19 items).
- `0000068505-26-000027:8k_2_02:133`: heading.
- `0000068505-26-000027:8k_2_02:134`: heading.
- `0000068505-26-000027:8k_2_02:135`: amounts only (non-GAAP tax rate).
- `0000068505-26-000027:8k_2_02:136`: page number.
- `0000068505-26-000027:8k_2_02:137`: table label.
- `0000068505-26-000027:8k_2_02:138`: heading.
- `0000068505-26-000027:8k_2_02:139`: amounts only (non-GAAP EPS reconciliation).
- `0000068505-26-000027:8k_2_02:140`: page number.
- `0000068505-26-000027:8k_2_02:141`: table label.
- `0000068505-26-000027:8k_2_02:142`: heading.
- `0000068505-26-000027:8k_2_02:143`: heading.
- `0000068505-26-000027:8k_2_02:144`: heading.
- `0000068505-26-000027:8k_2_02:145`: amounts only (three-month operating earnings reconciliation).
- `0000068505-26-000027:8k_2_02:146`: page number.
- `0000068505-26-000027:8k_2_02:147`: table label.
- `0000068505-26-000027:8k_2_02:148`: heading.
- `0000068505-26-000027:8k_2_02:149`: heading.
- `0000068505-26-000027:8k_2_02:150`: heading.
- `0000068505-26-000027:8k_2_02:151`: amounts only (six-month operating earnings reconciliation).
- `0000068505-26-000027:8k_2_02:152`: page number.
- `0000068505-26-000027:8k_2_02:153`: table label.
- `0000068505-26-000027:8k_2_02:154`: heading.
- `0000068505-26-000027:8k_2_02:155`: heading.
- `0000068505-26-000027:8k_2_02:156`: heading.
- `0000068505-26-000027:8k_2_02:157`: amounts only (organic revenue; cited in the 8k_2_02:22 item).
