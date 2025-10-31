import importlib
import types


def test_import_scripts_results():
    mod = importlib.import_module("scripts.results")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
