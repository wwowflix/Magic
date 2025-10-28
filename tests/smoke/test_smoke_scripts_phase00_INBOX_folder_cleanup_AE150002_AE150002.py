import importlib, types

def test_import_scripts_phase00_INBOX_folder_cleanup_AE150002_AE150002():
    mod = importlib.import_module("scripts.phase00.INBOX.folder_cleanup_AE150002_AE150002")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
