<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# report_notes_text — WDC 10-Q, quarter ended April 3, 2026 (0001628280-26-029054)

Prior period compared: 0001628280-26-004207 (quarter ended January 2, 2026).

## Input check

- The directory holds only the six permitted files. There is no trend table, price, abnormal return, short-interest figure, other company's file, prior probability or outcome window. The MD&A tables are the filing's own text.
- **Not in the input:**
  - No auditor's report (this is a 10-Q bundle).
  - No Item 1A diff.
  - No Exhibit 21 diff.
  - No Exhibit 10.
- **8-K:** the file has the item-code index only, with no verbatim bodies and no paragraph ids, so no 8-K text can be quoted. Where the index bears on an item (the preferred conversion), the item says so.
- **Prior predictions:** none on record.
- **How "insufficient" is marked:**
  - An item whose `what_changed` begins with "insufficient:" is a paragraph carried as changed text where the prior wording is not in the input.
  - A line in the paragraph list below that begins with "insufficient:" has the same meaning.

## Items

```json
[
  {
    "id": "liquidity_and_capital_senior_notes_redeemed_with_bridge_loan",
    "what_changed": "New paragraph. In February 2026 the company entered a $1.50 billion Bridge Loan. It used the loan to consolidate the holders of the 4.75% notes due 2026, the 2.85% notes due 2029 and the 3.10% notes due 2032 into two holders, then used the proceeds to redeem all of those Senior Notes in cash at par plus accrued interest. Two prior-period sentences are removed: the stated intent to redeem or repay the 4.75% notes on or before February 15, 2026 (0001628280-26-004207:note_history:21), and the Term Loan A-3 interest rate (0001628280-26-004207:note_history:22). The debt table (notes:69) now lists only the 2028 Convertible Notes.",
    "account": "Total debt (Senior Notes)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The proceeds of the Bridge Loan were used to fully redeem all of the Senior Notes in cash, at par plus accrued interest.",
    "paragraph_id": "0001628280-26-029054:notes:70",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_bridge_loan_and_term_loan_retired_through_sandisk_share_exchange",
    "what_changed": "New: the Bridge Loan and the remaining Term Loan A-3 were retired in a non-cash, tax-free exchange for 5.8 million Sandisk shares held by the company, valued at $3.62 billion on the exchange date. The asset given up is part of the retained Sandisk stake. The prose calls the exchange non-cash. The same sequence is summarized in notes:32 and mdna:9.",
    "account": "Total debt (Bridge Loan, Term Loan A-3); Retained interest in Sandisk",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Following the redemptions, the Company retired the Bridge Loan and its existing Term Loan A-3 through a non-cash, tax-free exchange for 5.8 million shares of Sandisk common stock held by the Company, valued at $3.62 billion on the date of exchange.",
    "paragraph_id": "0001628280-26-029054:notes:70",
    "explanation": false
  },
  {
    "id": "earnings_quality_debt_for_equity_exchange_discount_charge",
    "what_changed": "New charge and new caption. The note says the exchange resulted in $539 million recorded in Costs in connection with debt-for-equity exchange. It says the amount mainly reflects a discount on Sandisk shares given to the counterparties, and that the discount was needed mainly because the Sandisk stock price was volatile during the exchange. The same caption appears as a new line in the segment table (notes:24) and in both MD&A income statement tables (mdna:20, mdna:23). The prose does not say whether the planned exchanges of the remaining Sandisk shares (notes:32) will also carry a discount.",
    "account": "Costs in connection with debt-for-equity exchange",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The exchange resulted in $539 million recorded in Costs in connection with debt-for-equity exchange in the Condensed Consolidated Statement of Operations. This amount primarily reflects a discount on Sandisk shares provided to the counterparties in connection with the exchange.",
    "paragraph_id": "0001628280-26-029054:notes:70",
    "explanation": false
  },
  {
    "id": "earnings_quality_unamortized_issuance_costs_written_off_on_redemption",
    "what_changed": "New sentence: the company wrote off $6 million of remaining unamortized issuance costs on the Senior Notes redemptions. The prose does not name the income statement line where this was recorded.",
    "account": "Debt issuance costs written off (income statement line not named)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "In connection with the redemptions, the Company wrote off $6 million of remaining unamortized issuance costs.",
    "paragraph_id": "0001628280-26-029054:notes:70",
    "explanation": false
  },
  {
    "id": "across_documents_debt_exchange_cost_amount_note_and_discussion",
    "what_changed": "The two documents give different dollar figures for what each presents as the exchange cost. The note (notes:70) says the exchange resulted in $539 million recorded in Costs in connection with debt-for-equity exchange. The MD&A says $545 million of costs were incurred in connection with the exchange and describes that amount as reflecting the discount on the Sandisk shares. This reader does not reconcile the two; that is for the numbers reader and the supervisor.",
    "account": "Costs in connection with debt-for-equity exchange",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "These changes were partially offset by $545 million of costs incurred in connection with our debt-for-equity exchange, which reflects the discount provided on the monetization of Sandisk shares.",
    "paragraph_id": "0001628280-26-029054:mdna:46",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_remaining_sandisk_shares_to_be_exchanged_for_common_stock",
    "what_changed": "New: at April 3, 2026 the company still holds 1.7 million Sandisk shares. It expects to monetize them by the end of 2026 in one or more exchanges for its own outstanding common stock. The earlier monetizations described in the same paragraph retired debt; this one is described as an exchange for the company's own shares. The same statement appears in mdna:9.",
    "account": "Retained interest in Sandisk; common shares outstanding (treasury stock)",
    "expected_direction": "down",
    "horizon": "next quarter (prose: by the end of 2026, using the company's fiscal-year labels)",
    "quote": "As of April 3, 2026, the Company still held 1.7 million shares of Sandisk common stock, which it expects to monetize by the end of 2026 in one or more subsequent exchanges for its outstanding common stock.",
    "paragraph_id": "0001628280-26-029054:notes:32",
    "explanation": false
  },
  {
    "id": "earnings_quality_sandisk_mark_to_market_gain_in_pretax_income",
    "what_changed": "MD&A mainly attributes the quarter's change in total interest and other income to a $2.73 billion gain on the retained Sandisk interest, based on mark-to-market value at April 3, 2026. For nine months it cites a gain of $4.45 billion that it calls unrealized, although the notes describe 5.8 million Sandisk shares exchanged in February (notes:70). The tax note says the gain is tax-free (notes:98). This income is non-operating, and the remaining stake is slated for exchange (notes:32). The prose gives no direction for future mark-to-market results.",
    "account": "Gain (loss) on retained interest in Sandisk",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "The change reflects a gain of $2.73 billion on our retained interest in Sandisk in the current period based on the mark-to-market value as of April 3, 2026, compared to a loss of $606 million in the prior year",
    "paragraph_id": "0001628280-26-029054:mdna:46",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_interest_expense_lower_with_debt_reduction",
    "what_changed": "MD&A cites lower interest expense of $53 million for the quarter and attributes it to the reduction in debt. The Senior Notes, Bridge Loan and Term Loan A-3 were retired in February (notes:70), and the debt table now lists only the 2028 Convertible Notes. The prose therefore implies the lower interest charge continues into the next quarter.",
    "account": "Interest expense",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "lower interest expense of $53 million, which reflects the reduction in our debt",
    "paragraph_id": "0001628280-26-029054:mdna:46",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_convertible_notes_tendered_with_cash_settlement_election",
    "what_changed": "New. The sale-price conversion condition was met again in the calendar quarter ended March 31, 2026, so holders may convert through June 30, 2026. During the quarter, holders tendered $32 million principal of the 2028 Convertible Notes. For those notes the company irrevocably elected to settle in cash the part of the conversion obligation above principal, with settlement scheduled for June 2026. The standing terms (notes:74) already require cash for principal on any conversion. The same matter appears in mdna:87 and mdna:88.",
    "account": "Current portion of long-term debt (2028 Convertible Notes); cash",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "The Company made an irrevocable election to settle in cash the conversion obligation in excess of the principal amount of the Tendered Notes, as permitted by the Indenture.",
    "paragraph_id": "0001628280-26-029054:notes:75",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_conversion_feature_bifurcated_as_derivative",
    "what_changed": "New accounting. Because of the cash-settlement election, the embedded conversion feature of the Tendered Notes must be bifurcated and accounted for as a derivative under ASC 815. It is remeasured to fair value each period, with changes recognized in Other income (expense), net. The note reports an immaterial gain for the quarter. The derivative remains until the June 2026 settlement.",
    "account": "Other income (expense), net; derivative for the Tendered Notes conversion feature",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "This election requires bifurcation and separate accounting of the embedded conversion feature as a derivative instrument pursuant to Accounting Standards Codification 815.",
    "paragraph_id": "0001628280-26-029054:notes:75",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_preferred_shares_mandatorily_converted_to_common",
    "what_changed": "New. On February 17, 2026 all remaining Preferred Shares were mandatorily converted into 7 million common shares. Immediately before conversion their aggregate liquidation preference was $267 million, including $32 million of dividends paid in kind. A Certificate of Elimination was filed on February 24, 2026. The preferred-stock paragraphs (notes:135, notes:136) now use the past tense, and mdna:11 and mdna:12 add a heading and summary. The 8-K index lists filings on 2026-02-18 (item 3.03) and 2026-02-24 (items 5.03, 8.01); no 8-K body is in the input.",
    "account": "Preferred stock; common shares outstanding",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "On February 17, 2026, the Company converted all remaining outstanding Preferred Shares into 7 million shares of the Company’s common stock pursuant to a mandatory conversion",
    "paragraph_id": "0001628280-26-029054:notes:137",
    "explanation": false
  },
  {
    "id": "earnings_quality_participating_securities_allocation_ends_after_conversion",
    "what_changed": "The EPS footnote now says the Preferred Shares were participating securities 'prior to their conversion'. Since they have been converted (notes:137), the prose implies three things stop: dividends allocated to preferred shareholders, income allocated to participating securities in the basic EPS numerator, and preferred cash dividends (notes:136).",
    "account": "Income attributable to participating securities; Dividends allocated to preferred shareholders",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "Participating securities consisted of Preferred Shares because, prior to their conversion, they participated on a pro rata basis in any dividends declared on shares of common stock.",
    "paragraph_id": "0001628280-26-029054:notes:146",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_additional_share_repurchase_authorization",
    "what_changed": "New: on February 2, 2026 the Board authorized repurchases of up to an additional $4.00 billion, with no expiration date. In the quarter the company repurchased 2.9 million shares for $752 million plus $5 million of accrued excise tax. At April 3, 2026, $3.93 billion remained available. The company says it expects repurchases to be funded principally by operating cash flows.",
    "account": "Treasury stock / common shares outstanding; cash",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "authorized the repurchase of up to an additional $4.00 billion of the Company's common stock",
    "paragraph_id": "0001628280-26-029054:notes:139",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_investment_grade_ratings_release_revolver_guarantees_and_collateral",
    "what_changed": "New sentence: during the quarter the company obtained investment grade ratings from two rating agencies. Under the Loan Agreement, that released the guarantees and collateral on the 2027 Revolving Credit Facility. The debt note's revolver paragraphs (notes:71, notes:72) do not mention the release. The prose says $1.25 billion remains available under the revolver and that it matures in January 2027.",
    "account": "2027 Revolving Credit Facility (guarantee and collateral terms)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "During the three months ended April 3, 2026, the Company obtained investment grade ratings from two rating agencies and therefore, pursuant to the terms of the Loan Agreement, the guarantees and collateral on the 2027 Revolving Credit Facility were released.",
    "paragraph_id": "0001628280-26-029054:mdna:89",
    "explanation": false
  },
  {
    "id": "across_documents_bridge_loan_cash_inflow_and_non_cash_retirement",
    "what_changed": "Nine-month financing activities now include $1.50 billion of net proceeds from a bridge loan and $1.56 billion of debt repayments. The note (notes:70), however, says the Bridge Loan and Term Loan A-3 were retired through a non-cash exchange of Sandisk shares. So the cash flow statement shows the bridge borrowing as a cash inflow while the note describes its retirement as non-cash. How the repayment line relates to the Senior Notes redemptions and the scheduled Term Loan A-3 repayments is for the numbers reader.",
    "account": "Net cash used in financing activities (bridge loan proceeds; repayments of debt)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "These uses were partially offset by $1.50 billion of net proceeds from a bridge loan and $32 million of proceeds from the issuance of stock under employee stock plans.",
    "paragraph_id": "0001628280-26-029054:mdna:69",
    "explanation": false
  },
  {
    "id": "results_against_expectations_revenue_growth_from_exabytes_and_pricing",
    "what_changed": "MD&A attributes the quarter's 45% net revenue increase to a 34% increase in exabytes sold and a 9% increase in average selling price per exabyte, both driven by strong demand across all end markets. For nine months it cites a 26% exabyte increase and a 5% price increase. The prior quarter's wording is not in the input.",
    "account": "Revenue, net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "driven by a 34% increase in exabytes sold and a 9% increase in average selling price per exabyte, both of which were driven by strong demand across all of our end markets",
    "paragraph_id": "0001628280-26-029054:mdna:31",
    "explanation": false
  },
  {
    "id": "results_against_expectations_cloud_improved_pricing_environment",
    "what_changed": "MD&A says Cloud revenue (89% of total) increased 48% for the quarter. It attributes the exabyte increase to demand for high-capacity enterprise products, and the increase in average selling price per exabyte to an improved pricing environment.",
    "account": "Revenue, net (Cloud)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase in average selling price per exabyte was due to an improved pricing environment.",
    "paragraph_id": "0001628280-26-029054:mdna:32",
    "explanation": false
  },
  {
    "id": "results_against_expectations_client_revenue_volume_and_price",
    "what_changed": "MD&A says Client revenue increased 31% for the quarter on a 19% exabyte increase and a 10% price-per-exabyte increase, driven by dynamics largely consistent with the other end markets. For nine months it cites a 4% exabyte increase and a 16% price increase.",
    "account": "Revenue, net (Client)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Client revenue, representing 5% of total revenue, increased by 31% for the three months ended April 3, 2026 from the comparable period in the prior year, driven by a 19% increase in exabytes sold and a 10% increase in average selling price per exabyte.",
    "paragraph_id": "0001628280-26-029054:mdna:33",
    "explanation": false
  },
  {
    "id": "results_against_expectations_consumer_revenue_volume_and_price",
    "what_changed": "MD&A says Consumer revenue increased 24% for the quarter on a 6% exabyte increase and a 17% price-per-exabyte increase, driven by dynamics largely consistent with the other end markets. For nine months it cites a 1% exabyte increase and a 4% price increase.",
    "account": "Revenue, net (Consumer)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Consumer revenue, representing 6% of total revenue, increased by 24% for the three months ended April 3, 2026 from the comparable period in the prior year, driven by a 6% increase in exabytes sold and a 17% increase in average selling price per exabyte.",
    "paragraph_id": "0001628280-26-029054:mdna:34",
    "explanation": false
  },
  {
    "id": "results_against_expectations_asia_and_emea_data_center_ramp",
    "what_changed": "MD&A says the change in geographic revenue mix for the three and nine months reflects larger percentage increases in Asia and in Europe, Middle East and Africa, as customers ramp up data center capacity there.",
    "account": "Revenue by geography (Asia; Europe, Middle East and Africa)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "reflects larger percentage increases in the Asia and Europe, Middle East and Africa regions as customers are ramping up data center capacity in these regions",
    "paragraph_id": "0001628280-26-029054:mdna:35",
    "explanation": false
  },
  {
    "id": "results_against_expectations_gross_margin_newer_products_and_pricing",
    "what_changed": "MD&A attributes the quarter's gross profit increase to higher shipment volume, a lower cost structure on newer-generation products and improved pricing. It attributes the 10 percentage point gross margin increase mainly to the cost structure and pricing. It says nine-month gross margin increased 9 percentage points for the same reasons.",
    "account": "Gross margin",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Gross margin increased by 10 percentage points year over year, primarily due to a lower cost structure on our newer generation products and improved pricing.",
    "paragraph_id": "0001628280-26-029054:mdna:38",
    "explanation": false
  },
  {
    "id": "results_against_expectations_research_and_development_compensation_and_roadmap",
    "what_changed": "MD&A attributes the quarter's $49 million R&D increase to $25 million of incremental product development costs for the technology and product roadmap, and $20 million of higher compensation-related costs tied to improved financial performance. For nine months it cites $95 million of compensation-related costs and $50 million of product development costs.",
    "account": "Research and development",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase was attributable to $25 million of incremental product development related costs as we continue to execute on our innovative technology and product roadmap along with $20 million higher compensation-related costs aligned with the improved financial performance during the current year.",
    "paragraph_id": "0001628280-26-029054:mdna:41",
    "explanation": false
  },
  {
    "id": "results_against_expectations_selling_general_administrative_performance_compensation",
    "what_changed": "MD&A attributes the quarter's $39 million SG&A increase mainly to higher compensation-related expense resulting from improved financial performance. It says the nine-month decrease reflects Separation planning and execution costs in the prior-year period, including duplicative personnel costs and higher outside service fees.",
    "account": "Selling, general and administrative",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase was primarily attributable to higher compensation-related expense, as a result of our improved financial performance.",
    "paragraph_id": "0001628280-26-029054:mdna:42",
    "explanation": false
  },
  {
    "id": "earnings_quality_receivables_increase_attributed_to_business_volume",
    "what_changed": "MD&A explains part of the cash used for operating assets and liabilities as a $504 million increase in accounts receivable, driven by growth in business volume. Setting this explanation against the receivables balances in notes:20 and the revenue figures is for the numbers reader.",
    "account": "Accounts receivable, net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "These were partially offset by a $504 million increase in accounts receivable driven by the growth in our business volume",
    "paragraph_id": "0001628280-26-029054:mdna:65",
    "explanation": true
  },
  {
    "id": "earnings_quality_inventory_reduction_attributed_to_shipments",
    "what_changed": "MD&A says the year-over-year improvement in working-capital cash use largely reflects a $365 million reduction in inventory resulting from increased shipments to customers. The inventory table (notes:36) is amounts only; whether the balance moved this way is for the numbers reader.",
    "account": "Inventories",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "a $365 million reduction in inventory as a result of increased shipments to customers",
    "paragraph_id": "0001628280-26-029054:mdna:65",
    "explanation": true
  },
  {
    "id": "earnings_quality_reduced_derivative_hedging_since_separation",
    "what_changed": "MD&A says a $345 million improvement from accrued expenses resulted from a significant reduction in derivative hedging activity since the Separation. The prose does not say how much foreign-currency exposure is now unhedged. The related AOCI and fair-value tables (notes:52, notes:62) are amounts only.",
    "account": "Foreign exchange derivative hedging activity (accrued expenses)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "a $345 million improvement from accrued expenses resulting from a significant reduction in our derivative hedging activities since the Separation",
    "paragraph_id": "0001628280-26-029054:mdna:65",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_income_tax_receivable_timing_in_operating_cash",
    "what_changed": "MD&A attributes an $883 million improvement in other assets and liabilities to the timing of recognition and realization of income taxes receivable. It says this was partly offset by a $518 million increase in cash used, driven by the timing of recognition and payment of income taxes.",
    "account": "Income taxes receivable; income taxes payable",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "a $883 million improvement in other assets and liabilities driven by the timing of recognition and realization of income taxes receivable",
    "paragraph_id": "0001628280-26-029054:mdna:65",
    "explanation": true
  },
  {
    "id": "liquidity_and_capital_variable_compensation_payment_timing",
    "what_changed": "MD&A attributes a $225 million improvement from accrued compensation to the amount and timing of variable compensation payments. MD&A also attributes R&D and SG&A increases to performance-linked compensation (mdna:41, mdna:42). Read together, the prose implies variable compensation accrued but not yet paid, with the payment falling in a later period's operating cash flow.",
    "account": "Accrued compensation",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "a $225 million improvement from accrued compensation resulting from amount and timing of payment of variable compensation",
    "paragraph_id": "0001628280-26-029054:mdna:65",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_capital_expenditure_range_of_net_revenue",
    "what_changed": "insufficient: the paragraph is carried as changed text, but the prior wording is not in the input. It now states, as a paragraph on its own, that capital expenditures are expected to be about 4% to 6% of net revenue.",
    "account": "Capital expenditures",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "We expect our capital expenditures generally to be approximately 4% to 6% of our net revenue.",
    "paragraph_id": "0001628280-26-029054:mdna:60",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_dividend_declared_after_quarter_end",
    "what_changed": "New subsequent event: on April 29, 2026 the Board declared a common dividend of $0.15 per share, payable June 17, 2026 to holders of record on June 5, 2026 (also in mdna:83). The dividend paid in the quarter is stated as $0.125 per share in notes:141; how the two rates relate is for the numbers reader.",
    "account": "Dividends paid (financing cash flow)",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "Subsequent to quarter-end, on April 29, 2026, the Board of Directors declared a cash dividend of $0.15 per share",
    "paragraph_id": "0001628280-26-029054:notes:142",
    "explanation": false
  },
  {
    "id": "earnings_quality_excess_windfall_tax_benefits",
    "what_changed": "insufficient: the prior wording is not in the input. The paragraph states excess windfall tax benefits of $47 million for the quarter and $76 million for nine months, recognized in income tax expense, and calls the prior-year amounts immaterial. These are discrete benefits that depend on award vesting and the share price.",
    "account": "Income tax expense (benefit)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "During the three and nine months ended April 3, 2026, excess windfall tax benefits were $47 million and $76 million, respectively.",
    "paragraph_id": "0001628280-26-029054:notes:123",
    "explanation": false
  },
  {
    "id": "earnings_quality_tax_rate_lowered_by_tax_free_sandisk_gain",
    "what_changed": "insufficient: the prior wording is not in the input, so which driver is newly named cannot be established. The note gives four drivers of the current-period effective tax rate: jurisdictional mix, the FDDEI deduction, tax credits, and the tax-free treatment of the gain on the retained Sandisk interest. The provision includes GMT for Malaysia, Thailand and the Philippines. The same text is in mdna:53. With the remaining Sandisk shares slated for exchange (notes:32), the prose implies the tax-free-gain driver falls away.",
    "account": "Effective tax rate (income tax expense)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "the gain on the retained interest in Sandisk being tax-free due to the Separation",
    "paragraph_id": "0001628280-26-029054:notes:98",
    "explanation": false
  },
  {
    "id": "earnings_quality_prior_year_one_time_deferred_tax_benefit",
    "what_changed": "The comparative period is now the quarter ended March 28, 2025. The tax note says that period's tax line included one-time deferred tax benefits of $711 million from an inter-entity asset transfer executed with the Separation (the same text is in mdna:54). Year-over-year comparisons of income tax and of net income from continuing operations therefore include this one-time item in the comparative period.",
    "account": "Income tax expense (benefit), comparative period",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "This resulted in the recognition of one-time deferred tax benefits to continuing operations of $711 million for the three and nine months ended March 28, 2025.",
    "paragraph_id": "0001628280-26-029054:notes:99",
    "explanation": false
  },
  {
    "id": "earnings_quality_prior_year_litigation_reversal_in_comparative",
    "what_changed": "The MRT paragraphs are added back (history 0001628280-26-029054:note_history:2 and :3). They describe the original $384 million liability and the April 2025 global settlement of $130 million. They state that the comparative three- and nine-month periods ended March 28, 2025 include reversals of $201 million and $198 million of previously recorded charges in Litigation matter. So comparative-period operating income includes a one-time litigation credit; the MD&A tables show a dash for Litigation matter in the current periods. notes:151 is the background to this paragraph.",
    "account": "Litigation matter (operating expenses), comparative period",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "As a result of the settlement, in the three- and nine-month periods ended March 28, 2025, the Company reversed $201 million and $198 million, respectively, of previously recorded charges in Operating expenses under Litigation matter.",
    "paragraph_id": "0001628280-26-029054:notes:152",
    "explanation": false
  },
  {
    "id": "revenue_recognition_customer_revenue_concentration",
    "what_changed": "The prose names three customers at 17%, 15% and 11% of revenue for the quarter, and three customers at 16%, 15% and 13% for nine months. For the prior-year nine months it names two customers, at 18% and 11%. It gives the top 10 customers as 71% and 74% of revenue for the current three and nine months. The same text is in notes:19.",
    "account": "Revenue, net (customer concentration)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "For the nine months ended April 3, 2026, three customers accounted for 16%, 15%, and 13%, respectively, of our net revenue, and for the nine months ended March 28, 2025, two customers accounted for 18% and 11%, respectively, of our net revenue.",
    "paragraph_id": "0001628280-26-029054:mdna:36",
    "explanation": false
  },
  {
    "id": "earnings_quality_receivables_customer_concentration",
    "what_changed": "The prose names two customers at 28% and 12% of net accounts receivable at April 3, 2026. For June 27, 2025 it names three customers, at 20%, 19% and 12%. It states net receivables of $1.89 billion and $1.49 billion at those dates, and still calls credit-loss reserves not material. One counterparty is now stated at 28% of net receivables.",
    "account": "Accounts receivable, net (customer concentration)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "As of April 3, 2026, two customers accounted for 28% and 12%, respectively, of the Company’s net accounts receivable",
    "paragraph_id": "0001628280-26-029054:notes:20",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_remaining_realignment_termination_costs",
    "what_changed": "insufficient: the prior wording is not in the input. The note says the company expects about $5 million of further employee termination costs from the realignment actions in the rest of 2026. The quarter's charges are in the table at notes:108 (amounts only).",
    "account": "Business realignment charges",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "As a result of the above actions, the Company expects to record incremental employee termination costs of approximately $5 million in the remainder of 2026.",
    "paragraph_id": "0001628280-26-029054:notes:109",
    "explanation": false
  },
  {
    "id": "earnings_quality_cash_flow_hedge_net_losses_to_reclassify",
    "what_changed": "insufficient: the prior wording is not in the input. The note describes the cash flow hedge amounts in AOCI as net losses, all expected to be reclassified to earnings within twelve months. notes:53 says the amounts reclassified this period were losses on foreign exchange contracts, charged substantially to Cost of revenue.",
    "account": "Cost of revenue (reclassification from accumulated other comprehensive income)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "As of April 3, 2026, all existing net losses related to cash flow hedges recorded in Accumulated other comprehensive income are expected to be reclassified to earnings within the next twelve months.",
    "paragraph_id": "0001628280-26-029054:notes:54",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_chief_executive_trading_plan",
    "what_changed": "New trading-plan disclosure: Chief Executive Officer Irving Tan adopted a Rule 10b5-1 plan on February 5, 2026 to sell up to 80,000 shares before it expires on May 31, 2027.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "plan window stated in the prose, to May 31, 2027",
    "quote": "Irving Tan, Chief Executive Officer of the Company, adopted a Rule 10b5-1 Plan on February 5, 2026.",
    "paragraph_id": "0001628280-26-029054:notes:157",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_director_trading_plan",
    "what_changed": "New trading-plan disclosure: director Martin I. Cole adopted a Rule 10b5-1 plan on March 5, 2026 to sell up to 12,000 shares before it expires on October 31, 2026.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "plan window stated in the prose, to October 31, 2026",
    "quote": "Martin I. Cole, a director of the Company, adopted a Rule 10b5-1 Plan on March 5, 2026.",
    "paragraph_id": "0001628280-26-029054:notes:156",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_chief_legal_officer_trading_plan",
    "what_changed": "New trading-plan disclosure: Executive Vice President, Chief Legal Officer and Secretary Cynthia Tregillis adopted a Rule 10b5-1 plan on March 6, 2026 to sell up to 27,765 shares before it expires on December 31, 2027.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "plan window stated in the prose, to December 31, 2027",
    "quote": "Cynthia Tregillis, Executive Vice President, Chief Legal Officer and Secretary of the Company, adopted a Rule 10b5-1 Plan on March 6, 2026.",
    "paragraph_id": "0001628280-26-029054:notes:158",
    "explanation": false
  }
]
```

