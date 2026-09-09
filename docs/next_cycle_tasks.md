# Next cycle tasks

This replaces the work ledger. Git and pull requests carry the state; this file
carries the list.

One line per item:

`[ ] title · builds · judge · expected value from · PR`

- **judge** is the command that decides pass or fail.
- **expected value from** is where the judge's numbers came from. It must name
  a source outside the code being built: the filing, the companyfacts JSON, a
  hand computation written into the test, or a value planted on purpose. If the
  honest answer is "a run of the thing this judges", the item is not ready.
- An item with no judge is **needs judgment**. It is never launched. The owner
  reads all of them in one sitting at the next rules version.

Build each item with the `build-item` skill, and brief every agent with the
`dispatch` skill. One worktree, one branch, one pull request per item, auto-merge
on the moment it opens.

The parsers on the git branch `harness/cycle-020` — the numeric extractor, the
note extractor, the MD&A and controls splitters, the 8-K parser, the paragraph
diff, the note history, the trend table, the bundle assembler, the cutoff guard
and the extraction checks — land through their own pull request. Several items
below build on them and assume that has merged.

**They do not arrive judged.** Their fixtures are the ones `lessons.md` records
as self-certified: the expected values were produced by running the code they
judge. Merging that branch imports the parsers and the hole at the same time, so
the first item below re-judges them before anything is built on top. Nothing
lands through its own pull request and thereby escapes the rule this whole file
exists to enforce.

---

## Ready to build

[ ] write the plain-name check · `src/plain_name_check.py` and the post-write hook that calls it · `.venv/bin/python -m pytest tests/test_plain_name_check.py -q` · a letter-number code planted in a fixture file by the test itself, and a filter output that is greped rather than a filter that is inspected — a no-op regular expression fails quietly. It is written rather than ported: the display-name filter lives only inside the old harness, not on this branch and not on the parser branch · PR: #21

[ ] re-judge the parsers that arrive from the parser branch · no new code — a replacement expected-value file per company, and the deletion of every expected value that came from a parser run · `.venv/bin/python -m pytest tests -q` against the replaced fixtures · companyfacts for every numeric expectation, and the filing itself, read by eye, for every section boundary and paragraph count; each replaced value carries a one-line note naming where it came from. Do this before any item below builds on those parsers · PR:

[ ] companyfacts fetcher · `src/fetch_companyfacts.py` and one `companyfacts.json` fixture per company, with its sha256 in the manifest · `python3.12 -m pytest tests/test_fetch_companyfacts.py -q` · every `us-gaap` numeric fact in the committed XBRL instance, looked up in companyfacts and matched by value, with every difference listed rather than tolerated · PR:

[ ] trend table on companyfacts · `src/trends.py` reading companyfacts instead of a single instance · `python3.12 -m pytest tests/test_trends.py -q` · two claims, because "every ratio for twelve companies over 8 quarters and 5 years" is thousands of values and would become a generator sharing code with the thing it judges: (a) for three named companies and two named periods, every ratio computed by hand and written out term by term in the test; (b) for the rest, each ratio's numerator and denominator asserted equal to the named companyfacts fact and value they came from — a weaker claim than the ratio being right, but one the code under test cannot manufacture · PR:

[ ] fourth-quarter derivation and the dump indicator · `src/fourth_quarter.py` · `python3.12 -m pytest tests/test_fourth_quarter.py -q` · annual and nine-month figures read off the filings for three companies and subtracted by hand in the test · PR:

[ ] quiet-restatement trace · `src/restatement_trace.py` and the ledger line it writes · `python3.12 -m pytest tests/test_restatement_trace.py -q` · a duplicate-period value planted in a copy of the companyfacts fixture, whose planted difference is the expected output · PR:

[ ] articulation checks · `src/articulation.py` · `python3.12 -m pytest tests/test_articulation.py -q` · the cash-flow and balance-sheet lines for receivables, inventory and payables read off the statements of two companies and differenced by hand in the test · PR:

