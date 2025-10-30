import importlib, types


def test_import_scripts_phase00_INBOX_sanitizer_2FA28985_2FA28985():
    mod = importlib.import_module("scripts.phase00.INBOX.sanitizer_2FA28985_2FA28985")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
