<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# LITE numbers reader report: 10-K 0001628280-26-057358 (fiscal year ended 2026-06-27)

## Before the items

**Run check.** Four files were read in full: `input_8k.md`, `input_numbers.json`, `input_prior_predictions.md` and `input_trends.json`. None of them holds prices, abnormal returns, short interest, another company's files, a prior run's probability or an outcome window, so the run is not broken.

**Prior flags.** There are none. `input_prior_predictions.md` says "None on record."

**Inputs this run does not have.**
- No articulation-check file.
- No restatement-trace file.
- No fourth-quarter derivation output.

So no Python-computed articulation gap exists to report. The restated prior values below are rows in `input_numbers.json` where the 10-K prints a different value than an earlier 10-Q printed for the same period. Each item shows the values as printed; nothing was computed.

**quarters-back-0 is not reached by the record.** The trend table has no cells for that period. Its reason, as printed, begins: "no quarter ending within 20 days of 2026-06-27 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration". The same reason, with target end 2025-06-28, is printed for quarters-back-4. There is therefore no quarterly item for the triggering period. The 8-K's fourth-quarter figures appear below only as 8-K rows; no derived fourth-quarter trend value exists.

**The research_and_development_capitalized block of years-back-0 is not itemized.** It carries no paragraph_id, so it cannot be quoted. Its printed values are:

| Field | Value |
|---|---|
| book_value_with_rnd_capitalized | 5592100000.0 |
| earnings_with_rnd_capitalized | -6848420000.0 |
| research_and_development_amortization | 269820000.0 |
| research_and_development_asset | 948200000.0 |

Its capitalized_development_cost is missing because the record "tags none of us-gaap:CapitalizedComputerSoftwareAdditions in any period".

**How expected_direction is used.** For trend metrics and facts it gives the sign of the printed change: the trend table's change, or the direction between the two printed values. It is not a forecast. It is "none" where nothing moved or nothing can be compared, and where an item says the metric is `insufficient`. For items quoting the company's outlook, it gives the direction stated in the outlook.

---

## Seen in the statements

### Trend table, years-back-0: all 11 metrics

