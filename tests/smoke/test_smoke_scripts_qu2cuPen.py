import importlib
import types


def test_import_scripts_qu2cuPen():
    mod = importlib.import_module("scripts.qu2cuPen")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
