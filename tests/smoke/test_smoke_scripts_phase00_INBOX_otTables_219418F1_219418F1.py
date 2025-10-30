import importlib, types


def test_import_scripts_phase00_INBOX_otTables_219418F1_219418F1():
    mod = importlib.import_module("scripts.phase00.INBOX.otTables_219418F1_219418F1")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
