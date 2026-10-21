# Notes-text reader: VISN 10-Q 0001193125-26-336708, quarter ended June 30, 2026

## What I read

I read all six input files to the end:
- `input_notes.md`
- `input_notes_history.md`
- `input_mdna.md`
- `input_controls.md`
- `input_8k.md`, the Item 2.02 release 0001193125-26-336705 and the 8-K item index
- `input_prior_predictions.md`, which has no prior flags on record

These are not in my directory, so nothing here comes from them:
- the auditor's report (none is carried for this 10-Q)
- an Item 1A diff
- an Exhibit 21 diff
- any Exhibit 10

I found no trend table, prices, abnormal returns, short interest, other-company files, prior probabilities or outcome window. The press release contains condensed statements as part of the 8-K body. I read those only for their captions and stated figures.

**Conventions**
- **No arithmetic.** Where two passages give different figures for the same caption and period, I quote both and leave the reconciliation to the numbers reader and the supervisor.
- **`expected_direction`:**
  - `none` means the change is structural or a disclosure change and implies no movement in a number.
  - `insufficient` means the change bears on a number, but the prose does not let me state a direction without computing.
- **`explanation`** is set to `true` only where management gives a cause for a receivables, inventory or reserve figure.

## Items

```json
[
  {
    "id": "structure_and_disclosure_changes_business_description_drops_enterprise_wifi",
    "what_changed": "The Note 1 business description no longer says the solutions deliver 'Wi-Fi to their subscribers' or 'allow enterprises to experience constant wireless and wired connectivity'. It now describes service-provider solutions only. MD&A (mdna:5) carries the same narrowed description. The narrowing follows RUCKUS's move to held for sale.",
    "account": "net sales",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "to deliver media, voice and Internet Protocol (IP) data services.",
    "paragraph_id": "0001193125-26-336708:notes:3",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_ruckus_held_for_sale_discontinued",
    "what_changed": "Note 2 now states that RUCKUS met the held-for-sale criteria in Q2 2026. Management determined, qualitatively and quantitatively, that the sale is a strategic shift, so RUCKUS results are in discontinued operations and its assets and liabilities are held for sale. The Q1 subsequent-events note had said RUCKUS was 'expected to meet' these criteria in Q2; that is now stated as met. MD&A (mdna:8) repeats it.",
    "account": "current assets held for sale; current liabilities held for sale; income from discontinued operations",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "met the “held for sale” criteria in the second quarter of 2026",
    "paragraph_id": "0001193125-26-336708:notes:48",
    "explanation": false
  },
  {
    "id": "articulation_and_the_filed_history_ruckus_recast_all_periods",
    "what_changed": "New Note 1 paragraph: RUCKUS results are reclassified to discontinued operations for all periods presented, and its assets and liabilities are shown as held for sale for current and prior periods. Every continuing-operations figure for Q1 2026 and 2025 in this filing is therefore on a different basis from the same period as filed. The Q1 EPS table, the Q1 customer-concentration percentages and the Q1 tax explanation were removed (note history) and are not restated in prose. The press release (8k_2_02:18) says amounts 'have been recast'.",
    "account": "net sales and income from continuing operations (as recast against as filed)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "the results of operations directly attributable to the RUCKUS segment have been reclassified to discontinued operations for all periods presented on the Condensed Consolidated Statements of Operations",
    "paragraph_id": "0001193125-26-336708:notes:4",
    "explanation": false
  },
  {
    "id": "articulation_and_the_filed_history_rollforward_opening_balances_recast",
    "what_changed": "The warranty roll-forward is now shown for three and six months on the recast basis, with RUCKUS excluded. The filed Q1 roll-forward (note history) was on the old basis. The allowance roll-forward (notes:89) and the contract-balance table (notes:92, including its December 31, 2025 column) were recast the same way. No text bridges the filed Q1 closing balances to the recast opening balances; that reconciliation is for the numbers reader.",
    "account": "product warranty accrual; allowance for doubtful accounts; contract liabilities",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Product warranty accrual, beginning of period",
    "paragraph_id": "0001193125-26-336708:notes:16",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_customer_concentration_charter_named",
    "what_changed": "The concentration note now names Charter as a customer of 10% or more: 12% and 10% of Q2 and six-month net sales, and 15% and 14% in the 2025 periods. It states Comcast at 59% and 60%, and 48% and 42% in 2025. TD Synnex, named in Q1 as a RUCKUS customer, is no longer named. The sentence saying Comcast was a customer of both Aurora and RUCKUS was removed.",
    "account": "net sales",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Net sales to Charter Communications, Inc. (Charter) accounted for approximately 12% and 10%",
    "paragraph_id": "0001193125-26-336708:notes:9",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_receivable_concentration_comcast_charter",
    "what_changed": "Receivables concentration at June 30, 2026 now names Comcast (48%) and Charter (15%). The Q1 note named Comcast (44%) and TD Synnex (10%) at March 31, 2026. The allowance is estimated under the ASU 2025-05 practical expedient, which assumes balance-sheet-date conditions persist (notes:41). No text addresses credit risk on these two counterparties.",
    "account": "accounts receivable; allowance for doubtful accounts",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Accounts receivable from Comcast and Charter represented approximately 48% and 15%",
    "paragraph_id": "0001193125-26-336708:notes:9",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_restricted_cash_collateral_released",
    "what_changed": "The restricted-cash paragraph now states in the note body, not as a subsequent event, that the letter-of-credit cash deposits were returned and the restrictions released when the revolving facility was entered in April 2026. It still gives restricted cash only 'As of March 31, 2026': $56.5 million, of which $11.4 million is current and $45.1 million noncurrent. No June 30, 2026 restricted-cash amount is stated.",
    "account": "restricted cash (prepaid expenses and other current assets; other noncurrent assets)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "the related cash deposits were returned and the restrictions released.",
    "paragraph_id": "0001193125-26-336708:notes:22",
    "explanation": false
  },
  {
    "id": "across_documents_restricted_cash_line_in_press_release_cash_flow",
    "what_changed": "The press-release cash-flow statement has a 'Less: Restricted cash in prepaid expenses and other assets' line showing 56.5 in the three-months-ended June 30, 2026 column and '—' in the six-month column. Its 'Cash, cash equivalents and restricted cash at end of period' line shows 95.1 in the three-month column and 151.6 in the six-month column; both columns are for June 30, 2026. Both columns end at 151.6 of cash and cash equivalents. Note 1 says the restrictions were released in April 2026. The numbers reader should reconcile the three-month column.",
    "account": "restricted cash; cash and cash equivalents",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Less: Restricted cash in prepaid expenses and other assets",
    "paragraph_id": "0001193125-26-336705:8k_2_02:58",
    "explanation": false
  },
  {
    "id": "earnings_quality_tax_benefit_on_pretax_loss",
    "what_changed": "New Q2 and six-month tax paragraph: an income tax benefit of $28.7 million on a Q2 pretax loss of $2.6 million. The note gives three causes: $21.0 million (Q2) and $21.2 million (six months) of tax benefit from the equity compensation plan; $7.1 million from remeasuring certain net deferred taxes; and U.S. anti-deferral provisions as a partial offset. The press release headlines GAAP income from continuing operations of $26.1 million for the quarter (8k_2_02:7). The text does not say whether these tax items recur. MD&A (mdna:50) repeats it.",
    "account": "income tax (expense) benefit; income from continuing operations",
    "expected_direction": "insufficient",
    "horizon": "this quarter",
    "quote": "the Company recognized an income tax benefit of $28.7 million on a pretax loss of $2.6 million",
    "paragraph_id": "0001193125-26-336708:notes:30",
    "explanation": false
  },
  {
    "id": "articulation_and_the_filed_history_tax_planning_benefit_leaves_continuing_operations",
    "what_changed": "The Q1 note attributed Q1 2026 continuing-operations tax to a $196.6 million tax-planning-strategy benefit. That sentence was removed. The six-month continuing-operations tax paragraph (notes:30) now names no tax planning strategy for 2026. The new RUCKUS column in the discontinued-operations tables carries an income tax benefit line. No carried text says where the Q1 tax-planning benefit now sits. The CEO refers to a 'divesture tax strategy' (8k_2_02:16).",
    "account": "income tax (expense) benefit, continuing operations (as recast against as filed); income from discontinued operations",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "primarily due to $196.6 million of tax benefit recognized in the quarter associated with a tax planning strategy.",
    "paragraph_id": "0001193125-26-193963:note_history:21",
    "explanation": false
  },
  {
    "id": "earnings_quality_discontinued_operations_tax_lines_unexplained",
    "what_changed": "The Q2 discontinued-operations table now has a RUCKUS column, whose income tax line shows a benefit of 320.9 for Q2 2026 (512.5 for the six months, notes:69). In the same table the CCS column shows Q2 2026 income tax expense of (76.1) and a gain on disposal of 0.4. The OWN column shows a gain on disposal of 1.0. No paragraph in the notes or MD&A carried here explains the RUCKUS benefit or the Q2 CCS tax expense.",
    "account": "income from discontinued operations, net of income taxes",
    "expected_direction": "insufficient",
    "horizon": "this quarter",
    "quote": "Income tax (expense) benefit",
    "paragraph_id": "0001193125-26-336708:notes:66",
    "explanation": false
  },
  {
    "id": "articulation_and_the_filed_history_prior_year_valuation_allowance_dropped",
    "what_changed": "The Q1 note explained Q1 2025 tax partly by a $29.6 million additional valuation allowance on federal and state interest limitation carryforwards. The recast 2025 explanation (notes:31, mdna:51) names federal tax credits, the $361.1 million tax planning strategy and anti-deferral provisions, and no longer mentions the valuation allowance. All interest expense is now presented in discontinued operations (notes:67).",
    "account": "income tax (expense) benefit, 2025 comparative; valuation allowance",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Offsetting these benefits were the unfavorable impacts of $29.6 million of an additional valuation allowance recorded in the quarter related to current year federal and state interest limitation carryforwards",
    "paragraph_id": "0001193125-26-193963:note_history:22",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_eps_dividend_equivalents_not_participating",
    "what_changed": "The EPS policy has two new sentences. Dividend equivalents on unvested RSUs and PSUs are payable only on vesting and remain subject to forfeiture. The awards are therefore not participating securities, and the two-class method is not applied. This is a judgment that matters for the special distributions, whose dividend equivalents on unvested awards were recorded at declaration (notes:157). The discontinued-operations EPS paragraph (notes:34) adds only a parenthetical.",
    "account": "earnings per share",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "these awards do not represent participating securities under ASC 260, Earnings per Share",
    "paragraph_id": "0001193125-26-336708:notes:33",
    "explanation": false
  },
  {
    "id": "articulation_and_the_filed_history_preferred_dilution_now_antidilutive",
    "what_changed": "New paragraph: no Convertible Preferred was outstanding in Q2. For the six months ended June 30, 2026, 2.3 million as-if-converted preferred shares were excluded as antidilutive. The filed Q1 EPS table (removed, note history) counted 4.7 million as-if-converted preferred shares as dilutive for Q1 2026. The recast six-month table (notes:38) shows '—' for preferred dilution. The dilution treatment of the January preferred shares has changed with the recast.",
    "account": "diluted weighted average shares; diluted EPS from continuing operations",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "For the three months ended June 30, 2026, there were no shares related to the Convertible Preferred Stock that were excluded from the diluted share count and considered antidilutive",
    "paragraph_id": "0001193125-26-336708:notes:36",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_pending_accounting_standards_removed",
    "what_changed": "Five pending-standard disclosures from the Q1 filing were removed without comment: ASU 2025-12, 2025-11, 2025-10, 2025-09 (hedge accounting) and 2025-07 (derivatives scope and share-based noncash consideration in revenue contracts). The Q1 filing said each was being evaluated. Only ASU 2025-06 and ASU 2024-03 remain as pending.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "In December 2025, the FASB issued ASU No. 2025-12, Codification Improvements.",
    "paragraph_id": "0001193125-26-193963:note_history:25",
    "explanation": false
  },
  {
    "id": "results_against_expectations_ruckus_transaction_cost_estimate_withdrawn",
    "what_changed": "The Q1 subsequent-events note said the Company expected about $150 million of transaction-related expenses and taxes on the RUCKUS sale, with closing expected in the second half of 2026 subject to regulatory approvals. That sentence was removed. This filing reports that the sale closed on July 1, 2026. It gives no updated cost estimate and no expected gain or loss on the sale.",
    "account": "transaction costs and income taxes on the RUCKUS disposal (discontinued operations)",
    "expected_direction": "insufficient",
    "horizon": "next quarter",
    "quote": "The Company expects to incur approximately $150 million in transaction",
    "paragraph_id": "0001193125-26-193963:note_history:51",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_ruckus_sale_closed",
    "what_changed": "New subsequent event: RUCKUS was sold to Belden on July 1, 2026, cash-free and debt-free, for approximately $1.846 billion in cash, 'subject to certain adjustments'. No adjustment is quantified. Revolver commitments were cut the same day (notes:111), and a Belden TSA starts in Q3 (mdna:9). The RUCKUS assets and liabilities held for sale at June 30, 2026 should leave the balance sheet in Q3, with a gain or loss on disposal in discontinued operations.",
    "account": "current assets held for sale; current liabilities held for sale; gain on disposal of discontinued operations",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "On July 1, 2026, the Company completed the previously announced sale of its RUCKUS segment to Belden",
    "paragraph_id": "0001193125-26-336708:notes:161",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_own_das_disposal_adjustment",
    "what_changed": "New footnote: in Q2 2026 the Company recorded a $1.0 million adjustment to the carrying value of the OWN/DAS disposal group, with related tax effects, which affected the gain on disposal. That disposal closed on January 31, 2025. The text gives no cause and does not say which way the gain moved. The Q2 discontinued-operations table shows a gain on disposal of 1.0 in the OWN column.",
    "account": "gain on disposal of discontinued operations (OWN/DAS)",
    "expected_direction": "insufficient",
    "horizon": "this quarter",
    "quote": "the Company recorded a $1.0 million adjustment to the carrying value of the OWN/DAS disposal group",
    "paragraph_id": "0001193125-26-336708:notes:76",
    "explanation": false
  },
  {
    "id": "revenue_recognition_amphenol_msa_negative_net_revenue",
    "what_changed": "The Amphenol MSA paragraph reports negative net revenue for Q2 and the six months of 2026, presented in discontinued operations. It puts the twelve-month manufacturing obligation in the past tense ('was obligated') while also saying the Company 'continues to manufacture and supply'. Nothing explains the negative revenue; no credits, returns or price adjustments are mentioned. The discontinued-operations cash table (notes:79) shows Amphenol MSA inventory sales of 8.1 for the six months of 2026.",
    "account": "net sales in discontinued operations (OWN, Amphenol MSA)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "the Company recognized net revenues of $(0.3) million and $(0.5) million for the three and six months ended June 30, 2026",
    "paragraph_id": "0001193125-26-336708:notes:60",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_buyer_supply_agreements_kept_in_continuing_operations",
    "what_changed": "The paragraph describes a 36-month Sales and Supply Agreement and an indefinite-term Master Professional Services Agreement with Amphenol, the buyer of CCS and OWN/DAS. Management concludes these are not a continuation of the disposed business, so their revenues and expenses stay in continuing operations. Segment footnotes (notes:126, notes:139) say corporate-and-other revenue includes products tied to prior divestitures. The prior wording is not in my input, so I cannot show exactly what changed.",
    "account": "net sales (corporate and other, continuing operations)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The Company has evaluated these arrangements and concluded that while they represent ongoing business activity, they do not constitute a continuation of the disposed business.",
    "paragraph_id": "0001193125-26-336708:notes:61",
    "explanation": false
  },
  {
    "id": "earnings_quality_reverse_tsa_costs_and_tsa_income",
    "what_changed": "The TSA paragraph now reports costs under the reverse TSA with Amphenol of $3.9 million for Q2 and $7.9 million for the six months, mainly in SG&A. Amphenol TSA income for the same periods is $0.5 million and $1.6 million. The paragraph says the Company may incur incremental costs if services continue beyond the initial transition period. The cash table (notes:79) shows Amphenol TSA fees as a (5.7) outflow for the six months of 2026.",
    "account": "selling, general and administrative expense; transition service agreement income",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "The Company incurred costs under the reverse TSA of $3.9 million and $7.9 million for the three and six months ended June 30, 2026, respectively",
    "paragraph_id": "0001193125-26-336708:notes:83",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_revolver_terms_borrowing_base",
    "what_changed": "The financing note now gives the terms of the April 7, 2026 facility:\n- $300.0 million of commitments\n- a borrowing base based mainly on eligible receivables and inventory\n- Term SOFR with a 0.00% floor, or an alternate base rate, plus a margin\n- maturity on April 7, 2031\n- first-priority liens on substantially all assets\nThe Q1 text named Citibank as agent and a $100.0 million letter-of-credit sublimit; neither appears now. Because the borrowing base rests on receivables and inventory, the reported balances in those accounts directly affect availability.",
    "account": "revolving credit facility availability; accounts receivable; inventories",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Availability under the Revolving Credit Facility is subject to a borrowing base calculated primarily based on eligible accounts receivable and inventory.",
    "paragraph_id": "0001193125-26-336708:notes:110",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_revolver_commitments_reduced",
    "what_changed": "New: effective July 1, 2026, in connection with the RUCKUS sale, revolver commitments were reduced from $300.0 million to $246.9 million, subject to the borrowing base. The MD&A liquidity paragraph (mdna:72) still describes the facility as up to $300.0 million and does not mention the reduction.",
    "account": "revolving credit facility commitments and availability",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "the aggregate commitments under the Revolving Credit Facility were reduced from $300.0 million to $246.9 million",
    "paragraph_id": "0001193125-26-336708:notes:111",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_revolver_availability_after_letters_of_credit",
    "what_changed": "New: there were no borrowings at June 30, 2026. $39.9 million of letters of credit are outstanding under the facility; these were previously cash-collateralized (notes:22). Availability after letters of credit, under the borrowing base, is $137.0 million. The press release (8k_2_02:37) gives total liquidity of approximately $288.6 million.",
    "account": "revolving credit facility availability; letters of credit",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Based on the applicable borrowing base limitations, the availability after outstanding letters of credit under the facility was $137.0 million.",
    "paragraph_id": "0001193125-26-336708:notes:112",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_revolver_deferred_financing_costs",
    "what_changed": "New: about $2.6 million of upfront facility fees were capitalized as deferred financing costs and are being amortized to interest expense over the facility term. An interest expense line now appears in continuing operations for Q2 2026, and MD&A (mdna:48) says the Company expects to incur interest expense in the future.",
    "account": "interest expense (continuing operations); deferred financing costs",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "which were capitalized as deferred financing costs and are being amortized to interest expense over the term of the facility.",
    "paragraph_id": "0001193125-26-336708:notes:113",
    "explanation": false
  },
  {
    "id": "earnings_quality_interest_income_from_sale_proceeds",
    "what_changed": "MD&A attributes continuing-operations interest income to interest earned on the CCS sale proceeds. MD&A (mdna:92) and Note 8 (notes:156) say those proceeds funded the $2,316.3 million special distribution paid in Q2. A further $5.00 per share was declared on August 5, 2026 (notes:162). The prose therefore ties interest income to a cash balance that is being paid out.",
    "account": "interest income",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "The increase in interest income compared to the prior year periods was primarily driven by interest earned on the net proceeds related to the sale of the CCS segment.",
    "paragraph_id": "0001193125-26-336708:mdna:48",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_single_reportable_segment",
    "what_changed": "With RUCKUS held for sale and then sold, the segment note now says the Company has one remaining reportable segment, Aurora. The segment tables now show Aurora and corporate and other, and the segment wording has moved from plural to singular (notes:119, notes:121).",
    "account": "segment information",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "the Company has one remaining reportable segment.",
    "paragraph_id": "0001193125-26-336708:notes:115",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_ruckus_corporate_costs_reallocated_to_aurora",
    "what_changed": "New: from Q3 2026, corporate and other costs previously allocated to RUCKUS will be reallocated to the remaining segment, Aurora, partly offset by Belden TSA income. The same statement appears in the segment and restructuring footnotes (notes:125, notes:129, notes:132, notes:135, notes:145) and in the press-release footnotes. Aurora results, which are the Core measures, will then carry these costs. The CFO cites 'stranded costs associated with the divestitures'.",
    "account": "Aurora segment adjusted EBITDA and operating income; transition service agreement income",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "Beginning in the third quarter of 2026, the corporate and other costs related to the RUCKUS segment will be reallocated to our remaining segment and partially offset by income from the Transition Service Agreement with Belden (Belden TSA).",
    "paragraph_id": "0001193125-26-336708:mdna:9",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_core_measure_redefined_as_aurora_only",
    "what_changed": "The Core financial measures are now defined as the Aurora segment alone. They exclude corporate costs previously allocated to RUCKUS, CCS, OWN and DAS, so RUCKUS is now among the divested businesses whose allocated costs are excluded. The press release (8k_2_02:11, 8k_2_02:50) uses the same definition, and the prior-period Core figures in this filing are on it. The prior wording is not in my input.",
    "account": "Core adjusted EBITDA and Core operating income (non-GAAP)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "which reflect the results of the Aurora segment and exclude general corporate costs that were previously allocated to the RUCKUS segment, CCS segment, OWN segment and DAS business unit",
    "paragraph_id": "0001193125-26-336708:mdna:10",
    "explanation": false
  },
  {
    "id": "across_documents_transaction_costs_prose_vs_reconciliation_table",
    "what_changed": "mdna:6 gives transaction, transformation and integration costs of $7.6 million (Q2 2026), $5.6 million (six months 2026), $12.3 million (Q2 2025) and $10.0 million (six months 2025). The MD&A reconciliation table (mdna:100) shows 7.6, 12.3, 5.7 and 10.0 on that caption for Q2 2026, six months 2026, Q2 2025 and six months 2025. The press-release reconciliation shows 7.6 and 5.7 for Q2 2026 and Q2 2025. For six months 2026 and Q2 2025, the prose figures are not the figures the tables give.",
    "account": "transaction, transformation and integration costs",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "$7.6 million and $5.6 million of transaction, transformation and integration costs for the three and six months ended June 30, 2026, respectively",
    "paragraph_id": "0001193125-26-336708:mdna:6",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_net_sales_pricing_and_mix",
    "what_changed": "New Q2 explanation: net sales decreased, mainly because of unfavorable product mix, lower pricing and lower sales volume. For the six months, the prose says net sales increased on higher volume, partly offset by unfavorable mix and lower pricing. Lower pricing and unfavorable mix are named as headwinds in both periods. mdna:63 repeats this for Aurora.",
    "account": "net sales",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "primarily driven by unfavorable product mix, lower pricing and lower sales volume",
    "paragraph_id": "0001193125-26-336708:mdna:20",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_legacy_business_decline",
    "what_changed": "The press release attributes the Aurora net sales decrease to a decrease in the legacy business, partly offset by an increase in the Access Technologies business. The 10-Q MD&A does not use this legacy versus Access Technologies split.",
    "account": "net sales (Aurora legacy business)",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "driven by a decrease in the legacy business, partially offset by an increase in the Access Technologies business",
    "paragraph_id": "0001193125-26-336705:8k_2_02:33",
    "explanation": false
  },
  {
    "id": "across_documents_license_sales_cited_only_in_press_release",
    "what_changed": "The CFO attributes the year-over-year decline partly to strong license sales in Q2 2025, along with memory chip pricing and stranded costs. None of the MD&A explanations of net sales, gross profit or Aurora results (mdna:20, mdna:26, mdna:63, mdna:64) mentions license sales. Those explanations cite mix, pricing, volume, input costs, SG&A and R&D.",
    "account": "net sales; gross profit; Aurora adjusted EBITDA",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "down versus the prior year due to strong license sales in the second quarter of 2025, memory chip pricing and stranded costs associated with the divestitures",
    "paragraph_id": "0001193125-26-336705:8k_2_02:17",
    "explanation": false
  },
  {
    "id": "across_documents_lower_input_costs_vs_memory_chip_pricing",
    "what_changed": "MD&A says Q2 and six-month gross profit decreased mainly on unfavorable mix and lower pricing, partially offset by lower input costs. The CFO (8k_2_02:17) names memory chip pricing as a cause of the Q2 decline, and 'continued challenges with memory chip pricing and availability' as the reason for cutting the guideposts. The forward-looking statements (mdna:110) name memory chip cost and availability. MD&A credits input costs as an offset, while the CFO names them as a headwind.",
    "account": "gross profit; cost of sales",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "primarily due to unfavorable product mix and lower pricing, partially offset by lower input costs",
    "paragraph_id": "0001193125-26-336708:mdna:26",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_variable_incentive_compensation_accrual",
    "what_changed": "New SG&A driver: variable incentive compensation expense decreased by $7.6 million for Q2 and $8.2 million for the six months. For the same six months, MD&A (mdna:83) cites higher variable incentive compensation payments as a use of cash. The incentive accrual is a discretionary estimate. The text does not say whether the lower expense reflects lower targets, a reversal or the recast.",
    "account": "selling, general and administrative expense; compensation and employee benefit liabilities",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "the decrease was primarily due to decreased variable incentive compensation expense of $7.6 million and $8.2 million, respectively",
    "paragraph_id": "0001193125-26-336708:mdna:30",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_legal_expense_decrease",
    "what_changed": "New SG&A driver: legal expense decreased by $4.9 million for Q2 and $11.5 million for the six months. The legal proceedings note (notes:18) names no specific matter, settlement or resolution. MD&A (mdna:73) lists litigation settlements among the uses of liquidity. The text does not say which matters drove legal expense in the prior year or why it decreased.",
    "account": "selling, general and administrative expense (legal)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "decreased legal expense of $4.9 million and $11.5 million, respectively",
    "paragraph_id": "0001193125-26-336708:mdna:30",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_aurora_rd_spending_lower",
    "what_changed": "New: R&D expense decreased by $12.3 million for Q2 and $18.4 million for the six months, due to lower spending within the Aurora segment. The CEO (8k_2_02:16) speaks of possibly 'investing more aggressively in existing or new technology'.",
    "account": "research and development expense",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "due to lower spending within the Aurora segment compared to the prior year periods",
    "paragraph_id": "0001193125-26-336708:mdna:32",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_restructuring_reserve_new_plan",
    "what_changed": "Management attributes the Q2 and six-month net restructuring costs ($8.4 million and $15.1 million) mainly to the new plan to right-size the cost structure after the CCS divestiture. The paragraph states:\n- payments of $4.6 million (Q2) and $9.9 million (six months)\n- expected cash payments of $6.6 million in the rest of 2026 and $0.9 million in 2027\n- that further actions are expected, with charges that could be material\nThe restructuring note says the $2.3 million left from the prior program at December 31, 2025 is expected to be settled in 2027 (notes:149). The same figures appear in notes:153 and mdna:6.",
    "account": "restructuring liabilities (accrued and other liabilities); restructuring costs, net",
    "expected_direction": "insufficient",
    "horizon": "12 months",
    "quote": "The net restructuring costs recorded in the three and six months ended June 30, 2026 were primarily related to our new restructuring plan",
    "paragraph_id": "0001193125-26-336708:mdna:38",
    "explanation": true
  },
  {
    "id": "earnings_quality_other_income_gains_on_financial_assets",
    "what_changed": "MD&A says other income (expense), net for Q2 and the six months benefited from gains on 'certain financial assets'. The notes carried here do not identify these assets.",
    "account": "other income (expense), net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Other income (expense), net for the three and six months ended June 30, 2026 was favorably impacted by gains on certain financial assets.",
    "paragraph_id": "0001193125-26-336708:mdna:44",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_aurora_segment_profit_drivers",
    "what_changed": "New Aurora explanation: operating income and adjusted EBITDA decreased for the three and six months on unfavorable mix, lower pricing, lower sales volume and higher SG&A, partly offset by lower input costs and lower R&D. Two contradictions:\n- The consolidated SG&A paragraph (mdna:30) says SG&A decreased.\n- The next sentence of the same paragraph says six-month Aurora results benefited from higher sales volume, so the prose names both lower and higher volume for the six months.",
    "account": "Aurora segment operating income; Aurora adjusted EBITDA",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "primarily driven by unfavorable product mix, lower pricing, lower sales volume and higher SG&A, partially offset by lower input costs and lower R&D costs",
    "paragraph_id": "0001193125-26-336708:mdna:64",
    "explanation": false
  },
  {
    "id": "across_documents_special_distribution_amount_stated_differently",
    "what_changed": "mdna:76 gives the April special distribution paid as approximately $2,316.6 million. mdna:92, notes:158 and both cash-flow presentations give $2,316.3 million for the same payment.",
    "account": "special distribution paid (financing cash flows); retained earnings",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "special cash distribution of approximately $2,316.6 million",
    "paragraph_id": "0001193125-26-336708:mdna:76",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_working_capital_inventory_and_prepaid_build",
    "what_changed": "Management explains the six-month increase in working capital (excluding cash and held-for-sale items) mainly by increases in prepaid expenses and inventory and a decrease in accrued and other liabilities, partly offset by increased accounts payable. No cause is given for the inventory increase, and the contents of prepaid expenses are not identified. The CFO cites memory chip pricing and availability, and the revolver borrowing base rests on eligible inventory and receivables (notes:110).",
    "account": "inventories; prepaid expenses and other current assets",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "primarily due to increases in prepaid expenses and inventory balances and a decrease in accrued and other liabilities, partially offset by increased accounts payable",
    "paragraph_id": "0001193125-26-336708:mdna:77",
    "explanation": true
  },
  {
    "id": "across_documents_total_capitalization_explanation_omits_distribution",
    "what_changed": "MD&A explains the six-month net decrease in total capitalization by debt repayment, partly offset by net income. mdna:76 says the special distribution contributed to the decrease in stockholders' equity. mdna:71 says total capitalization included the Convertible Preferred Stock at December 31, 2025. The capitalization explanation names neither the distribution nor the preferred redemption.",
    "account": "total capitalization; stockholders' equity",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "is primarily driven by the repayment of debt in connection with the sale of the CCS segment, partially offset by net income reflected for the period",
    "paragraph_id": "0001193125-26-336708:mdna:77",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_operating_cash_outflow_drivers",
    "what_changed": "New explanation: the six-month increase in cash used in operations came from higher working-capital use, higher variable incentive compensation payments and cash taxes paid, partly offset by lower interest. The cash flows include discontinued operations, which are not segregated.",
    "account": "net cash used in operating activities",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "primarily driven by a higher use of cash from working capital and higher variable incentive compensation payments and cash taxes paid",
    "paragraph_id": "0001193125-26-336708:mdna:83",
    "explanation": false
  },
  {
    "id": "across_documents_capex_decrease_figure_matches_current_capex",
    "what_changed": "The investing paragraph says investing cash benefited from 'decreased capital expenditures of $4.2 million'. The adjacent table (mdna:85) shows (4.2) on the 2026 additions line and (28.1) on the 2025 line. The figure the prose gives for the decrease is the same as the table's 2026 additions figure.",
    "account": "additions to property, plant and equipment",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "decreased capital expenditures of $4.2 million compared to the prior year period",
    "paragraph_id": "0001193125-26-336708:mdna:86",
    "explanation": false
  },
  {
    "id": "across_documents_december_debt_table_lists_retired_notes",
    "what_changed": "The December 31, 2025 column of the debt table shows 1,500.0 for the 6.00% senior secured notes due March 2026 and 1,250.0 for the 4.75% senior secured notes due September 2029. The column is carried from Q1 with only its header date changed (note history), so this is not new this period. mdna:90 says the $1,500.0 million of 2026 Secured Notes were repurchased in full, and $299.0 million of 2029 Secured Notes repurchased, during the six months ended June 30, 2025. mdna:89 and notes:53 say $951.0 million of 2029 Secured Notes were redeemed in January 2026. The prose says the 2026 notes were repurchased in full in the first half of 2025, yet the table carries them at December 31, 2025.",
    "account": "long-term debt (December 31, 2025 comparative)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "6.00% senior secured notes due March 2026",
    "paragraph_id": "0001193125-26-336708:notes:108",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_special_distribution_dividend_equivalents_payable",
    "what_changed": "New Note 8: $2,316.3 million of the April distribution was paid in Q2. Dividend equivalents on unvested awards outstanding at June 30, 2026 will be paid as those awards vest. The accrued liabilities table (notes:98) has a new 'Special distribution payable' line of 33.6. The aggregate of the August distribution will also cover eligible equity awards (notes:162).",
    "account": "cash and cash equivalents; accrued and other liabilities (special distribution payable)",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "Dividend equivalents associated with unvested awards that remained outstanding at June 30, 2026 will be paid upon vesting of the related awards.",
    "paragraph_id": "0001193125-26-336708:notes:158",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_distribution_recorded_including_unvested_dividend_equivalents",
    "what_changed": "New: at declaration the Company recorded a total distribution of $2,373.7 million against retained earnings, including dividend equivalents on unvested RSUs and PSUs. The EPS note (notes:33) says those dividend equivalents remain subject to forfeiture. The text does not say how forfeited dividend equivalents will be treated.",
    "account": "retained earnings; accrued and other liabilities",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Upon declaration, the Company recorded a total distribution of $2,373.7 million as a reduction of retained earnings.",
    "paragraph_id": "0001193125-26-336708:notes:157",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_buyback_authorization_unused",
    "what_changed": "The repurchase program of up to $100.0 million, approved April 29, 2026, has moved from subsequent events into Note 8. It now states that no shares had been repurchased as of June 30, 2026. The CEO says the Company will keep evaluating buybacks under this authority. MD&A (mdna:93) attributes the period's share surrenders to tax withholding on vested RSUs and PSUs.",
    "account": "treasury stock",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "There were no share repurchases as of June 30, 2026.",
    "paragraph_id": "0001193125-26-336708:notes:160",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_second_special_distribution_declared",
    "what_changed": "New subsequent event: a $5.00 per share special distribution was declared on August 5, 2026, payable August 27 to holders of record on August 17. The aggregate depends on shares and eligible equity awards at the record date. The CEO says this brings the total returned in 2026 to $15.00 per share, or $3.4 billion.",
    "account": "cash and cash equivalents; retained earnings",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "On August 5, 2026, the Company declared a special cash distribution (the Special Distribution) of $5.00 per share",
    "paragraph_id": "0001193125-26-336708:notes:162",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_year_end_cash_and_acquisition_plans",
    "what_changed": "New CEO guidance: after the special distribution, the Company expects to end 2026 with $700 to $750 million of cash and no debt. The funds are for organic and inorganic growth, including possible acquisitions to broaden markets, technology and customer base. No such plan appears in the 10-Q text carried here.",
    "account": "cash and cash equivalents",
    "expected_direction": "insufficient",
    "horizon": "12 months",
    "quote": "we expect to end the year with between $700 and $750 million of cash with no outstanding debt",
    "paragraph_id": "0001193125-26-336705:8k_2_02:16",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_expected_tax_refund_divestiture_strategy",
    "what_changed": "New CEO statement: a $160 million tax refund is expected in 2027 from the divestiture tax strategy. None of the notes or MD&A carried here mentions the refund or a related receivable. MD&A cites higher cash taxes paid (mdna:83), and it explains the working-capital increase partly by higher prepaid expenses without naming their contents (mdna:77).",
    "account": "income taxes receivable; cash and cash equivalents",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "In addition in 2027, we expect a tax refund of $160 million related to our divesture tax strategy.",
    "paragraph_id": "0001193125-26-336705:8k_2_02:16",
    "explanation": false
  },
  {
    "id": "results_against_expectations_adjusted_ebitda_guideposts_lowered",
    "what_changed": "New: the full-year Aurora adjusted EBITDA guideposts are $200 to $225 million. The CFO states these are down $25 million from the Q1 guideposts because of memory chip pricing and availability, and calls Q2 Aurora results 'generally aligned with our expectations'. The outlook reconciliation (8k_2_02:66) gives 2026 Aurora operating income of $70 to $85 million and restructuring, transaction and transformation costs of $25 to $32 million.",
    "account": "Aurora adjusted EBITDA (non-GAAP); Aurora operating income",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "Our full year adjusted EBITDA guideposts of $200 to $225 million are down $25 million versus the first quarter guideposts driven by continued challenges with memory chip pricing and availability.",
    "paragraph_id": "0001193125-26-336705:8k_2_02:17",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_memory_chip_component_risk",
    "what_changed": "The forward-looking statements list is carried as changed. It names memory chips among key components whose cost and availability could affect customer pricing and delivery timing. The press release (8k_2_02:52) has the same language, and the CFO ties the guidepost cut to memory chip pricing and availability. The prior wording is not in my input, so I cannot confirm this phrase is the new one.",
    "account": "cost of sales; gross profit; timing of net sales",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "changes in cost and availability of key components, including memory chips, and the potential effect on customer pricing and timing of delivery of products to customers",
    "paragraph_id": "0001193125-26-336708:mdna:110",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_stranded_cost_reduction_risk",
    "what_changed": "The same forward-looking list names successful execution of stranded-cost reduction initiatives as a risk. This fits with RUCKUS corporate costs moving to Aurora from Q3 2026 (mdna:9) and with the CFO citing stranded costs. The prior wording is not in my input.",
    "account": "selling, general and administrative expense; corporate and other costs",
    "expected_direction": "insufficient",
    "horizon": "12 months",
    "quote": "risks related to the successful execution of our initiatives related to stranded costs reductions",
    "paragraph_id": "0001193125-26-336708:mdna:110",
    "explanation": false
  },
  {
    "id": "across_documents_basic_eps_press_release_vs_note",
    "what_changed": "For Q2 2026, the press-release statement of operations shows basic earnings from discontinued operations per share of 1.18 and basic earnings per share of 1.24. The 10-Q EPS table (notes:38) shows 1.19 and 1.25 on the same lines. The continuing-operations and diluted lines show the same figures in both.",
    "account": "basic earnings per share",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Earnings from discontinued operations per share",
    "paragraph_id": "0001193125-26-336705:8k_2_02:56",
    "explanation": false
  },
  {
    "id": "across_documents_retained_divested_business_inventory_and_msa_term",
    "what_changed": "The segment-asset footnote explains that divested and other business assets reflect inventory kept for continuing involvement under the Amphenol MSA. At June 30, 2026 it lists:\n- $6.4 million of OWN/DAS inventory\n- $4.1 million of PON inventory not divested with CCS\n- $104.8 million of corporate and other assets, not further described\nNote 2 (notes:60) puts the MSA obligation period, up to twelve months after the OWN/DAS closing, in the past tense and reports negative MSA net revenue.",
    "account": "inventories retained from divested businesses (divested and other business assets)",
    "expected_direction": "insufficient",
    "horizon": "12 months",
    "quote": "reflects certain inventory retained by the Company related to continuing involvement in divested businesses pursuant to the Amphenol MSA",
    "paragraph_id": "0001193125-26-336708:notes:120",
    "explanation": true
  }
]
```

