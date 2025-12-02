from __future__ import annotations

"""
MAGIC – Week 0 AST shim (scripts.ast).

Goal
----
- Let `import scripts.ast` succeed during smoke tests.
- Avoid triggering the stdlib `ast` CLI argument parsing that chokes on
  the "-m ast" pattern.
- Reuse the real stdlib `ast` module for all AST APIs.
"""

import ast as _stdlib_ast

# Re-export everything public from the stdlib ast module, so callers that
# expect ast.parse / ast.AST / etc. still work.
from ast import *  # type: ignore[misc]  # noqa: F401,F403


def main() -> None:
    """
    Safe entry point for Week 0.

    We only delegate to stdlib ast.main() if it exists, and we never call
    this automatically at import time. Tests that run this module with
    runpy will not see the bad "-m ast" argv combination anymore.
    """
    if hasattr(_stdlib_ast, "main"):
        return _stdlib_ast.main()
    return None


__all__ = list(getattr(_stdlib_ast, "__all__", []))
if "main" not in __all__:
    __all__.append("main")
