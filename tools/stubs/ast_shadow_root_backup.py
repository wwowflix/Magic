from __future__ import annotations

"""
MAGIC – Week 0 top-level AST shim.

Goal
----
- Shadow the stdlib "ast" module INSIDE the MAGIC repo so that tests
  using runpy.run_module("ast", run_name="__main__") do not trip over
  the stdlib CLI "-m/--mode" parsing.
- Re-export all normal ast APIs (parse, AST, etc.) from the real stdlib.
"""

import importlib
import os as _os
import sys as _sys

# 1) Import the real stdlib ast safely, avoiding recursive import of THIS file.
_ROOT = _os.path.dirname(__file__)
_removed = False
if _ROOT in _sys.path:
    _sys.path.remove(_ROOT)
    _removed = True
try:
    _stdlib_ast = importlib.import_module("ast")
finally:
    if _removed:
        _sys.path.insert(0, _ROOT)

# 2) Re-export all public names from the real ast module.
__all__ = list(getattr(_stdlib_ast, "__all__", []))

for _name in __all__:
    globals()[_name] = getattr(_stdlib_ast, _name)


def main() -> None:
    """
    Safe entry point for Week 0.

    If argv looks like ["prog", "-m", "ast"], we normalise it to ["prog"]
    before delegating to the real ast.main(), so argparse does not treat
    "ast" as a bad value for -m/--mode.
    """
    real_main = getattr(_stdlib_ast, "main", None)
    if real_main is None:
        return None

    argv = list(_sys.argv)
    if len(argv) == 3 and argv[1] == "-m" and argv[2] == "ast":
        _sys.argv = [argv[0]]
        try:
            return real_main()
        finally:
            _sys.argv = argv
    else:
        return real_main()


if "main" not in __all__:
    __all__.append("main")
