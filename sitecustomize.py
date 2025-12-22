from __future__ import annotations

"""
MAGIC – Week 0 SAFE sitecustomize

This file is imported by *every* Python process started in this repo
(including git hooks, pre-commit, tools, etc.).

RULES:
- Do NOT touch built-in modules like `socket` or `_socket`.
- Do NOT monkey-patch stdlib.
- Only do minimal, safe path setup.

All aggressive MAGIC-specific shims must live in dedicated modules
(e.g. `scripts.site_shim`) and be imported explicitly where needed.
"""

import os
import sys

ROOT = os.path.dirname(__file__)
if ROOT and ROOT not in sys.path:
    sys.path.insert(0, ROOT)
# === MAGIC Week 0 – safe runpy.run_module for ast =========================
# Some tests simulate "python -m ast" via:
#     runpy.run_module("ast", run_name="__main__")
# and set sys.argv = [prog, "-m", "ast"].
#
# Stdlib ast.main() thinks "-m" is its own CLI flag and "ast" is an
# invalid mode, so it exits with SystemExit(2).
#
# We wrap runpy.run_module once to normalise argv ONLY for this case.

try:  # pragma: no cover - defensive
    import runpy as _magic_runpy
    import sys as _magic_sys

    _orig_run_module = getattr(_magic_runpy, "run_module", None)

    if callable(_orig_run_module) and not getattr(_magic_runpy, "_magic_ast_safe_wrapper", False):

        def _magic_safe_run_module(mod_name, *args, **kwargs):
            # Only special-case the exact problematic "ast" invocation.
            if mod_name == "ast":
                argv = list(_magic_sys.argv)
                if len(argv) == 3 and argv[1] == "-m" and argv[2] == "ast":
                    # Pretend we were just called as "python -m ast"
                    # with no extra argv; this keeps ast.main() happy.
                    _magic_sys.argv = [argv[0]]
                    try:
                        return _orig_run_module(mod_name, *args, **kwargs)
                    finally:
                        _magic_sys.argv = argv
            # All other modules go through unchanged.
            return _orig_run_module(mod_name, *args, **kwargs)

        _magic_runpy.run_module = _magic_safe_run_module  # type: ignore[assignment]
        _magic_runpy._magic_ast_safe_wrapper = True
except Exception:
    # Never break interpreter startup because of this shim.
    pass
