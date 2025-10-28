import importlib, types

def test_import_scripts_phase00_INBOX_windows_support_F8897C21_F8897C21():
    mod = importlib.import_module("scripts.phase00.INBOX.windows_support_F8897C21_F8897C21")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
