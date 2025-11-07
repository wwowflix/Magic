import importlib, types


def test_import_scripts_phase00_INBOX_fpdf_9FD4C0E6_9FD4C0E6():
    mod = importlib.import_module("scripts.phase00.INBOX.fpdf_9FD4C0E6_9FD4C0E6")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
