# TASK: P1-04c — BN-18: English-canonical ERRATA.md (F-01/F-02), append-only preserved

## Mode hint
mode: inverted

## PRE-FLIGHT
- INV-17 satisfied by orchestrator; DO NOT run git fetch or abort on it.
- D-P50 #4 signed scope names ERRATA explicitly; BN-18's resolution
  condition prescribes exactly this design. NO English draft exists
  (verified) — this is a full translation of a 97-line ledger.
- ERRATA.md is protected + append-only (INV-06). The append-only
  property survives this design: ko file preserves the full original
  byte-exact; EN carries 1:1 translations of E-001/E-002; future errata
  append to the EN canonical only (both headers state this rule).

## Files in scope
- ERRATA.ko.md — create: byte-exact copy of current ERRATA.md + ONE
  leading blockquote line: "> 한국어 원본 (동결 스냅샷: E-001–E-002) —
  영어 정본: ERRATA.md (F-01/F-02, D-P50); 이후 정정 항목은 영어 정본에만
  추가된다."
- ERRATA.md — replace with full English translation:
  leading line ABOVE the H1: "> Korean original: [ERRATA.ko.md](ERRATA.ko.md)
  (frozen snapshot: E-001–E-002)." ; every numeric token identical
  (equivalence-locked); the header's append-only principle statement
  translated intact and EXTENDED with one sentence: future errata are
  appended here (English canonical); entry structure/ids (E-001, E-002)
  and all artifact paths byte-identical; INV-13/14 discipline (existing
  text compliant — no new vocabulary EXCEPT the following sanctioned
  additions, each marked with an HTML comment):
  (i) lint rule (D): the E-002 pooled-secondary mention MUST include the
  literal word "standalone" (e.g. "pooled secondary (alongside the
  standalone figures above)") — without it lint enrollment cannot pass;
  (ii) romanize rule, two pre-named sites: the §4 plan quote at ko line
  ~18 — the "이고" conjunction is the FINDING (romanize as *igo* = "and",
  gloss that the dropped conjunction is what E-002 corrects) — and the
  mandated disclosure sentence at ko lines ~50-53.
- tools/test_translation_equivalence.py — TRANSLATION_PAIRS += the
  4-tuple (marker = the ko leading line; en_truncate = None).
- tools/lint_publication.py — DOCS += "ERRATA.md" only (ko deferred,
  D-P55 reason pattern, one comment line).

## Read-only / forbidden paths
- harness/, CLAUDE.md, AGENTS.md, PROJECT_INVARIANTS.md; every other
  root/doc file; analysis/, runs/, scoring/, schemas/, BOTTLENECKS.md

## Check command
check: ./.venv/bin/python -m pytest tools -q && ./.venv/bin/python tools/lint_publication.py

## Acceptance criteria
1. EN complete (no Hangul outside HTML comments), E-001/E-002 1:1 with
   identical ids/paths/numbers (token-locked); ko byte-exact + one
   leading marker line.
2. Both headers state the future-append rule (EN-only appends).
3. Registry + DOCS extended; check passes; lint RC=0.
4. Diff touches ONLY the four listed paths.

## Out of scope
- Any change to E-001/E-002 substance; BN-18 flip (orchestrator);
  AUDIT_INDEX/README link text (paths unchanged).

## Notes
- MERGE PROTOCOL (orchestrator): docs-refresh; reader gate 2 personas;
  BN-18 flip + D-entry disclosing: BOTH protected paths touched
  (ERRATA.md at .protected-paths:45, tools/lint_publication.py at :38)
  under D-P50 signature; the append-only continuity design; AND that the
  frozen OWNER_FINAL_PACKET_2026-07-22.md E-002 byte-identity recipe
  (awk '/^## E-002/,0' + sha256) now reproduces against ERRATA.ko.md —
  the leading-marker placement keeps the E-002 byte range intact there.
