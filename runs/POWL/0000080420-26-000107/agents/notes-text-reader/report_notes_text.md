# POWL 10-Q 0000080420-26-000107 (quarter ended June 30, 2026): notes-text reader

## Scope check

I read all six input files in full: input_8k.md, input_controls.md, input_mdna.md, input_notes.md, input_notes_history.md and input_prior_predictions.md. None of them holds a trend table, prices, abnormal returns, short interest, another company's files, a prior run's probability or an outcome window. The prior-predictions file says there is no earlier run, so I carry forward no flags.

Some of what my input could carry is missing, so this report says nothing about it:
- **Auditor's report:** none. This is a 10-Q, and input_controls.md holds only Item 4.
- **Item 1A diff:** none.
- **Exhibit 21 diff:** none.
- **Exhibit 10:** none pulled.

The only 8-K body in the input is the Item 2.02 Exhibit 99.1 of filing 0000080420-26-000103.

I did no arithmetic. Where an amount is given against its prior-period value, both are quoted as the text states them, and I make no comparison.

## Items

29 items.

```json
[
  {
    "id": "estimates_and_discretion_net_favorable_contract_estimate_changes",
    "what_changed": "The note now states net favorable contract-estimate impacts of $12.8 million for the nine months ended June 30, 2026 and $15.1 million for the nine months ended June 30, 2025. The prior quarter's text stated $14.2 million and $8.8 million for the six-month periods. The causes named are unchanged in wording: favorable project execution, reduced cost estimates, negotiations of variable consideration, and revenue recognized from project cancellations. Gross unfavorable changes are still called immaterial. What the year-to-date figure implies for the third quarter alone is for the numbers reader; I make no comparison. The gross-margin explanations in MD&A (mdna:25, mdna:39) and in the press release (8k_2_02:20) do not name or size contract-estimate changes as a driver.",
    "account": "gross profit (revenue and cost of goods sold on over-time contracts)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "For the nine months ended June 30, 2026 and 2025, our operating results were positively impacted by $12.8 million and $15.1 million, respectively, as a result of net changes in contract estimates related to projects in progress at the beginning of the respective period.",
    "paragraph_id": "0000080420-26-000107:notes:45",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_liquidated_damages_exposure_and_accrual",
    "what_changed": "At June 30, 2026 the note states probable liquidated-damages exposure of $6.3 million, possible exposure of $9.3 million, and $5.1 million recorded as a reduction to revenue. The prior quarter's text stated $4.4 million, $7.5 million and $3.8 million at March 31, 2026. Management gives the cause of the recorded amount as actual or projected failure to meet contractual commitments. The remedies (change orders, contract extensions, accelerated completion) and the warning that additional liquidated damages could negatively impact future results are carried unchanged. mdna:16 lists liquidated damages among the factors that can move gross margins. The prose gives no direction for the stated amounts, and I compare none. The expected direction below follows the prose's warning of additional damages.",
    "account": "revenue (liquidated damages recorded as a reduction of revenue)",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "As of June 30, 2026, certain contracts had a probable exposure to liquidated damages claims of $6.3 million, which could possibly increase to $9.3 million under certain circumstances. Based on our actual or projected failure to meet these various contractual commitments, $5.1 million has been recorded as a reduction to revenue.",
    "paragraph_id": "0000080420-26-000107:notes:87",
    "explanation": true
  },
  {
    "id": "revenue_recognition_over_time_share_of_revenue",
    "what_changed": "The note now states that revenue recognized over time was about 97% of revenue for the quarter and 96% for the nine months ended June 30, 2026, against 95% and 96% for the 2025 periods. notes:36 correspondingly states that point-in-time sales of spare parts and replacement breakers were about 3% and 4%. The prior quarter's text stated 95% over time and 5% point in time for both the three and six months ended March 31, 2026. The text gives no reason for the stated mix. Revenue recognized over time depends on estimates of cost to complete.",
    "account": "revenue recognized over time",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Revenues from our custom-engineered products and value-added services transferred to customers over time accounted for approximately 97% and 96% of revenues for the three and nine months ended June 30, 2026, respectively",
    "paragraph_id": "0000080420-26-000107:notes:35",
    "explanation": false
  },
  {
    "id": "revenue_recognition_backlog_and_twelve_month_conversion",
    "what_changed": "The note now states backlog of $2.4 billion at June 30, 2026, of which about $1.3 billion is expected to be recognized as revenue within twelve months. The prior text stated $1.8 billion and about $1.1 billion at March 31, 2026. The MD&A says backlog 'increased', and the company states its own percentages: 35% from March 31, 2026 (mdna:33) and 73% from September 30, 2025 (mdna:47). The press release states 69% from June 30, 2025 (8k_2_02:22). The same sentence is repeated in the policy note (notes:65). The backlog caveat ('may not be indicative ... may be cancelled or modified') is unchanged.",
    "account": "remaining performance obligations (backlog)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "As of June 30, 2026, we had backlog of $2.4 billion, of which approximately $1.3 billion is expected to be recognized as revenue within the next twelve months.",
    "paragraph_id": "0000080420-26-000107:notes:41",
    "explanation": false
  },
  {
    "id": "revenue_recognition_net_contract_liability_bookings_and_milestones",
    "what_changed": "The cause given for the net contract liability position now adds 'strong bookings' to 'favorable contract billing milestones'; the prior text named billing milestones only. Revenue recognized from contract liabilities outstanding at September 30, 2025 is now stated as $243.7 million for the nine months; the prior text stated $204.3 million for the six months. The company again says it allocates a significant percentage of progress billing to the early stages of contracts. mdna:59 attributes operating cash flow partly to 'higher milestone payments associated with strong booking activity'.",
    "account": "contract liabilities (net contract position, including contract assets)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Our net contract billing position remained a net liability at both June 30, 2026 and September 30, 2025, primarily due to strong bookings and favorable contract billing milestones.",
    "paragraph_id": "0000080420-26-000107:notes:57",
    "explanation": true
  },
  {
    "id": "articulation_and_the_filed_history_retention_amounts_carried_from_prior_quarter",
    "what_changed": "Only the date changed. The retention figures now stated for June 30, 2026 are $6.0 million in total, $5.8 million expected within twelve months and recorded in accounts receivable, and $0.2 million in other assets. The prior quarter's text stated the same three figures for March 31, 2026, and the note change history shows the date as the only edit. Whether the retainage balance actually stood at those figures again or was carried forward without update is for the numbers reader.",
    "account": "accounts receivable (retainage)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "As of June 30, 2026 and September 30, 2025, we had retention amounts of $6.0 million and $8.1 million, respectively. Of the retained amount at June 30, 2026, $5.8 million is expected to be collected in the next twelve months and is recorded in accounts receivable.",
    "paragraph_id": "0000080420-26-000107:notes:59",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_surety_bonds_and_letters_of_credit",
    "what_changed": "At June 30, 2026 the note states letters of credit of $103.9 million (a contingent liability), surety bonds outstanding of $492.4 million, and $707.6 million of additional bonding capacity. The prior text stated $78.7 million, $432.8 million and $767.2 million at March 31, 2026. It still says there have been no significant draws or claims, and still warns that sureties could require cash collateral if market conditions or their view of the company's financial position change. The prose gives no direction for these amounts, and I compare none.",
    "account": "letters of credit and surety bonds (off-balance-sheet performance security)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "We were contingently liable for letters of credit of $103.9 million as of June 30, 2026. We also had surety bonds totaling $492.4 million that were outstanding, with additional bonding capacity of $707.6 million available, at June 30, 2026.",
    "paragraph_id": "0000080420-26-000107:notes:82",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_revolver_availability_net_of_letters_of_credit",
    "what_changed": "At June 30, 2026 the note states no borrowings, letters of credit outstanding of $103.9 million, and $46.1 million available under the U.S. Revolver. The prior text stated $78.7 million outstanding and $71.3 million available at March 31, 2026. The $150.0 million commitment and the October 4, 2028 expiry are restated in notes:78, and the same figures appear in mdna:56. mdna:51 still counts available borrowings under the facility toward liquidity sufficiency. The prose gives no direction, and I compare none.",
    "account": "U.S. Revolver availability",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "As of June 30, 2026, there were no amounts borrowed under the U.S. Revolver, and letters of credit outstanding were $103.9 million. There was $46.1 million available for the issuance of letters of credit and borrowings under the U.S. Revolver as of June 30, 2026.",
    "paragraph_id": "0000080420-26-000107:notes:79",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_uk_facility_bank_guarantees",
    "what_changed": "The Powell (UK) Limited facility agreement is now stated at $19.9 million (prior text: $19.8 million). Outstanding guarantees are stated at $5.7 million (prior text: $6.4 million) and additional capacity at $14.2 million (prior text: $13.4 million). The prose does not explain the change in the facility's stated size or say whether it reflects currency translation. The cross-default with the U.S. Revolver, the cash collateral required for guarantees over two years, and covenant compliance are carried unchanged.",
    "account": "bank guarantees under the Powell (UK) facility (off-balance-sheet)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "At June 30, 2026, we had outstanding guarantees totaling $5.7 million, with an additional capacity of $14.2 million",
    "paragraph_id": "0000080420-26-000107:notes:83",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_stock_split_par_value_reclassification",
    "what_changed": "A new sentence says the par value of the shares added by the April 2, 2026 three-for-one split was reclassified from additional paid-in capital to common stock in the third fiscal quarter. The split description has also moved. The prior quarter carried it as a subsequent event under 'Common Stock Split' (prior note_history:27 and :28); that subsection is removed, and the Subsequent Events note (notes:133, notes:134) now carries only the dividend. The press release (8k_2_02:45) says share and per-share amounts for all periods are retroactively adjusted.",
    "account": "common stock (par value), reclassified from additional paid-in capital",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Accordingly, an amount equal to the par value of the increased shares due to the Stock Split was reclassified from additional paid-in capital to common stock in the third fiscal quarter of 2026.",
    "paragraph_id": "0000080420-26-000107:notes:13",
    "explanation": false
  },
  {
    "id": "articulation_and_the_filed_history_director_restricted_stock_split_basis",
    "what_changed": "The paragraph states a February 2026 director restricted-stock grant, made before the April 2, 2026 split, as 4,200 shares at $184.83 per share. The same paragraph says each director's grant is worth $0.1 million and that the share count is that value divided by the grant-date average price. The prose does not say whether the 4,200 shares and $184.83 are on a pre-split or post-split basis. The press release footnote (8k_2_02:45) says share and per-share amounts for all periods are retroactively adjusted. Whether these figures are split-adjusted and agree with the stated grant value is for the numbers reader. This paragraph's prior wording is not in the input.",
    "account": "restricted stock (stock-based compensation)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "In February 2026, 4,200 shares of restricted stock were issued to our non-employee directors at a price of $184.83 per share.",
    "paragraph_id": "0000080420-26-000107:notes:94",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_executed_leases_not_yet_commenced",
    "what_changed": "The lease note discloses two operating leases executed in Fiscal 2026, both expected to commence in Fiscal 2027. One is in Canada, for additional office and warehouse space. The other is adjacent to the Houston manufacturing facility, for additional manufacturing and warehouse space. The maturity table (notes:118, notes:119) is now laid out in three columns, 'Leases Signed', 'Less: Leases Not Yet Commenced' and 'Leases in Effect', with the payments for leases not yet commenced shown separately. This paragraph's prior wording is not in the input, so whether one or both leases are new this quarter cannot be confirmed.",
    "account": "operating lease liabilities and right-of-use assets",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "In Fiscal 2026, we executed two operating leases, one in Canada for additional office and warehouse space and the other adjacent to our Houston manufacturing facility for additional manufacturing and warehouse space. Both leases are expected to commence in Fiscal 2027.",
    "paragraph_id": "0000080420-26-000107:notes:117",
    "explanation": false
  },
  {
    "id": "across_documents_ohio_leased_capacity_absent_from_lease_note",
    "what_changed": "The CFO refers to 'added leased capacity in Houston and Ohio'. The lease note (notes:117) names the Fiscal 2026 leases as one in Canada and one adjacent to Houston, and no Ohio lease or facility is named anywhere in the notes or the MD&A. The prose does not say whether an Ohio lease exists, whether it is short-term (such leases are kept off the balance sheet under notes:115) or not yet signed, or whether it is reflected in the lease commitments.",
    "account": "operating lease commitments",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "our added leased capacity in Houston and Ohio",
    "paragraph_id": "0000080420-26-000103:8k_2_02:28",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_greenfield_capacity_expansion_evaluation",
    "what_changed": "The CFO says the company is evaluating greenfield capacity expansions beyond its added leased capacity, and is 'prudently adding capacity to support the acceleration in our backlog'. The MD&A investing paragraph (mdna:61) mentions only the Jacintoport expansion. mdna:51 says cash, investments and revolver availability will support 'future organic and inorganic business growth'.",
    "account": "capital expenditures (property, plant and equipment)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "We are also evaluating greenfield capacity expansions incremental to our added leased capacity in Houston and Ohio, while prioritizing adequate returns and ensuring the optimal manufacturing footprint for Powell over the long term.",
    "paragraph_id": "0000080420-26-000103:8k_2_02:28",
    "explanation": false
  },
  {
    "id": "results_against_expectations_gross_margin_guidance_trailing_twelve_months",
    "what_changed": "In the press release, the CFO guides that gross margins will hold at trailing-twelve-month levels while capacity is added. He also says he is 'confident that Powell will deliver another very strong year of financial results as we close out Fiscal 2026 and look ahead to Fiscal 2027'. Two MD&A passages in the same period point the other way. mdna:15 says data center projects may shift product mix toward less custom engineered-to-order equipment, and mdna:18 says cost increases could bring 'negative impacts on our margins'.",
    "account": "gross margin",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "We expect that gross margins will maintain levels consistent to the trailing twelve months, while prudently adding capacity to support the acceleration in our backlog",
    "paragraph_id": "0000080420-26-000103:8k_2_02:28",
    "explanation": false
  },
  {
    "id": "results_against_expectations_jacintoport_yard_completion_by_fiscal_year_end",
    "what_changed": "The MD&A says the Jacintoport fabrication yard expansion in Houston is planned to be completed by the end of Fiscal 2026. The press release (8k_2_02:28) says it is expected by the close of Fiscal 2026 and that production will ramp up to support recent core industrial project awards. Investing cash for the nine months is attributed primarily to maturities of short-term investments, partly offset by capital spending.",
    "account": "property, plant and equipment (construction in process)",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "We continue to progress the expansion of our Jacintoport fabrication yard in Houston, which is planned to be completed by the end of Fiscal 2026.",
    "paragraph_id": "0000080420-26-000107:mdna:61",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_operating_cash_flow_milestone_payments",
    "what_changed": "The MD&A states nine-month operating cash of $195.0 million (prior-year period: $106.9 million); the overview (mdna:5) states that $100.2 million was generated in the third quarter. The increase is attributed to improved earnings and to higher milestone payments associated with strong booking activity. Those milestone payments are customer billings in advance of performance, which notes:57 places in the net contract liability.",
    "account": "cash from operating activities",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase in operating cash flow was primarily driven by improved earnings and higher milestone payments associated with strong booking activity.",
    "paragraph_id": "0000080420-26-000107:mdna:59",
    "explanation": false
  },
  {
    "id": "across_documents_cash_increase_attributed_to_earnings",
    "what_changed": "The liquidity paragraph attributes the increase in cash, cash equivalents and short-term investments to 'our strong earnings performance'. It nets out share withholding for taxes, capital expenditures and dividends, and does not name customer milestone payments. mdna:59 and notes:57, by contrast, name milestone payments tied to strong bookings as a driver of operating cash and of the net contract liability. The paragraph also says liquidity will support 'future organic and inorganic business growth'.",
    "account": "cash, cash equivalents and short-term investments",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase was primarily driven by our strong earnings performance, partially offset by cash payments related to shares withheld in lieu of employee tax withholding, capital expenditures and dividend payments.",
    "paragraph_id": "0000080420-26-000107:mdna:51",
    "explanation": false
  },
  {
    "id": "results_against_expectations_data_center_mega_order_booked_in_quarter",
    "what_changed": "The data center order valued at over $400 million, disclosed in the prior 10-Q as a subsequent event, is now booked in the third quarter. Third-quarter bookings are stated at $934 million with three mega orders: the data center order, an LNG order of about $60 million and a petrochemical order of about $75 million. Nine-month bookings are stated at $1.9 billion with seven mega orders. The press release adds that the data center order relates to 'a behind-the-meter design of on-site generation assets' and that the petrochemical order is in the fertilizer industry (8k_2_02:21). The CEO calls the bookings a record, with a 3.0x book-to-bill (8k_2_02:17). The MD&A paragraph also cautions that macroeconomic and geopolitical developments could affect customer spending behavior or the timing of project awards.",
    "account": "new orders (bookings) and backlog",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "During the third fiscal quarter, we achieved total bookings of $934 million, including three mega orders, a data center project valued at over $400 million, which was disclosed as a subsequent event in the second fiscal quarter",
    "paragraph_id": "0000080420-26-000107:mdna:10",
    "explanation": false
  },
  {
    "id": "results_against_expectations_data_center_awards_nine_months",
    "what_changed": "The MD&A now states about $800 million of data center infrastructure awards in the first nine months of Fiscal 2026. That figure includes the third-quarter mega order of over $400 million and two first-half mega orders each exceeding $75 million in contract value. The paragraph also says the company is 'observing increased activity across other industrial end markets'. mdna:33 and mdna:47 state that commercial and other industrial is 40% of total backlog.",
    "account": "backlog (commercial and other industrial, data center)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "During the first nine months of Fiscal 2026, we were awarded approximately $800 million in data center infrastructure projects",
    "paragraph_id": "0000080420-26-000107:mdna:13",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_data_center_product_mix_risk_language",
    "what_changed": "The paragraph now carries language specific to data centers, which I can see only in its current form. As data center projects become a larger part of backlog and revenue, product mix may shift toward less custom engineered-to-order equipment and systems. The company says it 'ha[s], and will, become subject' to additional end-market risks, including fluctuations in data center demand and legislative or regulatory developments, and that results may be affected. The Item 1A diff is not in the input, so I cannot check whether the risk factors were amended to match.",
    "account": "revenue mix and gross margin",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "As data center projects become a larger component of our backlog and revenues: (i) our product mix may shift",
    "paragraph_id": "0000080420-26-000107:mdna:15",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_petrochemical_revenue_backlog_runoff",
    "what_changed": "Petrochemical revenue is described as down 49% to $18.5 million for the quarter (mdna:24, 8k_2_02:19) and down 39% to $68.8 million for the nine months. The cause given is a reduction in petrochemical backlog after a large order secured in Fiscal 2023 was completed, together with lower backlog levels. Light rail traction power revenue is also described as down: 7% for the quarter and 4% for the nine months.",
    "account": "revenue (petrochemical and light rail traction power markets)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "These declines were primarily attributable to a reduction in backlog within the petrochemical market following the completion of a large petrochemical order secured in Fiscal 2023, as well as lower backlog levels in these markets.",
    "paragraph_id": "0000080420-26-000107:mdna:38",
    "explanation": false
  },
  {
    "id": "across_documents_petrochemical_recovery_characterization",
    "what_changed": "The nine-month bookings paragraph names 'a recovery of the petrochemical market' as a driver. mdna:11 says petrochemical activity 'has remained subdued over the past several quarters' and that the company is 'cautiously optimistic' the market 'may be entering the early stages of a cyclical recovery'. mdna:8 lists the strong-demand markets without petrochemical, and mdna:24, mdna:38 and 8k_2_02:19 describe petrochemical revenue as declining on lower backlog. Within the same filing, the market is called recovered in one paragraph and only possibly entering recovery in another.",
    "account": "new orders (bookings), petrochemical market",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "This increase was primarily driven by stronger booking activity in the commercial and other industrial market, a recovery of the petrochemical market, and continued growth in the oil and gas (excluding petrochemical) and electric utility markets.",
    "paragraph_id": "0000080420-26-000107:mdna:48",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_tariffs_commodities_supply_chain",
    "what_changed": "The paragraph is carried as changed, but its prior wording is not in the input, so the specific edit cannot be isolated. As it now reads, it describes continued high commodity-price volatility and persistent supply chain delays for specific engineered components through the first nine months of Fiscal 2026. It cites trade-policy changes 'including legal challenges thereto', possible international retaliation, and concerns over inflation, recession and slowing growth. It warns of possible increases in the cost of raw materials and components and of negative impacts on margins. The responses it names are managing product pricing, refining delivery schedules and managing bid validity dates.",
    "account": "gross margin (cost of goods sold)",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "We could potentially face the challenge of increased costs of raw materials and engineered components as well as negative impacts on our margins",
    "paragraph_id": "0000080420-26-000107:mdna:18",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_international_revenue_quarter_decline",
    "what_changed": "Third-quarter international revenue is described as having 'decreased slightly', while domestic revenue is described as up 12%. The nine-month paragraph (mdna:37) describes international revenue as up 16%, driven by Asia/Pacific, Middle East and Africa, and Europe, 'partially offset by decreased activity in Canada'.",
    "account": "revenue (international)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "International revenue decreased slightly by 1%, or $0.6 million, to $61.1 million in the third quarter of Fiscal 2026.",
    "paragraph_id": "0000080420-26-000107:mdna:23",
    "explanation": false
  },
  {
    "id": "earnings_quality_gross_profit_attributed_to_volume_and_pricing",
    "what_changed": "The press release attributes the gross profit increases to higher volume and a 'continued strong and stable pricing environment'. The MD&A says the quarter's gross margin 'remained flat at 31%' and attributes the increase primarily to higher revenue (mdna:25). For the nine months it attributes margin improvement to favorable volume leverage and strong project execution in a stable pricing environment (mdna:39). None of these three passages names or sizes the net favorable contract-estimate changes stated in notes:45.",
    "account": "gross profit",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increases in gross profit were primarily driven by higher volume levels and a continued strong and stable pricing environment.",
    "paragraph_id": "0000080420-26-000103:8k_2_02:20",
    "explanation": false
  },
  {
    "id": "articulation_and_the_filed_history_press_release_gross_profit_comparatives",
    "what_changed": "The press release states $87.9 million as gross profit for both comparison periods: the third quarter of Fiscal 2025, at 30.7% of revenue, and the second quarter of Fiscal 2026, at 29.6% of revenue. It states an 8% increase against each. Whether both comparatives agree with the filed prior-period statements is for the numbers reader; I have not checked them.",
    "account": "gross profit (comparative periods)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Gross profit of $95.3 million, or 30.6% of revenue, increased 8% compared to $87.9 million, or 30.7% of revenue, in the prior year and increased sequentially by 8% compared to $87.9 million, or 29.6% of revenue in the second quarter of Fiscal 2026.",
    "paragraph_id": "0000080420-26-000103:8k_2_02:20",
    "explanation": false
  },
  {
    "id": "earnings_quality_sga_compensation_infrastructure_and_remsdaq",
    "what_changed": "The nine-month increase in SG&A is attributed to higher compensation, including the effect of the Remsdaq Limited acquisition completed in August 2025, and to 'increased spending on infrastructure'. The quarterly paragraph (mdna:27) names compensation and Remsdaq only. mdna:31 and mdna:45 say SG&A and R&D partly offset the gain in gross profit.",
    "account": "selling, general and administrative expenses",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "primarily due to higher compensation expenses, including the impact of the Remsdaq Limited acquisition completed in August 2025, and increased spending on infrastructure",
    "paragraph_id": "0000080420-26-000107:mdna:41",
    "explanation": false
  },
  {
    "id": "across_documents_press_release_outlook_tone_versus_mdna_caution",
    "what_changed": "The CEO's outlook in the press release calls the outlook for each core end market highly favorable and expects activity across each core market to 'remain robust'. The MD&A for the same period is more guarded. It is monitoring macroeconomic and geopolitical developments that could affect customer spending or award timing (mdna:10). It describes petrochemical activity as subdued for several quarters (mdna:11). It cites trade policy, inflation, recession and slowing-growth concerns (mdna:18).",
    "account": "new orders (bookings)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "The outlook for each of our core end markets are highly favorable",
    "paragraph_id": "0000080420-26-000103:8k_2_02:27",
    "explanation": false
  }
]
```

