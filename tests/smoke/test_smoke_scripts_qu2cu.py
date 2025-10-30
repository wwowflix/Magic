import importlib, types


def test_import_scripts_qu2cu():
    mod = importlib.import_module("scripts.qu2cu")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
