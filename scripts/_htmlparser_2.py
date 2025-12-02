# -*- coding: utf-8 -*-
"""
MAGIC stub for scripts._htmlparser_2

This replaces a BeautifulSoup/HTMLParser-based tree builder with a tiny,
import-safe stand-in.

Goals:
- Avoid importing bs4.element internals (AttributeDict, CData, etc.).
- Provide a minimal HTMLParserTreeBuilder API that tests can import.
- Keep behaviour lightweight and deterministic for smoke tests.
"""

from __future__ import annotations

from typing import Any, Iterable, Optional

__all__ = ["HTMLParserTreeBuilder", "getTreeBuilder"]


class HTMLParserTreeBuilder:
    """
    Minimal stand-in for an HTMLParser-based tree builder.

    For MAGIC we only need:
    - Construction to succeed.
    - A .parse() method that returns some structured object.
    - Optionally a .feed() helper that also calls .parse().
    """

    def __init__(self, name: str = "html.parser") -> None:
        self.name = name

    def parse(
        self,
        markup: str,
        encoding: Optional[str] = None,
    ) -> Any:
        """
        Fake parse method.

        We don't build a real DOM — just return a small dict with enough
        fields that tests (if any) can safely inspect.
        """
        return {
            "builder": "HTMLParserTreeBuilder",
            "backend": self.name,
            "encoding": encoding,
            "length": len(markup) if markup is not None else 0,
        }

    def feed(self, chunks: Iterable[str]) -> Any:
        """
        Convenience wrapper to accept an iterable of HTML chunks.
        """
        text = "".join(chunks)
        return self.parse(text)


def getTreeBuilder(name: str = "html.parser") -> HTMLParserTreeBuilder:
    """
    Factory kept compatible with html5lib-style helpers.

    Some callers expect a getTreeBuilder() that returns an object
    with a .parse() API.
    """
    return HTMLParserTreeBuilder(name=name)
