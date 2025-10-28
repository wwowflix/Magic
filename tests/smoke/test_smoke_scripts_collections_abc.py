import importlib, types

def test_import_scripts_collections_abc():
    mod = importlib.import_module("scripts.collections_abc")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
