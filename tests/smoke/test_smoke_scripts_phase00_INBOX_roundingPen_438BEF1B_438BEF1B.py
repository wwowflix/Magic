import importlib, types


def test_import_scripts_phase00_INBOX_roundingPen_438BEF1B_438BEF1B():
    mod = importlib.import_module("scripts.phase00.INBOX.roundingPen_438BEF1B_438BEF1B")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