No paragraph carried as text shows narrative signs of operating pressure, and none bears on controls or filings beyond the routine Item 4 conclusion.

## Paragraphs carried as text and not made into items

### Notes

- 0001628280-26-029054:notes:1 — wording only: adds the "WD" short name and drops the spelled-out "hard disk drives".
- 0001628280-26-029054:notes:2 — wording only: quotation marks added around the end-market names.
- 0001628280-26-029054:notes:3 — wording only: shorter reference to the 2025 Annual Report.
- 0001628280-26-029054:notes:4 — date rolled forward (comparative now the three and nine months ended March 28, 2025); "former" added before "Flash business".
- 0001628280-26-029054:notes:9 — heading.
- 0001628280-26-029054:notes:10 — insufficient: pending standard ASU 2025-10, impact being assessed, no figure affected; prior text not in input.
- 0001628280-26-029054:notes:11 — insufficient: pending standard ASU 2025-09, impact being assessed; prior text not in input.
- 0001628280-26-029054:notes:12 — insufficient: pending standard ASU 2025-07, no material impact expected; prior text not in input.
- 0001628280-26-029054:notes:13 — insufficient: pending standard ASU 2025-06, impact being assessed; prior text not in input.
- 0001628280-26-029054:notes:14 — insufficient: pending standard ASU 2024-03, adoption timing stated; prior text not in input.
- 0001628280-26-029054:notes:15 — insufficient: ASU 2023-09 disclosures planned for the annual report; prior text not in input.
- 0001628280-26-029054:notes:17 — amounts only: revenue disaggregation table, periods rolled.
- 0001628280-26-029054:notes:19 — same text as mdna:36; covered by revenue_recognition_customer_revenue_concentration.
- 0001628280-26-029054:notes:21 — heading moved here from the organization note (0001628280-26-004207:note_history:8).
- 0001628280-26-029054:notes:22 — moved from the organization note, with wording changes only: names the CEO as CODM, labels the segment "HDD", adds "and solutions". Segment structure is unchanged.
- 0001628280-26-029054:notes:24 — amounts only. The new debt-for-equity caption is covered by earnings_quality_debt_for_equity_exchange_discount_charge.
- 0001628280-26-029054:notes:27 — insufficient: standing description of the February 2025 Separation; prior text not in input.
- 0001628280-26-029054:notes:28 — date rolled forward.
- 0001628280-26-029054:notes:29 — amounts only: discontinued-operations table, comparative period rolled.
- 0001628280-26-029054:notes:31 — amounts only.
- 0001628280-26-029054:notes:33 — insufficient: standing statement on transition services agreements (not material); prior text not in input.
- 0001628280-26-029054:notes:36 — amounts only: inventory table. The MD&A inventory explanation is itemized from mdna:65.
- 0001628280-26-029054:notes:38 — amounts only.
- 0001628280-26-029054:notes:40 — amounts only.
- 0001628280-26-029054:notes:43 — amounts only: warranty rollforward table.
- 0001628280-26-029054:notes:45 — amounts only.
- 0001628280-26-029054:notes:47 — amounts only.
- 0001628280-26-029054:notes:49 — date rolled forward: still no goodwill impairment indicators, and the prose gives the same carrying amount at both dates.
- 0001628280-26-029054:notes:52 — amounts only: AOCI table.
- 0001628280-26-029054:notes:53 — covered by earnings_quality_cash_flow_hedge_net_losses_to_reclassify.
- 0001628280-26-029054:notes:60 — insufficient: standing fair-value policy for the retained Sandisk interest; prior text not in input.
- 0001628280-26-029054:notes:62 — amounts only.
- 0001628280-26-029054:notes:66 — date rolled forward.
- 0001628280-26-029054:notes:67 — amounts only. The retired notes now show dashes; this is covered by the debt items from notes:70.
- 0001628280-26-029054:notes:68 — heading.
- 0001628280-26-029054:notes:69 — amounts only: debt table. Covered by liquidity_and_capital_senior_notes_redeemed_with_bridge_loan.
- 0001628280-26-029054:notes:71 — date rolled forward; wording.
- 0001628280-26-029054:notes:72 — wording: "Loan Agreement" is now defined here because the Term Loan paragraph that defined it was removed. Date rolled forward.
- 0001628280-26-029054:notes:73 — date rolled forward.
- 0001628280-26-029054:notes:74 — amounts only: conversion price now approximately $37.72 (prior text: approximately $37.74). The parenthetical on the basis of adjustment is removed, and the redemption sentence moved to notes:78.
- 0001628280-26-029054:notes:76 — date rolled forward. The current-debt classification is restated with "including the Tendered Notes" and "consistent with each quarter since the quarter ended June 27, 2025"; the classification itself is unchanged.
- 0001628280-26-029054:notes:77 — reordered: split out of the removed 0001628280-26-004207:note_history:23.
- 0001628280-26-029054:notes:78 — reordered: sentence moved out of the conversion-terms paragraph.
- 0001628280-26-029054:notes:79 — amounts and wording: strike approximately $37.72 and cap approximately $50.41 are now stated as current terms. The prior text gave $37.74 and an expected cap of $50.43.
- 0001628280-26-029054:notes:83 — amounts only.
- 0001628280-26-029054:notes:85 — amounts only.
- 0001628280-26-029054:notes:87 — amounts only.
- 0001628280-26-029054:notes:88 — date rolled forward.
- 0001628280-26-029054:notes:89 — amounts only.
- 0001628280-26-029054:notes:91 — date rolled forward: standing description of purchase commitments.
- 0001628280-26-029054:notes:92 — amounts only.
- 0001628280-26-029054:notes:96 — wording: table lead-in.
- 0001628280-26-029054:notes:97 — amounts only.
- 0001628280-26-029054:notes:102 — date rolled forward.
- 0001628280-26-029054:notes:103 — amounts only.
- 0001628280-26-029054:notes:104 — amounts only: accrued interest and penalties, and the potential cash payments within twelve months.
- 0001628280-26-029054:notes:108 — amounts only.
- 0001628280-26-029054:notes:110 — date rolled forward.
- 0001628280-26-029054:notes:111 — amounts only.
- 0001628280-26-029054:notes:115 — amounts only.
- 0001628280-26-029054:notes:117 — amounts only.
- 0001628280-26-029054:notes:118 — date rolled forward.
- 0001628280-26-029054:notes:121 — amounts only.
- 0001628280-26-029054:notes:122 — amounts only.
- 0001628280-26-029054:notes:124 — date rolled forward.
- 0001628280-26-029054:notes:125 — amounts only.
- 0001628280-26-029054:notes:130 — amounts only.
- 0001628280-26-029054:notes:132 — heading.
- 0001628280-26-029054:notes:133 — amounts only: shares issued, shares outstanding, treasury shares.
- 0001628280-26-029054:notes:135 — wording and date: now refers only to the June 27, 2025 preferred balance. Covered by liquidity_and_capital_preferred_shares_mandatorily_converted_to_common.
- 0001628280-26-029054:notes:136 — wording (past tense) and the cash preferred dividend amount. Covered by the preferred conversion item.
- 0001628280-26-029054:notes:141 — amounts only: dividends paid in the quarter and the nine months.
- 0001628280-26-029054:notes:145 — amounts only: EPS table.
- 0001628280-26-029054:notes:148 — date rolled forward.
- 0001628280-26-029054:notes:149 — heading.
- 0001628280-26-029054:notes:150 — date rolled forward only: SPEX no-accrual statement now as of April 3, 2026 (history similarity 0.9943).
- 0001628280-26-029054:notes:151 — background to notes:152; covered by earnings_quality_prior_year_litigation_reversal_in_comparative.
- 0001628280-26-029054:notes:153 — heading.
- 0001628280-26-029054:notes:154 — insufficient: standing boilerplate on other legal matters; prior text not in input.
- 0001628280-26-029054:notes:155 — insufficient: standing boilerplate on litigation estimates; prior text not in input.

