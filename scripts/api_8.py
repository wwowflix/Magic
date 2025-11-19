from __future__ import annotations

"""
MAGIC shim for scripts.api_8

Original module pulled in:
- altair (theme, utils)
- narwhals.stable.v1
- jsonschema
and a bunch of chart/validation logic.

For MAGIC smoke tests we only need:
- `import scripts.api_8` to succeed.
- Optionally a tiny, JSON-friendly chart-like object.
"""

from dataclasses import dataclass, asdict
from typing import Any, Dict


@dataclass
class ChartSpec:
    """Minimal chart specification for MAGIC."""
    data: Any
    mark: str = "point"
    encoding: Dict[str, Any] | None = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "data": self.data,
            "mark": self.mark,
            "encoding": self.encoding or {},
        }


def create_chart(data: Any, mark: str = "point", encoding: Dict[str, Any] | None = None) -> ChartSpec:
    """Return a simple ChartSpec wrapper."""
    return ChartSpec(data=data, mark=mark, encoding=encoding)


def as_json_dict(chart: ChartSpec) -> Dict[str, Any]:
    """Return a JSON-serializable dict for a ChartSpec."""
    # Using asdict is fine here; we also normalise to the to_dict() format.
    base = asdict(chart)
    return {
        "data": base["data"],
        "mark": base["mark"],
        "encoding": base.get("encoding") or {},
    }


__all__ = ["ChartSpec", "create_chart", "as_json_dict"]
