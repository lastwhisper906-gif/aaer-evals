# REPRODUCING.md — 제3자 재현 가이드 (P5, fresh-clone 실측)

> Authored by Claude Code, pending human audit (GA-001 (b)). 2026-07-08.
> 목적(G2 공공재): 독자가 발행 수치를 **커밋 산출물만으로** 재계산·재검증할 수 있게
> 하는 것. 아래 경로는 2026-07-08 임시 디렉토리 fresh-clone에서 **실제 실행**해 확인했다.

## 0. 두 종류의 재현 (포터빌리티 경계 — 정직 기록)

| 검증 | 외부 재현자(캐시 없음) | 근거 |
|---|---|---|
| `reproduce_analysis.py` (발행 수치 100/100) | ✅ 완전 포터블 | 커밋된 분석 산출물만 재계산 |
| `lint_publication.py` (발행 정합) | ✅ 완전 포터블 | 커밋 문서·json만 |
| `pytest` (113 passed·4 skipped, 스냅샷) | ✅ 완전 포터블 | 코드·픽스처만 |
| `verify_manifest.py --schema-only` | ✅ 완전 포터블 | 매니페스트 자체 정합 |
| `verify_blindness.py` | ✅ 완전 포터블 | runs/ 커밋 산출물 + git 이력 |
| `make analysis`·`synthesis.py`·`calibration*.py` | ⚠️ **XBRL 캐시 필요** | `screens.run_case`가 `~/aaer-data` PIT 조회 |
| `verify_manifest.py` (full, 402 파일) | ⚠️ **XBRL 캐시 필요** | 원문 코퍼스 sha256 대조 |

**핵심**: 발행 헤드라인 수치의 재검증(`reproduce_analysis`)은 **원문 코퍼스 없이도**
가능하다 — 이것이 검증 가능성의 1차 방어선(§6-5)이다. XBRL 원시 캐시(`~/aaer-data`,
git 밖 — `data/README.md`)는 기준선 **재계산**에만 필요하며, 없으면 fetch 도구로
재구성하거나(§3) 요청 시 제공한다.

## 1. 완전 포터블 경로 (캐시 불요 — 누구나)

```bash
git clone <repo> && cd aaer-evals
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python tools/reproduce_analysis.py            # → PASS 100/100
.venv/bin/python tools/lint_publication.py              # → PASS
.venv/bin/python -m pytest pipeline/ tools/ scoring/ -q # → 113 passed 4 skipped (스냅샷, 증가 가능)
.venv/bin/python tools/verify_manifest.py --schema-only # → PASS (402 파일 스키마)
.venv/bin/python tools/verify_blindness.py              # → PASS (이력·카나리·runs)
```

**2026-07-08 실측 (감사 후 스냅샷, temp dir)**: reproduce PASS 100/100 · lint PASS ·
pytest **113 passed 4 skipped** · manifest --schema-only PASS(402) · blindness PASS.
(pytest 수는 커밋마다 증가하는 스냅샷 — 정확 값보다 전건 PASS 여부가 기준.)

## 2. 캐시 포함 전체 경로 (`~/aaer-data` 있을 때)

```bash
make analysis            # baselines.py + stats.py → baseline_table.csv, results_stats.json
.venv/bin/python analysis/synthesis.py          # 교차-웨이브 종합 (seed 20260708)
.venv/bin/python analysis/calibration_wave2.py  # wave-2 ECE
make verify              # reproduce + blindness + manifest(full) + lint 전부
```

**2026-07-08 실측**: matplotlib 미고정으로 synthesis가 fresh-clone에서 실패 →
`requirements.txt`에 `matplotlib==3.11.0` 추가(본 커밋). 추가 후 synthesis·make analysis·
calibration 전부 통과 재확인.

## 3. 원시 XBRL 캐시 재구성 (외부 재현자용)

`~/aaer-data`는 SEC data.sec.gov companyfacts + submissions의 로컬 캐시다(git 밖,
대용량). 재구성:

```bash
# CIK별 companyfacts (scoring-side 수집; SEC fair-access UA 필수)
.venv/bin/python tools/fetch_xbrl_facts.py       # 케이스·대조군 CIK companyfacts
.venv/bin/python tools/fetch_primary_sources.py  # submissions/제출 이력
```

SEC egress가 막힌 환경이면 두 도구가 **fetch 매니페스트(필요 URL 목록)**를 출력하므로
별도 취득 후 `~/aaer-data/<TICKER>/`에 배치. provenance는 `runs/*/control_pool_raw/
provenance.jsonl` 규약 승계.

## 4. 파이프라인 재실행 (피평가자 채점 — API/구독 필요, 재현 선택)

발행 수치 재검증에는 **불필요**(위 §1로 충분). 채점 자체를 재실행하려면 구독 OAuth
(`claude` CLI) 필요, ANTHROPIC_API_KEY 부재 assert. 예: E3 재추첨 재현 —
`python pipeline/runner.py --cases data/evaluatee/cases_wave2.json --perturbed --out
runs/wave2/perturbed_redraw/draw_2 --only <9 fraud ids>` (멱등·핀검증·레이트리밋 재개).

## 5. 월간 홀드아웃 재조사 (`tools/holdout_rescan.py`)

컷오프 후 신규 폭로(8-K Item 4.02)를 한 명령으로 누적 — `docs/FUTURE_HOLDOUT_CANDIDATES.md`
Tier-2를 채우는 절차. §3와 동일한 SEC fair-access UA, egress 차단 시 fetch 매니페스트 출력.

## 6. 면책

단일 Claude 파이프라인 한정. 발행 수치의 재검증은 커밋 산출물만으로 가능(검증 가능성 =
최선의 방어, §6-5). 채점 재실행은 하네스 매개라 원시 API와 다를 수 있다(L-2).
