# Notes-text reader report: Dell Technologies quarterly report for the second quarter of fiscal 2027 (quarter ended July 31, 2026), filing 0001571996-26-000046

## Inputs

- **Read in full:** `input_notes.md`, `input_notes_history.md` (prior filing 0001571996-26-000030, quarter ended May 1, 2026), `input_mdna.md`, `input_controls.md` (Item 4), `input_8k.md` (earnings release of September 1, 2026, filing 0001571996-26-000039, plus the list of item codes and late-filing notices) and `input_prior_predictions.md`.
- **Prior flags:** none on record.
- **Not in this input:**
  - No auditor's report.
  - No Item 1A diff.
  - No Exhibit 21 diff.
  - No Exhibit 10 pulled on trigger.
  - No 8-K bodies other than the September 1, 2026 earnings release. Earlier 8-Ks appear only as item codes.
- **Late-filing notifications:** none on or before September 8, 2026, per the input.
- **Forbidden material:** none found. There was no trend table, prices, abnormal returns, short interest, other company files, prior probabilities or outcome window.
- **No arithmetic:** no amount was added, subtracted, divided, compared or turned into a growth rate. Where the prior filing's figure is shown, it is copied from the note change history. It is not compared.

## Items

```json
[
  {
    "id": "related_parties_contingencies_and_subsequent_events_contract_manufacturer_supplier_guarantees",
    "what_changed": "New 'Guarantees' section in the commitments and contingencies note, listed as added in the note change history. Dell may guarantee contract manufacturers' payments to suppliers for components the contract manufacturers buy directly. Maximum potential future payments as of July 31, 2026 are stated as $8.6 billion, with full recourse against the contract manufacturers, and the likelihood of having to perform is called remote. The paragraph refers to the 'Consolidated Statements of Financial Position' rather than the condensed statements named elsewhere in this quarterly report, which suggests the text came from an annual report. Whether the fiscal 2026 annual report carried it is not in this input.",
    "account": "off-balance-sheet guarantees (accrued and other if called)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "As of July 31, 2026, the Company’s maximum potential future payments under the financial guarantees is $8.6 billion, which the Company would have recourse to recover in full from the applicable contract manufacturers.",
    "paragraph_id": "0001571996-26-000046:notes:165",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_contract_manufacturers_buy_components_directly",
    "what_changed": "New paragraph. Besides Dell buying components and reselling them to contract manufacturers, certain contract manufacturers may now buy components directly from suppliers, with Dell guaranteeing payment. The text does not say what share of component purchases goes through each route. It also does not say how the direct route affects Dell's inventory, non-trade receivable or payable balances.",
    "account": "inventories; other current assets (non-trade receivables)",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "certain contract manufacturers may purchase components directly from a supplier, and the Company may issue financial guarantees to a supplier in connection with the purchases by such a contract manufacturer",
    "paragraph_id": "0001571996-26-000046:notes:164",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_component_sales_to_contract_manufacturers_non_trade_receivables",
    "what_changed": "New paragraph in the commitments note, listed as added in the note change history. When title passes, components Dell buys and sells to contract manufacturers leave inventory and become non-trade receivables. No revenue or profit is recognized until Dell sells the finished product. The related cash flows are classed as operating. Agreements with most contract manufacturers let Dell offset its payables against these receivables.",
    "account": "other current assets (non-trade receivables); inventories",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The Company reflects the sale of the components by recognizing non-trade receivables from the contract manufacturers and a reduction in inventory when title and risk of loss pass to the contract manufacturer.",
    "paragraph_id": "0001571996-26-000046:notes:163",
    "explanation": false
  },
  {
    "id": "across_documents_supplier_guarantees_absent_from_mdna_and_release",
    "what_changed": "The supplier guarantees are new in the notes this quarter. The earnings release does not mention them. Neither do any of the MD&A paragraphs carried as changed in this input, including the liquidity, purchase obligation and counterparty credit risk paragraphs. MD&A paragraphs carried as unchanged are not visible here. The supervisor should check whether MD&A covers guarantees or off-balance-sheet arrangements elsewhere.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "The Company believes the likelihood of having to perform under the guarantees is remote.",
    "paragraph_id": "0001571996-26-000046:notes:165",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_purchase_obligations_by_fiscal_year",
    "what_changed": "The note now states purchase obligations as of July 31, 2026 by fiscal year: $22.4 billion for the rest of fiscal 2027, $4.9 billion for fiscal 2028, $6.1 billion for fiscal 2029, $0.8 billion for fiscal 2030, and $0.6 billion for fiscal 2031 and after. The prior quarter's note stated $16.9 billion, $1.2 billion, $1.4 billion, $0.8 billion and $0.5 billion for the same periods, as of May 1, 2026. No comparison is made here. The expected direction is taken from the MD&A text at 0001571996-26-000046:mdna:33, which says increased component purchases have led to higher purchase obligations.",
    "account": "purchase obligations (off-balance-sheet); inventories",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "As of July 31, 2026, such purchase obligations were $22.4 billion for the remainder of Fiscal 2027, $4.9 billion for Fiscal 2028, $6.1 billion for Fiscal 2029, $0.8 billion for Fiscal 2030, and $0.6 billion for Fiscal 2031 and thereafter.",
    "paragraph_id": "0001571996-26-000046:notes:161",
    "explanation": false
  },
  {
    "id": "across_documents_purchase_obligations_total_and_twelve_month_portion",
    "what_changed": "The MD&A liquidity section now states total purchase obligations and the part payable within twelve months. The note instead states amounts by fiscal year: the rest of fiscal 2027, then whole fiscal years. The two documents split the periods differently. Whether they tie is for the numbers reader and the supervisor.",
    "account": "purchase obligations (off-balance-sheet)",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "As of July 31, 2026, we had purchase obligations of $34.8 billion, of which $24.6 billion is payable within twelve months.",
    "paragraph_id": "0001571996-26-000046:mdna:192",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_component_purchases_raise_inventory_and_obligations",
    "what_changed": "The trends paragraph is carried as changed; the prior wording is not in this input. It says that, to meet demand for AI-optimized servers and their growing complexity, Dell increased its component purchases from suppliers. It says this raised inventory levels and purchase obligations and created 'new working capital dynamics', a phrase it does not define. This is management's explanation of the inventory level. It also says frequent component updates or transitions may make demand and supply harder to manage.",
    "account": "inventories",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "we have increased our purchases of certain components with suppliers, which has resulted in increased inventory levels, higher purchase obligations, and new working capital dynamics",
    "paragraph_id": "0001571996-26-000046:mdna:33",
    "explanation": true
  },
  {
    "id": "narrative_signs_of_operating_pressure_memory_component_cost_inflation",
    "what_changed": "The supply chain trend now says input costs rose because of higher component costs. It says strong AI demand, combined with capacity limits at memory manufacturers, has caused global supply constraints and substantial inflation in memory component costs. The prior wording is not in this input.",
    "account": "cost of net revenue, products",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "has resulted in global supply constraints and substantial inflation in memory component costs",
    "paragraph_id": "0001571996-26-000046:mdna:24",
    "explanation": false
  },
  {
    "id": "results_against_expectations_outlook_significant_isg_strong_csg_growth",
    "what_changed": "The revenue outlook now expects significant ISG and strong CSG net revenue growth. It says ISG growth will come mostly from demand for servers and networking and, to a lesser extent, storage. The prior wording is not in this input.",
    "account": "net revenue",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "we anticipate significant ISG and strong CSG net revenue growth",
    "paragraph_id": "0001571996-26-000046:mdna:28",
    "explanation": false
  },
  {
    "id": "results_against_expectations_csg_demand_environment_significant",
    "what_changed": "The macroeconomic trend now describes substantial demand growth for ISG, with the business mix continuing to shift toward ISG. It describes the CSG demand environment as significant, producing CSG revenue growth. The prior wording is not in this input.",
    "account": "net revenue, CSG",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "the demand environment was significant for our CSG offerings, resulting in CSG net revenue growth",
    "paragraph_id": "0001571996-26-000046:mdna:21",
    "explanation": false
  },
  {
    "id": "results_against_expectations_gross_margin_rate_from_disciplined_pricing",
    "what_changed": "MD&A attributes the second quarter's rise in gross margin rate to disciplined pricing. It attributes the first-six-months fall in the rate to a mix shift toward AI-optimized servers, largely offset by disciplined pricing. The same MD&A reports memory component cost inflation at 0001571996-26-000046:mdna:24. The margin paragraphs name pricing, not cost, as what drove the rate.",
    "account": "gross margin",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "gross margin percentage and non-GAAP gross margin percentage increased 260 basis points to 20.9% and 240 basis points to 21.1%, respectively, driven by disciplined pricing",
    "paragraph_id": "0001571996-26-000046:mdna:90",
    "explanation": false
  },
  {
    "id": "results_against_expectations_traditional_servers_growth_from_selling_price",
    "what_changed": "The rise in traditional servers and networking revenue, for both the quarter and the six months, is attributed mainly to higher average selling prices from disciplined pricing and, to a lesser extent, richer configurations. The paragraph does not mention unit growth.",
    "account": "net revenue, traditional servers and networking",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "primarily driven by an increase in the average selling price of these offerings, driven by disciplined pricing and, to a lesser extent, richer configurations",
    "paragraph_id": "0001571996-26-000046:mdna:126",
    "explanation": false
  },
  {
    "id": "results_against_expectations_ai_server_units_and_richer_configurations",
    "what_changed": "The rise in AI-optimized server revenue is attributed mainly to more units sold on higher demand and, to a lesser extent, to higher average selling prices. Higher selling prices are in turn attributed to richer configurations and, to a lesser extent, disciplined pricing.",
    "account": "net revenue, AI-optimized servers",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase in average selling prices was driven by richer configurations and, to a lesser extent, disciplined pricing.",
    "paragraph_id": "0001571996-26-000046:mdna:125",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_commercial_client_units_declined",
    "what_changed": "The rise in commercial client revenue is attributed to higher average selling prices. For the second quarter, the paragraph says units sold fell. CSG selling prices are attributed to disciplined pricing at 0001571996-26-000046:mdna:138.",
    "account": "net revenue, CSG commercial",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "During the second quarter of Fiscal 2027, the increase was partially offset by a decrease in units sold.",
    "paragraph_id": "0001571996-26-000046:mdna:136",
    "explanation": false
  },
  {
    "id": "narrative_signs_of_operating_pressure_consumer_units_declined",
    "what_changed": "The rise in consumer revenue, for both the quarter and the six months, is attributed to higher average selling prices, partly offset by a decline in units sold.",
    "account": "net revenue, CSG consumer",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "due to an increase in the average selling prices of our consumer offerings, partially offset by a decline in units sold",
    "paragraph_id": "0001571996-26-000046:mdna:137",
    "explanation": false
  },
  {
    "id": "results_against_expectations_vmware_resale_revenue_decline",
    "what_changed": "The consolidated revenue paragraph says Corporate and other revenue fell mainly because VMware Resale revenue decreased, as Dell no longer distributes standalone VMware offerings. The prior wording is not in this input.",
    "account": "net revenue, Corporate and other",
    "expected_direction": "down",
    "horizon": "this quarter",
    "quote": "Corporate and other net revenue declined primarily due to a decrease in VMware Resale revenue, as we no longer act as a distributor of standalone VMware offerings.",
    "paragraph_id": "0001571996-26-000046:mdna:77",
    "explanation": false
  },
  {
    "id": "earnings_quality_services_margin_rate_from_vmware_exit_mix",
    "what_changed": "The rise in the six-month services gross margin rate is attributed mainly to a mix shift from no longer distributing standalone VMware offerings. Management names this structural mix effect as the cause.",
    "account": "gross margin, services",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "primarily driven by a shift in mix, as we no longer act as a distributor of standalone VMware offerings",
    "paragraph_id": "0001571996-26-000046:mdna:94",
    "explanation": false
  },
  {
    "id": "results_against_expectations_services_revenue_flat",
    "what_changed": "Services net revenue is described as flat for the quarter and the six months. A decline in Corporate and other services revenue was offset by higher ISG services revenue.",
    "account": "net revenue, services",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "services net revenue remained flat as a decline in Corporate and other services net revenue was offset by an increase in ISG services net revenue",
    "paragraph_id": "0001571996-26-000046:mdna:85",
    "explanation": false
  },
  {
    "id": "earnings_quality_variable_compensation_drives_operating_expenses",
    "what_changed": "The increases in SG&A, R&D and non-GAAP operating expenses are each attributed mainly to higher employee compensation and benefits, chiefly variable compensation.",
    "account": "selling, general, and administrative; research and development",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "principally due to an increase in employee compensation and benefits expense related primarily to an increase in variable compensation",
    "paragraph_id": "0001571996-26-000046:mdna:104",
    "explanation": false
  },
  {
    "id": "earnings_quality_severance_from_workforce_reductions",
    "what_changed": "The other corporate expenses paragraph states severance expense from workforce reductions for the first six months of fiscal 2027 and of fiscal 2026. These amounts are excluded from non-GAAP results. The paragraph also notes a $0.2 billion gain in the prior year from selling Secureworks.",
    "account": "other corporate expenses; severance liability in accrued and other",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "During the first six months of Fiscal 2027 and Fiscal 2026, we recognized $0.5 billion and $0.3 billion, respectively, of severance expense related to workforce reduction activities.",
    "paragraph_id": "0001571996-26-000046:mdna:52",
    "explanation": false
  },
  {
    "id": "earnings_quality_single_investee_gain_excluded_from_non_gaap",
    "what_changed": "The non-GAAP section now states a $0.6 billion gain in the first six months from a single strategic investee. The gain is excluded from non-GAAP net income and non-GAAP earnings per share.",
    "account": "interest and other, net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "During the first six months of Fiscal 2027, we recognized a $0.6 billion gain from our strategic investment portfolio related to a single investee.",
    "paragraph_id": "0001571996-26-000046:mdna:53",
    "explanation": false
  },
  {
    "id": "earnings_quality_strategic_investment_gain_in_interest_and_other",
    "what_changed": "The investments note now states total investments of $2.7 billion at July 31, 2026 and $1.7 billion at January 30, 2026. It states a $0.7 billion total gain on investments for the six months, recorded in interest and other, net. It calls the gain immaterial in every other period shown.",
    "account": "interest and other, net; long-term investments",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The total gain on investments, net is recorded as interest and other, net in the Condensed Consolidated Statements of Income and was $0.7 billion for the six months ended July 31, 2026 and immaterial for all other presented periods.",
    "paragraph_id": "0001571996-26-000046:notes:20",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_non_marketable_observable_price_adjustment",
    "what_changed": "A footnote attributes the six-month gains on non-marketable securities mainly to a single upward observable price adjustment of $0.6 billion for one investee. It states cumulative unrealized gains on non-marketable securities of $1.8 billion and $1.1 billion at the two dates. It states cumulative unrealized losses, including impairments, of $0.3 billion at both dates. Remeasuring a privately held investee depends on an observable transaction.",
    "account": "long-term investments (non-marketable equity securities)",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "net unrealized gains on non-marketable securities were primarily attributable to an upward observable price adjustment of $0.6 billion related to a single investee",
    "paragraph_id": "0001571996-26-000046:notes:27",
    "explanation": false
  },
  {
    "id": "earnings_quality_interest_and_other_favorable_from_investment_gains",
    "what_changed": "The change in interest and other, net for the quarter and the six months is attributed mainly to gains in the strategic investments portfolio.",
    "account": "interest and other, net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The favorable changes were primarily attributable to gains recognized within our strategic investments portfolio.",
    "paragraph_id": "0001571996-26-000046:mdna:112",
    "explanation": false
  },
  {
    "id": "revenue_recognition_accounts_receivable_increase_from_revenue_growth",
    "what_changed": "The liquidity paragraph states accounts receivable, net at the two dates. It attributes the increase mainly to higher net revenue, largely from AI-optimized servers.",
    "account": "accounts receivable, net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Our accounts receivable, net was $22.9 billion and $17.6 billion as of July 31, 2026 and January 30, 2026, respectively. The increase in accounts receivable, net was primarily driven by an increase in net revenue",
    "paragraph_id": "0001571996-26-000046:mdna:144",
    "explanation": true
  },
  {
    "id": "estimates_and_discretion_trade_receivable_allowance_adequacy",
    "what_changed": "The same paragraph states the allowance for expected credit losses at the two dates and asserts the reserve is adequate. It gives no cause for the allowance amount. Elsewhere, at 0001571996-26-000046:mdna:195, MD&A says AI server purchases come from a small number of large customers and involve larger amounts of credit. Whether the allowance moves with receivables is for the numbers reader.",
    "account": "allowance for expected credit losses on accounts receivable",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "As of July 31, 2026 and January 30, 2026, the allowance for expected credit losses was $56 million and $77 million, respectively. Based on our assessment, we believe that we are adequately reserved for expected credit losses.",
    "paragraph_id": "0001571996-26-000046:mdna:144",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_financing_receivables_increase_from_isg_demand",
    "what_changed": "MD&A states financing receivables, net at the two dates and attributes the increase mainly to demand for ISG offerings.",
    "account": "financing receivables, net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "As of July 31, 2026 and January 30, 2026, our financing receivables, net were $20.4 billion and $14.3 billion, respectively. The increase in financing receivables, net was primarily attributable to increased demand for our ISG offerings.",
    "paragraph_id": "0001571996-26-000046:mdna:148",
    "explanation": true
  },
  {
    "id": "estimates_and_discretion_financing_charge_off_rate_and_credit_quality",
    "what_changed": "MD&A states principal charge-off rates for the second quarter and the first six months of fiscal 2027 and fiscal 2026. It says credit quality remains strong because the portfolio is mostly high-quality commercial accounts, and that the portfolio is adequately reserved. Supervisors may read this against the allowance rollforward table at 0001571996-26-000046:notes:38, which this reader does not compare.",
    "account": "allowance for financing receivable losses",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "The principal charge-off rate for our financing receivables portfolio was 0.5% and 0.1% for the second quarter of Fiscal 2027 and Fiscal 2026, respectively, and 0.4% and 0.2% for the first six months of Fiscal 2027 and Fiscal 2026, respectively. The credit quality of our financing receivables remains strong due to the mix of high-quality commercial accounts in our portfolio.",
    "paragraph_id": "0001571996-26-000046:mdna:148",
    "explanation": true
  },
  {
    "id": "liquidity_and_capital_dfs_originations_from_isg_demand",
    "what_changed": "MD&A states new financing originations of $7.5 billion and $2.4 billion for the second quarters of fiscal 2027 and fiscal 2026, and $10.3 billion and $4.0 billion for the first six months. It attributes the increase mainly to demand for ISG offerings. The same amounts appear in the financial services note at 0001571996-26-000046:notes:29.",
    "account": "financing receivables, net",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "The increase in our new financing originations was primarily attributable to increased demand for our ISG offerings.",
    "paragraph_id": "0001571996-26-000046:mdna:146",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_operating_cash_offset_by_financing_receivables",
    "what_changed": "The six-month explanation of operating cash flow cites net revenue growth, profitability and 'working capital dynamics', partly offset by higher financing receivables, all tied to ISG demand. The prior-year explanation is described as 'similar working capital dynamics'. The working capital components are not named.",
    "account": "cash flows from operating activities",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "partially offset by higher financing receivables, all of which factors were primarily affected by increased demand for our ISG offerings",
    "paragraph_id": "0001571996-26-000046:mdna:179",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_sales_type_lease_funding_in_operating_cash",
    "what_changed": "In the DFS cash flow paragraph, amounts are rolled forward. It says the initial funding of sales-type leases is reported in operating cash flow and the funding of operating leases in investing cash flow. It restates originations and states $20.4 billion of net financing receivables and $3.2 billion of equipment under operating leases, net. The sales-type lease revenue table at 0001571996-26-000046:notes:52 is for the numbers reader. So is the release's adjusted free cash flow, which adds back financing receivables.",
    "account": "cash flows from operating activities",
    "expected_direction": "down",
    "horizon": "next quarter",
    "quote": "For offerings that qualify as sales-type leases, the initial funding of financing receivables is reflected as an impact to cash flows from operations.",
    "paragraph_id": "0001571996-26-000046:mdna:182",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_cash_flat_as_debt_and_operations_fund_capital_return",
    "what_changed": "MD&A now says cash and cash equivalents were flat over the six months. Operating cash flow and net proceeds from new debt were largely offset by capital returned to shareholders and by capital expenditures.",
    "account": "cash and cash equivalents",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "cash and cash equivalents was flat as the cash flows from operating activities and net proceeds from the issuance of debt were largely offset by the return of capital to our shareholders and capital expenditures",
    "paragraph_id": "0001571996-26-000046:mdna:161",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_senior_notes_issuance_drives_debt_increase",
    "what_changed": "MD&A says total debt principal increased in the first six months, mainly because of new Senior Notes.",
    "account": "total debt",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "During the first six months of Fiscal 2027, the outstanding principal amount of our total debt increased $3.0 billion to $34.7 billion, driven primarily by an increase in net debt from the issuance of Senior Notes.",
    "paragraph_id": "0001571996-26-000046:mdna:168",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_new_senior_notes_tranches",
    "what_changed": "New bullet in the debt note: three new tranches of Senior Notes were issued, at 4.75% due July 2031, 5.00% due February 2034 and 5.25% due February 2037. Net proceeds are for general corporate purposes, which may include repaying debt. The list of Senior Notes offerings at 0001571996-26-000046:notes:106 now includes a June 16, 2026 offering of $3.0 billion. The Form 8-K list shows filings on June 12 and June 16, 2026 that fit this.",
    "account": "long-term debt",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "issuance of $1.0 billion principal amount of 4.75% Senior Notes due July 2031, $0.75 billion principal amount of 5.00% Senior Notes due February 2034, and $1.25 billion principal amount of 5.25% Senior Notes due February 2037",
    "paragraph_id": "0001571996-26-000046:notes:104",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_new_revolving_credit_facility_replaces_prior",
    "what_changed": "New paragraph. On June 10, 2026, Dell entered into a new senior unsecured revolving credit facility. It matures June 10, 2031 and has $6.0 billion of commitments. It replaced and terminated the 2021 facility, which the prior filing said matured November 1, 2027. The earlier description of a letter of credit sub-facility, a swing-line sub-facility and incremental commitments was removed. Nothing was borrowed under the facility at July 31, 2026. The Form 8-K list shows a June 10, 2026 filing with items 1.01, 1.02 and 2.03.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "On June 10, 2026, the Company entered into a new senior unsecured revolving credit facility",
    "paragraph_id": "0001571996-26-000046:notes:109",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_interest_expense_paragraph_added",
    "what_changed": "New paragraph in the debt note, listed as added in the note change history. It states interest expense on outstanding debt, which the filing says was $0.4 billion in both second quarters and $0.8 billion in both six-month periods. The expense is recorded in interest and other, net.",
    "account": "interest and other, net",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Total interest expense related to the Company’s outstanding debt was $0.4 billion for both the three months ended July 31, 2026 and August 1, 2025",
    "paragraph_id": "0001571996-26-000046:notes:118",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_dfs_asset_based_facility_tranches_extended",
    "what_changed": "The asset-based financing facility's tranche dates now read July 7, 2027 and July 7, 2028. The prior filing read July 7, 2026 and July 7, 2027. The capacity sentence reads $4.6 billion in both filings.",
    "account": "DFS debt",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "The asset-based financing facility consists of two tranches, with effective dates through July 7, 2027 and July 7, 2028, respectively.",
    "paragraph_id": "0001571996-26-000046:notes:68",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_dfs_securitization_fixed_rate_range",
    "what_changed": "The fixed interest rate range on DFS fixed-term securitization securities now reads 4.01% to 6.12% as of July 31, 2026. The prior filing read 4.01% to 6.75% as of May 1, 2026.",
    "account": "DFS debt",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "The interest rate on these securities is fixed and ranges from 4.01% to 6.12% per annum as of July 31, 2026",
    "paragraph_id": "0001571996-26-000046:notes:70",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_european_securitization_facility_capacity",
    "what_changed": "The European securitization facility's capacity now reads $922 million as of July 31, 2026. The prior filing read $938 million as of May 1, 2026. The facility is still effective through December 22, 2026, which falls within this fiscal year, and no renewal is stated. The unchanged European other-borrowings facility at 0001571996-26-000046:notes:78 is effective through December 14, 2026.",
    "account": "DFS debt",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "This facility is effective through December 22, 2026 and had a total debt capacity of $922 million as of July 31, 2026.",
    "paragraph_id": "0001571996-26-000046:notes:72",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_singapore_facilities_effective_dates",
    "what_changed": "The two Singapore facilities now read $257 million of capacity, effective through July 3, 2027 and July 12, 2027. The prior filing read $259 million, with one facility effective through July 12, 2026 and then extended after that quarter to July 12, 2027. The sentence about that later extension was removed.",
    "account": "DFS debt",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "The Company also has two unsecured Singapore facilities, which had a total debt capacity of $257 million as of July 31, 2026 and are effective through July 3, 2027 and July 12, 2027, respectively.",
    "paragraph_id": "0001571996-26-000046:notes:81",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_dfs_securitization_transfers_to_special_purpose_entities",
    "what_changed": "The note now states the lease and loan payments and equipment transferred by securitization to consolidated special purpose entities. Amounts are given for the second quarters and the first six months of fiscal 2027 and fiscal 2026, and the six-month amounts are $2.7 billion and $2.0 billion.",
    "account": "financing receivables, net (held by consolidated VIEs); DFS debt",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "Lease and loan payments and associated equipment transferred via securitization through SPEs were $1.4 billion and $0.8 billion for the three months ended July 31, 2026 and August 1, 2025, respectively",
    "paragraph_id": "0001571996-26-000046:notes:88",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_remaining_performance_obligation_estimate_factors",
    "what_changed": "The factors that can change remaining performance obligation estimates now include changes in contract price. The prior filing also listed 'periodic revalidation' and 'adjustments for revenue that have not materialized'; neither is listed now.",
    "account": "remaining performance obligations",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Remaining performance obligations estimates are subject to change and are affected by multiple factors, including terminations, changes in the scope or price of contracts, and adjustments for currency.",
    "paragraph_id": "0001571996-26-000046:notes:159",
    "explanation": false
  },
  {
    "id": "revenue_recognition_remaining_performance_obligations_and_timing",
    "what_changed": "Remaining performance obligations are now stated at about $132 billion as of July 31, 2026. About 77% is expected to be recognized in the next twelve months and 14% in the twelve months after. The prior filing stated about $97 billion as of May 1, 2026, with 80% and 10%. The sentence defining the measure was shortened. No comparison is made here.",
    "account": "remaining performance obligations; net revenue",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Revenue allocated to remaining performance obligations, which includes deferred revenue and unbilled amounts not yet recorded in deferred revenue, was approximately $132 billion as of July 31, 2026.",
    "paragraph_id": "0001571996-26-000046:notes:157",
    "explanation": false
  },
  {
    "id": "across_documents_ai_backlog_versus_remaining_performance_obligations",
    "what_changed": "The earnings release gives an AI server backlog figure at quarter end and does not define backlog. The revenue note gives total remaining performance obligations, which exclude cancelable contracts with no substantive termination penalty (0001571996-26-000046:notes:158). The two measures are defined differently, and reconciling them is the supervisor's task.",
    "account": "remaining performance obligations",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "exited the quarter with a record $95 billion backlog",
    "paragraph_id": "0001571996-26-000039:8k_2_02:12",
    "explanation": false
  },
  {
    "id": "results_against_expectations_ai_server_orders_record",
    "what_changed": "The earnings release states record AI server orders booked in the second quarter and record AI server revenue recognized.",
    "account": "net revenue, AI-optimized servers",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "we booked a record $60.9 billion in orders, recognized a record $16.4 billion in revenue",
    "paragraph_id": "0001571996-26-000039:8k_2_02:12",
    "explanation": false
  },
  {
    "id": "results_against_expectations_full_year_revenue_guidance_raised",
    "what_changed": "The release raises full-year fiscal 2027 revenue guidance. Its guidance table (0001571996-26-000039:8k_2_02:33) prints previous and updated figures for revenue, AI-optimized server revenue, and GAAP and non-GAAP diluted earnings per share. Its bullets give updated GAAP earnings per share of $24.37 and non-GAAP of $25.50.",
    "account": "net revenue",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "we’re raising our full-year FY27 revenue outlook by $25 billion to $192 billion, up nearly 70% year over year",
    "paragraph_id": "0001571996-26-000039:8k_2_02:13",
    "explanation": false
  },
  {
    "id": "results_against_expectations_third_quarter_guidance",
    "what_changed": "New guidance for the third quarter of fiscal 2027: revenue of $49.0 billion, printed as up 81% year over year; GAAP diluted earnings per share of $6.10; and non-GAAP diluted earnings per share of $6.50.",
    "account": "net revenue",
    "expected_direction": "up",
    "horizon": "next quarter",
    "quote": "| Revenue | $ | 49.0 |",
    "paragraph_id": "0001571996-26-000039:8k_2_02:31",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_record_quarterly_capital_return",
    "what_changed": "The release states a record $4.3 billion returned to shareholders in the second quarter through share repurchases and dividends.",
    "account": "treasury stock; cash and cash equivalents",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "Dell Technologies returned a record $4.3 billion to shareholders in the second quarter through share repurchases and dividends.",
    "paragraph_id": "0001571996-26-000039:8k_2_02:26",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_share_repurchases_first_six_months",
    "what_changed": "MD&A states that about 20 million Class C shares were repurchased for about $5.4 billion in the first six months of fiscal 2027. For the prior year it states about 30 million shares for about $2.9 billion.",
    "account": "treasury stock",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "During the first six months of Fiscal 2027, we repurchased approximately 20 million shares of Class C Common Stock for a total purchase price of approximately $5.4 billion.",
    "paragraph_id": "0001571996-26-000046:mdna:187",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_dividend_declared_after_quarter",
    "what_changed": "After quarter end, on September 1, 2026, the board declared a quarterly dividend of $0.63 per share. It is payable October 30 to holders of record on October 20.",
    "account": "retained earnings (dividends); cash and cash equivalents",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "on Sept. 1 the company’s board of directors declared a quarterly cash dividend of $0.63 per common share, which will be payable on Oct. 30 to shareholders of record as of Oct. 20",
    "paragraph_id": "0001571996-26-000039:8k_2_02:27",
    "explanation": false
  },
  {
    "id": "earnings_quality_non_gaap_tax_adjustment_estimate",
    "what_changed": "The guidance reconciliation footnote puts the fiscal 2027 aggregate adjustment between non-GAAP and GAAP income tax expense at about $0.3 billion. The adjustment includes discrete tax items, and non-GAAP tax uses a fixed estimated annual rate. The prior release is not in this input.",
    "account": "income tax expense",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "The fiscal 2027 aggregate adjustment to reconcile non-GAAP income tax expense to GAAP income tax expense is approximately $0.3 billion.",
    "paragraph_id": "0001571996-26-000039:8k_2_02:130",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_unrecognized_tax_benefits",
    "what_changed": "The tax note states net unrecognized tax benefits at the two dates, held in other non-current liabilities. It asserts that reserves are adequate, including for the IRS audits it describes. It gives no cause for the amounts.",
    "account": "other non-current liabilities (unrecognized tax benefits)",
    "expected_direction": "none",
    "horizon": "12 months",
    "quote": "Net unrecognized tax benefits were $1.2 billion and $1.1 billion as of July 31, 2026 and January 30, 2026, respectively",
    "paragraph_id": "0001571996-26-000046:notes:177",
    "explanation": false
  },
  {
    "id": "liquidity_and_capital_supply_chain_finance_confirmed_invoices",
    "what_changed": "The supply chain finance program note states the supplier invoices confirmed under the program and included in accounts payable at July 31, 2026 and January 30, 2026. The MD&A liquidity section also describes the program (0001571996-26-000046:mdna:183).",
    "account": "accounts payable",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "As of July 31, 2026 and January 30, 2026, the Company had $3.1 billion and $2.0 billion, respectively, included within accounts payable",
    "paragraph_id": "0001571996-26-000046:notes:233",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_voting_rights_refer_to_texas_law",
    "what_changed": "The voting rights paragraph is carried as changed; the prior wording is not in this input. It refers to Texas law for Class D voting. The conversion paragraphs (0001571996-26-000046:notes:185 through 0001571996-26-000046:notes:187) refer to the company's 'certificate of formation'. The Form 8-K list shows a July 1, 2026 filing with items 3.03, 5.07 and 8.01, and a July 6, 2026 filing with items 3.03 and 5.03. The notes here do not say the state of incorporation changed, and those 8-K bodies are not in this input. The supervisor should confirm.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "is not entitled to any vote on any matter except to the extent required by provisions of Texas law",
    "paragraph_id": "0001571996-26-000046:notes:184",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_class_b_to_class_c_conversions",
    "what_changed": "The notes state that about 8 million Class B shares were converted into Class C shares in the first six months of fiscal 2027. The Form 8-K list shows filings under item 3.02 on April 20, 2026 and June 17, 2026.",
    "account": "common stock",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "the Company issued approximately 8 million shares of Class C Common Stock to shareholders upon the conversion of the same number of shares of Class B Common Stock",
    "paragraph_id": "0001571996-26-000046:notes:186",
    "explanation": false
  },
  {
    "id": "related_parties_contingencies_and_subsequent_events_general_counsel_trading_plan_terminated",
    "what_changed": "New disclosure. On June 11, 2026, the General Counsel terminated a Rule 10b5-1 trading arrangement adopted March 10, 2026 to sell up to 45,000 Class C shares. No shares were sold under it.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "On June 11, 2026, Richard J. Rothberg, the Company’s General Counsel, terminated a trading arrangement",
    "paragraph_id": "0001571996-26-000046:notes:235",
    "explanation": false
  },
  {
    "id": "controls_audit_and_filings_new_enterprise_resource_planning_functions",
    "what_changed": "Item 4 says some functions of a new enterprise resource planning system went live during the quarter ended July 31, 2026, and more business processes will migrate later. It says internal control design has been modified and will continue to be modified. Disclosure controls are concluded effective. The prior wording is not in this input, so whether earlier phases were reported cannot be seen here.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "next quarter",
    "quote": "During the fiscal quarter ended July 31, 2026, we implemented certain functions of a new enterprise resource planning system, and we plan to migrate additional business processes in the future.",
    "paragraph_id": "0001571996-26-000046:item_4_controls:7",
    "explanation": false
  },
  {
    "id": "structure_and_disclosure_changes_environmental_credits_pronouncement",
    "what_changed": "Recently issued pronouncements now include FASB guidance from May 2026 on environmental credits and environmental credit obligations. It takes effect for fiscal years beginning after December 15, 2027, applies retrospectively, and is under evaluation. The paragraph is carried as changed; the prior wording is not in this input.",
    "account": "none",
    "expected_direction": "none",
    "horizon": "beyond 12 months",
    "quote": "In May 2026, the Financial Accounting Standards Board (“FASB”) issued guidance to improve the financial accounting disclosure of environmental credits and environmental credit obligations",
    "paragraph_id": "0001571996-26-000046:notes:6",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_core_debt_depends_on_dfs_allocation",
    "what_changed": "MD&A states core debt of $14.0 billion and $17.0 billion at the two dates. Core debt subtracts DFS related debt, which includes 'DFS allocated debt': management's allocation of other borrowings that it considers to fund DFS. The total debt paragraph (0001571996-26-000046:mdna:168) says total debt increased. How those two statements reconcile through the allocation is for the numbers reader; the allocation is shown in the table at 0001571996-26-000046:mdna:167.",
    "account": "total debt",
    "expected_direction": "none",
    "horizon": "this quarter",
    "quote": "We define core debt as the total principal amount of our debt, less DFS related debt and other debt.",
    "paragraph_id": "0001571996-26-000046:mdna:169",
    "explanation": false
  },
  {
    "id": "estimates_and_discretion_ai_customer_credit_concentration",
    "what_changed": "The counterparty credit paragraph is carried as changed; the prior wording is not in this input. It says most AI-optimized server revenue so far has come from a relatively small number of large customers and cloud service providers. It says these purchases involve larger amounts of credit and could affect credit risk in trade and financing receivables.",
    "account": "accounts receivable, net; financing receivables, net",
    "expected_direction": "up",
    "horizon": "12 months",
    "quote": "Such purchases generally involve larger amounts of credit, and could impact our overall credit risk in trade and financing receivables.",
    "paragraph_id": "0001571996-26-000046:mdna:195",
    "explanation": false
  },
  {
    "id": "results_against_expectations_storage_growth_dell_ip_demand_and_pricing",
    "what_changed": "The rise in storage revenue for the quarter and the six months is attributed mainly to demand for Dell-IP storage offerings and to disciplined pricing.",
    "account": "net revenue, storage",
    "expected_direction": "up",
    "horizon": "this quarter",
    "quote": "primarily due to growth in demand for our Dell-IP storage offerings and disciplined pricing",
    "paragraph_id": "0001571996-26-000046:mdna:127",
    "explanation": false
  }
]
```

