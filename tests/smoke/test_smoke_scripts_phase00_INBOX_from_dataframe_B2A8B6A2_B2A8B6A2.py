import importlib, types


def test_import_scripts_phase00_INBOX_from_dataframe_B2A8B6A2_B2A8B6A2():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.from_dataframe_B2A8B6A2_B2A8B6A2"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
