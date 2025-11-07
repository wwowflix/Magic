import importlib, types


def test_import_scripts_phase00_INBOX_filterPen_90A4AF2E_90A4AF2E():
    mod = importlib.import_module("scripts.phase00.INBOX.filterPen_90A4AF2E_90A4AF2E")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
