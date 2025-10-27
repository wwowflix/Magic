import importlib, types

def test_import_scripts_phase00_INBOX_fontBuilder_C85DBE21_C85DBE21():
    mod = importlib.import_module("scripts.phase00.INBOX.fontBuilder_C85DBE21_C85DBE21")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