## Insufficient

3 entries. The input does not let me decide whether a substantive change occurred.

- **0000080420-26-000107:mdna:16:** The paragraph is carried as changed, and its prior wording is not in the input. It reads as standing narrative on operating-result variability: change orders, claims, liquidated damages and supply chain. It names no new amount, event or matter, and I cannot isolate the edit.
- **8-K 0000080420-26-000095 (2026-07-06, Item 5.02):** This 8-K was filed after the prior 10-Q and reports an officer or director change. Its body is not in the input, so I cannot say who or what changed.
- **8-K 0000080420-26-000103 (2026-08-03, Items 8.01 and 9.01):** Only the Item 2.02 Exhibit 99.1 body is in the input. The Item 8.01 body is not, though it may be the dividend announcement also given in notes:134.

## Paragraphs not made an item

Each line gives the paragraph and why it was not made an item. Where a paragraph's substance sits inside an item, the item's id is named.

### Item 4 (0000080420-26-000107)

This section is carried verbatim. No prior Item 4 is in the input, so it cannot be diffed.

- item_4_controls:1 — heading
- item_4_controls:2 — heading
- item_4_controls:3 — standard design statement for disclosure controls
- item_4_controls:4 — disclosure controls concluded 'effective'; nothing in the text signals a change
- item_4_controls:5 — heading
- item_4_controls:6 — no changes in internal control over financial reporting; only the quarter name rolled forward
- item_4_controls:7 — page number

