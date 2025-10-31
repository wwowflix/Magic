import importlib
import types


def test_import_scripts_plyparser():
    mod = importlib.import_module("scripts.plyparser")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
