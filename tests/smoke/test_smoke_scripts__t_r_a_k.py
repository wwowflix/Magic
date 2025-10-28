import importlib, types

def test_import_scripts__t_r_a_k():
    mod = importlib.import_module("scripts._t_r_a_k")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
