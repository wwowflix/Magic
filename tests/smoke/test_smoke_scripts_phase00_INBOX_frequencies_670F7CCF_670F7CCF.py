import importlib, types


def test_import_scripts_phase00_INBOX_frequencies_670F7CCF_670F7CCF():
    mod = importlib.import_module("scripts.phase00.INBOX.frequencies_670F7CCF_670F7CCF")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
