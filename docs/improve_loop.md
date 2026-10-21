# The improvement loop — design

The owner's words, 2026-10-16: a system that runs when told, finds a problem
like the dropped findings of 2026-10-14, finds its own remedy (a hook, a
prompt line, a line of wiring), tests it, and ships it — and that does not go
stale when the next model arrives. Designed against the seven findings of the
2026 harness literature read on 2026-10-16 (`docs/structure_changes.md`);
nothing below is built yet. A line that names a file names what will exist.

## What the model does, and what stays fixed

The model finds weaknesses, chooses the remedy, writes it, predicts its
effect, and argues from measurement. Everything that judges the model is
fixed, outside the loop, and read-only to it:

| Fixed (the loop may read, never write) | Enforced by |
|---|---|
| `evals/`, the graders and the rubric | already: the owner's (`CLAUDE.md`) |
| the gates: `src/analysis_check.py`, `src/quote_gate.py`, `src/plain_name_check.py`, `src/cutoff_guard.py`, `src/extraction_checks.py`, `src/calculator.py`'s arithmetic | the improve session's settings deny Edit/Write there and a PreToolUse guard on Bash refuses a shell write (`.claude/hooks/guard_fences.py`, the shape of `guard_evals.py`); CI's `fences` job, once the owner labels the workflow change |
| the measurement: `src/improve/measure.py` and its acceptance rule | the same |
| the records: `runs/`, `rules/`, `events/`, `history/`, `docs/improve/ledger.jsonl` | already: `src/append_check.py` |
| expected values: `tests/expected_values.py`, `tests/fixtures/**` | already: an unsourced value is refused |
| the model: an alias (`opus`), never a version string; the effort | `src/improve/measure.py` refuses a run whose manifest names a version the loop chose |

A change to anything in the left column is never the loop's to make. The loop
writes the row in `docs/needs_judgment.md` with the default "the gate stands"
and, in the scratch of its report, the patch it would propose. (Finding 1:
metrics kept outside the agent's control.)

**Editable surfaces**, each with one line in `docs/improve/components.md`
saying which weakness it exists for, which model that weakness was seen on,
and the measurement that justified it (finding 2: a harness component is an
assumption that goes stale):

- the analyst and reader prompts under `.claude/agents/` (never `analysis-grader.md`)
- `src/analysis_hook.py` and any hook like it
- the agent wiring in `src/run_analysis.py` and `src/agent_inputs.py` (the
  boundary tests hold them)
- `lessons.md` and the skills under `.claude/skills/`

## The loop, one pass

```
told to run (chat "/improve", `make improve`, or the Actions button)
  1. mine      Python lists what every published run shows: drops by reason,
               empty areas, adjustments, grader score and dealbreakers,
               gate_feedback rounds, tokens and cost — a table, no thresholds.
               The model reads the table, then the raw files and the agent
               transcripts, and writes weakness.md: evidence, root cause,
               the component responsible.
  2. propose   two or three distinct, minimal edits, one branch each, each
               with prediction.json: evidence · cause · component · expected
               effect (which measure, which direction) · what it might break.
  3. measure   src/improve/measure.py, on copies outside the tree: the agents
               the edit touches, run again on the held-in runs (where the
               weakness showed) and on held-out runs (drawn by Python from the
               rest, seed recorded, never named to the proposer), k times
               each; the baseline the same k times, so the spread is known.
  4. accept    only an edit that moves its target on held-in and regresses
               nothing on held-out beyond the baseline spread; rejected
               edits go to the ledger with their numbers. One pull request
               per accepted edit, the measurement in its body, auto-merge
               on green CI. Nothing waits for a click.
  5. check     the next pass starts by reading the open predictions and
               measuring them on the runs published since: kept or
               refuted, one ledger line each.
```

Findings 3 and 4: weakness → bounded proposal → held-in/held-out validation;
every edit a falsifiable prediction. Finding 5: the proposer never grades
itself — the graders are Opus under `evals/`, the second lens is Codex, and
`measure.py` is Python. Finding 6: a remedy may be a guide (a prompt line) or
a sensor (a hook); the loop measures which. Finding 7: the transcripts.

## What has to change for the loop to see anything

- **Transcripts on disk.** `src/run_analysis.ask` keeps the last 20,000
  characters of stderr. It will run the session with `--output-format
  stream-json` and write every event to `.{accession}.logs/{agent}.jsonl`
  beside the run, outside the record, the result event read off the last
  line as the JSON result is read today. The loop greps them.
- **`src/improve/mine.py`**: the table above, from the manifests and the
  analyses, one row per run per agent. Judge: a test on two hand-written
  manifests.
- **`src/improve/measure.py`**: `tools/measure` of 2026-10-15, generalised —
  copies named runs outside the tree, reruns named agents k times with and
  without the edit, grades with `src.grade_run`, prints before/after with the
  baseline spread and the acceptance verdict. Judge: a test over stubbed
  agent calls with hand-chosen numbers on both sides of the rule.
- **`.claude/skills/improve/SKILL.md`**: the goal, the fences, the five steps
  by name, the budget. No detection rule, no remedy list. Under forty lines.
- **`.claude/hooks/guard_fences.py`** and the improve session's `--settings`.
- **`make improve`** and `.github/workflows/improve.yml` (workflow_dispatch;
  needs an API key in the repository's secrets, the owner's to add).
- **Budget**: `--max-budget-usd` on every nested session; `measure.py`
  refuses a plan whose estimated cost, from the manifests' per-agent cost,
  exceeds the cap the invocation names.

## Rules the loop keeps

- A remedy is accepted on measurement, never on the proposer's account of it.
- The proposer is told a verdict and the numbers; the held-out set is not
  named to it before measurement (finding 1: data chosen to expose exploits).
- A weakness the gates do not refuse is not a weakness the loop fixes: it is
  a gate gap, the owner's row. The first such row, 2026-10-16: after the
  write-time hook, the analysts write counts as words ("lowest of the six
  fiscal years") twice as often on FN; the gate reads digits only, so this
  stands, and whether a count in words is a number in the analyst's own words
  is the owner's call.
- When a model changes, the first pass is an ablation: each component in
  `components.md` off in turn, measured; a component that moves nothing is
  removed by its own pull request (finding 2).
- No composite score, no rank, no threshold written into Python that says
  "this many drops is a problem": the table says what happened, the model says
  what it means, the measurement says whether the remedy worked.

## Needs the owner

- the `fences` CI job and the `improve.yml` secret (`ANTHROPIC_API_KEY`), both
  guarded paths or the owner's settings: rows in `docs/needs_judgment.md`,
  default in force the session-level guard and chat or `make improve` as the
  entry points;
- whether a count written in words is a digit in the analyst's own words
  (`src/analysis_check.py` is a gate, the owner's);
- the budget per pass (default proposed: 60 USD at list price, about one
  company's analysts run four times).

## Build order

1. transcripts on disk · `mine.py` · `measure.py`, each with its test
2. the skill, the fences guard, the session settings, `make improve`
3. one pass by hand on the 2026-10-14 runs, its ledger and predictions committed
4. `improve.yml`, the owner's rows
