import importlib
import types


def test_import_scripts_sbcsgroupprober():
    mod = importlib.import_module("scripts.sbcsgroupprober")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
