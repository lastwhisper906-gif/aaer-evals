# How we work — who does what

## 1. Principles

1. **Plain names.** No letter-number codes. A code in a report, ledger, issue
   title, filename or commit message is a bug. Machine keys are readable slugs
   like `receivables_outrun_revenue`.
   Enforced for files and file names by `src/plain_name_check.py` (`make check`).
2. **The owner's signature is never a bottleneck.** No sign-off queue, no
   pending-decisions file, no "owner decision required" state. Work with no
   judge — no test, no schema, no check — is not defined as a task. It is left
   in `docs/next_cycle_tasks.md` as "needs judgment", and the owner reads those
   in one sitting at the next rules version.
   Enforced by `src/owner_inbox_check.py` and `src/task_judge_check.py` (`make check`).
3. **Everything has a default.** If the owner has not decided, proceed with the
   default. The only stop is one the owner placed personally.
   Enforced by `src/owner_inbox_check.py`: every inbox row names its default.
4. **Text goes through verbatim.** A model may select paragraphs; it never
   rewrites or summarizes text for the predictor. Commit exactly the text the
   predictor saw. Every quote is string-matched against the committed input,
   with every whitespace character read as an ordinary space, one for one, and
   every quote that stood only through that counted.
   Enforced by `src/quote_gate.py`.
5. **Python does the arithmetic.** Ratios, trends, diffs, baselines — all
   deterministic code. The model judges text only.
   Enforced by `src/analysis_check.py`.
6. **Layers see only their own input.** A reader sees filings; a comparer sees
   reader reports and the market table; a supervisor sees reports. The per-run,
   per-agent input directory is the boundary, and it is committed as what that
   agent saw.
   Enforced by `src/agent_inputs.py` (`tests/test_agent_inputs.py`).
7. **Append-only under `runs/`, `rules/`, `events/` and `history/`:** existing content is
   never changed or deleted; appending to the end of a ledger file is allowed.
   A correction is a new file plus one ledger line.
   Enforced by `src/append_check.py` (`make check`).
8. **The seal is nothing more than** auto-commit, pull request, auto-merge on
   green CI, and one timestamp command. No manifest, no signature gate, no seal
   window, no launch approval.
9. **Rules are versioned.** Each prediction is scored against its own rules
   version. Improvements apply from the next version; nothing is retroactive.
   Enforced by `src/scorecard.py`, which places each run by its own rules version.
10. **Infrastructure changes are capped at one day.** Past that, build the
    parsers in an interactive session. No new methodology, no new governance
    layer, no new document system. The old repo is archived, not rewritten —
    this is a thin layer on top.
    The archive half is enforced by `src/archive_check.py` (`make check`).
11. **Never soften an adverse result.** If no event happened, say so. If the
    model underperformed the baseline, say so.
12. **Mistakes compound.** When a session ends, its mistakes go into
    `lessons.md`, one line each. A lesson that a script or a test comes to
    enforce moves to `archive/lessons_enforced.md` with one line naming it;
    `tools/session_start_lessons.sh` prints the newest of the rest.
13. **Less process.** A second lens reads only a change to `rules/`, scoring,
    an agent prompt or a calculator formula; every other pull request merges on
    green CI. A branch is merged or closed within a day. The weekly test is
    whether a readable result was produced. Decided by the owner on 2026-09-28;
    §5 says which files that is.

## 2. Vocabulary

