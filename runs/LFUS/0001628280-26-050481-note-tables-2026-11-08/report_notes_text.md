<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# Notes text reader: Littelfuse quarterly report for the second quarter of fiscal 2026 (quarter ended June 27, 2026)

## Input check

The directory holds the six permitted inputs: current report bodies, controls, MD&A, notes after the diff layer, note change history, and prior flags. It contains no trend table, prices, abnormal returns, short interest, other companies' files, prior-run probabilities or outcome window. The earnings release exhibit includes the company's own condensed statements and reconciliation tables. I quote them where needed and do no arithmetic on them.

Prior flags: none on record for this company.

Not in my input: an auditor's report, a risk factor diff, a subsidiary list diff and any material contract exhibit (see Insufficient below).

Totals: 36 items. One of them is marked insufficient. Four carry the management-explanation flag.

## Items

```json
{
  "id": "estimates_and_discretion_fixed_asset_impairment_on_semiconductor_site_closures",
  "what_changed": "The property, plant and equipment note adds a sentence, new this quarter: in the second quarter of 2026 the company recognized fixed asset impairment charges of $13.1 million, primarily related to the announced closure and/or disposition of two manufacturing sites for the semiconductor business in the Electronics segment. The same sentence appears again in the restructuring, fair value and segment notes and in the MD&A. The prose does not name the sites or say when the closures will be complete.",
  "account": "Net property, plant, and equipment",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "during the second quarter of 2026, the Company recognized fixed asset impairment charges of $13.1 million, primarily related to the announced closure and/or disposition of two manufacturing sites for the semiconductor business within the Electronics segment",
  "paragraph_id": "0001628280-26-050481:notes:64",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "estimates_and_discretion_site_impairment_measured_with_level_three_inputs",
  "what_changed": "The fair value note adds an Impairments paragraph. It says the assets impaired for the two semiconductor sites were measured at fair value on a nonrecurring basis, using valuation techniques with significant unobservable inputs, classified in Level 3. The note names neither the technique nor the inputs, so the size of the charge rests on a judgement the text does not describe.",
  "account": "Restructuring, impairment, and other charges",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "The related assets were measured at fair value on a nonrecurring basis using valuation techniques that incorporated significant unobservable inputs, which are classified within Level 3 of the fair value hierarchy.",
  "paragraph_id": "0001628280-26-050481:notes:150",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "narrative_signs_of_operating_pressure_semiconductor_and_commercial_vehicle_reorganization",
  "what_changed": "The restructuring note now gives restructuring charges of $6.9 million for the quarter and $14.3 million for six months, mainly employee terminations. It ties them to reorganizing manufacturing, selling and administrative functions in the semiconductor business (Electronics) and the commercial vehicle business (Transportation). It also adds the impairment for the announced closure and/or disposition of two semiconductor sites. The text gives no estimate of remaining costs. The prose implies further exit charges as the announced closures go ahead. The first-quarter wording of the reorganization sentence is not in my input.",
  "account": "Restructuring, impairment, and other charges",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "These charges primarily related to the reorganization of certain manufacturing, selling and administrative functions for the semiconductor business within the Electronics segment and the reorganization of certain manufacturing, selling and administrative functions for the commercial vehicle business within the Transportation segment.",
  "paragraph_id": "0001628280-26-050481:notes:85",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "across_documents_announced_site_closures_absent_from_release_and_current_reports",
  "what_changed": "The segment note footnote, repeated in the MD&A, calls the closure and/or disposition of two semiconductor manufacturing sites 'announced'. Nothing in my inputs shows that announcement. The earnings release prose does not mention the sites, and its footnote to the Other line says only that Other 'typically includes' restructuring and impairment charges. The index of current reports filed on or before July 29, 2026 shows no item for exit or disposal costs and none for a material impairment. Where and when the closure was announced is for the supervisors to settle.",
  "account": "Restructuring, impairment, and other charges",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "During the second quarter of 2026, the Company recognized fixed asset impairment charges of $13.1 million, primarily related to the announced closure and/or disposition of two manufacturing sites for the semiconductor business within the Electronics segment.",
  "paragraph_id": "0001628280-26-050481:notes:183",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "estimates_and_discretion_basler_purchase_price_allocation_still_preliminary",
  "what_changed": "The Basler acquisition note is carried as changed. It still calls the allocation of the $353.1 million consideration preliminary and names the third-party valuation of acquired tangible assets as the part not yet finalized. The preliminary measurements stay subject to change during the measurement period, and the MD&A says the consideration is subject to a working capital adjustment. The first-quarter wording is not in my input, so I cannot tell whether other open elements were dropped.",
  "account": "Goodwill",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "The purchase price allocation is preliminary because the determination of the fair value of the net assets acquired, including the third-party valuation of acquired tangible assets, is not yet finalized.",
  "paragraph_id": "0001628280-26-050481:notes:35",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "estimates_and_discretion_basler_measurement_period_adjustments_raise_goodwill",
  "what_changed": "The note now says measurement-period adjustments made during the six months increased Basler goodwill by $8.6 million, and the goodwill rollforward carries an adjustment line in the Industrial column. It also says $0.3 million and $2.8 million of Basler indebtedness were paid as part of the purchase consideration in the three and six months.",
  "account": "Goodwill",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "As a result of these adjustments, goodwill was increased by $8.6 million.",
  "paragraph_id": "0001628280-26-050481:notes:39",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "estimates_and_discretion_basler_acquired_receivables_and_inventories_written_down",
  "what_changed": "The same note says the six-month measurement-period adjustments reduced the fair values given to Basler's inventories by $2.6 million and its trade receivables by $2.1 million. They also reduced intangible assets ($5.0 million), current liabilities ($3.2 million), property, plant and equipment ($1.7 million) and other long-term assets ($1.6 million), and increased other current assets ($1.2 million). Management gives the valuation adjustments as the cause of the lower acquired receivable and inventory values. It does not say what it learned about those balances.",
  "account": "Trade receivables, net and Inventories acquired with Basler",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "During the six months ended June 27, 2026, the Company made adjustments to reduce the fair value of intangible assets of $5.0 million, current liabilities of $3.2 million, inventories of $2.6 million, trade receivables of $2.1 million",
  "paragraph_id": "0001628280-26-050481:notes:39",
  "explanation": true,
  "insufficient": false
}
```

