# FN 10-K FY2026 (0001408710-26-000028) — notes text reader

Input check: the directory holds only the six permitted inputs. It has no trend table, prices, returns, short interest, other-company files, prior probabilities or outcome window. The 8-K exhibit 99.1 carries the company's own financial statement tables. That is allowed and is not used for arithmetic here.

Scope note: the notes came through as full text, with no paragraph marked `[same as prior period ...]`. So every paragraph is accounted for below. The prior 10-K text is not in the input. "New" is therefore judged from the text itself, from the Q2→Q3 note change history, and from the other documents in the input. No amounts were computed or compared.

Prior flags: none on record.

## Items

```json
{ "id": "revenue_recognition_geography_basis_moved_to_ship_to", "what_changed": "Starting in Q4 FY2026, geographic revenue is attributed by the customer's ship-to location instead of bill-to, and prior periods are recast. The Q3 10-Q geography tables (note_history:18, :21) were on the bill-to basis and showed different country names leading. The annual ship-to table (notes:134) puts Thailand first. The quarterly and annual geography figures are no longer on one basis, so the numbers reader should not tie them together.", "account": "revenue by geographic area", "expected_direction": "none", "horizon": "this quarter", "quote": "updated its geographic area presentation from the bill-to-location of its customers to the ship-to-location of its customers", "paragraph_id": "0001408710-26-000028:notes:131", "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_end_market_categories_replaced", "what_changed": "The optical/non-optical revenue categories are replaced with data center, communications infrastructure, and automotive/industrial/other, recast for prior periods. High-performance computing, shown under non-optical in the Q3 10-Q (note_history:23), now falls inside data center according to the footnote (mdna:102).", "account": "revenue by end market", "expected_direction": "none", "horizon": "this quarter", "quote": "we updated our revenue category presentation from optical communications and non-optical communications to data center, communications infrastructure, and automotive, industrial and other markets", "paragraph_id": "0001408710-26-000028:mdna:100", "explanation": false }
```

```json
{ "id": "across_documents_raytek_stake_percentage_differs", "what_changed": "The 10-K describes the March 25, 2026 Raytek share purchase as a 13.8% equity interest for NT$1.02 billion ($32.4 million). The Q3 10-Q subsequent-event note (note_history:33) described the same agreement and price as a 16.0% equity interest. The two filings give different stake percentages for one transaction.", "account": "non-marketable equity securities", "expected_direction": "none", "horizon": "this quarter", "quote": "to acquire a 13.8% equity interest in Raytek Semiconductor, Inc.", "paragraph_id": "0001408710-26-000028:notes:185", "explanation": false }
```

```json
{ "id": "estimates_and_discretion_raytek_observable_price_remeasurement_gain", "what_changed": "This is new: Raytek began trading on the Taipei Emerging Stock Board in May 2026. The company treated that trading as an observable price change under the ASC 321 measurement alternative. It remeasured its restricted, unlisted shares from the board price, adjusted with a management-chosen discount for lack of marketability. The resulting unrealized gain went to other income in Q4. The policy (notes:116) says the valuation 'requires our judgment', and the MD&A critical policy (mdna:92) says adjustments 'may require use of unobservable inputs'. The 8-K excludes the gain from non-GAAP results.", "account": "other income (expense), net; non-marketable equity securities", "expected_direction": "up", "horizon": "this quarter", "quote": "As a result of the remeasurement, the Company recognized an unrealized gain of $56.7 million in other income (expense), net, during fiscal year 2026 and increased the carrying amount of the investment to $89.1 million as of June 26, 2026.", "paragraph_id": "0001408710-26-000028:notes:187", "explanation": false }
```

```json
{ "id": "across_documents_no_policy_change_stated_while_new_policy_added", "what_changed": "MD&A says there were no changes to accounting policies. The same filing adds a new non-marketable equity securities policy in the notes (notes:115-118) and a new critical accounting policy section in MD&A (mdna:91-93).", "account": "non-marketable equity securities", "expected_direction": "none", "horizon": "this quarter", "quote": "There were no changes to our accounting policies.", "paragraph_id": "0001408710-26-000028:mdna:77", "explanation": false }
```

```json
{ "id": "earnings_quality_pillar_two_top_up_tax_recognized", "what_changed": "This is new: current income tax expense under enacted Pillar Two UTPR legislation, with the liability sitting in income tax payable. MD&A attributes the higher effective tax rate to it (mdna:115) and names Thailand among the jurisdictions that enacted UTPR (mdna:72). It also warns that future law changes could materially affect the tax rate and cash taxes.", "account": "income tax expense; income tax payable", "expected_direction": "up", "horizon": "this quarter", "quote": "For the year ended June 26, 2026, we recognized $57.4 million of current income tax expense related to enacted Pillar Two UTPR legislation.", "paragraph_id": "0001408710-26-000028:mdna:73", "explanation": false }
```

```json
{ "id": "earnings_quality_non_gaap_new_exclusions_pillar_two_and_equity_revaluation", "what_changed": "The non-GAAP definition in the earnings release now also excludes non-marketable equity securities revaluation and Pillar Two tax charges. The reconciliation (8k_2_02:66) removes both the Raytek gain and the Pillar Two provision in Q4. The release also says non-GAAP measures are used to set employee incentive pay (8k_2_02:38).", "account": "non-GAAP net income and EPS", "expected_direction": "none", "horizon": "this quarter", "quote": "non-marketable equity securities revaluation; and charges arising from the implementation or application of the OECD Pillar Two global minimum tax framework", "paragraph_id": "0001408710-26-000026:8k_2_02:39", "explanation": false }
```

```json
{ "id": "earnings_quality_pillar_two_carried_into_guidance_as_excluded_item", "what_changed": "The release says guidance excludes share-based compensation and 'certain non-recurring items'. The Q1 FY2027 guidance reconciliation (8k_2_02:73) excludes a further Pillar Two tax provision of $0.40 per share. A charge the company expects to recur next quarter is being excluded under a description that calls it non-recurring.", "account": "income tax expense; non-GAAP EPS guidance", "expected_direction": "up", "horizon": "next quarter", "quote": "excludes share-based compensation expenses and certain non-recurring items", "paragraph_id": "0001408710-26-000026:8k_2_02:30", "explanation": false }
```

```json
{ "id": "earnings_quality_chonburi_tax_exemption_expired", "what_changed": "The text now says the Chonburi campus tax exemption ran through June 2026. That is the end of FY2026. What remains is the Building 9 exemption through 2031, capped at the actual investment ($52.2 million per mdna:69), plus a Navanakorn incentive that begins in August 2027. The prose implies more Thai income becomes taxable from FY2027.", "account": "income tax expense", "expected_direction": "up", "horizon": "next quarter", "quote": "was not subject to tax in Thailand from July 2018 through June 2026 on income generated from the manufacture of products at its Chonburi campus", "paragraph_id": "0001408710-26-000028:notes:142", "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_income_tax_disclosure_standard_adopted", "what_changed": "ASU 2023-09 was adopted prospectively for FY2026. There is a new rate reconciliation format with a 'Pillar Two Top-up Tax' line, and new cash taxes paid by jurisdiction (notes:148-149). Prior years stay in the old format (notes:152-153), so the two reconciliations do not line up row by row.", "account": "income tax expense", "expected_direction": "none", "horizon": "this quarter", "quote": "Beginning in fiscal year 2026, the Company adopted ASU 2023-09 prospectively.", "paragraph_id": "0001408710-26-000028:notes:150", "explanation": false }
```

