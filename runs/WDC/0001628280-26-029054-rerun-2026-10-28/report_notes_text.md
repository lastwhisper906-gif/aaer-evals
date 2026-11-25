<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# Notes text report: WDC 10-Q, quarter ended April 3, 2026 (0001628280-26-029054)

Prior period of the same kind: 0001628280-26-004207 (10-Q, quarter ended January 2, 2026).

## Scope

- **Files read in full:**
  - input_8k.md
  - input_controls.md
  - input_mdna.md
  - input_notes.md (all 760 lines)
  - input_notes_history.md
  - input_prior_predictions.md
- **Out-of-scope material:** none found. There is no trend table, price, abnormal return, short-interest figure, other company's file, prior probability or outcome window. The prior-predictions file says no earlier run is on record, so no flags are carried forward.
- **Expected inputs that were missing:**
  - The auditor's report: the controls file carries only Item 4.
  - The Item 1A diff.
  - The Exhibit 21 diff.
  - Any Exhibit 10.
  - Any 8-K item body: only item codes are listed.
- **Paragraphs with no prior text:** the note change history covers only the legal, organization, debt and revenue-table tags. Many other paragraphs are carried as changed, but their prior wording is not in the input. For those, each item reports what the text now says and states that the specific edit cannot be isolated.
- **No arithmetic was done.** Where two texts give figures for the same thing, both are quoted and the reconciliation is left to the numbers reader and the supervisor.
- **Counts:**
  - 48 items.
  - 4 items flagged `explanation: true`.
  - 5 `insufficient` entries.

## Items

```json
{ "id": "liquidity_and_capital_senior_notes_and_term_loan_retired_through_sandisk_exchange",
  "what_changed": "New paragraph. In February 2026 the company took a $1.50 billion Bridge Loan. It used the proceeds to redeem all Senior Notes (the 4.75% notes due 2026, 2.85% notes due 2029 and 3.10% notes due 2032) in cash at par plus accrued interest, and wrote off $6 million of unamortized issuance costs. It then retired the Bridge Loan and Term Loan A-3 in a non-cash, tax-free exchange of 5.8 million Sandisk shares valued at $3.62 billion. The prior text giving the Term Loan A-3 all-in rate (5.300%) and its scheduled repayments was removed. The debt note's prose now describes only the 2028 Convertible Notes and the undrawn revolver. The Loan Agreement is now defined as the agreement governing the revolver (notes:72).",
  "account": "Total debt; Current portion of long-term debt; Long-term debt",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "Following the redemptions, the Company retired the Bridge Loan and its existing Term Loan A-3 through a non-cash, tax-free exchange for 5.8 million shares of Sandisk common stock held by the Company, valued at $3.62 billion on the date of exchange.",
  "paragraph_id": "0001628280-26-029054:notes:70",
  "explanation": false }
```

```json
{ "id": "earnings_quality_debt_for_equity_exchange_discount_driven_by_sandisk_volatility",
  "what_changed": "New. The exchange produced $539 million in a new income-statement caption, Costs in connection with debt-for-equity exchange. Management says the amount mainly reflects a discount on the Sandisk shares given to the counterparties. It says the discount was needed because Sandisk's share price was volatile during the exchange. This is a non-operating charge, recorded for the first time this quarter. The prose does not say whether exchanging the remaining 1.7 million Sandisk shares will also involve a discount.",
  "account": "Costs in connection with debt-for-equity exchange",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "This amount primarily reflects a discount on Sandisk shares provided to the counterparties in connection with the exchange. The need for the discount was primarily driven by volatility of the Sandisk stock price in the period of the exchange.",
  "paragraph_id": "0001628280-26-029054:notes:70",
  "explanation": false }
```

```json
{ "id": "across_documents_debt_for_equity_exchange_cost_figures_in_notes_and_discussion",
  "what_changed": "MD&A describes $545 million of costs incurred in connection with the debt-for-equity exchange and says they reflect the discount. Notes:70 says the exchange resulted in $539 million recorded in the same caption, mainly reflecting a discount. Notes:70 separately states a $6 million write-off of unamortized issuance costs on the Senior Notes redemptions. The two texts give different figures for the exchange cost, and neither text explains the other. This reader has not checked how they relate; that reconciliation is for the numbers reader and the supervisor.",
  "account": "Costs in connection with debt-for-equity exchange",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "These changes were partially offset by $545 million of costs incurred in connection with our debt-for-equity exchange, which reflects the discount provided on the monetization of Sandisk shares.",
  "paragraph_id": "0001628280-26-029054:mdna:46",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_remaining_sandisk_stake_to_be_exchanged_for_own_shares",
  "what_changed": "New statement of intent. The 1.7 million Sandisk shares still held at April 3, 2026 are to be monetized by the end of 2026 in one or more exchanges for the company's own common stock. This follows the debt exchanges of June 2025 and February 2026. The filing labels fiscal periods by year (it calls the quarter ended April 3, 2026 'the third quarter of 2026'), so 'by the end of 2026' probably means fiscal year-end; the prose does not say. The prose implies that the Level 1 retained-interest asset and its gain/loss line go away and that the company's own shares come back in. MD&A repeats this under a retitled heading (mdna:8, mdna:9).",
  "account": "Retained interest in Sandisk",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "As of April 3, 2026, the Company still held 1.7 million shares of Sandisk common stock, which it expects to monetize by the end of 2026 in one or more subsequent exchanges for its outstanding common stock.",
  "paragraph_id": "0001628280-26-029054:notes:32",
  "explanation": false }
```

