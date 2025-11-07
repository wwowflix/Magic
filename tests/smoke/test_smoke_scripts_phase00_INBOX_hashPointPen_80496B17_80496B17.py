import importlib, types


def test_import_scripts_phase00_INBOX_hashPointPen_80496B17_80496B17():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.hashPointPen_80496B17_80496B17"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
