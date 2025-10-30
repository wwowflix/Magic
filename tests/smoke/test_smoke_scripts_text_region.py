import importlib, types


def test_import_scripts_text_region():
    mod = importlib.import_module("scripts.text_region")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
