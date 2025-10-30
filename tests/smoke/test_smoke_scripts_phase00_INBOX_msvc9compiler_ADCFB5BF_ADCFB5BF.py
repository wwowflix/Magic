import importlib, types


def test_import_scripts_phase00_INBOX_msvc9compiler_ADCFB5BF_ADCFB5BF():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.msvc9compiler_ADCFB5BF_ADCFB5BF"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