```json
{ "id": "estimates_and_discretion_israel_valuation_allowance_added", "what_changed": "The text states a FY2026 valuation allowance amount for the Israel subsidiary's deferred tax assets. The cause given is continuing net operating losses expected for the foreseeable future. The valuation allowance rollforward (notes:160) shows an addition and no reduction in FY2026.", "account": "deferred tax assets valuation allowance", "expected_direction": "up", "horizon": "this quarter", "quote": "The Company continued to record the full valuation allowance of $0.8 million and $2.1 million for fiscal year 2025 and fiscal year 2026, respectively.", "paragraph_id": "0001408710-26-000028:notes:163", "explanation": true }
```

```json
{ "id": "estimates_and_discretion_uncertain_tax_position_additions", "what_changed": "The uncertain tax position text now states accrued interest and penalties as of June 26, 2026. It says nothing was reversed in FY2026 and that Thailand tax years 2020 through 2024 remain open. The rollforward (notes:169) shows FY2026 additions and no prior-year releases. The new reconciliation adds a 'Changes in unrecognized tax benefits' line (notes:151).", "account": "uncertain tax positions; income tax payable", "expected_direction": "up", "horizon": "12 months", "quote": "No interest and penalties were reversed in fiscal 2026.", "paragraph_id": "0001408710-26-000028:notes:167", "explanation": false }
```

```json
{ "id": "estimates_and_discretion_inventory_excess_obsolete_sensitivity", "what_changed": "The excess and obsolete inventory sensitivity is restated with a FY2026 figure. Separately, the 8-K cash flow statement (8k_2_02:53) has a new 'Inventory obsolescence impairment' line for FY2026 with a dash for FY2025. No note prose explains that charge.", "account": "inventory reserve; cost of revenues", "expected_direction": "none", "horizon": "12 months", "quote": "During fiscal year 2026 and fiscal year 2025, a change of 10% for excess and obsolete materials, based on product demand and production requirements from our customers, would have affected our net income by approximately $0.7 million and $0.6 million, respectively.", "paragraph_id": "0001408710-26-000028:mdna:87", "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_inventory_build_for_next_quarter_demand", "what_changed": "MD&A says inventories increased to support higher demand in the next quarter, and that this drove lower operating cash flow. It also says payables rose in line with inventory volume. The prose implies the inventory turns into Q1 FY2027 revenue.", "account": "inventories", "expected_direction": "up", "horizon": "this quarter", "quote": "an increase in inventories to support higher demand in the next quarter", "paragraph_id": "0001408710-26-000028:mdna:142", "explanation": true }
```

```json
{ "id": "narrative_signs_of_operating_pressure_receivables_rise_from_collection_timing", "what_changed": "MD&A says trade receivables increased because of the timing of collection, and that this also lowered operating cash flow. The prose implies a timing effect that should reverse when collections arrive.", "account": "trade accounts receivable", "expected_direction": "up", "horizon": "this quarter", "quote": "an increase in trade receivables due to timing of collection", "paragraph_id": "0001408710-26-000028:mdna:142", "explanation": true }
```

```json
{ "id": "liquidity_and_capital_purchase_obligations_stated", "what_changed": "A new year-end amount for purchase obligations and other commitments. The Q3 and Q2 10-Qs stated $2.74 billion and $1.94 billion (note_history:2). The policy text says these orders can generally be cancelled or rescheduled and are expected to be fulfilled within one year.", "account": "purchase obligations; inventories; trade accounts payable", "expected_direction": "up", "horizon": "12 months", "quote": "As of June 26, 2026, the Company had purchase obligations and other commitments to third parties of $3.15 billion.", "paragraph_id": "0001408710-26-000028:notes:307", "explanation": false }
```

```json
{ "id": "liquidity_and_capital_capital_expenditure_commitments_stated", "what_changed": "A new year-end amount for capital expenditure commitments to third parties. The Q3 and Q2 10-Qs stated $164.7 million and $193.7 million (note_history:3).", "account": "property, plant and equipment; fixed assets payable", "expected_direction": "up", "horizon": "12 months", "quote": "As of June 26, 2026, the Company had total capital expenditure commitments to third parties of $108.1 million.", "paragraph_id": "0001408710-26-000028:notes:310", "explanation": false }
```

```json
{ "id": "liquidity_and_capital_chonburi_construction_remaining_balance", "what_changed": "MD&A states the remaining balance on the Chonburi building contract (total about $132.5 million, THB 4.45 billion) as of June 26, 2026. It also says current capacity is enough for 'at least the next few quarters'.", "account": "property, plant and equipment", "expected_direction": "up", "horizon": "12 months", "quote": "As of June 26, 2026, the remaining balance was approximately $39.7 million.", "paragraph_id": "0001408710-26-000028:mdna:138", "explanation": false }
```

```json
{ "id": "liquidity_and_capital_capex_expected_to_increase_with_california_building", "what_changed": "MD&A now says FY2027 capital expenditures will increase. The reasons given are buying a manufacturing building in California, the Pathum Thani campus, and equipment for added capacity.", "account": "capital expenditures; property, plant and equipment", "expected_direction": "up", "horizon": "12 months", "quote": "We expect our capital expenditures for fiscal year 2027 to increase compared to fiscal year 2026, mainly due to the purchase of a new manufacturing building in California", "paragraph_id": "0001408710-26-000028:mdna:153", "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_united_states_facility_acquired", "what_changed": "New subsequent event: on July 27, 2026, after year end, the company bought a manufacturing facility in the United States for a stated price. This matches the California building in the MD&A capex outlook.", "account": "property, plant and equipment; cash", "expected_direction": "up", "horizon": "next quarter", "quote": "On July 27, 2026, the Company completed the acquisition of a manufacturing facility in the United States, for a total purchase price of $76.9 million.", "paragraph_id": "0001408710-26-000028:notes:353", "explanation": false }
```

```json
{ "id": "liquidity_and_capital_baht_term_loan_drawn_after_year_end", "what_changed": "New: on August 17, 2026, the 2019 Bank of Ayudhya facility was amended to THB 2.61 billion plus $100.0 million, maturing in 2044 (notes:314). The 8-K (8k_body:2) calls this an extension of the 'drawdown period'. A THB 2.50 billion term loan was drawn the same day to fund capex. At year end MD&A states 'no outstanding debt' (mdna:134), so the company starts carrying debt after the balance sheet date.", "account": "borrowings; interest expense", "expected_direction": "up", "horizon": "next quarter", "quote": "in the original principal amount of Thai baht 2.50 billion (approximately $75.0 million based on the applicable exchange rate as of August 17, 2026)", "paragraph_id": "0001408710-26-000028:notes:315", "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_parent_guarantee_and_bank_judgment_default", "what_changed": "The 8-K says the parent company guarantees the term loan (8k_body:3). It also lists the events of default: cross default, plus any event that the Bank judges likely to have a material adverse effect. The terms add negative covenants on liens, asset disposals, debt and acquisitions. None of this guarantee or default language appears in the notes.", "account": "guarantees; borrowings", "expected_direction": "none", "horizon": "12 months", "quote": "the occurrence of any event or series of events that in the opinion of the Bank has or is reasonably likely to have a material adverse effect", "paragraph_id": "0001408710-26-000026:8k_body:4", "explanation": false }
```

