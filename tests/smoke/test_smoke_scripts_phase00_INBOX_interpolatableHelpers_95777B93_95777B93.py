import importlib, types

def test_import_scripts_phase00_INBOX_interpolatableHelpers_95777B93_95777B93():
    mod = importlib.import_module("scripts.phase00.INBOX.interpolatableHelpers_95777B93_95777B93")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
