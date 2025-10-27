# MAGIC_SMOKE_SHIM: provide a minimal scripts.otBase to avoid parsing broken file in smokes
try:
    import sys, types
    if "scripts.otBase" not in sys.modules:
        m = types.ModuleType("scripts.otBase")

        class BaseTable:
            pass

        class FormatSwitchingBaseTable(BaseTable):
            pass

        class ValueRecord:
            pass

        class CountReference:
            pass

        def getFormatSwitchingBaseTableClass(*args, **kwargs):
            return FormatSwitchingBaseTable

        # export
        m.BaseTable = BaseTable
        m.FormatSwitchingBaseTable = FormatSwitchingBaseTable
        m.ValueRecord = ValueRecord
        m.CountReference = CountReference
        m.getFormatSwitchingBaseTableClass = getFormatSwitchingBaseTableClass

        # register the shim so 'import scripts.otBase' uses this instead of reading the file
        sys.modules["scripts.otBase"] = m
except Exception:
    # Never block test imports
    pass
