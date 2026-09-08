# How we work — who does what

## 1. Principles

1. **Plain names.** No letter-number codes. A code in a report, ledger, issue
   title, filename or commit message is a bug. Machine keys are readable slugs
   like `receivables_outrun_revenue`.
2. **The owner's signature is never a bottleneck.** No sign-off queue, no
   pending-decisions file, no "owner decision required" state. Work with no
   judge — no test, no schema, no check — is not defined as a task. It is left
   in `docs/next_cycle_tasks.md` as "needs judgment", and the owner reads those
   in one sitting at the next rules version.
3. **Everything has a default.** If the owner has not decided, proceed with the
   default. The only stop is one the owner placed personally.
4. **Text goes through verbatim.** A model may select paragraphs; it never
   rewrites or summarizes text for the predictor. Commit exactly the text the
   predictor saw. Every quote is string-matched against the committed input.
5. **Python does the arithmetic.** Ratios, trends, diffs, baselines — all
   deterministic code. The model judges text only.
6. **Layers see only their own input.** A reader sees filings; a comparer sees
   reader reports and the market table; a supervisor sees reports. The per-run,
   per-agent input directory is the boundary, and it is committed as what that
   agent saw.
7. **Append-only under `runs/`, `rules/` and `events/`:** existing content is
   never changed or deleted; appending to the end of a ledger file is allowed.
   A correction is a new file plus one ledger line.
8. **The seal is nothing more than** auto-commit, pull request, auto-merge on
   green CI, and one timestamp command. No manifest, no signature gate, no seal
   window, no launch approval.
9. **Rules are versioned.** Each prediction is scored against its own rules
   version. Improvements apply from the next version; nothing is retroactive.
10. **Infrastructure changes are capped at one day.** Past that, build the
    parsers in an interactive session. No new methodology, no new governance
    layer, no new document system. The old repo is archived, not rewritten —
    this is a thin layer on top.
11. **Never soften an adverse result.** If no event happened, say so. If the
    model underperformed the baseline, say so.
12. **Mistakes compound.** When a session ends, its mistakes go into
    `lessons.md`, one line each. A weekly routine folds rules into `CLAUDE.md`
    and procedures into skills.

## 2. Vocabulary

**Two questions**, never merged: **accounting reliability** — do these numbers
reflect reality? **financial pressure** — is this company under pressure?

**Three layers**: readers → comparers → supervisor. A reader reads filings. A
comparer reads reader reports and the market table. A supervisor reads reports.

**Pipeline stages**: detect filing → extract → market → read → compare →
decide → controls → publish → record events → score.

**Task-list states**, in `docs/next_cycle_tasks.md`: unchecked → has a pull
request → merged. An item with no judge is "needs judgment" and is never
launched.

**Finding weight**: severe / moderate / minor.
**Finding kind**: threatens the prediction record / quality / cosmetic / needs
judgment.

---

## 3. The pipeline

Prediction is a routine, not a loop. There is no iterative improvement pass over
a prediction.

| Stage | Does | Passes when |
|---|---|---|
| detect filing | daily: new filings for the twelve, from the EDGAR submissions index | 12 of 12 lookups succeed |
| extract | the input spec, plus the diff, the trend table, the articulation checks and the histories | schema passes, paragraph counts in the normal range, zero cutoff violations, at least one `TextBlock` found |
| market | the market table — abnormal returns, both reaction windows, the short-interest ratio | every trading day between the prior filing and the cutoff has a row, and nothing past the cutoff plus two trading days exists in it |
| read | two calls: the numbers reader and the notes-text reader, each seeing only its own input directory | every item carries a verbatim quote that string-matches that reader's committed input; unverifiable items are dropped and counted |
| compare | two calls: numbers versus market, notes versus market. Neither sees a filing | every item cites an upstream item id that resolves, and carries exactly one of the three labels |
| decide | two calls: supervisor-accounting and supervisor-pressure. Neither sees a filing or the market table | output schema valid, every citation resolves to an upstream report, served model equals the pin |
| controls | the formula baselines (Python), the single-agent baseline, the shuffled-report control | every baseline computed, both controls wrote their files, none merged into the pipeline's number |
| publish | commit → pull request → auto-merge on green CI → `ots stamp input_manifest.json` | the merge succeeded and the `.ots` file exists |
| record events | 8-K 4.01 / 4.02 / 1.01 / 5.02, late filings, amendments, comment letters, material-weakness language, quiet restatements, explanation materialization → `events/ledger.jsonl` | the append succeeded |
| score | on horizon expiry or event occurrence, recompute the metrics and regenerate the results document | deterministic match |

