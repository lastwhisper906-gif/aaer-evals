<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# EXTR 10-K (0001193125-26-352872) — notes and text reader

Inputs read in full: input_notes.md (notes:1–331), input_mdna.md (mdna:1–142), input_controls.md (auditors_report:1–43, item_9a:1–14), input_8k.md (8-K index, late-filing list, 8k_2_02:1–124), input_notes_history.md (Q2→Q3 FY2026 10-Q note changes, used only to tell what is new), input_prior_predictions.md (none on record).

Directory check: no trend table, prices, returns, short interest, other-company files, prior probabilities or outcome window are present. The input carries no Item 1A diff, Exhibit 21 diff or Exhibit 10. Every notes paragraph is carried as full text; none is marked `[same as prior period ...]`. The prior annual report is not in the input. Newness is therefore established from the Q3 10-Q change history where it covers a paragraph, or from FY2026-dated events stated in the text. Where neither is available, the item says so.

No arithmetic or magnitude comparison was performed. Amounts appear only as the text states them.

## Items

```json
[
  {
    "id": "estimates_and_discretion_capitalized_commission_amortization_period_changed",
    "what_changed": "The annual revenue note now says capitalized commissions are amortized over the average service-contract period of 'approximately four years'. The Q3 FY2026 10-Q text (0001193125-26-197200:note_history:26) said 'approximately three years'. The 10-K text gives no change-in-estimate disclosure, effective date or effect. MD&A (mdna:57) separately says sales commissions rose in FY2026.",
    "account": "Sales and marketing (amortization of capitalized commissions)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Capitalized commission fees are amortized on a straight-line basis over the average period of service contracts of approximately four years",
    "paragraph_id": "0001193125-26-352872:notes:101",
    "explanation": false
  },
  {
    "id": "revenue_recognition_subscription_billing_described_as_fully_upfront",
    "what_changed": "The contract-balances paragraph says renewable SaaS subscription and support arrangements 'are billed fully at the inception of the contract'. The Q2 FY2026 10-Q wording (0001193125-26-029334:note_history:24) also allowed billing 'at periodic intervals (e.g., quarterly or annually)'. That alternative was dropped in Q3 and stays out of the 10-K. The text does not say whether billing practice changed or only the description.",
    "account": "Deferred revenue, less current portion",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Services provided under renewable SaaS subscription and support arrangements of the Company are billed in accordance with agreed-upon contractual terms, which are billed fully at the inception of the contract.",
    "paragraph_id": "0001193125-26-352872:notes:99",
    "explanation": false
  },
  {
    "id": "revenue_recognition_receivables_concentration_new_distributor",
    "what_changed": "The 10%-of-receivables table now lists Scansource, Inc. at June 30, 2026; it was marked below 10% at June 30, 2025. Ericsson, Inc., listed at June 30, 2025, is now marked below 10%. Scansource does not appear in the 10%-of-revenue table (notes:109). The Q3 10-Q table (0001193125-26-197200:note_history:30) listed Westcon Group at March 31, 2026, and Westcon is not in the year-end receivables table. No text explains the change in receivable counterparties.",
    "account": "Accounts receivable, net",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Scansource, Inc.",
    "paragraph_id": "0001193125-26-352872:notes:111",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_receivables_factoring_program",
    "what_changed": "Note 4 describes a nonrecourse Accounts Receivable Purchase Agreement. Up to $25.0 million of sold receivables may be outstanding at any time. Sold balances are removed from receivables, and proceeds are classified in operating cash flows. The note states that about $20.0 million of trade receivables were sold for cash in FY2026. It gives no balance of sold receivables outstanding at June 30, 2026. Neither the MD&A liquidity section (mdna:101) nor the operating cash flow discussion (mdna:120) mentions the factoring.",
    "account": "Accounts receivable, net",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "During fiscal year 2026, the Company sold approximately $20.0 million of trade accounts receivable in exchange for cash.",
    "paragraph_id": "0001193125-26-352872:notes:118",
    "explanation": false
  },
  {
    "id": "earnings_quality_receivables_increase_without_stated_cause",
    "what_changed": "MD&A's FY2026 operating cash flow discussion says increases in net accounts receivable and in prepaid expenses and other assets used cash. Neither MD&A nor the notes give a cause for the receivables increase; the only related text is the factoring disclosure (notes:118). The same paragraph lists a decrease in inventories as a source of cash, also without a cause.",
    "account": "Accounts receivable, net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "This was partially offset by increases in net accounts receivable and prepaid expenses and other assets",
    "paragraph_id": "0001193125-26-352872:mdna:120",
    "explanation": false
  },
  {
    "id": "earnings_quality_other_liabilities_decrease_without_stated_cause",
    "what_changed": "The same MD&A paragraph says decreases in other current and long-term liabilities used cash in FY2026. In the FY2025 paragraph (mdna:121), increases in other accrued liabilities were a source of cash. No text identifies what was paid down. The notes name two items in other accrued liabilities: the restructuring liability (notes:292) and loss-position derivatives (notes:73). The contingencies note discloses no litigation accrual or payment.",
    "account": "Other accrued liabilities",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "decreases in operating lease liabilities and other current and long-term liabilities",
    "paragraph_id": "0001193125-26-352872:mdna:120",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_internal_use_software_amortization_begins",
    "what_changed": "Note 2 says capitalized internal-use software began amortizing in FY2026 (about $1.2 million), with no amortization in FY2025 or FY2024. Capitalization continues: $17.2 million in FY2026 and $10.2 million in FY2025, amortized over three to seven years. MD&A now describes investing outflows as purchases of property and equipment 'and capitalized software development costs' (mdna:124). The long-lived asset policy lists capitalized software development costs as a category (notes:45).",
    "account": "Property and equipment, net / depreciation and amortization expense",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "The Company amortized approximately $1.2 million of software development costs for the fiscal year ended June 30, 2026. There were no software development amortization costs in fiscal years 2025 and 2024.",
    "paragraph_id": "0001193125-26-352872:notes:56",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_cloud_computing_implementation_amortization_begins",
    "what_changed": "Capitalized cloud-computing implementation costs, reported in prepaid expenses and other current assets and in other assets, began amortizing in FY2026 (about $5.2 million) over three to seven years. Capitalization was $30.1 million in FY2026 and $39.6 million in FY2025. MD&A attributes a $5.2 million G&A increase to this amortization (mdna:61), and the release cash flow statement adds a new add-back line for it (8k_2_02:95). The paragraph ends 'There were no software development amortization costs in fiscal years 2025 and 2024', which repeats the internal-use software sentence rather than speaking to cloud computing costs. This coincides with the ERP completion in Item 9A.",
    "account": "General and administrative",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "The Company amortized approximately $5.2 million of cloud computing implementation costs for the fiscal year ended June 30, 2026.",
    "paragraph_id": "0001193125-26-352872:notes:58",
    "explanation": false
  },
  {
    "id": "controls_audit_and_filings_erp_implementation_completed",
    "what_changed": "Item 9A says a new ERP system was fully implemented during FY2026 and that the related control changes 'significantly affected' internal control over financial reporting in fiscal 2026. item_9a:11 adds that ERP-related changes also occurred in Q4. Management and Grant Thornton both conclude ICFR was effective at June 30, 2026. The auditor's single CAM (distributor rebate estimates) tests controls over rebate claims, end-customer pricing and channel inventory in the same year.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "These changes significantly affected our internal control over financial reporting during fiscal 2026.",
    "paragraph_id": "0001193125-26-352872:item_9a:10",
    "explanation": false
  },
  {
    "id": "across_documents_system_transition_costs_continue_after_erp_completion",
    "what_changed": "Item 9A (item_9a:10) says the ERP implementation was completed during FY2026. Yet the August 5, 2026 release reconciliations exclude system transition costs from both Q1 FY2027 guidance (0.5% of operating margin, $0.01 EPS) and FY2027 guidance (0.3%, $0.03 EPS; 8k_2_02:67). The release defines these costs as non-capitalizable costs of a 'multi-phase transition' covering CRM, CPQ, ERP and human capital management (8k_2_02:108). The 10-K text does not describe any remaining system phases.",
    "account": "General and administrative (system transition costs)",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "System transition costs",
    "paragraph_id": "0001193125-26-333840:8k_2_02:62",
    "explanation": false
  },
  {
    "id": "across_documents_litigation_charge_guided_while_contingency_note_silent",
    "what_changed": "The August 5, 2026 release's Q1 FY2027 GAAP-to-non-GAAP reconciliation excludes litigation charges of 3.4%-3.5% of operating margin ($0.08 EPS). That category is defined as 'estimated settlement and related legal expenses' net of insurance proceeds (8k_2_02:109). The 10-K, filed August 14, 2026, reports that the securities class was certified on July 16, 2026 (notes:201). It discloses no accrual, settlement, or estimate or range of reasonably possible loss for any matter, and its subsequent-event disclosures cover only the refinancing. MD&A attributes the FY2026 G&A decrease mainly to lower litigation legal costs (mdna:61) and gives no forward litigation discussion.",
    "account": "General and administrative (litigation); Other accrued liabilities",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "Litigation charges",
    "paragraph_id": "0001193125-26-333840:8k_2_02:62",
    "explanation": false
  },
  {
    "id": "results_against_expectations_litigation_net_benefit_guided_for_fiscal_year",
    "what_changed": "The FY2027 guidance reconciliation shows a 'Litigation benefit, net' line ((0.3)% of operating margin, $(0.03) EPS), while Q1 FY2027 shows a litigation charge (8k_2_02:62). The release definition nets in insurance proceeds received or expected (8k_2_02:109), so the guide implies recoveries later in FY2027. The 10-K indemnification note says the company's ability to recover defense and indemnification costs through insurance 'is uncertain' (notes:204). The 10-K does not mention any insurance receivable.",
    "account": "General and administrative (litigation, net of insurance)",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "Litigation benefit, net",
    "paragraph_id": "0001193125-26-333840:8k_2_02:67",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_securities_class_certified",
    "what_changed": "New post-year-end development in the securities class action (Steamfitters): on July 16, 2026, the court granted plaintiffs' motion for class certification. Earlier, on March 3, 2026, the court had denied the company's motion to dismiss (first reported in Q3, 0001193125-26-197200:note_history:5). Damages are unspecified, and no accrual or loss estimate is disclosed. The release guides a Q1 FY2027 litigation charge (8k_2_02:62).",
    "account": "Other accrued liabilities",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "On July 16, 2026, the Court granted plaintiffs",
    "paragraph_id": "0001193125-26-352872:notes:201",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_derivative_suits_new_motion_to_dismiss",
    "what_changed": "New sentence: on June 2, 2026, the company moved to dismiss the second amended complaint in the two California derivative cases, which plaintiffs had filed on April 28, 2026. The North Carolina case remains stayed pending a final decision on the California motion.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "The Company filed a motion to dismiss the second amended complaint on June 2, 2026.",
    "paragraph_id": "0001193125-26-352872:notes:202",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_mala_appeal_hearing_scheduled",
    "what_changed": "The Mala nullity-appeal paragraph now gives a hearing date of February 9, 2027 (first added in the Q3 10-Q, 0001193125-26-197200:note_history:4). The German infringement action remains stayed until the nullity action is decided, and no accrual is disclosed.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "A hearing on the appeal is scheduled for February 9, 2027.",
    "paragraph_id": "0001193125-26-352872:notes:199",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_refinancing_into_new_revolving_facility",
    "what_changed": "Subsequent event: on July 29, 2026, the company entered a $500.0 million five-year revolving credit agreement with JPMorgan Chase as agent, terminated the Amended Credit Agreement, and repaid all of its outstanding indebtedness. It borrowed $200.0 million at closing to repay that debt and pay fees, leaving $300.0 million available. The 8-K index shows the July 30, 2026 filing (items 1.01, 1.02, 2.03). The June 30, 2026 debt table and repayment schedule (notes:164, notes:173) still show term-loan installments, and the new revolver states no scheduled installments.",
    "account": "Current portion of long-term debt",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "At closing, the Company borrowed $200.0 million under the 2026 Revolving Facility and used the proceeds to repay the outstanding indebtedness under the Amended Credit Agreement and to pay fees and expenses related to the 2026 Revolving Facility.",
    "paragraph_id": "0001193125-26-352872:notes:176",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_new_revolver_financial_covenants",
    "what_changed": "New covenant package under the 2026 Credit Agreement: interest coverage of at least 3.00 to 1.00, and consolidated total net leverage of no more than 3.75 to 1.00, stepping up to 4.25 to 1.00 for a period after a material acquisition. Both are tested from the quarter ending September 30, 2026. The agreement also has an uncommitted accordion of the greater of $175.0 million and 100% of Consolidated EBITDA, plus further amounts (mdna:109). The covenants replace those of the Amended Credit Agreement, which had carried an interest-coverage waiver for three quarters (notes:168).",
    "account": "none",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "Financial covenants under the 2026 Credit Agreement require us to maintain (i) a consolidated interest charge coverage ratio of at least 3.00 to 1.00 at the end of each fiscal quarter, commencing with the fiscal quarter ending September 30, 2026",
    "paragraph_id": "0001193125-26-352872:mdna:111",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_refinancing_improved_rate_structure_claim",
    "what_changed": "The release says the new revolver brings 'improved terms and rate structure'. The 10-K (mdna:110) gives new margins of 1.25%-2.00% over Adjusted Term SOFR or 0.25%-1.00% over the Alternate Base Rate, set by net leverage, plus a 0.20%-0.25% commitment fee on unused commitments. The terminated term loan's stated margins were 2.00%-2.75% over SOFR (mdna:105). The amount drawn at closing is stated separately (notes:176).",
    "account": "Interest expense",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "which provides additional working capital to fuel growth with improved terms and rate structure",
    "paragraph_id": "0001193125-26-333840:8k_2_02:33",
    "explanation": false
  },
  {
    "id": "earnings_quality_debt_refinancing_charge_guided",
    "what_changed": "Both Q1 FY2027 and FY2027 guidance exclude 'Debt refinancing charges' of $0.01 EPS. The release defines these as non-capitalizable costs in other expense from amendments, refinancings or terminations of credit facilities (8k_2_02:110). This implies a refinancing charge in Q1 FY2027 tied to the July 29, 2026 refinancing. The June 30, 2026 balance sheet still carries unamortized term-loan issuance costs (notes:164), and the 10-K does not quantify any extinguishment loss.",
    "account": "Other expense, net",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "Debt refinancing charges",
    "paragraph_id": "0001193125-26-333840:8k_2_02:62",
    "explanation": false
  },
  {
    "id": "articulation_and_the_filed_history_intra_year_revolver_draws_absent_from_annual_text",
    "what_changed": "The 10-K debt note describes only the zero year-end revolver balance. The Q3 FY2026 10-Q (0001193125-26-197200:note_history:16) disclosed a $30.0 million revolver draw in that quarter, repaid in April 2026. The release cash flow statement carries 'Borrowings under revolving facility' and 'Payments on revolving facility' line items for FY2026 (8k_2_02:95). MD&A's financing discussion (mdna:128) lists share repurchases, term-debt repayments and stock-award tax payments, but not revolver draws or repayments, and MD&A's cash-decrease paragraph (mdna:116) refers only to 'payments for borrowings'.",
    "account": "Revolving facility borrowings and payments (financing cash flows)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "As of June 30, 2026, the Company did not have any outstanding balance against its 2023 Revolving Facility.",
    "paragraph_id": "0001193125-26-352872:notes:170",
    "explanation": false
  },
  {
    "id": "across_documents_contractual_obligations_describe_terminated_term_loan",
    "what_changed": "The contractual obligations section still says debt obligations relate to the Amended Credit Agreement, payable in quarterly installments through FY2028. The same MD&A (mdna:108, mdna:112) and Note 7 (notes:176) say that agreement was terminated and fully repaid on July 29, 2026, before the August 14, 2026 filing, and replaced by a five-year revolver.",
    "account": "Long-term debt",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "As of June 30, 2026, we have $165.0 million of debt outstanding which is payable in quarterly installments through our fiscal year 2028.",
    "paragraph_id": "0001193125-26-352872:mdna:135",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_accelerated_share_repurchase",
    "what_changed": "New in FY2026: an accelerated share repurchase agreement entered January 30, 2026 under the 2025 Repurchase Program. The company paid $50.0 million for 3,299,807 shares. Total FY2026 repurchases were 5,377,808 shares for $87.0 million (notes:215), with $113.0 million left under the program. MD&A lists share repurchases among anticipated FY2027 principal uses of cash (mdna:101), and the release reports $25.0 million repurchased in Q4 (8k_2_02:21).",
    "account": "Treasury stock",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Pursuant to the 2026 ASR and during the year ended June 30, 2026, the Company paid $50.0 million for a total of 3,299,807 shares with an average price of $15.15 per share.",
    "paragraph_id": "0001193125-26-352872:notes:214",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_equity_plan_share_reserve_increase",
    "what_changed": "The 2013 Equity Incentive Plan was amended to add 6.8 million shares (Compensation Committee approval September 14, 2025; stockholder approval November 12, 2025). Note 11 says 14.0 million shares are available for grant at June 30, 2026 (notes:220).",
    "account": "Shares reserved for issuance",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "to increase the maximum number of available shares by 6.8 million shares, which was approved by the stockholders of the Company at the annual meeting of stockholders held on November 12, 2025.",
    "paragraph_id": "0001193125-26-352872:notes:209",
    "explanation": false
  },
  {
    "id": "earnings_quality_modified_price_target_executive_awards_now_earned",
    "what_changed": "New statement: both stock-price targets on certain executive officers' MSUs have been met as of June 30, 2026. The targets were modified on February 15, 2024 to $23.00 and $26.00, from the original $41.38 and $46.96 (notes:245). The shares vest on completion of the requisite service period. The incremental cost of the modification is described as not material.",
    "account": "Diluted weighted-average shares",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "As of June 30, 2026, both the modified price targets have been met and shares will vest upon completion of the requisite service period.",
    "paragraph_id": "0001193125-26-352872:notes:246",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_designated_cash_flow_hedges_begin",
    "what_changed": "New: zero-cost collar contracts designated as cash-flow hedges of forecast foreign-currency operating expenses, with $82.5 million notional and maturities under twelve months. Unrealized losses of $1.8 million sit in AOCI and are expected to be reclassified to the statement of operations within twelve months. $0.7 million of realized losses were reclassified in FY2026. No collars were designated at June 30, 2025. The policy text (notes:73), fair value table (notes:141) and fair value note (notes:147) add the hedge-accounting treatment, and ASU 2025-09 on hedge accounting is pending (notes:86).",
    "account": "Operating expenses (reclassified hedge losses) / Accumulated other comprehensive loss",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "As of June 30, 2026, the Company had zero-cost collar contracts that were designated as hedging instruments with a total notional principal amount of $82.5 million and had maturities of less than twelve months.",
    "paragraph_id": "0001193125-26-352872:notes:281",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_income_tax_disclosure_standard_adopted",
    "what_changed": "ASU 2023-09 adopted prospectively for FY2026. The tax note now has a jurisdictional rate reconciliation for FY2026 (notes:300-302) and income taxes paid by jurisdiction (notes:305-307). FY2025 and FY2024 stay in the old format (notes:303-304, notes:308). The Q3 10-Q said there were no recently adopted standards with a material effect (0001193125-26-197200:note_history:10).",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The Company adopted this standard on a prospective basis for the fiscal year 2026 annual consolidated financial statements.",
    "paragraph_id": "0001193125-26-352872:notes:83",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_irish_valuation_allowance_released",
    "what_changed": "New: the valuation allowance against Irish deferred tax assets was released in FY2026 'given the available positive evidence including cumulative earnings'. The FY2026 rate reconciliation shows an Ireland valuation-allowance line (notes:301). Full U.S. federal and state allowances and a Brazil allowance remain. MD&A's tax discussion (mdna:80-82) does not mention the Irish release.",
    "account": "Provision for income taxes / deferred tax assets",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "valuation allowance against its Irish deferred tax assets was released given the available positive evidence including cumulative earnings.",
    "paragraph_id": "0001193125-26-352872:notes:311",
    "explanation": true
  },
  {
    "id": "estimates_and_discretion_us_valuation_allowance_release_anticipated",
    "what_changed": "The release's non-GAAP tax note says 'Once this valuation allowance is released' the GAAP and non-GAAP provisions will align more closely. The 10-K (notes:311) keeps a full U.S. federal and state valuation allowance, citing inconsistent earnings and historical losses, and says it can be reversed if results sufficiently improve. FY2027 GAAP-to-non-GAAP EPS guidance includes a tax adjustment row (8k_2_02:67). Neither document gives timing for a U.S. release.",
    "account": "Provision for income taxes",
    "expected_direction": "down",
    "horizon": "insufficient",
    "quote": "Once this valuation allowance is released, the non-GAAP and the GAAP provision for income taxes will be more closely aligned.",
    "paragraph_id": "0001193125-26-333840:8k_2_02:113",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_tax_legislation_effects_reflected",
    "what_changed": "Note 15 says the One Big Beautiful Bill Act (enacted July 4, 2025) is reflected in the FY2026 financial statements. It names current deductibility of domestic R&D, changes to the interest limitation and international changes, with some provisions effective in FY2027. No amount is stated, and the FY2026 rate reconciliation's line for effects of tax-law changes carries no amount (notes:301).",
    "account": "Deferred tax assets (capitalization of research and development)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Accordingly, the effects of the new legislation are reflected in the consolidated financial statements for the fiscal year ended June 30, 2026.",
    "paragraph_id": "0001193125-26-352872:notes:315",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_irs_examination_open",
    "what_changed": "Note 15 says an IRS examination of the tax year ended June 30, 2023 is open, and that management believes adequate provision has been made. No prior annual text is in the input, so whether the examination is newly disclosed cannot be established from the text.",
    "account": "Unrecognized tax benefits / income taxes payable",
    "expected_direction": "none",
    "horizon": "insufficient",
    "quote": "The Company is currently under examination in the U.S. by the Internal Revenue Service for the tax year ended June 30, 2023.",
    "paragraph_id": "0001193125-26-352872:notes:317",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_noncancelable_inventory_purchase_commitments",
    "what_changed": "The purchase-commitment paragraph now calls the inventory commitments 'non-cancelable'. It says they 'will be received and consumed during fiscal 2027' and adds that the company expects to use them in normal ongoing operations. The Q3 10-Q version (0001193125-26-197200:note_history:1) said only that the company 'had commitments to purchase' inventory. No purchase-commitment loss liability is described. MD&A says the inventory decrease was a source of cash (mdna:120), cites higher memory component costs (mdna:41), and lists inventory purchases as a principal FY2027 use of cash (mdna:101).",
    "account": "Inventories",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "As of June 30, 2026, the Company had non-cancelable commitments to purchase $112.5 million of inventory, which will be received and consumed during fiscal 2027. The Company expects to utilize its non-cancelable purchase commitments in the normal ongoing operations.",
    "paragraph_id": "0001193125-26-352872:notes:192",
    "explanation": false
  },
  {
    "id": "across_documents_supply_secured_beyond_disclosed_commitment_horizon",
    "what_changed": "The CFO says supply is 'secured into Fiscal 2028'. The 10-K's disclosed inventory commitments are to be received and consumed during FY2027 (notes:192), and its other supplier commitments are for services (mdna:138). Neither document says how FY2028 supply is secured, for example by prepayments, supplier agreements or cancellable orders. MD&A notes that increases in prepaid expenses and other assets used cash (mdna:120) without explaining them.",
    "account": "Purchase commitments / prepaid expenses and other assets",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "With our supply secured into Fiscal 2028, we have broad product availability to meet growing demand.",
    "paragraph_id": "0001193125-26-333840:8k_2_02:11",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_memory_component_cost_increase",
    "what_changed": "New cost driver in the product gross profit explanation: the increase was partly offset by higher distribution costs ($8.2 million) and higher purchase price variances ($10.6 million) 'driven by higher memory component costs'. The release says pricing actions offset 'incremental supply chain costs the industry is facing' (8k_2_02:11).",
    "account": "Cost of product revenues",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "an increase in purchase price variances of $10.6 million driven by higher memory component costs",
    "paragraph_id": "0001193125-26-352872:mdna:41",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_pricing_actions_offset_supply_costs",
    "what_changed": "The CFO states that targeted pricing actions are offsetting industry-wide incremental supply chain costs and give confidence in the margin outlook. FY2027 guidance gives GAAP gross margin of 61.6%-62.1% (8k_2_02:65).",
    "account": "Product gross margin",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "The targeted pricing actions we implemented are successfully offsetting the incremental supply chain costs the industry is facing and provide increased confidence and visibility into our margin outlook.",
    "paragraph_id": "0001193125-26-333840:8k_2_02:11",
    "explanation": false
  },
  {
    "id": "across_documents_product_growth_attributed_to_price_not_demand",
    "what_changed": "MD&A attributes the FY2026 product revenue increase to 'average selling price improvements as a result of price increases implemented during fiscal 2026 and changes in product mix'; it cites no unit-volume or demand driver. The release headline credits 'Demand and Supply Chain Management' (8k_2_02:7), and the CEO cites accelerating demand and share gains (8k_2_02:9).",
    "account": "Product revenue",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "driven by average selling price improvements as a result of price increases implemented during fiscal 2026 and changes in product mix",
    "paragraph_id": "0001193125-26-352872:mdna:31",
    "explanation": false
  },
  {
    "id": "results_against_expectations_product_revenue_growth_outlook",
    "what_changed": "CFO guidance: double-digit FY2027 product revenue growth with continued solid gross margin. FY2027 total revenue guidance is $1,380.0-$1,400.0 million and Q1 FY2027 revenue guidance is $334.0-$339.0 million (8k_2_02:60, 8k_2_02:65). Revenue guidance is not split between product and subscription.",
    "account": "Product revenue",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Looking ahead at Fiscal 2027, we continue to expect double-digit product revenue growth and continued solid gross margin driving strong EPS growth.",
    "paragraph_id": "0001193125-26-333840:8k_2_02:11",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_subscription_hosting_costs",
    "what_changed": "The subscription and support gross profit explanation attributes the increase to Extreme Platform ONE adoption, partly offset by $10.0 million of higher subscription hosting costs and $3.9 million of higher personnel costs. Hosting costs are named as a driver alongside Platform ONE adoption.",
    "account": "Cost of subscription and support revenues",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "partially offset by $10.0 million of higher subscription hosting costs and $3.9 million in higher personnel costs",
    "paragraph_id": "0001193125-26-352872:mdna:44",
    "explanation": false
  },
  {
    "id": "earnings_quality_saas_arr_counts_multi_year_term_licenses_without_spreading",
    "what_changed": "The SaaS ARR definition in MD&A and the release (8k_2_02:51-52) includes on-premises term-based licenses, which are 'accounted for differently under U.S. GAAP' (mdna:11). ARR counts the trailing twelve months of license revenue, including multi-year term licenses recognized up front, and is not adjusted to spread that revenue over the contract term because the company calls it immaterial. No prior-period definition is in the input to date when this wording first appeared.",
    "account": "none (SaaS ARR operating metric)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The Company has not adjusted SaaS ARR to allocate revenue from these multi-year term-based license arrangements over their contractual term because they have historically been immaterial to SaaS ARR and doing so would not be expected to materially affect reported SaaS ARR or related growth rates.",
    "paragraph_id": "0001193125-26-352872:mdna:12",
    "explanation": false
  },
  {
    "id": "earnings_quality_saas_arr_includes_embedded_support",
    "what_changed": "ARR includes the annualized support portion of bundled offerings, including Extreme Platform ONE and term licenses, while support from standalone maintenance contracts is excluded (mdna:13). As customers move to Platform ONE bundles, support revenue enters ARR. MD&A attributes ARR growth to Platform ONE adoption (mdna:16).",
    "account": "none (SaaS ARR operating metric)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "For those software solutions that include embedded support as part of a bundled offering, including Extreme Platform ONE and term-based license arrangements, the quarterly revenue recognized in the period with respect to the support portion of the offering is annualized and included in SaaS ARR.",
    "paragraph_id": "0001193125-26-352872:mdna:12",
    "explanation": false
  },
  {
    "id": "revenue_recognition_maintenance_support_revenue_quantified",
    "what_changed": "MD&A quantifies maintenance-contract support revenue excluded from ARR: $235.3 million in FY2026 and $234.2 million in FY2025, given as 49.6% and 53.8% of subscription and support revenue. No prior-period MD&A is in the input to confirm whether this is a first-time disclosure.",
    "account": "Subscription and support revenue (maintenance contracts)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Support revenues from maintenance contracts included in Subscription and support revenues but excluded from SaaS ARR were $235.3 million and $234.2 million",
    "paragraph_id": "0001193125-26-352872:mdna:16",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_limited_visibility_into_end_customer_renewals",
    "what_changed": "MD&A says management tracks maintenance support revenue through GAAP revenue trends, renewal activity and support operations rather than a standalone metric. It gives part of the reason as the distributor and reseller model 'limiting consistent visibility into end-customer usage and renewals'.",
    "account": "Subscription and support revenue (maintenance contracts)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "limiting consistent visibility into end-customer usage and renewals",
    "paragraph_id": "0001193125-26-352872:mdna:13",
    "explanation": false
  },
  {
    "id": "revenue_recognition_platform_one_share_of_subscription_bookings",
    "what_changed": "The release says Extreme Platform ONE, generally available July 2025, reached over 30% of subscription bookings in its first year and doubled quarter over quarter in Q4. Platform ONE bundles embedded support that ARR counts (mdna:12). Bookings are not a GAAP measure, and the 10-K text does not mention them.",
    "account": "Deferred revenue / subscription and support revenue",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Extreme Platform ONE reached over 30% of our subscription bookings in its first year of availability and doubled quarter-over-quarter in the fourth quarter.",
    "paragraph_id": "0001193125-26-333840:8k_2_02:10",
    "explanation": false
  },
  {
    "id": "earnings_quality_new_non_gaap_exclusion_other_non_recurring_costs",
    "what_changed": "The release adds an exclusion category, 'Other non-recurring costs (benefit)': external advisory and professional fees for non-recurring transactions outside the normal course of business. It shows FY2026 amounts, a Q4 benefit, and a dash for FY2025 (8k_2_02:122). The transactions are not identified. 10-K MD&A cites a $3.3 million increase in G&A professional fees (mdna:61) without naming them.",
    "account": "General and administrative (professional fees)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Other non-recurring costs consist of certain external advisory and professional fees incurred for various non-recurring transactions and activities that occur outside of the normal course of business.",
    "paragraph_id": "0001193125-26-333840:8k_2_02:111",
    "explanation": false
  },
  {
    "id": "earnings_quality_information_technology_costs_reallocated_out_of_admin",
    "what_changed": "The G&A explanation cites a $9.5 million decrease in other costs 'primarily related to allocated information technology costs and depreciation'. The R&D (mdna:53) and S&M (mdna:57) explanations each cite increases in information technology costs. No change in cost-allocation method is disclosed.",
    "account": "General and administrative",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "a $9.5 million decrease in other costs primarily related to allocated information technology costs and depreciation",
    "paragraph_id": "0001193125-26-352872:mdna:61",
    "explanation": false
  },
  {
    "id": "across_documents_restructuring_charges_guided_after_all_plans_completed",
    "what_changed": "Note 14 says all restructuring plans from prior years were completed in FY2026 (also notes:290, notes:291), and the 10-K discloses no new plan or post-year-end restructuring. Yet the release reconciliations exclude restructuring and related charges of 1.5% of operating margin ($0.04 EPS) for Q1 FY2027 (8k_2_02:62) and 0.5% ($0.05 EPS) for FY2027 (8k_2_02:67).",
    "account": "Restructuring and related charges",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "During fiscal 2026, the Company completed all of the restructuring plans initiated in prior years",
    "paragraph_id": "0001193125-26-352872:notes:286",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_restructuring_liability_lease_termination_fee",
    "what_changed": "The year-end restructuring liability is now explained as the early-termination fee for a leased facility; a year earlier it was severance and benefits for the 2024 Plans. The FY2026 facilities charge of about $0.7 million comprised a one-time $1.1 million termination fee, partly offset by a gain on reducing the related ROU asset and lease liability (notes:286). Payment timing is not stated.",
    "account": "Other accrued liabilities (restructuring liability)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "As of June 30, 2026 the restructuring liability was $1.1 million related to the early termination fee for a leased facility.",
    "paragraph_id": "0001193125-26-352872:notes:292",
    "explanation": true
  },
  {
    "id": "structure_and_disclosure_changes_sublease_arrangement_ended",
    "what_changed": "New sentence: there were no subleased facilities in FY2026. Sublease income of less than $0.1 million had been included in lease expense in each of FY2025 and FY2024.",
    "account": "Operating lease costs (sublease income)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The Company did not have any subleased facilities during the fiscal year ended June 30, 2026.",
    "paragraph_id": "0001193125-26-352872:notes:189",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_cfo_trading_plan_adopted",
    "what_changed": "New disclosure: on May 22, 2026 the EVP and CFO adopted a Rule 10b5-1 plan to sell up to 43,629 shares through May 31, 2027. This is the only trading arrangement disclosed.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "adopted a Rule 10b5-1 trading arrangement that is intended to satisfy the affirmative defense conditions of Rule 10b5-1(c) for the sale of up to 43,629 shares",
    "paragraph_id": "0001193125-26-352872:notes:331",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_pending_receivables_credit_loss_standard",
    "what_changed": "New pending standard listed: ASU 2025-05, which changes how credit losses are measured on current accounts receivable and contract assets. It is effective for fiscal years beginning after December 15, 2025. The company says it is evaluating the impact and states no effect. It bears on the allowance for credit losses in Note 4.",
    "account": "Allowance for credit losses",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "ASU 2025-05 is effective for fiscal years beginning after December 15, 2025, and interim periods within those annual reporting periods.",
    "paragraph_id": "0001193125-26-352872:notes:88",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_pending_internal_use_software_standard",
    "what_changed": "New pending standard listed: ASU 2025-06, which removes the development-stage model for internal-use software and ties capitalization to management authorization and probable completion. It is effective for fiscal years beginning after December 15, 2027, with early adoption permitted, and the company is evaluating it. It bears on the internal-use software capitalization that began amortizing in FY2026 (notes:56).",
    "account": "Property and equipment, net (capitalized internal-use software)",
    "expected_direction": "none",
    "horizon": "per stated effective date (company evaluating)",
    "quote": "This ASU removes all references to prescriptive and sequential software development stages and requires entities to begin capitalizing software costs when management authorizes and commits to funding the software project",
    "paragraph_id": "0001193125-26-352872:notes:87",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_pending_hedge_accounting_standard",
    "what_changed": "New pending standard listed: ASU 2025-09 on hedge accounting, effective for fiscal years beginning after December 15, 2026 and applied prospectively. The company is evaluating it. It bears on the cash-flow hedges first designated in FY2026 (notes:281).",
    "account": "Accumulated other comprehensive loss (cash-flow hedges)",
    "expected_direction": "none",
    "horizon": "per stated effective date (company evaluating)",
    "quote": "ASU 2025-09 is effective for fiscal years beginning after December 15, 2026, and interim periods within those annual reporting periods, and should be applied on a prospective basis.",
    "paragraph_id": "0001193125-26-352872:notes:86",
    "explanation": false
  },
  {
    "id": "across_documents_stock_rotation_estimate_inputs_differ",
    "what_changed": "The revenue note says stock rotations are estimated from historical return rates and 'estimates provided by the distributors'. MD&A's critical accounting estimate (mdna:90) says they are estimated from an analysis of historical return rates only. The auditor's CAM (auditors_report:13) covers rebates and does not cover stock rotation.",
    "account": "Accounts receivable, net (allowance for product returns)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Stock rotations are variable consideration and are estimated based on historical return rates and estimates provided by the distributors.",
    "paragraph_id": "0001193125-26-352872:notes:95",
    "explanation": false
  }
]
```

