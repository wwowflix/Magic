"""
MAGIC stub for scripts.syntax

Goal:
- Provide a very small, safe stand-in for a "syntax" / token module
  (similar to pygments.tokens or rich.syntax).
- Avoid heavy imports and complex lexer logic.
- Make sure attributes like `Token.Preproc` exist and do NOT crash.

The smoke tests only need this module to import successfully and expose
some basic names; they do not rely on real syntax highlighting.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Iterator, Optional


class MagicAttr:
    """
    Extremely small placeholder object used as a stand-in for token
    hierarchies like `Token.Keyword`, `Token.Preproc`, etc.

    Any attribute access returns `self`, so things like
        Token.Preproc.Comment
    are all valid and harmless.

    Calling the object just returns `self` as well, so it can be used
    in places that expect a callable or type-like object.
    """

    def __getattr__(self, name: str) -> "MagicAttr":
        # Return self for any nested attribute access.
        return self

    def __call__(self, *args: Any, **kwargs: Any) -> "MagicAttr":
        # Allow it to be called without doing anything.
        return self

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return "<MagicAttr>"


# Token object used by callers like `Token.Keyword`, `Token.Preproc`, etc.
Token = MagicAttr()

# Some callers import `Name` separately for token classification.
# We just expose MagicAttr instances for compatibility.
Name = MagicAttr()
Raw = MagicAttr()




@dataclass
class Syntax:
    """
    Minimal stand-in for a "rich.syntax.Syntax"-style object.

    We only keep the constructor signature small and safe. This is
    enough for imports and simple usage in `drawing` / `style` shims.
    """

    code: str
    lexer: Optional[str] = None
    theme: Optional[str] = None
    line_numbers: bool = False

    def __post_init__(self) -> None:
        # No heavy work here; this is just a stub.
        if not isinstance(self.code, str):
            self.code = str(self.code)

    # The real rich.Syntax has a __rich_console__ method; we provide a
    # benign placeholder so that printing to a Rich console (if ever
    # used) at least yields the raw code.
    def __rich_console__(self, console: Any, options: Any) -> Iterator[str]:  # pragma: no cover
        yield self.code


# Optional theme stub – many callers only need the name to exist.
@dataclass
class SyntaxTheme:
    """
    Tiny placeholder for a syntax theme description.

    We just store the theme name and ignore the rest.
    """

    name: str = "magic-default"


DEFAULT_SYNTAX_THEME = SyntaxTheme(name="magic-default")

__all__ = [
    "MagicAttr",
    "Token",
    "Name",
    "Raw",
    "Syntax",
    "SyntaxTheme",
    "DEFAULT_SYNTAX_THEME",
]
