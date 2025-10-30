# --- MAGIC shim: add missing FeatureParamsCharacterVariants if absent ---
import sys

try:
    import fontTools.ttLib.tables.otTables as ot

    if not hasattr(ot, "FeatureParamsCharacterVariants"):

        class FeatureParamsCharacterVariants:
            def __init__(self, *a, **kw):
                pass

        ot.FeatureParamsCharacterVariants = FeatureParamsCharacterVariants
        sys.modules["fontTools.ttLib.tables.otTables"] = ot
        print("✅ Injected missing FeatureParamsCharacterVariants into otTables")
    else:
        print("ℹ️  otTables.FeatureParamsCharacterVariants already present")
except Exception as e:
    print("⚠️  Failed to apply otTables shim:", e)
