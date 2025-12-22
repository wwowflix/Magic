"""
MAGIC shim for `ply.yacc` used by pycparser's c_parser.

We DO NOT implement real parsing.
We only expose a `yacc()` function returning a dummy parser object.
"""

class DummyParser:
    def __init__(self, *args, **kwargs):
        pass

    def parse(self, *args, **kwargs):
        # Return None for all parse attempts
        return None

def yacc(module=None, **kwargs):
    """
    Minimal compatible API for ply.yacc.yacc(...)
    Ignore all arguments and return DummyParser.
    """
    return DummyParser()