```json
{
  "id": "earnings_quality_basler_inventory_step_up_fully_amortized",
  "what_changed": "The note says the $6.4 million Basler inventory step-up was fully amortized to cost of goods sold over the fourth quarter of 2025 and the first quarter of 2026 as the acquired inventory was sold, with $5.4 million of it in the first quarter of 2026, shown as other non-segment costs. No step-up charge is described for the second quarter. The six-month MD&A paragraphs now cite the $5.4 million as a partial offset to the margin improvement.",
  "account": "Cost of sales (purchase accounting inventory adjustment)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "The step-up was fully amortized as a non-cash charge to cost of goods sold during the fourth quarter of 2025 and first quarter of 2026 as the acquired inventory was sold and reflected as other non-segment costs",
  "paragraph_id": "0001628280-26-050481:notes:40",
  "explanation": true,
  "insufficient": false
}
```

```json
{
  "id": "estimates_and_discretion_credit_loss_practical_expedient_adoption",
  "what_changed": "Insufficient. The recently adopted standards paragraph is carried as changed. It says ASU No. 2025-05 was adopted without material impact; that standard lets an entity assume balance-sheet-date conditions persist when estimating expected credit losses on current receivables. The text does not say whether the company elected the practical expedient, and the first-quarter wording is not in my input. So I cannot tell whether anything in the method for the receivables allowance changed this quarter.",
  "account": "Allowance against trade receivables",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "The adoption of ASU 2025-05 did not have a material impact on the Company's Condensed Consolidated Financial Statements.",
  "paragraph_id": "0001628280-26-050481:notes:26",
  "explanation": false,
  "insufficient": true
}
```

```json
{
  "id": "estimates_and_discretion_united_kingdom_pension_settlement_charge_timing",
  "what_changed": "The United Kingdom pension paragraph is carried as changed. It now says the company expects to record a one-time non-cash settlement charge in the first quarter of 2027, estimated at $6 million to $8 million. The charge comes from the group annuity contract, which will reduce the pension benefit obligation by about $25 million. The first-quarter wording is not in my input, so I cannot tell whether the timing, the range or only the wording changed.",
  "account": "Pension settlement charge (non-cash)",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "In connection with this transaction, the Company currently expects to record a one-time non-cash settlement charge in the first quarter of 2027 estimated between $6 million and $8 million, reflecting the accelerated recognition of a portion of unamortized actuarial losses in the plan.",
  "paragraph_id": "0001628280-26-050481:notes:156",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "estimates_and_discretion_higher_annual_incentive_expense",
  "what_changed": "MD&A attributes the second-quarter increase in operating expenses mainly to higher selling, general and administrative expenses from higher annual incentive expenses, plus $11.7 million of Basler operating expenses. The six-month paragraph cites the same incentive driver. Annual incentive expense is an accrual that rests on management's estimate of full-year performance.",
  "account": "Selling, general, and administrative expenses",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The increase in operating expenses of $47.1 million was primarily due to higher selling, general, and administrative expenses of $25.1 million due to higher annual incentive expenses and incremental operating expenses of $11.7 million from the Basler acquisition",
  "paragraph_id": "0001628280-26-050481:mdna:28",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "liquidity_and_capital_effective_interest_rate_now_stated_with_the_hedge",
  "what_changed": "The first-quarter sentence gave the effective rate as 3.88% 'on the hedged portion'. It now gives the effective interest rate on the outstanding borrowings under the Credit Facility as 3.88% 'with the hedge', so the wording of what the rate covers has changed. The swap paragraph is unchanged and still describes the hedged loans as SOFR based loans scheduled to mature on June 30, 2027. The restated Credit Agreement, by contrast, eliminated the term loan and set the Maturity Date at March 12, 2031.",
  "account": "Interest expense",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "As of June 27, 2026, the effective interest rate on the outstanding borrowings under the Credit Facility was 3.88% with the hedge.",
  "paragraph_id": "0001628280-26-050481:notes:98",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "articulation_and_the_filed_history_debt_issuance_costs_dated_to_three_and_six_months",
  "what_changed": "The first-quarter note said the $2.2 million of debt issuance costs were incurred during the three months ended March 28, 2026. The sentence now says they were incurred 'during the three and six months ended June 27, 2026'. Read literally, that also places the costs in the second quarter, although the agreement was completed on March 12, 2026. Whether any issuance cost arose in the second quarter is for the numbers reader.",
  "account": "Unamortized debt issuance costs",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "During the three and six months ended June 27, 2026, the Company incurred debt issuance costs of $2.2 million in connection with the newly amended and restated Credit Agreement completed on March 12, 2026",
  "paragraph_id": "0001628280-26-050481:notes:101",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "across_documents_covenant_ebitda_now_adds_back_restructuring_charges",
  "what_changed": "The release says the Credit Agreement, amended in the first quarter of 2026, now lets the company add restructuring charges and business optimization expenses back into its covenant EBITDA. The quarterly report describes the March 12, 2026 amendment by the term loan payoff, the larger revolving facility and the later maturity, 'among other changes', and does not mention the add-back. This quarter had restructuring charges and site impairments, so the definition change bears on the covenant computation.",
  "account": "Consolidated EBITDA as defined in the Credit Agreement (covenant measure)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The Credit Agreement was amended in Q1 2026 and now allows to add restructuring charges and business optimization expenses in addition to the prior credit agreement.",
  "paragraph_id": "0001628280-26-050382:8k_2_02:84",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "earnings_quality_tax_rate_lowered_by_statute_lapses_and_share_compensation",
  "what_changed": "The income tax note now gives effective rates of 23.6% and 23.0% for the three and six months, against 26.7% and 27.0% a year earlier. It says the 2026 rates are lower mainly for two reasons: previously unrecognized tax benefits were released when statutes of limitation lapsed, and there were excess tax benefits on share-based compensation. The 2025 rates carried foreign exchange losses with no tax benefit. The release treats the statute-lapse benefit as a non-GAAP adjustment.",
  "account": "Income taxes (effective tax rate)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "The effective tax rate for 2026 was lower than the effective tax rate for the comparable 2025 periods primarily due to lapses in the statute of limitations for previously unrecognized tax benefits and excess tax benefits for share based compensation recognized in 2026",
  "paragraph_id": "0001628280-26-050481:notes:167",
  "explanation": true,
  "insufficient": false
}
```

