# E2_PREFLIGHT — 발사 전 정적 감사 (2026-07-13, 무호출)

**한 줄 답 (2026-07-13 D66/D67 갱신): E2는 명령 하나 거리다 — YES.**
잔여 차단 = **소유자 스모크 래치(§6-3) 단 하나.** 그 후:
`AAER_RAW_API_APPROVED=1 .venv/bin/python tools/e2_runner.py --execute`
(dry-run 실측: 드리프트 통과·계획 146·완료 0·temp 0.0·후처리 자동).
(이전 답 NO의 차단 3건 중 ①생성기 = D66 해소, ③RESUME 절 = 보완 완료.)

체크 방식: 각 줄은 명령으로 검증됐거나(✅ + 명령), 차단 항목이다(❌ + 조치).

## 1. 재개 문서·경로 정합

- ✅ `make smoke` 타깃 존재 (Makefile:13) · `tools/smoke_rev3.py` 존재 ·
  `runs/smoke_rev3/DRYRUN_MANIFEST.json` 커밋 상태 (30호출 계획, fail-closed
  불일치 정지). **스모크는 미발사** — 소유자 항목, E2 발사 전제 (§6-3).
- ✅ `pipeline/runner.py` / `pipeline/runner_api.py` 존재 (raw SDK 경로 =
  FREEZE_REV3, D40 Q-R02 GO — 래치 조건 §6 4건은 발사 세션이 확인).
- ❌→✅ `docs/RESUME.md`에 E2 재개 절 부재였음 (구절은 E3 명령 + 해소된
  Q-E01 보류 인용) — 본 세션이 2026-07-13 절 append (아래 ❌-1의 차단
  상태 포함). LAUNCH_SEQUENCE 2단계가 이 문서를 참조하도록 갱신.

## 2. 실행 재료

- ✅ **스냅샷 케이스 파일 (D66 해소)**: `tools/e2_generate_cases.py` →
  `data/e2/` 156파일 커밋 — 기록 146·배치 8·registry·매니페스트. 검증 명령:
  이중 전체 생성 바이트 동일(`diff -rq`)·매니페스트==기록 파일 수==사전
  산술(146)·실제 cutoff_guard 문서 단위 경유+독립 anti-leak 이중 통과·
  로스터는 규칙 기계 출력(테스트 `test_roster_equals_plan_rule_output`).
  b4 동반 실측 7/146 (D61 추정 3의 보수 과소집계 — 커버 2/13·판정 불변).
- ✅ **실행 하네스 (D67)**: `tools/e2_runner.py` — 드리프트/지출/온도/키
  4중 레일 + 크래시-재개 멱등(원자 기록, 중복 0·갭 0 테스트) + 후처리 자동
  (어댑터→engine_verdict→E2_SUMMARY, valid=false 라인 종단 테스트).
- ✅ `b3_score`/`b4_score` E2 컨텍스트 import 스모크:
  `python -c "... from b3_compute import b3_score; from b4_short_interest import b4_score"`
  → OK. 계약 테스트 `analysis/test_e2_interface_contract.py` (병행 호출·§8
  반환 키·결측=플래그·결정론) → **passed** (5게이트 pytest 135 포함).
- ✅ B4 데이터: `~/aaer-data/short_interest/` 79파일 아카이브 + 매니페스트
  등재 (D57 시점) — UAA 계산 가능 스냅샷 3점(D61)의 창 커버 확인.

## 3. 판정 경로

- ✅ `engine_verdict` §4b 비성립 자기 기록: 기존
  `test_b4_coverage_below_70pct_invalid` + 신규
  **`test_b4_invalid_at_d61_e2_shape`** (D61 산술 그대로 — 실험군 13·커버
  2(KHC형 s0 단독 + UAA형 3점)·11 전건 None → valid=false·커버리지 사유·기본
  판정 비오염) → 12 passed.
- ✅ `buyer_metrics_build` 합성 E2-형 픽스처 dry-run:
  `pytest analysis/test_buyer_metrics.py -q` → passed (D52 C2 픽스처 5건).
- ✅ 어댑터(E2 산출물 → e2_trajectories.json): D67이 선제 구축
  (`tools/e2_runner.py::build_trajectories`, q=floor(days/91)·s0=동결
  perturbed 재사용) — 합성 출력 종단 테스트 통과, 후처리에서 자동 호출.

## 4. 호출 산술 (동결 PLAN §1·§2·§5 문면 그대로 재생성, 2026-07-13)

- 적격 실험군 (detected): wave-1 6 (OFIX·HTZ·ICON·MRVL·SCOR·KHC — results_stats
  primary p≥50) + wave-2 7 (WFT·CGI·MDXG·HAIN·OSIR·TNGO·UAA) = 13.
- XBRL 제출 그리드 + 최소 요건(잔존 ≥6·10-K ≥1) 실측 스냅샷:
  **WFT 0** (XBRL 4건 — MON과 동일 경계 사유, PLAN 규칙의 기계적 귀결) ·
  OFIX 3 · 나머지 11케이스 8씩. **실험군 = 91**.
- 대조군 RP-01 8: **MOS 0** (XBRL 2건) · NUVA 7 · 나머지 6×8 = **55**
  (PLAN §4의 "8×8=64" 추정 대비 −9 — 최소 요건의 기계적 귀결).
- **합계 146 evaluatee ≤ 하위 cap 160 → §5 절단 규칙 휴면** (발동 시나리오:
  깊이 8→6 균일 축소 = 111). LAUNCH_SEQUENCE "~112–160호출" 밴드와 정합.
- **드리프트 플래그 2건 (스펙 변경 아님, 발사 세션 확인 사항)**:
  (i) PLAN §5 "실험군 ~7–8사" 추정은 §1 자신의 적격 규칙(13사)과 불일치 —
  산술은 §1이 지배, 146은 §1 기준. (ii) PLAN §5 "채점자 동수" 문구 —
  E2 지표(p 궤적·플래그 임계 돌파)는 피평가자 출력만 소비하므로 채점자
  0이 정합 (D49의 '점수 통계는 채점 0' 논리와 동일); 동수 해석 시 292로
  cap 초과. 발사 전 소유자 1줄 확인 권장 (OWNER_QUEUE 반영).
- 스냅샷별 컷오프·케이스별 깊이 전표는 이 문서와 동일 규칙으로 재생 가능
  (§4 재현: 레지스트리 + `~/aaer-data/{tk}/edgar/` isXBRL 10-K/10-Q).

## 5. 기대치 (D60/D61)

E2는 LLM vs **B3** 리드타임을 산다. B4 비교는 §4b가 valid=false로 자기
기록 (커버 2/13) — 무대는 전향 seal (첫 증거 ≈2027-11). 발사 편익 계산에
B4 해소를 계상하지 말 것.
