# TTMI — notes-text reader — 10-Q 0001193125-26-335107 (quarter ended June 29, 2026)

## Scope

- Read in full: `input_notes.md`, `input_notes_history.md`, `input_mdna.md`, `input_controls.md`, `input_8k.md`, `input_prior_predictions.md`.
- Missing from the directory: an auditor's report (a 10-Q normally has none), an Item 1A diff, an Exhibit 21 diff and any Exhibit 10. `input_8k.md` has item codes only and no 8-K bodies. Its header says no 8-K is on record at or before 2026-08-05, but the list underneath has dated entries, so I treated the list as the record.
- Nothing forbidden is in the directory: no trend table, prices, returns, short interest, other-company files, prior probabilities or outcome window.
- Prior predictions: none on record, so there is nothing to carry forward.
- I did no arithmetic. Every direction below is what the prose implies. Amounts are repeated as the filing states them, and none of them is compared with another.

## Items

```json
{ "id": "liquidity_and_capital_credit_agreement_amends_term_loan_and_adds_rcf",
  "what_changed": "New subsection. On June 1, 2026 the Company entered the 2026 Credit Agreement. It amended and restated the Prior Term Loan Facility, provided a new RCF, and permits one or more senior secured incremental term loan facilities, subject to conditions. The prior text described a Term Loan Facility and ABL Revolving Loans. MD&A (mdna:8) repeats this and adds that the prior revolving facilities have been terminated. Basis for 'up': the agreement now permits incremental secured term debt, and MD&A (mdna:77) names incremental debt as a source for anticipated acquisition needs.",
  "account": "long-term debt",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "Prior Term Loan Facility, and provided for a new RCF. In addition, the 2026 Credit Agreement will permit the Company to add one or more senior secured incremental term loan facilities to the Amended Term Loan Facility, subject to the satisfaction of certain conditions.",
  "paragraph_id": "0001193125-26-335107:notes:73",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_amended_term_loan_cash_and_cashless_rollover",
  "what_changed": "New. The Amended Term Loan Facility is $400,000, of which $4,000 is short-term and $396,000 long-term. The Company received $119,159 in cash and $280,841 of cashless rollover to pay off the Prior Term Loan Facility (stated as $340,436) plus fees. It is priced at 1-month CME Term SOFR plus 1.75%, its quarterly principal repayments are stated as 1% of the $400,000 initial principal, and its maturity stays at May 30, 2030. The debt table (notes:60) and the issuance-cost table (notes:65) now give new interest-rate and effective-rate figures for the term loan. The prose does not describe those figures. The numbers reader can tie the stated repayment term to current maturities (notes:60) and to the maturity schedule (notes:62); I have not checked it. Basis for 'up': the paragraph says cash was received on top of the rollover, and the cash-flow prose (mdna:69) describes borrowing proceeds 'partially offset' by repayments.",
  "account": "long-term debt (term loan)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The Company received $119,159 in cash and $280,841 of cashless rollover from continuing lenders to pay the full amount of indebtedness outstanding under the Company",
  "paragraph_id": "0001193125-26-335107:notes:75",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_rcf_replaces_us_and_asia_abl",
  "what_changed": "New. The RCF replaces the $150,000 U.S. ABL and the $150,000 Asia ABL, both terminated June 1, 2026. The Company drew $80,000 on the RCF to repay the Asia ABL in full. The $1,000,000 capacity can be drawn in USD to the extent Foreign Subsidiary Borrowers have not drawn on up to $300,000. The RCF matures in May 2031. The debt table now has an 'RCF due May 2031' row, and the Asia ABL and 'Other' rows show no balance at period end. The prose describes swapping one borrowing for another, not new net borrowing, so the direction is 'none'.",
  "account": "revolving credit borrowings (RCF in place of Asia ABL)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "The Company drew $80,000 on the RCF to pay the full amount outstanding under the previous Asia ABL. The $1,000,000 borrowing capacity is available to be drawn in USD by the Company to the extent that Foreign Subsidiary Borrowers (as defined in the 2026 Credit Agreement) have not drawn on the up to $300,000 available.",
  "paragraph_id": "0001193125-26-335107:notes:77",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_rcf_pricing_grid_and_unused_fees",
  "what_changed": "New. RCF pricing is 1-month CME Term SOFR plus a margin of 1.25% to 2.25%, set by the previous quarter's Consolidated Leverage Ratio. Unused-commitment fees run from 0.15% to 0.35% on the same ratio. There is a $200,000 letter-of-credit sublimit, and proceeds may be used for acquisitions. Available capacity was $913,866 at June 29, 2026; MD&A (mdna:70) gives $913.9 million. Because the prose ties the margin to leverage, the RCF margin moves with leverage rather than being fixed.",
  "account": "interest expense",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Borrowings under the RCF bear interest at an interest rate of 1-month CME Term SOFR plus a margin ranging from 1.25% to 2.25% determined by the Company",
  "paragraph_id": "0001193125-26-335107:notes:78",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_credit_agreement_first_priority_security",
  "what_changed": "New. The Guarantors unconditionally guarantee the 2026 Credit Agreement. It is secured by a perfected first-priority security interest in substantially all tangible and intangible assets of the Company and the Guarantors, including capital stock, with pledges of certain foreign-subsidiary stock capped at 65%.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "are secured by a perfected first priority security interest in substantially all of the tangible and intangible assets of the Company and the Guarantors",
  "paragraph_id": "0001193125-26-335107:notes:79",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_rcf_maintenance_covenants_and_acquisition_holiday",
  "what_changed": "New. The RCF has maintenance covenants tested at each fiscal quarter end: consolidated interest coverage of at least 2.50:1.00 and consolidated leverage of no more than 4.50:1.00. The leverage limit rises to 5.00:1.00 for the quarter in which a qualifying material acquisition closes and for the following three quarters. An uncured default allows acceleration. notes:71 now names interest coverage where the prior text named fixed-charge coverage for the ABL Revolving Loans. MD&A (mdna:76) states compliance at June 29, 2026. The STG and ILFA deals are expected to close in Q3 2026, and the prose links the higher leverage limit to such a closing.",
  "account": "none (leverage and interest coverage covenants)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "The maximum consolidated leverage ratio is subject to a customary acquisition holiday that permits the level to increase to 5.00:1.00 for the fiscal quarter in which a qualifying material acquisition is consummated and the following three fiscal quarters.",
  "paragraph_id": "0001193125-26-335107:notes:80",
  "explanation": false }
```