## Paragraphs carried as text that are not items

Each line gives the paragraph id and the reason. Lines marked `insufficient` were carried as changed, but the prior wording is not in this input and no period-specific text shows what changed.

### Notes

- 0001571996-26-000046:notes:1 — date rolled forward
- 0001571996-26-000046:notes:2 — date rolled forward
- 0001571996-26-000046:notes:5 — heading
- 0001571996-26-000046:notes:7 — insufficient: pronouncement issued September 2025, still under evaluation; prior wording not in input
- 0001571996-26-000046:notes:8 — insufficient: says adoption will increase disclosures; prior wording not in input
- 0001571996-26-000046:notes:10 — table; amounts only
- 0001571996-26-000046:notes:12 — date rolled forward
- 0001571996-26-000046:notes:18 — table; amounts only
- 0001571996-26-000046:notes:23 — table; amounts only
- 0001571996-26-000046:notes:25 — table; amounts only (the gain behind the notes:27 item)
- 0001571996-26-000046:notes:28 — unchanged per note change history
- 0001571996-26-000046:notes:29 — originations amounts; same amounts are in the mdna:146 item
- 0001571996-26-000046:notes:30 — unchanged per note change history
- 0001571996-26-000046:notes:31 — unchanged per note change history
- 0001571996-26-000046:notes:32 — unchanged per note change history
- 0001571996-26-000046:notes:33 — heading
- 0001571996-26-000046:notes:34 — table lead-in; unchanged per note change history
- 0001571996-26-000046:notes:35 — table; amounts only
- 0001571996-26-000046:notes:36 — table footnote; unchanged per note change history
- 0001571996-26-000046:notes:37 — table lead-in
- 0001571996-26-000046:notes:38 — table; amounts only (allowance rollforward, for the numbers reader; read with the mdna:148 credit quality item)
- 0001571996-26-000046:notes:39 — unchanged per note change history
- 0001571996-26-000046:notes:40 — heading
- 0001571996-26-000046:notes:41 — table lead-in
- 0001571996-26-000046:notes:42 — table; amounts only
- 0001571996-26-000046:notes:43 — unchanged per note change history
- 0001571996-26-000046:notes:44 — unchanged per note change history
- 0001571996-26-000046:notes:45 — heading
- 0001571996-26-000046:notes:46 — table lead-in
- 0001571996-26-000046:notes:47 — table; amounts only
- 0001571996-26-000046:notes:48 — table; year-end comparative, unchanged per note change history
- 0001571996-26-000046:notes:49 — unchanged per note change history
- 0001571996-26-000046:notes:50 — heading
- 0001571996-26-000046:notes:51 — table lead-in
- 0001571996-26-000046:notes:52 — table; amounts only (sales-type lease revenue, for the numbers reader)
- 0001571996-26-000046:notes:53 — table lead-in
- 0001571996-26-000046:notes:54 — table; amounts only (the history pairs it with a different prior table; this is a matching artifact)
- 0001571996-26-000046:notes:55 — heading
- 0001571996-26-000046:notes:56 — unchanged per note change history
- 0001571996-26-000046:notes:57 — table lead-in
- 0001571996-26-000046:notes:58 — table; amounts only (row label wording only)
- 0001571996-26-000046:notes:59 — table lead-in
- 0001571996-26-000046:notes:60 — table; amounts only
- 0001571996-26-000046:notes:61 — table lead-in
- 0001571996-26-000046:notes:62 — table; amounts only (listed as added, but the prior filing had a matching operating lease table under a different pairing)
- 0001571996-26-000046:notes:63 — heading
- 0001571996-26-000046:notes:64 — unchanged per note change history
- 0001571996-26-000046:notes:65 — unchanged per note change history
- 0001571996-26-000046:notes:66 — table; amounts only
- 0001571996-26-000046:notes:67 — heading
- 0001571996-26-000046:notes:69 — date rolled forward; criteria still met
- 0001571996-26-000046:notes:71 — heading
- 0001571996-26-000046:notes:73 — date rolled forward; criteria still met
- 0001571996-26-000046:notes:74 — unchanged per note change history
- 0001571996-26-000046:notes:75 — unchanged per note change history
- 0001571996-26-000046:notes:76 — date rolled forward
- 0001571996-26-000046:notes:77 — unchanged per note change history
- 0001571996-26-000046:notes:78 — unchanged per note change history
- 0001571996-26-000046:notes:79 — unchanged per note change history
- 0001571996-26-000046:notes:80 — unchanged per note change history
- 0001571996-26-000046:notes:82 — wording only: sentence order and rate precision
- 0001571996-26-000046:notes:83 — heading
- 0001571996-26-000046:notes:84 — unchanged per note change history
- 0001571996-26-000046:notes:85 — unchanged per note change history
- 0001571996-26-000046:notes:86 — table lead-in
- 0001571996-26-000046:notes:87 — table; amounts only
- 0001571996-26-000046:notes:89 — heading
- 0001571996-26-000046:notes:90 — period rolled forward; amounts still immaterial
- 0001571996-26-000046:notes:91 — table lead-in
- 0001571996-26-000046:notes:92 — table; amounts only (two carrying-value rows merged under one caption)
- 0001571996-26-000046:notes:93 — date rolled forward
- 0001571996-26-000046:notes:95 — period rolled forward; still immaterial
- 0001571996-26-000046:notes:97 — table; amounts only
- 0001571996-26-000046:notes:98 — period rolled forward; still immaterial
- 0001571996-26-000046:notes:100 — table; amounts only
- 0001571996-26-000046:notes:101 — heading and table lead-in
- 0001571996-26-000046:notes:102 — lead-in to bullets; content is in the notes:104 item
- 0001571996-26-000046:notes:103 — reworded; repayment already disclosed in the prior quarter
- 0001571996-26-000046:notes:105 — heading
- 0001571996-26-000046:notes:106 — adds the June 16, 2026 offering; covered by the notes:104 item
- 0001571996-26-000046:notes:107 — unchanged per note change history
- 0001571996-26-000046:notes:108 — unchanged per note change history
- 0001571996-26-000046:notes:110 — old maturity sentence removed; superseded by the notes:109 item
- 0001571996-26-000046:notes:111 — date rolled forward
- 0001571996-26-000046:notes:112 — date rolled forward
- 0001571996-26-000046:notes:113 — unchanged per note change history
- 0001571996-26-000046:notes:114 — date rolled forward; still in covenant compliance
- 0001571996-26-000046:notes:115 — heading
- 0001571996-26-000046:notes:116 — date rolled forward
- 0001571996-26-000046:notes:117 — table; amounts only
- 0001571996-26-000046:notes:123 — period rolled forward
- 0001571996-26-000046:notes:132 — table; amounts only
- 0001571996-26-000046:notes:134 — table; amounts only
- 0001571996-26-000046:notes:135 — period rolled forward; still immaterial
- 0001571996-26-000046:notes:137 — table; amounts only
- 0001571996-26-000046:notes:139 — table; amounts only
- 0001571996-26-000046:notes:141 — insufficient: cross-reference only, likely note renumbering; prior wording not in input
- 0001571996-26-000046:notes:143 — table; amounts only
- 0001571996-26-000046:notes:146 — table; amounts only
- 0001571996-26-000046:notes:147 — period rolled forward; no impairment
- 0001571996-26-000046:notes:149 — table; amounts only
- 0001571996-26-000046:notes:152 — period rolled forward; no interim impairment test
- 0001571996-26-000046:notes:155 — table; amounts only
- 0001571996-26-000046:notes:158 — wording only: rewrite of the removed exclusion paragraph, same content
- 0001571996-26-000046:notes:160 — heading
- 0001571996-26-000046:notes:162 — heading of the new guarantee section; content is in the notes:163, notes:164 and notes:165 items
- 0001571996-26-000046:notes:166 — heading
- 0001571996-26-000046:notes:167 — unchanged per note change history
- 0001571996-26-000046:notes:168 — unchanged per note change history
- 0001571996-26-000046:notes:169 — wording only: 'Employment' corrected to 'Employee'
- 0001571996-26-000046:notes:170 — date rolled forward
- 0001571996-26-000046:notes:171 — heading
- 0001571996-26-000046:notes:172 — unchanged per note change history
- 0001571996-26-000046:notes:173 — date rolled forward
- 0001571996-26-000046:notes:174 — amounts rolled forward; standard tax rate attribution
- 0001571996-26-000046:notes:178 — heading and table lead-in
- 0001571996-26-000046:notes:179 — table; amounts only
- 0001571996-26-000046:notes:181 — date rolled forward
- 0001571996-26-000046:notes:185 — 'certificate of formation' wording; covered by the notes:184 item
- 0001571996-26-000046:notes:187 — prior-year conversion fact; 'certificate of formation' wording covered by the notes:184 item
- 0001571996-26-000046:notes:191 — table; amounts only
- 0001571996-26-000046:notes:192 — period rolled forward
- 0001571996-26-000046:notes:194 — repeats the February 26, 2026 authorization; no new authorization
- 0001571996-26-000046:notes:195 — same repurchase facts as the mdna:187 item
- 0001571996-26-000046:notes:198 — table; amounts only
- 0001571996-26-000046:notes:200 — table; amounts only
- 0001571996-26-000046:notes:207 — table; amounts only
- 0001571996-26-000046:notes:215 — table; amounts only
- 0001571996-26-000046:notes:217 — table; amounts only
- 0001571996-26-000046:notes:219 — table; amounts only (inventory components, for the numbers reader)
- 0001571996-26-000046:notes:223 — table; amounts only (warranty rollforward, for the numbers reader)
- 0001571996-26-000046:notes:229 — table; amounts only
- 0001571996-26-000046:notes:231 — table; amounts only
- 0001571996-26-000046:notes:234 — date rolled forward

