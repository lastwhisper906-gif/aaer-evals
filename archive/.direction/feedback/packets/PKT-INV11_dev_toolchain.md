# PKT-INV11 — dev-toolchain amendment draft (Ruff / type check / coverage / pip-audit)
**STATUS: SIGNED (owner blanket, 2026-08-06, D-P83) — INV-11 amendment committed (6f04e2e); wiring queued as TASK_INV11.**
Status: OWNER SIGNATURE REQUIRED (INV-11 conflict — invariant wins, D-P45 rule).

## Why queued
EXT_FB_B item 9's quality-axis asks (lint, static types, coverage floor,
dependency audit, Dependabot) all require packages beyond the five frozen
top-level deps (INV-11: pytest·jsonschema·requests·pypdf·matplotlib,
hash-pinned lock). CI hardening's dep-free half landed separately (NB-02).

## Proposed amendment text (PROJECT_INVARIANTS.md INV-11, owner-signed commit)
Append: "예외 (D-P4x, 소유자 서명 시): 개발·CI 전용 도구 체인(ruff,
pyright 또는 mypy, pytest-cov, pip-audit)은 런타임 5종 동결과 별도의
`requirements-dev.lock`(해시 핀, pip-compile 생성)으로 허용된다. 채점·
파이프라인 코드는 이들 도구를 import할 수 없다(가드 스캔 대상). CI에서
비정본 보조 잡으로만 실행 — 정본 3.12 5게이트 잡은 무변경(INV-24)."

## Exact commands (after signature)
  pip-compile --generate-hashes -o requirements-dev.lock requirements-dev.in
  # + ci.yml additive job "quality" (continue-on-error 초기 도입, 실패 가시화)
  # + tools/test_no_dev_toolchain_import.py (pipeline/scoring 가드)

## Default if unsigned: stays queued; no effect on any gate.