```json
{ "id": "articulation_and_the_filed_history_rcf_covenant_springing_wording",
  "what_changed": "Changed. The sentence now says 'RCF' where it said 'ABL Revolving Loans' and 'interest coverage' where it said 'fixed-charge coverage'. It keeps the springing trigger carried over from the ABL text: 'Under the occurrence of certain events'. notes:80 describes the same RCF covenants as maintenance covenants required 'as of the end of each fiscal quarter', and MD&A (mdna:76) states compliance with no trigger. The two note paragraphs describe the trigger differently. Which one governs is for the supervisor.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Under the occurrence of certain events, the RCF is subject to various financial covenants, including leverage and interest coverage ratios.",
  "paragraph_id": "0001193125-26-335107:notes:71",
  "explanation": false }
```

```json
{ "id": "earnings_quality_loss_on_extinguishment_prior_term_loan",
  "what_changed": "New. The Company recorded a $747 loss on extinguishment of debt for the quarter and the half, 'primarily' related to the Prior Term Loan Facility. It appears as a new line in the reconciliation to income before taxes (notes:34, notes:36). The prose does not say what the rest of the loss relates to, or what happened to the unamortized ABL issuance costs when the ABLs were terminated.",
  "account": "loss on extinguishment of debt (other expense)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "During the quarter and two quarters ended June 29, 2026, the Company recognized loss on extinguishment of debt of $747, primarily related to the Company",
  "paragraph_id": "0001193125-26-335107:notes:82",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_rcf_issuance_costs_in_other_assets",
  "what_changed": "Changed. The capitalized issuance costs held in deposits and other non-current assets now belong to the new RCF and are amortized straight-line over the contractual term of each arrangement. The prior text referred only to the ABL Revolving Loans. MD&A (mdna:69) gives $4.7 million paid for debt issuance costs in the half.",
  "account": "deposits and other non-current assets; interest expense (amortization)",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Remaining unamortized debt issuance costs for the RCF of $5,674 as of June 29, 2026 and the previous U.S. ABL and Asia ABL of $874 as of December 29, 2025 are included in deposits and other",
  "paragraph_id": "0001193125-26-335107:notes:67",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_debt_maturity_schedule_added",
  "what_changed": "Added. The 10-Q now has a five-year fiscal-calendar debt maturity schedule (lead-in at notes:61, table at notes:62). The note history shows no earlier version (matched_by no_prior_note). The amounts are for the numbers reader.",
  "account": "long-term debt",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "The fiscal calendar maturities of debt for the next five years are as follows:",
  "paragraph_id": "0001193125-26-335107:notes:61",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_proposed_stg_and_ilfa_acquisitions",
  "what_changed": "New subsection. On June 17, 2026 the Company announced definitive stock purchase agreements to buy STG and ILFA in separate transactions. Both are expected to close in Q3 2026, subject to regulatory approvals and customary conditions. The notes give no purchase price and do not describe the targets. The only sign of size in the text is the CHF swap notional (notes:7). MD&A (mdna:9) repeats this.",
  "account": "goodwill and intangible assets (on closing)",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "On June 17, 2026, the Company announced that it had entered into definitive stock purchase agreements to acquire STG and ILFA in separate transactions.",
  "paragraph_id": "0001193125-26-335107:notes:112",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_planned_rcf_drawdown_for_stg",
  "what_changed": "New. The STG acquisition is to be funded by a planned RCF drawdown. The economic hedge covers interest on that drawdown as well as the CHF purchase price. MD&A (mdna:9) says the same.",
  "account": "RCF borrowings",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "interest related to the planned drawdown under the RCF to finance the proposed STG acquisition",
  "paragraph_id": "0001193125-26-335107:notes:113",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_deal_contingent_chf_swap",
  "what_changed": "New. On June 18, 2026 the Company entered a deal-contingent, forward-starting, fixed-for-fixed USD/CHF cross-currency swap with a major financial institution. Notional exchanges are $381,083 and CHF 306,200. The Company receives fixed USD at 6.0% and pays fixed CHF at 3.025%. The swap takes effect September 30, 2026, matures September 30, 2033, and depends on STG closing. Its stated purpose is to mitigate the FX risk on the CHF-denominated price and to convert part of the expected USD financing into fixed-rate CHF financing.",
  "account": "derivative assets and liabilities; interest expense after the effective date",
  "expected_direction": "none",
  "horizon": "next quarter (effective September 30, 2026) through 2033",
  "quote": "The instrument is contingent upon the closing of the proposed STG acquisition. The swap has notional exchanges of $381,083 and CHF 306,200, provides for the Company to receive fixed USD interest at 6.0% and pay fixed CHF interest at 3.025%, has an effective date of September 30, 2026, and matures on September 30, 2033.",
  "paragraph_id": "0001193125-26-335107:notes:7",
  "explanation": false }
```

