import importlib, types

def test_import_scripts_phase00_INBOX_asyn_wrapper_B9944E71_B9944E71():
    mod = importlib.import_module("scripts.phase00.INBOX.asyn_wrapper_B9944E71_B9944E71")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
