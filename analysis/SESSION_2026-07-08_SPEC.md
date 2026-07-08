# SESSION 2026-07-08 — 무인 하드닝 세션 freeze-spec (grader-free, ZERO metered)

> Orchestrator: opus (분석·오케스트레이션 전용 — evaluatee verdict/grade 생성 절대 없음).
> fable-5 소진 → **채점 불가** = grader-free 하드닝. **미터링 0·네트워크 0·frozen 불침해.**
> 브랜치 `hardening/2026-07-08`, 베이스 커밋 `94c8487` (pre-flight green: reproduce 100/100 ·
> reproduce_headline PASS · verify_blindness PASS(full history) · manifest schema PASS(402) ·
> lint PASS · pytest 123 passed 4 skipped). **이 스펙은 계산 전 동결 — 결과에 맞춰 규칙 변경 금지.**

## 불변 (위반 = 오염 = 세션 실패)
- runs/main·wave2/scores·perturbed·holdout/scores·grades* 및 published draw-1 **무침해**.
  모든 산출은 NEW 경로(analysis/ 또는 신설 runs/ 하위). runner/grader/probe_runner 미실행.
- Track별 파일 소유 분리(쓰기 충돌 방지). git 조작은 orchestrator 단독.

## Track 1 — 플래그 임계 민감도 (순수 재계산, grader-free)
동결 점수(runs/main·wave2/scores·holdout/scores)만 읽어, 임계 t∈{40,42,44,45,46,48,50,52,54,55,56,58,60}
스윕. 코호트별(wave-1 8v22·wave-2 9v23·holdout) TP/FP/FN/TN·FPR(Clopper-Pearson, 0카운트는
rule-of-three 3/n)·민감도·플래그 순열/Fisher p(**analysis/stats.py의 기존 추정기 재사용**).
t×metrics 표 + "knife-edge vs robust" 판정(t=50이 ±5 내 안정한가·결론이 어디서 뒤집히나),
AUC(results_stats.json)와 교차검증(분리 서사는 t 무관해야). 산출: analysis/threshold_sensitivity.md
+ .csv + fig_threshold_sensitivity.png + analysis/threshold_sweep.py(+단위테스트). stats.py 불변.

## Track 2 — 채점자 일치도/노이즈 하한 (기존 아티팩트, grader-free)
runs/hardening/regrade_opus/(opus SPOT-CHECK 재채점, 커밋됨) vs scoring/grades*/(fable-5). id_mapping*로
매핑 확인. 차원별(dim1/dim2/dim4) 원일치율·가능 시 Cohen's κ·불일치 목록(유형). **SPOT-CHECK 하한**
으로 프레이밍(헤드라인 재채점 아님, published grade 무변경, 전부 SPOT-CHECK 라벨). N 과소 시 κ 대신
N·CI로 정직 보고. **플래그를 뒤집을 불일치 → 큐잉(행동 금지).** 산출: analysis/grader_agreement.md + .csv.

## Track 3 — cutoff_guard 강화: EDGAR accession 교차검증 의무화 (코드+테스트, 무실행)
브랜치에서만 pipeline/cutoff_guard.py 수정: EDGAR 경로 문서는 accession_no 필수 + filing-date
교차검증 필수, 없으면 **fail-closed**. 기존 fail-closed 전부 보존·약화 0. 최소·자기완결(수정 ≤2지점).
테스트 추가(test_cutoff_guard.py·test_no_guard_bypass.py): accession 없는 EDGAR 문서→차단 /
accession+미래 filing date→차단 / accession+유효→허용. 전 suite 무회귀. 산출: 코드+테스트 +
analysis/cutoff_hardening.md(구멍·수정·감독 E1 안전화 논리). frozen 수치 변경 소지 시 STOP·큐잉.

## Track 4 — 재현성·격리 심층 재감사 (검증, 무실행)
full verifier battery(reproduce_analysis·verify_blindness·verify_manifest·lint) + pytest 전량 실행·
정확 출력·타이밍 기록. 불변 3(blindness/cutoff/immutability)의 코드 강제 지점 file:line 추적, 미커버
경로는 finding. load-bearing 경로의 테스트 공백에 NEW 테스트 추가(frozen 무변경, 전부 통과).
finding을 SAFE-FIX(브랜치 처리) vs OWNER-DECISION(큐잉) 분류(보수적 버킷 우선). 산출:
analysis/reaudit_2026-07-08.md(finding·file:line·검증 transcript) + 신설 테스트.

## OWNER-JUDGMENT QUEUE 규약
frozen 재해석·플래그 뒤집는 불일치·결과 유발 규칙변경·미터링/네트워크/E1/홀드아웃/320cap·발행/
채점확정·플랜 모호성 = **절대 self-resolve 안 함**. docs/OWNER_QUEUE.md에 Q-NNN(질문·옵션·권고+
비용/리스크·차단대상·무응답 기본값·OPEN) 즉시 append + 안전기본값으로 나머지 계속. 세션 말미
docs/OWNER_DECISIONS_2026-07-08.md에 전건 통합.