```json
{ "id": "earnings_quality_sandisk_mark_to_market_gain_in_other_income",
  "what_changed": "MD&A attributes the change in total interest and other income to a mark-to-market gain on the retained Sandisk interest. For the nine months it calls the gain an 'unrealized gain of $4.45 billion'. Notes:98 says the gain is tax-free because of the Separation. The gain is non-operating and non-cash. It depends on Sandisk's share price for as long as shares remain (1.7 million at quarter-end per notes:32).",
  "account": "Gain (loss) on retained interest in Sandisk",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The change reflects a gain of $2.73 billion on our retained interest in Sandisk in the current period based on the mark-to-market value as of April 3, 2026, compared to a loss of $606 million in the prior year",
  "paragraph_id": "0001628280-26-029054:mdna:46",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_interest_expense_lower_on_debt_reduction",
  "what_changed": "MD&A attributes lower interest expense to the reduction in debt. The Senior Notes, the Bridge Loan and Term Loan A-3 were all retired during this quarter (notes:70). The prose therefore implies interest expense stays lower next quarter, the first full quarter without them. The 3.00% 2028 Convertible Notes remain.",
  "account": "Interest expense",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "and lower interest expense of $53 million, which reflects the reduction in our debt",
  "paragraph_id": "0001628280-26-029054:mdna:46",
  "explanation": false }
```

```json
{ "id": "articulation_and_the_filed_history_prior_stated_intent_to_redeem_notes_carried_out",
  "what_changed": "Removed from the prior period. The prior 10-Q said the company intended to redeem or repay the $500 million 4.75% notes due 2026 by their February 15, 2026 maturity. The current notes say all Senior Notes, including those, were redeemed in cash in February 2026 with the Bridge Loan proceeds. The stated intent was carried out, and the 2029 and 2032 notes were redeemed as well. The removed paragraph also gave Term Loan A-3 scheduled repayments; notes:70 now gives them on a nine-month basis.",
  "account": "Current portion of long-term debt",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "The Company intends to redeem or repay the outstanding $500 million aggregate principal amount of 4.75% senior unsecured notes due 2026 on or before the scheduled maturity date of February 15, 2026.",
  "paragraph_id": "0001628280-26-004207:note_history:21",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_bridge_loan_cash_inflow_with_noncash_retirement",
  "what_changed": "Nine-month financing cash flows now show $1.50 billion of bridge-loan proceeds as an inflow. Outflows are $1.56 billion of debt repayments, $1.92 billion of share repurchases and $130 million of dividends (all figures from the prose). Notes:70 says the Bridge Loan and Term Loan A-3 were retired in a non-cash exchange. So the bridge loan is recorded as borrowed in cash but not repaid in cash. Whether the non-cash retirement is disclosed as such is for the numbers reader to check.",
  "account": "Net cash used in financing activities",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "These uses were partially offset by $1.50 billion of net proceeds from a bridge loan and $32 million of proceeds from the issuance of stock under employee stock plans.",
  "paragraph_id": "0001628280-26-029054:mdna:69",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_investment_grade_ratings_release_revolver_guarantees_and_collateral",
  "what_changed": "New sentence. During the quarter the company obtained investment-grade ratings from two rating agencies. Under the Loan Agreement, that released the guarantees and collateral on the 2027 Revolving Credit Facility. Only MD&A says this; the debt note (notes:71, notes:72) mentions neither the ratings nor the release. The summarized financial information for the parent and guarantors is still presented (mdna:93, mdna:95, mdna:97), and the prose does not say whether that presentation will change.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "During the three months ended April 3, 2026, the Company obtained investment grade ratings from two rating agencies and therefore, pursuant to the terms of the Loan Agreement, the guarantees and collateral on the 2027 Revolving Credit Facility were released.",
  "paragraph_id": "0001628280-26-029054:mdna:89",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_sufficiency_statement_relies_on_revolver_maturing_january",
  "what_changed": "This paragraph is marked as changed, but the prior wording is not in the input, so the specific edit cannot be isolated. It names cash and the available 2027 Revolving Credit Facility as the sources that will cover needs 'for at least the next twelve months'. Mdna:89 and notes:71 say that facility matures in January 2027, and the prose says nothing about renewing or replacing it. The paragraph also cites risk factors in Part II, Item 1A of this 10-Q, which are not in this input.",
  "account": "Cash and cash equivalents; 2027 Revolving Credit Facility",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "We believe our cash and cash equivalents and our available 2027 Revolving Credit Facility (as defined below) will be sufficient to meet our working capital, debt, dividend and capital expenditure needs for at least the next twelve months and for the foreseeable future thereafter.",
  "paragraph_id": "0001628280-26-029054:mdna:61",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_tendered_convertible_notes_cash_settlement_election",
  "what_changed": "New. Holders tendered $32 million principal of the 2028 Convertible Notes during the quarter. The company irrevocably elected to settle in cash the part of the conversion obligation above principal; under notes:74, principal is always paid in cash. Settlement is scheduled for June 2026, so the prose implies a cash outflow and a reduction in the convertible notes next quarter. For the remaining notes the company keeps the choice of cash, shares or a mix.",
  "account": "Current portion of long-term debt (Tendered Notes)",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "The Company made an irrevocable election to settle in cash the conversion obligation in excess of the principal amount of the Tendered Notes, as permitted by the Indenture.",
  "paragraph_id": "0001628280-26-029054:notes:75",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_bifurcated_conversion_derivative_remeasured_through_other_income",
  "what_changed": "New accounting. Because of the cash-settlement election, the embedded conversion feature on the Tendered Notes is split out as a derivative under ASC 815. The derivative is remeasured at fair value each period through Other income (expense), net; this quarter that produced what the company calls 'an immaterial gain'. Until settlement in June 2026, this line moves with the company's own share price. The fair value hierarchy table (notes:62) has no separate caption for the derivative. Where it sits on the balance sheet is a question for the numbers reader.",
  "account": "Other income (expense), net",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "This election requires bifurcation and separate accounting of the embedded conversion feature as a derivative instrument pursuant to Accounting Standards Codification 815. The derivative is remeasured to fair value at each reporting period, with changes recognized in Other income (expense), net in the Condensed Consolidated Statements of Operations.",
  "paragraph_id": "0001628280-26-029054:notes:75",
  "explanation": false }
```

