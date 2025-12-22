"""
MAGIC Week 0: stub for scripts.display_2 (Altair-style display helpers).

Goal:
- Let "import scripts.display_2" succeed.
- Provide a couple of no-op functions that tests (if any) can call safely.
- Avoid importing altair, vegafusion, or doing any heavy work at import time.
"""

from __future__ import annotations

from typing import Any


def render_chart(chart: Any, *args: Any, **kwargs: Any) -> Any:
    """
    Week 0 stub for any chart-display helper.

    We simply return the input object unchanged so callers don't break.
    """
    return chart


def transform_data(data: Any, *args: Any, **kwargs: Any) -> Any:
    """
    Week 0 stub for any data transformation step.

    Real implementation might adapt data for Vega/Vega-Lite.
    Here we just return it unchanged.
    """
    return data


__all__ = ["render_chart", "transform_data"]
