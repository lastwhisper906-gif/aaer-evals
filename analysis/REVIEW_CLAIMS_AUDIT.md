# REVIEW_CLAIMS_AUDIT.md — 외부 검토 주장 대조 (재현성 정합, Phase B1)

> Authored by Claude Code, pending human audit (GA-001 (b)). 2026-07-22 야간.
> 대상: 외부 검토(2026-07-20 수신)의 재현성 관련 주장 2건을 **병합 후 main**
> (D107 병합 커밋 0269b63 이후)에 대해 파일·행 증거로 판정.
> 판정 어휘: [still true / fixed by remediation merge / never true].

## 주장 (i) — "README의 4개 재현 명령이 '원문 코퍼스 불요'라고 주장하나 REPRODUCING·실제 코드와 모순"

**판정: still true** (병합 후에도 README 문구 잔존 — 본 세션 Phase B2에서 교정).

증거 (판정 시점 = 교정 전 README):

| 출처 | 내용 |
|---|---|
| `README.md` (교정 전 §"Reproducing the numbers") | 4개 명령(`reproduce_analysis.py`·`verify_blindness.py`·`verify_manifest.py`·`analysis/synthesis.py`) 직후 "All four use committed artifacts only (0 API calls, no source corpus needed)" |
| `REPRODUCING.md` (교정 전 §0 표) | `synthesis.py`는 "⚠️ XBRL 캐시 필요 — `screens.run_case`가 `~/aaer-data` PIT 조회", `verify_manifest.py`(full)도 "⚠️ XBRL 캐시 필요" |
| `analysis/synthesis.py:28` | `from screens import run_case` — 동결 기준선 **재계산** 호출 |
| `analysis/synthesis.py:42` | `baseline_mf()`가 `run_case(cand_rec)` 호출 |
| `scoring/baselines/screens.py:28` | `DATA_DIR = Path.home() / "aaer-data"` |
| `scoring/baselines/screens.py:98` | `xbrl_dir = DATA_DIR / ticker / "xbrl"` — 파일시스템 원시 코퍼스 의존 |

실측 (2026-07-22, HOME=빈 임시 디렉토리 샌드박스):
`reproduce_analysis.py`(PASS 100/100)·`lint_publication.py`(PASS)·
`verify_blindness.py`(PASS)·`verify_manifest.py --schema-only`(PASS)·
전체 pytest(266 passed, 9 skipped)는 코퍼스 없이 통과. `synthesis.py`와
`verify_manifest.py`(full)는 `~/aaer-data` 필요 — **REPRODUCING이 옳고
README가 틀렸다.** 해소 방향: 실제 코드 동작 우선 (검토 지시 그대로) —
README·REPRODUCING을 2계층 인터페이스(`make verify-public` / `make
verify-full`)로 재작성하고 `synthesis.py`는 full 계층에 배정 (로직 무변경).

## 주장 (ii) — "매니페스트 파일 수가 문서마다 402 vs 429로 불일치"

**판정: still true** — 그리고 **두 값 모두 현재값이 아니다**.

증거:

| 출처 | 값 |
|---|---|
| `REPRODUCING.md` (교정 전 §0 표·§1) | 402 파일 (2026-07-08 fresh-clone 실측 시점값) |
| `README.md` (교정 전) / `README.ko.md` | 429 파일 (이후 시점 스냅샷값) |
| **`data/manifests/aaer_data_manifest.json` `file_count` 필드 (기준)** | **538** |
| `tools/verify_manifest.py --schema-only` 실측 (2026-07-22) | "PASS (schema-only): 538 files, 585,654,364 bytes" |

원인: 매니페스트는 코퍼스 증분(Q-F01 캐시 보충, 홀드아웃·대조군 확장 등)마다
`--write`로 재생성되는데 문서의 수치는 손으로 박은 시점값이라 표류했다.
해소: 수치를 문서에 수기로 두지 않는다 — Phase B3 `tools/lint_doc_counts.py`가
매니페스트 `file_count`·pytest collected 수·재현 명령 목록을 저장소에서 유도해
README/REPRODUCING의 BEGIN/END-GENERATED 블록과 대조, 불일치 시 CI FAIL.
갱신은 `make docs-refresh`.

## 한정

본 문서는 감사 기록이다 — 교정 자체는 Phase B2/B3 커밋(README·REPRODUCING
재작성, Makefile 2계층 타깃, lint 배선)에서 수행되며, 판정 어휘의 기준 시점은
교정 커밋 직전 main이다. 본 결과는 Claude 기반 단일 파이프라인에 한정.
