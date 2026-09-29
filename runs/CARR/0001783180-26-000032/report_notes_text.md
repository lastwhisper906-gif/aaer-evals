<!-- the quote gate removed 2 item(s) from this copy; input_manifest.json lists each with its reason -->
# CARR 10-Q 0001783180-26-000032: notes and text reader

## What I read

**Files read in full:**
- input_notes.md
- input_notes_history.md
- input_mdna.md
- input_controls.md (Item 4)
- input_8k.md (8-K 0001783180-26-000030, item 2.02 release, plus the list of 8-K item codes)
- input_prior_predictions.md

**Inputs that are missing:**
- The input has no Item 1A diff, no Exhibit 21 diff and no Exhibit 10, so I had nothing to read for them.
- It has no auditor's report either. The controls file holds Item 4 only, which is normal for a 10-Q.

**Prior predictions:** None are on record, so no flags are carried forward.

**Out-of-bounds material:** None found. The directory has no trend table, prices, abnormal returns, short interest, other companies' files, prior probabilities or outcome window. The 8-K financial tables are part of the 8-K body, which I am allowed to see.

**Arithmetic:** I did none. Where a paragraph states amounts without saying which way they moved, the item gives the stated figures and sets `expected_direction` to `none`.

## Items

```json
{ "id": "structure_and_disclosure_changes_riello_sale_closed_after_quarter_end",
  "what_changed": "The basis-of-presentation note now adds that the Riello sale was completed on July 1, 2026, after the June 30, 2026 balance-sheet date. The prior 10-Q text (0001783180-26-000026:note_history:10) described Riello only as held for sale. The same completion sentence now also appears in notes:102, mdna:13 and mdna:167, and the release says the exit was completed (8k_2_02:15, 8k_2_02:49). The prose implies the Riello disposal group leaves held-for-sale balances next quarter. No text states a gain or loss on closing.",
  "account": "Assets held for sale; Liabilities held for sale (Riello disposal group)",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "The sale of Riello was completed on July 1, 2026.",
  "paragraph_id": "0001783180-26-000032:notes:4",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_riello_held_for_sale_impairment_charge",
  "what_changed": "The divestitures note now states a $46 million impairment on Riello, recorded in Other income (expense), net in the three months ended June 30, 2026. The same paragraph still gives expected gross proceeds of approximately $430 million, the wording carried from the prior period. The held-for-sale table (notes:105) has a new row, 'Impairment on held for sale assets'. The reconciliations (notes:117, mdna:45, 8k_2_02:105) have a new 'Riello impairment' row outside segment operating profit. Yet the MD&A (mdna:34, mdna:65) says 'our Climate Solutions Europe segment recorded' the impairment. The tax note (notes:94) calls the charge non-deductible. The text gives no reason for the impairment beyond the lower-of-carrying-value-or-fair-value-less-cost-to-sell basis.",
  "account": "Other income (expense), net; Assets held for sale",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "The Company recognized an impairment charge of $46 million recorded in Other income (expense), net on the accompanying Unaudited Condensed Consolidated Statement of Operations during the three months ended June 30, 2026.",
  "paragraph_id": "0001783180-26-000032:notes:102",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_noresco_sale_agreement_and_held_for_sale_classification",
  "what_changed": "This paragraph is new. On May 18, 2026 the Company agreed to sell Noresco to Opterra Energy Services, LLC, a subsidiary of LS Power Development, LLC. Noresco was historically reported in the Americas segment. Its assets and liabilities are now presented as held for sale at June 30, 2026, and closing is expected in the third quarter of 2026. The note gives no price, no expected proceeds and no impairment or gain for Noresco. The release (8k_2_02:48) puts an approximately $125 million year-over-year revenue headwind on the NORESCO exit.",
  "account": "Assets held for sale; Liabilities held for sale (Noresco disposal group); Net sales, Climate Solutions Americas",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "On May 18, 2026, the Company entered into an agreement to sell its Noresco business",
  "paragraph_id": "0001783180-26-000032:notes:103",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_held_for_sale_table_new_impairment_and_debt_rows",
  "what_changed": "The held-for-sale balance table has a new row, 'Impairment on held for sale assets'. It also shows June 30, 2026 amounts on the rows 'Short-term borrowings and current portion of long-term debt' and 'Long-term debt', where the December 31, 2025 column shows a dash. No prose in the input says which disposal group the held-for-sale debt belongs to or what kind of debt it is.",
  "account": "Assets held for sale; Liabilities held for sale; debt classified as held for sale",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Impairment on held for sale assets",
  "paragraph_id": "0001783180-26-000032:notes:105",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_tma_transition_tax_liability_paragraph_removed",
  "what_changed": "The commitments note has dropped its 'Income Taxes' subsection (prior 0001783180-26-000026:note_history:6 and 7). That subsection described a $101 million Tax Matters Agreement liability to UTC for the Tax Cuts and Jobs Act transition tax, held within Accrued liabilities as of March 31, 2026. The removed text itself said the obligation was settled in April 2026. The Separation paragraph (notes:6) still says only certain portions of the TMA remain in effect.",
  "account": "Accrued liabilities (TMA transition tax payable to UTC)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "This obligation was settled in April 2026.",
  "paragraph_id": "0001783180-26-000026:note_history:7",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_inventory_valuation_reserve_amounts_in_prose",
  "what_changed": "The inventory note now states valuation reserves of $328 million at June 30, 2026 and $337 million at December 31, 2025. The prose describes how the reserve is estimated: periodic assessments using customer demand, production requirements and historical usage. It gives no cause for the June 30 figure and does not say which way the reserve moved.",
  "account": "Inventories, net (excess and obsolete valuation reserve)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Raw materials, work-in-process and finished goods are net of valuation reserves of $328 million and $337 million as of June 30, 2026 and December 31, 2025, respectively.",
  "paragraph_id": "0001783180-26-000032:notes:14",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_commercial_paper_balance_and_weighted_rate_in_debt_note",
  "what_changed": "The debt note now states $685 million of commercial paper outstanding at June 30, 2026, at a weighted average interest rate of 4.01%. The prior 10-Q stated $708 million at 4.06% as of March 31, 2026 (note_history:13). The MD&A (mdna:162) repeats the $685 million and says the revolving credit facility had zero borrowings outstanding.",
  "account": "Short-term borrowings (commercial paper)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "At June 30, 2026, the Company had $685 million outstanding under its commercial paper facilities with a weighted average interest rate of 4.01%.",
  "paragraph_id": "0001783180-26-000032:notes:26",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_interest_expense_attributed_to_commercial_paper_borrowings",
  "what_changed": "The MD&A now says three-month interest expense of $126 million was 'a 10% increase'. It attributes this to commercial paper borrowings outstanding during the quarter. The six-month paragraph (mdna:69) gives the same cause for 'a 4% increase'. Per notes:26, commercial paper was still outstanding at June 30, 2026.",
  "account": "Interest expense",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "The increase is a result of commercial paper borrowings outstanding during the three months ended June 30, 2026.",
  "paragraph_id": "0001783180-26-000032:mdna:38",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_project_financing_debt_issued_and_repaid",
  "what_changed": "The project financing paragraph now gives six-month figures. Debt issued was $27 million in 2026 and $10 million in 2025. Repayments were $53 million in 2026 and zero in 2025. The prior 10-Q stated $14 million issued and $14 million repaid for the three months ended March 31, 2026 (note_history:16).",
  "account": "Long-term debt (project financing obligations)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Long-term debt repayments associated with these financing arrangements during the six months ended June 30, 2026 and 2025, were $53 million and zero, respectively.",
  "paragraph_id": "0001783180-26-000032:notes:33",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_share_repurchases_and_remaining_authorization_in_equity_note",
  "what_changed": "The equity note now states that 12.0 million shares were repurchased for an aggregate purchase price of $748 million in the six months ended June 30, 2026. It says approximately $4.6 billion remains under the current authorization. mdna:170 repeats the same text.",
  "account": "Treasury stock",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "During the six months ended June 30, 2026, the Company repurchased 12.0 million shares of common stock for an aggregate purchase price of $748 million.",
  "paragraph_id": "0001783180-26-000032:notes:70",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_issued_and_treasury_share_counts_in_equity_note",
  "what_changed": "The equity note now states share counts at June 30, 2026: 951,905,773 shares issued, including 126,879,717 treasury shares. At December 31, 2025 the figures were 950,633,287 and 114,891,176.",
  "account": "Common stock; Treasury stock (share counts)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "951,905,773 and 950,633,287 shares of common stock were issued, respectively, which includes 126,879,717 and 114,891,176 shares of treasury stock, respectively",
  "paragraph_id": "0001783180-26-000032:notes:67",
  "explanation": false }
```

