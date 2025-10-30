import importlib, types


def test_import_scripts_cache_mapper():
    mod = importlib.import_module("scripts.cache_mapper")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
