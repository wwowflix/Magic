import importlib, types


def test_import_scripts_phase00_INBOX_one_time_organizer_055564E4_055564E4():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.one_time_organizer_055564E4_055564E4"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