```json
{ "id": "articulation_and_the_filed_history_repurchase_purchase_price_versus_cash_flow_prose",
  "what_changed": "The text uses two figures for six-month share repurchases. The MD&A cash-flow prose gives repurchases of common stock of $745 million. The 8-K cash flow statement line 'Repurchases of common stock' shows (745) for the six months (8k_2_02:93). The equity note (notes:70) and mdna:170 give an aggregate purchase price of $748 million for the same six months. No text in the input explains why the two figures differ.",
  "account": "Treasury stock; Repurchases of common stock (financing cash flow)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "The primary driver of the outflow was related to repurchases of our common stock totaling $745 million.",
  "paragraph_id": "0001783180-26-000032:mdna:179",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_short_term_borrowings_offset_buybacks_and_dividends",
  "what_changed": "The MD&A financing prose now says six-month outflows for repurchases ($745 million) and common dividends ($400 million) were partially offset by short-term borrowings of $361 million. For 2025 it cites long-term debt repayments of $1.2 billion instead.",
  "account": "Short-term borrowings; financing cash flows",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "These outflows were partially offset by short-term borrowings of $361 million.",
  "paragraph_id": "0001783180-26-000032:mdna:179",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_dividend_declaration_and_payment_schedule",
  "what_changed": "The MD&A now states $400 million of common dividends paid in the six months. It also states a June 2026 declaration of $0.24 per share, payable August 10, 2026 to holders of record on July 21, 2026.",
  "account": "Dividends payable; Retained earnings",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "In June 2026, the Board of Directors declared a dividend of $0.24 per share of common stock payable on August 10, 2026, to shareowners of record at the close of business on July 21, 2026.",
  "paragraph_id": "0001783180-26-000032:mdna:172",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_revenue_recognized_from_opening_contract_liabilities",
  "what_changed": "The contract balances paragraph now states $407 million of revenue recognized in the six months ended June 30, 2026 from contract liabilities held at January 1, 2026. The prior 10-Q stated $250 million for the three months ended March 31, 2026 (note_history:29). The sentence expecting a majority of current contract liabilities to be recognized within 12 months is unchanged.",
  "account": "Contract liabilities; Net sales",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "The Company recognized revenue of $407 million during the six months ended June 30, 2026, that related to contract liabilities as of January 1, 2026.",
  "paragraph_id": "0001783180-26-000032:notes:82",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_restructuring_accrual_severance_and_utilization",
  "what_changed": "The restructuring note now states $111 million accrued at June 30, 2026. It attributes the balance to cost reduction efforts, primarily severance, across each segment, and says a majority is expected to be used within 12 months. The MD&A (mdna:58, mdna:62) names announced restructuring costs as a factor in six-month cost of sales and SG&A.",
  "account": "Restructuring accrual (Accrued liabilities)",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "As of June 30, 2026, the Company had $111 million accrued for costs associated with its announced restructuring initiatives.",
  "paragraph_id": "0001783180-26-000032:notes:93",
  "explanation": true }
```

```json
{ "id": "earnings_quality_tax_rate_riello_non_deductible_impairment_and_german_rate",
  "what_changed": "The income tax note, and mdna:42 with it, now states a 25.0% effective tax rate for the three months ended June 30, 2026, compared with 20.0%. It attributes the 'year-over-year increase' to the $46 million non-deductible Riello impairment and to a $10 million increase in tax expense from a higher German effective tax rate. The German rate is a new driver in the text. The release (8k_2_02:22) also cites a higher effective tax rate. The prose does not say whether the German rate effect will recur.",
  "account": "Income tax expense; effective tax rate",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The year-over-year increase was primarily driven by the $46 million non-deductible impairment charge on Riello and a $10 million increase in tax expense associated with a higher German effective tax rate during the three months ended June 30, 2026.",
  "paragraph_id": "0001783180-26-000032:notes:94",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_swiss_valuation_allowance_partial_release_and_state_audit_settlement",
  "what_changed": "The six-month tax paragraph, and mdna:72 with it, states two benefits. The first is a net $99 million benefit from a partial release of a valuation allowance on a Swiss subsidiary's operations. The second is an $18 million favorable state income tax audit settlement. The three-month paragraph (notes:94) names neither, so the prose places both in the six months but not in the three months ended June 30, 2026. The text names the Swiss subsidiary as the source of the release but does not say what evidence about realizability changed.",
  "account": "Income tax expense; deferred tax asset valuation allowance",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "a net $99 million tax benefit from the partial release of a valuation allowance associated with our operations in a Swiss subsidiary",
  "paragraph_id": "0001783180-26-000032:notes:95",
  "explanation": true }
```

