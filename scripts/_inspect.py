from __future__ import annotations

'''MAGIC Week 0 shim for scripts._inspect.

Auto-generated placeholder to allow safe import during Week 0.
Real implementation will be restored or replaced in Week 1+.
'''

from typing import Any

__all__: list[str] = []


class _DummyInspector:
    '''Very small placeholder used only in Week 0.'''
    def inspect(self, obj: Any) -> str:  # pragma: no cover
        return f"Dummy inspector for: {type(obj)!r}"


dummy_inspector = _DummyInspector()
