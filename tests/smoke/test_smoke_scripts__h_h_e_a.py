import importlib, types

def test_import_scripts__h_h_e_a():
    mod = importlib.import_module("scripts._h_h_e_a")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
