import importlib, types

def test_import_tools_data_integrity_check_data():
    mod = importlib.import_module("tools.data_integrity.check_data")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
