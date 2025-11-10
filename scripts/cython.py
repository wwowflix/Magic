# -*- coding: utf-8 -*-
"""Lightweight shim for optional Cython decorators so pure-Python runs work."""

from typing import Any, Callable, TypeVar

T = TypeVar("T")

def final(obj: T) -> T:
    # Acts like a no-op decorator: @cython.final
    return obj

def locals(**kw: Any) -> Callable[[T], T]:
    # Acts like a no-op decorator factory: @cython.locals(x=int)
    def deco(obj: T) -> T:
        return obj
    return deco

def cclass(cls: T) -> T:  # occasionally used
    return cls

def cfunc(func: T) -> T:  # occasionally used
    return func

__all__ = ["final", "locals", "cclass", "cfunc"]
