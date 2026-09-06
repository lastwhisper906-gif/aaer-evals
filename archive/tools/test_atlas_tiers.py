"""R9-1: atlas 지위 라벨 ↔ 후보 레지스트리 정합.

"vs SEC AAER ground truth" 표제가 저장소 자신의 도시에(dossier)와 모순되면
안 된다 — `aaer_no: null`(서명된 GP-4 ② — SEC 집행 확인·AAER 부재)인
케이스에 `AAER-confirmed` 라벨을 붙인 파일이 있으면 red.
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCORING_ID = re.compile(r"scoring ID ([A-Z]+\d+)")
TIER_ROW = re.compile(r"^\| Ground-truth tier \|(.+)\|", re.MULTILINE)


def _aaer_by_case_id() -> dict:
    out = {}
    for rel in ("data/candidates/candidates.json",
                "data/candidates/candidates_wave2.json"):
        for c in json.loads((REPO / rel).read_text(encoding="utf-8"))["candidates"]:
            out.setdefault(c["case_id"], c.get("aaer_no"))
    return out


def test_no_atlas_file_asserts_aaer_confirmed_for_null_aaer_case():
    aaer = _aaer_by_case_id()
    offenders = []
    for path in sorted((REPO / "atlas").glob("case_*.md")):
        text = path.read_text(encoding="utf-8")
        tier = TIER_ROW.search(text)
        sid = SCORING_ID.search(text)
        if not tier or "AAER-confirmed" not in tier.group(1):
            continue
        if sid and sid.group(1) in aaer and not aaer[sid.group(1)]:
            offenders.append(f"{path.name} ({sid.group(1)}: aaer_no null)")
    assert not offenders, (
        f"AAER-confirmed 라벨인데 후보 레코드 aaer_no가 null: {offenders} — "
        "GP-4 ② 어휘('SEC-enforcement-confirmed, no AAER')를 쓸 것 (R9-1)")
