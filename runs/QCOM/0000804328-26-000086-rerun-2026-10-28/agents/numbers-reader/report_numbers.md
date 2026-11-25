# QCOM — numbers reader — 10-Q 0000804328-26-000086 (quarter ended 2026-06-28)

Notes outside the items:

- **Periods the record does not reach.** `quarters-back-3` (target end 2025-09-28) and `quarters-back-7` (target end 2024-09-29) have no cells. The reason the table gives for both: "no quarter ending within 20 days of … is in the companyfacts record; the commonest cause is a fiscal fourth quarter, which no filing reports as a duration — the 10-K states the year and the three 10-Qs state the first three quarters, so it is derived by src/fourth_quarter.py". My input holds no derived fourth-quarter figure. So no fourth-quarter value exists here, and no quarter-over-quarter change against `quarters-back-3` exists.
- **Articulation checks and restatement traces.** My directory has no separate articulation-check, restatement-trace or fourth-quarter-derivation section. `input_numbers.json` holds only `documents` and `facts`. The only history marker on a fact is `superseded_by`. I compared every superseded row I could pair with the later filing's row for the same period and concept.
  - Two periods are reported differently by an earlier filing:
    - Alphawave goodwill at 2025-12-18 is 2215000000 in the prior 10-Q and 2210000000 in the current 10-Q (item `articulation_and_the_filed_history_alphawave_goodwill_restated`).
    - The swap notional at 2025-09-28 is 3550000000 under SwapMember in the 10-K, and 3600000000 under InterestRateSwapMember in both 10-Qs (item `articulation_and_the_filed_history_swap_notional_reported_differently_fact`).
  - These pairs print the same value in both filings:
    - the 10-K's 2025-09-28 balance-sheet rows (cash 5520000000, receivables 4315000000, inventory 6526000000, raw materials 336000000, finished goods 2205000000, goodwill 11358000000, assets 50143000000, restricted cash 2323000000);
    - total equity at 2026-03-29 (27278000000) and at 2025-03-30 (27728000000);
    - remaining repurchase authority at 2026-03-17 (2100000000);
    - the fiscal 2025 valuation allowance change (5700000000);
    - the second-quarter valuation allowance change (-5700000000);
    - the forecast fiscal 2026 tax rates (-0.40, and 0.13 on the FDDEI member);
    - the other Alphawave allocation rows (consideration 2300000000, equity value 1800000000, 11000000 shares, cash paid 301000000, assets 2895000000, liabilities 621000000, net 2274000000, tax-deductible goodwill 0).
- **Changes of concept.** Each has its own item:
  - total equity, on StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest;
  - receivables, AccountsAndOtherReceivablesNetCurrent against AccountsReceivableNetCurrent;
  - QCT handset revenue, MobileHandsetsMember in the 10-K and HandsetsMember in the 10-Qs;
  - the FDDEI tax-rate member, FDDEIEffectiveTaxRateRenamedFromFDIIMember in the 10-K and FDDEIEffectiveTaxRateMember in the 10-Qs;
  - the swap notional, SwapMember against InterestRateSwapMember.

  Commercial paper at 2025-09-28 also carries a CreditFacilityAxis=CommercialPaperMember dimension in the prior 10-Q and no dimension in the current 10-Q (noted in `liquidity_and_capital_commercial_paper_fact`).
- **Coverage of `input_numbers.json`.** I read all 49,290 lines. The items cover:
  - every trend metric in `quarters-back-0` and `years-back-0`;
  - every period I found reported differently;
  - every change of concept I found;
  - the facts that bear on these, with year-earlier and prior-quarter comparisons where the input prints them.

  Facts that only repeat an 8-K figure, or have no comparison, are not itemised one by one. Examples are fair-value hierarchy detail, lease and debt-maturity schedules, and per-jurisdiction carryforwards.
- **The note marker.** The instructions say each fact is marked with whether its element sat inside a note. No fact in my input carries that mark. Every fact row has only these fields: `id`, `paragraph_id`, `tag`, `prefix`, `namespace`, `context`, `context_ref`, `unit`, `decimals`, `value`, `number`, `nil`, `form`, `source_accession`, `filing_date`, and sometimes `superseded_by`. This is a gap in the run's input. With no mark I place no fact under the notes heading. Items that look like note-table facts stay under the statements heading, and each says it carries no note mark.
- **Research and development capitalisation baseline.** The block in `years-back-0` prints no `paragraph_id`, so it cannot be quoted and has no item. Its `stockholders_equity` input is missing: "us-gaap:StockholdersEquity is in the record, but not for this period". So `book_value_with_rnd_capitalized` does not exist. `capitalized_development_cost` is not tagged in any period.
- **Prior flags.** None are on record for this company.
- **Inputs that should not be here.** None are present: no prices, returns, short interest, other companies' files or outcome windows.
- **`expected_direction`.** This is the direction the row points for the named account's next reported value. `down` reads adverse, `up` reads favourable, and `none` means no direction or insufficient.

## Seen in the statements