**Three analyses**, never merged (the owner's decision of 2026-09-28):
**accounting** — do reported earnings and cash reflect economic reality?
**financial** — how healthy is this company? **valuation** — what is it worth,
and what does the price already assume? No composite score, no rank across
companies. The two questions of the first design — accounting reliability and
financial pressure — are the first two analyses' ancestors; the pilot runs that
answered them stay scored under their own rules version.

**Layers**: readers → analysts. A reader reads filings. The accounting and
financial analysts read the reader reports and what Python computed from the
filings, never a price; the valuation analyst adds the price at the cutoff, the
two analyses and the MD&A verbatim. A comparer reads reader reports and the
market table, and runs only for the reaction-window labels.

**Pipeline stages**: detect filing → extract → market → read → calculate →
analyse → controls → publish → record events → score.

**Task-list states**, in `docs/next_cycle_tasks.md`: unchecked → has a pull
request → merged.

**Finding weight**: severe / moderate / minor.
**Finding kind**: threatens the prediction record / quality / cosmetic / needs
judgment.

---

## 3. The pipeline

Prediction is a routine, not a loop. There is no iterative improvement pass over
a prediction.

**The agent stages are three: reader → analyst → valuation**, with three
handoffs, each through a Python gate: the quote-gated reader reports to the
accounting and financial analysts, the checked analyses to the valuation
analyst, and its checked reading to the memo. Everything between them -- the
market labels, the calculator, the gates, the memo -- is Python.

| Stage | Does | Passes when |
|---|---|---|
| detect filing | daily: new filings for the twelve, from the EDGAR submissions index — `src/detect_filing.py`, one lookup per `universe.json` row | 12 of 12 lookups succeed |
| extract | the input spec, plus the diff, the trend table, the articulation checks and the histories | schema passes, paragraph counts in the normal range, zero cutoff violations, at least one `TextBlock` found |
| market | the market table — abnormal returns, both reaction windows, the short-interest ratio and its two-year median | every trading day from the prior filing to reaction day two has a row, and nothing past reaction day two exists in it |
| read | two calls: the numbers reader and the notes-text reader, each seeing only its own input directory. **Waits until reaction day two has closed** | every item carries a verbatim quote that string-matches that reader's committed input; unverifiable items are dropped and counted |
| compare | Python, no model: `src/market_labels.py` labels each reader item against each reaction window -- `priced_in`, `not_priced` or `opposite_direction`, from the sign of the abnormal return against the item's `expected_direction` -- and writes short interest above its two-year median as a separate field; with no market table it writes nothing (the owner's decision of 2026-10-06) | every label cites a reader item, and carries exactly one of the three labels |
| calculate | `src/calculator.py`: ratios, the four free-cash-flow measures, WACC and, once drivers exist, the DCF, reverse DCF and sensitivity grid — Python only, from the as-filed rows at the cutoff | every core input on record or named as missing; exit status says which |
| analyse | `src/run_analysis.py`: the accounting and financial analysts (two calls, never merged, on the reader reports and the filings-only calculator), then the valuation analyst in two passes (drivers, then the reading of what Python computed from them), then the plain-Korean memo. The supervisors' decide stage left the live pipeline on 2026-09-28; their definitions and the comparers' are in `archive/agents/` since 2026-10-06 | every item passes `src/analysis_check.py` — numbers only as calculator paths, citations and quotes verbatim — or is dropped and counted; every agent's model, tokens and cost in `input_manifest.json` |
| controls | the formula baselines (Python) and the single-agent control answering the same three analyses from the whole bundle and the calculator | every baseline computed, the control wrote its files, none merged into the analyses; `src/analysis_scorecard.py` sets them side by side |
| publish | commit → pull request → auto-merge on green CI → `ots stamp input_manifest.json` | the merge succeeded and the `.ots` file exists |
| record events | 8-K 4.01 / 4.02 / 1.01 / 5.02, late filings, amendments, comment letters, material-weakness language, quiet restatements, explanation materialization → `events/ledger.jsonl` | the append succeeded |
| score | on horizon expiry or event occurrence, recompute the metrics and regenerate the results document | deterministic match |

On a failure of an agent call in `read` or `analyse`, retry once with identical
input, then record a failure. A retry never changes the input.
`src/run_analysis.py` does this: `RETRIES = 1`, and nothing the failed call wrote survives the retry.

`detect filing` runs daily; the rest of a full run does not. It waits for
reaction day two so the market labels get a whole window. A light run on an
8-K 2.02 wakes both readers only; its market table is refused by the labeller
("no filing window") until `src/market.py` writes the 8-K's own window as the
light run's `filing` window, so today nothing is labelled on a light run
(`docs/needs_judgment.md` holds the question and the default).

**Publish merges itself.** `main` requires the CI check and nothing else — no
reviewer, no approval. Every pull request from the pipeline or a routine sets
`gh pr merge --auto --squash` the moment it is opened, so it lands as soon as CI
goes green and nobody clicks anything. A pull request sitting open waiting for
the owner is the bottleneck the rules forbid, not a safety measure.

