"""MAGIC shim for numpy's internal _pocketfft module.

Very small, pure-Python wrapper around numpy.fft so that
`import scripts._pocketfft` succeeds.
"""

from __future__ import annotations

from typing import Any
import numpy as _np

ArrayLike = Any


def _asarray(x: ArrayLike) -> _np.ndarray:
    return _np.asarray(x)


def fft(a: ArrayLike, *args: Any, **kwargs: Any):
    return _np.fft.fft(_asarray(a), *args, **kwargs)


def ifft(a: ArrayLike, *args: Any, **kwargs: Any):
    return _np.fft.ifft(_asarray(a), *args, **kwargs)


def rfft(a: ArrayLike, *args: Any, **kwargs: Any):
    return _np.fft.rfft(_asarray(a), *args, **kwargs)


def irfft(a: ArrayLike, *args: Any, **kwargs: Any):
    return _np.fft.irfft(_asarray(a), *args, **kwargs)


__all__ = ["fft", "ifft", "rfft", "irfft"]
