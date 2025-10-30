import importlib, types


def test_import_scripts_phase00_INBOX_encoding_test_9C1F1376_9C1F1376():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.encoding_test_9C1F1376_9C1F1376"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
