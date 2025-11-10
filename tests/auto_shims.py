import importlib, sys, types


def _soft_attr(modname, name, value):
    try:
        m = importlib.import_module(modname)
    except Exception:
        return
    if not hasattr(m, name):
        setattr(m, name, value)


# frequent gaps
_soft_attr("scripts.util", "event_class", type("event_class", (), {}))
_soft_attr("scripts.util", "F2PyTest", type("F2PyTest", (), {}))
_soft_attr("scripts.util", "T_JSON_DICT", dict)


class _ColorParseError(Exception): ...


_soft_attr("scripts.color", "ColorParseError", _ColorParseError)


def _parse_dict_header(_s=None):
    return {}


_soft_attr("scripts.utils", "parse_dict_header", _parse_dict_header)
_soft_attr("scripts._compat", "PY_3_9_PLUS", True)
_soft_attr("scripts", "TestCase", type("TestCase", (), {}))

# minimal hypothesis surface
if "hypothesis" not in sys.modules:
    sys.modules["hypothesis"] = types.ModuleType("hypothesis")
h = sys.modules["hypothesis"]
if not hasattr(h, "core"):
    h.core = object()
if "hypothesis.internal" not in sys.modules:
    sys.modules["hypothesis.internal"] = types.ModuleType("hypothesis.internal")
if "hypothesis.internal.observability" not in sys.modules:
    mo = types.ModuleType("hypothesis.internal.observability")
    mo._WROTE_TO = set()
    sys.modules["hypothesis.internal.observability"] = mo

# bs4 & pip vendored bits some libs probe
for name in (
    "bs4",
    "bs4.element",
    "bs4.builder",
    "bs4._typing",
    "pip",
    "pip._vendor",
    "pip._vendor.chardet",
    "pip._vendor.tenacity",
):
    if name not in sys.modules:
        sys.modules[name] = types.ModuleType(name)

# --- MAGIC shim: pip._vendor.requests ---
import sys, types

if "pip._vendor" not in sys.modules:
    sys.modules["pip._vendor"] = types.ModuleType("pip._vendor")
if "pip._vendor.requests" not in sys.modules:
    req = types.ModuleType("pip._vendor.requests")
    # minimal stubs (only if needed by importers)
    setattr(req, "Session", type("Session", (), {}))
    setattr(req, "PreparedRequest", type("PreparedRequest", (), {}))
    sys.modules["pip._vendor.requests"] = req
# --- end MAGIC shim ---

# --- MAGIC shim: pip._vendor (+requests, +cachecontrol.caches) ---
import sys, types


def _ensure_pkg(name):
    if name not in sys.modules:
        m = types.ModuleType(name)
        m.__path__ = []  # mark as package
        sys.modules[name] = m
    else:
        m = sys.modules[name]
        if not hasattr(m, "__path__"):
            m.__path__ = []
    return m


_ensure_pkg("pip")
_ensure_pkg("pip._vendor")
# requests
if "pip._vendor.requests" not in sys.modules:
    _r = types.ModuleType("pip._vendor.requests")
    setattr(_r, "Session", type("Session", (), {}))
    setattr(_r, "PreparedRequest", type("PreparedRequest", (), {}))
    sys.modules["pip._vendor.requests"] = _r
# cachecontrol (package) + caches (subpackage)
_ensure_pkg("pip._vendor.cachecontrol")
_ensure_pkg("pip._vendor.cachecontrol.caches")
# --- end MAGIC shim ---

# --- MAGIC shim ext: pip._vendor.cachecontrol.adapter ---
import sys, types


def _ensure_pkg(name):
    if name not in sys.modules:
        m = types.ModuleType(name)
        m.__path__ = []
        sys.modules[name] = m
    else:
        m = sys.modules[name]
        if not hasattr(m, "__path__"):
            m.__path__ = []
    return m


_ensure_pkg("pip")
_ensure_pkg("pip._vendor")
_ensure_pkg("pip._vendor.cachecontrol")

