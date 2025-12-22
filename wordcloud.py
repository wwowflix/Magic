"""
Minimal shim for wordcloud.WordCloud for Week 0 import tests.

This is only to satisfy imports in scripts.charts_2 without
installing the real wordcloud package.
"""

from typing import Any, Iterable, Optional


class WordCloud:
    def __init__(
        self,
        width: int = 400,
        height: int = 200,
        stopwords: Optional[Iterable[str]] = None,
        **kwargs: Any,
    ) -> None:
        self.width = width
        self.height = height
        self.stopwords = set(stopwords or [])
        self.kwargs = kwargs
        self._text = ""

    def generate(self, text: str) -> "WordCloud":
        # Store the text so calls are chainable
        self._text = text
        return self

    def to_array(self):
        # Return a tiny dummy "image"-like structure
        # Code that just expects something array-ish will be satisfied.
        size = 10
        return [[0] * size for _ in range(size)]
