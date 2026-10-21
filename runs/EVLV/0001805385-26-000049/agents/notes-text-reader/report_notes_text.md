# EVLV — notes / text reader — 10-Q 0001805385-26-000049 (period ended June 30, 2026), prior period of same kind 0001805385-26-000028

## Scope of input

- Read in full: input_notes.md, input_notes_history.md, input_mdna.md, input_controls.md (Item 4 only), input_8k.md (item-code index plus the 2.02 body / exhibit 99.1 of 0001805385-26-000047), input_prior_predictions.md (none on record).
- Not in my directory: Item 1A diff, Exhibit 21 diff, any Exhibit 10. There is no auditor's report; this is a 10-Q.
- Nothing I'm not allowed to see was present: no trend table, prices, returns, short interest, other company files, prior probabilities or outcome window. The 8-K exhibit carries the company's own condensed statements and a six-quarter key-operating-statistics table as part of the 8-K body. I read them as prose and did no arithmetic on them.
- I could only see a prior version for the note sections the change history covers: contingencies, organization/liquidity, significant policies, debt, marketable securities and revenue. For other note sections, and for all MD&A and Item 4 paragraphs, I judged substance from the current text alone. Where that wasn't enough I marked the paragraph `insufficient` below.

## Items

```json
[
  {
    "id": "related_parties_contingencies_and_subsequent_events_sec_matter_first_accrual",
    "what_changed": "The prior filing said 'we have not accrued a loss pertaining to the SEC matter.' The note now says that as of June 30, 2026 the Company had accrued $0.1 million as an estimated liability for the SEC matter, recorded in other accrued liabilities, with the expense in general and administrative expense. The paragraph describing the SEC subpoena and the DOJ letter (notes:162) is unchanged and still says the Company is cooperating with the SEC's investigation.",
    "account": "accrued expenses and other current liabilities; general and administrative expense",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "As of June 30, 2026, the Company had accrued $0.1 million as an estimated liability related to the SEC matter, which was recorded in other accrued liabilities in the condensed consolidated balance sheets",
    "paragraph_id": "0001805385-26-000049:notes:164",
    "explanation": false
  },
  {
    "id": "across_documents_sec_resolution_fees_in_non_gaap_addback",
    "what_changed": "The earnings release defines 'other non-recurring legal and regulatory costs', which are added back in adjusted operating expenses, Adjusted EBITDA and adjusted earnings, to include 'fees related to the resolution of the Securities and Exchange Commission investigation, net of estimated insurance recoveries'. The 10-Q note records a first SEC accrual (notes:164) but does not say a resolution has been reached; notes:162 still says the Company is cooperating. The 8-K index also shows an item 8.01 filed 2026-08-10 (0001805385-26-000040) whose body is not in my input. My input doesn't show whether this release wording is new compared with earlier releases. Supervisor: check whether the SEC accrual and any resolution costs sit inside the non-GAAP add-back.",
    "account": "Adjusted EBITDA and adjusted earnings (non-GAAP); general and administrative expense",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "as well as fees related to the resolution of the Securities and Exchange Commission investigation, net of estimated insurance recoveries",
    "paragraph_id": "0001805385-26-000047:8k_2_02:30",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_derivative_settlement_stipulation_executed",
    "what_changed": "The prior filing had only a May 4, 2026 agreement in principle, still subject to definitive documentation and court approval. The note now says a Stipulation and Agreement of Settlement was executed on August 5, 2026. It resolves the Massachusetts and both Delaware derivative actions and also the 'January 6, 2026 stockholder litigation demand', which is newly named. The District Court gave preliminary approval on August 6, 2026, and the final settlement hearing is set for October 21, 2026. These are events after the balance-sheet date. The 8-K index shows an item 8.01 filed 2026-08-10 whose body is not in my input; I can't tell whether it relates to this settlement.",
    "account": "accrued expenses and other current liabilities; prepaid expenses and other current assets",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "On August 5, 2026, the parties executed a Stipulation and Agreement of Settlement to fully and finally resolve the Massachusetts Derivative Action, the First Delaware Derivative Action, the Second Delaware Derivative Action, and the January 6, 2026 stockholder litigation demand.",
    "paragraph_id": "0001805385-26-000049:notes:159",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_derivative_settlement_accrual_and_recovery_disclosed",
    "what_changed": "The prior filing described the $1.3 million plaintiffs' counsel fee, to be paid by the D&O carriers, but mentioned no accrual. The note now says a $1.3 million settlement accrual and a $1.3 million estimated insurance recovery were recognized during the three months ended March 31, 2026. They are carried gross, in accrued expenses and in prepaid and other current assets, as management's best estimate at June 30, 2026. A balance recognized in the prior quarter is disclosed for the first time this quarter.",
    "account": "accrued expenses and other current liabilities; prepaid expenses and other current assets",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "During the three months ended March 31, 2026, the Company recognized a settlement accrual of $1.3 million and an estimated insurance recovery of $1.3 million",
    "paragraph_id": "0001805385-26-000049:notes:160",
    "explanation": false
  },
  {
    "id": "across_documents_derivative_settlement_loss_versus_gross_accrual",
    "what_changed": "MD&A's contractual-obligations text says the Company 'recorded an estimated loss' of $1.3 million on the derivative lawsuits. Note 13 describes the same matter as a $1.3 million settlement accrual with a $1.3 million estimated insurance recovery, with the fee paid by the D&O carriers, and expects no material adverse effect. One document calls it a loss; the other calls it a gross accrual with a matching recovery. Supervisor: check which describes the effect on G&A.",
    "account": "general and administrative expense; accrued expenses and other current liabilities",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Additionally, the Company recorded an estimated loss related to derivate lawsuits filed on November 12, 2024 of $1.3 million.",
    "paragraph_id": "0001805385-26-000049:mdna:210",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_class_action_settlement_funded_into_qualified_settlement_fund",
    "what_changed": "New sentence: during the quarter the Company contributed $0.7 million into a Qualified Settlement Fund, as the class action settlement requires, and classified it as restricted cash. MD&A (mdna:210) adds that the full $15.0 million settlement was funded into the QSF during the quarter, with $14.3 million from insurers and $0.7 million from the Company. The final fairness hearing is still September 24, 2026 (notes:152, carried from the prior filing). This is the first restricted cash balance and comes with a new restricted cash policy.",
    "account": "restricted cash; accrued expenses and other current liabilities; prepaid expenses and other current assets",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "During the three months ended June 30, 2026, the Company contributed $0.7 million into a QSF as required by the settlement agreement, which is classified as restricted cash in the condensed consolidated balance sheet as of June 30, 2026.",
    "paragraph_id": "0001805385-26-000049:notes:153",
    "explanation": false
  },
  {
    "id": "across_documents_class_action_accrual_retained_after_settlement_funding",
    "what_changed": "MD&A says that as of June 30, 2026 the Company still has the $15.0 million settlement accrual and the $14.3 million insurance recovery recognized, while also saying the full settlement was funded into the QSF during the quarter. Note 13 (notes:153) says only that the accrual and recovery 'remain' in the balance sheet as of December 31, 2025, and gives no June 30, 2026 status. Neither text says whether funding the QSF before final court approval removed the gross liability and receivable. Supervisor: reconcile against the accrued expenses and prepaid balances.",
    "account": "accrued expenses and other current liabilities; prepaid expenses and other current assets",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "As of June 30, 2026, the Company has recognized a settlement accrual of $15.0 million and an estimated insurance recovery of $14.3 million for the preliminary class action settlement.",
    "paragraph_id": "0001805385-26-000049:mdna:210",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_restricted_cash_policy_added",
    "what_changed": "A new significant accounting policy for restricted cash covers funds held in the QSF for the securities class action settlement, which are not available for general corporate purposes. The statement on policy changes (notes:19) now names restricted cash alongside the PSU valuation estimates as the only changes. The fair value note (notes:36) now includes restricted cash among the carrying amounts that approximate fair value.",
    "account": "restricted cash",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The Company classifies cash and cash equivalents as restricted when they are unavailable for withdrawal or use in its general operations.",
    "paragraph_id": "0001805385-26-000049:notes:21",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_founder_shares_vesting_period_expired",
    "what_changed": "New subsequent-event statement: no Founder Share milestone was achieved before the vesting period expired on July 16, 2026. Under the arrangement (notes:46), unvested shares 'must be returned to the Company for cancellation' if the vesting conditions are not met. That includes shares already transferred to stockholders' brokerage accounts, which back the contingently returnable asset. MD&A (mdna:103) repeats the statement. The prose implies the shares are returned and cancelled, and the returnable asset settled, after the quarter.",
    "account": "common stock shares outstanding; contingently returnable common stock asset (other assets); additional paid-in capital",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "As of June 30, 2026, no milestones had been achieved, and none were achieved prior to the expiration of the vesting period on July 16, 2026.",
    "paragraph_id": "0001805385-26-000049:notes:45",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_founder_share_valuation_moved_off_monte_carlo",
    "what_changed": "The note now says the Monte Carlo valuation was used only 'Through March 31, 2026'. As of June 30, 2026 management determined the milestones were not achievable within the remaining term and concluded that no contingently issuable common shares remain, so the liability rollforward (notes:50) ends at nil. A $3.8 million contingently returnable common stock asset is carried in other assets at the estimated fair value of the returnable shares. This is a judgment-based change of estimate that runs through other income. The policy-change statement (notes:19) and MD&A's critical accounting estimates (mdna:243, mdna:245) name only restricted cash and the PSU valuation as changes.",
    "account": "contingently issuable common stock liability, noncurrent; other assets; change in fair value of contingently issuable/returnable common stock liability/asset",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "However, as of June 30, 2026, the Company determined that the required milestones were not achievable within the remaining term, and as a result, concluded there are no remaining contingently issuable common shares.",
    "paragraph_id": "0001805385-26-000049:notes:48",
    "explanation": false
  },
  {
    "id": "across_documents_contingently_issuable_shares_still_in_antidilution_table",
    "what_changed": "Note 3 (notes:48) says no contingently issuable common shares remain at June 30, 2026. The EPS note's antidilutive-securities table still has a 'Contingently issuable common stock*' row with a share count for June 30, 2026. Supervisor: reconcile the share count against the note's conclusion.",
    "account": "antidilutive securities excluded from diluted EPS",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Contingently issuable common stock*",
    "paragraph_id": "0001805385-26-000049:notes:143",
    "explanation": false
  },
  {
    "id": "across_documents_founder_share_gain_described_as_mark_to_market",
    "what_changed": "MD&A attributes the six-month gain on the contingently issuable/returnable common stock liability/asset to 'quarterly mark-to-market adjustments'; the quarter paragraph (mdna:149) says the same. The note (notes:48) says the liability was removed because management judged the milestones were not achievable, not by a model remeasurement. The two documents describe the source of the gain differently.",
    "account": "change in fair value of contingently issuable/returnable common stock liability/asset",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Change in the fair value of the contingently issuable/returnable common stock liability resulted in a $1.5 million gain and $2.2 million loss for the six months ended June 30, 2026 and 2025, respectively, resulting from quarterly mark-to-market adjustments.",
    "paragraph_id": "0001805385-26-000049:mdna:192",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_public_warrants_expired",
    "what_changed": "New subsequent-event statement: all Public Warrants expired on July 16, 2026. The note gives 14,324,893 outstanding at June 30, 2026 and now uses the past tense ('were classified as a liability and remeasured'). MD&A (mdna:105) repeats the expiry. The prose implies the remaining public warrant liability is extinguished, the warrant fair-value line in other income stops, and the warrants drop out of the antidilutive count.",
    "account": "public warrant liability, noncurrent; change in fair value of public warrant liability",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "As of June 30, 2026, 14,324,893 Public Warrants were outstanding, and on July 16, 2026, all Public Warrants expired.",
    "paragraph_id": "0001805385-26-000049:notes:54",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_rebate_asset_relabelled_commission_asset",
    "what_changed": "The prior filing said rebate liabilities 'are recognized as contract assets, amortized as reductions to revenue' and gave rebate balances as contract assets. The note now says they are 'recognized as commission asset', and labels the December 31, 2025 rebate balances as commission asset too. No reclassification or revision is disclosed. MD&A's explanation of the change in commission assets (mdna:222) doesn't mention rebates. Item 4 still reports a material weakness over 'the classification of various accounts'.",
    "account": "commission asset (current and noncurrent); contract assets; revenue (rebate reductions)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "recognized as commission asset, amortized as reductions to revenue over time, consistent with the recognition of the underlying revenue.",
    "paragraph_id": "0001805385-26-000049:notes:81",
    "explanation": false
  },
  {
    "id": "revenue_recognition_contract_liability_description_now_includes_subscription",
    "what_changed": "The contract liability was described as 'related to service revenue'. It is now 'related to subscription revenue and service revenue'. Subscription revenue is described elsewhere as operating-lease income (notes:58, notes:73), so the contract-liability description and its rollforward now cover lease-related deferrals as well as ASC 606 service deferrals. The paragraph also now gives revenue recognized out of opening deferred revenue for both the three- and six-month periods.",
    "account": "deferred revenue (current and noncurrent)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The Company has a contract liability related to subscription revenue and service revenue, which consists of amounts that have been invoiced but that have not been recognized as revenue.",
    "paragraph_id": "0001805385-26-000049:notes:68",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_remaining_performance_obligation_time_bands_relabelled",
    "what_changed": "The remaining performance obligation table's time-band headings changed from 'Less than 1 year / 1 - 2 years / More than 2 years' to 'Next 12 months / 13 to 24 months / More than 24 months'. The text doesn't say whether the basis of the bands changed, for example from remaining calendar periods to rolling twelve-month periods. The lease maturity schedule (notes:86), which covers the same subscription obligations, is still by calendar year. Supervisor: check that the RPO subscription row and the lease schedule are on the same basis.",
    "account": "remaining performance obligations",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Next 12 months",
    "paragraph_id": "0001805385-26-000049:notes:65",
    "explanation": false
  },
  {
    "id": "results_against_expectations_remaining_performance_obligation_growth_claim",
    "what_changed": "MD&A states RPO of $312.6 million at June 30, 2026, 'an increase of approximately 5% from December 31, 2025, driven by continued market demand.' The earnings release (8k_2_02:12) states RPO was 'up $13.6 million sequentially'. The two documents measure the change from different base dates. The prose says RPO rose.",
    "account": "remaining performance obligations",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "RPO at June 30, 2026 was $312.6 million, an increase of approximately 5% from December 31, 2025, driven by continued market demand.",
    "paragraph_id": "0001805385-26-000049:mdna:38",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_operating_cash_flow_described_as_inflow",
    "what_changed": "The liquidity paragraph now says operating activities 'resulted in cash inflow' for the year to date. The prior filing said operating activities 'resulted in cash outflows' for its year to date. The Company still 'expects to continue to generate losses for the foreseeable future.' MD&A gives the working-capital drivers, including the timing of vendor payments (mdna:219).",
    "account": "net cash provided by (used in) operating activities",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "operating activities resulted in cash inflow of $8.7 million and outflow of $0.4 million during the six months ended June 30, 2026 and 2025, respectively.",
    "paragraph_id": "0001805385-26-000049:notes:7",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_minimum_arr_covenant_threshold_updated",
    "what_changed": "The minimum required ARR under the MidCap covenant is now stated as $108.7 million at June 30, 2026; the prior filing stated $107.3 million at March 31, 2026. The threshold 'increases quarterly thereafter'. The Company states full compliance and expects to stay compliant for twelve months from the filing date. The minimum-liquidity covenant still lapses only once the litigation and regulatory matters are resolved, and the minimum EBITDA covenant starts June 30, 2027. The covenant uses ARR 'as defined' in the agreement; see the ARR definition item.",
    "account": "ARR (covenant metric); long-term debt",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "As of June 30, 2026, the minimum required ARR is $108.7 million, and the Company is in full compliance with all applicable covenant requirements, and expects to remain in compliance for a period of at least twelve months from the date of this Quarterly Report on Form 10-Q.",
    "paragraph_id": "0001805385-26-000049:notes:12",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_term_loan_applicable_margin_restated",
    "what_changed": "The rate in effect is now about 8.62%: Term SOFR of 3.62% plus an applicable margin of 5.00%. The prior filing stated about 8.92%: Term SOFR of 3.67% plus a margin of 5.25%. Notes:105 says the margin is 'calculated based on EBITDA'. The text gives no reason for the different margin. Whether and how interest cost moves is for the numbers reader.",
    "account": "interest expense; long-term debt",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "The interest rate in effect as of June 30, 2026 was approximately 8.62%, which includes Term SOFR of 3.62% and an applicable margin of 5.00%.",
    "paragraph_id": "0001805385-26-000049:notes:110",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_inventory_reserve_charges_first_generation_parts_quarter",
    "what_changed": "For the quarter, MD&A attributes the higher product gross margin to fixed-cost leverage and to a $1.7 million decrease in inventory reserve charges on first-generation Evolv Express parts. The offsets it names are manufacturing expense ($0.7 million) and outbound shipping ($0.3 million). It attributes the product revenue increase to demand and to the end of the Distribution and License Agreement, which moved buyers to the purchase subscription model.",
    "account": "inventory reserve; cost of product revenue",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "a $1.7 million decrease in charges taken related to our inventory reserve on first generation Evolv Express parts compared to the prior year period",
    "paragraph_id": "0001805385-26-000049:mdna:120",
    "explanation": true
  },
  {
    "id": "estimates_and_discretion_inventory_reserve_charges_first_generation_parts_year_to_date",
    "what_changed": "For the six months, MD&A again attributes the higher product gross margin to fixed-cost leverage and to a $1.7 million decrease in inventory reserve charges on first-generation Evolv Express parts. The offsets it names are manufacturing expense ($1.0 million) and outbound shipping ($0.7 million). The cash flow line 'Write-off of inventory and change in inventory reserve' is the figure for the numbers reader to check this against.",
    "account": "inventory reserve; cost of product revenue",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "a $1.7 million decrease in charges taken related to our inventory reserves on first generation Evolv Express parts",
    "paragraph_id": "0001805385-26-000049:mdna:162",
    "explanation": true
  },
  {
    "id": "liquidity_and_capital_inventory_decrease_attributed_to_inventory_management",
    "what_changed": "MD&A attributes a $2.3 million decrease in inventory for the six months to 'an increased focus on efficient inventory management'. It doesn't mention the change in uninstalled inventory in the inventory note (notes:91, notes:92). It doesn't mention transfers of inventory into leased equipment, an area named in the Item 4 material weakness. It also doesn't mention the Plexus onboarding, which MD&A says may temporarily affect working capital through dual production (mdna:49).",
    "account": "inventory",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "$2.3 million decrease in inventory primarily due to an increased focus on efficient inventory management;",
    "paragraph_id": "0001805385-26-000049:mdna:220",
    "explanation": true
  },
  {
    "id": "revenue_recognition_receivables_increase_attributed_to_sales_and_billing_timing",
    "what_changed": "MD&A attributes an $8.8 million increase in accounts receivable for the six months to 'higher sales and the timing of billings to customers'. The prior-year comparative bullet (mdna:233) uses the same wording. In the same quarter the text describes a move toward purchase-subscription hardware sales recognized upfront (mdna:120; 8k_2_02:21). The allowance note (notes:89) has no prose.",
    "account": "accounts receivable, net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "$8.8 million increase in accounts receivable primarily due to higher sales and the timing of billings to customers;",
    "paragraph_id": "0001805385-26-000049:mdna:224",
    "explanation": true
  },
  {
    "id": "revenue_recognition_contract_assets_increase_attributed_to_sales_volume",
    "what_changed": "MD&A attributes a $1.6 million increase in contract assets, which are unbilled amounts per notes:67, to 'higher volume of sales'. The note states current contract assets of $2.5 million at June 30, 2026 and $0.9 million at December 31, 2025. The rebate balances that the prior filing described as contract assets are now labelled commission asset (notes:81), so the text changed what the line is said to contain.",
    "account": "contract assets (current)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "$1.6 million increase in contract assets due to higher volume of sales;",
    "paragraph_id": "0001805385-26-000049:mdna:225",
    "explanation": true
  },
  {
    "id": "earnings_quality_prepaid_increase_attributed_to_estimated_insurance_recoveries",
    "what_changed": "MD&A attributes a $0.6 million increase in prepaid expenses and other current assets to 'increases in estimated insurance recoveries'. These are insurance-recovery receivables carried in prepaid. Note 13 gives remaining estimated defense-cost recoveries of $1.4 million at June 30, 2026 and $1.3 million at December 31, 2025 (notes:165). It also gives a new $1.3 million derivative-settlement recovery recognized in the first quarter (notes:160), and MD&A says the $14.3 million class action recovery is still recognized (mdna:210). The recoveries are estimates the Company has 'determined are probable of recovery' and are booked as reductions of G&A.",
    "account": "prepaid expenses and other current assets (insurance recovery receivable); general and administrative expense",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "$0.6 million increase in prepaid expenses and other current assets primarily due to increases in estimated insurance recoveries.",
    "paragraph_id": "0001805385-26-000049:mdna:227",
    "explanation": true
  },
  {
    "id": "liquidity_and_capital_accrued_expenses_increase_vendor_payables_and_derivative_accrual",
    "what_changed": "MD&A attributes a $1.5 million increase in accrued expenses and other current liabilities to higher accrued vendor payables and the $1.3 million derivative settlement accrual, partly offset by paying 2025 bonuses and commissions. This is the first time the derivative settlement accrual is named as a working-capital driver. The text doesn't mention the new SEC accrual (notes:164) or the class action accrual still stated as recognized (mdna:210).",
    "account": "accrued expenses and other current liabilities",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "$1.5 million increase in accrued expenses and other current liabilities primarily due to the increase in accrued vendor payables and $1.3 million settlement accrual for the derivative matters",
    "paragraph_id": "0001805385-26-000049:mdna:221",
    "explanation": true
  },
  {
    "id": "liquidity_and_capital_operating_cash_flow_supported_by_payables_timing",
    "what_changed": "MD&A attributes a $6.4 million increase in accounts payable, excluding unpaid capital expenditures, to 'the timing of vendor payments'. It is the first operating-cash driver listed in the period when the liquidity paragraph first describes an operating cash inflow (notes:7). The text gives no expectation of when the timing reverses.",
    "account": "accounts payable; net cash provided by (used in) operating activities",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "$6.4 million increase in accounts payable (excluding the non-cash portion related to capital expenditures incurred but not yet paid) due primarily to the timing of vendor payments;",
    "paragraph_id": "0001805385-26-000049:mdna:219",
    "explanation": false
  },
  {
    "id": "earnings_quality_commission_asset_decrease_attributed_to_purchase_subscription_mix",
    "what_changed": "MD&A attributes a $0.6 million decrease in commission assets to amortization timing and 'the increased proportion of orders utilizing our purchase subscription model'. Under notes:83, commissions on product sales are expensed when the revenue is recognized and subscription commissions are deferred, so more purchase-subscription orders means more commission expense upfront. The explanation doesn't mention that rebate assets are now carried in the commission asset line (notes:81).",
    "account": "commission asset (current and noncurrent); sales and marketing expense",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "$0.6 million decrease in commission assets due to the timing of amortization and the increased proportion of orders utilizing our purchase subscription model during the period",
    "paragraph_id": "0001805385-26-000049:mdna:222",
    "explanation": false
  },
  {
    "id": "earnings_quality_subscription_margin_helped_by_lower_disposal_losses_quarter",
    "what_changed": "MD&A attributes part of the quarter's higher subscription gross margin to a $1.1 million decrease in expense from disposals of first-generation Evolv Express systems. Notes:100 gives disposal losses on previously leased systems for the quarter and six months, 'primarily in connection with customer upgrades to the second generation'. The release adds disposal losses back in Adjusted EBITDA (8k_2_02:77), so this driver moves GAAP gross margin but not Adjusted EBITDA.",
    "account": "cost of subscription revenue; loss on disposal of property and equipment",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The increase in subscription gross profit margin is also driven by a decrease of $1.1 million of expense related to disposals of certain first generation Evolv Express systems",
    "paragraph_id": "0001805385-26-000049:mdna:123",
    "explanation": false
  },
  {
    "id": "earnings_quality_subscription_margin_helped_by_lower_field_service_costs_year_to_date",
    "what_changed": "For the six months, MD&A attributes the higher subscription gross margin to a $1.3 million decrease in field services cost for subscription systems and a $1.0 million decrease in disposal losses. The field services cost reduction does not appear in the quarter paragraph (mdna:123). The same paragraph says cost of subscription revenue rose as more systems were deployed.",
    "account": "cost of subscription revenue",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The increase in subscription gross profit margin is driven by a $1.3 million decrease in field services cost related to our subscription systems and a $1.0 million decrease in loss on disposals of certain first generation Evolv Express systems during the six months ended June 30, 2026.",
    "paragraph_id": "0001805385-26-000049:mdna:165",
    "explanation": false
  },
  {
    "id": "revenue_recognition_license_fee_revenue_ceased_after_distribution_agreement_expiry",
    "what_changed": "MD&A now says no license fee revenue was earned in the quarter, and that license revenue from the Columbia Tech agreement, which expired December 31, 2025, 'has reduced to zero' and is replaced by product revenue under purchase subscription (mdna:29, mdna:63). For the six months, $0.2 million of license fees was earned (mdna:171). The prose says gross profit rises 'over the term of the related subscription contract'; see the purchase-subscription mix item for the release's warning on near-term margin.",
    "account": "license fee and other revenue; product revenue",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "As a result, there was no license fee revenue earned during the three months ended June 30, 2026 compared to $2.3 million earned during the prior year period.",
    "paragraph_id": "0001805385-26-000049:mdna:130",
    "explanation": false
  },
  {
    "id": "results_against_expectations_full_year_outlook_raised_in_release",
    "what_changed": "The release raises the 2026 outlook. Revenue is now $180 to $185 million (May 12, 2026 outlook: $175 to $180 million). Ending ARR is now $148 to $150 million (May: $145 to $150 million). A first Adjusted EBITDA range of $15 to $16 million is added (May: 'n/a'). The Adjusted EBITDA margin outlook stays at high single digits. Headline: 'Company Raises Growth Estimates for 2026'.",
    "account": "total revenue; ARR; Adjusted EBITDA",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "The Company expects total revenues in 2026 to be between $180 to $185 million, reflecting growth of approximately 23% to 27% year-over-year.",
    "paragraph_id": "0001805385-26-000047:8k_2_02:21",
    "explanation": false
  },
  {
    "id": "revenue_recognition_purchase_subscription_mix_expectation_raised",
    "what_changed": "The Company now expects about 60% of 2026 new unit deployments under the purchase subscription model, against its prior expectation of about 55%. The release says a higher purchase-subscription mix brings revenue recognition forward into the early years of a typical four-year contract and creates a near-term headwind to gross margin percentage, because hardware cost is recognized upfront. MD&A (mdna:29) says the move to product revenue raises gross profit over the term of the subscription.",
    "account": "product revenue; cost of product revenue; gross margin",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "As expected under the purchase subscription model, a higher purchase subscription mix increases revenue recognition in the early years of a typical four year customer contract and creates a modest near-term headwind to reported gross margin percentage as associated hardware costs are recognized upfront.",
    "paragraph_id": "0001805385-26-000047:8k_2_02:21",
    "explanation": false
  },
  {
    "id": "results_against_expectations_long_term_growth_framework_stated",
    "what_changed": "The CFO quote cites a long-term framework from a recent Investor Day: revenue CAGR of about 25% through 2031, Adjusted EBITDA margins expanding every year, and 'Rule of 50 performance over time'. None of these targets appears in the 10-Q text in my input.",
    "account": "total revenue; Adjusted EBITDA margin",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "We remain focused on building a durable growth business capable of delivering revenue CAGR of approximately 25% through 2031 while expanding Adjusted EBITDA margins annually.",
    "paragraph_id": "0001805385-26-000047:8k_2_02:23",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_recurring_revenue_definition_excludes_short_term_rentals",
    "what_changed": "A footnote to the key operating statistics says prior quarters were reclassified for an 'update to the definition of non-recurring revenue'. Short-term rental subscription revenue, previously counted as recurring, is now non-recurring, applied to all prior periods. Footnote 3 (8k_2_02:31) now lists 'rental revenue' in non-recurring revenue. The prose implies the recurring revenue metric, as now reported, is lower for the reclassified periods.",
    "account": "recurring revenue (operating metric)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "*Certain prior quarter amounts have been reclassified to reflect an update to the definition of non-recurring revenue to include short term rental subscription revenue, applied consistently to all prior periods, which were previously classified as recurring revenue.",
    "paragraph_id": "0001805385-26-000047:8k_2_02:59",
    "explanation": false
  },
  {
    "id": "across_documents_arr_definition_and_covenant_metric",
    "what_changed": "The release defines ARR as final-month subscription revenue plus recurring purchase-subscription service revenue, times twelve. The definition keeps contracts in ARR past expiration while a renewal or upgrade is being negotiated, and keeps customers who have said they will not renew until the term ends. It doesn't say whether short-term rental subscription revenue, now non-recurring (8k_2_02:59), is excluded. The credit agreement's minimum-ARR covenant uses ARR 'as defined' (notes:12). Supervisor: check whether the reported ARR and the covenant ARR are the same measure. My input doesn't show whether the release definition is new.",
    "account": "ARR (covenant and operating metric)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "To the extent that we are negotiating a renewal or upgrade with a customer after the expiration of the subscription and we are continuing to provide service to that customer, we may continue to include that associated revenue in ARR.",
    "paragraph_id": "0001805385-26-000047:8k_2_02:29",
    "explanation": false
  },
  {
    "id": "across_documents_new_customer_counts_reconciliation",
    "what_changed": "MD&A attributes ARR growth partly to 'nearly 250 customers' added in the twelve months to June 30, 2026. It also gives 70 new end-users for the quarter (mdna:117) and 118 for the six months (mdna:160). The release table (8k_2_02:58) lists new customers by quarter. Supervisor: reconcile the counts.",
    "account": "ARR (operating metric)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "This increase was driven by the addition of nearly 250 customers during the twelve month period ended June 30, 2026",
    "paragraph_id": "0001805385-26-000049:mdna:37",
    "explanation": false
  },
  {
    "id": "across_documents_contract_manufacturer_forecast_shortfall_commitment",
    "what_changed": "MD&A says the contract with the 'new contract manufacturer' (Plexus, mdna:49) has provisions under which order volumes below the Company's forecasts 'may result in purchase commitments'. The note's commitments text (notes:168), unchanged, describes only cancellable purchase orders with payment on cancellation for work done. Neither document gives an amount.",
    "account": "purchase commitments; inventory; cost of product revenue",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Our contract with our new contract manufacturer includes provisions for which order volumes that fall short of our forecasts may result in purchase commitments.",
    "paragraph_id": "0001805385-26-000049:mdna:208",
    "explanation": false
  },
  {
    "id": "results_against_expectations_sales_and_marketing_expected_increase",
    "what_changed": "MD&A expects 2026 sales and marketing costs to exceed 2025's as the Company expands go-to-market efforts through direct and channel investments. The paragraph is carried as changed, but the prior text isn't in my input, so I can't tell whether this expectation is new or reworded.",
    "account": "sales and marketing expense",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "We expect our sales and marketing costs will increase for the year ending December 31, 2026 compared to the year ended December 31, 2025 as we expand our go to market efforts through both direct and channel investments.",
    "paragraph_id": "0001805385-26-000049:mdna:89",
    "explanation": false
  },
  {
    "id": "results_against_expectations_general_and_administrative_expected_increase",
    "what_changed": "MD&A expects 2026 G&A to exceed 2025's. It cites a bigger G&A team and external consultants for systems and Sarbanes-Oxley compliance, partly offset by investigation and restatement costs it calls 'substantially non-recurring'. It also says those costs 'began to decline in the second half of 2025'. Item 4 (item_4_controls:32) describes new quoting and ERP projects. The prior text isn't in my input.",
    "account": "general and administrative expense",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "We expect our general and administrative expenses to increase for the year ending December 31, 2026 compared to the year ended December 31, 2025 primarily due to expansion of our general and administrative team and engagements with external consultants to enhance our systems and Sarbanes-Oxley Act compliance efforts",
    "paragraph_id": "0001805385-26-000049:mdna:91",
    "explanation": false
  },
  {
    "id": "earnings_quality_general_and_administrative_lower_insurance_recoveries",
    "what_changed": "For the six months, MD&A attributes the decrease in non-recurring professional fees to a $10.7 million decrease in investigation and restatement fees and a $0.3 million decrease in estimated net class action losses, partly offset by 'a decrease in insurance recoveries of $2.3 million'. Insurance recoveries are estimates booked as reductions of G&A (notes:165), so G&A depends partly on the recovery estimate.",
    "account": "general and administrative expense; prepaid expenses and other current assets",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "partially offset by a decrease in insurance recoveries of $2.3 million.",
    "paragraph_id": "0001805385-26-000049:mdna:181",
    "explanation": false
  },
  {
    "id": "controls_audit_and_filings_quoting_system_release_and_erp_project_timeline",
    "what_changed": "New period-specific sentence: as of Q2 2026 the Company has a project plan, with release dates, for new quoting functionality due in Q3 2026, and is contracting resources to design the ERP project plan, still slated for 2027. Quoting, commissions and order processing feed the revenue and commission-asset processes named in the unremediated material weaknesses. Disclosure controls are still concluded not effective at June 30, 2026 (item_4_controls:5), and no material change in ICFR is reported for the quarter (item_4_controls:36).",
    "account": "none",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "As of Q2 2026, we have developed and commenced execution on a project plan with release dates for the new quoting functionality to be released in Q3 2026 while contracting additional resources to begin designing a project plan for the new ERP system.",
    "paragraph_id": "0001805385-26-000049:item_4_controls:32",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_first_delaware_derivative_stay_continued",
    "what_changed": "The First Delaware Derivative Action was previously stayed pending the outcome of the motion to dismiss in the Class Action. On June 30, 2026 the Court granted the parties' request to continue the stay while they pursue informal resolution, which ties it to the derivative settlement (notes:159).",
    "account": "none",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "to continue the stay of the First Delaware Derivative Action while the parties pursue informal resolution.",
    "paragraph_id": "0001805385-26-000049:notes:156",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_second_delaware_derivative_stay_continued",
    "what_changed": "The Second Delaware Derivative Action was previously stayed under a November 7, 2025 order pending renewed motions to dismiss or final disposition of the Class Action. On June 30, 2026 the Court granted the parties' request to continue the stay while they pursue informal resolution, which ties it to the derivative settlement (notes:159).",
    "account": "none",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "to continue the stay of the Second Delaware Derivative Action while the parties pursue informal resolution.",
    "paragraph_id": "0001805385-26-000049:notes:158",
    "explanation": false
  }
]
```

