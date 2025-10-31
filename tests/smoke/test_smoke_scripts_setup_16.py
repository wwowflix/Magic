import importlib
import types


def test_import_scripts_setup_16():
    mod = importlib.import_module("scripts.setup_16")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
