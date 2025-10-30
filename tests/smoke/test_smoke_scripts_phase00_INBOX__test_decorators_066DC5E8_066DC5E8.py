import importlib, types


def test_import_scripts_phase00_INBOX__test_decorators_066DC5E8_066DC5E8():
    mod = importlib.import_module(
        "scripts.phase00.INBOX._test_decorators_066DC5E8_066DC5E8"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
