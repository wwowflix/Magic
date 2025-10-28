import importlib, types

def test_import_scripts_phase00_INBOX_avarPlanner_B8B306B0_B8B306B0():
    mod = importlib.import_module("scripts.phase00.INBOX.avarPlanner_B8B306B0_B8B306B0")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
