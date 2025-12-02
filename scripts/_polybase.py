"""MAGIC shim for numpy.polynomial._polybase.

We just provide a minimal ABCPolyBase so imports succeed.
"""

from __future__ import annotations

from abc import ABCMeta
from typing import Any, Sequence


class ABCPolyBase(metaclass=ABCMeta):
    def __init__(self, coef: Sequence[Any], domain=None, window=None):
        self.coef = list(coef)
        self.domain = domain
        self.window = window

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(coef={self.coef!r})"