### Auditor's report

- None in the input (10-Q).

### Notes (0000080420-26-000107)

- notes:16 — ASU 2023-09 boilerplate; still 'currently evaluating'; no adoption decision or amount
- notes:17 — ASU 2024-03 boilerplate; still 'currently evaluating'; no adoption decision or amount
- notes:18 — standard EPS method text; no new amount or policy
- notes:19 — table introduction; date rolled forward
- notes:20 — EPS table; amounts only
- notes:23 — inventory table, including the excess and obsolete provision; amounts only, no prose explanation
- notes:26 — property, plant and equipment table; amounts only (construction in process tied to the Jacintoport expansion item)
- notes:27 — no finance-lease assets; date rolled forward
- notes:30 — warranty rollforward table; amounts only
- notes:36 — point-in-time revenue share, the complement of notes:35; covered by revenue_recognition_over_time_share_of_revenue
- notes:55 — table introduction; date rolled forward
- notes:56 — contract asset and liability table; amounts only; prose covered by revenue_recognition_net_contract_liability_bookings_and_milestones
- notes:61 — table introduction; period rolled forward
- notes:62 — revenue by geography table; amounts only (prose covered by narrative_signs_of_operating_pressure_international_revenue_quarter_decline)
- notes:63 — revenue by market table; amounts only (prose covered by narrative_signs_of_operating_pressure_petrochemical_revenue_backlog_runoff)
- notes:65 — performance-obligation policy; the backlog sentence repeats notes:41 and is covered by revenue_recognition_backlog_and_twelve_month_conversion; otherwise the date rolled forward
- notes:67 — goodwill and intangible totals; amounts only; still no impairment
- notes:69 — table introduction; period rolled forward
- notes:70 — goodwill rollforward (currency translation only); amounts only
- notes:72 — table introduction; date rolled forward
- notes:73 — intangible asset table; amounts only
- notes:75 — table introduction; date rolled forward
- notes:76 — amortization schedule; amounts only
- notes:77 — heading
- notes:78 — revolver terms restated ($150.0 million; Bank of America and Texas Capital Bank; expires October 4, 2028); the note change history for the debt tag records no change to this paragraph
- notes:80 — revolver covenant compliance; date rolled forward
- notes:81 — heading
- notes:84 — heading
- notes:85 — litigation; wording only ('provided for' replaces 'provided', per note_history:3)
- notes:86 — heading
- notes:90 — RSU program description and outstanding RSU count; amounts and date only
- notes:91 — table introduction; period rolled forward
- notes:92 — RSU activity table; amounts only
- notes:93 — RSU compensation expense; amounts only
- notes:101 — table introduction; date rolled forward
- notes:102 — fair-value table, including the Level 3 Remsdaq contingent consideration and a nil short-term investments line; amounts only, no prose change
- notes:110 — no transfers between fair-value levels; date rolled forward
- notes:111 — standard lease-composition introduction; no new amount or matter
- notes:112 — lease cost table; amounts only
- notes:113 — footnote defining variable lease cost; wording only
- notes:115 — lease table introduction; date rolled forward
- notes:116 — lease asset and liability table; amounts only
- notes:118 — maturity-table introduction now naming executed leases with future start dates; covered by structure_and_disclosure_changes_executed_leases_not_yet_commenced
- notes:119 — lease maturity table in its new three-column layout; covered by structure_and_disclosure_changes_executed_leases_not_yet_commenced
- notes:120 — weighted-average discount rate and remaining lease term; amounts only
- notes:122 — standard CODM text; paragraph split at a page break; no new substance
- notes:123 — continuation of the CODM text; no new substance
- notes:124 — table introduction; period rolled forward
- notes:125 — segment net income table; amounts only
- notes:126 — table introduction; period rolled forward
- notes:127 — revenue by geography table (duplicate of notes:62); amounts only
- notes:129 — long-lived assets by country table; amounts only
- notes:131 — effective tax rate table; amounts only
- notes:132 — tax narrative; rates and drivers (R&D credit, nondeductible items, first-quarter RSU vesting discrete items) restated for the new period; same drivers as mdna:29 and mdna:43
- notes:133 — Subsequent Events heading; the common stock split subsection was removed and moved to Note A; covered by structure_and_disclosure_changes_stock_split_par_value_reclassification
- notes:134 — quarterly dividend of $0.09 per share declared August 3, 2026; same per-share amount; dates rolled forward

