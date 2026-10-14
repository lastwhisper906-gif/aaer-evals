<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# report_notes_text — FELE 10-Q 0000038725-26-000055 (prior period of the same kind: 0000038725-26-000026)

Scope check:
- I read all six inputs to the end: input_8k.md, input_controls.md, input_mdna.md, input_notes.md, input_notes_history.md and input_prior_predictions.md.
- None of the forbidden material is in my directory: no trend table, prices, abnormal returns or short interest, no other company's files, no prior-run probability and no outcome window.
- Some inputs are missing, so I read nothing for them: the Item 1A diff, the Exhibit 21 diff, any Exhibit 10, and an auditor's report. input_controls.md carries Item 4 only.
- Prior flags: none on record (input_prior_predictions.md).
- The 8-K index shows no Item 4.01 or 4.02 filing and no late-filing notice up to 2026-07-29. Only the 2.02 body (0000038725-26-000051) is in my input.
- MD&A paragraphs that appear as text are marked as changed, but their prior-period wording is not in my input. For those, `what_changed` says what the current text states.
- I did no arithmetic. Every statement about amounts or direction is the prose's own.

## Items

```json
[
  {
    "id": "related_parties_contingencies_and_subsequent_events_esso_preliminary_settlement_accrued",
    "what_changed": "The prior note described the Esso France filling-station matter as unresolved, with an outcome the Company could not predict. It now says the parties reached a preliminary agreement in the second quarter of 2026, the Company agreed to pay $4.5 million to resolve its portion of the litigation, and $4.5 million was accrued at June 30, 2026. The note still gives the Company's position that its products were not the cause of any alleged damage. This is management's account of a new reserve.",
    "account": "Accrued expenses and other current liabilities; Legal settlement loss",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "As of June 30, 2026, the Company accrued $4.5 million and anticipates paying the amount upon approval by the Court.",
    "paragraph_id": "0000038725-26-000055:notes:52",
    "explanation": true
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_esso_settlement_awaits_court_approval",
    "what_changed": "New sentences say the settlement still has to be finalized between the parties and approved by the Court. The Court has set a hearing for late third quarter of 2026 to make sure the parties are progressing, and the Company expects to pay when the Court approves. So the accrual rests on a proposed agreement, and the cash payment depends on the Court's timetable.",
    "account": "Cash and cash equivalents; settlement accrual in accrued expenses",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "The settlement is subject to finalization between the parties and approval by the Court.",
    "paragraph_id": "0000038725-26-000055:notes:52",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_esso_expert_damages_and_warning_removed",
    "what_changed": "Four sentences from the prior note are gone: the expert's May 2022 total-damages figure for Esso; the statement that the Company cannot predict the outcome; the warning that payments could have a material effect on financial position, results of operations or cash flows; and the expected late-second-quarter hearing date. The new note gives only the Company's agreed payment for its own portion. It does not restate the total-damages figure or say how the Company's portion was set. I leave it to the numbers reader and the supervisor to set the agreed payment against the removed figure.",
    "account": "Legal settlement loss; settlement accrual",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "In May 2022, the subject-matter expert issued its final report, which indicates that total damages incurred by Esso amounted to approximately 9.5 million Euro.",
    "paragraph_id": "0000038725-26-000026:note_history:5",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_legal_settlement_line_in_accrued_expenses",
    "what_changed": "The accrued expenses table has a new row, 'Legal settlement loss (see Note 7)', with a balance at June 30, 2026 and a dash at December 31, 2025. This puts the settlement liability in current liabilities.",
    "account": "Accrued expenses and other current liabilities",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Legal settlement loss (see Note 7)",
    "paragraph_id": "0000038725-26-000055:notes:39",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_legal_settlement_section_charged_to_energy",
    "what_changed": "MD&A adds a new 'Legal settlement loss' section saying a $4.5 million provision was recorded in the Energy Systems segment in the second quarter of 2026. The same charge appears in three other places: as a new operating caption, 'Legal settlement loss', in the release's income statement (8k_2_02:40); as a new 'Legal settlement loss (see Note 7)' row under Energy Systems in the segment tables (notes:88, notes:90); and as a reconciling item in the release (8k_2_02:19, 8k_2_02:51).",
    "account": "Legal settlement loss; Energy Systems segment operating income",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "There was a $4.5 million provision for legal settlement recorded in the Energy Systems segment during the second quarter of 2026.",
    "paragraph_id": "0000038725-26-000055:mdna:29",
    "explanation": false
  },
  {
    "id": "results_against_expectations_energy_margin_decline_attributed_to_settlement",
    "what_changed": "MD&A describes Energy Systems' quarter operating income as a decrease and says the margin decrease was primarily due to the $4.5 million legal settlement. The release (8k_2_02:19) presents adjusted Energy Systems operating income with the settlement added back. Neither document says whether the charge could recur or be revised.",
    "account": "Energy Systems segment operating income and margin",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The decrease in margin was primarily due to $4.5 million legal settlement recorded in the second quarter of 2026.",
    "paragraph_id": "0000038725-26-000055:mdna:39",
    "explanation": false
  },
  {
    "id": "earnings_quality_adjusted_eps_settlement_add_back_gross_of_tax",
    "what_changed": "The adjusted diluted EPS reconciliation has a new row adding back the legal settlement, and the row is labelled 'gross of tax'. The restructuring row has no tax label. Whether the per-share add-back is before or after tax, and what that does to adjusted EPS, is for the numbers reader. The non-GAAP adjustments remove the settlement charge but do not remove the tariff-refund benefit that MD&A cites for the quarter (mdna:25, mdna:37).",
    "account": "Adjusted diluted EPS (non-GAAP); Legal settlement loss",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Legal settlement, gross of tax",
    "paragraph_id": "0000038725-26-000051:8k_2_02:49",
    "explanation": false
  },
  {
    "id": "earnings_quality_tariff_refunds_lift_gross_margin",
    "what_changed": "MD&A now says tariff refunds helped the second-quarter gross profit margin. It gives no amount and does not say whether the refunds were received in cash or are still receivable. It does not say whether more refunds are expected. None of the notes that appear as text mentions tariff refunds.",
    "account": "Cost of sales / gross profit; receivables or other current assets (the prose does not say where the refund is recorded)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The gross profit margin was favorably impacted in the second quarter by tariff refunds",
    "paragraph_id": "0000038725-26-000055:mdna:25",
    "explanation": false
  },
  {
    "id": "across_documents_tariff_refunds_in_mdna_absent_from_release",
    "what_changed": "MD&A credits part of Water Systems' quarter operating income increase to tariff refunds. The release does not mention tariff refunds: not in the Water Systems summary (8k_2_02:17) and not in the CEO's comments (8k_2_02:14, 8k_2_02:15). The CEO talks instead about inflationary pressure in sourced materials and logistics. A benefit that comes from refunds would not repeat once the refunds stop.",
    "account": "Water Systems segment operating income",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "The increase in operating income in the second quarter was primarily due to higher sales and tariff refunds.",
    "paragraph_id": "0000038725-26-000055:mdna:37",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_unfavorable_product_and_geographic_mix",
    "what_changed": "MD&A describes Water Systems' six-month operating margin as a decrease, primarily due to an unfavorable shift in product and geographic sales mix. mdna:25 gives the same mix shift as the reason for the consolidated six-month gross margin.",
    "account": "Water Systems operating margin; gross profit margin",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The decrease in margin for the first six months was primarily due to an unfavorable product and geographic sales mix shift.",
    "paragraph_id": "0000038725-26-000055:mdna:37",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_inflation_in_sourced_materials_and_logistics",
    "what_changed": "The CEO says the Company is seeing inflationary price pressure in sourced materials and logistics lanes and is managing it closely.",
    "account": "Cost of sales",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "continue to manage closely the inflationary price pressures",
    "paragraph_id": "0000038725-26-000051:8k_2_02:15",
    "explanation": false
  },
  {
    "id": "results_against_expectations_full_year_guidance_raised_in_release",
    "what_changed": "The release says the Company is raising its full-year 2026 guidance. Net sales guidance is now $2.21 billion to $2.29 billion and adjusted diluted EPS guidance is now $4.50 to $4.70. The CEO links the raise to 'continued momentum in our core businesses' (8k_2_02:14). The previous ranges are not in my input.",
    "account": "Net sales; adjusted diluted EPS",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "The Company is raising its guidance for full year 2026 net sales to be in the range of $2.21 billion to $2.29 billion and full year 2026 Adjusted Diluted EPS to be in the range of $4.50 to $4.70.",
    "paragraph_id": "0000038725-26-000051:8k_2_02:22",
    "explanation": false
  },
  {
    "id": "across_documents_organic_volume_claim_against_water_systems_drivers",
    "what_changed": "The CEO says the results reflect progress on organic volume growth initiatives and calls the quarter's growth 'balanced between organic and inorganic contributions'. MD&A's own wording differs in three places. The Water Systems quarter drivers it names are price, currency and acquisitions, with no volume (mdna:14). The consolidated quarter attribution lists acquisitions first (mdna:10). Outside the U.S. and Canada, excluding currency and acquisitions, it says Asia Pacific growth was 'more than offset' by declines in Latin America and Europe (mdna:15). Whether the CEO's description fits MD&A's breakdown is for the numbers reader.",
    "account": "Net sales (organic volume)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "These results reflect the progress of our organic volume growth initiatives",
    "paragraph_id": "0000038725-26-000051:8k_2_02:14",
    "explanation": false
  },
  {
    "id": "across_documents_dewatering_demand_claim_against_mdna_decline",
    "what_changed": "The CEO cites solid demand in dewatering for mining in fast-growing regions. MD&A reports lower U.S. and Canada sales of large dewatering equipment in both the quarter and the six months (mdna:15). The two may refer to different regions or products, but neither document reconciles them.",
    "account": "Water Systems net sales (dewatering)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "solid demand in areas such as dewatering for mining",
    "paragraph_id": "0000038725-26-000051:8k_2_02:14",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_large_dewatering_equipment_decline",
    "what_changed": "MD&A says U.S. and Canada sales of large dewatering equipment were lower in both the second quarter and the first six months, partly offsetting growth in groundwater, water treatment and surface pumping.",
    "account": "Water Systems net sales, U.S. and Canada (large dewatering equipment)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "These sales increases were partially offset by lower sales of large dewatering equipment of 10 percent compared to 2025.",
    "paragraph_id": "0000038725-26-000055:mdna:15",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_latin_america_and_europe_organic_declines",
    "what_changed": "MD&A says that, excluding currency translation and acquisitions, Water Systems sales growth in Asia Pacific was more than offset by declines in Latin America and Europe, in both the quarter and the six months. The reported growth outside the U.S. and Canada is attributed to acquisitions and favorable exchange rates.",
    "account": "Water Systems net sales outside the U.S. and Canada",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "the sales growth in the Asia Pacific regions was more than offset by sales declines in the Latin America and European regions",
    "paragraph_id": "0000038725-26-000055:mdna:15",
    "explanation": false
  },
  {
    "id": "across_documents_currency_row_includes_hyperinflation_price_increases",
    "what_changed": "A footnote to the release's sales bridge says local-currency price increases in Argentina and Turkey are shown in the foreign-currency-translation row, not in volume/price. MD&A (mdna:15) calls the international currency contribution 'the favorable impact from foreign exchange rates' and does not say it includes price increases. So MD&A's regional trend excluding currency leaves out this pricing by construction.",
    "account": "Net sales (split between currency and volume/price)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The Company has presented local currency price increases used to offset currency devaluation in the highly inflationary economies of Argentina and Turkey within the foreign currency translation, net row above.",
    "paragraph_id": "0000038725-26-000051:8k_2_02:45",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_water_systems_drivers_omit_volume",
    "what_changed": "MD&A attributes Water Systems' second-quarter sales increase to price realization, exchange rates and acquisitions, and names no volume driver. The six-month sentence names volume increases first. The release's Water Systems summary (8k_2_02:17) also leaves out volume.",
    "account": "Water Systems net sales (volume)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The sales increase for the second quarter was primarily due to price realization, the positive impact of foreign exchange rates, and the incremental sales impact from recent acquisitions.",
    "paragraph_id": "0000038725-26-000055:mdna:14",
    "explanation": false
  },
  {
    "id": "results_against_expectations_acquisitions_lead_sales_growth_attribution",
    "what_changed": "The consolidated attribution for the quarter now lists acquisitions first, then price and volume, then exchange rates. The six-month attribution lists volume and price first. The sentence also has a drafting slip ('second quarter three months').",
    "account": "Net sales",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The sales increase for the second quarter three months was primarily due to incremental sales impact from recent acquisitions of 3 percent, price and volume increases of 2 percent, and the positive impact of foreign exchange rates of 1 percent.",
    "paragraph_id": "0000038725-26-000055:mdna:10",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_benson_pump_and_wood_brothers_acquisitions",
    "what_changed": "MD&A adds two acquisitions. Benson Pump, an Arkansas groundwater distributor bought in April 2026, is in the Distribution segment. Wood Brothers Industries, a Nebraska water treatment wholesale supplier bought in May 2026, operates as a subsidiary of Water Systems. MD&A says acquisitions contributed about $15.0 million of incremental second-quarter net sales.",
    "account": "Net sales; goodwill and other intangible assets",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Acquisitions contributed approximately $15.0 million of incremental net sales in the second quarter of 2026.",
    "paragraph_id": "0000038725-26-000055:mdna:3",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_wood_brothers_acquired_legal_entities",
    "what_changed": "New: the Company acquired 100 percent of Piertek, Inc, Piertek III, LLC and Vistar Water Technologies, Inc. for $49.9 million net of cash acquired. The note defines these, together with 'its affiliated companies', as Wood Brothers Industries. The legal entities have different names from the trade name MD&A uses.",
    "account": "Goodwill; other intangible assets; acquisitions and investments (investing cash flow)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "acquired 100 percent of Piertek, Inc, Piertek III, LLC, and Vistar Water Technologies, Inc.",
    "paragraph_id": "0000038725-26-000055:notes:11",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_wood_brothers_preliminary_valuation",
    "what_changed": "The Wood Brothers valuation is still preliminary at June 30, 2026. The note says finalizing it within the one-year measurement period could change the amounts for intangible assets, goodwill and income taxes.",
    "account": "Goodwill; other intangible assets; deferred tax liabilities",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Finalization of the valuation during the measurement period could result in a change in the amounts recorded for the acquisition date fair value of intangible assets, goodwill, and income taxes among other items.",
    "paragraph_id": "0000038725-26-000055:notes:12",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_wood_brothers_intangible_lives_and_level_three_inputs",
    "what_changed": "New allocation: $19.1 million to customer relationships with a 12-year life, and $8.8 million to trade names with lives of 6 to 9 years. Both were valued by the income approach and are classed as Level 3 because they depend on significant management estimates.",
    "account": "Other intangible assets; amortization expense",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "The Company allocated $19.1 million of the total consideration to customer relationships with a useful life of 12 years, $8.8 million to trade names with a useful life of 6 to 9 years.",
    "paragraph_id": "0000038725-26-000055:notes:15",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_wood_brothers_wholesale_business_in_water_systems",
    "what_changed": "notes:11 describes Wood Brothers as a wholesale supplier to professional water treatment dealers, but its goodwill is placed in the Water Systems segment, not Distribution. The goodwill is not tax-deductible, and no pro forma is given because the business is not material. MD&A's U.S. and Canada water treatment product growth (mdna:15) does not say whether it includes the acquired sales.",
    "account": "Water Systems segment net sales; goodwill (Water Systems)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "and is included in the Water Systems segment",
    "paragraph_id": "0000038725-26-000055:notes:16",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_benson_pump_purchase_price_after_working_capital",
    "what_changed": "New: the Company acquired 100 percent of Benson Pump Corporation, a groundwater distributor operating out of Arkansas, for $21.7 million after purchase price adjustments for working capital.",
    "account": "Goodwill (Distribution); acquisitions and investments (investing cash flow)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "for a purchase price of $21.7 million, after purchase price adjustments based on the level of working capital acquired",
    "paragraph_id": "0000038725-26-000055:notes:18",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_benson_pump_allocation_not_tabulated",
    "what_changed": "The Benson Pump valuation is preliminary. The note says only that the price was primarily allocated to goodwill and other intangible assets, with no table and no useful lives. For a distribution business, it lists 'potential future technologies' among the elements of goodwill. notes:20 leaves out post-closing results and pro forma figures as immaterial.",
    "account": "Goodwill (Distribution); other intangible assets",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "The purchase price was primarily allocated to goodwill and other intangible assets.",
    "paragraph_id": "0000038725-26-000055:notes:19",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_credit_loss_practical_expedient_adopted",
    "what_changed": "The note says the Company adopted ASU 2025-05 prospectively from its 2026 interim statements, with no material impact. The ASU is an optional practical expedient for measuring credit losses on receivables and contract assets. The paragraph is marked as changed, but its prior wording is not in my input, so I cannot say which words changed.",
    "account": "Receivables (net): allowance for credit losses",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The Company adopted this ASU prospectively, effective with its 2026 interim financial statements and the adoption did not have a material impact on its financial statements.",
    "paragraph_id": "0000038725-26-000055:notes:3",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_environmental_credits_standard_added",
    "what_changed": "New paragraph on ASU 2026-02 (Environmental Credits and Environmental Credit Obligations, Topic 818), issued in May 2026. It is effective for interim periods within annual periods beginning after December 15, 2027, and the Company is evaluating it.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "beyond 12 months",
    "quote": "In May 2026, the FASB issued ASU 2026-02, Environmental Credits and Environmental Credit Obligations (Topic 818)",
    "paragraph_id": "0000038725-26-000055:notes:8",
    "explanation": false
  },
  {
    "id": "earnings_quality_unfavorable_discrete_tax_events_not_described",
    "what_changed": "The higher effective tax rate for the quarter and the six months is attributed primarily to 'increased unfavorable discrete events in 2026'. The events are not identified. MD&A (mdna:51) uses the same phrase.",
    "account": "Income tax expense",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase in the effective tax rate for the second quarter and first six months of 2026 compared to the comparable periods in the prior year was primarily due to increased unfavorable discrete events in 2026.",
    "paragraph_id": "0000038725-26-000055:notes:68",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_interest_expense_attributed_to_higher_average_debt",
    "what_changed": "MD&A attributes higher interest expense primarily to a higher average amount of outstanding debt. The debt note states Credit Agreement borrowings of $107.0 million at June 30, 2026 (notes:48), and the release's balance sheet shows them in current maturities and short-term borrowings.",
    "account": "Interest expense; Credit Agreement borrowings",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "The increases in the second quarter and first six months of 2026 were primarily driven by higher average amount of outstanding debt.",
    "paragraph_id": "0000038725-26-000055:mdna:45",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_copper_purchase_commitment",
    "what_changed": "MD&A states a firm, non-cancellable commitment to buy copper from a vendor, with about $3.4 million remaining, to be fulfilled within the next year. The paragraph is marked as changed, but its prior wording is not in my input. The commitments paragraph in the notes (notes:54) gives only a total.",
    "account": "Purchase commitments; inventory and cost of sales (copper)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "purchase commitment with a vendor for copper with an aggregate remaining obligation of approximately $3.4 million, expected to be fulfilled within the next year.",
    "paragraph_id": "0000038725-26-000055:mdna:61",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_operating_cash_flow_attribution_names_no_working_capital_line",
    "what_changed": "MD&A attributes the change in operating cash flow to an increase in net income and to 'changes in working capital', without naming any working-capital line. No MD&A paragraph or note that appears as text explains the receivables or inventory balances at June 30, 2026.",
    "account": "Net cash flows from operating activities; receivables; inventory",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The change in operating cash flow was primarily attributable to an increase in net income and changes in working capital.",
    "paragraph_id": "0000038725-26-000055:mdna:68",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_mdna_credits_lower_share_repurchases",
    "what_changed": "MD&A attributes the change in financing cash flow primarily to fewer repurchases of common stock in 2026. It does not mention borrowings as a source of financing, although mdna:45 cites higher average debt.",
    "account": "Purchases of common stock; financing cash flows",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The change in financing cash flow was primarily due to decreased repurchases of Common Stock in 2026 compared to 2025.",
    "paragraph_id": "0000038725-26-000055:mdna:74",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_share_swap_asset_in_receivables",
    "what_changed": "The fair value table (notes:82) has a share swap transaction asset at June 30, 2026 and no such row at December 31, 2025. The note says the swap asset is recorded within Receivables, and the quarter's swap gain is recorded in SG&A (notes:74). This sentence classifies the asset; it does not explain the change in receivables.",
    "account": "Receivables (net); Selling, general and administrative expenses",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The share swap transaction asset is recorded within the \"Receivables\" line of the condensed consolidated balance sheets.",
    "paragraph_id": "0000038725-26-000055:notes:83",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_dividend_to_noncontrolling_interest",
    "what_changed": "The equity roll-forward has a new 'Dividend to noncontrolling interest' row in the second quarter of 2026, which also appears in the six-month table (notes:59). The prior-year columns have no such row. Where this dividend appears in the cash flow statement is for the numbers reader.",
    "account": "Noncontrolling interest; financing cash flows",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Dividend to noncontrolling interest",
    "paragraph_id": "0000038725-26-000055:notes:58",
    "explanation": false
  }
]
```

