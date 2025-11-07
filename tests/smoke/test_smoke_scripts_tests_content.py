import importlib
import types


def test_import_scripts_tests_content():
    mod = importlib.import_module("scripts.tests_content")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
