# scripts/compat/np.py â€” central NumPy shim (public-only)
import importlib

try:
    import numpy as _np
    from numpy import array, asanyarray, asarray
except Exception:
    _np = None

    def array(x, *a, **k):
        return x

    def asanyarray(x, *a, **k):
        return x

    def asarray(x, *a, **k):
        return x


try:
    from numpy.core._multiarray_umath import (
        add_docstring as _add_docstring,
        implement_array_function as _implement_array_function,
        _get_implementing_args as _get_implementing_args_impl,
    )
except Exception:

    def _add_docstring(obj, doc):
        return obj

    def _implement_array_function(*_a, **_k):
        def _decorator(f):
            return f

        return _decorator

    def _get_implementing_args_impl(args):
        return ()


add_docstring = _add_docstring
implement_array_function = _implement_array_function
_get_implementing_args = _get_implementing_args_impl


def safe_add_newdoc(place, obj, doc):
    try:
        try:
            from numpy._core.function_base import add_newdoc as _np_add_newdoc
        except Exception:
            from numpy.core.function_base import add_newdoc as _np_add_newdoc
    except Exception:
        return
    try:
        mod = importlib.import_module(place)
        if not hasattr(mod, obj):
            return
        _np_add_newdoc(place, obj, doc)
    except Exception:
        pass


try:
    scalar = _np.generic
except Exception:

    class scalar: ...