```json
{ "id": "earnings_quality_discrete_tax_benefits_not_removed_from_adjusted_results",
  "what_changed": "In the release's 2026 GAAP-to-adjusted reconciliation, the only tax line is 'Tax effect on adjustments above'. It has no tax-specific line. The 2025 reconciliation (8k_2_02:116) does carry a 'Tax specific adjustments' line. Notes:95 describes a net $99 million Swiss valuation-allowance release and an $18 million state audit settlement in the six months. Read together, the tables as labeled leave those one-off tax benefits inside six-month adjusted EPS and inside the stated 15.1% six-month adjusted effective tax rate. The full-year adjusted EPS outlook of ~$2.90 (8k_2_02:48) is built on these adjusted results.",
  "account": "Adjusted EPS; adjusted effective tax rate",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Tax effect on adjustments above",
  "paragraph_id": "0001783180-26-000030:8k_2_02:111",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_unrecognized_tax_benefits_reasonably_possible_decrease_range",
  "what_changed": "The income tax note states it is reasonably possible that unrecognized tax benefits will fall by a net $5 million to $95 million within 12 months. The same paragraph says the One Big Beautiful Bill Act had no material impact on the Statement of Operations. Insufficient: the prior-period wording of this paragraph is not in the input, and the income tax note is not tracked in the change history, so I cannot confirm whether the range is new.",
  "account": "Unrecognized tax benefits",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "The Company believes that it is reasonably possible that a net decrease in unrecognized tax benefits of $5 million to $95 million may occur within 12 months",
  "paragraph_id": "0001783180-26-000032:notes:98",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_irs_and_australia_audit_closure_expectations",
  "what_changed": "The income tax note states the IRS examination of tax year 2022 is expected to close in 2027. It states the Australia Tax Office audit of the 2021 return, which includes the Chubb Australia disentanglement, is expected to close in early 2027. Insufficient: the prior-period wording is not in the input, so I cannot confirm a change in these expected dates.",
  "account": "Unrecognized tax benefits; income tax expense",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "is under examination by the IRS with closure of the examination expected in 2027",
  "paragraph_id": "0001783180-26-000032:notes:97",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_afff_lawsuit_count_stated",
  "what_changed": "The AFFF paragraph now says the Company, KFI and others are defendants in 'more than 18,000 lawsuits'. The prior 10-Q said 'more than 17,000' (note_history:3). The note still says the Company cannot assess the probability of liability or estimate a range of loss for the remaining AFFF claims (notes:141, unchanged).",
  "account": "AFFF-related liabilities (Accrued liabilities; Other long-term liabilities)",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "have been named as defendants in more than 18,000 lawsuits",
  "paragraph_id": "0001783180-26-000032:notes:136",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_afff_direct_claims_court_approval_start",
  "what_changed": "This sentence is new (note_history:4): the process of seeking court approval of the Direct Claims Settlements with water providers will begin in the third quarter of 2026. The settlement terms are unchanged apart from the as-of date (notes:140). Those terms are $615 million in cash over five years, KFI sale proceeds estimated at $115 million, and insurance rights. The statement that no expected insurance proceeds have been recorded is likewise unchanged. The Bankruptcy Court Disclosure Statement paragraph (notes:142) reports nothing new.",
  "account": "AFFF settlement liability (Accrued liabilities; Other long-term liabilities)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "The process of seeking court approval for the Direct Claims Settlements with water providers will begin in the third quarter of 2026.",
  "paragraph_id": "0001783180-26-000032:notes:139",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_ieepa_tariff_refunds_unrecorded_gain_contingency",
  "what_changed": "The MD&A states that, as of June 30, 2026, the Company had recorded no benefit for potential refunds of IEEPA tariffs. It says the amounts were not probable and reasonably estimable. This follows the February 2026 Supreme Court ruling and the March 2026 Court of International Trade order to refund IEEPA tariffs, and the Company was an importer of record. Insufficient to identify the exact edit: the prior 10-Q wording of this paragraph is not in the input. The MD&A (mdna:27, mdna:96) still names tariffs as a headwind to gross margin and segment profit.",
  "account": "Cost of products sold; potential tariff refund (unrecorded gain contingency)",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "As of June 30, 2026, we have not recorded any benefit related to potential refunds of IEEPA tariffs paid, as such amounts were not considered probable and reasonably estimable.",
  "paragraph_id": "0001783180-26-000032:mdna:8",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_organic_sales_growth_attributed_to_volume",
  "what_changed": "The MD&A now says three-month organic sales grew 3%. Net sales were $6.4 billion, 'a 4% increase' (mdna:21). It attributes the growth primarily to Climate Solutions Americas volume on improved end-market demand. It says Europe and Asia Pacific, Middle East & Africa also saw improved demand and that Transportation was flat. The release (8k_2_02:20) states the same totals.",
  "account": "Net sales",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The organic increase was primarily due to our Climate Solutions Americas segment as improved end-market demand resulted in higher volumes.",
  "paragraph_id": "0001783180-26-000032:mdna:23",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_gross_margin_input_costs_tariffs_and_mix",
  "what_changed": "The MD&A now attributes the three-month gross margin decline it states ($41 million; 170 basis points) to higher input costs, including tariffs, and to unfavorable business mix. Volume and productivity partially offset these. The release (8k_2_02:21) cites the same factors for the 190 basis-point fall in adjusted operating margin.",
  "account": "Gross margin; Cost of products sold",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "Gross margin decreased by $41 million compared with the three months ended June 30, 2025, primarily due to higher input costs, including the impact of tariffs, and unfavorable business mix.",
  "paragraph_id": "0001783180-26-000032:mdna:27",
  "explanation": false }
```

```json
{ "id": "earnings_quality_sga_flat_with_savings_offset_by_incentive_compensation",
  "what_changed": "The MD&A now says three-month SG&A of $810 million was 'primarily flat'. It says savings from cost reduction initiatives and lower managed expenses were largely offset by higher investment spending and incentive compensation costs.",
  "account": "Selling, general and administrative",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "These benefits were largely offset by higher investment spending and incentive compensation costs.",
  "paragraph_id": "0001783180-26-000032:mdna:31",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_joint_venture_earnings_decline_americas_and_asia",
  "what_changed": "The MD&A now states three-month equity method investment net earnings of $58 million, 'a 26% decrease'. It attributes this to lower joint-venture earnings in the Americas and in Asia Pacific, Middle East & Africa. The six-month paragraph (mdna:64) states 'a 27% decrease' and attributes it to Americas joint ventures only. The segment profit paragraphs (mdna:96, mdna:110) also cite lower equity method earnings.",
  "account": "Equity method investment net earnings",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "The decrease was primarily driven by lower earnings in joint ventures within our Climate Solutions Americas and Climate Solutions Asia Pacific, Middle East & Africa segments.",
  "paragraph_id": "0001783180-26-000032:mdna:33",
  "explanation": false }
```

```json
{ "id": "earnings_quality_restructuring_costs_cited_in_gross_margin_decline",
  "what_changed": "The new six-month MD&A section explains the gross margin decline it states ($242 million; 300 basis points). Besides input costs, tariffs and mix, it adds the cost of announced restructuring initiatives as a cause. The restructuring table (notes:89) has a cost-of-sales line.",
  "account": "Gross margin; Cost of sales (restructuring)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "In addition, an increase in costs associated with announced restructuring initiatives further impacted our results.",
  "paragraph_id": "0001783180-26-000032:mdna:58",
  "explanation": false }
```

