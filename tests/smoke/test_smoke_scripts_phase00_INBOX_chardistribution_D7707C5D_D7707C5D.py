import importlib, types


def test_import_scripts_phase00_INBOX_chardistribution_D7707C5D_D7707C5D():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.chardistribution_D7707C5D_D7707C5D"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
