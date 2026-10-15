<!-- the quote gate removed 1 item(s) from this copy; input_manifest.json lists each with its reason -->
# FLEX 10-Q 0000866374-26-000030 (quarter ended June 26, 2026): notes text reader report

## Inputs

- What I read: input_notes.md, input_notes_history.md (compares 0000866374-26-000005 with 0000866374-26-000030), input_mdna.md, input_controls.md (Item 4 only), input_8k.md (the item-code list and the body of the Item 2.02 release 0000866374-26-000026) and input_prior_predictions.md (none on record).
- Not in my directory: an Item 1A diff, an Exhibit 21 diff, any Exhibit 10, and an auditor's report. This is a 10-Q, so the controls file carries Item 4 only. The 8-K list shows filings whose bodies were not given to me (8.01 on 2026-07-29; 5.02 on 2026-06-12; 1.01/2.03 on 2026-06-02 and 2026-05-04). Items below mark these as insufficient where they matter.
- Forbidden material: none found. I saw no trend table, prices, returns, short interest, other company files, prior probabilities or outcome window. The 8-K schedules are part of the 8-K body.
- I did no arithmetic. Every amount, percentage and direction below is what the prose states.
- Totals: 53 items. 3 are marked `insufficient`. 4 carry `explanation: true`.

## Items