```json
{ "id": "earnings_quality_restructuring_and_compensation_costs_cited_in_sga_increase",
  "what_changed": "The six-month MD&A says SG&A was $1.7 billion, 'an 8% increase'. It attributes this primarily to announced restructuring initiatives, then to higher compensation, commission and employee-related costs. Lower consulting and other managed expenses partly offset them.",
  "account": "Selling, general and administrative",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The increase primarily relates to an increase in costs associated with announced restructuring initiatives.",
  "paragraph_id": "0001783180-26-000032:mdna:62",
  "explanation": false }
```

```json
{ "id": "across_documents_americas_demand_described_as_improved_and_reduced",
  "what_changed": "The MD&A describes Americas demand in conflicting terms. The consolidated six-month organic paragraph (mdna:54) credits growth to 'improved end-market demand across our Climate Solutions Americas' and other segments. The Americas six-month paragraph says residential was flat on reduced end-market demand and commercial was 'down 2%' on lower end-market demand. The Americas commercial decline also gets two causes: lower end-market demand for the six months, but timing of customer deliveries for the three months (mdna:93).",
  "account": "Net sales, Climate Solutions Americas",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Results in our residential business (flat) was primarily driven by reduced end-market demand offset by product mix.",
  "paragraph_id": "0001783180-26-000032:mdna:127",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_americas_commercial_decline_attributed_to_delivery_timing",
  "what_changed": "The MD&A now says three-month Americas organic growth came from volume. Residential was 'up 9%' on demand and pricing, and light commercial was 'up 10%' on higher volume. Commercial was 'down 6%', which the MD&A attributes to timing of customer deliveries, offset by improved price. Blaming delivery timing implies the delayed deliveries land in later periods. The release (8k_2_02:26) makes the same timing claim.",
  "account": "Net sales, Climate Solutions Americas commercial",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "These results were partially offset by volume reductions in our commercial business (down 6%) driven by timing of customer deliveries offset by improved price.",
  "paragraph_id": "0001783180-26-000032:mdna:93",
  "explanation": false }
```

```json
{ "id": "across_documents_americas_commercial_decline_percent_release_versus_filing",
  "what_changed": "The release says CSA Commercial was 'down 8%', with a footnote reading 'Excludes NORESCO' (8k_2_02:32). The 10-Q MD&A (mdna:93) says the Americas commercial business was 'down 6%', with no such footnote. Both attribute the decline to timing of customer deliveries. The two documents state different percentages for what both call the commercial business.",
  "account": "Net sales, Climate Solutions Americas commercial",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "partially offset by Commercial1, down 8% due to the timing of customer deliveries",
  "paragraph_id": "0001783180-26-000030:8k_2_02:26",
  "explanation": false }
```

```json
{ "id": "across_documents_americas_growth_price_in_release_volume_in_filing",
  "what_changed": "The release says Americas revenue growth was 'mainly related to price'. The 10-Q MD&A says Americas organic growth 'was driven by volume growth within certain end-markets' (mdna:93), and that consolidated organic growth came from 'higher volumes' (mdna:23). The two documents give different primary drivers for the same segment's growth in the same quarter.",
  "account": "Net sales, Climate Solutions Americas",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Segment operating margin decreased 260 basis points as revenue growth mainly related to price which was more than offset by unfavorable mix and input costs.",
  "paragraph_id": "0001783180-26-000030:8k_2_02:27",
  "explanation": false }
```

```json
{ "id": "earnings_quality_americas_segment_profit_timing_and_classification_adjustments",
  "what_changed": "The Americas three-month profit bridge (mdna:95) has an 'Other' component, shown as 3%. The text says it represents adjustments related to the timing and classification of amounts recognized in operating profit. The six-month bridge (mdna:129, mdna:131) uses the same words. The text gives no dollar amount, no description of the items and no statement of when the timing effect reverses.",
  "account": "Segment operating profit, Climate Solutions Americas",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Amounts reported in other represent adjustments related to the timing and classification of amounts recognized in operating profit.",
  "paragraph_id": "0001783180-26-000032:mdna:96",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_europe_pricing_promotions",
  "what_changed": "The MD&A now says three-month Europe residential and light commercial was 'up 7%' on higher volumes, partially offset by pricing promotions. Commercial was 'down 6%' on lower volumes. Per mdna:103, segment profit was hurt by product mix, price promotions and higher SG&A. The six-month paragraphs (mdna:135, mdna:138) repeat the promotions language.",
  "account": "Net sales and Segment operating profit, Climate Solutions Europe",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "Results in our residential and light commercial business increased (up 7%) as a result of higher volumes across the region partially offset by pricing promotions.",
  "paragraph_id": "0001783180-26-000032:mdna:100",
  "explanation": false }
```

```json
{ "id": "across_documents_europe_price_cost_favorable_in_release_promotions_in_filing",
  "what_changed": "The release attributes the Europe margin decline to unfavorable mix and selling investments, which outweighed 'favorable price / cost'. The 10-Q MD&A lists price promotions as a factor that 'further impacted the segment' (mdna:103) and says pricing promotions partially offset volume gains (mdna:100). The release defines price/cost to include cost inflation and productivity as well as pricing (8k_2_02:79).",
  "account": "Segment operating profit, Climate Solutions Europe",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Segment operating margin decreased 70 basis points driven by volume growth and favorable price / cost more than offset by unfavorable mix and selling investments.",
  "paragraph_id": "0001783180-26-000030:8k_2_02:31",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_europe_legal_reserve_no_longer_required",
  "what_changed": "The six-month Europe profit bridge (mdna:137) has an 'Other' component, shown as 1%. The text says it is the benefit of a legal reserve no longer required. The three-month Europe bridge (mdna:102) has no Other line, so the text places the reserve release in the six months but not in the three months ended June 30, 2026. The text gives no dollar amount and does not name the legal matter.",
  "account": "Segment operating profit, Climate Solutions Europe; legal reserves (accrued liabilities)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Amounts reported in other represent the benefit of a legal reserve no longer required.",
  "paragraph_id": "0001783180-26-000032:mdna:138",
  "explanation": true }
```

```json
{ "id": "estimates_and_discretion_europe_higher_warranty_related_expenses",
  "what_changed": "The six-month Europe segment paragraph now lists higher warranty-related expenses among the factors reducing segment profit. The related table is the warranty rollforward (notes:65). The prose does not say which products are involved or whether the expense will recur.",
  "account": "Warranty-related provisions; Cost of sales, Climate Solutions Europe",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "In addition, price promotions, higher selling, general and administrative expenses as well as higher warranty-related expenses further impacted the segment.",
  "paragraph_id": "0001783180-26-000032:mdna:138",
  "explanation": true }
```