There is no metered billing path — subscription authentication only.

---

## 4. Routines

These start from the errors actually hit in the ten months of the archived
project: the "documents used" list was really "documents provided"; the cache
checked fingerprints but not output validity; rows without accession numbers
passed the loader; perturbation was applied to one arm only; experiment labels
leaked into inputs; a cycle closed with empty result files; cross-references
dangled; verdicts were wrong on shallow clones; figure labels drifted; README
numbers disagreed with recomputation. Every one was found by a human later, and
every one could have been checked by a machine daily.

Every routine below is a **scheduled task**, not a loop run.

### Daily

- **nightly worker** — the queue's next items, then `make check` and `make eval`
  on main, and a report. `docs/routines/nightly-worker.md`
- **missing-filing check** — `src/nightly.py`, run by
  `.github/workflows/nightly.yml`: a filing with no directory under `runs/` is
  extracted, and `src/extraction_checks.py` holds each new bundle to ±20% of
  the recorded counts
- **prediction-tamper check** — `src/append_check.py`, in CI on every push
- **daily summary** — one notification at eight in the morning, local: where the
  pipeline stands, what moved in the ledger since yesterday, which pull requests
  are open, and the `docs/needs_judgment.md` rows. Status only. It never asks a
  question and never waits for an answer; `tools/daily_summary.sh` writes it and
  the notifier speaks it
- **morning report** — the nightly crew's results, failures first, as the final
  message of a cloud scheduled task at 07:30 US Eastern; it also opens the
  night's pull request. `docs/routines/morning-report.md`. The night itself is
  `.github/workflows/nightly.yml`, Python with no model

### Weekly

- **weekly gardener** — grader bugs, rules nobody follows and stale
  instructions, each from evidence. `docs/routines/weekly-gardener.md`
- **re-lens** — every row the second lens read on the same-family fallback, and
  every pull request labelled `one-lens`, re-read at the commit it merged at
  once the Codex quota is back. `docs/routines/weekly-relens.md`. A pass moves
  the row to done; a fail opens an issue marked "needs judgment" naming the
  merged pull request, and fixes nothing itself

### Monthly

- **ablation** — remove one harness component and see whether anything the
  owner measures gets worse. `docs/routines/monthly-ablation.md`

### Hooks

Configured in `.claude/settings.json`, not written by hand each session.

- **session start** — `sh tools/session_start_lessons.sh`: the header of
  `lessons.md` and its newest lessons, at most sixty lines
  (`tests/test_session_start_lessons.py`). **`CLAUDE.md` is capped at 22
  lines** (`src/instruction_length_check.py`, `make check`), so a rule that
  cannot fit replaces a line rather than appending one — the file is read in
  full at the start of every session.
- **after a compaction** — re-inject the cutoff line from `CLAUDE.md`. Of every
  rule here it is the one whose violation is silent, so it is the one that must
  not fall out of context.
- **after a write or edit** — the plain-name check on the changed files.
- **session end** — `make check` under the pinned interpreter, then one line to
  the notification centre if the turn opened a pull request or wrote a
  needs-judgment item. Silent otherwise; a notifier that speaks every turn is
  one you stop reading.

Writing this session's mistakes into `lessons.md` is not a hook and cannot be
one: only the session knows what it got wrong. It is a rule in `CLAUDE.md`, and
the Stop hook running green is not evidence that it happened.

---

## 5. The loop

The custom harness is gone. **Kept**, because nothing native does them:
`src/append_check.py`, in CI on every push; and the **refute protocol** — an
expected value comes from the source, never from the first run of the code it
judges (`tests/expected_values.py` refuses an unsourced value).

**Dropped, and what does the job now:**

| Dropped | Now |
|---|---|
| the work ledger and its six states | git, pull requests, `docs/next_cycle_tasks.md` |
| the cycle audit | Code Review on every pull request |
| the write-restriction guard and its self-test | hooks in `.claude/settings.json` |
| the stop conditions as a file | `/goal` |
| the builder and reviewer session pair | the `refute-check` and `reproduce-check` subagents |
| the doc-bloat penalty | nothing — it measured a frozen tree |
| the STOP file | the owner interrupting the session |
| the `claude --bg` launcher | scheduled tasks |

