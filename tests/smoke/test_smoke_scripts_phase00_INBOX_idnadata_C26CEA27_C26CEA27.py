import importlib, types

def test_import_scripts_phase00_INBOX_idnadata_C26CEA27_C26CEA27():
    mod = importlib.import_module("scripts.phase00.INBOX.idnadata_C26CEA27_C26CEA27")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
