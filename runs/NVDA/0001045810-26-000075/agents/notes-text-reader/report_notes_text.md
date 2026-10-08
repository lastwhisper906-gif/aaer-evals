# Notes-text reader: NVDA 10-Q 0001045810-26-000075 (quarter ended July 26, 2026)

## Scope and input check

- Read in full: input_notes.md, input_notes_history.md (prior 10-Q 0001045810-26-000052 to this filing), input_mdna.md, input_controls.md, input_8k.md (item-code list plus the Item 2.02 body of 0001045810-26-000073) and input_prior_predictions.md.
- Not in the directory: an auditor's report (input_controls.md has only Item 4), an Item 1A diff, an Exhibit 21 diff and any Exhibit 10. No items could come from these.
- Nothing forbidden is in the directory. The financial statement tables inside the 8-K Item 2.02 press release are part of the 8-K body. There is no trend table, no prices, no returns, no short interest, no other company's files and no prior probability.
- Prior flags: none on record, so there is nothing to carry forward.
- I did no arithmetic. Where the only way to give a direction would be to compare two figures, `expected_direction` is `insufficient`. Quotes come only from current-filing paragraphs, 8-K paragraphs or the 8-K item-code list. Where the change is a removed sentence, `what_changed` points to the note-history paragraph that holds the prior text.
- The note change history file was used to see what is new. It is not a second list to report, so its paragraphs are not listed below.

## Items

