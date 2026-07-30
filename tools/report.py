
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tools.common import (
    LATEST_REPORT_DIR,
    current_timestamp,
    ensure_report_directories,
    get_git_commit,
)
from tools.result import CheckResult, overall_status


def write_json_report(
    *,
    report_name: str,
    command: str,
    exit_code: int,
    results: list[CheckResult],
) -> Path:
    """
    寫入 JSON 檢查報告。
    """
    ensure_report_directories()

    report_path = LATEST_REPORT_DIR / f"{report_name}.json"

    payload: dict[str, Any] = {
        "report_name": report_name,
        "command": command,
        "timestamp": current_timestamp(),
        "git_commit": get_git_commit(),
        "status": overall_status(results).value,
        "exit_code": exit_code,
        "results": [result.to_dict() for result in results],
    }

    report_path.write_text(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    return report_path


def write_markdown_report(
    *,
    report_name: str,
    command: str,
    exit_code: int,
    results: list[CheckResult],
) -> Path:
    """
    寫入方便人工閱讀的 Markdown 報告。
    """
    ensure_report_directories()

    report_path = LATEST_REPORT_DIR / f"{report_name}.md"
    status = overall_status(results)

    lines = [
        f"# {report_name.replace('_', ' ').title()}",
        "",
        f"- Command: `{command}`",
        f"- Timestamp: `{current_timestamp()}`",
        f"- Git commit: `{get_git_commit()}`",
        f"- Exit code: `{exit_code}`",
        f"- Overall status: **{status.value}**",
        "",
        "## Results",
        "",
        "| Status | Required | Check | Location | Message |",
        "|---|---:|---|---|---|",
    ]

    for result in results:
        location = result.file or ""

        if result.file and result.line is not None:
            location = f"{result.file}:{result.line}"

        message = result.message.replace("|", "\\|")

        lines.append(
            "| "
            f"{result.status.value} | "
            f"{'Yes' if result.required else 'No'} | "
            f"{result.name} | "
            f"{location} | "
            f"{message} |"
        )

    report_path.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    return report_path


def write_reports(
    *,
    report_name: str,
    command: str,
    exit_code: int,
    results: list[CheckResult],
) -> tuple[Path, Path]:
    """
    同時輸出 JSON 與 Markdown 報告。
    """
    json_path = write_json_report(
        report_name=report_name,
        command=command,
        exit_code=exit_code,
        results=results,
    )

    markdown_path = write_markdown_report(
        report_name=report_name,
        command=command,
        exit_code=exit_code,
        results=results,
    )

    return json_path, markdown_path
