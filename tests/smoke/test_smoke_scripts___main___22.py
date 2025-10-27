import importlib, types

def test_import_scripts___main___22():
    mod = importlib.import_module("scripts.__main___22")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
