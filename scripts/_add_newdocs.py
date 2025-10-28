"""MAGIC shim: safe no-ops for legacy docs injection."""
def add_newdoc(place=None, obj=None, doc=None):
    try:
        if obj is not None and isinstance(doc, str):
            obj.__doc__ = doc
    except Exception:
        pass
def add_newdoc_ufunc(*a, **k): return None
__all__ = ["add_newdoc","add_newdoc_ufunc"]