[ ] tag-continuity map · `src/tag_continuity.py` and the map as versioned data · `python3.12 -m pytest tests/test_tag_continuity.py -q` · the two tag names read off the two filings of a company whose revenue tag changed; the expected output is an unbroken series across the change · PR:

[ ] research-and-development-capitalized column · `src/trends.py` · `python3.12 -m pytest tests/test_trends_rnd.py -q` · research and development expense and capitalized development cost read off the filings of two companies and capitalized by hand in the test · PR:

[ ] formula baselines · `src/baselines.py` writing `baselines.json` — Beneish M-score, accruals over assets, net operating assets, Piotroski F-score, Ohlson O-score, Altman Z-score, note cosine similarity, Loughran and McDonald negative share · `python3.12 -m pytest tests/test_baselines.py -q` · each published formula applied by hand to the frozen fixture and written out term by term in the test; the word-list file's sha256 recorded in the manifest · PR:

[ ] Exhibit 21 fetch and diff · `src/exhibits.py` and `input_exhibits.md` · `python3.12 -m pytest tests/test_exhibits.py -q` · the exhibit type read from the submission's SGML header for 12 of 12 companies, never from the filename, plus one subsidiary planted in a copy of a fixture that the diff must report · PR:

[ ] Exhibit 10 fetch on trigger · `src/exhibits.py` · `python3.12 -m pytest tests/test_exhibits_on_trigger.py -q` · a fixture 8-K carrying item 1.01, whose submission index names the exhibit that must be pulled · PR:

[ ] Item 1A splitter and diff · `src/split_sections.py` and `input_risk_factors.md` · `python3.12 -m pytest tests/test_split_risk_factors.py -q` · the section boundaries located by hand in 12 of 12 filings, plus a fixture whose risk factors are reordered without edits, which must yield zero changes · PR:

[ ] diff alignment with a multiset and a boilerplate score · `src/diff_periods.py` · `python3.12 -m pytest tests/test_diff_alignment.py -q` · constructed fixtures — one reordered, one retitled, one with a table of a hundred identical cells — whose expected change count is zero by construction · PR:

[ ] market module · `src/market.py` writing `input_market.json` · `python3.12 -m pytest tests/test_market.py -q` · abnormal returns computed by hand from a frozen price fixture and written out in the test; an after-close acceptance time that must move reaction day zero to the next trading day and carry the cutoff and the outcome window with it, so the window is still three days and still ends before the outcome window opens; a FINRA row that must attach by publication date and must not attach by settlement date; a two-year short-interest median computed by hand for one company · PR:

[ ] price-source delisting probe · a probe script and one line in `docs/structure_changes.md` · the probe run, exit status checked directly · a ticker known to have been delisted, whose history must come back; the source's own response is the expected value. Probe the three candidates named in the needs-judgment list below, in that order, and stop at the first that returns the history — this item gathers the evidence, it does not pick the source · PR:

[ ] per-agent input directory builder · `src/agent_inputs.py` · `python3.12 -m pytest tests/test_agent_inputs.py -q` · the layer table in `docs/INPUT_SPEC.md`, asserted file by file: a reader directory with no price file, a comparer directory with both reader reports and no filing, a supervisor directory with neither a filing nor the market table. The test must also assert the session root, because a directory that holds the right files but sits beside a readable sibling is not isolated — walk up from the root and fail if another agent's directory is reachable · PR:

[ ] quote and citation gate at every layer · `src/quote_gate.py` · `python3.12 -m pytest tests/test_quote_gate.py -q` · items planted on purpose — a quote with a changed dash, a quote with trimmed whitespace, a citation naming an id that does not exist — each of which must be dropped, and the drop count written into `input_manifest.json` · PR:

[ ] single-agent baseline runner · `src/control_single_agent.py` and the two control files · `python3.12 -m pytest tests/test_control_single_agent.py -q` · the output schema in `docs/CHECKLIST.md`, plus the quote gate, which must pass on the control's own output · PR:

