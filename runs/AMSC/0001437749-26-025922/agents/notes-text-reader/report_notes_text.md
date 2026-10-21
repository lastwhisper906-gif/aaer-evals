# AMSC — notes-text reader — 0001437749-26-025922 (10-Q, quarter ended June 30, 2026)

## Input check

- Files read in full: input_8k.md, input_controls.md, input_mdna.md, input_notes.md, input_notes_history.md, input_prior_predictions.md.
- Nothing forbidden was found: no trend table, prices, abnormal returns, short interest, other companies' files, prior probabilities or outcome window. The 8-K exhibit 99.1 carries the release's own statements (income statement, balance sheet, cash flow, non-GAAP reconciliation). I treated these as 8-K body text and did no arithmetic on them.
- Missing from the input: the auditor's report (a 10-Q has none; the controls file carries Item 4 only, despite its title), the Item 1A diff, the Exhibit 21 diff and any Exhibit 10. The release's Forward-Looking Statements heading (8k_2_02:21) has no text under it. The 2026-08-05 8-K lists Item 5.07, but only the Item 2.02 body is present.
- Prior flags: none on record.
- No arithmetic was done. Where two stated figures bear on each other, the item names both and leaves the reconciliation to the numbers reader and the supervisor.

## Items

```json
{ "id": "results_against_expectations_record_orders_utility_mining",
  "what_changed": "The earnings release headline now reports record total orders above $130 million, attributed to utility-sector mining developments. The CEO quote (8k_2_02:11) adds traditional energy markets and describes a 12-month backlog 'exceeding $300 million'. The MD&A business description now names the materials and mining sector among the markets served (mdna:4). The 10-Q gives remaining performance obligations (notes:39) but no orders figure, so the orders claim rests on the release alone.",
  "account": "revenue (Grid); remaining performance obligations",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "Reported Record Total Orders Above $130 Million Driven by the Utility-Sector Mining Developments",
  "paragraph_id": "0001437749-26-025921:8k_2_02:5",
  "explanation": false }
```

```json
{ "id": "across_documents_operating_cash_flow_quadrupled_headline",
  "what_changed": "The release headline says operating cash flow 'nearly quadrupled' to $16 million. MD&A (mdna:56) states $16.0 million for the quarter against $4.1 million a year earlier. It attributes the increase to deferred revenue, inventory, prepaid expenses and the change in fair value of contingent consideration. The multiple is the release's own characterization, and testing it is the numbers reader's job.",
  "account": "net cash provided by operating activities",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Nearly Quadrupled Operating Cash Flow to $16 million",
  "paragraph_id": "0001437749-26-025921:8k_2_02:5",
  "explanation": false }
```

```json
{ "id": "across_documents_revenue_growth_organic_versus_comtrafo",
  "what_changed": "The release says the year-over-year revenue increase came from organic growth and the Comtrafo acquisition. MD&A gives the Grid increase a single driver, 'the addition of Comtrafo revenues' (mdna:21), and gives the Wind increase to ECS shipments (mdna:22). Notes:24 states that Comtrafo contributed $19.4 million of revenue. The two documents describe the Grid driver differently. Whether legacy Grid grew is for the numbers reader.",
  "account": "revenue (Grid, excluding Comtrafo)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "The year-over-year increase was driven by organic growth and the acquisition of Comtrafo.",
  "paragraph_id": "0001437749-26-025921:8k_2_02:8",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_second_half_gross_margin_improvement",
  "what_changed": "New management statement: the company is 'well positioned for gross margin improvement in the second half of the fiscal year'. Under the company's fiscal-year convention (mdna:9), that means the quarters ending December 31, 2026 and March 31, 2027. In the same filing, the current quarter's gross margin is stated as decreased on product mix and Comtrafo purchase accounting (mdna:24). The inventory step-up is stated as fully recognized (notes:15), while Comtrafo backlog amortization continues to be charged to cost of revenues (notes:17).",
  "account": "gross margin",
  "expected_direction": "up",
  "horizon": "second half of fiscal 2026 (quarters ending December 31, 2026 and March 31, 2027)",
  "quote": "believe we are well positioned for gross margin improvement in the second half of the fiscal year",
  "paragraph_id": "0001437749-26-025921:8k_2_02:11",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_second_quarter_guidance_assumes_no_contingent_consideration_change",
  "what_changed": "New outlook for the quarter ending September 30, 2026: revenue to exceed $85.0 million; GAAP net income to exceed $1.0 million ($0.02 per share); non-GAAP net income to exceed $8.0 million ($0.17 per share). The GAAP figure assumes no change in the fair value of contingent consideration. The forecast reconciliation (8k_2_02:40) adds back stock-based compensation of 6.3 and amortization of 0.7 (millions), on 46.5 million shares. MD&A (mdna:46) says the current quarter's net income increase was driven primarily by the contingent consideration gain, which the guidance assumes away. Comparing the guided levels with the reported quarter is the numbers reader's job.",
  "account": "revenue; net income; non-GAAP net income",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "net income for the second quarter of fiscal 2026 is expected to exceed $1.0 million, or $0.02 per share",
  "paragraph_id": "0001437749-26-025921:8k_2_02:14",
  "explanation": false }
```

```json
{ "id": "controls_audit_and_filings_disclosure_controls_not_effective",
  "what_changed": "Item 4 now concludes that disclosure controls and procedures were not effective as of June 30, 2026. The stated cause is the material weakness disclosed in the 10-K for the year ended March 31, 2026, filed May 27, 2026. The prior period's Item 4 is not in the input. The text dates the identification of the weakness to the fourth quarter of fiscal 2025, during preparation of the 10-K, which is after the prior 10-Q.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "this quarter and until remediation is reported",
  "quote": "our Chief Executive Officer and Chief Financial Officer have concluded that our disclosure controls and procedures were not effective at the reasonable assurance level as of June 30, 2026",
  "paragraph_id": "0001437749-26-025922:item_4_controls:3",
  "explanation": false }
```

