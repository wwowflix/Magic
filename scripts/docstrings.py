"""
MAGIC Week 0: stub for scripts.docstrings.

Goal:
- Let "import scripts.docstrings" succeed.
- Provide simple factories for docstrings but avoid heavy templates.
"""

from __future__ import annotations
from typing import Any, Mapping


def make_flex_doc(op_name: str, extra: str | None = None) -> str:
    """
    Week 0 stub: return a very small docstring for a flexible operation.
    """
    base = f"{op_name} (MAGIC Week 0 stub docstring)."
    if extra:
        base += f" {extra}"
    return base


def make_fixed_doc(op_name: str, extra: str | None = None) -> str:
    """
    Week 0 stub: alias to make_flex_doc.
    """
    return make_flex_doc(op_name, extra)


__all__ = ["make_flex_doc", "make_fixed_doc"]
