
from __future__ import annotations
 
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    REPO_ROOT / "AGENTS.md",
    REPO_ROOT / "PROJECT.md",
]


def run() -> int:
    failed = False

    for path in REQUIRED_PATHS:
        if path.exists():
            print(f"[PASS] {path}")
        else:
            print(f"[FAIL] Missing: {path}")
            failed = True

    return 1 if failed else 0
