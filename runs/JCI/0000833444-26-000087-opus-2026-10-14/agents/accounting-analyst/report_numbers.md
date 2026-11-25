<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
# JCI — numbers reader — 10-Q 0000833444-26-000087 (cutoff 2026-07-29)

## Before the items

**Period the record does not reach.** `quarters-back-0` (target end 2026-06-30, the quarter this 10-Q reports) has no cells in the trend table. The reason it gives: "no quarter ending within 20 days of 2026-06-30 is in the companyfacts record; the companyfacts record's newest row was filed 2026-05-06, before this run's cutoff 2026-07-29 — the record was fetched before the triggering report, so the periods that report is the first to state are not in it". No ratio exists for that quarter. I do not derive any. Where this filing's own raw facts or the 8-K print that quarter's balances, they are reported below as facts, not as ratios. `quarters-back-3` (target 2025-09-30) and `quarters-back-7` (target 2024-10-01) also have no cells. Their reason says a fiscal fourth quarter "is derived by src/fourth_quarter.py". That derivation is not in my directory.

**Inputs missing from my directory.** There are no articulation checks, no restatement traces and no fourth-quarter derivation, so no articulation-gap item can be written. Restated prior values are reported only where the facts themselves show them (see the `superseded_by` item). Prior predictions: "None on record." Nothing forbidden is in my directory: no prices, returns, short interest, other companies' files, prior probabilities or outcome window.

**How much of `input_numbers.json` I read (95,337 lines).** My context could not hold all of it. I read lines 1–300, 2770–2995, 49880–49920, 50000–50025, 70000–70025, 72700–72720, 74000–74020, 75600–75630, 75820–75852, 75850–76489 and 94000–95336. Statements below about note markers, `superseded_by` rows and tag changes cover only those rows.

- No fact row I read has a field marking whether it sat inside a note. So no XBRL fact can be placed under "Seen in the notes", and all fact items sit under statements.
- The 10-K rows I read carry a `superseded_by` field naming 0000833444-26-000087.

**Placement rule for the 8-K.** The 8-K has no note marker either. Its tables printed after the release's `FOOTNOTES` heading (`0000833444-26-000083:8k_2_02:83`) go under "Seen in the notes". Its body, its financial statements and its prose go under "Seen in the statements".

**The R&D-capitalisation baseline has no paragraph_id**, so it cannot be quoted. For years-back-0 it prints:

- book_value_with_rnd_capitalized 13713600000.0
- earnings_with_rnd_capitalized 3303400000.0
- research_and_development_asset 786600000.0
- research_and_development_amortization 260600000.0
- capitalized_development_cost is missing (`insufficient`): "no row for capitalized_development_cost: the companyfacts record tags none of us-gaap:CapitalizedComputerSoftwareAdditions in any period."

**Field meanings.**

- `expected_direction` is the direction of the change the input itself prints for the account: the sign of the printed change, or later figure against earlier figure. It is `none` where the cell is insufficient or no direction is printed. It is not a forecast.
- `horizon` names the comparison the change covers.
- All numbers are copied as printed. None is rounded or computed.

## Seen in the statements

```json
{ "id": "earnings_quality_accruals_over_total_assets_annual",
  "what_changed": "accruals_over_total_assets for 2024-10-01..2025-09-30 is 0.019425920556683098; year_over_year change 0.016217113904850332 against years-back-1. Its place in history is printed in the quote: the highest of the 4 filled years on the same concepts, with years-back-4 resting on a different concept and not compared. Inputs as printed: net_income NetIncomeLoss 3291000000.0 and operating_cash_flow NetCashProvidedByUsedInOperatingActivitiesContinuingOperations 2554000000.0 (both 0000833444-25-000097), assets 37939000000.0 (0000833444-26-000050). The net_income input is the total NetIncomeLoss concept while the cash-flow input is the continuing-operations concept; the 8-K states the R&LC HVAC business sold in July 2025 is reported as a discontinued operation.",
  "account": "accruals over total assets (NetIncomeLoss, NetCashProvidedByUsedInOperatingActivitiesContinuingOperations, Assets)",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2025-09-30 against fiscal year ended 2024-09-30",
  "quote": "\"position_in_history\": \"highest of the 4 filled years on the same concepts; 1 other filled year rests on a different concept and is not compared\"",
  "paragraph_id": "0000833444-26-000087:trends:accruals_over_total_assets:2024-10-01..2025-09-30" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual",
  "what_changed": "bad_debt_reserve_ratio for 2024-10-01..2025-09-30 is 0.03166512202656781; year_over_year change -0.0018758458699343478 against years-back-1; second highest of the 5 filled years. Inputs as printed: AllowanceForDoubtfulAccountsReceivableCurrent 205000000.0 and AccountsReceivableNetCurrent 6269000000.0 at 2025-09-30 (0000833444-26-000050).",
  "account": "allowance for doubtful accounts against gross receivables",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2025-09-30 against fiscal year ended 2024-09-30",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0000833444-26-000087:trends:bad_debt_reserve_ratio:2024-10-01..2025-09-30" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_annual",
  "what_changed": "contract_liabilities_over_revenue for 2024-10-01..2025-09-30 is 0.10467875911171386; year_over_year change 0.010569313311783568 against years-back-1; highest of the 5 filled years. Inputs as printed: ContractWithCustomerLiabilityCurrent 2470000000.0 at 2025-09-30 (0000833444-26-000050) and revenue 23596000000.0 (0000833444-25-000097).",
  "account": "current contract liabilities (deferred revenue) against revenue",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2025-09-30 against fiscal year ended 2024-09-30",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000833444-26-000087:trends:contract_liabilities_over_revenue:2024-10-01..2025-09-30" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_annual",
  "what_changed": "days_sales_of_inventory for 2024-10-01..2025-09-30 is 44.27486003732338; year_over_year change 0.6255154995082535 against years-back-1; second lowest of the 5 filled years. Inputs as printed: InventoryNet 1820000000.0 at 2025-09-30 (0000833444-26-000050) and CostOfGoodsAndServicesSold 15004000000.0 (0000833444-25-000097).",
  "account": "inventory against cost of revenue",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2025-09-30 against fiscal year ended 2024-09-30",
  "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
  "paragraph_id": "0000833444-26-000087:trends:days_sales_of_inventory:2024-10-01..2025-09-30" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_annual",
  "what_changed": "days_sales_outstanding for 2024-10-01..2025-09-30 is 96.9734276996101; year_over_year change 0.48222867555989524 against years-back-1; second highest of the 5 filled years. Inputs as printed: AccountsReceivableNetCurrent 6269000000.0 at 2025-09-30 (0000833444-26-000050) and revenue 23596000000.0 (0000833444-25-000097).",
  "account": "accounts receivable against revenue (days)",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2025-09-30 against fiscal year ended 2024-09-30",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0000833444-26-000087:trends:days_sales_outstanding:2024-10-01..2025-09-30" }
```

