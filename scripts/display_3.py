"""
MAGIC Week 0 shim for a second Altair-based display example.

The original module depended on `altair` and `altair.utils`. For MAGIC
smoke tests we only need this module to import successfully and, at most,
to provide a small chart-like object for demos.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence, List


@dataclass
class DummyChart:
    """
    Minimal stand-in for an Altair Chart-like object.
    """

    data: Any
    title: str | None = None

    def to_dict(self) -> Mapping[str, Any]:
        """
        Return a tiny dict that "looks like" a chart configuration.
        """
        return {
            "data": self.data,
            "mark": "line",
            "encoding": {},
            "title": self.title,
        }


def make_demo_chart_3(
    data: Sequence[Mapping[str, Any]] | None = None,
    title: str | None = "MAGIC demo chart 3",
) -> DummyChart:
    """
    Construct a dummy chart object for demonstration.

    Parameters
    ----------
    data:
        Optional iterable of mapping-like rows. If omitted, a tiny placeholder
        structure is used.
    title:
        Optional title string stored on the DummyChart.

    Returns
    -------
    DummyChart
        A chart-like object that is safe to construct during smoke tests.
    """
    if data is None:
        data = [{"x": 0, "y": 0}]
    rows: List[Mapping[str, Any]] = list(data)
    return DummyChart(rows, title=title)