## Paragraphs carried as text that are not items

Paragraphs marked `[same as prior period ...]` are not listed. Paragraphs from the note change history are not listed separately; where a removal there is substantive, it is an item above.

**Item 4: controls**
- `0001193125-26-336708:item_4_controls:1`: heading
- `0001193125-26-336708:item_4_controls:2`: heading
- `0001193125-26-336708:item_4_controls:3`: standing conclusion that disclosure controls are effective. The prior Item 4 is not in my input, and no change in substance is visible.
- `0001193125-26-336708:item_4_controls:4`: heading
- `0001193125-26-336708:item_4_controls:5`: date rolled forward. It states no change in internal control over financial reporting.
- `0001193125-26-336708:item_4_controls:6`: page number

**MD&A**
- `0001193125-26-336708:mdna:2`: date rolled forward
- `0001193125-26-336708:mdna:5`: same narrowing as the business-description item (notes:3)
- `0001193125-26-336708:mdna:7`: wording only (cross-reference list)
- `0001193125-26-336708:mdna:8`: duplicate of the RUCKUS held-for-sale item (notes:48)
- `0001193125-26-336708:mdna:11`: page number
- `0001193125-26-336708:mdna:14`: heading, date rolled forward
- `0001193125-26-336708:mdna:15`: table, amounts only
- `0001193125-26-336708:mdna:16`: footnote duplicating the reallocation item (mdna:9) and the Core item (mdna:10)
- `0001193125-26-336708:mdna:19`: table, amounts only
- `0001193125-26-336708:mdna:21`: regional amounts only
- `0001193125-26-336708:mdna:22`: amounts only; the FX statement is standing
- `0001193125-26-336708:mdna:24`: table, amounts only
- `0001193125-26-336708:mdna:34`: table, amounts only
- `0001193125-26-336708:mdna:36`: date rolled forward; standing amortization explanation
- `0001193125-26-336708:mdna:40`: table, amounts only
- `0001193125-26-336708:mdna:42`: date rolled forward; standing FX explanation
- `0001193125-26-336708:mdna:46`: table, amounts only
- `0001193125-26-336708:mdna:49`: heading
- `0001193125-26-336708:mdna:50`: duplicate of notes:30 (tax item)
- `0001193125-26-336708:mdna:51`: duplicate of notes:31; covered by the valuation-allowance item
- `0001193125-26-336708:mdna:53`: table, amounts only
- `0001193125-26-336708:mdna:54`: footnote, wording only
- `0001193125-26-336708:mdna:55`: footnote duplicating mdna:9
- `0001193125-26-336708:mdna:57`: page number
- `0001193125-26-336708:mdna:58`: table, amounts only
- `0001193125-26-336708:mdna:59`: footnote, wording only
- `0001193125-26-336708:mdna:60`: footnote duplicating mdna:9
- `0001193125-26-336708:mdna:61`: cross-reference
- `0001193125-26-336708:mdna:63`: same causes as the mdna:20 item; regional amounts only
- `0001193125-26-336708:mdna:67`: table, amounts only
- `0001193125-26-336708:mdna:68`: amounts only
- `0001193125-26-336708:mdna:69`: amounts only
- `0001193125-26-336708:mdna:70`: covered by the revolver items (notes:110, notes:111)
- `0001193125-26-336708:mdna:71`: wording only (definition); cited in the capitalization item
- `0001193125-26-336708:mdna:72`: covered by the revolver items; its omission of the July 1 reduction is noted in the notes:111 item
- `0001193125-26-336708:mdna:73`: standing list of liquidity uses; prior wording not in input and no new obligation identifiable; its litigation-settlements mention is cited in the legal-expense item
- `0001193125-26-336708:mdna:74`: standing liquidity boilerplate
- `0001193125-26-336708:mdna:78`: page number
- `0001193125-26-336708:mdna:80`: table, amounts only
- `0001193125-26-336708:mdna:82`: table, amounts only
- `0001193125-26-336708:mdna:85`: table, amounts only (cited in the capex item)
- `0001193125-26-336708:mdna:88`: table, amounts only
- `0001193125-26-336708:mdna:89`: date rolled forward; same facts as notes:53 (cited in the debt-table item)
- `0001193125-26-336708:mdna:90`: prior-year comparative facts (cited in the debt-table item)
- `0001193125-26-336708:mdna:91`: covered by the deferred-financing-costs item (notes:113)
- `0001193125-26-336708:mdna:92`: covered by the special-distribution items (mdna:76, notes:158)
- `0001193125-26-336708:mdna:93`: amounts only
- `0001193125-26-336708:mdna:94`: page number
- `0001193125-26-336708:mdna:98`: date rolled forward
- `0001193125-26-336708:mdna:100`: table, amounts only (cited in the transaction-costs item)
- `0001193125-26-336708:mdna:102`: standing footnote (OneCell loss); its amounts are for the numbers reader
- `0001193125-26-336708:mdna:106`: table, amounts only
- `0001193125-26-336708:mdna:108`: page number

