# QCOM: notes and text reader report for 10-Q 0000804328-26-000086 (third quarter fiscal 2026)

## Scope and input check

Files read in full: input_notes.md, input_notes_history.md, input_mdna.md, input_controls.md, input_8k.md, input_prior_predictions.md.

- **Forbidden content:** none found. The directory holds no trend table, prices, abnormal returns, short interest, other-company files, prior-run probabilities or outcome window. The 8-K exhibit 99.1 includes the release's own condensed statements. These are part of the 8-K body, and no figures were compared.
- **Prior predictions:** none on record. No prior flags carry forward.
- **Sections absent from the input:**
  - There is no auditor's report, no Item 1A diff, no Exhibit 21 diff and no Exhibit 10. MD&A paragraph mdna:121 cites a risk factor in this Quarterly Report, but no Item 1A diff text was provided.
  - The 8-K index lists an Item 3.02 filing dated 2026-06-24 (0001104659-26-077071), but its body is not in the input.
- **Prior text:**
  - For changed MD&A paragraphs, the prior text is not in the input. Only the notes have a change history. Where an MD&A paragraph is carried as changed and the change cannot be identified, the item or the accounting line says so.
  - No prose in the input explains the cause of a movement in accounts receivable.
- **Arithmetic:** none performed. Directions below are what the prose implies. Amounts are reported only as stated.

## Items

