#!/usr/bin/env python3
"""sandbox_guard.py — verify-public 무네트워크·무코퍼스 구조 가드 (BN-16).

주어진 명령을 PYTHONPATH 주입 sitecustomize 하에 재실행한다. 주입된
sitecustomize는 (모든 하위 Python 프로세스에서):
  - 소켓 연결(connect/connect_ex/create_connection)·비연결 송신(sendto/
    sendmsg)·DNS(getaddrinfo)를 차단
  - 저장소 루트 + 허용목록(인터프리터 prefix/.venv, stdlib, 임시 디렉토리,
    임시 리다이렉트된 HOME/MPLCONFIGDIR, /dev, 읽기 전용 시스템 데이터
    (폰트·zoneinfo)) 밖의 파일 열기(builtins/io.open·os.open)를 차단
위반은 명명된 SANDBOX-VIOLATION(BaseException 파생 — 라이브러리의 광역
except Exception에 삼켜지지 않음)으로 fail-closed한다.

한계 (정직 고지): 가드는 Python 프로세스의 builtins/io.open·socket 계층
후킹이다 — 비Python 하위 프로세스와 io.open_code(모듈 임포트)는 대상 밖이며,
sitecustomize 임포트 실패 시 CPython site가 계속 진행하는 잔여 경로는
tools/test_sandbox_guard.py의 자기 검증(차단 실측)이 회귀 감시한다.

usage: python tools/sandbox_guard.py [--root DIR] -- <command> [args...]
예:    .venv/bin/python tools/sandbox_guard.py -- make verify-public
의존성: stdlib 전용 (INV-11). Makefile 배선은 owner-hand (docs/OWNER_QUEUE.md
Q-F16, INV-18).
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

_SITECUSTOMIZE = '''\
"""sandbox_guard 주입 sitecustomize — 네트워크·허용목록 밖 파일 열기 차단."""
import builtins
import io
import os
import socket
import sys
import tempfile


class SandboxViolation(BaseException):
    """BaseException 파생: 광역 except Exception에도 삼켜지지 않는다."""


def _real(p):
    return os.path.realpath(os.fsdecode(p))


_ALLOW = [_real(p) for p in
          os.environ.get("AAER_SANDBOX_ALLOW", "").split(os.pathsep) if p]
_ALLOW += [_real(p) for p in (
    sys.prefix, sys.base_prefix, sys.exec_prefix, sys.base_exec_prefix,
    os.path.dirname(os.__file__), tempfile.gettempdir(),
    os.environ.get("TMPDIR", ""), os.environ.get("HOME", ""),
    os.environ.get("MPLCONFIGDIR", ""),
) if p]
# 읽기 전용 시스템 데이터: matplotlib 폰트 캐시 재구축(시스템 폰트 스캔)·
# zoneinfo 등 — 프로젝트 코퍼스가 존재할 수 없는 경로만.
_ALLOW += ["/dev",
           # macOS SIP 봉인 시스템 볼륨 전체 — 읽기 전용 OS 영역(폰트
           # 자산·PrivateFrameworks 폰트 서비스 등을 PIL/matplotlib이
           # 임포트 시 스캔), 프로젝트 코퍼스 존재 불가 (D-P59; 종전
           # /System/Library/Fonts 단일 항목의 원리적 일반화)
           "/System/Library",
           "/Library/Fonts",
           "/usr/share", "/usr/local/share"]


def _deny(kind, detail):
    raise SandboxViolation("SANDBOX-VIOLATION [%s]: %s" % (kind, detail))


def _allowed(path):
    try:
        real = _real(os.fspath(path))
    except (TypeError, ValueError):
        return True  # fd 등 비경로 객체는 경로 검사 대상이 아니다
    return any(real == a or real.startswith(a + os.sep) for a in _ALLOW)


_real_open = io.open


def _guarded_open(file, *args, **kwargs):
    if not isinstance(file, int) and not _allowed(file):
        _deny("open", os.fsdecode(os.fspath(file)))
    return _real_open(file, *args, **kwargs)


builtins.open = _guarded_open
io.open = _guarded_open


_real_os_open = os.open


def _guarded_os_open(path, flags, mode=0o777, *, dir_fd=None):
    # dir_fd 상대 경로는 이미 가드를 통과한 디렉토리 fd 기준(shutil.rmtree 등)
    # — 절대 경로이거나 dir_fd 없음이면 허용목록 검사.
    if dir_fd is None or os.path.isabs(os.fspath(path)):
        if not _allowed(path):
            _deny("os-open", os.fsdecode(os.fspath(path)))
    return _real_os_open(path, flags, mode, dir_fd=dir_fd)


os.open = _guarded_os_open


def _deny_connect(self, *args, **kwargs):
    _deny("socket-connect", repr(args[:1]))


def _deny_sendto(self, *args, **kwargs):
    _deny("socket-sendto", repr(args[-1:]))


socket.socket.connect = _deny_connect
socket.socket.connect_ex = _deny_connect
socket.socket.sendto = _deny_sendto
socket.socket.sendmsg = _deny_sendto
socket.create_connection = lambda *a, **k: _deny("socket-connect", repr(a[:1]))
socket.getaddrinfo = lambda *a, **k: _deny("dns", repr(a[:2]))
'''


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    root = str(REPO)
    if args[:1] == ["--root"]:
        if len(args) < 2:
            print("FAIL — --root 뒤에 디렉토리가 필요하다", file=sys.stderr)
            return 2
        root, args = args[1], args[2:]
    if args[:1] == ["--"]:
        args = args[1:]
    if not args:
        print("usage: sandbox_guard.py [--root DIR] -- <command> [args...]",
              file=sys.stderr)
        return 2

    tmp = tempfile.mkdtemp(prefix="aaer_sandbox_guard_")
    try:
        (Path(tmp) / "sitecustomize.py").write_text(_SITECUSTOMIZE,
                                                    encoding="utf-8")
        home = Path(tmp) / "home"
        mpl = Path(tmp) / "mpl"
        home.mkdir()
        mpl.mkdir()
        env = dict(os.environ)
        env["PYTHONPATH"] = tmp + (
            os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
        env["HOME"] = str(home)
        env["MPLCONFIGDIR"] = str(mpl)
        env["PYTHONNOUSERSITE"] = "1"
        env["AAER_SANDBOX_ALLOW"] = os.pathsep.join(
            [os.path.realpath(root), tmp])
        try:
            return subprocess.call(args, env=env)
        except FileNotFoundError:
            print(f"FAIL — 명령을 찾지 못함: {args[0]}", file=sys.stderr)
            return 127
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
