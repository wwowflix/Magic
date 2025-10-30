import importlib, types


def test_import_scripts_phase00_INBOX_metadata_legacy_6AFE3DF6_6AFE3DF6():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.metadata_legacy_6AFE3DF6_6AFE3DF6"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