```json
{ "id": "narrative_signs_of_operating_pressure_china_demand_and_price",
  "what_changed": "The MD&A now says China results were 'down 14%' for the three months and 'down 13%' for the six months (mdna:142). It says end-markets faced economic challenges that hit both demand and price, and that the rest of the region more than offset this. The release (8k_2_02:36) cites 'continued pressure in RLC in China'.",
  "account": "Net sales, Climate Solutions Asia Pacific, Middle East & Africa (China)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "Results in China decreased (down 14%) as end-markets experienced economic challenges impacting both demand and price.",
  "paragraph_id": "0001783180-26-000032:mdna:107",
  "explanation": false }
```

```json
{ "id": "earnings_quality_asia_segment_profit_includes_land_sale_gain",
  "what_changed": "The Asia Pacific, Middle East & Africa profit bridge (mdna:109) has an 'Other' component, shown as 17%. The text says it represents a gain on sale of land. The six-month bridge (mdna:144, mdna:145) says the same. The MD&A places the gain inside segment operating profit. The release's paragraph on this segment (8k_2_02:37) does not mention it, and the text gives no dollar amount.",
  "account": "Segment operating profit, Climate Solutions Asia Pacific, Middle East & Africa; Other income (expense), net",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Amounts reported in other represent a gain on sale of land.",
  "paragraph_id": "0001783180-26-000032:mdna:110",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_middle_east_conflict_joint_venture_income",
  "what_changed": "The release attributes part of the margin decline in Asia Pacific, Middle East & Africa to lower JV income caused by the Middle East conflict. It also says the Middle East had double-digit sales growth (8k_2_02:36). The 10-Q MD&A text in the input (mdna:110, mdna:33) cites lower earnings from equity method investments but does not name the conflict.",
  "account": "Equity method investment net earnings, Climate Solutions Asia Pacific, Middle East & Africa",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "lower JV income due to the impacts from the Middle East conflict",
  "paragraph_id": "0001783180-26-000030:8k_2_02:37",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_truck_and_trailer_demand",
  "what_changed": "The MD&A now says three-month Transportation organic sales were flat. Container was 'up 39%' on end-market demand. Global truck and trailer was 'down 13%' on reduced demand in North America and Europe, partially offset by improvements in Asia. The six-month paragraph (mdna:149) puts truck and trailer 'down 10%' on reduced demand 'across all regions'. Segment profit is attributed to unfavorable mix and lower volumes (mdna:117, mdna:152).",
  "account": "Net sales and Segment operating profit, Climate Solutions Transportation",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "These results were partially offset by lower volume in our global truck and trailer business (down 13%) primarily due to reduced end-market demand in North America and Europe partially offset by improvements in Asia.",
  "paragraph_id": "0001783180-26-000032:mdna:114",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_operating_cash_flow_attributed_to_working_capital",
  "what_changed": "The MD&A now reports a 'year-over-year increase' in six-month cash from continuing operations. It attributes this primarily to favorable changes in working capital balances, partially offset by lower net earnings. The prose does not say which working capital balances moved.",
  "account": "Net cash flows from continuing operating activities; Accounts receivable; Inventories; Accounts payable",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The year-over-year increase in net cash provided by continuing operating activities was primarily driven by favorable changes in working capital balances partially offset by lower net earnings compared with the prior period.",
  "paragraph_id": "0001783180-26-000032:mdna:176",
  "explanation": true }
```

```json
{ "id": "liquidity_and_capital_investing_outflow_driven_by_capital_expenditures",
  "what_changed": "The MD&A now says six-month cash used in continuing investing activities was $235 million, with $211 million of capital expenditures as the primary driver. For 2025 it gives $113 million, with $144 million of capital expenditures partly offset by $87 million of derivative settlements. The release (8k_2_02:12) refers to new U.S. factory costs. No MD&A text paragraph in the input mentions a new factory.",
  "account": "Capital expenditures; investing cash flows",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "The primary driver of the outflow related to $211 million of capital expenditures.",
  "paragraph_id": "0001783180-26-000032:mdna:178",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_cash_held_by_foreign_subsidiaries_and_restricted_cash",
  "what_changed": "The MD&A now states cash and cash equivalents of $1.3 billion at June 30, 2026, approximately 95% of it held by foreign subsidiaries. It gives restricted cash of approximately $3 million at June 30, 2026 and $2 million at December 31, 2025.",
  "account": "Cash and cash equivalents; restricted cash",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "As of June 30, 2026, we had cash and cash equivalents of $1.3 billion, of which approximately 95% was held by our foreign subsidiaries.",
  "paragraph_id": "0001783180-26-000032:mdna:156",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_long_term_note_interest_payment_expectation",
  "what_changed": "The MD&A states that long-term notes mature between 2027 and 2054. It says interest on them should come to approximately $405 million a year, at an approximate weighted-average rate of 3.65%. Insufficient: the prior-period wording is not in the input, so I cannot tell which figure, if any, changed.",
  "account": "Interest expense; long-term debt",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Interest payments related to long-term notes are expected to approximate $405 million per year, reflecting an approximate weighted-average interest rate of 3.65%.",
  "paragraph_id": "0001783180-26-000032:mdna:163",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_results_described_as_better_than_expected",
  "what_changed": "The release calls second-quarter results 'better than expected' (8k_2_02:13). It says organic sales returned to growth earlier than expected. It also says improving residential and light commercial markets in CSA and CSE are encouraging.",
  "account": "Net sales",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Organic sales returned to growth earlier than expected, up 3%, driven by strong performance in our CSA segment.",
  "paragraph_id": "0001783180-26-000030:8k_2_02:14",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_orders_growth_and_record_backlog",
  "what_changed": "The release states total orders up ~40%, Commercial HVAC orders up ~65% and data center orders up more than 300%. The total and Commercial HVAC figures exclude NORESCO and Riello (8k_2_02:15). It cites 'record backlog levels' as a basis for the raised outlook (8k_2_02:14). Its definitions (8k_2_02:78) say orders 'may not be subject to penalty if cancelled'.",
  "account": "Net sales (future periods); backlog",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "Total company orders1 up ~40%; Commercial HVAC1 up ~65%; data centers up >300%",
  "paragraph_id": "0001783180-26-000030:8k_2_02:6",
  "explanation": false }
```


```json
{ "id": "results_against_expectations_free_cash_flow_outlook_held",
  "what_changed": "In the same guidance table, free cash flow is ~$2 billion in both the current and prior columns. The release raises its sales, adjusted operating profit and adjusted EPS guidance but leaves free cash flow guidance where it was.",
  "account": "Free cash flow (full year)",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Free Cash Flow* | ~$2 billion | ~$2 billion",
  "paragraph_id": "0001783180-26-000030:8k_2_02:48",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_divestiture_revenue_headwind_estimates",
  "what_changed": "Guidance now shows net acquisitions and divestitures at (2%). It gives year-over-year revenue headwinds of ~$225 million from Riello and ~$125 million from NORESCO. The prior column showed (1%) and ~$250 million from the Riello exit alone. The Riello estimate has been restated, and a NORESCO estimate has been added.",
  "account": "Net sales",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "~$225 million and ~$125 million year-over-year revenue headwind from Riello and NORESCO exits, respectively",
  "paragraph_id": "0001783180-26-000030:8k_2_02:48",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_outlook_includes_noresco_exit_and_new_us_factory_costs",
  "what_changed": "A new line in the release says the raised outlook includes about $0.05 of adjusted EPS impact from the NORESCO exit and new U.S. factory costs. This is the first reference in the input to new U.S. factory costs. No MD&A or notes paragraph in the input describes the factory, its cost or its timing.",
  "account": "Adjusted EPS; Cost of products sold",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "Includes ~($0.05) adj. EPS impact from NORESCO exit and new U.S. factory costs",
  "paragraph_id": "0001783180-26-000030:8k_2_02:12",
  "explanation": false }
```