**Less process.** The owner adopted this on 2026-09-28
(`docs/structure_changes.md`): a second lens is required only on a pull request that changes `rules/`,
scoring (`src/scorecard.py`, `src/scorecard_template.md`), an agent prompt
(`.claude/agents/`) or a calculator formula — the arithmetic in
`src/calculator.py`, which writes `calculator.json`, or in `src/trends.py`,
`src/articulation.py`, `src/baselines.py`, `src/fourth_quarter.py` or
`src/market.py`. A change elsewhere in those files (a fetch, a refusal, a
docstring) is not a formula.

**The two lenses, on the pull requests that need them.** Such a change is read
twice before its pull request opens: `refute-check` (Claude), then
`tools/second_lens.sh`. Both lenses read `tools/lens_prompt.md` and answer
`tools/lens_verdict.schema.json`, so the two verdicts are comparable and neither
drifts from the five rules. Codex is the cross-vendor lens; when it cannot run,
Claude Fable answers in a fresh context and the row is marked `confirmed -
same-family fallback` rather than `confirmed - cross-vendor`. When neither runs
the script exits 3, which is never an approval: the pull request opens labelled
`one-lens` with auto-merge off. The weekly re-lens routine re-reads every
fallback and every `one-lens` row once the Codex quota returns.
`.claude/skills/build-item/SKILL.md` step 4 is where the builder decides whether
a change needs the lenses at all.

A Stop hook is a safety net, not a judge — the turn ends after eight consecutive
blocks, so a hook that keeps failing stops blocking. CI is the judge.

---

## 6. Which model does what

The owner's decision of 2026-10-06 (`docs/structure_changes.md`) sets this table.

| Role | Model | Why |
|---|---|---|
| numbers reader, notes-text reader | Opus, effort xhigh | long inputs and most of the tokens; reading a filing is where a missed detail is not recoverable downstream |
| **accounting-analyst, financial-analyst, valuation-analyst (both passes)** | **Fable**, used efficiently | judgment over short, cited inputs; the efficiency rules are below |
| single-agent control | Fable, **on the golden filings only** | there it is scored against the owner's cases; on other filings it measured format as much as judgment |
| analysis-grader (`evals/`) | Opus | never the analysts' model, so it does not grade its own kind |
| market labels (were the two comparers) | Python, `src/market_labels.py` | the label is mechanical: the sign of the abnormal return against the expected direction |
| second lens, builder sessions, the three routines | Opus | the lens fallback runs with `LENS_FALLBACK_MODEL=opus` |
| when a model change is needed | the owner decides; `--model` on `src/run_analysis.py` is the run-time override, recorded as `model_override` in the manifest | a run set on two models compares models as well as companies |

**Fable, used efficiently.**
- **Trimmed inputs.** The analysts get the two reader reports, `calculator.json` and
  nothing they will not cite. The valuation analyst gets only the MD&A and guidance
  paragraphs the notes reader flagged.
- **Shared inputs first, in a fixed order,** so the prompt cache serves them.
- **No repeat of a passed call.** A Fable call whose output passed the gate is never
  run again. A failed call reruns only that agent, at most twice.
- **"Fable limit reached" stops the batch.** What finished is published, what is
  pending is written into `queue.md`, and the batch continues the next night. An
  analyst never falls back to Opus.
- **Tokens are counted.** Input, cache-write, cache-read and output tokens, and wall
  time, are recorded per agent per filing in `input_manifest.json`.
- **The batch is sized from the record.** The nightly batch is Fable tokens available ÷
  the median Fable tokens per filing on record, and the calculation goes into the
  morning report.

Agent prompts are committed under `.claude/agents/` and versioned with the
rules. **Nothing in the read, compare or decide stages writes a prompt at run
time.**