## Paragraphs carried as text that are not items

### 8-K 0000038725-26-000051, item 2.02
- 0000038725-26-000051:8k_2_02:1 — exhibit file header
- 0000038725-26-000051:8k_2_02:2 — document label
- 0000038725-26-000051:8k_2_02:3 — exhibit label
- 0000038725-26-000051:8k_2_02:4 — release banner
- 0000038725-26-000051:8k_2_02:5 — release title
- 0000038725-26-000051:8k_2_02:6 — heading
- 0000038725-26-000051:8k_2_02:7 — headline amounts only
- 0000038725-26-000051:8k_2_02:8 — headline segment amounts only
- 0000038725-26-000051:8k_2_02:9 — headline amounts only
- 0000038725-26-000051:8k_2_02:10 — amounts only; the "1" after "$1.55" reads as the footnote marker defined in :13 (it also runs into "EPS1" in :12)
- 0000038725-26-000051:8k_2_02:11 — dateline
- 0000038725-26-000051:8k_2_02:12 — amounts only
- 0000038725-26-000051:8k_2_02:13 — non-GAAP footnote, boilerplate
- 0000038725-26-000051:8k_2_02:16 — heading
- 0000038725-26-000051:8k_2_02:17 — Water Systems summary; its drivers are the same as mdna:14 (item `narrative_signs_of_operating_pressure_water_systems_drivers_omit_volume`); restructuring amount only
- 0000038725-26-000051:8k_2_02:18 — Distribution summary; amounts, with drivers repeated in mdna:20
- 0000038725-26-000051:8k_2_02:19 — Energy Systems summary; the settlement is covered by the settlement items
- 0000038725-26-000051:8k_2_02:20 — non-GAAP footnote, boilerplate
- 0000038725-26-000051:8k_2_02:21 — heading
- 0000038725-26-000051:8k_2_02:23 — heading
- 0000038725-26-000051:8k_2_02:24 — call logistics
- 0000038725-26-000051:8k_2_02:25 — webcast URL
- 0000038725-26-000051:8k_2_02:26 — call logistics
- 0000038725-26-000051:8k_2_02:27 — registration URL
- 0000038725-26-000051:8k_2_02:28 — call logistics
- 0000038725-26-000051:8k_2_02:29 — replay dates
- 0000038725-26-000051:8k_2_02:30 — heading
- 0000038725-26-000051:8k_2_02:31 — forward-looking boilerplate (fragment that starts mid-sentence)
- 0000038725-26-000051:8k_2_02:32 — heading
- 0000038725-26-000051:8k_2_02:33 — non-GAAP definitions, boilerplate; I have no prior release to tell whether Adjusted Operating Income is new
- 0000038725-26-000051:8k_2_02:34 — heading
- 0000038725-26-000051:8k_2_02:35 — company description, boilerplate
- 0000038725-26-000051:8k_2_02:36 — contact heading
- 0000038725-26-000051:8k_2_02:37 — contact names
- 0000038725-26-000051:8k_2_02:38 — company name
- 0000038725-26-000051:8k_2_02:39 — contact email
- 0000038725-26-000051:8k_2_02:40 — income statement, amounts only; the new "Legal settlement loss" caption is covered by `structure_and_disclosure_changes_legal_settlement_section_charged_to_energy`
- 0000038725-26-000051:8k_2_02:41 — balance sheet, amounts only
- 0000038725-26-000051:8k_2_02:42 — cash flow statement, amounts only
- 0000038725-26-000051:8k_2_02:43 — heading
- 0000038725-26-000051:8k_2_02:44 — sales bridge table, amounts only (its footnote :45 is an item)
- 0000038725-26-000051:8k_2_02:46 — heading
- 0000038725-26-000051:8k_2_02:47 — operating margin table, amounts only
- 0000038725-26-000051:8k_2_02:48 — heading
- 0000038725-26-000051:8k_2_02:50 — heading
- 0000038725-26-000051:8k_2_02:51 — adjusted operating income reconciliation, amounts only; the settlement add-back is covered by `earnings_quality_adjusted_eps_settlement_add_back_gross_of_tax`

