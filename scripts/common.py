"""
MAGIC shim for pyparsing.common used by cElementTree.

We ONLY need names to exist so imports do not fail.
No parsing, no real logic.
"""

from .core import ParserElement

# --- Dummy no-op functions / classes ---

def _generate_etree_functions(*args, **kwargs):
    """
    cElementTree expects this to return a 3-tuple:
        (parse, iterparse, fromstring)
    We return dummy no-op callables.
    """
    def _noop(*a, **k):
        return None
    return _noop, _noop, _noop


class pyparsing_common:
    integer = ParserElement()
    real = ParserElement()
    number = ParserElement()
    hex_integer = ParserElement()
    fraction = ParserElement()
    mixed_integer = ParserElement()
    fnumber = ParserElement()
    uuid = ParserElement()
    comma_separated_list = ParserElement()
    url = ParserElement()

__all__ = [
    "pyparsing_common",
    "_generate_etree_functions",
]
