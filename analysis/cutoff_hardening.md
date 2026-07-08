# cutoff_guard 강화 — EDGAR accession 교차검증 의무화 (Track 3, 2026-07-08)

> 범위: **툴링/테스트만 수정.** frozen 수치(runs/·scoring/grades*) 무침해, 미터링 0, 네트워크 0.
> 커밋된 어떤 점수·등급도 변하지 않는다(이 코드 경로는 채점 실행이 아니라 데이터 로딩 게이트).

## 1. 구멍 (the hole)

`pipeline/cutoff_guard.load_document`은 유일한 데이터 로딩 게이트웨이다(CLAUDE.md 방법론 규율 1).
v1에서 EDGAR filing-date 교차검증은 **호출자가 `accession_no`를 넘겨줬을 때만** 발동했다:

- `accession_no`가 있으면 → 로컬 submissions JSON의 `filingDate`를 역조회해 호출자 신고
  `doc_date`와 대조하고, 불일치·미보유는 fail-closed. (강함)
- `accession_no`가 **없으면** → 교차검증이 통째로 생략되고, 가드는 호출자 자기신고
  `doc_date`만 믿고 컷오프 비교를 수행했다. (약함)

즉 EDGAR 문서를 로드하면서 `accession_no`를 그냥 생략하면, 진짜 filing 날짜가 컷오프
이후여도 호출자가 컷오프 이내의 `doc_date`를 자기신고하면 통과할 수 있었다 — 가드의 강도가
"호출자 메타데이터의 정확성에 종속되지 않게 한다"는 v1 설계 목표(모듈 docstring)에 정면으로
어긋나는 look-ahead 누수 경로. 감독 E1/holdout 실행에서 실제 EDGAR 1차자료를 로드할 때
이 구멍이 조용한 오염원이 될 수 있다.

## 2. 정확한 수정 (the fix) — cutoff_guard.py, 2지점

**Fix point 1 — 시그니처(라인 ~114):** 명시적 불리언 파라미터 추가.
```
accession_no: str | None = None, edgar_sourced: bool = False,
```

**Fix point 2 — 본문(doc_date 파싱 직후, accession 교차검증 블록 앞):** 강제 규칙 삽입.
```python
if edgar_sourced and accession_no is None:
    attempt("blocked", "edgar_accession_required")
    raise CutoffGuardError(
        f"case={case_id}: EDGAR 출처 문서(edgar_sourced=True)는 accession_no 필수 — "
        "호출자 자기신고 doc_date만으로는 통과 불가, filing-date 교차검증 강제(fail-closed)"
    )
```
`edgar_sourced=True`이고 `accession_no`가 있으면, 기존 `if accession_no is not None:` 블록이
그대로 실행되어 filing-date 교차검증이 **반드시** 일어난다. 따라서 EDGAR 문서는 이제
"accession 필수 + 교차검증 필수"를 만족해야만 로드된다. 기존 fail-closed(미등록 케이스,
UNRESOLVED 컷오프, 중복 case_id, accession 미발견/미보유, doc_date≠filingDate, cutoff 위반)는
전부 그대로다 — 약화된 검사 0, 신규 fail-closed 1.

## 3. EDGAR-스코핑 근거 (왜 전역 강제가 아니라 플래그인가)

`tools/build_earliness_snapshots.guard_snapshot()`은 `load_document`를 `accession_no=None`으로
**의도적으로** 호출한다. 이는 EDGAR 문서 로드가 아니라 순수 날짜 경계검사다:
`path_or_url="earliness_snapshot:case_NN"`, `loader=lambda _p: "verified"`. 스냅샷 그리드는 이미
`filed <= 스냅샷컷오프`로 자기정합적이라, 여기서 막아야 할 유일한 위반은 "스냅샷 컷오프 자체가
폭로 경계를 넘는 것"이며 그건 `parsed > cutoff` 비교만으로 충분하다. accession을 요구하면 이
정당한 비-EDGAR 경계검사가 깨진다.

