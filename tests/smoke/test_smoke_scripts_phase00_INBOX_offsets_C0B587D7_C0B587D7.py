import importlib, types

def test_import_scripts_phase00_INBOX_offsets_C0B587D7_C0B587D7():
    mod = importlib.import_module("scripts.phase00.INBOX.offsets_C0B587D7_C0B587D7")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
