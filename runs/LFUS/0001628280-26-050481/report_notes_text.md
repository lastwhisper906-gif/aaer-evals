<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# report_notes_text — LFUS 10-Q 0001628280-26-050481 (quarter ended June 27, 2026)

## Input check

- Read in full: input_notes.md (all 972 lines), input_mdna.md, input_controls.md, input_8k.md (8-K 0001628280-26-050382, Item 2.02 / Ex. 99.1), input_notes_history.md, input_prior_predictions.md.
- Not in the input, so nothing to read: an auditor's report (no review report is carried for this 10-Q), an Item 1A diff, an Exhibit 21 diff, and any Exhibit 10.
- Nothing forbidden is present. There is no trend table, no prices, no returns, no short interest, no other company's files, no prior probability and no outcome window. The 8-K earnings release has the company's own statement tables. Those are part of the 8-K body. I read them as text and did no arithmetic on them.
- Prior flags: none on record.
- The 8-K index lines (item codes and the 2025 NT 10-K) list codes only, with no bodies. None of them is dated after the prior 10-Q except the release read here.
- Every amount below is quoted as stated. I did not add, subtract, compare or compute any figure.

## Items

```json
{ "id": "estimates_and_discretion_semiconductor_site_closure_fixed_asset_impairment",
  "what_changed": "New this quarter. The restructuring note now reports fixed asset impairment charges of $13.1 million recognized in the second quarter of 2026. The charges are primarily related to the announced closure and/or disposition of two manufacturing sites for the semiconductor business within the Electronics segment. The same sentence is added to the PP&E note (notes:64), the segment footnote (notes:183) and MD&A (mdna:15, mdna:28, mdna:29, mdna:44). The same paragraph attributes the period's restructuring charges to reorganizations of the semiconductor business (Electronics) and the commercial vehicle business (Transportation). An announced closure or disposition implies further exit costs, such as terminations and other restructuring charges, as the sites close.",
  "account": "Restructuring, impairment, and other charges",
  "expected_direction": "up",
  "horizon": "this quarter; further closure costs over 12 months",
  "quote": "In addition, during the second quarter of 2026, the Company recognized fixed asset impairment charges of $13.1 million, primarily related to the announced closure and/or disposition of two manufacturing sites for the semiconductor business within the Electronics segment.",
  "paragraph_id": "0001628280-26-050481:notes:85",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_level_three_nonrecurring_impairment_measurement",
  "what_changed": "New 'Impairments' paragraph in the fair value note. The impaired semiconductor site assets were measured at fair value on a nonrecurring basis, using significant unobservable (Level 3) inputs. The note still says no non-financial assets are measured at fair value on a recurring basis (notes:142). This paragraph adds a nonrecurring measurement that rests on management's estimate.",
  "account": "Net property, plant, and equipment",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "The related assets were measured at fair value on a nonrecurring basis using valuation techniques that incorporated significant unobservable inputs, which are classified within Level 3 of the fair value hierarchy.",
  "paragraph_id": "0001628280-26-050481:notes:150",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_basler_opening_receivables_and_inventory_reduced",
  "what_changed": "The Basler acquisition note now states six-month measurement-period adjustments. They reduce the fair values first assigned to acquired intangible assets ($5.0 million), current liabilities ($3.2 million), inventories ($2.6 million), trade receivables ($2.1 million), PP&E ($1.7 million) and other long-term assets ($1.6 million), and increase other current assets ($1.2 million). The prose gives measurement-period fair value adjustments as the cause of the lower acquired receivables and inventory values.",
  "account": "Trade receivables and inventories (Basler opening balances)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "the Company made adjustments to reduce the fair value of intangible assets of $5.0 million, current liabilities of $3.2 million, inventories of $2.6 million, trade receivables of $2.1 million, property, plant, and equipment of $1.7 million",
  "paragraph_id": "0001628280-26-050481:notes:39",
  "explanation": true }
```

