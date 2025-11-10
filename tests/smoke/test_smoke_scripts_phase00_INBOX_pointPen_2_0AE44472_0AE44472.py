import importlib, types


def test_import_scripts_phase00_INBOX_pointPen_2_0AE44472_0AE44472():
    mod = importlib.import_module("scripts.phase00.INBOX.pointPen_2_0AE44472_0AE44472")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
