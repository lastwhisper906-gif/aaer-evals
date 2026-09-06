# TASK: NB-03 — cross-model GPT runner (subscription Codex CLI) + tests, NO live calls

## Mode hint
mode: default

## PRE-FLIGHT — read first
- INV-17 already satisfied by the orchestrator. DO NOT run `git fetch`;
  do not abort on its failure.
- INV-12 now carries a signed exception (PROJECT_INVARIANTS.md, D-P48)
  permitting exactly this: subscription-Codex GPT pass over frozen
  retrospective cases, outputs to runs/crossmodel_gpt/ only.

## Objective

Build (but do NOT run) the cross-model evaluatee runner: same frozen
cases, same task text, same output schema as the Claude pipeline, but the
model call goes through `codex exec` (ChatGPT subscription — zero-metered,
INV-20). Purpose: empirical test of limitation L-6 (same-family grading
leniency) and the single-model scope limit. THIS TASK SHIPS CODE + TESTS
ONLY — the live tranche is launched separately by the orchestrator.

## Design contract

1. FROZEN-FRAME PAYLOADS: the published Claude runs saw pre-FB-01
   payloads that included two marker keys. For comparability the GPT arm
   must see byte-equivalent user_payload text. FB-01/FB-02 did not change
   payload CONTENT (same case/series/chronology values; FB-02 only added
   an assert), so reconstruct exactly:
     frozen = {"variant": payload["_variant"],
               "perturb_factor_recorded_scoring_side_only": None,
               **{k: payload[k] for k in ("case",
                  "financial_series_point_in_time", "filing_chronology")}}
     user_payload = json.dumps(frozen, ensure_ascii=False)
   (matches the pre-FB-01 dict insertion order: variant, perturb_*, case,
   series, chronology). FROZEN-FRAME comment must cite: eafc32b (the
   pipeline_version recorded in the frozen runs) and the byte-identical
   reconstruction basis, plus L-9 with the precision note that the code
   at eafc32b had the perturb-marker key in BOTH arms (value None) — code
   is the authority over L-9's "perturbed arm additionally" prose. The
   marker leak is knowingly reproduced for input parity; "frame":
   "frozen_v1_markers" goes in the sidecar metadata.
2. TASK TEXT: reuse runner.TASK verbatim via import (same .format call
   with company_name/ticker/cik_part/cutoff_date; cik included only for
   the original arm, mirroring runner.py:120-122).
3. CALL: subprocess `codex exec --sandbox read-only --cd <TEMP DIR
   OUTSIDE THE REPO>` (tempfile.mkdtemp; INV-19 isolation — codex must
   NOT get the repo as cwd). ISOLATION PARITY (the Claude arm blocked
   config/hooks/MCP/tools and replaced the system prompt —
   cli_client.py:199-211; codex has NO such defaults): inspect
   `codex exec --help` OFFLINE and apply the strongest available
   equivalents — config overrides that disable MCP servers and
   instruction-file loading (~/.codex/config.toml MCP + global AGENTS.md
   must NOT reach the model), and capture the `codex exec --json` event
   stream per case as an audit log stored next to the sidecar meta. A
   TEST must assert the isolation flags appear in the constructed
   command. The module docstring DISCLOSES residual gaps (read-only
   sandbox can still read the disk, incl. scoring/ — mitigation: audit
   log + empty temp cwd + prompt contains only the payload) as a stated
   limitation. Prompt = task text + instruction to output
   ONLY a JSON object conforming to the model schema (no prose, no
   fences) + the user_payload. Validate response against runner
   MODEL_SCHEMA with Draft7Validator + FormatChecker; ONE retry on
   parse/validation failure with IDENTICAL input (no schema coaching —
   the Claude arm never received error feedback; record the retry count
   and this asymmetry note in the sidecar meta and docstring); then FAIL
   the case (recorded, not raised).
4. GUARDS: (a) cli_client.guard_payload(user_payload, EVALUATEE_FORBIDDEN
   _MARKERS) before every send (import — value-level canary/answer scan);
   (b) refuse to run if ANTHROPIC_API_KEY/OPENAI_API_KEY/GEMINI_API_KEY/
   GOOGLE_API_KEY set (INV-20, mirror run_task.sh guard);
   (c) refuse if output dir is not under runs/crossmodel_gpt/ (the D-P48
   separated path).