```json
{ "id": "earnings_quality_gross_margin_annual",
  "what_changed": "gross_margin for 2024-10-01..2025-09-30 is 0.3641295134768605; year_over_year change 0.012221183048139683 against years-back-1; highest of the 5 filled years. Inputs as printed: revenue 23596000000.0 and cost_of_revenue 15004000000.0 (both 0000833444-25-000097).",
  "account": "gross margin (RevenueFromContractWithCustomerExcludingAssessedTax, CostOfGoodsAndServicesSold)",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2025-09-30 against fiscal year ended 2024-09-30",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000833444-26-000087:trends:gross_margin:2024-10-01..2025-09-30" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_annual",
  "what_changed": "insufficient: inventory_reserve_ratio is not filled for 2024-10-01..2025-09-30, nor in any other period of the table (filled 0). The cell says the record tags no us-gaap:InventoryValuationReserves in any period; whether the company does not tag it or states it only by segment, the record cannot say.",
  "account": "inventory valuation reserve",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2025-09-30",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period.",
  "paragraph_id": "0000833444-26-000087:trends:inventory_reserve_ratio:2024-10-01..2025-09-30" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_annual",
  "what_changed": "insufficient: non_gaap_gap is not filled for 2024-10-01..2025-09-30, nor in any other period of the table (filled 0), because companyfacts holds no non-GAAP measure. The 8-K prints adjusted figures for the quarter and nine months (see the notes item on adjusted net income); no gap is computed here.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2025-09-30",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0000833444-26-000087:trends:non_gaap_gap:2024-10-01..2025-09-30" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_annual",
  "what_changed": "receivables_over_revenue for 2024-10-01..2025-09-30 is 0.2656806238345482; year_over_year change 0.002043468031132367 against years-back-1; second highest of the 5 filled years. Inputs as printed: AccountsReceivableNetCurrent 6269000000.0 (0000833444-26-000050) and revenue 23596000000.0 (0000833444-25-000097).",
  "account": "accounts receivable against revenue",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2025-09-30 against fiscal year ended 2024-09-30",
  "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
  "paragraph_id": "0000833444-26-000087:trends:receivables_over_revenue:2024-10-01..2025-09-30" }
```

```json
{ "id": "earnings_quality_soft_asset_share_annual",
  "what_changed": "soft_asset_share for 2024-10-01..2025-09-30 is 0.9322069638103271; year_over_year change 0.0026836004188292018 against years-back-1; highest of the 5 filled years. Inputs as printed at 2025-09-30 (0000833444-26-000050): Assets 37939000000.0, PropertyPlantAndEquipmentNet 2193000000.0, CashAndCashEquivalentsAtCarryingValue 379000000.0.",
  "account": "assets other than PP&E and cash, against total assets",
  "expected_direction": "up",
  "horizon": "fiscal year ended 2025-09-30 against fiscal year ended 2024-09-30",
  "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
  "paragraph_id": "0000833444-26-000087:trends:soft_asset_share:2024-10-01..2025-09-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_annual",
  "what_changed": "warranty_reserve_ratio for 2024-10-01..2025-09-30 is 0.0050856077301237495; year_over_year change -0.00022983319005749799 against years-back-1; third highest of the 5 filled years. Inputs as printed: StandardProductWarrantyAccrual 120000000.0 at 2025-09-30 and revenue 23596000000.0 (both 0000833444-25-000097).",
  "account": "standard product warranty accrual against revenue",
  "expected_direction": "down",
  "horizon": "fiscal year ended 2025-09-30 against fiscal year ended 2024-09-30",
  "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
  "paragraph_id": "0000833444-26-000087:trends:warranty_reserve_ratio:2024-10-01..2025-09-30" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly",
  "what_changed": "insufficient: accruals_over_total_assets is not filled for 2026-01-01..2026-03-31, the latest quarter the record reaches, because no operating-cash-flow row exists for that three-month period. Quarters-back-4 and quarters-back-5 are not filled for the same reason.",
  "account": "accruals over total assets",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-03-31",
  "quote": "\"missing\": \"no row for operating_cash_flow in 2026-01-01..2026-03-31: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
  "paragraph_id": "0000833444-26-000087:trends:accruals_over_total_assets:2026-01-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_accruals_over_total_assets_quarterly_two_period_history",
  "what_changed": "insufficient for a trend: the latest filled quarterly accruals cell is 2025-10-01..2025-12-31 with value -0.002290498380854593 and year_over_year change -0.00632869496976618 against quarters-back-6 (0.004038196588911587). It is the lowest of only 2 filled quarters, and two periods do not support a trend claim. Its quarter_over_quarter comparison does not exist because quarters-back-3 is not filled.",
  "account": "accruals over total assets",
  "expected_direction": "down",
  "horizon": "quarter ended 2025-12-31 against quarter ended 2024-12-31",
  "quote": "\"position_in_history\": \"lowest of the 2 filled quarters\"",
  "paragraph_id": "0000833444-26-000087:trends:accruals_over_total_assets:2025-10-01..2025-12-31" }
```

```json
{ "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly",
  "what_changed": "bad_debt_reserve_ratio for 2026-01-01..2026-03-31 (latest quarter the record reaches) is 0.025346301208370173; quarter_over_quarter change -0.0024532904360463487 against quarters-back-2; year_over_year change -0.01290685919222086 against quarters-back-5; lowest of the 5 filled quarters. Inputs as printed: allowance 172000000.0 and receivables 6614000000.0 at 2026-03-31 (0000833444-26-000050). This 10-Q's facts print the allowance at 2026-06-30 as 165000000 (separate item); no ratio exists for that quarter.",
  "account": "allowance for doubtful accounts against gross receivables",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-03-31 against quarters ended 2025-12-31 and 2025-03-31",
  "quote": "\"position_in_history\": \"lowest of the 5 filled quarters\"",
  "paragraph_id": "0000833444-26-000087:trends:bad_debt_reserve_ratio:2026-01-01..2026-03-31" }
```

```json
{ "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly",
  "what_changed": "contract_liabilities_over_revenue for 2026-01-01..2026-03-31 is 0.4632041680234451; quarter_over_quarter change 0.024701494226653686; year_over_year change 0.04389479522570022; highest of the 5 filled quarters. Inputs as printed: ContractWithCustomerLiabilityCurrent 2845000000.0 and revenue 6142000000.0 (0000833444-26-000050). The 8-K prints deferred revenue of 2,943 at June 30, 2026 (separate item); no ratio exists for that quarter.",
  "account": "current contract liabilities against quarterly revenue",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-03-31 against quarters ended 2025-12-31 and 2025-03-31",
  "quote": "\"position_in_history\": \"highest of the 5 filled quarters\"",
  "paragraph_id": "0000833444-26-000087:trends:contract_liabilities_over_revenue:2026-01-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_days_sales_of_inventory_quarterly",
  "what_changed": "days_sales_of_inventory for 2026-01-01..2026-03-31 is 44.83762886597938; quarter_over_quarter change -2.904514566736168; year_over_year change 1.0228243192646644; third highest of the 5 filled quarters. Inputs as printed: InventoryNet 1933000000.0, CostOfGoodsAndServicesSold 3880000000.0 (0000833444-26-000050).",
  "account": "inventory against cost of revenue",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-03-31 against quarter ended 2025-12-31 (year over year the change is up)",
  "quote": "\"position_in_history\": \"third highest of the 5 filled quarters\"",
  "paragraph_id": "0000833444-26-000087:trends:days_sales_of_inventory:2026-01-01..2026-03-31" }
```