```json
{ "id": "controls_audit_and_filings_material_weakness_comtrafo_purchase_and_fair_value_accounting",
  "what_changed": "The material weakness is now described. Controls over the preparation and review of the initial purchase accounting, and of the continuing fair value accounting, for the Comtrafo acquisition did not operate at an appropriate level of precision, and 'errors went undetected in amounts initially recorded to the opening balance sheet'. By the text, the scope covers the purchase price allocation (goodwill, intangibles, deferred taxes, acquired receivables and inventory). It also covers the recurring Level 3 remeasurement of the earnout. That remeasurement produced this quarter's $8.1 million gain (mdna:33), and the allocation is still described as preliminary (notes:8).",
  "account": "goodwill; contingent consideration; acquired intangibles; deferred tax asset",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "We did not maintain effective internal controls over the preparation and review of the initial purchase accounting and the continuing fair value accounting associated with the Comtrafo Acquisition",
  "paragraph_id": "0001437749-26-025922:item_4_controls:5",
  "explanation": false }
```

```json
{ "id": "controls_audit_and_filings_material_weakness_remediation_in_progress",
  "what_changed": "Remediation is described as initiated, 'primarily through the development and implementation of new levels of precision of management review controls around business acquisitions', plus additional review in the quarter over areas of significant judgement and material balances. No completion date is given. Item 4's 'Other than the foregoing' (item_4_controls:9) presents these steps as the quarter's only changes to internal control over financial reporting.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "which we currently believe will be primarily through the development and implementation of new levels of precision of management review controls around business acquisitions",
  "paragraph_id": "0001437749-26-025922:item_4_controls:6",
  "explanation": false }
```

```json
{ "id": "controls_audit_and_filings_officer_or_director_change_filing_body_not_in_input",
  "what_changed": "insufficient as to content: the 8-K index shows an Item 5.02 filing on 2026-06-02 (departure, election or appointment of directors or officers, or compensatory arrangements). It came after the 10-K that disclosed the material weakness (filed May 27, 2026, per item_4_controls:3). Its body is not in the input, so the person or arrangement involved cannot be read. The 2026-08-05 8-K also lists Item 5.07 (shareholder vote), whose body is likewise absent.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "2026-06-02 0001437749-26-019163",
  "paragraph_id": "input_8k.md item-code index (this line carries no paragraph id)",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_business_description_adds_mining_sector",
  "what_changed": "The MD&A business description now names 'the materials and mining sector' among the sectors served and refers to the 'growing global demand for power'. The release attributes record orders to utility-sector mining developments (8k_2_02:5). The note-level company descriptor was rewritten this period (note_history:3 added, note_history:5 removed). The prior MD&A wording of this paragraph is not in the input.",
  "account": "revenue (Grid)",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "the materials and mining sector",
  "paragraph_id": "0001437749-26-025922:mdna:4",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_business_description_adds_industrial_and_emission_control",
  "what_changed": "MD&A, and the release's About paragraph (8k_2_02:18), now describe 'industrial process, environmental and emission control capabilities' beyond the grid, Navy and wind markets. Nothing else in the input goes with this description. Segments remain Grid and Wind (mdna:6), no acquisition other than Comtrafo is described, and the subsequent events note reports none (notes:160). The Exhibit 21 diff is not in the input, so whether a new subsidiary or business line sits behind this wording cannot be read.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Beyond these markets, we provide industrial process, environmental and emission control capabilities that support operational efficiency across the broader energy infrastructure.",
  "paragraph_id": "0001437749-26-025922:mdna:5",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_macro_risks_tariffs_and_trade_conflicts",
  "what_changed": "insufficient as to the prior wording: this paragraph is carried as changed, but its prior text is not in the input. It now names the following as possible material adverse effects: the wars between Russia and Ukraine and in the Middle East; tariffs, trade restrictions and resulting trade conflicts; labor force availability; sourcing; material delays; and supply chain disruptions. Which of these risks is new cannot be read. The Item 1A diff is not in the input.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "tariffs, trade restrictions and resulting trade conflicts",
  "paragraph_id": "0001437749-26-025922:mdna:11",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_grid_revenue_growth_attributed_to_comtrafo",
  "what_changed": "MD&A states that Grid revenue increased 27% to $76.3 million and attributes the increase to 'the addition of Comtrafo revenues', naming no other driver. The region table now carries a South America Grid line (notes:35). Fuji Bridex, a Grid customer listed at 16% of revenue in the prior-year quarter, is now shown at <10% (notes:41). The release instead calls the total increase organic growth plus the acquisition (8k_2_02:8).",
  "account": "revenue (Grid, excluding Comtrafo)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "was driven by the addition of Comtrafo revenues",
  "paragraph_id": "0001437749-26-025922:mdna:21",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_wind_revenue_from_ecs_shipments",
  "what_changed": "MD&A states that Wind revenue increased 45% to $17.8 million and attributes the increase to additional shipments of electrical control systems (ECS). Inox Wind Limited is listed at 19% of total revenue (notes:41). The region table shows Wind revenue in Asia Pacific and EMEA.",
  "account": "revenue (Wind)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "was driven by additional shipments of electrical control systems",
  "paragraph_id": "0001437749-26-025922:mdna:22",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_gross_margin_decrease_product_mix_and_purchase_accounting",
  "what_changed": "MD&A states gross margin at 26%, against 34% in the prior-year quarter, and cost of revenues as increased 45%. It attributes the margin decrease to a less favorable product mix and to Comtrafo purchase accounting items: $0.5 million of backlog amortization and $0.7 million of inventory step-up, both charged to cost of revenues. The text does not say which products or segments drove the mix.",
  "account": "gross margin; cost of revenues",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "The decrease in gross margin in the three months ended June 30, 2026 was due to a less favorable product mix and the impact of Comtrafo purchase accounting items.",
  "paragraph_id": "0001437749-26-025922:mdna:24",
  "explanation": false }
```

```json
{ "id": "earnings_quality_research_and_development_decrease",
  "what_changed": "MD&A states that R&D decreased 9% to $3.9 million and attributes the decrease to lower stock-based compensation expense and lower outside services expense. The stock-based compensation table (notes:44) breaks out the R&D line.",
  "account": "research and development expense",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "driven primarily by lower stock-based compensation expense and lower outside services expense",
  "paragraph_id": "0001437749-26-025922:mdna:27",
  "explanation": false }
```

