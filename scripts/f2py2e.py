from __future__ import annotations

"""
MAGIC Week 0 shim for scripts.f2py2e.

Goal
----
- Make `importlib.import_module("scripts.f2py2e")` safe.
- Provide minimal no-op CLI entry points so that any code
  doing `from scripts import f2py2e; f2py2e.main(...)` does not crash.
- Do NOT parse sys.argv or perform real f2py work at import time.
"""

from typing import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    """
    Week 0 no-op main.

    Returns 0 to indicate "success" without doing anything.
    """
    return 0


def run_main(argv: Sequence[str] | None = None) -> int:
    """
    Week 0 alias for main(), kept for compatibility.
    """
    return main(argv)


if __name__ == "__main__":  # pragma: no cover - direct CLI use
    raise SystemExit(main())