```json
{ "id": "revenue_recognition_days_sales_outstanding_quarterly",
  "what_changed": "days_sales_outstanding for 2026-01-01..2026-03-31 is 96.9163139042657; quarter_over_quarter change -1.3207052435693925; year_over_year change 4.030478809128283 against quarters-back-5; second highest of the 5 filled quarters. Inputs as printed: receivables 6614000000.0, revenue 6142000000.0 (0000833444-26-000050).",
  "account": "accounts receivable against quarterly revenue (days)",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-03-31 against quarter ended 2025-03-31 (quarter over quarter the change is down)",
  "quote": "\"position_in_history\": \"second highest of the 5 filled quarters\"",
  "paragraph_id": "0000833444-26-000087:trends:days_sales_outstanding:2026-01-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_gross_margin_quarterly",
  "what_changed": "gross_margin for 2026-01-01..2026-03-31 is 0.3682839465971996; quarter_over_quarter change 0.010512685600132132; year_over_year change 0.003766680917143217; second highest of the 5 filled quarters. Inputs as printed: revenue 6142000000.0, cost_of_revenue 3880000000.0 (0000833444-26-000050).",
  "account": "gross margin",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-03-31 against quarters ended 2025-12-31 and 2025-03-31",
  "quote": "\"position_in_history\": \"second highest of the 5 filled quarters\"",
  "paragraph_id": "0000833444-26-000087:trends:gross_margin:2026-01-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly",
  "what_changed": "insufficient: inventory_reserve_ratio is not filled for 2026-01-01..2026-03-31 or for any quarter; the record tags no us-gaap:InventoryValuationReserves.",
  "account": "inventory valuation reserve",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-03-31",
  "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period.",
  "paragraph_id": "0000833444-26-000087:trends:inventory_reserve_ratio:2026-01-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_non_gaap_gap_quarterly",
  "what_changed": "insufficient: non_gaap_gap is not filled for 2026-01-01..2026-03-31 or for any quarter; companyfacts carries no non-GAAP measure.",
  "account": "non-GAAP net income against GAAP net income",
  "expected_direction": "none",
  "horizon": "quarter ended 2026-03-31",
  "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
  "paragraph_id": "0000833444-26-000087:trends:non_gaap_gap:2026-01-01..2026-03-31" }
```

```json
{ "id": "revenue_recognition_receivables_over_revenue_quarterly",
  "what_changed": "receivables_over_revenue for 2026-01-01..2026-03-31 is 1.076847932269619; quarter_over_quarter change 0.009054245880107059; year_over_year change 0.044783097879203204; highest of the 5 filled quarters. Inputs as printed: receivables 6614000000.0, revenue 6142000000.0 (0000833444-26-000050). This 10-Q prints receivables of 6970000000 at 2026-06-30 (separate item); no ratio exists for that quarter.",
  "account": "accounts receivable against quarterly revenue",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-03-31 against quarters ended 2025-12-31 and 2025-03-31",
  "quote": "\"position_in_history\": \"highest of the 5 filled quarters\"",
  "paragraph_id": "0000833444-26-000087:trends:receivables_over_revenue:2026-01-01..2026-03-31" }
```

```json
{ "id": "earnings_quality_soft_asset_share_quarterly",
  "what_changed": "soft_asset_share for 2026-01-01..2026-03-31 is 0.9271523178807947; quarter_over_quarter change -0.002237145826653353; year_over_year change 0.0030840572062130756; second highest of the 5 filled quarters. Inputs as printed: Assets 38354000000.0, PP&E 2096000000.0, cash 698000000.0 (0000833444-26-000050).",
  "account": "assets other than PP&E and cash, against total assets",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-03-31 against quarter ended 2025-12-31 (year over year the change is up)",
  "quote": "\"position_in_history\": \"second highest of the 5 filled quarters\"",
  "paragraph_id": "0000833444-26-000087:trends:soft_asset_share:2026-01-01..2026-03-31" }
```

```json
{ "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly",
  "what_changed": "warranty_reserve_ratio for 2026-01-01..2026-03-31 is 0.026538586779550635; quarter_over_quarter change 0.003423182259971541; year_over_year change 0.00557311813966339; highest of the 5 filled quarters. Inputs as printed: ProductWarrantyAccrual 163000000.0 at 2026-03-31, revenue 6142000000.0 (0000833444-26-000050). This 10-Q prints ProductWarrantyAccrual of 146000000 at 2026-06-30 (separate item).",
  "account": "product warranty accrual against quarterly revenue",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-03-31 against quarters ended 2025-12-31 and 2025-03-31",
  "quote": "\"position_in_history\": \"highest of the 5 filled quarters\"",
  "paragraph_id": "0000833444-26-000087:trends:warranty_reserve_ratio:2026-01-01..2026-03-31" }
```

```json
{ "id": "structure_and_disclosure_changes_operating_cash_flow_concept_change",
  "what_changed": "Change of tag printed by the trend table. The accruals_over_total_assets cell for 2020-10-01..2021-09-30 rests its operating_cash_flow input on us-gaap:NetCashProvidedByUsedInOperatingActivities (2551000000.0, 0000833444-21-000046). Years-back-0 through years-back-3 use NetCashProvidedByUsedInOperatingActivitiesContinuingOperations. The table therefore prints no year_over_year change between years-back-3 and years-back-4, and this cell's position reads: the only filled year on the same concepts, with 4 other filled years on a different concept and not compared.",
  "account": "cash provided by operating activities (total versus continuing operations)",
  "expected_direction": "none",
  "horizon": "fiscal year ended 2021-09-30 against fiscal year ended 2022-09-30",
  "quote": "\"tag\": \"NetCashProvidedByUsedInOperatingActivities\"",
  "paragraph_id": "0000833444-26-000087:trends:accruals_over_total_assets:2020-10-01..2021-09-30" }
```

