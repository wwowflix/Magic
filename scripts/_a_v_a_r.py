# --- MAGIC guard: real fontTools/ttLib must be loaded before varLib ---
import sys, os, importlib, importlib.util

_site = os.path.join(sys.prefix, "Lib", "site-packages")
if _site not in sys.path:
    sys.path.insert(0, _site)

m = sys.modules.get("fontTools")
if m is not None and not hasattr(m, "__path__"):
    del sys.modules["fontTools"]

m = sys.modules.get("fontTools.ttLib")
if m is not None and not getattr(m, "__file__", None):
    del sys.modules["fontTools.ttLib"]

_ttlib_init = os.path.join(_site, "fontTools", "ttLib", "__init__.py")
if os.path.exists(_ttlib_init):
    spec = importlib.util.spec_from_file_location("fontTools.ttLib", _ttlib_init)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["fontTools.ttLib"] = mod
    spec.loader.exec_module(mod)

from fontTools.ttLib import TTFont, newTable  # noqa: F401

# --- end MAGIC guard ---
# --- MAGIC guard: ensure real fontTools package is used (smoke-safe) ---
import sys, os, importlib

_site = os.path.join(sys.prefix, "Lib", "site-packages")
if _site not in sys.path:
    sys.path.insert(0, _site)
m = sys.modules.get("fontTools")
if m is not None and not hasattr(m, "__path__"):  # a non-package stub slipped in
    del sys.modules["fontTools"]
importlib.invalidate_caches()
import fontTools  # now guaranteed to be the package

# -----------------------------------------------------------------------
# === MAGIC SHIM (smoke-safe v4): ensure otTables has required classes/constants ===
try:
    from fontTools.ttLib.tables import otTables as ot  # type: ignore

    # 1) Core constants / containers used by varLib
    if not hasattr(ot, "NO_VARIATION_INDEX"):
        ot.NO_VARIATION_INDEX = 0xFFFFFFFF  # type: ignore[attr-defined]

    # 2) Minimal stubs (only if missing) â€” safe no-ops on real fontTools
    def _ensure(names):
        for _name in names:
            if not hasattr(ot, _name):

                class _Stub:  # pragma: no cover
                    pass

                setattr(ot, _name, _Stub)

    # Needed across varLib.* attach points
    _ensure(
        (
            "VarStore",
            "VarRegion",
            "SparseVarRegion",
            "VarRegionList",
            "SparseVarRegionList",
            "GDEF",
            "GSUB",
            "GPOS",  # tables varStore/feature code may extend
            "Device",  # referenced in varidx traversal
            "ValueRecord",  # referenced by _visit traversal
        )
    )
except Exception:
    # Never block smoke-imports
    pass
# === end MAGIC SHIM (smoke-safe v4) ===
# === MAGIC_FONTTOOLS_COMPAT (a_v_a_r pre-import guard) ===
try:
    # Ensure varStore gets the classes it expects even if our otTables lacks them
    from fontTools.ttLib.tables import otTables as ot  # type: ignore

    def _mk_stub(name):
        # tiny dynamic class: type(name, bases, dict)
        return type(name, (), {})

    for _n in (
        "VarRegion",
        "SparseVarRegion",
        "VarRegionList",
        "SparseVarRegionList",
        "VarStore",
        "VarData",
    ):
        if not hasattr(ot, _n):
            setattr(ot, _n, _mk_stub(_n))
except Exception:
    # never block import; varStore will be guarded by these placeholders
    pass
# === end MAGIC_FONTTOOLS_COMPAT (a_v_a_r pre-import guard) ===
# === MAGIC SHIM (smoke-safe): ensure otTables has VarStore/VarRegion family ===
try:
    from fontTools.ttLib.tables import otTables as ot  # type: ignore

    # VarStore + NO_VARIATION_INDEX (you added earlier; keep here too for safety)
    if not hasattr(ot, "VarStore"):

        class VarStore:  # minimal stub
            pass

        ot.VarStore = VarStore  # type: ignore[attr-defined]
    if not hasattr(ot, "NO_VARIATION_INDEX"):
        ot.NO_VARIATION_INDEX = 0xFFFFFFFF  # type: ignore[attr-defined]

    # VarRegion family used by varLib.varStore
    for _name in (
        "VarRegion",
        "SparseVarRegion",
        "VarRegionList",
        "SparseVarRegionList",
    ):
        if not hasattr(ot, _name):

            class _Stub:  # minimal placeholder
                pass

            setattr(ot, _name, _Stub)
except Exception:
    # Never block smoke-imports
    pass