```json
{ "id": "structure_and_disclosure_changes_three_segment_recast",
  "what_changed": "The business description now says Flex has three operating and reportable segments: Integrated Technology Solutions (Communications; Lifestyle), Regulated Manufacturing Solutions (Industrial; Automotive; Healthcare) and Cloud and Power Infrastructure (Cloud and Cooling; Power). The prior period described two segments (Flex Agility Solutions and Flex Reliability Solutions). The capabilities sentence now ends 'plus a portfolio of power and cooling products' where it used to say 'post-production and post-sale services, and proprietary products'. A sentence on scale across technology-driven and regulated markets is added. The MD&A overview (mdna:4 to mdna:14) and the segment note (notes:128) carry the same three-segment structure.",
  "account": "segment net sales; segment income",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "As of June 26, 2026, Flex's three operating and reportable segments are as follows:",
  "paragraph_id": "0000866374-26-000030:notes:2",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "structure_and_disclosure_changes_consumer_devices_end_market_dropped",
  "what_changed": "The prior FAS end-market list included 'Consumer Devices, including mobile and high velocity consumer devices'. The new segment bullets name no consumer devices end market, and Lifestyle is now described as 'premium products across commercial, home and personal product categories'. The prior Industrial bullet's wording 'renewables, critical power, and embedded power' is also gone; power is now described under CPI. The text does not say where former consumer devices revenue is now reported.",
  "account": "segment net sales",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Consumer Devices, including mobile and high velocity consumer devices",
  "paragraph_id": "0000866374-26-000005:note_history:20",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "articulation_and_the_filed_history_prior_year_segment_figures_recast",
  "what_changed": "The segment note now says the prior-year quarter's segment information has been recast to the three new segments, both in the note and in MD&A. The prior-year segment net sales, segment income and segment margins shown are therefore recast figures, not the ones originally filed under FAS and FRS.",
  "account": "segment net sales; segment income",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "has been recast to reflect the operating and reportable segments in the table below and in Item 2",
  "paragraph_id": "0000866374-26-000030:notes:131",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "structure_and_disclosure_changes_cpi_spin_off_announced",
  "what_changed": "New paragraph. On May 5, 2026 Flex announced it intends to separate the CPI segment into an independent publicly traded company (SpinCo). Completion is expected in the first quarter of calendar 2027 and needs approval from the Board, shareholders and the High Court of Singapore, plus SEC effectiveness of SpinCo's Form 10. After the spin Flex would consist of ITS and RMS. The text says there is no assurance the transaction will occur, or of its terms or timing.",
  "account": "segment net sales (CPI); selling, general and administrative expenses",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "The spin-off of CPI from Flex is expected to be completed in the first quarter of calendar 2027",
  "paragraph_id": "0000866374-26-000030:notes:14",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "earnings_quality_spin_off_costs_excluded_as_legal_and_other",
  "what_changed": "The segment reconciliation footnote now says legal and other for the quarter included $53 million of costs for the intended CPI spin-off and $14 million of business acquisition costs. These costs are left out of segment income. The earnings release excludes the same amounts from non-GAAP operating income (8k_2_02:83). The spin is expected to run to the first quarter of calendar 2027, so the prose implies these costs continue.",
  "account": "selling, general and administrative expenses; legal and other",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "legal and other included $53 million of costs associated with the intended spin-off of the CPI business and $14 million of costs related to business acquisitions",
  "paragraph_id": "0000866374-26-000030:notes:134",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "results_against_expectations_sga_increase_attributed_to_spin_and_stock_compensation",
  "what_changed": "MD&A now says SG&A increased by $101 million. It attributes the increase to $53 million of CPI spin-off costs, $18 million of higher stock-based compensation, and other cost increases in line with growth.",
  "account": "selling, general and administrative expenses",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The increase was largely driven by $53 million of costs associated with the intended spin-off of the CPI business, $18 million of increases in stock based compensation and other cost increases in line with the growth of the business.",
  "paragraph_id": "0000866374-26-000030:mdna:80",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "liquidity_and_capital_separation_costs_reduce_operating_cash_flow",
  "what_changed": "MD&A now says $24 million of CPI spin-off separation costs reduced operating cash flow for the quarter. The earnings release says the same of free cash flow and makes no adjustment to free cash flow for these costs (8k_2_02:91).",
  "account": "net cash provided by operating activities; free cash flow",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "Cash provided by operating activities for the three month period ended June 26, 2026 was negatively impacted by $24 million of separation costs incurred in connection with the announced intention to spin-off of Flex's CPI segment.",
  "paragraph_id": "0000866374-26-000030:mdna:100",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "across_documents_warrant_vesting_accelerates_on_shareholder_distribution",
  "what_changed": "The warrant paragraph is carried as changed. It now says that if an acquisition transaction is completed, which may include a distribution to shareholders and is subject to a specified condition, the unvested part of the Amazon warrant vests in part or in full. It also says the Company will negotiate in good faith over a new two-year warrant at expiry if the commercial relationship continues, and that the exercise price is the preceding 30-trading-day VWAP. Read together with the announced CPI spin-off, which is a distribution to shareholders, the spin could accelerate vesting. Warrant expense is recorded as a deduction from revenue. The MD&A warrant paragraph (mdna:113) does not mention the acceleration term. The prior wording of this paragraph is not in my input, so I cannot confirm which of these terms are new.",
  "account": "net sales (warrant deduction from revenue)",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "which may include a distribution to shareholders, subject to a specified condition, the unvested portion of the Warrant will vest in part or in full",
  "paragraph_id": "0000866374-26-000030:notes:63",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "revenue_recognition_warrant_contra_revenue_charge_and_vesting",
  "what_changed": "The warrant note now states $3 million of warrant charges for the quarter. The same note says these are recorded as a deduction from revenue. It also says 0.1 million Warrant Shares had vested and were exercisable as of June 26, 2026. MD&A (mdna:113) repeats the $3 million. The revenue note no longer has its own 'Warrant' subsection describing the deduction from revenue; that description now appears only in the share-based compensation note and in MD&A.",
  "account": "net sales",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "As of the quarter ended June 26, 2026, 0.1 million Warrant Shares have vested and are exercisable.",
  "paragraph_id": "0000866374-26-000030:notes:66",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "structure_and_disclosure_changes_significant_customer_concentration_disclosed",
  "what_changed": "The revenue note has a new Concentration of Risk paragraph. One customer accounted for 12% of net sales in the quarter, most of it in CPI, and the text says no other customer exceeded 10% in either period presented. That wording means no customer exceeded 10% in the prior-year quarter. MD&A (mdna:60) says the same and states that the ten largest customers were approximately 49% and 48% of net sales. The customer is not named. Because most of this revenue is in CPI, the concentration sits in the segment planned for spin-off.",
  "account": "net sales; accounts receivable",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "A significant customer accounted for 12% of net sales during the three-month period ended June 26, 2026. The majority of the revenue with this customer is included within the CPI segment.",
  "paragraph_id": "0000866374-26-000030:notes:53",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "structure_and_disclosure_changes_epp_acquisition_completed",
  "what_changed": "New. On May 1, 2026 the Company completed the acquisition of 100% of Electrical Power Products, Inc. (EPP), described as a U.S. leader in critical power solutions. Total estimated purchase consideration was $1.2 billion in cash, and EPP is reported in CPI. The goodwill note attributes $473 million of goodwill to the acquisition (notes:29). The purchase price table records intangible assets and goodwill. MD&A says $1.1 billion was paid for EPP in investing cash flows (mdna:102).",
  "account": "goodwill; other intangible assets; intangible amortization",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "a U.S. leader in critical power solutions for a total estimated purchase consideration of $1.2 billion in cash",
  "paragraph_id": "0000866374-26-000030:notes:115",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "estimates_and_discretion_epp_purchase_price_allocation_provisional",
  "what_changed": "The acquisition note says the allocation rests on estimated fair values. It says information that existed at the acquisition date may come to light during a measurement period of up to 12 months, and that resulting changes may adjust goodwill. The intangible allocation is labelled 'initial'. The goodwill and intangible amounts, and the amortization that follows from them, are therefore provisional.",
  "account": "goodwill; other intangible assets",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Changes to amounts recorded as assets and liabilities may result in a corresponding adjustment to goodwill during the measurement period.",
  "paragraph_id": "0000866374-26-000030:notes:115",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "estimates_and_discretion_epp_intangible_useful_lives",
  "what_changed": "A new table sets useful lives for the EPP intangibles: trade names 15 years, know-how 10 years, backlog 2 years, customer relationships 20 years. These lives are management's choices and set the amortization path. MD&A (mdna:82) says intangible amortization increased because of EPP, partly offset by intangible assets that became fully amortized during fiscal 2026 and the first quarter of fiscal 2027.",
  "account": "intangible amortization; other intangible assets",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "The following represents the Company's initial allocation of intangible assets identified in the purchase price allocation of the acquired business (in millions):",
  "paragraph_id": "0000866374-26-000030:notes:118",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "across_documents_epp_not_material_yet_named_as_growth_driver",
  "what_changed": "The acquisition note says pro-forma results are not presented because EPP was not material to the condensed consolidated results. Elsewhere, MD&A names 'contributions from the recent EPP acquisition' as part of what drove CPI Power growth (mdna:59) and names EPP as the reason intangible amortization increased (mdna:82). The release also lists $14 million of acquisition costs. The documents describe the same acquisition differently; whether it is material is for the numbers reader.",
  "account": "net sales (CPI)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Pro-forma results of operations have not been presented because the acquisition was not material to the Company's condensed consolidated financial results for the period presented.",
  "paragraph_id": "0000866374-26-000030:notes:120",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "earnings_quality_divestiture_gain_in_other_income",
  "what_changed": "New. In the quarter the Company sold a non-strategic North American business reported in RMS for $90 million of gross cash proceeds. It recorded a $46 million gain in other charges (income), net and derecognized $6 million of goodwill from the Automotive reporting unit. MD&A says the gain is what turned other charges, net into income, partly offset by foreign exchange losses (mdna:88), and that tax on the gain raised the effective tax rate. The release excludes the gain from non-GAAP net income and calls the sale a 'divestiture of a subsidiary'; the goodwill note calls it 'the sale of a site in North America'. A gain reduces the 'other charges (income), net' line.",
  "account": "other charges (income), net",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "Gross cash sale proceeds of $90 million were received, generating a gain on sale of $46 million.",
  "paragraph_id": "0000866374-26-000030:notes:121",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "results_against_expectations_effective_tax_rate_higher_on_mix_and_disposal_gain",
  "what_changed": "MD&A now states the effective tax rate was 24% for the quarter and 22% a year earlier. It says the rate was higher mainly because of the changing jurisdictional mix of income and the additional tax recorded on the gain from the business disposition.",
  "account": "provision for income taxes",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "primarily due to the changing jurisdictional mix of income as well as the additional tax expense recorded on the gain from a business disposition occurring during current period",
  "paragraph_id": "0000866374-26-000030:mdna:93",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "liquidity_and_capital_senior_term_loan_funds_epp_acquisition",
  "what_changed": "There is a new Senior Term Loan: a $1.45 billion loan entered in April 2026 to finance the EPP acquisition. It bears interest at Term SOFR plus a spread set by Flex's credit rating and matures November 29, 2027. It appears as a new line in the debt table, in the debt fair value table, and in a new variable-rate sentence (notes:114). MD&A attributes three things to the new debt: higher interest expense, mainly from debt issued during the quarter (mdna:84); the financing inflow, from net borrowing proceeds (mdna:103); and the increase in cash, from the term loan borrowings (mdna:101).",
  "account": "long-term debt; interest expense",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "In April 2026, the Company entered into a $1.45 billion loan agreement to finance the acquisition of Electrical Power Products, Inc.",
  "paragraph_id": "0000866374-26-000030:notes:79",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "articulation_and_the_filed_history_term_loan_syndication_treated_as_extinguishment",
  "what_changed": "New. In the May 2026 syndication, $1.38 billion of the loan was transferred to new lenders. This is accounted for as a debt extinguishment and shown as additional borrowings and repayments in the cash flow statement, so the syndication inflates both financing lines. The text states no gain or loss on extinguishment and no fees for the syndication.",
  "account": "proceeds from bank borrowings and long-term debt; payments of bank borrowings, long-term debt and other financing liabilities",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "This transfer is accounted for as a debt extinguishment and so is presented as additional borrowings and repayments in the condensed consolidated statements of cash flows.",
  "paragraph_id": "0000866374-26-000030:notes:79",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "across_documents_senior_term_loan_agreement_month_inconsistent",
  "what_changed": "The debt table footnote says the Company entered into a senior term loan agreement in May 2026. The term-loan paragraph (notes:79) says the $1.45 billion loan agreement was entered in April 2026 and syndicated in May 2026. The 8-K list shows Item 1.01/2.03 filings dated 2026-05-04 and 2026-06-02. Their bodies are not in my input, so I cannot say which agreement each one reports.",
  "account": "long-term debt",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "(3)In May 2026, the Company entered into a senior term loan agreement.",
  "paragraph_id": "0000866374-26-000030:notes:74",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "liquidity_and_capital_term_loan_maturities_near_dated",
  "what_changed": "The term-loan paragraph gives the new loan's maturity as November 29, 2027, and the debt table gives the Delayed Draw Term Loan's maturity as December 2027. The debt table shows no current portion at June 26, 2026. The prose implies both loans will move into the current portion as their maturity dates approach; the exact timing is for the numbers reader.",
  "account": "current portion of long-term debt",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "The term loan matures on November 29, 2027.",
  "paragraph_id": "0000866374-26-000030:notes:79",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "liquidity_and_capital_debt_note_facility_and_covenant_text_removed",
  "what_changed": "Four pieces of text are gone from the debt note: (1) the statement that the Company complied with all indenture covenants; (2) the description of the $2.75 billion 2030 Credit Facility, including sub-limits, commitment fees and letter-of-credit fees; (3) the description of the $500 million delayed draw term loan, including SOFR plus 100 basis points and permitted uses; (4) the detail of the November 2025 notes issuance. MD&A still states that the Company complied with the covenants under all credit facilities and indentures as of June 26, 2026, and had no borrowings under the $2.75 billion revolver (mdna:99).",
  "account": "long-term debt",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "As of December 31, 2025, the Company was in compliance with all covenants in the indentures governing the Notes.",
  "paragraph_id": "0000866374-26-000005:note_history:45",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_foreign_tax_settlement_text_removed",
  "what_changed": "The contingencies note no longer describes the foreign Tax Authority matter. The removed text covered about $167 million assessed for fiscal years 2010 to 2020, a $50 million settlement with a definitive agreement executed February 3, 2026, and a further $20 million cash payment expected in the fourth quarter of fiscal 2026. The current note does not say whether that payment was made. The only specific matter left is the Brazilian sales and import tax assessments.",
  "account": "income taxes payable; provision for income taxes",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "The definitive settlement agreement was executed on February 3, 2026 and the $20 million cash payment is expected to occur in the fourth quarter of fiscal year ending March 31, 2026.",
  "paragraph_id": "0000866374-26-000005:note_history:2",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "estimates_and_discretion_ukraine_missile_strike_moved_out_of_notes",
  "what_changed": "The notes no longer carry the 'Impact of Missile Strike in Ukraine' paragraph. That paragraph split the charges into long-lived asset impairments, inventory write-downs and other charges, and placed them in restructuring and impairment charges. MD&A now gives a full-year figure of $51 million for the year ended March 31, 2026, attributed to the August 21, 2025 strike on the Mukachevo facility. It still expects additional immaterial near-term inefficiencies as restoration progresses. The current text does not break the full-year figure down.",
  "account": "restructuring and impairment charges; inventory write-downs; cost of sales",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "During the fiscal year ended March 31, 2026, we recognized $51 million in asset impairments, inventory write-downs and other charges as a result of a missile strike on our Mukachevo, Ukraine facility",
  "paragraph_id": "0000866374-26-000030:mdna:24",
  "explanation": true,
  "insufficient": false }
```