**Notes**
- `0001193125-26-336708:notes:7`: date rolled forward
- `0001193125-26-336708:notes:8`: heading
- `0001193125-26-336708:notes:11`: wording only (redemption date and period added)
- `0001193125-26-336708:notes:12`: heading
- `0001193125-26-336708:notes:17`: heading
- `0001193125-26-336708:notes:18`: wording only; not shown as changed in the note history; no new matter named
- `0001193125-26-336708:notes:25`: date rolled forward
- `0001193125-26-336708:notes:28`: date rolled forward
- `0001193125-26-336708:notes:31`: period rolled to six months; what it no longer says is covered by the valuation-allowance item
- `0001193125-26-336708:notes:34`: wording only (parenthetical)
- `0001193125-26-336708:notes:35`: amounts only
- `0001193125-26-336708:notes:38`: table, amounts only (cited in the EPS cross-document item)
- `0001193125-26-336708:notes:40`: heading, date rolled forward
- `0001193125-26-336708:notes:41`: wording only; not shown as changed in the note history; the adoption took effect January 1, 2026
- `0001193125-26-336708:notes:43`: wording only; not shown as changed in the note history
- `0001193125-26-336708:notes:44`: wording only; not shown as changed in the note history
- `0001193125-26-336708:notes:45`: heading
- `0001193125-26-336708:notes:46`: heading
- `0001193125-26-336708:notes:47`: heading
- `0001193125-26-336708:notes:49`: heading
- `0001193125-26-336708:notes:50`: heading
- `0001193125-26-336708:notes:51`: prior wording not in input; reads as the standing description of the CCS closing; amounts only
- `0001193125-26-336708:notes:52`: date rolled forward
- `0001193125-26-336708:notes:53`: date rolled forward
- `0001193125-26-336708:notes:56`: heading
- `0001193125-26-336708:notes:58`: date rolled forward
- `0001193125-26-336708:notes:62`: heading
- `0001193125-26-336708:notes:65`: table introduction, date rolled forward
- `0001193125-26-336708:notes:67`: standing footnote on allocating interest to discontinued operations
- `0001193125-26-336708:notes:68`: table introduction
- `0001193125-26-336708:notes:69`: table, amounts only; tax lines covered by the discontinued-operations tax item
- `0001193125-26-336708:notes:70`: standing footnote
- `0001193125-26-336708:notes:71`: standing footnote
- `0001193125-26-336708:notes:73`: table, amounts only
- `0001193125-26-336708:notes:75`: table, amounts only; its footnote is covered by the OWN/DAS adjustment item
- `0001193125-26-336708:notes:77`: standing footnote
- `0001193125-26-336708:notes:78`: standing table introduction
- `0001193125-26-336708:notes:79`: table, amounts only (cited in the reverse-TSA and MSA items)
- `0001193125-26-336708:notes:81`: table, amounts only
- `0001193125-26-336708:notes:84`: duplicate introduction text under a second tag block
- `0001193125-26-336708:notes:89`: table, amounts only; recast basis covered by the roll-forward item
- `0001193125-26-336708:notes:92`: table, amounts only; recast basis covered by the roll-forward item
- `0001193125-26-336708:notes:93`: date rolled forward; the contract-liability explanation is unchanged; the paragraph is truncated in the input
- `0001193125-26-336708:notes:96`: table, amounts only
- `0001193125-26-336708:notes:98`: table, amounts only; the new special-distribution-payable line is covered by the notes:158 item
- `0001193125-26-336708:notes:100`: table, amounts only
- `0001193125-26-336708:notes:103`: table, amounts only
- `0001193125-26-336708:notes:104`: date rolled forward
- `0001193125-26-336708:notes:106`: table, amounts only
- `0001193125-26-336708:notes:107`: heading (note renumbered)
- `0001193125-26-336708:notes:109`: wording only
- `0001193125-26-336708:notes:118`: table, amounts only
- `0001193125-26-336708:notes:119`: wording only (segment now singular)
- `0001193125-26-336708:notes:121`: wording only (segment now singular)
- `0001193125-26-336708:notes:123`: table introduction
- `0001193125-26-336708:notes:124`: table, amounts only
- `0001193125-26-336708:notes:125`: duplicate of the mdna:9 reallocation item
- `0001193125-26-336708:notes:126`: standing footnote (cited in the buyer-agreements item)
- `0001193125-26-336708:notes:127`: table introduction
- `0001193125-26-336708:notes:128`: table, amounts only
- `0001193125-26-336708:notes:129`: footnote duplicating the reallocation item
- `0001193125-26-336708:notes:130`: table introduction
- `0001193125-26-336708:notes:131`: table, amounts only
- `0001193125-26-336708:notes:132`: duplicate of notes:125
- `0001193125-26-336708:notes:133`: table introduction
- `0001193125-26-336708:notes:134`: table, amounts only
- `0001193125-26-336708:notes:135`: footnote duplicating the reallocation item
- `0001193125-26-336708:notes:136`: amounts only
- `0001193125-26-336708:notes:137`: table, amounts only
- `0001193125-26-336708:notes:138`: table, amounts only
- `0001193125-26-336708:notes:139`: standing footnote
- `0001193125-26-336708:notes:144`: table, amounts only
- `0001193125-26-336708:notes:145`: footnote duplicating the reallocation item
- `0001193125-26-336708:notes:147`: table, amounts only
- `0001193125-26-336708:notes:149`: prior wording not in input; standing description of the prior program; settlement timing cited in the restructuring item
- `0001193125-26-336708:notes:152`: table, amounts only
- `0001193125-26-336708:notes:153`: duplicate of the mdna:38 restructuring item; truncated in the input
- `0001193125-26-336708:notes:154`: heading
- `0001193125-26-336708:notes:155`: heading
- `0001193125-26-336708:notes:156`: moved from the Q1 subsequent-events note; same facts (April 7 declaration, $10.00 per share, April 27 payment)
- `0001193125-26-336708:notes:159`: heading

