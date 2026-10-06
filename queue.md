# Queue

The live work list. One line per item:

`[ ] what · eval command that must pass · depends on`

The nightly worker takes the first unchecked item whose dependencies are done, runs
`/goal <its eval command> exits 0 and the output is printed; no test or grader changed`,
and opens a pull request. Done items move to the bottom with their pull request
number. Claude may add items at the end; only the owner deletes or reorders them.
An item with no eval command is not an item: it goes to `docs/needs_judgment.md`.

`make eval` is the owner's grader over every run; `make eval-quick` grades the runs a
branch changed. A run item is done when its run directory is published and
`.venv/bin/python -m evals --runs <that directory>` exits 0.

## Open

[ ] DCF sanity: a free-cash-flow-yield cross-check, a WACC components table, and reverse-DCF growth beside three- and five-year revenue history, in `calculator.json` and the memo, each with a hand-worked test · `.venv/bin/python -m pytest tests/test_calculator.py tests/test_analysis_check.py -q -k "free_cash_flow_yield or wacc_components or growth_beside_history"` · none

[ ] the comparers become Python: `src/market_labels.py` labels each item priced_in, not_priced or opposite_direction from the sign of the abnormal return in each reaction window against the item's expected direction, plus short interest above its two-year median; `notes-vs-market` and `numbers-vs-market` move to `archive/agents/` · `.venv/bin/python -m pytest tests/test_market_labels.py tests/test_agent_inputs.py -q` · none

[ ] new Fable runs for AAPL, GNRC and LFUS, each in `runs/<ticker>/<accession>-rerun-<date>/` · `.venv/bin/python -m evals --runs runs/AAPL runs/GNRC runs/LFUS` · items one to three

[ ] the nightly crew: collects newest first; writes its ledger line to main through an auto-merging pull request instead of a `nightly/*` branch; reads the `TIINGO_TOKEN` secret; and `lessons.md` records why the 2006–2011 filings answered 404 · `.venv/bin/python -m pytest tests/test_nightly.py tests/test_collect_history.py -q` · none

[ ] NVDA's 10-Q filed 2026-08-26 on Fable · `.venv/bin/python -m evals --runs runs/NVDA` · item one

[ ] QCOM's 10-Q filed 2026-07-29 on Fable · `.venv/bin/python -m evals --runs runs/QCOM` · item one

[ ] ESE's 10-Q filed 2026-08-10 on Fable · `.venv/bin/python -m evals --runs runs/ESE` · item one

[ ] TTMI's 10-Q filed 2026-08-05 on Fable · `.venv/bin/python -m evals --runs runs/TTMI` · item one

[ ] `data/notes-and-calendar`: merge the code (`src/event_calendar.py`, `src/fsn.py` and their tests), download nothing; the bulk-data location is a row in `docs/needs_judgment.md` · `.venv/bin/python -m pytest tests/test_event_calendar.py tests/test_fsn.py -q` · none

[ ] golden consistency runs: three runs of each approved golden case · `.venv/bin/python -m evals.capability.consistency` · the owner approving at least one case in `evals/golden/cases/`

[ ] new runs for the eight filings published on 2026-09-29 (AAPL, CARR, CIEN, CSCO, GNRC, LFUS, PANW, STX), each as a rerun directory · `.venv/bin/python -m evals --runs runs` · items one to three

[ ] the manifest records the triggering filing's EDGAR acceptance stamp, Eastern, no Z: the fetch projects `acceptanceDateTime` onto the submissions rows and the manifest document rows (the two field tuples in `src/fetch_fixtures.py` and `submissions_record`), `src/assemble_bundle.py` writes it beside `filing_date`, and the hand-written `acceptance_datetime` on NVDA's 10-Q row in `tests/fixtures/NVDA/submissions.json` is then the fetcher's · eval: `python -m evals --runs <run>` passes nothing_after_cutoff on a run with a market table · depends on: nothing

[ ] the SessionStart hook runs `sh tools/session_start_lessons.sh` in place of `cat lessons.md`: a pull request of that one line in `.claude/settings.json`, a guarded path, merged with the owner's label `owner-approved-eval` · eval: `.venv/bin/python -m pytest tests/test_session_start_lessons.py tests/test_guards.py -q` passes and the guard job is green on the labeled run · depends on: the owner's label

[ ] the memo names a cost-of-debt fallback where calculator.json labels one (`pre_tax_cost_of_debt.fallback`), in the finance frame's valuation section · `.venv/bin/python -m pytest tests/test_analysis_check.py -q -k cost_of_debt_fallback` · items one and three

## Done

[x] valuation failures: AAPL's pre-tax cost of debt falls back to interest paid (`InterestPaidNet`) over average debt, then to the risk-free rate plus one point, labelled `fallback`; GNRC's and LFUS's scenarios stop being dropped for a bare year in a driver's reason (their `assumptions.json` `dropped_items`: "a number written in the analyst's own words" on "the second half of 2026", "through 2027"), which is the analysis gate's year rule, not a field mismatch · `.venv/bin/python -m pytest tests/test_calculator.py tests/test_analysis_check.py -q -k "interest_paid or risk_free_fallback or bare_year"` · none · PR: this one