```json
{ "id": "estimates_and_discretion_iran_operations_named_in_estimate_uncertainty",
  "what_changed": "The estimates paragraph lists geopolitical conflicts that create uncertainty in estimates. It now names 'recent U.S. and Israel military operations in Iran' where it previously named 'the Israel-Hamas conflict'. The MD&A estimates paragraph (mdna:50) makes the same change.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "recent U.S. and Israel military operations in Iran, and other geopolitical conflicts",
  "paragraph_id": "0000866374-26-000030:notes:20",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_middle_east_conflicts_section",
  "what_changed": "The MD&A geopolitical section is now titled 'Russian Invasion of Ukraine and Middle East Conflicts'. It says the Company is monitoring and responding to the Israel-Hamas conflict and recent U.S. and Israel military operations in Iran, and calls the full impact uncertain.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "We also are monitoring and responding to the Israel-Hamas conflict and recent U.S. and Israel military operations in Iran.",
  "paragraph_id": "0000866374-26-000030:mdna:23",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_strait_of_hormuz_shipping",
  "what_changed": "The supply-chain risk bullet now names disruptions to international commerce from the Strait of Hormuz alongside the Red Sea. The prior wording is not in my input. The Hormuz reference appears in the same filing that newly names the Iran operations.",
  "account": "cost of sales; inventories",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "disruptions in international commerce as a result of disruptions in the Strait of Hormuz and the Red Sea",
  "paragraph_id": "0000866374-26-000030:mdna:42",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_tariff_pass_through_quantified",
  "what_changed": "MD&A now puts a size on the quarter's tariff effect: tariff costs paid and recoveries from customers affected revenues and cost of goods by approximately one percent, with negligible effect on profitability. It repeats that passing tariffs through raises net sales, lowers operating income margins and delays operating cash flow. It also says results and cash flows would suffer if full pass-through stops.",
  "account": "net sales; cost of sales; net cash provided by operating activities",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "tariff costs paid and recoveries from our customers impacted our revenues and costs of goods by approximately one percent and had a negligible impact on our profitability",
  "paragraph_id": "0000866374-26-000030:mdna:26",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "earnings_quality_ieepa_tariff_refunds_received",
  "what_changed": "New. The Supreme Court struck down the IEEPA tariffs on February 20, 2026, and a refund system opened on April 20, 2026. The Company says it has requested refunds, has received a portion of them, and does not expect them to have a material effect. The text does not say where the refunds are recorded, whether any amount received is owed on to customers who bore the tariffs, or how much is still outstanding.",
  "account": "cost of sales; other current assets; other current liabilities (customer-related accruals)",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "We have requested and received a portion of our requested IEEPA tariff refunds and do not expect refunds received will have a material effect on our financial performance.",
  "paragraph_id": "0000866374-26-000030:mdna:26",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_memory_pricing_working_capital",
  "what_changed": "New 'Memory Pricing Environment' section. It says DRAM and NAND prices stayed elevated in the quarter because of AI and data center demand. The Company generally expects to pass increases through where contracts allow. Sustained increases could keep raising net sales while lowering gross profit percentage and increasing inventory balances and working capital needs. Management gives this as a cause of higher inventory and working capital.",
  "account": "inventories; net sales; gross profit percentage",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "sustained increases in memory pricing could continue to favorably impact net sales, while unfavorably impacting our gross profit percentage and increasing inventory balances and working capital requirements",
  "paragraph_id": "0000866374-26-000030:mdna:28",
  "explanation": true,
  "insufficient": false }
```

