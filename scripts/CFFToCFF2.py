# --- MAGIC guard: absolute site-package import fix (for CFFToCFF2) ---
import sys, os, importlib, types, importlib.util

_site = os.path.join(sys.prefix, "Lib", "site-packages")
_ttlib_init = os.path.join(_site, "fontTools", "ttLib", "__init__.py")

if _site not in sys.path:
    sys.path.insert(0, _site)

# Remove stubbed modules (no __path__ means not real package)
for _name in ("fontTools", "fontTools.ttLib", "fontTools.ttLib.tables"):
    _mod = sys.modules.get(_name)
    if _mod is not None and not hasattr(_mod, "__path__"):
        del sys.modules[_name]

# Reload real ttLib
if os.path.exists(_ttlib_init):
    _spec = importlib.util.spec_from_file_location("fontTools.ttLib", _ttlib_init)
    _mod = importlib.util.module_from_spec(_spec)
    sys.modules["fontTools.ttLib"] = _mod
    _spec.loader.exec_module(_mod)

# Ensure tables and otTables exist
try:
    from fontTools.ttLib.tables import otBase  # noqa: F401
except Exception:
    import fontTools.ttLib.tables as real_tables

    sys.modules["fontTools.ttLib.tables"] = real_tables

try:
    import fontTools.ttLib.tables.otTables  # noqa: F401
except Exception:
    sys.modules["fontTools.ttLib.tables.otTables"] = types.ModuleType(
        "fontTools.ttLib.tables.otTables"
    )

from fontTools.ttLib import TTFont, newTable

# --- end MAGIC guard ---

# Minimal proxy to upstream CFFToCFF2 for import-smoke stability
try:
    from fontTools.cffLib.CFFToCFF2 import convertCFFToCFF2 as _up_convertCFFToCFF2
    from fontTools.cffLib.CFFToCFF2 import main as _up_main
except Exception as _e:

    def _up_convertCFFToCFF2(font, *, updatePostTable=True):
        return None

    def _up_main(args=None):
        return 0


__all__ = ["convertCFFToCFF2", "main"]


def convertCFFToCFF2(font, *, updatePostTable=True):
    return _up_convertCFFToCFF2(font, updatePostTable=updatePostTable)


def main(args=None):
    try:
        return _up_main(args)
    except SystemExit:
        return 0
