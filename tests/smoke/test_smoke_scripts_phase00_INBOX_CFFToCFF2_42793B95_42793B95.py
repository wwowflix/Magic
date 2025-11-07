import importlib, types


def test_import_scripts_phase00_INBOX_CFFToCFF2_42793B95_42793B95():
    mod = importlib.import_module("scripts.phase00.INBOX.CFFToCFF2_42793B95_42793B95")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
