<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# SNDK — numbers reader — 10-K 0001628280-26-057406 (fiscal year ended 2026-07-03)

## Before the items

**What was read.** I read four inputs in full: `input_trends.json`, `input_numbers.json`, `input_8k.md` (8-K 0001628280-26-053346, filed 2026-08-05) and `input_prior_predictions.md`.

**Integrity check.** The directory holds no prices, abnormal returns, short interest, other companies' files, prior-run probabilities or outcome window. One caveat: the numeric facts include the company's own `us-gaap:SharePrice` tags in its employee stock purchase plan disclosure. That is filed XBRL, not a market-price feed. I flag it here and used none of it.

**Prior flags.** None on record. `input_prior_predictions.md` says this company has no earlier run.

**What is not in the input:**
- **No articulation checks.** No articulation gap was computed, so none is reported as such.
- **No restatement traces.** The restated prior values below come from reading the same tag and date as printed by different filings. Each printed value is quoted, and no reconciliation is in the input.
- **No fourth-quarter derivation output.** No standalone fourth-quarter number computed by Python exists here. The only fourth-quarter figures are the company's own, printed in the 8-K release.

**Periods with no cells.**
- `quarters-back-0` (target 2026-07-03) has no cells, so it has no items. The table gives this reason: "no quarter ending within 20 days of 2026-07-03 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py". That derivation is not in my inputs.
- `quarters-back-4` has no cells for the same reason, with target 2025-07-04.
- `years-back-4` has no cells: "no year ending within 20 days of 2022-07-08 is in the companyfacts record".

**R&D capitalization block for years-back-0.** It is unfilled. `capitalized_development_cost` is untagged in any period, and the four- and five-years-back R&D expense is not in the record. The block prints no `paragraph_id`, so it cannot be quoted as an item.

**Day counts.** The table prints years-back-0 as 371 days and years-back-1 as 364 days. Day-count ratios (DSI, DSO) therefore span periods of different length.

**History is short.** The trend table holds at most four filled years and six filled quarters, often fewer. No item below makes a trend claim, and every trend item says `insufficient` for a direction. `expected_direction` is `none` throughout, except for one item that restates management's own guidance.

**Where the release rows sit.** Rows quoted from the 8-K release come from its statement tables and prose, not from notes. They sit under the first heading.

## Seen in the statements