On a failure in `read`, `compare` or `decide`, retry once with identical input,
then record a failure. A retry never changes the input.

**Publish merges itself.** `main` requires the CI check and nothing else — no
reviewer, no approval. Every pull request from the pipeline or a routine sets
`gh pr merge --auto --squash` the moment it is opened, so it lands as soon as CI
goes green and nobody clicks anything. A pull request sitting open waiting for
the owner is the bottleneck the rules forbid, not a safety measure.

Scheduled-task sessions start from a clone, sparse-checked-out to that company's
`runs/` only. A model fallback is possible, so the served model is recorded; if
it differs from the pin the run is recorded as a failure. There is no metered
billing path — subscription authentication only.

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

- **cutoff re-check** — every date and accession in published inputs, including
  that no market row past the cutoff plus two trading days reached an agent
- **quote re-check** — every reader quote against its committed input, and every
  comparer and supervisor citation against the upstream report
- **layer-isolation re-check** — each agent input directory against the layer
  rule
- **missing-filing check** — the EDGAR list against `runs/`
- **prediction-tamper check** — any change to existing content, or deletion, of
  a `runs/`, `rules/` or `events/` file that exists on `origin/main` fails CI and
  blocks the merge; appending to the end of a ledger file passes. Everything
  under those three prefixes is a record — documentation about them lives in
  `docs/`
- **rules-precedence check** — the rules-version commit is an ancestor of the
  prediction commit
- **event-gap check** — EDGAR events against the ledger

### Weekly

- **extraction drift** — re-extract the latest filing for each of the twelve;
  paragraph, note or number counts outside ±20% open an issue
- **schema and hash**
- **unreferenced code**
- **dependencies** — update, hash-lock, test, pull request
- **document numbers recomputed**
- **broken links and paragraph ids**
- **fold lessons** — `lessons.md` into `CLAUDE.md` for rules and into skills for
  procedures; merge duplicates; strengthen anything seen three or more times;
  open a pull request

### On red CI

A fix pull request, at most three attempts. Never touch `runs/`, `rules/` or
`events/`. Never change a test expectation. After three failures, open an issue
marked "needs judgment" — not a signature request.

### Monthly

- **seeded-defect canary** — plant one known defect on a branch, run the
  `refute-check` subagent against it, and append hit or miss to
  `events/ledger.jsonl`. A verification layer that has never been shown to catch
  a defect is not known to work. This is the one piece of the old harness kept
  as a routine.
- **monthly scorecard** — the evaluation metric tables, with no judgment added.

### Hooks

Configured in `.claude/settings.json`, not written by hand each session.

- **session start** — read `lessons.md`.
- **after a write or edit** — the plain-name check on the changed files.
- **session end** — `make check`, and this session's mistakes into `lessons.md`,
  one line each, no judgment.

Routines do not run the pipeline, do not build parsers, and do not judge.

---

## 5. The loop

The custom harness is gone. What it did is now done by Claude Code's own
primitives, plus three things nothing native does.

**Kept.**

- `src/append_check.py` — the prediction record is append-only, and it runs in
  CI on every push.