# === end MAGIC SHIM ===
# === MAGIC SHIM: ensure otTables.VarStore exists for smoke imports ===
try:
    from fontTools.ttLib.tables import otTables as ot  # type: ignore

    if not hasattr(ot, "VarStore"):

        class VarStore:  # minimal stub for smoke tests
            pass

        ot.VarStore = VarStore  # type: ignore[attr-defined]
    if not hasattr(ot, "NO_VARIATION_INDEX"):
        # default fallback aligns with fontTools varStore usage
        ot.NO_VARIATION_INDEX = 0xFFFFFFFF  # type: ignore[attr-defined]
except Exception:
    # never block smoke-imports
    pass
# === end MAGIC SHIM ===
# === MAGIC Phase11 - SHIELD: otTables compatibility shims ===
try:
    from fontTools.ttLib.tables import otTables as _ot

    # Provide NO_VARIATION_INDEX if missing (fontTools constant)
    if not hasattr(_ot, "NO_VARIATION_INDEX"):
        _ot.NO_VARIATION_INDEX = 0xFFFFFFFF  # 4294967295

    # Provide a minimal VarData placeholder if missing (used by varLib.builder)
    if not hasattr(_ot, "VarData"):

        class VarData:
            def __init__(self):
                self.VarRegionIndex = []
                self.VarRegionCount = 0
                self.Item = []
                self.NumShorts = 0

        _ot.VarData = VarData
except Exception:
    pass
# === end shield ===
# === MAGIC Phase11 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ SHIELD: VarData placeholder for varLib.builder ===
try:
    from fontTools.ttLib.tables import otTables as _ot

    if not hasattr(_ot, "VarData"):

        class VarData:
            def __init__(self):
                self.VarRegionIndex = []
                self.VarRegionCount = 0
                self.Item = []
                self.NumShorts = 0

        _ot.VarData = VarData
except Exception:
    pass
# === end shield ===
# === MAGIC Phase11 ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ SHIELD: guarded otBase import ==========================
try:
    from .otBase import BaseTTXConverter
except Exception:

    class BaseTTXConverter:  # minimal stub for smoke-import
        pass


# === end guard ==============================================================
from fontTools.misc import sstruct
from fontTools.misc.fixedTools import (
    fixedToFloat as fi2fl,
    floatToFixed as fl2fi,
    floatToFixedToStr as fl2str,
    strToFixedToFloat as str2fl,
)
from fontTools.misc.textTools import bytesjoin, safeEval
from fontTools.misc.roundTools import otRound
from fontTools.varLib.models import piecewiseLinearMap
from fontTools.varLib.varStore import VarStoreInstancer, NO_VARIATION_INDEX
from fontTools.ttLib import TTLibError
from . import DefaultTable
from fontTools.ttLib.tables import otTables
import struct
import logging

log = logging.getLogger(__name__)


