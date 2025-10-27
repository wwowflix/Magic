import importlib, types

def test_import_scripts_phase00_INBOX_readers_B636D8C4_B636D8C4():
    mod = importlib.import_module("scripts.phase00.INBOX.readers_B636D8C4_B636D8C4")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
