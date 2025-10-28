import importlib, types

def test_import_scripts_phase00_INBOX_split_141D4DBA_141D4DBA():
    mod = importlib.import_module("scripts.phase00.INBOX.split_141D4DBA_141D4DBA")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
