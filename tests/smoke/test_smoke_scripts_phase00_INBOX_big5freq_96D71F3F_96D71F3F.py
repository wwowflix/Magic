import importlib, types


def test_import_scripts_phase00_INBOX_big5freq_96D71F3F_96D71F3F():
    mod = importlib.import_module("scripts.phase00.INBOX.big5freq_96D71F3F_96D71F3F")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
