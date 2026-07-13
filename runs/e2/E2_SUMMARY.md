# E2_SUMMARY — 자동 후처리 (tools/e2_runner.py, D67)

- 판정 브랜치: **a_llm_engine** (b_subcase=None)
- median lead — LLM 7.0분기 · B3 5.5분기
- b4_comparison.valid = **False** — 사유: 실험군 B4 커버리지 < 70% — 비교 불성립 (B4 스펙 §7 (i))
- (D60/D61 사전 예측: 커버리지 미달로 valid=false — 무료 신호 대결은 seal 관할)
- 다음: buyer_metrics — `.venv/bin/python analysis/buyer_metrics_build.py --logs-dir logs/<run_e2_*> --price-in <USD/MTok> --price-out <USD/MTok>`
- 판정 결과의 원장 기록(D-엔트리)·commit·push는 발사 세션 마무리 절차.
