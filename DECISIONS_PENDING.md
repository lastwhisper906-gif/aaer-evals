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
