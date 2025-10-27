import importlib, types

def test_import_scripts_phase00_INBOX_g95_E4A81388_E4A81388():
    mod = importlib.import_module("scripts.phase00.INBOX.g95_E4A81388_E4A81388")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