- **the refute protocol** — an expected value comes from the source document,
  from companyfacts, or from a hand computation. Never from the first run of the
  code it is meant to judge.
- **the seeded-defect canary** — monthly, as a scheduled task.

**Dropped, and what does the job now.**

| Dropped | Now |
|---|---|
| the work ledger and its six states | git, pull requests, `docs/next_cycle_tasks.md` |
| the cycle audit | Code Review on every pull request |
| the write-restriction guard and its self-test | hooks in `.claude/settings.json` |
| the stop conditions as a file | `/goal` |
| the builder and reviewer session pair | the `refute-check` and `reproduce-check` subagents |
| the doc-bloat penalty | nothing — it measured a frozen tree, so it measured nothing |
| the STOP file | the owner interrupting the session |
| the `claude --bg` launcher | scheduled tasks |

A Stop hook is a safety net, not a judge — Claude Code ends the turn after eight
consecutive blocks, so a hook that keeps failing stops blocking. CI is the judge.

---

## 6. Which model does what

| Role | Model | Why |
|---|---|---|
| numbers reader, notes-text reader, both comparers | Opus, effort xhigh | reading a filing and reading a report against a market table are the two places where a missed detail is not recoverable downstream |
| **supervisor-accounting, supervisor-pressure** | **Fable, pinned for one year together with rules v0.1** | keeping the pin matters more than raw capability — a track record only means something as quarter-to-quarter comparison under the same model and the same rules. Check subscription-path stability from the served-model record on the first run; if fallbacks are frequent, drop the pin to Opus. |
| single-agent baseline control | the same model as the supervisor | a control on a different model would measure the model, not the structure. Its prompt lives inside the control's run script, not in `.claude/agents/` — it is a control, not a layer, and it must not become something a session can invoke by name |
| refute verification, claim-strength review | Fable | heavy judgment, where a mistake is expensive |
| reproduce verification, full review | Opus, effort xhigh | the existing pins |
| when a model change is needed | run both models in parallel for one quarter, then switch | a switch without a bridge quarter contaminates the record |
| paragraph classifier | Haiku class | labels only |
| routines | Haiku to Sonnet class | reads script output and opens pull requests |

Agent prompts are committed under `.claude/agents/` and versioned with the
rules. **Nothing in the read, compare or decide stages writes a prompt at run
time.** Pins and served models are recorded in `input_manifest.json`.

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
   and the extraction pass checks. Every expected value comes from companyfacts,
   the source document or a hand computation — never from a run of the parser
   it judges. Done when every item has a merged pull request or is marked "needs
   judgment". Two weeks.
5. **Detect-filing and extract scheduled tasks, plus CI.** Done when the first
   automatic extraction lands in `runs/` as a pull request.
6. **Report shapes, agent definitions, then the three controls.** The four
   report shapes and the per-agent input directories first; then the six agent
   definitions run against a fixture; then the formula baselines, the
   single-agent control and the shuffled-report control. Done when one fixture
   filing produces four reports, two predictions, `baselines.json` and both
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

Each step starts when the previous step's condition is met. Never wait for owner
confirmation.

---

## 8. Do not

- Rewrite or refactor the archived repo. It is an archive.
- Create new identifier families, new ledgers, new approval procedures, new
  document systems.
- Hand summaries to the predictor.
- **Let anything cross a layer.** A reader never sees prices. A supervisor never
  sees a filing. Market data enters only through the market table, and only the
  comparers read it.
- Put a prior run's probability into any agent's input.
- **Write a prompt at run time** in the read, compare or decide stages. The
  prompts are committed files.
- Change or delete existing content under `runs/`, `rules/` or `events/`.
  Appending to the end of a ledger file is fine.
- Change a cycle's rules or thresholds after seeing its results.
- Combine indicators into a composite rank across companies. The formula
  baselines are baselines, never inputs.
- Stop and wait for the owner. Take the default and leave one line.
- Spend more than one day on infrastructure changes.
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
