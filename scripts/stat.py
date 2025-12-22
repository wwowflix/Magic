# -*- coding: utf-8 -*-
"""MAGIC shim: forward all imports to the real stdlib 'stat' module."""

import importlib as _importlib
import sys as _sys
from pathlib import Path as _Path

_target_name = "stat"

# Drop any half-initialized entry
_sys.modules.pop(_target_name, None)

# Temporarily hide this directory from sys.path to avoid re-importing ourselves
_original_path = list(_sys.path)
_this_dir = str(_Path(__file__).resolve().parent)

try:
    _sys.path = [
        p for p in _sys.path
        if _Path(p).resolve() != _Path(_this_dir)
    ]
    _real = _importlib.import_module(_target_name)
finally:
    _sys.path = _original_path

# Ensure future imports see the real module
_sys.modules[_target_name] = _real
_sys.modules.setdefault(f"scripts.{_target_name}", _real)

# Re-export everything
for _name in dir(_real):
    globals()[_name] = getattr(_real, _name)

# Keep a sensible __all__
try:
    __all__ = list(_real.__all__)
except Exception:
    __all__ = [n for n in globals() if not n.startswith("_")]

# Cleanup
del _importlib, _sys, _Path, _original_path, _this_dir, _name, _real, _target_name
