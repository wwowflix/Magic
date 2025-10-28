import importlib, types

def test_import_scripts_phase00_INBOX_scanner_96DABBD7_96DABBD7():
    mod = importlib.import_module("scripts.phase00.INBOX.scanner_96DABBD7_96DABBD7")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