```json
{
  "id": "across_documents_statute_lapse_benefit_dated_to_first_quarter_in_release",
  "what_changed": "The note cites statute-of-limitation lapses as an offset for both the three-month and the six-month rate. The release dates the $2.7 million statute-lapse tax benefit, and the related reversal of a $2.7 million indemnification receivable, to the first quarter of 2026. Its second-quarter non-GAAP column shows no other income adjustment. Neither document says whether a further lapse occurred in the second quarter.",
  "account": "Income taxes",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "The effective tax rate for three and six months ended June 27, 2026 was higher than the statutory tax rate primarily due to losses in non-U.S. jurisdictions with no related tax benefit, partially offset by lapses in the statute of limitations for previously unrecognized tax benefits as well as excess tax benefits for share based compensation.",
  "paragraph_id": "0001628280-26-050481:notes:168",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "earnings_quality_statute_lapse_benefit_paired_with_indemnification_receivable_reversal",
  "what_changed": "The release says the statute-lapse tax benefit was accompanied by the reversal of a $2.7 million indemnification receivable through other income, net. That reversal is a charge below operating income, tied to the same lapses. The release removes both from adjusted results. No carried paragraph of the quarterly report mentions the indemnification receivable.",
  "account": "Other income, net",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "2026 included the reversal of an indemnification receivable of $2.7 million related to lapses in the statute of limitations for previously unrecognized tax benefits recognized in the first quarter of 2026.",
  "paragraph_id": "0001628280-26-050382:8k_2_02:90",
  "explanation": true,
  "insufficient": false
}
```

