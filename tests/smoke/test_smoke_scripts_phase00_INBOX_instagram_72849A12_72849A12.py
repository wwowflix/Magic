import importlib, types

def test_import_scripts_phase00_INBOX_instagram_72849A12_72849A12():
    mod = importlib.import_module("scripts.phase00.INBOX.instagram_72849A12_72849A12")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
