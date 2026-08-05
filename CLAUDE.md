# CLAUDE.md — 역할 중립 저장소 컨텍스트 (자동 로드)

이 파일은 `claude`(대화형·`-p` 모두)와, `AGENTS.md` 심링크를 통해 `codex`에도
자동 로드된다. 따라서 **역할 중립 내용만** 담는다: 어떤 역할(빌더/리뷰어/
대화형 세션)이 읽어도 유효한 프로젝트 불변식.

- 단일 기준 문서는 PROJECT.md다. 충돌 시 PROJECT.md가 우선.
- 아래 블록의 원본은 `PROJECT_INVARIANTS.md`다. 수정은 그 파일에서 하고
  `~/tools/harness/sync_context.sh .`(저장소 루트에서 실행)로 이 블록을
  재생성한다. 이 블록을 직접 편집하지 않는다.
- 대화형 오케스트레이터 세션 전용 지침은 `docs/ORCHESTRATOR_NOTES.md`에
  있다(자동 로드되지 않음 — 대화형 세션에서만 수동 참조).

<!-- BEGIN SHARED INVARIANTS (source: PROJECT_INVARIANTS.md) -->
## 1. 방법론 불변식 — 위반 시 프로젝트 무효

### INV-01: Look-ahead 차단
**Constraint:** 케이스 컷오프일(최초 폭로일 기준) 이후 데이터 접근이 필요해
보이면 작업을 중단하고 보고한다. 모든 원시 데이터 로딩은
`pipeline/cutoff_guard.py`를 경유해야 하며 우회 코드를 작성하지 않는다.
**Basis:** PROJECT.md §5-1 · `pipeline/cutoff_guard.py` ·
`pipeline/test_no_guard_bypass.py` (가드 우회 스캔 테스트)
**Violation test:** `cutoff_guard`의 load_* 함수를 경유하지 않고 원시
데이터(`~/aaer-data` 등)를 여는 코드를 `pipeline/`·`tools/`·`analysis/`에
추가하는 변경, 또는 `test_no_guard_bypass.py`의 스캔 대상·허용목록을
좁히거나 넓혀 기존 스캔을 무력화하는 변경.

### INV-02: 결정론 — 수치는 Python, 난수는 시드, 채점 경로 벽시계 금지
**Constraint:** 수치 계산은 Python(결정론적)으로 한다. 난수는 반드시 시드
고정, 채점 경로에 벽시계(wall-clock) 의존 로직 금지. LLM 질적 분석은 원문
인용 강제, 출력은 `schemas/` 스키마 준수. 열린 질문 프롬프트 금지.
**Basis:** PROJECT.md §5-4 · `schemas/` (case_input·evaluatee_input·
llm_output·score_record) · METHOD.md §4·§5
**Violation test:** 채점·통계 코드에 시드 없는 난수 또는 현재 시각 의존
분기를 추가하는 변경; `schemas/` 검증을 거치지 않고 LLM 출력을 소비하는
코드 추가; 피평가자 프롬프트에 체크리스트·구조화 필드가 아닌 열린
질문("이 회사 수상해?")을 추가하는 변경.

### INV-03: 사전 고정·사후 개정 한계
**Constraint:** 채점 기준은 사전 고정. 결과를 본 뒤의 스펙 개정은 기계적
커버리지·배관(plumbing) 결함 수리에 한해 허용되며, 반드시 (a) 1차 결과의
git 이력 보존 (b) 공개(disclosure) 절을 포함한 신규 D-엔트리 (c) 재실행 전
개정 커밋을 갖춰야 한다. 임계값·판정 규칙·지표 정의는 어떤 경우에도 사후
변경 불가.
**Basis:** RP-17 (owner 2026-07-16, D90) · ERRATA.md E-001/E-002 (이 절차의
실제 적용례) · `scoring/decisions_log.md`
**Violation test:** 결과 산출 커밋 이후에 임계값·판정 규칙·지표 정의를
바꾸는 diff; 또는 커버리지·배관 수리이면서 (a)(b)(c) 중 하나라도 결여된
채로 재실행하는 변경.

