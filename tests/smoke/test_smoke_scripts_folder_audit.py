import importlib, types


def test_import_scripts_folder_audit():
    mod = importlib.import_module("scripts.folder_audit")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
