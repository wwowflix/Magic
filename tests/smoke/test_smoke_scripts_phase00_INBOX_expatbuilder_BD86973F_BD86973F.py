import importlib, types

def test_import_scripts_phase00_INBOX_expatbuilder_BD86973F_BD86973F():
    mod = importlib.import_module("scripts.phase00.INBOX.expatbuilder_BD86973F_BD86973F")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
