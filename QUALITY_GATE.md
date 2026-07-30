# Quality Gate

## Stage 0

- [ ] `python tools.py doctor` executes
- [ ] `python tools.py check` executes
- [ ] Required repository paths exist
- [ ] No command reports false PASS
- [ ] AGENTS.md commands are valid
- [ ] CI runs the same local commands

## Stage 1 Firmware

- [ ] Firmware build returns exit code 0
- [ ] Cppcheck unsuppressed errors = 0
- [ ] Ceedling tests pass
- [ ] Line coverage >= 80%
- [ ] Critical modules coverage >= 90%
- [ ] Architecture violations = 0

## Evidence

Every PASS result must include:

- Command executed
- Timestamp
- Tool version
- Exit code
- Report path
