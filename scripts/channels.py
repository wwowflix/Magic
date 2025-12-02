from __future__ import annotations

"""
MAGIC stub: safe placeholder for an Altair-like channels module.

Original depended on:
- narwhals.stable.v1 as nw
- altair.utils.infer_encoding_types

For MAGIC Week 0 we only need:
- `import scripts.channels` to succeed
- A tiny, harmless API surface so any light call sites don't explode
"""

from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional


@dataclass
class Channel:
    """Minimal stand-in for a chart channel (x, y, color, size, etc.)."""

    name: str
    type: Optional[str] = None
    description: Optional[str] = None


def infer_encoding_types(data: Any) -> Dict[str, str]:
    """
    Very small replacement for altair.utils.infer_encoding_types.

    We just guess that:
    - mapping keys become "quantitative"
    - otherwise we return an empty dict.
    This is enough so callers can iterate over a dict of field->type.
    """
    if isinstance(data, Mapping):
        return {str(k): "quantitative" for k in data.keys()}
    return {}


# Backwards-compatible alias with the original name
_infer_encoding_types = infer_encoding_types
