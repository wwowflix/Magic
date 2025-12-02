# -*- coding: utf-8 -*-
"""
MAGIC stub for scripts._html5lib_2

This is a lightweight stand-in for the html5lib / HTML5TreeBuilder stack.

Goals:
- Import cleanly (no SyntaxError, no missing symbols).
- Provide a minimal HTML5TreeBuilder API that tests can import.
- Avoid pulling heavy HTML/DOM dependencies at this stage.
"""

from __future__ import annotations

from typing import Any, Iterable, Optional

__all__ = ["HTML5TreeBuilder", "getTreeBuilder"]


class HTML5TreeBuilder:
    """
    Minimal stand-in for html5lib's HTML5TreeBuilder.

    For MAGIC:
    - We don't need a real DOM implementation.
    - We only need something that can be constructed and maybe called.
    """

    def __init__(self, name: str = "html5lib") -> None:
        self.name = name

    def parse(
        self,
        markup: str,
        encoding: Optional[str] = None,
        namespaceHTMLElements: bool = True,
    ) -> Any:
        """
        Very small fake parse method.

        In a real implementation this would return a tree-like structure.
        For MAGIC, we simply return a dict describing what happened so that
        tests (if any) have something structured to inspect.
        """
        return {
            "builder": "HTML5TreeBuilder",
            "backend": self.name,
            "encoding": encoding,
            "namespaceHTMLElements": namespaceHTMLElements,
            "length": len(markup) if markup is not None else 0,
        }

    def feed(self, chunks: Iterable[str]) -> Any:
        """
        Optional helper: pretend to accept an iterable of chunks.
        """
        text = "".join(chunks)
        return self.parse(text)


def getTreeBuilder(name: str = "html5lib") -> HTML5TreeBuilder:
    """
    Factory kept compatible with html5lib-style helpers.

    Some callers expect a getTreeBuilder() function that
    returns an object with a .parse() API.
    """
    return HTML5TreeBuilder(name=name)