**The lens does not read its instructions out of the tree it is judging.** That
sentence had to be earned. Four lens readings and four refute-checks of the lens
itself found fourteen defects in it, five of which ended in an approval, and
every one of them was a version of the same mistake: the thing deciding the
verdict was reachable from the branch being judged. The prompt, the schema and
the module that decides what a verdict is now come out of a pinned ref rather
than the worktree; the reader runs from the judge's own directory so `python -m`
cannot put the branch's `src/` first on the path; the judge directory is cleared
with the removal checked, because a planted one that survives `rm -rf` answers
from exactly where the pinned one would have; and the fallback is started
`--restricted`, with its agent definition passed inline, because a session
started in the worktree is handed that tree's `CLAUDE.md`, `AGENTS.md`, its
`.claude/` settings and agents, and — through the SessionStart hook — the
newest sixty lines of the lessons file verbatim. A sentinel line in `lessons.md` came
back to the model in one turn with no tool call; the same probe answered
`ABSENT` once the flag was added.

**Four trust roots remain, and they are named rather than papered over.**

1. **`tools/second_lens.sh` cannot pin itself.** It is already running, and the
   build skill invokes it by relative path from inside the worktree, so a branch
   that replaces the file gets whatever exit status it writes. No check inside a
   file survives that file being replaced. What the script does instead is
   record whether it matched the pinned ref, as `lens_from` in the ledger row
   and in the line it prints; the weekly routine greps the `tree` rows. **The
   hole itself is closed by a person reading the diff of that one file**, and
   nothing else closes it.
2. **Four refusal paths still write their ledger row with the tree's reader.**
   The judge directory is inside the worktree, so it cannot be materialised
   until the pin has been checked — and the checks that decide whether the pin
   is usable at all (the ref resolves, the ref is on the trunk, the directory
   cleared, the diff is not empty) run before it exists. Each of those refuses
   with exit 3, so nothing merges on the strength of one; what the tree gets is
   arbitrary code execution on a path where the run was failing anyway, and a
   ledger row it could falsify. The fix is to put the judge somewhere the tree
   cannot reach and pin before anything else runs, which is a row in
   `docs/next_cycle_tasks.md`. Until that lands this is a hole, not a design.

   The claim that stood here — that the first root is "closed by a person
   reading the diff of that one file" — was false while the interpreter probe
   ran `src.lens_verdict` out of the worktree before the pin: a reviewer reading
   `tools/second_lens.sh` would not have seen code planted in the tree's reader,
   and that code ran with the script's privileges over the running script, over
   the `.venv` link and over the ledger. The second lens found it on 2026-09-22;
   the probe now asks the interpreter a question with no repository code in it.
3. **The interpreter that runs the judge comes out of the worktree.**
   `LENS_PYTHON` defaults to `$REPO_ROOT/.venv/bin/python`, and in the build
   topology `REPO_ROOT` *is* the tree under review. `.venv/` is git-ignored, so
   a binary planted there is invisible to `git diff`, to the uncommitted-changes
   refusal and to `DEFINES_THE_JUDGE` — and it is what runs the pinned reader,
   reads both answers, maps the exit code and writes the ledger row. This
   document already watches the equally-ignored `.claude/settings.local.json` on
   exactly that reasoning. Refusing it outright would be wrong, because on the
   main checkout the repository is the worktree and that is the ordinary case,
   so the run records a caveat when the interpreter resolves inside the tree it
   is judging. Closing it means an interpreter the tree cannot write, which is
   the same row as moving the judge directory out of the worktree.
4. **A hook that runs the tree's own code prints the tree's own output.**
   `make check` at Stop is the tree's test suite. Reading a tree's output is
   what reviewing a tree is, so this is inherent rather than fixable. It is
   bounded by the fact that opening a *new* channel means editing
   `.claude/settings.json`, which is on the watch list.

**An agent file names a family, not a pin.** `model: opus` and `model: fable`
are aliases and carry no effort setting, so the pin proper — the dated model id
and the effort — lives in the rules version and is applied at invocation. The
run records both the requested pin and the served model in
`input_manifest.json`, and a run whose served model differs from the pin is
recorded as a failure. A pin that exists only in this table is not a pin.

---

## 7. The sequence

1. **Dispose of the old.** Done when `archive/` exists, the supersession commit
   exists, and the tags exist.
2. **Repo skeleton, `CLAUDE.md`, `lessons.md`, the three `docs/` files.** Done
   when the tree exists and CI is green.