```json
{ "id": "earnings_quality_accruals_over_total_assets",
  "what_changed": "years-back-0 value -1.0518645227505987; year_over_year change -1.0280657221722216 against years-back-1. Formula inputs in the cell: NetIncomeLoss -6935100000.0, NetCashProvidedByUsedInOperatingActivities 751400000.0, Assets 7307500000.0. Position as printed: lowest of the 5 filled years. The years-back-1 cell prints value -0.023798800578377226 and position 'highest of the 5 filled years'.",
  "account": "Total accruals (net income less operating cash flow) over total assets",
  "expected_direction": "down",
  "horizon": "fiscal year 2025-06-29..2026-06-27 (years-back-0)",
  "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-057358:trends:accruals_over_total_assets:2025-06-29..2026-06-27" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue",
  "what_changed": "years-back-0 value 0.0051094890510948905; year_over_year change 0.004683957136201273 against years-back-1. Inputs: ContractWithCustomerLiabilityCurrent 15400000.0 and RevenueFromContractWithCustomerExcludingAssessedTax 3014000000.0. Position: highest of only 2 filled years on the same concepts; the other 3 filled years rest on a different concept and are not compared. Two comparable years do not support a trend claim: insufficient for a trend.",
  "account": "Contract liabilities (current) over revenue",
  "expected_direction": "up",
  "horizon": "fiscal year 2025-06-29..2026-06-27 (years-back-0)",
  "quote": "\"position_in_history\": \"highest of the 2 filled years on the same concepts; 3 other filled years rest on a different concept and are not compared\"",
  "paragraph_id": "0001628280-26-057358:trends:contract_liabilities_over_revenue:2025-06-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_soft_asset_share",
  "what_changed": "years-back-0 value 0.5617379404721177; year_over_year change -0.1426496670847126 against years-back-1. Inputs: Assets 7307500000.0, CashAndCashEquivalentsAtCarryingValue 2043500000.0, PropertyPlantAndEquipmentAndFinanceLeaseRightOfUseAssetAfterAccumulatedDepreciationAndAmortization 1159100000.0. Position: lowest of the 3 filled years on the same concepts; 2 other filled years rest on a different concept.",
  "account": "Soft assets (assets less PP&E less cash) over total assets",
  "expected_direction": "down",
  "horizon": "fiscal year 2025-06-29..2026-06-27 (years-back-0)",
  "quote": "\"position_in_history\": \"lowest of the 3 filled years on the same concepts; 2 other filled years rest on a different concept and are not compared\"",
  "paragraph_id": "0001628280-26-057358:trends:soft_asset_share:2025-06-29..2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio",
  "what_changed": "years-back-0 value 0.008195089581950896; year_over_year change -0.0005587098101463676 against years-back-1. Inputs: ProductWarrantyAccrual 24700000.0 and RevenueFromContractWithCustomerExcludingAssessedTax 3014000000.0. Position: third highest of the 5 filled years, the middle of its history. The years-back-1 cell prints value 0.008753799392097264 ('second highest of the 5 filled years').",
  "account": "Product warranty accrual over revenue",
  "expected_direction": "down",
  "horizon": "fiscal year 2025-06-29..2026-06-27 (years-back-0)",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0001628280-26-057358:trends:warranty_reserve_ratio:2025-06-29..2026-06-27" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_insufficient",
  "what_changed": "insufficient. The cell has no value. The record has no receivables row for 2026-06-27 under the three receivables concepts the table looks for. The same reason is printed for every period from quarters-back-1 to years-back-4, so the metric has zero filled periods in its history.",
  "account": "Receivables over revenue",
  "expected_direction": "none",
  "horizon": "fiscal year 2025-06-29..2026-06-27 (years-back-0)",
  "quote": "\"missing\": \"no row for receivables in 2026-06-27: us-gaap:AccountsReceivableNetCurrent, us-gaap:ReceivablesNetCurrent, us-gaap:AccountsReceivableNet is in the record, but not for this period\"",
  "paragraph_id": "0001628280-26-057358:trends:receivables_over_revenue:2025-06-29..2026-06-27" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_insufficient",
  "what_changed": "insufficient. The cell has no value because there is no receivables row for 2026-06-27. The metric has zero filled periods across the whole window.",
  "account": "Days sales outstanding",
  "expected_direction": "none",
  "horizon": "fiscal year 2025-06-29..2026-06-27 (years-back-0)",
  "quote": "\"missing\": \"no row for receivables in 2026-06-27: us-gaap:AccountsReceivableNetCurrent, us-gaap:ReceivablesNetCurrent, us-gaap:AccountsReceivableNet is in the record, but not for this period\"",
  "paragraph_id": "0001628280-26-057358:trends:days_sales_outstanding:2025-06-29..2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_insufficient",
  "what_changed": "insufficient. The cell has no value because there is no receivables row for 2026-06-27. The metric has zero filled periods across the whole window.",
  "account": "Allowance for doubtful accounts over receivables",
  "expected_direction": "none",
  "horizon": "fiscal year 2025-06-29..2026-06-27 (years-back-0)",
  "quote": "\"missing\": \"no row for receivables in 2026-06-27: us-gaap:AccountsReceivableNetCurrent, us-gaap:ReceivablesNetCurrent, us-gaap:AccountsReceivableNet is in the record, but not for this period\"",
  "paragraph_id": "0001628280-26-057358:trends:bad_debt_reserve_ratio:2025-06-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_insufficient",
  "what_changed": "insufficient. The cell has no value because there is no cost-of-revenue row for the year under the five concepts the table looks for. The metric has zero filled periods across the whole window.",
  "account": "Days sales of inventory",
  "expected_direction": "none",
  "horizon": "fiscal year 2025-06-29..2026-06-27 (years-back-0)",
  "quote": "\"missing\": \"no row for cost_of_revenue in 2025-06-29..2026-06-27: us-gaap:CostOfRevenue, us-gaap:CostOfGoodsAndServicesSold, us-gaap:CostOfGoodsSold, us-gaap:CostOfServices, us-gaap:CostOfSales is in the record, but not for this period\"",
  "paragraph_id": "0001628280-26-057358:trends:days_sales_of_inventory:2025-06-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_gross_margin_insufficient",
  "what_changed": "insufficient. The cell has no value because there is no cost-of-revenue row for the year. The metric has zero filled periods across the whole window. The trend table computed no gross margin; the 8-K's own GAAP gross margin percentages are company-stated figures, not trend cells.",
  "account": "Gross margin",
  "expected_direction": "none",
  "horizon": "fiscal year 2025-06-29..2026-06-27 (years-back-0)",
  "quote": "\"missing\": \"no row for cost_of_revenue in 2025-06-29..2026-06-27: us-gaap:CostOfRevenue, us-gaap:CostOfGoodsAndServicesSold, us-gaap:CostOfGoodsSold, us-gaap:CostOfServices, us-gaap:CostOfSales is in the record, but not for this period\"",
  "paragraph_id": "0001628280-26-057358:trends:gross_margin:2025-06-29..2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_insufficient",
  "what_changed": "insufficient. The cell has no value. The record tags no InventoryValuationReserves in any period, so the metric has zero filled periods.",
  "account": "Inventory valuation reserve ratio",
  "expected_direction": "none",
  "horizon": "fiscal year 2025-06-29..2026-06-27 (years-back-0)",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
  "paragraph_id": "0001628280-26-057358:trends:inventory_reserve_ratio:2025-06-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_insufficient",
  "what_changed": "insufficient. The cell has no value because no us-gaap concept carries non-GAAP net income. The metric has zero filled periods. The 8-K prints non-GAAP figures (see the non-GAAP item below), but no computed gap exists.",
  "account": "Gap between non-GAAP and GAAP net income",
  "expected_direction": "none",
  "horizon": "fiscal year 2025-06-29..2026-06-27 (years-back-0)",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0001628280-26-057358:trends:non_gaap_gap:2025-06-29..2026-06-27" }
```

