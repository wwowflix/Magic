import importlib, types

def test_import_scripts_expected_conditions():
    mod = importlib.import_module("scripts.expected_conditions")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