5. PROVENANCE — schema facts (verified): FULL_OUTPUT_SCHEMA has
   `additionalProperties: false` at top level and fingerprint is OPTIONAL
   — so NO in-record `crossmodel`/`frame` keys are possible. Prescribed
   envelope: write a FULLY v1-conformant record (all required keys:
   case_id, run_id "xgpt-<frame>-<cid>-r1", model = the codex-reported
   model string (or the honest literal "model_string_unavailable" — never
   guess), pipeline_version = git HEAD, run_timestamp, documents_used,
   checklist, misstatement_probability, mechanism_hypotheses, overall)
   PLUS a fingerprint dict built BY THIS MODULE with codex-native values
   (model_requested = codex model string/fallback, harness_version_actual
   = `codex --version` output, prompt_sha256, payload_sha256) — do NOT
   call runner.compute_fingerprint (it hardcodes the Claude pin and
   claude --version: misleading provenance). `frame`/`crossmodel`/audit
   markers go in a per-case SIDECAR meta JSON (runmeta_* pattern from
   runner.py). Design point 7's "validates" = against FULL_OUTPUT_SCHEMA.
   The dry-run prompt/payload sha256s are ALSO written into run metadata
   at live-run time — the first recorded payload-hash baseline (no frozen
   run recorded one).
6. CLI: --cases (default: same registry as runner.py), --only, --frame
   {original,perturbed} (tranche 1 = original), --out (must be under
   runs/crossmodel_gpt/), --limit N (tranche control), --dry-run (build
   payloads + guards + prompts, print sha256s, NO codex call — the
   orchestrator uses this for the launch preflight). Concurrency 1
   (sequential — quota-gentle, simplest failure semantics).
7. Idempotency: skip if output exists and validates (this path has no
   fingerprint discipline; existing-file skip is enough for tranches).

## Files in scope

- pipeline/crossmodel_gpt.py — create (name chosen to avoid the
  protected `pipeline/runner` prefix).
- pipeline/test_crossmodel_gpt.py — create: ALL codex calls mocked
  (monkeypatch subprocess). Tests: (a) frozen-frame reconstruction is
  byte-stable and key-ordered as specified (golden string for the
  synthetic fixture); (b) guard refusal on metered env var (monkeypatch
  os.environ); (c) out-dir enforcement refuses paths outside
  runs/crossmodel_gpt/; (d) invalid-JSON response → one retry → FAIL
  recorded without exception; (e) valid mocked response → output file
  written with all provenance fields and validates per the chosen
  envelope; (f) --dry-run makes zero subprocess calls (assert mock not
  called) and prints prompt/payload sha256s; (g) temp cwd for codex is
  outside the repo (capture the --cd arg from the mock).

## Read-only / forbidden paths
- harness/, CLAUDE.md, AGENTS.md, PROJECT_INVARIANTS.md (always)
- pipeline/runner.py, runner_api.py, cli_client.py, build_payload.py,
  cutoff_guard.py, date_shift.py, probe_runner.py — IMPORT-ONLY, no edits
- schemas/ (zero edits — see design point 5), runs/ (no writes from
  tests — everything via tmp_path), analysis/, scoring/, docs/, README*

## Check command
check: ./.venv/bin/python -m pytest pipeline -q

## Acceptance criteria
1. Design points 1-7 implemented as specified; module docstring documents
   the envelope choice and the frozen-frame rationale (L-9 citation).
2. Tests (a)-(g) pass with zero real codex invocations (verify: grep the
   test file for subprocess mocking; check command passes offline).
3. No edits outside the two new files; imports only from the listed
   pipeline modules.
4. The runner physically cannot write outside runs/crossmodel_gpt/ (test c).

## Explicitly out of scope
- Any live codex call (orchestrator launches tranche 1 separately).
- Scoring/analysis of GPT outputs, publishing numbers (owner-gated).
- Gemini, API-key paths, new deps, schema edits.

## Notes / context
- INV-03 disclosure + manifest/gate handling at run time is the
  orchestrator's job. MERGE PROTOCOL: docs-refresh at merge as usual.
- Quota note: sequential, tranche-limited (--limit); quota exhaustion at
  run time = SAFETY HALT per loop rules (not this task's concern).