```json
{
  "id": "earnings_quality_foreign_exchange_gain_against_prior_year_loss",
  "what_changed": "MD&A says second-quarter income before income taxes was helped mainly by foreign exchange gains of $0.2 million, against foreign exchange losses of $10.4 million in the second quarter of 2025. The six-month paragraph says the same for the half year. The benefit is non-operating, and the release's non-GAAP table removes non-operating foreign exchange.",
  "account": "Income before income taxes",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "income before income taxes was primarily benefited by foreign exchange gains of $0.2 million in the second quarter of 2026 compared to foreign exchange losses of $10.4 million in the second quarter of 2025",
  "paragraph_id": "0001628280-26-050481:mdna:34",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "earnings_quality_gross_margin_gain_from_volume_price_mix_and_basler",
  "what_changed": "MD&A attributes the second-quarter rise in gross profit and gross margin mainly to higher volume, favorable price, operational execution and favorable product mix in Electronics and in industrial circuit protection. It adds the higher gross margin of the Basler business.",
  "account": "Gross profit",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The increase of $74.0 million in gross profit and the improved gross margin of 3.6% were primarily due to higher volume and favorable price, operational execution, and favorable product mix from the Electronics segment and the industrial circuit protection business within the Industrial segment.",
  "paragraph_id": "0001628280-26-050481:mdna:25",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "results_against_expectations_sales_growth_from_basler_volume_and_price",
  "what_changed": "MD&A says second-quarter net sales rose with $35.8 million from Basler and $4.1 million of favorable foreign exchange. It says the rest came mainly from higher volume of $44.7 million in electronics products and $26.1 million in semiconductor, driven by higher end market demand and favorable price, plus higher industrial circuit protection volume.",
  "account": "Net sales",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The remaining increase in net sales was primarily due to higher volume of $44.7 million and $26.1 million in the electronics products and semiconductor businesses within the Electronics segment, respectively, driven by higher end market demand and favorable price, and higher volume from the industrial circuit protection products within the Industrial segment.",
  "paragraph_id": "0001628280-26-050481:mdna:19",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "results_against_expectations_electronics_margin_from_leverage_execution_price_and_mix",
  "what_changed": "MD&A says Electronics segment operating margin rose from 14.9% to 21.4%, mainly from volume leverage, operational execution and favorable price and product mix in both the electronics products and semiconductor businesses. The semiconductor business took the site impairments in the same quarter. The restructuring table shows an Electronics impairment amount, and the segment note puts restructuring and impairment in Other rather than in segment operating income.",
  "account": "Electronics segment operating income",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Operating margins increased from 14.9% in the second quarter of 2025 to 21.4% in the second quarter of 2026 primarily due to volume leverage, operational execution and favorable price and product mix from the electronics products and the semiconductor businesses.",
  "paragraph_id": "0001628280-26-050481:mdna:51",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "narrative_signs_of_operating_pressure_commercial_vehicle_cost_inflation_and_mix",
  "what_changed": "MD&A says Transportation operating income fell in the second quarter mainly because of lower gross margin in the commercial vehicle business, hit by cost inflation and unfavorable product mix. It says segment margin fell from 15.6% to 14.1% for the same reason. The release says lower commercial vehicle profitability more than offset passenger vehicle margin expansion. The restructuring note names a reorganization of the commercial vehicle business.",
  "account": "Transportation segment operating income",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "The decrease in operating income was primarily due to lower gross margin from the commercial vehicles business impacted by cost inflation and unfavorable product mix.",
  "paragraph_id": "0001628280-26-050481:mdna:58",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "narrative_signs_of_operating_pressure_automotive_sensors_exit_of_lower_margin_products",
  "what_changed": "MD&A says Transportation sales growth was partly offset by lower automotive sensors volume, driven by the strategic exit of certain lower margin products. The six-month paragraph repeats this. The exit is presented as a continuing choice, so the prose implies lower automotive sensor sales while it runs.",
  "account": "Net sales of Automotive Sensors",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "partially offset by lower volume from the automotive sensors business driven by the strategic exit of certain lower margin products",
  "paragraph_id": "0001628280-26-050481:mdna:55",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "across_documents_passenger_vehicle_decline_cause_differs_between_release_and_report",
  "what_changed": "The release says passenger vehicle sales were hurt by lower global passenger car builds and auto sensor product declines. The quarterly report attributes the automotive sensors decline to a strategic exit of lower margin products and mentions lower passenger car volume only for Europe. One document points to market weakness and the other to a chosen exit. The supervisors can settle which drove the decline.",
  "account": "Net sales of Passenger Car Products and Automotive Sensors",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "Passenger vehicle sales were impacted by lower global passenger car builds and auto sensor product declines.",
  "paragraph_id": "0001628280-26-050382:8k_2_02:27",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "narrative_signs_of_operating_pressure_europe_semiconductor_and_passenger_car_volume",
  "what_changed": "MD&A says Europe sales growth in the second quarter was partly offset by lower volume in the passenger car products business and the semiconductor business. The six-month Europe paragraph does not include that offset, so the weakness is stated for the second quarter.",
  "account": "Europe net sales of passenger car products and semiconductor businesses",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "partially offset by lower volume from the passenger car products business within the Transportation segment and the semiconductor business within the Electronics segment",
  "paragraph_id": "0001628280-26-050481:mdna:77",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "earnings_quality_industrial_margin_diluted_by_basler_amortization",
  "what_changed": "MD&A says Industrial operating margin fell from 19.2% to 18.3% in the second quarter because of $2.9 million of higher amortization related to the Basler acquisition, partly offset by better industrial circuit protection gross margin. The release describes the Industrial adjusted EBITDA margin, which adds amortization back, as higher.",
  "account": "Industrial segment operating income",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "Operating margins decreased from 19.2% in the second quarter of 2025 to 18.3% in the second quarter of 2026 due to higher amortization expenses of $2.9 million, or 2.0% related to the Basler acquisition noted previously, partially offset by improved gross margin in the industrial circuit protection products.",
  "paragraph_id": "0001628280-26-050481:mdna:65",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "liquidity_and_capital_operating_cash_flow_attributed_to_higher_cash_earnings",
  "what_changed": "MD&A attributes the six-month increase in operating cash flow of $78.2 million primarily to higher cash earnings; the same sentence opens the overview. The carried text names no working-capital driver, while the release's cash flow statement carries separate lines for trade receivables, inventories and accounts payable. The paragraph that follows is unchanged from the first quarter and is not in my input.",
  "account": "Net cash provided by operating activities",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The increase in net cash provided by operating activities of $78.2 million was primarily due to higher cash earnings.",
  "paragraph_id": "0001628280-26-050481:mdna:110",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "liquidity_and_capital_stock_award_proceeds_in_financing",
  "what_changed": "The financing discussion now states $75.6 million of net proceeds from stock-based award activities in the six months, against $0.6 million a year earlier. This is the cash side of the excess tax benefits on share-based compensation cited in the tax note, and it bears on shares outstanding.",
  "account": "All other cash provided by financing activities (stock-based award proceeds)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The Company received $75.6 million of net proceeds related to stock-based award activities during the six months ended June 27, 2026 compared to $0.6 million for the six months ended June 28, 2025.",
  "paragraph_id": "0001628280-26-050481:mdna:114",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "liquidity_and_capital_quarterly_dividend_raised_after_quarter_end",
  "what_changed": "MD&A says the company paid $19.0 million of dividends in the second quarter. On July 29, 2026, after quarter end, it declared a quarterly dividend of $0.80 per share, payable September 3, 2026. MD&A calls this a 7% increase 'from the first quarter'; the release calls it an increase 'from the prior quarter dividend of $0.75 per share'.",
  "account": "Cash dividends paid",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "On July 29, 2026, the Company announced the declaration of a quarterly cash dividend of $0.80 per share, a 7% increase from the first quarter, payable on September 3, 2026 to stockholders of record as of August 20, 2026.",
  "paragraph_id": "0001628280-26-050481:mdna:105",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "liquidity_and_capital_basler_asset_held_for_sale_sold",
  "what_changed": "The investing discussion adds $1.7 million of proceeds from an asset held for sale that came with the Basler acquisition, next to $7.4 million from the Polytronics sale. The Basler allocation table does not list an asset held for sale as its own line.",
  "account": "Net proceeds from sale of property, plant and equipment, and other",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "$1.7 million from an asset held for sale from the Basler acquisition during the six months ended June 27, 2026",
  "paragraph_id": "0001628280-26-050481:mdna:112",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "structure_and_disclosure_changes_polytronics_equity_investment_sold",
  "what_changed": "The fair value note now says the Polytronics investment, a listed equity security carried at Level 1, was sold during the second quarter for net proceeds of $7.4 million. The proceeds are presented in the cash flow line for proceeds from sale of property, plant and equipment, and other. No realized gain or loss is stated.",
  "account": "Investments",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "The Company sold its investment in Polytronics Technology Corporation Ltd.",
  "paragraph_id": "0001628280-26-050481:notes:122",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "results_against_expectations_second_quarter_exceeded_company_expectations",
  "what_changed": "The chief executive says second-quarter performance exceeded the company's expectations, citing broad-based demand strength and disciplined execution. The guidance given for the quarter is not in my input.",
  "account": "Net sales",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "We delivered strong second quarter results, with performance exceeding our expectations reflecting broad-based demand strength and disciplined execution across the portfolio",
  "paragraph_id": "0001628280-26-050382:8k_2_02:15",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "results_against_expectations_record_bookings_support_third_quarter_outlook",
  "what_changed": "The release guides third-quarter total revenue growth of about 26% against the prior year. It cites record bookings, continued customer momentum and contributions from Basler.",
  "account": "Net sales",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "we expect approximately 26% total revenue growth versus the prior year, supported by record bookings, continued customer momentum, and contributions from the Basler acquisition",
  "paragraph_id": "0001628280-26-050382:8k_2_02:16",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "results_against_expectations_third_quarter_guidance_ranges",
  "what_changed": "The release gives third-quarter guidance: net sales of $780 to $800 million, adjusted diluted EPS of $4.85 to $5.05 and an adjusted effective tax rate of about 23% to 24%. The guidance is non-GAAP and excludes restructuring, impairment, acquisition and similar items, which the company says it cannot forecast.",
  "account": "Net sales; adjusted diluted earnings per share",
  "expected_direction": "up",
  "horizon": "next quarter",
  "quote": "Net sales in the range of $780",
  "paragraph_id": "0001628280-26-050382:8k_2_02:19",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "results_against_expectations_industrial_organic_growth_from_data_center_and_hvac",
  "what_changed": "The release says Industrial organic sales growth came from improved data center, HVAC, industrial automation and construction demand, with Basler adding to reported growth. The quarterly report text names higher industrial circuit protection volume.",
  "account": "Industrial segment net sales",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Organic sales increased +16% driven by improved data center, HVAC, industrial automation, and construction demand.",
  "paragraph_id": "0001628280-26-050382:8k_2_02:30",
  "explanation": false,
  "insufficient": false
}
```

