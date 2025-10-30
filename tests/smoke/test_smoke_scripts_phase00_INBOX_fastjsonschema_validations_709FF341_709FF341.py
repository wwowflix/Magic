import importlib, types


def test_import_scripts_phase00_INBOX_fastjsonschema_validations_709FF341_709FF341():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.fastjsonschema_validations_709FF341_709FF341"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