## Paragraphs not itemized

### Auditor's report
- 0001193125-26-352872:auditors_report:1 — heading
- 0001193125-26-352872:auditors_report:2 — addressee
- 0001193125-26-352872:auditors_report:3 — addressee
- 0001193125-26-352872:auditors_report:4 — heading
- 0001193125-26-352872:auditors_report:5 — unqualified opinion, standard wording; dates rolled forward
- 0001193125-26-352872:auditors_report:6 — standard cross-reference to ICFR report; date rolled forward
- 0001193125-26-352872:auditors_report:7 — heading
- 0001193125-26-352872:auditors_report:8 — standard basis-for-opinion wording
- 0001193125-26-352872:auditors_report:9 — standard audit-scope wording
- 0001193125-26-352872:auditors_report:10 — heading
- 0001193125-26-352872:auditors_report:11 — standard CAM preamble
- 0001193125-26-352872:auditors_report:12 — CAM title (distributor rebates); no prior report in input to show a change
- 0001193125-26-352872:auditors_report:13 — CAM description restates the Note 3 rebate process (cited in stock rotation item)
- 0001193125-26-352872:auditors_report:14 — standard CAM rationale
- 0001193125-26-352872:auditors_report:15 — lead-in
- 0001193125-26-352872:auditors_report:16 — standard control-testing procedure
- 0001193125-26-352872:auditors_report:17 — procedure sub-bullet
- 0001193125-26-352872:auditors_report:18 — procedure sub-bullet
- 0001193125-26-352872:auditors_report:19 — procedure sub-bullet
- 0001193125-26-352872:auditors_report:20 — procedure sub-bullet
- 0001193125-26-352872:auditors_report:21 — standard procedure
- 0001193125-26-352872:auditors_report:22 — standard retrospective-review procedure
- 0001193125-26-352872:auditors_report:23 — standard channel-inventory confirmation procedure
- 0001193125-26-352872:auditors_report:24 — signature
- 0001193125-26-352872:auditors_report:25 — auditor tenure, standing
- 0001193125-26-352872:auditors_report:26 — location
- 0001193125-26-352872:auditors_report:27 — report date rolled forward
- 0001193125-26-352872:auditors_report:28 — heading
- 0001193125-26-352872:auditors_report:29 — addressee
- 0001193125-26-352872:auditors_report:30 — addressee
- 0001193125-26-352872:auditors_report:31 — heading
- 0001193125-26-352872:auditors_report:32 — ICFR effective, standard wording; date rolled forward
- 0001193125-26-352872:auditors_report:33 — standard cross-reference; date rolled forward
- 0001193125-26-352872:auditors_report:34 — heading
- 0001193125-26-352872:auditors_report:35 — standard
- 0001193125-26-352872:auditors_report:36 — standard
- 0001193125-26-352872:auditors_report:37 — heading
- 0001193125-26-352872:auditors_report:38 — standard ICFR definition
- 0001193125-26-352872:auditors_report:39 — standard limitations language
- 0001193125-26-352872:auditors_report:40 — signature
- 0001193125-26-352872:auditors_report:41 — location
- 0001193125-26-352872:auditors_report:42 — date rolled forward
- 0001193125-26-352872:auditors_report:43 — page header

