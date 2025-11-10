import importlib, types


def test_import_scripts_phase00_INBOX_pickle_C265EE97_C265EE97():
    mod = importlib.import_module("scripts.phase00.INBOX.pickle_C265EE97_C265EE97")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