3. **Replace the harness with the native loop.** Done when
   `.claude/settings.json`, the agent definitions and the two skills exist, no
   hook points at the harness, and `make check` is green. One-day cap.
4. **Parser build.** The items in `docs/next_cycle_tasks.md` are this step: the
   companyfacts fetcher, the `TextBlock` extractor, the section splitters, the
   8-K parser, the paragraph diff and its alignment, the note change history,
   the trend table, the articulation checks, the exhibits, the market module,
   and the extraction pass checks. Done when every item has a merged pull
   request or is marked "needs judgment". Two weeks.
5. **Detect-filing and extract scheduled tasks, plus CI.** Done when the first
   automatic extraction lands in `runs/` as a pull request.
6. **Report shapes, agent definitions, then the baselines and the control.**
   The four report shapes and the per-agent input directories first; then the
   six agent definitions run against a fixture; then the formula baselines and
   the single-agent control. Done when one fixture filing produces four reports,
   two predictions, `baselines.json` and both
   control files, with every citation resolving.
7. **The 30 past cases, then rules v0.1 in force.** Run the input spec and the
   input indicators over the archived cases at their cutoff dates and produce the
   flag distribution table. The owner adjusts the thresholds or does not. Commit
   `rules/*_v0.1`. Done when the rules files exist.
8. **Enable read, compare, decide and publish.** Done when the next filing
   produces the first prediction pull request, auto-merged, with its timestamp
   file.
9. **Register the routines.** Daily, then weekly, then monthly, plus the hooks.
   Done when each scheduled task has one run log.
10. **Expansion — designed, not started.** The universe is drawn from the EDGAR
    full index **as of a past date**, never from today's ticker list, because
    today's list has already dropped everything that failed. Delisted companies
    stay in. Small and mid capitalizations are included on purpose — that is
    where the drift the pipeline is looking for still exists. The price source
    is checked for delisted coverage before the universe is frozen. The
    cross-section is cut by calendar frames, never by company fiscal quarters.
    Nothing here starts until step 9 is done.

    **Prices.** The study reads **CRSP through WRDS**, the only source in reach
    that carries the delisting return — free *to us*, through a subscription
    Stony Brook already pays for, which is not the same as free and is the
    distinction `docs/needs_judgment.md` turns on; the forward track's twelve are all currently
    listed and read through the **Tiingo** free tier instead. A row whose
    delisting return is missing takes **−30%**, and **−55%** on Nasdaq —
    Shumway (1997), and Shumway and Warther (1999) — recorded per row as the
    value used and the reason it was used, so the cross-section is reported both
    with and without the correction. The function that applies the default and
    records which of the two it was lands with the price-interface row in
    `docs/next_cycle_tasks.md`; until then these are two numbers out of the
    literature and nothing reads them.

    Paying for EODHD, if it comes to that, is a decision recorded in
    `docs/needs_judgment.md` that **overrides** a line already written:
    `docs/INPUT_SPEC.md` says the price source is free in the preamble, in §1's
    own table and in §4. The consensus exclusion is about consensus. The day a
    paid month is used, §4 is what has to be amended.

Each step starts when the previous step's condition is met.

---

## 8. Do not

- Create new identifier families, new ledgers, new approval procedures, new
  document systems.
- Put a prior run's probability into any agent's input.
  Enforced by `src/agent_inputs.py`, which refuses a prior-predictions file that still carries one.
- Change a cycle's rules or thresholds after seeing its results.
  `rules/` is append-only, so a published rules file cannot change (`src/append_check.py`).
- **Record any observation about signal from the twelve companies**, anywhere.
  They are the most-read filings on earth and the models already know how the
  period ended. What the twelve produce is a pipeline check.
- Write "finds alpha" or "detects accounting fraud". The sentence is: **reads
  filings, compares with the market, predicts two questions, and leaves a
  verifiable record.** That narrow claim is the one that survives Gu, Kelly and
  Xiu, whose winning signals were momentum, liquidity and volatility rather than
  accounting: our targets are accounting reliability and financial pressure, and
  return direction is one target among several.
- Hide that accounting-reliability events were zero in year one.
