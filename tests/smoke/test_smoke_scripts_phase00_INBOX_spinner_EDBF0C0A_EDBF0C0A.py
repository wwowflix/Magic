import importlib, types

def test_import_scripts_phase00_INBOX_spinner_EDBF0C0A_EDBF0C0A():
    mod = importlib.import_module("scripts.phase00.INBOX.spinner_EDBF0C0A_EDBF0C0A")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