### Changes of tag (a period rests on a different concept)

```json
{ "id": "structure_and_disclosure_changes_revenue_tag_switch_contract_liabilities_ratio",
  "what_changed": "Change of tag. The revenue in the quarterly contract_liabilities_over_revenue cells rests on RevenueFromContractWithCustomerIncludingAssessedTax in fiscal 2026 quarters and on RevenueFromContractWithCustomerExcludingAssessedTax a year earlier, so no year-over-year change is computed. The same tag change is printed on the quarters-back-2 cell (0001628280-26-057358:trends:contract_liabilities_over_revenue:2025-09-28..2025-12-27, against quarters-back-6) and the quarters-back-3 cell (0001628280-26-057358:trends:contract_liabilities_over_revenue:2025-06-29..2025-09-27, against quarters-back-7). The quarters-back-1 cell's position is 'highest of the 3 filled quarters on the same concepts'.",
  "account": "Revenue concept used in contract liabilities / revenue",
  "expected_direction": "none",
  "horizon": "quarters-back-1 against quarters-back-5 (also quarters-back-2 and quarters-back-3)",
  "quote": "revenue: us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax in quarters-back-1 and us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax in quarters-back-5",
  "paragraph_id": "0001628280-26-057358:trends:contract_liabilities_over_revenue:2025-12-28..2026-03-28" }
```

```json
{ "id": "structure_and_disclosure_changes_revenue_tag_switch_warranty_ratio",
  "what_changed": "Change of tag. The quarterly warranty_reserve_ratio cells use revenue tagged IncludingAssessedTax in fiscal 2026 and ExcludingAssessedTax a year earlier, so no year-over-year change is computed. The same is printed on the quarters-back-2 cell (0001628280-26-057358:trends:warranty_reserve_ratio:2025-09-28..2025-12-27) and the quarters-back-3 cell (0001628280-26-057358:trends:warranty_reserve_ratio:2025-06-29..2025-09-27). The quarters-back-1 cell prints value 0.030925284512617515 and position 'second highest of the 3 filled quarters on the same concepts'.",
  "account": "Revenue concept used in warranty accrual / revenue",
  "expected_direction": "none",
  "horizon": "quarters-back-1 against quarters-back-5 (also quarters-back-2 and quarters-back-3)",
  "quote": "revenue: us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax in quarters-back-1 and us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax in quarters-back-5",
  "paragraph_id": "0001628280-26-057358:trends:warranty_reserve_ratio:2025-12-28..2026-03-28" }
```

```json
{ "id": "structure_and_disclosure_changes_contract_liabilities_tag_switch",
  "what_changed": "Change of tag. Contract liabilities rest on ContractWithCustomerLiabilityCurrent in years-back-1 and on ContractWithCustomerLiability in years-back-2, so years-back-1 is not compared with years-back-2. This is why the years-back-0 contract liability ratio has only 2 comparable years.",
  "account": "Contract liabilities concept",
  "expected_direction": "none",
  "horizon": "years-back-1 against years-back-2",
  "quote": "contract_liabilities: us-gaap:ContractWithCustomerLiabilityCurrent in years-back-1 and us-gaap:ContractWithCustomerLiability in years-back-2",
  "paragraph_id": "0001628280-26-057358:trends:contract_liabilities_over_revenue:2024-06-30..2025-06-28" }
```

```json
{ "id": "structure_and_disclosure_changes_property_plant_equipment_tag_switch",
  "what_changed": "Change of tag. PP&E rests on PropertyPlantAndEquipmentAndFinanceLeaseRightOfUseAssetAfterAccumulatedDepreciationAndAmortization in years-back-2 and on PropertyPlantAndEquipmentNet in years-back-3, so soft_asset_share is not compared across that boundary. This is why the years-back-0 soft asset share has only 3 comparable years.",
  "account": "Property, plant and equipment concept",
  "expected_direction": "none",
  "horizon": "years-back-2 against years-back-3",
  "quote": "property_plant_and_equipment: us-gaap:PropertyPlantAndEquipmentAndFinanceLeaseRightOfUseAssetAfterAccumulatedDepreciationAndAmortization in years-back-2 and us-gaap:PropertyPlantAndEquipmentNet in years-back-3",
  "paragraph_id": "0001628280-26-057358:trends:soft_asset_share:2023-07-02..2024-06-29" }
```

```json
{ "id": "structure_and_disclosure_changes_revenue_tagged_two_ways_in_annual_report",
  "what_changed": "The 10-K tags fiscal 2026 total revenue under both concepts with the same printed value. RevenueFromContractWithCustomerExcludingAssessedTax prints 3014000000 here; RevenueFromContractWithCustomerIncludingAssessedTax prints 3014000000 at 0001628280-26-057358:facts:RevenueFromContractWithCustomerIncludingAssessedTax:2025-06-29..2026-06-27. The trend table's annual cells take the Excluding concept; its fiscal 2026 quarterly cells take the Including concept. That is the source of the tag changes above.",
  "account": "Net revenue (concept choice)",
  "expected_direction": "none",
  "horizon": "fiscal year 2025-06-29..2026-06-27",
  "quote": "\"value\": \"3014000000\"",
  "paragraph_id": "0001628280-26-057358:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2025-06-29..2026-06-27" }
```

