import importlib, types

def test_import_tools_data_quality_schema_check():
    mod = importlib.import_module("tools.data_quality.schema_check")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
