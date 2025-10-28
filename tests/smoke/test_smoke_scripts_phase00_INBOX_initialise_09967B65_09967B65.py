import importlib, types

def test_import_scripts_phase00_INBOX_initialise_09967B65_09967B65():
    mod = importlib.import_module("scripts.phase00.INBOX.initialise_09967B65_09967B65")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
