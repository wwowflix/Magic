import importlib, types

def test_import_scripts_phase00_INBOX_switch_to_4094EC28_4094EC28():
    mod = importlib.import_module("scripts.phase00.INBOX.switch_to_4094EC28_4094EC28")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
