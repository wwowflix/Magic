import importlib, types

def test_import_scripts__g_c_i_d():
    mod = importlib.import_module("scripts._g_c_i_d")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
