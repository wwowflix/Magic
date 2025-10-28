import importlib, types

def test_import_scripts_dataframe_protocol():
    mod = importlib.import_module("scripts.dataframe_protocol")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
