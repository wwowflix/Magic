import importlib, types


def test_import_scripts_encoding_test():
    mod = importlib.import_module("scripts.encoding_test")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