### MD&A (0000080420-26-000107)

- mdna:5 — headline amounts for the quarter; the $100.2 million third-quarter operating cash figure is cited in liquidity_and_capital_operating_cash_flow_milestone_payments
- mdna:8 — backlog figures covered by revenue_recognition_backlog_and_twelve_month_conversion; the market-demand sentence is cited in across_documents_petrochemical_recovery_characterization
- mdna:11 — LNG and petrochemical mega orders and petrochemical 'cautiously optimistic', covered by results_against_expectations_data_center_mega_order_booked_in_quarter and across_documents_petrochemical_recovery_characterization; the hydrogen, carbon capture and alternative-fuels sentence reads as a standing description of end markets
- mdna:12 — electric utility nine-month bookings of $313 million; period rolled forward, amount only
- mdna:16 — insufficient (see above)
- mdna:19 — page number
- mdna:21 — heading; period rolled forward
- mdna:24 — quarterly revenue by market; petrochemical and light rail declines covered by narrative_signs_of_operating_pressure_petrochemical_revenue_backlog_runoff; growth markets restated
- mdna:25 — quarterly gross profit; covered by earnings_quality_gross_profit_attributed_to_volume_and_pricing
- mdna:27 — quarterly SG&A; covered by earnings_quality_sga_compensation_infrastructure_and_remsdaq
- mdna:29 — quarterly tax; period rolled forward, same drivers as notes:132
- mdna:31 — quarterly net income; amounts and drivers restated (covered by the gross profit and SG&A items)
- mdna:33 — backlog increase since March 31 and mix by market; covered by revenue_recognition_backlog_and_twelve_month_conversion and results_against_expectations_data_center_awards_nine_months
- mdna:34 — quarterly bookings; covered by results_against_expectations_data_center_mega_order_booked_in_quarter
- mdna:35 — heading; period rolled forward
- mdna:37 — nine-month revenue by geography, including the Canada offset; covered by narrative_signs_of_operating_pressure_international_revenue_quarter_decline
- mdna:39 — nine-month gross profit; covered by earnings_quality_gross_profit_attributed_to_volume_and_pricing
- mdna:43 — nine-month tax; period rolled forward, same drivers as notes:132
- mdna:45 — nine-month net income; amounts and drivers restated
- mdna:47 — backlog increase since September 30 and mix by market; covered by revenue_recognition_backlog_and_twelve_month_conversion and results_against_expectations_data_center_awards_nine_months
- mdna:50 — current assets to current liabilities of 2.0 times; amount only
- mdna:53 — $125.8 million of cash held outside the U.S.; amount only; indefinite-reinvestment statement unchanged in substance
- mdna:56 — revolver letters of credit and availability (same text as notes:79); covered by liquidity_and_capital_revolver_availability_net_of_letters_of_credit
- mdna:63 — financing cash; period rolled forward; driver is share withholding linked to share price
- mdna:66 — page number

