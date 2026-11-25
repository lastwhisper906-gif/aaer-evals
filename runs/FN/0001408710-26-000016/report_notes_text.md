<!-- the quote gate removed 1 item(s) from this copy; input_manifest.json lists each with its reason -->
# Notes text reader — Fabrinet, quarterly report for the third quarter of fiscal 2026 (quarter ended March 27, 2026)

## Scope and inputs

I read six files in full: the notes, the note change history, the MD&A, the controls and procedures item, the current-report listing and the prior predictions file.

- **Nothing forbidden is present.** No trend table, prices, abnormal returns, short interest, other-company files, prior probabilities or outcome window appeared.
- **Not in the bundle.** There is no risk factors diff, no subsidiaries exhibit diff and no material contract exhibit. No auditor's report is included, which is normal for a quarterly report. No current-report body is carried; see the first item.
- **Prior flags.** None are on record for this company.
- **No arithmetic.** Directions below are what the prose implies. Where the prose gives only amounts, the direction is `none` and the comparison is left to the numbers reader.
- **Counts.** 42 items. 4 are marked `insufficient` (the first, the manufacturing capacity statement, the hedging program paragraph and the IRS examination wording). 2 carry `explanation: true` (inventories and trade receivables).

## Items

```json
[
{
    "id": "related_parties_contingencies_and_subsequent_events_raytek_minority_stake_after_quarter_end",
    "what_changed": "A subsequent-events note appears for the first time. On March 25, 2026 the Company agreed to buy a 16.0% equity interest in Raytek Semiconductor for approximately 1.02 billion New Taiwan dollars ($32.4 million), subject to customary closing conditions. The note says nothing was recognized in the third quarter of fiscal 2026 because the transaction was completed after the quarter ended. The stake should first appear in the fourth quarter of fiscal 2026.",
    "account": "other investments (equity security without readily determinable fair value)",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "No amounts related to the investment have been recognized in the accompanying condensed consolidated financial statements for the three and nine months ended March 27, 2026 because the transaction was completed after the fiscal quarter ended.",
    "paragraph_id": "0001408710-26-000016:notes:171",
    "explanation": false
  },
{
    "id": "estimates_and_discretion_raytek_stake_no_significant_influence_held_at_cost",
    "what_changed": "A new accounting judgment. The Company evaluated the Raytek stake under the equity-method guidance and concluded it has no significant influence. It will carry the stake at cost, adjusted only for observable price changes and impairment, because there is no readily determinable fair value. Changes in Raytek's value will not reach earnings unless an observable transaction or an impairment occurs.",
    "account": "other investments (equity security without readily determinable fair value)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "The Company will account for this investment at cost, subject to adjustments for observable price changes and impairment, as the investment does not have a readily determinable fair value.",
    "paragraph_id": "0001408710-26-000016:notes:172",
    "explanation": false
  },
{
    "id": "liquidity_and_capital_raytek_purchase_price_cash_outflow",
    "what_changed": "MD&A adds a Recent Developments heading and paragraph on the Raytek purchase: approximately 1.02 billion New Taiwan dollars ($32.4 million), subject to customary closing conditions. It says the stake 'will be accounted for' at cost. None of the liquidity paragraphs carried as text mention it. The purchase price implies a cash payment after quarter end.",
    "account": "cash and cash equivalents",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "for approximately NT$1.02 billion ($32.4 million), subject to customary closing conditions",
    "paragraph_id": "0001408710-26-000016:mdna:24",
    "explanation": false
  },
{
    "id": "related_parties_contingencies_and_subsequent_events_tariff_refund_recovery_not_recorded",
    "what_changed": "A new Other Matters heading and paragraph. In February 2026 the Supreme Court struck down certain tariffs imposed under the International Emergency Economic Powers Act. Customs and Border Protection then announced steps toward a refund process. The Company assessed recovery of tariffs it previously paid under a loss-recovery model. It booked no receivable because recovery is not considered probable. This is a possible gain that is disclosed but not recorded.",
    "account": "other receivables; cost of revenues (previously incurred tariffs)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "has not recorded a receivable because recovery is not considered probable",
    "paragraph_id": "0001408710-26-000016:notes:155",
    "explanation": false
  },
{
    "id": "related_parties_contingencies_and_subsequent_events_casix_litigation_disclosure_removed",
    "what_changed": "The Litigation and claim section has been removed from the commitments and contingencies note. The prior quarter's text described a suit against the Casix subsidiary in China seeking renminbi 400 million, with interest from March 1, 2000. It said the appellate court dismissed the suit on jurisdictional grounds in November 2025. No contingency is now disclosed in its place, and the removed text described no accrual.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "dismissed the lawsuit on jurisdictional grounds",
    "paragraph_id": "0001408710-26-000008:note_history:11",
    "explanation": false
  },
{
    "id": "liquidity_and_capital_purchase_obligations_restated_for_quarter_end",
    "what_changed": "Purchase obligations and other commitments to third parties are now stated as $2.74 billion at March 27, 2026. The prior quarter's text stated $1.94 billion at December 26, 2025. The unchanged lead-in says these are mainly inventory commitments, generally fulfilled within one year and cancellable or reschedulable before delivery. No prose explains the amount.",
    "account": "purchase obligations (inventory purchases and trade accounts payable)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "As of March 27, 2026, the Company had purchase obligations and other commitments to third parties of $2.74 billion.",
    "paragraph_id": "0001408710-26-000016:notes:144",
    "explanation": false
  },
{
    "id": "liquidity_and_capital_capital_expenditure_commitments_restated_for_quarter_end",
    "what_changed": "Capital expenditure commitments to third parties are now stated as $164.7 million at March 27, 2026. The prior quarter's text stated $193.7 million at December 26, 2025. The Chonburi building contract sentence (approximately $132.5 million, 4.45 billion Thai baht) is unchanged according to the note change history.",
    "account": "property, plant and equipment",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "As of March 27, 2026, the Company had total capital expenditure commitments to third parties of $164.7 million.",
    "paragraph_id": "0001408710-26-000016:notes:147",
    "explanation": false
  },
{
    "id": "earnings_quality_inventory_increase_for_next_quarter_demand",
    "what_changed": "MD&A names an increase in inventories as the first cause of lower operating cash flow for the first nine months of fiscal 2026. It says the inventory was built to support higher demand in the next quarter. This is management's explanation of the inventory balance, tied to expected demand in the fourth quarter of fiscal 2026.",
    "account": "inventories",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "an increase in inventories to support higher demand in the next quarter",
    "paragraph_id": "0001408710-26-000016:mdna:129",
    "explanation": true
  },
{
    "id": "earnings_quality_trade_receivables_increase_on_collection_timing",
    "what_changed": "MD&A names an increase in trade receivables as the second cause of lower operating cash flow. It attributes the increase to timing of collection only, with nothing on payment terms, customer mix or credit quality.",
    "account": "trade accounts receivable",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "an increase in trade receivables due to timing of collection",
    "paragraph_id": "0001408710-26-000016:mdna:129",
    "explanation": true
  },
{
    "id": "liquidity_and_capital_trade_payables_increase_with_inventory_volume",
    "what_changed": "MD&A says the operating cash decrease was partly offset by an increase in trade accounts payable. It describes that increase as aligned with the increasing volume of inventories.",
    "account": "trade accounts payable",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "partially offset by an increase in trade account payables aligned with the increasing volume of inventories",
    "paragraph_id": "0001408710-26-000016:mdna:129",
    "explanation": false
  },
{
    "id": "liquidity_and_capital_operating_cash_flow_decrease_on_working_capital",
    "what_changed": "MD&A states that cash provided by operating activities for the first nine months of fiscal 2026 decreased compared with the first nine months of fiscal 2025. It puts the decrease down to working capital (inventories and receivables), not earnings. Customer advance payments, which appear in the contract liability roll-forward, are not among the causes it names.",
    "account": "net cash provided by operating activities",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The decrease in cash provided by operating activities during the nine months ended March 27, 2026 as compared to the nine months ended March 28, 2025 was primarily due to",
    "paragraph_id": "0001408710-26-000016:mdna:129",
    "explanation": false
  },
{
    "id": "liquidity_and_capital_investing_outflow_lower_on_short_term_investment_proceeds",
    "what_changed": "MD&A says cash used in investing for the first nine months of fiscal 2026 decreased, primarily because of an increase in net proceeds of short-term investments. This implies short-term investments were drawn on to fund the period.",
    "account": "short-term investments",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "was primarily due to an increase in net proceeds of short-term investments",
    "paragraph_id": "0001408710-26-000016:mdna:131",
    "explanation": false
  },
{
    "id": "liquidity_and_capital_capital_expenditure_for_new_building_and_certain_customers",
    "what_changed": "MD&A says capital expenditures increased for construction of the new Chonburi manufacturing building and to support certain customers. The customers are not named.",
    "account": "property, plant and equipment",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "offset by an increase in capital expenditures related to the construction of a new manufacturing building at our Chonburi campus and support certain customers",
    "paragraph_id": "0001408710-26-000016:mdna:131",
    "explanation": false
  },
{
    "id": "liquidity_and_capital_financing_outflow_lower_on_fewer_share_repurchases",
    "what_changed": "MD&A says cash used in financing decreased, primarily due to a decrease in share repurchases. This was partly offset by an increase in withholding tax on net share settlement of restricted share units. The share-based compensation note gives the withholding cash remitted as $24.4 million for the first nine months of fiscal 2026 and $20.9 million for the same period of fiscal 2025.",
    "account": "net cash used in financing activities",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "primarily due to a decrease in share repurchases, offset by an increase in withholding tax related to net share settlement of restricted share units",
    "paragraph_id": "0001408710-26-000016:mdna:133",
    "explanation": false
  },
{
    "id": "liquidity_and_capital_share_repurchase_totals_and_remaining_authorization",
    "what_changed": "The equity note states that 13,766 shares were repurchased in the first nine months of fiscal 2026, at an average price of $379.99 and $5.2 million in total. It states $169.0 million of authorization remained at March 27, 2026. It does not say whether any shares were bought in the third quarter itself.",
    "account": "treasury shares",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "During the nine months ended March 27, 2026, 13,766 shares were repurchased under the program, at an average price per share (excluding other direct costs) of $379.99, for an aggregate purchase price of $5.2 million.",
    "paragraph_id": "0001408710-26-000016:notes:136",
    "explanation": false
  },
{
    "id": "liquidity_and_capital_cash_and_short_term_investments_with_no_debt",
    "what_changed": "MD&A states cash, cash equivalents and short-term investments of $945.2 million at March 27, 2026 and $950.7 million at March 28, 2025, and no outstanding debt. The comparison date is the prior-year quarter end, not the fiscal year end used in the balance sheet notes.",
    "account": "cash, cash equivalents and short-term investments",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "As of March 27, 2026 and March 28, 2025, we had cash, cash equivalents, and short-term investments of $945.2 million and $950.7 million, respectively, and no outstanding debt.",
    "paragraph_id": "0001408710-26-000016:mdna:122",
    "explanation": false
  },
{
    "id": "liquidity_and_capital_manufacturing_capacity_and_chonburi_building_statement",
    "what_changed": "insufficient: the paragraph is marked as changed, but the bundle has no prior MD&A text, so the exact change cannot be identified. As it now reads, it says three things. Liquidity, including funds available through the credit facility, is sufficient for at least the next 12 months. Manufacturing capacity is sufficient 'for at least the next few quarters'. Construction of a building of approximately 2.0 million square feet at Chonburi began in February 2025, with an expected total cost of approximately $132.5 million (4.45 billion Thai baht).",
    "account": "property, plant and equipment",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "We also believe that our current manufacturing capacity is sufficient to meet our anticipated production requirements for at least the next few quarters.",
    "paragraph_id": "0001408710-26-000016:mdna:125",
    "explanation": false,
    "insufficient": true
  },
{
    "id": "liquidity_and_capital_interest_income_lower_on_cash_balance_and_rates",
    "what_changed": "MD&A states that interest income for the third quarter of fiscal 2026 decreased. It attributes this to a decrease in the average cash and short-term investment balance and a decrease in the weighted-average interest rate. The same causes are given for the nine months. The liquidity section gives weighted-average rates on cash and cash equivalents of 3.6% and 3.8% for the three and nine months, and 4.1% and 4.3% a year earlier.",
    "account": "interest income",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The decrease was primarily due to a decrease in average cash balance and short-term investment and a decrease of weighted average interest income rate during the three months ended March 27, 2026 compared to the same period in the prior fiscal year.",
    "paragraph_id": "0001408710-26-000016:mdna:103",
    "explanation": false
  },
{
    "id": "earnings_quality_foreign_exchange_gain_from_baht_revaluation",
    "what_changed": "MD&A explains a net foreign exchange gain of $7.0 million for the third quarter of fiscal 2026, against a net loss of $2.7 million a year earlier. The main contributors are unrealized revaluation gains on Thai baht assets and liabilities ($12.7 million) and on other currencies ($2.4 million). These are partly offset by an unrealized mark-to-market loss on forward contracts ($5.9 million) and a realized loss of $0.4 million. The nine-month paragraph gives the same causes. The gain comes from unrealized currency revaluation, not from operations.",
    "account": "foreign exchange gain (loss), net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The foreign exchange gain was mainly due to (1) unrealized gain from revaluation of outstanding Thai baht assets and liabilities of $12.7 million",
    "paragraph_id": "0001408710-26-000016:mdna:106",
    "explanation": false
  },
{
    "id": "earnings_quality_undesignated_forward_contract_unrealized_loss",
    "what_changed": "The derivatives note states unrealized losses of $4.2 million for the quarter and $4.3 million for the nine months on a forward contract not designated for hedge accounting. They are recorded in foreign exchange gain (loss), net. The prior-year comparatives are stated as gains of $1.6 million and $0.6 million. The MD&A market-risk paragraphs repeat the same figures.",
    "account": "foreign exchange gain (loss), net",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "During the three and nine months ended March 27, 2026, the Company included an unrealized loss of $4.2 million and $4.3 million, respectively, from changes in the fair value of a foreign currency forward contract that was not designated for hedge accounting",
    "paragraph_id": "0001408710-26-000016:notes:65",
    "explanation": false
  },
{
    "id": "across_documents_forward_contract_mark_to_market_loss_in_notes_and_mdna",
    "what_changed": "Two different loss figures for forward contracts are given, with no bridge between them. The MD&A results discussion cites an 'unrealized loss from mark-to-market forward contracts' of $5.9 million for the quarter and $5.0 million for the nine months. The derivatives note and the MD&A market-risk paragraphs state the unrealized loss on the undesignated contract as $4.2 million and $4.3 million. Neither text says which contracts each figure covers. The supervisor should reconcile them.",
    "account": "foreign exchange gain (loss), net",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "offset by (1) unrealized loss from mark-to-market forward contracts of $5.9 million",
    "paragraph_id": "0001408710-26-000016:mdna:106",
    "explanation": false
  },
{
    "id": "earnings_quality_hedge_loss_in_accumulated_other_comprehensive_income_to_reclassify",
    "what_changed": "The derivatives note states that a loss of $8.9 million in accumulated other comprehensive income is expected to be reclassified into earnings within 12 months. The reclassification table sends such amounts to cost of revenues, SG&A and foreign exchange gain (loss), net. The hedges are described as highly effective under regression testing.",
    "account": "net income (hedge losses reclassified from accumulated other comprehensive income)",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "expected to be reclassified into earnings within 12 months was a loss of $8.9 million",
    "paragraph_id": "0001408710-26-000016:notes:63",
    "explanation": false
  },
{
    "id": "earnings_quality_thai_baht_forward_contracts_outstanding_and_maturities",
    "what_changed": "The derivatives note states 253 outstanding U.S. dollar forward contracts against Thai baht, with a notional amount of $253.0 million and maturities from April 2026 through October 2026. It also states one Canadian dollar contract of 0.4 million Canadian dollars maturing in June 2026. The MD&A market-risk paragraph gives the same $253.0 million against Thai baht payables. At March 27, 2026 the fair value table carries derivative liabilities and no derivative assets row.",
    "account": "derivative liabilities",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "with an aggregate notional amount of $253.0 million and maturity dates ranging from April 2026 through October 2026",
    "paragraph_id": "0001408710-26-000016:notes:61",
    "explanation": false
  },
{
    "id": "structure_and_disclosure_changes_hedging_program_paragraph_rewritten",
    "what_changed": "insufficient: this single paragraph takes the place of two prior-quarter paragraphs (the note's paragraph count closes up by one here), and the prior text is not in the bundle. It now says the Company uses forward and option contracts to hedge forecasted transactions in Thai baht and Canadian dollars, with counterparties that meet its minimum credit standard. Whether option contracts or Canadian dollar hedging are new cannot be confirmed.",
    "account": "derivatives",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The Company enters into foreign currency forward and option contracts to hedge fluctuations in the U.S. dollar value of forecasted transactions denominated in Thai baht and Canadian dollars",
    "paragraph_id": "0001408710-26-000016:notes:58",
    "explanation": false,
    "insufficient": true
  },
{
    "id": "earnings_quality_other_comprehensive_loss_from_hedges_and_securities",
    "what_changed": "MD&A states an other comprehensive loss of $14.9 million for the third quarter of fiscal 2026, against other comprehensive income of $6.2 million a year earlier. It attributes this mainly to mark-to-market losses on forward contracts ($13.7 million) and on available-for-sale debt securities ($6.3 million), plus a translation loss ($1.1 million).",
    "account": "accumulated other comprehensive income",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The change was mainly due to (1) unrealized loss from mark-to-market of forward contracts of $13.7 million, (2) unrealized loss from mark-to-market of available-for-sale debt securities of $6.3 million",
    "paragraph_id": "0001408710-26-000016:mdna:118",
    "explanation": false
  },
{
    "id": "across_documents_other_comprehensive_loss_attribution_against_aoci_table",
    "what_changed": "MD&A attributes the nine-month change in other comprehensive income mainly to unrealized losses of $11.0 million on available-for-sale debt securities and $10.3 million on forward contracts. The note table on accumulated other comprehensive income gives these nine-month figures, in thousands: (1,325) for the current year and 9,647 a year earlier on available-for-sale securities; (9,382) and 907 on derivatives. The MD&A sentence speaks of 'the change' and does not say whether its figures are period amounts or year-over-year differences. The figures are set out for the supervisor to reconcile.",
    "account": "accumulated other comprehensive income",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "unrealized loss from mark-to-market of available-for-sale debt securities of $11.0 million",
    "paragraph_id": "0001408710-26-000016:mdna:119",
    "explanation": false
  },
{
    "id": "estimates_and_discretion_effective_tax_rate_quarter_rise_on_income_subject_to_tax",
    "what_changed": "The tax note and MD&A give an effective tax rate of 6.7% for the third quarter of fiscal 2026 and 5.8% for the third quarter of fiscal 2025. They explain the increase as 'an increase in income subject to tax' and name no jurisdiction or entity.",
    "account": "effective tax rate (income tax expense)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The effective tax rate for the Company for the three months ended March 27, 2026 and March 28, 2025 was 6.7% and 5.8%, respectively, of net income. The increase was due to an increase in income subject to tax.",
    "paragraph_id": "0001408710-26-000016:notes:97",
    "explanation": false
  },
{
    "id": "estimates_and_discretion_effective_tax_rate_nine_month_decline_on_income_not_subject_to_tax",
    "what_changed": "For the first nine months of fiscal 2026 the tax note and MD&A give an effective rate of 6.1%, and 6.3% a year earlier. They explain the decrease as 'an increase in income not subject to tax'. The quarter and the year to date thus carry opposite explanations in adjacent paragraphs.",
    "account": "effective tax rate (income tax expense)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The effective tax rate for the Company for the nine months ended March 27, 2026 and March 28, 2025 was 6.1% and 6.3%, respectively, of net income. The decrease was due to an increase in income not subject to tax.",
    "paragraph_id": "0001408710-26-000016:notes:98",
    "explanation": false
  },
{
    "id": "estimates_and_discretion_uncertain_tax_position_liability_without_stated_cause",
    "what_changed": "The tax note states the liability for uncertain tax positions, including accrued interest and penalties, as $4.4 million at March 27, 2026 and $2.2 million at June 27, 2025. It gives no reason for the amount. It does not say whether the liability relates to the IRS examination described in the next paragraph.",
    "account": "liability for uncertain tax positions",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "As of March 27, 2026 and June 27, 2025, the liability for uncertain tax positions including accrued interest and penalties was $4.4 million and $2.2 million, respectively.",
    "paragraph_id": "0001408710-26-000016:notes:95",
    "explanation": false
  },
{
    "id": "related_parties_contingencies_and_subsequent_events_irs_examination_status_wording",
    "what_changed": "insufficient: the prior wording is not in the bundle, so whether this paragraph is new cannot be told. It says the Company 'is currently under examination' by the IRS for fiscal year 2022. The next sentence says the IRS completed its examination of the U.S. subsidiaries for fiscal 2022 and fiscal 2023 during fiscal 2025. The two statements read against each other unless they concern different entities, and the text does not say so. Open tax years are given as 2018 to 2024.",
    "account": "income taxes payable; liability for uncertain tax positions",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "for fiscal year 2022. In fiscal year 2025, the IRS completed its examination",
    "paragraph_id": "0001408710-26-000016:notes:96",
    "explanation": false,
    "insufficient": true
  },
{
    "id": "earnings_quality_severance_recorded_in_selling_general_and_administrative",
    "what_changed": "MD&A names an increase in severance expense of $0.6 million as the first cause of the SG&A increase in the third quarter of fiscal 2026. The same section says there were no restructuring costs in the three or nine months, so severance is reported in SG&A rather than on the restructuring line. The nine-month paragraph cites a severance increase of $0.3 million.",
    "account": "selling, general and administrative expenses",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase was primarily due to (1) an increase in severance expenses of $0.6 million",
    "paragraph_id": "0001408710-26-000016:mdna:95",
    "explanation": false
  },
{
    "id": "estimates_and_discretion_allowance_for_expected_credit_losses_net_increase",
    "what_changed": "MD&A lists a net increase of $0.2 million in the allowance for expected credit losses among the causes of the nine-month SG&A increase. It cites the allowance as a cause of SG&A and gives no reason for the allowance increase itself. No customer is named.",
    "account": "allowance for expected credit losses",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "a net increase in the allowance for expected credit losses of $0.2 million",
    "paragraph_id": "0001408710-26-000016:mdna:96",
    "explanation": false
  },
{
    "id": "results_against_expectations_quarter_revenue_growth_on_key_customer_demand",
    "what_changed": "MD&A states revenue of $1,214.3 million for the third quarter of fiscal 2026, an increase of $342.5 million or 39.3% on the third quarter of fiscal 2025. It credits key customers' demand for both optical and non-optical products. Within optical, it credits telecom and datacenter interconnect products.",
    "account": "revenues",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Our revenues increased by $342.5 million, or 39.3%, to $1,214.3 million for the three months ended March 27, 2026",
    "paragraph_id": "0001408710-26-000016:mdna:86",
    "explanation": false
  },
{
    "id": "narrative_signs_of_operating_pressure_automotive_revenue_decrease_in_quarter",
    "what_changed": "MD&A says the quarter's non-optical growth was partly offset by a decrease in automotive revenue. No cause is given.",
    "account": "revenues (automotive)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "primarily due to high demand for high-performance computing, and partially offset with a decrease in revenue from automotive",
    "paragraph_id": "0001408710-26-000016:mdna:86",
    "explanation": false
  },
{
    "id": "narrative_signs_of_operating_pressure_datacom_revenue_decrease_over_nine_months",
    "what_changed": "For the first nine months of fiscal 2026, MD&A says optical growth was partly offset by a decrease in revenue from data communication products. No cause is given, and the three-month paragraph does not mention datacom.",
    "account": "revenues (datacom)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "partially offset with a decrease in revenues from data communication products during the nine months ended March 27, 2026",
    "paragraph_id": "0001408710-26-000016:mdna:87",
    "explanation": false
  },
{
    "id": "revenue_recognition_high_performance_computing_demand_driving_non_optical_growth",
    "what_changed": "MD&A attributes non-optical revenue growth, for both the quarter and the nine months, primarily to high demand for high-performance computing. The product revenue tables print a high-performance computing row for the fiscal 2026 periods and none for the prior-year periods.",
    "account": "revenues (high-performance computing)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "increased by $278.2 million, or 48.0%, compared to the same period in the prior fiscal year, primarily due to high demand for high-performance computing",
    "paragraph_id": "0001408710-26-000016:mdna:87",
    "explanation": false
  },
{
    "id": "revenue_recognition_bill_to_mix_shift_toward_united_states_customers",
    "what_changed": "MD&A says the share of revenue billed outside North America decreased from 53.8% to 47.9% for the quarter, and from 56.8% to 52.3% for the nine months. In both cases it cites an increase in revenue from customers in the United States. It expects the outside-North-America share for the rest of fiscal 2026 to be in line with the nine-month share.",
    "account": "revenues (United States bill-to customers)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "decreased from 53.8% in the three months ended March 28, 2025 to 47.9% in the three months ended March 27, 2026, primarily because of an increase in revenue from customers in the United States",
    "paragraph_id": "0001408710-26-000016:mdna:29",
    "explanation": false
  },
{
    "id": "revenue_recognition_contract_liability_rollforward_with_customer_advances",
    "what_changed": "The contract liability roll-forward now covers nine months and adds a prior-year comparative column. The prior quarter's table covered only the six months to December 26, 2025, with no comparative. For the first nine months of fiscal 2026 it shows advance payments received of 72,650 thousand dollars and an ending balance of 58,827 thousand dollars. No prose discusses these customer advances, and the MD&A operating cash flow explanation does not mention them.",
    "account": "contract liabilities",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Advance payments received during the period | 72,650",
    "paragraph_id": "0001408710-26-000016:notes:28",
    "explanation": false
  },
{
    "id": "revenue_recognition_reduction_to_revenue_with_prior_year_comparatives",
    "what_changed": "The reduction-to-revenue sentences now carry prior-year comparatives. They give $2.0 million for the third quarter of fiscal 2026 and $3.9 million a year earlier, and $3.2 million for the nine months and $3.9 million a year earlier. Both prior-year figures are stated as $3.9 million. The prior quarter's text gave $0.8 million for the second quarter and $1.1 million for the six months, with no comparatives.",
    "account": "revenues (contra revenue)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "For the three months ended March 27, 2026 and March 28, 2025, the Company recognized $2.0 million and $3.9 million, respectively, as a reduction to revenue",
    "paragraph_id": "0001408710-26-000016:notes:32",
    "explanation": false
  },
{
    "id": "revenue_recognition_customer_warrant_vested_unexercised_shares",
    "what_changed": "The text states that 70,662 warrant shares were vested and unexercised at March 27, 2026, and 38,192 at June 27, 2025. The earnings-per-share table carries a row of incremental shares from the customer warrant. The vesting terms are in unchanged paragraphs that the bundle does not carry.",
    "account": "diluted weighted-average shares",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "As of March 27, 2026 and June 27, 2025, 70,662 and 38,192 Warrant Shares, respectively, were vested and remained unexercised.",
    "paragraph_id": "0001408710-26-000016:notes:128",
    "explanation": false
  },
{
    "id": "revenue_recognition_customer_concentration_four_ten_percent_customers",
    "what_changed": "The segment note states that four customers each contributed 10% or more of revenue in the first nine months of fiscal 2026, against two a year earlier. Together they accounted for 58.1% of revenue, against 47.5% a year earlier. Three customers each held 10% or more of trade receivables at both March 27, 2026 and June 27, 2025.",
    "account": "revenues (customer concentration)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "the Company had four and two customers, respectively, that each contributed 10% or more",
    "paragraph_id": "0001408710-26-000016:notes:170",
    "explanation": false
  }
]
```

