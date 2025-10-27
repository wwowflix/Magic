import importlib, types

def test_import_scripts_redis_cache():
    mod = importlib.import_module("scripts.redis_cache")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
