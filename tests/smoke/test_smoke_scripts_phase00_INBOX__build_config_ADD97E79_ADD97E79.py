import importlib, types


def test_import_scripts_phase00_INBOX__build_config_ADD97E79_ADD97E79():
    mod = importlib.import_module(
        "scripts.phase00.INBOX._build_config_ADD97E79_ADD97E79"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
