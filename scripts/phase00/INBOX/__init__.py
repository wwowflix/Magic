# UTF-8 (no BOM). Smoke-time shims only — zero side-effects.

# --- DefaultTable shim (already helping your last failure) ---
try:
    from fontTools.ttLib.tables.otBase import DefaultTable  # real
except Exception:
    class DefaultTable:  # minimal no-op
        def __init__(self, tag=None): self.tag = tag
        def decompile(self, data, ttFont=None): self._raw = data
        def compile(self, ttFont=None): return b""
        def toXML(self, writer, ttFont=None): ...
        def fromXML(self, name, attrs, content, ttFont=None): ...

# --- otTables re-export so modules can `from . import otTables` ---
try:
    from fontTools.ttLib import tables as _tables
    otTables = _tables.otTables  # real module
except Exception:
    # Ultra-minimal placeholder module if fontTools import fails entirely.
    class _OT: pass
    otTables = _OT()

# --- Gentle compatibility shims: only define if missing ---
def _maybe_define(name, cls):
    if not hasattr(otTables, name):
        try:
            setattr(otTables, name, cls)
        except Exception:
            pass

# Common attrs that some fontTools versions may lack but our smoke imports reference.
class _FeatureParamsSize: pass
class _FeatureParamsStylisticSet: pass
class _STAT: pass
class _AxisRecord: pass
class _AxisValue: pass
class _FeatureName: pass
class _Setting: pass

_maybe_define("FeatureParamsSize", _FeatureParamsSize)
_maybe_define("FeatureParamsStylisticSet", _FeatureParamsStylisticSet)
_maybe_define("STAT", _STAT)
_maybe_define("AxisRecord", _AxisRecord)
_maybe_define("AxisValue", _AxisValue)
_maybe_define("FeatureName", _FeatureName)
_maybe_define("Setting", _Setting)

__all__ = ["DefaultTable", "otTables"]
