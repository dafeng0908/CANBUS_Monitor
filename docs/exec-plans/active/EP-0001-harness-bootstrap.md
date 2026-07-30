# EP-0001 Harness Bootstrap

## Objective

Establish the minimum executable development harness.

## Scope

- Normalize docs directory
- Implement tools.py
- Add project definition
- Add quality gate
- Add architecture checker skeleton
- Add initial CI workflow

## Acceptance Criteria

- `python tools\tools.py doctor` executes
- `python tools\tools.py check` executes
- Missing external tools are reported
- No command reports a false PASS
- AGENTS.md links resolve
- CI invokes the same local commands

## Out of Scope

- FDCAN implementation
- FreeRTOS tasks
- Python Qt6 GUI