```json
{ "id": "articulation_and_the_filed_history_convertible_notes_current_in_each_quarter",
  "what_changed": "New wording. The conversion trigger was met again in the calendar quarter ended March 31, 2026, so holders can convert through June 30, 2026 and the notes stay in current liabilities. The text now says the current classification has been 'consistent with each quarter since the quarter ended June 27, 2025'. The removed prior paragraph named only January 2, 2026 and June 27, 2025 as current-classified dates. It cited triggers in the calendar quarters ended June 30, 2025 and December 31, 2025. The claim about every quarter can be checked against the filed balance sheets. The company says it will keep reassessing every quarter.",
  "account": "Current portion of long-term debt",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "the Company classified the 2028 Convertible Notes, including the Tendered Notes, in the Current portion of long-term debt in the Condensed Consolidated Balance Sheet as of April 3, 2026, consistent with each quarter since the quarter ended June 27, 2025",
  "paragraph_id": "0001628280-26-029054:notes:76",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_convertible_conversion_price_and_capped_call_terms_restated",
  "what_changed": "The conversion price is now 'approximately $37.72' as of April 3, 2026. The prior text said approximately $37.74 as of January 2, 2026, and explained the adjustment as resulting from the Separation and dividends paid; that explanation is gone. The capped calls (notes:79) are restated to a strike of about $37.72 and a cap of about $50.41. The prior text gave a strike of $37.74 and an expected adjusted cap of about $50.43. The optional-redemption sentence (on or after November 15, 2026) now has its own paragraph (notes:78). The prose does not say which way the terms moved.",
  "account": "Diluted weighted average shares (convertible notes)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "at a conversion price of approximately $37.72 per share of common stock as of April 3, 2026",
  "paragraph_id": "0001628280-26-029054:notes:74",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_preferred_shares_mandatory_conversion",
  "what_changed": "New. On February 17, 2026 all Preferred Shares were mandatorily converted into 7 million common shares. Just before conversion their aggregate liquidation preference was $267 million, including $32 million of in-kind dividends. A Certificate of Elimination was filed on February 24, 2026. The preferred-stock paragraphs (notes:135, notes:136) are now in the past tense, and MD&A adds a 'Conversion of Preferred Shares' section (mdna:11, mdna:12). The 8-K index lists filings on 2026-02-18 (item 3.03) and 2026-02-24 (items 5.03, 8.01, 9.01), but their bodies are not in input. With no preferred shares left, the prose implies preferred dividends stop.",
  "account": "Dividends allocated to preferred shareholders",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "On February 17, 2026, the Company converted all remaining outstanding Preferred Shares into 7 million shares of the Company",
  "paragraph_id": "0001628280-26-029054:notes:137",
  "explanation": false }
```

```json
{ "id": "earnings_quality_participating_securities_allocation_ends_with_conversion",
  "what_changed": "The EPS footnote now says the Preferred Shares were participating securities 'prior to their conversion'. Because they have been converted, the prose implies that from next quarter no income is allocated to participating securities in the two-class calculation. Notes:148 still lists Preferred Shares among potentially dilutive shares for the periods presented.",
  "account": "Income attributable to participating securities",
  "expected_direction": "down",
  "horizon": "next quarter",
  "quote": "Participating securities consisted of Preferred Shares because, prior to their conversion, they participated on a pro rata basis in any dividends declared on shares of common stock.",
  "paragraph_id": "0001628280-26-029054:notes:146",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_additional_share_repurchase_authorization",
  "what_changed": "New. On February 2, 2026 the board added a $4.00 billion repurchase authorization to the $2.00 billion program authorized on May 9, 2025; the program has no expiration date. In the quarter the company bought back 2.9 million shares for $752 million, plus $5 million of accrued excise tax. Over nine months it bought 13.1 million shares for $1.92 billion. $3.93 billion remained available at April 3, 2026. Repurchases are expected to be funded mainly from operating cash flows. The prose gives no target for future buybacks.",
  "account": "Share repurchases (financing cash outflow); treasury stock",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Board of Directors authorized the repurchase of up to an additional $4.00 billion",
  "paragraph_id": "0001628280-26-029054:notes:139",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_dividend_declared_after_quarter_end",
  "what_changed": "New subsequent event. On April 29, 2026 the board declared a dividend of $0.15 per share, payable June 17, 2026 to holders of record on June 5, 2026. The dividend paid this quarter is stated as $0.125 per share (notes:141, mdna:82). The prose does not call the declared amount an increase. Comparing the two is for the numbers reader.",
  "account": "Dividends paid",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "Subsequent to quarter-end, on April 29, 2026, the Board of Directors declared a cash dividend of $0.15 per share",
  "paragraph_id": "0001628280-26-029054:notes:142",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_mrt_settlement_reversal_in_comparative_period",
  "what_changed": "Added paragraph; the note change history shows it was not in the prior 10-Q's legal note. The company reached a $130 million global settlement with MRT in April 2025. As a result, the comparative three- and nine-month periods ended March 28, 2025 include reversals of $201 million and $198 million of earlier Litigation matter charges. Management attributes the reversal to the settlement. The comparative-period operating expenses therefore contain a settlement credit; the current-period Litigation matter line in the MD&A table shows none. This reader's interpretation, which the filing does not state: the paragraph appears to have been restored because the comparative quarter now contains the reversal.",
  "account": "Litigation matter (operating expenses)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "In April 2025, the Company reached a global settlement of $130 million for all pending matters with MRT.",
  "paragraph_id": "0001628280-26-029054:notes:152",
  "explanation": true }
```

```json
{ "id": "earnings_quality_mrt_patent_license_asset_amortization",
  "what_changed": "Added paragraph restating the MRT history. After the jury verdict, the company recognized a $384 million aggregate liability in Q4 fiscal 2024. Of that, $291 million was expensed under Litigation matter, and $93 million was recorded as patent licenses in Other non-current assets, to be amortized over their remaining lives. The prose does not say whether the later settlement changed that asset. The amortization continues to run through expense.",
  "account": "Other non-current assets (patent licenses)",
  "expected_direction": "down",
  "horizon": "12 months",
  "quote": "$93 million recognized as Other non-current assets for the patent licenses, to be amortized over their remaining lives",
  "paragraph_id": "0001628280-26-029054:notes:151",
  "explanation": false }
```

