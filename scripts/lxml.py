from __future__ import annotations

"""
MAGIC Week 0 stub for the `lxml` package.

Goals:
- Allow `from lxml import etree, html` to succeed for vendored scripts like ElementInclude / ElementSoup.
- Avoid importing any real lxml C extensions or causing circular imports.
- Provide a minimal `etree` namespace (Element, SubElement, fromstring, tostring).
- Provide a minimal `html` namespace with fromstring/tostring/document_fromstring.
- Provide etree.LxmlSyntaxError so ElementInclude can subclass it.

This is enough for smoke imports during Week 0.
"""

from typing import Any, Optional


class LxmlSyntaxError(Exception):
    """
    MAGIC Week 0 stub for lxml.etree.LxmlSyntaxError.

    No special behavior – it just has to exist as an exception type.
    """


class _DummyElement:
    """Very small stand-in for an XML Element node."""

    def __init__(self, tag: str = "dummy", text: Optional[str] = None, **attrs: Any) -> None:
        self.tag = tag
        self.text = text
        self.attrib = dict(attrs)
        self.children: list["_DummyElement"] = []

    def append(self, elem: "_DummyElement") -> None:
        self.children.append(elem)

    def __repr__(self) -> str:
        return f"<_DummyElement tag={self.tag!r}>"


def _element(tag: str, text: Optional[str] = None, **attrs: Any) -> _DummyElement:
    return _DummyElement(tag=tag, text=text, **attrs)


def _subelement(parent: _DummyElement, tag: str, text: Optional[str] = None, **attrs: Any) -> _DummyElement:
    elem = _DummyElement(tag=tag, text=text, **attrs)
    parent.append(elem)
    return elem


def _fromstring(data: str, *args: Any, **kwargs: Any) -> _DummyElement:
    # Minimal parser: ignore actual XML, just wrap into a dummy element.
    return _DummyElement(tag="root", text=data)


def _tostring(elem: _DummyElement, *args: Any, **kwargs: Any) -> bytes:
    # Minimal serializer: just return a placeholder representation.
    return f"<{elem.tag}>...</{elem.tag}>".encode("utf-8")


class _EtreeNamespace:
    """Namespace object mimicking lxml.etree with a tiny surface."""

    Element = staticmethod(_element)
    SubElement = staticmethod(_subelement)
    fromstring = staticmethod(_fromstring)
    tostring = staticmethod(_tostring)

    # Types / aliases some code may expect
    _Element = _DummyElement
    LxmlSyntaxError = LxmlSyntaxError


class _HtmlNamespace:
    """
    Tiny stand-in for lxml.html.

    soupparser does: `from lxml import etree, html`
    It typically calls html.fromstring / html.tostring / html.document_fromstring.
    We provide minimal versions that just use _DummyElement.
    """

    def fromstring(self, data: str, *args: Any, **kwargs: Any) -> _DummyElement:
        # Pretend we parsed an HTML document.
        return _DummyElement(tag="html", text=data)

    def document_fromstring(self, data: str, *args: Any, **kwargs: Any) -> _DummyElement:
        # Same idea as fromstring, but named differently.
        return _DummyElement(tag="html", text=data)

    def tostring(self, elem: _DummyElement, *args: Any, **kwargs: Any) -> bytes:
        return _tostring(elem, *args, **kwargs)


# What `from lxml import etree, html` should see.
etree = _EtreeNamespace()
html = _HtmlNamespace()

__all__ = ["etree", "html", "_DummyElement", "LxmlSyntaxError"]
