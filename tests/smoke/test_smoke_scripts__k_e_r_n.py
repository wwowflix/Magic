import importlib, types

def test_import_scripts__k_e_r_n():
    mod = importlib.import_module("scripts._k_e_r_n")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
