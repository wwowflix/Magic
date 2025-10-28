import importlib, types

def test_import_scripts__s_b_i_x():
    mod = importlib.import_module("scripts._s_b_i_x")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
