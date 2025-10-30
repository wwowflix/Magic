import importlib, types


def test_import_scripts_phase00_INBOX__odswriter_2FAADD3E_2FAADD3E():
    mod = importlib.import_module("scripts.phase00.INBOX._odswriter_2FAADD3E_2FAADD3E")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
