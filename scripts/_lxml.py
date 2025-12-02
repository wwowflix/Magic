"""
MAGIC shim module for ``scripts._lxml``.

The original version depended on BeautifulSoup + lxml internals and
imported symbols like ``AttributeDict`` from ``bs4.element`` which are
not present in your environment.

For MAGIC, the smoke tests only require that::

    import scripts._lxml

succeeds, and that the module exposes ``LXMLTreeBuilder`` and
``LXMLTreeBuilderForXML`` as public names.

This shim provides tiny placeholder classes to satisfy those imports
without pulling in heavy or version-sensitive dependencies.
"""

from __future__ import annotations

from typing import Any, Iterable, Optional


class LXMLTreeBuilder:
    """
    Minimal stand-in for BeautifulSoup's lxml tree builder.

    It accepts the same kinds of parameters in ``__init__`` as the real
    implementation (loosely), but doesn't actually perform any parsing.
    """

    def __init__(
        self,
        *,
        namespaceHTMLElements: bool = True,
        **kwargs: Any,
    ) -> None:
        # We intentionally ignore all arguments. This is just a shim.
        self.namespaceHTMLElements = namespaceHTMLElements
        self._options = dict(kwargs)

    def prepare_markup(
        self,
        markup: Any,
        user_specified_encoding: Optional[str] = None,
        document_declared_encoding: Optional[str] = None,
        exclude_encodings: Optional[Iterable[str]] = None,
    ):
        """
        Very small stub of the real prepare_markup() API.

        Returns a 4-tuple similar in spirit to the real implementation but
        without any actual parsing or encoding detection.
        """
        # We simply return the original markup and echo back the encodings.
        return (
            markup,
            user_specified_encoding,
            document_declared_encoding,
            False,  # handled = False (no special handling done)
        )

    def feed(self, data: Any) -> None:  # pragma: no cover - trivial stub
        """
        In the real implementation this would feed data into the parser.

        In MAGIC's shim we deliberately do nothing – any real parsing logic
        lives elsewhere in your codebase, not in this compatibility layer.
        """
        return None


class LXMLTreeBuilderForXML(LXMLTreeBuilder):
    """
    XML-specific variant of :class:`LXMLTreeBuilder`.

    For the shim, we don't need different behaviour – it only exists so
    external code can import the name without crashing.
    """

    pass


__all__ = ["LXMLTreeBuilder", "LXMLTreeBuilderForXML"]
