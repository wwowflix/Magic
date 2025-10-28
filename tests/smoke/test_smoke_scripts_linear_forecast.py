import importlib, types

def test_import_scripts_linear_forecast():
    mod = importlib.import_module("scripts.linear_forecast")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