### MD&A

- 0001571996-26-000046:mdna:17 — insufficient: cross-reference only; prior wording not in input
- 0001571996-26-000046:mdna:18 — insufficient: description of offerings; prior wording not in input
- 0001571996-26-000046:mdna:20 — period rolled forward; only the tone word 'exceptional' differs
- 0001571996-26-000046:mdna:26 — page number
- 0001571996-26-000046:mdna:38 — insufficient: recurring revenue definition carried as changed; prior definition not in input, so it cannot be seen whether the definition changed
- 0001571996-26-000046:mdna:40 — amounts rolled forward; no attribution
- 0001571996-26-000046:mdna:42 — page number
- 0001571996-26-000046:mdna:46 — insufficient: non-GAAP definitions carried as changed; prior wording not in input
- 0001571996-26-000046:mdna:51 — page number
- 0001571996-26-000046:mdna:56 — table; amounts only
- 0001571996-26-000046:mdna:58 — table; amounts only
- 0001571996-26-000046:mdna:63 — table; amounts only
- 0001571996-26-000046:mdna:71 — table; amounts only
- 0001571996-26-000046:mdna:73 — rounding footnote
- 0001571996-26-000046:mdna:74 — page number
- 0001571996-26-000046:mdna:78 — amounts with standard segment attribution; repeated word for word at mdna:109
- 0001571996-26-000046:mdna:79 — pricing and operating-leverage attribution covered by the mdna:90 item; repeated word for word at mdna:110
- 0001571996-26-000046:mdna:80 — same text as the mdna:179 item
- 0001571996-26-000046:mdna:83 — repeats the first sentence of mdna:77
- 0001571996-26-000046:mdna:84 — amounts; attribution repeats mdna:77
- 0001571996-26-000046:mdna:87 — geographic restatement; period rolled forward
- 0001571996-26-000046:mdna:89 — amounts; standard segment attribution
- 0001571996-26-000046:mdna:91 — amounts; standard segment attribution
- 0001571996-26-000046:mdna:92 — product-level repeat of the pricing and mix attribution in the mdna:90 item
- 0001571996-26-000046:mdna:93 — amounts only
- 0001571996-26-000046:mdna:97 — period rolled forward; same vendor rebate assertion
- 0001571996-26-000046:mdna:100 — table; amounts only
- 0001571996-26-000046:mdna:101 — separator
- 0001571996-26-000046:mdna:102 — rounding footnote
- 0001571996-26-000046:mdna:103 — amounts only
- 0001571996-26-000046:mdna:105 — same attribution as the mdna:104 item
- 0001571996-26-000046:mdna:106 — same attribution as the mdna:104 item
- 0001571996-26-000046:mdna:109 — word-for-word repeat of mdna:78
- 0001571996-26-000046:mdna:110 — word-for-word repeat of mdna:79
- 0001571996-26-000046:mdna:114 — amounts rolled forward (tax rates)
- 0001571996-26-000046:mdna:117 — amounts; standard attribution
- 0001571996-26-000046:mdna:120 — insufficient: cross-reference only; prior wording not in input
- 0001571996-26-000046:mdna:123 — table; amounts only
- 0001571996-26-000046:mdna:124 — amounts; attribution repeats mdna:77
- 0001571996-26-000046:mdna:128 — geographic restatement
- 0001571996-26-000046:mdna:129 — segment-level repeat of the pricing attribution in the mdna:90 item
- 0001571996-26-000046:mdna:130 — segment-level repeat of the mix attribution in the mdna:90 item
- 0001571996-26-000046:mdna:134 — table; amounts only
- 0001571996-26-000046:mdna:135 — amounts; attribution covered by the mdna:136 and mdna:137 items
- 0001571996-26-000046:mdna:138 — attribution folded into the mdna:136 and mdna:137 items
- 0001571996-26-000046:mdna:139 — geographic restatement
- 0001571996-26-000046:mdna:140 — segment-level repeat of the pricing attribution in the mdna:90 item
- 0001571996-26-000046:mdna:141 — page number
- 0001571996-26-000046:mdna:149 — amounts rolled forward; same no-expected-loss assertion
- 0001571996-26-000046:mdna:150 — amounts rolled forward; same no-impairment assertion
- 0001571996-26-000046:mdna:152 — page number
- 0001571996-26-000046:mdna:157 — insufficient: liquidity sufficiency statement; prior wording not in input
- 0001571996-26-000046:mdna:158 — insufficient: capital allocation statement; prior wording not in input
- 0001571996-26-000046:mdna:160 — table; amounts only
- 0001571996-26-000046:mdna:162 — date rolled forward; facility covered by the notes:109 item
- 0001571996-26-000046:mdna:163 — date rolled forward
- 0001571996-26-000046:mdna:164 — insufficient: statement on use of borrowings; prior wording not in input
- 0001571996-26-000046:mdna:167 — table; amounts only (core and DFS allocated debt, for the numbers reader)
- 0001571996-26-000046:mdna:173 — table; amounts only
- 0001571996-26-000046:mdna:174 — insufficient: debt-service statement; prior wording not in input
- 0001571996-26-000046:mdna:178 — table; amounts only
- 0001571996-26-000046:mdna:180 — amounts rolled forward; capital expenditure attribution
- 0001571996-26-000046:mdna:181 — amounts; attribution covered by the mdna:161 item
- 0001571996-26-000046:mdna:183 — insufficient: description of the supply chain finance program carried as changed; prior wording not in input; amounts are in the notes:233 item
- 0001571996-26-000046:mdna:185 — amounts rolled forward; standard list of factors
- 0001571996-26-000046:mdna:188 — amounts rolled forward
- 0001571996-26-000046:mdna:198 — page number
- 0001571996-26-000046:mdna:203 — table; amounts only
- 0001571996-26-000046:mdna:204 — separator
- 0001571996-26-000046:mdna:205 — amounts rolled forward; obligor group footnote
- 0001571996-26-000046:mdna:207 — table; amounts only

