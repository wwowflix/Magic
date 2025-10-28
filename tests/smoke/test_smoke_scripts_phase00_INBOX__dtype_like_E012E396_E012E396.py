import importlib, types

def test_import_scripts_phase00_INBOX__dtype_like_E012E396_E012E396():
    mod = importlib.import_module("scripts.phase00.INBOX._dtype_like_E012E396_E012E396")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