### INV-04: 동일 프로토콜
**Constraint:** 대조군과 실험군은 동일 프로토콜로 처리한다.
**Basis:** PROJECT.md §5-2 · `analysis/HOLDOUT_CONTROLS_PLAN.md`
**Violation test:** 실험군 또는 대조군 한쪽에만 적용되는 전처리·프롬프트·
채점 분기를 파이프라인·분석 코드에 추가하는 변경.

### INV-05: 5게이트 규율
**Constraint:** 게이트 실측은 pytest(analysis/ 포함)·reproduce·lint·
blindness·verify_manifest 5종 전부다 — 하나를 다른 것으로 대체 실측하면
그 자리에 구멍이 생긴다 (2026-07-13 reference/ 미등재 이틀 미검출 사례).
**Basis:** Makefile `verify-public` · `.github/workflows/ci.yml` ·
CLAUDE.md 방법론 불변식 5
**Violation test:** Makefile `verify-public` 타깃 또는 `ci.yml`에서
pytest·`tools/reproduce_analysis.py`·`tools/lint_publication.py`·
`tools/lint_doc_counts.py`·`tools/verify_blindness.py`·
`tools/verify_manifest.py` 중 하나를 삭제·주석 처리·조건부 skip으로 바꾸는
변경.

## 2. 동결 경로 — 수정 금지

### INV-06: 동결·게시 산출물 불변, 정정은 ERRATA 경유만
**Constraint:** v1 동결 산출물, 게시된(published) 결과, 과거 거버넌스
기록은 수정 금지. 정정은 `ERRATA.md` 항목 추가(append-only) + 신규 코드
경로/신규 산출물 경로의 병행 게시로만 한다 — 대체가 아니다.
**Basis:** ERRATA.md 헤더 원칙 · E-001 조치(원 구현
`analysis/legacy/wave2_analyze_v1.py` 보존, rev2는
`analysis/out/wave2_rev2/` 신규 경로) · AUDIT_INDEX.md §1
**Violation test:** 동결 산출물(`analysis/ISSUE_*_DRAFT.md`,
`analysis/wave2_results.json` 등 게시 소스 열이 가리키는 파일), `runs/`
하위 기존 기록, `scoring/decisions_log.md`·`ERRATA.md`·
`scoring/overrides.md`의 기존 항목을 수정·삭제하는 diff.

### INV-07: 기준 선행 커밋 — 타임스탬프가 증거
**Constraint:** 판정·기준 문서는 결과를 보기 전에 커밋한다. FREEZE_REV
개정은 재실행 커밋보다 앞서야 유효하다.
**Basis:** `tools/verify_blindness.py` (채점 기준 커밋이 점수 커밋보다
앞서는지 git 이력으로 기계 검증 — CI 매 push) · AUDIT_INDEX.md §1
FREEZE_REV 행
**Violation test:** 점수·결과 산출 커밋보다 늦게 커밋된 기준·계획 문서로
그 결과를 판정하는 변경 — `tools/verify_blindness.py`의 이력 증명 검사가
실패하는 상태.

## 3. 격리·보안 불변식

### INV-08: pipeline/ ↔ scoring/ 물리 분리
**Constraint:** `pipeline/` = 피평가자 쪽 코드, `scoring/` = 채점·서명
기록. 물리적으로 섞지 않는다.
**Basis:** METHOD.md 누출 위협 모델(정답 누출 방어) · CLAUDE.md 격리
불변식
**Violation test:** `pipeline/` 하위 코드가 `scoring/` 하위 파일을
import·read하는 변경(테스트의 격리 검증 제외), 또는 채점 로직을
`pipeline/`로 옮기는 변경.

### INV-09: 채점 측 비밀 비참조 + 송출 전 값 수준 스캔
**Constraint:** 채점 측 비밀(신원 맵, 섭동 계수, 정답 키)은 피평가자가 볼
수 있는 코드·경로에서 절대 참조하지 않는다. 피평가자 송출 전 페이로드는
정답지·카나리 마커를 값 수준으로 스캔하며, 적중 시 호출 자체가 일어나지
않는다.
**Basis:** METHOD.md §3 · `pipeline/cli_client.py` ·
`tools/verify_blindness.py` (전 runs/ 카나리 스캔)
**Violation test:** `pipeline/` 코드가 `scoring/id_mapping*.json`·
`scoring/perturbed_cases.json` 등 채점 비밀 파일을 참조하는 변경;
`cli_client.py`의 송출 전 스캔을 제거·약화하는 변경.

