import importlib, types


def test_import_scripts_phase00_INBOX__soft_9276B7E5_9276B7E5():
    mod = importlib.import_module("scripts.phase00.INBOX._soft_9276B7E5_9276B7E5")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
