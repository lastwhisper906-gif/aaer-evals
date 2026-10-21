<!-- the quote gate removed 1 item(s) from this copy; input_manifest.json lists each with its reason -->
# Notes text reader: MU 10-K 0000723125-26-000023 (fiscal year ended September 3, 2026)

## Scope and inputs

- **Read in full:**
  - `input_notes.md`: paragraphs notes:1 to notes:193.
  - `input_mdna.md`: mdna:1 to mdna:115.
  - `input_controls.md`: auditors_report:1 to auditors_report:24, and item_9a:1 to item_9a:8.
  - `input_8k.md`: the item-code index, plus the body of the 2026-09-30 item 2.02 release, 8k_2_02:1 to 8k_2_02:88.
  - `input_notes_history.md` and `input_prior_predictions.md`.
- **Nothing out of bounds is in the directory.** There is no trend table, no prices, no abnormal returns, no short interest, no other company's files, no prior-run probability and no outcome window. The earnings-release exhibit carries its own statements. Those are 8-K body; I read them as text and did no arithmetic on them.
- **Not in the directory:** no Item 1A diff, no Exhibit 21 diff, and no Exhibit 10. No item can come from them.
- **8-K bodies.** Only the 2026-09-30 item 2.02 body is present. The index also lists:
  - an item 5.02 filed 2026-08-26, after the last 10-Q;
  - an item 5.02 filed 2026-06-09;
  - item 8.01 filings dated 2026-03-25 and 2026-04-01.

  None of those bodies is in the input.
- **Diff layer.** No paragraph in the notes, MD&A or controls files is marked `[same as prior period ...]`. Every paragraph is carried as text, so every paragraph is accounted for below.
  - The note change history covers the Q2 to Q3 10-Q change (0000723125-26-000006 to 0000723125-26-000015). It does not cover the prior 10-K to this 10-K.
  - Where an item calls something new, the basis is either the history's added or removed text, or the paragraph itself dating the event to fiscal 2026.
  - Where the input cannot show whether standing text changed from the prior 10-K, the paragraph list says so.
- **Prior predictions:** none on record.
- **Management explanations** (`explanation: true`): two, both in mdna:92. One is receivables; the other is the consideration-payable-to-customers reserve. No prose in the input gives a cause for the fiscal 2026 inventory figures.
- **Counts:** 56 items. 8 have `expected_direction` of `insufficient`, and 2 carry `explanation: true`.

## Items

```json
{ "id": "revenue_recognition_policy_adds_take_or_pay_strategic_agreements",
  "what_changed": "The revenue policy no longer says substantially all contracts are short-term at fixed, negotiated prices; the history shows that sentence removed after the Q2 10-Q at [0000723125-26-000006:note_history:18]. It now says only certain contracts are short-term. It adds multi-year take-or-pay strategic customer agreements with binding, contractually enforceable volumes, priced either fixed or periodically negotiated, with the majority subject to minimum and maximum price bands. Revenue is still recognized at a point in time when control transfers, and payments are still generally due shortly after delivery. notes:140 repeats the same policy text.",
  "account": "revenue",
  "expected_direction": "none",
  "horizon": "this quarter onward, for the multi-year contract terms",
  "quote": "Contracts with certain of our customers are short-term in duration. We also have strategic customer agreements structured as take-or-pay agreements, with binding commitments for specific contractually enforceable volumes over the multi-year contract terms.",
  "paragraph_id": "0000723125-26-000023:notes:42",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_retained_customer_deposits_become_revenue",
  "what_changed": "New: a deposit is returned if the customer meets its minimum purchase commitments. If it does not, the company may keep all or part of the deposit, and the kept amount is recognized as revenue. No retention is described as having happened. Any kept deposit would be revenue with no product shipped against it.",
  "account": "revenue; customer contract liabilities",
  "expected_direction": "none",
  "horizon": "12 months and later; notes:141 says nearly all deposits are scheduled to be repaid between 2029 and 2031",
  "quote": "If not, we may retain all, or a portion of the deposit which will be recognized as revenue.",
  "paragraph_id": "0000723125-26-000023:notes:43",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_customer_deposits_no_significant_financing_component",
  "what_changed": "New judgment: the strategic-agreement deposits do not contain a significant financing component, so no interest is accreted on them and the transaction price is not adjusted for them. notes:141 says $13 billion is recognized as contract liabilities. The stated reason is that the payments secure future capacity and supply, not financing.",
  "account": "interest expense; revenue (transaction price); customer contract liabilities",
  "expected_direction": "none",
  "horizon": "this quarter and every period the deposits are held",
  "quote": "Customer deposits do not represent significant financing components because the payments are primarily intended to secure future production capacity and ensure supply availability rather than provide financing to us.",
  "paragraph_id": "0000723125-26-000023:notes:43",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_customer_contract_liabilities_current_noncurrent_split",
  "what_changed": "New: deposits are classified between other current liabilities and a new noncurrent customer contract liabilities line by the expected timing of satisfying the performance obligations, not by when the deposits are repaid. The Q3 10-Q said contract liabilities were primarily included in other noncurrent liabilities ([0000723125-26-000015:note_history:16]). The earnings-release balance sheet (8k_2_02:60) carries the new caption Noncurrent customer contract liabilities, including in its May 28, 2026 column. notes:16 says prior-period amounts were reclassified without affecting totals.",
  "account": "noncurrent customer contract liabilities; other noncurrent liabilities; other current liabilities",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Deposits are classified as contract liabilities in other current liabilities or noncurrent customer contract liabilities depending on the expected timing of the satisfaction of the underlying performance obligations.",
  "paragraph_id": "0000723125-26-000023:notes:43",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_remaining_performance_obligations_year_end_disclosure",
  "what_changed": "New year-end disclosure of remaining performance obligations: about $134 billion, of which $13 billion is recognized as contract liabilities. About one-fourth is expected to be recognized as revenue over the next twelve months, and all of it within five years. Nearly all deposits are repayable between 2029 and 2031. At August 28, 2025 they are called not material. The Q3 10-Q stated about $5 billion with one-third expected within twelve months ([0000723125-26-000015:note_history:16]); the twelve-month fraction now reads one-fourth. The prose states levels and fractions only, and turning them into a direction for revenue would take arithmetic.",
  "account": "remaining performance obligations; revenue",
  "expected_direction": "insufficient",
  "horizon": "12 months for the one-fourth portion; five years in full",
  "quote": "As of September 3, 2026, the transaction price allocated to our remaining performance obligations was approximately $134 billion, of which $13 billion has been recognized as contract liabilities.",
  "paragraph_id": "0000723125-26-000023:notes:141",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_remaining_obligations_measured_on_expected_purchases",
  "what_changed": "The basis for measuring remaining performance obligations has changed. The Q3 10-Q said the disclosure was based on minimum committed volumes and minimum pricing ([0000723125-26-000015:note_history:15]). The 10-K says it is based on expected purchases to satisfy committed volumes and minimum pricing, which brings management's expectation of purchases into the measure. Agreements without fixed pricing or price bands are still excluded, and the figure is still said not to indicate future revenue.",
  "account": "remaining performance obligations",
  "expected_direction": "insufficient",
  "horizon": "this quarter",
  "quote": "Our remaining performance obligations are based on expected purchases to satisfy committed volumes and minimum pricing and are not expected to be indicative of future revenue under these contracts.",
  "paragraph_id": "0000723125-26-000023:notes:142",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_strategic_agreement_deposits_received_and_repayable",
  "what_changed": "New: $12.75 billion of cash deposits were received in 2026 under strategic customer agreements entered into with a number of customers. The deposits are returned if customers meet minimum purchase commitments and may be kept if they do not. Nearly all are scheduled to be repaid between 2029 and 2031.",
  "account": "cash; customer contract liabilities",
  "expected_direction": "up",
  "horizon": "this quarter; outflow on repayment in 2029 to 2031",
  "quote": "In connection with these strategic customer agreements, we received cash deposits of $12.75 billion in 2026.",
  "paragraph_id": "0000723125-26-000023:mdna:66",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_customer_letters_of_credit_backing_agreements",
  "what_changed": "New: certain agreements require customers to maintain letters of credit with third-party financial institutions. The amount issued or committed is $7 billion, described as the maximum potential proceeds available on customer default or breach. Letters of credit are not recognized as revenue unless a default or breach occurs. mdna:66 gives the same $7 billion without the maximum-potential-proceeds clause, and notes:44 repeats the terms without an amount.",
  "account": "none (off-balance-sheet credit support); revenue only on default or breach",
  "expected_direction": "none",
  "horizon": "12 months and the multi-year contract terms",
  "quote": "The aggregate amount of letters of credit issued, or contractually committed to be issued, by third-party financial institutions was $7 billion as of September 3, 2026, which represented the maximum potential proceeds available to us in the event of customer default or breach.",
  "paragraph_id": "0000723125-26-000023:notes:143",
  "explanation": false }
```

