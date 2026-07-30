from __future__ import annotations

from pathlib import Path

from tools.architecture_check import run as run_architecture_check

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    Path("docs/architecture"),
    Path("docs/requirements"),
    Path("docs/development/coding_style.md"),
]

def run() -> int:
    failed = False

    for relative_path in REQUIRED_PATHS:
        full_path = REPO_ROOT / relative_path
        if full_path.exists():
            print(f"[PASS] {relative_path}")
        else:
            print(f"[FAIL] Missing: {relative_path}")
            failed = True

    if run_architecture_check() != 0:
        failed = True

    return 1 if failed else 0