```json
{ "id": "structure_and_disclosure_changes_receivables_tagged_as_contract_assets",
  "what_changed": "The balance sheet line the 8-K calls 'Accounts receivable, net' (520.3 and 250.0) appears in the 10-K facts as ContractWithCustomerAssetNet: 520300000 at 2026-06-27 and 250000000.0 at 2025-06-28 (0001628280-26-057358:facts:ContractWithCustomerAssetNet:2025-06-28). No receivables concept the trend table reads carries it, so receivables_over_revenue, days_sales_outstanding and bad_debt_reserve_ratio are insufficient in every period.",
  "account": "Accounts receivable, net",
  "expected_direction": "up",
  "horizon": "balance sheet 2026-06-27 against 2025-06-28",
  "quote": "\"value\": \"520300000\"",
  "paragraph_id": "0001628280-26-057358:facts:ContractWithCustomerAssetNet:2026-06-27" }
```

```json
{ "id": "structure_and_disclosure_changes_cost_of_sales_tag_outside_trend_concepts",
  "what_changed": "Cost of sales for fiscal 2026 is tagged CostOfGoodsAndServiceExcludingDepreciationDepletionAndAmortization (1680500000), a concept outside the five the trend table looks for. That is why gross_margin and days_sales_of_inventory are insufficient. The 8-K prints the matching cost of sales line as 1,680.5 for the twelve months.",
  "account": "Cost of sales",
  "expected_direction": "up",
  "horizon": "fiscal year 2025-06-29..2026-06-27",
  "quote": "\"value\": \"1680500000\"",
  "paragraph_id": "0001628280-26-057358:facts:CostOfGoodsAndServiceExcludingDepreciationDepletionAndAmortization:2025-06-29..2026-06-27" }
```

### Restated prior values (an earlier filing reported the period differently)

```json
{ "id": "articulation_and_the_filed_history_greensboro_goodwill_restated",
  "what_changed": "Restated prior value. Goodwill for the Greensboro, North Carolina manufacturing facility acquisition at 2026-03-17 is 8400000 in the 10-K. The third-quarter 10-Q printed 5400000 for the same date and member (0001628280-26-030777:facts:Goodwill:2026-03-17:us-gaap:BusinessAcquisitionAxis=lite:ManufacturingFacilityInGreensboroNorthCarolinaMember, marked superseded_by 0001628280-26-057358).",
  "account": "Goodwill, Greensboro acquisition purchase price allocation",
  "expected_direction": "up",
  "horizon": "acquisition date 2026-03-17, as reported in the 10-Q (2026-05-06) and the 10-K (2026-08-17)",
  "quote": "\"value\": \"8400000\"",
  "paragraph_id": "0001628280-26-057358:facts:Goodwill:2026-03-17:us-gaap:BusinessAcquisitionAxis=lite:ManufacturingFacilityInGreensboroNorthCarolinaMember" }
```

```json
{ "id": "articulation_and_the_filed_history_greensboro_assumed_liabilities_restated",
  "what_changed": "Restated prior value. Other noncurrent liabilities assumed in the Greensboro acquisition, at 2026-03-28, are 9900000 in the 10-K. The third-quarter 10-Q printed 6900000 for the same period and member (0001628280-26-030777:facts:BusinessCombinationRecognizedIdentifiableAssetsAcquiredAndLiabilitiesAssumedNoncurrentLiabilitiesOther:2026-03-28:us-gaap:BusinessAcquisitionAxis=lite:ManufacturingFacilityInGreensboroNorthCarolinaMember).",
  "account": "Business combination, noncurrent liabilities assumed (other), Greensboro",
  "expected_direction": "up",
  "horizon": "2026-03-28, as reported in the 10-Q and the 10-K",
  "quote": "\"value\": \"9900000\"",
  "paragraph_id": "0001628280-26-057358:facts:BusinessCombinationRecognizedIdentifiableAssetsAcquiredAndLiabilitiesAssumedNoncurrentLiabilitiesOther:2026-03-28:us-gaap:BusinessAcquisitionAxis=lite:ManufacturingFacilityInGreensboroNorthCarolinaMember" }
```

```json
{ "id": "articulation_and_the_filed_history_cloud_light_contingent_consideration_sign_flip",
  "what_changed": "Restated prior value, with a sign change. The change in the Cloud Light contingent consideration liability for 2025-11-01..2025-11-30 is 27500000 in the 10-K, tagged with the CloudLightTechnologyLimitedMember. The third-quarter 10-Q printed -27500000 for the same concept and period with no acquisition member (0001628280-26-030777:facts:BusinessCombinationContingentConsiderationArrangementsChangeInAmountOfContingentConsiderationLiability1:2025-11-01..2025-11-30). The 8-K treats a 27.5 escrow settlement as a gain excluded from non-GAAP results.",
  "account": "Change in contingent consideration liability, Cloud Light",
  "expected_direction": "none",
  "horizon": "2025-11-01..2025-11-30, as reported in the 10-Q and the 10-K",
  "quote": "\"value\": \"27500000\"",
  "paragraph_id": "0001628280-26-057358:facts:BusinessCombinationContingentConsiderationArrangementsChangeInAmountOfContingentConsiderationLiability1:2025-11-01..2025-11-30:us-gaap:BusinessAcquisitionAxis=lite:CloudLightTechnologyLimitedMember" }
```

