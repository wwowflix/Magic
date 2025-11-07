import importlib, types


def test_import_scripts_cli():
    mod = importlib.import_module("scripts.cli")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
