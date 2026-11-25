<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# LFUS — notes text reader — 10-Q 0001628280-26-050481 (quarter ended June 27, 2026)

## Scope

- Diffed against: 10-Q 0001628280-26-031041 (quarter ended March 28, 2026). 8-K read: 0001628280-26-050382 (Item 2.02, Exhibit 99.1, filed 2026-07-29).
- Files read in full: input_8k.md, input_controls.md, input_mdna.md, input_notes.md (all 972 lines), input_notes_history.md, input_prior_predictions.md.
- Not in my directory, so nothing to report from them: an auditor's report (input_controls.md has only Item 4), an Item 1A diff, an Exhibit 21 diff, any Exhibit 10.
- Forbidden-material check: my directory has no trend table, prices, returns, short interest, other-company files, prior probabilities or outcome window. Exhibit 99.1 includes the company's own condensed statements and non-GAAP tables. They are part of the 8-K body, and I treated them as amounts only.
- Prior flags: none on record.
- No arithmetic was done. Where an item cites an amount, a comparison or a direction, it repeats what the prose says.

## Items

```json
{ "id": "estimates_and_discretion_level_three_impairment_of_semiconductor_site_assets",
  "what_changed": "New this quarter: a $13.1 million non-cash fixed asset impairment tied to the announced closure and/or disposition of two semiconductor manufacturing sites in the Electronics segment. The impaired assets were measured at fair value on a nonrecurring basis using significant unobservable (Level 3) inputs. The prose names no valuation technique or input beyond that.",
  "account": "Net property, plant, and equipment",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "The related assets were measured at fair value on a nonrecurring basis using valuation techniques that incorporated significant unobservable inputs, which are classified within Level 3 of the fair value hierarchy.",
  "paragraph_id": "0001628280-26-050481:notes:150",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_closure_of_two_semiconductor_manufacturing_sites",
  "what_changed": "The restructuring note says the 2026 charges relate to reorganizing manufacturing, selling and administrative functions in two places: the semiconductor business (Electronics) and the commercial vehicle business (Transportation). It adds that two semiconductor manufacturing sites face an announced closure and/or disposition, with a $13.1 million fixed asset impairment in the second quarter. A closure or disposition usually brings further exit costs in later quarters: severance, other restructuring, and possibly a gain or loss on disposal. None of the text paragraphs I received estimates the remaining costs or gives a timetable for the sites.",
  "account": "Restructuring, impairment, and other charges",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "These charges primarily related to the reorganization of certain manufacturing, selling and administrative functions for the semiconductor business within the Electronics segment and the reorganization of certain manufacturing, selling and administrative functions for the commercial vehicle business within the Transportation segment. In addition, during the second quarter of 2026, the Company recognized fixed asset impairment charges of $13.1 million, primarily related to the announced closure and/or disposition of two manufacturing sites for the semiconductor business within the Electronics segment.",
  "paragraph_id": "0001628280-26-050481:notes:85",
  "explanation": false }
```

```json
{ "id": "earnings_quality_semiconductor_impairment_reported_outside_segment_results",
  "what_changed": "The segment footnote puts the second-quarter $13.1 million impairment for the two semiconductor sites, along with $6.9 million of restructuring, in the non-segment 'Other' line. The Electronics segment operating income and margin discussed in MD&A (mdna:51) and the release therefore exclude these charges. The restructuring table (notes:82) still shows an Impairment row by segment.",
  "account": "Electronics segment operating income",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Operating income for the second quarter of 2026 was $6.9 million ($14.3 million year-to-date) of restructuring charges primarily related to employee termination costs. During the second quarter of 2026, the Company recognized fixed asset impairment charges of $13.1 million, primarily related to the announced closure and/or disposition of two manufacturing sites for the semiconductor business within the Electronics segment.",
  "paragraph_id": "0001628280-26-050481:notes:183",
  "explanation": false }
```

```json
{ "id": "controls_audit_and_filings_announced_site_closure_without_exit_cost_or_impairment_filing",
  "what_changed": "The 10-Q calls the closure and/or disposition of the two semiconductor sites 'announced' and records an impairment for it. The 8-K index in my input lists no Item 2.05 (exit or disposal costs) or Item 2.06 (material impairments) on or before 2026-07-29. After the 2026-05-06 earnings release, the index lists only the 2026-05-14 filing (Items 7.01 and 9.01, body not in my input) and the 2026-07-29 release. My input does not say where or when the closure was announced. Whether either item was required depends on materiality and the commitment date, which I do not judge.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "In addition, during the second quarter of 2026, the Company recognized fixed asset impairment charges of $13.1 million, primarily related to the announced closure and/or disposition of two manufacturing sites for the semiconductor business within the Electronics segment.",
  "paragraph_id": "0001628280-26-050481:notes:64",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_basler_measurement_period_adjustments",
  "what_changed": "The Basler note now gives six-month measurement-period adjustments: lower fair values for acquired intangible assets ($5.0 million), current liabilities ($3.2 million), inventories ($2.6 million), trade receivables ($2.1 million), property, plant, and equipment ($1.7 million) and other long-term assets ($1.6 million), and a higher value for other current assets ($1.2 million). The stated result is an $8.6 million increase in goodwill. It also states $0.3 million and $2.8 million of indebtedness paid as purchase consideration in the three and six months. The allocation is still preliminary because the third-party valuation of acquired tangible assets is not finished (notes:35). Goodwill, PP&E and depreciation can therefore still change within the measurement period.",
  "account": "Goodwill",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "During the six months ended June 27, 2026, the Company made adjustments to reduce the fair value of intangible assets of $5.0 million, current liabilities of $3.2 million, inventories of $2.6 million, trade receivables of $2.1 million, property, plant, and equipment of $1.7 million, other long-term assets of $1.6 million, and increase in other current assets of $1.2 million. As a result of these adjustments, goodwill was increased by $8.6 million.",
  "paragraph_id": "0001628280-26-050481:notes:39",
  "explanation": true }
```

