import importlib, types


def test_import_scripts_phase00_INBOX_socks_FA26AB75_FA26AB75():
    mod = importlib.import_module("scripts.phase00.INBOX.socks_FA26AB75_FA26AB75")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