## Paragraphs carried as text that are not items

### Notes
- 0001805385-26-000049:notes:2 — wording only ("major" → "primary" products)
- 0001805385-26-000049:notes:3 — wording only ("dba" → "d/b/a")
- 0001805385-26-000049:notes:5 — no change identifiable; consolidation boilerplate
- 0001805385-26-000049:notes:10 — date rolled forward
- 0001805385-26-000049:notes:11 — date rolled forward; amount only
- 0001805385-26-000049:notes:16 — date rolled forward (basis of presentation)
- 0001805385-26-000049:notes:18 — paragraph split only
- 0001805385-26-000049:notes:19 — covered by restricted cash policy item; PSU cross-reference reworded
- 0001805385-26-000049:notes:20 — heading of new policy; covered by restricted cash policy item
- 0001805385-26-000049:notes:22 — heading
- 0001805385-26-000049:notes:23 — punctuation only
- 0001805385-26-000049:notes:24 — heading
- 0001805385-26-000049:notes:25 — not in change history; no change identifiable (pending ASU 2024-03)
- 0001805385-26-000049:notes:26 — not in change history; no change identifiable (pending ASU 2025-06)
- 0001805385-26-000049:notes:27 — date rolled forward
- 0001805385-26-000049:notes:28 — amounts only
- 0001805385-26-000049:notes:29 — amounts only
- 0001805385-26-000049:notes:30 — date rolled forward
- 0001805385-26-000049:notes:32 — amounts only (fair value table)
- 0001805385-26-000049:notes:34 — insufficient — amounts and dates; section not in history, so I can't tell whether the sentence on T-bills in cash equivalents is new
- 0001805385-26-000049:notes:36 — restricted cash added to short-maturity list; covered by restricted cash policy item
- 0001805385-26-000049:notes:38 — date rolled forward
- 0001805385-26-000049:notes:40 — date rolled forward; earn-out expired March 8, 2026, before the prior filing
- 0001805385-26-000049:notes:43 — amounts only (earn-out rollforward)
- 0001805385-26-000049:notes:46 — amounts and date; return obligation covered by founder shares vesting item
- 0001805385-26-000049:notes:47 — amount only
- 0001805385-26-000049:notes:50 — amounts only; covered by founder share valuation item
- 0001805385-26-000049:notes:52 — amounts only
- 0001805385-26-000049:notes:56 — amounts only
- 0001805385-26-000049:notes:58 — paragraph split only
- 0001805385-26-000049:notes:59 — paragraph split only
- 0001805385-26-000049:notes:61 — grammar fix and paragraph rejoin
- 0001805385-26-000049:notes:62 — wording only (cross-reference phrase removed)
- 0001805385-26-000049:notes:64 — date rolled forward
- 0001805385-26-000049:notes:67 — amounts and date; cause covered by contract assets item
- 0001805385-26-000049:notes:69 — amounts only (prior-year comparatives)
- 0001805385-26-000049:notes:71 — amounts only (deferred revenue rollforward)
- 0001805385-26-000049:notes:73 — amounts only
- 0001805385-26-000049:notes:77 — amounts only
- 0001805385-26-000049:notes:80 — amounts and date (rebate accrual); no cause stated
- 0001805385-26-000049:notes:83 — amounts and date; six-month figures added
- 0001805385-26-000049:notes:85 — date rolled forward
- 0001805385-26-000049:notes:86 — amounts only (period roll)
- 0001805385-26-000049:notes:88 — caption; no change identifiable
- 0001805385-26-000049:notes:89 — amounts only (allowance rollforward)
- 0001805385-26-000049:notes:91 — amounts only
- 0001805385-26-000049:notes:92 — definition; no change identifiable
- 0001805385-26-000049:notes:94 — amounts only
- 0001805385-26-000049:notes:96 — amounts and date only
- 0001805385-26-000049:notes:98 — amounts only
- 0001805385-26-000049:notes:99 — insufficient — amounts and dates; section not in history, so I can't confirm the "generally 7 years" useful life is unchanged
- 0001805385-26-000049:notes:100 — insufficient — amounts and dates; I can't tell whether the "customer upgrades" reason is new; its use in MD&A is covered by the subscription margin item
- 0001805385-26-000049:notes:101 — heading and caption
- 0001805385-26-000049:notes:102 — amounts only
- 0001805385-26-000049:notes:103 — date rolled forward
- 0001805385-26-000049:notes:104 — not in change history; no change identifiable
- 0001805385-26-000049:notes:105 — wording (abbreviation) and paragraph split
- 0001805385-26-000049:notes:106 — paragraph split only
- 0001805385-26-000049:notes:107 — date and amount rolled; covered by minimum ARR covenant item
- 0001805385-26-000049:notes:108 — heading
- 0001805385-26-000049:notes:109 — not in change history; no change identifiable
- 0001805385-26-000049:notes:111 — date rolled forward
- 0001805385-26-000049:notes:112 — date rolled forward
- 0001805385-26-000049:notes:113 — heading
- 0001805385-26-000049:notes:114 — date rolled forward; amounts only
- 0001805385-26-000049:notes:115 — wording; date rolled
- 0001805385-26-000049:notes:116 — date rolled forward
- 0001805385-26-000049:notes:119 — amounts only
- 0001805385-26-000049:notes:123 — amounts only
- 0001805385-26-000049:notes:126 — date rolled forward
- 0001805385-26-000049:notes:127 — date rolled forward
- 0001805385-26-000049:notes:129 — date rolled forward; PSU grants already in prior filing's policy statement
- 0001805385-26-000049:notes:131 — amounts only
- 0001805385-26-000049:notes:133 — amounts only
- 0001805385-26-000049:notes:136 — amounts only
- 0001805385-26-000049:notes:137 — no change identifiable; full valuation allowance as before
- 0001805385-26-000049:notes:138 — insufficient — section not in history, so I can't tell whether the Evolv UK unrecognized-tax-benefit language is new
- 0001805385-26-000049:notes:141 — amounts only
- 0001805385-26-000049:notes:145 — not in change history; no change identifiable
- 0001805385-26-000049:notes:146 — heading
- 0001805385-26-000049:notes:147 — not in change history; no change identifiable
- 0001805385-26-000049:notes:148 — heading
- 0001805385-26-000049:notes:149 — not in change history; no change identifiable
- 0001805385-26-000049:notes:150 — heading
- 0001805385-26-000049:notes:151 — heading
- 0001805385-26-000049:notes:152 — not in change history; events dated before the prior filing
- 0001805385-26-000049:notes:155 — not in change history; Massachusetts stay text unchanged
- 0001805385-26-000049:notes:157 — paragraph split only
- 0001805385-26-000049:notes:161 — heading
- 0001805385-26-000049:notes:162 — not in change history; SEC/DOJ description unchanged
- 0001805385-26-000049:notes:163 — not in change history; boilerplate
- 0001805385-26-000049:notes:165 — amounts and dates rolled; grammar fix; used in prepaid and G&A items
- 0001805385-26-000049:notes:166 — paragraph rejoin; text unchanged
- 0001805385-26-000049:notes:167 — heading
- 0001805385-26-000049:notes:168 — not in change history; contrast covered by contract manufacturer across item
- 0001805385-26-000049:notes:169 — no change identifiable (segment boilerplate)
- 0001805385-26-000049:notes:171 — amounts only
- 0001805385-26-000049:notes:172 — date rolled forward
- 0001805385-26-000049:notes:173 — date rolled forward

