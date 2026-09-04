# CHANGELOG.md

> 항목은 최신이 위. 발행 수치·동결 산출물 변경은 이 파일의 대상이 아니다
> (그건 ERRATA.md·decisions_log의 관할).

## 2026-09-04 — 외부 리뷰 C 반영: B1/B2 교차 티어 head-to-head (D-P105/D-P106)

- `specs/B1B2_CROSS_TIER.md` (freeze 95cf8cd) → `analysis/b1b2_screens_all_tiers.py`
  (코퍼스 tier, verify-full) + `analysis/b1b2_cross_tier.py` (공개 tier) →
  `analysis/out/b1b2_cross_tier/`. 동결 Beneish M / Dechow F 스크린을 LLM 점수와
  **동일 계산 가능 부분집합** 위에서 짝 비교(ΔAUC 층화 짝 부트스트랩 —
  `aaer_eval.statistics.boot_paired_auc_diff_ci` 신설), 동결 임계 탐지/오탐/정밀도
  (정확 CP95), 이름-식별 제외 민감도. RESULTS 행 14·15 신설(비준 대기), L-13.
- 리뷰 C 원문 `.direction/feedback/EXT_FB_C_2026-09-04.md`, 트리아지
  `audit/FEEDBACK_TRIAGE.md` §2026-09-04, 소유자 항목 Q-F22–Q-F25.
- 게시 수치·동결 산출물 변경 0 (행 1–13 불변; unified_table·baseline_table·
  results_stats·wave2_results·screens.py 무접촉).

## 2026-07-22 — 하네스 핀 강제 개시 (C3, D109)

- `pipeline/cli_client.py`: 런의 첫 호출 전 `claude --version` 실측을
  `HARNESS_PIN`과 대조, 불일치·명령 실패 시 fail-closed (모델 핀의
  modelUsage 사후 대조와 거울 지위). 실측 버전 문자열을 호출별 JSON 로그에
  `harness_version_actual`로 기록.
- **정직 기록**: 강제는 이 커밋부터다. **이전의 모든 런은 핀 상수를 로그에
  기록만 했고 실제 하네스 버전과 대조·강제하지 않았다** — 예컨대 2026-07-21
  세션 실측 CLI는 2.1.216이었고 핀은 2.1.201이었으나 어떤 런도 이를 이유로
  중단되지 않았다. 과거 로그의 `harness_pin` 필드는 "요청 핀"이지 "실측
  버전"이 아니다.
- 알려진 결과: 현 머신 CLI(2.1.216) ≠ 핀(2.1.201) — 다음 실 호출은 핀 개정
  (freeze 개정 전용) 전까지 fail-closed로 중단된다 (Q-O11).

## 2026-07-22 — 재현 인터페이스 2계층 고정 (B2/B3, D108)

- `make verify-public`(외부 데이터 0, 샌드박스 실측 증명) /
  `make verify-full`(코퍼스 의존) — README·REPRODUCING 재작성,
  문서-수치 lint(`tools/lint_doc_counts.py`) CI 배선.
