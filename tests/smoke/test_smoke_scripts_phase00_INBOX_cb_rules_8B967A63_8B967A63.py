import importlib, types

def test_import_scripts_phase00_INBOX_cb_rules_8B967A63_8B967A63():
    mod = importlib.import_module("scripts.phase00.INBOX.cb_rules_8B967A63_8B967A63")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
