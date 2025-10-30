# --- MAGIC sitecustomize: lock real fontTools/ttLib before anything else ---
import sys
import os
import importlib
import importlib.util

try:
    _site = os.path.join(sys.prefix, "Lib", "site-packages")
    if _site not in sys.path:
        sys.path.insert(0, _site)

    # If base fontTools is a stub (no __path__), drop it
    m = sys.modules.get("fontTools")
    if m is not None and not hasattr(m, "__path__"):
        del sys.modules["fontTools"]

    # If ttLib is present but bogus (no __file__), drop it
    m = sys.modules.get("fontTools.ttLib")
    if m is not None and not getattr(m, "__file__", None):
        del sys.modules["fontTools.ttLib"]

    # Ensure real ttLib is loaded from disk
    _ttlib_init = os.path.join(_site, "fontTools", "ttLib", "__init__.py")
    if os.path.exists(_ttlib_init):
        spec = importlib.util.spec_from_file_location("fontTools.ttLib", _ttlib_init)
        mod = importlib.util.module_from_spec(spec)
        sys.modules["fontTools.ttLib"] = mod
        spec.loader.exec_module(mod)

    # Final sanity import
    from fontTools.ttLib import TTFont, newTable  # noqa: F401

    # Minimal shim for rare distros
    try:
        from fontTools.ttLib.tables import otTables as ot  # type: ignore

        if not hasattr(ot, "FeatureParamsCharacterVariants"):

            class FeatureParamsCharacterVariants:  # tiny no-op stub
                def __init__(self, *a, **k):
                    pass

            ot.FeatureParamsCharacterVariants = FeatureParamsCharacterVariants
    except Exception:
        pass

except Exception:
    # Never block Python start if anything goes wrong here
    pass
# --- end MAGIC sitecustomize ---
