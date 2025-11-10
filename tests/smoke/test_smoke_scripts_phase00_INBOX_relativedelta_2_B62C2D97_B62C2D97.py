import importlib, types


def test_import_scripts_phase00_INBOX_relativedelta_2_B62C2D97_B62C2D97():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.relativedelta_2_B62C2D97_B62C2D97"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