```json
{ "id": "earnings_quality_net_sales_growth_partly_memory_price_and_acquisition",
  "what_changed": "MD&A now gives the drivers of sales growth by segment. ITS: Communications demand, plus higher memory pricing in Communications and Lifestyle. RMS: Industrial. CPI: Power, including contributions from the recent EPP acquisition, plus Cloud and Cooling demand. By MD&A's own account, part of the growth is memory-price pass-through and acquired revenue.",
  "account": "net sales",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "primarily driven by strong growth in the Communications business due to increased demand and increased memory pricing in both Communications and our Lifestyle businesses",
  "paragraph_id": "0000866374-26-000030:mdna:59",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "results_against_expectations_its_margin_memory_dilution",
  "what_changed": "MD&A now says ITS segment margin increased 10 basis points. It credits growth in higher-margin Communications, partly offset by lower margins from memory price increases.",
  "account": "segment income (ITS)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "partially offset by the impact of lower margins due to memory price increases",
  "paragraph_id": "0000866374-26-000030:mdna:73",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "results_against_expectations_rms_margin_mix",
  "what_changed": "MD&A now says RMS segment margin increased 130 basis points, mainly because of favorable mix in Industrial and Automotive. The cost-of-sales discussion (mdna:64) says favorable mix and cost efficiencies partly offset the growth in RMS cost of sales.",
  "account": "segment income (RMS); cost of sales",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "primarily due to favorable mix in Industrial and Automotive",
  "paragraph_id": "0000866374-26-000030:mdna:74",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "results_against_expectations_cpi_margin_power_offset_by_investment",
  "what_changed": "MD&A now says CPI segment margin increased 20 basis points. It credits growth and margin expansion in Power, offset by continued investment in growing the CPI businesses.",
  "account": "segment income (CPI)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "primarily due to growth and margin expansion in Power, offset by continued investments in the growth of the CPI businesses",
  "paragraph_id": "0000866374-26-000030:mdna:76",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "results_against_expectations_gross_margin_mix_and_execution",
  "what_changed": "MD&A now says gross margin improved 70 basis points year over year, mainly because of revenue growth, favorable mix and continued operational execution. The cost-of-sales paragraph (mdna:64) says ITS and CPI cost of sales moved in line with revenue.",
  "account": "gross profit",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Gross margin improved 70 basis points year over year primarily due to revenue growth, favorable mix and continued operational execution.",
  "paragraph_id": "0000866374-26-000030:mdna:67",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "estimates_and_discretion_restructuring_severance_estimate_reversal",
  "what_changed": "MD&A now says the Company reversed $2 million of restructuring charges in the quarter, mainly because of updated estimates of employee severance. This is a change in the estimate behind the severance reserve.",
  "account": "restructuring accrual (severance); restructuring and impairment charges",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "we reversed $2 million of restructuring charges primarily related to updated estimates of employee severance",
  "paragraph_id": "0000866374-26-000030:mdna:78",
  "explanation": true,
  "insufficient": false }
```

```json
{ "id": "across_documents_restructuring_recognized_versus_reversed",
  "what_changed": "The restructuring note says the Company 'recognized $2 million of restructuring and impairment charges' ($1 million severance and $1 million impairment). MD&A says it 'reversed $2 million of restructuring charges' because of updated severance estimates (mdna:78). The earnings release says it recognized $1 million of restructuring charges, mostly severance (8k_2_02:82), and the segment footnote refers to $1 million (notes:133). The documents describe the same quarter's restructuring with opposite verbs.",
  "account": "restructuring and impairment charges",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "the Company recognized $2 million of restructuring and impairment charges, of which $1 million related to employee severance and $1 million for impairment",
  "paragraph_id": "0000866374-26-000030:notes:142",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "estimates_and_discretion_contingent_consideration_fully_released",
  "what_changed": "The fair value note now says the remaining $2 million contingent consideration liability for a fiscal 2025 acquisition was fully released in the quarter, leaving it at zero. No reason is given beyond the valuation method, which is based on the probability of hitting milestones. The note does not say where the release is recorded. The follow-on sentence (notes:106) now says 'no other' additions or adjustments.",
  "account": "contingent consideration liability; operating expenses",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "During the three months ended June 26, 2026, the Company fully released the remaining $2 million contingent consideration liability.",
  "paragraph_id": "0000866374-26-000030:notes:104",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "across_documents_cross_currency_swap_balance_sheet_location",
  "what_changed": "The hedging note now says the fair value of the USD HUF cross currency swaps was in other current assets at June 26, 2026 and in other non-current liabilities at March 31, 2026; the text describes an asset now and a liability before. The derivatives table (notes:90) shows designated foreign currency contracts in 'Other non-current assets' at June 26, 2026. The swaps hedge HUF bonds due December 2031. The text and the table give different balance sheet locations.",
  "account": "other current assets; other non-current assets; accumulated other comprehensive loss",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "the fair value of the cross currency swaps was included in other current assets and other non-current liabilities as of June 26, 2026 and March 31, 2026, respectively",
  "paragraph_id": "0000866374-26-000030:notes:88",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "earnings_quality_performance_awards_tied_to_adjusted_eps",
  "what_changed": "The RSU paragraph now says the quarter's performance-based grants are tied to adjusted EPS growth and operating profit goals, with a maximum of about 0.7 million shares. It says no market-condition awards were granted in the first quarter of fiscal 2027, and that 0.7 million shares were issued above target for fiscal 2024 awards. The earnings release says management's incentive compensation is set using certain non-GAAP measures (8k_2_02:71). The prior wording is not in my input, so I cannot confirm whether the absence of market-condition grants is new.",
  "account": "stock-based compensation",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "These performance-based RSUs include awards tied to the Company's adjusted earnings per share growth and awards tied to operating profit goals.",
  "paragraph_id": "0000866374-26-000030:notes:59",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_chief_accounting_officer_trading_plan",
  "what_changed": "New disclosure. On May 18, 2026 Daniel J. Wendler, Senior Vice President and Chief Accounting Officer, adopted a trading plan to sell up to 10,000 ordinary shares. The plan ends November 30, 2026, unless certain specified events end it earlier.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "On May 18, 2026, Daniel J. Wendler, Senior Vice President and Chief Accounting Officer, adopted a trading plan that provides for the sale of up to 10,000 ordinary shares of the Company.",
  "paragraph_id": "0000866374-26-000030:notes:145",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "liquidity_and_capital_share_repurchases_paused",
  "what_changed": "The share repurchase note now says the Company made no share repurchases in the quarter. MD&A says the same (mdna:111) and states that $1.1 billion remains available under the $1.7 billion authorization. The same quarter included the EPP acquisition and the new term loan.",
  "account": "payments for repurchases of ordinary shares",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "the Company made no share repurchases.",
  "paragraph_id": "0000866374-26-000030:notes:126",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "liquidity_and_capital_cash_held_outside_singapore_share",
  "what_changed": "MD&A now states that approximately 29% of cash and cash equivalents at June 26, 2026, and 62% at March 31, 2026, was held by foreign subsidiaries outside Singapore. It puts indefinitely reinvested foreign earnings at approximately $0.9 billion as of March 31, 2026. The text gives no explanation for these percentages.",
  "account": "cash and cash equivalents",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "approximately 29% and 62%, respectively, of our cash and cash equivalents were held by foreign subsidiaries outside of Singapore",
  "paragraph_id": "0000866374-26-000030:mdna:106",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "liquidity_and_capital_working_capital_change_explained",
  "what_changed": "MD&A now explains the change in net working capital. It cites a $0.5 billion increase in cash driven by senior term loan borrowings and a $0.6 billion increase in inventory. Other increases it lists are $0.4 billion in accounts receivable, $0.3 billion in contract assets and $0.2 billion in other current assets, mainly customer-controlled inventory. Against these it lists increases of $1.1 billion in accounts payable and $0.3 billion in other current liabilities. The paragraph gives causes for the cash and other-current-asset movements but none for inventory or receivables. The memory-pricing section (mdna:28) is the only stated driver of inventory.",
  "account": "inventories; accounts receivable; contract assets; other current assets; accounts payable",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The increase was primarily the result of a $0.5 billion increase in cash and cash equivalents driven by the net increase from our senior term loan borrowings along with a $0.6 billion increase in our inventory balance.",
  "paragraph_id": "0000866374-26-000030:mdna:101",
  "explanation": true,
  "insufficient": false }
```

