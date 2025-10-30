import importlib, types


def test_import_scripts_phase00_INBOX_sasreader_37DD0BBF_37DD0BBF():
    mod = importlib.import_module("scripts.phase00.INBOX.sasreader_37DD0BBF_37DD0BBF")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
