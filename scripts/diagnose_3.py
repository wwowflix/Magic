"""
MAGIC Week 0 shim for BeautifulSoup-dependent diagnose script.

The original file attempted to import BeautifulSoup from bs4, which may not
exist in the MAGIC environment. For smoke tests, we only require imports
to succeed, so we provide minimal placeholder implementations.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any


class BeautifulSoup:
    """
    Minimal BeautifulSoup placeholder.

    Stores the provided markup and returns predictable dummy output.
    """
    def __init__(self, markup: str | bytes | None = None, parser: str = "html.parser") -> None:
        self.markup = markup
        self.parser = parser

    def find_all(self, *args: Any, **kwargs: Any) -> list:
        # MAGIC placeholder: always return an empty list
        return []

    def get_text(self) -> str:
        # MAGIC placeholder: return the markup string if available
        if isinstance(self.markup, (str, bytes)):
            return str(self.markup)
        return ""


@dataclass
class SoupStrainer:
    """
    Minimal SoupStrainer placeholder.
    """
    name: str | None = None


def extract_info(html: str) -> dict:
    """
    Dummy HTML extraction used for test imports.

    Accepts HTML string and returns a simple dictionary.
    """
    soup = BeautifulSoup(html)
    return {
        "text": soup.get_text(),
        "elements": [],
    }
