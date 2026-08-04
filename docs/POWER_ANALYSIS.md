# FB-07 — AUC 표본수 검정력 분석

## 질문

관측된 AUC 약 0.83을 무정보 수준인 0.50 및 더 가까운 비교 수준인 0.65와
양측 유의수준 0.05에서 구별하려면 어느 정도의 표본수가 필요한가? 이 문서는
DP-Q3의 소유자 판단에 제공할 수치 근거이며, 새 케이스를 등록하거나 측정 조건을
바꾸지 않는다. 문맥상 공개 수치는 wave-1 8 대 22, wave-2 9 대 23, holdout
N=3 및 AUC 0.829 (95% CI [0.616, 0.983])이다.

## 선행 분석과 범위

RP-09의 시드 고정 Monte-Carlo 분석
[`scoring/rp09_power.json`](../scoring/rp09_power.json)은 wave-2 분리도에 대한
순열검정에서 **대조군을 몇 개** 둘지를 물었다. 여기서는 그 파일을 변경하거나
재계산하지 않는다. 본 분석의 질문은 **두 AUC 수준을 구별하려면 양 군의 N이
얼마인가**이며, 폐쇄형 근사식으로 계산한다. 따라서 두 분석은 질문과 방법이
다르다.

## 방법

Hanley와 McNeil (1982), “The meaning and use of the area under a receiver
operating characteristic (ROC) curve,” *Radiology* 143(1), 29–36의 독립
표본 AUC 분산 근사를 사용했다. AUC를 \(A\), treatment(양성) 수를 \(n_t\),
control(음성) 수를 \(n_c\)라 하면

\[
Q_1=\frac{A}{2-A},\quad Q_2=\frac{2A^2}{1+A},
\]

\[
\operatorname{Var}(A)=\frac{A(1-A)+(n_t-1)(Q_1-A^2)+(n_c-1)(Q_2-A^2)}
{n_tn_c}.
\]

이는 지수분포 가정에서 얻은 Hanley–McNeil 근사이며, 공변량이나 paired 설계가
주는 효율을 사용하지 않으므로 그런 설계와 비교하면 보수적일 수 있다. 귀무가설과
대립가설 각각의 표준오차를 사용해 귀무가설의 양측 임계값을 정하고 대립가설 아래
양쪽 기각 꼬리 확률을 합했다. 요구 N은 지정 control:treatment 비율에서 control
수를 올림한 뒤 목표 검정력에 처음 도달하는 최소 정수 \(n_t\)이다.

정규 CDF는 `math.erf`, 역 CDF는 Acklam (2003)의 rational approximation
(보고된 최대 절대 오차 1.15e-9)에 `erf` 기반 Halley 보정 1회를 적용한다. 스크립트가
문서화하고 테스트하는 유한 격자 확률 round-trip 오차 한계는 2e-9이다. 난수나
외부 패키지는 사용하지 않는다.

## 결과

아래는 `.venv/bin/python tools/power_analysis.py`의 재생성 가능한 실제 출력이다.
각 요구 N 셀은 `n_t/n_c/total`이다.

```text
Required N (alpha=0.05, two-sided)
AUC contrast | control:treatment | 80% (n_t/n_c/total) | 90% (n_t/n_c/total)
0.83 vs 0.50 | 1:1 | 11/11/22 | 14/14/28
0.83 vs 0.50 | 1:2.75 | 8/22/30 | 10/28/38
0.83 vs 0.65 | 1:1 | 32/32/64 | 40/40/80
0.83 vs 0.65 | 1:2.75 | 25/69/94 | 31/86/117

Achieved power (alpha=0.05, two-sided)
Design | n_t/n_c | 0.83 vs 0.50 | 0.83 vs 0.65
wave-1 | 8/22 | 0.832 | 0.285
wave-2 | 9/23 | 0.874 | 0.320
E2 trajectory (exploratory, D94) | 12/7 | 0.716 | 0.216
```

## 현재 세 설계의 판독

wave-1(8/22)의 근사 검정력은 0.50 대비 0.832, 0.65 대비 0.285이다.
wave-2(9/23)는 각각 0.874와 0.320이다. 탐색적 E2 trajectory layer
(D94, 12/7)는 각각 0.716과 0.216이다 — 이 행은 해당 층에 게시된 AUC가
없으므로 가상의 12v7 비교 설계에 대한 설계 검정력(design power)으로만
읽어야 한다. 즉 같은 AUC 0.83 대립가설에서도
0.65처럼 가까운 귀무 수준을 구별하는 검정력은 세 설계 모두 낮게 계산된다.
이 수치는 DP-Q3 판단의 입력일 뿐이며 N 확대 여부는 소유자 게이트 결정으로
남는다.

## 한계

- Hanley–McNeil 표준오차는 정확한 유한표본 분포가 아니라 근사다.
- ROC 점수의 binormal/exponential 계열 분포 근사가 실제 점수 분포와 다르면
  검정력도 달라진다.
- 이 case-control 표집은 전향적 스크리닝이 아니다. 모집단 base rate를 반영하지
  않으므로 PR-AUC와 PPV, 전향적 스크리닝 검정력 질문에는 답하지 않는다
  (EXT_FB_B item 10; 해당 질문은 DP-Q6 범위).
- 단일 관측 AUC를 계획 대립가설로 두었으며 그 추정 불확실성 자체를 별도로
  전파하지 않았다.

본 결과는 Claude 기반 단일 파이프라인에 한정된다 (PROJECT.md §5-5).
채점: Claude 보조 + 인간 최종 확정. 포지션 없음 · 교육·정보 목적 · 투자 조언
아님.
