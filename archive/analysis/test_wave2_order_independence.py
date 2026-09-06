"""R2-21: wave-2 분석기 적재는 파일시스템 나열 순서와 무관해야 한다 (INV-02).

MC 값(perm_p·boot CI)은 입력 나열 순서에 민감하다 — _case_files의 정렬이
빠지면 게시 수치의 끝자리가 ext4/APFS 열거 순서에 종속된다. 여기서는 glob
열거를 역순으로 뒤집어도 적재 산출(값과 순서 모두)이 동일함을 잠근다;
하류 계산은 시드 고정 결정론이므로 적재 동일성 = 결과 동일성이다.
동결 rev2 수치 자체는 정렬 도입 이전(파일시스템 순서)에 생성됐다 —
ERRATA의 E-002 재현 주의 노트와 tools/test_recompute_published.py 헤더가
그 허용오차를 문서화한다.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wave2_analyze as w2


def test_reversed_glob_enumeration_loads_identically(monkeypatch):
    normal_w2 = w2.load_scores("runs/wave2/scores", "scoring/id_mapping_wave2.json")
    normal_pert = w2.load_scores("runs/wave2/perturbed", "scoring/id_mapping_wave2.json")
    normal_w1 = w2.load_wave1_scores()

    real_glob = w2.glob.glob
    monkeypatch.setattr(w2.glob, "glob",
                        lambda pattern: list(reversed(real_glob(pattern))))
    rev_w2 = w2.load_scores("runs/wave2/scores", "scoring/id_mapping_wave2.json")
    rev_pert = w2.load_scores("runs/wave2/perturbed", "scoring/id_mapping_wave2.json")
    rev_w1 = w2.load_wave1_scores()

    # dict 삽입 순서까지 동일해야 rng 소비 순서가 동일하다
    assert list(normal_w2.items()) == list(rev_w2.items())
    assert list(normal_pert.items()) == list(rev_pert.items())
    assert normal_w1 == rev_w1
