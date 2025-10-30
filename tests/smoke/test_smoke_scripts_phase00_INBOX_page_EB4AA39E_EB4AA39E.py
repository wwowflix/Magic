import importlib, types


def test_import_scripts_phase00_INBOX_page_EB4AA39E_EB4AA39E():
    mod = importlib.import_module("scripts.phase00.INBOX.page_EB4AA39E_EB4AA39E")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
