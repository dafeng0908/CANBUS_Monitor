
from dataclasses import dataclass


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str
    message: str
    required: bool
