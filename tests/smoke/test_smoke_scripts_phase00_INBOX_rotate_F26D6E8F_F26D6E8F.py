import importlib, types


def test_import_scripts_phase00_INBOX_rotate_F26D6E8F_F26D6E8F():
    mod = importlib.import_module("scripts.phase00.INBOX.rotate_F26D6E8F_F26D6E8F")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
