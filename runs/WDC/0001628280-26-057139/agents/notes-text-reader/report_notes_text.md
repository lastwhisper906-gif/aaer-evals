# WDC 10-K 0001628280-26-057139 (FY2026, ended 2026-07-03): notes-text reader

## Input check

- Files read in full: input_8k.md, input_controls.md, input_mdna.md, input_notes.md (lines 1-1558), input_notes_history.md, input_prior_predictions.md.
- Nothing out of scope is in the directory: no trend table, prices, abnormal returns, short interest, other-company files, prior probabilities or outcome window.
- Prior predictions: none on record. No flags to carry forward.
- **insufficient**: the Item 1A diff is not in the input.
- **insufficient**: the Exhibit 21 diff is not in the input.
- **insufficient**: no Exhibit 10 was pulled.
- **insufficient**: only Item 2.02 of the 8-Ks has a body. Every other 8-K is listed by item code only, including:
  - 3.02 on 2026-06-03 and 2026-06-08
  - 8.01 on 2026-06-11
  - 5.02/7.01 on 2026-05-28
  - 3.03 on 2026-02-18 and 5.03 on 2026-02-24
- **insufficient**: the Forward-Looking Statements body in the press release is a placeholder (`###`).
- The notes are carried in full text, with no `[same as prior period]` markers. The note history compares the Q2 and Q3 FY2026 10-Qs, not the prior 10-K. So for standing policy text there is often no baseline, and those paragraphs are marked insufficient below.
- Count of insufficient: 5 input-level (above), plus 23 paragraph-level (marked in the accounting list).
- No arithmetic was done. Where two documents state amounts for the same caption, both are quoted and the reconciliation is left to the numbers reader.

## Items

