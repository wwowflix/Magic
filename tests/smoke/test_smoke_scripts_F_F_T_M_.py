import importlib, types


def test_import_scripts_F_F_T_M_():
    mod = importlib.import_module("scripts.F_F_T_M_")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
