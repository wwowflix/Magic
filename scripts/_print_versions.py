"""MAGIC shim for SciPy-style _print_versions helper.

Real implementation prints dependency versions. For MAGIC we just need
a callable `main()` that does not crash when invoked.
"""

from __future__ import annotations


def main() -> None:
    """Best-effort no-op used by MAGIC smoke tests."""
    return None