```json
{ "id": "structure_and_disclosure_changes_reportable_segment_count",
  "what_changed": "The third-quarter 10-Q tags NumberOfReportableSegments as 1 for the nine months ended 2026-03-28. The same filing tags 2 for fiscal 2025 (0001628280-26-030777:facts:NumberOfReportableSegments:2024-06-30..2025-06-28, superseded_by the 10-K). The 10-K then reports fiscal 2026 revenue under two segment members, Components and Systems. The record holds no fourth figure that reconciles the count.",
  "account": "Number of reportable segments",
  "expected_direction": "down",
  "horizon": "nine months 2025-06-29..2026-03-28 against fiscal 2025",
  "quote": "\"value\": \"1\"",
  "paragraph_id": "0001628280-26-030777:facts:NumberOfReportableSegments:2025-06-29..2026-03-28" }
```

### Across documents

```json
{ "id": "across_documents_segment_revenue_members_swapped",
  "what_changed": "In the 10-K, fiscal 2026 operating-segment revenue tagged with the SystemsMember is 2005600000 and with the ComponentsMember is 1008400000 (0001628280-26-057358:facts:RevenueFromContractWithCustomerIncludingAssessedTax:2025-06-29..2026-06-27:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=lite:ComponentsMember). The 8-K table (0001628280-26-055726:8k_2_02:27) prints Components 2,005.6 and Systems 1,008.4 for the same year. The 10-K's own product-concentration facts print Components 0.665 and Systems 0.335. Fiscal 2025 members agree with the 8-K: Components 1116300000 and Systems 528700000.",
  "account": "Segment net revenue, Components and Systems",
  "expected_direction": "none",
  "horizon": "fiscal year 2025-06-29..2026-06-27",
  "quote": "\"value\": \"2005600000\"",
  "paragraph_id": "0001628280-26-057358:facts:RevenueFromContractWithCustomerIncludingAssessedTax:2025-06-29..2026-06-27:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=lite:SystemsMember" }
```

```json
{ "id": "across_documents_other_charges_differ_between_reconciliation_tables",
  "what_changed": "Within the 8-K, fiscal 2025 'Other charges (income), net' is 12.1 in the Adjusted EBITDA reconciliation. The GAAP to non-GAAP reconciliations print 12.3 for the same twelve months: 'Other charges, net (7)' in 0001628280-26-055726:8k_2_02:65 and 'Other charges (income), net (7)' in 0001628280-26-055726:8k_2_02:66. The other four columns match.",
  "account": "Other charges (income), net, a non-GAAP adjustment",
  "expected_direction": "none",
  "horizon": "twelve months ended 2025-06-28",
  "quote": "| Other charges (income), net | 0.5 |  |  | 2.7 |  |  | (1.2) |  |  | 17.0 |  |  | 12.1 |  |",
  "paragraph_id": "0001628280-26-055726:8k_2_02:83" }
```

### Earnings quality

```json
{ "id": "earnings_quality_debt_extinguishment_loss",
  "what_changed": "Fiscal 2026 includes a loss on debt extinguishment of -7756600000. The 8-K attributes it to the equitization of the 2026, 2028 and 2029 convertible notes. The loss turns income from operations of 524.8 into a net loss of (6,935.1), and it drives the accruals metric above to the lowest of its 5 filled years. The 8-K describes it as one-time and non-cash.",
  "account": "Loss on debt extinguishment",
  "expected_direction": "down",
  "horizon": "fiscal year 2025-06-29..2026-06-27 (all in the fourth quarter per the 8-K)",
  "quote": "\"value\": \"-7756600000\"",
  "paragraph_id": "0001628280-26-057358:facts:GainsLossesOnExtinguishmentOfDebt:2025-06-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_extinguishment_loss_components",
  "what_changed": "The 8-K breaks the 7.8 billion loss into:\n- 7.8 billion of conversion value in excess of principal;\n- 3.1 million of transaction costs;\n- 2.9 million of unamortized issuance costs;\n- offset by 2.9 million of forfeited interest and a 1.6 million negotiated exchange discount.",
  "account": "Loss on debt extinguishment (components)",
  "expected_direction": "none",
  "horizon": "three and twelve months ended 2026-06-27",
  "quote": "Included in loss on debt extinguishment are $7.8 billion of conversion value in excess of principal amounts",
  "paragraph_id": "0001628280-26-055726:8k_2_02:72" }
```

