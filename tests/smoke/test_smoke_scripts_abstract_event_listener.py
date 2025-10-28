import importlib, types

def test_import_scripts_abstract_event_listener():
    mod = importlib.import_module("scripts.abstract_event_listener")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
