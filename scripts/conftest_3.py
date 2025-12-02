from __future__ import annotations

"""
MAGIC – Week 0 fsspec test conftest shim (conftest_3).

Goal
----
- Let `import scripts.conftest_3` succeed during global smoke tests.
- Avoid importing heavy / missing deps like `fsspec.implementations`.
- This file is ONLY for vendored tests, not core MAGIC runtime.

The original vendored module has been moved to:
    conftest_3.py.magic_bak_week0
"""

# No-op placeholders; we don't expose any real fixtures here.
__all__: list[str] = []
