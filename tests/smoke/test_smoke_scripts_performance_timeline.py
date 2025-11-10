import importlib, types


def test_import_scripts_performance_timeline():
    mod = importlib.import_module("scripts.performance_timeline")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