```json
{ "id": "structure_and_disclosure_changes_polytronics_equity_investment_sold",
  "what_changed": "New: in the second quarter the Company sold its Level 1 equity investment in Polytronics Technology Corporation for $7.4 million of net proceeds. The proceeds are classified in investing cash flows under net proceeds from sale of property, plant and equipment, and other. MD&A (mdna:112) repeats the proceeds. The prose states no realized gain or loss on the sale.",
  "account": "Investments",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "during the three months ended June 27, 2026, with net proceeds of $7.4 million and is recognized in Net proceeds from sale of property, plant and equipment, and other in investing activities on the Condensed Consolidated Statement of Cash Flows.",
  "paragraph_id": "0001628280-26-050481:notes:122",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_proceeds_from_basler_asset_held_for_sale",
  "what_changed": "New: MD&A states $1.7 million of proceeds in the first six months of 2026 from an asset held for sale that came with the Basler acquisition. The Basler allocation table in my input (notes:37) has no separate held-for-sale line, and no note text in my input describes the asset.",
  "account": "Net proceeds from sale of property, plant and equipment, and other",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "and $1.7 million from an asset held for sale from the Basler acquisition during the six months ended June 27, 2026.",
  "paragraph_id": "0001628280-26-050481:mdna:112",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_uk_pension_buy_in_settlement_charge_timing",
  "what_changed": "The UK group annuity paragraph says the buy-in will cut the pension benefit obligation by about $25 million, about 31% of qualified-plan obligations. It says a one-time non-cash settlement charge of $6 million to $8 million is currently expected in the first quarter of 2027, depending on final data and wind-up expenses. The paragraph is carried as text and has no period-end date that would roll forward. The prior wording is not in my input, so I cannot tell (insufficient) whether the expected quarter, the range or the obligation figures moved.",
  "account": "Other income, net (where the settlement charge is classified is not stated)",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "In connection with this transaction, the Company currently expects to record a one-time non-cash settlement charge in the first quarter of 2027 estimated between $6 million and $8 million, reflecting the accelerated recognition of a portion of unamortized actuarial losses in the plan.",
  "paragraph_id": "0001628280-26-050481:notes:156",
  "explanation": false }
```

```json
{ "id": "earnings_quality_tax_rate_lowered_by_statute_lapses_and_share_award_benefits",
  "what_changed": "MD&A and the tax note give three reasons the 2026 effective tax rate (23.6% for the quarter, 23.0% for six months, as stated) is below 2025. Two are discrete items: lapses in the statute of limitations on previously unrecognized tax benefits, and excess tax benefits from share-based compensation. The third is that 2025 had foreign exchange losses with no tax benefit. Discrete benefits like these do not recur on a schedule. The release guides a third-quarter adjusted rate of about 23% to 24%.",
  "account": "Effective tax rate (income taxes)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "The effective tax rate for 2026 was lower than the effective tax rate for the comparable 2025 periods primarily due to lapses in the statute of limitations for previously unrecognized tax benefits and excess tax benefits for share based compensation recognized in 2026, as well as foreign exchange losses in non-U.S. jurisdictions with no related tax benefit recognized in 2025.",
  "paragraph_id": "0001628280-26-050481:mdna:37",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_non_us_losses_with_no_tax_benefit",
  "what_changed": "The prose says the 2026 rate is above the statutory rate mainly because of losses in non-U.S. jurisdictions with no related tax benefit. These are losses on which no deferred tax benefit is recognized, the valuation-allowance judgment. The discrete benefits only partly offset them. The 2025 wording led with foreign exchange losses. Continued unbenefited foreign losses keep the reported rate up once the discrete benefits fade.",
  "account": "Effective tax rate; deferred tax valuation allowance",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "The effective tax rate for the three and six months ended June 27, 2026 was higher than the statutory tax rate primarily due to losses in non-U.S. jurisdictions with no related tax benefit, partially offset by lapses in the statute of limitations for previously unrecognized tax benefits as well as excess tax benefits for share based compensation.",
  "paragraph_id": "0001628280-26-050481:mdna:38",
  "explanation": false }
```

```json
{ "id": "across_documents_indemnification_receivable_reversal_linked_to_tax_benefit",
  "what_changed": "The release says 2026 other income, net included the reversal of a $2.7 million indemnification receivable. The reversal is tied to the same statute-of-limitations lapses that produced $2.7 million of tax benefits in the first quarter (footnotes d and e), and both are adjusted out of non-GAAP results. The 10-Q tax paragraphs in my input (mdna:37, mdna:38, notes:167, notes:168) cite the statute lapses as lowering the tax rate. None of them mentions the linked receivable reversal in other income, net.",
  "account": "Other income, net",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "2026 included the reversal of an indemnification receivable of $2.7 million related to lapses in the statute of limitations for previously unrecognized tax benefits recognized in the first quarter of 2026.",
  "paragraph_id": "0001628280-26-050382:8k_2_02:90",
  "explanation": true }
```

