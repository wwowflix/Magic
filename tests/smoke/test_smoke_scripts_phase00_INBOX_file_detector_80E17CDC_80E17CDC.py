import importlib, types


def test_import_scripts_phase00_INBOX_file_detector_80E17CDC_80E17CDC():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.file_detector_80E17CDC_80E17CDC"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
