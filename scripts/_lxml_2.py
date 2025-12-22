"""
MAGIC shim module for ``scripts._lxml_2``.

The original version duplicated BeautifulSoup + lxml integration logic and
imported internal symbols like ``AttributeDict`` from ``bs4.element``,
which are not available in your current environment.

MAGIC only needs this module to be importable, and for it to expose the
same public names as ``scripts._lxml``.

This shim simply re-exports the lightweight classes defined in
``scripts._lxml``:

    from scripts._lxml import LXMLTreeBuilder, LXMLTreeBuilderForXML
"""

from __future__ import annotations

# Re-use the already-stable shim from scripts._lxml
from ._lxml import LXMLTreeBuilder, LXMLTreeBuilderForXML

__all__ = ["LXMLTreeBuilder", "LXMLTreeBuilderForXML"]
