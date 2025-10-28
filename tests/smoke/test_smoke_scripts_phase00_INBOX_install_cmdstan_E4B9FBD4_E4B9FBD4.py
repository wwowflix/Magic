import importlib, types

def test_import_scripts_phase00_INBOX_install_cmdstan_E4B9FBD4_E4B9FBD4():
    mod = importlib.import_module("scripts.phase00.INBOX.install_cmdstan_E4B9FBD4_E4B9FBD4")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