```json
[
{"id":"structure_and_disclosure_changes_fifty_three_week_fiscal_year","what_changed":"The annual note states that fiscal 2026 had 53 weeks, with a 14-week first quarter. Fiscal 2025 and 2024 had 52 weeks.","account":"Revenue, net; operating expenses","expected_direction":"up","horizon":"this quarter (FY2026 annual comparison); the effect reverses in the Q1 FY2027 comparison","quote":"Fiscal year 2026, which ended on July 3, 2026, comprised 53 weeks, with the first quarter consisting of 14 weeks and the remaining quarters consisting of 13 weeks.","paragraph_id":"0001628280-26-057139:notes:19","explanation":false},
{"id":"across_documents_revenue_explanation_silent_on_extra_week","what_changed":"MD&A attributes the full-year revenue increase to exabytes sold and ASPs per exabyte, driven by demand. The paragraph does not mention the 14-week first quarter disclosed at mdna:5 and notes:19. Whether the extra week accounts for part of the increase is for the numbers reader.","account":"Revenue, net","expected_direction":"none","horizon":"this quarter","quote":"Net revenue increased by 36% in 2026 compared to 2025, primarily driven by a 25% increase in exabytes sold and an 8% increase in ASPs per exabyte, both of which were driven by strong demand across all of our end markets.","paragraph_id":"0001628280-26-057139:mdna:33","explanation":false},
{"id":"results_against_expectations_first_quarter_guidance_against_fourteen_week_quarter","what_changed":"New guidance gives a year-over-year growth range for Q1 FY2027. Per notes:19, the comparison quarter (Q1 FY2026) had 14 weeks. The press release does not mention the different week count.","account":"Revenue, net","expected_direction":"up","horizon":"next quarter","quote":"Q1FY27 revenue expected to be up 42% to 49% year-over-year","paragraph_id":"0001628280-26-053305:8k_2_02:10","explanation":false},
{"id":"results_against_expectations_guidance_margin_expansion","what_changed":"The CFO gives Q1 FY2027 midpoints for revenue, non-GAAP gross margin and non-GAAP EPS. The same paragraph says the company is confident of 'further margin expansion' and 'strong free cash flow generation'.","account":"Gross margin; revenue","expected_direction":"up","horizon":"next quarter","quote":"we expect revenue of $4.1 billion, non-GAAP gross margin of 55.5%, and non-GAAP EPS of $4.00","paragraph_id":"0001628280-26-053305:8k_2_02:23","explanation":false},
{"id":"results_against_expectations_management_cites_increasing_visibility","what_changed":"The CEO enters fiscal 2027 citing durability of demand and 'increasing visibility'. This echoes the MD&A statement that customers are extending their commercial arrangements (mdna:8).","account":"Revenue, net","expected_direction":"up","horizon":"12 months","quote":"we enter fiscal year 2027 with continued confidence in the durability of demand and with increasing visibility into our business","paragraph_id":"0001628280-26-053305:8k_2_02:12","explanation":false},
{"id":"across_documents_longer_commercial_arrangements_versus_immaterial_remaining_obligations","what_changed":"MD&A says customers are extending the duration of their commercial arrangements, which improves visibility of demand. The notes say three things: remaining performance obligations were not material (notes:49), the one-year-or-less practical expedient is applied, and contract assets and liabilities were not material (notes:50). The prose does not say whether the longer arrangements carry volume, price or prepayment terms.","account":"Remaining performance obligations; contract liabilities","expected_direction":"none","horizon":"12 months","quote":"customers are partnering with us earlier to support their future growth requirements and are extending the duration of their commercial arrangements, which improves our long-term visibility of demand","paragraph_id":"0001628280-26-057139:mdna:8","explanation":false},
{"id":"earnings_quality_customer_concentration_three_customers","what_changed":"The note states FY2026 percentages for three customers above 10% and for the top 10. The customer list now names 'neoclouds' alongside hyperscale cloud service providers.","account":"Revenue, net","expected_direction":"none","horizon":"12 months","quote":"For 2026, three customers accounted for 16%, 15%, and 13%, respectively","paragraph_id":"0001628280-26-057139:notes:103","explanation":false},
{"id":"earnings_quality_receivables_concentration_two_customers","what_changed":"At year-end, two customers hold stated shares of net receivables. The prior-year comparison names three customers. Credit-loss reserves are described as not material, and collateral is used 'in some cases'.","account":"Accounts receivable, net","expected_direction":"none","horizon":"next quarter","quote":"As of July 3, 2026, two customers accounted for 25% and 17%, respectively","paragraph_id":"0001628280-26-057139:notes:104","explanation":false},
{"id":"revenue_recognition_accounts_receivable_growth_explained_by_shipments","what_changed":"Management attributes the FY2026 receivables increase to growth in shipments. Payment terms, customer mix and the timing of shipments within the quarter are not mentioned. notes:51 says terms are typically less than two months.","account":"Accounts receivable, net","expected_direction":"up","horizon":"this quarter","quote":"a $541 million increase in accounts receivable driven by our growth in shipments to customers","paragraph_id":"0001628280-26-057139:mdna:61","explanation":true},
{"id":"earnings_quality_inventory_build_explained_by_production_ramp","what_changed":"Management attributes the FY2026 inventory increase to a production ramp for growing demand. This is the same wording the paragraph uses for the 2025 inventory increase. The finished goods line is not discussed in prose.","account":"Inventories","expected_direction":"up","horizon":"this quarter","quote":"a $218 million increase in inventories as we ramped production in response to growing demand","paragraph_id":"0001628280-26-057139:mdna:61","explanation":true},
{"id":"liquidity_and_capital_payables_extended_by_supplier_terms","what_changed":"Part of the payables increase is attributed to 'more favorable payment terms with suppliers'. notes:342 states supplier terms generally of 60 to 90 days. notes:343 gives supplier-finance obligations at both year-ends.","account":"Accounts payable","expected_direction":"up","horizon":"this quarter","quote":"a $385 million increase in accounts payable as we ramped up purchases for production as well as more favorable payment terms with suppliers","paragraph_id":"0001628280-26-057139:mdna:61","explanation":false},
{"id":"liquidity_and_capital_taxes_payable_decrease_timing_of_payments","what_changed":"The decrease in taxes payable is attributed to payment timing. The 2025 increase in the same paragraph is also attributed to timing.","account":"Income taxes payable","expected_direction":"down","horizon":"this quarter","quote":"a $627 million decrease in taxes payable resulting from the timing of payments","paragraph_id":"0001628280-26-057139:mdna:61","explanation":false},
{"id":"earnings_quality_accrued_compensation_variable_plans","what_changed":"Accrued compensation rose and is attributed to higher variable-plan performance. mdna:42 also cites variable compensation in R&D.","account":"Accrued compensation","expected_direction":"up","horizon":"this quarter","quote":"a $144 million increase in accrued compensation driven by higher performance on our variable compensation plans","paragraph_id":"0001628280-26-057139:mdna:61","explanation":false},
{"id":"earnings_quality_other_assets_liabilities_other_taxes","what_changed":"There is a new source of operating cash in other assets and liabilities, attributed only to 'recognition and payment of other taxes'. The taxes are not identified.","account":"Other assets and liabilities, net","expected_direction":"none","horizon":"this quarter","quote":"$230 million from other assets and liabilities primarily driven by recognition and payment of other taxes","paragraph_id":"0001628280-26-057139:mdna:61","explanation":false},
{"id":"structure_and_disclosure_changes_cash_flow_reclassification","what_changed":"Prior-year cash flow amounts were reclassified. The prose does not say which lines or how much.","account":"Consolidated Statements of Cash Flows","expected_direction":"none","horizon":"this quarter","quote":"Certain prior year amounts have been reclassified in the Consolidated Statements of Cash Flows to conform to the current year presentation.","paragraph_id":"0001628280-26-057139:notes:25","explanation":false},
{"id":"structure_and_disclosure_changes_income_tax_disclosure_standard_adopted","what_changed":"ASU 2023-09 was adopted prospectively. There is a new jurisdiction-level rate reconciliation, with Thailand shown separately (notes:215), and new cash-taxes-paid tables (notes:220). Prior years keep the old format (notes:222).","account":"Income tax expense (benefit)","expected_direction":"none","horizon":"this quarter","quote":"The Company adopted this standard on a prospective basis for the year ended July 3, 2026.","paragraph_id":"0001628280-26-057139:notes:85","explanation":false},
{"id":"estimates_and_discretion_early_adoption_induced_conversion_standard","what_changed":"ASU 2024-04 was adopted early, ahead of its required effective date, and applied to the June 2026 exchanges of the convertible notes. notes:173 says the resulting induced conversion expense was immaterial.","account":"Costs in connection with convertible notes transactions","expected_direction":"none","horizon":"this quarter","quote":"The Company adopted the standard on a prospective basis for the year ended July 3, 2026 and applied it to the exchange transactions of the 2028 Convertible Notes","paragraph_id":"0001628280-26-057139:notes:86","explanation":false},
{"id":"structure_and_disclosure_changes_sandisk_retained_interest_fully_disposed","what_changed":"The remaining Sandisk shares were used in Q4 equity-for-equity exchanges, and the company now holds no Sandisk stock. There will be no further mark-to-market on this interest.","account":"Retained interest in Sandisk; gain (loss) on retained interest in Sandisk","expected_direction":"down","horizon":"next quarter","quote":"As of July 3, 2026, the Company no longer held any shares of Sandisk common stock.","paragraph_id":"0001628280-26-057139:notes:119","explanation":false},
{"id":"earnings_quality_sandisk_mark_to_market_gain_not_recurring","what_changed":"MD&A identifies a mark-to-market gain on Sandisk as the main driver of the change in other income. The 8-K excludes it from non-GAAP. With the shares gone (notes:119), the gain cannot recur.","account":"Total interest and other income (expense), net","expected_direction":"down","horizon":"next quarter","quote":"a mark-to-market gain on our retained interest in Sandisk of $6.50 billion in the current year","paragraph_id":"0001628280-26-057139:mdna:47","explanation":false},
{"id":"articulation_and_the_filed_history_debt_for_equity_exchange_cost_amounts","what_changed":"MD&A states a current-year debt-for-equity exchange cost. notes:162 says the February 2026 exchange 'resulted in $539 million recorded in Costs in connection with debt-for-equity exchange'. It also mentions a $6 million write-off of issuance costs on the redemptions, without naming the caption. The numbers reader should reconcile the two.","account":"Costs in connection with debt-for-equity exchange","expected_direction":"none","horizon":"this quarter","quote":"$545 million of costs incurred in connection with our debt-for-equity exchange in the current year","paragraph_id":"0001628280-26-057139:mdna:47","explanation":false},
{"id":"articulation_and_the_filed_history_convertible_notes_transaction_cost_components","what_changed":"MD&A states a current-year convertible notes transaction cost. In the notes, three pieces relate to it:\n- notes:172 puts a $106 million derivative remeasurement in this caption.\n- notes:173 adds an immaterial induced conversion expense to the same caption.\n- notes:173 also records a $10 million issuance-cost write-off, caption not stated.\nThe numbers reader should reconcile.","account":"Costs in connection with convertible notes transactions","expected_direction":"none","horizon":"this quarter","quote":"$108 million of costs in connection with our convertible notes transactions in the current year","paragraph_id":"0001628280-26-057139:mdna:47","explanation":false},
{"id":"liquidity_and_capital_interest_expense_lower_with_debt_reduction","what_changed":"Lower interest expense is attributed to reduced debt. The 8-K guidance table puts Q1 FY2027 interest and other expense at about $15 million.","account":"Interest expense","expected_direction":"down","horizon":"next quarter","quote":"lower interest expense of $192 million, which reflects the reduction in our debt levels","paragraph_id":"0001628280-26-057139:mdna:47","explanation":false},
{"id":"liquidity_and_capital_february_bridge_loan_and_debt_for_equity_exchange","what_changed":"The annual note restates the February 2026 sequence:\n- a $1.50 billion bridge loan\n- redemption of the Senior Notes, with a $6 million write-off\n- exchange for 5.8 million Sandisk shares valued at $3.62 billion, with a $539 million cost\nThe cause of the discount is reworded. The Q3 10-Q (note_history:11) said 'volatility of the Sandisk stock price in the period of the exchange'. The note now says volatility 'over the period between exchange and settlement'.","account":"Costs in connection with debt-for-equity exchange","expected_direction":"none","horizon":"this quarter","quote":"a discount to the market price of Sandisk shares provided to the counterparties in connection with the exchange","paragraph_id":"0001628280-26-057139:notes:162","explanation":false},
{"id":"liquidity_and_capital_revolving_credit_facility_drawn_in_june","what_changed":"The revolver now has a drawn balance, with stated remaining capacity of $900 million. The Q3 10-Q stated available capacity of $1.25 billion and no letters of credit. The draw came in the same month as the convertible note settlements (notes:171-173). The facility matures in January 2027.","account":"Current portion of long-term debt","expected_direction":"up","horizon":"this quarter","quote":"In June 2026, the Company drew $450 million in principal amount and repaid $100 million thereunder, with $350 million remaining outstanding as of July 3, 2026.","paragraph_id":"0001628280-26-057139:notes:163","explanation":false},
{"id":"liquidity_and_capital_revolver_maturity_inside_liquidity_horizon","what_changed":"The twelve-month liquidity assertion relies partly on the Revolving Credit Facility. mdna:82 and notes:163 say that facility matures in January 2027, inside the twelve-month window. The prose does not mention renewal or replacement.","account":"Revolving Credit Facility; cash and cash equivalents","expected_direction":"none","horizon":"12 months","quote":"We believe our cash and cash equivalents and our available Revolving Credit Facility will be sufficient to meet our working capital, debt, dividend and capital expenditure needs and fund our share repurchases for at least the next twelve months","paragraph_id":"0001628280-26-057139:mdna:68","explanation":false},
{"id":"liquidity_and_capital_investment_grade_ratings_collateral_released","what_changed":"New: investment-grade ratings were obtained in Q3, and the guarantee and collateral lien on the revolver were released. notes:164 says revolver margins and unused fees depend on the ratings.","account":"Interest expense; Revolving Credit Facility","expected_direction":"down","horizon":"12 months","quote":"During the third quarter of 2026, the Company obtained investment-grade ratings from two rating agencies","paragraph_id":"0001628280-26-057139:notes:183","explanation":false},
{"id":"liquidity_and_capital_convertible_notes_remain_convertible_through_september","what_changed":"The conversion trigger has held every quarter since June 2025. Holders can now convert through September 30, 2026, so the notes stay classified as current.","account":"Current portion of long-term debt","expected_direction":"none","horizon":"next quarter","quote":"which has provided, and continues to provide, the holders of those notes with the right to convert through September 30, 2026","paragraph_id":"0001628280-26-057139:notes:170","explanation":false},
{"id":"liquidity_and_capital_remaining_convertible_notes_expected_cash_settlement","what_changed":"Management now expects the whole remaining principal to be tendered. It expects to settle principal in cash and substantially all of the premium in shares.","account":"Cash and cash equivalents; current portion of long-term debt","expected_direction":"down","horizon":"next quarter","quote":"we believe the remaining $367 million principal amount will likely be tendered in the next few months","paragraph_id":"0001628280-26-057139:mdna:81","explanation":false},
{"id":"liquidity_and_capital_conversion_premium_settled_in_shares","what_changed":"For notes tendered through year-end, the premium is to be settled in shares in Q1 FY2027. This reverses the cash election made on the March Tendered Notes (mdna:14).","account":"Common shares outstanding; diluted shares","expected_direction":"up","horizon":"next quarter","quote":"The Company has elected to issue shares of its common stock to satisfy the conversion obligation in excess of the principal amount for substantially all of these notes, which have settled or are expected to settle in the first quarter of 2027.","paragraph_id":"0001628280-26-057139:notes:174","explanation":false},
{"id":"liquidity_and_capital_cash_election_for_tendered_notes_premium","what_changed":"New: on the March Tendered Notes, management elected to pay the conversion premium in cash instead of issuing shares.","account":"Cash and cash equivalents","expected_direction":"down","horizon":"this quarter","quote":"elected to use an additional $328 million of cash to settle the conversion premium instead of settling the premium with 0.8 million shares of our common stock","paragraph_id":"0001628280-26-057139:mdna:14","explanation":false},
{"id":"earnings_quality_tendered_notes_derivative_remeasurement_cost","what_changed":"The Q3 10-Q (note_history:16) reported an immaterial remeasurement gain on the bifurcated derivative, with settlement scheduled for June. The annual note now records a $106 million fair value recognized as a cost, attributed to the stock's appreciation through settlement.","account":"Costs in connection with convertible notes transactions","expected_direction":"up","horizon":"this quarter","quote":"the derivative instrument was remeasured to a fair value of $106 million and was recognized in Costs in connection with convertible notes transactions","paragraph_id":"0001628280-26-057139:notes:172","explanation":false},
{"id":"liquidity_and_capital_june_exchange_agreements_shares_issued","what_changed":"New: privately negotiated exchanges of the convertible notes were settled partly in newly issued common shares. The 8-K index lists Item 3.02 filings on 2026-06-03 and 2026-06-08 (amendment), consistent with this issuance. Their bodies are not in the input.","account":"Common shares outstanding; convertible notes","expected_direction":"up","horizon":"this quarter","quote":"fully settled the obligation for an aggregate $860 million cash (which reflected principal amount and a small inducement cost) and 21.3 million shares","paragraph_id":"0001628280-26-057139:notes:173","explanation":false},
{"id":"articulation_and_the_filed_history_stated_conversion_premium_value","what_changed":"The note gives a dollar value for the conversion premium settled in shares in the June exchanges. No other paragraph restates the amount. The numbers reader should reconcile it with the share count issued and the equity roll-forward.","account":"Additional paid-in capital; convertible notes","expected_direction":"none","horizon":"this quarter","quote":"for the conversion premium of $12.5 billion","paragraph_id":"0001628280-26-057139:notes:173","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_capped_call_shares_after_year_end","what_changed":"Subsequent event: shares have been or will be received from pro rata capped call settlement on notes tendered after year-end. The note also states the outstanding capped call notional. notes:173 says the capped calls were not settled or modified in the June exchanges.","account":"Treasury stock; shares outstanding","expected_direction":"down","horizon":"next quarter","quote":"the Company has received or will receive additional shares of its common stock in the first quarter of 2027 from the settlement of a pro rata amount of the Capped Calls","paragraph_id":"0001628280-26-057139:notes:177","explanation":false},
{"id":"across_documents_capped_call_benefit_excluded_from_share_guidance","what_changed":"The Q1 FY2027 share guidance now assumes no material capped call benefit. Elsewhere:\n- 8k_2_02:72 and 8k_2_02:87 say non-GAAP diluted shares have included that benefit since Q1 FY2026.\n- notes:177 says capped call shares are being received in Q1 FY2027.\nThe prose does not explain the change.","account":"Non-GAAP diluted weighted average shares","expected_direction":"none","horizon":"next quarter","quote":"Non-GAAP diluted weighted average shares guidance reflects no material benefit expected to be provided by existing capped call transactions","paragraph_id":"0001628280-26-053305:8k_2_02:97","explanation":false},
{"id":"structure_and_disclosure_changes_non_gaap_share_count_includes_capped_call","what_changed":"This non-GAAP method change was made during FY2026, with prior periods revised: non-GAAP diluted shares are reduced for capped call shares. Relative to the prior annual release, the non-GAAP share base is defined differently.","account":"Non-GAAP diluted EPS","expected_direction":"up","horizon":"this quarter","quote":"which include the benefit of shares related to capped call transactions","paragraph_id":"0001628280-26-053305:8k_2_02:72","explanation":false},
{"id":"earnings_quality_non_gaap_excludes_exchange_discount_costs","what_changed":"New non-GAAP exclusion category, 'Costs in connection with debt and equity transactions'. It covers:\n- the debt-for-equity exchange\n- the equity-for-equity exchanges\n- the private convertible-note settlements\nThe costs are described as mainly a discount given to counterparties.","account":"Non-GAAP net income","expected_direction":"none","horizon":"this quarter","quote":"the company recognized costs primarily related to a discount given to the counterparty of the transaction","paragraph_id":"0001628280-26-053305:8k_2_02:82","explanation":false},
{"id":"structure_and_disclosure_changes_preferred_stock_converted_and_eliminated","what_changed":"New: all remaining preferred shares were converted at the company's option, and the series was eliminated on February 24, 2026. The 8-K index lists Item 3.03 on 2026-02-18 and Item 5.03 on 2026-02-24. Allocations to participating securities end.","account":"Convertible preferred stock; amounts allocated to preferred shareholders","expected_direction":"down","horizon":"this quarter","quote":"On February 17, 2026, the Company exercised this option and converted all remaining outstanding Preferred Shares into 7 million shares","paragraph_id":"0001628280-26-057139:notes:323","explanation":false},
{"id":"liquidity_and_capital_share_repurchase_authorization_expanded","what_changed":"The board added a further $4.0 billion of repurchase authorization on February 2, 2026. The note states FY2026 repurchases and $3.26 billion remaining. Funding is expected primarily from operating cash flows.","account":"Shares outstanding; cash","expected_direction":"down","horizon":"12 months","quote":"For the year ended July 3, 2026, the Company repurchased 14.7 million shares for a total cost of $2.59 billion.","paragraph_id":"0001628280-26-057139:notes:327","explanation":false},
{"id":"liquidity_and_capital_cash_premium_election_framed_with_repurchases","what_changed":"New framing: MD&A combines buybacks with the cash settlement of the Tendered Notes premium into one dollar figure and one 'effective' share-impact figure.","account":"Shares outstanding","expected_direction":"none","horizon":"this quarter","quote":"which resulted in an effective impact to our outstanding shares of common stock of approximately 15.5 million shares","paragraph_id":"0001628280-26-057139:mdna:20","explanation":false},
{"id":"earnings_quality_equity_for_equity_exchange_cost","what_changed":"New: two Q4 exchanges of Sandisk shares for the company's own shares produced a cost, described as the difference in fair values at settlement. Both values are stated in the paragraph. The numbers reader should reconcile them with the cost. The cost is excluded from non-GAAP.","account":"Costs in connection with equity-for-equity exchanges","expected_direction":"none","horizon":"this quarter","quote":"The exchanges resulted in $254 million recorded in Costs in connection with equity-for-equity exchanges in the Consolidated Statement of Operations.","paragraph_id":"0001628280-26-057139:notes:328","explanation":false},
{"id":"controls_audit_and_filings_critical_audit_matter_tax_free_exchanges","what_changed":"The tax critical audit matter now covers the February 2026 debt-for-equity exchange and the Q4 equity-for-equity exchanges, in addition to the separation. KPMG describes 'especially subjective auditor judgment'. The prose does not quantify exposure if tax-free treatment failed.","account":"Income tax expense; income taxes payable","expected_direction":"none","horizon":"12 months","quote":"Management determined that the separation, debt-for-equity exchanges and equity-for-equity exchanges (collectively referred to as the Transactions) qualified as tax-free transactions","paragraph_id":"0001628280-26-057139:auditors_report:25","explanation":false},
{"id":"earnings_quality_effective_tax_rate_lowered_by_tax_free_gain","what_changed":"The tax-free Sandisk gain is named as an FY2026 driver of the rate below the statutory rate (also shown in the notes:215 reconciliation line). With the shares disposed, this driver does not recur. The 8-K guides a non-GAAP tax rate of about 17%.","account":"Effective tax rate","expected_direction":"up","horizon":"next quarter","quote":"the gain on the retained interest in Sandisk being tax-free due to the Separation","paragraph_id":"0001628280-26-057139:mdna:51","explanation":false},
{"id":"estimates_and_discretion_tax_legislation_research_expensing","what_changed":"The One Big Beautiful Bill Act is described as allowing immediate domestic R&D expensing from 2026, with FDDEI and GILTI changes effective for the company in 2027.","account":"Income tax expense; cash taxes","expected_direction":"down","horizon":"12 months","quote":"Notably, the new legislation now allows an option for the immediate expensing of domestic R&D expenditures, beginning with 2026.","paragraph_id":"0001628280-26-057139:notes:204","explanation":false},
{"id":"earnings_quality_tax_holiday_benefit_reduced_by_global_minimum_tax","what_changed":"New sentence: the tax holiday benefit was reduced by GMT in Thailand, which first applied in 2026. notes:206 says the company is subject to GMT in Malaysia and Thailand.","account":"Income tax expense (tax holiday benefit)","expected_direction":"down","horizon":"this quarter","quote":"The direct tax impact of these tax holidays and tax incentives amount was reduced for GMT in Thailand, which became applicable for the Company in 2026.","paragraph_id":"0001628280-26-057139:notes:228","explanation":false},
{"id":"estimates_and_discretion_thailand_tax_holiday_expiry","what_changed":"New: a Thailand tax holiday expires August 31, 2026, and extension talks are under way. Reversing deferred taxes are measured at the statutory rate. If an extension is granted, the effective tax rate would be adjusted.","account":"Income tax expense; deferred taxes","expected_direction":"up","horizon":"next quarter","quote":"tax holidays in Thailand is scheduled to expire on August 31, 2026","paragraph_id":"0001628280-26-057139:notes:227","explanation":false},
{"id":"liquidity_and_capital_global_minimum_tax_payment_deferred","what_changed":"New: accrued GMT liabilities are stated, with payment not expected until Q2 fiscal 2028.","account":"Accrued tax liabilities; cash","expected_direction":"none","horizon":"beyond 12 months (Q2 fiscal 2028)","quote":"As of July 3, 2026, we have accrued GMT liabilities of $89 million that are not expected to be paid until the second quarter of 2028.","paragraph_id":"0001628280-26-057139:mdna:103","explanation":false},
{"id":"earnings_quality_deferred_tax_assets_decrease_from_interest_carryforward_use","what_changed":"New explanation: the decrease in deferred tax assets is attributed to use of interest expense carryforwards, including interest from the IRS settlement for 2008-2015 (also notes:241).","account":"Deferred tax assets","expected_direction":"down","horizon":"this quarter","quote":"The decrease in the deferred tax assets is attributable primarily to the utilization of interest expense carryforwards that had been previously deferred due to interest expense limitations.","paragraph_id":"0001628280-26-057139:notes:210","explanation":false},
{"id":"earnings_quality_stock_compensation_tax_windfall","what_changed":"New: FY2026 stock-compensation windfalls are stated, and earlier periods are described as immaterial. notes:217 says the tax provision includes them. Windfalls depend on the stock price at vesting.","account":"Income tax expense","expected_direction":"down","horizon":"this quarter","quote":"As of July 3, 2026, excess windfall tax benefits were $155 million.","paragraph_id":"0001628280-26-057139:notes:303","explanation":false},
{"id":"liquidity_and_capital_unrecognized_tax_benefit_payments_within_twelve_months","what_changed":"A portion of the uncertain-tax-position payables is expected to be paid within twelve months and sits in Income taxes payable. The rest is in Other liabilities.","account":"Income taxes payable; cash","expected_direction":"down","horizon":"12 months","quote":"approximately $349 million, including interest and penalties, could result in potential cash payments to be made within the next twelve months","paragraph_id":"0001628280-26-057139:notes:239","explanation":false},
{"id":"liquidity_and_capital_tax_receivables_netted_against_payments","what_changed":"The expected payments are to be netted against $213 million of favorable tax receivables, held in Other current assets, for a stated net payment of $136 million. notes:244 says no other UTB change within twelve months can be estimated.","account":"Other current assets","expected_direction":"down","horizon":"12 months","quote":"These tax receivables are classified in Other current assets on the Consolidated Balance Sheets as of July 3, 2026.","paragraph_id":"0001628280-26-057139:notes:240","explanation":false},
{"id":"earnings_quality_business_realignment_capacity_project_cancellations","what_changed":"New sentence: FY2026 realignment included cancelling facility projects and impairing construction in progress, described as optimizing capacity to support growth. The 8-K shows Q4 non-cash asset impairment. Realignment is excluded from non-GAAP.","account":"Business realignment charges; property, plant and equipment","expected_direction":"up","horizon":"this quarter","quote":"In 2026, the Company canceled certain facility projects and impaired related construction in progress assets as realigned resources to optimize capacity to support recent growth.","paragraph_id":"0001628280-26-057139:notes:247","explanation":false},
{"id":"across_documents_termination_benefits_alongside_headcount_growth","what_changed":"MD&A cites increased headcount behind higher R&D. notes:247 describes FY2026 realignment as organization rationalization to reduce cost structure, and its table shows cash-based employee termination benefits for 2026. MD&A gives no prose on the 2026 realignment program beyond a cross-reference (mdna:45).","account":"Research and development; business realignment charges","expected_direction":"none","horizon":"this quarter","quote":"$75 million of higher compensation-related costs, reflecting increased headcount and variable compensation aligned with our improved financial performance during the current year","paragraph_id":"0001628280-26-057139:mdna:42","explanation":false},
{"id":"results_against_expectations_cloud_pricing_environment","what_changed":"Cloud ASP growth is attributed to an improved pricing environment.","account":"Revenue, net (Cloud)","expected_direction":"up","horizon":"this quarter","quote":"The increase in ASPs per exabyte was due to an improved pricing environment.","paragraph_id":"0001628280-26-057139:mdna:34","explanation":false},
{"id":"results_against_expectations_client_consumer_explanation_generic","what_changed":"The Client revenue increase is mostly ASP-driven by MD&A's own figures, but it is explained only as 'dynamics largely consistent with our other end markets'. The identical sentence is used for Consumer (mdna:36).","account":"Revenue, net (Client, Consumer)","expected_direction":"none","horizon":"this quarter","quote":"The increase in exabytes sold and ASPs per exabyte were driven by dynamics largely consistent with our other end markets.","paragraph_id":"0001628280-26-057139:mdna:35","explanation":false},
{"id":"revenue_recognition_sales_incentive_programs_share_of_gross_revenue","what_changed":"MD&A states the FY2026 share of gross revenue taken by sales incentive and price protection programs. These programs are the subject of the variable-consideration critical audit matter (auditors_report:16-23).","account":"Revenue, net (variable consideration)","expected_direction":"none","horizon":"this quarter","quote":"For 2026, 2025 and 2024, these programs represented 9%, 10% and 11%, respectively, of gross revenue.","paragraph_id":"0001628280-26-057139:mdna:38","explanation":false},
{"id":"results_against_expectations_gross_margin_drivers","what_changed":"Gross profit growth is attributed to four drivers: volume, cost structure on newer-generation products, mix shift to higher capacity, and pricing.","account":"Gross profit; gross margin","expected_direction":"up","horizon":"this quarter","quote":"The increase was largely due to an increased volume of shipments, a better cost structure on our newer generation products, a mix shift towards higher capacity drives and improved pricing.","paragraph_id":"0001628280-26-057139:mdna:40","explanation":false},
{"id":"results_against_expectations_selling_general_administrative_lower_after_separation","what_changed":"The SG&A decrease is attributed to separation-related costs in the 2025 base.","account":"Selling, general and administrative","expected_direction":"down","horizon":"this quarter","quote":"as 2025 included higher costs associated with the final planning and execution of the Separation","paragraph_id":"0001628280-26-057139:mdna:43","explanation":false},
{"id":"liquidity_and_capital_capital_expenditures_higher_next_year","what_changed":"New expectation: fiscal 2027 capital expenditures will be higher than 2026, for heads and media operations and automation.","account":"Purchases of property, plant and equipment","expected_direction":"up","horizon":"12 months","quote":"For 2027, we expect capital expenditures to be higher than 2026 as we are making the necessary investments in our heads and media operations, as well as in automation to increase our productivity.","paragraph_id":"0001628280-26-057139:mdna:93","explanation":false},
{"id":"liquidity_and_capital_capital_expenditure_range_over_five_years","what_changed":"MD&A states a five-year capital expenditure range as a percentage of revenue.","account":"Purchases of property, plant and equipment","expected_direction":"none","horizon":"12 months and beyond","quote":"Over the next five years, we expect our capital expenditures to average between 4% to 6% of our net revenue.","paragraph_id":"0001628280-26-057139:mdna:67","explanation":false},
{"id":"liquidity_and_capital_taxes_paid_on_vested_stock_awards","what_changed":"Financing uses now include a stated amount of taxes paid on vested stock awards. The same paragraph says bridge-loan and revolver draws partly offset the uses.","account":"Employee stock plans, net (financing cash flow)","expected_direction":"down","horizon":"this quarter","quote":"$376 million for taxes paid on vested stock awards under employee stock plans","paragraph_id":"0001628280-26-057139:mdna:65","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_dividend_declared_after_year_end","what_changed":"Subsequent event: a dividend was declared August 4, 2026, payable September 17, 2026. The 8-K (8k_2_02:27) and MD&A (mdna:17) say the same.","account":"Dividends; cash","expected_direction":"none","horizon":"next quarter","quote":"Subsequent to year-end, on August 4, 2026, the Board of Directors declared a cash dividend of $0.15 per share","paragraph_id":"0001628280-26-057139:notes:334","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_trading_plan_chief_product_officer","what_changed":"New: the EVP and Chief Product Officer adopted a 10b5-1 sale plan for up to 24,000 shares, expiring June 1, 2028.","account":"none","expected_direction":"none","horizon":"12 months","quote":"adopted a Rule 10b5-1 Plan on May 28, 2026","paragraph_id":"0001628280-26-057139:notes:351","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_trading_plan_director","what_changed":"New: director Kimberly Alexy adopted a 10b5-1 sale plan for up to 10,000 shares, expiring December 1, 2027.","account":"none","expected_direction":"none","horizon":"12 months","quote":"adopted a Rule 10b5-1 Plan on May 29, 2026","paragraph_id":"0001628280-26-057139:notes:352","explanation":false},
{"id":"related_parties_contingencies_and_subsequent_events_trading_plan_chief_sales_officer","what_changed":"New: the EVP and Chief Sales and Marketing Officer adopted a 10b5-1 sale plan for up to 31,016 shares, expiring February 16, 2027.","account":"none","expected_direction":"none","horizon":"12 months","quote":"adopted a Rule 10b5-1 Plan on June 5, 2026","paragraph_id":"0001628280-26-057139:notes:353","explanation":false},
{"id":"articulation_and_the_filed_history_litigation_reversal_wording","what_changed":"The Q3 10-Q (note_history:3) gave MRT reversals of $201 million for the three months and $198 million for the nine months ended March 28, 2025. The annual note now gives only the $201 million figure and adds a $6 million reversal of post-judgment interest in Other income (expense), net. The numbers reader should reconcile this with the FY2025 Litigation matter line.","account":"Litigation matter; other income (expense), net","expected_direction":"none","horizon":"this quarter","quote":"the Company reversed $201 million of previously recorded charges in Operating expense under Litigation matter and $6 million of post-judgment interest previously recorded in Other income (expense), net","paragraph_id":"0001628280-26-057139:notes:347","explanation":false},
{"id":"estimates_and_discretion_hedge_amounts_not_reclassified","what_changed":"New sentence: nothing was reclassified out of AOCI in 2026. notes:76 says all FX contract maturities are 12 months or less, and notes:77 says deferred amounts are recognized in earnings when the hedged cash flows are. The prose does not say why no reclassification occurred.","account":"Accumulated other comprehensive income (loss); cost of revenue","expected_direction":"none","horizon":"this quarter","quote":"There were no amounts reclassified out of Accumulated other comprehensive income (loss) during 2026.","paragraph_id":"0001628280-26-057139:notes:141","explanation":false}
]
```

