import importlib, types


def test_import_scripts_phase00_INBOX_upload_93D06CD7_93D06CD7():
    mod = importlib.import_module("scripts.phase00.INBOX.upload_93D06CD7_93D06CD7")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