```json
{ "id": "liquidity_and_capital_stock_award_exercise_proceeds",
  "what_changed": "New in the six-month financing discussion: $75.6 million of net proceeds from stock-based award activities in 2026. The prose sets this against $0.6 million in the 2025 period. Proceeds like these come with share issuance, and the tax note credits excess tax benefits from share-based compensation with lowering the 2026 rate. MD&A says there were no share repurchases in 2026.",
  "account": "Financing cash flow from stock-based award activities; weighted-average shares",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The Company received $75.6 million of net proceeds related to stock-based award activities during the six months ended June 27, 2026 compared to $0.6 million for the six months ended June 28, 2025.",
  "paragraph_id": "0001628280-26-050481:mdna:114",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_quarterly_dividend_raised",
  "what_changed": "New: the quarterly dividend rises to $0.80 per share from $0.75, which the release calls a 7% increase. It was declared July 29, 2026, after quarter end, and is payable September 3, 2026 to holders of record on August 20, 2026. MD&A (mdna:105) repeats it.",
  "account": "Cash dividends paid",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "The company will pay a cash dividend of $0.80 per share on its common stock, a 7% increase from the prior quarter dividend of $0.75 per share.",
  "paragraph_id": "0001628280-26-050382:8k_2_02:33",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_covenant_ebitda_adds_back_restructuring_and_optimization",
  "what_changed": "The release says the first-quarter 2026 amendment now allows restructuring charges and business optimization expenses to be added back in covenant Consolidated EBITDA, which the leverage covenant uses. The 10-Q paragraphs on the amendment in my input (notes:93, mdna:11, mdna:83) list the term-loan payoff, the larger revolver and the maturity extension 'among other changes'. None of them mentions this add-back. Wider add-backs raise covenant EBITDA and lower the covenant leverage ratio for the same reported results, which matters more while restructuring and site closures continue.",
  "account": "Consolidated EBITDA as defined in the Credit Agreement (covenant)",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "The Credit Agreement was amended in Q1 2026 and now allows to add restructuring charges and business optimization expenses in addition to the prior credit agreement.",
  "paragraph_id": "0001628280-26-050382:8k_2_02:84",
  "explanation": false }
```

```json
{ "id": "across_documents_private_placement_note_maturity_range",
  "what_changed": "The release says the Credit Agreement and Private Placement Notes have 'maturities ranging from 2027 to 2031'. The 10-Q debt note (notes:107, notes:91) describes U.S. Senior Notes 'due June 30, 2032'. The two documents give different final years for the maturity range. The supervisor should reconcile which is right.",
  "account": "Long-term debt",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "Our Credit Agreement and Private Placement Note with maturities ranging from 2027 to 2031, contain financial ratio covenants",
  "paragraph_id": "0001628280-26-050382:8k_2_02:83",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_quarter_exceeded_management_expectations",
  "what_changed": "The CEO says second-quarter performance exceeded the company's own expectations and cites broad-based demand strength and execution. The prior quarter's guidance is not in my input, so the text does not show how large the beat was.",
  "account": "Net sales",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "We delivered strong second quarter results, with performance exceeding our expectations",
  "paragraph_id": "0001628280-26-050382:8k_2_02:15",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_record_bookings_and_third_quarter_growth_outlook",
  "what_changed": "New forward statement: management expects about 26% total revenue growth in the third quarter over the prior year. It cites record bookings, customer momentum and the Basler contribution. Record bookings point to orders running ahead of shipments.",
  "account": "Net sales",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "Looking ahead to the third quarter, we expect approximately 26% total revenue growth versus the prior year, supported by record bookings, continued customer momentum, and contributions from the Basler acquisition.",
  "paragraph_id": "0001628280-26-050382:8k_2_02:16",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_third_quarter_guidance_ranges",
  "what_changed": "New third-quarter guidance on a non-GAAP basis: net sales of $780 million to $800 million, adjusted diluted EPS of $4.85 to $5.05, and an adjusted effective tax rate of about 23% to 24%. The 'up' direction comes from the CEO's year-over-year growth statement (8k_2_02:16). Placing the ranges against second-quarter actuals is for the numbers reader.",
  "account": "Net sales; adjusted diluted EPS; adjusted effective tax rate",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "Net sales in the range of $780 - $800 million, adjusted diluted EPS in the range of $4.85 – $5.05 and an adjusted effective tax rate of approximately 23% - 24%",
  "paragraph_id": "0001628280-26-050382:8k_2_02:19",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_electronics_volume_and_favorable_price",
  "what_changed": "MD&A attributes the second-quarter Electronics sales increase to volume: $44.7 million in electronics products and $26.1 million in semiconductor, driven by higher end-market demand and favorable price. The release adds passive products up 26% organic and semiconductor up 15% organic on protection and power semiconductor volumes. Favorable price is named as a driver of both sales and margin (mdna:25, mdna:51).",
  "account": "Net sales (Electronics segment)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The net sales increase was primarily due to higher volume of $44.7 million and $26.1 million in the electronics products and semiconductor businesses, respectively, driven by higher end market demand and favorable price.",
  "paragraph_id": "0001628280-26-050481:mdna:48",
  "explanation": false }
```

```json
{ "id": "earnings_quality_gross_margin_from_volume_price_mix_and_basler",
  "what_changed": "MD&A says second-quarter gross margin improved 3.6%. It credits higher volume, favorable price, operational execution and favorable mix in Electronics and industrial circuit protection, plus Basler's higher gross margin. These are operating drivers. Per notes:40, the Basler inventory step-up was fully amortized by the first quarter of 2026, so it brings no second-quarter charge.",
  "account": "Gross profit",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The increase of $74.0 million in gross profit and the improved gross margin of 3.6% were primarily due to higher volume and favorable price, operational execution, and favorable product mix from the Electronics segment and the industrial circuit protection business within the Industrial segment. Additionally, gross margin was higher due to higher gross margin from the Basler acquisition.",
  "paragraph_id": "0001628280-26-050481:mdna:25",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_higher_annual_incentive_accrual",
  "what_changed": "MD&A attributes $25.1 million of higher second-quarter SG&A to higher annual incentive expenses and $11.7 million of incremental Basler operating expenses. The annual incentive expense is accrued from management's estimate of full-year performance, so later quarters can true it up. The accrued liabilities table has an employee-related liabilities line, but no prose discusses the accrual balance.",
  "account": "Selling, general, and administrative expenses",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "The increase in operating expenses of $47.1 million was primarily due to higher selling, general, and administrative expenses of $25.1 million due to higher annual incentive expenses and incremental operating expenses of $11.7 million from the Basler acquisition",
  "paragraph_id": "0001628280-26-050481:mdna:28",
  "explanation": false }
```