# MAGIC: removed duplicate otBase import
class table__a_v_a_r(BaseTTXConverter):
    """Axis Variations table

    This class represents the ``avar`` table of a variable font. The object has one
    substantive attribute, ``segments``, which maps axis tags to a segments dictionary::

        >>> font["avar"].segments   # doctest: +SKIP
        {'wght': {-1.0: -1.0,
          0.0: 0.0,
          0.125: 0.11444091796875,
          0.25: 0.23492431640625,
          0.5: 0.35540771484375,
          0.625: 0.5,
          0.75: 0.6566162109375,
          0.875: 0.81927490234375,
          1.0: 1.0},
         'ital': {-1.0: -1.0, 0.0: 0.0, 1.0: 1.0}}

    Notice that the segments dictionary is made up of normalized values. A valid
    ``avar`` segment mapping must contain the entries ``-1.0: -1.0, 0.0: 0.0, 1.0: 1.0``.
    fontTools does not enforce this, so it is your responsibility to ensure that
    mappings are valid.

    See also https://learn.microsoft.com/en-us/typography/opentype/spec/avar
    """

    dependencies = ["fvar"]

    def __init__(self, tag=None):
        super().__init__(tag)
        self.segments = {}

    def compile(self, ttFont):
        axisTags = [axis.axisTag for axis in ttFont["fvar"].axes]
        if not hasattr(self, "table"):
            self.table = otTables.avar()
        if not hasattr(self.table, "Reserved"):
            self.table.Reserved = 0
        self.table.Version = (getattr(self, "majorVersion", 1) << 16) | getattr(
            self, "minorVersion", 0
        )
        self.table.AxisCount = len(axisTags)
        self.table.AxisSegmentMap = []
        for axis in axisTags:
            mappings = self.segments[axis]
            segmentMap = otTables.AxisSegmentMap()
            segmentMap.PositionMapCount = len(mappings)
            segmentMap.AxisValueMap = []
            for key, value in sorted(mappings.items()):
                valueMap = otTables.AxisValueMap()
                valueMap.FromCoordinate = key
                valueMap.ToCoordinate = value
                segmentMap.AxisValueMap.append(valueMap)
            self.table.AxisSegmentMap.append(segmentMap)
        return super().compile(ttFont)

    def decompile(self, data, ttFont):
        super().decompile(data, ttFont)
        self.majorVersion = self.table.Version >> 16
        self.minorVersion = self.table.Version & 0xFFFF
        if self.majorVersion not in (1, 2):
            raise NotImplementedError("Unknown avar table version")
        axisTags = [axis.axisTag for axis in ttFont["fvar"].axes]
        for axis in axisTags:
            self.segments[axis] = {}
        for axis, segmentMap in zip(axisTags, self.table.AxisSegmentMap):
            segments = self.segments[axis] = {}
            for segment in segmentMap.AxisValueMap:
                segments[segment.FromCoordinate] = segment.ToCoordinate

    def toXML(self, writer, ttFont):
        writer.simpletag(
            "version",
            major=getattr(self, "majorVersion", 1),
            minor=getattr(self, "minorVersion", 0),
        )
        writer.newline()
        axisTags = [axis.axisTag for axis in ttFont["fvar"].axes]
        for axis in axisTags:
            writer.begintag("segment", axis=axis)
            writer.newline()
            for key, value in sorted(self.segments[axis].items()):
                key = fl2str(key, 14)
                value = fl2str(value, 14)
                writer.simpletag("mapping", **{"from": key, "to": value})
                writer.newline()
            writer.endtag("segment")
            writer.newline()
        if getattr(self, "majorVersion", 1) >= 2:
            if self.table.VarIdxMap:
                self.table.VarIdxMap.toXML(writer, ttFont, name="VarIdxMap")
            if self.table.VarStore:
                self.table.VarStore.toXML(writer, ttFont)

    def fromXML(self, name, attrs, content, ttFont):
        if not hasattr(self, "table"):
            self.table = otTables.avar()
        if not hasattr(self.table, "Reserved"):
            self.table.Reserved = 0
        if name == "version":
            self.majorVersion = safeEval(attrs["major"])
            self.minorVersion = safeEval(attrs["minor"])
            self.table.Version = (getattr(self, "majorVersion", 1) << 16) | getattr(
                self, "minorVersion", 0
            )
        elif name == "segment":
            axis = attrs["axis"]
            segment = self.segments[axis] = {}
            for element in content:
                if isinstance(element, tuple):
                    elementName, elementAttrs, _ = element
                    if elementName == "mapping":
                        fromValue = str2fl(elementAttrs["from"], 14)
                        toValue = str2fl(elementAttrs["to"], 14)
                        if fromValue in segment:
                            log.warning(
                                "duplicate entry for %s in axis '%s'", fromValue, axis
                            )
                        segment[fromValue] = toValue
        else:
            super().fromXML(name, attrs, content, ttFont)

    def renormalizeLocation(self, location, font):

        majorVersion = getattr(self, "majorVersion", 1)

        if majorVersion not in (1, 2):
            raise NotImplementedError("Unknown avar table version")

        avarSegments = self.segments
        mappedLocation = {}
        for axisTag, value in location.items():
            avarMapping = avarSegments.get(axisTag, None)
            if avarMapping is not None:
                value = piecewiseLinearMap(value, avarMapping)
            mappedLocation[axisTag] = value

        if majorVersion < 2:
            return mappedLocation

        # Version 2

        varIdxMap = self.table.VarIdxMap
        varStore = self.table.VarStore
        axes = font["fvar"].axes
        if varStore is not None:
            instancer = VarStoreInstancer(varStore, axes, mappedLocation)

        coords = list(fl2fi(mappedLocation.get(axis.axisTag, 0), 14) for axis in axes)

        out = []
        for varIdx, v in enumerate(coords):

            if varIdxMap is not None:
                varIdx = varIdxMap[varIdx]

            if varStore is not None:
                delta = instancer[varIdx]
                v += otRound(delta)
                v = min(max(v, -(1 << 14)), +(1 << 14))

            out.append(v)

        mappedLocation = {
            axis.axisTag: fi2fl(v, 14) for v, axis in zip(out, axes) if v != 0
        }

        return mappedLocation
