# PROTOCOL.md — cycle_001 동결 프로토콜 스냅샷

- generated: 2026-07-22 (tools/forward_prepare.py)
- spec: specs/FORWARD_WATCHLIST_V1.md (규범 원문)
- screening_cutoff: 2026-11-15 (ET, EDGAR acceptance)
- evaluatee_model (pin): `claude-sonnet-5`
- execution path: subscription OAuth only — `claude -p` + `CLAUDE_CODE_OAUTH_TOKEN` via `pipeline/cli_client.py` (INVARIANT 4)
- draws: k=1 · retry ≤2 · decision cuts: ≥70 flag / 40–69 review / <40 no_flag / insufficient→abstain (사전 등록 서수 컷)

## 동결 파일 해시 (준비 시점)

- `docs/UNIVERSE_SELECTION.md` sha256 `4eac2e56221883355038d63361ffdab1098e9b2c8a0bdb483042da5cbafa4796`
- `pipeline/build_payload.py` sha256 `f86ff0f962158e2e74b2eb3d8f1dc04fce3643481fafb1cd942524f7f30825c4`
- `pipeline/cli_client.py` sha256 `0a06a7e7527bb2215c07eff7140b6727d53db3b89b15bae161d2fa8a8aa42d52`
- `pipeline/runner.py` sha256 `5603f60ae51154b1f539b6f1597222f6b6a1cda0a8cdbb46edca30472d8d973c`
- `schemas/llm_output.json` sha256 `3f2187aadc6ae914e903ebe94f7b36e2918ef55bb0019cf32be8198fa8681d89`
- `specs/FORWARD_WATCHLIST_V1.md` sha256 `12715c06fc5051eb11cda27daedd66f7a516a9c275d2beccaa47794a6e690b74`
- `specs/RISK_SCORE_SEMANTICS.md` sha256 `93012e66b1ae86d5336bcc5888b28662b4307372b9134baff99c1f4112dafd53`

모델 승계 조항·중단 규칙: spec §5·§3. 봉인 후 본 파일 수정 금지.
