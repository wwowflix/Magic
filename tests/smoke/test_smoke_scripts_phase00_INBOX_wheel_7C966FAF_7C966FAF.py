import importlib, types


def test_import_scripts_phase00_INBOX_wheel_7C966FAF_7C966FAF():
    mod = importlib.import_module("scripts.phase00.INBOX.wheel_7C966FAF_7C966FAF")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