## Paragraphs carried as text that are not items

### Controls and procedures
- 0001408710-26-000016:item_4_controls:1 — heading
- 0001408710-26-000016:item_4_controls:2 — heading
- 0001408710-26-000016:item_4_controls:3 — standard effectiveness conclusion, carried verbatim; no change in substance shown
- 0001408710-26-000016:item_4_controls:4 — heading
- 0001408710-26-000016:item_4_controls:5 — date rolled forward; no change in internal control reported
- 0001408710-26-000016:item_4_controls:6 — page number

### MD&A
- 0001408710-26-000016:mdna:5 — date rolled forward; forward-looking bullet now refers to the nine months
- 0001408710-26-000016:mdna:23 — heading for the Raytek paragraph, covered by the Raytek cash outflow item
- 0001408710-26-000016:mdna:30 — nine-month version of mdna:29, covered by the bill-to mix item
- 0001408710-26-000016:mdna:31 — date rolled forward; same expectation, now based on nine months
- 0001408710-26-000016:mdna:33 — amounts only (geographic percentage table)
- 0001408710-26-000016:mdna:48 — amounts only (currency exposure table)
- 0001408710-26-000016:mdna:49 — amounts only; forward contract notional is the same as in the Thai baht forward contracts item
- 0001408710-26-000016:mdna:50 — date rolled forward
- 0001408710-26-000016:mdna:51 — date rolled forward
- 0001408710-26-000016:mdna:52 — same figures as the undesignated forward contract item
- 0001408710-26-000016:mdna:53 — same figures as the undesignated forward contract item
- 0001408710-26-000016:mdna:68 — date rolled forward (statutory tax rates)
- 0001408710-26-000016:mdna:75 — amounts only (statement of operations table)
- 0001408710-26-000016:mdna:77 — amounts only (percentage-of-revenue table)
- 0001408710-26-000016:mdna:80 — amounts only (product revenue table; rows reordered)
- 0001408710-26-000016:mdna:81 — amounts only (prior-year product revenue table)
- 0001408710-26-000016:mdna:84 — heading; date rolled forward
- 0001408710-26-000016:mdna:89 — amounts only; cause stays "in line with sales volume"
- 0001408710-26-000016:mdna:90 — amounts only; same cause
- 0001408710-26-000016:mdna:92 — amounts only; cause stays sales volume
- 0001408710-26-000016:mdna:93 — amounts only; same cause
- 0001408710-26-000016:mdna:97 — heading
- 0001408710-26-000016:mdna:98 — date rolled forward; no restructuring costs (cited in the severance item)
- 0001408710-26-000016:mdna:100 — amounts only; cause stays revenue growth
- 0001408710-26-000016:mdna:101 — amounts only; same cause
- 0001408710-26-000016:mdna:104 — nine-month version, covered by the interest income item
- 0001408710-26-000016:mdna:107 — nine-month version, covered by the foreign exchange gain item and the across-documents forward loss item
- 0001408710-26-000016:mdna:109 — amounts only
- 0001408710-26-000016:mdna:110 — amounts only
- 0001408710-26-000016:mdna:112 — same text as notes:97, covered by the quarterly effective tax rate item
- 0001408710-26-000016:mdna:113 — same text as notes:98, covered by the nine-month effective tax rate item
- 0001408710-26-000016:mdna:115 — amounts only
- 0001408710-26-000016:mdna:116 — amounts only
- 0001408710-26-000016:mdna:123 — amounts only; rates cited in the interest income item
- 0001408710-26-000016:mdna:127 — amounts only (cash flow summary table)

