import importlib, types


def test_import_scripts_etree():
    mod = importlib.import_module("scripts.etree")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