### Item 9A
- 0001193125-26-352872:item_9a:1 — heading
- 0001193125-26-352872:item_9a:2 — heading
- 0001193125-26-352872:item_9a:3 — standard definition
- 0001193125-26-352872:item_9a:4 — disclosure controls effective; date rolled forward
- 0001193125-26-352872:item_9a:5 — heading
- 0001193125-26-352872:item_9a:6 — standard
- 0001193125-26-352872:item_9a:7 — ICFR effective; date rolled forward
- 0001193125-26-352872:item_9a:8 — standard auditor reference
- 0001193125-26-352872:item_9a:9 — heading
- 0001193125-26-352872:item_9a:11 — same ERP change as item_9a:10 item (Q4 ERP-related changes)
- 0001193125-26-352872:item_9a:12 — heading
- 0001193125-26-352872:item_9a:13 — standard inherent-limitations language
- 0001193125-26-352872:item_9a:14 — page number

### MD&A
- 0001193125-26-352872:mdna:1 — heading
- 0001193125-26-352872:mdna:2 — heading
- 0001193125-26-352872:mdna:3 — standard
- 0001193125-26-352872:mdna:4 — standing language on routine timing decisions
- 0001193125-26-352872:mdna:5 — business description; Platform ONE launch covered by ARR and Platform ONE items
- 0001193125-26-352872:mdna:6 — standing
- 0001193125-26-352872:mdna:7 — heading
- 0001193125-26-352872:mdna:8 — dates rolled forward
- 0001193125-26-352872:mdna:9 — heading
- 0001193125-26-352872:mdna:10 — heading
- 0001193125-26-352872:mdna:11 — same change as mdna:12 ARR term-license item (inclusion rationale)
- 0001193125-26-352872:mdna:14 — standing metric-use caveat
- 0001193125-26-352872:mdna:15 — continuation of caveat
- 0001193125-26-352872:mdna:17 — page number
- 0001193125-26-352872:mdna:18 — heading
- 0001193125-26-352872:mdna:19 — lead-in
- 0001193125-26-352872:mdna:20 — amounts only
- 0001193125-26-352872:mdna:21 — amounts only
- 0001193125-26-352872:mdna:22 — amounts only
- 0001193125-26-352872:mdna:23 — amounts only
- 0001193125-26-352872:mdna:24 — amounts only
- 0001193125-26-352872:mdna:25 — amounts only
- 0001193125-26-352872:mdna:26 — amounts only (operating cash flow and cash balance)
- 0001193125-26-352872:mdna:27 — heading
- 0001193125-26-352872:mdna:28 — lead-in
- 0001193125-26-352872:mdna:29 — table, amounts only
- 0001193125-26-352872:mdna:30 — standing
- 0001193125-26-352872:mdna:32 — prior-year comparison carried
- 0001193125-26-352872:mdna:33 — amounts; driver matches ARR items
- 0001193125-26-352872:mdna:34 — prior-year comparison carried
- 0001193125-26-352872:mdna:35 — standing lead-in
- 0001193125-26-352872:mdna:36 — table, amounts only
- 0001193125-26-352872:mdna:37 — heading
- 0001193125-26-352872:mdna:38 — lead-in
- 0001193125-26-352872:mdna:39 — table, amounts only
- 0001193125-26-352872:mdna:40 — standing cost description; site list has no prior text in input to show a change
- 0001193125-26-352872:mdna:42 — prior-year comparison carried
- 0001193125-26-352872:mdna:43 — standing
- 0001193125-26-352872:mdna:45 — prior-year comparison carried
- 0001193125-26-352872:mdna:46 — heading
- 0001193125-26-352872:mdna:47 — lead-in
- 0001193125-26-352872:mdna:48 — table, amounts only
- 0001193125-26-352872:mdna:49 — lead-in
- 0001193125-26-352872:mdna:50 — table, amounts only
- 0001193125-26-352872:mdna:51 — heading
- 0001193125-26-352872:mdna:52 — standing
- 0001193125-26-352872:mdna:53 — routine expense drivers with amounts (IT cost increase cited in mdna:61 item)
- 0001193125-26-352872:mdna:54 — prior-year comparison carried
- 0001193125-26-352872:mdna:55 — heading
- 0001193125-26-352872:mdna:56 — standing
- 0001193125-26-352872:mdna:57 — routine expense drivers with amounts (commission increase cited in commission-period item)
- 0001193125-26-352872:mdna:58 — prior-year comparison carried
- 0001193125-26-352872:mdna:59 — heading
- 0001193125-26-352872:mdna:60 — standing
- 0001193125-26-352872:mdna:62 — prior-year comparison carried
- 0001193125-26-352872:mdna:63 — heading
- 0001193125-26-352872:mdna:64 — amounts only
- 0001193125-26-352872:mdna:65 — heading
- 0001193125-26-352872:mdna:66 — same change as notes:286 item
- 0001193125-26-352872:mdna:67 — heading
- 0001193125-26-352872:mdna:68 — prior-year comparison carried
- 0001193125-26-352872:mdna:69 — heading
- 0001193125-26-352872:mdna:70 — prior-year comparison carried
- 0001193125-26-352872:mdna:71 — heading
- 0001193125-26-352872:mdna:72 — amounts; standing no-acquisition/no-impairment statement
- 0001193125-26-352872:mdna:73 — heading
- 0001193125-26-352872:mdna:74 — amounts; standing driver
- 0001193125-26-352872:mdna:75 — heading
- 0001193125-26-352872:mdna:76 — amounts; standing driver
- 0001193125-26-352872:mdna:77 — heading
- 0001193125-26-352872:mdna:78 — amounts; standing FX explanation
- 0001193125-26-352872:mdna:79 — heading
- 0001193125-26-352872:mdna:80 — standing ETR factors (omission of Irish release cited in notes:311 item)
- 0001193125-26-352872:mdna:81 — amounts only
- 0001193125-26-352872:mdna:82 — standing
- 0001193125-26-352872:mdna:83 — cross-reference
- 0001193125-26-352872:mdna:84 — heading
- 0001193125-26-352872:mdna:85 — standing
- 0001193125-26-352872:mdna:86 — heading
- 0001193125-26-352872:mdna:87 — standing
- 0001193125-26-352872:mdna:88 — standing
- 0001193125-26-352872:mdna:89 — standing
- 0001193125-26-352872:mdna:90 — standing (input difference cited in notes:95 item)
- 0001193125-26-352872:mdna:91 — standing
- 0001193125-26-352872:mdna:92 — standing
- 0001193125-26-352872:mdna:93 — cross-reference
- 0001193125-26-352872:mdna:94 — heading
- 0001193125-26-352872:mdna:95 — standing
- 0001193125-26-352872:mdna:96 — heading
- 0001193125-26-352872:mdna:97 — cross-reference
- 0001193125-26-352872:mdna:98 — heading
- 0001193125-26-352872:mdna:99 — lead-in
- 0001193125-26-352872:mdna:100 — table, amounts only
- 0001193125-26-352872:mdna:101 — new facility and availability covered by notes:176 and mdna:111 items
- 0001193125-26-352872:mdna:102 — standing program description
- 0001193125-26-352872:mdna:103 — amounts only (ASR covered by notes:214 item)
- 0001193125-26-352872:mdna:104 — standing description of terminated agreement
- 0001193125-26-352872:mdna:105 — standing (old margins cited in rate-structure item)
- 0001193125-26-352872:mdna:106 — standing
- 0001193125-26-352872:mdna:107 — standing
- 0001193125-26-352872:mdna:108 — compliance date rolled forward; termination covered by notes:176 item
- 0001193125-26-352872:mdna:109 — duplicate of notes:175; covered by notes:176 item
- 0001193125-26-352872:mdna:110 — new pricing terms covered by 8k_2_02:33 rate-structure item
- 0001193125-26-352872:mdna:112 — duplicate of notes:176
- 0001193125-26-352872:mdna:113 — heading
- 0001193125-26-352872:mdna:114 — lead-in
- 0001193125-26-352872:mdna:115 — table, amounts only
- 0001193125-26-352872:mdna:116 — amounts; standing explanation (cited in revolver item)
- 0001193125-26-352872:mdna:117 — continuation
- 0001193125-26-352872:mdna:118 — prior-year comparison carried
- 0001193125-26-352872:mdna:119 — heading
- 0001193125-26-352872:mdna:121 — prior-year comparison carried
- 0001193125-26-352872:mdna:122 — prior-year comparison carried
- 0001193125-26-352872:mdna:123 — heading
- 0001193125-26-352872:mdna:124 — amounts; capitalized software covered by notes:56 item
- 0001193125-26-352872:mdna:125 — prior-year comparison carried
- 0001193125-26-352872:mdna:126 — prior-year comparison carried
- 0001193125-26-352872:mdna:127 — heading
- 0001193125-26-352872:mdna:128 — amounts; missing revolver activity covered by notes:170 item
- 0001193125-26-352872:mdna:129 — prior-year comparison carried
- 0001193125-26-352872:mdna:130 — prior-year comparison carried
- 0001193125-26-352872:mdna:131 — heading
- 0001193125-26-352872:mdna:132 — standing FX explanation
- 0001193125-26-352872:mdna:133 — heading
- 0001193125-26-352872:mdna:134 — standing
- 0001193125-26-352872:mdna:136 — duplicate of notes:192
- 0001193125-26-352872:mdna:137 — amounts only
- 0001193125-26-352872:mdna:138 — amounts only (cited in supply item)
- 0001193125-26-352872:mdna:139 — standing
- 0001193125-26-352872:mdna:140 — standing
- 0001193125-26-352872:mdna:141 — heading
- 0001193125-26-352872:mdna:142 — standing

