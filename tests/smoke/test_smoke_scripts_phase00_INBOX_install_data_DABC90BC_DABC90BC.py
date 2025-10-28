import importlib, types

def test_import_scripts_phase00_INBOX_install_data_DABC90BC_DABC90BC():
    mod = importlib.import_module("scripts.phase00.INBOX.install_data_DABC90BC_DABC90BC")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
