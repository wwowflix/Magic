import importlib, types


def test_import_scripts_phase00_INBOX__common_ED415B93_ED415B93():
    mod = importlib.import_module("scripts.phase00.INBOX._common_ED415B93_ED415B93")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
