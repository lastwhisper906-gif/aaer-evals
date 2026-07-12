# RP-17 — D56/D57 사후 분모 개정: 소유자 분류 판정 패킷 (diff-only)

> Authored by Claude Code, 2026-07-13. 소유자 결정 대기 — 이 패킷은 어떤 결과도
> 바꾸지 않으며, 결정 재료와 원복 경로만 제공한다. (미션 문면은 RP-16을
> 지정했으나 RP-16은 D47 보정 언어 diff가 선점 — 차번호 RP-17로 발행.)

## 1. 사건 기술 (중립)

**공백**: B4 스펙(D55, 동결 커밋 `4753824`)의 SIR 분모는
`dei:EntityCommonStockSharesOutstanding` 단일 태그였다. 다중 클래스 발행사
(HUBG·GNE·UAA·RL·VIASP·VLGEA)는 클래스별(차원) 사실만 보고하고 SEC
companyfacts API는 차원 사실을 평탄화하지 않으므로, 해당 태그가 **체계적으로
부재** — fail-closed 규칙이 정상 작동하여 케이스가 탈락했고, 사전 등록 기대
커버리지(스펙 §6, holdout 12/12)와 실측(7/12)의 불일치로 발견됐다
(1차 실행 커밋 `287a92a`, 진단 포함 — 결과는 보존됨).

**개정 (D56, 커밋 `7994e2d` — 재실행 전 커밋)**: 분모를 4단 우선순위 사슬로
확장. 순서:

1. `dei:EntityCommonStockSharesOutstanding` (instant)
2. `us-gaap:CommonStockSharesOutstanding` (instant)
3. `us-gaap:WeightedAverageNumberOfDilutedSharesOutstanding` (duration, end 앵커)
4. `us-gaap:WeightedAverageNumberOfSharesOutstandingBasic` (duration, end 앵커)

규율: 케이스당 단일 소스(시계열 내 혼합 금지), 동일 (end, filed) 중복은 짧은
기간 승리, 전 태그가 D44 payload_v2 화이트리스트 내(신규 태그 0). 가중평균
주식수 = 기간 평균 ≠ 시점 잔고는 스펙 §13에 한계로 기록.

**재실행 (D57, 커밋 `efaf4a1`)** — 1차 대비 전량 델타 (results_b4.json 양판
git 실측, 생성기 결정론은 병합 세션이 재검증 `28a932b`):

| tier · score | 1차 (287a92a) | 재실행 (efaf4a1) |
|---|---|---|
| wave1 · level = slope-aug | 3/30, AUC 1.0 [1.0,1.0] p=.333 | 동일 (무변화) |
| wave2 · level | 2/32, 통계 불가 | 4/32, AUC 0.667 [0.0,1.0] p=.501 |
| wave2 · slope-aug | 1/32, 통계 불가 | 3/32, AUC 1.0 [1.0,1.0] p=.333 |
| holdout · level | 7/12, **AUC 0.1667** [0.0,0.5] p=.856 | 10/12, **AUC 0.5238** [0.048,1.0] p=.242 |
| holdout · slope-aug | 7/12, **AUC 0.1667** [0.0,0.5] p=.856 | 10/12, **AUC 0.4762** [0.0,1.0] p=.250 |

읽는 눈에 대한 정직: **AUC가 움직였다** (holdout +0.31/+0.36). 커버리지만
바뀐 것이 아니다 — 신규 편입 3건(HUBG·GNE·VIASP)이 통계에 들어왔기 때문이며,
이것이 §3의 분류 질문이 실재하는 이유다. wave-1/2는 개정 전후 모두
coverage-limited(<70%, 서술 전용)로 헤드라인 지위 무변화.

## 2. 원복 경로 (소유자 기각 시 — 정확 명령)

```bash
# ~/Documents/aaer-evals, main, 클린 트리에서:
git checkout 287a92a -- analysis/results_b4.json analysis/B4_REPORT.md
git commit -m "D59: RP-17 소유자 기각 — D57 결과 원복(1차 287a92a 정본 복귀), D56 사슬은 스펙 §13 '기각' 주석"
# 이어서 (append-only 규약):
#  - specs/B4_short_interest.md §13 말미에 '소유자 기각(RP-17, 날짜)' 주석 1줄 추가
#  - scoring/decisions_log.md 에 기각 D-엔트리 1줄 append
#  - analysis/b4_short_interest.py 의 SPEC_AMENDMENTS 항목에 기각 표기
#    (코드 사슬 로직 자체는 screener 운영용으로 존치 가능 — 별도 판단:
#     screener 01a4331/2287907 revert 여부는 스크리너 stage-1 설계 문제)
git push && gh run watch  # 게이트 5종 재실측 후
```
주의: `git revert efaf4a1`는 이후 커밋(28a932b·4e850ad)의 B4_REPORT 수정과
충돌한다 — 위 checkout 방식이 무충돌 정본 복귀다.

