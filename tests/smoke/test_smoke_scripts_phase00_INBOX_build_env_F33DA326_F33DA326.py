import importlib, types

def test_import_scripts_phase00_INBOX_build_env_F33DA326_F33DA326():
    mod = importlib.import_module("scripts.phase00.INBOX.build_env_F33DA326_F33DA326")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