```json
{ "id": "across_documents_free_cash_flow_definition_versus_reconciliation_starting_line",
  "what_changed": "The release defines free cash flow as cash from continuing operating activities less capex. But the headline (8k_2_02:9), the prose (8k_2_02:45) and the reconciliations (8k_2_02:44, 8k_2_02:119) all start from the line 'Net cash flows provided by operating activities', which is $927 million for the quarter. In the cash flow statement (8k_2_02:93) that line follows separate lines for continuing ($888 million) and discontinued ($39 million) operating activities. As labeled, reported free cash flow starts from the total that includes discontinued operating cash flows, not from the continuing figure the definition names.",
  "account": "Free cash flow; Net cash flows provided by operating activities",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Free cash flow is a non-GAAP financial measure that represents net cash flows provided by continuing operating activities (a GAAP measure) less capital expenditures.",
  "paragraph_id": "0001783180-26-000030:8k_2_02:78",
  "explanation": false }
```

```json
{ "id": "across_documents_noresco_agreement_not_discussed_in_mdna_text",
  "what_changed": "The MD&A text paragraphs in the input discuss the Riello agreement and its completion (mdna:13, mdna:167). None mentions the May 18, 2026 Noresco sale agreement, its held-for-sale classification or its expected third-quarter closing. Those are disclosed in notes:103 and in the release (8k_2_02:12, 8k_2_02:48, 8k_2_02:49). The MD&A paragraphs marked unchanged repeat the prior 10-Q, which the note change history dates 2026-04-30, before the agreement date.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "On December 16, 2025, we entered into a purchase agreement to sell our Riello business with expected gross proceeds of approximately $430 million.",
  "paragraph_id": "0001783180-26-000032:mdna:167",
  "explanation": false }
```


## Paragraphs not made into items

Every paragraph carried as text, with the reason it has no item of its own. "Covered by" means its substance is in the named item.

### Notes (0001783180-26-000032)
- `notes:2`: consolidation policy; the change history lists no change for this note block
- `notes:6`: date rolled forward only (note_history:11)
- `notes:9`: heading
- `notes:10`: pending ASU 2024-03 disclosure; the change history lists no change
- `notes:13`: amounts only (inventory table)
- `notes:17`: amounts only (goodwill rollforward); held-for-sale reclassification covered by the Noresco and held-for-sale table items
- `notes:20`: amounts only (intangibles table)
- `notes:22`: amounts only (amortization table)
- `notes:23`: heading and intro line; no change listed
- `notes:24`: amounts only; the history shows it as added and removed under a new tag, with the same rows
- `notes:25`: heading
- `notes:27`: intro line
- `notes:28`: amounts only (long-term debt table, note_history:14)
- `notes:29`: footnote already present in the prior table (marker (1) in the prior note_history:14); no change listed
- `notes:30`: heading
- `notes:31`: date rolled forward only (note_history:15)
- `notes:32`: heading
- `notes:34`: heading
- `notes:35`: date rolled forward only (note_history:17)
- `notes:45`: amounts only (derivative fair value table)
- `notes:49`: amounts only (notes fair value table)
- `notes:55`: amounts only (pension contributions table)
- `notes:57`: amounts only (net periodic pension table)
- `notes:61`: amounts only (stock compensation table)
- `notes:64`: intro line to the warranty table; no substance
- `notes:65`: amounts only (warranty rollforward); Europe warranty narrative covered by the warranty item on mdna:138
- `notes:72`: intro line; period rolled forward
- `notes:73`: amounts only (AOCI table)
- `notes:74`: intro line; period rolled forward
- `notes:75`: amounts only (prior-year AOCI table)
- `notes:78`: amounts only (sales by type table)
- `notes:81`: amounts only (contract balances table)
- `notes:85`: period rolled forward only (note_history:25)
- `notes:86`: amounts only (geographic table)
- `notes:89`: amounts only (restructuring by segment table)
- `notes:92`: amounts only (restructuring rollforward); accrual prose covered by the item on notes:93
- `notes:96`: insufficient: valuation-allowance policy language with no amount or date; the income tax note is not tracked in the change history and the prior text is not in the input
- `notes:101`: amounts only (EPS table)
- `notes:115`: amounts only (segment tables)
- `notes:116`: amounts only (prior-year six-month segment table)
- `notes:117`: amounts only; new Riello impairment row covered by the item on notes:102
- `notes:119`: heading; no change listed
- `notes:120`: related-party intro; no change listed
- `notes:121`: amounts only (note_history:22)
- `notes:122`: intro line; no change listed
- `notes:123`: amounts only (note_history:23)
- `notes:124`: general ASC 450 language; no change listed
- `notes:125`: heading
- `notes:126`: environmental accrual policy; no change listed
- `notes:127`: intro line
- `notes:128`: amounts only (note_history:1)
- `notes:129`: environmental policy; no change listed
- `notes:130`: heading
- `notes:131`: asbestos description; no change listed
- `notes:132`: intro line
- `notes:133`: amounts only (note_history:2)
- `notes:134`: asbestos method; no change listed
- `notes:135`: heading
- `notes:137`: KFI bankruptcy history; no change listed
- `notes:138`: settlement agreement history; no change listed
- `notes:140`: date rolled forward only (note_history:5)
- `notes:141`: remaining AFFF claims not estimable; no change listed
- `notes:142`: Disclosure Statement status; no change listed and no new court development
- `notes:143`: heading
- `notes:144`: antitrust suits (since March 2026); no change listed, carried from prior period
- `notes:145`: heading
- `notes:146`: general contingencies; no change listed
- `notes:147`: general litigation; no change listed