```json
{ "id": "structure_and_disclosure_changes_new_codification_improvements_standard",
  "what_changed": "New paragraph on ASU 2025-12 'Codification Improvements', which includes clarification of the accounting for retiring treasury stock. It takes effect for the Company in the first quarter of fiscal 2028. The Company is evaluating the adoption method and the effect on its disclosures.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "which includes numerous refinements and enhancements, including clarifications on the accounting for the retirement of treasury stock among others",
  "paragraph_id": "0000866374-26-000030:notes:23",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "structure_and_disclosure_changes_accounting_pronouncement_paragraphs_removed",
  "what_changed": "Three standards have been dropped from the pronouncements section: (1) ASU 2023-09 on income tax disclosures, then due in the fourth quarter of fiscal 2026; (2) ASU 2025-10 on government grants, which the removed text said takes effect in the first quarter of fiscal 2030 with immaterial expected impact; (3) the 'Recently Adopted' ASU 2025-05, a credit-loss practical expedient for receivables and contract assets. The text does not explain why ASU 2025-10 was removed.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "which establishes comprehensive guidance on the recognition, measurement, presentation, and disclosure of government grants",
  "paragraph_id": "0000866374-26-000005:note_history:28",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "liquidity_and_capital_supplier_finance_program_count",
  "what_changed": "The supplier finance paragraph is carried as changed. It now says the Company has six supplier finance programs with substantially similar characteristics. Confirmed outstanding obligations are stated as $134 million at June 26, 2026 and $154 million at March 31, 2026 (notes:45). The prior wording is not in my input, so I cannot tell whether the number of programs or any term changed.",
  "account": "accounts payable",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "The Company has six supplier finance programs, all of which have substantially similar characteristics",
  "paragraph_id": "0000866374-26-000030:notes:43",
  "explanation": false,
  "insufficient": true }
```

```json
{ "id": "results_against_expectations_second_quarter_guidance",
  "what_changed": "The release gives guidance for the second quarter of fiscal 2027. Net sales $7.95 billion to $8.25 billion, 'growth of 19% at the midpoint'. Adjusted operating income $535 million to $565 million. Adjusted EPS $1.00 to $1.07, 'growth of 32% at the midpoint'. Interest and other about $58 million. Adjusted tax rate 21%. About 375 million weighted shares.",
  "account": "net sales; adjusted operating income; adjusted EPS",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "Net Sales: $7.95 billion to $8.25 billion, growth of 19% at the midpoint",
  "paragraph_id": "0000866374-26-000026:8k_2_02:24",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "results_against_expectations_full_year_guidance_updated",
  "what_changed": "The release now carries 'Updated Fiscal Year 2027 Guidance', with the Prior and Updated ranges side by side. Updated ranges: net sales $33.7 billion to $35.2 billion ('growth of 23% at the midpoint'); adjusted operating margin 7.0% to 7.2%; adjusted EPS $4.42 to $4.74 ('growth of 39% at the midpoint'). A footnote says the full-year guidance does not give effect to the planned CPI spin-off (8k_2_02:38).",
  "account": "net sales; adjusted operating margin; adjusted EPS",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "Net Sales: $33.7 billion to $35.2 billion, growth of 23% at the midpoint",
  "paragraph_id": "0000866374-26-000026:8k_2_02:31",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "controls_audit_and_filings_guidance_note_names_wrong_quarter",
  "what_changed": "Schedule V says forward-looking non-GAAP measures appear in 'our first quarter and full year fiscal 2027 guidance'. The guidance in this release is for the second quarter and the full year (8k_2_02:23). The sentence names the wrong quarter.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "in our first quarter and full year fiscal 2027 guidance",
  "paragraph_id": "0000866374-26-000026:8k_2_02:76",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "structure_and_disclosure_changes_investor_day_scheduled",
  "what_changed": "The release announces an Investor Day on November 10th, 2026.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "Announced Investor Day date of November 10th, 2026.",
  "paragraph_id": "0000866374-26-000026:8k_2_02:8",
  "explanation": false,
  "insufficient": false }
```

```json
{ "id": "across_documents_spin_off_press_release_not_in_input",
  "what_changed": "The release says further spin-off risks are described in a separate press release issued the same day. The 8-K list shows an Item 8.01/9.01 filing on 2026-07-29 (0000866374-26-000027), but its body is not in my input, so I cannot report what it says.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Additional information concerning risks related to the planned spin-off is described in the separate press release issued today.",
  "paragraph_id": "0000866374-26-000026:8k_2_02:53",
  "explanation": false,
  "insufficient": true }
```


