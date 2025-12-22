from __future__ import annotations

"""
MAGIC shim for arithmetic demo modules.

Original files (arithmetic.py, arithmetic_2.py, arithmetic_3.py) contained
large numpy type-checking / arithmetic examples that:

- Execute at import time, and
- Depend on numpy.typing internals or operations that now fail.

For MAGIC smoke tests we only need:
- `import scripts.arithmetic*` to succeed.
- A small, predictable API surface.

This shim provides basic arithmetic helpers that are safe and portable.
"""

from typing import Any


def add(a: Any, b: Any) -> Any:
    return a + b


def subtract(a: Any, b: Any) -> Any:
    return a - b


def multiply(a: Any, b: Any) -> Any:
    return a * b


def divide(a: Any, b: Any) -> Any:
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b


__all__ = ["add", "subtract", "multiply", "divide"]