```json
{ "id": "across_documents_customer_deposits_reported_as_financing_cash_inflow",
  "what_changed": "New financing-activity source. MD&A and the earnings-release cash flow statement (line 'Proceeds from customer contract liability deposits', 8k_2_02:66) present the $12.75 billion of deposits as financing activities. mdna:64 calls them significant funding. notes:43, by contrast, says the payments are intended to secure capacity rather than provide financing to us. Reconciling the two characterizations is the supervisor's task. As presented, the deposits sit outside operating cash flow and outside the adjusted free cash flow build in 8k_2_02:73.",
  "account": "net cash provided by (used for) financing activities",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "For 2026, net cash provided by financing activities consisted primarily of $12.75 billion of proceeds from customer contract liability deposits on strategic customer agreements",
  "paragraph_id": "0000723125-26-000023:mdna:97",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_funding_sources_now_include_customer_deposits",
  "what_changed": "The liquidity-sources paragraph now names customer deposits under strategic customer agreements, alongside government assistance, as significant funding. It moves capital-markets and bank financing to 'in prior years'. mdna:87 likewise adds customer deposits under strategic customer agreements to the sources expected to be sufficient for at least the next 12 months.",
  "account": "customer contract liabilities; cash",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "We also receive significant funding from government assistance and customer deposits associated with strategic customer agreements. In prior years, we have obtained significant financing from capital markets and financial institutions.",
  "paragraph_id": "0000723125-26-000023:mdna:64",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_price_band_floor_margin_claim",
  "what_changed": "New forward claim: gross margins from price-band agreements, even at floor prices, are expected to be meaningfully above the company's peak quarterly margins in any past cycle. The agreements are said to significantly enhance the durability and predictability of financial performance. The input does not disclose the band floors or contract-level margins.",
  "account": "gross margin",
  "expected_direction": "none",
  "horizon": "12 months and the multi-year contract terms",
  "quote": "We expect gross margins from our strategic customer agreements with price bands, even at floor pricing levels, to yield gross margins meaningfully above our peak quarterly margins in any past cycle.",
  "paragraph_id": "0000723125-26-000023:mdna:11",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_more_strategic_agreements_expected",
  "what_changed": "New: strategic customer agreements were entered into in the third and fourth quarters of 2026, and management expects to keep entering into them. They are said to give customers supply assurance and pricing visibility, and the company visibility and stability.",
  "account": "customer contract liabilities; remaining performance obligations",
  "expected_direction": "up",
  "horizon": "next quarter and 12 months",
  "quote": "In the third and fourth quarters of 2026, we entered into, and expect to continue to enter into, strategic customer agreements.",
  "paragraph_id": "0000723125-26-000023:mdna:10",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_supply_allocation_among_customers",
  "what_changed": "New for 2026: AI-driven demand is said to be growing faster than both the company's and the industry's ability to add supply. This has led to supply-allocation decisions that may affect certain customers and end markets. Constrained supply is credited with higher pricing.",
  "account": "bit shipments to deprioritized customers and end markets",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "This has led to decisions on supply allocation that may impact certain customers and end markets.",
  "paragraph_id": "0000723125-26-000023:mdna:7",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_mobile_client_supply_redirected",
  "what_changed": "New driver: MCBU bit shipments were lower because MCBU supply was redirected to other business units; MCBU revenue still rose on price. mdna:41 names only CMBU, CDBU and AEBU as also benefiting from higher bit shipments.",
  "account": "MCBU bit shipments; MCBU revenue",
  "expected_direction": "down",
  "horizon": "this year (fiscal 2026 as reported)",
  "quote": "MCBU revenue increased 209% primarily due to increases in average selling prices, partially offset by lower bit shipments as MCBU product supply was redirected to other business units.",
  "paragraph_id": "0000723125-26-000023:mdna:31",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_dram_revenue_growth_attributed_to_price",
  "what_changed": "Management attributes 2026 DRAM revenue growth mainly to an approximate 180% increase in average selling prices, with a mid-20% range increase in bit shipments. The 53-week fiscal year (notes:17) is not cited as a factor.",
  "account": "revenue (DRAM)",
  "expected_direction": "up",
  "horizon": "this year (fiscal 2026 as reported)",
  "quote": "Sales of DRAM products increased 252% primarily due to an approximate 180% increase in average selling prices and a mid-20% range increase in bit shipments.",
  "paragraph_id": "0000723125-26-000023:mdna:18",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_nand_revenue_growth_attributed_to_price",
  "what_changed": "Management attributes 2026 NAND revenue growth mainly to an approximate 200% increase in average selling prices, with a mid-20% range increase in bit shipments. The 53-week fiscal year is not cited as a factor.",
  "account": "revenue (NAND)",
  "expected_direction": "up",
  "horizon": "this year (fiscal 2026 as reported)",
  "quote": "Sales of NAND products increased 274% primarily due to an approximate 200% increase in average selling prices and a mid-20% range increase in bit shipments.",
  "paragraph_id": "0000723125-26-000023:mdna:19",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_gross_margin_attributed_to_price_mix_and_cost",
  "what_changed": "The prose says consolidated gross margin improved to 81% for 2026 from 40% for 2025. It credits this mainly to higher average selling prices, with help from favorable mix and lower manufacturing costs. No inventory write-down, reserve release or the extra week is named as a factor.",
  "account": "gross margin",
  "expected_direction": "up",
  "horizon": "this year (fiscal 2026 as reported)",
  "quote": "Margins improved primarily due to increases in average selling prices and also benefited from favorable mix and manufacturing cost reductions due to continued strong execution.",
  "paragraph_id": "0000723125-26-000023:mdna:23",
  "explanation": false }
```

```json
{ "id": "earnings_quality_research_spend_driven_by_variable_compensation",
  "what_changed": "The 2026 R&D increase is attributed to employee compensation, including higher variable compensation, and to more development and pre-qualification wafers as R&D investment ramps for long-term opportunities.",
  "account": "research and development",
  "expected_direction": "up",
  "horizon": "this year and 12 months",
  "quote": "R&D expenses for 2026 increased 49% as compared to 2025 primarily due to increases in employee compensation, including higher variable compensation expense, and higher volumes of development and pre-qualification wafers, as we ramp R&D investments in support of long-term opportunities in memory and storage.",
  "paragraph_id": "0000723125-26-000023:mdna:50",
  "explanation": false }
```

```json
{ "id": "earnings_quality_administrative_spend_adds_community_investments",
  "what_changed": "The 2026 SG&A increase is attributed to employee compensation, including higher variable compensation, and to community investments. The input does not otherwise describe community investments as a cost driver.",
  "account": "selling, general, and administrative",
  "expected_direction": "up",
  "horizon": "this year (fiscal 2026 as reported)",
  "quote": "SG&A expenses for 2026 increased 62% as compared to 2025 primarily due to increases in employee compensation, including higher variable compensation expense, and community investments.",
  "paragraph_id": "0000723125-26-000023:mdna:51",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_interest_income_up_interest_expense_down",
  "what_changed": "The improvement in net interest is attributed to higher interest income on higher cash and investment balances, and to lower interest expense on lower debt balances. The earnings-release income statement (8k_2_02:55) shows a dash for interest expense in both the fourth and third quarters. notes:69 states $383 million of interest capitalized into property, plant and equipment in 2026. Reconciling capitalized against expensed interest is for the supervisor.",
  "account": "interest income; interest expense",
  "expected_direction": "up",
  "horizon": "this year (fiscal 2026 as reported)",
  "quote": "Interest income (expense) improved in 2026 as compared to 2025 primarily due to an increase in interest income due to higher cash and investments balances and a decrease in interest expense due to lower debt balances.",
  "paragraph_id": "0000723125-26-000023:mdna:52",
  "explanation": false }
```

```json
{ "id": "earnings_quality_pillar_two_drives_effective_tax_rate",
  "what_changed": "New: the change in the 2026 effective tax rate is attributed primarily to the Pillar Two 15% minimum tax. Singapore's implementing legislation took effect for the company in 2026 and largely offsets the benefit of its Singapore tax incentive arrangements.",
  "account": "income tax provision; effective tax rate",
  "expected_direction": "up",
  "horizon": "this year and later years while the Singapore incentive and Pillar Two both apply",
  "quote": "Singapore enacted legislation to implement Pillar Two, effective for us in 2026, which largely offsets the benefit from our Singapore tax incentive arrangements.",
  "paragraph_id": "0000723125-26-000023:mdna:55",
  "explanation": false }
```

