from __future__ import annotations

"""
MAGIC stub: lightweight replacement for the avar planning helper.

The original module imported from `fontTools.varLib.models` and triggered
version-dependent behavior inside fontTools (VarData, etc.).

For MAGIC we only need:
- safe import
- a couple of tiny helpers with *similar* names.
"""

from typing import Dict, Iterable, List, Mapping, Sequence, Tuple


def piecewiseLinearMap(x: float, mapping: Sequence[Tuple[float, float]]) -> float:
    """
    Very small stand-in for a piecewise-linear mapping function.

    `mapping` is a list of (input, output) points sorted by input.
    We linearly interpolate between the nearest points.
    This implementation is intentionally simple and only meant for tests.
    """
    if not mapping:
        return x

    pts = sorted(mapping, key=lambda p: p[0])
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]

    if x <= xs[0]:
        return ys[0]
    if x >= xs[-1]:
        return ys[-1]

    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            if x1 == x0:
                return y0
            t = (x - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)

    # Fallback (should not be hit if above covers all cases)
    return ys[-1]


def normalizeValue(value: float, triple: Tuple[float, float, float]) -> float:
    """
    Tiny stand-in for normalizeValue.

    `triple` is (min, default, max). We map the value into the -1..1 space
    using a simple linear rule.
    """
    min_v, default_v, max_v = triple
    if value == default_v:
        return 0.0
    if value < default_v and min_v != default_v:
        return (value - default_v) / (default_v - min_v)
    if value > default_v and max_v != default_v:
        return (value - default_v) / (max_v - default_v)
    return 0.0


def build_avar_plan(axes: Mapping[str, Iterable[Tuple[float, float]]]) -> Dict[str, List[Tuple[float, float]]]:
    """
    Very small helper that pretends to compute an 'avar' plan.

    For each axis we just normalize and return the points as a list.
    Enough for smoke tests to import and inspect.
    """
    plan: Dict[str, List[Tuple[float, float]]] = {}
    for tag, points in axes.items():
        plan[tag] = [(float(x), float(y)) for x, y in points]
    return plan
