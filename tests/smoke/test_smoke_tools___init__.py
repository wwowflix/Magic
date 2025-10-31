import importlib
import types


def test_import_tools___init__():
    mod = importlib.import_module("tools.__init__")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
