import importlib, types


def test_import_scripts_phase00_INBOX_StandardEncoding_128DC018_128DC018():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.StandardEncoding_128DC018_128DC018"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