```json
{ "id": "earnings_quality_unrealized_swap_loss_without_hedge_accounting",
  "what_changed": "New. The swap did not qualify for hedge accounting at inception, so its fair-value changes go through earnings. A $13,994 unrealized loss on derivative instruments was recorded for the quarter and the half, and it appears as its own line in the reconciliation (notes:34, notes:36). While the swap stays undesignated, each later mark will also hit earnings.",
  "account": "unrealized loss on derivative instruments (other expense)",
  "expected_direction": "up",
  "horizon": "this quarter; recurring marks next quarter and over 12 months",
  "quote": "The instrument does not qualify for hedge accounting at inception.",
  "paragraph_id": "0001193125-26-335107:notes:8",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_swap_split_across_current_asset_and_long_term_liability",
  "what_changed": "New. The one swap is shown in two places: a $6,825 derivative asset in prepaid expenses and other current assets, and a $20,819 derivative liability in other long-term liabilities. notes:8 describes the two together as a net liability of $13,994. The fair-value table (notes:100) adds a 'Derivatives not designated as hedges' block, and the supplemental table (notes:45) adds a 'Derivative liabilities' line. Whether the pieces tie is for the numbers reader.",
  "account": "prepaid expenses and other current assets; other long-term liabilities",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "As of June 29, 2026, prepaid expenses and other current assets include a derivative asset of $6,825 related to the fair value of the Company",
  "paragraph_id": "0001193125-26-335107:notes:46",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_swap_valuation_deal_contingent_adjustment",
  "what_changed": "Changed. The fair-value method for derivatives now lists USD/CHF spot and forward rates and USD and CHF interest-rate curves. Alongside non-performance risk, it adds an adjustment for 'deal-contingent provisions' (Level 2). That adjustment depends on a judgment about whether the deal closes, and the prose gives no figure or method for it.",
  "account": "derivative assets and liabilities",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "The values were adjusted to reflect non-performance risk of both the counterparty and the Company and deal-contingent provisions, as necessary.",
  "paragraph_id": "0001193125-26-335107:notes:101",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_derivative_accounting_policy_added",
  "what_changed": "Added. Note 1 now has a derivative accounting policy (heading at notes:5). Fair value comes from quoted prices or the Company's estimate. Changes go to earnings or OCI depending on hedge designation. Amounts in AOCI are reclassified when the hedged item affects earnings, or immediately if the hedged transaction ceases to exist.",
  "account": "derivatives; accumulated other comprehensive loss",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Changes in the fair values of derivatives are recorded in net earnings or other comprehensive income (loss), based on whether the instrument is designated and effective as a hedge transaction and, if so, the type of hedge transaction.",
  "paragraph_id": "0001193125-26-335107:notes:6",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_derivative_liabilities_in_contractual_obligations",
  "what_changed": "Changed. MD&A's list of contractual obligations now includes 'derivative liabilities'.",
  "account": "other long-term liabilities (derivative liabilities)",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "interest on debt obligations, derivative liabilities, purchase obligations, and leases.",
  "paragraph_id": "0001193125-26-335107:mdna:81",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_equipment_import_banking_facility",
  "what_changed": "New subsection. In June 2026 the Company entered a banking facility of up to $30,000 that replaces part of the trade credit capacity under the terminated Asia ABL. It is used to pay for imported equipment and can be drawn for up to 'one year and six months'. The fee is 1.25% per annum on the drawn portion. At June 29, 2026, $24,284 of current letters of credit had been issued under it. MD&A (mdna:70) cites $5.7 million of available letters of credit under the facility. The prose implies that equipment purchases are being paid through it.",
  "account": "commitments (letters of credit); property, plant and equipment",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "This banking facility provides the Company with a line of credit for up to an aggregate $30,000, which can be used to facilitate payments over imported equipment.",
  "paragraph_id": "0001193125-26-335107:notes:110",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_two_customers_collectively_named",
  "what_changed": "The concentration sentence now says two customers together accounted for about 26% of net sales in the 2026 quarter and half. The comparative-period sentence names one customer at about 12%. The Q1 2026 text for this tag is not in the input, so I cannot say whether Q1 already named two customers (insufficient on that point). The receivables concentration (notes:25) says one customer was 14% of receivables at both dates. MD&A (mdna:11) gives new top-ten share figures.",
  "account": "net sales; accounts receivable",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "For the quarter and two quarters ended June 29, 2026, two customers collectively accounted for approximately 26% of the Company",
  "paragraph_id": "0001193125-26-335107:notes:26",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_taiwan_above_ten_percent_for_half",
  "what_changed": "New sentence. Net sales in Taiwan exceeded 10% of the total for the two quarters ended June 29, 2026. The same paragraph says no country other than the U.S. exceeded 10% for the June 2026 quarter or for the 2025 periods. The geographic table (notes:41) now has a Taiwan row. Both threshold statements are claims the numbers reader can test against notes:41; I have not tested them.",
  "account": "net sales by country",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "For the two quarters ended June 29, 2026, net sales in Taiwan also exceeded 10% of the Company",
  "paragraph_id": "0001193125-26-335107:notes:40",
  "explanation": false }
```

