import importlib, types

def test_import_scripts_phase00_INBOX_setupcfg_DE47B6FE_DE47B6FE():
    mod = importlib.import_module("scripts.phase00.INBOX.setupcfg_DE47B6FE_DE47B6FE")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
