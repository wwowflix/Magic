import importlib, types

def test_import_scripts_phase00_INBOX_rtf_CFFC8A01_CFFC8A01():
    mod = importlib.import_module("scripts.phase00.INBOX.rtf_CFFC8A01_CFFC8A01")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
