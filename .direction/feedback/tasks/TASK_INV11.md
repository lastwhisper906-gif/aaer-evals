# TASK: INV11 — dev-toolchain wiring (PKT-INV11, owner-signed D-P83)

## Mode hint
mode: default

## PRE-FLIGHT
- INV-11 exception registered (PROJECT_INVARIANTS.md, commit 6f04e2e).
- pip-compile needs network: run ONLY in an owner-attended session (INV-23)
  — if unattended, do every other step and leave the lock generation queued.

## Required changes
1. requirements-dev.in (ruff, mypy OR pyright, pytest-cov, pip-audit) +
   requirements-dev.lock via pip-compile --generate-hashes (owner-attended).
2. ci.yml additive "quality" job — continue-on-error initially, failures
   visible (no silent green, INV-24); canonical 3.12 5-gate job UNCHANGED.
3. tools/test_no_dev_toolchain_import.py — guard scan: pipeline/ scoring/
   analysis/ must not import the dev toolchain.

## Check command
check: ./.venv/bin/python -m pytest tools/test_no_dev_toolchain_import.py -q && ./.venv/bin/python tools/lint_doc_counts.py

## Acceptance criteria
1. Canonical CI job diff = zero lines.
2. Guard test fails-closed on a planted violation (demonstrated in test).
3. requirements.txt / requirements.lock untouched.
