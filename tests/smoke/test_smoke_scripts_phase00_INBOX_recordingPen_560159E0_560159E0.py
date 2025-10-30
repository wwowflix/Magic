import importlib, types


def test_import_scripts_phase00_INBOX_recordingPen_560159E0_560159E0():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.recordingPen_560159E0_560159E0"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
