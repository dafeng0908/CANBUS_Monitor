from __future__ import annotations

import re
import sys
from pathlib import Path

from tools.architecture_check import collect_results as collect_architecture_results
from tools.common import REPO_ROOT, relative_to_repo, run_command
from tools.report_generator import write_reports
from tools.result import (
    CheckResult,
    Status,
    has_required_failure,
    print_results,
)


REQUIRED_PATHS = [
    Path("AGENTS.md"),
    Path("PROJECT.md"),
    Path("QUALITY_GATE.md"),
    Path("tools.py"),
    Path("docs/architecture"),
    Path("docs/requirements"),
    Path("docs/development/coding_style.md"),
    Path("docs/exec-plans/active"),
    Path("docs/exec-plans/completed"),
    Path("firmware"),
    Path("pc_tool"),
    Path("tools"),
]

ACTIVE_PLAN_ROOT = REPO_ROOT / "docs/exec-plans/active"

ACTIVE_PLAN_REQUIRED_SECTIONS = [
    "Objective",
    "Scope",
    "Acceptance Criteria",
    "Verification Evidence",
    "Out of Scope",
]

AGENTS_FILE = REPO_ROOT / "AGENTS.md"

AGENT_COMMAND_PATTERN = re.compile(
    r"^\s*(?:python|python3|py)\s+tools\.py\s+([A-Za-z0-9_-]+)\s*$"
)


def check_required_paths() -> list[CheckResult]:
    """
    檢查 Repository contract 所需路徑。
    """
    results: list[CheckResult] = []

    for relative_path in REQUIRED_PATHS:
        full_path = REPO_ROOT / relative_path

        if full_path.exists():
            results.append(
                CheckResult(
                    name="repository-path",
                    status=Status.PASS,
                    message="Required path exists.",
                    file=relative_path.as_posix(),
                )
            )
        else:
            results.append(
                CheckResult(
                    name="repository-path",
                    status=Status.FAIL,
                    message="Required path is missing.",
                    file=relative_path.as_posix(),
                )
            )

    return results


def find_active_plans() -> list[Path]:
    """
    找出 active 目錄中的 Exec Plan。

    README.md 與隱藏檔不視為 Active Plan。
    """
    if not ACTIVE_PLAN_ROOT.exists():
        return []

    return sorted(
        path
        for path in ACTIVE_PLAN_ROOT.glob("*.md")
        if path.name.lower() != "readme.md"
        and not path.name.startswith(".")
    )


def check_active_plan_count() -> tuple[list[CheckResult], Path | None]:
    """
    Active Plan 必須剛好一份。
    """
    plans = find_active_plans()

    if len(plans) == 0:
        return (
            [
                CheckResult(
                    name="active-plan-count",
                    status=Status.FAIL,
                    message="No active execution plan was found.",
                    file=relative_to_repo(ACTIVE_PLAN_ROOT),
                )
            ],
            None,
        )

    if len(plans) > 1:
        plan_names = ", ".join(
            relative_to_repo(path)
            for path in plans
        )

        return (
            [
                CheckResult(
                    name="active-plan-count",
                    status=Status.FAIL,
                    message=(
                        "Exactly one active execution plan is required. "
                        f"Found {len(plans)}: {plan_names}"
                    ),
                    file=relative_to_repo(ACTIVE_PLAN_ROOT),
                )
            ],
            None,
        )

    return (
        [
            CheckResult(
                name="active-plan-count",
                status=Status.PASS,
                message="Exactly one active execution plan exists.",
                file=relative_to_repo(plans[0]),
            )
        ],
        plans[0],
    )


def extract_markdown_headings(text: str) -> set[str]:
    """
    取得 Markdown 標題文字，忽略大小寫。
    """
    headings: set[str] = set()

    for line in text.splitlines():
        match = re.match(r"^\s*#{1,6}\s+(.+?)\s*$", line)

        if match:
            headings.add(match.group(1).strip().casefold())

    return headings


