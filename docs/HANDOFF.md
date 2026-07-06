# HANDOFF.md — 세션 인수인계 (최종 갱신: 2026-07-06, GA-001 사이클 Phase 4 종료)

> 다음 세션: CLAUDE.md → PROJECT.md → 이 문서 → `docs/execution_runbook.md`.
> 이번 사이클은 **GA-001 거버넌스 수정** (차단 게이트 → 비동기 review packet) 하에
> 진행됨 — 원문 `scoring/overrides.md` GA-001, 결정 대장 `scoring/decisions_log.md`.
> 인간 감사 진입점: **`review_packets/INDEX.md`** (재량 판단 J1~J12 + packet별 오버라이드 비용).

## 현재 위치: FREEZE 완료, 실행 대기 (단 하나의 격차 = API 자격 증명)

**freeze 커밋 = `82a7717`** (기준·루브릭·케이스·프로브·모델 핀 일괄 고정, push 완료).
Phase −1~2 + 3 실행층 + 4 문서 전부 완료. **남은 것은 `docs/execution_runbook.md`를
자격 증명 있는 환경에서 위에서 아래로 실행하는 것뿐이다** (프로브 → D7 분기 →
파일럿 → 본 실행 16+8 → 채점 → RP-03 분석 ①~⑦).

```bash
# 재개 절차 (요약 — 상세는 runbook)
source .venv/bin/activate && pip install anthropic
export ANTHROPIC_API_KEY=...   # 또는 ant auth login
python tools/verify_manifest.py          # PASS (264파일 기준선)
# 이후 docs/execution_runbook.md 순서대로
```

## 이 사이클의 고정값 (변경은 §5-6 이력 공개)

- 모델: 피평가자 `claude-sonnet-5` / 채점자 `claude-fable-5` (폴백 `claude-opus-4-8` — 발동 시 로그).
- 실험 16케이스: 실험군 8 (T07 MON·T11 OFIX·T12 LOGI·T13 HTZ·T16 ICON·T17 MRVL·
  T21 SCOR·T28 KHC) + 대조군 8 (C01 MOS·C02 NUVA·C03 GRMN·C04 R·C05 PERY·C06 XLNX·
  C07 FORR·C08 GIS — 선정 기록 RP-01, 실격 4건 포함). 중립 ID 시드 20260706.
- D7 오염 임계 ≥3/8 (사전 등록 `9f0fb42`) / D8 교란 = 익명화+상수배 (날짜 불변) /
  루브릭 4차원 + CL1~8 (freeze 개정 #1) / 실패 기준 rank-sum p≥0.20 ∨ 분리<10pp.
- Loop 3: **skipped — no sealed predictions** (logs/run_log.md).
- 사전 기준선 (분석 ③ 비교 대상): omission 장르 스크린 전멸 vs active 부분 신호
  (`docs/baseline_screens.md` §3) + 대조군 GIS의 F=1.66/C=6 (오탐 해부 1순위).

## 방법론 상태 (CI 녹색 — pytest 30 + validate + manifest)

- look-ahead 3채널 통제: cutoff_guard / point-in-time(`filed<=cutoff`) 테스트 /
  프로브 4종 (V5는 차단 불가 — 측정만, L-1).
- 페이로드 규약: evaluatee_input 5필드 + PIT 시계열 + 제출 연대기만. 러너가
  clean-tree(freeze-then-run)를 강제. pipeline↔scoring 상호 격리 정적 스캔 (V4/V7).
- 매니페스트 264파일/191.8MB (XBRL·대조군·AAER 색인 포함, 전건 source_url 귀속).

## 인간이 우선 볼 것 (비동기 감사 — INDEX.md 상세)

1. **J5 대조군 실격 4건** (Cherokee/Gartner/Avis=Cendant/URI) — 표본을 바꾼 판단.
2. **J1/J2 모델 핀** — 실행 전이 마지막 무비용 변경 기회.
3. **J8/J9 freeze 수치들** (밴드 경계 50, maxItems 3, rank-sum 0.20, CL 문언).
4. RP-01 §4-1: C05 PERY가 최약 매칭이라는 한계 수용 여부.

## 금지·주의 (실행 세션에서 그대로 유효)

- freeze 후 기준 변경 = 로그된 개정 + 재실행 노트. 코드 결함 수정만 예외 (테스트+로그).
- 세션 내 피평가자 판정 생성 금지 — 러너 경유만. 서브에이전트 대체 금지 (컨텍스트 상속).
- 파일럿(pilot/)·프로브(scoring/probe_results/) 출력의 본 실험(runs/) 혼입 금지.
- 보고 언어: % 헤드라인 금지 / n=8 ±35pp / 상한 명기 / D5 단일 실행 문구 / 선택·생존
  편향 문단 / §5-5 한정 문구 / 프로브 문서 BOUND-not-eliminate 헤더.
- 로컬 커밋은 기록이 아니다 — push까지.