```json
[
  {
    "id": "structure_and_disclosure_changes_income_tax_disclosure_prospective_adoption",
    "what_changed": "The note now commits to a transition method. The company will adopt the FASB annual income tax disclosure requirements (rate reconciliation, income taxes paid) for annual periods starting in fiscal 2026 on a prospective basis. The prior 10-Q said only that they could be applied on a retrospective or prospective basis. With prospective adoption, earlier years' tax disclosures will not be recast into the new format.",
    "account": "income tax disclosures (effective tax rate reconciliation; income taxes paid)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "We will adopt the new requirements for our annual periods starting in fiscal 2026 on a prospective basis.",
    "paragraph_id": "0000804328-26-000086:notes:6",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_capacity_purchase_advance_payments_restated",
    "what_changed": "The note restates advance payments under multi-year capacity purchase commitments at the new balance-sheet date: $769 million at June 28, 2026 and $1.9 billion at September 28, 2025. The current/noncurrent split is $195 million and $1.5 billion in other current assets, and $574 million and $357 million in other assets. The note gives no cause. MD&A (mdna:135) attributes the decrease in other assets to utilization of prior advanced supply agreement payments. The movement between the two dates is for the numbers reader.",
    "account": "other current assets; other assets (supplier capacity advance payments)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Total advance payments related to multi-year capacity purchase commitments recorded on our condensed consolidated balance sheets at June 28, 2026 and September 28, 2025 were $769 million and $1.9 billion, respectively",
    "paragraph_id": "0000804328-26-000086:notes:10",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_short_term_debt_schedule_added",
    "what_changed": "A short-term debt schedule appears for the first time (note history: added, no prior note). At June 28, 2026 it shows commercial paper of $498 million and a current portion of long-term debt of $1,991 million. Both lines show a dash at September 28, 2025. MD&A (mdna:131) says $2.0 billion of debt is classified as current and matures in May 2027.",
    "account": "short-term debt (commercial paper; current portion of long-term debt)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Current portion of long-term debt | 1,991",
    "paragraph_id": "0000804328-26-000086:notes:12",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_interest_rate_swap_notional_fair_value_hedges",
    "what_changed": "The note now gives the aggregate notional of interest rate swaps designated as fair value hedges as $5.0 billion at June 28, 2026 and $3.6 billion at September 28, 2025. These swaps convert fixed-rate payments to floating on part of long-term debt; the prior 10-Q gave the March 29, 2026 figure. The prose ties interest expense on the swapped portion to floating rates. Whether notional changed within the quarter is for the numbers reader.",
    "account": "interest expense; long-term debt (fair value hedge basis); derivative instruments",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "we had outstanding interest rate swaps with an aggregate notional amount of $5.0 billion and $3.6 billion, respectively, that are designated as fair value hedges",
    "paragraph_id": "0000804328-26-000086:notes:13",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_iot_revenue_category_redefinition",
    "what_changed": "The IoT revenue footnote has been redefined.\n- Before: consumer (PCs, XR, other personal computing), edge networking (mobile broadband, wireless access points) and industrial (handhelds, retail, tracking and logistics, utilities).\n- Now: 'personal AI and compute' and 'industrial, networking and robotics'. Robotics and 'other commercial and home applications' are added, and utilities is no longer named.\nThe IoT line's content is described differently, which affects comparability of the IoT stream.",
    "account": "QCT IoT revenues (disaggregation)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "personal AI and compute (including personal computers (PCs), extended reality (XR) and other personal computing devices) and industrial, networking and robotics",
    "paragraph_id": "0000804328-26-000086:notes:19",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_segment_description_iot_relabel_and_data_center",
    "what_changed": "The segment note's description of QCT now describes IoT as 'personal AI and compute devices and industrial, networking and robotics products', the same relabeling as the revenue footnote. It names QSI as a reportable segment and QGOV and the Data Center business as nonreportable segments. The paragraph is carried as changed, but its prior text is not in the input, so I can't confirm whether the Data Center wording is also new.",
    "account": "segment reporting (QCT description; nonreportable segments)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "IoT including personal AI and compute devices and industrial, networking and robotics products",
    "paragraph_id": "0000804328-26-000086:notes:49",
    "explanation": false
  },
  {
    "id": "revenue_recognition_key_oem_license_expiry_window",
    "what_changed": "The remaining-performance-obligations paragraph is carried as changed. It now says patent license agreements with key OEMs have remaining terms expiring between fiscal 2027 and 2031, and that the company generally seeks to renew or renegotiate before expiration. The prior wording is not in the input, so whether the expiry window moved is unknown. The earliest stated expiry year is fiscal 2027, which puts license renewals within the forecast horizon.",
    "account": "licensing revenues (QTL); unearned revenues",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Our patent license agreements with key OEMs are generally long-term, with remaining terms expiring between fiscal 2027 and 2031.",
    "paragraph_id": "0000804328-26-000086:notes:22",
    "explanation": false
  },
  {
    "id": "earnings_quality_restructuring_severance_charges_in_other_expense",
    "what_changed": "The note now says other expenses were $68 million for the quarter and $97 million for nine months, consisting of restructuring and restructuring-related charges, substantially all severance. Restructuring charges continued in the third quarter. The MD&A other-expense table shows a dash for the year-ago quarter. These charges are excluded from non-GAAP results.",
    "account": "other expenses (restructuring); operating expenses",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Other expenses in the three months and nine months ended June 28, 2026 consisted of $68 million and $97 million in restructuring and restructuring-related charges (substantially all of which related to severance costs), respectively.",
    "paragraph_id": "0000804328-26-000086:notes:26",
    "explanation": false
  },
  {
    "id": "earnings_quality_marketable_securities_gains_mostly_unrealized",
    "what_changed": "A new footnote to the investment and other income table says net gains on marketable securities are primarily net unrealized gains on certain marketable equity securities. The quarter's gain is mostly mark-to-market, not realized, so it can reverse with the investees' share prices.",
    "account": "investment and other income, net (net gains on marketable securities)",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "Primarily consist of net unrealized gains related to certain marketable equity securities.",
    "paragraph_id": "0000804328-26-000086:notes:28",
    "explanation": false
  },
  {
    "id": "earnings_quality_ipo_equity_securities_under_lock_up",
    "what_changed": "A new fair-value footnote says the Level 1 equity securities are primarily shares in QSI investees that completed IPOs. These shares remain under short-term lock-up restrictions on sale, so the gains above sit on positions that cannot yet be sold.",
    "account": "marketable securities (equity securities); investment and other income, net",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "Primarily consists of equity securities in certain QSI investees that have completed initial public offerings, which remain subject to short-term lock-up restrictions on the ability to sell.",
    "paragraph_id": "0000804328-26-000086:notes:60",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_annual_effective_tax_rate_estimate",
    "what_changed": "The tax paragraph is carried as changed and now states:\n- the estimated fiscal 2026 annual effective tax rate is a 40% benefit, driven by the $5.7 billion second-quarter valuation allowance release;\n- the third-quarter rate was 19%, which the company calls higher than the annual estimate;\n- the year-ago quarter's 10% reflected net discrete tax benefits.\nThe prior estimate wording is not in the input.",
    "account": "income tax expense (benefit); effective tax rate",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "We estimate our annual effective income tax rate to be 40% benefit for fiscal 2026",
    "paragraph_id": "0000804328-26-000086:notes:32",
    "explanation": false
  },
  {
    "id": "earnings_quality_fddei_benefit_reduced_by_research_expensing",
    "what_changed": "The tax note says FDDEI benefits for fiscal 2026 will be reduced compared to fiscal 2025, because domestic R&D is now deducted currently under OBBB. It also says cash flows benefit from significantly lower cash tax payments. The paragraph is carried as changed, but the prior text is not in the input, so whether this sentence is new is uncertain. The prose implies a smaller FDDEI rate benefit in the book tax provision.",
    "account": "income tax expense (FDDEI benefit)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Such benefits from FDDEI for fiscal 2026 will be reduced compared to fiscal 2025 as a result of the current deduction of domestic R&D expenditures under OBBB.",
    "paragraph_id": "0000804328-26-000086:notes:32",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_parkervision_appeal_hearing_held",
    "what_changed": "The ParkerVision paragraph adds that the Federal Circuit held a hearing on June 1, 2026 on ParkerVision's appeal of the Receiver Claims non-infringement judgment. The prior text said only that ParkerVision had appealed. A decision is now pending, and the Transmitter Claims remain severed and stayed. The company still records no accrual (notes:46).",
    "account": "contingent liabilities (no accrual); legal expense",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "ParkerVision has appealed to the Federal Circuit, and a hearing on the appeal was held on June 1, 2026.",
    "paragraph_id": "0000804328-26-000086:notes:41",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_arm_good_faith_negotiation_claim_added",
    "what_changed": "A new sentence in Qualcomm v. Arm says that on March 30, 2026 the complaint against Arm Ltd. was amended. It adds a claim for breach of the Qualcomm ALA based on Arm's failure to negotiate certain license terms in good faith. Trial is still scheduled to begin October 5, 2026.",
    "account": "contingencies (Qualcomm as plaintiff; Arm license terms and costs)",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "On March 30, 2026, our complaint against Arm Ltd. was amended to include an additional claim for breach of the Qualcomm ALA based on Arm’s failure to negotiate certain license terms in good faith.",
    "paragraph_id": "0000804328-26-000086:notes:44",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_arm_motion_to_strike_denied",
    "what_changed": "A new sentence reports a post-quarter ruling: on July 14, 2026 the court denied Arm's motion to strike Qualcomm's amended complaint against Arm Ltd. This leaves the added claim in the case ahead of the October 5, 2026 trial date.",
    "account": "contingencies (Qualcomm as plaintiff)",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "The court denied Arm’s motion to strike our amended complaint against Arm Ltd. on July 14, 2026.",
    "paragraph_id": "0000804328-26-000086:notes:44",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_arm_motion_to_dismiss_sentence_removed",
    "what_changed": "The prior 10-Q sentence saying Arm had moved to dismiss Qualcomm's amended complaint is gone from the current paragraph. The current text does not say how that motion was resolved; it reports only the denial of a motion to strike (separate item).",
    "account": "contingencies (Qualcomm as plaintiff)",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "Arm has moved to dismiss our amended complaint.",
    "paragraph_id": "0000804328-26-000061:note_history:4",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_modular_acquisition_completed",
    "what_changed": "New subsequent-event disclosure: the Modular Inc acquisition was completed on July 28, 2026, after quarter end. It is valued at about $3.1 billion on the closing share price, and consideration was primarily 18 million newly issued common shares. The company says it is not practicable to disclose the preliminary purchase price allocation yet. Acquired goodwill and intangibles, and the added shares, should appear from the fourth quarter. The release headline (8k_2_02:14) reports the same completion.",
    "account": "goodwill; other intangible assets; common shares outstanding",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "The transaction values Modular at approximately $3.1 billion based on the closing price of Qualcomm stock on the acquisition date, with consideration transferred consisting primarily of 18 million shares issued of our common stock.",
    "paragraph_id": "0000804328-26-000086:notes:75",
    "explanation": false
  },
  {
    "id": "earnings_quality_modular_executive_shares_compensation_expense",
    "what_changed": "Of the Modular shares, 4 million (fair value about $700 million) went to certain executives with a four-year post-acquisition service requirement. A portion of their value will be recognized as compensation expense and the rest included in purchase price; the split is not given. This adds future share-based compensation, as the Alphawave exchangeable shares did (notes:69).",
    "account": "share-based compensation expense (R&D / SG&A)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "This included 4 million shares with an estimated fair value of approximately $700 million that were issued to certain executives and are subject to a four-year service requirement post-acquisition",
    "paragraph_id": "0000804328-26-000086:notes:75",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_seven_other_businesses_acquired",
    "what_changed": "The note now says seven other businesses were acquired in the first nine months for a total accounting purchase price of $1.1 billion. Acquired assets were primarily $295 million of intangibles and $737 million of goodwill: $661 million to QCT and $76 million to the Data Center operating segment. The goodwill is attributed to assembled workforce and synergies. The prior six-month wording, including the count, is not in the input.",
    "account": "goodwill; other intangible assets",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "During the first nine months of fiscal 2026, we acquired seven other businesses for a total accounting purchase price of $1.1 billion.",
    "paragraph_id": "0000804328-26-000086:notes:76",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_alphawave_purchase_price_allocation_table_revised",
    "what_changed": "The Alphawave preliminary purchase price allocation table is carried as changed from the prior 10-Q. That indicates a measurement-period revision to at least one line, or possibly a reformat. No prose in the input describes or explains a measurement-period adjustment. Which line moved is for the numbers reader.",
    "account": "goodwill; intangible assets; IPR&D; other assets and liabilities (Alphawave)",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Goodwill | 2,210",
    "paragraph_id": "0000804328-26-000086:notes:71",
    "explanation": false
  },
  {
    "id": "earnings_quality_qsi_ipo_gains_drive_investment_income",
    "what_changed": "The MD&A overview attributes the quarter's $656 million increase in investment and other income, net mainly to higher net gains from IPOs of certain QSI equity investments. The same driver is given in mdna:58, mdna:112 and mdna:114. These gains are non-operating, sit in QSI, and are excluded from non-GAAP.",
    "account": "investment and other income, net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Investment and other income, net increased by $656 million compared to the year ago quarter, primarily due to higher net gains from initial public offerings of certain QSI equity investments.",
    "paragraph_id": "0000804328-26-000086:mdna:8",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_qct_handset_revenue_decline",
    "what_changed": "The overview says QCT revenues fell 5% year over year because of lower handset revenues, partly offset by automotive and IoT. The detailed handset-driver bullet (mdna:78) is carried unchanged from the prior 10-Q, and its text is not in the input.",
    "account": "QCT handset revenues; equipment and services revenues",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "QCT revenues decreased by 5% in the third quarter of fiscal 2026 compared to the year ago quarter due to lower handset revenues, partially offset by higher automotive and IoT revenues.",
    "paragraph_id": "0000804328-26-000086:mdna:6",
    "explanation": false
  },
  {
    "id": "earnings_quality_data_center_revenue_from_alphawave_acquisition",
    "what_changed": "The revenue bridge includes a Data Center line: $88 million higher in the quarter and $182 million higher for nine months (mdna:26). The prose says this came primarily from the first-quarter Alphawave acquisition, so the growth is acquired rather than organic.",
    "account": "equipment and services revenues (Data Center, nonreportable segment)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "$88 million in higher equipment and services revenues from our Data Center segment, primarily driven by our acquisition of Alphawave in the first quarter of fiscal 2026",
    "paragraph_id": "0000804328-26-000086:mdna:21",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_gross_margin_decline_from_qct",
    "what_changed": "MD&A says the gross margin percentage decreased in both the quarter and the nine months, primarily because QCT's gross margin percentage decreased. This matches the release's statement that higher input costs are reflected in third-quarter performance (8k_2_02:29).",
    "account": "gross margin; cost of revenues",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Gross margin percentage decreased in the third quarter and first nine months of fiscal 2026 primarily due to a decrease in QCT gross margin percentage.",
    "paragraph_id": "0000804328-26-000086:mdna:30",
    "explanation": false
  },
  {
    "id": "earnings_quality_lower_engineering_reimbursements_raise_research_spend",
    "what_changed": "The R&D bridge attributes a $244 million increase in the quarter (and $541 million for nine months, mdna:39) in development costs primarily to lower non-recurring engineering cost reimbursements for product-related development work. The nine-month bullet also cites higher employee-related expenses. Reported R&D rose partly because fewer customer reimbursements offset it, not only because gross spending grew.",
    "account": "research and development expense",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "primarily driven by lower non-recurring engineering cost reimbursements for product-related development work",
    "paragraph_id": "0000804328-26-000086:mdna:35",
    "explanation": false
  },
  {
    "id": "earnings_quality_share_based_compensation_named_as_expense_driver",
    "what_changed": "The expense bridges name share-based compensation increases as primary drivers. R&D: $101 million for the quarter and $269 million for nine months (mdna:40). SG&A: $62 million for the quarter (mdna:45) and $184 million for nine months (mdna:50). SBC is excluded from non-GAAP, and the release guides $0.72 of fourth-quarter EPS to it (8k_2_02:31).",
    "account": "share-based compensation (R&D; SG&A)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "$101 million increase in share-based compensation expense",
    "paragraph_id": "0000804328-26-000086:mdna:36",
    "explanation": false
  },
  {
    "id": "earnings_quality_sales_and_marketing_diversification_spend",
    "what_changed": "The SG&A bridge names a $27 million increase in the quarter (and $64 million for nine months, mdna:52) in sales and marketing expenses, including investments in growth and diversification initiatives.",
    "account": "selling, general and administrative expense",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "$27 million increase in sales and marketing expenses (including investments in growth and diversification initiatives)",
    "paragraph_id": "0000804328-26-000086:mdna:46",
    "explanation": false
  },
  {
    "id": "earnings_quality_deferred_compensation_revaluation_offset_in_investment_income",
    "what_changed": "The quarter's SG&A bridge cites $24 million from revaluing the deferred compensation obligation. Matching plan-asset gains are recorded in investment and other income, net. The release (8k_2_02:78) states $149 million of deferred-compensation losses in operating expenses offset by $149 million of plan-asset gains, all excluded from non-GAAP.",
    "account": "SG&A; investment and other income, net (deferred compensation plan assets)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "$24 million increase in expenses driven by the revaluation of our deferred compensation obligation",
    "paragraph_id": "0000804328-26-000086:mdna:47",
    "explanation": false
  },
  {
    "id": "earnings_quality_acquisition_related_expenses_named_as_driver",
    "what_changed": "The nine-month SG&A bridge names a $91 million increase in acquisition-related expenses as a primary driver. The release excludes $101 million of acquisition-related charges from third-quarter non-GAAP results (8k_2_02:78). It also guides fourth-quarter other items as primarily acquisition-related (8k_2_02:33), and Modular closed on July 28, 2026.",
    "account": "selling, general and administrative expense (acquisition-related)",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "$91 million increase in acquisition-related expenses",
    "paragraph_id": "0000804328-26-000086:mdna:51",
    "explanation": false
  },
  {
    "id": "earnings_quality_observable_price_change_gains_nonmarketable_investments",
    "what_changed": "MD&A attributes nine-month net gains on other investments primarily to observable price changes on certain QSI non-marketable equity investments. These are remeasurement gains under the measurement alternative, not realized sales.",
    "account": "investment and other income, net (net gains on other investments)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Net gains on other investments in the first nine months of fiscal 2026 was primarily driven by observable price changes on certain of our QSI non-marketable equity investments.",
    "paragraph_id": "0000804328-26-000086:mdna:59",
    "explanation": false
  },
  {
    "id": "earnings_quality_equity_method_investee_earnings_share",
    "what_changed": "MD&A attributes the nine-month increase in net earnings of investees to a larger share of earnings in certain QSI equity method investments.",
    "account": "investment and other income, net (equity in net earnings of investees)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase in net earnings of investees in the first nine months of fiscal 2026 was primarily driven by an increase in our share of earnings in certain QSI equity method investments.",
    "paragraph_id": "0000804328-26-000086:mdna:59",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_lower_interest_income_from_lower_balances",
    "what_changed": "MD&A attributes the nine-month decrease in interest and dividend income to lower balances of interest-bearing securities. The liquidity section (mdna:133) describes a net decrease in cash, cash equivalents and marketable securities, so the prose implies this continues while balances stay lower.",
    "account": "interest and dividend income",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "The decrease in interest and dividend income in the first nine months of fiscal 2026 was primarily due to lower balances of interest-bearing securities.",
    "paragraph_id": "0000804328-26-000086:mdna:59",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_unrecognized_tax_benefits_may_change",
    "what_changed": "MD&A now gives unrecognized tax benefits of $3.0 billion at June 28, 2026 and $2.7 billion at September 28, 2025. It says these benefits could reasonably change within twelve months, without saying in which direction. The paragraph is carried as changed and its prior wording is not in the input, so whether the twelve-month sentence is new is uncertain. No cause is given for the balances.",
    "account": "unrecognized tax benefits (tax reserves); income tax expense",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "We believe that it is reasonably possible that our unrecognized tax benefits will change within the next twelve months.",
    "paragraph_id": "0000804328-26-000086:mdna:68",
    "explanation": false
  },
  {
    "id": "earnings_quality_automotive_growth_price_mix_and_launches",
    "what_changed": "The quarter's QCT automotive growth is attributed to two drivers. $381 million came from higher revenue per unit (favorable mix and higher average selling prices). $223 million came from higher shipments, primarily new vehicle launches with Snapdragon digital cockpit and ADAS/AD. For nine months (mdna:87) the figures are $560 million and $551 million.",
    "account": "QCT automotive revenues",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "$381 million increase in revenues per unit driven by favorable mix and higher average selling prices and $223 million in higher shipments primarily from new vehicle launches",
    "paragraph_id": "0000804328-26-000086:mdna:79",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_qct_ebt_margin_decline",
    "what_changed": "MD&A says QCT EBT as a percentage of revenues decreased in the third quarter. The nine-month lead-in (mdna:89) says the same. The quarter's driver bullets (mdna:82, mdna:83) are carried unchanged from the prior 10-Q, and their text is not in the input.",
    "account": "QCT EBT; QCT EBT margin",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "QCT EBT as a percentage of revenues decreased in the third quarter of fiscal 2026 primarily due to:",
    "paragraph_id": "0000804328-26-000086:mdna:81",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_qct_lower_revenues_added_as_margin_driver",
    "what_changed": "The drivers of the lower nine-month QCT EBT margin now include a 'lower revenues' bullet. It is carried as new or changed text this period, while the neighbouring bullets are carried unchanged from the prior 10-Q.",
    "account": "QCT EBT; QCT revenues",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "lower revenues",
    "paragraph_id": "0000804328-26-000086:mdna:92",
    "explanation": false
  },
  {
    "id": "revenue_recognition_qtl_estimated_cellular_sales_decrease",
    "what_changed": "QTL's third-quarter decline is attributed first to a $67 million decrease in estimated sales of cellular products. QTL royalty revenue is recognized on estimates of licensees' device sales. The nine-month bridge (mdna:106) instead cites a $53 million increase in estimated sales.",
    "account": "licensing revenues (QTL)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "$67 million decrease in estimated sales of cellular products",
    "paragraph_id": "0000804328-26-000086:mdna:97",
    "explanation": false
  },
  {
    "id": "revenue_recognition_qtl_prior_period_royalties_lower",
    "what_changed": "The QTL bridge cites lower royalty revenue recognized for devices sold in prior periods: $25 million for the quarter and $65 million for nine months (mdna:107). Smaller catch-up or true-up revenue against earlier estimates is reducing QTL revenue. Notes:21 tables revenue from previously satisfied performance obligations.",
    "account": "licensing revenues (QTL); revenues from previously satisfied performance obligations",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "$25 million in lower royalty revenues recognized related to devices sold in prior periods",
    "paragraph_id": "0000804328-26-000086:mdna:98",
    "explanation": false
  },
  {
    "id": "revenue_recognition_qtl_revenue_per_unit_favorable_mix",
    "what_changed": "The QTL bridge cites higher revenue per unit from favorable mix: $59 million for the quarter and $111 million for nine months (mdna:105). This partly offsets the lower estimated unit sales.",
    "account": "licensing revenues (QTL)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "$59 million increase in revenues per unit, which was primarily driven by favorable mix",
    "paragraph_id": "0000804328-26-000086:mdna:99",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_qtl_margin_higher_selling_expense",
    "what_changed": "MD&A says QTL's EBT margin decreased in the quarter (mdna:100). It names higher operating expenses, primarily higher SG&A, together with lower revenues (mdna:102). The nine-month QTL margin is described as approximately flat (mdna:108).",
    "account": "QTL EBT; QTL operating expenses",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "higher operating expenses, primarily driven by higher selling, general and administrative expenses",
    "paragraph_id": "0000804328-26-000086:mdna:101",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_supplier_input_cost_increases",
    "what_changed": "The Looking Forward paragraph is carried as changed. It describes a broad-based rise in input costs and capacity constraints across wafer fabrication, assembly, test, advanced packaging, memory and other materials, attributed in part to demand for leading-edge, AI and data center applications. It says the company continues to see increased product costs from key suppliers that could hurt margins. The prior wording is not in the input.",
    "account": "cost of revenues; gross margin",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "As a result, we continue to see increased product costs from certain of our key suppliers, which could negatively impact our margins.",
    "paragraph_id": "0000804328-26-000086:mdna:120",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_supply_constraints_lost_or_delayed_revenue",
    "what_changed": "The same paragraph warns that if supply and capacity constraints limit component availability, manufacturing capacity or services from suppliers, the company may be unable to fully meet customer demand. That could mean lost or delayed revenue and hurt results, cash flows and financial condition.",
    "account": "revenues (QCT)",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "we may be unable to fully satisfy customer demand, which could result in lost or delayed revenue",
    "paragraph_id": "0000804328-26-000086:mdna:120",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_tariff_excess_obsolete_inventory_reserve_risk",
    "what_changed": "The trade-policy paragraph is carried as changed. It says tariffs and related trade actions add to the uncertainty of estimating customer demand. That may lead to more excess or obsolete inventory or more reserve charges. The paragraph points to a named risk factor in this Quarterly Report. The prior wording and the Item 1A diff are not in the input.",
    "account": "inventories (excess and obsolete reserves); cost of revenues",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "which may result in increased excess or obsolete inventory or reserve charges",
    "paragraph_id": "0000804328-26-000086:mdna:121",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_notes_maturing_may_classified_current",
    "what_changed": "The debt footnote now says $2.0 billion of issued debt is classified as current and matures in May 2027. It also says $498 million of commercial paper is outstanding as short-term debt and the credit facility was undrawn at June 28, 2026. This marks a near-term repayment or refinancing need and current use of the commercial paper program.",
    "account": "short-term debt; long-term debt",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "including $2.0 billion classified as current and maturing in May 2027, and $498 million of outstanding commercial paper reported as short-term debt as of June 28, 2026",
    "paragraph_id": "0000804328-26-000086:mdna:131",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_repurchases_offset_alphawave_share_issuance",
    "what_changed": "The liquidity bridge says the nine-month buybacks ($6.8 billion, 42 million shares) include repurchases that offset shares issued for the Alphawave acquisition. This ties capital return to acquisition dilution. Modular's consideration was also primarily shares (notes:75).",
    "account": "repurchases of common stock; shares outstanding",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "$6.8 billion in payments to repurchase 42 million shares of our common stock (which includes repurchases that offset share issuances in connection with the acquisition of Alphawave)",
    "paragraph_id": "0000804328-26-000086:mdna:133",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_capital_expenditures_and_acquisitions_cash_use",
    "what_changed": "The liquidity bridge names two primary nine-month cash uses: $1.6 billion of capital expenditures and $1.6 billion paid for acquisitions and other investments, net of cash acquired.",
    "account": "property, plant and equipment; goodwill and intangibles; cash",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "$1.6 billion in capital expenditures, $1.6 billion in cash paid for acquisitions and other investments (net of cash acquired)",
    "paragraph_id": "0000804328-26-000086:mdna:133",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_commercial_paper_net_proceeds_offset_cash_decline",
    "what_changed": "The liquidity bridge lists $495 million of net commercial paper proceeds, together with operating cash flow, as partly offsetting the nine-month decline in cash and marketable securities. Short-term borrowing is now part of the funding mix.",
    "account": "short-term debt (commercial paper); financing cash flows",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "$495 million in net proceeds of commercial paper",
    "paragraph_id": "0000804328-26-000086:mdna:133",
    "explanation": false
  },
  {
    "id": "earnings_quality_valuation_allowance_release_noncash_tax_benefit",
    "what_changed": "MD&A says nine-month income taxes paid were greater than the provision. It attributes this primarily to the $5.7 billion second-quarter valuation allowance release, plus the final repatriation installment (separate item). Nine-month net income therefore carries a large non-cash tax benefit.",
    "account": "income tax expense (benefit); deferred tax assets",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "This was primarily driven by the $5.7 billion release of our valuation allowance on federal deferred tax assets in the second quarter of fiscal 2026",
    "paragraph_id": "0000804328-26-000086:mdna:134",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_final_repatriation_tax_installment_paid",
    "what_changed": "MD&A says the nine months included the final installment, $663 million, of the one-time U.S. repatriation tax accrued in fiscal 2018. The prose calls it final, so this cash outflow ends.",
    "account": "income taxes paid; income taxes payable",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "our final installment payment for a one-time U.S. repatriation tax accrued in fiscal 2018 of $663 million",
    "paragraph_id": "0000804328-26-000086:mdna:134",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_research_expensing_lowers_cash_taxes",
    "what_changed": "MD&A says the OBBB's permanent reinstatement of current deduction of domestic R&D will help operating cash flows through significantly lower cash tax payments. The tax note (notes:32) says the same.",
    "account": "income taxes paid; operating cash flow",
    "expected_direction": "down",
    "horizon": "12 months",
    "quote": "We expect this change will have a favorable effect on our cash flows from operations due to significantly lower cash tax payments.",
    "paragraph_id": "0000804328-26-000086:mdna:134",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_inventory_build_memory_supply_constraints",
    "what_changed": "Management explains the inventory increase. MD&A says working-capital changes hurt nine-month operating cash flow, primarily because inventory increased. It attributes that increase to certain customer demand impacts from memory supply constraints. The release CEO quote likewise cites a challenging memory and supply environment (8k_2_02:16).",
    "account": "inventories",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "primarily driven by an increase in inventory reflecting certain customer demand impacts from memory supply constraints",
    "paragraph_id": "0000804328-26-000086:mdna:135",
    "explanation": true
  },
  {
    "id": "liquidity_and_capital_other_assets_utilization_of_supply_prepayments",
    "what_changed": "MD&A says other assets decreased primarily because prior advanced supply agreement payments were used. Notes:10 restates the capacity-purchase advance payment balances.",
    "account": "other current assets; other assets (supplier advance payments)",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "The decrease in other assets is primarily due to the utilization of prior advanced supply agreement payments.",
    "paragraph_id": "0000804328-26-000086:mdna:135",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_accrued_customer_incentives_increase_payment_timing",
    "what_changed": "Management explains the change in a revenue-reducing accrual. MD&A says payroll, benefits and other liabilities increased primarily because accrued customer incentives increased, including the effect of payment timing. Employee cash incentive payouts partly offset this. Notes:11 tables 'customer incentives and other customer-related liabilities' within other current liabilities.",
    "account": "other current liabilities (accrued customer incentives)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase in payroll, benefits and other liabilities is primarily due to an increase in accrued customer incentives, which included the impact of timing of related payments, partially offset by payments related to our employee cash incentive program.",
    "paragraph_id": "0000804328-26-000086:mdna:135",
    "explanation": true
  },
  {
    "id": "results_against_expectations_revenue_high_end_of_guidance",
    "what_changed": "The CEO says third-quarter revenue came in at the high end of guidance despite a challenging memory and supply environment. The prior guidance range is not in the input, so checking the claim is for the supervisor.",
    "account": "revenues",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "with quarterly revenues at the high end of guidance",
    "paragraph_id": "0000804328-26-000085:8k_2_02:16",
    "explanation": false
  },
  {
    "id": "across_documents_memory_supply_environment_release_and_mdna",
    "what_changed": "The release names the memory and supply environment as the quarter's headwind. The 10-Q ties the same condition to an inventory build from customer demand impacts (mdna:135) and to capacity constraints that could delay revenue (mdna:120). The two documents give a consistent cause for weaker handset demand and higher inventory.",
    "account": "QCT handset revenues; inventories",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "Despite a challenging memory and supply environment",
    "paragraph_id": "0000804328-26-000085:8k_2_02:16",
    "explanation": false
  },
  {
    "id": "results_against_expectations_non_handset_revenue_growth_targets",
    "what_changed": "The release sets new forward targets:\n- non-handset revenues of $40 billion by fiscal 2029, which the company calls nearly double its November 2024 target;\n- year-over-year non-handset growth, including Data Center, accelerating from 24% in fiscal 2026 to greater than 60% in fiscal 2027.",
    "account": "non-handset revenues (automotive, IoT, Data Center)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "we expect year-over-year growth in non-handset revenues, including Data Center, to accelerate from 24% in fiscal 2026 to greater than 60% in fiscal 2027",
    "paragraph_id": "0000804328-26-000085:8k_2_02:16",
    "explanation": false
  },
  {
    "id": "results_against_expectations_pricing_actions_for_higher_input_costs",
    "what_changed": "The release outlook says the company is raising product prices to reflect higher industry input costs. It expects these increases to help gross margins over time as they gradually take effect, and says these factors are reflected in third-quarter results and fourth-quarter guidance. MD&A (mdna:120) says the same cost rise could hurt margins. Near-term pressure and a later pricing benefit are both stated.",
    "account": "gross margin; average selling prices (QCT)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "We are taking concrete actions to reflect the higher input costs in our product pricing and expect these actions to benefit our gross margins over time as the pricing changes gradually come into effect.",
    "paragraph_id": "0000804328-26-000085:8k_2_02:29",
    "explanation": false
  },
  {
    "id": "results_against_expectations_fourth_quarter_guidance_ranges",
    "what_changed": "Fourth-quarter fiscal 2026 guidance:\n- revenues $9.7B to $10.5B (QCT $8.4B to $9.0B; QTL $1.2B to $1.4B);\n- GAAP diluted EPS $1.22 to $1.42;\n- non-GAAP diluted EPS $2.05 to $2.25, with $0.72 attributed to share-based compensation and $0.11 to other items.\nComparing these ranges with third-quarter actuals is for the numbers reader.",
    "account": "revenues; diluted EPS",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "$9.7B - $10.5B",
    "paragraph_id": "0000804328-26-000085:8k_2_02:31",
    "explanation": false
  },
  {
    "id": "earnings_quality_fourth_quarter_other_items_acquisition_related",
    "what_changed": "The guidance footnote says the fourth-quarter 'other items' EPS adjustment is primarily acquisition-related. This is consistent with the Modular closing on July 28, 2026 and its service-conditioned executive shares (notes:75).",
    "account": "acquisition-related charges (amortization, step-ups, integration costs)",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "Our guidance for diluted EPS attributable to other items for the fourth quarter of fiscal 2026 is primarily related to acquisition-related items.",
    "paragraph_id": "0000804328-26-000085:8k_2_02:33",
    "explanation": false
  },
  {
    "id": "earnings_quality_fixed_non_gaap_tax_rate_prior_periods_not_recast",
    "what_changed": "The release describes the non-GAAP tax method in use since the first quarter of fiscal 2026: a fixed estimated non-GAAP tax rate, set annually and subject to periodic re-evaluation. Prior periods were not updated because the company judged the effect immaterial. Year-over-year non-GAAP net income and EPS therefore mix two tax methods.",
    "account": "non-GAAP income tax; non-GAAP net income and EPS",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Prior periods have not been updated for this change as the effect would not be material.",
    "paragraph_id": "0000804328-26-000085:8k_2_02:71",
    "explanation": false
  },
  {
    "id": "earnings_quality_non_gaap_tax_rate_includes_capitalized_research_amortization",
    "what_changed": "The release gives the fixed non-GAAP tax rate as 12.5% for the third quarter. It says the other-items tax adjustment includes amortization of previously capitalized domestic R&D for U.S. federal tax purposes, whose initial benefit had been excluded from non-GAAP results. The 10-Q gives the GAAP quarterly rate as 19% (notes:32).",
    "account": "non-GAAP income tax; income tax expense",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "our fixed estimated Non-GAAP tax rate of 12.5% for the third quarter of fiscal 2026 and includes the impact of the amortization of previously capitalized domestic research and development expenditures for U.S. federal income tax purposes",
    "paragraph_id": "0000804328-26-000085:8k_2_02:79",
    "explanation": false
  },
  {
    "id": "across_documents_restructuring_figure_release_versus_note",
    "what_changed": "The release footnote and the 10-Q note each give a restructuring figure for the quarter. The release says other items excluded from non-GAAP included $70 million of restructuring and restructuring-related charges. The 10-Q note (notes:26) says other expenses consisted of $68 million of restructuring and restructuring-related charges. Whether the two figures cover the same scope (for example, part recorded outside other expenses) is for the supervisor's reconciliation.",
    "account": "other expenses (restructuring); operating expenses",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "$70 million of restructuring and restructuring-related charges",
    "paragraph_id": "0000804328-26-000085:8k_2_02:78",
    "explanation": false
  },
  {
    "id": "across_documents_european_commission_fine_interest_outside_contingency_note",
    "what_changed": "The release says third-quarter non-GAAP exclusions included $1 million of interest expense on a fine the European Commission imposed in 2019, so interest is still accruing on that fine. The contingencies note text in the input covers only ParkerVision, Arm and contingent losses (notes:39 to notes:46) and does not mention the European Commission fine.",
    "account": "interest expense; liabilities related to the European Commission fine",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "$1 million of interest expense related to a fine imposed on us by the European Commission in 2019",
    "paragraph_id": "0000804328-26-000085:8k_2_02:78",
    "explanation": false
  }
]
```