```json
{ "id": "estimates_and_discretion_basler_measurement_period_goodwill_increase",
  "what_changed": "The same paragraph states that these measurement-period adjustments increased Basler goodwill by $8.6 million. The goodwill roll-forward (notes:67) has a matching Industrial 'Adjustments' line.",
  "account": "Goodwill",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "As a result of these adjustments, goodwill was increased by $8.6 million.",
  "paragraph_id": "0001628280-26-050481:notes:39",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_basler_allocation_preliminary_tangible_assets",
  "what_changed": "The Basler purchase price allocation is still described as preliminary. The open element it names is the third-party valuation of acquired tangible assets. MD&A (mdna:102) still says the $353.1 million consideration is subject to a working capital adjustment. Further measurement-period changes to PP&E and goodwill remain possible until the measurement period closes; the acquisition was completed December 11, 2025. The prior-quarter wording is not in the input, so I cannot tell whether the named open element has narrowed.",
  "account": "Goodwill; Net property, plant, and equipment",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "valuation of acquired tangible assets, is not yet finalized",
  "paragraph_id": "0001628280-26-050481:notes:35",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_basler_indebtedness_paid_as_consideration",
  "what_changed": "New period amounts in the prose: $0.3 million (three months) and $2.8 million (six months) of Basler indebtedness paid as part of the purchase consideration. MD&A (mdna:112) reports the $2.8 million in investing activities as a payment for the Basler acquisition.",
  "account": "Acquisitions of businesses, net of cash acquired",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "The Company paid $0.3 million and $2.8 million of indebtedness as part of the purchase consideration during the three and six months ended June 27, 2026, respectively.",
  "paragraph_id": "0001628280-26-050481:notes:39",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_polytronics_equity_investment_sold",
  "what_changed": "New. The Company sold its Level 1 equity investment in Polytronics Technology Corporation during the second quarter for net proceeds of $7.4 million. The proceeds are classified in investing cash flow under net proceeds from sale of property, plant and equipment, and other (also stated at mdna:112). The holding had been carried at last sales price in Investments and Other long-term assets.",
  "account": "Investments",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "during the three months ended June 27, 2026, with net proceeds of $7.4 million and is recognized in Net proceeds from sale of property, plant and equipment, and other in investing activities",
  "paragraph_id": "0001628280-26-050481:notes:122",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_basler_asset_held_for_sale_proceeds",
  "what_changed": "New. MD&A states $1.7 million of proceeds in the six months from an asset held for sale that came with the Basler acquisition.",
  "account": "Net proceeds from sale of property, plant and equipment, and other",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "$1.7 million from an asset held for sale from the Basler acquisition during the six months ended June 27, 2026",
  "paragraph_id": "0001628280-26-050481:mdna:112",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_uk_pension_settlement_charge_expected_timing",
  "what_changed": "The UK pension paragraph is carried as changed text. It now states that the one-time non-cash settlement charge from the group annuity contract is expected in the first quarter of 2027, estimated at between $6 million and $8 million. The prior-quarter wording is not in the input, so I cannot tell whether the expected quarter or the range has moved.",
  "account": "Other income, net (pension settlement charge)",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "settlement charge in the first quarter of 2027 estimated between $6 million and $8 million",
  "paragraph_id": "0001628280-26-050481:notes:156",
  "explanation": false }
```

```json
{ "id": "earnings_quality_discrete_tax_benefits_lower_effective_rate",
  "what_changed": "The tax note gives the reasons the 2026 effective tax rate was lower, for both the three and the six months. The main reasons are statute-of-limitations lapses on previously unrecognized tax benefits and excess tax benefits on share based compensation recognized in 2026. The note also cites 2025 foreign exchange losses that carried no tax benefit. The 2026 reasons are discrete items. MD&A (mdna:37) carries the same text, and MD&A reports $75.6 million of stock-award proceeds for the six months (mdna:114).",
  "account": "Income taxes (effective tax rate)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "primarily due to lapses in the statute of limitations for previously unrecognized tax benefits and excess tax benefits for share based compensation recognized in 2026",
  "paragraph_id": "0001628280-26-050481:notes:167",
  "explanation": false }
```

```json
{ "id": "across_documents_statute_lapse_tax_benefit_quarter_placement",
  "what_changed": "The 8-K footnote places the $2.7 million statute-lapse tax benefit in the first quarter of 2026. The 10-Q tax note (notes:167) and MD&A (mdna:37), however, cite statute-of-limitations lapses as a reason the rate was lower for the three months ended June 27, 2026, as well as for the six months. For the supervisor to reconcile whether any statute-lapse benefit fell in the second quarter.",
  "account": "Income taxes",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "including $2.7 million of tax benefits due to lapses in the statute of limitations for previously unrecognized tax benefits recognized in the first quarter of 2026",
  "paragraph_id": "0001628280-26-050382:8k_2_02:91",
  "explanation": false }
```

