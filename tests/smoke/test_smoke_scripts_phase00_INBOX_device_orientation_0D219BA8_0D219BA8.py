import importlib, types


def test_import_scripts_phase00_INBOX_device_orientation_0D219BA8_0D219BA8():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.device_orientation_0D219BA8_0D219BA8"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
