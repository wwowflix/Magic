# -*- coding: utf-8 -*-
"""Compat helpers for numpy edge cases."""
try:
    import numpy as _np
    Inf = getattr(_np, "inf", float("inf"))
    NaN = getattr(_np, "nan", float("nan"))
except Exception:
    Inf = float("inf")
    NaN = float("nan")