```json
{ "id": "across_documents_floating_rate_borrowing_statement_with_no_debt", "what_changed": "The financial instruments note says the company borrows at floating rates to finance operations. MD&A says there was no outstanding debt at June 26, 2026, and the 2023 facility shows nothing outstanding (notes:319). The text conflicts at year end. It may become true with the August term loan.", "account": "borrowings; interest expense", "expected_direction": "none", "horizon": "this quarter", "quote": "The Company borrows at floating rates of interest to finance its operations.", "paragraph_id": "0001408710-26-000028:notes:349", "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_casix_retrial_accepted", "what_changed": "New: the plaintiffs appealed to the PRC Supreme Court. On July 30, 2026 that court accepted the RMB 400 million unjust-enrichment case against Casix for retrial. The company says this is not a ruling on the merits and that it cannot quantify the potential liability (notes:326). A matter that had been dismissed is open again.", "account": "contingent liabilities; accrued expenses", "expected_direction": "none", "horizon": "12 months", "quote": "rendered a ruling accepting the case for retrial", "paragraph_id": "0001408710-26-000028:notes:325", "explanation": false }
```

```json
{ "id": "across_documents_casix_litigation_removed_from_quarterly_report_during_appeal", "what_changed": "The note change history shows the Q3 10-Q, filed 2026-05-05, removed the whole Casix litigation section (note_history:9-11). The 10-K says the plaintiffs had already appealed to the PRC Supreme Court in April 2026, before that 10-Q was filed. The quarterly report left out a live appeal.", "account": "contingent liabilities", "expected_direction": "none", "horizon": "this quarter", "quote": "In April 2026, the Plaintiffs appealed", "paragraph_id": "0001408710-26-000028:notes:325", "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_tariff_refund_not_recognized", "what_changed": "This matter is new since the FY2025 10-K; it first appeared in the Q3 10-Q (note_history:7). Possible refunds of IEEPA tariffs after the February 2026 Supreme Court ruling were assessed under a loss-recovery model, and no receivable was recorded. Any refund would be a future gain.", "account": "other receivables; cost of revenues", "expected_direction": "none", "horizon": "12 months", "quote": "has not recorded a receivable because recovery is not considered probable", "paragraph_id": "0001408710-26-000028:notes:328", "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_thai_bank_guarantees_restated", "what_changed": "The Thailand bank guarantee amount for June 26, 2026 is a new figure. The Q3 10-Q stated THB 77.3 million at March 27, 2026 (note_history:1). The China RMB 4.8 million guarantee is still backed by $0.7 million of cash collateral, and the balance sheet now has a new 'Long-term restricted cash' line (8k_2_02:47).", "account": "guarantees; restricted cash", "expected_direction": "none", "horizon": "this quarter", "quote": "Thai baht 83.3 million and Thai baht 75.7 million, respectively", "paragraph_id": "0001408710-26-000028:notes:304", "explanation": false }
```

```json
{ "id": "revenue_recognition_customer_warrant_contra_revenue", "what_changed": "The annual reduction to revenue from the Amazon customer warrant is now stated. Vested, unexercised warrant shares are restated as of June 26, 2026 (notes:284). The diluted share count now includes incremental shares from the warrant (notes:172). Amazon appears as a 10% customer for the first time (notes:343). Vesting is tied to Amazon's payments, so the prose implies continuing reductions to revenue.", "account": "revenues", "expected_direction": "down", "horizon": "12 months", "quote": "the Company recognized $4.8 million and $4.1 million, respectively, as a reduction to revenue", "paragraph_id": "0001408710-26-000028:notes:129", "explanation": false }
```

```json
{ "id": "revenue_recognition_new_ten_percent_customers_listed", "what_changed": "The significant-customer table now lists Nokia and Amazon with FY2026 percentages and asterisks (under 10%) for prior years. Cisco and NVIDIA remain listed.", "account": "revenues (customer concentration)", "expected_direction": "none", "horizon": "this quarter", "quote": "Amazon.com, Inc. | 10.5 | % |", "paragraph_id": "0001408710-26-000028:notes:343", "explanation": false }
```

```json
{ "id": "revenue_recognition_receivable_concentration_shift", "what_changed": "The receivables concentration table marks NVIDIA with an asterisk (under 10%) at June 26, 2026, where it had a percentage at June 27, 2025. Amazon is added with a percentage. Nokia and Cisco remain.", "account": "trade accounts receivable", "expected_direction": "none", "horizon": "this quarter", "quote": "NVIDIA Corporation | * |", "paragraph_id": "0001408710-26-000028:notes:346", "explanation": false }
```

```json
{ "id": "estimates_and_discretion_warranty_allowance_now_quantified", "what_changed": "A warranty cost allowance is quantified for FY2026. Earlier years are described as immaterial.", "account": "warranty provision; cost of revenues", "expected_direction": "up", "horizon": "12 months", "quote": "Warranty cost allowances of $0.4 million were recognized in the consolidated statements of operations and comprehensive income for the year ended June 26, 2026.", "paragraph_id": "0001408710-26-000028:notes:95", "explanation": false }
```

```json
{ "id": "across_documents_severance_policy_says_non_current_but_current_portion_shown", "what_changed": "The policy text still says severance liabilities sit under non-current liabilities. The severance note (notes:250) and the balance sheet (8k_2_02:47) now show a new current portion at June 26, 2026, with a dash for the prior year.", "account": "severance liabilities", "expected_direction": "none", "horizon": "this quarter", "quote": "consolidated balance sheet under non-current liabilities", "paragraph_id": "0001408710-26-000028:notes:106", "explanation": false }
```

```json
{ "id": "across_documents_excess_inventory_sale_revenue_versus_cost_offset", "what_changed": "The revenue note says excess or obsolete inventory sold back to customers is recognized as revenue on shipment. MD&A (mdna:34) says the same shipments are recognized as an offset against cost of revenue. The two documents describe different line-item treatment for the same transactions.", "account": "revenues; cost of revenues", "expected_direction": "none", "horizon": "this quarter", "quote": "The excess or obsolete inventory is shipped to the customer and revenue is recognized upon shipment.", "paragraph_id": "0001408710-26-000028:notes:83", "explanation": false }
```

```json
{ "id": "earnings_quality_hedge_losses_to_reclassify_into_earnings", "what_changed": "The text now states that a loss sitting in AOCI on designated Thai baht forward contracts will be reclassified into earnings within 12 months. These reclassifications go mainly to cost of revenues (notes:210).", "account": "cost of revenues; AOCI", "expected_direction": "up", "horizon": "12 months", "quote": "the amount in AOCI that is expected to be reclassified into earnings within 12 months as loss was $5.6 million", "paragraph_id": "0001408710-26-000028:notes:207", "explanation": false }
```

