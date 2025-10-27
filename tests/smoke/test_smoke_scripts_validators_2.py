import importlib, types

def test_import_scripts_validators_2():
    mod = importlib.import_module("scripts.validators_2")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
