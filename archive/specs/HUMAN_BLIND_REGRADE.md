# HUMAN_BLIND_REGRADE — 인간 블라인드 재채점 사전 명세 (SPECIFICATION ONLY)

> **SPECIFICATION ONLY — 실행·모집·발송하지 않는다.** 이 문서는 L-6의
> 동일 계열 채점자 편향을 검증하기 위한 프로토콜만 고정한다. 인간 재채점자
> 모집, 보상 합의, 표본 동결, 패킷 발송 및 결과 게시는 모두 소유자 전속
> 행동이며 소유자 서명 전에는 시작할 수 없다 (EXT_FB_B item 3; DP-Q8).
>
> 본 결과는 Claude 기반 단일 파이프라인에 한정된다. 채점: Claude 보조 +
> 인간 최종 확정. 포지션 없음. 교육·정보 목적이며 투자·법률·회계 조언이
> 아니다. 게시되는 모든 수치는 해당 공시 원문 링크를 동반한다.

## 1. 표본 추출

모집단은 `scoring/grades*/` 아래의 모든 `*.json`(예:
`scoring/grades/main/`, `scoring/grades/perturbed/` 하위 디렉토리 포함) 중
`_meta.human_finalized`가 `true`인 레코드 전부다
(`tools/apply_rp13_finalization.py:113`, `tools/cross_grader_skeleton.py:89`).
모집단은 저장소 상대경로의 UTF-8 바이트 오름차순으로 열거한 뒤 추출한다.
층 키는 `"<tier>|<arm>"`으로 고정한다. `tier`는 scoring/ 상대 grades
디렉토리(예: `grades/main`, `grades_v2/controls` —
`tools/cross_grader_skeleton.py:83`의
`f.parent.relative_to(scoring).as_posix()`와 동일한 키)를
`tools/cross_grader_skeleton.py:33-40`의 `TIER_BY_DIR`에 조회한 값이며 미매핑
디렉토리는 fail-closed한다. `arm`은 각 모집단 원 채점 JSON
한 파일만을 scoring-side 출처로 삼아 그 최상위 `dim2_mechanism`이 `null`이면
`control`, 아니면 `treatment`로 정한다. 이는 원 채점의 control N/A 규칙을
이용하는 명시적 프록시이며 별도 신원 맵의 ID 접두사로 추정하지 않는다.
arm은 재채점자에게 공개하지 않는다. 모집단 크기를 `N`, 층 `h`의 크기를
`N_h`라 할 때 총 표본은 `n = max(1, round_half_up(0.25 * N))`으로 정한다.
따라서 모집단의 25%를 뽑으며, 반올림은 `floor(0.25*N + 0.5)`이다.

층별 수는 Hamilton 비례 배분으로 고정한다. `q_h = n*N_h/N`, 먼저
`a_h = floor(q_h)`를 배정하고, 남은 `n-sum(a_h)`개는
`q_h-a_h`가 큰 층부터 하나씩 배정한다. 잔여율 동률은 위
`"<tier>|<arm>"` 문자열의
UTF-8 바이트 오름차순으로 푼다. 표본 수가 비어 있지 않은 모든 층을 포함할
만큼 클 때는 각 층에 1개를 먼저 배정한 뒤 같은 공식을 잔여 모집단과 잔여
표본에 적용한다. 어떤 층도 `N_h`를 초과해 배정하지 않는다.

시드 원문은 `human-blind-regrade-v1\n`과 표본 동결 커밋에서의 동결 루브릭
`scoring/eval_spec.md` 파일 바이트의 SHA-256을 이어 붙인 UTF-8 문자열이고,
`seed = SHA256(seed_source).hexdigest()`다. 각 층 안에서 레코드 `r`의
선정 키를 `SHA256(seed + "\n" + canonical_record_id(r)).hexdigest()`로
계산해 `(선정 키, canonical_record_id)` 오름차순으로 정렬하고 배정 수만큼
취한다. `canonical_record_id`는 저장소 상대경로와 레코드의 `case_id`를
`relative_path + "#" + case_id`로 결합한 값이다. scoring-side 실행자가
결정론적 Python으로 모집단 목록, blob hash, 층별 배정, 선정 키와 최종 표본을
호출 전에 신규 실행 산출물에 기록한다. 교체 추출은 허용하지 않는다.

### 예상 유효 pair 수와 검정력 하한

