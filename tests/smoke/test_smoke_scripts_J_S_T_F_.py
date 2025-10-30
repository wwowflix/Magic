import importlib, types


def test_import_scripts_J_S_T_F_():
    mod = importlib.import_module("scripts.J_S_T_F_")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
