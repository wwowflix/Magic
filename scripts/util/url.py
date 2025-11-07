from __future__ import annotations

"""MAGIC shim: minimal Url object just for type/import satisfaction."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Url:
    scheme: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    path: Optional[str] = None
    query: Optional[str] = None

    def __str__(self) -> str:  # pragma: no cover
        core = (self.path or "") if self.path else ""
        if self.host:
            core = (self.host + (f":{self.port}" if self.port else "")) + (
                core if core.startswith("/") else f"/{core}"
            )
        if self.scheme:
            core = f"{self.scheme}://{core}"
        if self.query:
            core = f"{core}?{self.query}"
        return core


__all__ = ["Url"]