Items: 63. Items with `explanation: true`: 2 (inventory build, mdna:135; accrued customer incentives, mdna:135).

## Paragraphs carried as text that are not items

### Notes (0000804328-26-000086:notes:N)

- `notes:3`: date rolled forward (three and nine months now; fiscal 2026 still 52 weeks).
- `notes:9`: amounts only (inventory components table).
- `notes:11`: amounts only (other current liabilities table); the customer-incentives cause is itemized from mdna:135.
- `notes:16`: amounts only (QCT revenue disaggregation table).
- `notes:21`: amounts only (revenue from previously satisfied performance obligations); the related prose is itemized from mdna:98.
- `notes:24`: amounts only (customer concentration percentages).
- `notes:27`: amounts only (investment and other income table).
- `notes:34`: amount and date rolled forward (remaining repurchase authorization at June 28, 2026); program terms stated as before.
- `notes:35`: date rolled forward (lead-in to share table).
- `notes:36`: amounts only (shares outstanding roll-forward).
- `notes:38`: amounts only (dilutive and anti-dilutive share table).
- `notes:39`: heading; carried verbatim with the contingencies note.
- `notes:40`: heading; carried verbatim.
- `notes:42`: paragraph boundary moved (note history shows the same Arm v. Qualcomm text split differently); no change in substance.
- `notes:43`: continuation of the same Arm v. Qualcomm text; boundary moved only; no change in substance.
- `notes:45`: carried verbatim with the contingencies note; not in the change history; Arm's notice and withdrawal are unchanged.
- `notes:46`: date rolled forward (no accrual "at June 28, 2026" instead of March 29, 2026); wording otherwise identical per history.
- `notes:48`: insufficient. Carried as changed, but the prior text is not in the input and the change history does not cover it. It reads as standard segment-basis language, probably a boundary shift with notes:49.
- `notes:52`: amounts only (segment results table).
- `notes:55`: amounts only (segment-to-consolidated reconciliation table).
- `notes:56`: period label rolled forward (six to nine months); describes the fiscal 2025 licensing settlement already in prior periods.
- `notes:58`: date rolled forward (fair value table lead-in).
- `notes:59`: amounts only (fair value hierarchy table).
- `notes:61`: footnote renumbered to (2) after the new footnote (1) at notes:60; standard deferred-compensation description.
- `notes:62`: amount and date rolled forward (fair value of fixed-rate notes).
- `notes:63`: date rolled forward (marketable securities classification).
- `notes:65`: amounts only (debt securities maturity table).
- `notes:69`: date rolled forward (exchangeable shares outstanding "as of June 28, 2026"); Alphawave exchangeable-share terms as described.
- `notes:77`: date rolled forward; insufficient. It states no 10b5-1 adoptions or terminations in the quarter, but the prior quarter's text is not in the input.