### MD&A (0001783180-26-000032)
- `mdna:13`: Riello agreement, impairment and completion restated; covered by the items on notes:4 and notes:102
- `mdna:17`: heading; period rolled forward
- `mdna:19`: amounts only
- `mdna:21`: net sales amount lead-in; covered by the item on mdna:23
- `mdna:22`: amounts only
- `mdna:25`: gross margin amount lead-in; covered by the item on mdna:27
- `mdna:26`: amounts only
- `mdna:29`: operating expense amount lead-in; covered by the items on mdna:31 and mdna:33
- `mdna:30`: amounts only
- `mdna:34`: Riello impairment restated, covered by the item on notes:102; the CCR sentence is a prior-year item
- `mdna:36`: non-operating amount lead-in; covered by the item on mdna:38
- `mdna:37`: amounts only
- `mdna:40`: amounts only (tax rate table)
- `mdna:42`: same substance as notes:94; covered
- `mdna:45`: amounts only; Riello row covered by the item on notes:102
- `mdna:48`: heading (new six-month section)
- `mdna:49`: intro line
- `mdna:50`: amounts only
- `mdna:51`: heading
- `mdna:52`: six-month net sales amount lead-in; covered by the item on mdna:127
- `mdna:53`: amounts only
- `mdna:54`: six-month organic narrative; covered by the demand-characterization item on mdna:127
- `mdna:55`: heading
- `mdna:56`: six-month gross margin lead-in; covered by the item on mdna:58
- `mdna:57`: amounts only
- `mdna:59`: heading
- `mdna:60`: six-month operating expense lead-in; covered by the item on mdna:62
- `mdna:61`: amounts only
- `mdna:63`: research and development boilerplate; no amount or cause
- `mdna:64`: six-month equity method earnings; covered by the item on mdna:33
- `mdna:65`: Riello impairment restated; covered by the item on notes:102
- `mdna:66`: heading
- `mdna:67`: six-month non-operating lead-in; covered by the item on mdna:38
- `mdna:68`: amounts only
- `mdna:69`: six-month interest expense cause; covered by the item on mdna:38
- `mdna:70`: heading
- `mdna:71`: amounts only
- `mdna:72`: same substance as notes:95; covered
- `mdna:73`: heading
- `mdna:74`: non-GAAP definition boilerplate
- `mdna:75`: amounts only
- `mdna:76`: non-GAAP boilerplate
- `mdna:77`: page number
- `mdna:85`: heading; period rolled forward
- `mdna:87`: amounts only
- `mdna:89`: amounts only
- `mdna:91`: Americas sales amount lead-in; covered by the item on mdna:93
- `mdna:92`: amounts only
- `mdna:94`: Americas profit amount lead-in; covered by the item on mdna:96
- `mdna:95`: amounts only; Other row covered by the item on mdna:96
- `mdna:98`: Europe sales amount lead-in; covered by the item on mdna:100
- `mdna:99`: amounts only
- `mdna:101`: Europe profit amount lead-in; covered by the item on mdna:100
- `mdna:102`: amounts only; absence of an Other row noted in the item on mdna:138
- `mdna:103`: Europe profit drivers; covered by the items on mdna:100 and 8k_2_02:31
- `mdna:105`: Asia sales amount lead-in; covered by the item on mdna:107
- `mdna:106`: amounts only
- `mdna:108`: Asia profit amount lead-in; covered by the item on mdna:110
- `mdna:109`: amounts only; Other row covered by the item on mdna:110
- `mdna:112`: Transportation sales amount lead-in; covered by the item on mdna:114
- `mdna:113`: amounts only
- `mdna:115`: Transportation profit amount lead-in; covered by the item on mdna:114
- `mdna:116`: amounts only
- `mdna:117`: Transportation profit drivers; covered by the item on mdna:114
- `mdna:118`: page number
- `mdna:119`: heading
- `mdna:120`: intro line
- `mdna:121`: amounts only
- `mdna:122`: intro line
- `mdna:123`: amounts only
- `mdna:124`: heading
- `mdna:125`: six-month Americas sales lead-in; covered by the item on mdna:127
- `mdna:126`: amounts only
- `mdna:128`: six-month Americas profit lead-in; covered by the item on mdna:96
- `mdna:129`: amounts only
- `mdna:130`: page number
- `mdna:131`: same drivers and timing-and-classification wording as mdna:96; covered
- `mdna:132`: heading
- `mdna:133`: six-month Europe sales lead-in; covered by the item on mdna:100
- `mdna:134`: amounts only
- `mdna:135`: six-month Europe organic narrative; covered by the item on mdna:100
- `mdna:136`: six-month Europe profit lead-in; covered by the items on mdna:138
- `mdna:137`: amounts only; Other row covered by the legal reserve item on mdna:138
- `mdna:139`: heading
- `mdna:140`: six-month Asia sales lead-in; covered by the item on mdna:107
- `mdna:141`: amounts only
- `mdna:142`: six-month China narrative; covered by the item on mdna:107
- `mdna:143`: six-month Asia profit lead-in; covered by the item on mdna:110
- `mdna:144`: amounts only
- `mdna:145`: six-month Asia profit drivers and land gain; covered by the item on mdna:110
- `mdna:146`: heading
- `mdna:147`: six-month Transportation sales lead-in; covered by the item on mdna:114
- `mdna:148`: amounts only
- `mdna:149`: six-month Transportation narrative; covered by the item on mdna:114
- `mdna:150`: six-month Transportation profit lead-in; covered by the item on mdna:114
- `mdna:151`: amounts only
- `mdna:152`: six-month Transportation profit drivers; covered by the item on mdna:114
- `mdna:153`: page number
- `mdna:160`: amounts only (capitalization table)
- `mdna:162`: commercial paper and revolver amounts; covered by the item on notes:26
- `mdna:164`: date rolled forward only (ratings intro)
- `mdna:170`: same text as notes:70; covered
- `mdna:175`: amounts only (cash flow table)
- `mdna:177`: page number

### Item 4 controls (0001783180-26-000032)
- `item_4_controls:1`: heading
- `item_4_controls:2`: disclosure controls conclusion; date rolled forward only
- `item_4_controls:3`: no change in ICFR; date rolled forward only

