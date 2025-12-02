"""
MAGIC shim for `ply.lex` used by pycparser's c_lexer.

We do NOT implement real lexing. We just expose a `lex()` function
that returns a dummy lexer object with the methods that c_lexer expects.
"""

class DummyLexer:
    def __init__(self, *args, **kwargs):
        self.data = ""

    def build(self, *args, **kwargs):
        # Real PLY builds DFA tables etc. We just return self.
        return self

    def input(self, data):
        # Store the data; we don't actually tokenize.
        self.data = data

        # No real tokens – always signal "no more tokens".
        return None


def lex(module=None, **kwargs):
    """
    Minimal compatible API for `ply.lex.lex(module=..., ...)`.

    We ignore all arguments and return a DummyLexer instance.
    """
    return DummyLexer()
# --------------------------------------------------------------------
# MAGIC additional shim: TOKEN decorator
# pycparser does:  from ply.lex import TOKEN
# This decorator simply returns the function unchanged.
# --------------------------------------------------------------------
    return f
# --------------------------------------------------------------------
# Improved MAGIC TOKEN shim:
# TOKEN(<regex>) returns a decorator that returns the function unchanged.
# --------------------------------------------------------------------
def TOKEN(regex):
    def decorator(func):
        return func
    return decorator
