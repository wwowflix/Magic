import importlib, types


def test_import_scripts_V_D_M_X_():
    mod = importlib.import_module("scripts.V_D_M_X_")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
