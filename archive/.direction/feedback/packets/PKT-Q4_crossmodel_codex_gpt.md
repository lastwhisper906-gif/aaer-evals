# PKT-Q4 — cross-model pass over frozen payloads via Codex CLI (GPT, subscription)
**Owner decision: SIGNED (D-P44b, 2026-08-05) — vehicle = Codex CLI
(ChatGPT subscription auth), zero-metered; GPT only; Gemini stays out.**
Status: ready-to-execute packet. Runs are a SEPARATE owner-launched step.

## INV-12 amendment text (for PROJECT_INVARIANTS.md, owner-signed commit)
Append to INV-12 참고 clause:
  "예외 (D-P44b, 소유자 서명 2026-08-05): 동결(payload-frozen) 회고
  케이스에 한해, 구독 인증 Codex CLI(zero-metered, INV-20 준수)를 통한
  GPT 교차모델 1패스는 스코프 위반이 아니다 — L-6(동일 계열 관대화)의
  실증 테스트 목적. 신규 케이스 확장·Gemini·종량 API 경로는 여전히 금지.
  결과는 신규 병행 경로(runs/crossmodel_gpt/)에만 기록."
Then `~/tools/harness/sync_context.sh .` regenerates CLAUDE.md/AGENTS.md.

## Run protocol (mirrors INV-19/21 discipline; NOT run by the loop)
- Input: the frozen evaluatee payloads (post-FB-01 blindness NOT
  retro-applied — use payloads AS FROZEN, disclosure L-9 covers markers;
  or regenerate blinded payloads as a v2 arm — OWNER CHOICE at launch,
  default: as-frozen for comparability with published Claude runs).
- Vehicle: `codex exec --sandbox read-only` per case, single isolated
  call, temp dir outside repo, same task text + llm_output schema
  (v1.2), model = Codex default GPT; record codex CLI version pin +
  served-model string per call (fail-closed on absence, INV-21 spirit).
- Output: runs/crossmodel_gpt/<case>.json + manifest regeneration;
  scoring by the existing frozen rubric; report as a NEW parallel table
  (never merged into published Claude rows); L-6 gets an evidence row.
- Quota: ~35 calls (30 wave-1 + wave-2 delta) on the Codex subscription
  pool — schedule away from harness-heavy days.

## Exact commands
  # amendment commit first (owner-signed), then:
  ~/tools/harness/run_task.sh --task .direction/feedback/tasks/TASK_Q4_runner.md \
    --workdir ~/repos/aaer-evals-work   # builds the crossmodel runner + tests
  # launch (owner or owner-supervised session):
  .venv/bin/python pipeline/crossmodel_gpt_runner.py --out runs/crossmodel_gpt
