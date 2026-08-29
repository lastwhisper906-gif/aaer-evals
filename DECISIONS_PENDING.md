# DECISIONS_PENDING.md — direction-loop 설치 중 위임 결정 원장 (owner ratify 대기)

> 2026-07-29, 소유자 전권 위임 지시("decide, execute, log") 하의 세션이
> 내린 결정 기록. 형식: options / choice / basis / revert. 소유자 추인
> 시 D-원장(scoring/decisions_log.md)으로 이관하거나 여기 서명을 남긴다.
> 이 파일 자체는 게시 산출물이 아니다.

## D-P1 — INV-16 단일 작성자 원칙: direction-loop 조건부 예외 (U1 집행)
- **Options:** (a) 조건부 예외로 개정 (b) 루프를 INV-16 위반으로 보고 중단
- **Choice:** (a) — 소유자 답변 U1 그대로: 비-main 브랜치 + 하네스 기계적
  격리(워크트리 전용·보호 경로 revert·전역 단일 루프 잠금) 하에 허용,
  루프 실행 중 main push 금지는 소유자 관행. INV-16은 §6 저장소
  규약이지 측정 조건이 아니므로 동결 규칙 위반 아님.
- **Basis:** 소유자 지시문 U1 (2026-07-29) · PROJECT_INVARIANTS.md §6
- **Revert:** PROJECT_INVARIANTS.md INV-16 예외 단락 삭제 +
  `sync_context.sh .` 재실행.

## D-P2 — D-앵커 검증: 하네스를 저장소에 적응 (U2 집행)
- **Options:** (a) 하네스 H19의 D-분기를 scoring/decisions_log.md +
  하이픈 정규화로 적응 (b) docs/decisions/ 디렉토리·별칭을 저장소에 신설
- **Choice:** (a) — 저장소를 하네스에 맞추지 않는다. verify_anchors의
  D-* 분기는 `scoring/decisions_log.md`(+ `docs/decisions/` 존재 시 병행)
  를 검사하고, "D-94"·"D94" 두 표기를 하이픈 제거 정규화 후 `^## D` 형
  헤딩과 대조한다. 리뷰어 프롬프트의 앵커 사양도 동일하게 갱신.
- **Basis:** 소유자 지시문 U2 · AUDIT_INDEX.md §1 (D-NNN 원장 위치 규약)
- **Revert:** ~/tools/direction-loop.sh verify_anchors D-분기와
  ~/tools/prompts/direction_review.md 앵커 절을 계획 v2 원문으로 복원.

## D-P3 — .loop.conf GATE_CMD (U3 집행)
- **Options:** (a) pytest 스모크 게이트 (b) make verify-public 전체 5게이트
- **Choice:** (a) `GATE_CMD=".venv/bin/python -m pytest pipeline tools
  scoring analysis -q"`. **INV-05 비위반 사유(소유자 지시 그대로 기록):**
  루프의 사이클별 게이트는 스프린트 브랜치 위의 스모크 게이트다. 전체
  verify-public 5게이트는 소유자의 main 병합을 종전과 동일하게 계속
  지배한다 — 5게이트를 다른 것으로 "대체 실측"하는 것이 아니라, 병합
  게이트 앞단에 사이클 게이트를 추가하는 것이다.
- **Basis:** 소유자 지시문 U3 · Makefile verify-public · INV-05
- **Revert:** .loop.conf 1줄 수정.

## D-P4 — DIRECTION_CONTEXT.md 작성 규칙
- **Options:** (a) 저장소+덤프에서만 합성, 미답은 OPEN 절 (b) 그럴듯한
  보완 작성
- **Choice:** (a). 답변된 항목: Q1·Q4·Q7·Q8·Q12(부분)·Q13·Q15·Q16·Q19.
  OPEN (owner)로 이관(질문 원문 그대로): Q2·Q3·Q5·Q6·Q9·Q10·Q11·Q14·
  Q17·Q18. 덤프의 사실 주장(B3 귀속 0.147, 3-arm +6.0pp, Karpoff/Lou,
  Lowe v. SEC 등)은 소유자 제공 사실로 기재 — 세션이 검증·창작하지 않음.
- **Basis:** 소유자 지시문 MEMORY_DUMP 절 ("NEVER fabricate answers")
- **Revert:** git revert (파일 단독 커밋 아님 — 해당 커밋의 파일 복원).

## D-P5 — VALIDATION_CRITERIA v1: 위임 선택분 (V3/V5/V6 정의 + V1 처리)
- **Options:** V3/V5/V6를 계획 §7.0 원문 그대로 두기 vs 판정 가능하게
  구체화; V1을 게이트에 포함 vs 소유자 사후 채점으로 명시 분리
- **Choice:** V2=0·V4≥50%는 소유자 고정값 그대로. V3는 "항목 인용 +
  선호 이상의 사실 주장 부재" 판정 규칙으로, V5는 "done_when이 why의
  문제를 해소하지 못하는 불일치" 판정 규칙으로, V6는 "≤150줄 + 모듈
  책임 + INV 강제 지점 ≥5 + BN 차단 지점 ≥3 + 인용 경로 실재" 체크로
  구체화 — 전부 인용 증거 요구. V1은 소유자 사후 채점(기계 사인오프
  비게이트, 첫 병합 결정 게이트)으로 명시. 정지 규칙: V2–V6 실패 시
  중단, 리뷰어 프롬프트 개정 최대 2회.