```json
[
  {
    "id": "revenue_recognition_extended_payment_terms_for_investment_grade_customers",
    "what_changed": "The supplemental note now says payment is generally due shortly after delivery. It adds that for investment-grade customer purchases NVIDIA has provided, and may provide, longer terms of 90 days up to one year to help with large data center builds, depending on size. MD&A (mdna:84, mdna:110) links these terms to large multi-quarter agreements and calls them financing arrangements. The note does not say whether a significant financing component is recognized. The prior wording of this paragraph is not in the input.",
    "account": "Accounts receivable, net",
    "expected_direction": "up",
    "horizon": "this quarter and next 12 months",
    "quote": "In certain cases, for investment-grade customer purchases, we have and may in the future provide longer payment terms ranging from 90 days up to one year to assist customers with large data center builds depending on size.",
    "paragraph_id": "0001045810-26-000075:notes:54",
    "explanation": false
  },
  {
    "id": "earnings_quality_receivables_increase_attributed_to_extended_terms",
    "what_changed": "MD&A now says first-half operating cash flow rose on higher revenue, partially offset by an increase in accounts receivable. It attributes that receivables increase to extended payment terms on large multi-quarter agreements with certain investment-grade customers.",
    "account": "Accounts receivable, net; net cash provided by operating activities",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "partially offset by an increase in accounts receivable due to extended payment terms on large multi-quarter agreements with certain investment-grade customers",
    "paragraph_id": "0001045810-26-000075:mdna:84",
    "explanation": true
  },
  {
    "id": "liquidity_and_capital_customer_financing_arrangements_affect_cash_timing",
    "what_changed": "MD&A now calls the extended payment terms 'financing arrangements' with certain investment-grade customers. It says they will continue to affect the timing of operating cash flows, so the prose presents the receivables effect as ongoing rather than a one-quarter event.",
    "account": "Accounts receivable, net; net cash provided by operating activities",
    "expected_direction": "up",
    "horizon": "next quarter and 12 months",
    "quote": "Financing arrangements with certain investment-grade customers, including extended payment terms under large, multi-quarter agreements, will continue to affect the timing of our operating cash flows.",
    "paragraph_id": "0001045810-26-000075:mdna:110",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_further_credit_support_for_customer_buildouts",
    "what_changed": "MD&A now says the company has entered, and may in future enter, into long-term capacity purchase obligations, financial guarantees, other credit support and financing arrangements to support customers' and partners' data center buildouts. This is an open-ended statement of intent, separate from the specific guarantees disclosed in Note 10.",
    "account": "Guarantees and off-balance-sheet credit support",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "including long-term capacity purchase obligations, financial guarantees, and other forms of credit support and financing arrangements",
    "paragraph_id": "0001045810-26-000075:mdna:110",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_supply_and_capacity_commitments_increased",
    "what_changed": "MD&A and Note 10 (notes:99) now say supply and capacity commitments were significantly increased, from $119 billion last quarter to $279 billion as of July 26, 2026, to meet future demand. MD&A (mdna:14) adds that the commitments secure inventory and capacity for the next several years and that the supplier base keeps expanding.",
    "account": "Supply and capacity purchase obligations (off-balance-sheet); inventories",
    "expected_direction": "up",
    "horizon": "next quarter through 12 months; the commitments table schedules amounts from the remainder of fiscal 2027 onward",
    "quote": "We have significantly increased our supply and capacity commitments from $119 billion last quarter to $279 billion as of July 26, 2026 to meet future demand.",
    "paragraph_id": "0001045810-26-000075:mdna:16",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_supply_agreement_cancellability_softened",
    "what_changed": "The prior note (0001045810-26-000052:note_history:29) said that in certain instances these supplier agreements 'are cancellable, able to be rescheduled, or adjustable'. The current note says they 'may be cancelable, rescheduled, or adjustable'. The prior text scheduled payments through fiscal 2031; the current table has a '2032 and thereafter' column. The weaker cancellability wording bears on the judgement behind excess inventory purchase obligation accruals.",
    "account": "Excess inventory purchase obligations; supply commitments",
    "expected_direction": "insufficient",
    "horizon": "12 months",
    "quote": "in certain instances, these agreements may be cancelable, rescheduled, or adjustable for our business needs prior to placing firm orders",
    "paragraph_id": "0001045810-26-000075:notes:99",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_supply_commitments_for_memory_and_manufacturing_facilities",
    "what_changed": "The note now says the supply commitments are primarily for memory and manufacturing facilities, to meet long-term demand across current and future architectures. The prior text said they reflected data center-scale production and longer ordering horizons, and did not name memory or facilities.",
    "account": "Supply commitments; inventories",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "These supply commitments are for our data center infrastructure systems, primarily memory and manufacturing facilities, to produce our products for long-term demand across current and future product architectures.",
    "paragraph_id": "0001045810-26-000075:notes:99",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_commitments_note_recast_into_categories",
    "what_changed": "The commitments note has been rebuilt. One table by fiscal year now covers supply and capacity, cloud service agreements, data center leases not commenced, equity investments and capital expenditures. A separate 'Additional Commitments' table covers AI cloud agreements and data center leases for third parties, and a 'Guarantees' section follows. The prior 'Other vendor commitments' sentence is gone (0001045810-26-000052:note_history:31), and equity investment commitments have moved here from the investments note (0001045810-26-000052:note_history:74). The two tables show separate totals.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "We entered into strategic commitments across our supply, infrastructure, and partner ecosystems to capitalize on future growth opportunities and support our business.",
    "paragraph_id": "0001045810-26-000075:notes:96",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_cloud_service_reduction_language_removed",
    "what_changed": "The prior note said 'Cloud service capacity may be reduced or terminated' and gave a year-by-year schedule (0001045810-26-000052:note_history:30). The current description drops that sentence. It instead ties the commitments to R&D on open models (Nemotron, Cosmos, GR00T) and autonomous vehicle software. The note no longer says whether capacity can be reduced.",
    "account": "Cloud service agreement commitments; research and development expense",
    "expected_direction": "insufficient",
    "horizon": "12 months",
    "quote": "These commitments provide the cloud infrastructure to support our research and development of our open models, such as NVIDIA Nemotron, Cosmos, and GR00T, and our autonomous vehicle software.",
    "paragraph_id": "0001045810-26-000075:notes:100",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_own_use_data_center_leases_not_commenced",
    "what_changed": "New commitment category: data center leases signed but not yet commenced. They are mainly for engineering, product design and testing. They are expected to start between the third quarter of fiscal 2027 and fiscal 2033, run for up to twenty years, and their start dates depend on construction finishing.",
    "account": "Operating lease assets; operating lease liabilities",
    "expected_direction": "up",
    "horizon": "next quarter onward, through fiscal 2033",
    "quote": "They are expected to begin between the third quarter of fiscal year 2027 and fiscal year 2033 and have terms up to twenty years.",
    "paragraph_id": "0001045810-26-000075:notes:101",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_equity_investment_commitments_timing_and_counterparties",
    "what_changed": "Equity investment commitments now name the counterparties: AI model makers, infrastructure financiers and other private companies. The prior note expected the commitments to be made by the end of fiscal 2027 (0001045810-26-000052:note_history:74). The new table also puts equity investment amounts in the fiscal 2028, 2029 and 2030 columns.",
    "account": "Non-marketable equity securities; equity method investments",
    "expected_direction": "up",
    "horizon": "remainder of fiscal 2027 and later years",
    "quote": "We committed to make certain equity investments in AI model makers, infrastructure financiers, and other private companies, subject to certain contingencies.",
    "paragraph_id": "0001045810-26-000075:notes:102",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_capital_expenditure_commitments_new_category",
    "what_changed": "New category: capital expenditure obligations, mainly data center equipment and infrastructure for engineering and manufacturing. The table shows amounts in the remainder of fiscal 2027 and fiscal 2028 columns.",
    "account": "Property and equipment, net; purchases related to property and equipment",
    "expected_direction": "up",
    "horizon": "next quarter and fiscal 2028",
    "quote": "Our capital expenditures primarily include obligations for data center equipment and infrastructure used for engineering and manufacturing operations.",
    "paragraph_id": "0001045810-26-000075:notes:103",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_ecosystem_equity_investments_scale",
    "what_changed": "MD&A now gives ecosystem equity investments of $99 billion and equity investment commitments of $25 billion as of July 26, 2026, and says the company may keep making them. mdna:107 adds 'We expect to continue investing in our ecosystem'. mdna:85 explains investing cash flow mainly by higher investment purchases.",
    "account": "Marketable equity securities; non-marketable securities; Other income, net",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "These include equity investments of $99 billion and equity investment commitments of $25 billion as of July 26, 2026.",
    "paragraph_id": "0001045810-26-000075:mdna:19",
    "explanation": false
  },
  {
    "id": "revenue_recognition_ai_cloud_procure_and_commit_back_arrangements",
    "what_changed": "New arrangement, introduced in the second quarter (mdna:20). Select AI cloud partners buy NVIDIA data center products, and NVIDIA commits to buy cloud services from them. The AI clouds can stop providing that capacity to NVIDIA and sell it to third parties at better rates. NVIDIA's commitments shrink as third parties or NVIDIA's own R&D use the capacity, and NVIDIA may share in the AI clouds' third-party revenue if criteria are met. The notes do not say how the product sale and the purchase commitment are assessed together for revenue (for example, as consideration payable to a customer). They also do not say how much of the quarter's revenue came from these partners.",
    "account": "Revenue (AI Clouds, Industrial, & Enterprise); cloud service commitments",
    "expected_direction": "up",
    "horizon": "this quarter and 12 months",
    "quote": "Under these agreements, AI clouds procure our data center infrastructure products and we commit to cloud service agreements, which the AI clouds can unilaterally stop providing to us and sell to third-party customers at more advantageous rates.",
    "paragraph_id": "0001045810-26-000075:notes:108",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_ai_cloud_service_commitments_to_partners",
    "what_changed": "MD&A says the AI cloud commitments usually run six years and totaled $36 billion as of July 26, 2026. It adds that a change in market conditions may hurt results. In Note 10 these commitments sit in the separate 'Additional Commitments' table, with no amount for the rest of fiscal 2027 and amounts from fiscal 2028 onward.",
    "account": "Off-balance-sheet commitments; research and development expense",
    "expected_direction": "up",
    "horizon": "fiscal 2028 onward",
    "quote": "Our commitments, which are typically six years in duration, totaled $36 billion as of July 26, 2026, and decrease as capacity is used by third-party customers or by us for our research and development efforts.",
    "paragraph_id": "0001045810-26-000075:mdna:20",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_third_party_data_center_leases_to_reassign",
    "what_changed": "New: NVIDIA has itself signed data center leases of about fifteen years, expected to start between fiscal 2028 and fiscal 2029, which it expects to reassign to third parties. They appear in the 'Additional Commitments' table. The note does not say whether NVIDIA stays liable after reassignment, or what happens if the leases are not reassigned.",
    "account": "Operating lease liabilities; commitments",
    "expected_direction": "insufficient",
    "horizon": "fiscal 2028 to fiscal 2029",
    "quote": "We expect to reassign these data center leases to third parties.",
    "paragraph_id": "0001045810-26-000075:notes:110",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_sb_energy_openai_lease_guarantees",
    "what_changed": "Subsequent event, signed in August 2026 after quarter end. NVIDIA gave guarantees capped at $105 billion as credit support for SB Energy affiliates' land, power and shell buildout, on behalf of an OpenAI affiliate. They cover leases for about 4.25 gigawatts at the PORTS campus in Pike County, Ohio. Each guarantee starts when its lease commences and grows as each of nine phases is completed; the first phase is expected in fiscal 2029. Payment is triggered by certain tenant defaults, and exposure is expected to fall over each 20-year lease. The guarantees end if OpenAI reaches a satisfactory credit rating. In exchange, the site will host only NVIDIA infrastructure. MD&A (mdna:18) adds that the cap is subject to conditions, including the lessor meeting ready-for-service conditions. The note does not say how the guarantees will be accounted for. The existing AI cloud guarantees are carried as credit derivatives (notes:83).",
    "account": "Guarantee obligations (off-balance-sheet); possible guarantee or derivative liability",
    "expected_direction": "up",
    "horizon": "fiscal 2029 onward; signed after the balance sheet date",
    "quote": "In August 2026, we entered into guarantees, capped at a total of $105 billion, to provide credit support on a land, power, and shell buildout with affiliates of SB Energy Corp. (SB Energy) on behalf of a customer, an affiliate of OpenAI Group PBC (OpenAI)",
    "paragraph_id": "0001045810-26-000075:notes:113",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_sb_energy_additional_capacity_option",
    "what_changed": "New: NVIDIA also holds an option, at its sole discretion, to give more credit support in phases for about 3.8 more gigawatts as the site grows. No cap or amount is given for this option. MD&A (mdna:18) says the same.",
    "account": "Guarantee obligations (off-balance-sheet)",
    "expected_direction": "insufficient",
    "horizon": "12 months and beyond",
    "quote": "We also hold an option, exercisable in our sole discretion, to provide additional credit support in phases for approximately 3.8 additional gigawatts as the site scales.",
    "paragraph_id": "0001045810-26-000075:notes:113",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_land_power_shell_guarantee_fair_value_not_significant",
    "what_changed": "The derivatives note now has a section on land, power and shell guarantees of AI cloud partners' lease obligations. These are classified as credit derivatives, their fair values are called not significant, and changes go to Other income, net. The notional table (notes:86) shows $3.5 billion. A footnote (notes:87) says partners have put $712 million in escrow and exposure falls over five-to-seven-year terms. The fair value conclusion is management's judgement, and the input does not show the inputs behind it. The guarantees already existed at January 25, 2026, per the notional table.",
    "account": "Derivative liabilities; Other income, net",
    "expected_direction": "insufficient",
    "horizon": "12 months",
    "quote": "The guarantees are classified as credit derivatives, the fair values of which were not significant, with changes in fair values recognized in Other income, net.",
    "paragraph_id": "0001045810-26-000075:notes:83",
    "explanation": false
  },
  {
    "id": "revenue_recognition_public_company_warrants_received_benefit_deferred",
    "what_changed": "New: in the second quarter NVIDIA received warrants on publicly traded common stock, with three-to-five-year terms. They are booked as equity derivatives in Other assets, with the matching benefit 'substantially deferred'. Later value changes go to Other income, net. Fair value is a Level 3 measurement of $824 million, and notional is $4.8 billion (notes:86). The note does not say who issued the warrants or what NVIDIA gave for them. It also does not say where or when the deferred benefit will be recognized (revenue, cost reduction or other income).",
    "account": "Other assets; deferred credits; Other income, net",
    "expected_direction": "up",
    "horizon": "this quarter; deferred benefit over future periods",
    "quote": "These warrants are classified as equity derivatives, initially recognized within Other assets, with the corresponding benefit substantially deferred.",
    "paragraph_id": "0001045810-26-000075:notes:84",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_equity_forward_contract_without_description",
    "what_changed": "The derivative notional table adds an 'Equity forward contract' line: $1,000 million at July 26, 2026 and none at January 25, 2026. Nothing in the input describes its counterparty, purpose, settlement or accounting.",
    "account": "Derivatives; Other income, net",
    "expected_direction": "insufficient",
    "horizon": "this quarter",
    "quote": "Equity forward contract",
    "paragraph_id": "0001045810-26-000075:notes:86",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_infrastructure_financier_variable_interest_entities_not_consolidated",
    "what_changed": "Prior text: $1.0 billion of equity-method 'investments in infrastructure funds', with maximum loss exposure of $2.3 billion (0001045810-26-000052:note_history:72). Current text: $3.3 billion of equity-method investments in 'infrastructure financiers'. Those treated as VIEs have maximum loss exposure, including future committed amounts, of $4.7 billion. Management has concluded it is not the primary beneficiary and does not consolidate them, and equity-method income was not significant. The VIE and primary-beneficiary conclusion is new prose. The input does not name the financiers or say whether they finance purchases of NVIDIA products.",
    "account": "Equity method investments; Other income, net",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "We have determined we are not the primary beneficiary of our VIE investments and, therefore, do not consolidate the VIEs in our consolidated financial statements.",
    "paragraph_id": "0001045810-26-000075:notes:52",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_private_company_valuation_inputs",
    "what_changed": "The note says privately held investments are valued using observable comparable transactions and other inputs, including volatility, expected time to liquidity, the risk-free rate and security-specific rights. The roll-forward (notes:47) shows unrealized gains on these securities in the quarter. The input does not show whether this sentence is new.",
    "account": "Non-marketable equity securities; Other income, net",
    "expected_direction": "insufficient",
    "horizon": "this quarter",
    "quote": "We value investments using observable comparable transactions and other inputs including volatility, expected time to liquidity, the risk-free rate, and security-specific rights and obligations.",
    "paragraph_id": "0001045810-26-000075:notes:45",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_level_two_unregistered_warrants",
    "what_changed": "Footnote (3) to the holdings table now says the Level 2 publicly held equity securities include 'unregistered' warrants and convertible preferred stock. The prior footnote said only 'warrants' (0001045810-26-000052:note_history:46).",
    "account": "Marketable equity securities (Level 2)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Included investments in unregistered warrants and preferred stock convertible to common stock in public companies.",
    "paragraph_id": "0001045810-26-000075:notes:38",
    "explanation": false
  },
  {
    "id": "across_documents_marketable_equity_liquidity_versus_lockups",
    "what_changed": "MD&A lists marketable equity securities as a primary source of liquidity and cites $42.8 billion of them. The notes say the publicly held equity holdings 'Included $36.9 billion of investments that are subject to short-term lock-up restrictions on the ability to sell' (notes:36). They also say Level 2 holdings include unregistered warrants and convertible preferred stock (notes:38). The supervisor should work out how much of the MD&A liquidity figure can actually be sold.",
    "account": "Marketable equity securities; liquidity",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "As of July 26, 2026, we had $56.6 billion in cash, cash equivalents, and marketable debt securities as well as $42.8 billion of marketable equity securities.",
    "paragraph_id": "0001045810-26-000075:mdna:88",
    "explanation": false
  },
  {
    "id": "earnings_quality_other_income_driven_by_unrealized_equity_gains",
    "what_changed": "MD&A says the equity securities gains in Other income, net came mainly from unrealized gains. notes:39 gives net unrealized gains on public holdings for the quarter and the half, and notes:47 shows unrealized gains on private holdings. The release's non-GAAP measures leave these gains out (8k_2_02:57). The prose ties part of GAAP net income to unrealized mark-to-market gains.",
    "account": "Other income, net; net income",
    "expected_direction": "insufficient",
    "horizon": "next quarter",
    "quote": "Gains from equity securities, net, were primarily driven by unrealized gains in equity securities.",
    "paragraph_id": "0001045810-26-000075:mdna:73",
    "explanation": false
  },
  {
    "id": "earnings_quality_non_gaap_excludes_equity_derivative_and_equity_method_results",
    "what_changed": "The release's non-GAAP 'Other (B)' adjustment excludes four things: gains or losses on equity derivatives, interest expense on acquisition consideration discount to be paid later, the share of equity-method earnings or losses, and dividend income on equity securities. The 10-Q discloses equity derivatives (warrants, an equity forward) and infrastructure-financier equity-method investments for the first time this quarter, so this exclusion now covers them. The prior release is not in the input, so I cannot tell whether the definition is new. The release's own text dates its stock-based compensation change to the first quarter of fiscal 2027.",
    "account": "Non-GAAP other income, net; non-GAAP net income",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Comprised of net (gains)/losses on equity derivatives, interest expense related to acquisition consideration discount to be paid in the future, share of net (earnings)/losses related to equity method investments, and dividend income on equity securities.",
    "paragraph_id": "0001045810-26-000073:8k_2_02:75",
    "explanation": false
  },
  {
    "id": "earnings_quality_groq_license_consideration_paid_in_financing",
    "what_changed": "MD&A now names a payment related to Groq, Inc. among financing outflows. The notes say the accrued purchase consideration relates to the Groq non-exclusive license agreement (notes:63). The release's cash flow statement shows a Groq, Inc. line under financing (8k_2_02:72). Its free cash flow definition deducts only purchases of, and principal payments on, property, equipment and intangibles. Release footnote (B) mentions interest expense on acquisition consideration discount. Putting license consideration in financing keeps it out of operating and investing cash flow, and so out of free cash flow as defined.",
    "account": "Accrued purchase consideration; financing cash flows; free cash flow",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "mainly due to higher share repurchases, dividends, and a payment related to Groq, Inc. in the first half of fiscal year 2027, offset by higher cash proceeds from debt issuance",
    "paragraph_id": "0001045810-26-000075:mdna:86",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_senior_unsecured_notes_issued",
    "what_changed": "New prose: $25.0 billion of senior unsecured notes were issued in June 2026 in seven tranches for general corporate purposes. The debt table adds seven new notes due from 2028 to 2056. mdna:100 repeats the sentence.",
    "account": "Long-term debt; interest expense",
    "expected_direction": "up",
    "horizon": "this quarter and next quarter",
    "quote": "In June 2026, we issued an aggregate of $25.0 billion of senior unsecured notes across seven tranches for general corporate purposes.",
    "paragraph_id": "0001045810-26-000075:notes:90",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_covenant_non_financial_description_removed",
    "what_changed": "The prior note said NVIDIA complied with required covenants 'which are non-financial in nature' (0001045810-26-000052:note_history:40). The current sentence drops that description, in the quarter seven new tranches were issued. The input does not say whether the new notes carry financial covenants.",
    "account": "Long-term debt",
    "expected_direction": "insufficient",
    "horizon": "12 months",
    "quote": "As of July 26, 2026, we complied with the required covenants under the outstanding notes.",
    "paragraph_id": "0001045810-26-000075:notes:93",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_federal_tax_payment_timing",
    "what_changed": "New sentence: two federal income tax payments were made in the second quarter, 'as compared with' no estimated tax payments in the first quarter. The same paragraph says about $1.7 billion of foreign-held cash has no accrual for the foreign or state taxes that repatriation would trigger.",
    "account": "Taxes payable; net cash provided by operating activities",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "We made two federal income tax payments in the second quarter of fiscal year 2027, as compared with no estimated tax payments in the first quarter of fiscal year 2027.",
    "paragraph_id": "0001045810-26-000075:mdna:91",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_quarterly_dividend_rate_raised",
    "what_changed": "MD&A and the notes (notes:137) say the quarterly dividend was raised on May 18, 2026, from $0.01 to $0.25 per share. Dividends paid in the second quarter are given as $6.0 billion. The release sets the next $0.25 payment for October 1, 2026 (8k_2_02:9).",
    "account": "Dividends paid; financing cash flows",
    "expected_direction": "up",
    "horizon": "this quarter and onward",
    "quote": "On May 18, 2026, we increased our quarterly cash dividend from $0.01 per share to $0.25 per share.",
    "paragraph_id": "0001045810-26-000075:mdna:96",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_debt_portfolio_government_only",
    "what_changed": "MD&A now says marketable securities are publicly held equities plus debt issued by the U.S. government and its agencies. The July 26 holdings table (notes:35) has no rows for corporate debt, certificates of deposit or foreign government bonds. Those rows appear in the January 25 table (notes:40) and in the prior quarter's table (0001045810-26-000052:note_history:43).",
    "account": "Marketable debt securities; interest income",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Our marketable securities as of July 26, 2026, consist of publicly-held equity securities and debt securities issued by the U.S. government and its agencies.",
    "paragraph_id": "0001045810-26-000075:mdna:89",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_current_supply_constraints",
    "what_changed": "MD&A now says the company will ship both Blackwell and Rubin systems, is currently facing certain supply constraints, and that its demand estimates can be inaccurate.",
    "account": "Revenue; inventories",
    "expected_direction": "insufficient",
    "horizon": "next quarter",
    "quote": "We will be shipping both Blackwell and Rubin systems in the future and are currently experiencing certain supply constraints.",
    "paragraph_id": "0001045810-26-000075:mdna:14",
    "explanation": false
  },
  {
    "id": "results_against_expectations_vera_rubin_production_shipments_begun",
    "what_changed": "MD&A says Vera Rubin production shipments began in the third quarter of fiscal 2027, after the balance sheet date. The release says Vera Rubin is in full production, with racks running at named partners (8k_2_02:22). The same MD&A passage says the scale and complexity of production 'has caused and could in the future cause' delays, quality issues, higher inventory provisions, lower yields, higher material costs and higher warranty costs (mdna:14, mdna:16). The release gives gross margin guidance for next quarter (8k_2_02:16).",
    "account": "Inventories; inventory provisions; product warranty; cost of revenue",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "Our next-generation Data Center architecture, Vera Rubin, began production shipments in the third quarter of fiscal year 2027.",
    "paragraph_id": "0001045810-26-000075:mdna:14",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_customers_lack_investment_grade_financing",
    "what_changed": "MD&A now makes several statements. AI clouds and AI model makers currently cannot secure long-term infrastructure contracts or investment-grade financing. Less-capitalized companies have limited access to capital. NVIDIA is securing, and guaranteeing, land, power, shell and capacity for select customers. It expects large CSPs and investment-grade enterprises to secure these on their own. These commitments and guarantees depend on how customers and partners perform (also notes:105). mdna:16 adds that customers may delay purchases because of capital constraints.",
    "account": "Guarantees and commitments; revenue from less-capitalized customers",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "We believe AI clouds and AI model makers have significant demand for training and inference compute and currently lack the ability to secure long-term infrastructure contracts and investment-grade financing capacity to secure the AI infrastructure necessary to grow.",
    "paragraph_id": "0001045810-26-000075:mdna:17",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_financing_platform_residual_value_support",
    "what_changed": "New subsequent event, August 2026. NVIDIA signed memorandums of understanding with several large capital providers to set up independent financing platforms meant to raise more than $500 billion of third-party capital. These may not lead to definitive agreements. The capital providers are to underwrite and provide the funding, but NVIDIA may, at its option, give limited residual-value support for parts of specific projects.",
    "account": "Contingent obligations (residual-value support)",
    "expected_direction": "insufficient",
    "horizon": "12 months",
    "quote": "At our option, we may provide limited residual-value support for a portion of specific projects, subject to disciplined risk management and project-by-project evaluation.",
    "paragraph_id": "0001045810-26-000075:mdna:21",
    "explanation": false
  },
  {
    "id": "across_documents_release_describes_sb_energy_as_partnership",
    "what_changed": "The release describes SB Energy as a partnership that secured land, power and shell capacity to host NVIDIA compute. It does not mention the guarantees, the $105 billion cap, or that the leases are to an OpenAI affiliate. The 10-Q discloses all three (notes:113, mdna:18).",
    "account": "Guarantees",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Secured land, power and shell capacity through a partnership with SB Energy at the PORTS-Pike Technology Campus in Ohio to host NVIDIA compute.",
    "paragraph_id": "0001045810-26-000073:8k_2_02:30",
    "explanation": false
  },
  {
    "id": "across_documents_release_financing_platforms_omit_residual_value_support",
    "what_changed": "The release names six capital providers and calls the arrangements strategic partnerships. The 10-Q calls them memorandums of understanding that may not lead to definitive agreements, and says NVIDIA may give limited residual-value support (mdna:21). The release does not mention residual-value support.",
    "account": "Contingent obligations",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Announced strategic partnerships to establish independent compute financing platforms with Apollo, BlackRock, Blackstone, Brookfield, Goldman Sachs and KKR to mobilize over $500 billion of third-party capital for the buildout of AI infrastructure over time, subject to definitive agreements.",
    "paragraph_id": "0001045810-26-000073:8k_2_02:28",
    "explanation": false
  },
  {
    "id": "across_documents_openai_guarantee_and_unnamed_indirect_customer",
    "what_changed": "MD&A says one AI research and deployment company provided a meaningful amount of revenue by buying cloud services from NVIDIA's customers. Note 10 names an OpenAI affiliate as the customer behind the SB Energy guarantees, capped at $105 billion. The filing does not say whether these are the same company. The CEO's quote in the release says 'This time last year, one lab alone was driving the buildout' (8k_2_02:7). The supervisor should consider combined revenue and guarantee exposure to a single counterparty.",
    "account": "Revenue concentration; guarantees",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "We estimate that one AI research and deployment company contributed a meaningful amount of our revenue by purchasing cloud services from our customers in the second quarter and first half of fiscal year 2027.",
    "paragraph_id": "0001045810-26-000075:mdna:60",
    "explanation": false
  },
  {
    "id": "across_documents_acie_growth_and_ai_cloud_commitments",
    "what_changed": "MD&A attributes part of ACIE growth to 'hyperscalers utilizing AI clouds'. In the same quarter, NVIDIA introduced arrangements under which AI clouds buy its products and NVIDIA commits to buy their cloud services (notes:108, mdna:20). The filing does not say how much ACIE revenue came from AI clouds under those arrangements.",
    "account": "Revenue (AI Clouds, Industrial, & Enterprise)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "ACIE revenue increased 138% from a year ago and 25% sequentially driven by end-demand from AI natives, enterprises, and sovereign customers, as well as hyperscalers utilizing AI clouds.",
    "paragraph_id": "0001045810-26-000075:mdna:36",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_customer_reclassified_to_hyperscale",
    "what_changed": "New: one company moved from ACIE to Hyperscale because its business model changed, and its prior-period revenue was recast (also notes:155). The prose describes a move between market platforms, so the recast shifts revenue into Hyperscale and out of ACIE in the comparatives.",
    "account": "Hyperscale revenue (recast in) and ACIE revenue (recast out)",
    "expected_direction": "up",
    "horizon": "this quarter (recast comparatives)",
    "quote": "we reclassified a company from ACIE to Hyperscale due to a change in their business model and recast the prior period revenue associated with this company.",
    "paragraph_id": "0001045810-26-000075:mdna:33",
    "explanation": false
  },
  {
    "id": "across_documents_china_headquarters_revenue_versus_minimal_china_shipments",
    "what_changed": "MD&A says Data Center Hopper shipments to China were less than 1% of Data Center revenue this quarter. mdna:24 says licensed H200 shipments were less than 1%. The release outlook assumes no Data Center compute revenue from China (8k_2_02:15). The geographic table, which is based on customer headquarters, shows China (including Hong Kong) revenue of $7,880 million for the quarter (notes:150). notes:149 says headquarters location can differ from end-customer and shipping location. The supervisor should work out what that China line is made of.",
    "account": "Revenue by geography",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Shipments of Data Center Hopper products to China during the second quarter of fiscal year 2027 were less than 1% of Data Center revenue.",
    "paragraph_id": "0001045810-26-000075:mdna:36",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_licensed_china_hopper_inventory_charge",
    "what_changed": "New: a $0.4 billion charge in the first half of fiscal 2027 for H200 excess inventory and purchase obligations. Management attributes it to falling H200 demand after the PRC government restricted the licensed sales. After the charge, only a fraction of the allowed shipments were made, under 1% of Data Center revenue. Licensed H200s must be inspected in the U.S. and pay a 25% import tariff.",
    "account": "Inventory provisions; excess inventory purchase obligations; cost of revenue",
    "expected_direction": "up",
    "horizon": "this quarter (first half)",
    "quote": "During the first half of fiscal year 2027, we incurred a $0.4 billion charge associated with H200 for excess inventory and purchase obligations, as the demand for H200 products diminished.",
    "paragraph_id": "0001045810-26-000075:mdna:24",
    "explanation": true
  },
  {
    "id": "narrative_signs_of_operating_pressure_china_import_tariff_absorbed",
    "what_changed": "New: H200s shipped under the U.S. licensing program must go through U.S. inspection and pay a 25% import tariff. NVIDIA says it has passed none of that tariff to customers and does not expect to.",
    "account": "Cost of revenue (tariffs); gross margin",
    "expected_direction": "down",
    "horizon": "next quarter, to the extent licensed sales occur",
    "quote": "We have been unable to pass along any of the tariff to our customers, and do not anticipate doing so in the event we are able to sell licensed products into the China market.",
    "paragraph_id": "0001045810-26-000075:mdna:24",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_inventory_provision_releases_from_reserved_sales",
    "what_changed": "MD&A gives inventory and excess purchase obligation provisions of $985 million for the quarter and $2.1 billion for the half. It gives provision releases of $177 million and $280 million, which it attributes to selling previously reserved inventory and settling excess purchase obligations. The net effect on gross margin is unfavorable by 0.8% and 1.0%. The amounts are new for the period; the cause given for the releases is management's explanation.",
    "account": "Inventory reserves; excess inventory purchase obligations; gross margin",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Sales of previously reserved inventory and settlements of excess inventory purchase obligations resulted in a provision release of $177 million and $280 million for the second quarter and first half of fiscal year 2027, respectively.",
    "paragraph_id": "0001045810-26-000075:mdna:65",
    "explanation": true
  },
  {
    "id": "across_documents_research_compute_growth_and_cloud_commitments",
    "what_changed": "MD&A attributes the R&D increase mainly to compute infrastructure (up 127% for the quarter and 120% for the half) and to compensation; mdna:39 gives the same drivers for operating expenses. Note 10 says cloud service agreements support R&D on open models and autonomous vehicle software, and that AI cloud commitments shrink as NVIDIA uses the capacity for R&D. The release gives next-quarter operating expense guidance (8k_2_02:17).",
    "account": "Research and development expense",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "The increases in research and development expenses for the second quarter and first half of fiscal year 2027 were primarily driven by a 127% and 120% increase in compute infrastructure, respectively",
    "paragraph_id": "0001045810-26-000075:mdna:69",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_consumer_pc_memory_prices",
    "what_changed": "MD&A says Edge Computing growth was partly offset by slower consumer PC sales, held back by high memory and system prices.",
    "account": "Edge Computing revenue; Graphics segment revenue",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "partially offset by slower consumer PC sales that were tempered by elevated memory and systems prices",
    "paragraph_id": "0001045810-26-000075:mdna:37",
    "explanation": false
  },
  {
    "id": "results_against_expectations_revenue_outlook_excluding_china",
    "what_changed": "The release guides next-quarter revenue to $108.0 billion, plus or minus 2%, assuming no Data Center compute revenue from China. Whether that means sequential growth is a comparison for the numbers reader.",
    "account": "Revenue",
    "expected_direction": "insufficient",
    "horizon": "next quarter",
    "quote": "Revenue is expected to be $108.0 billion, plus or minus 2%. NVIDIA is not assuming any Data Center compute revenue from China in its outlook.",
    "paragraph_id": "0001045810-26-000073:8k_2_02:15",
    "explanation": false
  },
  {
    "id": "results_against_expectations_gross_margin_outlook",
    "what_changed": "The release guides next-quarter GAAP and non-GAAP gross margin to 74.0%, plus or minus 50 basis points. The outlook reconciliation (8k_2_02:76) shows no acquisition-related effect. Comparing this with the quarter's reported margin is for the numbers reader.",
    "account": "Gross margin",
    "expected_direction": "insufficient",
    "horizon": "next quarter",
    "quote": "GAAP and non-GAAP gross margins are expected to be 74.0%, plus or minus 50 basis points.",
    "paragraph_id": "0001045810-26-000073:8k_2_02:16",
    "explanation": false
  },
  {
    "id": "results_against_expectations_operating_expense_outlook",
    "what_changed": "The release guides next-quarter GAAP and non-GAAP operating expenses to about $9.2 billion and $9.0 billion. The outlook reconciliation (8k_2_02:76) shows $0.2 billion of acquisition-related and other costs.",
    "account": "Operating expenses",
    "expected_direction": "insufficient",
    "horizon": "next quarter",
    "quote": "GAAP and non-GAAP operating expenses are expected to be approximately $9.2 billion and $9.0 billion, respectively.",
    "paragraph_id": "0001045810-26-000073:8k_2_02:17",
    "explanation": false
  },
  {
    "id": "results_against_expectations_tax_rate_outlook",
    "what_changed": "The release guides full-year fiscal 2027 GAAP and non-GAAP tax rates to between 16.0% and 18.0%, excluding discrete items and material changes in the tax environment.",
    "account": "Income tax expense; effective tax rate",
    "expected_direction": "insufficient",
    "horizon": "12 months (fiscal 2027)",
    "quote": "NVIDIA expects GAAP and non-GAAP tax rates to be between 16.0% and 18.0%, excluding any discrete items",
    "paragraph_id": "0001045810-26-000073:8k_2_02:18",
    "explanation": false
  },
  {
    "id": "earnings_quality_effective_tax_rate_increase_explained",
    "what_changed": "The notes and MD&A (mdna:77) say the effective tax rate rose mainly because tax benefits from stock-based compensation, foreign-derived deduction eligible income and the research credit made up a lower percentage relative to the increase in pre-tax income. The prior tax note is not in the note history, so I cannot tell whether this wording is new.",
    "account": "Income tax expense; effective tax rate",
    "expected_direction": "up",
    "horizon": "this quarter and 12 months",
    "quote": "The effective tax rate increased primarily due to a lower percentage of tax benefits from stock-based compensation, foreign-derived deduction eligible income, and the U.S. federal research tax credit relative to the increase in income before income tax.",
    "paragraph_id": "0001045810-26-000075:notes:130",
    "explanation": false
  },
  {
    "id": "results_against_expectations_ceo_says_demand_accelerating",
    "what_changed": "The CEO's quote says demand is accelerating, that several frontier labs and new AI labs are scaling at the same time, and that Vera Rubin is in full production.",
    "account": "Revenue",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "And demand is accelerating.",
    "paragraph_id": "0001045810-26-000073:8k_2_02:7",
    "explanation": false
  },
  {
    "id": "across_documents_repurchase_authorization_remaining_figures",
    "what_changed": "The release says about $99.0 billion was left under the repurchase authorization at quarter end. The 10-Q says the company was authorized to repurchase up to $99.3 billion as of July 26, 2026 (mdna:94, notes:136). The two documents give different figures for what looks like the same measure; the supervisor should reconcile them.",
    "account": "Share repurchase authorization",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "As of the end of the second quarter, the company had approximately $99.0 billion remaining under its share repurchase authorization.",
    "paragraph_id": "0001045810-26-000073:8k_2_02:8",
    "explanation": false
  },
  {
    "id": "controls_audit_and_filings_erp_phased_upgrade_continuing",
    "what_changed": "Item 4 reports effective disclosure controls and no material change in internal control over financial reporting this quarter. It also says a phased upgrade of the ERP system for core financial systems is continuing and will be evaluated each quarter. Item 4 is carried verbatim, so the input does not show whether this sentence is new.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "are continuing a phased upgrade of our enterprise resource planning, or ERP, system to update our existing core financial systems.",
    "paragraph_id": "0001045810-26-000075:item_4_controls:7",
    "explanation": false
  },
  {
    "id": "controls_audit_and_filings_eight_k_material_agreement_and_direct_obligation",
    "what_changed": "Since the prior 10-Q, an 8-K was filed on 2026-08-17 with item 1.01 (material definitive agreement), item 2.03 (direct financial obligation or off-balance-sheet arrangement) and item 7.01. Its body is not in the input. Its timing matches the August 2026 SB Energy guarantees and capital-provider MOUs in the 10-Q, but the input does not confirm the link. The item-code list has no paragraph id, so the section heading is used instead.",
    "account": "Guarantees; debt or off-balance-sheet obligations",
    "expected_direction": "insufficient",
    "horizon": "this quarter",
    "quote": "2026-08-17 0001045810-26-000069 — 1.01, 2.03, 7.01",
    "paragraph_id": "item codes, every 8-K on or before 2026-08-26",
    "explanation": false
  },
  {
    "id": "controls_audit_and_filings_eight_k_officer_or_director_change",
    "what_changed": "An 8-K with item 5.02 (officer or director departure, appointment or compensation) was filed on 2026-07-02. Its body is not in the input, so the nature of the change is unknown.",
    "account": "none",
    "expected_direction": "insufficient",
    "horizon": "this quarter",
    "quote": "2026-07-02 0001045810-26-000060 — 5.02",
    "paragraph_id": "item codes, every 8-K on or before 2026-08-26",
    "explanation": false
  },
  {
    "id": "controls_audit_and_filings_eight_k_other_events_filed_by_agent",
    "what_changed": "An 8-K with items 8.01 and 9.01 was filed on 2026-06-18 under a filing agent's accession prefix. Its body is not in the input. The 10-Q reports a $25.0 billion notes issuance in June 2026, but the input does not confirm this filing is about it.",
    "account": "Long-term debt",
    "expected_direction": "insufficient",
    "horizon": "this quarter",
    "quote": "2026-06-18 0001193125-26-275783 — 8.01, 9.01",
    "paragraph_id": "item codes, every 8-K on or before 2026-08-26",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_class_action_appeal_petition_sentence_removed",
    "what_changed": "The prior note ended with NVIDIA's April 8, 2026 petition asking the Ninth Circuit for permission to appeal the class certification order under Rule 23(f) (0001045810-26-000052:note_history:26). The current note drops that sentence and says nothing about how the petition turned out. The class certified on March 25, 2026 stands as described, and nothing is accrued (notes:128).",
    "account": "Litigation contingencies",
    "expected_direction": "insufficient",
    "horizon": "12 months",
    "quote": "certified a class of investors consisting of all persons or entities who purchased or otherwise acquired NVIDIA common stock between August 10, 2017, and November 15, 2018, inclusive",
    "paragraph_id": "0001045810-26-000075:notes:123",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_irs_examination_disclosed",
    "what_changed": "MD&A says the IRS is examining fiscal 2023 and 2024. The same paragraph gives $5.0 billion of unrecognized tax benefits, including $503 million of interest and penalties, in non-current income tax payable. The input does not show whether the examination sentence is new.",
    "account": "Non-current income tax payable; unrecognized tax benefits",
    "expected_direction": "insufficient",
    "horizon": "12 months",
    "quote": "We are currently under examination by the Internal Revenue Service for our fiscal years 2023 and 2024.",
    "paragraph_id": "0001045810-26-000075:mdna:108",
    "explanation": false
  },
  {
    "id": "across_documents_no_critical_estimate_changes_despite_new_judgments",
    "what_changed": "MD&A says there were no material changes to critical accounting policies and estimates. In the same filing, the notes add several new judgements: Level 3 warrant valuations with a deferred benefit (notes:84), credit-derivative treatment of lease guarantees (notes:83), VIE non-consolidation conclusions (notes:52), and the AI cloud procure-and-commit arrangements (notes:108).",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "There have been no material changes to our Critical Accounting Policies and Estimates.",
    "paragraph_id": "0001045810-26-000075:mdna:43",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_receivables_concentration_five_customers",
    "what_changed": "The note now names five direct customers each holding 10% or more of receivables at July 26, 2026 (22%, 14%, 13%, 11%, 10%). At January 25, 2026 it named three (25%, 18%, 13%). This is the same quarter the extended payment terms for investment-grade customers are disclosed.",
    "account": "Accounts receivable, net",
    "expected_direction": "insufficient",
    "horizon": "this quarter",
    "quote": "Five direct customers accounted for 22%, 14%, 13%, 11%, and 10% of our accounts receivable balance as of July 26, 2026.",
    "paragraph_id": "0001045810-26-000075:notes:53",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_officer_trading_plan_adoptions",
    "what_changed": "Three trading arrangements were adopted this quarter: by director Aarti Shah (6,500 shares), by General Counsel Timothy S. Teter (547,942 shares plus future awards) and by CFO Colette M. Kress (375,439 shares). All expire in 2027. The share counts assume maximum performance-award vesting, before tax withholding (notes:166).",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Executive Vice President and Chief Financial Officer",
    "paragraph_id": "0001045810-26-000075:notes:165",
    "explanation": false
  }
]
```

