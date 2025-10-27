import importlib, types

def test_import_scripts_phase00_INBOX_makefile_9DBCEDDE_9DBCEDDE():
    mod = importlib.import_module("scripts.phase00.INBOX.makefile_9DBCEDDE_9DBCEDDE")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
