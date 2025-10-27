import importlib, types

def test_import_scripts_pg():
    mod = importlib.import_module("scripts.pg")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