### INV-10: 비밀·API 키·자격 증명 파일 금지
**Constraint:** 비밀·API 키·자격 증명을 어떤 파일에도 넣지 않는다.
**Basis:** CLAUDE.md 격리·보안 불변식
**Violation test:** API 키·토큰·자격 증명 문자열을 포함하는 파일을
커밋하는 변경.

### INV-11: 의존성 동결 — 최상위 5개, 해시 핀 lockfile
**Constraint:** 신규 의존성 추가 금지. 최상위 의존성은
`requirements.txt`의 5개(pytest·jsonschema·requests·pypdf·matplotlib)로
고정, 설치는 해시 핀 `requirements.lock`(`--require-hashes`) 경유.
**Basis:** `requirements.txt` · D109 C4 (pip-compile --generate-hashes,
전이 의존성 663해시) · README Quickstart
**Violation test:** `requirements.txt`에 여섯 번째 최상위 의존성을
추가하는 변경, 또는 `requirements.lock`을 pip-compile 재생성 없이 수기
수정하는 변경.

## 4. 스코프 불변식

### INV-12: 스코프 금지 목록
**Constraint:** 금지: 실험군 케이스 8개 초과 확장 / LBO 풀 모델 /
파이프라인 전면 재설계(수정 최대 2지점) / UI·제품화 / 딥다이브 3개+ /
타 LLM(GPT·Gemini) 벤치마크 확장. 참고: Beneish M-score / Dechow F-score
등 결정론적 공식 베이스라인 계산은 스코프 위반이 아니다(채점의 일부).
**예외 (소유자 서명 2026-08-05, D-P44b·D-P45):** 동결(payload-frozen)
회고 케이스에 한해, 구독 인증 Codex CLI(zero-metered, INV-20 준수)를
통한 GPT 교차모델 패스는 스코프 위반이 아니다 — L-6(동일 계열 관대화)
한계의 실증 테스트 목적. 신규 케이스 확장·Gemini·종량 API 경로는 여전히
금지. 산출물은 신규 분리 경로(`runs/crossmodel_gpt/`)에만 기록하며 동결
결과 집합과 병합하지 않는다; 수치 게시는 소유자 게이트.
**Basis:** PROJECT.md §8 · `docs/POST_FORWARD_BACKLOG.md` (P4 제품층
"수요 검증 전 착수 금지" 재확인)
**Violation test:** 실험군 케이스 등록을 8개 초과로 늘리는 데이터·코드
변경; UI·웹 프론트엔드 코드 추가; 위 예외 조건(구독 Codex·동결 케이스·
분리 경로) 밖의 GPT·Gemini 호출 경로 추가 — 종량 API 키 경로는 예외
없이 위반(기록·스펙 문서는 허용 — `specs/cross_grader.md`는
SPECIFICATION ONLY).

## 5. 산출물 표현 불변식 (현재 기업 대상)

### INV-13: 사실/가설 분리, 단정 어휘 금지
**Constraint:** 사실(지표)과 가설(해석)을 분리한다. "분식/fraud/조작"
단어를 현재 기업에 절대 사용하지 않는다.
**Basis:** PROJECT.md §6 · `tools/lint_publication.py` (G2-fraud 린트)
**Violation test:** 현재(비집행) 기업을 다루는 산출물에 해당 단어를
사용하는 변경 — `tools/lint_publication.py` 실패.

### INV-14: 출처 링크·면책·범위 한정 문구
**Constraint:** 모든 수치에 공시 원문 링크를 단다. 포지션 없음 고지 +
교육·정보 목적 면책 문구를 포함한다. 결과 문서화 시 "본 결과는 Claude
기반 단일 파이프라인에 한정" 문구와 "채점: Claude 보조 + 인간 최종 확정"을
명시한다.
**Basis:** PROJECT.md §5-5·§6 · README 헤더 · `tools/lint_publication.py`
**Violation test:** 발행 대상 문서에서 범위 한정 문구·면책 문구를
삭제하는 diff — `tools/lint_publication.py` 실패.

