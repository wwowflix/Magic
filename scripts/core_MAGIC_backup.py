"""
MAGIC shim for pyparsing core used by ElementTree, lxml-like helpers.

We do NOT implement real parsing. We only provide the *minimal*
classes and functions needed so that imports succeed.
"""

class ParserElement:
    """
    Extremely small parser base. Does nothing except exist.
    """
    def __init__(self, *args, **kwargs):
        self.customName = None
        self.errmsg = ""

    def set_name(self, name):
        self.customName = name
        return self

class Word(ParserElement):
    def __init__(self, *args, **kwargs):
        super().__init__()
        # Accept anything; no real parsing.

class Literal(ParserElement):
    pass

class Optional(ParserElement):
    pass

class OneOrMore(ParserElement):
    pass

class ZeroOrMore(ParserElement):
    pass

class Combine(ParserElement):
    pass

# Helpers that some modules expect
alphas = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
nums = "0123456789"
alphanums = alphas + nums

__all__ = [
    "ParserElement",
    "Word",
    "Literal",
    "Optional",
    "OneOrMore",
    "ZeroOrMore",
    "Combine",
    "alphas",
    "nums",
    "alphanums",
]