Item count: 67. Items marked as a management explanation (`explanation: true`): 2. One covers receivables (mdna:61), the other inventory (mdna:61).

## Paragraphs not made an item

Prefixes:
- notes / mdna / auditors_report / item_9a: `0001628280-26-057139:`
- 8-K: `0001628280-26-053305:`

### Notes

- 0001628280-26-057139:notes:1: boilerplate, proxy incorporation date rolled forward
- 0001628280-26-057139:notes:2: insufficient, cybersecurity boilerplate with no prior text carried
- 0001628280-26-057139:notes:3: insufficient, cybersecurity boilerplate
- 0001628280-26-057139:notes:4: insufficient, cybersecurity boilerplate
- 0001628280-26-057139:notes:5: insufficient, cybersecurity boilerplate
- 0001628280-26-057139:notes:6: insufficient, cybersecurity boilerplate
- 0001628280-26-057139:notes:7: insufficient, cybersecurity boilerplate
- 0001628280-26-057139:notes:8: insufficient, standing past-incident language
- 0001628280-26-057139:notes:9: insufficient, cybersecurity governance boilerplate
- 0001628280-26-057139:notes:10: insufficient, CISO description
- 0001628280-26-057139:notes:11: insufficient, governance boilerplate
- 0001628280-26-057139:notes:12: insufficient, governance boilerplate
- 0001628280-26-057139:notes:13: wording only, per note history
- 0001628280-26-057139:notes:14: wording only, quotation marks added
- 0001628280-26-057139:notes:15: heading
- 0001628280-26-057139:notes:16: boilerplate
- 0001628280-26-057139:notes:17: boilerplate, continuing operations basis
- 0001628280-26-057139:notes:18: heading
- 0001628280-26-057139:notes:20: heading
- 0001628280-26-057139:notes:21: carried from separation-year text
- 0001628280-26-057139:notes:22: heading
- 0001628280-26-057139:notes:23: boilerplate
- 0001628280-26-057139:notes:24: heading
- 0001628280-26-057139:notes:26: heading
- 0001628280-26-057139:notes:27: insufficient, tariff wording likely carried
- 0001628280-26-057139:notes:28: heading
- 0001628280-26-057139:notes:29: boilerplate
- 0001628280-26-057139:notes:30: heading
- 0001628280-26-057139:notes:31: boilerplate
- 0001628280-26-057139:notes:32: wording in past tense after disposal, covered by notes:119 item
- 0001628280-26-057139:notes:33: heading
- 0001628280-26-057139:notes:34: boilerplate
- 0001628280-26-057139:notes:35: heading
- 0001628280-26-057139:notes:36: boilerplate
- 0001628280-26-057139:notes:37: boilerplate
- 0001628280-26-057139:notes:38: heading
- 0001628280-26-057139:notes:39: boilerplate
- 0001628280-26-057139:notes:40: heading
- 0001628280-26-057139:notes:41: amounts only, no impairment, date rolled forward
- 0001628280-26-057139:notes:42: boilerplate
- 0001628280-26-057139:notes:43: amounts only, no impairment
- 0001628280-26-057139:notes:44: boilerplate
- 0001628280-26-057139:notes:45: heading
- 0001628280-26-057139:notes:46: boilerplate
- 0001628280-26-057139:notes:47: boilerplate
- 0001628280-26-057139:notes:48: boilerplate
- 0001628280-26-057139:notes:49: date rolled forward, used in mdna:8 cross-document item
- 0001628280-26-057139:notes:50: date rolled forward, used in mdna:8 cross-document item
- 0001628280-26-057139:notes:51: insufficient, payment-terms sentence with no baseline, cited in AR item
- 0001628280-26-057139:notes:52: boilerplate
- 0001628280-26-057139:notes:53: boilerplate
- 0001628280-26-057139:notes:54: boilerplate
- 0001628280-26-057139:notes:55: boilerplate
- 0001628280-26-057139:notes:56: boilerplate
- 0001628280-26-057139:notes:57: heading
- 0001628280-26-057139:notes:58: boilerplate warranty policy
- 0001628280-26-057139:notes:59: heading
- 0001628280-26-057139:notes:60: boilerplate
- 0001628280-26-057139:notes:61: heading
- 0001628280-26-057139:notes:62: amounts only
- 0001628280-26-057139:notes:63: heading
- 0001628280-26-057139:notes:64: boilerplate
- 0001628280-26-057139:notes:65: heading
- 0001628280-26-057139:notes:66: boilerplate
- 0001628280-26-057139:notes:67: boilerplate
- 0001628280-26-057139:notes:68: heading
- 0001628280-26-057139:notes:69: past tense after preferred conversion, covered by notes:323 item
- 0001628280-26-057139:notes:70: boilerplate
- 0001628280-26-057139:notes:71: heading
- 0001628280-26-057139:notes:72: boilerplate
- 0001628280-26-057139:notes:73: heading
- 0001628280-26-057139:notes:74: boilerplate
- 0001628280-26-057139:notes:75: heading
- 0001628280-26-057139:notes:76: amounts only, notional; cited in notes:141 item
- 0001628280-26-057139:notes:77: boilerplate, cited in notes:141 item
- 0001628280-26-057139:notes:78: boilerplate
- 0001628280-26-057139:notes:79: heading
- 0001628280-26-057139:notes:80: boilerplate
- 0001628280-26-057139:notes:81: boilerplate
- 0001628280-26-057139:notes:82: heading
- 0001628280-26-057139:notes:83: boilerplate
- 0001628280-26-057139:notes:84: heading
- 0001628280-26-057139:notes:87: heading
- 0001628280-26-057139:notes:88: new standard listed, impact being assessed, no company effect stated
- 0001628280-26-057139:notes:89: new standard listed, impact being assessed
- 0001628280-26-057139:notes:90: new standard listed, impact being assessed
- 0001628280-26-057139:notes:91: new standard listed, no material impact expected
- 0001628280-26-057139:notes:92: new standard listed, impact being assessed
- 0001628280-26-057139:notes:93: continuation of notes:92
- 0001628280-26-057139:notes:94: standard listed, adoption date only
- 0001628280-26-057139:notes:95: heading and table intro
- 0001628280-26-057139:notes:96: table, amounts only
- 0001628280-26-057139:notes:97: boilerplate
- 0001628280-26-057139:notes:98: table, amounts only
- 0001628280-26-057139:notes:99: footnote boilerplate
- 0001628280-26-057139:notes:100: table, amounts only
- 0001628280-26-057139:notes:101: footnote boilerplate
- 0001628280-26-057139:notes:102: heading
- 0001628280-26-057139:notes:105: boilerplate
- 0001628280-26-057139:notes:106: boilerplate segment text
- 0001628280-26-057139:notes:107: table intro
- 0001628280-26-057139:notes:108: table, amounts only
- 0001628280-26-057139:notes:109: footnote boilerplate
- 0001628280-26-057139:notes:110: footnote boilerplate
- 0001628280-26-057139:notes:111: heading
- 0001628280-26-057139:notes:112: boilerplate
- 0001628280-26-057139:notes:113: carried from prior year, separation
- 0001628280-26-057139:notes:114: table intro
- 0001628280-26-057139:notes:115: table, prior-year amounts only
- 0001628280-26-057139:notes:116: boilerplate
- 0001628280-26-057139:notes:117: table, prior-year amounts only
- 0001628280-26-057139:notes:118: covered by notes:119 and notes:162 items
- 0001628280-26-057139:notes:120: carried from prior year
- 0001628280-26-057139:notes:121: carried from prior year
- 0001628280-26-057139:notes:122: carried from prior year
- 0001628280-26-057139:notes:123: table intro fragment
- 0001628280-26-057139:notes:124: heading
- 0001628280-26-057139:notes:125: table, amounts only
- 0001628280-26-057139:notes:126: heading
- 0001628280-26-057139:notes:127: table, amounts only
- 0001628280-26-057139:notes:128: amounts only, recurring sentence
- 0001628280-26-057139:notes:129: heading
- 0001628280-26-057139:notes:130: table, amounts only
- 0001628280-26-057139:notes:131: heading
- 0001628280-26-057139:notes:132: table intro
- 0001628280-26-057139:notes:133: table, amounts only
- 0001628280-26-057139:notes:134: boilerplate
- 0001628280-26-057139:notes:135: table, amounts only
- 0001628280-26-057139:notes:136: heading
- 0001628280-26-057139:notes:137: table, amounts only
- 0001628280-26-057139:notes:138: heading
- 0001628280-26-057139:notes:139: boilerplate
- 0001628280-26-057139:notes:140: table, amounts only
- 0001628280-26-057139:notes:142: heading
- 0001628280-26-057139:notes:143: boilerplate
- 0001628280-26-057139:notes:144: boilerplate
- 0001628280-26-057139:notes:145: boilerplate
- 0001628280-26-057139:notes:146: boilerplate
- 0001628280-26-057139:notes:147: wording reflects disposal, covered by notes:119 item
- 0001628280-26-057139:notes:148: table intro
- 0001628280-26-057139:notes:149: table, amounts only
- 0001628280-26-057139:notes:150: table, amounts only
- 0001628280-26-057139:notes:151: duplicates notes:119 item content
- 0001628280-26-057139:notes:152: boilerplate
- 0001628280-26-057139:notes:153: boilerplate
- 0001628280-26-057139:notes:154: boilerplate
- 0001628280-26-057139:notes:155: heading
- 0001628280-26-057139:notes:156: boilerplate, date rolled forward
- 0001628280-26-057139:notes:157: table, amounts only
- 0001628280-26-057139:notes:158: heading
- 0001628280-26-057139:notes:159: table, revolver line covered by notes:163 item
- 0001628280-26-057139:notes:160: heading
- 0001628280-26-057139:notes:161: carried from prior year
- 0001628280-26-057139:notes:164: terms carried, rate amounts only
- 0001628280-26-057139:notes:165: compliance statement rolled forward
- 0001628280-26-057139:notes:166: boilerplate
- 0001628280-26-057139:notes:167: heading
- 0001628280-26-057139:notes:168: amounts only
- 0001628280-26-057139:notes:169: reordered; conversion price unchanged from Q3
- 0001628280-26-057139:notes:171: covered by mdna:14 and notes:172 items
- 0001628280-26-057139:notes:175: carried from Q3
- 0001628280-26-057139:notes:176: heading
- 0001628280-26-057139:notes:178: heading
- 0001628280-26-057139:notes:179: covered by notes:162 item
- 0001628280-26-057139:notes:180: covered by notes:162 item
- 0001628280-26-057139:notes:181: heading
- 0001628280-26-057139:notes:182: historical description, covered by notes:183 item
- 0001628280-26-057139:notes:184: boilerplate
- 0001628280-26-057139:notes:185: heading
- 0001628280-26-057139:notes:186: boilerplate, duplicates notes:83
- 0001628280-26-057139:notes:187: table intro
- 0001628280-26-057139:notes:188: table, amounts only
- 0001628280-26-057139:notes:189: table intro
- 0001628280-26-057139:notes:190: table, amounts only
- 0001628280-26-057139:notes:191: table intro
- 0001628280-26-057139:notes:192: table, amounts only
- 0001628280-26-057139:notes:193: table intro
- 0001628280-26-057139:notes:194: table, amounts only
- 0001628280-26-057139:notes:195: heading
- 0001628280-26-057139:notes:196: boilerplate
- 0001628280-26-057139:notes:197: table, amounts only
- 0001628280-26-057139:notes:198: heading
- 0001628280-26-057139:notes:199: table intro
- 0001628280-26-057139:notes:200: table, amounts only
- 0001628280-26-057139:notes:201: heading
- 0001628280-26-057139:notes:202: table intro
- 0001628280-26-057139:notes:203: table, amounts only
- 0001628280-26-057139:notes:205: date rolled forward (CAMT not applicable in 2026)
- 0001628280-26-057139:notes:206: covered by notes:228 item
- 0001628280-26-057139:notes:207: heading
- 0001628280-26-057139:notes:208: table intro
- 0001628280-26-057139:notes:209: table, amounts only
- 0001628280-26-057139:notes:211: boilerplate
- 0001628280-26-057139:notes:212: boilerplate
- 0001628280-26-057139:notes:213: heading
- 0001628280-26-057139:notes:214: table intro, covered by notes:85 item
- 0001628280-26-057139:notes:215: table, amounts only
- 0001628280-26-057139:notes:216: new required footnote, covered by notes:85 item
- 0001628280-26-057139:notes:217: covered by notes:303 item
- 0001628280-26-057139:notes:218: footnote boilerplate
- 0001628280-26-057139:notes:219: new required table intro, covered by notes:85 item
- 0001628280-26-057139:notes:220: table, amounts only
- 0001628280-26-057139:notes:221: table intro
- 0001628280-26-057139:notes:222: table, prior-year amounts only
- 0001628280-26-057139:notes:223: carried
- 0001628280-26-057139:notes:224: heading
- 0001628280-26-057139:notes:225: date rolled forward, covered by notes:227 item
- 0001628280-26-057139:notes:226: carried (Malaysia holiday expired 2023)
- 0001628280-26-057139:notes:229: heading
- 0001628280-26-057139:notes:230: boilerplate
- 0001628280-26-057139:notes:231: table, amounts only
- 0001628280-26-057139:notes:232: amounts only
- 0001628280-26-057139:notes:233: boilerplate
- 0001628280-26-057139:notes:234: table, amounts only
- 0001628280-26-057139:notes:235: heading
- 0001628280-26-057139:notes:236: boilerplate
- 0001628280-26-057139:notes:237: table intro
- 0001628280-26-057139:notes:238: table, amounts only
- 0001628280-26-057139:notes:241: amounts updated, covered by notes:210 item
- 0001628280-26-057139:notes:242: date rolled forward
- 0001628280-26-057139:notes:243: table, dates rolled forward
- 0001628280-26-057139:notes:244: covered by notes:240 item
- 0001628280-26-057139:notes:245: table intro fragment
- 0001628280-26-057139:notes:246: table intro fragment
- 0001628280-26-057139:notes:248: table intro
- 0001628280-26-057139:notes:249: table, amounts only
- 0001628280-26-057139:notes:250: table intro
- 0001628280-26-057139:notes:251: table, amounts only
- 0001628280-26-057139:notes:252: carried pension description
- 0001628280-26-057139:notes:253: heading
- 0001628280-26-057139:notes:254: table intro
- 0001628280-26-057139:notes:255: table, amounts only
- 0001628280-26-057139:notes:256: table intro
- 0001628280-26-057139:notes:257: table, amounts only
- 0001628280-26-057139:notes:258: amounts only
- 0001628280-26-057139:notes:259: boilerplate, not material
- 0001628280-26-057139:notes:260: heading
- 0001628280-26-057139:notes:261: heading
- 0001628280-26-057139:notes:262: table intro
- 0001628280-26-057139:notes:263: table, amounts only
- 0001628280-26-057139:notes:264: table intro
- 0001628280-26-057139:notes:265: table, amounts only
- 0001628280-26-057139:notes:266: boilerplate
- 0001628280-26-057139:notes:267: boilerplate
- 0001628280-26-057139:notes:268: boilerplate
- 0001628280-26-057139:notes:269: heading
- 0001628280-26-057139:notes:270: heading
- 0001628280-26-057139:notes:271: boilerplate
- 0001628280-26-057139:notes:272: boilerplate
- 0001628280-26-057139:notes:273: heading
- 0001628280-26-057139:notes:274: table intro
- 0001628280-26-057139:notes:275: table, amounts only
- 0001628280-26-057139:notes:276: table, amounts only
- 0001628280-26-057139:notes:277: footnote boilerplate
- 0001628280-26-057139:notes:278: footnote boilerplate
- 0001628280-26-057139:notes:279: footnote boilerplate
- 0001628280-26-057139:notes:280: boilerplate
- 0001628280-26-057139:notes:281: heading
- 0001628280-26-057139:notes:282: boilerplate
- 0001628280-26-057139:notes:283: boilerplate
- 0001628280-26-057139:notes:284: boilerplate
- 0001628280-26-057139:notes:285: heading
- 0001628280-26-057139:notes:286: boilerplate, not material
- 0001628280-26-057139:notes:287: boilerplate
- 0001628280-26-057139:notes:288: boilerplate
- 0001628280-26-057139:notes:289: amounts only
- 0001628280-26-057139:notes:290: heading
- 0001628280-26-057139:notes:291: boilerplate
- 0001628280-26-057139:notes:292: boilerplate
- 0001628280-26-057139:notes:293: insufficient, authorized share count with no baseline
- 0001628280-26-057139:notes:294: heading
- 0001628280-26-057139:notes:295: boilerplate
- 0001628280-26-057139:notes:296: amounts only
- 0001628280-26-057139:notes:297: boilerplate
- 0001628280-26-057139:notes:298: heading
- 0001628280-26-057139:notes:299: carried from prior year
- 0001628280-26-057139:notes:300: table intro
- 0001628280-26-057139:notes:301: table, amounts only
- 0001628280-26-057139:notes:302: table, amounts only
- 0001628280-26-057139:notes:304: boilerplate, table intro
- 0001628280-26-057139:notes:305: table, amounts only
- 0001628280-26-057139:notes:306: footnote boilerplate
- 0001628280-26-057139:notes:307: heading
- 0001628280-26-057139:notes:308: heading
- 0001628280-26-057139:notes:309: table intro
- 0001628280-26-057139:notes:310: table, amounts only
- 0001628280-26-057139:notes:311: boilerplate
- 0001628280-26-057139:notes:312: heading
- 0001628280-26-057139:notes:313: heading
- 0001628280-26-057139:notes:314: boilerplate
- 0001628280-26-057139:notes:315: heading
- 0001628280-26-057139:notes:316: boilerplate
- 0001628280-26-057139:notes:317: table intro
- 0001628280-26-057139:notes:318: table, amounts only
- 0001628280-26-057139:notes:319: heading
- 0001628280-26-057139:notes:320: amounts only
- 0001628280-26-057139:notes:321: heading
- 0001628280-26-057139:notes:322: carried history
- 0001628280-26-057139:notes:324: amounts only, covered by notes:323 item
- 0001628280-26-057139:notes:325: carried from prior year
- 0001628280-26-057139:notes:326: heading
- 0001628280-26-057139:notes:329: heading
- 0001628280-26-057139:notes:330: table intro
- 0001628280-26-057139:notes:331: table, amounts only
- 0001628280-26-057139:notes:332: heading
- 0001628280-26-057139:notes:333: amounts only, recurring sentence
- 0001628280-26-057139:notes:335: boilerplate
- 0001628280-26-057139:notes:336: heading and table intro
- 0001628280-26-057139:notes:337: table, amounts only
- 0001628280-26-057139:notes:338: footnote, covered by notes:323 item
- 0001628280-26-057139:notes:339: boilerplate
- 0001628280-26-057139:notes:340: boilerplate
- 0001628280-26-057139:notes:341: boilerplate
- 0001628280-26-057139:notes:342: insufficient, terms with no baseline, cited in AP item
- 0001628280-26-057139:notes:343: amounts only, cited in AP item
- 0001628280-26-057139:notes:344: table, amounts only
- 0001628280-26-057139:notes:345: heading
- 0001628280-26-057139:notes:346: date rolled forward (SPEX unchanged from Q3)
- 0001628280-26-057139:notes:348: heading
- 0001628280-26-057139:notes:349: boilerplate
- 0001628280-26-057139:notes:350: boilerplate