```json
{ "id": "controls_audit_and_filings_no_control_change_reported_in_acquisition_quarter",
  "what_changed": "Item 4 again says there was no change in internal control over financial reporting during the quarter that materially affected it or is reasonably likely to. Apart from the date, the wording is the standing wording. Per the notes, this same quarter included the EPP acquisition, the start of separation work for the CPI spin-off, the recast to three segments and the new term loan. Item 4 says nothing about bringing EPP into the Company's controls.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "There were no changes in our internal control over financial reporting that occurred during our quarter ended June 26, 2026 that have materially affected, or are reasonably likely to materially affect, our internal control over financial reporting.",
  "paragraph_id": "0000866374-26-000030:item_4_controls:5",
  "explanation": false,
  "insufficient": false }
```

## Paragraphs carried as text that are not the source paragraph of an item

### Notes (0000866374-26-000030)

- 0000866374-26-000030:notes:3: segment bullet; covered by structure_and_disclosure_changes_three_segment_recast
- 0000866374-26-000030:notes:4: segment end-market bullet; covered by the three-segment recast item
- 0000866374-26-000030:notes:5: segment end-market bullet; covered by the three-segment recast item
- 0000866374-26-000030:notes:6: segment bullet; covered by the three-segment recast item
- 0000866374-26-000030:notes:7: segment end-market bullet; covered by the three-segment recast item
- 0000866374-26-000030:notes:8: segment end-market bullet (Automotive rewording); covered by the three-segment recast item
- 0000866374-26-000030:notes:9: segment end-market bullet; covered by the three-segment recast item
- 0000866374-26-000030:notes:10: new CPI segment bullet; covered by the three-segment recast item
- 0000866374-26-000030:notes:11: CPI end-market bullet; covered by the three-segment recast item
- 0000866374-26-000030:notes:12: CPI end-market bullet; covered by the three-segment recast item
- 0000866374-26-000030:notes:16: date rolled forward (fiscal year and period references)
- 0000866374-26-000030:notes:17: date rolled forward (period-length sentence restated for the first quarters)
- 0000866374-26-000030:notes:21: heading
- 0000866374-26-000030:notes:22: standing ASU 2024-03 disclosure; the change history does not flag it; no new matter
- 0000866374-26-000030:notes:26: amounts only (inventory table)
- 0000866374-26-000030:notes:27: amounts only (customer-controlled inventory)
- 0000866374-26-000030:notes:29: goodwill roll-forward prose; covered by structure_and_disclosure_changes_epp_acquisition_completed and earnings_quality_divestiture_gain_in_other_income
- 0000866374-26-000030:notes:31: amounts only (intangibles table)
- 0000866374-26-000030:notes:34: amounts only (amortization schedule)
- 0000866374-26-000030:notes:35: date rolled forward (remaining nine-month period)
- 0000866374-26-000030:notes:37: amounts only (customer working capital advances; terms wording standing)
- 0000866374-26-000030:notes:39: amounts only (deferred tax assets)
- 0000866374-26-000030:notes:41: amounts only (customer-related accruals)
- 0000866374-26-000030:notes:44: continuation of notes:43; no new matter visible
- 0000866374-26-000030:notes:45: amounts only (confirmed supplier finance obligations); cited in the supplier finance item
- 0000866374-26-000030:notes:48: amounts only (contract liabilities); change history shows only amounts and dates changed
- 0000866374-26-000030:notes:51: disaggregation table recast to three segments; amounts; covered by the three-segment recast item
- 0000866374-26-000030:notes:52: heading; covered by the significant customer concentration item
- 0000866374-26-000030:notes:57: amounts only (share-based compensation table)
- 0000866374-26-000030:notes:60: amounts only (RSUs outstanding and vested)
- 0000866374-26-000030:notes:61: amounts only (unrecognized compensation and period)
- 0000866374-26-000030:notes:62: heading
- 0000866374-26-000030:notes:68: amounts only (EPS table)
- 0000866374-26-000030:notes:69: date rolled forward (anti-dilutive footnote)
- 0000866374-26-000030:notes:70: date rolled forward (debt heading)
- 0000866374-26-000030:notes:71: debt table; new Senior Term Loan line covered by liquidity_and_capital_senior_term_loan_funds_epp_acquisition; otherwise amounts
- 0000866374-26-000030:notes:72: wording only (standing notes footnote)
- 0000866374-26-000030:notes:73: footnote renumbered (HUF bonds); reordered
- 0000866374-26-000030:notes:75: amounts only (weighted-average interest rate)
- 0000866374-26-000030:notes:76: date rolled forward
- 0000866374-26-000030:notes:77: amounts only (repayment schedule); maturities covered by liquidity_and_capital_term_loan_maturities_near_dated
- 0000866374-26-000030:notes:78: heading; covered by the senior term loan item
- 0000866374-26-000030:notes:80: date rolled forward (interest heading)
- 0000866374-26-000030:notes:81: amounts only (interest table, including AR sale program expenses)
- 0000866374-26-000030:notes:84: amounts only (aggregate notional)
- 0000866374-26-000030:notes:85: amounts only (notional table)
- 0000866374-26-000030:notes:86: amounts only (deferred gains); the rest is standing wording
- 0000866374-26-000030:notes:87: continuation of notes:86; standing wording
- 0000866374-26-000030:notes:89: date rolled forward
- 0000866374-26-000030:notes:90: amounts only; its location label is cited in across_documents_cross_currency_swap_balance_sheet_location
- 0000866374-26-000030:notes:93: amounts only (AOCI table)
- 0000866374-26-000030:notes:94: wording only (standing reclassification text)
- 0000866374-26-000030:notes:95: amounts only (tax impacts on AOCI)
- 0000866374-26-000030:notes:96: amounts only (receivables sold and outstanding under factoring); same prose
- 0000866374-26-000030:notes:106: wording only ('no other'), follows from the release in notes:104; covered by that item
- 0000866374-26-000030:notes:109: date rolled forward
- 0000866374-26-000030:notes:110: amounts only (recurring fair value table)
- 0000866374-26-000030:notes:112: date rolled forward
- 0000866374-26-000030:notes:113: amounts; new term loan line covered by the senior term loan item
- 0000866374-26-000030:notes:114: added variable-rate sentence for the new term loan; covered by the senior term loan item
- 0000866374-26-000030:notes:117: amounts only (EPP purchase price table); covered by the EPP acquisition item
- 0000866374-26-000030:notes:119: intangible lives table; covered by estimates_and_discretion_epp_intangible_useful_lives
- 0000866374-26-000030:notes:122: heading
- 0000866374-26-000030:notes:123: wording only (standing loss-contingency text)
- 0000866374-26-000030:notes:124: amounts only (Brazilian assessment values updated; status wording standing)
- 0000866374-26-000030:notes:125: wording only (standing ordinary-course text)
- 0000866374-26-000030:notes:127: amounts only (authorization remaining); covered by the share repurchase item
- 0000866374-26-000030:notes:128: three segments named; covered by the three-segment recast item
- 0000866374-26-000030:notes:130: wording only (CODM)
- 0000866374-26-000030:notes:132: amounts only (current-quarter segment table)
- 0000866374-26-000030:notes:133: amounts only (restructuring footnote); cited in across_documents_restructuring_recognized_versus_reversed
- 0000866374-26-000030:notes:135: amounts only (recast prior-year segment table); covered by the recast items
- 0000866374-26-000030:notes:136: prior-year comparative footnote; wording
- 0000866374-26-000030:notes:140: wording only (date typo 'June 27, 205')
- 0000866374-26-000030:notes:141: amounts only (depreciation by segment)
- 0000866374-26-000030:notes:143: date rolled forward
- 0000866374-26-000030:notes:144: amounts only (severance accrual roll-forward)

