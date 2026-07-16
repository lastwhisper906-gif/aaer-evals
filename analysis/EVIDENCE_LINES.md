# EVIDENCE_LINES — 점수를 움직인 신호 유형 (기술 전용 부록)

> **신규 주장 없음.** 이 문서는 동결 채점 산출물(`runs/main/` 16 ·
> `runs/wave2/scores/` 32 · `runs/holdout/scores/` 3 — 총 51케이스)의
> 체크리스트 판정을 집계한 **기술 통계**다. 신규 실험·신규 미터링 0.
> 판별 성능과 그 한계는 여기가 아니라 README와
> `analysis/DECISION_TABLE.md`에 있다. 용도: GIL 메모의 "왜 이 방법을
> 신뢰하는가" 부록. 본 결과는 Claude 기반 단일 파이프라인에 한정
> (PROJECT.md §5-5). 채점: Claude 보조 + 인간 최종 확정.

## 1. 신호 유형 빈도표 — 실험군 vs 대조군 (정직 병기)

파이프라인은 케이스마다 고정 8항목 체크리스트(CL1–CL8)를 강제 출력한다
(열린 질문 금지 — PROJECT.md §5-4). 아래는 `finding == "flag"` 빈도.
실험군 20 = wave-1 fraud 8 + wave-2 fraud 9 + holdout 3(**G2 잠정 라벨 —
fraud 확정 아님**), 대조군 31 = wave-1 8 + wave-2 23.

| 항목 | 신호 유형 | 실험군 flag (n=20) | 대조군 flag (n=31) |
|---|---|---|---|
| CL1 | 매출채권이 매출보다 빠르게 성장 (AR/Revenue gap) | **16 (80%)** | 16 (52%) |
| CL2 | 소프트 자산(무형·기타·자본화) 팽창 | 9 (45%) | 15 (48%) |
| CL3 | 순이익–영업현금흐름 괴리 지속 | 13 (65%) | 14 (45%) |
| CL4 | 재고·마진 추세가 매출과 불일치 | 10 (50%) | 11 (35%) |
| CL5 | 매출·현금 변동성 대비 비정상적 이익 평활 | 2 (10%) | 1 (3%) |
| CL6 | 충당금·부채성 계정이 사업 성장에 역행해 감소 | 12 (60%) | **21 (68%)** |
| CL7 | 공시 연대기 이상 (지연·NT·정정 공시) | 17 (85%) | **23 (74%)** |
| CL8 | 데이터 커버리지 부족 (신호가 아니라 한계 기록) | 3 (15%) | 7 (23%) |

**이 표가 말하는 것과 말하지 않는 것 (정직 읽기)**
- 어떤 단일 체크리스트 항목도 판별자가 아니다 — CL7(공시 연대기)은
  대조군 74%에서도 발화하고, CL6은 대조군에서 **더 자주** 발화한다.
  대조군도 실제 상장사라 이런 신호를 일상적으로 낸다.
- 실험군 쪽으로 기우는 항목은 CL1(80% vs 52%)·CL3(65% vs 45%)·
  CL4(50% vs 35%)다 — 고전 발생액 계열(매출채권·현금흐름 괴리·재고)과
  일치하는 방향. 다만 이 표 자체는 판별 증명이 아니다. 판별은 8항목 +
  기제 가설을 종합한 서수 점수(0–100)에서 나오고, 그 성능·오탐·비용은
  README와 DECISION_TABLE에 구간과 함께 있다.
- 재계산: `python3 -c` 한 줄로 재현 가능 — 각 케이스 JSON의
  `checklist[].finding` 계수 (이 문서 하단 §4).

## 2. 유형별 대표 원문 인용 (실험군, 결정론적 선정 규칙)

선정 규칙(재량 배제): 해당 항목을 flag한 실험군 케이스 중 **케이스 ID
오름차순 첫 케이스의 첫 evidence 항목**. 인용은 채점 당시 모델에 입력된
XBRL/공시 발췌 그대로, accession no 병기.