## 6. 저장소 규약

커밋은 작게 유지한다 (관행 — 단독 위반 판정 대상은 아님).

### INV-15: 대용량 원문은 git 밖
**Constraint:** 대용량 원문(공시·AAER PDF)은 git 밖(`~/aaer-data/` 등
절대경로), 경로 규약은 `data/README.md`. 저장소 안에는 매니페스트
(`data/manifests/`)만 둔다.
**Basis:** `data/README.md` · `tools/verify_manifest.py`
**Violation test:** 원시 XBRL/EDGAR/PDF 원문 파일을 저장소 안에 커밋하는
변경.

### INV-16: 단일 작성자 원칙 (direction-loop 조건부 예외 포함)
**Constraint:** aaer-evals를 수정하는 작성자는 동시에 최대 1개(단일 작성자
원칙). 워크트리 병렬성은 서로소 저장소(예: screener)에만 허용.
**예외 (소유자 승인 2026-07-29, DECISIONS_PENDING.md D-P1):**
direction-loop 하네스의 전용 워크트리(`aaer-evals-loop`) 커밋은 비-main
브랜치에서, 하네스의 기계적 격리(워크트리 전용 실행 · 보호 경로 자동
revert · 전역 단일 루프 잠금) 하에 허용된다. 소유자 관행: 루프 실행 중
main push를 하지 않는다. 본 조항은 측정 조건이 아니라 저장소 규약(§6)
이므로 이 개정은 동결 규칙 위반이 아니다.
**Basis:** CLAUDE.md 저장소 규약 · 2026-07-20 브랜치 분기 사건 ·
DECISIONS_PENDING.md D-P1
**Violation test:** aaer-evals(및 그 워크트리)에 동시에 쓰는 두 번째
세션·프로세스를 기동하는 행위 — 단, 위 예외 조건을 전부 충족하는
direction-loop 워크트리 실행은 제외.

### INV-17: Fetch-first
**Constraint:** 이 저장소의 모든 에이전트 세션은 시작 시
`git fetch origin`을 실행한다. 로컬 HEAD가 origin/main보다 뒤에 있으면
세션은 그 분기 상태를 보고하고, 소유자가 정합(reconcile)하거나 달리
지시할 때까지 작업을 시작하지 않는다.
**Basis:** CLAUDE.md 저장소 규약 · 2026-07-20 브랜치 분기 사건(미러 클론
push 워크플로)
**Violation test:** fetch 없이, 또는 behind 상태를 인지하고도 커밋을
생성하는 세션 행위.

## 7. 거버넌스·실행 불변식

### INV-18: 인간 서명 전용 확정 + D-원장 기록, self-resolve 금지
**Constraint:** 모든 실행·서명·스코프 변경은 `scoring/decisions_log.md`에
D-엔트리로 기록된다. 소유자 판단이 필요한 항목은 `docs/OWNER_QUEUE.md`에
옵션/근거/기본값 형식으로 적재되며, 세션(AI)은 절대 self-resolve하지
않는다. 발견 → 격리 등록 → 검토 패킷 → 인간 서명 → 동결 텍스트 → (수동)
게시 사슬에서 서명 단계는 건너뛸 수 없다.
**Basis:** AUDIT_INDEX.md §1·§2 · PROJECT.md §7 (불변 조항 3) ·
`docs/OWNER_QUEUE.md` 헤더
**Violation test:** OWNER_QUEUE의 OPEN 항목을 소유자 서명 기록 없이
RESOLVED로 바꾸는 diff; 소유자 서명 없이 게시·봉인·스코프 변경을 실행하는
커밋.

### INV-19: 피평가자 ≠ 채점 보조 — 역할 분리
**Constraint:** 파이프라인 안의 Claude(피평가자)와 Claude Code(개발·채점
보조)는 분리된다. 채점 보조가 피평가자의 답을 세션 내에서 대신 생성하는
것 금지. 피평가자 호출은 저장소 밖 임시 디렉토리의 격리 단일 호출
(`pipeline/cli_client.py`)로만 한다.
**Basis:** PROJECT.md §7 역할 분리 · METHOD.md §3 ·
`docs/methodology_limitations.md` L-6 (동일 계열 관대화 한계로 공개)
**Violation test:** `runs/` 하위 피평가자 산출물을 `cli_client.py` 격리
호출 경로 밖에서 생성·수정하는 변경.