```json
{ "id": "structure_and_disclosure_changes_warranty_accrual_concept_differs",
  "what_changed": "Observed, not flagged by the input. For 2025-09-30, the annual trend cell's warranty input is us-gaap:StandardProductWarrantyAccrual 120000000.0 from the 10-K (0000833444-25-000097). This 10-Q tags the same date as us-gaap:ProductWarrantyAccrual with value 120000000. The value is the same and the concept differs. The quarterly trend series uses ProductWarrantyAccrual and the annual series uses StandardProductWarrantyAccrual. I did not read the 10-K rows that would show whether it also tagged ProductWarrantyAccrual.",
  "account": "product warranty accrual",
  "expected_direction": "none",
  "horizon": "balance at 2025-09-30 as tagged by the 10-K and by this 10-Q",
  "quote": "\"value\": \"120000000\"",
  "paragraph_id": "0000833444-26-000087:facts:ProductWarrantyAccrual:2025-09-30" }
```

```json
{ "id": "articulation_and_the_filed_history_superseded_balances_unchanged",
  "what_changed": "No restated prior value found in the rows read. The 10-K fact for AccountsReceivableNetCurrent at 2025-09-30 (value 6269000000) carries superseded_by 0000833444-26-000087, and this 10-Q prints 6269000000 for the same tag and date. The same holds in the rows I read for InventoryNet (1820000000 in both), AssetsOfDisposalGroupIncludingDiscontinuedOperationCurrent (14000000), OtherAssetsCurrent (1680000000), AssetsCurrent (10162000000) and PropertyPlantAndEquipmentNet (2193000000). The superseded_by rows outside the lines I read were not checked, and no restatement-trace file exists in my directory.",
  "account": "balance sheet at 2025-09-30 (receivables, inventory, current assets, PP&E)",
  "expected_direction": "none",
  "horizon": "2025-09-30 balances as filed in the 10-K and as filed in this 10-Q",
  "quote": "\"superseded_by\": \"0000833444-26-000087\"",
  "paragraph_id": "0000833444-25-000097:facts:AccountsReceivableNetCurrent:2025-09-30" }
```

```json
{ "id": "revenue_recognition_receivables_balance_latest_quarter_end",
  "what_changed": "This 10-Q prints AccountsReceivableNetCurrent of 6970000000 at 2026-06-30, against 6269000000 at 2025-09-30 in the same filing and 6614000000.0 at 2026-03-31 in the trend inputs. The 8-K balance sheet prints the same 6,970. Receivables ratios for this quarter do not exist in the trend table (quarters-back-0 is not reached).",
  "account": "accounts receivable, net",
  "expected_direction": "up",
  "horizon": "2026-06-30 against 2026-03-31 and 2025-09-30",
  "quote": "\"value\": \"6970000000\"",
  "paragraph_id": "0000833444-26-000087:facts:AccountsReceivableNetCurrent:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_allowance_for_doubtful_accounts_latest_quarter_end",
  "what_changed": "This 10-Q prints AllowanceForDoubtfulAccountsReceivableCurrent of 165000000 at 2026-06-30, against 205000000 at 2025-09-30 in the same filing and 172000000.0 at 2026-03-31 in the trend inputs, while receivables rose (separate item). The bad_debt_reserve_ratio for this quarter does not exist.",
  "account": "allowance for doubtful accounts",
  "expected_direction": "down",
  "horizon": "2026-06-30 against 2026-03-31 and 2025-09-30",
  "quote": "\"value\": \"165000000\"",
  "paragraph_id": "0000833444-26-000087:facts:AllowanceForDoubtfulAccountsReceivableCurrent:2026-06-30" }
```

```json
{ "id": "earnings_quality_inventory_balance_latest_quarter_end",
  "what_changed": "This 10-Q prints InventoryNet of 1955000000 at 2026-06-30, against 1820000000 at 2025-09-30 and 1933000000.0 at 2026-03-31 (trend input). The 8-K prints Inventories 1,955. days_sales_of_inventory for this quarter does not exist.",
  "account": "inventories, net",
  "expected_direction": "up",
  "horizon": "2026-06-30 against 2026-03-31 and 2025-09-30",
  "quote": "\"value\": \"1955000000\"",
  "paragraph_id": "0000833444-26-000087:facts:InventoryNet:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_warranty_accrual_latest_quarter_end",
  "what_changed": "This 10-Q prints ProductWarrantyAccrual of 146000000 at 2026-06-30, against 163000000.0 at 2026-03-31 (trend input) and 120000000 at 2025-09-30. For 2025-10-01..2026-06-30 the same filing prints WarrantiesIssued 94000000, Payments 70000000, PreexistingIncreaseDecrease 3000000 and a foreign-currency effect of 1000000. warranty_reserve_ratio for this quarter does not exist.",
  "account": "product warranty accrual",
  "expected_direction": "down",
  "horizon": "2026-06-30 against 2026-03-31 (against 2025-09-30 the balance is higher)",
  "quote": "\"value\": \"146000000\"",
  "paragraph_id": "0000833444-26-000087:facts:ProductWarrantyAccrual:2026-06-30" }
```

```json
{ "id": "earnings_quality_property_plant_and_equipment_latest_quarter_end",
  "what_changed": "This 10-Q prints PropertyPlantAndEquipmentNet of 1977000000 at 2026-06-30, against 2193000000 at 2025-09-30 and 2096000000.0 at 2026-03-31 (trend input). It also prints Assets of 38759000000 at 2026-06-30 against 37939000000 at 2025-09-30. soft_asset_share for this quarter does not exist.",
  "account": "property, plant and equipment, net",
  "expected_direction": "down",
  "horizon": "2026-06-30 against 2026-03-31 and 2025-09-30",
  "quote": "\"value\": \"1977000000\"",
  "paragraph_id": "0000833444-26-000087:facts:PropertyPlantAndEquipmentNet:2026-06-30" }
```

```json
{ "id": "structure_and_disclosure_changes_noncurrent_assets_held_for_sale",
  "what_changed": "This 10-Q prints DisposalGroupIncludingDiscontinuedOperationAssetsNoncurrent of 225000000 at 2026-06-30 against 140000000 at 2025-09-30. The 8-K prints noncurrent liabilities held for sale of 34 against 9.",
  "account": "noncurrent assets held for sale",
  "expected_direction": "up",
  "horizon": "2026-06-30 against 2025-09-30",
  "quote": "\"value\": \"225000000\"",
  "paragraph_id": "0000833444-26-000087:facts:DisposalGroupIncludingDiscontinuedOperationAssetsNoncurrent:2026-06-30" }
```

