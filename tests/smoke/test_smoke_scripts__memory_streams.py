import importlib, types


def test_import_scripts__memory_streams():
    mod = importlib.import_module("scripts._memory_streams")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
