import importlib, types


def test_import_scripts_create_trends_table():
    mod = importlib.import_module("scripts.create_trends_table")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
