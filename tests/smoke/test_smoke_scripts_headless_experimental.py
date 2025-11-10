import importlib, types


def test_import_scripts_headless_experimental():
    mod = importlib.import_module("scripts.headless_experimental")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