### Item 4

- 0001571996-26-000046:item_4_controls:1 — heading
- 0001571996-26-000046:item_4_controls:2 — standard reference to the certifications
- 0001571996-26-000046:item_4_controls:3 — heading
- 0001571996-26-000046:item_4_controls:4 — standard definition
- 0001571996-26-000046:item_4_controls:5 — date rolled forward; controls still concluded effective
- 0001571996-26-000046:item_4_controls:6 — heading
- 0001571996-26-000046:item_4_controls:8 — date rolled forward
- 0001571996-26-000046:item_4_controls:9 — page number

### Earnings release (Form 8-K filed September 1, 2026)

- 0001571996-26-000039:8k_2_02:1 — exhibit file header
- 0001571996-26-000039:8k_2_02:2 — document label
- 0001571996-26-000039:8k_2_02:3 — exhibit label
- 0001571996-26-000039:8k_2_02:4 — release headline
- 0001571996-26-000039:8k_2_02:5 — release lead; guidance covered by the guidance items
- 0001571996-26-000039:8k_2_02:6 — heading
- 0001571996-26-000039:8k_2_02:7 — results amounts, for the numbers reader
- 0001571996-26-000039:8k_2_02:8 — results amounts, for the numbers reader
- 0001571996-26-000039:8k_2_02:9 — results amounts, for the numbers reader
- 0001571996-26-000039:8k_2_02:10 — full-year revenue guidance bullet; covered by the 8k_2_02:13 item
- 0001571996-26-000039:8k_2_02:11 — full-year earnings per share guidance bullet; covered by the 8k_2_02:13 item
- 0001571996-26-000039:8k_2_02:14 — heading
- 0001571996-26-000039:8k_2_02:15 — segment results amounts
- 0001571996-26-000039:8k_2_02:16 — segment results amounts
- 0001571996-26-000039:8k_2_02:17 — segment results amounts
- 0001571996-26-000039:8k_2_02:18 — segment results amounts
- 0001571996-26-000039:8k_2_02:19 — segment results amounts
- 0001571996-26-000039:8k_2_02:20 — heading
- 0001571996-26-000039:8k_2_02:21 — segment results amounts
- 0001571996-26-000039:8k_2_02:22 — segment results amounts
- 0001571996-26-000039:8k_2_02:23 — segment results amounts
- 0001571996-26-000039:8k_2_02:24 — segment results amounts
- 0001571996-26-000039:8k_2_02:25 — heading
- 0001571996-26-000039:8k_2_02:28 — heading
- 0001571996-26-000039:8k_2_02:29 — units caption
- 0001571996-26-000039:8k_2_02:30 — heading
- 0001571996-26-000039:8k_2_02:32 — heading
- 0001571996-26-000039:8k_2_02:33 — guidance table of previous and updated amounts; covered by the 8k_2_02:13 item
- 0001571996-26-000039:8k_2_02:34 — heading
- 0001571996-26-000039:8k_2_02:35 — results table
- 0001571996-26-000039:8k_2_02:36 — non-GAAP reference note
- 0001571996-26-000039:8k_2_02:37 — heading
- 0001571996-26-000039:8k_2_02:38 — segment table
- 0001571996-26-000039:8k_2_02:39 — page number
- 0001571996-26-000039:8k_2_02:40 — heading
- 0001571996-26-000039:8k_2_02:41 — conference call logistics
- 0001571996-26-000039:8k_2_02:42 — conference call logistics
- 0001571996-26-000039:8k_2_02:43 — heading
- 0001571996-26-000039:8k_2_02:44 — company description boilerplate
- 0001571996-26-000039:8k_2_02:45 — company description boilerplate
- 0001571996-26-000039:8k_2_02:46 — company description boilerplate
- 0001571996-26-000039:8k_2_02:47 — heading
- 0001571996-26-000039:8k_2_02:48 — contact
- 0001571996-26-000039:8k_2_02:49 — contact
- 0001571996-26-000039:8k_2_02:50 — separator
- 0001571996-26-000039:8k_2_02:51 — copyright
- 0001571996-26-000039:8k_2_02:52 — heading
- 0001571996-26-000039:8k_2_02:53 — non-GAAP boilerplate
- 0001571996-26-000039:8k_2_02:54 — heading
- 0001571996-26-000039:8k_2_02:55 — forward-looking scope statement
- 0001571996-26-000039:8k_2_02:56 — standard risk list; prior release not in input
- 0001571996-26-000039:8k_2_02:57 — standard risk list, continued
- 0001571996-26-000039:8k_2_02:58 — standard cautionary statement
- 0001571996-26-000039:8k_2_02:59 — page number
- 0001571996-26-000039:8k_2_02:60 — heading
- 0001571996-26-000039:8k_2_02:61 — heading
- 0001571996-26-000039:8k_2_02:62 — units caption
- 0001571996-26-000039:8k_2_02:63 — income statement table
- 0001571996-26-000039:8k_2_02:64 — rounding note
- 0001571996-26-000039:8k_2_02:65 — page number
- 0001571996-26-000039:8k_2_02:66 — heading
- 0001571996-26-000039:8k_2_02:67 — heading
- 0001571996-26-000039:8k_2_02:68 — units caption
- 0001571996-26-000039:8k_2_02:69 — balance sheet table, for the numbers reader
- 0001571996-26-000039:8k_2_02:70 — page number
- 0001571996-26-000039:8k_2_02:71 — heading
- 0001571996-26-000039:8k_2_02:72 — heading
- 0001571996-26-000039:8k_2_02:73 — units caption
- 0001571996-26-000039:8k_2_02:74 — cash flow table, for the numbers reader
- 0001571996-26-000039:8k_2_02:75 — heading
- 0001571996-26-000039:8k_2_02:76 — heading
- 0001571996-26-000039:8k_2_02:77 — units caption
- 0001571996-26-000039:8k_2_02:78 — segment table
- 0001571996-26-000039:8k_2_02:79 — rounding note
- 0001571996-26-000039:8k_2_02:80 — page number
- 0001571996-26-000039:8k_2_02:81 — heading
- 0001571996-26-000039:8k_2_02:82 — heading
- 0001571996-26-000039:8k_2_02:83 — units caption
- 0001571996-26-000039:8k_2_02:84 — segment reconciliation table
- 0001571996-26-000039:8k_2_02:85 — separator
- 0001571996-26-000039:8k_2_02:86 — standard segment footnote
- 0001571996-26-000039:8k_2_02:87 — standard segment footnote
- 0001571996-26-000039:8k_2_02:88 — standard segment footnote
- 0001571996-26-000039:8k_2_02:89 — standard segment footnote
- 0001571996-26-000039:8k_2_02:90 — standard segment footnote
- 0001571996-26-000039:8k_2_02:91 — standard segment footnote
- 0001571996-26-000039:8k_2_02:92 — heading
- 0001571996-26-000039:8k_2_02:93 — non-GAAP boilerplate
- 0001571996-26-000039:8k_2_02:94 — page number
- 0001571996-26-000039:8k_2_02:95 — heading
- 0001571996-26-000039:8k_2_02:96 — heading
- 0001571996-26-000039:8k_2_02:97 — units caption
- 0001571996-26-000039:8k_2_02:98 — non-GAAP table
- 0001571996-26-000039:8k_2_02:99 — rounding note
- 0001571996-26-000039:8k_2_02:100 — heading
- 0001571996-26-000039:8k_2_02:101 — heading
- 0001571996-26-000039:8k_2_02:102 — units caption
- 0001571996-26-000039:8k_2_02:103 — reconciliation table
- 0001571996-26-000039:8k_2_02:104 — separator
- 0001571996-26-000039:8k_2_02:105 — standard tax footnote
- 0001571996-26-000039:8k_2_02:106 — page number
- 0001571996-26-000039:8k_2_02:107 — heading
- 0001571996-26-000039:8k_2_02:108 — heading
- 0001571996-26-000039:8k_2_02:109 — units caption
- 0001571996-26-000039:8k_2_02:110 — reconciliation table
- 0001571996-26-000039:8k_2_02:111 — separator
- 0001571996-26-000039:8k_2_02:112 — standard tax footnote
- 0001571996-26-000039:8k_2_02:113 — heading
- 0001571996-26-000039:8k_2_02:114 — heading
- 0001571996-26-000039:8k_2_02:115 — units caption
- 0001571996-26-000039:8k_2_02:116 — free cash flow table, for the numbers reader
- 0001571996-26-000039:8k_2_02:117 — separator
- 0001571996-26-000039:8k_2_02:118 — standard free cash flow footnote
- 0001571996-26-000039:8k_2_02:119 — standard free cash flow footnote (financing receivables add-back definition)
- 0001571996-26-000039:8k_2_02:120 — standard free cash flow footnote
- 0001571996-26-000039:8k_2_02:121 — page number
- 0001571996-26-000039:8k_2_02:122 — heading
- 0001571996-26-000039:8k_2_02:123 — heading
- 0001571996-26-000039:8k_2_02:124 — units caption
- 0001571996-26-000039:8k_2_02:125 — guidance reconciliation table
- 0001571996-26-000039:8k_2_02:126 — separator
- 0001571996-26-000039:8k_2_02:127 — standard amortization estimate footnote
- 0001571996-26-000039:8k_2_02:128 — standard footnote excluding severance from guidance; prior release not in input
- 0001571996-26-000039:8k_2_02:129 — standard footnote excluding fair value adjustments
- 0001571996-26-000039:8k_2_02:131 — page number

## Insufficient

These paragraphs were carried as changed, but the change cannot be seen from this input: 0001571996-26-000046:notes:7, 0001571996-26-000046:notes:8, 0001571996-26-000046:notes:141, 0001571996-26-000046:mdna:17, 0001571996-26-000046:mdna:18, 0001571996-26-000046:mdna:38, 0001571996-26-000046:mdna:46, 0001571996-26-000046:mdna:120, 0001571996-26-000046:mdna:157, 0001571996-26-000046:mdna:158, 0001571996-26-000046:mdna:164, 0001571996-26-000046:mdna:174, 0001571996-26-000046:mdna:183.
