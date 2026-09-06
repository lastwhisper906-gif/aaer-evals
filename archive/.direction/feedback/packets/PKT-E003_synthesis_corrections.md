# PKT-E003 — synthesis-layer published-artifact corrections
**STATUS: SIGNED & EXECUTED (owner verbatim "sign", 2026-08-06, D-P82).**
E-003 appended to ERRATA.md; artifacts regenerated; verify-public RC=0.

Two published-artifact defects found by the rotation-2 C1B component
review (full evidence: .direction/feedback/rot2_C1B_2026-08-05.md).
The CODE corrections are already committed (INV-03(c): revision commit
precedes any regeneration — this commit) with a divergence-lock test.
The ARTIFACT regeneration + erratum publication await your signature
(disclose-don't-revise; E-001/E-002 precedent).

## Defect 1 (C1B-01): analysis/unified_table.csv m_flag inverted
Every m-scored row of the published 65-row cross-wave table carries
`int(m <= -1.78)` where the frozen rule (screens.py flag_minus_1_78,
baseline_screens.md, baselines.py→baseline_table.csv) is `m > -1.78` —
exact complement, all rows wrong. Companion doc synthesis.md:76 wrote the
defect down rather than catching it.

## Defect 2 (C1B-02): analysis/synthesis.json wave-1 fraud_median 60.0 → 57.5
`sorted(fr)[len(fr)//2]` = upper-middle element; wave-1 fraud n=8 is the
repo's only even group. True median of the eight scores: 57.5.
control_median 33.0 numerically unaffected (tied middles). Wave-2/holdout
odd-n groups unaffected; AUC/CI fields unaffected (median not used).

## Draft ERRATA entry (E-003 — you may edit tone; ids/numbers verified)
### E-003 — P2 synthesis layer: unified_table m_flag inversion + wave-1 median estimator (2026-08-05)
- 발견: rotation-2 component review (adversarial replenish, D-P70).
- 결함 1: unified_table.csv의 m_flag가 동결 규칙(m > -1.78)의 정확한
  보수(complement)로 계산됨 — m_score 보유 전 행 반전. RESULTS 행 12의
  AUC·상관·p는 baseline_table.csv 소스라 무영향.
- 결함 2: synthesis.json wave-1 fraud_median 60.0 — 짝수 n 중앙값
  추정자 오류(상위 중앙 요소). 참값 57.5. 다른 웨이브·다른 필드 무영향.
- 조치: 코드 수정 커밋 <this commit> (m_flag 규칙 3개소 + statistics.median)
  + 발산 방지 테스트(analysis/test_synthesis_flag_convention.py) 선행;
  본 항목 서명 후 unified_table.csv·synthesis.json 재생성(신규 병행
  게시 — 원본은 git 이력 보존). 게시 표면 중 60.0을 인용하는 곳:
  <owner verifies: grep -rn "60.0" README* RESULTS* analysis/*.md>.

## Exact commands after signature
  .venv/bin/python analysis/synthesis.py           # regenerates both artifacts
  make docs-refresh && make verify-public          # gates
  # append the signed E-003 text to ERRATA.md (English canonical)
  # + ERRATA.ko.md stays frozen (snapshot note covers)