```json
{ "id": "earnings_quality_selling_general_and_administrative_increase",
  "what_changed": "MD&A states that SG&A increased 31% to $18.6 million and attributes the increase to Comtrafo expenses, higher overall compensation expense and additional stock-based compensation expense.",
  "account": "selling, general and administrative expense",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "driven primarily by the addition of Comtrafo expenses, higher overall compensation expense, and additional stock-based compensation expense",
  "paragraph_id": "0001437749-26-025922:mdna:29",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_contingent_consideration_gain_attributed_to_forecast_change",
  "what_changed": "MD&A now states that remeasuring the Comtrafo earnout produced an $8.1 million gain from a decrease in its fair value, 'driven by changes in the forecast'. The notes give the same decrease (notes:78, notes:119). They also add a June 30, 2026 column of Monte Carlo inputs (EBITDA risk premium 1.40%, EBITDA volatility 27.5%, credit spread 1.4%, EBITDA discount rate 15.4%, payment delay 89 days, fair value $31.9 million) beside the March 31, 2026 column (notes:117, notes:118). The text does not say which forecast changed or by how much; the earnout depends on Comtrafo EBITDA objectives over three years. In the roll-forward (notes:83), the fiscal year ended March 31, 2026 carries a change in fair value of 4,171 (thousand) that added to the liability. The 'continuing fair value accounting' for Comtrafo is the subject of the open material weakness (item_4_controls:5).",
  "account": "contingent consideration liability; change in fair value of contingent consideration (operating income)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "resulted in a gain of $8.1 million from a decrease in fair value of the contingent consideration driven by changes in the forecast",
  "paragraph_id": "0001437749-26-025922:mdna:33",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_grid_segment_operating_loss",
  "what_changed": "MD&A now states a Grid segment operating loss of $2.2 million, against operating income of $4.2 million in the prior-year quarter. It attributes the change to lower gross margins and Comtrafo purchase accounting expense. All goodwill, including Comtrafo's, is reported in Grid (notes:55, notes:19). The $8.1 million earnout gain is kept outside Grid, in Unallocated (notes:148).",
  "account": "Grid segment operating income",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "Our Grid business segment generated operating loss of $2.2 million in the three months ended June 30, 2026",
  "paragraph_id": "0001437749-26-025922:mdna:37",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_wind_operating_income_from_ecs_sales",
  "what_changed": "MD&A states Wind segment operating income of $3.9 million, against $1.5 million, and attributes it to higher revenues and gross margins from increased ECS sales. In the same filing, consolidated gross margin is stated as decreased on product mix (mdna:24).",
  "account": "Wind segment operating income",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "was due to higher revenues and gross margins from increased sales of ECS units",
  "paragraph_id": "0001437749-26-025922:mdna:38",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_interest_income_attributed_to_higher_cash_balances",
  "what_changed": "MD&A states interest income, net of $1.5 million, against $0.9 million, and attributes the increase to higher cash balances in the current year. The release's cash flow statement (8k_2_02:33) shows end-of-period cash, cash equivalents and restricted cash for both quarters, so the numbers reader can test the attribution.",
  "account": "interest income, net",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "was due to higher cash balances in the current year",
  "paragraph_id": "0001437749-26-025922:mdna:40",
  "explanation": false }
```

```json
{ "id": "earnings_quality_other_expense_from_foreign_currency_fluctuations",
  "what_changed": "MD&A states other expense, net of $0.6 million, against other income, net of $0.3 million, and attributes the change to unfavorable fluctuations in foreign currencies. The company now has Brazilian operations through Comtrafo, an earnout denominated in Brazilian Real (notes:7) and $22.8 million of cash in foreign bank accounts (mdna:54).",
  "account": "other income (expense), net",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "was driven by unfavorable fluctuations in foreign currencies",
  "paragraph_id": "0001437749-26-025922:mdna:42",
  "explanation": false }
```

```json
{ "id": "earnings_quality_income_tax_expense_attributed_to_foreign_jurisdictions",
  "what_changed": "MD&A states income tax expense of $1.3 million, against $0.2 million, and attributes the increase primarily to taxes in foreign jurisdictions. The tax note gives a different focus: it says the 11.7% effective rate was below the statutory rate mainly because of excess tax benefits from vesting share-based awards (notes:110). The two explanations are not stated as contradictory, but each names a different main factor.",
  "account": "income tax expense",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The increase in our income tax expense was primarily due to taxes in foreign jurisdictions.",
  "paragraph_id": "0001437749-26-025922:mdna:44",
  "explanation": false }
```

```json
{ "id": "earnings_quality_net_income_increase_driven_by_contingent_consideration_gain",
  "what_changed": "MD&A now states that the increase in net income (to $9.5 million from $6.7 million) was driven primarily by the change in fair value of contingent consideration, which is a Level 3 remeasurement gain. That remeasurement falls inside the open material weakness (item_4_controls:5). The release's guidance for the next quarter assumes no change in this fair value (8k_2_02:14).",
  "account": "net income; change in fair value of contingent consideration",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The increase in net income for the three months ended June 30, 2026 was driven primarily by the change in fair value of contingent consideration.",
  "paragraph_id": "0001437749-26-025922:mdna:46",
  "explanation": false }
```