[ ] shuffled-report control runner · `src/control_shuffled.py` and the two control files · `python3.12 -m pytest tests/test_control_shuffled.py -q` · a fixture pair of two companies' reports, where the expected output is that both files are written and that the numbers report and notes report in them came from different companies · PR:

[ ] scorecard template · `src/scorecard.py` and the template it renders · `python3.12 -m pytest tests/test_scorecard.py -q` · a fixture `runs/` directory; the expected output is a rendered scorecard with the Beneish M-score as the first accounting row and both caveat sentences present, with no hand edits anywhere in the path · PR:

[ ] monthly canary scheduled task · the task definition and its ledger line · one dry run, exit status checked directly · a defect planted on a branch on purpose; the expected result is that `refute-check` names it, and either a hit or a miss is appended to `events/ledger.jsonl` · PR:

---

## Needs judgment

Not launched. No judge exists for these, and inventing one would be inventing the
answer.

[ ] the price source · three candidates, in this order: **Stooq daily bulk zip** — a file download rather than an API call, which is why it survives the scripted-request block, delisted coverage unknown; **WRDS with CRSP through a Stony Brook account** — free if the school subscribes, and delisting returns handled the way the literature handles them, which is the only candidate that answers the delisted question properly; **a low-cost provider such as Tiingo or EODHD** — delisted coverage to be confirmed. Session 1 probed the two obvious free routes and neither served data: Stooq answers a scripted request with a JavaScript proof-of-work under both a plain and a browser user agent, and the Yahoo chart endpoint returns 429 unauthenticated, so the delisted-ticker question is still unanswered and the market module is built against a frozen price fixture. **Must be decided before the pattern study, not before expansion, because the study needs fifteen years of prices.** The project's no-paid-data rule named consensus data, not prices · needs judgment

[ ] thresholds for the four new numeric indicators — `articulation_gap`, `asset_growth_high`, `rnd_capitalization_shift`, `net_stock_issuance` · nothing waits: until rules v0.1 all four report their value and do not flag, so they measure from the first run and contribute nothing to a tier. What size of gap or growth should raise a flag needs the distribution over the 30 past cases, and a threshold is the owner's · needs judgment

[ ] the two-by-two flag thresholds · the accounting flag count grew from 26 to 33 and the pressure count from 16 to 17 while "4 or more" and "3 or more" stayed put, which loosens both tiers · needs judgment

[ ] narrowing the map from SIC code to sector ETF · the default is one ETF per SIC division and it ships with the market module, so nothing waits; whether a finer map by major group gives a better sector return is a modelling choice no test can settle · needs judgment

[ ] whether the review-response branch's published results merge into this history · two published-results histories diverge, and merging them is a claim about the record · needs judgment

[ ] whether the post-write plain-name hook should block the writer · the check names a code on stderr and exits 1; Claude Code hands any non-zero status other than 2 to the person at the keyboard and only 2 back to the agent that wrote the line, so today the writer is not told. Nothing waits: the check runs inside `make check` and CI runs `make check`, so a pull request carrying a code is red either way. Blocking would buy an earlier correction at the price of an interrupted turn, and that price is the owner's · needs judgment

[ ] whether the plain-name check should read source files and directory names · it reads `.py` and `.sh` by name only, because code quotes vocabulary that is not ours — a period offset, a linter's rule in a comment, the codes the check's own test plants — and it reads a file's own name but not the directories above it. The second-vendor lens calls both a blind spot. Widening either needs a rule for which quoted vocabulary is exempt, and a list of language suffixes has no rule to appeal to · needs judgment

[ ] the letter-number codes the archived project left in `CITATION.cff`, `LICENSE` and `LICENSE-docs` · a whole-tree sweep names six occurrences, four in the citation file and one in each licence file. Nothing waits: the check reads what a branch changed, and nothing changes those files. The two licence files are text that is not ours to edit and the citation file is a published record, so what to do with them is not a code change · needs judgment
