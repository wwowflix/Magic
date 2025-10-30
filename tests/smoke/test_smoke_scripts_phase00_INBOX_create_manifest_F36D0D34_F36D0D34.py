import importlib, types


def test_import_scripts_phase00_INBOX_create_manifest_F36D0D34_F36D0D34():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.create_manifest_F36D0D34_F36D0D34"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