```json
{
  "id": "results_against_expectations_electronics_passive_products_lead_organic_growth",
  "what_changed": "The release attributes Electronics organic growth to passive products, with semiconductor products also contributing through higher protection and power semiconductor volumes. In the same quarter, the quarterly report records the announced closure and/or disposition of two semiconductor manufacturing sites.",
  "account": "Electronics segment net sales",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Organic sales increased +20% driven by improved passive products (+26% organic) sales.",
  "paragraph_id": "0001628280-26-050382:8k_2_02:24",
  "explanation": false,
  "insufficient": false
}
```

## Insufficient

Five insufficient answers in total: one is an item above and four are listed here.

- The credit-loss standard adoption: the item `estimates_and_discretion_credit_loss_practical_expedient_adoption` above.
- Auditor's report: none is in my input. The controls file carries only the controls and procedures item, which is normal for a quarterly report, so there is nothing to read.
- Risk factor diff, subsidiary list diff and material contract exhibits: none is in my directory. The restated Credit Agreement (the current report of March 13, 2026) cannot be read, so I cannot check the release's covenant add-back against the agreement itself.
- Current report of May 14, 2026 (Regulation FD disclosure with exhibits): it is listed in the item index, but its body is not in my input.

Note on the carried paragraphs: prior-quarter wording is supplied only for the note sections covered by the note change history. For the other carried paragraphs (the Basler allocation, the United Kingdom pension, the restructuring narrative and the MD&A), I can see that the paragraph changed but not always what changed. The items above say so where it matters.

## Paragraphs not made into items

### MD&A

- 0001628280-26-050481:mdna:2 — heading only
- 0001628280-26-050481:mdna:6 — company description; prior wording not in my input; no accounting substance
- 0001628280-26-050481:mdna:9 — overview repeating the sales and Electronics income drivers already in the sales-growth and Electronics-margin items
- 0001628280-26-050481:mdna:10 — same sentence as the operating-cash-flow item
- 0001628280-26-050481:mdna:11 — restates the March 12, 2026 credit agreement amendment already reported in the first quarter; wording only
- 0001628280-26-050481:mdna:15 — repeats the segment footnote on restructuring, impairment, deal fees and step-up; covered by the site-closure and step-up items
- 0001628280-26-050481:mdna:16 — prior-year comparison; date rolled forward
- 0001628280-26-050481:mdna:17 — results table; amounts only
- 0001628280-26-050481:mdna:20 — six-month version of the sales-growth item; same drivers, amounts only
- 0001628280-26-050481:mdna:22 — cost of sales version of the gross-margin item; same drivers, amounts only
- 0001628280-26-050481:mdna:23 — six-month cost of sales; same drivers plus the step-up charge covered by the step-up item
- 0001628280-26-050481:mdna:26 — six-month gross profit; same drivers plus the step-up charge covered by the step-up item
- 0001628280-26-050481:mdna:29 — six-month version of the incentive-expense item; adds a research and development amount; amounts only
- 0001628280-26-050481:mdna:31 — operating income; repeats the gross profit and operating expense drivers already itemized
- 0001628280-26-050481:mdna:32 — six-month operating income; drivers carried over from the first quarter
- 0001628280-26-050481:mdna:35 — six-month version of the foreign-exchange item; amounts only
- 0001628280-26-050481:mdna:37 — same text as the tax-rate item in the income tax note
- 0001628280-26-050481:mdna:38 — same text as the statute-lapse across-documents item
- 0001628280-26-050481:mdna:42 — segment sales table; amounts only
- 0001628280-26-050481:mdna:43 — segment operating income table; amounts only
- 0001628280-26-050481:mdna:44 — same text as the segment footnote used in the site-closure across-documents item
- 0001628280-26-050481:mdna:45 — prior-year footnote; date rolled forward
- 0001628280-26-050481:mdna:48 — Electronics restatement of the sales-growth drivers; amounts only
- 0001628280-26-050481:mdna:49 — six-month Electronics sales; same drivers, amounts only
- 0001628280-26-050481:mdna:52 — six-month Electronics operating income; same drivers, amounts only
- 0001628280-26-050481:mdna:56 — six-month Transportation sales; same sensor-exit driver, plus passenger car volume carried over from the first quarter
- 0001628280-26-050481:mdna:59 — six-month Transportation operating income; vehicle-content driver carried over from the first quarter; amounts only
- 0001628280-26-050481:mdna:62 — Industrial quarter sales; Basler and circuit-protection drivers already in the sales-growth item; amounts only
- 0001628280-26-050481:mdna:63 — six-month Industrial sales; industrial control and sensor volume carried over from the first quarter
- 0001628280-26-050481:mdna:66 — six-month Industrial operating income; same amortization driver as the Industrial-margin item; amounts only
- 0001628280-26-050481:mdna:69 — geographic sales table; amounts only
- 0001628280-26-050481:mdna:71 — Americas quarter; Basler and volume drivers already itemized; amounts only
- 0001628280-26-050481:mdna:72 — six-month Americas; drivers carried over from the first quarter; amounts only
- 0001628280-26-050481:mdna:74 — Asia-Pacific quarter; volume drivers already itemized; amounts only
- 0001628280-26-050481:mdna:75 — six-month Asia-Pacific; amounts only
- 0001628280-26-050481:mdna:78 — six-month Europe; amounts only
- 0001628280-26-050481:mdna:81 — cash balance and the portion held in the United States; amounts only, date rolled forward
- 0001628280-26-050481:mdna:82 — heading only
- 0001628280-26-050481:mdna:83 — same as the debt note's amendment paragraph; first-quarter event, unchanged per note change history
- 0001628280-26-050481:mdna:84 — same as the debt note's revolver balance paragraph; date rolled forward
- 0001628280-26-050481:mdna:85 — same as the debt note's pricing paragraph; unchanged per note change history
- 0001628280-26-050481:mdna:88 — same sentence as the effective-interest-rate item
- 0001628280-26-050481:mdna:89 — letters of credit and capacity; amounts only, date rolled forward
- 0001628280-26-050481:mdna:92 — senior notes history; unchanged per note change history
- 0001628280-26-050481:mdna:93 — senior notes history; wording only
- 0001628280-26-050481:mdna:94 — note purchase agreement amendment of 2022; unchanged
- 0001628280-26-050481:mdna:95 — notes due 2032; unchanged
- 0001628280-26-050481:mdna:97 — senior notes covenants; unchanged
- 0001628280-26-050481:mdna:99 — heading only
- 0001628280-26-050481:mdna:100 — covenant compliance expectation; date rolled forward
- 0001628280-26-050481:mdna:102 — Basler acquisition facts restated; open status covered by the allocation item
- 0001628280-26-050481:mdna:107 — cash flow table; amounts only
- 0001628280-26-050481:mdna:116 — no repurchases in 2026; date rolled forward
- 0001628280-26-050481:mdna:118 — no off-balance sheet arrangements; date rolled forward
- 0001628280-26-050481:mdna:121 — no change in critical accounting estimates; date rolled forward

