import importlib, types

def test_import_scripts_seo_mapper():
    mod = importlib.import_module("scripts.seo_mapper")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