### 8-K item 2.02 (0001783180-26-000030)
- `8k_2_02:1`: exhibit file header
- `8k_2_02:2`: document label
- `8k_2_02:3`: exhibit label
- `8k_2_02:4`: release title
- `8k_2_02:5`: headline on raised outlook; covered by the item on 8k_2_02:11
- `8k_2_02:7`: sales bullet; covered by the item on mdna:23
- `8k_2_02:8`: EPS bullet; amounts only
- `8k_2_02:9`: cash flow bullet; covered by the free cash flow item on 8k_2_02:78
- `8k_2_02:10`: capital return bullet; amounts, covered by the repurchase and dividend items
- `8k_2_02:13`: 'better than expected' sentence; covered by the item on 8k_2_02:14
- `8k_2_02:15`: orders footnote excluding NORESCO and Riello; covered by the item on 8k_2_02:6
- `8k_2_02:16`: page number
- `8k_2_02:17`: heading
- `8k_2_02:18`: heading
- `8k_2_02:19`: amounts only
- `8k_2_02:20`: sales narrative; covered by the item on mdna:23
- `8k_2_02:21`: operating profit and margin drivers; covered by the item on mdna:27
- `8k_2_02:22`: EPS decline drivers; covered by the tax item on notes:94
- `8k_2_02:23`: page number
- `8k_2_02:24`: heading
- `8k_2_02:25`: amounts only
- `8k_2_02:28`: heading
- `8k_2_02:29`: amounts only
- `8k_2_02:30`: Europe sales narrative; covered by the item on mdna:100
- `8k_2_02:32`: footnote 'Excludes NORESCO'; covered by the item on 8k_2_02:26
- `8k_2_02:33`: page number
- `8k_2_02:34`: heading
- `8k_2_02:35`: amounts only
- `8k_2_02:36`: Asia sales narrative; covered by the items on mdna:107 and 8k_2_02:37
- `8k_2_02:38`: heading
- `8k_2_02:39`: amounts only
- `8k_2_02:40`: Transportation sales narrative; covered by the item on mdna:114
- `8k_2_02:41`: Transportation margin; covered by the item on mdna:114
- `8k_2_02:42`: page number
- `8k_2_02:43`: heading
- `8k_2_02:44`: amounts only; starting line referenced in the item on 8k_2_02:78
- `8k_2_02:45`: cash flow prose; covered by the item on 8k_2_02:78
- `8k_2_02:46`: page number
- `8k_2_02:47`: heading
- `8k_2_02:49`: divestiture status; covered by the items on notes:4 and notes:103
- `8k_2_02:50`: forward non-GAAP reconciliation boilerplate
- `8k_2_02:51`: guidance as-of date
- `8k_2_02:52`: heading
- `8k_2_02:53`: conference call logistics
- `8k_2_02:54`: page number
- `8k_2_02:55`: heading only; cautionary statement body not carried in input
- `8k_2_02:56`: page number
- `8k_2_02:57`: heading
- `8k_2_02:58`: company description boilerplate
- `8k_2_02:59`: tagline
- `8k_2_02:60`: release tag
- `8k_2_02:61`: contact label
- `8k_2_02:62`: contact label
- `8k_2_02:63`: contact name
- `8k_2_02:64`: contact phone
- `8k_2_02:65`: contact email
- `8k_2_02:66`: contact label
- `8k_2_02:67`: contact name
- `8k_2_02:68`: contact phone
- `8k_2_02:69`: contact email
- `8k_2_02:70`: page number
- `8k_2_02:71`: heading
- `8k_2_02:72`: intro line
- `8k_2_02:73`: heading
- `8k_2_02:74`: non-GAAP boilerplate
- `8k_2_02:75`: non-GAAP measure list
- `8k_2_02:76`: non-GAAP definitions
- `8k_2_02:77`: segment operating profit definition
- `8k_2_02:79`: price/cost definition; referenced in the item on 8k_2_02:31
- `8k_2_02:80`: forward non-GAAP boilerplate
- `8k_2_02:81`: page number
- `8k_2_02:82`: heading
- `8k_2_02:83`: heading
- `8k_2_02:84`: amounts only (statement of operations)
- `8k_2_02:85`: page number
- `8k_2_02:86`: heading
- `8k_2_02:87`: heading
- `8k_2_02:88`: amounts only (balance sheet)
- `8k_2_02:89`: page number
- `8k_2_02:90`: heading
- `8k_2_02:91`: heading
- `8k_2_02:92`: label
- `8k_2_02:93`: amounts only (cash flow statement); lines referenced in the items on 8k_2_02:78 and mdna:179
- `8k_2_02:94`: page number
- `8k_2_02:95`: heading
- `8k_2_02:96`: heading
- `8k_2_02:97`: amounts only (segment summary)
- `8k_2_02:98`: page number
- `8k_2_02:99`: heading
- `8k_2_02:100`: amounts only
- `8k_2_02:101`: amounts only
- `8k_2_02:102`: page number
- `8k_2_02:103`: heading
- `8k_2_02:104`: heading
- `8k_2_02:105`: amounts only; Riello impairment row covered by the item on notes:102
- `8k_2_02:106`: amounts only
- `8k_2_02:107`: page number
- `8k_2_02:108`: heading
- `8k_2_02:109`: heading
- `8k_2_02:110`: heading
- `8k_2_02:112`: page number
- `8k_2_02:113`: heading
- `8k_2_02:114`: heading
- `8k_2_02:115`: heading
- `8k_2_02:116`: amounts only (2025 reconciliation); its tax-specific row referenced in the item on 8k_2_02:111
- `8k_2_02:117`: page number
- `8k_2_02:118`: heading
- `8k_2_02:119`: amounts only; covered by the item on 8k_2_02:78
- `8k_2_02:120`: heading
- `8k_2_02:121`: amounts only (net debt)
- `8k_2_02:122`: page number
- 8-K item-code list: the only filing new since the prior 10-Q, other than this release, is the 2026-07-24 5.02 filing, which has an item. There are no late-filing notifications.

### Note change history (reference only; each entry maps to a notes paragraph above)
- `note_history:1`: copy of notes:128 (amounts only)
- `note_history:8`: copy of notes:128 (amounts only)
- `note_history:2`: copy of notes:133 (amounts only)
- `note_history:9`: copy of notes:133 (amounts only)
- `note_history:3`: has an item via notes:136
- `note_history:4`: has an item via notes:139
- `note_history:5`: date rolled (notes:140)
- `note_history:10`: has an item via notes:4
- `note_history:11`: date rolled (notes:6)
- `note_history:12`: amounts only (notes:24)
- `note_history:20`: amounts only (notes:24)
- `note_history:13`: has an item via notes:26
- `note_history:14`: amounts only (notes:28)
- `note_history:19`: amounts only (notes:28)
- `note_history:15`: date rolled (notes:31)
- `note_history:16`: has an item via notes:33
- `note_history:17`: date rolled (notes:35)
- `note_history:22`: amounts only (notes:121)
- `note_history:23`: amounts only (notes:123)
- `note_history:24`: amounts only (notes:78)
- `note_history:27`: amounts only (notes:78)
- `note_history:25`: period rolled (notes:85)
- `note_history:26`: amounts only (notes:86)
- `note_history:28`: amounts only (notes:81)
- `note_history:29`: has an item via notes:82
- Removed prior entries:
  - 0001783180-26-000026:note_history:6 is a heading only.
  - 0001783180-26-000026:note_history:7 has an item (TMA paragraph removed).
  - 0001783180-26-000026:note_history:18 and :21 are the prior short-term table, re-tagged; amounts only.

## Insufficient

Nine paragraphs where the input does not show what changed:
- **`notes:96` (not an item):** valuation-allowance policy text; the prior wording is not in the input.
- **`notes:97`:** audit closure dates; the prior wording is not in the input.
- **`notes:98`:** unrecognized tax benefit range; the prior wording is not in the input.
- **`mdna:8`:** IEEPA refund paragraph; the prior wording is not in the input.
- **`mdna:163`:** interest-payment expectation; the prior wording is not in the input.
- **8-K 5.02 filed 2026-07-24:** the body is not in the input.
- **Item 1A diff, Exhibit 21 diff and Exhibit 10:** none of them is in the directory.
