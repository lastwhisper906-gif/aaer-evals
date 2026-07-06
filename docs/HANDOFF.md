# HANDOFF.md — 세션 인수인계 (최종 갱신: 2026-07-06, 연속 실행 세션 중단 시점)

> 다음 세션: CLAUDE.md → PROJECT.md → 이 문서 → `scoring/decisions_log.md` →
> `review_packets/RP-00` 순으로 읽을 것. **이번 사이클은 GA-001 거버넌스 수정
> (차단 게이트 → 비동기 review packet, 소유자 지시 2026-07-06)이 유효하다** —
> 원문·효력 범위는 `scoring/overrides.md` GA-001. 소유자 결정 D1~D18 전문은
> `scoring/decisions_log.md`. 연속 실행 모드의 전체 지시문은 세션 시작 메시지였으므로
> 저장소에는 decisions_log에 기록된 범위만 남아 있음 — 재개 시 소유자가 동일 지시문을
> 다시 제공하거나, 아래 "다음 작업" 목록으로 진행.

## 진행 상황 (이 세션에서 완료 — 전부 origin/main에 push됨)

| Phase | 상태 | 커밋 | 내용 |
|---|---|---|---|
| −1 거버넌스 | ✅ | `9f0fb42` | GA-001 verbatim 기록 + D1~D18 결정 대장 (`scoring/decisions_log.md`) — D7 오염 임계(≥3/8) 사전 등록 포함 |
| 0 상태 조정 | ✅ | `88dbfe2`, `6652416` | 매니페스트 PASS · D1 검증기 코드 강제(+테스트) · D18 감사(**백데이트 필요 없음** — GO/1차표 결정 당일 커밋 확인) · **실험군 8 확정 기록**(T07/T11/T12/T13/T16/T17/T21/T28) · T04 전신 CIK 재수집(합산 34분기 = diff §B-1 일치) · **T13 폭로 vehicle EDGAR 확인**(2014-05-13 NT 10-Q, accession 0001104659-14-038216) · 모델 고정 · D12 브랜치 삭제 · `review_packets/RP-00` |
| 1 베이스라인 | ✅ | `51d7c0f` | `scoring/baselines/screens.py` (Beneish M/Dechow F/Montier C/Sloan, point-in-time XBRL `filed<=cutoff`) + 테스트 4건(PIT 속성 2 + 누출 차단 + 결정론 스캔, CI 편입) · 실험군 8+VRX+GE 실행(`scoring/baselines/results/`) · `docs/baseline_screens.md` (**GE 누락장르 근맹점 실증** — 분석 ③ 사전 기준선) · `scoring/genre_tags.md` (10건 1차 소스 검증, ICON은 참조 매핑과 부분 불일치 → mixed 태그) |
| 2 판단 산출물 | 🔶 진행 중 | (이번 커밋) | `scoring/eval_spec.md` v1 (4차원 루브릭 + 중립 문언 + llm_output v1.2 개정 계획) · `scoring/threat_model.md` v1 (V1~V10 → 방어 매핑) 작성 완료. **self-red-team 완료 — 발견 12건(HIGH 6) eval_spec 부록 A에 기록됨, v1.1 반영은 미수행** (특히 #1 `fraud_probability` 필드명 누출, #5 샷건 가설, #6 evidence 스키마 모순은 스키마 v1.2 설계에 직결) |

## 핵심 결정·고정값 (이 세션 확정분)

- **모델 고정 (D6)**: 피평가자 = `claude-sonnet-5` / 채점자 = `claude-fable-5`
  (폴백 `claude-opus-4-8`). 근거·기각 대안: decisions_log "모델 고정 기록".
- **실험군 8 확정** (소유자 07-06): proposal의 8건 그대로. 장르 참조 매핑 검증 완료
  (genre_tags.md — ICON만 mixed로 조정, 감사 대상).
- **베이스라인 1차 신호**: active 장르 플래그 존재(OFIX M=-1.53·F=1.63, VRX F=1.97,
  KHC C=5/M=-1.83) vs omission 장르 전멸(GE/LOGI/HTZ 무신호 또는 계산 불능).
  ⚠️ 대조군 없는 해석 금지 — 존재 증명 어법만.
- **실행 격차 (중요)**: 이 세션 환경에 **ANTHROPIC_API_KEY·ant CLI·anthropic SDK 없음**
  → Phase 3의 실제 API 실행(파일럿·본 실행·프로브·채점)은 "requires credentials"
  격차. 재개 세션에서 자격 증명 확보 필요 (`ant auth login` 또는 API 키).
  서브에이전트로 피평가자 호출 대체 금지 (CLAUDE.md 등 컨텍스트 상속 → GP-6 위반).

## 다음 작업 (우선순위순 — Phase 2 잔여 → FREEZE → 3 → 4)

1. **2-1 마무리**: 부록 A의 red-team 발견 12건을 §1~§5에 반영 → 헤더 v1.1 갱신
   (필드명 `misstatement_probability` 개명, hypotheses maxItems 3+순위, evidence 의미
   재정의, 차원 1 밴드 겹침 해소 + 판별 통계, 차원 2/3 앵커·매핑 행렬 확정 등).
2. **2-5 오류 분류 체계 v1**: 데이터 문제 / 기준 문제 / 모델 판단 오류 3버킷 +
   MECE 배정 규칙 + does-not-fit 탈출 범주 (D15 헤더).
3. **2-3 오염 프로브 구현** (실행은 Phase 3): ① 인지 프로브(D7 분기 ≥3/8 —
   이미 사전 등록됨) ② 교란 집합(D8: 사명 익명화 + 상수배 재스케일만, 날짜 이동 없음)
   ③ 축어 회상 프로브 ④ 카나리 GUID(D9) → `scoring/canary.md`.
   전 프로브 문서 헤더: "these controls BOUND memorization risk; they do not eliminate it."
4. **2-4 Loop-3 지원**: 예측 폼 + 봉인 커밋 스크립트 + Brier 스크립트 (D16 선택).
5. **2-6 대조군 선정 (D17 규칙)**: 실험군 8 × 후보 2–3씩 수집 → 4축(산업/규모/
   회계기간/장르) 1차 소스 근거 + EDGAR XBRL 실측 + 비집행 확인(AAER 명부 부재 +
   SEC 집행 검색, 검색일 기록) → 자격자 중 규모+기간 최근접 → Review Packet 01.
   컷오프 = 매칭 실험군 복사(GP-9 ①). 이 세션에서 검토한 후보 풀 초안(미검증 —
   전부 비집행·XBRL 실측 필요): T07→MOS/DD/FMC, T11→NUVA/IART/WMGI,
   T12→GRMN/PLT/UEIC, T13→CAR/R/URI, T16→PERY/CHKE/XELB(규모-모델 트레이드오프
   기록할 것), T17→XLNX/SWKS/CY, T21→FORR/IT/NLSN, T28→K/GIS/CPB.
   ⚠️ Conagra(AAER 있음)·Broadcom(옵션 백데이팅)·Sequential Brands(오버플로 풀)는
   배제 확인됨. data.sec.gov·www.sec.gov 모두 이 환경에서 접근 가능 확인.
   전 후보에 4스크린 + **Piotroski(신규 구현 필요)** 실행.
6. **2-7 cases.json v1.2**: 대조군 8 편입(candidates.json group=control,
   matched_case_id, scheme_type 없음 — D1 검증기가 강제) → 16케이스 중립 ID
   고정 시드 재셔플 → id_mapping.json 갱신 → 방어 테스트 대조군 확장 → CI 녹색.
7. **llm_output v1.2 스키마 개정** (eval spec §3): fraud_probability(0-100) +
   mechanism_hypotheses 추가 — freeze 전 필수.
8. **FREEZE 커밋** (기계적, 차단 게이트 1 대체): eval spec v1.1 + threat model +
   taxonomy + decisions_log + 대조군 명단 + cases.json v1.2 + 프로브 설정 + 모델 핀
   일괄 → freeze 해시 기록 → Review Packet 02 (+ D11 회고 절: 오버라이드 0건 패턴 /
   23/30 A형 분포 / 게이트 비동기 전환). **freeze 전 채점 실행 절대 금지.**
9. **Phase 3**: D16 봉인 예측 확인(부재 시 skip 기록) → 프로브 실행 → D7 분기 문서화
   → 파일럿(VRX+GE, `pilot/` 격리) → 본 실행(원본 16 + 교란 8, 변형당 1회 — D5) →
   분석 ①~⑦ = Review Packet 03. 러너 요구사항: 순수 anthropic SDK 직접 호출,
   페이로드 = evaluatee_input 필드 + point-in-time 지표표 + 제출물 연대기만(D10),
   run log에 response.model·타임스탬프·freeze 해시·비용/토큰 기록(SR 11-7).
10. **Phase 4**: SR 11-7 메모 · review packet 색인(+오버라이드 재실행 비용) ·
    HANDOFF 갱신 · Loop-5 fading 목록.

## 주의 사항 (재개 시 그대로 유효)

- 매 세션 시작: `python tools/verify_manifest.py` → PASS 확인 (현 기준선 **166파일**,
  63,712,938B — XBRL companyfacts 11건 포함. manifest --write 시 xbrl 파일
  source_url 역산 실패 WARN은 무해).
- CI: `pytest pipeline/ tools/ scoring/` 26건 + validate_schemas + verify_manifest
  --schema-only. 전부 녹색 상태로 push됨.
- 금지 사항 유지: freeze 전 채점 실행 / 세션 내 피평가자 판정 생성 / 인간 서명·예측
  날조 / 백데이트 / 파일럿·프로브 출력의 본 실험 디렉토리 혼입 / 베이스라인 출력의
  피평가자 페이로드 반입 / 로컬 전용 커밋(push까지가 기록).
- 보고 언어: 정밀도 % 헤드라인 금지, n=8 ±35pp, 상한(upper bound) 명기, D5 단일 실행
  문구, 선택/생존 편향 의무 문단.