```json
{ "id": "earnings_quality_comparative_period_one_time_deferred_tax_benefit",
  "what_changed": "The comparative quarter is now the one in which the Separation took place. The prior-year tax paragraph therefore includes a $711 million one-time deferred tax benefit for the three and nine months ended March 28, 2025. The benefit came from an inter-entity asset transfer done in anticipation of operating as a standalone HDD business in a GMT environment. In the prior 10-Q the comparative period was the quarter ended December 27, 2024 (note history); the Separation was completed on February 21, 2025. The prose implies current-period income tax expense is compared with a period that contained a one-time benefit. MD&A repeats this (mdna:54).",
  "account": "Income tax expense (benefit)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "This resulted in the recognition of one-time deferred tax benefits to continuing operations of $711 million for the three and nine months ended March 28, 2025.",
  "paragraph_id": "0001628280-26-029054:notes:99",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_effective_tax_rate_drivers_include_tax_free_sandisk_gain",
  "what_changed": "The current-period drivers of the effective tax rate are jurisdictional mix, the FDDEI deduction, tax credits, and the tax-free treatment of the Sandisk retained-interest gain. The provision includes GMT for Malaysia, Thailand and the Philippines, where the company has tax holidays. The prior wording is not in this input. Part of the low rate depends on the Sandisk gain, which ends once the remaining shares are exchanged (see the remaining Sandisk stake item). MD&A repeats this (mdna:53).",
  "account": "Income tax expense (benefit); effective tax rate",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "the deduction for FDDEI, tax credits, and the gain on the retained interest in Sandisk being tax-free due to the Separation",
  "paragraph_id": "0001628280-26-029054:notes:98",
  "explanation": false }
```

```json
{ "id": "earnings_quality_excess_windfall_tax_benefits_reduce_tax_expense",
  "what_changed": "The paragraph now gives excess windfall tax benefits of $47 million for the three months and $76 million for the nine months, recognized in income tax expense. It says they were immaterial in the comparative periods. These benefits come from the stock price at vesting and exercise, not from operations. The prior wording is not in this input.",
  "account": "Income tax expense (benefit)",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "During the three and nine months ended April 3, 2026, excess windfall tax benefits were $47 million and $76 million, respectively.",
  "paragraph_id": "0001628280-26-029054:notes:123",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_unrecognized_tax_benefits_near_term_cash_payments",
  "what_changed": "The estimate of unrecognized tax benefits, including interest and penalties, that could be paid in cash within twelve months is now approximately $133 million. Accrued interest and penalties are $123 million. Unrecognized tax benefits excluding interest are $603 million (mdna:78); the rollforward (notes:103) shows gross increases for current- and prior-year positions. The prior-period amounts are not in this input, and the prose gives no direction or cause. MD&A repeats this (mdna:78).",
  "account": "Liability for unrecognized tax benefits",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Of the aggregate unrecognized tax benefits, including interest and penalties, approximately $133 million could result in potential cash payments to be made within the next twelve months.",
  "paragraph_id": "0001628280-26-029054:notes:104",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_global_minimum_tax_accrual_payment_deferred",
  "what_changed": "The prose now says accrued GMT liabilities are $62 million at April 3, 2026 and are not expected to be paid until the second quarter of 2028. The prior amount is not in this input, and the prose gives no cause. The accrual is on the balance sheet now; the cash payment is beyond twelve months.",
  "account": "Accrued GMT liabilities",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "As of April 3, 2026, we have accrued GMT liabilities of $62 million that are not expected to be paid until the second quarter of 2028.",
  "paragraph_id": "0001628280-26-029054:mdna:101",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_corporate_alternative_minimum_tax_not_expected",
  "what_changed": "This paragraph is marked as changed. It says the company was not subject to CAMT for 2024 or 2025 and does not expect to be for 2026. The reason given is that its three-year average AFSI did not pass the $1.0 billion threshold. The prior wording is not in this input, so the specific edit cannot be isolated. The expectation covers 2026 only; the prose says nothing about later years.",
  "account": "Income tax expense",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "We do not expect to be subject to CAMT in 2026 as our annual average AFSI did not exceed $1.0 billion for the preceding three-year period.",
  "paragraph_id": "0001628280-26-029054:mdna:49",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_additional_employee_termination_costs_expected",
  "what_changed": "New forward estimate. The realignment actions are expected to add approximately $5 million of employee termination costs in the rest of 2026. The description of the actions themselves is carried unchanged (notes:106, notes:107). The prose implies realignment charges continue next quarter.",
  "account": "Business realignment charges",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "the Company expects to record incremental employee termination costs of approximately $5 million in the remainder of 2026",
  "paragraph_id": "0001628280-26-029054:notes:109",
  "explanation": false }
```

