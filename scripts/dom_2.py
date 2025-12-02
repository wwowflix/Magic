"""
MAGIC Week 0: stub for scripts.dom_2.

Goal:
- Let "import scripts.dom_2" succeed.
- Avoid depending on snscrape.utils.NonRecursiveTreeWalker.
- Provide a tiny DOMNode + parse_html helper so callers don’t crash.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class DOMNode:
    """
    Very small placeholder for a DOM-like node.

    Week 0:
    - Just stores tag, attrs, children, and text.
    - No real HTML parsing behaviour.
    """

    tag: str = "html"
    attrs: dict[str, Any] | None = None
    children: list["DOMNode"] | None = None
    text: str = ""

    def __post_init__(self) -> None:
        if self.attrs is None:
            self.attrs = {}
        if self.children is None:
            self.children = []


def parse_html(html: str) -> DOMNode:
    """
    Week 0 stub: wrap the raw HTML string in a single DOMNode.
    """
    return DOMNode(tag="html", attrs={}, children=[], text=html)


__all__ = ["DOMNode", "parse_html"]
