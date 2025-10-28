import importlib, types

def test_import_scripts_phase00_INBOX_pg_BC0779E4_BC0779E4():
    mod = importlib.import_module("scripts.phase00.INBOX.pg_BC0779E4_BC0779E4")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
