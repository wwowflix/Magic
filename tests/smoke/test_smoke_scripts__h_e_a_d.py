import importlib, types

def test_import_scripts__h_e_a_d():
    mod = importlib.import_module("scripts._h_e_a_d")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