## Paragraphs carried as text and not made an item

### Item 4 (input_controls.md)
- 0001045810-26-000075:item_4_controls:1: heading
- 0001045810-26-000075:item_4_controls:2: heading
- 0001045810-26-000075:item_4_controls:3: disclosure-controls conclusion; date rolled forward, still 'effective'
- 0001045810-26-000075:item_4_controls:4: heading
- 0001045810-26-000075:item_4_controls:5: 'no changes in ICFR'; quarter rolled forward
- 0001045810-26-000075:item_4_controls:6: page number
- 0001045810-26-000075:item_4_controls:8: heading
- 0001045810-26-000075:item_4_controls:9: inherent-limitations boilerplate

### Auditor's report, Item 1A diff, Exhibit 21 diff, Exhibit 10
- None in the input, so there are no paragraphs.

### 8-K item-code list and late-filing section (no paragraph ids)
- 2026-08-26 0001045810-26-000073 (2.02, 9.01): this release; its paragraphs are listed below
- 2026-06-30 0001045810-26-000056 (5.07): shareholder vote results; body not in input; routine
- 8-K entries dated on or before the prior 10-Q (2026-05-20 and earlier): belong to prior periods
- late-filing notifications: none

### 8-K Item 2.02 body (0001045810-26-000073)
- 0001045810-26-000073:8k_2_02:1: exhibit header
- 0001045810-26-000073:8k_2_02:2: document header
- 0001045810-26-000073:8k_2_02:3: release title
- 0001045810-26-000073:8k_2_02:4: headline revenue; amounts only
- 0001045810-26-000073:8k_2_02:5: headline Data Center revenue; amounts only
- 0001045810-26-000073:8k_2_02:6: quarter results, margins, EPS; amounts only
- 0001045810-26-000073:8k_2_02:9: next dividend at the rate covered in liquidity_and_capital_quarterly_dividend_rate_raised
- 0001045810-26-000073:8k_2_02:10: heading
- 0001045810-26-000073:8k_2_02:11: GAAP summary table; amounts only
- 0001045810-26-000073:8k_2_02:12: non-GAAP summary table; amounts only
- 0001045810-26-000073:8k_2_02:13: heading
- 0001045810-26-000073:8k_2_02:14: outlook lead-in
- 0001045810-26-000073:8k_2_02:19: heading
- 0001045810-26-000073:8k_2_02:20: heading
- 0001045810-26-000073:8k_2_02:21: Data Center revenue; amounts only
- 0001045810-26-000073:8k_2_02:22: Vera Rubin in full production; covered by results_against_expectations_vera_rubin_production_shipments_begun
- 0001045810-26-000073:8k_2_02:23: product announcement (Spectrum-6); no amount, account or commitment
- 0001045810-26-000073:8k_2_02:24: product announcement (Vera CPU)
- 0001045810-26-000073:8k_2_02:25: product announcement (Groq 3 LPX)
- 0001045810-26-000073:8k_2_02:26: product announcement (BlueField-4 STX)
- 0001045810-26-000073:8k_2_02:27: product announcement (DSX platform)
- 0001045810-26-000073:8k_2_02:29: customer deployment announcement (SpaceXAI); no terms
- 0001045810-26-000073:8k_2_02:31: benchmark claim
- 0001045810-26-000073:8k_2_02:32: software and partnership announcement; no terms
- 0001045810-26-000073:8k_2_02:33: continuation of software announcement
- 0001045810-26-000073:8k_2_02:34: software announcement (BioNeMo)
- 0001045810-26-000073:8k_2_02:35: alliance formed; no financial terms
- 0001045810-26-000073:8k_2_02:36: customer-use announcement (Apple); no terms
- 0001045810-26-000073:8k_2_02:37: Korea partnerships; no terms
- 0001045810-26-000073:8k_2_02:38: SK hynix technology partnership; no terms
- 0001045810-26-000073:8k_2_02:39: Japan partnership; no terms
- 0001045810-26-000073:8k_2_02:40: HPC supercomputer announcement
- 0001045810-26-000073:8k_2_02:41: heading
- 0001045810-26-000073:8k_2_02:42: Edge Computing revenue; amounts only
- 0001045810-26-000073:8k_2_02:43: product announcement (RTX Spark)
- 0001045810-26-000073:8k_2_02:44: product announcement (DGX Station)
- 0001045810-26-000073:8k_2_02:45: software initiative
- 0001045810-26-000073:8k_2_02:46: ecosystem collaborations; no terms
- 0001045810-26-000073:8k_2_02:47: model release
- 0001045810-26-000073:8k_2_02:48: model release
- 0001045810-26-000073:8k_2_02:49: reference design announcement
- 0001045810-26-000073:8k_2_02:50: product announcement
- 0001045810-26-000073:8k_2_02:51: software release
- 0001045810-26-000073:8k_2_02:52: heading
- 0001045810-26-000073:8k_2_02:53: pointer to CFO commentary
- 0001045810-26-000073:8k_2_02:54: heading
- 0001045810-26-000073:8k_2_02:55: conference call logistics
- 0001045810-26-000073:8k_2_02:56: heading
- 0001045810-26-000073:8k_2_02:57: non-GAAP definitions; its own text dates the stock-based compensation change to the first quarter of fiscal 2027; the equity exclusions are covered in earnings_quality_non_gaap_excludes_equity_derivative_and_equity_method_results
- 0001045810-26-000073:8k_2_02:58: heading
- 0001045810-26-000073:8k_2_02:59: company boilerplate
- 0001045810-26-000073:8k_2_02:60: separator
- 0001045810-26-000073:8k_2_02:61: contacts lead-in
- 0001045810-26-000073:8k_2_02:62: contacts
- 0001045810-26-000073:8k_2_02:63: forward-looking statements boilerplate (truncated)
- 0001045810-26-000073:8k_2_02:64: trademarks
- 0001045810-26-000073:8k_2_02:65: header
- 0001045810-26-000073:8k_2_02:66: header
- 0001045810-26-000073:8k_2_02:67: header
- 0001045810-26-000073:8k_2_02:68: header
- 0001045810-26-000073:8k_2_02:69: income statement; amounts only
- 0001045810-26-000073:8k_2_02:70: balance sheet; amounts only
- 0001045810-26-000073:8k_2_02:71: cash flow, operating and investing; amounts only
- 0001045810-26-000073:8k_2_02:72: cash flow, financing; amounts only; the Groq line is covered in earnings_quality_groq_license_consideration_paid_in_financing
- 0001045810-26-000073:8k_2_02:73: GAAP to non-GAAP reconciliation; amounts only
- 0001045810-26-000073:8k_2_02:74: free cash flow reconciliation and H20 footnote; amounts only
- 0001045810-26-000073:8k_2_02:76: outlook reconciliation; amounts only, cited in the outlook items

