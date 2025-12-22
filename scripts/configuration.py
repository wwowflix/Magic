from __future__ import annotations

"""
MAGIC – Week 0 configuration shim.

Goal
----
- Let `import scripts.configuration` succeed during global smoke tests.
- Avoid pulling in heavy / fragile original configuration logic.
- Provide a very loose MagicAttr that accepts *any* arguments.
- Keep the surface small but "reasonable" so future code can adapt.

The original vendored module has been moved to:
    configuration.py.magic_bak_week0
"""

from dataclasses import dataclass
from typing import Any, Optional, Dict


class MagicAttr:
    """
    Week 0 stand-in for the original MagicAttr.

    - Accepts *any* args/kwargs so call sites never fail due to signature mismatch.
    - Stores arguments for potential debugging.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs

    def __repr__(self) -> str:  # pragma: no cover - debug only
        return f"MagicAttr(args={self.args!r}, kwargs={self.kwargs!r})"


@dataclass
class ConfigOption:
    """
    Minimal stand-in for a configuration option.
    """
    name: str
    default: Any = None
    description: Optional[str] = None


def load_config(*_args: Any, **_kwargs: Any) -> Dict[str, Any]:
    """
    Week 0 placeholder configuration loader.

    Returns an empty dict so callers can safely iterate / .get() without error.
    """
    return {}


__all__ = [
    "MagicAttr",
    "ConfigOption",
    "load_config",
]
