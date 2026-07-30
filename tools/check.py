from tools.architecture_check import run as run_architecture_check
from __future__ import annotations
 
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "docs/architecture",
    "docs/requirements",
    "docs/development/coding_style.md",
]

REQUIRED_COMMANDS = [
    ["python", "tools.py", "doctor"],
    ["python", "tools.py", "check"],
    ["python", "tools.py", "build"],
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
