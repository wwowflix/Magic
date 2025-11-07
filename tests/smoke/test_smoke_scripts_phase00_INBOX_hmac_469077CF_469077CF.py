import importlib, types


def test_import_scripts_phase00_INBOX_hmac_469077CF_469077CF():
    mod = importlib.import_module("scripts.phase00.INBOX.hmac_469077CF_469077CF")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
