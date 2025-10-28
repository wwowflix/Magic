import importlib, types

def test_import_scripts_action_chains():
    mod = importlib.import_module("scripts.action_chains")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
