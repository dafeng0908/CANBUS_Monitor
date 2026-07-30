from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class Status(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"
    SKIP = "SKIP"


@dataclass(frozen=True)
class CheckResult:
    """
    單一 Harness 檢查結果。
    """

    name: str
    status: Status
    message: str
    required: bool = True
    file: str | None = None
    line: int | None = None

    def to_dict(self) -> dict[str, Any]:
        """
        將結果轉成可寫入 JSON 的 dict。
        """
        data = asdict(self)
        data["status"] = self.status.value
        return data


def has_required_failure(results: list[CheckResult]) -> bool:
    """
    判斷是否存在 Required FAIL。
    """
    return any(
        result.required and result.status == Status.FAIL
        for result in results
    )


def overall_status(results: list[CheckResult]) -> Status:
    """
    計算整體狀態。
    """
    if has_required_failure(results):
        return Status.FAIL

    if any(result.status == Status.WARN for result in results):
        return Status.WARN

    if results and all(result.status == Status.SKIP for result in results):
        return Status.SKIP

    return Status.PASS


def print_results(results: list[CheckResult]) -> None:
    """
    以統一格式輸出結果。
    """
    for result in results:
        location = ""

        if result.file:
            location = f" {result.file}"
            if result.line is not None:
                location += f":{result.line}"

        required_text = "" if result.required else " [optional]"

        print(
            f"[{result.status.value}] "
            f"{result.name}{required_text}{location}: "
            f"{result.message}"
        )