### Notes
- 0001193125-26-352872:notes:1 — standing incorporation by reference
- 0001193125-26-352872:notes:2 — heading
- 0001193125-26-352872:notes:3 — heading
- 0001193125-26-352872:notes:4 — standing cybersecurity program language
- 0001193125-26-352872:notes:5 — standing
- 0001193125-26-352872:notes:6 — standing
- 0001193125-26-352872:notes:7 — lead-in
- 0001193125-26-352872:notes:8 — standing program element
- 0001193125-26-352872:notes:9 — standing program element
- 0001193125-26-352872:notes:10 — standing program element
- 0001193125-26-352872:notes:11 — standing program element
- 0001193125-26-352872:notes:12 — standing program element
- 0001193125-26-352872:notes:13 — standing program element
- 0001193125-26-352872:notes:14 — standing risk statement
- 0001193125-26-352872:notes:15 — heading
- 0001193125-26-352872:notes:16 — standing governance
- 0001193125-26-352872:notes:17 — governance reporting lines; no prior text in input to establish a change (insufficient)
- 0001193125-26-352872:notes:18 — officer experience description; no prior text in input to establish a change (insufficient)
- 0001193125-26-352872:notes:19 — standing
- 0001193125-26-352872:notes:20 — heading
- 0001193125-26-352872:notes:21 — duplicate of auditors_report:5
- 0001193125-26-352872:notes:22 — duplicate of auditors_report:6
- 0001193125-26-352872:notes:23 — heading
- 0001193125-26-352872:notes:24 — standing business description
- 0001193125-26-352872:notes:25 — heading
- 0001193125-26-352872:notes:26 — dates rolled forward
- 0001193125-26-352872:notes:27 — heading
- 0001193125-26-352872:notes:28 — standing
- 0001193125-26-352872:notes:29 — standing
- 0001193125-26-352872:notes:30 — heading
- 0001193125-26-352872:notes:31 — standing
- 0001193125-26-352872:notes:32 — heading
- 0001193125-26-352872:notes:33 — heading
- 0001193125-26-352872:notes:34 — standing revenue policy
- 0001193125-26-352872:notes:35 — cross-reference
- 0001193125-26-352872:notes:36 — heading
- 0001193125-26-352872:notes:37 — standing
- 0001193125-26-352872:notes:38 — heading
- 0001193125-26-352872:notes:39 — standing returns-allowance policy
- 0001193125-26-352872:notes:40 — heading
- 0001193125-26-352872:notes:41 — standing credit-loss policy
- 0001193125-26-352872:notes:42 — heading
- 0001193125-26-352872:notes:43 — standing inventory policy
- 0001193125-26-352872:notes:44 — heading
- 0001193125-26-352872:notes:45 — lists capitalized software development costs; same change as notes:56 item
- 0001193125-26-352872:notes:46 — heading
- 0001193125-26-352872:notes:47 — standing
- 0001193125-26-352872:notes:48 — heading
- 0001193125-26-352872:notes:49 — standing
- 0001193125-26-352872:notes:50 — standing
- 0001193125-26-352872:notes:51 — cross-reference
- 0001193125-26-352872:notes:52 — heading
- 0001193125-26-352872:notes:53 — heading
- 0001193125-26-352872:notes:54 — standing
- 0001193125-26-352872:notes:55 — heading
- 0001193125-26-352872:notes:57 — heading
- 0001193125-26-352872:notes:59 — heading
- 0001193125-26-352872:notes:60 — standing
- 0001193125-26-352872:notes:61 — standing
- 0001193125-26-352872:notes:62 — standing goodwill policy; no impairment
- 0001193125-26-352872:notes:63 — heading
- 0001193125-26-352872:notes:64 — standing boilerplate
- 0001193125-26-352872:notes:65 — standing boilerplate
- 0001193125-26-352872:notes:66 — heading
- 0001193125-26-352872:notes:67 — standing
- 0001193125-26-352872:notes:68 — heading
- 0001193125-26-352872:notes:69 — standing warranty policy
- 0001193125-26-352872:notes:70 — standing indemnification policy
- 0001193125-26-352872:notes:71 — heading
- 0001193125-26-352872:notes:72 — standing
- 0001193125-26-352872:notes:73 — hedge-accounting policy text; same change as notes:281 item
- 0001193125-26-352872:notes:74 — heading
- 0001193125-26-352872:notes:75 — standing
- 0001193125-26-352872:notes:76 — standing
- 0001193125-26-352872:notes:77 — heading
- 0001193125-26-352872:notes:78 — standing
- 0001193125-26-352872:notes:79 — heading
- 0001193125-26-352872:notes:80 — standing
- 0001193125-26-352872:notes:81 — standing
- 0001193125-26-352872:notes:82 — heading
- 0001193125-26-352872:notes:84 — heading
- 0001193125-26-352872:notes:85 — pending disclosure-only standard (ASU 2025-11); company evaluating; no stated effect
- 0001193125-26-352872:notes:89 — pending disclosure-only standard (ASU 2024-03/2025-01); company evaluating; no stated effect
- 0001193125-26-352872:notes:90 — continuation of notes:89
- 0001193125-26-352872:notes:91 — heading
- 0001193125-26-352872:notes:92 — standing
- 0001193125-26-352872:notes:93 — standing
- 0001193125-26-352872:notes:94 — standing
- 0001193125-26-352872:notes:96 — standing
- 0001193125-26-352872:notes:97 — standing
- 0001193125-26-352872:notes:98 — RPO amount and fiscal-year buckets rolled forward
- 0001193125-26-352872:notes:100 — amounts only
- 0001193125-26-352872:notes:102 — standing
- 0001193125-26-352872:notes:103 — lead-in
- 0001193125-26-352872:notes:104 — table, amounts only
- 0001193125-26-352872:notes:105 — amounts only (country concentration)
- 0001193125-26-352872:notes:106 — heading
- 0001193125-26-352872:notes:107 — standing
- 0001193125-26-352872:notes:108 — lead-in
- 0001193125-26-352872:notes:109 — table, amounts only
- 0001193125-26-352872:notes:110 — lead-in
- 0001193125-26-352872:notes:112 — heading
- 0001193125-26-352872:notes:113 — lead-in
- 0001193125-26-352872:notes:114 — table, amounts only
- 0001193125-26-352872:notes:115 — heading
- 0001193125-26-352872:notes:116 — lead-in
- 0001193125-26-352872:notes:117 — table, amounts only
- 0001193125-26-352872:notes:119 — lead-in
- 0001193125-26-352872:notes:120 — table, amounts only
- 0001193125-26-352872:notes:121 — footnote
- 0001193125-26-352872:notes:122 — lead-in
- 0001193125-26-352872:notes:123 — table, amounts only
- 0001193125-26-352872:notes:124 — lead-in
- 0001193125-26-352872:notes:125 — table, amounts only
- 0001193125-26-352872:notes:126 — heading
- 0001193125-26-352872:notes:127 — lead-in
- 0001193125-26-352872:notes:128 — table, amounts only
- 0001193125-26-352872:notes:129 — amounts only
- 0001193125-26-352872:notes:130 — lead-in
- 0001193125-26-352872:notes:131 — table, amounts only
- 0001193125-26-352872:notes:132 — heading
- 0001193125-26-352872:notes:133 — lead-in
- 0001193125-26-352872:notes:134 — table, amounts only
- 0001193125-26-352872:notes:135 — heading
- 0001193125-26-352872:notes:136 — standing
- 0001193125-26-352872:notes:137 — standing
- 0001193125-26-352872:notes:138 — standing
- 0001193125-26-352872:notes:139 — standing
- 0001193125-26-352872:notes:140 — lead-in
- 0001193125-26-352872:notes:141 — table; designated-hedge row covered by notes:281 item
- 0001193125-26-352872:notes:142 — table, amounts only
- 0001193125-26-352872:notes:143 — standing
- 0001193125-26-352872:notes:144 — standing; collar valuation covered by notes:281 item
- 0001193125-26-352872:notes:145 — amounts only
- 0001193125-26-352872:notes:146 — amounts only
- 0001193125-26-352872:notes:147 — same change as notes:281 item
- 0001193125-26-352872:notes:148 — amounts only
- 0001193125-26-352872:notes:149 — standing
- 0001193125-26-352872:notes:150 — standing
- 0001193125-26-352872:notes:151 — heading
- 0001193125-26-352872:notes:152 — lead-in
- 0001193125-26-352872:notes:153 — table, amounts only
- 0001193125-26-352872:notes:154 — lead-in
- 0001193125-26-352872:notes:155 — table, amounts only
- 0001193125-26-352872:notes:156 — table, amounts only
- 0001193125-26-352872:notes:157 — lead-in
- 0001193125-26-352872:notes:158 — table, amounts only
- 0001193125-26-352872:notes:159 — standing
- 0001193125-26-352872:notes:160 — lead-in
- 0001193125-26-352872:notes:161 — table, amounts only
- 0001193125-26-352872:notes:162 — heading
- 0001193125-26-352872:notes:163 — lead-in
- 0001193125-26-352872:notes:164 — table, amounts only
- 0001193125-26-352872:notes:165 — standing description of 2023 Credit Agreement
- 0001193125-26-352872:notes:166 — standing
- 0001193125-26-352872:notes:167 — standing
- 0001193125-26-352872:notes:168 — compliance date rolled forward
- 0001193125-26-352872:notes:169 — amounts only
- 0001193125-26-352872:notes:171 — amounts only
- 0001193125-26-352872:notes:172 — lead-in
- 0001193125-26-352872:notes:173 — table, amounts only
- 0001193125-26-352872:notes:174 — heading
- 0001193125-26-352872:notes:175 — same change as notes:176 item
- 0001193125-26-352872:notes:177 — heading
- 0001193125-26-352872:notes:178 — heading
- 0001193125-26-352872:notes:179 — standing
- 0001193125-26-352872:notes:180 — standing
- 0001193125-26-352872:notes:181 — standing
- 0001193125-26-352872:notes:182 — lead-in
- 0001193125-26-352872:notes:183 — table, amounts only
- 0001193125-26-352872:notes:184 — table, amounts only
- 0001193125-26-352872:notes:185 — standing
- 0001193125-26-352872:notes:186 — lead-in
- 0001193125-26-352872:notes:187 — table, amounts only
- 0001193125-26-352872:notes:188 — heading
- 0001193125-26-352872:notes:190 — heading
- 0001193125-26-352872:notes:191 — heading
- 0001193125-26-352872:notes:193 — heading
- 0001193125-26-352872:notes:194 — standing
- 0001193125-26-352872:notes:195 — standing
- 0001193125-26-352872:notes:196 — caption
- 0001193125-26-352872:notes:197 — standing Mala history
- 0001193125-26-352872:notes:198 — standing Mala history
- 0001193125-26-352872:notes:200 — caption
- 0001193125-26-352872:notes:203 — heading
- 0001193125-26-352872:notes:204 — standing indemnification language (cited in litigation net benefit item)
- 0001193125-26-352872:notes:205 — heading
- 0001193125-26-352872:notes:206 — heading
- 0001193125-26-352872:notes:207 — standing
- 0001193125-26-352872:notes:208 — heading
- 0001193125-26-352872:notes:210 — heading
- 0001193125-26-352872:notes:211 — standing (2021 amendment)
- 0001193125-26-352872:notes:212 — heading
- 0001193125-26-352872:notes:213 — standing program description
- 0001193125-26-352872:notes:215 — amounts only (ASR covered by notes:214 item)
- 0001193125-26-352872:notes:216 — standing
- 0001193125-26-352872:notes:217 — heading
- 0001193125-26-352872:notes:218 — lead-in
- 0001193125-26-352872:notes:219 — heading
- 0001193125-26-352872:notes:220 — same change as notes:209 item; otherwise standing plan description
- 0001193125-26-352872:notes:221 — heading
- 0001193125-26-352872:notes:222 — lead-in
- 0001193125-26-352872:notes:223 — table, amounts only
- 0001193125-26-352872:notes:224 — heading
- 0001193125-26-352872:notes:225 — lead-in
- 0001193125-26-352872:notes:226 — table, amounts only
- 0001193125-26-352872:notes:227 — amounts only
- 0001193125-26-352872:notes:228 — standing
- 0001193125-26-352872:notes:229 — heading
- 0001193125-26-352872:notes:230 — standing
- 0001193125-26-352872:notes:231 — lead-in
- 0001193125-26-352872:notes:232 — table, amounts only
- 0001193125-26-352872:notes:233 — standing
- 0001193125-26-352872:notes:234 — amounts only
- 0001193125-26-352872:notes:235 — amounts only
- 0001193125-26-352872:notes:236 — amounts only
- 0001193125-26-352872:notes:237 — amounts only
- 0001193125-26-352872:notes:238 — heading
- 0001193125-26-352872:notes:239 — amounts only
- 0001193125-26-352872:notes:240 — heading
- 0001193125-26-352872:notes:241 — amounts only
- 0001193125-26-352872:notes:242 — standing
- 0001193125-26-352872:notes:243 — table, standing
- 0001193125-26-352872:notes:244 — standing
- 0001193125-26-352872:notes:245 — standing (original targets cited in notes:246 item)
- 0001193125-26-352872:notes:247 — amounts only
- 0001193125-26-352872:notes:248 — table, amounts only
- 0001193125-26-352872:notes:249 — standing
- 0001193125-26-352872:notes:250 — lead-in
- 0001193125-26-352872:notes:251 — table, amounts only
- 0001193125-26-352872:notes:252 — heading
- 0001193125-26-352872:notes:253 — standing
- 0001193125-26-352872:notes:254 — amounts only
- 0001193125-26-352872:notes:255 — heading
- 0001193125-26-352872:notes:256 — lead-in
- 0001193125-26-352872:notes:257 — table, amounts only
- 0001193125-26-352872:notes:258 — standing
- 0001193125-26-352872:notes:259 — standing
- 0001193125-26-352872:notes:260 — standing
- 0001193125-26-352872:notes:261 — amounts only
- 0001193125-26-352872:notes:262 — table, amounts only
- 0001193125-26-352872:notes:263 — heading
- 0001193125-26-352872:notes:264 — contribution limits rolled forward
- 0001193125-26-352872:notes:265 — amounts only
- 0001193125-26-352872:notes:266 — heading
- 0001193125-26-352872:notes:267 — standing
- 0001193125-26-352872:notes:268 — heading
- 0001193125-26-352872:notes:269 — standing
- 0001193125-26-352872:notes:270 — standing
- 0001193125-26-352872:notes:271 — heading
- 0001193125-26-352872:notes:272 — amounts only
- 0001193125-26-352872:notes:273 — lead-in
- 0001193125-26-352872:notes:274 — table, amounts only
- 0001193125-26-352872:notes:275 — heading
- 0001193125-26-352872:notes:276 — heading
- 0001193125-26-352872:notes:277 — standing; collar use covered by notes:281 item
- 0001193125-26-352872:notes:278 — amounts only
- 0001193125-26-352872:notes:279 — heading
- 0001193125-26-352872:notes:280 — same change as notes:281 item
- 0001193125-26-352872:notes:282 — heading
- 0001193125-26-352872:notes:283 — amounts only
- 0001193125-26-352872:notes:284 — heading
- 0001193125-26-352872:notes:285 — amounts only
- 0001193125-26-352872:notes:287 — amounts only for completed plan
- 0001193125-26-352872:notes:288 — amounts only for completed plan
- 0001193125-26-352872:notes:289 — standing (plan completed in FY2024)
- 0001193125-26-352872:notes:290 — same change as notes:286 item (plans completed)
- 0001193125-26-352872:notes:291 — amounts; completion covered by notes:286 item
- 0001193125-26-352872:notes:293 — lead-in
- 0001193125-26-352872:notes:294 — table, amounts only
- 0001193125-26-352872:notes:295 — heading
- 0001193125-26-352872:notes:296 — lead-in
- 0001193125-26-352872:notes:297 — table, amounts only
- 0001193125-26-352872:notes:298 — lead-in
- 0001193125-26-352872:notes:299 — table, amounts only
- 0001193125-26-352872:notes:300 — same change as notes:83 item
- 0001193125-26-352872:notes:301 — table; Ireland line cited in notes:311 item
- 0001193125-26-352872:notes:302 — footnote
- 0001193125-26-352872:notes:303 — lead-in
- 0001193125-26-352872:notes:304 — table, amounts only
- 0001193125-26-352872:notes:305 — lead-in; new taxes-paid disclosure covered by notes:83 item
- 0001193125-26-352872:notes:306 — table, amounts only
- 0001193125-26-352872:notes:307 — footnote
- 0001193125-26-352872:notes:308 — amounts only
- 0001193125-26-352872:notes:309 — lead-in
- 0001193125-26-352872:notes:310 — table, amounts only
- 0001193125-26-352872:notes:312 — amounts and expiry dates
- 0001193125-26-352872:notes:313 — standing
- 0001193125-26-352872:notes:314 — amounts only
- 0001193125-26-352872:notes:316 — standing
- 0001193125-26-352872:notes:318 — standing
- 0001193125-26-352872:notes:319 — amounts only
- 0001193125-26-352872:notes:320 — lead-in
- 0001193125-26-352872:notes:321 — table, amounts only
- 0001193125-26-352872:notes:322 — standing
- 0001193125-26-352872:notes:323 — heading
- 0001193125-26-352872:notes:324 — standing
- 0001193125-26-352872:notes:325 — lead-in
- 0001193125-26-352872:notes:326 — table, amounts only
- 0001193125-26-352872:notes:327 — standing
- 0001193125-26-352872:notes:328 — lead-in
- 0001193125-26-352872:notes:329 — table, amounts only
- 0001193125-26-352872:notes:330 — heading

