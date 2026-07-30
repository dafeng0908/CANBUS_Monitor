
from __future__ import annotations

import shutil
import sys


def run() -> int:
    failed = False

    print(f"[PASS] Python {sys.version.split()[0]}")

    git_path = shutil.which("git")
    if git_path is None:
        print("[FAIL] Git not found")
        failed = True
    else:
        print(f"[PASS] Git: {git_path}")

    cppcheck_path = shutil.which("cppcheck")
    if cppcheck_path is None:
        print("[WARN] Cppcheck not found")
    else:
        print(f"[PASS] Cppcheck: {cppcheck_path}")

    ceedling_path = shutil.which("ceedling")
    if ceedling_path is None:
        print("[WARN] Ceedling not found")
    else:
        print(f"[PASS] Ceedling: {ceedling_path}")

    return 1 if failed else 0
