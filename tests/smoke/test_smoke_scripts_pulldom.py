import importlib, types


def test_import_scripts_pulldom():
    mod = importlib.import_module("scripts.pulldom")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
