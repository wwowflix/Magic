import importlib, types


def test_import_scripts_phase00_INBOX_text_file_1706E776_1706E776():
    mod = importlib.import_module("scripts.phase00.INBOX.text_file_1706E776_1706E776")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
