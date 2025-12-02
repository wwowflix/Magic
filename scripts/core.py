from __future__ import annotations

'''MAGIC Week 0 shim for scripts.core.

Auto-generated placeholder to allow safe import during Week 0.
Real implementation will be added or restored in Week 1+.
'''

from typing import Any

__all__: list[str] = []


# ---------------------------------------------------------------------------
# MAGIC Week 0 shim: ParserElement (used by scripts.cElementTree and others)
# ---------------------------------------------------------------------------
from typing import Any

class ParserElement:
    """
    Minimal Week 0 stand-in for pyparsing.ParserElement.

    It only exists so imports like `from scripts.core import ParserElement`
    succeed. Real parsing logic is NOT implemented in Week 0.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs

    def parse_string(self, text: str) -> Any:  # pragma: no cover
        # Week 0: just return the original text or a trivial wrapper
        return text

__all__ = globals().get("__all__", [])
if "ParserElement" not in __all__:
    __all__.append("ParserElement")
