import importlib, types

def test_import_scripts_phase00_INBOX_setup_2_036962E4_036962E4():
    mod = importlib.import_module("scripts.phase00.INBOX.setup_2_036962E4_036962E4")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