```json
{ "id": "estimates_and_discretion_accrued_compensation_balance",
  "what_changed": "This 10-Q prints EmployeeRelatedLiabilitiesCurrent of 1098000000 at 2026-06-30; the 8-K balance sheet prints accrued compensation and benefits of 1,098 against 1,268 at September 30, 2025. The 8-K separately attributes the rise in corporate expense to increased incentive-compensation accruals (separate item).",
  "account": "accrued compensation and benefits",
  "expected_direction": "down",
  "horizon": "2026-06-30 against 2025-09-30",
  "quote": "\"value\": \"1098000000\"",
  "paragraph_id": "0000833444-26-000087:facts:EmployeeRelatedLiabilitiesCurrent:2026-06-30" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_environmental_accrual",
  "what_changed": "This 10-Q prints AccrualForEnvironmentalLossContingencies of 169000000 at 2026-06-30 against 187000000 at 2025-09-30 (current 21000000 against 27000000; noncurrent 148000000 against 160000000).",
  "account": "environmental loss contingency accrual",
  "expected_direction": "down",
  "horizon": "2026-06-30 against 2025-09-30",
  "quote": "\"value\": \"169000000\"",
  "paragraph_id": "0000833444-26-000087:facts:AccrualForEnvironmentalLossContingencies:2026-06-30" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_asbestos_liability",
  "what_changed": "This 10-Q prints LiabilityForAsbestosAndEnvironmentalClaimsGross of 381000000 at 2026-06-30 against 387000000 at 2025-09-30. EstimatedInsuranceRecoveries is 40000000 against 44000000, and asbestos-restricted cash and investments are 310000000 against 295000000.",
  "account": "asbestos liability, gross",
  "expected_direction": "down",
  "horizon": "2026-06-30 against 2025-09-30",
  "quote": "\"value\": \"381000000\"",
  "paragraph_id": "0000833444-26-000087:facts:LiabilityForAsbestosAndEnvironmentalClaimsGross:2026-06-30" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_afff_individual_claims_count",
  "what_changed": "This 10-Q prints LossContingencyPendingClaimsNumber of 16515 at 2026-06-30 for AFFF individual or mass actions. The same filing prints 403 municipal and water-provider cases, 50 putative class actions and 35 state or territory attorney-general cases at 2026-06-30. No earlier count for these members appears in the rows I read: insufficient for a change.",
  "account": "AFFF pending claims (count)",
  "expected_direction": "none",
  "horizon": "count at 2026-06-30",
  "quote": "\"value\": \"16515\"",
  "paragraph_id": "0000833444-26-000087:facts:LossContingencyPendingClaimsNumber:2026-06-30:srt:LitigationCaseAxis=jci:AqueousFilmFormingFoamIndividualOrMassActionsMember" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_afff_insurance_recoveries",
  "what_changed": "This 10-Q prints InsuranceRecoveries of 148000000 for 2025-10-01..2026-06-30 against 13000000 for 2024-10-01..2025-06-30, and 17000000 for the quarter against 1000000. Two rows print this paragraph_id (f-1094 and f-1153), both 148000000. The 8-K excludes these recoveries from adjusted results (notes item).",
  "account": "AFFF-related insurance recoveries",
  "expected_direction": "up",
  "horizon": "nine months ended 2026-06-30 against nine months ended 2025-06-30",
  "quote": "\"value\": \"148000000\"",
  "paragraph_id": "0000833444-26-000087:facts:InsuranceRecoveries:2025-10-01..2026-06-30" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_wisconsin_settlement_payment",
  "what_changed": "This 10-Q prints PaymentsForLegalSettlements of 10000000 dated 2026-06-04 for the State of Wisconsin v. Tyco Fire Products LP and Johnson Controls Inc. member. No earlier figure for this member appears in the rows I read.",
  "account": "legal settlement payment",
  "expected_direction": "none",
  "horizon": "payment on 2026-06-04",
  "quote": "\"value\": \"10000000\"",
  "paragraph_id": "0000833444-26-000087:facts:PaymentsForLegalSettlements:2026-06-04..2026-06-04:srt:LitigationCaseAxis=jci:StateOfWisconsinV.TycoFireProductsLPAndJohnsonControlsInc.Member" }
```

```json
{ "id": "across_documents_restructuring_charges_agree_with_release",
  "what_changed": "This 10-Q prints RestructuringCharges of 224000000 for 2025-10-01..2026-06-30 against 146000000 for 2024-10-01..2025-06-30 (51000000 for the prior-year quarter). The 8-K income statement prints restructuring and impairment costs of 224 against 146 for the nine months and 80 against 51 for the quarter. The two documents agree on the figures read.",
  "account": "restructuring and impairment costs",
  "expected_direction": "up",
  "horizon": "nine months ended 2026-06-30 against nine months ended 2025-06-30",
  "quote": "\"value\": \"224000000\"",
  "paragraph_id": "0000833444-26-000087:facts:RestructuringCharges:2025-10-01..2026-06-30" }
```

```json
{ "id": "across_documents_pretax_income_agrees_with_release",
  "what_changed": "This 10-Q prints income from continuing operations before income taxes of 917000000 for 2026-04-01..2026-06-30 against 705000000 for 2025-04-01..2025-06-30, and 2363000000 against 1614000000 for the nine months. The 8-K prints 917, 705, 2,363 and 1,614, so the figures agree.",
  "account": "income from continuing operations before income taxes",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "\"value\": \"917000000\"",
  "paragraph_id": "0000833444-26-000087:facts:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest:2026-04-01..2026-06-30" }
```

```json
{ "id": "structure_and_disclosure_changes_backlog_restated_for_equipment_only_orders",
  "what_changed": "Restated prior value stated by the release. Orders before the first fiscal 2026 quarter exclude certain equipment-only sales for longer-cycle projects, and backlog has been restated to include this new category. The headline backlog of $21.0 billion, up 32% organically, is on the restated basis. No pre-restatement backlog figure exists in my input.",
  "account": "orders and backlog (Solutions and Services)",
  "expected_direction": "up",
  "horizon": "prior-period backlog as restated in the fiscal third quarter 2026 release",
  "quote": "Backlog has been restated to include this new category.",
  "paragraph_id": "0000833444-26-000083:8k_2_02:18" }
```

```json
{ "id": "results_against_expectations_full_year_adjusted_eps_guidance_raised",
  "what_changed": "The release raises fiscal 2026 adjusted EPS guidance to ~$5.05 from ~$4.85. It is a non-GAAP figure, and the release says no quantitative reconciliation to GAAP is presented.",
  "account": "adjusted EPS guidance (non-GAAP)",
  "expected_direction": "up",
  "horizon": "fiscal year 2026",
  "quote": "Adjusted EPS of ~$5.05 (previously ~$4.85)",
  "paragraph_id": "0000833444-26-000083:8k_2_02:53" }
```

```json
{ "id": "results_against_expectations_full_year_organic_sales_guidance_raised",
  "what_changed": "The release raises fiscal 2026 organic sales growth guidance to ~8% from ~6%. The nine-month organic growth printed in the release's sales table is 7%.",
  "account": "organic sales growth guidance (non-GAAP)",
  "expected_direction": "up",
  "horizon": "fiscal year 2026",
  "quote": "Organic sales growth of ~8% (previously up ~6%)",
  "paragraph_id": "0000833444-26-000083:8k_2_02:51" }
```

