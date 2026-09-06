# 실행 런북 — Phase 3+ (구독 헤드리스 경로, freeze 개정 #2)

> Authored by Claude Code, pending human audit (GA-001 (b), D15).
> 전제: freeze 커밋 `82a7717` 이후 기준 무변경 (러너가 clean tree를 강제).
> **실행층 = Claude Code 구독 헤드리스** (`claude -p`, freeze 개정 #2 —
> `scoring/decisions_log.md` 참조). 하네스 핀 v2.1.201.
> **자격 증명 = 구독 OAuth 전용**: 대화형 세션에서 `claude /status` → Auth가
> **Claude Max** 구독인지 확인. API 키는 설정·요구·문서화 금지 (RP-04 R1/R2,
> GLOBAL INVARIANT 4). 러너가 환경에 ANTHROPIC_API_KEY 부재를 assert한다.
> 비용: 구독에 흡수 — `total_cost_usd`는 참고 기록일 뿐 과금 알람으로 쓰지 않는다.

## 격리 모델 (모든 모델 호출 공통 — pipeline/cli_client.py)

- 호출별 작업 디렉토리 = 저장소 밖 임시 디렉토리 (fresh, 종료 후 삭제).
- `CLAUDE_CONFIG_DIR=<빈 임시 디렉토리>` — 전역 설정·메모리·훅·MCP 로딩 차단.
- 플래그: `--max-turns 1 --disallowedTools "Bash,Read,Edit,Write,Glob,Grep,WebFetch,WebSearch,Task,NotebookEdit" --json-schema <스키마> --output-format json`.
- 파싱: `structured_output` 필드 → 기존 스키마 검증기 통과 필수.
- 로그: `logs/run_<ts>/` 케이스별 JSON — 플래그 전체·session_id·modelUsage(서빙
  모델 — 핀 불일치는 해당 케이스 FAIL)·토큰·total_cost_usd(참고)·freeze 해시.

## 재개 의미론 (idempotent run)

러너는 **멱등**이다: `outputs/<case_id>.json`이 존재하고 스키마를 통과하면 skip.
- 중단(레이트 리밋 포함) 시: 러너가 정확한 재개 명령을 stdout에 출력하고 중단.
  재개 = **같은 명령을 다시 실행** (완료분은 자동 skip).
- 스키마 실패·빈 응답: 동일 입력 1회 재시도, 2연속 실패 = 해당 케이스 FAIL 기록
  후 다음 케이스 계속 (전체 중단 없음).
- 실행 전 clean tree 필수 — dirty tree면 러너가 거부 (freeze-commit-then-run).

## 순서 (역순 금지 — D7 분기가 본 실행 해석을 결정)

```bash
source .venv/bin/activate
python tools/verify_manifest.py                      # PASS 확인

# 0. 파일럿 + 격리 게이트 (Phase 3/4 — 본 실행 사전 조건)
python pipeline/runner.py --cases pilot/cases_pilot.json --out pilot/runs
#    + 격리 프로브·--verbose 오염 트레이스 grep — 게이트 5항목 전부 PASS여야 본 실행

# 1. 인지 프로브 (교란 페이로드, 실험군 8) → D7 분기
python pipeline/probe_runner.py --recognition --cases scoring/perturbed_cases.json
#    n>=3: CONTAMINATED — 본 분석 = 교란 실행, 원본은 부록 상한
#    n<3 : 본 분석 = 원본 실행, delta = 암기 기여 추정

# 2. 축어 회상 프로브 (원본 필드만, 실험군 8)
python pipeline/probe_runner.py --verbatim --cases scoring/perturbed_cases.json

# 3. 본 실행 (원본 16 + 교란 8, 변형당 1회 — D5, 동시성 3)
python pipeline/runner.py --cases data/evaluatee/cases.json --out runs/main
python pipeline/runner.py --cases scoring/perturbed_cases.json --perturbed --out runs/perturbed

# 4. 채점 (grader = fable-5, 폴백 opus-4-8 로그 — 중립 ID 유지)
python scoring/grader_runner.py --runs runs/main --out scoring/grades/main
python scoring/grader_runner.py --runs runs/perturbed --out scoring/grades/perturbed

# 5. 스키마 검증 + Brier/판별 통계 (결정론) — 채점 커밋 후에만 id_mapping 개봉
```

## 실행 중 의무 기록 (SR 11-7 제3자 모델 규칙)

- `logs/run_<ts>/`: 호출별 서빙 모델·session_id·토큰·시간·freeze 해시 — 자동 기록,
  실행 후 커밋. 시크릿·토큰은 로그·커밋 어디에도 남기지 않는다.
- grader 폴백 발동 시: `_meta.fallback_used=true` 건수를 RP-05에 집계.
- 카나리 GUID의 응답 내 출현 여부를 케이스별 기록.

## 실행 후 → 분석 (RP-05, 사전 등록 절차)

① 케이스별 판정+인용+근거 등급 ② Loop-3: **skipped — no sealed predictions**
③ LLM vs 4스크린+Piotroski (사전 기준선 docs/baseline_screens.md §3) ④ 원본−교란
delta (또는 D7 오염 분기 보고) ⑤ 오류 1차 분류 (R1→R2→R3) ⑥ 장르 비대칭
⑦ D10 조건부 평가. 실패 기준: rank-sum p≥0.20 ∨ 중위 분리<10pp ∨ 퇴화 분포.

보고 언어 제약(3-6): 정밀도 % 헤드라인 금지 / n=8 ±35pp / 상한 명기 / D5 단일 실행
문구 / 선택·생존 편향 문단 / "Claude 기반 단일 파이프라인 한정" / 오염 프로브 문서
헤더 "these controls BOUND memorization risk; they do not eliminate it."
