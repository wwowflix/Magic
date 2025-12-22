"""
MAGIC Week 0 shim for default styles.

The original module built a large mapping of Style objects and triggered
`Color.parse("default")` during import, which is fragile.

Here we define a tiny, safe subset that is enough for imports and for any
debug / pretty-printing we might use in MAGIC.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class Style:
    name: str
    description: Optional[str] = None


DEFAULT_STYLES = {
    "reset": Style("reset", "MAGIC default style"),
}
