# TASK: FWD — forward-tool fail-closed hardening (PKT-FWD, owner-signed D-P83)

## Mode hint
mode: default

## PRE-FLIGHT
- Owner signature 2026-08-06 (D-P83) converted PKT-FWD into this task.
- Full evidence: .direction/feedback/rot2_C1B_2026-08-05.md (C1B-03/04/05).
- Protected prefix tools/forward_ — signature covers exactly these three
  S-sized fail-open→fail-closed conversions, each with a test. No other
  forward/ contact. Timing: before ANY cycle_002 preparation.

## Required changes
1. forward_validate: enforce the FULL sealed-spec §6 record contract
   (currently a subset) + correct spec §4's false mechanism sentence.
2. forward_prepare: post-seal guard on PROTOCOL.md writes; fail-closed on
   pin-source drop and UNRESOLVED model pin.
3. forward_enumerate: fail-closed on fetch failure; bounded trailing
   window (fetch-date-independence for cycle_002).

## Check command
check: ./.venv/bin/python -m pytest tools/ -q -k "forward" && ./.venv/bin/python tools/lint_publication.py

## Acceptance criteria
1. Each of the three conversions has a test proving the fail-closed branch.
2. No behavior change on the happy path (existing forward tests green).
3. INV-22 untouched — no cycle_002 artifacts created.