```json
{ "id": "earnings_quality_discrete_tax_benefit_stock_compensation_deduction",
  "what_changed": "New for the period. There was a net discrete tax benefit of $24,637 for the quarter and $27,452 for the half, mainly from the deduction of stock-based compensation. MD&A (mdna:40, mdna:41) attributes the quarter's income tax benefit, and the lower expense for the half, to the same deduction, partly offset by higher pre-tax income. The prose labels the benefit discrete.",
  "account": "income tax provision",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "effective tax rate was impacted by a net discrete benefit of $24,637 and $27,452, respectively.",
  "paragraph_id": "0001193125-26-335107:notes:85",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_china_hnte_approval_and_return_finalization",
  "what_changed": "New. Part of the discrete benefit is offset by tax expense from finalizing the China and Canada corporate income tax returns, and from the approval of HNTE status for a manufacturing subsidiary in China. The prose ties the HNTE approval to tax expense in this quarter. It says nothing about how the approval affects that subsidiary's tax rate in later periods.",
  "account": "income tax provision; deferred income taxes",
  "expected_direction": "up",
  "horizon": "this quarter; effect after this quarter not stated",
  "quote": "partially offset by tax expenses related to the finalization of China and Canada corporate income tax returns and the approval of the High and New Technology Enterprise (HNTE) status for a manufacturing subsidiary in China.",
  "paragraph_id": "0001193125-26-335107:notes:85",
  "explanation": false }
```

