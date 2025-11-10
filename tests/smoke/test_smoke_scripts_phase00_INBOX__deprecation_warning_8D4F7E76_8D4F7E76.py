import importlib, types


def test_import_scripts_phase00_INBOX__deprecation_warning_8D4F7E76_8D4F7E76():
    mod = importlib.import_module(
        "scripts.phase00.INBOX._deprecation_warning_8D4F7E76_8D4F7E76"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
