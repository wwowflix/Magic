import importlib, types


def test_import_scripts_file_system():
    mod = importlib.import_module("scripts.file_system")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
