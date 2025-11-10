import importlib
import types


def test_import_scripts_range():
    mod = importlib.import_module("scripts.range")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
