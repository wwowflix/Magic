import importlib, types

def test_import_scripts_keyword_deduper():
    mod = importlib.import_module("scripts.keyword_deduper")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
