# aaer-evals — two frames over each company's raw filings: accounting (can these numbers be trusted?) and finance (how healthy is it, and what is it worth from free cash flow); every anomaly listed

Read: docs/INPUT_SPEC.md (what we fetch), docs/CHECKLIST.md (what we look at), docs/HOW_WE_WORK.md (who does what), queue.md (the work)

Rules (each names what enforces it; a rule naming nothing is a judgment the owner keeps; this file stays at 22 lines or fewer: src/instruction_length_check.py, make check)
- Plain names. No letter-number codes. Machine keys are readable slugs. An item id says what it looks at: its area, then its subject, letters and underscores only. (src/plain_name_check.py, make check; item ids: src/quote_gate.py)
- Append-only under runs/ · rules/ · events/ · history/ · evals/scoreboard.jsonl: existing content is never changed or deleted; appending to the end of a ledger file is allowed. A correction is a new file plus one ledger line. (src/append_check.py, make check)
- Text handed to the predictor is verbatim. No summaries. Commit the text the model saw. Every report item carries a verbatim quote or an upstream item id that Python verifies; a failed item is dropped and counted. (src/quote_gate.py; the committed inputs: src/agent_inputs.py)
- Python does the arithmetic. Agents read, judge and choose assumptions with verbatim quotes; every number an agent writes comes from calculator.json or companyfacts. No composite score, no rank across companies. (src/analysis_check.py)
- "Every company" means Python computes every metric wide and cheap, and agents read deep where they add something. The one bridge between the frames is the accounting analyst's adjustments, which Python applies to free cash flow. (src/calculator.py)
- Readers see filings. The accounting and financial analysts see reports and calculator.json, never prices; the valuation analyst adds MD&A and guidance paragraphs and the price at the cutoff. Nothing else crosses a layer. (src/agent_inputs.py, tests/test_agent_inputs.py)
- evals/ is the owner's evaluation code: Claude reads it and never writes it. A goal is met only by printed `make eval` output; analysts never grade themselves. (src/eval_guard.py in CI; .claude/settings.json denies the tools)
- An expected value comes from the source, never from the first run of the code it judges. The twelve companies test the pipeline, not the signal. (tests/expected_values.py refuses an unsourced value)
- Work with no judge (test, schema, check, eval) is not a task. Leave it as "needs judgment". (src/task_judge_check.py, make check)
- Never create a state that waits for the owner's signature. Proceed with the default and leave one line. (src/owner_inbox_check.py, make check)
- Cutoff: document filing date ≤ filing date of the triggering report. Nothing later enters the input. (src/cutoff_guard.py; tests/test_cutoff_guard.py fails a read that skips it)
- Ground truth is the first-reported value (the 8-K earnings release). Restatements are analyzed separately. (src/parse_8k.py, src/restatement_trace.py)
- Each prediction is scored against its own rules version. Rule changes apply from the next version. Never soften an adverse result. (src/scorecard.py; rules/ is append-only)
- Read lessons.md at session start (the SessionStart hook prints it; its cut, tools/session_start_lessons.sh, waits for the owner's label). Write this session's mistakes to lessons.md, one line each, at session end.
- Start long runs under `caffeinate -s` so a locked screen never stops them. The lock is harmless; system sleep is what halts the loop.

Success criterion: every published prediction is reproducible from its published inputs alone, every quote exists in those inputs, the inputs do not violate the cutoff, and every layer saw only what its directory held.