### 8-K 0000080420-26-000103, Item 2.02, Exhibit 99.1

- 8k_2_02:1 — exhibit file header
- 8k_2_02:2 — document header
- 8k_2_02:3 — exhibit label
- 8k_2_02:4 — press release label
- 8k_2_02:5 — contacts table
- 8k_2_02:6 — headline
- 8k_2_02:7 — dateline and introduction boilerplate
- 8k_2_02:8 — heading
- 8k_2_02:9 — revenue bullet; amounts, covered by the petrochemical and international revenue items
- 8k_2_02:10 — gross profit bullet; covered by earnings_quality_gross_profit_attributed_to_volume_and_pricing
- 8k_2_02:11 — net income and EPS bullet; amounts only
- 8k_2_02:12 — new orders bullet; covered by results_against_expectations_data_center_mega_order_booked_in_quarter
- 8k_2_02:13 — backlog bullet; covered by revenue_recognition_backlog_and_twelve_month_conversion
- 8k_2_02:14 — cash bullet; amount, covered by across_documents_cash_increase_attributed_to_earnings
- 8k_2_02:15 — mega orders bullet; covered by results_against_expectations_data_center_mega_order_booked_in_quarter
- 8k_2_02:16 — exhibit marker
- 8k_2_02:17 — CEO quote (record orders, 3.0x book-to-bill, mega orders); covered by results_against_expectations_data_center_mega_order_booked_in_quarter
- 8k_2_02:18 — heading
- 8k_2_02:19 — revenue paragraph; market drivers covered by the petrochemical item; the sequential figure is an amount only
- 8k_2_02:21 — orders paragraph (behind-the-meter, fertilizer, Gulf Coast detail); covered by results_against_expectations_data_center_mega_order_booked_in_quarter
- 8k_2_02:22 — backlog paragraph; covered by revenue_recognition_backlog_and_twelve_month_conversion
- 8k_2_02:23 — exhibit marker
- 8k_2_02:24 — net income paragraph; amounts and drivers restated
- 8k_2_02:25 — stock split; duplicate of notes:13, covered by structure_and_disclosure_changes_stock_split_par_value_reclassification
- 8k_2_02:26 — heading
- 8k_2_02:29 — exhibit marker
- 8k_2_02:30 — heading
- 8k_2_02:31 — conference call logistics
- 8k_2_02:32 — webcast logistics
- 8k_2_02:33 — exhibit marker
- 8k_2_02:34 — heading
- 8k_2_02:35 — company description boilerplate
- 8k_2_02:36 — website and material-information boilerplate
- 8k_2_02:37 — exhibit marker
- 8k_2_02:38 — heading
- 8k_2_02:39 — heading
- 8k_2_02:40 — condensed statement of operations table; amounts only
- 8k_2_02:41 — exhibit marker
- 8k_2_02:42 — heading
- 8k_2_02:43 — heading
- 8k_2_02:44 — condensed balance sheet table; amounts only
- 8k_2_02:45 — stock split footnote (retroactive adjustment); covered by the stock split item and articulation_and_the_filed_history_director_restricted_stock_split_basis
- 8k_2_02:46 — definition of new orders
- 8k_2_02:47 — backlog caveat boilerplate
- 8k_2_02:48 — definition of a mega order (over $50 million)
- 8k_2_02:49 — definition of working capital

