"""
MAGIC Week 0 shim for a second decorators module (e.g. click / CLI style).

The original file imported `Argument` from a local `core` module. Here we
just define a minimal stand-in so that imports succeed.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Argument:
    name: str
    required: bool = False
    default: Optional[Any] = None


def with_argument(name: str, required: bool = False):
    """
    Decorator that attaches very small metadata to a function.
    """
    def decorator(func):
        if not hasattr(func, "__magic_arguments__"):
            func.__magic_arguments__ = []
        func.__magic_arguments__.append(Argument(name=name, required=required))
        return func

    return decorator
