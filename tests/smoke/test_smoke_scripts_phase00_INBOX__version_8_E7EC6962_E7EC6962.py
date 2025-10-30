import importlib, types


def test_import_scripts_phase00_INBOX__version_8_E7EC6962_E7EC6962():
    mod = importlib.import_module("scripts.phase00.INBOX._version_8_E7EC6962_E7EC6962")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