```json
{ "id": "earnings_quality_income_tax_benefit_second_year",
  "what_changed": "The income tax line is a benefit of -237700000 for fiscal 2026. Fiscal 2025 was also a benefit, -198000000.0 (0001628280-26-057358:facts:IncomeTaxExpenseBenefit:2024-06-30..2025-06-28), and fiscal 2024 was an expense of 140800000. The effective tax rate prints 0.032 for fiscal 2026 and 1.1504 for fiscal 2025. Pre-tax loss splits into domestic -8018700000 and foreign 845900000.",
  "account": "Income tax expense (benefit)",
  "expected_direction": "down",
  "horizon": "fiscal year 2025-06-29..2026-06-27",
  "quote": "\"value\": \"-237700000\"",
  "paragraph_id": "0001628280-26-057358:facts:IncomeTaxExpenseBenefit:2025-06-29..2026-06-27" }
```

```json
{ "id": "earnings_quality_non_gaap_net_income_against_gaap_loss",
  "what_changed": "The 8-K reports non-GAAP net income of 326.3 for the fourth quarter and 782.3 for fiscal 2026. The GAAP figures are net losses of (7,161.7) and (6,935.1). The reconciliation removes the 7,756.6 extinguishment loss, removes the 27.5 escrow settlement, and applies non-GAAP tax reconciling adjustments of (361.1) for the quarter and (392.3) for the year. The trend table's non_gaap_gap cell is insufficient, so no computed gap exists.",
  "account": "Net income on non-GAAP basis",
  "expected_direction": "up",
  "horizon": "three and twelve months ended 2026-06-27",
  "quote": "| Net income on non-GAAP basis | $ | 326.3 |  |  | $ | 225.7 |  |  | $ | 63.3 |  |  | $ | 782.3 |  |  | $ | 146.4 |  |",
  "paragraph_id": "0001628280-26-055726:8k_2_02:66" }
```

```json
{ "id": "earnings_quality_escrow_settlement_gain",
  "what_changed": "Fiscal 2026 income includes a 27500000 gain tagged GainLossRelatedToLitigationSettlement, which the 8-K calls the Cloud Light escrow settlement. A 9.8 acquisition-related warranty provision was recorded in cost of sales. The 8-K removes the net benefit of 17.7 from non-GAAP results.",
  "account": "Escrow settlement (other income)",
  "expected_direction": "none",
  "horizon": "fiscal year 2025-06-29..2026-06-27",
  "quote": "\"value\": \"27500000\"",
  "paragraph_id": "0001628280-26-057358:facts:GainLossRelatedToLitigationSettlement:2025-06-29..2026-06-27" }
```

### Estimates and discretion

```json
{ "id": "estimates_and_discretion_deferred_tax_valuation_allowance_release",
  "what_changed": "The deferred tax asset valuation allowance is 189000000.0 at 2026-06-27, against 440800000 at 2025-06-28 (0001628280-26-057358:facts:DeferredTaxAssetsValuationAllowance:2025-06-28). Supporting facts:\n- The rate reconciliation's valuation-allowance line is -181400000 for fiscal 2026.\n- The valuation-allowance deductions line prints 273700000.\n- The balance-sheet deferred tax asset is 530.9, against 210.3 a year earlier.",
  "account": "Deferred tax asset valuation allowance",
  "expected_direction": "down",
  "horizon": "balance sheet 2026-06-27 against 2025-06-28",
  "quote": "\"value\": \"189000000.0\"",
  "paragraph_id": "0001628280-26-057358:facts:DeferredTaxAssetsValuationAllowance:2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_credit_loss_provision_small_against_receivable_growth",
  "what_changed": "Amounts charged to the allowance for credit losses are 100000 in fiscal 2026, against 3400000 in fiscal 2025. The allowance balance prints 3500000 at both 2025-06-28 and 2026-06-27. Over the same dates the accounts receivable line is 520.3 against 250.0 in the 8-K.",
  "account": "Allowance for credit losses, provision",
  "expected_direction": "down",
  "horizon": "fiscal year 2025-06-29..2026-06-27",
  "quote": "\"value\": \"100000\"",
  "paragraph_id": "0001628280-26-057358:facts:ValuationAllowancesAndReservesChargedToCostAndExpense:2025-06-29..2026-06-27:us-gaap:ValuationAllowancesAndReservesTypeAxis=us-gaap:AllowanceForCreditLossMember" }
```

```json
{ "id": "estimates_and_discretion_warranty_provisions_issued",
  "what_changed": "Warranty provisions issued were 25900000 in fiscal 2026, against 10200000 in fiscal 2025. Payments were 15600000 against 9800000. The accrual ends at 24700000, against 14400000. The 8-K says 9.8 of the year's provision is an acquisition-related warranty provision for Cloud Light legacy products.",
  "account": "Product warranty accrual, warranties issued",
  "expected_direction": "up",
  "horizon": "fiscal year 2025-06-29..2026-06-27",
  "quote": "\"value\": \"25900000\"",
  "paragraph_id": "0001628280-26-057358:facts:ProductWarrantyAccrualWarrantiesIssued:2025-06-29..2026-06-27" }
```

