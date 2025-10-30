import importlib, types


def test_import_scripts_phase00_INBOX_storage_manager_80B053AF_80B053AF():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.storage_manager_80B053AF_80B053AF"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
