import importlib, types


def test_import_scripts_key_actions():
    mod = importlib.import_module("scripts.key_actions")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
