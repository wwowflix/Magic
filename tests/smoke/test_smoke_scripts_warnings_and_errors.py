import importlib
import types


def test_import_scripts_warnings_and_errors():
    mod = importlib.import_module("scripts.warnings_and_errors")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
