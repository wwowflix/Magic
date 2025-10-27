import importlib, types

def test_import_scripts__generated_io_windows():
    mod = importlib.import_module("scripts._generated_io_windows")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