```json
{ "id": "earnings_quality_non_gaap_definition_excludes_contingent_consideration",
  "what_changed": "This paragraph is carried as changed. The MD&A non-GAAP definition now lists change in fair value of contingent consideration among the excluded items, and the reconciliation removes the $8.1 million gain (mdna:50). The release's version of the definition (8k_2_02:42) also refers to 'the tax effect of adjustments calculated at the relevant rate', but neither reconciliation table (mdna:50, 8k_2_02:37) shows a tax-effect line. The non-GAAP measure therefore carries neither this remeasurement gain nor any future remeasurement loss.",
  "account": "non-GAAP net income",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "We define non-GAAP net income as net income before stock-based compensation, amortization of acquisition-related intangibles, change in fair value of contingent consideration, and other non-cash or unusual charges.",
  "paragraph_id": "0001437749-26-025922:mdna:49",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_non_gaap_net_income_decrease_lower_gross_margins",
  "what_changed": "MD&A now states non-GAAP net income of $7.6 million ($0.17 per share), against $11.6 million ($0.30), and attributes the decrease to lower gross margins. The release headline (8k_2_02:5) shows no non-GAAP figure and leads with record revenue and orders.",
  "account": "non-GAAP net income; gross margin",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "the decrease in non-GAAP net income was a result of lower gross margins",
  "paragraph_id": "0001437749-26-025922:mdna:51",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_foreign_bank_account_cash_and_liquidity_sources",
  "what_changed": "MD&A states that $22.8 million of cash, cash equivalents and restricted cash was held in foreign bank accounts at June 30, 2026. It names access to capital markets 'through our currently effective Registration Statements on Form S-3' among liquidity sources, and calls those sources sufficient for short-term and reasonably foreseeable long-term needs. It states total cash, cash equivalents and restricted cash of $153.1 million, 'an increase of $5.5 million' from March 31, 2026. The release (8k_2_02:10) gives the March figure as 147.6 million.",
  "account": "cash, cash equivalents and restricted cash",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "As of June 30, 2026, we had $22.8 million in cash, cash equivalents, and restricted cash in foreign bank accounts.",
  "paragraph_id": "0001437749-26-025922:mdna:54",
  "explanation": false }
```

```json
{ "id": "earnings_quality_operating_cash_flow_drivers_cite_fair_value_change",
  "what_changed": "MD&A attributes the increase in operating cash flow (to $16.0 million from $4.1 million) to changes in deferred revenue, inventory, and prepaid expenses and other current assets, 'and changes in fair value consideration'. The release's cash flow statement (8k_2_02:33) presents the change in fair value of contingent consideration as a non-cash adjustment to net income. Citing a non-cash remeasurement as a driver of operating cash flow is a wording for the supervisor to reconcile. The other named drivers are working-capital movements in customer deposits (deferred revenue) and inventory.",
  "account": "net cash provided by operating activities; deferred revenue; inventory",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "was due primarily to changes in deferred revenue, inventory, prepaid expenses and other current assets, and changes in fair value consideration",
  "paragraph_id": "0001437749-26-025922:mdna:56",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_property_plant_and_equipment_purchases",
  "what_changed": "MD&A states net cash used in investing activities of $10.5 million, against $0.7 million, primarily from purchases of property, plant and equipment. The notes now say the additional Brazilian real estate was purchased for 37.2 million Brazilian Real in cash (notes:135). The PP&E table shows land and building lines (notes:94). MD&A does not say what was purchased.",
  "account": "property, plant and equipment; investing cash flow",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "was primarily due to cash paid for the purchase of property, plant and equipment in the current year",
  "paragraph_id": "0001437749-26-025922:mdna:57",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_contractual_obligations_carve_out_for_earnout",
  "what_changed": "MD&A says that, other than the contingent consideration owed to the former Comtrafo stockholders, contractual obligations have not changed materially since the 10-K for the fiscal year ended March 31, 2026. The roll-forward (notes:83) shows the earnout already outstanding at March 31, 2026, so the carve-out does not say what changed in the obligation beyond the remeasurement. The completed 37.2 million Brazilian Real real estate purchase (notes:135) is not mentioned in this paragraph. The former stockholders also received 2,417,142 AMSC shares (notes:10).",
  "account": "contingent consideration; contractual obligations",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Other than the contingent consideration owed to the former Comtrafo stockholders there have been no material changes to our contractual obligations",
  "paragraph_id": "0001437749-26-025922:mdna:60",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_comtrafo_purchase_price_allocation_still_preliminary",
  "what_changed": "insufficient as to the prior wording: this paragraph is carried as changed, but its prior text is not in the input. It now says the Comtrafo purchase price and allocation remain preliminary and could be revised for deferred taxes, contingent consideration and intangible assets. It also says 'Changes to the purchase price allocation could be significant', and that the allocation will be finalized within the measurement period of up to one year from the December 5, 2025 acquisition. A measurement-period adjustment to goodwill has already been booked (notes:57), and the same accounting is under an open material weakness (item_4_controls:5).",
  "account": "goodwill; intangible assets; deferred tax asset; contingent consideration",
  "expected_direction": "none",
  "horizon": "by the end of the measurement period (within one year of December 5, 2025)",
  "quote": "Changes to the purchase price allocation could be significant.",
  "paragraph_id": "0001437749-26-025922:notes:8",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_acquired_receivables_uncollectible_portion",
  "what_changed": "insufficient as to the prior wording: this paragraph is carried as changed, but its prior text is not in the input. It states acquired Comtrafo receivables at a fair value of $6.9 million, with a gross amount due of $10.5 million, of which $3.6 million is expected to be uncollectible. It says fair value was adjusted for receivables more than a year old. The allocation table (notes:13) carries its own accounts receivable line; the numbers reader should reconcile the prose figures with the table. This is management's explanation of the acquired receivable valuation.",
  "account": "accounts receivable (acquired)",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "The gross amount due is $10.5 million, of which $3.6 million is expected to be uncollectible. The Company adjusted the fair value for receivables that exceeded a year.",
  "paragraph_id": "0001437749-26-025922:notes:14",
  "explanation": true }
```

```json
{ "id": "earnings_quality_inventory_step_up_fully_recognized",
  "what_changed": "The note now says the $1.5 million Comtrafo inventory step-up added $0.7 million to cost of revenue this quarter, after $0.8 million in the fiscal year ended March 31, 2026. It says the step-up 'has been fully recognized' as of June 30, 2026. MD&A (mdna:24) names this charge among the causes of the gross margin decrease. The prose implies no further step-up charge to cost of revenue after this quarter.",
  "account": "inventory; cost of revenues",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "The inventory step-up has been fully recognized to cost of revenue as of",
  "paragraph_id": "0001437749-26-025922:notes:15",
  "explanation": true }
```

