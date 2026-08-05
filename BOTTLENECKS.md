# BOTTLENECKS.md — 현재 막혀 있는 것 (direction-loop 판단 기반 문서)

> 형식: `### BN-xx:` — **Blocked**(무엇이 막혀 있나) / **Blocks**(그래서
> 무엇이 진행 불가인가) / **Resolution condition**(측정 가능한 해소 조건) /
> **Basis**(근거). 해소된 항목은 삭제하지 않고 `RESOLVED (날짜, 근거)`를
> 붙여 하단으로 이동한다.

### BN-01: 궤적 레이어 — 단독 LLM 임계의 지배 전략 부재 (오탐 71.4%)
**Blocked:** E2 궤적 레이어의 발행 가능한 판정 규칙. T≥50은 탐지
12/12이나 오탐 5/7=71.4% CP95 [29.0%, 96.3%]; T=70은 오탐을 잡는 대신
탐지가 1/12로 죽는다. 오탐 0/7인 결합 규칙(B3≥2 AND llm_p≥T)은 사후
규칙이라 소급 인용 불가.
**Blocks:** 궤적 레이어를 검증된 신호로 쓰는 모든 후속(2단계 현재 기업
스크리닝의 궤적 축, G0). 결합 규칙의 지위 승격은 Cycle-2 sealed 전향
검증 전까지 불가.
**Resolution condition:** Cycle-2에서 결합 규칙이 사전 등록·봉인된 뒤
전향 결과로 평가됨 — 등록 문서가 seal 커밋에 포함되고, 사이클 마감 후
해당 규칙의 전향 탐지/오탐 수치가 산출되면 해소.
**Basis:** RESULTS.md 행 13 · `analysis/DECISION_TABLE.md` §4 (서명 D94) ·
`docs/FUTURE_CYCLE_PROTOCOL.md`

### BN-02: 첫 forward seal — 소유자 발사 게이트 미서명 + 선행 수동 항목
**Blocked:** cycle_001 봉인(목표 2026-11-15).
`forward/cycle_001/OWNER_LAUNCH_GATE.md` §6 체크리스트 4항목 전부 미체크
(§1 인지 2건 확인 · Q-O08 해석 확인 · screener S-01/S-03 완료 · 11월 창
발사 승인). seal 타임스탬프 앵커 사슬의 전제인 screener SEC User-Agent
(S-01)와 GitHub 원격 push(S-03)가 소유자 수동 대기.
**Blocks:** 첫 전향 봉인 전체 — 그리고 BN-01의 해소 경로(Cycle-2는 첫
seal 이후).
**Resolution condition:** OWNER_LAUNCH_GATE §6 네 박스 전부 체크 + 서명
기록, `tools/forward_seal.py` 실행과 seal 커밋·태그 존재.
**Basis:** `forward/cycle_001/OWNER_LAUNCH_GATE.md` §6 ·
`docs/OWNER_QUEUE.md` 레버리지 2·3

### BN-03: 하네스 핀 불일치 — 다음 실 피평가자 호출 차단 상태
**Blocked:** 실 모델 호출 전부. 핀 2.1.201 vs 실측 CLI 2.1.216 불일치로
`enforce_harness_pin`이 fail-closed 차단 중. 소유자 결정 Q-O11 (C):
차단 상태를 무해하게 유지하고, 11월 실행 창에서 FREEZE_REV 핀 개정 +
재핀 1회로 해소한다 (지금 박아도 11월까지 재표류 확실하다는 근거).
**Blocks:** 실행 창 전의 어떤 라이브 파이프라인 호출도 불가(의도된
상태) — 단, 창에서 FREEZE_REV 개정을 빠뜨리면 발사 자체가 막힌다.
**Resolution condition:** 실행 창에서 FREEZE_REV 신규 문서로 핀 개정 →
`pipeline/cli_client.py` 핀 대조 통과 → PROTOCOL 재핀 1회 완료.
**Basis:** `docs/OWNER_QUEUE.md` Q-O11 (RESOLVED 2026-07-22, D113 ③) ·
`governance/SUPERSESSION_CYCLE001_REPIN_2026-07-22.md` 주의 절

