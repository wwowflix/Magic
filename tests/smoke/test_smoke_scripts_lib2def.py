import importlib, types


def test_import_scripts_lib2def():
    mod = importlib.import_module("scripts.lib2def")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
