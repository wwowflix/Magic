import importlib, types

def test_import_scripts_nursery_start():
    mod = importlib.import_module("scripts.nursery_start")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