def check_active_plan_sections(
    active_plan: Path | None,
) -> list[CheckResult]:
    """
    檢查 Active Plan 必要章節。
    """
    if active_plan is None:
        return []

    try:
        text = active_plan.read_text(
            encoding="utf-8",
            errors="replace",
        )
    except OSError as exc:
        return [
            CheckResult(
                name="active-plan-read",
                status=Status.FAIL,
                message=f"Unable to read active plan: {exc}",
                file=relative_to_repo(active_plan),
            )
        ]

    headings = extract_markdown_headings(text)
    results: list[CheckResult] = []

    for section in ACTIVE_PLAN_REQUIRED_SECTIONS:
        if section.casefold() in headings:
            results.append(
                CheckResult(
                    name="active-plan-section",
                    status=Status.PASS,
                    message=f"Required section exists: {section}",
                    file=relative_to_repo(active_plan),
                )
            )
        else:
            results.append(
                CheckResult(
                    name="active-plan-section",
                    status=Status.FAIL,
                    message=f"Missing required section: {section}",
                    file=relative_to_repo(active_plan),
                )
            )

    return results


def read_agent_commands() -> tuple[list[str], list[CheckResult]]:
    """
    從 AGENTS.md 讀取 `python tools.py <command>`。
    """
    if not AGENTS_FILE.exists():
        return (
            [],
            [
                CheckResult(
                    name="agents-command-read",
                    status=Status.FAIL,
                    message="AGENTS.md does not exist.",
                    file="AGENTS.md",
                )
            ],
        )

    try:
        text = AGENTS_FILE.read_text(
            encoding="utf-8",
            errors="replace",
        )
    except OSError as exc:
        return (
            [],
            [
                CheckResult(
                    name="agents-command-read",
                    status=Status.FAIL,
                    message=f"Unable to read AGENTS.md: {exc}",
                    file="AGENTS.md",
                )
            ],
        )

    commands: list[str] = []

    for line in text.splitlines():
        match = AGENT_COMMAND_PATTERN.match(line)

        if match:
            commands.append(match.group(1))

    if not commands:
        return (
            [],
            [
                CheckResult(
                    name="agents-command-read",
                    status=Status.FAIL,
                    message="No Harness command found in AGENTS.md.",
                    file="AGENTS.md",
                )
            ],
        )

    return (
        commands,
        [
            CheckResult(
                name="agents-command-read",
                status=Status.PASS,
                message=f"Found {len(commands)} Harness commands.",
                file="AGENTS.md",
            )
        ],
    )


def check_cli_commands(commands: list[str]) -> list[CheckResult]:
    """
    驗證 AGENTS.md 宣告的 CLI command 可以由 argparse 解析。

    使用 --help，避免真正執行 build、flash 或其他動作。
    """
    results: list[CheckResult] = []

    for command_name in commands:
        command = [
            sys.executable,
            "tools.py",
            command_name,
            "--help",
        ]

        process = run_command(
            command,
            cwd=REPO_ROOT,
            timeout_seconds=30,
        )

        display_command = (
            f"python tools.py {command_name} --help"
        )

        if process.returncode == 0:
            results.append(
                CheckResult(
                    name="agents-cli-command",
                    status=Status.PASS,
                    message=f"CLI command is valid: {display_command}",
                    file="AGENTS.md",
                )
            )
        else:
            error_message = (
                process.stderr.strip()
                or process.stdout.strip()
                or f"Exit code {process.returncode}"
            )

            results.append(
                CheckResult(
                    name="agents-cli-command",
                    status=Status.FAIL,
                    message=(
                        f"Invalid CLI command: {display_command}. "
                        f"{error_message}"
                    ),
                    file="AGENTS.md",
                )
            )

    return results


def collect_results() -> list[CheckResult]:
    """
    收集完整 Repository 與 Architecture 檢查結果。
    """
    results: list[CheckResult] = []

    results.extend(check_required_paths())

    plan_results, active_plan = check_active_plan_count()
    results.extend(plan_results)
    results.extend(check_active_plan_sections(active_plan))

    agent_commands, command_read_results = read_agent_commands()
    results.extend(command_read_results)
    results.extend(check_cli_commands(agent_commands))

    results.extend(collect_architecture_results())

    return results


def run() -> int:
    """
    執行 Repository Contract、Active Plan 與架構檢查。
    """
    results = collect_results()
    exit_code = 1 if has_required_failure(results) else 0

    print_results(results)

    json_path, markdown_path = write_reports(
        report_name="check",
        command="python tools.py check",
        exit_code=exit_code,
        results=results,
    )

    print(f"[INFO] JSON report: {json_path}")
    print(f"[INFO] Markdown report: {markdown_path}")

    return exit_code