### MD&A (0000866374-26-000030)

- 0000866374-26-000030:mdna:4: business overview; mirrors notes:2; covered by the three-segment recast item
- 0000866374-26-000030:mdna:5: segment bullet; covered by the three-segment recast item
- 0000866374-26-000030:mdna:6: segment end-market bullet; covered by the three-segment recast item
- 0000866374-26-000030:mdna:7: segment end-market bullet; covered by the three-segment recast item
- 0000866374-26-000030:mdna:8: segment bullet; covered by the three-segment recast item
- 0000866374-26-000030:mdna:9: segment end-market bullet; covered by the three-segment recast item
- 0000866374-26-000030:mdna:10: segment end-market bullet; covered by the three-segment recast item
- 0000866374-26-000030:mdna:11: segment end-market bullet; covered by the three-segment recast item
- 0000866374-26-000030:mdna:12: CPI segment bullet; covered by the three-segment recast item
- 0000866374-26-000030:mdna:13: CPI end-market bullet; covered by the three-segment recast item
- 0000866374-26-000030:mdna:14: CPI end-market bullet; covered by the three-segment recast item
- 0000866374-26-000030:mdna:17: wording only; paragraph split by page break
- 0000866374-26-000030:mdna:18: page number
- 0000866374-26-000030:mdna:19: continuation of mdna:17; wording only
- 0000866374-26-000030:mdna:22: heading; covered by narrative_signs_of_operating_pressure_middle_east_conflicts_section
- 0000866374-26-000030:mdna:27: heading; covered by the memory pricing item
- 0000866374-26-000030:mdna:29: page number
- 0000866374-26-000030:mdna:31: amounts and dates rolled forward (revenue scale, facility count)
- 0000866374-26-000030:mdna:32: amounts only (net sales by region and country)
- 0000866374-26-000030:mdna:33: amounts only (property and equipment by country)
- 0000866374-26-000030:mdna:36: prior wording not in input; standing risk bullet (names stagflation among conditions); no new matter identifiable
- 0000866374-26-000030:mdna:37: prior wording not in input; standing risk bullet
- 0000866374-26-000030:mdna:38: prior wording not in input; standing risk bullet
- 0000866374-26-000030:mdna:40: prior wording not in input; standing risk bullet
- 0000866374-26-000030:mdna:41: prior wording not in input; standing risk bullet
- 0000866374-26-000030:mdna:43: prior wording not in input; standing risk bullet (integration of acquired businesses)
- 0000866374-26-000030:mdna:44: prior wording not in input; standing risk bullet
- 0000866374-26-000030:mdna:45: prior wording not in input; standing risk bullet
- 0000866374-26-000030:mdna:46: prior wording not in input; standing risk bullet
- 0000866374-26-000030:mdna:47: prior wording not in input; standing risk bullet
- 0000866374-26-000030:mdna:48: date rolled forward (10-K reference)
- 0000866374-26-000030:mdna:50: same Iran change as notes:20; covered by estimates_and_discretion_iran_operations_named_in_estimate_uncertainty
- 0000866374-26-000030:mdna:51: date rolled forward (10-K reference)
- 0000866374-26-000030:mdna:52: page number
- 0000866374-26-000030:mdna:54: date rolled forward
- 0000866374-26-000030:mdna:55: amounts only (percentage of sales table)
- 0000866374-26-000030:mdna:58: amounts only (segment net sales table)
- 0000866374-26-000030:mdna:60: covered by the significant customer concentration item; top-ten amounts
- 0000866374-26-000030:mdna:61: page number
- 0000866374-26-000030:mdna:64: cost of sales drivers; covered by results_against_expectations_rms_margin_mix and results_against_expectations_gross_margin_mix_and_execution
- 0000866374-26-000030:mdna:69: prior wording not in input; segment income definition matches the note's reconciling items; no new matter identifiable
- 0000866374-26-000030:mdna:70: wording only (CODM)
- 0000866374-26-000030:mdna:72: amounts only (segment income table)
- 0000866374-26-000030:mdna:82: amortization driver; covered by estimates_and_discretion_epp_intangible_useful_lives
- 0000866374-26-000030:mdna:84: interest expense driver; covered by the senior term loan item
- 0000866374-26-000030:mdna:86: amounts only (interest income)
- 0000866374-26-000030:mdna:88: divestiture gain and FX offset; covered by earnings_quality_divestiture_gain_in_other_income
- 0000866374-26-000030:mdna:90: amounts only; generic driver (equity method losses)
- 0000866374-26-000030:mdna:92: date rolled forward (10-K note reference)
- 0000866374-26-000030:mdna:94: date rolled forward (Pillar Two)
- 0000866374-26-000030:mdna:95: no new matter visible (OBBBA, no material impact expected)
- 0000866374-26-000030:mdna:97: amounts only (net income)
- 0000866374-26-000030:mdna:99: amounts only (liquidity sources); the covenant compliance statement is cited in the debt-note removal item
- 0000866374-26-000030:mdna:102: investing cash amounts; EPP payment covered by the EPP acquisition item
- 0000866374-26-000030:mdna:103: financing cash; covered by the senior term loan item
- 0000866374-26-000030:mdna:104: amounts only (free cash flow)
- 0000866374-26-000030:mdna:105: amounts only (free cash flow table)
- 0000866374-26-000030:mdna:108: date rolled forward (commercial paper, none outstanding)
- 0000866374-26-000030:mdna:110: prior wording not in input; standing capital-structure and dilution text
- 0000866374-26-000030:mdna:111: covered by liquidity_and_capital_share_repurchases_paused
- 0000866374-26-000030:mdna:113: covered by revenue_recognition_warrant_contra_revenue_charge_and_vesting
- 0000866374-26-000030:mdna:115: date rolled forward (10-K reference)

### Item 4 (0000866374-26-000030)

- 0000866374-26-000030:item_4_controls:1: heading
- 0000866374-26-000030:item_4_controls:2: heading
- 0000866374-26-000030:item_4_controls:3: date rolled forward (disclosure controls effective)
- 0000866374-26-000030:item_4_controls:4: heading
- 0000866374-26-000030:item_4_controls:6: page number