```json
{ "id": "earnings_quality_indemnification_receivable_reversal_paired_with_tax_benefit",
  "what_changed": "The 8-K states that 2026 other income includes the reversal of a $2.7 million indemnification receivable. The reversal relates to the statute-of-limitations lapses behind the $2.7 million tax benefit, and both were recognized in the first quarter of 2026. The reversal is treated as a non-GAAP adjustment. The 10-Q text carried here (notes:167, mdna:37) cites the statute lapses as a tax-rate driver but does not mention the indemnification receivable reversal.",
  "account": "Other income, net",
  "expected_direction": "down",
  "horizon": "this quarter (six-month period)",
  "quote": "2026 included the reversal of an indemnification receivable of $2.7 million related to lapses in the statute of limitations for previously unrecognized tax benefits recognized in the first quarter of 2026",
  "paragraph_id": "0001628280-26-050382:8k_2_02:90",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_second_quarter_exceeded_expectations",
  "what_changed": "The CEO states that second-quarter performance exceeded the company's own expectations. He cites broad-based demand strength and disciplined execution.",
  "account": "Net sales",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "We delivered strong second quarter results, with performance exceeding our expectations",
  "paragraph_id": "0001628280-26-050382:8k_2_02:15",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_third_quarter_sales_and_eps_guidance",
  "what_changed": "New third-quarter 2026 guidance, based on current market conditions: net sales in the range of $780 to $800 million, adjusted diluted EPS of $4.85 to $5.05, and an adjusted effective tax rate of approximately 23% to 24%.",
  "account": "Net sales",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "Net sales in the range of $780",
  "paragraph_id": "0001628280-26-050382:8k_2_02:19",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_record_bookings_behind_third_quarter_growth",
  "what_changed": "Management expects approximately 26% total revenue growth over the prior-year third quarter. It attributes this to record bookings, continued customer momentum and Basler contributions. The 'record bookings' demand statement does not appear in the 10-Q paragraphs carried as text.",
  "account": "Net sales",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "we expect approximately 26% total revenue growth versus the prior year, supported by record bookings, continued customer momentum, and contributions from the Basler acquisition",
  "paragraph_id": "0001628280-26-050382:8k_2_02:16",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_covenant_ebitda_restructuring_addback",
  "what_changed": "The 8-K states that the Q1 2026 Credit Agreement amendment now lets restructuring charges and business optimization expenses be added back in covenant Consolidated EBITDA. Restructuring and site-closure charges are now being recognized (notes:85), so these add-backs enter the leverage covenant measure. The 8-K reports the Consolidated Net Leverage Ratio against a 3.50:1.00 event-of-default trigger.",
  "account": "Consolidated EBITDA (credit agreement definition)",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "The Credit Agreement was amended in Q1 2026 and now allows to add restructuring charges and business optimization expenses in addition to the prior credit agreement.",
  "paragraph_id": "0001628280-26-050382:8k_2_02:84",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_dividend_raised_after_quarter_end",
  "what_changed": "Subsequent event. On July 29, 2026 the Company declared a quarterly dividend of $0.80 per share, described as a 7% increase, payable September 3, 2026. The 8-K also reports it at :13 and :33, citing the prior $0.75 dividend. Second-quarter dividends paid are stated as $19.0 million.",
  "account": "Cash dividends paid",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "the Company announced the declaration of a quarterly cash dividend of $0.80 per share, a 7% increase from the first quarter, payable on September 3, 2026",
  "paragraph_id": "0001628280-26-050481:mdna:105",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_stock_award_exercise_proceeds",
  "what_changed": "New in the financing discussion: $75.6 million of net proceeds from stock-based award activities in the six months ended June 27, 2026, against $0.6 million in the prior-year period, as stated. No shares were repurchased in 2026 (mdna:116). This bears on the excess tax benefits on share based compensation cited in the tax note, and on the diluted share count.",
  "account": "Financing cash flows (stock-based award proceeds); shares outstanding",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The Company received $75.6 million of net proceeds related to stock",
  "paragraph_id": "0001628280-26-050481:mdna:114",
  "explanation": false }
```

```json
{ "id": "earnings_quality_annual_incentive_expense_drives_sga",
  "what_changed": "MD&A attributes the second-quarter SG&A increase of $25.1 million to higher annual incentive expenses and to $11.7 million of incremental Basler operating expenses. Higher annual incentive expense is named as a driver.",
  "account": "Selling, general, and administrative expenses",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "higher selling, general, and administrative expenses of $25.1 million due to higher annual incentive expenses and incremental operating expenses of $11.7 million from the Basler acquisition",
  "paragraph_id": "0001628280-26-050481:mdna:28",
  "explanation": false }
```