```json
{ "id": "earnings_quality_singapore_incentive_and_top_up_tax_amounts",
  "what_changed": "New amounts. Singapore tax incentives reduced the 2026 provision by $11.22 billion, largely offset by $9.03 billion of qualified domestic minimum top-up taxes under Pillar Two. The net benefit was $2.21 billion, or $1.93 per diluted share. mdna:56 gives the same net figures.",
  "account": "income tax provision",
  "expected_direction": "up",
  "horizon": "this year (fiscal 2026 as reported)",
  "quote": "This benefit was largely offset by $9.03 billion of qualified domestic minimum top-up taxes",
  "paragraph_id": "0000723125-26-000023:notes:158",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_noncurrent_income_taxes_payable_from_pillar_two",
  "what_changed": "The note states income taxes payable inside other noncurrent liabilities of $9.82 billion at September 3, 2026 and $648 million at August 28, 2025. mdna:92 attributes the increase in noncurrent liabilities largely to higher noncurrent income taxes payable related to implementing Pillar Two. Neither text gives a payment date beyond classifying the amount as noncurrent.",
  "account": "other noncurrent liabilities (income taxes payable)",
  "expected_direction": "up",
  "horizon": "this year; cash payment beyond 12 months",
  "quote": "Other noncurrent liabilities included $9.82 billion and $648 million related to income taxes payable as of September 3, 2026 and August 28, 2025, respectively.",
  "paragraph_id": "0000723125-26-000023:notes:159",
  "explanation": false }
```

```json
{ "id": "earnings_quality_receivables_increase_attributed_to_higher_revenue",
  "what_changed": "Management gives the cause of the 2026 receivables movement as a significant increase due to higher revenue. notes:62 splits receivables into trade, government incentives, income and other taxes, and other; no prose speaks to the parts, collection terms or days outstanding. notes:42 still says payments are generally due shortly after delivery.",
  "account": "receivables",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "These increases were partially offset by a significant increase in receivables due to higher revenue in 2026.",
  "paragraph_id": "0000723125-26-000023:mdna:92",
  "explanation": true }
```

```json
{ "id": "estimates_and_discretion_consideration_payable_for_pricing_adjustments",
  "what_changed": "Management gives the cause of the increase in other current liabilities as mainly higher consideration payable to customers for pricing adjustments. notes:144 states the estimate of consideration payable to customers, including pricing adjustments and returns, at $4.32 billion at September 3, 2026 and $1.19 billion at August 28, 2025. The Q3 10-Q stated $3.32 billion at May 28, 2026 ([0000723125-26-000015:note_history:17]). The input does not say what pricing adjustments are owed to customers in a year the MD&A describes as one of rising prices.",
  "account": "other current liabilities (estimates of consideration payable to customers)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "an increase in other current liabilities resulting mainly from higher consideration payable to customers for pricing adjustments",
  "paragraph_id": "0000723125-26-000023:mdna:92",
  "explanation": true }
```

```json
{ "id": "earnings_quality_accrued_taxes_and_compensation_lift_operating_cash",
  "what_changed": "Part of the operating cash flow increase is credited to higher accounts payable and accrued expenses, mostly income and other taxes and salaries, wages and benefits. This matches the variable-compensation drivers in mdna:50 and mdna:51 and the line items in notes:71.",
  "account": "accounts payable and accrued expenses",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "an increase in accounts payable and accrued expenses mostly related to income and other taxes and salaries, wages, and benefits",
  "paragraph_id": "0000723125-26-000023:mdna:92",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_fifty_three_week_year_not_cited_in_results_prose",
  "what_changed": "New: fiscal 2026 contained 53 weeks, and fiscal 2025 and 2024 contained 52 weeks each; mdna:2 says the same. None of the revenue, margin, expense or cash flow discussion in mdna:17 to mdna:97 names the week count as a factor, and the input does not say which quarter carried the extra week. The prose attaches no effect, so I give no direction.",
  "account": "revenue; cost of goods sold; operating expenses",
  "expected_direction": "insufficient",
  "horizon": "this year (fiscal 2026 as reported)",
  "quote": "Fiscal 2026 contained 53 weeks and fiscal 2025 and 2024 each contained 52 weeks.",
  "paragraph_id": "0000723125-26-000023:notes:17",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_income_tax_disclosure_standard_adopted_prospectively",
  "what_changed": "New: ASU 2023-09 was adopted in the fourth quarter of 2026 on a prospective basis.\n- The rate reconciliation is in the new format for 2026 only (notes:150); 2025 and 2024 stay in the old format (notes:153 and notes:154).\n- A new table of cash paid for income taxes appears (notes:156).\n- New footnotes say Illinois made up most of the 2026 state tax effect in the rate reconciliation (notes:151) and California most of the state cash taxes paid (notes:157).\nThis is a disclosure-only change.",
  "account": "income tax disclosures",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "We adopted this ASU in the fourth quarter of 2026 on a prospective basis.",
  "paragraph_id": "0000723125-26-000023:notes:52",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_government_grants_standard_issued",
  "what_changed": "A newly issued standard is listed: ASU 2025-10 on government grants, effective in the first quarter of 2030 with early adoption permitted. The company does not expect a material effect. The balance it bears on is large: notes:122 says government incentives have reduced property, plant and equipment by $10.93 billion.",
  "account": "property, plant, and equipment; government incentive balances",
  "expected_direction": "none",
  "horizon": "first quarter of 2030 or earlier on early adoption",
  "quote": "In December 2025, the FASB issued ASU 2025-10 (ASC Topic 832), Accounting for Government Grants Received by Business Entities.",
  "paragraph_id": "0000723125-26-000023:notes:52",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_non_marketable_equity_investments_in_ai_companies",
  "what_changed": "The note describes non-marketable equity investments as primarily held in AI and technology companies. It states them at $1.30 billion at September 3, 2026 and $194 million at August 28, 2025, inside other noncurrent assets. mdna:94 gives $1.05 billion of purchases of non-marketable equity securities in 2026. The text does not say whether any investee is a customer or a party to a strategic customer agreement.",
  "account": "other noncurrent assets (non-marketable equity investments)",
  "expected_direction": "up",
  "horizon": "this year (fiscal 2026 as reported)",
  "quote": "Our non-marketable investments were primarily held in AI and technology companies.",
  "paragraph_id": "0000723125-26-000023:notes:60",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_patent_license_charge_without_note",
  "what_changed": "New: a $500 million patent license charge in 2026 in other operating (income) expense, held outside the segments. The earnings-release reconciliation (8k_2_02:70) places it in the fourth-quarter column. The input carries no commitments-and-contingencies or litigation note, and no prose names the counterparty, says whether the charge settles a dispute, or says whether further royalties are owed.",
  "account": "other operating (income) expense, net",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "the unallocated amounts included $500 million of patent license charges in other operating (income) expense, net in 2026",
  "paragraph_id": "0000723125-26-000023:notes:179",
  "explanation": false }
```

