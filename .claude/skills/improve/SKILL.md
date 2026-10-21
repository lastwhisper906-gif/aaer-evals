---
name: improve
description: One pass of the improvement loop (docs/improve_loop.md) — find a weakness in the published runs, propose two or three minimal remedies, measure each against its baseline on held-in and held-out runs, open a pull request for what the measurement accepts. Use when the owner says to run the loop; $ARGUMENTS is the budget in list-price USD (default 60).
---

# One pass of the improvement loop

**Goal.** The pipeline's agents produce more that stands: fewer items the gates drop, fewer empty areas, no fewer anomalies, no lower grade — without weakening any gate. A measurement that refuses your remedy is this pass's finding, not a failure to hide.

**Fixed, read only.** The gates, `src/improve/`, `evals/`, `runs/ rules/ events/ history/`, `tests/fixtures/`, the expected values, the hooks, settings and workflows (`.claude/hooks/guard_fences.py` lists them; the session's settings and the hook refuse a write). A change you want there is a row in `docs/needs_judgment.md` with the default "stands" and the patch in your weakness file. Never soften a gate to pass it.

**Editable.** `.claude/agents/*.md` (never `analysis-grader.md`), `src/analysis_hook.py`, the agent wiring in `src/run_analysis.py` and `src/agent_inputs.py`, `lessons.md`, `.claude/skills/`. A component you add or change gets its line in `docs/improve/components.md`: which weakness, on which model, which measurement.

**Steps, in order.**
0. check — read `docs/improve/ledger.jsonl`; for each accepted edit not yet checked, measure its prediction on runs published since it merged, and append `kept` or `refuted` with the numbers.
1. mine — `.venv/bin/python -m src.improve.mine --runs runs --table`, then the raw analyses and the transcripts under `runs/<ticker>/.<accession>.logs/`. Write `docs/improve/<date>-weakness.md`: the evidence as file paths and counts, the root cause, the component responsible. A weakness no gate refuses is a gate gap: the owner's row, not yours to fix.
2. propose — two or three distinct, minimal edits, each on its own branch `improve/<date>-<slug>`, each with `docs/improve/<date>-<slug>/prediction.json`: evidence, cause, component, target metric and direction (one of `mine.WATCHED`), what might regress.
3. measure — `measure draw` the held-out runs (count 2; record the seed); `measure plan` under the budget; `measure run` the baseline from `origin/main` and the candidate, `--repeats 2`, `--work` outside the tree; `measure compare`. Put the rows and the verdict beside the prediction.
4. accept — `accepted: true`: commit the edit with its prediction and verdict, `make check`, push, open the pull request with auto-merge, one ledger line. Otherwise the ledger line with the numbers and the branch left as it is.

**Budget.** $ARGUMENTS USD at list price for the whole pass (60 when none is named); `measure plan` refuses what would exceed it. Model: `fable`, by alias (the owner's decision of 2026-10-21); a nested run falls back to Opus at the Fable limit as `src/run_analysis.py` does. Write what you did and what you would do next to `docs/improve/<date>-report.md`.