### 8-K item-code list and late-filing list

- **Item-code list:** Since the prior 10-Q, the only new filings are 0000080420-26-000095 (Item 5.02; insufficient, see above) and 0000080420-26-000103 (Items 2.02, 8.01 and 9.01). The older Item 4.02 filings (2011, 2007) are history, not a change this period.
- **Late-filing list:** The only entry is the 2007 NT 10-Q. It is history, not a change this period.

### Note change history

The history only shows which paragraphs changed. Each entry below is accounted for through the notes paragraph it mirrors.

- note_history:1 — mirrors notes:82; related_parties_contingencies_and_subsequent_events_surety_bonds_and_letters_of_credit
- note_history:2 — mirrors notes:83; related_parties_contingencies_and_subsequent_events_uk_facility_bank_guarantees
- note_history:3 — mirrors notes:85; wording only
- note_history:4 — mirrors notes:87; estimates_and_discretion_liquidated_damages_exposure_and_accrual
- note_history:5 — mirrors notes:13; structure_and_disclosure_changes_stock_split_par_value_reclassification
- note_history:6 — mirrors notes:79; liquidity_and_capital_revolver_availability_net_of_letters_of_credit
- note_history:7 — mirrors notes:80; date rolled forward
- note_history:8 — mirrors notes:61; period rolled forward
- note_history:9 — mirrors notes:62; amounts only
- note_history:10 — mirrors notes:63; amounts only
- note_history:11 — mirrors notes:35; revenue_recognition_over_time_share_of_revenue
- note_history:12 — mirrors notes:36; covered by revenue_recognition_over_time_share_of_revenue
- note_history:13 — mirrors notes:65; backlog covered by revenue_recognition_backlog_and_twelve_month_conversion
- note_history:14 — duplicate of note_history:11 (notes:35)
- note_history:15 — duplicate of note_history:12 (notes:36)
- note_history:16 — mirrors notes:41; revenue_recognition_backlog_and_twelve_month_conversion
- note_history:17 — mirrors notes:45; estimates_and_discretion_net_favorable_contract_estimate_changes
- note_history:18 — mirrors notes:55; date rolled forward
- note_history:19 — mirrors notes:56; amounts only
- note_history:20 — mirrors notes:57; revenue_recognition_net_contract_liability_bookings_and_milestones
- note_history:21 — mirrors notes:59; articulation_and_the_filed_history_retention_amounts_carried_from_prior_quarter
- note_history:22 — duplicate of note_history:8 (notes:61)
- note_history:23 — duplicate of note_history:9 (notes:62 and notes:127)
- note_history:24 — duplicate of note_history:10 (notes:63)
- note_history:25 — mirrors notes:133; covered by the stock split item
- note_history:26 — mirrors notes:134; dates rolled forward
- 0000080420-26-000070:note_history:1 to :26 — the prior-period versions of the entries above, used only for the comparisons quoted in the items
- 0000080420-26-000070:note_history:27 — removed Subsequent Events / Common Stock Split heading; covered by the stock split item
- 0000080420-26-000070:note_history:28 — removed subsequent-event stock split paragraph; covered by the stock split item
