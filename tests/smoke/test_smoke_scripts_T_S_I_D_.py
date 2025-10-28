import importlib, types

def test_import_scripts_T_S_I_D_():
    mod = importlib.import_module("scripts.T_S_I_D_")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