### Notes

- 0001628280-26-050481:notes:3 — company description; prior wording not in my input; no accounting substance
- 0001628280-26-050481:notes:8 — date rolled forward (note change history)
- 0001628280-26-050481:notes:9 — revenue disaggregation table; amounts only
- 0001628280-26-050481:notes:10 — prior-year disaggregation table; amounts only
- 0001628280-26-050481:notes:23 — date rolled forward (note change history)
- 0001628280-26-050481:notes:24 — restricted cash table; amounts only
- 0001628280-26-050481:notes:25 — heading only
- 0001628280-26-050481:notes:27 — heading only
- 0001628280-26-050481:notes:28 — software cost standard not yet effective, still under evaluation; no change in substance
- 0001628280-26-050481:notes:29 — expense disaggregation standard not yet effective, still under evaluation; no change in substance
- 0001628280-26-050481:notes:30 — disclosure improvements standard not yet effective; no change in substance
- 0001628280-26-050481:notes:37 — Basler allocation table; amounts only, adjustments covered by the measurement-period items
- 0001628280-26-050481:notes:41 — Basler legal and professional fees; amounts only, period rolled forward
- 0001628280-26-050481:notes:48 — Dortmund Fab step-down a year earlier; date rolled forward
- 0001628280-26-050481:notes:49 — Dortmund Fab fees a year earlier; date rolled forward
- 0001628280-26-050481:notes:52 — pro forma table; amounts only
- 0001628280-26-050481:notes:54 — pro forma adjustments table; amounts only
- 0001628280-26-050481:notes:55 — pro forma footnote; date rolled forward
- 0001628280-26-050481:notes:56 — pro forma footnote; repeats the step-up timing in the step-up item
- 0001628280-26-050481:notes:57 — pro forma footnote; date rolled forward
- 0001628280-26-050481:notes:59 — inventory lead-in; date rolled forward
- 0001628280-26-050481:notes:60 — inventory components and reserves table; amounts only, no explanation offered
- 0001628280-26-050481:notes:62 — property lead-in; date rolled forward
- 0001628280-26-050481:notes:63 — property table; amounts only
- 0001628280-26-050481:notes:66 — goodwill lead-in; date rolled forward
- 0001628280-26-050481:notes:67 — goodwill rollforward; amounts only, adjustment explained in the measurement-period items
- 0001628280-26-050481:notes:69 — intangibles lead-in; date rolled forward
- 0001628280-26-050481:notes:70 — intangibles table; amounts only
- 0001628280-26-050481:notes:74 — amortization expense; amounts only
- 0001628280-26-050481:notes:75 — amortization schedule lead-in; date rolled forward
- 0001628280-26-050481:notes:76 — amortization schedule; amounts only
- 0001628280-26-050481:notes:78 — accrued liabilities lead-in; date rolled forward
- 0001628280-26-050481:notes:79 — accrued liabilities table; amounts only
- 0001628280-26-050481:notes:81 — restructuring heading and lead-in; date rolled forward
- 0001628280-26-050481:notes:82 — restructuring table; amounts only
- 0001628280-26-050481:notes:83 — prior-year restructuring table; amounts only
- 0001628280-26-050481:notes:87 — prior-year restructuring narrative; date rolled forward
- 0001628280-26-050481:notes:88 — restructuring reserve balances and payment timing; amounts only, date rolled forward
- 0001628280-26-050481:notes:89 — heading only
- 0001628280-26-050481:notes:90 — date rolled forward (note change history)
- 0001628280-26-050481:notes:91 — debt table; amounts only
- 0001628280-26-050481:notes:92 — heading only
- 0001628280-26-050481:notes:93 — first-quarter amendment; unchanged per note change history
- 0001628280-26-050481:notes:94 — date rolled forward (note change history)
- 0001628280-26-050481:notes:95 — loan pricing; unchanged per note change history
- 0001628280-26-050481:notes:96 — borrowing mechanics; unchanged per note change history
- 0001628280-26-050481:notes:97 — swap designation; text unchanged, a prior paragraph break removed
- 0001628280-26-050481:notes:99 — letters of credit and capacity; amounts only, date rolled forward
- 0001628280-26-050481:notes:100 — heading only
- 0001628280-26-050481:notes:102 — heading only
- 0001628280-26-050481:notes:103 — euro senior notes; unchanged per note change history
- 0001628280-26-050481:notes:104 — senior notes due 2027; unchanged per note change history
- 0001628280-26-050481:notes:105 — senior notes due 2030; wording only (first fiscal quarter became first quarter)
- 0001628280-26-050481:notes:106 — amendment of 2022; unchanged per note change history
- 0001628280-26-050481:notes:107 — notes due 2032; unchanged per note change history
- 0001628280-26-050481:notes:108 — registration and ranking; unchanged per note change history
- 0001628280-26-050481:notes:109 — covenant compliance; date rolled forward, a prior paragraph break removed
- 0001628280-26-050481:notes:110 — redemption terms; unchanged per note change history
- 0001628280-26-050481:notes:111 — interest paid; amounts only, period rolled forward
- 0001628280-26-050481:notes:124 — hedge accounting policy; date rolled forward
- 0001628280-26-050481:notes:126 — cross-currency swaps entered in February 2026, already reported; amounts only
- 0001628280-26-050481:notes:129 — collar schedule; routine monthly trades added; amounts only
- 0001628280-26-050481:notes:130 — collar fair value and reclassification estimate; amounts only
- 0001628280-26-050481:notes:132 — swap fair value and reclassification estimate; amounts only
- 0001628280-26-050481:notes:134 — derivative balance lead-in; date rolled forward
- 0001628280-26-050481:notes:135 — derivative balance table; amounts only
- 0001628280-26-050481:notes:136 — derivative income lead-in; date rolled forward
- 0001628280-26-050481:notes:137 — derivative income table; amounts only
- 0001628280-26-050481:notes:138 — derivative comprehensive income lead-in; date rolled forward
- 0001628280-26-050481:notes:139 — derivative comprehensive income table; amounts only
- 0001628280-26-050481:notes:142 — no change in valuation techniques; date rolled forward
- 0001628280-26-050481:notes:143 — fair value lead-in; date rolled forward
- 0001628280-26-050481:notes:144 — fair value hierarchy table; amounts only
- 0001628280-26-050481:notes:147 — fair value methods for other instruments; date rolled forward
- 0001628280-26-050481:notes:148 — senior notes fair value lead-in; date rolled forward
- 0001628280-26-050481:notes:149 — senior notes fair values; amounts only
- 0001628280-26-050481:notes:153 — pension cost lead-in; date rolled forward
- 0001628280-26-050481:notes:154 — pension cost table; amounts only
- 0001628280-26-050481:notes:157 — other post-employment plans; amounts only
- 0001628280-26-050481:notes:159 — comprehensive income table; amounts only
- 0001628280-26-050481:notes:161 — accumulated comprehensive loss lead-in; date rolled forward
- 0001628280-26-050481:notes:162 — accumulated comprehensive loss table; amounts only
- 0001628280-26-050481:notes:163 — prior-year accumulated comprehensive loss table; amounts only
- 0001628280-26-050481:notes:164 — reclassification lead-in; date rolled forward
- 0001628280-26-050481:notes:165 — reclassification table; amounts only
- 0001628280-26-050481:notes:171 — earnings per share table; amounts only
- 0001628280-26-050481:notes:172 — anti-dilutive shares; amounts only
- 0001628280-26-050481:notes:173 — heading only
- 0001628280-26-050481:notes:174 — no repurchases in 2026; date rolled forward
- 0001628280-26-050481:notes:182 — segment table; amounts only
- 0001628280-26-050481:notes:184 — prior-year segment footnote; date rolled forward
- 0001628280-26-050481:notes:186 — depreciation and amortization lead-in; date rolled forward
- 0001628280-26-050481:notes:187 — depreciation and amortization by segment; amounts only
- 0001628280-26-050481:notes:189 — sales by country; amounts only
- 0001628280-26-050481:notes:191 — long-lived assets by country; amounts only
- 0001628280-26-050481:notes:193 — additions to long-lived assets by country; amounts only
- 0001628280-26-050481:notes:195 — heading only
- 0001628280-26-050481:notes:196 — no off-balance sheet arrangements; date rolled forward (note change history)
- 0001628280-26-050481:notes:197 — heading only
- 0001628280-26-050481:notes:198 — warranty accrual policy; unchanged per note change history
- 0001628280-26-050481:notes:199 — product liability insurance; unchanged per note change history
- 0001628280-26-050481:notes:200 — customer fuse recall; unchanged per note change history; still unaccrued and unquantified, no new facts
- 0001628280-26-050481:notes:201 — heading only
- 0001628280-26-050481:notes:202 — environmental matters; unchanged per note change history
- 0001628280-26-050481:notes:203 — heading only
- 0001628280-26-050481:notes:204 — ordinary-course claims; unchanged per note change history
- 0001628280-26-050481:notes:205 — loss contingency policy; unchanged per note change history
- 0001628280-26-050481:notes:206 — heading only
- 0001628280-26-050481:notes:207 — no material pending litigation; date rolled forward (note change history)
- 0001628280-26-050481:notes:208 — heading only
- 0001628280-26-050481:notes:209 — equity-method background; unchanged per note change history
- 0001628280-26-050481:notes:210 — Powersem ownership; unchanged per note change history
- 0001628280-26-050481:notes:211 — EB Tech ownership; unchanged per note change history
- 0001628280-26-050481:notes:212 — ATEC ownership; unchanged per note change history
- 0001628280-26-050481:notes:213 — related party table; amounts only

