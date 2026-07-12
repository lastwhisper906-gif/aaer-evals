# analysis/vendor — provenance (역방향 vendoring)

screener 저장소 모듈의 문자 그대로 스냅샷. **여기서 절대 수정하지 않는다** —
수정은 원본(screener)에서만, 그 후 재수출 + 이 기록 갱신. (screener의
vendor/aaer_evals 관용구를 역방향으로 재사용 — specs/B4_short_interest.md §8.)

- **원본 저장소**: ~/Documents/screener (github 원격 소유자 생성 전, OWNER_TODO S-03)
- **원본 커밋**: `b60fd85` (2026-07-13 재수출 — D53→D56 주석 재부여 반영; 직전 `01a4331`)
- **무결성 테스트**: analysis/test_b4_short_interest.py::test_vendor_integrity

| File | Source path in screener | sha256 |
|---|---|---|
| `short_interest.py` | `ingest/short_interest.py` | `e72de0a303ff93917b17c2f9f9a2a61500c1e9f330c24f2c5cf384a0b39613f6` |