```json
{ "id": "estimates_and_discretion_unrecognized_tax_benefits",
  "what_changed": "Unrecognized tax benefits are 108400000 at 2026-06-27, against 98600000 at 2025-06-28. Additions for current-period positions are 16200000. 93800000 would affect the effective rate. Accrued interest and penalties are 14800000, against 12500000.",
  "account": "Unrecognized tax benefits",
  "expected_direction": "up",
  "horizon": "balance sheet 2026-06-27 against 2025-06-28",
  "quote": "\"value\": \"108400000\"",
  "paragraph_id": "0001628280-26-057358:facts:UnrecognizedTaxBenefits:2026-06-27" }
```

### Revenue recognition

```json
{ "id": "revenue_recognition_receivables_increase_in_cash_flow",
  "what_changed": "The cash flow statement's increase in accounts receivable is 270400000 for fiscal 2026, against 58700000 for fiscal 2025. Revenue is 3014000000 against 1645000000. No receivables-based trend metric is filled (see the insufficient items above).",
  "account": "Change in accounts receivable",
  "expected_direction": "up",
  "horizon": "fiscal year 2025-06-29..2026-06-27",
  "quote": "\"value\": \"270400000\"",
  "paragraph_id": "0001628280-26-057358:facts:IncreaseDecreaseInAccountsReceivable:2025-06-29..2026-06-27" }
```

```json
{ "id": "revenue_recognition_receivable_concentration_single_customer",
  "what_changed": "The largest customer (CustomerOneMember) holds 0.304 of accounts receivable for fiscal 2026, against 0.132 for fiscal 2025. CustomerTwoMember holds 0.107, against 0.110.",
  "account": "Accounts receivable concentration",
  "expected_direction": "up",
  "horizon": "fiscal year 2025-06-29..2026-06-27",
  "quote": "\"value\": \"0.304\"",
  "paragraph_id": "0001628280-26-057358:facts:ConcentrationRiskPercentage1:2025-06-29..2026-06-27:srt:MajorCustomersAxis=lite:CustomerOneMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:AccountsReceivableMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember" }
```

```json
{ "id": "revenue_recognition_revenue_concentration_single_customer",
  "what_changed": "CustomerAMember accounts for 0.266 of net revenue in fiscal 2026, against 0.154 in fiscal 2025 and 0.189 in fiscal 2024. CustomerBMember accounts for 0.150, against 0.160.",
  "account": "Revenue concentration",
  "expected_direction": "up",
  "horizon": "fiscal year 2025-06-29..2026-06-27",
  "quote": "\"value\": \"0.266\"",
  "paragraph_id": "0001628280-26-057358:facts:ConcentrationRiskPercentage1:2025-06-29..2026-06-27:srt:MajorCustomersAxis=lite:CustomerAMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:SalesRevenueNetMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember" }
```

### Liquidity and capital

```json
{ "id": "liquidity_and_capital_convertible_notes_classified_current",
  "what_changed": "The current portion of long-term debt is 1596900000 at 2026-06-27, against 10600000 at 2025-06-28. Long-term debt, noncurrent, is 40500000, against 2562600000. In the convertible-debt maturity table, principal due in the next twelve months prints 60200000 and principal after year five prints 1269800000. Both are printed values; the record holds no figure reconciling the classification.",
  "account": "Current portion of long-term debt",
  "expected_direction": "up",
  "horizon": "balance sheet 2026-06-27 against 2025-06-28",
  "quote": "\"value\": \"1596900000\"",
  "paragraph_id": "0001628280-26-057358:facts:LongTermDebtCurrent:2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_convertible_principal_outstanding",
  "what_changed": "Convertible note face amount outstanding is 1554300000 at 2026-06-27, against 2514700000 at 2025-06-28. By series the face amounts are:\n- 2026 notes 54800000;\n- 2028 notes 179600000;\n- 2029 notes 54900000;\n- 2032 notes 1265000000.\nThe 10-K also tags a further conversion of 757800000 dated 2026-08-14, after year end.",
  "account": "Convertible senior notes, principal",
  "expected_direction": "down",
  "horizon": "balance sheet 2026-06-27 against 2025-06-28, and the period after year end",
  "quote": "\"value\": \"1554300000\"",
  "paragraph_id": "0001628280-26-057358:facts:DebtInstrumentFaceAmount:2026-06-27:us-gaap:LongtermDebtTypeAxis=us-gaap:ConvertibleDebtMember" }
```

```json
{ "id": "liquidity_and_capital_series_a_convertible_preferred_issued",
  "what_changed": "Series A convertible preferred stock was issued on 2026-03-02 for consideration of 2000000000.0: 2900000 shares at 695.31 per share. The 8-K says basic EPS now uses the two-class method and diluted EPS assumes conversion.",
  "account": "Convertible preferred stock issuance",
  "expected_direction": "up",
  "horizon": "issued 2026-03-02, within fiscal 2026",
  "quote": "\"value\": \"2000000000.0\"",
  "paragraph_id": "0001628280-26-057358:facts:SaleOfStockConsiderationReceivedOnTransaction:2026-03-02..2026-03-02:us-gaap:SubsidiarySaleOfStockAxis=us-gaap:SeriesAPreferredStockMember" }
```

