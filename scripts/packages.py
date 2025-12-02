"""
MAGIC Week 0 – shim for `scripts.packages`

Goal:
- Make vendored imports like:
    from scripts.packages import six
    from scripts.packages.six.moves import queue
  work without pulling any real network logic.

We simply delegate to the real `six` from site-packages if available,
and register an alias module `scripts.packages.six`.
"""

from __future__ import annotations

import sys
import types

try:
    import six as _real_six  # type: ignore[import]
except Exception:
    # Minimal fallback if `six` isn't installed (enough for our imports).
    class _MiniSix(types.SimpleNamespace):  # type: ignore[misc]
        PY2 = False
        PY3 = True

    _real_six = _MiniSix()  # type: ignore[assignment]

# Expose as attribute on this module
six = _real_six

# Also register `scripts.packages.six` as a real module in sys.modules
_module_name = __name__ + ".six"  # "scripts.packages.six"

if _module_name not in sys.modules:
    six_module = types.ModuleType(_module_name)
    for _name in dir(_real_six):
        try:
            setattr(six_module, _name, getattr(_real_six, _name))
        except Exception:
            # Best-effort copy; we only really care about `.moves`
            pass
    sys.modules[_module_name] = six_module

__all__ = ["six"]
