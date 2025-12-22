"""
MAGIC – Week 0 stub for adapter.

Original module used MagicAttr with a constructor signature mismatch, causing:
    TypeError: MagicAttr.__init__() takes 2 positional arguments but 4 were given

For Week 0 we only need `import scripts.adapter` to succeed during smoke tests.
No runtime behaviour is required.
"""

from typing import Any

class AdapterPlaceholder:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # Accept any arguments to avoid signature issues.
        self.args = args
        self.kwargs = kwargs

    def __repr__(self) -> str:  # pragma: no cover
        return f"<AdapterPlaceholder Week0 stub args={self.args!r} kwargs={self.kwargs!r}>"

__all__ = ["AdapterPlaceholder"]
