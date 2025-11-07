import importlib, types


def test_import_scripts_phase00_INBOX_big5prober_94F31FC0_94F31FC0():
    mod = importlib.import_module("scripts.phase00.INBOX.big5prober_94F31FC0_94F31FC0")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
