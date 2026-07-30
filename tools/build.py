from __future__ import annotations

from tools.report_generator import write_reports
from tools.result import CheckResult, Status, print_results


def run() -> int:
    """
    Firmware build 尚未實作。

    回傳 2，表示功能尚未建立，不可視為 PASS。
    """
    results = [
        CheckResult(
            name="firmware-build",
            status=Status.SKIP,
            message=(
                "Firmware build is not implemented. "
                "STM32CubeIDE project has not been integrated."
            ),
            required=True,
        )
    ]

    exit_code = 2

    print_results(results)

    json_path, markdown_path = write_reports(
        report_name="build",
        command="python tools.py build",
        exit_code=exit_code,
        results=results,
    )

    print(f"[INFO] JSON report: {json_path}")
    print(f"[INFO] Markdown report: {markdown_path}")

    return exit_code