### MD&A (0001045810-26-000075)
- 0001045810-26-000075:mdna:1: heading
- 0001045810-26-000075:mdna:6: cross-reference to risk factors; wording only
- 0001045810-26-000075:mdna:13: revenue growth driver; period rolled forward
- 0001045810-26-000075:mdna:18: SB Energy description; repeats notes:113, covered in the two SB Energy items (ready-for-service condition noted there)
- 0001045810-26-000075:mdna:22: open-source model risk narrative, split differently across the page break; no amount, account or commitment
- 0001045810-26-000075:mdna:23: continuation of mdna:22; same reason
- 0001045810-26-000075:mdna:25: Israel/Middle East disclosure; employee count updated only
- 0001045810-26-000075:mdna:26: macroeconomic boilerplate
- 0001045810-26-000075:mdna:27: cross-reference
- 0001045810-26-000075:mdna:28: heading
- 0001045810-26-000075:mdna:29: quarterly summary table; amounts only
- 0001045810-26-000075:mdna:30: description of platforms; wording only
- 0001045810-26-000075:mdna:31: market platform revenue table; amounts only
- 0001045810-26-000075:mdna:34: page number
- 0001045810-26-000075:mdna:35: revenue; amounts only
- 0001045810-26-000075:mdna:38: gross margin explained by mix; amounts and period rolled
- 0001045810-26-000075:mdna:39: operating expense drivers; covered by across_documents_research_compute_growth_and_cloud_commitments
- 0001045810-26-000075:mdna:41: cross-reference
- 0001045810-26-000075:mdna:46: percentage-of-revenue table; amounts only
- 0001045810-26-000075:mdna:47: heading
- 0001045810-26-000075:mdna:49: segment revenue table; amounts only
- 0001045810-26-000075:mdna:51: segment operating income table; amounts only
- 0001045810-26-000075:mdna:52: Compute & Networking revenue driver; period rolled
- 0001045810-26-000075:mdna:53: Graphics revenue driver; period rolled
- 0001045810-26-000075:mdna:54: segment operating income drivers; period rolled, prior-year H20 charge
- 0001045810-26-000075:mdna:56: customer definitions; wording only
- 0001045810-26-000075:mdna:57: direct customer revenue concentration; amounts only
- 0001045810-26-000075:mdna:58: prior-year concentration; amounts only
- 0001045810-26-000075:mdna:61: geographic share; amounts only
- 0001045810-26-000075:mdna:63: cost-of-revenue composition; definitional, no amount
- 0001045810-26-000075:mdna:64: gross margin against prior year; amounts and mix
- 0001045810-26-000075:mdna:66: prior-year provisions; amounts only
- 0001045810-26-000075:mdna:68: operating expense table; amounts only
- 0001045810-26-000075:mdna:70: SG&A driver; period rolled
- 0001045810-26-000075:mdna:71: heading
- 0001045810-26-000075:mdna:72: other income table; amounts only
- 0001045810-26-000075:mdna:74: cross-reference
- 0001045810-26-000075:mdna:76: tax amounts and rates; amounts only
- 0001045810-26-000075:mdna:77: effective tax rate explanation; repeats notes:130, covered in earnings_quality_effective_tax_rate_increase_explained
- 0001045810-26-000075:mdna:78: rate against statutory rate; period rolled
- 0001045810-26-000075:mdna:81: cash and securities table; amounts only
- 0001045810-26-000075:mdna:82: cash flow summary table; amounts only
- 0001045810-26-000075:mdna:83: fixed-income description; wording, related to liquidity_and_capital_debt_portfolio_government_only
- 0001045810-26-000075:mdna:85: investing cash flow driver; covered by liquidity_and_capital_ecosystem_equity_investments_scale
- 0001045810-26-000075:mdna:90: cash held outside the U.S.; period rolled
- 0001045810-26-000075:mdna:93: repurchases; amounts only
- 0001045810-26-000075:mdna:94: repurchase authorization; amounts only, the figure is used in across_documents_repurchase_authorization_remaining_figures
- 0001045810-26-000075:mdna:97: dividend boilerplate
- 0001045810-26-000075:mdna:98: excise tax; period rolled
- 0001045810-26-000075:mdna:100: notes issuance; repeats notes:90, covered in liquidity_and_capital_senior_unsecured_notes_issued
- 0001045810-26-000075:mdna:101: lead-in
- 0001045810-26-000075:mdna:102: debt maturity table; amounts only
- 0001045810-26-000075:mdna:103: commercial paper program; date rolled
- 0001045810-26-000075:mdna:106: cross-reference to Notes 8, 9, 10 and 14; covered by the commitment and guarantee items
- 0001045810-26-000075:mdna:107: 'continue investing'; covered by liquidity_and_capital_ecosystem_equity_investments_scale
- 0001045810-26-000075:mdna:109: contractual obligations, pointing to Note 10; covered by the commitment items
- 0001045810-26-000075:mdna:111: heading
- 0001045810-26-000075:mdna:112: no new pronouncements adopted