### MD&A
- 0001805385-26-000049:mdna:7 — insufficient — AI platform business description; prior text not in input; no account bearing
- 0001805385-26-000049:mdna:8 — wording ("two primary products"), same as notes:2
- 0001805385-26-000049:mdna:22 — page number
- 0001805385-26-000049:mdna:25 — insufficient — list of fluctuation factors; prior text and Item 1A diff not in input
- 0001805385-26-000049:mdna:29 — covered by license fee item; expiry before prior filing
- 0001805385-26-000049:mdna:31 — page number
- 0001805385-26-000049:mdna:33 — amounts and date only
- 0001805385-26-000049:mdna:35 — insufficient — ARR rationale; prior text not in input
- 0001805385-26-000049:mdna:41 — page number
- 0001805385-26-000049:mdna:45 — amounts only
- 0001805385-26-000049:mdna:46 — period comparison; generic causes
- 0001805385-26-000049:mdna:48 — insufficient — legal/financing statement, probably a date roll; SEC accrual covered by its own item
- 0001805385-26-000049:mdna:49 — page split; Plexus is in the unchanged Supply Chain Strategy section
- 0001805385-26-000049:mdna:51 — continuation of mdna:49
- 0001805385-26-000049:mdna:63 — covered by license fee item
- 0001805385-26-000049:mdna:100 — page number
- 0001805385-26-000049:mdna:102 — vesting deadline restated; outcome covered by founder shares item
- 0001805385-26-000049:mdna:103 — covered by founder shares vesting item
- 0001805385-26-000049:mdna:105 — covered by public warrants item
- 0001805385-26-000049:mdna:108 — date rolled forward
- 0001805385-26-000049:mdna:109 — page number
- 0001805385-26-000049:mdna:111 — heading
- 0001805385-26-000049:mdna:112 — caption; date rolled
- 0001805385-26-000049:mdna:113 — amounts only
- 0001805385-26-000049:mdna:114 — table footnote
- 0001805385-26-000049:mdna:117 — customer count; covered by customer-count across item
- 0001805385-26-000049:mdna:119 — amounts only
- 0001805385-26-000049:mdna:122 — amounts only
- 0001805385-26-000049:mdna:124 — page number
- 0001805385-26-000049:mdna:126 — amounts only
- 0001805385-26-000049:mdna:127 — period comparison; template wording
- 0001805385-26-000049:mdna:129 — amounts only
- 0001805385-26-000049:mdna:132 — amounts only
- 0001805385-26-000049:mdna:133 — period comparison; template wording
- 0001805385-26-000049:mdna:136 — amounts only
- 0001805385-26-000049:mdna:137 — period comparison; template wording
- 0001805385-26-000049:mdna:139 — amounts only
- 0001805385-26-000049:mdna:140 — period comparison; six-month version is an item
- 0001805385-26-000049:mdna:142 — period comparison; template wording
- 0001805385-26-000049:mdna:144 — period comparison; template wording
- 0001805385-26-000049:mdna:146 — earn-out expiry before prior filing; period roll
- 0001805385-26-000049:mdna:147 — continuation; prior-year amount
- 0001805385-26-000049:mdna:149 — amounts; mark-to-market wording covered by across item
- 0001805385-26-000049:mdna:151 — amounts only
- 0001805385-26-000049:mdna:154 — heading
- 0001805385-26-000049:mdna:155 — caption
- 0001805385-26-000049:mdna:156 — amounts only
- 0001805385-26-000049:mdna:157 — table footnote
- 0001805385-26-000049:mdna:159 — heading
- 0001805385-26-000049:mdna:160 — customer count; covered by customer-count across item
- 0001805385-26-000049:mdna:161 — amounts only
- 0001805385-26-000049:mdna:163 — heading
- 0001805385-26-000049:mdna:164 — amounts only
- 0001805385-26-000049:mdna:166 — heading
- 0001805385-26-000049:mdna:167 — amounts only
- 0001805385-26-000049:mdna:168 — period comparison; template wording
- 0001805385-26-000049:mdna:169 — heading
- 0001805385-26-000049:mdna:170 — amounts only
- 0001805385-26-000049:mdna:171 — covered by license fee item
- 0001805385-26-000049:mdna:172 — heading
- 0001805385-26-000049:mdna:173 — amounts only
- 0001805385-26-000049:mdna:174 — period comparison; template wording
- 0001805385-26-000049:mdna:175 — page number
- 0001805385-26-000049:mdna:176 — heading
- 0001805385-26-000049:mdna:177 — amounts only
- 0001805385-26-000049:mdna:178 — period comparison; template wording
- 0001805385-26-000049:mdna:179 — heading
- 0001805385-26-000049:mdna:180 — amounts only
- 0001805385-26-000049:mdna:183 — amounts only
- 0001805385-26-000049:mdna:184 — heading
- 0001805385-26-000049:mdna:185 — period comparison; template wording
- 0001805385-26-000049:mdna:186 — page number
- 0001805385-26-000049:mdna:187 — heading
- 0001805385-26-000049:mdna:188 — period comparison; template wording
- 0001805385-26-000049:mdna:189 — heading
- 0001805385-26-000049:mdna:190 — earn-out expiry before prior filing; amounts
- 0001805385-26-000049:mdna:191 — heading
- 0001805385-26-000049:mdna:193 — heading
- 0001805385-26-000049:mdna:194 — amounts only
- 0001805385-26-000049:mdna:196 — date rolled; same as notes:7 (covered)
- 0001805385-26-000049:mdna:198 — date rolled forward
- 0001805385-26-000049:mdna:199 — date rolled forward
- 0001805385-26-000049:mdna:200 — date rolled; covered by minimum ARR covenant item
- 0001805385-26-000049:mdna:202 — no change identifiable
- 0001805385-26-000049:mdna:203 — no change identifiable; wording
- 0001805385-26-000049:mdna:204 — date rolled forward
- 0001805385-26-000049:mdna:206 — date and amount rolled
- 0001805385-26-000049:mdna:207 — amount rolled (HQ lease)
- 0001805385-26-000049:mdna:209 — page number
- 0001805385-26-000049:mdna:213 — amounts only
- 0001805385-26-000049:mdna:215 — amounts only
- 0001805385-26-000049:mdna:216 — amounts only
- 0001805385-26-000049:mdna:217 — amounts only
- 0001805385-26-000049:mdna:218 — lead-in line
- 0001805385-26-000049:mdna:223 — period comparison; debt cost amortization; template
- 0001805385-26-000049:mdna:226 — period comparison; lease payments; template
- 0001805385-26-000049:mdna:228 — lead-in (prior-year comparative)
- 0001805385-26-000049:mdna:229 — prior-year comparative; not a current-period change
- 0001805385-26-000049:mdna:230 — prior-year comparative
- 0001805385-26-000049:mdna:231 — prior-year comparative
- 0001805385-26-000049:mdna:232 — prior-year comparative
- 0001805385-26-000049:mdna:233 — prior-year comparative
- 0001805385-26-000049:mdna:234 — prior-year comparative
- 0001805385-26-000049:mdna:236 — period comparison; investing amounts
- 0001805385-26-000049:mdna:237 — prior-year comparative
- 0001805385-26-000049:mdna:239 — amounts only
- 0001805385-26-000049:mdna:243 — date rolled; PSU exception as before; contrast noted in founder share valuation item
- 0001805385-26-000049:mdna:244 — page number
- 0001805385-26-000049:mdna:245 — continuation; date rolled

