from __future__ import annotations

"""
MAGIC stub: lightweight replacement for pygments.formatters.bbcode.

The original module depended on `pip._vendor.pygments.formatter.Formatter`.
For MAGIC Week 0 we only need:
- imports to succeed
- a tiny formatter class with a no-op format() method
"""

from typing import Any


class BBCodeFormatter:
    """
    Minimal stand-in for the real Pygments BBCode formatter.

    We accept arbitrary options, but the formatter does nothing. This is
    enough for tests that just want to instantiate or import the class.
    """

    def __init__(self, **options: Any) -> None:
        self.options = options

    def format(self, tokensource: Any, outfile: Any) -> None:
        # No-op: in real pygments this would write styled text to outfile.
        return None


def format_bbcode(code: str) -> str:
    """
    Simple helper that mirrors the idea of "formatting" BBCode.

    In this stub we just return the input unchanged.
    """
    return code
