import importlib, types

def test_import_scripts_phase00_INBOX_psCharStrings_4DBE7E93_4DBE7E93():
    mod = importlib.import_module("scripts.phase00.INBOX.psCharStrings_4DBE7E93_4DBE7E93")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
