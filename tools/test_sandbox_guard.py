"""tools/sandbox_guard.py 자기 검증 (BN-16). 네트워크 0 — 위반 시도는
가드가 연결·열기 전에 차단함을 실측한다 (차단 실패 시 여기서 깨진다)."""
import subprocess
import sys
from pathlib import Path

GUARD = Path(__file__).resolve().parent / "sandbox_guard.py"
REPO = Path(__file__).resolve().parents[1]


def run_guarded(code):
    return subprocess.run(
        [sys.executable, str(GUARD), "--", sys.executable, "-c", code],
        capture_output=True, text=True, cwd=str(REPO), timeout=120)


def test_socket_connect_blocked():
    r = run_guarded(
        "import socket; socket.create_connection(('127.0.0.1', 9), timeout=1)")
    assert r.returncode != 0
    assert "SANDBOX-VIOLATION" in r.stderr and "socket" in r.stderr


def test_udp_sendto_blocked():
    r = run_guarded(
        "import socket; socket.socket(socket.AF_INET, socket.SOCK_DGRAM)"
        ".sendto(b'x', ('127.0.0.1', 9))")
    assert r.returncode != 0
    assert "SANDBOX-VIOLATION" in r.stderr and "sendto" in r.stderr


def test_out_of_repo_read_blocked():
    r = run_guarded("open('/etc/hosts').read()")
    assert r.returncode != 0
    assert "SANDBOX-VIOLATION" in r.stderr and "open" in r.stderr


def test_os_open_out_of_repo_blocked():
    r = run_guarded("import os; os.open('/etc/hosts', os.O_RDONLY)")
    assert r.returncode != 0
    assert "SANDBOX-VIOLATION" in r.stderr and "os-open" in r.stderr


def test_in_repo_read_allowed():
    r = run_guarded(
        "open('README.md', encoding='utf-8').read(64); print('IN-REPO-OK')")
    assert r.returncode == 0, r.stderr
    assert "IN-REPO-OK" in r.stdout


def test_exit_code_propagated():
    r = run_guarded("import sys; sys.exit(7)")
    assert r.returncode == 7
