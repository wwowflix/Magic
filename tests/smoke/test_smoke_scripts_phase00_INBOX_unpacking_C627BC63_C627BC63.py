import importlib, types

def test_import_scripts_phase00_INBOX_unpacking_C627BC63_C627BC63():
    mod = importlib.import_module("scripts.phase00.INBOX.unpacking_C627BC63_C627BC63")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
