import importlib
import types


def test_import_scripts_validators_4():
    mod = importlib.import_module("scripts.validators_4")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
