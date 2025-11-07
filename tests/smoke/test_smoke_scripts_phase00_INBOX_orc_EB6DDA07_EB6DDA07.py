import importlib, types


def test_import_scripts_phase00_INBOX_orc_EB6DDA07_EB6DDA07():
    mod = importlib.import_module("scripts.phase00.INBOX.orc_EB6DDA07_EB6DDA07")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
