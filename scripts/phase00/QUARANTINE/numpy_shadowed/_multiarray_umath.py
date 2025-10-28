# MAGIC stub to satisfy numpy-like private API for smoke imports only.
# Provides names imported by scripts.multiarray; not functional.

def _fastCopyAndTranspose(a, *args, **kwargs):
    # Return the input for smoke safety
    return a

_flagdict = {}

def _insert(*args, **kwargs):
    return None

def _reconstruct(*args, **kwargs):
    return None

def _vec_string(*args, **kwargs):
    return []

_ARRAY_API = object()

def _monotonicity(*args, **kwargs):
    return None

__all__ = [
    "_fastCopyAndTranspose",
    "_flagdict",
    "_insert",
    "_reconstruct",
    "_vec_string",
    "_ARRAY_API",
    "_monotonicity",
]