### Item 4 (no auditor's report in input)
- 0000038725-26-000055:item_4_controls:1 — heading
- 0000038725-26-000055:item_4_controls:2 — standard conclusion that disclosure controls are effective; no change in substance
- 0000038725-26-000055:item_4_controls:3 — standard statement of no change in ICFR; no change in substance
- 0000038725-26-000055:item_4_controls:4 — page number

### MD&A
- 0000038725-26-000055:mdna:2 — period rolled forward
- 0000038725-26-000055:mdna:5 — heading, period rolled forward
- 0000038725-26-000055:mdna:7 — amounts rolled forward; the sales drivers are the ones itemized from mdna:10 and mdna:25
- 0000038725-26-000055:mdna:11 — table, amounts only
- 0000038725-26-000055:mdna:12 — table, amounts only
- 0000038725-26-000055:mdna:17 — amounts rolled forward; drivers (volume, price) given with no new cause
- 0000038725-26-000055:mdna:18 — amounts rolled forward; product and regional sources named, no new matter
- 0000038725-26-000055:mdna:19 — heading only
- 0000038725-26-000055:mdna:20 — amounts rolled forward; the acquisitions driver reflects Benson Pump, covered by the acquisition items
- 0000038725-26-000055:mdna:22 — table, amounts only
- 0000038725-26-000055:mdna:23 — table, amounts only
- 0000038725-26-000055:mdna:27 — amounts rolled forward; driver (expense from acquisitions) stated with no new matter
- 0000038725-26-000055:mdna:28 — new heading for the section itemized from mdna:29
- 0000038725-26-000055:mdna:31 — amounts rolled forward; cause ("continued manufacturing realignment") repeated
- 0000038725-26-000055:mdna:33 — amounts only
- 0000038725-26-000055:mdna:34 — table, amounts only
- 0000038725-26-000055:mdna:35 — table, amounts only
- 0000038725-26-000055:mdna:41 — amounts rolled forward; cause (higher sales, 2025 cost actions) repeated
- 0000038725-26-000055:mdna:43 — amounts rolled forward; standing explanation of the deferral of intersegment profit
- 0000038725-26-000055:mdna:47 — amounts only
- 0000038725-26-000055:mdna:49 — amounts rolled forward; same currency cause (Argentine Peso, Turkish Lira)
- 0000038725-26-000055:mdna:51 — same discrete-tax wording as notes:68 (item `earnings_quality_unfavorable_discrete_tax_events_not_described`)
- 0000038725-26-000055:mdna:53 — amounts only
- 0000038725-26-000055:mdna:56 — date rolled forward
- 0000038725-26-000055:mdna:57 — amounts and date rolled forward
- 0000038725-26-000055:mdna:58 — date rolled forward
- 0000038725-26-000055:mdna:59 — date rolled forward
- 0000038725-26-000055:mdna:60 — cross-reference wording only
- 0000038725-26-000055:mdna:62 — amounts only
- 0000038725-26-000055:mdna:64 — date rolled forward
- 0000038725-26-000055:mdna:65 — table, amounts only
- 0000038725-26-000055:mdna:71 — amounts rolled forward; cause (less acquisition activity) restated for the period
- 0000038725-26-000055:mdna:76 — page number