```json
{ "id": "liquidity_and_capital_cash_decline_in_final_quarter",
  "what_changed": "The 8-K states that total cash, cash equivalents and short-term investments of 2.7 billion at year end are 433.9 million lower than at the end of the third quarter. For the full year they rose by 1.9 billion. Operating cash flow for the year prints 751400000.",
  "account": "Cash, cash equivalents and short-term investments",
  "expected_direction": "down",
  "horizon": "fourth quarter of fiscal 2026 (third-quarter end to 2026-06-27)",
  "quote": "a decrease of $433.9 million from the end of the third quarter of fiscal year 2026",
  "paragraph_id": "0001628280-26-055726:8k_2_02:16" }
```

```json
{ "id": "liquidity_and_capital_capex_accrued_not_paid",
  "what_changed": "Capital expenditures incurred but not yet paid (tagged with the PropertyPlantAndEquipmentMember) are 181400000 for fiscal 2026, against 43400000 for fiscal 2025. Cash capital spending prints 451300000, against 231000000.0.",
  "account": "Capital expenditures incurred but not yet paid",
  "expected_direction": "up",
  "horizon": "fiscal year 2025-06-29..2026-06-27",
  "quote": "\"value\": \"181400000\"",
  "paragraph_id": "0001628280-26-057358:facts:CapitalExpendituresIncurredButNotYetPaid:2025-06-29..2026-06-27:us-gaap:FairValueByAssetClassAxis=us-gaap:PropertyPlantAndEquipmentMember" }
```

```json
{ "id": "liquidity_and_capital_share_withholding_tax_payments",
  "what_changed": "Payments for tax withholding on share-based compensation are 281000000.0 for fiscal 2026, against 41700000 for fiscal 2025.",
  "account": "Tax withholding payments on share-based compensation",
  "expected_direction": "up",
  "horizon": "fiscal year 2025-06-29..2026-06-27",
  "quote": "\"value\": \"281000000.0\"",
  "paragraph_id": "0001628280-26-057358:facts:PaymentsRelatedToTaxWithholdingForShareBasedCompensation:2025-06-29..2026-06-27" }
```

```json
{ "id": "liquidity_and_capital_purchase_commitments",
  "what_changed": "Remaining minimum purchase commitments are 2400000000 at 2026-06-27. The third-quarter 10-Q printed 1795600000 at 2026-03-28.",
  "account": "Purchase commitments",
  "expected_direction": "up",
  "horizon": "2026-06-27 against 2026-03-28",
  "quote": "\"value\": \"2400000000\"",
  "paragraph_id": "0001628280-26-057358:facts:PurchaseCommitmentRemainingMinimumAmountCommitted:2026-06-27" }
```

### Results against expectations

```json
{ "id": "results_against_expectations_fourth_quarter_revenue_in_release",
  "what_changed": "The 8-K prints fourth-quarter fiscal 2026 net revenue of 1,006.3, against 808.4 in the third quarter and 480.7 a year earlier, with company-stated changes of 24.5% and 109.3%. The trend table has no quarters-back-0 cell, and no fourth-quarter derivation is in the inputs, so these release figures stand unchecked against any computed quarter.",
  "account": "Net revenue, fourth quarter",
  "expected_direction": "up",
  "horizon": "three months ended 2026-06-27",
  "quote": "| Net revenue | $ | 1,006.3 |  |  | $ | 808.4 |  |  | $ | 480.7 |  |  | 24.5% |  | 109.3% |",
  "paragraph_id": "0001628280-26-055726:8k_2_02:22" }
```

```json
{ "id": "results_against_expectations_next_quarter_revenue_outlook",
  "what_changed": "The outlook for the first quarter of fiscal 2027 is:\n- net revenue of 1.225 to 1.275 billion;\n- non-GAAP operating margin of 39.5% to 40.5%;\n- non-GAAP diluted EPS of 4.05 to 4.35.\nNo GAAP reconciliation is given.",
  "account": "Net revenue outlook",
  "expected_direction": "up",
  "horizon": "next 10-Q (first quarter of fiscal 2027)",
  "quote": "•Net revenue in the range of $1.225 billion to $1.275 billion",
  "paragraph_id": "0001628280-26-055726:8k_2_02:31" }
```

---

## Seen in the notes

No items. The heading is for facts whose element sat inside a note when it was extracted, and each fact is supposed to carry a marker saying so. No fact in `input_numbers.json` carries any such marker. Every fact row has only these fields: id, paragraph_id, tag, prefix, namespace, context, context_ref, unit, decimals, value, number, nil, form, source_accession, filing_date, and sometimes superseded_by. Without the marker, no fact can be placed here.

Several facts quoted above come from tags that usually appear in note tables: the income tax, debt maturity, warranty roll-forward, concentration, segment and business-combination facts. They stay under "Seen in the statements" because the input does not mark them as note facts.