### BN-04: 소유자 수동 게시 4종 + 독자 발송 — Tier-3 가치 검증 0점 상태
**Blocked:** ① Issue #4 게시(GIL 메모) ② RP-18 코멘트(Issue #2) ③ Issue
#1/#3 편집(RP-15/16 반영) ④ 독자 발송 5–10명. 전부 텍스트 동결·명령 준비
완료, 소유자 실행만 대기.
**Blocks:** 3층 가치 검증(PROJECT.md §9 — "몰랐던 것" 응답 수집은 발송
없이는 0점) · P3 외부 감사 패킷(발송 전 착수 금지로 명시적 게이트) ·
게시 URL의 후속 D-엔트리 기록.
**Resolution condition:** 게시 4종의 URL이 D-엔트리로 기록되고, 발송
독자 수 ≥5.
**Basis:** `docs/OWNER_QUEUE.md` 레버리지 1 · `docs/HANDOFF.md` 게시 절차 ·
`docs/POST_FORWARD_BACKLOG.md` P3

### BN-06: DOI 미발급 — 인용 경로 미완결
**Blocked:** `CITATION.cff`의 DOI 필드 (Q-R03 — Zenodo vs release 경로는
확정, 소유자 계정 실행 대기).
**Blocks:** 외부 인용의 영구 식별자 — 발행물의 검증가능성 주장(진짜
가치 4기준 ④)의 마지막 조각.
**Resolution condition:** DOI 발급 + `CITATION.cff` 반영 커밋.
**Basis:** README.md Licensing 절 (DOI pending Q-R03) ·
`docs/OWNER_QUEUE.md` 12

### BN-07: 재현 경로의 shallow-clone 취약성 — 이력 증명이 전체 git 이력 전제
**Blocked:** 제3자 재현 주장의 견고성. `tools/verify_blindness.py`의
기준-선행 증명(INV-07)은 `git merge-base --is-ancestor`로 커밋 SHA 이력을
대조한다 — shallow clone(`--depth 1`, GitHub actions/checkout 기본값
fetch-depth 1 포함)에서는 대상 SHA가 로컬 이력에 없어 검사가 실패하거나
오판정한다. REPRODUCING.md의 재현 명령(`git clone <repo>`)은 full-clone
요구를 명시하지 않는다.
**Blocks:** 외부 감사자의 blindness 게이트 재현 — README "auditable"
주장의 실측 경로. 얕은 클론으로 시도한 첫 외부 재현자가 원인 불명
실패를 만나면 신뢰 비용이 발생한다.
**Resolution condition:** verify_blindness.py가 shallow clone을 감지해
명시적 fail-closed 메시지를 내고, REPRODUCING.md가 full-clone 전제를
명시하며, full clone·shallow clone 각각에서 동작이 실측 확인됨.
**Basis:** `tools/verify_blindness.py` check_history · REPRODUCING.md
재현 명령 절

### BN-05: R3 산입 규칙 미규정 — RESOLVED (2026-07-29, D116)
**Blocked (당시):** 교란 draw가 없는 실험군 케이스의 R3 산입 처리 —
분자에서 제외되며 분모(n_treatment)에는 포함되는 현행 동작(v1=rev2
동일)이 `analysis/ANALYSIS_PLAN_WAVE2.md`에 규정되어 있지 않았다. E-002가
"차기 계획 개정 시 명시적으로 규정할 것 (소급 변경 금지)"로 플래그.
**RESOLVED:** `docs/FUTURE_CYCLE_PROTOCOL.md` 부록 A-3에 전향 전용으로
명문화(소유자 서명 D116) — 관할은 차기 사이클 측정 절차이며 소급 개정
아님. 차기 ANALYSIS_PLAN 개정본이 이 규칙을 계승 명문화한다.
**Basis:** ERRATA.md E-002 "차기 계획 개정 플래그" 절 ·
`docs/FUTURE_CYCLE_PROTOCOL.md` 부록 A-3 · `scoring/decisions_log.md` D116

