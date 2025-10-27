import importlib, types

def test_import_scripts_phase00_INBOX_linalg_D0827E65_D0827E65():
    mod = importlib.import_module("scripts.phase00.INBOX.linalg_D0827E65_D0827E65")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
