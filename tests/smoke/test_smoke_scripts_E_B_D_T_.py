import importlib, types


def test_import_scripts_E_B_D_T_():
    mod = importlib.import_module("scripts.E_B_D_T_")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