```json
{ "id": "earnings_quality_stock_compensation_targets_and_performance_vesting",
  "what_changed": "MD&A attributes the half-year rise in stock-based compensation to beating predetermined targets, stock price appreciation, and vesting of certain performance-based grants. In the segment reconciliation, stock-based compensation is an unallocated line (mdna:47, notes:36). The same vesting drives the discrete tax deduction in notes:85.",
  "account": "stock-based compensation (operating expenses)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "primarily driven by exceeding predetermined targets, stock price appreciation, and vesting of certain performance",
  "paragraph_id": "0001193125-26-335107:mdna:32",
  "explanation": false }
```

```json
{ "id": "earnings_quality_acquisition_costs_in_operating_expenses",
  "what_changed": "MD&A now lists 'acquisition costs' among the reasons operating expenses rose in the quarter, and in the half (mdna:32). The segment reconciliation has an unallocated 'Acquisition-related and other charges' line for the 2026 periods and none for 2025 (mdna:47, notes:34, notes:36). The prose expects STG and ILFA to close in Q3 2026, which puts more such costs in next quarter.",
  "account": "operating expenses (acquisition-related and other charges)",
  "expected_direction": "up",
  "horizon": "this quarter and next quarter",
  "quote": "primarily due to higher labor costs, incentive compensation, and acquisition costs.",
  "paragraph_id": "0001193125-26-335107:mdna:31",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_net_sales_ai_data_center_buildout",
  "what_changed": "The quarter's sales explanation names data center and networking demand from AI data center build-out as the main driver, plus strong growth in A&D and in medical, industrial, and instrumentation. The half-year paragraph (mdna:25 to mdna:26) gives the same drivers, and the Commercial segment paragraph (mdna:60) repeats the data center driver. The Q1 wording is not in the input.",
  "account": "net sales",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The primary driver of this increase was due to continued strong demand in our data center and networking end market driven by the continued build out of AI data centers and related applications, as well as strong growth in our aerospace and defense and medical, industrial, and instrumentation end markets.",
  "paragraph_id": "0001193125-26-335107:mdna:24",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_gross_margin_volume_mix_execution",
  "what_changed": "The rise in gross profit and gross margin is attributed to higher sales volume, favorable product mix, and improved operational execution. The same three drivers are given for the half (mdna:29) and for A&D and Commercial segment operating income (mdna:56, mdna:63).",
  "account": "gross profit and gross margin",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "These increases were primarily due to higher sales volume, favorable product mix, and improved operational execution.",
  "paragraph_id": "0001193125-26-335107:mdna:28",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_a_and_d_defense_spending_and_restricted_programs",
  "what_changed": "A&D segment sales growth is attributed to defense budget spending, strategic program alignment, and key bookings for ongoing franchise programs including restricted programs. The paragraph also names higher missiles-and-munitions sales and strong demand in mission systems and specialty assembly. The prose ties some of this to bookings, so it points beyond the quarter.",
  "account": "A&D segment sales",
  "expected_direction": "up",
  "horizon": "this quarter; 12 months on the bookings",
  "quote": "The primary drivers of this increase were strong defense budget spending, our strong strategic program alignment, and key bookings for ongoing franchise programs, including restricted programs.",
  "paragraph_id": "0001193125-26-335107:mdna:52",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_rmb_and_myr_strengthening",
  "what_changed": "The other-expense explanation now cites FX losses from a strengthening RMB and MYR. It says the Company uses RMB and MYR at its China and Malaysia facilities for employee-related and other operating costs, an exposure that continues for as long as those currencies stay strong.",
  "account": "other expense, net (foreign exchange losses)",
  "expected_direction": "up",
  "horizon": "this quarter; 12 months",
  "quote": "We utilize the RMB and MYR at our China and Malaysia facilities, respectively, for employee",
  "paragraph_id": "0001193125-26-335107:mdna:37",
  "explanation": false }
```

```json
{ "id": "across_documents_other_expense_explanation_omits_swap_and_extinguishment_losses",
  "what_changed": "MD&A attributes the rise in total other expense 'primarily' to FX losses, here and for the half (mdna:38). It does not mention the $13,994 unrealized loss on derivative instruments (notes:8) or the $747 loss on extinguishment of debt (notes:82). Both appear as new lines in the quarter's reconciliation to income before taxes (notes:34). Whether 'primarily' fits the components is for the numbers reader and the supervisor; I have not compared them.",
  "account": "total other expense, net",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Total other expense, net increased $11.6 million to $27.8 million for the quarter ended June 29, 2026, from $16.2 million for the quarter ended June 30, 2025, primarily due to a higher amount of foreign exchange losses",
  "paragraph_id": "0001193125-26-335107:mdna:37",
  "explanation": false }
```

