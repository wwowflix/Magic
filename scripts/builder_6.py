"""
MAGIC shim for fontTools.varLib VariationStore builder.

This project only needs this module to be importable for smoke tests.
All heavy OpenType / variation math is intentionally skipped.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, List, Mapping, Sequence


# --- Lightweight data classes -------------------------------------------------


@dataclass
class VarRegionAxis:
    start: float = 0.0
    peak: float = 0.0
    end: float = 0.0


@dataclass
class VarRegion:
    axes: List[VarRegionAxis]


@dataclass
class SparseVarRegionAxis:
    axis_index: int
    start: float = 0.0
    peak: float = 0.0
    end: float = 0.0


@dataclass
class SparseVarRegion:
    axes: List[SparseVarRegionAxis]


@dataclass
class VarRegionList:
    regions: List[VarRegion]


@dataclass
class SparseVarRegionList:
    regions: List[SparseVarRegion]


# --- Builder helpers (no-op / simplified) -------------------------------------


def _norm_axis_support(axis_support: Sequence[float] | None) -> Sequence[float]:
    if not axis_support:
        return (0.0, 0.0, 0.0)
    if len(axis_support) == 1:
        v = float(axis_support[0])
        return (0.0, v, 0.0)
    if len(axis_support) == 2:
        start, peak = axis_support
        return (float(start), float(peak), float(peak))
    start, peak, end = axis_support[:3]
    return (float(start), float(peak), float(end))


def buildVarRegionAxis(axisSupport: Sequence[float] | None) -> VarRegionAxis:
    start, peak, end = _norm_axis_support(axisSupport)
    return VarRegionAxis(start=start, peak=peak, end=end)


def buildVarRegion(
    support: Mapping[str, Sequence[float]] | None, axisTags: Sequence[str]
) -> VarRegion:
    support = support or {}
    axes = [buildVarRegionAxis(support.get(tag)) for tag in axisTags]
    return VarRegion(axes=axes)


def buildVarRegionList(
    supports: Iterable[Mapping[str, Sequence[float]]], axisTags: Sequence[str]
) -> VarRegionList:
    regions = [buildVarRegion(support, axisTags) for support in supports]
    return VarRegionList(regions=regions)


def buildSparseVarRegionAxis(
    axisIndex: int, axisSupport: Sequence[float] | None
) -> SparseVarRegionAxis:
    start, peak, end = _norm_axis_support(axisSupport)
    return SparseVarRegionAxis(axis_index=axisIndex, start=start, peak=peak, end=end)


def buildSparseVarRegion(
    support: Mapping[str, Sequence[float]] | None, axisTags: Sequence[str]
) -> SparseVarRegion:
    support = support or {}
    axes: List[SparseVarRegionAxis] = []
    for i, tag in enumerate(axisTags):
        if tag not in support:
            continue
        axes.append(buildSparseVarRegionAxis(i, support[tag]))
    return SparseVarRegion(axes=axes)


def buildSparseVarRegionList(
    supports: Iterable[Mapping[str, Sequence[float]]], axisTags: Sequence[str]
) -> SparseVarRegionList:
    regions = [buildSparseVarRegion(support, axisTags) for support in supports]
    return SparseVarRegionList(regions=regions)


class VarData:
    """
    Lightweight mock VarData.

    Only exists so tests importing builder_6 succeed; we do NOT perform any
    OpenType math here.
    """

    def __init__(self) -> None:
        self.VarRegionIndex: List[int] = []
        self.VarRegionCount: int = 0
        self.Item: List[Sequence[int]] = []
        self.NumShorts: int = 0

    def calculateNumShorts(self, optimize: bool = False) -> "VarData":
        # No-op; keep attributes consistent and return self so callers can chain.
        return self


def VarData_calculateNumShorts(self: Any, optimize: bool = False) -> Any:
    """
    Helper function with the same signature as the original varLib helper.

    In the real fontTools, this gets monkey-patched onto ot.VarData.
    Here we just keep it around so any caller that imports it can call it
    and get back the same object.
    """
    return self


__all__ = [
    "VarRegionAxis",
    "VarRegion",
    "SparseVarRegionAxis",
    "SparseVarRegion",
    "VarRegionList",
    "SparseVarRegionList",
    "buildVarRegionAxis",
    "buildVarRegion",
    "buildVarRegionList",
    "buildSparseVarRegionAxis",
    "buildSparseVarRegion",
    "buildSparseVarRegionList",
    "VarData",
    "VarData_calculateNumShorts",
]
