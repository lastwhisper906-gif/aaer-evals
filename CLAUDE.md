# aaer-evals — two frames over each company's raw filings: accounting (can these numbers be trusted?) and finance (how healthy is it, and what is it worth from free cash flow); every anomaly listed

Read: docs/INPUT_SPEC.md (what we fetch), docs/CHECKLIST.md (what we look at), docs/HOW_WE_WORK.md (who does what), queue.md (the work)

Rules
- Plain names. No letter-number codes. Machine keys are readable slugs. An item id says what it looks at: its area, then its subject, letters and underscores only.
- Append-only under runs/ · rules/ · events/ · history/ · evals/scoreboard.jsonl: existing content is never changed or deleted; appending to the end of a ledger file is allowed. A correction is a new file plus one ledger line.
- Text handed to the predictor is verbatim. No summaries. Commit the text the model saw. Every report item carries a verbatim quote or an upstream item id that Python verifies; a failed item is dropped and counted.
- Python does the arithmetic. Agents read, judge and choose assumptions with verbatim quotes; every number an agent writes comes from calculator.json or companyfacts. No composite score, no rank across companies.
- "Every company" means Python computes every metric wide and cheap, and agents read deep where they add something. The one bridge between the frames is the accounting analyst's adjustments, which Python applies to free cash flow.
- Readers see filings. The accounting and financial analysts see reports and calculator.json, never prices; the valuation analyst adds MD&A and guidance paragraphs and the price at the cutoff. Nothing else crosses a layer.
- evals/ is the owner's evaluation code: Claude reads it and never writes it. A goal is met only by printed `make eval` output; analysts never grade themselves.
- An expected value comes from the source, never from the first run of the code it judges. The twelve companies test the pipeline, not the signal.
- Work with no judge (test, schema, check, eval) is not a task. Leave it as "needs judgment".
- Never create a state that waits for the owner's signature. Proceed with the default and leave one line.
- Cutoff: document filing date ≤ filing date of the triggering report. Nothing later enters the input.
- Ground truth is the first-reported value (the 8-K earnings release). Restatements are analyzed separately.
- Each prediction is scored against its own rules version. Rule changes apply from the next version. Never soften an adverse result.
- Read lessons.md at session start (the SessionStart hook prints it). Write this session's mistakes to lessons.md, one line each, at session end.
- Start long runs under `caffeinate -s` so a locked screen never stops them. The lock is harmless; system sleep is what halts the loop.

Success criterion: every published prediction is reproducible from its published inputs alone, every quote exists in those inputs, the inputs do not violate the cutoff, and every layer saw only what its directory held.
