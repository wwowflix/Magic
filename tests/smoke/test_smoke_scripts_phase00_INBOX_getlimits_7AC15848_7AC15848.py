import importlib, types

def test_import_scripts_phase00_INBOX_getlimits_7AC15848_7AC15848():
    mod = importlib.import_module("scripts.phase00.INBOX.getlimits_7AC15848_7AC15848")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