```json
{ "id": "earnings_quality_non_gaap_excludes_patent_license_charge",
  "what_changed": "The earnings release excludes the $500 million patent license charge from non-GAAP operating expenses, operating income and net income (8k_2_02:70). The listed exclusion categories (8k_2_02:75 to 8k_2_02:79) are stock-based compensation, settlements, debt prepayments, restructure and impairments, and tax effects. None names patent license charges, and the release does not say which category this charge falls under. The fiscal 2025 column also shows a $57 million patent license charge excluded.",
  "account": "non-GAAP operating expenses; non-GAAP net income",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Gains and losses from settlements;",
  "paragraph_id": "0000723125-26-000018:8k_2_02:76",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_debt_prepayments_continue_into_final_quarter",
  "what_changed": "The prepayment table adds a July 27, 2026 prepayment of 2031 Notes. notes:73 now lists the 2031 Notes with N/A rates and no carrying amount, and notes:91 shows no notes payable maturing before 2032. Prepayment losses in other non-operating expense are stated as $510 million for 2026; the Q3 10-Q stated $500 million for the first nine months ([0000723125-26-000015:note_history:7]). The earnings-release reconciliation carries its own loss-on-debt-prepayments line, and checking it against this note is for the numbers reader.",
  "account": "debt; other non-operating income (expense)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "In connection with these prepayments, we recognized losses in other non-operating income (expense) of $510 million for 2026.",
  "paragraph_id": "0000723125-26-000023:notes:79",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_revolving_credit_capacity_reduced_per_debt_note",
  "what_changed": "Revolving credit capacity was reduced on May 6, 2026 from $3.50 billion to $2.00 billion, with nothing outstanding; this was first reported in the Q3 10-Q ([0000723125-26-000015:note_history:8]) and is new to the annual report. mdna:67 states $2.00 billion available. The leverage covenant wording in notes:88 is unchanged.",
  "account": "available committed borrowing capacity",
  "expected_direction": "down",
  "horizon": "this year (fiscal 2026 as reported)",
  "quote": "On May 6, 2026, we reduced our borrowing capacity under the Revolving Credit Facility from $3.50 billion to $2.00 billion.",
  "paragraph_id": "0000723125-26-000023:notes:87",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_capital_expenditure_guidance_rising",
  "what_changed": "New guidance: capital expenditures net of government incentives of about $11.5 billion in the first quarter of 2027 and about $25 billion in the first six months of 2027, and higher in the second half of 2027. Also new: $4.18 billion of property, plant and equipment purchase obligations, substantially all expected to be paid within one year.",
  "account": "capital expenditures; property, plant, and equipment",
  "expected_direction": "up",
  "horizon": "next quarter and 12 months",
  "quote": "We estimate capital expenditures for property, plant, and equipment, net of proceeds from government incentives, to be approximately $11.5 billion in the first quarter of 2027, approximately $25 billion in the first six months of 2027, and higher in the second half of 2027.",
  "paragraph_id": "0000723125-26-000023:mdna:69",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_idaho_fab_output_and_second_fab_construction",
  "what_changed": "New dates: first DRAM wafer output from the first Boise fab is projected for mid-calendar 2027. Construction of the second Idaho fab began in 2026, with initial wafer output expected by late calendar 2028.",
  "account": "property, plant, and equipment (construction in progress)",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "Construction activities for the second Idaho fab began in 2026, and we expect initial wafer output by late calendar 2028.",
  "paragraph_id": "0000723125-26-000023:mdna:71",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_new_york_fab_vertical_construction",
  "what_changed": "New: the first New York fab broke ground in January 2026. The first foundation concrete pour in July 2026 is described as the move into vertical construction. Initial wafer output is expected in calendar 2030.",
  "account": "property, plant, and equipment (construction in progress)",
  "expected_direction": "up",
  "horizon": "12 months and beyond",
  "quote": "In July 2026, we achieved the first concrete pour for the foundation of that fab, marking the transition from site preparation into vertical construction.",
  "paragraph_id": "0000723125-26-000023:mdna:72",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_manassas_legacy_dram_production_start",
  "what_changed": "New: first production starts of 1-alpha DDR4 at the Manassas, Virginia fab in 2026, to support legacy-product needs in auto, industrial, medical, aerospace and defense markets. No amount is given.",
  "account": "property, plant, and equipment; AEBU revenue",
  "expected_direction": "insufficient",
  "horizon": "12 months",
  "quote": "which will add to our capability to support the legacy product needs of our customers in auto, industrial, medical, aerospace and defense markets.",
  "paragraph_id": "0000723125-26-000023:mdna:73",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_research_labs_decade_investment_plan",
  "what_changed": "New: Micron Research Labs was announced in August 2026, with a planned investment of about $10 billion over the next decade. The text does not split the plan between expense and capital.",
  "account": "research and development; capital expenditures",
  "expected_direction": "up",
  "horizon": "12 months and the next decade",
  "quote": "supported by a planned investment of approximately $10 billion over the next decade to advance memory, compute and semiconductor manufacturing technologies.",
  "paragraph_id": "0000723125-26-000023:mdna:76",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_india_assembly_facility_ramping",
  "what_changed": "New: the Gujarat, India assembly and test facility began commercial shipments and started ramping production in 2026. notes:135 states the remaining unrecognized Indian incentive commitment for this project at up to about $1.1 billion.",
  "account": "property, plant, and equipment; cost of goods sold",
  "expected_direction": "insufficient",
  "horizon": "12 months",
  "quote": "Our assembly and test facility in Gujarat commenced commercial shipments and started ramping production in 2026",
  "paragraph_id": "0000723125-26-000023:mdna:79",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_hiroshima_cleanroom_construction_started",
  "what_changed": "New: ground was broken in July 2026 on a cleanroom project at Hiroshima for future DRAM transitions including HBM, with initial output expected in late calendar 2028. notes:136 states the remaining unrecognized Japanese incentive commitment at up to about $3.4 billion.",
  "account": "property, plant, and equipment (construction in progress)",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "We broke ground in July 2026 on a new cleanroom project at our Hiroshima manufacturing facility",
  "paragraph_id": "0000723125-26-000023:mdna:80",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_singapore_nand_fab_and_packaging_timeline",
  "what_changed": "New: in January 2026 the company broke ground on an additional advanced wafer fab within its Singapore NAND complex, expected to be operational in the second half of calendar 2028. The HBM advanced packaging facility, where ground was broken in January 2025, is to expand packaging capacity beginning in early calendar 2027.",
  "account": "property, plant, and equipment (construction in progress)",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "In January 2026, we broke ground on an additional advanced wafer fab facility located within our existing NAND manufacturing complex.",
  "paragraph_id": "0000723125-26-000023:mdna:81",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_taiwan_fab_acquired_for_cash",
  "what_changed": "New: in March 2026 the company bought a wafer fab in Tongluo, Taiwan from Powerchip Semiconductor Manufacturing Corporation for $1.80 billion in cash. It is disclosed inside the property, plant and equipment note, and the input has no business-combination note. mdna:82 gives the price as $1.8 billion.",
  "account": "property, plant, and equipment",
  "expected_direction": "up",
  "horizon": "this year (fiscal 2026 as reported)",
  "quote": "In March 2026, we completed the acquisition of a wafer fabrication facility in Tongluo, Miaoli County, Taiwan, from Powerchip Semiconductor Manufacturing Corporation for total cash consideration of $1.80 billion.",
  "paragraph_id": "0000723125-26-000023:notes:68",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_taiwan_second_cleanroom_and_shipment_timing",
  "what_changed": "New: meaningful product shipments from the acquired Tongluo fab are expected from mid-calendar 2027, and construction of a similar-sized second cleanroom has begun at the site.",
  "account": "property, plant, and equipment (construction in progress)",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "Adding to the existing fab, we have begun construction of a similar-sized second cleanroom at this site.",
  "paragraph_id": "0000723125-26-000023:mdna:82",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_chips_investment_credit_rate_increase",
  "what_changed": "The note says the One Big Beautiful Bill Act increased the CHIPS investment tax credit from 25% to 35% on qualified investments, recognized in receivables or other noncurrent assets as investments are made; mdna:75 says the company receives 35%. The input does not date the change and does not carry the prior 10-K, so it cannot show whether this sentence is new to the annual report.",
  "account": "receivables (government incentives); other noncurrent assets; property, plant, and equipment",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "The One Big Beautiful Bill Act increased the investment tax credit from 25% to 35% on qualified investments.",
  "paragraph_id": "0000723125-26-000023:notes:132",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_buyback_authorization_raised",
  "what_changed": "Subsequent event after the September 3, 2026 year end: on October 8, 2026 the Board increased the repurchase authorization to $35.16 billion, effective from December 9, 2026. Repurchases are to follow the CHIPS Act direct funding agreements.\n- notes:130 measures the CHIPS repurchase limits from the December 9, 2024 award date: amounts specified in the agreements for the first two years, then conditions in the final three years that include limits based on free cash flow net of CHIPS grants and dividends.\n- The new authorization starts on December 9, the same day and month as that award date. The input does not say whether its start marks the boundary between the two regimes.\nmdna:85 repeats the authorization.",
  "account": "treasury stock; cash",
  "expected_direction": "up",
  "horizon": "next quarter onward",
  "quote": "on October 8, 2026 our Board of Directors authorized an increase in the maximum amount of discretionary repurchases of our outstanding common stock to be made from December 9, 2026 to $35.16 billion",
  "paragraph_id": "0000723125-26-000023:notes:94",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_share_repurchases_resumed_under_old_authorization",
  "what_changed": "Open-market repurchases restarted under the 2018 authorization: 2.5 million shares for $650 million in 2026, and none in 2025. Cumulative repurchases under that authorization are stated at $7.84 billion. mdna:97 gives the same $650 million.",
  "account": "treasury stock",
  "expected_direction": "up",
  "horizon": "this year (fiscal 2026 as reported)",
  "quote": "We repurchased 2.5 million shares of our common stock for $650 million in 2026. No shares were repurchased in 2025.",
  "paragraph_id": "0000723125-26-000023:notes:94",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_dividend_declared_after_year_end",
  "what_changed": "The note states dividends of $0.115 per share in the first and second quarters of 2026 and $0.15 per share in the third and fourth quarters. As a subsequent event, a $0.15 dividend was declared on September 30, 2026, payable October 29, 2026; mdna:86 and 8k_2_02:23 repeat it. The prose does not characterize the change in rate. The CHIPS agreements permit customary recurring dividends and reasonable ordinary-course increases (notes:130).",
  "account": "dividends; retained earnings; cash",
  "expected_direction": "insufficient",
  "horizon": "next quarter",
  "quote": "We declared and paid dividends of $0.115 per share in the first and second quarters of 2026 and $0.15 per share in the third and fourth quarters of 2026.",
  "paragraph_id": "0000723125-26-000023:notes:96",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_no_ten_percent_customer_despite_strategic_agreements",
  "what_changed": "Concentration disclosure: no customer reached 10% of total revenue in 2026. In 2025 one customer was 17%, mainly in CMBU, and in 2024 one customer was 10%. The same year brought multi-year take-or-pay agreements with a number of customers (mdna:66).",
  "account": "revenue (customer concentration)",
  "expected_direction": "none",
  "horizon": "this year (fiscal 2026 as reported)",
  "quote": "No customer accounted for 10% or more of total revenue in 2026.",
  "paragraph_id": "0000723125-26-000023:notes:186",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_executive_trading_plan_adopted",
  "what_changed": "New: on July 17, 2026 Scott DeBoer, President and Chief Technology and Products Officer, adopted a Rule 10b5-1 plan to sell up to 85,632 shares, with sales permitted from October 16, 2026. The 8-K index shows an item 5.02 filed 2026-08-26 whose body is not in the input, so the input cannot show whether it concerns this officer.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "adopted a Rule 10b5-1 trading arrangement providing for the sale of an aggregate of up to 85,632 shares of our common stock.",
  "paragraph_id": "0000723125-26-000023:notes:193",
  "explanation": false }
```

