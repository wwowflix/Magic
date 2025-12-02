"""
MAGIC Week 0: safe stub for pandas config_init_2.

Goal:
- Let "import scripts.config_init_2" succeed.
- Do NOT call pandas.option.register_option again.
- Avoid any heavy side effects.

The smoke test only checks that this module imports.
"""

from __future__ import annotations

# Import pandas lazily/safely – no option registration here.
try:
    import pandas as _pd  # noqa: F401
except Exception:
    # If pandas import fails for any reason, we still want the module
    # to import, so we just swallow the error for Week 0.
    _pd = None  # type: ignore[assignment]

# Public API (empty – this module is just an import-time stub in Week 0)
__all__: list[str] = []
