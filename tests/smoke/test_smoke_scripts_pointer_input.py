import importlib
import types


def test_import_scripts_pointer_input():
    mod = importlib.import_module("scripts.pointer_input")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