```json
{ "id": "earnings_quality_net_sales_volume_and_favorable_price",
  "what_changed": "MD&A explains the second-quarter net sales increase. Apart from $35.8 million from Basler and $4.1 million of FX, it attributes the increase to higher volume of $44.7 million in electronics products and $26.1 million in semiconductor, driven by higher end market demand and favorable price. Industrial circuit protection volume also contributed. Favorable price is named as a driver alongside volume.",
  "account": "Net sales",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "higher volume of $44.7 million and $26.1 million in the electronics products and semiconductor businesses within the Electronics segment, respectively, driven by higher end market demand and favorable price",
  "paragraph_id": "0001628280-26-050481:mdna:19",
  "explanation": false }
```

```json
{ "id": "earnings_quality_gross_margin_price_execution_mix",
  "what_changed": "MD&A attributes the higher second-quarter gross profit and gross margin to higher volume and favorable price, operational execution and favorable product mix in Electronics and in industrial circuit protection. It also cites Basler's higher gross margin.",
  "account": "Gross profit / gross margin",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "were primarily due to higher volume and favorable price, operational execution, and favorable product mix from the Electronics segment and the industrial circuit protection business within the Industrial segment",
  "paragraph_id": "0001628280-26-050481:mdna:25",
  "explanation": false }
```

```json
{ "id": "earnings_quality_electronics_margin_volume_leverage",
  "what_changed": "MD&A states that the Electronics operating margin increased from 14.9% to 21.4% in the second quarter. It cites volume leverage, operational execution, and favorable price and product mix across electronics products and semiconductor. The overview (mdna:9) names Electronics operating income as the main driver of the consolidated net income increase.",
  "account": "Electronics segment operating income",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Operating margins increased from 14.9% in the second quarter of 2025 to 21.4% in the second quarter of 2026 primarily due to volume leverage, operational execution and favorable price and product mix from the electronics products and the semiconductor businesses.",
  "paragraph_id": "0001628280-26-050481:mdna:51",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_commercial_vehicle_cost_inflation_mix",
  "what_changed": "MD&A states that Transportation operating income decreased in the second quarter. The main cause given is lower gross margin in the commercial vehicle business, hit by cost inflation and unfavorable product mix. The restructuring note (notes:85) names a reorganization of commercial vehicle manufacturing, selling and administrative functions. The 8-K (:28) cites lower commercial vehicle profitability.",
  "account": "Transportation segment operating income",
  "expected_direction": "down",
  "horizon": "this quarter; next quarter",
  "quote": "The decrease in operating income was primarily due to lower gross margin from the commercial vehicles business impacted by cost inflation and unfavorable product mix.",
  "paragraph_id": "0001628280-26-050481:mdna:58",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_automotive_sensor_strategic_exit",
  "what_changed": "MD&A states that Transportation's second-quarter sales growth came from commercial vehicle volume in the Asia region. This was partly offset by lower automotive sensors volume, driven by the strategic exit of certain lower margin products. A deliberate product exit implies automotive sensor sales stay lower while the exit runs.",
  "account": "Automotive Sensors net sales",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "partially offset by lower volume from the automotive sensors business driven by the strategic exit of certain lower margin products",
  "paragraph_id": "0001628280-26-050481:mdna:55",
  "explanation": false }
```

```json
{ "id": "across_documents_passenger_vehicle_decline_attribution",
  "what_changed": "The press release attributes passenger vehicle weakness to lower global passenger car builds and auto sensor product declines. The 10-Q MD&A (mdna:55) attributes the automotive sensor decline to the strategic exit of certain lower margin products and does not cite car builds for the quarter. The two documents frame the same decline differently: one as market-driven, the other as elective.",
  "account": "Passenger vehicle net sales (passenger car and auto sensor products)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "Passenger vehicle sales were impacted by lower global passenger car builds and auto sensor product declines.",
  "paragraph_id": "0001628280-26-050382:8k_2_02:27",
  "explanation": false }
```

