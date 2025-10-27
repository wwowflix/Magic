import importlib, types

def test_import_scripts__a_n_k_r():
    mod = importlib.import_module("scripts._a_n_k_r")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
