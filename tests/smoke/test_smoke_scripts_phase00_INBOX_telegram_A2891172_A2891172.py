import importlib, types


def test_import_scripts_phase00_INBOX_telegram_A2891172_A2891172():
    mod = importlib.import_module("scripts.phase00.INBOX.telegram_A2891172_A2891172")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
