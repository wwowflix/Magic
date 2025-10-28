import importlib, types

def test_import_scripts_plugin_registry():
    mod = importlib.import_module("scripts.plugin_registry")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
