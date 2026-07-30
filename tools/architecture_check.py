
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
FIRMWARE_ROOT = REPO_ROOT / "firmware"

FORBIDDEN_RULES = {
    "App": ["HAL_", "stm32c5xx_hal.h", "FDCAN_HandleTypeDef"],
    "Services": ["HAL_", "stm32c5xx_hal.h", "FDCAN_HandleTypeDef"],
}

ISR_FORBIDDEN = ["printf(", "malloc(", "calloc(", "vTaskDelay("]


def run() -> int:
    failed = False

    for layer, tokens in FORBIDDEN_RULES.items():
        layer_root = FIRMWARE_ROOT / layer
        if not layer_root.exists():
            continue

        for file_path in layer_root.rglob("*.[ch]"):
            text = file_path.read_text(encoding="utf-8", errors="ignore")

            for token in tokens:
                if token in text:
                    relative = file_path.relative_to(REPO_ROOT)
                    print(f"[FAIL] {relative}: forbidden token '{token}'")
                    failed = True

    return 1 if failed else 0
