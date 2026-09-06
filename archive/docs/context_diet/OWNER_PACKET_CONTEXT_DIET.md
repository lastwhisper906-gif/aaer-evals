# OWNER_PACKET_CONTEXT_DIET.md — 컨텍스트 다이어트 3결정 (OWNER SIGNATURE REQUIRED — INV-18)

Branch: `context-diet` (aaer-evals, unpushed) + harness commit `abcb978`
(~/tools, branch `v3-restructure`). Session 2026-08-06. Nothing below is
active; every default is NO/defer. INV 본문 24종 무변경 (표현/도구만).

## 준비된 것 (전부 비활성)

| # | 산출물 | 위치 | 상태 |
|---|---|---|---|
| 1 | `sync_context.sh --compact` 플래그 | ~/tools `abcb978` | 커밋됨 — **기본 경로 byte-identical 실증** (md5 48f65ac7… 동일, diff 공백). 플래그는 opt-in |
| 2 | compact CLAUDE.md 후보 | job-tmp `compact_stage/` (재생성: `sync_context.sh --compact <staging>`) | 284→196행 (−88). 24 INV 헤더·Constraint·예외 3건 verbatim 보존, Basis/Violation → 포인터 24행, 경고 헤더 1행 — 전부 grep 실증 |
| 3 | 리뷰어 프롬프트 후보 | `docs/context_diet/reviewer_system.candidate.md` | 5행 삽입 diff — **live 하네스 미적용** |
| 4 | A/B 실험 설계 | `docs/CONTEXT_DERIVATION_EXPERIMENT.md` | 설계만 — 실행 게이트는 본 패킷 |
| 5 | 의식 개정 초안 | `docs/MONTHLY_RITUAL_AMENDMENT_DRAFT.md` | 별도 파일 — MONTHLY_RITUAL.md 무접촉 |

## Decision 1 — CLAUDE.md 생성 기본값을 --compact로 전환할까?

- **옵션**: (A) 전환 — sync_context.sh 기본 호출이 compact 출력
  (모든 자동 로드 소비자가 압축본을 받음) · (B) **현행 유지 — 플래그는
  opt-in으로 두고 A/B 1라운드(실험 문서 Arm C, N=6) 완료 후 재상정** ·
  (C) 플래그 자체 철회.
- **근거**: 압축은 세션 컨텍스트 ~88행 절감이지만, Violation test가
  자동 로드에서 빠지는 대가가 실측 없이 정당화되지 않는다. 실험 문서의
  판정 규칙이 이 실측을 정의한다.
- **기본값 (무응답 시): (B) — NO.** 전환 없음.

## Decision 2 — 리뷰어 프롬프트 변경을 live 하네스에 채택할까?

- **옵션**: (A) 채택 — 서명 후
  `cp docs/context_diet/reviewer_system.candidate.md ~/tools/harness/judgment/prompts/reviewer_system.md`
  (다음 루프 시작부터 효력; run-start 스냅샷 구조상 진행 중 런은 불변) ·
  (B) **거치 — 서명 전 미적용** · (C) 기각.
- **동반 노트 (Phase 2.2 conformance):** v3 M2가 검증 증거를 이미 3중
  강제한다 — intake가 `verify:` 없는 태스크를 거부(exec/contract.sh),
  검증 실패는 리뷰어 호출 전 auto-REVISE(run_task.sh:367), 통과 출력은
  리뷰 프롬프트에 주입(:387-388). **중복 요구 미작성.** 잔여 갭 1:
  REVIEW_SPEC §a EVIDENCE가 `cycle_N_check.log`를 인용 대상으로
  명명하지 않음 — 채택 시 §a에 한 줄 추가 여부는 (A) 서명에 포함해
  지정 가능 (기본: 추가 안 함 — 구조 강제가 이미 충분).
- **기본값 (무응답 시): (B) — NO.** 서명 후 다음 루프 시작부터.

## Decision 3 — 의식 개정 초안을 MONTHLY_RITUAL.md에 병합할까?

- **옵션**: (A) 병합 (§A와 §B 사이 A-2 절) · (B) **연기 — Decision 1/2
  결과 확인 후** · (C) 기각.
- **기본값 (무응답 시): (B) — defer.**

## 세션 공개 사항 (판단 재료)

- 하네스 커밋 `abcb978`은 소유자의 활성 브랜치 `v3-restructure` 위에
  있다 (별도 브랜치 아님 — ~/tools에 브랜치 지시 부재, 단일 파일 커밋).
- 60초 병행 작성자 점검 2회 통과 후 진행; 점검 중 정적 미추적 파일
  `exec/retry.sh`·`exec/state.sh` 관찰 (소유자 v3 후속 작업으로 추정,
  본 세션 무접촉).
- 본 세션이 편집한 하네스 파일은 `sync_context.sh` 단 1개. 리뷰어
  프롬프트·REVIEW_SPEC·run_task.sh·contract는 live 무접촉.
- 스코프 준수: pipeline/·schemas/·scoring/ 기존 항목 무접촉,
  INV 본문 24종 무변경 (git diff로 기계 검증 가능).

> 범위 한정: Claude 기반 단일 파이프라인의 개발 하네스에 한정. 채점:
> Claude 보조 + 인간 최종 확정. No positions · educational/informational.
