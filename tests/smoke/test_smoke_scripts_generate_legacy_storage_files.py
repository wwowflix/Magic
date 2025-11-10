import importlib, types


def test_import_scripts_generate_legacy_storage_files():
    mod = importlib.import_module("scripts.generate_legacy_storage_files")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