### Notes
- 0001408710-26-000016:notes:2 — date rolled forward
- 0001408710-26-000016:notes:4 — date rolled forward
- 0001408710-26-000016:notes:8 — date rolled forward; adds the nine-month week count
- 0001408710-26-000016:notes:10 — pending income tax disclosure standard; no change in substance can be identified and no effect on amounts is stated
- 0001408710-26-000016:notes:11 — pending expense disaggregation standard; no change in substance can be identified and no effect on amounts is stated
- 0001408710-26-000016:notes:15 — amounts only (geographic revenue table; Germany and Finland rows reordered)
- 0001408710-26-000016:notes:16 — amounts only (prior-year geographic revenue table)
- 0001408710-26-000016:notes:19 — amounts only (product revenue table)
- 0001408710-26-000016:notes:20 — amounts only (prior-year product revenue table)
- 0001408710-26-000016:notes:25 — date rolled forward (contract assets de minimis)
- 0001408710-26-000016:notes:27 — lead-in reworded, covered by the contract liability roll-forward item
- 0001408710-26-000016:notes:33 — nine-month version, covered by the reduction-to-revenue item
- 0001408710-26-000016:notes:36 — amounts only (earnings per share table)
- 0001408710-26-000016:notes:39 — amounts only (cash and investments table)
- 0001408710-26-000016:notes:41 — date rolled forward
- 0001408710-26-000016:notes:42 — amounts only (maturity table)
- 0001408710-26-000016:notes:49 — amounts only (fair value table)
- 0001408710-26-000016:notes:50 — amounts only (fiscal-year-end fair value table)
- 0001408710-26-000016:notes:51 — amounts only; notional cited in the Thai baht forward contracts item
- 0001408710-26-000016:notes:52 — fiscal-year-end comparative footnote; amounts only
- 0001408710-26-000016:notes:53 — fiscal-year-end comparative footnote; amounts only
- 0001408710-26-000016:notes:62 — fiscal-year-end comparative of forward contracts; no change in substance
- 0001408710-26-000016:notes:66 — prior-year comparative, covered by the undesignated forward contract item
- 0001408710-26-000016:notes:68 — amounts only (derivative gains and losses table)
- 0001408710-26-000016:notes:69 — heading
- 0001408710-26-000016:notes:71 — amounts only (derivative fair value table)
- 0001408710-26-000016:notes:75 — amounts only (inventory components table)
- 0001408710-26-000016:notes:78 — date rolled forward
- 0001408710-26-000016:notes:79 — amounts only (lease maturity table)
- 0001408710-26-000016:notes:80 — amounts only
- 0001408710-26-000016:notes:82 — amounts only
- 0001408710-26-000016:notes:83 — date rolled forward
- 0001408710-26-000016:notes:85 — amounts only (lease term and discount rate)
- 0001408710-26-000016:notes:86 — date rolled forward
- 0001408710-26-000016:notes:87 — amounts only
- 0001408710-26-000016:notes:89 — amounts only (intangibles table)
- 0001408710-26-000016:notes:90 — amounts only
- 0001408710-26-000016:notes:92 — amounts only
- 0001408710-26-000016:notes:93 — date rolled forward
- 0001408710-26-000016:notes:94 — amounts only
- 0001408710-26-000016:notes:101 — date rolled forward
- 0001408710-26-000016:notes:102 — amounts only (share-based compensation table)
- 0001408710-26-000016:notes:104 — amounts only
- 0001408710-26-000016:notes:105 — date rolled forward
- 0001408710-26-000016:notes:110 — date rolled forward
- 0001408710-26-000016:notes:111 — amounts only
- 0001408710-26-000016:notes:117 — amounts only (restricted share unit activity)
- 0001408710-26-000016:notes:118 — amounts only (prior-year restricted share unit activity)
- 0001408710-26-000016:notes:120 — amounts only (performance share unit activity)
- 0001408710-26-000016:notes:121 — amounts only (prior-year performance share unit activity)
- 0001408710-26-000016:notes:122 — amounts only (unrecognized compensation)
- 0001408710-26-000016:notes:123 — amounts only; withholding cash cited in the financing outflow item
- 0001408710-26-000016:notes:131 — amounts only (shares issued on vesting)
- 0001408710-26-000016:notes:132 — amounts only (prior-year shares issued on vesting)
- 0001408710-26-000016:notes:137 — date rolled forward
- 0001408710-26-000016:notes:138 — amounts only; cited in the across-documents other comprehensive loss item
- 0001408710-26-000016:notes:139 — amounts only (prior-year table)
- 0001408710-26-000016:notes:140 — heading; unchanged according to the note change history
- 0001408710-26-000016:notes:141 — reworded; the baht and renminbi guarantee amounts match the prior text, with the dollar equivalent restated
- 0001408710-26-000016:notes:142 — heading; unchanged according to the note change history
- 0001408710-26-000016:notes:143 — unchanged according to the note change history
- 0001408710-26-000016:notes:145 — heading; unchanged according to the note change history
- 0001408710-26-000016:notes:146 — unchanged according to the note change history
- 0001408710-26-000016:notes:148 — heading; unchanged according to the note change history
- 0001408710-26-000016:notes:149 — unchanged according to the note change history
- 0001408710-26-000016:notes:150 — unchanged according to the note change history
- 0001408710-26-000016:notes:151 — date rolled forward (nothing drawn on the credit facility)
- 0001408710-26-000016:notes:152 — unchanged according to the note change history
- 0001408710-26-000016:notes:153 — date rolled forward (covenant compliance)
- 0001408710-26-000016:notes:154 — new heading, covered by the tariff refund item
- 0001408710-26-000016:notes:156 — heading; unchanged according to the note change history
- 0001408710-26-000016:notes:157 — unchanged according to the note change history
- 0001408710-26-000016:notes:158 — unchanged according to the note change history
- 0001408710-26-000016:notes:160 — date rolled forward (no restructuring liability)
- 0001408710-26-000016:notes:164 — amounts only (segment results table)
- 0001408710-26-000016:notes:167 — amounts only (long-lived assets by country)
- 0001408710-26-000016:notes:169 — date rolled forward; cited in the customer concentration item

### Current reports
- input_8k listing — item codes only, no body carried; covered by the first item (insufficient)