- **Basis:** 소유자 지시문 §1 (V2/V4 고정, "choose and justify the rest
  yourself; V1 owner-graded post-hoc") · 계획 §7.0
- **Revert:** VALIDATION_CRITERIA.md는 등록 후 동결 — 수정이 아니라
  차기 검증 라운드에서 v2로 재등록.

## D-P6 — .protected-paths: 위임 작성분 + 애매 판정 기록 (Stage 2)
- **Options:** 각 경로마다 (보호) vs (루프 편집 허용). 기준: "루프가
  바꾼 뒤 revert해도 피해가 남는가" (비가역성). 애매 ⇒ 보호.
- **Choice (전체 52 프리픽스, 전부 prefix-anchored·사각 항목 0 검증):**
  - 명백 보호: forward/ · runs/ · data/ · scoring/ (비밀+원장) ·
    schemas/ · specs/ · governance/ · review_packets/ · audit/ ·
    docs/FREEZE_REV · 평가 핀 파일 5종(pipeline/cutoff_guard·cli_client·
    build_payload·runner*·api_client·date_shift) · 게이트 정의(Makefile·
    .github/·tools/verify_*·lint_*·reproduce_analysis·memo_verify 2종·
    forward_* 8종·seal_predictions) · requirements. · ERRATA.md ·
    EXCLUSION.md · GATE_PACKAGE.md · LICENSE* · CITATION.cff ·
    PROJECT.md · CLAUDE.md · AGENTS.md · 기준 문서(docs/CONTROL_CRITERIA*·
    HOLDOUT_CRITERIA·UNIVERSE_SELECTION·FUTURE_*·EARLINESS_DESIGN·
    SURVIVORSHIP_AUDIT_PLAN·V1_PARTIAL_DEIDENTIFICATION_NOTE·
    baseline_screens)
  - **애매→보호 (양쪽 논거 기록):**
    - analysis/ 전체: [편집 허용론] 문서 정합 수리의 주 무대, 상당수가
      파생 보고물. [보호론] 사전 등록 PLAN·서명 DECISION_TABLE·게시
      JSON이 혼재 — 분리 목록은 누락 위험. ⇒ 보호 (루프는 제안만).
    - aaer_eval/: rev2 게시 경로의 판정·통계 모듈 — 사후 변경은 판정
      기준 변경. ⇒ 보호.
    - atlas/·issue0/·pilot/·experiments/·logs/·output/·surface/·
      controls/: 과거 기록·구성 산출물, 용도 불명 포함. ⇒ 보호 (불명은
      30초 규칙으로 보호).
  - **의도적 비보호 (루프의 실행 가능 표면):** README*·RESULTS.md·
    METHOD.md·AUDIT_INDEX.md·REPRODUCING.md·CHANGELOG 등 파생 보고
    문서(revert로 완전 복원 가능, lint·owner 병합 5게이트가 백스톱) ·
    docs/ 서사·상태 문서(HANDOFF·RESUME·OWNER_QUEUE 등) · pipeline/
    테스트·픽스처 · tools/ 나머지 · conftest.py · 판단 기반 문서 4종
    (.loop.conf 포함)은 H9 가드셋이 별도 자동 보호.
- **Basis:** 계획 §4 (비가역성 기준·과보호 저비용) · 소유자 Q15 경계 ·
  SUPERSESSION_CYCLE001_REPIN(핀 파일 목록) · awk prefix 검증 실측
  (dead 0, caught 3543/3681)
- **Revert:** .protected-paths에서 해당 줄 삭제 (줄 단위 가역).

## D-P7 — H23 해석: 발견 필수 필드 기계 검증 [ASSUMED]
- **Options:** H23의 "missing-field … terminate"를 (a) 발견(executable)
  블록의 필수 필드 9종(id·category·anchor·what·why·files·action·
  done_when·touches_protected) 전수 검사로 해석 (b) STRATEGIC 채널까지
  확장 (c) 미구현
- **Choice:** (a). 계획 v2 문서에는 H23이 없고 소유자 지시문의 드라이런
  항목("H23 missing-field and INV-99-basis terminate")만 존재 — 실행기가
  의존하는 필드가 빠진 발견은 기본 모드에서 런 종료, review-only에서는
  "incomplete findings: N" 출력. INV-99-basis 종료는 H19 경로가 담당.
  STRATEGIC 항목은 실행되지 않으므로 검사 제외.
- **Basis:** 소유자 지시문 Stage 3 · direction-loop.sh check_finding_fields
  (~/tools/direction-loop.sh, [ASSUMED D-P7] 주석) · 드라이런 T21 PASS
- **Revert:** 해당 블록 삭제 (H19·A2는 독립).

## D-P8 — H24 해석: 소유자 컨텍스트 충돌 스크린 [ASSUMED]
- **Options:** "repeat-conflict exit 6 / ungrounded-conflict dropped /
  call-failure non-fatal"의 "conflict"를 (a) 발견 vs DIRECTION_CONTEXT
  기각 목록·INV 제약의 충돌로 해석 — 읽기 전용 추가 호출 1회로 스크린
  (b) 발견 간 상호 충돌로 해석 (c) 미구현
- **Choice:** (a). 근거: "call-failure non-fatal"은 모델 호출 전제,
  기각 접근 재제안 차단은 G2·DIRECTION_CONTEXT의 명시 목적. 동작:
  스크린 호출 실패 → 비치명(로그 후 진행) · CONFLICT 라인의 앵커가
  검증 불가 → 그 충돌 폐기 · 검증된 충돌 → 해당 사이클 exec 스킵 +
  키(발견 앵커|충돌 앵커) 기록 · 동일 키 재발 → exit 6 (리뷰어가
  소유자 기각 작업을 반복 제안 — 경성 정지). 기본 모드 전용
  (review-only는 H13의 "리뷰만" 계약 유지).
- **Basis:** 소유자 지시문 Stage 3 · direction-loop.sh H24 블록
  ([ASSUMED D-P8] 주석) · 드라이런 T22a/b/c PASS
- **Revert:** H24 블록 삭제 — 프롬프트 수준 금지(리뷰어 Rules)는 그대로
  남는다.

## D-P9 — H18 체크섬 범위: ~/tools 전체 → 루프 소비 파일 8종 [ASSUMED]
- **Options:** (a) 계획 원문대로 ~/tools 전체 sha256 (b) 루프가 읽고
  실행하는 파일 8종(direction-loop.sh·preflight.sh·bootstrap.sh·
  loop-status.sh·loop-autoreview.sh·prompts 3종)만
- **Choice:** (b). 이 머신의 ~/tools에는 무관한 상시 작업(market-brief/
  — launchd plist + 증가하는 brief.log)과 .git 디렉토리가 있어 전체
  체크섬은 중간 실행 오탐(exit 5)을 구조적으로 낸다. D4 위협(exec가
  다음 사이클용 리뷰어 프롬프트·하네스를 몰래 수정)은 루프 소비 파일
  집합으로 완전 커버 — 그 밖의 ~/tools 파일은 루프가 읽지 않으므로
  변조가 루프 동작에 도달할 경로가 없다. 부작용: "~/tools에 새 파일
  추가"는 감지하지 않는다(목록 파일 수정·삭제는 감지).
- **Basis:** ~/tools 실측(market-brief 상주) · 계획 D4 위협 모델 ·
  드라이런 T14 PASS (목록 파일 변조 → exit 5)
- **Revert:** harness_sum을 계획 6.2 원문 find 방식으로 교체.

## D-P10 — 기계 이식성 2건: sha256 폴백 + 워크트리 .venv 링크 [ASSUMED]
- **Options/Choice:** ① macOS에 sha256sum 부재 가능 → `shasum -a 256`
  폴백 함수. ② GATE_CMD(U3 고정 문자열)의 `.venv/bin/python`은
  gitignore된 .venv가 신선 워크트리에 없어 실패 → H1 프로비저닝에서
  메인 저장소 .venv를 심링크하고 git info/exclude에 등록(커밋 불가
  경로, H2 clean-tree 무영향). GATE_CMD 문자열 자체는 소유자 지정
  그대로 유지.
- **Basis:** darwin 실측 · .gitignore(.venv/) · 드라이런 전체 PASS
- **Revert:** ① sha() 제거 ② 심링크 블록 제거 + .loop.conf를 절대
  경로로 변경(소유자 승인 필요).

## D-P11 — Stage 1 기계 사인오프 (V1 소유자 사후 채점 대기)
- **Options:** (a) V2–V6 전부 통과 확인 후 기계 사인오프 생성 (b) 소유자
  복귀까지 사인오프 보류
- **Choice:** (a) — 소유자 지시문 §5 그대로("If all machine-gradable
  criteria pass: create .direction/stage1_signed_off"). 실측:
  V2=0/0/0 (기계) · V4=50%(1/2)·100%(1/1) ≥50% (기계) · H23 incomplete
  0/0/0 · V3=위반 0 (전 채널 실측 — 발견은 3건 전부 BN-05 omission,
  STRATEGIC S-01 1건은 역량 배치 평가) · V5=위장 없음 (유일 발견의
  done_when이 why의 미규정 상태를 직접 해소 + OWNER DECISION
  REQUIRED로 정직 라우팅) · V6=baseline 115줄≤150, 모듈 책임 6구역,
  INV 강제 지점 7개(코드 경로 포함), BN 차단 지점 6개, 인용 경로 전수
  실재(맨이름 3건은 문장 명시 디렉토리 내 해소). V1은 미채점 — 마커
  문구에 명기.
- **Basis:** VALIDATION_CRITERIA v1 (커밋 d720ac8, 리뷰 실행 전 등록) ·
  런 .direction/20260729-021552 (worktree aaer-evals-loop, base 0c2d227)
- **Revert:** rm aaer-evals-loop/.direction/stage1_signed_off — 기본
  모드는 즉시 다시 거부된다 (H15).

## D-P12 — 리뷰어 미션 확장: goal_gap 카테고리 (소유자 승인 편집)
- **What:** 소유자 지시(2026-07-29, ~/Downloads/direction-loop-v2.md)에
  따라 두 편집 실행. ① ~/tools/prompts/direction_review.md "What to look
  for"에 7번 카테고리 **goal_gap** 추가 — DIRECTION_CONTEXT.md "What good
  looks like this quarter" 대비 저장소 감사(기존 6종은 자기 문서 대비
  감사). H19 앵커 규칙 불변: anchor = 갭을 증거하는 실재 저장소 경로.
  라우팅 불변. ② DIRECTION_CONTEXT.md "What good" 절에 소유자 추가분
  1항(대상 독자 가독성: 영어 헤드라인 문서·90초 README·열린 피드백
  채널·인용 가능 정체성) append — 소유자 목소리 문서의 소유자 승인 편집.
- **Assumed micro-decisions:** (a) 출력 포맷의 category 열거형에
  goal_gap 병기 — 미션과 포맷 스펙의 정합 목적. 하네스(H23)는 필드
  존재만 검증하고 값은 검증하지 않음을 실측 확인 — 기존 규칙 약화 없음.
  (b) ~/tools는 git 저장소지만 prompts/ 전체가 untracked — "commit both
  edits" 이행을 위해 prompts/direction_review.md 단일 파일만 add·commit
  (부분 추적 개시). 타임스탬프 증거(INV-07 정신) 확보 목적.
- **Not touched:** PROJECT_INVARIANTS.md 무변경 (git status 실측) —
  sync_context.sh 불요. 측정 조건·동결 경로 무접촉.
- **Basis:** 소유자 지시문 원문 · direction-loop.sh:195-211 실측(H23
  필드 존재 검증만) · git status 실측
- **Revert:** ① 카테고리 7 블록 + 열거형 goal_gap 제거 ②
  DIRECTION_CONTEXT.md append 1항 제거 (양쪽 모두 단일 커밋 revert).

## D-P13 — 승인 푸시 실행 + 첫 실전 스프린트 기동 (2026-07-29)
- **What:** ① 5게이트(verify-public) 전부 PASS 실측 후 main 7커밋 푸시
  (d92ce25..429c1ce). 소유자 지시문은 "6 pending commits"였으나 실측
  ahead 7 — 7번째는 직전 지시로 승인·커밋된 429c1ce(goal_gap 편집)라
  범위 내로 판단하고 포함 푸시. CI run 30389485749 green 확인.
  ② 2사이클 스프린트를 tmux(dloop) 분리 기동 — preflight·H15 사인오프
  게이트 통과 확인(60초 체크), run .direction/20260729-035419.
- **Outcome:** exit 0 (REASON="exec produced no commit (cycle 2)" —
  실행 가능 항목 소진, 정상 종료 형태). cycle 1: F-01/F-02 번역 2커밋
  (c4c187d·d4c0e9f, 게이트 green). cycle 2: 유일 발견이 보호 경로
  (tools/lint_publication.py DOCS) + OWNER DECISION REQUIRED → 커밋 0.
  done_when 전 항목 본 세션 재실측 PASS. 충돌 검사 양 사이클 NONE.
  머지/체리픽/폐기는 미실행 — 번역 정본 문서 내용 검수가 선행하는
  소유자 결정 (INV-18).
- **Basis:** verify-public 실측 로그 · facts.txt(기계 생성) ·
  review-2.md 검증 절 · 소유자 지시문(2026-07-29 Action 1·2)
- **Revert:** 푸시는 되돌리지 않음(이력) · 스프린트 산출물은 워크트리
  브랜치에 격리 — 폐기 시 `git -C ../aaer-evals-loop reset --hard 0c2d227`.

## D-P14 — 승인 병합 실행 + 수치 등가 기계 검사 판정 (2026-07-29)
- **What:** 소유자 지시 Action 1 — 병합 전 수치 토큰 다중집합 검사 실행.
  RESULTS 표 영역(정본 수치 전체): 189=189 토큰 **완전 동일 PASS**.
  전문(full-file) 비교의 비대칭 토큰 8건은 전수 판독 결과 전부
  (a) `.ko.md` 전용 D29 교차링크 메타데이터 라인("D29 패턴" → '29' 2건)
  (b) 숫자의 영어 단어 렌더링 — "신규 주장 0"↔"Zero new claims"(×2),
  "1페이지"↔"one page", "1회"↔"one … invocation", "정확히 1회"↔"exactly
  once", "3계기"↔"three instruments". 정본 수치를 건드리는 비대칭 0건 →
  가정 결정: 전문 검사의 "IDENTICAL" 요건은 위 두 클래스(구조적
  메타데이터·단어 렌더링)를 정규화로 제외한 판정 — 표 영역은 무정규화
  엄격 동일. 이 판정 하 병합 d5523a7 실행, verify-public GATE_RC=0,
  push 429c1ce..d5523a7 (D-P13 커밋 3b49a3e 포함 — main push 승인 범위 내).
- **Basis:** 소유자 지시문 Action 1 · numcheck 스크립트 출력(본 세션) ·
  review-2.md 값-대-값 검증(이중 게이트의 나머지 절반)
- **Revert:** `git revert -m 1 d5523a7` (병합 커밋).

## D-P15 — D114 적용 기록: 영어 표면 경계 (2026-07-29)
- **What:** 소유자 서명 D-A를 원장 D114로 기입, DIRECTION_CONTEXT.md
  분기 목표 절에 경계 확정 1항 추가 (커밋 ca30fd6). 번역 실행은 미포함
  — Action 3 루프 실행 채널로 위임.
- **Basis:** 소유자 지시문 Action 2 D-A · scoring/decisions_log.md D114
- **Revert:** ca30fd6 revert (원장은 append-only — revert도 이력 보존).

## D-P16 — D115 적용 기록: lint DOCS 확장 (2026-07-29)
- **What:** 소유자 서명 D-B를 원장 D115로 기입, 보호 경로
  tools/lint_publication.py DOCS에 RESULTS.md·METHOD.md·RESULTS.ko.md·
  METHOD.ko.md 4종 추가 (커밋 5f9661f). 적용 후 lint 단독 실행 RC=0
  PASS 실측. 가정 결정: 소유자 문안은 4종 명시라 .ko.md 원본 포함이
  지시 그대로 — cycle-2 패킷의 '.ko.md 포함 여부' 하위 질문도 이로써
  해소됨.
- **Basis:** 소유자 지시문 Action 2 D-B · lint 실측 RC=0
- **Revert:** 5f9661f revert.

## D-P17 — D116 적용 기록: BN-05 전향 명문화 (2026-07-29)
- **What:** 소유자 서명 D-C를 원장 D116으로 기입,
  docs/FUTURE_CYCLE_PROTOCOL.md 부록 A-3 신설 + BOTTLENECKS.md BN-05
  RESOLVED 하단 이동 (커밋 a19d3ea). ERRATA.md는 무수정(append-only) —
  교차 참조는 A-3 쪽에서 단방향. done_when 실측: grep R3 대상 파일 2건.
- **Basis:** 소유자 지시문 Action 2 D-C · ERRATA E-002 플래그 절 ·
  Stage-1 런 리뷰 done_when
- **Revert:** a19d3ea revert.

## D-P18 — D117 적용 기록: S-01 기각 (2026-07-29)
- **What:** 소유자 서명 D-D를 원장 D117로 기입, DIRECTION_CONTEXT.md
  Rejected approaches에 기각 등재 (커밋 f3d1ea2), 루프 워크트리
  .direction/strategic.md의 S-01을 RESOLVED 주석 처리. 가정 결정: S-02도
  D114로 해소되었으므로 동일 파일에서 RESOLVED 주석 병기(재라우팅 소음
  방지) — 소유자 명시 지시는 S-01만이었음을 기록.
- **Basis:** 소유자 지시문 Action 2 D-D · 병합 d5523a7 (실행 채널 실증)
- **Revert:** f3d1ea2 revert + strategic.md 원문 복원.

## D-P19 — 스프린트 20260729-112828 병합 (2026-07-29)
- **What:** Action 0-1 실행 — d09c8d7(F-01 AUDIT_INDEX 영어화) +
  7ec58c5(F-02 REPRODUCING 영어화)를 main에 --no-ff 병합 (ada2405).
  수치 등가 검사는 전 세션 보고에서 양 파일 PASS 완료(EN-only 토큰 0,
  KO-only 15건 전부 D29 헤더 2건 + 숫자→영단어 렌더링 13건으로 판정).
  병합 후 verify-public 5게이트 전부 PASS RC=0, push 완료.
- **Basis:** 소유자 지시문 Action 0-1 · 전 세션 수치 등가 판정(D-P14
  방법 동일) · vp0.log RC=0
- **Revert:** `git revert -m 1 ada2405`.

## D-P20 — D118 적용 기록: lint DOCS 확장 2차 (2026-07-29)
- **What:** 소유자 서명 D-E를 원장 D118로 기입, tools/lint_publication.py
  DOCS에 AUDIT_INDEX.md·REPRODUCING.md + .ko.md 원본 2종 추가 (D115와
  동일 패턴). 적용 후 lint 단독 실행 RC=0 PASS 실측. 스프린트 제기
  S-04 해소.
- **Basis:** 소유자 지시문 Action 0-2 D-E · D115/D-P16 선례 · lint 실측
- **Revert:** 본 커밋 revert.

## D-P21 — D119 적용 기록: BN-07/08/09 주입 + 상시 의심 등재 (2026-07-29)
- **What:** BOTTLENECKS.md에 BN-07(shallow-clone 재현 취약성)·BN-08
  (README 첫 방문자 전환)·BN-09(L-6 교차 채점자 부채) 주입,
  DIRECTION_CONTEXT.md Standing suspicions에 '정적 리뷰의 실행 경로
  맹점' 추가. **가정 결정(소유자 검토 대상):** 지시문의 '기지정 문언'이
  접근 가능한 어떤 기록에도 부재 — 계획 문서(direction-loop-v2-2.md)·
  전 세션 전사 전수 검색 0건. 주제 괄호 3건 + 저장소 실측(verify_blindness
  merge-base 이력 대조, README figure 0장, cross_grader SPECIFICATION
  ONLY)으로 문언을 도출해 주입했다. 문언이 소유자 의도와 다르면 이
  커밋 revert 후 원문 재주입이 정정 경로다.
- **Basis:** 소유자 지시문 Action 0-3 · D119 원장 기록
- **Revert:** 본 커밋 revert (BOTTLENECKS 형식 규약상 해소 항목은 하단
  이동이나, 미해소 신규 항목의 오기입 정정은 주입 커밋 revert가 맞다).

## D-P22 — D-F 적용 기록: 루프 워크트리 fast-forward 정합 (2026-07-29)
- **What:** 소유자 승인 D-F 실행 — 루프 워크트리(aaer-evals-loop)를
  origin/main(dbac35b)으로 --ff-only 정합, status clean 실측. 스프린트
  제기 S-03 해소. 부수: .direction/strategic.md의 S-03·S-04에 RESOLVED
  주석 병기(S-01/S-02 선례와 동일 — 재라우팅 소음 방지).
- **Basis:** 소유자 지시문 Action 0-2 D-F · INV-17(정합은 소유자 몫 —
  본 세션은 소유자 위임 실행)
- **Revert:** 워크트리 브랜치를 7ec58c5로 reset (main은 무영향).

## D-P23 — H25 replenish cycle 구현 (2026-07-29)
- **What:** ~/tools 하네스에 H25 구현(커밋 7ef8b1a): 기본 모드
  findings:[] 수렴 시 종료 대신 read-only FULL replenish 호출(런당 최대
  2회, 5렌즈 외부 리뷰어 미션 프롬프트 prompts/replenish.md). 후보는
  기계 필터 3종(H19 basis 검증 · 기존 Basis 중복 기각 · id 충돌 기각)
  통과분만 하네스 자신이 BOTTLENECKS.md에 append + D-P 기록 + 커밋
  (`replenish(harness): ` 접두, SHA를 $RUN/replenish_shas에 기록). H9
  보호 경로 검사는 per-commit으로 전환 + 기록된 replenish SHA가
  BOTTLENECKS.md/DECISIONS_PENDING.md만 건드린 커밋에 한정된 carve-out
  (잔여 위험 코드 주석 문서화: 적대 exec의 SHA 위조는 append 범위로
  bounded — 측정 조건 경로는 열지 못함). 드라이런 6시나리오 전부 green
  (/tmp stub, bash -n·shellcheck clean). **미세 가정 결정 2건:**
  (1) 소유자 미션 텍스트 뒤에 엄격 출력 계약 절(필드 문법)을 부가 —
  행동 스펙의 계약을 프롬프트 안에 명시해야 모델이 준수 가능;
  (2) shellcheck 미설치 상태라 brew로 설치 후 실측(지시 'shellcheck as
  usual' 이행 경로).
- **Basis:** 소유자 지시문 Action 1 · ~/tools 커밋 7ef8b1a · 드라이런
  로그 /tmp/h25-dryrun/log-s1..s6.txt
- **Revert:** ~/tools에서 7ef8b1a revert (aaer-evals 저장소는 무영향).

## D-P24 — D120 적용 기록: rescue + cherry-pick + BN-08 플립 (2026-07-29)
- **What:** rescue 브랜치 rescue-20260729-152205(15fc704) 생성으로 루프
  워크트리의 unreachable 커밋 보존, main에 0cfc80e·15fc704 cherry-pick
  (874b025·d813a1a) — verify-public RC=0, push, CI green 확인. 소유자
  손으로 BN-08 RESOLVED 이동(실측 증거 포함, 원장 D120).
- **Basis:** 소유자 지시문 Action 0 · vp2 로그 RC=0 · CI run d813a1a
  success
- **Revert:** BN-08 플립 커밋 revert + `git revert 874b025 d813a1a`
  (rescue 브랜치는 무영향).

## D-P25 — D121 적용 기록: S-05 해소, BN-09 재규정 (2026-07-29)
- **What:** BOTTLENECKS.md BN-09 resolution_condition을 소유자 패킷 준비
  3종(SPEC·선정 프로토콜·호출-비활성 SKELETON)으로 재규정(원장 D121).
  INV-12·INV-20 무개정. 루프 워크트리 strategic.md의 S-05에 RESOLVED
  주석 병기.
- **Basis:** 소유자 지시문 Action 2 · S-05 (run 20260729-152205 cycle 1)
- **Revert:** 본 커밋 revert + strategic.md 주석 제거.

## D-P26 — H26 검증 상태-플립 채널 구현 (2026-07-29)
- **What:** ~/tools 커밋 aa3dd0b. (a) direction_review.md에 GUARDED SET
  명문 규칙(BOTTLENECKS·DIRECTION_CONTEXT·PROJECT_INVARIANTS·.loop.conf·
  .protected-paths 변경 = 무조건 touches_protected: true) +
  `bn_resolved_claim: BN-xx` 필드 신설. (b) 하네스: 사이클의
  gate+Codex+scope 통과 후에만, 해소 조건의 runnable check(명시 `check:`
  라인, 또는 공백 포함 백틱 스팬 — 공백 없는 백틱 경로는 인용으로 간주)
  실행 PASS 시 하네스 자신이 헤딩 RESOLVED 편집 + 검증 증거(명령·출력
  sha256 다이제스트·날짜) 부기 + `bnflip(harness): ` 커밋 + SHA를
  replenish_shas에 기록(H9 carve-out 무확장 감사 완료 — BOTTLENECKS.md·
  DECISIONS_PENDING.md 한정 유지). check 실패 = 플립 없이 런 종료(실패
  출력 표시); runnable check 부재 = 플립 없이 소유자 패킷 라우팅.
  exit-4 경로가 revert 전에 facts.txt를 기록하도록 수정(이번 포스트모템의
  reflog 재구성 재발 방지). 드라이런 4/4 green, bash -n + shellcheck
  clean. **미세 가정 결정 2건:** (1) runnable check 판별 휴리스틱은
  보수(과소검출→소유자 패킷, 안전) 방향으로 설계 — 공백 포함 백틱만
  명령으로 간주; (2) H26 플립 항목은 제자리 RESOLVED(하단 이동은 소유자
  정리 몫 — 기계 편집 최소화).
- **Basis:** 소유자 지시문 Action 1 · ~/tools aa3dd0b · 드라이런 로그
  /tmp/h25-dryrun/log-h26a..d.txt
- **Revert:** ~/tools에서 aa3dd0b revert (aaer-evals 무영향).

## D-P (harness replenish) — H25 BN append: BN-10 BN-12 (20260729-170154 cycle 4)
- **What:** H25 replenish accepted BN-10 BN-12 after mechanical filters
  (H19 basis verification · no Basis overlap · no id collision). Appended
  and committed by the HARNESS, not exec-claude. Source: .direction/20260729-170154/replenish-4.md
- **Basis:** .direction/20260729-170154/replenish-4.md · H25 (owner-signed 2026-07-29)
- **Revert:** revert the replenish(harness) commit listed in .direction/20260729-170154/replenish_shas.

## D-P27 — 스프린트 20260729-170154 병합 + D122~D126 적용 기록 (2026-07-29)
- **What:** Action 1: 스프린트 6커밋 --no-ff 병합(42fedf3), verify-public
  RC=0, push, CI green. Action 2 서명 5건 적용 — D122: BN-09 플립(H26
  BNFLIP-09 패킷 증거), D123: verify_blindness shallow 가드(실측 full
  RC=0/shallow RC=1, CI fetch-depth 0 확인), D124: lint_doc_counts DOCS
  + REPRODUCING.ko.md(PASS RC=0), D125: BN-11 재진입(basis 교체
  analysis/DECISION_TABLE.md), D126: ISSUE_TEMPLATE 2종+config.
  **주기:** D123으로 BN-07 해소 조건 3종(코드 가드·문서 문언·양쪽 실측)이
  전부 충족됨 — 플립은 소유자 미지시라 보류, 차기 스프린트 리뷰어가
  bn_resolved_claim으로 올리면 H26 경로(프로즈 조건 → 소유자 패킷)로
  돌아오므로 소유자 서명 1건이 최단 경로.
- **Basis:** 소유자 지시문 Action 1·2 · vp4 로그 RC=0 · CI 42fedf3
  success · 원장 D122~D126
- **Revert:** 각 governance 커밋 개별 revert (원장은 append-only).

## D-P28 — direction-loop pager 정지 사고: 프로세스 해제 + 하네스 수정 (2026-07-30)
- **What:** 스프린트 20260729-185813(5사이클 전부 ok)이 종료 리포트의
  `git log --oneline`이 tmux tty에서 less로 페이징되며 ~3h54m 정지
  (20:21→00:14, EXIT trap 미실행, 워크트리 잠금+전역 잠금 고정, 토큰 소비
  0). 소유자 승인 하에 계보 확인 후 less(pid 52202)만 SIGTERM — 스크립트는
  자연 재개해 H20 브리프 생성 후 00:15:25 정상 종료, **양 잠금 모두 EXIT
  trap이 회수(누수 0), tmux 세션 자연 소멸(좀비 없음)**. 하네스 수정:
  ~/tools 커밋 0f4b226 — `export GIT_PAGER=cat PAGER=cat` + 종료 리포트
  tty 대면 2개 호출(git diff --stat/git log --oneline)에 `--no-pager`,
  bash -n·shellcheck PASS. 전용 dry-run 체크리스트 파일은 부재 —
  실패 모드는 스크립트 수정부 주석에 기록.
- **Basis:** ps 계보 실측(46643→52201 git log→52202 less, etime 03:52) ·
  ~/tools 커밋 0f4b226 · run 로그 .direction/20260729-185813 (BRIEF.md
  00:15 생성)
- **Revert:** ~/tools에서 0f4b226 revert (본 항목은 append-only 기록).

## D-P29 — H27 until-stop 모드 + H28 모델 fallback/쿼터 일시정지 구현·발사 (2026-07-30)
- **What:** 소유자 지시(플랜 ~/Downloads/direction-loop-v2-2.md + 2026-07-30
  지시문)로 ~/tools 커밋 072fed7. **H27:** `--until-stop` 플래그(--cycles·
  --review-only와 상호 배타, 워크트리 핸드오프 전파) — 사이클 캡 없음,
  종료는 `.direction/STOP`(모든 대기 전후 확인). 5사이클=1에포크; 에포크
  경계마다 H24 정합 패스를 롤링(직전 에포크 누적 diff + 신규 결정만)으로
  실행, 근거 있는 CONFLICT는 `.direction/coherence_conflicts.md`로 다음
  사이클 리뷰어 최우선 항목 라우팅(direction_review.md 규칙 신설), 동일
  앵커가 연속 두 에포크 패스 생존 시 exit 6. 보충 예산 2/에포크(경계
  리셋); 한 에포크 내 빈 수렴 2회 = "judgment base exhausted" 종료(소유자
  인지·수용한 유일한 자체 종료 예외). facts.txt에 에포크별 커밋 수 요약.
  **H28:** PRIMARY_MODEL(기본 = CLI 기본 모델)·FALLBACK_MODEL(기본
  claude-opus-4-8 — claude CLI 2.1.220이 해당 문자열 수락함을 라이브 1회
  호출로 확인). 쿼터 시그니처(429/rate limit/overloaded/usage limit) 실패
  시 fallback으로 1회 재시도, 호출별 모델을 meta.txt에 기록("cycle N step
  X: model=..."); fallback도 쿼터 실패 시 사이클 경계 QUOTA PAUSE(기본
  30분 sleep, STOP 전후 확인, 사이클 처음(리뷰 단계)부터 PRIMARY로 재시도,
  일시정지 이벤트당 예산 6h 초과 시 "quota exhausted beyond pause budget"
  종료). 비쿼터 실패는 H10 유지(재시도 없음). BRIEF·정합 패스도 fallback
  참여; Codex는 별도 풀(무변경). fallback 사용 시 BRIEF에 기계 부기
  honesty marker(고정 caveat 문구, 모델 아닌 하네스가 append). **미세 가정
  결정:** (1) coherence_conflicts.md는 최신 에포크 패스가 덮어쓰기,
  COHERENT 시 삭제; 생존 판정 앵커 집합은 .direction/epoch_anchors_prev로
  런 간 지속(per-cycle conflicts_seen 전례). (2) 에포크 경계 처리는 루프
  상단(continue 경로 포섭)이며 STOP 검사가 경계 처리보다 우선. (3)
  exec·codex-fix 쿼터 재시도 전 `git reset --hard PREV`(부분 커밋 파기).
  (4) 예산 소진 상태의 수렴도 빈 수렴으로 계상. (5) 정합 패스 실패(쿼터
  포함)는 S-B대로 비치명 로그, 직전 충돌 상태 유지. 드라이런 7/7 green
  (/tmp/h27-dryrun/log-{s1,s2,s3,s4a,s4b,s4c,s5a+b}.txt: 11사이클
  until-stop+STOP, 에포크 5·10 정합, 반복 충돌 exit 6, 빈 수렴 2회 종료,
  fallback meta 기록, pause 예산 소진, pause 중 STOP, 플래그 상호 배타),
  bash -n + shellcheck -S warning clean. 본 기록 push 후
  `--until-stop`으로 발사(기존 aaer-evals-loop 워크트리 재사용 — 미병합
  스프린트 20260729-185813 14커밋 위에서 계속; 병합 판단은 소유자 몫으로
  유지).
- **Basis:** 소유자 지시문(2026-07-30) · ~/tools 커밋 072fed7 · 드라이런
  로그 /tmp/h27-dryrun
- **Revert:** ~/tools에서 072fed7 revert (aaer-evals 무영향; 본 항목은
  append-only 기록).

## D-P30 — H31 사전 exec 라벨 검증: touches_protected는 주장, 기계 대조가 판정 (2026-08-03)
- **What:** 소유자 지시(런 히스토리 기반 강화 5건 중 1)로 ~/tools 커밋
  78fd717. 리뷰어의 `touches_protected` 라벨을 exec 실행 전에 GUARDED
  집합과 동일 prefix-anchored 매처로 전 소견 기계 대조: false인데 files가
  guarded와 겹치면 강제 true 라우팅(exec 입력 사본에서 라벨 플립 + 오라벨
  명기한 소유자 패킷을 strategic.md로 + "label corrected: F-xx" 로그),
  true인데 files가 clean이면 라우팅 유지·over-label 로그(소유자 패킷
  방향은 위험하지 않음). ALLOWED(H17c)는 이제 실행 가능 소견의 files
  합집합만 포함 — 정정으로 실행 집합이 비면 findings:[]와 동일한
  수렴/보충(H25) 경로로 진입(오류 아님). H25 블록은 이 재사용을 위해
  함수(replenish_path)로 전환(동작 동일). H5/H9 누적 스캔은 그대로 백스톱
  (심층 방어, 대체 아님).
- **Basis:** 스프린트 3(런 20260729-152205) exit 4 — review-2의 소견이
  `files: [BOTTLENECKS.md]`를 `touches_protected: false`로 오라벨, exec가
  guarded 파일을 커밋해 exit 4로 사이클 1의 검증된 2커밋까지 파괴 ·
  ~/tools 커밋 78fd717 · 드라이런 b1/b1b (/tmp/h31-dryrun/log-b1*.txt:
  오라벨 정정+소유자 패킷+exit 4 없음 / 전건 보호 시 replenish 진입)
- **Revert:** ~/tools에서 78fd717 revert (aaer-evals 무영향).

## D-P31 — H32 폭발 반경 축소 + 비정상 종료 facts 상시화 + 배너 off-by-one (2026-08-03)
- **What:** (a) 보호 경로 위반 시 reset 대상을 BASE→PREV(당해 사이클
  시작)로 변경 — 이전 사이클들은 각자 사이클별 보호 검사를 통과했으므로
  검증된 작업을 파괴하지 않는다. exit 4 유지, 종료 리포트·facts가 생존
  범위와 되돌린 범위를 커밋 수와 함께 명명. **수용 잔여:** 당해 사이클보다
  오래된 위반 커밋(사이클 간 주입 등)은 reset에서 생존하되 facts의 생존
  범위에 명시되어 소유자가 제거 — 침묵 보존 아님(드라이런 b6이 이 경로
  실증). (b) facts.txt를 모든 비정상 종료(4·5·6·쿼터 소진)에서 기록 —
  write_facts 함수화, exit 6 두 지점(사이클 H24 반복·에포크 반복)과
  exit 5(UNTRUSTED)·쿼터 소진 종료에 추가(H26 시절 지시는 exit 4만
  커버했음을 확인). 비정상 종료에는 BRIEF 호출 없음(비용 억제), git
  사실은 항상. (c) 종료 배너 "after N cycles" off-by-one 수정 — 루프
  상단 break 지점(STOP·캡·review-only 완료·에포크 경계 STOP)에서 미실행
  사이클을 계상하지 않음.
- **Basis:** 스프린트 3 exit 4 사고(D-P30과 동일 사건 — BASE reset이
  사이클 1 검증 커밋 파괴, facts 부재로 reflog 복구 필요했음) · 배너
  off-by-one 2회 관측(소유자 지시문) · ~/tools 커밋 78fd717 · 드라이런
  b2/b2e5/b2e6/b6/b7 (exit 4 PREV-reset+생존 범위, exit 5·6 facts 존재,
  "after 3 cycles" 정확)
- **Revert:** ~/tools에서 78fd717 revert.

## D-P32 — H33 런 시작 워크트리 자동 정합: behind는 ff, diverged는 거부 (2026-08-03)
- **What:** H2 clean-tree 검사 직후, 워크트리 브랜치가 main보다 strictly
  behind이고 ff 가능하면 `git merge --ff-only main` 자동 실행 +
  meta.txt에 "worktree ff'd to <sha>" 기록. DIVERGED(양쪽 커밋)면 exit 3
  거부 + 정합 옵션 3종(merge/rebase/discard) 출력 — divergence는 미병합
  스프린트를 뜻하고 그 판단은 하네스가 아니라 소유자의 것. 수동 ff 단계
  (한 번 잊혔던)를 제거해 낡은 거버넌스 문서를 리뷰하는 사이클을 차단.
- **Basis:** S-03 (런 20260729-112828 cycle 1 strategic — 워크트리가
  origin/main 6커밋 behind인 채 리뷰, 소유자가 수동 ff로 해소 D-F
  dbac35b; 재발성 수동 단계) · ~/tools 커밋 78fd717 · 드라이런 b3a/b3b
  (behind→ff 로그+HEAD==main / diverged→exit 3+옵션 출력+런 미시작)
- **Revert:** ~/tools에서 78fd717 revert.

## D-P33 — H34 until-stop 인체공학 + H28 정정: 실패 단계 재개·codex 쿼터 동등·STOP 단계 경계·에포크 DELTA (2026-08-03)
- **What:** (a) H28 정정 — 쿼터 일시정지 후 재개를 사이클 시작이 아니라
  **실패한 단계**로: run_step 래퍼가 매 모델 호출 전
  `.direction/cycle_step`에 현재 단계를 기록하고, pause 후 동일
  PREV로 그 단계만 재시도. exec가 이미 커밋한 뒤의 pause가 review+exec를
  재실행(중복 커밋)하는 D-P29 설계 결함 제거; exec 단계 자체의 쿼터
  실패는 종전대로 PREV로 reset 후 exec만 재시도, codex-fix는 post-exec
  HEAD(FIXBASE)로 reset 후 fix만 재시도(exec 커밋 보존). (b) codex 쿼터
  동등 — codex 호출 실패가 쿼터 시그니처와 일치하면 pause-and-retry
  경로 합류(codex는 별도 풀: 모델 fallback 없음, pause만); 비쿼터 실패는
  H10 종료 유지. (c) STOP 반응성 — `.direction/STOP`을 사이클 상단 외에
  단계 경계(리뷰 후 · exec+scope 검사 후 · codex fix 후)에서도 검사;
  exec와 그 scope 검사 사이에서는 절대 중단하지 않음(H31이 ALLOWED를
  guarded-clean으로 보장하므로 경계 중단 시 보호 위반 잔류 불가).
  loop-stop.md 문구 갱신("halts at the next step boundary, typically
  minutes"). (d) 에포크 스코프 DELTA — --until-stop에서 에포크 경계마다
  리뷰어 기준점 롤링: changed_files.txt는 epoch-start..HEAD, 이전 역사는
  설계대로 baseline/strategic이 대신. PROTECTED 스캔은 BASE..HEAD 누적
  유지(replenish/bnflip SHA carve-out 포함) — 안전 경계는 줄지 않고
  리뷰어 읽기 부하만 준다.
- **Basis:** H28 스펙 리뷰(D-P29의 "사이클 처음(리뷰 단계)부터 재시도"
  명세가 exec 커밋 후 중복 커밋 위험 — 소유자 지시문 적시) · ~/tools
  커밋 78fd717 · 드라이런 b4/b4b/b5a/b5b/b6 (exec 커밋 후 codex 쿼터
  pause→wake에서 codex만 재시도·exec 미재실행·커밋 셋 정확히 1 /
  비쿼터 codex 실패 H10 종료 / STOP after-review는 exec 전 정지 /
  STOP after-exec는 scope 검사 후에만 정지 / 에포크 롤오버 시
  changed_files 리셋+보호 스캔 누적성 유지)
- **Revert:** ~/tools에서 78fd717 revert + loop-stop.md 문구 원복.
## D-P (harness replenish) — H25 BN append: BN-13 BN-14 (20260729-185813 cycle 4)
- **What:** H25 replenish accepted BN-13 BN-14 after mechanical filters
  (H19 basis verification · no Basis overlap · no id collision). Appended
  and committed by the HARNESS, not exec-claude. Source: .direction/20260729-185813/replenish-4.md
- **Basis:** .direction/20260729-185813/replenish-4.md · H25 (owner-signed 2026-07-29)
- **Revert:** revert the replenish(harness) commit listed in .direction/20260729-185813/replenish_shas.

## D-P (harness replenish) — H25 BN append: BN-15 BN-16 (20260730-004720 cycle 2)
- **What:** H25 replenish accepted BN-15 BN-16 after mechanical filters
  (H19 basis verification · no Basis overlap · no id collision). Appended
  and committed by the HARNESS, not exec-claude. Source: .direction/20260730-004720/replenish-2.md
- **Basis:** .direction/20260730-004720/replenish-2.md · H25 (owner-signed 2026-07-29)
- **Revert:** revert the replenish(harness) commit listed in .direction/20260730-004720/replenish_shas.

## D-P (harness replenish) — H25 BN append: BN-17 BN-18 BN-19 (20260730-004720 cycle 4)
- **What:** H25 replenish accepted BN-17 BN-18 BN-19 after mechanical filters
  (H19 basis verification · no Basis overlap · no id collision). Appended
  and committed by the HARNESS, not exec-claude. Source: .direction/20260730-004720/replenish-4.md
- **Basis:** .direction/20260730-004720/replenish-4.md · H25 (owner-signed 2026-07-29)
- **Revert:** revert the replenish(harness) commit listed in .direction/20260730-004720/replenish_shas.

## D-P34 — 오케스트레이터 연속 개선 루프 기동: 외부 피드백 인테이크 + 소유자 결정 큐 (2026-08-05)
- **What:** 소유자 지시문(2026-08-05 오케스트레이터 프롬프트)에 따라
  외부 피드백 2건을 `.direction/feedback/EXT_FB_{A,B}_2026-08-05.md`로
  원문 보존하고, 코드 대조 검증을 거친 통합 백로그
  `.direction/feedback/BACKLOG.md`를 작성. 하네스(~/tools/harness)에
  OWNER_MODEL.md + REVIEW_SPEC.md 리뷰어 계약을 부트스트랩(~/tools 커밋
  457b77a). 빌드 루프는 Tier-1 CODE-FIX(FB-01..04)부터 실행하며, 각각
  INV-03 공개(disclosure) 기록을 본 원장에 append한다.
- **소유자 서명 대기 큐 (BACKLOG.md DP-Q1..Q10 — 루프는 절대 실행하지
  않음):** 스키마 v2 의미 강화·확률→서열 개명(DP-Q1) · CI 강화(DP-Q2) ·
  N 확장 스코프 개정(DP-Q3, INV-12 충돌) · 타 LLM 교차검증(DP-Q4,
  INV-12 충돌) · ML 베이스라인(DP-Q5, INV-12 경계) · forward 유니버스
  재설계(DP-Q6, INV-22) · 재추출 k≥5(DP-Q7, INV-19/21/22) · 외부 인간
  채점/DOI/GA-001(b)(DP-Q8) · 교란 v2(DP-Q9) · README 재구조화(DP-Q10,
  기존 Q-F11/13/14와 연결).
- **환경 공개 (INV-16/17 관련):** 세션 중 macOS TCC가 ~/Documents 접근을
  차단(기지 재발 현상). 표준 우회(미러 클론)를 무푸시 규약에 맞춰 적응:
  작업 사본은 `~/repos/aaer-evals-work`(origin/main 37ac75b에서 풀클론,
  로컬 main과 동일 상태 확인 후 생성). 모든 커밋은 이 사본에 로컬로만
  누적. ~/Documents 원본과 origin은 무변경. 동시 작성자 없음(단일 루프).
- **소유자 정합 명령:** TCC 복구 후
  `git -C ~/Documents/aaer-evals pull ~/repos/aaer-evals-work main`
  (또는 검토 후 사본에서 owner-dispatch push).
- **Revert:** 사본 폐기(`rm -rf ~/repos/aaer-evals-work`) +
  ~/tools 457b77a revert.

## D-P35 — FB-01 집행 기록: 교란 실험 마커의 페이로드 차단 (INV-03 공개, 2026-08-05)
- **What:** EXT_FB_B 항목 1 실측 확인 후 수리. 모델 가시 페이로드를
  3-키 allowlist(case·financial_series_point_in_time·filing_chronology)로
  고정 — 송출 3개소(runner.py·runner_api.py·probe_runner.py) 전부.
  `variant`→`_variant`(런 측 전용), `perturb_factor_recorded_scoring_side_only`
  삭제. 문자열 수준 회귀 테스트 `pipeline/test_payload_blindness.py`
  (3경로×2군 + v2-dateshift 형상). 스위트 306 passed/1 skipped,
  `make verify-public` 5게이트 PASS(RC=0), 문서 카운트 297→307 갱신.
- **INV-03 요건:** (a) 1차 결과 git 이력 보존 — 동결 runs/ 무접촉,
  수리는 전향(future-run) 경로만. (b) 공개 절 — docs/methodology_limitations.md
  L-9 (동결 수치가 마커 가시 조건에서 측정되었음과 편향 방향 미상 명기).
  (c) 재실행 없음 — 재측정은 DP-Q7(소유자 게이트) 대기.
- **주의(.protected-paths):** pipeline/build_payload.py·runner*는
  direction-loop 보호 목록에 있으나, 본 루프는 소유자 지시문(2026-08-05
  우선순위 규칙 1이 본 수리를 명시 지명)에 따라 집행 — D-P34 운영 규칙
  참조. 소유자 추인 대상.
- **하네스 실행 기록:** TASK_FB01_20260805_023947(STALLED — 빌더
  샌드박스 내 git fetch 불가로 사이클2 무변경; 원인·완화는 CYCLE_LOG
  entry 2) → 체크포인트 d8ae885 → TASK_FB01_20260805_024411 cycle 1
  APPROVE(REVIEW_SPEC 6절 준수, 근거 인용 리뷰).
- **Revert:** 해당 커밋 revert + L-9 항목은 append-only 규약상 존치
  (revert 사실을 후속 항목으로 추가).

## D-P36 — FB-02 집행 기록: 완성 payload 컷오프 fail-closed 불변식 + 로그 키 정정 + METHOD §2 정합 (INV-03 공개, 2026-08-05)
- **What:** EXT_FB_B 항목 2 실측 확인 후 수리. (i)
  `cutoff_guard.assert_payload_pre_cutoff()` 신설 — 완성 payload의 전
  날짜(series `filed`·chronology `filing_date`)를 재스캔, 컷오프 초과
  1건이라도 있으면 CutoffGuardError, 스캔 대상 키 부재도 fail-closed;
  `build_payload()` 말미에서 양군 공통 호출(INV-04 중립). (ii) 요약 로그
  키 정정: facts_after_cutoff→facts_retained_pre_cutoff,
  facts_dropped→facts_dropped_post_cutoff (의미 반전 해소). (iii)
  METHOD.md §2를 실제 3층 구조로 정합 — 원시 파일의 사후 데이터 허용 →
  로더 명시 필터+집계 로그 → 완성 payload 위반 즉시 실패; 기존 참
  문장(accession 교차검증·우회 스캔 테스트) 존치. 신규 테스트 5종.
  스위트 311 passed/1 skipped, verify-public 5게이트 PASS(RC=0), 문서
  카운트 307→312.
- **INV-03 요건:** (a) 동결 산출물 무접촉 — 코드·문서 전향 수리만.
  (b) 공개 절 — 본 항목이 METHOD §2의 종전 과잉 주장(전 로더 예외
  주장)을 명시 기록. (c) 재실행 없음.
- **하네스 실행 기록:** TASK_FB02_20260805 run cycle 1 APPROVE. 사전
  리뷰가 스펙의 차단급 오류(chronology 키명 filingDate→filing_date,
  build_payload.py:156 개명 미반영)를 빌드 전 교정 — 사전 리뷰 계약의
  실측 효용 사례.
- **Revert:** 해당 커밋 revert.

## D-P37 — FB-03 집행 기록: legacy 무-fingerprint 출력 자동 신뢰 제거 (INV-03 공개, 2026-08-05)
- **What:** EXT_FB_B 항목 7 실측 확인 후 수리. runner.run_case 기본값:
  스키마 유효·fingerprint 부재 기존 출력 = "FAIL (stale_legacy_output…)"
  — 모델 호출 0, 파일 쓰기 0, 원본 무변경(종전: 무조건 skip 신뢰).
  명시 수용은 `--accept-legacy-output` 플래그(감사 가능). fingerprint
  일치 멱등 skip은 무변경. 사전 리뷰가 초안(자동 재실행 기본값)을
  기각하고 사전 등록된 fix shape(보고-거부, DP-Q7 소유자 게이트 유지)로
  교정 — 무단 쿼터 소진 방지. 스위트 312 passed/1 skipped,
  verify-public PASS(RC=0), 문서 카운트 312→313.
- **스코프 일탈 공개:** 과업 명시 2파일 외 pipeline/test_cli_client.py
  4줄 강제 수정 — 기존 테스트가 구(舊) legacy-skip 동작을 단정하고
  있어 스펙 자체가 모순(오케스트레이터 스펙 결함). 하네스 리뷰어가
  일탈을 명시 공개 후 승인; 단정은 강화 방향(FAIL 거부 + 호출 0 유지).
- **하네스 실행 기록:** TASK_FB03_20260805_030750 cycle 2 APPROVE
  (cycle 1은 기계 체크 자동 REVISE — 위 기존 테스트 충돌).
- **Revert:** 해당 커밋 revert.

## D-P38 — FB-04 집행 기록: 피평가자 경로 검증기 FormatChecker 부착 (INV-03 공개, 2026-08-05)
- **What:** EXT_FB_B 항목 6(검증기 반쪽) 실측 확인 후 수리. 4개
  호출부에 `format_checker=jsonschema.FormatChecker()` 부착 —
  runner.py(~:176, 실구멍), cli_client.output_is_valid(~:329, 실구멍),
  cli_client.call_model(~:215, 오늘 기준 형식 주석 없는 스키마만 통과 —
  방어층, 실구멍 아님), test_output_schema_enforcement.py:~120(동결 출력
  재검증 테스트 — 생산 검증기와 엄격도 동기화, 동결 출력 전수 ISO 검증
  통과 실측). 경계 정직 기록: 핀 jsonschema는 draft-7 `date`만 내장 검사
  — `date-time`·`uri`는 의존성 동결(INV-11)로 미검사 유지, 주석 명기.
  회귀 테스트 1종 추가(비날짜 문자열 거부 + 정상 날짜 통과). 스키마
  파일 무변경(의미 강화는 DP-Q1 소유자 게이트).
- **보호 경로 공개:** cli_client.py·runner.py(.protected-paths 등재)
  수정 — 소유자 우선순위 규칙(스키마 강제) 근거, hunk 단위 실측: 인자
  추가 2건+1건과 경계 주석뿐. 스위트 313 passed/1 skipped,
  verify-public PASS, 문서 카운트 313→314.
- **하네스 실행 기록:** TASK_FB04_20260805 cycle 1 APPROVE. 사전 리뷰
  1회 일시 실패(Execution error) → CLI 건강 프로브 후 재시도 성공
  (쿼터 아님 판정).
- **Revert:** 해당 커밋 revert.

## D-P39 — FB-06 집행 기록: BN-19 headline tradeoff figure (INV-03 공개, 2026-08-05)
- **What:** BN-19 해소 조건 문언 그대로 집행 — `analysis/fig_tradeoff.py`
  (결정론, decision_table.json의 layers 객체만 순회, layer-수준
  n_treatment==12 유일 일치=L4_e2_trajectory, post-hoc `exploratory_combo`
  선택 불가 fail-closed) + `analysis/fig_tradeoff.png` 커밋 +
  OWNER_QUEUE Q-F17(배치 소유자 결정, 기본값 (C) both) 등재. 테스트
  4종: 재생성·커밋 존재·post-hoc 거부(완전 plottable 픽스처로 판별력
  확보 — 하네스 리뷰 cycle 1 REVISE 반영)·라벨 어휘(in-suite fraud/확률
  프레이밍 금지 — lint는 .py/.png 미스캔이므로 유일 게이트).
  기존 analysis/ 파일·README·DECISION_TABLE·BOTTLENECKS 무접촉.
- **FB-05 기각 기록:** verify-* 분리 요구는 D108 2계층 인터페이스로
  기충족(README.md:62-67 정직 스코프 문언 + 샌드박스 트랜스크립트) —
  사전 리뷰 독립 감사로 기각 유지 확정. A8 "시각화 전무" 주장도 기각
  (fig_dotplot 4종 기존재, BN-08/D120).
- **스위트:** 전체 통과, verify-public 5게이트 PASS, 문서 카운트
  314→318 (신규 테스트 4). BN-19 상태 플립은 이 루프가 하지 않음
  (guarded 채널 — 소유자/direction-loop).
- **Revert:** 해당 커밋 revert + Q-F17 항목은 append-only 존치.

## D-P40 — FB-07 집행 기록: N-확장 결정용 검정력 분석 (INV-03 공개, 2026-08-05)
- **What:** EXT_FB_A 항목 1 요구 실행 — `tools/power_analysis.py`
  (stdlib 전용·폐형식·무RNG; Hanley-McNeil 1982 근사 + Acklam 역정규
  근사, 오차 한계 주석) + `docs/POWER_ANALYSIS.md` + 테스트 5종.
  핵심 수치: AUC 0.83 vs 0.50 구별에 총 N 22-30(80% 검정력)로 현행
  설계 충분(wave-1 0.832·wave-2 0.874); 0.83 vs 0.65 구별에는 총 N
  64-94 필요 — 현행 검정력 0.285-0.320으로 심대 부족(A1의 "0.65인지
  0.95인지 모른다" 정량 확인). E2 trajectory 행은 게시 AUC 없음·가상
  설계 검정력 명기(사전 리뷰 요구; 마지막 절 문구는 오케스트레이터가
  병합 시 1문장 보강 — 공개 기록). RP-09 선행 분석과 스코프 구별 인용.
  권고 없음 — DP-Q3(INV-12 스코프 개정, 소유자 게이트)의 증거 입력.
- **하네스:** TASK_FB07 inverted mode(Claude 빌드·Codex 리뷰) cycle 1
  APPROVE. 스위트 323 passed/1 skipped, verify-public PASS, 문서 카운트
  319→324.
- **Revert:** 해당 커밋 revert.

## D-P41 — FB-08 집행 기록: CLAIMS.json 기계 가독 주장 원장 (INV-03 공개, 2026-08-05)
- **What:** EXT_FB_B 항목 11 집행 — 루트 `CLAIMS.json`(RESULTS.md 13행
  표의 verbatim 기계 렌더링: id·task_tag·측정·게시 수치·한계·출처 원문·
  출처 경로·status) + `tools/test_claims_ledger.py`(RESULTS.md 자체를
  파싱해 문자 단위 동기 잠금 — 1문자 오염 실측 FAIL 확인 후 복원).
  RESULTS.md가 정본, CLAIMS.json은 파생 — 생성기 스크립트는 사전 리뷰
  kill 지침대로 미제작(13행 표에 3번째 유지 대상 기계는 bloat).
  README 연결 여부는 소유자 결정 대기(Q-F18 후보 — 큐 등재는 다음
  소유자 세션에서, OWNER_QUEUE 연속 append 충돌 방지).
- **하네스:** TASK_FB08 cycle 1 APPROVE. 스위트 324 passed/1 skipped,
  verify-public PASS, 문서 카운트 324→325.
- **Revert:** 해당 커밋 revert.

## D-P42 — FB-09 집행 기록: MC 오차·시드·정확 순열 가능성 부록 (INV-03 공개, 2026-08-05)
- **What:** EXT_FB_B 항목 10(실행 가능 부분집합) 집행 —
  `tools/stats_annex.py` + `docs/STATS_ANNEX.md` + 테스트 5종. 게시된
  MC 순열 p 9건 전수: B=100,000을 소스에서 인용(analysis/stats.py:16 ·
  legacy/wave2_analyze_v1.py:29 — 역산 금지 규칙 준수), 추정량
  (ge+1)/(n+1) 인용, MC-SE·95% MC 구간 병기(최대 SE 0.0016 — MC 오차가
  결론에 무의미함을 정량화). 정확 순열 가능성: 6v16·8v22·9v23 enumerable,
  pooled 17v45 C(62,17)≈7.4e14 불가 — MC가 필요였음을 명시. 시드 출처:
  results_stats 아티팩트 기록 20260707, wave2는 아티팩트 부재 —
  legacy/wave2_analyze_v1.py:12 소스 인용(부재를 미상으로 오기하지 않음,
  사전 리뷰 A1). 재계산·수정 0, analysis/ 무접촉.
- **하네스:** TASK_FB09 inverted mode cycle 1 APPROVE. 스위트 329
  passed/1 skipped, verify-public PASS, 문서 카운트 325→330.
- **Revert:** 해당 커밋 revert.

## D-P43 — 소유자 서명 기록: 2026-08-05 루프 산출물 일괄 추인 (2026-08-05)
- **서명 원문 (세션 내 소유자 입력, verbatim):** "i will sign on all of
  above. approve." (2026-08-05, 오케스트레이터 세션)
- **서명 적용 범위 판정 (ORCHESTRATOR_NOTES 반(反)일괄승인 규율 적용):**
  (a) **확정 추인** — D-P34..D-P42(공개 기록 9건: 미러 클론 운영, 백로그
  검증, FB-01..04·06..09 집행, FB-05 기각) 및 그 커밋 18건; L-9; 하네스
  리뷰어 계약(~/tools 457b77a). (b) **기본값 있는 결정 확정** — Q-F17
  그림 배치 = 기본값 (C) both → 본 세션이 집행. BN-19 해소 조건 충족 +
  서명 → RESOLVED 플립 집행. (c) **원칙 승인, 패킷별 집행 대기** —
  DP-Q1..Q10 중 하위 선택지가 남은 항목(Q1: 개명 vs 보정 · Q4: 실행
  수단/INV-20 · Q6: 유니버스 확장 vs 중간 라벨)은 blanket approve로
  해소 불가 — 패킷 초안에 소유자 선택 1줄씩 필요. 세션은 이를
  추측하지 않는다.
- **Basis:** INV-18 (서명 기록 요건 충족 — 본 항목이 그 기록) ·
  docs/ORCHESTRATOR_NOTES.md 세션 운영 규율.
- **Revert:** 본 항목 아래 부인(disavowal) 항목 추가로만 (append-only).

## D-P44 — 소유자 서명 기록: DP-Q1/Q4/Q6 하위 선택 + push 디스패치 (2026-08-05)
- **서명 방식:** 세션 제시 선택지(각 2-3안 + 권고)에 대한 소유자 명시
  선택 (AskUserQuestion, 2026-08-05).
- **DP-Q1 확정:** (a) v2 계약에서 `misstatement_probability` →
  `misstatement_risk_score` 개명, ECE/Brier 주지표 강등. 동결 wave-1/2
  무접촉 — 전향 적용만. 패킷: PKT-Q1.
- **DP-Q4 확정:** (a) 교차모델 수단 = Codex CLI(ChatGPT 구독 인증) —
  zero-metered(INV-20 준수), GPT 한정(Gemini 제외 유지). INV-12 개정
  문안 포함 패킷: PKT-Q4. 실행(런)은 패킷 내 프로토콜로 별도 발사.
- **DP-Q6 확정:** (c) both — 규칙 정의 수백 사 유니버스 확장 + 중간
  라벨(Item 4.02 non-reliance·재작성) 사전 등록, AAER은 확인 라벨로.
  패킷: PKT-Q6 (Nov 2026 창 시계).
- **Push 디스패치:** 소유자 지시로 본 세션이 미러 클론에서 origin/main
  push 실행 (owner-dispatch 규약의 명시 디스패치 — 2026-07-20 사건
  예방 조건인 fetch-first·ahead-only 확인 후).
- **Revert:** append-only 부인 항목으로만.

## D-P45 — 소유자 서명 기록: 루프 수정판 v2 — 연속 모드 + 상시 위임 (2026-08-05)
- **서명:** 소유자 지시문 "LOOP AMENDMENT + RESUME — CONTINUOUS MODE (v2)"
  전문이 서명이다 (세션 입력, 2026-08-05). 요지: (1) WAITING-ON-OWNER
  종료 삭제 — 종료는 STOP 파일·SAFETY HALT만. (2) 보충 리뷰 생성형 전환
  — R1..R6 렌즈 로테이션, 무유휴. (3) 상시 위임: 로컬·가역·동결/게시
  무접촉 조건 하에 스키마 v2/CI 강화/README 재구조(브랜치)/교란 v2/
  그림·요약/통계 부록/유니버스 확장 PREP/구독 CLI 모델 런 사전 승인.
  종량 경로·push·게시·동결 접촉은 여전히 소유자 전속. 불변식 충돌 시
  불변식 우선 — 개정문 초안만. (4) 소유자 게이트 큐는 차단 사유 아님.
- **DP-Q 재분류 (v2 §3 적용):**
  - 실행 가능 전환: DP-Q1(스키마 v2 — D-P44a 기서명) · DP-Q2 절반
    (의존성 무추가 부분: SHA 핀·permissions·잡 분리 — Ruff/타입/커버리지는
    INV-11 충돌로 개정 초안 대기) · DP-Q9(교란 v2 구축+신호 보존 검증 —
    명시 사전 승인) · DP-Q10(README 재구조 — delivery-restructure 브랜치,
    병합 소유자 게이트) · DP-Q6 메모 초안(비보호 부분) · DP-Q3 PREP
    (매칭 규칙·픽스처 드라이런 — 신규 fetch는 INV-23으로 제외) ·
    DP-Q4 (INV-12 개정 커밋은 D-P44b 서명 인용, GPT 런은 구독 codex —
    v2 §3 모델 런 조항; 산출물은 신규 분리 경로, 게시 소유자 게이트).
  - 잔류 (불변식/외부 행위): k≥5 재추출(INV-21 핀 불일치 BN-03 —
    FREEZE_REV 재핀은 11월 창 결정 D113③) · ML 베이스라인(INV-12 개정
    초안 대기) · 인간 채점/DOI/GA-001(b)(소유자 외부 행위) ·
    유니버스 확장 본실행(INV-23 감독 fetch + INV-12 개정).
- **Revert:** append-only 부인 항목으로만.

## D-P46 — NB-01 집행 기록: schemas/llm_output_v2.json 서수 개명 계약 (INV-03 공개, 2026-08-05)
- **What:** D-P44a/D-P45 서명 하 집행 — v2 계약 파일 신설: 8개 소재지
  전부 개명(property·required×2·$defs·if/then 트리거·$ref 값 문자열·
  mechanism_hypotheses 설명 내 문구), 서수 의미 재기술("보정된 확률이
  아니다"), v1.2는 byte 무접촉(git diff 0줄 실측 + 테스트 가드).
  구조 diff 테스트가 의도된 델타 외 모든 차이를 JSON-pointer로 실패
  처리. 트리거 의미 인스턴스 검증(45→실패, 30→통과). 채택 배선은
  차기 FREEZE_REV(INV-21 핀 규율) — 이 파일은 그때까지 불활성.
- **패킷 문언 일탈 공개:** PKT-Q1은 $comment 헤더를 지정했으나 구현은
  최상위 description에 v2 표식 기재 — 기능 동등, 사전 리뷰 지적대로
  침묵 일탈 대신 본 기록으로 공개.
- **하네스:** TASK_NB01 cycle 1 APPROVE. 스위트 333 passed/1 skipped,
  validate_schemas PASS, verify-public PASS, 문서 카운트 330→334.
- **Revert:** 해당 커밋 revert (v1 무영향).

## D-P47 — NB-02 집행 기록: CI 공급망 강화 — 의존성 무추가 절반 (INV-03 공개, 2026-08-05)
- **What:** D-P45 §3(CI hardening) 인용 집행 — ci.yml에 (1) workflow 수준
  `permissions: contents: read` (2) actions/checkout@v4 →
  11d5960a326750d5838078e36cf38b85af677262, actions/setup-python@v5 →
  a26af69be951a213d495a4c3e4e4022e16d87065 (전체 SHA 핀 + 사람 가독 버전
  주석; SHA는 오케스트레이터가 gh api로 공식 저장소에서 실측 조회).
  스텝 목록·매트릭스·3.12 정본 잡 무변경 — INV-24 문언 보존. B9의 잡
  분리는 미집행: 3.12 잡 전 단계 실행이 INV-24의 보호 대상이라 이동은
  불변식 저촉, 병렬 중복 잡은 가치 대비 기계 증가로 kill.
- **직접 편집 공개:** 3줄 추가+2토큰 교체 규모로 하네스 자체 독트린
  ("one-line edits는 직접 편집이 저렴") 적용 — 빌더·리뷰어 호출 생략,
  텍스트 diff 검증(로컬 YAML 파서 부재는 INV-11 귀결; GitHub 푸시 시
  가시 검증). Ruff/타입/커버리지 절반은 PKT-INV11 개정 초안으로 큐잉.
- **Revert:** 해당 커밋 revert.

## D-P48 — INV-12 개정 발효: 구독 Codex GPT 교차모델 예외 (2026-08-05)
- **서명 근거:** D-P44b(소유자 명시 선택: "Codex/GPT via subscription —
  Requires an INV-12 amendment entry you sign" 옵션 선택) + D-P45 §3
  (불변식 충돌 시 개정 초안 → 서명 후 발효 규칙). 개정문은 PKT-Q4
  초안(15bca1c 커밋, push됨)과 동일 취지 — 소유자 열람 가능 상태였음.
- **What:** PROJECT_INVARIANTS.md INV-12에 예외 단락 + Violation test
  정합 수정; sync_context.sh로 CLAUDE.md 블록 재생성. 예외 범위: 동결
  회고 케이스 × 구독 Codex × 분리 경로(runs/crossmodel_gpt/) × 게시
  소유자 게이트. Gemini·종량 API·신규 케이스는 예외 밖(여전히 위반).
- **Revert:** 본 커밋 revert + sync 재실행.

## D-P49 — NB-03 집행 기록: 교차모델 GPT 러너 병합 · 라이브 트랜치 PARKED (INV-03 공개, 2026-08-05)
- **What:** pipeline/crossmodel_gpt.py + 테스트 병합 (하네스 3사이클
  APPROVE — cycle 1-2 REVISE가 라이브 치명 결함 2건 교정: 스키마 미포함
  프롬프트(전 트랜치 FAIL 예정이었음) · provenance 문서화). v1 완전
  준수 봉투 + codex-native fingerprint, MCP/지시파일 격리 플래그 +
  --json 감사 로그, 동일 입력 재시도(코칭 금지), frozen-frame 재구성
  (eafc32b 기준). 스위트 345 passed/1 skipped, verify-public PASS,
  문서 카운트 334→346. 모델 호출 0.
- **라이브 트랜치 PARKED:** 2026-08 신규 소유자 지시(Reader Surface
  Completion 우선 잠금, Phase 2도 zero model calls)에 따라 30콜 트랜치
  발사는 보류 — 소유자 액션 아이템으로 이관: 발사 명령
  `.venv/bin/python pipeline/crossmodel_gpt.py --frame original --out
  runs/crossmodel_gpt/wave1_original --limit 30` (D-P48 예외 하 합법,
  실행 시점은 소유자/차기 지시).
- **Revert:** 해당 커밋 revert.

## D-P50 — 소유자 지시 기록: Reader Surface Completion → Observatory Prep (2026-08-05)
- **서명:** 소유자 지시문 "DIRECTION: Reader Surface Completion →
  Observatory Prep (2026-08 revision, owner-approved verbally)" 전문.
- **효력:** 우선순위 잠금 — Phase 1(독자 표면 8항목) 완결/소유자 차단
  전까지 하위 단계 착수 금지; Phase 2는 스펙·스키마만(모델 호출 0).
  거버넌스 다이어트(스프린트당 신규 최상위 문서 ≤1, 신규 INV/BN 식별자
  금지), 독자 테스트 게이트(항목 1·2·4·8: 모의 독자 2인 통과 기록),
  게시·발송·계정·모델 호출·신규 fetch 필요 시 즉시 정지+큐 적재,
  사이클마다 본 원장에 완료 요약/소유자 액션/차기 계획 append.
- **기존 백로그 처분:** NB-04(교란 v2)·NB-05(전달 재구조 — Phase 1
  항목 1로 흡수)·NB-06(forward 메모)·NB-07(확장 PREP)·GPT 트랜치 →
  Phase 1 완결 후 재평가 대상으로 PARK. 기존 불변식·5게이트·동결
  규율·보호 경로 무변경.
- **Revert:** append-only 부인 항목으로만.

## D-P51 — P1-01 집행 기록: README 독자 표면 재작성 (D-P50 Phase 1 항목 1, 2026-08-05)
- **완료 요약:** 첫 화면 재구성 — 질문 1문장 → 답 2문장(분리 실재 +
  평판 기억: Hertz 78→55(−23)·Monsanto 28→58(+30), 평문) → 점 플롯 1장
  → 검증 명령 3줄. 첫 화면 전문 식별자 0 (D/Q/RP/BN/CP95/R3/E2/GA 부재;
  lint 요구 계층 표지는 평어 "wave 1"로 충족). 기존 내용 전부 접힘 아래
  보존(Scope & attribution — INV-14 문구 전량 유지 · 종전 headline 절
  원문 · Quickstart+GENERATED 블록 무변경 · "Want to check our work?"로
  기존 탐색 절 이동). README.ko.md 무접촉(F-01/F-02). lint_publication
  RC=0 · verify-public 5게이트 RC=0.
- **독자 테스트 게이트 (D-P50):** 모의 독자 2인 — 비기술 리크루터·
  회계사(AI 비전공) — 첫 화면만 제시, (a)(b)(c) 자기 언어 재진술
  **2/2 PASS** (기록: .direction/feedback/readertests/P1-01_reader{1,2}.md).
  통과 후 이들의 정직 혼동 5건을 자구 반영(AAER 풀네임·매칭 기준
  "industry, size, era"(CONTROL_CRITERIA 실측)·재호출 아님 명시·훈련
  힌트 포인터·통계 위치 포인터) — 추가 절만, 재게이트 불요 판단.
- **소유자 인지 필요 (수치 정정):** 구두 지시의 "Hertz −30 / Monsanto
  +16"은 커밋 아티팩트(analysis/baseline_table.csv)와 불일치 — 실측
  Hertz −23(78→55)·Monsanto +30(28→58). 표면에는 실측치 사용.
- **차기 계획:** P1-02 (Issues #1-3 이미지 절대 URL 패킷).
- **Revert:** 해당 커밋 revert (README.ko.md 무영향).

## D-P52 — P1-03 집행 기록: BN-12 해소 — 서수 라벨 + 그림 드리프트 게이트 (INV-03 공개, 2026-08-05)
- **완료 요약:** fig_dotplot x축 "Misstatement probability…" →
  "Evaluatee risk score (0-100, ordinal; original frame)", 주석
  "p=50"→"T=50", PNG 결정론 재생성(시각 델타는 라벨뿐 — 육안 대조 실측).
  의미 사이드카 게이트: 두 현세대 그림이 compute_sidecar()로 데이터
  sha256+라벨+주석을 기록, tools/verify_figures.py가 재계산-대조,
  verify-public 7번째 명령으로 추가(기존 6종 verbatim, INV-05). 렌더
  재생성은 pytest 게이트 내 실측. 레거시 3종 제외 사유는 BN-12 플립
  문안에 명기. 스위트 전체 green, verify-public(7명령) RC=0.
- **소유자 액션:** 없음 (BN-12 플립은 D-P50 지시 범위 내 집행).
- **차기 계획:** P1-04 (BN-11/14/18 영어 정본 배치 — 독자 게이트 대상).
- **Revert:** 해당 커밋 revert.

## D-P53 — P1-07 집행 기록: BN-07 잔여분 판정 — 기존재 확인 + 실측 완결 (2026-08-05)
- **완료 요약:** 지시 항목 7("REPRODUCING.md에 full-clone 요구 1줄")은
  기존재 확인 — REPRODUCING.md:59-66이 이미 전제·수리 명령(--unshallow)·
  CI fetch-depth:0 주석까지 명시(D123 스프린트 산출). 신규 작성 대신
  BN-07 해소 조건의 미실측 3요소를 실측 완결: full clone RC=0 ·
  depth-1 로컬 클론에서 명시 FATAL + RC=1 (fail-closed 실증). BN-07
  RESOLVED 플립(증거 인용). 파일 수정 0 (플립 외).
- **소유자 액션:** 없음. **차기:** P1-04 (영어 정본 배치, 독자 게이트).
- **Revert:** 플립 revert.

## D-P54 — P1-04a 집행 기록: BN-11 해소 — DECISION_TABLE 영어 정본 (INV-03 공개, 2026-08-05)
- **완료 요약:** Q-F11 기존 초안(docs/DECISION_TABLE_EN_DRAFT.md) 승격 —
  재번역 아님(사전 리뷰가 고아화 방지 지적): DRAFT 배너 제거,
  fig_tradeoff 블록 번역 삽입, 양방향 포인터, 초안 파일 동일 커밋 삭제.
  한국어 원본 DECISION_TABLE.ko.md 동결 보존. 수치 토큰 등가 기계 잠금
  (신규 tools/test_translation_equivalence.py — 레지스트리 확장형,
  포인터 줄 제외 규칙 명시). lint DOCS += en/ko 동일 커밋(D115/D118
  사슬 규칙). atlas 4파일의 한국어 인용 귀속을 .ko.md로 재지정(승격이
  만든 사실 오류의 기계적 수리 — 보호 경로, 서명 지시 범위 공개).
  독자 게이트 2/2 PASS(리크루터·애널리스트 — 기록 커밋). BN-11·Q-F11
  RESOLVED. 스위트 353/1, verify-public(7) RC=0, 문서 카운트 352→354.
- **소유자 액션:** 없음. **차기:** P1-04b (methodology_limitations 영어
  정본 — Q-F14 초안 존재 여부 확인 후 동일 패턴).
- **Revert:** 해당 커밋 revert.

## D-P55 — P1-04b(1) 집행 기록: methodology_limitations 영어 정본 채택 완결 (INV-03 공개, 2026-08-05)
- **완료 요약:** 기번역본(direction-loop 산출, 양방향 링크 기존재) 채택
  기계화 — lint DOCS += 영어 정본(en만; 동결 ko는 W3/(E) 규칙 제정 이전
  문언이라 편입 시 영구 적색 — 사유 주석 + 본 기록 공개, 수치 충실도는
  등가 테스트가 잠금), 등가 레지스트리 += 쌍(L-9 이후 EN 전용 성장
  규칙: EN 비교를 "## L-9"에서 절단, 양측 헤더에 스냅샷 문구 명시).
  잠금이 즉시 성과: 토크나이저 문말 마침표 아티팩트 2건 교정(문말 숫자
  허용으로 원리 수정), 캐너리 주석 한글 비표면 처리, lint 순응 편집
  2건(cross-model EXPLORATORY 라벨 · 교란 하한 W3 교정 문구 — EN 정본만,
  ko 동결 유지). Q-F14 RESOLVED. BN-14는 절반 잔존(오류 해부 문서
  영어화 — P1-04b2). 스위트 353/1, verify-public RC=0.
- **소유자 액션:** 없음. **차기:** P1-04b2 (error_analysis_wave2_holdout
  영어화 — Q-F15 스코프, 하네스 번역 사이클).
- **Revert:** 해당 커밋 revert.

## D-P56 — P1-04b2 집행 기록: error_analysis 영어 정본 — BN-14 완결 (INV-03 공개, 2026-08-05)
- **완료 요약:** Q-F15 기존 초안 승격(재번역 아님 — 사전 리뷰 적발 2연속:
  차기 번역 과업은 초안 존재 확인을 스펙 기본 절차로 상시화), ko 동결
  (.ko.md + 헤더 마커), 포인터를 H1 위 선행 줄로(등가 헬퍼 스트립 규약),
  "분식" 인용 로마자 처리(1:1 승인 일탈 주석), 레지스트리·lint DOCS(en)
  확장. 독자 게이트 2/2 PASS — 두 독자 모두 HUBG 자기 강등을 자발적으로
  핵심 정직성으로 지목. Q-F15·BN-14 RESOLVED. 스위트 353/1,
  verify-public RC=0, 문서 카운트 354 유지.
- **소유자 액션:** 없음. **차기:** P1-04c (ERRATA — append-only 설계
  중재를 사전 리뷰에 회부).
- **Revert:** 해당 커밋 revert.

## D-P57 — P1-04c 집행 기록: ERRATA 영어 정본 — BN-18 해소, P1-04 배치 완결 (INV-03 공개, 2026-08-05)
- **완료 요약:** ERRATA.md 영어 정본화(전문 번역 — 초안 부재 실측),
  ERRATA.ko.md 동결(선행 마커 1줄만 추가 — E-002 바이트 범위 보존 설계:
  동결 OWNER_FINAL_PACKET의 awk+sha256 검증 레시피가 ko에서 동일 해시
  a326427a… 재현 실측). 향후 정정은 영어 정본에만 append(양측 헤더
  명문). lint 편입(en만) + 규칙 (D) standalone 문구 승인 일탈 + 로마자
  2개소(*igo* 접속사 = E-002의 발견 그 자체). 독자 게이트 2/2 PASS.
- **보호 경로 공개:** ERRATA.md(.protected-paths:45) ·
  tools/lint_publication.py(:38) — D-P50 #4 서명 스코프, hunk 검증.
- **후속 후보(비차단):** 독자 지적 — 로마자 주석이 낯섦, R4 의미 미정의
  — ERRATA 자체는 원장이므로 손대지 않고 AUDIT_INDEX 용어행 보강 후보로만
  기록.
- **P1-04 배치 완결:** BN-11·BN-14·BN-18 전부 RESOLVED (D-P54..57).
- **소유자 액션:** 없음. **차기:** P1-05 (BN-13 재계산 게이트 배선).
- **Revert:** 해당 커밋 revert.

## D-P58 — P1-05 판정: BN-13 기충족 확인 — 중복 빌드 기각 (2026-08-05)
- **판정:** 사전 리뷰가 초안 과업을 REJECT — 계약한 3계열 재계산이
  tools/test_recompute_published.py(F-01, 06b9345·2ea5be8, BN-13 명시
  인용)로 기구현·기배선(verify-public pytest 게이트 내). 본 세션 실측:
  6 passed / 6.97s. 추가로 스펙의 두 함정 적발 — "정확 동치" 요구는 MC
  추정치에 비현실(풀 열거 순서 민감; 기존 ±3e-3 설계가 옳음), "게시
  계보 임포트" 지시는 동결 v1 스크립트(임포트 시 실행·동결 JSON 덮어쓰기·
  ~/aaer-data 필수)를 가리키는 덫. 초안 과업 파일 삭제, BN-13 플립만
  집행. 3번째 "기존재" 적발 — 사전 리뷰 계약의 실측 가치 반복 확인.
- **소유자 액션:** 없음. **차기:** P1-06 (BN-16 가드 배선, Q-F16).
- **Revert:** 플립 revert.

## D-P59 — P1-06 집행 기록: BN-16 해소 — 구조적 무네트워크·무코퍼스 게이트 (INV-03 공개, 2026-08-05)
- **완료 요약:** Q-F16 기본값 (A) 집행(D-P50 #6 서명) — Makefile 추가
  타깃 `verify-public-sandboxed`(기존 7명령 verbatim 유지, 추가만).
  가드 경유 전체 게이트 RC=0 실측; 부정 프로브 실측 2종(코퍼스 open ·
  네트워크 connect → SANDBOX-VIOLATION fail-closed). 가드 허용목록
  원리적 일반화: /System/Library 전체(SIP 봉인 읽기 전용 — matplotlib
  임포트가 폰트 자산·PrivateFrameworks를 스캔; 코퍼스 존재 불가) —
  종전 Fonts 단일 항목의 두더지잡기 3회를 종결. 자기 검증 6/6.
  일회 트랜스크립트(2026-07-22) → 매 실행 구조 강제로 전환.
- **보호 경로 공개:** Makefile(추가 타깃 1개, INV-05 6+1명령 무손상).
- **소유자 액션:** 없음. **차기:** P1-08 (리크루팅 패킷 — Phase 1 최종).
- **Revert:** 해당 커밋 revert.

## D-P60 — P1-08 집행 기록: 리크루팅 패킷 — PHASE 1 완결 (2026-08-05)
- **완료 요약:** PKT-P108(이력서 불릿 2 + LinkedIn 초안, 전 수치 RESULTS
  행 인용) 작성 → 독자 게이트 2인 PASS-with-edits → 편집 전량 반영:
  자화자찬 절 삭제·전문용어 평문화·행 인용 저장소측 이동·마스킹 후
  성능(p=0.0021, row 2)을 리드로 — 애널리스트가 지목한 "의도적 누락
  의혹"을 실측 수치로 해소(잔존 인지 ~22%의 불완전성도 병기). 게시
  경로는 소유자 수동(클릭 경로 포함, INV-18).
- **PHASE 1 완결 판정:** 8항목 전부 DONE/기존재 — P1-01(독자 게이트
  2/2)·02(패킷)·03(BN-12)·04a/b/b2/c(BN-11·14·18)·05(BN-13 기존재)·
  06(BN-16)·07(BN-07 기존재)·08(본 패킷). 금일 해소 BN 7종:
  BN-07·11·12·13·14·16·18. 소유자 액션 대기 패킷 2종: PKT-P102(이슈
  이미지)·PKT-P108(리크루팅).
- **차기 계획:** Phase 2 (스펙 전용, 모델 호출 0): P2-09 관측소 파일럿
  스펙 → P2-10 Sealed Analyst 스키마 → P2-11 클린 케이스 인벤토리 플랜.
- **Revert:** 해당 커밋 revert.

## D-P61 — P2-09 집행 기록: specs/OBSERVATORY_PILOT_V0.md (SPECIFICATION ONLY, 2026-08-05)
- **완료 요약:** D-P50 Phase 2 #9 — 관측소 파일럿 스펙 (229줄, 모델 호출
  0·호출 경로 코드 0). 사전 리뷰의 핵심 적발 반영: (1) 교차 컷오프
  대비가 오늘 기준 퇴화 가능(웨이브 사건 전부 knows-era · 홀드아웃 사건
  2026-02/03 — 현행 구독 후보 전원의 컷오프 이후) → off-diagonal 셀
  부재 시 NO-GO + LONGITUDINAL baseline leg 재프레임을 소유자 별도
  서명란으로 사전 등록 — "아무것도 측정하지 않는 스펙 서명" 차단.
  (2) tier별 측정 매트릭스(홀드아웃은 교란 arm 부재 — 설계상 PRIMARY
  identity-visible). (3) 프로브 인용 교정(holdout_probe.py·
  probe_verdict.py:name_match). (4) G2 어휘 수동 검증(0건 실측 — lint는
  specs/ 미스캔). 후보 로스터는 options/rationale/default로 미해소 유지.
- **보호 경로 공개:** specs/OBSERVATORY_PILOT_V0.md(.protected-paths) —
  D-P50 Phase 2 #9 서명 스코프. 스프린트 신규 최상위 문서 1/1 슬롯 소진
  (거버넌스 다이어트 준수 — P2-10/11은 specs/ 기존 계열·플랜 문서).
- **언어 관행 기록:** 스펙은 소유자 결정 문서로 한국어 혼용 —
  D114 경계(독자 대면 영어 정본)는 specs/ 내부 설계 문서에 부적용
  (cross_grader.md 선례).
- **소유자 액션:** 서명 시 §8 체크리스트 순서 실행 (§5.1 판정 포함).
- **차기:** P2-10 (Sealed Analyst 스키마 v0.1).
- **Revert:** 해당 커밋 revert.

## D-P62 — P2-10 집행 기록: Sealed Analyst 스키마 v0.1 스펙 (2026-08-05)
- **완료 요약:** specs/SEALED_ANALYST_V0_1.md (466줄, SPEC ONLY, 모델
  호출 0) — 3단 판정/반증 가능 콜/커버넌트 트리거(소유자 지시문 문언
  그대로 — provenance 헤더 명기), draft-7 스키마 내장(기계 검증:
  tools/check_sealed_analyst_spec.py — 스키마 유일성 + worked example
  인스턴스 검증), 필드별 결정론 채점 공식(상수 전수 sourced-or-
  preregistered), ETF 축은 비규범 부록(가격 데이터 부재 정직 명기,
  INV-23 취득 전제), RISK_SCORE_SEMANTICS 결정 어휘 매핑. 사후 리뷰가
  게임 가능 지평 결함 적발 — 이벤트 지평이 피평가자 출력(resolution_date)
  의존이던 것을 사전 등록 상수(case_cutoff + HORIZON_DAYS=730,
  HOLDOUT (g) 관행)로 교정: INV-03 동결 전 마지막 합법 시점의 1문장
  수리. 수리 후 fence check·전체 게이트 green.
- **스톨 사후 부검 (공개):** 하네스 1차 런 STALLED — 원인은 빌더가 아닌
  오케스트레이터: 체크 명령 수정 str.replace가 무매치 침묵 실패(세션 2번째
  동일 실수)해 백틱 파손 체크(사전 리뷰가 예언한 바로 그 결함)로 실행.
  교정: 체크를 도구 파일화(tools/check_sealed_analyst_spec.py), 이후
  편집 스크립트는 assert 매치 의무화(본 수리부터 적용).
- **보호 경로 공개:** specs/SEALED_ANALYST_V0_1.md(.protected-paths) —
  D-P50 Phase 2 #10 서명 스코프 (사이클당 신규 문서 1 슬롯).
- **소유자 액션:** 서명 시 §6 전제 체크리스트. **차기:** P2-11 (클린
  케이스 인벤토리 플랜 — Phase 2 최종).
- **Revert:** 해당 커밋 revert.

## D-P63 — P2-11 판정: 클린 케이스 인벤토리 플랜 기존재 — DIRECTION 백로그 완결 (2026-08-05)
- **판정:** D-P50 Phase 2 #11의 요구(N=3→15+ 로드맵 · cycle_001 창 관계 ·
  INV-23 플랜 한정)는 specs/POSTCUTOFF_ACCUMULATION.md(D111)가 기충족 —
  공급 산술(실측 0.6건/월)·N 타임라인 표·도착별 매칭 대조군 사전 배정
  규칙·감독 fetch 규율·분기 seal 검증 채널·정직 단서 3종 전부 기재.
  유일 문언 갭: 명시 N=15 행 부재 → 표 자체 관행으로 1행 보간
  (15/0.6≈25개월 → ~2028-08), assert-매치 편집. 4번째 "기존재" 적발.
- **D-P50 DIRECTION 완결 선언:** Phase 1 (8/8) + Phase 2 (3/3) 전 항목
  DONE/기존재. 금일 총계: BN 7종 해소(BN-07/11/12/13/14/16/18), Q-F
  4종 RESOLVED(Q-F11/14/15/16), 스펙 2종 신설(관측소·Sealed Analyst),
  소유자 패킷 2종(PKT-P102·P108), D-P50..D-P63 원장 14건, 독자 게이트
  5회(전부 PASS), 매 병합 verify-public RC=0 (사이클 중 7명령으로 확장 +
  sandboxed 변형 신설).
- **차기 계획 (D-P45 §2 규율):** 백로그 공백 → 생성형 보충 R1 렌즈(코드
  정합·숨은 버그 — 실코드 경로 정독)부터 로테이션 개시.
- **Revert:** 해당 커밋 revert.

## D-P64 — R1-01/02/03 집행 기록: 재개 멱등 + 교차모델 핀 + 레지스트리 커버리지 (INV-03 공개, 2026-08-05)
- **완료 요약:** R1 보충 리뷰 3건 수리 — (01) runner fp-sibling 재개
  경로: 현행 fingerprint 일치 sibling 존재 시 skip(모델 재호출·기록
  덮어쓰기 종결; _never_called 3차 실행 회귀로 봉인 — 종전 테스트가
  오동작을 인증하던 상태 교정). (02) crossmodel_gpt fail-closed 핀:
  -c model=<핀> 명령 주입 + _pin_matches 의미론(정확 일치 또는 핀+"-"
  접두) + MODEL_FALLBACK 수용 거부 + codex 버전 사전 lazy 검사(드라이런
  무서브프로세스 보존); 핀 상수는 OWNER-SET-BEFORE-LAUNCH 플레이스홀더 —
  플레이스홀더인 채 실행 시 기동 거부. (03) 블라인드니스 레지스트리에
  crossmodel_gpt 항목(완전 키 형상, 추가만) + 커버리지 테스트 —
  D-P49 발사 시 첫 산출물부터 카나리 스캔 안이며 게이트 적색 함정 제거.
  스위트 358/1, verify-public RC=0, 문서 카운트 354→359.
- **D-P49 발사 전제 갱신:** 발사 전 소유자가 CODEX_MODEL_PIN(+버전 핀)을
  실측 확정 문자열로 교체·서명해야 기동 가능(fail-closed가 강제).
- **보호 경로 공개:** pipeline/runner.py·pipeline/crossmodel_gpt.py·
  scoring/experiment_registry.json(추가 1객체) — R1 정합 수리, hunk 검증.
- **차기:** 보충 로테이션 R2 (통계 타당성·지표 선택).
- **Revert:** 해당 커밋 revert.

## D-P65 — R2 라운드 집행 기록: 통계 해석 공시 3건 (2026-08-05)
- **완료 요약:** R2 렌즈(통계 타당성) — 게시 수치 전수 재검증 clean
  (계수·추정량 외부 문헌 대조 포함, 오류 0). 발견 3건 전부 해석 공시
  갭: (R2-03) POWER_ANALYSIS 한계절에 검정 불일치(양측 AUC 계획 vs 등록
  1차 단측 순열; 보수 방향 명기) 직접 추가 — DP-Q3 증거 입력의 정직성
  보강, 시뮬레이션 기계는 리뷰어 kill대로 불제작. (R2-01/02) RESULTS
  행 2·11 limits 열 문장 추가는 서명 패킷 PKT-R2로 큐잉(게시 표면 —
  INV-18; DECISION_TABLE이 이미 지는 J14 비대칭 한계와 ECE 설계 유병률
  스코프의 행-단위 병기). lint·verify-public green.
- **소유자 액션:** PKT-R2 서명(문장 2개 + CLAIMS 동기화 — 명령 포함).
- **차기:** 보충 로테이션 R3 (외부 독자 전달 표면).
- **Revert:** 해당 커밋 revert.

## D-P66 — R3 라운드 집행 기록: 독자 표면 이음새 결함 5건 (INV-03 공개, 2026-08-05)
- **완료 요약:** R3 렌즈 — 문서별 독자 게이트가 구조적으로 못 잡는 문서
  간 이음새 결함 5건. 직접 수리 4건: (R3-01) **본 루프의 P1-01 재작성
  커밋(e05db78)이 낳은 편집 손상** — 중복 헤더·빈 섹션 삭제, 중복
  그림·명령 블록을 실제 <details> 접힘으로 전환(D-P51 기록의 "접힘 아래
  보존" 서술이 이제 사실) — 자기 결함의 정직 수리로 기록. (R3-02)
  README_DETAIL 유일 증거 링크 2건 404 수리(D110 이전 잔재; 링크 린터
  기계는 리뷰어 kill대로 불제작). (R3-03) README_DETAIL의 E-002 이전
  Spearman 0.337/0.265 → rev2 0.333/0.293 + 에라타 포인터(자기 에라타
  전파 실패 해소). (R3-05) CLAIMS.json 인바운드 링크 1줄. 패킷 1건:
  (R3-04) analysis/ 보호 — 스냅샷 마커 문안을 PKT-R2에 병합.
  lint·tools 스위트·verify-public green.
- **소유자 액션:** PKT-R2 (이제 문장 3개: RESULTS 행 2·11 + 스냅샷 마커).
- **차기:** 보충 로테이션 R4 (테스트 품질·커버리지 갭).
- **Revert:** 해당 커밋 revert.

## D-P67 — R4 라운드 집행 기록: 테스트 품질 4건 (INV-03 공개, 2026-08-05)
- **완료 요약:** 테스트 전용 번들 — (R4-01) 블라인드니스 회귀를 실송출
  지점 캡처 방식으로 교체: run_case가 실제로 넘기는 user_payload를
  가로채 검증 — 뮤테이션 실측(송출부를 FB-01 이전 제외식으로 되돌리면
  2건 적색, 복원 시 전green): FB-01 fix shape의 약속("rendered
  user_payload에 대한 회귀")이 이제 기계적 사실. (R4-02) INV-07 이력
  증명 check_history 무테스트 해소(공허 통과 클래스 적색화). (R4-03(ii))
  crossmodel 재개 동작 핀 + fingerprint-less 처리 단정(생산 코드
  무변경, 갭 주석). (R4-04) INV-01 우회 스캔 양성 대조군. R4-05는
  리뷰어 자체 제안대로 kill, R4-06은 E-003 초안 시점으로 연기.
  스위트 369/1, verify-public RC=0, 문서 카운트 359→370.
- **차기:** 보충 로테이션 R5 (제3자 재현 경로).
- **Revert:** 해당 커밋 revert.

## D-P68 — R5 라운드 집행 기록: 제3자 재현 경로 6건 (INV-03 공개, 2026-08-05)
- **완료 요약:** 헤드라인 판정 — Tier-1은 실제로 낯선 이가 걸을 수 있는
  경로(clean), Tier-2는 문서대로면 어떤 외부 재현자도 성공 불가한 상태
  였음. 수리: (R5-01) REPRODUCING §2 정직 스코프 — 값 재현 가능·바이트
  불가(살아있는 SEC 엔드포인트 vs 동결 코퍼스 핀), 도구 목록 완결,
  코퍼스 요청 채널, 제3자 UA 자기 신원 사용 명시(R5-06 흡수). (R5-02)
  verify-full 순서 교정 — verify_manifest를 재계산 4종 앞으로(명령
  verbatim 순수 재배열): 드리프트 코퍼스가 커밋 산출물을 덮어쓴 뒤
  "수치 불재현"으로 위장하던 파괴-후-검증 순서 종결 + git diff 경고
  문장. (R5-03) fetch 매니페스트 약속을 실제 구현체(holdout_rescan)로
  귀속 교정. (R5-04i) 일회 트랜스크립트(2026-07-22 게이트 세트로 날짜
  스코프) 대신 매 실행 구조 증명(verify-public-sandboxed)을 README·
  REPRODUCING 표면에 노출 — 재녹화는 차기 실행 세션으로 연기. (R5-05)
  ci.yml에 그림 게이트 1스텝 추가(additive) — P1-03가 만든 verify-public
  ↔ CI 동등성 갭(본 루프 자기 결함 2호)의 수리. R5-06 단독 kill.
  전 게이트 green (문서 카운트 370 유지).
- **보호 경로 공개:** Makefile(verify-full 순수 재배열 — verify-public
  무접촉)·.github/workflows/ci.yml(additive 1스텝, INV-24 강화 방향).
- **차기:** 보충 로테이션 R6 (전제 도전) — 1회전 완료 렌즈.
- **Revert:** 해당 커밋 revert.

## D-P69 — R6 라운드 + 로테이션 1 완결 기록 (2026-08-05)
- **완료 요약:** 전제 도전 렌즈 — 게시 수치 오류 0 유지; 전제 7종 공격
  후 생존(1종은 독립 재계산으로 — 외부 회의 독자용 검증 기록으로 커밋).
  발견 4건 전부 게시 표면 문장급(구조적 불가능→선언 컷오프+실측 비인지;
  FPR 편향 부호 미상 정정; A-type 탐지가능성 스크린 공시; 0% 분모) —
  PKT-R2 서명 패킷으로 통합(이제 문장 9개 + 동결 ISSUE 공지 3건 D99
  채널). **로테이션 1 결산 (R1..R6):** 발견 25건 — 빌드 16(전부 게이트
  green, 1건 뮤테이션 실증), 패킷 7(전부 PKT-R2), kill 2, 연기 2;
  자기 결함 2건 정직 수리(P1-01 편집 손상·P1-03 CI 동등성); 게시 수치
  오류 0 (2개 렌즈가 독립 재검증).
- **소유자 액션:** PKT-R2 서명 1회로 문장 일괄 적용 가능(명령 포함).
- **차기 (D-P50 로테이션 상승 규칙):** 로테이션 2 — 미검토 컴포넌트
  우선: R1 예약 목록(grader_runner·probe_runner·forward_validate/
  enumerate/prepare·calibration/synthesis·e2/e4 러너·sandbox_guard 손자
  전파·lint_doc_counts)부터, 전 소스·문서·테스트 모듈 개별 검토 완료까지.
- **Revert:** 해당 커밋 revert.

## D-P70 — 로테이션-2 C1 라운드: 첫 게시 수치 결함 2건 발견 — 수정 커밋 선행 (INV-03, 2026-08-05)
- **발견 (루프 최초 게시 수치 결함):** (C1B-01) 게시 unified_table.csv의
  Beneish m_flag가 동결 규칙의 정확한 보수 — 전 행 반전 (RESULTS 행 12
  수치들은 baseline_table 소스라 무영향 실측). (C1B-02) synthesis.json
  wave-1 fraud_median 60.0 → 참값 57.5 (짝수 n 추정자 오류; 유일한 짝수
  군). INV-03(c) 준수: 수정 커밋(m_flag 3개소 + statistics.median +
  발산 방지 테스트)을 재생성 전에 선행 — 재생성·E-003 초안·게시 표면
  인용 검증은 PKT-E003 서명 패킷. 산출물 원본 무접촉.
- **여타:** C1 half-A 5건 + half-B forward 3건 등록(전부 S; forward
  3건은 11월 창 표식). grader_runner·calibration NO-FINDING 커버리지
  기록. 장시간 렌즈 호출 kill 패턴에 리뷰 이분할 적응(6·7번째 kill).
- **소유자 액션:** PKT-E003 서명 (+ 기존 PKT-R2·PKT-P102·PKT-P108).
- **차기:** C1 잔여 8건 빌드 사이클.
- **Revert:** 해당 커밋 revert (게시 산출물 무영향 — 코드·테스트만).

## D-P71 — C1A 번들 집행 기록: 예약 컴포넌트 5건 (INV-03 공개, 2026-08-05)
- **완료 요약:** (C1-01) probe v2ds 산출물 파일명·루트 분리 — v1 결과의
  침묵 채택 종결(변형 구분 멱등). (C1-02) sandbox_guard 손자 전파
  실측 테스트(광고된 전-하위-프로세스 속성 봉인). (C1-03) DNS 탈출구
  차단(gethostbyname 계열) — 라이브 프로브 실측 SANDBOX-VIOLATION.
  (C1-04) lint_doc_counts가 pytest 수집 오류를 성공으로 오파싱하던 것
  fail-closed화(축소 카운트가 독자 표면에 쓰이는 경로 종결). (C1-05)
  holdout_probe 멱등 skip + 동결 트랜스크립트 침묵 덮어쓰기 거부.
  하네스 cycle 2 APPROVE. 스위트 376/1, verify-public RC=0, 문서 카운트
  372→377. forward 3건은 PKT-FWD 서명 패킷(보호 prefix, 11월 창 전 권고).
- **소유자 패킷 큐 (서명 대기 6):** PKT-E003(게시 수치 정정 — 최우선) ·
  PKT-R2(문장 9) · PKT-FWD(cycle_002 경화) · PKT-P102 · PKT-P108 ·
  PKT-Q1/Q4/Q6(스펙 실행).
- **차기:** 로테이션-2 다음 컴포넌트 군(미검토 잔여: memo 파이프라인·
  e2/e4 러너·payload_v2_extract·probe 스키마·runner_api 등 — 커버리지
  맵은 CYCLE_LOG 추적).
- **Revert:** 해당 커밋 revert.

## D-P72 — SAFETY HALT 기록: 장문 호출 스로틀 — 루프 정지 (2026-08-05)
- **판정:** 연속 4회 장문 리뷰 호출 실패(킬 2·900s 무출력 타임아웃 2),
  단문 프로브 즉답 유지 — 지속 세션의 장문 호출 스로틀 = 루프 규칙의
  쿼터 SAFETY HALT 해당. 반적용 상태 없음(사이클 전부 착지·게이트
  green). 재개 지침은 CYCLE_LOG 최종 항목(컴포넌트 목록·제외 범위·
  패킷 큐 포함).
- **정지 시점 성과 요약 (본 세션):** 사이클 32회 — D-P50 지시 완결
  (Phase 1 8/8 + Phase 2 3/3), BN 7종 해소, Q-F 4종 종결, 로테이션 1
  완주(발견 25) + 로테이션 2 C1(발견 12 — **최초 게시 수치 결함 2건
  발견·수정 커밋·E-003 패킷화 포함**), 독자 게이트 5회 전PASS, 뮤테이션
  실증 1회, 자기 결함 3건 정직 수리, 매 병합 verify-public RC=0.
- **Revert:** 해당 없음 (기록).

## D-P73 — 소유자 지시 기록: External Audit Feedback Integration (2026-08-05)
- **서명:** 지시문 전문 (verbally approved). D-P50을 대체; 미결 항목은
  Phase 6으로 승계. 하네스 자기 개선 3종(External Code Auditor 렌즈 ·
  모델 문자열 로깅 · 소유자 큐 노화 표시) 채택.
- **⚠ 소유자 액션 최상단 (매 요약 반복, 나이 표기):**
  ① **PKT-E003 서명** (0일 — 게시 수치 정정; 서명·재생성·push 전까지
  게시 수치 접촉 단계는 브랜치 빌드만) ② PKT-R2 (0일) ③ PKT-FWD (0일)
  ④ PKT-P102/P108 (0일) ⑤ 계정 리네임·Zenodo DOI(Q-R03, 2026-07-11부터
  **25일**)·BN-04 디스패치·인간 재채점자 모집·GPT 결정.
- **Phase 0 완료:** audit/FEEDBACK_TRIAGE.md (본 스프린트 유일 신규 문서;
  audit/ 보호 경로 — 지시 명명 스코프 공개). 판정: P0-1/P0-2 **HEAD에서
  확증**(글롭 선택 12개소 · 채점 fingerprint 부재 — 로테이션 렌즈의
  게이트-시스템 사각 실증), threat_model 주장 **반박**(파일 부재·SDK
  언급 0), 기해소 7건 검증 인용, 나머지 부분/미결 상 매핑.
- **차기:** Phase 1 (결과 선택 결정론) — 브랜치 audit-integration에서
  하네스 빌드.
- **Revert:** append-only 부인 항목으로만.

## D-P74 — P1a 집행 기록: 실행 매니페스트 + 글롭 선택 종결 (P0-1, 브랜치, 2026-08-05)
- **⚠ 최상단 소유자 액션 (나이):** PKT-E003 서명 0일 · PKT-R2 0일 ·
  PKT-FWD 0일 · PKT-P102/P108 0일 · Zenodo DOI(Q-R03) **25일** ·
  계정 리네임/BN-04/재채점자/GPT 결정 — 본 브랜치의 main 병합은
  PKT-E003 서명·push 후.
- **완료 요약 (audit-integration 브랜치):** 결과 파일 선택의 매니페스트
  전환 — runs/실험별 MANIFEST.json(17종 생성·커밋), aaer_eval/manifest.py
  로더(5중 fail-closed: 중복 ID·등록 누락·미등록 존재·해시 불일치·
  fingerprint-null 거부 플래그 — 각 테스트 실증), 글롭 선택 10개소 전환
  (baselines·decision_table·name_probes×2·buyer_metrics·analyze_rp05),
  산출물 무변경 실측(선택 리팩토링만). 하네스 3사이클 UNRESOLVED의
  원인은 스펙 내부 모순(README* 금지 vs RC=0 요구 — 오케스트레이터
  결함, 리뷰어가 정확 진단): docs-refresh는 병합 프로토콜대로
  오케스트레이터가 수행(377→399). 전 게이트 RC=0; 매니페스트 원장
  188엔트리 독립 재해시 0 불일치(리뷰어 미검증분 보완).
- **리뷰어 유예 채택:** holdout 분석기 로더 배선은 별도 스코프 후속
  (매니페스트는 사전 등록 상태로 커밋); e2/usage류 확장 자제.
- **모델 문자열 (지시 요구):** builder=codex-cli 0.144.6 기본 모델 ·
  reviewer=claude 2.1.221 (meta.txt 기록).
- **차기:** P1b (채점 fingerprint — P0-2).
- **Revert:** 브랜치 revert.

## D-P75 — Phase 1 완결: P0-2 채점 fingerprint + 발산 감사 (브랜치, 2026-08-05)
- **⚠ 최상단 소유자 액션 (나이):** PKT-E003 서명 **0일** (본 브랜치 병합
  게이트) · PKT-R2/FWD/P102/P108 0일 · Zenodo DOI(Q-R03) **25일** ·
  계정 리네임/BN-04/재채점자/GPT 결정.
- **P1b:** grader_runner에 8필드 fingerprint(각 필드가 지문을 바꾸는
  것 실증 테스트) + fp-일치 skip + legacy fail-closed(--accept-legacy-grade
  옵트인, FB-03 선례) + 불일치 시 형제 파일 + R1-01 교훈(형제 멱등).
  하네스 cycle 2 APPROVE. 모델 호출 0.
- **발산 감사 (Phase 1 step 4) — 판정:** 전 분석기 재실행 대조 결과,
  게시 수치 이탈은 **정확히 E-003 기지 델타 2건뿐** (synthesis
  fraud_median 60.0→57.5 · unified_table m_flag 반전) — E-003 검증
  주장의 상향 기록(그 외 이탈 0). 부수 판정 2건: (i) BUYER_METRICS
  이탈은 감사 절차 오호출(--logs-dir 미지정)의 거짓 양성 — 도구는
  usage 0건·단가 미입력에 fail-closed함을 실측 확인. (ii) rp05_stats
  이탈 = P1a 매니페스트의 시대(era) 미스코프 (전 세션 자기 결함 —
  RP-05 동결 산출물은 2026-07-06 창의 wave-1 8케이스인데 현재 디스크
  전체를 핀): run_20260706T* 로 시대 스코프 교정 — 생성기의 드롭 가드가
  침묵 축소를 거부(설계 의도 실증)해 삭제-재생성의 명시 정정으로 수행,
  교정 후 재생성이 커밋 산출물과 **의미 동일(parsed-equal)** 실증(잔여
  24줄은 키 순서). 전역 runs 원장 재생성(--write-manifest). 후속 등록:
  생성기의 generated_from_commit 필드가 무변경 재생성에도 전 파일을
  더럽히는 처닝 와트 — 내용 무변경 시 무기록으로 개선 (차기).
- **게이트:** 402/1 green · verify-public RC=0 (브랜치). main 병합은
  PKT-E003 후.
- **차기:** Phase 2 (스키마 v2 하드 제약 — 서명된 플랜 실행).
- **Revert:** 브랜치 revert.

## D-P76 — Phase 2 완결: 스키마 v2.1 하드 제약 (브랜치, 2026-08-05)
- **⚠ 최상단:** PKT-E003 서명 0일 (병합 게이트) · Zenodo DOI 25일 · 기타
  패킷 큐 동일.
- **완료:** llm_output_v2 → v2.1 — checklist 정확 8(enum CL1..CL8),
  top_signals enum, fingerprint 필수 승격, 커밋 해시/accession/케이스 ID
  패턴 제약; aaer_eval/output_contract_v2.py 의미 검증기(스키마 비틀기
  금지 지시 준수 — ID 집합 동치·tier/score 정합 양방향·top_signals ⊆
  checklist), 위반 클래스별 발화 테스트. v2.0 구조 diff-lock은 문서화
  대체(침묵 삭제 아님). v1 byte-동결 실측(diff 0줄). 하네스 cycle 2
  APPROVE. 스위트 412/1, validate_schemas PASS, verify-public RC=0.
- **차기:** Phase 3 (verify-claims 타깃 + CLAIMS 게이트 구동 + 그림
  게이트 확장).
- **Revert:** 브랜치 revert.

## D-P77 — Phase 3 완결: 검증 표면 정직화 (브랜치, 2026-08-05)
- **⚠ 최상단:** PKT-E003 서명 0일 (병합 게이트) · Zenodo DOI 25일 · 패킷
  큐 동일.
- **완료:** 재현 사다리 명명 — verify-claims(재계산+재계산 테스트+그림
  게이트+CLAIMS 커버리지 반복자) · verify-fixture-pipeline ·
  reproduce-corpus/rerun-evaluatee(정직 거부 스텁, 전제 echo+exit 1).
  verify-public 7행 verbatim 유지(diff 실측 — 제거 1행은 .PHONY 확장).
  CLAIMS.json v2: per-claim recompute{command,artifacts}+limitation_ref,
  기존 verbatim-lock 열 무변경. verify_claims_coverage: RESULTS 행
  1..13 전수 존재·아티팩트 실재·명령 유효 — 결손 시 명명 실패(테스트
  실증). 그림 게이트 5종 전커버(현세대 2: 사이드카+config-hash · 동결
  3: bytes-pin+정직 주석, figures.manifest.json). 하네스 cycle 1
  APPROVE. 스위트 414/1, verify-claims RC=0, verify-public RC=0.
- **차기:** Phase 4 스펙 3종 (P4a 교란 v2 → P4b 전향 지표 → P4c 인간
  블라인드 재채점) — 각각 사이클당 문서 슬롯 1.
- **Revert:** 브랜치 revert.

## D-P78 — P4a 완결: specs/PERTURBATION_V2.md (브랜치, 2026-08-06)
- **⚠ 최상단:** PKT-E003 서명 **1일** (병합 게이트) · Zenodo DOI **26일** ·
  패킷 큐 동일 (PKT-R2/FWD/P102/P108 1일).
- **완료:** 대칭 2×2 교란 설계 스펙 — J14 비대칭 종결 설계(승계 근거
  명시), 케이스별 짝지은 델타 추정자, 정체 제거 arm과 연대기 보존
  arm 분리(CL7 상호작용 문서화), accession 가명화·상대 날짜 이동·회계
  기간 안정성 요건, 신호 보존 검증 플랜(결정론 탐지기 불변), 실행 전제
  체크리스트(서명 활성), 잔존 채널 정직 절(L-5/L-9). PKT-Q9 흡수.
  하네스 cycle 2 APPROVE. lint·verify-public green.
- **차기:** P4b (PROSPECTIVE_METRICS).
- **Revert:** 브랜치 revert.

## D-P79 — P4b 완결: specs/PROSPECTIVE_METRICS.md (브랜치, 2026-08-06)
- **⚠ 최상단:** PKT-E003 서명 1일 · Zenodo DOI 26일 · 패킷 큐 동일.
- **완료:** 결과변수 분류 분리(4.02/재작성 Big-R·little-r/조사 공시/
  소장/AAER — 결과별 기저율·시차 주석), 지표 계약(PR-AUC·PPV·top-k
  정밀도·1000사당 경보·건당 검토 수·6/12/24개월 지평, 결정론 정의),
  봉인 전향 통합(INV-22 경계 — cycle_001 무접촉·전 유니버스 점수 보존
  독트린·임계 동결), cycle 2 유니버스 확장 산술, 소N 정직 절, 소유자
  결정 3건 미해소 유지. PKT-Q6 지표 반 흡수. 하네스 cycle 1 APPROVE.
  lint·verify-public green.
- **차기:** P4c (HUMAN_BLIND_REGRADE) — Phase 4 마지막.
- **Revert:** 브랜치 revert.

## D-P80 — P4c 완결: specs/HUMAN_BLIND_REGRADE.md — Phase 4 종결 (브랜치, 2026-08-06)
- **⚠ 최상단:** PKT-E003 서명 **1일** (병합 게이트) · Zenodo DOI **26일** ·
  패킷 큐 동일 (PKT-R2/FWD/P102/P108 1일). 신규: PKT-P4C-SAMPLE (0일).
- **완료:** 인간 블라인드 재채점 사전 명세 — 결정론 표본(25%, Hamilton
  비례배분, 시드=고정 리터럴‖동결 eval_spec.md 바이트의 SHA-256, 층 키
  `"<tier>|<arm>"`를 `TIER_BY_DIR`(scoring/ 상대) 조회로 기계 정의,
  미매핑 fail-closed), 필드별 삭제표(schemas/llm_output.json 전수 대조),
  quadratic-weighted kappa(반열린 실수 구간 밴드 사전 등록), 전건 불일치
  공개, 두 인간 합의 전속(모델 타이브레이크 금지), 소유자 전속 모집 패킷.
  **정직 표기:** dim1 제외·dim2 블라인드 채점 불가로 제거·dim3는
  `underpowered`(e_d=7 < 선례 하한 20)로 밴드 라벨 없이 불일치 목록만 —
  밴드 라벨을 받는 차원은 `dim4_blind` 하나뿐임을 문서에 명시.
- **하네스:** cycle 5 APPROVE (REVIEW→REVISE 5회, 상한 없음 — 지시 규정).
  수렴: 6건 → 4건 → 1건 → 2건 → 0건. 게이트 약화 0건.
- **모델 문자열 (지시 요구 — 본 사이클 전수 기록):** 오케스트레이터
  claude-opus-5[1m] · 빌더 codex-cli 0.144.6 (cycle 1-5) · 리뷰어
  `claude -p --model opus` CLI 2.1.222 (cycle 1 재실행·2·3·4·5).
  **cycle 1 최초 리뷰어 호출은 핀 부재로 Fable 5를 상속해 주간 한도로
  사망** — 하네스 모델 핀 부재의 실증. `~/tools/harness/run_task.sh`에
  `HARNESS_CLAUDE_MODEL`(기본 opus) 도입 + 양 호출부 `--model` + 호출별
  로깅 + meta.txt `claude_model=` 기록으로 수리.
- **자기 결함 정직 기록 2건:** (i) 오케스트레이터 수정안 7의 유효 pair
  추정치 "약 9-10"이 오산 — 리뷰어가 문서 자체 공식을 실제 모집단에
  적용해 7로 정정(cycle 2). (ii) cycle 2 리뷰어 항목 2의
  `cross_grader_skeleton.py:36-43`·"저장소 상대" 표현이 오류 —
  오케스트레이터가 무검증 통과시켰고 cycle 4에서 리뷰어가 자기 오류를
  발견, 33-40·"scoring/ 상대"로 정정(그대로 두었으면 모집단 공집합).
- **게이트:** verify-public RC=0 (7행 전부) · 414 passed/1 skipped ·
  reproduce 100/100 · lint_publication · lint_doc_counts(538/415) ·
  verify_blindness · verify_manifest · verify_figures. main 병합은
  PKT-E003 후.
- **차기:** Phase 6 표면 작업 — (a) 다중 검정 문단 (b) README November
  2026 절 (c) candidates PENDING 승계 헤더는 **동결 산출물 접촉 →
  소유자 패킷** (d) 소유자 큐 승계분.
- **Revert:** 브랜치 revert.

## D-P81 — Phase 6 (a) 완결: docs/MULTIPLE_TESTING.md — 다중 검정 공개 (브랜치, 2026-08-06)
- **⚠ 최상단:** PKT-E003 서명 **1일** (병합 게이트) · Zenodo DOI **26일** ·
  PKT-R2/FWD/P102/P108 1일 · Q-F18 (P4c 표본률 — 모집 게이트) 0일.
- **완료:** 감사 지적 24번(다중 검정 문단 부재 — grep 0건 실측) 해소.
  확증(confirmatory) 계열 열거 = 순열·Fisher p 11개를 두 동결 산출물
  (`analysis/results_stats.json`, `analysis/wave2_results.json`)에서 읽어
  각각의 사전등록 plan 절·freeze 커밋을 인용해 분류; 탐색(EXPLORATORY)
  L4·E2 계열은 계열에서 분리(무풀링 규율 준수). Holm step-down은
  `tools/multiple_testing.py`(stdlib 전용 — INV-11 무증설), 결정론,
  단조성 강제 포함; 산출물 부재 시 `FileNotFoundError` fail-closed(테스트
  실증). 신규 테스트 3종(수기 계산 대조 + fail-closed).
- **정직 공개 (실질):** 보정 후 미생존 1건 — wave-1 perturbed Fisher
  `p=0.059613`(보정 전후 동일, 계열 최대값)은 **결론과 같은 문장에서**
  유의하지 않다고 기술. 이 Fisher 값은 RESULTS row 2가 애초에 발행하지
  않은 동반 통계이며, 감추지 않고 공개하는 쪽을 택했다. 나머지 확증
  결론은 보정 후에도 유지(최대 조정 p=0.009435).
- **계열 선택의 보수성 실증:** 리뷰어가 wave-1/wave-2 분할 계열(4+2)과
  통합 계열(6)을 양쪽 계산해 통합 쪽 조정 p가 **엄격히 더 크다**는 것을
  확인 — 계열 프레이밍으로 유의성을 만들어낼 수 없음.
- **발행 수치 무변경 실측:** RESULTS.md·METHOD.md diff는 포인터 줄 각
  1행뿐 — 셀 값 변경 0. README/REPRODUCING은 docs-refresh 카운트
  (415→418) 갱신뿐. FB-09(ac29b6d) 신규파일+포인터 선례 준수.
- **하네스:** `run_task.sh --until-approve` cycle 3 APPROVE (REVISE 2회).
  **모델 문자열:** meta.txt `claude_model=opus` (핀 도입 후 하네스가 직접
  기록) · claude 2.1.222 · codex-cli 0.144.6 · 오케스트레이터
  claude-opus-5[1m].
- **게이트:** verify-public RC=0 · 417 passed/1 skipped · reproduce 100/100
  · lint_doc_counts(538/418) · blindness · manifest · figures.
  main 병합은 PKT-E003 후.
- **차기:** Phase 6 (b) README November 2026 절. (c) candidates PENDING
  승계 헤더는 동결 커밋 산출물 접촉 → 소유자 패킷(빌드 아님).
- **Revert:** 브랜치 revert.
## D-P82 — PKT-E003 소유자 서명·집행: E-003 게시 + 산출물 재생성 (2026-08-06, OWNER DECISION SESSION)
- **⚠ 최상단:** PKT-E003 **서명 완료 (본 엔트리)** — 병합 게이트 해제
  (병합·push 자체는 소유자 별도 지시 대기, Item 2) · Zenodo DOI **26일** ·
  PKT-R2/FWD/P102/P108 1일 · Q-F18 0일.
- **서명 (verbatim):** 소유자 답변 **"sign"** (2026-08-06, owner decision
  session, 옵션 A). INV-18 사슬: 발견(D-P70 C1B) → 격리 등록(0bf612e 코드
  선행 커밋 + 발산 잠금 테스트) → 검토 패킷(PKT-E003) → **인간 서명(본
  엔트리)** → 동결 텍스트(ERRATA.md E-003) 완결.
- **집행 (서명 후 본 세션):**
  ① ERRATA.md에 E-003 영어 정본 추가(append-only; 패킷 초안 기반, 게시
  표면 60.0 인용 grep 실측 결과 "인용 0건 — 전부 무관한 CP 상한 60.0%"
  명기). ② `analysis/synthesis.py` 재생성 — synthesis.json 1행 delta
  (wave-1 fraud_median 60.0→57.5), unified_table.csv m_flag 전 m-행 정정
  (m > -1.78 규칙 실측: -1.527→1, -2.426→0). 기지 delta 2건 외 변경 0
  (Phase-1 발산 감사와 일치). 원본은 git 이력 보존(10a97fe 이전) —
  병행 게시. ③ `tools/test_translation_equivalence.py` ERRATA 쌍에
  en_truncate `"\n## E-003"` 지정 — methodology_limitations 쌍의 L-9 절단과
  동일한 설계 기제(동결 ko 스냅샷 E-002 종료, 이후 영어 전용). E-001/E-002
  구간 수치 동치 검사는 전량 유지 — 게이트 약화 아님. ④ 재생성 부산물
  `analysis/out/synthesis_exclusions.json`(excluded_n=0, 비추적 이력)은
  미커밋 관례 유지로 제거.
- **게이트 (집행 후 실측):** `make verify-public` RC=0 — pytest 417 passed/
  1 skipped · reproduce · lint_publication · lint_doc_counts(538/418) ·
  verify_blindness PASS · verify_manifest · verify_figures OK.
  divergence-lock `analysis/test_synthesis_flag_convention.py` 2 passed.
- **차기:** 소유자 결정 세션 Item 2 — push/정합 결정 (로컬 main 41 ahead
  미푸시 · audit-integration +17 · ~/Documents 23 behind).
- **Revert:** 브랜치 revert (ERRATA는 append-only — revert 시에도 후속
  엔트리로만 정정).
## D-P83 — OWNER DECISION SESSION 일괄 서명·집행 (2026-08-06)
- **⚠ 최상단:** PKT-E003 서명·집행 완료(D-P82) · PKT-R2 집행 완료(본
  엔트리) · **잔여 소유자 수동 액션은 close-out 표 참조** (Issue 공지 3건
  포스팅 · P102 이미지 수정 · Zenodo DOI · P108 포스팅).
- **서명 (verbatim, 전 항목 공통):** 소유자 답변 **"sign all sections
  with your recommend options that you believe the choice would most
  contribute for the project."** (2026-08-06). 위임 범위: 각 항목의 권고
  옵션 채택. 세션 규율 준수: 빌드 작업은 서명만 기록하고 TASK로 큐잉
  (본 세션 무빌드).
- **집행 완료 (본 세션 커밋):**
  ① **[2A]** main ← audit-integration ff-only 병합 (011180d), push는 본
  엔트리 커밋 후 1회 — CI 3.12 잡 결과 확인 의무 (INV-24).
  ② **[PKT-R2]** RESULTS 행 1·2·3·4·8·9·10·11·13 limits 추가 문장 9건
  (패킷 문언 그대로) + CLAIMS.json char-lock 동기(테스트 2 passed) +
  README·METHOD·README_DETAIL "structurally impossible" → 선언 컷오프+
  실측 비인지 문언(패킷 edit 4; README_DETAIL.md:118의 동일 문구 1건은
  패킷 명시 밖이나 동일 주장 표면이라 포함 — 본 문장으로 공개) +
  error_analysis 스냅샷 블록쿼트(edit 3; 등가성 테스트 선두 포인터
  인식자에 "> Snapshot of " 추가 — 본문 수치 잠금 무변경) + README 검증
  기록 링크(edit 9). Edit 8 공지 3건은 패킷에 포스팅 문안으로 작성 —
  포스팅은 소유자 수동 (D99). 커밋 38c0c77.
  ③ **[Q-F12/(A)]** ENGINE_DECISION v2 등재 (f43f36c) — §A 정확 FPR 매칭
  · §B 확장 대조군 목표 n≈30 (규모만 서명 — 조달·fetch·채점 지출은
  INV-22/23 별도 게이트) · §C 공개 절 내장 · 영어 정본 (D114).
  ④ **[PKT-INV11]** INV-11 dev-toolchain 예외 개정 등재 + sync_context
  재생성 (6f04e2e). 배선은 TASK_INV11 큐잉 (pip-compile은 소유자 입회
  세션 한정 — INV-23).
  ⑤ **[Q-F18/(A)]** 25% 유지, dim3 underpowered 정직 발행 — 모집 게이트
  해제. ⑥ **[Q-F13]** 기본 옵션 서명, TASK_QF13 큐잉. ⑦ **[PKT-FWD]**
  서명, TASK_FWD 큐잉 (cycle_002 준비 전 실행 권고). ⑧ **[PKT-Q1]**
  집행 TASK_Q1 큐잉. **[PKT-Q4]** INV-12 개정 기등재(D-P44b/D-P45) 확인
  — 런 발사는 소유자 수동 유지. **[PKT-Q6]** Nov 2026 시계 — 무조치.
  ⑨ **[계정]** 핸들 유지 결정: lastwhisper906-gif (리네임 없음 — P102/
  Zenodo/P108 시퀀스 차단 해제; 위임 하 판단: 계정 변경은 세션 불가
  액션이므로 유지가 유일한 집행 가능 권고).
  ⑩ **[주차 6건]** Q-F02·Q-F07·Q-M01·Q-M05·Q-M06·Q-M07 → PARKED (각
  재부상 조건 명기; Q-M06은 차기 감독 미터링 세션 최우선 후보).
  ⑪ **[Q-F19]** candidates.json 승계 헤더 사안 신규 등재 (등재만 —
  처분은 기본값 (A) ERRATA-인접 공개, 무응답 시).
  ⑫ **[정정]** Q-F14/15/16 상태줄 OPEN 잔존 표기 → RESOLVED 정정
  (헤더·D-원장이 정본; 갱신 누락 bookkeeping).
  ⑬ **[하네스 핀 추인]** HARNESS_CLAUDE_MODEL=opus (run_task.sh 기본값,
  빌더·리뷰어 --model 명시 + meta.txt 기록)를 상시 결정으로 추인 —
  세션 대화형 /model 전환과 무관하게 하네스 호출은 핀 고정.
- **게이트:** 본 엔트리 커밋 직후 make verify-public 실측 → push → CI
  3.12 확인 (결과는 close-out 보고).
- **Revert:** 항목별 커밋 revert + 본 엔트리 후속 정정 엔트리.

## D-P84 — [DRAFT — 소유자 서명 대기] 스키마 채널 누출 봉합 공개 (INV-09/INV-03)
- **Status:** DRAFT — 세션(harness v4 cycle 001, R1-2)이 작성. 서명 전까지
  미집행 게시 없음. 코드 변경 자체는 커밋됨(전향 런 전용 — 동결 런 무접촉).
- **발견 (channel):** `--json-schema`로 피평가자에게 송출되는 출력 스키마와
  Codex 프롬프트 내장 스키마가 송출 전 값 수준 가드(guard_payload)를 거치지
  않았고, `schemas/llm_output.json`의 description 필드에 채점 루브릭 문구
  ("fraud 어휘 금지 (red-team #1)"·"문장 인용을 쓰면 날조로 채점(차원 4=0)"
  등)가 있어 EVALUATEE_FORBIDDEN_MARKERS의 "fraud"가 문자 그대로 피평가자
  가시 채널에 실려 나갔다 — INV-09 "전 페이로드 값 수준 스캔" 주장 자가
  위반. 케이스별 정답은 누출되지 않음(문구는 전 케이스·전 군 균일).
- **조치 (커밋됨):** ① `pipeline/runner.derive_model_schema`가 모델 송출
  스키마에서 description 키를 전량 제거(_strip_descriptions — 스키마 파일
  자체는 무변경, 검증 의미론 불변) ② `cli_client.call_model`이 송출 스키마
  JSON도 guard_payload 스캔 ③ `crossmodel_gpt.run_case`가 user_payload
  대신 송출 프롬프트 전문(task+스키마+페이로드)을 스캔. 테스트 3종 추가.
- **핑거프린트 영향 (전향 런만):** 실제 송출 스키마 문자열이 달라지므로
  Claude arm의 argv·GPT arm의 prompt_sha256이 이후 런부터 변한다.
  `compute_fingerprint.schema_sha256`은 스키마 파일 해시라 무변경.
  동결 runs/ 산출물 무접촉 (git 확인).
- **Options:** (a) 본 공개를 ERRATA 없이 D-원장 엔트리로 승인 (권고 —
  게시 수치 무영향, 방법론 주장 문구의 자가 위반 봉합) (b) ERRATA 병행
  등재 (INV-09 주장을 게시문에서 강하게 낸 표면이 있다고 판단 시)
- **Basis:** INV-09 · INV-03 · METHOD.md §3 · reviews/cycle-001.md R1-2
- **Revert:** 커밋 revert (가드 완화이므로 revert 시 사유 기록 의무).

## D-P85 — [DRAFT — 소유자 서명 대기] ERRATA E-004 초안: wave-2 대조군 5건 후신 사명 반입 (OV-002/§5-1)
- **Status:** DRAFT — 세션(harness v4 cycle 001, R1-3)이 작성. ERRATA.md는
  본 세션이 접촉하지 않았다 — 등재는 소유자 서명 후 append-only로만.
- **제안 ERRATA 본문 (E-004, ready-to-sign):**
  - **결함:** `tools/run_wave2_scoring._cutoff_name`이 EDGAR 청크 파일
    (`CIK…-submissions-001.json` — 사전순으로 본 파일보다 앞서고 formerNames
    부재)을 먼저 만나면 첫 파일에서 break하여 본 파일의 formerNames 재구성을
    건너뛰었다. 결과: 동결 `data/evaluatee/cases_wave2.json` 대조군 22건 중
    5건이 컷오프 이후 사명으로 송출됨 — case_51(Valaris↔Ensco)·case_49
    (Iovance↔Lion Bio)·case_63(SITE Centers↔DDR)·case_44(Adamas Trust↔NY
    Mortgage Trust)·case_69(Artivion↔CryoLife). 아티팩트 자체 `_meta`
    "name_convention: 컷오프 시점 사명" 및 OV-002와 모순 — 필드 값 수준의
    §5-1 look-ahead.
  - **영향:** 실험군 9건 전부 무영향(검증 완료 — 프로젝트 핵심 주장 유지).
    영향 범위는 대조군 사명 필드 한정. case_44/69는 게시된 wave-2 오탐 2건
    (`analysis/error_analysis_wave2_holdout.md`)과 겹침 — 후신 사명 노출이
    오탐에 기여했을 가능성은 판정 불가로 정직 공개(피평가자는 사명으로
    사후 지식을 상기할 수 있으나 방향 효과 미측정).
  - **조치 (코드만, 커밋됨):** `_cutoff_name`이 존재 파일 전부를 순회한 뒤
    낙하하도록 수정 + 회귀 테스트 3종(`tools/test_run_wave2_scoring.py`).
    동결 `cases_wave2.json`·`runs/` 무접촉 (INV-06). 재실행·병행 경로 산출은
    소유자 결정 사항(하단 Options).
  - **비영향 확인:** `tools/run_control_v2_scoring.name_at_cutoff`는 본
    파일(`CIK{cik}.json`)만 읽는 구조라 본 결함 비해당.
- **Options:** (a) E-004 등재 + 정정 사명으로 대조군 5건 재실행을 신규 분리
  경로(`runs/wave2_rev3/` 류)에 병행 산출 — E-001 판형 (b) E-004 등재만
  하고 재실행은 보류 — 오탐 해석 각주만 게시 표면에 추가 (권고: 소유자
  판단 — 재실행은 모델 호출 비용·INV-19 격리 경로 필요)
- **Basis:** OV-002 · PROJECT.md §5-1 · INV-03/INV-06 (disclose-dont-revise)
  · reviews/cycle-001.md R1-3 검증 노트 (~/aaer-data/_rp08 대조 실측)
- **Revert:** 코드 revert 시 후속 엔트리로 사유 기록 (ERRATA append-only).

## D-P86 — [DRAFT — 소유자 서명 대기] 특성화 공개: 쓰기 시점 검증 이전 draw 기록 15건의 스키마 위반 (ERRATA 후보)
- **Status:** DRAFT — 세션(harness v4 cycle 002, R2-2)이 작성. 동결
  기록·ERRATA.md 무접촉; 등재 여부는 소유자 서명 사항.
- **사실:** `runs/**` 아래 llm_output 형태 기록 508건 전수 검증 결과,
  15건이 현행 동결 스키마(FULL_OUTPUT_SCHEMA)에 실패한다. 전부 draw
  디렉토리 도입 커밋(62fe360)이 쓰기 시점 검증 도입(e1b5a43)보다 앞서는
  pre-validation 기록. 실패 사유는 두 종:
  - `overall.top_signals` maxItems 5 초과 — 14건:
    runs/draw_k3/w1_controls/draw_2/case_24, case_37 ·
    runs/draw_k3/wave2/draw_2/case_45 ·
    runs/hardening/draws/draw_3/case_14, draw_4/case_12, draw_5/case_12,
    draw_5/case_13 · runs/holdout/mainscore_redraw/draw_5/case_73 ·
    runs/rp07/draws/draw_3/case_08, draw_3/case_12, draw_5/case_09,
    draw_5/case_12 · runs/wave2/perturbed_redraw/draw_2/case_66,
    draw_3/case_66 (모두 .json)
  - `checklist[3].evidence` minItems 1 위반 — 1건:
    runs/draw_k3/wave2/draw_3/case_67.json
- **하류 소비:** draw 소비 경로(`scoring/analyze_hardening.py`,
  `analysis/draw_k3_analysis.py` 등)는 `misstatement_probability`만
  읽으며, 이 필드는 15건 전부에서 스키마 유효 — 게시 수치 무영향.
- **조치 (코드만, 커밋됨):** `pipeline/test_output_schema_enforcement.py`
  스위프를 runs/**·pilot 전체 rglob로 확장, 15건은 경로+실패 키워드
  명시 허용목록으로 열거(존재·기재 사유 일치까지 단언) — 16번째 위반
  기록은 어디에 생겨도 pytest 실패. 동결 기록 무수정 (INV-06).
- **Options:** (a) ERRATA 등재 없이 본 엔트리를 특성화 공개로 종결
  (권고 — 게시 수치 무영향, 소비 필드 유효) (b) ERRATA 병행 등재
  (draw-robustness 표를 게시 표면으로 강하게 낸다고 판단 시)
- **Basis:** INV-02(스키마 준수)·INV-06 · reviews/cycle-002.md R2-2
- **Revert:** 허용목록 축소는 후속 엔트리로 사유 기록.
- **REVISION 2026-08-27 (harness v4 cycle 003, R3-12 — 주장 정밀화):**
  위 원문(보존)의 "16번째 위반 기록은 어디에 생겨도 pytest 실패"는 발견
  전제조건을 누락한 과잉 진술이었다. 당시 발견 술어는
  `misstatement_probability`와 `checklist` **둘 다** 가진 dict만 스캔 —
  필수 키 자체가 빠진 기록(가장 나쁜 위반 클래스)과 미래 v2 기록
  (`misstatement_risk_score`)은 발견조차 되지 않았고, fp-sibling은 스캔
  제외였다. cycle 003 R3-12에서 술어를 확장: v1/v2 확률 필드·checklist·
  case-패턴 파일명 어느 것으로든 발견, v1은 llm_output·v2는
  llm_output_v2+validate_v2로 검증, 알려진 타계약 가족(채점·프로브·진단
  페이로드 — 자체 게이트 관할)을 제외한 분류 불가 case-패턴 파일은 실패,
  fp-sibling은 스위프 포함(소비자 제외 R2-5와 별개 축). 이 리비전
  이후에야 원문 주장("어떤 16번째 위반 기록도 실패")이 정확하다.
- **REVISION 2026-08-27 (cycle 004, R4-9d·e — census 추가 공개 2건):**
  (d) `schemas/llm_output.json`의 `overall.top_signals` description
  ("checklist item_id 참조만 허용")은 코퍼스 전체에서 사문(死文)이다 —
  커밋된 top_signals 문자열 전건이 자유 산문(신호 서술)이고 item_id
  참조는 **0건** (본 세션 재계수 0/2,224; 검토 렌즈 계수 2,215 — 발견
  술어 차이일 뿐 결론 동일). description은 비강제 주석이라 스키마 검증은
  전건 통과 — 스키마는 동결이므로 수정하지 않고 여기 기록한다 (독자는
  top_signals를 checklist 참조가 아니라 서술 텍스트로 읽을 것).
  (e) wave-2 identity arm-B의 runmeta 9건은 `canary_hit` 필드 없이
  `fict_name`을 기록한다 (arm-B 전용 러너 판형) — 카나리 검사 자체는
  verify_blindness 전수 스캔이 커버하므로 누출 게이트 공백은 아니나,
  runmeta 필드 균일성 주장에는 이 예외를 병기해야 한다. 기록만, 동결
  로그 무수정.

## D-P87 — [DRAFT — 소유자 서명 대기] L4 12/12의 탐지 조건부(denominator) 문구 — 서명 표면 전파 제안
- **Status:** DRAFT — 세션(harness v4 cycle 002, R2-6)이 작성. 서명 동결
  표면(`analysis/DECISION_TABLE.md` §4 — D94 서명 · fig_tradeoff
  그림/사이드카)은 본 세션이 접촉하지 않았다.
- **사실:** L4 "T≥50 탐지 12/12 CP95 [73.5, 100]"의 E2 계층 모집단
  (`analysis/e2_trajectories.json`, EARLINESS_PLAN §1)은 본채점에서 이미
  탐지된(p≥50) 케이스만 포함한다 — 미탐지 4건(CSC·BRX, 데이터 사유
  MON·WFT)은 분모에서 제외. 비조건부로 읽으면 ~12/16. 공개는
  BUYER_METRICS §1/§4·EARLINESS_PLAN §1에만 존재했고 README/RESULTS
  헤드라인에는 부재했다.
- **조치 (라이브 표면만, 커밋됨):** README.md 헤드라인 절 + RESULTS.md
  행 13 한계 열(+ 잠금 렌더링 CLAIMS.json 행 13)에 탐지 조건부 절 추가.
  RESULTS.ko는 PKT-R2 스냅샷 마커 관행(영어 정본에만 신규 개정 반영,
  D-P83)에 따라 무접촉.
- **제안 (서명 필요):** (a) DECISION_TABLE.md §4에 일자 기입 addendum
  한 문단(동일 조건부 문구, disclose-don't-revise 채널) (b) fig_tradeoff
  그림 캡션/사이드카 재생성에 같은 조건부 명시 — 두 표면 모두 D94 서명
  동결이므로 소유자 서명 후 집행.
- **Options:** (a) addendum + 그림 캡션 재생성 모두 (권고 — 그림은
  README에서 직링크되는 고노출 표면) (b) addendum만 (c) 현행 유지 —
  라이브 표면 절만으로 충분하다고 판단 시
- **Basis:** `analysis/EARLINESS_PLAN.md` §1 · `analysis/BUYER_METRICS.md`
  §1/§4 · INV-03/INV-06 · reviews/cycle-002.md R2-6
- **Revert:** 라이브 표면 절 삭제 diff + 사유 기록.
- **REVISION 2026-08-27 (harness v4 cycle 003, R3-2 — 서명 전 사실 정정):**
  위 원문(보존)의 배제 목록·산술이 틀렸다. 실측 정정
  (`analysis/EARLINESS_PLAN.md` §1·주석 1 · `analysis/e2_trajectories.json`
  로스터 12 실험군 대조 확인):
  - 실험군 모집단 **17** (wave-1 8 + wave-2 9), 원문의 "~12/16"은 오류 —
    비조건부 판독은 **≈12/17**.
  - 본채점 미탐(p<50) 배제는 **4건: MON(T07, p=28)·LOGI(T12, p=42)·CSC·BRX**
    — 원문은 LOGI를 누락하고 MON·WFT를 "데이터 사유"로 묶어 오기했다.
  - **WFT(T04)는 본채점 탐지 7/9에 포함**되나 스냅샷-0 데이터 사유
    (XBRL 의무화 경계, 잔존 제출 미달 — EARLINESS_PLAN 주석 1)로 별도
    배제된 **다섯 번째** 케이스다. MON은 미탐+데이터 사유 이중 배제.
  - 산술: **12 = 17 − 4(미탐) − 1(탐지-데이터배제 WFT)**.
  - 라이브 표면(README.md·RESULTS.md 행 13·CLAIMS.json)은 본 리비전
    커밋에서 정정 완료. 서명 대상 제안 (a)(b)의 addendum 문구는 본 리비전
    목록을 기준으로 할 것 — 원문 목록으로 서명하지 말 것.
  - **ko-정책 미결 (R3-19, 소유자 판단):** cycle 2는 README.ko의
    E-002/E-003 수치는 갱신하면서 이 L4 조건부 절은 RESULTS.ko 스냅샷
    마커 관행을 이유로 보류했다 — 두 처리 중 하나는 틀렸다 (정오 준수
    갱신 vs 스냅샷 동결의 경계 기준을 소유자가 정해야 함).

## D-P88 — [DRAFT — 소유자 서명 대기] ERRATA 후보: wave-2 dim3는 정답 장르 표 없이 채점됨
- **Status:** DRAFT — 세션(harness v4 cycle 002, R2-7)이 작성. 동결
  `scoring/grades_wave2/` 무접촉.
- **결함:** `grader_runner.answer_key()`가 `--candidates`는 파라미터화하면서
  장르 표는 wave-1 `scoring/genre_tags.md`를 하드코딩했다. wave-2 실험군
  9건의 id는 이 표에 전부 부재 → 채점자 페이로드의 `genre_tag_row: null`,
  그러나 SYSTEM 프롬프트는 dim3(장르 매핑) 채점을 계속 요구. 동결
  `grades_wave2/`의 dim3는 정답지 없이 산출된 즉석 채점이다 (T19/T23/T26/
  T29 점수 부여, T02/T04/T20/T22/T24 null) — 어떤 커밋된 정답 표로도 재현
  불가.
- **소비 감사 (커밋 시점 실측):** wave-2 dim3 점수를 읽는 코드는
  `tools/build_rp13_workbench.py`(인간 최종 확정 워크벤치의 d3 표시 열)
  뿐이다. 게시 수치·집계(`analysis/wave2_analyze.py`·
  `tools/reproduce_analysis.py`·RESULTS 행)는 wave-2 dim3를 소비하지
  않는다 — misstatement_probability·dim1/dim4 경로만. 게시 수치 무영향.
- **조치 (코드만, 커밋됨):** 장르 표 경로 파라미터화(`--genre-table`) +
  실험군 후보에 장르 행이 없으면 `AnswerKeyError`로 fail-closed
  (`scoring/test_grader_runner.py` 3종). 미래 웨이브 보호 목적 — 동결
  기록 무수정 (INV-06).
- **Options:** (a) ERRATA 등재 (grading-record 재현성 주장을 게시 표면으로
  낸다고 판단 시 — RP-13 워크벤치가 dim3를 표시하므로 권고) (b) 본
  엔트리 특성화 공개로 종결 + RP-13 문서에 각주 (c) wave-2 장르 표를
  사후 작성해 재채점 병행 산출 — INV-03 사후 개정 한계 검토 필요
- **Basis:** INV-03/INV-06 · METHOD.md §4 (정답지 기반 채점) ·
  reviews/cycle-002.md R2-7
- **Revert:** fail-closed 완화는 후속 엔트리로 사유 기록.

## D-P89 — [DRAFT — 소유자 서명 대기] 대조군 풀 layer-2 병행 정규화 매니페스트 게시 (disclose-don't-revise)
- **Status:** DRAFT — 세션(harness v4 cycle 003, R3-3)이 작성.
- **결함:** 동결 대조군 풀 매니페스트 4종(runs/rp08·wave2·rp09/
  control_pool_raw, runs/holdout/controls/pool_raw의 MANIFEST.sha256)의
  키가 전건 절대 경로다 — 362+301건은 stale 클론
  `/Users/chaeryeollee/Documents/aaer-evals/...`, 4,961건은
  `/Users/chaeryeollee/aaer-data/_rp08/...`. 현 체크아웃에서
  `validate_control_input.layer2_hashes`는 죽어 있었고(수천 건 오탐;
  stale 클론이 존재하는 머신에서는 조용히 *그쪽* 파일을 해시),
  `verify_manifest.py`는 layer-2가 담당한다는 사유로 `_rp08`을 제외해
  원시 대조군 풀 ~4,961파일에 작동하는 해시 게이트가 없었다.
- **조치 (커밋됨):** 각 풀에 병행 `MANIFEST.relpaths.sha256` 게시 —
  동결 원본의 **해시 열은 그대로**(재해시 아님, attestation 승계) 키 열만
  기계 재작성(저장소 상대 / `~/aaer-data/` 정박; 파생 규칙은 파일 헤더에
  명기). 동결 원본 무수정 (INV-06). `layer2_hashes`는 정규화 매니페스트
  우선 + 구세대 키도 마커 재정박으로 해석(stale 클론 절대 경로 직참조
  불가). pytest 게이트 4풀 전건 (`tools/test_control_pool_layer2.py`) —
  in-repo 항목 상시 검증, 코퍼스 항목은 부재 시 skip. 실측: 현 체크아웃
  + 현 코퍼스에서 4,961 코퍼스 항목 포함 전건 해시 일치.
- **한 가지 의도적 스코프 구분 (공개):** "매니페스트 밖 원시 파일" 스윕은
  RP-08 수집 시점 검증 경로(main)에서는 BIG_DIR 포함 그대로 유지하되,
  이식성 풀 게이트(pytest)에서는 BIG_DIR을 제외한다 — 이 디렉토리는 이후
  웨이브들과 공유되는 코퍼스라(현재 17,154파일 vs rp08 키 4,961) 미등재
  파일 존재가 상시 게이트의 결함 신호가 아니다. 등재분의 존재·해시 검증은
  두 경로 모두 전건 유지.
- **Options:** (a) 본 엔트리로 공개 종결 (권고) (b) ERRATA 병행 등재
  (4-layer 방어 주장을 게시 표면으로 강하게 냈다고 판단 시)
- **Basis:** INV-06 · CONTROL_CRITERIA §6 (4층 방어) · data/README.md
  경로 규약 · reviews/cycle-003.md R3-3
- **Revert:** 병행 매니페스트 삭제 + 해석기 revert 시 사유 기록.
- **REVISION 2026-08-27 (cycle 004, R4-9a — 산술 오기 정정):** 위 결함
  단락의 "362+301건은 stale 클론"은 오기 — 올바른 분해는 **stale 클론
  키 362건 = rp08 61 + wave2 180 + rp09 83 + holdout 38**이고, 여기에
  `~/aaer-data/_rp08` 절대 경로 키 4,961건(rp08)이 더해진다 (총 5,323행,
  회귀 렌즈 실측 확인).

## D-P90 — [DRAFT — 소유자 서명 대기] 후보 파일 4종의 case_input 스키마 편차 66건 — 정리 방안 결정 요청
- **Status:** DRAFT — 세션(harness v4 cycle 003, R3-11)이 작성. 데이터
  파일·스키마 파일 무접촉 (둘 다 동결 — 소유자만 정리 가능).
- **실측 census (2026-08-27, 게이트 코드에 열거 잠금):**
  `schemas/case_input.json`은 `data/candidates/candidates.json`(38/38 유효)
  만을 상정한다. 나머지 4파일 66/66 레코드 무효 — 편차 클래스:
  - AAER 필수 필드 부재 (aaer_no·aaer_date·aaer_url·first_revelation_date·
    revelation_source): wave2 32 · holdout 3 · holdout_controls 9 ·
    v2_controls 22 — 대조군/G2 잠정 케이스에는 정의상 없는 필드가 필수로
    걸림.
  - id 패턴 밖: W08/V07/case_71/VIASP 형 (스키마는 T/C-접두만 허용).
  - scheme_type: null(스키마는 배열/부재만) · scheme_summary 문자열-vs-배열
    드리프트 · matched_treatment ↔ matched_case_id 개명 (not:<root> 23+9+22).
- **조치 (코드만, 커밋됨):** `tools/validate_schemas.py`가 5파일 전부를
  스윕 — 기존 66건은 파일별 {invalid id 집합, 허용 시그니처 집합, 편차
  총수}로 열거 특성화(blanket 면제 아님): 신규 편차 클래스·신규 무효
  케이스·총수 변화(개선 포함) 어느 것도 침묵 통과 불가
  (`tools/test_validate_schemas.py` 4종). CI는 기존 validate_schemas 단계
  그대로 커버.
- **Options (소유자 결정):** (a) case_input 스키마 개정 서명 — 그룹/티어
  조건부 required (treatment-AAER 필수, control/G2 면제) + id 패턴 확장
  (b) 웨이브별 스키마(case_input_wave2 등) 신설 후 파일별 바인딩
  (c) case_input_v2 신설, v1은 wave-1 전용으로 스코프 명시
  (d) 현상 유지 — 본 특성화 게이트를 영구 계약으로 (권고하지 않음: "사전
  등록 계약 준수" 주장이 wave-1에만 성립)
- **Basis:** INV-02(스키마 준수)·INV-06 · reviews/cycle-003.md R3-11
- **Revert:** 특성화 축소는 후속 엔트리로 사유 기록.

## D-P91 — [DRAFT — 소유자 서명 대기] ERRATA 후보: 2026-07-07 동결 표제 wave-2 기록 4건의 무공개 제자리 재작성
- **Status:** DRAFT — 세션(harness v4 cycle 004, R4-1)이 작성. 동결
  파일·로그 전건 무접촉; 전 수치·SHA·타임스탬프는 본 세션이 git 이력에서
  재실측 확인함 (2026-08-27).
- **사실 (git 이력 실측):**
  - `040f7901` (2026-07-07 20:58:47 +09, "W2 채점 원시 출력 — **I3 즉시
    동결**")이 `runs/wave2/scores/case_40.json`(p=60/elevated) ·
    `case_45.json`(p=35/watch) · `case_63.json`(p=22/watch)을,
    `b9077a88` (21:04:56, "W2 교란 draw")이
    `runs/wave2/perturbed/case_66.json`(p=58/elevated)을 커밋했다.
  - `3223fb28` (21:41:51) · `eba481c0` (21:43:46)이 동일 경로 4건을 신규
    모델 호출 산출로 **제자리 교체**: case_40 60/elevated→55/watch ·
    case_45 35→28/watch · case_63 22→30/watch · perturbed case_66
    58/elevated→42/watch. 공개 절·D-엔트리·커밋 메시지 언급 없음 —
    두 교체 커밋의 제목은 원 커밋과 동일한 동결 표제였다.
  - 양 draw의 호출 로그는 전건 생존: 1차 `logs/run_20260707T113920Z`
    (original) · `logs/run_20260707T115847Z`(perturbed), 재추첨
    `logs/run_20260707T123948Z`(case_40/45/63) ·
    `logs/run_20260707T124151Z`(case_66).
  - **기계적 원인 (재실측):** 1차 draw 4건 전부 `overall.top_signals`
    6항목 — 동결 스키마 maxItems 5 위반 (교체본은 3–5항목으로 유효).
    D82(2026-07-13)가 E2 재지출 기록에서 "top_signals 스키마 재추첨 9"로
    같은 결함 클래스를 기록하고 `docs/HANDOFF.md:16`은 이를 "잠복 불일치
    (재추첨 수렴, ~7% 발현)"라 썼으나 — 사실관계는 **6일 전(07-07)에
    이미 발화해 무공개로 처리**된 상태였다.
  - **경미 동류 사례 (포함 공개):** `runs/holdout/controls/recognition/
    {BCO,RXO}.json` — `2e70caf`(07-09 11:25:24) 추가 후 `acd0c0ba`
    (11:26:18)가 재호출로 교체 (session_id·cost 변경,
    event_description "Placeholder"→"See above."). 판정 필드
    (knows_event=false·confidence) 무변경 — 결과 무영향.
- **중대성 (실측):**
  - 채점은 최종값만 소비 — wave-2 grader 로그는 재추첨 이후인
    `run_20260707T124441Z`(12:44Z, 32건)부터 시작. wave-2 FPR 5/23은
    현행 기록에서 재현됨.
  - 단 **perturbed case_66(T29)의 교란 민감도 판독은 생존 draw에
    의존**: original p=55 대비 1차 draw 58(Δ+3) vs 채택 draw 42(Δ−13).
    방향까지 뒤집힌다 — draw 잡음 밴드(케이스당 ≈±10pp, E5 §7)의 실증
    사례로 공개할 것.
- **INV-03/INV-06 분석:** 스키마 위반 산출의 재추첨 자체는 기계적
  배관(plumbing) 수리로 (a) git 이력 보존은 (우연히) 충족되나, (b)
  공개 절을 포함한 신규 D-엔트리 요건이 결여됐고, 동결 표제로 커밋된
  파일의 제자리 교체는 disclose-don't-revise 원칙 위반이다. 본 엔트리가
  그 결여된 (b)를 사후 이행한다.
- **HANDOFF.md "잠복" 문구 정정의 소재:** `docs/HANDOFF.md`는 일자 기입
  세션 인수인계 기록(2026-07-13 갱신)으로 과거 세션 기록에 준한다 —
  본 세션은 수정하지 않았다. 정정은 (i) 본 엔트리 서명으로 갈음하거나
  (ii) ERRATA 등재 본문에 한 줄 포함 — 소유자 서명 시 결정.
- **Options:** (a) ERRATA 등재 (권고 — 동결 표제 커밋의 제자리 교체는
  게시된 "frozen-at-commit" 주장의 신뢰 문제; case_66 민감도 판독
  의존성 공개 포함) (b) 본 엔트리 특성화 공개로 종결 (c) (a)+
  **freeze-title single-add 게이트** 신설 — "동결" 표제 커밋이 기존
  동결 경로를 수정하면 CI 실패 (코드는 소유자 승인 후 별도 항목;
  본 세션은 구축하지 않았다).
- **Basis:** INV-03/INV-06 · D82 · reviews/cycle-004.md R4-1 (전 사실
  본 세션 git 재검증)
- **Revert:** 해당 없음 (기록 전용 — 동결 무접촉).

## D-P92 — [DRAFT — 소유자 서명 대기] cp95_pct 라벨-계산 불일치: v2ds wave-2 0/32의 rule-of-three 상한 9.4 (정확 CP95 10.9) — rev2 병행 산출물 게시

- **Status:** DRAFT — 세션(harness v4 cycle 007, R7-11)이 작성. 동결
  산출물 무접촉.
- **결함 (계산-라벨링, 임계값·판정 규칙 변경 아님):**
  `analysis/name_probe_results_v2ds.json`(동결, D84가 "CP95 병기 산출물"로
  인용)의 `cp95_pct` 필드는 `stats.fpr_bound` 산출을 실었는데, 이 함수는
  k=0에서 Clopper-Pearson이 아니라 rule-of-three(300/n)로 낙하한다 —
  wave-2 0/32 행이 CP95 라벨 아래 [0.0, 9.4]를 게시 (정확 양측 CP95 상한
  10.9보다 반보수적·방법 라벨 불일치). wave-1 4/30(k>0)은 정확 CP와 일치
  ([3.8, 30.7] 불변). RESULTS 행 4는 0/3에 정확 CP를 쓰므로 한 표면에 두
  규약이 공존했다.
- **조치 (disclose-don't-revise — INV-03 (a)(b)(c) / INV-06):**
  (a) 원 산출물·git 이력 보존 (byte-identical 확인);
  (b) 본 엔트리가 공개 절;
  (c) 재산출 전 개정 커밋 — `analysis/name_probes_v2ds.py` frame()이 전
  k(0·n 극점 포함)에서 정확 CP(`holdout_controls_analyze.clopper_pearson`,
  RESULTS 행 4와 동일 규칙)를 쓰도록 수정, 산출은 신규 병행 경로
  `analysis/name_probe_results_v2ds_rev2.json`에만 기록. 극점 회귀는
  `analysis/test_statistics.py`가 잠금 (0/32 → 10.9 · 3/3 → [29.2, 100]).
- **게시 표면 영향:** rate·count·delta 무변 (13.3%/0.0% 등) — 구간 라벨만
  교정. D84 본문(동결)은 "CP95 병기 산출물 참조"라는 포인터라 정정 불요;
  어느 문서가 9.4를 인용하게 되면 rev2 값(10.9)으로 인용할 것.
- **Options:** (a) rev2 병행 게시 승인 + 원 산출물 헤더에 rev2 포인터
  주석(신규 커밋) (b) rev2 병행 게시만 (c) ERRATA 등재 격상 — 소유자 판단.
- **Basis:** INV-03·INV-06 · D84 · reviews/cycle-007.md R7-11 ·
  ERRATA.md E-001 (병행 경로 선례)
- **Revert:** rev2 경로 삭제로 원상 (원 산출물 무접촉이므로 안전).

## D-P93 — [DRAFT — 소유자 서명 대기] 교란 표면 accession/CIK 스캔 확장의 정책 선택 (Q-F20 참조)

- **Status:** DRAFT — 세션(harness v4 cycle 008, R7-6 재디스패치)이 작성.
  게이트 행동 변경 0 (INV-18 — 서명 대상은 게이트의 행동 그 자체).
- **사실관계:** cycle 007 실측 — 교란-kind 표면에 실험군 실제
  accession(접두 = filer CIK) 2,558건 / 35 동결 파일, 스캔 오탐 0.
  벡터 자체는 D99/L-9로 공개되어 있고 `build_payload.py`가 교란
  페이로드에 실제 accession을 유지하는 설계도 공개 문서에 있다 — 결함은
  "게이트가 공개된 벡터를 스캔하지 않는다"는 검증 공백이다.
- **결정 요청:** docs/OWNER_QUEUE.md Q-F20의 옵션 (A) 일자 경계 /
  (B) 열거 allowlist / (C) 현상 유지 중 서명. 권고 (A). `identity_arm_b`
  분류 확인 포함 (정체 가시 arm이 perturbed-kind glob에 등재된 현황).
- **집행 조건:** 서명 후 별도 커밋으로 스캔 구현 + 회귀 테스트. 서명 전
  게이트 코드 무접촉 — 본 엔트리와 Q-F20 등재가 이번 사이클의 전부다.
- **Basis:** INV-18 · INV-06 · reviews/cycle-007.md R7-6 ·
  reviews/cycle-008.md (재디스패치 지시) · builds/cycle-007.md census
- **Revert:** 해당 없음 (기록 전용).

## D-P94 — [DRAFT — 소유자 서명 대기] forward 유니버스 자기 오염(fw001-r08=CIEN) 처리 + cycle-002 예방: 소각 목록을 cutoff_guard 정본에서 파생 (Q-F21 참조)

- **Status:** DRAFT — 세션(harness v4 cycle 010, R10-1)이 작성. 동결 산출물
  무접촉 (universe.json·GATE_PIN·tools/forward_enumerate.py 무변경).
- **사실관계:** `tools/forward_enumerate.py`의 `cycle1_ciks()`는
  cases.json·cases_wave2.json·cases_holdout.json·cases_holdout_controls.json
  4파일만 소각하나, 러너 정본 `pipeline/cutoff_guard.py
  TRUSTED_CASE_FILES`에는 `cases_v2.json`이 더 있다. 그 결과
  case_36(CIENA CORP, CIK 0000936395; 2026-07-07 커밋·채점, 게시 wave-2
  통계에 `runs/rp09/scores/case_36.json` 경유 반영)이 T₀=2026-07-20 열거에서
  소각되지 않고 fw001-r08로 선정·GATE_PIN 동결되었다 —
  docs/UNIVERSE_SELECTION.md §2-2의 문서화된 위반 (1/12 봉인 레코드).
- **결정 요청:** Q-F21 옵션 (A) 기록 + §3 사전 고정 1순위 대기(NEE) 자동
  승격 / (B) 유지 + disclosure / (C) 단건 abort 중 서명. 권고 (A).
- **집행 조건 (서명 후 각각 별도 커밋):**
  1. 선택지 집행 — (A)면 GATE_PIN supersession 문서 + 병행 산출물 경로
     (동결 원본 무수정, INV-06 병행 경로 규약; R3-13의 승격 절차
     사전 등록과 연동).
  2. 예방(cycle-002): `cycle1_ciks()`의 하드코딩 4파일 목록을
     `cutoff_guard.TRUSTED_CASE_FILES`에서 파생하되 `cases_forward_*` 접두
     파일만 제외하는 형태로 교체 + 두 목록의 드리프트를 잠그는 회귀 테스트
     (R7-10 교차 대조 관용구). 지금 고치지 않는 이유: `cycle1_ciks()`는
     동결 universe.json의 byte-identity 재현 경로다 — 서명 없는 코드 변경은
     §2-2 위반을 침묵 소거하는 재열거를 만들 수 있다
     (tools/test_forward_enumerate_offline.py의 byte-identity 핀과 충돌).
- **Basis:** docs/UNIVERSE_SELECTION.md §2-2·§3 · INV-18 · INV-06 · INV-22 ·
  reviews/cycle-010.md R10-1 · runs/rp09/scores/case_36.json (실재 확인).
- **Revert:** 해당 없음 (기록 전용).

## D-P95 — [DRAFT — 소유자 서명 대기] OWNER_LAUNCH_GATE §4 실행 절차 개정 통합 패킷: 현행 문면대로는 step (4)에서 결정론적으로 기동 거부된다 (R3-14/Q-O11 연동)

- **Status:** DRAFT — 세션(harness v4 cycle 010, R10-4)이 작성.
  `forward/cycle_001/OWNER_LAUNCH_GATE.md`는 소유자 서명 문서 — 세션
  무접촉(INV-18). 기존 DEFERRED R3-14(§4 runbook에 Q-O11 in-window 재핀
  단계 부재)를 확장·통합한다.
- **결함 목록 (문면 그대로 실행 시):**
  (i) step (2)-(3)이 생성하는 `forward/cycle_001/source_manifest.json`·
      `data/evaluatee/cases_forward_001.json`은
      `pipeline/cli_client.py UNTRACKED_OUTPUT_PREFIXES`의 예외 접두
      (runs/·logs/·pilot/·scoring/grades·probe_results)에 없다 — §4에 커밋
      단계가 없으므로 step (4) 러너가 "freeze-commit-then-run 위반"으로
      기동 거부 (결정론적 발사 실패).
  (ii) fetch 후 `verify_manifest.py --write` + 커밋 단계 부재 —
      R10-2 가드·fetch_log 귀속과 짝을 이루는 corpus 매니페스트 갱신이
      절차에 없어 fetch 직후부터 full verify가 적색.
  (iii) §4(6) `git add forward/cycle_001`은 SEAL_RECORD가 방출하는 정본
      stage 목록(runs/forward/<cycle> + logs/run_* + runs/MANIFEST.sha256,
      R7-16/R10-3)과 어긋난다 — 문면대로면 클론 검증자의 run-output
      re-hash leg가 침묵 격하.
  (iv) §4(1)이 쓰기 모드 `--offline`을 호출 — 검증 전용으로 만든
      읽기 전용 `--check` 형(R3-1)이 정위치 (동결본 mtime/클로버 무위험).
  (v) §4(2)가 요구 산출물(source_manifest.json)을 만들 도구
      `tools/forward_source_manifest.py`를 이름으로 지시하지 않는다.
  (vi) 창 내 supersession 열거 대상이 3/7에서 **4/7**로 늘었다 — 실측
      (2026-08-28): `pipeline/build_payload.py`·`pipeline/cli_client.py`·
      `pipeline/runner.py`·`specs/FORWARD_WATCHLIST_V1.md` 드리프트,
      `docs/UNIVERSE_SELECTION.md`·`schemas/llm_output.json`·
      `specs/RISK_SCORE_SEMANTICS.md` 일치. Q-O11 서명된 in-window 재핀
      단계는 이 4종 전부를 열거해야 한다 (R1-40 관측의 현재값).
- **결정 요청:** 아래 §4 교체문 승인 (게이트 문서 개정은 소유자 직접 편집).
- **집행 조건:** 서명 = 소유자가 아래 펜스 블록으로
  `forward/cycle_001/OWNER_LAUNCH_GATE.md` §4를 직접 교체 + (vi)의 4종
  재핀을 Q-O11 절차(FREEZE_REV/supersession 문서)에 등재. 세션은 게이트
  파일을 편집하지 않는다.
- **§4 교체문 (ready-to-apply):**

```bash
# (0) 사전: 병행 작성자 검사 + 5게이트 green + Q-O08 확인 + Q-O11 재핀
#     (supersession 문서 — 드리프트 4종: build_payload.py·cli_client.py·
#      runner.py·FORWARD_WATCHLIST_V1.md, 2026-08-28 실측; 실행 직전 재실측)
# (1) 유니버스 신선도 재확인 — 읽기 전용 --check 형 (R3-1; 쓰기 모드 금지)
#     신규 4.02 오염 시 §2 규칙 인용 + alternates 승격 (Q-F21/D-P94 참조)
python tools/forward_enumerate.py --offline --check
# (2) 입력 수집 (컷오프 가드 경유; retrieval/filing 분리 기록;
#     매니페스트 핀 충돌 시 fetch가 파일 0개 쓴 채 거부 — R10-2)
python tools/fetch_xbrl_facts.py --universe forward/cycle_001/universe.json --dest ~/aaer-data
python tools/forward_source_manifest.py --fetch-dir ~/aaer-data --cycle forward/cycle_001
# (2b) corpus 매니페스트 재생성 + 커밋 (R10-2 짝)
python tools/verify_manifest.py --write
git add data/manifests/aaer_data_manifest.json && git commit -m "cycle_001: corpus manifest post-fetch"
# (3) 케이스 빌드 (R3-4 파라미터화 경로)
python tools/build_evaluatee_inputs.py --universe forward/cycle_001/universe.json \
    --out data/evaluatee/cases_forward_001.json
# (3b) 생성 입력 2종 커밋 — cli_client freeze-commit-then-run 게이트:
#     forward/·data/evaluatee/는 미추적 예외 접두가 아니므로 미커밋 시
#     step (4)가 기동 거부한다
git add forward/cycle_001/source_manifest.json data/evaluatee/cases_forward_001.json && \
  git commit -m "cycle_001: frozen inputs (source_manifest + cases_forward_001)"
# (4) 발사 (소유자 승인 후):
python pipeline/runner.py --cases data/evaluatee/cases_forward_001.json \
    --out runs/forward/cycle_001
# (5) 조립·검증·봉인 (validate는 R5-1 --runs leg 포함형):
python tools/forward_assemble.py --cycle forward/cycle_001 --runs runs/forward/cycle_001
python tools/forward_validate.py --cycle forward/cycle_001 --runs runs/forward/cycle_001
python tools/forward_seal.py --cycle forward/cycle_001
# (6) 봉인 직후 (외부 타임스탬프 — 즉시): 정본은 forward_seal이 방출한
#     소유자 명령 블록(SEAL_RECORD.md §소유자 봉인 명령) — 그대로 실행.
#     현재 형태 사본 (R7-16/R10-3 stage 목록):
python tools/verify_blindness.py --write-manifest
git add runs/MANIFEST.sha256 forward/cycle_001 runs/forward/cycle_001 logs/run_* && \
  git commit -m "SEAL: cycle_001 forward watchlist"
git tag -a forward-cycle-001-seal -m "forward seal"
git push origin main --tags
pip install opentimestamps-client   # (ots 부재 시 1회, 무료)
ots stamp forward/cycle_001/MANIFEST.sha256
git add forward/cycle_001/MANIFEST.sha256.ots && git commit -m "SEAL: OTS anchor" && git push
# (7) 사후 검증:
python tools/forward_verify_seal.py --cycle forward/cycle_001
```

- **Basis:** reviews/cycle-010.md R10-4 · R3-14 (DEFERRED, Q-O11 연동) ·
  pipeline/cli_client.py UNTRACKED_OUTPUT_PREFIXES ·
  forward/cycle_001/PROTOCOL.md 핀 실측 (2026-08-28) · INV-18 · INV-22.
- **Revert:** 해당 없음 (기록 전용 — 게이트 파일 무변경).

## D-P96 — [DRAFT — 소유자 서명 대기] DECISION_TABLE §2 프레임 오표기 공개: "가공명 프레임"이 실은 정체 노출(원본) 프레임 점수 위에 있었다

- **Status:** DRAFT — 세션(harness v4 cycle 010, R10-7)이 작성.
- **개정 블록 (2026-08-28, R3-2/D-P87 판례의 일자 기입 방식):**
  - 영어 정본 `analysis/DECISION_TABLE.md` §2의 프레임 문장
    "Fictional-name frame, …"을 "Identity-exposed (original) frame, …"으로
    정정했다 (수치 토큰 무변경). §2 셀(≥50 7/9·FP 5/23, ≥60 3/9)은
    `wave2_results.json` 원본 프레임 벡터 — 페이로드에 실명이 들어간
    실행이며(`analysis/wave2_summary.md` "1차 프레임: 정체 노출",
    `data/evaluatee/cases_wave2.json`의 실명 payload), 8/9 knows_event
    (docs/README_DETAIL.md). 유일한 가공명 wave-2 점수(3-arm b-arm,
    `identity_3arm_results.json`)는 대조군이 없고 ≥60 계수도 다르다(5/9).
  - **동결 ko 표면**: `analysis/DECISION_TABLE.ko.md:44`에 같은 오표기
    ("가공명(fictional name) 프레임")가 남아 있다 — D94 서명 동결 표면이므로
    무수정(INV-06). 본 엔트리가 공개(disclosure) 기록이며, 소유자는
    (a) 본 공개로 종결 또는 (b) ERRATA 항목 승격 중 서명한다. ko 스냅샷
    vs live 정책의 양방향 적용 이력은 R3-19(DEFERRED)가 다룬다.
  - 오표기는 rigor-inflating 방향(정체 마스킹 주장 → 실제는 노출)이었다 —
    오염 축의 정확 공개가 봉인 신뢰성의 근거라는 점에서 P2.
- **Basis:** reviews/cycle-010.md R10-7 · analysis/wave2_summary.md ·
  docs/README_DETAIL.md:105-109 · INV-06 · D94 (표면 서명).
- **Revert:** DECISION_TABLE.md §2 문장 원복 (비권장 — 오표기 복원이 된다).

## D-P97 — [DRAFT — 소유자 서명 대기] holdout 대조군 위양성 2건 = 자체 감사가 `ineligible`로 기록한 2건이라는 중첩 공개 (L-8 의무의 holdout 티어 이행)

- **Status:** DRAFT — 세션(harness v4 cycle 014, R14-4)이 작성. 게시
  표면 편집이므로 소유자 감사 대상이다.
- **사실 (전건 아티팩트 재확인):**
  - `analysis/holdout_controls_results.json`의 `control_fpr` = fp 2 · n 9 ·
    point 0.222 · CP95 [0.028, 0.600]. ≥50 쌍은 정확히 {GRDX 78, GO 58}.
  - `controls/retrospective_audit_v1.md` 판정표의 hc 9행 중 `ineligible`은
    정확히 2행 — GRDX (기준 (e), 감사인 사임 8-K + 회사 공시 Item 304
    disagreement)와 GO (기준 (d), 차기 연차 평가까지 미해소 중요한 취약점).
    나머지 7행은 전부 `provisional-INCOMPLETE`이며 ≥50에 도달한 행은 없다.
  - `runs/holdout/controls/control_group_holdout.json` `selections.case_73`:
    GRDX는 `rev_pit` 0 · `size_basis` "assets" · `size_dist` 1.0686 · S1
    플래그(매출 PIT 불능 → 총자산 대체), `eligible_ranked_count` 3의 rank 3,
    `alternates` [] — 사전 등록 축 순서(size → industry → era,
    `analysis/HOLDOUT_CONTROLS_PLAN.md` §1)에 비추어 "industry·size·era로
    매칭"은 이 한 쌍에 대해 문자 그대로는 아니다.
- **왜 공개인가:** `docs/methodology_limitations.md` L-8이 스스로 부과한
  의무("어떤 위양성 해석에서도 이 중첩을 명시하라")가 wave-1 사례(C04/R)
  에는 이행돼 있고 holdout 티어에는 이행돼 있지 않았다. 이 사실은 양방향
  으로 하중을 받는다 — 22.2%가 대조군 풀 조건부라는 읽기와, 그래서 오차율
  과대 표시일 수 있다는 읽기가 동시에 성립한다. 그래서 해석을 정하지 않고
  사실만 병기했다.
- **편집 표면 (게시·live만):** `RESULTS.md` 6·10행 limits 열 + 잠금
  렌더링 `CLAIMS.json`의 같은 두 셀(tools/test_claims_ledger.py가 강제하는
  동기화) · `README.md` GRDX 문장 · `analysis/DECISION_TABLE.md` §3 ·
  `docs/methodology_limitations.md` L-12.
- **무접촉 (동결):** `runs/` 0건 · `analysis/ISSUE_2_HOLDOUT_DRAFT.md`
  (2026-07-11 게시, 2026-07-21 감사보다 앞섬) 0건 ·
  `analysis/holdout_controls_results.json` 0건 · 공표 수치 재계산 0건.
- **두 건의 형식 제약 (소유자 확인 요망):**
  (i) 추가분을 L-8 본문 아래 addendum으로 넣으면 동결 ko 스냅샷(L-1–L-8)과의
      수치 토큰 등가 잠금(tools/test_translation_equivalence.py)이 깨진다 —
      L-8은 무수정으로 두고 신규 L-12로 기입했다(L-9 이후 영어 정본 전용
      규약, L-10/L-11 판례).
  (ii) 같은 잠금 때문에 `analysis/DECISION_TABLE.md` §3의 문구는 숫자 토큰을
      하나도 담을 수 없다 — 그 절에는 무숫자 요약 + 전체 인용 위치 지시만
      두고, 수치·accession은 RESULTS.md와 감사 문서가 진다.
- **INV-13:** 두 회사는 집행 대상이 아닌 현재 기업이다. 추가 문면은 공시
  사실 + 출처만 담고 단정 어휘를 쓰지 않으며, 모델이 왜 그 점수를 냈는지에
  대한 추론을 담지 않는다.
- **Basis:** reviews/cycle-014.md R14-4 (C13-p 승격) · L-8 자체 지시 ·
  D106 common OUT · GA-001 (b) (RESULTS.md는 인간 감사 대기 표면) ·
  INV-06 (동결 경로 무접촉).
- **Revert:** 위 다섯 표면의 추가 문면 삭제 + `CLAIMS.json` 두 셀 원복
  (비권장 — L-8이 부과한 공개 의무가 다시 미이행 상태로 돌아간다).

## D-P98 — [DRAFT — 소유자 서명 대기] 11월 창 runbook 변경: `--allow-new-custody-claims`(2b 1회 거부)가 사라지고 "수집 직후 `data/provenance/fetch_log.jsonl` 커밋"이 그 자리에 들어온다

- **Status:** DRAFT — 세션(harness v4 cycle 015, R15-1)이 작성. 소유자가
  11월 창에서 **실제로 실행하는 절차**가 바뀌므로 서명 대상이다.
- **무엇이 바뀌나 (소유자 관점, 절차 두 줄):**
  - **사라지는 것:** R13-5가 예고한 "첫 실 재핀(runbook 2b)이 한 번 거부하고,
    소유자가 `python tools/verify_manifest.py --write --allow-new-custody-claims`
    로 명시 승인한다"는 단계. 그 플래그도, 매니페스트의 `custody_claims` 키도
    더 이상 존재하지 않는다. 2b는 이제 조건 없이 통과한다.
  - **들어오는 것:** 수집 로그의 정본이 corpus 트리 밖 git 관리 경로
    (`data/provenance/fetch_log.jsonl`)로 옮겨졌으므로, **각 감독 fetch 직후
    그 파일을 커밋**해야 출처 주장이 이력에 정박된다. 커밋하지 않은 로그는
    정박되지 않은 로그다. `fetch_xbrl_facts.py`가 종료 시 이 문구를 인쇄한다.
    **R16-2 이후 이 커밋은 권고가 아니라 절차의 일부다:** 가드는 정본 로그의
    HEAD 판만 신뢰하므로, 2b에서 로그를 커밋하지 않으면 다음 재수집이 자기가
    방금 쓴 핀 경로에서 거부된다 (거부 메시지가 커밋 명령을 인쇄한다).
- **왜 (한 문장):** 커스터디 앵커를 "매니페스트 핀"에서 "git diff"로 옮기면
  같은 도구가 자기 앵커를 재생성하는 순환이 끊긴다 — R11-2 → R12-1 → R13-5 →
  R14-5로 네 번 재발한 결함(두 경로·두 파서·두 파일)의 클래스가 사라진다.
  체크포인트는 약해지지 않고 옮겨간다: 제3자가 이력에서 검사할 수 있으므로
  재핀 시점의 자체 신고보다 강하다.
- **열린 질문 (기록만 — 답하지 않았다) — R16-2에서 정정:** 이 항목은 종전에
  "도구가 커밋을 강제해야 하는가"를 **전부 아니면 전무**로 적었다: 가드
  시점에 clean git 상태를 요구하면 `fetch → 2b → 재수집` 루프가 깨지므로
  알림만 인쇄한다는 것이었다. 그것은 거짓 이분법이었다. 더 좁은 통제가
  존재하고, R16-2가 그것을 구현했다 — 가드는 **자신이 의지하는 행**만 HEAD에
  있을 것을 요구한다(`committed_log_lines`). 방금 수집해 아직 커밋되지 않은
  행은 의지 대상이 아니므로 루프는 그대로 돌고(2b가 커밋 단계다), 작업 트리
  전체의 청결은 요구하지 않는다. 남은 열린 질문은 더 좁다: **커스터디 앵커가
  어디에 살고 무엇이 그것을 강제하는가** — 여섯 번의 디스패치가 매번 신뢰
  근원을 옮겼을 뿐 없애지 못했다. 이는 소유자 판단이며 세션이 답하지 않는다.
- **다음 단계 (소유자):** 위 열린 질문은 `reviews/cycle-016.md` R16-2의
  "OWNER-FACING" 절에 여섯 번의 디스패치 이력과 함께 정리되어 있다 — 일곱 번째
  국소 패치 전에 소유자가 답할 설계 질문이다. 본 항목(D-P98)의 서명은 여전히
  대기 중이며, R16-2는 그 서명을 대신하지 않는다.
- **INV-15 관계:** 저장소 안에 두는 것은 여전히 매니페스트류 텍스트뿐이다 —
  대용량 원문은 git 밖 그대로다. 수집 로그는 크기가 아니라 **증거 성격**
  때문에 안으로 들어온다.
- **잔존 우회 경로 — R16-2에서 정정 (종전 서술은 틀렸다):** 이 항목은 종전에
  "핀된 온전한 스냅샷을 실제로 덮어쓰는 길은 `--allow-pinned TICKER` 하나뿐"
  이라고 적었다. R15-1 검증(lens B)이 그 문장을 반증했다 — 정본 로그의 **작업
  트리 판**에 위조 행 한 줄을 덧붙이면 `fetch_forward`가 0을 반환하며 온전한·
  핀된·동결 바이트를 **아무 플래그 없이** 덮어썼다. R15-1이 `_log_is_authoritative`
  를 삭제하고 그 자리에 아무 인증도 놓지 않았기 때문이다. 현재(R16-2 이후)의
  실제 집합은 다음 셋이다:
  1. 수집 시점의 `--allow-pinned TICKER` — 소유자 판단, 정본 로그에 기록됨.
  2. 정본 로그에 위조 행을 **커밋**하기 — 커밋해야만 권위가 생기므로
     저장소 이력에 남는다. 이력에 남는 것이 이 통제의 전부이며, 커밋 자체를
     막지는 않는다.
  3. 저장소 작업 트리에 대한 쓰기 권한 + `git commit` 권한을 가진 주체는
     결국 (2)를 실행할 수 있다 — 단일 사용자 워크스테이션에서 이는 corpus
     쓰기 권한과 같은 권한이다. 이것이 위 "열린 질문"이 가리키는 잔여 위험이다.
  종전 문장이 맞는 범위는 **소유자 플래그**에 한정된다: 플래그는 둘(재핀 쪽 +
  수집 쪽)에서 하나로 줄었다. 그 범위를 넘어 "유일한 길"이라고 읽히면 안 된다.
- **R17-3 정정 — 위 (2)의 "이력에 남는다"는 cycle 016 시점에는 거짓이었다.**
  R16-2 검증(lens B)이 네 번째 경로를 실증했다: 게이트가
  `git -C <로그가 사는 디렉토리> show HEAD:./fetch_log.jsonl`이었으므로, 위조
  행을 덧붙일 수 있는 주체는 같은 자리에 `git init`도 할 수 있었고, **중첩
  저장소가 바깥 저장소를 가렸다** — 바깥 HEAD의 로그는 그대로 비어 있고 바깥
  `git log`에도 흔적이 없는데 `fetch_forward`가 0을 반환하며 온전한 핀 스냅샷을
  덮어썼다. 즉 "커밋해야만 권위가 생긴다"가 "**어느 저장소에** 커밋할지 공격자가
  고른다"로 무너져 있었고, 바깥 저장소에서의 유일한 흔적은 더러운 작업 트리 —
  이 항목이 대체하려던 바로 그 미강제 보완통제 — 뿐이었다. cycle 017 R17-3이
  앵커 저장소를 데이터에 적힌 경로가 아니라 모듈 자신의 위치에서
  `rev-parse --show-toplevel`로 해석하고 저장소 루트 상대 pathspec으로 조회하도록
  고쳤다(중첩 저장소·상위 디렉토리 중첩·`.git` 파일 간접·심볼릭 링크 로그
  디렉토리 전건 거부). **위 (2)의 서술은 R17-3 이후 시점에 한해 참이다.**
  이 정정은 DRAFT 문면 수정일 뿐이며, 본 항목의 서명은 여전히 대기 중이다
  (INV-18). 앵커가 **어디에 살아야 하는가**는 여전히 소유자 설계 결정이다 —
  R17-3은 소유자가 고른 근원(저장소 자신의 이력) 안의 구멍을 막은 것이지
  그 선택을 대신하지 않는다.
- **Basis:** reviews/cycle-015.md R15-1 (R11-2 → R12-1 → R13-5 → R14-5의 5차
  디스패치) · builds/cycle-015.md · INV-18 (세션은 self-resolve하지 않는다).
- **Revert:** `tools/fetch_xbrl_facts.py`의 `FETCH_LOG_REL`/`fetch_log_path()`
  제거 + `verify_manifest`의 custody_claims 층 복원 (비권장 — 네 번 뚫린
  앵커로 되돌아간다).

## D-P99 — [DRAFT — 소유자 서명 대기] Q-F21은 11월 창 첫날의 **커스터디 교착**이기도 하다: 옵션 (B)·(C)는 기계적으로 실행 불가

- **Status:** DRAFT — 세션(harness v4 cycle 016, R16-4)이 작성. 선택도, 서명도
  하지 않았다 (INV-18). Q-F21은 `docs/OWNER_QUEUE.md`에서 **OPEN 그대로**다.
- **새로 밝혀진 사실 (통계·거버넌스가 아니라 실행 가능성):** `fw001-r08` =
  CIEN(CIK 0000936395)은 `data/manifests/aaer_data_manifest.json`의 핀 4건과
  충돌한다. `tools/fetch_xbrl_facts.py`의
  `assert_no_pinned_custody_conflict`는 `dest.mkdir` **전에**, 바이트 하나
  쓰기 전에 `universe["selected"]` 전건을 판정하고 막힌 티커를 한 dict에 모아
  **단일 `SystemExit`**을 던진다. 따라서 OWNER_LAUNCH_GATE step (2)는 CIEN만이
  아니라 **12사 전건에 대해 0파일**로 끝난다. 봉인 사슬이 실행 창 첫날 멈춘다.
  - 실측: 커밋된 `forward/cycle_001/universe.json` × 커밋된 매니페스트에 대한
    blocked 집합 =
    `{"CIEN": ["CIEN/edgar/CIK0000936395-submissions-001.json",
    "CIEN/edgar/CIK0000936395-submissions-002.json",
    "CIEN/edgar/CIK0000936395.json", "CIEN/xbrl/CIK0000936395.json"]}`.
    `tools/test_forward_tools.py::test_committed_universe_has_no_pinned_custody_deadlock`
    이 이 판정을 재생한다 (현재 strict xfail — 해소되면 XPASS로 깨진다).
- **각 옵션에 붙는 교착 결과 (Q-F21의 선택지 그대로, 판단은 소유자):**
  - **(A) 대기 1순위 NEE(CIK 0000753308) 자동 승격** — NEE는 핀 매니페스트에
    없다. runbook을 **적힌 그대로** 실행 가능하게 두는 유일한 옵션.
    §3 명문의 집행이라는 점은 Q-F21의 기존 서술과 같다. GATE_PIN·byte-identity
    supersession 문서가 필요하다는 점도 같다. *본 초안의 기본값 — 적용하지
    않았다.*
  - **(B) fw001-r08 유지 + 봉인 문서 disclosure** — **기계적으로 실행 불가.**
    CIEN이 `selected`에 남는 한 step (2)가 전건을 막으므로 disclosure를 붙일
    산출물 자체가 생기지 않는다.
  - **(C) fw001-r08 단건 not_scored/abort** — **기계적으로 실행 불가.**
    아무것도 쓰지 않고 거부하는 fetch를 통과해 not_scored 레코드에 도달할 수
    없다. 창 안 코드 변경이 필요하다.
  - **(D) 가드를 티커 단위 skip으로 재설계** (막힌 티커만 건너뛰고 나머지는
    수집) — 선택지로 **기록만** 한다. 서명된 runbook 안의 게이트 의미를 바꾸는
    변경이므로 소유자 결정이며, 본 사이클에서 구현하지 않았다. 부작용: 부분
    수집이 조용히 정상 종료가 되어 "12사 전건 수집"이 게이트에서 빠진다.
- **`--allow-pinned CIEN`이 해법이 아닌 이유 (경로 자체를 배제 권고):**
  매니페스트 핀 wave-2 파일 4건을 덮어쓰고, D-P95 §4 step **(2b)**
  (`verify_manifest --write` + 커밋)가 파괴된 바이트를 **다시 핀**한다 —
  게시된 wave-2 케이스의 재현 바이트를 ERRATA도 D-엔트리도 없이 제자리
  개서하는 것(INV-06). CI는 `--schema-only`로 돌아 green을 유지하므로
  `make verify-full`을 돌릴 때까지 보이지 않는다. R11-12가 가설이 아니라 확정
  경로가 된다.
- **시한:** 2026-11-15 창 시작 전. 미서명으로 창에 들어가면 step (2)가 0파일로
  중단되고, 그 자리에서 쓸 수 있는 유일한 명령이 위 파괴적 경로다.
- **세션 조치 (여기까지만):** OWNER_QUEUE Q-F21에 교착 결과 bullet 추가(OPEN
  유지), 본 DRAFT 등재, 판정을 재생하는 테스트 추가.
  `forward/cycle_001/universe.json`·`SNAPSHOT_MANIFEST.sha256`·
  `data/manifests/` **무접촉** (GATE_PIN 동결, INV-06).
- **Basis:** reviews/cycle-016.md R16-4 · docs/OWNER_QUEUE.md Q-F21 ·
  DECISIONS_PENDING D-P94·D-P95 §4 · docs/UNIVERSE_SELECTION.md §2-2·§3 ·
  INV-06 · INV-18 · INV-22.
- **Revert:** 본 항목은 문서·테스트만 추가한다. 되돌리려면 Q-F21 bullet과 본
  항목, 그리고 두 테스트를 제거하면 된다 — 실행 코드의 판정 규칙은 바뀌지
  않았다 (`pinned_conflicts` 추출은 동작 보존 리팩터).

## D-P100 — [DRAFT — 소유자 서명 대기] 커스터디 앵커는 어디에 살고 무엇이 그것을 강제하는가: 일곱 번째 국소 패치 대신 설계를 고른다

- **Status:** DRAFT — 세션(harness v4 cycle 017, R17-5 (a))이 작성. 서명 대상은
  **설계 선택 하나**이며, 아래 옵션 중 무엇도 선택하지 않았다 (INV-18).
- **왜 지금 소유자에게 오는가:** 같은 결함 클래스가 여섯 번 디스패치됐고 매번
  유능하게 처리됐다. 매 통과가 신뢰 근원을 **옮겼을 뿐 없애지 못했다**는 것이
  이 항목의 전부다. 일곱 번째 패치를 쓰기 전에 앵커의 자리를 정한다.

  | # | 디스패치 | 무엇이 앵커였나 | 무엇이 그것을 깼나 |
  |---|---|---|---|
  | 1 | R11-2 | 보호 트리(DATA_DIR) 안의 append-only 수집 로그 | 서명 없는 파일 — 위조 행 한 줄로 동결 바이트가 열렸다 |
  | 2 | R12-1 | 로그가 **자기 매니페스트 핀과 바이트 일치**할 것 | 같은 도구가 자기 앵커를 재생성하는 순환 (2b가 위조를 축복) |
  | 3 | R13-5 | 가드와 재핀이 **같은 파서**를 쓰도록 통일 | 통일된 것은 파서였고 **경로**가 아니었다 |
  | 4 | R14-5 | (동일 — 경로 통일 시도) | `--dest`가 가드(`dest/…`)와 재핀(`DATA_DIR/…`)을 갈라 놓았다 · 빌더가 BLOCKED로 정확히 보고 |
  | 5 | R15-1 | 로그를 트리 **밖** git 관리 정본으로 이동 | 옮긴 자리에 **아무 인증도 놓지 않았다** — 작업 트리 위조 행이 그대로 권위를 가졌다 |
  | 6 | R16-2 | 정본 로그의 **HEAD 판**만 신뢰 | 조회가 `git -C <로그가 사는 디렉토리>`였다 — 아래 익스플로잇 |
  | 7 | R17-3 | 앵커 저장소를 **모듈 자신의 위치**에서 해석 (구멍 봉합) | (미봉합 잔여 위험: 아래 "남는 것") |

- **6번을 깬 익스플로잇 (logs/verdicts/R16-2-B.md 실측 전사):**

  ```
  OUTER REPO HEAD CONTENT: ''                      <- 바깥 HEAD의 로그는 그대로 비어 있다
  OUTER REPO log --oneline: 24a4bf0 fetch log      <- 위조는 실제 이력에 없다
  _own_writes(): {'TK01/xbrl/CIK0000001001.json'}  <- 위조가 커스터디 권위를 얻었다
  fetch_forward rc: 0
  frozen bytes after: b'{"filings": {"files": []}}' <- 온전한 핀 스냅샷이 덮어써졌다
  ```

  위조 행을 덧붙일 수 있는 주체는 같은 자리에 `git init`도 할 수 있으므로,
  **어느 저장소의 HEAD가 답하는지를 공격자가 골랐다**. 이 통제가 사려던 유일한
  값("위조는 git 이력에 남지 않고서는 성립할 수 없다")이 지불되지 않았고,
  바깥 저장소의 유일한 흔적은 더러운 작업 트리 — R15-1이 대체하려던 바로 그
  미강제 보완통제 — 뿐이었다.
- **R17-3이 한 일과 하지 않은 일:** cycle 017이 앵커 저장소를 데이터에 적힌
  경로가 아니라 모듈 자신의 설치 위치에서 `rev-parse --show-toplevel`로 해석하고
  저장소 루트 상대 pathspec으로 조회하도록 고쳤다 (중첩 저장소·상위 디렉토리
  중첩·`.git` 파일 간접·심볼릭 링크 로그 디렉토리 전건 거부, 커밋된 정당한 행은
  그대로 통과). **이는 옵션 (i) 아래의 구멍 봉합이며, 소유자가 다른 옵션을
  고르면 대체(superseded)되는 것이지 모순되지 않는다.** 지금 봉합한 이유는
  익스플로잇이 오늘 동결 바이트를 덮어쓰기 때문이지, 설계 질문에 답했기
  때문이 아니다.
- **남는 것 (어느 옵션을 고르든 소유자가 알아야 할 사실):** 통제가 결속된
  열쇠는 **저장소 HEAD의 내용**이다. 저장소에 커밋할 수 있는 주체는 그 열쇠를
  스스로 공급할 수 있다 — 단일 사용자 워크스테이션에서 그것은 corpus 쓰기
  권한과 같은 권한이다. 파일 쓰기만 가능한 주체(익스플로잇이 필요로 한 능력)는
  더 이상 공급할 수 없다. 이 차이가 R17-3이 실제로 사들인 값의 전부다.
- **옵션 (하나를 고르시오 — 세션은 고르지 않았다):**
  - **(i) 저장소 루트 정박 HEAD 판정** (= R17-3이 구현한 것). *찬:* 추가 인프라
    0, 제3자가 `git log`로 검사 가능, 런북 루프 무변경, 이미 구현·측정됨
    (앵커 제거 4 red · `git -C <로그 디렉토리>` 회귀 3 red · 무조건 신뢰 회귀
    9 red, 각각 동일 줄 무의미 대조 0 red). *반:* 열쇠가 저장소 이력이므로
    커밋 권한자가 곧 앵커 소유자다. 위 표의 여섯 번이 모두 "이번엔 맞다"처럼
    보였다는 사실이 이 옵션에 대한 가장 강한 반론이다.
  - **(ii) 트리 밖 커스터디 기록** (예: 수집 시각에 로그 행을 OTS 스탬프,
    또는 append-only 외부 로그에 이중 기록). *찬:* 앵커가 저장소 쓰기 권한과
    분리된다 — 위 "남는 것"이 실제로 사라지는 유일한 옵션. *반:* 새 외부
    의존과 절차 단계가 생기고($0 제약은 OTS로 유지 가능), 11월 창 안에서
    실패하면 수집 자체가 막힌다. 무엇보다 **아직 존재하지 않는 기제**다.
  - **(iii) 핀된 바이트 덮어쓰기를 무조건 거부** — 커스터디 주장이라는 개념을
    없앤다. 핀된 파일을 다시 쓰려면 매니페스트를 먼저 소유자가 명시적으로
    푸는 수밖에 없다. *찬:* 방어할 앵커가 없어지므로 이 클래스가 종결된다.
    가장 단순하고 가장 검증 가능하다. *반:* 재수집이 필요한 정당한 경우
    (손상 파일 교체, 창 중간 재시도)마다 소유자 개입이 필요하다 — 11월 창의
    운영 부담이 실제로 커진다. Q-F21/D-P99의 CIEN 교착과 상호작용한다.
- **시한:** 2026-11-15 창 시작 전 (창 안에서는 INV-22로 정정이 불가능하다).
- **Basis:** reviews/cycle-017.md R17-3·R17-5 (a) · logs/verdicts/R16-2-B.md ·
  D-P98 (같은 계열, 절차 문면) · reviews/cycle-016.md R16-2 · INV-06 · INV-18.
- **Revert:** 본 항목은 문서만 추가한다. (i)을 유지하면 코드 변경은 없다.

## D-P101 — [DRAFT — 소유자 서명 대기] 철회 문언 잠금(규칙 M)의 설계: 근접창 allowlist는 어떤 문구를 열쇠로 삼든 그 문구를 적어 넣으면 열린다

- **Status:** DRAFT — 세션(harness v4 cycle 017, R17-5 (b))이 작성. 두 번 연속
  검증 실패한 항목이므로 CRITERIA_RULES C-11(two-strike)에 따라 패치가 아니라
  설계 결정으로 올린다. 세션은 옵션을 고르지 않았다 (INV-18).
- **근본 원인 (한 문장):** ±160자 근접창을 문구 allowlist로 여는 구조는, 열쇠가
  무엇이든 **그 열쇠를 문장에 함께 적어 넣으면 열리므로**, 철회된 주장을 다시
  단언하는 바로 그 방향으로 느슨하다.
- **열쇠가 옮겨간 이력 (구멍은 닫히지 않았다):**
  - **R15-5:** 열쇠 = 주제어 (`retracted`, `declared cutoff`, `D-P83`).
    철회 문장을 그 어휘와 함께 재단언 → 20/20 DOCS 미검출.
  - **R16-3:** 열쇠 = 짧은 정형구 (`문언/주장/표현 … was retracted` 류).
    4단어 접두사만 붙이면 criterion (a)의 네 문장이 전부 exit 0, 재단언을
    **앞에** 두는 형태 10종 추가 확인. 같은 결함 클래스, 열쇠 길이만 다르다.
  - 두 경우 모두 빌더는 주어진 기준을 전부 충족했다. 기준이 성질이 아니라
    사례를 지목했다는 것이 실패 원인이며, 그것은 리뷰어 결함으로 기록됐다.
- **cycle 017의 증거 (선택을 대신하지 않는다):** **같은 구멍이 규칙 (G)에도
  있었고**, 거기서는 구조적으로 닫혔다 — allowlist 분기가 **자기 텍스트만으로**
  하한 표현을 부정하거나 홀드아웃 계층에 귀속해야 하고(맨 긍정어는 분기가 될 수
  없다), 테스트 코퍼스는 그 분기들에서 실행 시점에 파생된다. 그래서 맨 긍정
  분기를 하나 넣으면 테스트를 한 줄도 고치지 않아도 스위트가 적색이 된다
  (실측 4 red, 동일 줄 무의미 대조 0 red). 덧붙여 (M)의 설계 주석이 근거로
  삼았던 "규칙 (G)는 부정 구문만 받는다"는 **당시 거짓**이었고, 그 주석은
  cycle 017에서 정정됐다.
- **옵션 (하나를 고르시오):**
  - **(i) 살아 있는 표면에서 철회 주장을 allowlist 없이 전면 금지하고, 교정
    논의에는 구조적 자리를 준다** — 펜스 블록, 명시 마커, 또는 전용 ERRATA
    표면. *찬:* 근접창 판정 자체가 사라지므로 이 클래스가 종결된다.
    *반:* 정본 문서 안에서 철회 사실을 서술하는 자연스러운 문장이 불가능해지고,
    "어디에 쓰면 되는가"를 문서 규약으로 새로 정해야 한다.
  - **(ii) (G)에 적용한 **파생 코퍼스** 형태를 (M)에도 적용 — 유력 후보.**
    분기 형식 제약("철회를 **서술**하는 구문만": 철회 동사 + 문언/주장을 가리키는
    목적어) + 분기에서 파생한 프로브 문장. *찬:* 열쇠를 옮기는 게 아니라 열쇠를
    **추가할 능력**을 없앤다. (G)에서 실측으로 동작한다. *반 (정직하게):*
    "철회를 서술하는 구문"의 형식 판정은 (G)의 "부정/귀속"보다 경계가 흐리다 —
    한국어 어미 변화가 넓고, 재단언과 서술이 한 문장에 공존하는 형태
    ("철회된 문언대로, 암기는 불가능하다")를 형식만으로 가르기 어렵다. 이
    한계를 감춘 채 (ii)를 고르면 세 번째 실패가 된다.
  - **(iii) 수용하고 공개한다** — 규칙 (M)을 현행대로 두되, 그 한계를
    `docs/methodology_limitations.md`에 명시한다("이 잠금은 우발적 재유입을
    막고 의도적 재단언은 막지 못한다"). *찬:* 거짓 보증을 팔지 않는다.
    *반:* 11월 발행 표면에 대한 기계 방어가 실질적으로 사라진다.
- **시한:** 11월 발행문 작성 전.
- **Basis:** reviews/cycle-017.md R17-4·R17-5 (b) · reviews/cycle-016.md R16-3 ·
  logs/verdicts/R16-3-B.md · scoring/decisions_log.md D-P83 · CRITERIA_RULES C-11.
- **Revert:** 본 항목은 문서만 추가한다.

## D-P102 — [DRAFT — 소유자 서명 대기] 서명된 런북의 첫 명령이 실패한다 — 그리고 두 번째 파손은 어떤 결정으로도 되돌릴 수 없다

- **Status:** DRAFT — 세션(harness v4 cycle 017, R17-5 (c))이 작성. 서명 대상은
  §4 step (1)과 §1 결정론 주장의 처리다. 세션은 아무것도 고치지 않았다.
- **파손 ① — step (1)이 exit 1이다.** `OWNER_LAUNCH_GATE.md` §4 step (1)은
  `python tools/forward_enumerate.py --offline`이다. cycle_001에는 커밋된
  `.missing` 마커가 35개 있고 전부 `_fetch_errors`를 무장시키므로,
  `--offline`·`--check`·`--force` **셋 다 아무것도 쓰지 않고 1을 반환한다**
  (logs/verdicts/R16-7-B.md 실행 실측). 창 첫날 첫 명령이 멈춘다.
- **파손 ② — 되돌릴 수 없다.** 동결된 `universe.json`은
  `"missing_data": 35`를 기록하고 있는데, 모듈은 R16-7 이후 그 키를 더 이상
  방출하지 않는다. 따라서 `--check`의 바이트 일치는 **마커를 전부 없애더라도
  다시 성립하지 않는다**. §1의 결정론 재계산 주장은 서로 무관한 두 이유로
  깨져 있으며, 두 번째는 ERRATA 또는 신규 사이클 말고는 어떤 소유자 결정으로도
  복구되지 않는다. 이 두 번째 파손은 R16-7의 기준(b)이 만든 것이며 리뷰어가
  자기 결함으로 기록했다 (RV-19).
- **본 초안이 제안하지 않는 것:** 동결 산출물(`universe.json`,
  `SNAPSHOT_MANIFEST.sha256`) 수정 — INV-06/INV-22 위반이며, 여기서 제안하지
  않는다.
- **소유자가 정해야 할 것 (선택지 기록만):**
  - **(A) §1의 결정론 주장을 ERRATA로 정정하고 step (1)을 "재계산 일치 확인"이
    아닌 다른 확인으로 교체** — 예: 스냅샷 해시 대조. *찬:* 창 안에서 실행
    가능한 상태가 된다. *반:* 서명된 게이트 문서를 창 전에 개정해야 한다.
  - **(B) cycle_001을 abort 처리하고 cycle_002로 재출발** — *찬:* 두 파손이
    함께 사라지고 결정론 주장이 진실이 된다. *반:* 사전 등록된 창을 놓친다
    (사이클 전체가 그 사실을 기록한 채 보존된다).
  - **(C) step (1)을 창 절차에서 제거하고 그 사실을 봉인 문서에 공개** —
    *찬:* 최소 변경. *반:* 유니버스 신선도 재확인이라는 절차적 방어가 사라진다.
- **시한:** **2026-11-15 이전 — 하드 데드라인.** 미서명으로 창에 들어가면 첫
  명령에서 멈춘다.
- **Basis:** reviews/cycle-017.md R17-5 (c) · logs/verdicts/R16-7-B.md ·
  reviews/cycle-016.md RV-19 · forward/cycle_001/OWNER_LAUNCH_GATE.md §1·§4 ·
  INV-06 · INV-22.
- **Revert:** 본 항목은 문서만 추가한다.

## D-P103 — [DRAFT — 소유자 서명 대기] CIEN 교착의 strict-xfail 표시를 유지할 것인가, 영구 red로 둘 것인가 (INV-24 상호작용)

- **Status:** DRAFT — 세션(harness v4 cycle 017, R17-5 (d))이 작성.
  `docs/OWNER_QUEUE.md` Q-F21은 **OPEN 그대로**이며 본 초안은 아무 옵션도
  선택하지 않는다 (INV-18).
- **무엇이 걸려 있나:** R16-4가 11월 창 첫날의 커스터디 교착(CIEN의 매니페스트
  핀 4파일이 디스크에 있으면서 정본 로그에 없고, 가드가 배치 전체에 대해 하나의
  SystemExit를 올려 **12사 전건 0파일**이 되는 상태)을 재생하는 테스트를 남겼다.
  그 테스트는 현재 `strict` xfail이며, 스위트에서 유일한 비-green 표시다.
- **선택지:**
  - **(A) strict xfail 유지.** *찬:* 정본 3.12 잡이 green을 유지하므로 INV-24
    ("침묵 green 금지"가 아니라 "정본 green 유지")와 충돌하지 않고, 교착이
    해소되면 xpass로 **자동으로 적색**이 되어 소유자에게 알린다. *반:* 초록
    스위트 안의 xfail은 읽는 사람에게 "알려진 실패"로 보이지 않는다 — 교착의
    심각도가 표시 형태에 의해 축소된다.
  - **(B) 영구 red로 둔다.** *찬:* 미해결 11월 블로커가 CI에서 매 push 보인다.
    *반:* 정본 3.12 잡이 붉어지므로 **INV-24 정면 위반**이다 — 다른 회귀가
    이 붉음에 묻힌다. 이 옵션을 고르려면 INV-24의 예외 조항이 함께 서명돼야
    한다.
  - **(C) xfail 유지 + 별도 가시 채널** — 예: CI 요약에 알려진 블로커 목록을
    notice로 인쇄. *찬:* (A)의 green과 (B)의 가시성을 동시에 얻는다.
    *반:* 프로세스 기계가 하나 늘어난다 (거버넌스 팽창 주의 대상).
- **연동:** D-P99(교착 자체의 처리)와 D-P102(step (1) 파손)가 해소되면 본
  항목은 자동으로 소멸한다 — 그 전까지의 **표시 방법**에 대한 결정이다.
- **시한:** D-P99보다 늦어도 된다. 다만 창 전에 (B)를 고를 경우 INV-24 예외가
  선행 서명돼야 한다.
- **Basis:** reviews/cycle-017.md R17-5 (d) · reviews/cycle-016.md R16-4 ·
  logs/verdicts/R16-4-A.md · docs/OWNER_QUEUE.md Q-F21 · INV-24.
- **Revert:** 본 항목은 문서만 추가한다.
