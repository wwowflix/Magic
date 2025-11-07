import importlib, types


def test_import_scripts_phase00_INBOX__html5lib_2_DCC5EADB_DCC5EADB():
    mod = importlib.import_module("scripts.phase00.INBOX._html5lib_2_DCC5EADB_DCC5EADB")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
