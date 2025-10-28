import importlib, types

def test_import_scripts_text_file():
    mod = importlib.import_module("scripts.text_file")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
