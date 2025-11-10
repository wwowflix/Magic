import importlib, types


def test_import_scripts_phase00_INBOX__error_FB98CC72_FB98CC72():
    mod = importlib.import_module("scripts.phase00.INBOX._error_FB98CC72_FB98CC72")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