### Notes
- 0000038725-26-000055:notes:1 — period rolled forward (the note history confirms nothing else changed)
- 0000038725-26-000055:notes:2 — heading
- 0000038725-26-000055:notes:4 — heading
- 0000038725-26-000055:notes:5 — insufficient: marked as changed, prior wording not in input, no new substance visible
- 0000038725-26-000055:notes:6 — insufficient: marked as changed, prior wording not in input, no new substance visible
- 0000038725-26-000055:notes:7 — insufficient: marked as changed, prior wording not in input, no new substance visible
- 0000038725-26-000055:notes:9 — heading (new subheading for the year)
- 0000038725-26-000055:notes:10 — heading
- 0000038725-26-000055:notes:13 — table introduction
- 0000038725-26-000055:notes:14 — table, amounts only
- 0000038725-26-000055:notes:17 — heading
- 0000038725-26-000055:notes:20 — standard omission as immaterial; covered by the Benson Pump items
- 0000038725-26-000055:notes:21 — heading
- 0000038725-26-000055:notes:28 — insufficient: Barnes contribution disclosure, prior wording not in input, no new matter visible
- 0000038725-26-000055:notes:32 — amounts only
- 0000038725-26-000055:notes:34 — table, amounts only
- 0000038725-26-000055:notes:35 — amounts only
- 0000038725-26-000055:notes:36 — date rolled forward
- 0000038725-26-000055:notes:37 — table, amounts only; its acquisition rows reflect the two 2026 acquisitions itemized above
- 0000038725-26-000055:notes:40 — heading
- 0000038725-26-000055:notes:41 — table, amounts only (per the note history)
- 0000038725-26-000055:notes:42 — heading
- 0000038725-26-000055:notes:43 — date rolled forward (per the note history)
- 0000038725-26-000055:notes:44 — heading
- 0000038725-26-000055:notes:45 — date rolled forward (per the note history)
- 0000038725-26-000055:notes:46 — heading
- 0000038725-26-000055:notes:47 — standing credit agreement terms; no change entry in the note history
- 0000038725-26-000055:notes:48 — amounts only (per the note history)
- 0000038725-26-000055:notes:49 — heading
- 0000038725-26-000055:notes:50 — standing Project Bond terms; no change entry in the note history
- 0000038725-26-000055:notes:51 — amounts only; "credits" corrected to "credit"
- 0000038725-26-000055:notes:53 — standing language on ordinary-course claims; no change entry in the note history
- 0000038725-26-000055:notes:54 — amounts and date only (per the note history)
- 0000038725-26-000055:notes:55 — period rolled forward (per the note history)
- 0000038725-26-000055:notes:56 — warranty table, amounts only (per the note history)
- 0000038725-26-000055:notes:57 — period rolled forward
- 0000038725-26-000055:notes:59 — table, amounts only; the NCI dividend row is covered by the notes:58 item
- 0000038725-26-000055:notes:60 — period rolled forward
- 0000038725-26-000055:notes:61 — table, amounts only
- 0000038725-26-000055:notes:62 — standing footnote, wording only
- 0000038725-26-000055:notes:64 — period rolled forward
- 0000038725-26-000055:notes:65 — table, amounts only
- 0000038725-26-000055:notes:66 — period rolled forward
- 0000038725-26-000055:notes:67 — table, amounts only
- 0000038725-26-000055:notes:72 — table, amounts only
- 0000038725-26-000055:notes:73 — amounts only
- 0000038725-26-000055:notes:74 — amounts only; the swap is still recorded in SG&A
- 0000038725-26-000055:notes:75 — amounts only
- 0000038725-26-000055:notes:76 — standing fair value text (split across a page break)
- 0000038725-26-000055:notes:77 — standing fair value text (continuation)
- 0000038725-26-000055:notes:81 — date rolled forward
- 0000038725-26-000055:notes:82 — table, amounts; the new share swap row is covered by the notes:83 item
- 0000038725-26-000055:notes:87 — table introduction
- 0000038725-26-000055:notes:88 — segment table, amounts; the new legal settlement row is covered by the settlement items
- 0000038725-26-000055:notes:89 — prior-year segment table, amounts only
- 0000038725-26-000055:notes:90 — segment table, amounts; the legal settlement row is covered by the settlement items
- 0000038725-26-000055:notes:91 — prior-year segment table, amounts only
- 0000038725-26-000055:notes:92 — table, amounts only
- 0000038725-26-000055:notes:93 — period wording
- 0000038725-26-000055:notes:95 — table, amounts only
- 0000038725-26-000055:notes:96 — date rolled forward; no trading arrangements

### How the note history maps to the notes (not a separate list)
- History 0000038725-26-000055:note_history:1 is notes:52.
- :2 is notes:54.
- :3 is notes:55.
- :4 is notes:56.
- :6 is notes:1.
- :7 and :12 are notes:41.
- :8 is notes:43.
- :9 is notes:45.
- :10 is notes:48.
- :11 is notes:51.
- The removed prior paragraph, 0000038725-26-000026:note_history:5, is the source of item `related_parties_contingencies_and_subsequent_events_esso_expert_damages_and_warning_removed`.

## Counts
- Items: 35.
- Insufficient: 4 (notes:5, notes:6, notes:7, notes:28).