### MD&A

- 0001628280-26-029054:mdna:4 — insufficient: business description (cloud and hyperscale focus); prior text not in input; no figure affected.
- 0001628280-26-029054:mdna:5 — wording: end-market description, mirrors notes:2.
- 0001628280-26-029054:mdna:8 — heading, now naming the monetization of Sandisk shares.
- 0001628280-26-029054:mdna:9 — same substance as notes:32 and notes:70; covered there.
- 0001628280-26-029054:mdna:11 — new heading for the preferred conversion; covered by the preferred conversion item.
- 0001628280-26-029054:mdna:12 — same substance as notes:137; covered by the preferred conversion item.
- 0001628280-26-029054:mdna:15 — date rolled forward: tariffs still described as not material, now through the third quarter of 2026.
- 0001628280-26-029054:mdna:16 — page number.
- 0001628280-26-029054:mdna:18 — heading; date rolled forward.
- 0001628280-26-029054:mdna:20 — amounts only. The new debt-for-equity caption is covered by earnings_quality_debt_for_equity_exchange_discount_charge.
- 0001628280-26-029054:mdna:23 — amounts only.
- 0001628280-26-029054:mdna:26 — amounts only: same table as notes:17.
- 0001628280-26-029054:mdna:28 — page number.
- 0001628280-26-029054:mdna:29 — heading; date rolled forward.
- 0001628280-26-029054:mdna:43 — cross-reference to Note 14.
- 0001628280-26-029054:mdna:49 — insufficient: says CAMT is not expected to apply in 2026; prior text not in input.
- 0001628280-26-029054:mdna:51 — table lead-in.
- 0001628280-26-029054:mdna:52 — amounts only.
- 0001628280-26-029054:mdna:53 — same text as notes:98; covered by earnings_quality_tax_rate_lowered_by_tax_free_sandisk_gain.
- 0001628280-26-029054:mdna:54 — same text as notes:99; covered by earnings_quality_prior_year_one_time_deferred_tax_benefit.
- 0001628280-26-029054:mdna:55 — page number.
- 0001628280-26-029054:mdna:58 — amounts only: cash flow summary table.
- 0001628280-26-029054:mdna:61 — insufficient: standing statement that liquidity is sufficient, relying on cash and the 2027 revolver; prior text not in input.
- 0001628280-26-029054:mdna:62 — amounts only: cash held by foreign subsidiaries.
- 0001628280-26-029054:mdna:67 — amounts only: investing activities and the capex amount.
- 0001628280-26-029054:mdna:72 — page number.
- 0001628280-26-029054:mdna:75 — date rolled forward: lead-in to cash requirements.
- 0001628280-26-029054:mdna:76 — amounts only: contractual obligations table.
- 0001628280-26-029054:mdna:78 — amounts only: same as notes:103 and notes:104.
- 0001628280-26-029054:mdna:79 — heading.
- 0001628280-26-029054:mdna:80 — cross-reference to Note 14.
- 0001628280-26-029054:mdna:82 — amounts only: same as notes:141.
- 0001628280-26-029054:mdna:83 — same as notes:142; covered by related_parties_contingencies_and_subsequent_events_dividend_declared_after_quarter_end.
- 0001628280-26-029054:mdna:86 — amounts and wording: conversion price and redemption terms, same as notes:74 and notes:78.
- 0001628280-26-029054:mdna:87 — same as notes:75; covered by liquidity_and_capital_convertible_notes_tendered_with_cash_settlement_election.
- 0001628280-26-029054:mdna:88 — same as notes:75 and notes:76; date rolled forward and covered.
- 0001628280-26-029054:mdna:93 — amounts only: guarantor summarized balance sheet.
- 0001628280-26-029054:mdna:95 — amounts only: guarantor summarized results.
- 0001628280-26-029054:mdna:97 — amounts only: intercompany amounts.
- 0001628280-26-029054:mdna:101 — insufficient: accrued GMT liabilities and their expected payment timing; prior text not in input.

