from __future__ import annotations

"""
MAGIC – Week 0 completion shim.

Goal
----
- Allow `import scripts.completion` to succeed during global smoke tests.
- Avoid executing the heavy / incompatible original completion logic.
- Do NOT affect the real stdlib or external completion libraries.

The original vendored module has been moved to:
    completion.py.magic_bak_week0

A later week can reintroduce a proper adapter if needed.
"""

from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class CompletionItem:
    """
    Minimal stand-in for a completion entry.

    This is intentionally tiny: it just needs to be a reasonable value object
    if any higher-level code inspects items.
    """
    text: str
    type: str = "text"
    description: Optional[str] = None


class MagicAttr:
    """
    Very loose stand-in for the original MagicAttr.

    The important part for Week 0 is:
    - Accept *any* arguments in __init__ so imports never crash due to
      signature mismatches.
    - Store them for debugging if needed.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs

    def __repr__(self) -> str:  # pragma: no cover - just for debugging
        return f"MagicAttr(args={self.args!r}, kwargs={self.kwargs!r})"


def complete(prefix: str) -> List[CompletionItem]:
    """
    Week 0 placeholder completion function.

    Returns an empty list by default so it is safe to call but does
    not provide real suggestions yet.
    """
    return []


__all__ = [
    "CompletionItem",
    "MagicAttr",
    "complete",
]
