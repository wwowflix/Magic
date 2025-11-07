import importlib, types


def test_import_scripts_f90mod_rules():
    mod = importlib.import_module("scripts.f90mod_rules")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