```json
{ "id": "liquidity_and_capital_comtrafo_debt_repaid_and_debt_note_removed",
  "what_changed": "The note now says Comtrafo's three pre-acquisition debt agreements, totaling $8.8 million, were paid off during the fiscal year ended March 31, 2026. The separate Debt note is gone (note_history:6 and note_history:7 removed; Leases is now note 15, at notes:120). The prior 10-Q said current and long-term debt of $1.6 million and $6.1 million had been recorded (note_history:7), and the allocation table shows debt of 8.8 (notes:13). The numbers reader should reconcile these figures. The prose implies no Comtrafo debt remains.",
  "account": "debt (current and long-term)",
  "expected_direction": "down",
  "horizon": "already reflected at March 31, 2026 and June 30, 2026",
  "quote": "The debt agreements totaling $8.8 million were subsequently paid off during the fiscal year ended",
  "paragraph_id": "0001437749-26-025922:notes:16",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_backlog_amortization_sixteen_month_economic_consumption",
  "what_changed": "insufficient as to the prior wording: this paragraph is carried as changed, but its prior text is not in the input. It now says the $2.6 million Comtrafo backlog is amortized on an economic-consumption basis over a sixteen-month period and charged to cost of revenues. The intangibles table (notes:61) lists an estimated useful life of 2 for the backlog line. The supervisor should reconcile the two. Backlog amortization in cost of revenues bears on the release's expectation of second-half gross margin improvement (8k_2_02:11).",
  "account": "intangible assets (backlog); cost of revenues",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "The amortization method being utilized is economic consumption estimated over a sixteen-month period with the expense being allocated to cost of revenues.",
  "paragraph_id": "0001437749-26-025922:notes:17",
  "explanation": false }
```

```json
{ "id": "articulation_and_the_filed_history_comtrafo_deferred_tax_asset_figure",
  "what_changed": "The prose states '$1.1 million of deferred tax asset' for the Comtrafo acquisition, while the allocation table (notes:13) carries its own 'Deferred tax asset' line. The numbers reader should reconcile the prose figure with the table line. Notes:8 names deferred taxes as a provisional estimate, and the material weakness covers amounts recorded in the opening balance sheet (item_4_controls:5).",
  "account": "deferred tax asset; goodwill",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "The $1.1 million of deferred tax asset is primarily related to basis difference of intangibles, inventory and property, plant, and equipment.",
  "paragraph_id": "0001437749-26-025922:notes:19",
  "explanation": false }
```

```json
{ "id": "across_documents_comtrafo_contribution_against_earnout_forecast_and_grid_loss",
  "what_changed": "The note now states that Comtrafo contributed $19.4 million of revenue and $9.0 million of net income in the quarter. In the same quarter, MD&A says the earnout liability fell on 'changes in the forecast' (mdna:33). It also says the Grid segment, which holds Comtrafo, generated an operating loss due to lower gross margins and Comtrafo purchase accounting expense (mdna:37). The text does not say whether the $9.0 million includes the $8.1 million earnout gain, which the segment note places in Unallocated (notes:148). The supervisor should reconcile a stated net-income contribution with a lowered earnout forecast.",
  "account": "Comtrafo net income contribution; contingent consideration; Grid segment operating income",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Comtrafo contributed $19.4 million of revenue and $9.0 million in net income for the Company for the three months ended",
  "paragraph_id": "0001437749-26-025922:notes:24",
  "explanation": false }
```

```json
{ "id": "across_documents_acquisition_intangible_amortization_figures",
  "what_changed": "The text gives several acquisition-amortization figures for the quarter. Notes:24 gives $0.7 million of amortization from Comtrafo intangibles. Mdna:24 and notes:62 give $0.5 million of backlog amortization in cost of revenues. Mdna:31 and notes:62 give $0.5 million of customer-relationship and core-technology amortization, which MD&A attributes to Comtrafo plus NEPSI and Neeltran on an economic-consumption basis. The release's income statement line for amortization of acquisition-related intangibles (8k_2_02:25) and its non-GAAP add-back (8k_2_02:37) each carry their own figure. Reconciling these statements is the numbers reader's job.",
  "account": "amortization of acquisition-related intangibles; cost of revenues",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Amortization expense of $0.7 million is included in the three months ended",
  "paragraph_id": "0001437749-26-025922:notes:24",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_product_line_disaggregation_removed",
  "what_changed": "Revenue is now disaggregated by shipment destination only. The prior 10-Q disaggregated by product line as well (note_history:15). The product-line tables (Equipment and systems; Services and technology development, by segment) are removed (note_history:9, note_history:10, note_history:24, note_history:25), and the product-line terms are replaced in the policy paragraphs (notes:27, notes:28). In their place, notes:27 adds a sentence that 94% of revenue (93% in the prior-year quarter) was recognized on product sales. The region table now splits North America and South America where it previously showed 'Americas' (notes:35). Without the removed table, the segment-level product/service mix can no longer be tested.",
  "account": "revenue (disaggregation)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "revenue by shipment destination (in thousands)",
  "paragraph_id": "0001437749-26-025922:notes:34",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_remaining_performance_obligations_restated",
  "what_changed": "The note now states remaining performance obligations of approximately $301.8 million to be recognized in the next twelve months and approximately $118.8 million over thirteen to sixty months. The prior 10-Q stated $253.5 million and $99.7 million as of December 31, 2025 (note_history:20). The release calls the 12-month backlog 'robust' and 'exceeding $300 million' (8k_2_02:11). The note repeats that timing is subject to customer actions.",
  "account": "remaining performance obligations; revenue",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "to be recognized in the next twelve months of approximately $301.8 million",
  "paragraph_id": "0001437749-26-025922:notes:39",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_customer_concentration_fuji_bridex_below_threshold",
  "what_changed": "The 10% customer table now lists Inox Wind Limited (Wind) at 19%, against 21% in the prior-year quarter. It lists Fuji Bridex Pte Ltd (Grid) at <10%, against 16% in the prior-year quarter. Innomotics LLC, which appeared in the prior 10-Q's table (note_history:26), is no longer listed. MD&A names no Grid growth driver other than Comtrafo (mdna:21).",
  "account": "revenue concentration (Fuji Bridex Pte Ltd, Grid)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "Fuji Bridex Pte Ltd",
  "paragraph_id": "0001437749-26-025922:notes:41",
  "explanation": false }
```