```json
{ "id": "earnings_quality_basler_amortization_lowers_industrial_margin",
  "what_changed": "MD&A states that the Industrial operating margin decreased from 19.2% to 18.3% in the second quarter because of $2.9 million of higher amortization related to Basler. Improved industrial circuit protection gross margin partly offset this. Basler intangible amortization is a continuing charge on the segment. The 8-K reports the Industrial adjusted EBITDA margin, which excludes amortization, separately (:31).",
  "account": "Industrial segment operating margin",
  "expected_direction": "down",
  "horizon": "this quarter; 12 months",
  "quote": "Operating margins decreased from 19.2% in the second quarter of 2025 to 18.3% in the second quarter of 2026 due to higher amortization expenses of $2.9 million, or 2.0% related to the Basler acquisition",
  "paragraph_id": "0001628280-26-050481:mdna:65",
  "explanation": false }
```

```json
{ "id": "earnings_quality_industrial_sales_basler_contribution",
  "what_changed": "MD&A states that the second-quarter Industrial net sales increase includes $35.8 million, or 36.4%, of incremental Basler sales and $0.2 million of unfavorable FX. The rest came from industrial circuit protection volume. The 8-K (:30) cites data center, HVAC, industrial automation and construction demand for organic growth.",
  "account": "Industrial segment net sales",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "including $35.8 million, or 36.4% of incremental net sales from the Basler acquisition",
  "paragraph_id": "0001628280-26-050481:mdna:62",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_europe_semiconductor_passenger_car_volume",
  "what_changed": "MD&A states that Europe's second-quarter increase included $3.5 million of favorable FX. It was partly offset by lower volume in Europe in passenger car products (Transportation) and in semiconductor (Electronics).",
  "account": "Net sales, Europe (semiconductor and passenger car products)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "partially offset by lower volume from the passenger car products business within the Transportation segment and the semiconductor business within the Electronics segment",
  "paragraph_id": "0001628280-26-050481:mdna:77",
  "explanation": false }
```

```json
{ "id": "earnings_quality_pretax_income_foreign_exchange_swing",
  "what_changed": "Beyond the operating factors, MD&A names a primary benefit to pretax income: foreign exchange gains in Q2 2026, set against foreign exchange losses in Q2 2025. This is a non-operating item, and the 8-K excludes it as a non-GAAP adjustment.",
  "account": "Foreign exchange (gain) loss",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "income before income taxes was primarily benefited by foreign exchange gains of $0.2 million in the second quarter of 2026 compared to foreign exchange losses of $10.4 million in the second quarter of 2025",
  "paragraph_id": "0001628280-26-050481:mdna:34",
  "explanation": false }
```

```json
{ "id": "earnings_quality_operating_cash_flow_attributed_to_cash_earnings",
  "what_changed": "MD&A attributes the six-month operating cash flow increase of $78.2 million mainly to higher cash earnings. The paragraph does not discuss receivables, inventories or payables. The same sentence appears at mdna:10.",
  "account": "Net cash provided by operating activities",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The increase in net cash provided by operating activities of $78.2 million was primarily due to higher cash earnings.",
  "paragraph_id": "0001628280-26-050481:mdna:110",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_collar_gains_to_earnings_next_year",
  "what_changed": "The collar hedge paragraph restates its estimate as of June 27, 2026: approximately $3.9 million of pre-tax gains in accumulated other comprehensive loss are expected to be recognized in earnings over the next 12 months. Per notes:137, collar gains are classified in cost of sales and SG&A.",
  "account": "Cost of sales",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "As of June 27, 2026, the Company estimates that approximately $3.9 million of",
  "paragraph_id": "0001628280-26-050481:notes:130",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_interest_swap_gains_to_earnings_next_year",
  "what_changed": "The interest rate swap paragraph restates its estimate as of June 27, 2026: approximately $2.2 million of pre-tax gains in accumulated other comprehensive loss are expected to be recognized in earnings over the next 12 months. Per notes:137, swap gains reduce interest expense. The swap covers SOFR loans scheduled to mature June 30, 2027, while the revolver now matures March 12, 2031.",
  "account": "Interest expense",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "As of June 27, 2026, the Company estimates that approximately $2.2 million of",
  "paragraph_id": "0001628280-26-050481:notes:132",
  "explanation": false }
```

## Paragraphs carried as text and not made into items

### Notes (0001628280-26-050481:notes)