### MD&A

- 0001628280-26-057139:mdna:1: heading
- 0001628280-26-057139:mdna:2: heading
- 0001628280-26-057139:mdna:3: wording only
- 0001628280-26-057139:mdna:4: wording only
- 0001628280-26-057139:mdna:5: duplicates notes:19 item
- 0001628280-26-057139:mdna:6: heading
- 0001628280-26-057139:mdna:7: heading
- 0001628280-26-057139:mdna:9: heading
- 0001628280-26-057139:mdna:10: duplicates notes:119 and notes:328 items
- 0001628280-26-057139:mdna:11: heading
- 0001628280-26-057139:mdna:12: wording only
- 0001628280-26-057139:mdna:13: duplicates notes:323 item
- 0001628280-26-057139:mdna:15: duplicates notes:173 item
- 0001628280-26-057139:mdna:16: amounts only, duplicates notes:333
- 0001628280-26-057139:mdna:17: duplicates notes:334 item
- 0001628280-26-057139:mdna:18: page number
- 0001628280-26-057139:mdna:19: duplicates notes:327 item
- 0001628280-26-057139:mdna:21: cross-reference
- 0001628280-26-057139:mdna:22: page number
- 0001628280-26-057139:mdna:23: heading
- 0001628280-26-057139:mdna:24: boilerplate
- 0001628280-26-057139:mdna:25: heading
- 0001628280-26-057139:mdna:26: table intro
- 0001628280-26-057139:mdna:27: table, amounts only
- 0001628280-26-057139:mdna:28: footnote boilerplate
- 0001628280-26-057139:mdna:29: table intro
- 0001628280-26-057139:mdna:30: table, amounts only
- 0001628280-26-057139:mdna:31: footnote boilerplate
- 0001628280-26-057139:mdna:32: heading
- 0001628280-26-057139:mdna:36: same sentence as mdna:35, covered by that item
- 0001628280-26-057139:mdna:37: duplicates notes:103 item
- 0001628280-26-057139:mdna:39: heading
- 0001628280-26-057139:mdna:41: heading
- 0001628280-26-057139:mdna:44: cross-reference
- 0001628280-26-057139:mdna:45: cross-reference, cited in mdna:42 item
- 0001628280-26-057139:mdna:46: heading
- 0001628280-26-057139:mdna:48: heading
- 0001628280-26-057139:mdna:49: table intro
- 0001628280-26-057139:mdna:50: table, amounts only
- 0001628280-26-057139:mdna:52: prior-year explanation carried
- 0001628280-26-057139:mdna:53: page number
- 0001628280-26-057139:mdna:54: cross-reference
- 0001628280-26-057139:mdna:55: cross-reference
- 0001628280-26-057139:mdna:56: page number
- 0001628280-26-057139:mdna:57: heading
- 0001628280-26-057139:mdna:58: boilerplate
- 0001628280-26-057139:mdna:59: table, amounts only
- 0001628280-26-057139:mdna:60: heading
- 0001628280-26-057139:mdna:62: heading
- 0001628280-26-057139:mdna:63: amounts only
- 0001628280-26-057139:mdna:64: heading
- 0001628280-26-057139:mdna:66: carried (shelf expires 2027)
- 0001628280-26-057139:mdna:69: amounts only
- 0001628280-26-057139:mdna:70: boilerplate
- 0001628280-26-057139:mdna:71: cross-reference
- 0001628280-26-057139:mdna:72: heading
- 0001628280-26-057139:mdna:73: boilerplate
- 0001628280-26-057139:mdna:74: page number
- 0001628280-26-057139:mdna:75: heading
- 0001628280-26-057139:mdna:76: heading
- 0001628280-26-057139:mdna:77: boilerplate
- 0001628280-26-057139:mdna:78: table, amounts only
- 0001628280-26-057139:mdna:79: heading
- 0001628280-26-057139:mdna:80: wording only, cross-reference
- 0001628280-26-057139:mdna:82: duplicates notes:163 item
- 0001628280-26-057139:mdna:83: boilerplate
- 0001628280-26-057139:mdna:84: boilerplate
- 0001628280-26-057139:mdna:85: boilerplate
- 0001628280-26-057139:mdna:86: table intro
- 0001628280-26-057139:mdna:87: table, amounts only
- 0001628280-26-057139:mdna:88: table intro
- 0001628280-26-057139:mdna:89: table, amounts only
- 0001628280-26-057139:mdna:90: table intro
- 0001628280-26-057139:mdna:91: table, amounts only
- 0001628280-26-057139:mdna:92: heading
- 0001628280-26-057139:mdna:94: boilerplate
- 0001628280-26-057139:mdna:95: heading
- 0001628280-26-057139:mdna:96: cross-reference
- 0001628280-26-057139:mdna:97: heading
- 0001628280-26-057139:mdna:98: duplicates notes:327 item
- 0001628280-26-057139:mdna:99: heading
- 0001628280-26-057139:mdna:100: duplicates notes:239 and notes:240 items
- 0001628280-26-057139:mdna:101: duplicates notes:241, covered by notes:210 item
- 0001628280-26-057139:mdna:102: heading
- 0001628280-26-057139:mdna:104: heading
- 0001628280-26-057139:mdna:105: boilerplate
- 0001628280-26-057139:mdna:106: heading
- 0001628280-26-057139:mdna:107: cross-reference
- 0001628280-26-057139:mdna:108: heading
- 0001628280-26-057139:mdna:109: boilerplate
- 0001628280-26-057139:mdna:110: boilerplate
- 0001628280-26-057139:mdna:111: heading
- 0001628280-26-057139:mdna:112: cross-reference
- 0001628280-26-057139:mdna:113: heading
- 0001628280-26-057139:mdna:114: boilerplate
- 0001628280-26-057139:mdna:115: heading
- 0001628280-26-057139:mdna:116: boilerplate, duplicates notes:52
- 0001628280-26-057139:mdna:117: boilerplate, duplicates notes:53
- 0001628280-26-057139:mdna:118: heading
- 0001628280-26-057139:mdna:119: boilerplate
- 0001628280-26-057139:mdna:120: boilerplate
- 0001628280-26-057139:mdna:121: heading
- 0001628280-26-057139:mdna:122: boilerplate
- 0001628280-26-057139:mdna:123: boilerplate
- 0001628280-26-057139:mdna:124: page number
- 0001628280-26-057139:mdna:125: heading
- 0001628280-26-057139:mdna:126: boilerplate
- 0001628280-26-057139:mdna:127: page number