### BN-08: README 첫 화면 첫 방문자 전환 — RESOLVED (2026-07-29, D120)
**Blocked (당시):** DIRECTION_CONTEXT의 분기 성공 조건 "a README that
survives 90 seconds" — README 첫 화면에 figure 0장.
**RESOLVED:** wave-1 30사 dot plot이 README 첫 화면에 삽입됨 — 실측
증거: `analysis/fig_dotplot_30firms.png`(git-tracked) 참조가
README.md:46, `## Quickstart`(:56)보다 위. `make verify-public` RC=0
(lint_publication PASS · lint_doc_counts PASS · pytest 279 passed) —
해소 조건 3종 동시 충족. 커밋 874b025(루프 0cfc80e cherry-pick, 소유자
채택). 소유자 서명 D120.
**Basis:** README.md:46 · `scoring/decisions_log.md` D120 · vp2 게이트
로그 (verify-public RC=0)

### BN-10: ENGINE_DECISION v2 (FPR-matched comparison + control expansion) is doctrine-cited but exists in no file
**Blocked:** The owner-mandated sole path for engine changes and control widening — DIRECTION_CONTEXT cites "ENGINE_DECISION v2" as pre-registered, but specs/ENGINE_DECISION.md contains no v2, no FPR-matching clause, no expansion clause
**Blocks:** Claimable resolution of BN-01 — with n=7 controls, CP95 upper stays 41% even at 0/7 false positives, so no Cycle-2 forward result can support any FP claim until a signed v2 registers the widened control set and FPR-matched readout
**Resolution condition:** Owner packet exists containing a v2 draft (FPR-matching readout rules + control-expansion selection protocol + post-E2 history-disclosure section per PROJECT.md §5-6) and owner signature is recorded in the D-ledger before Cycle-2 registration
**Basis:** specs/ENGINE_DECISION.md

### BN-11: The README headline's sole evidence link (analysis/DECISION_TABLE.md) is Korean-only — D114 English-surface boundary unapplied at its most load-bearing click
**Blocked:** Target-audience readability of the headline finding's evidence
— README.md:26 sends practitioners and academics to a Korean-throughout
signed table with no English counterpart. (Owner re-entry D125: the H25
repackaging filter rejected the original candidate on a basis-token
mechanism artifact, not on substance.)
**Blocks:** The quarter goal "headline evidence documents in English /
audit-ready but unread fails this quarter" — both simulated non-Korean
readers stop at the first click off the headline.
**Resolution condition:** English canonical DECISION_TABLE with preserved
.ko.md original (F-01/F-02 protocol), numeric token-equivalence check
PASS, owner-adopted on main, and lint_publication DOCS extended to both
files.
**Basis:** analysis/DECISION_TABLE.md

