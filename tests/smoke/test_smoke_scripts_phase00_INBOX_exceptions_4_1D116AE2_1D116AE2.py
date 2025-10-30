import importlib, types


def test_import_scripts_phase00_INBOX_exceptions_4_1D116AE2_1D116AE2():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.exceptions_4_1D116AE2_1D116AE2"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
