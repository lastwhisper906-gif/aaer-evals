"""memo_run.py — 티커 일반화 메모 러너 (blind_memo_run.py의 매개변수화 후계, P1).

blind_memo_run.py는 OUT-GIL-V1 기록으로 동결 — 본 파일은 경로/ID만 매개변수화한
후계다. INSTRUCTION·SCHEMA·페이로드 조립 로직·cutoff_guard 경유·모델 핀은
바이트 동일 상속 (tools/test_memo_pipeline.py가 상수 동일성과 GIL 페이로드
sha256 재현을 강제한다 — 재현 게이트).

문서 로스터는 하드코딩 대신 매니페스트(JSON)로 받는다:
  {"stages": {"annual": [{"filing_date","accession","file","label"}...],
              "combined": [...]},
   "combined_uses_prior_flags": true}

--dry-run: 전 페이로드를 조립해 토큰 추정·문서별 컷오프 판정을 보고하고
DRYRUN_MANIFEST.json을 쓴 뒤 호출 직전에 종료한다 — 유니버스 비용 추정을
무호출로 산출하는 경로 (P4 spend gate 입력).

Usage:
  python tools/memo_run.py --registry data/<t>/registry.json --case-id OUT-<T>-V1 \
      --docs data/<t>/memo_docs.json --out runs/<t>_memo_v1 [--stage all] [--dry-run]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "pipeline"))
from cli_client import call_model  # noqa: E402
from cutoff_guard import load_document  # noqa: E402
from runner import EVALUATEE_MODEL  # noqa: E402

# Verbatim from the task definition — do not edit without invalidating the experiment.
# (blind_memo_run.INSTRUCTION과 바이트 동일 — 테스트 강제)
INSTRUCTION = (
    "You are a forensic accountant. Analyze the attached SEC filings of this company. "
    "Identify the 3-5 most significant accounting red flags or anomalies, prioritizing "
    "issues in revenue recognition, receivables, off-balance-sheet arrangements, cash "
    "flow vs earnings divergence, and footnote disclosures. For each flag: "
    "(1) describe the anomaly, (2) quote the exact supporting passage(s) verbatim "
    "with their location (item/note number), (3) explain the verification path — "
    "what a human analyst should check to confirm or dismiss this, (4) state your "
    "confidence (low/medium/high) and what additional data would change it. "
    "Base every claim strictly on the provided documents. If the documents do not "
    "support a claim, do not make it."
)

# (blind_memo_run.SCHEMA와 동일 — 테스트 강제)
SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["flags"],
    "properties": {
        "flags": {
            "type": "array", "minItems": 3, "maxItems": 5,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["title", "description", "quotes",
                             "verification_path", "confidence",
                             "additional_data_that_would_change_confidence"],
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "quotes": {
                        "type": "array", "minItems": 1,
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "required": ["text", "location"],
                            "properties": {
                                "text": {"type": "string",
                                         "description": "verbatim passage from the documents"},
                                "location": {"type": "string",
                                             "description": "document + item/note number"},
                            },
                        },
                    },
                    "verification_path": {"type": "string"},
                    "confidence": {"enum": ["low", "medium", "high"]},
                    "additional_data_that_would_change_confidence": {"type": "string"},
                },
            },
        }
    },
}

PRIOR_FLAGS_PREAMBLE = (
    "Your prior analysis of this company's annual filing produced the flags "
    "below. The additional filing documents follow; update, confirm, replace "
    "or re-rank your flags into a final set of 3-5 based on all documents "
    "you have now seen.\n\nPRIOR FLAGS (your own earlier output):\n"
)


class MemoConfig:
    def __init__(self, registry: Path, case_id: str, docs_manifest: Path,
                 out: Path, prior_flags_path: Path | None = None) -> None:
        self.registry = registry
        self.case_id = case_id
        self.data_dir = registry.parent
        self.out = out
        m = json.loads(docs_manifest.read_text(encoding="utf-8"))
        self.stages: dict[str, list] = m["stages"]
        self.combined_uses_prior_flags: bool = m.get("combined_uses_prior_flags", True)
        self.prior_flags_path = prior_flags_path or (out / "flags_annual.json")


def build_payload(cfg: MemoConfig, docs: list, prior_flags: dict | None = None) -> str:
    """blind_memo_run.build_payload와 조립 로직 바이트 동일 — 경로만 매개변수."""
    parts = []
    if prior_flags is not None:
        parts.append(PRIOR_FLAGS_PREAMBLE + json.dumps(prior_flags, indent=2))
    for d in docs:
        text = load_document(cfg.case_id, str(cfg.data_dir / d["file"]), d["filing_date"],
                             accession_no=d["accession"], registry_path=cfg.registry)
        parts.append(f"=== BEGIN DOCUMENT: {d['label']} ===\n{text}\n=== END DOCUMENT ===")
    return "\n\n".join(parts)


def _load_prior_flags(cfg: MemoConfig) -> dict | None:
    if cfg.prior_flags_path.exists():
        return json.loads(cfg.prior_flags_path.read_text(encoding="utf-8"))
    return None


def stage_payload(cfg: MemoConfig, stage: str) -> tuple[str, bool]:
    """(payload, prior_flags_present). combined에서 prior flags 부재 시 무전문 조립
    (dry-run 사전 추정용 — 실발사 combined는 flags_annual 필수)."""
    docs = cfg.stages[stage]
    if stage == "combined" and cfg.combined_uses_prior_flags:
        prior = _load_prior_flags(cfg)
        return build_payload(cfg, docs, prior_flags=prior), prior is not None
    return build_payload(cfg, docs), False


def dry_run(cfg: MemoConfig, stages: list[str]) -> dict:
    cfg.out.mkdir(parents=True, exist_ok=True)
    manifest: dict = {
        "mode": "dry-run (assembled payloads, no calls)",
        "case_id": cfg.case_id,
        "registry": str(cfg.registry.relative_to(REPO)) if cfg.registry.is_relative_to(REPO) else str(cfg.registry),
        "model_pin": EVALUATEE_MODEL,
        "token_estimate_rule": "chars/4 (휴리스틱 — 과금 등가 실측은 BUYER_METRICS §3 $0.5304/스크린)",
        "stages": {},
    }
    for stage in stages:
        payload, prior_present = stage_payload(cfg, stage)
        docs = [{"file": d["file"], "filing_date": d["filing_date"],
                 "accession": d["accession"], "cutoff_verdict": "allowed"}
                for d in cfg.stages[stage]]  # load_document가 위반 시 이미 예외로 중단
        manifest["stages"][stage] = {
            "payload_sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
            "chars": len(payload),
            "est_input_tokens": len(payload) // 4,
            "prior_flags_present": prior_present,
            "documents": docs,
        }
        print(f"[dry-run:{stage}] {len(payload):,} chars ≈ {len(payload)//4:,} tokens "
              f"sha256={manifest['stages'][stage]['payload_sha256'][:12]} "
              f"prior_flags={prior_present}", flush=True)
    out = cfg.out / "DRYRUN_MANIFEST.json"
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    print(f"[dry-run] wrote {out} — no calls made", flush=True)
    return manifest


def run_stage(cfg: MemoConfig, stage: str) -> bool:
    cfg.out.mkdir(parents=True, exist_ok=True)
    if stage == "combined" and cfg.combined_uses_prior_flags:
        prior = _load_prior_flags(cfg)
        if prior is None:
            print(f"[{stage}] flags_annual 부재 — combined 실발사는 annual 완료 후에만",
                  flush=True)
            return False
        payload = build_payload(cfg, cfg.stages[stage], prior_flags=prior)
    else:
        payload = build_payload(cfg, cfg.stages[stage])
    print(f"[{stage}] payload: {len(payload):,} chars", flush=True)
    r = call_model(EVALUATEE_MODEL, INSTRUCTION, payload, SCHEMA,
                   log_dir=cfg.out, log_name=f"call_{stage}",
                   timeout_seconds=3600)
    print(f"[{stage}] ok={r.ok} fail={r.fail_reason} served={r.served_models} "
          f"usage={r.usage} wall={r.wall_seconds}s", flush=True)
    if not r.ok:
        return False
    (cfg.out / f"flags_{stage}.json").write_text(
        json.dumps(r.structured, indent=2) + "\n", encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", required=True, type=Path)
    ap.add_argument("--case-id", required=True)
    ap.add_argument("--docs", type=Path, default=None,
                    help="문서 로스터 매니페스트 (기본: <registry dir>/memo_docs.json)")
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--stage", choices=["annual", "combined", "all"], default="all")
    ap.add_argument("--prior-flags", type=Path, default=None,
                    help="combined의 prior flags 경로 (기본: <out>/flags_annual.json)")
    ap.add_argument("--dry-run", action="store_true",
                    help="페이로드 조립·토큰 추정·컷오프 판정·DRYRUN_MANIFEST 후 무호출 종료")
    args = ap.parse_args()

    docs_manifest = args.docs or (args.registry.parent / "memo_docs.json")
    cfg = MemoConfig(args.registry, args.case_id, docs_manifest, args.out,
                     prior_flags_path=args.prior_flags)
    stages = ["annual", "combined"] if args.stage == "all" else [args.stage]

    if args.dry_run:
        dry_run(cfg, stages)
        return 0
    for s in stages:
        if not run_stage(cfg, s):
            print(f"[{s}] FAILED — stopping", flush=True)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