```json
{ "id": "controls_audit_and_filings_critical_audit_matter_describes_take_or_pay_agreements",
  "what_changed": "The revenue recognition critical audit matter now describes the strategic customer agreements as take-or-pay agreements with binding, contractually enforceable volumes over multi-year terms, and says contracts with only certain customers are short-term. It states total revenue of $133,188 million. The stated basis for the CAM is still a high degree of auditor effort (auditors_report:18), not judgment about the new contract terms. Both opinions are unqualified, and ICFR is reported effective by the auditor and management (item_9a:7).",
  "account": "revenue",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "The Company also has strategic customer agreements structured as take-or-pay agreements, with binding commitments for specific contractually enforceable volumes over the multi-year contract terms.",
  "paragraph_id": "0000723125-26-000023:auditors_report:17",
  "explanation": false }
```

```json
{ "id": "controls_audit_and_filings_critical_audit_matter_procedures_omit_deposits",
  "what_changed": "The listed CAM procedures are reading a sample of customer agreements for relevant terms, testing invoices and credit memos, confirming year-end receivables, and testing distributor price-protection adjustments. None names customer deposits or contract liabilities, letters of credit, remaining performance obligations, or the significant-financing-component judgment. The input does not show whether clause (i) is new.",
  "account": "revenue; receivables; customer contract liabilities",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "(i) reading a sample of customer agreements for relevant contractual terms",
  "paragraph_id": "0000723125-26-000023:auditors_report:19",
  "explanation": false }
```


```json
{ "id": "results_against_expectations_management_expects_stronger_next_year",
  "what_changed": "The CEO says fiscal 2026 was a record and the company expects an even stronger fiscal 2027. He says investment in technology, products and manufacturing is increasing, and that the strategic customer agreements add confidence in the durability of financial performance. The release subheadline (8k_2_02:8) says the company is positioned for a record fiscal 2027.",
  "account": "revenue; net income",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "Micron delivered record fiscal 2026 results, and we expect an even stronger fiscal 2027",
  "paragraph_id": "0000723125-26-000018:8k_2_02:20",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_first_quarter_guidance_levels_in_release",
  "what_changed": "New first-quarter fiscal 2027 guidance: revenue of $61.5 billion ± $1.5 billion; GAAP gross margin of about 85.95%; GAAP operating expenses of about $2.31 billion; GAAP diluted EPS of $37.84 ± $1.00, on about 1.15 billion diluted shares. The prose gives levels only. Comparing them with the quarter just reported is arithmetic and is left to the numbers reader.",
  "account": "revenue; gross margin; operating expenses",
  "expected_direction": "insufficient",
  "horizon": "next quarter",
  "quote": "$61.5 billion ± $1.5 billion",
  "paragraph_id": "0000723125-26-000018:8k_2_02:28",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_socamm_revenue_more_than_doubled",
  "what_changed": "The release says revenue from the server LPDDR SOCAMM portfolio more than doubled sequentially in the fourth quarter of 2026. The notes do not break this product line out.",
  "account": "revenue (product line)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Our industry leading server LPDDR SOCAMM portfolio revenue more than doubled sequentially in the fourth quarter of 2026.",
  "paragraph_id": "0000723125-26-000018:8k_2_02:33",
  "explanation": false }
```

## Paragraphs not made into items

The input carried every paragraph as text, with no `[same as prior period ...]` markers. "Standing" means the paragraph reads as policy or boilerplate, and neither the note history nor the text shows a change. The input does not carry the prior 10-K, so this cannot be confirmed paragraph by paragraph. "Carried" means discussion of a prior year, carried forward.

### 8-K 0000723125-26-000018, item 2.02 exhibit 99.1