```json
{ "id": "earnings_quality_operating_cash_flow_attributed_to_cash_earnings",
  "what_changed": "MD&A credits the six-month rise in operating cash flow mainly to higher cash earnings. It states $226.5 million against $148.2 million, an increase of $78.2 million. It says nothing about working capital. The release's cash flow statement has separate trade receivables and inventories lines, and reconciling them with this explanation is for the numbers reader. mdna:10 repeats the sentence.",
  "account": "Net cash provided by operating activities",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The increase in net cash provided by operating activities of $78.2 million was primarily due to higher cash earnings.",
  "paragraph_id": "0001628280-26-050481:mdna:110",
  "explanation": false }
```

```json
{ "id": "earnings_quality_pretax_income_helped_by_foreign_exchange_swing",
  "what_changed": "MD&A says that, beyond operating factors, second-quarter pre-tax income was mainly helped by a $0.2 million foreign exchange gain where a year earlier there was a $10.4 million loss. For six months it states a $2.6 million gain against a $15.3 million loss (mdna:35). By the prose's own account, part of the year-over-year pre-tax growth comes from a non-operating line that the company excludes from adjusted results.",
  "account": "Income before income taxes",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "In addition to the factors impacting comparative results for operating income discussed above, income before income taxes was primarily benefited by foreign exchange gains of $0.2 million in the second quarter of 2026 compared to foreign exchange losses of $10.4 million in the second quarter of 2025.",
  "paragraph_id": "0001628280-26-050481:mdna:34",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_commercial_vehicle_cost_inflation_and_mix",
  "what_changed": "MD&A says Transportation's second-quarter operating income and margin fell. It blames lower commercial vehicle gross margin from cost inflation and unfavorable product mix, even though MD&A also cites higher commercial vehicle volume in Asia (mdna:55). The release gives the same reason (lower commercial vehicle profitability, 8k_2_02:28), and the restructuring note names a reorganization of the commercial vehicle business.",
  "account": "Transportation segment operating income",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "The decrease in operating income was primarily due to lower gross margin from the commercial vehicles business impacted by cost inflation and unfavorable product mix.",
  "paragraph_id": "0001628280-26-050481:mdna:58",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_strategic_exit_of_lower_margin_automotive_sensor_products",
  "what_changed": "MD&A names a strategic exit from certain lower-margin automotive sensor products as the cause of lower sensor volume in the quarter and the six months (mdna:56). A deliberate exit implies sensor sales keep falling as those products run off. The release calls this 'auto sensor product declines'.",
  "account": "Net sales (Automotive Sensors, Transportation segment)",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "The remaining net sales increase was due to higher volume in the commercial vehicle business within the Asia region, partially offset by lower volume from the automotive sensors business driven by the strategic exit of certain lower margin products.",
  "paragraph_id": "0001628280-26-050481:mdna:55",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_europe_semiconductor_and_passenger_car_volume",
  "what_changed": "The Europe paragraph says second-quarter Europe sales included $3.5 million of favorable foreign exchange. It says the rest of the increase came mainly from electronics products volume and $2.0 million of Basler sales, partly offset by lower volume in passenger car products and in the semiconductor business. The semiconductor business is the one being reorganized and closing sites. The prose does not say where the two sites are.",
  "account": "Net sales (Europe: semiconductor and passenger car products)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "The remaining increase in net sales was primarily due to higher volume from the electronics products business within the Electronics segment and incremental net sales of $2.0 million from the Basler acquisition within the Industrial segment, partially offset by lower volume from the passenger car products business within the Transportation segment and the semiconductor business within the Electronics segment.",
  "paragraph_id": "0001628280-26-050481:mdna:77",
  "explanation": false }
```

```json
{ "id": "earnings_quality_industrial_margin_diluted_by_basler_amortization",
  "what_changed": "MD&A says the Industrial second-quarter operating margin fell from 19.2% to 18.3% because of $2.9 million of higher amortization from the Basler acquisition, partly offset by better industrial circuit protection gross margin. The release describes Industrial adjusted EBITDA margin, which adds amortization back, as higher (8k_2_02:31). Basler intangible values are still preliminary and were marked down in the measurement period (notes:39), so the amortization run-rate can still change.",
  "account": "Amortization of intangibles (Industrial segment)",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "Operating margins decreased from 19.2% in the second quarter of 2025 to 18.3% in the second quarter of 2026 due to higher amortization expenses of $2.9 million, or 2.0% related to the Basler acquisition noted previously, partially offset by improved gross margin in the industrial circuit protection products.",
  "paragraph_id": "0001628280-26-050481:mdna:65",
  "explanation": false }
```

```json
{ "id": "results_against_expectations_industrial_organic_demand_from_data_center_and_hvac",
  "what_changed": "The release attributes Industrial organic growth of 16% to stronger data center, HVAC, industrial automation and construction demand, with Basler adding 36%. MD&A (mdna:62) attributes the non-Basler increase to industrial circuit protection volume.",
  "account": "Net sales (Industrial segment)",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "Organic sales increased +16% driven by improved data center, HVAC, industrial automation, and construction demand.",
  "paragraph_id": "0001628280-26-050382:8k_2_02:30",
  "explanation": false }
```

```json
{ "id": "narrative_signs_of_operating_pressure_lower_global_passenger_car_builds",
  "what_changed": "The release says passenger vehicle organic sales fell 2%. It blames lower global passenger car builds and auto sensor product declines, which puts an external market factor next to the company's own sensor exit. The 10-Q's second-quarter Transportation paragraph (mdna:55) explains the offset only through the sensor exit. Lower passenger car volume appears in the 10-Q only in the Europe paragraph (mdna:77).",
  "account": "Net sales (Passenger Car Products and Automotive Sensors)",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "Passenger vehicle sales were impacted by lower global passenger car builds and auto sensor product declines.",
  "paragraph_id": "0001628280-26-050382:8k_2_02:27",
  "explanation": false }
```

Item count: 29. Items with `explanation` true: 2 (`estimates_and_discretion_basler_measurement_period_adjustments`, `across_documents_indemnification_receivable_reversal_linked_to_tax_benefit`).

## Paragraphs carried as text that did not become items

### Item 4 (input_controls.md)

