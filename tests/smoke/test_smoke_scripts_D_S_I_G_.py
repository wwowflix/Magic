import importlib, types

def test_import_scripts_D_S_I_G_():
    mod = importlib.import_module("scripts.D_S_I_G_")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
