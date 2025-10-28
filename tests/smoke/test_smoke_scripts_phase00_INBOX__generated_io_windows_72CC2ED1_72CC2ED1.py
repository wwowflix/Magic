import importlib, types

def test_import_scripts_phase00_INBOX__generated_io_windows_72CC2ED1_72CC2ED1():
    mod = importlib.import_module("scripts.phase00.INBOX._generated_io_windows_72CC2ED1_72CC2ED1")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
