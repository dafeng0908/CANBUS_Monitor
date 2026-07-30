from __future__ import annotations

import argparse
import sys
from collections.abc import Callable

from tools.build import run as run_build
from tools.check import run as run_check
from tools.doctor import run as run_doctor


CommandFunction = Callable[[], int]


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CANBUS Monitor development harness"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    subparsers.add_parser(
        "doctor",
        help="Check the local development environment",
    )
    subparsers.add_parser(
        "check",
        help="Run repository and architecture checks",
    )
    subparsers.add_parser(
        "build",
        help="Build the firmware and PC tool",
    )

    return parser


def main() -> int:
    parser = create_parser()
    args = parser.parse_args()

    commands: dict[str, CommandFunction] = {
        "doctor": run_doctor,
        "check": run_check,
        "build": run_build,
    }

    command = commands.get(args.command)
    if command is None:
        parser.error(f"Unsupported command: {args.command}")
        return 2

    return command()


if __name__ == "__main__":
    sys.exit(main())
