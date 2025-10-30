"""MAGIC shim: safe no-op for scalar doc hooks."""


def add_newdoc_for_scalar(*a, **k):
    return None


__all__ = ["add_newdoc_for_scalar"]
