from __future__ import annotations

"""
MAGIC Week 0 shim for the third-party `py` package.

Why:
- Your project has `scripts/py.py`, which shadows the real `py` package
  that pytest and its compat layer expect.
- This shim finds the real `py` package in site-packages (excluding the
  `scripts/` directory) and re-exports all of its public attributes.

Result:
- `import py` and any code using pytest internals see exactly the real
  package API, not this shim's file-level implementation.
"""

from types import ModuleType
import importlib.util
import importlib.machinery
import importlib.machinery
import os as _os
import sys as _sys


# Directory of this shim (E:\MAGIC\scripts)
_here = _os.path.dirname(__file__)

# Build a search path that excludes the scripts directory, so that
# PathFinder finds the real site-packages `py` instead of this file.
_search_paths = [
    p
    for p in _sys.path
    if _os.path.abspath(p) != _os.path.abspath(_here)
]

_spec = importlib.machinery.PathFinder.find_spec("py", _search_paths)
if _spec is None or _spec.loader is None:
    raise ImportError("Cannot locate real third-party 'py' package outside scripts/")

_real = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_real)  # type: ignore[arg-type]

# Re-export everything public from the real package into this module.
for name in dir(_real):
    if not name.startswith("_"):
        globals()[name] = getattr(_real, name)

# Also expose the real module object if needed.
_real_py: ModuleType = _real

__all__ = [name for name in globals() if not name.startswith("_")]