```json
{ "id": "results_against_expectations_operating_leverage_guidance_widened",
  "what_changed": "Fiscal 2026 operating leverage guidance changes from ~50% to a range of 45% to 50%. The new range reaches below the previous point.",
  "account": "operating leverage guidance (non-GAAP)",
  "expected_direction": "down",
  "horizon": "fiscal year 2026",
  "quote": "Operating leverage of 45% to 50% (previously ~50%)",
  "paragraph_id": "0000833444-26-000083:8k_2_02:52" }
```

```json
{ "id": "results_against_expectations_free_cash_flow_conversion_guidance_unchanged",
  "what_changed": "Fiscal 2026 adjusted free cash flow conversion guidance is unchanged at ~100%. The release's footnote table prints nine-month adjusted free cash flow conversion of 98% (notes item).",
  "account": "adjusted free cash flow conversion guidance (non-GAAP)",
  "expected_direction": "none",
  "horizon": "fiscal year 2026",
  "quote": "Adjusted free cash flow conversion of ~100% (unchanged)",
  "paragraph_id": "0000833444-26-000083:8k_2_02:54" }
```

```json
{ "id": "revenue_recognition_receivables_increase_in_cash_flow",
  "what_changed": "The release's cash flow statement prints a cash use from the change in accounts receivable of (368) for the quarter against (172), and (757) for the nine months against (79). The balance sheet prints receivables of 6,970 against 6,269 at September 30, 2025.",
  "account": "accounts receivable (cash flow change)",
  "expected_direction": "up",
  "horizon": "quarter and nine months ended 2026-06-30 against the same periods of 2025",
  "quote": "| Accounts receivable | (368) |  |  | (172) |  |  | (757) |  |  | (79) |",
  "paragraph_id": "0000833444-26-000083:8k_2_02:81" }
```

```json
{ "id": "revenue_recognition_deferred_revenue_balance",
  "what_changed": "The release's balance sheet prints deferred revenue of 2,943 at June 30, 2026 against 2,470 at September 30, 2025. The 2,470 equals the ContractWithCustomerLiabilityCurrent input of 2470000000.0 in the annual trend cell; the quarterly contract-liabilities ratio for June 2026 does not exist.",
  "account": "deferred revenue (current contract liabilities)",
  "expected_direction": "up",
  "horizon": "2026-06-30 against 2025-09-30",
  "quote": "| Deferred revenue | 2,943 |  |  | 2,470 |",
  "paragraph_id": "0000833444-26-000083:8k_2_02:77" }
```

```json
{ "id": "earnings_quality_payables_and_accrued_liabilities_cash_inflow",
  "what_changed": "The cash flow statement prints a source of cash from accounts payable and accrued liabilities of 701 for the quarter against 258, and 764 for the nine months against 31. Operating cash flow from continuing operations is 1,289 against 787 for the quarter.",
  "account": "accounts payable and accrued liabilities (cash flow change)",
  "expected_direction": "up",
  "horizon": "quarter and nine months ended 2026-06-30 against the same periods of 2025",
  "quote": "| Accounts payable and accrued liabilities | 701 |  |  | 258 |  |  | 764 |  |  | 31 |",
  "paragraph_id": "0000833444-26-000083:8k_2_02:81" }
```

```json
{ "id": "earnings_quality_accrued_income_taxes_cash_inflow",
  "what_changed": "The cash flow statement prints a source of cash from accrued income taxes of 125 for the quarter against 23, and 205 for the nine months against (12).",
  "account": "accrued income taxes (cash flow change)",
  "expected_direction": "up",
  "horizon": "quarter and nine months ended 2026-06-30 against the same periods of 2025",
  "quote": "| Accrued income taxes | 125 |  |  | 23 |  |  | 205 |  |  | (12) |",
  "paragraph_id": "0000833444-26-000083:8k_2_02:81" }
```

```json
{ "id": "liquidity_and_capital_operating_cash_flow_quarter",
  "what_changed": "Cash provided by operating activities is $1,289 million for the quarter against 787. Free cash flow is $1,194 million and adjusted free cash flow $1,179 million. Nine-month operating cash flow is 2,572 against 1,586.",
  "account": "cash provided by operating activities from continuing operations",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "Cash provided by operating activities was $1,289 million.",
  "paragraph_id": "0000833444-26-000083:8k_2_02:42" }
```

```json
{ "id": "estimates_and_discretion_restructuring_and_impairment_costs",
  "what_changed": "The release's income statement prints restructuring and impairment costs of 80 for the quarter against 51, and 224 for the nine months against 146. The cash flow statement prints noncash restructuring and impairment charges of 56 against 23, and 160 against 56.",
  "account": "restructuring and impairment costs",
  "expected_direction": "up",
  "horizon": "quarter and nine months ended 2026-06-30 against the same periods of 2025",
  "quote": "| Restructuring and impairment costs | 80 |  |  | 51 |  |  | 224 |  |  | 146 |",
  "paragraph_id": "0000833444-26-000083:8k_2_02:72" }
```

```json
{ "id": "earnings_quality_effective_tax_rate_higher",
  "what_changed": "The release's adjusted effective tax rate for continuing operations is approximately 17% for the three and nine months of 2026, against approximately 12% for 2025. The income statement prints an income tax provision of 165 against 87 for the quarter and 443 against 160 for the nine months.",
  "account": "income tax provision and adjusted effective tax rate",
  "expected_direction": "up",
  "horizon": "three and nine months ended 2026-06-30 against the same periods of 2025",
  "quote": "effective tax rate for continuing operations was approximately 17% for the three and nine months ending June 30, 2026 and approximately 12% for the three and nine months ending June 30, 2025.",
  "paragraph_id": "0000833444-26-000083:8k_2_02:164" }
```

```json
{ "id": "earnings_quality_depreciation_and_amortization_lower",
  "what_changed": "The cash flow statement prints depreciation and amortization of 162 for the quarter against 190, and 495 for the nine months against 585.",
  "account": "depreciation and amortization",
  "expected_direction": "down",
  "horizon": "quarter and nine months ended 2026-06-30 against the same periods of 2025",
  "quote": "| Depreciation and amortization | 162 |  |  | 190 |  |  | 495 |  |  | 585 |",
  "paragraph_id": "0000833444-26-000083:8k_2_02:81" }
```

```json
{ "id": "earnings_quality_equity_based_compensation_lower",
  "what_changed": "The cash flow statement prints equity-based compensation of 29 for the quarter against 48, and 95 for the nine months against 107.",
  "account": "equity-based compensation",
  "expected_direction": "down",
  "horizon": "quarter and nine months ended 2026-06-30 against the same periods of 2025",
  "quote": "| Equity-based compensation | 29 |  |  | 48 |  |  | 95 |  |  | 107 |",
  "paragraph_id": "0000833444-26-000083:8k_2_02:81" }
```