차원 `d`의 추출 전 예상 유효 pair 수는
`e_d = round_half_up(n * M_d / N)`으로 고정한다. 여기서 `M_d`는 모집단 중
결정론적으로 적용했을 때 해당 차원을 채점할 수 있는 레코드 수다. 구체적으로
dim3의 `M_d`는 모집단 중 원 채점의
`dim3_genre_mapping.mapped_genre`가 `null`이 아닌 레코드 수이고,
dim4_blind의 `M_d`는 quote가 하나 이상 있는 레코드 수다. 재채점자의 내용
판단에 따른 추가
`N/A_INSUFFICIENT`는 예측값에 넣지 않고 실제 유효 pair 수에서만 차감한다.
추출 후 실제 유효 pair 수는 선정 표본에서 양쪽 모두 N/A가 아닌 쌍을 직접
센다. **ESTIMATE:** 현재 `N=90`이면 `n=round_half_up(0.25*90)=23`이고,
현재 dim3 `M_d=26`이므로
`e_d=round_half_up(23*26/90)=7`이고, quote가 모두 존재한다는 가정 아래
dim4_blind `e_d`는 23이다. 이는 dim3에 관해
`specs/cross_grader.md` §2가 `n=10`을 기각하고 `n=20`을 최소 실용 규모로
사전 등록한 선례보다 작다. 새 power 계산은 만들지 않고 그 하한을 그대로 쓴다.
예상 또는 실제 유효 pair 수가 20 미만인 차원은 §4에 따라 `underpowered`로
보고한다. 이 명세는 25% 표본률을 올리거나 게시 수치를 변경하지 않는다.

## 2. 블라인딩과 레코드별 삭제 절차

scoring-side 담당자만 원본 레코드를 읽고 아래 allowlist 변환을 수행한다.
이는 `pipeline/`이 `scoring/`의 신원 맵·정답 키를 읽지 않게 하는 INV-08/09
경계를 유지한다. 재채점자에게는 `R001` 형식의 packet ID, 기제 내용,
근거 quote만 전달한다. 회사명·ticker·CIK·case ID·arm·모델 점수·기존
차원 점수·wave 소속은 패킷과 파일명에서 모두 제외한다. packet ID와 원본의
대응표는 scoring-side에만 둔다. packet ID는 선정 표본을
`SHA256(seed + "\npacketid\n" + canonical_record_id(r)).hexdigest()`의
오름차순으로 정렬한 뒤 `R001…Rnnn`을 순서대로 부여한다.

`schemas/llm_output.json`의 필드별 처리는 다음과 같이 고정한다.

| 원본 필드 | 재채점 패킷 처리 |
|---|---|
| `case_id`, `run_id`, `model`, `pipeline_version`, `run_timestamp`, `fingerprint` | 전부 삭제 |
| `documents_used[*]` | 전부 삭제 |
| `checklist[*].item_id`, `.question`, `.finding` | 그대로 유지 |
| `checklist[*].confidence` | 삭제 |
| `checklist[*].evidence[*].quote` | quote 문자열만 유지하고 packet 내 순번 부여 |
| `checklist[*].evidence[*].source_accession_no`, `.location`, `.computed_by` | 전부 삭제 |
| `misstatement_probability` | 삭제 |
| `mechanism_hypotheses[*].affected_line_items`, `.direction`, `.accounting_treatment` | 배열 순서를 유지해 기제 내용으로 제공 |
| `mechanism_hypotheses[*].rationale_evidence[*].quote` | quote 문자열만 유지 |
| `mechanism_hypotheses[*].rationale_evidence[*].source_accession_no`, `.location`, `.computed_by` | 전부 삭제 |
| `overall.risk_tier`, `overall.top_signals` | 전부 삭제 |

추가 값 수준 치환은 최소화하되, quote 또는 `accounting_treatment` 안의 회사명,
ticker, CIK, arm명, wave명, 모델명, 원본 case ID가 정확 토큰으로 나타나면
`[REDACTED_ENTITY]`로 바꾼다. scoring-side 담당자는 금지 토큰 사전으로 완성
패킷을 재스캔하고 적중 0건일 때만 소유자에게 전달한다. 숫자, 회계 계정,
기간 및 기제 표현은 변경하지 않는다. 원본-패킷 SHA-256, 치환 필드 경로,
치환 횟수는 비공개 대응표에 기록한다.

## 3. 재채점 도구

재채점자는 원 채점자와 같은 동결 루브릭인 `scoring/eval_spec.md` §4
(표본 동결 커밋과 파일 SHA-256으로 식별)를 사용한다. 다만 블라인드 패킷에 없는
정보를 추정하거나 보충하지 않고, 제공된 기제와 quote만으로 적용 가능한
차원 3의 장르 매핑과 차원 4의 블라인드 변형을 채점한다. 차원 2는 명령문
서술과 `genre_tags.md`의 pinpoint 사실을 요구하므로 블라인드 응답에서 제외한다.
차원 1은 확률과 arm이 가려져 있으므로 재채점 응답 표에서 완전히 제외한다.
제출 봉인과 키 공개 후 scoring-side가 `N/A_BLINDED`를 기록하며 일치도 분석에서
제외한다. 패킷에 기제 가설이 없거나 제공된 quote만으로 판정할 수 없는 경우
재채점자는 `N/A_INSUFFICIENT`로 기록한다.

