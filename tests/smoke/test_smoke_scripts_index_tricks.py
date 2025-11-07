import importlib, types


def test_import_scripts_index_tricks():
    mod = importlib.import_module("scripts.index_tricks")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