### INV-20: zero-metered — 종량 과금 경로 금지
**Constraint:** 모델 호출은 구독 인증 전용(Claude 구독 headless, Codex는
`~/.codex/auth.json`). 종량 API 키 경로는 금지 — FREEZE_REV3 raw-API
이행은 무기 정지(D102). 종량 자격증명 감지 시 자동 기동 거부. 유일한
예외: 소유자가 직접 `AAER_RAW_API_APPROVED=1`로 실행하는 `make smoke`.
**Basis:** `docs/OWNER_QUEUE.md` Q-O08 (RESOLVED 2026-07-20, D102) ·
`forward/cycle_001/OWNER_LAUNCH_GATE.md` §5 · POST_FORWARD_BACKLOG P1
**Violation test:** 소유자 명시 승인 플래그 없이 ANTHROPIC_API_KEY·
OPENAI_API_KEY를 설정·요구하는 실행 경로를 추가하는 변경.

### INV-21: 하네스·모델 핀 fail-closed
**Constraint:** 피평가자 호출 전 CLI 버전 핀과 서빙 모델 핀
(claude-sonnet-5)을 실측 대조하고 불일치·명령 실패 시 fail-closed
(`enforce_harness_pin`). 핀 개정은 FREEZE_REV 문서로만 한다.
**Basis:** D109 C3 · `pipeline/cli_client.py` ·
`governance/SUPERSESSION_CYCLE001_REPIN_2026-07-22.md`
**Violation test:** `cli_client.py`의 핀 대조를 우회·완화하는 변경;
FREEZE_REV 신규 문서 없이 핀 값을 바꾸는 커밋.

### INV-22: 전향(forward) 사이클 봉인 규율
**Constraint:** `forward/cycle_XXX`는 소유자가 OWNER_LAUNCH_GATE에
서명하기 전 어떤 모델 런도 발사되지 않는다. 봉인(seal) 후 사이클 산출물
수정 금지. 창 내 완료 불가 시 조용한 연장 금지 — abort 마감 + 신규 사이클.
채점 완료 <11/12이면 봉인 금지.
**Basis:** `forward/cycle_001/OWNER_LAUNCH_GATE.md` §5–§6 ·
`docs/FUTURE_CYCLE_PROTOCOL.md` · `tools/forward_verify_seal.py`
**Violation test:** 게이트 서명 기록 없이 forward 사이클의 모델 호출을
실행하는 변경; seal 커밋·태그 이후 `forward/cycle_XXX/` 하위 파일을
수정하는 diff.

### INV-23: 무인 네트워크 fetch 금지 — look-ahead의 조용한 경로
**Constraint:** 신규 외부 데이터 fetch(EDGAR·XBRL·FINRA 등)는 소유자 입회
감독 세션에서만 한다. 무인 자동화(cron 등) fetch 금지 — 각 케이스
컷오프에 대한 look-ahead 누출을 조용히 만들 수 있다.
**Basis:** `docs/OWNER_QUEUE.md` Q-E03 (RESOLVED — 감독 하 실행) ·
Makefile `rescan` 주석 (PROJECT.md §5-1 연결)
**Violation test:** 네트워크 fetch를 수행하는 무인 실행 경로(cron·
백그라운드 세션 포함)를 추가하는 변경.

### INV-24: CI 정본 그린 — 침묵 green 금지
**Constraint:** 재현 주장의 정본은 Python 3.12 — 3.12 잡의 CI 전 단계는
매 push 통과해야 한다. 비정본(3.11/3.13) 실패는 허용하되 가시
기록(continue-on-error + notice)한다 — 침묵 green 금지.
**Basis:** `.github/workflows/ci.yml` (C5, D109) · REPRODUCING.md §1
**Violation test:** 3.12 잡을 continue-on-error로 바꾸거나 CI 단계를
삭제하는 변경; 비정본 실패의 notice 주석을 제거하는 변경.
<!-- END SHARED INVARIANTS -->
