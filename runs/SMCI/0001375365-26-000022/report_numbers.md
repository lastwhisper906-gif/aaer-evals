<!-- the quote gate removed 0 item(s) from this copy; input_manifest.json lists each with its reason -->
**Numbers reader — SMCI (Super Micro Computer, Inc.), 10-K 0001375365-26-000022, fiscal year ended 2026-06-30**

**What I read.** I read `input_8k.md`, `input_prior_predictions.md` and `input_trends.json` in full. `input_numbers.json` has 114,970 lines. It holds a `documents` list and one `facts` array, and nothing else. The documents are the 10-Q 0001375365-26-000007 filed 2026-02-06, the 10-Q 0001375365-26-000014 filed 2026-05-11 and the 10-K 0001375365-26-000022 filed 2026-08-31. The file is larger than I can hold in context at once, so I did not read all of it. I read:
- lines 1–4,050: the start of the February 10-Q block, with its balance sheet, income statement and comprehensive income facts;
- lines 32,880–33,140: where the May 10-Q block starts;
- lines 67,025–72,025: the end of the May 10-Q block, then the 10-K's balance sheet, income statement, comprehensive income and the start of its equity statement;
- lines 74,250–75,000: the end of the 10-K's operating cash flow section;
- lines 113,700–114,970: the end of the file;
- short probes near lines 20,000, 25,000, 30,000, 32,300, 35,000, 40,000, 60,000, 65,000, 67,000, 68,500, 70,000, 73,600, 75,000, 80,000 and 100,000.

About 100,000 lines of the facts file I did not read. Any restated value, change of tag or note marker in those lines is missing from this report.

**Periods with no cells.** `quarters-back-0` (target end 2026-06-30) has no cells at all, so there is nothing to quote for any metric in it. The reason the period gives: "no quarter ending within 20 days of 2026-06-30 is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py". The same reason, with target 2025-07-01, empties `quarters-back-4`. The fourth-quarter derivation that reason names is not in my directory. The only fourth-quarter figures in my input are the ones the 8-K prints, and they appear as release items below. Because `quarters-back-0` is empty, I also itemize `quarters-back-1` (2026-01-01..2026-03-31), the latest quarter the table fills, alongside the required `years-back-0` items.