### Notes (0001045810-26-000075)
- 0001045810-26-000075:notes:2: basis of presentation; date rolled
- 0001045810-26-000075:notes:7: fiscal calendar; quarter rolled
- 0001045810-26-000075:notes:12: heading
- 0001045810-26-000075:notes:14: FASB standard; punctuation only
- 0001045810-26-000075:notes:17: stock-based compensation table; amounts only
- 0001045810-26-000075:notes:20: equity award activity table; amounts only
- 0001045810-26-000075:notes:21: unearned stock-based compensation; amounts only
- 0001045810-26-000075:notes:22: EPS lead-in
- 0001045810-26-000075:notes:23: EPS table; amounts only
- 0001045810-26-000075:notes:27: intangibles heading and lead-in
- 0001045810-26-000075:notes:28: intangibles table; amounts only
- 0001045810-26-000075:notes:29: amortization expense; amounts only
- 0001045810-26-000075:notes:30: lead-in
- 0001045810-26-000075:notes:31: future amortization table; amounts only
- 0001045810-26-000075:notes:32: goodwill increase; amounts only, period rolled
- 0001045810-26-000075:notes:33: fair value hierarchy lead-in; wording only
- 0001045810-26-000075:notes:34: lead-in
- 0001045810-26-000075:notes:35: holdings table; amounts only (missing rows covered in liquidity_and_capital_debt_portfolio_government_only)
- 0001045810-26-000075:notes:36: lock-up footnote; amounts only, covered in across_documents_marketable_equity_liquidity_versus_lockups
- 0001045810-26-000075:notes:37: long-term lock-up footnote; amounts only
- 0001045810-26-000075:notes:39: unrealized gains on public equity; amounts only, covered in earnings_quality_other_income_driven_by_unrealized_equity_gains
- 0001045810-26-000075:notes:40: January 25 comparative table; formatting only
- 0001045810-26-000075:notes:41: January 25 lock-up footnote; wording only
- 0001045810-26-000075:notes:42: January 25 long-term lock-up footnote; no change in substance
- 0001045810-26-000075:notes:43: debt securities in continuous loss position; table condensed into a sentence, amounts only
- 0001045810-26-000075:notes:44: debt maturities; table condensed into a sentence, amounts only
- 0001045810-26-000075:notes:46: lead-in
- 0001045810-26-000075:notes:47: privately held securities roll-forward; amounts only
- 0001045810-26-000075:notes:48: footnote; wording only
- 0001045810-26-000075:notes:49: footnote; wording only
- 0001045810-26-000075:notes:50: cumulative gains and impairments; amounts only
- 0001045810-26-000075:notes:51: heading
- 0001045810-26-000075:notes:55: lead-in
- 0001045810-26-000075:notes:56: inventory table; amounts only
- 0001045810-26-000075:notes:57: inventory provisions footnote; amounts only
- 0001045810-26-000075:notes:58: heading
- 0001045810-26-000075:notes:59: property acquired but not paid for; amounts only
- 0001045810-26-000075:notes:60: accrued liabilities table; amounts only
- 0001045810-26-000075:notes:61: deferred revenue and customer advances footnote; amounts only
- 0001045810-26-000075:notes:62: excess purchase obligations footnote; amounts only
- 0001045810-26-000075:notes:63: Groq footnote; covered in earnings_quality_groq_license_consideration_paid_in_financing
- 0001045810-26-000075:notes:64: other long-term liabilities table; amounts only
- 0001045810-26-000075:notes:65: footnote; wording only
- 0001045810-26-000075:notes:66: footnote; wording only
- 0001045810-26-000075:notes:67: heading
- 0001045810-26-000075:notes:68: lead-in
- 0001045810-26-000075:notes:69: deferred revenue roll-forward; amounts only
- 0001045810-26-000075:notes:70: customer advance additions; amounts only
- 0001045810-26-000075:notes:71: customer advances recognized; amounts only
- 0001045810-26-000075:notes:72: revenue from opening deferred revenue; amounts only
- 0001045810-26-000075:notes:73: remaining performance obligations; amounts only
- 0001045810-26-000075:notes:74: heading
- 0001045810-26-000075:notes:75: lead-in
- 0001045810-26-000075:notes:76: other income table; amounts only
- 0001045810-26-000075:notes:78: designated FX hedges; period rolled
- 0001045810-26-000075:notes:79: non-designated FX contracts; date rolled
- 0001045810-26-000075:notes:80: FX contract maturity; date rolled
- 0001045810-26-000075:notes:81: FX gains and losses; period rolled
- 0001045810-26-000075:notes:82: heading
- 0001045810-26-000075:notes:85: lead-in
- 0001045810-26-000075:notes:87: guarantee escrow and terms footnote; amounts only, covered in estimates_and_discretion_land_power_shell_guarantee_fair_value_not_significant
- 0001045810-26-000075:notes:88: heading
- 0001045810-26-000075:notes:89: debt table; amounts only (new tranches covered in liquidity_and_capital_senior_unsecured_notes_issued)
- 0001045810-26-000075:notes:91: debt fair value; amounts only
- 0001045810-26-000075:notes:92: standing terms of the notes
- 0001045810-26-000075:notes:94: commercial paper program; date rolled
- 0001045810-26-000075:notes:95: heading
- 0001045810-26-000075:notes:97: lead-in
- 0001045810-26-000075:notes:98: commitments table; amounts only, structure covered in structure_and_disclosure_changes_commitments_note_recast_into_categories
- 0001045810-26-000075:notes:104: heading
- 0001045810-26-000075:notes:105: land, power and shell framing; repeats mdna:17, covered in narrative_signs_of_operating_pressure_customers_lack_investment_grade_financing
- 0001045810-26-000075:notes:106: heading
- 0001045810-26-000075:notes:107: additional commitments table; amounts only, covered in liquidity_and_capital_ai_cloud_service_commitments_to_partners and the third-party lease item
- 0001045810-26-000075:notes:109: continuation of notes:108; covered in revenue_recognition_ai_cloud_procure_and_commit_back_arrangements
- 0001045810-26-000075:notes:111: heading
- 0001045810-26-000075:notes:112: existing AI cloud guarantees, now also listed in the commitments note; same amount as the derivatives note, covered in the guarantee fair-value item
- 0001045810-26-000075:notes:114: lead-in to guarantee table; covered in the SB Energy guarantee item
- 0001045810-26-000075:notes:115: guarantee exposure table; amounts only, covered in the SB Energy guarantee item
- 0001045810-26-000075:notes:116: heading
- 0001045810-26-000075:notes:117: warranty lead-in; balance sentence removed, amounts only
- 0001045810-26-000075:notes:118: warranty roll-forward; amounts only
- 0001045810-26-000075:notes:119: warranty additions by segment; period rolled
- 0001045810-26-000075:notes:120: indemnities; one word changed (recorded to recognized)
- 0001045810-26-000075:notes:121: heading
- 0001045810-26-000075:notes:122: heading
- 0001045810-26-000075:notes:124: N.D. Cal. derivative suit; no change found
- 0001045810-26-000075:notes:125: Delaware derivative suits; paragraph rejoined, wording only
- 0001045810-26-000075:notes:126: Horanic suit; no change found
- 0001045810-26-000075:notes:127: heading
- 0001045810-26-000075:notes:128: loss contingencies; date rolled
- 0001045810-26-000075:notes:129: tax amounts and rates; amounts only
- 0001045810-26-000075:notes:131: rate against statutory rate; period rolled
- 0001045810-26-000075:notes:132: uncertain tax positions boilerplate
- 0001045810-26-000075:notes:135: repurchases; amounts only
- 0001045810-26-000075:notes:136: repurchase authorization; amounts only, the figure is used in across_documents_repurchase_authorization_remaining_figures
- 0001045810-26-000075:notes:137: dividends; amounts only, the rate change is covered in liquidity_and_capital_quarterly_dividend_rate_raised
- 0001045810-26-000075:notes:138: dividend boilerplate
- 0001045810-26-000075:notes:144: segment table; amounts only
- 0001045810-26-000075:notes:146: segment depreciation and amortization; amounts only
- 0001045810-26-000075:notes:147: lead-in
- 0001045810-26-000075:notes:148: segment reconciliation; amounts only
- 0001045810-26-000075:notes:149: basis for geographic designation; standing text, used in the China revenue item
- 0001045810-26-000075:notes:150: geographic revenue table; amounts only, covered in the China revenue item
- 0001045810-26-000075:notes:151: geographic share; amounts only
- 0001045810-26-000075:notes:152: customer definitions; wording only
- 0001045810-26-000075:notes:153: direct customer revenue concentration; amounts only
- 0001045810-26-000075:notes:154: prior-year concentration; amounts only
- 0001045810-26-000075:notes:155: platform recast; repeats mdna:33, covered in structure_and_disclosure_changes_customer_reclassified_to_hyperscale
- 0001045810-26-000075:notes:156: market platform revenue table; amounts only
- 0001045810-26-000075:notes:159: lead-in
- 0001045810-26-000075:notes:160: lease maturity table; amounts only
- 0001045810-26-000075:notes:161: lease term and discount rate; amounts only
- 0001045810-26-000075:notes:162: lease cost; amounts only
- 0001045810-26-000075:notes:164: supplemental lease cash flows; amounts only
- 0001045810-26-000075:notes:166: trading-plan footnotes; covered in related_parties_contingencies_and_subsequent_events_officer_trading_plan_adoptions
