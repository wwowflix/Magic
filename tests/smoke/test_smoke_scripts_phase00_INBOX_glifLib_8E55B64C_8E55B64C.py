import importlib, types

def test_import_scripts_phase00_INBOX_glifLib_8E55B64C_8E55B64C():
    mod = importlib.import_module("scripts.phase00.INBOX.glifLib_8E55B64C_8E55B64C")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
