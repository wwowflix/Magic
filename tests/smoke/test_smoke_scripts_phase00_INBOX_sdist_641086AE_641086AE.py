import importlib, types


def test_import_scripts_phase00_INBOX_sdist_641086AE_641086AE():
    mod = importlib.import_module("scripts.phase00.INBOX.sdist_641086AE_641086AE")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