### 8-K item 2.02 (0001193125-26-333840)
- 0001193125-26-333840:8k_2_02:1 — exhibit header
- 0001193125-26-333840:8k_2_02:2 — exhibit header
- 0001193125-26-333840:8k_2_02:3 — exhibit header
- 0001193125-26-333840:8k_2_02:4 — contacts
- 0001193125-26-333840:8k_2_02:5 — title
- 0001193125-26-333840:8k_2_02:6 — headline amounts
- 0001193125-26-333840:8k_2_02:7 — covered by mdna:31 product-growth attribution item
- 0001193125-26-333840:8k_2_02:8 — dateline
- 0001193125-26-333840:8k_2_02:9 — promotional CEO narrative; KPI without prior counterpart in input (cited in mdna:31 item)
- 0001193125-26-333840:8k_2_02:12 — heading
- 0001193125-26-333840:8k_2_02:13 — amounts only
- 0001193125-26-333840:8k_2_02:14 — amounts only
- 0001193125-26-333840:8k_2_02:15 — amounts only
- 0001193125-26-333840:8k_2_02:16 — amounts only
- 0001193125-26-333840:8k_2_02:17 — amounts only
- 0001193125-26-333840:8k_2_02:18 — amounts only
- 0001193125-26-333840:8k_2_02:19 — amounts only
- 0001193125-26-333840:8k_2_02:20 — amounts only
- 0001193125-26-333840:8k_2_02:21 — amounts only (Q4 repurchases; cited in ASR item)
- 0001193125-26-333840:8k_2_02:22 — heading
- 0001193125-26-333840:8k_2_02:23 — amounts only
- 0001193125-26-333840:8k_2_02:24 — amounts only
- 0001193125-26-333840:8k_2_02:25 — amounts only
- 0001193125-26-333840:8k_2_02:26 — amounts only
- 0001193125-26-333840:8k_2_02:27 — amounts only
- 0001193125-26-333840:8k_2_02:28 — amounts only
- 0001193125-26-333840:8k_2_02:29 — amounts only
- 0001193125-26-333840:8k_2_02:30 — heading
- 0001193125-26-333840:8k_2_02:31 — amounts only
- 0001193125-26-333840:8k_2_02:32 — amounts only
- 0001193125-26-333840:8k_2_02:34 — heading
- 0001193125-26-333840:8k_2_02:35 — promotional product highlight
- 0001193125-26-333840:8k_2_02:36 — promotional product highlight
- 0001193125-26-333840:8k_2_02:37 — promotional customer highlight
- 0001193125-26-333840:8k_2_02:38 — promotional customer highlight
- 0001193125-26-333840:8k_2_02:39 — promotional customer highlight
- 0001193125-26-333840:8k_2_02:40 — continuation of customer highlight
- 0001193125-26-333840:8k_2_02:41 — promotional customer highlight
- 0001193125-26-333840:8k_2_02:42 — promotional customer highlight
- 0001193125-26-333840:8k_2_02:43 — promotional customer highlight
- 0001193125-26-333840:8k_2_02:44 — heading
- 0001193125-26-333840:8k_2_02:45 — heading
- 0001193125-26-333840:8k_2_02:46 — table, amounts only
- 0001193125-26-333840:8k_2_02:47 — table, amounts only
- 0001193125-26-333840:8k_2_02:48 — standing free cash flow definition
- 0001193125-26-333840:8k_2_02:49 — continuation
- 0001193125-26-333840:8k_2_02:50 — table, amounts only
- 0001193125-26-333840:8k_2_02:51 — duplicate of mdna:11 (covered by ARR items)
- 0001193125-26-333840:8k_2_02:52 — duplicate of mdna:12 (covered by ARR items)
- 0001193125-26-333840:8k_2_02:53 — duplicate of mdna:13 (covered by limited-visibility item)
- 0001193125-26-333840:8k_2_02:54 — duplicate of mdna:14–15
- 0001193125-26-333840:8k_2_02:55 — standing definition
- 0001193125-26-333840:8k_2_02:56 — standing definition
- 0001193125-26-333840:8k_2_02:57 — table, amounts only
- 0001193125-26-333840:8k_2_02:58 — heading
- 0001193125-26-333840:8k_2_02:59 — lead-in
- 0001193125-26-333840:8k_2_02:60 — guidance amounts (adjustment rows itemized at 8k_2_02:62)
- 0001193125-26-333840:8k_2_02:61 — lead-in
- 0001193125-26-333840:8k_2_02:63 — rounding note
- 0001193125-26-333840:8k_2_02:64 — lead-in
- 0001193125-26-333840:8k_2_02:65 — guidance amounts (cited in product-growth and pricing items)
- 0001193125-26-333840:8k_2_02:66 — lead-in
- 0001193125-26-333840:8k_2_02:68 — rounding note
- 0001193125-26-333840:8k_2_02:69 — heading
- 0001193125-26-333840:8k_2_02:70 — conference call logistics
- 0001193125-26-333840:8k_2_02:71 — heading
- 0001193125-26-333840:8k_2_02:72 — standing
- 0001193125-26-333840:8k_2_02:73 — standing
- 0001193125-26-333840:8k_2_02:74 — heading
- 0001193125-26-333840:8k_2_02:75 — standing list of exclusions (new category itemized at 8k_2_02:111)
- 0001193125-26-333840:8k_2_02:76 — standing
- 0001193125-26-333840:8k_2_02:77 — heading
- 0001193125-26-333840:8k_2_02:78 — standing
- 0001193125-26-333840:8k_2_02:79 — standing
- 0001193125-26-333840:8k_2_02:80 — separator
- 0001193125-26-333840:8k_2_02:81 — header
- 0001193125-26-333840:8k_2_02:82 — header
- 0001193125-26-333840:8k_2_02:83 — header
- 0001193125-26-333840:8k_2_02:84 — header
- 0001193125-26-333840:8k_2_02:85 — table, amounts only
- 0001193125-26-333840:8k_2_02:86 — header
- 0001193125-26-333840:8k_2_02:87 — header
- 0001193125-26-333840:8k_2_02:88 — header
- 0001193125-26-333840:8k_2_02:89 — header
- 0001193125-26-333840:8k_2_02:90 — table, amounts only
- 0001193125-26-333840:8k_2_02:91 — header
- 0001193125-26-333840:8k_2_02:92 — header
- 0001193125-26-333840:8k_2_02:93 — header
- 0001193125-26-333840:8k_2_02:94 — header
- 0001193125-26-333840:8k_2_02:95 — table (revolver and cloud-amortization lines cited in notes:170 and notes:58 items)
- 0001193125-26-333840:8k_2_02:96 — header
- 0001193125-26-333840:8k_2_02:97 — header
- 0001193125-26-333840:8k_2_02:98 — standing
- 0001193125-26-333840:8k_2_02:99 — standing
- 0001193125-26-333840:8k_2_02:100 — standing
- 0001193125-26-333840:8k_2_02:101 — standing
- 0001193125-26-333840:8k_2_02:102 — standing
- 0001193125-26-333840:8k_2_02:103 — lead-in
- 0001193125-26-333840:8k_2_02:104 — standing definition
- 0001193125-26-333840:8k_2_02:105 — standing definition
- 0001193125-26-333840:8k_2_02:106 — continuation
- 0001193125-26-333840:8k_2_02:107 — standing definition
- 0001193125-26-333840:8k_2_02:108 — standing definition (cited in system-transition item)
- 0001193125-26-333840:8k_2_02:109 — standing definition (cited in litigation items)
- 0001193125-26-333840:8k_2_02:110 — standing definition (cited in debt-refinancing item)
- 0001193125-26-333840:8k_2_02:112 — standing non-GAAP tax method
- 0001193125-26-333840:8k_2_02:114 — standing cash-tax outlook
- 0001193125-26-333840:8k_2_02:115 — header
- 0001193125-26-333840:8k_2_02:116 — header
- 0001193125-26-333840:8k_2_02:117 — header
- 0001193125-26-333840:8k_2_02:118 — header
- 0001193125-26-333840:8k_2_02:119 — header
- 0001193125-26-333840:8k_2_02:120 — table, amounts only
- 0001193125-26-333840:8k_2_02:121 — table, amounts only
- 0001193125-26-333840:8k_2_02:122 — table, amounts only (new category cited in 8k_2_02:111 item)
- 0001193125-26-333840:8k_2_02:123 — table, amounts only
- 0001193125-26-333840:8k_2_02:124 — table, amounts only

### Material without paragraph ids
- 8-K item-code index: read. The 2026-07-30 filing (items 1.01, 1.02, 2.03) matches the refinancing item. The 2026-01-07 filing (item 5.02) has no body in the input (insufficient).
- Late-filing notifications: none on or before 2026-08-17.
- Note change history (note_history:1–38): used only as the reference for what is new. It is not reported as a separate list.
- Prior predictions: none on record.