```json
[
  {
    "id": "earnings_quality_accruals_over_total_assets_trend_table_year",
    "what_changed": "Accruals over total assets, fiscal year ended 2026-07-03: value -0.01057448793708624; year-over-year change against years-back-1 is 0.1222711031295291; position in the company's filed history: highest of the 3 filled years. Cell inputs: NetIncomeLoss 11433000000.0, NetCashProvidedByUsedInOperatingActivities 11671000000.0, Assets 22507000000.0. With three filled years there is no basis for a trend claim, so the direction is insufficient.",
    "account": "NetIncomeLoss; NetCashProvidedByUsedInOperatingActivities; Assets",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"position_in_history\": \"highest of the 3 filled years\"",
    "paragraph_id": "0001628280-26-057406:trends:accruals_over_total_assets:2025-06-28..2026-07-03"
  },
  {
    "id": "revenue_recognition_bad_debt_reserve_ratio_trend_table_insufficient",
    "what_changed": "insufficient. bad_debt_reserve_ratio has no value for the fiscal year ended 2026-07-03 or for any other period in the table. The cell says none of the three allowance concepts is tagged in any period, so no value, change or history position exists. Receivables at the same date are printed at 4708000000.0 in the receivables cells, and no allowance against them appears anywhere in this input.",
    "account": "AccountsReceivableAllowanceForCreditLossCurrent (untagged)",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"missing\": \"no row for bad_debt_allowance: the companyfacts record tags none of us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable in any period.",
    "paragraph_id": "0001628280-26-057406:trends:bad_debt_reserve_ratio:2025-06-28..2026-07-03"
  },
  {
    "id": "revenue_recognition_contract_liabilities_over_revenue_trend_table_year",
    "what_changed": "Contract liabilities over revenue, fiscal year ended 2026-07-03: value 0.04193006716712762; year-over-year change 0.038531018900642235; position: highest of the 2 filled years. Inputs: ContractWithCustomerLiabilityCurrent 849000000.0 and revenue 20248000000.0. Noncurrent contract liabilities (393000000 in the facts) are outside the formula. The numerator's tag first appears in the third-quarter 10-Q. Two filled years is insufficient for a trend claim.",
    "account": "ContractWithCustomerLiabilityCurrent; RevenueFromContractWithCustomerExcludingAssessedTax",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"position_in_history\": \"highest of the 2 filled years\"",
    "paragraph_id": "0001628280-26-057406:trends:contract_liabilities_over_revenue:2025-06-28..2026-07-03"
  },
  {
    "id": "earnings_quality_days_sales_of_inventory_trend_table_year",
    "what_changed": "Days sales of inventory, fiscal year ended 2026-07-03: value 173.29605263157896; year-over-year change 26.15313993470943; position: highest of the 3 filled years. Inputs: InventoryNet 2698000000.0 and CostOfGoodsAndServicesSold 5776000000.0. The table prints this period as 371 days against 364 for years-back-1. Three filled years is insufficient for a direction.",
    "account": "InventoryNet; CostOfGoodsAndServicesSold",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"position_in_history\": \"highest of the 3 filled years\"",
    "paragraph_id": "0001628280-26-057406:trends:days_sales_of_inventory:2025-06-28..2026-07-03"
  },
  {
    "id": "revenue_recognition_days_sales_outstanding_trend_table_year",
    "what_changed": "Days sales outstanding, fiscal year ended 2026-07-03: value 86.26372975108653; year-over-year change 33.40825728337749; position: highest of the 3 filled years. Inputs: AccountsReceivableNetCurrent 4708000000.0 and revenue 20248000000.0. The period has 371 days against 364 for years-back-1. The release cash flow shows receivables changes of (1,982) for the fourth quarter and (3,640) for the year. Three filled years is insufficient for a direction.",
    "account": "AccountsReceivableNetCurrent; RevenueFromContractWithCustomerExcludingAssessedTax",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"position_in_history\": \"highest of the 3 filled years\"",
    "paragraph_id": "0001628280-26-057406:trends:days_sales_outstanding:2025-06-28..2026-07-03"
  },
  {
    "id": "earnings_quality_gross_margin_trend_table_year",
    "what_changed": "Gross margin, fiscal year ended 2026-07-03: value 0.7147372580007902; year-over-year change 0.41398946738216347; position: highest of the 4 filled years. Inputs: revenue 20248000000.0 and CostOfGoodsAndServicesSold 5776000000.0. The release attributes sequential revenue growth about one-third to volume and two-thirds to price. Four filled years is insufficient for a durable trend claim.",
    "account": "RevenueFromContractWithCustomerExcludingAssessedTax; CostOfGoodsAndServicesSold",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"position_in_history\": \"highest of the 4 filled years\"",
    "paragraph_id": "0001628280-26-057406:trends:gross_margin:2025-06-28..2026-07-03"
  },
  {
    "id": "estimates_and_discretion_inventory_reserve_ratio_trend_table_year",
    "what_changed": "Inventory reserve ratio, fiscal year ended 2026-07-03: value 0.046330615270570794; year-over-year change -0.014275445335489814; position: lowest of the 2 filled years. Inputs: InventoryValuationReserves 125000000.0 and InventoryNet 2698000000.0. Years-back-1 used 126000000.0 and 2079000000.0. The tagged inventory write-down for the year is 91000000. No quarter carries a reserve row. Two filled years is insufficient for a trend claim.",
    "account": "InventoryValuationReserves; InventoryNet",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"position_in_history\": \"lowest of the 2 filled years\"",
    "paragraph_id": "0001628280-26-057406:trends:inventory_reserve_ratio:2025-06-28..2026-07-03"
  },
  {
    "id": "earnings_quality_non_gaap_gap_trend_table_insufficient",
    "what_changed": "insufficient. non_gaap_gap has no value for the fiscal year ended 2026-07-03. The cell says no us-gaap concept carries a non-GAAP measure. The release prints fiscal 2026 non-GAAP net income of 10,987 next to GAAP net income of 11,433. No gap was computed, so none is stated here.",
    "account": "non_gaap_net_income (not in record); NetIncomeLoss",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
    "paragraph_id": "0001628280-26-057406:trends:non_gaap_gap:2025-06-28..2026-07-03"
  },
  {
    "id": "revenue_recognition_receivables_over_revenue_trend_table_year",
    "what_changed": "Receivables over revenue, fiscal year ended 2026-07-03: value 0.23251679178190438; year-over-year change 0.08730944983764877; position: highest of the 3 filled years. Inputs: AccountsReceivableNetCurrent 4708000000.0 and revenue 20248000000.0. Three filled years is insufficient for a direction.",
    "account": "AccountsReceivableNetCurrent; RevenueFromContractWithCustomerExcludingAssessedTax",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"position_in_history\": \"highest of the 3 filled years\"",
    "paragraph_id": "0001628280-26-057406:trends:receivables_over_revenue:2025-06-28..2026-07-03"
  },
  {
    "id": "earnings_quality_soft_asset_share_trend_table_year",
    "what_changed": "Soft asset share, fiscal year ended 2026-07-03: value 0.7584751410672236; year-over-year change -0.07979979154733163; position: lowest of the 3 filled years. Inputs: Assets 22507000000.0, CashAndCashEquivalentsAtCarryingValue 4762000000.0 and PropertyPlantAndEquipmentNet 674000000.0. Three filled years is insufficient for a direction.",
    "account": "Assets; CashAndCashEquivalentsAtCarryingValue; PropertyPlantAndEquipmentNet",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"position_in_history\": \"lowest of the 3 filled years\"",
    "paragraph_id": "0001628280-26-057406:trends:soft_asset_share:2025-06-28..2026-07-03"
  },
  {
    "id": "estimates_and_discretion_warranty_reserve_ratio_trend_table_year",
    "what_changed": "Warranty reserve ratio, fiscal year ended 2026-07-03: value 0.002370604504148558; year-over-year change -0.0036117204448657177; position: lowest of the 4 filled years. Inputs: StandardProductWarrantyAccrual 48000000.0 and revenue 20248000000.0. The quarters-back-1 cell used an accrual of 73000000.0 at 2026-04-03. The tagged rollforward shows a -28000000 change for pre-existing warranties in the year. Four filled years is insufficient for a durable trend claim.",
    "account": "StandardProductWarrantyAccrual; RevenueFromContractWithCustomerExcludingAssessedTax",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"position_in_history\": \"lowest of the 4 filled years\"",
    "paragraph_id": "0001628280-26-057406:trends:warranty_reserve_ratio:2025-06-28..2026-07-03"
  },
  {
    "id": "articulation_and_the_filed_history_accrued_liabilities_prior_year_end_second_quarter_print",
    "what_changed": "Restated prior value. The second-quarter 10-Q (0001628280-26-004407) prints AccruedLiabilitiesCurrent at 2025-06-27 as 425000000. The third-quarter 10-Q prints 400000000 for the same date, and the 10-K prints 274000000. From the third-quarter 10-Q onward, the same date also carries new contract-liability (25000000) and refund-liability (126000000) tags. With no restatement trace or reconciliation in the input, a pure reclassification is not established.",
    "account": "AccruedLiabilitiesCurrent",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "\"value\": \"425000000\"",
    "paragraph_id": "0001628280-26-004407:facts:AccruedLiabilitiesCurrent:2025-06-27"
  },
  {
    "id": "articulation_and_the_filed_history_accrued_liabilities_prior_year_end_third_quarter_print",
    "what_changed": "Restated prior value. The third-quarter 10-Q (0001628280-26-029401) prints AccruedLiabilitiesCurrent at 2025-06-27 as 400000000. The second-quarter 10-Q printed 425000000 and the 10-K prints 274000000, so three filings give three values for one date. The same 10-Q is the first to tag ContractWithCustomerLiabilityCurrent for that date (25000000).",
    "account": "AccruedLiabilitiesCurrent",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "\"value\": \"400000000\"",
    "paragraph_id": "0001628280-26-029401:facts:AccruedLiabilitiesCurrent:2025-06-27"
  },
  {
    "id": "articulation_and_the_filed_history_accrued_liabilities_prior_year_end_annual_print",
    "what_changed": "Restated prior value. The 10-K prints AccruedLiabilitiesCurrent at 2025-06-27 as 274000000, against 425000000 and 400000000 in the two earlier 10-Qs. The release balance sheet shows accrued expenses of 274 for June 27, 2025, with refund liabilities (126) and contract liabilities (25) on separate lines. No Python reconciliation exists.",
    "account": "AccruedLiabilitiesCurrent",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "\"value\": \"274000000\"",
    "paragraph_id": "0001628280-26-057406:facts:AccruedLiabilitiesCurrent:2025-06-27"
  },
  {
    "id": "articulation_and_the_filed_history_other_noncurrent_liabilities_prior_year_end_second_quarter_print",
    "what_changed": "Restated prior value. The second-quarter 10-Q prints OtherLiabilitiesNoncurrent at 2025-06-27 as 496000000. The third-quarter 10-Q and the 10-K both print 365000000. The release balance sheet carries a separate 'Income tax payable, non-current' line of 131 for June 27, 2025. No reconciliation is in the input.",
    "account": "OtherLiabilitiesNoncurrent",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "\"value\": \"496000000\"",
    "paragraph_id": "0001628280-26-004407:facts:OtherLiabilitiesNoncurrent:2025-06-27"
  },
  {
    "id": "articulation_and_the_filed_history_other_noncurrent_liabilities_prior_year_end_third_quarter_print",
    "what_changed": "Restated prior value. The third-quarter 10-Q prints OtherLiabilitiesNoncurrent at 2025-06-27 as 365000000, against 496000000 in the second-quarter 10-Q. The value changed in the third quarter, the same filing that changed the accrued-liabilities print for this date.",
    "account": "OtherLiabilitiesNoncurrent",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "\"value\": \"365000000\"",
    "paragraph_id": "0001628280-26-029401:facts:OtherLiabilitiesNoncurrent:2025-06-27"
  },
  {
    "id": "articulation_and_the_filed_history_other_noncurrent_liabilities_prior_year_end_annual_print",
    "what_changed": "Restated prior value, as carried in the 10-K. The 10-K prints OtherLiabilitiesNoncurrent at 2025-06-27 as 365000000, the same as the third-quarter 10-Q and different from the second-quarter 10-Q's 496000000.",
    "account": "OtherLiabilitiesNoncurrent",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "\"value\": \"365000000\"",
    "paragraph_id": "0001628280-26-057406:facts:OtherLiabilitiesNoncurrent:2025-06-27"
  },
  {
    "id": "structure_and_disclosure_changes_contract_liability_current_tag_first_filed",
    "what_changed": "Change of tag. ContractWithCustomerLiabilityCurrent for 2025-06-27 first appears in the third-quarter 10-Q, at 25000000. The trend table has no contract_liabilities row for 2025-10-03 or 2026-01-02, so the quarterly contract-liability history starts with the third quarter.",
    "account": "ContractWithCustomerLiabilityCurrent",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "\"value\": \"25000000\"",
    "paragraph_id": "0001628280-26-029401:facts:ContractWithCustomerLiabilityCurrent:2025-06-27"
  },
  {
    "id": "structure_and_disclosure_changes_contract_liability_noncurrent_tag_first_filed",
    "what_changed": "Change of tag. ContractWithCustomerLiabilityNoncurrent for 2025-06-27 first appears in the third-quarter 10-Q, at 0. The 10-K prints 393000000 for 2026-07-03.",
    "account": "ContractWithCustomerLiabilityNoncurrent",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "\"value\": \"0\"",
    "paragraph_id": "0001628280-26-029401:facts:ContractWithCustomerLiabilityNoncurrent:2025-06-27"
  },
  {
    "id": "structure_and_disclosure_changes_refund_liability_current_tag_first_filed",
    "what_changed": "Change of tag. ContractWithCustomerRefundLiabilityCurrent first appears in the 10-K, at 126000000 for 2025-06-27. The earlier 10-Qs covered that date under AccruedLiabilitiesCurrent, at higher values. This concept is new to the filed history.",
    "account": "ContractWithCustomerRefundLiabilityCurrent",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "\"value\": \"126000000\"",
    "paragraph_id": "0001628280-26-057406:facts:ContractWithCustomerRefundLiabilityCurrent:2025-06-27"
  },
  {
    "id": "structure_and_disclosure_changes_refund_liability_second_tag_same_filing",
    "what_changed": "Change of tag. The 10-K also tags the refund balance as ContractWithCustomerRefundLiability, without the Current suffix: 126000000 at 2025-06-27 and 1500000000 at 2026-07-03. One balance carries two concepts in one filing.",
    "account": "ContractWithCustomerRefundLiability",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "\"value\": \"126000000\"",
    "paragraph_id": "0001628280-26-057406:facts:ContractWithCustomerRefundLiability:2025-06-27"
  },
  {
    "id": "articulation_and_the_filed_history_goodwill_impairment_two_values_one_filing",
    "what_changed": "Same filing, concept and period, two values. Under this one paragraph_id the 10-K prints GoodwillImpairmentLoss for the year ended 2025-06-27 as 1800000000 (decimals -8) and as 1830000000 (decimals -6). The release statement of operations shows 1,830, and its prose says $1.8 billion. This is a precision difference inside the filing, not a restatement.",
    "account": "GoodwillImpairmentLoss",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"1800000000\"",
    "paragraph_id": "0001628280-26-057406:facts:GoodwillImpairmentLoss:2024-06-29..2025-06-27"
  },
  {
    "id": "articulation_and_the_filed_history_receivables_two_precisions_one_filing",
    "what_changed": "Same filing, concept and date, two precisions. AccountsReceivableNetCurrent at 2026-07-03 prints here as 4700000000 (decimals -8). The trend cells use 4708000000.0 for the same id, and the release balance sheet shows 4,708. This is a precision difference only.",
    "account": "AccountsReceivableNetCurrent",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "\"value\": \"4700000000\"",
    "paragraph_id": "0001628280-26-057406:facts:AccountsReceivableNetCurrent:2026-07-03"
  },
  {
    "id": "articulation_and_the_filed_history_prior_receivables_two_precisions_one_filing",
    "what_changed": "Same filing, concept and date, two precisions. AccountsReceivableNetCurrent at 2025-06-27 prints here as 1100000000 (decimals -8). The years-back-1 trend cells use 1068000000.0, and the release shows 1,068. This is a precision difference only.",
    "account": "AccountsReceivableNetCurrent",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "\"value\": \"1100000000\"",
    "paragraph_id": "0001628280-26-057406:facts:AccountsReceivableNetCurrent:2025-06-27"
  },
  {
    "id": "articulation_and_the_filed_history_tax_reserve_prior_position_increases_half_year_print",
    "what_changed": "A year-to-date series that does not build. The second-quarter 10-Q prints UnrecognizedTaxBenefitsIncreasesResultingFromPriorPeriodTaxPositions for the six months to 2026-01-02 as 35000000. The nine-month print to 2026-04-03 is 29000000, and the full-year 10-K print is 31000000. A cumulative year-to-date addition that is lower at nine months than at six means an earlier figure was revised or reclassified. No trace in the input says which.",
    "account": "UnrecognizedTaxBenefitsIncreasesResultingFromPriorPeriodTaxPositions",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"35000000\"",
    "paragraph_id": "0001628280-26-004407:facts:UnrecognizedTaxBenefitsIncreasesResultingFromPriorPeriodTaxPositions:2025-06-28..2026-01-02"
  },
  {
    "id": "articulation_and_the_filed_history_tax_reserve_prior_position_increases_nine_month_print",
    "what_changed": "The third-quarter 10-Q prints UnrecognizedTaxBenefitsIncreasesResultingFromPriorPeriodTaxPositions for the nine months to 2026-04-03 as 29000000. That is below the six-month figure (35000000) and the full-year figure (31000000). The release says its income tax adjustments include re-measuring unrecognized tax benefits on positions taken in prior quarters.",
    "account": "UnrecognizedTaxBenefitsIncreasesResultingFromPriorPeriodTaxPositions",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"29000000\"",
    "paragraph_id": "0001628280-26-029401:facts:UnrecognizedTaxBenefitsIncreasesResultingFromPriorPeriodTaxPositions:2025-06-28..2026-04-03"
  },
  {
    "id": "articulation_and_the_filed_history_tax_reserve_prior_position_increases_full_year_print",
    "what_changed": "The 10-K prints UnrecognizedTaxBenefitsIncreasesResultingFromPriorPeriodTaxPositions for the full year to 2026-07-03 as 31000000, against 35000000 at six months and 29000000 at nine months. Current-period-position increases for the full year are 168000000.",
    "account": "UnrecognizedTaxBenefitsIncreasesResultingFromPriorPeriodTaxPositions",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"31000000\"",
    "paragraph_id": "0001628280-26-057406:facts:UnrecognizedTaxBenefitsIncreasesResultingFromPriorPeriodTaxPositions:2025-06-28..2026-07-03"
  },
  {
    "id": "revenue_recognition_tagged_refund_liability_year_end_balance",
    "what_changed": "ContractWithCustomerRefundLiabilityCurrent is 1500000000 at 2026-07-03, against 126000000 at 2025-06-27. The release cash flow shows refund-liability changes of 1,360 for the fourth quarter and 1,374 for the year. A refund liability is variable consideration held back from revenue, so this balance carries estimate risk. One annual comparison is insufficient for a trend claim.",
    "account": "ContractWithCustomerRefundLiabilityCurrent",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "\"value\": \"1500000000\"",
    "paragraph_id": "0001628280-26-057406:facts:ContractWithCustomerRefundLiabilityCurrent:2026-07-03"
  },
  {
    "id": "revenue_recognition_tagged_contract_liability_current_year_end_balance",
    "what_changed": "ContractWithCustomerLiabilityCurrent is 849000000 at 2026-07-03, against 25000000 at 2025-06-27. The release cash flow shows contract-liability changes of 731 for the fourth quarter and 1,217 for the year.",
    "account": "ContractWithCustomerLiabilityCurrent",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "\"value\": \"849000000\"",
    "paragraph_id": "0001628280-26-057406:facts:ContractWithCustomerLiabilityCurrent:2026-07-03"
  },
  {
    "id": "revenue_recognition_tagged_contract_liability_noncurrent_year_end_balance",
    "what_changed": "ContractWithCustomerLiabilityNoncurrent is 393000000 at 2026-07-03. The prior-year-end noncurrent balance was tagged 0 in the third-quarter 10-Q. This balance is outside the trend table's contract-liability formula.",
    "account": "ContractWithCustomerLiabilityNoncurrent",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "\"value\": \"393000000\"",
    "paragraph_id": "0001628280-26-057406:facts:ContractWithCustomerLiabilityNoncurrent:2026-07-03"
  },
  {
    "id": "revenue_recognition_tagged_contract_liability_total_year_end_balance",
    "what_changed": "Total ContractWithCustomerLiability is 1242000000 at 2026-07-03, against 25000000 at 2025-06-27. The third-quarter 10-Q printed 511000000 for 2026-04-03.",
    "account": "ContractWithCustomerLiability",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "\"value\": \"1242000000\"",
    "paragraph_id": "0001628280-26-057406:facts:ContractWithCustomerLiability:2026-07-03"
  },
  {
    "id": "revenue_recognition_tagged_revenue_from_opening_contract_liabilities",
    "what_changed": "Revenue recognized in fiscal 2026 out of contract liabilities (ContractWithCustomerLiabilityRevenueRecognized) is 23000000.",
    "account": "ContractWithCustomerLiabilityRevenueRecognized",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"23000000\"",
    "paragraph_id": "0001628280-26-057406:facts:ContractWithCustomerLiabilityRevenueRecognized:2025-06-28..2026-07-03"
  },
  {
    "id": "estimates_and_discretion_tagged_cumulative_catch_up_revenue_adjustment",
    "what_changed": "The fiscal 2026 cumulative catch-up adjustment to revenue from a change in the estimate of transaction price is 1100000000. The third-quarter 10-Q printed 400000000 for the nine months to 2026-04-03. Revenue moved this much by an estimate change is a discretion item. The input does not split it by quarter, and no split is derived here.",
    "account": "ContractWithCustomerLiabilityCumulativeCatchUpAdjustmentToRevenueChangeInEstimateOfTransactionPrice",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "\"value\": \"1100000000\"",
    "paragraph_id": "0001628280-26-057406:facts:ContractWithCustomerLiabilityCumulativeCatchUpAdjustmentToRevenueChangeInEstimateOfTransactionPrice:2025-06-28..2026-07-03"
  },
  {
    "id": "revenue_recognition_tagged_remaining_performance_obligation_year_end",
    "what_changed": "The remaining performance obligation is 59800000000 at 2026-07-03.",
    "account": "RevenueRemainingPerformanceObligation",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "\"value\": \"59800000000\"",
    "paragraph_id": "0001628280-26-057406:facts:RevenueRemainingPerformanceObligation:2026-07-03"
  },
  {
    "id": "revenue_recognition_tagged_remaining_performance_obligation_third_quarter",
    "what_changed": "The third-quarter 10-Q prints the remaining performance obligation at 2026-04-03 as 41600000000. The 10-K prints 59800000000 at 2026-07-03.",
    "account": "RevenueRemainingPerformanceObligation",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "\"value\": \"41600000000\"",
    "paragraph_id": "0001628280-26-029401:facts:RevenueRemainingPerformanceObligation:2026-04-03"
  },
  {
    "id": "revenue_recognition_tagged_remaining_performance_obligation_percentage",
    "what_changed": "RevenueRemainingPerformanceObligationPercentage is 0.19 at 2026-07-03. The recognition window it refers to is not in the input.",
    "account": "RevenueRemainingPerformanceObligationPercentage",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"0.19\"",
    "paragraph_id": "0001628280-26-057406:facts:RevenueRemainingPerformanceObligationPercentage:2026-07-03"
  },
  {
    "id": "revenue_recognition_tagged_unbilled_contracts_receivable_year_end",
    "what_changed": "UnbilledContractsReceivable is 58700000000 at 2026-07-03, close in size to the 59800000000 remaining performance obligation. The third-quarter 10-Q printed 41200000000 for 2026-04-03. This input does not establish what the tag measures.",
    "account": "UnbilledContractsReceivable",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "\"value\": \"58700000000\"",
    "paragraph_id": "0001628280-26-057406:facts:UnbilledContractsReceivable:2026-07-03"
  },
  {
    "id": "revenue_recognition_tagged_top_ten_customer_revenue_concentration",
    "what_changed": "The top ten customers' share of revenue is 0.44 for fiscal 2026. The 10-K prints 0.40 for fiscal 2025 and 0.41 for fiscal 2024. One customer is printed at 0.10 of fiscal 2026 revenue.",
    "account": "ConcentrationRiskPercentage1 (revenue, top ten customers)",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"0.44\"",
    "paragraph_id": "0001628280-26-057406:facts:ConcentrationRiskPercentage1:2025-06-28..2026-07-03:srt:MajorCustomersAxis=sndk:TopTenCustomersMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:RevenueFromContractWithCustomerMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember"
  },
  {
    "id": "revenue_recognition_tagged_single_customer_receivable_concentration",
    "what_changed": "One customer holds 0.19 of accounts receivable at fiscal 2026 year-end, against 0.11 at fiscal 2025 year-end. A second customer is printed at 0.12 of fiscal 2026 receivables.",
    "account": "ConcentrationRiskPercentage1 (accounts receivable, one customer)",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"0.19\"",
    "paragraph_id": "0001628280-26-057406:facts:ConcentrationRiskPercentage1:2025-06-28..2026-07-03:srt:MajorCustomersAxis=sndk:OneCustomerMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:AccountsReceivableMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember"
  },
  {
    "id": "revenue_recognition_tagged_datacenter_revenue_full_year",
    "what_changed": "Datacenter revenue is 5153000000 for fiscal 2026, against 960000000 for fiscal 2025 and 325000000 for fiscal 2024. The release prints Datacenter up 437%.",
    "account": "RevenueFromContractWithCustomerExcludingAssessedTax (Datacenter)",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"5153000000\"",
    "paragraph_id": "0001628280-26-057406:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2025-06-28..2026-07-03:srt:ProductOrServiceAxis=sndk:DatacenterMember"
  },
  {
    "id": "revenue_recognition_tagged_hong_kong_revenue_full_year",
    "what_changed": "Revenue attributed to Hong Kong is 5126000000 for fiscal 2026, against 1301000000 for fiscal 2025. China is printed at 4503000000 against 2040000000, and rest of Asia at 4612000000 against 1116000000.",
    "account": "RevenueFromContractWithCustomerExcludingAssessedTax (Hong Kong)",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"5126000000\"",
    "paragraph_id": "0001628280-26-057406:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2025-06-28..2026-07-03:srt:StatementGeographicalAxis=country:HK"
  },
  {
    "id": "estimates_and_discretion_tagged_inventory_write_down_full_year",
    "what_changed": "The inventory write-down is 91000000 for fiscal 2026, against 45000000 for fiscal 2025 and -22000000 for fiscal 2024.",
    "account": "InventoryWriteDown",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"91000000\"",
    "paragraph_id": "0001628280-26-057406:facts:InventoryWriteDown:2025-06-28..2026-07-03"
  },
  {
    "id": "estimates_and_discretion_tagged_inventory_valuation_reserve_year_end",
    "what_changed": "InventoryValuationReserves is 125000000 at 2026-07-03 and 126000000 at 2025-06-27. No quarter has a reserve row, so the history is two points and insufficient.",
    "account": "InventoryValuationReserves",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"125000000\"",
    "paragraph_id": "0001628280-26-057406:facts:InventoryValuationReserves:2026-07-03"
  },
  {
    "id": "estimates_and_discretion_tagged_warranty_accruals_issued",
    "what_changed": "Warranties issued are 62000000 in fiscal 2026 and 27000000 in fiscal 2025.",
    "account": "StandardProductWarrantyAccrualWarrantiesIssued",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"62000000\"",
    "paragraph_id": "0001628280-26-057406:facts:StandardProductWarrantyAccrualWarrantiesIssued:2025-06-28..2026-07-03"
  },
  {
    "id": "estimates_and_discretion_tagged_warranty_payments",
    "what_changed": "Warranty payments are 30000000 in fiscal 2026 and 35000000 in fiscal 2025.",
    "account": "StandardProductWarrantyAccrualPayments",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"30000000\"",
    "paragraph_id": "0001628280-26-057406:facts:StandardProductWarrantyAccrualPayments:2025-06-28..2026-07-03"
  },
  {
    "id": "estimates_and_discretion_tagged_warranty_pre_existing_release",
    "what_changed": "The change in estimate for pre-existing warranties is -28000000 in fiscal 2026, against 4000000 in fiscal 2025. A negative change on pre-existing warranties releases earlier accruals into income. The year-end accrual prints as 48000000, against 44000000 a year earlier and 73000000.0 at 2026-04-03 in the quarters-back-1 trend cell.",
    "account": "StandardProductWarrantyAccrualPreexistingIncreaseDecrease",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "\"value\": \"-28000000\"",
    "paragraph_id": "0001628280-26-057406:facts:StandardProductWarrantyAccrualPreexistingIncreaseDecrease:2025-06-28..2026-07-03"
  },
  {
    "id": "estimates_and_discretion_tagged_effective_tax_rate_full_year",
    "what_changed": "The effective tax rate is 0.12 for fiscal 2026. The 10-K prints -0.11 for fiscal 2025 and -0.34 for fiscal 2024.",
    "account": "EffectiveIncomeTaxRateContinuingOperations",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"0.12\"",
    "paragraph_id": "0001628280-26-057406:facts:EffectiveIncomeTaxRateContinuingOperations:2025-06-28..2026-07-03"
  },
  {
    "id": "estimates_and_discretion_tagged_unrecognized_tax_benefits_year_end",
    "what_changed": "Unrecognized tax benefits are 323000000 at 2026-07-03. The 10-K prints 140000000 at 2025-06-27. The 10-Qs printed 196000000 at 2026-01-02 and 253000000 at 2026-04-03. Accrued penalties and interest are 16000000 at 2026-07-03.",
    "account": "UnrecognizedTaxBenefits",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "\"value\": \"323000000\"",
    "paragraph_id": "0001628280-26-057406:facts:UnrecognizedTaxBenefits:2026-07-03"
  },
  {
    "id": "estimates_and_discretion_tagged_unrecognized_tax_benefits_prior_year_end",
    "what_changed": "The 10-K prints unrecognized tax benefits at 2025-06-27 as 140000000, with 47000000 at 2024-06-28 and 25000000 at 2023-06-30.",
    "account": "UnrecognizedTaxBenefits",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"140000000\"",
    "paragraph_id": "0001628280-26-057406:facts:UnrecognizedTaxBenefits:2025-06-27"
  },
  {
    "id": "estimates_and_discretion_tagged_unrecognized_tax_benefits_current_position_increases",
    "what_changed": "Increases to unrecognized tax benefits from current-period tax positions are 168000000 for fiscal 2026. The 10-Qs printed 29000000 for six months and 95000000 for nine months.",
    "account": "UnrecognizedTaxBenefitsIncreasesResultingFromCurrentPeriodTaxPositions",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"168000000\"",
    "paragraph_id": "0001628280-26-057406:facts:UnrecognizedTaxBenefitsIncreasesResultingFromCurrentPeriodTaxPositions:2025-06-28..2026-07-03"
  },
  {
    "id": "estimates_and_discretion_tagged_tax_contingencies_reconciling_item",
    "what_changed": "The fiscal 2026 rate reconciliation carries a tax-contingency reconciling item of 70000000.",
    "account": "IncomeTaxReconciliationTaxContingencies",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"70000000\"",
    "paragraph_id": "0001628280-26-057406:facts:IncomeTaxReconciliationTaxContingencies:2025-06-28..2026-07-03"
  },
  {
    "id": "estimates_and_discretion_tagged_malaysia_tax_holiday",
    "what_changed": "The Malaysia tax-holiday reconciling item is 492000000 for fiscal 2026, printed with a 0.04 rate effect. Malaysia pre-tax income is also printed at 492000000 for the year (82000000 in fiscal 2025).",
    "account": "IncomeTaxReconciliationTaxHolidays (Malaysia)",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"492000000\"",
    "paragraph_id": "0001628280-26-057406:facts:IncomeTaxReconciliationTaxHolidays:2025-06-28..2026-07-03:us-gaap:IncomeTaxAuthorityAxis=country:MY"
  },
  {
    "id": "estimates_and_discretion_tagged_deferred_tax_valuation_allowance",
    "what_changed": "The deferred tax asset valuation allowance is 118000000 at 2026-07-03, against 61000000 at 2025-06-27.",
    "account": "DeferredTaxAssetsValuationAllowance",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"118000000\"",
    "paragraph_id": "0001628280-26-057406:facts:DeferredTaxAssetsValuationAllowance:2026-07-03"
  },
  {
    "id": "earnings_quality_tagged_income_taxes_paid_against_current_expense",
    "what_changed": "Income taxes paid are 146000000 for fiscal 2026, while current income tax expense is printed at 1464000000. The release shows current income tax payable of 1,286 at July 3, 2026, against 43 a year earlier, and a cash-flow change in income taxes payable of 1,370. Python computed no ratio between these figures.",
    "account": "IncomeTaxesPaidNet; CurrentIncomeTaxExpenseBenefit",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "\"value\": \"146000000\"",
    "paragraph_id": "0001628280-26-057406:facts:IncomeTaxesPaidNet:2025-06-28..2026-07-03"
  },
  {
    "id": "earnings_quality_tagged_equity_securities_gain_full_year",
    "what_changed": "The fiscal 2026 unrealized gain on equity securities measured at fair value through net income is 808000000. It sits in non-operating income, and the release excludes it from non-GAAP results. One year is insufficient for a trend claim.",
    "account": "EquitySecuritiesFvNiUnrealizedGainLoss",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "\"value\": \"808000000\"",
    "paragraph_id": "0001628280-26-057406:facts:EquitySecuritiesFvNiUnrealizedGainLoss:2025-06-28..2026-07-03"
  },
  {
    "id": "earnings_quality_tagged_nanya_unrealized_gain",
    "what_changed": "The Nanya Technology holding accounts for 807000000 of the fiscal 2026 unrealized equity-securities gain. The 10-K prints a 0.039 ownership stake at 2026-04-08 and 970000000 of marketable equity purchases in the year.",
    "account": "EquitySecuritiesFvNiUnrealizedGainLoss (Nanya)",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "\"value\": \"807000000\"",
    "paragraph_id": "0001628280-26-057406:facts:EquitySecuritiesFvNiUnrealizedGainLoss:2025-06-28..2026-07-03:srt:OwnershipAxis=sndk:NanyaTechnologyCorporationMember"
  },
  {
    "id": "earnings_quality_tagged_deferred_tax_liability_unrealized_gains",
    "what_changed": "The deferred tax liability on unrealized gains on securities is 172000000 at 2026-07-03, against 0 at 2025-06-27.",
    "account": "DeferredTaxLiabilitiesUnrealizedGainsOnTradingSecurities",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"172000000\"",
    "paragraph_id": "0001628280-26-057406:facts:DeferredTaxLiabilitiesUnrealizedGainsOnTradingSecurities:2026-07-03"
  },
  {
    "id": "earnings_quality_tagged_litigation_settlement_expense",
    "what_changed": "Tagged litigation settlement expense for fiscal 2026 is 93000000. The release's fiscal 2026 'Other, net' non-GAAP adjustment prints as 111 and is described as including legal-settlement charges. The input computes no reconciliation between the two figures.",
    "account": "LitigationSettlementExpense",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"93000000\"",
    "paragraph_id": "0001628280-26-057406:facts:LitigationSettlementExpense:2025-06-28..2026-07-03"
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_tagged_guarantee_maximum_exposure",
    "what_changed": "The maximum exposure under related-party guarantees is 923000000 at 2026-07-03. The 10-K also prints 149000000000.0 in JPY on the same axis.",
    "account": "GuaranteeObligationsMaximumExposure (related party)",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"923000000\"",
    "paragraph_id": "0001628280-26-057406:facts:GuaranteeObligationsMaximumExposure:2026-07-03:us-gaap:RelatedPartyTransactionsByRelatedPartyAxis=us-gaap:RelatedPartyMember"
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_tagged_variable_interest_maximum_loss",
    "what_changed": "The maximum loss exposure to related-party variable interest entities is 2897000000 at 2026-07-03.",
    "account": "VariableInterestEntityEntityMaximumLossExposureAmount",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"2897000000\"",
    "paragraph_id": "0001628280-26-057406:facts:VariableInterestEntityEntityMaximumLossExposureAmount:2026-07-03:us-gaap:RelatedPartyTransactionsByRelatedPartyAxis=us-gaap:RelatedPartyMember"
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_tagged_extension_agreement_commitment",
    "what_changed": "The related-party commitment under extension agreements, tagged at 2026-01-29, is 1200000000.",
    "account": "OtherCommitment (extension agreements, related party)",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"1200000000\"",
    "paragraph_id": "0001628280-26-057406:facts:OtherCommitment:2026-01-29:us-gaap:OtherCommitmentsAxis=sndk:ExtensionAgreementsMember,us-gaap:RelatedPartyTransactionsByRelatedPartyAxis=us-gaap:RelatedPartyMember"
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_tagged_payments_to_equity_method_investees",
    "what_changed": "Payments to equity-method investees (related parties) are 3600000000 for fiscal 2026, against 3400000000 in each of fiscal 2025 and fiscal 2024.",
    "account": "PaymentsToAcquireEquityMethodInvestments (equity-method investees)",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"3600000000\"",
    "paragraph_id": "0001628280-26-057406:facts:PaymentsToAcquireEquityMethodInvestments:2025-06-28..2026-07-03:us-gaap:AccountsNotesLoansAndFinancingReceivablesByLegalEntityOfCounterpartyTypeAxis=us-gaap:EquityMethodInvesteeMember,us-gaap:RelatedPartyTransactionsByRelatedPartyAxis=us-gaap:RelatedPartyMember"
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_tagged_related_party_inventory",
    "what_changed": "InventoryGross tagged with the related-party member is 1295000000 at 2026-07-03, against total InventoryNet of 2698000000. The tag pairing is reported as printed and not interpreted further.",
    "account": "InventoryGross (related party)",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"1295000000\"",
    "paragraph_id": "0001628280-26-057406:facts:InventoryGross:2026-07-03:us-gaap:RelatedPartyTransactionsByRelatedPartyAxis=us-gaap:RelatedPartyMember"
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_tagged_flash_forward_notes_receivable",
    "what_changed": "Notes receivable from Flash Forward Ltd. (related party) are 543000000 at 2026-07-03, against 316000000 at 2025-06-27. Payments to acquire notes receivable in fiscal 2026 are 462000000.",
    "account": "NotesReceivableNet (Flash Forward Ltd.)",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"543000000\"",
    "paragraph_id": "0001628280-26-057406:facts:NotesReceivableNet:2026-07-03:us-gaap:AccountsNotesLoansAndFinancingReceivablesByLegalEntityOfCounterpartyTypeAxis=sndk:FlashForwardLtdMember,us-gaap:RelatedPartyTransactionsByRelatedPartyAxis=us-gaap:RelatedPartyMember"
  },
  {
    "id": "liquidity_and_capital_tagged_long_term_debt_prior_year_end",
    "what_changed": "Long-term debt is 1849000000 at 2025-06-27. The 10-K prints 0 at 2026-07-03 and debt repayments of 1900000000 in fiscal 2026.",
    "account": "LongTermDebt",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"1849000000\"",
    "paragraph_id": "0001628280-26-057406:facts:LongTermDebt:2025-06-27"
  },
  {
    "id": "liquidity_and_capital_tagged_debt_extinguishment_loss",
    "what_changed": "The loss on extinguishing the Term B loan, tagged on 2026-03-04, is -46000000.",
    "account": "GainsLossesOnExtinguishmentOfDebt",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"-46000000\"",
    "paragraph_id": "0001628280-26-057406:facts:GainsLossesOnExtinguishmentOfDebt:2026-03-04..2026-03-04:us-gaap:CreditFacilityAxis=sndk:TermBLoanMember,us-gaap:LongtermDebtTypeAxis=us-gaap:LineOfCreditMember"
  },
  {
    "id": "liquidity_and_capital_tagged_share_repurchases_cash",
    "what_changed": "Cash paid to repurchase common stock is 4524000000 in fiscal 2026 and 0 in fiscal 2025. Treasury stock acquired at cost prints as 4537000000, and excise tax payable on repurchases is 37000000.",
    "account": "PaymentsForRepurchaseOfCommonStock",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "\"value\": \"4524000000\"",
    "paragraph_id": "0001628280-26-057406:facts:PaymentsForRepurchaseOfCommonStock:2025-06-28..2026-07-03"
  },
  {
    "id": "liquidity_and_capital_tagged_remaining_repurchase_authorization",
    "what_changed": "The remaining repurchase authorization is 1500000000 at 2026-07-03. The release says the Board approved an additional $14 billion program, bringing total remaining authorization to $15.5 billion.",
    "account": "StockRepurchaseProgramRemainingAuthorizedRepurchaseAmount1",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "\"value\": \"1500000000\"",
    "paragraph_id": "0001628280-26-057406:facts:StockRepurchaseProgramRemainingAuthorizedRepurchaseAmount1:2026-07-03"
  },
  {
    "id": "liquidity_and_capital_tagged_purchase_obligations_year_end",
    "what_changed": "Purchase obligations are 5892000000 at 2026-07-03. The third-quarter 10-Q printed 7107000000 at 2026-04-03, and an earlier print was 2539000000 at 2026-01-02.",
    "account": "PurchaseObligation",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "\"value\": \"5892000000\"",
    "paragraph_id": "0001628280-26-057406:facts:PurchaseObligation:2026-07-03"
  },
  {
    "id": "liquidity_and_capital_tagged_marketable_equity_purchase",
    "what_changed": "Purchases of marketable equity securities are 970000000 in fiscal 2026, and 0 in both fiscal 2025 and fiscal 2024.",
    "account": "PaymentsToAcquireEquitySecuritiesFvNi",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "\"value\": \"970000000\"",
    "paragraph_id": "0001628280-26-057406:facts:PaymentsToAcquireEquitySecuritiesFvNi:2025-06-28..2026-07-03"
  },
  {
    "id": "across_documents_release_refund_liabilities_balance",
    "what_changed": "The release balance sheet prints refund liabilities of 1,500 at July 3, 2026, against 126 at June 27, 2025. This matches the 10-K refund-liability facts (1500000000 and 126000000).",
    "account": "Refund liabilities (release balance sheet)",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "| Refund liabilities | 1,500 |  |  | 126 |  |",
    "paragraph_id": "0001628280-26-053346:8k_2_02:47"
  },
  {
    "id": "across_documents_release_contract_liabilities_balance",
    "what_changed": "The release balance sheet prints current contract liabilities of 849, against 25, plus a separate non-current line of 393. This matches the 10-K facts.",
    "account": "Contract liabilities (release balance sheet)",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "| Contract liabilities | 849 |  |  | 25 |  |",
    "paragraph_id": "0001628280-26-053346:8k_2_02:47"
  },
  {
    "id": "across_documents_release_accrued_expenses_prior_year",
    "what_changed": "The release prints accrued expenses of 274 for June 27, 2025, the same as the 10-K's re-presented AccruedLiabilitiesCurrent. The second- and third-quarter 10-Qs printed 425000000 and 400000000 for that date.",
    "account": "Accrued expenses (release balance sheet)",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "| Accrued expenses | 313 |  |  | 274 |  |",
    "paragraph_id": "0001628280-26-053346:8k_2_02:47"
  },
  {
    "id": "across_documents_release_noncurrent_income_tax_payable",
    "what_changed": "The release prints non-current income tax payable of 258 at July 3, 2026 and 131 at June 27, 2025, on its own line. For that June 27, 2025 date, OtherLiabilitiesNoncurrent printed as 496000000 in the second-quarter 10-Q and 365000000 later. No reconciliation is in the input.",
    "account": "Income tax payable, non-current (release balance sheet)",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "| Income tax payable, non-current | 258 |  |  | 131 |  |",
    "paragraph_id": "0001628280-26-053346:8k_2_02:47"
  },
  {
    "id": "across_documents_release_current_income_tax_payable",
    "what_changed": "The release balance sheet prints current income tax payable of 1,286 at July 3, 2026, against 43 at June 27, 2025. The 10-K tags income taxes paid of 146000000 for the year.",
    "account": "Income tax payable, current (release balance sheet)",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "| Income tax payable, current | 1,286 |  |  | 43 |  |",
    "paragraph_id": "0001628280-26-053346:8k_2_02:47"
  },
  {
    "id": "across_documents_release_refund_liability_cash_flow",
    "what_changed": "The release cash flow shows a refund-liability change of 1,360 in the fourth quarter (4 a year earlier), and 1,374 for fiscal 2026 (25 in fiscal 2025). No Python fourth-quarter derivation exists to check it against.",
    "account": "Refund liability (release cash flow)",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "| Refund liability | 1,360 |  |  | 4 |  |  | 1,374 |  |  | 25 |  |",
    "paragraph_id": "0001628280-26-053346:8k_2_02:57"
  },
  {
    "id": "across_documents_release_receivables_cash_flow",
    "what_changed": "The release cash flow shows receivables changes of (1,982) in the fourth quarter and (3,640) for fiscal 2026. The fourth-quarter figure is the company's own; Python derived none.",
    "account": "Accounts receivable, net (release cash flow)",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "| Accounts receivable, net | (1,982) |  |  | (89) |  |  | (3,640) |  |  | (100) |  |",
    "paragraph_id": "0001628280-26-053346:8k_2_02:57"
  },
  {
    "id": "across_documents_release_nbm_payments_excluded_from_adjusted_free_cash_flow",
    "what_changed": "Adjusted free cash flow deducts the impact of NBM prepayments and deposits: (1,938) in the fourth quarter, (538) in the third quarter and (2,476) for fiscal 2026. By the release's definition these customer cash flows sit inside operating cash flow, which is 11,671 for the year.",
    "account": "Impact of NBM prepayments and deposits (release reconciliation)",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "| Impact of NBM prepayments and deposits | (1,938) |  |  | (538) |  |  | — |  |  | (2,476) |  |  | — |  |",
    "paragraph_id": "0001628280-26-053346:8k_2_02:67"
  },
  {
    "id": "across_documents_release_nbm_payments_rationale",
    "what_changed": "The release says it adjusts for NBM payments because they are not indicative of core underlying cash flows. The input does not tie these prepayments and deposits to particular balance-sheet lines.",
    "account": "NBM Payments (release definition)",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "The Company is adjusting for the NBM Payments because the Company believes that these cash flows are not indicative of the core underlying cash flows of the Company’s business.",
    "paragraph_id": "0001628280-26-053346:8k_2_02:81"
  },
  {
    "id": "across_documents_release_other_net_non_gaap_adjustment",
    "what_changed": "The release's 'Other, net' non-GAAP adjustment prints as 111 for fiscal 2026 and 1 for the third quarter. The 10-K tags litigation settlement expense of 93000000 for the year. The input does not reconcile the two.",
    "account": "Other, net (release non-GAAP reconciliation)",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "| Other, net | — |  |  | 1 |  |  | (2) |  |  | 111 |  |  | (9) |  |",
    "paragraph_id": "0001628280-26-053346:8k_2_02:67"
  },
  {
    "id": "across_documents_release_legal_matters_description",
    "what_changed": "The release describes fiscal 2026 'Other adjustments' as charges to settle certain previously existing legal matters, and excludes them from non-GAAP results.",
    "account": "Other adjustments (release prose)",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "For the year ended July 3, 2026, Other adjustments include charges for the settlement of certain previously existing legal matters.",
    "paragraph_id": "0001628280-26-053346:8k_2_02:79"
  },
  {
    "id": "across_documents_release_income_tax_adjustments",
    "what_changed": "The release's non-GAAP income tax adjustments are (4) in the fourth quarter, (48) in the third quarter and (60) for fiscal 2026.",
    "account": "Income tax adjustments (release non-GAAP reconciliation)",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "| Income tax adjustments | (4) |  |  | (48) |  |  | (16) |  |  | (60) |  |  | 22 |  |",
    "paragraph_id": "0001628280-26-053346:8k_2_02:67"
  },
  {
    "id": "across_documents_release_tax_reserve_remeasurement_description",
    "what_changed": "The release says income tax adjustments include re-measuring unrecognized tax benefits on positions taken in prior quarters. The prior-period-position increases for that same account print non-cumulatively across the 10-Qs and the 10-K (35000000, 29000000, 31000000).",
    "account": "Unrecognized tax benefits (release prose)",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "The income tax adjustments also include the re-measurement of certain unrecognized tax benefits primarily related to tax positions taken in prior quarters, including interest.",
    "paragraph_id": "0001628280-26-053346:8k_2_02:80"
  },
  {
    "id": "across_documents_release_goodwill_impairment_rounded",
    "what_changed": "The release describes the fiscal 2025 goodwill impairment as $1.8 billion, and its statement of operations shows 1,830. The 10-K tags both 1800000000 and 1830000000 for the period.",
    "account": "Goodwill impairment (release prose)",
    "expected_direction": "none",
    "horizon": "next annual filing",
    "quote": "resulting in the recognition of a $1.8 billion impairment charge for the year ended June 27, 2025.",
    "paragraph_id": "0001628280-26-053346:8k_2_02:71"
  },
  {
    "id": "across_documents_release_new_business_model_agreements",
    "what_changed": "The release says five more new-business-model agreements have been signed since the April call. The refund- and contract-liability balances and the NBM prepayment adjustment all arise in the same fiscal year. The input does not link specific agreements to specific balances.",
    "account": "New Business Model agreements (release prose)",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "we have signed five additional agreements, including three NBMs with new customers and two deals expanding on previously signed NBMs.",
    "paragraph_id": "0001628280-26-053346:8k_2_02:8"
  },
  {
    "id": "across_documents_release_buyback_authorization",
    "what_changed": "The release prints an additional $14 billion buyback authorization and total remaining authorization of $15.5 billion. The 10-K's period-end fact for remaining authorization is 1500000000.",
    "account": "Share repurchase authorization (release prose)",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "with Sandisk’s Board of Directors approving an additional $14 billion buyback program, bringing total remaining authorization to $15.5 billion.",
    "paragraph_id": "0001628280-26-053346:8k_2_02:9"
  },
  {
    "id": "revenue_recognition_release_price_and_volume_mix",
    "what_changed": "The release attributes sequential revenue growth about one-third to higher volume and two-thirds to higher pricing. Price-led growth is the backdrop to the refund-liability balance and the cumulative catch-up revenue adjustment reported above.",
    "account": "Revenue (release prose)",
    "expected_direction": "none",
    "horizon": "next quarterly filing",
    "quote": "Sequential revenue growth came approximately one-third from higher volumes and two-thirds from higher pricing.",
    "paragraph_id": "0001628280-26-053346:8k_2_02:6"
  },
  {
    "id": "results_against_expectations_first_quarter_revenue_guidance",
    "what_changed": "Management guides fiscal first-quarter 2027 revenue to $10.30 to $10.80 billion. The same release prints fourth-quarter revenue of $8,965 million. The direction comes from management's guidance, not from a derived figure. The input holds no consensus or outside expectation, so results against expectations cannot be judged: insufficient.",
    "account": "Revenue guidance (release prose)",
    "expected_direction": "up",
    "horizon": "fiscal first quarter 2027",
    "quote": "Expect first quarter 2027 revenue to be in the range of $10.30 billion to $10.80 billion",
    "paragraph_id": "0001628280-26-053346:8k_2_02:10"
  }
]
```

## Seen in the notes

None of the facts in `input_numbers.json` carries a field saying whether its element sat inside a note. The fields present are id, paragraph_id, tag, prefix, namespace, context, context_ref, unit, decimals, value, number, nil, form, source_accession and filing_date. The instructions say this split comes from the extraction marker, not from my judgment, so I have routed no fact here.

Several facts quoted under the first heading look like note tables: the warranty rollforward, the remaining performance obligation, the tax rate reconciliation, the unrecognized-tax-benefit rollforward, customer concentration, and related-party guarantees and commitments. Read their placement as "marker absent", not as "known to come from a statement".

```json
[]
```