- 0001628280-26-050481:item_4_controls:1 — heading
- 0001628280-26-050481:item_4_controls:2 — heading
- 0001628280-26-050481:item_4_controls:3 — definition of disclosure controls; boilerplate, always carried in full
- 0001628280-26-050481:item_4_controls:4 — page number
- 0001628280-26-050481:item_4_controls:5 — controls concluded effective; date rolled forward
- 0001628280-26-050481:item_4_controls:6 — heading
- 0001628280-26-050481:item_4_controls:7 — no internal-control changes in the quarter; date rolled forward

### 8-K (input_8k.md)

- Item-code index and late-filing list (these lines have no paragraph ids) — read. They are used in the site-closure filing item. The NT 10-K for fiscal 2024 (2025-02-27) is history, not new this period.
- 0001628280-26-050382:8k_2_02:1 — filing metadata
- 0001628280-26-050382:8k_2_02:2 — filing metadata
- 0001628280-26-050382:8k_2_02:3 — exhibit label
- 0001628280-26-050382:8k_2_02:4 — press contact block
- 0001628280-26-050382:8k_2_02:5 — release title
- 0001628280-26-050382:8k_2_02:6 — heading
- 0001628280-26-050382:8k_2_02:7 — note on comparison basis
- 0001628280-26-050382:8k_2_02:8 — amounts only (headline net sales and organic growth; drivers are covered by the results items)
- 0001628280-26-050382:8k_2_02:9 — amounts only (quarter operating and free cash flow)
- 0001628280-26-050382:8k_2_02:10 — amounts only (year-to-date cash flow)
- 0001628280-26-050382:8k_2_02:11 — amounts only (GAAP and adjusted EPS)
- 0001628280-26-050382:8k_2_02:12 — amounts only (margins)
- 0001628280-26-050382:8k_2_02:13 — repeats the dividend increase itemized at 8k_2_02:33
- 0001628280-26-050382:8k_2_02:14 — dateline
- 0001628280-26-050382:8k_2_02:17 — heading
- 0001628280-26-050382:8k_2_02:18 — lead-in to the guidance itemized at 8k_2_02:19
- 0001628280-26-050382:8k_2_02:20 — page marker
- 0001628280-26-050382:8k_2_02:21 — non-GAAP guidance disclaimer; boilerplate
- 0001628280-26-050382:8k_2_02:22 — heading
- 0001628280-26-050382:8k_2_02:23 — heading
- 0001628280-26-050382:8k_2_02:24 — Electronics sales drivers; same facts as the Electronics item (mdna:48)
- 0001628280-26-050382:8k_2_02:25 — Electronics adjusted EBITDA margin drivers; same as the Electronics and gross-margin items
- 0001628280-26-050382:8k_2_02:26 — heading
- 0001628280-26-050382:8k_2_02:28 — Transportation margin fall from lower commercial vehicle profitability; same as the commercial vehicle item (mdna:58)
- 0001628280-26-050382:8k_2_02:29 — heading
- 0001628280-26-050382:8k_2_02:31 — Industrial adjusted EBITDA margin; mentioned in the Basler amortization item
- 0001628280-26-050382:8k_2_02:32 — heading
- 0001628280-26-050382:8k_2_02:34 — heading
- 0001628280-26-050382:8k_2_02:35 — conference call logistics
- 0001628280-26-050382:8k_2_02:36 — page marker
- 0001628280-26-050382:8k_2_02:37 — heading
- 0001628280-26-050382:8k_2_02:38 — company description; boilerplate
- 0001628280-26-050382:8k_2_02:39 — insufficient — forward-looking-statement boilerplate; no prior release in my input to compare against
- 0001628280-26-050382:8k_2_02:40 — risk-factor cross-reference; boilerplate
- 0001628280-26-050382:8k_2_02:41 — page marker
- 0001628280-26-050382:8k_2_02:42 — heading
- 0001628280-26-050382:8k_2_02:43 — non-GAAP definitions; boilerplate
- 0001628280-26-050382:8k_2_02:44 — document code
- 0001628280-26-050382:8k_2_02:45 — end marker
- 0001628280-26-050382:8k_2_02:46 — address block
- 0001628280-26-050382:8k_2_02:47 — heading
- 0001628280-26-050382:8k_2_02:48 — heading
- 0001628280-26-050382:8k_2_02:49 — balance sheet; amounts only
- 0001628280-26-050382:8k_2_02:50 — heading
- 0001628280-26-050382:8k_2_02:51 — heading
- 0001628280-26-050382:8k_2_02:52 — heading
- 0001628280-26-050382:8k_2_02:53 — statement of operations; amounts only
- 0001628280-26-050382:8k_2_02:54 — heading
- 0001628280-26-050382:8k_2_02:55 — heading
- 0001628280-26-050382:8k_2_02:56 — heading
- 0001628280-26-050382:8k_2_02:57 — cash flow statement; amounts only
- 0001628280-26-050382:8k_2_02:58 — heading
- 0001628280-26-050382:8k_2_02:59 — heading
- 0001628280-26-050382:8k_2_02:60 — heading
- 0001628280-26-050382:8k_2_02:61 — segment sales and operating income table; amounts only
- 0001628280-26-050382:8k_2_02:62 — footnote defining 'Other'; boilerplate
- 0001628280-26-050382:8k_2_02:63 — legend
- 0001628280-26-050382:8k_2_02:64 — segment margin table; amounts only
- 0001628280-26-050382:8k_2_02:65 — heading
- 0001628280-26-050382:8k_2_02:66 — heading
- 0001628280-26-050382:8k_2_02:67 — units caption
- 0001628280-26-050382:8k_2_02:68 — EPS reconciliation; amounts only
- 0001628280-26-050382:8k_2_02:69 — non-GAAP adjustments table; amounts only
- 0001628280-26-050382:8k_2_02:70 — adjusted EBITDA reconciliation; amounts only
- 0001628280-26-050382:8k_2_02:71 — segment adjusted EBITDA, quarter; amounts only
- 0001628280-26-050382:8k_2_02:72 — segment adjusted EBITDA, year-to-date; amounts only
- 0001628280-26-050382:8k_2_02:73 — net sales reconciliation, quarter; amounts only
- 0001628280-26-050382:8k_2_02:74 — Electronics reconciliation, quarter; amounts only
- 0001628280-26-050382:8k_2_02:75 — Transportation reconciliation, quarter; amounts only
- 0001628280-26-050382:8k_2_02:76 — footnote defining the passenger vehicle business
- 0001628280-26-050382:8k_2_02:77 — net sales reconciliation, year-to-date; amounts only
- 0001628280-26-050382:8k_2_02:78 — Electronics reconciliation, year-to-date; amounts only
- 0001628280-26-050382:8k_2_02:79 — Transportation reconciliation, year-to-date; amounts only
- 0001628280-26-050382:8k_2_02:80 — footnote; same as 8k_2_02:76
- 0001628280-26-050382:8k_2_02:81 — tax and free cash flow reconciliations; amounts only
- 0001628280-26-050382:8k_2_02:82 — covenant debt, Consolidated EBITDA and leverage table; amounts only
- 0001628280-26-050382:8k_2_02:85 — footnote defining Consolidated EBITDA
- 0001628280-26-050382:8k_2_02:86 — rounding note
- 0001628280-26-050382:8k_2_02:87 — footnote mapping to captions
- 0001628280-26-050382:8k_2_02:88 — footnote mapping to captions
- 0001628280-26-050382:8k_2_02:89 — footnote mapping to captions
- 0001628280-26-050382:8k_2_02:91 — tax-effect footnote; the $2.7 million statute-lapse event is covered by the 8k_2_02:90 item
- 0001628280-26-050382:8k_2_02:92 — end marker