### Controls and procedures

- 0001628280-26-050481:item_4_controls:1 — heading only
- 0001628280-26-050481:item_4_controls:2 — heading only
- 0001628280-26-050481:item_4_controls:3 — definition; standard wording
- 0001628280-26-050481:item_4_controls:4 — page number
- 0001628280-26-050481:item_4_controls:5 — disclosure controls effective; date rolled forward
- 0001628280-26-050481:item_4_controls:6 — heading only
- 0001628280-26-050481:item_4_controls:7 — no change in internal control; date rolled forward

### Earnings release (current report of July 29, 2026)

- 0001628280-26-050382:8k_2_02:1 — exhibit file header
- 0001628280-26-050382:8k_2_02:2 — document label
- 0001628280-26-050382:8k_2_02:3 — exhibit label
- 0001628280-26-050382:8k_2_02:4 — press contact
- 0001628280-26-050382:8k_2_02:5 — release title
- 0001628280-26-050382:8k_2_02:6 — heading only
- 0001628280-26-050382:8k_2_02:7 — heading note
- 0001628280-26-050382:8k_2_02:8 — headline sales and organic growth; amounts only
- 0001628280-26-050382:8k_2_02:9 — quarter operating and free cash flow; amounts only
- 0001628280-26-050382:8k_2_02:10 — year-to-date cash flow; amounts only
- 0001628280-26-050382:8k_2_02:11 — earnings per share; amounts only
- 0001628280-26-050382:8k_2_02:12 — margins; amounts only
- 0001628280-26-050382:8k_2_02:13 — dividend headline; same as the dividend item
- 0001628280-26-050382:8k_2_02:14 — dateline
- 0001628280-26-050382:8k_2_02:17 — heading only
- 0001628280-26-050382:8k_2_02:18 — lead-in to guidance
- 0001628280-26-050382:8k_2_02:20 — page marker
- 0001628280-26-050382:8k_2_02:21 — non-GAAP guidance disclaimer; boilerplate
- 0001628280-26-050382:8k_2_02:22 — heading only
- 0001628280-26-050382:8k_2_02:23 — heading only
- 0001628280-26-050382:8k_2_02:25 — Electronics adjusted margin; same drivers as the Electronics-margin item
- 0001628280-26-050382:8k_2_02:26 — heading only
- 0001628280-26-050382:8k_2_02:28 — Transportation adjusted margin; same driver as the commercial-vehicle item
- 0001628280-26-050382:8k_2_02:29 — heading only
- 0001628280-26-050382:8k_2_02:31 — Industrial adjusted margin; covered in the Industrial-margin item
- 0001628280-26-050382:8k_2_02:32 — heading only
- 0001628280-26-050382:8k_2_02:33 — dividend detail; same as the dividend item
- 0001628280-26-050382:8k_2_02:34 — heading only
- 0001628280-26-050382:8k_2_02:35 — conference call logistics
- 0001628280-26-050382:8k_2_02:36 — page marker
- 0001628280-26-050382:8k_2_02:37 — heading only
- 0001628280-26-050382:8k_2_02:38 — company description; boilerplate
- 0001628280-26-050382:8k_2_02:39 — safe-harbor risk list; boilerplate, prior release not in my input
- 0001628280-26-050382:8k_2_02:40 — risk factor reference; boilerplate
- 0001628280-26-050382:8k_2_02:41 — page marker
- 0001628280-26-050382:8k_2_02:42 — heading only
- 0001628280-26-050382:8k_2_02:43 — non-GAAP definitions; boilerplate
- 0001628280-26-050382:8k_2_02:44 — release code
- 0001628280-26-050382:8k_2_02:45 — end marker
- 0001628280-26-050382:8k_2_02:46 — company address
- 0001628280-26-050382:8k_2_02:47 — company name
- 0001628280-26-050382:8k_2_02:48 — heading only
- 0001628280-26-050382:8k_2_02:49 — balance sheet; amounts only
- 0001628280-26-050382:8k_2_02:50 — company name
- 0001628280-26-050382:8k_2_02:51 — heading only
- 0001628280-26-050382:8k_2_02:52 — unaudited label
- 0001628280-26-050382:8k_2_02:53 — statement of operations; amounts only
- 0001628280-26-050382:8k_2_02:54 — company name
- 0001628280-26-050382:8k_2_02:55 — heading only
- 0001628280-26-050382:8k_2_02:56 — unaudited label
- 0001628280-26-050382:8k_2_02:57 — cash flow statement; amounts only
- 0001628280-26-050382:8k_2_02:58 — company name
- 0001628280-26-050382:8k_2_02:59 — heading only
- 0001628280-26-050382:8k_2_02:60 — unaudited label
- 0001628280-26-050382:8k_2_02:61 — segment table; amounts only
- 0001628280-26-050382:8k_2_02:62 — Other footnote; the counterpart cited in the site-closure across-documents item
- 0001628280-26-050382:8k_2_02:63 — abbreviation note
- 0001628280-26-050382:8k_2_02:64 — segment operating margins; amounts only
- 0001628280-26-050382:8k_2_02:65 — company name
- 0001628280-26-050382:8k_2_02:66 — heading only
- 0001628280-26-050382:8k_2_02:67 — units label
- 0001628280-26-050382:8k_2_02:68 — EPS reconciliation; amounts only
- 0001628280-26-050382:8k_2_02:69 — non-GAAP adjustments; amounts only
- 0001628280-26-050382:8k_2_02:70 — EBITDA reconciliation; amounts only
- 0001628280-26-050382:8k_2_02:71 — segment EBITDA for the quarter; amounts only
- 0001628280-26-050382:8k_2_02:72 — segment EBITDA year to date; amounts only
- 0001628280-26-050382:8k_2_02:73 — sales reconciliation for the quarter; amounts only
- 0001628280-26-050382:8k_2_02:74 — Electronics reconciliation for the quarter; amounts only
- 0001628280-26-050382:8k_2_02:75 — Transportation reconciliation for the quarter; amounts only
- 0001628280-26-050382:8k_2_02:76 — footnote definition
- 0001628280-26-050382:8k_2_02:77 — sales reconciliation year to date; amounts only
- 0001628280-26-050382:8k_2_02:78 — Electronics reconciliation year to date; amounts only
- 0001628280-26-050382:8k_2_02:79 — Transportation reconciliation year to date; amounts only
- 0001628280-26-050382:8k_2_02:80 — footnote definition
- 0001628280-26-050382:8k_2_02:81 — tax and free cash flow reconciliation; amounts only
- 0001628280-26-050382:8k_2_02:82 — net debt and covenant EBITDA table; amounts only
- 0001628280-26-050382:8k_2_02:83 — covenant threshold description; no change stated
- 0001628280-26-050382:8k_2_02:85 — covenant EBITDA definition
- 0001628280-26-050382:8k_2_02:86 — rounding note
- 0001628280-26-050382:8k_2_02:87 — footnote caption
- 0001628280-26-050382:8k_2_02:88 — footnote caption
- 0001628280-26-050382:8k_2_02:89 — footnote caption
- 0001628280-26-050382:8k_2_02:91 — tax footnote; the counterpart cited in the statute-lapse across-documents item
- 0001628280-26-050382:8k_2_02:92 — end marker
