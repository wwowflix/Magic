from __future__ import annotations

# --- MAGIC compat shims (PY_3_XX_PLUS) [hard] ---
try:
    import sys as _sys

    _v = _sys.version_info
    PY_3_10_PLUS = (_v.major, _v.minor) >= (3, 10)
    PY_3_11_PLUS = (_v.major, _v.minor) >= (3, 11)
    PY_3_13_PLUS = (_v.major, _v.minor) >= (3, 13)
except Exception:
    PY_3_10_PLUS = False
    PY_3_11_PLUS = False
    PY_3_13_PLUS = False
# --- end MAGIC compat shims (PY_3_XX_PLUS) [hard] ---

# --- MAGIC compat shim (_NonClosingTextIOWrapper) [hard] ---
try:
    import io as _io
except Exception:
    _io = None

_Base = getattr(_io, "TextIOWrapper", object)


class _NonClosingTextIOWrapper(_Base):
    # Do not close the underlying buffer; just flush if possible.
    def close(self):
        try:
            flush = getattr(super(), "flush", None)
            if callable(flush):
                flush()
        except Exception:
            pass
        # Intentionally do NOT call super().close()


# --- end MAGIC compat shim (_NonClosingTextIOWrapper) [hard] ---

# --- MAGIC clean __all__ ensure ---
try:
    __all__
except NameError:
    __all__ = []


def _ensure_in_all(*names):
    for _n in names:
        if _n not in __all__:
            __all__.append(_n)


# --- end MAGIC clean __all__ ensure ---

_ensure_in_all(
    "PY_3_10_PLUS", "PY_3_11_PLUS", "PY_3_13_PLUS", "_NonClosingTextIOWrapper"
)

# --- MAGIC compat shims (annotation helpers) ---
import typing as _t
import inspect as _i


def _get_annotations(obj):
    try:
        mod = _i.getmodule(obj)
        gns = getattr(mod, "__dict__", None)
        try:
            return _t.get_type_hints(
                obj, globalns=gns, localns=None, include_extras=True
            )
        except TypeError:
            return _t.get_type_hints(obj, globalns=gns, localns=None)
    except Exception:
        return getattr(obj, "__annotations__", {}) or {}


class _AnnotationExtractor:
    def __init__(self, obj):
        self._ann = _get_annotations(obj)

    @property
    def annotations(self):
        return dict(self._ann)

    def for_param(self, name, default=_t.Any):
        return self._ann.get(name, default)


def get_generic_base(tp):
    try:
        origin = _t.get_origin(tp)
        if origin is not None:
            return origin
    except Exception:
        pass
    return tp if isinstance(tp, type) else type(tp)


# --- end MAGIC compat shims (annotation helpers) ---


# --- MAGIC compat shim (wrap_spec) [hard] ---
def wrap_spec(obj, name=None, origin=None, is_package=False):
    try:
        import importlib.machinery as _machinery
    except Exception:
        _machinery = None
    # Already a spec? (duck test)
    try:
        if hasattr(obj, "loader") and hasattr(obj, "name"):
            return obj
    except Exception:
        pass
    # Build a spec from loader+name
    if _machinery is not None and name is not None:
        try:
            spec = _machinery.ModuleSpec(name=name, loader=obj, origin=origin)
            if is_package:
                try:
                    spec.submodule_search_locations = []
                except Exception:
                    pass
            return spec
        except Exception:
            pass
    # Fallback passthrough
    return obj


# --- end MAGIC compat shim (wrap_spec) [hard] ---

_ensure_in_all("wrap_spec")
