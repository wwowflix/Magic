import importlib, types


def test_import_scripts_phase00_INBOX_folder_cleanup_2_0F9A0C27_0F9A0C27():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.folder_cleanup_2_0F9A0C27_0F9A0C27"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