```json
{ "id": "articulation_and_the_filed_history_goodwill_measurement_period_adjustment",
  "what_changed": "The goodwill roll-forward carries a 'Measurement period adjustment' line (2,674 thousand) between the Comtrafo balance acquired and March 31, 2026. The allocation table (notes:13) is presented 'as of the Comtrafo Acquisition Date', and notes:8 says the allocation is still preliminary. The material weakness says errors went undetected in amounts initially recorded to the opening balance sheet (item_4_controls:5). The text does not describe what the adjustment corrected or whether the allocation table reflects it. Reconciling the table with the roll-forward is the numbers reader's job.",
  "account": "goodwill",
  "expected_direction": "none",
  "horizon": "by the end of the measurement period (within one year of December 5, 2025)",
  "quote": "Measurement period adjustment",
  "paragraph_id": "0001437749-26-025922:notes:57",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_goodwill_no_impairment_trigger_identified",
  "what_changed": "The note says no impairment triggers were identified in the quarter. In the same filing, the earnout fair value was lowered on 'changes in the forecast' for Comtrafo (mdna:33), and the Grid segment, which carries all goodwill (notes:55), is reported at an operating loss (mdna:37). The material weakness covers Comtrafo purchase and fair value accounting (item_4_controls:5). The text does not say whether the forecast change was considered as a possible trigger. The annual test date is February 28 (notes:56).",
  "account": "goodwill",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "The Company did not identify any triggers to assess impairment in the three months ended",
  "paragraph_id": "0001437749-26-025922:notes:58",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_inventory_write_downs_excess_and_obsolescence",
  "what_changed": "The note states inventory write-downs of $1.1 million for the quarter ($0.7 million in the prior-year quarter). It bases them on an evaluation of inventory on hand for excess quantities and obsolescence. The release's cash flow statement carries a provision for excess and obsolete inventory line (8k_2_02:33). The stated cause is generic and names no product, segment or customer.",
  "account": "inventory reserve (excess and obsolete)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "evaluation of its inventory on hand for excess quantities and obsolescence",
  "paragraph_id": "0001437749-26-025922:notes:90",
  "explanation": true }
```

```json
{ "id": "estimates_and_discretion_effective_tax_rate_share_based_vesting_benefit",
  "what_changed": "The note now attributes the 11.7% effective rate being below the statutory rate to excess tax benefits from vesting share-based awards in the quarter. It explains the prior-year rate of 2.9% by the U.S. valuation allowance, 'a majority of which was subsequently released in fiscal 2025'. Benefits of this kind arise in the periods when awards vest, so the prose ties this quarter's rate to that discrete item. MD&A names a different main factor, foreign taxes (mdna:44).",
  "account": "effective tax rate; income tax expense",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "the effective tax rate was lower than the statutory rate primarily as a result of excess tax benefits for the vesting of share-based compensation awards during the period",
  "paragraph_id": "0001437749-26-025922:notes:110",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_valuation_allowance_united_states_and_poland",
  "what_changed": "insufficient as to the prior wording: this paragraph is carried as changed, but its prior text is not in the input. It now states that as of June 30, 2026 a valuation allowance remains against certain deferred tax assets in the U.S. and Poland, reassessed quarterly. The balance sheet carries deferred tax assets (8k_2_02:29), and notes:110 says the majority of the U.S. allowance was released in fiscal 2025. Whether Poland is newly named cannot be read.",
  "account": "deferred tax assets; valuation allowance",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "the Company maintains a valuation allowance against certain deferred tax assets in the U.S. and Poland",
  "paragraph_id": "0001437749-26-025922:notes:111",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_comtrafo_real_estate_purchase_completed",
  "what_changed": "The prior 10-Q said AMSC Brazil had 'entered into an agreement to purchase' additional real estate for 37,246,459 Brazilian Real, conditional on successful re-zoning (note_history:1). The text now says the real estate was purchased, for 37.2 million Brazilian Real in cash, upon successful re-zoning, so the commitment has been settled. The text does not give the purchase date or name the seller. MD&A (mdna:12) describes earlier real estate and transportation asset purchases under 'certain additional real property agreements' made alongside the acquisition, also without naming the counterparty. MD&A attributes the quarter's investing outflow to PP&E purchases (mdna:57).",
  "account": "property, plant and equipment (land, buildings); commitments",
  "expected_direction": "up",
  "horizon": "this quarter (the text does not give the purchase date)",
  "quote": "purchased additional real estate within the twelve months following the Comtrafo Acquisition Date for 37.2 million Brazilian Real in cash upon successful re-zoning classification of such real estate",
  "paragraph_id": "0001437749-26-025922:notes:135",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_contingent_consideration_gain_held_in_unallocated",
  "what_changed": "The segment note now has an 'Unallocated' column (notes:143) and says unallocated corporate expenses included the $8.1 million net gain on contingent consideration. MD&A's segment table labels the same 8,115 'Unallocated corporate expenses' (mdna:36). The earnout relates to Comtrafo, whose goodwill is assigned to Grid (notes:19), but the gain sits outside Grid segment results, and Grid is presented at an operating loss.",
  "account": "segment operating income (Grid; unallocated)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Unallocated corporate expenses included a net gain on contingent consideration of $8.1 million",
  "paragraph_id": "0001437749-26-025922:notes:148",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_bill_and_hold_disclosure_removed",
  "what_changed": "The prior 10-Q carried a bill-and-hold paragraph. It set out the recognition criteria and said revenue for the nine months ended December 31, 2025 included $7.9 million from held transactions. That paragraph is removed from this filing. The current text does not say whether any bill-and-hold revenue was recognized in the quarter ended June 30, 2026, or whether the practice continues.",
  "account": "revenue (bill-and-hold)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "included $7.9 million from such held transactions",
  "paragraph_id": "0001437749-26-002978:note_history:23",
  "explanation": false }
```

## Paragraphs carried as text and not made an item

### 8-K (0001437749-26-025921, exhibit 99.1)