- 0000723125-26-000018:8k_2_02:1 — exhibit cover line; formatting
- 0000723125-26-000018:8k_2_02:2 — document label; formatting
- 0000723125-26-000018:8k_2_02:3 — exhibit heading
- 0000723125-26-000018:8k_2_02:4 — release heading
- 0000723125-26-000018:8k_2_02:5 — investor and media contacts; no account bearing
- 0000723125-26-000018:8k_2_02:6 — headline
- 0000723125-26-000018:8k_2_02:7 — headline
- 0000723125-26-000018:8k_2_02:8 — subheadline repeating the record fiscal 2027 claim; taken in the stronger-next-year item
- 0000723125-26-000018:8k_2_02:9 — dateline and period-end date; date only
- 0000723125-26-000018:8k_2_02:10 — heading
- 0000723125-26-000018:8k_2_02:11 — fourth-quarter revenue; amounts only
- 0000723125-26-000018:8k_2_02:12 — fourth-quarter GAAP net income and EPS; amounts only
- 0000723125-26-000018:8k_2_02:13 — fourth-quarter non-GAAP net income and EPS; amounts only
- 0000723125-26-000018:8k_2_02:14 — fourth-quarter operating cash flow; amounts only
- 0000723125-26-000018:8k_2_02:15 — heading
- 0000723125-26-000018:8k_2_02:16 — full-year revenue; amounts only
- 0000723125-26-000018:8k_2_02:17 — full-year GAAP net income; amounts only
- 0000723125-26-000018:8k_2_02:18 — full-year non-GAAP net income; amounts only
- 0000723125-26-000018:8k_2_02:19 — full-year operating cash flow; amounts only
- 0000723125-26-000018:8k_2_02:21 — quarterly results table; amounts only
- 0000723125-26-000018:8k_2_02:22 — annual results table; amounts only
- 0000723125-26-000018:8k_2_02:23 — net capex, adjusted free cash flow, year-end cash figure; amounts only; dividend taken in the dividend item
- 0000723125-26-000018:8k_2_02:24 — business-unit quarterly table; amounts only
- 0000723125-26-000018:8k_2_02:25 — page number
- 0000723125-26-000018:8k_2_02:26 — heading
- 0000723125-26-000018:8k_2_02:27 — guidance lead-in; wording only
- 0000723125-26-000018:8k_2_02:29 — pointer to prepared remarks; wording only
- 0000723125-26-000018:8k_2_02:30 — heading
- 0000723125-26-000018:8k_2_02:31 — product sampling news; no amount or account
- 0000723125-26-000018:8k_2_02:32 — product qualification news; no amount or account
- 0000723125-26-000018:8k_2_02:34 — SSD shipments to customers; no amount or account
- 0000723125-26-000018:8k_2_02:35 — SSD volume ramp; no amount or account
- 0000723125-26-000018:8k_2_02:36 — LPDDR5X shipping; no amount or account
- 0000723125-26-000018:8k_2_02:37 — workstation design wins; no amount or account
- 0000723125-26-000018:8k_2_02:38 — SSD qualifications; no amount or account
- 0000723125-26-000018:8k_2_02:39 — LPDDR6 sampling; no amount or account
- 0000723125-26-000018:8k_2_02:40 — heading
- 0000723125-26-000018:8k_2_02:41 — webcast logistics; date only
- 0000723125-26-000018:8k_2_02:42 — website and social media boilerplate
- 0000723125-26-000018:8k_2_02:43 — heading
- 0000723125-26-000018:8k_2_02:44 — company description; boilerplate
- 0000723125-26-000018:8k_2_02:45 — copyright; boilerplate
- 0000723125-26-000018:8k_2_02:46 — heading
- 0000723125-26-000018:8k_2_02:47 — forward-looking statements; boilerplate
- 0000723125-26-000018:8k_2_02:48 — GAAP definition footnote; boilerplate
- 0000723125-26-000018:8k_2_02:49 — non-GAAP definition footnote; boilerplate
- 0000723125-26-000018:8k_2_02:50 — page number
- 0000723125-26-000018:8k_2_02:51 — heading
- 0000723125-26-000018:8k_2_02:52 — heading
- 0000723125-26-000018:8k_2_02:53 — heading
- 0000723125-26-000018:8k_2_02:54 — heading
- 0000723125-26-000018:8k_2_02:55 — income statement; amounts only; patent charge and interest-expense dash used in items
- 0000723125-26-000018:8k_2_02:56 — heading
- 0000723125-26-000018:8k_2_02:57 — heading
- 0000723125-26-000018:8k_2_02:58 — heading
- 0000723125-26-000018:8k_2_02:59 — heading
- 0000723125-26-000018:8k_2_02:60 — balance sheet; amounts only; new caption taken in the contract-liabilities split item
- 0000723125-26-000018:8k_2_02:61 — page number
- 0000723125-26-000018:8k_2_02:62 — heading
- 0000723125-26-000018:8k_2_02:63 — heading
- 0000723125-26-000018:8k_2_02:64 — heading
- 0000723125-26-000018:8k_2_02:65 — heading
- 0000723125-26-000018:8k_2_02:66 — cash flow statement; amounts only; deposit-proceeds line taken in the across-documents item
- 0000723125-26-000018:8k_2_02:67 — heading
- 0000723125-26-000018:8k_2_02:68 — heading
- 0000723125-26-000018:8k_2_02:69 — heading
- 0000723125-26-000018:8k_2_02:70 — GAAP to non-GAAP reconciliation; amounts only; patent and prepayment lines used in items
- 0000723125-26-000018:8k_2_02:71 — page number
- 0000723125-26-000018:8k_2_02:72 — heading
- 0000723125-26-000018:8k_2_02:73 — adjusted free cash flow reconciliation; amounts only
- 0000723125-26-000018:8k_2_02:74 — non-GAAP rationale; boilerplate
- 0000723125-26-000018:8k_2_02:75 — stock-based compensation exclusion category; standing
- 0000723125-26-000018:8k_2_02:77 — debt prepayment exclusion category; standing
- 0000723125-26-000018:8k_2_02:78 — restructure and impairment exclusion category; standing
- 0000723125-26-000018:8k_2_02:79 — tax-effect exclusion category; standing
- 0000723125-26-000018:8k_2_02:80 — non-GAAP diluted share adjustment; standing
- 0000723125-26-000018:8k_2_02:81 — page number
- 0000723125-26-000018:8k_2_02:82 — heading
- 0000723125-26-000018:8k_2_02:83 — heading
- 0000723125-26-000018:8k_2_02:84 — outlook reconciliation table; amounts only; guidance taken in the guidance item
- 0000723125-26-000018:8k_2_02:85 — outlook adjustment amounts; amounts only
- 0000723125-26-000018:8k_2_02:86 — diluted share basis for guidance; amounts only
- 0000723125-26-000018:8k_2_02:87 — guidance exclusions; boilerplate
- 0000723125-26-000018:8k_2_02:88 — page number

### Auditor's report

- 0000723125-26-000023:auditors_report:1 — heading
- 0000723125-26-000023:auditors_report:2 — addressee
- 0000723125-26-000023:auditors_report:3 — heading
- 0000723125-26-000023:auditors_report:4 — audit scope; dates rolled forward
- 0000723125-26-000023:auditors_report:5 — unqualified opinions on statements and ICFR; dates rolled forward
- 0000723125-26-000023:auditors_report:6 — heading
- 0000723125-26-000023:auditors_report:7 — basis for opinions; boilerplate
- 0000723125-26-000023:auditors_report:8 — PCAOB standards; boilerplate
- 0000723125-26-000023:auditors_report:9 — audit procedures; boilerplate
- 0000723125-26-000023:auditors_report:10 — heading
- 0000723125-26-000023:auditors_report:11 — ICFR definition; boilerplate
- 0000723125-26-000023:auditors_report:12 — page number
- 0000723125-26-000023:auditors_report:13 — inherent limitations; boilerplate
- 0000723125-26-000023:auditors_report:14 — heading
- 0000723125-26-000023:auditors_report:15 — CAM preamble; boilerplate
- 0000723125-26-000023:auditors_report:16 — CAM heading, revenue recognition; topic heading only
- 0000723125-26-000023:auditors_report:18 — CAM principal consideration, auditor effort; standing as far as the input shows
- 0000723125-26-000023:auditors_report:20 — signature
- 0000723125-26-000023:auditors_report:21 — city
- 0000723125-26-000023:auditors_report:22 — report date; date rolled forward
- 0000723125-26-000023:auditors_report:23 — auditor tenure since 1984; standing
- 0000723125-26-000023:auditors_report:24 — page number

### Item 9A

- 0000723125-26-000023:item_9a:1 — heading
- 0000723125-26-000023:item_9a:2 — disclosure controls effective; standing
- 0000723125-26-000023:item_9a:3 — no fourth-quarter ICFR change; standing, quarter rolled forward
- 0000723125-26-000023:item_9a:4 — heading
- 0000723125-26-000023:item_9a:5 — ICFR responsibility; boilerplate
- 0000723125-26-000023:item_9a:6 — inherent limitations; boilerplate
- 0000723125-26-000023:item_9a:7 — ICFR effective with auditor attestation; date rolled forward
- 0000723125-26-000023:item_9a:8 — page number

### MD&A

