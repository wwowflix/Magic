import importlib, types


def test_import_scripts_indexed_db():
    mod = importlib.import_module("scripts.indexed_db")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
