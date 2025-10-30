import importlib, types


def test_import_scripts_generate_numpy_api():
    mod = importlib.import_module("scripts.generate_numpy_api")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