### MD&A (input_mdna.md)

- 0001628280-26-050481:mdna:2 — heading
- 0001628280-26-050481:mdna:6 — insufficient — company description; prior wording not in my input; no effect on the numbers
- 0001628280-26-050481:mdna:9 — overview repeating the sales and Electronics operating-income drivers already itemized; amounts
- 0001628280-26-050481:mdna:10 — same sentence as mdna:110, which is itemized
- 0001628280-26-050481:mdna:11 — March 12, 2026 credit agreement amendment, a first-quarter event; note history shows the same terms in notes:93 unchanged
- 0001628280-26-050481:mdna:15 — repeats the restructuring and impairment covered by the notes:85 and notes:183 items, and the first-quarter Basler step-up
- 0001628280-26-050481:mdna:16 — prior-year comparison; date rolled forward
- 0001628280-26-050481:mdna:17 — results table; amounts only
- 0001628280-26-050481:mdna:19 — consolidated version of the Electronics volume-and-price drivers (mdna:48), plus Basler and FX amounts
- 0001628280-26-050481:mdna:20 — six-month version of mdna:19; amounts
- 0001628280-26-050481:mdna:22 — cost-of-sales version of the gross-margin drivers itemized at mdna:25
- 0001628280-26-050481:mdna:23 — six-month cost of sales; mdna:25 drivers plus the first-quarter step-up; amounts
- 0001628280-26-050481:mdna:26 — six-month gross profit; mdna:25 drivers; amounts
- 0001628280-26-050481:mdna:29 — six-month operating expenses; mdna:28 drivers plus an R&D amount; amounts
- 0001628280-26-050481:mdna:31 — second-quarter operating income summary; drivers already itemized (mdna:25, mdna:28)
- 0001628280-26-050481:mdna:32 — six-month operating income summary; same drivers; amounts
- 0001628280-26-050481:mdna:35 — six-month version of the FX item (mdna:34)
- 0001628280-26-050481:mdna:42 — segment sales table; amounts only
- 0001628280-26-050481:mdna:43 — segment operating income table; amounts only
- 0001628280-26-050481:mdna:44 — same text as notes:183, which is itemized
- 0001628280-26-050481:mdna:45 — prior-year footnote; date rolled forward
- 0001628280-26-050481:mdna:49 — six-month Electronics sales; mdna:48 drivers
- 0001628280-26-050481:mdna:51 — Electronics second-quarter operating income and margin; mdna:48 and mdna:25 drivers
- 0001628280-26-050481:mdna:52 — Electronics six-month operating income; same drivers
- 0001628280-26-050481:mdna:56 — six-month Transportation sales; the mdna:55 sensor exit plus first-quarter volume drivers
- 0001628280-26-050481:mdna:59 — six-month Transportation operating income (passenger car volume and content growth); year-to-date repeat of first-quarter drivers
- 0001628280-26-050481:mdna:62 — Industrial second-quarter sales; Basler and FX amounts; circuit protection volume as in 8k_2_02:30
- 0001628280-26-050481:mdna:63 — six-month Industrial sales; repeats the first-quarter offset from industrial control and sensor products
- 0001628280-26-050481:mdna:66 — six-month Industrial operating income; same Basler amortization driver as mdna:65
- 0001628280-26-050481:mdna:69 — regional sales table; amounts only
- 0001628280-26-050481:mdna:71 — Americas second quarter; Basler amount; drivers already itemized
- 0001628280-26-050481:mdna:72 — Americas six months; year-to-date repeat
- 0001628280-26-050481:mdna:74 — Asia-Pacific second quarter; drivers already itemized
- 0001628280-26-050481:mdna:75 — Asia-Pacific six months; year-to-date repeat
- 0001628280-26-050481:mdna:78 — Europe six months; FX and Basler amounts
- 0001628280-26-050481:mdna:81 — cash, and cash held by U.S. subsidiaries; amounts only
- 0001628280-26-050481:mdna:82 — heading
- 0001628280-26-050481:mdna:83 — same as notes:93; unchanged per note history
- 0001628280-26-050481:mdna:84 — date rolled forward (notes:94 in the history)
- 0001628280-26-050481:mdna:85 — same as notes:95; unchanged per note history
- 0001628280-26-050481:mdna:88 — wording only ('on the hedged portion' became 'with the hedge', per the notes:98 history)
- 0001628280-26-050481:mdna:89 — amounts only (letters of credit, available capacity)
- 0001628280-26-050481:mdna:92 — same as notes:104; unchanged per note history
- 0001628280-26-050481:mdna:93 — wording only ('first fiscal quarter' became 'first quarter', per the notes:105 history)
- 0001628280-26-050481:mdna:94 — same as notes:106; unchanged per note history
- 0001628280-26-050481:mdna:95 — same as notes:107; unchanged per note history
- 0001628280-26-050481:mdna:97 — same covenant text as notes:109; no change in substance
- 0001628280-26-050481:mdna:99 — heading
- 0001628280-26-050481:mdna:100 — covenant compliance and expectation; date rolled forward
- 0001628280-26-050481:mdna:102 — Basler acquisition description; consideration amount covered by the measurement-period item
- 0001628280-26-050481:mdna:105 — repeats the dividend increase itemized at 8k_2_02:33; second-quarter dividends paid is an amount
- 0001628280-26-050481:mdna:107 — cash flow table; amounts only
- 0001628280-26-050481:mdna:116 — no repurchases in 2026; date rolled forward (same as notes:174)
- 0001628280-26-050481:mdna:118 — off-balance-sheet statement; date rolled forward (per history)
- 0001628280-26-050481:mdna:121 — no change in critical accounting estimates; date rolled forward

