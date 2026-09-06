# CROSS_GRADER_OWNER_PACKET.md — BN-09 소유자 패킷 (D121 재범위)

> **목적**: 한계 L-6(동일 패밀리 채점 관대화, `docs/methodology_limitations.md`)
> 정량화를 위한 교차 패밀리 채점자 스팟체크의 **소유자 실행 전 준비물 일체**.
> D121이 BN-09의 해소 조건을 "루프가 준비 가능한 패킷"으로 좁혔다:
> ① SPEC 확정 ② 선정 프로토콜 ③ fail-closed 호출 봉쇄 스켈레톤.
> 실 호출·채점자 모델 선정·일치도 표 산출은 전부 **소유자가 루프 밖에서**
> 실행한다 (게이트: `docs/OWNER_QUEUE.md` **Q-F07**, OPEN). 이 패킷의 어떤
> 부분도 Q-F07을 self-resolve하지 않는다 (INV-18).

## 1. SPEC 확정

- 기준 문서: **`specs/cross_grader.md`** — 커밋 **`4ee5e0b`** (2026-07-12)
  상태를 **최종(final)** 으로 확정한다. 추가 개정 불요 — launch-ready 동결
  그대로 발사 가능.
- 확정 내용 요약 (원문 우선, 충돌 시 spec이 이긴다):
  - **n = 20**, 노출 차원 = **dim2 (mechanism-match) · dim4
    (evidence-groundedness)** 두 주관 차원만 (dim1은 기계적 밴딩이라 제외).
  - 채점 프레임 = 동결 루브릭 앵커 프롬프트 **원문 그대로**, 피평가자 모델
    정체 비공개.
  - 사전 등록 판독 = **Cohen's κ ≥ 0.6 (양 차원 모두)** 유지 /
    κ < 0.6 시 해당 차원 "grader-dependent" 강등 **diff 제안 의무**
    (diff-only, 동결값 불변). 경계 0.6 단일, 중간 판정 없음.
  - 채점자 = 실행 시점 최강 가용 비-Anthropic 모델 — **소유자가 Q-F07에서
    선정** (spec은 사전 지명하지 않음).

## 2. 선정 프로토콜 — spec §2의 기계적 재서술 (seed 20260712)

구현: `tools/cross_grader_skeleton.py` (`select_sample`). 아래 산술이 spec
§2("비례 배분 · tier 최소 4건 · seed 20260712 정렬 후 균등 간격 추출")의
기계적 해석이며, 소유자는 발사 서명 시 이 해석을 함께 확정한다.

1. **모집단**: `scoring/grades*/` 전체의 `human_finalized: true` 레코드.
   패킷 작성 시점 실측 90건 — 디렉토리→tier 매핑 (확인 대상):

   | 디렉토리 | tier | 건수 |
   |---|---|---|
   | `scoring/grades/main` | wave-1 | 16 |
   | `scoring/grades/perturbed` | wave-1 | 8 |
   | `scoring/grades_v2/controls` | wave-1 | 22 |
   | `scoring/grades_wave2` | wave-2 | 32 |
   | `scoring/grades_holdout` | holdout+E1 | 3 |
   | `scoring/grades_holdout_controls` | holdout+E1 | 9 |

   미매핑 grades 디렉토리 발견 시 스켈레톤은 fail-closed (조용한 포함/배제
   금지).
2. **층(셀)**: tier × dim2 수준 × dim4 밴드.
   - dim2 수준 = spec의 {0,1,2} + **null** (대조군·무가설 레코드 — 실측
     관찰값 {null,0,1,2}, 3 없음).
   - dim4 밴드 (하/중/상의 기계적 밴딩 제안): **{0,1}=low · {2}=mid ·
     {3}=high** (실측 관찰값 {2,3}).
3. **배분**: n=20을 tier 수준에서 최대-잔여(largest-remainder) 비례 배분,
   각 tier 최소 4건 보장(부족분은 최대 배분 tier에서 결정론적 이전) →
   tier 내 셀 수준 최대-잔여 배분 (동률은 키 문자열 정렬). 현 모집단
   기계 적용 결과: **wave-1 9 · wave-2 7 · holdout+E1 4**.
4. **셀 내 추출**: 레코드 키(디렉토리/case_id) 정렬 후
   `offset = 20260712 mod m`, 인덱스 `(offset + ⌊i·m/c⌋) mod m`
   (m=셀 크기, c=셀 배분량) — 균등 간격, 자의 선정 봉쇄.
5. **표본 목록 freeze-commit = 소유자 발사 단계 (spec §5)**: 선정된 20건
   case_id 목록은 **채점자 호출 전에 소유자가 커밋**한다
   (freeze-commit-then-run). 루프는 목록을 커밋하지 않으며, 스켈레톤도
   목록을 출력하지 않는다 (선정 산술 적용 확인만 출력 — 루프 접촉 경계).

## 3. 스켈레톤 사용법과 Q-F07 연결

- **지금 실행 가능 (호출 0)**: `.venv/bin/python tools/cross_grader_skeleton.py`
  — 동결 루브릭 앵커(SYSTEM sha256 지문)와 층화 입력(모집단·tier·셀 계수)을
  결정론 적재하고, 채점자 호출 지점에서 **CALLS DISABLED 메시지와 함께
  비영 종료**한다. 네트워크 모듈 0, 자격 증명 요구 0, 신규 의존성 0
  (INV-11/INV-20 무접촉). 검증: `tools/test_cross_grader_skeleton.py`
  (fail-closed 종료 + import 허용목록 + 선정 결정론).
- **발사 절차 (전부 소유자, 루프 밖)** — Q-F07 서명 후:
  1. Q-F07 옵션 결정: **(A)** E4 교차모델 런과 같은 배치에 편승 발사 ·
     **(B)** 별도 시점 · **(C)** 기각 — 서명은 OWNER_QUEUE 해소 기록 +
     D-엔트리로 (INV-18 사슬).
  2. 채점자 모델 선정 + 자격 증명·과금(~20호출)은 소유자 인프라
     (2026-07-20 계획: Codex CLI 구독 인증 경유, 종량 API 키 금지 — Q-O08/D102).
  3. §2 산술로 20건 선정 → **case_id 목록 freeze-commit** (spec §5).
  4. 호출 경로는 소유자가 서명 하에 추가 (스켈레톤 확장 또는 별도 러너) —
     본 스켈레톤 파일 자체는 호출 봉쇄 상태가 기본값.
  5. 결과 = `runs/` 신규 하위 디렉토리 + 전역 MANIFEST 재생성 + 결정론
     Python κ 계산, E4와 산출물·D-엔트리 분리 기록 (spec §5).

---

*본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).
채점: Claude 보조 + 인간 최종 확정. 본 문서는 내부 거버넌스 패킷이며 발행
표면이 아니다.*