### Item 4
- 0001805385-26-000049:item_4_controls:1 — heading
- 0001805385-26-000049:item_4_controls:2 — heading
- 0001805385-26-000049:item_4_controls:3 — boilerplate
- 0001805385-26-000049:item_4_controls:4 — heading
- 0001805385-26-000049:item_4_controls:5 — date rolled; still "not effective"
- 0001805385-26-000049:item_4_controls:6 — heading
- 0001805385-26-000049:item_4_controls:7 — boilerplate definition
- 0001805385-26-000049:item_4_controls:8 — insufficient — material weakness description; prior Item 4 not in input
- 0001805385-26-000049:item_4_controls:9 — insufficient — same
- 0001805385-26-000049:item_4_controls:10 — insufficient — same
- 0001805385-26-000049:item_4_controls:11 — insufficient — same
- 0001805385-26-000049:item_4_controls:12 — insufficient — same
- 0001805385-26-000049:item_4_controls:13 — historical restatement list; no change identifiable
- 0001805385-26-000049:item_4_controls:14 — lead-in
- 0001805385-26-000049:item_4_controls:15 — historical restatement
- 0001805385-26-000049:item_4_controls:16 — historical revision
- 0001805385-26-000049:item_4_controls:17 — insufficient — years listed include 2025; can't tell if new
- 0001805385-26-000049:item_4_controls:18 — boilerplate
- 0001805385-26-000049:item_4_controls:19 — insufficient — ITGC material weakness; prior Item 4 not in input
- 0001805385-26-000049:item_4_controls:20 — insufficient — same
- 0001805385-26-000049:item_4_controls:21 — heading
- 0001805385-26-000049:item_4_controls:22 — lead-in
- 0001805385-26-000049:item_4_controls:23 — insufficient — remediation dated 2025; prior Item 4 not in input
- 0001805385-26-000049:item_4_controls:24 — insufficient — same
- 0001805385-26-000049:item_4_controls:25 — insufficient — same
- 0001805385-26-000049:item_4_controls:26 — insufficient — same
- 0001805385-26-000049:item_4_controls:27 — insufficient — same
- 0001805385-26-000049:item_4_controls:28 — insufficient — same
- 0001805385-26-000049:item_4_controls:29 — lead-in
- 0001805385-26-000049:item_4_controls:30 — insufficient — ongoing remediation; prior Item 4 not in input
- 0001805385-26-000049:item_4_controls:31 — insufficient — same
- 0001805385-26-000049:item_4_controls:33 — boilerplate
- 0001805385-26-000049:item_4_controls:34 — boilerplate
- 0001805385-26-000049:item_4_controls:35 — heading
- 0001805385-26-000049:item_4_controls:36 — date rolled; no ICFR change reported

