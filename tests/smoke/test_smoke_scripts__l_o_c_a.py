import importlib, types

def test_import_scripts__l_o_c_a():
    mod = importlib.import_module("scripts._l_o_c_a")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
