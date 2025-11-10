import importlib, types


def test_import_scripts_phase00_INBOX_func2subr_8787ABBD_8787ABBD():
    mod = importlib.import_module("scripts.phase00.INBOX.func2subr_8787ABBD_8787ABBD")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
