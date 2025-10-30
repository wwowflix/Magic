import importlib, types


def test_import_scripts_phase00_INBOX_editable_legacy_D126889C_D126889C():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.editable_legacy_D126889C_D126889C"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
