# METHOD.md — Pipeline method (one page, readable without the ledger)

> Authored by Claude Code, pending human audit (GA-001 (b)). Zero new claims —
> every paragraph carries its repository source path as an HTML comment. For
> the detailed audit trail, see `AUDIT_INDEX.md`.
> Korean original: [METHOD.ko.md](METHOD.ko.md).

## Execution path (the road one case travels)

<!-- source: pipeline/build_payload.py -->
**1. Payload assembly.** Per-case point-in-time inputs (XBRL financial time
series + EDGAR filing history) are assembled by deterministic code. The
perturbed frame that hides company identity removes names, tickers, and CIKs
and rescales amounts (limit: the v1 frame retains accession numbers and filing
chronology — partial de-anonymization; README post-publication disclosure
section).

<!-- source: pipeline/cutoff_guard.py -->
**2. Cutoff guard (fail-closed).** All raw-data loading passes through a
single guard module. Raw SEC files may contain post-cutoff data, as expected;
bulk loaders explicitly drop those rows and log retained and dropped counts.
Each fact's date is checked against the case cutoff date, and filed documents
are cross-validated against the filingDate in the EDGAR filing history. At
`build_payload` assembly, the completed payload is re-scanned and any
surviving post-cutoff date raises `CutoffGuardError` (fail-closed).
Single-document loads (`load_document`) retain their raise-on-violation
behavior. Bypass code is forbidden by a scan test.

<!-- source: pipeline/cli_client.py -->
**3. Isolated single call.** Each evaluatee call is one subscription headless
`claude -p` invocation executed in a temporary directory outside the
repository. Settings, hooks, MCP, and built-in tools are fully disabled by
flags, the system prompt is replaced, and the payload is scanned at value
level for answer-key and canary markers before sending (on a hit, the call
never happens). The serving-model pin and the harness-version pin are
verified and recorded per call.

<!-- source: schemas/llm_output.json, pipeline/cli_client.py -->
**4. Schema-forced output (bounded retry).** Output is forced through a JSON
schema; a schema failure or empty response is retried exactly once with
identical input, then recorded as FAIL. No prompt contains an open-ended
question ("does this company look suspicious?") — checklists and structured
fields only.

<!-- source: tools/memo_verify.py, tools/blind_memo_verify.py -->
**5. Deterministic quote verification.** Verbatim quotes in model output are
re-confirmed against the source filings by deterministic string comparison.
Unverifiable quotes do not pass — they go to the adjudication queue.

<!-- source: scoring/overrides.md, docs/OWNER_QUEUE.md -->
**6. Human adjudication queue.** Non-VERIFIED quotes, grading judgments, and
publication decisions are loaded into the owner queue in
options/rationale/default format and are never resolved without a signature.

## Leakage threat model

<!-- source: pipeline/cutoff_guard.py, scoring/threat_model.md -->
**Look-ahead** — post-cutoff data mixed into inputs. Defense: the single
guard path of §2 + fail-closed behavior + the guard-bypass scan test. <!-- source: pipeline/cli_client.py -->
**Answer leakage** — grading-side secrets (answer keys, perturbation
coefficients, identity maps) exposed to the evaluatee. Defense: pre-send
value-level marker scan (including a tamper-injection test) + physical
separation of pipeline/ and scoring/. <!-- source: analysis/synthesis.md, docs/V1_PARTIAL_DEIDENTIFICATION_NOTE.md -->
**Memorization** — the model knowing case outcomes from training data. It
cannot be blocked, only measured: disclosed measurement via three
instruments — the name-ID probe (50%→21.9%→0%), the outcome-recognition
probe (wave-2 8/9), and the post-cutoff holdout (the structurally impossible
axis).
<!-- source: tools/verify_blindness.py -->
**Canaries** — all runs/ are scanned for grading-material GUIDs appearing in
evaluatee artifacts (an appearance is an immediate FAIL). The same gate also
machine-verifies the criteria-precedence history proof (criteria commits
precede score commits).

## Role-separation contract

<!-- source: PROJECT.md §5·§7 -->
**Python computes, the LLM judges qualitatively only, and a human signs.**
All numeric computation (baselines, statistics, tests) is deterministic
Python. The LLM handles only qualitative judgment with verbatim quotes
forced, and its graded output is not signable without adjudication grounds.
Final confirmation is human-signature only — a model from the same family as
the evaluatee cannot unilaterally finalize its own report card (same-family
leniency is disclosed as limitation L-6).

<!-- source: README.md Limitations -->
This document is a method summary and contains no performance claims. All
numbers live in `RESULTS.md` (with row-level limits alongside); the audit
trail is in `AUDIT_INDEX.md`. All results are scoped to a single Claude-based
pipeline.

Multiple-testing family classification and Holm adjustment are documented in
`docs/MULTIPLE_TESTING.md`.
