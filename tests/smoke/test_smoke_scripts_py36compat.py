import importlib
import types


def test_import_scripts_py36compat():
    mod = importlib.import_module("scripts.py36compat")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