- notes:3 — insufficient: the company description is carried as changed text, but the prior wording is not in the input, so the change can't be identified
- notes:8 — date rolled forward
- notes:9 — amounts only (revenue disaggregation, current year)
- notes:10 — amounts only (revenue disaggregation, prior year)
- notes:23 — date rolled forward
- notes:24 — amounts only
- notes:25 — insufficient: heading carried as changed text; what changed can't be identified
- notes:26 — insufficient: states ASU 2025-05 was adopted with no material impact; prior wording not in input and no effect stated
- notes:27 — heading
- notes:28 — insufficient: ASU 2025-06 still under evaluation; prior wording not in input
- notes:29 — insufficient: ASU 2024-03 (disclosure only) under evaluation; prior wording not in input
- notes:30 — insufficient: ASU 2023-06 under evaluation; prior wording not in input
- notes:37 — amounts only (purchase price allocation table; the adjustments are itemized from notes:39)
- notes:40 — restates a Q1 fact (Basler step-up fully amortized by Q1 2026); no new amount
- notes:41 — period and amounts rolled forward (Basler fees)
- notes:48 — prior-year comparative (Dortmund step-down); wording only
- notes:49 — prior-year comparative; period rolled forward
- notes:52 — amounts only (pro forma)
- notes:54 — amounts only (pro forma adjustments)
- notes:55 — period rolled forward
- notes:56 — wording and period only; restates the Q1 step-up amortization
- notes:57 — period rolled forward
- notes:59 — date rolled forward
- notes:60 — amounts only (inventory components and reserves)
- notes:62 — date rolled forward
- notes:63 — amounts only
- notes:64 — depreciation amounts rolled forward; the added impairment sentence is the change itemized at notes:85
- notes:66 — date rolled forward
- notes:67 — amounts only (goodwill roll-forward; the adjustment is explained at notes:39)
- notes:69 — date rolled forward
- notes:70 — amounts only
- notes:74 — amounts only
- notes:75 — date rolled forward
- notes:76 — amounts only
- notes:78 — date rolled forward
- notes:79 — amounts only (accrued liabilities)
- notes:81 — heading; period rolled forward
- notes:82 — amounts only (current-year restructuring and impairment table)
- notes:83 — amounts only (prior-year table)
- notes:87 — prior-year comparative; period rolled forward
- notes:88 — amounts and date rolled forward (restructuring reserve; payment-timing sentence)
- notes:89 — heading
- notes:90 — date rolled forward (per note change history)
- notes:91 — amounts only (per note change history)
- notes:92 — heading
- notes:93 — unchanged per note change history (Credit Agreement entered in Q1)
- notes:94 — date rolled forward (per history)
- notes:95 — unchanged per history
- notes:96 — unchanged per history
- notes:97 — paragraph re-segmented only (per history)
- notes:98 — wording only ('on the hedged portion' became 'with the hedge')
- notes:99 — amounts and date rolled forward (letters of credit, availability); covenant compliance statement unchanged
- notes:100 — heading
- notes:101 — period rolled forward; now reads 'three and six months' for the $2.2 million March 12 costs (wording only)
- notes:102 — heading
- notes:103 — unchanged per history
- notes:104 — unchanged per history
- notes:105 — wording only ('first fiscal quarter' became 'first quarter')
- notes:106 — unchanged per history
- notes:107 — unchanged per history
- notes:108 — unchanged per history
- notes:109 — date rolled forward and re-segmented (per history)
- notes:110 — unchanged per history
- notes:111 — amounts and period rolled forward (interest paid)
- notes:124 — period rolled forward
- notes:126 — period and amounts rolled forward; the cross-currency swaps were entered in February 2026 (Q1)
- notes:129 — table rows added for new monthly collar trades; dates and rates only
- notes:134 — date rolled forward
- notes:135 — amounts only
- notes:136 — period rolled forward
- notes:137 — amounts only
- notes:138 — period rolled forward
- notes:139 — amounts only
- notes:142 — date rolled forward
- notes:143 — date rolled forward
- notes:144 — amounts only
- notes:147 — date rolled forward
- notes:148 — date rolled forward
- notes:149 — amounts only
- notes:153 — period rolled forward
- notes:154 — amounts only
- notes:157 — amounts and period rolled forward
- notes:159 — amounts only
- notes:161 — period rolled forward
- notes:162 — amounts only
- notes:163 — amounts only
- notes:164 — period rolled forward
- notes:165 — amounts only
- notes:168 — restates the drivers itemized at notes:167, this time against the statutory rate; non-U.S. losses without tax benefit are also cited for 2025
- notes:171 — amounts only
- notes:172 — amounts and period rolled forward
- notes:173 — heading
- notes:174 — period rolled forward (still no repurchases)
- notes:182 — amounts only
- notes:183 — same impairment sentence as the item at notes:85; restructuring amounts rolled forward
- notes:184 — prior-year comparative
- notes:186 — period rolled forward
- notes:187 — amounts only
- notes:189 — amounts only
- notes:191 — amounts only
- notes:193 — amounts only
- notes:195 — heading
- notes:196 — date rolled forward (per history)
- notes:197 — heading
- notes:198 — unchanged per note change history
- notes:199 — unchanged per note change history
- notes:200 — unchanged per note change history. Customer fuse recall status carried forward: loss reasonably possible, no accrual, range not determinable
- notes:201 — heading
- notes:202 — unchanged per history
- notes:203 — heading
- notes:204 — unchanged per history
- notes:205 — unchanged per history
- notes:206 — heading
- notes:207 — date rolled forward (per history)
- notes:208 — heading
- notes:209 — unchanged per history
- notes:210 — unchanged per history
- notes:211 — unchanged per history
- notes:212 — unchanged per history
- notes:213 — amounts only (related-party table, per history)