응답은 packet ID별로 다음 필드를 갖는 고정 표다: `packet_id`, `dim3_mapping`
(`active|omission-estimate|mixed|N/A_INSUFFICIENT`), `dim3_rationale`,
`dim4_blind` (`0|1|2|3|N/A_INSUFFICIENT`),
`dim4_rationale`, `submitted_at`, `regrader_attestation`. 각 rationale은 제공된
quote 순번을 하나 이상 인용해야 한다. attestation은 독립 수행, 패킷 외 자료
미사용, 제출 전 정답 키 미열람을 확인한다. 재채점자는 모든 응답을 제출하고
수정 불가 상태로 봉인하기 전까지 answer key, 회사 대응표, 기존 점수·근거,
arm 및 wave 정보를 열람할 수 없다. `dim3_score`는 응답 필드가 아니다. 제출
봉인 후 scoring-side의 결정론 Python이 재채점자의 `dim3_mapping`과
`genre_tags.md` truth label에 동결된 3×3 행렬을 적용해 파생하며 모델은 이
과정에 관여하지 않는다.

`dim4_blind`는 동결 dim4에서 패킷 삭제 필드가 필요한 다음 두 조항을 적용하지
않는 변형이다: "인용이 제공 데이터에 없는 값(날조)" 판정, "risk_tier↔p 정합
위반 시 차원 4 상한 1". 그 밖의 0–3 앵커는 그대로 적용한다.

## 4. 분석과 사전 등록 판독

키 공개 후 원 채점과 인간 재채점을 차원별로 대조한다. arm에 따라 원 채점의
차원을 N/A로 만드는 처리는 키 공개 후 scoring-side가 적용한다. `dim3_score`는
§3의 방식으로 제출 후 파생한다. dim4 통계는 동결 dim4가 아니라 양쪽에 같은
제한 조항을 적용한 `dim4_blind` 간 일치도이며, 구조적으로 다른 원래 dim4와의
일치도로 표현하지 않는다. `dim4_blind`에는 quadratic-weighted Cohen's
kappa를 사용한다. 차원의
최댓값을 `K`라 할 때 범주 `i,j`의 가중치는
`w_ij = 1 - ((i-j)/K)^2`이고, `kappa_w = (P_o,w-P_e,w)/(1-P_e,w)`다.
dim4_blind는 `K=3`이다. 한쪽이라도 N/A인 쌍은 kappa에서 제외하되 제외
packet ID와 양쪽 값을 전부 공개한다. 분모가 0이면 값을 만들지 않고
`undefined`로 보고한다. dim3 mapping과 파생 score에는 kappa를 계산하지 않고
각각의 agreement matrix만 보고한다.

각 차원은 행=원 채점, 열=인간 재채점인 전체 agreement matrix를 원시 건수와
행 백분율로 게시한다. 정확 일치율, 유효 pair 수, N/A 수를 함께 쓰고,
dim4_blind에만 weighted kappa를 덧붙인다. kappa 해석 밴드는 계산 전에
다음처럼 실수 구간으로 고정한다:
`<0` 역방향, `[0.00,0.21)` slight, `[0.21,0.41)` fair,
`[0.41,0.61)` moderate, `[0.61,0.81)` substantial,
`[0.81,1.00]` almost perfect. 단, 이 명세에서 kappa를 계산하는 차원(현재
`dim4_blind`만 해당)의 §1 예상 또는 실제 유효 pair 수가 20 미만이면
`underpowered`와 유효 pair를 단위로 한 `B=10000`회 비모수 부트스트랩
percentile 95% 신뢰구간을 표시하고 어떤 밴드 라벨도 붙이지 않는다. 이때
RNG 시드는 §1의 `seed` 문자열을 재사용하며 벽시계나 미시드 난수를 사용하지
않는다. kappa를 계산하지 않는 차원은 유효 pair 수가 20 미만이면
`underpowered`와 agreement matrix만 표시하고 신뢰구간이나 밴드 라벨은
붙이지 않는다.

불일치는 축약하거나 표본만 고르지 않는다. 점수가 한 칸이라도 다르거나
mapping/N/A 상태가 다른 모든 packet을 공개하고, packet ID, 차원, 양쪽 값,
원 채점 rationale, 인간 rationale, 최종 합의 및 합의 rationale을 나란히
싣는다. 종전의 단독 `0 overrides` 보고는 이 검증 결과에서 사용하지 않으며,
그 자리를 차원별 agreement matrix와 전건 불일치 공개가 대체한다.

