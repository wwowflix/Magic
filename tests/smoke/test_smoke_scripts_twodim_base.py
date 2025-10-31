import importlib
import types


def test_import_scripts_twodim_base():
    mod = importlib.import_module("scripts.twodim_base")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
