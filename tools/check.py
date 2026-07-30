
from __future__ import annotations

from pathlib import Path


REQUIRED_PATHS = [
    Path("AGENTS.md"),
    Path("PROJECT.md"),
    Path("QUALITY_GATE.md"),
    Path("docs/architecture"),
    Path("docs/requirements"),
    Path("docs/development"),
    Path("docs/exec-plans/active"),
    Path("firmware"),
    Path("pc_tool"),
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
