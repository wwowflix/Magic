import importlib, types


def test_import_scripts_phase00_INBOX_dsa_9446EDF9_9446EDF9():
    mod = importlib.import_module("scripts.phase00.INBOX.dsa_9446EDF9_9446EDF9")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