- 8k_2_02:1 — exhibit cover and filename, no prose
- 8k_2_02:2 — filename only
- 8k_2_02:3 — exhibit heading
- 8k_2_02:4 — release title
- 8k_2_02:6 — conference call notice
- 8k_2_02:7 — dateline; company descriptor wording (same repositioning as notes:3)
- 8k_2_02:9 — GAAP and non-GAAP amounts only; causes itemized from mdna:46 and mdna:51
- 8k_2_02:10 — cash amounts only; covered by liquidity_and_capital_foreign_bank_account_cash_and_liquidity_sources
- 8k_2_02:12 — page header
- 8k_2_02:13 — section heading
- 8k_2_02:15 — section heading
- 8k_2_02:16 — call logistics
- 8k_2_02:17 — section heading
- 8k_2_02:18 — About boilerplate; new capability wording covered by structure_and_disclosure_changes_business_description_adds_industrial_and_emission_control
- 8k_2_02:19 — trademark notice; adds acquired brand names, wording only
- 8k_2_02:20 — page header
- 8k_2_02:21 — heading only; the forward-looking statement text is not carried
- 8k_2_02:22 — page header
- 8k_2_02:23 — table heading
- 8k_2_02:24 — units line
- 8k_2_02:25 — income statement table, amounts only
- 8k_2_02:26 — page header
- 8k_2_02:27 — table heading
- 8k_2_02:28 — units line
- 8k_2_02:29 — balance sheet table, amounts only
- 8k_2_02:30 — page header
- 8k_2_02:31 — table heading
- 8k_2_02:32 — units line
- 8k_2_02:33 — cash flow table, amounts only
- 8k_2_02:34 — page header
- 8k_2_02:35 — table heading
- 8k_2_02:36 — units line
- 8k_2_02:37 — non-GAAP reconciliation table, amounts only; the add-back is cited in across_documents_acquisition_intangible_amortization_figures
- 8k_2_02:38 — table heading
- 8k_2_02:39 — units line
- 8k_2_02:40 — forecast reconciliation table, amounts only; covered by the second-quarter guidance item
- 8k_2_02:41 — page header
- 8k_2_02:42 — non-GAAP definition note; covered by earnings_quality_non_gaap_definition_excludes_contingent_consideration
- 8k_2_02:43 — generic non-GAAP caution, boilerplate
- 8k_2_02:44 — contacts heading
- 8k_2_02:45 — contact title
- 8k_2_02:46 — contact name
- 8k_2_02:47 — phone number
- 8k_2_02:48 — email address
- 8k_2_02:49 — contact heading
- 8k_2_02:50 — contact name
- 8k_2_02:51 — phone number
- 8k_2_02:52 — email address
- 8k_2_02:53 — contact heading
- 8k_2_02:54 — contact name
- 8k_2_02:55 — phone number
- 8k_2_02:56 — email address

### 8-K index lines new since the prior period (these lines carry no paragraph id)

- 2026-08-05 0001437749-26-025921, Item 5.07 — insufficient: body not in input
- 2026-06-02 0001437749-26-019163, Item 5.02 — itemized (controls_audit_and_filings_officer_or_director_change_filing_body_not_in_input)
- 2026-05-27 0001437749-26-018539, Item 2.02 — insufficient: fiscal-year earnings release body not in input
- 2026-02-17 0001437749-26-004349, Item 9.01, amendment of the 2025-12-10 Comtrafo 8-K — insufficient: body not in input
- Late-filing notifications: only 2011 entries; nothing new

### Item 4 controls (0001437749-26-025922)

- item_4_controls:1 — heading
- item_4_controls:2 — heading
- item_4_controls:4 — heading
- item_4_controls:7 — standard "notwithstanding" fair-presentation statement that goes with the material weakness; covered by controls_audit_and_filings_disclosure_controls_not_effective
- item_4_controls:8 — heading
- item_4_controls:9 — "Other than the foregoing" no-other-changes statement; covered by controls_audit_and_filings_material_weakness_remediation_in_progress
- item_4_controls:10 — page number

### MD&A (0001437749-26-025922)

- mdna:2 — wording only: trademark list (names Comtrafo)
- mdna:6 — insufficient: prior wording not in input; restates the two segments, Grid and Wind
- mdna:7 — insufficient: prior wording not in input; Grid segment description with no amount or estimate
- mdna:8 — insufficient: prior wording not in input; Wind segment description with no amount or estimate
- mdna:9 — date rolled forward (fiscal-year definition)
- mdna:10 — page number
- mdna:12 — insufficient: prior wording not in input; restates the Comtrafo terms (Brazilian Real cash, shares, real estate and transportation assets, earnout cap); counterparty to the real estate purchases not named
- mdna:17 — heading, date rolled forward
- mdna:19 — amounts only (total revenue); causes itemized from mdna:21 and mdna:22
- mdna:20 — table, amounts only
- mdna:31 — covered by across_documents_acquisition_intangible_amortization_figures
- mdna:36 — table, amounts only; the unallocated label is covered by structure_and_disclosure_changes_contingent_consideration_gain_held_in_unallocated
- mdna:50 — table, amounts only
- mdna:55 — table, amounts only
- mdna:58 — amounts only: no financing activity this quarter; the prior-year equity raise was already disclosed
- mdna:59 — amounts only: restricted cash rolled forward (same amounts as notes:136)
- mdna:62 — heading
- mdna:65 — insufficient: pronouncement boilerplate, prior wording not in input; no adoption or effect stated
- mdna:66 — insufficient: pronouncement boilerplate, prior wording not in input; cites "ASU 2024-05" for ASU 2025-06 (typo)
- mdna:67 — insufficient: pronouncement boilerplate, prior wording not in input

### Notes (0001437749-26-025922)

