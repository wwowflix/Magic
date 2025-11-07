import importlib
import types


def test_import_scripts_resultdict():
    mod = importlib.import_module("scripts.resultdict")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
