import argparse
import sys


def command_doctor() -> int:
    print("[DOCTOR] NOT IMPLEMENTED")
    return 2


def command_check() -> int:
    print("[CHECK] NOT IMPLEMENTED")
    return 2


def command_build() -> int:
    print("[BUILD] NOT IMPLEMENTED")
    return 2


def main() -> int:
    parser = argparse.ArgumentParser(
        description="CANBUS Monitor development harness"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("doctor")
    subparsers.add_parser("check")
    subparsers.add_parser("build")

    args = parser.parse_args()

    commands = {
        "doctor": command_doctor,
        "check": command_check,
        "build": command_build,
    }

    return commands[args.command]()


if __name__ == "__main__":
    sys.exit(main())