```json
{ "id": "structure_and_disclosure_changes_income_tax_disclosure_standard_in_next_annual_report",
  "what_changed": "The enhanced income tax disclosures under ASU 2023-09 (tabular rate reconciliation and income taxes paid) are to appear in the annual report for the year ending July 3, 2026, which is the next periodic filing. The paragraph is marked as changed, and the prior wording is not in this input.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "next quarter",
  "quote": "The Company is currently compiling the information required for these disclosures and expects to provide any required disclosures in its annual report for the year ending July 3, 2026.",
  "paragraph_id": "0001628280-26-029054:notes:15",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_exabyte_volume_and_price_drivers",
  "what_changed": "MD&A attributes the quarter's revenue growth to both exabytes sold and average selling price per exabyte. It attributes both to 'strong demand across all of our end markets'. The nine-month explanation cites the same factors. The prior wording is not in this input.",
  "account": "Revenue, net",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "driven by a 34% increase in exabytes sold and a 9% increase in average selling price per exabyte, both of which were driven by strong demand across all of our end markets",
  "paragraph_id": "0001628280-26-029054:mdna:31",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_cloud_improved_pricing_environment",
  "what_changed": "MD&A attributes Cloud's increase in average selling price per exabyte to 'an improved pricing environment'. It attributes Cloud's volume to demand for high-capacity enterprise products. Cloud is stated as 89% of revenue. Pricing is a market condition, and the prose does not say whether it will last.",
  "account": "Revenue, net (Cloud)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The increase in average selling price per exabyte was due to an improved pricing environment.",
  "paragraph_id": "0001628280-26-029054:mdna:32",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_client_end_market_volume_and_price",
  "what_changed": "MD&A says Client revenue rose on both exabytes and average selling price. It says the drivers are 'dynamics largely consistent with our other end markets'. The prior wording is not in this input.",
  "account": "Revenue, net (Client)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Client revenue, representing 5% of total revenue, increased by 31% for the three months ended April 3, 2026 from the comparable period in the prior year, driven by a 19% increase in exabytes sold and a 10% increase in average selling price per exabyte.",
  "paragraph_id": "0001628280-26-029054:mdna:33",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_consumer_end_market_volume_and_price",
  "what_changed": "MD&A says Consumer revenue rose for the quarter on both exabytes and average selling price, with dynamics 'largely consistent with our other end markets'. It also gives nine-month figures. The prior wording is not in this input.",
  "account": "Revenue, net (Consumer)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Consumer revenue, representing 6% of total revenue, increased by 24% for the three months ended April 3, 2026 from the comparable period in the prior year, driven by a 6% increase in exabytes sold and a 17% increase in average selling price per exabyte.",
  "paragraph_id": "0001628280-26-029054:mdna:34",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_geographic_mix_data_center_ramp",
  "what_changed": "MD&A explains the shift in geographic revenue mix toward Asia and Europe, Middle East and Africa by customers ramping up data center capacity in those regions. The prior wording is not in this input.",
  "account": "Revenue by geography (Asia; Europe, Middle East and Africa)",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "reflects larger percentage increases in the Asia and Europe, Middle East and Africa regions as customers are ramping up data center capacity in these regions",
  "paragraph_id": "0001628280-26-029054:mdna:35",
  "explanation": false }
```

```json
{ "id": "revenue_recognition_customer_concentration_three_large_customers",
  "what_changed": "Revenue concentration is restated. The top 10 customers are stated as 71% of revenue for the quarter and 74% for nine months. Three customers each passed 10% in both current periods (17%, 15% and 11% for the quarter). The prose says the comparative nine-month period had two such customers. The amounts are rolled forward with no direction word. MD&A repeats this (mdna:36).",
  "account": "Revenue, net (customer concentration)",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "three customers accounted for 17%, 15%, and 11%, respectively",
  "paragraph_id": "0001628280-26-029054:notes:19",
  "explanation": false }
```

```json
{ "id": "estimates_and_discretion_receivables_concentration_and_credit_reserve_not_material",
  "what_changed": "Net accounts receivable are stated as $1.89 billion at April 3, 2026 and $1.49 billion at June 27, 2025. Reserves for potential credit losses are called 'not material'. Two customers hold 28% and 12% of net receivables at April 3, 2026; three customers held 20%, 19% and 12% at June 27, 2025. This paragraph gives no cause; MD&A's cash-flow paragraph gives one (see the receivables cash-flow item). Calling the credit reserve not material is a judgment made while one customer holds a stated 28% of receivables.",
  "account": "Accounts receivable, net; allowance for credit losses",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "As of April 3, 2026, two customers accounted for 28% and 12%, respectively",
  "paragraph_id": "0001628280-26-029054:notes:20",
  "explanation": false }
```

```json
{ "id": "earnings_quality_gross_margin_cost_structure_and_pricing",
  "what_changed": "MD&A attributes the gross margin increase to a lower cost structure on newer-generation products and to improved pricing. It also attributes the gross profit increase to shipment volume. The prior wording is not in this input.",
  "account": "Gross profit; gross margin",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "Gross margin increased by 10 percentage points year over year, primarily due to a lower cost structure on our newer generation products and improved pricing.",
  "paragraph_id": "0001628280-26-029054:mdna:38",
  "explanation": false }
```

```json
{ "id": "earnings_quality_research_development_performance_compensation_and_roadmap",
  "what_changed": "MD&A attributes the R&D increase to product development costs ($25 million for the quarter) and to compensation costs ($20 million) 'aligned with the improved financial performance'. For the nine months it gives $95 million of compensation and $50 million of product development. The prose ties part of R&D to variable, performance-linked pay.",
  "account": "Research and development",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "$20 million higher compensation-related costs aligned with the improved financial performance during the current year",
  "paragraph_id": "0001628280-26-029054:mdna:41",
  "explanation": false }
```

```json
{ "id": "earnings_quality_selling_general_administrative_performance_compensation",
  "what_changed": "MD&A attributes the quarter's SG&A increase to compensation driven by improved financial performance. It attributes the nine-month decrease to Separation costs in the comparative period: duplicate personnel costs and outside service fees.",
  "account": "Selling, general and administrative",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "The increase was primarily attributable to higher compensation-related expense, as a result of our improved financial performance.",
  "paragraph_id": "0001628280-26-029054:mdna:42",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_inventory_reduction_from_increased_shipments",
  "what_changed": "MD&A explains part of the year-over-year improvement in operating cash flow as 'a $365 million reduction in inventory as a result of increased shipments to customers'. The prose does not say over what interval that reduction is measured. Checking it against the inventory balances in notes:36 is for the numbers reader.",
  "account": "Inventories",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "a $365 million reduction in inventory as a result of increased shipments to customers",
  "paragraph_id": "0001628280-26-029054:mdna:65",
  "explanation": true }
```

```json
{ "id": "liquidity_and_capital_receivables_increase_from_business_volume",
  "what_changed": "MD&A attributes 'a $504 million increase in accounts receivable' to growth in business volume. It names no other cause, such as payment terms, timing or collections. Notes:20 gives the receivable balances and concentration (see the receivables concentration item).",
  "account": "Accounts receivable, net",
  "expected_direction": "up",
  "horizon": "this quarter",
  "quote": "These were partially offset by a $504 million increase in accounts receivable driven by the growth in our business volume",
  "paragraph_id": "0001628280-26-029054:mdna:65",
  "explanation": true }
```