```json
{ "id": "earnings_quality_gross_profit_latest_quarter",
  "what_changed": "The release prints gross profit of 2,474 for the quarter against 2,246, and 6,810 for the nine months against 6,241, on net sales of 6,614 against 6,052. The trend table's gross_margin for this quarter does not exist, and I do not compute it.",
  "account": "gross profit",
  "expected_direction": "up",
  "horizon": "quarter and nine months ended 2026-06-30 against the same periods of 2025",
  "quote": "| Gross profit | 2,474 |  |  | 2,246 |  |  | 6,810 |  |  | 6,241 |",
  "paragraph_id": "0000833444-26-000083:8k_2_02:72" }
```

```json
{ "id": "earnings_quality_services_cost_of_sales_lower",
  "what_changed": "The income statement prints services cost of sales of 1,128 for the quarter against 1,150, while services net sales are 2,018 against 1,930. Nine-month services cost of sales is 3,295 against 3,278.",
  "account": "cost of sales, services",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "| Services | 1,128 |  |  | 1,150 |  |  | 3,295 |  |  | 3,278 |",
  "paragraph_id": "0000833444-26-000083:8k_2_02:72" }
```

```json
{ "id": "earnings_quality_selling_general_administrative_lower",
  "what_changed": "The income statement prints selling, general and administrative expenses of 1,407 for the quarter against 1,417, and 4,029 for the nine months against 4,243.",
  "account": "selling, general and administrative expenses",
  "expected_direction": "down",
  "horizon": "quarter and nine months ended 2026-06-30 against the same periods of 2025",
  "quote": "| Selling, general and administrative expenses | 1,407 |  |  | 1,417 |  |  | 4,029 |  |  | 4,243 |",
  "paragraph_id": "0000833444-26-000083:8k_2_02:72" }
```

```json
{ "id": "estimates_and_discretion_corporate_incentive_compensation_accruals",
  "what_changed": "The release attributes the year-over-year rise in corporate expense (GAAP 167 against 141; adjusted 100 against 93) to increased corporate accruals for incentive compensation and to the timing of certain corporate expenses.",
  "account": "corporate expense and incentive compensation accruals",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "The increase year-over-year is primarily due to increased corporate accruals related to incentive compensation and the timing of certain corporate expenses.",
  "paragraph_id": "0000833444-26-000083:8k_2_02:40" }
```

```json
{ "id": "liquidity_and_capital_stock_repurchases",
  "what_changed": "The cash flow statement prints stock repurchases and retirements of (635) for the quarter against (310), and (850) for the nine months against (970). Dividends paid are (245) against (243).",
  "account": "stock repurchases",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30 (the nine months are lower)",
  "quote": "| Stock repurchases and retirements | (635) |  |  | (310) |  |  | (850) |  |  | (970) |",
  "paragraph_id": "0000833444-26-000083:8k_2_02:81" }
```

```json
{ "id": "structure_and_disclosure_changes_acquisition_in_quarter",
  "what_changed": "The cash flow statement prints acquisitions of businesses, net of cash acquired, of (291) for the quarter and the nine months, against (1) and (9).",
  "account": "acquisitions of businesses",
  "expected_direction": "up",
  "horizon": "quarter and nine months ended 2026-06-30 against the same periods of 2025",
  "quote": "| Acquisitions of businesses, net of cash acquired | (291) |  |  | (1) |  |  | (291) |  |  | (9) |",
  "paragraph_id": "0000833444-26-000083:8k_2_02:81" }
```

```json
{ "id": "structure_and_disclosure_changes_divestiture_gains",
  "what_changed": "The cash flow statement prints a gain on business divestiture of (13) for the quarter and (86) for the nine months, against none and a loss of 6. Divestiture proceeds are 122 and 331 against 1 and 2. The release names the sale of the ADT Mexico Security and ADTi businesses and excludes a 70 nine-month gain from adjusted results.",
  "account": "gain on business divestitures",
  "expected_direction": "up",
  "horizon": "quarter and nine months ended 2026-06-30 against the same periods of 2025",
  "quote": "| (Gain) loss on business divestiture | (13) |  |  | — |  |  | (86) |  |  | 6 |",
  "paragraph_id": "0000833444-26-000083:8k_2_02:81" }
```

```json
{ "id": "structure_and_disclosure_changes_discontinued_operations_investing_outflow",
  "what_changed": "Under discontinued operations, the cash flow statement prints cash used by investing activities of (155) for the quarter and the nine months, against (25) and (52). Income from discontinued operations is nil for the quarter against 160, and (27) for the nine months against 301. The release says the R&LC HVAC business sold in July 2025 is reported as a discontinued operation.",
  "account": "discontinued operations cash flows",
  "expected_direction": "up",
  "horizon": "quarter and nine months ended 2026-06-30 against the same periods of 2025",
  "quote": "| Cash used by investing activities | (155) |  |  | (25) |  |  | (155) |  |  | (52) |",
  "paragraph_id": "0000833444-26-000083:8k_2_02:81" }
```

```json
{ "id": "narrative_signs_of_operating_pressure_emea_middle_east",
  "what_changed": "EMEA sales are $1,264 against $1,273, down 1%, with organic growth of 1%. The release says the region was constrained by continued pressure from the conflicts in the Middle East. EMEA sales include divestitures and other of (41) in the base-year adjustment.",
  "account": "EMEA segment sales",
  "expected_direction": "down",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "constrained by continued pressure in the region due to the conflicts in the Middle East",
  "paragraph_id": "0000833444-26-000083:8k_2_02:29" }
```

## Seen in the notes

No XBRL fact in the rows I read carries a note marker, so none appears here. The items below are tables printed after the 8-K release's `FOOTNOTES` heading (`0000833444-26-000083:8k_2_02:83`), placed by the rule stated above.

```json
{ "id": "earnings_quality_adjusted_net_income_over_gaap",
  "what_changed": "For the quarter, the release's reconciliation prints adjusted (non-GAAP) income from continuing operations attributable to JCI of 868 against GAAP 749, and 693 against 618 a year earlier. Adjusted diluted EPS is 1.42 against GAAP 1.23. Nine months: adjusted 2,145 against GAAP 1,913. The trend table's non_gaap_gap is insufficient in every period. I do not compute the gap.",
  "account": "adjusted net income (non-GAAP) against GAAP net income",
  "expected_direction": "up",
  "horizon": "quarter and nine months ended 2026-06-30 against the same periods of 2025",
  "quote": "| Adjusted (non-GAAP)* | $ | 868 |  |  | $ | 693 |  |  | $ | 1.42 |  |  | $ | 1.05 |",
  "paragraph_id": "0000833444-26-000083:8k_2_02:150" }
```

