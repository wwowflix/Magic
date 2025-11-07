import importlib
import types


def test_import_scripts_poly1305():
    mod = importlib.import_module("scripts.poly1305")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
