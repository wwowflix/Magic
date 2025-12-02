from __future__ import annotations

"""
MAGIC shim for scripts.browser_test.

The original module used Playwright and greenlet to run real browser tests.
For MAGIC Week 0 we only need:

- the module to import cleanly
- a couple of no-op helpers that *look* like a test runner
- absolutely no dependency on playwright / greenlet at import time
"""

from dataclasses import dataclass
from typing import List


@dataclass
class BrowserTestResult:
    name: str
    passed: bool
    details: str = ""


def run_all_tests() -> List[BrowserTestResult]:
    """
    Return an empty list of browser test results.

    In a future phase you could integrate real Playwright tests here, but for
    Week 0 we keep this as a harmless no-op.
    """
    return []


def main() -> int:
    """
    Optional entrypoint-style helper.

    Prints any test results if present. In this shim, the list is empty.
    """
    for result in run_all_tests():
        status = "PASS" if result.passed else "FAIL"
        print(f"[{status}] {result.name} {result.details}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
