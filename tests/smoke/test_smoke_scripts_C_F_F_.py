import importlib, types


def test_import_scripts_C_F_F_():
    mod = importlib.import_module("scripts.C_F_F_")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
