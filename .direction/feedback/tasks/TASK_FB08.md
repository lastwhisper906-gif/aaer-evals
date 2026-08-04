# TASK: FB-08 — CLAIMS.json: machine-readable claims ledger locked to RESULTS.md

## Mode hint
mode: default

## PRE-FLIGHT — read first

- INV-17 already satisfied by the orchestrator. DO NOT run `git fetch`;
  do not abort on its failure.

## Objective

EXT_FB_B item 11 asks for a machine-readable claims index (number → source
artifact → limitation → status) so an external reader has one structured
entry point. RESULTS.md already holds exactly this as a 13-row markdown
table (rows |1|..|13|). Produce CLAIMS.json as a faithful machine-readable
rendering of that table, plus a test that LOCKS it to RESULTS.md so the
two can never drift silently. RESULTS.md stays the human-readable
authority; CLAIMS.json is derived and the test enforces the derivation.

## Files in scope

- CLAIMS.json — create, repo root. Shape:
  {
    "generated_from": "RESULTS.md",
    "authority": "RESULTS.md is authoritative; this file is a locked
                  machine-readable rendering (tools/test_claims_ledger.py)",
    "scope": "<the RESULTS.md header scope sentence: single Claude-based
              pipeline, Claude-assisted human-finalized grading — verbatim>",
    "disclaimer": "<the repo-standard no-position/educational wording —
                   copy the README footer convention (INV-14)>",
    "claims": [ per table row:
      { "id": <int 1-13>,
        "task_tag": "<[T1]|[T2]|[Exploratory L4] as printed>",
        "measurement": "<Measurement cell, verbatim minus the task tag>",
        "published_value": "<Published number cell, verbatim>",
        "limits": "<Limits cell, verbatim>",
        "source_raw": "<Source cell, verbatim>",
        "source_paths": ["<each backticked repo path extracted from the
                          Source cell, trailing §/notes stripped>"],
        "status": "published" } ]
  }
  Verbatim = character-identical after collapsing internal whitespace
  runs to single spaces (markdown wrapping tolerance) and stripping
  markdown bold markers is NOT allowed — keep ** as-is (cells contain
  deliberate emphasis).
- tools/test_claims_ledger.py — create: parses the RESULTS.md table
  directly (split on | with escaping care; the table is regular) and
  asserts: (a) exactly 13 rows in both, ids 1..13 matching; (b) for every
  row, measurement/published_value/limits/source_raw in CLAIMS.json equal
  the markdown cells under the whitespace-collapse rule; (c) every entry
  in source_paths exists in the repo (files OR directories — entries like
  runs/holdout/ are dirs; strip trailing '/'); (d) every backticked
  path-like token (contains '/' or ends .md/.json/.csv) in each Source
  cell appears in that row's source_paths (no silently dropped source);
  (e) json.load succeeds and top-level keys are exactly the five keys
  shown in the shape block (generated_from, authority, scope, disclaimer,
  claims).

## Read-only / forbidden paths

- harness/, CLAUDE.md, AGENTS.md, PROJECT_INVARIANTS.md (always)
- RESULTS.md, RESULTS.ko.md, README*, REPRODUCING* — READ but never write
- schemas/ (no new schema file — the test is the shape gate), analysis/,
  runs/, forward/, scoring/, pipeline/, docs/, Makefile, tools/lint_*
  and every existing tools/ file

## Check command
check: ./.venv/bin/python -m pytest tools -q

## Acceptance criteria

1. CLAIMS.json exists at repo root with the exact top-level shape and 13
   claims whose text cells are verbatim (whitespace-collapse rule) from
   RESULTS.md.
2. The test parses RESULTS.md itself (not a copy) and enforces (a)-(e);
   deliberately corrupting one character of CLAIMS.json makes it fail
   (verify by reading the assertions).
3. Every source_paths entry exists in the working tree.
4. Check command passes; diff touches ONLY the two new files.

## Explicitly out of scope

- README/RESULTS restructure, prose changes, or linking CLAIMS.json from
  any doc (owner surface decision — orchestrator queues it).
- New Makefile targets or lint wiring (the pytest gate inside
  verify-public already runs tools/ tests).
- A JSON Schema under schemas/ (protected; the test is the gate).
- Translating or normalizing cell text beyond whitespace collapse.

## Notes / context

- MERGE PROTOCOL (for the build reviewer's information): the new test file
  changes the pytest collected count, so verify-public goes red at
  lint_doc_counts on the raw branch — this is expected and NOT a builder
  failure; the ORCHESTRATOR runs `make docs-refresh` at merge (established
  FB-04/06/07 precedent).

- INV-03 disclosure D-entry + owner-queue linkage authored by the
  ORCHESTRATOR at merge (incl. Q-F18 candidate: whether README links
  CLAIMS.json).
- The Source cells contain notes like "(signed D94)" and "§4" — those
  stay in source_raw; source_paths carries only existing repo paths
  (e.g. analysis/DECISION_TABLE.md).
