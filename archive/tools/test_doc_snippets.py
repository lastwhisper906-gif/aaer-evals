"""R2-19: 발행 문서의 재현 스니펫이 커밋 트리에서 실제로 실행된다.

원 결함: EVIDENCE_LINES §4 스니펫의 glob이 MANIFEST.json(케이스 아님)을
집어 case_id KeyError — 발행된 검증 명령이 복제자에게서 즉사했다 (수치
자체는 원 기재 시점에 검증 완료). 문서에서 코드를 추출해 exec한다 —
문서와 테스트가 어긋나면 red (스니펫 사본 드리프트 없음).
"""
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_evidence_lines_section4_snippet_runs_green():
    text = (REPO / "analysis/EVIDENCE_LINES.md").read_text(encoding="utf-8")
    m = re.search(r"## 4\. 재현 경로\n\n```\npython3 - <<'PY'\n(.*?)\nPY\n```",
                  text, re.DOTALL)
    assert m, "EVIDENCE_LINES §4 스니펫 블록을 찾지 못함 — 형식 드리프트"
    result = subprocess.run([sys.executable, "-c", m.group(1)], cwd=REPO,
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr[-500:]
    assert "Counter" in result.stdout  # freq 출력 도달 = 전 파일 파싱 성공