### Note change history

`0000804328-26-000086:note_history:1` to `:11` and `0000804328-26-000061:note_history:1` to `:10` mirror notes paragraphs already accounted for:
- history 1 → notes:41
- history 2 and 3 → notes:42 and notes:43
- history 4 → notes:44 (the removed sentence is itemized from 061 history 4)
- history 5 → notes:46
- history 6 → notes:3
- history 7 → notes:6
- history 8 → notes:12
- history 9 → notes:16
- history 10 → notes:19
- history 11 → notes:75

### MD&A (0000804328-26-000086:mdna:N)

- `mdna:4`: heading, quarter rolled forward.
- `mdna:5`: amounts only (headline revenue and net income changes).
- `mdna:7`: amounts only (QTL decline summary); QTL drivers itemized at mdna:97, mdna:98, mdna:99.
- `mdna:12`: insufficient. Standard QTI/QTL structure description; the paragraph boundary appears shifted (next paragraph maps to prior mdna:15); prior text is not in the input.
- `mdna:13`: insufficient. Continuation of mdna:12; boundary shift; no new statement identifiable.
- `mdna:16`: amounts only (revenue table).
- `mdna:17`: heading.
- `mdna:18`: lead-in to the revenue bridge.
- `mdna:19`: amounts only (QCT bridge figure; QCT drivers itemized at mdna:6 and mdna:79).
- `mdna:20`: amounts only (QTL bridge figure).
- `mdna:22`: heading.
- `mdna:23`: lead-in.
- `mdna:24`: amounts only (nine-month QCT bridge figure).
- `mdna:26`: nine-month counterpart of the mdna:21 item (same Alphawave driver).
- `mdna:27`: amounts only (nine-month QTL bridge figure).
- `mdna:28`: amounts only (cost of revenues and gross margin table).
- `mdna:29`: heading.
- `mdna:31`: page number.
- `mdna:32`: amounts only (R&D table).
- `mdna:33`: heading.
- `mdna:34`: lead-in.
- `mdna:37`: heading.
- `mdna:38`: lead-in.
- `mdna:39`: nine-month counterpart of the mdna:35 item (same NRE driver plus employee-related expenses, noted there).
- `mdna:40`: nine-month SBC figure; covered by the mdna:36 item.
- `mdna:42`: amounts only (SG&A table).
- `mdna:43`: heading.
- `mdna:44`: lead-in.
- `mdna:45`: quarter SG&A SBC figure; covered by the mdna:36 item.
- `mdna:48`: heading.
- `mdna:49`: lead-in.
- `mdna:50`: nine-month SG&A SBC figure; covered by the mdna:36 item.
- `mdna:52`: nine-month counterpart of the mdna:46 item.
- `mdna:53`: amounts only (other expense table).
- `mdna:54`: heading.
- `mdna:55`: same restructuring and severance matter as the notes:26 item, without amounts.
- `mdna:57`: amounts only (interest expense and investment income table).
- `mdna:58`: same IPO-gain driver as the mdna:8 item.
- `mdna:62`: amounts only (tax rate reconciliation table).
- `mdna:64`: insufficient. OBBB background split across paragraphs (continues at mdna:66); no new statement identifiable; prior text is not in the input.
- `mdna:66`: insufficient. Continuation of the OBBB and fiscal 2025 valuation allowance background; split artifact; prior text is not in the input.
- `mdna:70`: date rolled forward (cross-reference to Note 6 for the third quarter).
- `mdna:72`: amounts only (QCT segment table).
- `mdna:75`: insufficient. QCT equipment and services amounts rolled forward; it can't be told whether the product list wording changed.
- `mdna:76`: heading.
- `mdna:77`: lead-in.
- `mdna:84`: heading.
- `mdna:85`: lead-in.
- `mdna:87`: nine-month counterpart of the mdna:79 item.
- `mdna:89`: nine-month QCT margin lead-in; covered by the mdna:81 item.
- `mdna:94`: amounts only (QTL table).
- `mdna:95`: heading.
- `mdna:96`: lead-in.
- `mdna:100`: lead-in to QTL margin drivers; covered by the mdna:101 item.
- `mdna:102`: QTL 'lower revenues' margin bullet; folded into the mdna:101 item.
- `mdna:103`: heading.
- `mdna:104`: lead-in.
- `mdna:105`: nine-month counterpart of the mdna:99 item.
- `mdna:106`: nine-month counterpart of the mdna:97 item (noted there).
- `mdna:107`: nine-month counterpart of the mdna:98 item.
- `mdna:108`: nine-month QTL margin described as approximately flat; noted in the mdna:101 item.
- `mdna:110`: amounts only (QSI table).
- `mdna:111`: heading.
- `mdna:112`: same IPO-gain driver as the mdna:8 item.
- `mdna:113`: heading.
- `mdna:114`: nine-month QSI drivers covered by the mdna:8 and mdna:59 items.
- `mdna:124`: insufficient. Standard legal-proceedings cross-reference to Note 5; no new matter; prior text is not in the input.
- `mdna:128`: date rolled forward (liquidity lead-in).
- `mdna:129`: amounts only (cash, marketable securities and debt table).
- `mdna:132`: amounts only (cash flow summary table).
- `mdna:137`: date rolled forward (additional capital requirements reference).
- `mdna:138`: insufficient. Generic regulatory and litigation risk language with no new matter, amount or date; prior text is not in the input.