```json
{ "id": "estimates_and_discretion_performance_units_not_expected_to_vest", "what_changed": "New footnote: some outstanding performance share units are left out of diluted EPS because management currently judges they will not vest. The FY2026 row has a number and prior years have dashes. The PSU rollforward also shows a FY2026 forfeiture (notes:276).", "account": "share-based compensation; diluted shares", "expected_direction": "none", "horizon": "12 months", "quote": "not expected to vest based on the Company", "paragraph_id": "0001408710-26-000028:notes:173", "explanation": false }
```

```json
{ "id": "controls_audit_and_filings_revenue_timing_critical_audit_matter", "what_changed": "The auditor's report carries one critical audit matter, on identifying contract terms that affect when revenue is recognized. It includes cut-off testing of sales just before and after year end (auditors_report:19) and states FY2026 revenue. The opinions are unqualified, and ICFR is effective with no Q4 changes (item_9a:5, :10). The prior report's text is not in the input, so whether this CAM is new is insufficient to judge.", "account": "revenues", "expected_direction": "none", "horizon": "this quarter", "quote": "The management applies judgment in identifying and evaluating any terms and conditions when the Company has an enforceable right to payment.", "paragraph_id": "0001408710-26-000028:auditors_report:17", "explanation": false }
```

```json
{ "id": "results_against_expectations_fourth_quarter_revenue_above_guidance", "what_changed": "The release says Q4 revenue was a record and above the company's own guidance range. The CEO describes 'accelerating growth' (8k_2_02:8). The input does not give the guidance range.", "account": "revenues", "expected_direction": "up", "horizon": "this quarter", "quote": "Record Fourth Quarter Revenue Exceeds Guidance Range", "paragraph_id": "0001408710-26-000026:8k_2_02:5", "explanation": false }
```

```json
{ "id": "results_against_expectations_first_quarter_revenue_guidance_issued", "what_changed": "New Q1 FY2027 guidance on revenue and GAAP and non-GAAP EPS. The CEO frames the outlook as continued growth ('durability in the growth trends', 8k_2_02:8). This is the expectation the next quarter's results will be judged against.", "account": "revenues", "expected_direction": "up", "horizon": "next quarter", "quote": "Fabrinet expects first quarter revenue to be in the range of $1.375 billion to $1.425 billion.", "paragraph_id": "0001408710-26-000026:8k_2_02:27", "explanation": false }
```

```json
{ "id": "results_against_expectations_sga_expected_to_increase", "what_changed": "MD&A expects FY2027 SG&A to increase, driven by R&D, IT hardware and compensation-related expenses. The August 2026 executive raises and grants in the 8-K are consistent with the compensation part.", "account": "selling, general and administrative expenses", "expected_direction": "up", "horizon": "12 months", "quote": "In fiscal year 2027, we expect our SG&A expenses will increase compared with our fiscal year 2026 SG&A expenses, mainly due to increases in research and development expenses, investments in information technology hardware, and compensation-related expenses.", "paragraph_id": "0001408710-26-000028:mdna:42", "explanation": false }
```

```json
{ "id": "results_against_expectations_geographic_mix_outlook_outside_north_america", "what_changed": "Now on the ship-to basis, MD&A says the non-North America share fell in FY2026 because North America customers grew. It expects the non-North America share to increase again, based on customer forecasts.", "account": "revenue by geographic area", "expected_direction": "up", "horizon": "12 months", "quote": "we expect that the portion of our future revenues attributable to customers in regions outside of North America will increase as compared with the portion of revenues attributable to such customers during fiscal year 2026", "paragraph_id": "0001408710-26-000028:mdna:30", "explanation": false }
```

```json
{ "id": "liquidity_and_capital_lower_average_cash_and_rates", "what_changed": "MD&A explains lower interest income by a lower average cash and short-term investment balance and a lower average rate. It states that year-end cash, cash equivalents and short-term investments came with no outstanding debt (mdna:134).", "account": "interest income; cash and short-term investments", "expected_direction": "down", "horizon": "12 months", "quote": "The decrease was primarily due to a lower average cash balance and short-term investment of $872.0 million in fiscal year 2026", "paragraph_id": "0001408710-26-000028:mdna:112", "explanation": false }
```

```json
{ "id": "across_documents_prior_year_margin_percentages_stated_differently", "what_changed": "The FY2025 ratios are written differently in different places. For the FY2025 net income margin, the MD&A prose figure is not the one in the MD&A percent table (mdna:98). For the FY2025 GAAP operating margin, the MD&A prose (mdna:111) and percent table do not match the 8-K reconciliation (8k_2_02:62). These are text-to-text mismatches only, with no amounts recomputed. Left for the supervisor to reconcile.", "account": "net income; operating income (ratios)", "expected_direction": "none", "horizon": "this quarter", "quote": "or 9.7% of revenues, for fiscal year 2025", "paragraph_id": "0001408710-26-000028:mdna:116", "explanation": false }
```

```json
{ "id": "earnings_quality_executive_stretch_performance_units_on_revenue_and_non_gaap_margin", "what_changed": "The FY2027 equity grants add a new 'Stretch PSU' award, the same size as the regular PSUs. It vests on cumulative FY2027-FY2028 revenue and non-GAAP operating margin goals set 5% above the PSU targets. The notes (notes:272) describe PSU vesting only from 0% to 100%. Executive pay is now more heavily tied to revenue and non-GAAP operating margin.", "account": "share-based compensation", "expected_direction": "up", "horizon": "12 months", "quote": "The Company must exceed the PSU Revenue Target or the PSU Operating Margin Target in order for any of the Stretch PSUs to vest.", "paragraph_id": "0001408710-26-000026:8k_body:76", "explanation": false }
```

```json
{ "id": "earnings_quality_executive_salary_increase_and_bonus_plan", "what_changed": "The Compensation Committee raised named executive officer base salaries, effective June 27, 2026. It adopted a FY2027 cash bonus plan paying up to 120% of target, weighted 50/50 on revenue and non-GAAP operating margin (8k_body:8, :24).", "account": "selling, general and administrative expenses (compensation)", "expected_direction": "up", "horizon": "12 months", "quote": "approved an increase to the annual base salaries", "paragraph_id": "0001408710-26-000026:8k_body:26", "explanation": false }
```