```json
{ "id": "liquidity_and_capital_income_taxes_receivable_timing",
  "what_changed": "MD&A attributes part of the operating cash-flow improvement to the timing of recognition and realization of income taxes receivable. It partly offsets this with 'a $518 million increase in cash used driven by the timing of recognition and payment of income taxes'. The prose describes both as timing effects.",
  "account": "Income taxes receivable",
  "expected_direction": "down",
  "horizon": "this quarter",
  "quote": "a $883 million improvement in other assets and liabilities driven by the timing of recognition and realization of income taxes receivable",
  "paragraph_id": "0001628280-26-029054:mdna:65",
  "explanation": true }
```

```json
{ "id": "liquidity_and_capital_accrued_expenses_reduced_hedging_activity",
  "what_changed": "MD&A attributes a cash-flow improvement from accrued expenses to 'a significant reduction in our derivative hedging activities since the Separation'. So the company now does less hedging. The AOCI note (notes:54) still shows net cash flow hedge losses waiting to be reclassified into earnings.",
  "account": "Accrued expenses",
  "expected_direction": "none",
  "horizon": "this quarter",
  "quote": "a $345 million improvement from accrued expenses resulting from a significant reduction in our derivative hedging activities since the Separation",
  "paragraph_id": "0001628280-26-029054:mdna:65",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_accrued_compensation_variable_pay_timing",
  "what_changed": "MD&A attributes a cash-flow improvement from accrued compensation to the amount and timing of variable compensation payments. This is consistent with the performance-pay explanations given for R&D and SG&A. Because the prose describes it as timing, paying that compensation would be a later use of cash; the prose does not say when.",
  "account": "Accrued compensation",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "a $225 million improvement from accrued compensation resulting from amount and timing of payment of variable compensation",
  "paragraph_id": "0001628280-26-029054:mdna:65",
  "explanation": false }
```

```json
{ "id": "earnings_quality_cash_flow_hedge_losses_reclassified_within_twelve_months",
  "what_changed": "The AOCI note says all existing net losses on cash flow hedges are expected to be reclassified into earnings within twelve months. Notes:53 says this period's reclassifications were losses charged mainly to Cost of revenue. The prior wording is not in this input, so it cannot be established whether earlier text described gains.",
  "account": "Cost of revenue",
  "expected_direction": "up",
  "horizon": "12 months",
  "quote": "all existing net losses related to cash flow hedges recorded in Accumulated other comprehensive income are expected to be reclassified to earnings within the next twelve months",
  "paragraph_id": "0001628280-26-029054:notes:54",
  "explanation": false }
```

```json
{ "id": "liquidity_and_capital_capital_expenditure_range_of_net_revenue",
  "what_changed": "This paragraph is marked as changed. It now says capital expenditures are expected to be 'generally' about 4% to 6% of net revenue, with no period attached. The prior wording is not in this input. MD&A states nine-month capex as $310 million (mdna:67); setting that against the range is for the numbers reader.",
  "account": "Capital expenditures",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "We expect our capital expenditures generally to be approximately 4% to 6% of our net revenue.",
  "paragraph_id": "0001628280-26-029054:mdna:60",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_chief_executive_trading_plan_adopted",
  "what_changed": "New disclosure. The Chief Executive Officer, Irving Tan, adopted a Rule 10b5-1 plan on February 5, 2026. It allows sales of up to 80,000 shares before it expires on May 31, 2027.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Irving Tan, Chief Executive Officer of the Company, adopted a Rule 10b5-1 Plan on February 5, 2026.",
  "paragraph_id": "0001628280-26-029054:notes:157",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_director_trading_plan_adopted",
  "what_changed": "New disclosure. Director Martin I. Cole adopted a Rule 10b5-1 plan on March 5, 2026. It allows sales of up to 12,000 shares before it expires on October 31, 2026.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Martin I. Cole, a director of the Company, adopted a Rule 10b5-1 Plan on March 5, 2026.",
  "paragraph_id": "0001628280-26-029054:notes:156",
  "explanation": false }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_chief_legal_officer_trading_plan_adopted",
  "what_changed": "New disclosure. Cynthia Tregillis, the Executive Vice President, Chief Legal Officer and Secretary, adopted a Rule 10b5-1 plan on March 6, 2026. It allows sales of up to 27,765 shares before it expires on December 31, 2027.",
  "account": "none",
  "expected_direction": "none",
  "horizon": "12 months",
  "quote": "Cynthia Tregillis, Executive Vice President, Chief Legal Officer and Secretary of the Company, adopted a Rule 10b5-1 Plan on March 6, 2026.",
  "paragraph_id": "0001628280-26-029054:notes:158",
  "explanation": false }
```

## Insufficient

- **insufficient: 8-K item bodies.** No 8-K body is in the input; only the item codes are listed. The 8-Ks after the prior 10-Q (2026-01-30) are:
  - 2026-02-09: 8.01
  - 2026-02-18: 3.03
  - 2026-02-24: 5.03, 8.01, 9.01
  - 2026-04-30: 2.02, 9.01

  None of them can be read or quoted.
- **insufficient: results_against_expectations.** No earnings release, guidance or outlook text is in the input; the 2026-04-30 item 2.02 body is absent. Results cannot be compared with any stated expectation.
- **insufficient: auditor's report.** The controls file carries only Item 4; no auditor's or review report is present.
- **insufficient: Item 1A diff.** It is not in the input, although mdna:61 cites risk factors in Part II, Item 1A of this 10-Q.
- **insufficient: Exhibit 21 diff and Exhibit 10.** Neither is in the input, and no Exhibit 10 was pulled.

## Paragraphs read and not itemized

### Item 4 (controls)
- 0001628280-26-029054:item_4_controls:1 — heading
- 0001628280-26-029054:item_4_controls:2 — heading
- 0001628280-26-029054:item_4_controls:3 — standard conclusion that disclosure controls are effective; no change in substance
- 0001628280-26-029054:item_4_controls:4 — heading
- 0001628280-26-029054:item_4_controls:5 — no change in internal control over financial reporting; quarter-end date rolled forward
- 0001628280-26-029054:item_4_controls:6 — page number

