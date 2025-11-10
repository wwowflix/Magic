import importlib, types


def test_import_scripts_phase00_INBOX_quarantine_agent_backup_8770D9B1_8770D9B1():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.quarantine_agent_backup_8770D9B1_8770D9B1"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