## 3. 소유자가 결정하는 분류 질문

> **이 개정은 '기계적 커버리지 결함 수리'(결과를 본 뒤에도 허용)인가,
> '분석 변경'(허용 불가)인가?**

**세션 측 논거 (기계적 결함 쪽)**: (i) 편입 기준이 결과와 무관한 기계 조건
(분모 태그 존재 여부)이고 편입 케이스는 그 조건이 자동 결정 — 케이스 선별
재량 0; (ii) 방향 예측 불가였고 실제 방향은 **기준선(경쟁자)을 강하게** 만드는
쪽 — 파이프라인 이해에 반하는(against-interest) 변화; (iii) 절차 준수 — 1차
결과 선커밋, 개정 스펙 선커밋, 재실행 후커밋, 전 과정 이력 공개(D56 원장
disclosure 절); (iv) 스펙 §6이 기대 커버리지 12/12를 사전 등록했으므로 7/12은
설계 결함의 *사전 등록된 검출*이다.

**최강 반론 (분석 변경 쪽)**: 세션은 holdout AUC 0.1667을 **본 뒤에** 개정을
설계했다. "커버리지 동기"는 사후 서사일 수 있으며, 어떤 사후 개정이든 통계를
움직였다면(실제로 +0.31 움직임) 그 개정의 채택 여부가 결과 지식에 오염되지
않았음을 증명할 방법은 절차 기록뿐이다 — 그리고 절차 기록은 자기 보고다.
또한 분모 선택지가 4개였다는 사실 자체가 재량 공간의 존재 증명이다 (다른
사다리 순서는 다른 AUC를 냈을 수 있다).

**세션 권고 (1문장 상한)**: 편입 기준의 기계성·방향의 역이해관계·N=3 판독
불능(어느 쪽 수치도 결론을 지지하지 않음)을 근거로 수용을 권고한다.

## 4. 제안 거버넌스 라인 (CLAUDE.md — 소유자 서명 시에만 적용, diff-only)

```diff
 ## 방법론 규율 (PROJECT.md §5) — 위반 시 프로젝트 무효
 ...
+6. **사후 스펙 개정 한계**: 결과를 본 뒤의 스펙 개정은 기계적 커버리지·
+   배관(plumbing) 결함 수리에 한해 허용되며, 반드시 (a) 1차 결과의 git 이력
+   보존 (b) 공개(disclosure) 절을 포함한 신규 D-엔트리 (c) 재실행 전 개정
+   커밋을 갖춰야 한다. 임계값·판정 규칙·지표 정의는 어떤 경우에도 사후
+   변경 불가.
+7. **5게이트 규율**: 게이트 실측은 pytest(analysis/ 포함)·reproduce·lint·
+   blindness·**verify_manifest** 5종 전부다 — 목록에서 하나를 다른 것으로
+   대체 실측하면 그 자리에 구멍이 생긴다 (2026-07-13 reference/ 미등재
+   이틀 미검출 사례).
+8. **단일 작성자 규율**: aaer-evals를 수정하는 세션은 동시에 최대 1개.
+   세션 개시·각 워크스트림 개시 때 git fetch + 60초 재확인·최근 커밋
+   author/시각·미추적 파일로 병행 작성자를 탐지하고, 감지 시 중단·보고한다.
+   워크트리 병렬성은 서로소 저장소(예: screener)에만 허용.
```

## 5. 학습 노트 (이 판단에서 알아야 할 것)

사후 개정의 수용 가능성은 개정 *내용*이 아니라 편입 기준의 *기계성*과 절차
기록의 *선커밋 순서*에서 나온다 — 그리고 그 순서를 증명하는 유일한 장치가
"1차 결과를 먼저 커밋"이므로, 이 관행(287a92a)이 없었다면 이 패킷은 분류
질문 자체가 성립하지 않았다.