### MD&A
- 0001628280-26-029054:mdna:4 — business description; wording only (edit not identifiable without prior text; matches the notes:1 wording edits)
- 0001628280-26-029054:mdna:5 — end-market description; wording only
- 0001628280-26-029054:mdna:8 — heading now adds 'Monetization of Sandisk Shares'; substance in liquidity_and_capital_remaining_sandisk_stake_to_be_exchanged_for_own_shares
- 0001628280-26-029054:mdna:9 — same changes as liquidity_and_capital_senior_notes_and_term_loan_retired_through_sandisk_exchange and liquidity_and_capital_remaining_sandisk_stake_to_be_exchanged_for_own_shares; 'approximately $800 million' against the note's '$800 million' is wording
- 0001628280-26-029054:mdna:11 — heading of the new section; substance in structure_and_disclosure_changes_preferred_shares_mandatory_conversion
- 0001628280-26-029054:mdna:12 — same change as structure_and_disclosure_changes_preferred_shares_mandatory_conversion (notes:137)
- 0001628280-26-029054:mdna:15 — tariffs; date rolled forward ('through the third quarter of 2026')
- 0001628280-26-029054:mdna:16 — page number
- 0001628280-26-029054:mdna:18 — heading; date rolled forward
- 0001628280-26-029054:mdna:20 — three-month results table; amounts only (the new caption is covered by earnings_quality_debt_for_equity_exchange_discount_driven_by_sandisk_volatility)
- 0001628280-26-029054:mdna:23 — nine-month results table; amounts only
- 0001628280-26-029054:mdna:26 — revenue by end market and geography table; amounts only (duplicates notes:17)
- 0001628280-26-029054:mdna:28 — page number
- 0001628280-26-029054:mdna:29 — heading; dates rolled forward
- 0001628280-26-029054:mdna:36 — same change as revenue_recognition_customer_concentration_three_large_customers (notes:19)
- 0001628280-26-029054:mdna:43 — cross-reference to the legal note; no substance
- 0001628280-26-029054:mdna:51 — table lead-in; wording
- 0001628280-26-029054:mdna:52 — tax table; amounts only
- 0001628280-26-029054:mdna:53 — same change as estimates_and_discretion_effective_tax_rate_drivers_include_tax_free_sandisk_gain (notes:98)
- 0001628280-26-029054:mdna:54 — same change as earnings_quality_comparative_period_one_time_deferred_tax_benefit (notes:99)
- 0001628280-26-029054:mdna:55 — page number
- 0001628280-26-029054:mdna:58 — cash flow summary table; amounts only
- 0001628280-26-029054:mdna:62 — cash held by foreign subsidiaries; amounts only
- 0001628280-26-029054:mdna:67 — investing activities; amounts only
- 0001628280-26-029054:mdna:72 — page number
- 0001628280-26-029054:mdna:75 — cash requirements lead-in; date rolled forward
- 0001628280-26-029054:mdna:76 — cash requirements table; amounts only
- 0001628280-26-029054:mdna:78 — same change as estimates_and_discretion_unrecognized_tax_benefits_near_term_cash_payments (notes:104)
- 0001628280-26-029054:mdna:79 — heading
- 0001628280-26-029054:mdna:80 — cross-reference to the legal note; no substance
- 0001628280-26-029054:mdna:82 — dividends paid; amounts only
- 0001628280-26-029054:mdna:83 — same change as related_parties_contingencies_and_subsequent_events_dividend_declared_after_quarter_end (notes:142)
- 0001628280-26-029054:mdna:86 — same change as structure_and_disclosure_changes_convertible_conversion_price_and_capped_call_terms_restated (notes:74)
- 0001628280-26-029054:mdna:87 — same change as liquidity_and_capital_tendered_convertible_notes_cash_settlement_election (notes:75)
- 0001628280-26-029054:mdna:88 — same change as articulation_and_the_filed_history_convertible_notes_current_in_each_quarter (notes:76)
- 0001628280-26-029054:mdna:93 — summarized guarantor balance sheet; amounts only
- 0001628280-26-029054:mdna:95 — summarized guarantor operations; amounts only
- 0001628280-26-029054:mdna:97 — guarantor intercompany amounts; amounts only

