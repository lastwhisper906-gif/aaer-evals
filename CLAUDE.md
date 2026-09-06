# aaer-evals — read 12 companies' filings and predict accounting reliability and financial pressure separately

Read: docs/INPUT_SPEC.md (what we fetch), docs/CHECKLIST.md (what we look at), docs/HOW_WE_WORK.md (who does what)

Rules
- Plain names. No letter-number codes. Machine keys are readable slugs.
- Never edit or delete published files under runs/ · rules/ · events/. A correction is a new file plus one ledger line.
- Text handed to the predictor is verbatim. No summaries. Commit the text the model saw.
- Python does the arithmetic. The LLM judges text only.
- Work with no judge (test, schema, check) is not a task. Leave it as "needs judgment".
- Never create a state that waits for the owner's signature. Proceed with the default and leave one line.
- Cutoff: document filing date ≤ filing date of the triggering report. Nothing later enters the input.
- Ground truth is the first-reported value (the 8-K earnings release). Restatements are analyzed separately.
- Each prediction is scored against its own rules version. Rule changes apply from the next version.
- Never soften an adverse result.
- Read lessons.md at session start. Write this session's mistakes to lessons.md, one line each, at session end.

Success criterion: every published prediction is reproducible from its published inputs alone, every quote exists in those inputs, and the inputs do not violate the cutoff.
