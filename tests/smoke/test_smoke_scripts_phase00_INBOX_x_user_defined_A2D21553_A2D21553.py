import importlib, types

def test_import_scripts_phase00_INBOX_x_user_defined_A2D21553_A2D21553():
    mod = importlib.import_module("scripts.phase00.INBOX.x_user_defined_A2D21553_A2D21553")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
