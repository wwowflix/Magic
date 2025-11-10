import importlib, types


def test_import_scripts_phase00_INBOX_flatiter_E0CC376A_E0CC376A():
    mod = importlib.import_module("scripts.phase00.INBOX.flatiter_E0CC376A_E0CC376A")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