- notes:3 — wording only: company descriptor rewritten (note_history:3 added, note_history:5 removed); the Navy wording is dropped from the note but kept in MD&A (mdna:5); no effect on any account
- notes:4 — date rolled forward (note_history:4)
- notes:7 — insufficient: prior wording not in input; restates acquisition and earnout terms; the Monte Carlo method is covered by the contingent consideration item
- notes:9 — amounts only: total purchase price; reconciliation left to the numbers reader
- notes:10 — consideration table, amounts only
- notes:11 — date rolled forward: acquisition-cost period is now the full fiscal year; share value at closing restated
- notes:12 — table lead-in
- notes:13 — allocation table, amounts only; cited in the goodwill measurement-period, deferred-tax, receivables and debt items
- notes:18 — insufficient: prior wording not in input; customer-relationship method and life restated; covered alongside the backlog amortization item
- notes:21 — date rolled forward (pro forma lead-in)
- notes:22 — pro forma table, amounts only
- notes:23 — boilerplate pro forma caveat
- notes:26 — amounts only: point-in-time percentages rolled forward (note_history:11)
- notes:27 — covered by structure_and_disclosure_changes_product_line_disaggregation_removed
- notes:28 — wording only: product-line terms replaced (note_history:13); covered by the disaggregation item
- notes:32 — date rolled forward (note_history:14)
- notes:35 — table; the new North America / South America split is covered by the disaggregation item
- notes:36 — date rolled forward (note_history:17)
- notes:37 — contract balance roll-forward table, amounts only (note_history:18)
- notes:38 — prior-year roll-forward table, amounts only (note_history:19)
- notes:40 — date rolled forward (note_history:21)
- notes:43 — date rolled forward
- notes:44 — table, amounts only
- notes:45 — amounts only (restricted stock issuances)
- notes:46 — amounts only (no option grants; unrecognized compensation)
- notes:47 — date rolled forward
- notes:48 — table, amounts only
- notes:50 — amounts only (anti-dilutive share counts)
- notes:51 — table lead-in
- notes:52 — EPS table, amounts only
- notes:55 — insufficient: prior wording not in input; lists the acquisitions behind goodwill, all in Grid
- notes:56 — insufficient: prior wording not in input; goodwill policy and February 28 test date restated
- notes:60 — table lead-in, dates rolled forward
- notes:61 — intangibles table, amounts only; the backlog useful life is cited in the backlog item
- notes:62 — covered by across_documents_acquisition_intangible_amortization_figures
- notes:64 — amortization schedule table, amounts only
- notes:65 — insufficient: prior wording not in input; intangibles attributed to Grid in the U.S. and Brazil
- notes:66 — table, amounts only
- notes:70 — date rolled forward (no Level transfers)
- notes:78 — covered by estimates_and_discretion_contingent_consideration_gain_attributed_to_forecast_change
- notes:79 — table lead-in
- notes:80 — fair value table, amounts only
- notes:81 — fair value table, amounts only
- notes:83 — contingent consideration roll-forward table; cited in the contingent consideration item
- notes:85 — table lead-in
- notes:86 — receivables table, amounts only
- notes:88 — table lead-in
- notes:89 — inventory table, amounts only
- notes:91 — date rolled forward (deferred program costs definition)
- notes:93 — table lead-in
- notes:94 — PP&E table, amounts only; cited in the PP&E and real estate items
- notes:95 — amounts only (depreciation)
- notes:99 — date rolled forward and amounts only (NWL Pacific balances "not material", investment carrying amount)
- notes:101 — NWL Pacific summary table, amounts only
- notes:103 — table lead-in
- notes:104 — payables and accruals table, amounts only
- notes:107 — warranty roll-forward table, amounts only
- notes:109 — amounts only; covered by the two tax items
- notes:112 — date rolled forward (no uncertain tax positions)
- notes:115 — insufficient: prior wording not in input; restates the earnout's liability classification
- notes:117 — valuation inputs table; cited in the contingent consideration item
- notes:118 — prior valuation inputs table; cited in the contingent consideration item
- notes:119 — covered by the contingent consideration item
- notes:120 — heading renumbered after removal of the Debt note; covered by liquidity_and_capital_comtrafo_debt_repaid_and_debt_note_removed
- notes:124 — table lead-in
- notes:125 — lease balance table, amounts only
- notes:126 — table lead-in
- notes:127 — lease cost table, amounts only
- notes:129 — lease maturity table, amounts only
- notes:130 — renumbered heading
- notes:131 — heading
- notes:132 — insufficient: prior wording not in input; legal-contingency policy boilerplate, no matter named
- notes:133 — heading
- notes:134 — insufficient: prior wording not in input; performance-bond and minimum-purchase commitment boilerplate
- notes:136 — amounts only: dates and restricted cash amounts rolled forward (note_history:2)
- notes:137 — renumbered heading
- notes:142 — table lead-in
- notes:143 — segment table; the Unallocated column is covered by structure_and_disclosure_changes_contingent_consideration_gain_held_in_unallocated
- notes:146 — prior-year segment table, amounts only
- notes:149 — table lead-in
- notes:150 — reconciliation table, amounts only
- notes:151 — table lead-in
- notes:152 — depreciation and amortization by segment table, amounts only
- notes:154 — table lead-in
- notes:155 — segment assets table, amounts only
- notes:156 — renumbered heading
- notes:157 — insufficient: pronouncement boilerplate, prior wording not in input
- notes:158 — insufficient: pronouncement boilerplate, prior wording not in input; cites "ASU 2024-05" for ASU 2025-06 (typo)
- notes:159 — renumbered heading
- notes:160 — insufficient: prior wording not in input; states that there are no subsequent events
- notes:164 — date rolled forward (no 10b5-1 adoptions or terminations)

### Note change history

Every changed, added or removed paragraph in the history is covered by the items and lines above. note_history:23 (bill-and-hold paragraph removed) is itemized directly, because its removal leaves no current paragraph to point to.

## Counts

- Items: 49 (explanation flagged on 3: estimates_and_discretion_acquired_receivables_uncollectible_portion, earnings_quality_inventory_step_up_fully_recognized, estimates_and_discretion_inventory_write_downs_excess_and_obsolescence).
- Insufficient: 27 in total:
  - 6 items marked insufficient as to prior wording or content: the 5.02 filing, macro risks, purchase price allocation, acquired receivables, backlog amortization and valuation allowance.
  - 18 carried-as-text paragraphs: mdna:6, 7, 8, 12, 65, 66, 67 and notes:7, 18, 55, 56, 65, 115, 132, 134, 157, 158, 160.
  - 3 8-K index lines whose bodies are not in the input.