```json
{ "id": "earnings_quality_transformation_costs_excluded",
  "what_changed": "Transformation costs excluded from adjusted EBIT are (80) for the quarter against (45), and (197) for the nine months against (124). The last-twelve-months table prints 253 against 124.",
  "account": "transformation costs (non-GAAP adjusting item)",
  "expected_direction": "up",
  "horizon": "quarter and nine months ended 2026-06-30 against the same periods of 2025",
  "quote": "| Transformation costs | (80) |  |  | (45) |  |  | (197) |  |  | (124) |",
  "paragraph_id": "0000833444-26-000083:8k_2_02:137" }
```

```json
{ "id": "earnings_quality_afff_insurance_recoveries_excluded_from_adjusted",
  "what_changed": "Water systems AFFF insurance recoveries removed from adjusted EBIT are 17 for the quarter against 1, and 148 for the nine months against 13. The nine-month 148 equals this 10-Q's InsuranceRecoveries fact of 148000000.",
  "account": "AFFF insurance recoveries (non-GAAP adjusting item)",
  "expected_direction": "up",
  "horizon": "quarter and nine months ended 2026-06-30 against the same periods of 2025",
  "quote": "| Water systems AFFF insurance recoveries | 17 |  |  | 1 |  |  | 148 |  |  | 13 |",
  "paragraph_id": "0000833444-26-000083:8k_2_02:137" }
```

```json
{ "id": "liquidity_and_capital_adjusted_free_cash_flow_conversion",
  "what_changed": "Adjusted free cash flow conversion (non-GAAP) is 132% for the quarter against 106%, and 98% for the nine months against 108%. Full-year guidance is ~100% (unchanged).",
  "account": "adjusted free cash flow conversion (non-GAAP)",
  "expected_direction": "down",
  "horizon": "nine months ended 2026-06-30 against nine months ended 2025-06-30 (the quarter is up)",
  "quote": "| Adjusted free cash flow conversion (non-GAAP) | 132 | % |  | 106 | % |  | 98 | % |  | 108 | % |",
  "paragraph_id": "0000833444-26-000083:8k_2_02:133" }
```

```json
{ "id": "related_parties_contingencies_and_subsequent_events_afff_settlement_cash_flows",
  "what_changed": "The adjusted free cash flow reconciliation prints water systems AFFF settlement cash payments and insurance recoveries of (7) for the quarter against (3), and (165) for the nine months against 383.",
  "account": "AFFF settlement cash payments and insurance recoveries",
  "expected_direction": "down",
  "horizon": "nine months ended 2026-06-30 against nine months ended 2025-06-30",
  "quote": "| Water systems AFFF settlement cash payments and insurance recoveries | (7) |  | (3) |  | (165) |  | 383 |",
  "paragraph_id": "0000833444-26-000083:8k_2_02:133" }
```

```json
{ "id": "earnings_quality_jc_capital_net_loss",
  "what_changed": "The reconciliation prints JC Capital net (income) loss of 26 for the quarter against (8), and 22 for the nine months against (4): a loss in 2026 against income in 2025. JC Capital cash used by operating activities is (8) against 34 provided.",
  "account": "JC Capital net income (loss)",
  "expected_direction": "down",
  "horizon": "quarter and nine months ended 2026-06-30 against the same periods of 2025",
  "quote": "| JC Capital net (income) loss | 26 |  | (8) |  | 22 |  | (4) |",
  "paragraph_id": "0000833444-26-000083:8k_2_02:133" }
```

```json
{ "id": "liquidity_and_capital_net_debt_to_adjusted_ebitda",
  "what_changed": "Net debt to adjusted EBITDA (non-GAAP) is 1.9x at June 30, 2026, against 2.0x at March 31, 2026 and 2.5x at June 30, 2025. Total debt is 9,475 against 9,523 and 10,293. Net debt to income before income taxes is 3.3x against 3.5x and 4.2x.",
  "account": "net debt to adjusted EBITDA",
  "expected_direction": "down",
  "horizon": "2026-06-30 against 2026-03-31 and 2025-06-30",
  "quote": "| Net debt to adjusted EBITDA (non-GAAP) | 1.9x |  | 2.0x |  | 2.5x |",
  "paragraph_id": "0000833444-26-000083:8k_2_02:160" }
```

```json
{ "id": "estimates_and_discretion_erp_accelerated_depreciation",
  "what_changed": "The last-twelve-months adjusted EBIT reconciliation excludes ERP asset accelerated depreciation of 102 for the twelve months to June 30, 2026 and to March 31, 2026, and nil to June 30, 2025. The release attributes it to a change in ERP strategy in EMEA, under which assets were abandoned and useful lives reduced. The same table prints last-twelve-months restructuring and impairment costs of 624 against 595 and 279.",
  "account": "ERP asset accelerated depreciation (useful-life change)",
  "expected_direction": "up",
  "horizon": "twelve months ended 2026-06-30 against twelve months ended 2025-06-30",
  "quote": "| ERP asset - accelerated depreciation | 102 |  |  | 102 |",
  "paragraph_id": "0000833444-26-000083:8k_2_02:162" }
```

```json
{ "id": "estimates_and_discretion_discrete_tax_items",
  "what_changed": "The nine-month net income reconciliation prints discrete tax items of 11 for 2026 against (36) for 2025 (EPS 0.02 against (0.05)). The release says these items include changes in estimates for valuation allowances and uncertain tax positions.",
  "account": "discrete tax items",
  "expected_direction": "up",
  "horizon": "nine months ended 2026-06-30 against nine months ended 2025-06-30",
  "quote": "| Discrete tax items | 11 |  |  | (36) |  |  | 0.02 |  |  | (0.05) |",
  "paragraph_id": "0000833444-26-000083:8k_2_02:153" }
```

```json
{ "id": "liquidity_and_capital_diluted_share_count_lower",
  "what_changed": "Diluted weighted average shares outstanding are 610 for the quarter against 657, and 612 for the nine months against 661. Basic shares are 608 against 655.",
  "account": "diluted weighted average shares",
  "expected_direction": "down",
  "horizon": "quarter and nine months ended 2026-06-30 against the same periods of 2025",
  "quote": "| Diluted weighted average shares outstanding | 610 |  |  | 657 |  |  | 612 |  |  | 661 |",
  "paragraph_id": "0000833444-26-000083:8k_2_02:156" }
```

```json
{ "id": "estimates_and_discretion_segment_transformation_costs_americas",
  "what_changed": "The segment reconciliation prints transformation costs excluded from adjusted segment EBITA of 25 in Americas for the quarter against 4, 2 in EMEA against 2, and 4 in APAC against nil. Nine-month Americas is 57 against 6.",
  "account": "segment transformation costs (non-GAAP adjusting item)",
  "expected_direction": "up",
  "horizon": "quarter ended 2026-06-30 against quarter ended 2025-06-30",
  "quote": "| Transformation costs | 25 |  |  | 4 |  |  | 2 |  |  | 2 |  |  | 4 |",
  "paragraph_id": "0000833444-26-000083:8k_2_02:141" }
```