```json
[
  {
    "id": "earnings_quality_gross_margin_quarterly",
    "what_changed": "Gross margin for 2026-03-30..2026-06-28 is 0.5305117120739922 (inputs: Revenues 9947000000, CostOfRevenue 4670000000). Change against quarters-back-1: -0.007180523042528253. Change against quarters-back-4: -0.025108162503914233. Lowest of the 6 filled quarters.",
    "account": "gross margin (Revenues, CostOfRevenue)",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "\"position_in_history\": \"lowest of the 6 filled quarters\"",
    "paragraph_id": "0000804328-26-000086:trends:gross_margin:2026-03-30..2026-06-28"
  },
  {
    "id": "earnings_quality_gross_margin_annual",
    "what_changed": "Gross margin for fiscal 2024-09-30..2025-09-28 is 0.5542859723602204 (Revenues 44284000000, CostOfRevenue 19738000000). Change against years-back-1: -0.007851494915586787. Lowest of the 5 filled years.",
    "account": "gross margin (Revenues, CostOfRevenue)",
    "expected_direction": "down",
    "horizon": "next fiscal year",
    "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
    "paragraph_id": "0000804328-26-000086:trends:gross_margin:2024-09-30..2025-09-28"
  },
  {
    "id": "earnings_quality_days_sales_of_inventory_quarterly",
    "what_changed": "Days sales of inventory for 2026-03-30..2026-06-28 is 163.27387580299785 (InventoryNet 8379000000, CostOfRevenue 4670000000). Change against quarters-back-1: 26.439590088712123. Change against quarters-back-4: 38.05503081819542. Highest of the 6 filled quarters. The quarters-back-1 cell also prints a rise (27.90558600164205 against quarters-back-2).",
    "account": "inventories against cost of revenues",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
    "paragraph_id": "0000804328-26-000086:trends:days_sales_of_inventory:2026-03-30..2026-06-28"
  },
  {
    "id": "earnings_quality_days_sales_of_inventory_annual",
    "what_changed": "Days sales of inventory for fiscal 2024-09-30..2025-09-28 is 120.3497821461141 (InventoryNet 6526000000, CostOfRevenue 19738000000). Change against years-back-1: -19.32976064403833. Second lowest of the 5 filled years.",
    "account": "inventories against cost of revenues",
    "expected_direction": "none",
    "horizon": "next fiscal year",
    "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
    "paragraph_id": "0000804328-26-000086:trends:days_sales_of_inventory:2024-09-30..2025-09-28"
  },
  {
    "id": "revenue_recognition_contract_liabilities_over_revenue_quarterly",
    "what_changed": "Contract liabilities over revenue for 2026-03-30..2026-06-28 is 0.028149190710767064 (DeferredRevenueCurrent 280000000, Revenues 9947000000). Change against quarters-back-1: -0.0023253823621643445. Change against quarters-back-4: 0.0006528086557743007. Third highest of the 6 filled quarters.",
    "account": "current unearned revenues (DeferredRevenueCurrent) against revenues",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "\"position_in_history\": \"third highest of the 6 filled quarters\"",
    "paragraph_id": "0000804328-26-000086:trends:contract_liabilities_over_revenue:2026-03-30..2026-06-28"
  },
  {
    "id": "revenue_recognition_contract_liabilities_over_revenue_annual",
    "what_changed": "Contract liabilities over revenue for fiscal 2024-09-30..2025-09-28 is 0.008084183903893054 (DeferredRevenueCurrent 358000000, Revenues 44284000000). Change against years-back-1: 0.0004613719332549962. Second lowest of the 5 filled years. The denominator is a full year, so this cell is on a different scale from the quarterly cells.",
    "account": "current unearned revenues (DeferredRevenueCurrent) against revenues",
    "expected_direction": "none",
    "horizon": "next fiscal year",
    "quote": "\"position_in_history\": \"second lowest of the 5 filled years\"",
    "paragraph_id": "0000804328-26-000086:trends:contract_liabilities_over_revenue:2024-09-30..2025-09-28"
  },
  {
    "id": "earnings_quality_soft_asset_share_quarterly",
    "what_changed": "Soft asset share at 2026-06-28 is 0.8300416615824429 (Assets 57367000000, PropertyPlantAndEquipmentNet 5217000000, CashAndCashEquivalentsAtCarryingValue 4533000000). Change against quarters-back-1: 0.01391872683027262. Change against quarters-back-4: 0.011296446315044673. Highest of the 6 filled quarters.",
    "account": "total assets less PP&E and cash, over total assets",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "\"position_in_history\": \"highest of the 6 filled quarters\"",
    "paragraph_id": "0000804328-26-000086:trends:soft_asset_share:2026-03-30..2026-06-28"
  },
  {
    "id": "earnings_quality_soft_asset_share_annual",
    "what_changed": "Soft asset share at fiscal year end 2025-09-28 is 0.7963823464890414 (Assets 50143000000, PP&E 4690000000, cash 5520000000). Change against years-back-1: 0.023274321685763266. Second highest of the 5 filled years.",
    "account": "total assets less PP&E and cash, over total assets",
    "expected_direction": "down",
    "horizon": "next fiscal year",
    "quote": "\"position_in_history\": \"second highest of the 5 filled years\"",
    "paragraph_id": "0000804328-26-000086:trends:soft_asset_share:2024-09-30..2025-09-28"
  },
  {
    "id": "earnings_quality_accruals_over_total_assets_quarterly",
    "what_changed": "insufficient: the cell is not filled because there is no three-month operating cash flow for 2026-03-30..2026-06-28. The 10-Q and the 8-K print only a nine-month operating cash flow, so no quarterly accrual figure exists in my input.",
    "account": "net income less operating cash flow, over total assets",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"missing\": \"no row for operating_cash_flow in 2026-03-30..2026-06-28: us-gaap:NetCashProvidedByUsedInOperatingActivities, us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations is in the record, but not for this period\"",
    "paragraph_id": "0000804328-26-000086:trends:accruals_over_total_assets:2026-03-30..2026-06-28"
  },
  {
    "id": "earnings_quality_accruals_quarterly_history_too_short",
    "what_changed": "insufficient: the quarterly accruals series has only 2 filled quarters in the table (quarters-back-2 and quarters-back-6), so it supports no quarterly trend claim. Quarters-back-2 prints -0.036976279367952634, with a change against quarters-back-6 of -0.011659140366603107.",
    "account": "net income less operating cash flow, over total assets",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"position_in_history\": \"lowest of the 2 filled quarters\"",
    "paragraph_id": "0000804328-26-000086:trends:accruals_over_total_assets:2025-09-29..2025-12-28"
  },
  {
    "id": "earnings_quality_accruals_over_total_assets_annual",
    "what_changed": "Accruals over total assets for fiscal 2024-09-30..2025-09-28 is -0.16893684063578165 (NetIncomeLoss 5541000000, NetCashProvidedByUsedInOperatingActivities 14012000000, Assets 50143000000). Change against years-back-1: -0.131586875084779. Lowest of the 5 filled years: operating cash flow exceeds net income by the widest margin in the filed history the table holds. The same year carries an income tax expense of 7122000000 and an effective rate of 0.56 (item earnings_quality_annual_effective_tax_rate_prior_year_fact).",
    "account": "net income less operating cash flow, over total assets",
    "expected_direction": "up",
    "horizon": "next fiscal year",
    "quote": "\"position_in_history\": \"lowest of the 5 filled years\"",
    "paragraph_id": "0000804328-26-000086:trends:accruals_over_total_assets:2024-09-30..2025-09-28"
  },
  {
    "id": "revenue_recognition_days_sales_outstanding_quarterly",
    "what_changed": "insufficient: no quarterly receivables row exists under the concepts the table looks for. The 10-Q tags the balance-sheet receivable at 2026-06-28 as AccountsAndOtherReceivablesNetCurrent 4668000000, but the table does not read that concept, so no quarterly days sales outstanding exists in my input.",
    "account": "accounts receivable against revenues",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"missing\": \"no row for receivables in 2026-06-28: us-gaap:AccountsReceivableNetCurrent, us-gaap:ReceivablesNetCurrent, us-gaap:AccountsReceivableNet is in the record, but not for this period\"",
    "paragraph_id": "0000804328-26-000086:trends:days_sales_outstanding:2026-03-30..2026-06-28"
  },
  {
    "id": "revenue_recognition_days_sales_outstanding_annual",
    "what_changed": "Days sales outstanding for fiscal 2024-09-30..2025-09-28 is 23.467166470960166 (AccountsReceivableNetCurrent 2855000000, Revenues 44284000000). Change against years-back-1: 1.1188013972986504. Third highest of the 5 filled years. The receivables input is the AccountsReceivableNetCurrent concept, not the balance-sheet line (see the receivables concept items).",
    "account": "accounts receivable against revenues",
    "expected_direction": "none",
    "horizon": "next fiscal year",
    "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
    "paragraph_id": "0000804328-26-000086:trends:days_sales_outstanding:2024-09-30..2025-09-28"
  },
  {
    "id": "revenue_recognition_receivables_over_revenue_quarterly",
    "what_changed": "insufficient: the cell is not filled because there is no receivables row for 2026-06-28 under the concepts the table reads.",
    "account": "accounts receivable over revenues",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"missing\": \"no row for receivables in 2026-06-28: us-gaap:AccountsReceivableNetCurrent, us-gaap:ReceivablesNetCurrent, us-gaap:AccountsReceivableNet is in the record, but not for this period\"",
    "paragraph_id": "0000804328-26-000086:trends:receivables_over_revenue:2026-03-30..2026-06-28"
  },
  {
    "id": "revenue_recognition_receivables_over_revenue_annual",
    "what_changed": "Receivables over revenue for fiscal 2024-09-30..2025-09-28 is 0.06447023755758287 (AccountsReceivableNetCurrent 2855000000, Revenues 44284000000). Change against years-back-1: 0.004232056766042394. Third highest of the 5 filled years.",
    "account": "accounts receivable over revenues",
    "expected_direction": "none",
    "horizon": "next fiscal year",
    "quote": "\"position_in_history\": \"third highest of the 5 filled years\"",
    "paragraph_id": "0000804328-26-000086:trends:receivables_over_revenue:2024-09-30..2025-09-28"
  },
  {
    "id": "estimates_and_discretion_bad_debt_reserve_ratio_quarterly",
    "what_changed": "insufficient: no allowance row for 2026-06-28. The ratio is filled in none of the 13 periods the table requests.",
    "account": "allowance for credit losses on receivables",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"missing\": \"no row for bad_debt_allowance in 2026-06-28: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"",
    "paragraph_id": "0000804328-26-000086:trends:bad_debt_reserve_ratio:2026-03-30..2026-06-28"
  },
  {
    "id": "estimates_and_discretion_bad_debt_reserve_ratio_annual",
    "what_changed": "insufficient: no allowance row for fiscal year end 2025-09-28.",
    "account": "allowance for credit losses on receivables",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"missing\": \"no row for bad_debt_allowance in 2025-09-28: us-gaap:AccountsReceivableAllowanceForCreditLossCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivableCurrent, us-gaap:AllowanceForDoubtfulAccountsReceivable is in the record, but not for this period\"",
    "paragraph_id": "0000804328-26-000086:trends:bad_debt_reserve_ratio:2024-09-30..2025-09-28"
  },
  {
    "id": "estimates_and_discretion_inventory_reserve_ratio_quarterly",
    "what_changed": "insufficient: InventoryValuationReserves is not tagged in any period, so no inventory reserve ratio exists. This comes alongside days sales of inventory at the highest of the 6 filled quarters. The 10-Q tags its inventory components net of reserves (see the inventory component items), so the reserve itself is not in my input.",
    "account": "inventory valuation reserve",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
    "paragraph_id": "0000804328-26-000086:trends:inventory_reserve_ratio:2026-03-30..2026-06-28"
  },
  {
    "id": "estimates_and_discretion_inventory_reserve_ratio_annual",
    "what_changed": "insufficient: InventoryValuationReserves is not tagged in any period, so there is no annual inventory reserve ratio.",
    "account": "inventory valuation reserve",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"missing\": \"no row for inventory_reserve: the companyfacts record tags none of us-gaap:InventoryValuationReserves in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
    "paragraph_id": "0000804328-26-000086:trends:inventory_reserve_ratio:2024-09-30..2025-09-28"
  },
  {
    "id": "estimates_and_discretion_warranty_reserve_ratio_quarterly",
    "what_changed": "insufficient: none of the warranty accrual concepts is tagged in any period, so there is no warranty reserve ratio.",
    "account": "product warranty accrual",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
    "paragraph_id": "0000804328-26-000086:trends:warranty_reserve_ratio:2026-03-30..2026-06-28"
  },
  {
    "id": "estimates_and_discretion_warranty_reserve_ratio_annual",
    "what_changed": "insufficient: none of the warranty accrual concepts is tagged in any period, so there is no annual warranty reserve ratio.",
    "account": "product warranty accrual",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"missing\": \"no row for warranty_accrual: the companyfacts record tags none of us-gaap:StandardProductWarrantyAccrual, us-gaap:ProductWarrantyAccrual, us-gaap:StandardProductWarrantyAccrualCurrent in any period. companyfacts holds the entity-wide fact alone, so this is either a concept the company does not tag or one it states only by segment",
    "paragraph_id": "0000804328-26-000086:trends:warranty_reserve_ratio:2024-09-30..2025-09-28"
  },
  {
    "id": "earnings_quality_non_gaap_gap_quarterly",
    "what_changed": "insufficient: the table carries no non-GAAP net income, so the gap ratio does not exist. The 8-K prints GAAP net income 2,002 and non-GAAP net income 2,356 for Q3 fiscal 2026, but no computed gap exists in my input.",
    "account": "non-GAAP against GAAP net income",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
    "paragraph_id": "0000804328-26-000086:trends:non_gaap_gap:2026-03-30..2026-06-28"
  },
  {
    "id": "earnings_quality_non_gaap_gap_annual",
    "what_changed": "insufficient: there is no non-GAAP net income row for fiscal 2024-09-30..2025-09-28, so the annual gap ratio does not exist.",
    "account": "non-GAAP against GAAP net income",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"missing\": \"no row for non_gaap_net_income: no us-gaap concept carries a non-GAAP measure, and companyfacts holds us-gaap and dei facts only\"",
    "paragraph_id": "0000804328-26-000086:trends:non_gaap_gap:2024-09-30..2025-09-28"
  },
  {
    "id": "articulation_and_the_filed_history_alphawave_goodwill_restated",
    "what_changed": "Restated prior value. The prior 10-Q (0000804328-26-000061, filed 2026-04-29) gave Alphawave goodwill at the 2025-12-18 acquisition date as 2215000000, and that row is marked superseded_by 0000804328-26-000086. The current 10-Q gives 2210000000 for the same date and member (item structure_and_disclosure_changes_alphawave_goodwill). The other Alphawave allocation rows print the same values in both filings: consideration 2300000000, equity value 1800000000, 11000000 shares, cash paid 301000000, assets acquired 2895000000, liabilities assumed 621000000, net 2274000000, tax-deductible goodwill 0. My input has no restatement trace naming the line that took the difference.",
    "account": "goodwill (Alphawave purchase price allocation)",
    "expected_direction": "none",
    "horizon": "next fiscal year",
    "quote": "\"value\": \"2215000000\"",
    "paragraph_id": "0000804328-26-000061:facts:Goodwill:2025-12-18:us-gaap:BusinessAcquisitionAxis=qcom:AlphawaveMember"
  },
  {
    "id": "articulation_and_the_filed_history_swap_notional_reported_differently_fact",
    "what_changed": "The same date is reported differently by an earlier filing, under a different member. The 10-K tags the swap notional at 2025-09-28 to SwapMember as 3550000000 (decimals -6). The prior 10-Q, marked superseded_by 0000804328-26-000086, and the current 10-Q both tag the same date to InterestRateSwapMember as 3600000000 (decimals -8). Because the member changed, the superseded_by link does not join the 10-K row to the 10-Q rows. The current notional is 5000000000.0 at 2026-06-28, the same as the prior 10-Q's 2026-03-29 figure.",
    "account": "interest rate swaps (notional)",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"value\": \"3550000000\"",
    "paragraph_id": "0000804328-25-000085:facts:DerivativeNotionalAmount:2025-09-28:us-gaap:DerivativeInstrumentRiskAxis=us-gaap:SwapMember"
  },
  {
    "id": "structure_and_disclosure_changes_equity_concept_includes_noncontrolling_interest_fact",
    "what_changed": "Change of concept. The current 10-Q tags total equity as StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest: 21206000000 at 2025-09-28 and 27658000000 at 2026-06-28. The 10-K's equity statement uses the same concept. The trend table's research-and-development baseline (a block with no paragraph_id) says us-gaap:StockholdersEquity is in the record but not for the fiscal year ending 2025-09-28. Equity for that period therefore rests on a different concept from the periods where StockholdersEquity is tagged, and the baseline's book value with R&D capitalised does not exist.",
    "account": "total stockholders' equity",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"value\": \"21206000000\"",
    "paragraph_id": "0000804328-26-000086:facts:StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest:2025-09-28"
  },
  {
    "id": "structure_and_disclosure_changes_handsets_member_renamed_fact",
    "what_changed": "Change of concept. The 10-K tags QCT handset revenue to the member MobileHandsetsMember:\n- fiscal 2025: 27793000000\n- fiscal 2024: 24863000000\n- fiscal 2023: 22570000000\n\nBoth 10-Qs tag it to HandsetsMember. The prior 10-Q gives 6024000000 for 2025-12-29..2026-03-29 against 6929000000 a year earlier. The current 10-Q gives 5086000000 for 2026-03-30..2026-06-28 against 6328000000. Annual and quarterly handset series sit on differently named members, so anything keyed to one member name sees a break at the 10-K to 10-Q boundary.",
    "account": "QCT handsets revenue (member name)",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"value\": \"27793000000\"",
    "paragraph_id": "0000804328-25-000085:facts:Revenues:2024-09-30..2025-09-28:srt:ProductOrServiceAxis=qcom:MobileHandsetsMember,us-gaap:StatementBusinessSegmentsAxis=qcom:QctMember"
  },
  {
    "id": "structure_and_disclosure_changes_fddei_member_renamed_fact",
    "what_changed": "Change of concept. The 10-K tags a fiscal 2025 rate of 0.13 to the member FDDEIEffectiveTaxRateRenamedFromFDIIMember. Both 10-Qs tag the fiscal 2026 forecast rate of 0.13 to FDDEIEffectiveTaxRateMember. The 10-K also forecasts fiscal 2027 at 0.14 on the renamed FDDEI member and 0.16 on FDIIEffectiveTaxFutureRateMember. The member's own name records a rename from FDII.",
    "account": "effective tax rate component (FDDEI / FDII)",
    "expected_direction": "none",
    "horizon": "next fiscal year",
    "quote": "\"value\": \"0.13\"",
    "paragraph_id": "0000804328-25-000085:facts:EffectiveIncomeTaxRateContinuingOperations:2024-09-30..2025-09-28:us-gaap:IncomeTaxAuthorityNameAxis=qcom:FDDEIEffectiveTaxRateRenamedFromFDIIMember"
  },
  {
    "id": "articulation_and_the_filed_history_receivables_concept_differs_from_face_line",
    "what_changed": "Two concepts carry receivables at 2025-09-28. The 10-K tags the balance-sheet line as AccountsAndOtherReceivablesNetCurrent, value 4315000000 (3929000000 at 2024-09-29), which matches the 8-K's 'Accounts receivable, net' of 4,315. The trend table's annual receivables input is AccountsReceivableNetCurrent, value 2855000000. Annual days sales outstanding and receivables over revenue rest on the narrower concept. The quarterly cells are unfilled because neither concept the table looks for exists for the quarters.",
    "account": "accounts receivable, net",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"value\": \"4315000000\"",
    "paragraph_id": "0000804328-25-000085:facts:AccountsAndOtherReceivablesNetCurrent:2025-09-28"
  },
  {
    "id": "articulation_and_the_filed_history_quarterly_receivables_concept_fact",
    "what_changed": "The current 10-Q tags the balance-sheet receivable at 2026-06-28 as AccountsAndOtherReceivablesNetCurrent 4668000000, against 4315000000 at 2025-09-28. This is the concept the trend table does not read, so the quarterly receivables cells stay unfilled.",
    "account": "accounts receivable, net",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "\"value\": \"4668000000\"",
    "paragraph_id": "0000804328-26-000086:facts:AccountsAndOtherReceivablesNetCurrent:2026-06-28"
  },
  {
    "id": "revenue_recognition_receivables_cash_flow_change_fact",
    "what_changed": "The nine-month cash flow line IncreaseDecreaseInReceivables is 264000000 for 2025-09-29..2026-06-28, against -535000000 a year earlier. The sign flips between the two periods.",
    "account": "receivables (cash flow)",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "\"value\": \"264000000\"",
    "paragraph_id": "0000804328-26-000086:facts:IncreaseDecreaseInReceivables:2025-09-29..2026-06-28"
  },
  {
    "id": "revenue_recognition_deferred_revenue_cash_flow_change_fact",
    "what_changed": "The nine-month cash flow line IncreaseDecreaseInDeferredRevenue is -225000000, against 3000000 a year earlier. Current deferred revenue is 280000000 at 2026-06-28 against 358000000 at 2025-09-28. Noncurrent deferred revenue is 81000000 against 71000000.",
    "account": "deferred revenue",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "\"value\": \"-225000000\"",
    "paragraph_id": "0000804328-26-000086:facts:IncreaseDecreaseInDeferredRevenue:2025-09-29..2026-06-28"
  },
  {
    "id": "revenue_recognition_revenue_from_prior_period_obligations_fact",
    "what_changed": "Revenue recognised from performance obligations satisfied in previous periods is 165000000 for 2026-03-30..2026-06-28, against 189000000 a year earlier. Nine months: 417000000 against 691000000. The prior 10-Q gave 132000000 for 2025-12-29..2026-03-29, against 285000000 a year earlier.",
    "account": "revenue from performance obligations satisfied in prior periods",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "\"value\": \"165000000\"",
    "paragraph_id": "0000804328-26-000086:facts:ContractWithCustomerPerformanceObligationSatisfiedInPreviousPeriod:2026-03-30..2026-06-28"
  },
  {
    "id": "revenue_recognition_customer_x_concentration_fact",
    "what_changed": "The customer tagged CustomerXMember accounts for 0.23 of revenues in 2026-03-30..2026-06-28, against 0.18 a year earlier. Nine months: 0.24 against 0.20. The prior 10-Q gave 0.24 for 2025-12-29..2026-03-29 against 0.27 a year earlier. The fact carries no note mark in my input.",
    "account": "customer concentration (Customer X)",
    "expected_direction": "down",
    "horizon": "next fiscal year",
    "quote": "\"value\": \"0.23\"",
    "paragraph_id": "0000804328-26-000086:facts:ConcentrationRiskPercentage1:2026-03-30..2026-06-28:srt:MajorCustomersAxis=qcom:CustomerXMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:SalesRevenueNetMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember"
  },
  {
    "id": "revenue_recognition_customer_y_concentration_fact",
    "what_changed": "The customer tagged CustomerYMember accounts for 0.20 of revenues in 2026-03-30..2026-06-28, against 0.21 a year earlier. Nine months: 0.20 against 0.21. The prior 10-Q gave 0.22 for 2025-12-29..2026-03-29 against 0.18 a year earlier.",
    "account": "customer concentration (Customer Y)",
    "expected_direction": "none",
    "horizon": "next fiscal year",
    "quote": "\"value\": \"0.20\"",
    "paragraph_id": "0000804328-26-000086:facts:ConcentrationRiskPercentage1:2026-03-30..2026-06-28:srt:MajorCustomersAxis=qcom:CustomerYMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:SalesRevenueNetMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember"
  },
  {
    "id": "structure_and_disclosure_changes_customer_z_concentration_prior_year_only_fact",
    "what_changed": "insufficient: the customer tagged CustomerZMember has a share only for year-earlier periods. The current 10-Q gives 0.13 for 2025-03-31..2025-06-29 and 0.13 for the nine months to 2025-06-29. The prior 10-Q gave 0.10 for 2024-12-30..2025-03-30 and 0.12 for the six months to 2025-03-30. Neither 10-Q prints a Customer Z share for a fiscal 2026 period. My input does not say why the current-period value is absent.",
    "account": "customer concentration (Customer Z)",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"value\": \"0.13\"",
    "paragraph_id": "0000804328-26-000086:facts:ConcentrationRiskPercentage1:2025-03-31..2025-06-29:srt:MajorCustomersAxis=qcom:CustomerZMember,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:SalesRevenueNetMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:CustomerConcentrationRiskMember"
  },
  {
    "id": "revenue_recognition_china_revenue_share_fact",
    "what_changed": "The 10-K gives China (country:CN) as 0.46 of revenues for fiscal 2025 (20340000000), 0.46 for fiscal 2024 (17826000000) and 0.37 for fiscal 2023 (13386000000). The United States is 0.24 for fiscal 2025. The current 10-Q prints no geographic share, so no quarterly China share exists in my input.",
    "account": "revenue concentration (China)",
    "expected_direction": "none",
    "horizon": "next fiscal year",
    "quote": "\"value\": \"0.46\"",
    "paragraph_id": "0000804328-25-000085:facts:ConcentrationRiskPercentage1:2024-09-30..2025-09-28:srt:StatementGeographicalAxis=country:CN,us-gaap:ConcentrationRiskByBenchmarkAxis=us-gaap:RevenueFromContractWithCustomerMember,us-gaap:ConcentrationRiskByTypeAxis=us-gaap:GeographicConcentrationRiskMember"
  },
  {
    "id": "earnings_quality_operating_income_quarter_fact",
    "what_changed": "Operating income is 1626000000 for 2026-03-30..2026-06-28, against 2762000000 a year earlier. Nine months: 7302000000 against 9437000000. Pre-tax income is 2462000000 against 2952000000. Non-operating income rose over the same quarter (next item).",
    "account": "operating income",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "\"value\": \"1626000000\"",
    "paragraph_id": "0000804328-26-000086:facts:OperatingIncomeLoss:2026-03-30..2026-06-28"
  },
  {
    "id": "earnings_quality_nonoperating_income_quarter_fact",
    "what_changed": "Non-operating income (NonoperatingIncomeExpense) is 1014000000 for 2026-03-30..2026-06-28, against 358000000 a year earlier. Nine months: 1458000000 against 748000000. The prior 10-Q gave 94000000 for 2025-12-29..2026-03-29. The 8-K investment-and-other-income row carries the same 1,014.",
    "account": "investment and other income, net",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "\"value\": \"1014000000\"",
    "paragraph_id": "0000804328-26-000086:facts:NonoperatingIncomeExpense:2026-03-30..2026-06-28"
  },
  {
    "id": "earnings_quality_realized_gains_on_marketable_securities_fact",
    "what_changed": "Realised gains on marketable securities are 726000000 for 2026-03-30..2026-06-28, against 204000000 a year earlier. Nine months: 605000000 against 241000000. The prior 10-Q gave -64000000 for 2025-12-29..2026-03-29 and -120000000 for the six months, so the year to date held losses before this quarter. Gains on sale of other investments: 19000000 against 5000000 in the quarter, and 237000000 against 30000000 over nine months.",
    "account": "gains on marketable securities",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "\"value\": \"726000000\"",
    "paragraph_id": "0000804328-26-000086:facts:MarketableSecuritiesRealizedGainLossExcludingOtherThanTemporaryImpairments:2026-03-30..2026-06-28"
  },
  {
    "id": "earnings_quality_equity_method_income_fact",
    "what_changed": "Income from equity-method investments is 66000000 for 2026-03-30..2026-06-28, against -4000000 a year earlier. Nine months: 149000000 against 13000000. The prior 10-Q gave 44000000 for 2025-12-29..2026-03-29.",
    "account": "equity in earnings of investees",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "\"value\": \"66000000\"",
    "paragraph_id": "0000804328-26-000086:facts:IncomeLossFromEquityMethodInvestments:2026-03-30..2026-06-28"
  },
  {
    "id": "liquidity_and_capital_interest_and_dividend_income_fact",
    "what_changed": "Interest and dividend income is 97000000 for 2026-03-30..2026-06-28, against 160000000 a year earlier. Nine months: 347000000 against 495000000. The prior 10-Q gave 113000000 for 2025-12-29..2026-03-29. Interest expense is 178000000 against 168000000 in the quarter.",
    "account": "interest and dividend income",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "\"value\": \"97000000\"",
    "paragraph_id": "0000804328-26-000086:facts:InvestmentIncomeInterestAndDividend:2026-03-30..2026-06-28"
  },
  {
    "id": "earnings_quality_qsi_segment_pretax_income_fact",
    "what_changed": "QSI segment pre-tax income is 768000000 for 2026-03-30..2026-06-28, against 149000000 a year earlier. The prior 10-Q gave QSI -30000000 for 2025-12-29..2026-03-29. QSI revenue is 0 in every period shown. QSI non-operating income is 771000000 against 152000000. Nine months: QSI pre-tax 917000000 against 179000000.",
    "account": "QSI (strategic investments) pre-tax income",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "\"value\": \"768000000\"",
    "paragraph_id": "0000804328-26-000086:facts:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest:2026-03-30..2026-06-28:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=qcom:QsiMember"
  },
  {
    "id": "narrative_signs_of_operating_pressure_qct_segment_pretax_income_fact",
    "what_changed": "QCT segment pre-tax income is 2192000000 for 2026-03-30..2026-06-28, against 2671000000 a year earlier. Nine months: 7959000000 against 8774000000. QCT revenue is 8504000000 against 8993000000; the prior 10-Q gave 9076000000 for 2025-12-29..2026-03-29. QCT operating expenses are 1860000000 against 1825000000.",
    "account": "QCT pre-tax income",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "\"value\": \"2192000000\"",
    "paragraph_id": "0000804328-26-000086:facts:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest:2026-03-30..2026-06-28:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=qcom:QctMember"
  },
  {
    "id": "narrative_signs_of_operating_pressure_qtl_segment_fact",
    "what_changed": "QTL segment revenue is 1278000000 for 2026-03-30..2026-06-28, against 1318000000 a year earlier. QTL pre-tax income is 881000000 against 942000000. Nine months: revenue 4252000000 against 4172000000, and pre-tax income 3105000000 against 3028000000. The quarter is lower year on year and the nine months are higher.",
    "account": "QTL (licensing) revenue and pre-tax income",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "\"value\": \"1278000000\"",
    "paragraph_id": "0000804328-26-000086:facts:RevenueFromContractWithCustomerExcludingAssessedTax:2026-03-30..2026-06-28:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=qcom:QtlMember"
  },
  {
    "id": "articulation_and_the_filed_history_qct_cost_of_revenue_negative_sign_fact",
    "what_changed": "In the segment table, QCT CostOfRevenue is tagged with a negative value: -4452000000 for 2026-03-30..2026-06-28, against -4497000000 a year earlier. The nine-month figures are -14598000000 and -14395000000. The consolidated CostOfRevenue is positive (4670000000). The QCT cost rows in the prior 10-Q were also negative. Anything that sums segment costs by tag will carry the sign. My input has no articulation check covering this row.",
    "account": "QCT cost of revenues (segment)",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"value\": \"-4452000000\"",
    "paragraph_id": "0000804328-26-000086:facts:CostOfRevenue:2026-03-30..2026-06-28:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember,us-gaap:StatementBusinessSegmentsAxis=qcom:QctMember"
  },
  {
    "id": "articulation_and_the_filed_history_segment_pretax_nine_month_values_equal_fact",
    "what_changed": "Total operating-segment pre-tax income prints 11981000000 for both 2025-09-29..2026-06-28 and 2024-09-30..2025-06-29. For the quarter, the segment total is 3841000000 against 3762000000. Two different nine-month periods carry the same value. My input has no articulation check that tests either row, so whether this is coincidence or a copied value cannot be told here.",
    "account": "operating segments pre-tax income (total)",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"value\": \"11981000000\"",
    "paragraph_id": "0000804328-26-000086:facts:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest:2024-09-30..2025-06-29:srt:ConsolidationItemsAxis=us-gaap:OperatingSegmentsMember"
  },
  {
    "id": "narrative_signs_of_operating_pressure_all_other_segment_loss_fact",
    "what_changed": "The reconciling 'all other' row's pre-tax result is -214000000 for 2026-03-30..2026-06-28, against -10000000 a year earlier. The prior 10-Q gave -121000000 for 2025-12-29..2026-03-29. All-other revenue is 165000000 against 54000000. Nine months: -419000000 against -15000000.",
    "account": "all other segments (reconciling) pre-tax result",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "\"value\": \"-214000000\"",
    "paragraph_id": "0000804328-26-000086:facts:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest:2026-03-30..2026-06-28:srt:ConsolidationItemsAxis=us-gaap:MaterialReconcilingItemsMember,us-gaap:StatementBusinessSegmentsAxis=us-gaap:AllOtherSegmentsMember"
  },
  {
    "id": "earnings_quality_unallocated_research_and_development_fact",
    "what_changed": "Unallocated (reconciling-item) costs, quarter against year-earlier quarter:\n- R&D: 755000000 against 595000000. The prior 10-Q gave 616000000 for 2025-12-29..2026-03-29.\n- SG&A: 323000000 against 182000000 (prior 10-Q Q2: 274000000).\n- Cost of revenues: 97000000 against 65000000.\n\nThe 8-K's GAAP-to-non-GAAP reconciliation sits on these lines.",
    "account": "unallocated research and development",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "\"value\": \"755000000\"",
    "paragraph_id": "0000804328-26-000086:facts:ResearchAndDevelopmentExpense:2026-03-30..2026-06-28:srt:ConsolidationItemsAxis=us-gaap:MaterialReconcilingItemsMember"
  },
  {
    "id": "narrative_signs_of_operating_pressure_research_and_development_expense_fact",
    "what_changed": "Research and development expense is 2607000000 for 2026-03-30..2026-06-28, against 2226000000 a year earlier, while revenues are 9947000000 against 10365000000. Nine months: 7523000000 against 6672000000.",
    "account": "research and development expense",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "\"value\": \"2607000000\"",
    "paragraph_id": "0000804328-26-000086:facts:ResearchAndDevelopmentExpense:2026-03-30..2026-06-28"
  },
  {
    "id": "narrative_signs_of_operating_pressure_selling_general_administrative_fact",
    "what_changed": "Selling, general and administrative expense is 976000000 for 2026-03-30..2026-06-28, against 771000000 a year earlier. Nine months: 2738000000 against 2200000000.",
    "account": "selling, general and administrative expense",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "\"value\": \"976000000\"",
    "paragraph_id": "0000804328-26-000086:facts:SellingGeneralAndAdministrativeExpense:2026-03-30..2026-06-28"
  },
  {
    "id": "narrative_signs_of_operating_pressure_restructuring_charges_fact",
    "what_changed": "Restructuring and related costs are 68000000 for 2026-03-30..2026-06-28 and 97000000 for the nine months; no year-earlier value is printed. The prior 10-Q gave 29000000 for 2025-12-29..2026-03-29. Other operating expense is -68000000 in the quarter against 0 a year earlier.",
    "account": "restructuring charges",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "\"value\": \"68000000\"",
    "paragraph_id": "0000804328-26-000086:facts:RestructuringAndRelatedCostIncurredCost:2026-03-30..2026-06-28"
  },
  {
    "id": "earnings_quality_quarterly_effective_tax_rate_fact",
    "what_changed": "The effective tax rate is 0.19 for 2026-03-30..2026-06-28, against 0.10 a year earlier. Income tax expense is 460000000 against 286000000.",
    "account": "effective income tax rate",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "\"value\": \"0.19\"",
    "paragraph_id": "0000804328-26-000086:facts:EffectiveIncomeTaxRateContinuingOperations:2026-03-30..2026-06-28"
  },
  {
    "id": "estimates_and_discretion_second_quarter_tax_benefit_fact",
    "what_changed": "The prior 10-Q gives income tax of -5138000000 (a benefit) for 2025-12-29..2026-03-29. Its effective rate for that quarter is -2.30, against 0.09 a year earlier. This is the quarter of the valuation allowance release. The current 10-Q's nine-month tax is a benefit of -4136000000.",
    "account": "income tax (benefit), second quarter of fiscal 2026",
    "expected_direction": "none",
    "horizon": "next fiscal year",
    "quote": "\"value\": \"-5138000000\"",
    "paragraph_id": "0000804328-26-000061:facts:IncomeTaxExpenseBenefit:2025-12-29..2026-03-29"
  },
  {
    "id": "earnings_quality_annual_effective_tax_rate_prior_year_fact",
    "what_changed": "The 10-K gives an effective tax rate of 0.56 for fiscal 2025, against 0.02 for fiscal 2024. Income tax expense is 7122000000 against 226000000. Fiscal 2025 is the year the valuation allowance was set up, and the tax expense depresses that year's net income of 5541000000 in the trend table.",
    "account": "annual effective income tax rate",
    "expected_direction": "none",
    "horizon": "next fiscal year",
    "quote": "\"value\": \"0.56\"",
    "paragraph_id": "0000804328-25-000085:facts:EffectiveIncomeTaxRateContinuingOperations:2024-09-30..2025-09-28"
  },
  {
    "id": "estimates_and_discretion_forecast_annual_tax_rate_fact",
    "what_changed": "The 10-Q states a forecast effective tax rate of -0.40 for fiscal 2026 (2025-09-29..2026-09-27, ScenarioForecastMember). The prior 10-Q gave the same -0.40. Nine-month income tax is a benefit of -4136000000 against an expense of 1034000000.",
    "account": "annual effective income tax rate (forecast)",
    "expected_direction": "none",
    "horizon": "next fiscal year",
    "quote": "\"value\": \"-0.40\"",
    "paragraph_id": "0000804328-26-000086:facts:EffectiveIncomeTaxRateContinuingOperations:2025-09-29..2026-09-27:srt:StatementScenarioAxis=srt:ScenarioForecastMember"
  },
  {
    "id": "estimates_and_discretion_fddei_forecast_rate_fact",
    "what_changed": "The 10-Q tags a forecast rate of 0.13 for fiscal 2026 to the member FDDEIEffectiveTaxRateMember; the prior 10-Q gave the same 0.13. The rate's basis is not in my input. See the member-rename item for the 10-K's version of this member.",
    "account": "effective tax rate component (FDDEI, forecast)",
    "expected_direction": "none",
    "horizon": "next fiscal year",
    "quote": "\"value\": \"0.13\"",
    "paragraph_id": "0000804328-26-000086:facts:EffectiveIncomeTaxRateContinuingOperations:2025-09-29..2026-09-27:srt:StatementScenarioAxis=srt:ScenarioForecastMember,us-gaap:IncomeTaxAuthorityNameAxis=qcom:FDDEIEffectiveTaxRateMember"
  },
  {
    "id": "estimates_and_discretion_valuation_allowance_release_second_quarter_fact",
    "what_changed": "The U.S. federal valuation allowance changed by -5700000000 in 2025-12-29..2026-03-29. The current 10-Q prints this row three times and the prior 10-Q printed the same value. Deferred tax assets are 5679000000 at 2026-06-28 against 743000000 at 2025-09-28. The release is a management judgement on realisability, and it carries the nine-month tax benefit.",
    "account": "deferred tax asset valuation allowance",
    "expected_direction": "none",
    "horizon": "next fiscal year",
    "quote": "\"value\": \"-5700000000\"",
    "paragraph_id": "0000804328-26-000086:facts:ValuationAllowanceDeferredTaxAssetChangeInAmount:2025-12-29..2026-03-29:us-gaap:ValuationAllowanceByDeferredTaxAssetAxis=qcom:U.S.FederalMember"
  },
  {
    "id": "estimates_and_discretion_valuation_allowance_established_prior_year_fact",
    "what_changed": "The U.S. federal valuation allowance changed by +5700000000 in fiscal 2024-09-30..2025-09-28; the 10-K and the prior 10-Q print the same value. The same amount comes back out in the second quarter of fiscal 2026 (previous item). The allowance was set up during fiscal 2025 and released in the second quarter of fiscal 2026.",
    "account": "deferred tax asset valuation allowance",
    "expected_direction": "none",
    "horizon": "next fiscal year",
    "quote": "\"value\": \"5700000000\"",
    "paragraph_id": "0000804328-26-000086:facts:ValuationAllowanceDeferredTaxAssetChangeInAmount:2024-09-30..2025-09-28:us-gaap:ValuationAllowanceByDeferredTaxAssetAxis=qcom:U.S.FederalMember"
  },
  {
    "id": "earnings_quality_valuation_allowance_balance_prior_year_end_fact",
    "what_changed": "The 10-K gives a total deferred tax asset valuation allowance of 8016000000 at 2025-09-28, against 2061000000 at 2024-09-29. Gross deferred tax assets are 9698000000 against 8111000000. Net deferred tax assets are 612000000 against 5048000000. No total allowance balance at 2026-06-28 is in my input.",
    "account": "deferred tax asset valuation allowance (balance)",
    "expected_direction": "none",
    "horizon": "next fiscal year",
    "quote": "\"value\": \"8016000000\"",
    "paragraph_id": "0000804328-25-000085:facts:DeferredTaxAssetsValuationAllowance:2025-09-28"
  },
  {
    "id": "liquidity_and_capital_accrued_income_taxes_fact",
    "what_changed": "Accrued income taxes, current, are 557000000 at 2026-06-28, against 1007000000 at 2025-09-28. The cash flow statement shows income tax payments in excess of the provision of (5,550) for the nine months.",
    "account": "accrued income taxes",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "\"value\": \"557000000\"",
    "paragraph_id": "0000804328-26-000086:facts:AccruedIncomeTaxesCurrent:2026-06-28"
  },
  {
    "id": "earnings_quality_deferred_tax_assets_prior_year_end",
    "what_changed": "The 10-K tags DeferredIncomeTaxAssetsNet (balance-sheet location: assets) at 2024-09-29 as 5162000000 and at 2025-09-28 as 743000000. The 10-Q and the 8-K print 5,679 at June 28, 2026. The balance fell in fiscal 2025 and is back above its 2024 level within three quarters, alongside the valuation allowance items.",
    "account": "deferred tax assets",
    "expected_direction": "down",
    "horizon": "next fiscal year",
    "quote": "\"value\": \"5162000000\"",
    "paragraph_id": "0000804328-25-000085:facts:DeferredIncomeTaxAssetsNet:2024-09-29:us-gaap:BalanceSheetLocationAxis=us-gaap:AssetsMember"
  },
  {
    "id": "earnings_quality_deferred_tax_assets_balance_sheet_figure",
    "what_changed": "Deferred tax assets are 5,679 at June 28, 2026, against 743 at September 28, 2025 (millions, 8-K condensed balance sheet). This agrees with the 10-Q fact DeferredIncomeTaxAssetsNet 5679000000.",
    "account": "deferred tax assets",
    "expected_direction": "down",
    "horizon": "next fiscal year",
    "quote": "| Deferred tax assets | 5,679 |  |  | 743 |  |",
    "paragraph_id": "0000804328-26-000085:8k_2_02:48"
  },
  {
    "id": "earnings_quality_income_tax_benefit_nine_months",
    "what_changed": "Income tax line: (460) in Q3 fiscal 2026 against (286) in the year-earlier quarter. Nine months: a benefit of 4,136 against an expense of (1,034). Nine-month net income is 12,377 against 8,658; the benefit is a tax item, not operating income.",
    "account": "income tax (expense) benefit",
    "expected_direction": "down",
    "horizon": "next fiscal year",
    "quote": "| Income tax (expense) benefit |  |  |  |  |  |  | (460) |  |  | (286) |  |  | 4,136 |  |  | (1,034) |  |",
    "paragraph_id": "0000804328-26-000085:8k_2_02:54"
  },
  {
    "id": "earnings_quality_income_tax_payments_in_excess_of_provision",
    "what_changed": "The cash flow statement reconciles net income with a nine-month adjustment of (5,550) for income tax payments in excess of the provision, against (1,535) a year earlier. The reported tax benefit is non-cash.",
    "account": "income taxes, cash against provision",
    "expected_direction": "none",
    "horizon": "next fiscal year",
    "quote": "| Income tax payments in excess of income tax provision | (5,550) |  |  | (1,535) |  |  |  |  |  |  |  |",
    "paragraph_id": "0000804328-26-000085:8k_2_02:60"
  },
  {
    "id": "earnings_quality_strategic_investment_gains_in_pretax_income",
    "what_changed": "In Q3 fiscal 2026, 771 of the 1,014 of investment and other income, net, sits in the QSI column. The reconciliation table prints QSI EBT of 768 within GAAP EBT of 2,462. GAAP pre-tax income in the quarter leans on investment gains outside operations.",
    "account": "investment and other income, net",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "| Investment and other income, net |  | 1,014 |  |  | 771 |  |  | — |  |  | 149 |  |  | 94 |  |",
    "paragraph_id": "0000804328-26-000085:8k_2_02:77"
  },
  {
    "id": "earnings_quality_net_gains_on_investments_nine_months",
    "what_changed": "The nine-month cash flow statement deducts net gains on marketable securities and other investments of (933), against (297) a year earlier. The 10-Q fact GainLossOnInvestments carries 933000000 against 297000000.",
    "account": "net gains on marketable securities and other investments",
    "expected_direction": "down",
    "horizon": "next fiscal year",
    "quote": "| Net gains on marketable securities and other investments | (933) |  |  | (297) |  |  |  |  |  |  |  |",
    "paragraph_id": "0000804328-26-000085:8k_2_02:60"
  },
  {
    "id": "earnings_quality_share_based_compensation_fact",
    "what_changed": "Nine-month share-based compensation is 2579000000, against 2120000000 a year earlier. The quarter's share-based compensation credited to paid-in capital is 857000000 against 687000000. The Q4 non-GAAP guidance excludes ($0.72) of share-based compensation per share.",
    "account": "share-based compensation",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "\"value\": \"2579000000\"",
    "paragraph_id": "0000804328-26-000086:facts:ShareBasedCompensation:2025-09-29..2026-06-28"
  },
  {
    "id": "earnings_quality_other_operating_assets_cash_flow_change_fact",
    "what_changed": "The nine-month cash flow line for other operating assets is -777000000, against -361000000 a year earlier. Accrued liabilities are 231000000 against -943000000. Depreciation and amortisation are 1202000000 against 1231000000.",
    "account": "other operating assets and liabilities (cash flow)",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "\"value\": \"-777000000\"",
    "paragraph_id": "0000804328-26-000086:facts:IncreaseDecreaseInOtherOperatingAssets:2025-09-29..2026-06-28"
  },
  {
    "id": "earnings_quality_other_noncurrent_assets_fact",
    "what_changed": "Other noncurrent assets are 7683000000 at 2026-06-28, against 6450000000 at 2025-09-28. Other current assets are 1653000000 against 2435000000.",
    "account": "other noncurrent assets",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "\"value\": \"7683000000\"",
    "paragraph_id": "0000804328-26-000086:facts:OtherAssetsNoncurrent:2026-06-28"
  },
  {
    "id": "across_documents_cost_of_revenues_against_trend_input",
    "what_changed": "The 8-K prints cost of revenues of 4,670 for Q3 fiscal 2026, against 4,606 a year earlier, while total revenues are 9,947 against 10,365. The trend table's CostOfRevenue input for 2026-03-30..2026-06-28 prints 4670000000.0, and the 10-Q fact is 4670000000. Both agree with the release.",
    "account": "cost of revenues",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "| Cost of revenues |  |  |  |  |  |  | 4,670 |  |  | 4,606 |  |  | 15,138 |  |  | 14,704 |  |",
    "paragraph_id": "0000804328-26-000085:8k_2_02:54"
  },
  {
    "id": "liquidity_and_capital_inventories_balance_sheet_figure",
    "what_changed": "Inventories are 8,379 at June 28, 2026, against 6,526 at September 28, 2025 (millions). This agrees with the trend input InventoryNet 8379000000.",
    "account": "inventories",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "| Inventories | 8,379 |  |  | 6,526 |  |",
    "paragraph_id": "0000804328-26-000085:8k_2_02:48"
  },
  {
    "id": "liquidity_and_capital_inventory_work_in_process_fact",
    "what_changed": "Work-in-process inventory, net of reserves, is 5005000000 at 2026-06-28, against 3985000000 at 2025-09-28. It is the largest of the three components. The fact carries no note mark in my input.",
    "account": "inventories: work in process",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "\"value\": \"5005000000\"",
    "paragraph_id": "0000804328-26-000086:facts:InventoryWorkInProcessNetOfReserves:2026-06-28"
  },
  {
    "id": "liquidity_and_capital_inventory_raw_materials_fact",
    "what_changed": "Raw materials inventory, net of reserves, is 682000000 at 2026-06-28, against 336000000 at 2025-09-28. The 10-K gave 336000000 at 2025-09-28 and 340000000 at 2024-09-29.",
    "account": "inventories: raw materials",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "\"value\": \"682000000\"",
    "paragraph_id": "0000804328-26-000086:facts:InventoryRawMaterialsNetOfReserves:2026-06-28"
  },
  {
    "id": "liquidity_and_capital_inventory_finished_goods_fact",
    "what_changed": "Finished goods inventory, net of reserves, is 2692000000 at 2026-06-28, against 2205000000 at 2025-09-28.",
    "account": "inventories: finished goods",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "\"value\": \"2692000000\"",
    "paragraph_id": "0000804328-26-000086:facts:InventoryFinishedGoodsNetOfReserves:2026-06-28"
  },
  {
    "id": "liquidity_and_capital_inventory_build_in_operating_cash_flow",
    "what_changed": "The nine-month change in inventories absorbed (1,798) of operating cash, against a release of 33 a year earlier.",
    "account": "inventories (cash flow)",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "| Inventories | (1,798) |  |  | 33 |  |  |  |  |  |  |  |",
    "paragraph_id": "0000804328-26-000085:8k_2_02:60"
  },
  {
    "id": "liquidity_and_capital_operating_cash_flow_nine_months",
    "what_changed": "Net cash provided by operating activities is 8,405 for the nine months ended June 28, 2026, against 10,016 a year earlier. Nine-month net income is 12,377 against 8,658.",
    "account": "net cash provided by operating activities",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "| Net cash provided by operating activities | 8,405 |  |  | 10,016 |  |  |  |  |  |  |  |",
    "paragraph_id": "0000804328-26-000085:8k_2_02:60"
  },
  {
    "id": "liquidity_and_capital_net_decrease_in_cash_fact",
    "what_changed": "Cash, cash equivalents and restricted cash fell by -3310000000 over the nine months to 2026-06-28, against -78000000 a year earlier. Investing used -1648000000 against -329000000. Financing used -10046000000 against -9760000000.",
    "account": "cash, cash equivalents and restricted cash",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "\"value\": \"-3310000000\"",
    "paragraph_id": "0000804328-26-000086:facts:CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsPeriodIncreaseDecreaseIncludingExchangeRateEffect:2025-09-29..2026-06-28"
  },
  {
    "id": "liquidity_and_capital_marketable_securities_current_fact",
    "what_changed": "Current marketable securities are 3771000000 at 2026-06-28, against 4635000000 at 2025-09-28. Nine-month purchases are 2449000000 against 3785000000. Sales and maturities are 3896000000 against 4892000000.",
    "account": "marketable securities",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "\"value\": \"3771000000\"",
    "paragraph_id": "0000804328-26-000086:facts:MarketableSecuritiesCurrent:2026-06-28"
  },
  {
    "id": "liquidity_and_capital_capital_expenditures_nine_months",
    "what_changed": "Nine-month capital expenditures are (1,578), against (785) a year earlier.",
    "account": "capital expenditures",
    "expected_direction": "none",
    "horizon": "next fiscal year",
    "quote": "| Capital expenditures | (1,578) |  |  | (785) |  |  |  |  |  |  |  |",
    "paragraph_id": "0000804328-26-000085:8k_2_02:60"
  },
  {
    "id": "liquidity_and_capital_short_term_debt_appears",
    "what_changed": "Short-term debt is 2,489 at June 28, 2026, against none at September 28, 2025. Long-term debt is 12,781 against 14,811 on the same balance sheet.",
    "account": "short-term debt",
    "expected_direction": "none",
    "horizon": "next fiscal year",
    "quote": "| Short-term debt | 2,489 |  |  | — |  |",
    "paragraph_id": "0000804328-26-000085:8k_2_02:48"
  },
  {
    "id": "liquidity_and_capital_commercial_paper_fact",
    "what_changed": "Commercial paper outstanding is 498000000 at 2026-06-28, against 0 at 2025-09-28. The prior 10-Q also gave 498000000 at 2026-03-29, under a program with maximum capacity of 4500000000. The prior 10-Q tagged its commercial paper rows with CreditFacilityAxis=CommercialPaperMember; the current 10-Q tags them with no dimension. Nine-month issuance is 3238000000 against 998000000, and repayments are 2743000000 against 998000000.",
    "account": "commercial paper",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "\"value\": \"498000000\"",
    "paragraph_id": "0000804328-26-000086:facts:CommercialPaper:2026-06-28"
  },
  {
    "id": "liquidity_and_capital_current_portion_long_term_debt_fact",
    "what_changed": "The current portion of long-term debt is 1991000000 at 2026-06-28, against 0 at 2025-09-28. Long-term debt is 12781000000 against 14811000000. The nine months show no long-term debt issuance (0 against 1487000000) and no other long-term debt repayment (0 against 1365000000).",
    "account": "current portion of long-term debt",
    "expected_direction": "none",
    "horizon": "next fiscal year",
    "quote": "\"value\": \"1991000000\"",
    "paragraph_id": "0000804328-26-000086:facts:LongTermDebtCurrent:2026-06-28"
  },
  {
    "id": "liquidity_and_capital_repayment_of_assumed_acquisition_debt_fact",
    "what_changed": "Nine-month repayments of assumed debt are 174000000, against 0 a year earlier. The prior 10-Q's Alphawave allocation listed 278000000 of current long-term debt assumed at 2025-12-18.",
    "account": "debt assumed in acquisitions",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "\"value\": \"174000000\"",
    "paragraph_id": "0000804328-26-000086:facts:RepaymentsOfAssumedDebt:2025-09-29..2026-06-28"
  },
  {
    "id": "liquidity_and_capital_interest_rate_swap_notional_fact",
    "what_changed": "The notional amount of interest rate swaps is 5000000000.0 at 2026-06-28, against 3600000000 at 2025-09-28 under the same member. See the articulation item for the 10-K's different figure for 2025-09-28.",
    "account": "interest rate swaps (notional)",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"value\": \"5000000000.0\"",
    "paragraph_id": "0000804328-26-000086:facts:DerivativeNotionalAmount:2026-06-28:us-gaap:DerivativeInstrumentRiskAxis=us-gaap:InterestRateSwapMember"
  },
  {
    "id": "liquidity_and_capital_long_term_debt_fair_value",
    "what_changed": "The Level 2 fair value of long-term debt at 2026-06-28 is 14000000000.0 (decimals -8). The prior 10-Q gave 13700000000 at 2026-03-29. The 8-K balance sheet prints long-term debt 12,781 and short-term debt 2,489.",
    "account": "long-term debt (fair value)",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"value\": \"14000000000.0\"",
    "paragraph_id": "0000804328-26-000086:facts:LongTermDebtFairValue:2026-06-28:us-gaap:FairValueByFairValueHierarchyLevelAxis=us-gaap:FairValueInputsLevel2Member"
  },
  {
    "id": "liquidity_and_capital_cash_and_equivalents_lower",
    "what_changed": "Cash and cash equivalents are 4,533 at June 28, 2026, against 5,520 at September 28, 2025. The trend input CashAndCashEquivalentsAtCarryingValue prints 4533000000.0.",
    "account": "cash and cash equivalents",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "| Cash and cash equivalents | $ | 4,533 |  |  | $ | 5,520 |  |",
    "paragraph_id": "0000804328-26-000085:8k_2_02:48"
  },
  {
    "id": "liquidity_and_capital_restricted_cash_released",
    "what_changed": "Restricted cash is none at June 28, 2026, against 2,323 at September 28, 2025. The 10-K fact RestrictedCashCurrent at 2025-09-28 is 2323000000, marked superseded_by 0000804328-26-000086. The current 10-Q prints the same 2323000000 for that date and 0 at 2026-06-28.",
    "account": "restricted cash",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "| Restricted cash | — |  |  | 2,323 |  |",
    "paragraph_id": "0000804328-26-000085:8k_2_02:48"
  },
  {
    "id": "liquidity_and_capital_employee_related_liabilities_fact",
    "what_changed": "Current employee-related liabilities are 1470000000 at 2026-06-28, against 1839000000 at 2025-09-28.",
    "account": "employee-related liabilities",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"value\": \"1470000000\"",
    "paragraph_id": "0000804328-26-000086:facts:EmployeeRelatedLiabilitiesCurrent:2026-06-28"
  },
  {
    "id": "liquidity_and_capital_share_repurchases_nine_months",
    "what_changed": "Nine-month repurchases and retirements of common stock are (6,806), against (6,347) a year earlier. Dividends paid are (2,868) against (2,848).",
    "account": "repurchases of common stock",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "| Repurchases and retirements of common stock | (6,806) |  |  | (6,347) |  |  |  |  |  |  |  |",
    "paragraph_id": "0000804328-26-000085:8k_2_02:60"
  },
  {
    "id": "liquidity_and_capital_shares_repurchased_count_fact",
    "what_changed": "Share counts:\n- 42000000 shares repurchased and 25000000 issued over the nine months to 2026-06-28.\n- Shares outstanding: 1057000000 at 2026-06-28 against 1074000000 at 2025-09-28.\n- The cover page gives 1050000000 at 2026-07-27.\n- Diluted weighted shares for the quarter: 1069000000 against 1099000000.",
    "account": "common shares",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "\"value\": \"42000000\"",
    "paragraph_id": "0000804328-26-000086:facts:StockRepurchasedDuringPeriodShares:2025-09-29..2026-06-28"
  },
  {
    "id": "liquidity_and_capital_remaining_repurchase_authorization_fact",
    "what_changed": "Remaining repurchase authority across programs is 20600000000 at 2026-06-28. The prior 10-Q gave 21900000000 at 2026-03-29. The current 10-Q also prints 2100000000 remaining at 2026-03-17 under the program announced November 6, 2024, the same value the prior 10-Q gave.",
    "account": "stock repurchase authorization remaining",
    "expected_direction": "none",
    "horizon": "next fiscal year",
    "quote": "\"value\": \"20600000000\"",
    "paragraph_id": "0000804328-26-000086:facts:StockRepurchaseProgramRemainingAuthorizedRepurchaseAmount1:2026-06-28:srt:ShareRepurchaseProgramAxis=qcom:StockRepurchaseProgramsAuthorizedAndRemainingMember"
  },
  {
    "id": "liquidity_and_capital_dividends_per_share_fact",
    "what_changed": "Dividends declared per share are 0.92 for 2026-03-30..2026-06-28, against 0.89 a year earlier. Nine months: 2.70 against 2.59.",
    "account": "dividends per share",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "\"value\": \"0.92\"",
    "paragraph_id": "0000804328-26-000086:facts:CommonStockDividendsPerShareDeclared:2026-03-30..2026-06-28"
  },
  {
    "id": "liquidity_and_capital_accumulated_other_comprehensive_income_fact",
    "what_changed": "Accumulated other comprehensive income is 395000000 at 2026-06-28, against 560000000 at 2025-09-28. Foreign currency translation in the quarter is -27000000, against 231000000 a year earlier.",
    "account": "accumulated other comprehensive income",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"value\": \"395000000\"",
    "paragraph_id": "0000804328-26-000086:facts:AccumulatedOtherComprehensiveIncomeLossNetOfTax:2026-06-28"
  },
  {
    "id": "structure_and_disclosure_changes_goodwill_growth_from_acquisitions",
    "what_changed": "Goodwill is 14,274 at June 28, 2026, against 11,358 at September 28, 2025. Other intangible assets, net are 1,510 against 1,148. See the acquisition fact items.",
    "account": "goodwill",
    "expected_direction": "none",
    "horizon": "next fiscal year",
    "quote": "| Goodwill | 14,274 |  |  | 11,358 |  |",
    "paragraph_id": "0000804328-26-000085:8k_2_02:48"
  },
  {
    "id": "structure_and_disclosure_changes_alphawave_goodwill",
    "what_changed": "Alphawave acquisition dated 2025-12-18, as the current 10-Q prints it:\n- goodwill 2210000000\n- consideration transferred 2300000000\n- equity interest value assigned 1800000000\n- 11000000 shares\n- PaymentsToAcquireBusinessesGross 301000000\n- assets acquired 2895000000\n- liabilities assumed 621000000\n- net 2274000000\n- tax-deductible goodwill 0\n\nThe prior 10-Q printed goodwill 2215000000 (see the restatement item). The 10-K gave an expected price of 2400000000 at the 2025-06-09 announcement. The facts carry no note mark in my input.",
    "account": "goodwill (Alphawave)",
    "expected_direction": "none",
    "horizon": "next fiscal year",
    "quote": "\"value\": \"2210000000\"",
    "paragraph_id": "0000804328-26-000086:facts:Goodwill:2025-12-18:us-gaap:BusinessAcquisitionAxis=qcom:AlphawaveMember"
  },
  {
    "id": "structure_and_disclosure_changes_stock_issued_for_acquisitions_fact",
    "what_changed": "Stock issued for acquisitions is 1903000000 for the nine months to 2026-06-28, against 0 a year earlier, with none in the latest quarter. Conversion of convertible securities adds 67000000 over the nine months. The prior 10-Q tagged exchangeable shares from the Alphawave deal: 4000000 outstanding at 2026-03-29, valued at 453000000 at the acquisition date.",
    "account": "common stock issued in acquisitions",
    "expected_direction": "none",
    "horizon": "next fiscal year",
    "quote": "\"value\": \"1903000000\"",
    "paragraph_id": "0000804328-26-000086:facts:StockIssuedDuringPeriodValueAcquisitions:2025-09-29..2026-06-28:us-gaap:StatementEquityComponentsAxis=us-gaap:CommonStockIncludingAdditionalPaidInCapitalMember"
  },
  {
    "id": "structure_and_disclosure_changes_other_acquisitions_count",
    "what_changed": "Seven other businesses were acquired in 2025-09-29..2026-06-28 (A2026OtherBusinessAcquisitionsMember). The prior 10-Q gave six for 2025-09-29..2026-03-29, with payments of 985000000 and goodwill of 698000000. For the nine months, PaymentsToAcquireBusinessesGross is 1100000000 and goodwill is 737000000, tagged 661000000 to QctMember and 76000000 to a member named DataCenterOperatingSegmentMember.",
    "account": "business acquisitions (other)",
    "expected_direction": "none",
    "horizon": "next fiscal year",
    "quote": "\"value\": \"7\"",
    "paragraph_id": "0000804328-26-000086:facts:NumberOfBusinessesAcquired:2025-09-29..2026-06-28:us-gaap:BusinessAcquisitionAxis=qcom:A2026OtherBusinessAcquisitionsMember"
  },
  {
    "id": "structure_and_disclosure_changes_data_center_segment_member_fact",
    "what_changed": "The prior 10-Q tagged 76000000 of goodwill from other acquisitions at 2026-03-29 to a member named DataCenterOperatingSegmentMember, alongside QctMember. The current 10-Q tags three reportable segments for 2025-09-29..2026-06-28 (QCT, QTL and QSI in the segment rows) and keeps the 76000000 on that member. The goodwill rows name a data center operating segment that is not one of the reportable segments.",
    "account": "segment structure",
    "expected_direction": "none",
    "horizon": "next fiscal year",
    "quote": "\"value\": \"76000000\"",
    "paragraph_id": "0000804328-26-000061:facts:Goodwill:2026-03-29:us-gaap:BusinessAcquisitionAxis=qcom:A2026OtherBusinessAcquisitionsMember,us-gaap:StatementBusinessSegmentsAxis=qcom:DataCenterOperatingSegmentMember"
  },
  {
    "id": "structure_and_disclosure_changes_reportable_segments_count_fact",
    "what_changed": "The number of reportable segments is 3 for 2025-09-29..2026-06-28.",
    "account": "reportable segments",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"value\": \"3\"",
    "paragraph_id": "0000804328-26-000086:facts:NumberOfReportableSegments:2025-09-29..2026-06-28"
  },
  {
    "id": "narrative_signs_of_operating_pressure_qct_handset_revenue_figure",
    "what_changed": "QCT handset revenues are $5,086 in Q3 fiscal 2026, against $6,328 in Q3 fiscal 2025, printed as (20%). Total QCT revenues are $8,504 against $8,993, printed as (5%). The 10-Q facts on HandsetsMember carry 5086000000 and 6328000000. Nine months: 18934000000 against 20831000000. The prior 10-Q gave 6024000000 for 2025-12-29..2026-03-29 against 6929000000.",
    "account": "QCT handsets revenue",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "| Handsets | $5,086 |  | $6,328 |  | (20%) |",
    "paragraph_id": "0000804328-26-000085:8k_2_02:24"
  },
  {
    "id": "narrative_signs_of_operating_pressure_qct_automotive_offset",
    "what_changed": "QCT automotive revenues are 1,588 in Q3 fiscal 2026 against 984, printed as +61%. IoT is 1,830 against 1,681, printed as +9%. This partly offsets the handset decline. Nine-month automotive is 4015000000 against 2904000000. The prior 10-Q gave 1326000000 for 2025-12-29..2026-03-29 against 959000000.",
    "account": "QCT automotive revenue",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "| Automotive | 1,588 |  | 984 |  | +61% |",
    "paragraph_id": "0000804328-26-000085:8k_2_02:24"
  },
  {
    "id": "narrative_signs_of_operating_pressure_input_cost_increase_and_margin",
    "what_changed": "The release states a broad rise in input costs. This sits beside quarterly gross margin at the lowest of the 6 filled quarters in the trend table. The release says pricing actions are expected to benefit gross margins 'over time'.",
    "account": "cost of revenues / gross margin",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "The semiconductor industry is experiencing a broad-based increase in input costs, across wafer fabrication, assembly, test, advanced packaging, memory and other materials.",
    "paragraph_id": "0000804328-26-000085:8k_2_02:29"
  },
  {
    "id": "results_against_expectations_fourth_quarter_revenue_guidance",
    "what_changed": "Q4 fiscal 2026 revenue guidance is $9.7B - $10.5B (QCT $8.4B - $9.0B, QTL $1.2B - $1.4B). insufficient for a year-on-year comparison: the year-earlier fourth quarter (quarters-back-3) is not in the record, and no derived fourth quarter is in my input.",
    "account": "revenues (guidance)",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "|  | Revenues |  | $9.7B - $10.5B |  |",
    "paragraph_id": "0000804328-26-000085:8k_2_02:31"
  },
  {
    "id": "results_against_expectations_fourth_quarter_gaap_eps_guidance",
    "what_changed": "Q4 fiscal 2026 GAAP diluted EPS guidance is $1.22 - $1.42, below the Q3 fiscal 2026 GAAP diluted EPS of $1.87 (10-Q fact 1.87 against 2.43 a year earlier). Non-GAAP guidance is $2.05 - $2.25 against Q3 non-GAAP of $2.21. The guidance excludes ($0.72) of share-based compensation and ($0.11) of other items.",
    "account": "diluted EPS (guidance)",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "|  | GAAP diluted EPS |  | $1.22 - $1.42 |  |",
    "paragraph_id": "0000804328-26-000085:8k_2_02:31"
  },
  {
    "id": "results_against_expectations_high_end_of_guidance_claim_unverifiable",
    "what_changed": "insufficient: the release says Q3 revenues were at the high end of guidance. The Q3 guidance range from the prior 8-K is not in my input, so the claim cannot be checked against a number here.",
    "account": "revenues against prior guidance",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "with quarterly revenues at the high end of guidance",
    "paragraph_id": "0000804328-26-000085:8k_2_02:16"
  },
  {
    "id": "structure_and_disclosure_changes_fixed_non_gaap_tax_rate",
    "what_changed": "From Q1 fiscal 2026 the non-GAAP tax provision uses a fixed estimated rate (12.5% for Q3 fiscal 2026, per footnote 2). Prior periods are not recast, so the non-GAAP net income of 2,356 against 3,040 compares across two tax methods. The GAAP quarterly rate is 0.19 against 0.10 (item earnings_quality_quarterly_effective_tax_rate_fact).",
    "account": "non-GAAP income tax provision",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "Beginning in the first quarter of fiscal 2026, we are applying a fixed estimated Non-GAAP tax rate to determine our Non-GAAP provision for income taxes.",
    "paragraph_id": "0000804328-26-000085:8k_2_02:71"
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_loss_contingency_estimate_fact",
    "what_changed": "The estimate of possible loss for contingencies is tagged 0 at 2026-06-28. The CommitmentsAndContingencies balance-sheet row is nil at both dates.",
    "account": "loss contingencies",
    "expected_direction": "none",
    "horizon": "none",
    "quote": "\"value\": \"0\"",
    "paragraph_id": "0000804328-26-000086:facts:LossContingencyEstimateOfPossibleLoss:2026-06-28"
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_modular_acquisition_consideration",
    "what_changed": "Subsequent event: consideration transferred for Modular, dated 2026-07-28, is 3100000000 (decimals -8). This dimensional fact (BusinessAcquisitionAxis=ModularMember, SubsequentEventMember) carries no note mark in my input.",
    "account": "business combination consideration (Modular)",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "\"value\": \"3100000000\"",
    "paragraph_id": "0000804328-26-000086:facts:BusinessCombinationConsiderationTransferred1:2026-07-28..2026-07-28:us-gaap:BusinessAcquisitionAxis=qcom:ModularMember,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember"
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_modular_shares_issued",
    "what_changed": "Subsequent event: 18000000 shares issued or issuable for Modular, dated 2026-07-28. The 10-Q gives 1057000000 shares outstanding at June 28, 2026 and 1050000000 on the cover at 2026-07-27.",
    "account": "common stock issued in acquisition (Modular)",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "\"value\": \"18000000\"",
    "paragraph_id": "0000804328-26-000086:facts:BusinessAcquisitionEquityInterestsIssuedOrIssuableNumberOfSharesIssued:2026-07-28..2026-07-28:us-gaap:BusinessAcquisitionAxis=qcom:ModularMember,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember"
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_modular_executive_shares_service_condition",
    "what_changed": "Subsequent event: equity valued at 700000000, covering 4000000 shares, is tagged to the member ExecutiveSharesSubjectToServiceRequirementsMember for Modular. The member name ties these shares to service requirements.",
    "account": "acquisition equity subject to service requirements (Modular)",
    "expected_direction": "down",
    "horizon": "next fiscal year",
    "quote": "\"value\": \"700000000\"",
    "paragraph_id": "0000804328-26-000086:facts:BusinessAcquisitionEquityInterestIssuedOrIssuableValueAssigned:2026-07-28:us-gaap:AwardTypeAxis=qcom:ExecutiveSharesSubjectToServiceRequirementsMember,us-gaap:BusinessAcquisitionAxis=qcom:ModularMember,us-gaap:SubsequentEventTypeAxis=us-gaap:SubsequentEventMember"
  }
]
```

## Seen in the notes

My input carries no note mark on any fact. Every fact row has only `id`, `paragraph_id`, `tag`, `prefix`, `namespace`, `context`, `context_ref`, `unit`, `decimals`, `value`, `number`, `nil`, `form`, `source_accession`, `filing_date` and sometimes `superseded_by`. The instructions say I should not judge which facts came from a note table, and with no mark to go on I place nothing under this heading. The facts above that may come from note tables stay under the statements heading, and each one says it carries no note mark:

- inventory components;
- tax rates;
- the valuation allowance;
- customer and geographic concentration;
- revenue from prior-period obligations;
- business combinations;
- subsequent events;
- fair value;
- swap notionals;
- repurchase authority.

A later split of this reader will need that mark in its input.

```json
[]
```
