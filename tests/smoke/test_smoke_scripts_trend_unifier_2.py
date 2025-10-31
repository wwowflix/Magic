import importlib
import types


def test_import_scripts_trend_unifier_2():
    mod = importlib.import_module("scripts.trend_unifier_2")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