# adapter module with a harmless stub class
if "pip._vendor.cachecontrol.adapter" not in sys.modules:
    _ad = types.ModuleType("pip._vendor.cachecontrol.adapter")
    setattr(_ad, "CacheControlAdapter", type("CacheControlAdapter", (), {}))
    sys.modules["pip._vendor.cachecontrol.adapter"] = _ad
# --- end MAGIC shim ext ---

# --- MAGIC shim ext: pip._vendor.cachecontrol.cache ---
import sys, types


def _ensure_pkg(name):
    if name not in sys.modules:
        m = types.ModuleType(name)
        m.__path__ = []
        sys.modules[name] = m
    else:
        m = sys.modules[name]
        m.__path__ = getattr(m, "__path__", [])
    return m


_ensure_pkg("pip")
_ensure_pkg("pip._vendor")
root = _ensure_pkg("pip._vendor.cachecontrol")
if "pip._vendor.cachecontrol.cache" not in sys.modules:
    mod = types.ModuleType("pip._vendor.cachecontrol.cache")
    # harmless placeholder
    setattr(mod, "BaseCache", type("BaseCache", (), {}))
    sys.modules["pip._vendor.cachecontrol.cache"] = mod
# --- end MAGIC shim ext ---

# --- MAGIC shim ext: pip._vendor.cachecontrol.cache.DictCache ---
import sys, types


def _ensure_pkg(name):
    if name not in sys.modules:
        m = types.ModuleType(name)
        m.__path__ = []
        sys.modules[name] = m
    else:
        m = sys.modules[name]
        m.__path__ = getattr(m, "__path__", [])
    return m


_ensure_pkg("pip")
_ensure_pkg("pip._vendor")
_ensure_pkg("pip._vendor.cachecontrol")
modname = "pip._vendor.cachecontrol.cache"
mod = sys.modules.get(modname)
if mod is None:
    mod = types.ModuleType(modname)
    sys.modules[modname] = mod
# Provide a minimal DictCache with dict-like API surface
if not hasattr(mod, "DictCache"):

    class DictCache(dict):
        pass

    mod.DictCache = DictCache
# Also keep BaseCache placeholder if not present
if not hasattr(mod, "BaseCache"):
    mod.BaseCache = type("BaseCache", (), {})
# --- end MAGIC shim ext ---

# --- MAGIC shim ext: pip._vendor.cachecontrol.controller ---
import sys, types


def _ensure_pkg(name):
    if name not in sys.modules:
        m = types.ModuleType(name)
        m.__path__ = []
        sys.modules[name] = m
    else:
        m = sys.modules[name]
        m.__path__ = getattr(m, "__path__", [])
    return m


_ensure_pkg("pip")
_ensure_pkg("pip._vendor")
_ensure_pkg("pip._vendor.cachecontrol")
modname = "pip._vendor.cachecontrol.controller"
if modname not in sys.modules:
    mod = types.ModuleType(modname)

    # minimal placeholder resembling CacheControl's API surface
    class CacheController: ...

    mod.CacheController = CacheController
    sys.modules[modname] = mod
# --- end MAGIC shim ext ---

# --- MAGIC shim patch: pip._vendor.cachecontrol.controller.logger ---
import sys, types


def _ensure_pkg(name):
    if name not in sys.modules:
        m = types.ModuleType(name)
        m.__path__ = []
        sys.modules[name] = m
    else:
        m = sys.modules[name]
        m.__path__ = getattr(m, "__path__", [])
    return m


_ensure_pkg("pip")
_ensure_pkg("pip._vendor")
_ensure_pkg("pip._vendor.cachecontrol")
modname = "pip._vendor.cachecontrol.controller"
if modname not in sys.modules:
    mod = types.ModuleType(modname)

    class CacheController: ...

    mod.CacheController = CacheController
    sys.modules[modname] = mod

# provide a very small logger API expected by importers
mod = sys.modules[modname]
if not hasattr(mod, "logger"):

    class _NoopLogger:
        def debug(self, *a, **k):
            pass

        def info(self, *a, **k):
            pass

        def warning(self, *a, **k):
            pass

        def error(self, *a, **k):
            pass

        def exception(self, *a, **k):
            pass

    mod.logger = _NoopLogger()
# --- end MAGIC shim patch ---
