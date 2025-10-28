import importlib, types

def test_import_scripts_phase00_INBOX_env_loader_31872BC0_31872BC0():
    mod = importlib.import_module("scripts.phase00.INBOX.env_loader_31872BC0_31872BC0")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
