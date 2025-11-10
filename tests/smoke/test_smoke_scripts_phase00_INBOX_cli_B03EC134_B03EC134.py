import importlib, types


def test_import_scripts_phase00_INBOX_cli_B03EC134_B03EC134():
    mod = importlib.import_module("scripts.phase00.INBOX.cli_B03EC134_B03EC134")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
