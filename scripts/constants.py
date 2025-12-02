"""
MAGIC shim for scripts.constants.

This provides the minimal subset of symbols needed by:
- scripts._ihatexml
- scripts._inputstream
- (and any future html5lib-style stubs)

Goal:
- Satisfy imports during tests.
- Behave safely at runtime.
- We do NOT re-implement full html5lib behaviour.
"""

from __future__ import annotations

import string
from typing import FrozenSet


class DataLossWarning(UserWarning):
    """
    MAGIC stub warning used by _ihatexml.

    The real library defines a custom warning type; inheriting from
    UserWarning is enough so that `issubclass(DataLossWarning, Warning)`
    and catching it still work.
    """
    pass


class _ReparseException(Exception):
    """
    MAGIC stub exception used by _inputstream.

    In the original parser, this is raised internally to indicate that
    the input stream should be reparsed from a different position.
    For our purposes, we only need a distinct exception type so that
    `except _ReparseException:` blocks still behave correctly.
    """
    pass


# Sentinel used to indicate "end of file" in html5lib-style parsers.
EOF = object()

# Minimal set of whitespace characters treated as "space" by the parser.
# Common html5lib definition: space, tab, LF, FF, CR.
spaceCharacters: FrozenSet[str] = frozenset(" \t\n\x0c\r")

# Basic ASCII helper sets, as expected by html5lib-style code.
asciiLetters: str = string.ascii_letters
asciiUppercase: str = string.ascii_uppercase
asciiLowercase: str = string.ascii_lowercase

# Extra helpers that may be imported later; they are cheap to define now.
digits: str = string.digits
hexDigits: str = string.hexdigits

__all__ = [
    "DataLossWarning",
    "_ReparseException",
    "EOF",
    "spaceCharacters",
    "asciiLetters",
    "asciiUppercase",
    "asciiLowercase",
    "digits",
    "hexDigits",
]
# ===== MAGIC compatibility shim appended at end of constants.py =====
# These names are expected by html5lib-style modules (base_2, base_3, etc.).
# We define simple, safe defaults ONLY if they don't already exist.

try:
    scopingElements  # type: ignore[name-defined]
except NameError:  # pragma: no cover
    # Minimal set of elements that act as "scoping" elements in HTML parsing.
    scopingElements = {
        "html",
        "table",
        "td",
        "th",
        "caption",
    }

try:
    tableInsertModeElements  # type: ignore[name-defined]
except NameError:  # pragma: no cover
    # Elements that trigger "in table" insertion mode in HTML parsers.
    tableInsertModeElements = {
        "table",
        "tbody",
        "tfoot",
        "thead",
        "tr",
    }

try:
    namespaces  # type: ignore[name-defined]
except NameError:  # pragma: no cover
    # Standard HTML-related namespace map used by html5lib.
    namespaces = {
        "html": "http://www.w3.org/1999/xhtml",
        "mathml": "http://www.w3.org/1998/Math/MathML",
        "svg": "http://www.w3.org/2000/svg",
        "xlink": "http://www.w3.org/1999/xlink",
        "xml": "http://www.w3.org/XML/1998/namespace",
        "xmlns": "http://www.w3.org/2000/xmlns/",
    }
# ===== end MAGIC compatibility shim =====
# ===== MAGIC extra compatibility shim (voidElements / spaceCharacters) =====
# More html5lib-style names expected by base_3 and related modules.

try:
    voidElements  # type: ignore[name-defined]
except NameError:  # pragma: no cover
    # Set of elements that do not have closing tags in HTML.
    voidElements = {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
        # legacy/obsolete but safe to include:
        "command",
        "keygen",
        "menuitem",
    }

try:
    spaceCharacters  # type: ignore[name-defined]
except NameError:  # pragma: no cover
    # Characters treated as whitespace by the HTML tokenizer.
    spaceCharacters = {
        " ",
        "\t",
        "\n",
        "\r",
        "\f",
    }
# ===== end MAGIC extra compatibility shim =====
