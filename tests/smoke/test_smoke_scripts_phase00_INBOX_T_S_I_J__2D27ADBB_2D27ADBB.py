import importlib, types


def test_import_scripts_phase00_INBOX_T_S_I_J__2D27ADBB_2D27ADBB():
    mod = importlib.import_module("scripts.phase00.INBOX.T_S_I_J__2D27ADBB_2D27ADBB")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
