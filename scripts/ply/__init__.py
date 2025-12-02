"""
MAGIC shim for the `ply` package used by c_lexer.

We only provide a dummy `lex` module so that:
    from .ply import lex
and
    lex.lex(...)
both work without errors.
"""
# The real implementation lives in ply/lex.py
