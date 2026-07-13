# DRAW_K3 리포트 — median-of-3 병기 (Q-F06-B, 동결 draw-1 불변)

> temp=0이 배포 API에서 결정론을 보장하지 않으므로 median-of-k는 분산 완화이지 제거가 아니다 (스펙 §1 — 발행 표면 인용 시 동반 의무)

> 본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).

## wave1 — flip-rate 3/30

- case_02: gained_flag (draws [45, 55, 60] → median 55)
- case_08: lost_flag (draws [55, 45, 45] → median 45)
- case_33: lost_flag (draws [55, 18, 28] → median 28)
- median-of-3 AUC 0.8494 CI [0.665, 0.983] p=0.00168 — **병기 전용**

## wave2 — flip-rate 3/32

- case_69: lost_flag (draws [50, 45, 48] → median 48)
- case_49: lost_flag (draws [58, 48, 42] → median 48)
- case_40: lost_flag (draws [55, 42, 45] → median 45)
- median-of-3 AUC 0.8261 CI [0.618, 0.981] p=0.00084 — **병기 전용**

