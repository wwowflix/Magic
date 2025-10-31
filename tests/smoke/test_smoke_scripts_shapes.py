import importlib
import types


def test_import_scripts_shapes():
    mod = importlib.import_module("scripts.shapes")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