### 8-K 0001805385-26-000047, item 2.02 / exhibit 99.1
- 0001805385-26-000047:8k_2_02:1 — exhibit header
- 0001805385-26-000047:8k_2_02:2 — exhibit header
- 0001805385-26-000047:8k_2_02:3 — exhibit header
- 0001805385-26-000047:8k_2_02:4 — title
- 0001805385-26-000047:8k_2_02:5 — headline; covered by customer-count across item
- 0001805385-26-000047:8k_2_02:6 — headline; covered by outlook item
- 0001805385-26-000047:8k_2_02:7 — amounts only
- 0001805385-26-000047:8k_2_02:8 — amounts only
- 0001805385-26-000047:8k_2_02:9 — amounts only
- 0001805385-26-000047:8k_2_02:10 — amounts only
- 0001805385-26-000047:8k_2_02:11 — amounts only (includes restricted cash)
- 0001805385-26-000047:8k_2_02:12 — amount; covered by RPO item
- 0001805385-26-000047:8k_2_02:13 — dateline
- 0001805385-26-000047:8k_2_02:14 — CEO commentary; renewal claim not quantified; no account to test
- 0001805385-26-000047:8k_2_02:15 — heading
- 0001805385-26-000047:8k_2_02:16 — amounts only
- 0001805385-26-000047:8k_2_02:17 — heading
- 0001805385-26-000047:8k_2_02:18 — amounts only
- 0001805385-26-000047:8k_2_02:19 — amounts only
- 0001805385-26-000047:8k_2_02:20 — heading
- 0001805385-26-000047:8k_2_02:22 — guidance table; covered by outlook item
- 0001805385-26-000047:8k_2_02:24 — heading
- 0001805385-26-000047:8k_2_02:25 — call logistics
- 0001805385-26-000047:8k_2_02:26 — heading
- 0001805385-26-000047:8k_2_02:27 — company boilerplate
- 0001805385-26-000047:8k_2_02:28 — company boilerplate
- 0001805385-26-000047:8k_2_02:31 — definition footnote; covered by recurring revenue definition item
- 0001805385-26-000047:8k_2_02:32 — heading
- 0001805385-26-000047:8k_2_02:33 — forward-looking boilerplate
- 0001805385-26-000047:8k_2_02:34 — contact
- 0001805385-26-000047:8k_2_02:35 — contact
- 0001805385-26-000047:8k_2_02:36 — contact
- 0001805385-26-000047:8k_2_02:37 — contact
- 0001805385-26-000047:8k_2_02:38 — heading
- 0001805385-26-000047:8k_2_02:39 — heading
- 0001805385-26-000047:8k_2_02:40 — heading
- 0001805385-26-000047:8k_2_02:41 — heading
- 0001805385-26-000047:8k_2_02:42 — amounts only (income statement)
- 0001805385-26-000047:8k_2_02:43 — heading
- 0001805385-26-000047:8k_2_02:44 — heading
- 0001805385-26-000047:8k_2_02:45 — heading
- 0001805385-26-000047:8k_2_02:46 — heading
- 0001805385-26-000047:8k_2_02:47 — amounts only (balance sheet)
- 0001805385-26-000047:8k_2_02:48 — heading
- 0001805385-26-000047:8k_2_02:49 — heading
- 0001805385-26-000047:8k_2_02:50 — heading
- 0001805385-26-000047:8k_2_02:51 — heading
- 0001805385-26-000047:8k_2_02:52 — amounts only (cash flow)
- 0001805385-26-000047:8k_2_02:53 — caption
- 0001805385-26-000047:8k_2_02:54 — amounts only
- 0001805385-26-000047:8k_2_02:55 — heading
- 0001805385-26-000047:8k_2_02:56 — heading
- 0001805385-26-000047:8k_2_02:57 — heading
- 0001805385-26-000047:8k_2_02:58 — amounts only; used by customer-count across item
- 0001805385-26-000047:8k_2_02:60 — heading
- 0001805385-26-000047:8k_2_02:61 — heading
- 0001805385-26-000047:8k_2_02:62 — heading
- 0001805385-26-000047:8k_2_02:63 — heading
- 0001805385-26-000047:8k_2_02:64 — amounts only
- 0001805385-26-000047:8k_2_02:65 — heading
- 0001805385-26-000047:8k_2_02:66 — heading
- 0001805385-26-000047:8k_2_02:67 — heading
- 0001805385-26-000047:8k_2_02:68 — heading
- 0001805385-26-000047:8k_2_02:69 — amounts only
- 0001805385-26-000047:8k_2_02:70 — footnote; definition change "as previously disclosed"
- 0001805385-26-000047:8k_2_02:71 — amounts only
- 0001805385-26-000047:8k_2_02:72 — footnote; "as previously disclosed"
- 0001805385-26-000047:8k_2_02:73 — heading
- 0001805385-26-000047:8k_2_02:74 — heading
- 0001805385-26-000047:8k_2_02:75 — heading
- 0001805385-26-000047:8k_2_02:76 — heading
- 0001805385-26-000047:8k_2_02:77 — amounts only
- 0001805385-26-000047:8k_2_02:78 — footnote; refinement made in Q3 2025
- 0001805385-26-000047:8k_2_02:79 — heading
- 0001805385-26-000047:8k_2_02:80 — heading
- 0001805385-26-000047:8k_2_02:81 — heading
- 0001805385-26-000047:8k_2_02:82 — heading
- 0001805385-26-000047:8k_2_02:83 — amounts only
- 0001805385-26-000047:8k_2_02:84 — footnote caption
- 0001805385-26-000047:8k_2_02:85 — amounts only

## 8-K index entries with no body in my input (since the prior 10-Q of 2026-05-12)

- 2026-05-13 0001805385-26-000032 — 9.01 only; body not in input; I can't tell which exhibit was furnished.
- 2026-06-22 0001805385-26-000036 — 5.07; body not in input.
- 2026-08-10 0001805385-26-000040 — 8.01; body not in input. It was filed the day before the earnings release, after the August 5–6 derivative settlement events and in the quarter of the first SEC accrual. The supervisor may want to pull it.
- No late-filing notices since 2025-05-15.

## Counts

- Items: 45. Management explanations (`explanation: true`): 7.
- Paragraphs marked `insufficient`: 24 (notes 4, MD&A 4, Item 4 16).
