import importlib, types

def test_import_scripts_one_time_organizer():
    mod = importlib.import_module("scripts.one_time_organizer")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
