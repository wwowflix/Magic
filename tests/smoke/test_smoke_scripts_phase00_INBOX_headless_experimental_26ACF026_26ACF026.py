import importlib, types


def test_import_scripts_phase00_INBOX_headless_experimental_26ACF026_26ACF026():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.headless_experimental_26ACF026_26ACF026"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