### MD&A (0001628280-26-050481:mdna)

- mdna:2 — heading
- mdna:6 — insufficient: company description, same text as notes:3
- mdna:9 — overview restating Q2 results; its drivers are itemized at mdna:19 and mdna:51
- mdna:10 — same sentence as mdna:110 (itemized)
- mdna:11 — restates the Credit Agreement entered in Q1; no new substance (notes counterpart unchanged per history)
- mdna:15 — table lead-in: impairment itemized at notes:85; restructuring and fee amounts rolled forward; Q1 step-up restated
- mdna:16 — prior-year comparative
- mdna:17 — amounts only
- mdna:20 — six-month restatement of the mdna:19 drivers
- mdna:22 — cost-of-sales restatement of the margin drivers itemized at mdna:25; Basler cost amount
- mdna:23 — six-month restatement; Q1 step-up charge restated
- mdna:26 — six-month restatement of mdna:25
- mdna:29 — six-month restatement of mdna:28; impairment itemized at notes:85
- mdna:31 — consolidated operating income, restating drivers itemized at mdna:25, mdna:28 and notes:85
- mdna:32 — six-month restatement
- mdna:35 — six-month restatement of mdna:34
- mdna:37 — same text as notes:167 (itemized)
- mdna:38 — same text as notes:168
- mdna:42 — amounts only
- mdna:43 — amounts only
- mdna:44 — same footnote as notes:183; impairment itemized at notes:85
- mdna:45 — prior-year comparative
- mdna:48 — Electronics sales, restating the drivers itemized at mdna:19
- mdna:49 — six-month restatement
- mdna:52 — six-month restatement of mdna:51
- mdna:56 — six-month restatement of mdna:55
- mdna:59 — six-month restatement (passenger car driver for the six months)
- mdna:63 — six-month restatement of mdna:62
- mdna:66 — six-month restatement of mdna:65
- mdna:69 — amounts only
- mdna:71 — Americas: geographic restatement of the segment drivers and the Basler contribution
- mdna:72 — six-month Americas restatement
- mdna:74 — Asia: geographic restatement of the segment drivers
- mdna:75 — six-month Asia restatement
- mdna:78 — six-month Europe restatement
- mdna:81 — amounts and date rolled forward (cash, and cash held by U.S. subsidiaries)
- mdna:82 — heading
- mdna:83 — same as notes:93; unchanged per history
- mdna:84 — date rolled forward (same as notes:94)
- mdna:85 — same as notes:95; unchanged
- mdna:88 — wording only (same as notes:98)
- mdna:89 — amounts and date rolled forward (same as notes:99)
- mdna:92 — same as notes:104; unchanged
- mdna:93 — wording only (same as notes:105)
- mdna:94 — same as notes:106; unchanged
- mdna:95 — same as notes:107; unchanged
- mdna:97 — same as the first part of notes:109; re-segmented only
- mdna:99 — heading
- mdna:100 — date rolled forward; covenant compliance expectation unchanged
- mdna:102 — restates the Basler terms; the consideration and working-capital status are folded into the item at notes:35
- mdna:107 — amounts only
- mdna:116 — period rolled forward (same as notes:174)
- mdna:118 — date rolled forward (same as notes:196)
- mdna:121 — period rolled forward; states no change in critical accounting policies

### Item 4 (0001628280-26-050481:item_4_controls)

- item_4_controls:1 — heading
- item_4_controls:2 — heading
- item_4_controls:3 — boilerplate definition
- item_4_controls:4 — page number
- item_4_controls:5 — date rolled forward; conclusion ('effective') unchanged
- item_4_controls:6 — heading
- item_4_controls:7 — date rolled forward; no ICFR changes reported

