import importlib, types


def test_import_scripts_phase00_INBOX_ttFont_AD319634_AD319634():
    mod = importlib.import_module("scripts.phase00.INBOX.ttFont_AD319634_AD319634")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
