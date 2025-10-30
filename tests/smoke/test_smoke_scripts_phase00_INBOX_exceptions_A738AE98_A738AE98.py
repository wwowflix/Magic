import importlib, types


def test_import_scripts_phase00_INBOX_exceptions_A738AE98_A738AE98():
    mod = importlib.import_module("scripts.phase00.INBOX.exceptions_A738AE98_A738AE98")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
