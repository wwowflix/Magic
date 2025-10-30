import importlib, types


def test_import_scripts_f2py2e():
    mod = importlib.import_module("scripts.f2py2e")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