그래서 규칙을 **모든 `load_document` 호출**이 아니라 **진짜 EDGAR 문서 로드**로 스코핑했다.
`edgar_sourced`는 기본 `False`이므로:

- 현존 호출자(guard_snapshot + 모든 테스트)는 이 인자를 넘기지 않아 **동작이 바이트 단위로 보존**된다.
- 실제 EDGAR 1차자료를 로드하는 미래 호출자만 `edgar_sourced=True`를 명시 → accession 필수화.

경로 문자열 패턴 감지(`earliness_snapshot:*` 제외) 대신 명시적 플래그를 택한 이유: 새 비-EDGAR
경로가 생겨도 실수로 규칙에 걸리지 않고, 호출 지점에서 "이건 EDGAR 문서다"라는 의도가 코드로
드러나 감사 가능하기 때문(안전한 기본값 = 규칙 미적용).

## 4. 신규 테스트 (pipeline/test_cutoff_guard.py, v2 섹션)

- `test_edgar_sourced_without_accession_fails_closed` — `edgar_sourced=True` + accession 없음 →
  `CutoffGuardError` 차단 + access-log에 `verdict="blocked", reason="edgar_accession_required"` 기록.
- `test_edgar_sourced_with_accession_after_cutoff_still_blocked` — accession 있으나 EDGAR
  filingDate가 컷오프 이후 → `CutoffViolationError`(기존 동작 보존, reason=`cutoff_violation`).
- `test_edgar_sourced_with_valid_accession_and_date_allowed` — accession + filingDate<=컷오프 →
  허용, 로그 reason에 `cross-checked` 포함.
- `test_non_edgar_call_without_accession_still_allowed` — 회귀: 기본(False)·accession=None 비-EDGAR
  호출은 여전히 허용(earliness 가드와 동형).

`pipeline/test_no_guard_bypass.py`에는 스캔 케이스 추가 불요 — 이 정적 스캐너는 네트워크
import/candidates.json/id_mapping/scoring import 우회를 잡는 것이고, 이번 변경은 게이트웨이
**본체를 강화**하는 것이라 우회 패턴과 무관하다(새 우회 표면을 만들지 않음).

## 5. 감독 E1/holdout 실행이 왜 더 안전해지나

감독 실행에서 실제 EDGAR 1차자료(10-K/10-Q 등)를 로드하는 호출자가 `edgar_sourced=True`를
쓰면, "accession을 빠뜨려 교차검증을 우회"하는 경로가 원천 차단된다. 호출자 자기신고 `doc_date`가
아니라 로컬 submissions JSON의 권위 있는 `filingDate`가 컷오프 비교의 근거가 되도록 **강제**되며,
검증 불가능한(accession 없는) EDGAR 로드는 조용히 통과하지 못하고 access-log에 `blocked` 증거를
남기고 예외로 중단된다. 이는 look-ahead 차단(PROJECT.md §5-1)의 강제 지점을 호출자 성실성에서
게이트웨이 불변식으로 옮긴다.

## 6. 불변·범위 확인

- 수정 파일: `pipeline/cutoff_guard.py`(2지점) + `pipeline/test_cutoff_guard.py`(테스트) +
  본 문서. runs/·scoring/grades*·published 무침해.
- frozen 수치 변경 0(데이터 로딩 게이트 코드이며 채점 실행 아님). 미터링 0, 네트워크 0.
- 타깃 테스트: `pipeline/test_cutoff_guard.py pipeline/test_no_guard_bypass.py
  tools/test_build_earliness_snapshots.py` → **22 passed**. earliness 가드
  (`test_guard_snapshot_allows_within_revelation` 등) 무회귀 통과로 비-EDGAR 호출자 보존 입증.
  (참고: 자기점검 명령에 있던 `pipeline/test_build_earliness_snapshots.py`는 존재하지 않는 파일 —
  earliness 테스트는 `tools/`에만 있음.)