```json
{ "id": "earnings_quality_operating_cash_flow_collections_timing",
  "what_changed": "MD&A says operating cash flow rose on higher net income, partly offset by more working capital 'largely driven by the timing of collections'. In other words, management explains a build in receivables as a matter of collection timing. A timing explanation implies the build reverses in a later period.",
  "account": "accounts receivable",
  "expected_direction": "up",
  "horizon": "this quarter (timing implies reversal next quarter)",
  "quote": "partially offset by increased working capital largely driven by the timing of collections.",
  "paragraph_id": "0001193125-26-335107:mdna:67",
  "explanation": true }
```

```json
{ "id": "liquidity_and_capital_asset_sale_proceeds_in_investing",
  "what_changed": "The investing paragraph now cites $12.0 million of proceeds from selling property, plant, and equipment and other assets in the half; no such proceeds are named for 2025. They sit next to $169.2 million of net purchases, which the prose says the proceeds 'partially offset'. The prose does not say what was sold or whether a gain or loss was booked.",
  "account": "property, plant and equipment",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "partially offset by the receipt of $12.0 million of proceeds from the sale of property, plant, and equipment and other assets.",
  "paragraph_id": "0001193125-26-335107:mdna:68",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_customer_deposit_repayments",
  "what_changed": "The financing paragraph now cites $5.0 million of customer-deposit repayments and $4.7 million of debt issuance cost payments in the half. In the comparative half it names only share repurchases and debt repayment. Customer deposits are a line in other long-term liabilities (notes:45), and the prose says they are being repaid.",
  "account": "customer deposits (other long-term liabilities)",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "repayments of $5.0 million for customer deposits, and $4.7 million for payment of debt issuance costs.",
  "paragraph_id": "0001193125-26-335107:mdna:69",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_capex_guidance_for_capacity_expansion",
  "what_changed": "MD&A gives 2026 capital expenditure guidance of $345.0 million to $365.0 million, mainly for capacity expansion to meet demand. The earlier guidance is not in my input, so I cannot say whether the range moved. The equipment-import letter-of-credit facility (notes:110) points the same way.",
  "account": "property, plant and equipment; capital expenditures",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "Our total 2026 capital expenditures are expected to be in the range of $345.0 million to $365.0 million, primarily for capacity expansion to meet market demand.",
  "paragraph_id": "0001193125-26-335107:mdna:71",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_acquisitions_named_as_principal_cash_demand",
  "what_changed": "MD&A's statement of the main future demands on cash now names the proposed STG and ILFA acquisitions.",
  "account": "cash and cash equivalents",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "financing acquisitions including but not limited to the proposed STG and ILFA acquisitions",
  "paragraph_id": "0001193125-26-335107:mdna:66",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_liquidity_adequacy_relies_on_incremental_debt",
  "what_changed": "The 12-month liquidity adequacy statement now counts 'cash from the issuance of available term, incremental, and revolving debt' as a source. It lists acquisitions among the needs.",
  "account": "long-term debt",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "cash from the issuance of available term, incremental, and revolving debt will be adequate to meet our currently anticipated capital expenditure, acquisitions, debt service, and working capital needs for the next 12 months.",
  "paragraph_id": "0001193125-26-335107:mdna:77",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_interest_obligations_schedule_stated",
  "what_changed": "MD&A now states aggregate interest on debt obligations of $162.8 million, with a schedule of when it will be paid; variable-rate debt uses June 29, 2026 rates. mdna:84 now says there were no 'other' material changes to contractual obligations. The schedule is as of June 29, 2026, and the prose does not say whether it reflects the planned STG drawdown.",
  "account": "interest on debt obligations",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Our aggregate interest on debt obligations as of June 29, 2026, amounted to $162.8 million, which is expected to be settled as follows: $45.9 million within 1 year",
  "paragraph_id": "0001193125-26-335107:mdna:83",
  "explanation": false }
```

```json
{ "id": "across_documents_credit_agreement_eight_k_item_codes",
  "what_changed": "The 8-K list has a 2026-06-03 filing (0001193125-26-255711) with items 1.01, 1.02, 2.03, 3.03, 7.01 and 9.01. Its timing matches the June 1, 2026 credit agreement, the ABL terminations and the new borrowing in notes:73 to notes:80. Item 3.03 (material modification to rights of security holders) has no counterpart in the 10-Q prose; the closest is the dividend limitation in notes:80. The 8-K body is not in the input.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "1.01, 1.02, 2.03, 3.03, 7.01, 9.01",
  "paragraph_id": "0001193125-26-255711:8k_item_codes",
  "explanation": false }
```

