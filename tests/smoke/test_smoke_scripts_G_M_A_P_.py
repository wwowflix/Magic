import importlib, types

def test_import_scripts_G_M_A_P_():
    mod = importlib.import_module("scripts.G_M_A_P_")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
