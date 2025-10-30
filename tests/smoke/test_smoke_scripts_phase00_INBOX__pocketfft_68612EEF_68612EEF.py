import importlib, types


def test_import_scripts_phase00_INBOX__pocketfft_68612EEF_68612EEF():
    mod = importlib.import_module("scripts.phase00.INBOX._pocketfft_68612EEF_68612EEF")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
