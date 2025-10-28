import importlib, types

def test_import_scripts_mips():
    mod = importlib.import_module("scripts.mips")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
