import importlib, types


def test_import_scripts_phase00_INBOX_aead_173972C7_173972C7():
    mod = importlib.import_module("scripts.phase00.INBOX.aead_173972C7_173972C7")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
