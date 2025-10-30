import importlib, types


def test_import_scripts_minidom():
    mod = importlib.import_module("scripts.minidom")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