```json
{ "id": "across_documents_acquisition_agreements_filed_as_other_events",
  "what_changed": "The only 8-K on record near the June 17, 2026 announcement is dated 2026-06-18 (0001193125-26-274429), with items 8.01 and 9.01 and no item 1.01. On the item codes alone, the STG and ILFA stock purchase agreements were not filed as material definitive agreements. The body is not in the input.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "2026-06-18 0001193125-26-274429",
  "paragraph_id": "0001193125-26-274429:8k_item_codes",
  "explanation": false }
```

```json
{ "id": "controls_audit_and_filings_no_quarter_earnings_release_on_record",
  "what_changed": "The item-code list has no Item 2.02 filing between the first-quarter release on 2026-04-29 and the 10-Q date of 2026-08-05. Every earlier year in the list has a 2.02 in late July or early August. The release may have been filed after the 10-Q, or it may be missing from the collection; the bundle cannot tell which.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "this bundle has no earnings release and no verbatim item body.",
  "paragraph_id": "input_8k:header",
  "explanation": false }
```

## Paragraphs carried as text and not made into items

The note change history (`note_history:1`–`49`) was used only to find what changed; it is not listed again here. Lines marked `insufficient` are paragraphs where the prior text is not in my input and I cannot tell whether anything substantive changed.

**Item 4 — controls**
- `item_4_controls:1`: heading.
- `item_4_controls:2`: heading.
- `item_4_controls:3`: date rolled forward; still concludes "effective".
- `item_4_controls:4`: standard limitations language.
- `item_4_controls:5`: heading.
- `item_4_controls:6`: date rolled forward; still says no change in internal control over financial reporting.
- `item_4_controls:7`: page number.

**MD&A**
- `mdna:8`: same change as `liquidity_and_capital_credit_agreement_amends_term_loan_and_adds_rcf`.
- `mdna:9`: same change as the STG/ILFA acquisition, CHF swap and planned RCF drawdown items.
- `mdna:11`: amounts only (top-ten customer shares).
- `mdna:13`: table; amounts only.
- `mdna:14`: date rolled forward (recast for the combined data center and networking end market).
- `mdna:22`: table; amounts only.
- `mdna:25`: half-year repeat of the `mdna:24` drivers.
- `mdna:26`: half-year repeat of the `mdna:24` drivers (A&D and MI&I in a different order).
- `mdna:29`: half-year repeat of the `mdna:28` drivers.
- `mdna:34`: amounts; refers back to the drivers above.
- `mdna:35`: amounts; refers back to the drivers above.
- `mdna:38`: half-year repeat of `mdna:37`; covered by the two `mdna:37` items.
- `mdna:40`: same change as `earnings_quality_discrete_tax_benefit_stock_compensation_deduction`.
- `mdna:41`: same change as `earnings_quality_discrete_tax_benefit_stock_compensation_deduction`.
- `mdna:42`: insufficient. Reads as amounts and dates rolled forward; I cannot check the list of effective-tax-rate factors against the prior text.
- `mdna:47`: table; amounts. Its new "Acquisition-related and other charges" line is covered by `earnings_quality_acquisition_costs_in_operating_expenses`.
- `mdna:48`: insufficient. Amortization relates to A&D but is not reviewed separately by the CODM; prior text not in input.
- `mdna:49`: insufficient. Statement that segment measures fall outside non-GAAP rules; prior text not in input.
- `mdna:53`: half-year repeat of the `mdna:52` drivers.
- `mdna:55`: same driver language as `results_against_expectations_gross_margin_volume_mix_execution`.
- `mdna:56`: same driver language as `results_against_expectations_gross_margin_volume_mix_execution`.
- `mdna:57`: half-year repeat.
- `mdna:60`: Commercial sales drivers repeat `results_against_expectations_net_sales_ai_data_center_buildout`.
- `mdna:61`: half-year repeat.
- `mdna:63`: same driver language as the gross margin item ("improving mix").
- `mdna:64`: half-year repeat.
- `mdna:70`: cash amounts. RCF capacity and banking-facility letters of credit are covered by the RCF and banking facility items.
- `mdna:73`: date rolled forward; no repurchases, amount remaining unchanged.
- `mdna:75`: amounts; debt composition covered by the term loan and RCF items.
- `mdna:76`: same change as the RCF covenant items.
- `mdna:79`: amounts only (supplier finance; duplicates `notes:108`).
- `mdna:82`: date rolled forward.
- `mdna:84`: wording ("other") and date; context noted in `liquidity_and_capital_interest_obligations_schedule_stated`.
- `mdna:87`: heading.