### Notes (input_notes.md)

- 0001628280-26-050481:notes:3 — insufficient — company description; prior wording not in my input; no effect on the numbers
- 0001628280-26-050481:notes:8 — table caption; date rolled forward (per history)
- 0001628280-26-050481:notes:9 — revenue disaggregation table; amounts only (history: six-month columns added)
- 0001628280-26-050481:notes:10 — prior-year disaggregation table; amounts only
- 0001628280-26-050481:notes:23 — caption; date rolled forward (per history)
- 0001628280-26-050481:notes:24 — cash reconciliation; amounts only (per history)
- 0001628280-26-050481:notes:25 — heading
- 0001628280-26-050481:notes:26 — insufficient — adoption of ASU 2025-05 stated as not material; prior wording not in my input; the text does not say whether the credit-loss practical expedient was elected
- 0001628280-26-050481:notes:27 — heading
- 0001628280-26-050481:notes:28 — insufficient — ASU 2025-06 still being evaluated; prior wording not in my input
- 0001628280-26-050481:notes:29 — insufficient — ASU 2024-03, a disclosure-only standard, still being evaluated; prior wording not in my input
- 0001628280-26-050481:notes:30 — insufficient — ASU 2023-06 boilerplate; prior wording not in my input
- 0001628280-26-050481:notes:35 — insufficient — allocation still preliminary pending the third-party valuation of acquired tangible assets; prior wording not in my input, so I cannot tell whether the open items narrowed; folded into the notes:39 item
- 0001628280-26-050481:notes:37 — purchase price allocation table; amounts only
- 0001628280-26-050481:notes:40 — Basler inventory step-up fully amortized by the first quarter of 2026; repeats a first-quarter event
- 0001628280-26-050481:notes:41 — Basler legal fees; amounts; date rolled forward
- 0001628280-26-050481:notes:48 — repeats the 2025 Dortmund step-down
- 0001628280-26-050481:notes:49 — Dortmund fees; date rolled forward
- 0001628280-26-050481:notes:52 — pro forma table; amounts only
- 0001628280-26-050481:notes:54 — pro forma adjustments table; amounts only
- 0001628280-26-050481:notes:55 — pro forma footnote; date rolled forward
- 0001628280-26-050481:notes:56 — pro forma footnote; date rolled forward
- 0001628280-26-050481:notes:57 — pro forma footnote; date rolled forward
- 0001628280-26-050481:notes:59 — caption; date rolled forward
- 0001628280-26-050481:notes:60 — inventory components table; amounts only
- 0001628280-26-050481:notes:62 — caption; date rolled forward
- 0001628280-26-050481:notes:63 — PP&E table; amounts only
- 0001628280-26-050481:notes:66 — caption; date rolled forward
- 0001628280-26-050481:notes:67 — goodwill rollforward; amounts only (adjustment line covered by the notes:39 item)
- 0001628280-26-050481:notes:69 — caption; date rolled forward
- 0001628280-26-050481:notes:70 — intangible assets table; amounts only
- 0001628280-26-050481:notes:74 — amortization expense; amounts only
- 0001628280-26-050481:notes:75 — caption; date rolled forward
- 0001628280-26-050481:notes:76 — amortization schedule; amounts only
- 0001628280-26-050481:notes:78 — caption; date rolled forward
- 0001628280-26-050481:notes:79 — accrued liabilities table; amounts only
- 0001628280-26-050481:notes:81 — heading and caption; date rolled forward
- 0001628280-26-050481:notes:82 — restructuring table; amounts only (impairment row covered by the notes:85 item)
- 0001628280-26-050481:notes:83 — prior-year restructuring table; amounts only
- 0001628280-26-050481:notes:87 — prior-year restructuring narrative; date rolled forward
- 0001628280-26-050481:notes:88 — restructuring reserve amounts; payment-timing sentence repeated
- 0001628280-26-050481:notes:89 — heading
- 0001628280-26-050481:notes:90 — caption; date rolled forward (per history)
- 0001628280-26-050481:notes:91 — debt table; amounts only (per history)
- 0001628280-26-050481:notes:92 — heading
- 0001628280-26-050481:notes:93 — unchanged per note history
- 0001628280-26-050481:notes:94 — date rolled forward (per history)
- 0001628280-26-050481:notes:95 — unchanged per note history
- 0001628280-26-050481:notes:96 — unchanged per note history
- 0001628280-26-050481:notes:97 — text unchanged (the history shows only a paragraph-split artifact); the swap is still described as hedging SOFR loans scheduled to mature June 30, 2027, as in the prior period
- 0001628280-26-050481:notes:98 — wording only (per history)
- 0001628280-26-050481:notes:99 — amounts only (letters of credit, available capacity; per history)
- 0001628280-26-050481:notes:100 — heading
- 0001628280-26-050481:notes:101 — date rolled forward to 'three and six months' (per history)
- 0001628280-26-050481:notes:102 — heading
- 0001628280-26-050481:notes:103 — unchanged per note history
- 0001628280-26-050481:notes:104 — unchanged per note history
- 0001628280-26-050481:notes:105 — wording only (per history)
- 0001628280-26-050481:notes:106 — unchanged per note history
- 0001628280-26-050481:notes:107 — unchanged per note history
- 0001628280-26-050481:notes:108 — unchanged per note history
- 0001628280-26-050481:notes:109 — date rolled forward; paragraph-split artifact (per history)
- 0001628280-26-050481:notes:110 — unchanged per note history
- 0001628280-26-050481:notes:111 — interest paid; amounts only (per history)
- 0001628280-26-050481:notes:124 — hedge accounting policy; date rolled forward
- 0001628280-26-050481:notes:126 — cross-currency swaps entered in February 2026 (a first-quarter event); period amounts and notional only
- 0001628280-26-050481:notes:129 — collar trade table; routine monthly trades added; amounts only
- 0001628280-26-050481:notes:130 — collar period amounts and next-12-month reclassification estimate; amounts only
- 0001628280-26-050481:notes:132 — interest rate swap period amounts and reclassification estimate; amounts only
- 0001628280-26-050481:notes:134 — caption; date rolled forward
- 0001628280-26-050481:notes:135 — derivative fair value table; amounts only
- 0001628280-26-050481:notes:136 — caption; date rolled forward
- 0001628280-26-050481:notes:137 — derivative gains in the income statement; amounts only
- 0001628280-26-050481:notes:138 — caption; date rolled forward
- 0001628280-26-050481:notes:139 — derivative gains in comprehensive income; amounts only
- 0001628280-26-050481:notes:142 — no change in valuation techniques; date rolled forward
- 0001628280-26-050481:notes:143 — caption; date rolled forward
- 0001628280-26-050481:notes:144 — recurring fair value table; amounts only
- 0001628280-26-050481:notes:147 — date rolled forward; the wording still mentions a term loan facility
- 0001628280-26-050481:notes:148 — caption; date rolled forward
- 0001628280-26-050481:notes:149 — senior notes fair value table; amounts only
- 0001628280-26-050481:notes:153 — pension cost caption; date rolled forward
- 0001628280-26-050481:notes:154 — pension cost table; amounts only
- 0001628280-26-050481:notes:157 — post-employment plan expense; amounts only
- 0001628280-26-050481:notes:159 — other comprehensive income table; amounts only
- 0001628280-26-050481:notes:161 — caption; date rolled forward
- 0001628280-26-050481:notes:162 — accumulated other comprehensive income rollforward; amounts only
- 0001628280-26-050481:notes:163 — prior-year rollforward; amounts only
- 0001628280-26-050481:notes:164 — caption; date rolled forward
- 0001628280-26-050481:notes:165 — reclassification table; amounts only
- 0001628280-26-050481:notes:167 — same text as mdna:37, which is itemized
- 0001628280-26-050481:notes:168 — same text as mdna:38, which is itemized
- 0001628280-26-050481:notes:171 — EPS table; amounts only
- 0001628280-26-050481:notes:172 — anti-dilutive share counts; amounts only
- 0001628280-26-050481:notes:173 — heading
- 0001628280-26-050481:notes:174 — no repurchases in 2026; date rolled forward
- 0001628280-26-050481:notes:182 — segment table; amounts only
- 0001628280-26-050481:notes:184 — prior-year segment footnote; date rolled forward
- 0001628280-26-050481:notes:186 — caption; date rolled forward
- 0001628280-26-050481:notes:187 — depreciation and amortization by segment; amounts only
- 0001628280-26-050481:notes:189 — sales by country; amounts only
- 0001628280-26-050481:notes:191 — long-lived assets by country; amounts only
- 0001628280-26-050481:notes:193 — additions to long-lived assets; amounts only
- 0001628280-26-050481:notes:195 — heading
- 0001628280-26-050481:notes:196 — off-balance-sheet statement; date rolled forward (per history)
- 0001628280-26-050481:notes:197 — heading
- 0001628280-26-050481:notes:198 — warranty policy; unchanged per note history
- 0001628280-26-050481:notes:199 — product liability insurance; unchanged per note history
- 0001628280-26-050481:notes:200 — customer fuse recall; unchanged per note history; loss still reasonably possible, no accrual, range cannot be determined
- 0001628280-26-050481:notes:201 — heading
- 0001628280-26-050481:notes:202 — environmental; unchanged per note history
- 0001628280-26-050481:notes:203 — heading
- 0001628280-26-050481:notes:204 — ordinary-course litigation; unchanged per note history
- 0001628280-26-050481:notes:205 — ASC 450 policy; unchanged per note history
- 0001628280-26-050481:notes:206 — heading
- 0001628280-26-050481:notes:207 — no material pending litigation; date rolled forward (per history)
- 0001628280-26-050481:notes:208 — heading
- 0001628280-26-050481:notes:209 — related-party introduction; unchanged (the history lists only the table)
- 0001628280-26-050481:notes:210 — Powersem ownership; unchanged
- 0001628280-26-050481:notes:211 — EB Tech ownership; unchanged
- 0001628280-26-050481:notes:212 — ATEC ownership; unchanged
- 0001628280-26-050481:notes:213 — related-party table; amounts only (per history)

### Note change history (input_notes_history.md)

Every history entry points to a notes paragraph that is either itemized above or listed above. I used the history to tell what was new and did not report it as a separate list.

## Counts

- Items: 29
- Items with explanation true: 2
- Lines marked insufficient in the list above: 8 (mdna:6, notes:3, notes:26, notes:28, notes:29, notes:30, notes:35, 8k_2_02:39). The pension item (notes:156) also records that its prior wording is insufficient to say what moved.