### 8-K Item 2.02 release (0000866374-26-000026)

- 0000866374-26-000026:8k_2_02:1: exhibit header
- 0000866374-26-000026:8k_2_02:2: header
- 0000866374-26-000026:8k_2_02:3: header
- 0000866374-26-000026:8k_2_02:4: title
- 0000866374-26-000026:8k_2_02:5: amounts only (headline net sales)
- 0000866374-26-000026:8k_2_02:6: amounts only (margins)
- 0000866374-26-000026:8k_2_02:7: amounts only (EPS; 'record' adjusted EPS claim)
- 0000866374-26-000026:8k_2_02:9: dateline
- 0000866374-26-000026:8k_2_02:10: promotional CEO quote; S&P 500 inclusion mentioned, no accounting matter; spin covered elsewhere
- 0000866374-26-000026:8k_2_02:11: heading
- 0000866374-26-000026:8k_2_02:12: amounts only
- 0000866374-26-000026:8k_2_02:13: amounts only
- 0000866374-26-000026:8k_2_02:14: amounts only
- 0000866374-26-000026:8k_2_02:15: amounts only
- 0000866374-26-000026:8k_2_02:16: amounts only
- 0000866374-26-000026:8k_2_02:17: heading
- 0000866374-26-000026:8k_2_02:18: amounts only
- 0000866374-26-000026:8k_2_02:19: amounts only
- 0000866374-26-000026:8k_2_02:20: amounts only
- 0000866374-26-000026:8k_2_02:21: amounts only
- 0000866374-26-000026:8k_2_02:22: cross-reference
- 0000866374-26-000026:8k_2_02:23: heading; covered by results_against_expectations_second_quarter_guidance
- 0000866374-26-000026:8k_2_02:25: covered by the second-quarter guidance item
- 0000866374-26-000026:8k_2_02:26: covered by the second-quarter guidance item
- 0000866374-26-000026:8k_2_02:27: covered by the second-quarter guidance item
- 0000866374-26-000026:8k_2_02:28: covered by the second-quarter guidance item
- 0000866374-26-000026:8k_2_02:29: covered by the second-quarter guidance item
- 0000866374-26-000026:8k_2_02:30: heading; covered by results_against_expectations_full_year_guidance_updated
- 0000866374-26-000026:8k_2_02:32: covered by the full-year guidance item
- 0000866374-26-000026:8k_2_02:33: covered by the full-year guidance item
- 0000866374-26-000026:8k_2_02:34: covered by the full-year guidance item
- 0000866374-26-000026:8k_2_02:35: header
- 0000866374-26-000026:8k_2_02:36: prior versus updated guidance table; covered by the full-year guidance item
- 0000866374-26-000026:8k_2_02:37: non-GAAP footnote boilerplate
- 0000866374-26-000026:8k_2_02:38: guidance excludes spin; covered by the full-year guidance item
- 0000866374-26-000026:8k_2_02:39: heading
- 0000866374-26-000026:8k_2_02:40: webcast logistics
- 0000866374-26-000026:8k_2_02:41: heading
- 0000866374-26-000026:8k_2_02:42: About Flex boilerplate
- 0000866374-26-000026:8k_2_02:43: contacts
- 0000866374-26-000026:8k_2_02:44: contacts
- 0000866374-26-000026:8k_2_02:45: contacts
- 0000866374-26-000026:8k_2_02:46: contacts
- 0000866374-26-000026:8k_2_02:47: contacts
- 0000866374-26-000026:8k_2_02:48: contacts
- 0000866374-26-000026:8k_2_02:49: contacts
- 0000866374-26-000026:8k_2_02:50: contacts
- 0000866374-26-000026:8k_2_02:51: header
- 0000866374-26-000026:8k_2_02:52: heading
- 0000866374-26-000026:8k_2_02:54: header
- 0000866374-26-000026:8k_2_02:55: header
- 0000866374-26-000026:8k_2_02:56: amounts only (income statement)
- 0000866374-26-000026:8k_2_02:57: header
- 0000866374-26-000026:8k_2_02:58: header
- 0000866374-26-000026:8k_2_02:59: amounts only (GAAP to non-GAAP reconciliation)
- 0000866374-26-000026:8k_2_02:60: header
- 0000866374-26-000026:8k_2_02:61: header
- 0000866374-26-000026:8k_2_02:62: amounts only (balance sheet)
- 0000866374-26-000026:8k_2_02:63: header
- 0000866374-26-000026:8k_2_02:64: header
- 0000866374-26-000026:8k_2_02:65: amounts only (cash flow statement)
- 0000866374-26-000026:8k_2_02:66: header
- 0000866374-26-000026:8k_2_02:67: header
- 0000866374-26-000026:8k_2_02:68: header
- 0000866374-26-000026:8k_2_02:69: header
- 0000866374-26-000026:8k_2_02:70: non-GAAP description boilerplate
- 0000866374-26-000026:8k_2_02:71: non-GAAP rationale boilerplate; the incentive-compensation sentence is cited in earnings_quality_performance_awards_tied_to_adjusted_eps
- 0000866374-26-000026:8k_2_02:72: boilerplate bullet
- 0000866374-26-000026:8k_2_02:73: boilerplate bullet
- 0000866374-26-000026:8k_2_02:74: boilerplate bullet
- 0000866374-26-000026:8k_2_02:75: boilerplate bullet
- 0000866374-26-000026:8k_2_02:77: header
- 0000866374-26-000026:8k_2_02:78: introductory sentence
- 0000866374-26-000026:8k_2_02:79: stock-based compensation exclusion boilerplate
- 0000866374-26-000026:8k_2_02:80: amortization exclusion boilerplate
- 0000866374-26-000026:8k_2_02:81: restructuring exclusion boilerplate
- 0000866374-26-000026:8k_2_02:82: restructuring amount; covered by across_documents_restructuring_recognized_versus_reversed
- 0000866374-26-000026:8k_2_02:83: legal and other amounts; covered by earnings_quality_spin_off_costs_excluded_as_legal_and_other
- 0000866374-26-000026:8k_2_02:84: prior-year comparative amounts (equity method fund valuation)
- 0000866374-26-000026:8k_2_02:85: interest and other exclusion text; gain covered by the divestiture item
- 0000866374-26-000026:8k_2_02:86: header
- 0000866374-26-000026:8k_2_02:87: divestiture gain; covered by the divestiture item
- 0000866374-26-000026:8k_2_02:88: standing tax-adjustment text (normalized rate stated as effective fiscal 2026, not this quarter)
- 0000866374-26-000026:8k_2_02:89: amounts only (tax effects)
- 0000866374-26-000026:8k_2_02:90: free cash flow definition boilerplate
- 0000866374-26-000026:8k_2_02:91: separation costs in free cash flow; covered by liquidity_and_capital_separation_costs_reduce_operating_cash_flow