- 0000723125-26-000023:mdna:1 — heading
- 0000723125-26-000023:mdna:2 — fiscal-year intro; 53-week statement taken in the notes:17 item
- 0000723125-26-000023:mdna:3 — heading
- 0000723125-26-000023:mdna:4 — pointer to Item 1
- 0000723125-26-000023:mdna:5 — heading
- 0000723125-26-000023:mdna:6 — heading
- 0000723125-26-000023:mdna:8 — 2025 versus 2024 industry discussion; carried
- 0000723125-26-000023:mdna:9 — new section heading; content taken in the mdna:10 and mdna:11 items
- 0000723125-26-000023:mdna:12 — page number
- 0000723125-26-000023:mdna:13 — heading
- 0000723125-26-000023:mdna:14 — heading
- 0000723125-26-000023:mdna:15 — consolidated results table; amounts only
- 0000723125-26-000023:mdna:16 — pointer to industry conditions; wording only
- 0000723125-26-000023:mdna:17 — total revenue percentage; summary of the DRAM and NAND driver items
- 0000723125-26-000023:mdna:20 — 2025 versus 2024 revenue; carried
- 0000723125-26-000023:mdna:21 — 2025 DRAM drivers; carried
- 0000723125-26-000023:mdna:22 — 2025 NAND drivers; carried
- 0000723125-26-000023:mdna:24 — 2025 versus 2024 gross margin and 2024 write-down benefit; carried
- 0000723125-26-000023:mdna:25 — heading
- 0000723125-26-000023:mdna:26 — revenue by business unit table; amounts only
- 0000723125-26-000023:mdna:27 — rounding note
- 0000723125-26-000023:mdna:28 — lead-in
- 0000723125-26-000023:mdna:29 — CMBU percentage with the usual price and bit attribution; amounts only
- 0000723125-26-000023:mdna:30 — CDBU percentage with the usual price and bit attribution; amounts only
- 0000723125-26-000023:mdna:32 — AEBU percentage with the usual price and bit attribution; amounts only
- 0000723125-26-000023:mdna:33 — lead-in to prior-year business-unit discussion
- 0000723125-26-000023:mdna:34 — 2025 CMBU revenue; carried
- 0000723125-26-000023:mdna:35 — 2025 CDBU revenue; carried
- 0000723125-26-000023:mdna:36 — 2025 MCBU revenue; carried
- 0000723125-26-000023:mdna:37 — 2025 AEBU revenue; carried
- 0000723125-26-000023:mdna:38 — heading
- 0000723125-26-000023:mdna:39 — business-unit operating income table; amounts only
- 0000723125-26-000023:mdna:40 — table note
- 0000723125-26-000023:mdna:41 — 2026 business-unit operating income drivers; MCBU bit exception taken in the MCBU item
- 0000723125-26-000023:mdna:42 — page number
- 0000723125-26-000023:mdna:43 — lead-in to prior-year discussion
- 0000723125-26-000023:mdna:44 — 2025 CMBU operating income; carried
- 0000723125-26-000023:mdna:45 — 2025 CDBU operating income; carried
- 0000723125-26-000023:mdna:46 — 2025 MCBU operating income; carried
- 0000723125-26-000023:mdna:47 — 2025 AEBU operating income; carried
- 0000723125-26-000023:mdna:48 — heading
- 0000723125-26-000023:mdna:49 — R&D description; standing
- 0000723125-26-000023:mdna:53 — lead-in
- 0000723125-26-000023:mdna:54 — tax rate table; amounts only
- 0000723125-26-000023:mdna:56 — Singapore net incentive benefit; same content as the notes:158 item
- 0000723125-26-000023:mdna:57 — tax reform monitoring; boilerplate
- 0000723125-26-000023:mdna:58 — pointer lead-in
- 0000723125-26-000023:mdna:59 — note pointer
- 0000723125-26-000023:mdna:60 — note pointer
- 0000723125-26-000023:mdna:61 — note pointer
- 0000723125-26-000023:mdna:62 — note pointer
- 0000723125-26-000023:mdna:63 — heading
- 0000723125-26-000023:mdna:65 — cash and investment balances, investment policy, foreign-held amount; amounts only
- 0000723125-26-000023:mdna:67 — revolver availability (taken in the revolver item) and incentive clawback; standing
- 0000723125-26-000023:mdna:68 — page number
- 0000723125-26-000023:mdna:70 — capacity need and CHIPS plan; standing
- 0000723125-26-000023:mdna:74 — CHIPS direct funding history; carried, also in notes:128
- 0000723125-26-000023:mdna:75 — 35% credit (taken in the notes:132 item) and New York term sheet; standing
- 0000723125-26-000023:mdna:77 — page number
- 0000723125-26-000023:mdna:78 — lead-in to non-U.S. investments; standing
- 0000723125-26-000023:mdna:83 — foreign government incentives; standing
- 0000723125-26-000023:mdna:84 — pointer
- 0000723125-26-000023:mdna:85 — repurchase authorization; same content as the notes:94 items
- 0000723125-26-000023:mdna:86 — dividend declaration; same content as the notes:96 item
- 0000723125-26-000023:mdna:87 — sufficiency statement adding customer deposits; same change as the funding-sources item
- 0000723125-26-000023:mdna:88 — page number
- 0000723125-26-000023:mdna:89 — heading
- 0000723125-26-000023:mdna:90 — cash flow summary table; amounts only
- 0000723125-26-000023:mdna:91 — operating cash flow description; standing
- 0000723125-26-000023:mdna:93 — 2025 operating cash flow; carried
- 0000723125-26-000023:mdna:94 — 2026 investing cash flows; amounts only; non-marketable purchases used in the notes:60 item
- 0000723125-26-000023:mdna:95 — 2025 investing; carried
- 0000723125-26-000023:mdna:96 — 2024 investing; carried
- 0000723125-26-000023:mdna:98 — 2025 financing; carried
- 0000723125-26-000023:mdna:99 — 2024 financing; carried
- 0000723125-26-000023:mdna:100 — heading
- 0000723125-26-000023:mdna:101 — critical estimates preamble; standing
- 0000723125-26-000023:mdna:102 — contingencies estimate; standing
- 0000723125-26-000023:mdna:103 — government incentives estimate; standing
- 0000723125-26-000023:mdna:104 — government incentives recognition; standing
- 0000723125-26-000023:mdna:105 — income tax estimate; standing
- 0000723125-26-000023:mdna:106 — page number
- 0000723125-26-000023:mdna:107 — inventory valuation estimate; standing
- 0000723125-26-000023:mdna:108 — inventory unit of account; standing
- 0000723125-26-000023:mdna:109 — property, plant and equipment estimate; standing
- 0000723125-26-000023:mdna:110 — revenue estimate; standing, does not mention strategic customer agreements
- 0000723125-26-000023:mdna:111 — heading
- 0000723125-26-000023:mdna:112 — pointer
- 0000723125-26-000023:mdna:113 — heading
- 0000723125-26-000023:mdna:114 — pointer
- 0000723125-26-000023:mdna:115 — page number

### Notes