### BN-12: Published figures outside the machine-check perimeter — RESOLVED (2026-08-05, D-P52)
**RESOLVED:** condition met under owner direction D-P50 #3 — fig_dotplot
axis label and threshold annotation now ordinal-convention ("Evaluatee risk
score (0-100, ordinal)", "T=50"), PNG regenerated; drift gate
`tools/verify_figures.py` wired as an additive verify-public line comparing
recomputed vs committed semantic sidecars (data sha256 + labels +
annotations), figures also re-render inside the pytest gate. Honest scope:
2 current-generation figures gated; 3 legacy companions excluded with
semantic reasons (reliability = probability-hypothesis instrument;
memorization figures label-clean); committed PNG bytes attested by
same-run convention + git review, not machine-compared.
**Blocked:** A trustworthy figure layer — no gate in verify-public/CI regenerates or compares any of the 4 published PNGs, and fig_dotplot's committed axis label "Misstatement probability" contradicts the ordinal-only publication convention (Q-F04/D91, RESULTS row 11) on the README first screen
**Blocks:** Publication-surface integrity — the ordinal lint and INV-05 gates cover text only, so figure drift or terminology violations ship silently (the standing suspicion "static review passes figure generation" instantiated)
**Resolution condition:** README-referenced figures regenerate from committed artifacts with ordinal-convention labels and a gate step fails on drift, with make verify-public RC=0 after wiring
**Basis:** analysis/fig_dotplot.py:40


### BN-09: L-6 교차 채점자 부채 — RESOLVED (2026-07-29, D122)
**Blocked (당시):** 채점 신뢰성 주장의 독립성 정량화 — 교차 패밀리
채점자가 스펙만 존재, 합의율 실측 0.
**RESOLVED:** D121 재규정 조건(소유자 패킷 준비 3종) 충족 실측 —
① SPEC 확정 문서 `docs/CROSS_GRADER_OWNER_PACKET.md`(스프린트 커밋
5594c44, 병합 42fedf3), ② 채점 대상 선정 프로토콜 동 패킷 수록,
③ 호출-비활성 스켈레톤 `tools/cross_grader_skeleton.py` — 단독 실행
RC=2 "CALLS DISABLED" fail-closed, `requests|urllib|http` 임포트 0건,
전용 테스트 4건이 pytest 283에 편입. GPT/Gemini 호출 경로 무추가
(INV-12·INV-20 무개정 존치). H26 BNFLIP-09 패킷 경유, 소유자 서명 D122.
실제 타 계열 호출·합의표 게시는 여전히 루프 밖 소유자 실행 전용(Q-F07).
**Basis:** `docs/CROSS_GRADER_OWNER_PACKET.md` ·
`tools/test_cross_grader_skeleton.py` · `scoring/decisions_log.md` D122

### BN-13: E-001's blind spot is still open — published numbers beyond wave-1 sit outside the recompute gate
**Blocked:** Machine-verified provenance of RESULTS rows 3/6/9/10/13 (including the headline 71.4%) — verify-public recomputes only RP-05/wave-1 numbers, while wave2_results.json, holdout_controls_results.json, and decision_table.json are trusted as-is (lint_publication rule F cross-reads them; nothing recomputes them from the committed runs/ scores and e2_trajectories.json, and even verify-full omits wave2_analyze.py)
**Blocks:** The README/CLAIM_HIERARCHY Level-0 claim "recomputes every published number from committed artifacts" at exactly the artifact class where the project's own errata (E-001/E-002) found real plan-deviation defects — silent drift or a regenerated-JSON error in the wave-2/holdout/E2 numbers would pass all 5 gates green
**Resolution condition:** A verify-public step (reproduce_analysis extension or dedicated pytest) recomputes the wave-2 separation stats, holdout-controls numbers, and decision-table cells from committed runs/ artifacts and analysis/e2_trajectories.json (seeds per E-002), fails on mismatch with the published JSONs, and make verify-public exits RC=0 after wiring
**Basis:** tools/reproduce_analysis.py

### BN-14: The limits half of the evidence chain is Korean-only — the limitation ledger every honest-scrutiny click resolves to
**Blocked:** Non-Korean reader access to docs/methodology_limitations.md (L-1…L-8 — the target of AUDIT_INDEX's L-N row, README_DETAIL's L-1/L-5 citations, and RESULTS row 8/9 limit language) and to analysis/error_analysis_wave2_holdout.md (RESULTS row 9's source column) — the claims half of the chain is now English, the limits half is not
**Blocks:** The quarter goal "readable by its target audience" on the academic-scrutiny path — the reader verifying "residual memorization is measured, not eliminated" hits a Korean wall one click below RESULTS, leaving the D114 boundary (all reader-facing docs English-canonical) unapplied to the very docs that carry the project's honesty differentiator
**Resolution condition:** English-canonical methodology_limitations.md (and the row-9 source doc) with .ko.md originals preserved per the F-01/F-02 protocol, numeric token-equivalence check PASS, lint DOCS lists extended to the new pairs, owner-adopted on main with verify-public RC=0
**Basis:** docs/methodology_limitations.md


### BN-15: The Nov-15 seal window's pre-seal steps run on unwritten or never-executed code — in-window authoring risk under the abort discipline
**Blocked:** A pre-verified offline execution path for OWNER_LAUNCH_GATE §4 steps (1)–(3) — the forward case-build script is unwritten (build_evaluatee_inputs.py has no forward parameterization; the gate schedules "파라미터화, 커밋 후 실행" inside the window) and the claimed forward_enumerate --offline determinism recheck has zero pytest coverage
**Blocks:** Low-risk cycle_001 sealing — any in-window tooling failure converts to INV-22 abort (no silent extension), slipping the calendar-critical seal and with it BN-01's sole resolution path
**Resolution condition:** Committed offline pytest proves (i) forward_enumerate --offline recomputes universe.json matching the pinned sha256 and (ii) a committed forward case-build path emits a schema-valid cases_forward_001-shaped file from a synthetic fixture, with make verify-public RC=0
**Basis:** tools/forward_enumerate.py

### BN-16: verify-public's zero-external-data property rests on a stale one-time transcript, not a gate — the named static-review blind spot on the project's most load-bearing reproduce claim
**Blocked:** Continuous machine proof of the README Quickstart claim "no corpus, no API key, no network" — sole evidence is the 2026-07-22 clean-HOME transcript recorded at the 279-test state while the suite is now 289 and growing
**Blocks:** Reproduce-promise integrity — a new test or tool that silently reaches network, ~/aaer-data, or HOME passes all 5 gates green while falsifying the README sentence auditors act on first
**Resolution condition:** make verify-public runs under a machine-enforced no-network/no-corpus guard that fails the gate on any socket or out-of-repo data access, and exits RC=0 with the guard active
**Basis:** audit/verify_public_sandbox_transcript_20260722.txt


### BN-17: The D/Q/RP/E governance-identifier web is outside the machine-check perimeter — referential integrity is hand-maintained despite three real renumbering collisions
**Blocked:** Machine-verified resolution of every cross-ledger identifier reference (Q→D signatures, RP/FREEZE_REV/E citations, BOTTLENECKS Basis paths) that AUDIT_INDEX promises auditors as the audit trail's spine
**Blocks:** The "existence-proof record with its full audit trail" claim surviving an auditor's first dangling reference — Q-M03→Q-M04, Q-O03→Q-O04, and FREEZE_REV5→REV7 renumberings already happened and only hand-checks catch the next one
**Resolution condition:** A collected pytest fails on any dangling D-/Q-/RP-/E-/FREEZE_REV cross-reference or nonexistent BOTTLENECKS Basis path (seeded-violation test proves it fires), and the full verify-public pytest gate passes green on the current tree
**Basis:** tools/lint_publication.py

### BN-18: The post-publication defect record (ERRATA E-001/E-002) is Korean-only — the honesty differentiator's sharpest surface is unreadable at the exact click where scrutiny lands
**Blocked:** Non-Korean reader access to the errata that RESULTS rows 3/12 cite in their source columns and the README Publication section links directly — the only place the project proves it discloses its own plan-deviation defects
**Blocks:** The quarter goal's academic-scrutiny path — the reader verifying "defects are found and disclosed, not hidden" hits a Korean wall one click below the English claims/limits chain that BN-11/BN-14 are closing
**Resolution condition:** English-canonical ERRATA.md with the Korean original preserved as .ko.md per the F-01/F-02 protocol, numeric token-parity PASS, adoption queue entry filed, owner-adopted on main with verify-public RC=0
**Basis:** AUDIT_INDEX.md:18

### BN-19: The headline finding has no figure — RESOLVED (2026-08-05, D-P43)
**RESOLVED:** resolution condition met and owner-signed — deterministic
`analysis/fig_tradeoff.py` regenerates the threshold-sweep figure (detection
+ FPR with CP95, ordinal labels) from `analysis/decision_table.json`; PNG
committed; adoption executed per Q-F17 default (C): README companion line +
DECISION_TABLE.md header (D-P43 signature record).
**Blocked:** A 30-second visual of the threshold sweep (detection 12/12 vs FP 71.4% at T≥50; detection 1/12 at T=70) from committed decision_table.json — the README first-screen figure shows the narrower wave-1 claim, not the headline
**Blocks:** Practitioner conversion on the headline claim itself — the quarter's "readable by its target audience" goal fails at the top sentence, where prose forces minutes for what one tradeoff chart gives in seconds
**Resolution condition:** A committed deterministic script regenerates a threshold-sweep figure (detection and false-positive rates with CP95, ordinal-convention labels) from analysis/decision_table.json, PNG committed, plus an owner adoption queue entry for README/DECISION_TABLE placement
**Basis:** analysis/decision_table.json

