import importlib, types


def test_import_scripts_phase00_INBOX_metadata_editable_EAE94176_EAE94176():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.metadata_editable_EAE94176_EAE94176"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