**What my input does not contain.**
- **No articulation checks.** No section of either JSON file holds articulation checks, so there are no articulation-gap items.
- **No restatement traces.** Facts from the two 10-Qs carry a `superseded_by` field naming the later filing that re-reported the same context. Where I could set a superseded fact beside its replacement, the convertible-note conversion ratios differ, and I report them below. The superseded facts I compared and found equal are the February 10-Q's 2025-06-30 balance sheet facts against the 10-K's 2025-06-30 facts (cash, receivables, allowance, inventories, prepaid and other, current assets, PP&E, deferred tax assets, other assets, total assets, payables, accrued liabilities, income taxes, both contract-liability lines, current liabilities, convertible notes, other long-term liabilities, total liabilities, common stock and APIC, AOCI, retained earnings, stockholders' equity, non-controlling interest, and the related-party lines among them). I did not compare the facts the February 10-Q marks as superseded by the May 10-Q (for example its 2025-12-31 total equity 6992177000 and its first-quarter equity-statement rows), because I did not read the matching May facts.
- **No change of tag.** Nothing in my input says a period rests on a different concept. Every trend input for each metric uses one tag across all filled periods. Some trend inputs come from a filing later than the period's own; for example, quarters-back-5 revenue and cost of revenue come from 0001375365-26-000014. That is a later filing re-reporting the period, not a change of concept.
- **No note marker.** No fact I read carries a field saying whether its element sat inside a note. Every fact has the keys id, paragraph_id, tag, prefix, namespace, context, context_ref, unit, decimals, value, number, nil, form, source_accession and filing_date, and some also have superseded_by. So I cannot route any fact to the notes heading. By that heading's own rule, every fact item sits under the statements heading, including facts whose location (statement face or note) my input does not record: purchase obligations, unrecognized tax benefits, conversion ratios and related-party amounts among them.
- **The R&D-capitalization baseline has no paragraph ids.** Its values in each annual period print without a paragraph id, so I cannot quote them. For years-back-0 it prints research_and_development_asset 1735959400.0, research_and_development_amortization 380800000.0, earnings_with_rnd_capitalized 2620885000.0 and book_value_with_rnd_capitalized 16215411400.0. Its capitalized_development_cost and capitalized_over_expense are missing: "no row for capitalized_development_cost: the companyfacts record tags none of us-gaap:CapitalizedComputerSoftwareAdditions in any period". I itemize only its R&D expense input, which is a quotable fact.
- **The 8-K's lists have no paragraph ids.** The 8-K file's item-code list and late-filing list print no paragraph ids, so they are not items.
- **No prior predictions.** None are on record for this company.
- **Nothing that marks a broken run.** My directory holds no prices, abnormal returns, short interest, other companies' files, prior probabilities or outcome windows. The only price-denominated content is the 10-K's own tagged facts (the SharePrice milestones of the CEO performance award and EntityPublicFloat), which are filing content.

**Conventions.**
- `expected_direction` is the direction from the comparison value to the reported value, both as printed in my input:
  - a trend cell: the sign of Python's year_over_year change;
  - a fact or release line: from the earlier period to the later;
  - a restated value: from the earlier filing to the later;
  - guidance: from the latest reported figure to the guided range.
- `none` means my input prints no comparison, or the item is insufficient. `expected_direction` is not a forecast.
- `horizon` names the periods compared.
- Values are copied as printed; I did no arithmetic.
- Release items quote the 8-K's condensed statements and release text, not notes, and sit under the statements heading.

## Seen in the statements

```json
[
  {
    "id": "earnings_quality_accruals_over_total_assets_annual_trend",
    "what_changed": "accruals_over_total_assets for years-back-0 is 0.3018934051020143; year_over_year change 0.3454553477419492 against years-back-1, whose cell prints -0.0435619426399349. Inputs from 0001375365-26-000022: net_income 2230453000.0, operating_cash_flow -6809886000.0, assets 29945467000.0. Position in the company's own filed history: second highest of the 5 filled years (the years-back-2 cell, 0.37030367718926305, prints highest).",
    "account": "accruals: (net income - operating cash flow) / total assets",
    "expected_direction": "up",
    "horizon": "years-back-0 (2025-07-01..2026-06-30) against years-back-1 (2024-07-01..2025-06-30)",
    "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
    "paragraph_id": "0001375365-26-000022:trends:accruals_over_total_assets:2025-07-01..2026-06-30"
  },
  {
    "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual_trend",
    "what_changed": "bad_debt_reserve_ratio for years-back-0 is 1.779439894356776e-05; year_over_year change 1.779439894356776e-05 against years-back-1, whose cell prints 0.0 (allowance input 0.0 at 2025-06-30). Inputs: AllowanceForDoubtfulAccountsReceivableCurrent 109000.0 and AccountsReceivableNetCurrent 6125414000.0 at 2026-06-30. Position: second lowest of the 5 filled years.",
    "account": "allowance for credit losses / (receivables + allowance)",
    "expected_direction": "up",
    "horizon": "years-back-0 (2025-07-01..2026-06-30) against years-back-1 (2024-07-01..2025-06-30)",
    "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
    "paragraph_id": "0001375365-26-000022:trends:bad_debt_reserve_ratio:2025-07-01..2026-06-30"
  },
  {
    "id": "revenue_recognition_contract_liabilities_over_revenue_annual_trend",
    "what_changed": "contract_liabilities_over_revenue for years-back-0 is 0.04039633646836582; year_over_year change 0.02361423674363382 against years-back-1 (0.016782099724732002). Inputs: ContractWithCustomerLiabilityCurrent 1578005000.0 at 2026-06-30 and RevenueFromContractWithCustomerExcludingAssessedTax 39063072000.0. The formula's contract_liabilities input is the current tag only; the 10-K also tags ContractWithCustomerLiabilityNoncurrent 1034027000 at 2026-06-30, which this ratio does not include. Position: highest of the 5 filled years.",
    "account": "contract liabilities (deferred revenue, current) / revenue",
    "expected_direction": "up",
    "horizon": "years-back-0 (2025-07-01..2026-06-30) against years-back-1 (2024-07-01..2025-06-30)",
    "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
    "paragraph_id": "0001375365-26-000022:trends:contract_liabilities_over_revenue:2025-07-01..2026-06-30"
  },
  {
    "id": "earnings_quality_days_sales_of_inventory_annual_trend",
    "what_changed": "days_sales_of_inventory for years-back-0 is 135.12015074942542; year_over_year change 47.70195482185973 against years-back-1 (87.41819592756569). Inputs: InventoryNet 12895949000.0 at 2026-06-30, CostOfRevenue 34835821000.0, 365 days. Position: highest of the 5 filled years.",
    "account": "inventory / cost of revenue x days",
    "expected_direction": "up",
    "horizon": "years-back-0 (2025-07-01..2026-06-30) against years-back-1 (2024-07-01..2025-06-30)",
    "quote": "\"position_in_history\": \"highest of the 5 filled years\"",
    "paragraph_id": "0001375365-26-000022:trends:days_sales_of_inventory:2025-07-01..2026-06-30"
  },
  {
    "id": "revenue_recognition_days_sales_outstanding_annual_trend",
    "what_changed": "days_sales_outstanding for years-back-0 is 57.23503031200414; year_over_year change 20.62310184399921 against years-back-1 (36.61192846800493). Inputs: AccountsReceivableNetCurrent 6125414000.0 at 2026-06-30, revenue 39063072000.0, 365 days. Position: second lowest of the 5 filled years.",
    "account": "accounts receivable / revenue x days",
    "expected_direction": "up",
    "horizon": "years-back-0 (2025-07-01..2026-06-30) against years-back-1 (2024-07-01..2025-06-30)",
    "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
    "paragraph_id": "0001375365-26-000022:trends:days_sales_outstanding:2025-07-01..2026-06-30"
  },
  {
    "id": "earnings_quality_gross_margin_annual_trend",
    "what_changed": "gross_margin for years-back-0 is 0.10821604097086886; year_over_year change -0.0023755007711321885 against years-back-1 (0.11059154174200105). Inputs: revenue 39063072000.0, CostOfRevenue 34835821000.0. Position: lowest of the 5 filled years.",
    "account": "gross margin",
    "expected_direction": "down",
    "horizon": "years-back-0 (2025-07-01..2026-06-30) against years-back-1 (2024-07-01..2025-06-30)",
    "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
    "paragraph_id": "0001375365-26-000022:trends:gross_margin:2025-07-01..2026-06-30"
  },
  {
    "id": "estimates_and_discretion_inventory_reserve_ratio_annual_trend_insufficient",
    "what_changed": "insufficient. The years-back-0 cell has no value; its reason is quoted. The coverage block lists inventory_reserve_ratio as filled in 0 periods (every quarter and every year in the window), so there is no value and no history to place one in.",
    "account": "inventory valuation reserve ratio",
    "expected_direction": "none",
    "horizon": "years-back-0 (2025-07-01..2026-06-30)",
    "quote": "\"missing\": \"no row for inventory_reserve in 2026-06-30: us-gaap:InventoryValuationReserves is in the record, but not for this period\"",
    "paragraph_id": "0001375365-26-000022:trends:inventory_reserve_ratio:2025-07-01..2026-06-30"
  },
  {
    "id": "earnings_quality_non_gaap_gap_annual_trend_insufficient",
    "what_changed": "insufficient. The years-back-0 cell has no value; its reason is quoted. The coverage block lists non_gaap_gap as filled in 0 periods. The 8-K prints non-GAAP figures (release item below), but no gap is computed in my input and I compute none.",
    "account": "gap between non-GAAP and GAAP net income",
    "expected_direction": "none",
    "horizon": "years-back-0 (2025-07-01..2026-06-30)",
    "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
    "paragraph_id": "0001375365-26-000022:trends:non_gaap_gap:2025-07-01..2026-06-30"
  },
  {
    "id": "revenue_recognition_receivables_over_revenue_annual_trend",
    "what_changed": "receivables_over_revenue for years-back-0 is 0.15680830222466888; year_over_year change 0.056501648887669065 against years-back-1 (0.10030665333699981). Inputs: AccountsReceivableNetCurrent 6125414000.0, revenue 39063072000.0. Position: second lowest of the 5 filled years.",
    "account": "accounts receivable / revenue",
    "expected_direction": "up",
    "horizon": "years-back-0 (2025-07-01..2026-06-30) against years-back-1 (2024-07-01..2025-06-30)",
    "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
    "paragraph_id": "0001375365-26-000022:trends:receivables_over_revenue:2025-07-01..2026-06-30"
  },
  {
    "id": "earnings_quality_soft_asset_share_annual_trend",
    "what_changed": "soft_asset_share for years-back-0 is 0.7279378878946854; year_over_year change 0.13271926532292644 against years-back-1 (0.595218622571759). Inputs: Assets 29945467000.0, PropertyPlantAndEquipmentNet 625553000.0, CashAndCashEquivalentsAtCarryingValue 7521474000.0 at 2026-06-30. Position: second lowest of the 5 filled years.",
    "account": "soft assets: (assets - PP&E - cash) / assets",
    "expected_direction": "up",
    "horizon": "years-back-0 (2025-07-01..2026-06-30) against years-back-1 (2024-07-01..2025-06-30)",
    "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
    "paragraph_id": "0001375365-26-000022:trends:soft_asset_share:2025-07-01..2026-06-30"
  },
  {
    "id": "estimates_and_discretion_warranty_reserve_ratio_annual_trend",
    "what_changed": "warranty_reserve_ratio for years-back-0 is 0.0007258517712073439; year_over_year change -4.576517727655218e-05 against years-back-1 (0.0007716169484838961). Inputs: StandardProductWarrantyAccrual 28354000.0 at 2026-06-30, revenue 39063072000.0. Position: lowest of the 5 filled years.",
    "account": "warranty accrual / revenue",
    "expected_direction": "down",
    "horizon": "years-back-0 (2025-07-01..2026-06-30) against years-back-1 (2024-07-01..2025-06-30)",
    "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
    "paragraph_id": "0001375365-26-000022:trends:warranty_reserve_ratio:2025-07-01..2026-06-30"
  },
  {
    "id": "earnings_quality_accruals_over_total_assets_quarterly_trend_insufficient",
    "what_changed": "insufficient. quarters-back-1 has no accruals value because no operating cash flow row exists for that three-month period (reason quoted). In the whole quarterly window the ratio fills only quarters-back-3 and quarters-back-7, whose cells place them among 2 filled quarters; two periods do not support a trend claim.",
    "account": "accruals: (net income - operating cash flow) / total assets",
    "expected_direction": "none",
    "horizon": "quarters-back-1 (2026-01-01..2026-03-31)",
    "quote": "\"missing\": \"no row for operating_cash_flow in 2026-01-01..2026-03-31: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
    "paragraph_id": "0001375365-26-000022:trends:accruals_over_total_assets:2026-01-01..2026-03-31"
  },
  {
    "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly_trend",
    "what_changed": "bad_debt_reserve_ratio for quarters-back-1 is 5.799937341660522e-05; quarter_over_quarter change 6.021553769825401e-06 against quarters-back-2; year_over_year change 3.2645775873558025e-05 against quarters-back-5. Inputs: allowance 488000.0 and receivables 8413396000.0 at 2026-03-31 (0001375365-26-000014). Position: second highest of the 6 filled quarters.",
    "account": "allowance for credit losses / (receivables + allowance)",
    "expected_direction": "up",
    "horizon": "quarters-back-1 (2026-01-01..2026-03-31) against quarters-back-2 and quarters-back-5",
    "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"",
    "paragraph_id": "0001375365-26-000022:trends:bad_debt_reserve_ratio:2026-01-01..2026-03-31"
  },
  {
    "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly_trend",
    "what_changed": "contract_liabilities_over_revenue for quarters-back-1 is 0.14373064412486403; quarter_over_quarter change 0.08263491774114334; year_over_year change 0.06703288918906415. Inputs: ContractWithCustomerLiabilityCurrent 1472235000.0 at 2026-03-31, quarterly revenue 10243014000.0. Position: highest of the 6 filled quarters.",
    "account": "contract liabilities (deferred revenue, current) / revenue",
    "expected_direction": "up",
    "horizon": "quarters-back-1 (2026-01-01..2026-03-31) against quarters-back-2 and quarters-back-5",
    "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
    "paragraph_id": "0001375365-26-000022:trends:contract_liabilities_over_revenue:2026-01-01..2026-03-31"
  },
  {
    "id": "earnings_quality_days_sales_of_inventory_quarterly_trend",
    "what_changed": "days_sales_of_inventory for quarters-back-1 is 108.33344065815483; quarter_over_quarter change 26.30824292043789; year_over_year change 24.59608251050217. Inputs: InventoryNet 11103376000.0 at 2026-03-31, CostOfRevenue 9224334000.0, 90 days. Position: second highest of the 6 filled quarters (the quarters-back-3 cell, 115.84876375066285, prints highest).",
    "account": "inventory / cost of revenue x days",
    "expected_direction": "up",
    "horizon": "quarters-back-1 (2026-01-01..2026-03-31) against quarters-back-2 and quarters-back-5",
    "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"",
    "paragraph_id": "0001375365-26-000022:trends:days_sales_of_inventory:2026-01-01..2026-03-31"
  },
  {
    "id": "revenue_recognition_days_sales_outstanding_quarterly_trend",
    "what_changed": "days_sales_outstanding for quarters-back-1 is 73.92410476057145; quarter_over_quarter change -5.900846347219598 against quarters-back-2 (79.82495110779105, which prints highest of the 6); year_over_year change 22.22094428775381 against quarters-back-5. Inputs: AccountsReceivableNetCurrent 8413396000.0, revenue 10243014000.0, 90 days. Position: second highest of the 6 filled quarters.",
    "account": "accounts receivable / revenue x days",
    "expected_direction": "up",
    "horizon": "quarters-back-1 (2026-01-01..2026-03-31) against quarters-back-2 and quarters-back-5",
    "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"",
    "paragraph_id": "0001375365-26-000022:trends:days_sales_outstanding:2026-01-01..2026-03-31"
  },
  {
    "id": "earnings_quality_gross_margin_quarterly_trend",
    "what_changed": "gross_margin for quarters-back-1 is 0.0994511966887871; quarter_over_quarter change 0.03648509641716065 against quarters-back-2 (0.06296610027162645, which prints lowest of the 6); year_over_year change 0.003749821467125297 against quarters-back-5. Inputs: revenue 10243014000.0, CostOfRevenue 9224334000.0. Position: third highest of the 6 filled quarters.",
    "account": "gross margin",
    "expected_direction": "up",
    "horizon": "quarters-back-1 (2026-01-01..2026-03-31) against quarters-back-2 and quarters-back-5",
    "quote": "\"position_in_history\": \"third highest of the 6 filled quarters\"",
    "paragraph_id": "0001375365-26-000022:trends:gross_margin:2026-01-01..2026-03-31"
  },
  {
    "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly_trend_insufficient",
    "what_changed": "insufficient. The quarters-back-1 cell has no value; its reason is quoted. The ratio fills in no quarter of the window.",
    "account": "inventory valuation reserve ratio",
    "expected_direction": "none",
    "horizon": "quarters-back-1 (2026-01-01..2026-03-31)",
    "quote": "\"missing\": \"no row for inventory_reserve in 2026-03-31: us-gaap:InventoryValuationReserves is in the record, but not for this period\"",
    "paragraph_id": "0001375365-26-000022:trends:inventory_reserve_ratio:2026-01-01..2026-03-31"
  },
  {
    "id": "earnings_quality_non_gaap_gap_quarterly_trend_insufficient",
    "what_changed": "insufficient. The quarters-back-1 cell has no value; its reason is quoted. No quarter of the window fills this ratio.",
    "account": "gap between non-GAAP and GAAP net income",
    "expected_direction": "none",
    "horizon": "quarters-back-1 (2026-01-01..2026-03-31)",
    "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
    "paragraph_id": "0001375365-26-000022:trends:non_gaap_gap:2026-01-01..2026-03-31"
  },
  {
    "id": "revenue_recognition_receivables_over_revenue_quarterly_trend",
    "what_changed": "receivables_over_revenue for quarters-back-1 is 0.8213789417841272; quarter_over_quarter change -0.046283570257079854 against quarters-back-2 (0.867662512041207, which prints highest of the 6); year_over_year change 0.24689938097504227 against quarters-back-5. Position: second highest of the 6 filled quarters.",
    "account": "accounts receivable / revenue",
    "expected_direction": "up",
    "horizon": "quarters-back-1 (2026-01-01..2026-03-31) against quarters-back-2 and quarters-back-5",
    "quote": "\"position_in_history\": \"second highest of the 6 filled quarters\"",
    "paragraph_id": "0001375365-26-000022:trends:receivables_over_revenue:2026-01-01..2026-03-31"
  },
  {
    "id": "earnings_quality_soft_asset_share_quarterly_trend",
    "what_changed": "soft_asset_share for quarters-back-1 is 0.9190695611027941; quarter_over_quarter change 0.08440530429756044; year_over_year change 0.20110699175551416. Inputs: Assets 23452029000.0, CashAndCashEquivalentsAtCarryingValue 1290324000.0, PropertyPlantAndEquipmentNet 607659000.0 at 2026-03-31. Position: highest of the 6 filled quarters.",
    "account": "soft assets: (assets - PP&E - cash) / assets",
    "expected_direction": "up",
    "horizon": "quarters-back-1 (2026-01-01..2026-03-31) against quarters-back-2 and quarters-back-5",
    "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
    "paragraph_id": "0001375365-26-000022:trends:soft_asset_share:2026-01-01..2026-03-31"
  },
  {
    "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly_trend",
    "what_changed": "warranty_reserve_ratio for quarters-back-1 is 0.0023203131422059953; quarter_over_quarter change 0.0005058430984267409; year_over_year change -0.001794329895607981. Inputs: StandardProductWarrantyAccrual 23767000.0 at 2026-03-31, quarterly revenue 10243014000.0. Position: second lowest of the 6 filled quarters.",
    "account": "warranty accrual / revenue",
    "expected_direction": "down",
    "horizon": "quarters-back-1 (2026-01-01..2026-03-31) against quarters-back-2 and quarters-back-5",
    "quote": "\"position_in_history\": \"second lowest of the 6 filled quarters\"",
    "paragraph_id": "0001375365-26-000022:trends:warranty_reserve_ratio:2026-01-01..2026-03-31"
  },
  {
    "id": "earnings_quality_operating_cash_outflow_annual_fact",
    "what_changed": "The 10-K tags NetCashProvidedByUsedInOperatingActivities for the year at -6809886000. The same filing tags 1659524000 for the year ended 2025-06-30 and -2485972000 for the year ended 2024-06-30. Net income for the year is tagged 2230453000. This is the operating_cash_flow input to the annual accruals cell.",
    "account": "net cash provided by (used in) operating activities",
    "expected_direction": "down",
    "horizon": "2025-07-01..2026-06-30 against 2024-07-01..2025-06-30",
    "quote": "\"value\": \"-6809886000\"",
    "paragraph_id": "0001375365-26-000022:facts:NetCashProvidedByUsedInOperatingActivities:2025-07-01..2026-06-30"
  },
  {
    "id": "earnings_quality_net_income_annual_fact",
    "what_changed": "NetIncomeLoss for the year is 2230453000, against 1048854000 for the year ended 2025-06-30 and 1152666000 for the year ended 2024-06-30 (all from the 10-K).",
    "account": "net income",
    "expected_direction": "up",
    "horizon": "2025-07-01..2026-06-30 against 2024-07-01..2025-06-30",
    "quote": "\"value\": \"2230453000\"",
    "paragraph_id": "0001375365-26-000022:facts:NetIncomeLoss:2025-07-01..2026-06-30"
  },
  {
    "id": "revenue_recognition_revenue_annual_fact",
    "what_changed": "RevenueFromContractWithCustomerExcludingAssessedTax for the year is 39063072000, against 21972042000 for the year ended 2025-06-30 and 14989251000 for the year ended 2024-06-30. CostOfRevenue is 34835821000, against 19542120000 and 12927841000.",
    "account": "revenue",
    "expected_direction": "up",
    "horizon": "2025-07-01..2026-06-30 against 2024-07-01..2025-06-30",
    "quote": "\"value\": \"39063072000\"",
    "paragraph_id": "0001375365-26-000022:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2025-07-01..2026-06-30"
  },
  {
    "id": "revenue_recognition_accounts_receivable_year_end_fact",
    "what_changed": "AccountsReceivableNetCurrent is 6125414000 at 2026-06-30, against 2203942000 at 2025-06-30. In between, the February 10-Q tags 11004122000 at 2025-12-31 and the trend input from the May 10-Q shows 8413396000.0 at 2026-03-31.",
    "account": "accounts receivable, net",
    "expected_direction": "up",
    "horizon": "2026-06-30 against 2025-06-30",
    "quote": "\"value\": \"6125414000\"",
    "paragraph_id": "0001375365-26-000022:facts:AccountsReceivableNetCurrent:2026-06-30"
  },
  {
    "id": "earnings_quality_inventory_year_end_fact",
    "what_changed": "InventoryNet is 12895949000 at 2026-06-30, against 4680375000 at 2025-06-30. In between, the February 10-Q tags 10595448000 at 2025-12-31 and the trend input from the May 10-Q shows 11103376000.0 at 2026-03-31.",
    "account": "inventories",
    "expected_direction": "up",
    "horizon": "2026-06-30 against 2025-06-30",
    "quote": "\"value\": \"12895949000\"",
    "paragraph_id": "0001375365-26-000022:facts:InventoryNet:2026-06-30"
  },
  {
    "id": "revenue_recognition_contract_liabilities_current_year_end_fact",
    "what_changed": "ContractWithCustomerLiabilityCurrent is 1578005000 at 2026-06-30, against 368737000 at 2025-06-30; the February 10-Q tags 774846000 at 2025-12-31.",
    "account": "deferred revenue (contract liabilities), current",
    "expected_direction": "up",
    "horizon": "2026-06-30 against 2025-06-30",
    "quote": "\"value\": \"1578005000\"",
    "paragraph_id": "0001375365-26-000022:facts:ContractWithCustomerLiabilityCurrent:2026-06-30"
  },
  {
    "id": "revenue_recognition_contract_liabilities_noncurrent_year_end_fact",
    "what_changed": "ContractWithCustomerLiabilityNoncurrent is 1034027000 at 2026-06-30, against 362645000 at 2025-06-30; the February 10-Q tags 527909000 at 2025-12-31. This line is outside the trend table's contract-liabilities ratio, which uses the current tag only.",
    "account": "deferred revenue (contract liabilities), non-current",
    "expected_direction": "up",
    "horizon": "2026-06-30 against 2025-06-30",
    "quote": "\"value\": \"1034027000\"",
    "paragraph_id": "0001375365-26-000022:facts:ContractWithCustomerLiabilityNoncurrent:2026-06-30"
  },
  {
    "id": "revenue_recognition_contract_liability_increase_cash_flow_fact",
    "what_changed": "IncreaseDecreaseInContractWithCustomerLiability in the year's operating cash flow is 1880650000, against 315006000 for the year ended 2025-06-30 and 111927000 for the year ended 2024-06-30.",
    "account": "change in deferred revenue (operating cash flow)",
    "expected_direction": "up",
    "horizon": "2025-07-01..2026-06-30 against 2024-07-01..2025-06-30",
    "quote": "\"value\": \"1880650000\"",
    "paragraph_id": "0001375365-26-000022:facts:IncreaseDecreaseInContractWithCustomerLiability:2025-07-01..2026-06-30"
  },
  {
    "id": "estimates_and_discretion_allowance_for_credit_losses_year_end_fact",
    "what_changed": "AllowanceForDoubtfulAccountsReceivableCurrent is 109000 at 2026-06-30, against 0 at 2025-06-30. The February 10-Q tags 572000 at 2025-12-31 and the trend input from the May 10-Q shows 488000.0 at 2026-03-31.",
    "account": "allowance for credit losses",
    "expected_direction": "up",
    "horizon": "2026-06-30 against 2025-06-30",
    "quote": "\"value\": \"109000\"",
    "paragraph_id": "0001375365-26-000022:facts:AllowanceForDoubtfulAccountsReceivableCurrent:2026-06-30"
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_related_party_revenue_fact",
    "what_changed": "Revenue tagged with the RelatedPartyMember is 29781000 for the year, against 42259000 for the year ended 2025-06-30 and 69791000 for the year ended 2024-06-30.",
    "account": "related-party revenue",
    "expected_direction": "down",
    "horizon": "2025-07-01..2026-06-30 against 2024-07-01..2025-06-30",
    "quote": "\"value\": \"29781000\"",
    "paragraph_id": "0001375365-26-000022:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2025-07-01..2026-06-30:us-gaap:RelatedPartyTransactionsByRelatedPartyAxis=us-gaap:RelatedPartyMember"
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_related_party_cost_of_revenue_fact",
    "what_changed": "CostOfRevenue tagged with the RelatedPartyMember is 725694000 for the year, against 650658000 for the year ended 2025-06-30 and 552136000 for the year ended 2024-06-30.",
    "account": "related-party cost of revenue",
    "expected_direction": "up",
    "horizon": "2025-07-01..2026-06-30 against 2024-07-01..2025-06-30",
    "quote": "\"value\": \"725694000\"",
    "paragraph_id": "0001375365-26-000022:facts:CostOfRevenue:2025-07-01..2026-06-30:us-gaap:RelatedPartyTransactionsByRelatedPartyAxis=us-gaap:RelatedPartyMember"
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_related_party_accounts_payable_fact",
    "what_changed": "AccountsPayableCurrent tagged with the RelatedPartyMember is 117062000 at 2026-06-30, against 129752000 at 2025-06-30; the February 10-Q tags 149848000 at 2025-12-31.",
    "account": "related-party accounts payable",
    "expected_direction": "down",
    "horizon": "2026-06-30 against 2025-06-30",
    "quote": "\"value\": \"117062000\"",
    "paragraph_id": "0001375365-26-000022:facts:AccountsPayableCurrent:2026-06-30:us-gaap:RelatedPartyTransactionsByRelatedPartyAxis=us-gaap:RelatedPartyMember"
  },
  {
    "id": "liquidity_and_capital_purchase_obligation_year_end_fact",
    "what_changed": "PurchaseObligation is 34200000000 at 2026-06-30 (decimals -8). The May 10-Q (0001375365-26-000014) tags PurchaseObligation 10100000000 at 2026-03-31.",
    "account": "purchase obligations",
    "expected_direction": "up",
    "horizon": "2026-06-30 against 2026-03-31",
    "quote": "\"value\": \"34200000000\"",
    "paragraph_id": "0001375365-26-000022:facts:PurchaseObligation:2026-06-30"
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_related_party_purchase_obligation_fact",
    "what_changed": "PurchaseObligation tagged with the RelatedPartyMember is 200000000 at 2026-06-30 (decimals -8). The May 10-Q tags 228600000 at 2026-03-31 (decimals -5).",
    "account": "related-party purchase obligations",
    "expected_direction": "down",
    "horizon": "2026-06-30 against 2026-03-31",
    "quote": "\"value\": \"200000000\"",
    "paragraph_id": "0001375365-26-000022:facts:PurchaseObligation:2026-06-30:us-gaap:RelatedPartyTransactionsByRelatedPartyAxis=us-gaap:RelatedPartyMember"
  },
  {
    "id": "structure_and_disclosure_changes_mandatory_convertible_preferred_fact",
    "what_changed": "PreferredStockIncludingAdditionalPaidInCapital is 4226258000 at 2026-06-30, against 0 at 2025-06-30. PreferredStockSharesIssued is 4313000 at 2026-06-30, against 0 at 2025-06-30. A class of equity absent a year earlier.",
    "account": "mandatory convertible preferred stock and APIC",
    "expected_direction": "up",
    "horizon": "2026-06-30 against 2025-06-30",
    "quote": "\"value\": \"4226258000\"",
    "paragraph_id": "0001375365-26-000022:facts:PreferredStockIncludingAdditionalPaidInCapital:2026-06-30"
  },
  {
    "id": "liquidity_and_capital_interest_expense_annual_fact",
    "what_changed": "InterestExpenseNonoperating is 194574000 for the year, against 59573000 for the year ended 2025-06-30 and 19352000 for the year ended 2024-06-30.",
    "account": "interest expense",
    "expected_direction": "up",
    "horizon": "2025-07-01..2026-06-30 against 2024-07-01..2025-06-30",
    "quote": "\"value\": \"194574000\"",
    "paragraph_id": "0001375365-26-000022:facts:InterestExpenseNonoperating:2025-07-01..2026-06-30"
  },
  {
    "id": "estimates_and_discretion_unrecognized_tax_benefits_fact",
    "what_changed": "UnrecognizedTaxBenefits is 84559000 at 2026-06-30, against 61569000 at 2025-06-30, 53441000 at 2024-06-30 and 42743000 at 2023-06-30. Of the 2026-06-30 balance, UnrecognizedTaxBenefitsThatWouldImpactEffectiveTaxRate is tagged 41400000 (30900000 at 2025-06-30).",
    "account": "unrecognized tax benefits",
    "expected_direction": "up",
    "horizon": "2026-06-30 against 2025-06-30",
    "quote": "\"value\": \"84559000\"",
    "paragraph_id": "0001375365-26-000022:facts:UnrecognizedTaxBenefits:2026-06-30"
  },
  {
    "id": "estimates_and_discretion_research_and_development_expense_baseline_input_fact",
    "what_changed": "ResearchAndDevelopmentExpense is 771232000 for the year, against 636550000 for the year ended 2025-06-30. This is the years_back 0 input of the R&D-capitalization baseline. The baseline's derived values print without a paragraph id (see the top of this report), and its capitalized_development_cost is missing in every period.",
    "account": "research and development expense",
    "expected_direction": "up",
    "horizon": "2025-07-01..2026-06-30 against 2024-07-01..2025-06-30",
    "quote": "\"value\": \"771232000\"",
    "paragraph_id": "0001375365-26-000022:facts:ResearchAndDevelopmentExpense:2025-07-01..2026-06-30"
  },
  {
    "id": "articulation_and_the_filed_history_convertible_conversion_ratio_restated_shorter_dated_notes_earlier_filing",
    "what_changed": "Restated prior value. The February 10-Q (0001375365-26-000007) tags DebtInstrumentConvertibleConversionRatio1 for the convertible senior notes due 2029, context 2025-02-20, as 0.0119842 (decimals 7), and marks the fact superseded_by 0001375365-26-000022. The May 10-Q (0001375365-26-000014) tags the same 0.0119842. The 10-K tags 0.0119482 (decimals INF) for the same context. My input carries no restatement trace that explains the difference.",
    "account": "convertible senior notes due 2029: conversion ratio",
    "expected_direction": "down",
    "horizon": "context 2025-02-20, as filed 2026-02-06 and 2026-05-11 against as filed 2026-08-31",
    "quote": "\"value\": \"0.0119842\"",
    "paragraph_id": "0001375365-26-000007:facts:DebtInstrumentConvertibleConversionRatio1:2025-02-20..2025-02-20:us-gaap:DebtInstrumentAxis=smci:ConvertibleSeniorNotesDue2029Member,us-gaap:LongtermDebtTypeAxis=us-gaap:ConvertibleNotesPayableMember"
  },
  {
    "id": "articulation_and_the_filed_history_convertible_conversion_ratio_restated_shorter_dated_notes_annual_report",
    "what_changed": "The 10-K's value for the same context as the item above: 0.0119482 (decimals INF), where both 10-Qs printed 0.0119842. The 10-K also adds two new contexts for the same notes, 2025-02-11 (0.0007455) and 2025-02-12 (0.0119480); those are new periods, not restatements.",
    "account": "convertible senior notes due 2029: conversion ratio",
    "expected_direction": "down",
    "horizon": "context 2025-02-20, as filed 2026-08-31 against as filed 2026-02-06 and 2026-05-11",
    "quote": "\"value\": \"0.0119482\"",
    "paragraph_id": "0001375365-26-000022:facts:DebtInstrumentConvertibleConversionRatio1:2025-02-20..2025-02-20:us-gaap:DebtInstrumentAxis=smci:ConvertibleSeniorNotesDue2029Member,us-gaap:LongtermDebtTypeAxis=us-gaap:ConvertibleNotesPayableMember"
  },
  {
    "id": "articulation_and_the_filed_history_convertible_conversion_ratio_restated_longer_dated_notes_earlier_filing",
    "what_changed": "Restated prior value. The February 10-Q tags DebtInstrumentConvertibleConversionRatio1 for the convertible senior notes due 2030, context 2025-06-23, as 0.0181554 (decimals 7), superseded_by 0001375365-26-000022. The May 10-Q tags 0.0181154 and the 10-K tags 0.018115 (decimals INF): three filings print three values for one context. The notes due 2028 (context 2025-02-20) print 0.0163784 in all three filings, unchanged.",
    "account": "convertible senior notes due 2030: conversion ratio",
    "expected_direction": "down",
    "horizon": "context 2025-06-23, as filed 2026-02-06 against as filed 2026-05-11 and 2026-08-31",
    "quote": "\"value\": \"0.0181554\"",
    "paragraph_id": "0001375365-26-000007:facts:DebtInstrumentConvertibleConversionRatio1:2025-06-23..2025-06-23:us-gaap:DebtInstrumentAxis=smci:ConvertibleSeniorNotesDue2030Member,us-gaap:LongtermDebtTypeAxis=us-gaap:ConvertibleNotesPayableMember"
  },
  {
    "id": "articulation_and_the_filed_history_convertible_conversion_ratio_restated_longer_dated_notes_later_quarterly_filing",
    "what_changed": "The May 10-Q's value for the context in the item above: 0.0181154 (decimals 7), superseded_by 0001375365-26-000022. The February 10-Q had printed 0.0181554, and the 10-K prints 0.018115.",
    "account": "convertible senior notes due 2030: conversion ratio",
    "expected_direction": "down",
    "horizon": "context 2025-06-23, as filed 2026-05-11 against as filed 2026-02-06",
    "quote": "\"value\": \"0.0181154\"",
    "paragraph_id": "0001375365-26-000014:facts:DebtInstrumentConvertibleConversionRatio1:2025-06-23..2025-06-23:us-gaap:DebtInstrumentAxis=smci:ConvertibleSeniorNotesDue2030Member,us-gaap:LongtermDebtTypeAxis=us-gaap:ConvertibleNotesPayableMember"
  },
  {
    "id": "articulation_and_the_filed_history_convertible_conversion_ratio_restated_longer_dated_notes_annual_report",
    "what_changed": "The 10-K's value for the same context: 0.018115 (decimals INF), against 0.0181554 in the February 10-Q and 0.0181154 in the May 10-Q.",
    "account": "convertible senior notes due 2030: conversion ratio",
    "expected_direction": "down",
    "horizon": "context 2025-06-23, as filed 2026-08-31 against as filed 2026-05-11",
    "quote": "\"value\": \"0.018115\"",
    "paragraph_id": "0001375365-26-000022:facts:DebtInstrumentConvertibleConversionRatio1:2025-06-23..2025-06-23:us-gaap:DebtInstrumentAxis=smci:ConvertibleSeniorNotesDue2030Member,us-gaap:LongtermDebtTypeAxis=us-gaap:ConvertibleNotesPayableMember"
  },
  {
    "id": "across_documents_preliminary_release_matches_annual_report_facts",
    "what_changed": "The 8-K filed 2026-08-11 calls its figures preliminary and unaudited. Every line I compared between its condensed statements (in thousands) and the 10-K facts filed 2026-08-31 prints the same value: net sales 39,063,072 and 39063072000; cost of sales 34,835,821 and 34835821000; gross profit 4,227,251 and 4227251000; operating expenses 1,456,765 and 1456765000; income tax 556,329 and 556329000; net income 2,230,453 and 2230453000; diluted EPS 3.26 and 3.26; accounts receivable 6,125,414 and 6125414000; inventories 12,895,949 and 12895949000; deferred revenue 1,578,005 and 1,034,027 against 1578005000 and 1034027000; total assets 29,945,467 and 29945467000; total liabilities 15,465,851 and 15465851000; net cash used in operating activities (6,809,886) and -6809886000. I found no line the 10-K changed from the release.",
    "account": "whole income statement, balance sheet and operating cash flow",
    "expected_direction": "none",
    "horizon": "8-K of 2026-08-11 against 10-K of 2026-08-31, fiscal year ended 2026-06-30",
    "quote": "The unaudited financial information presented in this press release is preliminary.",
    "paragraph_id": "0001375365-26-000021:8k_2_02:28"
  },
  {
    "id": "controls_audit_and_filings_preliminary_close_incomplete_release",
    "what_changed": "The release says the financial closing procedures for the quarter and year were not complete when it was issued, and that the independent registered public accounting firm had performed no procedures on the preliminary data. The 10-K facts filed later match the release on every line I compared (item above).",
    "account": "financial close and audit status at release",
    "expected_direction": "none",
    "horizon": "release of 2026-08-11 for the quarter and year ended 2026-06-30",
    "quote": "The Company has provided preliminary estimates of financial results primarily because its financial closing procedures for the quarter and fiscal year ended June 30, 2026 are not yet complete.",
    "paragraph_id": "0001375365-26-000021:8k_2_02:29"
  },
  {
    "id": "results_against_expectations_fourth_quarter_net_sales_release",
    "what_changed": "The fourth quarter (three months ended 2026-06-30) has no cells in the trend table. The release prints net sales of $11.1 billion for it, against $10.2 billion in the third quarter and $5.8 billion a year earlier; its table prints 11,119,777 against 5,756,911 thousand.",
    "account": "net sales",
    "expected_direction": "up",
    "horizon": "three months ended 2026-06-30 against three months ended 2026-03-31 and 2025-06-30",
    "quote": "Net sales of $11.1 billion versus $10.2 billion in Q3'26 and $5.8 billion in Q4'25.",
    "paragraph_id": "0001375365-26-000021:8k_2_02:7"
  },
  {
    "id": "earnings_quality_fourth_quarter_gross_margin_release",
    "what_changed": "The release prints GAAP gross margin of 17.5% for the fourth quarter, against 9.9% for the third quarter and 9.5% a year earlier, and 10.8% for the full year (11.1% the prior year, per its reconciliation table). The trend table has no fourth-quarter cell, so my input cannot place this quarter in the filed history. The latest filled quarter, quarters-back-1, prints gross_margin 0.0994511966887871, third highest of the 6 filled quarters.",
    "account": "gross margin",
    "expected_direction": "up",
    "horizon": "three months ended 2026-06-30 against three months ended 2026-03-31 and 2025-06-30",
    "quote": "Gross margin of 17.5% versus 9.9% in Q3'26 and 9.5% in Q4'25.",
    "paragraph_id": "0001375365-26-000021:8k_2_02:8"
  },
  {
    "id": "results_against_expectations_fourth_quarter_net_income_release",
    "what_changed": "The release prints fourth-quarter net income of $1,178 million, against $483 million in the third quarter and $195 million a year earlier. For the full year its table prints 2,230,453 thousand, which the 10-K fact matches.",
    "account": "net income",
    "expected_direction": "up",
    "horizon": "three months ended 2026-06-30 against three months ended 2026-03-31 and 2025-06-30",
    "quote": "Net income of $1,178 million versus $483 million in Q3'26 and $195 million in Q4'25.",
    "paragraph_id": "0001375365-26-000021:8k_2_02:9"
  },
  {
    "id": "earnings_quality_fourth_quarter_operating_cash_flow_release",
    "what_changed": "The release prints fourth-quarter operating cash flow of $747 million, against fourth-quarter net income of 1,178,217 thousand (its operations table) and full-year net cash used in operating activities of (6,809,886) thousand (its cash flow table). The trend table has no fourth-quarter cell and fills no operating cash flow for quarters-back-1 or quarters-back-2.",
    "account": "operating cash flow",
    "expected_direction": "none",
    "horizon": "three months ended 2026-06-30",
    "quote": "Cash flow provided by operations for Q4'26 of $747 million and capital expenditures and investments of $25 million.",
    "paragraph_id": "0001375365-26-000021:8k_2_02:13"
  },
  {
    "id": "earnings_quality_receivables_cash_flow_change_release",
    "what_changed": "In the year's operating cash flow, the change in accounts receivable is (3,921,872) thousand, against 533,341 thousand the prior year.",
    "account": "change in accounts receivable (operating cash flow)",
    "expected_direction": "down",
    "horizon": "year ended 2026-06-30 against year ended 2025-06-30",
    "quote": "Accounts receivable, net | (3,921,872)",
    "paragraph_id": "0001375365-26-000021:8k_2_02:54"
  },
  {
    "id": "earnings_quality_inventory_cash_flow_change_release",
    "what_changed": "In the year's operating cash flow, the change in inventories is (8,876,747) thousand, against (587,689) thousand the prior year.",
    "account": "change in inventories (operating cash flow)",
    "expected_direction": "down",
    "horizon": "year ended 2026-06-30 against year ended 2025-06-30",
    "quote": "Inventories | (8,876,747)",
    "paragraph_id": "0001375365-26-000021:8k_2_02:54"
  },
  {
    "id": "estimates_and_discretion_inventory_write_down_release",
    "what_changed": "The inventory valuation adjustment write-down is 188,110 thousand for the year, against 232,083 thousand the prior year; the 10-K fact InventoryWriteDown for the prior year prints 232083000. The trend table cannot fill inventory_reserve_ratio in any period, so this write-down is the only inventory-valuation figure in my input.",
    "account": "inventory write-down",
    "expected_direction": "down",
    "horizon": "year ended 2026-06-30 against year ended 2025-06-30",
    "quote": "Inventory valuation adjustment write-down | 188,110",
    "paragraph_id": "0001375365-26-000021:8k_2_02:54"
  },
  {
    "id": "liquidity_and_capital_bank_debt_current_release",
    "what_changed": "Lines of credit and term loans, current: 2,039,774 thousand at 2026-06-30, against 75,060 thousand at 2025-06-30. The cash flow table prints proceeds from lines of credit and term loans of 4,468,808 and repayments of (520,510) for the year.",
    "account": "lines of credit and term loans, current",
    "expected_direction": "up",
    "horizon": "2026-06-30 against 2025-06-30",
    "quote": "Lines of credit and term loans, current | 2,039,774",
    "paragraph_id": "0001375365-26-000021:8k_2_02:41"
  },
  {
    "id": "liquidity_and_capital_bank_debt_noncurrent_release",
    "what_changed": "Lines of credit and term loans, non-current: 2,016,374 thousand at 2026-06-30, against 37,415 thousand at 2025-06-30.",
    "account": "lines of credit and term loans, non-current",
    "expected_direction": "up",
    "horizon": "2026-06-30 against 2025-06-30",
    "quote": "Lines of credit and term loans, non-current | 2,016,374",
    "paragraph_id": "0001375365-26-000021:8k_2_02:41"
  },
  {
    "id": "liquidity_and_capital_total_debt_and_cash_release",
    "what_changed": "The release states cash and cash equivalents of $7.5 billion and bank debt plus convertible notes of $8.7 billion at year end. The 10-K tags cash 7521474000 and convertible notes 4664139000 (4645178000 a year earlier).",
    "account": "cash and total debt",
    "expected_direction": "none",
    "horizon": "2026-06-30",
    "quote": "As of June 30, 2026, total cash and cash equivalents was $7.5 billion and total bank debt and convertible notes were $8.7 billion.",
    "paragraph_id": "0001375365-26-000021:8k_2_02:19"
  },
  {
    "id": "liquidity_and_capital_preferred_stock_issuance_release",
    "what_changed": "Financing cash flow for the year includes mandatory convertible preferred stock issuance, net, of 4,230,844 thousand, against none the prior year. The release prints preferred stock dividends of (13,088) thousand for the quarter and the year.",
    "account": "preferred stock issuance (financing cash flow)",
    "expected_direction": "up",
    "horizon": "year ended 2026-06-30 against year ended 2025-06-30",
    "quote": "Mandatory Convertible Preferred Stock issuance, net of issuance costs | 4,230,844",
    "paragraph_id": "0001375365-26-000021:8k_2_02:54"
  },
  {
    "id": "liquidity_and_capital_common_stock_issuance_release",
    "what_changed": "Financing cash flow for the year includes common stock issuance, net, of 1,406,753 thousand, against none the prior year. Net cash provided by financing activities is 9,478,755 thousand, against 2,024,045 thousand.",
    "account": "common stock issuance (financing cash flow)",
    "expected_direction": "up",
    "horizon": "year ended 2026-06-30 against year ended 2025-06-30",
    "quote": "Common stock issuance, net of issuance costs | 1,406,753",
    "paragraph_id": "0001375365-26-000021:8k_2_02:54"
  },
  {
    "id": "results_against_expectations_next_quarter_net_sales_outlook_release",
    "what_changed": "Guidance for the quarter ending 2026-09-30: net sales of $14.5 billion to $15.5 billion, against $11.1 billion reported for the fourth quarter. GAAP diluted EPS guidance is $0.89 to $0.98 and non-GAAP $1.01 to $1.10.",
    "account": "net sales guidance",
    "expected_direction": "up",
    "horizon": "quarter ending 2026-09-30 against three months ended 2026-06-30",
    "quote": "The Company expects net sales in the range of $14.5 billion and $15.5 billion for the first quarter of fiscal year 2027 ending September 30, 2026",
    "paragraph_id": "0001375365-26-000021:8k_2_02:21"
  },
  {
    "id": "results_against_expectations_next_year_net_sales_outlook_release",
    "what_changed": "Guidance for fiscal year 2027: net sales of $65.0 billion to $72.0 billion, against $39.1 billion reported for fiscal year 2026.",
    "account": "net sales guidance",
    "expected_direction": "up",
    "horizon": "fiscal year 2027 against fiscal year ended 2026-06-30",
    "quote": "For fiscal year 2027, the Company expects net sales in the range of $65.0 billion to $72.0 billion.",
    "paragraph_id": "0001375365-26-000021:8k_2_02:22"
  },
  {
    "id": "earnings_quality_non_gaap_net_income_release",
    "what_changed": "The release prints non-GAAP net income attributable to common stockholders of $2.5 billion ($3.63 diluted) for the year, against GAAP net income of $2.2 billion ($3.26 diluted). The adjustment is stock-based compensation of $316 million, net of a $97 million tax effect. Its reconciliation table prints non-GAAP basic net income of 2,511,425 thousand against GAAP 2,195,842. The trend table's non_gaap_gap is unfilled; I compute no gap.",
    "account": "non-GAAP net income",
    "expected_direction": "up",
    "horizon": "year ended 2026-06-30 against year ended 2025-06-30",
    "quote": "Non-GAAP net income attributable to common stockholders for fiscal year 2026 was $2.5 billion, or $3.63 per diluted share, versus $1.3 billion, or $2.06 per diluted share, for fiscal year 2025.",
    "paragraph_id": "0001375365-26-000021:8k_2_02:18"
  },
  {
    "id": "earnings_quality_fourth_quarter_effective_tax_rate_release",
    "what_changed": "The GAAP effective tax rate is 19.7% for the fourth quarter, against 8.7% a year earlier; 19.9% for the year, against 12.9%.",
    "account": "effective tax rate",
    "expected_direction": "up",
    "horizon": "three months and year ended 2026-06-30 against the same periods ended 2025-06-30",
    "quote": "GAAP effective tax rate | 19.7",
    "paragraph_id": "0001375365-26-000021:8k_2_02:98"
  },
  {
    "id": "earnings_quality_fourth_quarter_selling_and_marketing_release",
    "what_changed": "Sales and marketing expense is 142,078 thousand for the fourth quarter, against 64,739 thousand a year earlier; 352,594 for the year, against 273,139. The February 10-Q tags SellingAndMarketingExpense 73078000 for the quarter ended 2025-12-31.",
    "account": "sales and marketing expense",
    "expected_direction": "up",
    "horizon": "three months ended 2026-06-30 against three months ended 2025-06-30",
    "quote": "Sales and marketing | 142,078",
    "paragraph_id": "0001375365-26-000021:8k_2_02:46"
  }
]
```

## Seen in the notes

No fact in my input carries a field saying its element sat inside a note, so I have nothing I can place here without judging it myself, which I was told not to do. The item list is empty. Under the statements heading, the purchase-obligation, unrecognized-tax-benefit, conversion-ratio and related-party items may well come from note tables. My input does not record that, so the later split cannot take it from this report.

```json
[]
```
