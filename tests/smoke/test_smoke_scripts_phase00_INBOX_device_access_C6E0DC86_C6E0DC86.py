import importlib, types


def test_import_scripts_phase00_INBOX_device_access_C6E0DC86_C6E0DC86():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.device_access_C6E0DC86_C6E0DC86"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
