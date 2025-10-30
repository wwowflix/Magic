import importlib, types


def test_import_scripts_phase00_INBOX__cookiejar_F3DDD25A_F3DDD25A():
    mod = importlib.import_module("scripts.phase00.INBOX._cookiejar_F3DDD25A_F3DDD25A")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