**8-K, Item 2.02 earnings release**
- `0001193125-26-336705:8k_2_02:1`: exhibit cover text
- `0001193125-26-336705:8k_2_02:2`: exhibit cover text
- `0001193125-26-336705:8k_2_02:3`: exhibit label
- `0001193125-26-336705:8k_2_02:4`: title
- `0001193125-26-336705:8k_2_02:5`: heading
- `0001193125-26-336705:8k_2_02:6`: amounts only
- `0001193125-26-336705:8k_2_02:7`: amounts only (cited in the tax item)
- `0001193125-26-336705:8k_2_02:8`: amounts only
- `0001193125-26-336705:8k_2_02:9`: amounts only
- `0001193125-26-336705:8k_2_02:10`: amounts only
- `0001193125-26-336705:8k_2_02:11`: duplicate of the Core redefinition item
- `0001193125-26-336705:8k_2_02:12`: cross-reference
- `0001193125-26-336705:8k_2_02:13`: standing caveat (cash flows not segregated)
- `0001193125-26-336705:8k_2_02:14`: dateline
- `0001193125-26-336705:8k_2_02:15`: table, amounts only
- `0001193125-26-336705:8k_2_02:18`: duplicate of the RUCKUS closing and recast items
- `0001193125-26-336705:8k_2_02:19`: heading
- `0001193125-26-336705:8k_2_02:20`: amounts only
- `0001193125-26-336705:8k_2_02:21`: amounts only
- `0001193125-26-336705:8k_2_02:22`: amounts only
- `0001193125-26-336705:8k_2_02:23`: heading
- `0001193125-26-336705:8k_2_02:24`: heading
- `0001193125-26-336705:8k_2_02:25`: table, amounts only
- `0001193125-26-336705:8k_2_02:26`: heading
- `0001193125-26-336705:8k_2_02:27`: table, amounts only
- `0001193125-26-336705:8k_2_02:28`: heading
- `0001193125-26-336705:8k_2_02:29`: table, amounts only
- `0001193125-26-336705:8k_2_02:30`: heading
- `0001193125-26-336705:8k_2_02:31`: table, amounts only; its footnotes duplicate the reallocation item
- `0001193125-26-336705:8k_2_02:32`: heading
- `0001193125-26-336705:8k_2_02:34`: amounts only
- `0001193125-26-336705:8k_2_02:35`: amounts only; standing caveat
- `0001193125-26-336705:8k_2_02:36`: amounts only
- `0001193125-26-336705:8k_2_02:37`: amounts only; covered by the availability item
- `0001193125-26-336705:8k_2_02:38`: heading
- `0001193125-26-336705:8k_2_02:39`: call logistics
- `0001193125-26-336705:8k_2_02:40`: call logistics
- `0001193125-26-336705:8k_2_02:41`: call logistics
- `0001193125-26-336705:8k_2_02:42`: standard call caveat
- `0001193125-26-336705:8k_2_02:43`: heading
- `0001193125-26-336705:8k_2_02:44`: company boilerplate
- `0001193125-26-336705:8k_2_02:45`: contact
- `0001193125-26-336705:8k_2_02:46`: contact
- `0001193125-26-336705:8k_2_02:47`: heading
- `0001193125-26-336705:8k_2_02:48`: standard non-GAAP boilerplate
- `0001193125-26-336705:8k_2_02:49`: heading
- `0001193125-26-336705:8k_2_02:50`: duplicate of the Core redefinition item
- `0001193125-26-336705:8k_2_02:51`: heading
- `0001193125-26-336705:8k_2_02:52`: duplicate of the forward-looking risk items (mdna:110)
- `0001193125-26-336705:8k_2_02:53`: continuation of the standard forward-looking list
- `0001193125-26-336705:8k_2_02:54`: standard boilerplate
- `0001193125-26-336705:8k_2_02:55`: end marker
- `0001193125-26-336705:8k_2_02:57`: table, amounts only
- `0001193125-26-336705:8k_2_02:59`: table, amounts only
- `0001193125-26-336705:8k_2_02:60`: table, amounts only
- `0001193125-26-336705:8k_2_02:61`: table, amounts only; footnotes are duplicates
- `0001193125-26-336705:8k_2_02:62`: table, amounts only
- `0001193125-26-336705:8k_2_02:63`: table, amounts only
- `0001193125-26-336705:8k_2_02:64`: table, amounts only
- `0001193125-26-336705:8k_2_02:65`: table, amounts only
- `0001193125-26-336705:8k_2_02:66`: table, amounts only; the outlook figures are cited in the guidepost item

## Observations that are not items

- **Same-day 8-K without a body.** The 8-K index lists 0001193125-26-336699, filed 2026-08-06 (same day as the earnings release), with items 5.02, 8.01 and 9.01. Its body is not in my directory, so a director or officer change cannot be read. The Item 2.01 filings of 2026-07-01 and 2026-07-08 (the RUCKUS closing) also have no body here. The index shows no late-filing notifications.
- **Item 4.** It reports effective disclosure controls and no change in internal control over financial reporting in a quarter where the notes describe three things:
  - transition services received from Amphenol under a reverse TSA
  - RUCKUS reclassified to held for sale
  - a move to one reportable segment

  Item 4 does not mention these transition arrangements. I have no prior Item 4 to compare, so this is not an item.
- **Truncated paragraphs.** Two paragraphs end mid-sentence in my input: notes:93 ("During the three and six months ended June 30, 2026, the Company") and notes:153 ("the resulting charges and cash"). Whatever follows was not available to me.
