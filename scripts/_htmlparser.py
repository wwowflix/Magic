# -*- coding: utf-8 -*-
"""
MAGIC stub for scripts._htmlparser

This is a lightweight stand-in for the stdlib HTMLParser-based tree builder.

Goals:
- Import cleanly (no SyntaxError, no missing symbols).
- Provide a minimal HTMLParserTreeBuilder API that tests can import.
- Avoid pulling any heavy HTML/DOM dependencies at this stage.
"""

from __future__ import annotations

from typing import Any, Iterable, Optional

__all__ = ["HTMLParserTreeBuilder", "getTreeBuilder"]


class HTMLParserTreeBuilder:
    """
    Minimal stand-in for an HTMLParser-based tree builder.

    For MAGIC:
    - We don't need a real DOM implementation.
    - We only need something that can be constructed and maybe called.
    """

    def __init__(self, name: str = "html.parser") -> None:
        self.name = name

    def parse(
        self,
        markup: str,
        encoding: Optional[str] = None,
    ) -> Any:
        """
        Very small fake parse method.

        Returns a simple dict so tests (if any) have something structured
        to inspect, without needing a real HTML tree.
        """
        return {
            "builder": "HTMLParserTreeBuilder",
            "backend": self.name,
            "encoding": encoding,
            "length": len(markup) if markup is not None else 0,
        }

    def feed(self, chunks: Iterable[str]) -> Any:
        """
        Optional helper: pretend to accept an iterable of chunks.
        """
        text = "".join(chunks)
        return self.parse(text)


def getTreeBuilder(name: str = "html.parser") -> HTMLParserTreeBuilder:
    """
    Factory kept compatible with html5lib-style helpers.

    Some callers expect a getTreeBuilder() function that
    returns an object with a .parse() API.
    """
    return HTMLParserTreeBuilder(name=name)
