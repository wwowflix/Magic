import importlib, types


def test_import_scripts_phase00_INBOX_filesize_F5F4CB00_F5F4CB00():
    mod = importlib.import_module("scripts.phase00.INBOX.filesize_F5F4CB00_F5F4CB00")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