### Item 4 and the auditor's report

- 0001628280-26-029054:item_4_controls:1 — heading.
- 0001628280-26-029054:item_4_controls:2 — heading.
- 0001628280-26-029054:item_4_controls:3 — carried verbatim: disclosure controls effective; no change in substance.
- 0001628280-26-029054:item_4_controls:4 — heading.
- 0001628280-26-029054:item_4_controls:5 — date rolled forward: no material change in internal control for the quarter ended April 3, 2026.
- 0001628280-26-029054:item_4_controls:6 — page number.
- Auditor's report: none in the input.

### 8-K and prior flags

- input_8k.md — item-code index only. There is no body text and no paragraph id to quote. The index shows no 4.01 or 4.02 item; its February 2026 codes are referenced in the preferred conversion item.
- input_prior_predictions.md — none on record.

### Note change history (a guide to what is new, not a second list; mapped to where each change is handled)

- 0001628280-26-029054:note_history:1 — current SPEX text; see notes:150 (date rolled forward).
- 0001628280-26-029054:note_history:2 — current MRT text; see notes:151 (covered).
- 0001628280-26-029054:note_history:3 — current MRT text; see notes:152 (itemized).
- 0001628280-26-029054:note_history:4 — see notes:1 (wording).
- 0001628280-26-029054:note_history:5 — see notes:2 (wording).
- 0001628280-26-029054:note_history:6 — see notes:3 (wording).
- 0001628280-26-029054:note_history:7 — see notes:4 (date rolled forward).
- 0001628280-26-029054:note_history:10 — see notes:69 (amounts only).
- 0001628280-26-029054:note_history:11 — see notes:70 (itemized).
- 0001628280-26-029054:note_history:12 — see notes:71 (date rolled forward).
- 0001628280-26-029054:note_history:13 — see notes:72 (wording).
- 0001628280-26-029054:note_history:14 — see notes:73 (date rolled forward).
- 0001628280-26-029054:note_history:15 — see notes:74 (amounts only; reordered).
- 0001628280-26-029054:note_history:16 — see notes:75 (itemized).
- 0001628280-26-029054:note_history:17 — see notes:76 (date rolled forward).
- 0001628280-26-029054:note_history:18 — see notes:77 (reordered).
- 0001628280-26-029054:note_history:19 — see notes:78 (reordered).
- 0001628280-26-029054:note_history:20 — see notes:79 (amounts and wording).
- 0001628280-26-029054:note_history:24 — see notes:69 (amounts only).
- 0001628280-26-029054:note_history:25 — see notes:17 (amounts only).
- 0001628280-26-004207:note_history:1 — prior wording for notes:150; no separate item.
- 0001628280-26-004207:note_history:4 — prior wording for notes:1; no separate item.
- 0001628280-26-004207:note_history:5 — prior wording for notes:2; no separate item.
- 0001628280-26-004207:note_history:6 — prior wording for notes:3; no separate item.
- 0001628280-26-004207:note_history:7 — prior wording for notes:4; no separate item.
- 0001628280-26-004207:note_history:8 — removed from the organization note; segment heading moved to notes:21.
- 0001628280-26-004207:note_history:9 — removed from the organization note; segment text moved to notes:22.
- 0001628280-26-004207:note_history:10 — prior debt table; no separate item.
- 0001628280-26-004207:note_history:12 — prior wording for notes:71; no separate item.
- 0001628280-26-004207:note_history:13 — prior wording for notes:72; no separate item.
- 0001628280-26-004207:note_history:14 — prior wording for notes:73; no separate item.
- 0001628280-26-004207:note_history:15 — prior wording for notes:74 and notes:78; no separate item.
- 0001628280-26-004207:note_history:20 — prior wording for notes:79; no separate item.
- 0001628280-26-004207:note_history:21 — removed: the stated intent to redeem the 4.75% notes and the scheduled repayments. Covered in liquidity_and_capital_senior_notes_redeemed_with_bridge_loan.
- 0001628280-26-004207:note_history:22 — removed: the Term Loan A-3 interest rate (loan since retired). Covered in liquidity_and_capital_bridge_loan_and_term_loan_retired_through_sandisk_share_exchange.
- 0001628280-26-004207:note_history:23 — removed: the earlier conversion trigger and classification text, restated in notes:75 through notes:77.
- 0001628280-26-004207:note_history:24 — prior debt table; no separate item.
- 0001628280-26-004207:note_history:25 — prior revenue disaggregation table; no separate item.

## Marked insufficient

These are listed by id, without a count.

- **Items:**
  - liquidity_and_capital_capital_expenditure_range_of_net_revenue
  - earnings_quality_excess_windfall_tax_benefits
  - earnings_quality_tax_rate_lowered_by_tax_free_sandisk_gain
  - estimates_and_discretion_remaining_realignment_termination_costs
  - earnings_quality_cash_flow_hedge_net_losses_to_reclassify
- **Paragraph lines:**
  - notes:10, notes:11, notes:12, notes:13, notes:14, notes:15
  - notes:27, notes:33, notes:60, notes:154, notes:155
  - mdna:4, mdna:49, mdna:61, mdna:101
