import importlib, types

def test_import_scripts_phase00_INBOX_weekly_consolidator_6AE379D8_6AE379D8():
    mod = importlib.import_module("scripts.phase00.INBOX.weekly_consolidator_6AE379D8_6AE379D8")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