### Auditor's report

- 0001628280-26-057139:auditors_report:1: heading
- 0001628280-26-057139:auditors_report:2: heading
- 0001628280-26-057139:auditors_report:3: heading
- 0001628280-26-057139:auditors_report:4: heading
- 0001628280-26-057139:auditors_report:5: boilerplate, dates rolled forward
- 0001628280-26-057139:auditors_report:6: unqualified opinions, dates rolled forward
- 0001628280-26-057139:auditors_report:7: heading
- 0001628280-26-057139:auditors_report:8: boilerplate
- 0001628280-26-057139:auditors_report:9: boilerplate
- 0001628280-26-057139:auditors_report:10: boilerplate
- 0001628280-26-057139:auditors_report:11: heading
- 0001628280-26-057139:auditors_report:12: boilerplate
- 0001628280-26-057139:auditors_report:13: boilerplate
- 0001628280-26-057139:auditors_report:14: heading
- 0001628280-26-057139:auditors_report:15: boilerplate
- 0001628280-26-057139:auditors_report:16: insufficient, standing variable-consideration CAM with no prior report carried
- 0001628280-26-057139:auditors_report:17: insufficient, standing CAM
- 0001628280-26-057139:auditors_report:18: insufficient, standing CAM
- 0001628280-26-057139:auditors_report:19: boilerplate
- 0001628280-26-057139:auditors_report:20: insufficient, standing CAM procedure
- 0001628280-26-057139:auditors_report:21: insufficient, standing CAM procedure
- 0001628280-26-057139:auditors_report:22: insufficient, standing CAM procedure
- 0001628280-26-057139:auditors_report:23: insufficient, standing CAM procedure
- 0001628280-26-057139:auditors_report:24: heading of CAM, covered by auditors_report:25 item
- 0001628280-26-057139:auditors_report:26: covered by auditors_report:25 item
- 0001628280-26-057139:auditors_report:27: boilerplate
- 0001628280-26-057139:auditors_report:28: covered by auditors_report:25 item
- 0001628280-26-057139:auditors_report:29: covered by auditors_report:25 item
- 0001628280-26-057139:auditors_report:30: signature, KPMG unchanged
- 0001628280-26-057139:auditors_report:31: tenure statement
- 0001628280-26-057139:auditors_report:32: location
- 0001628280-26-057139:auditors_report:33: date rolled forward
- 0001628280-26-057139:auditors_report:34: heading

