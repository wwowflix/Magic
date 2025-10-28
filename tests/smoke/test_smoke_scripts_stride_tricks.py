import importlib, types

def test_import_scripts_stride_tricks():
    mod = importlib.import_module("scripts.stride_tricks")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