Count: 41 items. Items with `explanation` true: 3 (inventory build, receivables timing, Israel valuation allowance). Insufficient: 1 (whether the critical audit matter is new; the prior auditor's report is not in the input).

## Paragraphs without an item

Ids drop the accession prefix. `notes`, `mdna`, `auditors_report` and `item_9a` belong to 0001408710-26-000028. `8k_2_02` and `8k_body` belong to 0001408710-26-000026. "covered" means the paragraph is cited inside the named item.

- notes:1 — proxy incorporation boilerplate
- notes:2 — cybersecurity process boilerplate
- notes:3 — cybersecurity framework boilerplate
- notes:4 — cybersecurity governance boilerplate
- notes:5 — cybersecurity tools boilerplate
- notes:6 — no material breach; boilerplate
- notes:7 — cross-reference
- notes:8 — board oversight boilerplate
- notes:9 — officer credentials boilerplate
- notes:10 — escalation boilerplate
- notes:11 — heading
- notes:12 — fiscal year, date rolled forward
- notes:13 — consolidation boilerplate
- notes:14 — heading
- notes:15 — use-of-estimates boilerplate, no change signalled
- notes:16 — heading
- notes:17 — functional currency boilerplate
- notes:18 — FX policy boilerplate
- notes:19 — translation policy boilerplate
- notes:20 — heading
- notes:21 — cash policy boilerplate
- notes:22 — heading
- notes:23 — investment maturity policy boilerplate
- notes:24 — AFS/HTM policy boilerplate
- notes:25 — CECL policy boilerplate
- notes:26 — AFS impairment policy boilerplate
- notes:27 — impairment conditions boilerplate
- notes:28 — impairment policy boilerplate
- notes:29 — impairment policy boilerplate
- notes:30 — heading
- notes:31 — receivables allowance policy boilerplate
- notes:32 — heading
- notes:33 — contract asset policy boilerplate
- notes:34 — heading
- notes:35 — contract liability policy boilerplate
- notes:36 — heading
- notes:37 — inventory policy boilerplate
- notes:38 — heading
- notes:39 — heading
- notes:40 — lease policy boilerplate
- notes:41 — lease policy boilerplate
- notes:42 — short-term lease policy boilerplate
- notes:43 — heading
- notes:44 — PP&E policy boilerplate
- notes:45 — useful-lives table, no change signalled
- notes:46 — construction-in-process policy boilerplate
- notes:47 — disposal policy boilerplate
- notes:48 — impairment review policy boilerplate
- notes:49 — heading
- notes:50 — intangibles policy boilerplate
- notes:51 — intangibles impairment boilerplate
- notes:52 — heading
- notes:53 — treasury share policy boilerplate
- notes:54 — heading
- notes:55 — borrowing cost policy boilerplate
- notes:56 — capitalization rate policy boilerplate
- notes:57 — heading
- notes:58 — fair value definition boilerplate
- notes:59 — Level 1 definition
- notes:60 — Level 2 definition
- notes:61 — Level 3 definition
- notes:62 — market approach boilerplate
- notes:63 — carrying amount boilerplate
- notes:64 — heading
- notes:65 — derivative presentation boilerplate
- notes:66 — classification boilerplate
- notes:67 — classification boilerplate
- notes:68 — cash flow classification boilerplate
- notes:69 — hedge accounting boilerplate
- notes:70 — cash flow hedge boilerplate
- notes:71 — counterparty credit boilerplate
- notes:72 — heading
- notes:73 — credit risk boilerplate
- notes:74 — deposits boilerplate
- notes:75 — counterparties boilerplate
- notes:76 — customer credit monitoring boilerplate
- notes:77 — heading
- notes:78 — five-step revenue policy boilerplate
- notes:79 — performance obligation boilerplate
- notes:80 — heading
- notes:81 — point-in-time policy, no change signalled
- notes:82 — customer-requested warehouse holding policy, no change signalled
- notes:84 — returns/warranty term policy, no change signalled
- notes:85 — rebates/variable consideration policy, no change signalled
- notes:86 — heading
- notes:87 — services policy boilerplate
- notes:88 — service revenue amounts only
- notes:89 — heading
- notes:90 — no contract costs; boilerplate
- notes:91 — heading
- notes:92 — shipping policy boilerplate
- notes:93 — heading
- notes:94 — warranty policy text; amount covered by estimates_and_discretion_warranty_allowance_now_quantified
- notes:96 — heading
- notes:97 — share-based compensation policy boilerplate
- notes:98 — heading
- notes:99 — warrant policy; covered by revenue_recognition_customer_warrant_contra_revenue
- notes:100 — warrant policy; covered by same
- notes:101 — heading
- notes:102 — contribution plan boilerplate
- notes:103 — heading
- notes:104 — severance entitlement boilerplate
- notes:105 — actuarial method boilerplate
- notes:107 — heading
- notes:108 — annual leave boilerplate
- notes:109 — heading
- notes:110 — tax policy boilerplate
- notes:111 — tax audit policy boilerplate
- notes:112 — valuation allowance policy boilerplate
- notes:113 — uncertain tax position policy boilerplate
- notes:114 — uncertain tax position policy boilerplate
- notes:115 — heading; covered by Raytek items
- notes:116 — new policy; covered by estimates_and_discretion_raytek_observable_price_remeasurement_gain
- notes:117 — new policy; covered by across_documents_no_policy_change_stated_while_new_policy_added
- notes:118 — equity-method assessment; covered by Raytek items
- notes:119 — heading
- notes:120 — ASU 2023-09 adoption; covered by structure_and_disclosure_changes_income_tax_disclosure_standard_adopted
- notes:121 — heading
- notes:122 — ASU 2024-03 not yet adopted; dates only
- notes:123 — heading
- notes:124 — no contract asset impairment; boilerplate
- notes:125 — contract assets immaterial; Q3 said "de minimis", wording only
- notes:126 — contract liability policy boilerplate
- notes:127 — lead-in
- notes:128 — contract liability rollforward; amounts only
- notes:130 — heading
- notes:132 — ship-to attribution; covered by revenue_recognition_geography_basis_moved_to_ship_to
- notes:133 — lead-in
- notes:134 — geography table; amounts only, basis covered
- notes:135 — Cayman footnote boilerplate
- notes:136 — lead-in
- notes:137 — end-market table; amounts only
- notes:138 — definition; covered by structure_and_disclosure_changes_end_market_categories_replaced
- notes:139 — definition; covered by same
- notes:140 — definition; covered by same
- notes:141 — Cayman domicile boilerplate
- notes:143 — statutory rates boilerplate
- notes:144 — lead-in
- notes:145 — pre-tax income table; amounts only
- notes:146 — lead-in
- notes:147 — tax expense table; amounts only
- notes:148 — new disclosure; covered by ASU 2023-09 item
- notes:149 — taxes paid table; amounts only
- notes:151 — new-format rate reconciliation; amounts only, Pillar Two line covered
- notes:152 — lead-in
- notes:153 — old-format reconciliation; amounts only
- notes:154 — Cayman pre-tax amounts only
- notes:155 — income not subject to tax per share; amounts only
- notes:156 — footnote boilerplate
- notes:157 — lead-in
- notes:158 — deferred tax table; amounts only
- notes:159 — lead-in
- notes:160 — valuation allowance rollforward; covered by Israel valuation allowance item
- notes:161 — U.K. valuation allowance history; prior periods, no change
- notes:162 — U.K. valuation allowance history; prior periods, no change
- notes:164 — Thailand unremitted earnings; amounts only
- notes:165 — China withholding deferred tax liability; amounts only
- notes:166 — heading
- notes:168 — lead-in
- notes:169 — uncertain tax position rollforward; covered by estimates_and_discretion_uncertain_tax_position_additions
- notes:170 — EPS method boilerplate
- notes:171 — lead-in
- notes:172 — EPS table; amounts only, warrant shares covered
- notes:174 — lead-in
- notes:175 — investments table; amounts only
- notes:176 — deposit rate; amounts only
- notes:177 — certificates of deposit; amounts only
- notes:178 — no held-to-maturity securities; unchanged
- notes:179 — share of cash held by parent; amounts only
- notes:180 — lead-in
- notes:181 — maturity table; amounts only
- notes:182 — no AFS impairment; boilerplate
- notes:183 — lead-in
- notes:184 — Raytek rollforward; covered by Raytek remeasurement item
- notes:186 — measurement alternative; covered by Raytek remeasurement item
- notes:188 — fair value definition boilerplate
- notes:189 — Level 2 definition
- notes:190 — Level 3 definition
- notes:191 — lead-in
- notes:192 — fair value table; amounts only
- notes:193 — fair value table; amounts only
- notes:194 — notional; amounts only
- notes:195 — notional; amounts only
- notes:196 — notional; amounts only
- notes:197 — notional; amounts only
- notes:198 — heading
- notes:199 — hedging purpose boilerplate
- notes:200 — counterparty boilerplate
- notes:201 — heading
- notes:202 — forward contract boilerplate
- notes:203 — dual-purpose hedge policy, no change signalled
- notes:204 — non-designated contracts boilerplate
- notes:205 — contract count and notional; amounts only
- notes:206 — prior-year count and notional; amounts only
- notes:208 — non-designated gain/loss; amounts only
- notes:209 — lead-in
- notes:210 — hedge impact table; amounts only
- notes:211 — heading
- notes:212 — lead-in
- notes:213 — derivative fair value table; amounts only
- notes:214 — gross presentation boilerplate
- notes:215 — lead-in
- notes:216 — line-item mapping boilerplate
- notes:217 — heading
- notes:218 — receivables table; amounts only
- notes:219 — lead-in
- notes:220 — allowance rollforward; amounts only, no prose cause given
- notes:221 — heading
- notes:222 — inventory table; amounts only
- notes:223 — lease description boilerplate
- notes:224 — lead-in
- notes:225 — lease maturity table; amounts only
- notes:226 — current portion; amounts only
- notes:227 — straight-line boilerplate
- notes:228 — rent expense; amounts only
- notes:229 — rent expense; amounts only
- notes:230 — lead-in
- notes:231 — lease term and discount rate; amounts only
- notes:232 — lead-in
- notes:233 — lease cash flows; amounts only
- notes:234 — lead-in
- notes:235 — PP&E table; amounts only
- notes:236 — depreciation; amounts only
- notes:237 — write-offs and impairment reserve; amounts only
- notes:238 — lead-in
- notes:239 — software table; amounts only
- notes:240 — amortization; amounts only
- notes:241 — lead-in
- notes:242 — remaining life; amounts only
- notes:243 — lead-in
- notes:244 — amortization schedule; amounts only
- notes:245 — lead-in
- notes:246 — severance rollforward; amounts only
- notes:247 — lead-in
- notes:248 — severance schedule; amounts only
- notes:249 — lead-in
- notes:250 — current/non-current split; covered by across_documents_severance_policy_says_non_current_but_current_portion_shown
- notes:251 — lead-in
- notes:252 — accumulated benefit obligation; amounts only
- notes:253 — lead-in
- notes:254 — lead-in
- notes:255 — actuarial assumptions; amounts only
- notes:256 — heading
- notes:257 — grant-date fair value boilerplate
- notes:258 — lead-in
- notes:259 — share-based compensation by award; amounts only
- notes:260 — lead-in
- notes:261 — share-based compensation by line; amounts only
- notes:262 — none capitalized; unchanged
- notes:263 — heading
- notes:264 — 2020 Plan history; unchanged
- notes:265 — 2017 Inducement Plan history; unchanged
- notes:266 — definition
- notes:267 — lead-in
- notes:268 — awards outstanding; amounts only
- notes:269 — heading
- notes:270 — boilerplate
- notes:271 — RSU vesting terms; unchanged
- notes:272 — PSU terms; covered by earnings_quality_executive_stretch_performance_units_on_revenue_and_non_gaap_margin
- notes:273 — lead-in
- notes:274 — RSU activity; amounts only
- notes:275 — lead-in
- notes:276 — PSU activity; amounts only, forfeiture covered
- notes:277 — vested fair value; amounts only
- notes:278 — unrecognized compensation; amounts only
- notes:279 — shares withheld; amounts only
- notes:280 — warrant terms; unchanged since issuance
- notes:281 — warrant vesting terms; unchanged
- notes:282 — warrant fair value; unchanged
- notes:283 — Black-Scholes inputs; unchanged
- notes:284 — vested warrant shares; covered by revenue_recognition_customer_warrant_contra_revenue
- notes:285 — contribution plan heading/boilerplate
- notes:286 — provident fund; amounts only
- notes:287 — 401(k); amounts only
- notes:288 — heading
- notes:289 — incentive plan description; wording only
- notes:290 — bonus amounts only
- notes:291 — heading
- notes:292 — authorized capital; unchanged
- notes:293 — shares issued; amounts only
- notes:294 — shares issued; amounts only
- notes:295 — shares issued; amounts only
- notes:296 — fully paid; boilerplate
- notes:297 — buyback authorization history; no new increase
- notes:298 — FY2026 repurchases and remaining authorization; amounts only
- notes:299 — lead-in
- notes:300 — AOCI table; amounts only
- notes:301 — lead-in
- notes:302 — reclassification table; amounts only
- notes:303 — heading
- notes:305 — heading
- notes:306 — purchase obligation definition boilerplate
- notes:308 — heading
- notes:309 — Chonburi contract; unchanged, status covered by liquidity_and_capital_chonburi_construction_remaining_balance
- notes:311 — heading
- notes:312 — heading
- notes:313 — 2019 facility history; unchanged
- notes:314 — facility amendment; covered by liquidity_and_capital_baht_term_loan_drawn_after_year_end
- notes:316 — heading
- notes:317 — 2023 facility history; unchanged
- notes:318 — 2023 facility amendment history; unchanged
- notes:319 — nothing outstanding; date rolled forward
- notes:320 — covenant ratios; unchanged
- notes:321 — covenant compliance; date rolled forward
- notes:322 — heading
- notes:323 — Casix complaint history; unchanged
- notes:324 — Casix dismissal history; unchanged
- notes:326 — liability cannot be quantified; covered by related_parties_contingencies_and_subsequent_events_casix_retrial_accepted
- notes:327 — heading
- notes:329 — heading
- notes:330 — indemnification law boilerplate
- notes:331 — indemnification agreement boilerplate
- notes:332 — restructuring policy boilerplate
- notes:333 — no restructuring liability; amounts only
- notes:334 — single segment boilerplate
- notes:335 — CODM boilerplate
- notes:336 — lead-in
- notes:337 — segment table; amounts only
- notes:338 — cross-reference
- notes:339 — lead-in
- notes:340 — long-lived assets by country; amounts only
- notes:341 — heading
- notes:342 — lead-in
- notes:344 — footnote
- notes:345 — lead-in
- notes:347 — footnote
- notes:348 — heading
- notes:350 — forward contract boilerplate
- notes:351 — heading
- notes:352 — FX risk boilerplate
- mdna:1 — heading
- mdna:2 — forward-looking bullet boilerplate
- mdna:3 — forward-looking bullet boilerplate
- mdna:4 — forward-looking bullet boilerplate
- mdna:5 — covered by results_against_expectations_geographic_mix_outlook_outside_north_america
- mdna:6 — covered by results_against_expectations_sga_expected_to_increase
- mdna:7 — employee cost bullet boilerplate
- mdna:8 — capex bullet; covered by liquidity_and_capital_capex_expected_to_increase_with_california_building
- mdna:9 — forward-looking bullet boilerplate
- mdna:10 — forward-looking bullet boilerplate
- mdna:11 — forward-looking bullet boilerplate
- mdna:12 — forward-looking bullet boilerplate
- mdna:13 — forward-looking bullet boilerplate
- mdna:14 — forward-looking bullet boilerplate
- mdna:15 — forward-looking bullet boilerplate
- mdna:16 — forward-looking bullet boilerplate
- mdna:17 — forward-looking bullet boilerplate
- mdna:18 — forward-looking bullet boilerplate
- mdna:19 — heading
- mdna:20 — cross-reference
- mdna:21 — heading
- mdna:22 — fiscal year; date rolled forward
- mdna:23 — heading
- mdna:24 — pricing narrative boilerplate
- mdna:25 — customer concentration risk boilerplate
- mdna:26 — customer leverage boilerplate
- mdna:27 — covered by the geography and end-market items
- mdna:28 — heading
- mdna:29 — covered by revenue_recognition_geography_basis_moved_to_ship_to
- mdna:31 — lead-in
- mdna:32 — geography percent table; amounts only
- mdna:33 — heading
- mdna:34 — contract terms; cited in across_documents_excess_inventory_sale_revenue_versus_cost_offset
- mdna:35 — heading
- mdna:36 — material cost boilerplate
- mdna:37 — employee cost boilerplate
- mdna:38 — infrastructure cost boilerplate
- mdna:39 — bonus amounts only
- mdna:40 — share-based compensation amounts only
- mdna:41 — heading
- mdna:43 — incentive plan description; date rolled forward
- mdna:44 — bonus amounts only
- mdna:45 — share-based compensation amounts only
- mdna:46 — heading
- mdna:47 — heading
- mdna:48 — FX exposure boilerplate
- mdna:49 — derivative use boilerplate
- mdna:50 — lead-in
- mdna:51 — currency table; amounts only
- mdna:52 — baht composition and forward contracts; amounts only
- mdna:53 — RMB composition boilerplate
- mdna:54 — GBP composition boilerplate
- mdna:55 — non-designated derivative result; amounts only
- mdna:56 — heading
- mdna:57 — PRC rules boilerplate
- mdna:58 — PRC rules boilerplate
- mdna:59 — PRC rules boilerplate
- mdna:60 — PRC rules boilerplate
- mdna:61 — PRC rules boilerplate
- mdna:62 — PRC rules boilerplate
- mdna:63 — PRC rules boilerplate
- mdna:64 — PRC rules boilerplate
- mdna:65 — PRC rules boilerplate
- mdna:66 — PRC rules boilerplate
- mdna:67 — heading
- mdna:68 — Cayman domicile boilerplate
- mdna:69 — tax holidays; covered by earnings_quality_chonburi_tax_exemption_expired
- mdna:70 — statutory rates boilerplate
- mdna:71 — Pillar Two framework; covered by earnings_quality_pillar_two_top_up_tax_recognized
- mdna:72 — UTPR jurisdictions; covered by same
- mdna:74 — heading
- mdna:75 — estimates boilerplate
- mdna:76 — sensitivity boilerplate
- mdna:78 — heading
- mdna:79 — revenue policy boilerplate
- mdna:80 — performance obligation boilerplate
- mdna:81 — revenue judgment boilerplate
- mdna:82 — heading
- mdna:83 — long-lived asset boilerplate
- mdna:84 — heading
- mdna:85 — credit loss boilerplate
- mdna:86 — heading
- mdna:88 — heading
- mdna:89 — deferred tax boilerplate
- mdna:90 — same text as notes:163; covered by estimates_and_discretion_israel_valuation_allowance_added
- mdna:91 — heading
- mdna:92 — new critical policy; covered by Raytek remeasurement item
- mdna:93 — new critical policy; covered by across_documents_no_policy_change_stated_while_new_policy_added
- mdna:94 — heading
- mdna:95 — lead-in
- mdna:96 — results table; amounts only
- mdna:97 — lead-in
- mdna:98 — percent table; cited in across_documents_prior_year_margin_percentages_stated_differently
- mdna:99 — page number
- mdna:101 — end-market table; amounts only
- mdna:102 — definition; covered by end-market item
- mdna:103 — definition; covered by end-market item
- mdna:104 — definition; covered by end-market item
- mdna:105 — heading
- mdna:106 — revenue explanation; amounts with demand drivers named
- mdna:107 — cost of revenues; wording only
- mdna:108 — gross profit; wording only
- mdna:109 — SG&A components; amounts only
- mdna:110 — restructuring; amounts only
- mdna:111 — operating income; cited in margin mismatch item
- mdna:113 — FX gain components; amounts only
- mdna:114 — pre-tax income; amounts only
- mdna:115 — effective tax rate; covered by Pillar Two item
- mdna:117 — OCI components; amounts only
- mdna:118 — heading
- mdna:119 — prior-year comparison, recast categories
- mdna:120 — prior-year comparison
- mdna:121 — prior-year comparison
- mdna:122 — prior-year comparison
- mdna:123 — prior-year comparison
- mdna:124 — prior-year comparison
- mdna:125 — prior-year comparison
- mdna:126 — prior-year comparison
- mdna:127 — prior-year comparison
- mdna:128 — prior-year comparison
- mdna:129 — prior-year comparison
- mdna:130 — prior-year comparison
- mdna:131 — prior-year comparison
- mdna:132 — heading
- mdna:133 — heading
- mdna:134 — no outstanding debt; cited in term loan and floating-rate items
- mdna:135 — deposit rates; amounts only
- mdna:136 — investment policy boilerplate
- mdna:137 — liquidity sufficiency; wording only
- mdna:139 — lead-in
- mdna:140 — cash flow table; amounts only
- mdna:141 — heading
- mdna:143 — heading
- mdna:144 — investing explanation; covered by Raytek and capex items
- mdna:145 — heading
- mdna:146 — financing explanation; amounts only
- mdna:147 — heading
- mdna:148 — heading
- mdna:149 — lease payments; amounts only
- mdna:150 — heading
- mdna:151 — lead-in
- mdna:152 — capex table; amounts only
- mdna:154 — heading
- mdna:155 — cross-reference
- auditors_report:1 — heading
- auditors_report:2 — addressee
- auditors_report:3 — heading
- auditors_report:4 — scope; standard
- auditors_report:5 — unqualified opinions; standard
- auditors_report:6 — heading
- auditors_report:7 — standard
- auditors_report:8 — standard
- auditors_report:9 — standard
- auditors_report:10 — heading
- auditors_report:11 — standard ICFR definition
- auditors_report:12 — page number
- auditors_report:13 — standard limitations
- auditors_report:14 — heading
- auditors_report:15 — standard CAM preamble
- auditors_report:16 — CAM title; covered by controls_audit_and_filings_revenue_timing_critical_audit_matter
- auditors_report:18 — CAM reasoning; covered by same
- auditors_report:19 — CAM procedures; covered by same
- auditors_report:20 — signature
- auditors_report:21 — location
- auditors_report:22 — date
- auditors_report:23 — tenure; unchanged
- auditors_report:24 — page number
- auditors_report:25 — header
- item_9a:1 — heading
- item_9a:2 — heading
- item_9a:3 — disclosure controls effective; standard
- item_9a:4 — heading
- item_9a:5 — no ICFR changes; standard, cited in CAM item
- item_9a:6 — heading
- item_9a:7 — standard
- item_9a:8 — standard
- item_9a:9 — standard
- item_9a:10 — ICFR effective; standard
- 8k_2_02:1 — exhibit header
- 8k_2_02:2 — header
- 8k_2_02:3 — header
- 8k_2_02:4 — title
- 8k_2_02:6 — annual growth headline; amounts only
- 8k_2_02:7 — dateline
- 8k_2_02:8 — CEO quote; cited in the guidance and Q4 results items
- 8k_2_02:9 — heading
- 8k_2_02:10 — heading
- 8k_2_02:11 — amounts only
- 8k_2_02:12 — amounts only
- 8k_2_02:13 — amounts only
- 8k_2_02:14 — heading
- 8k_2_02:15 — amounts only
- 8k_2_02:16 — amounts only
- 8k_2_02:17 — heading
- 8k_2_02:18 — heading
- 8k_2_02:19 — amounts only
- 8k_2_02:20 — amounts only
- 8k_2_02:21 — amounts only
- 8k_2_02:22 — heading
- 8k_2_02:23 — amounts only
- 8k_2_02:24 — amounts only
- 8k_2_02:25 — heading
- 8k_2_02:26 — guidance lead-in
- 8k_2_02:28 — EPS guidance; covered by guidance items
- 8k_2_02:29 — EPS guidance; covered by guidance items
- 8k_2_02:31 — heading
- 8k_2_02:32 — call logistics
- 8k_2_02:33 — webcast logistics
- 8k_2_02:34 — heading
- 8k_2_02:35 — company description boilerplate
- 8k_2_02:36 — heading (no text carried)
- 8k_2_02:37 — heading
- 8k_2_02:38 — non-GAAP purpose; incentive-pay use cited in non-GAAP exclusions item
- 8k_2_02:40 — free cash flow definition boilerplate
- 8k_2_02:41 — non-GAAP limitations boilerplate
- 8k_2_02:42 — contact
- 8k_2_02:43 — contact
- 8k_2_02:44 — contact
- 8k_2_02:45 — header
- 8k_2_02:46 — header
- 8k_2_02:47 — balance sheet; amounts only, new lines cited in severance and guarantee items
- 8k_2_02:48 — header
- 8k_2_02:49 — header
- 8k_2_02:50 — income statement; amounts only
- 8k_2_02:51 — header
- 8k_2_02:52 — header
- 8k_2_02:53 — cash flow statement; amounts only, obsolescence line cited in inventory item
- 8k_2_02:54 — header
- 8k_2_02:55 — header
- 8k_2_02:56 — supplemental cash flow; amounts only
- 8k_2_02:57 — header
- 8k_2_02:58 — header
- 8k_2_02:59 — header
- 8k_2_02:60 — gross margin reconciliation; amounts only
- 8k_2_02:61 — header
- 8k_2_02:62 — operating margin reconciliation; cited in margin mismatch item
- 8k_2_02:63 — header
- 8k_2_02:64 — header
- 8k_2_02:65 — header
- 8k_2_02:66 — net income reconciliation; covered by non-GAAP exclusions item
- 8k_2_02:67 — header
- 8k_2_02:68 — header
- 8k_2_02:69 — free cash flow table; amounts only
- 8k_2_02:70 — header
- 8k_2_02:71 — header
- 8k_2_02:72 — header
- 8k_2_02:73 — guidance reconciliation; covered by earnings_quality_pillar_two_carried_into_guidance_as_excluded_item
- 8k_body:1 — heading
- 8k_body:2 — facility amendment; covered by term loan item
- 8k_body:3 — term loan and parent guarantee; covered by term loan and guarantee items
- 8k_body:5 — incorporation by reference
- 8k_body:6 — heading
- 8k_body:7 — heading
- 8k_body:8 — bonus plan terms; covered by earnings_quality_executive_salary_increase_and_bonus_plan
- 8k_body:9 — table cell
- 8k_body:10 — table cell
- 8k_body:11 — table cell
- 8k_body:12 — table cell
- 8k_body:13 — table cell; amounts only
- 8k_body:14 — table cell; amounts only
- 8k_body:15 — table cell
- 8k_body:16 — table cell; amounts only
- 8k_body:17 — table cell; amounts only
- 8k_body:18 — table cell
- 8k_body:19 — table cell; amounts only
- 8k_body:20 — table cell; amounts only
- 8k_body:21 — table cell
- 8k_body:22 — table cell; amounts only
- 8k_body:23 — table cell; amounts only
- 8k_body:24 — bonus formula; covered by salary and bonus item
- 8k_body:25 — heading
- 8k_body:27 — table cell
- 8k_body:28 — table cell
- 8k_body:29 — table cell
- 8k_body:30 — table cell
- 8k_body:31 — table cell
- 8k_body:32 — table cell
- 8k_body:33 — table cell
- 8k_body:34 — table cell; amounts only
- 8k_body:35 — table cell; amounts only
- 8k_body:36 — table cell; amounts only
- 8k_body:37 — table cell
- 8k_body:38 — table cell
- 8k_body:39 — table cell; amounts only
- 8k_body:40 — table cell; amounts only
- 8k_body:41 — table cell; amounts only
- 8k_body:42 — table cell
- 8k_body:43 — table cell
- 8k_body:44 — table cell; amounts only
- 8k_body:45 — table cell; amounts only
- 8k_body:46 — table cell; amounts only
- 8k_body:47 — table cell
- 8k_body:48 — table cell
- 8k_body:49 — table cell; amounts only
- 8k_body:50 — table cell; amounts only
- 8k_body:51 — table cell; amounts only
- 8k_body:52 — heading
- 8k_body:53 — grant lead-in; covered by stretch PSU item
- 8k_body:54 — table cell
- 8k_body:55 — table cell
- 8k_body:56 — table cell
- 8k_body:57 — table cell
- 8k_body:58 — table cell
- 8k_body:59 — table cell; amounts only
- 8k_body:60 — table cell; amounts only
- 8k_body:61 — table cell; amounts only
- 8k_body:62 — table cell
- 8k_body:63 — table cell; amounts only
- 8k_body:64 — table cell; amounts only
- 8k_body:65 — table cell; amounts only
- 8k_body:66 — table cell
- 8k_body:67 — table cell; amounts only
- 8k_body:68 — table cell; amounts only
- 8k_body:69 — table cell; amounts only
- 8k_body:70 — table cell
- 8k_body:71 — table cell; amounts only
- 8k_body:72 — table cell; amounts only
- 8k_body:73 — table cell; amounts only
- 8k_body:74 — RSU vesting terms boilerplate
- 8k_body:75 — PSU terms; covered by stretch PSU item
- 8k_body:77 — change-in-control treatment boilerplate