**Notes**
- `notes:5`: heading for the added policy (covered by the policy item).
- `notes:9`: heading.
- `notes:10`: not flagged as changed in the note history; ASU text unchanged in substance.
- `notes:11`: not flagged as changed in the note history; ASU text unchanged in substance.
- `notes:12`: not flagged as changed in the note history; ASU text unchanged in substance.
- `notes:14`: amounts only. The loss-contract remaining-cost figure is updated with no explanation, so no explanation flag.
- `notes:15`: amounts only (remaining performance obligations and the share expected within 12 months).
- `notes:16`: amounts and period rolled to the half.
- `notes:17`: amounts and period rolled to the half.
- `notes:19`: table; amounts only.
- `notes:20`: table; amounts only.
- `notes:21`: date rolled forward. The reference to the June 2025 reorganization drops out because the comparative period is now that quarter.
- `notes:24`: amounts only.
- `notes:25`: insufficient. One customer is 14% of receivables at both dates; prior text not in input.
- `notes:29`: insufficient. CODM and segment description; prior text not in input.
- `notes:32`: table; amounts only.
- `notes:33`: table; amounts only.
- `notes:34`: table. Its new lines are covered by the extinguishment, unrealized swap loss and acquisition-cost items.
- `notes:35`: prior-year table; amounts only.
- `notes:36`: table. Its new lines are covered by the same items as `notes:34`.
- `notes:37`: prior-year table; amounts only.
- `notes:39`: table; amounts only.
- `notes:41`: table. The Taiwan row is covered by `structure_and_disclosure_changes_taiwan_above_ten_percent_for_half`.
- `notes:42`: insufficient. Definition of long-lived assets; prior text not in input.
- `notes:43`: amounts only.
- `notes:45`: table; amounts. The new "Derivative liabilities" line is covered by the swap split item.
- `notes:50`: date rolled forward.
- `notes:53`: amounts only.
- `notes:54`: insufficient. Amortization method lead-in; prior text not in input.
- `notes:55`: amounts only.
- `notes:57`: amounts only.
- `notes:58`: heading.
- `notes:59`: heading.
- `notes:60`: table; new rows covered by the term loan and RCF items.
- `notes:62`: table; covered by `structure_and_disclosure_changes_debt_maturity_schedule_added`.
- `notes:63`: heading.
- `notes:64`: heading.
- `notes:65`: amounts only. The term loan's effective-rate figure is updated; left to the numbers reader through the term loan item.
- `notes:66`: not flagged as changed in the note history; wording.
- `notes:68`: amounts only (weighted average amortization period).
- `notes:69`: heading.
- `notes:70`: wording only ("Amended Term Loan Facility").
- `notes:72`: heading.
- `notes:74`: heading.
- `notes:76`: heading.
- `notes:81`: heading.
- `notes:86`: insufficient. Repatriation and deferred-tax-liability policy; prior text not in input.
- `notes:90`: amounts only.
- `notes:91`: amounts only (stock options no longer named for 2026).
- `notes:94`: date rolled forward.
- `notes:97`: amounts only.
- `notes:100`: table. New rows are covered by the swap split and RCF items.
- `notes:102`: insufficient. Debt fair-value basis; prior text not in input.
- `notes:103`: insufficient. Other financial instruments; prior text not in input.
- `notes:104`: heading.
- `notes:105`: heading.
- `notes:106`: date rolled forward (note history confirms).
- `notes:107`: heading.
- `notes:108`: amounts only (note history confirms).
- `notes:109`: heading.
- `notes:111`: heading.

**8-K item-code lines** (no bodies in the input)
- 2026-05-08, 0001193125-26-214668 (5.02, 5.07, 8.01, 9.01): codes only, no body to read.
- 2026-05-08, 0001193125-26-214701 (5.02, amends 0001193125-26-032638): codes only, no body to read.
- 2026-05-18, 0001193125-26-229075 (7.01): codes only, no body to read.
- 2026-05-27, 0001193125-26-240340 (7.01): codes only, no body to read.
- Lines dated on or before 2026-04-29: history from before the prior 10-Q.
- Late-filing notifications: none on record.

## Counts

- 40 items.
- 1 item with `explanation: true` (`earnings_quality_operating_cash_flow_collections_timing`, on receivables). No carried prose explains inventory or reserves.
- 10 paragraphs marked `insufficient`, plus one point inside `structure_and_disclosure_changes_two_customers_collectively_named`.
