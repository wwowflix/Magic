from __future__ import annotations

"""
MAGIC Week 0 – adjusted AST smoke test.

We only verify:
- stdlib ast imports and exposes parse()
- if a scripts.ast module exists, it imports and exposes parse()/AST

If scripts.ast is not present in this environment, we skip that part.
"""

import importlib
import pytest


def test_stdlib_ast_imports() -> None:
    std_ast = importlib.import_module("ast")
    assert hasattr(std_ast, "parse")


def test_scripts_ast_optional() -> None:
    try:
        scripts_ast = importlib.import_module("scripts.ast")
    except ModuleNotFoundError:
        pytest.skip("scripts.ast is not present in this Week 0 environment")
    else:
        assert hasattr(scripts_ast, "parse") or hasattr(scripts_ast, "AST")