| 항목 | 대표 인용 (원문) | accession no · 위치 |
|---|---|---|
| CL1 | "AccountsReceivableNetCurrent=68,348,000 (2012-12-31)" → 이듬해 90,040,000 (+32%) vs 매출 +12.5% | 0001158172-14-000004 · Balance Sheet, FY2012→FY2013 10-K (case_01) |
| CL2 | "Goodwill=454663000 (2012-09-30, 10-Q) vs Goodwill=1329300000 (2012-12-31, 10-K/A)" | 0001445305-12-003378 / 0001364479-14-000008 · Q3 10-Q vs FY 10-K/A (case_08) |
| CL3 | "NetIncomeLoss=-15,790,000 (FY2011)" — 이후 연도 순이익·영업현금흐름 방향 괴리 | 0001158172-14-000004 · Income Statement FY2011 (case_01) |
| CL4 | "InventoryNet=82969000 (2011-12-31)" — 매출 추세와 불일치 계열 | 0001193125-13-087561 · 10-K balance sheet (case_02) |
| CL5 | "NetIncomeLoss=59768000 (Q1 2014) vs 23870000 (Q4 2014) on relatively stable quarterly Revenues" | 0001193125-15-071602 · 10-K FY2014 quarterly data (case_09) |
| CL6 | "AllowanceForDoubtfulAccountsReceivableCurrent=0 (2015-03-31)" — 대손충당금 소멸 | 0001158172-15-000051 · Balance Sheet Q1 2015 (case_01) |
| CL7 | "10-Q filed 2013-05-03 … followed by 10-Q/A filed 2013-05-13" — 10일 만의 정정 | 0001158172-13-000034 · Filing chronology Q1 2013 (case_01) |
| CL8 | 재무활동·투자활동 현금흐름 시계열이 FY2011 이후 미제공 — 커버리지 한계 기록 | 0001104659-12-014637 · 10-K cash flow series (case_02) |

## 3. HUBG 박스 — 기계식 스크린이 계산 불능이던 곳의 LLM 플래그 (README 기술 범위 내)

> **Hub Group (HUBG, holdout case_71)** — p=70 (flagged), G2 잠정 라벨
> (8-K 4.02 non-reliance, fraud 확정 아님).
> - k=5 재추첨에서 5/5 모두 ≥50 (범위 58–76) — 사전 커밋 규칙(≥4/5)상
>   robust. 매칭 대조군 3사(RXO 42 · Brink's 30 · XPO 20) 전부보다 위.
> - **Beneish M-score·Dechow F-score는 입력 결측으로 계산 자체가 불능**
>   이던 케이스 — LLM 신호는 M/F의 복제가 아니다 (README ③).
> - 정직 병기 (README 그대로): ① holdout 풀 전체 최고 점수는 대조군
>   오탐(GridAI 78)이다 — HUBG는 자기 매칭 대조군은 이기지만 풀은 못
>   이긴다. ② 이 적중은 tier-correct / **mechanism-missed** — 모델은
>   2018년 재작성 군집에 앵커했고 2026년 재작성의 실제 기제는 놓쳤다.
>   리스크 스크리닝 ≠ 포렌식 기제 탐지. ③ N=3에서 통계 유의 주장 없음.

## 4. 재현 경로

```
python3 - <<'PY'
import json, glob
from collections import Counter
W1_T={"case_01","case_02","case_03","case_06","case_08","case_09","case_12","case_13"}
w2f=set(json.load(open("runs/wave2/fraud_case_ids.json")))
freq={"treat":Counter(),"ctrl":Counter()}
for p in glob.glob("runs/main/*.json")+glob.glob("runs/wave2/scores/*.json")+glob.glob("runs/holdout/scores/*.json"):
    d=json.load(open(p)); cid=d["case_id"]
    t = cid in W1_T or cid in w2f or cid in {"case_71","case_72","case_73"}
    for it in d["checklist"]:
        if it["finding"]=="flag": freq["treat" if t else "ctrl"][it["item_id"]]+=1
print(freq)
PY
```
