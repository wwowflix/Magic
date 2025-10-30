import importlib, types


def test_import_scripts_open_memory_channel():
    mod = importlib.import_module("scripts.open_memory_channel")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
