import importlib, types

def test_import_scripts_phase00_INBOX__ssl_compat_9573AFE2_9573AFE2():
    mod = importlib.import_module("scripts.phase00.INBOX._ssl_compat_9573AFE2_9573AFE2")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
