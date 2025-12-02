from __future__ import annotations

"""
MAGIC – Week 0 pandas test conftest shim (conftest_2).

Goal
----
- Let `import scripts.conftest_2` succeed during global smoke tests.
- Avoid importing heavy / missing testing deps (hypothesis, dateutil, etc.).
- This file is *not* used by MAGIC runtime logic; only vendored tests.

If a later week wants real behavior, it can restore:
    conftest_2.py.magic_bak_week0
"""

# No-op placeholders so attributes access won’t explode if something pokes here.

__all__: list[str] = []