- 0000723125-26-000023:notes:1 — heading
- 0000723125-26-000023:notes:2 — proxy incorporation; date rolled forward
- 0000723125-26-000023:notes:3 — cybersecurity process; standing
- 0000723125-26-000023:notes:4 — cybersecurity process continued; standing
- 0000723125-26-000023:notes:5 — risk assessments; standing
- 0000723125-26-000023:notes:6 — safeguards; standing
- 0000723125-26-000023:notes:7 — technical controls; standing
- 0000723125-26-000023:notes:8 — third parties and incident materiality; standing
- 0000723125-26-000023:notes:9 — board cybersecurity oversight; standing
- 0000723125-26-000023:notes:10 — officers' years of experience; amounts only
- 0000723125-26-000023:notes:11 — briefing cadence; standing
- 0000723125-26-000023:notes:12 — management role; duplicate standing text
- 0000723125-26-000023:notes:13 — committee process; duplicate standing text
- 0000723125-26-000023:notes:14 — heading
- 0000723125-26-000023:notes:15 — business description; wording only
- 0000723125-26-000023:notes:16 — basis of presentation and reclassification sentence; standing, reclassification bears on the new caption item
- 0000723125-26-000023:notes:18 — heading
- 0000723125-26-000023:notes:19 — derivative uses; standing
- 0000723125-26-000023:notes:20 — derivative accounting; standing
- 0000723125-26-000023:notes:21 — master netting; standing
- 0000723125-26-000023:notes:22 — heading
- 0000723125-26-000023:notes:23 — financial instrument classification; standing
- 0000723125-26-000023:notes:24 — heading
- 0000723125-26-000023:notes:25 — functional currency; standing
- 0000723125-26-000023:notes:26 — heading
- 0000723125-26-000023:notes:27 — goodwill test, no impairment indicators; standing
- 0000723125-26-000023:notes:28 — heading
- 0000723125-26-000023:notes:29 — government incentive policy; standing
- 0000723125-26-000023:notes:30 — heading
- 0000723125-26-000023:notes:31 — inventory policy; standing
- 0000723125-26-000023:notes:32 — heading
- 0000723125-26-000023:notes:33 — lease policy; standing
- 0000723125-26-000023:notes:34 — heading
- 0000723125-26-000023:notes:35 — warranty policy; standing
- 0000723125-26-000023:notes:36 — heading
- 0000723125-26-000023:notes:37 — useful lives; standing, input shows no change
- 0000723125-26-000023:notes:38 — capitalized interest policy; standing
- 0000723125-26-000023:notes:39 — heading
- 0000723125-26-000023:notes:40 — R&D policy; standing
- 0000723125-26-000023:notes:41 — heading
- 0000723125-26-000023:notes:44 — letter-of-credit terms; same terms as the notes:143 item
- 0000723125-26-000023:notes:45 — returns and price protection estimate; standing
- 0000723125-26-000023:notes:46 — heading
- 0000723125-26-000023:notes:47 — stock compensation policy; standing
- 0000723125-26-000023:notes:48 — heading
- 0000723125-26-000023:notes:49 — treasury stock policy; standing
- 0000723125-26-000023:notes:50 — heading
- 0000723125-26-000023:notes:51 — use of estimates; standing
- 0000723125-26-000023:notes:53 — cash and investments lead-in; standing
- 0000723125-26-000023:notes:54 — cash and investments table; amounts only
- 0000723125-26-000023:notes:55 — maturities footnote; standing
- 0000723125-26-000023:notes:56 — Level 1 footnote; standing
- 0000723125-26-000023:notes:57 — Level 2 footnote; date rolled forward
- 0000723125-26-000023:notes:58 — restricted cash footnote; standing
- 0000723125-26-000023:notes:59 — realized gains not material; standing
- 0000723125-26-000023:notes:61 — heading
- 0000723125-26-000023:notes:62 — receivables table; amounts only, cause taken in the receivables explanation item
- 0000723125-26-000023:notes:63 — inventory table; amounts only, no prose
- 0000723125-26-000023:notes:64 — property, plant and equipment table; amounts only
- 0000723125-26-000023:notes:65 — equipment not yet in service; amounts only
- 0000723125-26-000023:notes:66 — construction in progress footnote; standing
- 0000723125-26-000023:notes:67 — finance lease right-of-use carrying value; amounts only
- 0000723125-26-000023:notes:69 — depreciation and capitalized interest; amounts only, used in the interest item
- 0000723125-26-000023:notes:70 — heading
- 0000723125-26-000023:notes:71 — accounts payable and accrued table; amounts only, cause taken in the accrued item
- 0000723125-26-000023:notes:72 — heading
- 0000723125-26-000023:notes:73 — debt table; amounts only, 2031 Notes row used in the prepayment item
- 0000723125-26-000023:notes:74 — ranking and guarantees; standing
- 0000723125-26-000023:notes:75 — fair value of notes; amounts only
- 0000723125-26-000023:notes:76 — heading
- 0000723125-26-000023:notes:77 — lead-in
- 0000723125-26-000023:notes:78 — prepayment table; amounts only, new row taken in the prepayment item
- 0000723125-26-000023:notes:80 — heading
- 0000723125-26-000023:notes:81 — redemption terms; standing
- 0000723125-26-000023:notes:82 — covenants; standing
- 0000723125-26-000023:notes:83 — heading
- 0000723125-26-000023:notes:84 — finance lease description and term; standing
- 0000723125-26-000023:notes:85 — lease SPEs; amounts only
- 0000723125-26-000023:notes:86 — heading
- 0000723125-26-000023:notes:88 — leverage covenant; standing
- 0000723125-26-000023:notes:89 — heading
- 0000723125-26-000023:notes:90 — maturities lead-in; date rolled forward
- 0000723125-26-000023:notes:91 — maturities table; amounts only
- 0000723125-26-000023:notes:92 — purchase obligations; amounts only
- 0000723125-26-000023:notes:93 — heading
- 0000723125-26-000023:notes:95 — heading
- 0000723125-26-000023:notes:97 — heading
- 0000723125-26-000023:notes:98 — derivatives table; amounts only
- 0000723125-26-000023:notes:99 — fair value footnote; standing
- 0000723125-26-000023:notes:100 — assets footnote; standing
- 0000723125-26-000023:notes:101 — liabilities footnote; standing
- 0000723125-26-000023:notes:102 — heading
- 0000723125-26-000023:notes:103 — cash flow hedges; standing
- 0000723125-26-000023:notes:104 — fair value hedges; amounts only
- 0000723125-26-000023:notes:105 — heading
- 0000723125-26-000023:notes:106 — non-designated hedges; standing
- 0000723125-26-000023:notes:107 — derivative gains and losses not material; standing
- 0000723125-26-000023:notes:108 — heading
- 0000723125-26-000023:notes:109 — counterparty risk; standing
- 0000723125-26-000023:notes:110 — shares available for awards; amounts only
- 0000723125-26-000023:notes:111 — heading
- 0000723125-26-000023:notes:112 — award vesting terms; standing, amounts only
- 0000723125-26-000023:notes:113 — lead-in
- 0000723125-26-000023:notes:114 — award activity; amounts only
- 0000723125-26-000023:notes:115 — award summary; amounts only
- 0000723125-26-000023:notes:116 — heading
- 0000723125-26-000023:notes:117 — ESPP; amounts only
- 0000723125-26-000023:notes:118 — heading
- 0000723125-26-000023:notes:119 — stock compensation by caption; amounts only
- 0000723125-26-000023:notes:120 — tax benefits and unrecognized cost; amounts only, date rolled forward
- 0000723125-26-000023:notes:121 — incentive jurisdictions and conditions; standing
- 0000723125-26-000023:notes:122 — incentive reduction of property, plant and equipment; amounts only
- 0000723125-26-000023:notes:123 — operating income benefit from incentives; amounts only
- 0000723125-26-000023:notes:124 — lead-in
- 0000723125-26-000023:notes:125 — incentive balance sheet lines; amounts only
- 0000723125-26-000023:notes:126 — incentive commitments; standing
- 0000723125-26-000023:notes:127 — heading
- 0000723125-26-000023:notes:128 — CHIPS agreements; carried, remaining commitment amount only
- 0000723125-26-000023:notes:129 — milestones and clawbacks; standing
- 0000723125-26-000023:notes:130 — dividend and repurchase restrictions; standing, used in the buyback and dividend items
- 0000723125-26-000023:notes:131 — upside sharing; standing
- 0000723125-26-000023:notes:133 — New York term sheet; standing
- 0000723125-26-000023:notes:134 — heading
- 0000723125-26-000023:notes:135 — India commitment; amounts only
- 0000723125-26-000023:notes:136 — Japan commitment; amounts only
- 0000723125-26-000023:notes:137 — heading
- 0000723125-26-000023:notes:138 — revenue by technology; amounts only
- 0000723125-26-000023:notes:139 — pointer
- 0000723125-26-000023:notes:140 — repeats the notes:42 revenue policy; taken in the revenue policy item
- 0000723125-26-000023:notes:144 — consideration payable estimate; amounts only, cause taken in the mdna:92 explanation item
- 0000723125-26-000023:notes:145 — heading
- 0000723125-26-000023:notes:146 — other operating table; amounts only, patent charge taken in the notes:179 item
- 0000723125-26-000023:notes:147 — heading and lead-in
- 0000723125-26-000023:notes:148 — tax provision table; amounts only
- 0000723125-26-000023:notes:149 — ASU adoption lead-in; taken in the ASU adoption item
- 0000723125-26-000023:notes:150 — new-format rate reconciliation; amounts only, format taken in the ASU item
- 0000723125-26-000023:notes:151 — Illinois footnote; ASU disaggregation, taken in the ASU item
- 0000723125-26-000023:notes:152 — other-category footnote; ASU format
- 0000723125-26-000023:notes:153 — old-format lead-in; ASU format
- 0000723125-26-000023:notes:154 — old-format reconciliation; amounts only
- 0000723125-26-000023:notes:155 — cash taxes lead-in; ASU format
- 0000723125-26-000023:notes:156 — cash taxes paid table; amounts only
- 0000723125-26-000023:notes:157 — California footnote; ASU disaggregation, taken in the ASU item
- 0000723125-26-000023:notes:160 — indefinite reinvestment; standing
- 0000723125-26-000023:notes:161 — deferred tax lead-in; standing
- 0000723125-26-000023:notes:162 — deferred tax table; amounts only
- 0000723125-26-000023:notes:163 — valuation allowance; amounts only
- 0000723125-26-000023:notes:164 — operating loss carryforwards; amounts and expiry years only
- 0000723125-26-000023:notes:165 — tax credit carryforwards; amounts and expiry years only
- 0000723125-26-000023:notes:166 — lead-in
- 0000723125-26-000023:notes:167 — unrecognized tax benefit rollforward; amounts only
- 0000723125-26-000023:notes:168 — unrecognized tax benefits and open years; amounts and years rolled forward, input cannot show whether the IRS audit sentence is new
- 0000723125-26-000023:notes:169 — heading
- 0000723125-26-000023:notes:170 — EPS table; amounts only
- 0000723125-26-000023:notes:171 — lead-in
- 0000723125-26-000023:notes:172 — antidilutive shares; amounts only
- 0000723125-26-000023:notes:173 — segment basis; standing
- 0000723125-26-000023:notes:174 — lead-in
- 0000723125-26-000023:notes:175 — CMBU description; standing
- 0000723125-26-000023:notes:176 — CDBU description; standing, input cannot show whether the NeoCloud wording is new
- 0000723125-26-000023:notes:177 — MCBU description; standing
- 0000723125-26-000023:notes:178 — AEBU description; standing
- 0000723125-26-000023:notes:180 — 2026 segment table; amounts only
- 0000723125-26-000023:notes:181 — 2025 segment table; amounts only
- 0000723125-26-000023:notes:182 — 2024 segment table; amounts only
- 0000723125-26-000023:notes:183 — lead-in
- 0000723125-26-000023:notes:184 — depreciation by segment; amounts only
- 0000723125-26-000023:notes:185 — segment assets and goodwill; standing, amounts only
- 0000723125-26-000023:notes:187 — supplier concentration; standing
- 0000723125-26-000023:notes:188 — credit risk concentration; standing
- 0000723125-26-000023:notes:189 — geographic lead-in
- 0000723125-26-000023:notes:190 — revenue by geography; amounts only
- 0000723125-26-000023:notes:191 — lead-in
- 0000723125-26-000023:notes:192 — long-lived assets by geography; amounts only