### 8-K Item 2.02, Ex. 99.1 (0001628280-26-050382:8k_2_02)

- 8k_2_02:1 — exhibit cover
- 8k_2_02:2 — document label
- 8k_2_02:3 — exhibit label
- 8k_2_02:4 — contact block
- 8k_2_02:5 — headline
- 8k_2_02:6 — heading
- 8k_2_02:7 — heading note
- 8k_2_02:8 — amounts only (headline sales and organic growth); drivers itemized from MD&A
- 8k_2_02:9 — amounts only (cash flow, free cash flow)
- 8k_2_02:10 — amounts only (year-to-date cash flow)
- 8k_2_02:11 — amounts only (EPS)
- 8k_2_02:12 — amounts only (margins)
- 8k_2_02:13 — same dividend increase as the mdna:105 item
- 8k_2_02:14 — release date and intro
- 8k_2_02:17 — heading
- 8k_2_02:18 — guidance lead-in
- 8k_2_02:20 — page marker
- 8k_2_02:21 — non-GAAP guidance boilerplate
- 8k_2_02:22 — heading
- 8k_2_02:23 — heading
- 8k_2_02:24 — Electronics commentary restating the drivers itemized at mdna:19; adds product detail only
- 8k_2_02:25 — Electronics adjusted EBITDA margin; amounts, with the same drivers as mdna:51
- 8k_2_02:26 — heading
- 8k_2_02:28 — Transportation margin driver, same as the mdna:58 item
- 8k_2_02:29 — heading
- 8k_2_02:30 — Industrial end-market detail, folded into the mdna:62 item
- 8k_2_02:31 — Industrial adjusted EBITDA margin; amounts
- 8k_2_02:32 — heading
- 8k_2_02:33 — same dividend increase as the mdna:105 item
- 8k_2_02:34 — heading
- 8k_2_02:35 — conference call logistics
- 8k_2_02:36 — page marker
- 8k_2_02:37 — heading
- 8k_2_02:38 — insufficient: company description, same text as notes:3
- 8k_2_02:39 — forward-looking statement boilerplate
- 8k_2_02:40 — boilerplate
- 8k_2_02:41 — page marker
- 8k_2_02:42 — heading
- 8k_2_02:43 — non-GAAP boilerplate
- 8k_2_02:44 — code
- 8k_2_02:45 — marker
- 8k_2_02:46 — address
- 8k_2_02:47 — heading
- 8k_2_02:48 — heading
- 8k_2_02:49 — amounts only (balance sheet)
- 8k_2_02:50 — heading
- 8k_2_02:51 — heading
- 8k_2_02:52 — label
- 8k_2_02:53 — amounts only (income statement)
- 8k_2_02:54 — heading
- 8k_2_02:55 — heading
- 8k_2_02:56 — label
- 8k_2_02:57 — amounts only (cash flow statement)
- 8k_2_02:58 — heading
- 8k_2_02:59 — heading
- 8k_2_02:60 — label
- 8k_2_02:61 — amounts only (segment table)
- 8k_2_02:62 — footnote boilerplate
- 8k_2_02:63 — label
- 8k_2_02:64 — amounts only (segment margins)
- 8k_2_02:65 — heading
- 8k_2_02:66 — heading
- 8k_2_02:67 — label
- 8k_2_02:68 — amounts only
- 8k_2_02:69 — amounts only
- 8k_2_02:70 — amounts only
- 8k_2_02:71 — amounts only
- 8k_2_02:72 — amounts only
- 8k_2_02:73 — amounts only
- 8k_2_02:74 — amounts only
- 8k_2_02:75 — amounts only
- 8k_2_02:76 — footnote definition
- 8k_2_02:77 — amounts only
- 8k_2_02:78 — amounts only
- 8k_2_02:79 — amounts only
- 8k_2_02:80 — footnote definition
- 8k_2_02:81 — amounts only
- 8k_2_02:82 — amounts only (net debt, consolidated EBITDA, leverage ratio)
- 8k_2_02:83 — covenant terms restated (3.50:1.00 trigger)
- 8k_2_02:85 — footnote definition
- 8k_2_02:86 — rounding note
- 8k_2_02:87 — footnote reference
- 8k_2_02:88 — footnote reference
- 8k_2_02:89 — footnote reference
- 8k_2_02:92 — marker