이 설계의 산출 범위에는 한계가 있다. dim1은 제외되고 dim2는 블라인드
채점하지 않는다. dim3은 전건 불일치 목록과 agreement matrix만 내며 kappa나
밴드 라벨을 내지 않으므로, 신뢰도 계수가 아니라 정성적 불일치 공개다.
`dim4_blind`만 kappa와 사전 등록 밴드 라벨을 내는 유일한 차원이다. dim3의
예상 또는 실제 유효 pair 수가 20 미만이면 `underpowered`와 agreement
matrix만 표시하며 신뢰구간이나 밴드 라벨은 붙이지 않는다.

## 5. 이견 조정

모든 불일치는 두 명의 인간이 원 패킷, 양쪽 rationale, 필요 시 키 공개 후
허용된 원 채점 자료를 검토해 합의로만 확정한다. 한 명은 최초 재채점자일 수
있지만 두 번째 사람은 독립성 기준을 별도로 충족해야 한다. 모델은 이견을
판정하거나 타이브레이크하지 않는다 (EXT_FB_B item 3). 합의가 되지 않으면
`UNRESOLVED`로 남기고 두 견해를 모두 게시하며, 어느 한 점수로 강제 병합하지
않는다. 합의 결과는 동결된 과거 점수를 덮어쓰지 않고 별도 재채점 산출물로
병행 게시한다.

## 6. 소유자 실행 패킷 — 사람을 찾은 뒤에만

### 모집 기준과 보상

모집과 후보 접촉은 소유자만 한다. 후보는 재무제표와 회계 추정·수익 인식·
충당부채를 읽을 수 있는 accounting-literate 성인이어야 한다. CPA/회계사,
회계감사·재무보고 실무자, 또는 동등한 교육·경력을 우선한다. 후보는 본
프로젝트, 대상 회사, 사용 모델 제공자와 현재 고용·투자·자문·친족 관계가
없어야 하며, 원 채점·파이프라인 개발·대상 케이스 선정에 참여하지 않았고
대상 레코드의 답을 사전에 본 적이 없어야 한다. 이해상충과 관련 보유 포지션을
서면 확인하며 하나라도 있으면 해당 후보를 배제한다.

**ESTIMATE:** 오리엔테이션 30분 + packet당 12–18분 + 제출 점검 30분이다.
예상 총시간은 `1시간 + 표본수 × 12–18분`이며 실제 표본 수와 난도에 따라
달라진다. 보상은 이 추정시간과 후보의 통상 전문 요율을 기준으로 소유자가
사전에 합의하고, 결과 방향·일치율·점수와 연동하지 않는다. 금액은 모집 시
소유자가 정하며 이 명세는 지출을 승인하지 않는다.

### 정확한 실행 클릭 경로/체크리스트

1. 소유자가 저장소의 `specs/HUMAN_BLIND_REGRADE.md`를 열고 SPECIFICATION
   ONLY 상태와 최신 소유자 서명 D-entry를 확인한다.
2. `docs/OWNER_QUEUE.md`에서 DP-Q8 관련 항목을 열어 후보의 경력,
   독립성 확인서, 시간·보상 합의, 두 번째 인간 조정자를 첨부하고 소유자가
   launch 승인을 서명한다.
3. 저장소의 Actions 탭을 클릭하지 않는다. 감독 중인 로컬 scoring-side
   세션에서 §1의 결정론 Python 추출을 실행하고 모집단·시드·표본 목록을
   신규 실행 경로에 저장한 뒤, 호출 전 커밋/동결한다.
4. §2 allowlist redaction을 실행하고 금지 토큰 스캔 `0 hits`, packet 수,
   packet SHA-256을 체크한다. 회사 대응표와 answer key는 공유 폴더 밖의
   scoring-side 제한 경로에 둔다.
5. 재채점자에게 이 문서 §3의 루브릭 링크/고정 응답표와 redacted packet만
   전달한다. 회사명, arm, wave, 모델 점수 또는 answer key가 보이지 않는지
   소유자가 화면에서 한 packet을 표본 확인한다.
6. 제출을 수신하면 전 packet ID 존재, 허용 enum, rationale의 quote 순번,
   attestation을 체크하고 파일을 읽기 전용으로 봉인한다. 그 후에만 대응표와
   원 채점을 분석 담당자에게 공개한다.
7. 결정론 Python으로 §4의 matrix와 kappa를 계산하고 모든 불일치 packet을
   두 인간에게 배정한다. 두 사람의 합의 또는 `UNRESOLVED`를 각각 서명받는다.
8. agreement matrix, kappa, 제외 목록, 전건 불일치와 양쪽 rationale,
   보상 방식, 표본 공식·시드를 신규 경로에 게시 후보로 만들고 소유자 최종
   게시 서명을 받는다. 과거 산출물은 수정하지 않는다.

<!-- Manual G2 / INV-13 vocabulary pass: PASS (2026-08-06); specs/ is not scanned by lint_publication.py. -->
