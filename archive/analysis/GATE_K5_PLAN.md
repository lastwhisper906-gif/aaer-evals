# GATE_K5_PLAN.md — recognition gate k=5 승격 사전 등록 (D32, freeze-commit-then-run)

> 2026-07-10 기입. **본 문서와 `analysis/gate_k5_analyze.py`는 프로브 호출 전에
> 커밋된다** — 판정 규칙·임계·해석 문장은 결과를 보기 전에 고정된다.
> 우선순위 근거: E1 이후 Tier-③ 증거는 단일 케이스 HUBG에 의존하는데, 그 홀드아웃
> 자격을 결정한 recognition gate는 단발(k=1) 추첨이었다 (거짓음성 산술: 케이스당
> draw 인지 확률 30% 가정 시 3/3 통과 ≈ 0.7³ ≈ 34% —
> `docs/methodology_limitations.md` §Instrument bias directions). 발행 후 자격이
> 흔들리면 교정 비용이 수십 배가 된다 — 발행 전 k=5로 승격한다.

## 1. 대상·호출 (13 호출)

| 대상 | 내용 | 호출 |
|---|---|---|
| HUBG·WMK·GNE | knows_event 프로브 draws 2–5 (k=5는 기존 draw-1 포함) | 12 |
| HTZ (양성대조) | 민감도 재검증 1회 — 계기가 True를 낼 수 있음의 증명 | 1 |

- 러너: **동결 `tools/holdout_probe.py` 그대로 재사용** — 문구·스키마 무수정.
  출력 경로만 분리: `--out runs/holdout/recognition_k5/draw_{2..5}` ·
  HTZ는 `--out runs/holdout/recognition_k5/positive_control --kind positive-control`.
- 회사 문자열은 draw-1 transcript와 동일: Hub Group, Inc. / Weis Markets, Inc. /
  Genie Energy Ltd. / Hertz Global Holdings, Inc.
- 실행 순서: **HTZ 최우선 1호출** → knows_event=False(민감도 붕괴)면 **즉시 중단**
  + OWNER_QUEUE (게이트 계기 해석 불능 — draw 프로브 미발사). True면 draw 2–5 진행.
- 경계 커밋 4회: [HTZ+draw-2 4호출] · [draw-3 3호출] · [draw-4] · [draw-5] —
  각 커밋 전 `python tools/verify_blindness.py --write-manifest` (runs/ 신규 파일).

## 2. 판정 규칙 (사전 고정 — 완화 불가)

band = 케이스별 knows_event=True 수 / 5 draws (draw-1 = `runs/holdout/recognition/`,
draws 2–5 = `runs/holdout/recognition_k5/`). 판정은 `analysis/gate_k5_analyze.py`
(결정론)가 기계 적용한다 — 재해석 없음.

- **≥2/5 True → 해당 케이스 홀드아웃 자격 상실**: H2에서 제외, 발행 표면에 강등
  사유 명시, Tier-③ 서사 재작성. **HUBG가 해당하면 OWNER_QUEUE에 "Issue #2 발행
  보류" 긴급 항목 append.**
- **≤1/5 True → 자격 유지**: 발행 표면의 "recognition gate 3/3 (draw-1)"에
  "gate band x/5 per case (k=5)"를 **병기** (대체 아님 — draw-1 발행값 불변).
- HTZ가 knows_event=False → **SENSITIVITY_FAIL**: Phase 즉시 중단 + OWNER_QUEUE
  (양성대조 붕괴 시 0/5 결과는 "비인지"가 아니라 "계기 무감" 가능성 — 해석 금지).

## 3. 결과 3방향 해석 문장 (사전 등록 — 이 문장 외 재해석 금지)

- **(i) 3케이스 전부 0/5**: "recognition gate 판정은 draw 잡음에 강건 — 자격 3/3
  유지. 발행 표면에 band(0/5 ×3, k=5) 병기. k=1 거짓음성 산술(≈34%)은 반박된 것이
  아니라, 이 케이스 세트의 관측 인지율이 가정(30%)보다 낮은 방향임을 시사하는
  것으로만 기술한다."
- **(ii) HUBG만 ≥2/5**: "Tier-③의 유일 robust 케이스가 자격 상실 — HUBG를 H2에서
  제외, 강등 사유(게이트 k=5 재검에서 인지 재현) 발행 표면 명시, Tier-③ 서사를
  잔존 WMK·GNE(비분리) 기준으로 재작성 → 홀드아웃 tier의 탐지 주장 소멸.
  OWNER_QUEUE 긴급: Issue #2 발행 보류. E1·k=5 redraw 등 HUBG 파생 결과는 삭제가
  아니라 '자격 상실 케이스의 참고 기록'으로 강등 병기."
- **(iii) 그 외 조합** (WMK/GNE의 자격 상실, 또는 band 1/5 혼재 등): "자격 상실
  케이스는 H2 제외·강등 사유 명시 후 잔존 케이스 기준 Tier-③ 재기술. band 1/5
  케이스는 자격 유지 + band 병기(단발 인지가 재현되지 않음도 정직 기록). 본
  문장으로 덮이지 않는 세부 해석은 **보류하고 기록만** — 소유자 검토로 이관."

## 4. 불변량

- 발행 동결값(draw-1 게이트 3/3, 이름-ID 21.9%, R/H 판정 전부) 무변경 — 신규
  결과는 전부 병기. 이 계획 커밋(D32) 후에만 프로브 발사. 초과·낭비 호출은
  가계부에 정직 기록 (D26 gate_incident 형식).