### Item 4 (0000804328-26-000086:item_4_controls:N)

- `item_4_controls:1`: heading.
- `item_4_controls:2`: standard conclusion that disclosure controls are effective; no change identifiable.
- `item_4_controls:3`: quarter label rolled forward; no change in internal control reported.
- `item_4_controls:4`: page number.

### 8-K item 2.02, exhibit 99.1 (0000804328-26-000085:8k_2_02:N)

- `:1` to `:4`: filing and exhibit headers.
- `:5` to `:8`: IR contact block.
- `:9`: release title.
- `:10`: amounts only (headline revenue).
- `:11`: amounts only (headline EPS).
- `:12`: amounts only (headline combined automotive and IoT growth claim).
- `:13`: amounts only (headline automotive streak claim); the automotive driver is itemized at mdna:79.
- `:14`: headline for the same event as the notes:75 Modular item.
- `:15`: dateline.
- `:17`: heading.
- `:18`: amounts only (GAAP and non-GAAP results table).
- `:19`: non-GAAP footnote boilerplate.
- `:20`: heading.
- `:21`: amounts only (segment table).
- `:22`: page footer.
- `:23`: heading.
- `:24`: amounts only (QCT revenue streams table).
- `:25`: disaggregation-basis boilerplate.
- `:26`: heading.
- `:27`: amounts only (quarterly dividends and buybacks); the buyback driver is itemized at mdna:133.
- `:28`: heading.
- `:30`: lead-in to the guidance table.
- `:32`: outlook-basis boilerplate.
- `:34`: page footer.
- `:35`: heading.
- `:36`: call logistics.
- `:37`: replay logistics.
- `:38`: IR website boilerplate.
- `:39`: heading.
- `:40`: corporate description boilerplate.
- `:41`: corporate structure and trademark boilerplate.
- `:42`: heading only; the forward-looking statement body is not carried.
- `:43`: page footer.
- `:44` to `:47`: balance sheet headers.
- `:48`: amounts only (balance sheet).
- `:49`: page footer.
- `:50` to `:53`: income statement headers.
- `:54`: amounts only (income statement).
- `:55`: page footer.
- `:56` to `:59`: cash flow headers.
- `:60`: amounts only (cash flow statement).
- `:61`: page footer.
- `:62`: heading.
- `:63`: non-GAAP caution boilerplate.
- `:64`: non-GAAP use boilerplate.
- `:65`: list of non-GAAP exclusions, boilerplate.
- `:66`: QSI exclusion rationale, boilerplate; QSI gains itemized at mdna:8.
- `:67`: SBC exclusion rationale, boilerplate.
- `:68`: lead-in.
- `:69`: insufficient. Definition of acquisition-related exclusions, including operating results of acquired businesses expected to be sold and pre-close temporary debt facility or letter-of-credit costs. No prior release is in the input to tell whether it changed.
- `:70`: other-items exclusion boilerplate; deferred compensation itemized at mdna:47.
- `:72`: page footer.
- `:73`: heading.
- `:74`: amounts only (GAAP to non-GAAP reconciliation).
- `:75`: reconciliation footnote boilerplate.
- `:76`: rounding note.
- `:77`: amounts only (supplemental reconciliation table).
- `:80`: rounding note.

### 8-K index and late-filing list

- **2026-06-24 Item 3.02 filing (0001104659-26-077071):** insufficient. Its body is not in the input; it cannot be tied to the Alphawave exchangeable shares (notes:69) or to Modular (notes:75).
- **Late-filing notifications:** none listed.
- **Other index lines:** item codes for earlier periods only.

### Count of insufficient

11: notes:48, notes:77, mdna:12, mdna:13, mdna:64, mdna:66, mdna:75, mdna:124, mdna:138, 8k_2_02:69, and the 2026-06-24 Item 3.02 filing.
