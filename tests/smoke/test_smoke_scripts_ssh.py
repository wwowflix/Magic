import importlib
import types


def test_import_scripts_ssh():
    mod = importlib.import_module("scripts.ssh")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
