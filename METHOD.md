# METHOD.md — 파이프라인 방법 (1페이지, 원장 참조 없이 읽는 판)

> Authored by Claude Code, pending human audit (GA-001 (b)). 신규 주장 0 —
> 모든 문단은 저장소 소스 경로를 HTML 주석으로 단다. 상세 감사 이력이
> 필요하면 `AUDIT_INDEX.md`.

## 실행 경로 (한 케이스가 지나는 길)

<!-- source: pipeline/build_payload.py -->
**1. 페이로드 조립.** 케이스별 point-in-time 입력(XBRL 재무 시계열 + EDGAR
제출 이력)을 결정론 코드로 조립한다. 회사 정체를 가리는 교란(perturbed)
프레임은 명칭·티커·CIK 제거와 금액 재척도를 적용한다 (한계: v1 프레임은
accession 번호·제출 연대기를 유지 — 부분 탈익명화, README 발행 후 고지 절).

<!-- source: pipeline/cutoff_guard.py -->
**2. 컷오프 가드 (fail-closed).** 모든 원시 데이터 로딩은 단일 가드 모듈을
경유한다. 각 사실(fact)의 날짜를 케이스 컷오프일과 대조하고, 제출 문서는
EDGAR 제출 이력의 filingDate와 교차 검증한다. 컷오프 이후 데이터가 감지되면
해당 로드는 예외로 죽는다 — 우회 코드는 스캔 테스트가 금지한다.

<!-- source: pipeline/cli_client.py -->
**3. 격리 단일 호출.** 피평가자 호출은 저장소 밖 임시 디렉토리에서 실행되는
구독 헤드리스 `claude -p` 1회다. 설정·훅·MCP·내장 도구를 플래그로 전면
차단하고, 시스템 프롬프트를 대체하며, 송출 전 페이로드에서 정답지·카나리
마커를 값 수준으로 스캔한다(적중 시 호출 자체가 일어나지 않는다). 서빙 모델
핀과 하네스 버전 핀은 호출별로 검증·기록된다.

<!-- source: schemas/llm_output.json, pipeline/cli_client.py -->
**4. 스키마 강제 출력 (제한 재시도).** 출력은 JSON 스키마로 강제되고, 스키마
실패·빈 응답은 동일 입력으로 정확히 1회 재시도 후 FAIL로 기록된다. 열린
질문("이 회사 수상해?")은 어떤 프롬프트에도 없다 — 체크리스트·구조화 필드만.

<!-- source: tools/memo_verify.py, tools/blind_memo_verify.py -->
**5. 결정론 인용 검증.** 모델 출력의 원문 인용은 결정론 문자열 대조로
원본 공시에서 재확인된다. 검증 불가 인용은 통과되지 않고 판정 큐로 간다.

<!-- source: scoring/overrides.md, docs/OWNER_QUEUE.md -->
**6. 인간 판정 큐.** 비-VERIFIED 인용·채점 판정·발행 결정은 옵션/근거/
기본값 형식으로 소유자 큐에 적재되고, 서명 없이 해소되지 않는다.

## 누출 위협 모델

<!-- source: pipeline/cutoff_guard.py, scoring/threat_model.md -->
**Look-ahead** — 컷오프 후 데이터의 입력 혼입. 방어: §2의 가드 단일 경유 +
fail-closed + 가드 우회 스캔 테스트. <!-- source: pipeline/cli_client.py -->
**정답 누출(answer leakage)** — 채점 측 비밀(정답 키·섭동 계수·신원 맵)의
피평가자 노출. 방어: 송출 전 값 수준 마커 스캔(변조 주입 테스트 포함) +
pipeline/과 scoring/의 물리 분리. <!-- source: analysis/synthesis.md, docs/V1_PARTIAL_DEIDENTIFICATION_NOTE.md -->
**암기(memorization)** — 모델이 사건 결말을 학습 데이터로 아는 것. 차단
불가·측정만 가능: name-ID 프로브(50%→21.9%→0%), outcome-recognition 프로브
(wave-2 8/9), 컷오프-후 홀드아웃(구조적 불가 축)의 3계기로 공개 측정한다.
<!-- source: tools/verify_blindness.py -->
**카나리** — 채점 자료 GUID가 피평가자 산출물에 나타나는지 전 runs/ 스캔
(나타나면 즉시 FAIL). 채점 선행 이력 증명(criteria 커밋이 점수 커밋보다
앞선다)도 같은 게이트가 기계 검증한다.

## 역할 분리 계약

<!-- source: PROJECT.md §5·§7 -->
**Python이 계산하고, LLM은 질적으로만 판단하며, 인간이 서명한다.** 수치
계산(기준선·통계·검정)은 전부 결정론 Python. LLM은 원문 인용이 강제된
질적 판단만 담당하고, 그 채점 출력은 판정 근거 없이는 서명 대상이 아니다.
최종 확정은 인간 서명 전용 — 피평가자와 같은 계열의 모델이 자기 성적표를
단독 확정할 수 없다 (동일 계열 관대화는 한계 L-6으로 공개).

<!-- source: README.md Limitations -->
본 문서는 방법 요약이며 성능 주장을 포함하지 않는다. 수치는 전부
`RESULTS.md`(행별 한계 병기)에, 감사 이력은 `AUDIT_INDEX.md`에 있다.
본 결과는 Claude 기반 단일 파이프라인에 한정된다.
