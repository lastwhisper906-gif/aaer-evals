# Run Log

## 2026-07-06 — Phase 3/4: 파일럿 + 격리 게이트 (freeze 개정 #2 경로)

> Authored by Claude Code, pending human audit (GA-001 (b), D15).
> 실행층 = `claude -p` 구독 헤드리스 (하네스 v2.1.201 실측 일치). 격리 기제 확정
> 이력: decisions_log 개정 #2 부록 J13-a(--bare 기각)~J13-e. 원시 증거:
> `logs/run_20260706T121146Z/` (파일럿), 격리 프로브·debug 트레이스는 세션
> scratchpad (미커밋 — debug.log 커밋 금지 지시).

### 격리 게이트 판정표 (기계 판정, PASS 5/5)

| # | 항목 | 판정 | 근거 (기계 검증 가능) |
|---|---|---|---|
| 1 | 파일럿 2건 스키마 통과 | **PASS** | case_90 (p=60, elevated)·case_91 (p=55, elevated) — llm_output v1.2 Draft-07 검증 PASS |
| 2 | 서빙 모델 = 핀 | **PASS** | modelUsage 단독 키 `claude-sonnet-5` (파일럿 2건) / `claude-fable-5` (파일럿 채점 2건, 폴백 0) — nonessential-call 차단 env 후 하우스키핑 haiku 항목 소멸 실증 |
| 3 | 격리 프로브 | **PASS (관찰 2건)** | 자백: files=[] · mcp=[] · can_run_commands=false · 저장소/CLAUDE.md/메모리 컨텍스트 0. 관찰 ①: tools=["StructuredOutput"] — `--json-schema` 출력 채널 그 자체 (환경 능력 아님, J13-f 판정 규칙). 관찰 ②: 하네스 system-reminder(userEmail·currentDate) 주입 — J13-e, 실험군·대조군 동일 적용 |
| 4 | verbose/debug 트레이스 오염 0 | **PASS (관찰 1건)** | grep 실측: CLAUDE.md 0건 · memory 0건 · 저장소 경로 0건 · hooks "Registered 0 hooks / Found 0 total" · plugins 0 · 프로젝트 skills 0. 관찰: `[claudeai-mcp] Fetched 6 servers` — 계정 커넥터 메타데이터 fetch 발생하나 **미부착** (session init 이벤트 `mcp_servers:[]`, `tools:["StructuredOutput"]` + 프로브 자백 mcp=[] 이중 확인) |
| 5 | 러너 테스트 green | **PASS** | pytest 51/51 (기존 30 + 신규 21: subprocess 모킹·변조 주입 가드·폴백·멱등) |

### 판정 규칙 재량 (J13-f)

게이트 3 "도구 0"의 판정에서 `StructuredOutput` 1건을 예외로 인정 — 이 항목은
`--json-schema` 플래그가 구조화 출력을 수신하는 채널 자체로, 이것이 없으면 출력
계약이 성립하지 않는다. 파일·명령·네트워크·MCP 능력이 아니며 페이로드 밖 정보에
접근할 수 없다. 인간 감사 플래그: 이 예외 인정이 게이트 3의 유일한 비자명 판정.

### 토큰 실측 → 본 실행 소요 projection (Max 20x 대비)

- 실측: 피평가자 호출 in ≈ 83K~126K (캐시 생성 포함) / out ≈ 9.5K~13.5K.
  채점 호출 in ≈ 8K / out ≈ 3.5K~4.5K. 격리 프로브 in ≈ 166K (재시도 포함).
- projection (잔여 58호출): 피평가자·프로브 32건 × ~100K in ≈ 3.2M in / ~0.35M out
  + 축어 프로브 8건 (≈1K in each) + 채점 24건 ≈ 0.2M in / 0.1M out
  → **총 ≈ 3.5M input (대부분 캐시 생성 단가) / ≈ 0.45M output**.
- 판단: Max 20x 한도 내 실행 가능 범위 — 단 5시간 윈도우 스로틀 가능성 있음.
  러너는 레이트 리밋 감지 시 정확한 재개 명령을 출력하고 중단 (멱등 재실행).
- 비용 참고 기록: total_cost_usd 합산은 참고 전용 (과금은 인증 경로=구독이 결정).

### 파일럿 채점 결과 (인간 감사 대상 1차 채점 — 중립 ID)

- case_90: d1=1 d2=2 d4=3 mem2=False / case_91: d1=1 d2=1 d4=3 mem2=False.
- 채점자 폴백 발동 0건. 파일럿 산출물은 pilot/ 격리 유지 (본 실험 디렉토리 혼입 없음).

## 2026-07-06 — Phase 5: 오염 프로브 → D7 분기 판정 (본 실행 전)

> These controls BOUND memorization risk; they do not eliminate it.
> 판정 규칙·정규화는 실행 전 커밋 (`72eefef` probe_verdict.py). 원시 출력:
> `scoring/probe_results/{recognition,verbatim}/` (중립 ID).

- **인지 프로브: 6/8 실명 지목** (comScore·Logitech·Hertz·Iconix·Kraft Heinz·
  Marvell — 익명화+상수배 재스케일+날짜 원본 페이로드에서). guess 원문은
  probe_results에 전건 보존.
- **D7 판정 (사전 등록 9f0fb42, 임계 ≥3): CONTAMINATED.**
  분기 효력: ① 본 분석 = **교란 실행 전용** ② 원본 입력 결과 = 부록 상한(upper
  bound) 전용 ③ 전 보고서 헤드라인에 오염 명시.
- 축어 회상: 완전 회상 0/8 (case_03·case_12 revenue만 ±2% 내, NI 실패 —
  known=true 2건 한정). 잔여 위험 등급: MED 6건 / LOW 2건 (probe_verdict 출력).
- 해석 노트: D8 소유자 결정의 예측("내용 기반 재식별은 어차피 발생")이 실측으로
  확인됨 — 교란은 암기 *측정* 장치이지 제거 장치가 아니다.

## 2026-07-06 — Phase 3-1 (D16 확인)
- **Loop 3 skipped — no sealed predictions** (본 실행 전 봉인 커밋 부재 실측:
  scoring/loop3/predictions.md 없음, 봉인 커밋 git 이력 없음). 분석 ②는 skip 노트로 대체.
- freeze 해시: 82a77176579ba6f84b2fcc00806d27d0d98601d7
- 실행 자격 증명: 부재 (ANTHROPIC_API_KEY unset, ant 프로필 없음) — API 실행 단계는
  "requires credentials" 상태로 스테이징. 페이로드 빌드·러너 구현은 오프라인 선행.