### Item 9A

- 0001628280-26-057139:item_9a:1: heading
- 0001628280-26-057139:item_9a:2: heading
- 0001628280-26-057139:item_9a:3: boilerplate
- 0001628280-26-057139:item_9a:4: disclosure controls effective, no change in conclusion
- 0001628280-26-057139:item_9a:5: heading
- 0001628280-26-057139:item_9a:6: boilerplate
- 0001628280-26-057139:item_9a:7: ICFR effective, no change in conclusion
- 0001628280-26-057139:item_9a:8: heading
- 0001628280-26-057139:item_9a:9: no change in ICFR, date rolled forward
- 0001628280-26-057139:item_9a:10: heading
- 0001628280-26-057139:item_9a:11: boilerplate
- 0001628280-26-057139:item_9a:12: page number

### 8-K, Item 2.02 press release

- 0001628280-26-053305:8k_2_02:1: exhibit header
- 0001628280-26-053305:8k_2_02:2: exhibit header
- 0001628280-26-053305:8k_2_02:3: exhibit header
- 0001628280-26-053305:8k_2_02:4: title
- 0001628280-26-053305:8k_2_02:5: heading
- 0001628280-26-053305:8k_2_02:6: results amounts only
- 0001628280-26-053305:8k_2_02:7: results amounts only
- 0001628280-26-053305:8k_2_02:8: results amounts only
- 0001628280-26-053305:8k_2_02:9: results amounts only
- 0001628280-26-053305:8k_2_02:11: dateline
- 0001628280-26-053305:8k_2_02:13: page number
- 0001628280-26-053305:8k_2_02:14: title
- 0001628280-26-053305:8k_2_02:15: heading
- 0001628280-26-053305:8k_2_02:16: table, amounts only
- 0001628280-26-053305:8k_2_02:17: table, amounts only
- 0001628280-26-053305:8k_2_02:18: heading
- 0001628280-26-053305:8k_2_02:19: table, amounts only
- 0001628280-26-053305:8k_2_02:20: page number
- 0001628280-26-053305:8k_2_02:21: title
- 0001628280-26-053305:8k_2_02:22: heading
- 0001628280-26-053305:8k_2_02:24: guidance table amounts, covered by 8k_2_02:23 item
- 0001628280-26-053305:8k_2_02:25: boilerplate
- 0001628280-26-053305:8k_2_02:26: heading
- 0001628280-26-053305:8k_2_02:27: duplicates notes:334 item
- 0001628280-26-053305:8k_2_02:28: heading
- 0001628280-26-053305:8k_2_02:29: call logistics
- 0001628280-26-053305:8k_2_02:30: heading
- 0001628280-26-053305:8k_2_02:31: boilerplate
- 0001628280-26-053305:8k_2_02:32: page number
- 0001628280-26-053305:8k_2_02:33: title
- 0001628280-26-053305:8k_2_02:34: heading
- 0001628280-26-053305:8k_2_02:35: carried, separation
- 0001628280-26-053305:8k_2_02:36: carried, separation
- 0001628280-26-053305:8k_2_02:37: heading
- 0001628280-26-053305:8k_2_02:38: insufficient, forward-looking statements body is a placeholder
- 0001628280-26-053305:8k_2_02:39: boilerplate
- 0001628280-26-053305:8k_2_02:40: page number
- 0001628280-26-053305:8k_2_02:41: heading
- 0001628280-26-053305:8k_2_02:42: heading
- 0001628280-26-053305:8k_2_02:43: heading
- 0001628280-26-053305:8k_2_02:44: table, amounts only
- 0001628280-26-053305:8k_2_02:45: page number
- 0001628280-26-053305:8k_2_02:46: heading
- 0001628280-26-053305:8k_2_02:47: heading
- 0001628280-26-053305:8k_2_02:48: heading
- 0001628280-26-053305:8k_2_02:49: table, amounts only
- 0001628280-26-053305:8k_2_02:50: footnote, covered by notes:323 item
- 0001628280-26-053305:8k_2_02:51: page number
- 0001628280-26-053305:8k_2_02:52: heading
- 0001628280-26-053305:8k_2_02:53: heading
- 0001628280-26-053305:8k_2_02:54: heading
- 0001628280-26-053305:8k_2_02:55: table, amounts only
- 0001628280-26-053305:8k_2_02:56: page number
- 0001628280-26-053305:8k_2_02:57: heading
- 0001628280-26-053305:8k_2_02:58: heading
- 0001628280-26-053305:8k_2_02:59: heading
- 0001628280-26-053305:8k_2_02:60: table, amounts only
- 0001628280-26-053305:8k_2_02:61: page number
- 0001628280-26-053305:8k_2_02:62: heading
- 0001628280-26-053305:8k_2_02:63: heading
- 0001628280-26-053305:8k_2_02:64: heading
- 0001628280-26-053305:8k_2_02:65: table, amounts only
- 0001628280-26-053305:8k_2_02:66: page number
- 0001628280-26-053305:8k_2_02:67: heading
- 0001628280-26-053305:8k_2_02:68: heading
- 0001628280-26-053305:8k_2_02:69: heading
- 0001628280-26-053305:8k_2_02:70: table, amounts only
- 0001628280-26-053305:8k_2_02:71: footnote boilerplate
- 0001628280-26-053305:8k_2_02:73: carried footnote
- 0001628280-26-053305:8k_2_02:74: page number
- 0001628280-26-053305:8k_2_02:75: heading
- 0001628280-26-053305:8k_2_02:76: boilerplate, exclusion list covered by 8k_2_02:82 item
- 0001628280-26-053305:8k_2_02:77: boilerplate
- 0001628280-26-053305:8k_2_02:78: boilerplate
- 0001628280-26-053305:8k_2_02:79: carried
- 0001628280-26-053305:8k_2_02:80: boilerplate
- 0001628280-26-053305:8k_2_02:81: covered by mdna:47 Sandisk gain item
- 0001628280-26-053305:8k_2_02:83: page number
- 0001628280-26-053305:8k_2_02:84: boilerplate
- 0001628280-26-053305:8k_2_02:85: boilerplate
- 0001628280-26-053305:8k_2_02:86: boilerplate
- 0001628280-26-053305:8k_2_02:87: duplicates 8k_2_02:72 item
- 0001628280-26-053305:8k_2_02:88: carried definition
- 0001628280-26-053305:8k_2_02:89: page number
- 0001628280-26-053305:8k_2_02:90: heading
- 0001628280-26-053305:8k_2_02:91: boilerplate
- 0001628280-26-053305:8k_2_02:92: boilerplate
- 0001628280-26-053305:8k_2_02:93: guidance adjustment amounts only
- 0001628280-26-053305:8k_2_02:94: guidance adjustment amounts only
- 0001628280-26-053305:8k_2_02:95: guidance adjustment amounts only
- 0001628280-26-053305:8k_2_02:96: boilerplate
- 0001628280-26-053305:8k_2_02:98: boilerplate
- 0001628280-26-053305:8k_2_02:99: separator
- 0001628280-26-053305:8k_2_02:100: contacts
- 0001628280-26-053305:8k_2_02:101: contacts
- 0001628280-26-053305:8k_2_02:102: contacts
- 0001628280-26-053305:8k_2_02:103: page number
