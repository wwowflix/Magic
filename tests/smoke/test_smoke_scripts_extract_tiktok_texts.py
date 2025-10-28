import importlib, types

def test_import_scripts_extract_tiktok_texts():
    mod = importlib.import_module("scripts.extract_tiktok_texts")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