### Notes
- 0001628280-26-029054:notes:1 — wording only (adds 'WD'; shortens 'hard disk drives (HDD)' to 'HDD')
- 0001628280-26-029054:notes:2 — wording only (quotation marks around end-market names)
- 0001628280-26-029054:notes:3 — wording only (where the 2025 Form 10-K is defined)
- 0001628280-26-029054:notes:4 — date rolled forward; 'Flash business' becomes 'former Flash business'
- 0001628280-26-029054:notes:9 — heading
- 0001628280-26-029054:notes:10 — ASU 2025-10, effective for the year beginning June 30, 2029; prior text not in input; no substantive change identifiable
- 0001628280-26-029054:notes:11 — ASU 2025-09, effective for the year beginning July 3, 2027; under assessment; no substantive change identifiable
- 0001628280-26-029054:notes:12 — ASU 2025-07, effective for the year beginning July 3, 2027; no material impact expected; no substantive change identifiable
- 0001628280-26-029054:notes:13 — ASU 2025-06, effective for the year beginning July 1, 2028; under assessment; no substantive change identifiable
- 0001628280-26-029054:notes:14 — ASU 2024-03, adoption planned in the annual report for the year ending June 30, 2028; no substantive change identifiable
- 0001628280-26-029054:notes:17 — revenue table; amounts only (the note history shows only amounts and period labels changed)
- 0001628280-26-029054:notes:21 — 'Segment Reporting' heading moved here from the organization note; reordered
- 0001628280-26-029054:notes:22 — CODM paragraph moved here; wording only (names Irving Tan; 'devices and solutions'; 'one reportable segment: HDD')
- 0001628280-26-029054:notes:24 — segment expense table; amounts only
- 0001628280-26-029054:notes:27 — discontinued operations description; wording only ('initially 19.9%')
- 0001628280-26-029054:notes:28 — table lead-in; dates rolled forward
- 0001628280-26-029054:notes:29 — discontinued operations table; amounts only
- 0001628280-26-029054:notes:31 — discontinued operations cash flow table; amounts only
- 0001628280-26-029054:notes:33 — transition services agreements, stated as immaterial; no substantive change identifiable
- 0001628280-26-029054:notes:36 — inventory table; amounts only
- 0001628280-26-029054:notes:38 — property, plant and equipment table; amounts only
- 0001628280-26-029054:notes:40 — other non-current assets table; amounts only
- 0001628280-26-029054:notes:43 — warranty rollforward; amounts only
- 0001628280-26-029054:notes:45 — warranty current and long-term split; amounts only
- 0001628280-26-029054:notes:47 — other liabilities table; amounts only
- 0001628280-26-029054:notes:49 — goodwill; dates rolled forward; still no impairment indicators
- 0001628280-26-029054:notes:52 — AOCI rollforward; amounts only
- 0001628280-26-029054:notes:53 — this period's reclassified hedge losses charged to Cost of revenue; historical companion to earnings_quality_cash_flow_hedge_losses_reclassified_within_twelve_months
- 0001628280-26-029054:notes:60 — fair value basis for the Sandisk interest; wording only
- 0001628280-26-029054:notes:62 — fair value hierarchy table; amounts only
- 0001628280-26-029054:notes:66 — fair value lead-in; dates rolled forward
- 0001628280-26-029054:notes:67 — carrying and fair value table; amounts only
- 0001628280-26-029054:notes:68 — heading
- 0001628280-26-029054:notes:69 — debt table; amounts only
- 0001628280-26-029054:notes:71 — revolver availability and letters of credit; date rolled forward
- 0001628280-26-029054:notes:72 — covenant compliance; date rolled forward; the Loan Agreement redefinition is covered in liquidity_and_capital_senior_notes_and_term_loan_retired_through_sandisk_exchange
- 0001628280-26-029054:notes:73 — convertible notes outstanding; date rolled forward
- 0001628280-26-029054:notes:77 — restates the June 2025 trigger history from the removed prior paragraph; reordered
- 0001628280-26-029054:notes:78 — optional-redemption sentence split out of the conversion paragraph; reordered
- 0001628280-26-029054:notes:79 — capped call strike and cap restated; amounts only; covered in structure_and_disclosure_changes_convertible_conversion_price_and_capped_call_terms_restated
- 0001628280-26-029054:notes:83 — lease balances table; amounts only
- 0001628280-26-029054:notes:85 — lease cost table; amounts only
- 0001628280-26-029054:notes:87 — lease term and discount rate; amounts only
- 0001628280-26-029054:notes:88 — table lead-in; date rolled forward
- 0001628280-26-029054:notes:89 — lease maturity table; amounts only
- 0001628280-26-029054:notes:91 — purchase commitments description; date rolled forward
- 0001628280-26-029054:notes:92 — commitments table; amounts only
- 0001628280-26-029054:notes:96 — table lead-in; wording
- 0001628280-26-029054:notes:97 — tax table; amounts only
- 0001628280-26-029054:notes:102 — lead-in to the unrecognized tax benefits rollforward; date rolled forward
- 0001628280-26-029054:notes:103 — unrecognized tax benefits rollforward table; amounts only
- 0001628280-26-029054:notes:108 — business realignment charges table; amounts only
- 0001628280-26-029054:notes:110 — reserve table lead-in; date rolled forward
- 0001628280-26-029054:notes:111 — realignment reserve rollforward; amounts only
- 0001628280-26-029054:notes:115 — pension funded status table; amounts only
- 0001628280-26-029054:notes:117 — pension balance sheet table; amounts only
- 0001628280-26-029054:notes:118 — net periodic benefit cost immaterial; dates rolled forward
- 0001628280-26-029054:notes:121 — stock-based compensation by award type table; amounts only
- 0001628280-26-029054:notes:122 — stock-based compensation by line item table; amounts only
- 0001628280-26-029054:notes:124 — table lead-in; date rolled forward
- 0001628280-26-029054:notes:125 — unamortized compensation table; amounts only
- 0001628280-26-029054:notes:130 — RSU and PSU activity table; amounts only
- 0001628280-26-029054:notes:132 — heading
- 0001628280-26-029054:notes:133 — common stock authorized, issued and outstanding; amounts only
- 0001628280-26-029054:notes:135 — preferred stock history now in the past tense; covered by structure_and_disclosure_changes_preferred_shares_mandatory_conversion
- 0001628280-26-029054:notes:136 — preferred dividend terms now in the past tense ($8 million paid in cash); covered by structure_and_disclosure_changes_preferred_shares_mandatory_conversion
- 0001628280-26-029054:notes:141 — dividends paid; amounts only
- 0001628280-26-029054:notes:145 — EPS table; amounts only
- 0001628280-26-029054:notes:148 — potentially dilutive shares; dates rolled forward
- 0001628280-26-029054:notes:149 — heading
- 0001628280-26-029054:notes:150 — SPEX; only the as-of date rolled forward (confirmed by the note change history)
- 0001628280-26-029054:notes:153 — heading
- 0001628280-26-029054:notes:154 — other legal matters boilerplate; wording only
- 0001628280-26-029054:notes:155 — boilerplate; wording only

### 8-K
- No 8-K paragraphs are carried as text (item codes only); see Insufficient.

### Note change history
- The current history paragraphs (0001628280-26-029054:note_history:1 to :20 and :24 to :25) are the same text as the notes paragraphs above and are accounted for through them.
- Removed prior paragraphs:
  - 0001628280-26-004207:note_history:8 and :9 — segment heading and CODM paragraph; moved to notes:21 and notes:22
  - 0001628280-26-004207:note_history:21 — itemized as articulation_and_the_filed_history_prior_stated_intent_to_redeem_notes_carried_out
  - 0001628280-26-004207:note_history:22 — Term Loan A-3 interest rate; removed because the loan was retired; covered in liquidity_and_capital_senior_notes_and_term_loan_retired_through_sandisk_exchange
  - 0001628280-26-004207:note_history:23 — prior conversion-trigger paragraph; replaced by notes:76 and notes:77
