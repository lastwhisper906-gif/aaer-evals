# atlas/INDEX.md — Accounting Error Atlas 전수 색인

> authority: D106 ② (ERROR_ATLAS_v1). Template: `atlas/TEMPLATE.md`.
> status 어휘: pending → drafted → owner-finalized. 생성 순서 = D106
> follow-up 지시 순서 (wave-2 T → wave-1 T → holdout T → FP 전수 →
> FN/TN-flagged). FN 실험군(MON·LOGI·CSC·BRX·WMK·GNE)은 실험군 그룹에서
> outcome class FN으로 커버된다.

## 실험군 — wave-2 (AAER-confirmed, 9)

| case | ticker | outcome@50 (main) | entry | status |
|---|---|---|---|---|
| case_39 | OSIR | TP | atlas/case_39.md | drafted |
| case_40 | TNGO | TP | atlas/case_40.md | drafted |
| case_52 | CSC | FN (score 40) | atlas/case_52.md | drafted |
| case_59 | HAIN | TP | atlas/case_59.md | drafted |
| case_60 | MDXG | TP | atlas/case_60.md | drafted |
| case_61 | CGI | TP | atlas/case_61.md | drafted |
| case_65 | WFT | TP | atlas/case_65.md | drafted |
| case_66 | UAA | TP | atlas/case_66.md | drafted |
| case_67 | BRX | FN (score 20) | atlas/case_67.md | drafted |

## 실험군 — wave-1 (AAER-confirmed, 8)

| case | ticker | outcome@50 (main) | entry | status |
|---|---|---|---|---|
| case_01 | SCOR | TP | atlas/case_01.md | drafted |
| case_02 | OFIX | TP | atlas/case_02.md | drafted |
| case_03 | LOGI | FN (score 42) | atlas/case_03.md | drafted |
| case_06 | MON | FN (score 28) | atlas/case_06.md | drafted |
| case_08 | HTZ | TP | atlas/case_08.md | drafted |
| case_09 | ICON | TP | atlas/case_09.md | drafted |
| case_12 | KHC | TP | atlas/case_12.md | drafted |
| case_13 | MRVL | TP | atlas/case_13.md | drafted |

## 실험군 — holdout (provisional-4.02/restatement, 3)

| case | ticker | outcome@50 (main) | entry | status |
|---|---|---|---|---|
| case_71 | HUBG | TP-provisional (score 70) | atlas/case_71.md | drafted |
| case_72 | WMK | FN-provisional (score 32) | atlas/case_72.md | drafted |
| case_73 | GNE | FN-provisional (score 42) | atlas/case_73.md | pending |

## 오탐(FP) 전수 (11)

| case | ticker | cohort/frame | score | entry | status |
|---|---|---|---|---|---|
| case_10 | R | wave-1 main frame (8-control arm) | 58 | atlas/case_10.md | pending |
| case_30 | LQDT | wave-1 v2-controls frame | 65 | atlas/case_30.md | pending |
| case_33 | FORR | wave-1 v2-controls frame | 55 | atlas/case_33.md | pending |
| case_37 | RCKY | wave-1 v2-controls frame | 55 | atlas/case_37.md | pending |
| case_44 | ADAM | wave-2 | 55 | atlas/case_44.md | pending |
| case_48 | LPSN | wave-2 | 55 | atlas/case_48.md | pending |
| case_49 | IOVA | wave-2 | 58 | atlas/case_49.md | pending |
| case_54 | LEVI | wave-2 | 55 | atlas/case_54.md | pending |
| case_69 | AORT | wave-2 | 50 | atlas/case_69.md | pending |
| hc_03 | GRDX | holdout controls | 78 | atlas/hc_03.md | pending |
| hc_07 | GO | holdout controls | 58 | atlas/hc_07.md | pending |

## TN-flagged (E2 trajectory layer에서 플래그된 wave-1 대조군, 4)

| case | ticker | frame | entry | status |
|---|---|---|---|---|
| case_05 | PERY | E2 (main score 48) | atlas/case_05.md | pending |
| case_07 | XLNX | E2 (main score 25) | atlas/case_07.md | pending |
| case_11 | NUVA | E2 (main score 45) | atlas/case_11.md | pending |
| case_14 | GRMN | E2 (main score 32) | atlas/case_14.md | pending |

(case_10 R은 E2 플래그이기도 하나 FP 그룹 엔트리에서 함께 다룬다.)

## 종합

- `atlas/PATTERNS.md` — cross-case synthesis [human_finalized=false] — pending

*본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).*
